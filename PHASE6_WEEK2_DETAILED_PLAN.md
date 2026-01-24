# Phase-6 Week-2 Detailed Plan

**Week:** Week-2 (Feeder/BOM Hierarchy UI + BOM Tracking + Reuse Workflows)  
**Status:** ⚠️ PARTIAL (Read APIs exist; CRUD + tracking + reuse missing)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-2 extends the quotation UI foundation with feeder and BOM hierarchy management. This includes Add Feeder, Add BOM, Add Items functionality, BOM tracking runtime behavior (compliance obligation), and reuse workflows with master BOM application. Week-2 also continues guardrails work from Track E.

**Key Deliverables:**
- Feeder/BOM hierarchy UI (design + implementation)
- Add Feeder functionality (API + UI)
- Add BOM functionality (API + UI)
- Add Items functionality (API + UI)
- BOM tracking runtime behavior (compliance - mandatory)
- Reuse workflows (master BOM apply + post-reuse editability)
- Guardrails continuation (Track E)

**Critical Alarms (From Matrix):**
- 🔴 **2 Compliance Alarms** (must resolve before Phase-6 closure)
  - ALARM-CRUD (Week-2 portion: Add Feeder, Add BOM, Add Items)
  - ALARM-BOM-TRACKING (P6-BOM-TRACK-001..003 - mandatory Week-2 compliance)
- 🔴 **1 Compliance Alarm** (ALARM-REUSE - master BOM apply + editability)
- 🟠 **High Priority Items** (design documentation, reuse validation)
- 🟡 **Medium Priority Items** (partial evidence, needs completion)

---

## Week-2 Task Breakdown

### Track: Feeder/BOM Hierarchy UI (Track A) + BOM Tracking (Track E) + Reuse (Track A-R) + Guardrails (Track E)

#### Track A - Feeder/BOM Hierarchy UI

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-006 | Design feeder/BOM hierarchy UI | `docs/PHASE_6/UI/FEEDER_BOM_HIERARCHY_DESIGN.md` | ❌ MISSING | 🟠 | Design document with feeder list, BOM tree, Add Feeder/BOM buttons, hierarchy visualization |
| P6-UI-007 | Implement feeder/BOM hierarchy UI | Route: `/quotation/{id}/panel/{panelId}/feeder/{feederId}`, View: `quotation/v2/feeder.blade.php` | ⚠️ PARTIAL | 🟡 | Partial view exists; needs completion |
| P6-UI-008 | Implement add feeder functionality | Route: `POST /quotation/{id}/panel/{panelId}/feeder`, Controller: `addFeeder()` | ❌ MISSING | 🔴 **COMPLIANCE** | STUB exists; not implemented. Part of ALARM-CRUD (compliance) |
| P6-UI-009 | Implement add BOM functionality | Route: `POST /quotation/{id}/panel/{panelId}/bom`, Controller: `addBom()` | ❌ MISSING | 🔴 **COMPLIANCE** | STUB exists; not implemented. Part of ALARM-CRUD (compliance) |
| P6-UI-010 | Implement add items functionality | Route: `POST /quotation/{id}/panel/{panelId}/bom/{bomId}/item`, Controller: `addItem()` | ⚠️ PARTIAL | 🔴 **COMPLIANCE** | Partial implementation exists; needs completion. Part of ALARM-CRUD (compliance) |

**Track A Status:** ⚠️ PARTIAL (Read APIs exist; Add Feeder/BOM/Items missing or incomplete)

---

#### Track E - BOM Tracking (Compliance Obligation - Mandatory Week-2)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-BOM-TRACK-001 | BOM tracking runtime behavior | Tracking fields runtime enforcement | ❌ MISSING | 🔴 **COMPLIANCE** | BOM tracking fields must be tracked at runtime. Part of ALARM-BOM-TRACKING |
| P6-BOM-TRACK-002 | BOM tracking validation | Tracking field validation rules | ❌ MISSING | 🔴 **COMPLIANCE** | Validation rules for tracking fields. Part of ALARM-BOM-TRACKING |
| P6-BOM-TRACK-003 | BOM tracking tests | Test suite for BOM tracking | ❌ MISSING | 🔴 **COMPLIANCE** | Test coverage for BOM tracking behavior. Part of ALARM-BOM-TRACKING |

**Track E (BOM Tracking) Status:** ❌ MISSING (Compliance obligation - mandatory Week-2, blocking Phase-6 sign-off)

---

#### Track A-R - Reuse Workflows

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-REUSE-001 | Master BOM apply workflow | Master BOM copy-to-quotation workflow | ⚠️ PARTIAL | 🔴 **COMPLIANCE** | Copy endpoints exist; master apply workflow missing. Part of ALARM-REUSE |
| P6-REUSE-002 | Post-reuse editability validation | Verify items remain editable after reuse | ❌ MISSING | 🔴 **COMPLIANCE** | Validation that reused items can be edited. Part of ALARM-REUSE |
| P6-REUSE-003 | Reuse guardrail validation | Guardrails applied after reuse | ❌ MISSING | 🟠 | Guardrails must validate reused items. Part of ALARM-REUSE |
| P6-REUSE-004 | Reuse workflow tests | Test suite for reuse workflows | ⚠️ PARTIAL | 🟡 | Reuse invariant tests exist; master apply + editability tests missing |

**Track A-R Status:** ⚠️ PARTIAL (Copy endpoints exist; master apply + editability validation missing)

---

#### Track E - Guardrails Continuation (Week 2-4)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-VAL-001 | Guardrails G1-G8 runtime enforcement | Runtime guardrail validation | ❌ MISSING | 🔴 **COMPLIANCE** | Guardrails G1-G8 must be enforced at runtime. Part of ALARM-GUARDRAILS (Week 2-4) |
| P6-VAL-002 | Guardrails error taxonomy mapping | Error taxonomy for guardrail violations | ❌ MISSING | 🔴 **COMPLIANCE** | Error taxonomy mapping for guardrails. Part of ALARM-GUARDRAILS |
| P6-VAL-003 | Guardrails test suite | Test coverage for guardrails | ❌ MISSING | 🔴 **COMPLIANCE** | Test suite for guardrails G1-G8. Part of ALARM-GUARDRAILS |
| P6-VAL-004 | Guardrails API parity | API parity for guardrail validation | ❌ MISSING | 🟠 | API endpoints for guardrail validation |

**Track E (Guardrails) Status:** ❌ MISSING (Compliance obligation - Weeks 2-4, blocking Phase-6 sign-off)

---

## Alarm Summary for Week-2

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-CRUD** (Week-2 portion) | Review 1 (Finalized Review 4) | P6-UI-008, P6-UI-009, P6-UI-010 | Add Feeder/BOM/Items functionality missing | ❌ MISSING | Implement Add Feeder, Add BOM, Add Items (API + UI) |
| **ALARM-BOM-TRACKING** | Review 3 (Finalized Review 4) | P6-BOM-TRACK-001..003 | BOM tracking runtime behavior (mandatory Week-2 compliance) | ❌ MISSING | Implement BOM tracking runtime enforcement + validation + tests |
| **ALARM-REUSE** | Review 1 (Finalized Review 4) | P6-REUSE-001, P6-REUSE-002 | Master BOM apply + post-reuse editability missing | ⚠️ PARTIAL | Implement master BOM apply workflow + editability validation |
| **ALARM-GUARDRAILS** (Week-2 portion) | Review 1 (Finalized Review 4) | P6-VAL-001..004 | Guardrails G1-G8 runtime + tests (Weeks 2-4) | ❌ MISSING | Implement guardrails runtime enforcement + error taxonomy + tests |

**Alarm Details:**

#### ALARM-CRUD (Week-2 Portion - Compliance)
- **Tasks Affected:** P6-UI-008 (Add Feeder), P6-UI-009 (Add BOM), P6-UI-010 (Add Items)
- **Impact:** Core functionality gap. Part of ALARM-CRUD compliance alarm (Weeks 1-2).
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-UI-008: Implement Add Feeder API + UI
    - API: POST /api/v1/quotation/{id}/panel/{panelId}/feeder
    - UI: Add Feeder modal + form
    - Form validation (feeder name, qty, etc.)
    - Database insert (quotation_sale_boms, Level=0)
    - Redirect to feeder details
  - P6-UI-009: Implement Add BOM API + UI
    - API: POST /api/v1/quotation/{id}/panel/{panelId}/bom
    - UI: Add BOM modal + form
    - Form validation (BOM name, parent BOM, level, etc.)
    - Database insert (quotation_sale_boms, Level>0)
    - Hierarchy management
  - P6-UI-010: Implement Add Items API + UI (complete partial implementation)
    - API: POST /api/v1/quotation/{id}/panel/{panelId}/bom/{bomId}/item
    - UI: Add Item modal + form
    - Form validation (product, qty, rate, etc.)
    - Database insert (quotation_sale_bom_items)
    - Product selection/autocomplete
- **Notes:** STUBs exist but not implemented. This is part of the broader ALARM-CRUD covering Add Panel/Feeder/BOM/Item (Weeks 1-2). P6-UI-010 has partial implementation, needs completion.

#### ALARM-BOM-TRACKING (Compliance - Mandatory Week-2)
- **Tasks Affected:** P6-BOM-TRACK-001, P6-BOM-TRACK-002, P6-BOM-TRACK-003
- **Impact:** Phase-5 compliance obligation. Mandatory Week-2 compliance, blocking Phase-6 sign-off.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (mandatory Week-2)
- **Resolution:** 
  - P6-BOM-TRACK-001: Implement BOM tracking runtime behavior
    - Track BOM creation/modification timestamps
    - Track BOM source (master/reuse/manual)
    - Track BOM modifications post-reuse
    - Runtime enforcement of tracking fields
  - P6-BOM-TRACK-002: Implement BOM tracking validation
    - Validation rules for tracking fields
    - Validation that tracking fields are populated
    - Validation that tracking fields are immutable after creation
  - P6-BOM-TRACK-003: Implement BOM tracking tests
    - Test tracking field population
    - Test tracking field validation
    - Test tracking field immutability
- **Notes:** This is a mandatory Week-2 compliance obligation. BOM tracking runtime behavior must be implemented for Phase-6 sign-off.

#### ALARM-REUSE (Compliance - Master BOM Apply + Editability)
- **Tasks Affected:** P6-REUSE-001 (Master BOM apply), P6-REUSE-002 (Post-reuse editability)
- **Impact:** Legacy parity requirement. Master BOM apply workflow and post-reuse editability are mandatory.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-REUSE-001: Implement master BOM apply workflow
    - Master BOM selection UI
    - Copy master BOM to quotation workflow
    - Apply master BOM to panel/feeder
    - Handle master BOM hierarchy (feeders, BOMs, items)
  - P6-REUSE-002: Implement post-reuse editability validation
    - Verify items remain editable after reuse
    - Verify items can be modified post-reuse
    - Verify guardrails apply to reused items
    - Test editability after reuse
- **Notes:** Copy endpoints exist (P6-REUSE-004 partial), but master BOM apply workflow and editability validation are missing. This is a compliance requirement for legacy parity.

#### ALARM-GUARDRAILS (Week-2 Portion - Compliance)
- **Tasks Affected:** P6-VAL-001, P6-VAL-002, P6-VAL-003, P6-VAL-004
- **Impact:** Phase-5 compliance obligation. Guardrails G1-G8 runtime enforcement is mandatory (Weeks 2-4).
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (Weeks 2-4)
- **Resolution:** 
  - P6-VAL-001: Implement guardrails G1-G8 runtime enforcement
    - Runtime validation for guardrails G1-G8
    - Guardrail violation detection
    - Guardrail violation blocking/prevention
  - P6-VAL-002: Implement guardrails error taxonomy mapping
    - Error taxonomy for guardrail violations
    - Error codes/categories for each guardrail
    - Error message mapping
  - P6-VAL-003: Implement guardrails test suite
    - Test coverage for each guardrail (G1-G8)
    - Test guardrail violation scenarios
    - Test guardrail enforcement
  - P6-VAL-004: Implement guardrails API parity
    - API endpoints for guardrail validation
    - API response format for guardrail violations
- **Notes:** Guardrails G1-G8 runtime enforcement is a Phase-5 compliance obligation. Must be implemented during Weeks 2-4 for Phase-6 sign-off.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-UI-006 | P6-UI-006 | Design feeder/BOM hierarchy UI | ❌ MISSING | Create design document: `docs/PHASE_6/UI/FEEDER_BOM_HIERARCHY_DESIGN.md` |
| ALARM-REUSE-003 | P6-REUSE-003 | Reuse guardrail validation | ❌ MISSING | Implement guardrail validation after reuse |
| ALARM-VAL-004 | P6-VAL-004 | Guardrails API parity | ❌ MISSING | Implement API endpoints for guardrail validation |

---

### 🟡 Medium Priority (Partial Evidence - Needs Completion)

These items have partial evidence but need completion.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| P6-UI-007 | Implement feeder/BOM hierarchy UI | ⚠️ PARTIAL | Complete implementation - Partial view exists. Need to verify it matches design requirements and includes all planned features. |
| P6-UI-010 | Implement add items functionality | ⚠️ PARTIAL | Complete implementation - Partial implementation exists. Need to verify it matches requirements and is fully functional. |
| P6-REUSE-004 | Reuse workflow tests | ⚠️ PARTIAL | Complete test suite - Reuse invariant tests exist; master apply + editability tests missing. |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-2 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-UI-006 (Design feeder/BOM hierarchy)
- ✅ P6-UI-007 (Implement feeder/BOM hierarchy)
- ✅ P6-UI-008 (Add Feeder)
- ✅ P6-UI-009 (Add BOM)
- ✅ P6-UI-010 (Add Items)
- ✅ P6-BOM-TRACK-001..003 (BOM tracking)
- ✅ P6-REUSE-001..004 (Reuse workflows)
- ✅ P6-VAL-001..004 (Guardrails continuation)

### ⚠️ Items Requiring Verification

1. **Add Feeder/BOM/Items APIs (P6-UI-008, P6-UI-009, P6-UI-010)**
   - Need to verify API endpoints exist and are implemented
   - Current status: ❌ MISSING (STUBs exist, not implemented)

2. **BOM Tracking Runtime (P6-BOM-TRACK-001..003)**
   - Need to verify tracking fields are enforced at runtime
   - Current status: ❌ MISSING (needs verification)

3. **Master BOM Apply Workflow (P6-REUSE-001)**
   - Need to verify master BOM apply workflow exists
   - Current status: ⚠️ PARTIAL (copy endpoints exist; master apply missing)

4. **Post-Reuse Editability (P6-REUSE-002)**
   - Need to verify items remain editable after reuse
   - Current status: ❌ MISSING (needs verification)

5. **Guardrails Runtime Enforcement (P6-VAL-001..004)**
   - Need to verify guardrails G1-G8 are enforced at runtime
   - Current status: ❌ MISSING (needs verification)

---

## Week-2 Closure Criteria

### Required for Closure

1. ⏳ **Add Feeder API Implemented** (P6-UI-008 backend)
2. ⏳ **Add Feeder UI Implemented** (P6-UI-008 frontend)
3. ⏳ **Add BOM API Implemented** (P6-UI-009 backend)
4. ⏳ **Add BOM UI Implemented** (P6-UI-009 frontend)
5. ⏳ **Add Items API Implemented** (P6-UI-010 backend - complete partial)
6. ⏳ **Add Items UI Implemented** (P6-UI-010 frontend - complete partial)
7. ⏳ **BOM Tracking Runtime Implemented** (P6-BOM-TRACK-001..003)
8. ⏳ **Master BOM Apply Workflow Implemented** (P6-REUSE-001)
9. ⏳ **Post-Reuse Editability Verified** (P6-REUSE-002)
10. ⏳ **Guardrails Runtime Enforcement Implemented** (P6-VAL-001..004)
11. ⏳ **All Tests Passing** (CRUD + tracking + reuse + guardrails tests)
12. ⏳ **Design Documents Created** (P6-UI-006)
13. ⏳ **All Compliance Alarms Resolved** (4 compliance alarms)
14. ⏳ **UI Implementation Complete** (P6-UI-007 verified as complete)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ⚠️ PARTIAL (Read APIs exist; CRUD + tracking + reuse missing)
- **Compliance Alarms:** ❌ 4 alarms need resolution (ALARM-CRUD, ALARM-BOM-TRACKING, ALARM-REUSE, ALARM-GUARDRAILS)
- **Formal Sign-off:** ⏳ PENDING

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Resolve Compliance Alarms (Blocking)

1. **ALARM-CRUD Resolution (Week-2 Portion)**
   - P6-UI-008: Implement Add Feeder API + UI
   - P6-UI-009: Implement Add BOM API + UI
   - P6-UI-010: Complete Add Items implementation (partial exists)
   - Tests: test_add_feeder.py, test_add_bom.py, test_add_item.py

2. **ALARM-BOM-TRACKING Resolution**
   - P6-BOM-TRACK-001: Implement BOM tracking runtime behavior
   - P6-BOM-TRACK-002: Implement BOM tracking validation
   - P6-BOM-TRACK-003: Implement BOM tracking tests
   - Integration with BOM creation/modification flows

3. **ALARM-REUSE Resolution**
   - P6-REUSE-001: Implement master BOM apply workflow
   - P6-REUSE-002: Implement post-reuse editability validation
   - Tests: test_master_bom_apply.py, test_post_reuse_editability.py

4. **ALARM-GUARDRAILS Resolution (Week-2 Portion)**
   - P6-VAL-001: Implement guardrails G1-G8 runtime enforcement
   - P6-VAL-002: Implement guardrails error taxonomy mapping
   - P6-VAL-003: Implement guardrails test suite
   - P6-VAL-004: Implement guardrails API parity

#### Priority 2: Complete Documentation

5. **Design Documents**
   - P6-UI-006: Create feeder/BOM hierarchy design document

6. **Implementation Completion**
   - P6-UI-007: Verify feeder/BOM hierarchy implementation is complete
   - P6-UI-010: Complete Add Items implementation
   - P6-REUSE-004: Complete reuse workflow tests

#### Priority 3: Verification

7. **Implementation Verification**
   - Verify all APIs exist and work
   - Verify all UI components exist and work
   - Verify BOM tracking enforcement works
   - Verify reuse workflows work
   - Verify guardrails enforcement works
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week2_checks.sh` - Week-2 verification runner
     - Runs all Week-2 tests (CRUD + tracking + reuse + guardrails)
     - Verifies API endpoints
     - Validates BOM tracking enforcement
     - Validates reuse workflows
     - Validates guardrails enforcement
     - Generates evidence summary

2. **Tests:**
   - `tests/quotation/test_add_feeder.py` - Add Feeder functionality tests
     - Test POST /api/v1/quotation/{id}/panel/{panelId}/feeder endpoint
     - Test feeder creation with valid data
     - Test validation errors
     - Test feeder list refresh after creation
   - `tests/quotation/test_add_bom.py` - Add BOM functionality tests
     - Test POST /api/v1/quotation/{id}/panel/{panelId}/bom endpoint
     - Test BOM creation with valid data
     - Test hierarchy management
     - Test validation errors
   - `tests/quotation/test_add_item.py` - Add Item functionality tests (complete partial)
     - Test POST /api/v1/quotation/{id}/panel/{panelId}/bom/{bomId}/item endpoint
     - Test item creation with valid data
     - Test product selection/autocomplete
     - Test validation errors
   - `tests/bom/test_bom_tracking.py` - BOM tracking compliance tests
     - Test tracking field population (P6-BOM-TRACK-001)
     - Test tracking field validation (P6-BOM-TRACK-002)
     - Test tracking field immutability
   - `tests/reuse/test_master_bom_apply.py` - Master BOM apply workflow tests
     - Test master BOM selection
     - Test master BOM copy to quotation
     - Test master BOM hierarchy application
   - `tests/reuse/test_post_reuse_editability.py` - Post-reuse editability tests
     - Test items remain editable after reuse
     - Test items can be modified post-reuse
     - Test guardrails apply to reused items
   - `tests/guardrails/test_guardrails_runtime.py` - Guardrails runtime enforcement tests
     - Test guardrails G1-G8 enforcement
     - Test guardrail violation detection
     - Test guardrail violation blocking/prevention

3. **Evidence:**
   - `evidence/PHASE6_WEEK2_EVIDENCE_PACK.md` - Week-2 evidence documentation
     - API endpoint documentation
     - Test results summary
     - UI screenshots/workflows
     - Compliance verification (BOM tracking, reuse, guardrails)

4. **API Endpoints:**
   - POST /api/v1/quotation/{id}/panel/{panelId}/feeder - Add Feeder API
     - Request: { feeder_name, qty, rate?, ... }
     - Response: { feeder_id, ... }
     - Validation: feeder_name required, qty > 0
     - Creates quotation_sale_boms record (Level=0)
   - POST /api/v1/quotation/{id}/panel/{panelId}/bom - Add BOM API
     - Request: { bom_name, parent_bom_id, level, qty?, ... }
     - Response: { bom_id, ... }
     - Validation: bom_name required, level > 0, parent_bom_id valid
     - Creates quotation_sale_boms record (Level>0)
   - POST /api/v1/quotation/{id}/panel/{panelId}/bom/{bomId}/item - Add Item API
     - Request: { product_id, qty, rate?, rate_source?, ... }
     - Response: { item_id, ... }
     - Validation: product_id required, qty > 0
     - Creates quotation_sale_bom_items record
   - POST /api/v1/quotation/{id}/panel/{panelId}/master-bom/apply - Master BOM Apply API
     - Request: { master_bom_id, ... }
     - Response: { applied_bom_id, ... }
     - Copies master BOM to quotation
   - GET /api/v1/quotation/{id}/panel/{panelId}/guardrails/validate - Guardrails Validation API
     - Response: { violations: [], ... }
     - Validates guardrails G1-G8

5. **Frontend Components:**
   - Add Feeder modal component
     - Form fields: Feeder Name, Qty, Rate (optional)
     - Validation feedback
     - Submit button
     - Cancel button
   - Add BOM modal component
     - Form fields: BOM Name, Parent BOM, Level, Qty (optional)
     - Validation feedback
     - Submit button
     - Cancel button
   - Add Item modal component
     - Form fields: Product (autocomplete), Qty, Rate, Rate Source
     - Validation feedback
     - Submit button
     - Cancel button
   - Feeder/BOM hierarchy tree component
     - Hierarchical display
     - Expand/collapse
     - Navigation
   - Master BOM selection component
     - Master BOM list
     - Selection UI
     - Apply button

6. **Backend Services:**
   - Feeder creation service
   - BOM creation service
   - Item creation service
   - BOM tracking service
   - Master BOM apply service
   - Guardrails validation service

7. **Database Changes:**
   - quotation_sale_boms table (existing)
     - QuotationSaleBomId (auto-increment)
     - QuotationSaleId (foreign key)
     - Level (0=Feeder, 1=BOM L1, 2=BOM L2)
     - ParentBomId (nullable, foreign key)
     - FeederName (for Level=0)
     - BomName (for Level>0)
     - Tracking fields (creation timestamp, source, etc.)
   - quotation_sale_bom_items table (existing)
     - QuotationSaleBomItemId (auto-increment)
     - QuotationSaleBomId (foreign key)
     - ProductId (foreign key)
     - Qty, Rate, RateSource, etc.

### Verification Checklist

- [ ] Verify scripts/run_week2_checks.sh exists
- [ ] Verify all test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify BOM tracking enforcement works (P6-BOM-TRACK-001..003)
- [ ] Verify master BOM apply workflow works (P6-REUSE-001)
- [ ] Verify post-reuse editability works (P6-REUSE-002)
- [ ] Verify guardrails enforcement works (P6-VAL-001..004)
- [ ] Verify evidence/PHASE6_WEEK2_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-2 runner
- [ ] Verify all compliance alarms resolved

---

## Decision Point

**Week-2 Closure Status:**
- ⏳ **PENDING COMPLETION**

**Options:**
1. **"Close Week-2 and start Week-3 detailed plan"** - If all implementation artifacts verified and tests passing
2. **"Verify Week-2 implementation"** - If artifacts need verification
3. **"Complete Week-2 implementation"** - If CRUD, tracking, reuse, or guardrails still missing

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-2 tasks)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 15 | All captured from matrix |
| **Compliance Alarms** | 4 | 🔴 Must resolve |
| **High Priority Alarms** | 3 | 🟠 Should resolve |
| **Medium Priority Items** | 3 | 🟡 Needs completion |
| **Completed Tasks** | 0 | None fully complete |
| **Partial Tasks** | 3 | ⚠️ PARTIAL (P6-UI-007, P6-UI-010, P6-REUSE-004) |
| **Missing Tasks** | 12 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-CRUD (Week-2 portion):** Implement Add Feeder, Add BOM, Add Items (P6-UI-008, P6-UI-009, P6-UI-010)
- [ ] **ALARM-BOM-TRACKING:** Implement BOM tracking runtime enforcement + validation + tests (P6-BOM-TRACK-001..003)
- [ ] **ALARM-REUSE:** Implement master BOM apply workflow + editability validation (P6-REUSE-001, P6-REUSE-002)
- [ ] **ALARM-GUARDRAILS (Week-2 portion):** Implement guardrails runtime enforcement + error taxonomy + tests (P6-VAL-001..004)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-UI-006:** Create feeder/BOM hierarchy design document (P6-UI-006)
- [ ] **ALARM-REUSE-003:** Implement reuse guardrail validation (P6-REUSE-003)
- [ ] **ALARM-VAL-004:** Implement guardrails API parity (P6-VAL-004)

### Documentation Tasks

- [ ] Complete feeder/BOM hierarchy implementation verification (P6-UI-007)
- [ ] Complete Add Items implementation (P6-UI-010)
- [ ] Complete reuse workflow tests (P6-REUSE-004)
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After implementation verification
