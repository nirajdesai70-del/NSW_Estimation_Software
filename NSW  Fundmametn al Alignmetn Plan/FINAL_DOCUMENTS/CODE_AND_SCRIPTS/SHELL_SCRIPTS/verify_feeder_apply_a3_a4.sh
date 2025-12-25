#!/bin/bash
#
# Feeder BOM Round-0: A3/A4 Validation Script
# Validates feeder apply operations using A3 (status distribution) and A4 (duplicate detection) queries
#
# Usage: ./scripts/governance/verify_feeder_apply_a3_a4.sh <FEEDER_ID> [--laravel-path PATH]
#
# Requirements:
#   - Laravel application with database access
#   - FEEDER_ID must be a valid QuotationSaleBomId
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
FEEDER_ID="${1:-}"
LARAVEL_PATH="${2:-}"

# Default Laravel path (try common locations)
if [ -z "$LARAVEL_PATH" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    
    # Try to find Laravel app
    if [ -f "/Users/nirajdesai/Projects/nish/artisan" ]; then
        LARAVEL_PATH="/Users/nirajdesai/Projects/nish"
    elif [ -f "$REPO_ROOT/../nish/artisan" ]; then
        LARAVEL_PATH="$REPO_ROOT/../nish"
    else
        echo -e "${RED}❌ ERROR:${NC} Laravel application not found"
        echo "   Please specify --laravel-path or ensure Laravel is in a standard location"
        exit 1
    fi
fi

if [ -z "$FEEDER_ID" ]; then
    echo -e "${RED}❌ ERROR:${NC} FEEDER_ID is required"
    echo "Usage: $0 <FEEDER_ID> [--laravel-path PATH]"
    exit 1
fi

if [ ! -f "$LARAVEL_PATH/artisan" ]; then
    echo -e "${RED}❌ ERROR:${NC} Laravel artisan not found at: $LARAVEL_PATH"
    exit 1
fi

echo -e "${BLUE}🔍 Feeder BOM Round-0: A3/A4 Validation${NC}"
echo "=========================================="
echo "Feeder ID: $FEEDER_ID"
echo "Laravel Path: $LARAVEL_PATH"
echo ""

cd "$LARAVEL_PATH"

# Create temporary PHP script for queries
TEMP_SCRIPT=$(mktemp /tmp/feeder_verify_XXXXXX.php)
cat > "$TEMP_SCRIPT" << EOFPHP
<?php
require __DIR__ . '/vendor/autoload.php';
\$app = require_once __DIR__ . '/bootstrap/app.php';
\$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

\$feederId = \$argv[1] ?? null;
if (!\$feederId) {
    echo "ERROR: FEEDER_ID required\n";
    exit(1);
}

// A3 Query: Status Distribution
\$results = DB::select('
    SELECT 
        Status,
        COUNT(*) AS item_count
    FROM quotation_sale_bom_items
    WHERE QuotationSaleBomId = ?
    GROUP BY Status
    ORDER BY Status
', [\$feederId]);

echo "A3_RESULTS_START\n";
foreach (\$results as \$row) {
    echo "Status=" . \$row->Status . ": " . \$row->item_count . " items\n";
}
echo "A3_RESULTS_END\n";

// A4 Query: Duplicate Detection
\$duplicates = DB::select('
    SELECT 
        ProductId,
        MakeId,
        SeriesId,
        COUNT(*) AS duplicate_count
    FROM quotation_sale_bom_items
    WHERE QuotationSaleBomId = ?
      AND Status = 0
    GROUP BY ProductId, MakeId, SeriesId
    HAVING COUNT(*) > 1
    ORDER BY duplicate_count DESC, ProductId
', [\$feederId]);

echo "A4_RESULTS_START\n";
if (count(\$duplicates) === 0) {
    echo "NO_DUPLICATES\n";
} else {
    echo "DUPLICATES_FOUND: " . count(\$duplicates) . " groups\n";
    foreach (\$duplicates as \$dup) {
        echo "  ProductId=" . \$dup->ProductId . ", MakeId=" . \$dup->MakeId . ", SeriesId=" . \$dup->SeriesId . ": " . \$dup->duplicate_count . " duplicates\n";
    }
}
echo "A4_RESULTS_END\n";
EOFPHP

# A3 Query: Status Distribution
echo -e "${BLUE}📊 A3 Query: Status Distribution${NC}"
echo "----------------------------------------"
A3_OUTPUT=$(php "$TEMP_SCRIPT" "$FEEDER_ID" 2>&1 | sed -n '/A3_RESULTS_START/,/A3_RESULTS_END/p' | grep -v "A3_RESULTS")
echo "$A3_OUTPUT"
echo ""

# Extract counts for validation
STATUS_0_COUNT=$(echo "$A3_OUTPUT" | grep -oP "Status=0: \K\d+" || echo "0")
STATUS_1_COUNT=$(echo "$A3_OUTPUT" | grep -oP "Status=1: \K\d+" || echo "0")

# A4 Query: Duplicate Detection
echo -e "${BLUE}🔍 A4 Query: Duplicate Detection${NC}"
echo "----------------------------------------"
A4_OUTPUT=$(php "$TEMP_SCRIPT" "$FEEDER_ID" 2>&1 | sed -n '/A4_RESULTS_START/,/A4_RESULTS_END/p' | grep -v "A4_RESULTS")
echo "$A4_OUTPUT"
echo ""

# Cleanup
rm -f "$TEMP_SCRIPT"

# Check for duplicates
DUPLICATE_COUNT=$(echo "$A4_OUTPUT" | grep -c "DUPLICATES_FOUND" || echo "0")

# Validation Summary
echo "=========================================="
echo -e "${BLUE}📋 Validation Summary${NC}"
echo "=========================================="
echo "A3 Status=0 count: $STATUS_0_COUNT"
echo "A3 Status=1 count: $STATUS_1_COUNT"
echo ""

if [ "$DUPLICATE_COUNT" -gt 0 ]; then
    echo -e "${RED}❌ FAIL:${NC} A4 detected duplicates!"
    echo -e "${RED}   STOP immediately - clear-before-copy is not working correctly${NC}"
    echo ""
    echo "Expected: 0 duplicate rows"
    echo "Found: Duplicates detected"
    exit 1
else
    echo -e "${GREEN}✅ PASS:${NC} A4 validation passed (no duplicates)"
    echo ""
    echo "A3 Status Distribution:"
    echo "  - Active items (Status=0): $STATUS_0_COUNT"
    echo "  - Soft-deleted items (Status=1): $STATUS_1_COUNT"
    echo ""
    echo -e "${GREEN}✅ All validations passed${NC}"
    exit 0
fi
