# Phase 3 Execution Checklist

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE  
**Date:** 2025-12-17 (IST)

---

## A) Pre-Execution Readiness (Must be true)

- [ ] Phase 1 baselines frozen (all modules)
- [ ] Phase 2 trace maps complete:
  - [ ] ROUTE_MAP
  - [ ] FEATURE_CODE_MAP
  - [ ] FILE_OWNERSHIP
- [ ] Phase 3 documents exist and are linked in Phase 3 Index
- [ ] Protected files list confirmed (PROTECTED zone)
- [ ] Cross-module touchpoints identified (apply/reuse/shared APIs)

---

## B) Task Creation Checklist (For every task)

- [ ] Task ID created (NSW-P4-<S_STAGE>-<MODULE>-###)
- [ ] Module + sub-area selected
- [ ] Task type selected (Governance/Refactor/Bugfix/Hardening/UX/Performance/Migration)
- [ ] File list added (paths under `source_snapshot/`)
- [ ] Owner module confirmed (FILE_OWNERSHIP)
- [ ] Risk level assigned (PROTECTED/HIGH/MEDIUM/LOW)
- [ ] Cross-module touchpoints noted (if any)
- [ ] Rollback defined (mandatory for HIGH/PROTECTED)
- [ ] Gate assigned (G1–G4)

---

## C) Risk Gate Checklist

### PROTECTED (G4)

- [ ] Wrapper-only approach confirmed
- [ ] Regression suite defined
- [ ] Apply-flow bundle included if Quotation V2 touched
- [ ] Costing validation included if costing touched
- [ ] Approval recorded

### HIGH (G3)

- [ ] Cross-module test bundle defined
- [ ] Rollback steps written and feasible
- [ ] Performance check included if reuse/search affected
- [ ] Approval recorded

### MEDIUM (G2)

- [ ] Module regression defined
- [ ] UI check defined

### LOW (G1)

- [ ] Basic verification defined

---

## D) Planning Freeze Checklist (Before any code work begins)

- [ ] Task Register reviewed and approved for first execution set
- [ ] Refactor order confirmed for chosen module
- [ ] Risk controls acknowledged by team
- [ ] Testing gates agreed
- [ ] “No-go zones” confirmed (CostingService, QuotationQuantityService, core V2 entities)

---

## E) Phase 3 Closure Checklist

Phase 3 can be closed only when:
- [ ] Approved first execution sprint exists (Phase 4 entry)
- [ ] Rollback logic is documented for all HIGH/PROTECTED tasks
- [ ] Cross-module bundles are written and testable
- [ ] Stakeholder sign-off recorded (internal)

---

## F) Reference Links

- Phase 1:
  - `docs/PHASE_1/BASELINE_FREEZE_REGISTER.md`
- Phase 2:
  - `trace/phase_2/ROUTE_MAP.md`
  - `trace/phase_2/FEATURE_CODE_MAP.md`
  - `trace/phase_2/FILE_OWNERSHIP.md`
- Phase 3:
  - `docs/PHASE_3/PHASE_3_INDEX.md`
  - `docs/PHASE_3/PHASE_3_EXECUTION_PLAN.md`
  - `docs/PHASE_3/04_TASK_REGISTER/TASK_REGISTER.md`
  - `docs/PHASE_3/05_RISK_CONTROL/RISK_CONTROL_MATRIX.md`
  - `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`

