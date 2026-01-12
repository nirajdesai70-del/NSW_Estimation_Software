# Category-C Full Regeneration Plan

**Purpose:** Regenerate all Category-C artifacts from validated Step-5 DDL to ensure completeness  
**Source of Truth:** `DDL/schema.sql` (validated, 34 tables, Step-5 PASSED ✅)  
**Date:** 2026-01-05

---

## Category-C Workflow Overview

```
Step-1: Blueprint (CATEGORY_C_STEP1_BLUEPRINT.md)
   ↓
Step-2: Constraints (CATEGORY_C_STEP2_CONSTRAINTS.md)
   ↓
Step-3: Inventory (INVENTORY/*.csv) ← WE ARE HERE
   ↓
Step-4: ER Diagram (ER_DIAGRAM/*)
   ↓
Step-5: DDL + Validation (DDL/schema.sql) ✅ VALIDATED
```

**Current Status:**
- ✅ Step-5: DDL validated (34 tables, all constraints pass)
- ⚠️ Step-3: Inventory incomplete (30/34 tables, missing column details)
- ✅ Step-4: ER Diagram exists
- ✅ Step-1/2: Blueprint/Constraints (used to generate schema.sql)

---

## Regeneration Strategy

### Option A: Full Category-C Re-run (Recommended for Safety)

**Approach:** Regenerate all artifacts from validated `schema.sql` (Step-5 output) as authoritative source

**Why This Approach:**
- ✅ Uses validated, frozen DDL (Step-5 passed)
- ✅ Ensures all artifacts match the final validated schema
- ✅ Catches any drift between steps
- ✅ Single source of truth (schema.sql)

**Steps:**

1. **Extract from schema.sql** (Step-5 validated DDL)
   - Parse all 34 tables
   - Extract all columns, types, constraints
   - Extract all FKs, indexes, CHECK constraints
   - Extract module assignments from comments

2. **Regenerate Step-3 Inventory** (from schema.sql)
   - Generate full inventory CSV (column-level)
   - Generate key-only inventory CSV (table-level)
   - Generate diff view CSV
   - Verify: All 34 tables present

3. **Verify Coverage Report**
   - Compare CSVs to schema.sql
   - Update counts to 34/34
   - Regenerate if needed

4. **Validate Completeness**
   - Run verification script
   - Confirm: 34 tables in all CSVs
   - Confirm: No missing/extra tables

---

## Regeneration Scripts & Tools

### Existing Tools

1. **`tools/generate_inventory_from_ddl.py`**
   - Status: ⚠️ PARTIALLY WORKING
   - Issue: Finds 30 tables instead of 34, column parsing incomplete
   - Fix Required: Improve DDL parser

2. **`tools/generate_schema_from_blueprint.py`**
   - Status: ✅ WORKING (used to generate schema.sql)
   - Purpose: Blueprint → DDL generation
   - Not needed for inventory regeneration (we use schema.sql directly)

### Required Fixes

**Fix `generate_inventory_from_ddl.py`:**
- Improve CREATE TABLE parsing to catch all 34 tables
- Fix column extraction to handle all data types
- Extract all constraints correctly (FKs, UNIQUE, CHECK)
- Extract module from table comments

---

## Execution Plan

### Phase 1: Fix Parser (15-20 min)
1. Debug why parser finds 30 instead of 34 tables
2. Fix column extraction logic
3. Test parser on schema.sql
4. Verify: All 34 tables parsed correctly

### Phase 2: Regenerate CSVs (5 min)
1. Run fixed parser
2. Generate full inventory CSV
3. Generate key-only inventory CSV  
4. Generate diff view CSV

### Phase 3: Verification (5 min)
1. Run verification script
2. Compare against schema.sql
3. Confirm: 34/34 tables in all CSVs
4. Confirm: All columns present in full inventory

### Phase 4: Documentation Update (5 min)
1. Update coverage report with new counts
2. Update verification report
3. Document regeneration process

**Total Time:** ~30-35 minutes

---

## Verification Checklist

After regeneration, verify:

- [ ] Full inventory CSV has 34 tables
- [ ] Full inventory CSV has all columns for all tables
- [ ] Key-only CSV has 34 tables with constraints
- [ ] Diff view shows all 34 tables as MATCH
- [ ] Coverage report claims 34/34 tables
- [ ] Verification script passes all checks
- [ ] No tables missing when compared to schema.sql
- [ ] No extra tables that don't exist in schema.sql

---

## Alternative: Quick Fix (If Time-Constrained)

**If full regeneration not possible now:**

1. Manually add 4 missing tables to key-only CSV
   - Extract from schema.sql: l1_attributes, l1_intent_lines, l1_l2_mappings, l1_line_groups
   - Add constraints, FKs, indexes

2. Fix parser later for full inventory CSV

3. Regenerate diff view after key-only is complete

**Note:** Quick fix maintains current structure but doesn't ensure full completeness of column-level data.

---

## Recommendation

✅ **Run Full Category-C Regeneration**

**Reasoning:**
- Validated schema.sql is the authoritative source (Step-5 PASSED)
- Ensures 100% completeness and accuracy
- Catches any drift between steps
- ~30 minutes to complete
- Provides clean baseline for future work

**Next Action:** Fix parser script and regenerate all inventory CSVs from schema.sql

---

**Created:** 2026-01-05  
**Status:** READY TO EXECUTE

