"""
Quotation Structure Read Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class PanelListItem(BaseModel):
    """Panel list item schema"""
    id: int
    quotation_id: int
    name: str
    sequence_order: Optional[int] = None
    total_amount: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FeederListItem(BaseModel):
    """Feeder (BOM) list item schema"""
    id: int
    panel_id: int
    quotation_id: int
    name: str
    level: int
    quantity: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    sequence_order: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
