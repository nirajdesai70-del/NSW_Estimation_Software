---
Status: CANONICAL
Version: v1.0
Owner: Phase 5 Senate
Last_Updated: 2026-01-27
Scope: Phase-5 Category-C Step-5 Schema Canon
Supersedes: null
---

# NSW Schema Canon v1.0

## 1. Purpose
Defines the authoritative database schema (DDL + constraints) for NSW Estimation Phase-5.

## 2. Scope and Non-Scope
### In scope
- Tables, columns, constraints, indexes
- Enum/check constraints and canonical values
- Tenant isolation rules (tenant_id everywhere)
- Audit/immutability expectations for money fields
- Seed script as design validation artifact

### Out of scope
- UI/UX flows
- Business process documentation (lives in Data Dictionary)
- Runtime compute algorithms (live in QUO/PRICING services)

## 3. Governance Contract
- This document is CANONICAL.
- Changes require: Decision entry + version bump + kb_refresh + governance gate pass.
- Source of truth: `docs/PHASE_5/04_SCHEMA_CANON/INVENTORY/NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv`

## 4. Canonical Table Inventory

**Total Tables:** 34  
**Modules:** 9

### 4.9 AI

- **`ai_call_logs`** — AI advisory call log (reserved)
  - *Note:* Reservation only in Phase-5; AI is advisory-only and must not mutate money fields

### 4.8 AUDIT

- **`audit_logs`** — Append-only audit trail
  - *Note:* entity_id); INDEX(created_at)"

### 4.1 AUTH

- **`roles`** — RBAC roles
  - *Note:* name)"
- **`tenants`** — Multi-tenant isolation root
  - *Note:* Root tenant table; all other tenant_id FKs point here
- **`user_roles`** — User↔Role assignment junction
  - *Note:* Surrogate PK + composite unique; ON DELETE CASCADE from users; RESTRICT from roles
- **`users`** — User accounts/authentication
  - *Note:* email)"

### 4.2 CIM

- **`attribute_options`** — Allowed values for attributes
  - *Note:* Option values can be text or numeric; display_label required
- **`attributes`** — Attribute schema per category
  - *Note:* category_id
- **`catalog_skus`** — L2 commercial SKU identity (SKU-pure)
  - *Note:* make
- **`categories`** — Top-level taxonomy category
  - *Note:* code)"
- **`l1_attributes`** — L1 KVU attributes per intent line
  - *Note:* KVU carrier: attribute_code + (value_text/value_number) + optional unit
- **`l1_intent_lines`** — L1 engineering interpretation line
  - *Note:* Engineering-only; no SKU/price; series_bucket optional text
- **`l1_l2_mappings`** — L1→L2 mapping bridge
  - *Note:* G-08: DO NOT add unique on catalog_sku_id; many L1 lines can map to same SKU
- **`l1_line_groups`** — Group container for related L1 lines
  - *Note:* group_name)"
- **`makes`** — Make master (optional/reserved)
  - *Note:* code)"
- **`product_types`** — Device identity anchor (Type/ProductType)
  - *Note:* Nullable subcategory_id requires partial uniques (Phase-5 friendly)
- **`products`** — Legacy/transitional product identity for QUO binding
  - *Note:* LEGACY/TRANSITIONAL: commercial binding in QUO during Phase-5; pricing truth migrates to L2 SKUs
- **`series`** — Series master (optional/reserved)
  - *Note:* code); INDEX(make_id)"
- **`subcategories`** — Second-level taxonomy under category
  - *Note:* category_id

### 4.3 MBOM

- **`master_bom_items`** — Master BOM template line (L0/L1 only)
  - *Note:* G-01: product_id must be NULL; do NOT FK product_id; defined_spec_json JSONB optional
- **`master_boms`** — Master BOM template header (source-of-truth)
  - *Note:* unique_no)"

### 4.5 PRICING

- **`import_batches`** — Import lineage header
  - *Note:* Links to source_file and imported_at; supports sku_prices lineage
- **`price_lists`** — Price list header
  - *Note:* name)"
- **`prices`** — Legacy product pricing timeline (transitional)
  - *Note:* product_id
- **`sku_prices`** — L2 SKU price timeline (append-only)
  - *Note:* catalog_sku_id

### 4.4 QUO

- **`discount_rules`** — Discount rules (quotation-scoped policy / JSON)
  - *Note:* Schema placeholder: rule_json stores logic; enforcement in QUO compute/resolver
- **`quotations`** — Quotation workspace root
  - *Note:* Snapshot totals written on Apply-Recalc only; status DRAFT/APPROVED/FINALIZED
- **`quote_bom_items`** — Leaf line item with pricing + resolution
  - *Note:* Monetary fields normalized by compute rules (G-03/G-05); override_rate requires reason + attribution
- **`quote_boms`** — BOM/Feeder container under panel (hierarchical)
  - *Note:* Feeder is level=0; origin_master_bom_id is reference-only (NO FK)
- **`quote_panels`** — Panel container under quotation
  - *Note:* Panel totals computed; optional UNIQUE(quotation_id,name) later

### 4.7 SHARED

- **`cost_heads`** — Cost bucket master
  - *Note:* Classification only; precedence: item override → product default → tenant/system default
- **`customers`** — Customer master reference
  - *Note:* Quotation uses customer_name snapshot; customer_id is non-authoritative reference
- **`projects`** — Project master (optional/reserved)
  - *Note:* code)"

### 4.6 TAX

- **`tax_profiles`** — GST tax profile master
  - *Note:* name)"

## 5. Canonical Enums / Check Constraints

### Guardrail Constraints (DB-Enforced)

- **G-01:** Master BOM Rejects ProductId: `master_bom_items.product_id IS NULL`
- **G-02:** Production/L2 Requires ProductId: `resolution_status <> 'L2' OR product_id IS NOT NULL`
- **G-06:** FIXED_NO_DISCOUNT Forces Discount=0: `rate_source <> 'FIXED_NO_DISCOUNT' OR discount_pct = 0`
- **G-07:** Discounts Are Percentage-Only: `discount_pct BETWEEN 0 AND 100`

### Enum Safety Checks

- **`cost_heads`:**
  - `category IN ('MATERIAL','LABOUR','OTHER'`
- **`l1_intent_lines`:**
  - `line_type IN ('BASE','FEATURE'`
- **`l1_l2_mappings`:**
  - `mapping_type IN ('BASE','FEATURE_ADDON','FEATURE_INCLUDED','FEATURE_BUNDLED'`
- **`master_bom_items`:**
  - `resolution_status IN ('L0','L1'`
- **`quotations`:**
  - `tax_mode IS NULL OR tax_mode IN ('CGST_SGST','IGST'`
- **`quote_bom_items`:**
  - `rate_source IN ('PRICELIST','MANUAL_WITH_DISCOUNT','FIXED_NO_DISCOUNT','UNRESOLVED'`
  - `resolution_status IN ('L0','L1','L2'`
- **`quote_boms`:**
  - `level IN (0,1,2`

## 6. Index Strategy

### Tenant Isolation
- All tenant-scoped tables: `INDEX (tenant_id)`

### High-Value Lookups
- `users (tenant_id, email)`
- `quotations (tenant_id, quote_no)`
- `catalog_skus (tenant_id, make, oem_catalog_no)`
- `sku_prices (tenant_id, catalog_sku_id, effective_from DESC)`

### Quote Graph Traversal
- `quote_panels (quotation_id)`
- `quote_boms (quotation_id, panel_id, parent_bom_id)`
- `quote_bom_items (quotation_id, bom_id, panel_id, product_id)`

### L1/L2 Mappings
- `l1_attributes (l1_intent_line_id)`
- `l1_l2_mappings (l1_intent_line_id, catalog_sku_id)`

## 7. DDL (Authoritative)

> See `schema.sql` for complete CREATE TABLE statements, constraints, and indexes.
> DDL is generated from inventory and ordered by dependency.

## 8. Seed Script (Design Validation Artifact)

> See `SEED/NSW_SCHEMA_SEED_v1.0.sql` for minimal seed data to validate:
> - Tenant, users/roles
> - Category tree
> - Sample quotation workspace
> - Sample pricing

## 9. Appendix

### A. Cross-Module Ownership Matrix

| Module | Owner Module | Tables |
|--------|--------------|--------|
| AI | AI | `ai_call_logs` |
| AUDIT | AUDIT | `audit_logs` |
| AUTH | AUTH | `roles`, `tenants`, `user_roles`, `users` |
| CIM | CIM | `attribute_options`, `attributes`, `catalog_skus`, `categories`, `l1_attributes`, `l1_intent_lines`, `l1_l2_mappings`, `l1_line_groups`, `makes`, `product_types`, `products`, `series`, `subcategories` |
| MBOM | MBOM | `master_bom_items`, `master_boms` |
| PRICING | PRICING | `import_batches`, `price_lists`, `prices`, `sku_prices` |
| QUO | QUO | `discount_rules`, `quotations`, `quote_bom_items`, `quote_boms`, `quote_panels` |
| SHARED | SHARED | `cost_heads`, `customers`, `projects` |
| TAX | TAX | `tax_profiles` |

### B. Guardrail Enforcement Mapping

| Guardrail | Enforcement Level | Table/Column | Constraint Type |
|-----------|-------------------|--------------|-----------------|
| G-01 | DB CHECK | `master_bom_items.product_id` | `CHECK (product_id IS NULL)` |
| G-02 | DB CHECK | `quote_bom_items.resolution_status`, `product_id` | `CHECK (resolution_status <> 'L2' OR product_id IS NOT NULL)` |
| G-03 | Compute | `quote_bom_items.amount` | Normalization logic |
| G-04 | Compute + DB | `quote_bom_items.rate_source` | Enum CHECK + consistency rules |
| G-05 | Compute | `quote_bom_items.*` (UNRESOLVED) | Normalization logic |
| G-06 | DB CHECK | `quote_bom_items.rate_source`, `discount_pct` | `CHECK (rate_source <> 'FIXED_NO_DISCOUNT' OR discount_pct = 0)` |
| G-07 | DB CHECK | `quote_bom_items.discount_pct`, `quotations.discount_pct` | `CHECK (discount_pct BETWEEN 0 AND 100)` |
| G-08 | Schema Design | `l1_l2_mappings.catalog_sku_id` | No unique constraint (allows reuse) |

### C. Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | 2026-01-27 | Initial Schema Canon compilation from Step-1/2/3 artifacts | Phase 5 Senate |

---

**Last Updated:** 2026-01-27  
**Status:** CANONICAL — Schema structure ready; DDL requires column completion from Blueprint
