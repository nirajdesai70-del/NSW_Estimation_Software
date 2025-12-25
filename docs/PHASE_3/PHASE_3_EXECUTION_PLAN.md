# PHASE 3 — EXECUTION PLAN

**NSW Estimation Software**  
**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE (Planning Only)  
**Date:** 2025-12-17 (IST)

---

## 1. Purpose of Phase 3

Phase 3 converts the frozen baselines (Phase 1) and traceability intelligence (Phase 2) into an executable, low-risk delivery roadmap for evolving NEPL Estimation Software into NSW Estimation Software.

Phase 3 does NOT involve coding.  
It defines how, when, and in what order changes will be executed safely.

---

## 2. What Phase 3 Is — and Is Not

Phase 3 IS:
- A controlled planning phase
- A decision-making and sequencing phase
- A risk-managed execution blueprint
- The bridge between documentation and delivery

Phase 3 IS NOT:
- Refactoring
- Feature development
- UI redesign
- Database changes
- “Quick fixes”

No code moves without completing Phase 3 deliverables.

---

## 3. Inputs Used for Phase 3

Phase 3 planning is grounded in completed artifacts:

**Phase 1 (Frozen Truth)**
- Baseline Freeze Register
- Module-wise frozen documentation
- Agreed module boundaries

**Phase 2 (Trace Intelligence)**
- ROUTE_MAP — route → controller → module
- FEATURE_CODE_MAP — feature → code → UI
- FILE_OWNERSHIP — ownership + risk classification

Phase 3 assumes all Phase 1 and Phase 2 artifacts are immutable.

---

## 4. Phase 3 Objectives

1. Define NSW target architecture (logical, not code-level)
2. Establish safe execution sequencing (S0–S5 control stages) and module prioritization within it
3. Convert trace data into actionable work packages
4. Enforce risk-based execution rules
5. Prevent accidental damage to PROTECTED logic
6. Enable parallel planning without cross-team conflict (execution remains sequential and gated)

---

## 5. NSW Target Architecture (Logical)

### Architectural Principles

1. **Frozen core, evolving edges**
   - Core business logic remains stable
   - Enhancements wrap, not replace
2. **Module ownership is absolute**
   - Each file has one accountable owner
   - Cross-module changes require coordination
3. **Reference-based masters**
   - No duplicated logic
   - One canonical owner per concept
4. **Trace-first execution**
   - Every change traces back to ROUTE_MAP and FILE_OWNERSHIP

---

## 6. Execution Sequencing (S0–S5) + Module Prioritization (MANDATORY)

Phase 3 uses **two aligned sequencing systems**, with a strict hierarchy:

- **Primary (control stages): S0–S5**
  - S0: Verification
  - S1: Ownership
  - S2: Isolation
  - S3: Alignment
  - S4: Propagation
  - S5: Regression Gate
- **Secondary (prioritization): Module Order**
  - Used **inside S2/S3/S4** to decide what to work on first, without changing the control-stage rules.

### S0–S5 Control Stages (Execution Control)

- **S0 — Verification**
  - Confirm Phase 1 baselines and Phase 2 trace artifacts are complete and treated as read-only inputs.
- **S1 — Ownership**
  - Confirm ownership + risk level (FILE_OWNERSHIP) for every planned file touched.
  - Declare hands-off (PROTECTED) areas and allowed patterns (wrapper/adapter).
- **S2 — Isolation**
  - Establish safe boundaries: module isolation, wrapper entry points, and “no-go” enforcement patterns.
- **S3 — Alignment**
  - Standardize interfaces and behaviors within agreed boundaries (without destabilizing protected logic).
- **S4 — Propagation**
  - Roll aligned patterns through dependent modules in dependency order (upstream → downstream).
- **S5 — Regression Gate**
  - Execute defined regression bundles (especially apply flows + costing integrity), collect evidence, and obtain approval for release.

### Module Order (Used inside S2/S3/S4)

This order minimizes blast radius and respects FILE_OWNERSHIP risk:

1. Dashboard / Shared / Ops
2. Master (Org / Vendor / PDF)
3. Employee / Role
4. Component / Item Master
5. Master BOM
6. Feeder Library
7. Proposal BOM
8. Quotation (Legacy)
9. Quotation V2 (always last)

The detailed mapping of **module ordering inside S2/S3/S4** is defined in:
- `02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`

---

## 7. Risk-Based Execution Rules

Risk Levels (from FILE_OWNERSHIP)

| Level | Meaning |
|---|---|
| PROTECTED | Core business logic — must not break |
| HIGH | Cross-module impact |
| MEDIUM | Module-scoped |
| LOW | Isolated |

Execution Rules
- **PROTECTED**
  - Written change justification
  - Mandatory regression testing
  - Explicit approval gate
- **HIGH**
  - Cross-module test plan
  - Rollback strategy
- **MEDIUM / LOW**
  - Normal test cycle

No exceptions.

---

## 8. Non-Negotiable Protected Areas

The following must not be modified directly without Phase-3 approval:
- CostingService (SUM(AmountTotal) rule)
- QuotationQuantityService
- QuotationV2Controller
- Core models:
  - Quotation
  - QuotationSale
  - QuotationSaleBom
  - QuotationSaleBomItem
  - MasterBom
  - MasterBomItem

Allowed approach: wrappers, adapters, decorators.

---

## 9. Phase 3 Deliverables

Phase 3 will produce:
1. Target Architecture Document
2. Refactor Sequence (S0–S5 control stages + module prioritization mapping)
3. Migration Strategy
4. Execution Rulebook (ACTIVE, FINAL) — `07_RULEBOOK/EXECUTION_RULEBOOK.md`
5. Task Register (Executable Backlog)
6. Risk Control Matrix
7. Testing & Release Gates

Each deliverable must be approved before any coding begins.

---

## 10. Phase 3 Working Method

For each module:

**Step 1 — Module Readiness Pack**
- Current state
- Frozen scope
- Ownership & risk summary
- Cross-module touchpoints

**Step 2 — Change Candidate Identification**
- What problems exist
- What improvements are allowed
- What is explicitly out-of-scope

**Step 3 — Work Package Definition**

Each task must include:
- File list
- Owner
- Risk level
- Test requirements

**Step 4 — Go / No-Go Gate**
- Risk reviewed
- Tests defined
- Approval recorded

---

## 11. Change Discipline

Before touching any file:
1. Check FILE_OWNERSHIP
2. Identify risk level
3. Check module dependencies
4. Confirm execution stage
5. Confirm approval requirement

No “small changes” bypass this process.

---

## 12. Phase Exit Criteria

Phase 3 is complete only when:
- All Phase 3 documents are finalized
- Task Register is approved
- Refactor order is locked
- Risk gates are signed off

Only then does Phase 4 (Execution) begin.

---

## 13. Summary

Phase 3 ensures that NSW evolution is:
- Predictable
- Auditable
- Safe
- Scalable

This phase converts knowledge into control.

---

**Phase 3 Status:** ACTIVE  
**Next Document:** `01_TARGET_ARCH/NSW_TARGET_ARCHITECTURE.md`

---

Next: Lane 3 — Task Decomposition (Task Cards) + Batch-1 Task Register population (S0 + S1).

