# Batch-S4-3: CP0 Baseline Checkpoint

**Batch:** S4-3 (BOM Consumer Migration)  
**Checkpoint:** CP0 (Baseline)  
**Date:** 2025-12-24  
**Status:** ✅ **BASELINE LOCKED**  
**Authority:** S4-GOV-001, S3_CIM_ALIGNMENT.md (Section 2.2), BATCH_S4_2_CP3_EVIDENCE_PACK.md

---

## CP0 Purpose

CP0 establishes the baseline state before Batch-S4-3 execution. This checkpoint documents:
- Current git commit hash (rollback point)
- All SHARED catalog routes (13 endpoints - stable from S4-1)
- All MBOM COMPAT endpoints (3 endpoints)
- MBOM consumer call-site inventory (create/edit/copy views)
- FEED/PBOM consumer status (catalog lookup usage verification)
- Scope lock for Batch-S4-3
- Rollback command

**This baseline must remain unchanged until Batch-S4-3 CP3 closure.**

---

## 1. Git Baseline

**Git Commit Hash:** `1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`

**Baseline Date:** 2025-12-24

**Rollback Command:**
```bash
git reset --hard 1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0
```

**Note:** This is the same commit as Batch-S4-1 CP0 and Batch-S4-2 CP0. Batch-S4-2 did not modify MBOM consumers.

---

## 2. Route Snapshot

### 2.1 SHARED Routes (13 endpoints - Stable from S4-1)

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
- ✅ Services verified in Batch-S4-1 CP2 (6/6 smoke tests passed)
- ✅ CIM consumers migrated in Batch-S4-2 (CP3 complete)

### 2.2 MBOM COMPAT Endpoints (3 endpoints)

**Location:** `source_snapshot/routes/web.php` (lines 231-233)

| Route Name | Method | URI | Handler | Current Payload | Target SHARED Endpoint | Status |
|---|---|---|---:|---|---|---|
| `masterbom.getsubcategory` | GET | `/masterbom/getsubcategory/{id}` | `MasterBomController@getsubcategory` | `{ subcategory: [...], producttype: [...] }` | Split: `api.category.subcategories` + `api.category.items` | ✅ Active (COMPAT) |
| `masterbom.getproducttype` | GET | `/masterbom/getproducttype/{id}` | `MasterBomController@getproducttype` | `{ producttype: [...] }` | `api.category.items` with `?subcategory={subCategoryId}` | ✅ Active (COMPAT) |
| `masterbom.getdescription` | GET | `/masterbom/getdescription` | `MasterBomController@getdescription` | `{ description: [{ProductId,Name}] }` (filters: CategoryId/SubCategoryId/ItemId; ProductType=1) | `api.category.products` with `subcategoryId` + `itemId` inputs | ✅ Active (COMPAT) |

**COMPAT Lifecycle Policy:**
- ✅ COMPAT endpoints remain active during Batch-S4-3 migration
- ✅ COMPAT endpoints must NOT be deleted in Batch-S4-3
- ✅ COMPAT endpoints serve as fallback until S5 Bundle-C passes
- ✅ COMPAT endpoints will be deprecated but not removed

### 2.3 FEED / PBOM Apply Surfaces (Frozen from S3)

**Reference:** `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md` (Section 2.3)

**FEED Apply Surface:**
- `quotation.v2.applyFeederTemplate` - V2 apply surface (frozen, no catalog lookup migration in Batch-S4-3)

**PBOM Apply Surface:**
- `quotation.v2.applyProposalBom` - V2 apply surface (frozen, no catalog lookup migration in Batch-S4-3)

**MBOM Apply Surface:**
- `quotation.v2.applyMasterBom` - V2 apply surface (frozen, no catalog lookup migration in Batch-S4-3)

**Note:** FEED/PBOM/MBOM apply behaviors are separate from catalog lookup migration. Apply/reuse/clear and copy-history are separate batches/tasks.

---

## 3. Consumer Call-Site Inventory

**Reference:** `docs/PHASE_4/S3_CIM_ALIGNMENT.md` (Section 2.2)

### 3.1 MBOM View Files (Call Sites)

| Consumer (module/screen) | View File | Current COMPAT Endpoints Used | JS/Blade Location | Migration Target |
|---|---|---|---|---|
| MBOM — Master BOM (create) | `source_snapshot/resources/views/masterbom/create.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | TBD (verify in execution) | `api.category.subcategories`, `api.category.items`, `api.category.products` |
| MBOM — Master BOM (edit) | `source_snapshot/resources/views/masterbom/edit.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | TBD (verify in execution) | `api.category.subcategories`, `api.category.items`, `api.category.products` |
| MBOM — Master BOM (copy) | `source_snapshot/resources/views/masterbom/copy.blade.php` | `masterbom.getsubcategory`, `masterbom.getdescription` | TBD (verify in execution) | `api.category.subcategories`, `api.category.items`, `api.category.products` |

**Migration Order (from S3_CIM_ALIGNMENT.md pattern):**
1. **Phase 1:** Migrate `masterbom.getdescription` (simplest parameter mapping)
2. **Phase 2:** Migrate `masterbom.getproducttype` (requires subcategoryId context, if used)
3. **Phase 3:** Migrate `masterbom.getsubcategory` (most complex, split into multiple endpoints)

### 3.2 JS Call Sites (To Be Verified in CP1)

**Note:** Exact JS call sites will be verified during CP1 execution. The following are expected locations based on S3_CIM_ALIGNMENT.md:

- `masterbom/create.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)
- `masterbom/edit.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)
- `masterbom/copy.blade.php` - JavaScript section (AJAX calls to COMPAT endpoints)

**Verification Required in CP1:**
- [ ] Identify all AJAX call sites in each view file
- [ ] Document parameter mapping for each call
- [ ] Document response transformation requirements
- [ ] Verify context availability (subcategoryId, itemId, etc.)
- [ ] Verify Select2 initialization patterns (if used)

### 3.3 FEED Consumer Lookups (Verification Required)

**Reference:** `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md` (Section 2.3)

**FEED Library Views:**
- `source_snapshot/resources/views/feeder-library/create.blade.php`
- `source_snapshot/resources/views/feeder-library/edit.blade.php`
- `source_snapshot/resources/views/feeder-library/index.blade.php`
- `source_snapshot/resources/views/feeder-library/show.blade.php`

**Verification Required in CP1:**
- [ ] Check if FEED views use catalog lookup endpoints (COMPAT or SHARED)
- [ ] If catalog lookups exist, document call sites
- [ ] If no catalog lookups exist, mark as "No catalog lookup migration needed"

**Note:** FEED apply behavior (`quotation.v2.applyFeederTemplate`) is separate from catalog lookup migration.

### 3.4 PBOM Consumer Lookups (Verification Required)

**Reference:** `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md` (Section 2.3)

**PBOM Views:**
- `source_snapshot/resources/views/proposal-bom/index.blade.php`
- `source_snapshot/resources/views/proposal-bom/show.blade.php`

**Verification Required in CP1:**
- [ ] Check if PBOM views use catalog lookup endpoints (COMPAT or SHARED)
- [ ] If catalog lookups exist, document call sites
- [ ] If no catalog lookups exist, mark as "No catalog lookup migration needed"

**Note:** PBOM apply behavior (`quotation.v2.applyProposalBom`) is separate from catalog lookup migration.

---

## 4. Batch-S4-3 Scope Lock

### 4.1 In Scope (✅ Allowed)

**Consumer Migration:**
- ✅ Update MBOM views/JavaScript to call `/api/*` SHARED endpoints (CatalogLookupContract endpoints)
- ✅ Update MBOM JavaScript to use new endpoint URIs and parameter formats
- ✅ Add client-side response transformation (flatten nested objects to `{id,label}` arrays)
- ✅ Verify MBOM functionality after migration (dropdowns, searches work correctly)
- ✅ Migrate FEED catalog lookups (if FEED screens call catalog endpoints)
- ✅ Migrate PBOM catalog lookups (if PBOM screens call catalog endpoints)

**COMPAT Endpoint Lifecycle:**
- ✅ Keep COMPAT endpoints alive (no deletions)
- ✅ COMPAT endpoints remain available as fallback
- ✅ COMPAT endpoints remain unmodified (no changes to handlers or payloads)

**Testing:**
- ✅ Smoke test MBOM screens (create/edit/copy)
- ✅ Verify dropdown population works correctly
- ✅ Verify search functionality works correctly
- ✅ Verify no breaking changes to MBOM workflows
- ✅ Verify FEED/PBOM catalog lookups (if migrated)

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

**QUO-V2 PROTECTED Zone:**
- ❌ No QUO-V2 touches (PROTECTED zone remains fenced)
- ❌ No apply behavior changes (FEED reuse/clear and copy-history are separate batches/tasks)
- ❌ No MBOM/PBOM/FEED apply surface modifications

**Other Modules:**
- ❌ No QUO consumer migration (deferred to Batch-S4-4)
- ❌ No other module consumer migrations

**Controller Changes:**
- ❌ No controller extraction (endpoints remain in existing controllers)
- ❌ No controller refactoring beyond what's needed for migration

---

## 5. Migration Blueprint Reference

**Primary Reference:** `docs/PHASE_4/S3_CIM_ALIGNMENT.md`

**Key Sections:**
- Section 2.2: MBOM module call sites (for reference)
- Section 3.2: COMPAT endpoint classification
- Section 4: Migration blueprint pattern (adapt for MBOM)
- Section 5: Compatibility gaps & resolution strategy
- Section 6: Migration execution plan

**Parameter Mapping (from S3_CIM_ALIGNMENT.md pattern, adapted for MBOM):**

1. **`masterbom.getdescription` → `api.category.products`:**
   - Current: `CategoryId`, `SubCategoryId`, `ItemId` (query params)
   - Target: `{categoryId}` (path param) + `?subcategoryId={subCategoryId}&itemId={itemId}` (query params)
   - **Gap:** Requires subcategoryId and itemId to be available in client context

2. **`masterbom.getproducttype` → `api.category.items`:**
   - Current: `{id}` (path param) → categoryId
   - Target: `{categoryId}` (path param) + `?subcategory={subCategoryId}` (query param)
   - **Gap:** Requires subcategoryId to be available in client context
   - **Note:** Usage in known views may be commented—verify in CP1

3. **`masterbom.getsubcategory` → Multiple endpoints:**
   - Current: `{id}` (path param) → categoryId
   - Target: Split into `api.category.subcategories` + `api.category.items`
   - **Gap:** Response transformation required (split nested payload into separate dropdowns)

**Response Transformation (from S3_CIM_ALIGNMENT.md Section 5.1, adapted for MBOM):**
- Current COMPAT endpoints return nested objects (e.g., `{ subcategory: [...], producttype: [...] }`)
- SHARED endpoints return flat arrays `[{id, label}]`
- Client-side transformation required: extract nested arrays, flatten to `{id,label}`

---

## 6. Stop Conditions

**Stop Conditions (from S4-GOV-001):**
- ❌ Breaking payload shape change detected → **STOP IMMEDIATELY**
- ❌ COMPAT endpoint removed prematurely → **STOP IMMEDIATELY**
- ❌ MBOM functionality broken → **STOP IMMEDIATELY**
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
- **Consumer Status:** CIM consumers migrated in Batch-S4-2 (CP3 complete)

**ReuseSearchService:**
- **Location:** `app/Services/Shared/ReuseSearchService.php`
- **Contract:** `app/Contracts/Shared/ReuseSearchContract.php`
- **Status:** ✅ Wired behind existing routes (Batch-S4-1 CP3 complete)
- **Endpoints:** All 4 reuse endpoints use this service

**Service Wiring:**
- ✅ Services created in Batch-S4-1
- ✅ Services verified in Batch-S4-1 CP2 (6/6 smoke tests passed)
- ✅ Services ready for MBOM consumer adoption in Batch-S4-3

---

## 8. Authority References

**Governance:**
- `docs/PHASE_4/S4_GOV_001_PROPAGATION_ORDER.md` - Propagation order and governance rules

**S3 Blueprints:**
- `docs/PHASE_4/S3_CIM_ALIGNMENT.md` - CIM alignment blueprint (migration plan pattern)
- `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` - SHARED alignment (frozen contracts)

**Batch-S4-1 Evidence:**
- `docs/PHASE_4/evidence/BATCH_S4_1_CP0_BASELINE.md` - Batch-S4-1 baseline
- `docs/PHASE_4/evidence/BATCH_S4_1_CP2_VERIFICATION.md` - Batch-S4-1 verification
- `docs/PHASE_4/evidence/BATCH_S4_1_CP3_EVIDENCE_PACK.md` - Batch-S4-1 closure

**Batch-S4-2 Evidence:**
- `docs/PHASE_4/evidence/BATCH_S4_2_CP0_BASELINE.md` - Batch-S4-2 baseline
- `docs/PHASE_4/evidence/BATCH_S4_2_CP1_JS_EXTRACTS.md` - Batch-S4-2 JS extracts
- `docs/PHASE_4/evidence/BATCH_S4_2_CP2_VERIFICATION.md` - Batch-S4-2 verification
- `docs/PHASE_4/evidence/BATCH_S4_2_CP3_EVIDENCE_PACK.md` - Batch-S4-2 closure

**Handoff:**
- `docs/PHASE_4/evidence/BATCH_S4_2_CP3_EVIDENCE_PACK.md` - Batch-S4-2 to Batch-S4-3 handoff

---

## 9. CP0 Lock Statement

**Baseline Status:** ✅ **LOCKED**

**This CP0 baseline establishes:**
- ✅ Git commit hash for rollback: `1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`
- ✅ 13 SHARED routes documented and verified (stable from S4-1)
- ✅ 3 MBOM COMPAT endpoints documented
- ✅ MBOM call-site inventory referenced (S3_CIM_ALIGNMENT.md Section 2.2)
- ✅ FEED/PBOM consumer status verification plan defined
- ✅ Scope lock defined (in-scope and out-of-scope items)
- ✅ Migration blueprint referenced (S3_CIM_ALIGNMENT.md pattern)
- ✅ Stop conditions defined
- ✅ Service availability confirmed

**This baseline must remain unchanged until Batch-S4-3 CP3 closure.**

---

## 10. ⚠️ Important Context: Live Environment & Future NSW Changes

### Live Environment Execution

**Execution Context:**
- This work is being executed in **live/production environment** (Nish Live)
- Changes are **minimal and safe** - JavaScript endpoint migration only
- No database schema changes or new tables introduced
- COMPAT endpoints remain active as fallback

**Phase-4 Scope (Legacy Stabilization):**
- Phase-4 work is **transport layer standardization** only
- Focus: Converge consumers onto SHARED contract interface
- No semantic meaning changes (legacy truth preserved)
- No data model modifications

### Future NSW Fundamental Work Impact

**Important Note:**
- When **NSW Fundamental Alignment** begins with new table structures, Phase-4 work may need review/revision
- Current Phase-4 changes are **adapter seam** implementations, not data model changes
- SHARED contracts can be remapped to future NSW tables without changing consumers
- Phase-4 reduces blast radius for future changes (single adapter point vs. dozens of consumers)

**Revert Capability:**
- All Phase-4 changes can be reverted to this CP0 baseline if needed
- Rollback command: `git reset --hard 1b4dff0c3496e6116ef78b5d8ec90fac95e5b7f0`
- COMPAT endpoints remain available during any transition period

**Design Philosophy:**
- Phase-4 = Legacy truth (operational/tolerated)
- NSW = Canonical truth (future/enforced)
- SHARED contracts = Transport layer (can swap implementation)
- Phase-4 creates clean adapter seam without locking in legacy schema

**Reference:**
- `docs/PHASE_5/LEGACY_VS_NSW_COEXISTENCE_POLICY.md` - Two Truth Layers policy
- `docs/PHASE_5/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` - NSW firewall policy

---

**CP0 Locked:** 2025-12-24  
**Batch-S4-3 Status:** ⏳ **READY FOR CP1**  
**Next Checkpoint:** CP1 (MBOM Consumer Migration)

