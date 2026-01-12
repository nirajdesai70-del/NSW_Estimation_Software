# Catalog Conversion Pipeline - Operating Model

**Version**: 1.0  
**Status**: ✅ LOCKED  
**Effective**: Phase-5 & onward

---

## Purpose

This document defines the operating model for catalog conversion in NSW. It establishes the separation of concerns between **Cursor (execution)** and **ChatGPT (governance)** to ensure speed, consistency, and auditability.

---

## Core Principle: Dual-Lane Architecture

### A) Cursor = Execution Lane (Where Work Happens)

**Use Cursor for:**
- ✅ Building/maintaining extraction + transformation scripts
- ✅ Generating canonical XLSX outputs
- ✅ Committing versioned files into the repo
- ✅ Running validations (counts, duplicates, missing variants)
- ✅ Producing repeatable "one command" pipelines

**Why:** It's closest to the codebase, data files, and future automation.

---

### B) ChatGPT = Governance + Review Lane (Where Truth Is Locked)

**Use ChatGPT for:**
- ✅ Locking rules (what is L0/L1/L2, selection dimensions, naming)
- ✅ Reviewing output samples and spotting semantic errors
- ✅ Deciding how to generalize across OEM series
- ✅ Documenting decisions (A9/A10 style) and freeze-gate readiness
- ✅ Creating the "canonical templates" like v6

**Why:** Avoids local context loss + gives consistent, audit-ready reasoning.

---

## Practical Workflow (Fast + Safe)

### Step 1 — Cursor Generates

**Actions:**
1. Run `run_pipeline.sh` in `active/schneider/<SERIES>/`
2. Pipeline produces:
   - `<SERIES>_CANONICAL_vX.xlsx` (canonical + NSW format)
   - `QC_SUMMARY.md` (counts, missing checks)

**Outputs:**
- `02_outputs/NSW_<SERIES>_WEF_<DATE>_vX.xlsx`
- `03_qc/QC_SUMMARY.md`

---

### Step 2 — Upload to ChatGPT

**Upload only 2 artifacts:**
1. The generated NSW file (vX)
2. The QC summary

**Ask ChatGPT:**
- "Review this NSW file and QC summary for <SERIES>"
- "Is this ready to freeze?"

---

### Step 3 — ChatGPT Signs Off

**ChatGPT returns:**
- ✅ "OK to freeze" OR
- ❌ "Fix these 3 issues: [list]"

**If fixes needed:**
- Return to Cursor
- Fix issues
- Re-run pipeline
- Re-upload to ChatGPT

---

### Step 4 — Cursor Freezes

**Actions:**
1. Move to archive:
   ```bash
   mv active/schneider/<SERIES> \
      archives/schneider/<SERIES>/<WEF>/
   ```

2. Commit with message:
   ```
   freeze(<SERIES>): WEF <WEF> vX canonical + QC
   ```

3. Tag version (optional):
   ```bash
   git tag <SERIES>-vX-<WEF>
   ```

---

## What NOT to Do (To Avoid Time Loss)

❌ **Don't keep doing extraction "by chat"**  
→ File I/O + script iteration belongs in Cursor.

❌ **Don't skip QC checklist**  
→ Every series must pass QC before ChatGPT review.

❌ **Don't freeze without ChatGPT approval**  
→ Governance lane must sign off.

❌ **Don't mix execution and governance**  
→ Keep lanes separate for clarity and speed.

---

## Standard Folder Structure

```
catalog_pipeline_v2/
├── active/                       # Execution lane (work in progress)
│   └── schneider/
│       └── <SERIES>/            # Active series work
│           ├── 00_inputs/
│           ├── 01_working/
│           ├── 02_outputs/
│           ├── 03_qc/
│           ├── 04_docs/
│           ├── run_pipeline.sh
│           └── README.md
│
├── archives/                     # Frozen history
│   └── schneider/
│       └── <SERIES>/
│           └── <WEF_YYYY-MM-DD>/
│               ├── 00_inputs/
│               ├── 01_scripts/
│               ├── 02_outputs/
│               ├── 03_qc/
│               ├── 04_docs/
│               ├── 05_decisions/
│               └── README.md
│
├── scripts/                      # Shared pipeline scripts
│   ├── build_l2_from_canonical.py
│   ├── derive_l1_from_l2.py
│   ├── build_master_workbook.py
│   └── <series>_extract_canonical.py
│
├── templates/                    # Reusable templates
│   ├── QC_SUMMARY_TEMPLATE.md
│   ├── run_pipeline.sh
│   └── README_ACTIVE_SERIES.md
│
├── OPERATING_MODEL.md            # This file
└── NEXT_SERIES_BOOTSTRAP.md     # Bootstrap guide
```

---

## Naming Conventions

### Input Files
- `Switching_All_WEF_<DATE>.xlsx`
- `Switching_All_WEF_<DATE>.pdf`

### Canonical Output
- `<SERIES>_CANONICAL_v<X>.xlsx`

### NSW Formatted Output
- `NSW_<SERIES>_WEF_<YYYY-MM-DD>_v<X>.xlsx`

### QC File
- `QC_SUMMARY.md` (or `QC_SUMMARY_v<X>.md`)

### Engineer Review Workbook
- `NSW_MASTER_SCHNEIDER_WEF_<YYYY-MM-DD>_ENGINEER_REVIEW.xlsx`

---

## Standard Sheets (Must Exist)

Every NSW series file must contain:

**Required Sheets:**
- `NSW_L0_TEMPLATE` - L0 intent templates
- `NSW_L0_L2_ELIGIBILITY` - L0→L2 eligibility mappings
- `NSW_L2_PRODUCTS` - L2 product identity (stable)
- `NSW_VARIANT_MASTER` - Variant definitions
- `NSW_PRODUCT_VARIANTS` - L2→variant allowed mappings
- `NSW_PRICE_MATRIX` - Price matrix
- `NSW_L1_CONFIG_LINES` - L1 configuration lines

**Canonical Extractor Sheets (series-specific):**
- `<SERIES>_CANONICAL_ROWS` - Base references
- `<SERIES>_COIL_CODE_PRICES` - Completed SKUs with prices
- `<SERIES>_ACCESSORY_SKUS` - Accessory SKUs (can be empty)

---

## QC Checklist (Must Pass Before Freeze)

Every series must pass these checks:

### A) Counts
- [ ] Base refs count (canonical rows)
- [ ] Price rows count (coil prices)
- [ ] L2 count
- [ ] Price matrix count
- [ ] L1 count (= price matrix × #duties unless duty not applicable)

### B) Rule Checks
- [ ] No bogus base refs
- [ ] Frame carry-forward applied (if catalog uses it)
- [ ] kW range policy applied (min rule + note)
- [ ] duty_current_A matches duty_class
- [ ] selected_voltage_* matches voltage_class_code
- [ ] Every L1 row has: duty_class, duty_current_A, voltage_class_code, selected_voltage_V/type, generic_descriptor

### C) Optional Checks
- [ ] Accessories extracted? (if not, explicitly say "not detected")
- [ ] RATING_MAP (if unused) explicitly say "unused; ratings embedded in L1"

---

## Decision Logging

**For major decisions:**
1. Document in `04_docs/` or `05_decisions/` (archived)
2. Update canonical rules if needed
3. Propagate to next series bootstrap guide

**Examples:**
- "LC1E uses duty × voltage expansion"
- "MCCB uses voltage-only (no duty expansion)"
- "ACB uses frame-based grouping"

---

## Success Metrics

✅ **Speed:** New series conversion takes < 20% of LC1E effort  
✅ **Consistency:** All series follow same structure  
✅ **Auditability:** Every freeze has ChatGPT sign-off  
✅ **Traceability:** Every archive has complete history

---

## References

- **LC1E Canonical Document**: `archives/schneider/LC1E/2025-07-15_WEF/README.md`
- **LC1E QC Summary**: `archives/schneider/LC1E/2025-07-15_WEF/03_qc/QC_SUMMARY.md`
- **Next Series Bootstrap**: `NEXT_SERIES_BOOTSTRAP.md`

---

**Status**: ✅ LOCKED - Ready for use

