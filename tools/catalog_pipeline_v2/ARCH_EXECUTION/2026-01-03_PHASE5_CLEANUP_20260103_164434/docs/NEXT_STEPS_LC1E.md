# LC1E Pipeline - Next Steps

## ✅ Files Located

The pricelist files are available at:
- XLSX: `input/schneider/lc1e/Switching _All_WEF 15th Jul 25.xlsx`
- PDF: `input/schneider/lc1e/Switching _All_WEF 15th Jul 25.pdf`

## ⚠️ Current Status

1. ✅ Folder structure created
2. ✅ Scripts created (placeholder extraction script)
3. ⚠️ **NEXT**: Need to inspect pricelist structure to customize extraction

## 🔍 To Customize Extraction Script

The file `scripts/lc1e_extract_canonical.py` needs to be customized based on the actual pricelist structure.

### Inspection Steps

1. **Open the XLSX file** and locate pages 8-10 (LC1E tables):
   - Page 8: LC1E 3P AC control (columns: M7, N5)
   - Page 9: LC1E 3P DC control (column: BD) + 4P AC control (columns: B7, F7, M5WB, N5WB)
   - Page 10: LC1E accessories

2. **Identify key information**:
   - Header row number where column names start
   - Column positions for:
     - Base reference (e.g., LC1E0601*)
     - AC1 current rating
     - AC3 current rating
     - HP, kW
     - Coil code price columns (M7, N5, F7, B7, BD, M5WB, N5WB)
     - Aux contacts configuration
     - Poles (3P/4P)

3. **Update `scripts/lc1e_extract_canonical.py`**:
   - Modify `extract_lc1e_canonical_rows()` function
   - Implement table detection logic
   - Implement column parsing based on actual positions
   - Extract base references, ratings, and prices

### Quick Test

Once customized, test the extraction:

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2

python3 scripts/lc1e_extract_canonical.py \
  --input_xlsx "input/schneider/lc1e/Switching _All_WEF 15th Jul 25.xlsx" \
  --out output/lc1e/LC1E_CANONICAL_ROWS_v1.xlsx
```

Then inspect the output to verify:
- `LC1E_CANONICAL_ROWS` has base refs with AC1/AC3 ratings
- `LC1E_COIL_CODE_PRICES` has completed SKUs with prices
- `LC1E_ACCESSORY_SKUS` has accessory SKUs (if present)

### Full Pipeline (After Extraction Works)

```bash
# Step 1: Build L2
python3 scripts/lc1e_build_l2.py \
  --canonical output/lc1e/LC1E_CANONICAL_ROWS_v1.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out output/lc1e/LC1E_L2_tmp.xlsx

# Step 2: Derive L1
python3 scripts/derive_l1_from_l2.py \
  --l2 output/lc1e/LC1E_L2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out output/lc1e/LC1E_L1_tmp.xlsx

# Step 3: Build Engineer Review Workbook
python3 scripts/build_master_workbook.py \
  --l2 output/lc1e/LC1E_L2_tmp.xlsx \
  --l1 output/lc1e/LC1E_L1_tmp.xlsx \
  --out output/lc1e/LC1E_ENGINEER_REVIEW_v1.xlsx
```

## 📝 Notes

- The pricelist XLSX likely has a single sheet "Table 1" with formatted data
- Pages 8-10 need to be identified within that sheet (may require row range detection)
- Column positions may shift, so the extraction script should be flexible
- Base references need normalization (strip *, #, coil suffixes)


