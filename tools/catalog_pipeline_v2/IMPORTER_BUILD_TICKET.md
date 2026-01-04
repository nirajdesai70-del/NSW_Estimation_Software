# Generic Catalog Importer - Build Ticket

**Date:** 2026-01-03  
**Status:** 📋 READY FOR IMPLEMENTATION  
**Priority:** HIGH (Week-1 Day 2-3)  
**Dependencies:** Week-1 Day 1-2 migrations complete

---

## 🎯 Objective

Build a **generic, product-agnostic importer** that can ingest the normalized item master workbook (`ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`) and populate Phase-5 database tables without any product-specific branching logic.

**Key Principle:** One structure, many products. Same importer handles LC1D, EOCR, MPCB, Accessories, etc.

---

## 📋 Requirements

### Functional Requirements

1. **Read Normalized Workbook**
   - Accept Excel file path as input
   - Read multiple sheets (NSW_ITEM_MASTER_ENGINEER_VIEW, ACCESSORIES_MASTER, ACCESSORY_COMPATIBILITY)
   - Handle missing columns gracefully

2. **Idempotent Import**
   - Can run multiple times without duplicates
   - Update existing records if data changed
   - Track import batches for audit

3. **Multi-Product-Type Support**
   - Process Contactors, EOCR, MPCB, MCCB, ACB, Accessories uniformly
   - No product-specific branching logic
   - Same processing path for all items

4. **Data Mapping**
   - Map source columns to Schema Canon tables
   - Handle SC_Lx → JSONB conversion
   - Handle KVU attributes (FIX_*/ATTR_*)
   - Handle pricing data

5. **Error Handling**
   - Log validation errors
   - Continue processing on non-fatal errors
   - Report summary at end

---

## 🗂️ Target Tables

### Core Tables (Required)

1. **Taxonomy:**
   - `makes` (from `make` column)
   - `series` (from `oem_series`, `series_code`)
   - `categories` (from `business_category`)
   - `product_types` (from `item_producttype`)

2. **Catalog:**
   - `catalog_skus` (L2 SKUs)
     - Identity: `make`, `oem_catalog_no` (from `sku_code`)
     - Structure: `sc_struct_jsonb` (from `SC_L1` through `SC_L8`)
     - Metadata: `oem_series_range`, `item_producttype`, `business_subcategory`

3. **Attributes:**
   - `l1_intent_lines` (L1 configuration lines)
   - `l1_attributes` (from `FIX_*` and `ATTR_*` columns)

4. **Pricing:**
   - `price_lists` (from `price_list_ref`)
   - `sku_prices` (from `price_inr`, `currency`, `wef_date`)

5. **Compatibility:**
   - `accessory_compatibility` (from `ACCESSORY_COMPATIBILITY` sheet)

---

## 📊 Column Mapping Specification

### Source: NSW_ITEM_MASTER_ENGINEER_VIEW

| Source Column | Target Table | Target Column | Transformation |
|---------------|--------------|---------------|----------------|
| `make` | `makes` | `name` | Lookup or create |
| `oem_series` | `series` | `name` | Lookup or create (link to make) |
| `series_code` | `series` | (metadata) | Alternative identifier |
| `sku_code` | `catalog_skus` | `oem_catalog_no` | Primary SKU identifier |
| `make` | `catalog_skus` | `make` | SKU make |
| `oem_series` | `catalog_skus` | `oem_series_range` | SKU series |
| `item_producttype` | `product_types` | `code`, `name` | Lookup or create |
| `business_category` | `categories` | `code`, `name` | Lookup or create |
| `SC_L1` through `SC_L8` | `catalog_skus` | `sc_struct_jsonb` | Convert to JSONB object |
| `FIX_1_CODE` through `FIX_8_CODE` | `l1_attributes` | `attribute_code` | Fixed attributes |
| `FIX_1_VALUE` through `FIX_8_VALUE` | `l1_attributes` | `value_text` or `value_number` | Based on data type |
| `FIX_1_UNIT` through `FIX_8_UNIT` | `l1_attributes` | `value_unit` | Unit of measure |
| `ATTR_1_CODE` through `ATTR_8_CODE` | `l1_attributes` | `attribute_code` | Variable attributes |
| `ATTR_1_VALUE` through `ATTR_8_VALUE` | `l1_attributes` | `value_text` or `value_number` | Based on data type |
| `ATTR_1_UNIT` through `ATTR_8_UNIT` | `l1_attributes` | `value_unit` | Unit of measure |
| `l0_code`, `l0_name` | `categories`/`product_types` | `code`, `name` | L0 taxonomy |
| `l1_code`, `l1_name` | `l1_intent_lines` | `description` | L1 intent |
| `generic_item_name` | `l1_intent_lines` | `description` | Generic descriptor |
| `price_inr` | `sku_prices` | `price` | Numeric price |
| `currency` | `sku_prices` | `currency` | Currency code |
| `wef_date` | `sku_prices` | `effective_from` | Price effective date |
| `price_list_ref` | `price_lists` | `code` | Price list lookup |

### Source: ACCESSORIES_MASTER

**Same mapping as NSW_ITEM_MASTER_ENGINEER_VIEW** (same structure)

### Source: ACCESSORY_COMPATIBILITY

| Source Column | Target Table | Target Column | Transformation |
|---------------|--------------|---------------|----------------|
| `parent_make` | `accessory_compatibility` | `parent_make` | Direct |
| `parent_series_code` | `accessory_compatibility` | `parent_series_code` | Direct |
| `accessory_sku_code` | `accessory_compatibility` | `accessory_sku_code` | Direct |
| `applies_to_range` | `accessory_compatibility` | `applies_to_range` | Direct |
| `notes` | `accessory_compatibility` | `notes` | Direct |
| `source_page` | `accessory_compatibility` | `source_page` | Direct |

---

## 🔧 Implementation Details

### SC_Lx → JSONB Conversion

```python
def convert_sc_to_jsonb(row):
    """Convert SC_L1 through SC_L8 to JSONB structure"""
    sc_struct = {}
    for i in range(1, 9):
        col_name = f"SC_L{i}"
        value = row.get(col_name)
        if value is not None and str(value).strip() != "":
            sc_struct[f"l{i}"] = str(value).strip()
    return json.dumps(sc_struct) if sc_struct else None
```

### KVU Attribute Processing

```python
def process_kvu_attributes(row, prefix="FIX"):
    """Process FIX_* or ATTR_* columns into l1_attributes"""
    attributes = []
    for i in range(1, 9):
        code_col = f"{prefix}_{i}_CODE"
        value_col = f"{prefix}_{i}_VALUE"
        unit_col = f"{prefix}_{i}_UNIT"
        
        code = row.get(code_col)
        value = row.get(value_col)
        unit = row.get(unit_col)
        
        if code and value:
            attr = {
                "attribute_code": str(code).strip(),
                "value": value,  # Will be converted to text/number based on type
                "unit": str(unit).strip() if unit else None
            }
            attributes.append(attr)
    return attributes
```

### Idempotency Rules

1. **Makes/Series/Categories/Product Types:**
   - Lookup by `tenant_id + name/code`
   - Create if not exists
   - Update if exists (soft update - only if changed)

2. **Catalog SKUs:**
   - Lookup by `tenant_id + make + oem_catalog_no`
   - Update `sc_struct_jsonb` if changed
   - No duplicates

3. **L1 Attributes:**
   - Lookup by `l1_intent_line_id + attribute_code`
   - Update if value changed
   - No duplicates

4. **SKU Prices:**
   - Lookup by `sku_id + price_list_id + effective_from`
   - Insert new price if date changed
   - No duplicates

---

## 📝 Import Batch Tracking

### import_batches Table

Track each import run:

```sql
INSERT INTO import_batches (
    tenant_id,
    batch_code,
    source_file,
    status,
    total_rows,
    successful_rows,
    failed_rows,
    started_at,
    completed_at
) VALUES (...)
```

### Import Logs

Log validation errors and warnings:

```sql
INSERT INTO import_logs (
    import_batch_id,
    row_number,
    sheet_name,
    error_type,
    error_message,
    raw_data
) VALUES (...)
```

---

## 🧪 Testing Requirements

### Test Case 1: LC1D Import

**Input:** LC1D rows from NSW_ITEM_MASTER_ENGINEER_VIEW

**Verify:**
- ✅ Makes/Series created
- ✅ Catalog SKUs inserted with SC_Lx in JSONB
- ✅ L1 attributes created (FIX_* and ATTR_*)
- ✅ Prices inserted
- ✅ Idempotent (can run twice without duplicates)

### Test Case 2: EOCR Import

**Input:** EOCR rows from ITEM_TESYS_EOCR_WORK

**Verify:**
- ✅ Same processing path as LC1D
- ✅ Different attribute codes (TRIP_CLASS, etc.) handled correctly
- ✅ No product-specific branching

### Test Case 3: Accessories Import

**Input:** ACCESSORIES_MASTER sheet

**Verify:**
- ✅ Same processing path as other items
- ✅ Compatibility mappings inserted into `accessory_compatibility`
- ✅ No special handling needed

### Test Case 4: Mixed Import

**Input:** All sheets from normalized master

**Verify:**
- ✅ All product types processed uniformly
- ✅ No errors or warnings
- ✅ Complete import summary

---

## 📤 API Endpoints (Minimal for Week-1)

### POST /api/v1/catalog/import

**Request:**
```json
{
  "file_path": "/path/to/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx",
  "tenant_id": 1,
  "dry_run": false
}
```

**Response:**
```json
{
  "batch_id": 123,
  "status": "completed",
  "total_rows": 1026,
  "successful_rows": 1020,
  "failed_rows": 6,
  "errors": [...]
}
```

### GET /api/v1/catalog/import/{batch_id}

**Response:**
```json
{
  "batch_id": 123,
  "status": "completed",
  "started_at": "2026-01-03T10:00:00Z",
  "completed_at": "2026-01-03T10:05:00Z",
  "logs": [...]
}
```

---

## ✅ Success Criteria

1. ✅ Can import normalized master workbook
2. ✅ All product types processed uniformly (no branching)
3. ✅ Idempotent (can run multiple times)
4. ✅ SC_Lx stored as JSONB correctly
5. ✅ KVU attributes processed correctly
6. ✅ Prices imported correctly
7. ✅ Compatibility mappings imported
8. ✅ Import batch tracking works
9. ✅ Error logging works
10. ✅ Can query imported data via APIs

---

## 📋 Implementation Checklist

- [ ] Create import service class
- [ ] Implement SC_Lx → JSONB conversion
- [ ] Implement KVU attribute processing
- [ ] Implement taxonomy lookup/create
- [ ] Implement catalog SKU import
- [ ] Implement L1 intent lines import
- [ ] Implement L1 attributes import
- [ ] Implement pricing import
- [ ] Implement compatibility import
- [ ] Implement idempotency logic
- [ ] Implement import batch tracking
- [ ] Implement error logging
- [ ] Create API endpoints
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Test with LC1D data
- [ ] Test with EOCR data
- [ ] Test with Accessories data
- [ ] Test with mixed data
- [ ] Verify idempotency

---

**Status:** 📋 READY FOR IMPLEMENTATION  
**Priority:** HIGH (Week-1 Day 2-3)  
**Estimated Effort:** 2-3 days

---

## 🔍 Verification Status

**Track A (Legacy Business Decisions):** ⬜ PENDING / ✅ PASS / ❌ FAIL  
**Track B (NSW Fundamentals):** ⬜ PENDING / ✅ PASS / ❌ FAIL  
**Overall Verification:** ⬜ PENDING / ✅ VERIFIED / ❌ BLOCKED

**Track A Worksheet:** [Link to completed worksheet]  
**Verification Report:** [Link to verification report]

**Note:** Build completion requires both Track A (RETAIN items) and Track B to pass.

---

## 🔍 Standing Verification Requirement (v2.1)

**⚠️ MANDATORY:** This build MUST be verified in **PARALLEL** against **BOTH:**
1. **Track A:** Legacy Business-Decision Reference Audit (`project/nish/`) - Blocking only for RETAIN items
2. **Track B:** NSW Fundamental Alignment Plan (`NSW Fundamental Alignment Plan/`) - Always mandatory and blocking

**See:** `STANDING_VERIFICATION_INSTRUCTION.md` (v2.1) for complete dual verification process  
**Quick Reference:** `VERIFICATION_CHECKLIST_QUICK_REFERENCE.md` (v2.1) for fast checklist  
**Track A Worksheet:** `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md` (v1.0)

### Track A: Legacy Business-Decision Reference Audit

✅ **Business Decision Check** - Confirm we are not missing any business decision related to catalog import:
- Price list usage expectations
- Effective dating expectations (WEF date usage)
- Discount governance expectations
- Error handling expectations (operator workflow)
- Idempotency expectations
- Import completeness expectations

✅ **Tagging Required:**
- Tag any legacy requirement as **RETAIN** / **REPLACE** / **DROP**
- Block only if **RETAIN** is not met
- Use `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md`

❌ **Explicitly OUT OF SCOPE:**
- No legacy data migration in Phase-5
- No legacy schema/table parity in Phase-5
- No legacy import pipeline parity (compare behaviors, not implementation)

### Track B: NSW Fundamental Alignment Plan Verification Required

- ✅ Master Fundamentals v2.0 compliance (`01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`)
- ✅ L0/L1/L2 canonical rules compliance (`02_GOVERNANCE/NEPL_CANONICAL_RULES.md`)
- ✅ Governance standards compliance (`02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md`)
- ✅ Design document alignment (relevant component designs in `05_DESIGN_DOCUMENTS/`)
- ✅ Gap register verification (`02_GOVERNANCE/BOM_GAP_REGISTER.md`)
- ✅ Verification queries and checklist (`07_VERIFICATION/`)

**Verification Gate:**
- **Track B:** Always blocking - must PASS
- **Track A:** Blocking only for RETAIN-tagged items - must PASS for RETAIN items only
- Build completion blocked until **BOTH** verification reports approved

