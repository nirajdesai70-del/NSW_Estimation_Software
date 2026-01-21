"""
Tax Profile Lookup
Phase-5: Fetch tax profiles from database (tenant-scoped)
"""
from __future__ import annotations
from typing import Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import text


class TaxProfileLookup:
    """
    Lookup service for tax profiles.
    
    Validates:
    - Profile must exist
    - Profile must belong to tenant
    - Profile must be active
    """
    
    def __init__(self, db: Session):
        """
        Initialize lookup service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_profile(
        self,
        *,
        tenant_id: int,
        tax_profile_id: int,
    ) -> Dict[str, Any]:
        """
        Fetch tax profile by ID.
        
        Args:
            tenant_id: Tenant ID
            tax_profile_id: Tax profile ID
            
        Returns:
            Dict with keys: id, tenant_id, name, cgst_pct, sgst_pct, igst_pct, is_active
            (percentages as Decimal)
            
        Raises:
            ValueError: If profile not found, inactive, or doesn't belong to tenant
        """
        result = self.db.execute(
            text("""
                SELECT 
                    id,
                    tenant_id,
                    name,
                    cgst_pct,
                    sgst_pct,
                    igst_pct,
                    is_active
                FROM tax_profiles
                WHERE id = :tax_profile_id
                  AND tenant_id = :tenant_id
            """),
            {
                "tax_profile_id": tax_profile_id,
                "tenant_id": tenant_id,
            }
        ).mappings().first()
        
        if not result:
            raise ValueError(
                f"Tax profile {tax_profile_id} not found for tenant {tenant_id}"
            )
        
        if not result["is_active"]:
            raise ValueError(
                f"Tax profile {tax_profile_id} is not active"
            )
        
        # Convert to Decimal and quantize percentages
        return {
            "id": int(result["id"]),
            "tenant_id": int(result["tenant_id"]),
            "name": str(result["name"]),
            "cgst_pct": Decimal(str(result["cgst_pct"])),
            "sgst_pct": Decimal(str(result["sgst_pct"])),
            "igst_pct": Decimal(str(result["igst_pct"])),
            "is_active": bool(result["is_active"]),
        }

