# Archive and Migration Plan - Pre-Freeze Housekeeping v1.1

**Date:** 2025-01-XX  
**Status:** CRITICAL - MUST COMPLETE BEFORE FREEZE IMPLEMENTATION  
**Version:** v1.1 (FINAL - FROZEN)  
**Purpose:** Identify what to archive, what to migrate, and new file structure before implementing freeze documents

---

## ⚠️ SCOPE LOCK

**This migration applies only to the SKU + Price Creation Pack.**

It does **NOT** implement estimation runtime logic (feature explosion, BOM, quotation rules). Those belong to later Phase-5 artifacts.

---

## ⚠️ CRITICAL QUESTION ANSWERED

**Q: Does adopting the freeze structure mean redoing all pricelist/catalog work?**

**A: NO - Most work can be MIGRATED, not redone. But we need housekeeping first.**

### What Can Be Migrated (No Rework Needed)
- ✅ **SKU data** - Can be migrated from legacy `NSW_L2_PRODUCTS` → `NSW_SKU_MASTER_CANONICAL`
- ✅ **Price data** - Can be migrated from `NSW_PRICE_MATRIX` → `NSW_PRICE_MATRIX_CANONICAL`
- ✅ **Ratings data** - Can be migrated to `NSW_SKU_RATINGS` (already generated)
- ✅ **Accessory SKU data** - Can be migrated to `NSW_ACCESSORY_SKU_MASTER`
- ✅ **Source lineage** - Source doc/page/table/row columns preserved
- ✅ **Source files** - Keep as-is (input files don't change)

### What Needs Rework (Limited Scope)
- ⚠️ **Catalog Chain Master** - Must be **rebuilt** from canonical extraction (not migrated)
  - Reason: L0/L1 naming rules corrected (no OEM series at L0/L1; Option B coil in L2)
  - Action: Use `build_catalog_chain_master.py` script
- ⚠️ **Terminology aliases** - Column renaming during migration:
  - `business_subcategory` → `business_segment` (legacy alias supported)
  - `SC_Lx` → `capability_class_x` (legacy alias supported during transition)

### What Can Be Archived (No Migration Needed)
- ⚠️ **Legacy parse sheets** - `NSW_L1_CONFIG_LINES` (old format, archive after QC)
- ⚠️ **Legacy compat sheets** - `NSW_L2_PRODUCTS` (legacy parse/compat output, not authoritative)
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
- ✅ **Already generated:** `NSW_CATALOG_CHAIN_MASTER`, `NSW_SKU_RATINGS`, `NSW_PRICE_MATRIX_QC`, dictionary sheets

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
| Legacy `NSW_L2_PRODUCTS` sheet | `NSW_SKU_MASTER_CANONICAL` | Column rename + sheet copy | Low |
| `NSW_PRICE_MATRIX` sheet | `NSW_PRICE_MATRIX_CANONICAL` | Sheet copy (same structure) | Low |
| Ratings data | `NSW_SKU_RATINGS` | Sheet copy (already generated) | Low |
| Accessory SKU data | `NSW_ACCESSORY_SKU_MASTER` | Sheet copy | Low |
| Source pricelist files | `input/` (keep as-is) | No change | None |

**Note:** `NSW_L2_PRODUCTS` is a **legacy parse/compat sheet**. The **authoritative SKU list** is `NSW_SKU_MASTER_CANONICAL`.

**Migration Script Needed:** ✅ Yes - Script A: `migrate_sku_price_pack.py`

---

### 2.2 What Needs Rework (Cannot Migrate)

| Current File/Sheet | Issue | Action |
|-------------------|-------|--------|
| `NSW_L1_CONFIG_LINES` (old format) | Different structure (duty×voltage expansion) | **Rebuild** `NSW_CATALOG_CHAIN_MASTER` from canonical extraction |
| `*_tmp.xlsx` files | Temporary intermediate files | Regenerate from canonical |
| Rebuild test files | Multiple rebuild attempts | Archive (not needed) |
| Legacy scripts | Old extraction logic | Archive (keep for reference) |

**Note:** `NSW_CATALOG_CHAIN_MASTER` must be **rebuilt** (not migrated) because:
- L0/L1 naming rules have been corrected (no OEM series at L0/L1)
- Option B: coil voltage is L2-only (not L1)
- Semantic corrections require regeneration from canonical source

**Rework Script Needed:** ✅ Yes - Script B: `build_catalog_chain_master.py`

**Rework Effort:** ⚠️ Medium - Need to regenerate from canonical extraction

---

### 2.3 What Can Be Archived (No Migration Needed)

| File/Item | Reason | Action |
|-----------|--------|--------|
| `rebuild_check/*.xlsx` (14 files) | Test/rebuild attempts | Archive |
| `LC1E_L1_tmp.xlsx`, `LC1E_L2_tmp.xlsx` | Temporary intermediate files | Archive (can regenerate) |
| Legacy extraction scripts | Superseded by new scripts | Archive (keep for reference) |
| Old QC reports | Historical reference | Archive |
| Legacy `NSW_L2_PRODUCTS` sheet | Legacy parse/compat output | Archive after migration |
| Legacy `NSW_L1_CONFIG_LINES` sheet | Legacy parse output | Archive after QC verification |

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

### 3.2 Archive Checklist (Freeze Gate - MANDATORY)

**Before Archiving (MUST PASS ALL):**
- [ ] **Price QC count stable** - Missing prices are "not in price list" (not data loss)
- [ ] **SKU master completeness check passes** - All SKUs accounted for
- [ ] **Chain master validated** - Sample rows approved, L0/L1/L2 structure correct
- [ ] **Freeze docs v1.1 committed** - `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.1.md` in `freeze_docs/`
- [ ] **Sheet index v1.1 aligns** - `NSW_SHEET_SET_INDEX_v1.1.md` matches actual workbook
- [ ] **Migration scripts tested** - Both Script A and Script B validated
- [ ] **Data integrity verified** - Row counts match, no data loss

**Archive Actions (After Freeze Gate Passes):**
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
├── sku_price_pack/             # NEW: Single authoritative SKU+Price pack
│   └── schneider/
│       └── LC1E/
│           ├── NSW_SKU_PRICE_PACK_MASTER.xlsx   # Single authoritative workbook
│           │   ├── NSW_SKU_MASTER_CANONICAL
│           │   ├── NSW_PRICE_MATRIX_CANONICAL
│           │   ├── NSW_CATALOG_CHAIN_MASTER
│           │   ├── NSW_SKU_RATINGS
│           │   ├── NSW_ACCESSORY_SKU_MASTER
│           │   ├── NSW_VARIANT_MASTER
│           │   ├── NSW_PRODUCT_VARIANTS
│           │   └── (dictionary sheets)
│           │
│           ├── freeze_docs/                    # Freeze documentation
│           │   ├── NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.1.md
│           │   ├── NSW_SHEET_SET_INDEX_v1.1.md
│           │   └── FREEZE_IMPLEMENTATION_SUMMARY_v1.1.md
│           │
│           └── qc/                            # QC artifacts
│               ├── QC_CHECKLIST.md
│               └── QC_EXPORTS/
│
├── scripts/                    # Active scripts (unchanged)
│   ├── build_nsw_workbook_from_canonical.py
│   ├── migrate_sku_price_pack.py              # NEW: Script A
│   ├── build_catalog_chain_master.py           # NEW: Script B
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

**SKU+Price Pack Master Workbook:**
- `NSW_SKU_PRICE_PACK_MASTER.xlsx` (single authoritative workbook)

**Sheet Names (Inside Master Workbook):**
- `NSW_SKU_MASTER_CANONICAL` (authoritative SKU list)
- `NSW_PRICE_MATRIX_CANONICAL` (authoritative price truth)
- `NSW_CATALOG_CHAIN_MASTER` (L0/L1/L2 continuity - **rebuilt**, not migrated)
- `NSW_SKU_RATINGS` (already generated, reference-active)
- `NSW_ACCESSORY_SKU_MASTER` (already generated, active)
- `NSW_VARIANT_MASTER` (already generated, reference-active)
- `NSW_PRODUCT_VARIANTS` (already generated, active)
- Dictionary sheets (already generated, locked)

**Note:** Legacy sheets `NSW_L2_PRODUCTS` and `NSW_L1_CONFIG_LINES` are **not** in the master workbook. They are legacy parse outputs, archive-ready after QC.

---

## 5. Migration Script Plan

### 5.1 Script A: `migrate_sku_price_pack.py`

**Purpose:** Migrate SKU + Price + Ratings + Accessories (deterministic migration)

**Input:**
- Legacy workbook: `NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx`
- Legacy sheets: `NSW_L2_PRODUCTS`, `NSW_PRICE_MATRIX`, ratings, accessories

**Output:**
- New workbook: `NSW_SKU_PRICE_PACK_MASTER.xlsx`
- New sheets: `NSW_SKU_MASTER_CANONICAL`, `NSW_PRICE_MATRIX_CANONICAL`, `NSW_SKU_RATINGS`, `NSW_ACCESSORY_SKU_MASTER`

**Migration Steps:**
1. Read legacy `NSW_L2_PRODUCTS` sheet (legacy parse/compat output)
2. Rename columns: `business_subcategory` → `business_segment` (legacy alias supported)
3. Rename columns: `SC_Lx` → `capability_class_x` (legacy alias supported during transition)
4. Write to `NSW_SKU_MASTER_CANONICAL` sheet (authoritative)
5. Read legacy `NSW_PRICE_MATRIX` sheet
6. Write to `NSW_PRICE_MATRIX_CANONICAL` sheet (same structure)
7. Migrate ratings data to `NSW_SKU_RATINGS` (already generated, verify)
8. Migrate accessory SKU data to `NSW_ACCESSORY_SKU_MASTER`
9. Validate migration (row counts, data integrity, no data loss)

**Status:** ✅ Deterministic - No semantic changes, only column renaming

---

### 5.2 Script B: `build_catalog_chain_master.py`

**Purpose:** Rebuild Catalog Chain Master from canonical extraction (not migration)

**Input:**
- Canonical extraction: `LC1E_CANONICAL_v1.xlsx`
- Source pricelist: `input/schneider/lc1e/Switching _All_WEF 15th Jul 25.xlsx`

**Output:**
- New sheet: `NSW_CATALOG_CHAIN_MASTER` (in master workbook)

**Rebuild Steps:**
1. Read canonical extraction
2. Apply corrected L0/L1 naming rules:
   - No OEM series at L0/L1
   - Option B: coil voltage is L2-only
   - Business segment vs capability separation
3. Build L0/L1/L2 chain structure
4. Write to `NSW_CATALOG_CHAIN_MASTER` sheet
5. Validate chain structure (L0 → L1 → L2 continuity)

**Status:** ⚠️ Rebuild required - Semantic corrections applied

**Note:** This is **NOT** a migration. It's a rebuild from canonical source with corrected semantics.

---

## 6. Housekeeping Actions (Before Freeze)

### 6.1 Immediate Actions (This Week)

1. **✅ FINALIZE FREEZE DOCS v1.1**
   - Apply patches to `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.1.md`
   - Apply patches to `NSW_SHEET_SET_INDEX_v1.1.md`
   - Apply patches to `FREEZE_IMPLEMENTATION_SUMMARY_v1.1.md`
   - Commit to `sku_price_pack/.../freeze_docs/`

2. **✅ CREATE MIGRATION SCRIPTS**
   - Create `scripts/migrate_sku_price_pack.py` (Script A)
   - Create `scripts/build_catalog_chain_master.py` (Script B)
   - Test on sample data
   - Document migration process

3. **✅ REVIEW ACTIVE FILES**
   - Review `output/` directory
   - Identify what can be migrated vs archived
   - Document decisions

4. **✅ CREATE ARCHIVE STRUCTURE**
   - Create `PRE_FREEZE_ARCHIVE/` directory structure
   - Create `ARCHIVE_INDEX.md`

### 6.2 Archive Actions (After Freeze Gate Passes)

1. **✅ MIGRATE ACTIVE DATA**
   - Run Script A: `migrate_sku_price_pack.py`
   - Run Script B: `build_catalog_chain_master.py`
   - Validate migrated data
   - Create new master workbook

2. **✅ MOVE LEGACY FILES**
   - Move legacy outputs to archive
   - Move temporary files to archive
   - Move rebuild tests to archive

3. **✅ UPDATE DOCUMENTATION**
   - Update file structure documentation
   - Update workflow documentation
   - Create migration notes

4. **✅ CLEAN OUTPUT DIRECTORY**
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
- Catalog chain rebuild (semantic corrections) - **MITIGATED** by Script B validation

### 7.3 High Risk ❌
- Data loss during migration - **MITIGATED** by:
  - Keeping original files in archive
  - Testing migration scripts
  - Validating migrated data
  - Creating backup before migration
  - Freeze gate checklist

---

## 8. Success Criteria

**Migration is successful when:**
- ✅ All SKU data migrated to `NSW_SKU_MASTER_CANONICAL` (authoritative)
- ✅ All price data migrated to `NSW_PRICE_MATRIX_CANONICAL` (authoritative)
- ✅ Catalog chain **rebuilt** in `NSW_CATALOG_CHAIN_MASTER` (not migrated)
- ✅ Row counts match (no data loss)
- ✅ Column names follow freeze terminology (with legacy alias support)
- ✅ Legacy files safely archived
- ✅ New file structure in place
- ✅ Documentation updated
- ✅ Freeze gate checklist passed

---

## 9. Next Steps

### Step 1: Finalize Freeze Docs v1.1 (Priority 1)
- [ ] Apply patches to freeze documents
- [ ] Commit to `sku_price_pack/.../freeze_docs/`
- [ ] Verify alignment with actual workbook

### Step 2: Create Migration Scripts (Priority 2)
- [ ] Create `scripts/migrate_sku_price_pack.py` (Script A)
- [ ] Create `scripts/build_catalog_chain_master.py` (Script B)
- [ ] Test on sample data
- [ ] Document migration process

### Step 3: Review and Archive (Priority 3)
- [ ] Review `output/` directory
- [ ] Create archive structure
- [ ] Pass freeze gate checklist

### Step 4: Migrate Active Data (Priority 4)
- [ ] Run Script A: `migrate_sku_price_pack.py`
- [ ] Run Script B: `build_catalog_chain_master.py`
- [ ] Validate migrated data
- [ ] Create new master workbook

### Step 5: Clean and Document (Priority 5)
- [ ] Clean output directory
- [ ] Update documentation
- [ ] Create migration notes

---

## 10. References

- `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.1.md` - Terminology definitions
- `NSW_SHEET_SET_INDEX_v1.1.md` - Sheet structure definitions
- `FREEZE_DOCUMENTS_REVIEW.md` - Review and assessment

---

## 11. Decision Log

### Decision CLOSED: NSW_L1_CONFIG_LINES vs NSW_CATALOG_CHAIN_MASTER

**Status:** ✅ **CLOSED** - No further debate

**Decision:**
- `NSW_CATALOG_CHAIN_MASTER` is the **canonical L0/L1/L2 continuity sheet**
- `NSW_L1_CONFIG_LINES` is **legacy parse output** and becomes archive-ready after QC

**Rationale:**
- Catalog Chain Master has corrected semantics (no OEM series at L0/L1, Option B coil in L2)
- Legacy parse sheet has old structure (duty×voltage expansion)
- Rebuild from canonical is safer than migration

---

**Status:** ✅ PLAN COMPLETE v1.1 - READY FOR EXECUTION

**Critical:** Complete housekeeping BEFORE implementing freeze structure to avoid rework.

**Freeze Gate:** Must pass all checklist items before archiving.

