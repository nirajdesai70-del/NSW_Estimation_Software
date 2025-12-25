# Canonical BOM Hierarchy — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Canonical BOM hierarchy definition (design-time vs runtime)  
**Status:** 🔒 FROZEN (Reference Only)

---

## A) Design-Time Masters (Template Definitions)

**PANEL MASTER** (L0 - Design-time)
  ├─ **FEEDER MASTER** (L1 - Design-time; TemplateType='FEEDER')
  │   └─ **BOM MASTER** (L2 - Design-time; TemplateType='BOM')
  │       └─ **BOM ITEM MASTER** (L2 only; ProductType=2; resolve → Item Master)

**Rules:**
- Panel Master defines panel type
- Feeder Master defines feeder type (reusable across panels)
- BOM Master defines BOM structure
- BOM Item Master references Item Master (ProductType=2)

**Implementation:**
- Panel Master: Panel definition (design-time)
- Feeder Master: `master_boms` where `TemplateType='FEEDER'`
- BOM Master: `master_boms` where `TemplateType='BOM'`
- BOM Item Master: Item Master references (ProductType=2)

---

## B) Runtime Instances (Quotation Scoped; Copy-Never-Link)

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

**Implementation:**
- Proposal BOM Master: `QuotationId` (root reference)
- Proposal Panels: `quotation_sale` where `QuotationId = :id`
- Feeder Instances: `quotation_sale_boms` where `QuotationId = :id` AND `MasterBomId` references Feeder Master
- Proposal BOMs: `quotation_sale_boms` where `QuotationId = :id` AND executable
- Proposal BOM Items: `quotation_sale_bom_items` where `QuotationId = :id`

---

## C) Rules

### C.1 Copy-Never-Link
- All instances are copies, never links
- Feeder Instances are copies of Feeder Master
- Proposal BOMs are copies of BOM Master
- No upward mutation allowed

### C.2 No Upward Mutation
- Instances never mutate masters
- Feeder Instances never mutate Feeder Master
- Proposal BOMs never mutate BOM Master
- Proposal BOM Items never mutate Item Master

### C.3 One Master → Many Instances
- Feeder Master can have many Feeder Instances across panels
- BOM Master can have many Proposal BOMs
- Item Master can have many Proposal BOM Items

### C.4 Quotation Scoped
- All runtime entities belong to one Proposal BOM Master (QuotationId)
- All entities have `QuotationId` FK for ownership
- Ownership is transitive

### C.5 Template Apply
- Creates new instance via copy operation
- Template apply copies structure from master to instance
- Copy operation is idempotent (Phase-2)

### C.6 Clear-Before-Copy
- Template apply clears existing before copying (Phase-2, conditional patch P3)
- Prevents duplicate stacking
- Ensures clean instance state

---

## D) Layer Annotations

### Design-Time (L0/L1/L2)
- **L0:** Panel Master
- **L1:** Feeder Master (TemplateType='FEEDER')
- **L2:** BOM Master (TemplateType='BOM')
- **L2 Items:** BOM Item Master (ProductType=2)

### Runtime (Quotation Scoped)
- **Root:** Proposal BOM Master (QuotationId)
- **L0:** Proposal Panels
- **L1:** Feeder Instances (instances of Feeder Master)
- **L2:** Proposal BOMs (executable)
- **L2 Items:** Proposal BOM Items (ProductType=2)

---

## E) Verification Queries

See `FUNDAMENTALS_VERIFICATION_QUERIES.md` for complete verification framework.

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

**Relevant Patches:**
- **P3:** Clear-before-copy (if VQ-002 fails)
- **P4:** Hierarchy verification (if VQ-004 fails)

Patches are **conditional** and may be applied only if verification fails (VQ-002, VQ-004).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF CANONICAL BOM HIERARCHY**

