---
Source: docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISION_SUMMARY.md
KB_Namespace: phase5_docs
Status: WORKING
Last_Updated: 2025-12-27T10:59:25.269179
KB_Path: phase5_pack/04_RULES_LIBRARY/governance/PHASE_5_DECISION_SUMMARY.md
---

# Phase 5 Decision Summary - Quick Reference

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DECISION REQUIRED  
**Purpose:** Quick decision-making guide for Phase 5 changes

---

## Critical Confirmation Question

**Before proceeding, confirm:**

> **"Phase-5 explosion will allow multiple L1 rows to resolve to the same L2 SKU."**

**Once confirmed, we will:**
- ✅ Patch Phase-5 execution spec
- ✅ Provide diff-style checklist of exactly what to update
- ✅ Proceed cleanly

---

## What Changed (TL;DR)

### The Insight
Price list working revealed that **L2 must be SKU-pure (commercial only)**, and **L1 carries all engineering meaning**.

### The Correction
- ❌ **OLD:** Different duty/rating = different SKU
- ✅ **NEW:** Same SKU, multiple L1 interpretations, same price

### The Impact
- ✅ **Simplifies Phase 5** once aligned correctly
- ✅ **No SKU duplication**
- ✅ **Clear separation:** engineering meaning vs commercial SKU

---

## What Stays the Same ✅

| Area | Status |
|------|-------|
| Catalog pipeline | ✅ No rework |
| Price history | ✅ No rework |
| SKU import | ✅ No rework |
| BOM totals | ✅ No rework |
| Phase-4 legacy | ✅ Isolated |

**Only Phase 5 logic documents + explosion rules need alignment — not code rewrite.**

---

## What Must Change 🔴

### 1. Explosion Logic (CRITICAL)

**❌ OLD:**
```
Duty × Rating × Voltage → multiple L2 rows
```

**✅ NEW:**
```
Engineering interpretation → multiple L1 rows
Commercial reality → single L2 row
```

**Key Rule:** Multiple L1 rows can legally map to the same L2 SKU.

### 2. L2 Import Structure

**❌ OLD:** Trying to encode engineering meaning into price list

**✅ NEW:** Price list imports create L2-only records. L1 and L0 are derived, not imported.

**Final Rule:** If a field is not mandatory for L2, it must not be imported.

### 3. Validation Rules

**Must Add:**
- ✅ L1 validation rules must allow same SKU mapping for multiple L1 rows
- ✅ UI must not assume 1 L1 → 1 SKU

---

## Documents Created

### New Documents ✅

1. **Phase 5 Impact Assessment**
   - `docs/PHASE_5/00_GOVERNANCE/PHASE_5_PRICE_LIST_IMPACT_ASSESSMENT.md`
   - Comprehensive impact analysis

2. **L2 Import Structure**
   - `docs/PHASE_5/CANONICAL/L2_IMPORT_STRUCTURE_v1.3.1.md`
   - Final L2 import specification

3. **Excel Template Structure**
   - `docs/PHASE_5/CANONICAL/EXCEL_TEMPLATE_STRUCTURE_v1.3.1.md`
   - Excel template specification

4. **OpenAPI Contract**
   - `docs/PHASE_5/CANONICAL/openapi_l2_first.yaml`
   - API contract for L2 import endpoints

5. **L1/L2 Explosion Logic**
   - `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/L1_L2_EXPLOSION_LOGIC.md`
   - Corrected explosion rules

---

## Documents to Update 📋

### High Priority

1. **Data Dictionary**
   - `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md`
   - Add L1 validation rules for SKU reuse
   - Clarify L1 → L2 is many-to-one

2. **Schema Canon**
   - `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
   - Verify L1 table supports many-to-one L2 mapping
   - Add explicit "NOT stored in L2" section

3. **Validation Guardrails**
   - `docs/PHASE_5/03_DATA_DICTIONARY/VALIDATION_GUARDRAILS_G1_G7.md`
   - Add G8: L1-SKU reuse rule

### Medium Priority

4. **Post-Phase 5 Implementation Roadmap**
   - `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/POST_PHASE_5_IMPLEMENTATION_ROADMAP.md`
   - Update explosion service section
   - Add L2-first import workflow

---

## 5R Summary

### RESULTS ✅
- Phase-5 becomes simpler and more robust
- Clear separation: engineering meaning vs commercial SKU
- No SKU duplication

### RISKS (Removed) ✅
- Over-exploded SKUs
- Pricing inconsistency
- Frame/pole misuse as multipliers

### RULES (Locked) 🔒
1. L2 = commercial truth only
2. L1 = engineering interpretation
3. Same SKU may serve many L1s
4. Duty/rating never creates SKU unless OEM changes catalog number
5. Accessories resolve via feature policy, not multiplication

### ROADMAP 📋
1. ✅ Update Phase-5 explosion spec (DONE)
2. ⏳ Update L1 validation rules (PENDING)
3. ⏳ Proceed with LC1D → LC1K → MPCB confidently
4. ⏳ Resume full Phase-5 execution

### REFERENCES 📚
- NSW Master Fundamentals v2.0
- Feature policy doctrine
- L1/L2 inheritance model
- ADR-005 governance firewall
- Schneider L2/L1 Differentiation Clarification v1.0

---

## Next Steps

### Immediate (Before Phase 5 Execution)

1. **Confirm:** "Phase-5 explosion will allow multiple L1 rows to resolve to the same L2 SKU"
2. **Update:** Data Dictionary with L1 validation rules
3. **Update:** Schema Canon with L1 many-to-one L2 mapping
4. **Update:** Validation Guardrails with G8 rule

### During Phase 5 Execution

- Follow updated explosion logic
- Use L2-first import approach
- Validate L1 → L2 many-to-one mapping

### After Phase 5 (Implementation)

- Implement L2 import endpoints
- Implement L1 derivation service
- Implement explosion service with SKU reuse

---

## Quick Decision Matrix

| Question | Answer |
|----------|--------|
| Does Phase 5 break? | ❌ NO - Only design assumptions tightened |
| Does catalog import change? | ❌ NO - Only clarification |
| Does BOM math change? | ❌ NO - Only explosion rules corrected |
| Does schema change? | ⚠️ MINIMAL - L1 table must support many-to-one L2 |
| Does explosion logic change? | ✅ YES - Critical correction |
| Does L2 import structure change? | ✅ YES - SKU-only approach |

---

**Document Status:** ✅ **REVIEW COMPLETE - AWAITING CONFIRMATION**

**Next Step:** Confirm the critical question, then proceed with document updates.

