# S4 — Batch-3 Decision Log (PLAN-ONLY)
#
# Status: ACTIVE (planning log)
# Last Updated: 2025-12-18

---

## Purpose

Record Batch‑3 decisions and explicit deferrals so the plan is audit-safe and does not “drift into execution”.

**Rule:** Batch‑3 is PLAN‑ONLY. No code changes are authorized by this file.

---

## Decisions (authoritative)

### B3-D-001 — Batch‑3 execution mode

- **Decision:** Batch‑3 is **PLAN‑ONLY**.
- **Rationale:** QUO surfaces have higher blast radius; Batch‑2 just stabilized consumer migration and governance posture. Planning must lock scope + rollback before touching QUO.
- **Resulting constraint:** No routes/controllers/JS/queries are modified in Batch‑3.

### B3-D-002 — PBOM search surface ownership (for now)

- **Decision:** Keep `/api/proposal-bom/search` **QUO-hosted** during Batch‑3 (no migration).
- **Rationale:** It is used by QUO‑V2 Select2; preserving the exact Select2 contract is non-negotiable. Ownership migration is a later S4 execution step only after contract capture + rollback plan is proven.
- **Preconditions for later execution:**
  - Contract frozen (request params + response envelope + ordering/limit behavior)
  - All callers enumerated (V2 modal(s), reuse flows, any legacy screens)
  - Rollback is one-step (single revert) and observable

### B3-D-003 — Legacy HTML hydration endpoints stance (for now)

- **Decision:** Do not refactor or “clean up” the legacy hydration endpoints in Batch‑3:
  - `quotation.getMasterBomVal`
  - `quotation.getProposalBomVal`
  - `quotation.getSingleVal`
- **Rationale:** These endpoints return `quotation.item` HTML and are directly coupled to DOM insertion and, in some V2 flows, HTML parsing. Any change is high-risk and must be treated as controlled execution later.
- **Preconditions for later execution:**
  - Caller map (legacy vs V2) complete
  - Fallback logic is explicit in callers (canonical-first with compat fallback pattern where applicable)
  - Evidence bundle defined for both legacy + V2 behaviors

### B3-D-004 — ReuseSearchContract extraction (deferred)

- **Decision:** Do not extract `/api/reuse/*` out of `ReuseController` in Batch‑3.
- **Rationale:** S3 already treats the reuse endpoints as SHARED contracts; extraction is optional and should occur only when rollback discipline + evidence bundles are ready, not during Batch‑3 planning.

---

## Explicit non-goals (Batch‑3)

- No route renames (name or URI)
- No controller moves/splits
- No payload normalization or “shape cleanup”
- No endpoint deletions
- No refactors of QUO legacy or QUO‑V2 logic

---

## Outputs produced by Batch‑3

- `docs/PHASE_4/S4_BATCH_3_TASKS.md`
- `docs/PHASE_4/S4_BATCH_3_QUO_SURFACE_MAP.md`
- This decision log


