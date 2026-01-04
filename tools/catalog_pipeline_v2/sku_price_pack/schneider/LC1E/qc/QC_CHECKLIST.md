# Freeze Gate Checklist - QC Evidence

**Date:** 2025-01-XX  
**Status:** IN PROGRESS  
**Purpose:** Mandatory quality gates before archiving legacy files

---

## ⚠️ Acceptance Criteria

**Freeze gate is PASSED only when every checkbox is ✅ and evidence links are recorded in `qc/QC_EXPORTS/`**

---

## Freeze Gate Checklist

### 1. Price QC Count Stable

- [ ] Price QC count verified
- [ ] Missing prices are "not in price list" (not data loss)
- [ ] Evidence file: `qc/QC_EXPORTS/price_qc_report.xlsx` or `.md`

**Status:** ⬜ PENDING  
**Evidence:** _Link to evidence file_

---

### 2. SKU Master Completeness Check

- [ ] SKU master completeness check passes
- [ ] All SKUs from legacy workbook accounted for
- [ ] No orphan SKUs
- [ ] Evidence file: `qc/QC_EXPORTS/sku_completeness_check.xlsx` or `.md`

**Status:** ⬜ PENDING  
**Evidence:** _Link to evidence file_

---

### 3. Chain Master Validated

- [ ] Chain master sample rows reviewed and approved
- [ ] L0/L1/L2 structure correct
- [ ] No OEM series at L0/L1
- [ ] Coil voltage not in L1 (Option B verified)
- [ ] Evidence file: `qc/QC_EXPORTS/chain_master_validation.xlsx` or `.md`

**Status:** ⬜ PENDING  
**Evidence:** _Link to evidence file_

---

### 4. Freeze Docs v1.1 Committed

- [ ] `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.1.md` in `freeze_docs/`
- [ ] `NSW_SHEET_SET_INDEX_v1.1.md` in `freeze_docs/`
- [ ] `FREEZE_IMPLEMENTATION_SUMMARY_v1.1.md` in `freeze_docs/`
- [ ] `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` in `freeze_docs/`
- [ ] `ARCHIVE_QUICK_REFERENCE_v1.1.md` in `freeze_docs/`
- [ ] `ARCHIVE_PLAN_v1.0_TO_v1.1_DIFF.md` in `freeze_docs/`

**Status:** ⬜ PENDING  
**Evidence:** _List of files in freeze_docs/_

---

### 5. Sheet Index v1.1 Aligns to Actual Workbook

- [ ] Sheet index matches actual workbook structure
- [ ] All sheets listed in index exist in workbook
- [ ] No unexpected sheets in workbook
- [ ] Evidence file: `qc/QC_EXPORTS/sheet_index_verification.xlsx` or `.md`

**Status:** ⬜ PENDING  
**Evidence:** _Link to evidence file_

---

### 6. Migration Scripts Tested

- [ ] Script A (`migrate_sku_price_pack.py`) tested on sample data
- [ ] Script B (`build_catalog_chain_master.py`) tested on sample data
- [ ] Both scripts produce expected output
- [ ] Evidence file: `qc/QC_EXPORTS/migration_script_test_results.md`

**Status:** ⬜ PENDING  
**Evidence:** _Link to evidence file_

---

### 7. Data Integrity Verified

- [ ] Row counts match (no data loss)
- [ ] Column mappings verified
- [ ] Data types correct
- [ ] Evidence file: `qc/QC_EXPORTS/data_integrity_report.xlsx` or `.md`

**Status:** ⬜ PENDING  
**Evidence:** _Link to evidence file_

---

## Overall Status

**Freeze Gate Status:** ⬜ NOT PASSED

**All items must be ✅ before proceeding to archive.**

---

## Evidence Files Location

All evidence files should be saved in: `qc/QC_EXPORTS/`

**Required Evidence Files:**
1. `price_qc_report.xlsx` or `.md`
2. `sku_completeness_check.xlsx` or `.md`
3. `chain_master_validation.xlsx` or `.md`
4. `sheet_index_verification.xlsx` or `.md`
5. `migration_script_test_results.md`
6. `data_integrity_report.xlsx` or `.md`

---

## Next Steps

Once all items are ✅:
1. Update this checklist with all evidence links
2. Mark overall status as ✅ PASSED
3. Proceed with archive actions per `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md`

---

**Last Updated:** 2025-01-XX


