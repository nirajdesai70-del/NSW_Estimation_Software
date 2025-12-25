# Fundamentals Verification Queries — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Read-only verification queries to validate fundamentals baseline alignment  
**Status:** 🔒 FROZEN (Reference Only)  
**Execution:** Read-only queries only (no data mutation)

---

## Verification Framework

### Rules
1. **Read-Only:** All queries are SELECT statements only
2. **No Mutation:** No INSERT, UPDATE, DELETE, or DDL
3. **Evidence Required:** All query results must be captured
4. **Conditional:** Patches apply only if verification fails

### Execution Order
Execute queries in sequence (VQ-001 through VQ-005).  
If any query fails → proceed to patch decision gate (see `EXECUTION_WINDOW_SOP.md`).

---

## VQ-001: Feeder Masters Exist

### Purpose
Verify that Feeder Masters exist in the database as logical abstractions over `master_boms` where `TemplateType='FEEDER'`.

### Query
```sql
-- VQ-001: List all Feeder Masters (design-time)
SELECT 
    MasterBomId AS FeederMasterId,
    MasterBomName AS FeederName,
    TemplateType,
    Status,
    CreatedAt,
    UpdatedAt
FROM master_boms
WHERE TemplateType = 'FEEDER' AND Status = 0
ORDER BY MasterBomId;
```

### Expected Result
- At least one row returned (Feeder Masters exist)
- All rows have `TemplateType = 'FEEDER'`
- All rows have `Status = 0` (active)

### Failure Condition
- Zero rows returned (no Feeder Masters exist)
- Rows with `TemplateType != 'FEEDER'` (data inconsistency)
- All rows have `Status != 0` (no active Feeder Masters)

### Patch Trigger
If fails → Consider P1 (Feeder Template Filter Standardization) or P4 (Legacy Data Normalization).

### Evidence Capture
- Query output (CSV or text)
- Row count
- Sample rows (if any)

---

## VQ-002: Feeder Master → Instance Relationship

### Purpose
Verify that Feeder Instances correctly reference Feeder Masters via `MasterBomId` FK, and check for duplicate stacking (clear-before-copy violation).

### Query
```sql
-- VQ-002: Count Feeder Instances per Feeder Master
SELECT 
    mb.MasterBomId AS FeederMasterId,
    mb.MasterBomName AS FeederName,
    COUNT(qsb.QuotationSaleBomId) AS InstanceCount,
    COUNT(DISTINCT qsb.QuotationId) AS QuotationCount
FROM master_boms mb
LEFT JOIN quotation_sale_boms qsb ON qsb.MasterBomId = mb.MasterBomId
WHERE mb.TemplateType = 'FEEDER' AND mb.Status = 0
GROUP BY mb.MasterBomId, mb.MasterBomName
ORDER BY mb.MasterBomId;

-- VQ-002b: Check for duplicate stacking (same Feeder Master + Quotation + Panel)
SELECT 
    qsb.MasterBomId AS FeederMasterId,
    qsb.QuotationId,
    qsb.QuotationSaleId AS PanelId,
    COUNT(*) AS DuplicateCount
FROM quotation_sale_boms qsb
INNER JOIN master_boms mb ON mb.MasterBomId = qsb.MasterBomId
WHERE mb.TemplateType = 'FEEDER' AND mb.Status = 0
GROUP BY qsb.MasterBomId, qsb.QuotationId, qsb.QuotationSaleId
HAVING COUNT(*) > 1;
```

### Expected Result
- VQ-002: At least one Feeder Master has instances (or zero instances is acceptable)
- VQ-002b: Zero rows returned (no duplicate stacking)

### Failure Condition
- VQ-002b returns rows (duplicate stacking detected - clear-before-copy violation)
- Feeder Instances reference non-existent Feeder Masters (FK violation)

### Patch Trigger
If fails → Apply P3 (Copy-Never-Link Enforcement Guard / Clear-Before-Copy).

### Evidence Capture
- Query output (CSV or text)
- Instance count per Feeder Master
- Duplicate stacking evidence (if any)

---

## VQ-003: Proposal BOM Master Ownership

### Purpose
Verify that all runtime entities correctly belong to a Proposal BOM Master (QuotationId), and that ownership is complete.

### Query
```sql
-- VQ-003: Verify Proposal BOM Master ownership
SELECT 
    q.QuotationId AS ProposalBomMasterId,
    COUNT(DISTINCT qs.QuotationSaleId) AS ProposalPanelCount,
    COUNT(DISTINCT qsb.QuotationSaleBomId) AS FeederAndBomCount,
    COUNT(DISTINCT qsbi.QuotationSaleBomItemId) AS BomItemCount
FROM quotations q
LEFT JOIN quotation_sale qs ON qs.QuotationId = q.QuotationId
LEFT JOIN quotation_sale_boms qsb ON qsb.QuotationId = q.QuotationId
LEFT JOIN quotation_sale_bom_items qsbi ON qsbi.QuotationId = q.QuotationId
GROUP BY q.QuotationId
ORDER BY q.QuotationId;

-- VQ-003b: Check for orphan runtime entities (missing QuotationId)
SELECT 'quotation_sale' AS TableName, COUNT(*) AS OrphanCount
FROM quotation_sale
WHERE QuotationId IS NULL
UNION ALL
SELECT 'quotation_sale_boms' AS TableName, COUNT(*) AS OrphanCount
FROM quotation_sale_boms
WHERE QuotationId IS NULL
UNION ALL
SELECT 'quotation_sale_bom_items' AS TableName, COUNT(*) AS OrphanCount
FROM quotation_sale_bom_items
WHERE QuotationId IS NULL;
```

### Expected Result
- VQ-003: All quotations have associated runtime entities (or zero is acceptable)
- VQ-003b: All orphan counts are zero (no orphan runtime entities)

### Failure Condition
- VQ-003b returns non-zero orphan counts (ownership violation)
- Runtime entities exist without valid QuotationId

### Patch Trigger
If fails → Apply P2 (Quotation Ownership Enforcement).

### Evidence Capture
- Query output (CSV or text)
- Ownership counts per Proposal BOM Master
- Orphan entity evidence (if any)

---

## VQ-004: Orphan Runtime BOMs

### Purpose
Verify that all runtime BOMs (Feeder Instances and Proposal BOMs) have valid references to Feeder Masters or BOM Masters.

### Query
```sql
-- VQ-004: Check for orphan runtime BOMs (invalid MasterBomId references)
SELECT 
    qsb.QuotationSaleBomId,
    qsb.MasterBomId,
    qsb.QuotationId,
    CASE 
        WHEN mb.MasterBomId IS NULL THEN 'ORPHAN'
        WHEN mb.TemplateType NOT IN ('FEEDER', 'BOM') THEN 'INVALID_TYPE'
        ELSE 'VALID'
    END AS ReferenceStatus
FROM quotation_sale_boms qsb
LEFT JOIN master_boms mb ON mb.MasterBomId = qsb.MasterBomId
WHERE mb.MasterBomId IS NULL 
   OR mb.TemplateType NOT IN ('FEEDER', 'BOM')
   OR mb.Status != 0;

-- VQ-004b: Check for runtime BOMs with missing MasterBomId
SELECT 
    QuotationSaleBomId,
    QuotationId,
    MasterBomId
FROM quotation_sale_boms
WHERE MasterBomId IS NULL;
```

### Expected Result
- VQ-004: Zero rows returned (no orphan runtime BOMs)
- VQ-004b: Zero rows returned (all runtime BOMs have MasterBomId)

### Failure Condition
- Rows returned (orphan runtime BOMs detected)
- Runtime BOMs reference non-existent or invalid masters

### Patch Trigger
If fails → Consider P2 (Quotation Ownership Enforcement) or P4 (Legacy Data Normalization).

### Evidence Capture
- Query output (CSV or text)
- Orphan BOM evidence (if any)
- Reference status breakdown

---

## VQ-005: Copy-Never-Link Sanity Check

### Purpose
Verify that copy-never-link principle is maintained (no master mutation from runtime operations).

### Query
```sql
-- VQ-005: Check for master mutation indicators (read-only check)
-- This query checks for suspicious patterns that might indicate master mutation

-- VQ-005a: Check if master_boms have been updated after quotation creation
-- (This is a pattern check, not a definitive violation)
SELECT 
    mb.MasterBomId,
    mb.MasterBomName,
    mb.TemplateType,
    mb.UpdatedAt AS MasterUpdatedAt,
    MAX(q.CreatedAt) AS LatestQuotationCreatedAt
FROM master_boms mb
LEFT JOIN quotations q ON 1=1
LEFT JOIN quotation_sale_boms qsb ON qsb.MasterBomId = mb.MasterBomId AND qsb.QuotationId = q.QuotationId
WHERE mb.TemplateType IN ('FEEDER', 'BOM')
GROUP BY mb.MasterBomId, mb.MasterBomName, mb.TemplateType, mb.UpdatedAt
HAVING mb.UpdatedAt > MAX(q.CreatedAt);

-- VQ-005b: Verify Feeder Master filter usage (code-level check via query pattern)
-- This is a documentation check - actual code review required
-- Query verifies that feeder templates are correctly identified
SELECT 
    COUNT(*) AS FeederMasterCount,
    COUNT(CASE WHEN TemplateType = 'FEEDER' THEN 1 END) AS ExplicitlyFilteredCount
FROM master_boms
WHERE Status = 0;
```

### Expected Result
- VQ-005a: Zero rows returned (no suspicious master mutation patterns)
- VQ-005b: FeederMasterCount = ExplicitlyFilteredCount (all feeder masters correctly identified)

### Failure Condition
- VQ-005a returns rows (suspicious master mutation patterns detected)
- VQ-005b shows mismatch (feeder templates not correctly filtered)

### Patch Trigger
If fails → Apply P1 (Feeder Template Filter Standardization) or P3 (Copy-Never-Link Enforcement Guard).

### Evidence Capture
- Query output (CSV or text)
- Mutation pattern evidence (if any)
- Filter usage verification

---

## Verification Summary Template

**Execution Date:** _______________  
**Executed By:** _______________  

| Query | Status | Evidence File | Notes |
|-------|--------|---------------|-------|
| VQ-001 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| VQ-002 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| VQ-003 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| VQ-004 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| VQ-005 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |

**Overall Status:** ⬜ ALL PASS / ⬜ FAILURES DETECTED  
**Patch Decision:** ⬜ NO PATCHES / ⬜ PATCHES REQUIRED (see PATCH_REGISTER.md)

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

Patches are **conditional** and may be applied only if verification fails (VQ-001..VQ-005).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF FUNDAMENTALS VERIFICATION QUERIES**

