# Batch-S4-2: CP0 Baseline Checkpoint

**Batch:** S4-2 (CIM Propagation)  
**Checkpoint:** CP0 (Baseline)  
**Date:** 2025-12-24  
**Status:** ✅ **BASELINE LOCKED**  
**Authority:** S4-GOV-001, S3_CIM_ALIGNMENT.md, BATCH_S4_2_HANDOFF.md

---

## CP0 Purpose

CP0 establishes the baseline state before Batch-S4-2 execution. This checkpoint documents:
- Current git commit hash (rollback point)
- All SHARED routes (13 endpoints)
- All CIM COMPAT endpoints (4 endpoints)
- CIM call-site inventory (views/JS files)
- Scope lock for Batch-S4-2
- Rollback command

**This baseline must remain unchanged until Batch-S4-2 CP3 closure.**

---

## 1. Git Baseline

**Git Commit Hash:** `1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`

**Baseline Date:** 2025-12-24

**Rollback Command:**
```bash
git reset --hard 1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0
```

**Note:** This is the same commit as Batch-S4-1 CP0 (Batch-S4-1 did not modify CIM consumers).

---

## 2. Route Snapshot

### 2.1 SHARED Routes (13 endpoints)

**Location:** `source_snapshot/routes/web.php` (lines 51-97)

**Route Group:** `Route::group(['middleware' => 'auth', 'prefix' => 'api'], ...)`

| Route Name | Method | URI | Handler | Middleware | Status |
|---|---|---|---:|---|---|
| `api.category.subcategories` | GET | `/api/category/{categoryId}/subcategories` | `QuotationController@getSubCategories` | `auth`, `throttle:search` | ✅ Active |
| `api.category.items` | GET | `/api/category/{categoryId}/items` | `QuotationController@getItems` | `auth`, `throttle:search` | ✅ Active |
| `api.category.products` | GET | `/api/category/{categoryId}/products` | `QuotationController@getProducts` | `auth`, `throttle:search` | ✅ Active |
| `api.item.products` | GET | `/api/item/{itemId}/products` | `QuotationController@getProductsByItem` | `auth`, `throttle:search` | ✅ Active |
| `api.product.makes` | GET | `/api/product/{productId}/makes` | `QuotationController@getMakes` | `auth`, `throttle:search` | ✅ Active |
| `api.make.series` | GET | `/api/make/{makeId}/series` | `QuotationController@getSeriesApi` | `auth`, `throttle:search` | ✅ Active |
| `api.product.descriptions` | GET | `/api/product/{productId}/descriptions` | `QuotationController@getDescriptions` | `auth`, `throttle:search` | ✅ Active |
| `api.category.makes` | GET | `/api/category/{categoryId}/makes` | `QuotationController@getMakesByCategory` | `auth`, `throttle:search` | ✅ Active |
| `api.makes` | GET | `/api/makes` | `QuotationController@getAllMakes` | `auth`, `throttle:search` | ✅ Active |
| `api.reuse.panels` | GET | `/api/reuse/panels` | `ReuseController@getPanels` | `auth`, `throttle:search` | ✅ Active |
| `api.reuse.feeders` | GET | `/api/reuse/feeders` | `ReuseController@getFeeders` | `auth`, `throttle:search` | ✅ Active |
| `api.reuse.masterBoms` | GET | `/api/reuse/masterBoms` | `ReuseController@getMasterBoms` | `auth`, `throttle:search` | ✅ Active |
| `api.reuse.proposalBoms` | GET | `/api/reuse/proposalBoms` | `ReuseController@getProposalBoms` | `auth`, `throttle:search` | ✅ Active |

**Service Wiring Status:**
- ✅ All 9 catalog endpoints wired to `CatalogLookupService` (via `CatalogLookupContract`)
- ✅ All 4 reuse endpoints wired to `ReuseSearchService` (via `ReuseSearchContract`)
- ✅ Services created in Batch-S4-1 (CP3 complete)

### 2.2 CIM COMPAT Endpoints (4 endpoints)

**Location:** `source_snapshot/routes/web.php` (lines 216-219)

| Route Name | Method | URI | Handler | Current Payload | Target SHARED Endpoint | Status |
|---|---|---|---:|---|---|---|
| `product.getsubcategory` | GET | `/product/getsubcategory/{id}` | `ProductController@getsubcategory` | `{ subcategory: [...], producttype: [...], attribute: [...], make: [...] }` | Split: `api.category.subcategories` + `api.category.items` + `api.category.makes` | ✅ Active (COMPAT) |
| `product.getproducttype` | GET | `/product/getproducttype/{id}` | `ProductController@getproducttype` | `{ producttype: [{ItemId,Name}] }` | `api.category.items` with `?subcategory={subCategoryId}` | ✅ Active (COMPAT) |
| `product.getseries` | GET | `/product/getseries` | `ProductController@getseries` | `{ series: [{SeriesId,Name}] }` (requires `CategoryId`, `MakeId`) | `api.make.series` with `{makeId}` + `categoryId` query | ✅ Active (COMPAT) |
| `product.getgeneric` | GET | `/product/getgeneric` | `ProductController@getgeneric` | `{ description: [{ProductId,Name}] }` (filters: CategoryId/SubCategoryId/ItemId; ProductType=1) | `api.category.products` with `subcategoryId` + `itemId` inputs | ✅ Active (COMPAT) |

**COMPAT Lifecycle Policy:**
- ✅ COMPAT endpoints remain active during Batch-S4-2 migration
- ✅ COMPAT endpoints must NOT be deleted in Batch-S4-2
- ✅ COMPAT endpoints serve as fallback until S5 Bundle-C passes
- ✅ COMPAT endpoints will be deprecated but not removed

---

## 3. CIM Call-Site Inventory

**Reference:** `docs/PHASE_4/S3_CIM_ALIGNMENT.md` (Section 2.1, Section 4)

### 3.1 CIM View Files (Call Sites)

| Consumer (module/screen) | View File | Current COMPAT Endpoints Used | JS/Blade Location | Migration Target |
|---|---|---|---|---|
| CIM — Specific Product (create) | `source_snapshot/resources/views/product/create.blade.php` | `product.getsubcategory`, `product.getseries`, `product.getgeneric` | TBD (verify in execution) | `api.category.subcategories`, `api.make.series`, `api.category.products` |
| CIM — Specific Product (edit) | `source_snapshot/resources/views/product/edit.blade.php` | `product.getsubcategory`, `product.getproducttype`, `product.getseries`, `product.getgeneric` | TBD (verify in execution) | `api.category.subcategories`, `api.category.items`, `api.make.series`, `api.category.products` |
| CIM — Generic Product (create) | `source_snapshot/resources/views/generic/create.blade.php` | `source_snapshot/resources/views/generic/create.blade.php` | `product.getsubcategory` | TBD (verify in execution) | `api.category.subcategories` |
| CIM — Generic Product (edit) | `source_snapshot/resources/views/generic/edit.blade.php` | `product.getsubcategory`, `product.getproducttype` | TBD (verify in execution) | `api.category.subcategories`, `api.category.items` |

**Migration Order (from S3_CIM_ALIGNMENT.md Section 6.1):**
1. **Phase 1:** Migrate `product.getgeneric` (simplest parameter mapping)
2. **Phase 2:** Migrate `product.getproducttype` (requires subcategoryId context)
3. **Phase 3:** Migrate `product.getseries` (requires MakeId context)
4. **Phase 4:** Migrate `product.getsubcategory` (most complex, includes attributes gap)

### 3.2 JS Call Sites (To Be Verified in CP1)

**Note:** Exact JS call sites will be verified during CP1 execution. The following are expected locations based on S3_CIM_ALIGNMENT.md:

- `product/create.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)
- `product/edit.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)
- `generic/create.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)
- `generic/edit.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)

**Verification Required in CP1:**
- [ ] Identify all AJAX call sites in each view file
- [ ] Document parameter mapping for each call
- [ ] Document response transformation requirements
- [ ] Verify context availability (subcategoryId, MakeId, etc.)

---

## 4. Batch-S4-2 Scope Lock

### 4.1 In Scope (✅ Allowed)

**Consumer Migration:**
- ✅ Update CIM views/JavaScript to call `/api/*` SHARED endpoints
- ✅ Update CIM JavaScript to use new endpoint URIs and parameter formats
- ✅ Add client-side response transformation (flatten nested objects to `{id,label}` arrays)
- ✅ Verify CIM functionality after migration (dropdowns, searches work correctly)

**COMPAT Endpoint Lifecycle:**
- ✅ Keep COMPAT endpoints alive (no deletions)
- ✅ COMPAT endpoints remain available as fallback
- ✅ COMPAT endpoints remain unmodified (no changes to handlers or payloads)

**Testing:**
- ✅ Smoke test CIM screens (create/edit for product and generic)
- ✅ Verify dropdown population works correctly
- ✅ Verify search functionality works correctly
- ✅ Verify no breaking changes to CIM workflows

### 4.2 Out of Scope (❌ Forbidden)

**Payload Changes:**
- ❌ No payload shape changes (response shapes must remain stable)
- ❌ No field additions/removals
- ❌ No data structure modifications

**Route Changes:**
- ❌ No route renames (URIs must remain stable)
- ❌ No route URI changes
- ❌ No middleware changes
- ❌ No route file migrations (`web.php` → `api.php`)

**COMPAT Endpoint Modifications:**
- ❌ No COMPAT endpoint deletions (must remain until S5 Bundle-C)
- ❌ No COMPAT endpoint modifications (keep as-is for fallback)
- ❌ No breaking COMPAT endpoint behavior

**Other Modules:**
- ❌ No MBOM consumer migration (deferred to Batch-S4-3)
- ❌ No QUO consumer migration (deferred to Batch-S4-4)
- ❌ No QUO-V2 touches (PROTECTED zone remains fenced)
- ❌ No FEED/PBOM consumer migrations

**Controller Changes:**
- ❌ No controller extraction (endpoints remain in existing controllers)
- ❌ No controller refactoring beyond what's needed for migration

---

## 5. Migration Blueprint Reference

**Primary Reference:** `docs/PHASE_4/S3_CIM_ALIGNMENT.md`

**Key Sections:**
- Section 3.2: COMPAT endpoint classification
- Section 4: Migration blueprint for each COMPAT endpoint
- Section 5: Compatibility gaps & resolution strategy
- Section 6: Migration execution plan

**Parameter Mapping (from S3_CIM_ALIGNMENT.md):**

1. **`product.getgeneric` → `api.category.products`:**
   - Current: `CategoryId`, `SubCategoryId`, `ItemId` (query params)
   - Target: `{categoryId}` (path param) + `?subcategoryId={subCategoryId}&itemId={itemId}` (query params)

2. **`product.getproducttype` → `api.category.items`:**
   - Current: `{id}` (path param) → categoryId
   - Target: `{categoryId}` (path param) + `?subcategory={subCategoryId}` (query param)
   - **Gap:** Requires subcategoryId to be available in client context

3. **`product.getseries` → `api.make.series`:**
   - Current: `CategoryId`, `MakeId` (query params)
   - Target: `{makeId}` (path param) + `categoryId` (query param, if required)
   - **Gap:** Requires MakeId to be available in client context

4. **`product.getsubcategory` → Multiple endpoints:**
   - Current: `{id}` (path param) → categoryId
   - Target: Split into `api.category.subcategories`, `api.category.items`, `api.category.makes`
   - **Gap:** Attributes are not in CatalogLookupContract (must be handled separately)

**Response Transformation (from S3_CIM_ALIGNMENT.md Section 5.1):**
- Current COMPAT endpoints return nested objects (e.g., `{ subcategory: [...] }`)
- SHARED endpoints return flat arrays `[{id, label}]`
- Client-side transformation required: extract nested arrays, flatten to `{id,label}`

---

## 6. Stop Conditions

**Stop Conditions (from S4-GOV-001):**
- ❌ Breaking payload shape change detected → **STOP IMMEDIATELY**
- ❌ COMPAT endpoint removed prematurely → **STOP IMMEDIATELY**
- ❌ CIM functionality broken → **STOP IMMEDIATELY**
- ❌ Route changes detected → **STOP IMMEDIATELY**
- ❌ QUO-V2 PROTECTED touch without G4 → **STOP IMMEDIATELY**

**Rollback Trigger:**
- If any stop condition is triggered, rollback to CP0 baseline using:
  ```bash
  git reset --hard 1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0
  ```

---

## 7. Service Availability

**SHARED Services (Ready for Consumer Adoption):**

**CatalogLookupService:**
- **Location:** `app/Services/Shared/CatalogLookupService.php`
- **Contract:** `app/Contracts/Shared/CatalogLookupContract.php`
- **Status:** ✅ Wired behind existing routes (Batch-S4-1 CP3 complete)
- **Endpoints:** All 9 catalog endpoints use this service

**ReuseSearchService:**
- **Location:** `app/Services/Shared/ReuseSearchService.php`
- **Contract:** `app/Contracts/Shared/ReuseSearchContract.php`
- **Status:** ✅ Wired behind existing routes (Batch-S4-1 CP3 complete)
- **Endpoints:** All 4 reuse endpoints use this service

**Service Wiring:**
- ✅ Services created in Batch-S4-1
- ✅ Services verified in Batch-S4-1 CP2 (6/6 smoke tests passed)
- ✅ Services ready for consumer adoption in Batch-S4-2

---

## 8. Authority References

**Governance:**
- `docs/PHASE_4/S4_GOV_001_PROPAGATION_ORDER.md` - Propagation order and governance rules

**S3 Blueprints:**
- `docs/PHASE_4/S3_CIM_ALIGNMENT.md` - CIM alignment blueprint (migration plan)
- `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` - SHARED alignment (frozen contracts)

**Batch-S4-1 Evidence:**
- `docs/PHASE_4/evidence/BATCH_S4_1_CP0_BASELINE.md` - Batch-S4-1 baseline
- `docs/PHASE_4/evidence/BATCH_S4_1_CP2_VERIFICATION.md` - Batch-S4-1 verification
- `docs/PHASE_4/evidence/BATCH_S4_1_CP3_EVIDENCE_PACK.md` - Batch-S4-1 closure

**Handoff:**
- `docs/PHASE_4/evidence/BATCH_S4_2_HANDOFF.md` - Batch-S4-1 to Batch-S4-2 handoff

---

## 9. CP0 Lock Statement

**Baseline Status:** ✅ **LOCKED**

**This CP0 baseline establishes:**
- ✅ Git commit hash for rollback: `1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`
- ✅ 13 SHARED routes documented and verified
- ✅ 4 CIM COMPAT endpoints documented
- ✅ CIM call-site inventory referenced (S3_CIM_ALIGNMENT.md)
- ✅ Scope lock defined (in-scope and out-of-scope items)
- ✅ Migration blueprint referenced
- ✅ Stop conditions defined
- ✅ Service availability confirmed

**This baseline must remain unchanged until Batch-S4-2 CP3 closure.**

---

**CP0 Locked:** 2025-12-24  
**Batch-S4-2 Status:** ⏳ **READY FOR CP1**  
**Next Checkpoint:** CP1 (CIM Consumer Migration)

