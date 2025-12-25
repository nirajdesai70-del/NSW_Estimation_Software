# S2.4 — FEED Isolation Pack (Feeder Library CRUD vs QUO Apply Boundary + Gap Closure Requirements)
#
# Task coverage:
# - NSW-P4-S2-FEED-001 (G3) FEED read/apply contract boundary (planning-only)
# - NSW-P4-S2-FEED-GAP-001 (G3) Freeze Feeder Apply Contract requirements: reuse detection + clear-before-copy semantics (BOM-GAP-001, BOM-GAP-002)
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase‑4 execution.
- **No code moves**.
- **No logic fixes**.
- **No QUO‑V2 execution**: QUO‑V2 remains fenced behind `NSW-P4-S2-QUO-REVERIFY-001` (G4).
- FEED isolation here is limited to: **contracts, boundaries, forbidden couplings, and adapter seam notes**.

---

## 1) Confirmed Apply Entry Point (authoritative route; implementation fenced)

### Route surface (code anchor)

- **Route**: `quotation.v2.applyFeederTemplate`
- **HTTP**: `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
- **Controller target (snapshot)**: `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyFeederTemplate`

### Apply request contract (observed from FEED modal caller)

The V2 FEED modal posts:

- `MasterBomId` (template id; FEED templates are stored as `MasterBom` records with `TemplateType = FEEDER`)
- `FeederName` (required by UI)
- `Qty` (required by UI; parsed as float in UI)
- `_token` (CSRF)

### Apply response contract (observed from FEED modal caller)

The FEED modal expects:

- Success: `{ success: true, message?: string }` (reloads page)
- Failure: `{ success: false, message?: string }` (alerts)

---

## 2) FEED CRUD Surface (authoritative; FEED-owned)

### Feeder Library routes (code anchor)

FEED CRUD is provided via the Feeder Library route group:

- Prefix: `/feeder-library`
- Controller: `source_snapshot/app/Http/Controllers/FeederTemplateController.php`

**Routes (per `source_snapshot/routes/web.php` + `source_snapshot/trace/ROUTE_MAP.md`):**

- `feeder-library.index` → `GET /feeder-library`
- `feeder-library.create` → `GET /feeder-library/create`
- `feeder-library.store` → `POST /feeder-library`
- `feeder-library.show` → `GET /feeder-library/{id}`
- `feeder-library.edit` → `GET /feeder-library/{id}/edit`
- `feeder-library.update` → `PUT /feeder-library/{id}`
- `feeder-library.toggle` → `PATCH /feeder-library/{id}/toggle`

### Storage reality (important boundary note)

FEED templates are persisted using MBOM tables/models:

- `MasterBom` where `TemplateType = 'FEEDER'`
- Items via `masterbomitem` relationship (`MasterBomItem`)

**Discipline:** S2 does not refactor this storage; it only records the boundary and the required seams.

---

## 3) FEED Read vs Apply Boundary (hard boundary statements)

### Ownership split (effective for Phase‑4 planning)

- **FEED owns (CRUD + listing/UI)**:
  - Feeder template creation/editing/listing/archiving
  - The FEED modal’s template browse/select UX (read-only list + apply call)
  - Query contract for listing templates (including `masterbomitem_count`)
- **QUO owns (apply/mutation into quotations)**:
  - Creating a feeder instance inside a quotation tree from a template
  - Any pricing/discount/quantity propagation caused by applying a template

### Contract boundary statement

- FEED **may expose** a **read-only template snapshot** for selection (DTO).
- FEED **must not** apply templates into quotations (no writes into QUO models/tables).
- QUO apply **must treat FEED templates as external input** (via contracts/routes), not via direct coupling to FEED controller internals.

---

## 4) Forbidden Coupling (explicit)

### Forbidden: any QUO‑V2 core edits / behavior changes

**Rule:** No edits to QUO‑V2 controllers/services/models in S2.

- Do not touch `QuotationV2Controller` (PROTECTED) or downstream QUO services.
- Do not change request/response semantics of apply endpoints.

### Forbidden: FEED depending on QUO models/services

**Rule:** FEED CRUD code must not import or depend on QUO models/services/controllers.

- No new `App\Models\Quotation*` references inside FEED controllers/models.
- No new QUO service instantiations from FEED code.

---

## 5) Adapter Seam Notes (planning-only; no execution leakage)

### 5.1 Proposed seam: FEED template read adapter (FEED-owned)

**Contract name:** `FeederTemplateReadContract`  
**Owner:** FEED  
**Consumers:** FEED modal UI; (later) QUO apply (via adapter)  
**Purpose:** provide stable, read-only access to “active feeder templates” and basic metadata

**DTO skeleton (minimum):**

- `FeederTemplateSummary`:
  - `TemplateId` (maps to `MasterBomId`)
  - `Name`
  - `DefaultFeederName`
  - `UniqueNo?`
  - `Description?`
  - `IsActive`
  - `ComponentCount`

### 5.2 Proposed seam: FEED apply command wrapper (QUO-owned; FEED calls via route)

**Contract name:** `ApplyFeederTemplateCommand`  
**Owner:** QUO  
**Consumer:** FEED modal/apply UI  
**Purpose:** stable command interface for “apply template into quotation” without FEED reaching into QUO internals

**Input skeleton (matches observed UI payload):**

- `quotationId`
- `panelId`
- `templateId` (MasterBomId)
- `feederName`
- `qty`

---

## 6) Known Risks / Divergences (record only; do not fix in S2)

### Route ↔ controller mismatch (G4 re-verify blocker; authoritative)

Per `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`:

- `source_snapshot/routes/web.php` references `QuotationV2Controller@applyFeederTemplate`
- Route exists in snapshot
- Method is **not found** in `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`

**Discipline:** This is handled only by `NSW-P4-S2-QUO-REVERIFY-001` (G4). No fixes or QUO‑V2 edits in S2.

### Quantity type mismatch (UI vs request validation)

- FEED modal parses `Qty` as a float (`parseFloat(...) || 1`).
- `source_snapshot/app/Http/Requests/AddFeederRequest.php` defines `Qty` as `integer|min:1|max:999999`.

**Discipline:** Record only; no behavior change in S2.

### Storage coupling: FEED templates share MBOM persistence

- FEED CRUD uses `MasterBom` (`TemplateType='FEEDER'`) and `MasterBomItem`.

**Discipline:** Treat MBOM model changes as **out of scope** for S2 FEED; any future separation is via adapters/contracts only.

---

## 7) FEED Routes Inventory (authoritative; current implementation reality)

### 7.1 FEED-owned CRUD routes (FeederTemplateController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `feeder-library.index` | GET | `/feeder-library` | `FeederTemplateController@index` | List feeder templates | FEED-owned |
| `feeder-library.create` | GET | `/feeder-library/create` | `FeederTemplateController@create` | Show create form | FEED-owned |
| `feeder-library.store` | POST | `/feeder-library` | `FeederTemplateController@store` | Create feeder template | FEED-owned |
| `feeder-library.show` | GET | `/feeder-library/{id}` | `FeederTemplateController@show` | View feeder template | FEED-owned |
| `feeder-library.edit` | GET | `/feeder-library/{id}/edit` | `FeederTemplateController@edit` | Show edit form | FEED-owned |
| `feeder-library.update` | PUT | `/feeder-library/{id}` | `FeederTemplateController@update` | Update feeder template | FEED-owned |
| `feeder-library.toggle` | PATCH | `/feeder-library/{id}/toggle` | `FeederTemplateController@toggleActive` | Toggle active status | FEED-owned |

### 7.2 QUO-owned apply routes (QuotationV2Controller)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.v2.applyFeederTemplate` | POST | `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | `QuotationV2Controller@applyFeederTemplate` | Apply feeder template to quotation | QUO-owned (PROTECTED) |
| `reuse.feeder.apply` | POST | `/reuse/feeder/apply` | `QuotationV2Controller@applyFeederReuse` | Apply feeder from reuse search | QUO-owned (PROTECTED) |

**Note (route mismatch — G4 re-verify blocker):**
- Route `quotation.v2.applyFeederTemplate` exists in `source_snapshot/routes/web.php`
- Method `applyFeederTemplate` is **not found** in `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`
- **Discipline:** This is handled only by `NSW-P4-S2-QUO-REVERIFY-001` (G4). No fixes or QUO‑V2 edits in S2.

### 7.3 SHARED-owned reuse routes (ReuseController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `api.reuse.feeders` | GET | `/api/reuse/feeders` | `ReuseController@searchFeeders` | Search feeders for reuse | SHARED-owned (future) |

---

## 8) Forbidden Callers (hard fence for Phase-4)

### 8.1 Modules forbidden from calling FEED directly

**Rule:** The following modules **must not** call FEED ORM models or internal services directly:

- **QUO (Legacy + V2):** Must use `quotation.v2.applyFeederTemplate` wrapper endpoint only
- **MBOM:** Must not access FEED-specific logic (FEED templates are stored as `MasterBom` with `TemplateType='FEEDER'`)
- **PBOM:** Must use QUO apply wrapper (proposal reuse is QUO-owned)
- **SHARED:** Must use `FeederTemplateReadContract` (when implemented) or reuse search endpoints

### 8.2 Forbidden direct access patterns

**Forbidden:**
- `App\Models\MasterBom::where('TemplateType', 'FEEDER')` from QUO code (must use contract/route)
- Direct `FeederTemplateController` method calls from other controllers
- Bypassing `quotation.v2.applyFeederTemplate` to create feeder instances directly

**Allowed:**
- HTTP calls to `quotation.v2.applyFeederTemplate` endpoint
- HTTP calls to `api.reuse.feeders` endpoint (SHARED contract)
- Future: `FeederTemplateReadContract` interface calls (S4+)

### 8.3 FEED forbidden from calling

**Rule:** FEED **must not** call:

- QUO models/services (except via `ApplyFeederTemplateCommand` wrapper)
- MBOM models/services (FEED shares storage but must not couple to MBOM internals)
- PBOM models/services
- QUO costing/quantity services
- QUO controllers (except via HTTP wrapper endpoints)

---

## 9) Apply Semantics (qty, reuse detection, clear-before-copy, origin tracking, no side effects)

### 9.1 Quantity multiplier semantics

**Contract rule:** The `Qty` parameter in `quotation.v2.applyFeederTemplate` is a **feeder quantity**, not an item multiplier.

**Behavior (frozen in S2):**
- Template represents ONE canonical feeder (Qty=1)
- When applied, create ONE feeder row with `Qty` from request
- Use `master_bom_items.Quantity` as `ItemQtyPerBom` (do NOT multiply by feeder Qty)
- `QuotationQuantityService` handles `FeederQty × PanelQty` multipliers downstream

**Example:**
- Template item: `Quantity = 2.0`
- Apply request: `Qty = 3.0` (feeder quantity)
- Result: `QuotationSaleBomItem.Quantity = 2.0` (item qty per BOM, not multiplied)
- `QuotationSaleBom.Qty = 3.0` (feeder quantity)

### 9.2 Reuse detection semantics (BOM-GAP-001 closure requirement)

**Contract rule (frozen for S3 implementation):** Apply endpoint **must detect** if a feeder instance already exists from the same template in the same panel.

**Required behavior (to be implemented in S3):**
- Before creating a new feeder, check if `QuotationSaleBom` exists where:
  - `QuotationId` = target quotation
  - `ParentBomId` = target panel
  - `Level` = 0 (feeder level)
  - `OriginMasterBomId` = template `MasterBomId`
  - `Status` = 0 (active)
- If reuse detected:
  - Return response indicating reuse (e.g., `{ success: false, message: 'Feeder already exists from this template', reuse_detected: true, existing_feeder_id: <id> }`)
  - Do NOT create duplicate feeder
- If no reuse detected:
  - Proceed with normal apply flow

**Evidence requirement (BOM-GAP-001):**
- S3 implementation must provide evidence in `docs/PHASE_4/evidence/GAP/BOM-GAP-001/`
- Evidence must include: R1 request/response, S1/S2 snapshots showing reuse detection working

### 9.3 Clear-before-copy semantics (BOM-GAP-002 closure requirement)

**Contract rule (frozen for S3 implementation):** Apply endpoint **must clear** existing items from target feeder before copying template items.

**Required behavior (to be implemented in S3):**
- Before copying template items, delete all existing `QuotationSaleBomItem` rows where:
  - `QuotationSaleBomId` = target feeder `QuotationSaleBomId`
  - `Status` = 0 (active)
- Then copy template items as new rows
- This prevents duplicate stacking when applying the same template multiple times

**Evidence requirement (BOM-GAP-002):**
- S3 implementation must provide evidence in `docs/PHASE_4/evidence/GAP/BOM-GAP-002/`
- Evidence must include: R1 request/response, S1/S2 snapshots showing clear-before-copy working (items cleared, then new items added)

### 9.4 Origin tracking semantics

**Contract rule:** Apply endpoint must set origin tracking fields to enable reuse detection and audit trails.

**Fields set by apply (observed pattern from MBOM apply):**
- `QuotationSaleBom.OriginMasterBomId` = template `MasterBomId`
- `QuotationSaleBom.MasterBomId` = template `MasterBomId` (reference)
- `QuotationSaleBom.MasterBomName` = template `Name` (denormalized)
- `QuotationSaleBom.InstanceSequenceNo` = calculated sequence (1, 2, 3... per panel)
- `QuotationSaleBomItem.OriginMasterBomItemId` = `MasterBomItemId` (if applicable)

**Reuse detection dependency:**
- Reuse detection (BOM-GAP-001) depends on `OriginMasterBomId` being set correctly

### 9.5 No side effects rule

**Contract rule:** Apply operation must not mutate FEED template data.

**Guarantees:**
- `MasterBom` / `MasterBomItem` rows (where `TemplateType='FEEDER'`) are **never modified** by apply
- Apply creates new `QuotationSaleBom` / `QuotationSaleBomItem` rows only
- Template remains immutable and reusable

---

## 10) Gate-0 Template Data Readiness (BOM-GAP-013 requirement)

### 10.1 Gate-0 rule (must be satisfied before apply verification)

**Rule:** A feeder template (MasterBomId with `TemplateType='FEEDER'`) is "ready" only if:

- `COUNT(master_bom_items WHERE MasterBomId = TEMPLATE_ID) > 0`

**Discipline:** Do not execute apply verification unless selected `TEMPLATE_ID` has items.

### 10.2 Required evidence (read-only SQL)

**Evidence folder:** `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/`

**Evidence filename format:** `TEMPLATE_<TEMPLATE_ID>_count.txt`

**SQL to run (read-only):**
```sql
SELECT COUNT(*) AS item_count 
FROM master_bom_items 
WHERE MasterBomId = <TEMPLATE_ID>;
```

**Pass/Fail decision:**
- **PASS:** `item_count > 0` → template can be used for R1/R2 verification later
- **FAIL:** `item_count = 0` → do not proceed with apply verification; record FAIL and choose a different template (no DB edits in S2)

### 10.3 Evidence structure (BOM-GAP-013)

**Gate-0 output:** `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/TEMPLATE_<ID>_count.txt`

**R1 response:** `inserted_count = N` (must match `item_count` from Gate-0)

**S1/S2 snapshots:** `docs/PHASE_4/evidence/GAP/BOM-GAP-013/`

**Authority:** `docs/PHASE_4/GAP_GATEBOARD.md` (Lane-A gap BOM-GAP-013)

---

## 11) S4 Propagation Hooks (declared, not executed)

### 11.1 Contract propagation targets

**Target 1: FeederTemplateReadContract implementation**
- **Owner:** FEED
- **Consumers:** QUO apply, FEED modal UI, reuse search
- **S4 Task:** `NSW-P4-S4-FEED-001` — Propagate Feeder apply contract to V2

**Target 2: ApplyFeederTemplateCommand wrapper**
- **Owner:** QUO
- **Consumer:** FEED modal/apply UI
- **S4 Task:** Adopt wrapper entry points for V2 apply flows (when `NSW-P4-S2-QUO-002` completes)

**Target 3: Reuse detection + clear-before-copy implementation**
- **Owner:** QUO (apply behavior)
- **Consumer:** FEED apply flows
- **S3 Task:** `NSW-P4-S3-FEED-GAP-001` — Align Feeder apply implementation to match contract: reuse detection + clear-before-copy (close BOM-GAP-001, BOM-GAP-002 via evidence)

### 11.2 Route migration targets

**Target 1: Reuse search routes → ReuseSearchContract**
- `api.reuse.feeders` → Migrate to `ReuseSearchContract` (when `NSW-P4-S2-SHARED-001` completes)

**Target 2: Legacy routes → Deprecation**
- No legacy FEED routes identified (FEED is V2-only feature)

### 11.3 Gap closure targets (S3/S4)

**Target 1: BOM-GAP-001 closure (reuse detection)**
- **S3 Task:** `NSW-P4-S3-FEED-GAP-001` — Implement reuse detection in `quotation.v2.applyFeederTemplate`
- **Evidence:** `docs/PHASE_4/evidence/GAP/BOM-GAP-001/`

**Target 2: BOM-GAP-002 closure (clear-before-copy)**
- **S3 Task:** `NSW-P4-S3-FEED-GAP-001` — Implement clear-before-copy in `quotation.v2.applyFeederTemplate`
- **Evidence:** `docs/PHASE_4/evidence/GAP/BOM-GAP-002/`

**Target 3: BOM-GAP-013 closure (template data readiness)**
- **S2 Task:** Gate-0 evidence collection (read-only)
- **S5 Task:** Final closure verification (G4)

---

## 12) References (Authority)

**Authority Documents:**
- `trace/phase_2/FILE_OWNERSHIP.md` (FeederTemplateController ownership)
- `trace/phase_2/ROUTE_MAP.md` (FEED routes inventory)
- `docs/PHASE_4/S2_GOV_BOUNDARY_BLOCKS.md` (FEED boundary rules)
- `docs/PHASE_4/S2_GOV_EXCEPTION_TASK_MAPPING.md` (Exception mapping)
- `docs/PHASE_4/GAP_GATEBOARD.md` (BOM-GAP-001, BOM-GAP-002, BOM-GAP-013)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (Gate-0 Template Data Readiness rule)
- `docs/PHASE_4/S2_MBOM_ISOLATION.md` (MBOM pattern reference)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (CatalogLookupContract + ReuseSearchContract)

**Code Anchors:**
- `source_snapshot/app/Http/Controllers/FeederTemplateController.php` (FEED CRUD)
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyFeederTemplate` (QUO apply — route exists, method missing, G4 re-verify blocker)
- `source_snapshot/app/Http/Controllers/ReuseController.php@searchFeeders` (Reuse search)
- `source_snapshot/routes/web.php` (Route definitions)
- `source_snapshot/resources/views/quotation/v2/_feeder_library_modal.blade.php` (FEED modal caller)

---

## 13) Evidence / Approvals Checklist (G3)

- [x] Architectural approval: FEED CRUD vs QUO apply boundary accepted
- [x] Execution approval: planning-only; no behavior change; no QUO‑V2 scope crossed
- [x] Adapter seam acceptance: `FeederTemplateReadContract` + `ApplyFeederTemplateCommand` recorded as the only approved future refactor seams
- [x] Gap closure requirements: BOM-GAP-001 (reuse detection) + BOM-GAP-002 (clear-before-copy) semantics frozen in contract
- [x] Gate-0 template readiness: BOM-GAP-013 evidence procedure declared
- [x] Routes inventory: All FEED routes classified (FEED-owned, QUO-owned, SHARED-owned)
- [x] Forbidden callers: Hard fence documented for all modules
- [x] Apply semantics: Quantity multiplier, reuse detection, clear-before-copy, origin tracking, no side effects documented
- [x] S4 propagation hooks: Contract migration targets declared

---

## Task Status

- **NSW-P4-S2-FEED-001:** ✅ Complete
- **NSW-P4-S2-FEED-GAP-001:** ✅ Complete
- **Next Task:** NSW-P4-S2-PBOM-001 (Proposal BOM interface contract)

---

**Last Updated:** 2025-12-18  
**Status:** ✅ Complete — Ready for S3 alignment


