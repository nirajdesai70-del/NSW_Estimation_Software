> Source: source_snapshot/EXCEL_BOM_IMPORT_IMPLEMENTATION_PLAN.md
> Bifurcated into: features/master_bom/import_export/EXCEL_BOM_IMPORT_IMPLEMENTATION_PLAN.md
> Module: Master BOM > Import/Export
> Date: 2025-12-17 (IST)

# Excel BOM Import Implementation Plan
**Date:** December 9, 2025  
**Purpose:** Bridge legacy Excel BOMs into NEPL V2 system

---

## 🎯 Overview

This implementation provides a **two-stage import pipeline**:
1. **Stage 1 (Python):** Excel → JSON conversion (flexible, format-agnostic)
2. **Stage 2 (Laravel):** JSON → V2 BOM items (NEPL-specific integration)

---

## 📁 Project Structure

```
/tools/
  ├── nepl_bom_to_json.py          # Main Python converter
  ├── requirements.txt              # Python dependencies
  └── mappings/
      ├── map_nepl_legacy.yaml      # NEPL legacy format mapping
      ├── map_customer_a.yaml       # Customer A format
      └── map_vendor_schneider.yaml # Vendor-specific format

/app/Console/Commands/
  └── ImportBomJson.php            # Laravel Artisan command

/docs/
  └── EXCEL_BOM_IMPORT_GUIDE.md    # User guide
```

---

## 🔧 Stage 1: Python Excel → JSON Converter

### Purpose
Convert any Excel BOM format to standardized JSON using YAML mapping files.

### Features
- **Format-agnostic:** Works with any Excel structure via YAML mapping
- **Profile-based:** Different mappings for different vendors/customers
- **Validation:** Reports parsing errors and missing columns
- **Flexible:** Easy to add new formats without code changes

### Usage
```bash
# Install dependencies
pip install -r tools/requirements.txt

# Convert Excel to JSON
python tools/nepl_bom_to_json.py \
  path/to/bom.xlsx \
  --map tools/mappings/map_nepl_legacy.yaml \
  --out bom.json

# With validation report
python tools/nepl_bom_to_json.py \
  path/to/bom.xlsx \
  --map tools/mappings/map_nepl_legacy.yaml \
  --out bom.json \
  --validate
```

### JSON Output Format
```json
[
  {
    "item_code": "MCCB-250A",
    "description": "250A 4P MCCB 36kA",
    "quantity": 2,
    "uom": "NOS",
    "unit_price": 3250.0,
    "make": "Schneider",
    "model": "NSX250",
    "category": "MCCB",
    "panel_name": "MDB-01",
    "feeder_name": "INCOMER 1",
    "bom_name": "INCOMER BOM",
    "bom_level": 0,
    "currency": "INR",
    "source_system": "NEPL-LEGACY"
  }
]
```

---

## 🔧 Stage 2: Laravel JSON → V2 Import

### Purpose
Import JSON BOM data into NEPL V2 quotation structure.

### Artisan Command
```bash
php artisan nepl:bom-import bom.json \
  --quotation=123 \
  --panel="MDB-01" \
  --feeder="INCOMER 1" \
  --bom="INCOMER BOM" \
  --level=0 \
  --dry-run
```

### Command Options
- `bom.json` - Path to JSON file (required)
- `--quotation=ID` - Quotation ID (required)
- `--panel=NAME` - Panel/Sale name (required)
- `--feeder=NAME` - Feeder name (optional, for V2 hierarchy)
- `--bom=NAME` - BOM name (optional, defaults to "Imported BOM")
- `--level=N` - BOM level (0=feeder, 1=BOM1, 2=BOM2, default: 0)
- `--dry-run` - Preview without importing
- `--create-missing` - Create products if not found (optional)

### Import Logic

1. **Validate Quotation**
   - Check quotation exists and is active
   - Verify user has permission

2. **Resolve Panel (QuotationSale)**
   - Find by `SaleCustomName` matching `--panel`
   - If not found and `--create-missing`, create new panel

3. **Resolve Feeder/BOM (QuotationSaleBom)**
   - For V2 hierarchy:
     - Level 0: Find/create feeder (ParentBomId = NULL)
     - Level 1+: Find/create BOM under parent
   - For legacy: Create flat BOM structure

4. **Resolve Products**
   - Search strategy (in order):
     1. By SKU (`item_code`)
     2. By description + make + model
     3. By description only
     4. By make + model (if generic product exists)
   - If not found:
     - Log to `missing_products.json`
     - Skip item (or create if `--create-missing`)

5. **Resolve Make/Series**
   - Find Make by name (case-insensitive)
   - Find Series by name + MakeId
   - If not found: log warning, continue with MakeId=0

6. **Create BOM Items**
   - For each JSON item:
     ```php
     QuotationSaleBomItem::create([
         'QuotationId' => $quotationId,
         'QuotationSaleId' => $panelId,
         'QuotationSaleBomId' => $bomId,
         'ProductId' => $genericProductId,
         'Description' => $specificProductId, // If specific product found
         'MakeId' => $makeId,
         'SeriesId' => $seriesId,
         'Qty' => $item['quantity'],
         'Rate' => $item['unit_price'],
         'Discount' => 0,
         'NetRate' => $item['unit_price'],
         'Amount' => $item['quantity'] * $item['unit_price'],
         'RateSource' => 'MANUAL_WITH_DISCOUNT',
         'IsClientSupplied' => 0,
         'IsPriceConfirmed' => 0,
         'Status' => 0,
     ]);
     ```

7. **Recalculate Amounts**
   - Update BOM totals
   - Update Panel totals
   - Update Quotation totals

8. **Generate Report**
   - Summary: X items imported, Y skipped, Z errors
   - Missing products list
   - Unmatched makes/series

---

## 📋 Implementation Steps

### Step 1: Create Python Script Structure
- [x] Create `/tools/` directory
- [ ] Add `nepl_bom_to_json.py`
- [ ] Add `requirements.txt`
- [ ] Create sample mapping files

### Step 2: Create Laravel Artisan Command
- [ ] Create `ImportBomJson.php` command
- [ ] Implement product resolution logic
- [ ] Implement V2 hierarchy support
- [ ] Add validation and error handling
- [ ] Add dry-run mode

### Step 3: Testing
- [ ] Test with legacy NEPL Excel format
- [ ] Test with customer-specific formats
- [ ] Test product matching strategies
- [ ] Test V2 hierarchy creation

### Step 4: Documentation
- [ ] User guide for Excel → JSON
- [ ] User guide for JSON → V2 import
- [ ] Mapping file examples
- [ ] Troubleshooting guide

---

## 🔍 Product Resolution Strategy

### Priority Order
1. **Exact SKU Match**
   ```php
   Product::where('SKU', $itemCode)->where('ProductType', 2)->first();
   ```

2. **Description + Make + Model**
   ```php
   Product::where('Name', 'LIKE', "%{$description}%")
       ->where('MakeId', $makeId)
       ->whereHas('series', fn($q) => $q->where('Name', $model))
       ->where('ProductType', 2)
       ->first();
   ```

3. **Description Only**
   ```php
   Product::where('Name', 'LIKE', "%{$description}%")
       ->where('ProductType', 2)
       ->first();
   ```

4. **Generic Product by Make + Model**
   ```php
   $generic = Product::where('Name', 'LIKE', "%{$description}%")
       ->where('ProductType', 1)
       ->first();
   if ($generic) {
       // Use generic, create specific later if needed
   }
   ```

---

## ⚠️ Error Handling

### Missing Products
- Log to `missing_products.json` with full item details
- Continue import for other items
- Option to create products later via separate command

### Missing Make/Series
- Log warning
- Continue with MakeId=0, SeriesId=0
- User can update later in UI

### Invalid Data
- Skip rows with missing required fields
- Log to `import_errors.json`
- Report summary at end

---

## 🚀 Future Enhancements

1. **Web UI Import**
   - Upload Excel directly in NEPL
   - Preview before import
   - Map columns interactively

2. **Batch Import**
   - Import multiple BOMs at once
   - Progress tracking
   - Resume on failure

3. **Product Auto-Creation**
   - Create missing products during import
   - Map to categories automatically
   - Set default prices

4. **Validation Rules**
   - Required field validation
   - Price range validation
   - Quantity validation

---

## 📝 Example Workflow

```bash
# 1. Convert Excel to JSON
python tools/nepl_bom_to_json.py \
  customer_bom.xlsx \
  --map tools/mappings/map_customer_a.yaml \
  --out customer_bom.json

# 2. Preview import (dry-run)
php artisan nepl:bom-import customer_bom.json \
  --quotation=123 \
  --panel="MDB-01" \
  --dry-run

# 3. Actual import
php artisan nepl:bom-import customer_bom.json \
  --quotation=123 \
  --panel="MDB-01" \
  --feeder="INCOMER 1" \
  --bom="INCOMER BOM"

# 4. Check missing products
cat missing_products.json

# 5. Fix missing products and re-import
php artisan nepl:bom-import customer_bom.json \
  --quotation=123 \
  --panel="MDB-01" \
  --create-missing
```

---

**Status:** Ready for Implementation  
**Next Step:** Create Python script and Laravel command
