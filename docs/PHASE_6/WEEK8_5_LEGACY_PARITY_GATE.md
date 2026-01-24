# Week-8.5 Legacy Parity Gate Checklist (Hard Stop)

**Date:** 2026-01-XX  
**Status:** 🚨 HARD STOP CRITERIA  
**Objective:** Define finish line early — prevent feature creep past parity

---

## Gate Policy

**If any FAIL → Phase-6 stops feature expansion and enters parity-fix mode.**

---

## Parity Areas (Must Pass)

### 1. Quotation CRUD parity

- Create, open, update metadata, status flows (DRAFT → etc. if defined)

---

### 2. Panel/Feeder/BOM structure parity

- Add/edit/delete panel
- Feeder (level 0) behavior matches legacy expectations

---

### 3. Reuse parity (critical)

- Copy quotation
- Copy panel subtree
- Copy feeder
- Copy BOM subtree
- Post-copy editability intact

---

### 4. Pricing integrity (Phase-5 rules)

- Preview pricing works deterministically
- Apply-Recalc works with permissions (Reviewer/Approver)
- Manual override governance preserved (D-P5-003)

---

### 5. Canon compliance

- Schema Canon unchanged
- Guardrails unchanged

---

### 6. Output readiness

- Quotation summary export (even basic) matches legacy totals format expectations (internal)

---

## Required Evidence Set (for Week-8.5 sign-off)

- 3 sample quotations: baseline + copied + edited copy
- Screenshots/video of reuse workflows
- DB proof: no shared IDs + tracking fields
- Pricing preview/apply outputs logged with request_id
- Canon drift check PASS report

---

## Gate Decision Matrix

| Area | Status | Evidence | Sign-off |
|------|--------|----------|----------|
| Quotation CRUD | ⬜ | | |
| Panel/Feeder/BOM | ⬜ | | |
| Reuse | ⬜ | | |
| Pricing | ⬜ | | |
| Canon | ⬜ | | |
| Output | ⬜ | | |

**Overall Gate Status:** ⬜ PASS / ⬜ FAIL

---

## Gate Enforcement Rules

1. **No feature expansion** until all areas PASS
2. **Parity-fix mode** if any FAIL detected
3. **Evidence must be reviewable** (DB queries, screenshots, logs)
4. **Sign-off required** before proceeding to Phase-7

---

**This document prevents future arguments about "done enough"** ✅