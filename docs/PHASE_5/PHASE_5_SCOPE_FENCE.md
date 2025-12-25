# Phase 5 - Scope Fence & Execution Plan

**Version:** 2.0 (Updated with Scope Separation)  
**Date:** 2025-12-18  
**Status:** FROZEN - Authoritative Scope Definition

---

## 🎯 Phase 5 Purpose

Phase 5 is **analysis-only** work that freezes the canonical data definitions and schema design for NSW.

**Critical Rule:** Phase 5 is limited to canonical data definition and schema design only. Legacy data validation and migration are explicitly out of scope and will be handled as a separate governed project if required.

---

## ✅ Phase 5 Scope (Authoritative)

### Prerequisites (Must Be Complete)

Phase 5 starts **only after**:
- ✅ v3.0 Master Plan execution is complete
- ✅ Phase 4 exit criteria are satisfied
- ✅ G5 Regression Gate passed
- ✅ NSW system is functionally complete and stable

---

### Phase 5 - Step 1: Freeze NSW Canonical Data Dictionary

**Status:** ✅ Mandatory part of Phase 5  
**Type:** Analysis & Definition Only

**Objectives:**
1. Finalize terminology and semantics:
   - Category / Subcategory / Type / Attribute
   - L0 / L1 / L2 meaning
   - ProductType rules
   - Copy-never-link rules
2. Define what each entity means (business semantics, not legacy structure)
3. Define ownership (which module owns which table)
4. Establish naming conventions
5. Define constraints and business rules

**Deliverables:**
- `NSW_DATA_DICTIONARY_v1.0.md` (FROZEN)
  - Entity definitions
  - Allowed relationships
  - Field-level meaning (business semantics)
  - Naming conventions
  - Constraints and rules

**Activities:**
- Document entity definitions
- Lock semantic meanings
- Define module ownership
- Establish naming standards
- Document business rules
- **Reference:** `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` - Consider all pending upgrade requirements during entity definition (BOM tracking, CostHead, AI entities, validation rules, etc.)

**🚫 Forbidden:**
- ❌ Database creation
- ❌ Code implementation
- ❌ Data migration
- ❌ Legacy DB access (except read-only reference)

---

### Phase 5 - Step 2: Define NSW Canonical Schema (Design Only)

**Status:** ✅ Mandatory part of Phase 5  
**Type:** Design & Documentation Only  
**Prerequisite:** Step 1 must be complete and approved

**Objectives:**
1. Translate data dictionary into concrete schema:
   - Final table list
   - Column definitions
   - Constraints (PK/FK/Unique/Check)
   - Relationships and cardinality
2. Produce design artifacts:
   - ER diagram
   - Table inventory
   - Relationship map
3. Tag everything as CONFIRMED (design-locked)

**Deliverables:**
- `NSW_SCHEMA_CANON_v1.0.md`
  - Complete table list
  - Column definitions with business meaning
  - PK/FK relationships
  - Constraints documentation
  - Module ownership mapping
- ER Diagram (PNG / draw.io / PDF)
- Table Inventory (Excel/CSV format)

**Activities:**
- Design table structure
- Define relationships
- Document constraints
- Create ER diagram
- Generate table inventory
- **Reference:** `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` - Include all fields and tables from pending upgrades (BOM tracking fields, CostHead tables, AI tables, IsLocked fields, audit tables, etc.)

**🚫 Forbidden:**
- ❌ Migration creation
- ❌ Database writes
- ❌ Runtime testing
- ❌ Code implementation
- ❌ Data import

---

## 🚫 Phase 5 Explicit Exclusions

The following are **explicitly excluded** from Phase 5:

### Legacy Data Work (Separate Project)
- ❌ Legacy DB schema extraction
- ❌ Legacy data quality assessment
- ❌ Legacy data cleanup
- ❌ Legacy → NSW mapping matrices
- ❌ Data migration scripts
- ❌ Staging database setup
- ❌ Import validation

**Note:** Legacy data work may proceed in parallel as analysis-only (see `project/nish/`), but:
- Cannot influence Phase 5 outputs
- Cannot execute migration before Phase 5 completes
- Is a separate governed project

### Implementation Work
- ❌ Migration file creation
- ❌ Database changes
- ❌ Code changes
- ❌ Runtime testing
- ❌ Performance testing

---

## 📊 Phase 5 Success Criteria

Phase 5 is complete when:

1. ✅ Data Dictionary v1.0 is frozen and approved
   - All entities defined
   - All relationships documented
   - All naming conventions locked
   - All business rules captured

2. ✅ Schema Canon v1.0 is frozen and approved
   - All tables designed
   - All relationships mapped
   - ER diagram complete
   - Table inventory complete

3. ✅ Design artifacts are approved by:
   - Architecture approval
   - Execution team approval
   - Release gate (if applicable)

4. ✅ Phase 5 closure documentation complete

---

## 🔀 Post-Phase 5: Legacy Data Migration (Separate Project)

After Phase 5 completes, if legacy data migration is required, it becomes a **separate governed project**:

**Project Name:** NSW – Legacy Data Validation & Migration

**Scope:**
- Legacy schema extraction
- Data quality assessment
- Mapping matrix creation
- Migration strategy
- Controlled import (optional)

**Prerequisites:**
- Phase 5 must be complete
- NSW canonical schema must be frozen
- Business decision on migration scope

**Governance:**
- Separate project charter
- Independent approval gates
- Optional execution (can be skipped if not needed)

---

## 📋 Execution Order Summary

```
1. Execute v3.0 Master Plan (Phase 4)
   └─> Complete S2 → S3 → S4 → S5
   └─> Pass G5 Regression Gate
   └─> Phase 4 Exit

2. Enter Phase 5 (Analysis Only)
   ├─> Step 1: Freeze NSW Data Dictionary
   │   └─> Output: NSW_DATA_DICTIONARY_v1.0.md (FROZEN)
   │
   └─> Step 2: Define NSW Canonical Schema
       └─> Output: NSW_SCHEMA_CANON_v1.0.md + ERD

3. Phase 5 Complete

4. (Optional) Legacy Data Migration Project
   ├─> Step 3: Legacy Discovery
   └─> Step 4: Migration Mapping & Import
```

---

## 🔗 Related Documents

- **Scope Separation:** `docs/PHASE_5/SCOPE_SEPARATION.md`
- **Legacy Analysis:** `project/nish/README.md`
- **v3.0 Master Plan:** (reference main plan document)
- **Phase 4 Exit Criteria:** (reference Phase 4 documentation)

---

**Document Status:** FROZEN - Authoritative Scope  
**Last Updated:** 2025-12-18  
**Owner:** Phase 5 Governance Team

