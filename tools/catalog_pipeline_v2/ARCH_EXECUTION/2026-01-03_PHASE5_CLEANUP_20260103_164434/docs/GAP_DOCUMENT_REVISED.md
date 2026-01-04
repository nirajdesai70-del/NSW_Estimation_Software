# Revised Gap Document - Consolidated Findings

**Date:** 2025-01-XX  
**Status:** FINAL - READY FOR EXECUTION  
**Based On:**
- PATCH_REVIEW_REPORT_v1.2.md
- EXCEL_REVIEW_REPORT.md
- PATCH_REVIEW_REPORT_v1.2_REVISED.md

---

## Executive Summary

This document consolidates all findings from:
1. Patch requirements analysis
2. Excel file review (`item_master_020126.xlsx`)
3. Cross-comparison of documents and practice

**Key Finding:** Excel file demonstrates **correct practice**, but **documentation contradictions** exist that must be resolved.

---

## Critical Gaps (Must Fix)

### Gap 1: TERMINOLOGY_ALIASES Contradiction (HIGHEST PRIORITY)

**Location:** Excel file `item_master_020126.xlsx`, TERMINOLOGY_ALIASES sheet

**Issue:**
- TERMINOLOGY_ALIASES says: SC_L1..SC_L4 → capability_class_1..4
- But SC_DEFINITION shows: SC_L1 = FRAME_SIZE (structural)
- DECISION_REGISTER states: SC_Lx = "construction/form only"
- Actual data shows: SC_L1 = "FRAME-1" (structural)

**Impact:** Creates confusion and contradicts correct practice

**Fix Required:**
Update TERMINOLOGY_ALIASES sheet:
```
SC_L1..SC_L8 → Structural Construction Layers (SCL)
meaning: Physical construction elements (frame, mounting, terminals, zones, etc.)
```

**Priority:** 🔴 CRITICAL

---

### Gap 2: Freeze Document SC_Lx Definition

**Location:** NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md, Section 2, World C

**Issue:**
- Current: SC_L1…SC_L4 → Capability_Class_1…4 (WRONG)
- Required: SC_Lx = Structural Construction Layers (SCL) ONLY

**Fix Required:**
- Complete rewrite of SC_Lx definition section
- Add explicit "Structural vs Capability Separation" section
- Remove incorrect capability mapping

**Priority:** 🔴 CRITICAL

---

### Gap 3: Script Auto-Mapping

**Location:** migrate_sku_price_pack.py, Lines 44-58

**Issue:**
- Script auto-maps SC_Lx → capability_class_x
- This is incorrect per patch requirements

**Fix Required:**
- Remove auto-mapping
- Preserve SC_Lx as SCL
- Only rename if source explicitly indicates capability

**Priority:** 🔴 CRITICAL

---

### Gap 4: Contactor Example Contradiction

**Location:** NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md, Section 6

**Issue:**
- Example shows: Capability_Class_2: AC Coil, Capability_Class_3: AC1/AC3
- But Option B says: Coil voltage is L2-only (SKU-defining)

**Fix Required:**
- Rewrite Contactor example
- Remove coil from Capability_Class
- Clarify AC1/AC3 as ratings

**Priority:** 🔴 CRITICAL

---

## Important Gaps (Should Fix)

### Gap 5: Missing Generic Naming Rule

**Locations:**
- Freeze document (missing)
- Excel README sheets (missing)

**Fix Required:**
Add explicit rule:
```
Generic names must be vendor- and series-neutral.
Do NOT include: OEM name, Series, Family
Make/Series allowed only at L2 (SKU level).
```

**Priority:** 🟡 IMPORTANT

---

### Gap 6: Missing "Do Not Force Fill" Rule

**Locations:**
- Freeze document (missing)
- Excel README sheets (missing)

**Fix Required:**
Add rule:
```
Populate SC_Lx or ATTR_* only if explicitly defined in OEM catalog.
Do NOT substitute series, family, or marketing names.
Leave blank if not explicitly stated.
```

**Priority:** 🟡 IMPORTANT

---

### Gap 7: Missing Engineering Bank Operating Reality Section

**Location:** Freeze document (missing Section 0)

**Fix Required:**
Add authoritative section covering:
- Structural vs Capability vs Attribute separation
- Generic naming neutrality
- Layer discipline
- Sheet semantics

**Priority:** 🟡 IMPORTANT

---

## Minor Gaps (Nice to Have)

### Gap 8: business_subcategory Statement Clarification

**Location:** Freeze document, Section 2, World A

**Fix Required:**
Change from "aligned!" to "legacy alias during transition"

**Priority:** 🟢 MINOR

---

### Gap 9: Missing "Two-Worlds" Warning

**Location:** Freeze document (missing)

**Fix Required:**
Add warning block about Business vs Engineering separation

**Priority:** 🟢 MINOR

---

## Excel File: What's Already Correct

✅ **SC_Lx Usage:** Correctly used as Structural Construction Layers
✅ **business_segment:** Correctly used
✅ **Generic Naming:** Vendor/series neutral (practice is correct)
✅ **Capability Separation:** capability_codes column exists separately

**Note:** Excel file practice is correct. Only TERMINOLOGY_ALIASES documentation needs fix.

---

## Consolidated Fix List

### Excel File Fixes

1. 🔴 Fix TERMINOLOGY_ALIASES sheet (CRITICAL)
2. 🟡 Add Generic Naming Rule to README_ITEM_GOVERNANCE
3. 🟡 Add "Do Not Force Fill" Rule to README_ITEM_GOVERNANCE

### Freeze Document Fixes

1. 🔴 Add Engineering Bank Operating Reality (Section 0)
2. 🔴 Fix SC_Lx definition (Section 2, World C)
3. 🔴 Fix Contactor example (Section 6)
4. 🟡 Add Generic Naming Rule
5. 🟡 Add "Do Not Force Fill" Rule
6. 🟡 Add "Two-Worlds" Warning
7. 🟢 Fix business_subcategory statement
8. 🟢 Add other clarifications

### Script Fixes

1. 🔴 Remove SC_Lx → capability_class_x auto-mapping
2. 🟡 Add Generic Naming validation

---

## Execution Priority

### Phase 1: Critical (Do First)
- Fix Excel TERMINOLOGY_ALIASES
- Fix freeze doc SC_Lx definition
- Remove script auto-mapping
- Fix Contactor example
- Add Operating Reality section

### Phase 2: Important (Do Next)
- Add Generic Naming Rule (both Excel and freeze doc)
- Add "Do Not Force Fill" Rule (both Excel and freeze doc)
- Add Generic Naming validation to script
- Add Engineering Bank Mapping

### Phase 3: Clarifications (Do Last)
- All remaining clarifications
- Update sheet statuses
- Add alias support blocks

---

## Success Criteria

All gaps are resolved when:

- [ ] Excel TERMINOLOGY_ALIASES correctly maps SC_Lx to SCL
- [ ] Freeze document SC_Lx definition is correct
- [ ] Script does not auto-map SC_Lx
- [ ] Contactor example aligns with Option B
- [ ] Generic naming rules are explicit (Excel + freeze doc)
- [ ] "Do Not Force Fill" rules are explicit (Excel + freeze doc)
- [ ] Operating Reality section exists
- [ ] No contradictions between Excel, freeze docs, and scripts

---

## Conclusion

The analysis reveals that **correct practice exists** (demonstrated in Excel file), but **documentation contradictions** must be resolved. Once fixed, the system will be fully aligned.

**Overall Status:** ✅ **PRACTICE CORRECT, DOCUMENTATION NEEDS FIX**

**Estimated Effort:** 
- Critical fixes: 2-3 hours
- Important fixes: 2-3 hours
- Clarifications: 1-2 hours
- **Total: 5-8 hours**

---

**END OF GAP DOCUMENT**

