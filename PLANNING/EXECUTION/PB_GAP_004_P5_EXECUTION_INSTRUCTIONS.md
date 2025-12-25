# PB-GAP-004 — P5 Execution Instructions

**Status:** 🟡 PLANNING MODE - Ready for Phase 5 Execution (DB PENDING)  
**Mode:** Planning Only - No DB Access Available  
**Phase:** Verification contract locked, awaiting DB run  
**Estimated Time:** 15 minutes when DB access is available

**⚠️ PLANNING MODE:** This test is documented and ready but **cannot be executed** until Phase 5 begins with DB access. See `../TRANSITION_PLAN.md` for execution procedures.

---

## Pre-Execution Checklist

- [ ] Planning DB access available (NOT production)
- [ ] DB client open (MySQL or PostgreSQL)
- [ ] API client ready (Postman/curl/etc)
- [ ] Results template ready: `PB_GAP_004_RESULTS_TEMPLATE.md`

---

## Execution Steps (Sequential)

### Step 1 — Fixture Discovery (3 queries)

**Query A — Pick TID:**
```sql
SELECT 
  mbi.MasterBomId,
  mb.Name AS MasterBomName,
  COUNT(*) AS item_count
FROM master_bom_items mbi
JOIN master_boms mb ON mb.MasterBomId = mbi.MasterBomId
GROUP BY mbi.MasterBomId, mb.Name
HAVING COUNT(*) > 0
ORDER BY item_count DESC
LIMIT 5;

→ Pick highest item_count → TID

Query B — Pick QID:

SELECT 
  QuotationId,
  QuotationNo
FROM quotations
WHERE Status = 0
ORDER BY QuotationId DESC
LIMIT 5;

→ Pick one → QID

Query C — Pick PID (must belong to QID):

SELECT
  qs.QuotationSaleId,
  qs.QuotationId,
  qs.Name,
  qs.SaleCustomName
FROM quotation_sales qs
JOIN quotations q ON q.QuotationId = qs.QuotationId
WHERE q.Status = 0
  AND qs.Status = 0
  AND qs.QuotationId = <YOUR_QID>
ORDER BY qs.QuotationSaleId DESC
LIMIT 5;

→ Pick one where QuotationId matches QID → PID

Declare fixtures:

QID   = [from Query B]
PID   = [from Query C, verified: belongs to QID]
TID   = [from Query A, highest item_count]
FNAME = PB004_FDR_YYYYMMDD_XXX (e.g., PB004_FDR_20251220_001)
QTY   = 1


⸻

Step 2 — Confirm Template Size (N)

SELECT COUNT(*) AS item_count
FROM master_bom_items
WHERE MasterBomId = <TID>;

→ Record N
→ STOP if N = 0

⸻

Step 3 — Apply #1 (R1)

Request:

POST /quotation/{QID}/panel/{PID}/feeder/apply-template
Content-Type: application/json

{
  "MasterBomId": <TID>,
  "FeederName": "<FNAME>",
  "Qty": 1
}

Record from response:
	•	feeder_id → FEEDER_ID
	•	inserted_count (should = N)
	•	feeder_reused (should be false)

⸻

Step 4 — Snapshot S1

Query A3:

SELECT Status, COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID>
GROUP BY Status
ORDER BY Status;

Query A4:

SELECT ProductId, MakeId, SeriesId, COUNT(*) AS duplicate_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID>
  AND Status = 0
GROUP BY ProductId, MakeId, SeriesId
HAVING COUNT(*) > 1;

Expected:
	•	A3: Status=0 → N
	•	A4: 0 rows

→ STOP if A4 has rows

⸻

Step 5 — Apply #2 (R2) — Same Request

Request: (identical to R1)

POST /quotation/{QID}/panel/{PID}/feeder/apply-template
Content-Type: application/json

{
  "MasterBomId": <TID>,
  "FeederName": "<FNAME>",
  "Qty": 1
}

Expected:
	•	feeder_id unchanged (same as R1)
	•	feeder_reused = true
	•	deleted_count > 0 (ideally = N)
	•	inserted_count = N

→ STOP if feeder_id changes or deleted_count = 0

⸻

Step 6 — Snapshot S2

Run A3 & A4 again (same queries as Step 4)

Expected:
	•	A3: Status=0 → N, Status=1 → N
	•	A4: 0 rows

⸻

PASS Criteria

✅ All of these must be true:
	•	R1: inserted_count == N
	•	R2: feeder_id == R1.feeder_id
	•	R2: feeder_reused == true
	•	R2: deleted_count > 0
	•	R2: inserted_count == N
	•	S1: A4 empty (0 rows)
	•	S2: A4 empty (0 rows)
	•	S2: A3 shows Status=1 increased AND Status=0 stable at N

⸻

Results Capture

Fill PB_GAP_004_RESULTS_TEMPLATE.md with:
	•	Fixture values
	•	R1/R2 JSON responses
	•	S1/S2 query outputs
	•	PASS/FAIL verdict

⸻

Troubleshooting

If Step 1 returns 0 rows:
	•	No templates have items → create test template first
	•	No active quotations → verify Status = 0 is correct

If PID doesn't match QID:
	•	Re-run Query C with explicit filter: WHERE qs.QuotationId = <YOUR_QID>

If A4 has rows:
	•	Duplicate detection failed → STOP, investigate root cause

If feeder_id changes on R2:
	•	Idempotency broken → STOP, investigate root cause

⸻

Last Updated: 2025-12-20
Reference: PB_GAP_004_QUICK_START.md (detailed logic)
Reference: PB_GAP_004_FIXTURE_DISCOVERY_QUERIES.md (query variants)



