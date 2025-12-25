# Batch-5 — S5 Regression Gate (Final Readiness + Release Authorization)

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Batch:** B5  
**Coverage:** S5 (Regression Gate)  
**Status:** ACTIVE (Planning Only)  
**Last Updated:** 2025-12-18 (IST)

**Authority:**
- Risk/ownership: `trace/phase_2/FILE_OWNERSHIP.md`
- Sequencing: `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- Gates: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Governance: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`
- Propagation inputs: `docs/PHASE_3/04_TASK_REGISTER/BATCH_4_S4.md`

---

## 1. Batch Purpose

Batch-5 defines the **S5 Regression Gate** tasks that certify the system is safe to move from
**planning (Phase 3)** to **execution (Phase 4)**.

S5 focuses on:
- system-level regression readiness
- cross-module bundle validation
- rollback verification
- final go / no-go authorization

**Rule:** No execution may begin unless Batch-5 exit criteria are satisfied and approvals recorded.

---

## 2. Pre-Conditions (Must be true)

- Batches 1–4 (S0–S4) are complete and approved
- No unresolved ownership ambiguity exists
- All HIGH / PROTECTED tasks have rollback plans defined
- Wrapper seams and contracts are frozen (planning level)

If any prerequisite fails, Phase-4 execution is blocked.

---

## 3. Batch Task List (Authoritative)

| Task ID | S-Stage | Module | Sub-Area | Type | Risk | Gate | Objective (1 line) | In Scope (explicit) | Forbidden | Cross-Module Touchpoints | Evidence Required | Approvals Required | Rollback Required | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NSW-P4-S5-GOV-001 | S5 | GOV | Regression Matrix | Governance | HIGH | G3 | Compile system-level regression matrix from all prior batches | All B1–B4 batch artefacts | Any execution | All modules | Master regression matrix | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S5-GOV-002 | S5 | GOV | Bundle Validation | Governance | PROTECTED | G4 | Validate completeness of cross-module test bundles (A/B/C) | TESTING_GATES + Batch outputs | Running tests | Shared + QUO + BOM | Bundle coverage checklist | Arch: Yes / Exec: Yes / Release: Yes | Yes | Planned |
| NSW-P4-S5-GOV-003 | S5 | GOV | Rollback Certification | Governance | PROTECTED | G4 | Certify rollback feasibility for all HIGH/PROTECTED tasks | Rollback plans from B2–B4 | Executing rollback | All modules | Rollback certification sheet | Arch: Yes / Exec: Yes / Release: Yes | Yes (validated) | Planned |
| NSW-P4-S5-GOV-004 | S5 | GOV | Phase-4 Readiness | Governance | HIGH | G3 | Confirm Phase-4 execution prerequisites and freeze planning artefacts | All Phase-3 docs | Doc changes post-freeze | All modules | Readiness checklist + freeze note | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S5-QUO-001 | S5 | QUO | Apply-Flow Safety | Governance | PROTECTED | G4 | Certify safety of V2 apply flows under wrapper + contract model | Apply contracts + wrapper specs | Any logic change | Bundle A + B | Apply-flow safety checklist | Arch: Yes / Exec: Yes / Release: Yes | Yes (validated) | Planned |
| NSW-P4-S5-SHARED-001 | S5 | SHARED | Catalog & Reuse Safety | Governance | HIGH | G3 | Certify shared catalog & reuse flows under contract-first model | SHARED contracts + consumers | Execution | Legacy + V2 | Shared-flow safety checklist | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |

---

## 4. Batch-5 Outputs (Mandatory)

1. **System Regression Matrix**
   - mapping of modules × bundles × risk level
2. **Bundle Coverage Checklist**
   - Bundle A (Apply)
   - Bundle B (Costing / Quantity)
   - Bundle C (Catalog Validity)
3. **Rollback Certification Sheet**
   - HIGH / PROTECTED only
4. **Phase-4 Readiness & Freeze Note**
5. **Go / No-Go Decision Record**

---

## 5. Batch-5 Exit Criteria (Hard Gate)

Batch-5 is complete only when:
- All regression artefacts exist and are approved
- All bundles are accounted for (even if execution is deferred)
- Rollback feasibility is certified
- Planning artefacts are frozen
- Go / No-Go decision is explicitly recorded

Only after this gate:
- **Phase-3 closes**
- **Phase-4 execution may begin in nish**

---

## 6. Phase-3 Closure Statement

Upon completion of Batch-5:

> “Phase-3 Planning is complete. All execution must follow approved tasks, gates, and rollback doctrine.”

No further planning changes are permitted without reopening Phase-3 under governance control.


