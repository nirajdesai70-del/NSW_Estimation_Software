# S4 — Propagation Plan (Contract Adoption + Extraction Strategy)
#
# Status: ACTIVE (S4)
# Last Updated: 2025-12-18

---

## 1) Objective

Execute controlled propagation of frozen S3 contracts:
- SHARED contract ownership realized in code (without breaking callers)
- CIM consumers migrated to canonical SHARED endpoints
- Apply surfaces remain stable; only consumption alignment propagation occurs
- QUO legacy responsibilities reduced gradually (no big-bang)

---

## 2) Non-negotiable rules

- No route renames in Batch-1
- No payload shape changes in Batch-1
- No controller refactors beyond the planned extraction seams
- No removal of compat endpoints until S5 Bundle C passes

---

## 3) Propagation waves (recommended)

### Wave 1 — SHARED Extraction (foundation)
Goal: create SHARED-owned controller(s) without changing route names/URIs.

- Extract CatalogLookup endpoints into a SHARED controller:
  - `CatalogLookupController` (new, SHARED owner)
- Keep routes identical; only change handler targets
- ReuseSearch endpoints may remain in `ReuseController` in Wave 1 (optional), or also moved if low risk

### Wave 2 — Consumer Migration (CIM + MBOM helper endpoints)
Goal: stop using module-local compat endpoints where safe, but keep them for fallback.

- Update CIM views/JS to call canonical `/api/*` endpoints instead of `/product/get*`
- Update MBOM views/JS to call canonical `/api/*` endpoints instead of `/masterbom/get*`
- Keep compat endpoints alive (no deletions yet)

### Wave 3 — QUO Legacy disentangling (record-only to execution)
Goal: reduce QUO acting as “everything hub”.

- Stop QUO legacy pages from calling module-local endpoints if contract equivalents exist
- Maintain legacy HTML hydration endpoints (do not break)
- Do not touch pricing/discount logic

**Batch-3 (PLAN-ONLY) artifacts (authoritative):**
- `docs/PHASE_4/S4_BATCH_3_TASKS.md`
- `docs/PHASE_4/S4_BATCH_3_QUO_SURFACE_MAP.md`
- `docs/PHASE_4/S4_BATCH_3_DECISION_LOG.md`

### Wave 4 — Clean-up preparation (S5 readiness)
Goal: ensure everything is measurable and revertible.

- Confirm no consumer depends on undocumented payload fields
- Prepare removal candidates list (no deletions yet)
- Ensure bundles A/B/C cover new wiring

---

## 4) Test bundles mapping (must be run in S5)

- Bundle A (Apply): V2 apply surfaces remain valid
- Bundle B (Costing/Quantity): no double-counting or rollup drift
- Bundle C (Catalog Validity): dropdowns + searches behave consistently after migration


