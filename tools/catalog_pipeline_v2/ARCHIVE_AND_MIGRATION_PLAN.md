# Archive and Migration Plan - Pre-Freeze Housekeeping

**Date:** 2025-01-XX  
**Status:** CRITICAL - MUST COMPLETE BEFORE FREEZE IMPLEMENTATION  
**Purpose:** Identify what to archive, what to migrate, and new file structure before implementing freeze documents

---

## ⚠️ CRITICAL QUESTION ANSWERED

**Q: Does adopting the freeze structure mean redoing all pricelist/catalog work?**

**A: NO - Most work can be MIGRATED, not redone. But we need housekeeping first.**

### What Can Be Migrated (No Rework Needed)
- ✅ **SKU data** - Can be migrated from `NSW_L2_PRODUCTS` → `NSW_SKU_MASTER_CANONICAL`
- ✅ **Price data** - Can be migrated from `NSW_PRICE_MATRIX` → `NSW_PRICE_MATRIX_CANONICAL`
- ✅ **Canonical extraction** - Already in correct format, just needs sheet renaming
- ✅ **Source files** - Keep as-is (input files don't change)

### What Needs Review/Archive (May Need Rework)
- ⚠️ **Legacy parse sheets** - `NSW_L1_CONFIG_LINES` (old format) vs `NSW_CATALOG_CHAIN_MASTER` (new format)
- ⚠️ **Intermediate temp files** - `*_tmp.xlsx` files (can be regenerated)
- ⚠️ **Rebuild test files** - Multiple rebuild attempts (archive-ready)
- ⚠️ **Legacy scripts** - Old extraction scripts (archive, but keep for reference)

---

## 1. Current State Analysis

### 1.1 Completed Work (Archived)

**Location:** `archives/schneider/LC1E/2025-07-15_WEF/`

**What's There:**
- ✅ Complete LC1E extraction (2025-07-15 WEF)
- ✅ Legacy scripts (build_l2_from_canonical.py, derive_l1_from_l2.py, etc.)
- ✅ Output files (LC1E_CANONICAL_v1.xlsx, LC1E_ENGINEER_REVIEW_v1.xlsx, etc.)
- ✅ Rebuild test files (14 files in rebuild_check/)
- ✅ QC documentation
- ✅ Decision documentation

**Status:** ✅ **ALREADY ARCHIVED** - Keep as-is for reference

---

### 1.2 Active Work (Current)

**Location:** `active/schneider/LC1E/` and `output/`

**What's There:**
- ✅ Active extraction script: `active/schneider/LC1E/01_scripts/lc1e_extract_page8_v6.py`
- ✅ Current outputs: `output/lc1e/LC1E_CANONICAL_v1.xlsx`, `LC1E_ENGINEER_REVIEW_v1.xlsx`
- ✅ Active scripts: `scripts/build_nsw_workbook_from_canonical.py` (generates NSW format)

**Status:** ⚠️ **NEEDS REVIEW** - Some files may need migration to new structure

---

### 1.3 Legacy Outputs (Needs Archive Decision)

**Location:** `output/` and `archives/.../02_outputs/`

**Files to Review:**
- `output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx` - Legacy format?
- `output/lc1e/LC1E_L1_tmp.xlsx` - Temporary file?
- `output/lc1e/LC1E_L2_tmp.xlsx` - Temporary file?
- `archives/.../02_outputs/rebuild_check/*.xlsx` - 14 rebuild test files

**Status:** ⚠️ **NEEDS DECISION** - Archive or migrate?

---

## 2. Migration vs Rework Assessment

### 2.1 What Can Be Migrated (No Rework)

| Current File/Sheet | New File/Sheet | Migration Method | Effort |
|-------------------|----------------|------------------|--------|
| `NSW_L2_PRODUCTS` sheet | `NSW_SKU_MASTER_CANONICAL` | Column rename + sheet copy | Low |
| `NSW_PRICE_MATRIX` sheet | `NSW_PRICE_MATRIX_CANONICAL` | Sheet copy (same structure) | Low |
| Canonical extraction output | `NSW_CATALOG_CHAIN_MASTER` | Restructure L0/L1/L2 chain | Medium |
| Source pricelist files | `input/` (keep as-is) | No change | None |

**Migration Script Needed:** ✅ Yes - Create migration script to:
1. Read old workbook
2. Extract sheets
3. Rename columns (business_subcategory → business_segment, SC_Lx → capability_class_x)
4. Write to new workbook structure

---

### 2.2 What Needs Rework (Cannot Migrate)

| Current File/Sheet | Issue | Action |
|-------------------|-------|--------|
| `NSW_L1_CONFIG_LINES` (old format) | Different structure (duty×voltage expansion) | Generate new `NSW_CATALOG_CHAIN_MASTER` from canonical |
| `*_tmp.xlsx` files | Temporary intermediate files | Regenerate from canonical |
| Rebuild test files | Multiple rebuild attempts | Archive (not needed) |
| Legacy scripts | Old extraction logic | Archive (keep for reference) |

**Rework Effort:** ⚠️ Medium - Need to regenerate from canonical extraction

---

### 2.3 What Can Be Archived (No Migration Needed)

| File/Item | Reason | Action |
|-----------|--------|--------|
| `rebuild_check/*.xlsx` (14 files) | Test/rebuild attempts | Archive |
| `LC1E_L1_tmp.xlsx`, `LC1E_L2_tmp.xlsx` | Temporary intermediate files | Archive (can regenerate) |
| Legacy extraction scripts | Superseded by new scripts | Archive (keep for reference) |
| Old QC reports | Historical reference | Archive |

---

## 3. Archive Plan

### 3.1 Archive Structure

**New Archive Location:** `archives/schneider/LC1E/2025-07-15_WEF/PRE_FREEZE_ARCHIVE/`

**Archive Categories:**

```
PRE_FREEZE_ARCHIVE/
├── 00_legacy_outputs/          # Old format outputs (before freeze)
│   ├── NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
│   ├── LC1E_ENGINEER_REVIEW_v1.xlsx
│   └── LC1E_CANONICAL_v1.xlsx (old format)
│
├── 01_temporary_files/         # Temp files (can regenerate)
│   ├── LC1E_L1_tmp.xlsx
│   ├── LC1E_L2_tmp.xlsx
│   └── l1_tmp.xlsx, l2_tmp.xlsx
│
├── 02_rebuild_tests/           # Rebuild test files
│   └── (move from rebuild_check/)
│
├── 03_legacy_scripts/          # Old scripts (reference only)
│   ├── build_l2_from_canonical.py (old version)
│   ├── derive_l1_from_l2.py (old version)
│   └── build_master_workbook.py (old version)
│
└── 04_documentation/           # Pre-freeze documentation
    └── (keep existing docs, add migration notes)
```

---

### 3.2 Archive Checklist

**Before Archiving:**
- [ ] Verify canonical extraction is complete and validated
- [ ] Verify SKU data can be migrated (no data loss)
- [ ] Verify price data can be migrated (no data loss)
- [ ] Document what's being archived and why
- [ ] Create migration script to convert old → new format
- [ ] Test migration script on sample data

**Archive Actions:**
- [ ] Move legacy outputs to `00_legacy_outputs/`
- [ ] Move temporary files to `01_temporary_files/`
- [ ] Move rebuild tests to `02_rebuild_tests/`
- [ ] Move legacy scripts to `03_legacy_scripts/`
- [ ] Update documentation in `04_documentation/`
- [ ] Create `ARCHIVE_INDEX.md` listing what's archived

---

## 4. New File Structure (Post-Freeze)

### 4.1 Active Work Structure

```
tools/catalog_pipeline_v2/
├── input/                      # Source files (unchanged)
│   └── schneider/
│       └── lc1e/
│           ├── Switching _All_WEF 15th Jul 25.xlsx
│           └── Switching _All_WEF 15th Jul 25.pdf
│
├── active/                     # Active series work
│   └── schneider/
│       └── LC1E/
│           ├── 01_scripts/
│           │   └── lc1e_extract_page8_v6.py
│           ├── 02_outputs/
│           │   └── NSW_LC1E_WEF_2025-07-15_CANONICAL.xlsx
│           ├── 03_qc/
│           │   └── QC_PAGE8_VALIDATION.md
│           └── 04_docs/
│               └── LC1E_Page8_SEMANTIC_LOCK.yaml
│
├── canonical/                  # NEW: Canonical extraction outputs
│   └── schneider/
│       └── LC1E/
│           └── LC1E_CANONICAL_v1.xlsx
│
├── nsw_master/                 # NEW: NSW format master workbooks
│   └── schneider/
│       └── LC1E/
│           └── NSW_LC1E_WEF_2025-07-15_MASTER.xlsx
│               ├── NSW_SKU_MASTER_CANONICAL
│               ├── NSW_PRICE_MATRIX_CANONICAL
│               ├── NSW_CATALOG_CHAIN_MASTER
│               ├── NSW_SKU_RATINGS
│               └── NSW_ACCESSORY_SKU_MASTER
│
├── scripts/                    # Active scripts (unchanged)
│   ├── build_nsw_workbook_from_canonical.py
│   └── ...
│
└── archives/                   # Archived work (unchanged structure)
    └── schneider/
        └── LC1E/
            └── 2025-07-15_WEF/
                └── PRE_FREEZE_ARCHIVE/
```

---

### 4.2 New File Naming Convention

**Canonical Extraction:**
- `{SERIES}_CANONICAL_v{VERSION}.xlsx` (e.g., `LC1E_CANONICAL_v1.xlsx`)

**NSW Master Workbook:**
- `NSW_{SERIES}_WEF_{DATE}_MASTER.xlsx` (e.g., `NSW_LC1E_WEF_2025-07-15_MASTER.xlsx`)

**Sheet Names (Inside Master Workbook):**
- `NSW_SKU_MASTER_CANONICAL`
- `NSW_PRICE_MATRIX_CANONICAL`
- `NSW_CATALOG_CHAIN_MASTER`
- `NSW_SKU_RATINGS`
- `NSW_ACCESSORY_SKU_MASTER`
- `NSW_VARIANT_MASTER`
- `NSW_PRODUCT_VARIANTS`

---

## 5. Migration Script Plan

### 5.1 Migration Script: `migrate_to_freeze_structure.py`

**Purpose:** Convert old workbook structure to new freeze structure

**Input:**
- Old workbook: `NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx`
- Canonical extraction: `LC1E_CANONICAL_v1.xlsx`

**Output:**
- New workbook: `NSW_LC1E_WEF_2025-07-15_MASTER.xlsx` (freeze structure)

**Migration Steps:**
1. Read old `NSW_L2_PRODUCTS` sheet
2. Rename columns: `business_subcategory` → `business_segment`, `SC_Lx` → `capability_class_x`
3. Write to `NSW_SKU_MASTER_CANONICAL` sheet
4. Read old `NSW_PRICE_MATRIX` sheet
5. Write to `NSW_PRICE_MATRIX_CANONICAL` sheet (same structure)
6. Generate `NSW_CATALOG_CHAIN_MASTER` from canonical extraction
7. Generate `NSW_SKU_RATINGS` from canonical extraction
8. Generate `NSW_ACCESSORY_SKU_MASTER` from canonical extraction
9. Validate migration (row counts, data integrity)

---

## 6. Housekeeping Actions (Before Freeze)

### 6.1 Immediate Actions (This Week)

1. **✅ CREATE MIGRATION SCRIPT**
   - Create `scripts/migrate_to_freeze_structure.py`
   - Test on sample data
   - Document migration process

2. **✅ REVIEW ACTIVE FILES**
   - Review `output/` directory
   - Identify what can be migrated vs archived
   - Document decisions

3. **✅ CREATE ARCHIVE STRUCTURE**
   - Create `PRE_FREEZE_ARCHIVE/` directory structure
   - Create `ARCHIVE_INDEX.md`

4. **✅ MIGRATE ACTIVE DATA**
   - Run migration script on active LC1E data
   - Validate migrated data
   - Create new master workbook

### 6.2 Archive Actions (After Migration)

1. **✅ MOVE LEGACY FILES**
   - Move legacy outputs to archive
   - Move temporary files to archive
   - Move rebuild tests to archive

2. **✅ UPDATE DOCUMENTATION**
   - Update file structure documentation
   - Update workflow documentation
   - Create migration notes

3. **✅ CLEAN OUTPUT DIRECTORY**
   - Remove temporary files
   - Keep only active canonical and master workbooks
   - Update `.gitignore` if needed

---

## 7. Risk Assessment

### 7.1 Low Risk ✅
- Archiving completed work (already in archives/)
- Moving temporary files (can regenerate)
- Creating new directory structure

### 7.2 Medium Risk ⚠️
- Migration script (data transformation) - **MITIGATED** by testing
- Column renaming (terminology changes) - **MITIGATED** by dual support
- File structure changes - **MITIGATED** by keeping archives

### 7.3 High Risk ❌
- Data loss during migration - **MITIGATED** by:
  - Keeping original files in archive
  - Testing migration script
  - Validating migrated data
  - Creating backup before migration

---

## 8. Success Criteria

**Migration is successful when:**
- ✅ All SKU data migrated to `NSW_SKU_MASTER_CANONICAL`
- ✅ All price data migrated to `NSW_PRICE_MATRIX_CANONICAL`
- ✅ Catalog chain generated in `NSW_CATALOG_CHAIN_MASTER`
- ✅ Row counts match (no data loss)
- ✅ Column names follow freeze terminology
- ✅ Legacy files safely archived
- ✅ New file structure in place
- ✅ Documentation updated

---

## 9. Next Steps

### Step 1: Create Migration Script (Priority 1)
- [ ] Create `scripts/migrate_to_freeze_structure.py`
- [ ] Test on sample data
- [ ] Document migration process

### Step 2: Review and Archive (Priority 2)
- [ ] Review `output/` directory
- [ ] Create archive structure
- [ ] Move files to archive

### Step 3: Migrate Active Data (Priority 3)
- [ ] Run migration script
- [ ] Validate migrated data
- [ ] Create new master workbook

### Step 4: Clean and Document (Priority 4)
- [ ] Clean output directory
- [ ] Update documentation
- [ ] Create migration notes

---

## 10. References

- `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md` - Terminology definitions
- `NSW_SHEET_SET_INDEX_v1.md` - Sheet structure definitions
- `FREEZE_DOCUMENTS_REVIEW.md` - Review and assessment

---

**Status:** ✅ PLAN COMPLETE - READY FOR EXECUTION

**Critical:** Complete housekeeping BEFORE implementing freeze structure to avoid rework.


