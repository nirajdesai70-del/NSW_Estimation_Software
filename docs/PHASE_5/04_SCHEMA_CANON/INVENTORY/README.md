---
Status: WORKING
Version: 1.0
Owner: Phase 5 Senate
Date: 2026-01-27
Scope: Schema Inventory Directory
---

# Schema Inventory Directory

**Purpose:** Centralized location for schema table inventory files and validation artifacts

---

## Files in This Directory

### 1. Full Inventory (Detailed)
**File:** `NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv`

Complete column-level inventory with:
- All tables (35 total)
- All columns, data types, constraints
- All foreign keys with ON DELETE policies
- All CHECK constraints (G-01, G-02, G-06, G-07)
- Baseline indexes
- Detailed notes (legacy/transitional, append-only, etc.)

**Use Case:** Authoritative reference for schema design and DDL generation

---

### 2. Key-Only Inventory (Simplified)
**File:** `NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv`

Simplified table-level inventory with:
- One row per table
- Essential constraints and relationships only
- Quick reference format

**Use Case:** Fast Excel review, quick lookup, overview

---

### 3. Diff View
**File:** `NSW_INVENTORY_DIFF_VIEW_v1.0.csv`

Comparison between full and key-only inventories:
- Table-level coverage validation
- Field drift detection
- Status indicators (MATCH / MISSING / DRIFT)

**Use Case:** Validate consistency between full and key-only inventories

---

### 4. Coverage Report
**File:** `NSW_INVENTORY_COVERAGE_REPORT_v1.0.md`

Coverage analysis report:
- Coverage summary
- Diff analysis results
- Schema Canon readiness score
- Missing tables/constraints identification

**Use Case:** Quality assurance, completeness validation

---

## File Relationships

```
NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv (Full Detail)
                    ↓
                    ├─→ NSW_INVENTORY_DIFF_VIEW_v1.0.csv (Comparison)
                    │
NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv (Simplified)
                    ↓
                    └─→ NSW_INVENTORY_COVERAGE_REPORT_v1.0.md (Analysis)
```

---

## Usage

### For Schema Design
- Use **Full Inventory** for complete reference
- Use **Key-Only Inventory** for quick lookup

### For Validation
- Use **Diff View** to check consistency
- Use **Coverage Report** for quality assurance

### For DDL Generation
- Reference **Full Inventory** for all constraints and indexes
- Verify **Coverage Report** for completeness

---

## Maintenance

When updating inventories:

1. Update **Full Inventory** first (authoritative source)
2. Update **Key-Only Inventory** to match
3. Regenerate **Diff View** to validate consistency
4. Regenerate **Coverage Report** to update metrics

---

## Governance Stance (Category-C v1.0 Freeze)

**Canonical Source of Truth:**
- ✅ `../DDL/schema.sql` — Authoritative DDL
- ✅ `../NSW_SCHEMA_CANON_v1.0.md` — Authoritative documentation

**CSV Inventory Files Status:**
- CSV inventories are **generated artifacts** (optional, non-versioned)
- Full inventory CSV can be regenerated from DDL using `tools/generate_inventory_from_ddl.py`
- Key-only and diff-view CSVs are tracked for reference but not required for validation
- DDL + Schema Canon document serve as the definitive source of truth

**Rationale:**
- DDL is the executable canonical source
- Schema Canon document is the human-readable authority
- CSV files are derivable from DDL and can be regenerated on-demand
- This stance maintains clean version control while preserving auditability via DDL

---

## Related Documents

- **Step-1 Blueprint:** `../CATEGORY_C_STEP1_BLUEPRINT.md`
- **Step-2 Constraints:** `../CATEGORY_C_STEP2_CONSTRAINTS.md`
- **Step-3 ER Diagram Spec:** `../CATEGORY_C_STEP3_ER_DIAGRAM_SPEC.md`
- **Re-Verification:** `../CATEGORY_C_REVERIFICATION_COMPLETE.md`

---

**Last Updated:** 2026-01-06  
**Status:** WORKING — Governance stance documented (Option B: Generated outputs, DDL canonical)

