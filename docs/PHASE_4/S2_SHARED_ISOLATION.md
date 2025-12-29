# S2.1 — SHARED Isolation Pack (Contracts + Split Plan)
#
# Task coverage:
# - NSW-P4-S2-SHARED-001 (G3) Shared utilities contract
# - NSW-P4-S2-SHARED-002 (G3) Shared controller split plan (no moves)
#
# Status: ACTIVE (Execution Support)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document is **planning-only isolation** for Phase-4 execution.
- **No QUO‑V2 work** is authorized here (fenced by `NSW-P4-S2-QUO-REVERIFY-001`, G4).
- No functional changes are proposed; only **contracts, boundaries, and split plans**.

---

## 1) Contract: CatalogLookupContract (Shared Dropdown APIs)

### Current reality (trace + code anchor)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`, `trace/phase_2/ROUTE_MAP.md`

These endpoints are "shared" (consumed by Legacy + V2), but currently implemented inside **Quotation**:

**From FILE_OWNERSHIP.md:**
- `source_snapshot/app/Http/Controllers/QuotationController.php` | Controller | Quotation | Legacy | HIGH | Legacy quotation workflow; widely used | Review required | `quotation.*` (Legacy), `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*` (Shared APIs)
- `source_snapshot/routes/api.php` | Route File | Quotation | Shared APIs | HIGH | Contains throttled search APIs used by Quotation (Legacy+V2) | Review + verify throttling | `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.reuse.*`

**From ROUTE_MAP.md (Shared catalog lookup routes):**
- `GET /api/category/{categoryId}/subcategories` → `api.category.subcategories` → `QuotationController@getSubCategories` | Quotation | Shared (Legacy+V2)
- `GET /api/category/{categoryId}/items` → `api.category.items` → `QuotationController@getItems` | Quotation | Shared (Legacy+V2)
- `GET /api/category/{categoryId}/products` → `api.category.products` → `QuotationController@getProducts` | Quotation | Shared (Legacy+V2)
- `GET /api/item/{itemId}/products` → `api.item.products` → `QuotationController@getProductsByItem` | Quotation | Shared (Legacy+V2)
- `GET /api/product/{productId}/makes` → `api.product.makes` → `QuotationController@getMakes` | Quotation | Shared (Legacy+V2)
- `GET /api/make/{makeId}/series` → `api.make.series` → `QuotationController@getSeriesApi` | Quotation | Shared (Legacy+V2)
- `GET /api/product/{productId}/descriptions` → `api.product.descriptions` → `QuotationController@getDescriptions` | Quotation | Shared (Legacy+V2)
- `GET /api/category/{categoryId}/makes` → `api.category.makes` → `QuotationController@getMakesByCategory` | Quotation | Shared (Legacy+V2)
- `GET /api/makes` → `api.makes` → `QuotationController@getAllMakes` | Quotation | Shared (Legacy+V2)

**Code anchors:**
- **Routes file**: `source_snapshot/routes/web.php` (in this snapshot, `/api/*` routes live under `routes/web.php` with `/api` prefix; treat this as canonical until S4)
- **Route group**: `Route::group(['middleware' => 'auth', 'prefix' => 'api'], function () { ... })`
- **Implementation controller**: `source_snapshot/app/Http/Controllers/QuotationController.php`

### In-scope endpoints (route name → URI → controller method)

- `api.category.subcategories` → `GET /api/category/{categoryId}/subcategories` → `QuotationController@getSubCategories`
- `api.category.items` → `GET /api/category/{categoryId}/items` → `QuotationController@getItems`
- `api.category.products` → `GET /api/category/{categoryId}/products` → `QuotationController@getProducts`
- `api.item.products` → `GET /api/item/{itemId}/products` → `QuotationController@getProductsByItem`
- `api.product.makes` → `GET /api/product/{productId}/makes` → `QuotationController@getMakes`
- `api.make.series` → `GET /api/make/{makeId}/series` → `QuotationController@getSeriesApi`
- `api.product.descriptions` → `GET /api/product/{productId}/descriptions` → `QuotationController@getDescriptions`
- `api.category.makes` → `GET /api/category/{categoryId}/makes` → `QuotationController@getMakesByCategory`
- `api.makes` → `GET /api/makes` → `QuotationController@getAllMakes`

### Contract inputs (canonical)

- Path params: `categoryId`, `itemId`, `productId`, `makeId` (as applicable)
- Optional query: `search` / `term` (if present in UI; must be verified during live execution)

### Contract outputs (canonical response shape)

Return a list of stable option objects:

- `{ id: string|number, label: string }`

Optional (future, non-breaking) metadata:

- `{ meta?: { sourceVersion?: string, cacheTtlSeconds?: number } }`

### Error contract

**Standard HTTP status codes:**
- `200 OK`: Success (with data array, may be empty)
- `400 Bad Request`: Invalid path/query parameters (e.g., missing required `categoryId`)
- `401 Unauthorized`: Authentication required (auth middleware)
- `404 Not Found`: Resource not found (e.g., invalid categoryId)
- `500 Internal Server Error`: Server error

**Error response shape:**
- `{ error: string, message?: string }`

### Caching/lookup rules

**Current state (to be verified in execution):**
- No explicit caching contract defined (implementation may cache; contract does not guarantee it)
- Callers must not assume caching behavior

**Future contract extension (non-breaking):**
- Optional `cacheTtlSeconds` in response metadata
- Optional `cache-control` headers

### Logging requirements

**Contract requirement:**
- All catalog lookup requests must be logged for audit/debugging
- Log: route name, path params, query params (sanitized), response status
- No PII in logs (IDs only, not names/labels)

### Versioning rule

**Contract version:** v1 (frozen in S3)
**Versioning strategy:**
- Non-breaking additions (new optional fields) allowed
- Breaking changes require new route/version identifier
- Current routes remain v1 until explicit migration

### Forbidden coupling (enforced by SHARED contract)

- No module may rely on "extra" fields not declared by the contract.
- No caller may assume ORM field names from CIM tables.

### Consumer list (who must migrate in S4)

**Current consumers (to migrate to contract in S4):**
- CIM: Product create/edit pages (use `product.getsubcategory`, `product.getproducttype` → migrate to `CatalogLookupContract`)
- MBOM: BOM create/edit/copy pages (use `masterbom.getsubcategory`, `masterbom.getdescription` → migrate to `CatalogLookupContract`)
- FEED: Template operations (internal catalog lookups → migrate to `CatalogLookupContract`)
- PBOM: BOM operations (internal catalog lookups → migrate to `CatalogLookupContract`)
- QUO Legacy: Dropdown APIs (currently hosts, will consume after extraction)
- QUO V2: Dropdown APIs (currently hosts, will consume after extraction)

**S4 Migration Tasks:**
- NSW-P4-S4-CIM-001: Migrate CIM consumers
- NSW-P4-S4-MBOM-001: Migrate MBOM consumers  
- NSW-P4-S4-FEED-001: Migrate FEED consumers
- NSW-P4-S4-PBOM-001: Migrate PBOM consumers
- NSW-P4-S4-QUO-001: Migrate QUO legacy consumers
- NSW-P4-S4-QUO-002: Migrate QUO V2 consumers (via wrapper)

---

## 2) Contract: ReuseSearchContract (Shared Reuse Search APIs)

### Current reality (code anchor)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`, `trace/phase_2/ROUTE_MAP.md`

**From FILE_OWNERSHIP.md:**
- `source_snapshot/app/Http/Controllers/ReuseController.php` | Controller | Quotation | V2 | HIGH | Reuse search endpoints; cross-module + search perf sensitive | Review + perf testing | `api.reuse.*`

**From ROUTE_MAP.md (Shared reuse search routes):**
- `GET /api/reuse/panels` → `api.reuse.panels` → `ReuseController@searchPanels` | Quotation | V2
- `GET /api/reuse/feeders` → `api.reuse.feeders` → `ReuseController@searchFeeders` | Quotation | V2
- `GET /api/reuse/master-boms` → `api.reuse.masterBoms` → `ReuseController@searchMasterBoms` | Quotation | V2
- `GET /api/reuse/proposal-boms` → `api.reuse.proposalBoms` → `ReuseController@searchProposalBoms` | Quotation | V2

**Code anchors:**
- Reuse search routes live in `source_snapshot/routes/web.php` (in this snapshot, `/api/*` routes live under `routes/web.php` with `/api` prefix; treat this as canonical until S4)
- **Implementation controller**: `source_snapshot/app/Http/Controllers/ReuseController.php`

### Contract inputs (canonical)

- `searchTerm` (query)
- Optional filters (to be verified in live execution): `quotationId`, `panelId`, `type`, paging

### Contract outputs (canonical)

- `{ id: string|number, label: string, kind: 'panel'|'feeder'|'masterBom'|'proposalBom' }`

**Rules:**
- `kind` is required for routing UI actions safely without type inference
- Callers must ignore extra fields

### Error contract

**Standard HTTP status codes:**
- `200 OK`: Success (with data array, may be empty)
- `400 Bad Request`: Invalid query parameters (e.g., missing required `searchTerm`)
- `401 Unauthorized`: Authentication required (auth middleware)
- `500 Internal Server Error`: Server error

**Error response shape:**
- `{ error: string, message?: string }`

### Caching/lookup rules

**Current state (to be verified in execution):**
- Search performance may be throttled (`throttle:search` middleware)
- No explicit caching contract defined
- Callers must not assume caching behavior

**Future contract extension (non-breaking):**
- Optional paging parameters
- Optional result limits

### Logging requirements

**Contract requirement:**
- All reuse search requests must be logged for audit/debugging
- Log: route name, optional filters, response status, and searchTermLength (not full searchTerm)
- Never log raw searchTerm (PII protection)
- No PII in logs (IDs only, not names/labels)

### Versioning rule

**Contract version:** v1 (frozen in S3)
**Versioning strategy:**
- Non-breaking additions (new optional filters) allowed
- Breaking changes require new route/version identifier
- Current routes remain v1 until explicit migration

### Consumer list (who must migrate in S4)

**Current consumers (to migrate to contract in S4):**
- QUO V2: Reuse search UI (`api.reuse.*` → already using, will continue after extraction)
- MBOM: Internal reuse searches → migrate to `ReuseSearchContract`
- FEED: Internal reuse searches → migrate to `ReuseSearchContract`
- PBOM: Internal reuse searches → migrate to `ReuseSearchContract`

**S4 Migration Tasks:**
- NSW-P4-S4-MBOM-001: Migrate MBOM reuse consumers
- NSW-P4-S4-FEED-001: Migrate FEED reuse consumers
- NSW-P4-S4-PBOM-001: Migrate PBOM reuse consumers
- NSW-P4-S4-QUO-001: Ensure QUO V2 continues using contract after extraction

---

## 3) Shared Controller Split Plan (no moves yet)

### 3.1 Candidate: `QuotationController` (mixed responsibility)

**Authority:** `trace/phase_2/FILE_OWNERSHIP.md`

**From FILE_OWNERSHIP.md:**
- `source_snapshot/app/Http/Controllers/QuotationController.php` | Controller | Quotation | Legacy | HIGH | Legacy quotation workflow; widely used | Review required | `quotation.*` (Legacy), `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*` (Shared APIs)

**Problem:** One controller owns both:
- Quotation legacy flow (QUO-owned)
- Cross-module dropdown APIs (should become SHARED contract surface)

**Split plan (Phase-4 execution; no moves in S2):**
- Extract the dropdown API method group into a SHARED-owned controller, e.g.:
  - `CatalogLookupController` (SHARED owner)
- Keep route names stable until S4 propagation is complete.
- Quotation legacy remains in `QuotationController` (QUO owner).

**Owner per method group (current method list):**
- SHARED (future): `getSubCategories`, `getItems`, `getProducts`, `getProductsByItem`, `getMakes`, `getSeriesApi`, `getDescriptions`, `getMakesByCategory`, `getAllMakes`
- QUO: everything else in Quotation legacy flows

### 3.2 Candidate: `routes/web.php` contains “API” surface

**Observation:** `source_snapshot/routes/api.php` is effectively empty in this snapshot; “API” endpoints are registered under `routes/web.php` with an `/api` prefix.

**Split plan:**
- Phase-4 may migrate API endpoints to `routes/api.php` (or keep in `web.php`) **only after** contract shapes are frozen (S3) and propagation is planned (S4).

### 3.3 Candidate: `ImportController` (mixed ownership — cross-module exception)

Tracked as split ownership in S1:
- CIM import flow methods
- MASTER pdfcontain methods

**Plan:** Detailed adapter seam spec is handled in `docs/PHASE_4/S2_CIM_ISOLATION.md` (CIM step).

---

## Evidence

**Authority References:**
- Route Map: `trace/phase_2/ROUTE_MAP.md`
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- Batch-2 Planning: `docs/PHASE_3/04_TASK_REGISTER/BATCH_2_S2.md` (Section 6.3)
- Boundary Blocks: `docs/PHASE_4/S2_BOUNDARY_BLOCKS.md`

**Evidence Pointers:**
- Controller/service file list: `QuotationController.php`, `ReuseController.php`
- Route names touched: All `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.reuse.*`
- Touchpoint list from S0: See S0-SHARED-001 evidence
- Cross-module call sites: CIM, MBOM, FEED, PBOM, QUO (all modules consume)

**Gate Satisfied By:**
- Contract definitions complete (CatalogLookupContract, ReuseSearchContract)
- Inputs/outputs documented
- Error contract defined
- Caching/logging/versioning rules specified
- Consumer migration list prepared for S4
- Controller split plan documented
- No behavior changes proposed (planning-only)

---

## Task Status

**NSW-P4-S2-SHARED-001:** ✅ Complete  
**NSW-P4-S2-SHARED-002:** ✅ Complete (split plan documented)

**Next Tasks:** S2.3 CIM Isolation (NSW-P4-S2-CIM-001, NSW-P4-S2-CIM-002)


