# Panel BOM Copy Rules

**File:** PLANNING/PANEL_BOM/COPY_RULES.md  
**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** ✅ FROZEN (PB0.2)  
**Purpose:** Lock the copy-never-link rule and PanelMasterId reference-only contract for Panel BOM

---

## ⚠️ CRITICAL: FROZEN CONTRACT

This document defines the **copy-never-link rule** and **PanelMasterId reference-only contract**. These are **locked, non-negotiable rules** — any deviation must be explicitly approved and documented.

**Mode:** Planning-only (execution deferred)  
**Governance:** Aligned with Feeder BOM methodology  
**Reference:** `PANEL_BOM_PLANNING_TRACK.md` PB0.2  
**Related:** `CANONICAL_FLOW.md` (PB0.1)

---

## 1) Copy-Never-Link Rule (Locked)

### 1.1 Core Principle

**ALWAYS copy Panel Master, never link.**

- Panel Master is a **template** (design-time, immutable)
- Proposal Panel is an **instance** (runtime, mutable per proposal)
- Copy operation creates **new, independent instances**
- **NO direct references** from runtime instances back to master (except tracking-only fields)

### 1.2 Copy Operation Behavior

**When copying Panel Master → Proposal Panel:**

1. **Create new Proposal Panel instance:**
   - New `QuotationSaleId` (new primary key)
   - New row in `QuotationSale` table
   - Linked to `QuotationId` (Proposal root)

2. **Copy Panel Master data:**
   - Copy all panel-level fields (Name, Description, Configuration, etc.)
   - Store `PanelMasterId` as **reference-only** (never mutated after copy)

3. **Copy Feeder references:**
   - For each feeder referenced by Panel Master:
     - If `FeederMasterId` present → copy from Feeder Master template
     - If `FeederMasterId` absent → copy from direct feeder reference
   - Create new feeder instances (`QuotationSaleBom`, Level=0)
   - Each feeder instance gets new `QuotationSaleBomId`

4. **Copy nested BOMs:**
   - Copy all Proposal BOMs (Level>=1) within feeders
   - Each BOM instance gets new `QuotationSaleBomId`
   - Maintain parent-child relationships via `ParentBomId` (pointing to new instance IDs)

5. **Copy BOM Items:**
   - Copy all items within each BOM
   - Each item instance gets new `QuotationSaleBomItemId`
   - Maintain reference to Item Master (via ItemId, not mutable)

### 1.3 Independence Guarantee

**All runtime instances are independent:**

- ✅ Modification to Proposal Panel **does NOT affect** Panel Master
- ✅ Modification to Feeder instance **does NOT affect** Feeder Master (if exists)
- ✅ Modification to Proposal BOM **does NOT affect** Master BOM
- ✅ Deletion of Proposal Panel **does NOT affect** Panel Master
- ✅ No cascading updates from instances to masters
- ✅ No database triggers linking instances to masters

---

## 2) PanelMasterId Reference-Only Contract (Locked)

### 2.1 Field Definition

**PanelMasterId** is stored in `QuotationSale` table:
- Column: `PanelMasterId` (or `panel_master_id` if snake_case)
- Type: Foreign key or reference integer
- Points to: `panel_masters` table (or logical entity)
- **Purpose:** Reference/tracking only

### 2.2 Reference-Only Rules

**CRITICAL:** PanelMasterId is **NEVER used for behavioral linking**.

**Allowed Uses:**
- ✅ Tracking which Panel Master was used as source
- ✅ Audit/logging purposes
- ✅ Display in UI ("Based on Panel Master: X")
- ✅ Reporting/analytics

**Forbidden Uses:**
- ❌ Cascading updates (if Panel Master changes, Proposal Panel does NOT change)
- ❌ Cascading deletes (if Panel Master deleted, Proposal Panel remains)
- ❌ Behavioral linking (no logic that reads PanelMasterId to fetch data)
- ❌ Mutation after initial copy (PanelMasterId never changes after creation)

### 2.3 Immutability Contract

**Panel Master is immutable:**

- ✅ Panel Master fields are **never mutated** by Proposal Panel operations
- ✅ Proposal Panel operations **never write** to `panel_masters` table
- ✅ No "sync" or "update from master" operations
- ✅ Panel Master remains as original template

**Proposal Panel is independent:**

- ✅ Proposal Panel fields can be modified per proposal
- ✅ Proposal Panel modifications do **not** propagate back to Panel Master
- ✅ Each Proposal Panel is a **snapshot** of Panel Master at copy time

---

## 3) No Upward Mutation Rule (Locked)

### 3.1 Unidirectional Flow

**Flow direction:** Masters → Instances (one direction only)

```
Panel Master (immutable)
    ↓
[COPY OPERATION]
    ↓
Proposal Panel (mutable, independent)
```

**Reverse flow is FORBIDDEN:**

```
Proposal Panel (mutable)
    ↑
[NO REVERSE OPERATION]
    ↑
Panel Master (immutable)
```

### 3.2 Upward Mutation Examples (Forbidden)

**These operations are FORBIDDEN:**

1. ❌ "Update Panel Master from Proposal Panel"
2. ❌ "Sync Proposal Panel changes back to Panel Master"
3. ❌ "Merge Proposal Panel modifications into Panel Master"
4. ❌ "Promote Proposal Panel to Panel Master"
5. ❌ Any operation that modifies `panel_masters` table based on Proposal Panel data

### 3.3 Template Update Process (If Needed)

**If Panel Master needs to be updated:**

1. Update Panel Master **directly** (not via Proposal Panel)
2. Update is **manual/administrative** (not driven by instance changes)
3. Existing Proposal Panels **remain unchanged** (they keep their copied snapshot)
4. New Proposal Panels created **after** update will use new Panel Master version

**This preserves:**
- Copy-never-link rule
- Independence of existing Proposal Panels
- Audit trail (PanelMasterId tracks which version was used)

---

## 4) Copy History Recording (Aligned with Feeder BOM)

### 4.1 History Table

**Copy history is recorded in `bom_copy_history`:**

- Source type: `PANEL_MASTER`
- Source ID: `PanelMasterId`
- Target type: `PROPOSAL_PANEL`
- Target ID: `QuotationSaleId`
- Operation metadata: Copy timestamp, user ID, options
- ID mapping: Panel → Panel, Feeder → Feeder, BOM → BOM, Item → Item

### 4.2 History Purpose

**Copy history enables:**
- ✅ Audit trail (which Panel Master was used)
- ✅ Debugging (trace instance back to source)
- ✅ Verification (confirm copy-never-link rule)
- ✅ Reuse detection (similar to Feeder BOM pattern)

### 4.3 History Alignment with Feeder BOM

Panel copy history follows the **same pattern** as Feeder BOM copy history:
- Same table structure (`bom_copy_history`)
- Same ID mapping format (JSON snapshots)
- Same verification queries (Gate-3: R1/S1/R2/S2)

---

## 5) Integration with Feeder BOM Copy Rules

### 5.1 Nested Feeder Copy

**When Panel copy triggers Feeder copy:**

- Feeder copy **delegates** to Feeder BOM copy logic
- Feeder copy **follows** Feeder BOM copy rules (copy-never-link, reuse detection, clear-before-copy)
- Feeder copy **records** history in `bom_copy_history` (with source type `FEEDER_MASTER` or `FEEDER_DIRECT`)

### 5.2 FeederMasterId Optional Branch

**Panel Master may reference feeders in two ways:**

1. **Via FeederMasterId (optional):**
   - Panel Master stores `FeederMasterId` pointing to Feeder Master template
   - Copy operation uses Feeder Master as source
   - Copy history records `FEEDER_MASTER` as source type

2. **Direct feeder reference (no FeederMasterId):**
   - Panel Master references feeder directly (not via Feeder Master)
   - Copy operation uses direct feeder as source
   - Copy history records `FEEDER_DIRECT` as source type

**Both paths must:**
- ✅ Create new feeder instances (copy-never-link)
- ✅ Record copy history
- ✅ Follow Feeder BOM copy rules

---

## 6) Alignment with Fundamentals

### 6.1 Mental Model Alignment

Copy rules implement the **"One Master → Many Instances"** mental model:

- One Panel Master → Many Proposal Panels (via copy)
- Each Proposal Panel is independent (no linking)
- PanelMasterId tracks source (reference-only)

### 6.2 Fundamentals Rules Enforced

- ✅ Copy-Never-Link: All instances are independent copies
- ✅ No Upward Mutation: Panel Master remains immutable
- ✅ Reference-Only Tracking: PanelMasterId stored but never mutated
- ✅ Clear Separation: Design-time vs Runtime explicitly separated

---

## 7) Exit Criteria (PB0.2)

- [x] Copy-never-link rule locked
- [x] PanelMasterId reference-only contract locked
- [x] No upward mutation rule locked
- [x] Copy history recording documented
- [x] Integration with Feeder BOM documented
- [x] Alignment with Fundamentals verified

**Status:** ✅ **COMPLETE** — Copy rules locked

---

## 8) References

### Internal Documents
- `PLANNING/PANEL_BOM/CANONICAL_FLOW.md` - Canonical flow (PB0.1)
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` - Main planning track

### External References
- `PLANNING/FEEDER_BOM/FEEDER_BOM_PLAN_NORMALIZATION.md` - Feeder BOM copy pattern
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` - Fundamentals hierarchy
- Panel Master design Part-4 (Copy Process) - Detailed copy flow

---

**END OF DOCUMENT**

