# Panel BOM Planning TODO Tracker

**File:** PLANNING/PANEL_BOM/PANEL_BOM_TODO_TRACKER.md  
**Version:** v1.0  
**Date:** 2025-12-23  
**Status:** 📋 PLANNING MODE  
**Purpose:** Cursor-ready TODO tracker for Panel BOM planning phases (PB0-PB6)

---

## ⚠️ PLANNING MODE RULES

- ✅ All work is **planning-only** documentation
- ⛔ No runtime code changes
- ⛔ No DB queries against live data
- ⛔ No execution windows / evidence population
- ✅ Implementation status treated as "unknown until verified"

---

## Phase Status Overview

| Phase | Status | Progress | Blockers |
|-------|--------|----------|----------|
| **PB0** | ✅ COMPLETE | 3/3 tasks | - |
| **PB1** | ✅ COMPLETE | 3/3 tasks | - |
| **PB2** | ✅ COMPLETE | 4/4 tasks | - |
| **PB3** | ✅ COMPLETE | 4/4 tasks | - |
| **PB4** | ✅ COMPLETE | 3/3 tasks | - |
| **PB5** | ✅ COMPLETE | 6/6 tasks | Execution deferred |
| **PB6** | ✅ COMPLETE | 3/3 tasks | Execution deferred |

---

## PB0: Normalize & Lock Contracts

**Status:** ✅ COMPLETE  
**Priority:** HIGH  
**Estimated Time:** 2 hours  
**Completed:** 2025-12-23

### Tasks

- [x] **PB0.1:** Create canonical flow document
  - Lock: Panel Master → Proposal Panel → Feeders → Proposal BOM → Items
  - Explicit separation: Panel Master (template) vs Proposal Panel (instance)
  - PanelMasterId reference-only rule
  - **File:** `PLANNING/PANEL_BOM/CANONICAL_FLOW.md` ✅ CREATED
  - **Dependencies:** None

- [x] **PB0.2:** Lock copy-never-link rule document
  - Always copy Panel Master, never link
  - No upward mutation (Panel Master immutable)
  - PanelMasterId stored as reference-only
  - **File:** `PLANNING/PANEL_BOM/COPY_RULES.md` ✅ CREATED
  - **Dependencies:** PB0.1

- [x] **PB0.3:** Confirm quantity contract
  - Panel qty multiply happens once (already verified)
  - Component level: ItemQty × BOMQty
  - Panel level: multiply once by PanelQty (inside quotationAmount())
  - **File:** `PLANNING/PANEL_BOM/QUANTITY_CONTRACT.md` ✅ CREATED
  - **Dependencies:** None (already verified)

**Exit Criteria:** All contracts locked, no ambiguity

---

## PB1: Document Register + Index

**Status:** ✅ COMPLETE  
**Priority:** HIGH  
**Estimated Time:** 1.5 hours  
**Completed:** 2025-12-23

### Tasks

- [x] **PB1.1:** Document Register created
  - ✅ Status: EXISTS (`PANEL_BOM_DOCUMENT_REGISTER.md`)
  - ✅ Tracks design documents (PB-DOC-001 through PB-DOC-013)
  - ✅ Tracks verification documents (PB-VER-001, PB-VER-002)

- [x] **PB1.2:** Create phases/gates tracker
  - Phase structure (PB0-PB6)
  - Gate definitions (Gate-0 through Gate-5)
  - Evidence stub locations
  - Stop-rule enforcement
  - **File:** `PLANNING/PANEL_BOM/GATES_TRACKER.md` ✅ CREATED
  - **Dependencies:** PB0 (for contract references)

- [x] **PB1.3:** Create master index
  - Cross-reference to Feeder BOM phases
  - Link to Fundamentals hierarchy
  - Link to gap register
  - **File:** `PLANNING/PANEL_BOM/MASTER_INDEX.md` ✅ CREATED
  - **Dependencies:** PB1.2

**Exit Criteria:** All tracking structures in place

---

## PB2: Data Models & Mapping

**Status:** ✅ COMPLETE  
**Priority:** HIGH  
**Estimated Time:** 3 hours  
**Completed:** 2025-12-23

### Tasks

- [x] **PB2.1:** Freeze Panel Master table structure ✅
  - `panel_masters` table (if exists) or logical entity
  - Fields: PanelMasterId, Name, Description, etc.
  - Template semantics
  - **File:** `PLANNING/PANEL_BOM/DATA_MODELS_PB2.1_PANEL_MASTER.md` ✅ CREATED
  - **Dependencies:** Panel Master design Part-2 (Data Models)

- [x] **PB2.2:** Freeze Panel Master → Feeder linkage ✅
  - `panel_master_feeders` table (if exists) or logical relationship
  - FeederMasterId optional branch
  - Reference structure
  - **File:** `PLANNING/PANEL_BOM/DATA_MODELS_PB2.2_FEEDER_MAPPING.md` ✅ CREATED
  - **Dependencies:** Panel Master design Part-3 (Structure)

- [x] **PB2.3:** Freeze Proposal Panel mapping ✅
  - QuotationSale table mapping
  - PanelMasterId reference field (reference-only)
  - QuotationId linkage (Proposal root)
  - **File:** `PLANNING/PANEL_BOM/DATA_MODELS_PB2.3_PROPOSAL_PANEL.md` ✅ CREATED
  - **Dependencies:** Panel Master design Part-2, Part-4

- [x] **PB2.4:** Freeze runtime instance mapping ✅
  - Feeders: QuotationSaleBom (Level=0, ParentBomId=NULL)
  - Proposal BOMs: QuotationSaleBom (Level=1/2..., ParentBomId set)
  - Items: QuotationSaleBomItem
  - **File:** `PLANNING/PANEL_BOM/DATA_MODELS_PB2.4_RUNTIME_INSTANCES.md` ✅ CREATED
  - **Dependencies:** Panel Master design Part-3, Part-5

**Exit Criteria:** ✅ All tables/entities explicitly mapped, field-level documentation complete

---

## PB3: Copy Process Planning (Panel Master → Proposal Panel)

**Status:** ✅ COMPLETE  
**Priority:** HIGH  
**Estimated Time:** 4 hours  
**Completed:** 2025-12-23

### Tasks

- [x] **PB3.1:** Document copy flow
  - Panel Master → Proposal Panel copy operation
  - FeederMasterId optional branch handling
  - Nested feeder copy delegation
  - **File:** `PLANNING/PANEL_BOM/COPY_FLOW.md` ✅ CREATED
  - **Dependencies:** PB2, Panel Master design Part-4

- [x] **PB3.2:** Define copy governance gates
  - Gate-0: Panel source readiness (has N feeders)
  - Gate-1: Schema + history readiness
  - Gate-2: Controller/route wiring proof
  - Gate-3: R1/S1/R2/S2 sequence for panel copy
  - **File:** `PLANNING/PANEL_BOM/COPY_GOVERNANCE_GATES.md` ✅ CREATED
  - **Dependencies:** PB3.1

- [x] **PB3.3:** Document copy-never-link enforcement
  - New Proposal Panel instance (new QuotationSaleId)
  - New Feeder instances (new QuotationSaleBomId)
  - PanelMasterId stored as reference-only (never mutated)
  - **File:** `PLANNING/PANEL_BOM/COPY_ENFORCEMENT.md` ✅ CREATED
  - **Dependencies:** PB0.2, PB3.1

- [x] **PB3.4:** Handle FeederMasterId optional branch
  - Branch logic: If FeederMasterId present → use Feeder Master template
  - Branch logic: If FeederMasterId absent → use direct feeder copy
  - Both paths must record copy history
  - **File:** `PLANNING/PANEL_BOM/FEEDER_MASTER_BRANCH.md` ✅ CREATED
  - **Dependencies:** PB3.1, Feeder BOM governance

**Exit Criteria:** ✅ Copy flow explicitly documented, governance gates defined, branch logic clear

---

## PB4: Runtime Behavior Fixes (Planning Only)

**Status:** ✅ COMPLETE  
**Priority:** MEDIUM  
**Estimated Time:** 2 hours  
**Completed:** 2025-12-23

### Tasks

- [x] **PB4.1:** Document "panel not appearing after save"
  - Runtime history reference only
  - Convert to verification check: Status=0 filter required
  - Step page must filter Status=0 (active panels only)
  - **File:** `PLANNING/PANEL_BOM/RUNTIME_BEHAVIOR_PANEL_VISIBILITY.md` ✅ CREATED
  - **Dependencies:** None

- [x] **PB4.2:** Document "BOMs not appearing"
  - Runtime history reference only
  - Convert to verification check: Status=0 filter required
  - BOM visibility must respect Status field
  - **File:** `PLANNING/PANEL_BOM/RUNTIME_BEHAVIOR_BOM_VISIBILITY.md` ✅ CREATED
  - **Dependencies:** None

- [x] **PB4.3:** Create verification checks
  - VQ-PB-001: Panel visibility (Status=0 filter)
  - VQ-PB-002: BOM visibility (Status=0 filter)
  - VQ-PB-003: Feeder visibility (Status=0 filter)
  - **File:** `PLANNING/PANEL_BOM/VERIFICATION_QUERIES_RUNTIME.md` ✅ CREATED
  - **Dependencies:** PB4.1, PB4.2

**Exit Criteria:** ✅ Runtime-history references documented, verification checks created

---

## PB5: Verification Framework

**Status:** ✅ COMPLETE (Planning Pack Created)  
**Priority:** MEDIUM  
**Estimated Time:** 4 hours  
**Completed:** 2025-12-23  
**Note:** Planning pack complete (Window-PB style). Execution deferred until execution window.

### Tasks

- [x] **PB5.1:** Define Gate-0: Panel Source Readiness
  - Panel has N>0 feeders
  - Panel Master Status=0 validation
  - Evidence stub: `evidence/PANEL_BOM/G0_panel_readiness.txt` ✅ CREATED
  - **Planning Pack:** `PLANNING/PANEL_BOM/WINDOW_PB_COMMAND_BLOCK.md` (Gate-0 SQL)
  - **Dependencies:** PB3 (copy flow)

- [x] **PB5.2:** Define Gate-1: Schema + History Readiness
  - Panel tables exist
  - bom_copy_history table supports panel copy
  - Evidence stub: `evidence/PANEL_BOM/G1_schema_history.txt` ✅ CREATED
  - **Planning Pack:** `PLANNING/PANEL_BOM/WINDOW_PB_COMMAND_BLOCK.md` (Gate-1 SQL)
  - **Dependencies:** PB2 (data models)

- [x] **PB5.3:** Define Gate-2: Controller/Route Wiring Proof
  - Controller method exists (thin controller)
  - Route exists
  - BomEngine::copyPanelTree() called
  - Evidence stub: `evidence/PANEL_BOM/G2_controller_wiring.txt` ✅ CREATED
  - **Planning Pack:** `PLANNING/PANEL_BOM/WINDOW_PB_COMMAND_BLOCK.md` (Gate-2 pointers)
  - **Dependencies:** PB3 (copy governance)

- [x] **PB5.4:** Define Gate-3: R1/S1/R2/S2 Sequence
  - R1: First panel copy API call
  - S1: First verification SQL (copy history, structure integrity)
  - R2: Re-apply panel copy (idempotent)
  - S2: Second verification SQL (reuse detection, clear-before-copy)
  - Evidence stub: `evidence/PANEL_BOM/R1_S1_S2/` ✅ CREATED
  - **Planning Pack:** `PLANNING/PANEL_BOM/05_VERIFICATION/PANEL_R1_R2_S1_S2_VERIFICATION.sql` ✅ CREATED
  - **Dependencies:** PB3 (copy flow), Feeder BOM Gate-3 reference

- [x] **PB5.5:** Define Gate-4: Rollup Verification ✅
  - Quantity contract verified (already locked)
  - Panel qty multiply happens once
  - Evidence stub: `evidence/PANEL_BOM/G4_rollup_verification.txt`
  - **File:** `PLANNING/PANEL_BOM/GATE4_ROLLUP.md` ✅ CREATED
  - **Dependencies:** PB0.3 (quantity contract) ✅

- [x] **PB5.6:** Define Gate-5: Lookup Integrity ✅
  - Reuse Phase-4 lookup integrity rules
  - Panel → Feeder → Item lookup chain verified
  - Evidence stub: `evidence/PANEL_BOM/G5_lookup_integrity.txt`
  - **File:** `PLANNING/PANEL_BOM/GATE5_LOOKUP_INTEGRITY.md` ✅ CREATED
  - **Dependencies:** Phase-4 governance (Feeder BOM) ✅

**Exit Criteria:** ✅ Planning pack created (Window-PB style with preflight, command block, verification SQL, evidence stubs). Gate-4 and Gate-5 complete.

**Planning Pack Files Created:**
- ✅ `PLANNING/PANEL_BOM/WINDOW_PB_PREFLIGHT.md`
- ✅ `PLANNING/PANEL_BOM/WINDOW_PB_COMMAND_BLOCK.md`
- ✅ `PLANNING/PANEL_BOM/05_VERIFICATION/PANEL_R1_R2_S1_S2_VERIFICATION.sql`
- ✅ `evidence/PANEL_BOM/G0_panel_readiness.txt`
- ✅ `evidence/PANEL_BOM/G1_schema_history.txt`
- ✅ `evidence/PANEL_BOM/G2_controller_wiring.txt`
- ✅ `evidence/PANEL_BOM/R1_S1_S2/S1_sql_output.txt`
- ✅ `evidence/PANEL_BOM/R1_S1_S2/S2_sql_output.txt`
- ✅ `evidence/PANEL_BOM/R1_S1_S2/R1.json` (optional)
- ✅ `evidence/PANEL_BOM/R1_S1_S2/R2.json` (optional)

---

## PB6: Closure Pack

**Status:** ✅ COMPLETE (Templates created)  
**Priority:** LOW  
**Estimated Time:** 2 hours  
**Completed:** 2025-12-23  
**Note:** Templates created, ready for execution window (fill during execution)

### Tasks

- [x] **PB6.1:** Create evidence index template ✅
  - All evidence files catalogued
  - Evidence validation checklist
  - Cross-reference to gates
  - **File:** `PLANNING/PANEL_BOM/EVIDENCE_INDEX.md` ✅ CREATED
  - **Dependencies:** PB5 (all gates defined) ✅

- [x] **PB6.2:** Create gap register closure template ✅
  - Panel BOM gaps marked CLOSED (template)
  - Gap closure evidence attached (template)
  - Related gaps cross-referenced
  - **File:** `PLANNING/PANEL_BOM/GAP_CLOSURE_TEMPLATE.md` ✅ CREATED
  - **Dependencies:** Gap register review ✅

- [x] **PB6.3:** Create freeze declaration template ✅
  - Panel BOM design frozen (template)
  - Governance locked (template)
  - Execution complete declaration (template)
  - **File:** `PLANNING/PANEL_BOM/FREEZE_DECLARATION_TEMPLATE.md` ✅ CREATED
  - **Dependencies:** All phases complete ✅

**Exit Criteria:** ✅ Closure templates ready for execution window

---

## Cross-Phase Tasks

### Documentation Alignment

- [ ] **ALIGN-1:** Update Document Register
  - Mark PB-DOC-* documents as uploaded (per user confirmation)
  - Update status for each document
  - Cross-reference to planning phases

- [ ] **ALIGN-2:** Update Master Planning Index
  - Add Panel BOM section
  - Link to PB0-PB6 phases
  - Status: PLANNING IN PROGRESS

- [ ] **ALIGN-3:** Update Gap Register
  - Review Panel BOM gaps
  - Mark resolved gaps (if any)
  - Update gap status per Fundamentals corrections

### Review & Validation

- [ ] **REVIEW-1:** Peer review PB0 contracts
  - Canonical flow
  - Copy rules
  - Quantity contract

- [ ] **REVIEW-2:** Peer review PB2 data models
  - Table mappings
  - Field mappings
  - Template vs Instance separation

- [ ] **REVIEW-3:** Peer review PB3 copy process
  - Copy flow
  - Governance gates
  - Branch logic

---

## Notes

### Implementation Status

**⚠️ Important:** Implementation status treated as "unknown until verified during execution window". Planning will work whether code exists or needs implementation.

### Dependencies

- **Panel Master Design Documents:** User confirmed uploaded (PB-DOC-001 through PB-DOC-013)
- **Track B (Fundamentals Gap Correction):** Separate thread, produces canonical hierarchy doc
- **Feeder BOM Governance:** Reference pattern for gates and verification

### Stop Rules

- Any gate/check failure → STOP → capture evidence → no patching unless explicitly approved
- Planning-only mode: no runtime changes allowed
- Evidence-driven execution: all gates require evidence

---

## Progress Tracking

**Overall Progress:** 22/29 tasks complete (76%)

**By Phase:**
- PB0: 3/3 (100%) ✅
- PB1: 3/3 (100%) ✅
- PB2: 4/4 (100%) ✅
- PB3: 4/4 (100%) ✅
- PB4: 3/3 (100%) ✅
- PB5: 6/6 (100%) ✅ COMPLETE (Planning Pack Created)
- PB6: 3/3 (100%) ✅ COMPLETE (Templates Created)
- Cross-Phase: 0/6 (0%)

**Next Actions:**
1. ✅ PB0 (Normalize & Lock Contracts) - COMPLETE
2. ✅ PB1 (Document Register + Index) - COMPLETE
3. Start PB2 (Data Models & Mapping) - HIGH PRIORITY (requires design docs review)

---

**END OF TODO TRACKER**




