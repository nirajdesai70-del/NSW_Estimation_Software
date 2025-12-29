# NSW-P4-S2-QUO-REVERIFY-001 — G4 Re-Verification Note (QUO‑V2 Surface)

**Date:** 2025-12-18  
**Gate:** G4  
**Rule:** Evidence + decision only (no refactor, no behavior change)

---

## Scope (strict)

Verify **live execution code (not snapshot)** for:

- `QuotationV2Controller@applyFeederTemplate`
- `QuotationV2Controller@updateItemQty`

---

## Live codebase inspected (evidence source)

Local working copy at:

- `/Users/nirajdesai/Projects/nish/`

Files inspected:

- `app/Http/Controllers/QuotationV2Controller.php`
- `routes/web.php`
- `resources/views/quotation/v2/panel.blade.php`
- `resources/views/quotation/v2/_feeder_library_modal.blade.php`
- `resources/views/quotation/v2/_items_table.blade.php`

---

## Findings (what is true in live code)

### 1) Routes exist and are wired to the missing controller methods

In `nish/routes/web.php`:

- Route exists for feeder template apply:
  - `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
  - Handler: `QuotationV2Controller::applyFeederTemplate`
  - Name: `quotation.v2.applyFeederTemplate`
- Route exists for item qty update:
  - `POST /quotation/{quotation}/item/{item}/qty`
  - Handler: `QuotationV2Controller::updateItemQty`
  - Name: `quotation.v2.item.updateQty`

### 2) V2 UI actively references these routes

In `nish/resources/views/quotation/v2/panel.blade.php`:

- `_feeder_library_modal` is included (so the feature surface is present in V2 panel UI).

In `nish/resources/views/quotation/v2/_feeder_library_modal.blade.php`:

- JS calls `POST /quotation/{quotationId}/panel/{panelId}/feeder/apply-template` (apply feeder template).

In `nish/resources/views/quotation/v2/_items_table.blade.php`:

- Item qty modal posts to `route('quotation.v2.item.updateQty', ...)` (update item qty).

### 3) The live controller does NOT implement the required methods

In `nish/app/Http/Controllers/QuotationV2Controller.php`:

- No definition found for `applyFeederTemplate(...)` (string not present in file).
- No definition found for `updateItemQty(...)` (string not present in file).

The controller **does** implement adjacent/related endpoints (confirming the file is the live V2 controller), e.g.:

- `updatePanelQty(...)`
- `updateFeederQty(...)`
- `updateBomQty(...)`
- `updateItemRate(...)`
- `updateItemDiscount(...)`
- `applyFeederReuse(...)`

---

## Decision (required outcome)

**Outcome:** 2 — **Routes are stale / miswired relative to live execution code** (routes reference controller methods that do not exist in the live controller surface).

**Gate result:** ❌ **G4 FAIL**  
**Fence status:** QUO‑V2 remains fenced. **S3 must NOT start.**

---

## Next allowed action (if any)

Create a QUO remediation task to reconcile the live QUO‑V2 surface **without changing behavior yet**, then repeat G4:

- Either **implement** the missing controller methods (`applyFeederTemplate`, `updateItemQty`) in the live codebase, **or**
- **rewire** routes/views to the correct existing implementation *if functionality has moved elsewhere*.

Until remediation is completed and G4 re-verification passes, **no QUO‑V2 execution work is allowed**.

---

## Re-run (post-remediation)

**Re-run Date:** 2025-12-18  
**Live execution branch:** `fix/v2-route-controller-realign` (in `/Users/nirajdesai/Projects/nish/`)  
**Remediation task:** `NSW-P4-QUO-V2-ROUTE-CONTROLLER-REALIGN-001`

### Findings (re-run)

**Routes remain wired as expected (live):**

- `nish/routes/web.php`:
  - Line **337**: `quotation.v2.applyFeederTemplate` → `QuotationV2Controller::applyFeederTemplate`
  - Lines **404–406**: `quotation.v2.item.updateQty` → `QuotationV2Controller::updateItemQty`

**Controller methods now exist (live):**

- `nish/app/Http/Controllers/QuotationV2Controller.php`:
  - Line **3114**: `public function applyFeederTemplate(...)`
  - Line **3287**: `public function updateItemQty(...)`

**Static safety check:**

- `php -l nish/app/Http/Controllers/QuotationV2Controller.php` → **No syntax errors detected**

### Decision (re-run)

**Gate result:** ✅ **G4 PASS** — QUO‑V2 route↔controller surface is now present and no longer fails due to missing methods.  
**Fence status:** QUO‑V2 may be **unfenced** (subject to standard Phase‑4 controls). **S3 Alignment may now begin.**


