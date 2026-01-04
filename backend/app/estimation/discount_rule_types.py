"""
Discount Rule Types
Phase-5: Type definitions for quotation-scoped discount rules
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional, List


class DiscountScope(str, Enum):
    """Discount rule scope types (precedence order: LINE > MAKE_SERIES > CATEGORY > SITE)"""
    SITE = "SITE"                 # quote-level (site discount on quotation)
    CATEGORY = "CATEGORY"         # category-level discount
    MAKE_SERIES = "MAKE_SERIES"   # make+series combination discount
    LINE = "LINE"                 # explicit line override


@dataclass(frozen=True)
class DiscountRule:
    """Immutable discount rule for a quotation"""
    id: int
    tenant_id: int
    quotation_id: int            # NOT NULL (quotation-scoped)
    scope_type: DiscountScope
    scope_key: str                # Deterministic key format (see scope_key formats)
    discount_pct: Decimal         # 0..100
    is_active: bool
    reason: Optional[str] = None
    
    # Audit fields (optional, for display)
    created_by: Optional[int] = None
    created_at: Optional[str] = None


@dataclass(frozen=True)
class DiscountDecision:
    """Result of discount resolution for a line item"""
    effective_discount_pct: Decimal    # Final discount % to apply
    applied_scope: str                  # "LINE"|"MAKE_SERIES"|"CATEGORY"|"SITE"|"NONE"
    applied_rule_id: Optional[int]     # ID of rule that was applied (if any)
    flags: List[str] = field(default_factory=list)  # Warning/info flags (e.g., "MAKE_SERIES_MAPPING_NOT_AVAILABLE")


# Scope key format constants (frozen)
SCOPE_KEY_SITE = "site"                                    # Single per quote
SCOPE_KEY_CATEGORY_PREFIX = "category:"                    # category:{category_id}
SCOPE_KEY_MAKE_SERIES_PREFIX = "make:"                     # make:{make_id}|series:{series_id}
SCOPE_KEY_LINE_PREFIX = "line:"                           # line:{quote_bom_item_id}

