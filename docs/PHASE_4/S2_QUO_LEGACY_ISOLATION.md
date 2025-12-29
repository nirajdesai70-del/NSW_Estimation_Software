# S2.6 — QUO Legacy Isolation Pack (Legacy Surface + Consumption Map)
#
# Task coverage:
# - NSW-P4-S2-QUO-LEGACY-001 (G3) Quotation Legacy boundary isolation (planning-only)
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase‑4 execution.
- **Legacy QUO only**: identify and bound the **legacy quotation** surface.
- **No code moves**.
- **No logic fixes**.
- **No apply behavior changes** (MBOM/FEED/PBOM apply behavior is frozen in S2).
- **No QUO‑V2 execution or edits**:
  - Do **not** touch `QuotationV2Controller` or any V2 apply behavior.
  - QUO‑V2 remains fenced behind `NSW-P4-S2-QUO-REVERIFY-001` (G4).
- This artifact records: **surface inventory, consumption map, hard boundaries, forbidden couplings, known risks, adapter seam notes**.

---

## 1) Legacy QUO Surface (routes + controllers)

### 1.1 Main legacy quotation routes (`quotation.*`)

**Routes file:** `source_snapshot/routes/web.php`  
**Primary controller:** `source_snapshot/app/Http/Controllers/QuotationController.php`

Core legacy CRUD + workflow:

- `quotation.index` → `GET /quotation` → `QuotationController@index`
- `quotation.bom-list` → `GET /quotation/bom-list` → `QuotationController@bomList`
- `quotation.create` → `GET /quotation/create` → `QuotationController@create`
- `quotation.store` → `POST /quotation/create` → `QuotationController@store`
- `quotation.edit` → `GET /quotation/{id}/edit` → `QuotationController@edit`
- `quotation.update` → `PUT /quotation/{id}/edit` → `QuotationController@update`
- `quotation.destroy` → `DELETE /quotation/{id}/destroy` → `QuotationController@destroy`
- `quotation.step` → `GET /quotation/{id}/step` → `QuotationController@step`
- `quotation.step.panel` → `GET /quotation/{quotation}/step/panel/{panel}` → `QuotationController@stepPanel`
- `quotation.stepupdate` → `PUT /quotation/{id}/step` → `QuotationController@stepupdate`
- `quotation.updateSaleData` → `PUT /quotation/{id}/updateSaleData` → `QuotationController@updateSaleData`

Exports:

- `quotation.pdf` → `GET /quotation/pdf/{id}` → `QuotationController@pdf`
- `quotation.excel` → `GET /quotation/excel/{id}` → `QuotationController@excel`

### 1.2 Legacy quotation “helper/AJAX” endpoints (HTML + partial hydration)

These routes are legacy QUO internals but are consumed by UI flows (and some V2 UI compatibility paths):

- `quotation.getMasterBom` → `GET /quotation/getMasterBom` → `QuotationController@getMasterBom`
- `quotation.getMultipleMasterBom` → `GET /quotation/getMultipleMasterBom` → `QuotationController@getMultipleMasterBom`
- `quotation.getMasterBomVal` → `GET /quotation/getMasterBomVal` → `QuotationController@getMasterBomVal` (returns `quotation.item` HTML)
- `quotation.getProposalBomVal` → `GET /quotation/getProposalBomVal` → `QuotationController@getProposalBomVal` (returns `quotation.item` HTML)
- `quotation.getSingleVal` → `GET /quotation/getSingleVal` → `QuotationController@getSingleVal` (returns `quotation.item` HTML)
- `quotation.masterbomremove` → `POST /quotation/masterbomremove` → `QuotationController@masterbomremove`
- `quotation.itemremove` → `POST /quotation/itemremove` → `QuotationController@itemremove`

### 1.3 QUO-adjacent subsystems under quotation namespace (record-only)

Discount rules surfaces exist under:

- `quotation-discount-rules/*` (test endpoints; temporary)
- `quotations/{quotation_id}/discount-rules/*` (CRUD + apply/reset + lookup)

**Discipline:** Included here for awareness only; no changes in S2.

---

## 2) Consumption Map (what legacy QUO serves + what it consumes)

### 2.1 SHARED contract endpoints currently implemented inside legacy QUO

Legacy QUO is currently the **implementation host** of SHARED dropdown endpoints (see `docs/PHASE_4/S2_SHARED_ISOLATION.md`):

- **CatalogLookupContract** routes under `/api/*` implemented by `QuotationController`:
  - `/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*`, `/api/makes`

Legacy QUO is also the host (via `ReuseController`) of reuse search endpoints:

- `/api/reuse/panels`
- `/api/reuse/feeders`
- `/api/reuse/master-boms`
- `/api/reuse/proposal-boms`

**Important:** Legacy QUO therefore acts as both:

- **A consumer** of catalog data (via CIM tables/models)
- **A shared API server** for other modules

### 2.2 CIM catalog consumption (direct model access — current reality)

`QuotationController` directly imports and queries CIM-owned tables/models for:

- Category/Subcategory/Item/Product resolution
- Make/Series/Description selection
- Pricelist lookup for rates

**Discipline:** This is recorded as current coupling; target state is contract-first access via SHARED contracts.

### 2.3 Template system consumption (MBOM / PBOM / FEED)

#### MBOM (Master BOM) — legacy consumption

Legacy QUO consumes MBOM templates via direct model reads and legacy helper routes:

- `QuotationController@getMasterBomVal` reads:
  - `MasterBomItem` (items by `MasterBomId`)
  - `Product` (to populate dropdown selections)
- Legacy “apply” is performed via the legacy item UI path (HTML returned from `quotation.item`) and subsequent save/update flows.

#### PBOM (Proposal BOM) — legacy consumption + selection

Legacy QUO consumes proposal BOM content via:

- `QuotationController@getProposalBomVal` reading `QuotationSaleBom`/`QuotationSaleBomItem` and catalog tables for dropdown hydration (returns HTML)

Legacy QUO also provides a search endpoint used by V2 selection UI:

- `api.proposalBom.search` → `GET /api/proposal-bom/search?q=term` → `QuotationController@searchProposalBom`

#### FEED (Feeder Library) — legacy status

- Feeder templates are managed under `/feeder-library/*` (FEED module) and applied via `quotation.v2.applyFeederTemplate` (V2 apply surface).
- Legacy QUO does not have a dedicated “apply feeder template” surface in this snapshot; treat FEED apply as **V2-only** for S2 purposes.

#### QUO apply entrypoints (recorded for boundary completeness; fenced)

Existing apply entrypoints (implementation fenced; do not change in S2):

- `quotation.v2.applyMasterBom` → `POST /quotation/v2/apply-master-bom`
- `quotation.v2.applyFeederTemplate` → `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template` (**re-verify required**, G4)
- `quotation.v2.applyProposalBom` → `POST /quotation/v2/apply-proposal-bom`

---

## 3) Hard Boundary Statements (effective for Phase‑4 planning)

### 3.1 Legacy QUO integration rules (contract-first target)

- Legacy QUO **must consume** cross-module data via **documented contracts/routes** (HTTP surfaces) rather than direct model access (target state).
- Legacy QUO **must not** introduce new direct dependencies on:
  - CIM internal table structure
  - MBOM template internals
  - FEED/PBOM internals

### 3.2 QUO‑V2 fence (non-negotiable)

- Legacy QUO isolation work **must not** modify or depend on QUO‑V2 protected core.
- Any QUO‑V2 refactor, apply fixes, or controller alignment waits for `NSW-P4-S2-QUO-REVERIFY-001` (G4).

### 3.3 “Shared API host” separation target (no moves in S2)

- SHARED endpoints currently implemented in `QuotationController` should be split out (see `docs/PHASE_4/S2_SHARED_ISOLATION.md`) so that:
  - QUO legacy remains QUO-owned
  - SHARED contract endpoints are SHARED-owned

---

## 4) Forbidden Couplings (explicit)

### 4.1 Forbidden: QUO‑V2 protected core changes

- Do not edit `QuotationV2Controller` or V2 apply behavior.
- Do not edit QUO protected services/models (see `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md` for S1 no-go list).

### 4.2 Forbidden: new direct cross-module model/service imports

Legacy QUO must not introduce new direct imports/callers into:

- **MBOM protected templates**: `MasterBom`, `MasterBomItem` (recorded as currently imported; do not expand)
- **CIM internals** beyond contract surfaces (target state; do not expand)
- **SHARED protected services** (e.g. `DeletionPolicyService`) unless explicitly approved

---

## 5) Known Risks / Couplings (record only; do not fix in S2)

### QuotationController is a mixed-responsibility hub

`QuotationController` currently owns:

- Legacy quotation CRUD/workflow
- SHARED dropdown APIs (`/api/*`)
- PBOM search API (`/api/proposal-bom/search`)
- Legacy template hydration endpoints returning HTML (`quotation/get*Val`)

This creates a high change-risk surface for Phase‑4 execution if not carefully isolated via seams.

### Legacy HTML hydration endpoints are used as compatibility utilities

Endpoints like:

- `quotation.getMasterBomVal`
- `quotation.getProposalBomVal`
- `quotation.getSingleVal`

return HTML intended for legacy UI, but are also referenced by V2 UI code paths as fallbacks. This creates a legacy↔V2 coupling that must be handled carefully during future propagation.

### SHARED “API” endpoints live in `routes/web.php`

The `/api/*` contract endpoints are registered under `routes/web.php` rather than `routes/api.php` in this snapshot. Route relocation is out of scope for S2.

---

## 6) Adapter Seam Notes (planning-only; no execution leakage)

### 6.1 Controller split seam (already identified in S2.1 SHARED)

**Seam goal:** reduce risk by extracting shared API method groups out of `QuotationController`:

- `CatalogLookupController` (SHARED owner; implements CatalogLookupContract)
- `QuotationController` (QUO owner; legacy quotation flows only)

### 6.2 Legacy template hydration seam

**Contract name:** `LegacyQuotationTemplateHydrationContract`  
**Owner:** QUO (legacy)  
**Consumers:** legacy step UI; any compatibility caller  
**Purpose:** provide a stable interface for “template → editable item form payload” while decoupling UI rendering from direct model access over time

### 6.3 Export seam

**Contract name:** `QuotationLegacyExportContract`  
**Owner:** QUO (legacy)  
**Consumers:** PDF/Excel export actions  
**Purpose:** isolate export generation dependencies for safer future refactors

---

## 7) Legacy QUO Routes Inventory (authoritative; current implementation reality)

### 7.1 Legacy QUO-owned CRUD routes (QuotationController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.index` | GET | `/quotation` | `QuotationController@index` | List quotations | QUO-owned (legacy) |
| `quotation.bom-list` | GET | `/quotation/bom-list` | `QuotationController@bomList` | List BOMs | QUO-owned (legacy) |
| `quotation.create` | GET | `/quotation/create` | `QuotationController@create` | Show create form | QUO-owned (legacy) |
| `quotation.store` | POST | `/quotation/create` | `QuotationController@store` | Create quotation | QUO-owned (legacy) |
| `quotation.edit` | GET | `/quotation/{id}/edit` | `QuotationController@edit` | Show edit form | QUO-owned (legacy) |
| `quotation.update` | PUT | `/quotation/{id}/edit` | `QuotationController@update` | Update quotation | QUO-owned (legacy) |
| `quotation.destroy` | DELETE | `/quotation/{id}/destroy` | `QuotationController@destroy` | Delete quotation | QUO-owned (legacy) |
| `quotation.step` | GET | `/quotation/{id}/step` | `QuotationController@step` | Step workflow | QUO-owned (legacy) |
| `quotation.step.panel` | GET | `/quotation/{quotation}/step/panel/{panel}` | `QuotationController@stepPanel` | Panel step | QUO-owned (legacy) |
| `quotation.stepupdate` | PUT | `/quotation/{id}/step` | `QuotationController@stepupdate` | Update step | QUO-owned (legacy) |
| `quotation.updateSaleData` | PUT | `/quotation/{id}/updateSaleData` | `QuotationController@updateSaleData` | Update sale data | QUO-owned (legacy) |
| `quotation.pdf` | GET | `/quotation/pdf/{id}` | `QuotationController@pdf` | PDF export | QUO-owned (legacy) |
| `quotation.excel` | GET | `/quotation/excel/{id}` | `QuotationController@excel` | Excel export | QUO-owned (legacy) |
| `quotation.audit-logs` | GET | `/quotation/{id}/audit-logs` | `QuotationController@auditLogs` | Audit logs | QUO-owned (legacy) |

### 7.2 Legacy QUO helper/AJAX routes (QuotationController — compat)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.getMasterBom` | GET | `/quotation/getMasterBom` | `QuotationController@getMasterBom` | Get master BOM (legacy) | COMPAT (legacy) |
| `quotation.getMultipleMasterBom` | GET | `/quotation/getMultipleMasterBom` | `QuotationController@getMultipleMasterBom` | Get multiple master BOMs | COMPAT (legacy) |
| `quotation.getMasterBomVal` | GET | `/quotation/getMasterBomVal` | `QuotationController@getMasterBomVal` | Get master BOM HTML | COMPAT (legacy) |
| `quotation.getProposalBomVal` | GET | `/quotation/getProposalBomVal` | `QuotationController@getProposalBomVal` | Get proposal BOM HTML | COMPAT (legacy) |
| `quotation.getSingleVal` | GET | `/quotation/getSingleVal` | `QuotationController@getSingleVal` | Get single item HTML | COMPAT (legacy) |
| `quotation.masterbomremove` | POST | `/quotation/masterbomremove` | `QuotationController@masterbomremove` | Remove master BOM | COMPAT (legacy) |
| `quotation.itemremove` | POST | `/quotation/itemremove` | `QuotationController@itemremove` | Remove item | COMPAT (legacy) |
| `quotation.addmore` | GET | `/quotation/addmore` | `QuotationController@addmore` | Add more items | COMPAT (legacy) |
| `quotation.remove` | GET | `/quotation/remove` | `QuotationController@remove` | Remove item | COMPAT (legacy) |
| `quotation.contact` | GET | `/quotation/contact` | `QuotationController@contact` | Contact info | COMPAT (legacy) |
| `quotation.getmake` | GET | `/quotation/getmake/{id}` | `QuotationController@getmake` | Get make | COMPAT (legacy) |
| `quotation.getseries` | GET | `/quotation/getseries/{id}` | `QuotationController@getseries` | Get series | COMPAT (legacy) |

### 7.3 SHARED contract routes (currently implemented in QuotationController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `api.category.subcategories` | GET | `/api/category/{categoryId}/subcategories` | `QuotationController@getSubCategories` | Catalog lookup | SHARED-owned (future) |
| `api.category.items` | GET | `/api/category/{categoryId}/items` | `QuotationController@getItems` | Catalog lookup | SHARED-owned (future) |
| `api.category.products` | GET | `/api/category/{categoryId}/products` | `QuotationController@getProducts` | Catalog lookup | SHARED-owned (future) |
| `api.item.products` | GET | `/api/item/{itemId}/products` | `QuotationController@getProductsByItem` | Catalog lookup | SHARED-owned (future) |
| `api.product.makes` | GET | `/api/product/{productId}/makes` | `QuotationController@getMakes` | Catalog lookup | SHARED-owned (future) |
| `api.make.series` | GET | `/api/make/{makeId}/series` | `QuotationController@getSeriesApi` | Catalog lookup | SHARED-owned (future) |
| `api.product.descriptions` | GET | `/api/product/{productId}/descriptions` | `QuotationController@getDescriptions` | Catalog lookup | SHARED-owned (future) |
| `api.category.makes` | GET | `/api/category/{categoryId}/makes` | `QuotationController@getMakesByCategory` | Catalog lookup | SHARED-owned (future) |
| `api.makes` | GET | `/api/makes` | `QuotationController@getAllMakes` | Catalog lookup | SHARED-owned (future) |
| `api.proposalBom.search` | GET | `/api/proposal-bom/search` | `QuotationController@searchProposalBom` | Proposal BOM search | SHARED-owned (future) |

**Note:** These routes are currently implemented in `QuotationController` but are target-owned by SHARED. Migration happens in S4 (see `docs/PHASE_4/S2_SHARED_ISOLATION.md`).

### 7.4 SHARED reuse routes (currently implemented in ReuseController)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `api.reuse.panels` | GET | `/api/reuse/panels` | `ReuseController@searchPanels` | Reuse search | SHARED-owned (future) |
| `api.reuse.feeders` | GET | `/api/reuse/feeders` | `ReuseController@searchFeeders` | Reuse search | SHARED-owned (future) |
| `api.reuse.masterBoms` | GET | `/api/reuse/master-boms` | `ReuseController@searchMasterBoms` | Reuse search | SHARED-owned (future) |
| `api.reuse.proposalBoms` | GET | `/api/reuse/proposal-boms` | `ReuseController@searchProposalBoms` | Reuse search | SHARED-owned (future) |

**Note:** These routes are currently implemented in `ReuseController` but are target-owned by SHARED. Migration happens in S4.

### 7.5 QUO V2 routes (fenced — no changes in S2)

| Route Name | Method | URI | Controller Method | Purpose | Classification |
|------------|--------|-----|-------------------|---------|----------------|
| `quotation.v2.index` | GET | `/quotation/{id}/v2` | `QuotationV2Controller@index` | V2 panel list | QUO-owned (PROTECTED) |
| `quotation.v2.applyMasterBom` | POST | `/quotation/v2/apply-master-bom` | `QuotationV2Controller@applyMasterBom` | Apply master BOM | QUO-owned (PROTECTED) |
| `quotation.v2.applyFeederTemplate` | POST | `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | `QuotationV2Controller@applyFeederTemplate` | Apply feeder template | QUO-owned (PROTECTED) |
| `quotation.v2.applyProposalBom` | POST | `/quotation/v2/apply-proposal-bom` | `QuotationV2Controller@applyProposalBom` | Apply proposal BOM | QUO-owned (PROTECTED) |

**Note:** V2 routes are fenced and require G4 re-verification (`NSW-P4-S2-QUO-REVERIFY-001`) before any changes.

---

## 8) Forbidden Callers (hard fence for Phase-4)

### 8.1 Modules forbidden from calling legacy QUO directly

**Rule:** The following modules **must not** call legacy QUO ORM models or internal services directly:

- **CIM:** Must use `CatalogLookupContract` (when implemented) instead of direct `QuotationController` catalog methods
- **MBOM:** Must use `quotation.v2.applyMasterBom` wrapper endpoint only (V2 apply)
- **FEED:** Must use `quotation.v2.applyFeederTemplate` wrapper endpoint only (V2 apply)
- **PBOM:** Must use `quotation.v2.applyProposalBom` wrapper endpoint only (V2 apply)
- **SHARED:** Must not depend on legacy QUO internals (target: extract shared endpoints to SHARED module)

### 8.2 Forbidden direct access patterns

**Forbidden:**
- Direct `QuotationController` method calls from other controllers (except via HTTP routes)
- Direct `QuotationSaleBom` / `QuotationSaleBomItem` queries from MBOM/FEED/PBOM code
- Bypassing apply endpoints to mutate quotation structures directly
- Direct access to legacy QUO costing/quantity services from other modules

**Allowed:**
- HTTP calls to documented apply endpoints (`quotation.v2.applyMasterBom`, etc.)
- HTTP calls to catalog lookup endpoints (`/api/category/*`, etc.) — until migrated to SHARED
- Future: `CatalogLookupContract` interface calls (S4+)
- Future: `ReuseSearchContract` interface calls (S4+)

### 8.3 Legacy QUO forbidden from calling

**Rule:** Legacy QUO **must not** call:

- V2 protected services/models (QUO-V2 is fenced)
- MBOM models/services (except via documented routes/contracts)
- FEED models/services (except via documented routes/contracts)
- PBOM models/services (except via documented routes/contracts)

**Current exception (to be fixed in S4):**
- `QuotationController` directly queries CIM models (`Category`, `SubCategory`, `Item`, `Product`, etc.)
- **Fix:** Migrate to `CatalogLookupContract` in S4

---

## 9) S4 Propagation Hooks (declared, not executed)

### 9.1 Contract propagation targets

**Target 1: CatalogLookupContract migration**
- **Owner:** SHARED
- **Current:** Implemented in `QuotationController` (`/api/category/*`, `/api/item/*`, etc.)
- **Target:** Extract to `SHARED/CatalogLookupController`
- **S4 Task:** `NSW-P4-S4-SHARED-001` — Propagate CatalogLookupContract to consumers
- **S4 Task:** `NSW-P4-S4-QUO-001` — Migrate legacy quotation to SHARED + BOM contracts

**Target 2: ReuseSearchContract migration**
- **Owner:** SHARED
- **Current:** Implemented in `ReuseController` (`/api/reuse/*`)
- **Target:** Extract to `SHARED/ReuseSearchController`
- **S4 Task:** `NSW-P4-S4-SHARED-002` — Propagate ReuseSearchContract to consumers

**Target 3: Legacy template hydration contract**
- **Owner:** QUO (legacy)
- **Consumer:** Legacy step UI, V2 compatibility paths
- **S4 Task:** Implement `LegacyQuotationTemplateHydrationContract` to decouple UI rendering

### 9.2 Route migration targets

**Target 1: SHARED catalog lookup routes → SHARED module**
- All `/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*` routes → Move to SHARED controller
- `api.proposalBom.search` → Move to SHARED or PBOM module

**Target 2: SHARED reuse search routes → SHARED module**
- All `/api/reuse/*` routes → Move to SHARED controller

**Target 3: Legacy helper routes → Deprecation**
- `quotation.getMasterBom` → Remove after S5 Bundle-C pass
- `quotation.getMultipleMasterBom` → Remove after S5 Bundle-C pass
- `quotation.getMasterBomVal` → Remove after S5 Bundle-C pass
- `quotation.getProposalBomVal` → Remove after S5 Bundle-C pass
- `quotation.getSingleVal` → Remove after S5 Bundle-C pass
- `quotation.masterbomremove` → Remove after S5 Bundle-C pass

### 9.3 Controller split targets

**Target 1: Extract CatalogLookupController**
- **From:** `QuotationController` (catalog lookup methods)
- **To:** `SHARED/CatalogLookupController`
- **S4 Task:** `NSW-P4-S4-SHARED-001`

**Target 2: Extract ReuseSearchController**
- **From:** `ReuseController` (reuse search methods)
- **To:** `SHARED/ReuseSearchController`
- **S4 Task:** `NSW-P4-S4-SHARED-002`

**Target 3: Clean QuotationController**
- **After splits:** `QuotationController` contains only legacy quotation CRUD/workflow
- **Result:** Reduced change-risk surface for Phase-4 execution

---

## 10) References (Authority)

**Authority Documents:**
- `trace/phase_2/FILE_OWNERSHIP.md` (QuotationController ownership)
- `trace/phase_2/ROUTE_MAP.md` (Legacy QUO routes inventory)
- `docs/PHASE_4/S2_GOV_BOUNDARY_BLOCKS.md` (QUO boundary rules)
- `docs/PHASE_4/S2_GOV_EXCEPTION_TASK_MAPPING.md` (Exception mapping)
- `docs/PHASE_4/S2_SHARED_ISOLATION.md` (CatalogLookupContract + ReuseSearchContract)
- `docs/PHASE_4/S2_MBOM_ISOLATION.md` (MBOM apply contract)
- `docs/PHASE_4/S2_FEED_ISOLATION.md` (FEED apply contract)
- `docs/PHASE_4/S2_PBOM_ISOLATION.md` (PBOM apply contract)
- `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md` (S2 fences + order)
- `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md` (QUO-V2 fence rules)

**Code Anchors:**
- `source_snapshot/app/Http/Controllers/QuotationController.php` (Legacy QUO CRUD)
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php` (V2 QUO — PROTECTED, fenced)
- `source_snapshot/app/Http/Controllers/ReuseController.php` (Reuse search — future SHARED)
- `source_snapshot/routes/web.php` (Route definitions)

---

## 11) Evidence / Approvals Checklist (G3)

- [x] Architectural approval: legacy QUO surface + consumption map accepted
- [x] Execution approval: planning-only; no behavior change; QUO‑V2 fence maintained
- [x] Adapter seam acceptance: split/hydration/export seams recorded (planning-only)
- [x] Routes inventory: All legacy QUO routes classified (QUO-owned, SHARED-owned, COMPAT)
- [x] Forbidden callers: Hard fence documented for all modules
- [x] Consumption map: Legacy QUO serves SHARED endpoints + consumes CIM/MBOM/PBOM documented
- [x] S4 propagation hooks: Contract migration targets declared

---

## Task Status

- **NSW-P4-S2-QUO-001:** ✅ Complete
- **Next Stage:** S3 — Alignment (contract freeze)

---

**Last Updated:** 2025-12-18  
**Status:** ✅ Complete — Ready for S3 alignment


