"""
Data models for estimation calculations
Phase-5: Type definitions for pricing, discount, tax
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, Any


class RateSource(str, Enum):
    """Rate source enumeration"""

    PRICELIST = "PRICELIST"
    MANUAL = "MANUAL"
    FIXED_NO_DISCOUNT = "FIXED_NO_DISCOUNT"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class PriceSnapshot:
    """Immutable snapshot of pricing decision for a line item"""

    sku_rate: Optional[Decimal]  # rate from SKU pricelist (if applicable)
    override_rate: Optional[Decimal]  # manual override rate (if applicable)
    applied_rate: Decimal  # final applied rate used for calculation
    rate_source: RateSource  # PRICELIST or MANUAL


@dataclass(frozen=True)
class LineInput:
    """Input data for a single line item calculation"""

    line_id: int
    product_id: Optional[int]
    qty: Decimal
    item_discount_pct: Decimal  # 0..100
    rate_source: RateSource
    override_rate: Optional[Decimal]
    override_reason: Optional[str]


@dataclass(frozen=True)
class QuoteInput:
    """Input data for quotation-level calculation"""

    quote_id: int
    quotation_discount_pct: Decimal  # 0..100
    tax_profile_id: Optional[int]  # nullable
    # Optional: price tier, customer tier, currency, etc.
    metadata: Dict[str, Any]


class TaxMode(str, Enum):
    """Tax mode enumeration"""

    CGST_SGST = "CGST_SGST"  # Local: CGST + SGST
    IGST = "IGST"  # Interstate: IGST only


@dataclass(frozen=True)
class TaxSnapshot:
    """Tax calculation snapshot (legacy - single rate)"""

    tax_profile_id: Optional[int]
    tax_rate_pct: Decimal  # 0 if none
    taxable_base: Decimal
    tax_amount: Decimal


@dataclass(frozen=True)
class GstSnapshot:
    """GST calculation snapshot with split components (CGST/SGST/IGST)"""

    tax_profile_id: Optional[int]
    tax_mode: str  # "CGST_SGST" or "IGST"
    taxable_base: Decimal
    cgst_pct: Decimal  # 0..100, quantized to 2dp
    sgst_pct: Decimal  # 0..100, quantized to 2dp
    igst_pct: Decimal  # 0..100, quantized to 2dp
    cgst_amount: Decimal  # quantized to 4dp
    sgst_amount: Decimal  # quantized to 4dp
    igst_amount: Decimal  # quantized to 4dp
    tax_total: Decimal  # cgst + sgst + igst, quantized to 4dp


@dataclass(frozen=True)
class Totals:
    """Final calculated totals for a quotation"""

    subtotal: Decimal
    quotation_discount_pct: Decimal
    discounted_subtotal: Decimal
    tax_rate_pct: Decimal
    tax_amount: Decimal
    grand_total: Decimal


@dataclass(frozen=True)
class PricingPreviewResponse:
    """Response for preview recalculation"""

    stored_totals: Optional[Totals]  # can be None if not stored
    recalculated_preview: Totals
    diff: Dict[str, Any]  # deltas + flags
    policy: Dict[str, Any]  # migration policy info
