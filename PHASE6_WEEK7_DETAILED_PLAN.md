# Phase-6 Week-7 Detailed Plan

**Week:** Week-7 (Costing Pack Foundation + Operational Readiness)  
**Status:** ❌ NOT STARTED (Planning only - Track D execution blocked until D0 Gate signoff)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-7 turns the system into a finance-consumable product by introducing costing pack foundation and operational readiness foundation. This includes quotation costing snapshot, panel summary view, and role-based access control for costing pack access.

**Key Deliverables (Week-7 Core Closure):**
- Costing Pack Foundation (Track D - quotation costing snapshot, panel summary view)
- Operational Readiness Foundation (Track C - role-based access, permissions, approval flow design)
- D0 Gate Verification (Track D0 - must be signed off before Track D execution)

**Critical Alarms (From Matrix):**
- 🔴 **Gate Blocker**
  - ALARM-D0-GATE: Track D execution blocked until D0 Gate signoff (P6-COST-D0-007)
- 🔴 **Operational Risk**
  - ALARM-OPS-PERMISSIONS: Permission checks must be enforced (P6-OPS-003)
- 🟠 **High Priority Items** (design documentation, role/permission implementation)

**Note:** Week-7 does not do: global dashboards, Excel export, catalog governance, deep audit UI. Track D execution is blocked until D0 Gate signoff, but planning can proceed.

---

## Week-7 Task Breakdown

### Track: Costing Pack Foundation (Track D) + Operational Readiness (Track C) + D0 Gate Verification (Track D0)

#### Track D - Costing Pack Foundation

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-COST-001 | Design Costing Pack UI | `docs/PHASE_6/COSTING/COSTING_PACK_DESIGN.md` | ❌ MISSING | 🟠 | Design document with costing snapshot view, panel summary view, navigation skeleton |
| P6-COST-002 | Confirm D0 Gate passed | D0 Gate verification document/reference | ❌ MISSING | 🔴 **GATE** | D0 Gate signoff verification (P6-COST-D0-007). Track D execution blocked until D0 Gate passes |
| P6-COST-003 | Implement quotation costing snapshot | UI/API view fed by QCD+QCA only | ❌ MISSING | 🔴 **COMPLIANCE** | Quotation costing snapshot sourced from QCD+QCA only (no duplicate calculators). Must show: quotation total cost, cost heads totals (from QCA), BOM cost totals (from QCD), margin placeholders |
| P6-COST-004 | Implement panel summary view | UI/API view fed by QCD+QCA only | ❌ MISSING | 🔴 **COMPLIANCE** | Panel summary view sourced from QCD+QCA only (no duplicate calculators). Must show panel cost totals from QCD/QCA |

**Track D Status:** ❌ NOT STARTED (Track D execution blocked until D0 Gate signoff)

**Non-Negotiable Rules:**
- ✅ Use QCD/QCA only (engine-first approach)
- ❌ No costing breakup inside quotation normal view
- ✅ Costing pack may show controlled breakdown (within pack only) but must respect canon
- ❌ No schema changes
- ✅ D0 Gate is a hard precondition to Track D execution (but not to planning)

---

#### Track C - Operational Readiness Foundation

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-OPS-001 | Design role-based access | `docs/PHASE_6/OPS/ROLE_BASED_ACCESS_DESIGN.md` | ❌ MISSING | 🟠 | Design document for role-based access control |
| P6-OPS-002 | Implement basic roles | Role tables/use existing role system | ❌ MISSING | 🟠 | Implement basic roles (or use existing role system) |
| P6-OPS-003 | Permission checks | Middleware/guards for permission checks | ❌ MISSING | 🔴 **COMPLIANCE** | Permission checks middleware/guards. Must be implemented for operational readiness |
| P6-OPS-004 | Design approval flows | `docs/PHASE_6/OPS/APPROVAL_FLOWS_DESIGN.md` | ❌ MISSING | 🟠 | Design document for approval flows (design foundation, no heavy workflow yet) |
| P6-OPS-005 | Implement price change approval | Price change approval workflow implementation | ❌ MISSING | 🟠 | Price change approval workflow implementation (Week-7 scope) |
| P6-OPS-006 | Implement override approval | Override approval workflow implementation | ❌ MISSING | 🟠 | Override approval workflow implementation (Week-7 scope) |

**Track C Status:** ❌ MISSING (Operational readiness foundation not implemented)

**Week-7 Scope Limit:** Implement only the minimum roles/permissions required for operational readiness foundation. Full costing pack permissions (P6-OPS-012) is in Week-8.

---

## Alarm Summary for Week-7

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-D0-GATE** | Review 4 (Finalized Review 4) | P6-COST-002, P6-COST-D0-007 | D0 Gate signoff (gate blocker for Track D execution) | ❌ MISSING | Verify D0 Gate signoff (P6-COST-D0-007) before Track D execution |
| **ALARM-OPS-PERMISSIONS** | Review 1 (Finalized Review 4) | P6-OPS-003 | Permission checks enforcement (operational risk) | ❌ MISSING | Implement permission checks middleware/guards for operational readiness |

**Alarm Details:**

#### ALARM-D0-GATE (Gate Blocker for Track D Execution)
- **Tasks Affected:** P6-COST-002 (D0 Gate verification), P6-COST-D0-007 (D0 Gate signoff from Week-6)
- **Impact:** Gate blocker. Track D (Costing Pack) execution is blocked until D0 Gate is signed off.
- **Matrix Status:** Finalized in Review 4 as **GATE** alarm
- **Resolution:** 
  - P6-COST-002: Confirm D0 Gate passed
    - Verify D0 Gate signoff (P6-COST-D0-007 from Week-6)
    - Document D0 Gate verification reference
    - Track D execution cannot proceed until D0 Gate passes
- **Notes:** D0 Gate (P6-COST-D0-007) is a gate blocker. Track D execution is blocked until D0 Gate signoff. However, Week-7 planning can proceed. Track D execution must wait for D0 Gate signoff.

#### ALARM-OPS-PERMISSIONS (Operational Risk)
- **Tasks Affected:** P6-OPS-003 (Permission checks)
- **Impact:** Operational risk. If permission checks are not implemented, Week-7 cannot be "operationally ready".
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-OPS-003: Implement permission checks
    - Middleware/guards for permission checks
    - Role-based access control enforcement
    - Basic permission framework for operational readiness
- **Notes:** Permission checks must be implemented for operational readiness foundation. Full costing pack permissions (P6-OPS-012) is in Week-8 scope.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-COST-001 | P6-COST-001 | Design Costing Pack UI | ❌ MISSING | Create design document: `docs/PHASE_6/COSTING/COSTING_PACK_DESIGN.md` |
| ALARM-OPS-001 | P6-OPS-001 | Design role-based access | ❌ MISSING | Create design document: `docs/PHASE_6/OPS/ROLE_BASED_ACCESS_DESIGN.md` |
| ALARM-OPS-002 | P6-OPS-002 | Implement basic roles | ❌ MISSING | Implement basic roles (or use existing role system) |
| ALARM-OPS-004 | P6-OPS-004 | Design approval flows | ❌ MISSING | Create design document: `docs/PHASE_6/OPS/APPROVAL_FLOWS_DESIGN.md` |
| ALARM-OPS-005 | P6-OPS-005 | Implement price change approval | ❌ MISSING | Implement price change approval workflow |
| ALARM-OPS-006 | P6-OPS-006 | Implement override approval | ❌ MISSING | Implement override approval workflow |

---

### 🟡 Medium Priority (Non-Critical Enhancements)

These items are enhancements and not blocking Phase-6 closure.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| Approval Flows Implementation | Heavy workflow implementation | ⏳ DEFERRED | Approval flows design foundation only (no heavy workflow yet) |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-7 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-COST-001..004 (Costing Pack Foundation - 4 tasks)
- ✅ P6-OPS-001, 002, 003, 004, 005, 006 (Operational Readiness - 6 tasks)

### ⚠️ Items Requiring Verification

1. **Costing Pack Foundation Implementation (P6-COST-001..004)**
   - Need to verify D0 Gate signoff before Track D execution
   - Need to verify costing snapshot uses QCD/QCA only
   - Need to verify panel summary uses QCD/QCA only
   - Need to verify no duplicate calculators
   - Current status: ❌ NOT STARTED (Track D execution blocked until D0 Gate)

2. **Operational Readiness Implementation (P6-OPS-001..004, 012)**
   - Need to verify role-based access implemented
   - Need to verify permission checks implemented
   - Need to verify costing pack permissions enforced
   - Current status: ❌ MISSING (needs verification)

---

## Week-7 Closure Criteria

### Required for Closure

1. ⏳ **D0 Gate Verified** (P6-COST-002)
   - D0 Gate signoff verified (P6-COST-D0-007 from Week-6)
   - Track D execution can proceed
2. ⏳ **Costing Pack Snapshot View Implemented** (P6-COST-003)
   - Sourced from QCD+QCA only
   - Shows quotation total cost, cost heads totals, BOM cost totals, margin placeholders
   - No duplicate calculators
3. ⏳ **Panel Summary View Implemented** (P6-COST-004)
   - Sourced from QCD+QCA only
   - Shows panel cost totals
   - No duplicate calculators
4. ⏳ **Role-Based Access Implemented** (P6-OPS-001, 002)
   - Basic roles implemented (or existing role system used)
5. ⏳ **Permission Checks Implemented** (P6-OPS-003)
   - Middleware/guards for permission checks
   - Role-based access control enforcement
6. ⏳ **Approval Workflows Implemented** (P6-OPS-005, 006)
   - Price change approval workflow
   - Override approval workflow
7. ⏳ **All Tests Passing** (Costing pack + Ops tests)
8. ⏳ **Design Documents Created** (P6-COST-001, P6-OPS-001, P6-OPS-004)
9. ⏳ **All Compliance Alarms Resolved** (2 compliance alarms)
10. ⏳ **No Schema Changes Introduced** (scope guard)
11. ⏳ **QCD/QCA Only Rule Enforced** (no duplicate calculators)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ❌ NOT STARTED (Track D execution blocked until D0 Gate signoff)
- **Compliance Alarms:** ❌ 2 alarms need resolution (ALARM-D0-GATE, ALARM-OPS-PERMISSIONS)
- **Formal Sign-off:** ⏳ PENDING (D0 Gate blocker)

**Closure Rule:** Week-7 is CLOSED only if costing pack foundation is implemented (with D0 Gate verified) and operational readiness (permissions) is enforced. Track D execution is blocked until D0 Gate signoff, but planning can proceed.

---

## Dependencies

### Requires (Execution)

- **Week-6:** D0 Gate signoff (P6-COST-D0-007) - blocks Track D execution
- **Week-3-6:** Stable cost summary (already exists)
- **Week-3-4:** Pricing/resolution statuses available (for flags)

### Can Run in Parallel (Planning / Scaffolding)

- **Track C:** Role/permission scaffolding can be built without D0 completion
- **Design:** Costing Pack UI design can proceed without D0 completion

### Blocks

- **Week-8:** Costing Pack details & pivots depend on Week-7 foundation
- **Week-9:** Global dashboard may depend on costing pack foundation

---

## Risks & Mitigations

### Risk 1: Costing Pack Uses Ad-Hoc Calculations (Violates QCD/QCA-Only Rule)

**Mitigation:** Enforce QCD/QCA-only rule. Add test that forbids other sources. Costing pack must source data from QCD+QCA only (no duplicate calculators).

### Risk 2: D0 Gate Not Ready Blocks Week-7 Execution

**Mitigation:** Still complete Week-7 design + permission scaffolding. Execute Track D once gate passes. Planning can proceed; execution is blocked until D0 Gate signoff.

### Risk 3: Permission Checks Incomplete Causes Operational Risk

**Mitigation:** Gate Week-7 closure on P6-OPS-003 enforcement. Permission checks must be implemented for operational readiness foundation. Full costing pack permissions (P6-OPS-012) is in Week-8 scope.

### Risk 4: Schema Changes Introduced

**Mitigation:** No schema changes allowed. Use existing schema only. Scope guard: no schema changes.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Verify D0 Gate (Blocking Track D Execution)

1. **D0 Gate Verification**
   - P6-COST-002: Confirm D0 Gate passed
   - Verify D0 Gate signoff (P6-COST-D0-007 from Week-6)
   - Document D0 Gate verification reference
   - Track D execution cannot proceed until D0 Gate passes

#### Priority 2: Implement Costing Pack Foundation (After D0 Gate)

2. **Costing Pack Implementation (Track D)**
   - P6-COST-001: Create costing pack UI design document
   - P6-COST-003: Implement quotation costing snapshot (QCD+QCA only)
   - P6-COST-004: Implement panel summary view (QCD+QCA only)
   - Tests: test_snapshot_view.py, test_panel_summary_view.py
   - Verify QCD/QCA-only rule (no duplicate calculators)

#### Priority 3: Implement Operational Readiness (Can Proceed in Parallel)

3. **Operational Readiness Implementation (Track C)**
   - P6-OPS-001: Create role-based access design document
   - P6-OPS-002: Implement basic roles (or use existing role system)
   - P6-OPS-003: Implement permission checks (middleware/guards)
   - P6-OPS-004: Create approval flows design document
   - P6-OPS-005: Implement price change approval workflow
   - P6-OPS-006: Implement override approval workflow
   - Tests: test_role_guards.py, test_approval_workflows.py

#### Priority 4: Verification

4. **Implementation Verification**
   - Verify D0 Gate signoff
   - Verify costing pack uses QCD/QCA only
   - Verify permission enforcement works
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week7_checks.sh` - Week-7 verification runner
     - Runs all Week-7 tests (costing pack + ops)
     - Verifies API endpoints
     - Validates costing pack functionality (QCD/QCA-only rule)
     - Validates permission enforcement
     - Generates evidence summary

2. **Tests:**
   - `tests/costing_pack/test_snapshot_view.py` - Costing snapshot view tests
     - Test quotation costing snapshot
     - Test QCD/QCA-only rule (no duplicate calculators)
     - Test quotation total cost, cost heads totals, BOM cost totals
     - Test margin placeholders
   - `tests/costing_pack/test_panel_summary_view.py` - Panel summary view tests
     - Test panel summary view
     - Test QCD/QCA-only rule (no duplicate calculators)
     - Test panel cost totals from QCD/QCA
   - `tests/ops/test_role_guards.py` - Role-based access control tests
     - Test permission checks middleware/guards
     - Test role-based access control enforcement
     - Test basic roles
   - `tests/ops/test_approval_workflows.py` - Approval workflow tests
     - Test price change approval workflow
     - Test override approval workflow
     - Test permission checks middleware/guards
     - Test role-based access control enforcement
     - Test basic roles

3. **Evidence:**
   - `evidence/PHASE6_WEEK7_EVIDENCE_PACK.md` - Week-7 evidence documentation
     - API endpoint documentation
     - Test results summary
     - Costing pack UI screenshots
     - D0 Gate verification link/hash
     - Role matrix excerpt
     - Permission enforcement verification

4. **API Endpoints:**
   - GET /api/v1/quotation/{id}/costing/snapshot - Quotation costing snapshot
   - GET /api/v1/quotation/{id}/panel/{panelId}/costing/summary - Panel summary view

5. **Frontend Components:**
   - Costing snapshot view component (quotation-level)
   - Panel summary view component
   - Costing pack navigation skeleton

6. **Backend Services:**
   - Costing pack service (QCD/QCA integration)
   - Role-based access control service
   - Permission enforcement service

7. **Documentation:**
   - `docs/PHASE_6/COSTING/COSTING_PACK_DESIGN.md` - Costing Pack UI design document
   - `docs/PHASE_6/COSTING/D0_GATE_VERIFICATION.md` - D0 Gate verification document
   - `docs/PHASE_6/OPS/ROLE_BASED_ACCESS_DESIGN.md` - Role-based access design document
   - `docs/PHASE_6/OPS/APPROVAL_FLOWS_DESIGN.md` - Approval flows design document

### Verification Checklist

- [ ] Verify scripts/run_week7_checks.sh exists
- [ ] Verify all test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify D0 Gate signoff (P6-COST-002)
- [ ] Verify costing pack uses QCD/QCA only (P6-COST-003/004)
- [ ] Verify no duplicate calculators
- [ ] Verify permission enforcement works (P6-OPS-003)
- [ ] Verify approval workflows work (P6-OPS-005, 006)
- [ ] Verify role-based access works (P6-OPS-001/002/003)
- [ ] Verify evidence/PHASE6_WEEK7_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-7 runner
- [ ] Verify no schema changes introduced

---

## Decision Point

**Week-7 Closure Status:**
- ⏳ **PENDING COMPLETION** (D0 Gate verification + implementation required)

**Options:**
1. **"Close Week-7 and start Week-8 detailed plan"** - If D0 Gate verified, costing pack implemented, and permissions enforced
2. **"Verify D0 Gate and proceed with Track D execution"** - If D0 Gate needs verification
3. **"Complete Week-7 implementation"** - If costing pack or permissions still missing

**Note:** Track D execution is blocked until D0 Gate signoff. Planning can proceed, but execution must wait.

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-7 tasks)
- **D0 Gate Signoff:** Week-6 (P6-COST-D0-007) - must be verified before Track D execution
- **QCD Contract v1.0:** (Week-0 governance pack - for QCD/QCA-only rule)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 10 | All captured from matrix |
| **Compliance Alarms** | 2 | 🔴 Must resolve |
| **High Priority Alarms** | 6 | 🟠 Should resolve |
| **Medium Priority Items** | 1 | 🟡 Can be deferred |
| **Completed Tasks** | 0 | None complete |
| **Missing Tasks** | 10 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-D0-GATE:** Verify D0 Gate signoff before Track D execution (P6-COST-002, P6-COST-D0-007)
- [ ] **ALARM-OPS-PERMISSIONS:** Implement permission checks enforcement (P6-OPS-003)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-COST-001:** Create Costing Pack UI design document (P6-COST-001)
- [ ] **ALARM-OPS-001:** Create role-based access design document (P6-OPS-001)
- [ ] **ALARM-OPS-002:** Implement basic roles (P6-OPS-002)
- [ ] **ALARM-OPS-004:** Create approval flows design document (P6-OPS-004)
- [ ] **ALARM-OPS-005:** Implement price change approval (P6-OPS-005)
- [ ] **ALARM-OPS-006:** Implement override approval (P6-OPS-006)

### Documentation Tasks

- [ ] Complete costing pack implementation (P6-COST-003/004)
- [ ] Complete operational readiness implementation (P6-OPS-001/002/003/004/005/006)
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete
- [ ] Verify no schema changes introduced
- [ ] Verify QCD/QCA-only rule enforced

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After D0 Gate verification and implementation

**Note:** Week-7 does not do: global dashboards, Excel export, catalog governance, deep audit UI. Track D execution is blocked until D0 Gate signoff (P6-COST-D0-007 from Week-6), but planning can proceed. Costing pack must use QCD/QCA only (engine-first approach, no duplicate calculators).
