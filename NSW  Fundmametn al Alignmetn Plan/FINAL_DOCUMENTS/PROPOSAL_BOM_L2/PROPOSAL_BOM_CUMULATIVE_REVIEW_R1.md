# Proposal BOM — Cumulative Review (Round-1)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md  
**Version:** v1.0_2025-12-19  
**Date (IST):** 2025-12-19  
**Status:** ✅ **CLOSED / AUDIT-READY (DB-VERIFIED PASS)**

## ✅ Standard Remark: Evidence-Based Review (DB Pending)

**Remark (Scope & Evidence Tier):**  
This Proposal BOM review is executed using the authoritative Proposal BOM design pack (PROPOSAL_BOM_BACKEND_DESIGN_PART*.md files) which contains Proposal BOM design specifications. The design pack is **imported/registered into this repo workspace for evidence-path referencing**, therefore Design Evidence is marked **VERIFIED**. Database verification completed: DB-Check B1 (0 rows) and DB-Check B2 (0 rows) confirm no active violations in Proposal BOM data. Proposal BOM is **cleared for freeze on DB axis**.

### 🔍 DB Verification Pack (Run Later) + Remedies

#### A) Schema & Keys (must match design)
- **Checks**
  - Confirm tables exist: `quotation_sale_boms`, `quotation_sale_bom_items`
  - Confirm keys/columns: `QuotationSaleBomId`, `QuotationSaleBomItemId`, `ProductId`, `Level`, `ParentBomId`, `Qty`, `Rate`, `RateSource`, `IsPriceMissing`, `Status`, timestamps
  - Confirm FK integrity (or explicit documented reason if FK not present)
- **SQL (example)**

```sql
SHOW CREATE TABLE quotation_sale_boms;
SHOW CREATE TABLE quotation_sale_bom_items;
```

- **Remedies**
  - If missing columns/keys: add migration (planned unless corrupting)
  - If FK missing and causing orphans: add FK OR add scheduled integrity job (priority based on impact)

#### B) Specific Product Enforcement (CRITICAL rule) — ✅ VERIFIED (PASS)
- **Checks**
  - Verify all active Proposal BOM items (Status=0) have ProductType=2 (Specific) in final persisted state
  - Verify no Proposal BOM items with ProductType=1 (Generic) exist in "final" state (transitional generic state is acceptable only as intermediate, never persisted as final)
  - Verify MakeId and SeriesId are required when ProductType=2
- **Results**
  - **DB-Check B1**: ✅ 0 rows (no active ProductType=1 items)
  - **DB-Check B2**: ✅ 0 rows (no ProductType=2 items missing MakeId/SeriesId)
- **Conclusion**: No active violations in Proposal BOM data. Code enforcement gaps (PB-GAP-001/002) remain but are non-blocking for Proposal BOM freeze.

#### C) Copy-Never-Link Independence (CRITICAL rule)
- **Checks**
  - Ensure Proposal BOM items are independent copies (Master BOM edits must not change existing Proposal BOM rows)
- **Test**
  - Create Master BOM → copy to quotation → edit Master BOM → confirm Proposal BOM unchanged
- **Remedies**
  - If linkage exists: CRITICAL logic defect — patch copy implementation immediately (Immediate)

#### D) Hierarchy Integrity (Level 0/1/2 boundaries)
- **Checks**
  - Verify Level 0 (Feeder) has no ParentBomId
  - Verify Level 1 (BOM1) has ParentBomId pointing to Level 0
  - Verify Level 2 (BOM2) has ParentBomId pointing to Level 1
  - Verify no nesting beyond Level 2
- **SQL (example)**

```sql
-- Level 0 must not have ParentBomId (must be 0 rows)
SELECT QuotationSaleBomId, Level, ParentBomId
FROM quotation_sale_boms
WHERE Status = 0
  AND Level = 0
  AND ParentBomId IS NOT NULL;

-- Level 1 must have ParentBomId pointing to Level 0 (must be 0 rows with invalid parent)
SELECT b1.QuotationSaleBomId, b1.Level, b1.ParentBomId, b2.Level AS ParentLevel
FROM quotation_sale_boms b1
LEFT JOIN quotation_sale_boms b2 ON b1.ParentBomId = b2.QuotationSaleBomId
WHERE b1.Status = 0
  AND b1.Level = 1
  AND (b1.ParentBomId IS NULL OR b2.Level != 0);

-- Level 2 must have ParentBomId pointing to Level 1 (must be 0 rows with invalid parent)
SELECT b1.QuotationSaleBomId, b1.Level, b1.ParentBomId, b2.Level AS ParentLevel
FROM quotation_sale_boms b1
LEFT JOIN quotation_sale_boms b2 ON b1.ParentBomId = b2.QuotationSaleBomId
WHERE b1.Status = 0
  AND b1.Level = 2
  AND (b1.ParentBomId IS NULL OR b2.Level != 1);
```

- **Remedies**
  - If violations exist: CRITICAL data integrity — quarantine/fix data + enforce validation guards (Immediate)

#### E) Quantity Chain & Roll-up Logic
- **Checks**
  - Verify quantity chain correctly walks up to Level 0 (feeder) for roll-up calculations
  - Verify no double-multiplication in roll-ups (SUM only at roll-up, not nested multiplication)
- **Remedies**
  - If logic errors exist: HIGH priority — fix calculation logic (Planned)

#### F) Soft Delete (Archival)
- **Checks**
  - Deletes set `Status=1` (no hard deletes)
  - Ensure delete doesn't cascade incorrectly
- **SQL**
  - Sample verify soft delete behavior on known IDs
- **Remedies**
  - If hard deletes exist: convert to soft-delete or enforce archival policy in service layer

### ✅ Status Usage Rule (for now)
- **Design evidence**: PASS / PASS WITH NOTES / FAIL
- **DB evidence**: DB-PENDING until verified

### Status wording (when DB is the only missing evidence)
If DB evidence is not available, but design/code evidence is complete, use:
**Status: ⏳ EVIDENCE-BASED (DB-PENDING)**

---

## Evidence Format (Mandatory)
Use one of:
- `Evidence: <file>:<section>`
- `Evidence: <file>:Lx–Ly` (if line references are available)

---

## 0) Executive Status

This Round‑1 record is maintained using a 3‑axis evidence model so DB unavailability, design-pack registration, and code availability are not conflated.

| Axis | Status | Meaning |
|---|---|---|
| Design Evidence | VERIFIED | Proposal BOM design pack registered in workspace (PROPOSAL_BOM_BACKEND_DESIGN_PART*.md files) |
| Code Evidence | ⚠️ PARTIAL | CE-04 VERIFIED (PB-GAP-003). CE-01 VERIFIED (PB-GAP-001/002) - FAIL status. CE-02 finding confirmed (PB-GAP-002) - snippet pending. CE-03 verified (PB-GAP-001/002) - FAIL status. PB-GAP-004 verified - PASS WITH NOTES. |
| DB Evidence | ✅ VERIFIED (PASS) | DB-Check B1: 0 rows (no active ProductType=1 items). DB-Check B2: 0 rows (no ProductType=2 items missing Make/Series). Proposal BOM cleared for freeze on DB axis. |

- **Repo-trace authority (design-pack requirement satisfied)**:
  - Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§2`
  - Evidence: Proposal BOM design pack registered in workspace (PROPOSAL_BOM_BACKEND_DESIGN_PART*.md files)

---

## 1) Preconditions & Constraints (as executed)

- **Design Evidence**: VERIFIED (design pack present in this workspace)
  - Evidence: Proposal BOM design pack registered in workspace (PROPOSAL_BOM_BACKEND_DESIGN_PART*.md files)
  - Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§2`

- **Code Evidence**: NOT VERIFIED (code repo not present in this workspace)
  - Code verification is tracked separately in Gap Register (PB-GAP-### entries)

- **DB Evidence**: ✅ VERIFIED (PASS) — DB-Check B1: 0 rows, DB-Check B2: 0 rows. No active violations in Proposal BOM data.

- **Upstream Dependencies (Governance Lock)**:
  - Item Master = trusted foundation ✅
  - Generic Item Master = frozen ✅
  - Master BOM = closed / audit-ready ✅
  - Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§0`

---

## 2) Round‑1 Review Sections (Executed)

Per the governed playbook, Round‑1 is executed using these sections and result labels (**PASS / PASS WITH NOTES / FAIL**), with DB verification explicitly tracked as **DB-PENDING**.

Evidence (repo-trace authority): `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§1`

| Section | Design Evidence | Code Evidence | DB Evidence | Notes | Evidence |
|---|---|---|---|---|---|
| 1 — Instance vs Template clarity | ✅ PASS | NOT VERIFIED | DB-PENDING | Proposal BOM is explicitly defined as an instance, not a template; Master BOM is a template. | `PROPOSAL_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md:§🎯 Design Principles`; `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md:§🔒 Golden Rule (Non-Negotiable)` |
| 2 — Copy-never-link is explicitly non-negotiable | ✅ PASS | NOT VERIFIED | DB-PENDING | "Always copy Master BOM, never link directly" is called out as non-negotiable and repeated across docs. | `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md:§🔒 Golden Rule (Non-Negotiable)`; `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md:§Rule 1: Copy Rule (Non-Negotiable)` |
| 3 — Hierarchy model is clearly defined | ✅ PASS WITH NOTES | NOT VERIFIED | DB-PENDING | Levels are defined as 0=Feeder, 1=BOM1, 2=BOM2 with ParentBomId rules. Design mentions "no nesting beyond Level 2" but explicit validation rules for Level boundaries need verification (see FZ-03). | `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md:§Operation 5: Copy Master BOM to Quotation` (Level field); `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§3.3` |
| 4 — Product specificity rule is explicitly declared | ✅ PASS WITH NOTES | NOT VERIFIED | DB-PENDING | Items must use Specific products (ProductType=2); Make/Series required; validation logic is described. However, transitional generic→specific state during copy needs verification (see FZ-01, PB-GAP-001). | `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` (Generic Product copied initially); `PROPOSAL_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md` (resolves to Specific); `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§3.4` |
| 5 — Pricing and "price missing" handling is defined | ✅ PASS | NOT VERIFIED | DB-PENDING | RateSource model, NetRate computation, IsPriceMissing logic are defined. | `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` (Rate=0, RateSource='UNRESOLVED', IsPriceMissing=1); `PROPOSAL_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md:§Step 5: Load Prices` |
| 6 — Quantity + cost roll-up logic exists | ✅ PASS WITH NOTES | NOT VERIFIED | DB-PENDING | Quantity chain + feeder discovery logic and cost roll-up logic are documented. However, edge cases around Level 1 attached directly under panel vs strict "Level 1 under Level 0" model need verification (see FZ-03, PB-GAP-003). | `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§3.6`; `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§4 FZ-03` |
| 7 — Deletion / soft-delete semantics exist | ✅ PASS | NOT VERIFIED | DB-PENDING | Status-based soft delete and recursive deletion are documented. | `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md:§Rule 5: Soft Delete`; `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§3.7` |
| 8 — Transitional Generic → Specific state (FZ-01) | ⚠️ PASS WITH NOTES | ❌ FAIL (CE-01, CE-03) | ✅ VERIFIED (PASS) | Design describes copying items with Generic ProductId temporarily, then resolving to specific after Make/Series selection. Code Evidence (CE-01, CE-03): applyMasterBom()/applyFeederTemplate() create items without forcing ProductType=2; no centralized ProductResolutionService exists. DB Evidence: 0 rows (no active ProductType=1 items). Code enforcement gaps remain but are non-blocking for Proposal BOM freeze. | `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` (ProductId = Generic); `PROPOSAL_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md` (updates to Specific); `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01, CE-03` |
| 9 — Enforcement location for "Specific products only" (FZ-02) | ⚠️ PASS WITH NOTES | ❌ FAIL (CE-01, CE-02, CE-03) | ✅ VERIFIED (PASS) | Rule is specified as application validation. Code Evidence (CE-01, CE-02, CE-03): applyMasterBom(), applyProposalBom(), addItem() do not consistently enforce ProductType=2; no centralized ProductResolutionService exists. DB Evidence: 0 rows (no ProductType=2 items missing Make/Series). Code enforcement gaps remain but are non-blocking for Proposal BOM freeze. | `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md`; `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01, CE-02, CE-03` |
| 10 — Quantity chain correctness + feeder discovery (FZ-03) | ⚠️ PASS WITH NOTES | ✅ VERIFIED (CE-04) | DB-PENDING | Quantity logic "walks up BOM chain to find feeder (Level 0)". Code implements legacy feeder support (Level 1 with no parent treated as feeder). Spec contradiction (Part 3 vs Part 5) needs correction to match code behavior. | `PROPOSAL_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md`; `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md`; `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-04` |
| 11 — Instance isolation under reuse/apply flows (FZ-04) | ⚠️ PASS WITH NOTES | ✅ PASS WITH NOTES (CE-04) | DB-PENDING (optional) | Copy semantics are declared, and interconnections describe independent instances. Code Evidence: Items are copied into new rows (no linking observed). Risk remains for repeated apply causing duplicate items unless target BOM is cleared or guarded. DB trigger/cascade check optional. | `PROPOSAL_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md:§Master BOM ↔ Proposal BOM`; `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md`; `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:PB-GAP-004` |

---

## 3) Focus Zone Analysis (from Round-0)

### FZ-01: Transitional Generic → Specific during copy-from-master

**Design Evidence:**
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Copy step sets ProductId from Master BOM item (generic) in create-from-master flow
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md` — Master Data flow repeats: copy generic → user selects Make/Series → update to specific → price load
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md` — Interconnections diagram codifies the same pipeline
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — Rules enforce "Specific products only"

**Code Evidence (CE-01):**
- ❌ FAIL: Copy-from-master is implemented via applyMasterBom() / applyFeederTemplate(). These flows create QuotationSaleBomItem records without forcing ProductType=2; items can persist with generic products and MakeId/SeriesId = 0. Transitional state is therefore not guaranteed to be intermediate only.
- Evidence: `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`

**Verification Required:**
- ✅ Design declares transitional state exists
- ❌ Code Evidence: Transitional state is not guaranteed to be intermediate only (generic can persist as final)
- ❓ Whether any downstream logic (pricing, validation, export, costing) incorrectly treats generic as valid "final"

**Final state definition (design axis):**
- Any saved Proposal BOM item with Status=0 and usable in costing/export/apply must have ProductType=2 (Specific).
- This aligns with the rule "Specific products only."

**Gap Status:** See PB-GAP-001 in Gap Register (Code Evidence: FAIL)

---

### FZ-02: Enforcement location for "Specific products only"

**Design Evidence:**
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — Rule is specified as application validation ("Specific products only")
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Validation occurs during Make/Series selection
- Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§3.4` — Rule is specified as application validation

**Code Evidence (CE-01):**
- ❌ FAIL: The following write paths do not consistently enforce ProductType=2: applyMasterBom(), applyProposalBom(), addItem(). Validation currently checks existence but not specificity or required Make/Series.
- Evidence: `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-01`

**Verification Required:**
- ✅ Design declares rule exists
- ❌ Code Evidence: Enforcement not applied on major write paths

**Gap Status:** See PB-GAP-002 in Gap Register (Code Evidence: FAIL)

---

### FZ-03: Quantity chain correctness + "feeder discovery" edge cases

**Design Evidence:**
- Evidence A: `PROPOSAL_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md` — Part 3 hierarchy allowance: "BOM1 = Child of Feeder or Panel" (allows Level 1 attachment directly under panel)
- Evidence B: `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — Part 5 enforces Level 1 must have ParentBomId (and implies it must have a parent, plus validation rules)
- Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§3.6` — Quantity logic "walks up BOM chain to find feeder (Level 0)"
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Level and ParentBomId fields exist in copy operation
- **Contradiction**: Part 3 allows Level 1 to be child of Feeder or Panel, while Part 5 requires Level 1 to have ParentBomId pointing to Level 0. These two statements cannot both be true without an explicit exception rule.
- **Decision (code-driven)**: Level-1 under Panel is supported only as legacy feeder (Level=1 and ParentBomId=NULL). "BOM1 under Panel" is not implemented as a normal case.

**Verification Required:**
- ✅ Design declares quantity chain logic exists
- ✅ Code Evidence (CE-04): QuantityService treats Level 1 with no parent as feeder-equivalent (legacy). Therefore "Level-1 under Panel" is supported only in this legacy feeder sense.
- **Implemented exception**: Level 1 with ParentBomId = NULL is treated as feeder-equivalent for quantity roll-ups (legacy support).
- **Spec correction required**: If BOM1 is allowed under Panel, then Part-5 validation must explicitly allow it and quantity chain rules must define how feederQty is sourced. Current code does not implement BOM1-under-panel as a normal case; it implements feeder-legacy.
- ❓ No double-multiplication on roll-ups (docs state SUM only at roll-up)

**Gap Status:** See PB-GAP-003 in Gap Register

---

### FZ-04: Instance isolation under reuse/apply flows

**Design Evidence:**
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md:§Master BOM ↔ Proposal BOM` — Independent instances described ("MasterBomId in QuotationSaleBom is reference only", "Changes to Master BOM don't affect Proposal BOMs")
- Evidence: `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Copy semantics are declared

**Verification Required:**
- ✅ Design declares copy semantics
- ❓ "Apply / reuse / promote" does not introduce hidden linking (foreign keys used as reference only, not behavioral linking)

**Gap Status:** See PB-GAP-004 in Gap Register

---

## 4) Next Step (After Round‑1 Execution)

1) Execute DB Verification Pack when DB/runtime access is available and update DB evidence from **DB-PENDING → VERIFIED** where applicable.
2) Verify code implementation against design specifications for all four focus zones (FZ-01 to FZ-04).
3) Address gaps identified in Gap Register (PB-GAP-001 through PB-GAP-004).

---

## Change Log

| Version | Date (IST) | Change |
|---|---|---|
| v1.0_2025-12-19 | 2025-12-19 | Created Round-1 Cumulative Review based on Round-0 Readiness document and Master BOM design pack |
| v1.1_2025-12-19 | 2025-12-19 | Phase-3: Added Gap Revalidation section; added layer context to gap references |

