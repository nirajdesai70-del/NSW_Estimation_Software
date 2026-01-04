# All Series Processing Plan - Normalized Item Master

**Date:** 2026-01-03  
**Status:** 📋 PLANNING  
**Source File (Normalized):** `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`  
**Source File (Original):** `TESYS_PROTECT_ITEM_FULL_WORK.xlsx` (reference only)  
**Location:** `tools/catalog_pipeline_v2/input/reviseditemmaster/` (expected)  
**Reference:** LC1E processing completed as template

**Note:** The normalized file has the same data as TESYS_PROTECT_ITEM_FULL_WORK.xlsx, but with normalized/cleaned structure. Use the normalized version for all processing.

---

## 📊 Source File Analysis

### Normalized File Structure

**File:** `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`  
**Location:** `tools/catalog_pipeline_v2/input/reviseditemmaster/`  
**Status:** ✅ Clean and aligned version (normalized structure, same data)

### File Structure (Same as Original, Normalized Format)

| Sheet Name | Rows | Purpose | Series/Items Contained |
|------------|------|---------|----------------------|
| `NSW_ITEM_MASTER_ENGINEER_VIEW` | 497 | Consolidated master view | LC1D (332), LC1E (165) |
| `ITEM_TESYS_EOCR_WORK` | 44 | EOCR items | TeSys Protect EOCR (44) |
| `ITEM_TESYS_PROTECT_WORK` | 22 | Protect items | TeSys K (14), TeSys Deca (4), TeSys Giga (4) |
| `ITEM_GIGA_SERIES_WORK` | 40 | Giga series | TeSys Giga Power Contactor (40) |
| `ITEM_K_SERIES_WORK` | 83 | K series | Power Contactor (43), Control Relay (24), Reversing Contactor (16) |
| `ITEM_CAPACITOR_DUTY_WORK` | 13 | Capacitor Duty | Capacitor Duty Contactor (13) |
| `ACCESSORY_COMPATIBILITY` | 169 | Compatibility mappings | Cross-series compatibility |
| `ACCESSORIES_MASTER` | 158 | Accessories master | TeSys Deca (85), Giga (27), Easy TeSys (22), K (13), EOCR (11) |

**Total Items:** 1,026 rows across all sheets

**Key Difference:** Normalized file has cleaned/aligned structure but same data content as `TESYS_PROTECT_ITEM_FULL_WORK.xlsx`

---

## 🎯 Series Identified for Processing

### ✅ Completed
1. **LC1E** (Easy TeSys) - 165 items
   - Status: ✅ Complete
   - Output: `NSW_LC1E_WEF_2025-07-15_v1.xlsx`
   - Location: `active/schneider/LC1E/02_outputs/`

### ⏳ To Be Processed

2. **LC1D** (Easy TeSys) - 332 items
   - Source: `NSW_ITEM_MASTER_ENGINEER_VIEW` (filter: `series_code == 'LC1D'`)
   - Product Type: Contactor / Control Contactor
   - Similar to LC1E structure

3. **LC1K / TeSys K** - 83 items
   - Source: `ITEM_K_SERIES_WORK`
   - Product Types: Power Contactor (43), Control Relay (24), Reversing Contactor (16)
   - Mixed product types

4. **GIG / TeSys Giga** - 40 items
   - Source: `ITEM_GIGA_SERIES_WORK`
   - Product Type: Power Contactor (40)

5. **EOCR / TeSys Protect EOCR** - 44 items
   - Source: `ITEM_TESYS_EOCR_WORK`
   - Product Type: EOCR (Electronic Overload Relay)

6. **Protect / TeSys Protect** - 22 items
   - Source: `ITEM_TESYS_PROTECT_WORK`
   - Product Types: Thermal Overload Relay (14), Electronic Overload Relay (8)
   - Includes: TeSys K (14), TeSys Deca (4), TeSys Giga (4)

7. **Capacitor Duty** - 13 items
   - Source: `ITEM_CAPACITOR_DUTY_WORK`
   - Product Type: Capacitor Duty Contactor (13)

8. **Accessories** - 158 items
   - Source: `ACCESSORIES_MASTER`
   - Product Types: Accessory (140), Control Relay (6), Aux Contact Block (5), Mechanical Interlock (4), Surge Suppressor (2), Timer (1)
   - Series: TeSys Deca (85), Giga (27), Easy TeSys (22), K (13), EOCR (11)

9. **Accessory Compatibility** - 169 mappings
   - Source: `ACCESSORY_COMPATIBILITY`
   - Purpose: Cross-series compatibility mappings (not a series, but needs processing)

---

## 📋 Processing Approach

### Phase 5 Pipeline Steps (Per Series)

Each series will follow the same 8-step process used for LC1E:

1. **Step 0: Data Extraction** - Extract series data from source file
2. **Step 1: Canonical Extraction** - Create canonical tables (base refs, prices, accessories)
3. **Step 2: L2 Build** - Build L2 SKU layer (identity + SKU codes)
4. **Step 3: L1 Derivation** - Derive L1 configuration lines (duty × voltage × attributes)
5. **Step 4: Variant System** - Build variant master and product-variant mappings
6. **Step 5: NSW Workbook Generation** - Generate final NSW format workbook
7. **Step 6: QC** - Quality control validation
8. **Step 7: Governance Review** - ChatGPT approval
9. **Step 8: Archive** - Archive approved outputs

---

## 🗂️ Folder Structure (Per Series)

```
active/schneider/
├── LC1E/                    ✅ Complete
│   ├── 00_inputs/
│   ├── 01_scripts/
│   ├── 02_outputs/
│   ├── 03_qc/
│   └── 04_docs/
├── LC1D/                    ⏳ To Process
│   ├── 00_inputs/
│   ├── 01_scripts/
│   ├── 02_outputs/
│   ├── 03_qc/
│   └── 04_docs/
├── LC1K/                    ⏳ To Process
├── GIG/                     ⏳ To Process
├── EOCR/                    ⏳ To Process
├── PROTECT/                 ⏳ To Process
├── CAPACITOR_DUTY/          ⏳ To Process
└── ACCESSORIES/             ⏳ To Process
```

---

## 📝 Series-by-Series Processing Plan

### 1. LC1D (Easy TeSys) - 332 items

**Source:** `NSW_ITEM_MASTER_ENGINEER_VIEW` (filter: `series_code == 'LC1D'`)

**Characteristics:**
- Similar structure to LC1E
- Product Type: Contactor / Control Contactor
- Likely has duty classes (AC1/AC3), coil voltages, frames

**Processing Steps:**
1. Extract LC1D rows from normalized master view (`ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`)
2. Identify canonical structure (base refs, coil codes, prices)
3. Follow LC1E pipeline pattern
4. Generate `NSW_LC1D_WEF_2025-07-15_v1.xlsx`

**Source File:** `tools/catalog_pipeline_v2/input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`  
**Source Sheet:** `NSW_ITEM_MASTER_ENGINEER_VIEW` (filter: `series_code == 'LC1D'`)

**Expected Output:**
- L2 Products: ~X SKUs (TBD after extraction)
- L1 Config Lines: ~X lines (TBD after L1 derivation)
- Price Matrix: ~X prices (TBD)

**Note:** KVU ingestion is uniform; duty/voltage are just attribute codes and values. Same processing path as LC1E.

---

### 2. LC1K / TeSys K - 83 items

**Source:** `ITEM_K_SERIES_WORK`

**Characteristics:**
- Mixed product types: Power Contactor (43), Control Relay (24), Reversing Contactor (16)
- May need separate processing per product type

**Processing Steps:**
1. Extract from `ITEM_K_SERIES_WORK` sheet
2. **Option A:** Process as single series with product type differentiation
3. **Option B:** Split by product type (Power Contactor, Control Relay, Reversing Contactor)
4. Follow Phase 5 pipeline for each product type

**Expected Output:**
- Option A: Single workbook `NSW_LC1K_WEF_2025-07-15_v1.xlsx`
- Option B: Multiple workbooks per product type

**Special Considerations:**
- Mixed product types may require different L1 derivation rules
- Control Relay may have different attributes than Contactor
- Reversing Contactor may have special attributes

---

### 3. GIG / TeSys Giga - 40 items

**Source:** `ITEM_GIGA_SERIES_WORK`

**Characteristics:**
- Product Type: Power Contactor (40)
- Similar structure to LC1E/LC1D

**Processing Steps:**
1. Extract from `ITEM_GIGA_SERIES_WORK` sheet
2. Follow LC1E pipeline pattern
3. Generate `NSW_GIG_WEF_2025-07-15_v1.xlsx`

**Expected Output:**
- L2 Products: ~40 SKUs (or fewer if variants)
- L1 Config Lines: ~X lines (TBD)
- Price Matrix: ~X prices (TBD)

**Special Considerations:**
- Check for unique Giga-specific attributes
- Verify coil codes and duty classes

---

### 4. EOCR / TeSys Protect EOCR - 44 items

**Source:** `ITEM_TESYS_EOCR_WORK`

**Characteristics:**
- Product Type: EOCR (Electronic Overload Relay)
- Different from contactors - may have different attribute structure

**Processing Steps:**
1. Extract from `ITEM_TESYS_EOCR_WORK` sheet
2. Follow same Phase 5 pipeline (same structure, different attribute codes)
3. Generate `NSW_EOCR_WEF_2025-07-15_v1.xlsx`

**Note:** Same KVU ingestion; different attribute codes (e.g., TRIP_CLASS instead of DUTY_CURRENT), but same structure and processing path.

**Expected Output:**
- L2 Products: ~44 SKUs (or fewer if variants)
- L1 Config Lines: ~X lines (TBD)
- Price Matrix: ~X prices (TBD)

**Special Considerations:**
- ✅ Same structure as all other items (SC_Lx + KVU attributes)
- ✅ Different attribute codes (e.g., TRIP_CLASS instead of DUTY_CURRENT)
- ✅ Same processing path - no product-specific logic needed

---

### 5. PROTECT / TeSys Protect - 22 items

**Source:** `ITEM_TESYS_PROTECT_WORK`

**Characteristics:**
- Product Types: Thermal Overload Relay (14), Electronic Overload Relay (8)
- Includes: TeSys K (14), TeSys Deca (4), TeSys Giga (4)
- May overlap with EOCR sheet

**Processing Steps:**
1. Extract from `ITEM_TESYS_PROTECT_WORK` sheet
2. Analyze overlap with EOCR and K series
3. Decide: Process separately or merge with related series
4. Follow Phase 5 pipeline
5. Generate `NSW_PROTECT_WEF_2025-07-15_v1.xlsx`

**Expected Output:**
- L2 Products: ~22 SKUs (or fewer if variants)
- L1 Config Lines: ~X lines (TBD)
- Price Matrix: ~X prices (TBD)

**Special Considerations:**
- Overlap with EOCR and K series needs resolution
- Thermal vs Electronic may have different attributes
- May need to coordinate with EOCR processing

---

### 6. CAPACITOR_DUTY - 13 items

**Source:** `ITEM_CAPACITOR_DUTY_WORK`

**Characteristics:**
- Product Type: Capacitor Duty Contactor (13)
- Specialized contactor type

**Processing Steps:**
1. Extract from `ITEM_CAPACITOR_DUTY_WORK` sheet
2. Follow LC1E pipeline pattern
3. Generate `NSW_CAPACITOR_DUTY_WEF_2025-07-15_v1.xlsx`

**Expected Output:**
- L2 Products: ~13 SKUs (or fewer if variants)
- L1 Config Lines: ~X lines (TBD)
- Price Matrix: ~X prices (TBD)

**Special Considerations:**
- Small dataset - may be straightforward
- Check for capacitor-specific attributes

---

### 7. ACCESSORIES - 158 items

**Source:** `ACCESSORIES_MASTER`

**Characteristics:**
- Product Types: Accessory (140), Control Relay (6), Aux Contact Block (5), Mechanical Interlock (4), Surge Suppressor (2), Timer (1)
- Series: TeSys Deca (85), Giga (27), Easy TeSys (22), K (13), EOCR (11)
- Cross-series compatibility

**Processing Steps:**
1. Extract from `ACCESSORIES_MASTER` sheet
2. Follow same Phase 5 pipeline (same structure as all items)
3. Process compatibility mappings from `ACCESSORY_COMPATIBILITY` sheet
4. Generate `NSW_ACCESSORIES_WEF_2025-07-15_v1.xlsx`

**Note:** Accessories are first-class catalog items. Same structure (SC_Lx + KVU), same processing path. Compatibility stored as reference data only.

**Expected Output:**
- L2 Products: ~158 SKUs (or fewer if variants)
- L1 Config Lines: ~X lines (TBD)
- Price Matrix: ~X prices (TBD)
- Compatibility mappings: Reference `ACCESSORY_COMPATIBILITY` sheet

**Special Considerations:**
- ✅ Same structure as all other items (SC_Lx + KVU attributes)
- ✅ First-class catalog items (no special handling needed)
- ✅ Compatibility mappings stored in `accessory_compatibility` table (reference only, no enforcement in Phase-5)
- ✅ Same processing path - no product-specific logic needed

---

### 8. ACCESSORY_COMPATIBILITY - 169 mappings

**Source:** `ACCESSORY_COMPATIBILITY`

**Characteristics:**
- Not a product series, but compatibility mappings
- Cross-series compatibility data

**Processing Steps:**
1. Extract from `ACCESSORY_COMPATIBILITY` sheet
2. Process as reference data (not a catalog series)
3. May be integrated into ACCESSORIES workbook or kept separate
4. Generate `NSW_ACCESSORY_COMPATIBILITY_v1.xlsx` (reference sheet)

**Expected Output:**
- Compatibility mapping table
- May be included as sheet in ACCESSORIES workbook

**Special Considerations:**
- This is reference data, not a product catalog
- May be used for validation or UI display
- Keep separate or integrate with ACCESSORIES

---

## 🔄 Execution Order (Recommended)

### Phase 1: Similar to LC1E (Easy Processing)
1. **LC1D** - Similar structure to LC1E, can reuse patterns
2. **GIG** - Similar structure, straightforward
3. **CAPACITOR_DUTY** - Small dataset, straightforward

### Phase 2: Mixed Product Types (Requires Analysis)
4. **LC1K** - Mixed product types, needs analysis
5. **EOCR** - Different product type, may need adaptation
6. **PROTECT** - Overlap analysis needed

### Phase 3: Special Cases
7. **ACCESSORIES** - Different structure, compatibility mappings
8. **ACCESSORY_COMPATIBILITY** - Reference data processing

---

## 📦 Expected Outputs (Per Series)

### Standard Output Structure

Each series will produce:

1. **Primary Freeze Artifact:**
   - `NSW_{SERIES}_WEF_2025-07-15_v1.xlsx`
   - Contains all NSW format sheets:
     - `NSW_L2_PRODUCTS`
     - `NSW_PRICE_MATRIX`
     - `NSW_L1_CONFIG_LINES`
     - `NSW_VARIANT_MASTER`
     - `NSW_PRODUCT_VARIANTS`
     - `NSW_L0_TEMPLATE` (if applicable)
     - `NSW_L0_L2_ELIGIBILITY` (if applicable)

2. **Intermediate Files:**
   - `{SERIES}_CANONICAL_v1.xlsx` - Canonical extraction
   - `{SERIES}_L2_tmp.xlsx` - L2 intermediate
   - `{SERIES}_L1_tmp.xlsx` - L1 intermediate

3. **QC Documents:**
   - `QC_SUMMARY.md` - Quality control summary
   - `STEP_7_GOVERNANCE_REVIEW_PROMPT.md` - Review prompt

4. **Documentation:**
   - `ALIGNMENT_PACKAGE_SUMMARY.md` - Series-specific summary
   - Series-specific semantic lock YAML (if needed)

---

## 🛠️ Implementation Approach

### Step 1: Data Extraction Scripts

Create extraction scripts for each series:

```python
# Example: extract_lc1d_from_master.py
# Extracts LC1D rows from NSW_ITEM_MASTER_ENGINEER_VIEW
# Outputs: LC1D_CANONICAL_v1.xlsx
```

### Step 2: Reuse LC1E Pipeline

For similar series (LC1D, GIG, CAPACITOR_DUTY):
- Reuse LC1E extraction patterns
- Adapt for series-specific differences
- Follow same 8-step process

### Step 3: Adapt for Special Cases

For different product types (EOCR, ACCESSORIES):
- Analyze attribute structure
- Adapt L1 derivation rules
- May need product-type-specific logic

### Step 4: Validation

Each series must pass:
- All Phase 5 validation gates (A through I)
- Series-specific sanity checks
- Governance review

---

## 📊 Progress Tracking

| Series | Items | Status | Output File | QC Status | Governance Review |
|--------|-------|--------|-------------|------------|-------------------|
| LC1E | 165 | ✅ Complete | `NSW_LC1E_WEF_2025-07-15_v1.xlsx` | ✅ Pass | ⏳ Pending |
| LC1D | 332 | ⏳ Pending | TBD | - | - |
| LC1K | 83 | ⏳ Pending | TBD | - | - |
| GIG | 40 | ⏳ Pending | TBD | - | - |
| EOCR | 44 | ⏳ Pending | TBD | - | - |
| PROTECT | 22 | ⏳ Pending | TBD | - | - |
| CAPACITOR_DUTY | 13 | ⏳ Pending | TBD | - | - |
| ACCESSORIES | 158 | ⏳ Pending | TBD | - | - |
| ACCESSORY_COMPATIBILITY | 169 | ⏳ Pending | TBD | - | - |

**Total Items to Process:** 1,026 rows  
**Completed:** 165 (16%)  
**Remaining:** 861 (84%)

---

## 🎯 Success Criteria

### Per Series
1. ✅ All Phase 5 validation gates passed
2. ✅ NSW format workbook generated
3. ✅ QC summary created and approved
4. ✅ Governance review completed
5. ✅ Outputs archived

### Overall
1. ✅ All 8 series processed
2. ✅ All outputs follow Phase 5 standards
3. ✅ All outputs validated and approved
4. ✅ Complete catalog coverage for TESYS_PROTECT_ITEM_FULL_WORK.xlsx

---

## 📝 Next Steps

1. **Start with LC1D** (most similar to LC1E)
   - Extract LC1D data from master view
   - Create extraction script
   - Follow LC1E pipeline

2. **Create Series Template**
   - Document common patterns
   - Create reusable scripts
   - Establish series-specific variations

3. **Process Remaining Series**
   - Follow execution order
   - Adapt as needed
   - Track progress

---

**Last Updated:** 2026-01-03  
**Status:** Ready for Execution  
**Next Action:** Begin LC1D extraction and processing

