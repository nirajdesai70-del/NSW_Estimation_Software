# LC1E Series - Execution Status

## Current Status

✅ **Option B Patches Complete**: All 4 patches have been applied to the unified generic pipeline
- Patch 1: LC1E coil codes added (N5, M5WB, N5WB, M5)
- Patch 2: Duty expansion per Base_Ref (CRITICAL bug fix)
- Patch 3: Accessory tagging via IsAccessory flag (canonical-driven)
- Patch 4: Voltage de-dup + range code SC_L2_Operation handling

⚠️ **Step 0 BLOCKER**: LC1E canonical table extraction script needs customization based on actual pricelist structure

---

## File Locations

### Input Files (Expected)
- Raw pricelist XLSX: `input/schneider/lc1e/Switching_All_WEF_15th_Jul_25.xlsx`
- Raw pricelist PDF: `input/schneider/lc1e/Switching_All_WEF_15th_Jul_25.pdf` (optional, for cross-check)

### Output Files (Generated)
- Canonical: `output/lc1e/LC1E_CANONICAL_v1.xlsx`
- L2 temporary: `output/lc1e/LC1E_L2_tmp.xlsx`
- L1 temporary: `output/lc1e/LC1E_L1_tmp.xlsx`
- Engineer Review: `output/lc1e/LC1E_ENGINEER_REVIEW_v1.xlsx`

---

## Execution Commands

All commands should be run from: `/Users/nirajdesai/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2`

### Step 1: Inspect Raw Pricelist

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2

python3 scripts/inspect_lc1e_raw.py \
  --input_xlsx "input/schneider/lc1e/Switching_All_WEF_15th_Jul_25.xlsx"
```

**Expected Output**: Sheet names, LC1E match locations, surrounding rows

---

### Step 2: Extract LC1E Canonical Tables (Step 0 - BLOCKER)

**⚠️ IMPORTANT**: This script currently outputs empty canonical structure. It MUST be customized based on actual pricelist structure before it will extract real data.

```bash
python3 scripts/lc1e_extract_canonical.py \
  --input_xlsx "input/schneider/lc1e/Switching_All_WEF_15th_Jul_25.xlsx" \
  --out "output/lc1e/LC1E_CANONICAL_v1.xlsx"
```

**Expected Output**: 
- 3 sheets: `LC1E_CANONICAL_ROWS`, `LC1E_COIL_CODE_PRICES`, `LC1E_ACCESSORY_SKUS`
- Row counts (should be > 0 after customization):
  - Base refs extracted
  - Coil price rows created (priced-only)
  - Accessory SKUs extracted

**Coil Tokens Supported**:
- 3P AC: M7(220), N5(415)
- 3P DC: BD(24V DC)
- 4P AC: B7(24), F7(110), M5WB(220), N5WB(415)
- Higher frame: M5(220), N7(415) - treat M5 as coil token if present

---

### Step 3: Build L2 (Script A)

```bash
python3 scripts/build_l2_from_canonical.py \
  --input "output/lc1e/LC1E_CANONICAL_v1.xlsx" \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out "output/lc1e/LC1E_L2_tmp.xlsx"
```

**Expected Output**:
- 3 sheets: `L2_SKU_MASTER`, `L2_PRICE_HISTORY`, `RATING_MAP`
- L2_SKU_MASTER rows = completed SKUs with prices
- RATING_MAP rows > 0 (AC1/AC3 ratings per base ref)
- IsAccessory column in L2_SKU_MASTER

---

### Step 4: Derive L1 (Script B)

```bash
python3 scripts/derive_l1_from_l2.py \
  --l2 "output/lc1e/LC1E_L2_tmp.xlsx" \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out "output/lc1e/LC1E_L1_tmp.xlsx"
```

**Expected Output**:
- 2 sheets: `L1_LINES`, `L1_ATTRIBUTES_KVU`
- L1_LINES BASE count > L2 count (duty × voltage combinations)
- L1_LINES FEATURE count > 0 (accessories from IsAccessory=True)
- Duty expansion per Base_Ref (not global)
- SC_L2_Operation = "{AC/DC} Coil Range" for range codes

---

### Step 5: Build Engineer Review Workbook (Script C)

```bash
python3 scripts/build_master_workbook.py \
  --l2 "output/lc1e/LC1E_L2_tmp.xlsx" \
  --l1 "output/lc1e/LC1E_L1_tmp.xlsx" \
  --out "output/lc1e/LC1E_ENGINEER_REVIEW_v1.xlsx"
```

**Expected Output**:
- 5 sheets: `L2_SKU_MASTER`, `L2_PRICE_HISTORY`, `L1_LINES`, `L1_ATTRIBUTES_KVU`, `RATING_MAP`

---

## Validation Checklist

After running the full pipeline, verify:

- [ ] L2_SKU_MASTER: All SKUs are completed (no * or #)
- [ ] L2_SKU_MASTER: IsAccessory column present and correctly flagged
- [ ] RATING_MAP: Not empty, contains AC1/AC3 rows per base ref
- [ ] L1_LINES BASE: Count > L2 count (duty × voltage combinations)
- [ ] L1_LINES BASE: SC_L2_Operation correct (Coil vs Coil Range)
- [ ] L1_LINES FEATURE: Count > 0 if accessories exist
- [ ] L1_LINES FEATURE: Item_ProductType = "Contactor" (locked)
- [ ] L1_LINES FEATURE: Business_SubCategory = "Power Contactor" (locked)
- [ ] L1_LINES FEATURE: Do NOT multiply across duty/voltage
- [ ] L1_ATTRIBUTES_KVU: KVU values populated from RATING_MAP

---

## Notes

- **Coil Code M5**: Treated as 220V AC coil token. Verify in raw XLSX if it appears.
- **Accessory Tagging**: Uses IsAccessory flag from canonical source (SC_L4_AccessoryClass / AccessoryClass / is_accessory / SC_L4)
- **Duty Expansion**: Per Base_Ref from RATING_MAP (not global). Fallback marked with "DUTY_FALLBACK_REVIEW" in Notes.
- **Range Codes**: SC_L2_Operation = "{AC/DC} Coil Range" when voltage is None.

---

## Next Steps

1. Customize `lc1e_extract_canonical.py` based on actual pricelist structure (pages 8-10)
2. Run Step 2 to generate canonical tables
3. Validate canonical output row counts
4. Run Steps 3-5 to generate engineer review workbook
5. Engineer validation against raw pricelist pages 8-10
