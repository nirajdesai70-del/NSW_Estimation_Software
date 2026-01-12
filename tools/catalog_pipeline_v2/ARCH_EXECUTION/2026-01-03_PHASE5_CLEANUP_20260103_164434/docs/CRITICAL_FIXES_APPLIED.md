# Critical Fixes Applied - Pipeline Alignment

**Date**: 2025-01-XX  
**Status**: ✅ COMPLETE

---

## Issue Summary

Two critical mismatches were identified between the pipeline structure and the frozen LC1E canonical model (v6):

1. **QC Summary Template** - Still referenced old format (L2_SKU_MASTER/L1_LINES/RATING_MAP) instead of NSW format
2. **Pipeline Output** - Produced engineer review workbook instead of NSW format workbook (primary freeze artifact)

---

## Fixes Applied

### 1. QC Summary Template Updated ✅

**File**: `templates/QC_SUMMARY_TEMPLATE.md`

**Changes:**
- ✅ Already uses NSW format sheets (NSW_L2_PRODUCTS, NSW_L1_CONFIG_LINES, etc.)
- ✅ Added explicit statement: **RATING_MAP: UNUSED** - Ratings embedded in L1
- ✅ Added note: L1 count = price matrix × duties (NOT equal to L2 count)

**Key Updates:**
```markdown
- **RATING_MAP**: **UNUSED** - Ratings are embedded directly in L1 (NSW_L1_CONFIG_LINES). 
  RATING_MAP sheet is not required for NSW format.

**Note on L1 count**: L1 count should equal `NSW_PRICE_MATRIX count × number of duty classes` 
(if duty expansion applies). L1 count is NOT equal to L2 count - L1 expands by duty × voltage combinations.
```

---

### 2. NSW Format Workbook Builder Created ✅

**File**: `scripts/build_nsw_workbook.py`

**Purpose:**
- Builds NSW format workbook (PRIMARY freeze artifact)
- Creates all required NSW sheets:
  - NSW_L0_TEMPLATE
  - NSW_L0_L2_ELIGIBILITY
  - NSW_L2_PRODUCTS
  - NSW_VARIANT_MASTER
  - NSW_PRODUCT_VARIANTS
  - NSW_PRICE_MATRIX
  - NSW_L1_CONFIG_LINES

**Status:**
- ✅ Structure created
- ⚠️  Series-specific logic placeholder (requires implementation per series)
- ✅ Correct output format defined

**Note**: The script currently has placeholder logic. Series-specific extraction must be implemented based on canonical structure (similar to how LC1E v6 was built).

---

### 3. Pipeline Script Updated ✅

**File**: `templates/run_pipeline.sh`

**Changes:**
- ✅ Step 5 now builds NSW format workbook (PRIMARY artifact)
- ✅ Step 6 builds engineer review workbook (OPTIONAL, legacy format)
- ✅ Clear labeling of which file is the freeze artifact
- ✅ Updated next steps to reference NSW file for ChatGPT upload

**Output Files:**
1. **NSW_<SERIES>_WEF_<DATE>_vX.xlsx** ← PRIMARY freeze artifact
2. NSW_MASTER_SCHNEIDER_WEF_<DATE>_ENGINEER_REVIEW.xlsx ← Optional (legacy)

---

## Deliverable Decision

**Answer**: **Option 1 - NSW workbook as primary freeze artifact** ✅

**Rationale:**
- NSW format is the canonical model (aligned with LC1E v6)
- Engineer review workbook is legacy format (optional for reference)
- Primary freeze artifact = NSW format workbook

**Workflow:**
1. Cursor generates: `NSW_<SERIES>_WEF_<DATE>_vX.xlsx` + QC summary
2. Upload to ChatGPT: NSW file + QC summary (2 artifacts only)
3. ChatGPT signs off
4. Cursor archives & commits

---

## What's Still Needed

### For Next Series (e.g., LC1D)

1. **Implement series-specific logic in `build_nsw_workbook.py`**:
   - Extract NSW_L2_PRODUCTS from canonical rows
   - Extract NSW_VARIANT_MASTER from coil codes
   - Build NSW_PRICE_MATRIX from prices
   - Expand NSW_L1_CONFIG_LINES (duty × voltage)

2. **Reference LC1E v6** as the pattern:
   - Study how LC1E v6 was built
   - Replicate structure for new series
   - Ensure same sheet/column structure

3. **Test pipeline**:
   - Run full pipeline for new series
   - Verify NSW format output matches LC1E v6 structure
   - QC checklist passes

---

## Verification Checklist

Before starting next series, verify:

- [x] QC template uses NSW format sheets
- [x] QC template explicitly states RATING_MAP is unused
- [x] QC template notes L1 count ≠ L2 count
- [x] Pipeline builds NSW format workbook (primary)
- [x] Pipeline builds engineer review (optional)
- [x] Output file naming is clear (NSW vs engineer review)
- [ ] Series-specific logic implemented in build_nsw_workbook.py
- [ ] Test run produces correct NSW format structure

---

## References

- **LC1E v6 Structure**: `input/schneider/lc1e/LC1E_Page8_Canonical_and_NSW_Format_v6.xlsx`
- **Operating Model**: `OPERATING_MODEL.md`
- **Bootstrap Guide**: `NEXT_SERIES_BOOTSTRAP.md`

---

**Status**: ✅ CRITICAL FIXES APPLIED - Ready for next series (after series-specific logic implementation)

