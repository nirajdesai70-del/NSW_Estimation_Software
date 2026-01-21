"""
Quotation structure read API schemas
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class PanelListItem(BaseModel):
    id: int
    name: Optional[str] = None
    quantity: Optional[float] = None


class FeederListItem(BaseModel):
    id: int
    name: Optional[str] = None
    quantity: Optional[float] = None

