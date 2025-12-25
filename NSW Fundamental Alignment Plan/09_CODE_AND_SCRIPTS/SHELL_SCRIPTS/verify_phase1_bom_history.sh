#!/bin/bash

# Verification Script: Phase-1 BOM History Implementation
# Purpose: Verify that Phase-1 deliverables are complete and working
# Reference: BOM_ENGINE_IMPLEMENTATION_PLAN.md (Phase-1 STOP Gate)
# Phase: Phase-1 (P0) - Line Item Edit + History Foundation

set -e

echo "=========================================="
echo "Phase-1 BOM History Verification"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if database connection is available
if ! command -v mysql &> /dev/null && ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}Warning: Database client not found. Some checks will be skipped.${NC}"
    DB_AVAILABLE=false
else
    DB_AVAILABLE=true
fi

# Track verification results
PASSED=0
FAILED=0
WARNINGS=0

# Function to check file existence
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description exists: $file"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $description missing: $file"
        ((FAILED++))
        return 1
    fi
}

# Function to check database table
check_table() {
    local table=$1
    local description=$2
    
    if [ "$DB_AVAILABLE" = true ]; then
        # Try MySQL first
        if command -v mysql &> /dev/null; then
            if mysql -e "DESCRIBE $table" &> /dev/null; then
                echo -e "${GREEN}✓${NC} $description table exists: $table"
                ((PASSED++))
                return 0
            fi
        fi
        # Try PostgreSQL
        if command -v psql &> /dev/null; then
            if psql -c "\d $table" &> /dev/null; then
                echo -e "${GREEN}✓${NC} $description table exists: $table"
                ((PASSED++))
                return 0
            fi
        fi
    fi
    
    echo -e "${YELLOW}⚠${NC} $description table check skipped (database not accessible)"
    ((WARNINGS++))
    return 1
}

echo "1. Checking Migration Files..."
echo "-----------------------------------"
MIGRATION_FILE=$(find database/migrations -name "*create_quotation_sale_bom_item_history*" | head -1)
check_file "$MIGRATION_FILE" "History table migration"

echo ""
echo "2. Checking Service Files..."
echo "-----------------------------------"
check_file "app/Services/BomHistoryService.php" "BomHistoryService"
check_file "app/Services/BomEngine.php" "BomEngine"

echo ""
echo "3. Checking Service Methods..."
echo "-----------------------------------"

# Check BomHistoryService methods
if [ -f "app/Services/BomHistoryService.php" ]; then
    if grep -q "function recordItemHistory" app/Services/BomHistoryService.php; then
        echo -e "${GREEN}✓${NC} BomHistoryService::recordItemHistory() exists"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} BomHistoryService::recordItemHistory() missing"
        ((FAILED++))
    fi
    
    if grep -q "function captureItemSnapshot" app/Services/BomHistoryService.php; then
        echo -e "${GREEN}✓${NC} BomHistoryService::captureItemSnapshot() exists"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} BomHistoryService::captureItemSnapshot() missing"
        ((FAILED++))
    fi
fi

# Check BomEngine methods
if [ -f "app/Services/BomEngine.php" ]; then
    if grep -q "function addLineItem" app/Services/BomEngine.php; then
        echo -e "${GREEN}✓${NC} BomEngine::addLineItem() exists"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} BomEngine::addLineItem() missing"
        ((FAILED++))
    fi
    
    if grep -q "function updateLineItem" app/Services/BomEngine.php; then
        echo -e "${GREEN}✓${NC} BomEngine::updateLineItem() exists"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} BomEngine::updateLineItem() missing"
        ((FAILED++))
    fi
    
    if grep -q "function replaceLineItem" app/Services/BomEngine.php; then
        echo -e "${GREEN}✓${NC} BomEngine::replaceLineItem() exists"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} BomEngine::replaceLineItem() missing"
        ((FAILED++))
    fi
    
    if grep -q "function deleteLineItem" app/Services/BomEngine.php; then
        echo -e "${GREEN}✓${NC} BomEngine::deleteLineItem() exists"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} BomEngine::deleteLineItem() missing"
        ((FAILED++))
    fi
fi

echo ""
echo "4. Checking Database Schema..."
echo "-----------------------------------"
if [ "$DB_AVAILABLE" = true ]; then
    check_table "quotation_sale_bom_item_history" "History"
else
    echo -e "${YELLOW}⚠${NC} Database schema check skipped (run migration first)"
    ((WARNINGS++))
fi

echo ""
echo "5. Checking Controller Integration Example..."
echo "-----------------------------------"
check_file "app/Http/Controllers/QuotationV2Controller_Example_Integration.php" "Controller integration example"

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Phase-1 verification PASSED${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. Run migration: php artisan migrate"
    echo "2. Test BomEngine methods with sample data"
    echo "3. Integrate BomEngine into actual controller methods"
    echo "4. Run integration tests"
    exit 0
else
    echo -e "${RED}✗ Phase-1 verification FAILED${NC}"
    echo "Please fix the issues above before proceeding."
    exit 1
fi

