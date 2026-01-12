# Self-Validation Guide - No V6 Reference Required

**Date**: 2025-01-XX  
**Status**: ✅ COMPLETE

---

## Problem Statement

**Question**: How can we verify canonical extraction is correct when v6 reference file is not available?

**Answer**: Use **self-validation** against source files (XLSX + PDF).

---

## Self-Validation Approach

### ✅ Validation Script Created

**File**: `scripts/validate_canonical_against_source.py`

**Purpose**: Cross-validates canonical extraction against input XLSX/PDF without requiring v6 reference.

**What It Checks**:
1. **Base refs**: Are all base refs from source captured in canonical?
2. **Frame labels**: Do frame labels match source XLSX FRAME- rows?
3. **Coil codes**: Are all coil codes from source captured?
4. **Section mapping**: Are coil codes in correct sections (e.g., no DC in AC section)?
5. **Missing frames**: Are expected frames present (e.g., FRAME-4)?

---

## How It Works

### Input Files Used

1. **Source XLSX**: `00_inputs/Switching_All_WEF_15th_Jul_25.xlsx`
   - Extracts base refs, frame labels, coil codes
   - Analyzes section structure

2. **Source PDF**: `00_inputs/Switching_All_WEF_15th_Jul_25.pdf` (optional, for future PDF parsing)

3. **Canonical Output**: `02_outputs/<SERIES>_CANONICAL_vX.xlsx`
   - What was extracted by the canonical extractor

### Validation Process

```bash
python3 scripts/validate_canonical_against_source.py \
  --canonical <CANONICAL_FILE> \
  --xlsx <SOURCE_XLSX> \
  --pdf <SOURCE_PDF> \
  --out <VALIDATION_REPORT>
```

**Output**: Validation report with:
- ✅ Issues (critical problems)
- ⚠️ Warnings (potential problems)
- Summary statistics

---

## What Gets Validated

### 1. Base Reference Coverage

**Check**: Are all base refs from source captured?

**Example**:
```
Source base refs: 64
Canonical base refs: 23
Missing in canonical: 41 (may include invalid/bogus refs)
```

**Action**: Review missing refs - some may be invalid (e.g., LC1E0600), others may be missing.

---

### 2. Frame Label Accuracy

**Check**: Do frame labels match source XLSX FRAME- rows?

**Method**:
- Extract FRAME- rows from source XLSX
- Map base refs to their nearest FRAME- label
- Compare with canonical frame labels

**Example Issue**:
```
Frame mismatch for LC1E80: canonical=FRAME-3, source=FRAME-4
```

**Action**: Fix frame inference or improve frame carry-forward logic.

---

### 3. Coil Code Coverage

**Check**: Are all coil codes from source captured?

**Example**:
```
Source coil codes: ['B7', 'BD', 'F7', 'M5', 'M5WB', 'M7', 'N5', 'N5WB', 'N7']
Canonical coil codes: ['BD', 'M7', 'N5']
Missing: ['B7', 'F7', 'M5', 'M5WB', 'N5WB', 'N7']
```

**Action**: Check if missing coil codes are in different sections (4P, DC, etc.) that weren't extracted.

---

### 4. Section-Specific Validation

**Check**: Are coil codes in correct sections?

**Example Issues**:
- ❌ DC coil (BD) found in 3P AC section → **ISSUE**
- ✅ M7, N5 in 3P AC section → **CORRECT**

**Action**: Fix section detection logic if wrong.

---

### 5. Missing Frame Detection

**Check**: Are expected frames present?

**Example**:
```
⚠️ FRAME-4 not found in canonical (may be missing from extraction)
```

**User Observation**: "Many FRAME-4 items are missing"

**Action**: Check if FRAME-4 base refs (LC1E80, LC1E95) are being extracted.

---

## Integration into Pipeline

### Updated Pipeline Script

**File**: `templates/run_pipeline.sh`

**New Step 5**: Validation against source files
```bash
python3 scripts/validate_canonical_against_source.py \
  --canonical <CANONICAL_OUTPUT> \
  --xlsx <INPUT_XLSX> \
  --out <VALIDATION_REPORT>
```

**Result**: Validation report generated automatically during pipeline execution.

---

## Validation Report Format

```
============================================================
VALIDATION RESULTS
============================================================

❌ ISSUES FOUND:
  - DC coil codes found in 3P AC section: {'BD'}

⚠️  WARNINGS:
  - Base refs in source but not in canonical (41): [...]
  - Frame mismatch for LC1E80: canonical=FRAME-3, source=FRAME-4
  - Coil codes in source but not in canonical: ['B7', 'F7', ...]
  - FRAME-4 not found in canonical

============================================================
SUMMARY
============================================================
Canonical base refs: 23
Source base refs: 64
Match: 23 common
...
```

---

## How to Use Without V6

### Scenario: New Series, No Reference File

1. **Run Pipeline**:
   ```bash
   ./run_pipeline.sh
   ```

2. **Check Validation Report**:
   ```bash
   cat 02_outputs/VALIDATION_REPORT.txt
   ```

3. **Review Issues/Warnings**:
   - Fix critical issues (e.g., DC in AC section)
   - Review warnings (e.g., frame mismatches)
   - Check missing base refs (may be intentional)

4. **Iterate**:
   - Fix extractor based on validation findings
   - Re-run pipeline
   - Re-validate

5. **Freeze When**:
   - ✅ No critical issues
   - ✅ Warnings are explainable/acceptable
   - ✅ Frame labels match source
   - ✅ Coil codes correctly mapped

---

## Current Validation Results (LC1E)

### Issues Found
- ✅ No critical issues (DC not in wrong section)

### Warnings Found
- ⚠️ Frame mismatches (many base refs show FRAME-9 in source, but canonical has different frames)
- ⚠️ Missing coil codes (B7, F7, M5, M5WB, N5WB, N7 - likely in 4P or DC sections not extracted)
- ⚠️ FRAME-4 missing (LC1E80, LC1E95 should be FRAME-4, not FRAME-3)

### Root Causes

1. **Frame Inference Issue**: 
   - Source shows many base refs under FRAME-9 (likely a section header)
   - Our inference logic assigns different frames
   - **Fix**: Improve frame carry-forward to better track from source

2. **Missing Sections**:
   - 4P AC section may not be extracted (has M5WB, N5WB)
   - DC section may be incomplete (has BD, but may have more)
   - **Fix**: Ensure all sections are extracted

3. **FRAME-4 Missing**:
   - LC1E80, LC1E95 should be FRAME-4 (user observation)
   - Currently inferred as FRAME-3
   - **Fix**: Update inference logic

---

## Next Steps to Fix Issues

### 1. Fix Frame Inference

**Update**: `infer_frame_from_base_ref()` function
- LC1E80, LC1E95 → FRAME-4 (not FRAME-3)
- Better handle FRAME-9 section (may be a grouping, not actual frame)

### 2. Improve Frame Carry-Forward

**Enhance**: Frame tracking in extractor
- Better track FRAME- rows from source
- Carry forward more reliably
- Use source frame labels as primary, inference as fallback

### 3. Extract All Sections

**Verify**: All sections extracted
- 3P AC ✅
- 3P DC ⚠️ (may be incomplete)
- 4P AC ⚠️ (may be missing)

---

## Benefits of Self-Validation

✅ **No V6 Required**: Can validate without reference file  
✅ **Source of Truth**: Uses actual source documents  
✅ **Detects Issues**: Finds missing frames, wrong sections, etc.  
✅ **Iterative Improvement**: Can fix and re-validate  
✅ **Automated**: Runs as part of pipeline

---

## Usage Example

```bash
# Run full pipeline (includes validation)
cd active/schneider/LC1E/
./run_pipeline.sh

# Check validation report
cat 02_outputs/VALIDATION_REPORT.txt

# If issues found, fix extractor and re-run
# Re-validate
python3 ../../scripts/validate_canonical_against_source.py \
  --canonical 02_outputs/LC1E_CANONICAL_v1.xlsx \
  --xlsx 00_inputs/input.xlsx \
  --out 02_outputs/VALIDATION_REPORT_v2.txt
```

---

**Status**: ✅ **SELF-VALIDATION ENABLED** - Can verify without v6 reference file

