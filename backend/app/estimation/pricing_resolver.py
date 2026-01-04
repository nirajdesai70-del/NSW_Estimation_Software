"""
Pricing Resolver
Phase-5: Deterministic rate resolution with manual override governance
"""
from __future__ import annotations

from typing import Optional, List, Protocol
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.estimation.types import RateSource, PriceSnapshot, LineInput
from app.validators.override_rules import OverrideRulesValidator
from app.audit.logger import AuditLogger
from app.estimation.decimal_norm import qrate
from app.estimation.rate_source_map import internal_to_db_rate_source


class ProductRateLookup(Protocol):
    """Protocol for Product (L2 commercial identity) rate lookup service (Phase-5 schema: prices.product_id)."""

    def get_rate_for_product(self, *, product_id: int, quote_id: int) -> Decimal:
        """
        Return the effective product rate for this quote context.

        Note: quote_id is kept for future-tiering logic (customer tier, date rules, etc.).
        In Phase-5, most implementations can ignore quote_id and just use product_id + effective_date.

        Args:
            product_id: products.id (current L2 commercial identity reference)
            quote_id: quotation identifier (context)

        Returns:
            Decimal rate
        """
        ...


class PricingResolver:
    """
    Resolves line item rates with deterministic logic.

    Supports:
    - PRICELIST: Rate from product pricelist (default)
    - MANUAL: Manual override (requires role + reason)
    - FIXED_NO_DISCOUNT: Quotation-scoped fixed pricing (no discounts)
    - UNRESOLVED: Safe zero contribution (handled elsewhere too)

    Persists rate snapshots for audit and determinism.
    """

    def __init__(self, db: Session, *, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def resolve_line_rate(
        self,
        *,
        quote_id: int,
        line: LineInput,
        user_id: int,
        user_roles: List[str],
        product_rate_lookup: ProductRateLookup,
    ) -> PriceSnapshot:
        """
        Resolve rate for a line item.

        Enforces:
        - MANUAL requires role + reason + positive override_rate
        - PRICELIST requires product_id and valid product rate
        - FIXED_NO_DISCOUNT preserves fixed rate (override_rate), no pricelist consultation
        - UNRESOLVED yields applied_rate = 0
        """

        # FIXED_NO_DISCOUNT: preserve fixed rate, discount is handled elsewhere (schema enforces discount_pct=0)
        if line.rate_source == RateSource.FIXED_NO_DISCOUNT:
            if line.override_rate is None:
                raise ValueError("override_rate is required for FIXED_NO_DISCOUNT rate_source")

            applied_rate = qrate(line.override_rate)  # type: ignore[arg-type]
            return PriceSnapshot(
                sku_rate=None,  # keep field name for now (legacy); value is not applicable
                override_rate=qrate(line.override_rate),  # type: ignore[arg-type]
                applied_rate=applied_rate,
                rate_source=RateSource.FIXED_NO_DISCOUNT,
            )

        # UNRESOLVED: safe zero (G-05 / G-03)
        if line.rate_source == RateSource.UNRESOLVED:
            return PriceSnapshot(
                sku_rate=None,
                override_rate=None,
                applied_rate=qrate(Decimal("0")),
                rate_source=RateSource.UNRESOLVED,
            )

        # MANUAL: validate governance
        if line.rate_source == RateSource.MANUAL:
            OverrideRulesValidator.validate_override_request(
                rate_source=line.rate_source,
                override_rate=line.override_rate,
                override_reason=line.override_reason,
                user_roles=user_roles,
            )

        # Resolve rate based on source
        if line.rate_source == RateSource.MANUAL:
            if line.override_rate is None:
                raise ValueError("override_rate is required for MANUAL rate_source")

            applied_rate = qrate(line.override_rate)  # type: ignore[arg-type]
            return PriceSnapshot(
                sku_rate=None,  # optional metadata; not required for correctness
                override_rate=qrate(line.override_rate),  # type: ignore[arg-type]
                applied_rate=applied_rate,
                rate_source=RateSource.MANUAL,
            )

        if line.rate_source == RateSource.PRICELIST:
            # Phase-5 schema: quote_bom_items.product_id (NOT sku_id)
            if line.product_id is None:
                raise ValueError("product_id is required for PRICELIST rate_source")

            product_rate = qrate(
                product_rate_lookup.get_rate_for_product(
                    product_id=line.product_id,
                    quote_id=quote_id,
                )
            )

            return PriceSnapshot(
                sku_rate=product_rate,  # keep field name for now (legacy); value is the pricelist rate
                override_rate=None,
                applied_rate=product_rate,
                rate_source=RateSource.PRICELIST,
            )

        raise ValueError(f"Unsupported rate_source: {line.rate_source}")

    def snapshot_line_rate(
        self,
        *,
        quote_id: int,
        line_id: int,
        snapshot: PriceSnapshot,
        actor_id: int,
        override_reason: Optional[str] = None,
        product_id: Optional[int] = None,
    ) -> None:
        """
        Persist rate snapshots to quote_bom_items table.

        Option A locked: internal MANUAL -> DB MANUAL_WITH_DISCOUNT
        FIXED_NO_DISCOUNT persists as DB FIXED_NO_DISCOUNT and enforces discount_pct=0.

        NOTE: No commit here. Caller controls transaction atomicity (Policy-1 safe).
        """
        db_rate_source = internal_to_db_rate_source(snapshot.rate_source)

        # Read current values for accurate audit old_values
        current_result = self.db.execute(
            text(
                """
                SELECT
                    rate_source,
                    rate,
                    COALESCE(override_rate, NULL) as override_rate,
                    COALESCE(override_reason, NULL) as override_reason,
                    discount_pct
                FROM quote_bom_items
                WHERE id = :line_id AND quotation_id = :quote_id
                """
            ),
            {"line_id": line_id, "quote_id": quote_id},
        ).mappings().first()

        old_values = dict(current_result) if current_result else {}

        update_fields = [
            "rate_source = :rate_source",
            "rate = :applied_rate",
            "updated_at = CURRENT_TIMESTAMP",
        ]

        update_params = {
            "rate_source": db_rate_source,
            "applied_rate": snapshot.applied_rate,
            "line_id": line_id,
            "quote_id": quote_id,
        }

        # MANUAL or FIXED_NO_DISCOUNT -> keep override trace columns populated
        if snapshot.rate_source in (RateSource.MANUAL, RateSource.FIXED_NO_DISCOUNT):
            update_fields.extend(
                [
                    "override_rate = :override_rate",
                    "override_reason = :override_reason",
                    "overridden_by = :overridden_by",
                    "overridden_at = CURRENT_TIMESTAMP",
                ]
            )
            update_params.update(
                {
                    "override_rate": snapshot.override_rate,
                    "override_reason": override_reason,
                    "overridden_by": actor_id,
                }
            )

            # G-06 hard rule: discount_pct forced 0 for FIXED_NO_DISCOUNT
            if snapshot.rate_source == RateSource.FIXED_NO_DISCOUNT:
                update_fields.append("discount_pct = 0")

        else:
            # PRICELIST or UNRESOLVED -> clear override fields
            update_fields.extend(
                [
                    "override_rate = NULL",
                    "override_reason = NULL",
                    "overridden_by = NULL",
                    # preserve overridden_at for history
                ]
            )

        update_stmt = text(
            f"""
            UPDATE quote_bom_items
            SET {', '.join(update_fields)}
            WHERE id = :line_id AND quotation_id = :quote_id
            """
        )

        self.db.execute(update_stmt, update_params)

        action_type = (
            "OVERRIDE_RATE"
            if snapshot.rate_source in (RateSource.MANUAL, RateSource.FIXED_NO_DISCOUNT)
            else "RATE_SET"
        )

        AuditLogger.log_event(
            db=self.db,
            tenant_id=self.tenant_id,
            actor_id=actor_id,
            action_type=action_type,
            resource_type="quote_bom_item",
            resource_id=line_id,
            old_values=old_values,
            new_values={
                "rate_source": db_rate_source,
                "rate": str(snapshot.applied_rate),
                "override_rate": str(snapshot.override_rate) if snapshot.override_rate else None,
                "override_reason": override_reason,
                "discount_pct": "0" if snapshot.rate_source == RateSource.FIXED_NO_DISCOUNT else None,
            },
            metadata={"quote_id": quote_id, "product_id": product_id},
        )

        # IMPORTANT: Do NOT commit here. Caller controls atomicity.
