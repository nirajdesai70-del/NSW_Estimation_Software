# Phase-6 Week-8 Detailed Plan

**Week:** Week-8 (Costing Pack Details + Operations Completion)  
**Status:** ❌ NOT STARTED (Planning only)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-8 deepens financial transparency and governance by extending the Costing Pack into detailed, auditable views and introducing audit visibility across quotation lifecycle, pricing, and approvals. This includes costing pack details (BOM/Feeder breakdown, CostHead grouping, pivot tables), costing pack navigation, and operational readiness completion (audit visibility, SOPs, audit export, costing pack permissions).

**Key Deliverables (Week-8 Core Closure):**
- Costing Pack Details (Track D - BOM/Feeder breakdown, CostHead grouping, pivot tables, navigation)
- Operations Completion (Track C - audit visibility, SOPs, audit export, costing pack permissions)

**Critical Alarms (From Matrix):**
- 🔴 **Compliance Alarms** (must resolve for Week-8 closure)
  - Costing pack details (P6-COST-005, 006, 007)
  - Costing pack permissions (P6-OPS-012)
- 🟠 **High Priority Items** (design documentation, audit visibility, SOPs, audit export)

**Note:** Week-8 consumes Week-7 foundations and assumes D0 Gate has passed. No new costing logic is introduced — only presentation, pivots, audit trails, and permission-aware visibility. Week-8 does not do: Excel export (Week-10), global dashboard (Week-9), catalog governance (Week-6), new approval workflows.

---

## Week-8 Task Breakdown

### Track: Costing Pack Details (Track D) + Operations Completion (Track C)

#### Track D - Costing Pack Details

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-COST-005 | Implement BOM/Feeder costing breakdown | BOM/Feeder costing breakdown view | ❌ MISSING | 🔴 **COMPLIANCE** | BOM/Feeder costing breakdown view. QCD/QCA only (no duplicate calculators) |
| P6-COST-006 | Implement CostHead grouping (mandatory) | CostHead grouping pivot/view | ❌ MISSING | 🔴 **COMPLIANCE** | CostHead grouping (BUSBAR, LABOUR, etc.) - mandatory compliance requirement. QCD/QCA only |
| P6-COST-007 | Implement pivot tables | Pivot tables for costing analysis | ❌ MISSING | 🔴 **COMPLIANCE** | Pivot tables (category, make, series, rate source). QCD/QCA only, read-only |
| P6-COST-008 | Implement costing pack navigation | Costing pack navigation UI | ❌ MISSING | 🟠 | Costing pack navigation UI (drill-down navigation, view switching) |

**Track D Status:** ❌ NOT STARTED (Costing pack details not implemented)

**Non-Negotiable Rules:**
- ✅ Use QCD/QCA only (engine-first approach)
- ❌ No calculators
- ❌ No recompute
- ✅ All views are read-only
- ❌ No schema changes

---

#### Track C - Operations Completion

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-OPS-007 | Design audit visibility UI | `docs/PHASE_6/OPS/AUDIT_VISIBILITY_UI_DESIGN.md` | ❌ MISSING | 🟠 | Design document for audit visibility UI |
| P6-OPS-008 | Implement audit log display | Audit log display UI/timeline view | ❌ MISSING | 🟠 | Audit log display (timeline view for quotation). Read-only, query-only |
| P6-OPS-009 | Implement audit log details | Audit log details view | ❌ MISSING | 🟠 | Audit log details (pricing changes, discount changes, lock/unlock, approvals). Read-only |
| P6-OPS-010 | Create initial SOPs | Initial SOPs documentation | ❌ MISSING | 🟠 | Create initial SOPs (Standard Operating Procedures) for operations |
| P6-OPS-011 | Implement audit export | Audit export functionality | ❌ MISSING | 🟠 | Audit export (export audit logs to file format). Read-only export |
| P6-OPS-012 | Costing Pack/dashboard/export permissions + bulk discount approval hook | Permission matrix + enforcement | ❌ MISSING | 🔴 **COMPLIANCE** | Costing pack permissions enforcement (role → view matrix). Bulk discount approval hook. Must restrict costing pack/dashboard/export access |

**Track C Status:** ❌ MISSING (Operations completion not implemented)

**Week-8 Scope Limit:** Complete operational readiness with audit visibility, SOPs, and costing pack permissions. No new approval workflow logic (visibility only).

---

## Alarm Summary for Week-8

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-COSTING-DETAILS** | Review 1 (Finalized Review 4) | P6-COST-005, P6-COST-006, P6-COST-007 | Missing costing pack details (BOM/Feeder breakdown, CostHead grouping, pivot tables) | ❌ MISSING | Implement costing pack details (BOM/Feeder breakdown, CostHead grouping, pivot tables) - QCD/QCA only |
| **ALARM-OPS-012** | Review 1 (Finalized Review 4) | P6-OPS-012 | Costing pack permissions enforcement (operational risk) | ❌ MISSING | Implement costing pack/dashboard/export permissions enforcement (role → view matrix) |

**Alarm Details:**

#### ALARM-COSTING-DETAILS (Compliance - Costing Pack Details)

- **Tasks Affected:** P6-COST-005 (BOM/Feeder breakdown), P6-COST-006 (CostHead grouping), P6-COST-007 (Pivot tables)
- **Impact:** Compliance requirement. Costing pack details must be implemented for financial transparency and auditability.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-COST-005: Implement BOM/Feeder costing breakdown
    - BOM/Feeder costing breakdown view
    - QCD/QCA only (no duplicate calculators)
    - Read-only view
  - P6-COST-006: Implement CostHead grouping (mandatory)
    - CostHead grouping pivot/view (BUSBAR, LABOUR, etc.)
    - QCD/QCA only (no duplicate calculators)
    - Mandatory compliance requirement
  - P6-COST-007: Implement pivot tables
    - Pivot tables for costing analysis (category, make, series, rate source)
    - QCD/QCA only (no duplicate calculators)
    - Read-only view
- **Notes:** All costing pack details must use QCD/QCA only (engine-first approach). No calculators, no recompute. All views are read-only.

#### ALARM-OPS-012 (Operational Risk - Costing Pack Permissions)

- **Tasks Affected:** P6-OPS-012 (Costing pack permissions)
- **Impact:** Operational risk. If costing pack permissions are not enforced, Week-8 cannot be "operationally ready".
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-OPS-012: Implement costing pack/dashboard/export permissions
    - Permission matrix for costing pack access (role → view matrix)
    - Permission enforcement for costing pack/dashboard/export endpoints/UI
    - Bulk discount approval hook
    - Access control for costing pack views
- **Notes:** Costing pack permissions must be enforced for operational readiness. Week-8 closure is gated on permission enforcement.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-COST-008 | P6-COST-008 | Implement costing pack navigation | ❌ MISSING | Implement costing pack navigation UI (drill-down navigation, view switching) |
| ALARM-OPS-007 | P6-OPS-007 | Design audit visibility UI | ❌ MISSING | Create design document: `docs/PHASE_6/OPS/AUDIT_VISIBILITY_UI_DESIGN.md` |
| ALARM-OPS-008 | P6-OPS-008 | Implement audit log display | ❌ MISSING | Implement audit log display (timeline view for quotation) |
| ALARM-OPS-009 | P6-OPS-009 | Implement audit log details | ❌ MISSING | Implement audit log details (pricing changes, discount changes, lock/unlock, approvals) |
| ALARM-OPS-010 | P6-OPS-010 | Create initial SOPs | ❌ MISSING | Create initial SOPs (Standard Operating Procedures) for operations |
| ALARM-OPS-011 | P6-OPS-011 | Implement audit export | ❌ MISSING | Implement audit export (export audit logs to file format) |

---

### 🟡 Medium Priority (Non-Critical Enhancements)

These items are enhancements and not blocking Phase-6 closure.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| Advanced pivot features | Advanced pivot table features | ⏳ DEFERRED | Advanced pivot features (can be added later) |
| Enhanced audit visibility | Enhanced audit visibility features | ⏳ DEFERRED | Enhanced audit visibility features (can be added later) |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-8 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-COST-005..008 (Costing Pack Details - 4 tasks)
- ✅ P6-OPS-007..012 (Operations Completion - 6 tasks)

### ⚠️ Items Requiring Verification

1. **Costing Pack Details Implementation (P6-COST-005..008)**
   - Need to verify BOM/Feeder breakdown uses QCD/QCA only
   - Need to verify CostHead grouping uses QCD/QCA only
   - Need to verify pivot tables use QCD/QCA only
   - Need to verify costing pack navigation works
   - Current status: ❌ NOT STARTED (needs verification)

2. **Operations Completion Implementation (P6-OPS-007..012)**
   - Need to verify audit visibility UI implemented
   - Need to verify audit log display implemented
   - Need to verify audit log details implemented
   - Need to verify SOPs created
   - Need to verify audit export implemented
   - Need to verify costing pack permissions enforced
   - Current status: ❌ MISSING (needs verification)

---

## Week-8 Closure Criteria

### Required for Closure

1. ⏳ **Costing Pack Details Implemented** (P6-COST-005, 006, 007)
   - BOM/Feeder costing breakdown view (QCD/QCA only)
   - CostHead grouping pivot/view (QCD/QCA only)
   - Pivot tables (QCD/QCA only)
   - All views are read-only
2. ⏳ **Costing Pack Navigation Implemented** (P6-COST-008)
   - Costing pack navigation UI
   - Drill-down navigation
   - View switching
3. ⏳ **Audit Visibility Implemented** (P6-OPS-007, 008, 009)
   - Audit visibility UI design
   - Audit log display (timeline view)
   - Audit log details (pricing, discount, lock/unlock, approvals)
4. ⏳ **SOPs Created** (P6-OPS-010)
   - Initial SOPs documentation created
5. ⏳ **Audit Export Implemented** (P6-OPS-011)
   - Audit export functionality (export audit logs)
6. ⏳ **Costing Pack Permissions Enforced** (P6-OPS-012)
   - Permission matrix for costing pack access (role → view matrix)
   - Permission enforcement for costing pack/dashboard/export endpoints/UI
   - Bulk discount approval hook
7. ⏳ **All Tests Passing** (Costing pack details + Ops tests)
8. ⏳ **Design Documents Created** (P6-OPS-007)
9. ⏳ **All Compliance Alarms Resolved** (2 compliance alarms)
10. ⏳ **No Schema Changes Introduced** (scope guard)
11. ⏳ **QCD/QCA Only Rule Enforced** (no duplicate calculators)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ❌ NOT STARTED (needs implementation)
- **Compliance Alarms:** ❌ 2 alarms need resolution (ALARM-COSTING-DETAILS, ALARM-OPS-012)
- **Formal Sign-off:** ⏳ PENDING

**Closure Rule:** Week-8 is CLOSED only if costing pack details are implemented (QCD/QCA only) and operations completion (audit visibility, SOPs, audit export, costing pack permissions) is complete.

---

## Dependencies

### Requires (Execution)

- **Week-7:** Costing Pack Foundation (snapshot + panel summary) must be complete
- **Week-6:** D0 Gate must be passed (P6-COST-D0-007) - blocks Track D execution
- **Week-7:** Role & permission enforcement must exist (for P6-OPS-012)
- **Week-5:** Lock/unlock functionality must exist (for audit visibility)

### Can Run in Parallel (Planning / Scaffolding)

- **Design:** Costing pack details design can proceed in parallel
- **Design:** Audit visibility UI design can proceed in parallel

### Blocks

- **Week-9:** Global Dashboard depends on costing pack details
- **Week-10:** Excel export may depend on costing pack details

---

## Risks & Mitigations

### Risk 1: Costing Pack Details Use Ad-Hoc Calculations (Violates QCD/QCA-Only Rule)

**Mitigation:** Enforce QCD/QCA-only rule. Add test that forbids other sources. All costing pack details must source data from QCD+QCA only (no duplicate calculators).

### Risk 2: Permission Leaks Cause Finance Data Exposure

**Mitigation:** Gate Week-8 closure on P6-OPS-012 enforcement. Costing pack permissions must be enforced for operational readiness. Role-matrix tests required.

### Risk 3: Audit Gaps Cause Compliance Issues

**Mitigation:** Mandatory audit view tests required. Audit logs must capture all pricing, discount, lock/unlock, and approval events.

### Risk 4: Schema Changes Introduced

**Mitigation:** No schema changes allowed. Use existing schema only. Scope guard: no schema changes.

### Risk 5: Scope Creep into Approval Workflows

**Mitigation:** Explicit non-goals defined. Week-8 does not do: new approval workflows (visibility only). Approval workflow logic is not part of Week-8 scope.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Implement Costing Pack Details (After D0 Gate Passed)

1. **Costing Pack Details Implementation (Track D)**
   - P6-COST-005: Implement BOM/Feeder costing breakdown (QCD/QCA only)
   - P6-COST-006: Implement CostHead grouping (QCD/QCA only)
   - P6-COST-007: Implement pivot tables (QCD/QCA only)
   - P6-COST-008: Implement costing pack navigation UI
   - Tests: test_cost_pivots.py, test_drilldown_views.py
   - Verify QCD/QCA-only rule (no duplicate calculators)

#### Priority 2: Implement Operations Completion (Can Proceed in Parallel)

2. **Operations Completion Implementation (Track C)**
   - P6-OPS-007: Create audit visibility UI design document
   - P6-OPS-008: Implement audit log display (timeline view)
   - P6-OPS-009: Implement audit log details
   - P6-OPS-010: Create initial SOPs
   - P6-OPS-011: Implement audit export
   - P6-OPS-012: Implement costing pack permissions enforcement
   - Tests: test_audit_visibility.py, test_costing_permissions.py

#### Priority 3: Verification

3. **Implementation Verification**
   - Verify costing pack details use QCD/QCA only
   - Verify permission enforcement works
   - Verify audit visibility works
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week8_checks.sh` - Week-8 verification runner
     - Runs all Week-8 tests (costing pack details + ops)
     - Verifies API endpoints
     - Validates costing pack details functionality (QCD/QCA-only rule)
     - Validates permission enforcement
     - Validates audit visibility
     - Generates evidence summary

2. **Tests:**
   - `tests/costing_pack/test_cost_pivots.py` - Cost pivot tests
     - Test CostHead grouping pivot
     - Test pivot tables (category, make, series, rate source)
     - Test QCD/QCA-only rule (no duplicate calculators)
   - `tests/costing_pack/test_drilldown_views.py` - Drill-down view tests
     - Test BOM/Feeder costing breakdown
     - Test costing pack navigation
     - Test QCD/QCA-only rule (no duplicate calculators)
   - `tests/audit/test_audit_visibility.py` - Audit visibility tests
     - Test audit log display (timeline view)
     - Test audit log details (pricing, discount, lock/unlock, approvals)
     - Test audit export
   - `tests/ops/test_costing_permissions.py` - Costing pack permissions tests
     - Test permission matrix for costing pack access
     - Test permission enforcement for costing pack/dashboard/export endpoints/UI
     - Test bulk discount approval hook
     - Test access control for costing pack views

3. **Evidence:**
   - `evidence/PHASE6_WEEK8_EVIDENCE_PACK.md` - Week-8 evidence documentation
     - API endpoint documentation
     - Test results summary
     - Costing pack details UI screenshots
     - Audit visibility UI screenshots
     - Permission matrix documentation
     - SOPs documentation
     - Audit export verification

4. **API Endpoints:**
   - GET /api/v1/quotation/{id}/costing/breakdown - BOM/Feeder costing breakdown
   - GET /api/v1/quotation/{id}/costing/pivot/costhead - CostHead grouping pivot
   - GET /api/v1/quotation/{id}/costing/pivot/{type} - Pivot tables (category, make, series, rate source)
   - GET /api/v1/quotation/{id}/audit/timeline - Audit log timeline view
   - GET /api/v1/quotation/{id}/audit/details - Audit log details
   - GET /api/v1/quotation/{id}/audit/export - Audit export

5. **Frontend Components:**
   - Costing pack breakdown view component
   - CostHead grouping pivot component
   - Pivot tables component
   - Costing pack navigation component
   - Audit timeline view component
   - Audit details view component

6. **Backend Services:**
   - Costing pack details service (QCD/QCA integration)
   - Audit visibility service
   - Permission enforcement service (costing pack permissions)

7. **Documentation:**
   - `docs/PHASE_6/OPS/AUDIT_VISIBILITY_UI_DESIGN.md` - Audit visibility UI design document
   - `docs/PHASE_6/OPS/SOPs/` - Initial SOPs documentation directory
   - Permission matrix documentation

### Verification Checklist

- [ ] Verify scripts/run_week8_checks.sh exists
- [ ] Verify all test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify costing pack details use QCD/QCA only (P6-COST-005/006/007)
- [ ] Verify no duplicate calculators
- [ ] Verify permission enforcement works (P6-OPS-012)
- [ ] Verify audit visibility works (P6-OPS-008/009)
- [ ] Verify audit export works (P6-OPS-011)
- [ ] Verify SOPs created (P6-OPS-010)
- [ ] Verify evidence/PHASE6_WEEK8_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-8 runner
- [ ] Verify no schema changes introduced

---

## Decision Point

**Week-8 Closure Status:**
- ⏳ **PENDING COMPLETION** (Implementation required)

**Options:**
1. **"Close Week-8 and start Week-8.5 detailed plan"** - If costing pack details implemented, operations completion done, and permissions enforced
2. **"Complete Week-8 implementation"** - If costing pack details or operations completion still missing
3. **"Verify D0 Gate and proceed with Track D execution"** - If D0 Gate needs verification

**Note:** Week-8 consumes Week-7 foundations and assumes D0 Gate has passed. No new costing logic is introduced — only presentation, pivots, audit trails, and permission-aware visibility.

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-8 tasks)
- **D0 Gate Signoff:** Week-6 (P6-COST-D0-007) - must be passed before Track D execution
- **Week-7 Foundation:** Costing Pack Foundation (snapshot + panel summary) must be complete
- **QCD Contract v1.0:** (Week-0 governance pack - for QCD/QCA-only rule)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 10 | All captured from matrix |
| **Compliance Alarms** | 2 | 🔴 Must resolve |
| **High Priority Alarms** | 6 | 🟠 Should resolve |
| **Medium Priority Items** | 2 | 🟡 Can be deferred |
| **Completed Tasks** | 0 | None complete |
| **Missing Tasks** | 10 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-COSTING-DETAILS:** Implement costing pack details (P6-COST-005, 006, 007) - QCD/QCA only
- [ ] **ALARM-OPS-012:** Implement costing pack permissions enforcement (P6-OPS-012)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-COST-008:** Implement costing pack navigation (P6-COST-008)
- [ ] **ALARM-OPS-007:** Create audit visibility UI design document (P6-OPS-007)
- [ ] **ALARM-OPS-008:** Implement audit log display (P6-OPS-008)
- [ ] **ALARM-OPS-009:** Implement audit log details (P6-OPS-009)
- [ ] **ALARM-OPS-010:** Create initial SOPs (P6-OPS-010)
- [ ] **ALARM-OPS-011:** Implement audit export (P6-OPS-011)

### Documentation Tasks

- [ ] Complete costing pack details implementation (P6-COST-005/006/007/008)
- [ ] Complete operations completion implementation (P6-OPS-007/008/009/010/011/012)
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete
- [ ] Verify no schema changes introduced
- [ ] Verify QCD/QCA-only rule enforced

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After implementation

**Note:** Week-8 consumes Week-7 foundations and assumes D0 Gate has passed. No new costing logic is introduced — only presentation, pivots, audit trails, and permission-aware visibility. Week-8 does not do: Excel export (Week-10), global dashboard (Week-9), catalog governance (Week-6), new approval workflows (visibility only). All costing pack details must use QCD/QCA only (engine-first approach, no duplicate calculators).
