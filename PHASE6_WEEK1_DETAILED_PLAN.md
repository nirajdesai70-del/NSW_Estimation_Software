# Phase-6 Week-1 Detailed Plan

**Week:** Week-1 (Quotation & Panel UI + Customer Snapshot)  
**Status:** ⚠️ PARTIAL (Read APIs exist; snapshot + add panel missing)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-1 establishes the core quotation and panel management UI foundation. This includes quotation overview, panel details, and the critical "Add Panel" functionality. Week-1 also includes mandatory customer snapshot handling as a Phase-5 compliance obligation (D-009).

**Key Deliverables:**
- Quotation overview page (design + implementation)
- Panel details page (design + implementation)
- Add Panel functionality (API + UI)
- Customer snapshot handling (mandatory compliance - D-009)
- Customer ID nullable support

**Critical Alarms (From Matrix):**
- 🔴 **1 Compliance Alarm** (must resolve before Phase-6 closure)
  - ALARM-CUSTOMER-SNAPSHOT (P6-UI-001A/001B, P6-QUO-001A/B - D-009 obligation)
- 🔴 **1 Compliance Alarm** (ALARM-CRUD includes Week-1 Add Panel)
  - Add Panel functionality (P6-UI-005)
- 🟠 **2 High Priority Items** (design documentation)
- 🟡 **2 Medium Priority Items** (partial evidence, needs completion)

**Note:** Week-1 Scutwork Plan has been generated in canvas covering Add Panel API, customer snapshot enforcement, frontend modal, tests, and runner. This detailed plan aligns with the matrix and includes all tasks and alarms.

---

## Week-1 Task Breakdown

### Track: Quotation & Panel UI (Track A) + Customer Snapshot (Track E)

#### Track A - Quotation & Panel UI

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-001 | Design quotation overview page | `docs/PHASE_6/UI/QUOTATION_OVERVIEW_DESIGN.md` | ❌ MISSING | 🟠 | Design document with header, panel list, Add Panel button, navigation |
| P6-UI-002 | Implement quotation overview page | Route: `/quotation/{id}/v2`, View: `quotation/v2/index.blade.php` | ⚠️ PARTIAL | 🟡 | React pages exist but not stated as "full overview UI" |
| P6-UI-003 | Design panel details page | `docs/PHASE_6/UI/PANEL_DETAILS_DESIGN.md` | ❌ MISSING | 🟠 | Design document with panel header, feeder list, Add Feeder button |
| P6-UI-004 | Implement panel details page | Route: `/quotation/{id}/panel/{panelId}`, View: `quotation/v2/panel.blade.php` | ⚠️ PARTIAL | 🟡 | Partial view exists |
| P6-UI-005 | Implement add panel functionality | Route: `POST /quotation/{id}/panel`, Controller: `addPanel()` | ❌ MISSING | 🔴 **COMPLIANCE** | STUB exists; not implemented. Part of ALARM-CRUD (compliance) |

**Track A Status:** ⚠️ PARTIAL (Read APIs exist; Add Panel + design docs missing)

---

#### Track E - Customer Snapshot (Compliance Obligation - D-009)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-001A | Ensure customer_name_snapshot always stored (D-009) | Customer snapshot enforcement in quotation creation flow | ❌ MISSING | 🔴 **COMPLIANCE** | When creating quotation, always populate `customer_name_snapshot`. Part of ALARM-CUSTOMER-SNAPSHOT |
| P6-UI-001B | customer_id remains nullable (D-009) | Support nullable customer_id in quotation creation | ❌ MISSING | 🟠 | Ensure customer_id can be NULL. Support quotation creation without customer_id. Part of ALARM-CUSTOMER-SNAPSHOT |
| P6-QUO-001A | Customer snapshot handling (alternative task ID) | Same as P6-UI-001A | ❌ MISSING | 🔴 **COMPLIANCE** | Referenced in compliance alarms as P6-QUO-001A/B (same as P6-UI-001A) |
| P6-QUO-001B | Customer snapshot handling (alternative task ID) | Same as P6-UI-001B | ❌ MISSING | 🟠 | Referenced in compliance alarms as P6-QUO-001A/B (same as P6-UI-001B) |

**Track E Status:** ❌ MISSING (Compliance obligation - D-009, mandatory for Phase-6 sign-off)

---

## Week-1 Scutwork Plan Status

Based on the canvas document mentioned, the following implementation items should be covered:

### ✅ Scutwork Plan Coverage (From Canvas)

1. **Add Panel API** ✅
   - POST /api/v1/quotation/{quotation_id}/panels
   - **Alarm:** P6-UI-005 (Add Panel functionality) needs verification

2. **Customer Snapshot Enforcement Rules (D-009)** ✅
   - Customer snapshot enforcement rules
   - **Alarm:** P6-UI-001A/001B (customer snapshot) needs verification

3. **Frontend Add Panel Modal + Refresh List** ✅
   - Add Panel modal UI
   - List refresh after add
   - **Alarm:** P6-UI-005 (Add Panel UI) needs verification

4. **Tests** ✅
   - Add panel tests
   - Customer snapshot rules tests
   - **Alarm:** Test evidence needs verification

5. **Week-1 Runner + Evidence Pack** ✅
   - scripts/run_week1_checks.sh
   - evidence/PHASE6_WEEK1_EVIDENCE_PACK.md
   - **Alarm:** Runner and evidence pack need verification

6. **Closure Criteria** ✅
   - Week-1 closure requires UI + tests + evidence all green
   - **Status:** ⏳ PENDING (closure criteria defined but not met)

---

## Alarm Summary for Week-1

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-CUSTOMER-SNAPSHOT** | Review 1 (Finalized Review 4) | P6-UI-001A/001B, P6-QUO-001A/B | Customer snapshot handling (D-009 obligation) | ❌ MISSING | Implement customer_name_snapshot always stored + customer_id nullable support |
| **ALARM-CRUD** (Week-1 portion) | Review 1 (Finalized Review 4) | P6-UI-005 | Add Panel functionality missing | ❌ MISSING | Implement Add Panel API + UI (part of ALARM-CRUD compliance alarm) |

**Alarm Details:**

#### ALARM-CUSTOMER-SNAPSHOT (Compliance - D-009 Obligation)
- **Tasks Affected:** P6-UI-001A, P6-UI-001B, P6-QUO-001A/B (same tasks, different IDs)
- **Impact:** Phase-5 compliance obligation (D-009). Mandatory for Phase-6 sign-off.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (upgraded from Review 3, finalized in Review 4)
- **Resolution:** 
  - P6-UI-001A: Implement customer_name_snapshot always stored
    - When creating quotation, always populate `customer_name_snapshot`
    - If customer_id provided, copy customer name to snapshot
    - If customer_id NULL, use provided customer name for snapshot
  - P6-UI-001B: Ensure customer_id remains nullable
    - Support quotation creation without customer_id
    - Support future customer normalization
  - Integration with quotation creation flow
- **Notes:** This is a Phase-5 compliance obligation (D-009). Customer snapshot handling is mandatory, not optional. P6-QUO-001A/B are alternative task IDs for the same work (referenced in compliance alarms).

#### ALARM-CRUD (Week-1 Portion - Compliance)
- **Tasks Affected:** P6-UI-005 (Add Panel)
- **Impact:** Core functionality gap. Part of ALARM-CRUD compliance alarm (Weeks 1-2).
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - Implement Add Panel API: POST /quotation/{id}/panel
  - Implement Add Panel UI (modal + form)
  - Form validation
  - Database insert
  - Redirect to panel details
  - Refresh panel list after add
- **Notes:** STUB exists but not implemented. This is part of the broader ALARM-CRUD covering Add Panel/Feeder/BOM/Item (Weeks 1-2).

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-UI-001 | P6-UI-001 | Design quotation overview page | ❌ MISSING | Create design document: `docs/PHASE_6/UI/QUOTATION_OVERVIEW_DESIGN.md` |
| ALARM-UI-003 | P6-UI-003 | Design panel details page | ❌ MISSING | Create design document: `docs/PHASE_6/UI/PANEL_DETAILS_DESIGN.md` |

---

### 🟡 Medium Priority (Partial Evidence - Needs Completion)

These items have partial evidence but need completion.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| P6-UI-002 | Implement quotation overview page | ⚠️ PARTIAL | Complete implementation - React pages exist but not stated as "full overview UI". Need to verify it matches design requirements. |
| P6-UI-004 | Implement panel details page | ⚠️ PARTIAL | Complete implementation - Partial view exists. Need to verify it matches design requirements and includes all planned features. |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-1 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-UI-001 (Design quotation overview)
- ✅ P6-UI-002 (Implement quotation overview)
- ✅ P6-UI-003 (Design panel details)
- ✅ P6-UI-004 (Implement panel details)
- ✅ P6-UI-005 (Add Panel functionality)
- ✅ P6-UI-001A (customer_name_snapshot always stored)
- ✅ P6-UI-001B (customer_id nullable)

### ⚠️ Items Requiring Verification

The canvas scutwork plan is mentioned but needs verification that it covers:

1. **Add Panel API (P6-UI-005)**
   - Mentioned as POST /api/v1/quotation/{quotation_id}/panels
   - Need to verify API exists and is implemented
   - Current status: ❌ MISSING (STUB exists, not implemented)

2. **Customer Snapshot Enforcement (P6-UI-001A/001B)**
   - Mentioned as enforcement rules (D-009 obligation)
   - Need to verify implementation exists
   - Current status: ❌ MISSING (needs verification)

3. **Frontend Add Panel Modal (P6-UI-005)**
   - Mentioned as modal + refresh list
   - Need to verify UI exists
   - Current status: ❌ MISSING (needs verification)

4. **Tests**
   - Mentioned as test_add_panel.py and test_customer_snapshot_rules.py
   - Need to verify tests exist
   - Current status: ❌ MISSING (needs verification)

5. **Week-1 Runner**
   - Mentioned as scripts/run_week1_checks.sh
   - Need to verify script exists
   - Current status: ❌ MISSING (needs verification)

6. **Week-1 Evidence Pack**
   - Mentioned as evidence/PHASE6_WEEK1_EVIDENCE_PACK.md
   - Need to verify evidence pack exists
   - Current status: ❌ MISSING (needs verification)

---

## Week-1 Closure Criteria

### Required for Closure

1. ✅ **Scutwork Plan Created** (Structural completion)
2. ⏳ **Add Panel API Implemented** (P6-UI-005 backend)
3. ⏳ **Add Panel UI Implemented** (P6-UI-005 frontend)
4. ⏳ **Customer Snapshot Enforcement Implemented** (P6-UI-001A/001B)
5. ⏳ **All Tests Passing** (Add panel + customer snapshot tests)
6. ⏳ **Week-1 Runner Exists** (scripts/run_week1_checks.sh)
7. ⏳ **Week-1 Evidence Pack Complete** (evidence/PHASE6_WEEK1_EVIDENCE_PACK.md)
8. ⏳ **Design Documents Created** (P6-UI-001, P6-UI-003)
9. ⏳ **All Compliance Alarms Resolved** (2 compliance alarms)
10. ⏳ **UI Implementation Complete** (P6-UI-002, P6-UI-004 verified as complete)

### Current Closure Status

- **Structural Completion:** ✅ DONE (Scutwork plan created in canvas)
- **Implementation Status:** ⚠️ PARTIAL (Read APIs exist; Add Panel + customer snapshot missing)
- **Compliance Alarms:** ❌ 2 alarms need resolution (ALARM-CUSTOMER-SNAPSHOT, ALARM-CRUD Week-1 portion)
- **Formal Sign-off:** ⏳ PENDING

**Closure Rule (from canvas):** Week-1 is only closed when UI + tests + evidence are green.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Resolve Compliance Alarms (Blocking)

1. **ALARM-CUSTOMER-SNAPSHOT Resolution**
   - P6-UI-001A: Implement customer_name_snapshot always stored
     - When creating quotation, always populate `customer_name_snapshot`
     - If customer_id provided, copy customer name to snapshot
     - If customer_id NULL, use provided customer name for snapshot
   - P6-UI-001B: Ensure customer_id remains nullable
     - Support quotation creation without customer_id
     - Support future customer normalization
   - Integration with quotation creation flow
   - Tests: test_customer_snapshot_rules.py

2. **ALARM-CRUD Resolution (Week-1 Portion)**
   - P6-UI-005: Implement Add Panel functionality
     - Backend API: POST /api/v1/quotation/{quotation_id}/panels
     - Frontend: Add Panel modal + form
     - Form validation
     - Database insert
     - Redirect to panel details
     - Refresh panel list after add
   - Tests: test_add_panel.py

#### Priority 2: Verify Scutwork Plan Implementation

3. **Implementation Verification**
   - Verify Add Panel API exists and works
   - Verify Add Panel UI (modal) exists and works
   - Verify customer snapshot enforcement works
   - Verify tests exist and pass
   - Verify Week-1 runner exists and passes
   - Verify evidence pack exists and is complete

#### Priority 3: Complete Documentation

4. **Design Documents**
   - P6-UI-001: Create quotation overview design document
   - P6-UI-003: Create panel details design document

5. **Implementation Completion**
   - P6-UI-002: Verify quotation overview implementation is complete
   - P6-UI-004: Verify panel details implementation is complete

6. **Evidence Documentation**
   - Update Week-1 evidence pack with implementation proof
   - Document API endpoints and UI flows
   - Document test coverage

---

## Implementation Artifacts (From Canvas Scutwork Plan)

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week1_checks.sh` - Week-1 verification runner
     - Runs all Week-1 tests
     - Verifies API endpoints
     - Validates customer snapshot enforcement
     - Generates evidence summary

2. **Tests:**
   - `tests/quotation/test_add_panel.py` - Add Panel functionality tests
     - Test POST /api/v1/quotation/{quotation_id}/panels endpoint
     - Test panel creation with valid data
     - Test validation errors
     - Test panel list refresh after creation
   - `tests/quotation/test_customer_snapshot_rules.py` - Customer snapshot compliance tests
     - Test customer_name_snapshot always stored (P6-UI-001A)
     - Test customer_id nullable support (P6-UI-001B)
     - Test snapshot population from customer_id
     - Test snapshot with NULL customer_id

3. **Evidence:**
   - `evidence/PHASE6_WEEK1_EVIDENCE_PACK.md` - Week-1 evidence documentation
     - API endpoint documentation
     - Test results summary
     - UI screenshots/workflows
     - Compliance verification (D-009)

4. **API Endpoints:**
   - POST /api/v1/quotation/{quotation_id}/panels - Add Panel API
     - Request: { panel_name, qty, rate?, ... }
     - Response: { panel_id, ... }
     - Validation: panel_name required, qty > 0
     - Creates quotation_sale record

5. **Frontend Components:**
   - Add Panel modal component
     - Form fields: Panel Name, Qty, Rate (optional)
     - Validation feedback
     - Submit button
     - Cancel button
   - Panel list refresh functionality
     - Auto-refresh after panel creation
     - Update panel count
     - Navigate to new panel details

6. **Backend Services:**
   - Panel creation service
     - Handles panel creation logic
     - Validates input
     - Persists to database
     - Returns created panel data

7. **Database Changes:**
   - quotation_sales table (existing)
     - QuotationSaleId (auto-increment)
     - QuotationId (foreign key)
     - SaleCustomName (panel name)
     - Qty, Rate, Amount
   - quotations table (customer snapshot)
     - customer_name_snapshot (always populated)
     - customer_id (nullable)

### Verification Checklist

- [ ] Verify scripts/run_week1_checks.sh exists
- [ ] Verify tests/quotation/test_add_panel.py exists and passes
- [ ] Verify tests/quotation/test_customer_snapshot_rules.py exists and passes
- [ ] Verify POST /api/v1/quotation/{quotation_id}/panels endpoint exists
- [ ] Verify Add Panel modal UI exists and works
- [ ] Verify customer snapshot enforcement works (P6-UI-001A/001B)
- [ ] Verify evidence/PHASE6_WEEK1_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-1 runner
- [ ] Verify UI + tests + evidence are all green (closure criteria)

---

## Decision Point

**Week-1 Closure Status:**
- ⏳ **PENDING COMPLETION**

**Options:**
1. **"Close Week-1 and start Week-2 detailed plan"** - If all implementation artifacts verified and tests passing
2. **"Verify Week-1 scutwork plan implementation"** - If artifacts need verification
3. **"Complete Week-1 implementation"** - If Add Panel or customer snapshot still missing

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-1 tasks)
- **Week-1 Scutwork Plan:** (Location needs verification - mentioned in canvas document)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 7 | All captured from matrix |
| **Compliance Alarms** | 2 | 🔴 Must resolve |
| **High Priority Alarms** | 2 | 🟠 Should resolve |
| **Medium Priority Items** | 2 | 🟡 Needs completion |
| **Completed Tasks** | 0 | None fully complete |
| **Partial Tasks** | 2 | ⚠️ PARTIAL (P6-UI-002, P6-UI-004) |
| **Missing Tasks** | 5 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-CUSTOMER-SNAPSHOT:** Implement customer_name_snapshot always stored + customer_id nullable (P6-UI-001A/001B)
- [ ] **ALARM-CRUD (Week-1 portion):** Implement Add Panel functionality (P6-UI-005 - API + UI)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-UI-001:** Create quotation overview design document (P6-UI-001)
- [ ] **ALARM-UI-003:** Create panel details design document (P6-UI-003)

### Documentation Tasks

- [ ] Complete quotation overview implementation verification (P6-UI-002)
- [ ] Complete panel details implementation verification (P6-UI-004)
- [ ] Verify Week-1 scutwork plan artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After scutwork plan implementation verification
