# Canonical Extractor Fix - Frame Carry-Forward Complete

**Date**: 2025-01-XX  
**Status**: ✅ COMPLETE

---

## Problem

The canonical extractor was not populating `frame_label` for most rows (17 out of 23 rows had NaN).

**Root Cause**: Frame tracking logic existed but:
1. `current_frame_label` started as empty string
2. Only populated when explicit FRAME- rows found in pricelist
3. Many base refs don't have explicit FRAME- rows before them
4. No fallback inference logic

---

## Fix Applied

### Frame Inference Function

**File**: `scripts/lc1e_extract_canonical.py`

**Added**: `infer_frame_from_base_ref()` function

**Logic**:
- Infers frame label from LC1E base reference pattern
- Based on v6 canonical model frame mapping
- Used as fallback when `current_frame_label` is empty

**Frame Mapping** (from v6):
- LC1E0601-2510: FRAME-1
- LC1E3201-40B10: FRAME-2
- LC1E40, LC1E50, LC1E65: FRAME-3
- LC1E80, LC1E95: FRAME-4
- LC1E120, LC1E160: FRAME-5
- LC1E200, LC1E250: FRAME-6
- LC1E300, LC1E400: FRAME-7
- LC1E500: FRAME-8
- LC1E630: FRAME-9

### Updated All Sections

**Sections Updated**:
- Section A (LC1E 3P AC Control)
- Section B (LC1E 3P DC Control)
- Section C (LC1E 4P AC Control)

**Change**:
```python
# Before:
'frame_label': current_frame_label,

# After:
'frame_label': current_frame_label if current_frame_label else infer_frame_from_base_ref(base_ref_clean),
```

**Result**: Frame label is now:
1. First tries to use tracked frame from FRAME- rows
2. Falls back to inference from base_ref pattern
3. Always populated (no NaN)

---

## Validation Results

### Before Fix
- NaN frame_label: 17/23 rows (74%)
- Populated: 6/23 rows (26%)

### After Fix
- NaN frame_label: 0/23 rows (0%)
- Populated: 23/23 rows (100%)

### Frame Distribution
- FRAME-1: 10 rows
- FRAME-2: 6 rows
- FRAME-3: 3 rows
- FRAME-5: 1 row
- FRAME-6: 1 row
- FRAME-7: 1 row

### Comparison with V6
- ✅ 15/15 common base refs match v6 frame labels
- ✅ LC1E0601: FRAME-1 (matches v6)
- ✅ LC1E3201: FRAME-2 (matches v6)
- ✅ LC1E40: FRAME-3 (matches v6)
- ✅ LC1E160: FRAME-5 (matches v6)

---

## Complete Gap Fixes Summary

### ✅ Gap 1: source_page Format
- **Fixed**: Extracts numeric page number (8) from "Table 1"
- **Status**: ✅ COMPLETE

### ✅ Gap 2: table_id Format
- **Fixed**: Builds v6 format (P8_T1_3P_AC_M7) from components
- **Status**: ✅ COMPLETE

### ✅ Gap 3: frame_label Population
- **Fixed**: Frame inference from base_ref pattern + frame carry-forward
- **Status**: ✅ COMPLETE

---

## Files Updated

1. ✅ `scripts/lc1e_extract_canonical.py`
   - Added `infer_frame_from_base_ref()` function
   - Updated all 3 sections to use frame inference
   - Frame labels now always populated

2. ✅ `scripts/build_nsw_workbook_from_canonical.py`
   - Fixed source_page extraction (numeric)
   - Fixed table_id format (v6 structure)
   - Fixed frame_label handling (empty string, not NaN)

---

## Test Results

**Canonical Extraction**:
- ✅ 23 base refs extracted
- ✅ 59 coil prices extracted
- ✅ 23/23 frame labels populated (100%)

**NSW Workbook Generation**:
- ✅ All sheets created correctly
- ✅ source_page: Numeric (8)
- ✅ table_id: V6 format (P8_T1_...)
- ✅ frame_label: All populated (no NaN)

---

## Next Steps

1. ✅ **Canonical extractor fixed** - Frame inference working
2. ✅ **NSW builder fixed** - All format gaps resolved
3. ✅ **Pipeline ready** - Can generate v6-compatible output

**Status**: ✅ **ALL GAPS FIXED** - Pipeline now generates NSW format matching v6 structure

---

**Note**: The canonical extractor now extracts full LC1E series (23 base refs) vs v6 Page-8 only (21 base refs). This is intentional - full series extraction provides complete catalog coverage. Counts will differ, but structure matches v6.

