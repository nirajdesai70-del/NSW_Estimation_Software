"""
Quotation copy API schemas
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class CopyQuotationRequest(BaseModel):
    """Request schema for copying a quotation (deep copy)."""

    new_quote_no: Optional[str] = Field(
        default=None, description="New quote number or AUTO for auto suffix"
    )
    copy_panels: bool = Field(default=True, description="Copy panels")
    copy_boms: bool = Field(default=True, description="Copy BOMs (requires panels)")
    copy_bom_items: bool = Field(default=True, description="Copy BOM items (requires BOMs)")


class CopyQuotationResponse(BaseModel):
    """Response schema for copying a quotation."""

    new_quotation_id: int


class CopyPanelResponse(BaseModel):
    """Response schema for copying a panel."""

    new_panel_id: int


class CopyBOMResponse(BaseModel):
    """Response schema for copying a BOM tree."""

    new_bom_id: int

