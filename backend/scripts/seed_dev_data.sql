-- Minimal seed data for /bom/explode happy-path testing
-- Run with: psql -h 127.0.0.1 -p 5433 -U postgres -d nsw_dev -f backend/scripts/seed_dev_data.sql
-- Or: cat backend/scripts/seed_dev_data.sql | docker exec -i nsw_pg psql -U postgres -d nsw_dev

-- 1) Tenant (id=1)
INSERT INTO tenants (id, code, name, status, created_at, updated_at)
VALUES (1, 'DEV', 'DEV Tenant', 'ACTIVE', now(), now())
ON CONFLICT (id) DO NOTHING;

-- 2) Category (id=1)
INSERT INTO categories (id, tenant_id, name, code, description, is_active, created_at, updated_at)
VALUES (1, 1, 'DEV Category', 'DEV_CAT', 'Development category for testing', true, now(), now())
ON CONFLICT (id) DO NOTHING;

-- 3) Product Type (id=1) - requires category_id
INSERT INTO product_types (id, tenant_id, category_id, name, code, description, is_active, created_at, updated_at)
VALUES (1, 1, 1, 'DEV ProductType', 'DEV_PT', 'Development product type for testing', true, now(), now())
ON CONFLICT (id) DO NOTHING;

-- 4) Catalog SKU (id=501) - note: uses oem_catalog_no, not sku_code
INSERT INTO catalog_skus (
  id, tenant_id, make, oem_catalog_no, uom, is_active,
  created_at, updated_at
)
VALUES (
  501, 1, 'DEV-MAKE', 'DEV-SKU-001', 'EA', true,
  now(), now()
)
ON CONFLICT (id) DO NOTHING;

-- 5) L1 Intent Line (id=1001) - BASE type
INSERT INTO l1_intent_lines (
  id, tenant_id, category_id, product_type_id, line_type,
  description, is_active, created_at, updated_at
)
VALUES (
  1001, 1, 1, 1, 'BASE',
  'DEV L1 base line for testing', true, now(), now()
)
ON CONFLICT (id) DO NOTHING;

-- 6) L1 -> L2 mapping (G-08)
INSERT INTO l1_l2_mappings (
  id, tenant_id, l1_intent_line_id, catalog_sku_id,
  mapping_type, is_primary, created_at, updated_at
)
VALUES (
  9001, 1, 1001, 501,
  'BASE', true, now(), now()
)
ON CONFLICT (id) DO NOTHING;

-- Verify seed data
SELECT 'tenants' as table_name, count(*) as count from tenants where id=1
UNION ALL SELECT 'categories', count(*) from categories where id=1
UNION ALL SELECT 'product_types', count(*) from product_types where id=1
UNION ALL SELECT 'catalog_skus', count(*) from catalog_skus where id=501
UNION ALL SELECT 'l1_intent_lines', count(*) from l1_intent_lines where id=1001
UNION ALL SELECT 'l1_l2_mappings', count(*) from l1_l2_mappings where id=9001;

