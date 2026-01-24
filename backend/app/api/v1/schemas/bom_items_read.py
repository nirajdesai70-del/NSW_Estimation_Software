"""
BOM Items Read Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class BOMItemListItem(BaseModel):
    """BOM Item list item schema"""
    id: int
    bom_id: int
    panel_id: int
    quotation_id: int
    product_id: Optional[int] = None
    quantity: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    sequence_order: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
