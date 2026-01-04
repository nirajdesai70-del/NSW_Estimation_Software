# NSW Builder Fix - Complete

**Date**: 2025-01-XX  
**Status**: ✅ COMPLETE

---

## Problem Summary

The pipeline was generating **legacy Engineer Review workbook** (L2_SKU_MASTER, L1_LINES) instead of **NSW format workbook** (NSW_L2_PRODUCTS, NSW_L1_CONFIG_LINES).

**Gaps Identified:**
1. ❌ No NSW workbook builder (missing step)
2. ❌ Pipeline produced legacy format, not NSW format
3. ❌ L1 format was expanded (L1_LINES) instead of normalized (NSW_L1_CONFIG_LINES)

---

## Fixes Applied

### ✅ Fix A: NSW Workbook Builder Created

**File**: `scripts/build_nsw_workbook_from_canonical.py`

**Purpose:**
- Builds NSW format workbook (PRIMARY freeze artifact) from canonical extraction
- Creates all NSW format sheets with proper normalization

**Sheets Generated:**
- `NSW_L0_TEMPLATE` - L0 intent templates (optional)
- `NSW_L0_L2_ELIGIBILITY` - L0→L2 eligibility mappings (optional)
- `NSW_L2_PRODUCTS` - L2 product identity (stable, no price/voltage/duty)
- `NSW_VARIANT_MASTER` - Variant definitions (voltage codes)
- `NSW_PRODUCT_VARIANTS` - L2→variant allowed mappings
- `NSW_PRICE_MATRIX` - Price matrix (l2_product_code × variant_code)
- `NSW_L1_CONFIG_LINES` - L1 configuration with normalization

**Normalization Implemented:**
- ✅ **Duty normalization**: `duty_class`, `duty_current_A`, `catalog_ac1_A`, `catalog_ac3_A`
- ✅ **Voltage normalization**: `variant_code`, `voltage_class_code`, `selected_voltage_V`, `selected_voltage_type`, `catalog_voltage_label`
- ✅ **Engineering context**: `motor_kw`, `motor_hp`, `aux_no`, `aux_nc`, `poles`, `frame_label`

---

### ✅ Fix B: Pipeline Updated

**File**: `templates/run_pipeline.sh`

**Changes:**
- Step 5 now builds NSW format workbook (PRIMARY artifact)
- Uses `build_nsw_workbook_from_canonical.py`
- Engineer review workbook is optional (secondary output)

**Output Files:**
1. **NSW_<SERIES>_WEF_<DATE>_vX.xlsx** ← PRIMARY freeze artifact
2. NSW_MASTER_SCHNEIDER_WEF_<DATE>_ENGINEER_REVIEW.xlsx ← Optional (legacy)

---

### ✅ Fix C: Canonical Extractor Scope Documented

**File**: `CANONICAL_EXTRACTOR_NOTE.md`

**Decision**: **Full LC1E** (not Page-8 only)

**Rationale:**
- Full series extraction provides complete catalog coverage
- Same extractor can be used for all LC1E sections
- Counts will differ from v6 Page-8-only output (expected)

**Counts:**
- Rebuild (Full LC1E): 23 base refs, 59 coil prices
- V6 (Page-8 only): 21 base refs, 40 coil prices

---

## Validation Results

### ✅ NSW Workbook Structure

**Test Run**: Rebuild from canonical
- ✅ All required sheets present
- ✅ NSW_L2_PRODUCTS: 23 rows
- ✅ NSW_VARIANT_MASTER: 3 rows
- ✅ NSW_PRODUCT_VARIANTS: 59 rows
- ✅ NSW_PRICE_MATRIX: 59 rows
- ✅ NSW_L1_CONFIG_LINES: 118 rows (23 base × 2 duties × ~2.5 variants)

### ✅ Normalization Validation

**Duty Normalization:**
- ✅ `duty_class` present (AC1/AC3)
- ✅ `duty_current_A` derived from `duty_class`
- ✅ `catalog_ac1_A`, `catalog_ac3_A` present as reference

**Voltage Normalization:**
- ✅ `variant_code` present (M7, N5, etc.)
- ✅ `voltage_class_code` = `variant_code`
- ✅ `selected_voltage_V`, `selected_voltage_type` derived from variant
- ✅ `catalog_voltage_label` present

**Engineering Context:**
- ✅ `motor_kw`, `motor_hp` present
- ✅ `aux_no`, `aux_nc` present
- ✅ `poles`, `frame_label` present
- ✅ `generic_descriptor` includes all context

---

## Quick Validation Criteria (Met)

✅ **Output contains v6 sheet set** (L0/L1/L2/variants/price matrix)  
✅ **NSW_L1_CONFIG_LINES includes duty normalization columns**  
✅ **NSW_L1_CONFIG_LINES includes voltage normalization columns**  
✅ **NSW_L1_CONFIG_LINES includes engineering context columns**  
✅ **RATING_MAP unused** (ratings embedded in L1, as per NSW model)

---

## Usage

### For New Series

```bash
cd active/schneider/<SERIES>/
./run_pipeline.sh
```

**Output:**
- `NSW_<SERIES>_WEF_<DATE>_vX.xlsx` ← PRIMARY (freeze artifact)
- `NSW_MASTER_SCHNEIDER_WEF_<DATE>_ENGINEER_REVIEW.xlsx` ← Optional (legacy)

### Manual NSW Builder

```bash
python3 scripts/build_nsw_workbook_from_canonical.py \
  --canonical <SERIES>_CANONICAL_vX.xlsx \
  --series <SERIES> \
  --series_name "Easy TeSys" \
  --wef YYYY-MM-DD \
  --pricelist_ref "WEF DATE" \
  --out NSW_<SERIES>_WEF_<DATE>_vX.xlsx
```

---

## Files Created/Updated

### New Files
- ✅ `scripts/build_nsw_workbook_from_canonical.py` - NSW workbook builder
- ✅ `CANONICAL_EXTRACTOR_NOTE.md` - Scope documentation
- ✅ `NSW_BUILDER_FIX_COMPLETE.md` - This file

### Updated Files
- ✅ `templates/run_pipeline.sh` - Uses NSW builder as primary output

---

## Next Steps

1. ✅ **NSW builder implemented** - Ready for use
2. ✅ **Pipeline updated** - Primary output is NSW format
3. ✅ **Scope documented** - Full LC1E extraction (not Page-8 only)
4. 🔄 **Ready for next series** - LC1D, LC1F, etc. can use same builder

---

## Test Results

**Rebuild Test:**
- ✅ NSW workbook generated successfully
- ✅ All sheets present and correct
- ✅ Normalization working correctly
- ✅ L1 expansion correct (118 rows = 23 base × 2 duties × variants)

**Sample Output:**
```
NSW_L0_TEMPLATE: 0 rows
NSW_L0_L2_ELIGIBILITY: 0 rows
NSW_L2_PRODUCTS: 23 rows
NSW_VARIANT_MASTER: 3 rows
NSW_PRODUCT_VARIANTS: 59 rows
NSW_PRICE_MATRIX: 59 rows
NSW_L1_CONFIG_LINES: 118 rows
```

---

**Status**: ✅ COMPLETE - Pipeline now generates NSW format workbook (v6 structure)

