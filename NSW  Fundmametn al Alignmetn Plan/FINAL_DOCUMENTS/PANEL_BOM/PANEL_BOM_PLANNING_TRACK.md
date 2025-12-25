# Panel BOM Planning Track (Track A)

**File:** PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md  
**Version:** v1.0  
**Date:** 2025-12-23  
**Status:** 📋 PLANNING ONLY (Execution deferred until approval)  
**Purpose:** Primary planning track for Panel BOM design layer aligned with Fundamentals + Feeder BOM governance

---

## ⚠️ CRITICAL DECLARATION

**MODE:** 📋 PLANNING ONLY  
**EXECUTION:** ⛔ DEFERRED until execution windows + evidence + stop-rule  
**IMPLEMENTATION STATUS:** ⚠️ Unknown until verified during execution window  
**APPROACH:** Planning will work whether code exists or needs implementation

This track follows the exact governance approach used for Feeder BOM:
- Planning-only documentation
- Water-tight contracts and gates
- Evidence-driven execution (deferred)
- Stop-rule enforcement

---

## Runtime Hierarchy (Locked)

### Design-Time Masters → Runtime Instances

```
Item Master
  ↓
Master BOM (generic templates)
  ↓
Feeder Master (template, optional) → feeder_masters table
  ↓
Panel Master (template) → panel_masters table
  ↓
[COPY OPERATION]
  ↓
Proposal Panels (QuotationSale instances)
  ↓
Feeders (QuotationSaleBom, Level=0)
  ↓
Proposal BOMs (QuotationSaleBom, Level=1/2...)
  ↓
Proposal BOM Items (QuotationSaleBomItem)
  ↓
[RESOLVE]
  ↓
Item Master
```

### Key Separation

- **Panel Master** = Template layer (design-time, reference data)
- **Proposal Panel** = Runtime instance (QuotationSale, linked to Quotation/Proposal root)
- **PanelMasterId** = Reference-only field in Proposal Panel (never mutated)

---

## Panel BOM Planning Phases (PB0-PB6)

### PB0: Normalize & Lock Contracts

**Status:** ✅ COMPLETE  
**Goal:** Lock canonical flow, copy rules, and quantity contract  
**Completed:** 2025-12-23

**Deliverables:**
- [x] **PB0.1:** Lock canonical flow document ✅
  - Panel Master → Proposal Panel → Feeders → Proposal BOM → Items
  - Explicit separation: Panel Master (template) vs Proposal Panel (instance)
  - PanelMasterId reference-only rule
  - **File:** `CANONICAL_FLOW.md` ✅ CREATED

- [x] **PB0.2:** Lock copy-never-link rule ✅
  - Always copy Panel Master, never link
  - No upward mutation (Panel Master immutable)
  - PanelMasterId stored as reference-only
  - **File:** `COPY_RULES.md` ✅ CREATED

- [x] **PB0.3:** Lock quantity contract ✅
  - Panel qty multiply happens once (already verified)
  - Component level: ItemQty × BOMQty
  - Panel level: multiply once by PanelQty (inside quotationAmount())
  - No other multipliers anywhere
  - **File:** `QUANTITY_CONTRACT.md` ✅ CREATED

**Reference:** Quantity contract already verified and locked per user confirmation

**Exit Criteria:**
- ✅ Canonical flow document frozen
- ✅ Copy rules explicitly stated and locked
- ✅ Quantity contract confirmed (already verified)

---

### PB1: Document Register + Index

**Status:** ✅ COMPLETE  
**Goal:** Create Panel BOM tracker structure similar to Feeder BOM  
**Completed:** 2025-12-23

**Deliverables:**
- [x] **PB1.1:** Document Register created ✅
  - Status: ✅ EXISTS (`PANEL_BOM_DOCUMENT_REGISTER.md`)
  - Tracks design documents (PB-DOC-001 through PB-DOC-013)
  - Tracks verification documents (PB-VER-001, PB-VER-002)

- [x] **PB1.2:** Create phases/gates tracker ✅
  - Phase structure (PB0-PB6)
  - Gate definitions (Gate-0 through Gate-5)
  - Evidence stub locations
  - Stop-rule enforcement
  - **File:** `GATES_TRACKER.md` ✅ CREATED

- [x] **PB1.3:** Create master index ✅
  - Cross-reference to Feeder BOM phases
  - Link to Fundamentals hierarchy
  - Link to gap register
  - **File:** `MASTER_INDEX.md` ✅ CREATED

**Exit Criteria:**
- ✅ Document register complete and maintained
- ✅ Phase tracker created
- ✅ Master index cross-references established

---

### PB2: Data Models & Mapping

**Status:** ✅ COMPLETE  
**Goal:** Freeze tables/entities from uploaded Panel Master design  
**Completed:** 2025-12-23

**Deliverables:**
- [x] **PB2.1:** Freeze Panel Master table structure ✅
  - `panel_masters` table (if exists) or logical entity
  - Fields: PanelMasterId, Name, Description, etc.
  - Template semantics
  - **File:** `DATA_MODELS_PB2.1_PANEL_MASTER.md` ✅ CREATED

- [x] **PB2.2:** Freeze Panel Master → Feeder linkage ✅
  - `panel_master_feeders` table (if exists) or logical relationship
  - FeederMasterId optional branch
  - Reference structure
  - **File:** `DATA_MODELS_PB2.2_FEEDER_MAPPING.md` ✅ CREATED

- [x] **PB2.3:** Freeze Proposal Panel mapping ✅
  - QuotationSale table mapping
  - PanelMasterId reference field (reference-only)
  - QuotationId linkage (Proposal root)
  - **File:** `DATA_MODELS_PB2.3_PROPOSAL_PANEL.md` ✅ CREATED

- [x] **PB2.4:** Freeze runtime instance mapping ✅
  - Feeders: QuotationSaleBom (Level=0, ParentBomId=NULL)
  - Proposal BOMs: QuotationSaleBom (Level=1/2..., ParentBomId set)
  - Items: QuotationSaleBomItem
  - **File:** `DATA_MODELS_PB2.4_RUNTIME_INSTANCES.md` ✅ CREATED

**Input:** Uploaded Panel Master design documents (PB-DOC-001 through PB-DOC-013)

**Exit Criteria:**
- ✅ All tables/entities explicitly mapped
- ✅ Field-level mapping documented
- ✅ Template vs Instance separation clear

---

### PB3: Copy Process Planning (Panel Master → Proposal Panel)

**Status:** ⏳ PENDING  
**Goal:** Convert Part-4 copy process into governance gates

**Deliverables:**
- [ ] **PB3.1:** Document copy flow
  - Panel Master → Proposal Panel copy operation
  - FeederMasterId optional branch handling
  - Nested feeder copy delegation

- [ ] **PB3.2:** Define copy governance gates
  - Gate-0: Panel source readiness (has N feeders)
  - Gate-1: Schema + history readiness
  - Gate-2: Controller/route wiring proof
  - Gate-3: R1/S1/R2/S2 sequence for panel copy
  - Similar structure to Feeder BOM Gate-0/R1/S1/R2/S2

- [ ] **PB3.3:** Document copy-never-link enforcement
  - New Proposal Panel instance (new QuotationSaleId)
  - New Feeder instances (new QuotationSaleBomId)
  - PanelMasterId stored as reference-only (never mutated)

- [ ] **PB3.4:** Handle FeederMasterId optional branch
  - Branch logic: If FeederMasterId present → use Feeder Master template
  - Branch logic: If FeederMasterId absent → use direct feeder copy
  - Both paths must record copy history

**Input:** Panel Master design Part-4 (Copy Process document)

**Exit Criteria:**
- Copy flow explicitly documented
- Governance gates defined (Gate-0 through Gate-3)
- Copy-never-link rules locked
- FeederMasterId branch logic documented

---

### PB4: Runtime Behavior Fixes (Planning Only)

**Status:** ⏳ PENDING  
**Goal:** Convert runtime-history references into controlled verification checks

**Deliverables:**
- [ ] **PB4.1:** Document "panel not appearing after save"
  - Runtime history reference only
  - Convert to verification check: Status=0 filter required
  - Step page must filter Status=0 (active panels only)

- [ ] **PB4.2:** Document "BOMs not appearing"
  - Runtime history reference only
  - Convert to verification check: Status=0 filter required
  - BOM visibility must respect Status field

- [ ] **PB4.3:** Create verification checks
  - VQ-PB-001: Panel visibility (Status=0 filter)
  - VQ-PB-002: BOM visibility (Status=0 filter)
  - VQ-PB-003: Feeder visibility (Status=0 filter)

**Approach:** Treat runtime issues as verification requirements, not ad-hoc fixes

**Exit Criteria:**
- Runtime-history references documented
- Verification checks created
- No ad-hoc runtime patching planned

---

### PB5: Verification Framework

**Status:** ✅ COMPLETE (Planning Pack Created)  
**Goal:** Create Panel BOM verification gates and evidence structure  
**Completed:** 2025-12-23

**Deliverables:**
- [x] **PB5.1:** Gate-0: Panel Source Readiness ✅
  - Panel has N>0 feeders
  - Panel has N>0 BOMs (if applicable)
  - Evidence: `evidence/PANEL_BOM/G0_panel_readiness.txt`
  - **File:** `GATES_TRACKER.md` ✅ CREATED

- [x] **PB5.2:** Gate-1: Schema + History Readiness ✅
  - Panel tables exist
  - bom_copy_history table supports panel copy
  - Evidence: `evidence/PANEL_BOM/G1_schema_history.txt`
  - **File:** `GATES_TRACKER.md` ✅ CREATED

- [x] **PB5.3:** Gate-2: Controller/Route Wiring Proof ✅
  - Controller method exists (thin controller)
  - Route exists
  - BomEngine::copyPanelTree() called
  - Evidence: `evidence/PANEL_BOM/G2_controller_wiring.txt`
  - **File:** `GATES_TRACKER.md` ✅ CREATED

- [x] **PB5.4:** Gate-3: R1/S1/R2/S2 Sequence ✅
  - R1: First panel copy API call
  - S1: First verification SQL (copy history, structure integrity)
  - R2: Re-apply panel copy (idempotent)
  - S2: Second verification SQL (reuse detection, clear-before-copy)
  - Evidence: `evidence/PANEL_BOM/R1_S1_S2/`
  - **File:** `GATES_TRACKER.md` ✅ CREATED

- [x] **PB5.5:** Gate-4: Rollup Verification ✅
  - Quantity contract verified (already locked)
  - Panel qty multiply happens once
  - Evidence: `evidence/PANEL_BOM/G4_rollup_verification.txt`
  - **File:** `GATE4_ROLLUP.md` ✅ CREATED

- [x] **PB5.6:** Gate-5: Lookup Integrity ✅
  - Reuse Phase-4 lookup integrity rules
  - Panel → Feeder → Item lookup chain verified
  - Evidence: `evidence/PANEL_BOM/G5_lookup_integrity.txt`
  - **File:** `GATE5_LOOKUP_INTEGRITY.md` ✅ CREATED

**Reference:** Feeder BOM Gate-0/R1/S1/R2/S2 structure

**Exit Criteria:**
- ✅ All gates defined
- ✅ Evidence structure created
- ✅ Verification SQL queries drafted (execution deferred)

---

### PB6: Closure Pack

**Status:** ✅ COMPLETE (Templates created)  
**Goal:** Evidence index updates + gap register closures + freeze declaration  
**Completed:** 2025-12-23

**Deliverables:**
- [x] **PB6.1:** Evidence Index Template ✅
  - All evidence files catalogued
  - Evidence validation checklist
  - Cross-reference to gates
  - **File:** `EVIDENCE_INDEX.md` ✅ CREATED

- [x] **PB6.2:** Gap Closure Template ✅
  - Panel BOM gaps marked CLOSED (template)
  - Gap closure evidence attached (template)
  - Related gaps cross-referenced
  - **File:** `GAP_CLOSURE_TEMPLATE.md` ✅ CREATED

- [x] **PB6.3:** Freeze Declaration Template ✅
  - Panel BOM design frozen (template)
  - Governance locked (template)
  - Execution complete declaration (template)
  - **File:** `FREEZE_DECLARATION_TEMPLATE.md` ✅ CREATED

**Exit Criteria:**
- ✅ Evidence index template complete
- ✅ Gap closure template complete
- ✅ Freeze declaration template complete
- ⏳ Templates ready for execution window (fill during execution)

---

## Dependencies & Prerequisites

### Upstream Dependencies (Must Be Complete)

- ✅ Category → Subcategory → Type → Attribute (locked)
- ✅ Generic Item Master (locked)
- ✅ Specific Item Master (locked)
- ✅ Generic BOM (locked)
- ✅ Feeder BOM methodology (frozen governance)
- ✅ Proposal BOM structure (baseline frozen)

### Panel BOM Prerequisites

- ⏳ Panel Master design documents uploaded (PB-DOC-001 through PB-DOC-013)
- ⏳ Fundamentals hierarchy finalized (Track B - separate thread)
- ⏳ Master→Instance mapping table created (Track B - separate thread)

---

## Execution Rules

### Planning Mode Rules

- ✅ All work is planning-only documentation
- ✅ No runtime code changes
- ✅ No DB queries against live data
- ✅ Implementation status treated as "unknown until verified"

### Execution Window Rules (Deferred)

- ⛔ Execution blocked until approval
- ✅ Evidence-driven (all gates require evidence)
- ✅ Stop-rule enforced (any gate failure → STOP)
- ✅ Reversible operations only

---

## Alignment with Feeder BOM

### Pattern Matching

| Feeder BOM Phase | Panel BOM Phase | Alignment |
|-----------------|-----------------|-----------|
| F0: Normalization | PB0: Normalize & Lock Contracts | ✅ Same approach |
| F1: Gate-0 | PB1: Document Register | ✅ Same structure |
| F2: Thin Controller | PB2: Data Models | ✅ Same pattern |
| F3: Copy Process | PB3: Copy Process Planning | ✅ Same governance |
| F4: Verification | PB5: Verification Framework | ✅ Same gates |
| F5: Closure | PB6: Closure Pack | ✅ Same closure |

### Key Differences

- **Panel BOM** adds PB4 (Runtime Behavior Fixes) - converts history references
- **Panel BOM** adds PB5 Gate-4 (Rollup) - already verified, locked
- **Panel BOM** copy flow includes FeederMasterId optional branch

---

## Related Tracks

### Track A: Panel BOM Planning (This Document)
**Scope:** Panel BOM design layer planning  
**Status:** In progress (PB0-PB6)

### Track B: Fundamentals Gap Correction (Separate Thread)
**Scope:** Fix Fundamentals Validation Review, canonical hierarchy doc  
**Status:** Separate chat thread (see user-provided starter MD)

**Cross-Link:** Track B will produce canonical hierarchy doc that Panel BOM depends on.

---

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2025-12-23 | v1.0 | Initial Panel BOM planning track created | System |

---

## References

### Related Documents
- `PLANNING/PANEL_BOM/PANEL_BOM_DOCUMENT_REGISTER.md` - Document registry
- `PLANNING/FEEDER_BOM/FEEDER_BOM_PLAN_NORMALIZATION.md` - Reference pattern
- `PLANNING/FEEDER_BOM/FEEDER_BOM_EXECUTION_READINESS_SUMMARY.md` - Gate structure reference

### Related Plans
- `PLANNING/MASTER_PLANNING_INDEX.md` - Master planning (Panel BOM not yet listed)
- `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` - BOM gap tracking

---

**END OF PLANNING TRACK**




