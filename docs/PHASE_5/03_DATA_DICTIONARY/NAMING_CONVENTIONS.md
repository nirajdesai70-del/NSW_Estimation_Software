# Naming Conventions

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Purpose:** Define naming standards for tables, columns, foreign keys, enums, timestamps, and IDs

---

## Purpose

This document defines canonical naming conventions for the NSW schema. Consistent naming ensures:
- Clarity and readability
- Predictable patterns
- Easy maintenance
- Standard tooling support

---

## Table Naming

### Standard: snake_case, Plural

**Rule:** Table names use `snake_case` and are **plural**.

**Examples:**
- ✅ `users` (not `user` or `Users`)
- ✅ `products` (not `product` or `Products`)
- ✅ `quote_bom_items` (not `quoteBomItems` or `QuoteBomItems`)
- ✅ `master_boms` (not `masterBoms` or `MasterBoms`)

**Rationale:**
- Plural reflects that table contains multiple rows
- snake_case is standard for SQL databases
- Consistent with PostgreSQL conventions

---

## Column Naming

### Standard: snake_case, Singular

**Rule:** Column names use `snake_case` and are **singular** (for scalar values).

**Examples:**
- ✅ `product_id` (not `productId` or `productID`)
- ✅ `created_at` (not `createdAt` or `CreatedAt`)
- ✅ `is_active` (not `isActive` or `IsActive`)
- ✅ `cost_head_id` (not `costHeadId` or `CostHeadId`)

**Rationale:**
- Singular for scalar values (one value per row)
- snake_case matches table naming
- Consistent with PostgreSQL conventions

---

## Foreign Key Naming

### Pattern: `{referenced_table_singular}_id`

**Rule:** Foreign key columns follow pattern: `{referenced_table_singular}_id`

**Examples:**
- `products.id` → `quote_bom_items.product_id`
- `users.id` → `quotations.created_by` (user reference)
- `master_boms.id` → `quote_boms.origin_master_bom_id`
- `cost_heads.id` → `quote_bom_items.cost_head_id`

**Special Cases:**
- User references: `created_by`, `updated_by`, `modified_by` (not `user_id`)
- Timestamp references: `created_at`, `updated_at`, `modified_at` (not `timestamp_id`)

**Rationale:**
- Clear relationship to referenced table
- Predictable pattern for lookups
- Self-documenting code

---

## Enum Naming

### Standard: UPPER_SNAKE_CASE

**Rule:** Enum values use `UPPER_SNAKE_CASE`.

**Examples:**
- ✅ `RateSource`: `'PRICELIST'`, `'MANUAL_WITH_DISCOUNT'`, `'FIXED_NO_DISCOUNT'`, `'UNRESOLVED'`
- ✅ `ResolutionStatus`: `'L0'`, `'L1'`, `'L2'`
- ✅ `CostHeadCategory`: `'MATERIAL'`, `'LABOUR'`, `'OTHER'`
- ✅ `Status`: `'ACTIVE'`, `'INACTIVE'`, `'DELETED'`

**Rationale:**
- UPPER_CASE distinguishes enum values from variables
- Clear and readable
- Standard SQL enum convention

---

## Timestamp Naming

### Standard: `{action}_at`

**Rule:** Timestamp columns use pattern: `{action}_at`

**Standard Timestamps:**
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp
- `modified_at` - Record modification timestamp (first modification)
- `deleted_at` - Soft delete timestamp (if using soft deletes)

**Examples:**
- ✅ `created_at` (not `created` or `createDate`)
- ✅ `updated_at` (not `updated` or `updateDate`)
- ✅ `modified_at` (not `modified` or `modifyDate`)

**Rationale:**
- Consistent pattern across all tables
- Clear semantic meaning
- Standard Rails/Laravel convention

---

## ID Strategy

### Current: bigserial (PostgreSQL)

**Rule:** Primary keys use `BIGSERIAL` (auto-incrementing big integer).

**Examples:**
```sql
id BIGSERIAL PRIMARY KEY
```

**Rationale:**
- Simple and efficient
- Sequential IDs for easy debugging
- Standard PostgreSQL type

### Future Option: UUID

**Consideration:** UUID may be considered for future phases.

**If Adopted:**
- Use `UUID` type (PostgreSQL native)
- Generate using `gen_random_uuid()` or application layer
- Update all primary keys and foreign keys
- Migration strategy required

**Decision:** **BIGSERIAL for MVP**, UUID option reserved for future.

---

## Tenant Isolation Convention

### Standard: `tenant_id` Everywhere

**Rule:** All tables (except `tenants` itself) must have `tenant_id` column.

**Pattern:**
```sql
tenant_id BIGINT UNSIGNED NOT NULL,
FOREIGN KEY (tenant_id) REFERENCES tenants(id)
```

**Examples:**
- ✅ `products.tenant_id`
- ✅ `quotations.tenant_id`
- ✅ `quote_bom_items.tenant_id`
- ✅ `master_boms.tenant_id`

**Index:**
- Index on `tenant_id` for multi-tenant queries
- Composite indexes: `(tenant_id, other_column)` for filtered queries

**Rationale:**
- Multi-tenant data isolation
- Required for security
- Consistent across all tables

---

## Boolean Naming

### Standard: `is_{condition}` or `has_{condition}`

**Rule:** Boolean columns use `is_` or `has_` prefix.

**Examples:**
- ✅ `is_active` (not `active` or `Active`)
- ✅ `is_locked` (not `locked` or `Locked`)
- ✅ `is_price_missing` (not `priceMissing` or `PriceMissing`)
- ✅ `is_client_supplied` (not `clientSupplied` or `ClientSupplied`)
- ✅ `is_modified` (not `modified` or `Modified`)
- ✅ `has_discount` (not `discount` or `Discount`)

**Rationale:**
- Clear boolean semantic
- Self-documenting
- Consistent pattern

---

## Status Naming

### Standard: `status` or `{entity}_status`

**Rule:** Status columns use `status` (generic) or `{entity}_status` (specific).

**Examples:**
- ✅ `status` (generic: 0=Active, 1=Deleted)
- ✅ `quotation_status` (specific: DRAFT, APPROVED, FINALIZED)
- ✅ `bom_status` (specific: DRAFT, LOCKED, FINALIZED)

**Enum Values:**
- Generic: `0` (Active), `1` (Deleted) - integers
- Specific: `'DRAFT'`, `'APPROVED'`, `'FINALIZED'` - enum strings

**Rationale:**
- Flexible for different status types
- Clear semantic meaning
- Standard pattern

---

## JSON Column Naming

### Standard: `{purpose}_json` or `{purpose}_data`

**Rule:** JSON columns use `{purpose}_json` or `{purpose}_data` suffix.

**Examples:**
- ✅ `defined_spec_json` (not `definedSpec` or `DefinedSpec`)
- ✅ `metadata_json` (not `metadata` or `Metadata`)
- ✅ `attribute_data` (not `attributes` or `Attributes`)

**Rationale:**
- Clear that column contains JSON
- Distinguishes from relational data
- Self-documenting

---

## Naming Exceptions

### Legacy Compatibility

**Exception:** Some existing columns may not follow conventions (legacy).

**Handling:**
- Document exceptions in this section
- New columns must follow conventions
- Legacy columns can be renamed in future migrations

**Examples:**
- `ProductId` → Should be `product_id` (legacy, to be migrated)
- `QuotationSaleId` → Should be `quotation_sale_id` (legacy, to be migrated)

---

## Summary Table

| Element | Convention | Example |
|---------|------------|---------|
| **Table** | snake_case, plural | `quote_bom_items` |
| **Column** | snake_case, singular | `product_id` |
| **Foreign Key** | `{table_singular}_id` | `product_id` |
| **Enum Value** | UPPER_SNAKE_CASE | `'PRICELIST'` |
| **Timestamp** | `{action}_at` | `created_at` |
| **Boolean** | `is_{condition}` | `is_active` |
| **Status** | `status` or `{entity}_status` | `quotation_status` |
| **JSON** | `{purpose}_json` | `metadata_json` |
| **ID** | `id` (bigserial) | `id` |
| **Tenant** | `tenant_id` | `tenant_id` |

---

## References

- `SPEC_5_FREEZE_GATE_CHECKLIST.md` - Section 7 (Naming Conventions)
- PostgreSQL naming conventions
- Laravel/Rails naming conventions

---

## Change Log

### v1.0 (2025-01-27) - FROZEN

- Initial naming conventions for NSW schema

**Freeze Date:** 2025-01-27  
**Freeze Reason:** Frozen after Phase-5 Senate review. All Step-1 requirements verified and approved.

---

**Status:** FROZEN  
**Frozen:** 2025-01-27 after Phase-5 Senate review

