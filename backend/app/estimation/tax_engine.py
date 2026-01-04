"""
Tax Engine
Phase-5: Deterministic GST calculation with split components (CGST/SGST/IGST)
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP

from app.estimation.types import TaxMode, GstSnapshot
from app.estimation.decimal_norm import qrate

# Quantization precision for percentages: 2 decimal places (0.01)
PCT_Q = Decimal("0.01")


def qpct(x: Decimal) -> Decimal:
    """
    Quantize percentage to 2 decimal places for determinism.
    
    Args:
        x: Decimal percentage value (0..100)
        
    Returns:
        Quantized Decimal with 2 decimal places
    """
    return x.quantize(PCT_Q, rounding=ROUND_HALF_UP)


class TaxEngine:
    """
    Deterministic tax calculation engine for GST (split: CGST/SGST/IGST).
    
    Rules:
    - Mode CGST_SGST: applies cgst_pct + sgst_pct, forces igst=0
    - Mode IGST: applies igst_pct, forces cgst=sgst=0
    - All percentages quantized to 2dp
    - All amounts quantized to 4dp (using qrate)
    """
    
    @staticmethod
    def calculate_gst(
        *,
        taxable_base: Decimal,
        tax_profile: dict,  # {id?, cgst_pct, sgst_pct, igst_pct}
        tax_mode: TaxMode,  # ✅ now Enum, not str
    ) -> GstSnapshot:
        """
        Calculate GST with split components.
        
        Args:
            taxable_base: Base amount (after discounts, quantized to 4dp)
            tax_profile: Dict with keys: cgst_pct, sgst_pct, igst_pct (all Decimal)
            tax_mode: TaxMode enum (CGST_SGST or IGST)
            
        Returns:
            GstSnapshot with all components calculated and quantized
            
        Raises:
            ValueError: If tax_mode is invalid
        """
        if tax_mode not in (TaxMode.CGST_SGST, TaxMode.IGST):
            raise ValueError(f"Invalid tax_mode: {tax_mode}. Must be CGST_SGST or IGST")
        
        # Ensure taxable_base is quantized
        base = qrate(taxable_base)
        
        # Use consistent zeroes (quantized)
        zero_amt = qrate(Decimal("0"))
        zero_pct = qpct(Decimal("0"))
        
        # Extract rates from profile (quantize to 2dp)
        cgst_pct = qpct(Decimal(str(tax_profile.get("cgst_pct", 0))))
        sgst_pct = qpct(Decimal(str(tax_profile.get("sgst_pct", 0))))
        igst_pct = qpct(Decimal(str(tax_profile.get("igst_pct", 0))))
        
        # Apply mode rules
        if tax_mode == TaxMode.CGST_SGST:
            # Local mode: apply CGST + SGST, force IGST to 0
            igst_pct = zero_pct
            igst_amount = zero_amt
            
            cgst_amount = qrate(base * (cgst_pct / Decimal("100")))
            sgst_amount = qrate(base * (sgst_pct / Decimal("100")))
            
        else:  # TaxMode.IGST
            # Interstate mode: apply IGST, force CGST/SGST to 0
            cgst_pct = zero_pct
            sgst_pct = zero_pct
            cgst_amount = zero_amt
            sgst_amount = zero_amt
            
            igst_amount = qrate(base * (igst_pct / Decimal("100")))
        
        # Calculate total tax
        tax_total = qrate(cgst_amount + sgst_amount + igst_amount)
        
        # Extract tax_profile_id if available
        tax_profile_id = tax_profile.get("id")
        
        return GstSnapshot(
            tax_profile_id=tax_profile_id,
            tax_mode=tax_mode.value,  # keep snapshot stored as string
            taxable_base=base,
            cgst_pct=cgst_pct,
            sgst_pct=sgst_pct,
            igst_pct=igst_pct,
            cgst_amount=cgst_amount,
            sgst_amount=sgst_amount,
            igst_amount=igst_amount,
            tax_total=tax_total,
        )

