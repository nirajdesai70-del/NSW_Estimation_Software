# Master→Instance Mapping — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Complete master→instance mapping across all layers  
**Status:** 🔒 FROZEN (Reference Only)

---

## Mapping Table

| Layer | Master (Design-time) | Instance (Runtime) | Reference Mechanism |
|-------|----------------------|-------------------|---------------------|
| **L0** | Panel Master | Proposal Panel | `quotation_sale` references panel definition |
| **L1** | Feeder Master (`master_boms` where `TemplateType='FEEDER'`) | Feeder Instance (`quotation_sale_boms` where `MasterBomId` references Feeder Master) | `quotation_sale_boms.MasterBomId` → `master_boms.MasterBomId` |
| **L2** | BOM Master (`master_boms` where `TemplateType='BOM'`) | Proposal BOM (`quotation_sale_boms` executable) | `quotation_sale_boms` structure copied from BOM Master |
| **L2 Items** | Item Master | Proposal BOM Item | `quotation_sale_bom_items.ProductType=2` → Item Master |
| **Root** | N/A (quotation-level) | Proposal BOM Master (`QuotationId`) | `QuotationId` as root reference |

---

## Detailed Mapping

### L0: Panel Master → Proposal Panel

**Master:**
- Panel Master (design-time definition)

**Instance:**
- Proposal Panel (`quotation_sale`)

**Reference Mechanism:**
- `quotation_sale` references panel definition
- Panel type determines structure

**Notes:**
- Proposal Panels are copies, not links
- One Panel Master → Many Proposal Panels (across quotations)

---

### L1: Feeder Master → Feeder Instance

**Master:**
- Feeder Master = `master_boms` where `TemplateType='FEEDER'`
- Key: `MasterBomId`

**Instance:**
- Feeder Instance = `quotation_sale_boms` where `MasterBomId` references Feeder Master
- Key: `QuotationSaleBomId`

**Reference Mechanism:**
- `quotation_sale_boms.MasterBomId` → `master_boms.MasterBomId` (where `TemplateType='FEEDER'`)
- FK relationship establishes master→instance link

**Notes:**
- Feeder Instances are copies, not links
- One Feeder Master → Many Feeder Instances (across panels and quotations)
- Feeder Instances never mutate Feeder Master

**Verification Query:**
```sql
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

### L2: BOM Master → Proposal BOM

**Master:**
- BOM Master = `master_boms` where `TemplateType='BOM'`
- Key: `MasterBomId`

**Instance:**
- Proposal BOM = `quotation_sale_boms` (executable)
- Key: `QuotationSaleBomId`

**Reference Mechanism:**
- `quotation_sale_boms` structure copied from BOM Master
- Copy operation creates new instance

**Notes:**
- Proposal BOMs are copies, not links
- One BOM Master → Many Proposal BOMs (across feeders and quotations)
- Proposal BOMs never mutate BOM Master

---

### L2 Items: Item Master → Proposal BOM Item

**Master:**
- Item Master (product/item definition)
- Key: Item identifier

**Instance:**
- Proposal BOM Item = `quotation_sale_bom_items` where `ProductType=2`
- Key: `QuotationSaleBomItemId`

**Reference Mechanism:**
- `quotation_sale_bom_items.ProductType=2` → Item Master
- Item reference resolves to Item Master

**Notes:**
- Proposal BOM Items reference Item Master
- One Item Master → Many Proposal BOM Items (across BOMs and quotations)
- Proposal BOM Items never mutate Item Master

---

### Root: Proposal BOM Master

**Master:**
- N/A (quotation-level, not a template)

**Instance:**
- Proposal BOM Master = `QuotationId` (root reference)

**Reference Mechanism:**
- `QuotationId` as root reference
- All runtime entities have `QuotationId` FK:
  - `quotation_sale.QuotationId`
  - `quotation_sale_boms.QuotationId`
  - `quotation_sale_bom_items.QuotationId`

**Notes:**
- One Proposal BOM Master per quotation
- Owns all runtime entities
- Root of ownership graph

**Verification Query:**
```sql
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

## Summary Rules

1. **Copy-Never-Link:** All instances are copies, never links
2. **No Upward Mutation:** Instances never mutate masters
3. **One Master → Many Instances:** Each master can have many instances
4. **Quotation Scoped:** All runtime entities belong to one Proposal BOM Master
5. **Reference Mechanisms:** Each layer has explicit reference mechanism (FK, copy, etc.)

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

**Relevant Patches:**
- **P1:** Reuse detection (if VQ-001 fails)
- **P3:** Clear-before-copy (if VQ-002 fails)
- **P4:** Mapping verification (if VQ-004 fails)

Patches are **conditional** and may be applied only if verification fails (VQ-001, VQ-002, VQ-004).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF MASTER→INSTANCE MAPPING**

