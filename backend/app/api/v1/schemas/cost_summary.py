"""
Cost Summary Schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict
from decimal import Decimal


class QuotationCostSummaryResponse(BaseModel):
    """Quotation cost summary response"""
    quotation_id: int
    subtotal: Optional[Decimal] = None
    discount_pct: Optional[Decimal] = None
    discounted_subtotal: Optional[Decimal] = None
    gst: Optional[Decimal] = None
    grand_total: Optional[Decimal] = None
    cost_heads: Optional[Dict[str, Decimal]] = None

    class Config:
        from_attributes = True
