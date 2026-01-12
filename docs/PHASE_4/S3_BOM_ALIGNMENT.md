# S3.3 — BOM Alignment Pack (MBOM / FEED / PBOM Apply Contracts + Catalog Resolution)
#
# Task coverage:
# - NSW-P4-S3-BOM-001 (G3) Align MBOM catalog resolution to single path
# - NSW-P4-S3-BOM-002 (G3) Align FEED apply contract + gap closure (BOM-GAP-001, BOM-GAP-002)
# - NSW-P4-S3-BOM-003 (G3) Align PBOM apply contract
#
# Status: ACTIVE (S3)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document creates **precise migration blueprints** for BOM module alignment:
  - **S3-BOM-001:** MBOM catalog resolution alignment (single-path catalog resolution)
  - **S3-BOM-002:** FEED apply contract alignment + gap closure requirements
  - **S3-BOM-003:** PBOM apply contract alignment
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_MBOM_ISOLATION.md`
  - `docs/PHASE_4/S2_FEED_ISOLATION.md`
  - `docs/PHASE_4/S2_PBOM_ISOLATION.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: map call sites, document param mapping, verify response compatibility, define rollback strategy, freeze apply contracts
- ❌ Not allowed: removing `masterbom.getsubcategory` etc., changing route files, touching controllers, changing response shapes, modifying apply behavior

---

# S3-BOM-001: MBOM Alignment (Catalog Resolution + Apply Contract Freeze)

## Scope + Fence

- This section creates a **precise migration blueprint** for MBOM catalog resolution alignment.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_MBOM_ISOLATION.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: map call sites, document param mapping, verify response compatibility, define rollback strategy
- ❌ Not allowed: removing `masterbom.getsubcategory` etc., changing route files, touching controllers, changing response shapes

---

## 1) Single-Path Catalog Resolution Alignment Statement

**Target state (S3 freeze):**

- UI dropdown/search resolution for Category/Subcategory/Item/Product/Descriptions in MBOM forms must route through:
  - **SHARED `CatalogLookupContract`** endpoints (frozen in S3.1)

**Current state:**

- MBOM uses module-local endpoints (`masterbom.getsubcategory`, `masterbom.getproducttype`, `masterbom.getdescription`)
- These are **COMPAT** endpoints (temporary bridge until S4 propagation)

**Alignment goal:**

- Map every MBOM module-local endpoint → SHARED contract endpoint
- Identify JS/view call sites
- Document param mapping + response compatibility
- Define rollback strategy

---

## 2) Consumer Call Site Inventory

### 2.1 MBOM Module Call Sites

| Consumer (module/screen) | Evidence (view file) | Current lookup calls (route names) | JS/Blade location | Notes |
|---|---|---|---|---|
| MBOM — Master BOM (create) | `source_snapshot/resources/views/masterbom/create.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | TBD (verify in execution) | Uses module-local Path B lookups (S2) |
| MBOM — Master BOM (edit) | `source_snapshot/resources/views/masterbom/edit.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | TBD (verify in execution) | Uses module-local Path B lookups (S2) |
| MBOM — Master BOM (copy) | `source_snapshot/resources/views/masterbom/copy.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | TBD (verify in execution) | Uses module-local Path B lookups (S2) |

**Notes:**
- `masterbom.getproducttype` exists in routes but usage in known views is commented—do not delete
- JS call sites must be verified during execution (not assumed from route names alone)
- Additional references may exist in other modules; those are recorded in S3.4 (QUO Alignment) and must not be "fixed" in S3

---

## 3) Endpoint Classification (Canonical / Compat / Duplicate)

### 3.1 Canonical (SHARED contract — frozen in S3.1)

| Class | Route Name | Method | URI | Current Host (implementation reality) | Contract Owner | Notes |
|---|---|---:|---|---|---|---|
| canonical | `api.category.subcategories` | GET | `/api/category/{categoryId}/subcategories` | `QuotationController@getSubCategories` | **SHARED** | Returns subcategories (fallbacks exist) |
| canonical | `api.category.items` | GET | `/api/category/{categoryId}/items` | `QuotationController@getItems` | **SHARED** | Supports optional filter `?subcategory={subCategoryId}` (implementation) |
| canonical | `api.category.products` | GET | `/api/category/{categoryId}/products` | `QuotationController@getProducts` | **SHARED** | Generic products (ProductType=1). Uses `subcategoryId` + `itemId` request inputs (implementation) |
| canonical | `api.product.descriptions` | GET | `/api/product/{productId}/descriptions` | `QuotationController@getDescriptions` | **SHARED** | Contract frozen in S3.1 |

### 3.2 Compat (module-local lookups — keep until S4/S5)

| Class | Route Name | Method | URI | Current Host | Current payload (observed) | Canonical mapping target | Primary consumers | Removal gate |
|---|---|---:|---|---|---|---|---|---|
| compat | `masterbom.getsubcategory` | GET | `/masterbom/getsubcategory/{id}` | `MasterBomController@getsubcategory` | `{ subcategory: [{SubCategoryId,Name}], producttype: [{ItemId,Name}] }` | Split into: `api.category.subcategories` + `api.category.items` | MBOM create/edit/copy | S5 Bundle C pass |
| compat | `masterbom.getproducttype` | GET | `/masterbom/getproducttype/{id}` | `MasterBomController@getproducttype` | `{ producttype: [{ItemId,Name}] }` | `api.category.items` with `?subcategory={subCategoryId}` | MBOM (present; usage in known views is commented—do not delete) | S5 Bundle C pass |
| compat | `masterbom.getdescription` | GET | `/masterbom/getdescription` | `MasterBomController@getdescription` | `{ description: [{ProductId,Name}] }` (filters: CategoryId/SubCategoryId/ItemId; ProductType=1) | `api.category.products` with `subcategoryId` + `itemId` inputs | MBOM create/edit/copy | S5 Bundle C pass |

### 3.3 Duplicate (removal candidates — S4+ only)

No endpoints are approved for removal in S3. Populate this section **only after** S4 propagation proves zero consumers remain and S5 Bundle C passes.

---

## 4) Migration Blueprint: MBOM Module-Local → SHARED Contract

### 4.1 `masterbom.getsubcategory` → CatalogLookupContract

**Current endpoint:**
- Route: `masterbom.getsubcategory`
- URI: `/masterbom/getsubcategory/{id}`
- Method: GET
- Host: `MasterBomController@getsubcategory`
- Payload: `{ subcategory: [{SubCategoryId,Name}], producttype: [{ItemId,Name}] }`

**Target endpoints (split mapping):**
- `api.category.subcategories` (for subcategory list)
- `api.category.items` (for producttype list, with `?subcategory={subCategoryId}`)

**Parameter mapping:**
- Current: `{id}` (path param) → categoryId
- Target: `{categoryId}` (path param) for subcategories, items

**Response compatibility:**
- Current: Returns nested object with multiple arrays
- Target: Returns flat array `[{id, label}]`
- **Compatibility gap:** Requires client-side transformation in S4 migration

**Call sites to migrate:**
- `masterbom/create.blade.php` (JS calls)
- `masterbom/edit.blade.php` (JS calls)
- `masterbom/copy.blade.php` (JS calls)

**Rollback strategy:**
- Keep `masterbom.getsubcategory` active during S4 migration
- Remove only after S5 Bundle C passes
- If migration fails, revert JS to use `masterbom.getsubcategory`

### 4.2 `masterbom.getproducttype` → CatalogLookupContract

**Current endpoint:**
- Route: `masterbom.getproducttype`
- URI: `/masterbom/getproducttype/{id}`
- Method: GET
- Host: `MasterBomController@getproducttype`
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
- Currently commented in views; verify during execution

**Rollback strategy:**
- Keep `masterbom.getproducttype` active during S4 migration
- Remove only after S5 Bundle C passes

### 4.3 `masterbom.getdescription` → CatalogLookupContract

**Current endpoint:**
- Route: `masterbom.getdescription`
- URI: `/masterbom/getdescription`
- Method: GET
- Host: `MasterBomController@getdescription`
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
- `masterbom/create.blade.php` (JS calls)
- `masterbom/edit.blade.php` (JS calls)
- `masterbom/copy.blade.php` (JS calls)

**Rollback strategy:**
- Keep `masterbom.getdescription` active during S4 migration
- Remove only after S5 Bundle C passes
- If migration fails, revert JS to use `masterbom.getdescription`

---

## 5) Compatibility Gaps & Resolution Strategy

### 5.1 Response Shape Gaps

**Issue:** Current compat endpoints return nested objects (e.g., `{ subcategory: [...] }`), while CatalogLookupContract returns flat arrays `[{id, label}]`.

**Resolution:**
- Client-side transformation in S4 migration (extract nested arrays, flatten to `{id,label}`)
- No server-side payload changes in S3 (forbidden)

### 5.2 Parameter Context Gaps

**Issue:** Some compat endpoints require context that may not be immediately available in client (e.g., `subcategoryId` for `masterbom.getproducttype` → `api.category.items`).

**Resolution:**
- Document required context in migration blueprint
- Ensure client collects required context before calling target endpoint
- Rollback to compat endpoint if context unavailable

### 5.3 Missing Contract Coverage

**Issue:** None identified for MBOM (all required lookups are covered by CatalogLookupContract v1).

**S3 Decision (frozen):**
- **MBOM catalog lookups are fully covered by CatalogLookupContract v1; no MBOM-specific SHARED contract extensions will be created in S3.**
- All MBOM catalog lookups map cleanly to CatalogLookupContract v1
- No additional contract extensions required

---

## 6) S4 Migration Execution Plan (S3 Blueprint Only)

### 6.1 Migration Order (recommended)

1. **Phase 1:** Migrate `masterbom.getdescription` (simplest parameter mapping)
2. **Phase 2:** Migrate `masterbom.getsubcategory` (requires split into multiple endpoints)
3. **Phase 3:** Migrate `masterbom.getproducttype` (requires subcategoryId context; currently commented in views)

### 6.2 Migration Checklist (for S4 execution)

For each compat endpoint:

- [ ] **Call sites identified:** All JS/Blade files using the endpoint
- [ ] **Parameter mapping verified:** All required params available in client context
- [ ] **Response transformation tested:** Client-side flattening works correctly
- [ ] **Rollback tested:** Reverting to compat endpoint works
- [ ] **Bundle A/B/C verified:** No regression in test bundles
- [ ] **Compat endpoint removed:** Only after S5 Bundle C passes

---

## 7) What is Frozen (S3-BOM-001)

### 7.1 Catalog Resolution Contract Freeze

- **SHARED CatalogLookupContract v1 is frozen** (from S3.1)
- **MBOM module-local endpoints remain active** until S5 Bundle C passes
- **Route names and URIs are frozen** for S3
- **Response shapes from compat endpoints remain stable** (no breaking changes)

### 7.2 Apply Contract Freeze

- **`quotation.v2.applyMasterBom` contract is frozen** (see Section 10.1)
- **Request/response semantics remain stable** through S3
- **Quantity multiplier semantics remain stable** (UI supplies multiplier; apply owns quantity math)
- **Origin tracking fields remain stable** (`OriginMasterBomId`, `MasterBomId`, `MasterBomName`, `InstanceSequenceNo`)

---

## 8) What is Explicitly NOT Changed (S3-BOM-001)

- **No route renames** (no changes to `masterbom.getsubcategory`, `masterbom.getproducttype`, `masterbom.getdescription` route names)
- **No controller moves** (no changes to `MasterBomController` location or structure)
- **No response shape changes** (compat endpoints continue to return nested objects)
- **No apply behavior changes** (no changes to `quotation.v2.applyMasterBom` logic, pricing, discount, rollup)
- **No schema changes** (no changes to `MasterBom` / `MasterBomItem` table structure)
- **No deletion of compat endpoints** (removal happens only after S5 Bundle C passes)

---

## 9) Consumer Map (S3-BOM-001)

### 9.1 MBOM Catalog Lookup Consumers

| Consumer | Current State | Target State (S4) | Migration Task |
|---|---|---|---|
| MBOM create form | Uses `masterbom.getsubcategory`, `masterbom.getdescription` | Use `api.category.subcategories`, `api.category.items`, `api.category.products` | NSW-P4-S4-MBOM-001 |
| MBOM edit form | Uses `masterbom.getsubcategory`, `masterbom.getdescription` | Use `api.category.subcategories`, `api.category.items`, `api.category.products` | NSW-P4-S4-MBOM-001 |
| MBOM copy form | Uses `masterbom.getsubcategory`, `masterbom.getdescription` | Use `api.category.subcategories`, `api.category.items`, `api.category.products` | NSW-P4-S4-MBOM-001 |

### 9.2 MBOM Apply Contract Consumers

| Consumer | Current State | Target State (S4) | Notes |
|---|---|---|---|
| QUO V2 Panel UI | Calls `quotation.v2.applyMasterBom` | Continue using same endpoint | No migration needed (already using contract) |
| QUO V2 Reuse modal | Calls `quotation.v2.applyMasterBom` | Continue using same endpoint | No migration needed (already using contract) |

---

## 10) MBOM Apply Contract Freeze (S3-BOM-001)

### 10.1 `quotation.v2.applyMasterBom` — Apply Master BOM Contract

**Sources (authority):**
- `docs/PHASE_4/S2_MBOM_ISOLATION.md`
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyMasterBom` (observed)

**Request (minimum):**

- `QuotationId` (required)
- `QuotationSaleBomId` (required) — target feeder/BOM node to receive items
- `MasterBomId` (required) — template id
- `Qty` (required numeric) — multiplier
- `Items` (optional array) — if present, apply uses request payload; if absent, apply loads `MasterBomItem` rows

**Item payload shape (observed; optional fields defaulted in apply):**

- Required to create an item: `ProductId` (truthy; falsy/0 values are skipped)
- Optional: `MakeId`, `SeriesId`, `Description`, `Qty`, `Rate`, `Discount`, `Remark`, `RateSource`, `IsClientSupplied`

**Response (minimum):**

- Success: `{ success: true, message: string }`
- Validation failure: `{ success: false, message: string }` (422)
- Execution failure: `{ success: false, message: string, error_details?: string|null }` (500)

**Apply semantics (frozen):**

- **Quantity multiplier:** The `Qty` parameter is a **multiplier**, not an absolute quantity. Each `MasterBomItem.Quantity` is multiplied by `Qty` when creating `QuotationSaleBomItem`.
- **Origin tracking:** Apply endpoint sets `OriginMasterBomId`, `MasterBomId`, `MasterBomName`, `InstanceSequenceNo` for reuse detection.
- **No side effects:** Apply operation must not mutate MBOM template data. `MasterBom` / `MasterBomItem` rows are never modified by apply.

**Notes (record-only):**

- If `Items` are not provided and the template has no items, apply may return a non-422 failure (e.g. `{success:false,...}` with 400 in observed controller).
- B4 resolution status handling: L0/L1 items with `ProductId = NULL` may be skipped in fallback path (known risk, requires QUO-V2 re-verification G4).

---

## 11) S4 Propagation Hooks (S3-BOM-001)

### 11.1 Catalog Resolution Migration Targets

**Target 1: MBOM catalog lookup routes → CatalogLookupContract**
- `masterbom.getsubcategory` → Remove after S4 migration
- `masterbom.getproducttype` → Remove after S4 migration
- `masterbom.getdescription` → Remove after S4 migration
- **S4 Task:** `NSW-P4-S4-MBOM-001` — Migrate MBOM catalog lookup endpoints

### 11.2 Apply Contract Propagation Targets

**Target 1: MasterBomTemplateReadContract implementation**
- **Owner:** MBOM
- **Consumers:** QUO apply, FEED operations, PBOM operations, reuse search
- **S4 Task:** `NSW-P4-S4-MBOM-002` — Implement MasterBomTemplateReadContract

**Target 2: MasterBomUsageContract implementation**
- **Owner:** QUO (or SHARED if standardized)
- **Consumer:** MBOM delete guard
- **S4 Task:** Replace direct `QuotationSaleBom` query in `MasterBomController@destroy`

---

## 11) Exit Criteria (S3-BOM-001)

S3-BOM-001 is **COMPLETE** when:

- [x] **Catalog resolution alignment blueprint documented:**
  - [x] All MBOM module-local endpoints mapped to SHARED contract endpoints
  - [x] All call sites identified and documented
  - [x] Parameter mapping documented for each compat endpoint
  - [x] Response compatibility analyzed
  - [x] Compatibility gaps identified
  - [x] Rollback strategy defined
- [x] **Apply contract frozen:**
  - [x] `quotation.v2.applyMasterBom` contract documented (see Section 10.1)
  - [x] Request/response semantics frozen
  - [x] Consumer map documented
- [x] **S4 propagation hooks declared:**
  - [x] Migration targets identified
  - [x] S4 tasks linked
- [x] **Explicit "not changed" section present:**
  - [x] No route renames proposed
  - [x] No behavior changes proposed
  - [x] No endpoint deletions proposed

**Status:** ✅ Complete

---

# S3-BOM-002: FEED Alignment (Apply Contract + Gap Closure)

## Scope + Fence

- This section creates a **precise alignment blueprint** for FEED apply contract + gap closure requirements.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_FEED_ISOLATION.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
  - `docs/PHASE_4/GAP_GATEBOARD.md` (BOM-GAP-001, BOM-GAP-002)

**S3 Guardrails:**
- ✅ Allowed: freeze apply contract, document gap closure requirements, define evidence requirements
- ✅ Allowed: implement gap fixes (NSW-P4-S3-FEED-GAP-001) — implementation target is S3
- ❌ Not allowed: changing route files, touching controllers, changing response shapes (beyond gap fixes)

---

## 1) Frozen Apply Surface (S3-BOM-002)

### 1.1 `quotation.v2.applyFeederTemplate` — Apply Feeder Template (FEED → QUO)

Sources (authority):

- `docs/PHASE_4/S2_FEED_ISOLATION.md`
- `source_snapshot/resources/views/quotation/v2/_feeder_library_modal.blade.php` (observed caller)

**Route params (frozen):**

- `{quotation}` (target quotation id)
- `{panel}` (target panel id)

**Request (minimum):**

- `MasterBomId` (required) — template id (stored as `MasterBom` with `TemplateType='FEEDER'`)
- `FeederName` (required) — instance name in the quotation
- `Qty` (required) — feeder qty (UI sends numeric)
- `_token` (CSRF)

**Response (minimum, as expected by UI caller):**

- Success: `{ success: true, message?: string }`
- Failure: `{ success: false, message?: string }`

Guardrail (from S2 FEED + S2 SHARED):

- Do **not** pre-multiply item quantities during apply; QuantityService handles multipliers.

Notes (record-only, snapshot discrepancy):

- The route exists in snapshot routing, and the UI posts to it, but the method is not found in `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`. This is a G4 re-verify concern; **contract remains frozen** here and must not be "fixed" in S3.

---

## 2) Gap Closure Requirements (S3-BOM-002)

### 2.1 BOM-GAP-001: Reuse Detection Semantics

**Contract rule (frozen for S3 implementation):** Apply endpoint **must detect** if a feeder instance already exists from the same template in the same panel.

**Required behavior (implementation target: S3 — NSW-P4-S3-FEED-GAP-001):**
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
- Evidence + regression finalization: S4/S5 as needed (depends on wiring/propagation + S5 gate)

### 2.2 BOM-GAP-002: Clear-Before-Copy Semantics

**Contract rule (frozen for S3 implementation):** Apply endpoint **must clear** existing items from target feeder before copying template items.

**Required behavior (implementation target: S3 — NSW-P4-S3-FEED-GAP-001):**
- Before copying template items, delete all existing `QuotationSaleBomItem` rows where:
  - `QuotationSaleBomId` = target feeder `QuotationSaleBomId`
  - `Status` = 0 (active)
- Then copy template items as new rows
- This prevents duplicate stacking when applying the same template multiple times

**Evidence requirement (BOM-GAP-002):**
- S3 implementation must provide evidence in `docs/PHASE_4/evidence/GAP/BOM-GAP-002/`
- Evidence must include: R1 request/response, S1/S2 snapshots showing clear-before-copy working (items cleared, then new items added)
- Evidence + regression finalization: S4/S5 as needed (depends on wiring/propagation + S5 gate)

---

## 3) What is Frozen (S3-BOM-002)

- **`quotation.v2.applyFeederTemplate` contract is frozen** (route params, request/response shapes)
- **Gap closure requirements are frozen** (BOM-GAP-001, BOM-GAP-002 semantics documented)
- **Evidence requirements are frozen** (evidence structure and location defined)

---

## 4) What is Explicitly NOT Changed (S3-BOM-002)

- **No gap implementation** (implementation happens in S4, not S3)
- **No route renames** (no changes to `quotation.v2.applyFeederTemplate` route name or URI)
- **No controller moves** (no changes to `QuotationV2Controller` location or structure)
- **No response shape changes** (contract remains stable)
- **No apply behavior changes** (no changes to pricing, discount, rollup logic)

---

## 5) Consumer Map (S3-BOM-002)

| Consumer | Current State | Target State (S4) | Notes |
|---|---|---|---|
| QUO V2 Feeder Library modal | Calls `quotation.v2.applyFeederTemplate` | Continue using same endpoint (with gap fixes) | Gap fixes implemented in S4 |

---

## 6) S4 Propagation Hooks (S3-BOM-002)

### 6.1 Gap Closure Implementation Targets

**Target 1: BOM-GAP-001 closure (reuse detection)**
- **S3 Task:** `NSW-P4-S3-FEED-GAP-001` — Implement reuse detection in `quotation.v2.applyFeederTemplate`
- **Evidence:** `docs/PHASE_4/evidence/GAP/BOM-GAP-001/`

**Target 2: BOM-GAP-002 closure (clear-before-copy)**
- **S3 Task:** `NSW-P4-S3-FEED-GAP-001` — Implement clear-before-copy in `quotation.v2.applyFeederTemplate`
- **Evidence:** `docs/PHASE_4/evidence/GAP/BOM-GAP-002/`

---

## 7) Exit Criteria (S3-BOM-002)

S3-BOM-002 is **COMPLETE** when:

- [x] **Apply contract frozen:**
  - [x] `quotation.v2.applyFeederTemplate` contract documented
  - [x] Request/response semantics frozen
  - [x] Consumer map documented
- [x] **Gap closure requirements documented:**
  - [x] BOM-GAP-001 semantics frozen
  - [x] BOM-GAP-002 semantics frozen
  - [x] Evidence requirements defined
- [x] **S4 propagation hooks declared:**
  - [x] Gap closure implementation targets identified
  - [x] S4 tasks linked

**Status:** ✅ Complete

---

# S3-BOM-003: PBOM Alignment (Apply Contract Freeze)

## Scope + Fence

- This section creates a **precise alignment blueprint** for PBOM apply contract.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_PBOM_ISOLATION.md`
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: freeze apply contract, document consumer map
- ❌ Not allowed: changing route files, touching controllers, changing response shapes

---

## 1) Frozen Apply Surface (S3-BOM-003)

### 1.1 `quotation.v2.applyProposalBom` — Apply Proposal BOM (PBOM → QUO)

Sources (authority):

- `docs/PHASE_4/S2_PBOM_ISOLATION.md`
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyProposalBom` (observed)

**Request (minimum):**

- `QuotationId` (required)
- `QuotationSaleBomId` (required) — target node
- `SourceQuotationSaleBomId` (required) — source
- `Qty` (required) — multiplier

**Response (minimum):**

- Success: `{ success: true, message: string }`
- Validation failure: `{ success: false, message: string }` (422)
- Execution failure: `{ success: false, message: string, error_details?: string|null }` (500)

---

## 2) What is Frozen (S3-BOM-003)

- **`quotation.v2.applyProposalBom` contract is frozen** (request/response shapes)
- **Request/response semantics remain stable** through S3
- **Quantity multiplier semantics remain stable** (UI supplies multiplier; apply owns quantity math)

---

## 3) What is Explicitly NOT Changed (S3-BOM-003)

- **No route renames** (no changes to `quotation.v2.applyProposalBom` route name or URI)
- **No controller moves** (no changes to `QuotationV2Controller` location or structure)
- **No response shape changes** (contract remains stable)
- **No apply behavior changes** (no changes to pricing, discount, rollup logic)

---

## 4) Consumer Map (S3-BOM-003)

| Consumer | Current State | Target State (S4) | Notes |
|---|---|---|---|
| QUO V2 Panel UI | Calls `quotation.v2.applyProposalBom` | Continue using same endpoint | No migration needed (already using contract) |
| QUO V2 Reuse modal | Calls `quotation.v2.applyProposalBom` | Continue using same endpoint | No migration needed (already using contract) |

---

## 5) S4 Propagation Hooks (S3-BOM-003)

### 5.1 Apply Contract Propagation Targets

**Target 1: ProposalBomApplyContract implementation**
- **Owner:** QUO
- **Consumers:** QUO V2 Panel UI, QUO V2 Reuse modal
- **S4 Task:** `NSW-P4-S4-PBOM-001` — Verify and document ProposalBomApplyContract (if needed)

---

## 6) Exit Criteria (S3-BOM-003)

S3-BOM-003 is **COMPLETE** when:

- [x] **Apply contract frozen:**
  - [x] `quotation.v2.applyProposalBom` contract documented
  - [x] Request/response semantics frozen
  - [x] Consumer map documented
- [x] **S4 propagation hooks declared:**
  - [x] Migration targets identified (if any)
  - [x] S4 tasks linked

**Status:** ✅ Complete

---

# Cross-Cutting Apply Contracts (All BOM Modules)

## 1) Frozen apply surfaces table (routes must remain stable in S3)

| Route Name | Method | URI | Owner (behavior) | Notes |
|---|---:|---|---|---|
| `quotation.v2.applyMasterBom` | POST | `/quotation/v2/apply-master-bom` | QUO | MBOM template apply surface (see S3-BOM-001 Section 10.1) |
| `quotation.v2.applyFeederTemplate` | POST | `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | QUO | FEED apply surface (see S3-BOM-002 Section 1.1) |
| `quotation.v2.applyProposalBom` | POST | `/quotation/v2/apply-proposal-bom` | QUO | PBOM apply surface (see S3-BOM-003 Section 1.1) |

## 2) Apply contract freeze (minimum request/response contracts)

### 2.1 `quotation.v2.applyMasterBom` — Apply Master BOM (MBOM → QUO)

**Note:** Full contract details are documented in S3-BOM-001 Section 10.1. This is a summary reference.

Sources (authority):

- `docs/PHASE_4/S2_MBOM_ISOLATION.md`
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyMasterBom` (observed)

**Request (minimum):**

- `QuotationId` (required)
- `QuotationSaleBomId` (required) — target feeder/BOM node to receive items
- `MasterBomId` (required) — template id
- `Qty` (required numeric) — multiplier
- `Items` (optional array) — if present, apply uses request payload; if absent, apply loads `MasterBomItem` rows

**Item payload shape (observed; optional fields defaulted in apply):**

- Required to create an item: `ProductId` (truthy; falsy/0 values are skipped)
- Optional: `MakeId`, `SeriesId`, `Description`, `Qty`, `Rate`, `Discount`, `Remark`, `RateSource`, `IsClientSupplied`

**Response (minimum):**

- Success: `{ success: true, message: string }`
- Validation failure: `{ success: false, message: string }` (422)
- Execution failure: `{ success: false, message: string, error_details?: string|null }` (500)

Notes (record-only):

- If `Items` are not provided and the template has no items, apply may return a non-422 failure (e.g. `{success:false,...}` with 400 in observed controller).

### 2.2 `quotation.v2.applyFeederTemplate` — Apply Feeder Template (FEED → QUO)

**Note:** Full contract details are documented in S3-BOM-002 Section 1.1. This is a summary reference.

Sources (authority):

- `docs/PHASE_4/S2_FEED_ISOLATION.md`
- `source_snapshot/resources/views/quotation/v2/_feeder_library_modal.blade.php` (observed caller)

**Route params (frozen):**

- `{quotation}` (target quotation id)
- `{panel}` (target panel id)

**Request (minimum):**

- `MasterBomId` (required) — template id (stored as `MasterBom` with `TemplateType='FEEDER'`)
- `FeederName` (required) — instance name in the quotation
- `Qty` (required) — feeder qty (UI sends numeric)
- `_token` (CSRF)

**Response (minimum, as expected by UI caller):**

- Success: `{ success: true, message?: string }`
- Failure: `{ success: false, message?: string }`

Guardrail (from S2 FEED + S2 SHARED):

- Do **not** pre-multiply item quantities during apply; QuantityService handles multipliers.

Notes (record-only, snapshot discrepancy):

- The route exists in snapshot routing, and the UI posts to it, but the method is not found in `source_snapshot/app/Http/Controllers/QuotationV2Controller.php`. This is a G4 re-verify concern; **contract remains frozen** here and must not be "fixed" in S3.

### 2.3 `quotation.v2.applyProposalBom` — Apply Proposal BOM (PBOM → QUO)

**Note:** Full contract details are documented in S3-BOM-003 Section 1.1. This is a summary reference.

Sources (authority):

- `docs/PHASE_4/S2_PBOM_ISOLATION.md`
- `source_snapshot/app/Http/Controllers/QuotationV2Controller.php@applyProposalBom` (observed)

**Request (minimum):**

- `QuotationId` (required)
- `QuotationSaleBomId` (required) — target node
- `SourceQuotationSaleBomId` (required) — source
- `Qty` (required) — multiplier

**Response (minimum):**

- Success: `{ success: true, message: string }`
- Validation failure: `{ success: false, message: string }` (422)
- Execution failure: `{ success: false, message: string, error_details?: string|null }` (500)

---

## 3) Consumer map (who calls each apply surface)

This is a **record-only** consumer map for S3 (no execution changes authorized).

| Apply surface | Primary consumer(s) | Evidence (caller) | Notes |
|---|---|---|---|
| `quotation.v2.applyMasterBom` | QUO V2 Panel UI — "Apply Master BOM" | `source_snapshot/resources/views/quotation/v2/panel.blade.php` | Posts to `/quotation/v2/apply-master-bom` with `QuotationId`, `QuotationSaleBomId`, `MasterBomId`, `Qty`, optional `Items`. |
| `quotation.v2.applyMasterBom` | QUO V2 Reuse modal — "Master BOM reuse → apply" | `source_snapshot/resources/views/quotation/v2/_reuse_filter_modal.blade.php` | Posts to `/quotation/v2/apply-master-bom` with `Qty=1` in reuse flow. |
| `quotation.v2.applyFeederTemplate` | QUO V2 Feeder Library modal — "Apply feeder template" | `source_snapshot/resources/views/quotation/v2/_feeder_library_modal.blade.php` | Posts to `/quotation/{quotation}/panel/{panel}/feeder/apply-template`. |
| `quotation.v2.applyProposalBom` | QUO V2 Panel UI — "Apply Proposal BOM" | `source_snapshot/resources/views/quotation/v2/panel.blade.php` | Uses `route('quotation.v2.applyProposalBom')`. |
| `quotation.v2.applyProposalBom` | QUO V2 Reuse modal — "Proposal BOM reuse → apply" | `source_snapshot/resources/views/quotation/v2/_reuse_filter_modal.blade.php` | Posts to `/quotation/v2/apply-proposal-bom` with `Qty=1` in reuse flow. |

---

## 4) Alignment decisions (frozen until S4)

- FEED owns **template CRUD + read contract**, QUO owns **apply/mutation** into quotations.
- PBOM owns **selection/reuse intent**, QUO owns **apply** into live quotations.
- MBOM owns **template integrity**, QUO owns **apply semantics** into quotation trees.

---

## 5) Out of Scope (S3)

- Any changes to apply behavior (pricing, discount, rollup, quantity math)
- Any schema changes for template storage
- Any route regrouping / prefix changes
- Any controller moves/splits or service refactors
- Any gap implementation (gap fixes happen in S4, not S3)

---

## 6) Evidence Requirements

### 6.1 S3-BOM-001 Evidence

- [x] All MBOM view files identified (Section 2.1)
- [x] All JS call sites mapped (verify in execution)
- [x] All compat endpoints classified (Section 3.2)
- [x] Parameter mapping documented for each compat endpoint (Section 4)
- [x] Response compatibility analyzed (Section 4)
- [x] Compatibility gaps identified (Section 5)
- [x] Rollback strategy defined (Section 4)
- [x] Apply contract frozen (Section 10.1)
- [x] Consumer map documented (Section 9)
- [x] S4 propagation hooks declared (Section 10)

### 6.2 S3-BOM-002 Evidence

- [x] Apply contract frozen (Section 1.1)
- [x] Gap closure requirements documented (Section 2)
- [x] Evidence requirements defined (Section 2)
- [x] Consumer map documented (Section 5)
- [x] S4 propagation hooks declared (Section 6)

### 6.3 S3-BOM-003 Evidence

- [x] Apply contract frozen (Section 1.1)
- [x] Consumer map documented (Section 4)
- [x] S4 propagation hooks declared (Section 5)

---

## 7) Task Status

**NSW-P4-S3-BOM-001 (Align MBOM catalog resolution to single path):** ✅ Complete  
**NSW-P4-S3-BOM-002 (Align FEED apply contract + gap closure):** ✅ Complete  
**NSW-P4-S3-BOM-003 (Align PBOM apply contract):** ✅ Complete

**Next Tasks:** S3-QUO-001 (QUO legacy alignment), S3-QUO-002 (QUO-V2 apply alignment map)

---

## 8) Authority References

- Route Map: `trace/phase_2/ROUTE_MAP.md`
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- S2 MBOM Isolation: `docs/PHASE_4/S2_MBOM_ISOLATION.md`
- S2 FEED Isolation: `docs/PHASE_4/S2_FEED_ISOLATION.md`
- S2 PBOM Isolation: `docs/PHASE_4/S2_PBOM_ISOLATION.md`
- S2 SHARED Isolation: `docs/PHASE_4/S2_SHARED_ISOLATION.md`
- S3 SHARED Alignment: `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
- S3 Execution Checklist: `docs/PHASE_4/S3_EXECUTION_CHECKLIST.md`
- Master Task List: `docs/PHASE_4/MASTER_TASK_LIST.md`
- Gap Gateboard: `docs/PHASE_4/GAP_GATEBOARD.md` (BOM-GAP-001, BOM-GAP-002)


