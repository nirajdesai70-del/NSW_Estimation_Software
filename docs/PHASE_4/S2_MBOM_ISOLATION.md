# S2.3 — MBOM Isolation Pack (Read/Apply Boundary + Adapter Seam Notes)
#
# Task coverage:
# - NSW-P4-S2-MBOM-001 (G3) MBOM read/apply contract boundary (planning-only)
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase‑4 execution.
- **No code moves**.
- **No apply behavior changes** (explicitly forbidden in S2).
- **No QUO‑V2 execution work** is authorized here beyond naming the existing entrypoint contracts (QUO‑V2 remains fenced by `NSW-P4-S2-QUO-REVERIFY-001`, G4).
- This artifact only defines **contracts, boundaries, forbidden couplings, and adapter seam notes**.

---

## 1) Confirmed Apply Entry Point (authoritative)

### Route surface (code anchor)

- **Route**: `quotation.v2.applyMasterBom`
- **HTTP**: `POST /quotation/v2/apply-master-bom`
- **Controller**: `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyMasterBom`
- **Middleware**: `auth`, `throttle:critical-write`

### Apply request contract (observed; stable contract target)

The apply endpoint validates/consumes:

- `QuotationId` (required)
- `QuotationSaleBomId` (required) — target feeder/BOM node to receive items
- `MasterBomId` (required) — selected template
- `Qty` (required) — multiplier
- `Items` (optional array) — if present, items are created from request payload; if absent, items are loaded from `MasterBomItem` rows

**Item payload shape (observed from V2 panel modal + controller usage):**

- `ProductId` (required to create an item; falsy/0/empty values are skipped)
- Optional fields (defaulted if missing): `MakeId`, `SeriesId`, `Description`, `Qty`, `Rate`, `Discount`, `Remark`, `RateSource`, `IsClientSupplied`

### Apply response contract (observed; stable contract target)

- Success: `{ success: true, message: string }`
- Validation failure: `{ success: false, message: string }` (422)
- Execution failure: `{ success: false, message: string, error_details?: string|null }` (500)

---

## 2) MBOM Read vs Apply Boundary (hard boundary statements)

### Ownership split (authoritative intent for Phase‑4)

- **MBOM owns (read/store integrity)**:
  - `MasterBom` / `MasterBomItem` data model and CRUD behavior
  - Template integrity rules (e.g. B4 constraints)
  - MBOM UI + CRUD routes: `source_snapshot/routes/web.php` → `MasterBomController`
- **QUO owns (apply/mutation into quotations)**:
  - “Apply Master BOM” behavior that mutates quotation structures and prices
  - The `quotation.v2.applyMasterBom` endpoint and all downstream QUO models/services it touches

### Contract boundary statement (effective immediately for Phase‑4 execution planning)

- MBOM **may expose** a **read-only template snapshot** (DTO) suitable for application elsewhere.
- MBOM **must not** apply templates into quotations (no writes into QUO tables/models).
- QUO apply **must treat MBOM as an external template source**, not as a set of ORM models to couple to.

---

## 3) Forbidden Coupling (explicit)

### Forbidden: MBOM ↔ QUO direct model access

**Rule:** MBOM code must not import or depend on QUO models/services/controllers (especially **PROTECTED** QUO objects).

- Forbidden examples (representative):
  - `App\Models\Quotation*`
  - QUO services (costing/discount/quantity/audit)
  - QUO controllers

**Note (current snapshot coupling to record, not to change in S2):**

- `source_snapshot/app/Http/Controllers/MasterBomController.php` currently imports and queries `App\Models\QuotationSaleBom` in `destroy()` to block deletion when a master BOM is referenced.
- This is a direct QUO model dependency and must be isolated behind an adapter/contract in Phase‑4 execution **after approvals**, but **not in S2**.

### Forbidden: any apply behavior change

**Rule:** `quotation.v2.applyMasterBom` behavior is frozen in S2.

- No changes to item creation logic
- No changes to pricing/discounting logic
- No changes to request/response semantics
- No changes to throttling/auth surface

---

## 4) Adapter Seam Notes (planning-only; no execution leakage)

### 4.1 Proposed seam: MBOM read adapter (MBOM-owned)

**Contract name:** `MasterBomTemplateReadContract`  
**Owner:** MBOM  
**Consumer(s):** QUO apply (later via adapter), reuse/search UI flows  
**Purpose:** provide a stable, read-only DTO representation of a template and its items

**DTO skeleton (minimum required fields; derived from current schema):**

- `MasterBomTemplateSnapshot`:
  - `MasterBomId`
  - `Name`
  - `UniqueNo`
  - `Description`
  - `TemplateType?`, `IsActive?`, `DefaultFeederName?` (if needed by UI)
  - `items[]`
- `MasterBomTemplateItemSnapshot`:
  - `MasterBomItemId`
  - `Quantity`
  - `UOM?`
  - `ResolutionStatus` (B4: `L0|L1`)
  - `ProductId` (nullable by design under B4)
  - `GenericDescriptor?`, `DefinedSpecJson?`, `SpecKey?`

### 4.2 Proposed seam: “usage check” for delete guard (QUO-owned, consumed by MBOM)

**Contract name:** `MasterBomUsageContract`  
**Owner:** QUO (or SHARED if later standardized)  
**Consumer:** MBOM delete guard  
**Purpose:** answer “is this MasterBomId referenced by any active quotation structures?”

**Return shape:**

- `{ inUse: boolean, usageCount?: number, exampleQuotationIds?: number[] }`

**Resulting MBOM rule:** MBOM enforces deletion constraints via contract call, not via direct QUO model imports.

---

## 5) Known Cross-Module Assumption Risks (record only; do not fix in S2)

### B4 template items vs apply expectations

- MBOM enforces (B4 + model normalization): for `ResolutionStatus ∈ {L0, L1}`, `ProductId` is **NULL**.
- `quotation.v2.applyMasterBom`’s fallback path (when `Items` are not provided) loads `MasterBomItem` rows and then attempts to resolve `Product` using `masterItem->ProductId`.
- This creates a high-likelihood “skip all items” failure mode if templates contain only L0/L1 items with `ProductId = NULL`.

**Discipline:** Record as a re-verify/fix candidate, but do not modify QUO‑V2 behavior until `NSW-P4-S2-QUO-REVERIFY-001` (G4) is completed and approvals are in place.

### V2 UI “compat materialization” dependency

- The V2 panel modal JS can attempt to materialize `Items` by calling a legacy route `quotation.getMasterBomVal` to obtain HTML and parse component rows.

**Discipline:** This is an important coupling to document; isolation/cleanup is **not allowed** in S2.

---

## 6) MBOM Read Contract (what consumers may read, nothing more)

### 6.1 Read-only template access (MBOM-owned surface)

**Contract name:** `MasterBomTemplateReadContract`  
**Owner:** MBOM  
**Consumers:** QUO apply flows, reuse/search UI, FEED operations, PBOM operations  
**Purpose:** Expose read-only template data without exposing internal ORM models

**Allowed read operations:**

1. **Get template header:**
   - `getTemplateHeader(MasterBomId): MasterBomTemplateSnapshot`
   - Returns: `MasterBomId`, `Name`, `UniqueNo`, `Description`, `TemplateType?`, `IsActive?`, `DefaultFeederName?`

2. **Get template items:**
   - `getTemplateItems(MasterBomId): MasterBomTemplateItemSnapshot[]`
   - Returns: Array of item snapshots with `MasterBomItemId`, `Quantity`, `UOM?`, `ResolutionStatus`, `ProductId?`, `GenericDescriptor?`, `DefinedSpecJson?`, `SpecKey?`

3. **List active templates:**
   - `listActiveTemplates(TemplateType?: string): MasterBomTemplateSnapshot[]`
   - Returns: Array of template headers (filtered by `IsActive = 1`, optionally by `TemplateType`)

**Forbidden read operations:**

- Direct `MasterBom` / `MasterBomItem` ORM model access from outside MBOM
- Reading internal MBOM validation state or business logic
- Accessing MBOM audit logs or internal tracking fields

### 6.2 Catalog lookup dependency (SHARED contract)

**Rule:** MBOM UI operations (create/edit) must consume `CatalogLookupContract` for dropdown data.

**Current state (to migrate in S4):**
- `MasterBomController@getsubcategory` → COMPAT endpoint (must migrate to `CatalogLookupContract`)
- `MasterBomController@getproducttype` → COMPAT endpoint (must migrate to `CatalogLookupContract`)
- `MasterBomController@getdescription` → COMPAT endpoint (must migrate to `CatalogLookupContract`)

**Migration plan:** See `docs/PHASE_4/S2_CIM_ISOLATION.md` (Section 2.4.1 — Catalog Lookup Route Classification Table)

---

## 7) MBOM Routes Inventory (authoritative; current implementation reality)

### 7.1 MBOM-owned CRUD routes (MasterBomController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `masterbom.index` | GET | `/masterbom` | `MasterBomController@index` | List master BOMs | MBOM-owned |
| `masterbom.create` | GET | `/masterbom/create` | `MasterBomController@create` | Show create form | MBOM-owned |
| `masterbom.store` | POST | `/masterbom/create` | `MasterBomController@store` | Create master BOM | MBOM-owned |
| `masterbom.edit` | GET | `/masterbom/{id}/edit` | `MasterBomController@edit` | Show edit form | MBOM-owned |
| `masterbom.update` | PUT | `/masterbom/{id}/edit` | `MasterBomController@update` | Update master BOM | MBOM-owned |
| `masterbom.copy` | GET | `/masterbom/{id}/copy` | `MasterBomController@copy` | Copy master BOM | MBOM-owned |
| `masterbom.destroy` | DELETE | `/masterbom/{id}/destroy` | `MasterBomController@destroy` | Delete master BOM | MBOM-owned |
| `masterbom.addmore` | GET | `/masterbom/addmore` | `MasterBomController@addmore` | AJAX add item row | MBOM-owned |
| `masterbom.remove` | GET | `/masterbom/remove` | `MasterBomController@remove` | AJAX remove item | MBOM-owned |
| `masterbom.getsubcategory` | GET | `/masterbom/getsubcategory/{id}` | `MasterBomController@getsubcategory` | AJAX catalog lookup | COMPAT (S4 migration) |
| `masterbom.getproducttype` | GET | `/masterbom/getproducttype/{id}` | `MasterBomController@getproducttype` | AJAX catalog lookup | COMPAT (S4 migration) |
| `masterbom.getdescription` | GET | `/masterbom/getdescription` | `MasterBomController@getdescription` | AJAX catalog lookup | COMPAT (S4 migration) |

### 7.2 QUO-owned apply routes (QuotationV2Controller)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.v2.applyMasterBom` | POST | `/quotation/v2/apply-master-bom` | `QuotationV2Controller@applyMasterBom` | Apply master BOM to quotation | QUO-owned (PROTECTED) |
| `quotation.v2.masterbomView` | GET | `/quotation/v2/masterbom-view` | `QuotationV2Controller@getMasterBomView` | Get master BOM view data | QUO-owned |

### 7.3 SHARED-owned reuse routes (ReuseController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `api.reuse.masterBoms` | GET | `/api/reuse/master-boms` | `ReuseController@searchMasterBoms` | Search master BOMs for reuse | SHARED-owned (future) |

### 7.4 Legacy QUO routes (QuotationController — compat only)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.getMasterBom` | GET | `/quotation/getMasterBom` | `QuotationController@getMasterBom` | Legacy master BOM lookup | COMPAT (legacy) |
| `quotation.getMultipleMasterBom` | GET | `/quotation/getMultipleMasterBom` | `QuotationController@getMultipleMasterBom` | Legacy multi-BOM lookup | COMPAT (legacy) |
| `quotation.getMasterBomVal` | GET | `/quotation/getMasterBomVal` | `QuotationController@getMasterBomVal` | Legacy BOM value (HTML) | COMPAT (legacy) |
| `quotation.masterbomremove` | POST | `/quotation/masterbomremove` | `QuotationController@masterbomremove` | Legacy BOM removal | COMPAT (legacy) |

**Note:** Legacy routes are inventory-only in S2; removal happens only after S4 propagation + S5 Bundle-C pass.

---

## 8) Forbidden Callers (hard fence for Phase-4)

### 8.1 Modules forbidden from calling MBOM directly

**Rule:** The following modules **must not** call MBOM ORM models or internal services directly:

- **QUO (Legacy + V2):** Must use `quotation.v2.applyMasterBom` wrapper endpoint only
- **FEED:** Must use QUO apply wrapper (feeder templates are MasterBOMs with `TemplateType='FEEDER'`)
- **PBOM:** Must use QUO apply wrapper (proposal reuse is QUO-owned)
- **SHARED:** Must use `MasterBomTemplateReadContract` (when implemented) or reuse search endpoints

### 8.2 Forbidden direct access patterns

**Forbidden:**
- `App\Models\MasterBom::find($id)` from QUO/FEED/PBOM code
- `App\Models\MasterBomItem::where('MasterBomId', $id)->get()` from QUO/FEED/PBOM code
- Direct `MasterBomController` method calls from other controllers
- Bypassing `quotation.v2.applyMasterBom` to create quotation items directly

**Allowed:**
- HTTP calls to `quotation.v2.applyMasterBom` endpoint
- HTTP calls to `api.reuse.masterBoms` endpoint (SHARED contract)
- Future: `MasterBomTemplateReadContract` interface calls (S4+)

### 8.3 MBOM forbidden from calling

**Rule:** MBOM **must not** call:

- QUO models/services (except via `MasterBomUsageContract` for delete guard)
- FEED models/services
- PBOM models/services
- QUO costing/quantity services
- QUO controllers (except via HTTP wrapper endpoints)

**Current exception (to be fixed in S4):**
- `MasterBomController@destroy` directly queries `QuotationSaleBom` (forbidden coupling)
- **Fix:** Replace with `MasterBomUsageContract` call in S4

---

## 9) Apply Semantics (qty, reuse, origin tracking, no side effects)

### 9.1 Quantity multiplier semantics

**Contract rule:** The `Qty` parameter in `quotation.v2.applyMasterBom` is a **multiplier**, not an absolute quantity.

**Behavior (frozen in S2):**
- Each `MasterBomItem.Quantity` is multiplied by `Qty` when creating `QuotationSaleBomItem`
- UI must supply multiplier; apply endpoint owns quantity math
- No pre-multiplication in UI callers (explicitly forbidden)

**Example:**
- Template item: `Quantity = 2.0`
- Apply request: `Qty = 3.0`
- Result: `QuotationSaleBomItem.Quantity = 6.0`

### 9.2 Reuse detection and origin tracking

**Contract rule:** Apply endpoint must set origin tracking fields to enable reuse detection.

**Fields set by apply (observed):**
- `QuotationSaleBom.OriginMasterBomId` = `MasterBomId`
- `QuotationSaleBom.MasterBomId` = `MasterBomId` (reference)
- `QuotationSaleBom.MasterBomName` = `MasterBom.Name` (denormalized)
- `QuotationSaleBom.InstanceSequenceNo` = calculated sequence (1, 2, 3... per quotation)
- `QuotationSaleBomItem.OriginMasterBomItemId` = `MasterBomItemId` (if applicable)

**Reuse detection:**
- Multiple applications of the same `MasterBomId` to the same `QuotationId` are tracked via `InstanceSequenceNo`
- Reuse search (`api.reuse.masterBoms`) can query by `OriginMasterBomId` to find all instances

### 9.3 No side effects rule

**Contract rule:** Apply operation must not mutate MBOM template data.

**Guarantees:**
- `MasterBom` / `MasterBomItem` rows are **never modified** by apply
- Apply creates new `QuotationSaleBom` / `QuotationSaleBomItem` rows only
- Template remains immutable and reusable

**Exception (record only, not to fix in S2):**
- If `Items` array is provided in request, apply uses request payload instead of loading from `MasterBomItem`
- This is a UI materialization path; template data is not mutated

### 9.4 B4 resolution status handling

**Contract rule:** Apply must handle L0/L1 items correctly (B4 constraint: `ProductId = NULL` for L0/L1).

**Current behavior (record only):**
- If `Items` array is provided: apply uses request payload (UI materialized items)
- If `Items` array is absent: apply loads `MasterBomItem` rows and attempts to resolve `Product` via `ProductId`
- **Risk:** L0/L1 items with `ProductId = NULL` are skipped in fallback path

**Discipline:** This is a known risk (see Section 5); fix requires QUO-V2 re-verification (G4).

---

## 10) S4 Propagation Hooks (declared, not executed)

### 10.1 Contract propagation targets

**Target 1: MasterBomTemplateReadContract implementation**
- **Owner:** MBOM
- **Consumers:** QUO apply, FEED operations, PBOM operations, reuse search
- **S4 Task:** `NSW-P4-S4-MBOM-001` — Propagate MBOM apply contract to V2

**Target 2: MasterBomUsageContract implementation**
- **Owner:** QUO (or SHARED if standardized)
- **Consumer:** MBOM delete guard
- **S4 Task:** Replace direct `QuotationSaleBom` query in `MasterBomController@destroy`

**Target 3: CatalogLookupContract migration**
- **Owner:** SHARED
- **Consumers:** MBOM UI (create/edit forms)
- **S4 Task:** `NSW-P4-S4-SHARED-001` — Migrate MBOM catalog lookup endpoints

### 10.2 Route migration targets

**Target 1: MBOM catalog lookup routes → CatalogLookupContract**
- `masterbom.getsubcategory` → Remove after S4 migration
- `masterbom.getproducttype` → Remove after S4 migration
- `masterbom.getdescription` → Remove after S4 migration

**Target 2: Legacy QUO routes → Deprecation**
- `quotation.getMasterBom` → Remove after S5 Bundle-C pass
- `quotation.getMultipleMasterBom` → Remove after S5 Bundle-C pass
- `quotation.getMasterBomVal` → Remove after S5 Bundle-C pass
- `quotation.masterbomremove` → Remove after S5 Bundle-C pass

### 10.3 Wrapper adoption targets

**Target 1: QUO apply wrapper adoption**
- **Current:** Direct HTTP calls to `quotation.v2.applyMasterBom`
- **Future:** Adopt wrapper interface (when `NSW-P4-S2-QUO-002` completes)

**Target 2: Reuse search wrapper adoption**
- **Current:** Direct HTTP calls to `api.reuse.masterBoms`
- **Future:** Adopt `ReuseSearchContract` (when `NSW-P4-S2-SHARED-001` completes)

---

## 11) References (Authority)

**Authority Documents:**
- `trace/phase_2/FILE_OWNERSHIP.md` (MasterBomController ownership)
- `trace/phase_2/ROUTE_MAP.md` (MBOM routes inventory)
- `docs/PHASE_4/S2_GOV_BOUNDARY_BLOCKS.md` (MBOM boundary rules)
- `docs/PHASE_4/S2_GOV_EXCEPTION_TASK_MAPPING.md` (Exception mapping)
- `docs/PHASE_4/S2_CIM_ISOLATION.md` (Catalog lookup contract pattern)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (CatalogLookupContract + ReuseSearchContract)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (S2 fences + order)
- `features/master_bom/_general/09_BOM_MODULE.md` (MBOM module overview)
- `features/master_bom/_general/MASTER_BOM_VS_PROPOSAL_BOM_SPECIFICATION.md` (BOM comparison)

**Code Anchors:**
- `source_snapshot/app/Http/Controllers/MasterBomController.php` (MBOM CRUD)
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyMasterBom` (QUO apply)
- `source_snapshot/app/Http/Controllers/ReuseController.php@searchMasterBoms` (Reuse search)
- `source_snapshot/routes/web.php` (Route definitions)

---

## 12) Evidence / Approvals Checklist (G3)

- [x] Architectural approval: MBOM read/apply boundary + forbidden coupling statements accepted
- [x] Execution approval: planning-only; no behavior change; no QUO‑V2 scope crossed beyond contract naming
- [x] Adapter seam acceptance: `MasterBomTemplateReadContract` + `MasterBomUsageContract` recorded as the only approved future refactor seams
- [x] Routes inventory: All MBOM routes classified (MBOM-owned, QUO-owned, SHARED-owned, COMPAT)
- [x] Forbidden callers: Hard fence documented for all modules
- [x] Apply semantics: Quantity multiplier, reuse tracking, no side effects documented
- [x] S4 propagation hooks: Contract migration targets declared

---

## Task Status

- **NSW-P4-S2-MBOM-001:** ✅ Complete
- **Next Task:** NSW-P4-S2-FEED-001 (Feeder template interface contract)

---

**Last Updated:** 2025-12-18  
**Status:** ✅ Complete — Ready for S3 alignment


