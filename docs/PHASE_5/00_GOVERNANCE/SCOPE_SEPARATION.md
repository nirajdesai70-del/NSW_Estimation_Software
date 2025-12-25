# Scope Separation - Phase 5 vs Legacy Data Project

**Purpose:** Clarify the governance split between Phase 5 (canonical definition) and legacy data migration work  
**Date:** 2025-12-18  
**Status:** FROZEN - Authoritative Decision

---

## 🎯 Executive Summary

This document records the critical decision that **Phase 5** and **Legacy Data Migration** are separate workstreams with distinct scopes, governance, and execution timelines.

**Key Principle:** NSW must be built on clean canonical definitions, not compromised by legacy data semantics.

---

## ✅ Phase 5 Scope (Analysis Only)

Phase 5 is **limited to canonical data definition and schema design only**.

### Phase 5 - Step 1: Freeze NSW Canonical Data Dictionary
**Status:** Mandatory part of Phase 5  
**When:** After v3.0 Master Plan execution completes (Phase 4 exit)

**What Happens:**
- Finalize terminology and semantics:
  - Category / Subcategory / Type / Attribute
  - L0 / L1 / L2 meaning
  - ProductType rules
  - Copy-never-link rules
- Define what each entity means (not how legacy stores it)
- Define ownership (which module owns which table)

**Outputs (documents only):**
- `NSW_DATA_DICTIONARY_v1.0.md` (FROZEN)
- Entity definitions + allowed relationships
- Field-level meaning (business semantics)
- Naming conventions + constraints

**🚫 No DB creation**  
**🚫 No code**  
**🚫 No migration**

---

### Phase 5 - Step 2: Define NSW Canonical Schema (Design Only)
**Status:** Mandatory part of Phase 5  
**When:** After Step 1 completes

**What Happens:**
- Translate the data dictionary into:
  - Final table list
  - Columns + constraints
  - PK/FK relationships
  - Cardinality
- Produce ERD + table inventory
- Tag everything as CONFIRMED (design-locked)

**Outputs (documents only):**
- `NSW_SCHEMA_CANON_v1.0.md`
- ER diagram (PNG / draw.io / PDF)
- Table inventory (Excel/CSV)

**🚫 No migrations**  
**🚫 No DB writes**  
**🚫 No execution**

📌 Phase-5 ends here.

---

## 🚫 What Phase 5 Explicitly Does NOT Include

The following are **explicitly excluded** from Phase 5:

- ❌ Legacy DB analysis
- ❌ Legacy data cleanup
- ❌ Data migration
- ❌ Staging DB
- ❌ Import scripts

This keeps Phase 5 pure, auditable, and reversible.

---

## 🔀 Separate Project (After Phase 5)

🧩 Legacy Data Validation & Migration Project

This is NOT part of Phase 5.

You were absolutely right to separate it.

This becomes a new, standalone project, for example:

Project: NSW – Legacy Data Validation & Migration

⸻

This separate project will cover Step 3 and Step 4

Step 3 — Legacy Data Discovery & Quality Assessment

(New Project – Analysis + Read-Only)

What happens:
	•	Extract legacy DB schema (tables, columns, keys)
	•	Measure data quality:
	•	duplicates
	•	orphan rows
	•	invalid enums
	•	semantic mismatches
	•	Build Legacy Truth Pack

Outputs:
	•	Legacy schema workbook
	•	Legacy ER snapshot
	•	Data quality report
	•	"Do Not Import" list

🚫 No writes to legacy
🚫 No NSW impact

⸻

Step 4 — Migration Mapping & Controlled Import (Optional)

(New Project – Optional Execution)

What happens:
	•	Decide what (if anything) to migrate:
	•	none
	•	only active quotations
	•	only selected masters
	•	Build mapping matrix:
	•	Legacy → NSW
	•	Transform rules
	•	Use staging DB (never direct import)

Outputs:
	•	Mapping matrix
	•	Migration scripts
	•	Validation queries
	•	Cutover / rollback plan

✅ Executed only if business requires it

---

## 🔐 Why this split is the right decision

Governance Benefits
	•	Phase 5 stays clean and defensible
	•	NSW schema is not polluted by legacy mistakes
	•	Migration risk is isolated and optional

Technical Benefits
	•	You build NSW as a product, not a patch
	•	UI + code can be fully redesigned
	•	Constraints and rules can finally be enforced

Business Benefits
	•	No cutover pressure
	•	Legacy remains as archive/reference
	•	Migration can be delayed, partial, or skipped entirely

---

## 📋 Current Project Status: `project/nish/`

The `project/nish/` directory contains work related to **Legacy Data Analysis** (Steps 3 & 4).

**Important:** This work is **separate** from Phase 5 and should be treated as:
- Read-only analysis track
- Independent of Phase 4 execution
- Optional future project preparation

**Current Contents:**
- `01_SEMANTICS/` - Entity definitions (overlaps with Phase 5 Step 1, but from legacy perspective)
- `02_LEGACY_SCHEMA/` - Legacy schema extraction (Step 3)
- `03_NSW_SCHEMA/` - NSW schema documentation (may inform Phase 5 Step 2)
- `04_MAPPING/` - Mapping matrices (Step 4)
- `05_MIGRATION_STRATEGY/` - Migration planning (Step 4)

**Decision:** This work can continue in parallel as analysis-only, but:
- ✅ Can inform Phase 5 Step 1 & 2 (as reference)
- ❌ Cannot influence Phase 5 scope or outputs
- ❌ Cannot execute migration before Phase 5 completes

**Note:** We are NOT changing anything in `project/nish/` as part of this scope separation decision. It remains as existing legacy analysis work.

---

## 📋 Decision Context

**Business Constraints:**
- No business cutover pressure
- No need for full historical continuity
- Willingness to redesign UI
- Clear quality issues in legacy category/subcategory/type/attribute definitions
- Terminology and item creation in old software (v2) has many gaps

**Strategic Choice:**
- **Option B** chosen: New canonical DB + new code, legacy only as source
- Legacy/V2 DB = read-only archive + optional future import source
- Data validation/correction = separate project (runs in parallel, does not block NSW build)

**Migration Approach:**
- NSW DB = canonical truth
- Legacy/V2 DB = read-only archive
- Can ship NSW fast with clean masters
- Later decide what to import (if anything) from legacy after cleanup

---

## ✅ Final Confirmation

| Question | Answer |
|----------|--------|
| Are Step 1 & 2 part of Phase 5? | ✅ Yes |
| Are Step 3 & 4 part of Phase 5? | ❌ No |
| Should migration be a separate project? | ✅ Yes |
| Can NSW go live without legacy import? | ✅ Yes |
| Does Phase 5 start after v3.0 execution? | ✅ Yes |
| Is `project/nish/` separate from Phase 5? | ✅ Yes |
| Are we changing anything in `project/nish/`? | ❌ No (it remains as existing analysis work) |

---

## 📝 Governance Statement for v3.0 Master Plan

Add this paragraph under Phase 5 Scope Fence:

> **Migration Note:** Legacy data validation and migration are explicitly out of scope for Phase 5. They will be handled as a separate governed project after the NSW canonical data dictionary and schema are frozen. NSW can operate independently without legacy data import.

---

**Document Status:** FROZEN - Authoritative Decision  
**Last Updated:** 2025-12-18  
**Owner:** Architecture & Governance Team  
**Location:** `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md` (Phase 5 governance document)

