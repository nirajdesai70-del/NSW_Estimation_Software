# <SERIES> Catalog Pipeline - Active Work

**Status**: 🟡 IN PROGRESS  
**WEF Date**: <WEF_YYYY-MM-DD>  
**Version**: v<VERSION>

---

## What This Is

This is the active working directory for converting the `<SERIES>` catalog series into NSW format. This folder contains work-in-progress files and should be archived to `archives/schneider/<SERIES>/<WEF>/` once frozen.

---

## Folder Structure

```
<SERIES>/
├── README.md                    # This file
├── run_pipeline.sh              # One-command pipeline execution
├── 00_inputs/                   # Raw input files
│   ├── <INPUT_FILE>.xlsx
│   └── <INPUT_FILE>.pdf
├── 01_working/                  # Intermediate working files
│   └── (temporary files)
├── 02_outputs/                  # Generated outputs
│   ├── <SERIES>_CANONICAL_v<VERSION>.xlsx
│   ├── <SERIES>_L2_tmp.xlsx
│   ├── <SERIES>_L1_tmp.xlsx
│   └── NSW_<SERIES>_WEF_<WEF>_v<VERSION>.xlsx
├── 03_qc/                       # Quality control
│   └── QC_SUMMARY.md            # QC checklist (copy from template)
└── 04_docs/                     # Documentation
    └── (any series-specific notes)
```

---

## Quick Start

### 1. Prepare Input Files

Place your pricelist files in `00_inputs/`:
- `<INPUT_FILE>.xlsx` (required)
- `<INPUT_FILE>.pdf` (optional, for reference)

### 2. Configure Pipeline

Edit `run_pipeline.sh` and set:
- `SERIES="<SERIES>"`
- `WEF="<WEF_YYYY-MM-DD>"`
- `INPUT_FILE_NAME="<INPUT_FILE>.xlsx"`

### 3. Run Pipeline

```bash
cd active/schneider/<SERIES>/
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### 4. Review Outputs

Check outputs in `02_outputs/`:
- Canonical extraction
- L2 products
- L1 configuration lines
- NSW master workbook

### 5. Run QC Checks

Copy `templates/QC_SUMMARY_TEMPLATE.md` to `03_qc/QC_SUMMARY.md` and fill it out.

### 6. Freeze Process

Once QC passes:
1. Upload final NSW file + QC summary to ChatGPT for review
2. Get ✅ "OK to freeze" approval
3. Archive to `archives/schneider/<SERIES>/<WEF>/`
4. Commit with message: `freeze(<SERIES>): WEF <WEF> v<VERSION> canonical + QC`

---

## Series-Specific Notes

**<Add any series-specific extraction rules, special cases, or notes here>**

---

## Canonical Rules Applied

- ✅ FRAME carry-forward (if applicable)
- ✅ KW range uses minimum
- ✅ Priced-only filtering
- ✅ Duty normalization (AC1/AC3)
- ✅ Voltage normalization (variant system)
- ✅ No SKU explosion

---

## Scripts Used

- `inspect_<series>_raw.py` - Raw input inspection
- `<series>_extract_canonical.py` - Canonical extraction
- `build_l2_from_canonical.py` - L2 generation
- `derive_l1_from_l2.py` - L1 generation
- `build_master_workbook.py` - NSW format assembly

---

## References

- **Operating Model**: `../../OPERATING_MODEL.md`
- **Next Series Bootstrap**: `../../NEXT_SERIES_BOOTSTRAP.md`
- **QC Template**: `../../templates/QC_SUMMARY_TEMPLATE.md`

---

**Last Updated**: <DATE>

