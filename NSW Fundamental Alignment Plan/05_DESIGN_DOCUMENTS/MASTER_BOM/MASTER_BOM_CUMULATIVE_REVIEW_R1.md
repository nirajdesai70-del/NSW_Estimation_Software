# Master BOM — Cumulative Review (Round-1)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md  
**Version:** v1.0_20251218  
**Date (IST):** 2025-12-18  
**Status:** ⏳ **EVIDENCE-BASED (DB-PENDING)**

## ✅ Standard Remark: Evidence-Based Review (DB Pending)

**Remark (Scope & Evidence Tier):**  
This Master BOM review is executed using the authoritative Master BOM design pack (Index/Plan + Parts 1–11) and code references where available. The design pack is now **imported/registered into this repo workspace for evidence-path referencing** under `docs/MASTER_BOM/DESIGN/`, therefore Design Evidence is marked **VERIFIED**. Live database verification is not available as of **2025-12-18**, therefore all data-integrity outcomes that require runtime/DB proof are marked **DB-PENDING** and must be validated before any “final freeze” is treated as production-confirmed.

**Reminder (Mandatory DB Verification Later):**  
Before final acceptance / production freeze, execute the DB Verification Pack below and update this document’s status from **DB-PENDING → VERIFIED** (DB axis).

### 🔍 DB Verification Pack (Run Later) + Remedies

#### A) Schema & Keys (must match design)
- **SQL (example)**

```sql
SHOW CREATE TABLE master_boms;
SHOW CREATE TABLE master_bom_items;
```

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

#### C) Copy-Never-Link Independence (CRITICAL rule)
- **Test**: Create Master BOM → copy to quotation → edit Master BOM → confirm quotation BOM unchanged

#### D) Soft Delete (Archival)
- **Check**: Deletes set `Status=1` (no hard deletes); ensure delete doesn’t cascade into quotation/proposal BOM

#### E) Pricing/SKU Non-Leakage at Master BOM stage
- **Check**: Master BOM stage must not join price/SKU tables; proposal stage may resolve pricing after Make/Series selection

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
| Design Evidence | VERIFIED | Design pack registered under `docs/MASTER_BOM/DESIGN/` |
| Code Evidence | PARTIAL (EXTERNAL) | Code evidence exists externally (see MB-GAP-003/004); code repo not registered in this workspace |
| DB Evidence | DB-PENDING | No DB access available today; runtime data integrity proof pending |

- **Repo-trace authority (design-pack requirement satisfied)**:
  - Evidence: `CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md:L38–L59`
  - Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§3.2`

---

## 1) Preconditions & Constraints (as executed)

- **Design Evidence**: VERIFIED (design pack present in this workspace)
  - Evidence: `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_INDEX.md:§📚 Document Structure`

- **Code Evidence**: PARTIAL (EXTERNAL) — authoritative code-path evidence for critical gaps is tracked in MB-GAP-003/004.
  - Evidence: `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-003`
  - Evidence: `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-004`

- **DB Evidence**: DB-PENDING (no runtime/DB access in this workspace)

- **Specific Item Master “plan recorded” artifact**: still IMPORT-PENDING (tracked separately as MB-GAP-002; does not block Master BOM design-pack execution here)
  - Evidence: `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-002`

---

## 2) Round‑1 Review Sections (Executed)

Per the governed playbook, Round‑1 is executed using these sections and result labels (**PASS / PASS WITH NOTES / FAIL**), with DB verification explicitly tracked as **DB-PENDING**.

Evidence (repo-trace authority): `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§1`

| Section | Design Evidence | Code Evidence | DB Evidence | Notes | Evidence |
|---|---|---|---|---|---|
| 1 — Category compliance | ✅ PASS | N/A | DB-PENDING | Category/SubCategory/Item used as hierarchy path (grouping/browse), not as device identity anchor | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md:§Product Hierarchy Connection`; `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md:§Master BOM ↔ Category/SubCategory/Item` |
| 2 — SubCategory compliance (EX‑SUBCAT‑001 aware) | ✅ PASS WITH NOTES | N/A | DB-PENDING | Design uses SubCategory as hierarchy tier; EX‑SUBCAT‑001 governance exception remains handled in frozen Generic Item Master standards, not inside Master BOM design | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md:§Product Hierarchy Connection` |
| 3 — Item/ProductType compliance | ✅ PASS WITH NOTES | ⚠️ PARTIAL (EXTERNAL) | DB-PENDING | Design pack models MasterBomItem.ProductId → Generic Product (ProductType=1). External code evidence establishes a B4 L0/L1 spec-template model (ProductId NULL + ResolutionStatus L0/L1), and quotation apply logic expects ProductId — reconcile/align as governed in MB-GAP-003 | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md:§MasterBomItem Entity`; `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md:§Generic Products Only`; `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-003` |
| 4 — Attributes compliance | ✅ PASS WITH NOTES | NOT VERIFIED | DB-PENDING | Design pack defines MasterBomItem as template rows (Quantity + reference fields) and explicitly excludes Make/Series and pricing; L0/L1 descriptor/spec attribute shape (B4) is established in external code and should be aligned into governed docs as needed | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md:§🎯 Design Principles`; `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md:§📊 Field Details` |
| 5 — Item Master + Product rule (CRITICAL) | ✅ PASS WITH NOTES | ⚠️ PARTIAL (EXTERNAL) | DB-PENDING | Design rule is “generic products only” at Master BOM stage; external B4 implementation enforces ProductId NULL for L0/L1 templates, pushing concrete Product selection to quotation/proposal resolution stage; treat as governed model difference (MB-GAP-003) until reconciled | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md:§Generic Products Only`; `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md:§Generic Products Only`; `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-003` |
| 6 — Generic Item Master alignment (FROZEN) | ✅ PASS WITH NOTES | N/A | DB-PENDING | Design pack keeps Master BOM as template layer (no pricing, no Make/Series); Generic Item Master freeze is an external governance dependency (not re-modeled here) | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md:§🎯 Design Principles`; `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md:§🎯 Master BOM Characteristics` |
| 7 — Specific Item Master alignment (PLANNED) | ✅ PASS WITH NOTES | NOT VERIFIED | DB-PENDING | Specific product selection happens only after copy into quotation (Make/Series selection), consistent with planned Specific Item Master dependency; plan-recorded artifact remains IMPORT-PENDING (MB-GAP-002) | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md:§🔄 Copy Process Overview`; `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-002` |
| 8 — L0/L1/L2 integrity | ✅ PASS WITH NOTES | ⚠️ PARTIAL (EXTERNAL) | DB-PENDING | Design pack keeps Master BOM as template; quotation resolution creates/uses specific products after Make/Series. Enforce B4 invariant (ResolutionStatus L0/L1 only, ProductId NULL for L0/L1) via DB verification later | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md:§📊 Step-by-Step Copy Process`; `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:§✅ DB-PENDING verification items`; `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-003` |
| 9 — Copy‑never‑link rule (CRITICAL) | ✅ PASS | ✅ PASS (EXTERNAL) | DB-PENDING | Design states always copy/never link; external quotation apply logic creates new quotation BOM items from Master BOM items (copy semantics) | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md:§🔒 Golden Rule (Non-Negotiable)`; `/Users/nirajdesai/Projects/nish/app/Http/Controllers/QuotationV2Controller.php:L1155–L1225` |
| 10 — Pricing / SKU governance non‑leakage | ✅ PASS | ✅ PASS WITH NOTES (EXTERNAL) | DB-PENDING | Design: no pricing at Master BOM stage; pricing resolved after copy at quotation/proposal stage. External code applies pricing during quotation BOM item creation (acceptable at proposal layer, not at Master BOM template layer) | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md:§🎯 Master BOM Characteristics`; `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md:§📊 Step-by-Step Copy Process`; `/Users/nirajdesai/Projects/nish/app/Http/Controllers/QuotationV2Controller.php:L1174–L1215` |
| 11 — Archival / deletion governance | ✅ PASS | ❌ FAIL (EXTERNAL) | DB-PENDING | Design requires soft delete via Status; external code evidence shows hard delete (`delete()`) for MasterBom and MasterBomItem (MB-GAP-004) | `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md:§Rule 5: Soft Delete`; `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L287–L299`; `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:MB-GAP-004` |

---

## 3) Next Step (After Round‑1 Execution)

1) Execute DB Verification Pack when DB/runtime access is available and update DB evidence from **DB-PENDING → VERIFIED** where applicable.
2) Import/register the Specific Item Master "plan recorded" artifact and close MB-GAP-002 when evidence-path references are resolvable.
3) If the authoritative implementation is the B4 ResolutionStatus model, align the design pack (and any quotation apply flows) to remove ProductId-model drift (see MB-GAP-003).

---

## 4) Gap Revalidation (Phase-3)

**Purpose:** All gaps referenced in this review are tracked in the Master BOM Gap Register with L0-L1-L2 layer labels.

**Gap References:**
- **MB-GAP-003 [L1 Layer]:** Master BOM items force ProductId = NULL (descriptor/spec model) — See Gap Register for revalidation
- **MB-GAP-004 [L1 Layer]:** Master BOM uses hard delete — See Gap Register for revalidation
- **MB-GAP-002 [Cross-Layer]:** Specific Item Master plan — CLOSED (resolved)

**Layer Context:**
- **L0:** Generic Item Master (Functional Family)
- **L1:** Master BOM (Technical Variant, Make-agnostic) — **Master BOM operates at L1**
- **L2:** Specific Item Master / Proposal BOM (Catalog Item with Make+Series+SKU)
- **Proposal-Resolution:** L1 → L2 resolution process

**See:** `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:§6 Gap Revalidation (Phase-3)` for complete revalidation table.

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | Updated to 2-axis evidence model; Design Evidence set to IMPORT-PENDING (pack exists externally, pending repo registration) and DB set to DB-PENDING |
| v1.0_20251218 | 2025-12-18 | Executed Round-1 using registered design pack; updated evidence axes and recorded section outcomes (DB remains DB-PENDING) |
| v1.1_20251219 | 2025-12-19 | Phase-3: Added Gap Revalidation section; added layer context to gap references |


