# Phase-2 Release Pack — Runbook

**Status:** 📋 **PLANNING ARTIFACT** (Deployment-Ready Release Pack)  
**Date:** 2025-12-21  
**Purpose:** Complete execution guide for Phase-2 deployment (Gate-1 → Gate-2 → Gate-3)

**⚠️ PLANNING MODE:** This release pack is in planning mode. Gate statuses reflect readiness, not execution completion. See `STATUS.md` for current gate statuses.

---

## 🎯 Phase-2 Objective

Wire feeder template apply endpoint to `BomEngine::copyFeederTree()` with:
- ✅ Feeder reuse detection (idempotent re-apply)
- ✅ Clear-before-copy semantics (prevents duplicate stacking)
- ✅ Copy history recording (audit trail)
- ✅ Zero direct DB writes from controller (thin controller pattern)

---

## 📦 Release Pack Contents

```
PHASE2/
├─ 00_README_RUNBOOK.md          ← You are here
├─ 01_ARCH_DECISIONS.md          ← Design decisions and rationale
├─ 02_BOM_ENGINE_CONTRACT.md     ← Input/output contract for copyFeederTree()
├─ 03_APPLY_FEEDER_TEMPLATE_IO.json  ← Request/response examples
├─ 04_EXECUTION_SCRIPTS/
│  ├─ apply_feeder_template.sql  ← Read-only verification queries
│  ├─ copy_history.sql            ← History inspection queries
│  └─ rollback.sql                ← Rollback procedure (if needed)
├─ 05_VERIFICATION/
│  ├─ S1_S2_VERIFICATION.sql     ← Gate-3 verification queries
│  └─ SCORECARD.md                ← Pass/fail rubric
├─ 06_RISKS_AND_ROLLBACK.md      ← Risk mitigation and rollback plan
└─ 07_DATA_READINESS/
   ├─ DATA_READINESS_GATE.md      ← Gate-0 template validation guide
   └─ TEMPLATE_SHORTLIST.md       ← Template selection list for Window A
```

---

## 🚪 Gate Sequence

### Gate-0: Data Readiness 📌
**Status:** **MANDATORY** (must pass before R1 execution)

**⚠️ BLOCKING RULE: Gate-0 MUST PASS before R1 can be executed.**

**Purpose:** Ensure selected MasterBomId template has N > 0 items in `master_bom_items` before attempting R1/R2.

**Action:** See `07_DATA_READINESS/DATA_READINESS_GATE.md` for queries and pass criteria.

**PASS Criteria:** Selected MasterBomId has `COUNT(*) > 0` rows in `master_bom_items`.

**Evidence Requirement:** 
- Chosen TEMPLATE_ID must be recorded in evidence header
- Item count (N) must be recorded in evidence header
- Evidence file: `evidence/PHASE2/G0_template_itemcount.txt`

**Execution Blocking:** R1 cannot begin until Gate-0 SQL output is captured and TEMPLATE_ID with N>0 is confirmed.

---

### Gate-1: Migration Execution ✅
**Status:** PASS (Schema verified on staging DB)  
**Evidence:** `evidence/PHASE2/G1_bom_copy_history_schema.txt`

**Action:** Migration already applied. Verify table exists:
```sql
SELECT DATABASE();
SHOW TABLES LIKE 'bom_copy_history';
DESCRIBE bom_copy_history;
```

**PASS Criteria:** Table exists + columns match PascalCase names

---

### Gate-2: Controller Wiring 📌
**Status:** READY (runtime endpoint confirmed; execution window pending)

**Evidence:**
- UI file: `resources/views/quotation/v2/_feeder_library_modal.blade.php:202` (runtime reference)
- Route: `routes/web.php:321` (runtime reference)
- Controller: `app/Http/Controllers/QuotationV2Controller.php:2996` (runtime reference)

**Action:** Controller method exists and wired to `BomEngine::copyFeederTree()` (verified in runtime workspace)

**READY Criteria:** Runtime endpoint confirmed via UI analysis. Execution window required for PASS validation.

---

### Gate-3: Verification (R1 → S1 → R2 → S2) 📌
**Status:** READY (execution window required)

**⚠️ BLOCKING REQUIREMENT:** Gate-0 must PASS before R1 can start. R1 cannot begin until Gate-0 SQL output is captured and TEMPLATE_ID with N>0 is confirmed.

**Test Sequence:**
1. **Gate-0:** Execute template validation SQL → Verify chosen TEMPLATE_ID has N>0 items → Record TEMPLATE_ID + N in evidence header
2. **R1:** Trigger first apply via UI → Capture Response JSON
3. **S1:** Run verification SQL queries → Validate first apply
4. **R2:** Trigger re-apply (same request) → Capture Response JSON
5. **S2:** Run verification SQL queries → Validate re-apply (reuse + clear-before-copy)

**Evidence Files:**
- `evidence/PHASE2/S1_sql_output.txt` (R1 + S1 results)
- `evidence/PHASE2/S2_sql_output.txt` (R2 + S2 results)

**PASS Criteria:** See `05_VERIFICATION/SCORECARD.md`

---

## 📋 Execution Checklist

### Pre-Deployment
- [ ] Review `01_ARCH_DECISIONS.md` (understand design rationale)
- [ ] Review `02_BOM_ENGINE_CONTRACT.md` (understand I/O contract)
- [ ] Review `06_RISKS_AND_ROLLBACK.md` (understand rollback procedure)
- [ ] **Gate-0 (Data Readiness) — MANDATORY before R1:** Verify template item count > 0 (see `07_DATA_READINESS/DATA_READINESS_GATE.md`)
  - [ ] Run Gate-0 SQL queries to find usable templates
  - [ ] Pick a MasterBomId with N > 0 items
  - [ ] **Chosen TEMPLATE_ID must be recorded in evidence header.**
  - [ ] Record chosen `<TEMPLATE_ID>` and N in evidence header
  - [ ] **R1 cannot start until Gate-0 SQL output is captured and TEMPLATE_ID confirmed with N>0**
- [ ] Verify Gate-1 PASS (migration applied)
- [ ] Verify Gate-2 READY (runtime endpoint confirmed)

### Deployment Window
- [ ] **Gate-1:** Verify `bom_copy_history` table exists (if not already done)
- [ ] **Gate-2:** Verify controller method exists (runtime endpoint confirmed via UI analysis)
- [ ] **Gate-3:** Execute R1 → S1 → R2 → S2 sequence
  - [ ] Trigger R1 via UI (Feeder Library modal → Apply Template)
  - [ ] Capture R1 Response JSON
  - [ ] Run S1 queries (replace `<FEEDER_ID_R1>` with actual value)
  - [ ] Populate `evidence/PHASE2/S1_sql_output.txt`
  - [ ] Trigger R2 via UI (same request as R1)
  - [ ] Capture R2 Response JSON
  - [ ] Run S2 queries (use same `FEEDER_ID_R1`)
  - [ ] Populate `evidence/PHASE2/S2_sql_output.txt`
- [ ] Validate S1 PASS criteria (see scorecard)
- [ ] Validate S2 PASS criteria (see scorecard)

### Post-Deployment
- [ ] Declare Gate-3 PASS if all criteria met
- [ ] Declare Phase-2 PASS
- [ ] Update gap register (BOM-GAP-001, BOM-GAP-002 closure)

---

## 🔍 Verification Quick Reference

### R1 Response (First Apply)
```json
{
  "success": true,
  "message": "Feeder template applied successfully",
  "data": {
    "feeder_id": <FEEDER_ID_R1>,
    "feeder_reused": false,
    "deleted_count": 0,
    "inserted_count": <N>,
    "copy_history_id": <history_id>
  }
}
```

### R2 Response (Re-Apply)
```json
{
  "success": true,
  "message": "Feeder template applied successfully",
  "data": {
    "feeder_id": <FEEDER_ID_R2>,  // Should equal FEEDER_ID_R1
    "feeder_reused": true,          // Should be true
    "deleted_count": <N>,          // Should equal N
    "inserted_count": <N>,         // Should equal N
    "copy_history_id": <history_id>
  }
}
```

### S1 Critical Checks
- ✅ Copy history row exists (`Operation = 'COPY_FEEDER_TREE'`)
- ✅ No illegal link-copy (`SourceId != TargetId`)
- ✅ Status=0 → N items, Status=1 → 0 items
- ✅ No duplicates in active set

### S2 Critical Checks
- ✅ Copy history has 2 rows (R1 + R2)
- ✅ `feeder_id` unchanged (reuse verified)
- ✅ `feeder_reused = true`
- ✅ Status=0 → N items, Status=1 → N items (clear-before-copy verified)
- ✅ Status=0 IDs > Status=1 IDs (ID-based timing proof)

---

## 📚 Related Documents

- **Architecture:** `01_ARCH_DECISIONS.md`
- **Contract:** `02_BOM_ENGINE_CONTRACT.md`
- **I/O Examples:** `03_APPLY_FEEDER_TEMPLATE_IO.json`
- **Data Readiness:** `07_DATA_READINESS/DATA_READINESS_GATE.md` (Gate-0)
- **Verification:** `05_VERIFICATION/SCORECARD.md`
- **Rollback:** `06_RISKS_AND_ROLLBACK.md`
- **Controller Patch:** `PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`
- **Execution Status:** `PHASE2_EXECUTION_STATUS.md`

---

## ⚠️ Critical Rules

### Thin Controller Contract (LOCKED)

**Controller MUST:**
- Validate input parameters (MasterBomId, FeederName, Qty)
- Call `BomEngine::copyFeederTree()` with validated parameters
- Return JSON response with evidence fields: `feeder_id`, `feeder_reused`, `deleted_count`, `inserted_count`, `copy_history_id`

**Controller MUST NOT:**
- Create BOM rows directly (`QuotationSaleBom::create()`)
- Create item rows directly (`QuotationSaleBomItem::create()`)
- Clear data directly (direct Status updates to items)
- Record history directly (direct `bom_copy_history` inserts)
- Execute business logic (feeder detection, reuse logic, copy logic, clear-before-copy logic)

### General Rules

1. **No Direct DB Writes:** Controller must NOT write directly to `quotation_sale_boms` or `quotation_sale_bom_items`
2. **Engine-Only Writes:** All BOM operations go through `BomEngine`
3. **Thin Controller:** Controller validates input, calls engine, returns response
4. **History Automatic:** BomEngine automatically records copy history via `BomHistoryService::recordCopyHistory()`
5. **Idempotent Re-Apply:** Re-applying same template reuses existing feeder and clears before copy

---

## 🎯 Success Criteria

**Phase-2 PASS when:**
- ✅ Gate-0 PASS (template data readiness verified)
- ✅ Gate-1 PASS (migration applied)
- ✅ Gate-2 PASS (controller wired + execution window validated)
- ✅ Gate-3 PASS (R1/S1/R2/S2 verified)

**Gap Closure:**
- ✅ BOM-GAP-001: Feeder reuse detection implemented
- ✅ BOM-GAP-002: Clear-before-copy implemented
- ✅ BOM-GAP-007: Copy history recording implemented

---

**END OF RUNBOOK**

