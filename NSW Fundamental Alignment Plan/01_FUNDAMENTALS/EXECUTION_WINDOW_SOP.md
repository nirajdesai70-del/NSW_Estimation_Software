# EXECUTION WINDOW SOP — FUNDAMENTALS VERIFICATION & PATCHING

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Baseline:** FUNDAMENTALS_BASELINE_BUNDLE_v1.0  
**Mode:** CONTROLLED EXECUTION  
**Risk Level:** LOW (if SOP followed)

---

## 1) Entry Criteria (ALL MUST BE TRUE)

- [ ] Execution window formally approved
- [ ] DB backup completed and verified
- [ ] Execution engineer assigned
- [ ] Baseline documents frozen (v1.0)
- [ ] Verification queries reviewed (not executed yet)

---

## 2) Execution Window Phases

---

### PHASE 0 — Pre-Flight (No DB Touch)

- [ ] Confirm branch & commit
- [ ] Confirm no pending migrations
- [ ] Confirm read-only intent

**STOP if any mismatch found**

---

### PHASE 1 — Read-Only Verification

Run verification queries in order:

1. [ ] VQ-001 — Feeder Masters exist
2. [ ] VQ-002 — Feeder Master → Instances
3. [ ] VQ-003 — Proposal BOM Master ownership
4. [ ] VQ-004 — Orphan runtime BOMs
5. [ ] VQ-005 — Copy-never-link sanity

📸 Capture evidence for each query.

**Decision Gate A**
- If all pass → go to Phase 4
- If any fail → proceed to Phase 2

---

### PHASE 2 — Patch Decision Gate

For each failed check:
- [ ] Map to Patch ID (P1–P4)
- [ ] Record decision
- [ ] Get approval (verbal/written)

**NO AUTO PATCHING**

---

### PHASE 3 — Patch Application (If Approved)

For each approved patch:
1. [ ] Apply patch
2. [ ] Commit changes
3. [ ] Capture patch evidence
4. [ ] Re-run affected verification queries

**STOP if patch introduces new failure**

---

### PHASE 4 — Post-Verification

- [ ] Re-run all verification queries
- [ ] Ensure all G1–G4 checks pass
- [ ] Update verification checklist
- [ ] Sign execution summary

---

## 3) Exit Criteria

- [ ] All verification checks passed
- [ ] No orphan runtime data
- [ ] No master mutation paths
- [ ] Patch plan updated (if patches applied)
- [ ] Evidence archived

---

## 4) Emergency STOP Conditions

Immediately STOP if:
- Unexpected data mutation
- Query results contradict baseline
- Patch affects schema
- Performance degradation detected

Rollback immediately if needed.

---

## 5) Evidence Archive Structure

```
evidence/
  fundamentals/
    execution_window_YYYYMMDD/
      preflight/
      verification/
      patches/
      post_verification/
```

---

## 6) Execution Summary Template

**Execution Window ID:** _______________  
**Date / Time:** _______________  
**Participants:** _______________  

**Verification Results:**
- VQ-001: ⬜ PASS / ⬜ FAIL
- VQ-002: ⬜ PASS / ⬜ FAIL
- VQ-003: ⬜ PASS / ⬜ FAIL
- VQ-004: ⬜ PASS / ⬜ FAIL
- VQ-005: ⬜ PASS / ⬜ FAIL

**Patches Applied (if any):**
- P1: ⬜ Applied / ⬜ Not Applied
- P2: ⬜ Applied / ⬜ Not Applied
- P3: ⬜ Applied / ⬜ Not Applied
- P4: ⬜ Applied / ⬜ Not Applied

**Final Status:**
- ⬜ PASS
- ⬜ PASS WITH PATCHES
- ⬜ FAIL (Rollback)

**Signed By:** _______________  
**Date:** _______________

---

**END OF EXECUTION SOP**

