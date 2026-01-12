"""
Discount Rule Lookup
Phase-5: DB query layer for fetching quotation-scoped discount rules
"""
from __future__ import annotations
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.estimation.discount_rule_types import DiscountRule, DiscountScope


class DiscountRuleLookup:
    """
    Fetches active discount rules for a quotation.
    All rules are quotation-scoped (quotation_id NOT NULL).
    """
    
    def __init__(self, db: Session):
        """
        Initialize lookup service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def list_active_rules_for_quote(
        self,
        *,
        tenant_id: int,
        quotation_id: int,
    ) -> List[DiscountRule]:
        """
        Returns active discount rules relevant to this quotation.
        
        Args:
            tenant_id: Tenant ID
            quotation_id: Quotation ID
            
        Returns:
            List of active DiscountRule objects (sorted by precedence: LINE > MAKE_SERIES > CATEGORY > SITE)
        """
        query = text("""
            SELECT 
                id,
                tenant_id,
                quotation_id,
                scope_type,
                scope_key,
                discount_pct,
                is_active,
                reason,
                created_by,
                created_at
            FROM discount_rules
            WHERE tenant_id = :tenant_id
              AND quotation_id = :quotation_id
              AND is_active = true
            ORDER BY 
                CASE scope_type
                    WHEN 'LINE' THEN 1
                    WHEN 'MAKE_SERIES' THEN 2
                    WHEN 'CATEGORY' THEN 3
                    WHEN 'SITE' THEN 4
                END,
                id ASC
        """)
        
        result = self.db.execute(
            query,
            {
                "tenant_id": tenant_id,
                "quotation_id": quotation_id,
            }
        ).mappings().all()
        
        rules = []
        for row in result:
            rules.append(DiscountRule(
                id=row['id'],
                tenant_id=row['tenant_id'],
                quotation_id=row['quotation_id'],
                scope_type=DiscountScope(row['scope_type']),
                scope_key=row['scope_key'],
                discount_pct=Decimal(str(row['discount_pct'])),
                is_active=row['is_active'],
                reason=row['reason'],
                created_by=row['created_by'],
                created_at=str(row['created_at']) if row['created_at'] else None,
            ))
        
        return rules

