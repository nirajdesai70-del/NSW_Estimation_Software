#!/bin/bash
#
# Phase-4 Automated Gates Script
# Validates code and documentation against NEPL canonical rules
#
# Usage: ./scripts/governance/validate_phase4_gates.sh [--path PATH]
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default path (repo root)
SEARCH_PATH="${1:-.}"

# Track violations
VIOLATIONS=0
WARNINGS=0

echo "🔍 Phase-4 Automated Gates Validation"
echo "======================================"
echo "Search path: $SEARCH_PATH"
echo ""

# Function to report violation
violation() {
    echo -e "${RED}❌ VIOLATION:${NC} $1"
    ((VIOLATIONS++))
}

# Function to report warning
warning() {
    echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
    ((WARNINGS++))
}

# Function to report success
success() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
}

# Gate 1: Check for raw DB inserts into quotation_sale_bom_items
echo "Gate 1: Checking for raw DB inserts into quotation_sale_bom_items..."
if grep -r "DB::table('quotation_sale_bom_items')->insert" "$SEARCH_PATH" --include="*.php" 2>/dev/null | grep -v ".git" | grep -v "vendor" > /dev/null; then
    violation "Raw DB insert found: DB::table('quotation_sale_bom_items')->insert"
    grep -rn "DB::table('quotation_sale_bom_items')->insert" "$SEARCH_PATH" --include="*.php" 2>/dev/null | grep -v ".git" | grep -v "vendor" || true
else
    success "No raw DB inserts found"
fi

# Gate 2: Check for QuotationSaleBomItem::create outside ProposalBomItemWriter
echo ""
echo "Gate 2: Checking for QuotationSaleBomItem::create outside ProposalBomItemWriter..."
# This is a heuristic check - we look for create() calls and check if they're in the writer service
if grep -r "QuotationSaleBomItem::create" "$SEARCH_PATH" --include="*.php" 2>/dev/null | grep -v ".git" | grep -v "vendor" | grep -v "ProposalBomItemWriter" > /dev/null; then
    violation "QuotationSaleBomItem::create found outside ProposalBomItemWriter"
    grep -rn "QuotationSaleBomItem::create" "$SEARCH_PATH" --include="*.php" 2>/dev/null | grep -v ".git" | grep -v "vendor" | grep -v "ProposalBomItemWriter" || true
else
    success "No QuotationSaleBomItem::create calls outside gateway found"
fi

# Gate 3: Check for L0/L1/L2 block in key documentation files
echo ""
echo "Gate 3: Checking for L0/L1/L2 block or canonical reference in key docs..."
CANONICAL_RULES="docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md"
KEY_DOCS=(
    "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md"
    "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md"
    "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_GOVERNANCE_ONBOARDING_POSTER_v1.0_20251218.md"
)

for doc in "${KEY_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        if grep -q "NEPL_CANONICAL_RULES" "$doc" || grep -q "L0.*L1.*L2" "$doc"; then
            success "Canonical reference or L0/L1/L2 block found in $(basename $doc)"
        else
            warning "No canonical reference or L0/L1/L2 block found in $(basename $doc)"
        fi
    fi
done

# Gate 4: Check for gap registers missing Phase-3 revalidation sections
echo ""
echo "Gate 4: Checking gap registers for Phase-3 revalidation sections..."
GAP_REGISTERS=(
    "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md"
    "docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md"
)

for gap_reg in "${GAP_REGISTERS[@]}"; do
    if [ -f "$gap_reg" ]; then
        if grep -qi "phase.*3.*revalidation\|gap.*revalidation" "$gap_reg"; then
            success "Phase-3 revalidation section found in $(basename $gap_reg)"
        else
            warning "No Phase-3 revalidation section found in $(basename $gap_reg)"
        fi
    fi
done

# Gate 5: Check for silent default patterns (MakeId/SeriesId => 0)
echo ""
echo "Gate 5: Checking for silent default patterns (MakeId/SeriesId => 0)..."
if grep -r "MakeId.*=>.*0.*\?\?\|SeriesId.*=>.*0.*\?\?" "$SEARCH_PATH" --include="*.php" 2>/dev/null | grep -v ".git" | grep -v "vendor" | grep -v "ProposalBomItemWriter" > /dev/null; then
    violation "Silent default pattern found (MakeId/SeriesId => 0 ?? 0)"
    grep -rn "MakeId.*=>.*0.*\?\?\|SeriesId.*=>.*0.*\?\?" "$SEARCH_PATH" --include="*.php" 2>/dev/null | grep -v ".git" | grep -v "vendor" | grep -v "ProposalBomItemWriter" || true
else
    success "No silent default patterns found"
fi

# Gate 6: Verify canonical rules file exists
echo ""
echo "Gate 6: Verifying canonical rules file exists..."
if [ -f "$CANONICAL_RULES" ]; then
    success "Canonical rules file exists: $CANONICAL_RULES"
else
    violation "Canonical rules file missing: $CANONICAL_RULES"
fi

# Gate 7: Verify Cursor rules file exists
echo ""
echo "Gate 7: Verifying Cursor rules file exists..."
CURSOR_RULES=".cursor/rules/nepl_governance.mdc"
if [ -f "$CURSOR_RULES" ]; then
    success "Cursor rules file exists: $CURSOR_RULES"
else
    warning "Cursor rules file missing: $CURSOR_RULES"
fi

# Summary
echo ""
echo "======================================"
echo "Validation Summary"
echo "======================================"
echo -e "${RED}Violations: $VIOLATIONS${NC}"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}"

if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✅ All critical gates passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Validation failed with $VIOLATIONS violation(s)${NC}"
    exit 1
fi

