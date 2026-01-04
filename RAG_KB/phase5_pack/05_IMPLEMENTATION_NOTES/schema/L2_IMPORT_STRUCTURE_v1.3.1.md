---
Source: docs/PHASE_5/CANONICAL/L2_IMPORT_STRUCTURE_v1.3.1.md
KB_Namespace: phase5_docs
Status: WORKING
Last_Updated: 2025-12-27T10:59:25.269192
KB_Path: phase5_pack/05_IMPLEMENTATION_NOTES/schema/L2_IMPORT_STRUCTURE_v1.3.1.md
---

# L2 Import Structure v1.3.1 - SKU-First Approach

**Version:** 1.3.1  
**Date:** 2025-01-27  
**Status:** LOCKED - FINAL  
**Purpose:** Final L2 import structure aligned to NSW Fundamentals v2.0

---

## Core Principle (LOCKED)

> **Price list import creates L2-only records. L1 and L0 are derived, not imported.**

**Final Rule:**
> **If a field is not mandatory for L2, it must not be imported.**

---

## L2 MASTER (SKU Table) - FINAL FIELDS

### Required Fields

| Field | Type | Required | Meaning | Example |
|-------|------|----------|---------|---------|
| Make | VARCHAR(255) | ✅ | OEM manufacturer | Schneider |
| OEM_Catalog_No | VARCHAR(100) | ✅ | SKU (unique identifier) | LC1E0601, LC1D25*, LP1K0601 |
| OEM_Series_Range | VARCHAR(255) | ✅ | Series name | Easy TeSys / TeSys Deca / TeSys K |
| SeriesBucket | VARCHAR(100) | ✅ | Series code | LC1E/LC1D/LP1K/GV/EOCR |
| Item_ProductType | VARCHAR(100) | ✅ | Product type | Contactor / Control Relay / MPCB |
| Business_SubCategory | VARCHAR(100) | ✅ | Business subcategory | Power Contactor / Control Relay / MPCB |
| UOM | VARCHAR(50) | Optional | Unit of measure (default: EA) | EA |
| IsActive | BOOLEAN | Optional | Active status (default: TRUE) | TRUE |
| SourceFile | VARCHAR(255) | Optional | Source file name | schneider_price_list_2025.xlsx |
| SourcePageOrTableId | VARCHAR(100) | Optional | Page/table identifier | Page 45, Table 2 |
| SourceRow | INTEGER | Optional | Source row number | 123 |
| Notes | TEXT | Optional | Notes | Reference notes |

### Unique Constraint

**Unique Key:** `(Make, OEM_Catalog_No)`

---

## Fields NOT ALLOWED in L2 Import ❌

**These are engineering interpretations, not commercial truth:**

- ❌ Duty (AC1 / AC3)
- ❌ Rating interpretation (20A vs 6A)
- ❌ Poles as multipliers
- ❌ NO/NC meaning
- ❌ Frame size as multiplier
- ❌ Feature logic
- ❌ Voltage values (only Voltage_Class allowed: AC/DC)

**Where These Go:**
- ✅ L1 derivation rules (engineering rule sheets)
- ✅ L1 attributes (after derivation)

---

## L2 PRICE HISTORY - FINAL FIELDS

### Required Fields

| Field | Type | Required | Meaning | Example |
|-------|------|----------|---------|---------|
| Make | VARCHAR(255) | ✅ | OEM manufacturer | Schneider |
| OEM_Catalog_No | VARCHAR(100) | ✅ | SKU | LC1E0601 |
| PriceListRef | VARCHAR(255) | ✅ | Price list reference | Jul-2025 |
| EffectiveFrom | DATE | ✅ | Effective date | 2025-07-01 |
| Currency | VARCHAR(10) | ✅ | Currency (default: INR) | INR |
| Region | VARCHAR(100) | ✅ | Region (default: INDIA) | INDIA |
| Rate | NUMERIC(15,2) | ✅ | Price (numeric) | 2875.00 |
| ImportBatchId | VARCHAR(100) | Optional | Import batch identifier | BATCH_20250127_001 |
| SourceFile | VARCHAR(255) | Optional | Source file name | schneider_price_list_2025.xlsx |
| SourceRow | INTEGER | Optional | Source row number | 123 |
| Notes | TEXT | Optional | Notes | Reference notes |

### Rules

1. **Append-Only:** Never overwrite old rates; always insert new rows
2. **Price List Versioning:** Each PriceListRef + EffectiveFrom = new price record
3. **SKU Must Exist:** SKU must exist in L2_SKU_MASTER before price import (or auto-create blocked per ADR-005)

---

## Import Workflow

### Step 1: Import L2 SKU Master

```
OEM Price List
   ↓
Extract: Make, SKU, Series, Item, SubCategory
   ↓
Import to L2_SKU_MASTER
   ↓
Upsert by (Make, OEM_Catalog_No)
```

### Step 2: Import L2 Price History

```
OEM Price List
   ↓
Extract: Make, SKU, PriceListRef, EffectiveFrom, Rate
   ↓
Import to L2_PRICE_HISTORY
   ↓
Insert new rows (append-only)
```

### Step 3: Derive L1 (System-Driven, Not Import)

```
L2 SKU (LC1E0601)
   ↓
Apply L1_DERIVATION_RULES
   ↓
Generate L1 lines (AC1, AC3, etc.)
   ↓
All map to same L2 SKU
```

---

## Example: LC1E0601

### L2 Import (Single Row)

```
Make: Schneider
OEM_Catalog_No: LC1E0601
OEM_Series_Range: Easy TeSys
SeriesBucket: LC1E
Item_ProductType: Contactor
Business_SubCategory: Power Contactor
UOM: EA
IsActive: TRUE
```

### L2 Price (Single Row)

```
Make: Schneider
OEM_Catalog_No: LC1E0601
PriceListRef: Jul-2025
EffectiveFrom: 2025-07-01
Currency: INR
Region: INDIA
Rate: 2875.00
```

### L1 Derivation (Multiple Rows - System Generated)

```
L1-A: AC1, 20A, 3P, 220V → LC1E0601
L1-B: AC3, 6A, 3P, 220V → LC1E0601
L1-C: AC1, 20A, 3P, 415V → LC1E0601
L1-D: AC3, 6A, 3P, 415V → LC1E0601
```

**All map to same L2 SKU (LC1E0601) with same price (₹2875)**

---

## Validation Rules

### L2 SKU Master Validation

1. ✅ Make must be present
2. ✅ OEM_Catalog_No must be present
3. ✅ SeriesBucket must be present
4. ✅ Item_ProductType must be present
5. ✅ Business_SubCategory must be present
6. ✅ Unique constraint: (Make, OEM_Catalog_No)

### L2 Price History Validation

1. ✅ SKU must exist in L2_SKU_MASTER (or auto-create blocked per ADR-005)
2. ✅ PriceListRef must be present
3. ✅ EffectiveFrom must be present
4. ✅ Rate must be numeric and >= 0
5. ✅ Currency must be present (default: INR)
6. ✅ Region must be present (default: INDIA)

---

## Database Mapping

### L2 SKU Master → Database Table

**Table:** `catalog_skus` (or `l2_skus`)

**Mapping:**
- Make → `make` (VARCHAR)
- OEM_Catalog_No → `oem_catalog_no` (VARCHAR, UNIQUE with make)
- OEM_Series_Range → `oem_series_range` (VARCHAR)
- SeriesBucket → `series_bucket` (VARCHAR)
- Item_ProductType → `item_producttype` (VARCHAR)
- Business_SubCategory → `business_subcategory` (VARCHAR)
- UOM → `uom` (VARCHAR, default: 'EA')
- IsActive → `is_active` (BOOLEAN, default: TRUE)

### L2 Price History → Database Table

**Table:** `sku_prices` (or `l2_prices`)

**Mapping:**
- Make → `make` (VARCHAR)
- OEM_Catalog_No → `oem_catalog_no` (VARCHAR, FK to catalog_skus)
- PriceListRef → `pricelist_ref` (VARCHAR)
- EffectiveFrom → `effective_from` (DATE)
- Currency → `currency` (VARCHAR, default: 'INR')
- Region → `region` (VARCHAR, default: 'INDIA')
- Rate → `rate` (NUMERIC(15,2))

---

## References

- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Schneider L2/L1 Differentiation:** `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`
- **Phase 5 Impact Assessment:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_PRICE_LIST_IMPACT_ASSESSMENT.md`

---

**Document Status:** ✅ **LOCKED - FINAL**

**Next Step:** Use this structure for Excel template and API implementation.

