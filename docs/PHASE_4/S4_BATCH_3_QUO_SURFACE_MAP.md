# S4 — Batch-3 QUO Surface Map (PLAN-ONLY)
#
# Status: PLAN-ONLY (no execution authorized)
# Last Updated: 2025-12-18

---

## Purpose

Provide an audit-safe, source-backed map of QUO-hosted surfaces in Batch‑3 scope:
- PBOM search surface currently hosted in QUO (`/api/proposal-bom/search`)
- Legacy HTML hydration helpers (direct-coupled)
- ReuseSearchContract endpoints (`/api/reuse/*`)

**Rule:** This document is descriptive only. It does not authorize code changes.

---

## Authority inputs

- S3 alignment (record-only): `docs/PHASE_4/S3_QUO_ALIGNMENT.md`
- Route map (trace authority): `trace/phase_2/ROUTE_MAP.md`
- Snapshot source (implementation evidence):
  - `source_snapshot/routes/web.php`
  - `source_snapshot/app/Http/Controllers/QuotationController.php`
  - `source_snapshot/app/Http/Controllers/ReuseController.php`
  - `source_snapshot/resources/views/quotation/v2/panel.blade.php`
  - `source_snapshot/resources/views/quotation/step.blade.php`

---

## 1) PBOM search surface (QUO-hosted today)

### Route record

| Route name | Method | URI | Handler | Middleware | Classification |
|---|---:|---|---|---|---|
| `api.proposalBom.search` | GET | `/api/proposal-bom/search` | `QuotationController@searchProposalBom` | `auth`, `throttle:search` | **direct-coupled** (S3.4) |

### Request contract (snapshot)

- **Query params**:
  - `q` (string; optional; empty allowed)

### Response contract (snapshot)

- **Shape (Select2)**:
  - `{"results":[{"id":<QuotationSaleBomId>,"text":<display string>}, ...]}`
- **Limit**: 50 items
- **Order**: newest first (by `qsb.updated_at DESC`)

### Known consumers (snapshot)

- **QUO‑V2 panel view**:
  - `source_snapshot/resources/views/quotation/v2/panel.blade.php`
  - Select2 AJAX config reads `data.results` and maps to `{id,text}`
  - Has transport failure handling (warn + empty results) to avoid hard crash

### Migration notes (planning-only)

- **Hard constraint**: keep behavior stable; keep route name/URI stable.
- **Migration candidate**: PBOM/SHARED-owned surface *behind the same route* (handler swap only), with rollback-first discipline.

---

## 2) Legacy HTML hydration helpers (direct-coupled)

### Route record

| Route name | Method | URI | Handler | Return type | Classification |
|---|---:|---|---|---|---|
| `quotation.getMasterBomVal` | GET | `/quotation/getMasterBomVal` | `QuotationController@getMasterBomVal` | HTML (`quotation.item`) | **direct-coupled** (S3.4) |
| `quotation.getProposalBomVal` | GET | `/quotation/getProposalBomVal` | `QuotationController@getProposalBomVal` | HTML (`quotation.item`) | **direct-coupled** (S3.4) |
| `quotation.getSingleVal` | GET | `/quotation/getSingleVal` | `QuotationController@getSingleVal` | HTML (`quotation.item`) | **direct-coupled** (S3.4) |

### Auth note (snapshot)

Even when the route line does not explicitly show middleware, `QuotationController` enforces:
- `__construct() { $this->middleware('auth'); }`

So these endpoints are auth-protected by controller-level middleware.

### Parameters (observed callers; snapshot)

- **Common**:
  - `count` (UI row counter)
  - `co` (UI sub-counter / column index)
  - `it` (item index; sometimes incremented before call)
  - `id` (MasterBomId or QuotationSaleBomId depending on context; may be `0` for “add item”)

- **`getProposalBomVal` additionally**:
  - `QuotationId`
  - `QuotationSaleId`

### Known consumers / call sites (snapshot)

- **Legacy quotation step**: `source_snapshot/resources/views/quotation/step.blade.php`
  - `getMasterBomVal()` chooses:
    - Master BOM hydration → `quotation.getMasterBomVal`
    - Proposal BOM hydration → `quotation.getProposalBomVal`
  - `getSingleVal()` loads a single new component row via `quotation.getSingleVal`

- **QUO‑V2 panel**: `source_snapshot/resources/views/quotation/v2/panel.blade.php`
  - Loads Master BOM components using `quotation.getMasterBomVal` in multiple paths
  - Adds component rows using `quotation.getSingleVal`
  - In at least one flow, parses returned HTML to extract item fields (direct HTML-contract coupling)

### Planning caution

These endpoints are **HTML contracts**. Any HTML structure change can break:
- legacy DOM insertion paths
- QUO‑V2 parsing logic (where present)

Therefore, treat later execution work here as **HIGH/PROTECTED** depending on impacted V2 surfaces.

---

## 3) ReuseSearchContract endpoints (optional Batch‑3 decision)

### Route record

| Route name | Method | URI | Handler | Middleware | Classification |
|---|---:|---|---|---|---|
| `api.reuse.panels` | GET | `/api/reuse/panels` | `ReuseController@searchPanels` | `auth`, `throttle:search` | **contract-based** (S3) |
| `api.reuse.feeders` | GET | `/api/reuse/feeders` | `ReuseController@searchFeeders` | `auth`, `throttle:search` | **contract-based** (S3) |
| `api.reuse.masterBoms` | GET | `/api/reuse/master-boms` | `ReuseController@searchMasterBoms` | `auth`, `throttle:search` | **contract-based** (S3) |
| `api.reuse.proposalBoms` | GET | `/api/reuse/proposal-boms` | `ReuseController@searchProposalBoms` | `auth`, `throttle:search` | **contract-based** (S3) |

### Response shape note (snapshot)

All reuse endpoints supply a Select2-compatible list in `results`, but the envelope is not perfectly consistent:
- Some return `{"results":[...]}`
- Some return `{"success":true,"results":[...],"count":N}`

Consumers should therefore treat `data.results` as the stable field.

### Known consumers (snapshot)

- QUO‑V2 reuse filter modal uses direct endpoint strings:
  - `/api/reuse/panels`
  - `/api/reuse/feeders`
  - `/api/reuse/master-boms`
  - `/api/reuse/proposal-boms`

---

## 4) Batch‑3 execution stance (locked)

Batch‑3 is **PLAN-ONLY**. No changes may be applied to any surface documented here until:
- tasks are approved for execution (S4 governance)
- rollback steps are proven feasible for HIGH/PROTECTED scope
- evidence strategy is agreed per gate requirements


