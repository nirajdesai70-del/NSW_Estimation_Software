# Price Normalizer

## Purpose
Convert OEM price list XLSX files into NSW import-ready CSV with standardized schema:
`import_stage, make, series, sku_code, description, uom, list_price, currency, notes`

The tool handles wide sheets with empty columns by collapsing each row to non-empty cells first, then mapping by position.

**Features:**
- Series detection (heading-based + SKU-prefix fallback)
- SKU validation (rejects purely numeric codes)
- TEST/FINAL mode separation for governance
- Automatic folder routing based on mode

## Install
```bash
pip install -r tools/price_normalizer/requirements-tools.txt
```

## Run (Schneider)

### Test Mode (Learning/Calibration)
```bash
python tools/price_normalizer/normalize.py \
  --profile tools/price_normalizer/profiles/schneider_contactors.yml \
  --file tools/price_normalizer/input/test/schneider_TEST1.xlsx \
  --mode test
```

### Final Mode (Canonical Import)
```bash
python tools/price_normalizer/normalize.py \
  --profile tools/price_normalizer/profiles/schneider_contactors.yml \
  --file tools/price_normalizer/input/final/schneider_FINAL_2025-12-26.xlsx \
  --mode final
```

## Output

Outputs are routed to mode-specific folders:

- **Test Mode**: `output/test/`, `errors/test/`, `logs/test/`
- **Final Mode**: `output/final/`, `errors/final/`, `logs/final/`

Files generated:
- `*.csv` - Import-ready normalized CSV
- `*_errors.xlsx` - Rows that failed parsing
- `*_summary.json` - Processing statistics and series coverage

## Next Step
Upload CSV to FastAPI:
```bash
# Dry run first (validate only)
curl -X POST "http://localhost:8000/api/v1/catalog/skus/import?dry_run=true" \
  -F "file=@tools/price_normalizer/output/schneider_*.csv"

# Then actual import
curl -X POST "http://localhost:8000/api/v1/catalog/skus/import?dry_run=false" \
  -F "file=@tools/price_normalizer/output/schneider_*.csv"
```

## How It Works

1. **Collapse rows**: Each Excel row is collapsed to only non-empty cells (handles wide sheets)
2. **Map by index**: After collapsing, columns are mapped by position (0-based)
3. **Series detection**:
   - **Tier 1**: Detect series from heading rows (e.g., "Easy TeSys Power Contactors")
   - **Tier 2**: Infer series from SKU prefix if heading not found (e.g., `LC1E*` → "Easy TeSys Power Contactors")
4. **SKU validation**: Rejects purely numeric codes (must contain at least one alphabet)
5. **Extract SKU**: Handles SKU codes with asterisks (e.g., `LC1E0601*`) and trailing junk
6. **Build description**: Combines section markers (FRAME-3) with technical specs
7. **Filter**: Drops header rows, section titles, and rows missing required fields
8. **Add metadata**: Includes `import_stage` (TEST/FINAL) and `series` columns

## Adding New OEMs

1. Copy `profiles/template.yml` to `profiles/{oem_name}.yml`
2. Adjust `columns_by_index` to match your XLSX structure after collapsing
3. Configure `series.heading_patterns` for series detection
4. Optionally add `series.sku_prefix_mappings` for fallback
5. Update `filters.ignore_if_contains_any` for header patterns
6. Run with `--profile profiles/{oem_name}.yml --mode test` first

## Troubleshooting

**Wrong column data?**
- Check the error Excel to see raw collapsed cells
- Adjust `columns_by_index` in the profile (0-based after collapsing)

**Missing SKUs?**
- Verify `columns_by_index.sku_raw` points to the right position
- Check that SKU extraction regex matches your format

**Too many rows dropped?**
- Review `filters.ignore_if_contains_any` - may be too aggressive
- Check summary JSON for `rows_dropped` count

**Low series coverage?**
- Add more patterns to `series.heading_patterns` in profile
- Add `series.sku_prefix_mappings` for common SKU prefixes
- Check error Excel to see which rows are missing series

**Invalid SKU errors?**
- Review `invalid_sku_count` in summary JSON
- Adjust `ignore_if_contains_any` to filter junk rows earlier
- Verify SKU extraction regex matches your format

## Governance

- **[TEST1_PASS_CHECKLIST.md](TEST1_PASS_CHECKLIST.md)** - Criteria for promoting Test-1 to FINAL
- **[PRICE_CATALOG_FREEZE_POLICY.md](../../docs/GOVERNANCE/PRICE_CATALOG_FREEZE_POLICY.md)** - Rules for TEST vs FINAL separation

## Output Schema

All normalized CSVs follow this schema (columns in order):

| Column | Description | Required |
|--------|-------------|----------|
| `import_stage` | TEST or FINAL | Yes |
| `make` | Manufacturer name | Yes |
| `series` | Product series/family | Yes (empty string if not detected) |
| `sku_code` | Product SKU/Part number | Yes |
| `description` | Product description | Yes |
| `uom` | Unit of measure (EA, PCS, etc.) | Yes |
| `list_price` | List price (numeric) | Yes |
| `currency` | Currency code (INR, USD, etc.) | Yes |
| `notes` | Additional notes | No |
