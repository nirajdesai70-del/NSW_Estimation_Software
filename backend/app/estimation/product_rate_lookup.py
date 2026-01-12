"""
Product Rate Lookup
Phase-5: Product-based rate lookup (current schema uses prices.product_id)
"""
from __future__ import annotations
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.estimation.decimal_norm import qrate


class ProductRateLookup:
    """
    Phase-5: Product-based rate lookup (current schema uses prices.product_id).
    Returns latest ACTIVE rate with effective_date <= today.
    """

    def __init__(self, db: Session, *, tenant_id: int):
        """
        Initialize product rate lookup.

        Args:
            db: Database session
            tenant_id: Tenant ID (required for tenant-safe queries)
        """
        self.db = db
        self.tenant_id = tenant_id

    def get_rate_for_product(self, *, product_id: int, quote_id: int) -> Decimal:
        """
        Return the effective product rate for this quote context.

        Queries the prices table for the latest ACTIVE rate with effective_date <= today.

        Args:
            product_id: products.id (current L2 commercial identity reference)
            quote_id: quotation identifier (context - kept for future tiering logic)

        Returns:
            Decimal rate (quantized to 4 decimal places)

        Raises:
            ValueError: If no ACTIVE price found for the product
        """
        row = self.db.execute(
            text("""
                SELECT rate
                FROM prices
                WHERE tenant_id = :tenant_id
                  AND product_id = :product_id
                  AND effective_date <= CURRENT_DATE
                  AND status = 'ACTIVE'
                ORDER BY effective_date DESC
                LIMIT 1
            """),
            {"tenant_id": self.tenant_id, "product_id": product_id},
        ).mappings().first()

        if not row or row.get("rate") is None:
            raise ValueError(f"No ACTIVE price found for product_id={product_id}")

        return qrate(Decimal(str(row["rate"])))

