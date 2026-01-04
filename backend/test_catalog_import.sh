#!/bin/bash
# Test script for catalog import endpoint
# Run this from the backend directory

set -e

echo "=== Catalog Import Test Suite ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "alembic.ini" ]; then
    echo -e "${RED}Error: Must run from backend directory${NC}"
    exit 1
fi

# Step 1: Check Alembic status
echo -e "${YELLOW}Step 1: Checking Alembic migration status...${NC}"
if command -v alembic &> /dev/null || [ -f "venv/bin/alembic" ]; then
    ALEMBIC_CMD="alembic"
    if [ -f "venv/bin/alembic" ]; then
        ALEMBIC_CMD="venv/bin/alembic"
    fi
    
    echo "Current migration:"
    $ALEMBIC_CMD current || echo "No migrations applied yet"
    echo ""
    
    echo "Migration history:"
    $ALEMBIC_CMD history || true
    echo ""
else
    echo -e "${RED}Warning: Alembic not found. Skipping migration check.${NC}"
    echo ""
fi

# Step 2: Check if server is running
echo -e "${YELLOW}Step 2: Checking if FastAPI server is running...${NC}"
if curl -s http://localhost:8001/docs > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server is running on http://localhost:8001${NC}"
else
    echo -e "${RED}✗ Server is not running. Please start it with:${NC}"
    echo "  cd backend && uvicorn app.main:app --reload --port 8001"
    echo ""
    exit 1
fi
echo ""

# Step 3: Find FINAL CSV file
echo -e "${YELLOW}Step 3: Finding FINAL CSV file...${NC}"
FINAL_CSV="../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv"

if [ ! -f "$FINAL_CSV" ]; then
    echo -e "${RED}✗ FINAL CSV not found at: $FINAL_CSV${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found CSV: $FINAL_CSV${NC}"
echo "First few lines:"
head -3 "$FINAL_CSV"
echo ""

# Step 4: Dry run test
echo -e "${YELLOW}Step 4: Testing import with dry_run=true...${NC}"
DRY_RUN_RESPONSE=$(curl -s -X POST "http://localhost:8001/api/v1/catalog/skus/import?dry_run=true" \
    -F "file=@$FINAL_CSV" \
    -H "Content-Type: multipart/form-data")

if echo "$DRY_RUN_RESPONSE" | grep -q "batch_id"; then
    echo -e "${GREEN}✓ Dry run successful${NC}"
    echo "Response:"
    echo "$DRY_RUN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$DRY_RUN_RESPONSE"
else
    echo -e "${RED}✗ Dry run failed${NC}"
    echo "Response:"
    echo "$DRY_RUN_RESPONSE"
    exit 1
fi
echo ""

# Step 5: Check for errors in dry run
ERROR_COUNT=$(echo "$DRY_RUN_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('rows_error', 0))" 2>/dev/null || echo "0")
if [ "$ERROR_COUNT" -gt 0 ]; then
    echo -e "${RED}⚠ Warning: Dry run found $ERROR_COUNT errors${NC}"
    echo "Please review errors before committing"
    echo ""
    read -p "Continue with commit test? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 1
    fi
fi

# Step 6: Commit test (actual import)
echo -e "${YELLOW}Step 5: Testing import with dry_run=false (COMMIT)...${NC}"
read -p "This will write to database. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Skipping commit test"
    exit 0
fi

COMMIT_RESPONSE=$(curl -s -X POST "http://localhost:8001/api/v1/catalog/skus/import?dry_run=false" \
    -F "file=@$FINAL_CSV" \
    -H "Content-Type: multipart/form-data")

if echo "$COMMIT_RESPONSE" | grep -q "batch_id"; then
    echo -e "${GREEN}✓ Import committed successfully${NC}"
    echo "Response:"
    echo "$COMMIT_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$COMMIT_RESPONSE"
else
    echo -e "${RED}✗ Import commit failed${NC}"
    echo "Response:"
    echo "$COMMIT_RESPONSE"
    exit 1
fi
echo ""

# Step 7: Verify GET endpoints
echo -e "${YELLOW}Step 6: Verifying GET endpoints...${NC}"

echo "Testing GET /api/v1/catalog/skus:"
SKUS_RESPONSE=$(curl -s "http://localhost:8001/api/v1/catalog/skus?limit=5")
if echo "$SKUS_RESPONSE" | grep -q "skus"; then
    echo -e "${GREEN}✓ SKUs endpoint working${NC}"
    echo "$SKUS_RESPONSE" | python3 -m json.tool 2>/dev/null | head -20 || echo "$SKUS_RESPONSE" | head -20
else
    echo -e "${YELLOW}⚠ SKUs endpoint returned unexpected response${NC}"
    echo "$SKUS_RESPONSE"
fi
echo ""

echo -e "${GREEN}=== All Tests Complete ===${NC}"

