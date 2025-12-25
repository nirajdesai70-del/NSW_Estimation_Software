# Task Register — Phase 3 (Index + Standards)

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE (Planning Only)  
**Last Updated:** 2025-12-18 (IST)

---

## 1. Purpose

This register defines the **task governance standard** and acts as the **index** to all executable backlogs.

All executable work (Phase 4 onward) must be:
- registered as a task
- traceable to Phase 1 + Phase 2 artifacts
- governed by S0–S5 sequencing, risk gates, and approvals

**Rule:** No Task ID → No Work.

---

## 2. Task ID Standard (Single Source)

**NSW-P4-<S_STAGE>-<MODULE>-###**

Examples:
- NSW-P4-S0-GOV-001
- NSW-P4-S2-CIM-001
- NSW-P4-S4-QUO-005

---

## 3. Task Card Template (Canonical)

- `TASK_CARD_TEMPLATE.md`

This is the single template used for all tasks.

---

## 4. Authoritative Batch Files

Batch task lists are stored as separate files:

- `BATCH_1_S0_S1.md` — **Verification + Ownership (Batch-1)**
- `BATCH_2_S2.md` — **Isolation (Batch-2)**
- `BATCH_3_S3.md` — Alignment (Batch-3) *(to be created)*
- `BATCH_4_S4.md` — Propagation (Batch-4) *(to be created)*
- `BATCH_5_S5.md` — Regression Gate (Batch-5) *(to be created)*

---

## 5. Minimal Example Rows (Illustrative Only)

These are examples only. Real tasks live in batch files.

| Task ID | S-Stage | Module | Type | Risk | Gate | Objective |
|---|---|---|---|---|---|---|
| NSW-P4-S0-GOV-001 | S0 | GOV | Governance | LOW | G0 | Verify Phase 3 docs exist and links are correct |
| NSW-P4-S0-GOV-002 | S0 | GOV | Verification | HIGH | G3 | Confirm protected zone exists in nish (read-only evidence) |
| NSW-P4-S0-SHARED-001 | S0 | SHARED | Verification | HIGH | G3 | Map shared endpoints to bundles A/B/C |
| NSW-P4-S1-GOV-001 | S1 | GOV | Governance | MEDIUM | G2 | Confirm ownership/risk assigned for planned files |

---

## 6. References

- Phase 2 authority: `trace/phase_2/FILE_OWNERSHIP.md`
- Sequencing authority: `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- Gates authority: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Governance authority: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`
