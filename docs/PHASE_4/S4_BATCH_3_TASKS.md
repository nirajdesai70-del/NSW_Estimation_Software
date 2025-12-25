# S4 — Batch-3 Task Set (PLAN-ONLY: QUO consumers + direct-coupled surfaces)
#
# Status: PLAN-ONLY (no execution authorized)
# Last Updated: 2025-12-18

---

## Batch intent (authoritative)

Batch-3 is the next propagation wave **planning pack** focused on QUO-side consumers and remaining “direct-coupled” surfaces identified in S3.4.

**Batch-3 is PLAN-ONLY**:
- ❌ No code changes
- ❌ No behavior change
- ❌ No payload normalization
- ❌ No endpoint deletions
- ✅ Documentation, mapping, rollback-first thinking, and decision clarity

---

## Batch-3 scope (planning only)

### 1) PBOM search surface (currently QUO-hosted)

- **Route name:** `api.proposalBom.search`
- **URI:** `GET /api/proposal-bom/search`
- **Handler:** `QuotationController@searchProposalBom`
- **Primary consumer:** QUO‑V2 Select2 (Proposal BOM finder)
- **Classification (S3.4):** **direct-coupled**

**Contract facts (snapshot):**
- Request param: `q` (string; empty allowed)
- Response shape (Select2): `{"results":[{"id": "...","text":"..."}]}`
- Route is `auth` + `throttle:search`

**Planning questions to answer (no execution):**
- Should ownership remain **QUO** or migrate to **PBOM**/**SHARED** later?
- What is the *minimum stable payload contract* required by V2 Select2?
- What is the safest migration shape **without changing route name/URI**?

---

### 2) Legacy HTML hydration helpers (direct-coupled)

Recorded in S3.4:
- `quotation.getMasterBomVal` → `GET /quotation/getMasterBomVal` → `QuotationController@getMasterBomVal`
- `quotation.getProposalBomVal` → `GET /quotation/getProposalBomVal` → `QuotationController@getProposalBomVal`
- `quotation.getSingleVal` → `GET /quotation/getSingleVal` → `QuotationController@getSingleVal`

**Contract facts (snapshot):**
- These endpoints return **HTML** via the `quotation.item` view.
- Legacy screens inject the HTML into DOM; QUO‑V2 *also* uses these endpoints as fallback and, in some paths, parses the returned HTML.
- `QuotationController` is protected by controller-level `auth` middleware (constructor), so these endpoints are auth‑protected even if routes don’t explicitly declare middleware.

**Planning goals (no execution):**
- Map exact callers (legacy vs V2 vs fallback-only).
- Identify the parameters used by each caller (`count`, `id`, `co`, `it`, plus `QuotationId`/`QuotationSaleId` for PBOM hydration).
- Decide the future stance (explicitly deferred from Batch‑3 execution):
  - keep as legacy-only forever, or
  - wrap behind an adapter (future), or
  - migrate to JSON contract later (future; **not now**)

---

### 3) ReuseSearchContract (optional decision in this batch)

- **Routes:** `GET /api/reuse/*`
- **Handler:** `ReuseController@searchPanels/searchFeeders/searchMasterBoms/searchProposalBoms`
- **Classification (S3):** **contract-based** (treated as SHARED-owned contract)

**Planning decision to make (no execution):**
- Extract reuse endpoints into **SHARED** later, or keep in `ReuseController` until after S5.

---

## Task list (planning-only)

### S4-B3-001 — PBOM search surface contract capture + migration plan stub

- **Task ID:** NSW-P4-S4-QUO-PBOM-SEARCH-PLAN-001
- **Risk:** HIGH / G3 (QUO blast radius) | **Escalation rule:** elevate to **PROTECTED / G4** if handler changes touch **V2 UI** or **route middleware**
- **Objective:** Freeze the exact Select2 contract and caller expectations for `/api/proposal-bom/search`, then define a rollback-first migration pattern (no implementation).
- **In scope (planning):**
  - Document request/response contract and query semantics (empty `q` behavior; limit; ordering)
  - Identify all callers (V2 Select2 instances + any reuse flows)
  - Define migration options (handler extraction vs proxy endpoint vs dual-handler behind flag)
- **Forbidden (Batch-3):**
  - Any code edits
  - Any route/controller movement
  - Any query or payload changes
- **Rollback hooks (hypothetical, for later execution):**
  - Keep route name + URI stable; change handler behind the same route only if rollback is trivial (single revert)
  - Maintain a “shadow” fallback path (e.g. QUO handler remains callable during rollout)
  - Prefer a runtime toggle (owner switch) only if it can be proven safe + observable
- **Evidence strategy (for later execution):**
  - Snapshot route list + middleware
  - Browser-authenticated V2 flow: open modal, search, select item
  - Curl unauthenticated: `302 → /login` acceptable

### S4-B3-002 — Legacy hydration endpoint caller map + fallback explicitness plan

- **Task ID:** NSW-P4-S4-QUO-HYDRATION-MAP-001
- **Risk:** HIGH (HTML hydration + DOM parsing coupling) | **Escalation rule:** treat as **PROTECTED / G4** if any **V2 parsing path** is involved
- **Objective:** Map every caller and parameter contract of the three legacy hydration endpoints, and define “fallback is explicit” requirements without refactoring code.
- **In scope (planning):**
  - Call-site inventory (blade/js) for:
    - `getMasterBomVal`
    - `getProposalBomVal`
    - `getSingleVal`
  - Identify any V2 caller that parses returned HTML
  - Define future “adapter boundary” candidates (document-only)
- **Forbidden (Batch-3):**
  - Any endpoint edits or HTML changes
  - Any JS behavior changes
- **Rollback hooks (hypothetical, for later execution):**
  - If a caller is migrated, preserve compat fallback (canonical-first pattern) until S5 passes
- **Evidence strategy (for later execution):**
  - Browser-auth: legacy quotation step UI loads BOM items, adds item, saves
  - Browser-auth: V2 modal loads items and add component works

### S4-B3-003 — ReuseSearchContract ownership decision (keep vs extract)

- **Task ID:** NSW-P4-S4-REUSE-CONTRACT-DECIDE-001
- **Risk:** MEDIUM (contract-based, but QUO-hosted) | **Gate if executed later:** G3 or G4 depending on touched files
- **Objective:** Decide whether `/api/reuse/*` stays in `ReuseController` for S4 or becomes a SHARED-owned surface in a later batch.
- **In scope (planning):**
  - Confirm consumers and expected response shapes per endpoint
  - Define extraction approach that keeps route names/URIs stable
- **Forbidden (Batch-3):** any extraction or refactor

---

## Evidence + audit notes (carried forward)

- **Auth-protected routes** may return **`302 → /login`** for unauthenticated curl; this is expected Laravel behavior.
- Primary evidence remains **browser-authenticated behavior + snapshot logs** as per S4 governance.


