# PHASE-6 | WEEK-0 Task Scheduling & Decisions Report

**Date:** 2026-01-12  
**Run ID:** PHASE6_WEEK0_RUN_20260112_140401  
**Purpose:** Document when "not covered" tasks are planned and any decisions about them

---

## Executive Summary

**All "not covered" tasks are scheduled for Week-0** (same week as the runner script). However, they are **separate deliverables** that need to be completed **in parallel** or **sequentially** with the runner script execution.

**Key Decision:** The runner script (`run_week0_checks.sh`) is **read-only verification only**. All other Week-0 tasks require **documentation creation** or **implementation work**, which is why they are separate deliverables.

---

## Task Scheduling by Category

### Entry Gate Tasks (P6-ENTRY-002..006)

| Task ID | Description | When Planned | Priority | Decision/Status |
|---------|-------------|--------------|----------|-----------------|
| P6-ENTRY-002 | Verify Schema Canon locked | **Week-0** | 🟡 Medium | ⚠️ PARTIAL - Verification record needed |
| P6-ENTRY-003 | Verify Decision Register closed | **Week-0** | 🟡 Medium | ⚠️ PARTIAL - Closure record needed |
| P6-ENTRY-004 | Verify Freeze Gate Checklist 100% verified | **Week-0** | 🟡 Medium | ⚠️ PARTIAL - Checklist verification needed |
| P6-ENTRY-005 | Verify Core resolution engine tested | **Week-0** | 🟡 Medium | ⚠️ PARTIAL - Test verification needed |
| P6-ENTRY-006 | Naming conventions compliance check | **Week-0** | 🔴 **COMPLIANCE** | ❌ MISSING - Required for all new migrations/models/routes |

**Decision:**
- All are **Week-0 tasks** (same week as runner script)
- Status: ⚠️ PARTIAL (P6-ENTRY-002..005) or ❌ MISSING (P6-ENTRY-006)
- **Action Required:** Create formal documentation records for each
- **Blocking:** P6-ENTRY-006 is compliance-critical (blocks Phase-6 closure)

---

### Setup Tasks (P6-SETUP-002..008)

| Task ID | Description | When Planned | Priority | Decision/Status |
|---------|-------------|--------------|----------|-----------------|
| P6-SETUP-002 | Review Phase-5 deliverables | **Week-0** | 🟠 High | ❌ MISSING - Review Schema Canon, API contracts, resolution engine docs |
| P6-SETUP-003 | Create Phase-6 task register | **Week-0** | 🔴 **COMPLIANCE** | ❌ MISSING - Single source of truth for all Phase-6 tasks |
| P6-SETUP-004 | Create Costing manual structure | **Week-0** | 🟠 High | ❌ MISSING - Directory structure for costing documentation |
| P6-SETUP-005 | Freeze Costing Engine Contract (QCD v1.0) | **Week-0** | 🔴 **COMPLIANCE** | ❌ MISSING - Must freeze QCD contract before costing work |
| P6-SETUP-006 | Define D0 Gate checklist | **Week-0** | 🔴 **COMPLIANCE** | ❌ MISSING - D0 Gate definition required (checklist only, not passed yet) |
| P6-SETUP-007 | Review Phase-5 for implementation obligations | **Week-0** | 🟠 High | ❌ MISSING - Review Category A/B/C/D for Phase-6 obligations |
| P6-SETUP-008 | Create module folder boundaries + PR rules | **Week-0** | 🟠 High | ❌ MISSING - Module ownership boundaries per Phase-5 Module Ownership Matrix |

**Decision:**
- All are **Week-0 tasks** (same week as runner script)
- **3 Compliance Tasks:** P6-SETUP-003, P6-SETUP-005, P6-SETUP-006 (must resolve before Phase-6 closure)
- **4 High Priority Tasks:** P6-SETUP-002, P6-SETUP-004, P6-SETUP-007, P6-SETUP-008 (should resolve)
- **Action Required:** Create/verify all governance documents
- **Blocking:** Compliance tasks block Phase-6 closure

---

### Database Tasks (P6-DB-001..005)

| Task ID | Description | When Planned | Priority | Decision/Status |
|---------|-------------|--------------|----------|-----------------|
| P6-DB-001 | Choose DB creation approach | **Week-0 to Week-1** | 🟠 High | ❌ MISSING - Lock method for Canon v1.0 |
| P6-DB-002 | Implement DB schema from Canon v1.0 | **Week-0 to Week-1** | — | ✅ DONE - Schema drift checks exist and pass |
| P6-DB-003 | Execute seed script (C5) | **Week-0 to Week-1** | — | ✅ DONE - Included in schema implementation |
| P6-DB-004 | Schema parity gate | **Week-0 to Week-1** | — | ✅ DONE - Schema drift check validates parity |
| P6-DB-005 | Seed cost template master data | **Week-0** | 🔴 **COMPLIANCE** | ❌ MISSING - Spec-only (no DB mutation), defines what must be seeded later |

**Decision:**
- **Timeline:** Week-0 to Week-1 (Track E - Canon Implementation)
- **3 Tasks Done:** P6-DB-002..004 (schema implementation complete)
- **2 Tasks Missing:** P6-DB-001 (decision needed), P6-DB-005 (spec needed)
- **Action Required:** 
  - P6-DB-001: Choose and document DB creation method
  - P6-DB-005: Create cost template seed specification (spec-only, no DB mutation)
- **Blocking:** P6-DB-005 is compliance-critical

---

## Week-0 Closure Criteria

### Required for Closure (From Week-0 Detailed Plan)

1. ✅ **Governance Pack Created** (Structural completion) - ✅ DONE
2. ⏳ **All Governance Documents Verified** (Need to verify files exist) - ⏳ PENDING
3. ⏳ **All Compliance Alarms Resolved** (5 compliance alarms) - ❌ PENDING
4. ⏳ **Entry Gate Documentation Complete** (Formal records needed) - ⏳ PENDING
5. ⏳ **Task Register Accessible** (Single source of truth verified) - ⏳ PENDING
6. ⏳ **QCD Contract Verified** (File exists and is frozen) - ⏳ PENDING
7. ⏳ **D0 Gate Checklist Verified** (File exists) - ⏳ PENDING
8. ⏳ **Naming Conventions Document Verified** (Compliance doc exists) - ⏳ PENDING
9. ⏳ **Module Boundaries Document Verified** (Structure doc exists) - ⏳ PENDING

**Current Closure Status:**
- **Structural Completion:** ✅ DONE (Governance pack created)
- **Document Verification:** ⏳ PENDING (Need to verify all files exist)
- **Compliance Alarms:** ❌ 5 alarms need resolution
- **Formal Sign-off:** ⏳ PENDING

---

## Compliance Alarms (Must Resolve Before Phase-6 Closure)

### 🔴 ALARM-SETUP-DOCS (Compliance - Blocks Governance)

**Tasks Affected:** P6-SETUP-003, P6-SETUP-005, P6-SETUP-006

**When:** **Week-0** (must complete before Phase-6 closure)

**Decision:**
- All three tasks are **mandatory** for Phase-6 sign-off
- They block governance compliance and cannot be deferred
- **Resolution:**
  - P6-SETUP-003: Verify/create Phase-6 task register (single source of truth)
  - P6-SETUP-005: Verify QCD contract exists: `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
  - P6-SETUP-006: Verify D0 Gate checklist exists: `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`

---

### 🔴 ALARM-ENTRY-006 (Compliance - Naming Conventions)

**Task Affected:** P6-ENTRY-006

**When:** **Week-0** (must complete before Phase-6 closure)

**Decision:**
- Required for all new migrations/models/routes
- Compliance-critical for governance
- **Resolution:** Create naming convention compliance document verifying:
  - Table naming: snake_case, plural
  - Column naming: snake_case, singular
  - FK naming: {table_singular}_id
  - Enum naming: UPPER_SNAKE_CASE

---

### 🔴 ALARM-DB-005 (Compliance - Cost Template Seed)

**Task Affected:** P6-DB-005

**When:** **Week-0** (must complete before Phase-6 closure)

**Decision:**
- Required for cost adders implementation
- Spec-only (no DB mutation in Week-0)
- **Resolution:** Verify cost template seed specification exists: `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`
- **Note:** Spec-only definition (no DB mutation), defines what must be seeded later

---

## High Priority Alarms (Should Resolve)

### 🟠 ALARM-SETUP-002, ALARM-SETUP-004, ALARM-SETUP-007, ALARM-SETUP-008, ALARM-DB-001

**When:** **Week-0** (should resolve, not blocking Phase-6 closure)

**Decision:**
- These are high priority but not blocking
- Should be completed in Week-0 if possible
- Can be deferred if necessary (but not recommended)

---

## Key Decisions Summary

### 1. **Timeline Decision: All Tasks in Week-0**

**Decision:** All "not covered" tasks are scheduled for **Week-0** (same week as runner script).

**Rationale:**
- Week-0 is the entry gate and setup week
- These tasks establish foundation for Phase-6 execution
- Compliance tasks must be complete before Phase-6 closure

---

### 2. **Separation Decision: Runner Script vs Other Tasks**

**Decision:** Runner script is **read-only verification only**. Other tasks are **separate deliverables**.

**Rationale:**
- Runner script = automated verification (can run repeatedly)
- Other tasks = documentation/implementation work (one-time creation)
- Separation allows parallel execution and clear ownership

---

### 3. **Priority Decision: Compliance vs High Priority**

**Decision:** 
- **Compliance tasks** (🔴) = Must resolve before Phase-6 closure (blocking)
- **High priority tasks** (🟠) = Should resolve (not blocking but recommended)

**Compliance Tasks (5 total):**
1. P6-ENTRY-006: Naming conventions compliance
2. P6-SETUP-003: Phase-6 task register
3. P6-SETUP-005: QCD Contract v1.0
4. P6-SETUP-006: D0 Gate checklist
5. P6-DB-005: Cost template seed specification

---

### 4. **Execution Order Decision**

**Decision:** Tasks can be executed in parallel or sequentially, but compliance tasks should be prioritized.

**Recommended Order:**
1. **First:** Compliance tasks (P6-ENTRY-006, P6-SETUP-003, P6-SETUP-005, P6-SETUP-006, P6-DB-005)
2. **Second:** High priority tasks (P6-SETUP-002, P6-SETUP-004, P6-SETUP-007, P6-SETUP-008, P6-DB-001)
3. **Third:** Medium priority tasks (P6-ENTRY-002..005)

---

## Action Items

### Immediate (Week-0)

1. **Create Compliance Documents:**
   - [ ] P6-ENTRY-006: Naming conventions compliance document
   - [ ] P6-SETUP-003: Phase-6 task register
   - [ ] P6-SETUP-005: QCD Contract v1.0 (`docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`)
   - [ ] P6-SETUP-006: D0 Gate checklist (`docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`)
   - [ ] P6-DB-005: Cost template seed specification (`docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`)

2. **Create High Priority Documents:**
   - [ ] P6-SETUP-002: Phase-5 review document
   - [ ] P6-SETUP-004: Costing manual structure (`docs/PHASE_6/COSTING/MANUAL/`)
   - [ ] P6-SETUP-007: Implementation obligations document
   - [ ] P6-SETUP-008: Module boundaries document
   - [ ] P6-DB-001: DB creation method document (`docs/PHASE_6/DB/DB_CREATION_METHOD.md`)

3. **Create Entry Gate Documentation:**
   - [ ] P6-ENTRY-002: Schema Canon verification record
   - [ ] P6-ENTRY-003: Decision Register closure record
   - [ ] P6-ENTRY-004: Freeze Gate Checklist verification
   - [ ] P6-ENTRY-005: Core resolution engine test verification

---

## Conclusion

**All "not covered" tasks are scheduled for Week-0** (same week as the runner script). They are **separate deliverables** that need to be completed to achieve **complete Week-0 closure**.

**Key Points:**
- ✅ Timeline: All tasks in Week-0
- ✅ Decision: Separation between runner script (verification) and other tasks (documentation/implementation)
- ✅ Priority: 5 compliance tasks must be completed before Phase-6 closure
- ✅ Status: Currently all missing or partial (need to be created/verified)

**Next Step:** Create/verify all Week-0 deliverables to achieve complete Week-0 closure.

---

**Report Generated:** 2026-01-12  
**Source:** PHASE6_WEEK0_DETAILED_PLAN.md + Cross-verification against planning documents
