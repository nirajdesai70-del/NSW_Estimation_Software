"""
Quotation Copy Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CopyQuotationRequest(BaseModel):
    """Request to copy a quotation"""
    source_quotation_id: int
    target_name: Optional[str] = None


class CopyQuotationResponse(BaseModel):
    """Response after copying a quotation"""
    quotation_id: int
    name: str
    created_at: datetime


class CopyPanelResponse(BaseModel):
    """Response for copied panel"""
    panel_id: int
    name: str


class CopyBOMResponse(BaseModel):
    """Response for copied BOM"""
    bom_id: int
    item_count: int
