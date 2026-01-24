"""
Cost Adder Service
"""
from typing import Optional, List, Dict
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.v1.schemas.cost_adders import CostAdderUpsertRequest, CostAdderUpsertResponse


class CostAdderService:
    """Service for managing cost adders on quotations"""
    
    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id
    
    def upsert_cost_adder(
        self,
        quotation_id: int,
        panel_id: int,
        cost_head_code: str,
        amount: Decimal,
        currency: Optional[str] = None,
        notes: Optional[str] = None
    ) -> CostAdderUpsertResponse:
        """
        Upsert cost adder for a quotation panel.
        
        Enforces uniqueness: one row per (tenant_id, quotation_id, panel_id, cost_head_code).
        """
        # Get cost_head_id from code
        cost_head = self.db.execute(
            text("""
                SELECT id FROM cost_heads
                WHERE tenant_id = :tenant_id AND code = :code
            """),
            {"tenant_id": self.tenant_id, "code": cost_head_code}
        ).first()
        
        if not cost_head:
            raise ValueError(f"Cost head '{cost_head_code}' not found")
        
        cost_head_id = cost_head.id
        
        # Check if cost adder already exists
        existing = self.db.execute(
            text("""
                SELECT id FROM quotation_cost_adders
                WHERE tenant_id = :tenant_id
                  AND quotation_id = :quotation_id
                  AND panel_id = :panel_id
                  AND cost_head_id = :cost_head_id
            """),
            {
                "tenant_id": self.tenant_id,
                "quotation_id": quotation_id,
                "panel_id": panel_id,
                "cost_head_id": cost_head_id,
            }
        ).first()
        
        if existing:
            # Update existing
            self.db.execute(
                text("""
                    UPDATE quotation_cost_adders
                    SET amount = :amount,
                        notes = :notes,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :id
                """),
                {
                    "id": existing.id,
                    "amount": amount,
                    "notes": notes,
                }
            )
            self.db.commit()
            return CostAdderUpsertResponse(
                id=existing.id,
                quotation_id=quotation_id,
                cost_head_id=cost_head_id,
                amount=amount,
                description=notes,
            )
        else:
            # Insert new
            result = self.db.execute(
                text("""
                    INSERT INTO quotation_cost_adders
                    (tenant_id, quotation_id, panel_id, cost_head_id, amount, notes)
                    VALUES (:tenant_id, :quotation_id, :panel_id, :cost_head_id, :amount, :notes)
                    RETURNING id
                """),
                {
                    "tenant_id": self.tenant_id,
                    "quotation_id": quotation_id,
                    "panel_id": panel_id,
                    "cost_head_id": cost_head_id,
                    "amount": amount,
                    "notes": notes,
                }
            )
            self.db.commit()
            cost_adder_id = result.scalar()
            return CostAdderUpsertResponse(
                id=cost_adder_id,
                quotation_id=quotation_id,
                cost_head_id=cost_head_id,
                amount=amount,
                description=notes,
            )
