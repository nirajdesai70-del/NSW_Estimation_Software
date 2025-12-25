# DATA-MAP-TRACK - Legacy to NSW Data Migration Analysis

**Status:** READ-ONLY Analysis Track (Separate from Phase 5)  
**Purpose:** Legacy data discovery, mapping, and migration planning  
**Governance:** Standalone project, independent of Phase 4 execution and Phase 5 scope  
**Date Created:** 2025-12-18  
**Last Updated:** 2025-12-18

---

## ⚠️ IMPORTANT: Scope Separation

**This project is SEPARATE from Phase 5.**

**Phase 5 Scope:** Only canonical data dictionary and schema design (Steps 1 & 2)

**This Project Scope:** Legacy data discovery and migration planning (Steps 3 & 4)

**See:** `docs/PHASE_5/SCOPE_SEPARATION.md` for detailed explanation of the split.

**Note:** We are NOT changing anything in this `project/nish/` directory as part of the scope separation decision. It remains as existing legacy analysis work.

---

## 🎯 Purpose

This track is a **read-only analysis exercise** for legacy data work:

1. Extract and document legacy database schema from `/Users/nirajdesai/Projects/nish/` (old legacy codebase + SQL data)
2. Assess legacy data quality
3. Create mapping matrix (Legacy → NSW)
4. Identify gaps and migration risks
5. Produce migration strategy and cutover plan

**Critical Rule:** This is **analysis only**. No schema changes, no data writes, no code changes. Output is documents + mapping tables + migration scripts draft (not executed).

**Execution Status:** This work can proceed in parallel as analysis-only, but migration execution requires separate project approval and can only proceed after Phase 5 completes.

---

## 📁 Folder Structure

```
project/nish/
├── README.md (this file)
├── 01_SEMANTICS/
│   └── DATA_SEMANTICS_LOCK.md
├── 02_LEGACY_SCHEMA/
│   ├── LEGACY_SCHEMA_EXTRACTION_PLAN.md
│   ├── LEGACY_SCHEMA_REPORT.md (to be generated)
│   └── exports/ (SQL dumps, Excel exports)
├── 03_NSW_SCHEMA/
│   ├── NSW_SCHEMA_CANON.md (to be generated)
│   ├── NSW_SCHEMA_DICTIONARY.md (to be generated)
│   └── exports/ (migration analysis, Excel exports)
├── 04_MAPPING/
│   ├── MAPPING_MATRIX_TEMPLATE.md
│   ├── LEGACY_TO_NSW_MAPPING.md (to be generated)
│   └── exports/ (Excel mapping matrix)
└── 05_MIGRATION_STRATEGY/
    ├── MIGRATION_STRATEGY.md
    ├── MIGRATION_ORDERING.md (to be generated)
    └── VALIDATION_GATES.md (to be generated)
```

---

## 📋 Deliverables

### Deliverable A — Legacy DB Truth Pack
- **Status:** ⏳ Pending
- **Location:** `02_LEGACY_SCHEMA/`
- **Contents:**
  - Table list with row counts
  - Column definitions (types, nullability, defaults)
  - Keys (PK/FK/unique)
  - Indexes
  - Lookup/master tables
  - Sample data snapshots (anonymized)
- **Output Format:** Excel + JSON + `LEGACY_SCHEMA_REPORT.md`

### Deliverable B — NSW Target Canonical Data Dictionary
- **Status:** ⏳ Pending
- **Location:** `03_NSW_SCHEMA/`
- **Contents:**
  - Final table list (from migrations)
  - Column definitions (meaning, not just name)
  - PK/FK relationships
  - Enumerations/lookup references
  - Owner module (CIM / MBOM / PBOM / FEED / PANEL / QUO)
- **Output Format:** Excel + `NSW_SCHEMA_CANON.md`

### Deliverable C — Mapping Matrix (Legacy → NSW)
- **Status:** ⏳ Pending
- **Location:** `04_MAPPING/`
- **Contents:**
  - For every legacy column: target table.column in NSW
  - Transform rules (rename / convert / normalize / derive / split / join)
  - Key mapping rules (old IDs preserved? remapped? composite?)
  - Data quality checks
  - Migration priority (P0/P1/P2)
  - Risk flags
- **Output Format:** Excel `LEGACY_TO_NSW_MAPPING.xlsx` + markdown

### Deliverable D — Migration Strategy + Cutover Plan
- **Status:** ⏳ Pending
- **Location:** `05_MIGRATION_STRATEGY/`
- **Contents:**
  - Migration modes (lift & shift / transform & load / hybrid)
  - Order of migration (masters → relationships → BOM → quotations)
  - Rollback strategy
  - Validation gates (row counts, referential integrity, business totals)
- **Output Format:** `MIGRATION_STRATEGY.md`

---

## 🔒 Governance Rules

1. **READ-ONLY:** No changes to code, database, or migrations
2. **STANDALONE:** Independent of Phase-4 execution and Phase 5 scope
3. **ANALYSIS ONLY:** Documents and mapping tables only
4. **NO EXECUTION:** Migration scripts are drafts, not executed
5. **EVIDENCE-BASED:** All findings must be backed by schema exports or migration files
6. **SEPARATE PROJECT:** This is NOT part of Phase 5 (see `docs/PHASE_5/SCOPE_SEPARATION.md`)
7. **OPTIONAL EXECUTION:** Migration execution requires separate project approval and Phase 5 completion

---

## 📊 Current Status

| Deliverable | Status | Progress |
|------------|--------|----------|
| A: Legacy Schema Extraction | ⏳ Not Started | 0% |
| B: NSW Schema Canon | ⏳ Not Started | 0% |
| C: Mapping Matrix | ⏳ Not Started | 0% |
| D: Migration Strategy | ⏳ Not Started | 0% |

---

## 🚀 Next Steps

1. ✅ Create folder structure (DONE)
2. ⏳ Define data semantics lock (`01_SEMANTICS/DATA_SEMANTICS_LOCK.md`)
3. ⏳ Extract legacy schema from `/Users/nirajdesai/Projects/nish/` database/SQL files
4. ⏳ Extract NSW schema from migrations/models
5. ⏳ Build mapping matrix
6. ⏳ Create migration strategy

---

## 📝 Notes

- **Legacy Source:** `/Users/nirajdesai/Projects/nish/` (old legacy codebase + SQL data, v2 version mostly same SQL)
- **NSW Source:** Will reference Phase 5 outputs (NSW canonical schema) when available
- **Project Status:** Analysis can proceed in parallel, but execution is separate and optional
- **Decision Point:** After Phase 5 completes, decide if legacy migration project proceeds

---

## 🔗 Related Documents

- **Scope Separation:** `docs/PHASE_5/SCOPE_SEPARATION.md` (critical read)
- **Phase 5 Scope:** `docs/PHASE_5/PHASE_5_SCOPE_FENCE.md`
- **Phase 5 Execution Summary:** `docs/PHASE_5/PHASE_5_EXECUTION_SUMMARY.md`

---

**Last Updated:** 2025-12-18  
**Owner:** Legacy Data Migration Analysis Team  
**Review Status:** Initial Setup Complete - Scope Clarified

