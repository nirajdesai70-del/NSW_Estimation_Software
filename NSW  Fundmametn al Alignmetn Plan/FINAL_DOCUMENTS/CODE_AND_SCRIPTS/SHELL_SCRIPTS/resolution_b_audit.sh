#!/usr/bin/env bash
# Resolution-B Safety Audit Script (READ-ONLY)
# Purpose: Scan repository for forbidden patterns that violate L2 write enforcement rules
# Output: resolution_b_audit_present_repo.txt

set -euo pipefail

OUTPUT_FILE="resolution_b_audit_present_repo.txt"
REPO_PATH="$(pwd)"

echo "=== Resolution-B Safety Audit ===" | tee "$OUTPUT_FILE"
echo "Repository: $REPO_PATH" | tee -a "$OUTPUT_FILE"
echo "Date: $(date)" | tee -a "$OUTPUT_FILE"
echo "Mode: READ-ONLY (no file modifications)" | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"

# Colors for output (if terminal supports)
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check if ripgrep is available
HAS_RG=0
if command -v rg >/dev/null 2>&1; then
    HAS_RG=1
fi

# Scan function
scan() {
    local title="$1"
    local pattern="$2"
    local severity="${3:-MEDIUM}"
    local search_path="${4:-app}"

    echo | tee -a "$OUTPUT_FILE"
    echo "## $title [Severity: $severity]" | tee -a "$OUTPUT_FILE"
    echo "Pattern: $pattern" | tee -a "$OUTPUT_FILE"
    echo "Search path: $search_path" | tee -a "$OUTPUT_FILE"
    echo "---" | tee -a "$OUTPUT_FILE"

    local count=0

    if [[ $HAS_RG -eq 1 ]]; then
        # Use ripgrep with exclusions
        local results
        results=$(rg -n --hidden \
            --glob '!.git/*' \
            --glob '!vendor/*' \
            --glob '!storage/*' \
            --glob '!node_modules/*' \
            --glob '!*.log' \
            --glob '!*.cache' \
            "$pattern" "$search_path" 2>/dev/null || true)

        if [[ -n "$results" ]]; then
            echo "$results" | tee -a "$OUTPUT_FILE"
            count=$(echo "$results" | wc -l | tr -d ' ')
        fi
    else
        # Fallback to grep
        local results
        results=$(grep -RIn \
            --exclude-dir=.git \
            --exclude-dir=vendor \
            --exclude-dir=storage \
            --exclude-dir=node_modules \
            --exclude='*.log' \
            "$pattern" "$search_path" 2>/dev/null || true)

        if [[ -n "$results" ]]; then
            echo "$results" | tee -a "$OUTPUT_FILE"
            count=$(echo "$results" | wc -l | tr -d ' ')
        fi
    fi

    if [[ $count -eq 0 ]]; then
        echo "✅ No matches found" | tee -a "$OUTPUT_FILE"
    else
        echo "⚠️  Found $count match(es)" | tee -a "$OUTPUT_FILE"
    fi
}

# Summary counters
TOTAL_ISSUES=0
CRITICAL_ISSUES=0
HIGH_ISSUES=0
MEDIUM_ISSUES=0

count_issues() {
    local severity="$1"
    local count="$2"
    TOTAL_ISSUES=$((TOTAL_ISSUES + count))
    case "$severity" in
        CRITICAL)
            CRITICAL_ISSUES=$((CRITICAL_ISSUES + count))
            ;;
        HIGH)
            HIGH_ISSUES=$((HIGH_ISSUES + count))
            ;;
        MEDIUM)
            MEDIUM_ISSUES=$((MEDIUM_ISSUES + count))
            ;;
    esac
}

echo "Starting audit..." | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"

# ============================================
# 1. RAW DB INSERTS (CRITICAL)
# ============================================
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "1. RAW DB INSERTS (CRITICAL SEVERITY)" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"

scan \
    "Raw DB insert into quotation_sale_bom_items" \
    "DB::table\(['\"]quotation_sale_bom_items['\"]\)->insert" \
    "CRITICAL" \
    "app"

scan \
    "Raw DB insert (alternative pattern)" \
    "DB::table\(['\"]quotation_sale_bom_items['\"]\)->insert\(|DB::table\(['\"]quotation_sale_bom_items['\"]\)->insertBatch" \
    "CRITICAL" \
    "app"

scan \
    "Direct DB::insert for quotation_sale_bom_items" \
    "DB::insert.*quotation_sale_bom_items" \
    "CRITICAL" \
    "app"

# ============================================
# 2. DEFAULT-ZERO PATTERNS (HIGH)
# ============================================
echo | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "2. DEFAULT-ZERO PATTERNS (HIGH SEVERITY)" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"

scan \
    "MakeId default to zero (null coalescing)" \
    "MakeId['\"]?\s*=>\s*[^,]*\?\?\s*0|['\"]MakeId['\"]?\s*=>\s*0[,\s]" \
    "HIGH" \
    "app"

scan \
    "SeriesId default to zero (null coalescing)" \
    "SeriesId['\"]?\s*=>\s*[^,]*\?\?\s*0|['\"]SeriesId['\"]?\s*=>\s*0[,\s]" \
    "HIGH" \
    "app"

scan \
    "MakeId ternary to zero" \
    "MakeId.*\?.*:\s*0|makeId.*\?.*:\s*0" \
    "HIGH" \
    "app"

scan \
    "SeriesId ternary to zero" \
    "SeriesId.*\?.*:\s*0|seriesId.*\?.*:\s*0" \
    "HIGH" \
    "app"

# ============================================
# 3. PRODUCTTYPE VALIDATION (HIGH)
# ============================================
echo | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "3. MISSING PRODUCTTYPE VALIDATION (HIGH SEVERITY)" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"

scan \
    "QuotationSaleBomItem::create without ProductType check" \
    "QuotationSaleBomItem::create" \
    "HIGH" \
    "app"

# Note: This will find ALL creates, but doesn't guarantee validation is missing
# Manual review required

# ============================================
# 4. DUPLICATE STACKING RISK (MEDIUM)
# ============================================
echo | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "4. DUPLICATE STACKING RISK (MEDIUM SEVERITY)" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"

scan \
    "Apply methods that may not clear existing items" \
    "applyMasterBom|applyFeederTemplate|applyProposalBom|addBomFromMaster" \
    "MEDIUM" \
    "app"

# Note: This finds apply methods but doesn't verify clear-before-copy logic
# Manual review required

# ============================================
# 5. SUMMARY
# ============================================
echo | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "AUDIT SUMMARY" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"

echo "Total patterns scanned: Multiple" | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"
echo "⚠️  NOTE: Pattern matches do not guarantee violations." | tee -a "$OUTPUT_FILE"
echo "   Manual code review required to confirm actual violations." | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"

echo "Next steps:" | tee -a "$OUTPUT_FILE"
echo "1. Review all matches in this report" | tee -a "$OUTPUT_FILE"
echo "2. Verify context of each match (false positives possible)" | tee -a "$OUTPUT_FILE"
echo "3. Confirm actual violations requiring fixes" | tee -a "$OUTPUT_FILE"
echo "4. Refer to RESOLUTION_B_WRITE_PATHS.md for complete inventory" | tee -a "$OUTPUT_FILE"
echo "5. Refer to RESOLUTION_B_ILLEGAL_DEFAULTS.md for detailed analysis" | tee -a "$OUTPUT_FILE"
echo | tee -a "$OUTPUT_FILE"

echo "=== Audit Complete ===" | tee -a "$OUTPUT_FILE"
echo "Report saved to: $OUTPUT_FILE" | tee -a "$OUTPUT_FILE"

# Make output file readable
chmod 644 "$OUTPUT_FILE"

echo
echo "✅ Audit complete. Report: $OUTPUT_FILE"

