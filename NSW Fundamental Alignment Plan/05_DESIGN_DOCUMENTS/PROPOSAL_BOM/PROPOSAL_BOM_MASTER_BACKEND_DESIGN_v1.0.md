# Proposal BOM Master Backend Design — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Canonical Proposal BOM Master definition (logical container over `QuotationId`)  
**Status:** 🔒 FROZEN (Reference Only)

---

## 1. Definition

**Proposal BOM Master** = Top-level runtime container, represented as a logical container over `QuotationId`. One per quotation, owns all runtime entities.

**Key Characteristics:**
- One per quotation (`QuotationId`)
- Owns all runtime entities (panels, feeders, BOMs)
- Root of ownership graph
- Traceability root (all entities traceable back to `QuotationId`)

---

## 2. Purpose

- Quotation-level root reference
- Ownership boundary (all runtime entities belong to one Proposal BOM Master)
- Traceability root (all entities traceable back to `QuotationId`)
- Establishes clear ownership boundaries without new infrastructure

---

## 3. Scope

### In Scope
- Ownership definition (QuotationId as root)
- Ownership graph (what entities belong to Proposal BOM Master)
- Reference mechanism (QuotationId FK in all runtime entities)
- Verification queries (read-only)

### Out of Scope
- Quotation creation/editing (existing functionality)
- Future enhancement: Optional `proposal_bom_masters` table for audit (explicitly deferred)
- Schema changes (no new tables)

---

## 4. Lifecycle

- **Created:** When quotation is created
- **Mutated:** Via quotation lifecycle (existing)
- **Deleted:** When quotation is deleted (cascade)
- **Ownership:** All runtime entities belong to one Proposal BOM Master

---

## 5. Data Representation

**Chosen approach:** ✅ Logical container over `QuotationId`

**Rationale:**
- Zero migration risk
- Execution-ready (current code already uses `QuotationId` everywhere)
- Verifiable immediately: all runtime entities have `QuotationId`
- Clear ownership boundaries without new infrastructure
- Future-proof: Option to add table later if audit needs arise (explicitly deferred)

**Implementation Mapping:**
- Proposal BOM Master = `QuotationId` (root reference)
- All runtime entities traceable back to `QuotationId`:
  - `quotation_sale.QuotationId`
  - `quotation_sale_boms.QuotationId`
  - `quotation_sale_bom_items.QuotationId`

> ⚠️ **No separate `proposal_bom_masters` table. Proposal BOM Master is a logical container over `QuotationId`.**

---

## 6. Conceptual Data Model

**Proposal BOM Master is represented by:**
- Root reference: `QuotationId` (from `quotations` table)
- All runtime entities have `QuotationId` FK:
  - `quotation_sale.QuotationId`
  - `quotation_sale_boms.QuotationId`
  - `quotation_sale_bom_items.QuotationId`

**Ownership Graph:**
- Proposal BOM Master (QuotationId) owns:
  - Proposal Panels (`quotation_sale` where `QuotationId = :id`)
  - Feeder Instances (`quotation_sale_boms` where `QuotationId = :id` AND `MasterBomId` references Feeder Master)
  - Proposal BOMs (`quotation_sale_boms` where `QuotationId = :id` AND executable)
  - Proposal BOM Items (`quotation_sale_bom_items` where `QuotationId = :id`)

---

## 7. Ownership Graph

**Proposal BOM Master (QuotationId)**
  ├─ **Proposal Panels** (`quotation_sale` where `QuotationId = :id`)
  │   └─ **Feeder Instances** (`quotation_sale_boms` where `QuotationId = :id` AND `MasterBomId` references Feeder Master)
  │       └─ **Proposal BOMs** (`quotation_sale_boms` where `QuotationId = :id` AND executable)
  │           └─ **Proposal BOM Items** (`quotation_sale_bom_items` where `QuotationId = :id`)

**Rules:**
- All runtime entities must have `QuotationId` FK
- All entities belong to exactly one Proposal BOM Master
- Ownership is transitive (items belong to BOMs, BOMs belong to feeders, feeders belong to panels, panels belong to quotation)

---

## 8. Ownership Verification (Example)

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

## 9. Non-Goals

This document does NOT define:
- Quotation creation/editing (existing functionality)
- Future `proposal_bom_masters` table (explicitly deferred)
- Panel BOM structure (separate document)
- Feeder Master definition (separate document)

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

**Relevant Patches:**
- **P2:** Ownership verification (if VQ-003 fails)
- **P3:** Clear-before-copy (if VQ-002 fails)

Patches are **conditional** and may be applied only if verification fails (VQ-002, VQ-003).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF PROPOSAL BOM MASTER BACKEND DESIGN**

