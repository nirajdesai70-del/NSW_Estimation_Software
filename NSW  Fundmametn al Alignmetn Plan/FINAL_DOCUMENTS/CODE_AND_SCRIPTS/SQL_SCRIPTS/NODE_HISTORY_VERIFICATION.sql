-- Phase-3: Node History Verification (planning)
-- Replace <QID>, <NODE_ID>, <TS_START>, <TS_END>

-- A1) Ensure table exists
SHOW TABLES LIKE 'quotation_sale_bom_node_history';

-- A2) Recent events for a node
SELECT BomNodeHistoryId, QuotationId, QuotationSaleBomId, EventType, UserId, Timestamp
FROM quotation_sale_bom_node_history
WHERE QuotationId = <QID>
  AND QuotationSaleBomId = <NODE_ID>
ORDER BY BomNodeHistoryId DESC
LIMIT 20;

-- A3) Verify append-only (no updates is application rule)
-- Check for monotonic ids over time
SELECT COUNT(*) AS cnt, MIN(BomNodeHistoryId) AS min_id, MAX(BomNodeHistoryId) AS max_id
FROM quotation_sale_bom_node_history
WHERE QuotationId = <QID>
  AND Timestamp BETWEEN <TS_START> AND <TS_END>;

-- A4) Verify required fields not null (basic integrity)
SELECT COUNT(*) AS bad_rows
FROM quotation_sale_bom_node_history
WHERE QuotationId = <QID>
  AND (EventType IS NULL OR Timestamp IS NULL OR QuotationSaleBomId IS NULL);

-- A5) Verify event type domain
SELECT EventType, COUNT(*) AS cnt
FROM quotation_sale_bom_node_history
WHERE QuotationId = <QID>
GROUP BY EventType;
