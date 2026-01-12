# TESYS_PROTECT_ITEM_FULL_WORK.xlsx — Source File Reference

**File Name:** `TESYS_PROTECT_ITEM_FULL_WORK.xlsx`  
**Location:** `active/schneider/LC1E/00_inputs/`  
**Status:** ✅ Source Data File (Reference/Master Data)  
**Purpose:** Comprehensive item master data for TeSys product families — used for data connectivity verification and reference

---

## 📋 Overview

**Status:** ✅ **ALREADY ADOPTED** — This file has been adopted with sanity checks and corrections applied. All sheet names are registered and working.

**Adopted As:** `ITEM_Master_020126_v1.4_NORMALIZED.xlsx` (or `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`)  
**Adopted Location:** `tools/catalog_pipeline_v2/input/reviseditemmaster/`

This file contains consolidated item master data covering multiple Schneider TeSys product families. It serves as:

1. **Reference Data Source** — Comprehensive item definitions across product families
2. **Data Connectivity Check** — Verify compatibility with current Phase-5 pipeline structure
3. **Master Data Reference** — Contains L0/L1 level definitions, attributes, and pricing information

**Note:** This file has already been processed with all sanity checks and corrections. All 8 sheets are registered and working.

---

## 📊 File Structure

### Sheets Overview

**Total Sheets:** 8  
**Total Data Rows (All Sheets Combined): 1,026 rows**

| Sheet Name | Rows | Columns | Purpose | Status |
|------------|------|---------|---------|--------|
| `NSW_ITEM_MASTER_ENGINEER_VIEW` | 497 | 103 | Consolidated engineer view — master item data | ✅ Registered & Working |
| `ITEM_TESYS_EOCR_WORK` | 44 | 43 | EOCR (Electronic Overload Relays) item definitions | ✅ Registered & Working |
| `ITEM_TESYS_PROTECT_WORK` | 22 | 43 | TeSys Protect item definitions | ✅ Registered & Working |
| `ITEM_GIGA_SERIES_WORK` | 40 | 103 | Giga series item definitions | ✅ Registered & Working |
| `ITEM_K_SERIES_WORK` | 83 | 103 | K series item definitions | ✅ Registered & Working |
| `ITEM_CAPACITOR_DUTY_WORK` | 13 | 103 | Capacitor Duty item definitions | ✅ Registered & Working |
| `ACCESSORY_COMPATIBILITY` | 169 | 6 | Accessory compatibility mappings | ✅ Registered & Working |
| `ACCESSORIES_MASTER` | 158 | 43 | Accessories master data | ✅ Registered & Working |

**Note:** Row counts shown are data rows (excluding header row). Total of 1,026 rows represents all data across all 8 sheets combined.

---

## 🔑 Key Data Fields (NSW_ITEM_MASTER_ENGINEER_VIEW)

### Identity Fields
- `make` — Manufacturer (Schneider)
- `oem_series` — OEM series name
- `series_code` — Series code
- `sku_code` — SKU/product code
- `generic_item_code` — Generic item identifier

### Classification Fields
- `business_category` — Business category
- `business_segment` — Business segment
- `item_producttype` — Product type
- `l0_code`, `l0_name` — L0 level classification
- `l1_code`, `l1_name` — L1 level classification
- `SC_L1` through `SC_L8` — Structural Classification layers

### Attribute Fields (Key-Value-Unit)
- `FIX_1_CODE` through `FIX_8_CODE` — Fixed attribute codes
- `FIX_1_VALUE` through `FIX_8_VALUE` — Fixed attribute values
- `FIX_1_UNIT` through `FIX_8_UNIT` — Fixed attribute units
- `ATTR_1_CODE` through `ATTR_8_CODE` — Attribute codes
- `ATTR_1_VALUE` through `ATTR_8_VALUE` — Attribute values
- `ATTR_1_UNIT` through `ATTR_8_UNIT` — Attribute units

### Technical Specifications
- `poles` — Number of poles
- `duty_type`, `duty_current`, `duty_unit` — Duty specifications
- `coil_type`, `coil_voltage`, `coil_unit` — Coil specifications
- `aux_contacts` — Auxiliary contacts

### Pricing Fields
- `price_inr` — Price in INR
- `currency` — Currency code
- `wef_date` — With Effect From date
- `price_list_ref` — Price list reference

### Source Tracking
- `source_pdf` — Source PDF file
- `source_page` — Source page number
- `source_table` — Source table identifier
- `source_row` — Source row number
- `source_notes` — Source notes

### Quality Control
- `status` — Item status
- `qc_flag` — QC flag
- `qc_notes` — QC notes

---

## 🔄 Data Connectivity & Compatibility

### ✅ Compatible Elements

1. **Core Identity Data**
   - ✅ `make` field present (matches NSW format requirement)
   - ✅ `sku_code` present (equivalent to `l2_product_code` in NSW format)
   - ✅ `oem_series` present (equivalent to `series_name` in NSW format)

2. **Classification Structure**
   - ✅ L0/L1 level definitions present
   - ✅ SC_L1 through SC_L4 classification (matches Phase-5 requirements)
   - ✅ Generic item naming structure

3. **Pricing Data**
   - ✅ Price, currency, and effective date fields present
   - ✅ Source tracking for audit trail

4. **Product Coverage**
   - ✅ Multiple product families (EOCR, Protect, Giga, K, Capacitor Duty)
   - ✅ Accessory compatibility mappings
   - ✅ Comprehensive attribute structure

### ⚠️ Transformation Required

To align with Phase-5 NSW format (`NSW_L2_PRODUCTS`, `NSW_PRICE_MATRIX`, etc.), the following mappings/transformations would be needed:

| NSW Format Field | Source Field(s) | Notes |
|------------------|-----------------|-------|
| `l2_product_code` | `sku_code` | Direct mapping |
| `series_name` | `oem_series` | Direct mapping |
| `generic_name` | `generic_item_name` + `generic_item_description` | May require concatenation |
| `NSW_PRICE_MATRIX.Rate` | `price_inr` | Direct mapping |
| `NSW_PRICE_MATRIX.Currency` | `currency` | Direct mapping |
| `NSW_PRICE_MATRIX.EffectiveFrom` | `wef_date` | Date format conversion may be needed |

---

## 📍 Usage Guidelines

### As Source Data

1. **Reference Verification**
   - Use to verify data completeness across product families
   - Cross-check item definitions against Phase-5 pipeline outputs
   - Validate pricing data consistency

2. **Data Connectivity Checks**
   - Verify that current pipeline outputs align with this master data
   - Identify missing items or fields
   - Validate attribute mappings

3. **Sanity Corrections**
   - Note: Most data is available but may require sanity corrections
   - Use QC flags and notes to identify items needing review
   - Validate source tracking information

### Integration Notes

- **Not Direct Input** — This file is reference data, not a direct input to the Phase-5 pipeline
- **Transformation Required** — Data structure differs from NSW format (L1-level vs L2-level)
- **Multi-Family Coverage** — Contains multiple product families, not just LC1E
- **Attribute Rich** — Contains extensive attribute data (FIX/ATTR fields) useful for reference

---

## 🔗 Related Files

- **Phase-5 Output:** `02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx`
- **Input Pricelist:** `00_inputs/Switching _All_WEF 15th Jul 25.xlsx`
- **Governance Docs:** `governance/freeze_v1.2_clean/` (SoR Contract, SoE Guide)

---

## ✅ Status Confirmation

**File Status:** ✅ **ALREADY ADOPTED** — This file has been adopted with all sanity checks and corrections applied.  
**Sheet Registration:** ✅ **ALL 8 SHEETS REGISTERED & WORKING**  
**Data Availability:** ✅ Confirmed (1,026 total rows across all sheets)  
**Structure Compatibility:** ✅ Compatible (already processed and working)  
**Usefulness:** ✅ High value as reference/master data  
**Inline with Requirements:** ✅ Yes — Already adopted and working  

**Confirmation:**  
- ✅ File is already adopted with different name (processed version exists)
- ✅ All 8 sheet names are registered and working
- ✅ Total data rows: **1,026 rows** (sum of all sheets, not just one sheet)
- ✅ All sanity checks and corrections have been applied
- ✅ This file serves as the source reference for data connectivity verification

**Note:** The previous analysis showing only 497 rows was for the `NSW_ITEM_MASTER_ENGINEER_VIEW` sheet only. The complete file contains **1,026 total data rows** across all 8 sheets combined.

---

**Last Reviewed:** 2026-01-03  
**Review Status:** ✅ Approved as Source Reference File

