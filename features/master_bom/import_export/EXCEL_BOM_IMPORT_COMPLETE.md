> Source: source_snapshot/EXCEL_BOM_IMPORT_COMPLETE.md
> Bifurcated into: features/master_bom/import_export/EXCEL_BOM_IMPORT_COMPLETE.md
> Module: Master BOM > Import/Export
> Date: 2025-12-17 (IST)

# Excel BOM Import - Implementation Complete ✅
**Date:** December 9, 2025

---

## 📦 What Was Created

### 1. **Python Excel → JSON Converter**
- **File:** `/tools/nepl_bom_to_json.py`
- **Purpose:** Convert any Excel BOM format to standardized JSON
- **Features:**
  - YAML-based column mapping (no code changes needed)
  - Multiple format support via mapping files
  - Validation and error reporting
  - Handles missing columns gracefully

### 2. **Laravel Artisan Command**
- **File:** `/app/Console/Commands/ImportBomJson.php`
- **Command:** `php artisan nepl:bom-import`
- **Purpose:** Import JSON BOM data into NEPL V2 quotation structure
- **Features:**
  - Product resolution (SKU, description, make/model)
  - V2 hierarchy support (panels, feeders, BOMs)
  - Dry-run mode for preview
  - Missing product reporting
  - Automatic total recalculation

### 3. **Mapping Files**
- **File:** `/tools/mappings/map_nepl_legacy.yaml`
- **Purpose:** Map NEPL legacy Excel format to JSON
- **Extensible:** Easy to add new formats

### 4. **Documentation**
- **Implementation Plan:** `EXCEL_BOM_IMPORT_IMPLEMENTATION_PLAN.md`
- **Tools README:** `/tools/README.md`

---

## 🚀 Quick Start

### Step 1: Install Python Dependencies

```bash
cd tools
pip install -r requirements.txt
```

### Step 2: Convert Excel to JSON

```bash
python nepl_bom_to_json.py path/to/bom.xlsx \
  --map mappings/map_nepl_legacy.yaml \
  --out bom.json \
  --validate
```

### Step 3: Preview Import (Dry Run)

```bash
php artisan nepl:bom-import bom.json \
  --quotation=123 \
  --panel="MDB-01" \
  --feeder="INCOMER 1" \
  --bom="INCOMER BOM" \
  --dry-run
```

### Step 4: Import into NEPL

```bash
php artisan nepl:bom-import bom.json \
  --quotation=123 \
  --panel="MDB-01" \
  --feeder="INCOMER 1" \
  --bom="INCOMER BOM"
```

---

## 📋 Command Options

### `nepl:bom-import` Command

**Required:**
- `{file}` - Path to JSON file
- `--quotation=ID` - Quotation ID
- `--panel=NAME` - Panel/Sale name

**Optional:**
- `--feeder=NAME` - Feeder name (for V2 hierarchy)
- `--bom=NAME` - BOM name (defaults to "Imported BOM")
- `--level=N` - BOM level (0=feeder, 1=BOM1, 2=BOM2, default: 0)
- `--dry-run` - Preview without importing
- `--create-missing` - Create products if not found (use with caution)

---

## 🔍 How It Works

### Product Resolution Strategy

The import command tries to find products in this order:

1. **By SKU** - Exact match on `item_code`
2. **By Description + Make + Model** - Combined match
3. **By Description Only** - Partial match
4. **By Generic Product** - Falls back to generic if specific not found

### V2 Hierarchy Support

- **Level 0 (Feeder):** Creates `QuotationSaleBom` with `Level=0`, `ParentBomId=NULL`
- **Level 1+ (Nested BOMs):** Creates BOMs under parent feeders
- **Legacy Mode:** Creates flat BOM structure if no hierarchy specified

### Error Handling

- **Missing Products:** Logged to `missing_products.json`
- **Missing Makes/Series:** Logged but import continues
- **Invalid Data:** Skipped with error report

---

## 📊 Import Statistics

After import, you'll see:

```
Import Summary
==============
+------------------+-------+
| Metric           | Count |
+------------------+-------+
| Imported         | 45    |
| Skipped          | 2     |
| Errors           | 0     |
| Missing Products | 2     |
| Missing Makes    | 0     |
| Missing Series   | 1     |
+------------------+-------+
```

---

## 🎯 Use Cases

### 1. Legacy BOM Migration
Import old Excel BOMs into new V2 quotations:
```bash
python nepl_bom_to_json.py legacy_bom.xlsx --map mappings/map_nepl_legacy.yaml --out legacy.json
php artisan nepl:bom-import legacy.json --quotation=123 --panel="Panel 1"
```

### 2. Customer BOM Import
Import customer-provided Excel BOMs:
```bash
# Create custom mapping first
python nepl_bom_to_json.py customer_bom.xlsx --map mappings/map_customer_a.yaml --out customer.json
php artisan nepl:bom-import customer.json --quotation=123 --panel="Customer Panel"
```

### 3. Vendor BOM Import
Import vendor-specific formats (ABB, Schneider, etc.):
```bash
python nepl_bom_to_json.py vendor_bom.xlsx --map mappings/map_vendor_schneider.yaml --out vendor.json
php artisan nepl:bom-import vendor.json --quotation=123 --panel="Vendor Panel"
```

---

## 🔧 Customization

### Adding New Excel Formats

1. Create new mapping file in `/tools/mappings/`:
   ```yaml
   source_system: "CUSTOMER-B"
   columns:
     item_code: "Part Number"
     description: "Item Description"
     quantity: "Qty"
     # ... etc
   ```

2. Use the new mapping:
   ```bash
   python nepl_bom_to_json.py bom.xlsx --map mappings/map_customer_b.yaml --out bom.json
   ```

### Extending Product Resolution

Edit `ImportBomJson.php` → `resolveProduct()` method to add custom matching logic.

---

## ⚠️ Important Notes

1. **Always use `--dry-run` first** to preview what will be imported
2. **Check `missing_products.json`** after import to see what wasn't found
3. **Product matching is case-insensitive** but exact SKU matches are preferred
4. **Totals are recalculated automatically** after import
5. **Use `--create-missing` with caution** - it will create products automatically

---

## 🐛 Troubleshooting

### "Quotation not found"
- Verify quotation ID exists: `SELECT * FROM quotations WHERE QuotationId = 123`
- Check quotation is active: `Status = 0`

### "Panel not found"
- Panel name must match exactly (case-sensitive)
- Use `--dry-run` to see what would be created

### "Product not found"
- Check `missing_products.json` for details
- Verify product exists in database
- Try adjusting product resolution strategy

### "Invalid JSON"
- Validate JSON file: `cat bom.json | python -m json.tool`
- Check for syntax errors in JSON

---

## 📈 Next Steps

1. **Test with sample Excel file** - Use a small BOM first
2. **Create custom mappings** - For your specific Excel formats
3. **Review missing products** - Fix product matching if needed
4. **Scale up** - Import larger BOMs once validated

---

## ✅ Status

**Implementation:** ✅ Complete  
**Testing:** ⏳ Ready for testing  
**Documentation:** ✅ Complete

---

**Ready to use!** Start with a small test BOM and scale up once validated.
