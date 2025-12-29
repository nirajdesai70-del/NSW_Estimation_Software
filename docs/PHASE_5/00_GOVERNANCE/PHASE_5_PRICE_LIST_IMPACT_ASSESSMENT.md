# Phase 5 Impact Assessment - Price List Working Insights

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** REVIEW & DECISION REQUIRED  
**Purpose:** Comprehensive impact assessment of price list working insights on Phase 5 plan

---

## Executive Summary

**Key Insight:** Price list working revealed that Phase 5 must enforce strict L2/L1 separation:
- **L2 = SKU-pure (commercial only)** - One OEM catalog number = One L2 row
- **L1 = Engineering interpretation** - Multiple L1 rows can map to same L2 SKU
- **Explosion logic** moves from "SKU multiplication" → "L1 differentiation"

**Impact:** Phase 5 design assumptions must be tightened, but this **simplifies** Phase 5 once aligned correctly.

**Decision Required:** Confirm "Phase-5 explosion will allow multiple L1 rows to resolve to the same L2 SKU" before proceeding.

---

## 1. What Stays EXACTLY the Same in Phase 5

### 1.1 L2 (Catalog + Pricing) ✅ NO CHANGE

**Current Phase 5 Assumptions (Still Valid):**
- ✅ Price lives at SKU (L2)
- ✅ Price is versioned (price history)
- ✅ Price refresh is SKU-based
- ✅ Catalog import pipeline (Normalizer → Import API → SKU price history) is correct

**No Changes Required:**
- Catalog import pipeline structure
- Price history model
- SKU-based pricing model

---

### 1.2 BOM / Quotation Math ✅ NO CHANGE

**Current Phase 5 Assumptions (Still Valid):**
- ✅ Totals are derived from L2 rows
- ✅ L1 never owns price
- ✅ L1 → L2 explosion already exists in Phase 5 plan

**No Changes Required:**
- BOM costing logic
- Quotation calculation logic
- Price inheritance model

**Only Correction Needed:**
- Explosion rules (not the mechanism)

---

## 2. What MUST Change / Be Corrected in Phase 5

### 2.1 Wrong Assumption That Must Be Removed ❌

**❌ OLD (Incorrect):**
> "Different duty / rating = different SKU"

This assumption crept in during catalog work.

**✅ CORRECT (Locked Now):**
- Same SKU
- Multiple L1 interpretations
- Same price

**Impact:** Affects Phase 5 explosion logic, NOT catalog import.

---

### 2.2 Phase 5 Explosion Logic — Revised

**❌ OLD (Implicit, Wrong):**
```
Duty × Rating × Voltage → multiple L2 rows
```

**✅ CORRECT (Locked):**
```
Engineering interpretation → multiple L1 rows
Commercial reality → single L2 row
```

**New Phase 5 Explosion Flow:**
```
User intent (L0)
   ↓
Engineering specs (L1a, L1b, L1c…)
   ↓
SKU resolution (many L1 → same L2 allowed)
```

**Key Rule:** Multiple L1 rows can legally map to the same L2 SKU.

---

## 3. How This Impacts Each Phase 5 Component

### 3.1 Item Master (L0 / L1) ✅ POSITIVE SIMPLIFICATION

**Impact:**
- ✅ L1 becomes richer (more attributes)
- ✅ Fewer "fake SKUs" needed
- ✅ Engineers get clarity, not confusion

**Required Adjustment:**
- L1 validation rules must allow:
  - Same SKU mapping for multiple L1 rows
  - UI must not assume 1 L1 → 1 SKU

**Files to Update:**
- `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - Add L1 validation rules
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - Verify L1 table supports many-to-one L2 mapping

---

### 3.2 L1 → L2 Explosion Service 🔴 CRITICAL CHANGE

**What Changes:**
Explosion logic must be:

**✅ CORRECT:**
```php
FOR EACH L1:
   Resolve base SKU
   Resolve feature SKUs (if ADDON required)
```

**❌ NOT:**
```php
Multiply SKU per attribute
```

**Concrete Rule to Add:**
> **SKU reuse is allowed and expected.**

**This is the key Phase 5 correction.**

**Files to Create/Update:**
- `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/L1_L2_EXPLOSION_LOGIC.md` - NEW - Document explosion rules
- `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/POST_PHASE_5_IMPLEMENTATION_ROADMAP.md` - Update explosion service section

---

### 3.3 Feature / SubCategory Handling (SC-L1…SC-L4) ✅ CLEANER

**Impact:**
- ✅ SC-L1…SC-L4 only affect:
  - L1 intent
  - Feature lines
- ✅ They do NOT directly create SKUs

**SKU Impact Happens Only Via:**
- Feature policy (ADDON / INCLUDED / BUNDLED)

**Files to Verify:**
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_FINAL_RULES_v1.0.md` - Verify SC-L rules
- `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - Verify SubCategory model

---

### 3.4 Price Refresh & Re-rating ✅ DRAMATIC IMPROVEMENT

**Impact:**
- ✅ One SKU
- ✅ Price updated once
- ✅ All L1 interpretations automatically reflect new price
- ✅ No duplication, no reconciliation needed

**Example:**
```
LC1E0601 (one SKU)
  - Price updated: ₹2875 → ₹3000
  - All L1 interpretations (AC1, AC3) automatically get new price
```

**Files to Verify:**
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - Verify price history model supports this

---

## 4. What We Must Add to Phase 5 (Small but Critical)

### 4.1 Explicit L1–SKU Reuse Support 🔴 REQUIRED

**Add as Hard Rule:**
> **Multiple L1 lines may legally map to the same L2 SKU.**

**Files to Create/Update:**
- `docs/PHASE_5/03_DATA_DICTIONARY/VALIDATION_GUARDRAILS_G1_G7.md` - Add G8: L1-SKU reuse rule
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md` - Reference this rule

---

### 4.2 Engineer Validation Gate ✅ ALIGNED

**Engineers Validate:**
- ✅ Attributes
- ✅ Duty interpretation
- ✅ Ratings

**Engineers Do NOT Touch:**
- ❌ SKU
- ❌ Price

**This fits perfectly with ADR-005 firewall.**

**Files to Verify:**
- `docs/PHASE_5/00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` - Verify engineer boundaries

---

## 5. What Does NOT Need Rework ✅

| Area | Status |
|------|--------|
| Catalog pipeline | ✅ No rework |
| Price history | ✅ No rework |
| SKU import | ✅ No rework |
| BOM totals | ✅ No rework |
| Phase-4 legacy | ✅ Isolated |

**Only Phase 5 logic documents + explosion rules need alignment — not code rewrite.**

---

## 6. Import/Export Structure Changes

### 6.1 Final Import Structure — What CHANGES 🔴

**❌ OLD (Implicit, Incorrect):**
```
Price List → exploded rows
(each duty / rating / pole treated as separate SKU)
```

**✅ NEW (Correct, Final):**
```
Price list import creates L2-only records.
L1 and L0 are derived, not imported.
```

**Import Contract:**
```
OEM Price List
   ↓
L2 MASTER (SKU-only, commercial truth)
   ↓
System derives L1/L0 views dynamically
```

**Key Change:**
👉 We STOP trying to encode engineering meaning into the price list.

**Final Rule (LOCK THIS):**
> **If a field is not mandatory for L2, it must not be imported.**

---

### 6.2 Final L2 (Catalog) Structure — LOCKED ✅

**L2 MASTER (SKU table) — FINAL FIELDS:**

| Field | Required | Meaning |
|-------|----------|---------|
| Make | ✅ | Schneider |
| OEM_Catalog_No (SKU) | ✅ | LC1E0601, LC1D25*, LP1K0601 |
| Series | ✅ | Easy TeSys / TeSys Deca / TeSys K |
| Item_ProductType | ✅ | Contactor / Control Relay / MPCB |
| SubCategory | ✅ | Power Contactor / Control Relay / MPCB |
| Base_Description | Optional | Human readable |
| Price | ✅ | Numeric |
| Currency | ✅ | INR |
| Voltage_Class | Optional | AC / DC (not voltage value) |
| PriceListRef | ✅ | Pricelist name |
| EffectiveFrom | ✅ | Date |

**❌ NOT ALLOWED in L2 import anymore:**
- Duty (AC1 / AC3)
- Rating interpretation (20A vs 6A)
- Poles as multipliers
- NO/NC meaning
- Frame size as multiplier
- Feature logic

**Those are engineering interpretations, not commercial truth.**

**Files to Create:**
- `docs/PHASE_5/CANONICAL/L2_IMPORT_STRUCTURE_v1.3.1.md` - NEW - Final L2 import spec
- `docs/PHASE_5/CANONICAL/NSW_MASTER_v1.3.1_SKU_FIRST_TEMPLATE.xlsx` - NEW - Excel template

---

### 6.3 Where Engineering Meaning Goes (AC1 / AC3 / Poles / Ratings) ✅

**Example (LC1E0601):**

**Single L2 row:**
```
SKU = LC1E0601
Price = ₹2875
```

**System can derive MULTIPLE L1 rows:**
```
L1 Line | Duty | AC Rating | Poles | Voltage
--------|------|-----------|-------|--------
L1-A    | AC1  | 20 A      | 3P    | 220V
L1-B    | AC3  | 6 A       | 3P    | 220V
L1-C    | AC1  | 20 A      | 3P    | 415V
L1-D    | AC3  | 6 A       | 3P    | 415V
```

👉 All map to the same SKU (LC1E0601)  
👉 Price reused correctly

**Files to Create:**
- `docs/PHASE_5/CANONICAL/L1_DERIVATION_RULES.md` - NEW - How L1 is derived from L2

---

### 6.4 How SC-L1 → SC-L4 Now Behave ✅

**❌ OLD Misunderstanding:**
Using SC-L1…SC-L4 as multipliers.

**✅ CORRECT Meaning:**

| Layer | What it controls | Multiplies SKU? |
|-------|------------------|-----------------|
| SC-L1 Construction | Frame / Form | ❌ No |
| SC-L2 Operation | Poles / Actuation | ❌ No |
| SC-L3 Feature Class | AC1 / AC3 / Breaking Capacity | ❌ No |
| SC-L4 Accessory Class | Aux / Coil / OLR / Interlock | ❌ No (unless ADDON SKU) |

👉 Only feature policy may create extra SKUs, not attributes.

**Files to Verify:**
- `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - Verify SubCategory model

---

## 7. Excel File Structure Changes

### 7.1 What Changes ✅

**❌ OLD (Don't Do This):**
One row per: `SKU × Duty × Voltage × Poles × Rating`

**✅ NEW FINAL Excel Strategy (LOCK):**

**Sheet 1 — L2_SKU_MASTER (Importable)**
- One row = one OEM catalog number
- Columns: Make, Series, Item, SubCategory, SKU, Price, Currency, PriceList

**Sheet 2 — L1_DERIVATION_RULES (Engineering, not import)**
- System knowledge, not price data
- Drives auto-L1 creation
- Can be edited by engineering

**Sheet 3 — FEATURE_POLICY (already in fundamentals)**
- Controls when accessories create SKUs

**Files to Create:**
- `docs/PHASE_5/CANONICAL/NSW_MASTER_v1.3.1_SKU_FIRST_TEMPLATE.xlsx` - NEW - Excel template with all sheets

---

## 8. Database Schema Impact

### 8.1 Schema Changes Required ✅ MINIMAL

**Current Schema Status:**
- ✅ `catalog_skus` table (L2 SKUs) - Already exists conceptually
- ✅ `sku_prices` table (L2 price history) - Already exists conceptually
- ✅ `l1_intent_lines` table - Needs to support many-to-one L2 mapping

**Required Changes:**
1. **L1 Table:** Ensure FK to L2 allows many-to-one (multiple L1 → same L2)
2. **L1 Validation:** Remove any constraint that enforces 1:1 L1:L2 mapping
3. **Explosion Service:** Document that same L2 can be reused

**Files to Update:**
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - Verify L1 table structure
- Add explicit note: "L1 → L2 is many-to-one relationship"

---

### 8.2 What We Explicitly Do NOT Store in L2 ❌

**Do NOT store in L2:**
- ❌ AC1/AC3 rating rows
- ❌ Duty-wise current rows
- ❌ Frame as multiplier
- ❌ Accessory compatibility

**Those live in:**
- ✅ L1 rules tables or policy sheets

**Files to Update:**
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - Add explicit "NOT stored in L2" section

---

## 9. API Contract Changes

### 9.1 New Endpoints Required 🔴

**Required Endpoints:**

1. **POST /api/v1/catalog/l2/skus/import**
   - Imports Sheet A (L2_SKU_MASTER)
   - Upsert by (Make + OEM_Catalog_No)
   - No price writes here

2. **POST /api/v1/catalog/l2/prices/import**
   - Imports Sheet B (L2_PRICE_HISTORY)
   - Creates/uses PriceListRef container
   - Inserts append-only price rows

3. **POST /api/v1/catalog/l1/derive/from-l2** (optional but recommended)
   - Uses Sheets C–E to create L1 BASE/FEATURE lines from L2

**Files to Create:**
- `docs/PHASE_5/CANONICAL/openapi_l2_first.yaml` - NEW - OpenAPI contract

---

## 10. Phase 5 Execution Plan Updates

### 10.1 Documents Requiring Updates 📋

**High Priority (Must Update):**

1. **Explosion Logic Documentation**
   - `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/L1_L2_EXPLOSION_LOGIC.md` - CREATE NEW
   - Document: Multiple L1 → Same L2 is allowed and expected

2. **Data Dictionary**
   - `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - UPDATE
   - Add L1 validation rules for SKU reuse
   - Clarify L1 → L2 is many-to-one

3. **Schema Canon**
   - `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - UPDATE
   - Verify L1 table supports many-to-one L2 mapping
   - Add explicit "NOT stored in L2" section

4. **Validation Guardrails**
   - `docs/PHASE_5/03_DATA_DICTIONARY/VALIDATION_GUARDRAILS_G1_G7.md` - UPDATE
   - Add G8: L1-SKU reuse rule

**Medium Priority (Should Update):**

5. **Post-Phase 5 Implementation Roadmap**
   - `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/POST_PHASE_5_IMPLEMENTATION_ROADMAP.md` - UPDATE
   - Update explosion service section
   - Add L2-first import workflow

6. **Schneider Rules**
   - `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md` - VERIFY
   - Already aligned, but reference in Phase 5 docs

**Low Priority (Nice to Have):**

7. **Phase 5 Execution Summary**
   - `docs/PHASE_5/00_GOVERNANCE/PHASE_5_EXECUTION_SUMMARY.md` - UPDATE
   - Add note about L2-first approach

---

## 11. Implementation Timeline

### 11.1 When Changes Are Needed ⏰

**Before Phase 5 Execution:**
- ✅ Update Phase 5 design documents (Steps 1-2)
- ✅ Create L2 import structure documentation
- ✅ Create Excel template
- ✅ Create OpenAPI contract

**During Phase 5 Execution:**
- ✅ Follow updated explosion logic
- ✅ Use L2-first import approach
- ✅ Validate L1 → L2 many-to-one mapping

**After Phase 5 (Implementation Phase):**
- ✅ Implement L2 import endpoints
- ✅ Implement L1 derivation service
- ✅ Implement explosion service with SKU reuse

---

## 12. Risk Assessment

### 12.1 Risks Removed ✅

| Risk | Status |
|------|--------|
| Over-exploded SKUs | ✅ Removed |
| Pricing inconsistency | ✅ Removed |
| Frame/pole misuse as multipliers | ✅ Removed |

---

### 12.2 New Risks (Low) ⚠️

| Risk | Impact | Mitigation |
|------|--------|------------|
| Confusion about L1 → L2 many-to-one | LOW | Clear documentation, validation rules |
| Engineers creating duplicate L1s | LOW | UI validation, clear guidance |

---

## 13. 5R Summary — Phase 5 Impact (Freeze-Ready)

### RESULTS ✅
- Phase-5 becomes simpler and more robust
- Clear separation: engineering meaning vs commercial SKU
- No SKU duplication

### RISKS (Removed) ✅
- Over-exploded SKUs
- Pricing inconsistency
- Frame/pole misuse as multipliers

### RULES (Locked for Phase-5) 🔒
1. L2 = commercial truth only
2. L1 = engineering interpretation
3. Same SKU may serve many L1s
4. Duty/rating never creates SKU unless OEM changes catalog number
5. Accessories resolve via feature policy, not multiplication

### ROADMAP 📋
1. Update Phase-5 explosion spec
2. Update L1 validation rules
3. Proceed with LC1D → LC1K → MPCB confidently
4. Resume full Phase-5 execution

### REFERENCES 📚
- NSW Master Fundamentals v2.0
- Feature policy doctrine
- L1/L2 inheritance model
- ADR-005 governance firewall
- Schneider L2/L1 Differentiation Clarification v1.0

---

## 14. Final Confirmation Question (Critical)

**Before we proceed, confirm one line:**

> **"Phase-5 explosion will allow multiple L1 rows to resolve to the same L2 SKU."**

**Once you confirm this, we will:**
- ✅ Patch the Phase-5 execution spec
- ✅ Give you a diff-style checklist of exactly what to update (no guesswork)
- ✅ Then proceed cleanly

---

## 15. Action Items Checklist

### Immediate (Before Phase 5 Execution)

- [ ] **Confirm:** "Phase-5 explosion will allow multiple L1 rows to resolve to the same L2 SKU"
- [ ] **Create:** `docs/PHASE_5/CANONICAL/L2_IMPORT_STRUCTURE_v1.3.1.md`
- [ ] **Create:** `docs/PHASE_5/CANONICAL/NSW_MASTER_v1.3.1_SKU_FIRST_TEMPLATE.xlsx`
- [ ] **Create:** `docs/PHASE_5/CANONICAL/openapi_l2_first.yaml`
- [ ] **Create:** `docs/PHASE_5/06_IMPLEMENTATION_REFERENCE/L1_L2_EXPLOSION_LOGIC.md`
- [ ] **Update:** `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - Add L1 validation rules
- [ ] **Update:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - Verify L1 table structure
- [ ] **Update:** `docs/PHASE_5/03_DATA_DICTIONARY/VALIDATION_GUARDRAILS_G1_G7.md` - Add G8 rule

### During Phase 5 Execution

- [ ] Follow updated explosion logic
- [ ] Use L2-first import approach
- [ ] Validate L1 → L2 many-to-one mapping

### After Phase 5 (Implementation)

- [ ] Implement L2 import endpoints
- [ ] Implement L1 derivation service
- [ ] Implement explosion service with SKU reuse

---

**Document Status:** ✅ **REVIEW COMPLETE - AWAITING CONFIRMATION**

**Next Step:** Confirm the critical question in Section 14, then proceed with document updates.

