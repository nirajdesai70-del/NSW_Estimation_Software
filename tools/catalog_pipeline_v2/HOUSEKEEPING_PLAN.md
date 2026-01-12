# Catalog Pipeline v2 - Housekeeping Plan

**Date**: 2026-01-03  
**Status**: 📋 PLANNING → 🚀 READY FOR EXECUTION  
**Scope**: `catalog_pipeline_v2/` only (not entire repo)

---

## 🎯 Objective

**Freeze what is live, archive what is historical, clearly mark what is temporary.**

Prevent future confusion by structure, not memory. This is a **one-time structural cleanup** to establish discipline going forward.

---

## ✅ What We DO NOT Touch (Very Important)

❌ **DO NOT touch:**
- `catalog_pipeline_v2/active/` - Current work in progress
- `catalog_pipeline_v2/archives/` - Already frozen history
- `catalog_pipeline_v2/templates/` - Reusable templates
- `catalog_pipeline_v2/freeze_docs/` - Frozen documentation
- `SoR/`, `SoE/`, `SoW/`, `ARCH/` - Governed folders
- Any file explicitly marked `CLEAN` / `FINAL` / `FREEZE`

---

## 📋 Housekeeping Tasks

### Task 1: Create ARCH_EXECUTION Structure

**Action**: Create execution debris archive folder

```
catalog_pipeline_v2/
└── ARCH_EXECUTION/
    ├── 2025-12_ITERATION_1/    # First iteration debris
    ├── 2025-12_ITERATION_2/    # Second iteration debris
    └── README.md               # Archive index
```

**Purpose**: Capture execution debris from earlier runs without deleting anything.

---

### Task 2: Organize Scripts (Active vs Legacy)

**Action**: Create script subfolders and tag scripts

#### A. Create Script Structure

```
scripts/
├── [active scripts at root]  # Kept at root for backward compatibility
├── legacy/          # Superseded scripts
└── README.md        # Script status index
```

**Note:** Active scripts remain at `scripts/` root level to maintain backward compatibility with `templates/run_pipeline.sh`. Only legacy and one-off scripts are moved to subfolders.

#### B. Identify Active Scripts (KEEP IN active/)

✅ **Active Scripts** (Phase-5 v1.2 CLEAN):
- `lc1e_extract_canonical.py` - Extract canonical from raw pricelist (LC1E-specific)
- `lc1e_build_l2.py` - Build L2 from canonical (LC1E-specific)
- `derive_l1_from_l2.py` - Derive L1 from L2 (generic, used by template)
- `build_nsw_workbook_from_canonical.py` - Build NSW workbook (PRIMARY, generic)
- `migrate_sku_price_pack.py` - Migrate SKU/price/ratings

✅ **Generic Scripts** (still used by template, keep in active/):
- `build_l2_from_canonical.py` - Generic L2 builder (used by run_pipeline.sh template)
- `build_master_workbook.py` - Legacy format builder (optional output, used by template)

#### C. Identify Legacy Scripts (MOVE TO legacy/)

📦 **Legacy Scripts** (superseded, do not use):
- `build_nsw_workbook.py` - Old version, replaced by `build_nsw_workbook_from_canonical.py`

🔧 **One-off Fix Scripts** (move to ARCH_EXECUTION):
- `apply_phase2_fixes.py` - One-off Phase 2 fixes
- `apply_phase2_fixes_openpyxl.py` - One-off Phase 2 fixes (openpyxl version)
- `apply_phase3_fixes.py` - One-off Phase 3 fixes
- `review_phase2_file.py` - Review script
- `review_item_master_excel.py` - Review script
- `validate_against_v6_v2.py` - Validation script
- `validate_canonical_against_source.py` - Validation script
- `inspect_lc1e_raw.py` - Inspection script
- `inspect_pricelist.py` - Inspection script
- `build_catalog_chain_master.py` - Legacy chain builder

#### D. Tag Scripts

**Add to top of active scripts:**
```python
# STATUS: ACTIVE — Phase-5 v1.2 CLEAN
```

**Add to top of legacy scripts:**
```python
# STATUS: LEGACY — superseded, do not use
```

---

### Task 3: Archive Execution Debris from output/

**Action**: Move temporary/test/debug files to ARCH_EXECUTION

#### Files to Move:

**Temporary Outputs:**
- `output/l1_tmp.xlsx` → `ARCH_EXECUTION/2025-12_ITERATION_2/tmp_outputs/`
- `output/l2_tmp.xlsx` → `ARCH_EXECUTION/2025-12_ITERATION_2/tmp_outputs/`

**Test Files:**
- `output/NSW_LC1E_WEF_2025-07-15_TEST_20260103_103812.xlsx` → `ARCH_EXECUTION/2025-12_ITERATION_2/test_outputs/`

**Old Outputs:**
- `output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx` → `ARCH_EXECUTION/2025-12_ITERATION_1/old_outputs/` (if not needed)

**Debug Files:**
- `output/FILES_EXIST.txt` → `ARCH_EXECUTION/2025-12_ITERATION_2/debug/`
- `output/README_FINDER_FIX.txt` → `ARCH_EXECUTION/2025-12_ITERATION_2/debug/`
- `output/TEST_VISIBILITY.txt` → `ARCH_EXECUTION/2025-12_ITERATION_2/debug/`

**Subfolder:**
- `output/lc1e/` → Review contents, move test/tmp files to ARCH_EXECUTION, keep final if needed

---

### Task 4: Archive Root-Level Documentation Debris

**Action**: Move planning/execution docs to ARCH_EXECUTION (if not needed for reference)

**Files to Review and Possibly Move:**
- `PHASE_2_*.md` - Phase 2 execution docs
- `PHASE_3_*.md` - Phase 3 execution docs
- `PHASE_5_PREPARATION.md` - Preparation docs
- `EXECUTION_*.md` - Execution summaries
- `EXCEL_REVIEW_*.md` - Review reports
- `GAP_*.md` - Gap analysis docs
- `PATCH_REVIEW_*.md` - Patch review docs
- `ARCHIVE_*.md` - Archive planning docs (keep if still relevant)
- `CRITICAL_FIXES_APPLIED.md` - Fix documentation
- `CANONICAL_EXTRACTOR_*.md` - Extractor notes
- `NSW_BUILDER_FIX_COMPLETE.md` - Fix documentation
- `FIX_FINDER_VISIBILITY.md` - Fix documentation
- `ACCESSORIES_MASTER_GAPS_RESOLVED.md` - Gap resolution
- `V6_*.md` - V6 analysis docs
- `OPTION_B_*.md` - Option B docs
- `NEXT_STEPS_LC1E.md` - Next steps (if superseded)
- `LC1E_STATUS.md` - Status (if superseded)
- `PAUSE_NOTE.md` - Pause notes
- `REVIEW_COMPLETE_SUMMARY.md` - Review summary
- `SELF_VALIDATION_GUIDE.md` - Validation guide (if superseded)
- `INPUT_FILE_REQUIREMENTS.md` - Requirements (if superseded)

**Decision Rule**: 
- If doc is referenced in `README.md` or `OPERATING_MODEL.md` → KEEP
- If doc is historical execution log → MOVE to ARCH_EXECUTION
- If doc is planning that was executed → MOVE to ARCH_EXECUTION
- If doc is still needed for reference → KEEP

**Keep These (Governance/Reference):**
- `README.md` - Main readme
- `OPERATING_MODEL.md` - Operating model
- `NEXT_SERIES_BOOTSTRAP.md` - Bootstrap guide
- `SETUP_COMPLETE.md` - Setup documentation
- `LC1E_PRICELIST_STRUCTURE.md` - Structure reference (if still relevant)

---

### Task 5: Create README Files

**Action**: Add README files to document structure

#### A. `ARCH_EXECUTION/README.md`
```markdown
# Execution Archive

This folder contains execution debris from previous pipeline iterations.

**Structure:**
- `2025-12_ITERATION_1/` - First iteration execution artifacts
- `2025-12_ITERATION_2/` - Second iteration execution artifacts

**Purpose:** Archive temporary files, test outputs, and one-off scripts without deleting them.

**Rule:** New execution debris should go to `SoW/` (temporary) or `ARCH/` (after freeze), not here.
```

#### B. `scripts/README.md`
```markdown
# Pipeline Scripts

**Active Scripts** (`active/`):
- Scripts currently used in Phase-5 LC1E pipeline
- Tagged with `# STATUS: ACTIVE — Phase-5 v1.2 CLEAN`

**Legacy Scripts** (`legacy/`):
- Superseded scripts, kept for reference
- Tagged with `# STATUS: LEGACY — superseded, do not use`

**One-off Scripts** (`ARCH_EXECUTION/`):
- Temporary fix scripts and validation tools
- Moved to execution archive after use
```

---

## 🚀 Execution Checklist

### Phase 1: Create Structure
- [ ] Create `ARCH_EXECUTION/` folder
- [ ] Create `ARCH_EXECUTION/2025-12_ITERATION_1/` subfolders
- [ ] Create `ARCH_EXECUTION/2025-12_ITERATION_2/` subfolders
- [ ] Create `scripts/active/` folder
- [ ] Create `scripts/legacy/` folder

### Phase 2: Organize Scripts
- [ ] Tag active scripts with `# STATUS: ACTIVE` (keep at root for compatibility)
- [ ] Move legacy scripts to `scripts/legacy/`
- [ ] Add `# STATUS: LEGACY` tag to legacy scripts
- [ ] Move one-off scripts to `ARCH_EXECUTION/`
- [ ] Create `scripts/README.md`

### Phase 3: Archive Output Debris
- [ ] Review `output/` folder contents
- [ ] Move temporary files to `ARCH_EXECUTION/`
- [ ] Move test files to `ARCH_EXECUTION/`
- [ ] Move debug files to `ARCH_EXECUTION/`
- [ ] Review `output/lc1e/` subfolder
- [ ] Clean up `output/` folder (keep only active outputs)

### Phase 4: Archive Documentation
- [ ] Review root-level `.md` files
- [ ] Move historical execution docs to `ARCH_EXECUTION/`
- [ ] Keep governance/reference docs in root
- [ ] Create `ARCH_EXECUTION/README.md`

### Phase 5: Update References
- [ ] Update `README.md` if script paths changed
- [ ] Update any scripts that reference moved files
- [ ] Verify active scripts still work

---

## 📐 Output Discipline (Going Forward)

### ✅ Allowed Output Locations
- `catalog_pipeline_v2/active/<vendor>/<series>/02_outputs/` - Active work outputs
- `SoW/<CATEGORY>/` - Temporary outputs (before freeze)
- `ARCH/` - After freeze

### ❌ Not Allowed
- Root-level outputs in `catalog_pipeline_v2/output/` (legacy, use active/ instead)
- Random Excel exports outside SoW
- "Just one test file" outside designated folders

---

## 🎯 Success Criteria

✅ **Housekeeping Complete When:**
1. All active scripts are in `scripts/active/` and tagged
2. All legacy scripts are in `scripts/legacy/` and tagged
3. All execution debris is in `ARCH_EXECUTION/`
4. `output/` folder is clean (only active outputs or empty)
5. Root-level docs are either governance/reference or archived
6. README files document the structure
7. Active scripts still work after moves

---

## 🔄 After This Cleanup

**This is the last structural cleanup.**

Going forward:
- New work → goes to `SoW/`
- Final data → goes to `SoR/`
- Old execution junk → goes to `ARCH_EXECUTION/` (or `ARCH/` after freeze)
- Nothing accumulates in live paths

**One-Line Golden Rule:**
> If a file is not part of today's execution OR not explicitly CLEAN, it must live in `ARCH_EXECUTION` or `SoW` — never alongside active work.

---

**Next Step**: Execute this plan step by step.

