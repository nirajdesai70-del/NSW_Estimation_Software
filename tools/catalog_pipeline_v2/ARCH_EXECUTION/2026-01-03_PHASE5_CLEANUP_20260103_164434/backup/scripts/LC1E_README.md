# LC1E Series Pipeline

This folder contains LC1E-specific extraction and processing scripts.

## Status

⚠️ **INCOMPLETE**: The extraction script (`lc1e_extract_canonical.py`) is a placeholder that needs customization based on the actual pricelist structure.

## Required Input Files

Place these files in `input/schneider/lc1e/`:
- `Switching _All_WEF 15th Jul 25.pdf` (or similar PDF)
- `Switching _All_WEF 15th Jul 25.xlsx` (or similar XLSX)

## Workflow

### Step 0: Extract Canonical Tables (NEEDS CUSTOMIZATION)

```bash
python scripts/lc1e_extract_canonical.py \
  --input_xlsx input/schneider/lc1e/Switching_All_WEF_15th_Jul_25.xlsx \
  --out output/lc1e/LC1E_CANONICAL_ROWS_v1.xlsx
```

**Output**: `LC1E_CANONICAL_ROWS_v1.xlsx` with 3 sheets:
- `LC1E_CANONICAL_ROWS` - Base reference rows with AC1/AC3 ratings
- `LC1E_COIL_CODE_PRICES` - Completed SKU rows from coil columns
- `LC1E_ACCESSORY_SKUS` - Accessory SKUs from page 10

### Step 1: Build L2 from Canonical

```bash
python scripts/lc1e_build_l2.py \
  --canonical output/lc1e/LC1E_CANONICAL_ROWS_v1.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out output/lc1e/LC1E_L2_tmp.xlsx
```

### Step 2: Derive L1 (use existing script with LC1E-specific mode)

```bash
python scripts/derive_l1_from_l2.py \
  --l2 output/lc1e/LC1E_L2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out output/lc1e/LC1E_L1_tmp.xlsx
```

### Step 3: Build Engineer Review Workbook

```bash
python scripts/build_master_workbook.py \
  --l2 output/lc1e/LC1E_L2_tmp.xlsx \
  --l1 output/lc1e/LC1E_L1_tmp.xlsx \
  --out output/lc1e/LC1E_ENGINEER_REVIEW_v1.xlsx
```

## Next Steps

1. **Inspect raw pricelist structure** - Examine pages 8-10 to understand table layout
2. **Customize extraction logic** - Update `lc1e_extract_canonical.py` to parse actual table structure
3. **Test extraction** - Run Step 0 and verify canonical tables are populated correctly
4. **Run full pipeline** - Execute Steps 1-3
5. **Engineer validation** - Review output workbook

