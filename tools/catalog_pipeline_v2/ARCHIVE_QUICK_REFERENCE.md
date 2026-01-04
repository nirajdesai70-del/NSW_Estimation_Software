# Archive Quick Reference - What to Archive Before Freeze

**Date:** 2025-01-XX  
**Status:** QUICK REFERENCE  
**Purpose:** Quick checklist of what to archive before implementing freeze structure

---

## ✅ ANSWER: Do You Need to Redo Everything?

**NO** - Most work can be **MIGRATED**, not redone.

**What Can Be Migrated:**
- ✅ SKU data (NSW_L2_PRODUCTS → NSW_SKU_MASTER_CANONICAL)
- ✅ Price data (NSW_PRICE_MATRIX → NSW_PRICE_MATRIX_CANONICAL)
- ✅ Canonical extraction (just needs sheet renaming)

**What Needs Archive (Not Migration):**
- ⚠️ Legacy parse sheets (old format)
- ⚠️ Temporary files (can regenerate)
- ⚠️ Rebuild test files (not needed)

---

## 📁 What to Archive

### 1. Legacy Outputs (Archive - Old Format)

**Location:** `output/` and `archives/.../02_outputs/`

**Files:**
- `NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx` (old format)
- `LC1E_ENGINEER_REVIEW_v1.xlsx` (old format)
- `LC1E_CANONICAL_v1.xlsx` (old format, if different structure)

**Action:** Move to `archives/.../PRE_FREEZE_ARCHIVE/00_legacy_outputs/`

**Reason:** Old format, will be replaced by new freeze structure

---

### 2. Temporary Files (Archive - Can Regenerate)

**Location:** `output/` and `output/lc1e/`

**Files:**
- `LC1E_L1_tmp.xlsx`
- `LC1E_L2_tmp.xlsx`
- `l1_tmp.xlsx`
- `l2_tmp.xlsx`

**Action:** Move to `archives/.../PRE_FREEZE_ARCHIVE/01_temporary_files/`

**Reason:** Temporary intermediate files, can be regenerated from canonical

---

### 3. Rebuild Test Files (Archive - Not Needed)

**Location:** `archives/.../02_outputs/rebuild_check/`

**Files:**
- 14 rebuild test files (*.xlsx, *.txt)

**Action:** Move to `archives/.../PRE_FREEZE_ARCHIVE/02_rebuild_tests/`

**Reason:** Test/rebuild attempts, not needed for production

---

### 4. Legacy Scripts (Archive - Reference Only)

**Location:** `archives/.../01_scripts/`

**Files:**
- `build_l2_from_canonical.py` (old version)
- `derive_l1_from_l2.py` (old version)
- `build_master_workbook.py` (old version)

**Action:** Move to `archives/.../PRE_FREEZE_ARCHIVE/03_legacy_scripts/`

**Reason:** Superseded by new scripts, keep for reference

---

## ✅ What to Keep Active

### 1. Source Files (Keep - No Change)

**Location:** `input/schneider/lc1e/`

**Files:**
- `Switching _All_WEF 15th Jul 25.xlsx`
- `Switching _All_WEF 15th Jul 25.pdf`

**Action:** Keep as-is

**Reason:** Source files don't change

---

### 2. Active Scripts (Keep - Active)

**Location:** `scripts/` and `active/schneider/LC1E/01_scripts/`

**Files:**
- `build_nsw_workbook_from_canonical.py` (generates NSW format)
- `lc1e_extract_page8_v6.py` (active extraction)

**Action:** Keep active, may need updates for freeze terminology

**Reason:** Active scripts, needed for new structure

---

### 3. Canonical Extraction (Keep - Migrate)

**Location:** `output/lc1e/` or `active/.../02_outputs/`

**Files:**
- `LC1E_CANONICAL_v1.xlsx` (if in correct format)

**Action:** Keep, migrate to new structure

**Reason:** Can be migrated to new format

---

## 📊 New File Structure (After Archive)

```
tools/catalog_pipeline_v2/
├── input/                      # Source files (unchanged)
│   └── schneider/lc1e/
│
├── active/                     # Active series work
│   └── schneider/LC1E/
│
├── canonical/                  # NEW: Canonical extraction
│   └── schneider/LC1E/
│       └── LC1E_CANONICAL_v1.xlsx
│
├── nsw_master/                 # NEW: NSW format master workbooks
│   └── schneider/LC1E/
│       └── NSW_LC1E_WEF_2025-07-15_MASTER.xlsx
│           ├── NSW_SKU_MASTER_CANONICAL
│           ├── NSW_PRICE_MATRIX_CANONICAL
│           ├── NSW_CATALOG_CHAIN_MASTER
│           └── ...
│
├── scripts/                    # Active scripts
│   └── ...
│
└── archives/                   # Archived work
    └── schneider/LC1E/
        └── 2025-07-15_WEF/
            └── PRE_FREEZE_ARCHIVE/
                ├── 00_legacy_outputs/
                ├── 01_temporary_files/
                ├── 02_rebuild_tests/
                └── 03_legacy_scripts/
```

---

## ✅ Quick Checklist

**Before Freeze Implementation:**

- [ ] Review `output/` directory
- [ ] Identify files to archive
- [ ] Create `PRE_FREEZE_ARCHIVE/` structure
- [ ] Move legacy outputs to archive
- [ ] Move temporary files to archive
- [ ] Move rebuild tests to archive
- [ ] Create migration script
- [ ] Test migration on sample data
- [ ] Migrate active data to new structure
- [ ] Validate migrated data
- [ ] Update documentation

---

## 🎯 Migration vs Archive Decision Tree

```
Is it source data?
├─ YES → Keep in input/ (no change)
└─ NO → Is it in correct format?
    ├─ YES → Can it be migrated?
    │   ├─ YES → Migrate to new structure
    │   └─ NO → Keep active, update terminology
    └─ NO → Is it temporary?
        ├─ YES → Archive (can regenerate)
        └─ NO → Is it legacy format?
            ├─ YES → Archive (old format)
            └─ NO → Review case-by-case
```

---

## 📝 Archive Actions Summary

| Category | Files | Action | Location |
|----------|-------|--------|----------|
| Legacy Outputs | Old format workbooks | Archive | `PRE_FREEZE_ARCHIVE/00_legacy_outputs/` |
| Temporary Files | `*_tmp.xlsx` | Archive | `PRE_FREEZE_ARCHIVE/01_temporary_files/` |
| Rebuild Tests | 14 test files | Archive | `PRE_FREEZE_ARCHIVE/02_rebuild_tests/` |
| Legacy Scripts | Old extraction scripts | Archive | `PRE_FREEZE_ARCHIVE/03_legacy_scripts/` |
| Source Files | Pricelist XLSX/PDF | Keep | `input/` (unchanged) |
| Active Scripts | Current scripts | Keep | `scripts/` (may need updates) |
| Canonical Data | Extraction output | Migrate | `canonical/` (new location) |

---

## ⚠️ Critical: Do This First

1. **Create migration script** - Test before archiving
2. **Backup active data** - Before any moves
3. **Validate migration** - Ensure no data loss
4. **Then archive** - After successful migration

---

**Reference:** See `ARCHIVE_AND_MIGRATION_PLAN.md` for detailed plan.


