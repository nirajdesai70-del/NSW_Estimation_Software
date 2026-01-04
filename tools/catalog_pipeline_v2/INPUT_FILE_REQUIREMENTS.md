# Input File Requirements

## Current Status

The file `input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx` is a **raw pricelist file** with formatting rows and multiple sections.

## What the Pipeline Needs

The scripts expect a **canonical table** with one of these formats:

### Format 1: CANONICAL Mode
- Column: `sku_code` (or SKU, OEM_Catalog_No)
- Column: `price_primary` (or Price, Rate, list_price)
- Column: `coil_code` (or CoilCode)
- Optional: `voltage_type`, `voltage_value`
- Optional: `ac1_a`, `ac3_a`, `ac1_current`, `ac3_current`
- Optional: `kw`, `hp`, `poles`

### Format 2: RAW Mode
- Column: `Base_Reference` (or Reference, OEM_Catalog_No, SKU, sku_code)
- Columns: `M7`, `N7`, `F7`, `B7`, `BD`, `FD`, `MD`, etc. (coil code columns with prices)
- Optional: `AC1_Current_A`, `AC3_Current_A`, `kW`, `HP`, etc.

## Next Steps

The raw pricelist file needs to be converted to canonical format before running the pipeline.

**To create a canonical table:**
1. Extract table sections from the pricelist
2. Normalize column headers
3. Clean data rows
4. Save as canonical format Excel file

Once you have a canonical table file, place it at:
`input/schneider/Schneider_CANONICAL_TABLE_v3.xlsx`

Then run the pipeline.
