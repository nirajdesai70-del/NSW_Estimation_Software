# Archive Quick Reference - What to Archive Before Freeze v1.1

**Date:** 2025-01-XX  
**Status:** QUICK REFERENCE v1.1 (FINAL - FROZEN)  
**Purpose:** Quick checklist of what to archive before implementing freeze structure

---

## ⚠️ SCOPE LOCK

**This migration applies only to the SKU + Price Creation Pack.**

It does **NOT** implement estimation runtime logic (feature explosion, BOM, quotation rules).

---

## ✅ ANSWER: Do You Need to Redo Everything?

**NO** - Most work can be **MIGRATED**, not redone.

**What Can Be Migrated:**
- ✅ SKU data (legacy `NSW_L2_PRODUCTS` → `NSW_SKU_MASTER_CANONICAL`)
- ✅ Price data (`NSW_PRICE_MATRIX` → `NSW_PRICE_MATRIX_CANONICAL`)
- ✅ Ratings data (→ `NSW_SKU_RATINGS` - already generated)
- ✅ Accessory SKU data (→ `NSW_ACCESSORY_SKU_MASTER`)

**What Needs Rework (Limited):**
- ⚠️ Catalog Chain Master - Must be **rebuilt** from canonical (not migrated)
  - Reason: L0/L1 naming rules corrected (no OEM series at L0/L1; Option B coil in L2)

**What Needs Archive (Not Migration):**
- ⚠️ Legacy parse sheets (`NSW_L1_CONFIG_LINES` - old format)
- ⚠️ Legacy compat sheets (`NSW_L2_PRODUCTS` - legacy parse/compat output, not authoritative)
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
- `migrate_sku_price_pack.py` (NEW: Script A)
- `build_catalog_chain_master.py` (NEW: Script B)

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
├── sku_price_pack/             # NEW: Single authoritative SKU+Price pack
│   └── schneider/
│       └── LC1E/
│           ├── NSW_SKU_PRICE_PACK_MASTER.xlsx   # Single authoritative workbook
│           │   ├── NSW_SKU_MASTER_CANONICAL (authoritative)
│           │   ├── NSW_PRICE_MATRIX_CANONICAL (authoritative)
│           │   ├── NSW_CATALOG_CHAIN_MASTER (rebuilt, not migrated)
│           │   ├── NSW_SKU_RATINGS (already generated)
│           │   └── ...
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

- [ ] Finalize freeze docs v1.1 (Terminology, Sheet Index, Implementation Summary)
- [ ] Create migration scripts (Script A: migrate_sku_price_pack.py, Script B: build_catalog_chain_master.py)
- [ ] Test migration scripts on sample data
- [ ] Review `output/` directory
- [ ] Identify files to archive
- [ ] Create `PRE_FREEZE_ARCHIVE/` structure
- [ ] Pass freeze gate checklist:
  - [ ] Price QC count stable
  - [ ] SKU master completeness check passes
  - [ ] Chain master validated (sample rows approved)
  - [ ] Freeze docs v1.1 committed
  - [ ] Sheet index v1.1 aligns to actual workbook
- [ ] Run Script A: migrate SKU + price + ratings + accessories
- [ ] Run Script B: rebuild catalog chain master
- [ ] Validate migrated data (row counts, no data loss)
- [ ] Move legacy outputs to archive
- [ ] Move temporary files to archive
- [ ] Move rebuild tests to archive
- [ ] Update documentation

---

## 🎯 Migration vs Archive Decision Tree

```
Is it source data?
├─ YES → Keep in input/ (no change)
└─ NO → Is it in correct format?
    ├─ YES → Can it be migrated?
    │   ├─ YES → Is it Catalog Chain?
    │   │   ├─ YES → Rebuild (Script B) - semantic corrections needed
    │   │   └─ NO → Migrate (Script A) - deterministic migration
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
| Legacy Parse Sheets | `NSW_L1_CONFIG_LINES`, `NSW_L2_PRODUCTS` | Archive after QC | `PRE_FREEZE_ARCHIVE/00_legacy_outputs/` |
| Source Files | Pricelist XLSX/PDF | Keep | `input/` (unchanged) |
| Active Scripts | Current scripts | Keep | `scripts/` (may need updates) |
| Canonical Data | Extraction output | Migrate/Rebuild | `sku_price_pack/` (new location) |

---

## ⚠️ Critical: Do This First

1. **Finalize freeze docs v1.1** - Must be committed before migration
2. **Create migration scripts** - Script A (migrate) and Script B (rebuild)
3. **Test migration scripts** - On sample data before archiving
4. **Pass freeze gate checklist** - All items must pass
5. **Backup active data** - Before any moves
6. **Validate migration** - Ensure no data loss
7. **Then archive** - After successful migration

---

## 🔧 Two Migration Scripts

### Script A: `migrate_sku_price_pack.py`
- **Purpose:** Migrate SKU + Price + Ratings + Accessories (deterministic)
- **Input:** Legacy workbook with `NSW_L2_PRODUCTS`, `NSW_PRICE_MATRIX`
- **Output:** `NSW_SKU_MASTER_CANONICAL`, `NSW_PRICE_MATRIX_CANONICAL`, etc.
- **Status:** ✅ Deterministic - No semantic changes

### Script B: `build_catalog_chain_master.py`
- **Purpose:** Rebuild Catalog Chain Master (not migration)
- **Input:** Canonical extraction
- **Output:** `NSW_CATALOG_CHAIN_MASTER` (with corrected semantics)
- **Status:** ⚠️ Rebuild required - Semantic corrections applied

---

## 📋 Freeze Gate Checklist (MANDATORY)

**Before archiving, ALL must pass:**

- [ ] Price QC count stable (missing prices are "not in price list")
- [ ] SKU master completeness check passes
- [ ] Chain master validated (sample rows approved)
- [ ] Freeze docs v1.1 committed in `freeze_docs/`
- [ ] Sheet index v1.1 aligns to actual workbook
- [ ] Migration scripts tested and validated
- [ ] Data integrity verified (row counts match, no data loss)

---

## 🎯 Key Decisions (CLOSED)

### Decision: NSW_L2_PRODUCTS Status
- **Status:** ✅ CLOSED
- **Decision:** `NSW_L2_PRODUCTS` is **legacy parse/compat output**, not authoritative
- **Authoritative:** `NSW_SKU_MASTER_CANONICAL` is the canonical SKU list

### Decision: NSW_L1_CONFIG_LINES vs NSW_CATALOG_CHAIN_MASTER
- **Status:** ✅ CLOSED
- **Decision:** `NSW_CATALOG_CHAIN_MASTER` is canonical (rebuilt with corrected semantics)
- **Legacy:** `NSW_L1_CONFIG_LINES` is legacy parse output (archive after QC)

---

**Reference:** See `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` for detailed plan.


