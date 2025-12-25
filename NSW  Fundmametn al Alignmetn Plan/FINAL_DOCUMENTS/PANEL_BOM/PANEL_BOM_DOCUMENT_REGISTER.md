# Panel BOM Document Register

**File:** PLANNING/PANEL_BOM/PANEL_BOM_DOCUMENT_REGISTER.md  
**Version:** v1.1_2025-01-XX  
**Date:** 2025-01-XX (Updated: 2025-01-XX)  
**Status:** 🔄 REVIEW IN PROGRESS  
**Purpose:** Central registry of all Panel BOM design documents, versions, scope, dependencies, and status

---

## ⚠️ CRITICAL DECLARATION

**MODE:** 📋 PLANNING ONLY (Execution deferred until approval)  
**IMPLEMENTATION STATUS:** ⚠️ Unknown until verified during execution window  
**DOCUMENTATION STATUS:** ✅ Panel Master design documents uploaded (PB-DOC-001 through PB-DOC-013)  
**VERIFICATION STATUS:** ⏳ Verification gates not yet defined (unlike Feeder BOM which has Gate-0/R1/S1/R2/S2)  
**APPROACH:** Planning will work whether code exists or needs implementation

**Note on Implementation:** Even if runtime code exists (e.g., `BomEngine::copyPanelTree()`), we treat implementation status as "unknown until verified during execution window". Planning documents are written to be agnostic of implementation state.

This register tracks Panel BOM design documents that will be normalized and aligned with:
- Feeder BOM methodology (frozen governance)
- Fundamentals Master TODO Tracker
- Category → Subcategory → Type → Attribute → Item Master → BOM chain
- Execution windows (deferred until approval)

---

## Implementation Status

### Runtime Code Status

**⚠️ IMPORTANT:** Implementation status is treated as **unknown until verified during execution window**. Planning documents are written to work whether code exists or needs implementation.

**Potential Code Location (Unverified):**
- `app/Services/BomEngine.php` may contain `copyPanelTree()` method
- Controller integration status unknown
- API endpoint exposure unknown

### Planning Approach

**Planning documents assume:**
- Implementation may exist or may need to be created
- Verification will occur during execution window (Gate-2: Wiring Proof)
- All contracts and gates are defined independently of implementation state

**This ensures:**
- Planning completeness regardless of code state
- Clear verification requirements
- Water-tight contracts before execution

**Review Document:** See `PLANNING/PANEL_BOM/PANEL_BOM_PLAN_REVIEW_2025-01.md` for previous analysis (note: now superseded by planning-first approach).

---

## Document Registry

### Batch Status Tracking

| Batch | Status | Upload Date | Notes |
|-------|--------|-------------|-------|
| Batch-1 | ⏳ Pending | - | - |
| Batch-2 | ⏳ Pending | - | - |
| Batch-N | ⏳ Pending | - | - |

---

## Core Panel BOM Design Documents

### Document Index & Metadata

| Doc-ID | Filename | Version | Date | Scope | Dependencies | Status | Links |
|--------|----------|---------|------|-------|--------------|--------|-------|
| PB-DOC-001 | `PANEL_LIST_FIX_COMPLETE.md` | - | - | Panel list fixes and completion | - | ✅ Uploaded | - |
| PB-DOC-002 | `PANEL_MASTER_BACKEND_DESIGN_INDEX.md` | - | - | Design index and navigation | PB-DOC-003 to PB-DOC-012 | ✅ Uploaded | - |
| PB-DOC-003 | `PANEL_MASTER_BACKEND_DESIGN_PART1_FOUNDATION.md` | - | - | Foundation principles, architecture overview | - | ✅ Uploaded | - |
| PB-DOC-004 | `PANEL_MASTER_BACKEND_DESIGN_PART2_DATA_MODELS.md` | - | - | Data models, schemas, table structures | PB-DOC-003 | ✅ Uploaded | - |
| PB-DOC-005 | `PANEL_MASTER_BACKEND_DESIGN_PART3_STRUCTURE.md` | - | - | Structural relationships, hierarchies | PB-DOC-004 | ✅ Uploaded | - |
| PB-DOC-006 | `PANEL_MASTER_BACKEND_DESIGN_PART4_COPY_PROCESS.md` | - | - | Copy process, reuse rules, copy-never-link | PB-DOC-003, PB-DOC-005 | ✅ Uploaded | ⚠️ Non-negotiable rules |
| PB-DOC-007 | `PANEL_MASTER_BACKEND_DESIGN_PART5_RULES.md` | - | - | Business rules, validation rules | PB-DOC-006 | ✅ Uploaded | ⚠️ Non-negotiable rules |
| PB-DOC-008 | `PANEL_MASTER_BACKEND_DESIGN_PART6_SERVICES.md` | - | - | Service layer design, API contracts | PB-DOC-004, PB-DOC-006 | ✅ Uploaded | - |
| PB-DOC-009 | `PANEL_MASTER_BACKEND_DESIGN_PART7_MASTER_DATA.md` | - | - | Master data management, reference data | PB-DOC-004 | ✅ Uploaded | - |
| PB-DOC-010 | `PANEL_MASTER_BACKEND_DESIGN_PART8_OPERATIONS.md` | - | - | CRUD operations, workflows | PB-DOC-006, PB-DOC-008 | ✅ Uploaded | - |
| PB-DOC-011 | `PANEL_MASTER_BACKEND_DESIGN_PART9_LOGIC.md` | - | - | Business logic, calculations, rollups | PB-DOC-004, PB-DOC-007 | ✅ Uploaded | - |
| PB-DOC-012 | `PANEL_MASTER_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md` | - | - | Integration with Feeder BOM, Proposal BOM, Item Master | PB-DOC-003 to PB-DOC-011 | ✅ Uploaded | - |
| PB-DOC-013 | `PANEL_MASTER_BACKEND_DESIGN_PART11_CODEBASE.md` | - | - | Codebase mapping, file references | PB-DOC-002 to PB-DOC-011 | ✅ Uploaded | - |

---

## Verification & Rollup Documents

| Doc-ID | Filename | Version | Date | Scope | Dependencies | Status | Links |
|--------|----------|---------|------|-------|--------------|--------|-------|
| PB-VER-001 | Panel Rollup Verification (any format) | - | - | Quantity rollup verification, SQL checks | PB-DOC-011 | ⏳ Awaiting upload | ✅ Already verified (quantity contract locked) |
| PB-VER-002 | Panel Reuse Fix Documentation | - | - | BOM visibility fixes, reuse behavior | PB-DOC-006 | ⏳ Awaiting upload | ⚠️ Runtime history reference only |

---

## Document Categories

### Category 1: Core Design (Foundation → Structure)
- **Files:** PB-DOC-003, PB-DOC-004, PB-DOC-005
- **Purpose:** Architectural foundation, data models, structural relationships
- **Normalization Target:** Align with Feeder BOM foundation patterns

### Category 2: Copy & Rules (Non-Negotiable)
- **Files:** PB-DOC-006, PB-DOC-007
- **Purpose:** Copy process semantics, business rules
- **Normalization Target:** Must match Feeder BOM copy-never-link + idempotent reuse discipline
- **⚠️ Status:** Marked as non-negotiable per user instructions

### Category 3: Implementation (Services → Operations → Logic)
- **Files:** PB-DOC-008, PB-DOC-009, PB-DOC-010, PB-DOC-011
- **Purpose:** Service layer, operations, business logic
- **Normalization Target:** Thin controller, engine-only writes (same as BomEngine pattern)

### Category 4: Integration (Interconnections → Codebase)
- **Files:** PB-DOC-012, PB-DOC-013
- **Purpose:** Cross-system integration, codebase mapping
- **Normalization Target:** Explicit coupling to Feeder BOM, Generic BOM, Proposal BOM

---

## Alignment Mapping

### Links to Fundamentals

| Panel BOM Concept | Fundamentals Link | Status |
|-------------------|-------------------|--------|
| Panel Master Copy | Feeder BOM copy process | 🔄 In progress (PB3) |
| Panel → Feeder relationship | Feeder BOM reuse semantics | 🔄 In progress (PB2, PB3) |
| Panel quantity rollup | Generic BOM quantity contract | ✅ Already verified (locked) |
| Panel Master → Proposal Panel | Proposal BOM copy flow | 🔄 In progress (PB3) |
| Panel history tracking | bom_copy_history pattern | 🔄 In progress (PB3, PB5) |

### Canonical Sequence (Locked)

```
Panel (Proposal Panel / QuotationSale)
  → Feeder BOMs (QuotationSaleBom, Level=0)
    → Sub-BOM levels (Level=1/2 etc, if used)
      → Line items (QuotationSaleBomItem)
        → Make/Series resolution
          → pricing
            → rollup
```

**Quantity Contract (Already Verified):**
- Component level: ItemQty × BOMQty
- Panel level: multiply once by PanelQty (inside quotationAmount())
- No other multipliers anywhere

---

## Normalization Status

| Phase | Status | Next Action |
|-------|--------|-------------|
| Registration | 🔄 **REVIEW IN PROGRESS** | Implementation reviewed, documentation pending |
| Implementation Review | ✅ **COMPLETE** | Code verified, aligns with Feeder BOM patterns |
| Normalization | ⏳ Pending | Will mirror FEEDER_BOM_PLAN_NORMALIZATION.md structure (after doc uploads) |
| Gap Analysis | ⏳ Pending | Cross-check against Category → Item → BOM chain |
| Verification Framework | ⏳ **URGENT** | Define Panel BOM gates (Gate-0, Gate-1, Gate-2) similar to Feeder BOM |
| Execution Readiness | ⏳ Pending | Gate-0 definition, thin controller contract, verification SQL |
| Roadmap Creation | ⏳ Pending | Panel phases (P0–P6 or PB0–PB6) |

---

## Dependencies & Prerequisites

### Upstream Dependencies (Must Be Complete)
- ✅ Category → Subcategory → Type → Attribute (locked)
- ✅ Generic Item Master (locked)
- ✅ Specific Item Master (locked)
- ✅ Generic BOM (locked)
- ✅ Feeder BOM methodology (frozen governance)
- ✅ Proposal BOM structure (baseline frozen)

### Panel BOM Prerequisites (Planning Status)

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| Panel Master design documents | ✅ **UPLOADED** | PB-DOC-001 through PB-DOC-013 uploaded per user confirmation |
| Panel copy semantics (copy-never-link) | 🔄 **IN PROGRESS** | PB0.2 (Copy Rules), PB3 (Copy Process Planning) |
| Panel history tracking schema | 🔄 **IN PROGRESS** | PB2 (Data Models), PB3 (Copy Process), PB5 (Verification) |
| Panel → Feeder relationship rules | 🔄 **IN PROGRESS** | PB2.2 (Feeder Linkage), PB3 (Copy Process) |
| Panel Master data model integrity | 🔄 **IN PROGRESS** | PB2 (Data Models & Mapping) |
| Panel lookup integrity rules | 🔄 **IN PROGRESS** | PB5.6 (Gate-5: Lookup Integrity) |

---

## Notes & Warnings

### ⚠️ Non-Negotiable Rules (From User Instructions)
1. **Part-4 (Copy Process):** Copy-never-link for Panel Master → Proposal Panel
2. **Part-5 (Rules):** Business rules are non-negotiable
3. **Quantity Contract:** Already verified and locked (no changes)

### 📋 Runtime History Reference
- Documents mentioning "BOMs not appearing" fixes or step-page loading behavior should be treated as **runtime-history reference only**
- New work will proceed via locked fundamentals execution model (no ad-hoc runtime patching)

### 🔒 Execution Deferral
- All documents are **PLANNING-ONLY**
- Execution blocked until:
  - Normalization complete
  - Gap analysis complete
  - Execution readiness approved
  - Fundamentals alignment verified

---

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2025-01-XX | v1.0 | Initial register created | System |
| 2025-01-XX | v1.1 | **REVIEW UPDATE:** Added implementation status section, verified code alignment, updated prerequisites, separated implementation from documentation status | System |
| 2025-01-XX | v1.2 | **CORRECTION UPDATE:** Panel Master docs marked as uploaded (per user confirmation), implementation status changed to "unknown until verified", planning-first approach adopted | System |

---

## Review Feedback Summary

**Review Completed:** 2025-01-XX  
**Review Document:** `PLANNING/PANEL_BOM/PANEL_BOM_PLAN_REVIEW_2025-01.md`

### Key Findings:
1. ✅ **Implementation exists** - `BomEngine::copyPanelTree()` is implemented and follows Feeder BOM patterns
2. ⚠️ **Plan accuracy** - Plan needed update to reflect implementation reality
3. ✅ **No architectural drift** - Implementation aligns with planned patterns
4. ⏳ **Verification framework missing** - Need to define Panel BOM verification gates

### Immediate Actions Required:
1. **Update Document Register** ✅ (This update)
2. **Verify Controller Integration** ⏳ (Check if copyPanelTree is exposed via API)
3. **Define Verification Framework** ⏳ (Create Panel BOM gates similar to Feeder BOM)
4. **Prioritize Documentation** ⏳ (Service layer, operations, copy process docs)

---

**Next Step:** 
1. Verify controller integration status (check API endpoints)
2. Define Panel BOM verification gates (Gate-0, Gate-1, Gate-2)
3. Upload Panel BOM design documents (prioritize service layer and operations docs)
4. Create verification SQL queries for Panel BOM copy operations

