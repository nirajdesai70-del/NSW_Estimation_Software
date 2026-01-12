# Category-B API / Contract Layer

**Status:** DRAFT  
**Version:** v1.0  
**Owner:** Phase 5 Senate

---

## Overview

Category-B defines and freezes the API contracts that consume Schema Canon v1.0 and RAG KB v1.0, without modifying either.

**Core Principle:** APIs are consumers of canonical sources; they never mutate the schema or KB internals.

---

## Documents

1. **[CATEGORY_B_CHARTER.md](./CATEGORY_B_CHARTER.md)** — Charter, scope, acceptance gates
2. **[01_API_SURFACE_MAP.md](./01_API_SURFACE_MAP.md)** — Complete endpoint inventory
3. **[02_VALIDATION_MATRIX.md](./02_VALIDATION_MATRIX.md)** — API ↔ DB guardrails parity
4. **[03_ERROR_TAXONOMY.md](./03_ERROR_TAXONOMY.md)** — Error codes, messages, HTTP status
5. **[04_VERSIONING_POLICY.md](./04_VERSIONING_POLICY.md)** — Versioning strategy and compatibility
6. **[05_OPENAPI_SKELETON.yaml](./05_OPENAPI_SKELETON.yaml)** — OpenAPI v3.1 spec (draft)

---

## Quick Reference

### Endpoint Summary

- **System:** 2 endpoints (✅ implemented)
- **Catalog:** 5 endpoints (✅ implemented)
- **BOM:** 2 endpoints (⏳ stubbed)
- **Pricing:** 2 endpoints (⏳ stubbed)
- **Quotation:** 8 endpoints (4 ✅ implemented, 4 ⏳ stubbed)
- **Audit:** 2 endpoints (⏳ stubbed)
- **Auth:** 3 endpoints (⏳ stubbed)

**Total:** 22 endpoints (8 implemented, 14 stubbed)

---

## Validation Parity

**Status:** 8/9 guardrails mapped (89%)

- ✅ G-01: Tenant Isolation
- ✅ G-02: FINAL-Only Import
- ✅ G-03: Price Validation
- ✅ G-04: Currency Validation
- ✅ G-05: UNRESOLVED Handling
- ✅ G-06: Fixed Lines Excluded
- ✅ G-07: SKU Code Validation
- ⏳ G-08: L1→L2 Mapping (pending BOM explosion)
- ✅ A5.2: IsLocked Enforcement

---

## Error Taxonomy

**Format:** `{CATEGORY}_{SPECIFIC_ERROR}`

- **VALIDATION_*** — 400 Bad Request
- **AUTH_*** — 401 Unauthorized
- **PERMISSION_*** — 403 Forbidden
- **NOT_FOUND_*** — 404 Not Found
- **CONFLICT_*** — 409 Conflict
- **SEMANTIC_*** — 422 Unprocessable Entity
- **INTERNAL_*** — 500 Internal Server Error

---

## Versioning

**Current Version:** v1.0  
**Strategy:** URL-based (`/api/v1/...`)  
**Backward Compatibility:** Required within major version

---

## B3 Implementation Backlog

**Priority:** High-impact engineering tickets to close remaining gaps.

### 1. Request ID Middleware ✅ **Design Complete**
- **Status:** Design documented in `03_ERROR_TAXONOMY.md`
- **Implementation:** Add `RequestIDMiddleware` to `app/middleware/`
- **Outcome:** All requests get UUID v4 `request_id` + `X-Request-ID` header

### 2. Error Response Wrapper ✅ **Design Complete**
- **Status:** Design documented in `03_ERROR_TAXONOMY.md`
- **Implementation:** Add exception handlers to `app/core/exceptions.py`
- **Outcome:** All errors return standard format: `{detail, error_code, request_id, version}`

### 3. Error Code Constants
- **Status:** ⏳ Pending implementation
- **Implementation:** Create `app/core/error_codes.py` with all constants
- **Outcome:** Centralized error codes, IDE autocomplete, prevents typos

### 4. OpenAPI Completion for Stubbed Endpoints
- **Status:** ⏳ Pending
- **Implementation:** Add schemas + placeholder responses for 14 stubbed endpoints
- **Outcome:** Complete API contract documentation

### 5. G-08 Parity (BOM Explosion)
- **Status:** ⏳ Pending BOM explosion implementation
- **Implementation:** Add validation when `POST /api/v1/bom/explode` is implemented
- **Outcome:** Complete guardrail validation matrix (9/9)

---

## Next Steps

1. ✅ **Design complete** — Request ID middleware + error wrapper (see `03_ERROR_TAXONOMY.md`)
2. ⏳ **Implement middleware** — Request ID generation + error response wrapper
3. ⏳ **Add error constants** — Create `app/core/error_codes.py`
4. ⏳ **Update endpoints** — Replace `HTTPException` with standardized format
5. ⏳ **Complete OpenAPI** — Add schemas for stubbed endpoints
6. ⏳ **G-08 validation** — Add when BOM explosion is implemented
7. ⏳ **Prepare Category-D freeze** — Package for freeze gate

---

## References

- Schema Canon: `../04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- RAG KB: Tag `rag-kb-v1.0-bm25-sha256`
- Validation Guardrails: `../02_FREEZE_GATE/A1_Validation_Guardrails/`
- Data Dictionary: `../03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md`


