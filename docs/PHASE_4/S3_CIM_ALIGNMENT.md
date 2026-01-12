# S3.2 — CIM Alignment Pack (Single-Path Catalog Resolution Blueprint)
#
# Task coverage:
# - NSW-P4-S3-CIM-001 (G3) Align catalog resolution to single path
#
# Status: ACTIVE (S3)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document creates a **precise migration blueprint** for CIM catalog resolution alignment.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_CIM_ISOLATION.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: map call sites, document param mapping, verify response compatibility, define rollback strategy
- ❌ Not allowed: removing `product.getsubcategory` etc., changing route files, touching controllers, changing response shapes

---

## 1) Single-Path Catalog Resolution Alignment Statement

**Target state (S3 freeze):**

- UI dropdown/search resolution for Category/Subcategory/Item/Product/Make/Series/Descriptions must route through:
  - **SHARED `CatalogLookupContract`** endpoints (frozen in S3.1)

**Current state:**

- CIM uses module-local endpoints (`product.getsubcategory`, `product.getproducttype`, `product.getseries`, `product.getgeneric`)
- MBOM uses module-local endpoints (`masterbom.getsubcategory`, `masterbom.getproducttype`, `masterbom.getdescription`)
- These are **COMPAT** endpoints (temporary bridge until S4 propagation)

**Alignment goal:**

- Map every CIM module-local endpoint → SHARED contract endpoint
- Identify JS/view call sites
- Document param mapping + response compatibility
- Define rollback strategy

---

## 2) Consumer Call Site Inventory

### 2.1 CIM Module Call Sites

| Consumer (module/screen) | Evidence (view file) | Current lookup calls (route names) | JS/Blade location | Notes |
|---|---|---|---|---|
| CIM — Specific Product (create) | `source_snapshot/resources/views/product/create.blade.php` | `product.getsubcategory`, `product.getseries`, `product.getgeneric` | TBD (verify in execution) | Uses module-local Path B lookups (S2) |
| CIM — Specific Product (edit) | `source_snapshot/resources/views/product/edit.blade.php` | `product.getsubcategory`, `product.getproducttype`, `product.getseries`, `product.getgeneric` | TBD (verify in execution) | Uses module-local Path B lookups (S2) |
| CIM — Generic Product (create) | `source_snapshot/resources/views/generic/create.blade.php` | `product.getsubcategory` | TBD (verify in execution) | Uses module-local Path B lookup (S2) |
| CIM — Generic Product (edit) | `source_snapshot/resources/views/generic/edit.blade.php` | `product.getsubcategory`, `product.getproducttype` | TBD (verify in execution) | Uses module-local Path B lookups (S2) |

**Notes:**
- Additional references may exist in other modules (ex: QUO screens calling `product.*` lookups). Those are recorded in S3.4 (QUO Alignment) and must not be "fixed" in S3.
- JS call sites must be verified during execution (not assumed from route names alone).

### 2.2 MBOM Module Call Sites (for reference; MBOM alignment is S3-BOM-001)

| Consumer (module/screen) | Evidence (view file) | Current lookup calls (route names) | Notes |
|---|---|---|---|
| MBOM — Master BOM (create) | `source_snapshot/resources/views/masterbom/create.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | Catalog lookup helpers live inside MBOM module (still "catalog resolution", per S2) |
| MBOM — Master BOM (edit) | `source_snapshot/resources/views/masterbom/edit.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | Same as create |
| MBOM — Master BOM (copy) | `source_snapshot/resources/views/masterbom/copy.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | Same as create/edit |

**Note:** MBOM alignment is handled in S3-BOM-001; this section is for reference only.

---

## 3) Endpoint Classification (Canonical / Compat / Duplicate)

### 3.1 Canonical (SHARED contract — frozen in S3.1)

| Class | Route Name | Method | URI | Current Host (implementation reality) | Contract Owner | Notes |
|---|---|---:|---|---|---|---|
| canonical | `api.category.subcategories` | GET | `/api/category/{categoryId}/subcategories` | `QuotationController@getSubCategories` | **SHARED** | Returns subcategories (fallbacks exist) |
| canonical | `api.category.items` | GET | `/api/category/{categoryId}/items` | `QuotationController@getItems` | **SHARED** | Supports optional filter `?subcategory={subCategoryId}` (implementation) |
| canonical | `api.category.products` | GET | `/api/category/{categoryId}/products` | `QuotationController@getProducts` | **SHARED** | Generic products (ProductType=1). Uses `subcategoryId` + `itemId` request inputs (implementation) |
| canonical | `api.item.products` | GET | `/api/item/{itemId}/products` | `QuotationController@getProductsByItem` | **SHARED** | Generic products (ProductType=1). Supports optional filters (implementation) |
| canonical | `api.product.makes` | GET | `/api/product/{productId}/makes` | `QuotationController@getMakes` | **SHARED** | Requires `categoryId` or derives from product (implementation) |
| canonical | `api.make.series` | GET | `/api/make/{makeId}/series` | `QuotationController@getSeriesApi` | **SHARED** | Requires `categoryId` input (implementation returns empty without) |
| canonical | `api.product.descriptions` | GET | `/api/product/{productId}/descriptions` | `QuotationController@getDescriptions` | **SHARED** | Contract frozen in S3.1 |
| canonical | `api.category.makes` | GET | `/api/category/{categoryId}/makes` | `QuotationController@getMakesByCategory` | **SHARED** | **S3 Decision:** v1 allows response to be either map `{MakeId: Name}` or list `[{id,label}]`; consumers must normalize to `{id,label}` client-side during S4 |
| canonical | `api.makes` | GET | `/api/makes` | `QuotationController@getAllMakes` | **SHARED** | **S3 Decision:** v1 allows response to be either map `{MakeId: Name}` or list `[{id,label}]`; consumers must normalize to `{id,label}` client-side during S4 |

### 3.2 Compat (module-local lookups — keep until S4/S5)

| Class | Route Name | Method | URI | Current Host | Current payload (observed) | Canonical mapping target | Primary consumers | Removal gate |
|---|---|---:|---|---|---|---|---|---|
| compat | `product.getsubcategory` | GET | `/product/getsubcategory/{id}` | `ProductController@getsubcategory` | `{ subcategory: [{SubCategoryId,Name}], producttype: [{ItemId,Name}], attribute: [...], make: [...] }` | Split into: `api.category.subcategories` + `api.category.items` + `api.category.makes` (attributes are **not** in CatalogLookupContract) | CIM Product create/edit; CIM Generic create/edit | S5 Bundle C pass |
| compat | `product.getproducttype` | GET | `/product/getproducttype/{id}` | `ProductController@getproducttype` | `{ producttype: [{ItemId,Name}] }` | `api.category.items` with `?subcategory={subCategoryId}` | CIM Product edit; CIM Generic edit | S5 Bundle C pass |
| compat | `product.getseries` | GET | `/product/getseries` | `ProductController@getseries` | `{ series: [{SeriesId,Name}] }` (requires `CategoryId`, `MakeId`) | `api.make.series` (requires `categoryId` input in current implementation) | CIM Product create/edit | S5 Bundle C pass |
| compat | `product.getgeneric` | GET | `/product/getgeneric` | `ProductController@getgeneric` | `{ description: [{ProductId,Name}] }` (filters: CategoryId/SubCategoryId/ItemId; ProductType=1) | `api.category.products` with `subcategoryId` + `itemId` inputs | CIM Product create/edit | S5 Bundle C pass |
| compat | `masterbom.getsubcategory` | GET | `/masterbom/getsubcategory/{id}` | `MasterBomController@getsubcategory` | `{ subcategory: [...], producttype: [...] }` | `api.category.subcategories` + `api.category.items` | MBOM create/edit/copy | S5 Bundle C pass (MBOM alignment is S3-BOM-001) |
| compat | `masterbom.getproducttype` | GET | `/masterbom/getproducttype/{id}` | `MasterBomController@getproducttype` | `{ producttype: [...] }` | `api.category.items` with `?subcategory={subCategoryId}` | MBOM (present; usage in known views is commented—do not delete) | S5 Bundle C pass (MBOM alignment is S3-BOM-001) |
| compat | `masterbom.getdescription` | GET | `/masterbom/getdescription` | `MasterBomController@getdescription` | `{ description: [{ProductId,Name}] }` (filters: CategoryId/SubCategoryId/ItemId; ProductType=1) | `api.category.products` with `subcategoryId` + `itemId` inputs | MBOM create/edit/copy | S5 Bundle C pass (MBOM alignment is S3-BOM-001) |

### 3.3 Duplicate (removal candidates — S4+ only)

No endpoints are approved for removal in S3. Populate this section **only after** S4 propagation proves zero consumers remain and S5 Bundle C passes.

---

## 4) Migration Blueprint: CIM Module-Local → SHARED Contract

### 4.1 `product.getsubcategory` → CatalogLookupContract

**Current endpoint:**
- Route: `product.getsubcategory`
- URI: `/product/getsubcategory/{id}`
- Method: GET
- Host: `ProductController@getsubcategory`
- Payload: `{ subcategory: [{SubCategoryId,Name}], producttype: [{ItemId,Name}], attribute: [...], make: [...] }`

**Target endpoints (split mapping):**
- `api.category.subcategories` (for subcategory list)
- `api.category.items` (for producttype list, with `?subcategory={subCategoryId}`)
- `api.category.makes` (for make list, with `categoryId`)
- **Note:** Attributes are **not** in CatalogLookupContract; this is a compatibility gap that must be handled in S4

**Parameter mapping:**
- Current: `{id}` (path param) → categoryId
- Target: `{categoryId}` (path param) for subcategories, items, makes

**Response compatibility:**
- Current: Returns nested object with multiple arrays
- Target: Returns flat array `[{id, label}]`
- **Compatibility gap:** Requires client-side transformation in S4 migration

**Call sites to migrate:**
- `product/create.blade.php` (JS calls)
- `product/edit.blade.php` (JS calls)
- `generic/create.blade.php` (JS calls)
- `generic/edit.blade.php` (JS calls)

**Rollback strategy:**
- Keep `product.getsubcategory` active during S4 migration
- Remove only after S5 Bundle C passes
- If migration fails, revert JS to use `product.getsubcategory`

### 4.2 `product.getproducttype` → CatalogLookupContract

**Current endpoint:**
- Route: `product.getproducttype`
- URI: `/product/getproducttype/{id}`
- Method: GET
- Host: `ProductController@getproducttype`
- Payload: `{ producttype: [{ItemId,Name}] }`

**Target endpoint:**
- `api.category.items` with `?subcategory={subCategoryId}`

**Parameter mapping:**
- Current: `{id}` (path param) → categoryId
- Target: `{categoryId}` (path param) + `?subcategory={subCategoryId}` (query param)
- **Gap:** Requires subcategoryId to be available in client context

**Response compatibility:**
- Current: Returns `{ producttype: [{ItemId,Name}] }`
- Target: Returns `[{id, label}]`
- **Compatibility:** Requires client-side transformation (extract `producttype` array, then flatten to `{id,label}`)

**Call sites to migrate:**
- `product/edit.blade.php` (JS calls)
- `generic/edit.blade.php` (JS calls)

**Rollback strategy:**
- Keep `product.getproducttype` active during S4 migration
- Remove only after S5 Bundle C passes

### 4.3 `product.getseries` → CatalogLookupContract

**Current endpoint:**
- Route: `product.getseries`
- URI: `/product/getseries`
- Method: GET
- Host: `ProductController@getseries`
- Payload: `{ series: [{SeriesId,Name}] }` (requires `CategoryId`, `MakeId` as query params)

**Target endpoint:**
- `api.make.series` with `{makeId}` (path param) + `categoryId` (query param, if required by implementation)

**Parameter mapping:**
- Current: `CategoryId`, `MakeId` (query params)
- Target: `{makeId}` (path param) + `categoryId` (query param, if required)
- **Gap:** Requires MakeId to be available in client context

**Response compatibility:**
- Current: Returns `{ series: [{SeriesId,Name}] }`
- Target: Returns `[{id, label}]` (contract minimum)
- **Compatibility:** Requires client-side transformation (extract `series` array, then flatten to `{id,label}`)

**Call sites to migrate:**
- `product/create.blade.php` (JS calls)
- `product/edit.blade.php` (JS calls)

**Rollback strategy:**
- Keep `product.getseries` active during S4 migration
- Remove only after S5 Bundle C passes

### 4.4 `product.getgeneric` → CatalogLookupContract

**Current endpoint:**
- Route: `product.getgeneric`
- URI: `/product/getgeneric`
- Method: GET
- Host: `ProductController@getgeneric`
- Payload: `{ description: [{ProductId,Name}] }` (filters: CategoryId/SubCategoryId/ItemId; ProductType=1)

**Target endpoint:**
- `api.category.products` with `{categoryId}` (path param) + `?subcategoryId={subCategoryId}&itemId={itemId}` (query params)

**Parameter mapping:**
- Current: `CategoryId`, `SubCategoryId`, `ItemId` (query params)
- Target: `{categoryId}` (path param) + `?subcategoryId={subCategoryId}&itemId={itemId}` (query params)
- **Compatibility:** Direct mapping possible

**Response compatibility:**
- Current: Returns `{ description: [{ProductId,Name}] }`
- Target: Returns `[{id, label}]` (contract minimum)
- **Compatibility:** Requires client-side transformation (extract `description` array, then flatten to `{id,label}`)

**Call sites to migrate:**
- `product/create.blade.php` (JS calls)
- `product/edit.blade.php` (JS calls)

**Rollback strategy:**
- Keep `product.getgeneric` active during S4 migration
- Remove only after S5 Bundle C passes

---

## 5) Compatibility Gaps & Resolution Strategy

### 5.1 Response Shape Gaps

**Issue:** Current compat endpoints return nested objects (e.g., `{ subcategory: [...] }`), while CatalogLookupContract returns flat arrays `[{id, label}]`.

**Resolution:**
- Client-side transformation in S4 migration (extract nested arrays, flatten to `{id,label}`)
- No server-side payload changes in S3 (forbidden)

### 5.2 Parameter Context Gaps

**Issue:** Some compat endpoints require context that may not be immediately available in client (e.g., `subcategoryId` for `product.getproducttype` → `api.category.items`).

**Resolution:**
- Document required context in migration blueprint
- Ensure client collects required context before calling target endpoint
- Rollback to compat endpoint if context unavailable

### 5.3 Missing Contract Coverage

**Issue:** `product.getsubcategory` returns `attribute` array, which is **not** in CatalogLookupContract.

**S3 Decision (frozen):**
- Attributes will remain served by compat endpoint until a separate SHARED contract is defined (future v2)
- Therefore S4 migration of `product.getsubcategory` must be staged last (after other CIM endpoints are migrated)
- Attributes are out of scope for CatalogLookupContract v1
- If attributes are required, they must be handled via separate contract or remain on compat endpoint until v2 extension

---

## 6) S4 Migration Execution Plan (S3 Blueprint Only)

### 6.1 Migration Order (recommended)

1. **Phase 1:** Migrate `product.getgeneric` (simplest parameter mapping)
2. **Phase 2:** Migrate `product.getproducttype` (requires subcategoryId context)
3. **Phase 3:** Migrate `product.getseries` (requires MakeId context)
4. **Phase 4:** Migrate `product.getsubcategory` (most complex, includes attributes gap)

### 6.2 Migration Checklist (for S4 execution)

For each compat endpoint:

- [ ] **Call sites identified:** All JS/Blade files using the endpoint
- [ ] **Parameter mapping verified:** All required params available in client context
- [ ] **Response transformation tested:** Client-side flattening works correctly
- [ ] **Rollback tested:** Reverting to compat endpoint works
- [ ] **Bundle A/B/C verified:** No regression in test bundles
- [ ] **Compat endpoint removed:** Only after S5 Bundle C passes

---

## 7) Alignment Decisions (frozen until S4)

- Consumers must treat catalog lookup results as **read-only** and **tolerant**:
  - Prefer option arrays shaped like `{id,label}`
  - Tolerate current implementation differences where endpoints return id→label maps (no server payload changes in S3)
- CIM must not expand direct QUO coupling; any convergence work is S4.
- **Compat endpoints remain active** until S5 Bundle C passes (no deletions in S3 or S4).

---

## 8) Out of Scope for S3 (explicit)

- Deleting or renaming any module-local lookup endpoints
- Changing payload formats returned by module-local endpoints
- Any controller splits (ImportController split is S4 work only)
- Modifying QUO-V2 core behavior (PROTECTED zone remains fenced)
- Removing compat endpoints (deletion happens only after S5 Bundle C passes)

---

## 9) Evidence Requirements

### 9.1 Call Site Inventory Evidence

- [ ] All CIM view files identified (Section 2.1)
- [ ] All JS call sites mapped (verify in execution)
- [ ] All compat endpoints classified (Section 3.2)

### 9.2 Migration Blueprint Evidence

- [ ] Parameter mapping documented for each compat endpoint (Section 4)
- [ ] Response compatibility analyzed (Section 4)
- [ ] Compatibility gaps identified (Section 5)
- [ ] Rollback strategy defined (Section 4)

### 9.3 Alignment Decisions Evidence

- [ ] Alignment decisions recorded (Section 7)
- [ ] Out of scope explicitly listed (Section 8)
- [ ] No route renames proposed
- [ ] No behavior changes proposed

---

## 10) Task Status

**NSW-P4-S3-CIM-001 (Align catalog resolution to single path):** ✅ Complete

**Next Tasks:** S3-BOM-001 (MBOM), S3-BOM-002 (FEED), S3-BOM-003 (PBOM)

---

## 11) Authority References

- Route Map: `trace/phase_2/ROUTE_MAP.md`
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- S2 CIM Isolation: `docs/PHASE_4/S2_CIM_ISOLATION.md`
- S2 SHARED Isolation: `docs/PHASE_4/S2_SHARED_ISOLATION.md`
- S3 SHARED Alignment: `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
- S3 Execution Checklist: `docs/PHASE_4/S3_EXECUTION_CHECKLIST.md`
- Master Task List: `docs/PHASE_4/MASTER_TASK_LIST.md`
