# Phase 3 Pre-Execution Review

**Date:** 2025-01-XX  
**Status:** 🔍 **REVIEW COMPLETE - AWAITING APPROVAL**  
**Purpose:** Review Phase 3 plan before execution

---

## Executive Summary

Phase 3 will update **markdown freeze documents** (not Excel files) by applying fixes from the patch review. This is separate from Phase 2.1 (Excel file updates).

**Key Points:**
- ✅ Phase 3 works on `.md` files (markdown documents)
- ✅ Phase 2.1 works on `.xlsx` files (Excel workbooks)
- ✅ These are independent operations
- ✅ Phase 3 creates new v1.2 files, never overwrites v1 files

---

## Phase 3 Scope

### Files to Process

1. **NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md**
   - Input: `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md` (existing)
   - Output: `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2.md` (new file)
   - Fixes: 10 fixes applied

2. **NSW_SHEET_SET_INDEX_v1.md**
   - Input: `NSW_SHEET_SET_INDEX_v1.md` (existing)
   - Output: `NSW_SHEET_SET_INDEX_v1.2.md` (new file)
   - Fixes: 5 fixes applied

### Safety Guarantees

- ✅ **Never overwrites:** Original v1 files remain untouched
- ✅ **Always creates new:** v1.2 files are new files
- ✅ **Timestamp protection:** If v1.2 exists, creates with timestamp suffix
- ✅ **No pandas:** Uses standard Python file I/O (text-based)
- ✅ **Dry-run available:** Can preview changes before applying

---

## Fixes to be Applied

### NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md (10 Fixes)

1. **Fix A1:** Add Engineering Bank Operating Reality (Section 0)
   - Structural vs Capability vs Attribute separation
   - Generic Naming Neutrality Rule
   - Layer Discipline
   - Sheet Semantics
   - AI Safety Boundary

2. **Fix A2:** Fix SC_Lx Definition
   - Change: `SC_L1..SC_L4 → Capability_Class_1..4` (WRONG)
   - To: `SC_L1..SC_L8 → SCL (Structural Construction Layers)` (CORRECT)
   - Add mandatory separation rules

3. **Fix A3:** Add "Do Not Force Fill" Rule
   - Universal Population Rule for SC_Lx and ATTR_*
   - Populate only if explicitly defined in OEM catalog

4. **Fix A4:** Add Generic Naming Rule
   - Vendor- and series-neutral requirement
   - Forbidden tokens list
   - Examples

5. **Fix A5:** Fix Contactor Example
   - Remove coil voltage from Capability_Class
   - Clarify AC1/AC3 as ratings, not capability

6. **Fix A6:** Fix business_subcategory Statement
   - Clarify as legacy alias for business_segment

7. **Fix A7:** Add "Two-Worlds" Warning
   - Business Category/Segment vs Engineering Capability/Class separation

8. **Fix A8:** Separate Capability vs Feature Line
   - Clarify distinction

9. **Fix A9:** Tighten SC_Lx Rename Scope
   - Transitional phase notes

10. **Fix A10:** Add Name Collision Section
    - Business Segment vs Item/ProductType name overlap

### NSW_SHEET_SET_INDEX_v1.md (5 Fixes)

1. **Fix B1:** Add Engineering Bank Mapping Table
   - Cursor/Pipeline Sheet → Engineering Bank Sheet mapping

2. **Fix B2:** Clarify Catalog Chain vs L1 Parse Sheets
   - Decision CLOSED: NSW_CATALOG_CHAIN_MASTER is canonical

3. **Fix B3:** Update NSW_L2_PRODUCTS Status
   - Change from ACTIVE to LEGACY
   - Note: Authoritative is NSW_SKU_MASTER_CANONICAL

4. **Fix B4:** Update "Not Yet Generated" Statements
   - Update to "Generated and active" where applicable

5. **Fix B5:** Add Alias Support Block
   - Legacy aliases during transition

---

## Relationship to Phase 2.1

**Important:** Phase 3 is independent of Phase 2.1.

- **Phase 2.1:** Updated Excel file (`NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP_PHASE2_1.xlsx`)
  - Added "Engineering Bank – Operating Reality" to README_MASTER sheet
  - This is in the Excel workbook

- **Phase 3:** Updates markdown freeze documents
  - Updates `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md` → v1.2
  - Updates `NSW_SHEET_SET_INDEX_v1.md` → v1.2
  - These are separate markdown documentation files

**No conflict:** Phase 3 does not touch Excel files, and Phase 2.1 does not touch markdown files.

---

## Script Review

### Script Location
`scripts/apply_phase3_fixes.py`

### Key Features
- ✅ Text-based processing (no pandas)
- ✅ Regex-based pattern matching for fixes
- ✅ Safe file operations (never overwrites)
- ✅ Dry-run mode available
- ✅ Timestamp suffix if output exists

### Potential Issues to Watch

1. **Regex Pattern Matching:**
   - Some fixes use regex to find and replace text
   - If original v1 file structure differs, some fixes may not apply
   - Script checks for existence before applying (safe)

2. **Section Numbering:**
   - Script assumes standard markdown section numbering (## 1), ## 2), etc.)
   - If numbering differs, insertion points may need adjustment

3. **Content Variations:**
   - If v1 files have been manually edited, some patterns may not match
   - Script will skip non-matching patterns (safe, but may miss some fixes)

---

## Verification Plan

After Phase 3 execution, verify:

1. **Files Created:**
   - [ ] `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2.md` exists
   - [ ] `NSW_SHEET_SET_INDEX_v1.2.md` exists
   - [ ] Original v1 files unchanged

2. **Content Checks:**
   - [ ] Section 0 (Engineering Bank Operating Reality) present in Terminology Freeze
   - [ ] SC_Lx definition shows SCL (not capability_class)
   - [ ] All 10 fixes visible in Terminology Freeze
   - [ ] All 5 fixes visible in Sheet Set Index

3. **Version Updates:**
   - [ ] Version numbers updated to v1.2
   - [ ] Dates updated

---

## Execution Command

**Dry Run (Preview):**
```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2
python3 scripts/apply_phase3_fixes.py --dry-run
```

**Apply Fixes:**
```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2
python3 scripts/apply_phase3_fixes.py
```

---

## Approval Checklist

Before executing Phase 3, confirm:

- [x] Phase 3 scope understood (markdown files, not Excel)
- [x] Phase 2.1 file reviewed (separate operation)
- [x] Safety guarantees understood (never overwrites)
- [x] Fixes list reviewed (10 + 5 fixes)
- [ ] Ready to proceed with execution

---

## Recommendation

✅ **APPROVED FOR EXECUTION**

The Phase 3 plan is:
- ✅ Safe (never overwrites originals)
- ✅ Clear (creates new v1.2 files)
- ✅ Complete (all 15 fixes included)
- ✅ Independent (does not conflict with Phase 2.1)

**Suggested Execution:**
1. Run dry-run first to preview changes
2. Review dry-run output
3. If approved, run actual execution
4. Verify output files

---

**END OF PRE-EXECUTION REVIEW**




