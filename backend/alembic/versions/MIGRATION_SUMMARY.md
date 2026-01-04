# Phase-5 Schema Canon v1.0 Migration Summary

**Date:** 2026-01-04  
**Status:** ✅ MIGRATIONS CREATED  
**Source:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`

---

## Migration Files Created

### 1. `20260104_110309_create_schema_canon_v1_0_auth_cim.py`
**Revises:** `6fbca98f32b1`  
**Modules:** AUTH, CIM (partial)

**Tables Created:**
- AUTH: `tenants`, `users`, `roles`, `user_roles`, `permissions`, `role_permissions`
- CIM: `categories`, `subcategories`, `product_types`, `attributes`, `category_attributes`, `makes`, `series`

---

### 2. `20260104_110400_create_schema_canon_v1_0_l1_l2_quo_pricing.py`
**Revises:** `20260104_110309`  
**Modules:** CIM (products), L1/L2, SHARED, CUSTOMER, MBOM, QUO, PRICING

**Tables Created:**
- CIM: `products`, `product_attributes`
- L1/L2: `l1_line_groups`, `l1_intent_lines`, `l1_attributes`, `l1_l2_mappings`
- SHARED: `cost_heads`
- CUSTOMER: `customers`
- MBOM: `master_boms`, `master_bom_items`
- QUO: `quotations`, `quote_panels`, `quote_boms`, `quote_bom_items`, `quote_bom_item_history`
- PRICING: `prices`, `import_batches`, `import_approval_queue`

**Tables Updated:**
- `catalog_skus` - Updated to match Schema Canon (removed old columns, added new ones)
- `price_lists` - Updated to match Schema Canon (added tenant_id, code, effective_date)
- `sku_prices` - Updated to match Schema Canon (added tenant_id, catalog_sku_id, pricelist_ref, rate, currency, region, effective_from, effective_to)

---

### 3. `20260104_110500_add_audit_ai_sc_jsonb_accessory_compat.py`
**Revises:** `20260104_110400`  
**Modules:** AUDIT, AI, Storage Decisions

**Tables Created:**
- AUDIT: `audit_logs`, `bom_change_logs`
- AI: `ai_call_logs`

**Additions:**
- `catalog_skus.sc_struct_jsonb` - JSONB column with GIN index (Decision D-SCL-01)
- `accessory_compatibility` - Reference table (Decision D-ACC-01)

---

## Migration Order

1. ✅ `f43171814116_create_catalog_tables.py` (existing)
2. ✅ `6fbca98f32b1_catalog_current_price_skuprice_audit_make_.py` (existing)
3. ✅ `20260104_110309_create_schema_canon_v1_0_auth_cim.py` (new)
4. ✅ `20260104_110400_create_schema_canon_v1_0_l1_l2_quo_pricing.py` (new)
5. ✅ `20260104_110500_add_audit_ai_sc_jsonb_accessory_compat.py` (new)

---

## Key Features

### ✅ Complete Schema Canon Coverage
- All AUTH module tables
- All CIM module tables
- All L1/L2 module tables
- All QUO module tables
- All PRICING module tables
- All MBOM module tables
- All AUDIT module tables
- All AI module tables (schema reservation)
- All SHARED module tables
- All CUSTOMER module tables

### ✅ Storage Decisions Implemented
- **D-SCL-01:** `catalog_skus.sc_struct_jsonb` JSONB column with GIN index
- **D-ACC-01:** `accessory_compatibility` reference table

### ✅ Constraints and Guardrails
- All CHECK constraints from Schema Canon
- All foreign key constraints
- All unique constraints
- All indexes

### ✅ Backward Compatibility
- Existing `catalog_skus` table updated (not dropped)
- Existing `price_lists` table updated (not dropped)
- Existing `sku_prices` table updated (not dropped)
- Data migration logic included for existing data

---

## Testing Requirements

### Upgrade Test
```bash
cd backend
alembic upgrade head
```

**Verify:**
- All tables created
- All indexes created
- All constraints created
- `catalog_skus.sc_struct_jsonb` column exists with GIN index
- `accessory_compatibility` table exists

### Downgrade Test
```bash
cd backend
alembic downgrade -1
alembic downgrade -1
alembic downgrade -1
```

**Verify:**
- All tables dropped in reverse order
- No orphaned constraints or indexes

### Smoke Queries
```sql
-- Test SC_Lx JSONB
SELECT id, sc_struct_jsonb FROM catalog_skus LIMIT 1;

-- Test JSONB query
SELECT * FROM catalog_skus WHERE sc_struct_jsonb->>'l1' = 'FRAME-1';

-- Test accessory_compatibility
SELECT * FROM accessory_compatibility LIMIT 1;

-- Test all module tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'tenants', 'users', 'categories', 'catalog_skus', 
    'l1_intent_lines', 'quotations', 'sku_prices', 
    'audit_logs', 'accessory_compatibility'
);
```

---

## DDL Summary

### Total Tables: 35+
- AUTH: 6 tables
- CIM: 9 tables
- L1/L2: 5 tables
- SHARED: 1 table
- CUSTOMER: 1 table
- MBOM: 2 tables
- QUO: 5 tables
- PRICING: 5 tables
- AUDIT: 2 tables
- AI: 1 table
- **Plus:** `accessory_compatibility` (reference table)

### Total Indexes: 100+
- All indexes from Schema Canon
- GIN index on `sc_struct_jsonb`
- Composite indexes for lookups
- Partial indexes for filtered queries

### Total Constraints: 50+
- Primary keys
- Foreign keys
- Unique constraints
- CHECK constraints (guardrails)

---

## Next Steps

1. **Review migrations** - Verify against Schema Canon
2. **Run upgrade test** - `alembic upgrade head`
3. **Run downgrade test** - `alembic downgrade -1` (repeat)
4. **Run smoke queries** - Verify tables and indexes
5. **Update models** - Update SQLAlchemy models to match
6. **Begin importer** - Start building generic importer

---

**Status:** ✅ MIGRATIONS READY FOR REVIEW  
**Next Action:** Review and test migrations

