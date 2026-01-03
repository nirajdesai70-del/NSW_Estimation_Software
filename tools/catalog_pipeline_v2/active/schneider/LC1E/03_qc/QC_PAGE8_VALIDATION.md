# Validation Report

**Status**: ❌ **FAIL**

**Date**: 2025-12-30 00:16:03

**Golden**: `archives/schneider/LC1E/2025-07-15_WEF/00_inputs/LC1E_Page8_Canonical_and_NSW_Format_v6.xlsx`
**Rebuilt**: `active/schneider/LC1E/02_outputs/LC1E_PAGE8_v6_rebuilt.xlsx`

## Results

| Sheet | Golden Rows | Rebuilt Rows | Rowcount Match | Signature Match | Status |
|-------|-------------|--------------|----------------|-----------------|--------|
| P8_T1_CANONICAL_ROWS | 21 | 23 | ❌ | ❌ | ❌ FAIL |
| P8_T1_COIL_PRICES | 40 | 41 | ❌ | ❌ | ❌ FAIL |
| P8_T3_CANONICAL_ROWS | 8 | 3 | ❌ | ❌ | ❌ FAIL |
| P8_T3_COIL_PRICES | 15 | 6 | ❌ | ❌ | ❌ FAIL |

## Errors

- [P8_T1_CANONICAL_ROWS] rowcount differs: golden=21 rebuilt=23
- [P8_T1_CANONICAL_ROWS] content differs (key-col signature mismatch)
- [P8_T1_COIL_PRICES] rowcount differs: golden=40 rebuilt=41
- [P8_T1_COIL_PRICES] content differs (key-col signature mismatch)
- [P8_T3_CANONICAL_ROWS] rowcount differs: golden=8 rebuilt=3
- [P8_T3_CANONICAL_ROWS] content differs (key-col signature mismatch)
- [P8_T3_COIL_PRICES] rowcount differs: golden=15 rebuilt=6
- [P8_T3_COIL_PRICES] content differs (key-col signature mismatch)
