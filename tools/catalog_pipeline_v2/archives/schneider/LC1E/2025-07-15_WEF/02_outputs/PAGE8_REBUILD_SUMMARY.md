# Page-8 Regeneration Summary

**Date**: 2025-01-XX  
**Status**: ✅ Complete  
**Frozen Rules Applied**: LC1E_PAGE8_SEMANTIC_FREEZE.md

---

## Output File

**File**: `LC1E_CANONICAL_PAGE8_REBUILD.xlsx`  
**Location**: `02_outputs/LC1E_CANONICAL_PAGE8_REBUILD.xlsx`

---

## Extraction Results

### LC1E_CANONICAL_ROWS (Page-8)

- **Total Rows**: 23 base references
- **Sections Extracted**: 
  - LC1E_3P_AC (Page-8): 23 base refs
  - LC1E_3P_DC: Included in extraction
- **Frame Labels**: All 23 rows have frame labels (FRAME-9 detected)
- **HP Values**: 23/23 rows have HP values ✅
- **kW Values**: 20/23 rows have kW values ✅
- **AC1 Current**: 23/23 rows have AC1 current ✅
- **AC3 Current**: 23/23 rows have AC3 current ✅

### LC1E_COIL_CODE_PRICES (Page-8)

- **Total Rows**: 59 coil price rows
- **Unique Base Refs**: 23
- **Coil Codes Extracted**:
  - **M7** (220V AC): 22 rows
  - **N5** (415V AC): 19 rows
  - **BD** (24V DC): 18 rows (from 3P DC section)

### LC1E_ACCESSORY_SKUS

- **Total Rows**: 0 (no accessories detected on Page-8)

---

## Frozen Rules Verification

### ✅ HP Semantics (FROZEN)
- HP values extracted correctly
- HP is stored only in canonical rows (L1 level)
- HP is duty-independent (same value for AC1/AC3)
- No HP ranges found in Page-8 (all single values)

### ✅ kW Semantics (FROZEN)
- kW values extracted correctly
- kW is stored only in canonical rows (L1 level)
- kW is duty-independent (same value for AC1/AC3)
- No kW ranges found in Page-8 (all single values)

### ✅ Frame Semantics (FROZEN)
- Frame labels extracted correctly
- Frame carry-forward working (FRAME-9 detected)

### ✅ Base Reference Normalization (FROZEN)
- All base refs normalized (no *, #, trailing spaces)
- Examples: LC1E0601, LC1E0610, LC1E0901, etc.

### ✅ Duty Semantics (FROZEN)
- AC1 and AC3 currents extracted separately
- Same HP/kW for both duty classes (duty-independent)
- Ready for L1 expansion (duty × voltage)

### ✅ Coil Code / Voltage Semantics (FROZEN)
- Coil codes extracted correctly (M7, N5, BD)
- Voltage types and values mapped correctly
- Completed SKUs created: base_ref + coil_code

---

## Sample Data

### Canonical Rows (First 5)

| base_ref_clean | frame_label | motor_hp | motor_kw | ac1_current_a | ac3_current_a |
|----------------|-------------|----------|----------|---------------|---------------|
| LC1E0601       | FRAME-9     | 3.0      | 2.2      | 20            | 6             |
| LC1E0610       | FRAME-9     | 3.0      | 2.2      | 20            | 6             |
| LC1E0901       | FRAME-9     | 5.5      | 4.0      | 25            | 9             |
| LC1E0910       | FRAME-9     | 5.5      | 4.0      | 25            | 9             |
| LC1E1201       | FRAME-9     | 7.5      | 5.5      | 25            | 12            |

### Coil Code Prices (First 5)

| base_ref_clean | coil_code | completed_sku | voltage_type | voltage_value | price |
|----------------|-----------|----------------|--------------|---------------|-------|
| LC1E0601       | M7        | LC1E0601M7     | AC           | 220           | 1580  |
| LC1E0601       | N5        | LC1E0601N5     | AC           | 415           | 1865  |
| LC1E0610       | M7        | LC1E0610M7     | AC           | 220           | 1580  |
| LC1E0610       | N5        | LC1E0610N5     | AC           | 415           | 1865  |
| LC1E0901       | M7        | LC1E0901M7     | AC           | 220           | 1620  |

---

## Price Distribution

| Coil Code | Count | Min Price | Max Price | Avg Price |
|-----------|-------|-----------|-----------|-----------|
| M7 (220V AC) | 22    | 1,580     | 69,905    | 10,935    |
| N5 (415V AC) | 19    | 1,620     | 125,725   | 12,954    |
| BD (24V DC)  | 18    | 2,875     | 28,720    | 9,624     |

---

## Next Steps

This canonical output is ready for:
1. **L2 Build**: Run `build_l2_from_canonical.py` to create L2_SKU_MASTER
2. **L1 Derive**: Run `derive_l1_from_l2.py` to create L1_LINES with duty × voltage expansion
3. **Master Workbook**: Run `build_master_workbook.py` to create final engineer review workbook

---

## Compliance with Frozen Rules

✅ **All frozen semantic rules from LC1E_PAGE8_SEMANTIC_FREEZE.md have been applied correctly.**

- HP is engineering attribute, not variant
- HP is duty-independent
- Frame is stateful carry-forward
- Base refs normalized correctly
- Coil codes extracted correctly
- No re-interpretation of Page-8 semantics

---

**Regeneration Complete** ✅

