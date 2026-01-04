# Source File Reference

**Date:** 2026-01-03  
**Status:** ✅ ACTIVE

---

## Primary Source File (Normalized)

**File Name:** `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`  
**Location:** `tools/catalog_pipeline_v2/input/reviseditemmaster/`  
**Status:** ✅ Clean and aligned version (normalized structure)

**Characteristics:**
- Same data as `TESYS_PROTECT_ITEM_FULL_WORK.xlsx`
- Normalized/cleaned structure
- All 8 sheets present and working
- 1,026 total rows across all sheets

**Use This File For:**
- All series extraction (LC1D, LC1K, GIG, EOCR, etc.)
- All processing pipelines
- All catalog generation

---

## Reference File (Original)

**File Name:** `TESYS_PROTECT_ITEM_FULL_WORK.xlsx`  
**Location:** `active/schneider/LC1E/00_inputs/`  
**Status:** Reference only (use normalized version instead)

**Note:** This file is kept for reference but should NOT be used for processing. Use the normalized version instead.

---

## File Structure (Both Files)

Both files contain the same 8 sheets:

1. `NSW_ITEM_MASTER_ENGINEER_VIEW` - 497 rows (LC1D: 332, LC1E: 165)
2. `ITEM_TESYS_EOCR_WORK` - 44 rows
3. `ITEM_TESYS_PROTECT_WORK` - 22 rows
4. `ITEM_GIGA_SERIES_WORK` - 40 rows
5. `ITEM_K_SERIES_WORK` - 83 rows
6. `ITEM_CAPACITOR_DUTY_WORK` - 13 rows
7. `ACCESSORY_COMPATIBILITY` - 169 rows
8. `ACCESSORIES_MASTER` - 158 rows

**Total:** 1,026 rows

---

## Usage in Scripts

### Correct Usage:
```python
# ✅ Use normalized file
input_file = "tools/catalog_pipeline_v2/input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx"
df = pd.read_excel(input_file, sheet_name="NSW_ITEM_MASTER_ENGINEER_VIEW")
```

### Incorrect Usage:
```python
# ❌ Don't use original file
input_file = "active/schneider/LC1E/00_inputs/TESYS_PROTECT_ITEM_FULL_WORK.xlsx"  # WRONG
```

---

## Series Extraction Examples

### LC1D:
```python
df = pd.read_excel("tools/catalog_pipeline_v2/input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx",
                   sheet_name="NSW_ITEM_MASTER_ENGINEER_VIEW")
lc1d = df[df['series_code'] == 'LC1D']
```

### LC1K:
```python
df = pd.read_excel("tools/catalog_pipeline_v2/input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx",
                   sheet_name="ITEM_K_SERIES_WORK")
```

### GIG:
```python
df = pd.read_excel("tools/catalog_pipeline_v2/input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx",
                   sheet_name="ITEM_GIGA_SERIES_WORK")
```

---

**Last Updated:** 2026-01-03  
**Status:** ✅ Active Reference


