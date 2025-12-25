# Implementation Mapping — NSW Estimation Software Codebase

**Version:** v1.1  
**Date:** 2025-12-XX (Placeholder; derives from repo doc dates)  
**Status:** 📋 PLANNING MODE ONLY (No Code Edits)  
**Purpose:** Map fundamentals layers to NSW Estimation Software codebase implementation

**⚠️ CRITICAL:** See [PATCH_APPENDIX_v1.1.md](./PATCH_APPENDIX_v1.1.md) for audit-safe guardrails and code locality notes.

---

## ⚠️ Codebase Locality Note

**IMPORTANT:** This repository (`NSW_Estimation_Software_Fundamentals`) is a **documentation/standards-only** repository. The actual Laravel application codebase (containing `app/Services/BomEngine.php`, `app/Http/Controllers/`, etc.) is in a **separate repository** or may be located in `source_snapshot/` directory.

**All code paths must be confirmed under the actual Laravel root.** Mapping remains provisional until verified.

**Code References:** All references to `app/Services/BomEngine.php` and similar paths are **INFERRED** from documentation references. Actual file locations must be verified in the runtime codebase.

---

## Existing Software Reality Check

This section lists likely current areas (controllers/services/models/routes/views) that correspond to each layer, based on references found in documentation.

**Note:** This is planning-only analysis. Actual codebase structure may differ. Verification requires codebase scan.

---

## Target Architecture

### Canonical Flow

**Thin Controller → BomEngine → History → Gates**

```
Controller (Thin)
    ↓
BomEngine (Centralized Service)
    ↓
BomHistoryService (History Recording)
    ↓
ProposalBomItemWriter (Write Gateway)
    ↓
Models (QuotationSaleBom, QuotationSaleBomItem, etc.)
    ↓
Database (quotation_sale_boms, quotation_sale_bom_items, etc.)
```

### Architecture Principles

1. **Thin Controller:** Controllers are thin wrappers around BomEngine
2. **BomEngine:** Centralized service enforcing BOM principles across all levels
3. **History First:** History recording is built-in, not optional
4. **Copy-Never-Link:** All copies create new instances (enforced)
5. **Write Gateway:** All Proposal BOM writes go through ProposalBomItemWriter

---

## Delta Table: Layer-by-Layer Implementation Mapping

### A. Category / Subcategory / Type(Item) / Attributes

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Category/Subcategory/Item** | **NOT FOUND IN REPO:** Explicit schema references | Schema verification required | Category/Subcategory/Item schema may not match documented rules | NEPL Governance Checklist execution |
| **Attributes** | **NOT FOUND IN REPO:** Explicit attribute schema | Attribute schema verification required | Attributes may not be vendor-neutral | NEPL Governance Checklist execution |

**Files Found:**
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — Rules defined
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md` — Verification methodology

**Implementation Status:** **NOT FOUND IN REPO (needs decision)** — Schema verification required

---

### B. Item/Component List

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Item/Component List** | **NOT FOUND IN REPO:** Explicit catalog schema | Catalog schema verification required | Product catalog may not match documented structure | Product catalog integrity verification |

**Files Found:**
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — ProductType rules
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md` — Archival rules

**Implementation Status:** **NOT FOUND IN REPO (needs decision)** — Catalog schema verification required

---

### C. Generic Item Master

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Generic Item Master (L0/L1)** | **NOT FOUND IN REPO:** Explicit Generic Item Master schema | Schema verification required | Generic products may not be correctly identified (ProductType=1) | Generic Item Master freeze verification (✅ FROZEN) |

**Files Found:**
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md` — Freeze declaration
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — L0/L1 rules

**Implementation Status:** **NOT FOUND IN REPO (needs decision)** — Schema verification required (Generic Item Master frozen)

---

### D. Specific Item Master

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Specific Item Master (L2)** | **NOT FOUND IN REPO:** Explicit Specific Item Master schema | Schema verification required | Specific products may not be correctly identified (ProductType=2) | Specific Item Master Round-0 Readiness verification |

**Files Found:**
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND0_READINESS_v1.0_20251218.md` — Readiness checklist
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — L2 rules

**Implementation Status:** **NOT FOUND IN REPO (needs decision)** — Schema verification required

---

### E. Master BOM (generic)

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Master BOM (L1)** | `master_boms` table (inferred from usage) | L1-only enforcement (ProductType=1) | Master BOM may contain L2 products (violates L1-only rule) | Master BOM gap register verification |

**Files Found:**
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md` — Correction plan
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` — Gap register
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Hierarchy definition

**Implementation Status:** **PARTIALLY DOCUMENTED** — Schema exists, L1-only enforcement required

---

### F. Master BOM (specific)

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Master BOM (specific)** | **NOT FOUND IN REPO (needs decision)** | Clarification required | Layer may not exist | N/A |

**Implementation Status:** **NOT FOUND IN REPO (needs decision)**

---

### G. Proposal BOM + Proposal Sub-BOM

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Proposal BOM (L2)** | `quotation_sale_boms` table (inferred from usage)<br>`app/Services/BomEngine.php` — Copy methods implemented<br>`app/Services/BomHistoryService.php` — History service implemented | L2-only enforcement (ProductType=2)<br>Write gateway enforcement (ProposalBomItemWriter)<br>ensureResolved() requirement | Proposal BOM may contain Generic products (violates L2-only rule) | Proposal BOM gap register verification<br>Resolution-B rules verification |

**Files Found:**
- `app/Services/BomEngine.php` — **INFERRED** (referenced in docs, actual location in separate repository)
- `app/Services/BomHistoryService.php` — **INFERRED** (referenced in docs, actual location in separate repository)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` — Gap register
- `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md` — Resolution-B rules
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md` — Write gateway design
- `PLANNING/FUNDAMENTS_CORRECTION/PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md` — Proposal BOM Master design

**Implementation Status:** **PARTIALLY IMPLEMENTED** — BomEngine exists, L2 enforcement required

---

### H. Feeder BOM

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Feeder Master** | `master_boms` table where `TemplateType='FEEDER'` (inferred from usage) | Feeder template filter standardization (P1)<br>Reuse detection (BOM-GAP-001)<br>Clear-before-copy (BOM-GAP-002) | Feeder template apply creates duplicates (no reuse detection)<br>Feeder items stack (no clear-before-copy) | Fundamentals verification queries (VQ-001, VQ-002)<br>Feeder BOM execution gates (Gate-0 through Gate-3) |
| **Feeder Instance** | `quotation_sale_boms` table where `MasterBomId` references Feeder Master (inferred from usage) | Copy-never-link enforcement<br>Reuse detection<br>Clear-before-copy | Feeder Instances may mutate Feeder Master (copy-never-link violated) | Fundamentals verification checklist (G1) |

**Files Found:**
- `PLANNING/FUNDAMENTS_CORRECTION/FEEDER_MASTER_BACKEND_DESIGN_v1.0.md` — Feeder Master design (frozen)
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` — Verification queries
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` — Verification checklist
- `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` — BOM gap register (BOM-GAP-001, BOM-GAP-002)
- `docs/FEEDER_BOM/` — Feeder BOM documentation directory

**Implementation Status:** **PARTIALLY DOCUMENTED** — Schema exists, reuse detection + clear-before-copy required

---

### I. Panel BOM

| Layer | Current Implementation Signals | Required Additions/Changes | Risks | Verification Gates/Evidence |
|-------|------------------------------|---------------------------|-------|----------------------------|
| **Panel Master** | **NOT FOUND IN REPO:** Explicit Panel Master schema | Panel Master schema verification required | Panel Master may not be correctly identified | Panel BOM planning verification |
| **Proposal Panel** | `quotation_sale` table (inferred from usage) | Panel copy operations (BOM-GAP-007)<br>Copy-never-link enforcement | Panel copy may not copy entire tree (feeders → BOMs → items) | Panel BOM execution gates (Gate-0 through Gate-5) |

**Files Found:**
- `PLANNING/PANEL_BOM/MASTER_INDEX.md` — Panel BOM master index
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` — Planning track (PB0-PB6)
- `PLANNING/PANEL_BOM/GATES_TRACKER.md` — Gates tracker
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Hierarchy definition

**Implementation Status:** **PLANNING COMPLETE** — Execution deferred until approval

---

## Sequenced Implementation Plan

### Phase 0: Fundamentals Baseline (✅ COMPLETE)

**Status:** ✅ COMPLETE (Phase-0 Execution Complete, PASS WITH NOTES)

**Work:**
- Fundamentals baseline bundle frozen
- Canonical hierarchy defined
- Master→Instance mapping defined
- Verification queries created
- Verification checklist created

**Evidence:**
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` — Frozen
- `evidence/fundamentals/execution_window_20251222/` — Evidence captured

---

### Phase 1: History Foundation (✅ PARTIALLY COMPLETE)

**Status:** ⏳ PARTIALLY RESOLVED

**Work:**
- ✅ History tables created (migrations exist)
- ✅ BomHistoryService implemented
- ✅ BomEngine line item operations with history (addLineItem, updateLineItem, deleteLineItem, replaceLineItem)
- ⚠️ Controller integration pending (only updateSaleData() integrated)
- ❌ Restore capability not implemented

**Files:**
- `app/Services/BomEngine.php` — Line item operations implemented
- `app/Services/BomHistoryService.php` — History service implemented
- `database/migrations/2025_12_20_213521_create_quotation_sale_bom_item_history_table.php` — History table migration

**Evidence:**
- Phase-1A PASS — UPDATE operation verified with history row created

**Next Steps:**
- Integrate BomEngine into all controller methods
- Implement restore capability

---

### Phase 2: Copy Operations (⏳ PARTIALLY RESOLVED)

**Status:** ⏳ PARTIALLY RESOLVED

**Work:**
- ✅ Copy methods implemented in BomEngine (copyMasterBomToProposal, copyProposalBomToProposal, copyFeederTree)
- ✅ Copy history migration created (`bom_copy_history` table)
- ⚠️ Migration execution pending
- ⚠️ Controller wiring pending (Phase-2.1)
- ⚠️ Verification evidence pending (Phase-2.2 — R1/S1/R2/S2)
- ⚠️ Feeder reuse detection + clear-before-copy pending (BOM-GAP-001, BOM-GAP-002)

**Files:**
- `app/Services/BomEngine.php` — Copy methods implemented
- `app/Services/BomHistoryService.php` — recordCopyHistory() method implemented
- `NEPL_Basecode/database/migrations/2025_12_20_214545_create_bom_copy_history_table.php` — Copy history migration

**Evidence:**
- Gate-1 PASS — `bom_copy_history` schema verified on staging DB

**Next Steps:**
- Execute copy history migration
- Wire copy methods to controller endpoints
- Implement feeder reuse detection + clear-before-copy
- Capture R1/S1/R2/S2 verification evidence

---

### Phase 3: BOM Node Operations (❌ NOT IMPLEMENTED)

**Status:** ❌ NOT IMPLEMENTED (Planned for Phase-3)

**Work:**
- ❌ BOM node update methods not implemented
- ❌ BOM history recording not implemented
- ❌ BOM history table migration not created

**Files:**
- `PLANNING/GOVERNANCE/BOM_ENGINE_IMPLEMENTATION_PLAN.md` — Phase-3 planned
- `PLANNING/GOVERNANCE/HISTORY_BACKUP_MIN_SPEC.md` — BOM history schema defined

**Next Steps:**
- Create BOM history table migration
- Implement updateBomNode() in BomEngine
- Extend BomHistoryService with BOM history methods
- Implement restore capability for BOM nodes

---

### Phase 4: Lookup Pipeline Validation (OPEN)

**Status:** OPEN (Needs Verification)

**Work:**
- ⚠️ Lookup pipeline preservation not verified after copy
- ⚠️ Validation logic not implemented

**Files:**
- `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md` — Rule 3: Lookup-Pipeline
- `PLANNING/GOVERNANCE/BOM_MAPPING_REFERENCE.md` — Lookup pipeline requirements

**Next Steps:**
- Implement validateLookupPipeline() in BomEngine
- Implement preserveLookupPipeline() in BomEngine
- Add validation to all copy operations
- Add validation to all edit operations

---

### Phase 5: Panel BOM (PLANNING COMPLETE)

**Status:** 📋 PLANNING COMPLETE (Execution deferred until approval)

**Work:**
- ✅ Panel BOM planning complete (PB0-PB6)
- ✅ Panel BOM gates defined (Gate-0 through Gate-5)
- ⏳ Panel BOM execution deferred until approval

**Files:**
- `PLANNING/PANEL_BOM/MASTER_INDEX.md` — Master index
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` — Planning track
- `PLANNING/PANEL_BOM/GATES_TRACKER.md` — Gates tracker

**Next Steps:**
- Get approval for Panel BOM execution window
- Execute Panel BOM gates (Gate-0 through Gate-5)
- Capture Panel BOM evidence

---

## Implementation Dependencies

### Strict Order (What Must Be Implemented First)

1. **Phase 0: Fundamentals Baseline** (✅ COMPLETE)
   - Must be complete before any implementation

2. **Phase 1: History Foundation** (⏳ PARTIALLY RESOLVED)
   - Must be complete before Phase 2 (copy operations need history)

3. **Phase 2: Copy Operations** (⏳ PARTIALLY RESOLVED)
   - Depends on Phase 1 (history recording)
   - Must be complete before Phase 5 (Panel BOM uses copy operations)

4. **Phase 3: BOM Node Operations** (❌ NOT IMPLEMENTED)
   - Can be done in parallel with Phase 2
   - Depends on Phase 1 (history recording)

5. **Phase 4: Lookup Pipeline Validation** (OPEN)
   - Can be done in parallel with Phase 2 and Phase 3
   - Should be implemented before Phase 5

6. **Phase 5: Panel BOM** (📋 PLANNING COMPLETE)
   - Depends on Phase 2 (copy operations)
   - Execution deferred until approval

---

## Risks

### High Risk

1. **Schema Mismatch:** Actual database schema may not match documented structure
   - **Mitigation:** Schema verification required before implementation

2. **Missing Implementation:** Some layers have no explicit schema references
   - **Mitigation:** Codebase scan required to identify actual schema

3. **Controller Integration:** BomEngine exists but not fully integrated
   - **Mitigation:** Controller wiring required (Phase-2.1)

### Medium Risk

1. **Verification Evidence:** Implementation exists but verification evidence pending
   - **Mitigation:** Capture verification evidence during execution windows

2. **Gap Closure:** Gaps partially resolved but not closed
   - **Mitigation:** Complete implementation + verification evidence required

---

## Verification Gates/Evidence Required

### For Each Layer

1. **Schema Verification:** Verify actual database schema matches documented structure
2. **Code Verification:** Verify code implementation matches documented design
3. **Data Verification:** Verify data integrity (no violations of rules)
4. **Integration Verification:** Verify controller integration (thin controller pattern)
5. **History Verification:** Verify history recording works (before/after snapshots)
6. **Copy Verification:** Verify copy operations work (copy-never-link, reuse detection, clear-before-copy)

### Evidence Format

- SQL output (verification queries)
- JSON responses (API responses)
- Verification checklists (gate status)
- Code evidence (file paths, line numbers)

### Evidence Location

- `evidence/fundamentals/execution_window_YYYYMMDD/` — Fundamentals evidence
- `evidence/PHASE2/` — Phase-2 evidence
- `evidence/PANEL_BOM/` — Panel BOM evidence

---

## Execution Mapping Bridge

### Screen → Action → Endpoint → Service → Gates → Evidence Queries

This section provides a grounded "screen → API → service → DB" map for UI/Controller integration.

#### Example 1: Apply Feeder Template

- **Screen:** Quotation BOM Editor (Panel → Feeder section)
- **Action:** Apply Feeder Template
- **Endpoint:** `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
- **Service:** `BomEngine::copyFeederTree()`
- **Gates:**
  - Gate-0: Source Readiness (Feeder Master exists, template has items)
  - Gate-1: Schema + History Readiness (history tables exist)
  - Gate-2: Controller/Route Wiring (endpoint wired to BomEngine)
  - Gate-3: R1/S1/R2/S2 Sequence (copy operation verified)
- **Evidence:**
  - R1 JSON (copy request/response)
  - S1 SQL (before state verification)
  - R2 JSON (copy result)
  - S2 SQL (after state verification)

#### Example 2: Update Line Item

- **Screen:** Quotation BOM Editor (Item detail panel)
- **Action:** Update Item Quantity
- **Endpoint:** `PUT /quotation/{quotation}/bom/{bom}/item/{item}`
- **Service:** `BomEngine::updateLineItem()`
- **Gates:**
  - History recording verified (before/after snapshots)
  - Lookup pipeline preserved
  - Validation passes (ProductType=2, MakeId/SeriesId required)
- **Evidence:**
  - History row in `quotation_sale_bom_item_history`
  - Before/after snapshots captured
  - Changed fields recorded

#### Example 3: Apply Master BOM

- **Screen:** Quotation BOM Editor (BOM template selection)
- **Action:** Apply Master BOM Template
- **Endpoint:** `POST /quotation/{quotation}/panel/{panel}/bom/apply-master`
- **Service:** `BomEngine::copyMasterBomToProposal()`
- **Gates:**
  - L1 → L2 resolution works (Generic → Specific product mapping)
  - Copy history recorded
  - Proposal BOM items use ProductType=2
- **Evidence:**
  - Copy history row in `bom_copy_history`
  - Source/target snapshots captured
  - ID mapping recorded

### Validation Triggers

**Where validation happens:**
- **UI Level:** Client-side validation (MakeId/SeriesId required, ProductType=2)
- **Controller Level:** Request validation (Laravel form requests)
- **Service Level:** Business rule validation (BomEngine, ProposalBomItemWriter)
- **Database Level:** Foreign key constraints, NOT NULL constraints

**Write Gates:**
- All Proposal BOM writes must go through `ProposalBomItemWriter` gateway
- Gateway enforces ProductType=2, MakeId>0, SeriesId>0
- Gateway calls `ensureResolved()` before finalization

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial implementation mapping created from repository content |
| v1.1 | 2025-12-XX | Added code locality note, execution mapping bridge, date corrections, INFERRED tags |

---

**END OF IMPLEMENTATION MAPPING**

