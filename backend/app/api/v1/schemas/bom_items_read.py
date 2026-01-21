"""
BOM items read API schemas
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class BOMItemListItem(BaseModel):
    id: int
    name: Optional[str] = None
    quantity: Optional[float] = None

