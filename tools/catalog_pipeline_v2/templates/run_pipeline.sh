#!/usr/bin/env bash
# Standard Catalog Pipeline Execution Script
# Usage: ./run_pipeline.sh
# 
# This script runs the complete catalog conversion pipeline for a series.
# Customize SERIES, WEF, and INPUT_FILE_NAME before running.

set -euo pipefail

# ============================================================================
# CONFIGURATION - Customize these for each series
# ============================================================================

SERIES="<SERIES>"                    # e.g., LC1D, LC1F, MCCB, ACB
WEF="<WEF_YYYY-MM-DD>"               # e.g., 2025-07-15
INPUT_FILE_NAME="<INPUT_FILE_NAME>"  # e.g., Switching_All_WEF_15th_Jul_25.xlsx
VERSION="1"                          # Output version number

# ============================================================================
# PATHS - Usually no changes needed
# ============================================================================

ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$(cd "$ROOT/../../scripts" && pwd)"
INPUT_DIR="$ROOT/00_inputs"
OUTPUT_DIR="$ROOT/02_outputs"
WORKING_DIR="$ROOT/01_working"

# Create directories if they don't exist
mkdir -p "$INPUT_DIR" "$OUTPUT_DIR" "$WORKING_DIR"

# ============================================================================
# VALIDATION
# ============================================================================

if [ ! -f "$INPUT_DIR/$INPUT_FILE_NAME" ]; then
    echo "❌ ERROR: Input file not found: $INPUT_DIR/$INPUT_FILE_NAME"
    echo "   Please place your input pricelist file in 00_inputs/"
    exit 1
fi

echo "=========================================="
echo "Catalog Pipeline: $SERIES"
echo "WEF: $WEF"
echo "Input: $INPUT_FILE_NAME"
echo "=========================================="
echo ""

# ============================================================================
# STEP 1: Inspect Raw Input (Optional - for debugging)
# ============================================================================

echo "📋 Step 1: Inspecting raw input..."
if [ -f "$SCRIPTS_DIR/inspect_${SERIES,,}_raw.py" ]; then
    python3 "$SCRIPTS_DIR/inspect_${SERIES,,}_raw.py" \
        --input_xlsx "$INPUT_DIR/$INPUT_FILE_NAME" \
        --out "$WORKING_DIR/${SERIES}_raw_inspection.txt" || true
    echo "   ✅ Raw inspection complete"
else
    echo "   ⚠️  No raw inspection script found (skipping)"
fi
echo ""

# ============================================================================
# STEP 2: Extract Canonical Tables
# ============================================================================

echo "📋 Step 2: Extracting canonical tables..."
CANONICAL_OUTPUT="$OUTPUT_DIR/${SERIES}_CANONICAL_v${VERSION}.xlsx"

if [ -f "$SCRIPTS_DIR/${SERIES,,}_extract_canonical.py" ]; then
    python3 "$SCRIPTS_DIR/${SERIES,,}_extract_canonical.py" \
        --input_xlsx "$INPUT_DIR/$INPUT_FILE_NAME" \
        --out "$CANONICAL_OUTPUT"
    echo "   ✅ Canonical extraction complete: $CANONICAL_OUTPUT"
else
    echo "   ❌ ERROR: Canonical extraction script not found: $SCRIPTS_DIR/${SERIES,,}_extract_canonical.py"
    exit 1
fi
echo ""

# ============================================================================
# STEP 3: Build L2 from Canonical
# ============================================================================

echo "📋 Step 3: Building L2 from canonical..."
L2_OUTPUT="$OUTPUT_DIR/${SERIES}_L2_tmp.xlsx"

python3 "$SCRIPTS_DIR/build_l2_from_canonical.py" \
    --input "$CANONICAL_OUTPUT" \
    --pricelist_ref "WEF ${WEF}" \
    --effective_from "${WEF}" \
    --currency INR \
    --region INDIA \
    --out "$L2_OUTPUT"

echo "   ✅ L2 generation complete: $L2_OUTPUT"
echo ""

# ============================================================================
# STEP 4: Derive L1 from L2
# ============================================================================

echo "📋 Step 4: Deriving L1 from L2..."
L1_OUTPUT="$OUTPUT_DIR/${SERIES}_L1_tmp.xlsx"

python3 "$SCRIPTS_DIR/derive_l1_from_l2.py" \
    --l2 "$L2_OUTPUT" \
    --l1_mode duty_x_voltage \
    --include_accessories true \
    --out "$L1_OUTPUT"

echo "   ✅ L1 generation complete: $L1_OUTPUT"
echo ""

# ============================================================================
# STEP 5: Validate Canonical Against Source (Self-Validation)
# ============================================================================

echo "📋 Step 5: Validating canonical extraction against source files..."
VALIDATION_REPORT="$OUTPUT_DIR/VALIDATION_REPORT.txt"

python3 "$SCRIPTS_DIR/validate_canonical_against_source.py" \
    --canonical "$CANONICAL_OUTPUT" \
    --xlsx "$INPUT_DIR/$INPUT_FILE_NAME" \
    --out "$VALIDATION_REPORT" || true

if [ -f "$VALIDATION_REPORT" ]; then
    echo "   ✅ Validation report: $VALIDATION_REPORT"
    echo "   ⚠️  Review warnings/issues in validation report"
else
    echo "   ⚠️  Validation report not generated (non-blocking)"
fi
echo ""

# ============================================================================
# STEP 6: Build NSW Format Workbook (PRIMARY FREEZE ARTIFACT)
# ============================================================================

echo "📋 Step 6: Building NSW format workbook (primary freeze artifact)..."
NSW_OUTPUT="$OUTPUT_DIR/NSW_${SERIES}_WEF_${WEF}_v${VERSION}.xlsx"

# Series-specific configuration (customize per series)
SERIES_NAME="Easy TeSys"  # Default for Schneider, customize if needed

python3 "$SCRIPTS_DIR/build_nsw_workbook_from_canonical.py" \
    --canonical "$CANONICAL_OUTPUT" \
    --series "$SERIES" \
    --series_name "$SERIES_NAME" \
    --wef "$WEF" \
    --pricelist_ref "WEF ${WEF}" \
    --out "$NSW_OUTPUT"

if [ -f "$NSW_OUTPUT" ]; then
    echo "   ✅ NSW format workbook complete: $NSW_OUTPUT"
    echo "   📌 This is the PRIMARY freeze artifact"
else
    echo "   ❌ ERROR: NSW format workbook generation failed"
    exit 1
fi
echo ""

# ============================================================================
# STEP 7: Generate Engineer Review Workbook (OPTIONAL - Legacy Format)
# ============================================================================

echo "📋 Step 7: Building engineer review workbook (optional, legacy format)..."
ENGINEER_OUTPUT="$OUTPUT_DIR/NSW_MASTER_SCHNEIDER_WEF_${WEF}_ENGINEER_REVIEW.xlsx"

python3 "$SCRIPTS_DIR/build_master_workbook.py" \
    --l2 "$L2_OUTPUT" \
    --l1 "$L1_OUTPUT" \
    --out "$ENGINEER_OUTPUT" || true

if [ -f "$ENGINEER_OUTPUT" ]; then
    echo "   ✅ Engineer review workbook: $ENGINEER_OUTPUT"
    echo "   ⚠️  NOTE: This is secondary output (legacy format)"
else
    echo "   ⚠️  Engineer review workbook generation skipped (optional)"
fi
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "=========================================="
echo "✅ Pipeline Complete!"
echo "=========================================="
echo ""
echo "Output files:"
echo "  - Canonical: $CANONICAL_OUTPUT"
echo "  - L2 (intermediate): $L2_OUTPUT"
echo "  - L1 (intermediate): $L1_OUTPUT"
echo "  - ✅ NSW Format (PRIMARY FREEZE ARTIFACT): $NSW_OUTPUT"
echo "  - Engineer Review (optional, legacy): $ENGINEER_OUTPUT"
echo ""
echo "Next steps:"
echo "  1. Review NSW format workbook: $NSW_OUTPUT"
echo "     - Verify NSW_L2_PRODUCTS, NSW_L1_CONFIG_LINES, NSW_VARIANT_MASTER, etc."
echo "     - Check duty/voltage normalization in L1"
echo "  2. Fill QC checklist: 03_qc/QC_SUMMARY.md"
echo "  3. Upload to ChatGPT for freeze review:"
echo "     - NSW file: $NSW_OUTPUT"
echo "     - QC summary: 03_qc/QC_SUMMARY.md"
echo "  4. After approval, archive to archives/schneider/$SERIES/$WEF/"
echo ""
echo "Note: Canonical extractor extracts FULL series (not just Page-8)."
echo "      Counts may differ from v6 Page-8-only output."
echo ""

