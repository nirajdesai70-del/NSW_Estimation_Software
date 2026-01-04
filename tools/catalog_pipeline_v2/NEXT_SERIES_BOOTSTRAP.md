# Next Series Bootstrap Guide

**Purpose:** Use this checklist to convert a new catalog series (LC1D, LC1F, MCCB, ACB, etc.) with minimal rework.

**Reference:** This guide is based on the LC1E canonical model (frozen v6).

---

## Before You Start

### 1. Identify Catalog Structure

- [ ] Locate input pricelist file (XLSX + PDF)
- [ ] Identify catalog tables (base refs, duty ratings, voltage prices)
- [ ] Confirm frame presentation (explicit vs carry-forward)
- [ ] Note any special cases (accessories, DC coils, ranges, etc.)

### 2. Create Active Series Folder

```bash
cd tools/catalog_pipeline_v2/active/schneider/
mkdir -p <SERIES>/{00_inputs,01_working,02_outputs,03_qc,04_docs}
cd <SERIES>
```

### 3. Copy Templates

```bash
cp ../../templates/run_pipeline.sh ./
cp ../../templates/README_ACTIVE_SERIES.md ./README.md
cp ../../templates/QC_SUMMARY_TEMPLATE.md ./03_qc/QC_SUMMARY.md
```

### 4. Place Input Files

```bash
cp /path/to/input.xlsx ./00_inputs/
cp /path/to/input.pdf ./00_inputs/  # Optional
```

---

## L2 Setup

### Checklist

- [ ] **Base reference only** - Strip voltage/duty from base ref
- [ ] **Use series name** - Keep series number inside SKU
- [ ] **Poles + frame present** - Ensure physical attributes in L2
- [ ] **No price in L2** - Prices only in price matrix
- [ ] **No voltage in L2** - Voltage handled as variant
- [ ] **No duty in L2** - Duty handled in L1

### Example (LC1E pattern)

```python
# L2 should contain:
l2_product_code = "LC1E0601"  # No voltage, no duty
series_name = "Easy TeSys"
series_bucket = "LC1E"
poles = "3P"
frame_label = "FRAME-1"
```

---

## L1 Rules (Must Reuse)

### Duty Normalization

- [ ] **duty_class** field (AC1 / AC3)
- [ ] **duty_current_A** field (operational value)
- [ ] **catalog_ac1_A** field (reference)
- [ ] **catalog_ac3_A** field (reference)

**Rule (locked):**
- If `duty_class = AC1` → `duty_current_A = catalog_ac1_A`
- If `duty_class = AC3` → `duty_current_A = catalog_ac3_A`

### Voltage Normalization

- [ ] **voltage_class_code** field (M7 / N5 / M5 / N7)
- [ ] **selected_voltage_V** field (operational value)
- [ ] **selected_voltage_type** field (AC / DC)
- [ ] **catalog_voltage_label** field (reference, e.g., "N5 (415V AC)")

**Rule (locked):**
- Selected voltage fields are always derived from variant_code
- No parallel voltage columns are used in logic

### Engineering Attributes

- [ ] **motor_kw** - Motor kW rating
- [ ] **motor_hp** - Motor HP rating
- [ ] **poles** - Number of poles
- [ ] **frame_label** - Frame designation
- [ ] **aux_no** - Auxiliary NO contacts
- [ ] **aux_nc** - Auxiliary NC contacts

### Generic Descriptor

- [ ] All L1 rows have `generic_descriptor`
- [ ] Format: `Power Contactor – <SERIES> – <POLES> | <DUTY> | <VOLTAGE> | <kW>@<V> | Aux <NO>NO+<NC>NC`

---

## Pricing

### Price Matrix Structure

- [ ] **Prices only in NSW_PRICE_MATRIX** - Never in L1/L2
- [ ] **No SKU explosion** - Voltage variants don't create new products
- [ ] **Check if pricing depends on duty** - LC1E does not, but other series might

### Price Matrix Fields

- [ ] `l2_product_code` - Reference to L2
- [ ] `variant_type` - Usually "COIL_VOLTAGE"
- [ ] `variant_code` - M7 / N5 / M5 / N7
- [ ] `voltage_V` - Numeric voltage value
- [ ] `rate_inr` - Price in INR
- [ ] `effective_from` - WEF date

---

## Variants

### Variant Master

- [ ] Create `NSW_VARIANT_MASTER` sheet
- [ ] Fields: `variant_type`, `variant_code`, `voltage_V`, `voltage_type`, `display_label`
- [ ] Populate all variants used in catalog

### Product-Variant Mapping

- [ ] Create `NSW_PRODUCT_VARIANTS` sheet
- [ ] Fields: `l2_product_code`, `variant_type`, `variant_code`
- [ ] Map which variants are valid for which L2 products
- [ ] Drives UI dropdowns and validation

---

## Special Cases (Decide Early)

### kW Ranges

- [ ] **Policy:** Use minimum value OR split into separate rows?
- [ ] **LC1E pattern:** Use minimum + note in generic_descriptor

### Accessories

- [ ] **Detected?** - Are accessories in catalog?
- [ ] **Handling:** Separate FEATURE L1 lines OR embedded?
- [ ] **LC1E pattern:** Not detected (empty sheet)

### DC Coils

- [ ] **Present?** - Does series have DC coil variants?
- [ ] **Pattern:** Same voltage normalization as AC?

### Frame Carry-Forward

- [ ] **Used?** - Does catalog use frame carry-forward?
- [ ] **LC1E pattern:** Yes - frame from higher sections propagates down

---

## QC (Must Pass)

### Counts

- [ ] Base refs count matches canonical rows
- [ ] Price rows count matches coil prices
- [ ] L2 count = distinct base refs (no voltage/duty multiplication)
- [ ] Price matrix count = L2 × variants (with prices)
- [ ] L1 count = price matrix × duties (if duty expansion applies)

### Rule Checks

- [ ] **No bogus base refs** - All base refs are valid series codes
- [ ] **Frame populated everywhere** - No missing frame labels
- [ ] **L1 duty_current matches duty_class** - Operational value correct
- [ ] **selected_voltage matches variant** - Voltage fields aligned
- [ ] **L2 unchanged by price updates** - L2 contains no price/voltage/duty

### Structure Checks

- [ ] All required sheets present
- [ ] All required columns present
- [ ] No duplicate L2 products
- [ ] No orphaned L1 lines (all reference valid L2)

---

## Script Development

### 1. Create Extraction Script

```bash
cd tools/catalog_pipeline_v2/scripts/
cp lc1e_extract_canonical.py <series>_extract_canonical.py
```

**Customize:**
- Sheet detection logic
- Column mapping
- Base ref extraction
- Coil code detection
- Price extraction

### 2. Create Inspection Script (Optional)

```bash
cp inspect_lc1e_raw.py inspect_<series>_raw.py
```

**Customize:**
- Sheet structure detection
- Column identification
- Data sample output

---

## Freeze Process

### 1. Complete QC Checklist

- [ ] Fill out `03_qc/QC_SUMMARY.md`
- [ ] All checks pass
- [ ] No blocking issues

### 2. Upload to ChatGPT

**Upload:**
- `02_outputs/NSW_<SERIES>_WEF_<DATE>_vX.xlsx`
- `03_qc/QC_SUMMARY.md`

**Ask:**
- "Review this NSW file and QC summary for <SERIES>"
- "Is this ready to freeze?"

### 3. Get Approval

- [ ] ChatGPT returns ✅ "OK to freeze"
- [ ] OR fix issues and re-upload

### 4. Archive

```bash
cd tools/catalog_pipeline_v2/
mkdir -p archives/schneider/<SERIES>/<WEF>/
mv active/schneider/<SERIES>/* archives/schneider/<SERIES>/<WEF>/
```

### 5. Commit

```bash
git add archives/schneider/<SERIES>/<WEF>/
git commit -m "freeze(<SERIES>): WEF <WEF> vX canonical + QC"
```

---

## Series-Specific Notes Template

When you encounter series-specific patterns, document them here:

### <SERIES> Notes

**Special handling:**
- <Note 1>
- <Note 2>

**Deviations from LC1E:**
- <Deviation 1>
- <Deviation 2>

**Decisions:**
- <Decision 1>
- <Decision 2>

---

## Success Criteria

✅ **New series conversion takes < 20% of LC1E effort**  
✅ **All QC checks pass**  
✅ **ChatGPT approves freeze**  
✅ **Archive is complete and traceable**

---

## References

- **LC1E Canonical Model**: `archives/schneider/LC1E/2025-07-15_WEF/README.md`
- **Operating Model**: `OPERATING_MODEL.md`
- **QC Template**: `templates/QC_SUMMARY_TEMPLATE.md`

---

**Last Updated**: <DATE>

