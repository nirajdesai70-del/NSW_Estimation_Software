# Catalog Pipeline — PDF/XLSX → CSV → Import

**Status:** CANONICAL  
**Purpose:** Provide a standardized, repeatable pipeline to convert OEM catalog price lists into NSW canonical CSV format and import them safely into the system.

This pipeline is used:
- Today as a tooling workflow (CLI-driven)
- Later as the backbone of Phase-5 Catalog Price Maintenance UI

---

## 1. What This Pipeline Does

This pipeline converts OEM price catalogs into import-ready CSVs with strict governance.

End-to-end flow:

```
PDF / XLSX
   ↓
Normalization (profile-based)
   ↓
TEST CSV (calibration)
   ↓
FINAL CSV (frozen)
   ↓
Import API (archive + snapshot)
```

No shortcuts. No manual DB edits.

---

## 2. Canonical Folder Structure

```
tools/catalog_pipeline/
├── input/
│   ├── raw/        # Original source files (PDF/XLSX)
│   ├── test/       # TEST copies used during calibration
│   └── final/      # FINAL frozen source files (immutable)
│
├── profiles/       # Versioned YAML profiles
│   ├── schneider/
│   └── _template_oem_profile.yml
│
├── output/
│   ├── test/       # TEST CSV outputs
│   └── final/      # FINAL CSV outputs (importable)
│
├── errors/         # Error spreadsheets (row-level issues)
│   ├── test/
│   └── final/
│
├── logs/           # Summary JSON (counts, coverage, metrics)
│   ├── test/
│   └── final/
│
├── normalize.py    # Canonical normalizer script
└── README.md       # This file
```

---

## 3. Folder Responsibilities (Do Not Mix)

### input/raw/
- Original OEM artifacts
- PDFs, official XLSX exports
- Never edited (reference only)

### input/test/
- Copies of raw files for TEST runs
- Can be overwritten or deleted
- Used for profile tuning

### input/final/
- FINAL frozen sources
- Naming must include:

```
<OEM>_<FAMILY>_FINAL_<YYYY-MM-DD>.xlsx
```

- Never modify after creation

### profiles/
- YAML files defining how to interpret a catalog
- Versioned (_v1, _v2, …)
- One profile per OEM + product family
- FINAL imports must reference a specific profile version

### output/test/
- Disposable CSVs
- Used only for verification
- May change between runs

### output/final/
- Import-ready CSVs
- Produced only from FINAL input
- Imported once into DB

### errors/
- Row-level failures:
  - invalid SKU
  - missing price
  - malformed rows
- Used to tune profiles
- Should be near-empty before FINAL

### logs/
- Machine-readable summary JSON
- Includes:
  - row counts
  - invalid SKU counts
  - series coverage
  - reproducibility metrics
- Used for audit and SOP derivation

---

## 4. TEST vs FINAL (Critical Governance)

### TEST Mode
- Purpose: calibration
- Unlimited re-runs
- No DB writes
- Output is disposable

### FINAL Mode
- Purpose: canonical import
- Frozen artifacts
- Imported once
- Append-only price history

**Rule:**  
If a file is FINAL, it must never be re-imported or modified.

---

## 5. Normalizer Usage

### TEST run

```bash
python normalize.py \
  --profile profiles/<oem>/<profile>.yml \
  --file input/test/<oem>/<family>/<file>.xlsx \
  --mode test
```

### FINAL run

```bash
python normalize.py \
  --profile profiles/<oem>/<profile>_v1.yml \
  --file input/final/<oem>/<family>/<FINAL_file>.xlsx \
  --mode final
```

---

## 6. Import Process (API)

### Dry-run (mandatory)

```bash
POST /api/v1/catalog/skus/import?dry_run=true
```

### Commit (only if dry-run passes)

```bash
POST /api/v1/catalog/skus/import?dry_run=false
```

### Behavior:
- Auto-create CatalogItem (grouped by series)
- Upsert CatalogSku (make + sku_code)
- Append SkuPrice (price archive)
- Update CatalogSku.current_price snapshot

---

## 7. What This Pipeline Guarantees

- SKU-level pricing truth
- Full historical price audit
- Deterministic imports
- Zero manual intervention
- Compatibility with:
  - BOM engines
  - Quotation engines
  - Pricing packs
  - Phase-5 UI

---

## 8. Relationship to Documentation

This pipeline is governed by:
- **SOP:**  
  `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md`
- **OEM Tracker:**  
  `docs/PHASE_5/INPUT_ASSETS/<OEM>_CATALOG_MASTER.md`
- **Per-Family Work Files:**  
  `docs/PHASE_5/INPUT_ASSETS/<OEM>/<FAMILY>_WORK.md`

The README explains how to use the tool.  
The SOP explains why rules exist.

---

## 9. Phase-5 Extension (Planned)

This pipeline will be wrapped by a Catalog Price Maintenance UI in Phase-5:

| Tooling Today | Phase-5 UI |
|--------------|------------|
| input/raw | File upload |
| profiles | Profile selector |
| normalize (test) | Preview |
| output/test | Table preview |
| normalize (final) | Confirm |
| import API | Commit |

No alternate update paths will exist.

---

## 10. Final Rule

**If it doesn't go through this pipeline,  
it does not enter the catalog.**

