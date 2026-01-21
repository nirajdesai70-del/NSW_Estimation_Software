"""
Quotation read API schemas
"""
from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class QuotationListItem(BaseModel):
    """Minimal list item for quotation queries."""

    id: int
    quote_no: Optional[str] = None
    status: Optional[str] = None


class QuotationDetail(BaseModel):
    """Minimal detail payload for quotation read endpoints."""

    id: int
    quote_no: Optional[str] = None
    status: Optional[str] = None
    panels: List[dict] = []

