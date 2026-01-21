"""
Cost adders API schemas
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CostAdderUpsertRequest(BaseModel):
    cost_head_code: str
    amount: float
    currency: str
    notes: Optional[str] = None


class CostAdderUpsertResponse(BaseModel):
    quotation_id: int
    cost_head_code: str
    amount: float
    currency: str

