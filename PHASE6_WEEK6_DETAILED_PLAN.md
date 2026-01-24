# Phase-6 Week-6 Detailed Plan

**Week:** Week-6 (Error/Warning Surfacing + D0 Gate Signoff)  
**Status:** ⚠️ PARTIAL (Error/warning surfacing implementation exists; D0 Gate signoff pending)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-6 focuses on error and warning surfacing, D0 Gate signoff, and catalog governance. This includes price missing warnings, unresolved resolution warnings, validation error display, error summary panel, and user-friendly error messages. Week-6 also includes D0 Gate signoff and catalog governance work.

**Key Deliverables (Week-6 Core Closure):**
- Error/Warning Surfacing UX (Track A - warnings, validation errors, error summary)
- D0 Gate Signoff (Track D0 - QCD/QCA stable, costing engine foundations complete)

**Parallel Work (Not Closure-Blocking):**
- Catalog Governance (Track B - catalog governance enforcement) - Parallel work, not required for Week-6 closure
- Track E Continuation (discount editor, API contracts) - Parallel work, not required for Week-6 closure

**Critical Alarms (Week-6 Core Closure - From Matrix):**
- 🔴 **Compliance Items** (must resolve for Week-6 closure)
  - Error/warning surfacing UX (P6-UI-028..033)
  - D0 Gate signoff (P6-COST-D0-007 - gate blocker)

**Parallel Work Alarms (Not Closure-Blocking for Week-6):**
- 🟠 **High Priority Items** (Catalog governance, discount editor - parallel work)
- 🟡 **Medium Priority Items** (API contracts - deferable, performance hardening)

**Note:** Week-6 is "surfacing only" - must not introduce instability. Uses existing stored state only (rate_source, is_price_missing, resolution_status). Read-only surfacing, no logic changes.

---

## Week-6 Task Breakdown

### Track: Error/Warning Surfacing (Track A) + D0 Gate (Track D0) + Catalog Governance (Track B) + Track E Continuation

#### Track A - Error/Warning Surfacing UX

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-028 | Design error/warning surfacing UX | `docs/PHASE_6/UI/ERROR_WARNING_UX.md` | ❌ MISSING | 🟠 | Design document with error message display, warning message display, inline validation errors, summary error panel |
| P6-UI-029 | Implement price missing warnings | Warning detection + display (RateSource=PRICELIST but no price found) | ⚠️ PARTIAL | 🔴 **COMPLIANCE** | Detect missing prices, display warning icon, warning message, actionable guidance. Implementation exists but needs bug fixes |
| P6-UI-030 | Implement unresolved warnings | Warning detection + display (unresolved L0/L1/L2) | ⚠️ PARTIAL | 🔴 **COMPLIANCE** | Detect unresolved resolution, display warning icon, warning message, actionable guidance. Implementation exists but needs bug fixes |
| P6-UI-031 | Implement validation error display | Form validation errors + inline error messages + field-level indicators | ❌ MISSING | 🟠 | Form validation error display with inline messages and field-level indicators |
| P6-UI-032 | Implement error summary panel | Quotation-level error count + expandable error details + navigation | ⚠️ PARTIAL | 🟠 | Error summary panel with error counts at different levels. Implementation exists but needs bug fixes |
| P6-UI-033 | Implement user-friendly error messages | User-friendly error message formatting + actionable guidance | ⚠️ PARTIAL | 🟠 | User-friendly error messages with actionable guidance. Implementation exists |

**Track A Status:** ⚠️ PARTIAL (Error/warning surfacing implementation exists but needs bug fixes and completion)

**Scope Guard:** Week-6 is "surfacing only" - read-only, uses existing stored state only. No logic changes, no new constraints, no schema changes.

---

#### Track D0 - D0 Gate Signoff (Week 5-6 Continuation)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-COST-D0-004 | QCD Excel export (sheet-1 only) | QCD Excel export endpoint (sheet-1 only) | ❌ MISSING | 🔴 **COMPLIANCE** | QCD Excel export with sheet-1 only (per QCD contract). Part of D0 Gate requirements |
| P6-COST-D0-005 | Numeric validation vs Excel reference | Numeric validation against Excel reference | ❌ MISSING | 🔴 **COMPLIANCE** | Numeric validation to match Excel reference output. Part of D0 Gate requirements |
| P6-COST-D0-006 | Performance hardening for large quotations | Performance optimization for large quotations | ❌ MISSING | 🟠 | Performance hardening for large quotations (can be deferred if not blocking) |
| P6-COST-D0-011 | Implement cost sheet calculation engine | Cost sheet calculation engine implementation | ❌ MISSING | 🔴 **COMPLIANCE** | Cost sheet calculation engine. Part of D0 Gate requirements |
| P6-COST-D0-012 | Implement cost adder roll-up generator | Cost adder roll-up generator implementation | ❌ MISSING | 🔴 **COMPLIANCE** | Cost adder roll-up generator. Part of D0 Gate requirements |
| P6-COST-D0-014 | Update D0 Gate checklist (include cost adders) | D0 Gate checklist update | ❌ MISSING | 🔴 **COMPLIANCE** | Update D0 Gate checklist to include cost adders verification |
| P6-COST-D0-007 | D0 Gate signoff (QCD v1.0 + QCA v1.0 stable) | D0 Gate signoff documentation | ❌ MISSING | 🔴 **GATE** | D0 Gate signoff (QCD v1.0 + QCA v1.0 stable). Gate blocker - must pass for Track D to proceed |

**Track D0 Status:** ❌ MISSING (D0 Gate requirements not complete - gate blocker)

**Important:** D0 Gate is a gate blocker. Track D (Week-7 costing pack) cannot proceed until D0 Gate is signed off.

---

#### Track B - Catalog Governance (Week-6 Parallel Work - Not Closure-Blocking)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-CAT-013 | Design catalog governance UI | Catalog governance UI design document | ❌ MISSING | 🟠 | Design document for catalog governance UI (Parallel work, not required for Week-6 closure) |
| P6-CAT-014 | Implement catalog approval workflow | Catalog approval workflow implementation | ❌ MISSING | 🟠 | Catalog approval workflow implementation (Parallel work, not required for Week-6 closure) |
| P6-CAT-015 | Implement change tracking | Catalog change tracking implementation | ❌ MISSING | 🟠 | Catalog change tracking implementation (Parallel work, not required for Week-6 closure) |
| P6-CAT-016 | Implement governance enforcement | Catalog governance enforcement implementation | ❌ MISSING | 🟠 | Catalog governance enforcement implementation (Parallel work, not required for Week-6 closure) |

**Track B Status:** ❌ MISSING (Catalog governance not implemented - Parallel work, not required for Week-6 closure)

---

#### Track E Continuation (Week 3-6 Parallel Work - Not Closure-Blocking)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-DISC-001..004 | Discount Editor (legacy parity) | Discount editor implementation | ❌ MISSING | 🔴 **PARITY** | Discount editor for legacy parity (Week 3-6 scope, parallel work, not required for Week-6 closure) |
| P6-API-001..005 | API Contracts (optional/deferable) | API contract validation | ❌ MISSING | DEFER-ALLOWED | API contract validation (optional/deferable, parallel work, not required for Week-6 closure) |

**Track E Status:** ❌ MISSING (Discount editor + API contracts not implemented - Parallel work, not required for Week-6 closure)

---

## Alarm Summary for Week-6

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-ERROR-WARNING-UX** | Review 1 (Finalized Review 4) | P6-UI-028..033 | Error/warning surfacing UX missing | ⚠️ PARTIAL | Complete error/warning surfacing UX (bug fixes + completion) |
| **ALARM-D0-GATE** | Review 4 (Finalized Review 4) | P6-COST-D0-007, P6-COST-D0-004/005/011/012/014 | D0 Gate signoff (gate blocker) | ❌ MISSING | Complete D0 Gate requirements + signoff (QCD v1.0 + QCA v1.0 stable) |

**Alarm Details:**

#### ALARM-ERROR-WARNING-UX (Compliance)
- **Tasks Affected:** P6-UI-028..033
- **Impact:** Core functionality gap. Error/warning surfacing UX is mandatory for user feedback.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-UI-029: Implement price missing warnings (implementation exists, needs bug fixes)
    - Fix Pydantic mutable defaults (use Field(default_factory=list))
    - Fix indentation/syntax errors in service
    - Fix query column selection (remove non-existent columns)
    - Fix enum usage bugs in summary counts
    - Ensure deterministic tests (not skip-by-return)
  - P6-UI-030: Implement unresolved warnings (implementation exists, needs bug fixes)
    - Same bug fixes as P6-UI-029
  - P6-UI-032: Implement error summary panel (implementation exists, needs bug fixes)
    - Fix enum usage bugs in summary counts
    - Ensure stable warning schema
  - P6-UI-031: Implement validation error display (missing)
  - P6-UI-033: Implement user-friendly error messages (partial, needs completion)
- **Notes:** Week-6 is "surfacing only" - read-only, uses existing stored state only. No logic changes, no new constraints, no schema changes. Implementation exists but needs critical bug fixes before closure.

#### ALARM-D0-GATE (Gate Blocker)
- **Tasks Affected:** P6-COST-D0-007, P6-COST-D0-004, P6-COST-D0-005, P6-COST-D0-011, P6-COST-D0-012, P6-COST-D0-014
- **Impact:** Gate blocker. Track D (Week-7 costing pack) cannot proceed until D0 Gate is signed off.
- **Matrix Status:** Finalized in Review 4 as **GATE** alarm
- **Resolution:** 
  - P6-COST-D0-004: Implement QCD Excel export (sheet-1 only)
  - P6-COST-D0-005: Implement numeric validation vs Excel reference
  - P6-COST-D0-011: Implement cost sheet calculation engine
  - P6-COST-D0-012: Implement cost adder roll-up generator
  - P6-COST-D0-014: Update D0 Gate checklist (include cost adders)
  - P6-COST-D0-007: D0 Gate signoff (QCD v1.0 + QCA v1.0 stable)
- **Notes:** D0 Gate is a gate blocker. All D0 Gate requirements must be complete before signoff. Track D (Week-7) is blocked until D0 Gate passes.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-UI-028 | P6-UI-028 | Design error/warning surfacing UX | ❌ MISSING | Create design document: `docs/PHASE_6/UI/ERROR_WARNING_UX.md` |
| ALARM-UI-031 | P6-UI-031 | Implement validation error display | ❌ MISSING | Implement form validation error display |
| ALARM-UI-032 | P6-UI-032 | Implement error summary panel | ⚠️ PARTIAL | Complete error summary panel implementation (bug fixes) |
| ALARM-D0-006 | P6-COST-D0-006 | Performance hardening for large quotations | ❌ MISSING | Performance hardening (can be deferred if not blocking) |
| ALARM-CAT-013..016 | P6-CAT-013..016 | Catalog governance UI | ❌ MISSING | Implement catalog governance UI (4 tasks) |

---

### 🟡 Medium Priority / DEFER-ALLOWED

These items can be deferred with appropriate documentation.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| P6-API-001..005 | API Contracts (optional/deferable) | ❌ MISSING | API contract validation (DEFER-ALLOWED - needs memo at closure) |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-6 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-UI-028..033 (Error/Warning Surfacing UX - 6 tasks)
- ✅ P6-COST-D0-004..007, 011, 012, 014 (D0 Gate requirements - 7 tasks)
- ✅ P6-CAT-013..016 (Catalog Governance - 4 tasks)
- ✅ P6-DISC-001..004 (Discount Editor - parity)
- ✅ P6-API-001..005 (API Contracts - deferable)

### ⚠️ Items Requiring Verification

1. **Error/Warning Surfacing Implementation (P6-UI-029/030/032/033)**
   - Implementation exists but needs critical bug fixes
   - Need to verify bug fixes applied (Pydantic defaults, indentation, query columns, enum usage, tests)
   - Need to verify no Week-5 locking mixed into Week-6
   - Current status: ⚠️ PARTIAL (needs bug fixes)

2. **D0 Gate Requirements (P6-COST-D0-004/005/007/011/012/014)**
   - Need to verify D0 Gate requirements are complete
   - Need to verify D0 Gate signoff completed
   - Current status: ❌ MISSING (gate blocker)

3. **Catalog Governance (P6-CAT-013..016)**
   - Need to verify catalog governance implementation
   - Current status: ❌ MISSING (needs verification)

---

## Week-6 Closure Criteria

### Required for Closure (Week-6 Core Closure Gates)

**Gate A - Error/Warning Surfacing (P6-UI-028..033):**
1. ⏳ **Error/Warning Surfacing UX Complete**
   - Bug fixes applied (Pydantic defaults, indentation, query columns, enum usage)
   - Deterministic tests (not skip-by-return)
   - Stable warning schema
   - No Week-5 locking mixed into Week-6
   - Error summary panel implemented
   - request_id visibility
   - Taxonomy mapping alignment

**Gate B - D0 Gate Signoff (P6-COST-D0-007 + prerequisites):**
2. ⏳ **D0 Gate Requirements Complete** (P6-COST-D0-004/005/011/012/014)
3. ⏳ **D0 Gate Signoff Completed** (P6-COST-D0-007 - gate blocker)
   - QCD/QCA stable
   - Numeric validation
   - Performance acceptable
   - Checklist + signoff doc

**Cross-Cutting Requirements:**
4. ⏳ **All Tests Passing** (Error/warning + D0 Gate tests)
5. ⏳ **Design Documents Created** (P6-UI-028)
6. ⏳ **No Logic Changes Introduced** (Week-6 is surfacing only)
7. ⏳ **No Schema Changes Introduced** (read-only surfacing)
8. ⏳ **Uses Existing Stored State Only** (rate_source, is_price_missing, resolution_status)

**Note:** Catalog Governance (P6-CAT-013..016), Discount Editor (P6-DISC-001..004), and API Contracts (P6-API-001..005) are parallel work and NOT required for Week-6 closure.

### Current Closure Status

- **Structural Completion:** ⚠️ PARTIAL (Error/warning implementation exists but needs bug fixes)
- **Implementation Status:** ⚠️ PARTIAL (Error/warning surfacing partial; D0 Gate missing)
- **Compliance Alarms (Core Closure):** ⚠️ 2 alarms need resolution (ALARM-ERROR-WARNING-UX partial, ALARM-D0-GATE missing)
- **Formal Sign-off:** ⏳ PENDING (D0 Gate blocker)

**Closure Rule:** Week-6 is CLOSED only if:
- Gate A: Error/warning surfacing is complete (with bug fixes)
- Gate B: D0 Gate is signed off

Week-6 is "surfacing only" - no logic changes, no schema changes, read-only.

**Parallel Work:** Catalog Governance, Discount Editor, and API Contracts are parallel work and NOT required for Week-6 closure.

---

## Dependencies

### Requires

- **Week-3:** Pricing UX (for price missing warnings)
- **Week-4:** Resolution UX (for unresolved resolution warnings)
- **Week-3-6:** Costing Engine Foundations (for D0 Gate requirements)

### Blocks

- **Week-7:** Costing Pack (Track D) is blocked until D0 Gate signoff (P6-COST-D0-007)
- **Week-8.5:** Legacy Parity Gate may require error/warning surfacing verification

---

## Risks & Mitigations

### Risk 1: Week-6 Implementation Introduces Logic Changes (Violates "Surfacing Only")

**Mitigation:** Week-6 is "surfacing only" - read-only, uses existing stored state only. No logic changes, no new constraints, no schema changes. Verify implementation only reads existing fields (rate_source, is_price_missing, resolution_status).

### Risk 2: Week-5 Locking Mixed into Week-6 (Scope Violation)

**Mitigation:** Verify no Week-5 locking behavior introduced in Week-6. Week-6 is surfacing only. If delete endpoint with lock enforcement existed pre-Week-6, document it. If newly introduced, move to Week-5 plan.

### Risk 3: Critical Bug Fixes Not Applied (Runtime Errors)

**Mitigation:** Apply critical bug fixes before closure:
- Pydantic mutable defaults (use Field(default_factory=list))
- Indentation/syntax errors in service
- Query column selection (remove non-existent columns)
- Enum usage bugs in summary counts
- Deterministic tests (not skip-by-return)

### Risk 4: D0 Gate Blocking Week-7 (Gate Blocker)

**Mitigation:** D0 Gate (P6-COST-D0-007) is a gate blocker. All D0 Gate requirements must be complete before signoff. Track D (Week-7) cannot proceed until D0 Gate passes.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Apply Critical Bug Fixes (Blocking)

1. **Error/Warning Surfacing Bug Fixes**
   - Fix Pydantic mutable defaults (use Field(default_factory=list))
   - Fix indentation/syntax errors in ErrorWarningService
   - Fix query column selection (remove non-existent columns: generic_descriptor, defined_spec_json)
   - Fix enum usage bugs in summary counts (use "errors"/"warnings"/"info" keys, not ErrorSeverity.ERROR)
   - Ensure deterministic tests (not skip-by-return, create test fixtures)
   - Verify stable warning schema (consistent warning object shape)
   - Verify no Week-5 locking mixed into Week-6

#### Priority 2: Complete D0 Gate Requirements (Gate Blocker)

2. **D0 Gate Requirements Completion**
   - P6-COST-D0-004: Implement QCD Excel export (sheet-1 only)
   - P6-COST-D0-005: Implement numeric validation vs Excel reference
   - P6-COST-D0-011: Implement cost sheet calculation engine
   - P6-COST-D0-012: Implement cost adder roll-up generator
   - P6-COST-D0-014: Update D0 Gate checklist (include cost adders)
   - P6-COST-D0-007: D0 Gate signoff (QCD v1.0 + QCA v1.0 stable)

#### Priority 3: Complete Documentation

3. **Design Documents**
   - P6-UI-028: Create error/warning surfacing UX design document

4. **Implementation Completion**
   - P6-UI-031: Implement validation error display
   - P6-UI-033: Complete user-friendly error messages

#### Priority 4: Verification

5. **Implementation Verification**
   - Verify error/warning surfacing works (with bug fixes applied)
   - Verify D0 Gate requirements complete
   - Verify D0 Gate signoff completed
   - Verify no logic changes introduced
   - Verify no schema changes introduced
   - Verify uses existing stored state only
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week6_checks.sh` - Week-6 verification runner
     - Runs all Week-6 tests (error/warning + D0 Gate)
     - Verifies API endpoints
     - Validates error/warning surfacing functionality
     - Validates D0 Gate requirements
     - Generates evidence summary

2. **Tests:**
   - `tests/errors/test_price_missing_warning.py` - Price missing warning tests
     - Test price missing warning detection
     - Test warning display
     - Test actionable guidance
     - **Fix Required:** Deterministic tests (create test fixtures, not skip-by-return)
   - `tests/errors/test_unresolved_resolution_warning.py` - Unresolved resolution warning tests
     - Test unresolved resolution warning detection
     - Test warning display
     - Test actionable guidance
     - **Fix Required:** Deterministic tests (create test fixtures, not skip-by-return)
   - `tests/errors/test_error_summary_panel.py` - Error summary panel tests
     - Test error summary aggregation
     - Test error counts by severity
     - Test error counts by type
     - **Fix Required:** Fix enum usage bugs in summary counts
   - `tests/errors/test_validation_error_display.py` - Validation error display tests
     - Test form validation errors
     - Test inline error messages
     - Test field-level error indicators
   - `tests/errors/test_user_friendly_messages.py` - User-friendly error message tests
     - Test user-friendly error message formatting
     - Test actionable guidance
   - `tests/errors/test_error_taxonomy_mapping.py` - Error taxonomy mapping tests
     - Test error codes match taxonomy
     - Test error messages match taxonomy
     - Test request_id propagation
   - `tests/d0/test_qcd_excel_export.py` - QCD Excel export tests
     - Test QCD Excel export (sheet-1 only)
     - Test numeric validation vs Excel reference
   - `tests/d0/test_cost_sheet_calculation.py` - Cost sheet calculation tests
     - Test cost sheet calculation engine
   - `tests/d0/test_cost_adder_rollup.py` - Cost adder roll-up tests
     - Test cost adder roll-up generator

3. **Evidence:**
   - `evidence/PHASE6_WEEK6_EVIDENCE_PACK.md` - Week-6 evidence documentation
     - API endpoint documentation
     - Test results summary
     - Error/warning surfacing screenshots
     - D0 Gate signoff documentation
     - Bug fixes verification

4. **API Endpoints:**
   - GET /api/v1/quotation/{qid}/boms/{bom_id}/items - Get BOM items with warnings
   - GET /api/v1/quotation/{qid}/error-summary - Get error summary panel
   - GET /api/v1/quotation/{qid}/qcd/excel - QCD Excel export endpoint

5. **Frontend Components:**
   - Price missing warning component
   - Unresolved resolution warning component
   - Validation error display component
   - Error summary panel component
   - User-friendly error message component

6. **Backend Services:**
   - ErrorWarningService (error/warning detection and aggregation)
     - **Fix Required:** Fix Pydantic mutable defaults, indentation, query columns, enum usage
   - UserFriendlyMessagesService (error message formatting)
   - QCD Excel Export Service
   - Cost Sheet Calculation Service
   - Cost Adder Roll-up Service

7. **Documentation:**
   - `docs/PHASE_6/UI/ERROR_WARNING_UX.md` - Error/warning surfacing UX design document
   - `docs/PHASE_6/D0/D0_GATE_SIGNOFF.md` - D0 Gate signoff documentation

### Critical Bug Fixes Required (From Code Review)

1. **Pydantic Mutable Defaults**
   - **Issue:** `warnings: List[Dict[str, Any]] = []` (shared mutable default)
   - **Fix:** `warnings: List[Dict[str, Any]] = Field(default_factory=list)`
   - **Files:** BOMItemListItem schema, ErrorSummaryResponse schema

2. **Indentation/Syntax Errors**
   - **Issue:** Indentation errors in ErrorWarningService methods
   - **Fix:** Align code blocks properly
   - **Files:** `backend/app/services/error_warning_service.py`

3. **Query Column Selection**
   - **Issue:** Selecting non-existent columns (generic_descriptor, defined_spec_json)
   - **Fix:** Remove non-existent columns, use only: id, quotation_id, panel_id, bom_id, description, resolution_status, product_id
   - **Files:** ErrorWarningService query methods

4. **Enum Usage Bugs**
   - **Issue:** Using `ErrorSeverity.ERROR` as dictionary key instead of "errors"
   - **Fix:** Use string keys: "errors", "warnings", "info"
   - **Files:** ErrorWarningService summary aggregation

5. **Deterministic Tests**
   - **Issue:** Tests use skip-by-return (if not panels: return)
   - **Fix:** Create test fixtures, insert deterministic test data, assert warnings
   - **Files:** All error/warning test files

6. **Stable Warning Schema**
   - **Issue:** Warning object shape may drift
   - **Fix:** Define stable warning object shape: type, severity, message, actionable, item_id
   - **Files:** ErrorWarningService warning creation

7. **Week-5 Locking Mixed into Week-6**
   - **Issue:** Delete endpoint with lock enforcement may be new Week-6 code
   - **Fix:** Verify if endpoint existed pre-Week-6. If new, move to Week-5 plan. Week-6 is surfacing only.
   - **Files:** Delete endpoint implementation

### Verification Checklist

- [ ] Verify scripts/run_week6_checks.sh exists
- [ ] Verify all test files exist and pass (with bug fixes applied)
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify error/warning surfacing works (P6-UI-029/030/032/033 - with bug fixes)
- [ ] Verify validation error display works (P6-UI-031)
- [ ] Verify D0 Gate requirements complete (P6-COST-D0-004/005/007/011/012/014)
- [ ] Verify D0 Gate signoff completed (P6-COST-D0-007)
- [ ] Verify no logic changes introduced (Week-6 is surfacing only)
- [ ] Verify no schema changes introduced (read-only surfacing)
- [ ] Verify uses existing stored state only (rate_source, is_price_missing, resolution_status)
- [ ] Verify no Week-5 locking mixed into Week-6
- [ ] Verify evidence/PHASE6_WEEK6_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-6 runner
- [ ] Verify bug fixes applied (Pydantic defaults, indentation, query columns, enum usage, tests, warning schema)

---

## Decision Point

**Week-6 Closure Status:**
- ⏳ **PENDING COMPLETION** (Bug fixes + D0 Gate required)

**Options:**
1. **"Close Week-6 and start Week-7 detailed plan"** - If all bug fixes applied, D0 Gate signed off, and tests passing
2. **"Apply Week-6 bug fixes"** - If critical bug fixes need to be applied
3. **"Complete D0 Gate requirements"** - If D0 Gate requirements still missing

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-6 tasks)
- **Week-6 Evidence Pack:** `evidence/PHASE6_WEEK6_EVIDENCE_PACK.md` (Implementation evidence)
- **Week-6 Code Review Feedback:** (Critical bug fixes required)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"
- **QCD Contract v1.0:** (Week-0 governance pack - for D0 Gate verification)

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Week-6 Core Closure Tasks** | 13 | Error/Warning Surfacing + D0 Gate |
| **Parallel Work Tasks** | 9 | Catalog Governance + Discount Editor + API Contracts (not closure-blocking) |
| **Compliance Alarms (Core Closure)** | 2 | 🔴 Must resolve for Week-6 closure |
| **High Priority Alarms (Core Closure)** | 4 | 🟠 Should resolve (not blocking Week-6 closure) |
| **Parallel Work Alarms** | 3 | 🟠/🟡 Parallel work (not required for Week-6 closure) |
| **Completed Tasks (Partial)** | 4 | ⚠️ PARTIAL (P6-UI-029/030/032/033 - need bug fixes) |
| **Missing Tasks (Core Closure)** | 9 | ❌ MISSING (need implementation/verification) |
| **Missing Tasks (Parallel Work)** | 9 | ❌ MISSING (parallel work, not required for Week-6 closure) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-ERROR-WARNING-UX:** Complete error/warning surfacing UX with bug fixes (P6-UI-028..033)
  - [ ] Apply Pydantic mutable defaults fix
  - [ ] Fix indentation/syntax errors
  - [ ] Fix query column selection
  - [ ] Fix enum usage bugs
  - [ ] Ensure deterministic tests
  - [ ] Verify stable warning schema
  - [ ] Verify no Week-5 locking mixed into Week-6
- [ ] **ALARM-D0-GATE:** Complete D0 Gate requirements + signoff (P6-COST-D0-004/005/007/011/012/014)

### High Priority Alarms (Should Resolve - Not Closure-Blocking for Week-6)

- [ ] **ALARM-UI-028:** Create error/warning surfacing UX design document (P6-UI-028)
- [ ] **ALARM-UI-031:** Implement validation error display (P6-UI-031)
- [ ] **ALARM-UI-032:** Complete error summary panel (bug fixes) (P6-UI-032)
- [ ] **ALARM-D0-006:** Performance hardening (can be deferred if not blocking) (P6-COST-D0-006)

### Parallel Work (Not Required for Week-6 Closure)

- [ ] **ALARM-CAT-013..016:** Implement catalog governance UI (P6-CAT-013..016 - parallel work)
- [ ] **ALARM-DISC-001..004:** Implement discount editor (P6-DISC-001..004 - parallel work)
- [ ] **ALARM-API-001..005:** Implement API contracts (P6-API-001..005 - parallel work, deferable)

### Documentation Tasks

- [ ] Complete error/warning surfacing implementation (with bug fixes)
- [ ] Complete D0 Gate requirements
- [ ] Complete D0 Gate signoff
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete
- [ ] Verify no logic changes introduced (Week-6 is surfacing only)
- [ ] Verify no schema changes introduced (read-only surfacing)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After bug fixes applied and D0 Gate signoff

**Note:** Week-6 is "surfacing only" - read-only, uses existing stored state only. No logic changes, no new constraints, no schema changes. Critical bug fixes must be applied before closure. D0 Gate is a gate blocker - Track D (Week-7) cannot proceed until D0 Gate passes.
