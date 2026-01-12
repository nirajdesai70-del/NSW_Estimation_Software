# CATALOG PDF/XLSX → CSV → IMPORT SOP

**Status:** CANONICAL (v1.0)  
**Owner:** Catalog Pipeline Track (Pre-Phase-5)  
**Purpose:** Standardize OEM catalog conversion into NSW canonical CSV + controlled import (TEST → FINAL).  
**Scope:** All OEMs (Schneider first), all product families.

---

## 0. Core Principle

**Catalog pricing truth = SKU-level**  
- CatalogItem = grouping/browse (L1)
- CatalogSku = purchasable SKU (pricing truth)
- SkuPrice = append-only archive
- CatalogSku.current_price = fast quoting snapshot (Option-1)

---

## 1. Governance Rules (Non-negotiable)

### 1.1 TEST vs FINAL
- **TEST** = calibration only (disposable)
- **FINAL** = frozen artifact (importable once)
- Never modify FINAL in place.
- Any update requires a **new FINAL** file/date.

### 1.2 Profile versioning
- Profiles are versioned: `*_v1.yml`, `*_v2.yml`, etc.
- FINAL imports must reference a specific profile version.
- Never edit a profile that has produced a FINAL import; create a new version.

### 1.3 Single pipeline
All catalog updates must go through the same pipeline:
**PDF/XLSX → Normalizer → CSV → Import API**
No manual DB edits, no alternate scripts.

### 1.4 Audit requirements
Every commit import must store:
- source_file name
- import_batch_id
- append-only price archive row(s)
- current price snapshot update timestamp

---

## 2. Folder Structure (Standard)

See: `tools/catalog_pipeline/` (canonical tooling root)

- `input/raw/`   → original source artifacts (PDF/XLSX)
- `input/test/`  → TEST calibration copies
- `input/final/` → FINAL frozen copies
- `profiles/`    → versioned YAML profiles
- `output/test/` → test CSVs
- `output/final/`→ final CSVs (importable)
- `errors/`      → error sheets
- `logs/`        → summary JSON

---

## 3. Canonical CSV Contract (Import Schema)

**CSV header (v1):**
`import_stage,make,series,sku_code,description,uom,list_price,currency,notes`

### Required columns
- make
- sku_code
- uom
- list_price
- currency

### Recommended columns
- series (used for CatalogItem auto-grouping)
- description
- import_stage (must be FINAL for commit)

### Hard rules
- `(make, sku_code)` must be unique after normalization
- `list_price` numeric >= 0
- `currency` 3-letter code (INR, USD, …)
- `sku_code` must contain letters and be length ≥ 3

---

## 4. Normalization Process (Per Family)

### Step A — Source intake (RAW)
1. Place PDF/XLSX in `tools/catalog_pipeline/input/raw/<oem>/<family>/`
2. Record source date (WEF / revision date) in family WORK file.

### Step B — Create/Select Profile (vN)
1. Create profile file in `tools/catalog_pipeline/profiles/<oem>/`
2. Run TEST normalization until pass criteria met.

### Step C — TEST run
- Produce TEST CSV + errors + summary.
- Iterate profile until PASS.

### Step D — FINAL freeze
1. Copy XLSX into `input/final/<oem>/<family>/`
2. Name must include OEM + family + FINAL + date.
3. Run FINAL normalization → FINAL CSV.

---

## 5. Import Process (API)

### Dry-run (mandatory)
- `POST /api/v1/catalog/skus/import?dry_run=true`
- Must return `rows_error=0`

### Commit (only after clean dry-run)
- `POST /api/v1/catalog/skus/import?dry_run=false`
- Enforces FINAL-only imports

### DB behavior (v1)
- Auto-create CatalogItem grouped by `(make, series)`
- Upsert CatalogSku by `(make, sku_code)` (last-wins)
- Append SkuPrice row (archive)
- Update CatalogSku.current_price snapshot

---

## 6. PASS Criteria (Promotion to FINAL)

A family can be promoted to FINAL when:
- SKU validity: invalid SKUs < 1% of candidate rows
- prices: 99%+ numeric, no obvious noise
- series coverage: 95%+ (or profile-defined)
- reproducible output count across re-runs
- scope filter confirms family-only output (no bleed)

---

## 7. Exit Criteria (Schneider completion track)

This track is complete when:
- All targeted Schneider families have FINAL CSV(s)
- All FINAL CSVs imported successfully
- SOP remains stable and reusable for other OEMs

---

## 8. Phase-5 Extension Note (Planned)

A Phase-5 UI module will wrap this pipeline:
Upload PDF/XLSX → select profile → preview (dry-run) → commit (FINAL)

No alternate price-update paths will be allowed.

