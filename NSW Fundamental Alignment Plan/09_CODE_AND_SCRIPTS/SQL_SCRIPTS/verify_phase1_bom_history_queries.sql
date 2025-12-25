-- Verification Queries: Phase-1 BOM History Implementation
-- Purpose: SQL queries to verify history recording is working correctly
-- Reference: BOM_ENGINE_IMPLEMENTATION_PLAN.md (Phase-1 STOP Gate)
-- Phase: Phase-1 (P0) - Line Item Edit + History Foundation
--
-- Usage:
--   1. Run these queries after executing BOM operations
--   2. Verify that history records are created correctly
--   3. Verify that snapshots contain complete state
--   4. Verify that changed fields are tracked correctly

-- ============================================
-- 1. Verify History Table Exists
-- ============================================
DESCRIBE quotation_sale_bom_item_history;
-- Expected: Columns: id, quotation_sale_bom_item_id, operation, before_snapshot, after_snapshot, changed_fields, user_id, timestamp, parent_reference

-- ============================================
-- 2. Count History Records by Operation
-- ============================================
SELECT 
    operation,
    COUNT(*) as count,
    MIN(timestamp) as first_record,
    MAX(timestamp) as last_record
FROM quotation_sale_bom_item_history
GROUP BY operation
ORDER BY operation;
-- Expected: Should show CREATE, UPDATE, DELETE, REPLACE operations

-- ============================================
-- 3. Verify History Records for Specific Item
-- ============================================
-- Replace :item_id with actual QuotationSaleBomItemId
SELECT 
    id,
    operation,
    timestamp,
    user_id,
    JSON_LENGTH(changed_fields) as num_changed_fields,
    JSON_EXTRACT(before_snapshot, '$.Qty') as before_qty,
    JSON_EXTRACT(after_snapshot, '$.Qty') as after_qty,
    JSON_EXTRACT(before_snapshot, '$.ProductId') as before_product_id,
    JSON_EXTRACT(after_snapshot, '$.ProductId') as after_product_id
FROM quotation_sale_bom_item_history
WHERE quotation_sale_bom_item_id = :item_id
ORDER BY timestamp DESC;
-- Expected: Should show all history records for the item, ordered by most recent first

-- ============================================
-- 4. Verify Complete Snapshots (Before/After)
-- ============================================
-- Replace :history_id with actual history record ID
SELECT 
    id,
    operation,
    before_snapshot,
    after_snapshot,
    changed_fields
FROM quotation_sale_bom_item_history
WHERE id = :history_id;
-- Expected: 
--   - before_snapshot should contain complete item state (all fields)
--   - after_snapshot should contain complete item state (all fields)
--   - changed_fields should list only fields that actually changed

-- ============================================
-- 5. Verify UPDATE Operation Captures Changes
-- ============================================
SELECT 
    h.id,
    h.operation,
    h.timestamp,
    h.changed_fields,
    JSON_EXTRACT(h.before_snapshot, '$.Qty') as before_qty,
    JSON_EXTRACT(h.after_snapshot, '$.Qty') as after_qty,
    i.Qty as current_qty
FROM quotation_sale_bom_item_history h
JOIN quotation_sale_bom_items i ON h.quotation_sale_bom_item_id = i.QuotationSaleBomItemId
WHERE h.operation = 'UPDATE'
ORDER BY h.timestamp DESC
LIMIT 10;
-- Expected: 
--   - after_qty should match current_qty (if no further updates)
--   - changed_fields should include 'quantity' if quantity changed

-- ============================================
-- 6. Verify CREATE Operation Has After Snapshot
-- ============================================
SELECT 
    id,
    operation,
    quotation_sale_bom_item_id,
    before_snapshot,
    after_snapshot,
    timestamp
FROM quotation_sale_bom_item_history
WHERE operation = 'CREATE'
ORDER BY timestamp DESC
LIMIT 10;
-- Expected:
--   - before_snapshot should be NULL (no before state for CREATE)
--   - after_snapshot should contain complete item state
--   - changed_fields should list all initial fields

-- ============================================
-- 7. Verify DELETE Operation Has Before Snapshot
-- ============================================
SELECT 
    id,
    operation,
    quotation_sale_bom_item_id,
    before_snapshot,
    after_snapshot,
    JSON_EXTRACT(before_snapshot, '$.Status') as before_status,
    JSON_EXTRACT(after_snapshot, '$.Status') as after_status
FROM quotation_sale_bom_item_history
WHERE operation = 'DELETE'
ORDER BY timestamp DESC
LIMIT 10;
-- Expected:
--   - before_snapshot should contain complete item state (status = 0)
--   - after_snapshot should show status = 1 (soft deleted)
--   - changed_fields should include 'status'

-- ============================================
-- 8. Verify User Context is Recorded
-- ============================================
SELECT 
    user_id,
    COUNT(*) as operation_count,
    COUNT(DISTINCT operation) as distinct_operations
FROM quotation_sale_bom_item_history
WHERE user_id IS NOT NULL
GROUP BY user_id
ORDER BY operation_count DESC;
-- Expected: Should show user_id for all operations (if authentication is working)

-- ============================================
-- 9. Verify Parent Reference (for Copied Items)
-- ============================================
SELECT 
    id,
    operation,
    quotation_sale_bom_item_id,
    parent_reference,
    JSON_EXTRACT(parent_reference, '$.copied_from_item_id') as copied_from_item_id,
    JSON_EXTRACT(parent_reference, '$.copied_from_bom_id') as copied_from_bom_id
FROM quotation_sale_bom_item_history
WHERE parent_reference IS NOT NULL
ORDER BY timestamp DESC
LIMIT 10;
-- Expected: Should show parent references for items that were copied (Phase-2 feature)

-- ============================================
-- 10. Verify No Missing History Records
-- ============================================
-- Check if any items were updated without history
SELECT 
    i.QuotationSaleBomItemId,
    i.QuotationSaleBomId,
    i.UpdatedAt,
    COUNT(h.id) as history_count
FROM quotation_sale_bom_items i
LEFT JOIN quotation_sale_bom_item_history h ON i.QuotationSaleBomItemId = h.quotation_sale_bom_item_id
WHERE i.Status = 0  -- Active items only
GROUP BY i.QuotationSaleBomItemId, i.QuotationSaleBomId, i.UpdatedAt
HAVING history_count = 0
ORDER BY i.UpdatedAt DESC
LIMIT 20;
-- Expected: Should return 0 rows (all items should have history if they were created/updated via BomEngine)
-- Note: Items created before Phase-1 may not have history (expected)

-- ============================================
-- 11. Verify Snapshot Completeness
-- ============================================
-- Check that snapshots contain all required fields (NEPL column names)
SELECT 
    id,
    operation,
    JSON_EXTRACT(after_snapshot, '$.QuotationSaleBomItemId') as has_item_id,
    JSON_EXTRACT(after_snapshot, '$.QuotationSaleBomId') as has_bom_id,
    JSON_EXTRACT(after_snapshot, '$.Qty') as has_qty,
    JSON_EXTRACT(after_snapshot, '$.ProductId') as has_product_id,
    JSON_EXTRACT(after_snapshot, '$.Status') as has_status
FROM quotation_sale_bom_item_history
WHERE after_snapshot IS NOT NULL
ORDER BY timestamp DESC
LIMIT 10;
-- Expected: All fields should be non-NULL (snapshots should be complete)

-- ============================================
-- 12. Test Restore Capability (Manual)
-- ============================================
-- To restore an item to a previous state:
-- 1. Find the history record with desired state
-- 2. Extract the after_snapshot (or before_snapshot for DELETE)
-- 3. Update the item with values from snapshot
-- 4. Create a new history record for the restore operation
--
-- Example (pseudocode):
-- SELECT after_snapshot FROM quotation_sale_bom_item_history WHERE id = :history_id;
-- -- Then use the snapshot to restore the item

-- ============================================
-- Verification Checklist
-- ============================================
-- Use this checklist to verify Phase-1 completion:
--
-- [ ] History table exists with correct schema
-- [ ] History records are created for CREATE operations
-- [ ] History records are created for UPDATE operations
-- [ ] History records are created for DELETE operations
-- [ ] History records are created for REPLACE operations
-- [ ] Before snapshots are captured (for UPDATE/DELETE/REPLACE)
-- [ ] After snapshots are captured (for CREATE/UPDATE/REPLACE)
-- [ ] Changed fields are tracked correctly
-- [ ] User context is recorded
-- [ ] Timestamps are accurate
-- [ ] Snapshots contain complete state (all NEPL column names: QuotationSaleBomItemId, Qty, ProductId, Status, etc.)
-- [ ] No items are updated without history (after Phase-1 integration)
-- [ ] All column names in snapshots use NEPL PascalCase (QuotationSaleBomItemId, Qty, Status, not id, quantity, status)

