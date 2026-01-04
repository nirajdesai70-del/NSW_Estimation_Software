"""
Rate Source DB Mapping
Phase-5: Maps internal RateSource enum to/from DB enum values
"""
from __future__ import annotations
from typing import Optional
from app.estimation.types import RateSource

# DB enum values (from schema migration 20260104_110400)
DB_RATE_PRICELIST = "PRICELIST"
DB_RATE_MANUAL_DEFAULT = "MANUAL_WITH_DISCOUNT"   # Option A (locked)
DB_RATE_FIXED_NO_DISCOUNT = "FIXED_NO_DISCOUNT"
DB_RATE_UNRESOLVED = "UNRESOLVED"

# All DB values that map to internal MANUAL (only MANUAL_WITH_DISCOUNT now)
DB_MANUAL_VALUES = {DB_RATE_MANUAL_DEFAULT}


def db_to_internal_rate_source(db_value: Optional[str]) -> RateSource:
    """
    Convert DB rate_source value to internal RateSource enum.
    
    Maps DB enum values to internal enum values without loss of information:
    - PRICELIST -> PRICELIST
    - MANUAL_WITH_DISCOUNT -> MANUAL
    - FIXED_NO_DISCOUNT -> FIXED_NO_DISCOUNT
    - UNRESOLVED -> UNRESOLVED
    
    Args:
        db_value: DB rate_source string value
        
    Returns:
        Internal RateSource enum value
    """
    if not db_value:
        return RateSource.UNRESOLVED
    if db_value == DB_RATE_PRICELIST:
        return RateSource.PRICELIST
    if db_value == DB_RATE_MANUAL_DEFAULT:
        return RateSource.MANUAL
    if db_value == DB_RATE_FIXED_NO_DISCOUNT:
        return RateSource.FIXED_NO_DISCOUNT
    if db_value == DB_RATE_UNRESOLVED:
        return RateSource.UNRESOLVED
    # Default fallback for unknown values
    return RateSource.UNRESOLVED


def internal_to_db_rate_source(internal: RateSource) -> str:
    """
    Convert internal RateSource enum to DB rate_source value.
    
    Maps internal enum values to DB enum values:
    - PRICELIST -> PRICELIST
    - MANUAL -> MANUAL_WITH_DISCOUNT (Option A locked)
    - FIXED_NO_DISCOUNT -> FIXED_NO_DISCOUNT
    - UNRESOLVED -> UNRESOLVED
    
    Args:
        internal: Internal RateSource enum value
        
    Returns:
        DB rate_source string value
    """
    if internal == RateSource.PRICELIST:
        return DB_RATE_PRICELIST
    if internal == RateSource.MANUAL:
        return DB_RATE_MANUAL_DEFAULT
    if internal == RateSource.FIXED_NO_DISCOUNT:
        return DB_RATE_FIXED_NO_DISCOUNT
    if internal == RateSource.UNRESOLVED:
        return DB_RATE_UNRESOLVED
    # Default fallback
    return DB_RATE_UNRESOLVED

