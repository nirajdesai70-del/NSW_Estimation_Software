"""
Quotation discount API schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class QuotationDiscountSetRequest(BaseModel):
    """Request schema for setting quotation-level discount"""
    discount_pct: float = Field(..., ge=0.0, le=100.0, description="Discount percentage (0-100)")
    reason: Optional[str] = Field(None, description="Reason for discount change")


class QuotationDiscountSetResponse(BaseModel):
    """Response schema for setting quotation-level discount"""
    quotation_id: int
    discount_pct: float
    message: str

