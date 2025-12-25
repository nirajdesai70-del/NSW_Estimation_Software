# Panel BOM Canonical Flow

**File:** PLANNING/PANEL_BOM/CANONICAL_FLOW.md  
**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** ✅ FROZEN (PB0.1)  
**Purpose:** Lock the canonical runtime hierarchy and design-time master → instance flow for Panel BOM

---

## ⚠️ CRITICAL: FROZEN CONTRACT

This document defines the **only canonical path** for Panel BOM operations. This is a **locked contract** — any deviation must be explicitly approved and documented.

**Mode:** Planning-only (execution deferred)  
**Governance:** Aligned with Feeder BOM methodology  
**Reference:** `PANEL_BOM_PLANNING_TRACK.md` PB0.1

---

## 1) Runtime Hierarchy (Locked)

### 1.1 Instance Chain (Runtime)

The **only canonical runtime chain** for Proposal instances:

```
Quotation (Proposal Root)
  ↓
Proposal Panels (QuotationSale instances)
  ↓
Feeders (QuotationSaleBom, Level=0, ParentBomId=NULL)
  ↓
Proposal BOMs (QuotationSaleBom, Level=1/2..., ParentBomId set)
  ↓
Proposal BOM Items (QuotationSaleBomItem)
  ↓
[RESOLVE]
  ↓
Item Master
```

### 1.2 Key Runtime Rules

1. **Proposal Panel** = `QuotationSale` instance linked to `Quotation` (Proposal root)
2. **Feeder** = `QuotationSaleBom` with `Level=0` and `ParentBomId=NULL`
3. **Proposal BOM** = `QuotationSaleBom` with `Level>=1` and `ParentBomId` pointing to parent
4. **Proposal BOM Item** = `QuotationSaleBomItem` linked to `QuotationSaleBom`
5. **Item Master** = Ultimate resolution target for all items

---

## 2) Design-Time Master Hierarchy (Locked)

### 2.1 Master Chain (Design-Time)

The **only canonical master chain** that feeds into runtime:

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
[Continue with runtime chain from Section 1.1]
```

### 2.2 Key Master Rules

1. **Item Master** = Source of truth for all item definitions
2. **Master BOM** = Generic BOM templates (not Panel-specific)
3. **Feeder Master** = Optional template layer (logical abstraction over `master_boms` where `TemplateType='FEEDER'`)
4. **Panel Master** = Template layer above feeder references (design-time, reference data)
5. **Copy Operation** = Point of transformation from master to instance

---

## 3) Master → Instance Separation (Locked)

### 3.1 Explicit Separation

**Panel Master (Template):**
- Design-time reference data
- Immutable (no upward mutation)
- Defines structure, default feeders allowed, high-level configuration rules
- Stored in `panel_masters` table (or logical entity)

**Proposal Panel (Instance):**
- Runtime instance linked to specific Proposal/Quotation
- Mutable (can be modified per proposal)
- Created via copy operation from Panel Master
- Stored in `QuotationSale` table with `PanelMasterId` reference field

### 3.2 PanelMasterId Field Contract

**CRITICAL RULE:** `PanelMasterId` is **reference-only**.

- Stored in `QuotationSale` table
- Points back to `panel_masters` table (or logical entity)
- **NEVER mutated** after initial copy
- **NEVER used for behavioral linking** (no cascading updates, no triggers)
- **Reference/tracking only** — Panel Master remains immutable

### 3.3 Copy-Never-Link Rule

**CRITICAL RULE:** Always copy Panel Master, never link.

- Panel Master → Proposal Panel: **COPY operation creates new instance**
- Panel Master → Feeders: **COPY operation creates new feeder instances**
- Panel Master → Proposal BOM: **COPY operation creates new BOM instances**
- **NO direct references** from runtime instances back to master (except PanelMasterId for tracking)

---

## 4) Complete Flow Diagram

### 4.1 End-to-End Flow

```
┌─────────────────────────────────────────────────────────┐
│ DESIGN-TIME MASTERS (Immutable)                         │
├─────────────────────────────────────────────────────────┤
│ Item Master                                             │
│   ↓                                                     │
│ Master BOM (generic templates)                         │
│   ↓                                                     │
│ Feeder Master (optional) → TemplateType='FEEDER'       │
│   ↓                                                     │
│ Panel Master → panel_masters                           │
└─────────────────────────────────────────────────────────┘
                     │
                     │ [COPY OPERATION]
                     │ (Copy-Never-Link)
                     ↓
┌─────────────────────────────────────────────────────────┐
│ RUNTIME INSTANCES (Mutable, per Proposal)              │
├─────────────────────────────────────────────────────────┤
│ Quotation (Proposal Root)                              │
│   ↓                                                     │
│ Proposal Panel → QuotationSale (PanelMasterId ref)    │
│   ↓                                                     │
│ Feeders → QuotationSaleBom (Level=0)                  │
│   ↓                                                     │
│ Proposal BOMs → QuotationSaleBom (Level>=1)           │
│   ↓                                                     │
│ Proposal BOM Items → QuotationSaleBomItem             │
│   ↓                                                     │
│ [RESOLVE] → Item Master                                │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Flow Rules

1. **Unidirectional:** Masters → Instances (one direction only)
2. **Copy Operation:** Single point of transformation
3. **No Reverse Mutation:** Instances never mutate masters
4. **Reference Tracking:** PanelMasterId stored but never used for behavioral linking

---

## 5) Integration with Feeder BOM

### 5.1 Feeder Copy Within Panel Copy

When copying Panel Master → Proposal Panel:

1. Panel copy operation identifies feeders referenced by Panel Master
2. For each feeder reference:
   - If `FeederMasterId` present → use Feeder Master template
   - If `FeederMasterId` absent → use direct feeder copy
3. Copy operation creates new feeder instances (`QuotationSaleBom`, Level=0)
4. Copy operation delegates to Feeder BOM copy logic (reuse `BomEngine::copyFeederTree()` pattern)
5. All feeder instances are independent copies (copy-never-link)

### 5.2 Feeder Copy Governance

Feeder copy within Panel copy must follow Feeder BOM governance:
- Reuse detection (identity matching)
- Clear-before-copy (soft delete Status=0 → 1)
- Copy items (new IDs, copy-never-link)
- Record copy history (insert to `bom_copy_history`)

---

## 6) Alignment with Fundamentals

### 6.1 Mental Model Alignment

This canonical flow implements the **"One Master → Many Instances"** mental model:

- One Panel Master → Many Proposal Panels
- One Feeder Master → Many Feeders (within multiple panels)
- One Master BOM → Many Proposal BOMs (within multiple feeders/panels)
- One Item Master → Many Proposal BOM Items (across all BOMs)

### 6.2 Fundamentals Rules Enforced

- ✅ Copy-Never-Link: All instances are independent copies
- ✅ No Upward Mutation: Masters remain immutable
- ✅ Reference-Only Tracking: PanelMasterId stored but never mutated
- ✅ Clear Separation: Design-time vs Runtime explicitly separated

---

## 7) Exit Criteria (PB0.1)

- [x] Canonical flow document created
- [x] Runtime hierarchy locked
- [x] Design-time master hierarchy locked
- [x] Master → Instance separation explicit
- [x] PanelMasterId reference-only rule locked
- [x] Copy-never-link rule referenced (detailed in COPY_RULES.md)
- [x] Integration with Feeder BOM documented
- [x] Alignment with Fundamentals verified

**Status:** ✅ **COMPLETE** — Canonical flow locked

---

## 8) References

### Internal Documents
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` - Main planning track
- `PLANNING/PANEL_BOM/COPY_RULES.md` - Detailed copy rules (PB0.2)
- `PLANNING/PANEL_BOM/QUANTITY_CONTRACT.md` - Quantity contract (PB0.3)

### External References
- `PLANNING/FEEDER_BOM/FEEDER_BOM_PLAN_NORMALIZATION.md` - Feeder BOM pattern reference
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` - Fundamentals hierarchy
- `PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md` - Master→Instance mapping

---

**END OF DOCUMENT**

