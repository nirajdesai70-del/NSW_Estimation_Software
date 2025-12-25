# Phase Navigation Map (Canonical)

This diagram shows the **authoritative execution flow and dependencies**
from Fundamentals through Phase-2 and Phase-2.DR.

---

## High-Level Flow

```
Phase-0 (Fundamentals)
        │
        │  PASS (with notes)
        ▼
Phase-2 Window-A (Feeder Template Apply)
        │
        │  Gate-0: TEMPLATE_ID with N > 0 items
        │
        ├── PASS ───────────────▶ R1 → S1 → R2 → S2 → History → Phase-2 COMPLETE
        │
        └── FAIL (N = 0 items)
                 │
                 ▼
        Phase-2.DR (Feeder Template Data Readiness)
                 │
                 │  UI-based population of FEEDER template items
                 │  (No code / No DB scripts)
                 │
                 ├── PASS (N > 0)
                 │        │
                 │        ▼
                 │   Resume Phase-2 Window-A at R1
                 │
                 └── FAIL
                          │
                          ▼
                Data Readiness Issue (Templates / Item Master)
                Phase-2 remains BLOCKED
```

---

## Phase Responsibilities

### Phase-0 — Fundamentals Gap Correction

- Establish canonical model
- Validate schema + relationships
- Output: **Baseline truth**
- Status: PASS WITH NOTES

---

### Phase-2 Window-A — Feeder Template Apply Engine

- Purpose: **Behavioral validation**
  - Idempotency
  - Clear-before-copy
  - No duplicate stacking
  - Copy history integrity
- Hard Gate-0:
  - Requires FEEDER template with N > 0 items
- Status:
  - BLOCKED if Gate-0 fails
  - PASS only after full R1/S1/R2/S2

---

### Phase-2.DR — Feeder Template Data Readiness

- Purpose: **Unblock Phase-2**
- Scope:
  - UI-only feeder template population
- Forbidden:
  - Code changes
  - DB scripts
  - Phase-2 logic changes
- Output:
  - TEMPLATE_ID
  - ItemCount (N)
- Status:
  - PASS → Phase-2 resumes
  - FAIL → Phase-2 remains blocked

---

## Control Rules (Non-Negotiable)

- Phase-2 logic is **never modified** to fit missing data
- Phase-2.DR exists only to supply missing data
- Resume always happens at:
  **Phase-2 Window-A → R1**
- No phase bypassing
- No combined execution windows

---

## Authoritative Links

- Fundamentals Baseline:
  `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md`

- Phase-2 Window-A:
  `PLANNING/EXECUTION/PHASE2_WINDOWA_EXECUTION_SUMMARY.md`

- Phase-2.DR Plan:
  `PLANNING/RELEASE_PACKS/PHASE2/PHASE2_DR_FEEDER_TEMPLATE_DATA_READINESS_PLAN.md`

- Master Index:
  `PLANNING/MASTER_PLANNING_INDEX.md`

---

**End of Navigation Map**
