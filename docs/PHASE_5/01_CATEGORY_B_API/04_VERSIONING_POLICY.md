---
Status: DRAFT
Version: v1.0
Owner: Phase 5 Senate
Last_Updated: 2026-01-27
Scope: Phase-5 Category-B API Versioning Policy
---

# API Versioning Policy

**Purpose:** Define versioning strategy for API contracts to ensure backward compatibility and clear upgrade paths.

**Principle:** Explicit versioning in URL path; backward-compatible changes only within a major version.

---

## Version Format

**Pattern:** `v{major}.{minor}`

- **Major:** Breaking changes (new major version required)
- **Minor:** Non-breaking additions (same major version)

**Current Version:** `v1.0`

---

## Versioning Strategy

### URL-Based Versioning (Primary)

All endpoints are prefixed with `/api/v1`:

```
/api/v1/catalog/items
/api/v1/quotation/{id}/pricing/preview
```

**Benefits:**
- Explicit version in URL
- Easy to route different versions
- Clear upgrade path for clients

---

### Header-Based Versioning (Optional)

Clients can specify version via header:

```
X-API-Version: v1
```

**Usage:** For future flexibility; URL version takes precedence.

---

## Versioning Rules

### Major Version Bump (v1 → v2)

**Required when:**
- Removing endpoints
- Changing request/response structure (breaking)
- Removing required fields
- Changing HTTP methods
- Changing authentication mechanism
- Changing error response format

**Example:**
- v1: `GET /api/v1/catalog/items` returns `{items: []}`
- v2: `GET /api/v2/catalog/items` returns `{data: {items: []}}` (breaking change)

---

### Minor Version Bump (v1.0 → v1.1)

**Allowed when:**
- Adding new endpoints
- Adding optional fields to requests
- Adding new fields to responses (non-breaking)
- Adding new query parameters (optional)
- Adding new error codes
- Improving error messages (non-breaking)

**Example:**
- v1.0: `GET /api/v1/catalog/items` supports `limit`, `offset`
- v1.1: `GET /api/v1/catalog/items` adds optional `sort` parameter (non-breaking)

---

### Patch Changes (v1.0.0 → v1.0.1)

**Internal only:**
- Bug fixes
- Performance improvements
- Documentation updates
- No API contract changes

**Note:** Patch version not exposed in URL (URL remains `/api/v1`).

---

## Backward Compatibility

### Within Major Version (v1.x)

**Required:**
- All v1.0 endpoints must continue to work
- All v1.0 request formats must be accepted
- All v1.0 response formats must be supported (or extended)
- No removal of fields without deprecation period

**Deprecation Process:**
1. Mark field/endpoint as deprecated in OpenAPI spec
2. Add `deprecation_warning` to response
3. Support for at least 6 months
4. Remove in next major version

---

## Version Lifecycle

### v1.0 (Current)

**Status:** Active  
**Freeze Date:** TBD (Category-B completion)  
**End of Life:** TBD (after v2.0 release + 6 months)

**Features:**
- Catalog endpoints (items, SKUs, import)
- Quotation endpoints (CRUD, pricing, discounts)
- BOM endpoints (stubbed)
- Pricing endpoints (stubbed)
- Audit endpoints (stubbed)
- Auth endpoints (stubbed)

---

### v1.1 (Planned)

**Status:** Planned  
**Target Date:** TBD

**Planned Additions:**
- BOM explosion implementation
- Audit event listing
- Auth JWT implementation
- Additional query parameters (sort, filter)

---

### v2.0 (Future)

**Status:** Future  
**Target Date:** TBD

**Potential Breaking Changes:**
- Response format standardization
- Pagination format changes
- Error response format changes

---

## Version Negotiation

### Client Request

**Option 1: URL Version (Recommended)**
```
GET /api/v1/catalog/items
```

**Option 2: Header Version (Future)**
```
GET /api/catalog/items
X-API-Version: v1
```

**Precedence:** URL version > Header version > Default (v1)

---

## Response Version Header

All responses include version in header:

```
X-API-Version: v1.0
```

**Purpose:** Client can verify which version was used.

---

## Migration Guide

### For Clients

**Upgrading from v1.0 to v1.1:**
- No changes required (backward compatible)
- Optional: Use new features (sort, filter)

**Upgrading from v1.x to v2.0:**
- Review breaking changes document
- Update request/response handling
- Test thoroughly before production

---

## Version Documentation

### OpenAPI Spec

Each version has its own OpenAPI spec:

- `openapi-v1.json` — v1.0 spec
- `openapi-v1.1.json` — v1.1 spec (when released)
- `openapi-v2.json` — v2.0 spec (when released)

**Location:** `docs/PHASE_5/01_CATEGORY_B_API/openapi/`

---

## Freeze Policy

### v1.0 Freeze

**Criteria:**
- All endpoints documented
- OpenAPI spec complete
- Validation matrix complete
- Error taxonomy finalized
- Examples documented

**Post-Freeze:**
- No breaking changes without version bump
- Only bug fixes and non-breaking additions
- All changes require Category-D approval

---

## Next Steps

1. Finalize v1.0 API contracts
2. Generate OpenAPI spec
3. Document breaking changes policy
4. Create migration guide template


