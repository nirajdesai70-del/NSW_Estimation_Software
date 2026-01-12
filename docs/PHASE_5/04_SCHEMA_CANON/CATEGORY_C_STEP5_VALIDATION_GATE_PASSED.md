# Category-C Step-5: DDL Validation Gate - PASSED ✅

**Date:** 2026-01-05  
**Status:** ✅ VALIDATED - READY FOR FREEZE  
**Gate:** Category-C Step-5 DDL Execution Validation  
**Validation Method:** Automated Docker-based PostgreSQL validation

---

## Executive Summary

**Category-C Step-5 DDL validation gate: PASSED ✅**

The canonical Schema Canon v1.0 DDL has been successfully validated against PostgreSQL 16-alpine in a throwaway Docker container. All critical guardrails are present, all constraints compile correctly, and the schema structure matches design specifications.

---

## Validation Results

### Schema Structure Validation

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| **Tables** | 34 | 34 | ✅ PASS |
| **Primary Keys** | 34 | 34 | ✅ PASS |
| **Foreign Keys** | 76 | 76 | ✅ PASS |
| **CHECK Constraints** | 16 | 16 | ✅ PASS |

### Critical Guardrail Validation

| Guardrail | Table | Constraint Pattern | Status |
|-----------|-------|-------------------|--------|
| **G-01** | `master_bom_items` | `ck_master_bom_items%g01%` | ✅ PRESENT |
| **G-02** | `quote_bom_items` | `ck_quote_bom_items%g02%` | ✅ PRESENT |
| **G-06** | `quote_bom_items` | `ck_quote_bom_items%g06%` | ✅ PRESENT |
| **G-07** | `quote_bom_items` | `ck_quote_bom_items%g07%` | ✅ PRESENT |

### Guardrail Details

**G-01: master_bom_items.product_id IS NULL**
- Constraint: `ck_master_bom_items__g01_product_id_null_1`
- Purpose: Enforces that master BOM items remain L0/L1 pure (no product_id)

**G-02: resolution_status <> 'L2' OR product_id IS NOT NULL**
- Constraint: `ck_quote_bom_items__g02_l2_requires_product_3`
- Purpose: Ensures L2 resolution requires product assignment

**G-06: rate_source <> 'FIXED_NO_DISCOUNT' OR discount_pct = 0**
- Constraint: `ck_quote_bom_items__g06_fixed_no_discount_2`
- Purpose: Enforces discount policy for fixed-rate items

**G-07: discount_pct BETWEEN 0 AND 100**
- Constraint: `ck_quote_bom_items__g07_discount_range_1`
- Purpose: Validates discount percentage range

---

## Validation Method

### Tool
- **Script:** `validate_schema_ddl.sh`
- **Location:** Repository root
- **Docker Context:** desktop-linux
- **Version:** Canonical (validated 2026-01-05)

### Environment
- **Database:** PostgreSQL 16-alpine (Docker)
- **Docker Context:** desktop-linux
- **Container:** `nswpg` (throwaway)
- **Database Name:** `nsw_schema_tmp`
- **Validation Method:** Full DDL execution + constraint enumeration

### Execution Command
```bash
./validate_schema_ddl.sh --context desktop-linux
```

### Validation Steps
1. ✅ Container cleanup and startup
2. ✅ Database creation (`nsw_schema_tmp`)
3. ✅ Schema DDL execution (`schema.sql`)
4. ✅ Table count verification (34 tables)
5. ✅ Constraint enumeration and validation
6. ✅ Critical guardrail spot checks (G-01, G-02, G-06, G-07)
7. ✅ Primary key and foreign key validation

---

## All CHECK Constraints Detected

| Table | Constraint Name |
|-------|----------------|
| `attribute_options` | `ck_attribute_options__check_1_1` |
| `cost_heads` | `ck_cost_heads__category_in_material_1` |
| `master_bom_items` | `ck_master_bom_items__g01_product_id_null_1` |
| `master_bom_items` | `ck_master_bom_items__resolution_status_in_l0_2` |
| `l1_intent_lines` | `ck_l1_intent_lines__line_type_in_base_1` |
| `l1_attributes` | `ck_l1_attributes__check_1_1` |
| `l1_attributes` | `ck_l1_attributes__check_2_2` |
| `l1_l2_mappings` | `ck_l1_l2_mappings__mapping_type_in_base_1` |
| `quotations` | `ck_quotations__g07_discount_range_1` |
| `quotations` | `ck_quotations__tax_mode_in_cgst_sgst_2` |
| `quote_boms` | `ck_quote_boms__level_in_0_1` |
| `quote_bom_items` | `ck_quote_bom_items__g02_l2_requires_product_3` |
| `quote_bom_items` | `ck_quote_bom_items__g06_fixed_no_discount_2` |
| `quote_bom_items` | `ck_quote_bom_items__g07_discount_range_1` |
| `quote_bom_items` | `ck_quote_bom_items__rate_source_in_pricelist_4` |
| `quote_bom_items` | `ck_quote_bom_items__resolution_status_in_l0_5` |

**Total:** 16 CHECK constraints

---

## Validation Artifacts

### Canonical Files Validated

1. **DDL File**
   - Path: `docs/PHASE_5/04_SCHEMA_CANON/DDL/schema.sql`
   - Lines: 751
   - Status: ✅ Validated and executable

2. **Validation Script**
   - Path: `validate_schema_ddl.sh`
   - Status: ✅ Canonical, production-ready
   - Features:
     - Git-based repo root detection
     - LIKE pattern constraint matching
     - Hardened bash (`set -euo pipefail`)
     - Unique log files per run

3. **Generator Script**
   - Path: `docs/PHASE_5/04_SCHEMA_CANON/tools/generate_schema_from_blueprint.py`
   - Status: ✅ Used to generate validated schema.sql

---

## Technical Notes

### Database Creation Fix Applied

**Issue:** Initial validation failed due to heredoc approach with `docker exec psql <<EOF` behaving inconsistently.

**Resolution:** Switched to explicit `psql -c "..."` commands for deterministic database creation.

**Implementation:**
```bash
$DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -v ON_ERROR_STOP=1 -c "DROP DATABASE IF EXISTS $DB_NAME;" >/dev/null 2>&1 || true
$DOCKER_CMD exec "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE $DB_NAME;" >/dev/null 2>&1
```

### Constraint Name Pattern Matching

Validation script uses LIKE patterns to match generated constraint names:
- Pattern: `ck_master_bom_items%g01%` (matches `ck_master_bom_items__g01_product_id_null_1`)
- Pattern: `ck_quote_bom_items%g02%` (matches `ck_quote_bom_items__g02_l2_requires_product_3`)
- Pattern: `ck_quote_bom_items%g06%` (matches `ck_quote_bom_items__g06_fixed_no_discount_2`)
- Pattern: `ck_quote_bom_items%g07%` (matches `ck_quote_bom_items__g07_discount_range_1`)

This approach accommodates the generator's constraint naming pattern: `ck_<table>__<guardrail>_<description>_<index>`

---

## Freeze Readiness Assessment

### ✅ Ready for Freeze

**Criteria Met:**
- ✅ DDL executes without errors
- ✅ All expected tables created (34/34)
- ✅ All primary keys present (34/34)
- ✅ All foreign keys created (76/76)
- ✅ All CHECK constraints compile (16/16)
- ✅ Critical guardrails present (G-01, G-02, G-06, G-07)
- ✅ Validation script is canonical and reusable
- ✅ Reproducible validation method documented

**No blockers identified.** Schema Canon v1.0 DDL is ready for canonical freeze.

---

## Next Actions

1. ✅ **DDL Validation:** COMPLETE (this document)
2. ⏭️ **Canonical Freeze:** Proceed with freeze of Schema Canon v1.0
3. ⏭️ **Commit Artifacts:**
   - `docs/PHASE_5/04_SCHEMA_CANON/DDL/schema.sql`
   - `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
   - `validate_schema_ddl.sh`
   - `docs/PHASE_5/04_SCHEMA_CANON/tools/generate_schema_from_blueprint.py`

---

## Related Documents

- `CATEGORY_C_STEP1_BLUEPRINT.md` - Blueprint specification
- `CATEGORY_C_STEP2_CONSTRAINTS.md` - Constraint definitions
- `DDL/schema.sql` - Validated DDL file
- `NSW_SCHEMA_CANON_v1.0.md` - Canonical schema documentation

---

**Validation Performed By:** Automated validation script  
**Validation Date:** 2026-01-05  
**PostgreSQL Version:** 16-alpine  
**Docker Context:** desktop-linux  
**Gate Status:** ✅ **PASSED**

