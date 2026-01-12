# Phase 5 Enhancement — In‑DB Search Option (BM25 in Postgres) via `pg_textsearch`

**Date:** 2025-12-26  
**Scope:** NSW Estimation Software (Phase 5 — Enhancements)  
**Type:** Optional capability (Dev-first → Pilot → Production)  

---

## 1) What this is
`pg_textsearch` is an open‑source PostgreSQL extension that implements **BM25 relevance ranking** for keyword search directly inside Postgres.

Instead of syncing data to Elasticsearch/OpenSearch for relevance-ranked keyword search, we can evaluate whether **Postgres-only search** is sufficient for our needs.

---

## 2) Why this matters for NSW Estimation (Phase 5)
Our Phase 5 work is about modernising the **new NSW canonical layer** and making the system usable, fast, and consistent.

A strong in‑DB search layer helps with:
- **Catalog item search** (SKU, make/series, description, attributes)
- **Quotation search** (projects, clients, quote numbers, tags)
- **BOM search** (components, alternates, feature lines, policy outcomes)
- **“Find similar” workflows** (operator productivity)

---

## 3) Key capabilities (as claimed by authors)
- **BM25 ranking** (better relevance than vanilla Postgres full-text ranking)
- Simple query syntax (`ORDER BY column <@> 'terms'`)
- Uses Postgres text search configurations (languages)
- Supports partitioned tables
- Tunable BM25 parameters (`k1`, `b`)
- Extension is open source under the PostgreSQL license

---

## 4) Fit decision for NSW Estimation
### Use `pg_textsearch` when:
- We want **good ranked keyword search** inside Postgres with minimal infra.
- Search needs are mostly **text + metadata filtering**, not heavy faceting/aggregations beyond SQL.
- We want **one source of truth** without search-index drift.

### Prefer external search stack when:
- We require advanced search-engine features (complex analyzers, fuzzy/typo tolerance at scale, geo search, per-field boosting at large scale, multi-stage reranking).
- We need sub‑100ms search latency under heavy concurrent load and very large corpuses.

---

## 5) Phase 5 adoption plan (Dev-only → Pilot)
### Step A — Dev sandbox evaluation
- Use a dev Postgres instance dedicated to the NSW Estimation repo.
- Install/compile the extension in a controlled environment.
- Create a small pilot dataset:
  - `catalog_sku` (SKU, description, make, series)
  - `generic_item` (L1 intent name/description)
  - `quotation` (quote no, client, project)
- Measure:
  - Ranking quality (manual top‑10 checks)
  - Query latency under typical filters
  - Index build time and memory footprint

### Step B — Pilot in feature-flag style (Phase 5 only)
- Add a **search adapter** interface:
  - `SearchProvider = PostgresBM25 | PostgresFTS | ExternalSearch`
- Default: keep current behavior.
- Allow enabling BM25 search on a per‑environment basis.

### Step C — Production decision gate
Adopt only if:
- Ranked results feel clearly better than current approach
- Performance is stable
- Operational burden is acceptable

---

## 6) Risks and constraints
- **Postgres version support:** current releases may target newer Postgres versions; verify compatibility with our selected Postgres baseline before committing.
- **Operational footprint:** indexing architecture may require memory sizing and monitoring.
- **Feature coverage:** BM25 helps ranking, but fuzzy matching / spell correction / synonyms may still require additional design.

---

## 7) Minimal evaluation checklist (what to record)
- [ ] Postgres version and OS confirmed for build/install
- [ ] Extension install steps documented (repeatable)
- [ ] Index definition examples captured
- [ ] 20–30 representative queries collected
- [ ] Before/after relevance snapshots
- [ ] Latency numbers (p50/p95) in dev
- [ ] Decision memo: Adopt / Defer / Reject

---

## 8) References
- Tiger Data blog (BM25 + hybrid retrieval):  
  - https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres
- GitHub repository:  
  - https://github.com/timescale/pg_textsearch
- Docs page:  
  - https://www.tigerdata.com/docs/use-timescale/latest/extensions/pg-textsearch

---

## 9) Notes for NSW Estimation context
This is an **enhancement option** and must not disrupt:
- Phase 4 legacy stabilization
- Phase 5 canonical data model implementation (L1/L2/KVU policy)

Recommendation: treat as a **bolt‑on capability** with a clean adapter boundary, and only promote after a measured pilot.
