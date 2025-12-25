# Feeder Master Backend Design — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Canonical Feeder Master definition (logical abstraction over `master_boms`)  
**Status:** 🔒 FROZEN (Reference Only)

---

## 1. Definition

**Feeder Master** = Design-time definition of a feeder type, represented as a logical abstraction over `master_boms` where `TemplateType='FEEDER'`.

**Key Characteristics:**
- NOT tied to a single panel
- Defines feeder type, allowed BOM structure, default behavior
- Reusable across multiple panels
- One Feeder Master → Many Feeder Instances (across all panels)

---

## 2. Purpose

- Canonical feeder definition (what a feeder is conceptually)
- Reusable across multiple panels
- Defines feeder type, allowed BOM structure, default behavior
- Establishes master→instance relationship (via `MasterBomId`)

---

## 3. Scope

### In Scope
- Feeder identity (MasterBomId, MasterBomName)
- Feeder type definition (TemplateType='FEEDER')
- Master→Instance relationship (via MasterBomId FK)
- Verification queries (read-only)

### Out of Scope
- Feeder instance lifecycle (Phase-2)
- Feeder template apply logic (Phase-2)
- Feeder editing (Phase-3)
- Schema changes (no new tables)

---

## 4. Lifecycle

- **Created:** Design-time (admin/manual)
- **Mutated:** Design-time only (future instances only)
- **Referenced:** Runtime instances via `MasterBomId`
- **Deleted:** Design-time only (deprecation, not deletion)

---

## 5. Data Representation

**Chosen approach:** ✅ Logical abstraction over existing `master_boms` table

**Rationale:**
- Feeder identity must be stable and referenceable
- Current implementation uses `master_boms` with `TemplateType=FEEDER`
- Feeder Master is a logical abstraction, not a new table
- Supports master→instance traceability via MasterBomId
- Zero migration risk
- Execution-ready (no code changes needed)

**Implementation Mapping:**
- Feeder Master = `master_boms` row where `TemplateType = 'FEEDER'`
- Feeder Instance references Feeder Master via `MasterBomId` (FK to `master_boms`)
- No new table required
- Existing code structure preserved

---

## 6. Conceptual Data Model

**Feeder Master is represented by:**
- Table: `master_boms`
- Filter: `TemplateType = 'FEEDER'`
- Key fields:
  - `MasterBomId` (PK) - serves as FeederMasterId
  - `MasterBomName` - feeder name/identity
  - `TemplateType` - must be 'FEEDER'
  - `Status` - active/deprecated
  - `CreatedAt`, `UpdatedAt`

**Feeder Instance references:**
- `quotation_sale_boms.MasterBomId` → `master_boms.MasterBomId` (where TemplateType='FEEDER')
- This establishes the master→instance relationship

> ⚠️ **No separate `feeder_masters` table. Feeder Master is a logical view over `master_boms`.**

---

## 7. Relationships

### 7.1 Inbound References
- Referenced by **Feeder Instance** (`quotation_sale_boms`)
- Reference type: `MasterBomId` (FK to `master_boms` where `TemplateType='FEEDER'`)
- Relationship: One Feeder Master → Many Feeder Instances (across all panels)

### 7.2 Outbound References
- Feeder Master may reference BOM Masters (via hierarchy)
- Feeder Master defines structure for Feeder Instances

---

## 8. Copy Rules

- **Copy-Never-Link:** Feeder Instances are copies, not links
- **No Upward Mutation:** Feeder Instances never mutate Feeder Master
- **Template Apply:** Creates new instance via copy operation (Phase-2)
- **Clear-Before-Copy:** Template apply clears existing before copying (Phase-2, conditional patch P3)

---

## 9. Verification Query (Example)

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

## 10. Non-Goals

This document does NOT define:
- Feeder instance creation logic (Phase-2)
- Feeder template apply implementation (Phase-2)
- Feeder editing operations (Phase-3)
- Panel BOM structure (separate document)

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

**Relevant Patches:**
- **P1:** Reuse detection (if VQ-001 fails)
- **P3:** Clear-before-copy (if VQ-002 fails)

Patches are **conditional** and may be applied only if verification fails (VQ-001, VQ-002).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF FEEDER MASTER BACKEND DESIGN**

