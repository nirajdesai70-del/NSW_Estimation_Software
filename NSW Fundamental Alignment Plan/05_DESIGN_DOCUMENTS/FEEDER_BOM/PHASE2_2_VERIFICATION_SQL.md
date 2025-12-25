# Phase-2.2 Verification SQL — R1/S1/R2/S2 Evidence

**Status:** 🚀 **EXECUTION PLAN** (Phase-2.2)  
**Date:** 2025-12-20  
**Purpose:** Execute R1/S1/R2/S2 sequence and capture SQL evidence for Phase-2 PASS

---

## 🎯 Objective

Prove feeder apply is idempotent with clear-before-copy:
- R1: First apply creates feeder + items
- S1: Verify no duplicates in active set
- R2: Re-apply reuses feeder + clears before copy
- S2: Verify old items soft-deleted, new items active, no duplicates

---

## 📋 Prerequisites

- ✅ Gate 1: Migration executed (`bom_copy_history` table exists)
- ✅ Gate 2: Feeder endpoint wired to BomEngine::copyFeederTree()
- ✅ Planning DB accessible
- ✅ Test fixture IDs ready (QID, PID, TID, FNAME)

---

## 🔍 Step 1: Get Test Fixtures

**Run these queries to get test IDs:**

```sql
-- Get QuotationId (QID)
SELECT QuotationId, QuotationName
FROM quotations
WHERE Status = 0
LIMIT 1;

-- Get PanelId (PID) for the quotation
SELECT QuotationSaleBomId AS PanelId, QuotationId, QuotationSaleId, MasterBomName
FROM quotation_sale_boms
WHERE QuotationId = <QID>
  AND Level = -1  -- Panel level
  AND Status = 0
LIMIT 1;

-- Get MasterBomId (TID) for feeder template
SELECT MasterBomId, MasterBomName
FROM master_boms
WHERE Status = 0
LIMIT 1;

-- Count template items (N)
SELECT COUNT(*) AS item_count
FROM master_bom_items
WHERE MasterBomId = <TID>;
```

**Record:**
- QID = `<QuotationId>`
- PID = `<PanelId>`
- TID = `<MasterBomId>`
- FNAME = `"Test Feeder"` (or any name)
- N = `<item_count>`

---

## 🚀 Step 2: Execute R1 (Apply #1)

**Request:**
```bash
POST /quotation/{QID}/panel/{PID}/feeder/apply-template
Content-Type: application/json

{
  "MasterBomId": <TID>,
  "FeederName": "<FNAME>",
  "Qty": 1
}
```

**Record from response:**
- `feeder_id` → **FEEDER_ID_R1**
- `inserted_count` → **INSERTED_COUNT_R1** (should = N)
- `feeder_reused` → **FEEDER_REUSED_R1** (should be false)
- `deleted_count` → **DELETED_COUNT_R1** (should be 0)

---

## 📊 Step 3: Snapshot S1 (After R1)

**Run these queries and capture output:**

### Query A: Copy History Written

```sql
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
```

**Expected:** 1 row with Operation = 'COPY_FEEDER_TREE'

---

### Query B: No Illegal "Link-Copy"

```sql
SELECT 
    BomCopyHistoryId,
    SourceId,
    TargetId,
    Operation
FROM bom_copy_history
WHERE SourceId = TargetId
LIMIT 10;
```

**Expected:** 0 rows (must be empty)

---

### Query C: Status Distribution (Active Items Only)

```sql
SELECT Status, COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
GROUP BY Status
ORDER BY Status;
```

**Expected:**
- Status=0 → N (active items)
- Status=1 → 0 (no deleted items yet)

---

### Query D: No Duplicates in Active Set

```sql
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
```

**Expected:** 0 rows (must be empty)

---

### Query E: Feeder Row Inspection

```sql
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
```

**Expected:**
- Level = 0 (feeder level)
- ParentBomId = NULL
- Status = 0 (active)
- FeederName = "<FNAME>"

---

## 🚀 Step 4: Execute R2 (Apply #2 - Same Request)

**Request:** (identical to R1)
```bash
POST /quotation/{QID}/panel/{PID}/feeder/apply-template
Content-Type: application/json

{
  "MasterBomId": <TID>,
  "FeederName": "<FNAME>",
  "Qty": 1
}
```

**Record from response:**
- `feeder_id` → **FEEDER_ID_R2** (should = FEEDER_ID_R1)
- `inserted_count` → **INSERTED_COUNT_R2** (should = N)
- `feeder_reused` → **FEEDER_REUSED_R2** (should be true)
- `deleted_count` → **DELETED_COUNT_R2** (should > 0, ideally = N)

**STOP if:**
- ❌ `feeder_id` changed (feeder not reused)
- ❌ `deleted_count` = 0 (clear-before-copy didn't work)
- ❌ `feeder_reused` = false (reuse detection failed)

---

## 📊 Step 5: Snapshot S2 (After R2)

**Run the same queries as S1 and capture output:**

### Query A: Copy History (Should Have 2 Records Now)

```sql
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
```

**Expected:** 2 rows (R1 and R2 operations)

---

### Query B: No Illegal "Link-Copy" (Still Must Be 0)

```sql
SELECT 
    BomCopyHistoryId,
    SourceId,
    TargetId,
    Operation
FROM bom_copy_history
WHERE SourceId = TargetId
LIMIT 10;
```

**Expected:** 0 rows (must be empty)

---

### Query C: Status Distribution (Clear-Before-Copy Evidence)

```sql
SELECT Status, COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
GROUP BY Status
ORDER BY Status;
```

**Expected:**
- Status=0 → N (new active items)
- Status=1 → N (old items soft-deleted)

**This proves clear-before-copy worked!**

---

### Query D: No Duplicates in Active Set (Still Must Be 0)

```sql
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
```

**Expected:** 0 rows (must be empty)

---

### Query F: Clear-Before-Copy Verification (Detailed)

```sql
-- Count items by status and creation time
SELECT 
    Status,
    COUNT(*) AS item_count,
    MIN(CreatedAt) AS first_created,
    MAX(CreatedAt) AS last_created
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = <FEEDER_ID_R1>
GROUP BY Status
ORDER BY Status;
```

**Expected:**
- Status=0: N items (newly created in R2)
- Status=1: N items (created in R1, soft-deleted in R2)

---

## ✅ PASS Criteria

**All of these must be true:**

### R1 Criteria
- ✅ `inserted_count == N`
- ✅ `feeder_reused == false`
- ✅ `deleted_count == 0`

### R2 Criteria
- ✅ `feeder_id == FEEDER_ID_R1` (same feeder reused)
- ✅ `feeder_reused == true`
- ✅ `deleted_count > 0` (ideally = N)
- ✅ `inserted_count == N`

### S1 Criteria
- ✅ Query D: 0 rows (no duplicates)
- ✅ Query C: Status=0 → N, Status=1 → 0

### S2 Criteria
- ✅ Query D: 0 rows (no duplicates)
- ✅ Query C: Status=0 → N, Status=1 → N (clear-before-copy worked)
- ✅ Query B: 0 rows (no illegal link-copy)
- ✅ Query A: 2 rows (both R1 and R2 recorded in history)

---

## 📝 Evidence Capture

**Save all SQL outputs to:**
- `evidence/PHASE2/S1_queries_output.txt`
- `evidence/PHASE2/S2_queries_output.txt`
- `evidence/PHASE2/R1_response.json`
- `evidence/PHASE2/R2_response.json`

**Format:**
```
=== R1 Response ===
{JSON response}

=== S1 Queries ===
Query A: [output]
Query B: [output]
Query C: [output]
Query D: [output]
Query E: [output]

=== R2 Response ===
{JSON response}

=== S2 Queries ===
Query A: [output]
Query B: [output]
Query C: [output]
Query D: [output]
Query F: [output]
```

---

## 🔗 Related Files

- `PLANNING/VERIFICATION/PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md` — Full execution guide
- `PLANNING/VERIFICATION/PB_GAP_004_VERIFICATION_QUERIES.sql` — Query templates
- `PLANNING/CLOSURE/PB_GAP_004_CLOSURE_PACK_P6.md` — Closure template

---

## ✅ Completion Checklist

- [ ] Test fixtures obtained (QID, PID, TID, FNAME, N)
- [ ] R1 executed and response recorded
- [ ] S1 queries executed and outputs captured
- [ ] R2 executed and response recorded
- [ ] S2 queries executed and outputs captured
- [ ] All PASS criteria verified
- [ ] Evidence files saved to `evidence/PHASE2/`
- [ ] Phase-2 PASS declared

**After completion:** Update gap register and declare Phase-2 PASS

