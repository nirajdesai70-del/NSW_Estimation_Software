# Phase-6 Week-0 Detailed Plan

**Week:** Week-0 (Entry Gate & Setup)  
**Status:** ✅ STRUCTURALLY COMPLETE (Governance Pack Created)  
**Closure Status:** ⏳ Pending explicit sign-off  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-0 establishes the foundation for Phase-6 execution. All governance artifacts have been consolidated into a single canonical governance pack to prevent fragmentation. This document provides the detailed breakdown of all Week-0 tasks, aligned with the Phase-6 Document Review Matrix.

**Key Deliverables:**
- Entry Gate verification and documentation
- Project structure setup
- Task register establishment
- Costing contract freeze (QCD v1.0)
- Database schema foundation
- Module boundaries and governance rules

**Critical Alarms (From Matrix):**
- 🔴 **3 Compliance Alarms** (must resolve before Phase-6 closure)
  - ALARM-SETUP-DOCS (3 tasks: task register, QCD contract, D0 Gate checklist)
  - ALARM-ENTRY-006 (naming conventions)
  - ALARM-DB-005 (cost template seed spec)
- 🟠 **5 High Priority Alarms** (should resolve)
- 🟡 **2 Medium Priority Items** (partial evidence, needs documentation)
- 🔵 **1 Consolidated Alarm** (ALARM-NAMING-MODULE-RULES - may become compliance)

---

## Week-0 Task Breakdown

### Track: Entry Gate & Setup (Track E + Setup)

#### Entry Criteria Verification

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-ENTRY-001 | Verify SPEC-5 v1.0 frozen | Entry gate documentation | ⚠️ PARTIAL | 🟡 | Entry gate stated passed; repo proof doc needed |
| P6-ENTRY-002 | Verify Schema Canon locked | Schema Canon verification record | ⚠️ PARTIAL | 🟡 | Schema Canon referenced; verification record needed |
| P6-ENTRY-003 | Verify Decision Register closed | Decision register closure record | ⚠️ PARTIAL | 🟡 | Decision register referenced; closure record needed |
| P6-ENTRY-004 | Verify Freeze Gate Checklist 100% verified | Freeze gate checklist verification | ⚠️ PARTIAL | 🟡 | Freeze gate referenced; checklist verification needed |
| P6-ENTRY-005 | Verify Core resolution engine tested | Core engine test verification | ⚠️ PARTIAL | 🟡 | Core engine referenced; test verification needed |
| P6-ENTRY-006 | Naming conventions compliance check | Naming convention compliance document | ❌ MISSING | 🔴 **COMPLIANCE** | Required for all new migrations/models/routes |

**Entry Gate Status:** ⚠️ PARTIAL (All entry criteria referenced but formal documentation needed)

---

#### Setup Tasks

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-SETUP-001 | Create Phase-6 project structure | `docs/PHASE_6/` directory structure | ⚠️ PARTIAL | 🟡 | docs path in .cursorignore; evidence pack exists elsewhere |
| P6-SETUP-002 | Review Phase-5 deliverables | Phase-5 review document | ❌ MISSING | 🟠 | Review Schema Canon, API contracts, resolution engine docs |
| P6-SETUP-003 | Create Phase-6 task register | Task tracking system/register | ❌ MISSING | 🔴 **COMPLIANCE** | Single source of truth for all Phase-6 tasks |
| P6-SETUP-004 | Create Costing manual structure | `docs/PHASE_6/COSTING/MANUAL/` directory | ❌ MISSING | 🟠 | Directory structure for costing documentation |
| P6-SETUP-005 | Freeze Costing Engine Contract (QCD v1.0) | `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md` | ❌ MISSING | 🔴 **COMPLIANCE** | Must freeze QCD contract before costing work |
| P6-SETUP-006 | Define D0 Gate checklist | `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md` | ❌ MISSING | 🔴 **COMPLIANCE** | D0 Gate definition required (checklist only, not passed yet) |
| P6-SETUP-007 | Review Phase-5 deliverables for implementation obligations | Implementation obligations document | ❌ MISSING | 🟠 | Review Category A/B/C/D for Phase-6 obligations |
| P6-SETUP-008 | Create module folder boundaries + PR rules | Module structure + PR governance | ❌ MISSING | 🟠 | Module ownership boundaries per Phase-5 Module Ownership Matrix |

**Setup Tasks Status:** ❌ INCOMPLETE (8 tasks, 7 missing, 1 partial)

---

#### Database Tasks (Track E - Week 0-1)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-DB-001 | Choose DB creation approach (DDL vs migrations) | `docs/PHASE_6/DB/DB_CREATION_METHOD.md` | ❌ MISSING | 🟠 | Lock method for Canon v1.0 |
| P6-DB-002 | Implement DB schema from Schema Canon v1.0 | Schema migration files | ✅ DONE | — | Schema drift checks exist and pass |
| P6-DB-003 | Execute seed script (C5) on dev/stage | Seed script execution record | ✅ DONE | — | Included in schema implementation |
| P6-DB-004 | Schema parity gate (DB == Canon v1.0) | `docs/PHASE_6/DB/SCHEMA_PARITY_REPORT.md` | ✅ DONE | — | Schema drift check validates parity |
| P6-DB-005 | Seed cost template master data | Cost template seed data specification | ❌ MISSING | 🔴 **COMPLIANCE** | Spec-only (no DB mutation), defines what must be seeded later |

**Database Tasks Status:** ⚠️ PARTIAL (5 tasks, 3 done, 2 missing)

---

## Week-0 Governance Pack Status

Based on the canvas document mentioned, the following governance artifacts should be consolidated:

### ✅ Structurally Complete (Governance Pack)

1. **Phase-6 Entry Gate Record** ✅
   - Phase-5 freeze references locked
   - Entry gate formally documented
   - **Alarm:** P6-ENTRY-001..005 need formal documentation records

2. **Naming Conventions & Module Ownership** ✅
   - Canon-aligned naming rules
   - Module boundaries + PR governance rules
   - **Alarm:** P6-ENTRY-006 (naming compliance check) status unknown
   - **Alarm:** P6-SETUP-008 (module boundaries) status unknown

3. **Phase-6 Task Register (Authority Layer)** ✅
   - Declared as single source of truth
   - Blocks undocumented work
   - **Alarm:** P6-SETUP-003 (task register) needs verification

4. **QCD Contract v1.0 (Frozen)** ✅
   - Meaning locked (engine-first, BOM-only)
   - Prevents future costing drift
   - **Alarm:** P6-SETUP-005 (QCD contract) needs verification

5. **D0 Gate Definition (Checklist Only)** ✅
   - Defined but not passed (correct Week-0 behavior)
   - **Alarm:** P6-SETUP-006 (D0 Gate checklist) needs verification

6. **Cost Template Seed Definition (Spec-only)** ✅
   - What must be seeded later, without DB mutation now
   - **Alarm:** P6-DB-005 (cost template seed spec) needs verification

7. **Week-0 Closure Criteria** ✅
   - Explicit checklist to avoid re-opening Week-0 later

---

## Alarm Summary for Week-0

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-SETUP-DOCS** | Review 1 (Finalized Review 4) | P6-SETUP-003, P6-SETUP-005, P6-SETUP-006 | Entry-gate setup docs missing (task register, QCD contract, D0 checklist) | ❌ MISSING | Verify/create all three governance documents |
| **ALARM-ENTRY-006** | Review 1 | P6-ENTRY-006 | Naming convention compliance check | ❌ MISSING | Create compliance document verifying all new code follows Phase-5 naming conventions |
| **ALARM-DB-005** | Review 1 | P6-DB-005 | Cost template seed data specification | ❌ MISSING | Verify cost template seed spec exists (spec-only, no DB mutation) |

**Alarm Details:**

#### ALARM-SETUP-DOCS (Compliance - Blocks Governance)
- **Tasks Affected:** P6-SETUP-003, P6-SETUP-005, P6-SETUP-006
- **Impact:** Blocks governance compliance, prevents Phase-6 sign-off
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-SETUP-003: Verify/create Phase-6 task register (single source of truth)
  - P6-SETUP-005: Verify QCD contract exists: `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
  - P6-SETUP-006: Verify D0 Gate checklist exists: `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`
- **Notes:** This is the consolidated alarm covering all three setup documents. All three must be resolved.

#### ALARM-ENTRY-006 (Compliance - Naming Conventions)
- **Task Affected:** P6-ENTRY-006
- **Impact:** Required for all new migrations/models/routes. Compliance-critical for governance.
- **Matrix Status:** Marked as 🔴 MISSING in matrix, compliance-critical
- **Resolution:** Create naming convention compliance document verifying:
  - Table naming: snake_case, plural
  - Column naming: snake_case, singular
  - FK naming: {table_singular}_id
  - Enum naming: UPPER_SNAKE_CASE
- **Notes:** Part of ALARM-NAMING-MODULE-RULES (may be compliance-critical depending on governance)

#### ALARM-DB-005 (Compliance - Cost Template Seed)
- **Task Affected:** P6-DB-005
- **Impact:** Required for cost adders implementation. Spec-only (no DB mutation in Week-0).
- **Matrix Status:** Marked as 🔴 MISSING (compliance requirement)
- **Resolution:** Verify cost template seed specification exists: `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`
- **Notes:** Spec-only definition (no DB mutation), defines what must be seeded later

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-SETUP-002 | P6-SETUP-002 | Review Phase-5 deliverables | ❌ MISSING | Create Phase-5 review document (Schema Canon, API contracts, resolution engine) |
| ALARM-SETUP-004 | P6-SETUP-004 | Costing manual structure | ❌ MISSING | Create directory structure: `docs/PHASE_6/COSTING/MANUAL/` |
| ALARM-SETUP-007 | P6-SETUP-007 | Review Phase-5 for implementation obligations | ❌ MISSING | Create obligations document (Category A/B/C/D review) |
| ALARM-SETUP-008 | P6-SETUP-008 | Module boundaries + PR rules | ❌ MISSING | Verify/create module structure document (per Phase-5 Module Ownership Matrix) |
| ALARM-DB-001 | P6-DB-001 | DB creation method doc | ❌ MISSING | Create DB creation method document: `docs/PHASE_6/DB/DB_CREATION_METHOD.md` |

### 🟡 Medium Priority (Partial Evidence - Needs Documentation)

These items have partial evidence but need formal documentation.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| P6-ENTRY-001..005 | Entry gate checks (SPEC-5, Schema Canon, Decision Register, Freeze Gate, Core Engine) | ⚠️ PARTIAL | Create formal documentation records for each entry criterion verification |
| P6-SETUP-001 | Phase-6 project structure | ⚠️ PARTIAL | Verify structure matches plan (docs path in .cursorignore; evidence pack exists elsewhere) |
| P6-DB-002..004 | DB schema + seeds + schema parity gate | ✅ DONE | No action needed - schema drift checks exist and pass |

### 🔵 Consolidated Alarm (From Matrix - High Priority)

**ALARM-NAMING-MODULE-RULES** (May Become Compliance)
- **Tasks Affected:** P6-ENTRY-006, P6-SETUP-004, P6-SETUP-008
- **Status:** 🟠 (becomes 🔴 if governance requires)
- **Impact:** Naming convention + module boundaries - May be compliance-critical depending on governance
- **Matrix Status:** Review 1 - High Priority (may become compliance-critical depending on governance)
- **Resolution:** 
  - P6-ENTRY-006: Create naming convention compliance document (covered in ALARM-ENTRY-006 above)
  - P6-SETUP-004: Create costing manual structure (covered in ALARM-SETUP-004 above)
  - P6-SETUP-008: Verify/create module boundaries document (covered in ALARM-SETUP-008 above)
- **Notes:** This is a consolidated alarm covering naming and module rules. May upgrade to compliance if governance requires.

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-0 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-ENTRY-001..005 (Entry gate checks)
- ✅ P6-ENTRY-006 (Naming conventions)
- ✅ P6-SETUP-001..008 (All setup tasks)
- ✅ P6-DB-001..005 (All database tasks)

### ⚠️ Items Requiring Verification

The canvas governance pack is mentioned but needs verification that it contains:

1. **Entry Gate Documentation (P6-ENTRY-001..005)**
   - Need to verify formal records exist
   - Current status: ⚠️ PARTIAL (referenced but not documented)

2. **Task Register (P6-SETUP-003)**
   - Mentioned as "single source of truth"
   - Need to verify it exists and is accessible
   - Current status: ❌ MISSING (needs verification)

3. **QCD Contract (P6-SETUP-005)**
   - Mentioned as "frozen"
   - Need to verify file exists: `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
   - Current status: ❌ MISSING (needs verification)

4. **D0 Gate Checklist (P6-SETUP-006)**
   - Mentioned as "defined but not passed"
   - Need to verify file exists: `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`
   - Current status: ❌ MISSING (needs verification)

5. **Naming Conventions (P6-ENTRY-006)**
   - Mentioned as part of governance pack
   - Need to verify compliance document exists
   - Current status: ❌ MISSING (needs verification)

6. **Module Boundaries (P6-SETUP-008)**
   - Mentioned as part of governance pack
   - Need to verify module structure document exists
   - Current status: ❌ MISSING (needs verification)

---

## Week-0 Closure Criteria

### Required for Closure

1. ✅ **Governance Pack Created** (Structural completion)
2. ⏳ **All Governance Documents Verified** (Need to verify files exist)
3. ⏳ **All Compliance Alarms Resolved** (5 compliance alarms)
4. ⏳ **Entry Gate Documentation Complete** (Formal records needed)
5. ⏳ **Task Register Accessible** (Single source of truth verified)
6. ⏳ **QCD Contract Verified** (File exists and is frozen)
7. ⏳ **D0 Gate Checklist Verified** (File exists)
8. ⏳ **Naming Conventions Document Verified** (Compliance doc exists)
9. ⏳ **Module Boundaries Document Verified** (Structure doc exists)

### Current Closure Status

- **Structural Completion:** ✅ DONE (Governance pack created)
- **Document Verification:** ⏳ PENDING (Need to verify all files exist)
- **Compliance Alarms:** ❌ 5 alarms need resolution
- **Formal Sign-off:** ⏳ PENDING

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Resolve Compliance Alarms (Blocking)

1. **ALARM-SETUP-DOCS Resolution**
   - Verify/create Phase-6 task register (P6-SETUP-003)
   - Verify QCD contract exists: `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md` (P6-SETUP-005)
   - Verify D0 Gate checklist exists: `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md` (P6-SETUP-006)

2. **ALARM-ENTRY-006 Resolution**
   - Create naming convention compliance document
   - Verify all new code follows Phase-5 naming conventions (table, column, FK, enum naming rules)

3. **ALARM-DB-005 Resolution**
   - Verify cost template seed specification exists: `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`
   - Confirm it's spec-only (no DB mutation in Week-0)

#### Priority 2: Verify Governance Pack Contents

4. **Governance Pack Verification**
   - Confirm all mentioned documents actually exist
   - Provide file paths/locations for verification
   - Update evidence status based on verification
   - Verify: Entry Gate Record, Naming Conventions, Task Register, QCD Contract, D0 Gate Checklist, Cost Template Seed Spec, Module Boundaries

#### Priority 3: Complete Documentation

5. **Entry Gate Documentation (P6-ENTRY-001..005)**
   - Create formal records for each entry criterion:
     - P6-ENTRY-001: SPEC-5 v1.0 frozen verification
     - P6-ENTRY-002: Schema Canon locked verification
     - P6-ENTRY-003: Decision Register closed verification
     - P6-ENTRY-004: Freeze Gate Checklist 100% verified
     - P6-ENTRY-005: Core resolution engine tested verification

6. **High Priority Tasks**
   - P6-SETUP-002: Create Phase-5 review document
   - P6-SETUP-004: Create costing manual structure
   - P6-SETUP-007: Create implementation obligations document
   - P6-SETUP-008: Verify/create module boundaries document
   - P6-DB-001: Create DB creation method document

7. **Document Status Updates**
   - Verify all governance pack documents are accessible
   - Update task statuses based on actual evidence
   - Mark tasks as ✅ DONE when evidence is verified

### Decision Point

**Week-0 Closure Status:**
- ⏳ **PENDING EXPLICIT SIGN-OFF**

**Options:**
1. **"Close Week-0 and start Week-1 detailed plan"** - If governance pack verification passes
2. **"Revise Week-0 governance pack before closure"** - If documents need creation/verification

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-0 tasks)
- **Week-0 Governance Pack:** (Location needs verification - mentioned in canvas document)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 19 | All captured from matrix |
| **Compliance Alarms** | 3 (5 tasks) | 🔴 Must resolve |
| **High Priority Alarms** | 5 | 🟠 Should resolve |
| **Medium Priority Items** | 2 | 🟡 Needs documentation |
| **Completed Tasks** | 3 | ✅ DONE (P6-DB-002..004) |
| **Partial Tasks** | 2 | ⚠️ PARTIAL (P6-ENTRY-001..005, P6-SETUP-001) |
| **Missing Tasks** | 14 | ❌ MISSING (need verification/creation) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-SETUP-DOCS:** Verify/create task register, QCD contract, D0 Gate checklist
- [ ] **ALARM-ENTRY-006:** Create naming convention compliance document
- [ ] **ALARM-DB-005:** Verify cost template seed specification exists

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-SETUP-002:** Create Phase-5 review document
- [ ] **ALARM-SETUP-004:** Create costing manual structure
- [ ] **ALARM-SETUP-007:** Create implementation obligations document
- [ ] **ALARM-SETUP-008:** Verify/create module boundaries document
- [ ] **ALARM-DB-001:** Create DB creation method document

### Documentation Tasks

- [ ] Create formal entry gate documentation records (P6-ENTRY-001..005)
- [ ] Verify Phase-6 project structure matches plan (P6-SETUP-001)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After governance pack verification and alarm resolution
