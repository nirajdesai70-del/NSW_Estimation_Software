# Phase-Wise Execution Checklist (Canonical)

This checklist defines **what must be true** to ENTER, EXECUTE, and EXIT each phase.
No phase may be skipped or partially executed.

---

## Phase-0 — Fundamentals Gap Correction

### Entry Criteria
- [ ] Fundamentals baseline bundle exists and frozen
- [ ] Schema mappings validated (live vs canonical)
- [ ] Verification queries defined (VQ-001 … VQ-005)
- [ ] Patch plan + SOP approved

### Execution
- [ ] Run VQ-001 (Feeder Master existence)
- [ ] Run VQ-002 (Master → Instance mapping)
- [ ] Run VQ-003 (Proposal BOM Master ownership)
- [ ] Run VQ-004 (No orphan runtime BOMs)
- [ ] Run VQ-005 (Copy-never-link sanity)

### Exit Criteria
- [ ] All VQs PASS (or PASS WITH NOTES)
- [ ] No patches applied OR patches logged + approved
- [ ] Phase-0 status recorded in planning index

**Status:** ✅ COMPLETE (PASS WITH NOTES)

---

## Phase-2 Window-A — Feeder Template Apply Engine

### Entry Criteria
- [ ] Phase-0 COMPLETE
- [ ] Canonical Feeder BOM execution flow locked
- [ ] Route + controller + engine wiring confirmed
- [ ] Execution approval signed
- [ ] Evidence folder created

### Gate-0 (MANDATORY)
- [ ] FEEDER template selected
- [ ] Template has N > 0 items in `master_bom_items`
- [ ] Gate-0 SQL evidence captured

### Execution (ONLY if Gate-0 PASS)
- [ ] R1 — First Apply
- [ ] S1 — Post-R1 verification
- [ ] R2 — Re-Apply (same parameters)
- [ ] S2 — Post-R2 verification
- [ ] History verification (2 records)

### Exit Criteria
- [ ] Idempotency proven
- [ ] Clear-before-copy proven
- [ ] No duplicates
- [ ] Copy history intact

**Status:** ⛔ BLOCKED (Gate-0 failed: data readiness)

---

## Phase-2.DR — Feeder Template Data Readiness (UI-First)

### Entry Criteria
- [ ] Phase-2 Window-A BLOCKED at Gate-0
- [ ] Phase-2.DR approval granted
- [ ] UI available for feeder template editing
- [ ] Evidence folders prepared

### Execution (UI ONLY)
- [ ] Select FEEDER template
- [ ] Add items via Feeder Library UI
- [ ] Save template
- [ ] Capture UI screenshots

### Verification
- [ ] Re-run Gate-0 query
- [ ] Confirm ItemCount (N) > 0
- [ ] Capture SQL evidence

### Exit Criteria
- [ ] TEMPLATE_ID locked
- [ ] ItemCount (N) locked
- [ ] Evidence archived
- [ ] Phase-2.DR marked PASS

**Status:** 📌 PLANNED (Execution pending)

---

## Phase-2 Window-A (Resume)

### Re-Entry Conditions
- [ ] Phase-2.DR PASS
- [ ] TEMPLATE_ID + N recorded
- [ ] No Phase-2 logic changes

### Resume Point
- [ ] Start at R1 (First Apply)
- [ ] Follow original Phase-2 execution checklist

---

## Control Rules (Global)

- [ ] No phase logic modified to fit missing data
- [ ] Data readiness handled ONLY in Phase-2.DR
- [ ] Resume always returns to the blocked gate
- [ ] All deviations logged in planning

---

**End of Phase-Wise Checklist**
