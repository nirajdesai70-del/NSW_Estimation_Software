"""
Decimal Normalization
Phase-5: Deterministic decimal quantization for rates
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP

# Quantization precision: 4 decimal places (0.0001)
RATE_Q = Decimal("0.0001")


def qrate(x: Decimal) -> Decimal:
    """
    Quantize rate to 4 decimal places for determinism.
    
    Ensures same input produces same output regardless of
    source precision (e.g., 1000 vs 1000.00).
    
    Args:
        x: Decimal rate value
        
    Returns:
        Quantized Decimal with 4 decimal places
    """
    return x.quantize(RATE_Q, rounding=ROUND_HALF_UP)

