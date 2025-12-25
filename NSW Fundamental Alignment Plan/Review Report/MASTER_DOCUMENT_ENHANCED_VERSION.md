# NSW Estimation Software — Master Project Documentation (ENHANCED VERSION)

**Project:** NSW Estimation Software  
**Origin:** Evolved from NEPL Estimation Software V2  
**Repository:** NSW_Estimation_Software  
**Document:** docs/NSW_ESTIMATION_MASTER.md  
**Version:** v2.2 (ENHANCED - Pending Freeze Approval)  
**Status:** Phase 4 Execution (In Progress) | Phase 5 Locked (Not Started)  
**Last Updated:** 2025-12-18

---

## Table of Contents

1. Executive Summary
2. Purpose and Vision
3. Terminology Lock
4. Layer Definitions (L0/L1/L2) ⭐ NEW
5. Governance Model
6. The 5-Phase Framework
7. Phase Details
8. Phase 5 Prerequisites ⭐ NEW
9. Outcomes and Deliverables
10. Risks, Challenges, and Blockers
11. Integration Requirements ⭐ NEW
12. Next Steps
13. References

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

---

## Layer Definitions (L0/L1/L2) ⭐ NEW SECTION

**Source:** NEPL_CANONICAL_RULES.md (FROZEN - Single Source of Truth)

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

### Copy-Never-Link Rule ⭐ CRITICAL

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
6. **Copy-never-link rule (see Layer Definitions)**

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
- **ALL Phase 5 Prerequisites are complete** ⭐ NEW

---

## Phase 5 Prerequisites ⭐ NEW SECTION

⚠️ **CRITICAL:** Phase 5 may NOT start until all prerequisites are complete.

### Prerequisite 1: NEPL_CANONICAL_RULES.md Review (MANDATORY FIRST STEP)

- **Time Required:** 2-3 hours
- **Status:** ⏳ PENDING
- **Action:** Read complete `NEPL_CANONICAL_RULES.md` (FROZEN document)
- **Location:** `NSW Fundamental Alignment Plan/FINAL_DOCUMENTS/SUMMARIES_AND_REVIEWS/CRITICAL_DOCUMENTS/NEPL_CANONICAL_RULES.md`
- **Deliverable:** NEPL rules alignment document
- **Why:** Contains single source of truth for L0/L1/L2 definitions, copy-never-link rule, and ProductType rules
- **Priority:** ⭐⭐⭐⭐⭐ CRITICAL

### Prerequisite 2: Fundamentals Pack Review

- **Time Required:** 4-7 hours
- **Status:** ⏳ PENDING
- **Action:** Review Priority 1 documents:
  - `MASTER_REFERENCE.md` (2-3 hours) - Complete layer documentation (9 layers A-I)
  - `GAP_REGISTERS_GUIDE.md` (1-2 hours) - Gap management framework
  - `ADOPTION_STRATEGIC_ANALYSIS.md` (1-2 hours) - Strategic evaluation
- **Location:** `NSW Fundamental Alignment Plan/`
- **Deliverable:** Fundamentals integration plan
- **Why:** Provides layer definitions, gap management framework, and implementation mapping
- **Priority:** ⭐⭐⭐⭐⭐ CRITICAL

### Prerequisite 3: Gap Register Review

- **Time Required:** 1-2 hours
- **Status:** ⏳ PENDING
- **Action:** Review gap registers:
  - `BOM_GAP_REGISTER.md` (Primary) - BOM-GAP-001 through BOM-GAP-013
  - `PROPOSAL_BOM_GAP_REGISTER_R1.md` - PB-GAP-001 through PB-GAP-004
  - `MASTER_BOM_GAP_REGISTER_R1.md` - MB-GAP-001 through MB-GAP-XXX
- **Location:** `NSW Fundamental Alignment Plan/FINAL_DOCUMENTS/SUMMARIES_AND_REVIEWS/GAP_REGISTERS/`
- **Deliverable:** Gap-to-layer mapping
- **Why:** Tracks critical gaps that must be addressed in Phase 5
- **Priority:** ⭐⭐⭐⭐ HIGH

### Prerequisite 4: Naming Convention Verification

- **Time Required:** 2-3 hours
- **Status:** ⏳ PENDING
- **Action:** Verify NSW alignment:
  - Column naming (PascalCase vs snake_case)
  - Table/model names
  - Code references
- **Deliverable:** Naming convention alignment document
- **Why:** Code references use NEPL naming (PascalCase) - must verify NSW alignment
- **Priority:** ⭐⭐⭐ MEDIUM

### Prerequisite 5: Code Reference Review

- **Time Required:** 3-4 hours
- **Status:** ⏳ PENDING
- **Action:** Review core BOM logic:
  - `BomEngine.php` (2-3 hours) - Core BOM service
  - `BomHistoryService.php` (1 hour) - History recording service
- **Location:** `NSW Fundamental Alignment Plan/FINAL_DOCUMENTS/CODE_AND_SCRIPTS/PHP_SERVICES/`
- **Deliverable:** BOM logic alignment document
- **Why:** Core BOM logic reference for NSW implementation
- **Priority:** ⭐⭐⭐⭐ HIGH

### Prerequisite 6: Governance Standards Review

- **Time Required:** 1-2 hours
- **Status:** ⏳ PENDING
- **Action:** Review governance standards:
  - `CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md`
  - `CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md`
- **Location:** `NSW Fundamental Alignment Plan/FINAL_DOCUMENTS/ADDITIONAL_STANDARDS/`
- **Deliverable:** Governance workflow alignment document
- **Why:** Provides governance workflow patterns for Phase 5
- **Priority:** ⭐⭐⭐ MEDIUM

**Total Prerequisites Time:** 13-20 hours

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

### Phase 5 Prerequisites - Verification Requirements ⭐ NEW

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

## Integration Requirements ⭐ NEW SECTION

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

**Deliverables:**
- BOM logic alignment document
- Method mapping to NSW requirements
- Verification pattern alignment

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

**Total Estimated Time:** 13-20 hours

**Week 1: Critical Document Review (4-6 hours)**
- [ ] NEPL_CANONICAL_RULES.md (2-3 hours) - **MANDATORY FIRST**
- [ ] BOM_GAP_REGISTER.md (1-2 hours)
- [ ] Governance workflow review (1 hour)

**Week 1-2: Verification (2-3 hours)**
- [ ] Naming convention verification (2-3 hours)

**Week 2: Code Review and Mapping (3-4 hours)**
- [ ] BomEngine.php review (2-3 hours)
- [ ] BomHistoryService.php review (1 hour)

**Week 2: Governance Standards Review (1-2 hours)**
- [ ] Cursor playbooks review (1 hour)
- [ ] Governance checklists review (1 hour)

**Week 2-3: Integration Execution (2-3 hours)**
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

### Core Project Documents

- `docs/NSW_ESTIMATION_BASELINE.md`
- `docs/PHASE_4/PHASE_4_EXIT_CHECKLIST.md`
- `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`
- `trace/phase_2/ROUTE_MAP.md`
- `trace/phase_2/FEATURE_CODE_MAP.md`
- `trace/phase_2/FILE_OWNERSHIP.md`
- `docs/GOVERNANCE/PROJECT_DECISION_LOG.md`

### Critical Documents (Phase 5 Prerequisites) ⭐ NEW

- **NEPL_CANONICAL_RULES.md** (FROZEN - must read first)
  - Location: `NSW Fundamental Alignment Plan/FINAL_DOCUMENTS/SUMMARIES_AND_REVIEWS/CRITICAL_DOCUMENTS/NEPL_CANONICAL_RULES.md`
  - Status: 🔒 FROZEN
  - Priority: ⭐⭐⭐⭐⭐ CRITICAL

- **BOM_GAP_REGISTER.md** (Primary gap register)
  - Location: `NSW Fundamental Alignment Plan/FINAL_DOCUMENTS/SUMMARIES_AND_REVIEWS/GAP_REGISTERS/BOM_GAP_REGISTER.md`
  - Status: ✅ Verified
  - Priority: ⭐⭐⭐⭐ HIGH

- **MASTER_REFERENCE.md** (Fundamentals Pack)
  - Location: `NSW Fundamental Alignment Plan/MASTER_REFERENCE.md`
  - Status: ✅ Reviewed
  - Priority: ⭐⭐⭐⭐⭐ CRITICAL

### Review Work Documents ⭐ NEW

- `NSW Fundamental Alignment Plan/Review Report/FUNDAMENTALS_REVIEW_REPORT.md`
- `NSW Fundamental Alignment Plan/Review Report/CODE_AND_STANDARDS_REVIEW_REPORT.md`
- `NSW Fundamental Alignment Plan/Review Report/FINAL_WORKING_PLAN.md`
- `NSW Fundamental Alignment Plan/Review Report/MASTER_DOCUMENT_FINAL_ANALYSIS.md`

---

**END OF ENHANCED MASTER DOCUMENT**

