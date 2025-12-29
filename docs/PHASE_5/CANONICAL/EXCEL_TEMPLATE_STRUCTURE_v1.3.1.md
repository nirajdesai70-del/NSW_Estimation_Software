# Excel Template Structure v1.3.1 - SKU-First Approach

**Version:** 1.3.1  
**Date:** 2025-01-27  
**Status:** LOCKED - FINAL  
**Purpose:** Excel template structure for L2-first import approach

---

## Workbook Name

**Proposed:** `NSW_MASTER_v1.3.1_SKU_FIRST.xlsx`

---

## Sheet A: L2_SKU_MASTER (IMPORTABLE)

**Purpose:** One row = one OEM catalog number (SKU). No AC1/AC3 duplication.

### Columns (Exact Order)

| Column # | Column Name | Required | Type | Default | Description | Example |
|----------|-------------|----------|------|---------|-------------|---------|
| 1 | Make | ✅ | Text | - | OEM manufacturer | Schneider |
| 2 | OEM_Catalog_No | ✅ | Text | - | SKU (unique identifier) | LC1E0601 |
| 3 | OEM_Series_Range | ✅ | Text | - | Series name | Easy TeSys |
| 4 | SeriesBucket | ✅ | Text | - | Series code | LC1E |
| 5 | Item_ProductType | ✅ | Text | - | Product type | Contactor |
| 6 | Business_SubCategory | ✅ | Text | - | Business subcategory | Power Contactor |
| 7 | UOM | Optional | Text | EA | Unit of measure | EA |
| 8 | IsActive | Optional | Boolean | TRUE | Active status | TRUE |
| 9 | SourceFile | Optional | Text | - | Source file name | schneider_price_list_2025.xlsx |
| 10 | SourcePageOrTableId | Optional | Text | - | Page/table identifier | Page 45 |
| 11 | SourceRow | Optional | Integer | - | Source row number | 123 |
| 12 | Notes | Optional | Text | - | Notes | Reference notes |

### Rules

- ✅ **Unique Key:** (Make + OEM_Catalog_No)
- ✅ **No AC1/AC3 duplication:** One SKU = One row
- ✅ **No duty/rating columns:** These are L1 attributes, not L2

### Example Data

| Make | OEM_Catalog_No | OEM_Series_Range | SeriesBucket | Item_ProductType | Business_SubCategory | UOM | IsActive |
|------|----------------|------------------|--------------|------------------|---------------------|-----|----------|
| Schneider | LC1E0601 | Easy TeSys | LC1E | Contactor | Power Contactor | EA | TRUE |
| Schneider | LC1D25 | TeSys Deca | LC1D | Contactor | Power Contactor | EA | TRUE |
| Schneider | LP1K0601 | TeSys K | LP1K | MPCB | MPCB | EA | TRUE |

---

## Sheet B: L2_PRICE_HISTORY (IMPORTABLE, append-only)

**Purpose:** One row = one price record per SKU per price list version.

### Columns (Exact Order)

| Column # | Column Name | Required | Type | Default | Description | Example |
|----------|-------------|----------|------|---------|-------------|---------|
| 1 | Make | ✅ | Text | - | OEM manufacturer | Schneider |
| 2 | OEM_Catalog_No | ✅ | Text | - | SKU | LC1E0601 |
| 3 | PriceListRef | ✅ | Text | - | Price list reference | Jul-2025 |
| 4 | EffectiveFrom | ✅ | Date | - | Effective date (YYYY-MM-DD) | 2025-07-01 |
| 5 | Currency | ✅ | Text | INR | Currency | INR |
| 6 | Region | ✅ | Text | INDIA | Region | INDIA |
| 7 | Rate | ✅ | Number | - | Price (numeric) | 2875.00 |
| 8 | ImportBatchId | Optional | Text | - | Import batch identifier | BATCH_20250127_001 |
| 9 | SourceFile | Optional | Text | - | Source file name | schneider_price_list_2025.xlsx |
| 10 | SourceRow | Optional | Integer | - | Source row number | 123 |
| 11 | Notes | Optional | Text | - | Notes | Reference notes |

### Rules

- ✅ **Append-Only:** Never overwrite old rates; always insert new rows
- ✅ **SKU Must Exist:** SKU must exist in L2_SKU_MASTER (or auto-create blocked per ADR-005)

### Example Data

| Make | OEM_Catalog_No | PriceListRef | EffectiveFrom | Currency | Region | Rate |
|------|----------------|--------------|----------------|----------|--------|------|
| Schneider | LC1E0601 | Jul-2025 | 2025-07-01 | INR | INDIA | 2875.00 |
| Schneider | LC1E0601 | Aug-2025 | 2025-08-01 | INR | INDIA | 3000.00 |
| Schneider | LC1D25 | Jul-2025 | 2025-07-01 | INR | INDIA | 4500.00 |

---

## Sheet C: L1_DUTY_RATING_MAP (ENGINEERING RULE SHEET - NOT L2 IMPORT)

**Purpose:** This is where "same SKU has AC1 and AC3 ratings" is captured. Not L2.

### Columns

| Column # | Column Name | Required | Type | Description | Example |
|----------|-------------|----------|------|-------------|---------|
| 1 | Item_ProductType | ✅ | Text | Product type | Contactor |
| 2 | SeriesBucket | ✅ | Text | Series code | LC1E |
| 3 | DutyClass | ✅ | Text | Duty class | AC1 / AC3 |
| 4 | RatingAttributeCode | ✅ | Text | Attribute code | AC1_CURRENT_A / AC3_CURRENT_A |
| 5 | RatingValue | ✅ | Number | Rating value | 20 / 6 |
| 6 | RatingUnit | ✅ | Text | Unit | A |
| 7 | AppliesWhen | Optional | Text | Rule condition | "if table provides AC1/AC3 columns" |
| 8 | Notes | Optional | Text | Notes | Reference notes |

### Rules

- ✅ **NOT imported as L2:** This is engineering knowledge, not commercial data
- ✅ **Drives auto-L1 creation:** System uses this to generate L1 lines
- ✅ **Can be edited by engineering:** Engineers can update these rules

### Example Data

| Item_ProductType | SeriesBucket | DutyClass | RatingAttributeCode | RatingValue | RatingUnit | AppliesWhen |
|------------------|--------------|-----------|---------------------|--------------|-------------|-------------|
| Contactor | LC1E | AC1 | AC1_CURRENT_A | 20 | A | if table provides AC1/AC3 columns |
| Contactor | LC1E | AC3 | AC3_CURRENT_A | 6 | A | if table provides AC1/AC3 columns |
| Contactor | LC1D | AC1 | AC1_CURRENT_A | 25 | A | if table provides AC1/AC3 columns |
| Contactor | LC1D | AC3 | AC3_CURRENT_A | 9 | A | if table provides AC1/AC3 columns |

---

## Sheet D: L1_COIL_SUFFIX_RULES (ENGINEERING RULE SHEET - NOT L2 IMPORT)

**Purpose:** Defines how SKU is completed when OEM uses suffix logic.

### Columns

| Column # | Column Name | Required | Type | Description | Example |
|----------|-------------|----------|------|-------------|---------|
| 1 | SeriesBucket | ✅ | Text | Series code | LC1E |
| 2 | VoltageType | ✅ | Text | Voltage type | AC / DC |
| 3 | VoltageValue | ✅ | Number | Voltage value | 24 / 110 / 220 / 415 |
| 4 | VoltageUnit | ✅ | Text | Unit | V |
| 5 | OemSuffixCode | ✅ | Text | OEM suffix code | M7 / N7 / BD / FD / MD |
| 6 | SuffixPlacementRule | ✅ | Text | Placement rule | APPEND / REPLACE / APPEND_WITH_SEPARATOR |
| 7 | ExampleBaseSku | Optional | Text | Example base SKU | LC1E0601 |
| 8 | ExampleFinalSku | Optional | Text | Example final SKU | LC1E0601M7 |
| 9 | Notes | Optional | Text | Notes | Reference notes |

### Rules

- ✅ **NOT imported as L2:** This is engineering knowledge, not commercial data
- ✅ **Drives SKU completion:** System uses this to complete SKU when voltage suffix is needed

### Example Data

| SeriesBucket | VoltageType | VoltageValue | VoltageUnit | OemSuffixCode | SuffixPlacementRule | ExampleBaseSku | ExampleFinalSku |
|--------------|-------------|--------------|-------------|---------------|---------------------|----------------|----------------|
| LC1E | AC | 24 | V | M7 | APPEND | LC1E0601 | LC1E0601M7 |
| LC1E | AC | 110 | V | N7 | APPEND | LC1E0601 | LC1E0601N7 |
| LC1E | AC | 220 | V | BD | APPEND | LC1E0601 | LC1E0601BD |
| LC1E | AC | 415 | V | FD | APPEND | LC1E0601 | LC1E0601FD |

---

## Sheet E: FEATURE_POLICY (ENGINEERING RULE SHEET - NOT L2 IMPORT)

**Purpose:** Controls if accessories create L2 SKUs when selected.

### Columns

| Column # | Column Name | Required | Type | Description | Example |
|----------|-------------|----------|------|-------------|---------|
| 1 | Make | ✅ | Text | Make name | Schneider |
| 2 | SeriesBucket | Optional | Text | Series code | LC1E |
| 3 | Item_ProductType | ✅ | Text | Product type | Contactor |
| 4 | Feature_Code | ✅ | Text | Feature code | AUX / OLR / SUPPRESSOR / INTERLOCK |
| 5 | Handling_Type | ✅ | Text | Handling type | INCLUDED_IN_BASE / ADDON_SKU_REQUIRED / BUNDLED_ALTERNATE_BASE |
| 6 | Addon_OEM_Catalog_No | Optional | Text | Addon SKU (if ADDON) | LC1E0601AUX |
| 7 | Priority | ✅ | Integer | Priority (1=Series, 2=Make, 3=Global) | 1 / 2 / 3 |
| 8 | EffectiveFrom | Optional | Date | Effective from date | 2025-01-01 |
| 9 | EffectiveTo | Optional | Date | Effective to date | 2025-12-31 |
| 10 | Notes | Optional | Text | Notes | Reference notes |

### Rules

- ✅ **NOT imported as L2:** This is engineering policy, not commercial data
- ✅ **Drives feature handling:** System uses this to determine if accessories create SKUs
- ✅ **Priority resolution:** Series → Make → Global → else BLOCK

### Example Data

| Make | SeriesBucket | Item_ProductType | Feature_Code | Handling_Type | Addon_OEM_Catalog_No | Priority |
|------|--------------|------------------|--------------|---------------|----------------------|----------|
| Schneider | LC1E | Contactor | AUX | ADDON_SKU_REQUIRED | LC1E0601AUX | 1 |
| Schneider | LC1E | Contactor | OLR | ADDON_SKU_REQUIRED | LC1E0601OLR | 1 |
| Schneider | LC1D | Contactor | AUX | INCLUDED_IN_BASE | - | 1 |
| Schneider | - | Contactor | SUPPRESSOR | ADDON_SKU_REQUIRED | - | 3 |

---

## Import Workflow

### Step 1: Import L2 SKU Master (Sheet A)

```
1. Upload Excel file
2. System reads L2_SKU_MASTER sheet
3. Validates required fields
4. Upserts by (Make, OEM_Catalog_No)
5. Returns: created/updated counts
```

### Step 2: Import L2 Price History (Sheet B)

```
1. Upload Excel file
2. System reads L2_PRICE_HISTORY sheet
3. Validates required fields
4. Checks SKU exists in L2_SKU_MASTER
5. Creates price_list if PriceListRef is new
6. Inserts price rows (append-only)
7. Returns: prices_inserted count
```

### Step 3: Derive L1 (Optional - Uses Sheets C, D, E)

```
1. System reads L1_DERIVATION_RULES (Sheet C)
2. System reads L1_COIL_SUFFIX_RULES (Sheet D)
3. System reads FEATURE_POLICY (Sheet E)
4. For each L2 SKU:
   - Apply derivation rules
   - Generate L1 BASE lines (AC1, AC3, etc.)
   - Generate L1 FEATURE lines (if needed)
   - All map to same L2 SKU
5. Returns: l1_lines_created count
```

---

## Validation Rules

### L2 SKU Master Validation

- ✅ Make must be present
- ✅ OEM_Catalog_No must be present
- ✅ SeriesBucket must be present
- ✅ Item_ProductType must be present
- ✅ Business_SubCategory must be present
- ✅ Unique constraint: (Make, OEM_Catalog_No)

### L2 Price History Validation

- ✅ SKU must exist in L2_SKU_MASTER (or auto-create blocked per ADR-005)
- ✅ PriceListRef must be present
- ✅ EffectiveFrom must be present and valid date
- ✅ Rate must be numeric and >= 0
- ✅ Currency must be present (default: INR)
- ✅ Region must be present (default: INDIA)

---

## What Engineers Must Still Fill

**Mandatory Engineer Inputs (cannot come from price list):**

| Field | Why |
|-------|-----|
| Duty interpretation (AC1/AC3) | OEM catalogs mix this |
| Rating selection logic | AC1 ≠ AC3 current |
| Voltage applicability | Often implicit |
| Feature intent (OLR / Aux / Coil) | Commercially separate |
| Application constraints | Not priced |

**This is correct and unavoidable. Price lists can never fully define L1.**

---

## References

- **L2 Import Structure:** `docs/PHASE_5/CANONICAL/L2_IMPORT_STRUCTURE_v1.3.1.md`
- **OpenAPI Contract:** `docs/PHASE_5/CANONICAL/openapi_l2_first.yaml`
- **Phase 5 Impact Assessment:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_PRICE_LIST_IMPACT_ASSESSMENT.md`
- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`

---

**Document Status:** ✅ **LOCKED - FINAL**

**Next Step:** Create actual Excel template file with these sheets and headers prefilled.

