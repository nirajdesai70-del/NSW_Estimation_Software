# Execution Status - Archive and Migration Plan

**Date:** 2025-01-XX  
**Status:** IN PROGRESS  
**Current Phase:** Setup Complete - Ready for Migration

---

## ✅ Completed

### Phase 1: Setup (COMPLETE)

- [x] Created `sku_price_pack/` folder structure
- [x] Created `freeze_docs/` subfolder
- [x] Created `qc/` subfolder with `QC_EXPORTS/`
- [x] Moved v1.1 documents to `freeze_docs/`:
  - [x] `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md`
  - [x] `ARCHIVE_QUICK_REFERENCE_v1.1.md`
  - [x] `ARCHIVE_PLAN_v1.0_TO_v1.1_DIFF.md`
- [x] Created Script A: `migrate_sku_price_pack.py`
- [x] Created Script B: `build_catalog_chain_master.py`
- [x] Created `QC_CHECKLIST.md`
- [x] Created `ARCHIVE_INDEX.md` template

---

## ⚠️ In Progress

### Phase 2: Migration Scripts (READY FOR TESTING)

- [ ] Test Script A on sample data
- [ ] Test Script B on sample data
- [ ] Validate migration output
- [ ] Document test results in `qc/QC_EXPORTS/`

---

## 📋 Next Steps

### Phase 3: Freeze Gate Checklist

1. Run Script A: `migrate_sku_price_pack.py`
2. Run Script B: `build_catalog_chain_master.py`
3. Complete freeze gate checklist:
   - [ ] Price QC count stable
   - [ ] SKU master completeness check
   - [ ] Chain master validated
   - [ ] Freeze docs v1.1 committed
   - [ ] Sheet index v1.1 aligns
   - [ ] Migration scripts tested
   - [ ] Data integrity verified
4. Save all evidence in `qc/QC_EXPORTS/`

### Phase 4: Archive

1. Create `PRE_FREEZE_ARCHIVE/` structure
2. Move legacy files to archive
3. Update `ARCHIVE_INDEX.md`
4. Clean output directory

---

## 📁 Current Structure

```
tools/catalog_pipeline_v2/
├── sku_price_pack/
│   └── schneider/
│       └── LC1E/
│           ├── freeze_docs/          ✅ Created
│           │   ├── ARCHIVE_AND_MIGRATION_PLAN_v1.1.md
│           │   ├── ARCHIVE_QUICK_REFERENCE_v1.1.md
│           │   └── ARCHIVE_PLAN_v1.0_TO_v1.1_DIFF.md
│           ├── qc/                   ✅ Created
│           │   ├── QC_CHECKLIST.md
│           │   └── QC_EXPORTS/
│           └── ARCHIVE_INDEX.md      ✅ Created
│
├── scripts/
│   ├── migrate_sku_price_pack.py     ✅ Created (Script A)
│   └── build_catalog_chain_master.py   ✅ Created (Script B)
│
└── archives/
    └── schneider/
        └── LC1E/
            └── 2025-07-15_WEF/
                └── PRE_FREEZE_ARCHIVE/  ⬜ To be created
```

---

## 🎯 Execution Commands

### Test Script A

```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2

python3 scripts/migrate_sku_price_pack.py \
  --legacy_workbook "output/NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx" \
  --output "sku_price_pack/schneider/LC1E/NSW_SKU_PRICE_PACK_MASTER.xlsx" \
  --validate
```

### Test Script B

```bash
python3 scripts/build_catalog_chain_master.py \
  --canonical "output/lc1e/LC1E_CANONICAL_v1.xlsx" \
  --output_workbook "sku_price_pack/schneider/LC1E/NSW_SKU_PRICE_PACK_MASTER.xlsx" \
  --validate
```

---

## ⚠️ Important Notes

1. **Freeze Gate Required:** All checklist items must pass before archiving
2. **Evidence Required:** All evidence files must be saved in `qc/QC_EXPORTS/`
3. **Backup First:** Create backup of active files before migration
4. **Test First:** Test scripts on sample data before full migration

---

**Status:** ✅ SETUP COMPLETE - READY FOR MIGRATION TESTING
