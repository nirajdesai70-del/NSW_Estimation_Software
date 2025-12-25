# Fundamentals Baseline Bundle — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Canonical fundamentals baseline (Feeder Master, Proposal BOM Master, hierarchy, mapping)  
**Status:** 🔒 FROZEN (Reference Only)

---

## 0) Scope & Non-Scope

### In Scope
- Feeder Master definition (logical abstraction over `master_boms`)
- Proposal BOM Master definition (logical container over `QuotationId`)
- Canonical BOM hierarchy (design-time vs runtime)
- Master→Instance mapping (all layers)
- Gap fix plan (GAP-001, GAP-002, GAP-005, GAP-006)
- Verification framework (read-only queries)
- Conditional patch framework (P1–P4)

### Out of Scope
- Schema changes (no new tables)
- Code changes (planning only)
- Runtime execution (deferred to execution window)
- Testing (deferred to execution window)

---

## 1) Frozen Mental Model

### Core Principles
1. **Feeder Master** = Design-time definition of a feeder type
   - NOT tied to a single panel
   - Defines feeder type, allowed BOM structure, default behavior
   - One Feeder Master → Many Feeder Instances (across all panels)

2. **Proposal BOM Master** = Top-level runtime container
   - One per quotation (`QuotationId`)
   - Owns all runtime entities (panels, feeders, BOMs)
   - Root of ownership graph

3. **Copy-Never-Link** = Instances never mutate masters
   - Feeder Instances are copies, not links
   - Proposal BOMs are copies, not links
   - No upward mutation allowed

4. **Hierarchy Rules**
   - Design-time: Panel Master → Feeder Master → BOM Master
   - Runtime: Proposal BOM Master → Proposal Panels → Feeder Instances → Proposal BOMs → Proposal BOM Items

---

## 2) Fundamentals Decision Record

### Decision A: Feeder Master Representation
**Chosen:** Logical abstraction over `master_boms` table  
**Rationale:**
- Zero migration risk
- Execution-ready (no code changes)
- Verifiable immediately: `SELECT * FROM master_boms WHERE TemplateType='FEEDER'`
- Existing `MasterBomId` references already establish master→instance relationship

**Implementation Mapping:**
- Feeder Master = `master_boms` row where `TemplateType = 'FEEDER'`
- Feeder Instance references Feeder Master via `quotation_sale_boms.MasterBomId` (FK to `master_boms`)

### Decision B: Proposal BOM Master Representation
**Chosen:** Logical container over `QuotationId`  
**Rationale:**
- Zero migration risk
- Execution-ready (current code already uses `QuotationId` everywhere)
- Verifiable immediately: all runtime entities have `QuotationId`
- Clear ownership boundaries without new infrastructure

**Implementation Mapping:**
- Proposal BOM Master = `QuotationId` (root reference)
- All runtime entities traceable back to `QuotationId`

---

## 3) Feeder Master Design (v1.0)

### 3.1 Definition
**Feeder Master** = Design-time definition of a feeder type, represented as a logical abstraction over `master_boms` where `TemplateType='FEEDER'`.

### 3.2 Purpose
- Canonical feeder definition (what a feeder is conceptually)
- Reusable across multiple panels
- Defines feeder type, allowed BOM structure, default behavior

### 3.3 Scope
**In Scope:**
- Feeder identity (MasterBomId, MasterBomName)
- Feeder type definition (TemplateType='FEEDER')
- Master→Instance relationship (via MasterBomId FK)

**Out of Scope:**
- Feeder instance lifecycle (Phase-2)
- Feeder template apply logic (Phase-2)
- Feeder editing (Phase-3)

### 3.4 Lifecycle
- Created: Design-time (admin/manual)
- Mutated: Design-time only (future instances only)
- Referenced: Runtime instances via `MasterBomId`

### 3.5 Data Representation
**Implementation:**
- Table: `master_boms`
- Filter: `TemplateType = 'FEEDER'`
- Key fields:
  - `MasterBomId` (PK) - serves as FeederMasterId
  - `MasterBomName` - feeder name/identity
  - `TemplateType` - must be 'FEEDER'
  - `Status` - active/deprecated
  - `CreatedAt`, `UpdatedAt`

**No separate `feeder_masters` table. Feeder Master is a logical view over `master_boms`.**

### 3.6 Conceptual Data Model
**Feeder Master is represented by:**
- Table: `master_boms`
- Filter: `TemplateType = 'FEEDER'`
- Key: `MasterBomId`

**Feeder Instance references:**
- `quotation_sale_boms.MasterBomId` → `master_boms.MasterBomId` (where TemplateType='FEEDER')
- This establishes the master→instance relationship

### 3.7 Relationships
**Inbound References:**
- Referenced by **Feeder Instance** (`quotation_sale_boms`)
- Reference type: `MasterBomId` (FK to `master_boms` where `TemplateType='FEEDER'`)
- Relationship: One Feeder Master → Many Feeder Instances (across all panels)

### 3.8 Copy Rules
- **Copy-Never-Link:** Feeder Instances are copies, not links
- **No Upward Mutation:** Feeder Instances never mutate Feeder Master
- **Template Apply:** Creates new instance via copy operation (Phase-2)

### 3.9 Verification Query (Example)
```sql
-- List all Feeder Masters (design-time)
SELECT MasterBomId, MasterBomName, TemplateType, Status
FROM master_boms
WHERE TemplateType = 'FEEDER' AND Status = 0;

-- Count Feeder Instances per Feeder Master
SELECT 
    mb.MasterBomId AS FeederMasterId,
    mb.MasterBomName AS FeederName,
    COUNT(qsb.QuotationSaleBomId) AS InstanceCount
FROM master_boms mb
LEFT JOIN quotation_sale_boms qsb ON qsb.MasterBomId = mb.MasterBomId
WHERE mb.TemplateType = 'FEEDER' AND mb.Status = 0
GROUP BY mb.MasterBomId, mb.MasterBomName;
```

---

## 4) Proposal BOM Master Design (v1.0)

### 4.1 Definition
**Proposal BOM Master** = Top-level runtime container, represented as a logical container over `QuotationId`. One per quotation, owns all runtime entities.

### 4.2 Purpose
- Quotation-level root reference
- Ownership boundary (all runtime entities belong to one Proposal BOM Master)
- Traceability root (all entities traceable back to `QuotationId`)

### 4.3 Scope
**In Scope:**
- Ownership definition (QuotationId as root)
- Ownership graph (what entities belong to Proposal BOM Master)
- Reference mechanism (QuotationId FK in all runtime entities)

**Out of Scope:**
- Quotation creation/editing (existing functionality)
- Future enhancement: Optional `proposal_bom_masters` table for audit (explicitly deferred)

### 4.4 Lifecycle
- Created: When quotation is created
- Mutated: Via quotation lifecycle (existing)
- Deleted: When quotation is deleted (cascade)

### 4.5 Data Representation
**Implementation:**
- Root reference: `QuotationId` (from `quotations` table)
- All runtime entities have `QuotationId` FK:
  - `quotation_sale.QuotationId`
  - `quotation_sale_boms.QuotationId`
  - `quotation_sale_bom_items.QuotationId`

**No separate `proposal_bom_masters` table. Proposal BOM Master is a logical container over `QuotationId`.**

### 4.6 Ownership Graph
**Proposal BOM Master (QuotationId) owns:**
- Proposal Panels (`quotation_sale` where `QuotationId = :id`)
- Feeder Instances (`quotation_sale_boms` where `QuotationId = :id` AND `MasterBomId` references Feeder Master)
- Proposal BOMs (`quotation_sale_boms` where `QuotationId = :id` AND executable)
- Proposal BOM Items (`quotation_sale_bom_items` where `QuotationId = :id`)

### 4.7 Ownership Verification (Example)
```sql
-- Verify all runtime entities belong to a quotation (Proposal BOM Master)
SELECT 
    q.QuotationId AS ProposalBomMasterId,
    COUNT(DISTINCT qs.QuotationSaleId) AS ProposalPanelCount,
    COUNT(DISTINCT qsb.QuotationSaleBomId) AS FeederAndBomCount
FROM quotations q
LEFT JOIN quotation_sale qs ON qs.QuotationId = q.QuotationId
LEFT JOIN quotation_sale_boms qsb ON qsb.QuotationId = q.QuotationId
WHERE q.QuotationId = :quotation_id
GROUP BY q.QuotationId;
```

---

## 5) Canonical Hierarchy (v1.0)

### A) Design-Time Masters (Template Definitions)

**PANEL MASTER** (L0 - Design-time)
  ├─ **FEEDER MASTER** (L1 - Design-time; TemplateType='FEEDER')
  │   └─ **BOM MASTER** (L2 - Design-time; TemplateType='BOM')
  │       └─ **BOM ITEM MASTER** (L2 only; ProductType=2; resolve → Item Master)

**Rules:**
- Panel Master defines panel type
- Feeder Master defines feeder type (reusable across panels)
- BOM Master defines BOM structure
- BOM Item Master references Item Master (ProductType=2)

### B) Runtime Instances (Quotation Scoped; Copy-Never-Link)

**PROPOSAL BOM MASTER** = Quotation Runtime Root (ONE per quotation; QuotationId)
  ├─ **Proposal Panels** (copied from Panel Master)
  │   └─ **Feeder Instances** (instances of Feeder Master)
  │       └─ **Proposal BOMs** (executable)
  │           └─ **Proposal BOM Items** (L2 only; ProductType=2; resolve → Item Master)

**Rules:**
- Proposal BOM Master owns all runtime entities
- Proposal Panels are copies, not links
- Feeder Instances are copies, not links
- Proposal BOMs are copies, not links
- Proposal BOM Items reference Item Master (ProductType=2)

### C) Rules

1. **Copy-Never-Link:** All instances are copies, never links
2. **No Upward Mutation:** Instances never mutate masters
3. **One Master → Many Instances:** Feeder Master can have many Feeder Instances across panels
4. **Quotation Scoped:** All runtime entities belong to one Proposal BOM Master (QuotationId)
5. **Template Apply:** Creates new instance via copy operation
6. **Clear-Before-Copy:** Template apply clears existing before copying (Phase-2)

---

## 6) Master→Instance Mapping (v1.0)

| Layer | Master (Design-time) | Instance (Runtime) | Reference Mechanism |
|-------|----------------------|-------------------|---------------------|
| **L0** | Panel Master | Proposal Panel | `quotation_sale` references panel definition |
| **L1** | Feeder Master (`master_boms` where `TemplateType='FEEDER'`) | Feeder Instance (`quotation_sale_boms` where `MasterBomId` references Feeder Master) | `quotation_sale_boms.MasterBomId` → `master_boms.MasterBomId` |
| **L2** | BOM Master (`master_boms` where `TemplateType='BOM'`) | Proposal BOM (`quotation_sale_boms` executable) | `quotation_sale_boms` structure copied from BOM Master |
| **L2 Items** | Item Master | Proposal BOM Item | `quotation_sale_bom_items.ProductType=2` → Item Master |

**Notes:**
- Feeder Master = `master_boms` where `TemplateType='FEEDER'`
- Proposal BOM Master = `QuotationId` (root reference)
- All runtime entities have `QuotationId` FK for ownership
- Copy operations create new instances (copy-never-link)

---

## 7) Gap Fix Plan

### GAP-001: Feeder Template Apply Creates New Feeder Every Time
**Closure Path:**
- Verification: VQ-001, VQ-002
- Conditional Patch: P1 (reuse detection), P3 (clear-before-copy)

### GAP-002: Feeder Template Apply Missing Clear-Before-Copy
**Closure Path:**
- Verification: VQ-002
- Conditional Patch: P3 (clear-before-copy)

### GAP-005: BOM Node Edits Missing History/Backup
**Closure Path:**
- Reference: Fundamentals baseline documents hierarchy rules
- Implementation: Phase-3 (BOM node history)

### GAP-006: Lookup Pipeline Preservation Not Verified After Copy
**Closure Path:**
- Verification: VQ-005
- Conditional Patch: P3 (clear-before-copy)

---

## 8) TODO Tracker

See `FUNDAMENTALS_SERIAL_TRACKER_v1.0.md` for complete tracking.

---

## 9) Execution Framework

### SOP
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`

### Tracker
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_SERIAL_TRACKER_v1.0.md`

### Mode
- Read-only verification first
- Conditional patching only if verification fails
- Evidence mandatory

---

## 10) Next Planning Artifacts

- Verification Queries: `FUNDAMENTALS_VERIFICATION_QUERIES.md`
- Verification Checklist: `FUNDAMENTALS_VERIFICATION_CHECKLIST.md`
- Patch Plan: `PATCH_PLAN.md`
- Patch Register: `PATCH_REGISTER.md`

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

Patches are **conditional** and may be applied only if verification fails (VQ-001..VQ-005).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF FUNDAMENTALS BASELINE BUNDLE**

