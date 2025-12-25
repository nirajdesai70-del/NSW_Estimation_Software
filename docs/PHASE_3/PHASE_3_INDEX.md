# Phase 3 Index — Planning & Roadmap

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE  
**Date:** 2025-12-17 (IST)

---

## 1. Purpose

This index is the single navigation entry for all Phase 3 planning artifacts.  
Phase 3 defines **what will change, in what order, under which gates**, without coding.

---

## 2. Phase 3 Core Documents

### A) Execution Plan

- `PHASE_3_EXECUTION_PLAN.md`

### B) Target Architecture

- `01_TARGET_ARCH/NSW_TARGET_ARCHITECTURE.md`

### C) Refactor Roadmap

- `02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`

### D) Execution Rulebook

- `07_RULEBOOK/EXECUTION_RULEBOOK.md`

### E) Migration Strategy

- `03_MIGRATION_STRATEGY/MIGRATION_STRATEGY.md`

### F) Task Register

- `04_TASK_REGISTER/TASK_REGISTER.md`
- `04_TASK_REGISTER/TASK_CARD_TEMPLATE.md`
- `04_TASK_REGISTER/BATCH_1_S0_S1.md`
- `04_TASK_REGISTER/BATCH_2_S2.md`

### G) Risk Control

- `05_RISK_CONTROL/RISK_CONTROL_MATRIX.md`

### H) Testing & Release Gates

- `06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`

---

## 3. How to Use Phase 3 (Working Method)

1. Start with **PHASE_3_EXECUTION_PLAN.md**
2. Confirm target constraints in **NSW_TARGET_ARCHITECTURE.md**
3. Follow execution sequencing in **REFACTOR_SEQUENCE.md** (S0–S5 control stages + module order mapping)
4. Register tasks in **TASK_REGISTER.md**
5. Apply risk controls and gates:
   - `RISK_CONTROL_MATRIX.md`
   - `TESTING_AND_RELEASE_GATES.md`
6. Only after task approval can execution begin in the live codebase.

---

## 4. Phase 3 Inputs (Read-Only References)

Phase 3 planning is derived from:

- Phase 1 baselines:
  - `docs/PHASE_1/BASELINE_FREEZE_REGISTER.md`
- Phase 2 trace maps:
  - `trace/phase_2/ROUTE_MAP.md`
  - `trace/phase_2/FEATURE_CODE_MAP.md`
  - `trace/phase_2/FILE_OWNERSHIP.md`

---

## 5. Phase Exit Criteria

Phase 3 is complete only when:
- Task Register has an approved first execution batch
- Risk and testing gates are agreed
- Refactor order is locked
- Rollback strategy exists for HIGH/PROTECTED tasks

---

**Owner:** Planning/Architecture  
**Next Step:** Convert approved tasks into Phase 4 execution sprints.

