# Phase-6 Week-5 Detailed Plan

**Week:** Week-5 (Locking Visibility + Catalog Validation)  
**Status:** ❌ NOT STARTED  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-5 focuses on locking behavior visibility and catalog validation. This includes visual indicators for locked items, lock status display, lock prevention UI, and catalog validation governance. Week-5 also includes track E canon verification for locking compliance.

**Key Deliverables:**
- Locking Visibility UX (Track A - lock status display, lock prevention UI, lock indicators)
- Catalog Validation (Track B - catalog validation governance)
- Canon Verification for Locking (Track E - compliance blocker)

**Critical Alarms (From Matrix):**
- 🔴 **Compliance Items** (must resolve before Phase-6 closure)
  - Locking visibility UX (P6-UI-023..027)
  - Canon verification for locking (P6-LOCK-000)
- 🟠 **High Priority Items** (catalog validation governance)
- 🟡 **Medium Priority Items** (UI polish, non-critical enhancements)

**Note:** Week-5 is about locking visibility and catalog validation. No schema changes allowed. Line-item locking only (per D-005 obligation).

---

## Week-5 Task Breakdown

### Track: Locking Visibility UX (Track A) + Catalog Validation (Track B) + Canon Verification (Track E)

#### Track A - Locking Visibility UX

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-023 | Design locking visibility UX | `docs/PHASE_6/UI/LOCKING_VISIBILITY_UX.md` | ❌ MISSING | 🟠 | Design document with visual indicators, lock status display, lock reason display, lock prevention UI |
| P6-UI-024 | Implement lock status display | UI component (visual lock icon, lock status badge, lock timestamp, lock reason tooltip) | ❌ MISSING | 🔴 **COMPLIANCE** | Lock status display with visual indicators. Part of locking visibility UX |
| P6-UI-025 | Implement lock prevention UI | UI component (disable edits for locked items, prevent modifications) | ❌ MISSING | 🔴 **COMPLIANCE** | Lock prevention UI that disables edits for locked items. Part of locking visibility UX |
| P6-UI-026 | Implement lock status summary | Panel/BOM/quotation level lock count and summary (lock status dashboard) | ❌ MISSING | 🟠 | Lock status summary at panel/BOM/quotation levels with lock count. Part of locking visibility UX |
| P6-UI-027 | Implement lock/unlock controls (admin) | Admin-only lock/unlock controls with confirmation dialogs and audit log | ❌ MISSING | 🟠 | Lock/unlock controls for admin users with confirmation dialogs and audit log entries |

**Track A Status:** ❌ MISSING (Locking visibility UX not implemented)

**Scope Guard:** Line-item locking only (D-005 obligation). No schema changes. Locking visibility only (not locking implementation).

---

#### Track B - Catalog Validation (Governance)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-CAT-009 | Design validation preview system | Validation preview system design document | ❌ MISSING | 🟠 | Design validation preview system for catalog validation |
| P6-CAT-010 | Implement pre-import validation | Pre-import validation implementation | ❌ MISSING | 🟠 | Implement pre-import validation for catalog items |
| P6-CAT-011 | Implement validation results display | Validation results display UI | ❌ MISSING | 🟠 | Implement UI for displaying validation results |
| P6-CAT-012 | Implement validation rule configuration | Validation rule configuration UI | ❌ MISSING | 🟠 | Implement UI for configuring validation rules |

**Track B Status:** ❌ MISSING (Catalog validation governance not implemented)

---

#### Track E - Canon Verification for Locking (Compliance Blocker)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-LOCK-000 | Verify no higher-level locking (schema + UI) | Verification doc (no is_locked fields on quote_boms/quote_panels/quotations, line-item only) | ❌ MISSING | 🔴 **COMPLIANCE** | Verify no higher-level locking introduced (no is_locked on BOM/panel/quotation levels, only at quote_bom_items level per D-005 obligation) |

**Track E Status:** ❌ MISSING (Canon verification for locking not completed - compliance blocker)

---

## Alarm Summary for Week-5

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-LOCKING-VISIBILITY** | Review 1 (Finalized Review 4) | P6-UI-023..027 | Locking visibility UX missing | ❌ MISSING | Implement lock status display + lock prevention UI + lock status summary + lock/unlock controls (admin) |
| **ALARM-LOCKING-CANON** | Review 1 (Finalized Review 4) | P6-LOCK-000 | Verify no higher-level locking missing | ❌ MISSING | Verify no higher-level locking introduced (schema + UI verification, line-item only per D-005 obligation) |

**Alarm Details:**

#### ALARM-LOCKING-VISIBILITY (Compliance)
- **Tasks Affected:** P6-UI-023, P6-UI-024, P6-UI-025, P6-UI-026, P6-UI-027
- **Impact:** Core functionality gap. Locking visibility UX is mandatory for quotation locking workflow.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-UI-024: Implement lock status display
    - Visual lock icon on locked items
    - Lock status badge
    - Lock timestamp display
    - Lock reason tooltip
  - P6-UI-025: Implement lock prevention UI
    - Disable edits for locked items
    - Prevent modifications to locked items
    - Show lock reason when edit attempted
  - P6-UI-026: Implement lock status summary
    - Panel-level lock count
    - BOM-level lock count
    - Quotation-level lock summary
    - Visual lock status dashboard
  - P6-UI-027: Implement lock/unlock controls (admin)
    - Unlock button (admin only)
    - Lock confirmation dialog
    - Unlock confirmation dialog
    - Audit log entry
- **Notes:** Locking visibility UX enables users to see which items are locked and prevents editing locked items. Line-item locking only (D-005 obligation).

#### ALARM-LOCKING-CANON (Compliance - Canon Verification)
- **Tasks Affected:** P6-LOCK-000
- **Impact:** Canon compliance verification. Locking behavior must comply with Schema Canon and D-005 obligation.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (compliance blocker)
- **Resolution:** 
  - P6-LOCK-000: Canon verification for locking
    - Verify no is_locked field on quote_boms (BOM level)
    - Verify no is_locked field on quote_panels (Panel level)
    - Verify no is_locked field on quotations (Quotation level)
    - Verify locking only at quote_bom_items level (line-item only)
    - Document locking scope per D-005 decision
- **Notes:** Canon verification ensures locking behavior is compliant with Schema Canon and Phase-5 obligations. This is a compliance blocker.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-UI-023 | P6-UI-023 | Design locking visibility UX | ❌ MISSING | Create design document: `docs/PHASE_6/UI/LOCKING_VISIBILITY_UX.md` |
| ALARM-CAT-009 | P6-CAT-009 | Design validation preview system | ❌ MISSING | Create validation preview system design document |
| ALARM-CAT-010 | P6-CAT-010 | Implement pre-import validation | ❌ MISSING | Implement pre-import validation for catalog items |
| ALARM-CAT-011 | P6-CAT-011 | Implement validation results display | ❌ MISSING | Implement UI for displaying validation results |
| ALARM-CAT-012 | P6-CAT-012 | Implement validation rule configuration | ❌ MISSING | Implement UI for configuring validation rules |

---

### 🟡 Medium Priority (Non-Critical Enhancements)

These items are enhancements and not blocking Phase-6 closure.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| UI Polish | Lock UI polish, animations | ⏳ DEFERRED | UI polish and animations (non-critical, can be deferred) |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-5 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-UI-023..027 (Locking Visibility UX - 5 tasks)
- ✅ P6-LOCK-000 (Canon verification for locking)
- ✅ P6-CAT-009..012 (Catalog validation - 4 tasks)

### ⚠️ Items Requiring Verification

1. **Locking Visibility UX Implementation (P6-UI-023..027)**
   - Need to verify lock status display exists
   - Need to verify lock prevention UI exists
   - Need to verify lock indicators exist
   - Need to verify lock scope verification exists
   - Current status: ❌ MISSING (needs verification)

2. **Canon Verification for Locking (P6-LOCK-000)**
   - Need to verify canon verification document exists
   - Need to verify locking behavior complies with Schema Canon
   - Need to verify D-005 obligation compliance
   - Current status: ❌ MISSING (needs verification)

3. **Catalog Validation (P6-CAT-009..012)**
   - Need to verify validation preview system exists
   - Need to verify pre-import validation exists
   - Need to verify validation results display exists
   - Need to verify validation rule configuration exists
   - Current status: ❌ MISSING (needs verification)

---

## Week-5 Closure Criteria

### Required for Closure

1. ⏳ **Locking Visibility UX Implemented** (P6-UI-023..027)
2. ⏳ **Lock Status Display Implemented** (P6-UI-024)
3. ⏳ **Lock Prevention UI Implemented** (P6-UI-025)
4. ⏳ **Lock Status Summary Implemented** (P6-UI-026)
5. ⏳ **Lock/Unlock Controls Implemented** (P6-UI-027)
6. ⏳ **Canon Verification for Locking Completed** (P6-LOCK-000)
7. ⏳ **All Tests Passing** (Locking visibility + canon verification tests)
8. ⏳ **Design Documents Created** (P6-UI-023)
9. ⏳ **All Compliance Alarms Resolved** (2 compliance alarms)
10. ⏳ **Catalog Validation Implemented** (P6-CAT-009..012 - high priority)
11. ⏳ **No Schema Changes Introduced** (scope guard)
12. ⏳ **Line-Item Locking Only Verified** (D-005 obligation)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ❌ NOT STARTED (Locking visibility UX not implemented)
- **Compliance Alarms:** ❌ 2 alarms need resolution (ALARM-LOCKING-VISIBILITY, ALARM-LOCKING-CANON)
- **Formal Sign-off:** ⏳ PENDING

**Closure Rule:** Week-5 is CLOSED only if locking visibility UX is implemented and canon verification is completed, with no schema changes and line-item locking only verified.

---

## Dependencies

### Requires

- **Week-4:** Resolution UX (for lock indicators at resolution levels)
- **Week-3:** Pricing UX (for lock indicators at pricing levels)
- **Week-2:** Hierarchy CRUD (for lock indicators at hierarchy levels)

### Blocks

- **Week-6:** Error/warning surfacing may rely on lock status indicators
- **Week-8.5:** Legacy parity gate may require locking visibility verification

---

## Risks & Mitigations

### Risk 1: Locking Implementation Confused with Locking Visibility

**Mitigation:** Week-5 is about locking visibility only (UI indicators, status display, prevention UI). Locking implementation is separate. Scope guard: visibility only.

### Risk 2: Schema Changes Introduced for Locking

**Mitigation:** No schema changes allowed. Locking visibility uses existing locking fields. Scope guard: no schema changes.

### Risk 3: Line-Item Locking Violated (D-005 Obligation)

**Mitigation:** Verify lock scope is line-item only (P6-UI-027). D-005 obligation verification required. Scope guard: line-item only.

### Risk 4: Canon Verification Skipped

**Mitigation:** Canon verification (P6-LOCK-000) is a compliance blocker. Must be completed for Week-5 closure.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Resolve Compliance Alarms (Blocking)

1. **ALARM-LOCKING-VISIBILITY Resolution**
   - P6-UI-024: Implement lock status display
   - P6-UI-025: Implement lock prevention UI
   - P6-UI-026: Implement lock status summary
   - P6-UI-027: Implement lock/unlock controls (admin)
   - Tests: test_lock_status_display.py, test_lock_prevention_ui.py, test_lock_indicators.py

2. **ALARM-LOCKING-CANON Resolution**
   - P6-LOCK-000: Canon verification for locking
   - Verification document
   - Schema Canon compliance check
   - D-005 obligation verification

#### Priority 2: Complete Documentation

3. **Design Documents**
   - P6-UI-023: Create locking visibility UX design document

4. **Catalog Validation**
   - P6-CAT-009: Design validation preview system
   - P6-CAT-010: Implement pre-import validation
   - P6-CAT-011: Implement validation results display
   - P6-CAT-012: Implement validation rule configuration

#### Priority 3: Verification

5. **Implementation Verification**
   - Verify locking visibility UX works
   - Verify canon verification completed
   - Verify no schema changes introduced
   - Verify line-item locking only
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week5_checks.sh` - Week-5 verification runner
     - Runs all Week-5 tests (locking visibility + canon verification)
     - Verifies API endpoints
     - Validates locking visibility functionality
     - Validates canon compliance
     - Validates lock scope (line-item only)
     - Generates evidence summary

2. **Tests:**
   - `tests/locking/test_lock_status_display.py` - Lock status display tests
     - Test visual lock icon display
     - Test lock status badge
     - Test lock timestamp display
     - Test lock reason tooltip
   - `tests/locking/test_lock_prevention_ui.py` - Lock prevention UI tests
     - Test disabled edits for locked items
     - Test prevent modifications to locked items
     - Test lock reason display when edit attempted
   - `tests/locking/test_lock_status_summary.py` - Lock status summary tests
     - Test panel-level lock count
     - Test BOM-level lock count
     - Test quotation-level lock summary
     - Test lock status dashboard
   - `tests/locking/test_lock_unlock_controls.py` - Lock/unlock controls tests
     - Test unlock button (admin only)
     - Test lock confirmation dialog
     - Test unlock confirmation dialog
     - Test audit log entry
   - `tests/locking/test_no_higher_level_locking.py` - No higher-level locking verification tests
     - Test no is_locked field on quote_boms (BOM level)
     - Test no is_locked field on quote_panels (Panel level)
     - Test no is_locked field on quotations (Quotation level)
     - Test locking only at quote_bom_items level (line-item only)
     - Test D-005 obligation compliance

3. **Evidence:**
   - `evidence/PHASE6_WEEK5_EVIDENCE_PACK.md` - Week-5 evidence documentation
     - API endpoint documentation
     - Test results summary
     - Locking visibility UI screenshots
     - Canon verification document
     - Lock scope verification document

4. **API Endpoints:**
   - GET /api/v1/quotation/{id}/item/{itemId}/lock-status - Get lock status
   - GET /api/v1/quotation/{id}/lock-status - Get quotation lock status (aggregated)

5. **Frontend Components:**
   - Lock status display component (lock icon, badge, timestamp, tooltip)
   - Lock prevention UI component (disabled edits, lock reason display)
   - Lock status summary component (panel/BOM/quotation level lock counts)
   - Lock/unlock controls component (admin-only unlock button, confirmation dialogs)

6. **Backend Services:**
   - Lock status service (lock status retrieval)
   - Lock scope verification service (line-item only verification)

7. **Documentation:**
   - `docs/PHASE_6/UI/LOCKING_VISIBILITY_UX.md` - Locking visibility UX design document
   - `docs/PHASE_6/LOCKING/LOCKING_SCOPE_VERIFICATION.md` - Locking scope verification document (P6-LOCK-000)
   - `docs/PHASE_6/CATALOG/VALIDATION_PREVIEW_SYSTEM.md` - Validation preview system design document (P6-CAT-009)

### Verification Checklist

- [ ] Verify scripts/run_week5_checks.sh exists
- [ ] Verify all test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify locking visibility UX works (P6-UI-024..027)
- [ ] Verify no higher-level locking verification completed (P6-LOCK-000)
- [ ] Verify no schema changes introduced
- [ ] Verify line-item locking only (D-005 obligation)
- [ ] Verify evidence/PHASE6_WEEK5_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-5 runner
- [ ] Verify catalog validation implemented (P6-CAT-009..012)

---

## Decision Point

**Week-5 Closure Status:**
- ⏳ **PENDING COMPLETION**

**Options:**
1. **"Close Week-5 and start Week-6 detailed plan"** - If all implementation artifacts verified and tests passing
2. **"Verify Week-5 implementation"** - If artifacts need verification
3. **"Complete Week-5 implementation"** - If locking visibility or canon verification still missing

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-5 tasks)
- **Schema Canon v1.0:** (Week-0 governance pack - for canon verification)
- **D-005 Obligation:** (Phase-5 compliance - line-item locking only)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 10 | All captured from matrix |
| **Compliance Alarms** | 2 | 🔴 Must resolve |
| **High Priority Alarms** | 2 | 🟠 Should resolve |
| **Medium Priority Items** | 1 | 🟡 Can be deferred |
| **Completed Tasks** | 0 | None complete |
| **Missing Tasks** | 7 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-LOCKING-VISIBILITY:** Implement lock status display + lock prevention UI + lock status summary + lock/unlock controls (P6-UI-023..027)
- [ ] **ALARM-LOCKING-CANON:** Verify no higher-level locking introduced (schema + UI verification, line-item only) (P6-LOCK-000)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-UI-023:** Create locking visibility UX design document (P6-UI-023)
- [ ] **ALARM-CAT-009:** Design validation preview system (P6-CAT-009)
- [ ] **ALARM-CAT-010:** Implement pre-import validation (P6-CAT-010)
- [ ] **ALARM-CAT-011:** Implement validation results display (P6-CAT-011)
- [ ] **ALARM-CAT-012:** Implement validation rule configuration (P6-CAT-012)

### Documentation Tasks

- [ ] Complete locking visibility UX implementation (P6-UI-024..027)
- [ ] Complete no higher-level locking verification (P6-LOCK-000)
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete
- [ ] Verify no schema changes introduced
- [ ] Verify line-item locking only (D-005 obligation)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After implementation verification

**Note:** Week-5 is about locking visibility only (UI indicators, status display, prevention UI). Locking implementation is separate. No schema changes allowed. Line-item locking only (D-005 obligation).
