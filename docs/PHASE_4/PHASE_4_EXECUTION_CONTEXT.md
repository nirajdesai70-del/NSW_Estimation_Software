# Phase 4 Execution Context — S0 Evidence + S1 Ownership Lock
#
# Scope: Phase-4 execution governance artifacts only.
# Rule: Do NOT edit Phase-3 docs here. Phase-3 remains frozen.
#
# Repository: NSW_Estimation_Software
# Owner: Execution Lead (Nish) + Reviewer
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## S0 Closure (Formal)

**S0 CLOSED WITH CONDITIONS:** QUO-V2 route ↔ controller mismatches (`applyFeederTemplate`, `updateItemQty`) recorded as trace/snapshot divergence. **Hard prerequisite:** must be re-verified against live execution code before any QUO-V2 execution tasks in Phase-4.

---

## S0 Evidence Pointers (Read-only)

**Authority (Phase-3 / Phase-2):**
- Gates: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Rulebook: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`
- Task list (Batch-1): `docs/PHASE_3/04_TASK_REGISTER/BATCH_1_S0_S1.md`
- Trace maps: `trace/phase_2/ROUTE_MAP.md`, `trace/phase_2/FEATURE_CODE_MAP.md`, `trace/phase_2/FILE_OWNERSHIP.md`

**Observed trace/snapshot divergences (must re-verify in live code before QUO-V2 execution):**
- `source_snapshot/routes/web.php` references `QuotationV2Controller@applyFeederTemplate`
  - Route exists in snapshot
  - Method not found in `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`
- `source_snapshot/routes/web.php` references `QuotationV2Controller@updateItemQty`
  - Route exists in snapshot
  - Method not found in `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`

---

## S1 Ownership Lock (Authoritative for execution planning)

### 1) Locked ownership + risk (from Phase-2 authority)

**Source of truth:** `trace/phase_2/FILE_OWNERSHIP.md`

**Quotation (PROTECTED / no-go without G4 approvals):**
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php` — Owner: **QUO** — Risk: **PROTECTED** — **RE-VERIFY REQUIRED** (see S0 Closure)
- `source_snapshot/app/Services/QuotationQuantityService.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Services/CostingService.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Services/DiscountRuleApplyService.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Services/QuotationDiscountRuleService.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Services/DeletionPolicyService.php` — Owner: **SHARED** — Risk: **PROTECTED**
- `source_snapshot/app/Models/Quotation.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Models/QuotationSale.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Models/QuotationSaleBom.php` — Owner: **QUO** — Risk: **PROTECTED**
- `source_snapshot/app/Models/QuotationSaleBomItem.php` — Owner: **QUO** — Risk: **PROTECTED**

**Cross-module template entities (PROTECTED):**
- `source_snapshot/app/Models/MasterBom.php` — Owner: **MBOM** — Risk: **PROTECTED**
- `source_snapshot/app/Models/MasterBomItem.php` — Owner: **MBOM** — Risk: **PROTECTED**

**CIM protected list items (exist; treat as HIGH unless reclassified):**
- `source_snapshot/app/Services/ProductAttributeService.php` — Owner: **CIM** — Risk: *(not classified in FILE_OWNERSHIP first pass; treat as HIGH until confirmed)*
- `source_snapshot/app/Helpers/ProductHelper.php` — Owner: **CIM** — Risk: *(not classified in FILE_OWNERSHIP first pass; treat as HIGH until confirmed)*
- `source_snapshot/app/Services/AutoNamingService.php` — Owner: *(not classified in FILE_OWNERSHIP first pass; treat as HIGH until confirmed)*

### 2) Ownership exceptions list (split / mixed-responsibility)

**Split ownership (must coordinate before any change):**
- `source_snapshot/app/Http/Controllers/ImportController.php`
  - Component/Item Master: import routes (`/import*`)
  - Master: pdf container routes (`/pdfcontain*`)
  - Risk: **HIGH** (per `trace/phase_2/FILE_OWNERSHIP.md`)

### 3) Forbidden callers + “no-go list” (S1 fence)

**No-go list (do not edit / do not introduce new callers without correct gate + approvals):**
- PROTECTED: `QuotationV2Controller`, `CostingService`, `QuotationQuantityService`, `DeletionPolicyService`, core QUO V2 models (`Quotation*Sale*`), MBOM template models (`MasterBom*`)

**Evidence-based current callers (snapshot scan):**
- `CostingService` is instantiated via `app()` in:
  - `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`
  - `source_snapshot/app/Http/Controllers/QuotationController.php`
- `QuotationQuantityService` is instantiated via `app()` in:
  - `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`
  - `source_snapshot/app/Console/Commands/RecalculateQuotationAmounts.php`
- `DeletionPolicyService` is instantiated via `app()` in:
  - `source_snapshot/app/Http/Controllers/QuotationController.php`

**S1 forbidden-caller rule (effective immediately for Phase-4 execution):**
- No module outside **QUO** may introduce new direct calls to QUO PROTECTED services/models/controllers.
- Any cross-module integration must occur only via the **documented HTTP routes** (Apply endpoints, Shared APIs), or later via **approved adapters/wrappers** (G4) without modifying protected-core directly.

---

## S1 Module Boundary Blocks (Execution fences)

### SHARED
- **In-scope**: cross-cutting policies/services (e.g., `DeletionPolicyService`) and shared endpoints identification.
- **Forbidden**: direct edits to QUO protected logic; changes without explicit gate evidence.

### CIM (Component/Item Master)
- **In-scope**: Catalog CRUD, attributes, import/export (CIM-owned portions).
- **Forbidden callers**: do not call QUO protected services directly.
- **Integration points**:
  - Quotation shared dropdown APIs (served by QuotationController per current trace): `/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*`, `/api/makes`.

### MBOM
- **In-scope**: Master BOM CRUD + template integrity.
- **Forbidden**: direct edits to QUO-V2 protected core.
- **Integration points**:
  - QUO V2 apply: `quotation.v2.applyMasterBom` (POST `/quotation/v2/apply-master-bom`)

### FEED
- **In-scope**: Feeder template CRUD (via Feeder Library).
- **Forbidden**: direct edits to QUO-V2 protected core.
- **Integration points**:
  - QUO V2 apply: `quotation.v2.applyFeederTemplate` (POST `/quotation/{quotation}/panel/{panel}/feeder/apply-template`)
  - Note: **re-verify required** due to route↔controller mismatch recorded in S0.

### PBOM
- **In-scope**: Proposal BOM list/show/reuse/promote boundaries.
- **Forbidden**: direct edits to QUO-V2 protected core.
- **Integration points**:
  - QUO V2 apply: `quotation.v2.applyProposalBom` (POST `/quotation/v2/apply-proposal-bom`)

### QUO (Legacy + V2)
- **In-scope**: Legacy quotation flow, V2 flow, discount rules.
- **Forbidden**: any QUO-V2 changes before re-verifying the route/controller surface in live execution code; any protected changes without G4.

---

## Planned Task Stub (Planning-only; do NOT execute now)

**Task ID:** NSW-P4-S2-QUO-REVERIFY-001  
**Purpose:** Re-verify QUO-V2 routes vs live controller methods (resolve snapshot divergence: `applyFeederTemplate`, `updateItemQty`)  
**Precondition:** Phase-4 execution branch exists and governance approvals for PROTECTED scope are in place  
**Gate:** G4  
**Status:** Planned

---

## Phase 5 Scope Note

**Important:** Phase 5 (NSW Canonical Data Dictionary & Schema Design) will begin **only after** Phase 4 execution completes (S5 regression gate passed).

**Phase 5 Scope:**
- Analysis-only: Data dictionary freeze + schema design
- Does NOT include legacy data migration (separate project)
- See `docs/PHASE_5/PHASE_5_SCOPE_FENCE.md` for detailed scope

**Estimated Phase 4 completion timeline:** 13-18 weeks from current date (see `PHASE_4_EXECUTION_SUMMARY.md` for details).


