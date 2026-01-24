# Phase-6 Week-9 Detailed Plan

**Week:** Week-9 (Global Dashboard + Integration)  
**Status:** ❌ NOT STARTED (Planning only)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-9 is the first client-visible integration week after all internal foundations and the Week-8.5 Legacy Parity Gate. Its purpose is to integrate validated subsystems into one coherent, navigable experience and introduce global dashboards for management and review. This includes global dashboard design and implementation (margins, hit rates, cost drivers), dashboard filters, and integration testing (end-to-end quotation creation, catalog import, costing pack, cross-track integration, performance testing).

**Key Deliverables (Week-9 Core Closure):**
- Global Dashboard (Track D - margins, hit rates, cost drivers, dashboard filters)
- Integration Testing (Integration - end-to-end tests, cross-track integration, performance testing)

**Critical Alarms (From Matrix):**
- 🔴 **Compliance Alarms** (must resolve for Week-9 closure)
  - Global dashboard implementation (P6-COST-009..013)
  - Integration testing (P6-INT-001..006)
- 🟠 **High Priority Items** (design documentation, dashboard filters, performance testing)

**Note:** Week-9 does NOT change meaning. It integrates, visualizes, and aggregates only. Week-9 does not do: new costing logic, new pricing rules, Excel export (Week-10), new approval workflows, catalog governance changes. Week-9 CANNOT START unless Week-8.5 Gate = PASS.

---

## Week-9 Task Breakdown

### Track: Global Dashboard (Track D) + Integration (Integration Track)

#### Track D - Global Dashboard

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-COST-009 | Design global dashboard | `docs/PHASE_6/COSTING/GLOBAL_DASHBOARD_DESIGN.md` | ❌ MISSING | 🔴 **COMPLIANCE** | Design document for global dashboard (margins, hit rates, cost drivers, filters) |
| P6-COST-010 | Implement margins dashboard | Margins dashboard view | ❌ MISSING | 🔴 **COMPLIANCE** | Margins dashboard (quotation margins, margin trends, margin analysis) |
| P6-COST-011 | Implement hit rates dashboard | Hit rates dashboard view | ❌ MISSING | 🔴 **COMPLIANCE** | Hit rates dashboard (quotation hit rates, win/loss analysis). Hit rate = quotation status transitions (e.g., DRAFT → SENT → WON / LOST). Source: quotation status history (read-only) |
| P6-COST-012 | Implement cost drivers dashboard | Cost drivers dashboard view | ❌ MISSING | 🔴 **COMPLIANCE** | Cost drivers dashboard (cost driver analysis, cost breakdown trends) |
| P6-COST-013 | Implement dashboard filters | Dashboard filter controls | ❌ MISSING | 🟠 | Dashboard filters (date range, quotation status, filters for dashboard views) |

**Track D Status:** ❌ NOT STARTED (Global dashboard not implemented)

**Non-Negotiable Rules:**
- ✅ Dashboards read from existing services only
- ❌ No recompute
- ❌ No write APIs
- ❌ No schema changes
- ✅ Respect QCD/QCA-only costing
- ✅ Respect locking & approval semantics
- ✅ Dashboards are read-only

---

#### Integration Track - Integration Testing

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-INT-001 | End-to-end quotation creation test | End-to-end quotation creation test suite | ❌ MISSING | 🔴 **COMPLIANCE** | End-to-end test for quotation creation workflow (create quotation, add panel, add feeder, add BOM, add items, pricing, resolution) |
| P6-INT-002 | End-to-end catalog import test | End-to-end catalog import test suite | ❌ MISSING | 🔴 **COMPLIANCE** | End-to-end test for catalog import workflow (import catalog, validation, approval) |
| P6-INT-003 | Integration testing | Integration test suite | ❌ MISSING | 🔴 **COMPLIANCE** | Integration testing (cross-module integration, service integration, API integration) |
| P6-INT-004 | Cross-track integration | Cross-track integration test suite | ❌ MISSING | 🔴 **COMPLIANCE** | Cross-track integration testing (Track A + Track D, Track B + Track D, etc.) |
| P6-INT-005 | Performance testing | Performance test suite | ❌ MISSING | 🟠 | Performance testing (dashboard query response times, integration workflows only). Does NOT tune infra or refactor queries (scope fence: performance tests validate only, no infra optimization) |
| P6-INT-006 | End-to-end costing pack test | End-to-end costing pack test suite | ❌ MISSING | 🔴 **COMPLIANCE** | End-to-end test for costing pack workflow (snapshot, panel summary, breakdown, pivots, navigation) |

**Integration Track Status:** ❌ NOT STARTED (Integration testing not implemented)

**Week-9 Scope Limit:** Integration testing focuses on end-to-end workflows and cross-track integration. Performance testing is included but not blocking.

---

## Alarm Summary for Week-9

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-GLOBAL-DASHBOARD** | Review 1 (Finalized Review 4) | P6-COST-009..012 | Missing global dashboard implementation (margins, hit rates, cost drivers) | ❌ MISSING | Implement global dashboard (margins, hit rates, cost drivers) - read-only, QCD/QCA only |
| **ALARM-INTEGRATION-TESTING** | Review 1 (Finalized Review 4) | P6-INT-001..004, P6-INT-006 | Missing integration testing (end-to-end tests, cross-track integration) | ❌ MISSING | Implement integration testing (end-to-end quotation creation, catalog import, costing pack, cross-track integration) |

**Alarm Details:**

#### ALARM-GLOBAL-DASHBOARD (Compliance - Global Dashboard Implementation)

- **Tasks Affected:** P6-COST-009 (Design), P6-COST-010 (Margins), P6-COST-011 (Hit rates), P6-COST-012 (Cost drivers)
- **Impact:** Compliance requirement. Global dashboard must be implemented for management visibility and KPIs.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-COST-009: Design global dashboard
    - Design document for global dashboard
    - Margins, hit rates, cost drivers, filters design
  - P6-COST-010: Implement margins dashboard
    - Margins dashboard view (quotation margins, margin trends, margin analysis)
    - Read-only, QCD/QCA only
  - P6-COST-011: Implement hit rates dashboard
    - Hit rates dashboard view (quotation hit rates, win/loss analysis)
    - Hit rate = quotation status transitions (e.g., DRAFT → SENT → WON / LOST)
    - Source: quotation status history (read-only)
    - Read-only, QCD/QCA only
  - P6-COST-012: Implement cost drivers dashboard
    - Cost drivers dashboard view (cost driver analysis, cost breakdown trends)
    - Read-only, QCD/QCA only
- **Notes:** All dashboards must be read-only. Must respect QCD/QCA-only costing. Must respect locking & approval semantics. No recompute, no write APIs, no schema changes.

#### ALARM-INTEGRATION-TESTING (Compliance - Integration Testing)

- **Tasks Affected:** P6-INT-001 (Quotation creation), P6-INT-002 (Catalog import), P6-INT-003 (Integration testing), P6-INT-004 (Cross-track integration), P6-INT-006 (Costing pack)
- **Impact:** Compliance requirement. Integration testing must be implemented for system validation and regression prevention.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-INT-001: End-to-end quotation creation test
    - Test quotation creation workflow (create quotation, add panel, add feeder, add BOM, add items, pricing, resolution)
  - P6-INT-002: End-to-end catalog import test
    - Test catalog import workflow (import catalog, validation, approval)
  - P6-INT-003: Integration testing
    - Cross-module integration, service integration, API integration
  - P6-INT-004: Cross-track integration
    - Cross-track integration testing (Track A + Track D, Track B + Track D, etc.)
  - P6-INT-006: End-to-end costing pack test
    - Test costing pack workflow (snapshot, panel summary, breakdown, pivots, navigation)
- **Notes:** Integration testing focuses on end-to-end workflows and cross-track integration. Performance testing (P6-INT-005) is included but not blocking.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-COST-013 | P6-COST-013 | Implement dashboard filters | ❌ MISSING | Implement dashboard filters (date range, quotation status, filters for dashboard views) |
| ALARM-INT-005 | P6-INT-005 | Performance testing | ❌ MISSING | Implement performance testing (dashboard query response times, integration workflows only). Does NOT tune infra or refactor queries (scope fence: performance tests validate only, no infra optimization) |

---

### 🟡 Medium Priority (Non-Critical Enhancements)

These items are enhancements and not blocking Phase-6 closure.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| Advanced dashboard features | Advanced dashboard features | ⏳ DEFERRED | Advanced dashboard features (can be added later) |
| Enhanced integration testing | Enhanced integration testing features | ⏳ DEFERRED | Enhanced integration testing features (can be added later) |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-9 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-COST-009..013 (Global Dashboard - 5 tasks)
- ✅ P6-INT-001..006 (Integration Testing - 6 tasks)

### ⚠️ Items Requiring Verification

1. **Global Dashboard Implementation (P6-COST-009..013)**
   - Need to verify margins dashboard uses QCD/QCA only
   - Need to verify hit rates dashboard uses QCD/QCA only
   - Need to verify cost drivers dashboard uses QCD/QCA only
   - Need to verify dashboards are read-only
   - Need to verify dashboard filters work
   - Current status: ❌ NOT STARTED (needs verification)

2. **Integration Testing Implementation (P6-INT-001..006)**
   - Need to verify end-to-end quotation creation test works
   - Need to verify end-to-end catalog import test works
   - Need to verify integration testing works
   - Need to verify cross-track integration works
   - Need to verify performance testing works
   - Need to verify end-to-end costing pack test works
   - Current status: ❌ MISSING (needs verification)

---

## Hard Preconditions (Non-Negotiable)

Week-9 CANNOT START unless:
1. ✅ Week-8.5 Gate = PASS
2. ✅ No open parity alarms (editability, guardrails)
3. ✅ No canon violations pending
4. ✅ D0 Gate already passed (Week-6)

If any condition fails → return to originating week, not patch here.

---

## Week-9 Closure Criteria

### Required for Closure

1. ⏳ **Week-8.5 Gate PASSED** (Hard precondition)
   - Week-8.5 gate must pass before Week-9 can start
   - No open parity alarms
   - No canon violations pending
2. ⏳ **Global Dashboard Implemented** (P6-COST-009..012)
   - Margins dashboard (read-only, QCD/QCA only)
   - Hit rates dashboard (read-only, QCD/QCA only)
   - Cost drivers dashboard (read-only, QCD/QCA only)
   - All dashboards respect locking & approval semantics
3. ⏳ **Dashboard Filters Implemented** (P6-COST-013)
   - Dashboard filter controls (date range, quotation status, filters)
4. ⏳ **Integration Testing Implemented** (P6-INT-001..004, P6-INT-006)
   - End-to-end quotation creation test
   - End-to-end catalog import test
   - Integration testing
   - Cross-track integration
   - End-to-end costing pack test
5. ⏳ **Performance Testing Implemented** (P6-INT-005)
   - Performance test suite (load testing, response time testing, scalability testing)
6. ⏳ **All Tests Passing** (Integration tests + Performance tests)
7. ⏳ **Design Documents Created** (P6-COST-009)
8. ⏳ **All Compliance Alarms Resolved** (2 compliance alarms)
9. ⏳ **No Schema Changes Introduced** (scope guard)
10. ⏳ **QCD/QCA Only Rule Enforced** (no duplicate calculators)
11. ⏳ **Dashboards Read-Only** (no write APIs, no recompute)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ❌ NOT STARTED (Week-8.5 gate must pass first)
- **Precondition Status:** ⏳ PENDING (Week-8.5 gate must pass)
- **Compliance Alarms:** ❌ 2 alarms need resolution (ALARM-GLOBAL-DASHBOARD, ALARM-INTEGRATION-TESTING)
- **Formal Sign-off:** ⏳ PENDING

**Closure Rule:** Week-9 is CLOSED only if Week-8.5 gate passes, global dashboard is implemented (read-only, QCD/QCA only), and integration testing is complete. Week-9 does NOT change meaning - it integrates, visualizes, and aggregates only.

---

## Dependencies

### Requires (Execution)

- **Week-8.5:** Legacy Parity Gate must PASS (hard precondition - Week-9 cannot start without this)
- **Week-8:** Costing Pack Details must be complete (for costing pack integration testing)
- **Week-7:** Costing Pack Foundation must be complete (for global dashboard)
- **Week-6:** D0 Gate must be passed (for costing pack foundation)
- **Week-3-6:** All foundational tracks must be complete (for integration testing)

### Can Run in Parallel (Planning / Scaffolding)

- **Design:** Global dashboard design can proceed in parallel (but execution blocked until Week-8.5 gate passes)

### Blocks

- **Week-10:** Excel Export depends on global dashboard foundation
- **Week-11-12:** Final phases depend on integration testing completion

---

## Risks & Mitigations

### Risk 1: Global Dashboard Uses Ad-Hoc Calculations (Violates QCD/QCA-Only Rule)

**Mitigation:** Enforce QCD/QCA-only rule. Add test that forbids other sources. All dashboards must source data from QCD+QCA only (no duplicate calculators). Dashboards are read-only.

### Risk 2: Integration Testing Incomplete Causes Regression Risk

**Mitigation:** Integration testing must cover all end-to-end workflows. Cross-track integration testing required. Performance testing included but not blocking.

### Risk 3: Schema Changes Introduced

**Mitigation:** No schema changes allowed. Use existing schema only. Scope guard: no schema changes.

### Risk 4: Dashboard Write APIs Introduced

**Mitigation:** Dashboards must be strictly read-only. No write APIs, no recompute. Explicit deny-by-default for write operations.

### Risk 5: Scope Creep into Approval Workflows or Catalog Governance

**Mitigation:** Explicit non-goals defined. Week-9 does not do: new approval workflows, catalog governance changes, Excel export (Week-10). Scope guard: integration and visualization only.

### Risk 6: Week-9 Started Before Week-8.5 Gate Passes

**Mitigation:** Hard precondition check. Week-9 CANNOT START unless Week-8.5 Gate = PASS. If any precondition fails, return to originating week, not patch here.

---

## Next Steps

### Immediate Actions Required

#### Priority 0: Verify Week-8.5 Gate Passed (Hard Precondition)

0. **Week-8.5 Gate Verification**
   - Verify Week-8.5 gate PASSED
   - Verify no open parity alarms (editability, guardrails)
   - Verify no canon violations pending
   - Verify D0 Gate passed (Week-6)
   - Week-9 cannot start until this precondition is met

#### Priority 1: Implement Global Dashboard (After Week-8.5 Gate Passes)

1. **Global Dashboard Implementation (Track D)**
   - P6-COST-009: Create global dashboard design document
   - P6-COST-010: Implement margins dashboard (read-only, QCD/QCA only)
   - P6-COST-011: Implement hit rates dashboard (read-only, QCD/QCA only)
   - P6-COST-012: Implement cost drivers dashboard (read-only, QCD/QCA only)
   - P6-COST-013: Implement dashboard filters
   - Tests: test_global_dashboard.py, test_dashboard_filters.py
   - Verify QCD/QCA-only rule (no duplicate calculators)
   - Verify dashboards are read-only

#### Priority 2: Implement Integration Testing (Can Proceed in Parallel)

2. **Integration Testing Implementation (Integration Track)**
   - P6-INT-001: Implement end-to-end quotation creation test
   - P6-INT-002: Implement end-to-end catalog import test
   - P6-INT-003: Implement integration testing
   - P6-INT-004: Implement cross-track integration testing
   - P6-INT-005: Implement performance testing
   - P6-INT-006: Implement end-to-end costing pack test
   - Tests: test_integration_quotation.py, test_integration_catalog.py, test_integration_costing.py, test_cross_track_integration.py, test_performance.py

#### Priority 3: Verification

3. **Implementation Verification**
   - Verify global dashboard uses QCD/QCA only
   - Verify dashboards are read-only
   - Verify integration testing works
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week9_checks.sh` - Week-9 verification runner
     - Runs all Week-9 tests (global dashboard + integration)
     - Verifies API endpoints
     - Validates global dashboard functionality (QCD/QCA-only rule)
     - Validates integration testing
     - Validates performance testing
     - Generates evidence summary

2. **Tests:**
   - `tests/dashboard/test_global_dashboard.py` - Global dashboard tests
     - Test margins dashboard (read-only, QCD/QCA only)
     - Test hit rates dashboard (read-only, QCD/QCA only)
     - Test cost drivers dashboard (read-only, QCD/QCA only)
     - Test QCD/QCA-only rule (no duplicate calculators)
     - Test dashboards are read-only
   - `tests/dashboard/test_dashboard_filters.py` - Dashboard filter tests
     - Test dashboard filters (date range, quotation status, filters)
   - `tests/integration/test_quotation_creation.py` - End-to-end quotation creation test
     - Test quotation creation workflow (create quotation, add panel, add feeder, add BOM, add items, pricing, resolution)
   - `tests/integration/test_catalog_import.py` - End-to-end catalog import test
     - Test catalog import workflow (import catalog, validation, approval)
   - `tests/integration/test_costing_pack.py` - End-to-end costing pack test
     - Test costing pack workflow (snapshot, panel summary, breakdown, pivots, navigation)
   - `tests/integration/test_cross_track.py` - Cross-track integration tests
     - Test cross-track integration (Track A + Track D, Track B + Track D, etc.)
   - `tests/integration/test_performance.py` - Performance tests
     - Load testing, response time testing, scalability testing

3. **Evidence:**
   - `evidence/PHASE6_WEEK9_EVIDENCE_PACK.md` - Week-9 evidence documentation
     - API endpoint documentation
     - Test results summary
     - Global dashboard UI screenshots
     - Integration testing results
     - Performance testing results

4. **API Endpoints:**
   - GET /api/v1/dashboard/overview - Dashboard overview
   - GET /api/v1/dashboard/margins - Margins dashboard
   - GET /api/v1/dashboard/hit-rates - Hit rates dashboard
   - GET /api/v1/dashboard/cost-drivers - Cost drivers dashboard
   - GET /api/v1/dashboard/filters - Dashboard filters

5. **Frontend Components:**
   - Global dashboard overview component
   - Margins dashboard component
   - Hit rates dashboard component
   - Cost drivers dashboard component
   - Dashboard filters component

6. **Backend Services:**
   - Global dashboard service (QCD/QCA integration)
   - Integration test framework

7. **Documentation:**
   - `docs/PHASE_6/COSTING/GLOBAL_DASHBOARD_DESIGN.md` - Global dashboard design document
   - Integration testing documentation

### Verification Checklist

- [ ] Verify scripts/run_week9_checks.sh exists
- [ ] Verify all test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify Week-8.5 gate passed (hard precondition)
- [ ] Verify global dashboard uses QCD/QCA only (P6-COST-010/011/012)
- [ ] Verify no duplicate calculators
- [ ] Verify dashboards are read-only
- [ ] Verify integration testing works (P6-INT-001/002/003/004/006)
- [ ] Verify performance testing works (P6-INT-005)
- [ ] Verify evidence/PHASE6_WEEK9_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-9 runner
- [ ] Verify no schema changes introduced

---

## Decision Point

**Week-9 Closure Status:**
- ⏳ **PENDING COMPLETION** (Week-8.5 gate must pass first)

**Options:**
1. **"Close Week-9 and start Week-10 detailed plan"** - If Week-8.5 gate passed, global dashboard implemented, and integration testing complete
2. **"Complete Week-9 implementation"** - If global dashboard or integration testing still missing
3. **"Verify Week-8.5 gate and proceed"** - If Week-8.5 gate needs verification

**Note:** Week-9 does NOT change meaning - it integrates, visualizes, and aggregates only. Week-9 CANNOT START unless Week-8.5 Gate = PASS. All dashboards must be read-only and use QCD/QCA only.

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-9 tasks)
- **Week-8.5 Gate:** Legacy Parity Verification Gate - must PASS before Week-9 can start
- **D0 Gate Signoff:** Week-6 (P6-COST-D0-007) - must be passed
- **QCD Contract v1.0:** (Week-0 governance pack - for QCD/QCA-only rule)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 11 | All captured from matrix |
| **Compliance Alarms** | 2 | 🔴 Must resolve |
| **High Priority Alarms** | 2 | 🟠 Should resolve |
| **Medium Priority Items** | 2 | 🟡 Can be deferred |
| **Completed Tasks** | 0 | None complete |
| **Missing Tasks** | 11 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-GLOBAL-DASHBOARD:** Implement global dashboard (P6-COST-009..012) - read-only, QCD/QCA only
- [ ] **ALARM-INTEGRATION-TESTING:** Implement integration testing (P6-INT-001..004, P6-INT-006)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-COST-013:** Implement dashboard filters (P6-COST-013)
- [ ] **ALARM-INT-005:** Implement performance testing (P6-INT-005)

### Documentation Tasks

- [ ] Complete global dashboard implementation (P6-COST-009..013)
- [ ] Complete integration testing implementation (P6-INT-001..006)
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete
- [ ] Verify no schema changes introduced
- [ ] Verify QCD/QCA-only rule enforced
- [ ] Verify dashboards are read-only
- [ ] Verify Week-8.5 gate passed (hard precondition)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After Week-8.5 gate passes and implementation

**Note:** Week-9 does NOT change meaning - it integrates, visualizes, and aggregates only. Week-9 CANNOT START unless Week-8.5 Gate = PASS. All dashboards must be read-only and use QCD/QCA only. Week-9 does not do: new costing logic, new pricing rules, Excel export (Week-10), new approval workflows, catalog governance changes.
