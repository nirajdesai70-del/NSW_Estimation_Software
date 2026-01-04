# <SERIES> Catalog Pipeline - QC Summary

**Archive Date**: <WEF_YYYY-MM-DD>  
**Input Pricelist**: WEF <DATE>  
**Final Deliverable**: `NSW_<SERIES>_WEF_<WEF_YYYY-MM-DD>_v<VERSION>.xlsx`

---

## Input File Information

**File Name**: `<INPUT_FILE_NAME>.xlsx`  
**Path**: `<PATH_TO_INPUT>`  
**PDF**: `<INPUT_FILE_NAME>.pdf` (available/not available)

**Sheets Detected**:
- `<SHEET_NAME>` (<description>)

---

## Row Counts

### Canonical Tables (from `<SERIES>_CANONICAL_v<VERSION>.xlsx`)

| Sheet Name | Row Count | Description |
|------------|-----------|-------------|
| `<SERIES>_CANONICAL_ROWS` | <COUNT> | Base references with AC1/AC3 ratings and HP/kW |
| `<SERIES>_COIL_CODE_PRICES` | <COUNT> | Completed SKUs (base + coil code + price) |
| `<SERIES>_ACCESSORY_SKUS` | <COUNT> | Accessory SKUs (<N> detected / not detected) |

### NSW Format Output (from `NSW_<SERIES>_WEF_<WEF_YYYY-MM-DD>_v<VERSION>.xlsx`)

| Sheet Name | Row Count | Description |
|------------|-----------|-------------|
| `NSW_L0_TEMPLATE` | <COUNT> | L0 intent templates (populated/empty) |
| `NSW_L0_L2_ELIGIBILITY` | <COUNT> | L0→L2 eligibility mappings |
| `NSW_L2_PRODUCTS` | <COUNT> | L2 product identity (stable) |
| `NSW_VARIANT_MASTER` | <COUNT> | Variant definitions (voltage, etc.) |
| `NSW_PRODUCT_VARIANTS` | <COUNT> | L2→variant allowed mappings |
| `NSW_PRICE_MATRIX` | <COUNT> | Price matrix (l2_product_code × variant_code) |
| `NSW_L1_CONFIG_LINES` | <COUNT> | L1 configuration lines (duty × voltage) |

**Note on L1 count**: L1 count should equal `NSW_PRICE_MATRIX count × number of duty classes` (if duty expansion applies). L1 count is NOT equal to L2 count - L1 expands by duty × voltage combinations.

---

## Sanity Checks

### ✅ Canonical Extraction Rules Applied

- **FRAME carry-forward applied**: <YES/NO> - <description>
- **KW range uses min**: <YES/NO> - <description>
- **Priced-only filtering**: <YES/NO> - Only SKUs with prices included in canonical tables

### ✅ L2 Generation Checks

- **No bogus base refs**: <YES/NO> - No invalid base references detected
- **L2 identity stable**: <YES/NO> - L2 contains no price, voltage, or duty
- **Series name used**: <YES/NO> - Series name (not number) used in L2
- **Frame populated**: <YES/NO> - Frame label present in all L2 rows

### ✅ L1 Generation Checks

- **Duty normalization**: <YES/NO> - duty_current_A matches duty_class
- **Voltage normalization**: <YES/NO> - selected_voltage_* matches voltage_class_code
- **Engineering attributes**: <YES/NO> - motor_kw, motor_hp, frame_label, poles present
- **Generic descriptor**: <YES/NO> - All L1 rows have generic_descriptor
- **No SKU explosion**: <YES/NO> - Voltage/duty do not create new products

### ✅ Variant System Checks

- **Variant master populated**: <YES/NO> - NSW_VARIANT_MASTER contains all variants
- **Product-variant mapping**: <YES/NO> - NSW_PRODUCT_VARIANTS correctly maps L2→variants
- **Price matrix structure**: <YES/NO> - Prices only in NSW_PRICE_MATRIX, not in L1/L2

### ⚠️ Known Issues / Notes

- **RATING_MAP**: **UNUSED** - Ratings are embedded directly in L1 (NSW_L1_CONFIG_LINES). RATING_MAP sheet is not required for NSW format.
- **Accessories**: <DETECTED/NOT_DETECTED> - <description>
- **Special cases**: <any special handling notes>

---

## Output Files

### Final Deliverable
- `NSW_<SERIES>_WEF_<WEF_YYYY-MM-DD>_v<VERSION>.xlsx` (<SIZE>KB)
  - Contains all required NSW format sheets

### Intermediate Files (Archived)
- `<SERIES>_CANONICAL_v<VERSION>.xlsx`: Canonical extraction output
- `<SERIES>_L2_tmp.xlsx`: L2 intermediate output
- `<SERIES>_L1_tmp.xlsx`: L1 intermediate output

---

## Validation Status

- ✅ Input file structure validated
- ✅ Canonical extraction completed
- ✅ L2 generation completed
- ✅ L1 generation completed
- ✅ Variant system populated
- ✅ NSW format workbook generated
- ⚠️ <Any items requiring review>

---

## Freeze Readiness

**Status**: <READY_FOR_FREEZE / NEEDS_FIXES>

**Issues to resolve before freeze**:
1. <Issue 1>
2. <Issue 2>

**Ready for ChatGPT review**: <YES/NO>

