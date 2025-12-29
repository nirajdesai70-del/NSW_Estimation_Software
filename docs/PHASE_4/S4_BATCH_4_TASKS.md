# S4 — Batch-4 Task Set (Execution: QUO hydration contract locks)
#
# Status: ACTIVE (in progress)
# Last Updated: 2025-12-18

---

## Batch intent (authoritative)

Batch-4 focuses on QUO legacy “HTML hydration helpers” identified as **direct-coupled** in S3.4.

**Batch-4 constraints (non-negotiable):**
- ✅ tests-only (contract capture + route wiring guards)
- ✅ DB-free (no migrations, no factories, no SQL fixtures)
- ✅ CI-stable (no `APP_URL` dependency; prefer `route(..., [], false)`)
- ✅ rollback remains a single revert (remove/undo tests only)
- ❌ no controller code changes
- ❌ no query logic changes
- ❌ no view/HTML changes

---

## Task list

### S4-B4-004 — Contract-lock `GET /quotation/getMasterBomVal` (DONE)

- **Task ID:** NSW-P4-S4-QUO-MBOM-HYDRATION-CONTRACT-001
- **Risk:** HIGH (direct-coupled) | **Gate:** PROTECTED / G4
- **Objective:** Freeze the legacy HTML hydration contract for `quotation.getMasterBomVal` via DB-free feature tests only.
- **Locked contract facts:**
  - Unauth → `302` → `/login`
  - Route wiring is CI-stable (no `APP_URL` dependence)
  - Auth → `200` and `view('quotation.item')`
  - View vars exactly:
    - `MasterBomId`, `count`, `Item`, `co`, `it`, `tt`, `Category`, `type`, `cname`, `cqty`
  - `$Item[0]` minimum default contract (RateSource/flags/arrays/selected fields) locked
- **Rollback:** single revert (tests-only)
- **Evidence:** PHPUnit pass (feature test), route wiring guard assertion
- **Bundles:** C (CI / PHPUnit feature tests)

---

### S4-B4-005 — Contract-lock `GET /quotation/getProposalBomVal` (DONE)

- **Task ID:** NSW-P4-S4-QUO-PBOM-HYDRATION-CONTRACT-001
- **Risk:** HIGH (direct-coupled + pricing auto-fill branch) | **Gate:** PROTECTED / G4
- **Route:** `quotation.getProposalBomVal`
- **URI:** `GET /quotation/getProposalBomVal`
- **Handler:** `QuotationController@getProposalBomVal`
- **Objective:** Freeze the legacy PBOM hydration contract (HTML via `quotation.item`) via DB-free feature tests only, including the **PRICELIST auto-fill** branch.

**In scope (tests-only):**
- Route wiring guard (CI-stable):
  - `$this->assertSame('/quotation/getProposalBomVal', route('quotation.getProposalBomVal', [], false));`
- Unauth behavior:
  - `302` redirect to `/login`
- Auth behavior:
  - `200` and `view('quotation.item')`
  - View vars exactly:
    - `MasterBomId`, `count`, `Item`, `co`, `it`, `tt`, `Category`, `type`, `cname`, `cqty`
- `$Item[0]` minimum contract:
  - required keys present
  - dropdown arrays are arrays (`SubCategory`, `Item`, `Generic`, `Make`, `Series`, `Description`)
  - selection fields preserved (`*Selected`)
  - pricing flags stable:
    - `RateSource`
    - `IsClientSupplied`
    - `IsPriceConfirmed`

**Branch matrix (tests):**
- **B4-005-A (PRICELIST auto-fill hit)**:
  - Source: `RateSource=PRICELIST`, `Rate=0`, `Description>0`
  - Price lookup returns a Rate > 0
  - Expect: `Rate` auto-filled, `IsPriceConfirmed=1`, `NetRate/Amount` recalculated
- **B4-005-B (auto-fill bypass)**:
  - Source: `RateSource!=PRICELIST` *or* `Rate>0` *or* `Description<=0`
  - Expect: pricing values preserved, `IsPriceConfirmed` computed from `Rate>0`

**DB-free strategy (non-brittle):**
- Mock `DB::select()` without asserting the raw SQL string.
- Alias-mock Eloquent models used in the handler:
  - `QuotationSaleBom`, `Category`, `SubCategory`, `Item`, `Product`, `MakeCategory`, `SeriesMake`, `Price`
- Avoid asserting full dropdown contents; assert only:
  - view variable existence
  - required keys + types
  - small number of stable pricing invariants per branch matrix

**Forbidden (this task):**
- Any production code edits
- Any route/controller movement
- Any query or payload changes

**Rollback:** single revert (remove the test file)

**Evidence (minimum):**
- `php artisan test --filter GetProposalBomValContractTest` ✅ PASS
- Route wiring assertion uses `route(..., [], false)` (APP_URL-independent)

**Bundles:** C (CI / PHPUnit feature tests)

---

## Batch-4.1 (Reuse search contract locks) — PROTECTED / G4 (tests-only)

These are “search surfaces” used for Reuse flows (Select2-style), and are gated as **PROTECTED / G4**.

**Locked contract facts (applies to all endpoints):**
- Route wiring guard (CI-stable): `route('<name>', [], false) === '<path>'`
- Unauth: `302 → /login`
- Auth: `200`
- JSON invariants:
  - top-level has key `results`
  - `results` is an array
  - if non-empty: first element has keys `id` and `text`

**Branch matrix (minimal, non-brittle):**
- A1: no filter param
- A2: filter param = `valve` (non-empty)
- A3: filter param = `0` (edge)

**Rollback:** single revert (tests-only)

**Evidence (minimum):**
- `php artisan test --filter ReuseSearchContractTest` ✅ PASS

### S4-B4-006 — Contract-lock `GET /api/reuse/panels` (DONE)

- **Task ID:** NSW-P4-S4-REUSE-SEARCH-PANELS-CONTRACT-001
- **Risk:** HIGH (direct-coupled UI reuse) | **Gate:** PROTECTED / G4
- **Route name:** `api.reuse.panels`
- **URI:** `GET /api/reuse/panels`
- **Handler:** `ReuseController@searchPanels`
- **Evidence:** `ReuseSearchContractTest` (DB-free)
- **Rollback:** single revert (tests-only)
- **Bundles:** C

### S4-B4-007 — Contract-lock `GET /api/reuse/feeders` (DONE)

- **Task ID:** NSW-P4-S4-REUSE-SEARCH-FEEDERS-CONTRACT-001
- **Risk:** HIGH (direct-coupled UI reuse) | **Gate:** PROTECTED / G4
- **Route name:** `api.reuse.feeders`
- **URI:** `GET /api/reuse/feeders`
- **Handler:** `ReuseController@searchFeeders`
- **Evidence:** `ReuseSearchContractTest` (DB-free)
- **Rollback:** single revert (tests-only)
- **Bundles:** C

### S4-B4-008 — Contract-lock `GET /api/reuse/master-boms` (DONE)

- **Task ID:** NSW-P4-S4-REUSE-SEARCH-MASTERBOMS-CONTRACT-001
- **Risk:** HIGH (direct-coupled UI reuse) | **Gate:** PROTECTED / G4
- **Route name:** `api.reuse.masterBoms`
- **URI:** `GET /api/reuse/master-boms`
- **Handler:** `ReuseController@searchMasterBoms`
- **Evidence:** `ReuseSearchContractTest` (DB-free)
- **Rollback:** single revert (tests-only)
- **Bundles:** C

### S4-B4-009 — Contract-lock `GET /api/reuse/proposal-boms` (DONE)

- **Task ID:** NSW-P4-S4-REUSE-SEARCH-PROPOSALBOMS-CONTRACT-001
- **Risk:** HIGH (direct-coupled UI reuse) | **Gate:** PROTECTED / G4
- **Route name:** `api.reuse.proposalBoms`
- **URI:** `GET /api/reuse/proposal-boms`
- **Handler:** `ReuseController@searchProposalBoms`
- **Evidence:** `ReuseSearchContractTest` (DB-free)
- **Rollback:** single revert (tests-only)
- **Bundles:** C

---

## Batch-4.2 (Critical-write & Autosave Route Contract Locks) — PROTECTED / G4 (tests-only)

Batch-4.2 freezes the **route wiring** contract for write surfaces that are coupled to UI autosave / apply flows.

**Locked contract (minimal, applies to all endpoints below):**
- Route wiring guard (CI-stable): `route('<name>', <params>, false) === '<path>'`
- No assertions on write behavior (payload/DB side effects explicitly out of scope)

**DB-free harness note (tests-only):**
- DB access is out-of-scope (tests do not dispatch controller logic).

**Governance note (strict tests-only):**
- **Unauth redirect contract is not enforced** (`302 → /login` is intentionally not asserted); enforcing that requires a separately approved production security patch.

**Evidence (minimum):**
- `php artisan test --filter CriticalWriteAutosaveRouteContractTest` ✅ PASS

### S4-B4-010 — Contract-lock `POST /quotation/v2/apply-master-bom` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-CRITICAL-WRITE-ROUTE-CONTRACT-001
- **Risk:** HIGH (critical write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.applyMasterBom`
- **URI:** `POST /quotation/v2/apply-master-bom`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-011 — Contract-lock `POST /quotation/v2/apply-proposal-bom` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-CRITICAL-WRITE-ROUTE-CONTRACT-002
- **Risk:** HIGH (critical write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.applyProposalBom`
- **URI:** `POST /quotation/v2/apply-proposal-bom`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-012 — Contract-lock `POST /reuse/panel/apply` (DONE)

- **Task ID:** NSW-P4-S4-REUSE-APPLY-PANEL-ROUTE-CONTRACT-001
- **Risk:** HIGH (critical write surface) | **Gate:** PROTECTED / G4
- **Route name:** `reuse.panel.apply`
- **URI:** `POST /reuse/panel/apply`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-013 — Contract-lock `POST /reuse/feeder/apply` (DONE)

- **Task ID:** NSW-P4-S4-REUSE-APPLY-FEEDER-ROUTE-CONTRACT-001
- **Risk:** HIGH (critical write surface) | **Gate:** PROTECTED / G4
- **Route name:** `reuse.feeder.apply`
- **URI:** `POST /reuse/feeder/apply`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-014 — Contract-lock `POST /quotation/{quotation}/panel/{panel}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-PANEL-QTY-ROUTE-CONTRACT-001
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.panel.updateQty`
- **URI:** `POST /quotation/{quotation}/panel/{panel}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-015 — Contract-lock `POST /quotation/{quotation}/feeder/{feeder}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-FEEDER-QTY-ROUTE-CONTRACT-001
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.feeder.updateQty`
- **URI:** `POST /quotation/{quotation}/feeder/{feeder}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-016 — Contract-lock `POST /quotation/{quotation}/bom/{bom}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-BOM-QTY-ROUTE-CONTRACT-001
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.bom.updateQty`
- **URI:** `POST /quotation/{quotation}/bom/{bom}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-017 — Contract-lock `PATCH /quotation/{quotation}/panel/{panel}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-PANEL-QTY-ROUTE-CONTRACT-002
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.updatePanelQty`
- **URI:** `PATCH /quotation/{quotation}/panel/{panel}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-018 — Contract-lock `PATCH /quotation/{quotation}/feeder/{bom}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-FEEDER-QTY-ROUTE-CONTRACT-002
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.updateFeederQty`
- **URI:** `PATCH /quotation/{quotation}/feeder/{bom}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-019 — Contract-lock `PATCH /quotation/{quotation}/bom/{bom}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-BOM-QTY-ROUTE-CONTRACT-002
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.updateBomQty`
- **URI:** `PATCH /quotation/{quotation}/bom/{bom}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-020 — Contract-lock `POST /quotation/{quotation}/item/{item}/rate` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-ITEM-RATE-ROUTE-CONTRACT-001
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.item.updateRate`
- **URI:** `POST /quotation/{quotation}/item/{item}/rate`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-021 — Contract-lock `POST /quotation/{quotation}/item/{item}/discount` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-ITEM-DISCOUNT-ROUTE-CONTRACT-001
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.item.updateDiscount`
- **URI:** `POST /quotation/{quotation}/item/{item}/discount`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-022 — Contract-lock `POST /quotation/{quotation}/item/{item}/qty` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-AUTOSAVE-ITEM-QTY-ROUTE-CONTRACT-001
- **Risk:** HIGH (autosave write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.item.updateQty`
- **URI:** `POST /quotation/{quotation}/item/{item}/qty`
- **Evidence:** `CriticalWriteAutosaveRouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C



---

## Batch-4.3 (UI-coupled QUO V2 Create/Update/Delete Route Contract Locks) — PROTECTED / G4

Batch-4.3 freezes the **route wiring** contract for UI-coupled V2 write endpoints (create + update/delete flows).

**Governance note (strict tests-only):**
- **Phase-4 tests-only:** route wiring locked.
- **Unauth redirect contract is not enforced** (`302 → /login` is intentionally not asserted); this requires a separately approved production security patch (e.g., adding `auth` middleware to these routes).

**Locked contract (minimal, applies to all endpoints below):**
- Route wiring guard (CI-stable): `route('<name>', <params>, false) === '<path>'`
- No assertions on write behavior (payload/DB side effects explicitly out of scope)

**DB-free harness note (tests-only):**
- DB access is out-of-scope (tests do not dispatch controller logic).

**Evidence (minimum):**
- `php artisan test --filter Batch43RouteContractTest` ✅ PASS

### S4-B4-023 — Contract-lock `POST /quotation/{quotation}/feeder/{feeder}/delete` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-DELETE-FEEDER-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled delete write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.deleteFeeder`
- **URI:** `POST /quotation/{quotation}/feeder/{feeder}/delete`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-024 — Contract-lock `POST /quotation/{quotation}/bom/{bom}/delete` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-DELETE-BOM-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled delete write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.deleteBom`
- **URI:** `POST /quotation/{quotation}/bom/{bom}/delete`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-025 — Contract-lock `POST /quotation/{quotation}/panel/{panel}/delete` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-DELETE-PANEL-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled delete write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.deletePanel`
- **URI:** `POST /quotation/{quotation}/panel/{panel}/delete`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-026 — Contract-lock `POST /quotation/{quotation}/panel/{panel}/update` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-UPDATE-PANEL-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled update write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.updatePanel`
- **URI:** `POST /quotation/{quotation}/panel/{panel}/update`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-027 — Contract-lock `POST /quotation/{quotation}/bom/{bom}/update` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-UPDATE-BOM-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled update write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.updateBom`
- **URI:** `POST /quotation/{quotation}/bom/{bom}/update`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-028 — Contract-lock `POST /quotation/{quotation}/items/batch-update` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-BATCH-UPDATE-ITEMS-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled batch write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.batchUpdateItems`
- **URI:** `POST /quotation/{quotation}/items/batch-update`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-029 — Contract-lock `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-APPLY-FEEDER-TEMPLATE-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled apply write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.applyFeederTemplate`
- **URI:** `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-030 — Contract-lock `POST /quotation/{id}/panel` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-ADD-PANEL-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled create write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.addPanel`
- **URI:** `POST /quotation/{id}/panel`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-031 — Contract-lock `POST /quotation/{id}/panel/{panelId}/feeder` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-ADD-FEEDER-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled create write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.addFeeder`
- **URI:** `POST /quotation/{id}/panel/{panelId}/feeder`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-032 — Contract-lock `POST /quotation/{id}/bom/{parentBomId}/bom` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-ADD-BOM-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled create write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.addBom`
- **URI:** `POST /quotation/{id}/bom/{parentBomId}/bom`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

### S4-B4-033 — Contract-lock `POST /quotation/{id}/bom/{bomId}/item` (DONE)

- **Task ID:** NSW-P4-S4-QUO-V2-ADD-ITEM-ROUTE-CONTRACT-001
- **Risk:** HIGH (UI-coupled create write surface) | **Gate:** PROTECTED / G4
- **Route name:** `quotation.v2.addItem`
- **URI:** `POST /quotation/{id}/bom/{bomId}/item`
- **Evidence:** `Batch43RouteContractTest` (DB-free)
- **Rollback:** single revert (tests + ledger only)
- **Bundles:** C

---

**Evidence set (final):**
- `php artisan test --filter GetProposalBomValContractTest` ✅ PASS
- `php artisan test --filter ReuseSearchContractTest` ✅ PASS
- `php artisan test --filter CriticalWriteAutosaveRouteContractTest` ✅ PASS
- `php artisan test --filter Batch43RouteContractTest` ✅ PASS

**Phase-4 CLOSED (2025-12-18):** Phase‑4 contracts are frozen (tests-only contract capture; CI-stable `route(..., false)` wiring guards; DB-free where explicitly noted) for all items in this ledger, including QUO hydration (`GET /quotation/getProposalBomVal`), Reuse search surfaces (Batch‑4.1), critical-write/autosave surfaces (Batch‑4.2, including unauth `302 → /login` where asserted), and remaining V2 create/update/delete route wiring (Batch‑4.3); explicitly excluded: Batch‑4.3 unauth redirect enforcement (requires separately approved production security patch); any change to a locked route/contract requires reopening Phase‑4. **Phase‑5 guardrail:** Phase‑5 must not change frozen contracts without reopening Phase‑4.

