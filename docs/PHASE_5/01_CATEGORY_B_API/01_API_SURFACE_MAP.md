---
Status: DRAFT
Version: v1.0
Owner: Phase 5 Senate
Last_Updated: 2026-01-27
Scope: Phase-5 Category-B API Surface Inventory
---

# API Surface Map

**Purpose:** Complete inventory of all API endpoints, mapped to schema tables and guardrails.

**Last Updated:** 2026-01-27  
**Total Endpoints:** 22 (8 implemented, 14 stubbed)

---

## Endpoint Inventory

### System Endpoints

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/` | GET | Root info | None | None | `{message, version, status}` | System | ✅ Implemented |
| `/health` | GET | Health check | None | None | `{status, service}` | System | ✅ Implemented |

**Note:** Main API health endpoint (port 8003) returns minimal status. RAG KB service has separate `/health` at port 8099 (reports `keyword_backend=bm25`, `keyword_docs`, versions).

---

### Catalog Endpoints (`/api/v1/catalog`)

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/api/v1/catalog/items` | GET | List items (browse/search) | `catalog_items` | G-01: tenant_id, pagination | `{total, limit, offset, items[]}` | Catalog | ✅ Implemented |
| `/api/v1/catalog/items/{item_id}` | GET | Get item + SKUs | `catalog_items`, `catalog_skus` | G-01: tenant_id | `{id, item_code, name, ..., skus[]}` | Catalog | ✅ Implemented |
| `/api/v1/catalog/skus` | GET | List SKUs (pricing truth) | `catalog_skus` | G-01: tenant_id, pagination | `{total, limit, offset, skus[]}` | Catalog | ✅ Implemented |
| `/api/v1/catalog/skus/{sku_id}` | GET | Get SKU + price history | `catalog_skus`, `sku_prices` | G-01: tenant_id | `{id, sku_code, ..., price_history[]}` | Catalog | ✅ Implemented |
| `/api/v1/catalog/skus/import` | POST | Import SKUs from CSV | `catalog_items`, `catalog_skus`, `sku_prices`, `price_lists`, `import_batches` | G-02: FINAL-only, G-03: price validation, G-04: currency | `{batch_id, rows_total, rows_valid, ...}` | Catalog | ✅ Implemented |

**Catalog Notes:**
- SKU is pricing truth (ADR-0001)
- Auto-creates `CatalogItem` grouped by series
- Upserts `CatalogSku` (make+sku_code unique)
- Archives prices in `SkuPrice` (append-only)
- Updates `CatalogSku.current_price` for fast quoting

---

### BOM Endpoints (`/api/v1/bom`)

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/api/v1/bom/explode` | POST | BOM explosion (L1→L2) | `l1_intent_lines`, `l1_l2_mappings`, `catalog_skus` | G-08: many L1→same SKU | `{tenant_id, input, summary, unmapped[], items[], warnings[]}` | BOM | ✅ Implemented |
| `/api/v1/bom/{bom_id}` | GET | Get BOM by ID | `master_boms`, `master_bom_items` | G-01: tenant_id | TBD | BOM | ⏳ Stubbed |

**BOM Notes:**
- L1→L2 mapping uses `l1_l2_mappings` bridge
- G-08: DO NOT add unique on `catalog_sku_id` (many L1 lines can map to same SKU)

---

### Pricing Endpoints (`/api/v1/pricing`)

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/api/v1/pricing/import` | POST | Import catalog prices | `sku_prices`, `price_lists`, `import_batches` | G-02: FINAL-only, G-03: price validation | TBD | Pricing | ⏳ Stubbed |
| `/api/v1/pricing/rules` | GET | List price rules | `discount_rules` | G-01: tenant_id | TBD | Pricing | ⏳ Stubbed |

**Pricing Notes:**
- Price lists link to `import_batches` for lineage
- Discount rules are quote-scoped (MAKE_SERIES, CATEGORY, SITE)

---

### Quotation Endpoints (`/api/v1/quotation`)

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/api/v1/quotation/` | GET | List quotations | `quotations` | G-01: tenant_id, pagination | TBD | Quotation | ⏳ Stubbed |
| `/api/v1/quotation/` | POST | Create quotation | `quotations` | G-01: tenant_id, G-05: UNRESOLVED handling | TBD | Quotation | ⏳ Stubbed |
| `/api/v1/quotation/{quotation_id}` | GET | Get quotation by ID | `quotations`, `quote_bom_items` | G-01: tenant_id | TBD | Quotation | ⏳ Stubbed |
| `/api/v1/quotation/{quotation_id}/revisions` | POST | Create revision | `quotations`, `quotation_revisions` | G-01: tenant_id | TBD | Quotation | ⏳ Stubbed |
| `/api/v1/quotation/{quotation_id}/discount/quotation` | PUT | Set quotation-level discount | `quotations` | G-06: fixed lines excluded, role-based | `{quotation_id, discount_pct, message}` | Quotation | ✅ Implemented |
| `/api/v1/quotation/{quotation_id}/pricing/preview` | POST | Preview pricing (no DB write) | `quotations`, `quote_bom_items`, `discount_rules`, `tax_profiles` | G-05: UNRESOLVED=0, G-06: fixed lines excluded | `{quotation_id, subtotal, discounted_subtotal, gst, grand_total, flags[]}` | Quotation | ✅ Implemented |
| `/api/v1/quotation/{quotation_id}/pricing/apply-recalc` | POST | Apply pricing recalculation | `quotations`, `quote_bom_items`, `discount_rules`, `tax_profiles` | G-05: UNRESOLVED=0, G-06: fixed lines excluded, Reviewer/Approver only | `{quotation_id, decision_id, message, totals, gst}` | Quotation | ✅ Implemented |
| `/api/v1/quotation/{quotation_id}/bom/item/{line_id}` | DELETE | Delete quote BOM line | `quote_bom_items` | A5.2: is_locked enforcement, G-01: tenant_id | `{message, line_id, quotation_id}` | Quotation | ✅ Implemented |

**Quotation Notes:**
- G-05: UNRESOLVED / price-missing lines contribute zero
- G-06: FIXED_NO_DISCOUNT lines excluded from all discounts (including quotation-level)
- A5.2: Deletion blocked if `is_locked = true` (returns 409 LINE_ITEM_LOCKED)
- Discount precedence: LINE > MAKE_SERIES > CATEGORY > SITE
- Tax modes: CGST_SGST, IGST (via `tax_profiles`)

---

### Audit Endpoints (`/api/v1/audit`)

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/api/v1/audit/events` | GET | List audit events | `audit_logs` | G-01: tenant_id, pagination | TBD | Audit | ⏳ Stubbed |
| `/api/v1/audit/changes/{entity_type}/{entity_id}` | GET | Get change log for entity | `audit_logs` | G-01: tenant_id | TBD | Audit | ⏳ Stubbed |

**Audit Notes:**
- Append-only audit trail
- Indexed on `(entity_type, entity_id)` and `created_at`

---

### Auth Endpoints (`/api/v1/auth`)

| Endpoint | Method | Purpose | Source Tables | Guardrails | Response Shape | Owner | Status |
|----------|--------|---------|---------------|------------|-----------------|-------|--------|
| `/api/v1/auth/login` | POST | Login | `users`, `user_roles`, `roles` | Password validation, rate limiting | TBD | Auth | ⏳ Stubbed |
| `/api/v1/auth/refresh` | POST | Refresh token | `users` | Token validation | TBD | Auth | ⏳ Stubbed |
| `/api/v1/auth/me` | GET | Get current user | `users`, `user_roles`, `roles` | G-01: tenant_id | TBD | Auth | ⏳ Stubbed |

**Auth Notes:**
- Phase-5: Stub implementation using headers (`X-User-ID`, `X-User-Roles`)
- TODO: Replace with proper JWT/auth middleware

---

## Endpoint Summary by Status

- **✅ Implemented:** 9 endpoints
- **⏳ Stubbed:** 13 endpoints
- **Total:** 22 endpoints

---

## Common Patterns

### Pagination
- Query params: `limit` (default 50, max 200), `offset` (default 0)
- Response: `{total, limit, offset, items[]}`

### Search/Filter
- Query param: `q` (text search)
- Filters: `make`, `item_id`, etc. (domain-specific)

### Tenant Isolation
- All endpoints enforce `tenant_id` (G-01)
- Extracted via `X-Tenant-ID` header (stub) or JWT (future)

### Error Responses
- Format: `{detail: string}` or `{detail: {message, summary}}`
- HTTP status: 400 (validation), 404 (not found), 409 (conflict), 403 (forbidden), 500 (server error)

---

## Next Steps

1. Complete OpenAPI schemas for all endpoints
2. Map validation rules to DB guardrails (see `02_VALIDATION_MATRIX.md`)
3. Define error taxonomy (see `03_ERROR_TAXONOMY.md`)
4. Document versioning policy (see `04_VERSIONING_POLICY.md`)


