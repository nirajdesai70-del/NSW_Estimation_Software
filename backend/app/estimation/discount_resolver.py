"""
Discount Resolver
Phase-5: Resolves effective discount for a line item using precedence rules
"""
from __future__ import annotations
from typing import Optional, Protocol, List
from decimal import Decimal

from app.estimation.discount_rule_types import (
    DiscountRule,
    DiscountDecision,
    DiscountScope,
    SCOPE_KEY_SITE,
    SCOPE_KEY_CATEGORY_PREFIX,
)

# Percentage quantization: 2 decimal places
PCT_Q = Decimal("0.01")


def qpct(x: Decimal) -> Decimal:
    """Quantize percentage to 2 decimal places"""
    return x.quantize(PCT_Q)


class SkuSeriesLookup(Protocol):
    """
    Protocol for SKU → (make_id, series_id) mapping.
    
    Phase-5: Initially implemented as NullSkuSeriesLookup (returns None, None).
    Later replaced with DbSkuSeriesLookup once SKU mapping table is confirmed.
    """
    
    def get_make_series_for_sku(self, *, sku_id: int) -> tuple[Optional[int], Optional[int]]:
        """
        Return (make_id, series_id) for a SKU.
        
        Args:
            sku_id: SKU identifier
            
        Returns:
            Tuple of (make_id, series_id) or (None, None) if not available
        """
        ...


class NullSkuSeriesLookup:
    """
    Fallback implementation that returns None for make/series.
    
    Used until SKU mapping table is confirmed and DbSkuSeriesLookup is implemented.
    """
    
    def get_make_series_for_sku(self, *, sku_id: int) -> tuple[Optional[int], Optional[int]]:
        """Returns (None, None) - mapping not available yet"""
        return (None, None)


class DiscountResolver:
    """
    Resolves effective discount for a line item using precedence:
    LINE > MAKE_SERIES > CATEGORY > SITE > NONE
    
    All rules are quotation-scoped.
    """
    
    def __init__(self, sku_series_lookup: Optional[SkuSeriesLookup] = None):
        """
        Initialize resolver.
        
        Args:
            sku_series_lookup: SKU to make/series mapping (defaults to NullSkuSeriesLookup)
        """
        self.sku_series_lookup = sku_series_lookup or NullSkuSeriesLookup()
    
    def resolve_for_line(
        self,
        *,
        tenant_id: int,
        quotation_id: int,
        line_id: int,
        sku_id: Optional[int],
        category_id: Optional[int],
        line_discount_pct: Optional[Decimal],
        line_discount_source: Optional[str],  # "LINE" means line override
        rules: List[DiscountRule],
    ) -> DiscountDecision:
        """
        Resolves effective discount for a line item.
        
        Precedence (highest to lowest):
        1. LINE (if line_discount_source == "LINE" and line_discount_pct is set)
        2. MAKE_SERIES (if make_id + series_id match)
        3. CATEGORY (if category_id matches)
        4. SITE (quote-level discount)
        5. NONE (0%)
        
        Args:
            tenant_id: Tenant ID
            quotation_id: Quotation ID
            line_id: Line item ID
            sku_id: SKU ID (for make/series lookup)
            category_id: Category ID (for category rule matching)
            line_discount_pct: Line-level discount % (if explicitly set)
            line_discount_source: "LINE" if line discount is an override
            rules: List of active discount rules for this quotation
            
        Returns:
            DiscountDecision with effective discount, applied scope, and flags
        """
        flags: List[str] = []
        
        # Pre-scan: Check if MAKE_SERIES rules exist
        has_make_series_rules = any(
            r.scope_type == DiscountScope.MAKE_SERIES for r in rules
        )
        
        # 1. Check LINE override (highest precedence)
        if line_discount_source == "LINE" and line_discount_pct is not None:
            pct = qpct(line_discount_pct)
            # Validate range (safety check - API should validate too)
            if pct < 0 or pct > 100:
                flags.append("INVALID_LINE_DISCOUNT_PCT")
                # Fall through to rule-based resolution
            else:
                return DiscountDecision(
                    effective_discount_pct=pct,
                    applied_scope="LINE",
                    applied_rule_id=None,  # Line override is not a rule
                    flags=flags,
                )
        
        # 2. Check MAKE_SERIES rule
        if has_make_series_rules:
            if sku_id is None:
                # SKU ID missing but MAKE_SERIES rules exist
                flags.append("SKU_ID_MISSING_FOR_MAKE_SERIES")
            else:
                make_id, series_id = self.sku_series_lookup.get_make_series_for_sku(sku_id=sku_id)
                if make_id and series_id:
                    make_series_key = f"make:{make_id}|series:{series_id}"
                    for rule in rules:
                        if (rule.scope_type == DiscountScope.MAKE_SERIES and 
                            rule.scope_key == make_series_key):
                            return DiscountDecision(
                                effective_discount_pct=qpct(rule.discount_pct),
                                applied_scope="MAKE_SERIES",
                                applied_rule_id=rule.id,
                                flags=flags,
                            )
                    # MAKE_SERIES rules exist but no match (mapping available but no rule match)
                    # Continue to fallback without flag (this is normal)
                else:
                    # Mapping unavailable: sku_id present but lookup returns None
                    flags.append("MAKE_SERIES_MAPPING_NOT_AVAILABLE")
        
        # 3. Check CATEGORY rule
        if category_id:
            category_key = f"{SCOPE_KEY_CATEGORY_PREFIX}{category_id}"
            for rule in rules:
                if (rule.scope_type == DiscountScope.CATEGORY and 
                    rule.scope_key == category_key):
                    return DiscountDecision(
                        effective_discount_pct=qpct(rule.discount_pct),
                        applied_scope="CATEGORY",
                        applied_rule_id=rule.id,
                        flags=flags,
                    )
        
        # 4. Check SITE rule (quote-level)
        for rule in rules:
            if (rule.scope_type == DiscountScope.SITE and 
                rule.scope_key == SCOPE_KEY_SITE):
                return DiscountDecision(
                    effective_discount_pct=qpct(rule.discount_pct),
                    applied_scope="SITE",
                    applied_rule_id=rule.id,
                    flags=flags,
                )
        
        # 5. No match - return 0%
        return DiscountDecision(
            effective_discount_pct=Decimal("0"),
            applied_scope="NONE",
            applied_rule_id=None,
            flags=flags,
        )

