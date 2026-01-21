"""
Quotation endpoints
"""

from typing import List, Dict, Any
from decimal import Decimal
from fastapi import APIRouter, Depends, Path, Request

from app.core.raise_api_error import raise_api_error
from app.core.error_codes import ErrorCodes
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.api.v1.endpoints.pricing_helpers import get_tenant_id_from_request
from app.estimation.discount_rule_lookup import DiscountRuleLookup
from app.estimation.discount_engine import DiscountEngine
from app.estimation.discount_rule_types import DiscountScope
from app.api.v1.schemas.pricing import ApplyRecalcRequest, ApplyRecalcResponse
from app.api.v1.schemas.quotation_discount import (
    QuotationDiscountSetRequest,
    QuotationDiscountSetResponse,
)
from app.api.v1.schemas.quotation_copy import (
    CopyQuotationRequest,
    CopyQuotationResponse,
    CopyPanelResponse,
    CopyBOMResponse,
)
from app.api.v1.schemas.quotation_read import QuotationListItem, QuotationDetail
from app.api.v1.schemas.quotation_structure_read import PanelListItem, FeederListItem
from app.api.v1.schemas.bom_items_read import BOMItemListItem
from app.api.v1.schemas.cost_adders import (
    CostAdderUpsertRequest,
    CostAdderUpsertResponse,
)
from app.api.v1.schemas.cost_summary import QuotationCostSummaryResponse
from app.services.cost_adder_service import CostAdderService
from app.services.cost_summary_service import CostSummaryService
from app.validators.pricing_apply import (
    assert_apply_recalc_allowed,
    ApplyRecalcPermissionError,
)
from app.validators.discount_rules import assert_bulk_allowed, DiscountPermissionError
from app.audit.logger import AuditLogger
from app.estimation.tax_profile_lookup import TaxProfileLookup
from app.estimation.tax_engine import TaxEngine
from app.estimation.types import TaxMode
from app.estimation.decimal_norm import qrate

router = APIRouter()


def get_user_id_from_request(request: Request) -> int:
    """
    Extract user_id from request context.

    Phase-5: Stub implementation using header (similar to tenant_id).
    TODO: Replace with proper JWT/auth middleware.

    Args:
        request: FastAPI request object

    Returns:
        User ID (defaults to 1 for development)
    """
    user_id_header = request.headers.get("X-User-ID")
    if user_id_header:
        try:
            return int(user_id_header)
        except ValueError:
            pass

    # Default for development
    return 1


def get_user_roles_from_request(request: Request) -> List[str]:
    """Extract user roles from request context (stub for Phase-5)"""
    roles_header = request.headers.get("X-User-Roles")
    if roles_header:
        return [r.strip() for r in roles_header.split(",") if r.strip()]
    return ["Operator"]


def _compute_quote_pricing(
    *,
    db: Session,
    tenant_id: int,
    quotation_id: int,
) -> Dict[str, Any]:
    """
    Internal helper: Compute pricing for a quotation (shared by preview and apply-recalc).

    Returns deterministic pricing calculation with totals, GST, and flags.
    This is the single source of truth for pricing computation.

    Args:
        db: Database session
        tenant_id: Tenant ID
        quotation_id: Quotation ID

    Returns:
        Dict with keys: subtotal, quotation_discount_pct, discounted_subtotal, gst, grand_total, flags
    """
    # 1) Load quotation (tenant-safe)
    quote = (
        db.execute(
            text("""
            SELECT id, tenant_id, discount_pct, tax_profile_id, tax_mode
            FROM quotations
            WHERE id = :qid AND tenant_id = :tenant_id
        """),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not quote:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    quotation_discount_pct = Decimal(str(quote.get("discount_pct") or 0))
    tax_profile_id = quote.get("tax_profile_id")
    tax_mode_str = quote.get("tax_mode")

    # 2) Load quote lines (tenant-safe)
    lines = (
        db.execute(
            text("""
            SELECT
                id,
                product_id,
                quantity,
                rate,
                rate_source,
                discount_pct,
                discount_source,
                make_id,
                series_id,
                category_id,
                is_price_missing
            FROM quote_bom_items
            WHERE quotation_id = :qid
                AND tenant_id = :tenant_id
            ORDER BY id ASC
        """),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .all()
    )

    # 3) Load discount rules (quote-scoped)
    rule_lookup = DiscountRuleLookup(db)
    rules = rule_lookup.list_active_rules_for_quote(
        tenant_id=tenant_id, quotation_id=quotation_id
    )

    # Build fast lookup maps for rules (quote-scoped)
    site_rule = None
    make_series_rules = {}  # scope_key -> DiscountRule
    category_rules = {}  # category_id (int) -> DiscountRule

    for r in rules:
        if r.scope_type == DiscountScope.SITE and r.scope_key == "site":
            site_rule = r
        elif r.scope_type == DiscountScope.MAKE_SERIES:
            make_series_rules[r.scope_key] = r
        elif r.scope_type == DiscountScope.CATEGORY:
            # scope_key format: "category:{id}"
            if r.scope_key.startswith("category:"):
                try:
                    cid = int(r.scope_key.split("category:", 1)[1])
                    category_rules[cid] = r
                except ValueError:
                    # ignore malformed keys
                    pass

    # 4) Engine for discount calculations
    engine = DiscountEngine()

    # G-06: Split subtotals - fixed lines excluded from all discounts (including quotation-level)
    fixed_subtotal = qrate(Decimal("0"))
    discountable_subtotal = qrate(Decimal("0"))
    flags: List[str] = []

    for row in lines:
        qty = Decimal(str(row["quantity"] or 0))
        rate_source = row.get("rate_source")
        is_price_missing = bool(row.get("is_price_missing") or False)

        # G-05 + G-03: UNRESOLVED / price-missing must contribute zero
        if rate_source == "UNRESOLVED" or is_price_missing:
            applied_rate = qrate(Decimal("0"))
            net_rate = applied_rate
            line_amount = engine.compute_line_amount(qty=qty, net_rate=net_rate)
            # Contributes 0 anyway; keep flags for operator visibility
            if rate_source == "UNRESOLVED" and "HAS_UNRESOLVED_LINES" not in flags:
                flags.append("HAS_UNRESOLVED_LINES")
            if is_price_missing and "HAS_PRICE_MISSING_LINES" not in flags:
                flags.append("HAS_PRICE_MISSING_LINES")
            # No need to add to buckets; it will be zero
            continue

        applied_rate = qrate(Decimal(str(row["rate"] or 0)))

        # G-06: FIXED_NO_DISCOUNT - include in totals, exclude from all discounts
        if rate_source == "FIXED_NO_DISCOUNT":
            net_rate = applied_rate  # discount_pct is schema-forced to 0 anyway
            line_amount = engine.compute_line_amount(qty=qty, net_rate=net_rate)
            fixed_subtotal = qrate(fixed_subtotal + line_amount)
            if "HAS_FIXED_NO_DISCOUNT_LINES" not in flags:
                flags.append("HAS_FIXED_NO_DISCOUNT_LINES")
            continue

        # Normal discount resolution for PRICELIST, MANUAL_WITH_DISCOUNT
        line_discount_source = row.get("discount_source")
        line_discount_pct = (
            Decimal(str(row["discount_pct"]))
            if row.get("discount_pct") is not None
            else None
        )

        effective_discount_pct = Decimal("0")
        applied_scope = "NONE"
        local_flags: List[str] = []

        # 1) LINE override (highest precedence)
        if line_discount_source == "LINE" and line_discount_pct is not None:
            effective_discount_pct = line_discount_pct
            applied_scope = "LINE"

        else:
            # 2) MAKE_SERIES rule (match via make_id + series_id on the line)
            make_id = row.get("make_id")
            series_id = row.get("series_id")

            has_make_series_rules = len(make_series_rules) > 0
            if has_make_series_rules:
                if make_id and series_id:
                    key = f"make:{make_id}|series:{series_id}"
                    r = make_series_rules.get(key)
                    if r:
                        effective_discount_pct = r.discount_pct
                        applied_scope = "MAKE_SERIES"

                else:
                    # rules exist but this line can't be matched because identifiers missing
                    local_flags.append("MAKE_SERIES_MAPPING_NOT_AVAILABLE")

            # 3) CATEGORY rule
            if applied_scope == "NONE":
                cid = row.get("category_id")
                if cid is not None:
                    r = category_rules.get(int(cid))
                    if r:
                        effective_discount_pct = r.discount_pct
                        applied_scope = "CATEGORY"

            # 4) SITE rule (quote-level fallback)
            if applied_scope == "NONE" and site_rule is not None:
                effective_discount_pct = site_rule.discount_pct
                applied_scope = "SITE"

        # Use engine to validate/quantize via existing logic
        # (engine.validate_pct will be called inside apply_item_discount)
        net_rate = engine.apply_item_discount(
            applied_rate=applied_rate,
            item_discount_pct=effective_discount_pct,
        )

        # Collect flags (unique)
        for f in local_flags:
            if f not in flags:
                flags.append(f)

        # Compute line amount and add to discountable subtotal
        line_amount = engine.compute_line_amount(qty=qty, net_rate=net_rate)
        discountable_subtotal = qrate(discountable_subtotal + line_amount)

    # Combine subtotals
    subtotal = qrate(fixed_subtotal + discountable_subtotal)

    # G-06: Quotation-level discount applies only to discountable subtotal
    discounted_discountable = engine.apply_quotation_discount(
        subtotal=discountable_subtotal,
        quotation_discount_pct=quotation_discount_pct,
    )

    # Final discounted subtotal = fixed (no discount) + discounted discountable
    discounted_subtotal = qrate(fixed_subtotal + discounted_discountable)

    # 5) GST compute (if profile + mode set)
    gst_obj: Dict[str, Any] = {}
    grand_total = discounted_subtotal

    if tax_profile_id and tax_mode_str:
        if tax_mode_str not in (TaxMode.CGST_SGST.value, TaxMode.IGST.value):
            raise_api_error(
                status_code=422,
                error_code=ErrorCodes.SEMANTIC_INVALID_TAX_MODE,
                detail="Invalid tax_mode on quotation",
            )

        profile = TaxProfileLookup(db).get_profile(
            tenant_id=tenant_id,
            tax_profile_id=int(tax_profile_id),
        )

        gst = TaxEngine.calculate_gst(
            taxable_base=discounted_subtotal,
            tax_profile=profile,
            tax_mode=TaxMode(tax_mode_str),
        )

        gst_obj = {
            "tax_profile_id": gst.tax_profile_id,
            "tax_mode": gst.tax_mode,
            "taxable_base": str(gst.taxable_base),
            "cgst_pct": str(gst.cgst_pct),
            "sgst_pct": str(gst.sgst_pct),
            "igst_pct": str(gst.igst_pct),
            "cgst_amount": str(gst.cgst_amount),
            "sgst_amount": str(gst.sgst_amount),
            "igst_amount": str(gst.igst_amount),
            "tax_total": str(gst.tax_total),
        }

        grand_total = qrate(discounted_subtotal + gst.tax_total)

    return {
        "subtotal": str(subtotal),
        "quotation_discount_pct": str(quotation_discount_pct),
        "discounted_subtotal": str(discounted_subtotal),
        "gst": gst_obj,
        "grand_total": str(grand_total),
        "flags": flags,
    }


@router.get("/", response_model=List[QuotationListItem])
async def list_quotations(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    List quotations (Week-1 Day-1).

    Returns tenant-scoped list of quotations with basic fields.
    """
    rows = (
        db.execute(
            text("""
            SELECT id, quote_no, customer_name, status, created_at
            FROM quotations
            WHERE tenant_id = :tenant_id
            ORDER BY id ASC
        """),
            {"tenant_id": tenant_id},
        )
        .mappings()
        .all()
    )

    # Convert to list of dicts, handling datetime conversion
    result = []
    for row in rows:
        row_dict = dict(row)
        # Convert datetime to ISO string for JSON serialization
        if row_dict.get("created_at") and hasattr(row_dict["created_at"], "isoformat"):
            row_dict["created_at"] = row_dict["created_at"].isoformat()
        result.append(row_dict)

    return result


@router.get("/{quotation_id}/panels", response_model=List[PanelListItem])
async def list_panels(
    quotation_id: int = Path(..., description="Quotation ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    List panels for a quotation (Week-1 Day-2).

    Returns tenant-safe list of panels for the quotation or 404 if quotation not found.
    """
    # Ensure quotation exists tenant-safe (prevents leaking panel ids across tenants)
    q = db.execute(
        text("SELECT id FROM quotations WHERE id=:qid AND tenant_id=:tenant_id"),
        {"qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not q:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    rows = (
        db.execute(
            text("""
            SELECT id, quotation_id, name, quantity, rate, amount
            FROM quote_panels
            WHERE tenant_id = :tenant_id AND quotation_id = :qid
            ORDER BY id ASC
        """),
            {"tenant_id": tenant_id, "qid": quotation_id},
        )
        .mappings()
        .all()
    )

    return [dict(r) for r in rows]


@router.get(
    "/{quotation_id}/panels/{panel_id}/feeders", response_model=List[FeederListItem]
)
async def list_panel_feeders(
    quotation_id: int = Path(..., description="Quotation ID"),
    panel_id: int = Path(..., description="Panel ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    List feeders (level 0 BOMs) for a panel (Week-1 Day-2).

    Returns tenant-safe list of feeders (level 0 BOMs) for the panel.
    Feeder = quote_boms.level = 0
    """
    # Validate quotation exists tenant-safe
    q = db.execute(
        text("SELECT id FROM quotations WHERE id=:qid AND tenant_id=:tenant_id"),
        {"qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not q:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    # Validate panel belongs to quotation + tenant
    p = db.execute(
        text("""
            SELECT id
            FROM quote_panels
            WHERE id=:pid AND quotation_id=:qid AND tenant_id=:tenant_id
        """),
        {"pid": panel_id, "qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not p:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_RESOURCE,
            detail="Panel not found for quotation/tenant",
        )

    # Feeder = level 0 BOMs
    rows = (
        db.execute(
            text("""
            SELECT
                id,
                quotation_id,
                panel_id,
                level,
                name,
                quantity,
                rate,
                amount,
                instance_sequence_no,
                is_modified
            FROM quote_boms
            WHERE tenant_id = :tenant_id
              AND quotation_id = :qid
              AND panel_id = :pid
              AND level = 0
            ORDER BY id ASC
        """),
            {"tenant_id": tenant_id, "qid": quotation_id, "pid": panel_id},
        )
        .mappings()
        .all()
    )

    return [dict(r) for r in rows]


@router.get("/{quotation_id}/boms/{bom_id}/items", response_model=List[BOMItemListItem])
async def list_bom_items(
    quotation_id: int = Path(..., description="Quotation ID"),
    bom_id: int = Path(..., description="BOM ID (Feeder or child BOM)"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    List BOM items for a given BOM under a quotation (Week-1 Day-3).

    Read-only, tenant-safe, cost-neutral:
    - No pricing recompute
    - No QCA joins
    - Returns only fields already stored on quote_bom_items
    """
    # 1) Validate quotation exists (tenant-safe)
    q = db.execute(
        text("SELECT id FROM quotations WHERE id=:qid AND tenant_id=:tenant_id"),
        {"qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not q:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    # 2) Validate BOM belongs to quotation + tenant
    b = (
        db.execute(
            text("""
            SELECT id, panel_id, level
            FROM quote_boms
            WHERE id=:bid AND quotation_id=:qid AND tenant_id=:tenant_id
        """),
            {"bid": bom_id, "qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )
    if not b:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_RESOURCE,
            detail="BOM not found for quotation/tenant",
        )

    # 3) Fetch items for this BOM
    rows = (
        db.execute(
            text("""
            SELECT
                id,
                quotation_id,
                panel_id,
                bom_id,
                description,
                quantity,
                rate,
                amount,
                rate_source,
                is_price_missing
            FROM quote_bom_items
            WHERE tenant_id = :tenant_id
              AND quotation_id = :qid
              AND bom_id = :bid
            ORDER BY sequence_order ASC, id ASC
        """),
            {"tenant_id": tenant_id, "qid": quotation_id, "bid": bom_id},
        )
        .mappings()
        .all()
    )

    return [dict(r) for r in rows]


@router.post("/")
async def create_quotation():
    """Create quotation (to be implemented)"""
    return {"message": "Create quotation endpoint - to be implemented"}


@router.post(
    "/{quotation_id}/panels/{panel_id}/cost-adders",
    response_model=CostAdderUpsertResponse,
)
async def upsert_panel_cost_adder(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    panel_id: int = Path(..., description="Panel ID"),
    body: CostAdderUpsertRequest = ...,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Upsert (insert or update) a cost adder for a panel.

    Week-3 Day-1: Cost Adders write API (QCA only).
    Enforces uniqueness: one row per (tenant_id, quotation_id, panel_id, cost_head_code).
    """
    # 1) Validate quotation exists (tenant-safe)
    q = db.execute(
        text("SELECT id FROM quotations WHERE id=:qid AND tenant_id=:tenant_id"),
        {"qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not q:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    # 2) Validate panel belongs to quotation + tenant
    p = db.execute(
        text("""
            SELECT id FROM quote_panels
            WHERE id=:pid AND quotation_id=:qid AND tenant_id=:tenant_id
        """),
        {"pid": panel_id, "qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not p:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_RESOURCE,
            detail="Panel not found for quotation/tenant",
        )

    # 3) Upsert into QCA only
    svc = CostAdderService(db, tenant_id=tenant_id)
    row = svc.upsert_cost_adder(
        quotation_id=quotation_id,
        panel_id=panel_id,
        cost_head_code=body.cost_head_code,
        amount=body.amount,
        currency=body.currency,
        notes=body.notes,
    )

    db.commit()
    return row


@router.get("/{quotation_id}/cost-summary", response_model=QuotationCostSummaryResponse)
async def get_cost_summary(
    quotation_id: int = Path(..., description="Quotation ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Week-3 Day-2: Read-only QCA cost summary per quotation/panel.
    Rules:
    - Summary only (no breakup)
    - QCA only (no QCD access)
    - No pricing recompute
    """
    # Validate quotation exists (tenant-safe)
    q = db.execute(
        text("SELECT id FROM quotations WHERE id=:qid AND tenant_id=:tenant_id"),
        {"qid": quotation_id, "tenant_id": tenant_id},
    ).first()
    if not q:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    svc = CostSummaryService(db, tenant_id=tenant_id)
    return svc.get_cost_summary(quotation_id=quotation_id)


@router.get("/{quotation_id}", response_model=QuotationDetail)
async def get_quotation(
    quotation_id: int = Path(..., description="Quotation ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Get quotation by ID (Week-1 Day-1).

    Returns tenant-safe quotation detail or 404 if not found.
    """
    row = (
        db.execute(
            text("""
            SELECT
                id,
                quote_no,
                customer_name,
                status,
                customer_id,
                project_id,
                discount_pct,
                tax_profile_id,
                tax_mode,
                created_at,
                updated_at
            FROM quotations
            WHERE id = :qid AND tenant_id = :tenant_id
        """),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not row:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    # Convert to dict, handling datetime conversion
    result = dict(row)
    if result.get("created_at") and hasattr(result["created_at"], "isoformat"):
        result["created_at"] = result["created_at"].isoformat()
    if result.get("updated_at") and hasattr(result["updated_at"], "isoformat"):
        result["updated_at"] = result["updated_at"].isoformat()

    return result


@router.post("/{quotation_id}/revisions")
async def create_revision(quotation_id: int):
    """Create quotation revision (to be implemented)"""
    return {
        "message": f"Create revision for quotation {quotation_id} endpoint - to be implemented"
    }


@router.put(
    "/{quotation_id}/discount/quotation", response_model=QuotationDiscountSetResponse
)
async def set_quotation_discount(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    body: QuotationDiscountSetRequest = ...,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Set quotation-level discount percentage (Operator+ allowed).
    This is the quotation-wide discount applied AFTER line discounts and BEFORE tax.
    """
    user_id = get_user_id_from_request(request)
    user_roles = get_user_roles_from_request(request)

    try:
        assert_bulk_allowed(user_roles)  # Operator, Reviewer, Approver
    except DiscountPermissionError as e:
        raise_api_error(
            status_code=403,
            error_code=ErrorCodes.PERMISSION_INSUFFICIENT_ROLE,
            detail=str(e),
        )

    # verify quotation exists + tenant-safe
    q = (
        db.execute(
            text(
                "SELECT id, discount_pct FROM quotations WHERE id=:qid AND tenant_id=:tenant_id"
            ),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )
    if not q:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    old_pct = q.get("discount_pct")

    # update quotation discount
    res = db.execute(
        text("""
            UPDATE quotations
            SET discount_pct=:pct, updated_at=CURRENT_TIMESTAMP
            WHERE id=:qid AND tenant_id=:tenant_id
        """),
        {"pct": body.discount_pct, "qid": quotation_id, "tenant_id": tenant_id},
    )

    if res.rowcount != 1:
        raise_api_error(
            status_code=409,
            error_code=ErrorCodes.CONFLICT_UPDATE_FAILED,
            detail="Quotation discount update failed (rowcount mismatch)",
        )

    # audit
    AuditLogger.log_event(
        db=db,
        tenant_id=tenant_id,
        actor_id=user_id,
        action_type="QUOTATION_DISCOUNT_SET",
        resource_type="quotation",
        resource_id=quotation_id,
        old_values={"discount_pct": str(old_pct)} if old_pct is not None else None,
        new_values={
            "discount_pct": str(body.discount_pct),
            "reason": body.reason,
            "actor_roles": user_roles,
        },
        metadata={"quotation_id": quotation_id},
    )

    db.commit()

    return QuotationDiscountSetResponse(
        quotation_id=quotation_id,
        discount_pct=body.discount_pct,
        message="Quotation discount set successfully",
    )


@router.post("/{quotation_id}/pricing/preview")
async def pricing_preview(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Preview pricing calculation for a quotation (Policy-1: preview only, no DB overwrite).

    Computes:
    - Line-level discounts (rule-based precedence)
    - Subtotal
    - Quotation-level discount
    - GST split (CGST/SGST/IGST)
    - Grand total

    Returns preview response with totals, GST breakdown, and flags.
    """
    # Use shared computation helper (single source of truth)
    result = _compute_quote_pricing(
        db=db,
        tenant_id=tenant_id,
        quotation_id=quotation_id,
    )

    return {
        "quotation_id": quotation_id,
        **result,
    }


@router.post("/{quotation_id}/pricing/apply-recalc", response_model=ApplyRecalcResponse)
async def apply_recalc(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    body: ApplyRecalcRequest = ...,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Apply pricing recalculation to a quotation (Policy-1: explicit action, Reviewer/Approver only).

    Computes pricing using the same logic as preview, then persists snapshots to quotations table.
    Requires decision_id and reason for audit trail.

    Only Reviewer and Approver roles are allowed.
    """
    user_id = get_user_id_from_request(request)
    user_roles = get_user_roles_from_request(request)

    # Permission gate (Policy-1)
    try:
        assert_apply_recalc_allowed(user_roles)
    except ApplyRecalcPermissionError as e:
        raise_api_error(
            status_code=403,
            error_code=ErrorCodes.PERMISSION_INSUFFICIENT_ROLE,
            detail=str(e),
        )

    # Ensure quotation exists + belongs to tenant (also get tax profile info for audit)
    qrow = (
        db.execute(
            text("""
            SELECT id, tax_profile_id, tax_mode
            FROM quotations
            WHERE id = :qid AND tenant_id = :tenant_id
        """),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not qrow:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Quotation not found for tenant",
        )

    # Capture tax profile info for audit
    tax_profile_id_at_compute = qrow.get("tax_profile_id")
    tax_mode_at_compute = qrow.get("tax_mode")

    # Read old stored totals (for audit)
    old = (
        db.execute(
            text("""
            SELECT
                taxable_base,
                cgst_pct_snapshot,
                sgst_pct_snapshot,
                igst_pct_snapshot,
                cgst_amount,
                sgst_amount,
                igst_amount,
                tax_amount_total,
                grand_total
            FROM quotations
            WHERE id = :qid AND tenant_id = :tenant_id
        """),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    old_values = dict(old) if old else None

    # Compute pricing using the same logic as preview (single source of truth)
    preview = _compute_quote_pricing(
        db=db,
        tenant_id=tenant_id,
        quotation_id=quotation_id,
    )

    discounted_subtotal = Decimal(str(preview["discounted_subtotal"]))
    gst = preview.get("gst") or {}
    grand_total = Decimal(str(preview["grand_total"]))

    # Prepare snapshot fields
    taxable_base = discounted_subtotal

    if gst:
        # Convert to Decimal for proper SQL binding (snapshot pct values)
        cgst_pct = Decimal(str(gst.get("cgst_pct"))) if gst.get("cgst_pct") else None
        sgst_pct = Decimal(str(gst.get("sgst_pct"))) if gst.get("sgst_pct") else None
        igst_pct = Decimal(str(gst.get("igst_pct"))) if gst.get("igst_pct") else None
        # Convert to Decimal and quantize to 4dp for proper SQL binding
        cgst_amt = qrate(Decimal(str(gst.get("cgst_amount"))))
        sgst_amt = qrate(Decimal(str(gst.get("sgst_amount"))))
        igst_amt = qrate(Decimal(str(gst.get("igst_amount"))))
        tax_total = qrate(Decimal(str(gst.get("tax_total"))))
    else:
        cgst_pct = sgst_pct = igst_pct = None
        # Quantize zeros to 4dp for consistency with qrate() usage elsewhere
        zero_amt = qrate(Decimal("0"))
        cgst_amt = sgst_amt = igst_amt = zero_amt
        tax_total = zero_amt

    # Persist snapshots (explicit action)
    update_result = db.execute(
        text("""
            UPDATE quotations
            SET
                taxable_base = :taxable_base,
                cgst_pct_snapshot = :cgst_pct,
                sgst_pct_snapshot = :sgst_pct,
                igst_pct_snapshot = :igst_pct,
                cgst_amount = :cgst_amount,
                sgst_amount = :sgst_amount,
                igst_amount = :igst_amount,
                tax_amount_total = :tax_total,
                grand_total = :grand_total,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :qid AND tenant_id = :tenant_id
        """),
        {
            "taxable_base": taxable_base,
            "cgst_pct": cgst_pct,
            "sgst_pct": sgst_pct,
            "igst_pct": igst_pct,
            "cgst_amount": cgst_amt,
            "sgst_amount": sgst_amt,
            "igst_amount": igst_amt,
            "tax_total": tax_total,
            "grand_total": grand_total,
            "qid": quotation_id,
            "tenant_id": tenant_id,
        },
    )

    # Verify UPDATE actually affected 1 row (prevents silent no-op)
    if update_result.rowcount != 1:
        raise_api_error(
            status_code=409,
            error_code=ErrorCodes.CONFLICT_APPLY_RECALC_FAILED,
            detail="Apply-Recalc failed: quotation not updated (rowcount mismatch)",
        )

    # Audit
    AuditLogger.log_event(
        db=db,
        tenant_id=tenant_id,
        actor_id=user_id,
        action_type="APPLY_RECALC",
        resource_type="quotation",
        resource_id=quotation_id,
        old_values=old_values,
        new_values={
            "decision_id": body.decision_id,
            "reason": body.reason,
            "taxable_base": str(taxable_base),
            "gst": gst,
            "grand_total": str(grand_total),
            "tax_profile_id": tax_profile_id_at_compute,
            "tax_mode": tax_mode_at_compute,
            "actor_roles": user_roles,
        },
        metadata={"quotation_id": quotation_id},
    )

    db.commit()

    return ApplyRecalcResponse(
        quotation_id=quotation_id,
        decision_id=body.decision_id,
        message="Apply-Recalc completed and totals snapshot saved",
        totals={
            "subtotal": preview["subtotal"],
            "quotation_discount_pct": preview["quotation_discount_pct"],
            "discounted_subtotal": preview["discounted_subtotal"],
            "grand_total": preview["grand_total"],
        },
        gst=gst,
    )


@router.post("/{quotation_id}/copy", response_model=CopyQuotationResponse)
async def copy_quotation(
    request: Request,
    quotation_id: int = Path(..., description="Source quotation ID"),
    body: CopyQuotationRequest = ...,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Copy a quotation (deep copy - copy-never-link).

    Creates a new quotation with new IDs for all panels, BOMs, and BOM items.
    Tracking fields in quote_boms are set:
    - origin_master_bom_id: preserved if source had it, otherwise NULL
    - instance_sequence_no: set to 1 for new copies
    - is_modified: set to false for new copies
    """
    user_id = get_user_id_from_request(request)

    # Verify source quotation exists and belongs to tenant
    source_quote = (
        db.execute(
            text("""
            SELECT id, quote_no, customer_name, customer_id, project_id, status, 
                   discount_pct, tax_profile_id, tax_mode
            FROM quotations
            WHERE id = :qid AND tenant_id = :tenant_id
        """),
            {"qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not source_quote:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Source quotation not found for tenant",
        )

    # Generate new quote number
    if body.new_quote_no == "AUTO" or not body.new_quote_no:
        new_quote_no = f"{source_quote['quote_no']}-COPY"
        # Ensure uniqueness by adding suffix if needed
        counter = 1
        while True:
            check = db.execute(
                text(
                    "SELECT id FROM quotations WHERE tenant_id=:tid AND quote_no=:qno"
                ),
                {"tid": tenant_id, "qno": new_quote_no},
            ).first()
            if not check:
                break
            new_quote_no = f"{source_quote['quote_no']}-COPY-{counter}"
            counter += 1
    else:
        new_quote_no = body.new_quote_no

    # Create new quotation (copy-never-link: new ID)
    new_quote_result = db.execute(
        text("""
            INSERT INTO quotations (
                tenant_id, quote_no, customer_name, customer_id, project_id, status,
                discount_pct, tax_profile_id, tax_mode, created_by
            )
            VALUES (
                :tenant_id, :quote_no, :customer_name, :customer_id, :project_id, 'DRAFT',
                :discount_pct, :tax_profile_id, :tax_mode, :created_by
            )
            RETURNING id
        """),
        {
            "tenant_id": tenant_id,
            "quote_no": new_quote_no,
            "customer_name": source_quote["customer_name"],
            "customer_id": source_quote.get("customer_id"),
            "project_id": source_quote.get("project_id"),
            "discount_pct": source_quote.get("discount_pct") or 0,
            "tax_profile_id": source_quote.get("tax_profile_id"),
            "tax_mode": source_quote.get("tax_mode"),
            "created_by": user_id,
        },
    )
    new_quotation_id = new_quote_result.scalar_one()

    # Copy panels if requested
    panel_id_map = {}  # old_panel_id -> new_panel_id
    if body.copy_panels:
        source_panels = (
            db.execute(
                text("""
                SELECT id, name, quantity, rate, amount
                FROM quote_panels
                WHERE quotation_id = :qid AND tenant_id = :tenant_id
                ORDER BY id
            """),
                {"qid": quotation_id, "tenant_id": tenant_id},
            )
            .mappings()
            .all()
        )

        for panel in source_panels:
            new_panel_result = db.execute(
                text("""
                    INSERT INTO quote_panels (tenant_id, quotation_id, name, quantity, rate, amount)
                    VALUES (:tenant_id, :quotation_id, :name, :quantity, :rate, :amount)
                    RETURNING id
                """),
                {
                    "tenant_id": tenant_id,
                    "quotation_id": new_quotation_id,
                    "name": panel["name"],
                    "quantity": panel["quantity"],
                    "rate": panel.get("rate"),
                    "amount": panel.get("amount"),
                },
            )
            new_panel_id = new_panel_result.scalar_one()
            panel_id_map[panel["id"]] = new_panel_id

    # Copy BOMs if requested (preserve hierarchy)
    bom_id_map = {}  # old_bom_id -> new_bom_id
    if body.copy_boms and body.copy_panels:
        # First pass: copy all BOMs (level 0 first, then children)
        source_boms = (
            db.execute(
                text("""
                SELECT id, panel_id, parent_bom_id, level, name, quantity, rate, amount,
                       origin_master_bom_id, instance_sequence_no, is_modified
                FROM quote_boms
                WHERE quotation_id = :qid AND tenant_id = :tenant_id
                ORDER BY level, id
            """),
                {"qid": quotation_id, "tenant_id": tenant_id},
            )
            .mappings()
            .all()
        )

        for bom in source_boms:
            old_panel_id = bom["panel_id"]
            new_panel_id = panel_id_map.get(old_panel_id)
            if not new_panel_id:
                continue  # Skip if panel wasn't copied

            old_parent_bom_id = bom.get("parent_bom_id")
            new_parent_bom_id = (
                bom_id_map.get(old_parent_bom_id) if old_parent_bom_id else None
            )

            # Tracking fields: preserve origin_master_bom_id, set instance_sequence_no=1, is_modified=false
            new_bom_result = db.execute(
                text("""
                    INSERT INTO quote_boms (
                        tenant_id, quotation_id, panel_id, parent_bom_id, level, name, quantity, rate, amount,
                        origin_master_bom_id, instance_sequence_no, is_modified
                    )
                    VALUES (
                        :tenant_id, :quotation_id, :panel_id, :parent_bom_id, :level, :name, :quantity, :rate, :amount,
                        :origin_master_bom_id, 1, false
                    )
                    RETURNING id
                """),
                {
                    "tenant_id": tenant_id,
                    "quotation_id": new_quotation_id,
                    "panel_id": new_panel_id,
                    "parent_bom_id": new_parent_bom_id,
                    "level": bom["level"],
                    "name": bom["name"],
                    "quantity": bom["quantity"],
                    "rate": bom.get("rate"),
                    "amount": bom.get("amount"),
                    "origin_master_bom_id": bom.get(
                        "origin_master_bom_id"
                    ),  # Preserve if exists
                },
            )
            new_bom_id = new_bom_result.scalar_one()
            bom_id_map[bom["id"]] = new_bom_id

    # Copy BOM items if requested
    if body.copy_bom_items and body.copy_boms:
        source_items = (
            db.execute(
                text("""
                SELECT id, panel_id, bom_id, parent_line_id, product_id, make_id, series_id, category_id,
                       quantity, rate, discount_pct, discount_source, net_rate, amount, rate_source,
                       is_price_missing, is_client_supplied, is_locked, cost_head_id, resolution_status,
                       description, metadata_json, sequence_order, override_rate, override_reason
                FROM quote_bom_items
                WHERE quotation_id = :qid AND tenant_id = :tenant_id
                ORDER BY id
            """),
                {"qid": quotation_id, "tenant_id": tenant_id},
            )
            .mappings()
            .all()
        )

        item_id_map = {}  # old_item_id -> new_item_id

        for item in source_items:
            old_panel_id = item["panel_id"]
            new_panel_id = panel_id_map.get(old_panel_id)
            if not new_panel_id:
                continue

            old_bom_id = item.get("bom_id")
            new_bom_id = bom_id_map.get(old_bom_id) if old_bom_id else None

            old_parent_line_id = item.get("parent_line_id")
            new_parent_line_id = (
                item_id_map.get(old_parent_line_id) if old_parent_line_id else None
            )

            item_result = db.execute(
                text("""
                    INSERT INTO quote_bom_items (
                        tenant_id, quotation_id, panel_id, bom_id, parent_line_id, product_id, make_id, series_id, category_id,
                        quantity, rate, discount_pct, discount_source, net_rate, amount, rate_source,
                        is_price_missing, is_client_supplied, is_locked, cost_head_id, resolution_status,
                        description, metadata_json, sequence_order, override_rate, override_reason
                    )
                    VALUES (
                        :tenant_id, :quotation_id, :panel_id, :bom_id, :parent_line_id, :product_id, :make_id, :series_id, :category_id,
                        :quantity, :rate, :discount_pct, :discount_source, :net_rate, :amount, :rate_source,
                        :is_price_missing, :is_client_supplied, :is_locked, :cost_head_id, :resolution_status,
                        :description, :metadata_json, :sequence_order, :override_rate, :override_reason
                    )
                    RETURNING id
                """),
                {
                    "tenant_id": tenant_id,
                    "quotation_id": new_quotation_id,
                    "panel_id": new_panel_id,
                    "bom_id": new_bom_id,
                    "parent_line_id": new_parent_line_id,
                    "product_id": item.get("product_id"),
                    "make_id": item.get("make_id"),
                    "series_id": item.get("series_id"),
                    "category_id": item.get("category_id"),
                    "quantity": item["quantity"],
                    "rate": item.get("rate"),
                    "discount_pct": item.get("discount_pct"),
                    "discount_source": item.get("discount_source"),
                    "net_rate": item.get("net_rate"),
                    "amount": item.get("amount"),
                    "rate_source": item.get("rate_source"),
                    "is_price_missing": item.get("is_price_missing") or False,
                    "is_client_supplied": item.get("is_client_supplied") or False,
                    "is_locked": item.get("is_locked") or False,
                    "cost_head_id": item.get("cost_head_id"),
                    "resolution_status": item.get("resolution_status"),
                    "description": item.get("description"),
                    "metadata_json": item.get("metadata_json"),
                    "sequence_order": item.get("sequence_order") or 0,
                    "override_rate": item.get("override_rate"),
                    "override_reason": item.get("override_reason"),
                },
            )
            new_item_id = item_result.scalar_one()
            item_id_map[item["id"]] = new_item_id

    db.commit()

    return CopyQuotationResponse(new_quotation_id=new_quotation_id)


@router.post("/{quotation_id}/panels/{panel_id}/copy", response_model=CopyPanelResponse)
async def copy_panel(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    panel_id: int = Path(..., description="Source panel ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Copy a panel within the same quotation (deep copy).

    Creates a new panel with new ID, and copies all associated BOMs and BOM items.
    """
    # Verify source panel exists
    source_panel = (
        db.execute(
            text("""
            SELECT id, name, quantity, rate, amount
            FROM quote_panels
            WHERE id = :panel_id AND quotation_id = :qid AND tenant_id = :tenant_id
        """),
            {"panel_id": panel_id, "qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not source_panel:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Source panel not found",
        )

    # Create new panel
    new_panel_result = db.execute(
        text("""
            INSERT INTO quote_panels (tenant_id, quotation_id, name, quantity, rate, amount)
            VALUES (:tenant_id, :quotation_id, :name, :quantity, :rate, :amount)
            RETURNING id
        """),
        {
            "tenant_id": tenant_id,
            "quotation_id": quotation_id,
            "name": source_panel["name"],
            "quantity": source_panel["quantity"],
            "rate": source_panel.get("rate"),
            "amount": source_panel.get("amount"),
        },
    )
    new_panel_id = new_panel_result.scalar_one()

    # Copy BOMs (preserve hierarchy)
    bom_id_map = {}
    source_boms = (
        db.execute(
            text("""
            SELECT id, parent_bom_id, level, name, quantity, rate, amount,
                   origin_master_bom_id, instance_sequence_no, is_modified
            FROM quote_boms
            WHERE panel_id = :panel_id AND quotation_id = :qid AND tenant_id = :tenant_id
            ORDER BY level, id
        """),
            {"panel_id": panel_id, "qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .all()
    )

    for bom in source_boms:
        old_parent_bom_id = bom.get("parent_bom_id")
        new_parent_bom_id = (
            bom_id_map.get(old_parent_bom_id) if old_parent_bom_id else None
        )

        new_bom_result = db.execute(
            text("""
                INSERT INTO quote_boms (
                    tenant_id, quotation_id, panel_id, parent_bom_id, level, name, quantity, rate, amount,
                    origin_master_bom_id, instance_sequence_no, is_modified
                )
                VALUES (
                    :tenant_id, :quotation_id, :panel_id, :parent_bom_id, :level, :name, :quantity, :rate, :amount,
                    :origin_master_bom_id, 1, false
                )
                RETURNING id
            """),
            {
                "tenant_id": tenant_id,
                "quotation_id": quotation_id,
                "panel_id": new_panel_id,
                "parent_bom_id": new_parent_bom_id,
                "level": bom["level"],
                "name": bom["name"],
                "quantity": bom["quantity"],
                "rate": bom.get("rate"),
                "amount": bom.get("amount"),
                "origin_master_bom_id": bom.get("origin_master_bom_id"),
            },
        )
        new_bom_id = new_bom_result.scalar_one()
        bom_id_map[bom["id"]] = new_bom_id

    # Copy BOM items
    source_items = (
        db.execute(
            text("""
            SELECT id, bom_id, parent_line_id, product_id, make_id, series_id, category_id,
                   quantity, rate, discount_pct, discount_source, net_rate, amount, rate_source,
                   is_price_missing, is_client_supplied, is_locked, cost_head_id, resolution_status,
                   description, metadata_json, sequence_order, override_rate, override_reason
            FROM quote_bom_items
            WHERE panel_id = :panel_id AND quotation_id = :qid AND tenant_id = :tenant_id
            ORDER BY id
        """),
            {"panel_id": panel_id, "qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .all()
    )

    item_id_map = {}
    for item in source_items:
        old_bom_id = item.get("bom_id")
        new_bom_id = bom_id_map.get(old_bom_id) if old_bom_id else None

        old_parent_line_id = item.get("parent_line_id")
        new_parent_line_id = (
            item_id_map.get(old_parent_line_id) if old_parent_line_id else None
        )

        item_result = db.execute(
            text("""
                INSERT INTO quote_bom_items (
                    tenant_id, quotation_id, panel_id, bom_id, parent_line_id, product_id, make_id, series_id, category_id,
                    quantity, rate, discount_pct, discount_source, net_rate, amount, rate_source,
                    is_price_missing, is_client_supplied, is_locked, cost_head_id, resolution_status,
                    description, metadata_json, sequence_order, override_rate, override_reason
                )
                VALUES (
                    :tenant_id, :quotation_id, :panel_id, :bom_id, :parent_line_id, :product_id, :make_id, :series_id, :category_id,
                    :quantity, :rate, :discount_pct, :discount_source, :net_rate, :amount, :rate_source,
                    :is_price_missing, :is_client_supplied, :is_locked, :cost_head_id, :resolution_status,
                    :description, :metadata_json, :sequence_order, :override_rate, :override_reason
                )
                RETURNING id
            """),
            {
                "tenant_id": tenant_id,
                "quotation_id": quotation_id,
                "panel_id": new_panel_id,
                "bom_id": new_bom_id,
                "parent_line_id": new_parent_line_id,
                "product_id": item.get("product_id"),
                "make_id": item.get("make_id"),
                "series_id": item.get("series_id"),
                "category_id": item.get("category_id"),
                "quantity": item["quantity"],
                "rate": item.get("rate"),
                "discount_pct": item.get("discount_pct"),
                "discount_source": item.get("discount_source"),
                "net_rate": item.get("net_rate"),
                "amount": item.get("amount"),
                "rate_source": item.get("rate_source"),
                "is_price_missing": item.get("is_price_missing") or False,
                "is_client_supplied": item.get("is_client_supplied") or False,
                "is_locked": item.get("is_locked") or False,
                "cost_head_id": item.get("cost_head_id"),
                "resolution_status": item.get("resolution_status"),
                "description": item.get("description"),
                "metadata_json": item.get("metadata_json"),
                "sequence_order": item.get("sequence_order") or 0,
                "override_rate": item.get("override_rate"),
                "override_reason": item.get("override_reason"),
            },
        )
        new_item_id = item_result.scalar_one()
        item_id_map[item["id"]] = new_item_id

    db.commit()

    return CopyPanelResponse(new_panel_id=new_panel_id)


@router.post("/{quotation_id}/boms/{bom_id}/copy", response_model=CopyBOMResponse)
async def copy_bom(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    bom_id: int = Path(..., description="Source BOM ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Copy a BOM subtree (deep copy).

    Copies the BOM and all its children (recursive), plus all BOM items.
    Tracking fields are set: instance_sequence_no=1, is_modified=false.
    """
    # Verify source BOM exists
    source_bom = (
        db.execute(
            text("""
            SELECT id, panel_id, parent_bom_id, level, name, quantity, rate, amount,
                   origin_master_bom_id, instance_sequence_no, is_modified
            FROM quote_boms
            WHERE id = :bom_id AND quotation_id = :qid AND tenant_id = :tenant_id
        """),
            {"bom_id": bom_id, "qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not source_bom:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Source BOM not found",
        )

    panel_id = source_bom["panel_id"]
    old_parent_bom_id = source_bom.get("parent_bom_id")

    # Copy the BOM itself
    new_bom_result = db.execute(
        text("""
            INSERT INTO quote_boms (
                tenant_id, quotation_id, panel_id, parent_bom_id, level, name, quantity, rate, amount,
                origin_master_bom_id, instance_sequence_no, is_modified
            )
            VALUES (
                :tenant_id, :quotation_id, :panel_id, :parent_bom_id, :level, :name, :quantity, :rate, :amount,
                :origin_master_bom_id, 1, false
            )
            RETURNING id
        """),
        {
            "tenant_id": tenant_id,
            "quotation_id": quotation_id,
            "panel_id": panel_id,
            "parent_bom_id": old_parent_bom_id,  # Keep same parent
            "level": source_bom["level"],
            "name": source_bom["name"],
            "quantity": source_bom["quantity"],
            "rate": source_bom.get("rate"),
            "amount": source_bom.get("amount"),
            "origin_master_bom_id": source_bom.get("origin_master_bom_id"),
        },
    )
    new_bom_id = new_bom_result.scalar_one()

    # Recursively copy child BOMs
    bom_id_map = {bom_id: new_bom_id}

    def copy_bom_tree(old_parent_id: int, new_parent_id: int):
        """Recursively copy BOM subtree"""
        children = (
            db.execute(
                text("""
                SELECT id, level, name, quantity, rate, amount, origin_master_bom_id
                FROM quote_boms
                WHERE parent_bom_id = :parent_id AND quotation_id = :qid AND tenant_id = :tenant_id
            """),
                {
                    "parent_id": old_parent_id,
                    "qid": quotation_id,
                    "tenant_id": tenant_id,
                },
            )
            .mappings()
            .all()
        )

        for child in children:
            new_child_result = db.execute(
                text("""
                    INSERT INTO quote_boms (
                        tenant_id, quotation_id, panel_id, parent_bom_id, level, name, quantity, rate, amount,
                        origin_master_bom_id, instance_sequence_no, is_modified
                    )
                    VALUES (
                        :tenant_id, :quotation_id, :panel_id, :parent_bom_id, :level, :name, :quantity, :rate, :amount,
                        :origin_master_bom_id, 1, false
                    )
                    RETURNING id
                """),
                {
                    "tenant_id": tenant_id,
                    "quotation_id": quotation_id,
                    "panel_id": panel_id,
                    "parent_bom_id": new_parent_id,
                    "level": child["level"],
                    "name": child["name"],
                    "quantity": child["quantity"],
                    "rate": child.get("rate"),
                    "amount": child.get("amount"),
                    "origin_master_bom_id": child.get("origin_master_bom_id"),
                },
            )
            new_child_id = new_child_result.scalar_one()
            bom_id_map[child["id"]] = new_child_id
            copy_bom_tree(child["id"], new_child_id)  # Recursive

    copy_bom_tree(bom_id, new_bom_id)

    # Copy BOM items for all copied BOMs
    for old_bom_id, new_bom_id_mapped in bom_id_map.items():
        source_items = (
            db.execute(
                text("""
                SELECT id, parent_line_id, product_id, make_id, series_id, category_id,
                       quantity, rate, discount_pct, discount_source, net_rate, amount, rate_source,
                       is_price_missing, is_client_supplied, is_locked, cost_head_id, resolution_status,
                       description, metadata_json, sequence_order, override_rate, override_reason
                FROM quote_bom_items
                WHERE bom_id = :bom_id AND quotation_id = :qid AND tenant_id = :tenant_id
                ORDER BY id
            """),
                {"bom_id": old_bom_id, "qid": quotation_id, "tenant_id": tenant_id},
            )
            .mappings()
            .all()
        )

        item_id_map = {}
        for item in source_items:
            old_parent_line_id = item.get("parent_line_id")
            new_parent_line_id = (
                item_id_map.get(old_parent_line_id) if old_parent_line_id else None
            )

            db.execute(
                text("""
                    INSERT INTO quote_bom_items (
                        tenant_id, quotation_id, panel_id, bom_id, parent_line_id, product_id, make_id, series_id, category_id,
                        quantity, rate, discount_pct, discount_source, net_rate, amount, rate_source,
                        is_price_missing, is_client_supplied, is_locked, cost_head_id, resolution_status,
                        description, metadata_json, sequence_order, override_rate, override_reason
                    )
                    VALUES (
                        :tenant_id, :quotation_id, :panel_id, :bom_id, :parent_line_id, :product_id, :make_id, :series_id, :category_id,
                        :quantity, :rate, :discount_pct, :discount_source, :net_rate, :amount, :rate_source,
                        :is_price_missing, :is_client_supplied, :is_locked, :cost_head_id, :resolution_status,
                        :description, :metadata_json, :sequence_order, :override_rate, :override_reason
                    )
                """),
                {
                    "tenant_id": tenant_id,
                    "quotation_id": quotation_id,
                    "panel_id": panel_id,
                    "bom_id": new_bom_id_mapped,
                    "parent_line_id": new_parent_line_id,
                    "product_id": item.get("product_id"),
                    "make_id": item.get("make_id"),
                    "series_id": item.get("series_id"),
                    "category_id": item.get("category_id"),
                    "quantity": item["quantity"],
                    "rate": item.get("rate"),
                    "discount_pct": item.get("discount_pct"),
                    "discount_source": item.get("discount_source"),
                    "net_rate": item.get("net_rate"),
                    "amount": item.get("amount"),
                    "rate_source": item.get("rate_source"),
                    "is_price_missing": item.get("is_price_missing") or False,
                    "is_client_supplied": item.get("is_client_supplied") or False,
                    "is_locked": item.get("is_locked") or False,
                    "cost_head_id": item.get("cost_head_id"),
                    "resolution_status": item.get("resolution_status"),
                    "description": item.get("description"),
                    "metadata_json": item.get("metadata_json"),
                    "sequence_order": item.get("sequence_order") or 0,
                    "override_rate": item.get("override_rate"),
                    "override_reason": item.get("override_reason"),
                },
            )

    db.commit()

    return CopyBOMResponse(new_bom_id=new_bom_id)


@router.post("/{quotation_id}/feeders/{bom_id}/copy", response_model=CopyBOMResponse)
async def copy_feeder(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    bom_id: int = Path(..., description="Source feeder (level 0 BOM) ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Copy a feeder (level 0 BOM) - alias for copy_bom with level validation.

    A feeder is a BOM with level=0. This endpoint validates the level and then calls copy_bom logic.
    """
    # Verify it's a level 0 BOM
    source_bom = (
        db.execute(
            text("""
            SELECT id, level
            FROM quote_boms
            WHERE id = :bom_id AND quotation_id = :qid AND tenant_id = :tenant_id
        """),
            {"bom_id": bom_id, "qid": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not source_bom:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_QUOTATION,
            detail="Source feeder not found",
        )

    if source_bom["level"] != 0:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_ERROR,
            detail="BOM is not a feeder (level must be 0)",
        )

    # Delegate to copy_bom
    return await copy_bom(request, quotation_id, bom_id, db, tenant_id)


@router.delete("/{quotation_id}/bom/item/{line_id}")
async def delete_quote_bom_item(
    request: Request,
    quotation_id: int = Path(..., description="Quotation ID"),
    line_id: int = Path(..., description="Line item ID"),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id_from_request),
):
    """
    Delete a quote BOM line item.

    A5.2 IsLocked enforcement: Deletion is blocked if is_locked = true.
    Returns 409 LINE_ITEM_LOCKED if item is locked.

    Allowed roles: Operator, Reviewer, Approver
    """
    user_id = get_user_id_from_request(request)
    user_roles = get_user_roles_from_request(request)

    # Role enforcement: Operator, Reviewer, Approver allowed
    try:
        assert_bulk_allowed(user_roles)
    except DiscountPermissionError as e:
        raise_api_error(
            status_code=403,
            error_code=ErrorCodes.PERMISSION_INSUFFICIENT_ROLE,
            detail=str(e),
        )

    # Verify line item exists and belongs to quotation + tenant (tenant-filtered SELECT)
    line = (
        db.execute(
            text("""
            SELECT 
                id, 
                quotation_id, 
                is_locked
            FROM quote_bom_items
            WHERE id = :line_id 
                AND quotation_id = :quotation_id 
                AND tenant_id = :tenant_id
        """),
            {"line_id": line_id, "quotation_id": quotation_id, "tenant_id": tenant_id},
        )
        .mappings()
        .first()
    )

    if not line:
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_LINE_ITEM,
            detail="Line item not found",
        )

    # A5.2: IsLocked enforcement - block deletion if locked
    if line.get("is_locked"):
        raise_api_error(
            status_code=409,
            error_code=ErrorCodes.CONFLICT_LINE_ITEM_LOCKED,
            detail="LINE_ITEM_LOCKED",
        )

    # Read old values for audit
    old_values = dict(line)

    # Delete the line item
    delete_result = db.execute(
        text("""
            DELETE FROM quote_bom_items
            WHERE id = :line_id 
                AND quotation_id = :quotation_id
                AND tenant_id = :tenant_id
                AND is_locked = false
        """),
        {"line_id": line_id, "quotation_id": quotation_id, "tenant_id": tenant_id},
    )

    # Verify deletion succeeded (race condition protection)
    if delete_result.rowcount != 1:
        # Could be locked between check and delete, or already deleted
        # Re-check is_locked with tenant-safe query to give more specific error
        recheck = (
            db.execute(
                text("""
                SELECT is_locked
                FROM quote_bom_items
                WHERE id = :line_id
                  AND quotation_id = :quotation_id
                  AND tenant_id = :tenant_id
            """),
                {
                    "line_id": line_id,
                    "quotation_id": quotation_id,
                    "tenant_id": tenant_id,
                },
            )
            .mappings()
            .first()
        )

        if recheck and recheck.get("is_locked"):
            raise_api_error(
                status_code=409,
                error_code=ErrorCodes.CONFLICT_LINE_ITEM_LOCKED,
                detail="LINE_ITEM_LOCKED",
            )
        raise_api_error(
            status_code=404,
            error_code=ErrorCodes.NOT_FOUND_LINE_ITEM,
            detail="Line item not found or already deleted",
        )

    # Audit
    AuditLogger.log_event(
        db=db,
        tenant_id=tenant_id,
        actor_id=user_id,
        action_type="LINE_ITEM_DELETED",
        resource_type="quote_bom_item",
        resource_id=line_id,
        old_values=old_values,
        new_values=None,
        metadata={"quotation_id": quotation_id, "actor_roles": user_roles},
    )

    db.commit()

    return {
        "message": "Line item deleted successfully",
        "line_id": line_id,
        "quotation_id": quotation_id,
    }
