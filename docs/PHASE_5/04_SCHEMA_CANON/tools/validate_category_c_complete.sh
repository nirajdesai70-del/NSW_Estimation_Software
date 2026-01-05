#!/bin/bash
# Category-C Complete Validation Test Suite
# Validates all 6 groups (C1-C6) and 5 workflow steps

set -euo pipefail

REPO_ROOT="/Volumes/T9/Projects/NSW_Estimation_Software"
SCHEMA_DIR="${REPO_ROOT}/docs/PHASE_5/04_SCHEMA_CANON"
SCHEMA_DDL="${SCHEMA_DIR}/DDL/schema.sql"
INVENTORY_DIR="${SCHEMA_DIR}/INVENTORY"
TOOLS_DIR="${SCHEMA_DIR}/tools"

PASS=0
FAIL=0
WARN=0

echo "=========================================="
echo "CATEGORY-C COMPLETE VALIDATION SUITE"
echo "=========================================="
echo ""
echo "Validating all 6 groups (C1-C6) and 5 workflow steps..."
echo ""

# Helper functions
pass() {
    echo "  ✅ PASS: $1"
    ((PASS++)) || true
}

fail() {
    echo "  ❌ FAIL: $1"
    ((FAIL++)) || true
}

warn() {
    echo "  ⚠️  WARN: $1"
    ((WARN++)) || true
}

# Test 1: C1 - Step-1 Blueprint
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: C1 - Step-1 Blueprint → DDL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "${SCHEMA_DIR}/CATEGORY_C_STEP1_BLUEPRINT.md" ]; then
    pass "Blueprint document exists"
else
    fail "Blueprint document missing: CATEGORY_C_STEP1_BLUEPRINT.md"
fi

if [ -f "${TOOLS_DIR}/generate_schema_from_blueprint.py" ]; then
    pass "Blueprint generator script exists"
else
    fail "Generator script missing: generate_schema_from_blueprint.py"
fi

if [ -f "$SCHEMA_DDL" ]; then
    SCHEMA_TABLES=$(grep -i "^CREATE TABLE" "$SCHEMA_DDL" | wc -l | tr -d ' ')
    if [ "$SCHEMA_TABLES" -eq 34 ]; then
        pass "Schema.sql has 34 tables (as expected)"
    else
        fail "Schema.sql has ${SCHEMA_TABLES} tables (expected 34)"
    fi
else
    fail "Schema.sql missing: $SCHEMA_DDL"
fi

if grep -q "CATEGORY_C_STEP1_BLUEPRINT.md" "$SCHEMA_DDL" 2>/dev/null; then
    pass "Schema.sql references blueprint"
else
    warn "Schema.sql doesn't reference blueprint (may be OK)"
fi

echo ""

# Test 2: C2 - Step-2 Constraints
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: C2 - Step-2 Constraints → DDL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "${SCHEMA_DIR}/CATEGORY_C_STEP2_CONSTRAINTS.md" ]; then
    pass "Constraints document exists"
else
    warn "Constraints document missing: CATEGORY_C_STEP2_CONSTRAINTS.md"
fi

if [ -f "$SCHEMA_DDL" ]; then
    FK_COUNT=$(grep -i "FOREIGN KEY" "$SCHEMA_DDL" | wc -l | tr -d ' ')
    if [ "$FK_COUNT" -ge 70 ]; then
        pass "Schema.sql has ${FK_COUNT} foreign keys (expected ~76)"
    else
        warn "Schema.sql has ${FK_COUNT} foreign keys (expected ~76)"
    fi
    
    CHECK_COUNT=$(grep -i "CHECK" "$SCHEMA_DDL" | wc -l | tr -d ' ')
    if [ "$CHECK_COUNT" -ge 15 ]; then
        pass "Schema.sql has ${CHECK_COUNT} CHECK constraints (expected ~16)"
    else
        warn "Schema.sql has ${CHECK_COUNT} CHECK constraints (expected ~16)"
    fi
    
    # Check guardrails
    if grep -qi "g01\|product_id IS NULL" "$SCHEMA_DDL"; then
        pass "G-01 guardrail present (product_id IS NULL)"
    else
        fail "G-01 guardrail missing"
    fi
    
    if grep -qi "g02\|resolution_status.*L2.*product_id" "$SCHEMA_DDL"; then
        pass "G-02 guardrail present (L2 requires product_id)"
    else
        fail "G-02 guardrail missing"
    fi
else
    fail "Schema.sql missing for constraint validation"
fi

echo ""

# Test 3: C3 - Step-4 ER Diagram
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: C3 - Step-4 ER Diagram"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ER_DIR="${SCHEMA_DIR}/ER_DIAGRAM"
if [ -d "$ER_DIR" ]; then
    pass "ER diagram directory exists"
    
    if [ -f "${ER_DIR}/ER_MAIN.drawio" ]; then
        pass "ER diagram drawio file exists"
    else
        warn "ER diagram drawio file missing"
    fi
    
    if [ -f "${ER_DIR}/ER_MAIN.pdf" ]; then
        pass "ER diagram PDF exists"
    else
        warn "ER diagram PDF missing"
    fi
    
    if [ -f "${ER_DIR}/ER_MAIN.png" ]; then
        pass "ER diagram PNG exists"
    else
        warn "ER diagram PNG missing"
    fi
else
    fail "ER diagram directory missing: $ER_DIR"
fi

echo ""

# Test 4: C4 - Step-3 Inventory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: C4 - Step-3 Inventory"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "$INVENTORY_DIR" ]; then
    pass "Inventory directory exists"
    
    FULL_INV="${INVENTORY_DIR}/NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv"
    KEY_ONLY="${INVENTORY_DIR}/NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv"
    DIFF_VIEW="${INVENTORY_DIR}/NSW_INVENTORY_DIFF_VIEW_v1.0.csv"
    
    if [ -f "$FULL_INV" ]; then
        FULL_LINES=$(wc -l < "$FULL_INV" | tr -d ' ')
        if [ "$FULL_LINES" -gt 100 ]; then
            FULL_TABLES=$(tail -n +2 "$FULL_INV" | cut -d',' -f1 | sort -u | wc -l | tr -d ' ')
            if [ "$FULL_TABLES" -eq 34 ]; then
                pass "Full inventory has 34 tables (${FULL_LINES} rows)"
            else
                fail "Full inventory has ${FULL_TABLES} tables (expected 34, ${FULL_LINES} rows)"
            fi
        else
            fail "Full inventory appears empty (only ${FULL_LINES} lines)"
        fi
    else
        fail "Full inventory CSV missing"
    fi
    
    if [ -f "$KEY_ONLY" ]; then
        KEY_TABLES=$(tail -n +2 "$KEY_ONLY" | cut -d',' -f2 | sort -u | wc -l | tr -d ' ')
        if [ "$KEY_TABLES" -eq 34 ]; then
            pass "Key-only inventory has 34 tables"
        else
            fail "Key-only inventory has ${KEY_TABLES} tables (expected 34)"
        fi
    else
        fail "Key-only inventory CSV missing"
    fi
    
    if [ -f "$DIFF_VIEW" ]; then
        pass "Diff view CSV exists"
    else
        warn "Diff view CSV missing"
    fi
    
    if [ -f "${INVENTORY_DIR}/README.md" ]; then
        pass "Inventory README exists"
    else
        warn "Inventory README missing"
    fi
else
    fail "Inventory directory missing: $INVENTORY_DIR"
fi

echo ""

# Test 5: C5 - Step-4 Seed Script
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 5: C5 - Step-4 Seed Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SEED_SCRIPT="${SCHEMA_DIR}/SEED_DESIGN_VALIDATION.sql"
if [ -f "$SEED_SCRIPT" ]; then
    pass "Seed script exists"
    
    if grep -qi "tenant\|users\|roles" "$SEED_SCRIPT"; then
        pass "Seed script includes tenant/users/roles"
    else
        warn "Seed script may not include tenant/users/roles"
    fi
    
    if grep -qi "INSERT\|VALUES" "$SEED_SCRIPT"; then
        pass "Seed script contains data inserts"
    else
        warn "Seed script may not contain data"
    fi
else
    fail "Seed script missing: $SEED_SCRIPT"
fi

echo ""

# Test 6: C6 - Step-5 Schema Canon + Validation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 6: C6 - Step-5 Schema Canon + Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CANON_DOC="${SCHEMA_DIR}/NSW_SCHEMA_CANON_v1.0.md"
VALIDATION_DOC="${SCHEMA_DIR}/CATEGORY_C_STEP5_VALIDATION_GATE_PASSED.md"
VALIDATION_SCRIPT="${REPO_ROOT}/validate_schema_ddl.sh"

if [ -f "$CANON_DOC" ]; then
    pass "Schema Canon document exists"
else
    fail "Schema Canon document missing: $CANON_DOC"
fi

if [ -f "$VALIDATION_DOC" ]; then
    pass "Validation gate documentation exists"
    
    if grep -qi "PASSED\|VALIDATED" "$VALIDATION_DOC"; then
        pass "Validation gate shows PASSED status"
    else
        warn "Validation gate status unclear"
    fi
else
    fail "Validation gate documentation missing"
fi

if [ -f "$VALIDATION_SCRIPT" ]; then
    pass "Validation script exists (validate_schema_ddl.sh)"
else
    warn "Validation script missing (may be in repo root)"
fi

if [ -f "$SCHEMA_DDL" ]; then
    pass "Validated DDL exists (schema.sql)"
fi

echo ""

# Test 7: Cross-validation (Inventory vs Schema)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 7: Cross-Validation (Inventory vs Schema)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "$SCHEMA_DDL" ] && [ -f "$KEY_ONLY" ]; then
    SCHEMA_TABLES_LIST=$(grep -i "^CREATE TABLE" "$SCHEMA_DDL" | sed 's/^CREATE TABLE //;s/ (.*$//' | sort)
    KEY_TABLES_LIST=$(tail -n +2 "$KEY_ONLY" | cut -d',' -f2 | sort | uniq)
    
    MISSING=$(comm -23 <(echo "$SCHEMA_TABLES_LIST") <(echo "$KEY_TABLES_LIST") | grep -v '^$' || true)
    EXTRA=$(comm -13 <(echo "$SCHEMA_TABLES_LIST") <(echo "$KEY_TABLES_LIST") | grep -v '^$' || true)
    
    if [ -z "$MISSING" ] && [ -z "$EXTRA" ]; then
        pass "Inventory tables match schema.sql (34/34)"
    else
        if [ -n "$MISSING" ]; then
            fail "Missing in inventory: $(echo "$MISSING" | tr '\n' ',' | sed 's/,$//')"
        fi
        if [ -n "$EXTRA" ]; then
            warn "Extra in inventory: $(echo "$EXTRA" | tr '\n' ',' | sed 's/,$//')"
        fi
    fi
else
    warn "Cannot perform cross-validation (files missing)"
fi

echo ""

# Summary
echo "=========================================="
echo "VALIDATION SUMMARY"
echo "=========================================="
echo "✅ PASS: $PASS"
echo "⚠️  WARN: $WARN"
echo "❌ FAIL: $FAIL"
echo ""

if [ "$FAIL" -eq 0 ] && [ "$WARN" -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED - Category-C Complete!"
    exit 0
elif [ "$FAIL" -eq 0 ]; then
    echo "✅ ALL CRITICAL TESTS PASSED (some warnings)"
    exit 0
else
    echo "❌ VALIDATION FAILED - Action Required"
    exit 1
fi

