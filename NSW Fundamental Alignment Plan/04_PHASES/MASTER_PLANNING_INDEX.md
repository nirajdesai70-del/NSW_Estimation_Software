<!-- LOCKED: CANONICAL PLANNING INDEX -->
<!-- RULE: Edit only via Change Control (Section 9) -->
<!-- RULE: No runtime actions from this doc -->

# MASTER_PLANNING_INDEX.md

**Project:** NSW Estimation Software  
**Mode:** 📋 PLANNING ONLY (No runtime execution)  
**Date:** 2025-12-21  
**Canonical Location:** `PLANNING/MASTER_PLANNING_INDEX.md`  
**Lock State:** 🔒 LOCKED (reference-only; update only through Section 9)

---

## 0) Governance Rules (Locked)

- ⛔ Do NOT modify `/Users/nirajdesai/Projects/nish` (runtime workspace)
- ✅ All work happens in planning artifacts only
- ✅ Runtime activity is allowed only inside an approved execution window
- ✅ Gate status meanings:
  - **PASS** → Evidence captured (runtime validation complete)
  - **READY** → Planning complete; no runtime work; evidence not captured
  - **BLOCKED** → Execution window required (gates remain READY until execution approval)
  - **PLANNED** → Not yet packaged
- ✅ This file is the single source of truth for phase state

---

## 1) Phase Summary (One-Glance)

| Phase | Scope | Status | Notes |
|-------|-------|--------|-------|
| **Phase-0** | Fundamentals gap correction | 📌 **READY** | Baseline freeze + verification + conditional patching (planning complete) |
| **Phase-1** | History foundation | ✅ **PASS** | History foundation evidence recorded (copy history schema verified) |
| **Phase-2** | Feeder template apply engine | ✅ **PLANNING COMPLETE** | Planning fully complete; execution BLOCKED at Gate-0 (data readiness); Phase-2.DR unblock path ready |
| **Phase-3** | BOM-node history + restore | 📌 **READY** | Gate-1 planning complete, Gate-2/3 blocked until execution window |
| **Phase-4** | Lookup pipeline + integrity | 📌 **READY** | Gate-1 planning complete, Gate-2/3 blocked until execution window |
| **Phase-5** | Hardening + audit + freeze | 📌 **READY** | Gate-1 planning complete, Gate-2/3 blocked until execution window |
| **Panel BOM** | Panel Master → Proposal Panel copy | ✅ **PLANNING COMPLETE** | PB0-PB6 complete, execution BLOCKED until approval |

---

## 2) Phase-0 — Fundamentals Gap Correction

### Objective
- Freeze fundamentals baseline (Feeder Master, Proposal BOM Master, hierarchy, mapping)
- Verify alignment with runtime via read-only queries
- Apply conditional patches only if verification fails
- Establish fundamentals as Phase-0 foundation

**Status:** 📌 **READY** (Planning Complete)

### Canonical Pack
```
PLANNING/RELEASE_PACKS/FUNDAMENTALS/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 02_VERIFICATION/
│  ├─ VERIFICATION_QUERIES.md
│  └─ VERIFICATION_CHECKLIST.md
├─ 03_PATCHES/
│  ├─ PATCH_PLAN.md
│  └─ PATCH_REGISTER.md
└─ 04_RISKS_AND_ROLLBACK.md
```

### Baseline Bundle
- **Location:** `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` (to be frozen)
- **Includes:** Feeder Master mapping, Proposal BOM Master mapping, hierarchy, mapping table, rules

### Verification Pack
- **Location:** `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` (to be frozen)
- **Location:** `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` (to be frozen)

### Patch Pack
- **Location:** `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (✅ frozen)
- **Location:** `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md` (✅ frozen)
- **Location:** `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md` (to be created)

### Gate State
- **Gate G-A:** ⏳ PENDING (Baseline + Verification + Patch + SOP + Register freeze)
- **Gate G-B:** ⏳ PENDING (Patch governance embedded in fundamentals docs)
- **Gate G-C:** ⏳ PENDING (Integration with master planning system)
- **Gate G-D:** ⏳ PENDING (Fundamentals release pack created)
- **Gate G-E:** ⏳ BLOCKED (Execution window - requires approval)

### Gap Mapping
- **BOM-GAP-001:** Feeder Template Apply Creates New Feeder Every Time (No Reuse Detection)
  - Closure path: Verification (VQ-001/VQ-002) + conditional patch P1/P3
- **BOM-GAP-002:** Feeder Template Apply Missing Clear-Before-Copy (Duplicate Stacking)
  - Closure path: Verification (VQ-002) + conditional patch P3
- **BOM-GAP-005:** BOM Node Edits Missing History/Backup (planned for Phase-3)
  - Reference: Fundamentals baseline documents hierarchy rules
- **BOM-GAP-006:** Lookup Pipeline Preservation Not Verified After Copy
  - Closure path: Verification (VQ-005) + conditional patch P3

### Execution Framework
- **SOP:** `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- **Tracker:** `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_SERIAL_TRACKER_v1.0.md`
- **Mode:** Read-only verification first, conditional patching only if needed

### Rule
- ❌ No runtime/DB/UI work until execution window approved
- ✅ Planning artifacts must be frozen (v1.0) before execution
- ✅ Verification queries are read-only (no data mutation)

---

## 3) Phase-1 — History Foundation

### Objective
- Establish immutable history recording
- Prove copy-never-link pattern

**Status:** ✅ **PASS**

### Artifacts
- `evidence/PHASE2/G1_bom_copy_history_schema.txt` (schema verification)
- `bom_copy_history` schema verified

**Note:** Evidence file is stored under PHASE2 folder due to implementation timeline; it is Phase-1 foundation evidence.

### Locked Outcome
- History layer exists
- No further Phase-1 work allowed

---

## 4) Phase-2 — Feeder Template Apply

### Objective
- Idempotent feeder creation
- Clear-before-copy semantics
- Full audit trail

**Status:** ✅ **PLANNING COMPLETE** (Final Closure: 2025-12-22)

**Final Closure Statement:**  
Phase-2 (Feeder Template Apply) planning is COMPLETE.  
Execution is BLOCKED at Gate-0 due to FEEDER template data readiness.  
Unblock path is Phase-2.DR (UI-first).  
No further Phase-2 planning remains.

### Canonical Pack

```
PLANNING/RELEASE_PACKS/PHASE2/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 01_ARCH_DECISIONS.md
├─ 02_BOM_ENGINE_CONTRACT.md
├─ 03_APPLY_FEEDER_TEMPLATE_IO.json
├─ 04_EXECUTION_SCRIPTS/
├─ 05_VERIFICATION/
└─ 06_RISKS_AND_ROLLBACK.md
```

### Gate State
- **Gate-1:** ✅ PASS (schema evidence)
- **Gate-2:** 📌 READY (runtime endpoint confirmed, no execution)
- **Gate-3:** 📌 READY (R1/S1/R2/S2 scripts ready)

### Phase-2.DR — Feeder Template Data Readiness (UI-First)

**Status:** 📌 READY (Planning Complete)  
**Execution:** ⛔ BLOCKED until approval  
**Reason:** Phase-2 Gate-0 failed — FEEDER templates have zero items

**Objective:**
Populate at least one FEEDER template with N > 0 items using Feeder Library UI, enabling Phase-2 Window-A execution.

**Mode:**
- UI-based data entry only
- No code changes
- No DB scripts
- Evidence-driven execution

**Canonical Plan:**
`PLANNING/RELEASE_PACKS/PHASE2/PHASE2_DR_FEEDER_TEMPLATE_DATA_READINESS_PLAN.md`

**Approval Pack:**
- `EXECUTION_APPROVAL_PHASE2_DR.md`
- `PHASE2_DR_PREFLIGHT.md`
- `PHASE2_DR_EXECUTION_SUMMARY.md`

**Re-entry Point:**
On PASS, resume **Phase-2 Window-A** with selected TEMPLATE_ID and ItemCount (N).

↔ Phase-2 Window-A execution and Phase-2.DR are formally cross-linked; Phase-2 resumes only after Phase-2.DR PASS.

### Planning Closure (2025-12-22)

**Planning Status:** ✅ COMPLETE

All planning deliverables are complete:
- ✅ Architecture & Logic (idempotency, clear-before-copy, duplicate prevention)
- ✅ Contracts & Interfaces (API routes, BomEngine methods, error handling)
- ✅ Verification & Evidence (Gate-0, R1/R2 queries, evidence structure)
- ✅ Governance & Documentation (execution approvals, runbooks, cross-links)
- ✅ Data Readiness Handling (Phase-2.DR planned and approved)

**Execution Status:** ⛔ BLOCKED at Gate-0 (data readiness)

### Rule
- ❌ No more runtime/UI/DB work until execution window

**Note:** Phase-2 execution is BLOCKED at Gate-0 due to FEEDER template data readiness; Phase-2.DR (UI-first) planned to populate templates before resuming Window-A.

---

## 5) Phase-3 — BOM Node History & Restore

### Objective
- Track structural BOM edits (rename, qty, reparent, activate/deactivate)
- Enable history-safe restore (point-in-time)
- Provide audit trail for BOM node operations

### Deliverables
- BOM node history table (`quotation_sale_bom_node_history`)
- Restore semantics (point-in-time with optional cascade)
- Verification queries and evidence structure
- BomEngine integration contracts

**Status:** 📌 **READY** (Planning Complete - 2025-12-22)

### Canonical Pack
```
PLANNING/RELEASE_PACKS/PHASE3/
├─ 00_README_RUNBOOK.md - Execution guide
├─ 00_SCOPE_LOCK.md - Scope boundaries
├─ STATUS.md - Current status and gates
├─ 01_ARCH_DECISIONS.md - Architecture decisions (ADRs)
├─ 02_EVENT_MODEL.md - Event types and semantics
├─ 03_SCHEMA_NODE_HISTORY.md - Table schema design
├─ 04_BOMENGINE_NODE_OPS_CONTRACT.md - Method contracts
├─ 05_VERIFICATION/ - Verification SQL
│  ├─ NODE_HISTORY_VERIFICATION.sql
│  └─ RESTORE_VERIFICATION.sql
├─ 06_RISKS_AND_ROLLBACK.md - Risk assessment
└─ PHASE3_PLANNING_PACK_V1.0.md - Complete planning summary
```

### Planning Completion (2025-12-22)

**Planning Status:** ✅ COMPLETE

All planning deliverables are complete:
- ✅ Event model defined (6 event types)
- ✅ History table schema designed (PascalCase, append-only)
- ✅ Restore semantics documented (point-in-time, optional cascade)
- ✅ BomEngine methods designed (node operations with history)
- ✅ Verification SQL queries created
- ✅ Architecture decisions documented (5 ADRs)
- ✅ Scope locked (explicit boundaries)
- ✅ Risks and rollback procedures defined

**Execution Status:** ⏳ BLOCKED until approval

### Gate State
- **Gate-1:** 📌 READY (planning completeness verified - all artifacts complete)
- **Gate-2:** ⏳ BLOCKED (implementation window - requires execution approval)
- **Gate-3:** ⏳ BLOCKED (verification - requires Gate-2 completion)

### Independence

Phase-3 is **independent of Phase-2 execution**:
- ✅ No dependency on Phase-2 data readiness
- ✅ No dependency on Phase-2.DR completion
- ✅ Can proceed in parallel (planning already complete)
- ✅ Execution will be clean, reversible, auditable

### Rule
- ❌ No runtime/DB/UI work until execution window
- ✅ Planning artifacts are complete and ready for approval

---

## 6) Phase-4 — Lookup Pipeline Verification

### Objective
- Verify lookup pipeline integrity after copy/reuse/edit
- Ensure line items remain fully editable with full master-data lookup preserved
- Detect and repair broken lookup chains

**Status:** 📌 **READY** (Planning Complete)

### Canonical Pack
```
PLANNING/RELEASE_PACKS/PHASE4/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 01_SCOPE_LOCK.md
├─ 02_LOOKUP_INTEGRITY_RULES.md
├─ 03_SCHEMA_OPTIONAL_AUDIT_TABLE.md
├─ 04_VERIFICATION/
│  └─ LOOKUP_INTEGRITY_VERIFICATION.sql
├─ 05_FAILURE_MODES_AND_REPAIR.md
└─ 06_RISKS_AND_ROLLBACK.md
```

### Gate State
- **Gate-1:** 📌 READY (planning completeness verified)
- **Gate-2:** ⏳ BLOCKED (implementation window - requires execution approval)
- **Gate-3:** ⏳ BLOCKED (verification - requires Gate-2 completion)

### Gap Mapping
- **BOM-GAP-006:** Lookup Pipeline Preservation Not Verified After Copy
  - Closure path: Verification SQL + repair playbook (Gate-3 evidence)

### Rule
- ❌ No runtime/DB/UI work until execution window

---

## 7) Phase-5 — Hardening & Freeze

### Objective
- System-wide consistency
- Audit completeness
- Release freeze

**Status:** 📌 **READY** (Planning Complete)

### Canonical Pack
```
PLANNING/RELEASE_PACKS/PHASE5/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 00_SCOPE_LOCK.md
├─ 01_CROSS_PHASE_AUDIT_CHECKLIST.md
├─ 02_FREEZE_CHECKLIST.md
├─ 03_RELEASE_READINESS_CRITERIA.md
└─ 04_FINAL_ROLLBACK_POLICY.md
```

### Gate State
- **Gate-1:** 📌 READY (planning completeness verified)
- **Gate-2:** ⏳ BLOCKED (execution window - requires execution approval)
- **Gate-3:** ⏳ BLOCKED (freeze declaration - requires Gate-2 completion)

### Deliverables (Complete)
- [x] Cross-phase audit checklist
- [x] Freeze checklist
- [x] Release readiness criteria
- [x] Final rollback policy
- [x] Release pack structure

### Rule
- ❌ No runtime/DB/UI work until execution window

---

## 7.5) Panel BOM Planning Track (PB0-PB6)

### Objective
- Panel Master → Proposal Panel copy operations
- Panel → Feeder → BOM → Item hierarchy verification
- Quantity contract enforcement (Panel qty multiply once)
- Lookup integrity verification (Panel → Feeder → Item chain)

**Status:** ✅ **PLANNING COMPLETE** (2025-12-23)

### Canonical Pack
```
PLANNING/PANEL_BOM/
├─ PANEL_BOM_PLANNING_TRACK.md - Main planning track (PB0-PB6)
├─ PANEL_BOM_TODO_TRACKER.md - Cursor-ready TODO tracker
├─ PANEL_BOM_DOCUMENT_REGISTER.md - Document registry
├─ GATES_TRACKER.md - Verification gates (Gate-0 through Gate-5)
├─ CANONICAL_FLOW.md - Canonical runtime + design-time hierarchy (PB0.1)
├─ COPY_RULES.md - Copy-never-link + PanelMasterId reference-only (PB0.2)
├─ QUANTITY_CONTRACT.md - Quantity multiplication contract (PB0.3)
├─ GATE4_ROLLUP.md - Gate-4 rollup verification plan
├─ GATE5_LOOKUP_INTEGRITY.md - Gate-5 lookup integrity plan
├─ WINDOW_PB_PREFLIGHT.md - Execution window preflight
├─ WINDOW_PB_COMMAND_BLOCK.md - Execution window command block
├─ WINDOW_PB_EVIDENCE_HEADER_TEMPLATE.md - Evidence header template
├─ EVIDENCE_INDEX.md - Evidence index template (PB6.1)
├─ GAP_CLOSURE_TEMPLATE.md - Gap closure template (PB6.2)
└─ FREEZE_DECLARATION_TEMPLATE.md - Freeze declaration template (PB6.3)
```

### Planning Completion (2025-12-23)

**Planning Status:** ✅ COMPLETE

All planning deliverables are complete:
- ✅ PB0: Contracts locked (canonical flow, copy rules, quantity contract)
- ✅ PB1: Document register + master index created
- ✅ PB2: Data models documented (Panel Master, Feeder mapping, Proposal Panel, runtime instances)
- ✅ PB3: Copy process planning complete (copy flow, enforcement, governance gates)
- ✅ PB4: Runtime behavior fixes documented (BOM visibility, Panel visibility)
- ✅ PB5: Verification framework complete (Gate-0 through Gate-5, execution window pack)
- ✅ PB6: Closure pack complete (evidence index, gap closure, freeze declaration templates)

**Execution Status:** ⏳ BLOCKED until approval

### Gate State
- **Gate-0:** 📌 READY (Panel source readiness - planning complete)
- **Gate-1:** 📌 READY (Schema + history readiness - planning complete)
- **Gate-2:** 📌 READY (Controller/route wiring - planning complete)
- **Gate-3:** ⏳ BLOCKED (R1/S1/R2/S2 sequence - requires execution window)
- **Gate-4:** ⏳ BLOCKED (Rollup verification - requires Gate-3 completion)
- **Gate-5:** ⏳ BLOCKED (Lookup integrity - requires Gate-4 completion)

### Alignment with Feeder BOM

Panel BOM follows the same governance pattern as Feeder BOM:
- ✅ Planning-only mode (no runtime execution)
- ✅ Water-tight contracts (locked before execution)
- ✅ Evidence-driven execution (deferred)
- ✅ Stop-rule enforcement
- ✅ Copy-never-link pattern
- ✅ Reference-only tracking (PanelMasterId)

### Gap Mapping
- **BOM-GAP-007:** Copy Operations Not Implemented (includes Panel copy operations)
  - Panel copy operations planned but not yet verified
  - Closure path: Panel BOM execution window (Gate-0 through Gate-5 evidence)

### Rule
- ❌ No runtime/DB/UI work until execution window
- ✅ Planning artifacts are complete and ready for approval
- ✅ Execution will follow Window-PB pack (preflight, command block, verification SQL)

---

## 8) What We Are NOT Doing (Explicit)

- ❌ No UI debugging
- ❌ No DevTools
- ❌ No MariaDB execution
- ❌ No folder `/Users/nirajdesai/Projects/nish` edits
- ❌ No "quick fixes"

---

## 9) Execution Window Rule (Future)

**Only after:**
- Phase-1 → Phase-5 are all READY
- This index is unchanged
- A separate `EXECUTION_APPROVAL.md` is created

**Then (and only then):**
- Gates move from READY → PASS
- Evidence is captured
- Runtime is touched

**Pre-Execution Draft (Blocked):**
- ❌ No execution window todos should be created until Phase-5 is READY + `EXECUTION_APPROVAL.md` exists
- ❌ Execution strategy decision (combined vs split windows) is deferred until Phase-5 READY
- ✅ Execution todos will be created only after Phase-5 READY

**Next Step:** `EXECUTION_APPROVAL.md` draft creation (still planning mode).

---

## 10) Change Control

Any modification requires:
- Updating this file
- Date + reason
- Explicit phase reference

**Change Log:**
- 2025-12-21: Added Phase-0 (Fundamentals Gap Correction) integration per unified serial plan. Status: READY (planning complete, execution blocked until approval).
- 2025-12-23: Added Panel BOM Planning Track (PB0-PB6) section. Status: PLANNING COMPLETE (all phases PB0-PB6 complete, execution blocked until approval).

---

**END OF MASTER PLANNING INDEX**

