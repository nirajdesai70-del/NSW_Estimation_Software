# NSW Estimation Software — Master Project Documentation

![Coverage](docs/badges/coverage.svg)

**Project:** NSW Estimation Software
**Origin:** Evolved from NEPL Estimation Software V2
**Repository:** NSW_Estimation_Software
**Document:** docs/NSW_ESTIMATION_MASTER.md
**Version:** v3.0 (FROZEN)
**Status:** Phase 4 Execution (In Progress) | Phase 5 Locked (Not Started)
**Last Updated:** 2025-12-18

**Freeze Criteria:** Allowed only after validation of internal consistency (Section: Gate Canon + Paths + Terminology Lock).

**Document Structure:** Core section must remain executive-readable; detailed registers live only in appendices.

---

## Table of Contents

1. Executive Summary
2. Purpose and Vision
3. Terminology Lock
4. Path Authority
5. Layer Definitions (L0/L1/L2)
6. Governance Model
7. The 5-Phase Framework
8. Phase-0 Foundation Track (Pre-Phase)
9. Phase Details
10. Resolution-B Implementation (Reference Only)
11. Panel BOM Planning Track (Planning Only)
12. Gap Register Summary
13. Verification Queries Index
14. Patch Register Summary
15. Phase 5 Prerequisites
16. Outcomes and Deliverables
17. Risks, Challenges, and Blockers
18. Integration Requirements
19. Next Steps
20. References
21. Appendices

---

## Executive Summary

NSW Estimation Software is a structured, risk-managed evolution of NEPL Estimation Software V2. The initiative exists to:
- Preserve existing functionality (zero regression objective)
- Document the current system comprehensively (baseline truth)
- Plan safe enhancements (additive only)
- Execute controlled changes with governance (gated execution)
- Extract requirements for the next-generation NSW system (Phase 5)

**Current position:** Phases 1–3 are complete (baseline, traceability, planning). Phase 4 is in progress (controlled execution). Phase 5 is locked until Phase-4 exit conditions are satisfied **AND all Phase 5 prerequisites are complete**.

---

## Purpose and Vision

### Primary Purpose

1. **Eliminate regression risk**
   Preserve NEPL V2 logic, calculations, and workflows.

2. **Create a single source of truth**
   Freeze baselines to prevent "meaning drift" and support audit-safe decisions.

3. **Enable safe evolution**
   Improve UI/UX and add capabilities without destabilizing production behavior.

4. **Improve system quality (additive)**
   Add validation, audit visibility, and non-blocking assistance (including AI suggestions).

### Vision

Transform NEPL Estimation Software V2 into NSW Estimation Software through a controlled, documented, and governed process that improves usability and capability without changing business logic.

---

## Terminology Lock

**NEPL:** Source system (frozen meaning)
**NSW:** Next-generation target system (Phase 5 onward)
**Baseline:** Git-tagged factual state used as governing truth
**PROTECTED:** Core business logic (wrapper-only changes allowed)
**Execution Window:** Governed scope block with evidence and rollback discipline

### Truth Level Badges

**Source:** PATCH_APPENDIX_v1.1.md

All schema/implementation references use these badges:

| Badge | Meaning |
|-------|---------|
| **CONFIRMED-IN-REPO** | Explicitly found in repository (migration/model/query file reference) |
| **INFERRED** | Hypothesis based on usage patterns or documentation references |
| **DOC-CLOSED** | Documentation/spec frozen; planning complete; no runtime validation |
| **RUN-CLOSED** | Verified via SQL/API requests + evidence archive; runtime validated |

**Rule:** Any table/field naming shown as schema is hypothesis unless backed by an explicit migration/model/query file reference. Hypotheses must be tagged as **INFERRED** and never treated as truth.

### Gate vs Round Terminology

**Rounds (Round-0/1/2)** are legacy verification workflow labels and are not phases or gates. Only G0–G5 govern execution.

---

## Path Authority

**Path Authority Declaration:**

- **NSW_Estimation_Software/** is the authoritative repo for execution (`docs/`, `trace/`, `features/`)
- **NSW Fundamental Alignment Plan/** is a read-only reference pack (fundamentals, gaps, code reviews)
- No files under the reference pack are executed directly

**Path Registry:** See References section for canonical path mappings.

---

## Layer Definitions (L0/L1/L2)

**Source:** NEPL_CANONICAL_RULES.md (FROZEN - Single Source of Truth)

**Complete Layer Structure (9 Layers A-I):**
- **A.** Category / Subcategory / Type(Item) / Attributes
- **B.** Item/Component List
- **C.** Generic Item Master (L0/L1)
- **D.** Specific Item Master (L2)
- **E.** Master BOM (generic, L1)
- **F.** Master BOM (specific) — **NOT FOUND IN REPO** (needs decision)
- **G.** Proposal BOM + Proposal Sub-BOM (L2)
- **H.** Feeder BOM
- **I.** Panel BOM

**Note:** Layer F (Master BOM specific) is **NOT FOUND IN REPO** and requires a decision on whether it exists or not.

**Decision Required:** Confirm whether Layer-F exists in live NEPL/production or is deprecated. Record outcome in `docs/GOVERNANCE/PROJECT_DECISION_LOG.md`.

### L0 = Generic Item Master (Functional Family)

- **Example:** MCC / MCCB / ACB
- **Characteristics:**
  - No technical specification
  - No make
  - No series
  - No SKU
- **ProductType:** 1 (Generic Product)
- **Usage:** Unique; never duplicated; never used directly in any BOM

### L1 = Technical Variant (Make-agnostic)

- **Example:** MCCB 25A, 25kA / 35kA / 50kA
- **Characteristics:**
  - Derived from L0 + technical spec set
  - Make-agnostic
- **ProductType:** 1 (Generic Product)
- **Usage:** Unique; never duplicated; reusable
- **Critical Rule:** **Master BOM operates at L1 only. Master BOM must not contain L2.**

### L2 = Catalog Item (Make + Series + SKU/Model)

- **Example:** Schneider / ABB / Siemens model variants
- **Characteristics:**
  - Derived from L1 + Make + Series (+ SKU/Model)
  - Make-specific
- **ProductType:** 2 (Specific Product)
- **Usage:** Unique; never duplicated; reusable
- **Critical Rule:** **Proposal/Specific BOM operates at L2 only. Proposal BOM = Quotation-specific instance.**

### Copy-Never-Link Rule

**Rule:** All BOM instances are independent copies. Never link Master BOM to quotations. Always copy.

**Enforcement:**
- Master BOM must never contain L2
- Master BOM must never link to quotations
- Proposal BOM must never link to Master BOM
- All instances are independent copies

**Source:** NEPL_CANONICAL_RULES.md (FROZEN)

---

## Governance Model

### Non-Negotiable Rules

1. **No Task ID → No Work**
2. **Baseline governs everything**
3. **PROTECTED logic = wrapper-only (no direct edits without G4)**
4. **Rollback must exist before HIGH/PROTECTED execution**
5. **Gate failure = immediate stop**
6. **Copy-never-link is mandatory (see Layer Definitions)**

### Decision Authority

If a decision is recorded in `docs/GOVERNANCE/PROJECT_DECISION_LOG.md`, it is final unless formally reversed via a new decision entry.

### Gate Canon (LOCKED)

Use this gate model everywhere:

| Gate | Meaning |
|------|---------|
| G0 | Governance / Planning |
| G1 | LOW risk execution |
| G2 | MEDIUM risk execution |
| G3 | HIGH risk execution |
| G4 | PROTECTED execution |
| G5 | Final Regression / Go-No-Go |

**Note:** Gate-0..Gate-5 naming in legacy references must be treated as equivalent to G0..G5.

---

## The 5-Phase Framework

```
Phase 1: Baseline Capture (✅ Complete)
    ↓
Phase 2: Traceability & Mapping (✅ Complete)
    ↓
Phase 3: Planning & Roadmap (✅ Complete)
    ↓
Phase 4: Controlled Execution (🔄 In Progress)
    ↓
Phase 5: NSW Extraction (🔒 Locked — Not Started)
```

### Framework Principles

1. Logic first, UI second
2. Additive only (no removal, no behavioral regression)
3. Baseline governs everything
4. Zero regression objective
5. Controlled execution (gates + evidence + rollback)
6. Copy-never-link rule (all instances are independent copies)

---

## Phase-0 Foundation Track (Pre-Phase)

**Status:** ✅ COMPLETE
**Purpose:** Fundamentals gap correction, documentation closure, and verification readiness
**Type:** Foundation Track (Pre-Phase) — not an execution phase

**Objective:** Establish fundamentals baseline, correct gaps, and prepare verification readiness before Phase 1 begins.

**Key Deliverables:**
- Fundamentals baseline bundle (FUNDAMENTALS_BASELINE_BUNDLE_v1.0)
- Gap correction status summary
- Verification queries (VQ-001 through VQ-005)
- Patch register (P1-P4) — conditional execution plan
- Fundamentals verification checklist

**Note:** Phase-0 is a foundation track that precedes Phase 1. It does not have exit gates like Phase 1-5. It establishes the foundation for all subsequent phases.

**Reference:** See `NSW Fundamental Alignment Plan/04_PHASES/PHASES_1_5_COMPLETE_REVIEW.md` for complete Phase-0 status.

---

## Phase Details

### Phase 1 — Baseline Capture ✅ COMPLETE

**Objective:** Establish a clean, factual snapshot of what exists.
**Date:** 2025-12-17

**Modules captured (8):**
- Component/Item Master
- Quotation
- Master BOM
- Feeder Library
- Proposal BOM
- Project
- Master
- Employee/Role

**Baseline tags (8):**
- BASELINE_COMPONENT_ITEM_MASTER_20251217
- BASELINE_QUOTATION_20251217
- BASELINE_MASTER_BOM_20251217
- BASELINE_FEEDER_LIBRARY_20251217
- BASELINE_PROPOSAL_BOM_20251217
- BASELINE_PROJECT_20251217
- BASELINE_MASTER_20251217
- BASELINE_EMPLOYEE_ROLE_20251217

---

### Phase 2 — Traceability & Mapping ✅ COMPLETE

**Objective:** Map features → routes → controllers → services → models → views/JS.
**Date:** 2025-12-17

**Key deliverables:**
- `trace/phase_2/ROUTE_MAP.md` (~80% coverage)
- `trace/phase_2/FEATURE_CODE_MAP.md`
- `trace/phase_2/FILE_OWNERSHIP.md` (52 files)

**Key findings:**
- 11 PROTECTED files
- 13 HIGH risk files
- Cross-module touchpoints identified (Quotation V2 apply/reuse flows)

---

### Phase 3 — Planning & Roadmap ✅ COMPLETE

**Objective:** Convert knowledge into executable, low-risk delivery plan.
**Date:** 2025-12-17 to 2025-12-18

**Control stages (S0–S5):**
- S0: Verification & Evidence
- S1: Ownership Lock
- S2: Isolation
- S3: Alignment
- S4: Propagation
- S5: Regression Gate

**Task batching model (B1–B5):**
- Batch 1: S0/S1
- Batch 2: S2
- Batch 3: S3
- Batch 4: S4
- Batch 5: S5

---

### Phase 4 — Controlled Execution 🔄 IN PROGRESS

**Objective:** Execute safe corrections and improvements in NEPL system under governance.

**Current progress:**
- S0: ✅ Complete (with conditions)
- S1: ✅ Complete
- S2: 🔄 In progress
- S3: ⏳ Planned
- S4: ⏳ Planned
- S5: ⏳ Planned

**Key deliverables:**
- `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`
- `docs/PHASE_4/S2_*_ISOLATION.md`
- `docs/PHASE_4/S3_*_ALIGNMENT.md`
- `docs/PHASE_4/S4_*_TASKS.md`
- `docs/PHASE_4/RISK_REGISTER.md`

**Phase 4 Exit (Mandatory for Closure)**

Phase 4 is considered CLOSED only when:
- S0–S5 are completed
- G5 Regression Gate is PASSED
- `docs/PHASE_4/PHASE_4_EXIT_CHECKLIST.md` is signed
- Phase-4 Closure Summary is frozen

---

### Phase 5 — NSW Extraction 🔒 LOCKED (NOT STARTED)

⚠️ **PHASE 5 IS ANALYSIS-ONLY**

**NO:**
- code changes
- DB changes
- refactoring
- bug fixes

Any execution in Phase-5 is a governance violation.

**Entry conditions (hard gate):**

Phase 5 may start ONLY after:
- Phase-4 Exit Checklist approval
- G5 Regression Gate PASSED
- Production stability confirmed
- Baselines updated and tagged
- **ALL Phase 5 Prerequisites are complete**

**Scope Fence:**

Phase 5 outputs are documents only. Any implementation must be registered as Phase 6+ or NSW Build Program, with separate baselines and gates.

---

## Resolution-B Implementation (Reference Only)

⚠️ **SCOPE FENCE:** Design + verification references only; no new implementation inside v3.0.

**Status:** ✅ CLOSED (Option-A Implemented + Runtime Verified)
**Date:** 2025-12-19
**Scope:** Proposal BOM (QuotationSaleBomItem) L2 write enforcement analysis

**Summary:**
Resolution-B identified all write paths, illegal defaults, and required fixes to enforce L2 (Specific Item) discipline for Proposal BOM writes. Option-A (Hard Enforcement) has been implemented and verified.

**Key Deliverables:**
- Write gateway design (`ProposalBomItemWriter` service)
- Write paths inventory (13+ locations migrated to gateway)
- Illegal defaults analysis (38+ instances resolved)
- Runtime verification (RB-2 = 0, RB-1 scoped to Proposal BOM = 0)

**Gap Closure:**
- ✅ **PB-GAP-001** — CLOSED (L2 write enforcement via gateway)
- ✅ **PB-GAP-002** — CLOSED (Illegal defaults removed)

**Reference:** See `NSW Fundamental Alignment Plan/05_DESIGN_DOCUMENTS/RESOLUTION_B/RESOLUTION_B_SUMMARY.md` for complete details.

---

## Panel BOM Planning Track (Planning Only)

⚠️ **SCOPE FENCE:** Planning artifacts only; execution gated by Panel BOM Gates Tracker.

**Status:** 📋 PLANNING COMPLETE (Execution Deferred)
**Track:** PB0-PB6
**Purpose:** Primary planning track for Panel BOM design layer aligned with Fundamentals + Feeder BOM governance

**Planning Phases:**
- **PB0:** Normalize & Lock Contracts ✅ COMPLETE
- **PB1:** Document Register + Index ✅ COMPLETE
- **PB2:** Backend Design ✅ COMPLETE
- **PB3:** Copy Operations Design ✅ COMPLETE
- **PB4:** Verification Queries ✅ COMPLETE
- **PB5:** Execution Window Pack ✅ COMPLETE
- **PB6:** Gate Tracker ✅ COMPLETE

**Key Deliverables:**
- Panel BOM canonical flow document
- Copy-never-link rules for Panel BOM
- Quantity contract verification
- Panel BOM document register (PB-DOC-001 through PB-DOC-013)
- Panel BOM gate tracker (Gate-0 through Gate-5)

**Execution Status:** ⏳ BLOCKED until execution window approval

**Reference:** See `NSW Fundamental Alignment Plan/05_DESIGN_DOCUMENTS/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` for complete planning details.

---

## Gap Register Summary

**Status:** ⏳ PENDING (See Appendix B for complete details)

**Top 12 High-Impact Gaps (Open / Partially Resolved):**

| Gap ID | Description | Status | Layer | Severity | Rule Violated |
|--------|-------------|--------|-------|----------|---------------|
| BOM-GAP-001 | Feeder Template Apply Creates New Feeder Every Time | ⏳ OPEN | H | High | Rule 1, 5 |
| BOM-GAP-002 | Feeder Template Apply Missing Clear-Before-Copy | ⏳ OPEN | H | High | Rule 1, 5 |
| BOM-GAP-004 | BOM Copy Operations Missing History/Backup | ⏳ PARTIALLY RESOLVED | E/G/H/I | High | Rule 4 |
| BOM-GAP-007 | Copy Operations Not Implemented | ⏳ PARTIALLY RESOLVED | E/G/H/I | High | Rule 1, 5 |
| BOM-GAP-013 | [Description] | ⏳ OPEN | - | High | - |
| BOM-GAP-005 | BOM Node Edits Missing History/Backup | ⏳ OPEN | E/G/H/I | Medium | Rule 4 |
| BOM-GAP-006 | Lookup Pipeline Preservation Not Verified | ⏳ OPEN | - | Medium | Rule 3 |
| PB-GAP-001 | L2 Write Enforcement Missing | ✅ CLOSED | G | Critical | - |
| PB-GAP-002 | Illegal Defaults (MakeId=0, SeriesId=0) | ✅ CLOSED | G | Critical | - |
| PB-GAP-003 | [Description] | ⏳ OPEN | G | - | - |
| PB-GAP-004 | [Description] | ⏳ OPEN | G | - | - |
| MB-GAP-001 | [Description] | ⏳ OPEN | E | - | - |

**Summary Statistics:**
- **Total Gaps:** 20+ (across BOM, Proposal BOM, Master BOM)
- **Open Gaps:** 10+
- **Partially Resolved:** 2
- **Closed Gaps:** 3+

**Complete Details:** See Appendix B: Complete Gap Register

**Source Documents:**
- `NSW Fundamental Alignment Plan/02_GOVERNANCE/BOM_GAP_REGISTER.md` (Primary)
- `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/PROPOSAL_BOM_GAP_REGISTER_R1.md`
- `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/MASTER_BOM_GAP_REGISTER_R1.md`

---

## Verification Queries Index

**Status:** ⏳ PENDING (See Appendix C for complete SQL)

**Verification Queries (VQ-001 through VQ-005):**

| Query ID | Purpose | Expected Result | Patch Trigger |
|----------|---------|----------------|---------------|
| **VQ-001** | Feeder Masters Exist | At least one Feeder Master exists | P1 or P4 |
| **VQ-002** | Feeder Master → Instance Relationship | No duplicate stacking | P3 |
| **VQ-003** | Proposal BOM Master Ownership | No orphan runtime entities | P2 |
| **VQ-004** | Orphan Runtime BOMs | All BOMs have valid MasterBomId | P2 |
| **VQ-005** | Template Type Consistency | All templates have valid TemplateType | P1 or P4 |

**Execution Order:** Execute queries in sequence (VQ-001 through VQ-005). If any query fails → proceed to patch decision gate.

**Complete SQL:** See Appendix C: Verification Queries

**Source:** `NSW Fundamental Alignment Plan/07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md`

---

## Patch Register Summary

**Status:** 📋 PLANNED (See Appendix D for complete details)

**Patch Register (P1-P4):**

| Patch ID | Patch Name | Trigger (Verification) | Status |
|----------|------------|------------------------|--------|
| **P1** | Feeder Template Filter Standardization | VQ-005 (unexpected non-FEEDER template usage) | PLANNED |
| **P2** | Quotation Ownership Enforcement | VQ-004 (QuotationId IS NULL) / VQ-003 ownership mismatch | PLANNED |
| **P3** | Copy-Never-Link Enforcement Guard | VQ-005 indicates master mutation risk | PLANNED |
| **P4** | Legacy Data Normalization (Last Resort) | Any systemic legacy corruption found | PLANNED |

**Patch Logging Rules:**
- If any patch is applied, it MUST be logged with evidence pointers
- Applied In Window, Commit/Ref, Evidence Path, Notes required
- If NO patches are applied: Leave Status = PLANNED, add note: "No patches triggered; baseline verified."

**Complete Details:** See Appendix D: Patch Register

**Source Documents:**
- `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_REGISTER.md`
- `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_PLAN.md`
- `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_INTEGRATION_PLAN.md`

---

## Phase 5 Prerequisites

⚠️ **CRITICAL:** Prerequisites are mandatory to satisfy Phase-5 entry gate.

### Prerequisite 1: NEPL_CANONICAL_RULES.md Review (MANDATORY FIRST STEP)

- **Effort:** Medium (2-5 hours)
- **Status:** ⏳ PENDING
- **Action:** Read complete `NEPL_CANONICAL_RULES.md` (FROZEN document)
- **Location:** See Path Registry: `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md`
- **Deliverable:** NEPL rules alignment document
- **Why:** Contains single source of truth for L0/L1/L2 definitions, copy-never-link rule, and ProductType rules
- **Priority:** ⭐⭐⭐⭐⭐ CRITICAL

### Prerequisite 2: Fundamentals Pack Review

- **Effort:** High (5-10 hours)
- **Status:** ⏳ PENDING
- **Action:** Review Priority 1 documents:
  - `MASTER_REFERENCE.md` - Complete layer documentation (9 layers A-I)
  - `GAP_REGISTERS_GUIDE.md` - Gap management framework
  - `ADOPTION_STRATEGIC_ANALYSIS.md` - Strategic evaluation
- **Location:** See Path Registry: `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_REFERENCE.md`
- **Deliverable:** Fundamentals integration plan
- **Why:** Provides layer definitions, gap management framework, and implementation mapping
- **Priority:** ⭐⭐⭐⭐⭐ CRITICAL

### Prerequisite 3: Gap Register Review

- **Effort:** Medium (2-5 hours)
- **Status:** ⏳ PENDING
- **Action:** Review gap registers:
  - `BOM_GAP_REGISTER.md` (Primary) - BOM-GAP-001 through BOM-GAP-013
  - `PROPOSAL_BOM_GAP_REGISTER_R1.md` - PB-GAP-001 through PB-GAP-004
  - `MASTER_BOM_GAP_REGISTER_R1.md` - MB-GAP-001 through MB-GAP-XXX
- **Location:** See Path Registry: `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/`
- **Deliverable:** Gap-to-layer mapping
- **Why:** Tracks critical gaps that must be addressed in Phase 5
- **Priority:** ⭐⭐⭐⭐ HIGH

### Prerequisite 4: Naming Convention Verification

- **Effort:** Medium (2-5 hours)
- **Status:** ⏳ PENDING
- **Action:** Verify NSW alignment:
  - Column naming (PascalCase vs snake_case)
  - Table/model names
  - Code references
- **Deliverable:** Naming convention alignment document
- **Why:** Code references use NEPL naming (PascalCase) - must verify NSW alignment
- **Priority:** ⭐⭐⭐ MEDIUM

### Prerequisite 5: Code Reference Review

- **Effort:** High (5-10 hours)
- **Status:** ⏳ PENDING
- **Action:** Review core BOM logic:
  - `BomEngine.php` - Core BOM service
  - `BomHistoryService.php` - History recording service
- **Location:** See Path Registry: `NSW Fundamental Alignment Plan/09_CODE_AND_SCRIPTS/PHP_SERVICES/`
- **Deliverable:** BOM logic alignment document
- **Why:** Core BOM logic reference for NSW implementation
- **Priority:** ⭐⭐⭐⭐ HIGH

**Code Locality Note:**
- Code references are in a documentation-only repository or separate codebase
- All code paths must be confirmed under the actual Laravel root
- Mapping remains provisional until verified
- Code references are **INFERRED** until verified (see Truth Level Badges)

### Prerequisite 6: Governance Standards Review

- **Effort:** Low (0.5-2 hours)
- **Status:** ⏳ PENDING
- **Action:** Review governance standards:
  - `CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md`
  - `CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md`
- **Location:** See Path Registry: `NSW Fundamental Alignment Plan/10_STANDARDS_AND_TEMPLATES/`
- **Deliverable:** Governance workflow alignment document
- **Why:** Provides governance workflow patterns for Phase 5
- **Priority:** ⭐⭐⭐ MEDIUM

---

## Outcomes and Deliverables

### Repository Structure (Reference)

```
NSW_Estimation_Software/
├── docs/
│   ├── NSW_ESTIMATION_BASELINE.md
│   ├── NSW_ESTIMATION_MASTER.md (this document)
│   ├── PHASE_1/
│   ├── PHASE_2/
│   ├── PHASE_3/
│   ├── PHASE_4/
│   └── PHASE_5/
├── features/
├── changes/
├── trace/
└── source_snapshot/
```

### Quantitative Summary (Single Source)

- Modules documented: 8
- Route coverage: ~80%
- Files classified by risk: 52
- PROTECTED files: 11
- Task batches: 5 (B1–B5)
- Control stages: 6 (S0–S5)

---

## Risks, Challenges, and Blockers

### Key Risks (Live)

1. **RISK-QUO-V2-001** — Route/Controller mismatch
   Blocks QUO-V2 isolation until re-verification passes.

2. **RISK-PROTECTED-001** — Protected core logic damage
   Controlled via wrapper-only + G4 approvals.

3. **RISK-CROSS-MODULE-001** — hidden dependencies
   Controlled via cross-module test bundles + G3/G4 gates.

4. **RISK-DATA-001** — Legacy master data attachment / upload mapping drift
   - **Issue:** Tavase basic tables not properly attached / legacy uploads may be mis-mapped
   - **Impact:** Catalog browsing, dropdown integrity, BOM reuse accuracy, reporting correctness
   - **Scope fence:** Not part of S4 Batch-2 (UI caller migration). Do not change schema/data/selection semantics inside S4 propagation work
   - **Next action:** Create controlled read-only audit task (DATA-INTEGRITY-001) after S4/S5 propagation stabilizes
   - **Status:** ⏳ DEFERRED (Post-S5)

### Phase 5 Prerequisites - Verification Requirements

**Alarms Raised (from comprehensive review):**

1. **Column Naming Convention Mismatch** (MEDIUM)
   - **Issue:** Code uses PascalCase (NEPL convention)
   - **Impact:** Need to verify NSW column naming alignment
   - **Mitigation:** Verify in NSW baseline (Prerequisite 4)
   - **Status:** ⏳ PENDING

2. **Table/Model Naming Mismatch** (MEDIUM)
   - **Issue:** Code references NEPL table/model names
   - **Impact:** Need to verify NSW table/model names
   - **Mitigation:** Verify in NSW baseline (Prerequisite 4)
   - **Status:** ⏳ PENDING

3. **Phase Reference Mapping** (LOW)
   - **Issue:** Code references Phase-1, Phase-2, Phase-3, Phase-4
   - **Impact:** Need to map to Phase 5
   - **Mitigation:** Map during code review (Prerequisite 5)
   - **Status:** ⏳ PENDING

4. **Round Structure Verification** (LOW)
   - **Issue:** Governance documents reference Round-0, Round-1, Round-2
   - **Impact:** Need to verify NSW round structure
   - **Mitigation:** Verify during governance review (Prerequisite 6)
   - **Status:** ⏳ PENDING

### Legacy Data Integrity (Deferred, Post-S5)

This is not to be fixed inside Phase-4 propagation.

**Future Phase:** DATA-INTEGRITY-AUDIT (READ-ONLY)

**Rules:**
- Evidence only
- No writes
- Separate approval
- Run only after Phase-4 stability

---

## Integration Requirements

### Fundamentals Pack Integration

**Status:** ⏳ PENDING (Prerequisite 2)

**Integration Points:**
- Layer definitions (9 layers A-I) from MASTER_REFERENCE.md
- Gap management framework from GAP_REGISTERS_GUIDE.md
- Implementation mapping from IMPLEMENTATION_MAPPING.md
- Adoption strategy from ADOPTION_STRATEGIC_ANALYSIS.md

**Deliverables:**
- Fundamentals integration plan
- Layer-to-requirement mapping
- Gap-to-layer mapping

### Gap Register Integration

**Status:** ⏳ PENDING (Prerequisite 3)

**Integration Points:**
- BOM_GAP_REGISTER.md (Primary) - BOM-GAP-001 through BOM-GAP-013
- PROPOSAL_BOM_GAP_REGISTER_R1.md - Proposal BOM gaps
- MASTER_BOM_GAP_REGISTER_R1.md - Master BOM gaps

**Deliverables:**
- Gap-to-layer mapping
- Gap tracking integration plan
- Gap closure criteria

### Code Reference Integration

**Status:** ⏳ PENDING (Prerequisite 5)

**Integration Points:**
- BomEngine.php - Core BOM logic patterns
- BomHistoryService.php - History recording patterns
- SQL verification scripts - Verification query patterns
- Execution mapping bridge (Screen → API → Service → DB)

**Deliverables:**
- BOM logic alignment document
- Method mapping to NSW requirements
- Verification pattern alignment
- Execution mapping documentation

### Governance Standards Integration

**Status:** ⏳ PENDING (Prerequisite 6)

**Integration Points:**
- Cursor execution playbooks
- Governance checklists
- Evidence templates

**Deliverables:**
- Governance workflow alignment document
- Checklist adaptation for NSW
- Template adaptation for NSW

---

## Next Steps

### Immediate (Phase 4)

1. Complete S2 Isolation
2. Execute S3 Alignment
3. Execute S4 Propagation
4. Complete S5 Regression Gate (G5)
5. Run Phase-4 Exit Checklist and freeze closure summary

### Phase 5 Preparation (Before Phase 5 Start)

**Week 1: Critical Document Review**
- [ ] NEPL_CANONICAL_RULES.md - **MANDATORY FIRST**
- [ ] BOM_GAP_REGISTER.md
- [ ] Governance workflow review

**Week 1-2: Verification**
- [ ] Naming convention verification

**Week 2: Code Review and Mapping**
- [ ] BomEngine.php review
- [ ] BomHistoryService.php review

**Week 2: Governance Standards Review**
- [ ] Cursor playbooks review
- [ ] Governance checklists review

**Week 2-3: Integration Execution**
- [ ] Fundamentals Pack integration
- [ ] Gap register integration
- [ ] Code reference integration
- [ ] Governance standards integration

### After Phase-4 Exit (Phase 5)

1. Start NSW extraction (analysis-only)
2. Publish NSW requirements and migration plan
3. Create "Do Not Repeat" register
4. Plan NSW build as a separate governed program

---

## References

### Top Authority (Governing Documents)

1. **NEPL_CANONICAL_RULES.md** (FROZEN)
   - Single source of truth for L0/L1/L2 definitions and copy-never-link rule
   - Location: See local repo folder: `FINAL_DOCUMENTS/SUMMARIES_AND_REVIEWS/CRITICAL_DOCUMENTS/NEPL_CANONICAL_RULES.md`

2. **NSW_ESTIMATION_BASELINE.md** (FROZEN)
   - Baseline truth for all modules
   - Location: `docs/NSW_ESTIMATION_BASELINE.md`

3. **PHASE_4_EXIT_CHECKLIST.md** (mandatory gate)
   - Phase 4 exit requirements
   - Location: `docs/PHASE_4/PHASE_4_EXIT_CHECKLIST.md`

### Core Project Documents

- `docs/NSW_ESTIMATION_BASELINE.md`
- `docs/PHASE_4/PHASE_4_EXIT_CHECKLIST.md`
- `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`
- `trace/phase_2/ROUTE_MAP.md`
- `trace/phase_2/FEATURE_CODE_MAP.md`
- `trace/phase_2/FILE_OWNERSHIP.md`
- `docs/GOVERNANCE/PROJECT_DECISION_LOG.md`

### Critical Documents (Phase 5 Prerequisites)

- **NEPL_CANONICAL_RULES.md** (FROZEN - must read first)
  - Location: See Path Registry: `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md`
  - Status: 🔒 FROZEN
  - Priority: ⭐⭐⭐⭐⭐ CRITICAL

- **BOM_GAP_REGISTER.md** (Primary gap register)
  - Location: See Path Registry: `NSW Fundamental Alignment Plan/02_GOVERNANCE/BOM_GAP_REGISTER.md`
  - Status: ✅ Verified
  - Priority: ⭐⭐⭐⭐ HIGH

- **MASTER_REFERENCE.md** (Fundamentals Pack)
  - Location: See Path Registry: `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_REFERENCE.md`
  - Status: ✅ Reviewed
  - Priority: ⭐⭐⭐⭐⭐ CRITICAL

- **PATCH_REGISTER.md** (Patch tracking)
  - Location: See Path Registry: `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_REGISTER.md`
  - Status: 📋 PLANNED
  - Priority: ⭐⭐⭐⭐ HIGH

- **PATCH_PLAN.md** (Conditional patch execution plan)
  - Location: See Path Registry: `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_PLAN.md`
  - Status: 📋 PLANNED
  - Priority: ⭐⭐⭐ MEDIUM

- **PATCH_INTEGRATION_PLAN.md** (Patch integration approach)
  - Location: See Path Registry: `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_INTEGRATION_PLAN.md`
  - Status: 📋 PLANNED
  - Priority: ⭐⭐⭐ MEDIUM

### Review Work Documents

- See Path Registry: `NSW Fundamental Alignment Plan/08_REVIEWS_AND_ANALYSIS/`
  - FUNDAMENTALS_REVIEW_REPORT.md
  - FINAL_WORKING_PLAN.md
  - MASTER_DOCUMENT_FINAL_ANALYSIS.md
  - GAP_REFERENCES_ANALYSIS_AND_INTEGRATION_PLAN.md

---

## Path Registry

**Canonical Path Mappings:**

| Document Category | Path |
|-------------------|------|
| **Fundamentals** | `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/` |
| **Governance** | `NSW Fundamental Alignment Plan/02_GOVERNANCE/` |
| **Gap Registers** | `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/` |
| **Phases** | `NSW Fundamental Alignment Plan/04_PHASES/` |
| **Design Documents** | `NSW Fundamental Alignment Plan/05_DESIGN_DOCUMENTS/` |
| **Patches** | `NSW Fundamental Alignment Plan/06_PATCHES/` |
| **Verification** | `NSW Fundamental Alignment Plan/07_VERIFICATION/` |
| **Reviews & Analysis** | `NSW Fundamental Alignment Plan/08_REVIEWS_AND_ANALYSIS/` |
| **Code & Scripts** | `NSW Fundamental Alignment Plan/09_CODE_AND_SCRIPTS/` |
| **Standards & Templates** | `NSW Fundamental Alignment Plan/10_STANDARDS_AND_TEMPLATES/` |
| **Master Index** | `NSW Fundamental Alignment Plan/00_INDEX.md` |

**NSW Execution Repo:**
- `NSW_Estimation_Software/docs/` — Execution documents
- `NSW_Estimation_Software/trace/` — Traceability maps
- `NSW_Estimation_Software/features/` — Feature documentation

---

## Appendices

### Appendix A: Complete 9-Layer Architecture

**Location:** See `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_REFERENCE.md`

Complete documentation of all 9 layers (A-I) with purposes, definitions, relationships, and layer-to-gap mapping.

---

### Appendix B: Complete Gap Register

**Location:** See `NSW Fundamental Alignment Plan/02_GOVERNANCE/BOM_GAP_REGISTER.md` and related gap registers

Complete gap register with:
- All gaps with complete details
- Gap-to-rule mapping table
- Gap-to-phase mapping table
- Gap-to-layer mapping table
- Gap-to-verification query mapping table
- Gap-to-patch mapping table

---

### Appendix C: Verification Queries

**Location:** See `NSW Fundamental Alignment Plan/07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md`

Complete SQL queries (VQ-001 through VQ-005) with:
- Full SQL text
- Query purposes and expected results
- Query-to-gap mapping
- Query-to-patch mapping

---

### Appendix D: Patch Register

**Location:** See `NSW Fundamental Alignment Plan/06_PATCHES/PATCH_REGISTER.md`

Complete patch register with:
- Patch register table (P1-P4)
- Patch trigger conditions
- Patch logging rules
- Patch-to-gap mapping

---

### Appendix E: Layer-to-Gap Mapping

**Location:** See gap registers in `NSW Fundamental Alignment Plan/02_GOVERNANCE/` and `03_GAP_REGISTERS/`

Complete mapping of gaps to layers:
- Layer-specific gap tracking
- Layer-specific gap closure criteria
- Layer-to-requirement mapping

---

**END OF DOCUMENT**
