# Archive Index - Catalog Pipeline v1

**Date:** 2025-12-26  
**Archive Location:** `ARCHIVE/2025-12-26_catalog_pipeline_v1/`

---

## A) Archived Folders

| Source Path | Archived To | Reason |
|------------|-------------|--------|
| `tools/price_normalizer/` | `tools_old/price_normalizer/` | Old normalization tooling, superseded by `tools/catalog_pipeline/` |
| `tools/catalog_pipeline/tools/` | `tools_old/catalog_pipeline_nested_tools/` | Nested duplicate structure created during development |
| `tools/catalog_pipeline/tools/catalog_pipeline/output/` | `evidence_runs/catalog_pipeline_nested/output/` | Test outputs from nested structure |
| `tools/catalog_pipeline/tools/catalog_pipeline/logs/` | `evidence_runs/catalog_pipeline_nested/logs/` | Logs from nested structure |
| `tools/catalog_pipeline/tools/catalog_pipeline/errors/` | `evidence_runs/catalog_pipeline_nested/errors/` | Errors from nested structure |
| `tools/price_normalizer/output/` | `evidence_runs/price_normalizer_output/` | Old tool outputs |
| `tools/price_normalizer/logs/` | `evidence_runs/price_normalizer_logs/` | Old tool logs |
| `tools/price_normalizer/errors/` | `evidence_runs/price_normalizer_errors/` | Old tool errors |
| `tools/catalog_pipeline/output/test/` | `evidence_runs/catalog_pipeline_test_outputs/test/` | Test run outputs |
| `tools/catalog_pipeline/logs/` | `evidence_runs/catalog_pipeline_logs/` | Development logs |
| `tools/catalog_pipeline/errors/` | `evidence_runs/catalog_pipeline_errors/` | Development error files |

---

## B) Duplicates Copied

### LC1E Output Files

| File | Kept Canonical File | Archived Copy | Why |
|------|---------------------|---------------|-----|
| `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv` | `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_155038.csv` | `duplicates/lc1e_outputs/` | Older run (25 SKUs) - latest has 55 SKUs |
| `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_141842.csv` | `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_155038.csv` | `duplicates/lc1e_outputs/` | Older run (25 SKUs) - latest has 55 SKUs |
| `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_144045.csv` | `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_155038.csv` | `duplicates/lc1e_outputs/` | Older run (30 SKUs) - latest has 55 SKUs |
| `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_145040.csv` | `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_155038.csv` | `duplicates/lc1e_outputs/` | Older run (29 SKUs) - latest has 55 SKUs |

**Canonical:** `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_155038.csv` (55 SKUs - complete extraction)

### Profile Files

| File | Kept Canonical File | Archived Copy | Why |
|------|---------------------|---------------|-----|
| `schneider.yml` | `schneider_contactors_v2.yml` | `duplicates/profiles/` | Generic profile, superseded by specific profiles |
| `schneider_contactors.yml` | `schneider_contactors_v2.yml` | `duplicates/profiles/` | Older version, superseded by v2 |

**Canonical Profiles:**
- `schneider_contactors_v1.yml` - Frozen v1 (3P only, historical reference)
- `schneider_contactors_v2.yml` - Latest (all LC1E contactors)
- `schneider_lp1k_v1.yml` - LP1K profile (frozen)
- `schneider_lc1d_v1.yml` - LC1D profile (frozen)

---

## C) Canonical Confirmation

The following paths remain active and canonical:

### Tools & Pipeline
- ✅ `tools/catalog_pipeline/` - Main normalization pipeline
- ✅ `tools/catalog_pipeline/normalize.py` - Core normalization script
- ✅ `tools/catalog_pipeline/profiles/` - YAML profiles
  - `schneider_contactors_v1.yml` (frozen)
  - `schneider_contactors_v2.yml` (latest)
  - `schneider_lp1k_v1.yml` (frozen)
  - `schneider_lc1d_v1.yml` (frozen)
- ✅ `tools/catalog_pipeline/input/final/` - Final input files
- ✅ `tools/catalog_pipeline/output/final/` - Final normalized outputs
  - `schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_155038.csv` (55 SKUs)
  - `schneider_Schneider_LP1K_FINAL_2025-12-26_normalized_20251226_130950.csv` (6 SKUs)

### Documentation
- ✅ `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md` - Standard operating procedure
- ✅ `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER_CATALOG_MASTER.md` - Master tracker
- ✅ `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/*_WORK.md` - Work documentation
  - `SCHNEIDER_LP1K_WORK.md`
  - `SCHNEIDER_LC1E_WORK.md`
  - `SCHNEIDER_LC1D_WORK.md`
  - `LC1E_MISSING_SKUS_ANALYSIS.md`

### Backend
- ✅ `backend/app/api/v1/endpoints/catalog.py` - Catalog API endpoint
- ✅ `backend/app/models/catalog.py` - Catalog data models
- ✅ Database migrations (untouched)

### Canonical Artifacts
- ✅ `Schneider_CANONICAL_TABLE_v3.xlsx` (if exists)
- ✅ `Schneider_tablewise_splits_v3.zip` (if exists)

---

## Archive Statistics

- **Total folders archived:** 11+
- **Total files archived:** 620 files
  - `tools_old/`: 292 files
  - `evidence_runs/`: 322 files
  - `duplicates/`: 6 files
  - `docs_drafts/`: 0 files
- **Archive size:** ~66MB total
- **Canonical files preserved:** All active files remain in place
- **Deletions performed:** 0 (all files copied, not moved)

---

## Notes

1. All archived files are **copies** - originals remain in place until explicit approval for deletion
2. The nested `tools/catalog_pipeline/tools/` structure was created during development and is now archived
3. The latest LC1E extraction (55 SKUs) is the canonical version
4. Profile v1 files are kept as frozen references, v2 is the active version
5. Test outputs and logs are preserved for traceability but archived to keep workspace clean

---

## Next Steps (Optional)

After verification, you may choose to:
1. Delete the nested `tools/catalog_pipeline/tools/` structure (now archived)
2. Delete older LC1E CSV files (keeping only the latest)
3. Delete old profile files (keeping v1 frozen and latest active)
4. Clean up test outputs (now archived)

**⚠️ IMPORTANT:** No deletions have been performed. All files remain in their original locations.

