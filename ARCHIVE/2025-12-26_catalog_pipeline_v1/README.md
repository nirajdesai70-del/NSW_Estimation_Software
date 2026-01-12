# Archive: Catalog Pipeline v1 - December 26, 2025

## Date
2025-12-26

## Why Archived
This archive contains experimental runs, test outputs, and duplicate files from the initial catalog pipeline development work. The canonical workspace has been established and these files are preserved for traceability and reference.

## What Remains Canonical

The following paths remain active and canonical:

1. **Tools & Pipeline:**
   - `tools/catalog_pipeline/**` - Main normalization pipeline
   - `tools/catalog_pipeline/profiles/**` - YAML profiles for extraction
   - `tools/catalog_pipeline/input/final/**` - Final input files
   - `tools/catalog_pipeline/output/final/**` - Final normalized outputs

2. **Documentation:**
   - `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md` - Standard operating procedure
   - `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER_CATALOG_MASTER.md` - Master tracker
   - `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/*_WORK.md` - Work documentation files

3. **Backend:**
   - `backend/app/api/v1/endpoints/catalog.py` - Catalog API endpoint
   - `backend/app/models/catalog.py` - Catalog data models
   - Database migrations

4. **Canonical Artifacts:**
   - `Schneider_CANONICAL_TABLE_v3.xlsx`
   - `Schneider_tablewise_splits_v3.zip`

## What Was Archived

1. **Old Tooling** (`tools_old/`):
   - Previous normalization scripts outside the canonical pipeline
   - Debug and diagnostic scripts
   - Experimental tooling

2. **Evidence Runs** (`evidence_runs/`):
   - Test outputs, logs, and error files from experimental runs
   - Files created during development and testing
   - Outputs from non-canonical paths

3. **Documentation Drafts** (`docs_drafts/`):
   - Draft documentation files
   - Temporary analysis files

4. **Duplicates** (`duplicates/`):
   - Multiple CSV outputs for the same product family with different timestamps
   - Older profile versions (keeping only frozen v1 and latest)
   - Redundant test outputs

## Archive Structure

```
ARCHIVE/2025-12-26_catalog_pipeline_v1/
├── tools_old/          # Old tooling and experimental scripts
├── evidence_runs/      # Test outputs, logs, errors
├── docs_drafts/        # Draft documentation
├── duplicates/         # Duplicate files from canonical workspace
├── README.md           # This file
└── ARCHIVE_INDEX.md    # Detailed index of archived items
```

## Notes

- All files were **COPIED** (not moved) to preserve originals
- Canonical workspace remains fully functional
- No deletions were performed
- All archived files are preserved for traceability

