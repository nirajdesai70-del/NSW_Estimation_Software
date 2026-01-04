# Alignment Matrix: Freeze v1.2 CLEAN → Implementation → Verification

**Status:** 🟢 ACTIVE (Living Document)  
**Last Updated:** 2026-01-03  
**Scope:** Phase-5 Catalog Pipeline (Motor Control Equipment umbrella — all series and items)  
**Location:** `governance/freeze_v1.2_clean/` (shared across all MCE series)

**Purpose:** Single source of governance truth mapping freeze rules to implementation and verification.

**Review Policy:** This matrix is updated when:
- Real issues arise that require rule clarification
- Implementation patterns evolve
- Verification methods improve

---

## Rule → Implementation → Verification Mapping

| Freeze v1.2 CLEAN Rule | Where Implemented | How Verified | Status |
|------------------------|-------------------|--------------|--------|
| **SC_Lx = Structural Only (SCL)** | Scripts preserve SC_Lx as-is, no capability mapping | Gate D: Regex scan for forbidden tokens (AC1, AC3, kW, HP, WITH_*, AUX, SHUNT, UV, DRAWOUT, COIL, VOLT) = 0 hits | ✅ Pass |
| **Capability separation via capability_codes** | Capability stays in `capability_codes` column, never in SC_Lx | Gate E: Prints SC_Lx cols + capability cols (no overlap) | ✅ Pass |
| **Generic neutrality (generic fields only)** | GenericDescriptor, l0_name, l1_name are vendor/series-neutral | Gate C: Word-boundary scan on generic fields only (excludes identity fields: make, series_name, OEM_Catalog_No, sku_code) = 0 hits | ✅ Pass |
| **No OEM/Series leakage (non-word-bound patterns)** | Generic fields must not contain substring patterns like "LC1E-", "TeSysX", etc. | Gate H: Substring pattern scan (non-word-bound) for OEM/series patterns in generic fields = 0 hits | ✅ Pass |
| **Layer-1/Layer-2 mode boundary** | Phase-5 = Catalog Pipeline Mode (facts + derivations, no BOM enforcement) | Manual review: No accessory dependency enforcement, no BOM explosion, no runtime QC gating | ✅ Pass |
| **L0/L1/L2 level discipline** | L0/L1 = generic (neutral), L2 = identity + SKU + price | Manual review: Make/Series/Price are L2-only, generic names are L0/L1-only | ✅ Pass |
| **Price authority (L2 only)** | Prices exist only in NSW_PRICE_MATRIX | Gate G: Price exists only in price matrix, not in L0/L1 generic tables | ✅ Pass |
| **Identity fields allowed in L1 (traceability)** | series_name, make, OEM_Catalog_No allowed in L1 sheets for reference | Gate C: Excludes identity fields from generic naming scan | ✅ Pass |
| **Column contract (SoR schema stability)** | Required columns must exist per logical sheet role | Gate I: Required columns present per logical role (name-based or column-based resolution) | ✅ Pass |

---

## Verification Gate Summary

| Gate | Target | Current Result | Status |
|------|--------|----------------|--------|
| Gate A | File exists | ✅ Pass | ✅ |
| Gate B | Sheet structure | ✅ All expected sheets present | ✅ |
| Gate B2 | Row counts (non-empty) | ✅ L2: 23, L1: 118, Price: 59 | ✅ |
| Gate C | Generic naming (generic fields only) | ✅ 0 hits (identity fields excluded) | ✅ |
| Gate D | SC_Lx structural-only | ✅ 0 hits | ✅ |
| Gate E | Capability separation | ✅ SC_Lx ≠ capability | ✅ |
| Gate F | Layer discipline | ✅ L0/L1/L2 boundaries respected | ✅ |
| Gate G | Price discipline | ✅ Price only in matrix | ✅ |
| Gate H | Non-word-bound leakage | ✅ No OEM/series patterns in generic fields | ✅ |
| Gate I | Column contract | ✅ Required columns present per logical role | ✅ |

---

## Known Issues & Resolutions

### Issue 1: Generic Naming Validator Scope (Resolved)
**Problem:** Initial Gate C flagged `series_name` column (identity field, not generic)  
**Resolution:** Updated validator to scan only generic fields (GenericDescriptor, l0_name, l1_name)  
**Date:** 2026-01-03  
**Status:** ✅ Resolved

### Issue 2: Series Leakage in L1 Descriptors (Resolved)
**Problem:** `derive_l1_from_l2.py` included `series_bucket` in GenericDescriptor  
**Resolution:** Removed series_bucket from descriptor generation  
**Date:** 2026-01-03  
**Status:** ✅ Resolved

---

## Review & Correction Process

**When a rule becomes a roadblock:**

1. **Document the issue** in this matrix (add to "Known Issues & Resolutions")
2. **Review carefully** with freeze docs and implementation
3. **Propose correction** (rule update, implementation fix, or verification adjustment)
4. **Update this matrix** with resolution
5. **Commit change** with clear rationale

**Principle:** Rules are required, but when they block progress, we review and adopt what's useful.

---

## Series Processed

| Series | Date Processed | Status | Notes |
|--------|----------------|--------|-------|
| LC1E | 2026-01-03 | ✅ Complete | All gates passed, QC-Passed status |

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-01-03 | Initial matrix created | Phase-5 LC1E execution complete |
| 2026-01-03 | Added Gate C scope clarification | Resolved false-positive identity field hits |
| 2026-01-03 | Added Issue 1 & 2 resolutions | Documented fixes applied |
| 2026-01-03 | Added Gate H (non-word-bound leakage check) | Enhanced generic naming validation |
| 2026-01-03 | Updated scope to MCE umbrella | Aligned with SoR/SoE contracts |
| 2026-01-03 | Moved to shared governance folder | Prevent divergence across series |
| 2026-01-03 | Added Gate I (Column Contract) | Prevent schema drift via required column validation |

---

**Next Review:** When next series (LC1D, MPCB, etc.) is processed, or when real issues arise.

