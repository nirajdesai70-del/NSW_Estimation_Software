"""
Cost Adders Schemas
"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class CostAdderUpsertRequest(BaseModel):
    """Request to upsert cost adder"""
    quotation_id: int
    cost_head_id: int
    amount: Decimal
    description: Optional[str] = None


class CostAdderUpsertResponse(BaseModel):
    """Response after upserting cost adder"""
    id: int
    quotation_id: int
    cost_head_id: int
    amount: Decimal
    description: Optional[str] = None

    class Config:
        from_attributes = True
