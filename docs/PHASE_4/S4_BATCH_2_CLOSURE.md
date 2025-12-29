# S4 Batch-2 — Closure Summary (CIM + MBOM consumer migration)

**Status:** ✅ CLOSED  
**Scope:** UI caller migration only (canonical-first with compat fallback)  
**Guardrails:** no route/URI/name changes; no endpoint deletions; no payload changes

---

## What Batch-2 changed (summary)

Batch‑2 migrated UI dropdown lookups in CIM + MBOM views to use **canonical** `/api/*` endpoints first, with **compat fallback** preserved for safety.

**No backend route changes** were made in Batch‑2. The canonical `/api/*` surface was established in Batch‑1.

---

## Files in scope (completed)

### CIM

- `resources/views/product/create.blade.php`
- `resources/views/product/edit.blade.php`
- `resources/views/generic/create.blade.php`
- `resources/views/generic/edit.blade.php`

### MBOM

- `resources/views/masterbom/create.blade.php`
- `resources/views/masterbom/edit.blade.php`
- `resources/views/masterbom/copy.blade.php`

---

## Evidence notes (audit-safe)

- **Auth-protected `/api/*` routes** return **`302 → /login`** for unauthenticated curl. This is expected Laravel behavior and is not a defect.
- Primary evidence remains **browser-authenticated behavior + snapshot logs** as per `docs/PHASE_4/S4_BATCH_2_TASKS.md`.

---

## Rollback drill (performed)

Rollback drill was executed for MBOM `copy` migration using the standard pattern:

- revert
- verify app still loads (and `/api/*` responds with auth redirect when unauthenticated)
- re-apply via cherry-pick

---

## Key commits (Batch-2 tail)

**Note:** commit hashes may differ across environments if history was rewritten to remove oversized local SQL dumps (push hygiene only).

MBOM `copy` migration (commit → revert → re-apply):

- `S4-B2: MBOM masterbom/copy use canonical /api lookups with compat fallback`
- `Revert "S4-B2: MBOM masterbom/copy use canonical /api lookups with compat fallback"`
- `S4-B2: MBOM masterbom/copy use canonical /api lookups with compat fallback`

---

## Out of scope (explicitly deferred)

### DATA-INTEGRITY-001

Any observed **catalog/master-data correctness issues** (e.g., “tables not properly attached”, legacy upload mapping mismatches, inconsistent selection semantics) are **pre-existing** and are **not** part of Batch‑2. Batch‑2 only proves wiring + safety (canonical-first + fallback) without breaking flows.







