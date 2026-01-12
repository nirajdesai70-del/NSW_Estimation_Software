# S3.1 — SHARED Alignment Pack (Contract Freeze + Consumer Map)
#
# Task coverage:
# - NSW-P4-S3-SHARED-001 (G3) Freeze CatalogLookupContract
# - NSW-P4-S3-SHARED-002 (G3) Freeze ReuseSearchContract
#
# Status: ACTIVE (S3)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document **freezes** SHARED contract shapes identified in S2.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `trace/phase_2/ROUTE_MAP.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S2_CIM_ISOLATION.md`
  - `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md`

**S3 Guardrails:**
- ✅ Allowed: freeze contract specs, define adapter seams, update documentation + checklists, define consumer migration mapping
- ❌ Not allowed: controller/file moves, route file migration, changing response shapes, modifying QUO-V2 core behavior

---

## 1) Contract Freeze: CatalogLookupContract (v1) — NSW-P4-S3-SHARED-001

### 1.1 Frozen endpoint list (do not rename in S3)

All are **auth + throttle:search** in current trace.

| Route Name | Method | URI | Current Host (implementation reality) | Contract Owner (S3) |
|---|---:|---|---|
| `api.category.subcategories` | GET | `/api/category/{categoryId}/subcategories` | `QuotationController@getSubCategories` | **SHARED** |
| `api.category.items` | GET | `/api/category/{categoryId}/items` | `QuotationController@getItems` | **SHARED** |
| `api.category.products` | GET | `/api/category/{categoryId}/products` | `QuotationController@getProducts` | **SHARED** |
| `api.item.products` | GET | `/api/item/{itemId}/products` | `QuotationController@getProductsByItem` | **SHARED** |
| `api.product.makes` | GET | `/api/product/{productId}/makes` | `QuotationController@getMakes` | **SHARED** |
| `api.make.series` | GET | `/api/make/{makeId}/series` | `QuotationController@getSeriesApi` | **SHARED** |
| `api.product.descriptions` | GET | `/api/product/{productId}/descriptions` | `QuotationController@getDescriptions` | **SHARED** |
| `api.category.makes` | GET | `/api/category/{categoryId}/makes` | `QuotationController@getMakesByCategory` | **SHARED** |
| `api.makes` | GET | `/api/makes` | `QuotationController@getAllMakes` | **SHARED** |

**Code anchors:**
- Routes file: `source_snapshot/routes/web.php` (treat as canonical until S4)
- Route group: `Route::group(['middleware' => 'auth', 'prefix' => 'api'], function () { ... })`
- Implementation controller: `source_snapshot/app/Http/Controllers/QuotationController.php`

### 1.2 Frozen request contract (minimum)

**Path parameters (required, as applicable):**
- `categoryId` (string|number) — for category-scoped endpoints
- `itemId` (string|number) — for item-scoped endpoints
- `productId` (string|number) — for product-scoped endpoints
- `makeId` (string|number) — for make-scoped endpoints

**Query parameters (optional):**
- `search` / `term` (string) — allowed, optional; callers must not assume server-side filtering exists unless explicitly evidenced
- Additional query params may exist in implementation; contract guarantees only the above

### 1.3 Frozen response contract (minimum)

Return **a list of option objects** (order not guaranteed):

```json
[
  { "id": "string|number", "label": "string" }
]
```

**Contract rules:**
- Callers **must ignore unknown fields** (server may return additional fields; contract guarantees only `id`, `label`).
- Callers **must not** depend on CIM table/column names.
- Empty array `[]` is valid (no results found).
- `id` type may be string or number; callers must handle both.

**Optional (future, non-breaking) metadata:**
- `{ meta?: { sourceVersion?: string, cacheTtlSeconds?: number } }` — may be present but callers must not depend on it

### 1.4 Frozen error contract

**Standard HTTP status codes:**
- `200 OK`: Success (with data array, may be empty)
- `400 Bad Request`: Invalid path/query parameters (e.g., missing required `categoryId`)
- `401 Unauthorized`: Authentication required (auth middleware)
- `404 Not Found`: Resource not found (e.g., invalid categoryId)
- `500 Internal Server Error`: Server error

**Error response shape:**
```json
{ "error": "string", "message": "string (optional)" }
```

### 1.5 Frozen caching/lookup rules

**Current state (frozen in S3):**
- No explicit caching contract defined (implementation may cache; contract does not guarantee it)
- Callers must not assume caching behavior
- Throttling may apply (`throttle:search` middleware)

**Future contract extension (non-breaking, S4+):**
- Optional `cacheTtlSeconds` in response metadata
- Optional `cache-control` headers

### 1.6 Frozen logging requirements

**Contract requirement:**
- All catalog lookup requests must be logged for audit/debugging
- Log: route name, path params, query params (sanitized), response status
- No PII in logs (IDs only, not names/labels)

### 1.7 Frozen versioning rule

**Contract version:** v1 (frozen in S3)
**Versioning strategy:**
- Non-breaking additions (new optional fields) allowed
- Breaking changes require new route/version identifier
- Current routes remain v1 until explicit migration

### 1.8 Forbidden coupling (enforced by SHARED contract)

- No module may rely on "extra" fields not declared by the contract.
- No caller may assume ORM field names from CIM tables.
- No caller may depend on response order.

---

## 2) Contract Freeze: ReuseSearchContract (v1) — NSW-P4-S3-SHARED-002

### 2.1 Frozen endpoint list (do not rename in S3)

All are **auth + throttle:search** in current trace.

| Route Name | Method | URI | Current Host (implementation reality) | Contract Owner (S3) |
|---|---:|---|---|
| `api.reuse.panels` | GET | `/api/reuse/panels` | `ReuseController@searchPanels` | **SHARED** |
| `api.reuse.feeders` | GET | `/api/reuse/feeders` | `ReuseController@searchFeeders` | **SHARED** |
| `api.reuse.masterBoms` | GET | `/api/reuse/master-boms` | `ReuseController@searchMasterBoms` | **SHARED** |
| `api.reuse.proposalBoms` | GET | `/api/reuse/proposal-boms` | `ReuseController@searchProposalBoms` | **SHARED** |

**Code anchors:**
- Routes file: `source_snapshot/routes/web.php` (treat as canonical until S4)
- Implementation controller: `source_snapshot/app/Http/Controllers/ReuseController.php`

### 2.2 Frozen request contract (minimum)

**Query parameters:**
- `searchTerm` (string) — **canonical** search parameter
- `q` (string) — **allowed alias** (observed patterns vary; treat as compatibility)
- Optional filters (allowed but not required for v1):
  - `quotationId` (string|number) — filter by quotation context
  - `panelId` (string|number) — filter by panel context
  - Paging controls (if present in implementation; contract does not guarantee)

### 2.3 Frozen response contract (minimum)

Return a list of search results:

```json
[
  { 
    "id": "string|number", 
    "label": "string", 
    "kind": "panel" | "feeder" | "masterBom" | "proposalBom" 
  }
]
```

**Contract rules:**
- Callers must ignore extra fields.
- `kind` is **required** for routing UI actions safely without type inference.
- Empty array `[]` is valid (no results found).
- `id` type may be string or number; callers must handle both.

### 2.4 Frozen error contract

**Standard HTTP status codes:**
- `200 OK`: Success (with data array, may be empty)
- `400 Bad Request`: Invalid query parameters (e.g., missing required `searchTerm`)
- `401 Unauthorized`: Authentication required (auth middleware)
- `500 Internal Server Error`: Server error

**Error response shape:**
```json
{ "error": "string", "message": "string (optional)" }
```

### 2.5 Frozen caching/lookup rules

**Current state (frozen in S3):**
- Search performance may be throttled (`throttle:search` middleware)
- No explicit caching contract defined
- Callers must not assume caching behavior

**Future contract extension (non-breaking, S4+):**
- Optional paging parameters
- Optional result limits

### 2.6 Frozen logging requirements

**Contract requirement:**
- All reuse search requests must be logged for audit/debugging
- Log: route name, optional filters, response status, and `searchTermLength` (not full searchTerm)
- **Never log raw searchTerm** (PII protection)
- No PII in logs (IDs only, not names/labels)

### 2.7 Frozen versioning rule

**Contract version:** v1 (frozen in S3)
**Versioning strategy:**
- Non-breaking additions (new optional filters) allowed
- Breaking changes require new route/version identifier
- Current routes remain v1 until explicit migration

---

## 3) Consumer Map (who uses SHARED contracts)

### 3.1 Known consumers (recorded in S2/trace)

**Quotation (Legacy):**
- Hosts and consumes CatalogLookup endpoints (currently inside `QuotationController`)
- Hosts ReuseSearch endpoints (currently inside `ReuseController`)
- **S4 Migration:** Will continue consuming after extraction (no change in consumption pattern)

**Quotation (V2):**
- Uses CatalogLookup endpoints for dropdown hydration (Shared (Legacy+V2) in `trace/phase_2/ROUTE_MAP.md`)
- Uses ReuseSearch endpoints for reuse pickers
- **S4 Migration:** Will continue consuming after extraction (no change in consumption pattern)

**PBOM / Reuse flows:**
- `api.reuse.proposalBoms` is used for selection flows (see `docs/PHASE_4/S2_PBOM_ISOLATION.md`)
- **S4 Migration:** Already using contract; no migration needed

**CIM:**
- Target state: CIM UI and other modules converge onto these SHARED endpoints (single-path plan; see `docs/PHASE_4/S2_CIM_ISOLATION.md`)
- **Current state:** Uses module-local endpoints (`product.getsubcategory`, `product.getproducttype`, etc.)
- **S4 Migration:** Must migrate from module-local endpoints to `CatalogLookupContract` (NSW-P4-S4-CIM-001)

**MBOM:**
- **Current state:** Uses module-local endpoints (`masterbom.getsubcategory`, `masterbom.getdescription`, etc.)
- **S4 Migration:** Must migrate from module-local endpoints to `CatalogLookupContract` (NSW-P4-S4-MBOM-001)

**FEED:**
- **Current state:** Internal catalog lookups (module-local)
- **S4 Migration:** Must migrate to `CatalogLookupContract` (NSW-P4-S4-FEED-001)

---

## 4) Consumer Adoption Checklist (S4 Propagation Readiness)

### 4.1 CatalogLookupContract Adoption Checklist

**For each consumer module, verify:**

#### CIM Module (NSW-P4-S4-CIM-001)
- [ ] **Current state documented:**
  - [ ] Module-local endpoints identified: `product.getsubcategory`, `product.getproducttype`, `product.getgeneric`, `product.getseries`
  - [ ] Call sites mapped: views/JS files using these endpoints
- [ ] **Target state defined:**
  - [ ] Replacement `CatalogLookupContract` endpoints identified for each module-local endpoint
  - [ ] Migration path documented (which view/JS file → which contract endpoint)
- [ ] **Compatibility verified:**
  - [ ] Response shape compatibility checked (module-local returns `{id, label}` format)
  - [ ] Path/query param mapping verified
- [ ] **Rollback plan:**
  - [ ] Module-local endpoints remain active during migration (compat mode)
  - [ ] Rollback steps documented

#### MBOM Module (NSW-P4-S4-MBOM-001)
- [ ] **Current state documented:**
  - [ ] Module-local endpoints identified: `masterbom.getsubcategory`, `masterbom.getproducttype`, `masterbom.getdescription`
  - [ ] Call sites mapped: views/JS files using these endpoints
- [ ] **Target state defined:**
  - [ ] Replacement `CatalogLookupContract` endpoints identified
  - [ ] Migration path documented
- [ ] **Compatibility verified:**
  - [ ] Response shape compatibility checked
  - [ ] Path/query param mapping verified
- [ ] **Rollback plan:**
  - [ ] Module-local endpoints remain active during migration
  - [ ] Rollback steps documented

#### FEED Module (NSW-P4-S4-FEED-001)
- [ ] **Current state documented:**
  - [ ] Internal catalog lookup call sites identified
  - [ ] Current implementation pattern documented
- [ ] **Target state defined:**
  - [ ] Replacement `CatalogLookupContract` endpoints identified
  - [ ] Migration path documented
- [ ] **Compatibility verified:**
  - [ ] Response shape compatibility checked
  - [ ] Path/query param mapping verified
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented

#### QUO Legacy (NSW-P4-S4-QUO-001)
- [ ] **Current state documented:**
  - [ ] Hosts CatalogLookup endpoints (will be extracted in S4)
  - [ ] Consumes CatalogLookup endpoints (will continue consuming after extraction)
- [ ] **Target state defined:**
  - [ ] Extraction plan documented (move to SHARED controller)
  - [ ] Consumption pattern remains unchanged (no migration needed)
- [ ] **Compatibility verified:**
  - [ ] Route names remain stable (no breaking changes)
  - [ ] Response shapes remain stable
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented

#### QUO V2 (NSW-P4-S4-QUO-002)
- [ ] **Current state documented:**
  - [ ] Uses CatalogLookup endpoints for dropdown hydration
  - [ ] Call sites mapped (PROTECTED zone)
- [ ] **Target state defined:**
  - [ ] Consumption pattern remains unchanged (no migration needed)
  - [ ] Wrapper entry points verified (if applicable)
- [ ] **Compatibility verified:**
  - [ ] Route names remain stable
  - [ ] Response shapes remain stable
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented (G4 PROTECTED)

### 4.2 ReuseSearchContract Adoption Checklist

**For each consumer module, verify:**

#### QUO V2 (NSW-P4-S4-QUO-001)
- [ ] **Current state documented:**
  - [ ] Uses ReuseSearch endpoints for reuse pickers
  - [ ] Call sites mapped
- [ ] **Target state defined:**
  - [ ] Consumption pattern remains unchanged (no migration needed)
- [ ] **Compatibility verified:**
  - [ ] Route names remain stable
  - [ ] Response shapes remain stable
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented

#### MBOM Module (NSW-P4-S4-MBOM-001)
- [ ] **Current state documented:**
  - [ ] Internal reuse search call sites identified
  - [ ] Current implementation pattern documented
- [ ] **Target state defined:**
  - [ ] Replacement `ReuseSearchContract` endpoints identified
  - [ ] Migration path documented
- [ ] **Compatibility verified:**
  - [ ] Response shape compatibility checked
  - [ ] Query param mapping verified
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented

#### FEED Module (NSW-P4-S4-FEED-001)
- [ ] **Current state documented:**
  - [ ] Internal reuse search call sites identified
  - [ ] Current implementation pattern documented
- [ ] **Target state defined:**
  - [ ] Replacement `ReuseSearchContract` endpoints identified
  - [ ] Migration path documented
- [ ] **Compatibility verified:**
  - [ ] Response shape compatibility checked
  - [ ] Query param mapping verified
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented

#### PBOM Module (NSW-P4-S4-PBOM-001)
- [ ] **Current state documented:**
  - [ ] Uses `api.reuse.proposalBoms` for selection flows
  - [ ] Call sites mapped
- [ ] **Target state defined:**
  - [ ] Consumption pattern remains unchanged (already using contract)
- [ ] **Compatibility verified:**
  - [ ] Route names remain stable
  - [ ] Response shapes remain stable
- [ ] **Rollback plan:**
  - [ ] Rollback steps documented

---

## 5) S3 Alignment Decisions (frozen until S4)

- **Route names and URIs are frozen** for S3.
- **Implementation host may remain QUO/Reuse** through S3; moving to SHARED-owned controllers is S4 propagation work only.
- **Catalog resolution must converge** on CatalogLookupContract (single-path target); deprecations remain S4/S5 gated.
- **Contract shapes are immutable** until S4 propagation completes and S5 regression gate passes.

---

## 6) Out of Scope for S3 (explicit)

- Moving endpoints from `routes/web.php` to `routes/api.php`
- Creating/renaming controllers in code
- Changing JSON payload shapes beyond documenting the **minimum contract**
- Any performance optimization (caching, query tuning)
- Removing module-local compat endpoints (deletion happens only after S5 Bundle C passes)
- Modifying QUO-V2 core behavior (PROTECTED zone remains fenced)

---

## 7) Evidence Requirements

### 7.1 Contract Freeze Evidence

- [ ] Endpoint list + ownership recorded (Section 1.1, 2.1)
- [ ] Contract request/response shapes recorded (Section 1.2-1.3, 2.2-2.3)
- [ ] Error contract defined (Section 1.4, 2.4)
- [ ] Versioning rules documented (Section 1.7, 2.7)
- [ ] Forbidden coupling rules documented (Section 1.8)

### 7.2 Consumer Map Evidence

- [ ] Consumer list recorded (Section 3.1)
- [ ] Current state documented for each consumer
- [ ] Target state defined for each consumer
- [ ] S4 migration tasks linked (Section 4.1, 4.2)

### 7.3 Alignment Decisions Evidence

- [ ] S3 alignment decisions recorded (Section 5)
- [ ] Out of scope explicitly listed (Section 6)
- [ ] No route renames proposed
- [ ] No behavior changes proposed

---

## 8) Task Status

**NSW-P4-S3-SHARED-001 (Freeze CatalogLookupContract):** ✅ Complete  
**NSW-P4-S3-SHARED-002 (Freeze ReuseSearchContract):** ✅ Complete

**Next Tasks:** S3-CIM-001 (Align catalog resolution to single path)

---

## 9) Authority References

- Route Map: `trace/phase_2/ROUTE_MAP.md`
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- S2 Isolation: `docs/PHASE_4/S2_SHARED_ISOLATION.md`
- S2 CIM Isolation: `docs/PHASE_4/S2_CIM_ISOLATION.md`
- S2 QUO Legacy Isolation: `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md`
- S3 Execution Checklist: `docs/PHASE_4/S3_EXECUTION_CHECKLIST.md`
- Master Task List: `docs/PHASE_4/MASTER_TASK_LIST.md`

---

## 10) S3 Contract Freeze Declaration

By approving this document, the following is declared:

- **CatalogLookupContract v1 is frozen**
- **ReuseSearchContract v1 is frozen**
- **No breaking changes are allowed before S4 propagation**
- **All consumers must align to these contracts during S4**
- **No route, controller, or response-shape changes occurred in S3**

**Freeze Effective Date:** 2025-12-18  
**Applies Until:** S5 Regression Gate passes

**Evidence Closure:**
- ✅ Contract specifications documented (Sections 1, 2)
- ✅ Consumer map documented (Section 3)
- ✅ Consumer adoption checklists prepared (Section 4)
- ✅ Alignment decisions recorded (Section 5)
- ✅ Out of scope explicitly listed (Section 6)
- ✅ Evidence requirements satisfied (Section 7)
