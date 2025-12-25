# Batch-4 — S4 Propagation (Controlled Roll-Out of Aligned Contracts)

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Batch:** B4  
**Coverage:** S4 (Propagation)  
**Status:** ACTIVE (Planning Only)  
**Last Updated:** 2025-12-18 (IST)

**Authority:**
- Risk/ownership: `trace/phase_2/FILE_OWNERSHIP.md`
- Sequencing: `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- Gates: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Governance: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`
- Alignment inputs: `docs/PHASE_3/04_TASK_REGISTER/BATCH_3_S3.md`

---

## 1. Batch Purpose

Batch-4 defines **S4 Propagation tasks** to safely roll aligned interfaces and contracts across dependent modules.

S4 focuses on:
- propagating approved contracts into all consumers
- enforcing upstream → downstream order
- ensuring no partial adoption exists
- preparing the system for final regression gating (S5)

**Rule:** No semantic change. Propagation applies already-approved alignment only.

---

## 2. Pre-Conditions (Must be true)

- Batch-3 contract specs and alignment maps are approved
- Wrapper seam entry rules are frozen (PROTECTED)
- No unresolved ownership ambiguity remains

If any Batch-3 contract is not approved, dependent S4 tasks are blocked.

---

## 3. Batch Task List (Authoritative)

| Task ID | S-Stage | Module | Sub-Area | Type | Risk | Gate | Objective (1 line) | In Scope (explicit) | Forbidden | Cross-Module Touchpoints | Evidence Required | Approvals Required | Rollback Required | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NSW-P4-S4-GOV-001 | S4 | GOV | Propagation Control | Governance | MEDIUM | G2 | Define propagation order and “all-or-nothing” adoption rule | Module order + contracts | Parallel partial rollout | All modules | Propagation order doc | Arch: Yes / Exec: No / Release: No | No | Planned |
| NSW-P4-S4-SHARED-001 | S4 | SHARED | Contract Propagation | Propagation Planning | HIGH | G3 | Plan propagation of CatalogLookupContract to all consumers | Contract spec from Batch-3 | Changing logic | Legacy + V2 | Consumer adoption checklist | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-SHARED-002 | S4 | SHARED | Reuse Contract Propagation | Propagation Planning | HIGH | G3 | Plan propagation of ReuseSearchContract to all reuse consumers | Contract spec from Batch-3 | Changing logic | Reuse endpoints | Consumer adoption checklist | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-CIM-001 | S4 | CIM | Catalog Consumer Roll-Out | Propagation Planning | HIGH | G3 | Plan CIM consumer migration to SHARED CatalogLookupContract | CIM mapping from Batch-3 | Pricing logic change | Legacy + V2 | Roll-out sequence + checks | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-MBOM-001 | S4 | MBOM | Apply Contract Propagation | Propagation Planning | HIGH | G3 | Plan MBOM apply-contract propagation to all V2 entry points | MbomApplyContract | Apply behavior change | Bundle A (Apply) | Apply adoption checklist | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-FEED-001 | S4 | FEED | Apply Contract Propagation | Propagation Planning | HIGH | G3 | Plan Feeder apply-contract propagation to all V2 entry points | FeederApplyContract | Apply behavior change | Bundle A (Apply) | Apply adoption checklist | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-PBOM-001 | S4 | PBOM | Apply Contract Propagation | Propagation Planning | HIGH | G3 | Plan Proposal BOM apply-contract propagation | ProposalBomApplyContract | Apply behavior change | Bundle A (Apply) | Apply adoption checklist | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-QUO-001 | S4 | QUO | Legacy Consumer Propagation | Propagation Planning | HIGH | G3 | Plan legacy quotation migration to SHARED + BOM contracts | Legacy consumption map | Pricing change | Shared + BOM | Consumer migration plan | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S4-QUO-002 | S4 | QUO | V2 Wrapper Adoption | Propagation Planning | PROTECTED | G4 | Plan full adoption of wrapper entry points for V2 apply flows | Wrapper entry rules | Direct core edits | Bundle A + B | Wrapper adoption checklist | Arch: Yes / Exec: Yes / Release: Yes | Yes (validated) | Planned |

---

## 4. Batch-4 Outputs

1. Propagation order and dependency graph
2. Consumer adoption checklists per contract
3. Wrapper adoption checklist for V2
4. “All-or-nothing” propagation rule documentation
5. Ready-to-execute propagation plan for Phase 4

---

## 5. Batch-4 Exit Criteria

Batch-4 is complete when:
- All propagation plans are written and approved
- No consumer is left on a deprecated or partial contract path
- Rollback plans exist for every HIGH/PROTECTED propagation
- System is ready for final regression gating

Next batch:
- **Batch-5 — S5 Regression Gate task cards**


