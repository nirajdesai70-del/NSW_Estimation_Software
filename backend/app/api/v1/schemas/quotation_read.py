"""
Quotation Read Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class QuotationListItem(BaseModel):
    """Quotation list item schema"""
    id: int
    tenant_id: int
    name: str
    customer_id: Optional[int] = None
    status: Optional[str] = None
    total_amount: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QuotationDetail(BaseModel):
    """Quotation detail schema"""
    id: int
    tenant_id: int
    name: str
    customer_id: Optional[int] = None
    status: Optional[str] = None
    total_amount: Optional[Decimal] = None
    quotation_discount_pct: Optional[Decimal] = None
    tax_profile_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True
