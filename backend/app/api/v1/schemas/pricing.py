"""
Pricing API schemas
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ApplyRecalcRequest(BaseModel):
    """Request schema for apply-recalc endpoint"""
    decision_id: Optional[int] = Field(None, description="Decision ID for audit trail")
    reason: Optional[str] = Field(None, description="Reason for recalculation")


class ApplyRecalcResponse(BaseModel):
    """Response schema for apply-recalc endpoint"""
    quotation_id: int
    decision_id: Optional[int] = None
    message: str
    totals: Dict[str, Any] = Field(..., description="Quotation totals snapshot")
    gst: Optional[Dict[str, Any]] = Field(None, description="GST breakdown")

