"""
Discount Engine
Phase-5: Pure math functions for applying discounts
"""
from __future__ import annotations
from decimal import Decimal

from app.estimation.decimal_norm import qrate

# Percentage quantization: 2 decimal places
PCT_Q = Decimal("0.01")


def qpct(x: Decimal) -> Decimal:
    """Quantize percentage to 2 decimal places for determinism"""
    return x.quantize(PCT_Q)


class DiscountEngine:
    """
    Pure discount calculation functions.
    All calculations are deterministic (quantized).
    """
    
    @staticmethod
    def validate_pct(pct: Decimal) -> None:
        """
        Validate discount percentage is in range [0, 100].
        
        Args:
            pct: Discount percentage
            
        Raises:
            ValueError: If pct is outside [0, 100]
        """
        normalized = qpct(pct)
        if normalized < 0 or normalized > 100:
            raise ValueError(f"discount_pct must be between 0 and 100, got {normalized}")
    
    @classmethod
    def apply_item_discount(
        cls,
        *,
        applied_rate: Decimal,
        item_discount_pct: Decimal,
    ) -> Decimal:
        """
        Apply item-level discount to rate.
        
        Formula: net_rate = applied_rate * (1 - item_discount_pct / 100)
        
        Args:
            applied_rate: Base rate (already quantized)
            item_discount_pct: Item discount percentage (0..100)
            
        Returns:
            Net rate after discount (quantized to 4 decimal places)
        """
        pct = qpct(item_discount_pct)
        cls.validate_pct(pct)
        
        net = applied_rate * (Decimal("1") - (pct / Decimal("100")))
        return qrate(net)
    
    @staticmethod
    def compute_line_amount(
        *,
        qty: Decimal,
        net_rate: Decimal,
    ) -> Decimal:
        """
        Compute line amount from quantity and net rate.
        
        Formula: amount = qty * net_rate
        
        Args:
            qty: Quantity
            net_rate: Net rate after discounts (quantized)
            
        Returns:
            Line amount (quantized to 4 decimal places)
        """
        amt = qty * net_rate
        return qrate(amt)
    
    @classmethod
    def apply_quotation_discount(
        cls,
        *,
        subtotal: Decimal,
        quotation_discount_pct: Decimal,
    ) -> Decimal:
        """
        Apply quotation-level discount to subtotal.
        
        Formula: discounted_subtotal = subtotal * (1 - quotation_discount_pct / 100)
        
        Args:
            subtotal: Subtotal after item discounts (quantized)
            quotation_discount_pct: Quotation discount percentage (0..100)
            
        Returns:
            Discounted subtotal (quantized to 4 decimal places)
        """
        pct = qpct(quotation_discount_pct)
        cls.validate_pct(pct)
        
        out = subtotal * (Decimal("1") - (pct / Decimal("100")))
        return qrate(out)

