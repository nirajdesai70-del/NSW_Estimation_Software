# Phase-6 Week-8.5 Detailed Plan

**Week:** Week-8.5 (Legacy Parity Verification Gate)  
**Status:** ❌ NOT STARTED (Planning only - Gate verification)  
**Closure Status:** ⏳ Pending gate decision (PASS / CONDITIONAL PASS / FAIL)  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-8.5 is a formal gate (verification only, no execution) that validates NSW preserves all legacy capabilities before proceeding to integration, dashboards, and client-facing layers. This gate ensures functional equivalence or superiority to legacy, validates all reuse/editability/pricing/locking/workflows still work, confirms no Phase-5 Canon rule violations, and detects silent regressions.

**Key Deliverables (Week-8.5 Gate):**
- Legacy Parity Verification (Track G - quotation lifecycle, reuse workflows, editability, pricing, resolution, locking, error/warning visibility)
- Canon Compliance Confirmation
- Gate Decision (GO / CONDITIONAL / NO-GO)

**Critical Alarms (From Matrix):**
- 🔴 **Gate Blocker**
  - ALARM-PARITY-EDITABILITY: Post-reuse editability verification (blocks Week-8.5 gate)
  - ALARM-PARITY-GUARDRAILS: Guardrail validation after reuse (blocks Week-8.5 gate)
- 🔴 **Parity Alarms** (mandatory for Week-8.5 gate pass - cannot be deferred)
  - All legacy parity verification items must pass

**Note:** Week-8.5 is a verification gate only - no coding, no DB changes, no UI changes, no refactoring. This is a decision gate, not an execution sprint. Phase-6 cannot proceed to Integration (Week-9) unless all legacy parity items are verified.

---

## Week-8.5 Task Breakdown

### Track: Legacy Parity Gate (Track G) - Verification Only

#### Track G - Legacy Parity Gate

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-GATE-LEGACY-001 | Quotation reuse verified | Quotation reuse verification report | ❌ MISSING | 🔴 **GATE** | Verify quotation reuse (copy quotation, deep copy, copy-never-link, modify copied quotation freely, revision chain behavior) |
| P6-GATE-LEGACY-002 | Panel reuse verified | Panel reuse verification report | ❌ MISSING | 🔴 **GATE** | Verify panel reuse (panel copy/reuse workflows) |
| P6-GATE-LEGACY-003 | Feeder reuse verified | Feeder reuse verification report | ❌ MISSING | 🔴 **GATE** | Verify feeder reuse (Level-0 BOM reuse, feeder copy workflows) |
| P6-GATE-LEGACY-004 | BOM reuse verified | BOM reuse verification report | ❌ MISSING | 🔴 **GATE** | Verify BOM reuse (BOM copy/reuse workflows, Master BOM apply) |
| P6-GATE-LEGACY-005 | Post-reuse guardrails verified | Post-reuse guardrails verification report | ❌ MISSING | 🔴 **GATE** | Verify guardrail validation after reuse (P6-UI-REUSE-007). Part of ALARM-PARITY-GUARDRAILS |
| P6-GATE-LEGACY-006 | Legacy parity checklist complete | Legacy parity checklist completion report | ❌ MISSING | 🔴 **GATE** | Complete legacy parity checklist verification. All items must pass for gate to pass |

**Track G Status:** ❌ NOT STARTED (Gate verification pending)

**Gate Rule:** Phase-6 cannot proceed to Integration (Week-9) unless all legacy parity items are verified. This is a hard blocking gate.

**Verification Scope:**
- A. Quotation Lifecycle Parity (create, copy, modify, revision chain)
- B. Reuse Parity (panel, feeder, BOM, Master BOM apply, post-reuse editability)
- C. BOM & Item Editability (add/edit/delete items, quantity changes, pricing overrides, tracking fields)
- D. Pricing & Discount Parity (PRICELIST/MANUAL/FIXED modes, bulk discount editor, approval hooks, price-missing handling)
- E. Resolution Parity (L0→L1→L2 resolution, constraint enforcement, error taxonomy mapping)
- F. Locking Semantics (line-item locking only, locked item visibility, locked item edit prevention, no higher-level locking)
- G. Error & Warning Visibility (price missing warnings, unresolved resolution warnings, error summary aggregation, request_id visibility)
- H. Navigation & UX Parity (users can still do everything they could before, no workflow dead-ends)

---

## Alarm Summary for Week-8.5

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Parity Alarms (Must Resolve Before Week-8.5 Gate Pass)

These alarms are **mandatory** for Week-8.5 gate pass. They block gate passage and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-PARITY-EDITABILITY** | Review 5 | P6-GATE-LEGACY-003, P6-UI-REUSE-006 | Post-reuse editability verification (blocks Week-8.5 gate) | ❌ MISSING | Verify post-reuse editability (P6-UI-REUSE-006). Items must be editable after reuse. Non-negotiable requirement |
| **ALARM-PARITY-GUARDRAILS** | Review 5 | P6-GATE-LEGACY-005, P6-UI-REUSE-007 | Guardrail validation after reuse (blocks Week-8.5 gate) | ❌ MISSING | Verify guardrail validation after reuse (P6-UI-REUSE-007). Guardrails must be enforced after reuse workflows |

**Alarm Details:**

#### ALARM-PARITY-EDITABILITY (Parity Gate Blocker)

- **Tasks Affected:** P6-GATE-LEGACY-003 (Feeder reuse verified), P6-UI-REUSE-006 (Post-reuse editability check from Week-4)
- **Impact:** Gate blocker. Post-reuse editability is non-negotiable. If items are not editable after reuse, Week-8.5 gate cannot pass.
- **Matrix Status:** Finalized in Review 5 as **PARITY** alarm
- **Resolution:** 
  - P6-GATE-LEGACY-003: Verify feeder reuse (must include editability verification)
  - P6-UI-REUSE-006: Verify post-reuse editability (items must be editable after reuse workflows)
  - Verify: Items copied/reused must be fully editable (add/edit/delete items, quantity changes, pricing overrides)
- **Notes:** Post-reuse editability is non-negotiable. This is a parity-critical requirement. Week-8.5 gate cannot pass without this verification.

#### ALARM-PARITY-GUARDRAILS (Parity Gate Blocker)

- **Tasks Affected:** P6-GATE-LEGACY-005 (Post-reuse guardrails verified), P6-UI-REUSE-007 (Guardrails after reuse from Week-4)
- **Impact:** Gate blocker. Guardrail validation after reuse is required. If guardrails are not enforced after reuse, Week-8.5 gate cannot pass.
- **Matrix Status:** Finalized in Review 5 as **PARITY** alarm
- **Resolution:** 
  - P6-GATE-LEGACY-005: Verify post-reuse guardrails (guardrail validation after reuse)
  - P6-UI-REUSE-007: Verify guardrails after reuse (guardrails must be enforced after reuse workflows)
  - Verify: Guardrails (G1-G8) must be enforced after reuse workflows complete
- **Notes:** Guardrail validation after reuse is required. This is a parity-critical requirement. Week-8.5 gate cannot pass without this verification.

---

### 🔴 Gate Tasks (All Must Pass for Gate to Pass)

All P6-GATE-LEGACY-001..006 tasks must pass for Week-8.5 gate to pass. These are verification tasks, not implementation tasks.

| Task ID | Description | Status | Verification Required |
|---------|-------------|--------|----------------------|
| P6-GATE-LEGACY-001 | Quotation reuse verified | ❌ MISSING | Verify quotation lifecycle parity (create, copy, modify, revision chain) |
| P6-GATE-LEGACY-002 | Panel reuse verified | ❌ MISSING | Verify panel reuse workflows |
| P6-GATE-LEGACY-003 | Feeder reuse verified | ❌ MISSING | Verify feeder reuse workflows + post-reuse editability |
| P6-GATE-LEGACY-004 | BOM reuse verified | ❌ MISSING | Verify BOM reuse workflows + Master BOM apply |
| P6-GATE-LEGACY-005 | Post-reuse guardrails verified | ❌ MISSING | Verify guardrail validation after reuse |
| P6-GATE-LEGACY-006 | Legacy parity checklist complete | ❌ MISSING | Complete all legacy parity checklist items |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-8.5 gate tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-GATE-LEGACY-001..006 (Legacy Parity Gate - 6 verification tasks)
- ✅ ALARM-PARITY-EDITABILITY (Post-reuse editability verification)
- ✅ ALARM-PARITY-GUARDRAILS (Guardrail validation after reuse)

### ⚠️ Items Requiring Verification

1. **Legacy Parity Verification (P6-GATE-LEGACY-001..006)**
   - Need to verify quotation lifecycle parity
   - Need to verify reuse workflows (panel, feeder, BOM)
   - Need to verify post-reuse editability (ALARM-PARITY-EDITABILITY)
   - Need to verify post-reuse guardrails (ALARM-PARITY-GUARDRAILS)
   - Need to complete legacy parity checklist
   - Current status: ❌ NOT STARTED (gate verification pending)

---

## Week-8.5 Closure Criteria (Gate Decision Rules)

### Gate Decision Rules (Non-Negotiable)

#### ✅ PASS (Gate Passes - Proceed to Week-9)

Week-8.5 gate PASSES only if:
1. ✅ All checklist items pass (P6-GATE-LEGACY-001..006)
2. ✅ No canon violations
3. ✅ No blocked legacy workflows
4. ✅ Post-reuse editability verified (ALARM-PARITY-EDITABILITY resolved)
5. ✅ Post-reuse guardrails verified (ALARM-PARITY-GUARDRAILS resolved)
6. ✅ Legacy parity checklist complete (all items verified)

**Action:** ➡️ Proceed to Week-9 (Integration & Global Dashboard)

---

#### ⚠️ CONDITIONAL PASS (Gate Passes with Conditions - Fix and Confirm)

Week-8.5 gate CONDITIONAL PASS if:
1. ⚠️ Minor UX gaps (non-blocking)
2. ⚠️ Non-blocking polish items
3. ⚠️ Fixable without schema or logic change

**Action:** ➡️ Fix items → re-confirm → proceed to Week-9

**Note:** Conditional pass items must be explicitly documented and tracked. Re-verification required before proceeding.

---

#### ❌ FAIL (Gate Fails - Do Not Proceed)

Week-8.5 gate FAILS if any of the following:
1. ❌ Reuse editability broken (ALARM-PARITY-EDITABILITY not resolved)
2. ❌ Guardrail validation after reuse broken (ALARM-PARITY-GUARDRAILS not resolved)
3. ❌ Locking semantics violated
4. ❌ Pricing meaning changed
5. ❌ Canon rule violated
6. ❌ Any legacy workflow blocked

**Action:** ➡️ Return to originating week (never patch blindly)

**Note:** If gate fails, identify the exact week/task that introduced the failure and return to that week for correction. Do not attempt "quick fixes" or patches.

---

### Current Gate Status

- **Gate Status:** ❌ NOT STARTED (Gate verification pending)
- **Verification Status:** ❌ NOT STARTED (All verification tasks pending)
- **Parity Alarms:** ❌ 2 alarms need resolution (ALARM-PARITY-EDITABILITY, ALARM-PARITY-GUARDRAILS)
- **Gate Decision:** ⏳ PENDING (Cannot be made until verification complete)

**Gate Rule:** Week-8.5 is a hard blocking gate. Phase-6 cannot proceed to Integration (Week-9) unless gate passes. This is verification only - no execution, no coding, no UI changes, no refactoring.

---

## Dependencies

### Requires (Verification Inputs - Already Available)

These are inputs only, not re-created:
- **Legacy Parity Checklist:** `PHASE_6_LEGACY_PARITY_CHECKLIST.md` (if exists) or equivalent documentation
- **Completed Planning Artifacts:**
  - Week-0 → Week-8 detailed plans
  - Phase-6 Execution Plan v1.4
  - Phase-5 Canon (Schema, Validation, Error Taxonomy)
- **Legacy References:**
  - Nish System Reference
  - Phase-1–4 workflows

### Blocks (If Gate Passes)

- **Week-9:** Integration & Global Dashboard can proceed if gate passes
- **Week-10:** Excel export can proceed if gate passes
- **Week-11-12:** Final phases can proceed if gate passes

### Blocks (If Gate Fails)

- **Week-9+:** All subsequent weeks are blocked until gate passes
- **Must Return To:** Originating week that introduced the failure (never patch blindly)

---

## Risks & Mitigations

### Risk 1: Gate Skipped Leads to Silent Regressions

**Mitigation:** Week-8.5 gate is mandatory. Cannot skip. Phase-6 cannot proceed to Integration without gate pass. Gate must be explicitly documented and signed off.

### Risk 2: Gate Verification Incomplete

**Mitigation:** All verification tasks (P6-GATE-LEGACY-001..006) must be completed. Legacy parity checklist must be fully completed. All parity alarms must be resolved.

### Risk 3: Post-Reuse Editability Not Verified (ALARM-PARITY-EDITABILITY)

**Mitigation:** Post-reuse editability is non-negotiable. Must verify items are editable after reuse workflows. Gate cannot pass without this verification.

### Risk 4: Post-Reuse Guardrails Not Verified (ALARM-PARITY-GUARDRAILS)

**Mitigation:** Guardrail validation after reuse is required. Must verify guardrails (G1-G8) are enforced after reuse workflows. Gate cannot pass without this verification.

### Risk 5: "Quick Fixes" Applied Instead of Returning to Originating Week

**Mitigation:** If gate fails, must return to exact originating week that introduced the failure. Never patch blindly. Never apply "quick fixes" at gate level.

---

## Next Steps

### Immediate Actions Required (Gate Verification)

#### Priority 1: Complete Legacy Parity Verification

1. **Verification Tasks (P6-GATE-LEGACY-001..006)**
   - P6-GATE-LEGACY-001: Verify quotation lifecycle parity
   - P6-GATE-LEGACY-002: Verify panel reuse
   - P6-GATE-LEGACY-003: Verify feeder reuse + post-reuse editability (ALARM-PARITY-EDITABILITY)
   - P6-GATE-LEGACY-004: Verify BOM reuse
   - P6-GATE-LEGACY-005: Verify post-reuse guardrails (ALARM-PARITY-GUARDRAILS)
   - P6-GATE-LEGACY-006: Complete legacy parity checklist

#### Priority 2: Document Gate Decision

2. **Gate Decision Documentation**
   - Create gate decision document
   - Document verification results (PASS / FAIL / NOTES for each item)
   - Document canon compliance statement
   - Document explicit GO / NO-GO decision
   - Document required fixes (if any)

#### Priority 3: Gate Decision Action

3. **Gate Decision Action**
   - If PASS: ➡️ Proceed to Week-9
   - If CONDITIONAL PASS: ➡️ Fix items → re-confirm → proceed to Week-9
   - If FAIL: ➡️ Return to originating week (never patch blindly)

---

## Implementation Artifacts

### Expected Artifacts (Verification Output Only)

1. **Gate Decision Document:**
   - `docs/PHASE_6/GATES/PHASE6_WEEK8_5_LEGACY_PARITY_GATE.md` - Week-8.5 gate decision document
     - Checklist table (PASS / FAIL / NOTES for each verification item)
     - Canon compliance statement
     - Explicit GO / NO-GO decision
     - Required fixes (if any)
     - Verification evidence references

2. **Verification Reports:**
   - Quotation reuse verification report (P6-GATE-LEGACY-001)
   - Panel reuse verification report (P6-GATE-LEGACY-002)
   - Feeder reuse verification report (P6-GATE-LEGACY-003) - must include post-reuse editability verification
   - BOM reuse verification report (P6-GATE-LEGACY-004)
   - Post-reuse guardrails verification report (P6-GATE-LEGACY-005)
   - Legacy parity checklist completion report (P6-GATE-LEGACY-006)

### Verification Checklist

- [ ] P6-GATE-LEGACY-001: Quotation reuse verified
- [ ] P6-GATE-LEGACY-002: Panel reuse verified
- [ ] P6-GATE-LEGACY-003: Feeder reuse verified + post-reuse editability verified (ALARM-PARITY-EDITABILITY)
- [ ] P6-GATE-LEGACY-004: BOM reuse verified
- [ ] P6-GATE-LEGACY-005: Post-reuse guardrails verified (ALARM-PARITY-GUARDRAILS)
- [ ] P6-GATE-LEGACY-006: Legacy parity checklist complete
- [ ] Canon compliance confirmed
- [ ] Gate decision document created
- [ ] Explicit GO / NO-GO decision documented
- [ ] Required fixes documented (if any)

---

## Decision Point

**Week-8.5 Gate Status:**
- ⏳ **PENDING VERIFICATION** (Gate verification required)

**Options:**
1. **"Gate PASSES - Proceed to Week-9"** - If all verification tasks pass, all parity alarms resolved, and canon compliance confirmed
2. **"Gate CONDITIONAL PASS - Fix and Re-confirm"** - If minor non-blocking items need fixing
3. **"Gate FAILS - Return to Originating Week"** - If any critical parity item fails (editability, guardrails, canon violations, etc.)

**Note:** Week-8.5 is a hard blocking gate. Phase-6 cannot proceed to Integration (Week-9) unless gate passes. This is verification only - no execution, no coding, no UI changes, no refactoring.

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-8.5 gate requirements)
- **Legacy Parity Checklist:** (Reference document for verification scope)
- **Phase-5 Canon:** (Schema, Validation, Error Taxonomy - for canon compliance verification)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register" → "Parity Alarms"
- **Week-4 Tasks:** P6-UI-REUSE-006 (Post-reuse editability), P6-UI-REUSE-007 (Guardrails after reuse) - must be verified in Week-8.5 gate

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Verification Tasks** | 6 | All captured from matrix |
| **Parity Alarms** | 2 | 🔴 Must resolve for gate pass |
| **Gate Decision Options** | 3 | PASS / CONDITIONAL PASS / FAIL |
| **Completed Verifications** | 0 | None complete |
| **Pending Verifications** | 6 | ❌ MISSING (need verification) |

---

## Alarm Resolution Checklist

### Parity Alarms (Must Resolve for Gate Pass)

- [ ] **ALARM-PARITY-EDITABILITY:** Verify post-reuse editability (P6-GATE-LEGACY-003, P6-UI-REUSE-006)
- [ ] **ALARM-PARITY-GUARDRAILS:** Verify post-reuse guardrails (P6-GATE-LEGACY-005, P6-UI-REUSE-007)

### Gate Verification Tasks

- [ ] **P6-GATE-LEGACY-001:** Quotation reuse verified
- [ ] **P6-GATE-LEGACY-002:** Panel reuse verified
- [ ] **P6-GATE-LEGACY-003:** Feeder reuse verified + post-reuse editability verified
- [ ] **P6-GATE-LEGACY-004:** BOM reuse verified
- [ ] **P6-GATE-LEGACY-005:** Post-reuse guardrails verified
- [ ] **P6-GATE-LEGACY-006:** Legacy parity checklist complete

### Gate Decision Documentation

- [ ] Create gate decision document
- [ ] Document verification results (PASS / FAIL / NOTES)
- [ ] Document canon compliance statement
- [ ] Document explicit GO / NO-GO decision
- [ ] Document required fixes (if any)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After gate verification

**Note:** Week-8.5 is a verification gate only - no coding, no DB changes, no UI changes, no refactoring. This is a decision gate, not an execution sprint. Phase-6 cannot proceed to Integration (Week-9) unless all legacy parity items are verified. Post-reuse editability and post-reuse guardrails are non-negotiable requirements (ALARM-PARITY-EDITABILITY, ALARM-PARITY-GUARDRAILS).
