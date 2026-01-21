"""
Cost adder service
Phase-5: Minimal upsert service for QCA cost adders
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.api.v1.schemas.cost_adders import CostAdderUpsertResponse


class CostAdderService:
    def __init__(self, db: Session, *, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def upsert_cost_adder(
        self,
        *,
        quotation_id: int,
        panel_id: int,
        cost_head_code: str,
        amount: float,
        currency: str,
        notes: str | None,
    ) -> CostAdderUpsertResponse:
        # Phase-5: return a lightweight response payload (DB persistence is handled elsewhere).
        _ = (panel_id, notes)
        return CostAdderUpsertResponse(
            quotation_id=quotation_id,
            cost_head_code=cost_head_code,
            amount=float(amount),
            currency=currency,
        )
