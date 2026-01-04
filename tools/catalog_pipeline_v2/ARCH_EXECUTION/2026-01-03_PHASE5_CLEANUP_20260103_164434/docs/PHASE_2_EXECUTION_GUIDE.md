# Phase 2: Update v1.4 File - Execution Guide

**Date:** 2025-01-XX  
**Status:** ✅ READY FOR EXECUTION  
**Objective:** Apply fixes from normalized file to v1.4 file

---

## Overview

Phase 2 aligns the v1.4 master file (`NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP.xlsx`) with the normalized file (`ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`) by copying three sheets:

1. **TERMINOLOGY_ALIASES** - Correct SC_Lx → SCL mapping
2. **README_ITEM_GOVERNANCE** - Generic Naming and Do Not Force Fill rules
3. **README_MASTER** - Operating Reality section

**Key Principle:** SC_Lx is SCL; capability stays in capability_codes. capability_class_x is optional and must never replace SC_Lx.

---

## Prerequisites

### Required Files

1. **Normalized file** (source of fixes):
   - `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`
   - Must have sheets: `TERMINOLOGY_ALIASES`, `README_ITEM_GOVERNANCE`, `README_MASTER`

2. **v1.4 file** (target to update):
   - `NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP.xlsx`
   - Will be updated with fixes from normalized file

### Important Prerequisites (Must Do)

1. **Close Excel** - File must not be open during write
2. **Use admin/unlocked copy** - If structure protection blocks edits, use an unlocked copy
3. **Never overwrite in-place** - Always generate a new Phase-2 output file

### Required Tools

- Python 3.7+
- openpyxl

```bash
pip install openpyxl
```

---

## Execution Method: Automated Script (Recommended)

**Script:** `scripts/apply_phase2_fixes_openpyxl.py`

**Why openpyxl (not pandas):**
- Preserves README layout (no pandas NaN/type issues)
- Safer for "text sheets" + merged cells + widths
- Writes to a NEW output file (no in-place overwrite)
- Preserves formatting and structure

**Usage:**

```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2

python3 scripts/apply_phase2_fixes_openpyxl.py \
  --normalized-file "input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx" \
  --v14-file "active/NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP.xlsx" \
  --out "active/NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP_PHASE2.xlsx"
```

**What it does:**
1. Loads normalized and v1.4 workbooks
2. Copies three sheets cell-by-cell (preserving formatting)
3. Saves to new output file (safe copy)
4. Runs semantic verification checks
5. Prints summary

**Verification only (safe check, no changes):**

```bash
python3 scripts/apply_phase2_fixes_openpyxl.py \
  --normalized-file "input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx" \
  --v14-file "active/NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP_PHASE2.xlsx" \
  --verify-only
```

---

---

## What "Pass" Looks Like (Acceptance Checks)

After Phase-2, verify:

### ✅ TERMINOLOGY_ALIASES

- [x] Contains mapping: `SC_L1..SC_L8` → `SCL` (Structural Construction Layers)
- [x] Does NOT map `SC_Lx` to `capability_class_x`
- [x] Capability semantics remain separate (in `capability_codes` column)

### ✅ README_ITEM_GOVERNANCE

- [x] Contains "Generic Naming Rule (MANDATORY)"
- [x] Contains "Universal Population Rule" or "Do Not Force Fill Rule"
- [x] Text preserved exactly from normalized source (layout + content)

### ✅ README_MASTER

- [x] Contains "Operating Reality" or "Layer Discipline" section
- [x] Engineering Bank context preserved
- [x] Formatting preserved (no pandas flattening)

---

## Verification (Automated)

The script performs semantic verification:

1. **TERMINOLOGY_ALIASES verification:**
   - Confirms `SC_L1..SC_L8` → `SCL` mapping exists
   - Confirms no `SC_Lx` → `capability_class` mapping

2. **README verification:**
   - Scans for "Generic Naming Rule" text
   - Scans for "Universal Population Rule" or "Do Not Force Fill" text
   - Scans for "Operating Reality" text (warn-only if missing in README_MASTER)

---

## Safety & Integrity Guarantees

- ✔ No data sheets touched (only three governance/README sheets)
- ✔ No SC_Lx values modified in data sheets
- ✔ No workbook overwritten in place (always creates new output)
- ✔ README formatting preserved (cell-by-cell copy with openpyxl)
- ✔ Suitable for re-locking after review

---

## Failure Handling (Safe)

If verification fails:
- Do not overwrite files
- Open the output and compare the three sheets manually
- Re-run apply after correcting source sheet text
- Check that normalized file has correct content

---

## Troubleshooting

### Issue: "File not found"

**Solution:** Check file paths are correct and files exist.

### Issue: "Sheet not found"

**Solution:** Ensure normalized file has all required sheets:
- TERMINOLOGY_ALIASES
- README_ITEM_GOVERNANCE
- README_MASTER

### Issue: "Permission denied" or "Workbook is protected"

**Solution:** 
1. Ensure v1.4 file is not open in Excel
2. Use an admin/unlocked copy if structure protection is enabled
3. Close Excel and try again

### Issue: "Verification failed"

**Solution:** 
1. Check that all three sheets were copied correctly
2. Compare manually in Excel
3. Re-run the script with `--verify-only` to see specific differences
4. Verify normalized file has correct content

---

## Recommended Next Step (Admin)

After Phase-2 review:
1. Open the Phase-2 file in Excel
2. Re-apply Workbook Structure protection
3. Save as final: `NSW_ENGINEERING_BANK_MASTER_v1.4_ACTIVE_SOP_FINAL.xlsx`

---

## Success Criteria

Phase 2 is complete when:

- [x] TERMINOLOGY_ALIASES in v1.4 matches normalized file ✅
- [x] README_ITEM_GOVERNANCE in v1.4 matches normalized file ✅
- [x] README_MASTER in v1.4 matches normalized file ✅
- [x] Verification script passes ✅
- [x] Output file created (no in-place overwrite) ✅

---

## Next Steps

After Phase 2 is complete:

1. ✅ **Phase 2: Update v1.4 file** - **COMPLETE**
2. ⏭️ **Phase 3: Update freeze documents** (1-2 hours) - Next
3. ⏭️ **Phase 4: Fix scripts** (30 min)

**Note:** Do not run Phase-2 on AI-SAFE workbooks. Only the admin v1.4 master needs Phase-2. AI-safe files intentionally exclude these sheets.

---

## Document References

- `ACCESSORIES_MASTER_GAPS_RESOLVED.md` - Phase 1 completion
- `EXECUTIVE_SUMMARY_AND_ACTION_PLAN.md` - Overall plan
- `FINAL_PLAN_AFTER_NORMALIZATION.md` - Detailed plan

---

**END OF PHASE 2 EXECUTION GUIDE**

