# Validation Without V6 Reference - Complete Guide

**Date**: 2025-01-XX  
**Status**: ✅ COMPLETE

---

## Answer to Your Question

**Q**: Can we use PDF and XLSX input files for cross-verification? If v6 file is not available, how can we rectify based on these two input files?

**A**: ✅ **YES** - Self-validation using source files is now implemented.

---

## Self-Validation System

### ✅ Validation Script

**File**: `scripts/validate_canonical_against_source.py`

**Inputs**:
- Source XLSX file (required)
- Source PDF file (optional, for future)
- Canonical output file (to validate)

**Output**: Validation report with issues and warnings

---

## What Gets Validated

### 1. Base Reference Coverage

**Checks**:
- Are all base refs from source captured in canonical?
- Are there extra base refs in canonical not in source?

**Example Output**:
```
⚠️  Base refs in source but not in canonical (41): [...]
⚠️  Base refs in canonical but not in source (0): []
```

**Action**: Review missing refs - some may be invalid (LC1E0600), others may need extraction.

---

### 2. Frame Label Accuracy

**Checks**:
- Do frame labels match source XLSX FRAME- rows?
- Are expected frames present (e.g., FRAME-4)?

**Method**:
- Extracts FRAME- rows from source XLSX
- Maps base refs to their nearest FRAME- label
- Compares with canonical frame labels

**Example Issues**:
```
❌ CRITICAL: FRAME-4 not found in canonical
⚠️  Frame mismatch for LC1E80: canonical=FRAME-3, source=FRAME-4
⚠️  FRAME-9 assigned to 14 rows (60.9%). May be section header, not frame.
```

**Action**: Fix frame carry-forward logic based on source assignments.

---

### 3. Coil Code Coverage

**Checks**:
- Are all coil codes from source captured?
- Are coil codes in correct sections?

**Example**:
```
Source coil codes: ['B7', 'BD', 'F7', 'M5', 'M5WB', 'M7', 'N5', 'N5WB', 'N7']
Canonical coil codes: ['BD', 'M7', 'N5']
Missing: ['B7', 'F7', 'M5', 'M5WB', 'N5WB', 'N7']
```

**Action**: Check if missing codes are in different sections (4P, DC) that weren't extracted.

---

### 4. Section Validation

**Checks**:
- Are DC coils in AC section? (should not be)
- Are sections correctly separated?

**Example Issues**:
```
❌ CRITICAL: DC coil codes (BD) found in 3P AC canonical table
❌ CRITICAL: Source has 3P DC section, but canonical doesn't have LC1E_3P_DC table
```

**Action**: Fix section detection - DC should be separate from AC.

---

## Current Issues Detected (LC1E)

### ❌ Critical Issues

1. **FRAME-4 Missing**
   - User reported: "Many FRAME-4 items are missing"
   - Validation confirms: FRAME-4 not found or very low count
   - **Fix**: Improve frame carry-forward to capture FRAME-4 base refs

2. **DC Coil in AC Section**
   - User reported: "No DC coil for first table but it is included"
   - Validation detects: BD (DC coil) may be in 3P AC table
   - **Fix**: Ensure DC section is separate, BD only in 3P DC

3. **FRAME-9 Overuse**
   - 14/23 rows assigned FRAME-9 (60.9%)
   - Likely a section header, not actual frame
   - **Fix**: Improve frame tracking to use actual FRAME- rows, not section headers

### ⚠️ Warnings

1. **Missing Coil Codes**: B7, F7, M5, M5WB, N5WB, N7
   - Likely in 4P AC or other sections not extracted
   - **Action**: Verify all sections are extracted

2. **Frame Mismatches**: Many base refs show different frames in source vs canonical
   - **Action**: Use source frame assignments as primary truth

---

## How to Use (No V6 Required)

### Step 1: Run Pipeline

```bash
cd active/schneider/LC1E/
./run_pipeline.sh
```

**Pipeline now includes validation step automatically.**

### Step 2: Review Validation Report

```bash
cat 02_outputs/VALIDATION_REPORT.txt
```

**Look for**:
- ❌ Critical issues (must fix)
- ⚠️ Warnings (review and fix if needed)

### Step 3: Fix Based on Validation

**Example fixes**:
1. **FRAME-4 missing** → Improve frame carry-forward logic
2. **DC in AC section** → Fix section detection
3. **Missing coil codes** → Extract additional sections (4P, DC)

### Step 4: Re-run and Re-validate

```bash
# Fix extractor
# Re-run pipeline
./run_pipeline.sh

# Or validate manually
python3 ../../scripts/validate_canonical_against_source.py \
  --canonical 02_outputs/LC1E_CANONICAL_v1.xlsx \
  --xlsx 00_inputs/input.xlsx \
  --out 02_outputs/VALIDATION_v2.txt
```

### Step 5: Freeze When Ready

**Criteria**:
- ✅ No critical issues
- ✅ Warnings are explainable/acceptable
- ✅ Frame labels match source
- ✅ Sections correctly separated
- ✅ All expected frames present

---

## Validation Report Format

```
============================================================
VALIDATION RESULTS
============================================================

❌ ISSUES FOUND:
  - CRITICAL: FRAME-4 not found in canonical
  - CRITICAL: DC coil codes (BD) found in 3P AC section

⚠️  WARNINGS:
  - Base refs in source but not in canonical (41): [...]
  - Frame mismatch for LC1E80: canonical=FRAME-3, source=FRAME-4
  - Coil codes in source but not in canonical: ['B7', 'F7', ...]
  - FRAME-9 assigned to 14 rows (60.9%). May be section header.

============================================================
SUMMARY
============================================================
Canonical base refs: 23
Source base refs: 64
Match: 23 common
Canonical coil codes: ['BD', 'M7', 'N5']
Source coil codes: ['B7', 'BD', 'F7', 'M5', 'M5WB', 'M7', 'N5', 'N5WB', 'N7']
Frame labels in canonical: 4 unique frames
```

---

## Benefits

✅ **No V6 Required**: Validates against actual source documents  
✅ **Self-Contained**: Uses input files you already have  
✅ **Detects Real Issues**: Finds missing frames, wrong sections, etc.  
✅ **Actionable**: Provides specific issues to fix  
✅ **Automated**: Runs as part of pipeline

---

## Next Steps to Fix Current Issues

### 1. Fix FRAME-4 Extraction

**Problem**: FRAME-4 items missing  
**Solution**: Improve frame carry-forward to better track FRAME-4 base refs from source

### 2. Fix DC Section Separation

**Problem**: DC coil in AC section  
**Solution**: Ensure 3P DC section is properly detected and separated

### 3. Fix FRAME-9 Overuse

**Problem**: FRAME-9 used as section header, not frame  
**Solution**: Better distinguish between section headers and actual FRAME- labels

---

## Files Created

1. ✅ `scripts/validate_canonical_against_source.py` - Validation script
2. ✅ `SELF_VALIDATION_GUIDE.md` - Detailed guide
3. ✅ `VALIDATION_WITHOUT_V6.md` - This file

---

**Status**: ✅ **SELF-VALIDATION ENABLED** - Can verify and fix without v6 reference file

