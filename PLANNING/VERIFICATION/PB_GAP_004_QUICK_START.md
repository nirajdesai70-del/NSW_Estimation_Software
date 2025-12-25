# PB-GAP-004 — Quick Start (P3/P5 Verification)

**Status:** 🟡 PLANNING MODE - Ready for Phase 5 Execution (DB PENDING)  
**Mode:** Planning Only - No DB Access Available  
**Phase A:** Verification contract locked (COMPLETE)  
**Phase B:** Execution deferred until DB access available (INTENTIONAL HOLD)

**⚠️ PLANNING MODE:** This verification plan is documented and ready but **cannot be executed** until Phase 5 begins with DB access. See `../TRANSITION_PLAN.md` for execution procedures.

---

## Goal
Verify PB-GAP-004 passes:
- applyFeederTemplate() is idempotent
- clear-before-copy works (Status 0→1)
- no duplicates in active set (A4 empty)

## Preconditions
- Planning DB only (NOT production)
- You have QID, PID, TID, FNAME, QTY
- Template has items: N > 0

---

## Step A — Pick fixture
Record:
- QID  (QuotationId)
- PID  (QuotationSaleId / panel)
- TID  (MasterBomId / template)
- FNAME (FeederName label used consistently)
- QTY  (e.g. 1)

---

## Step B — Confirm template item count (N)
Run:
SELECT COUNT(*) AS item_count
FROM master_bom_items
WHERE MasterBomId = <TID>;

Record N.

STOP if N = 0.

---

## Step C — Apply #1 (R1)
POST /quotation/{QID}/panel/{PID}/feeder/apply-template
Body:
{
  "MasterBomId": TID,
  "FeederName": "FNAME",
  "Qty": QTY
}

Record:
- FEEDER_ID (from response)
- inserted_count (should = N)
- feeder_reused (should be false if clean)

---

## Step D — Snapshot #1 (S1)
A3:
SELECT Status, COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID>
GROUP BY Status
ORDER BY Status;

A4:
SELECT ProductId, MakeId, SeriesId, COUNT(*) AS duplicate_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID>
  AND Status = 0
GROUP BY ProductId, MakeId, SeriesId
HAVING COUNT(*) > 1;

Expect:
- A3: Status=0 => N
- A4: 0 rows

STOP if A4 has rows.

---

## Step E — Apply #2 (R2) (same identity tuple)
Same POST again with same QID/PID/TID/FNAME.

Expect:
- feeder_id unchanged (same as R1)
- feeder_reused = true
- deleted_count > 0 (ideally = N)
- inserted_count = N

STOP if feeder_id changes or deleted_count = 0.

---

## Step F — Snapshot #2 (S2)
Run A3 & A4 again.

Expect:
- A3: Status=0 => N, Status=1 => N
- A4: 0 rows

---

## PASS condition
PASS only if:
- feeder_id stable across R1/R2
- clear-before-copy happened (Status=1 grows)
- no duplicates in Status=0 (A4 empty)
- inserted_count == N on both applies



