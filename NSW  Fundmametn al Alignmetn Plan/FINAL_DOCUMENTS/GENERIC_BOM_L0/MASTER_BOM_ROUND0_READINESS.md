# Master BOM — Round-0 Readiness (Cumulative Governance)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md  
**Version:** v1.0_20251218  
**Date (IST):** 2025-12-18  
**Status:** ⏳ **EVIDENCE-BASED (DB-PENDING)**

## ✅ Standard Remark: Evidence-Based Review (DB Pending)

**Remark (Scope & Evidence Tier):**  
This Master BOM review is executed using the authoritative Master BOM design pack (Index/Plan + Parts 1–11) and code references where available. The design pack is now **imported/registered into this repo workspace for evidence-path referencing** (see `docs/MASTER_BOM/DESIGN/`), therefore Design Evidence is marked **VERIFIED**. Live database verification is not available as of **2025-12-18**, therefore all data-integrity outcomes that require runtime/DB proof are marked **DB-PENDING** and must be validated before any “final freeze” is treated as production-confirmed.

**Reminder (Mandatory DB Verification Later):**  
Before final acceptance / production freeze, execute the DB Verification Pack below and update this document’s status from **DB-PENDING → VERIFIED** (DB axis).

### 🔍 DB Verification Pack (Run Later) + Remedies

#### A) Schema & Keys (must match design)
- **Checks**
  - Confirm tables exist: `master_boms`, `master_bom_items`
  - Confirm keys/columns: `MasterBomId`, `MasterBomItemId`, `ProductId`, `Quantity`, `Status`, timestamps
  - Confirm FK integrity (or explicit documented reason if FK not present)
- **SQL (example)**

```sql
SHOW CREATE TABLE master_boms;
SHOW CREATE TABLE master_bom_items;
```

- **Remedies**
  - If missing columns/keys: add migration (planned unless corrupting)
  - If FK missing and causing orphans: add FK OR add scheduled integrity job (priority based on impact)

#### B) Resolution enforcement (CRITICAL rule)
- **Checks**
  - Verify `ResolutionStatus` in Master BOM items is only L0/L1 (no L2)
  - Verify `ProductId` remains NULL for Master BOM items where `ResolutionStatus` is L0/L1 (B4 invariant)
- **SQL (example)**

```sql
-- Any L2 resolution in Master BOM is a CRITICAL violation (must be 0 rows)
SELECT i.MasterBomItemId, i.MasterBomId, i.ResolutionStatus, i.ProductId
FROM master_bom_items i
WHERE i.Status = 0
  AND i.ResolutionStatus = 'L2';

-- For L0/L1 Master BOM items, ProductId must remain NULL (B4 invariant; must be 0 rows)
SELECT i.MasterBomItemId, i.MasterBomId, i.ResolutionStatus, i.ProductId
FROM master_bom_items i
WHERE i.Status = 0
  AND i.ResolutionStatus IN ('L0','L1')
  AND i.ProductId IS NOT NULL;
```

- **Remedies**
  - If any rows found: CRITICAL data integrity — quarantine/fix data + enforce hard guards in service validation (Immediate)

#### C) Copy-Never-Link Independence (CRITICAL rule)
- **Checks**
  - Ensure quotation/proposal BOM items are independent copies (Master BOM edits must not change existing quotation BOM rows)
- **Test**
  - Create Master BOM → copy to quotation → edit Master BOM → confirm quotation BOM unchanged
- **Remedies**
  - If linkage exists: CRITICAL logic defect — patch copy implementation immediately (Immediate)

#### D) Soft Delete (Archival)
- **Checks**
  - Deletes set `Status=1` (no hard deletes)
  - Ensure delete doesn’t cascade into quotation/proposal BOM
- **SQL**
  - Sample verify soft delete behavior on known IDs
- **Remedies**
  - If hard deletes exist: convert to soft-delete or enforce archival policy in service layer

#### E) Pricing/SKU Non-Leakage at Master BOM stage
- **Checks**
  - Master BOM stage must not join price/SKU tables
  - Proposal stage may resolve pricing after Make/Series selection
- **Remedies**
  - If price leaks into Master BOM: treat as governance violation (Planned unless totals are corrupted)

### ✅ Status Usage Rule (for now)
- **Design evidence**: PASS / PASS WITH NOTES / FAIL
- **DB evidence**: DB-PENDING until verified

### How to apply this immediately (all Master BOM outputs)
- In Round-0 Readiness: add “DB-PENDING verification required” note
- In Round-1 Review: add a “DB Evidence: DB-PENDING” column
- In Gap Register: create a section “DB-PENDING verification items” (not counted as FAIL)
- In Correction Plan: add Batch “DB Verification + Remedies” after DB access is available

### Status wording (when DB is the only missing evidence)
If DB evidence is not available, but design/code evidence is complete, use:
**Status: ⏳ EVIDENCE-BASED (DB-PENDING)**

---

## 1) Executive Status

Round-0 readiness for **Master BOM** is recorded as **evidence-based** with explicit evidence-axis constraints (Design import + DB availability). This avoids mislabeling “missing” when artifacts exist authoritatively but are not yet registered in this repo for traceable referencing.

Code evidence remains **NOT VERIFIED** in this workspace; code verification is tracked separately in **MB-GAP-003/004**.

| Axis | Status | Meaning |
|---|---|---|
| Design Evidence | VERIFIED | Design pack is registered in this repo workspace for evidence-path referencing |
| Code Evidence | NOT VERIFIED | Laravel/code repo is not present in this workspace (no code-path evidence) |
| DB Evidence | DB-PENDING | No DB access available today; runtime data integrity proof pending |

**Stop Condition (Repo-verified execution):** Do not mark Round‑1 as **repo‑verified** until Design Evidence is imported/registered and DB verification is completed where required.

---

## 2) Readiness Checklist (ALL must be TRUE)

| Check | Required | Result | Evidence |
|---|---:|---|---|
| Generic Item Master is **FROZEN** | YES | ✅ PASS | Evidence: `GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md:L1–L16` |
| Specific Item Master is **Reviewed + plan recorded** | YES | ✅ PASS | Evidence: `docs/SPECIFIC_ITEM_MASTER/PLAN/SPECIFIC_ITEM_MASTER_DETAILED_DESIGN.md:L1–L6` |
| NEPL archival standard exists | YES | ✅ PASS | Evidence: `NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md:L1–L6` |
| EX-SUBCAT-001 is active | YES | ✅ PASS | Evidence: `GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md:L20–L27`, `GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_FINAL_v1.0_20251218.md:L53–L60` |
| Master BOM Parts 1–11 + Index + Plan exist | YES | ✅ PASS | Evidence: `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_INDEX.md` + `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PLAN.md` + Parts 1–11 (see §3) |

---

## 3) Workspace Preconditions Scan (Master BOM Design Artifacts)

### 3.1 Required files (must exist)

- `MASTER_BOM_BACKEND_DESIGN_INDEX.md`
- `MASTER_BOM_BACKEND_DESIGN_PLAN.md`
- `MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md`
- `MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md`
- `MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md`
- `MASTER_BOM_BACKEND_DESIGN_PART6_SERVICES.md`
- `MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md`
- `MASTER_BOM_BACKEND_DESIGN_PART8_OPERATIONS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART9_LOGIC.md`
- `MASTER_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART11_CODEBASE.md`

### 3.2 Scan result (this workspace)

**Design Evidence Status:** VERIFIED  
Master BOM design artifacts (Index/Plan + Parts 1–11) are now imported into this repo workspace for evidence-path referencing under `docs/MASTER_BOM/DESIGN/`.

**Repo import list (required for repo-level trace):**
- `MASTER_BOM_BACKEND_DESIGN_INDEX.md`
- `MASTER_BOM_BACKEND_DESIGN_PLAN.md`
- `MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md`
- `MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md`
- `MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md`
- `MASTER_BOM_BACKEND_DESIGN_PART6_SERVICES.md`
- `MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md`
- `MASTER_BOM_BACKEND_DESIGN_PART8_OPERATIONS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART9_LOGIC.md`
- `MASTER_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md`
- `MASTER_BOM_BACKEND_DESIGN_PART11_CODEBASE.md`

---

## 4) Action Required to Move Remaining IMPORT-PENDING → VERIFIED

1) ✅ Imported/registered the Master BOM design artifacts (Index/Plan + Parts 1–11) into this repo/workspace so evidence-path references are resolvable (see `docs/MASTER_BOM/DESIGN/`).
2) Import/register the Specific Item Master “plan recorded” artifact into this repo/workspace (implementation can be deferred; the governance dependency is “plan recorded”).

Once unblocked, proceed to create:
- `MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md`
- `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md`
- `MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md`

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | Updated to 2-axis evidence model; Design Evidence set to IMPORT-PENDING (pack exists externally, pending repo registration) and DB set to DB-PENDING |
| v1.0_20251218 | 2025-12-18 | Imported/registered Master BOM design pack under `docs/MASTER_BOM/DESIGN/`; Design Evidence set to VERIFIED (DB remains DB-PENDING) |



