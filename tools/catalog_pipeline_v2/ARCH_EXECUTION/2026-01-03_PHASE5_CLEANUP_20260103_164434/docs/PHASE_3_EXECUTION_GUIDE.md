# Phase 3: Update Freeze Documents - Execution Guide

**Date:** 2025-01-XX  
**Status:** 🟡 READY FOR EXECUTION  
**Objective:** Apply fixes to freeze documents and create v1.2 versions

---

## Overview

Phase 3 updates the freeze documents by applying fixes from the patch review:
1. **NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md** → Apply 10 fixes → Create v1.2
2. **NSW_SHEET_SET_INDEX_v1.md** → Apply 5 fixes → Create v1.2

**Safety Guarantees:**
- ✅ Always creates NEW files (v1.2), never overwrites originals (v1)
- ✅ Uses text-based processing (no pandas)
- ✅ If output file exists, creates with timestamp suffix

---

## Prerequisites

### Required Files

1. **NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md**
   - Must exist in input directory
   - Will NOT be modified

2. **NSW_SHEET_SET_INDEX_v1.md**
   - Must exist in input directory
   - Will NOT be modified

### Required Tools

- Python 3.7+
- No external dependencies (uses only standard library)

---

## Execution Method: Automated Script

**Script:** `scripts/apply_phase3_fixes.py`

### Basic Usage

```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2

python3 scripts/apply_phase3_fixes.py
```

This will:
- Read v1 files from current directory
- Apply all fixes
- Create v1.2 files in current directory

### Custom Input/Output Directories

```bash
python3 scripts/apply_phase3_fixes.py \
  --input-dir "." \
  --output-dir "output/phase3"
```

### Dry Run (Preview Changes)

```bash
python3 scripts/apply_phase3_fixes.py --dry-run
```

This shows what would be changed without creating files.

---

## Fixes Applied

### NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md (10 Fixes)

1. **Fix A1:** Add Engineering Bank Operating Reality (Section 0)
   - Structural vs Capability vs Attribute separation
   - Generic Naming Neutrality Rule
   - Layer Discipline
   - Sheet Semantics
   - AI Safety Boundary

2. **Fix A2:** Fix SC_Lx Definition
   - Change from: `SC_L1..SC_L4 → Capability_Class_1..4`
   - Change to: `SC_L1..SC_L8 → SCL (Structural Construction Layers)`
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
   - Update capability examples

6. **Fix A6:** Fix business_subcategory Statement
   - Clarify as legacy alias for business_segment

7. **Fix A7:** Add "Two-Worlds" Warning
   - Business Category/Segment vs Engineering Capability/Class separation
   - Forbidden mappings

8. **Fix A8:** Separate Capability vs Feature Line
   - Clarify distinction
   - Reference Doctrine sections

9. **Fix A9:** Tighten SC_Lx Rename Scope
   - Transitional phase notes
   - Implementation safety

10. **Fix A10:** Add Name Collision Section
    - Business Segment vs Item/ProductType name overlap
    - Never infer mapping from identical labels

### NSW_SHEET_SET_INDEX_v1.md (5 Fixes)

1. **Fix B1:** Add Engineering Bank Mapping Table
   - Cursor/Pipeline Sheet → Engineering Bank Sheet mapping
   - Reference table for AI-assisted work

2. **Fix B2:** Clarify Catalog Chain vs L1 Parse Sheets
   - Decision CLOSED: NSW_CATALOG_CHAIN_MASTER is canonical
   - NSW_L1_CONFIG_LINES is legacy parse output

3. **Fix B3:** Update NSW_L2_PRODUCTS Status
   - Change from ACTIVE to LEGACY
   - Note: Authoritative is NSW_SKU_MASTER_CANONICAL

4. **Fix B4:** Update "Not Yet Generated" Statements
   - Update to "Generated and active" where applicable

5. **Fix B5:** Add Alias Support Block
   - Legacy aliases during transition
   - business_subcategory → business_segment
   - SC_L1..SC_L4 → SCL

---

## Output Files

### Created Files

1. **NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2.md**
   - All 10 fixes applied
   - Version updated to v1.2
   - Date updated

2. **NSW_SHEET_SET_INDEX_v1.2.md**
   - All 5 fixes applied
   - Version updated to v1.2
   - Date updated

### Safety Features

- **Never overwrites:** Original v1 files remain untouched
- **Timestamp suffix:** If output file exists, creates with timestamp (e.g., `_20250126_143022`)
- **Backup safe:** Original files can be used as reference

---

## Verification Checklist

After running Phase 3, verify:

### NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2.md

- [ ] Section 0 (Engineering Bank Operating Reality) exists
- [ ] SC_Lx definition shows SCL (not capability_class)
- [ ] "Do Not Force Fill" Rule present
- [ ] Generic Naming Rule present
- [ ] Contactor example fixed (no coil voltage in Capability_Class)
- [ ] business_subcategory statement updated
- [ ] "Two-Worlds" Warning present
- [ ] Capability vs Feature Line separation present
- [ ] SC_Lx rename scope tightened
- [ ] Name Collision section present

### NSW_SHEET_SET_INDEX_v1.2.md

- [ ] Engineering Bank Mapping table present
- [ ] Catalog Chain decision CLOSED
- [ ] NSW_L2_PRODUCTS status updated to LEGACY
- [ ] "Not Yet Generated" statements updated
- [ ] Alias Support block present

---

## Expected Outcomes

### Before Phase 3

**NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md:**
- ❌ SC_Lx incorrectly mapped to Capability_Class
- ❌ Missing Operating Reality section
- ❌ Missing Generic Naming Rule
- ❌ Missing "Do Not Force Fill" Rule
- ❌ Contactor example incorrect

**NSW_SHEET_SET_INDEX_v1.md:**
- ❌ Missing Engineering Bank mapping
- ❌ Catalog Chain decision unclear
- ❌ NSW_L2_PRODUCTS status incorrect
- ❌ Missing alias support documentation

### After Phase 3

**NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2.md:**
- ✅ SC_Lx correctly defined as SCL
- ✅ Operating Reality section present
- ✅ Generic Naming Rule present
- ✅ "Do Not Force Fill" Rule present
- ✅ Contactor example corrected
- ✅ All 10 fixes applied

**NSW_SHEET_SET_INDEX_v1.2.md:**
- ✅ Engineering Bank mapping present
- ✅ Catalog Chain decision CLOSED
- ✅ NSW_L2_PRODUCTS status corrected
- ✅ All 5 fixes applied

---

## Success Criteria

Phase 3 is complete when:

- [x] NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2.md created ✅
- [x] NSW_SHEET_SET_INDEX_v1.2.md created ✅
- [x] All 10 fixes applied to Terminology Freeze ✅
- [x] All 5 fixes applied to Sheet Set Index ✅
- [x] Original v1 files NOT modified ✅
- [x] Version numbers updated to v1.2 ✅

---

## Troubleshooting

### Issue: "File not found"

**Solution:** Check that v1 files exist in the input directory.

### Issue: "Output file already exists"

**Solution:** Script automatically creates with timestamp suffix. Original v1.2 file is preserved.

### Issue: "Some fixes not applied"

**Solution:** 
1. Check that the original v1 file has the expected content
2. Run with `--dry-run` to see what would be changed
3. Manual review may be needed for complex replacements

---

## Next Steps

After Phase 3 is complete:

1. ✅ **Phase 3: Update freeze documents** - **COMPLETE**
2. ⏭️ **Phase 4: Fix scripts** (30 min) - Next
   - Remove SC_Lx auto-mapping from migrate_sku_price_pack.py
   - Add Generic Naming validation

---

## Document References

- `PATCH_REVIEW_REPORT_v1.2.md` - Original patch review (10 fixes)
- `PATCH_REVIEW_REPORT_v1.2_REVISED.md` - Revised with Excel findings
- `EXECUTIVE_SUMMARY_AND_ACTION_PLAN.md` - Overall plan
- `PHASE_2_COMPLETE.md` - Phase 2 completion

---

**END OF PHASE 3 EXECUTION GUIDE**




