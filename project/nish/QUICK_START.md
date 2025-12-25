# DATA-MAP-TRACK Quick Start Guide

**Purpose:** Get started with the data migration analysis track  
**Date:** 2025-12-18

---

## 🎯 What Is This?

This is a **read-only analysis track** to analyze data migration from legacy system (`/Users/nirajdesai/Projects/nish/`) to NSW. It's **standalone** and **independent** of Phase-4 execution.

**Key Rule:** No code changes, no database writes, no schema changes. Documents and analysis only.

---

## 📁 Folder Structure

```
project/nish/
├── README.md                    # Overview and governance
├── QUICK_START.md               # This file
├── 01_SEMANTICS/
│   └── DATA_SEMANTICS_LOCK.md   # Entity definitions (prevent semantic drift)
├── 02_LEGACY_SCHEMA/
│   └── LEGACY_SCHEMA_EXTRACTION_PLAN.md  # How to extract legacy schema
├── 03_NSW_SCHEMA/
│   └── NSW_SCHEMA_CANON.md      # NSW target schema documentation
├── 04_MAPPING/
│   └── MAPPING_MATRIX_TEMPLATE.md  # Legacy → NSW mapping template
└── 05_MIGRATION_STRATEGY/
    └── MIGRATION_STRATEGY.md     # Migration ordering and cutover plan
```

---

## 🚀 Getting Started

### Step 1: Read the Semantics Lock (30 min)

**File:** `01_SEMANTICS/DATA_SEMANTICS_LOCK.md`

**Why:** Before mapping any field, you must understand what each entity means. This prevents "semantic drift" where same field names have different meanings.

**Key Questions Answered:**
- What is a Product? (L0/L1/L2)
- What is a Master BOM vs Proposal BOM?
- What is a Panel vs Feeder vs BOM?
- What is the hierarchy structure?

**Action:** Review and confirm entity definitions match your understanding.

---

### Step 2: Extract Legacy Schema (4-6 hours)

**File:** `02_LEGACY_SCHEMA/LEGACY_SCHEMA_EXTRACTION_PLAN.md`

**Source:** `/Users/nirajdesai/Projects/nish/` (old legacy codebase + SQL data)

**What to Extract:**
1. Table list with row counts
2. Column definitions (types, nullability, defaults)
3. Foreign keys and relationships
4. Indexes
5. Sample data (anonymized)

**Output:**
- Excel: `LEGACY_SCHEMA_INVENTORY.xlsx`
- JSON: `LEGACY_SCHEMA.json`
- Markdown: `LEGACY_SCHEMA_REPORT.md`

**Action:** Follow the extraction plan, generate Deliverable A.

---

### Step 3: Extract NSW Schema (6-8 hours)

**File:** `03_NSW_SCHEMA/NSW_SCHEMA_CANON.md`

**Source:** Current repo migrations/models (from `source_snapshot/database/migrations/` or actual codebase)

**What to Extract:**
1. Table list from migrations
2. Column definitions with **meaning** (not just name)
3. Relationships with business meaning
4. Enumerations and lookup references
5. Module ownership (CIM / MBOM / PBOM / FEED / PANEL / QUO)

**Output:**
- Excel: `NSW_SCHEMA_DICTIONARY.xlsx`
- Markdown: `NSW_SCHEMA_CANON.md` (populated)

**Action:** Follow the extraction plan, generate Deliverable B.

---

### Step 4: Build Mapping Matrix (8-12 hours)

**File:** `04_MAPPING/MAPPING_MATRIX_TEMPLATE.md`

**What to Map:**
- Every legacy column → NSW target table.column
- Transform rules (PRESERVE, RENAME, CONVERT, NORMALIZE, DERIVE, SPLIT, JOIN, MAP, DEFAULT, SKIP)
- Key mapping rules (preserve old IDs? remap?)
- Data quality checks
- Migration priority (P0/P1/P2/P3)
- Risk flags (LOW/MEDIUM/HIGH/CRITICAL)

**Output:**
- Excel: `LEGACY_TO_NSW_MAPPING.xlsx`
- Markdown: Mapping documentation

**Action:** Use template, populate mapping matrix, generate Deliverable C.

---

### Step 5: Create Migration Strategy (4-6 hours)

**File:** `05_MIGRATION_STRATEGY/MIGRATION_STRATEGY.md`

**What to Define:**
- Migration mode (Transform & Load recommended)
- Migration ordering (masters → relationships → BOM → quotations)
- Validation gates (row counts, referential integrity, business totals)
- Rollback strategy

**Output:**
- Markdown: `MIGRATION_STRATEGY.md` (populated)
- Migration scripts (draft, not executed)

**Action:** Review strategy, create detailed migration plan, generate Deliverable D.

---

## 📊 Deliverables Summary

| Deliverable | File | Status | Estimated Time |
|------------|------|--------|----------------|
| A: Legacy Schema | `02_LEGACY_SCHEMA/LEGACY_SCHEMA_REPORT.md` | ⏳ Pending | 4-6 hours |
| B: NSW Schema | `03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` | ⏳ Pending | 6-8 hours |
| C: Mapping Matrix | `04_MAPPING/LEGACY_TO_NSW_MAPPING.xlsx` | ⏳ Pending | 8-12 hours |
| D: Migration Strategy | `05_MIGRATION_STRATEGY/MIGRATION_STRATEGY.md` | ⏳ Pending | 4-6 hours |

**Total Estimated Time:** 22-32 hours

---

## ⚠️ Critical Rules

1. **READ-ONLY:** No changes to code, database, or migrations
2. **STANDALONE:** Independent of Phase-4 execution
3. **ANALYSIS ONLY:** Documents and mapping tables only
4. **NO EXECUTION:** Migration scripts are drafts, not executed
5. **EVIDENCE-BASED:** All findings must be backed by schema exports or migration files

---

## 🎯 Success Criteria

**This track is successful when:**
- ✅ All 4 deliverables are complete
- ✅ Mapping matrix identifies all gaps and risks
- ✅ Migration strategy is actionable
- ✅ Decision can be made: include in master execution plan or not

---

## 📝 Next Actions

1. **Start with Semantics Lock:** Review `01_SEMANTICS/DATA_SEMANTICS_LOCK.md`
2. **Extract Legacy Schema:** Follow `02_LEGACY_SCHEMA/LEGACY_SCHEMA_EXTRACTION_PLAN.md`
3. **Extract NSW Schema:** Follow `03_NSW_SCHEMA/NSW_SCHEMA_CANON.md`
4. **Build Mapping:** Use `04_MAPPING/MAPPING_MATRIX_TEMPLATE.md`
5. **Create Strategy:** Review `05_MIGRATION_STRATEGY/MIGRATION_STRATEGY.md`

---

## 🔗 Related Documents

- **Main README:** `README.md` (overview and governance)
- **Phase-5 Context:** `docs/PHASE_5/` (related Phase-5 work)
- **Risk Register:** `docs/PHASE_4/RISK_REGISTER.md` (DATA-INTEGRITY-001)

---

**Last Updated:** 2025-12-18  
**Status:** Ready to Execute

