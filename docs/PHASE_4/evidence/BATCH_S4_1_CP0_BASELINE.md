# Batch-S4-1: CP0 Baseline Checkpoint

**Batch:** S4-1 (SHARED Contract Propagation)  
**Checkpoint:** CP0 (Baseline)  
**Date:** 2025-12-18  
**Status:** ✅ RECORDED  
**Authority:** S4-GOV-001, S4_BATCH_1_TASKS.md

---

## CP0 Purpose

CP0 establishes the known-good baseline state before any code changes. This checkpoint enables safe rollback to a stable state if stop conditions are triggered during Batch-S4-1 execution.

---

## 1. Git Baseline

### Commit Hash
```
1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0
```

### Branch
- Current branch will be verified at execution start
- Baseline commit must be tagged or documented for rollback reference

### Verification Command
```bash
git rev-parse HEAD
git log --oneline -1
```

---

## 2. Routes Snapshot (SHARED Contract Endpoints)

### 2.1 CatalogLookupContract Routes

All routes currently hosted in `QuotationController` (implementation reality). Routes defined in `routes/web.php` with `/api` prefix and `auth, throttle:search` middleware.

| Route Name | Method | URI | Current Controller@Method | Middleware | Contract Owner |
|------------|--------|-----|---------------------------|------------|----------------|
| `api.category.subcategories` | GET | `/api/category/{categoryId}/subcategories` | `QuotationController@getSubCategories` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.category.items` | GET | `/api/category/{categoryId}/items` | `QuotationController@getItems` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.category.products` | GET | `/api/category/{categoryId}/products` | `QuotationController@getProducts` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.item.products` | GET | `/api/item/{itemId}/products` | `QuotationController@getProductsByItem` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.product.makes` | GET | `/api/product/{productId}/makes` | `QuotationController@getMakes` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.make.series` | GET | `/api/make/{makeId}/series` | `QuotationController@getSeriesApi` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.product.descriptions` | GET | `/api/product/{productId}/descriptions` | `QuotationController@getDescriptions` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.category.makes` | GET | `/api/category/{categoryId}/makes` | `QuotationController@getMakesByCategory` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.makes` | GET | `/api/makes` | `QuotationController@getAllMakes` | auth, throttle:search | **SHARED** (S3 frozen) |

**Total CatalogLookupContract routes:** 9 endpoints

### 2.2 ReuseSearchContract Routes

All routes currently hosted in `ReuseController` (implementation reality). Routes defined in `routes/web.php` with `/api` prefix and `auth, throttle:search` middleware.

| Route Name | Method | URI | Current Controller@Method | Middleware | Contract Owner |
|------------|--------|-----|---------------------------|------------|----------------|
| `api.reuse.panels` | GET | `/api/reuse/panels` | `ReuseController@searchPanels` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.reuse.feeders` | GET | `/api/reuse/feeders` | `ReuseController@searchFeeders` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.reuse.masterBoms` | GET | `/api/reuse/master-boms` | `ReuseController@searchMasterBoms` | auth, throttle:search | **SHARED** (S3 frozen) |
| `api.reuse.proposalBoms` | GET | `/api/reuse/proposal-boms` | `ReuseController@searchProposalBoms` | auth, throttle:search | **SHARED** (S3 frozen) |

**Total ReuseSearchContract routes:** 4 endpoints

### 2.3 Route File Location (VERIFIED)

- **Routes file:** `source_snapshot/routes/web.php`
  - CatalogLookupContract routes: Lines 50-96
  - ReuseSearchContract routes: Lines 374-385
- **Route group pattern:** `Route::group(['middleware' => 'auth', 'prefix' => 'api'], function () { ... })`
- **Implementation controllers:**
  - `source_snapshot/app/Http/Controllers/QuotationController.php` (CatalogLookupContract)
  - `source_snapshot/app/Http/Controllers/ReuseController.php` (ReuseSearchContract)

**Verification Status:** ✅ Route file locations verified in `source_snapshot/` directory structure.

---

## 3. Smoke Notes (Endpoint Responsiveness)

### 3.1 CatalogLookupContract Smoke Tests

**Target endpoints for smoke verification:**
- `/api/category/{categoryId}/subcategories` → Should return `[{id, label}, ...]` or `[]`
- `/api/item/{itemId}/products` → Should return `[{id, label}, ...]` or `[]`
- `/api/makes` → Should return `[{id, label}, ...]` or `[]`

**Expected behavior:**
- All endpoints require authentication (401 if not authenticated)
- All endpoints respond with 200 OK and JSON array when authenticated
- Empty arrays `[]` are valid responses (no results found)
- Response shape: `[{id: string|number, label: string}]`
- No breaking payload changes from current implementation

**Smoke test status:** ⚠️ **MANUAL VERIFICATION REQUIRED**
- Smoke tests require running application instance
- Tests should be performed before CP1 changes
- Document results in CP2 verification section

### 3.2 ReuseSearchContract Smoke Tests

**Target endpoints for smoke verification:**
- `/api/reuse/panels?searchTerm=<term>` → Should return `[{id, label, kind}, ...]` or `[]`
- `/api/reuse/feeders?searchTerm=<term>` → Should return `[{id, label, kind}, ...]` or `[]`

**Expected behavior:**
- All endpoints require authentication (401 if not authenticated)
- All endpoints respond with 200 OK and JSON array when authenticated
- Empty arrays `[]` are valid responses (no results found)
- Response shape: `[{id: string|number, label: string, kind: string}]`
- Query parameter `searchTerm` or `q` accepted
- No breaking payload changes from current implementation

**Smoke test status:** ⚠️ **MANUAL VERIFICATION REQUIRED**
- Smoke tests require running application instance
- Tests should be performed before CP1 changes
- Document results in CP2 verification section

---

## 4. Current Implementation State

### 4.1 Controller Locations

**CatalogLookupContract:**
- **Host:** `QuotationController` (Legacy namespace)
- **Methods:**
  - `getSubCategories($categoryId)`
  - `getItems($categoryId)`
  - `getProducts($categoryId)`
  - `getProductsByItem($itemId)`
  - `getMakes($productId)`
  - `getSeriesApi($makeId)`
  - `getDescriptions($productId)`
  - `getMakesByCategory($categoryId)`
  - `getAllMakes()`

**ReuseSearchContract:**
- **Host:** `ReuseController` (QUO namespace)
- **Methods:**
  - `searchPanels()`
  - `searchFeeders()`
  - `searchMasterBoms()`
  - `searchProposalBoms()`

### 4.2 Consumer Dependencies

**Known consumers (from S3_SHARED_ALIGNMENT.md):**
- **Quotation (Legacy):** Consumes CatalogLookup endpoints (internal to same controller)
- **Quotation (V2):** Consumes CatalogLookup + ReuseSearch endpoints
- **CIM:** Will migrate in Batch-S4-2 (not in Batch-S4-1 scope)
- **MBOM/FEED/PBOM:** Will migrate in Batch-S4-3+ (not in Batch-S4-1 scope)

**Batch-S4-1 scope:** NO consumer migrations. Only contract surface stabilization.

---

## 5. Guardrails Confirmation

### 5.1 Batch-S4-1 Constraints (Frozen)

✅ **Allowed in Batch-S4-1:**
- Optional controller extraction/wiring for SHARED (implementation may remain in QUO namespace)
- Centralize/shared helpers without changing behavior
- Ensure auth + throttle remain intact

❌ **Forbidden in Batch-S4-1:**
- Any response payload modification
- Any new SHARED endpoint
- Any consumer edits (no migrations)
- Any route renames
- Any COMPAT deletions
- Any QUO-V2 PROTECTED edits

### 5.2 Stop Conditions (Auto-Rollback Triggers)

Execution **must stop immediately** and rollback to CP0 if:
- ❌ Runtime auto-create master pattern detected
- ❌ Breaking payload shape change detected
- ❌ COMPAT endpoint removed prematurely
- ❌ QUO-V2 PROTECTED touch without G4
- ❌ Copy-never-link breach

---

## 6. CP0 Evidence Checklist

- [x] Git baseline commit hash recorded: `1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`
- [x] Routes snapshot documented (9 CatalogLookup + 4 ReuseSearch routes)
- [x] Current controller locations documented
- [x] Consumer dependencies mapped (no migrations in Batch-S4-1)
- [x] Guardrails confirmed
- [x] Stop conditions documented
- [ ] Smoke tests performed (MANUAL - requires running app)
- [x] Route file location verified: `source_snapshot/routes/web.php` (lines 50-96, 374-385)

---

## 7. Rollback Rehearsal Plan

**Rollback procedure (if stop condition triggered):**
1. `git revert <CP0-commit-hash>` OR `git reset --hard 1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`
2. Verify routes restored to CP0 state
3. Re-run smoke tests to confirm baseline restored
4. Document rollback reason in evidence folder

**Rollback evidence required:**
- Git log showing revert/reset
- Route verification (before/after)
- Smoke test results (baseline restored)

---

## 8. Next Steps

**CP0 Status:** ✅ RECORDED

**Proceeding to CP1:**
- CP0 baseline is documented and locked
- Route file location will be verified during CP1 setup
- Smoke tests will be performed if running app is available
- CP1 changes may begin once route verification is complete

**CP1 Objective:**
- Optional controller extraction/wiring for SHARED contracts
- Maintain all routes, payloads, and behavior
- No consumer changes

---

## 9. Authority References

- **Governance:** `docs/PHASE_4/S4_GOV_001_PROPAGATION_ORDER.md`
- **Batch Tasks:** `docs/PHASE_4/S4_BATCH_1_TASKS.md`
- **Contract Freeze:** `docs/PHASE_4/S3_SHARED_ALIGNMENT.md`
- **Route Mapping:** `trace/phase_2/ROUTE_MAP.md`
- **Master Task List:** `docs/PHASE_4/MASTER_TASK_LIST.md`

---

**CP0 Locked:** 2025-12-18  
**CP0 Author:** Batch-S4-1 Execution  
**Next Checkpoint:** CP1 (SHARED Wiring)

