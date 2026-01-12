---
Status: ACTIVE
Version: v1.0
Owner: Phase 5 Senate
Last_Updated: 2026-01-27
Scope: Phase-5 Category-B API/Contract Layer
Supersedes: null
---

# Category-B Charter — API / Contract Layer

## 1. Objective

Define and freeze the API contracts that consume Schema Canon v1.0 and RAG KB v1.0, without modifying either.

**Core Principle:** APIs are consumers of canonical sources; they never mutate the schema or KB internals.

---

## 2. Scope and Non-Scope

### In Scope (IN)
- Public & internal API endpoints (REST)
- Request/response JSON schemas
- Validation rules (mapped to DB guardrails)
- Error taxonomy & response format standards
- Versioning & backward compatibility rules
- Pagination, sorting, determinism contracts
- Idempotency rules (where applicable)

### Out of Scope (STRICT)
- Schema changes (Category-C, frozen)
- Runtime/UI logic (separate layer)
- Indexing or KB internals (Phase-3, tagged)
- Business process documentation (Data Dictionary)

---

## 3. Read-Only Inputs

**Do Not Modify:**
- `docs/PHASE_5/04_SCHEMA_CANON/DDL/schema.sql` (Schema Canon v1.0)
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- RAG KB (BM25 + strict SHA256, tagged: `rag-kb-v1.0-bm25-sha256`)
- `/health` endpoint (backend metadata)

---

## 4. Deliverables

1. **API Surface Map** — Endpoint list + ownership + source tables
2. **OpenAPI / JSON Schemas** — Request & response models (v1)
3. **Validation Matrix** — API rules ↔ DB guardrails parity proof
4. **Error Taxonomy** — Codes, messages, HTTP status mapping
5. **Versioning Rules** — v1, v1.1 compatibility policy
6. **Examples** — curl / JSON request/response samples
7. **Freeze Note** — Commit + tag declaration

---

## 5. Contract Rules (Non-Negotiable)

1. **Consumption Only** — APIs consume Category-C; never mutate it
2. **Fail-Fast Validation** — API validation mirrors DB guardrails
3. **Deterministic Responses** — Ordering, pagination, sorting are explicit
4. **Explicit Versioning** — URL or header-based (e.g., `/api/v1/...`)
5. **Backward Compatibility** — v1 changes require version bump
6. **Minimal Payloads** — No temporary fields; explicit defaults

---

## 6. Acceptance Gates

- [ ] All endpoints validated against Schema Canon
- [ ] Guardrail parity proven (API ↔ DB)
- [ ] No breaking change to v1 once frozen
- [ ] OpenAPI spec passes lint + example calls
- [ ] Error taxonomy approved
- [ ] Versioning policy documented
- [ ] Commit + tag present

---

## 7. Do / Don't

### Do
- Centralize error codes
- Include `request_id` and `version` in responses
- Keep payloads minimal and explicit
- Document defaults explicitly
- Map validation to DB guardrails

### Don't
- Infer schema behavior in API
- Add "temporary" fields
- Reopen Category-C decisions
- Modify frozen artifacts
- Break backward compatibility without version bump

---

## 8. Category-B Exit Criteria

- [ ] API spec frozen (OpenAPI v3)
- [ ] Example calls documented
- [ ] Validation matrix complete
- [ ] Error taxonomy finalized
- [ ] Ready for client integration or mock testing
- [ ] Commit + tag: `category-b-api-v1.0`

---

## 9. Phased Execution Plan

### B1 — Inventory & Mapping
- List endpoints (read/write)
- Map each to tables/guardrails
- Identify required filters & joins

**Gate B1:** No ambiguity in ownership or data source.

### B2 — Schema Definition
- Define request/response JSON schemas
- Pagination & sorting contracts
- Idempotency rules (if applicable)

**Gate B2:** Schemas lint clean; examples validated.

### B3 — Validation & Errors
- Guardrail parity (e.g., ranges, required fields)
- Error codes (stable) + HTTP statuses
- `request_id` propagation

**Gate B3:** Matrix proves API ↔ DB parity.

### B4 — Versioning & Freeze
- Version policy documented
- Tag commit
- Freeze declaration

**Gate B4:** Ready for Category-D approval.

---

## 10. References

- Schema Canon: `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- RAG KB: Tag `rag-kb-v1.0-bm25-sha256`
- Validation Guardrails: `docs/PHASE_5/02_FREEZE_GATE/A1_Validation_Guardrails/`
- Data Dictionary: `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md`

---

**Next Step:** Create API Surface Map (see `01_API_SURFACE_MAP.md`)


