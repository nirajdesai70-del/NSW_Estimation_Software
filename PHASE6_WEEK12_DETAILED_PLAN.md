# Phase-6 Week-12 Detailed Plan

**Week:** Week-12 (Phase-6 Closure)  
**Status:** ❌ NOT STARTED (Planning only)  
**Closure Status:** ⏳ Pending formal sign-off  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-12 is the formal closure and governance sign-off week for Phase-6. Its sole purpose is to freeze scope, confirm compliance, and declare Phase-6 DONE. This includes Phase-6 exit criteria verification, success metrics verification, Phase-6 closure report creation, handover to Phase-7, and canon compliance signoff.

**Key Deliverables (Week-12 Core Closure):**
- Phase-6 Closure (Exit criteria verification, success metrics verification, closure report, handover to Phase-7, canon compliance signoff)

**Critical Alarms (From Matrix):**
- 🔴 **Gate Alarms** (must resolve for Phase-6 closure)
  - Phase-6 exit criteria verification (P6-CLOSE-001 - gate blocker)
  - Success metrics verification (P6-CLOSE-002 - gate blocker)
  - Canon compliance signoff (P6-CLOSE-005 - gate blocker)
- 🔴 **Compliance Alarms** (must resolve for Phase-6 closure)
  - Phase-6 closure report (P6-CLOSE-003)
  - Handover to Phase-7 (P6-CLOSE-004)

**Note:** Week-12 does NOT add features, fix bugs, refactor code, or tune performance. All work here is verification, documentation, and sign-off only. Week-12 can start only if Week-11 is CLOSED, no critical or compliance alarms remain open, D0 Gate = PASSED, Week-8.5 Legacy Parity Gate = PASSED, and no canon violations remain.

---

## Week-12 Task Breakdown

### Track: Phase-6 Closure & Governance

#### Phase-6 Closure Track - Closure & Governance

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-CLOSE-001 | Phase-6 exit criteria verification | Phase-6 exit criteria verification report | ❌ MISSING | 🔴 **GATE** | Phase-6 exit criteria verification (verify all Phase-6 exit criteria are met, gate blocker for Phase-6 closure) |
| P6-CLOSE-002 | Success metrics verification | Success metrics verification report | ❌ MISSING | 🔴 **GATE** | Success metrics verification (verify all Phase-6 success metrics are met, gate blocker for Phase-6 closure) |
| P6-CLOSE-003 | Create Phase-6 closure report | Phase-6 closure report document | ❌ MISSING | 🔴 **COMPLIANCE** | Create Phase-6 closure report (comprehensive closure report documenting Phase-6 completion, deliverables, evidence) |
| P6-CLOSE-004 | Handover to Phase-7 | Handover documentation | ❌ MISSING | 🔴 **COMPLIANCE** | Handover to Phase-7 (handover documentation, deferred items register, Phase-7 input preparation) |
| P6-CLOSE-005 | Canon compliance signoff | Canon compliance signoff document | ❌ MISSING | 🔴 **GATE** | Canon compliance signoff (formal confirmation: schema, validation, error taxonomy unchanged, gate blocker for Phase-6 closure) |

**Phase-6 Closure Track Status:** ❌ NOT STARTED (Phase-6 closure work not implemented)

**Week-12 Scope Limit:** Week-12 is governance, not engineering. All work is verification, documentation, and sign-off only. No new features, no bug fixes, no refactoring, no performance tuning.

---

## Alarm Summary for Week-12

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Gate Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** gate blockers for Phase-6 closure. They block formal closure and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-CLOSE-EXIT-CRITERIA** | Review 1 (Finalized Review 4) | P6-CLOSE-001 | Phase-6 exit criteria verification (gate blocker) | ❌ MISSING | Verify all Phase-6 exit criteria are met (gate blocker for Phase-6 closure) |
| **ALARM-CLOSE-SUCCESS-METRICS** | Review 1 (Finalized Review 4) | P6-CLOSE-002 | Success metrics verification (gate blocker) | ❌ MISSING | Verify all Phase-6 success metrics are met (gate blocker for Phase-6 closure) |
| **ALARM-CLOSE-CANON-SIGNOFF** | Review 1 (Finalized Review 4) | P6-CLOSE-005 | Canon compliance signoff (gate blocker) | ❌ MISSING | Canon compliance signoff (formal confirmation: schema, validation, error taxonomy unchanged, gate blocker for Phase-6 closure) |

**Alarm Details:**

#### ALARM-CLOSE-EXIT-CRITERIA (Gate Blocker - Exit Criteria Verification)

- **Tasks Affected:** P6-CLOSE-001 (Phase-6 exit criteria verification)
- **Impact:** Gate blocker. Phase-6 cannot be declared closed without exit criteria verification.
- **Matrix Status:** Finalized in Review 4 as **GATE** alarm
- **Resolution:** 
  - P6-CLOSE-001: Phase-6 exit criteria verification
    - Verify all Phase-6 exit criteria are met
    - Exit criteria verification report
    - Gate blocker for Phase-6 closure
- **Notes:** Phase-6 exit criteria verification is a gate blocker. Phase-6 cannot be declared closed without this verification.

#### ALARM-CLOSE-SUCCESS-METRICS (Gate Blocker - Success Metrics Verification)

- **Tasks Affected:** P6-CLOSE-002 (Success metrics verification)
- **Impact:** Gate blocker. Phase-6 cannot be declared closed without success metrics verification.
- **Matrix Status:** Finalized in Review 4 as **GATE** alarm
- **Resolution:** 
  - P6-CLOSE-002: Success metrics verification
    - Verify all Phase-6 success metrics are met
    - Success metrics verification report
    - Gate blocker for Phase-6 closure
- **Notes:** Success metrics verification is a gate blocker. Phase-6 cannot be declared closed without this verification.

#### ALARM-CLOSE-CANON-SIGNOFF (Gate Blocker - Canon Compliance Signoff)

- **Tasks Affected:** P6-CLOSE-005 (Canon compliance signoff)
- **Impact:** Gate blocker. Phase-6 cannot be declared closed without canon compliance signoff.
- **Matrix Status:** Finalized in Review 4 as **GATE** alarm
- **Resolution:** 
  - P6-CLOSE-005: Canon compliance signoff
    - Formal confirmation: schema, validation, error taxonomy unchanged
    - Canon compliance signoff document
    - Gate blocker for Phase-6 closure
- **Notes:** Canon compliance signoff is a gate blocker. Phase-6 cannot be declared closed without this signoff. This is a declarative sign-off, not a re-implementation.

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-CLOSE-REPORT** | Review 1 (Finalized Review 4) | P6-CLOSE-003 | Phase-6 closure report missing (compliance requirement) | ❌ MISSING | Create Phase-6 closure report (comprehensive closure report documenting Phase-6 completion, deliverables, evidence) |
| **ALARM-CLOSE-HANDOVER** | Review 1 (Finalized Review 4) | P6-CLOSE-004 | Handover to Phase-7 missing (compliance requirement) | ❌ MISSING | Handover to Phase-7 (handover documentation, deferred items register, Phase-7 input preparation) |

**Alarm Details:**

#### ALARM-CLOSE-REPORT (Compliance - Phase-6 Closure Report)

- **Tasks Affected:** P6-CLOSE-003 (Create Phase-6 closure report)
- **Impact:** Compliance requirement. Phase-6 closure report must be created for governance compliance.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-CLOSE-003: Create Phase-6 closure report
    - Comprehensive closure report documenting Phase-6 completion
    - Deliverables summary
    - Evidence consolidation
    - Official "Phase-6 CLOSED" declaration
- **Notes:** Phase-6 closure report is a compliance requirement. It documents Phase-6 completion and serves as the official closure declaration.

#### ALARM-CLOSE-HANDOVER (Compliance - Handover to Phase-7)

- **Tasks Affected:** P6-CLOSE-004 (Handover to Phase-7)
- **Impact:** Compliance requirement. Handover to Phase-7 must be prepared for continuity.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-CLOSE-004: Handover to Phase-7
    - Handover documentation
    - Deferred items register (items explicitly deferred to Phase-7)
    - Phase-7 input preparation
- **Notes:** Handover to Phase-7 is a compliance requirement. It ensures continuity and documents deferred items for Phase-7 planning.

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-12 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-CLOSE-001..005 (Phase-6 Closure - 5 tasks)

### ⚠️ Items Requiring Verification

1. **Phase-6 Closure Implementation (P6-CLOSE-001..005)**
   - Need to verify Phase-6 exit criteria verification complete
   - Need to verify success metrics verification complete
   - Need to verify Phase-6 closure report created
   - Need to verify handover to Phase-7 prepared
   - Need to verify canon compliance signoff complete
   - Current status: ❌ NOT STARTED (needs verification)

---

## Hard Preconditions (Non-Negotiable)

Week-12 can start only if:
1. ✅ Week-11 is CLOSED
2. ✅ No critical or compliance alarms remain open
3. ✅ D0 Gate = PASSED
4. ✅ Week-8.5 Legacy Parity Gate = PASSED
5. ✅ No canon violations (schema, validation, taxonomy)

If any precondition fails → Phase-6 is NOT closable.

---

## Week-12 Closure Criteria

### Required for Closure

1. ⏳ **Week-11 CLOSED** (Hard precondition)
   - Week-11 must be closed before Week-12 can start
2. ⏳ **No Critical or Compliance Alarms Open** (Hard precondition)
   - No critical or compliance alarms must remain open
3. ⏳ **D0 Gate PASSED** (Hard precondition)
   - D0 Gate must be passed (Week-6)
4. ⏳ **Week-8.5 Legacy Parity Gate PASSED** (Hard precondition)
   - Week-8.5 Legacy Parity Gate must be passed
5. ⏳ **No Canon Violations** (Hard precondition)
   - No canon violations (schema, validation, taxonomy) must remain
6. ⏳ **Phase-6 Exit Criteria Verified** (P6-CLOSE-001)
   - Phase-6 exit criteria verification complete
   - Exit criteria verification report
7. ⏳ **Success Metrics Verified** (P6-CLOSE-002)
   - Success metrics verification complete
   - Success metrics verification report
8. ⏳ **Phase-6 Closure Report Created** (P6-CLOSE-003)
   - Phase-6 closure report created
   - Comprehensive closure report documenting Phase-6 completion
9. ⏳ **Handover to Phase-7 Prepared** (P6-CLOSE-004)
   - Handover documentation prepared
   - Deferred items register prepared
   - Phase-7 input preparation complete
10. ⏳ **Canon Compliance Signoff Complete** (P6-CLOSE-005)
    - Canon compliance signoff complete
    - Formal confirmation: schema, validation, error taxonomy unchanged
11. ⏳ **All Gate Alarms Resolved** (3 gate alarms)
12. ⏳ **All Compliance Alarms Resolved** (2 compliance alarms)
13. ⏳ **Formal Closure Declaration** (Official "Phase-6 CLOSED" declaration)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ❌ NOT STARTED (Preconditions must be met first)
- **Precondition Status:** ⏳ PENDING (Week-11 must be closed, all gates must pass)
- **Gate Alarms:** ❌ 3 alarms need resolution (ALARM-CLOSE-EXIT-CRITERIA, ALARM-CLOSE-SUCCESS-METRICS, ALARM-CLOSE-CANON-SIGNOFF)
- **Compliance Alarms:** ❌ 2 alarms need resolution (ALARM-CLOSE-REPORT, ALARM-CLOSE-HANDOVER)
- **Formal Sign-off:** ⏳ PENDING

**Closure Rule:** Week-12 is CLOSED only if all preconditions are met, all gate alarms are resolved, all compliance alarms are resolved, and formal closure declaration is issued. Week-12 is binary: PASS → Phase-6 closed, FAIL → return to originating week (not patch here). No partial closures.

---

## Dependencies

### Requires (Execution)

- **Week-11:** Buffer Week must be CLOSED (hard precondition - Week-12 cannot start without this)
- **Week-8.5:** Legacy Parity Gate must PASS (hard precondition)
- **Week-6:** D0 Gate must PASS (hard precondition)
- **All Weeks 0-11:** All previous weeks must be at acceptable state (no critical blockers)

### Can Run in Parallel (Planning / Scaffolding)

- **Documentation:** Closure report and handover documentation can be prepared in parallel (but execution blocked until preconditions met)

### Blocks

- **Phase-7:** Phase-7 planning depends on Phase-6 closure completion

---

## Risks & Mitigations

### Risk 1: Hidden Work Sneaks into Phase-6 (Scope Bleed)

**Mitigation:** Explicit scope freeze. Phase-6 scope must be frozen. No additional fixes are allowed under Phase-6. All remaining work moves to Phase-7. This prevents scope bleed.

### Risk 2: Canon Drift Discovered Late

**Mitigation:** Canon sign-off document required. Canon compliance signoff must explicitly confirm: schema, validation, error taxonomy unchanged. This is a declarative sign-off, not a re-implementation.

### Risk 3: Ambiguous Closure

**Mitigation:** Formal closure declaration required. Official "Phase-6 CLOSED" declaration must be issued. This is the legal-grade closure.

### Risk 4: Phase-7 Polluted by Phase-6 Leftovers

**Mitigation:** Explicit deferral register required. All deferred items must be documented in the deferred items register for Phase-7 input. Handover documentation must include deferred items.

### Risk 5: Week-12 Becomes Engineering Week (Violates "Governance Only" Rule)

**Mitigation:** Strict "governance only" rule. Week-12 does NOT add features, fix bugs, refactor code, or tune performance. All work is verification, documentation, and sign-off only. If Week-12 feels "boring", it means Phase-6 was done correctly.

### Risk 6: Partial Closures Allowed

**Mitigation:** Binary closure rule. Week-12 is binary: PASS → Phase-6 closed, FAIL → return to originating week (not patch here). No partial closures allowed.

---

## What Week-12 Verifies (Nothing New)

### A. Canon Compliance (P6-CLOSE-005)

Explicit confirmation that:
- Schema Canon unchanged
- Validation rules unchanged
- Error taxonomy unchanged
- Guardrails unchanged
- No silent logic drift

This is a declarative sign-off, not a re-implementation.

### B. Exit Criteria Verification (P6-CLOSE-001)

Verify all Phase-6 exit criteria are met:
- All defined scope delivered
- All compliance requirements met
- All gates passed
- All evidence complete

### C. Success Metrics Verification (P6-CLOSE-002)

Verify all Phase-6 success metrics are met:
- Functional requirements met
- Quality requirements met
- Performance requirements met (if applicable)
- Compliance requirements met

### D. Scope Freeze (P6-CLOSE-003)

A written declaration that:
- Phase-6 scope is frozen
- No additional fixes are allowed under Phase-6
- All remaining work moves to Phase-7

This prevents scope bleed.

### E. Evidence Consolidation (P6-CLOSE-003)

Week-12 produces a single authoritative bundle:
- All weekly evidence packs consolidated
- All gate signoffs consolidated
- Canon compliance signoff consolidated
- Phase-6 closure declaration

No placeholders. No "TODO".

### F. Handover to Phase-7 (P6-CLOSE-004)

Handover documentation including:
- Phase-6 completion summary
- Deferred items register (items explicitly deferred to Phase-7)
- Phase-7 input preparation
- Continuity documentation

---

## Next Steps

### Immediate Actions Required

#### Priority 0: Verify Preconditions (Hard Precondition)

0. **Precondition Verification**
   - Verify Week-11 CLOSED
   - Verify no critical or compliance alarms remain open
   - Verify D0 Gate PASSED
   - Verify Week-8.5 Legacy Parity Gate PASSED
   - Verify no canon violations (schema, validation, taxonomy)
   - Week-12 can start only if these preconditions are met

#### Priority 1: Verify Exit Criteria and Success Metrics (After Preconditions Met)

1. **Exit Criteria and Success Metrics Verification (Gate Blockers)**
   - P6-CLOSE-001: Phase-6 exit criteria verification
     - Verify all Phase-6 exit criteria are met
     - Exit criteria verification report
   - P6-CLOSE-002: Success metrics verification
     - Verify all Phase-6 success metrics are met
     - Success metrics verification report

#### Priority 2: Canon Compliance Signoff (Gate Blocker)

2. **Canon Compliance Signoff (Gate Blocker)**
   - P6-CLOSE-005: Canon compliance signoff
     - Formal confirmation: schema, validation, error taxonomy unchanged
     - Canon compliance signoff document
     - Declarative sign-off (not re-implementation)

#### Priority 3: Closure Report and Handover (Can Proceed in Parallel)

3. **Closure Report and Handover (Compliance Requirements)**
   - P6-CLOSE-003: Create Phase-6 closure report
     - Comprehensive closure report documenting Phase-6 completion
     - Deliverables summary
     - Evidence consolidation
     - Official "Phase-6 CLOSED" declaration
   - P6-CLOSE-004: Handover to Phase-7
     - Handover documentation
     - Deferred items register (items explicitly deferred to Phase-7)
     - Phase-7 input preparation

#### Priority 4: Formal Closure Declaration

4. **Formal Closure Declaration**
   - Issue official "Phase-6 CLOSED" declaration
   - Confirm all gate alarms resolved
   - Confirm all compliance alarms resolved
   - Confirm all preconditions met

---

## Implementation Artifacts

### Expected Artifacts

1. **Documents:**
   - `docs/PHASE_6/CLOSURE/PHASE6_EXIT_CRITERIA_VERIFICATION.md` - Exit criteria verification report
   - `docs/PHASE_6/CLOSURE/PHASE6_SUCCESS_METRICS_VERIFICATION.md` - Success metrics verification report
   - `docs/PHASE_6/CLOSURE/PHASE6_CLOSURE_REPORT.md` - Phase-6 closure report
   - `docs/PHASE_6/CLOSURE/PHASE6_HANDOVER_TO_PHASE7.md` - Handover documentation
   - `docs/PHASE_6/CLOSURE/PHASE6_CANON_COMPLIANCE_SIGNOFF.md` - Canon compliance signoff document
   - `docs/PHASE_6/CLOSURE/PHASE6_CLOSURE_DECLARATION.md` - Formal closure declaration

2. **Evidence:**
   - `evidence/PHASE6_CLOSURE_PACK/` - Phase-6 closure evidence bundle
     - All weekly evidence packs consolidated
     - All gate signoffs consolidated
     - Canon compliance signoff
     - Phase-6 closure declaration

3. **Documentation:**
   - Deferred items register (items explicitly deferred to Phase-7)
   - Phase-7 input preparation documents

### Verification Checklist

- [ ] Verify Week-11 CLOSED (hard precondition)
- [ ] Verify no critical or compliance alarms remain open (hard precondition)
- [ ] Verify D0 Gate PASSED (hard precondition)
- [ ] Verify Week-8.5 Legacy Parity Gate PASSED (hard precondition)
- [ ] Verify no canon violations (hard precondition)
- [ ] Verify Phase-6 exit criteria verification complete (P6-CLOSE-001)
- [ ] Verify success metrics verification complete (P6-CLOSE-002)
- [ ] Verify Phase-6 closure report created (P6-CLOSE-003)
- [ ] Verify handover to Phase-7 prepared (P6-CLOSE-004)
- [ ] Verify canon compliance signoff complete (P6-CLOSE-005)
- [ ] Verify all gate alarms resolved (3 gate alarms)
- [ ] Verify all compliance alarms resolved (2 compliance alarms)
- [ ] Verify formal closure declaration issued
- [ ] Verify evidence bundle complete
- [ ] Verify no placeholders or "TODO" items

---

## Decision Point

**Week-12 Closure Status:**
- ⏳ **PENDING FORMAL SIGN-OFF** (Preconditions must be met first)

**Options:**
1. **"Phase-6 CLOSED - Proceed to Phase-7"** - If all preconditions pass, all gate alarms resolved, all compliance alarms resolved, and formal closure declaration issued
2. **"Complete Week-12 closure tasks"** - If exit criteria verification, success metrics verification, closure report, handover, or canon signoff still missing
3. **"Verify preconditions and proceed"** - If Week-11, D0 Gate, or Week-8.5 Gate needs verification

**Note:** Week-12 is binary: PASS → Phase-6 closed, FAIL → return to originating week (not patch here). No partial closures. Week-12 does NOT add features, fix bugs, refactor code, or tune performance. All work is verification, documentation, and sign-off only. If Week-12 feels "boring", it means Phase-6 was done correctly.

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-12 tasks)
- **Week-11:** Buffer Week - must be CLOSED
- **Week-8.5 Gate:** Legacy Parity Verification Gate - must PASS
- **Week-6:** D0 Gate - must PASS
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 5 | All captured from matrix |
| **Gate Alarms** | 3 | 🔴 Must resolve (gate blockers) |
| **Compliance Alarms** | 2 | 🔴 Must resolve |
| **New Features** | 0 | None (governance only) |
| **Allowed Fixes** | 0 | None (governance only) |
| **Canon Changes** | 0 | None (governance only) |
| **Completed Tasks** | 0 | None complete |
| **Missing Tasks** | 5 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Gate Alarms (Must Resolve - Gate Blockers)

- [ ] **ALARM-CLOSE-EXIT-CRITERIA:** Phase-6 exit criteria verification (P6-CLOSE-001) - gate blocker
- [ ] **ALARM-CLOSE-SUCCESS-METRICS:** Success metrics verification (P6-CLOSE-002) - gate blocker
- [ ] **ALARM-CLOSE-CANON-SIGNOFF:** Canon compliance signoff (P6-CLOSE-005) - gate blocker

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-CLOSE-REPORT:** Create Phase-6 closure report (P6-CLOSE-003)
- [ ] **ALARM-CLOSE-HANDOVER:** Handover to Phase-7 (P6-CLOSE-004)

### Documentation Tasks

- [ ] Complete Phase-6 exit criteria verification (P6-CLOSE-001)
- [ ] Complete success metrics verification (P6-CLOSE-002)
- [ ] Create Phase-6 closure report (P6-CLOSE-003)
- [ ] Prepare handover to Phase-7 (P6-CLOSE-004)
- [ ] Complete canon compliance signoff (P6-CLOSE-005)
- [ ] Verify all implementation artifacts exist
- [ ] Verify evidence bundle complete
- [ ] Verify formal closure declaration issued
- [ ] Verify Week-11 CLOSED (hard precondition)
- [ ] Verify D0 Gate PASSED (hard precondition)
- [ ] Verify Week-8.5 Legacy Parity Gate PASSED (hard precondition)
- [ ] Verify no canon violations (hard precondition)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After preconditions pass and closure tasks complete

**Note:** Week-12 is the formal closure and governance sign-off week for Phase-6. Its sole purpose is to freeze scope, confirm compliance, and declare Phase-6 DONE. Week-12 does NOT add features, fix bugs, refactor code, or tune performance. All work is verification, documentation, and sign-off only. Week-12 is binary: PASS → Phase-6 closed, FAIL → return to originating week (not patch here). No partial closures. If Week-12 feels "boring", it means Phase-6 was done correctly.
