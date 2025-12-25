-- Phase-3: Restore Replay Verification (planning)
-- Goal: prove replay reconstructs state.

-- ============================================================================
-- STATE RECONSTRUCTION EXPECTATIONS
-- ============================================================================
--
-- What a reconstructed node state must contain:
--   - ParentBomId: Parent node reference (NULL for root nodes)
--   - Level: Hierarchy depth (0 = root)
--   - FeederName/BomName: Node name fields (may differ by node type)
--   - Qty: Quantity value
--   - Status: Node status (e.g., ACTIVE, DEACTIVATED)
--
-- Replay ordering (critical for correct state reconstruction):
--   1. Timestamp ASC (chronological order of events)
--   2. BomNodeHistoryId ASC (tie-breaker for events with identical timestamps)
--
-- Fail-fast rules (must be validated during replay):
--   - Node missing: Target node (QuotationSaleBomId) does not exist → FAIL
--   - Timestamp invalid: Restore timestamp is before first event or in future → FAIL
--   - Circular dependency: Parent chain creates a cycle → FAIL
--
-- ============================================================================

-- B1) Fetch events up to a timestamp (node)
SELECT BomNodeHistoryId, EventType, Timestamp, BeforeState, AfterState, ChangedFields
FROM quotation_sale_bom_node_history
WHERE QuotationId = <QID>
  AND QuotationSaleBomId = <NODE_ID>
  AND Timestamp <= <TS_RESTORE>
ORDER BY Timestamp ASC, BomNodeHistoryId ASC;

-- B2) Fetch current node row for comparison (runtime window later)
SELECT QuotationSaleBomId, QuotationId, QuotationSaleId, ParentBomId, Level, FeederName, BomName, Qty, Status
FROM quotation_sale_boms
WHERE QuotationSaleBomId = <NODE_ID>;
