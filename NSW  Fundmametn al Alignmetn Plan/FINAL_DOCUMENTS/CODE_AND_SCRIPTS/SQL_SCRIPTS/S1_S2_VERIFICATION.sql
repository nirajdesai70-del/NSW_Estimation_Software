-- Phase-2 Gate-3 Verification Queries (S1 and S2)
-- Purpose: Complete verification SQL for R1 → S1 → R2 → S2 sequence
-- Database: nepl_quotation
-- Usage: Replace <FEEDER_ID_R1> with actual feeder ID from R1 response

-- ============================================
-- S1 QUERIES (After R1 - First Apply)
-- ============================================

-- S1-A: Copy History Written
SELECT 
    BomCopyHistoryId,
    SourceType,
    SourceId,
    TargetType,
    TargetId,
    Operation,
    UserId,
    Timestamp
FROM bom_copy_history
WHERE TargetId = <FEEDER_ID_R1>
ORDER BY BomCopyHistoryId DESC
LIMIT 5;

-- Expected: 1 row with Operation = 'COPY_FEEDER_TREE'

-- S1-B: No Illegal "Link-Copy" (Must be 0 rows)
SELECT 
    BomCopyHistoryId,
    SourceId,
    TargetId,
    Operation
FROM bom_copy_history
WHERE SourceId = TargetId
LIMIT 10;

-- Expected: 0 rows (copy-never-link pattern)

-- S1-C: Status Distribution (Active Items Only)
SELECT Status, COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
GROUP BY Status
ORDER BY Status;

-- Expected:
-- Status=0 → N items (active)
-- Status=1 → 0 items (no deleted items yet)

-- S1-D: No Duplicates in Active Set (Must be 0 rows)
SELECT 
    ProductId, 
    MakeId, 
    SeriesId, 
    COUNT(*) AS duplicate_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
  AND Status = 0
GROUP BY ProductId, MakeId, SeriesId
HAVING COUNT(*) > 1;

-- Expected: 0 rows (no duplicates)

-- S1-E: Feeder Row Inspection
SELECT 
    QuotationSaleBomId,
    QuotationId,
    QuotationSaleId,
    MasterBomId,
    MasterBomName,
    FeederName,
    Qty,
    Status,
    Level,
    ParentBomId
FROM quotation_sale_boms
WHERE QuotationSaleBomId = <FEEDER_ID_R1>;

-- Expected:
-- Level = 0 (feeder level)
-- ParentBomId = NULL
-- Status = 0 (active)
-- FeederName matches request

-- ============================================
-- S2 QUERIES (After R2 - Re-Apply)
-- ============================================
-- Note: Use same <FEEDER_ID_R1> (feeder should be reused)

-- S2-A: Copy History (Should Have 2 Records Now)
SELECT 
    BomCopyHistoryId,
    SourceType,
    SourceId,
    TargetType,
    TargetId,
    Operation,
    UserId,
    Timestamp
FROM bom_copy_history
WHERE TargetId = <FEEDER_ID_R1>
ORDER BY BomCopyHistoryId DESC
LIMIT 5;

-- Expected: 2 rows (R1 and R2 operations)

-- S2-B: No Illegal "Link-Copy" (Still Must Be 0)
SELECT 
    BomCopyHistoryId,
    SourceId,
    TargetId,
    Operation
FROM bom_copy_history
WHERE SourceId = TargetId
LIMIT 10;

-- Expected: 0 rows (copy-never-link pattern maintained)

-- S2-C: Status Distribution (Clear-Before-Copy Evidence)
SELECT Status, COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
GROUP BY Status
ORDER BY Status;

-- Expected:
-- Status=0 → N items (new active items from R2)
-- Status=1 → N items (old items soft-deleted from R1)
-- This proves clear-before-copy worked!

-- S2-D: No Duplicates in Active Set (Still Must Be 0)
SELECT 
    ProductId, 
    MakeId, 
    SeriesId, 
    COUNT(*) AS duplicate_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
  AND Status = 0
GROUP BY ProductId, MakeId, SeriesId
HAVING COUNT(*) > 1;

-- Expected: 0 rows (no duplicates after clear-before-copy)

-- S2-F: Clear-Before-Copy Verification (ID-based timing)
SELECT 
    Status,
    COUNT(*) AS item_count,
    MIN(QuotationSaleBomItemId) AS min_item_id,
    MAX(QuotationSaleBomItemId) AS max_item_id
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
GROUP BY Status
ORDER BY Status;

-- Expected:
-- Status=0: N items (newly created in R2) → higher IDs (max_item_id)
-- Status=1: N items (created in R1, soft-deleted in R2) → lower IDs (min_item_id)
-- Interpretation:
-- Status=1 range should be older IDs (lower min_item_id/max_item_id)
-- Status=0 range should be newer IDs (higher min_item_id/max_item_id)
-- This proves "clear-before-copy then insert" without relying on timestamps

