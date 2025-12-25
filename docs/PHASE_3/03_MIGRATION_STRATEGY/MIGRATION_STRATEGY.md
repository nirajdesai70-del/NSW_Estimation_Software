# Migration Strategy — Phase 3

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE (Planning Only)  
**Date:** 2025-12-17 (IST)

---

## 1. Purpose

Define **how NSW evolves from NEPL (nish)** without breaking production stability.

This strategy ensures:
- No “big bang” rewrites
- No protected logic breakage
- Safe coexistence of legacy and NSW behavior
- Controlled, reversible execution

---

## 2. Migration Philosophy

### 2.1 Core Principle

> **NEPL continues to run. NSW evolves alongside it.**

- NSW does **not** replace NEPL instantly
- NSW logic is layered using wrappers, adapters, and guarded extensions
- All execution follows FILE_OWNERSHIP rules

---

## 3. Migration Modes

### 3.1 Wrapper Mode (Preferred)

Used for **PROTECTED and HIGH** risk files.

- Existing service/controller logic remains untouched
- New behavior introduced via:
  - service wrappers
  - feature flags
  - delegation patterns

**Example**
- CostingService remains unchanged
- NSW-specific costing rules wrap CostingService outputs

---

### 3.2 Parallel Mode

Used where both **legacy and NSW behavior must coexist**.

- Legacy path remains default
- NSW path is opt-in or condition-driven

**Example**
- Quotation Legacy vs Quotation V2 flows
- Import validation v1 vs NSW validation v2

---

### 3.3 Replace Mode (Controlled)

Used only for **LOW/MEDIUM** risk files after validation.

- Full replacement allowed
- Must pass standard test gates

---

## 4. What Must Never Be Migrated Directly

The following are **non-negotiable**:

- CostingService logic
- Quotation V2 hierarchy logic
- Discount rule evaluation
- DeletionPolicyService
- Core Eloquent models

These must always be **wrapped, not rewritten**.

---

## 5. Migration Flow (Stepwise)

### Step 1 — Planning

- Task created in TASK_REGISTER
- Risk level assigned
- Ownership verified

### Step 2 — Isolation

- Identify impacted files
- Confirm cross-module touchpoints
- Define rollback path

### Step 3 — Execution

- Apply wrapper/parallel/replace strategy
- Keep legacy path intact

### Step 4 — Validation

- Run module-level tests
- Run cross-module bundles if applicable

### Step 5 — Release

- Controlled deployment
- Monitoring enabled
- Rollback readiness confirmed

---

## 6. Migration Dependencies

| Upstream | Downstream |
|--------|-----------|
| Component/Item Master | Quotation, Master BOM |
| Master BOM | Quotation V2 |
| Feeder Library | Quotation V2 |
| Proposal BOM | Quotation V2 |
| Project | Quotation |
| Master (Org/Vendor/PDF) | Quotation, Project |

Downstream modules must **never be migrated before upstream stabilization**.

---

## 7. Rollback Strategy (Mandatory)

Every migration task must include:

- Feature flag or conditional switch
- Data safety verification
- Clear revert procedure

If rollback cannot be defined → task cannot start.

---

## 8. Migration Acceptance Criteria

A migration step is complete only if:
- Legacy behavior is still available
- NSW behavior is traceable
- No protected logic changed
- Tests pass as per risk category

---

## 9. References

- `trace/phase_2/FILE_OWNERSHIP.md`
- `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- `docs/PHASE_3/04_TASK_REGISTER/TASK_REGISTER.md`

