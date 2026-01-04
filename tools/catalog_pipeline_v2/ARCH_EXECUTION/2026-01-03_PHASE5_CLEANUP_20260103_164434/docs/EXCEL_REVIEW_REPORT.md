# Excel File Review Report - Item Master Analysis

**Date:** 2025-01-XX  
**File:** `item_master_020126.xlsx`  
**Status:** ✅ ANALYSIS COMPLETE  
**Comparison With:** PATCH_REVIEW_REPORT_v1.2.md

---

## Executive Summary

The Excel file contains **39 sheets** with comprehensive documentation and data. Analysis reveals:

- ✅ **GOOD:** SC_Lx is correctly used as Structural Construction Layers in practice
- ✅ **GOOD:** Generic naming appears vendor/series neutral
- ✅ **GOOD:** business_segment is used (aligned with patch)
- 🔴 **CRITICAL CONFLICT:** TERMINOLOGY_ALIASES sheet contradicts actual usage
- 🟡 **GAPS:** Missing explicit "Engineering Bank Operating Reality" section

---

## 1. Sheet Inventory Summary

### Sheet Categories

| Category | Count | Examples |
|----------|-------|----------|
| **DATA** | 12 | NSW_ITEM_MASTER_ENGINEER_VIEW, ITEM_GIGA_SERIES_WORK, ACCESSORIES_MASTER |
| **README** | 10 | README_MASTER, README_ITEM_GOVERNANCE, README_FUNDAMENTAL_PROCESS |
| **PROCESS** | 5 | PAGE_WORKFLOW_SOP, INTERP_LC1E_SUMMARY, INTERP_LC1D_SUMMARY |
| **GOVERNANCE** | 12 | DECISION_REGISTER, GUARDRAILS_DO_NOT, TERMINOLOGY_ALIASES, QC_LOG |

### Key Data Sheets

1. **NSW_ITEM_MASTER_ENGINEER_VIEW** (497 rows, 103 columns)
   - Main item master data
   - Contains SC_L1 through SC_L8 columns
   - Contains capability_codes column (separate from SC_Lx) ✅

2. **ITEM_GIGA_SERIES_WORK** (40 rows, 103 columns)
3. **ITEM_K_SERIES_WORK** (83 rows, 103 columns)
4. **ACCESSORIES_MASTER** (158 rows, 43 columns)

---

## 2. Critical Findings

### 🔴 Finding 1: TERMINOLOGY_ALIASES Contradiction (CRITICAL)

**Location:** `TERMINOLOGY_ALIASES` sheet, Row 1

**Current Content:**
```
term_used_in_code: SC_L1..SC_L4
canonical_term: capability_class_1..4
meaning: Engineering capability grouping axes
```

**Problem:**
This contradicts:
1. **SC_DEFINITION sheet** which shows:
   - SC_L1 = FRAME_SIZE (structural)
   - SC_L2 = MOUNTING_TYPE (structural)

2. **DECISION_REGISTER (DR-003)** which states:
   - "SC_L1..SC_L8 are construction/form only"

3. **Actual data usage** where SC_L1 contains values like "FRAME-1" (clearly structural)

**Impact:** This creates confusion and contradicts patch requirements that SC_Lx = SCL (Structural Construction Layers), not Capability.

**Resolution Required:**
- Update TERMINOLOGY_ALIASES to reflect:
  - SC_L1..SC_L8 = Structural Construction Layers (SCL)
  - capability_class_1..4 = separate concept (if needed)
  - Remove incorrect mapping

---

### ✅ Finding 2: SC_DEFINITION Correctly Defines SC_Lx as Structural

**Location:** `SC_DEFINITION` sheet

**Content:**
- SC_L1 = FRAME_SIZE (Frame size bucket)
- SC_L2 = MOUNTING_TYPE (Mounting style)

**Status:** ✅ **CORRECT** - Aligns with patch requirements that SC_Lx = SCL

---

### ✅ Finding 3: DECISION_REGISTER Confirms SC_Lx as Construction

**Location:** `DECISION_REGISTER` sheet, Decision DR-003

**Content:**
- Topic: SC semantics
- Decision: "SC_L1..SC_L8 are construction/form only and single-choice per SC per row."

**Status:** ✅ **CORRECT** - Aligns with patch requirements

---

### ✅ Finding 4: Actual Data Usage is Correct

**Location:** `NSW_ITEM_MASTER_ENGINEER_VIEW` sheet

**Observation:**
- SC_L1 contains values like "FRAME-1" (structural)
- SC_L2, SC_L3, SC_L4 are mostly empty (as expected for optional structural elements)
- capability_codes column exists separately (good separation)

**Status:** ✅ **CORRECT** - Data usage aligns with structural definition

---

### ✅ Finding 5: Generic Naming Appears Correct

**Location:** `NSW_ITEM_MASTER_ENGINEER_VIEW` sheet

**Sample Values:**
- "Power Contactor – 3P | AC1 20A | 2.2kW/3HP @415V | Aux 0NO+1NC"
- No vendor names (Schneider, ABB, Siemens) found
- No series names (LC1, GZ1, NSX, NW) found

**Status:** ✅ **GOOD** - Generic names are vendor/series neutral

---

### ✅ Finding 6: business_segment Usage

**Location:** All data sheets

**Observation:**
- Column name: `business_segment` (not business_subcategory)
- Aligned with patch requirement

**Status:** ✅ **CORRECT** - Uses canonical term

---

## 3. Comparison with Patch Requirements

### Patch Requirement: SC_Lx = SCL (Structural Construction Layers)

| Source | Status | Alignment |
|--------|--------|-----------|
| SC_DEFINITION sheet | ✅ Correct | Defines SC_L1=FRAME_SIZE, SC_L2=MOUNTING_TYPE |
| DECISION_REGISTER | ✅ Correct | States "construction/form only" |
| Actual data usage | ✅ Correct | SC_L1 = "FRAME-1" (structural) |
| TERMINOLOGY_ALIASES | 🔴 **WRONG** | Says SC_Lx = capability_class (contradicts others) |

**Verdict:** 3 out of 4 sources are correct. TERMINOLOGY_ALIASES needs correction.

---

### Patch Requirement: Generic Naming Neutrality

| Check | Status | Finding |
|------|--------|---------|
| Vendor names in generic names | ✅ Pass | No violations found |
| Series names in generic names | ✅ Pass | No violations found |
| Generic naming rule documented | ⚠️ Partial | Not explicitly in README sheets |

**Verdict:** Practice is correct, but explicit rule should be added to README.

---

### Patch Requirement: business_segment (not business_subcategory)

| Check | Status | Finding |
|------|--------|---------|
| Column name in data | ✅ Correct | Uses `business_segment` |
| TERMINOLOGY_ALIASES | ✅ Correct | Lists business_subcategory as legacy alias |

**Verdict:** ✅ Fully aligned

---

## 4. Gaps Identified

### Gap 1: Missing "Engineering Bank Operating Reality" Section

**Patch Requirement:** Add Section 0 to freeze document with authoritative operating reality.

**Excel Status:** No equivalent section found in README sheets.

**Impact:** Medium - Excel has governance but lacks explicit "operating reality" override section.

---

### Gap 2: TERMINOLOGY_ALIASES Contradiction

**Issue:** TERMINOLOGY_ALIASES incorrectly maps SC_Lx to capability_class.

**Impact:** High - Creates confusion and contradicts actual usage.

**Fix Required:** Update TERMINOLOGY_ALIASES sheet to reflect SC_Lx = SCL.

---

### Gap 3: Generic Naming Rule Not Explicitly Documented

**Issue:** Generic naming appears correct in practice, but no explicit rule found in README sheets.

**Impact:** Low - Practice is correct, but documentation should be explicit.

**Fix Required:** Add explicit rule to README_ITEM_GOVERNANCE or README_MASTER.

---

### Gap 4: Missing "Do Not Force Fill" Rule

**Patch Requirement:** Universal population rule - only populate SC_Lx if explicitly defined in catalog.

**Excel Status:** Not explicitly documented in README sheets.

**Impact:** Medium - Prevents over-population but should be explicit.

---

## 5. Recommendations

### Priority 1: Fix TERMINOLOGY_ALIASES (CRITICAL)

**Action:**
1. Update TERMINOLOGY_ALIASES sheet, Row 1:
   - Change: `SC_L1..SC_L4` → `capability_class_1..4`
   - To: `SC_L1..SC_L8` → `Structural Construction Layers (SCL)`
   - Meaning: "Physical construction elements (frame, mounting, terminals, etc.)"
   - Notes: "Do not confuse with capability. Capability is separate concept using capability_codes."

2. Add new row if capability_class is needed:
   - `capability_class_1..4` → "Engineering capability grouping axes (separate from SCL)"

**Rationale:** Aligns with SC_DEFINITION, DECISION_REGISTER, and actual data usage.

---

### Priority 2: Add Generic Naming Rule to README

**Action:**
Add to README_ITEM_GOVERNANCE or README_MASTER:

```
Generic Naming Rule (MANDATORY):
- Generic item names and descriptions must be vendor- and series-neutral.
- Do NOT include: OEM name (Schneider, ABB, etc.), Series (LC1E, GZ1E, NSX, NW)
- Make/Series are allowed only at L2 (SKU level).
```

**Rationale:** Practice is correct, but explicit rule prevents future violations.

---

### Priority 3: Add "Do Not Force Fill" Rule

**Action:**
Add to README_ITEM_GOVERNANCE:

```
Universal Population Rule (Applies to ALL SC_Lx and ATTR_*):
- Populate SC_Lx or ATTR_* fields only if explicitly defined in the OEM catalog.
- Do NOT substitute series, family, or marketing names.
- Do NOT guess or infer.
- Leave blank if not explicitly stated.
```

**Rationale:** Prevents over-population and maintains data quality.

---

### Priority 4: Add "Engineering Bank Operating Reality" Section

**Action:**
Add new section to README_MASTER or create new README_OPERATING_REALITY sheet:

```
Engineering Bank – Operating Reality (Authoritative)

This section overrides ambiguous interpretations elsewhere.

A. Structural vs Capability vs Attribute (Final)
  1. SC_Lx fields represent Structural / Construction Layers (SCL) only.
  2. Capability represents optional inclusion/exclusion logic.
  3. Attributes represent numeric or KVU facts.

B. Generic Naming (Mandatory)
  - Generic names must be vendor- and series-neutral.

C. Layer Discipline (Hard Boundary)
  - Layer-1: Records facts only.
  - Layer-2: Applies rules, capability logic, dependency checks.
```

**Rationale:** Provides authoritative override for ambiguous interpretations.

---

## 6. Alignment Summary

### ✅ What's Aligned

1. **SC_Lx Usage:** Correctly used as Structural Construction Layers in:
   - SC_DEFINITION sheet
   - DECISION_REGISTER
   - Actual data (SC_L1 = FRAME-1, etc.)

2. **business_segment:** Correctly used (not business_subcategory)

3. **Generic Naming:** Practice is correct (no vendor/series in generic names)

4. **Capability Separation:** capability_codes column exists separately from SC_Lx

### 🔴 What Needs Fixing

1. **TERMINOLOGY_ALIASES:** Incorrectly maps SC_Lx to capability_class
2. **Missing Explicit Rules:** Generic naming and "Do Not Force Fill" rules not documented
3. **Missing Operating Reality Section:** No authoritative override section

### 🟡 What's Partially Aligned

1. **Documentation:** Good governance structure but needs explicit rules added
2. **Terminology:** Mostly correct but TERMINOLOGY_ALIASES needs update

---

## 7. Updated Gap Document Recommendations

Based on this analysis, the following should be added to PATCH_REVIEW_REPORT_v1.2.md:

### New Finding: Excel File TERMINOLOGY_ALIASES Contradiction

**Location:** Excel file `item_master_020126.xlsx`, TERMINOLOGY_ALIASES sheet

**Issue:** TERMINOLOGY_ALIASES incorrectly states SC_L1..SC_L4 = capability_class_1..4

**Evidence:**
- SC_DEFINITION shows SC_L1 = FRAME_SIZE (structural)
- DECISION_REGISTER states SC_Lx = "construction/form only"
- Actual data shows SC_L1 = "FRAME-1" (structural)

**Resolution:**
- Update TERMINOLOGY_ALIASES in Excel file
- Align with SC_DEFINITION and DECISION_REGISTER
- Update freeze documents to reference Excel file correction

---

## 8. Conclusion

The Excel file demonstrates **correct practice** in:
- Using SC_Lx as Structural Construction Layers
- Using business_segment (not business_subcategory)
- Maintaining vendor/series neutral generic names
- Separating capability from structure

However, there is a **critical documentation contradiction** in TERMINOLOGY_ALIASES that must be fixed to prevent confusion.

**Overall Assessment:** ✅ **GOOD PRACTICE, NEEDS DOCUMENTATION FIX**

---

**Next Steps:**
1. Fix TERMINOLOGY_ALIASES sheet in Excel file
2. Add explicit rules to README sheets
3. Update PATCH_REVIEW_REPORT_v1.2.md with Excel findings
4. Create revised gap document with consolidated recommendations

---

**END OF REPORT**

