# Catalog Pipeline v2 - Standardized Structure Setup Complete

**Date**: 2025-01-XX  
**Status**: ✅ COMPLETE

---

## What Was Created

This setup implements the standardized catalog conversion pipeline structure based on the LC1E canonical model (frozen v6). The structure enables repeatable, fast conversion of new series (LC1D, LC1F, MCCB, ACB, etc.) with minimal rework.

---

## New Structure

### 1. Standardized Folders

```
catalog_pipeline_v2/
├── active/                       # 🟡 Work in progress
│   └── schneider/               # Ready for new series
│
├── archives/                     # ✅ Frozen history
│   └── schneider/
│       └── LC1E/                # LC1E already archived here
│
├── templates/                    # ✅ Reusable templates
│   ├── QC_SUMMARY_TEMPLATE.md
│   ├── run_pipeline.sh
│   └── README_ACTIVE_SERIES.md
│
├── OPERATING_MODEL.md            # ✅ Operating model (Cursor + ChatGPT)
└── NEXT_SERIES_BOOTSTRAP.md     # ✅ Bootstrap guide
```

---

## Key Documents

### Operating Model (`OPERATING_MODEL.md`)

Defines the dual-lane architecture:
- **Cursor** = Execution lane (scripts, generation, commits)
- **ChatGPT** = Governance lane (rules, review, freeze approval)

**Workflow:**
1. Cursor generates outputs
2. Upload to ChatGPT for review
3. Get approval
4. Freeze and archive

---

### Next Series Bootstrap (`NEXT_SERIES_BOOTSTRAP.md`)

Step-by-step checklist for converting new series:
- Before you start
- L2 setup
- L1 rules (duty/voltage normalization)
- Pricing structure
- Variant system
- Special cases
- QC checklist
- Freeze process

**Goal:** New series conversion takes < 20% of LC1E effort.

---

### Templates

#### `templates/QC_SUMMARY_TEMPLATE.md`

Standard QC checklist covering:
- Row counts (canonical, L2, L1, variants)
- Sanity checks (frame, duty, voltage, pricing)
- Validation status
- Freeze readiness

#### `templates/run_pipeline.sh`

One-command pipeline execution script:
- Configurable (SERIES, WEF, INPUT_FILE)
- Runs all pipeline steps
- Produces canonical + NSW format outputs
- Ready to customize per series

#### `templates/README_ACTIVE_SERIES.md`

Template README for active series work:
- Quick start guide
- Folder structure
- Series-specific notes
- References

---

## How to Use for Next Series

### Example: Converting LC1D

```bash
# 1. Create active series folder
cd tools/catalog_pipeline_v2/active/schneider/
mkdir -p LC1D/{00_inputs,01_working,02_outputs,03_qc,04_docs}
cd LC1D

# 2. Copy templates
cp ../../templates/run_pipeline.sh ./
cp ../../templates/README_ACTIVE_SERIES.md ./README.md
cp ../../templates/QC_SUMMARY_TEMPLATE.md ./03_qc/QC_SUMMARY.md

# 3. Customize run_pipeline.sh
# Edit: SERIES="LC1D", WEF="2025-XX-XX", INPUT_FILE_NAME="..."

# 4. Place input files
cp /path/to/input.xlsx ./00_inputs/

# 5. Run pipeline
chmod +x run_pipeline.sh
./run_pipeline.sh

# 6. Fill QC checklist
# Edit 03_qc/QC_SUMMARY.md

# 7. Upload to ChatGPT for review
# Upload: 02_outputs/NSW_LC1D_WEF_..._v1.xlsx + 03_qc/QC_SUMMARY.md

# 8. After approval, archive
cd ../..
mkdir -p archives/schneider/LC1D/<WEF>/
mv active/schneider/LC1D/* archives/schneider/LC1D/<WEF>/

# 9. Commit
git add archives/schneider/LC1D/
git commit -m "freeze(LC1D): WEF <WEF> v1 canonical + QC"
```

---

## Key Principles (Locked)

### 1. Catalog-First Principle
Follow catalog semantics exactly (frame carry-forward, priced-only).

### 2. Separation of Concerns
- **L2** = Identity (stable, no price/voltage/duty)
- **L1** = Configuration + engineering meaning
- **Price Matrix** = Commercial variation (changes with price updates)

### 3. No SKU Explosion
Voltage & duty do not create new products.

### 4. Symmetric Selection Model
Duty and Voltage behave the same (both are selection dimensions).

### 5. Variant System
- Variant Master defines variants
- Product-Variant mapping drives UI dropdowns
- Prices only in Price Matrix

---

## Standard Sheets (Must Exist)

Every NSW series file must contain:

**Required:**
- `NSW_L0_TEMPLATE`
- `NSW_L0_L2_ELIGIBILITY`
- `NSW_L2_PRODUCTS`
- `NSW_VARIANT_MASTER`
- `NSW_PRODUCT_VARIANTS`
- `NSW_PRICE_MATRIX`
- `NSW_L1_CONFIG_LINES`

**Canonical (series-specific):**
- `<SERIES>_CANONICAL_ROWS`
- `<SERIES>_COIL_CODE_PRICES`
- `<SERIES>_ACCESSORY_SKUS`

---

## Naming Conventions

### Input Files
- `Switching_All_WEF_<DATE>.xlsx`
- `Switching_All_WEF_<DATE>.pdf`

### Output Files
- Canonical: `<SERIES>_CANONICAL_v<X>.xlsx`
- NSW Format: `NSW_<SERIES>_WEF_<YYYY-MM-DD>_v<X>.xlsx`
- QC: `QC_SUMMARY.md`

---

## Success Metrics

✅ **Speed:** New series conversion < 20% of LC1E effort  
✅ **Consistency:** All series follow same structure  
✅ **Auditability:** Every freeze has ChatGPT sign-off  
✅ **Traceability:** Complete history in archives

---

## References

- **LC1E Canonical Model**: `archives/schneider/LC1E/2025-07-15_WEF/README.md`
- **LC1E QC Summary**: `archives/schneider/LC1E/2025-07-15_WEF/03_qc/QC_SUMMARY.md`
- **Operating Model**: `OPERATING_MODEL.md`
- **Bootstrap Guide**: `NEXT_SERIES_BOOTSTRAP.md`

---

## Next Steps

1. ✅ Structure created
2. ✅ Templates ready
3. ✅ Documentation complete
4. 🔄 **Ready for next series conversion**

**To start a new series:**
- Follow `NEXT_SERIES_BOOTSTRAP.md`
- Use templates from `templates/`
- Follow operating model in `OPERATING_MODEL.md`

---

**Status**: ✅ SETUP COMPLETE - Ready for use

