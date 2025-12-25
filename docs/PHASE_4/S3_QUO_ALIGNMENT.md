# S3.4 — QUO Alignment Pack (Legacy + V2 Consumption Map)
#
# Task coverage:
# - NSW-P4-S3-QUO-001 (G3) Align QUO legacy consumption + hosting map
# - NSW-P4-S3-QUO-002 (G3) Align QUO-V2 apply alignment map (post-G4 PASS)
#
# Status: ACTIVE (S3)
# Last Updated: 2025-12-18

---

## Scope + Fence

- This document creates **precise alignment blueprints** for QUO module responsibilities:
  - **S3-QUO-001:** Legacy quotation consumption + hosting map alignment
  - **S3-QUO-002:** QUO-V2 apply alignment map (post-G4 PASS)
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
  - `docs/PHASE_4/S3_BOM_ALIGNMENT.md` (frozen apply contracts)
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: map call paths, classify contract-based vs direct-coupled, document hosting responsibilities, define S4 extraction targets
- ❌ Not allowed: moving controllers, renaming routes, changing response shapes, modifying QUO-V2 core behavior (PROTECTED zone)

---

# S3-QUO-001: Legacy Quotation Alignment (Consumption + Hosting Map)

## Scope + Fence

- This section creates a **precise alignment blueprint** for QUO legacy consumption and hosting responsibilities.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md`
  - `docs/PHASE_4/S2_SHARED_ISOLATION.md`
  - `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: map call paths, classify contract-based vs direct-coupled, document hosting responsibilities
- ❌ Not allowed: moving controllers, renaming routes, changing response shapes, extracting SHARED endpoints

---

## 1) QUO as "Shared API host" (current reality; alignment target)

Legacy QUO currently hosts SHARED contracts:

- CatalogLookupContract (`/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*`, `/api/makes`)
- ReuseSearchContract (`/api/reuse/*`)

**S3 Alignment Decision (frozen):**

- Treat these as **SHARED-owned contracts** even if implementation remains in QUO through S3.
- Controller extraction (e.g., `CatalogLookupController`) is S4 propagation only.
- **Implementation host may remain QUO** through S3; moving to SHARED-owned controllers is S4 propagation work only.

**S3 Freeze Statement:**
- **Contract owner = SHARED; implementation host = QUO until S4; therefore QUO must not add new SHARED endpoints or change payload shapes in S3.**

---

## 2) QUO Legacy Consumption Map (S3-QUO-001)

Legacy QUO consumes:

- CIM catalog resolution (currently direct model access; target is contract-first consumption)
- MBOM template hydration and apply flows (legacy paths)
- PBOM selection/hydration (legacy HTML hydration + V2 search endpoint)

S3 output requirement:

- For each QUO legacy call path, record whether it is:
  - **contract-based** (preferred)
  - **direct-coupled** (current reality; must not expand)

### 2.1 Legacy QUO call-path classification (contract-based vs direct-coupled)

| Legacy QUO capability | Route / Endpoint | Controller / Method | Classification | Notes |
|---|---|---|---|---|
| Catalog dropdowns (Category/Subcategory/Item/Product/Make/Series/Descriptions) | `/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*`, `/api/makes` | `QuotationController@getSubCategories/getItems/getProducts/getProductsByItem/getMakes/getSeriesApi/getDescriptions/getMakesByCategory/getAllMakes` | **contract-based** | Treated as **SHARED contracts** in S3. Implementation remains in QUO until S4. |
| Reuse search (panels/feeders/masterBoms/proposalBoms) | `/api/reuse/*` | `ReuseController@searchPanels/searchFeeders/searchMasterBoms/searchProposalBoms` | **contract-based** | Treated as **SHARED contracts** in S3. |
| PBOM selection search (V2 uses Select2) | `/api/proposal-bom/search` | `QuotationController@searchProposalBom` | **COMPAT (legacy QUO-hosted search)** | Classification: COMPAT (legacy QUO-hosted search). S4 target: Move under PBOM (or SHARED) only after propagation readiness; no change in S3. |
| Legacy MBOM hydration (HTML builder) | `quotation.getMasterBomVal` | `QuotationController@getMasterBomVal` | **direct-coupled** | Legacy HTML hydration used by legacy flows and can be used by V2 fallback paths (record-only). |
| Legacy PBOM hydration (HTML builder) | `quotation.getProposalBomVal` | `QuotationController@getProposalBomVal` | **direct-coupled** | Same as above; keep stable in S3. |
| Legacy “single value” helper | `quotation.getSingleVal` | `QuotationController@getSingleVal` | **direct-coupled** | Used for UI hydration; record-only. |
| Module-local compat lookups used by QUO screens (if any) | `product.get*`, `masterbom.get*` | `ProductController*`, `MasterBomController*` | **direct-coupled** | If QUO screens call these, list them here once confirmed. Do not change in S3. |

**S3 rule:** No call-path may switch classification in S3 (no propagation). Only record and fence.

---

---

## 3) What is Frozen (S3-QUO-001)

### 3.1 SHARED Contract Hosting Freeze

- **SHARED CatalogLookupContract endpoints remain hosted in QUO** (implementation reality)
- **SHARED ReuseSearchContract endpoints remain hosted in QUO** (via ReuseController)
- **Route names and URIs are frozen** for S3
- **Contract ownership is SHARED** (even though implementation is in QUO)
- **Controller extraction is S4 propagation only**

### 3.2 Legacy Consumption Patterns Freeze

- **Direct-coupled call paths remain stable** (no expansion of direct model access)
- **Contract-based call paths remain stable** (SHARED endpoints continue to work)
- **Legacy helper endpoints remain stable** (HTML hydration endpoints unchanged)

---

## 4) What is Explicitly NOT Changed (S3-QUO-001)

- **No controller moves** (no extraction of SHARED endpoints from QUO controllers)
- **No route renames** (no changes to route names or URIs)
- **No response shape changes** (contracts remain stable)
- **No expansion of direct coupling** (must not add new direct model access patterns)
- **No changes to legacy helper endpoints** (HTML hydration endpoints remain as-is)

---

## 5) Consumer Map (S3-QUO-001)

### 5.1 QUO as SHARED Contract Host

| Contract | Endpoints | Current Host | Contract Owner | S4 Extraction Target |
|---|---|---|---|
| CatalogLookupContract | `/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*`, `/api/makes` | `QuotationController` | **SHARED** | Extract to `CatalogLookupController` (S4) |
| ReuseSearchContract | `/api/reuse/*` | `ReuseController` | **SHARED** | Extract to `ReuseController` (move to SHARED namespace, S4) |

### 5.2 QUO Legacy Consumption Patterns

| Consumption Pattern | Route / Endpoint | Controller / Method | Classification | Notes |
|---|---|---|---|---|
| Catalog dropdowns (SHARED contract) | `/api/category/*`, `/api/item/*`, `/api/product/*`, `/api/make/*`, `/api/makes` | `QuotationController@getSubCategories/getItems/getProducts/getProductsByItem/getMakes/getSeriesApi/getDescriptions/getMakesByCategory/getAllMakes` | **contract-based** | QUO hosts these; also consumes internally (via direct model access currently) |
| Reuse search (SHARED contract) | `/api/reuse/*` | `ReuseController@searchPanels/searchFeeders/searchMasterBoms/searchProposalBoms` | **contract-based** | QUO hosts these; treated as SHARED contracts in S3 |
| PBOM selection search (V2 uses Select2) | `/api/proposal-bom/search` | `QuotationController@searchProposalBom` | **COMPAT (legacy QUO-hosted search)** | Classification: COMPAT (legacy QUO-hosted search). S4 target: Move under PBOM (or SHARED) only after propagation readiness; no change in S3. |
| Legacy MBOM hydration (HTML builder) | `quotation.getMasterBomVal` | `QuotationController@getMasterBomVal` | **direct-coupled** | Legacy HTML hydration used by legacy flows and can be used by V2 fallback paths (record-only) |
| Legacy PBOM hydration (HTML builder) | `quotation.getProposalBomVal` | `QuotationController@getProposalBomVal` | **direct-coupled** | Same as above; keep stable in S3 |
| Legacy "single value" helper | `quotation.getSingleVal` | `QuotationController@getSingleVal` | **direct-coupled** | Used for UI hydration; record-only |
| CIM catalog direct model access | N/A (internal) | `QuotationController` (various methods) | **direct-coupled** | QUO directly queries CIM tables/models for catalog resolution. Target state: contract-first consumption (S4+) |

**S3 Rule:** No call-path may switch classification in S3 (no propagation). Only record and fence.

---

## 6) Compatibility Gaps & Resolution Strategy (S3-QUO-001)

### 6.1 Hosting vs Ownership Gap

**Issue:** QUO currently hosts SHARED contracts but ownership is SHARED. This creates a hosting/ownership mismatch.

**S3 Decision (frozen):**
- **Contract ownership is SHARED** (frozen in S3.1)
- **Implementation host remains QUO** through S3
- **Controller extraction is S4 propagation only**
- This gap is acceptable in S3; resolution happens in S4

### 6.2 Direct Model Access vs Contract-First Gap

**Issue:** QUO internally uses direct CIM model access for catalog resolution, while external consumers use SHARED contracts.

**S3 Decision (frozen):**
- **Direct model access patterns remain stable** (no expansion)
- **Target state is contract-first consumption** (S4+ migration)
- **No changes to internal QUO consumption patterns in S3**

---

## 7) S4 Propagation Hooks (S3-QUO-001)

### 7.1 SHARED Contract Extraction Targets

**Target 1: CatalogLookupContract extraction**
- **Current:** Implemented in `QuotationController`
- **Target:** Extract to `CatalogLookupController` (SHARED namespace)
- **S4 Task:** `NSW-P4-S4-SHARED-001` — Extract CatalogLookupContract to SHARED controller

**Target 2: ReuseSearchContract extraction**
- **Current:** Implemented in `ReuseController` (QUO namespace)
- **Target:** Move `ReuseController` to SHARED namespace (or extract to new SHARED controller)
- **S4 Task:** `NSW-P4-S4-SHARED-002` — Extract ReuseSearchContract to SHARED controller

### 7.2 Internal Consumption Migration Targets

**Target 1: QUO internal catalog consumption → contract-first**
- **Current:** Direct CIM model access
- **Target:** QUO internal code consumes SHARED CatalogLookupContract endpoints
- **S4 Task:** `NSW-P4-S4-QUO-001` — Migrate QUO internal consumption to contract-first

---

## 8) Exit Criteria (S3-QUO-001)

S3-QUO-001 is **COMPLETE** when:

- [x] **SHARED contract hosting responsibilities documented:**
  - [x] CatalogLookupContract hosting recorded
  - [x] ReuseSearchContract hosting recorded
  - [x] Contract ownership vs implementation host clarified
- [x] **Legacy consumption patterns classified:**
  - [x] Contract-based call paths identified
  - [x] Direct-coupled call paths identified
  - [x] Classification rules frozen
- [x] **S4 propagation hooks declared:**
  - [x] SHARED contract extraction targets identified
  - [x] Internal consumption migration targets identified
  - [x] S4 tasks linked
- [x] **Explicit "not changed" section present:**
  - [x] No controller moves proposed
  - [x] No route renames proposed
  - [x] No expansion of direct coupling proposed

**Status:** ✅ Complete

---

# S3-QUO-002: QUO-V2 Apply Alignment Map (Post-G4 PASS)

## Scope + Fence

- This section creates a **precise alignment map** for QUO-V2 apply surfaces and responsibilities.
- **No propagation** (no route renames, no controller moves, no behavior changes).
- This is **planning + alignment only** (record-only).
- **QUO-V2 is now unfenced** (post-G4 PASS); S3 must produce responsibility maps.
- Inputs are based on Phase‑2 trace + S2 isolation packs:
  - `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md`
  - `docs/PHASE_4/S3_BOM_ALIGNMENT.md` (frozen apply contracts)
  - `trace/phase_2/ROUTE_MAP.md`

**S3 Guardrails:**
- ✅ Allowed: map apply surfaces, document controller responsibilities, record downstream services
- ❌ Not allowed: modifying QUO-V2 core behavior (PROTECTED zone), changing apply logic, changing pricing/discount/quantity math

---

## 1) QUO-V2 Apply Surfaces (S3-QUO-002)

### 1.1 Frozen Apply Surface List

| Route Name | Method | URI | Owner (behavior) | Notes |
|---|---:|---|---|---|
| `quotation.v2.applyMasterBom` | POST | `/quotation/v2/apply-master-bom` | QUO | MBOM template apply surface (see S3-BOM-001 Section 10.1) |
| `quotation.v2.applyFeederTemplate` | POST | `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | QUO | FEED apply surface (see S3-BOM-002 Section 1.1) |
| `quotation.v2.applyProposalBom` | POST | `/quotation/v2/apply-proposal-bom` | QUO | PBOM apply surface (see S3-BOM-003 Section 1.1) |
| `quotation.v2.item.updateQty` | PUT | `/quotation/{quotation}/item/{item}/qty` | QUO | Update item quantity (V2 update surface) |

---

## 2) V2 Apply & Update Surfaces — Responsibility Map (S3-QUO-002)

This is a **record-only** responsibility map for S3 (no execution changes authorized).

| Surface (route name) | URI | Controller method | Primary responsibility (record-only) | Downstream services / models touched (record-only) |
|---|---|---|---|---|
| `quotation.v2.applyMasterBom` | `/quotation/v2/apply-master-bom` | `QuotationV2Controller@applyMasterBom` | Apply MBOM template items into a target quotation BOM node | `MasterBom`, `MasterBomItem`, `QuotationSaleBom`, `QuotationSaleBomItem`, costing/qty rollups (via existing QUO services) |
| `quotation.v2.applyFeederTemplate` | `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | `QuotationV2Controller@applyFeederTemplate` | Create feeder instance + copy FEED template items into quotation tree | `MasterBom (TemplateType=FEEDER)`, `MasterBomItem`, `QuotationSaleBom`, `QuotationSaleBomItem`, qty/cost rollups (existing logic) |
| `quotation.v2.applyProposalBom` | `/quotation/v2/apply-proposal-bom` | `QuotationV2Controller@applyProposalBom` | Copy items from a source quotation BOM into a target quotation BOM node | `QuotationSaleBom` (source+target), `QuotationSaleBomItem`, qty/cost rollups (existing logic) |
| `quotation.v2.item.updateQty` | `/quotation/{quotation}/item/{item}/qty` | `QuotationV2Controller@updateItemQty` | Update a single item quantity and trigger existing rollups | `QuotationSaleBomItem`, rollup routines, `QuotationQuantityService` (as currently wired) |

**Guardrail:** This table is descriptive only. It does not authorize code changes.

---

## 3) What is Frozen (S3-QUO-002)

- **QUO-V2 apply surfaces are frozen** (route names, URIs, request/response contracts)
- **Controller responsibilities remain stable** (no changes to `QuotationV2Controller` methods)
- **Downstream services remain stable** (no changes to costing/quantity/rollup logic)
- **Apply behavior remains stable** (no changes to pricing, discount, quantity math)

---

## 4) What is Explicitly NOT Changed (S3-QUO-002)

- **No changes to QUO-V2 core behavior** (PROTECTED zone remains fenced)
- **No changes to apply logic** (pricing, discount, rollup remain as-is)
- **No changes to quantity math** (multiplier semantics remain stable)
- **No route renames** (no changes to route names or URIs)
- **No controller moves** (no changes to `QuotationV2Controller` location or structure)

---

## 5) Consumer Map (S3-QUO-002)

| Apply Surface | Primary Consumer(s) | Evidence (caller) | Notes |
|---|---|---|---|
| `quotation.v2.applyMasterBom` | QUO V2 Panel UI — "Apply Master BOM" | `source_snapshot/resources/views/quotation/v2/panel.blade.php` | Posts to `/quotation/v2/apply-master-bom` |
| `quotation.v2.applyMasterBom` | QUO V2 Reuse modal — "Master BOM reuse → apply" | `source_snapshot/resources/views/quotation/v2/_reuse_filter_modal.blade.php` | Posts to `/quotation/v2/apply-master-bom` |
| `quotation.v2.applyFeederTemplate` | QUO V2 Feeder Library modal — "Apply feeder template" | `source_snapshot/resources/views/quotation/v2/_feeder_library_modal.blade.php` | Posts to `/quotation/{quotation}/panel/{panel}/feeder/apply-template` |
| `quotation.v2.applyProposalBom` | QUO V2 Panel UI — "Apply Proposal BOM" | `source_snapshot/resources/views/quotation/v2/panel.blade.php` | Uses `route('quotation.v2.applyProposalBom')` |
| `quotation.v2.applyProposalBom` | QUO V2 Reuse modal — "Proposal BOM reuse → apply" | `source_snapshot/resources/views/quotation/v2/_reuse_filter_modal.blade.php` | Posts to `/quotation/v2/apply-proposal-bom` |
| `quotation.v2.item.updateQty` | QUO V2 Panel UI — "Update item quantity" | `source_snapshot/resources/views/quotation/v2/panel.blade.php` | PUT request to update item quantity |

---

## 6) S4 Propagation Hooks (S3-QUO-002)

### 6.1 Apply Contract Propagation Targets

**Target 1: Apply contract verification (if needed)**
- **Current:** Apply contracts frozen in S3-BOM alignment
- **Target:** Verify apply contracts match implementation (if discrepancies found)
- **S4 Task:** `NSW-P4-S4-QUO-002` — Verify QUO-V2 apply contracts match implementation

**Target 2: Wrapper adoption (if applicable)**
- **Current:** Direct HTTP calls to apply endpoints
- **Target:** Adopt wrapper interfaces (when wrapper contracts are defined)
- **S4 Task:** `NSW-P4-S4-QUO-003` — Adopt wrapper interfaces for V2 apply flows

---

## 7) Exit Criteria (S3-QUO-002)

S3-QUO-002 is **COMPLETE** when:

- [x] **Apply surfaces mapped:**
  - [x] All QUO-V2 apply surfaces identified
  - [x] Controller responsibilities documented
  - [x] Downstream services recorded
- [x] **Consumer map documented:**
  - [x] All consumers identified
  - [x] Evidence locations recorded
- [x] **S4 propagation hooks declared:**
  - [x] Propagation targets identified (if any)
  - [x] S4 tasks linked
- [x] **Explicit "not changed" section present:**
  - [x] No QUO-V2 core behavior changes proposed
  - [x] No apply logic changes proposed

**Status:** ✅ Complete

---

# Cross-Cutting QUO Alignment Summary

## 1) No-propagation gate (S3 hard rule)

| Surface (route name) | URI | Controller method | Primary responsibility (record-only) | Downstream services / models touched (record-only) |
|---|---|---|---|---|
| `quotation.v2.applyMasterBom` | `/quotation/v2/apply-master-bom` | `QuotationV2Controller@applyMasterBom` | Apply MBOM template items into a target quotation BOM node | `MasterBom`, `MasterBomItem`, `QuotationSaleBom`, `QuotationSaleBomItem`, costing/qty rollups (via existing QUO services) |
| `quotation.v2.applyFeederTemplate` | `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | `QuotationV2Controller@applyFeederTemplate` | Create feeder instance + copy FEED template items into quotation tree | `MasterBom (TemplateType=FEEDER)`, `MasterBomItem`, `QuotationSaleBom`, `QuotationSaleBomItem`, qty/cost rollups (existing logic) |
| `quotation.v2.applyProposalBom` | `/quotation/v2/apply-proposal-bom` | `QuotationV2Controller@applyProposalBom` | Copy items from a source quotation BOM into a target quotation BOM node | `QuotationSaleBom` (source+target), `QuotationSaleBomItem`, qty/cost rollups (existing logic) |
| `quotation.v2.item.updateQty` | `/quotation/{quotation}/item/{item}/qty` | `QuotationV2Controller@updateItemQty` | Update a single item quantity and trigger existing rollups | `QuotationSaleBomItem`, rollup routines, `QuotationQuantityService` (as currently wired) |

**Guardrail:** This table is descriptive only. It does not authorize code changes.

---

The following are **forbidden in S3** (this document does not authorize execution):

- **No controller moves or splits** (no extraction of SHARED endpoints from QUO controllers)
- **No route renames** (no changes to route names or URIs)
- **No payload/semantics changes** (request/response meaning must remain stable)
- **No optimization or refactor "for cleanliness"**
- **No changes to pricing/discount/quantity math**
- **No changes to QUO-V2 core behavior** (PROTECTED zone remains fenced)

All execution movement belongs to S4.

---

## 2) Alignment Decisions (frozen until S4)

- **QUO hosts SHARED contracts** but ownership is SHARED (frozen in S3.1)
- **Contract-based consumption is preferred** over direct-coupled patterns
- **Direct-coupled patterns remain stable** (no expansion, no changes in S3)
- **QUO-V2 apply surfaces are frozen** (contracts documented in S3-BOM alignment)

---

## 3) Evidence Requirements

### 3.1 S3-QUO-001 Evidence

- [x] SHARED contract hosting responsibilities documented (Section 5.1)
- [x] Legacy consumption patterns classified (Section 5.2)
- [x] Compatibility gaps identified (Section 6)
- [x] S4 propagation hooks declared (Section 7)
- [x] Explicit "not changed" section present (Section 4)

### 3.2 S3-QUO-002 Evidence

- [x] Apply surfaces mapped (Section 1.1, 2)
- [x] Consumer map documented (Section 5)
- [x] S4 propagation hooks declared (Section 6)
- [x] Explicit "not changed" section present (Section 4)

---

## 4) Task Status

**NSW-P4-S3-QUO-001 (Align QUO legacy consumption + hosting map):** ✅ Complete  
**NSW-P4-S3-QUO-002 (Align QUO-V2 apply alignment map):** ✅ Complete

**Next Tasks:** S3-COPY-HIST-GAP-004 (copy history), then continue with remaining S3 tasks

---

## 5) Authority References

- Route Map: `trace/phase_2/ROUTE_MAP.md`
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- S2 QUO Legacy Isolation: `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md`
- S2 SHARED Isolation: `docs/PHASE_4/S2_SHARED_ISOLATION.md`
- S3 SHARED Alignment: `docs/PHASE_4/S3_SHARED_ALIGNMENT.md` (frozen contracts)
- S3 BOM Alignment: `docs/PHASE_4/S3_BOM_ALIGNMENT.md` (frozen apply contracts)
- S3 Execution Checklist: `docs/PHASE_4/S3_EXECUTION_CHECKLIST.md`
- Master Task List: `docs/PHASE_4/MASTER_TASK_LIST.md`

---

## 6) Out of Scope (S3)

- Splitting controllers in code
- Moving SHARED endpoints out of QUO code
- Any QUO legacy UI refactor
- Modifying QUO-V2 core behavior (PROTECTED zone remains fenced)


