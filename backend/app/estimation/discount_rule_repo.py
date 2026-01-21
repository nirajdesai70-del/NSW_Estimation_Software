"""
Discount Rule Repository
Phase-5: DB operations for discount rules (quotation-scoped)
"""
from __future__ import annotations
from typing import Optional, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text




class DiscountRuleRepo:
    """Repository for discount rule CRUD operations"""
    
    def __init__(self, db: Session):
        """
        Initialize repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def upsert_rule(
        self,
        *,
        tenant_id: int,
        quotation_id: int,
        scope_type: str,
        scope_key: str,
        discount_pct: Decimal,
        reason: Optional[str],
        actor_id: int,
    ) -> Tuple[str, int, Optional[Decimal]]:
        """
        Create or update a discount rule.
        
        Handles inactive rules by reactivating them (prevents unique constraint violation).
        
        Args:
            tenant_id: Tenant ID
            quotation_id: Quotation ID
            scope_type: Scope type (SITE, CATEGORY, MAKE_SERIES)
            scope_key: Scope key (deterministic format)
            discount_pct: Discount percentage (0..100)
            reason: Optional reason
            actor_id: User ID performing the action
            
        Returns:
            Tuple of (action, rule_id, old_discount_pct) where:
            - action is 'SET' or 'UPDATE'
            - old_discount_pct is None for SET, previous value for UPDATE
        """
        # Find existing rule regardless of is_active (to handle reactivation)
        existing = self.db.execute(
            text("""
                SELECT id, discount_pct, is_active
                FROM discount_rules
                WHERE tenant_id = :tenant_id
                  AND quotation_id = :quotation_id
                  AND scope_type = :scope_type
                  AND scope_key = :scope_key
            """),
            {
                "tenant_id": tenant_id,
                "quotation_id": quotation_id,
                "scope_type": scope_type,
                "scope_key": scope_key,
            }
        ).mappings().first()
        
        if existing:
            old_pct = Decimal(str(existing["discount_pct"]))
            # Update existing rule (reactivate if inactive)
            self.db.execute(
                text("""
                    UPDATE discount_rules
                    SET 
                        discount_pct = :pct,
                        reason = :reason,
                        is_active = true,
                        updated_by = :actor_id,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :id
                """),
                {
                    "pct": discount_pct,
                    "reason": reason,
                    "actor_id": actor_id,
                    "id": existing["id"],
                }
            )
            return ("UPDATE", int(existing["id"]), old_pct)
        
        # Create new rule
        rule_id = self.db.execute(
            text("""
                INSERT INTO discount_rules (
                    tenant_id,
                    quotation_id,
                    scope_type,
                    scope_key,
                    discount_pct,
                    reason,
                    is_active,
                    created_by,
                    created_at,
                    updated_by,
                    updated_at
                ) VALUES (
                    :tenant_id,
                    :quotation_id,
                    :scope_type,
                    :scope_key,
                    :pct,
                    :reason,
                    true,
                    :actor_id,
                    CURRENT_TIMESTAMP,
                    :actor_id,
                    CURRENT_TIMESTAMP
                ) RETURNING id
            """),
            {
                "tenant_id": tenant_id,
                "quotation_id": quotation_id,
                "scope_type": scope_type,
                "scope_key": scope_key,
                "pct": discount_pct,
                "reason": reason,
                "actor_id": actor_id,
            }
        ).scalar_one()
        
        return ("SET", int(rule_id), None)
    
    def deactivate_rule(
        self,
        *,
        tenant_id: int,
        quotation_id: int,
        rule_id: int,
        actor_id: int,
    ) -> None:
        """
        Deactivate a discount rule (soft delete).
        
        Args:
            tenant_id: Tenant ID
            quotation_id: Quotation ID
            rule_id: Rule ID to deactivate
            actor_id: User ID performing the action
        """
        self.db.execute(
            text("""
                UPDATE discount_rules
                SET 
                    is_active = false,
                    updated_by = :actor_id,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = :rule_id
                  AND tenant_id = :tenant_id
                  AND quotation_id = :quotation_id
            """),
            {
                "actor_id": actor_id,
                "rule_id": rule_id,
                "tenant_id": tenant_id,
                "quotation_id": quotation_id,
            }
        )
    
    def set_line_override(
        self,
        *,
        tenant_id: int,
        quotation_id: int,
        line_id: int,
        discount_pct: Decimal,
        reason: Optional[str],  # Stored in audit metadata, not on line
        actor_id: int,
    ) -> None:
        """
        Set line-level discount override.
        
        Uses tenant-safe join through quotations table.
        
        Args:
            tenant_id: Tenant ID
            quotation_id: Quotation ID
            line_id: Line item ID
            discount_pct: Discount percentage (0..100)
            reason: Optional reason (stored in audit metadata only)
            actor_id: User ID performing the action
            
        Raises:
            ValueError: If line not found for quote/tenant (rowcount == 0)
        """
        result = self.db.execute(
            text("""
                UPDATE quote_bom_items qbi
                SET 
                    discount_pct = :pct,
                    discount_source = 'LINE',
                    updated_at = CURRENT_TIMESTAMP
                FROM quotations q
                WHERE qbi.id = :line_id
                  AND qbi.quotation_id = q.id
                  AND q.id = :quotation_id
                  AND q.tenant_id = :tenant_id
            """),
            {
                "pct": discount_pct,
                "line_id": line_id,
                "quotation_id": quotation_id,
                "tenant_id": tenant_id,
            }
        )
        
        if result.rowcount == 0:
            raise ValueError(
                f"Line override failed: line {line_id} not found for quotation {quotation_id}/tenant {tenant_id}"
            )

