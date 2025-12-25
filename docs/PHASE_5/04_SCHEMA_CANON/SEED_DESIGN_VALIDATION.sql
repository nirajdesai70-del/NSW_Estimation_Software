-- NSW Schema Canon v1.0 - Seed Design Validation SQL
-- Purpose: Demonstrate complete data structure with sample data
-- Date: 2025-01-27
-- Status: DRAFT

-- ============================================================================
-- 1. TENANT + ADMIN + ROLES
-- ============================================================================

-- Insert tenant
INSERT INTO tenants (code, name, status) VALUES
('DEMO001', 'Demo Tenant', 'ACTIVE');

-- Get tenant ID (assuming id = 1)
-- For PostgreSQL, we'll use sequence values, but for demonstration, we'll assume IDs

-- Insert roles
INSERT INTO roles (tenant_id, name, description) VALUES
(1, 'admin', 'Administrator with full access'),
(1, 'estimator', 'Can create and edit quotations'),
(1, 'reviewer', 'Can review and approve quotations'),
(1, 'viewer', 'Read-only access');

-- Insert admin user
INSERT INTO users (tenant_id, email, name, password_hash, status) VALUES
(1, 'admin@demo.com', 'Admin User', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ACTIVE');
-- Password hash above is for 'password' (bcrypt)

-- Link admin user to admin role
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u, roles r
WHERE u.email = 'admin@demo.com' AND r.name = 'admin' AND u.tenant_id = 1;

-- ============================================================================
-- 2. CIM TAXONOMY + ATTRIBUTES MAPPING
-- ============================================================================

-- Insert category
INSERT INTO categories (tenant_id, code, name, description, is_active) VALUES
(1, 'ELEC_PANEL', 'Electrical Panel', 'Electrical panel components', true);

-- Insert subcategory
INSERT INTO subcategories (tenant_id, category_id, code, name, description, is_active) VALUES
(1, 1, 'MCB', 'Miniature Circuit Breaker', 'MCB components', true);

-- Insert product type
INSERT INTO product_types (tenant_id, category_id, code, name, description, is_active) VALUES
(1, 1, 'MCB_100A', 'MCB 100A', '100 Ampere MCB', true);

-- Insert attributes
INSERT INTO attributes (tenant_id, name, data_type, is_active) VALUES
(1, 'Voltage', 'NUMBER', true),
(1, 'Current Rating', 'NUMBER', true),
(1, 'IP Rating', 'TEXT', true),
(1, 'Breaking Capacity', 'NUMBER', true);

-- Map attributes to category
INSERT INTO category_attributes (tenant_id, category_id, attribute_id, is_required)
SELECT 1, c.id, a.id, true
FROM categories c, attributes a
WHERE c.code = 'ELEC_PANEL' AND c.tenant_id = 1
  AND a.name IN ('Voltage', 'Current Rating', 'IP Rating') AND a.tenant_id = 1;

INSERT INTO category_attributes (tenant_id, category_id, attribute_id, is_required)
SELECT 1, c.id, a.id, false
FROM categories c, attributes a
WHERE c.code = 'ELEC_PANEL' AND c.tenant_id = 1
  AND a.name = 'Breaking Capacity' AND a.tenant_id = 1;

-- Insert makes
INSERT INTO makes (tenant_id, name, is_active) VALUES
(1, 'Schneider Electric', true),
(1, 'ABB', true);

-- Insert series
INSERT INTO series (tenant_id, make_id, name, is_active) VALUES
(1, 1, 'Acti9', true),
(1, 1, 'SIVACON S8', true),
(1, 2, 'S200', true);

-- ============================================================================
-- 3. GENERIC + SPECIFIC PRODUCT WITH SKU
-- ============================================================================

-- Insert cost head (required for product default)
INSERT INTO cost_heads (tenant_id, code, name, category, priority, is_active) VALUES
(1, 'OEM_MATERIAL', 'OEM Material', 'MATERIAL', 1, true),
(1, 'LABOUR', 'Labour', 'LABOUR', 1, true);

-- Insert generic product (ProductType = 1 equivalent, no make/series)
INSERT INTO products (tenant_id, category_id, subcategory_id, product_type_id, name, description, cost_head_id, is_active) VALUES
(1, 1, 1, 1, 'MCB 100A Generic', 'Generic 100A MCB', 1, true);

-- Get generic product ID (assuming id = 1)

-- Insert specific product with SKU (links to generic)
INSERT INTO products (tenant_id, category_id, subcategory_id, product_type_id, generic_product_id, make_id, series_id, sku, name, description, cost_head_id, is_active) VALUES
(1, 1, 1, 1, 1, 1, 1, 'SCH-ACTI9-MCB-100A', 'Schneider Acti9 MCB 100A', 'Schneider Electric Acti9 series 100A MCB', 1, true);

-- Insert product attributes for specific product
INSERT INTO product_attributes (tenant_id, product_id, attribute_id, value_number)
SELECT 1, p.id, a.id, 415
FROM products p, attributes a
WHERE p.sku = 'SCH-ACTI9-MCB-100A' AND p.tenant_id = 1
  AND a.name = 'Voltage' AND a.tenant_id = 1;

INSERT INTO product_attributes (tenant_id, product_id, attribute_id, value_number)
SELECT 1, p.id, a.id, 100
FROM products p, attributes a
WHERE p.sku = 'SCH-ACTI9-MCB-100A' AND p.tenant_id = 1
  AND a.name = 'Current Rating' AND a.tenant_id = 1;

INSERT INTO product_attributes (tenant_id, product_id, attribute_id, value_text)
SELECT 1, p.id, a.id, 'IP65'
FROM products p, attributes a
WHERE p.sku = 'SCH-ACTI9-MCB-100A' AND p.tenant_id = 1
  AND a.name = 'IP Rating' AND a.tenant_id = 1;

-- ============================================================================
-- 4. PRICE LIST + EFFECTIVE PRICE
-- ============================================================================

-- Insert price list
INSERT INTO price_lists (tenant_id, code, name, effective_date, is_active) VALUES
(1, 'PL-2025-01', 'Price List Jan 2025', '2025-01-01', true);

-- Insert price for specific product
INSERT INTO prices (tenant_id, product_id, price_list_id, rate, effective_date, status)
SELECT 1, p.id, pl.id, 5000.00, '2025-01-01', 'ACTIVE'
FROM products p, price_lists pl
WHERE p.sku = 'SCH-ACTI9-MCB-100A' AND p.tenant_id = 1
  AND pl.code = 'PL-2025-01' AND pl.tenant_id = 1;

-- ============================================================================
-- 5. MASTER BOM + L0/L1 ITEMS
-- ============================================================================

-- Insert master BOM
INSERT INTO master_boms (tenant_id, name, unique_no, description, template_type, is_active) VALUES
(1, 'Standard Feeder Panel', 'MBOM-FEED-001', 'Standard feeder panel template', 'FEEDER', true);

-- Insert L0 item (generic descriptor, no product_id)
INSERT INTO master_bom_items (tenant_id, master_bom_id, resolution_status, generic_descriptor, quantity, uom, sequence_order) VALUES
(1, 1, 'L0', 'MCB 100A', 1, 'Nos', 1);

-- Insert L1 item (defined spec JSON, no product_id)
INSERT INTO master_bom_items (tenant_id, master_bom_id, resolution_status, defined_spec_json, quantity, uom, sequence_order) VALUES
(1, 1, 'L1', '{"voltage": 415, "current_rating": 100, "ip_rating": "IP65"}', 2, 'Nos', 2);

-- Note: product_id is NULL for both L0 and L1 items (G1 guardrail enforced)

-- ============================================================================
-- 6. QUOTATION + PANEL + BOM GROUP + ONE UNRESOLVED AND ONE RESOLVED ITEM
-- ============================================================================

-- Insert quotation
INSERT INTO quotations (tenant_id, quote_no, customer_name_snapshot, status, created_by)
SELECT 1, 'Q-2025-001', 'ABC Industries', 'DRAFT', u.id
FROM users u
WHERE u.email = 'admin@demo.com' AND u.tenant_id = 1;

-- Insert quote panel
INSERT INTO quote_panels (tenant_id, quotation_id, name, quantity, rate, amount, sequence_order)
SELECT 1, q.id, 'Panel 1', 1, 0, 0, 1
FROM quotations q
WHERE q.quote_no = 'Q-2025-001' AND q.tenant_id = 1;

-- Insert quote BOM (applied from master BOM)
INSERT INTO quote_boms (tenant_id, quotation_id, panel_id, level, name, quantity, rate, amount, origin_master_bom_id, origin_master_bom_version, instance_sequence_no, is_modified, sequence_order)
SELECT 1, q.id, qp.id, 0, 'Feeder 1', 1, 0, 0, mb.id, 'v1.0', 1, false, 1
FROM quotations q, quote_panels qp, master_boms mb
WHERE q.quote_no = 'Q-2025-001' AND q.tenant_id = 1
  AND qp.quotation_id = q.id
  AND mb.unique_no = 'MBOM-FEED-001' AND mb.tenant_id = 1;

-- Insert unresolved item (L0 resolution, no product_id)
INSERT INTO quote_bom_items (tenant_id, quotation_id, panel_id, bom_id, resolution_status, description, quantity, rate, discount_pct, net_rate, amount, rate_source, is_price_missing, cost_head_id, sequence_order)
SELECT 1, q.id, qp.id, qb.id, 'L0', 'MCB 100A (Unresolved)', 1, 0, 0, 0, 0, 'UNRESOLVED', true, ch.id, 1
FROM quotations q, quote_panels qp, quote_boms qb, cost_heads ch
WHERE q.quote_no = 'Q-2025-001' AND q.tenant_id = 1
  AND qp.quotation_id = q.id
  AND qb.quotation_id = q.id AND qb.panel_id = qp.id
  AND ch.code = 'OEM_MATERIAL' AND ch.tenant_id = 1;

-- Insert resolved item (L2 resolution, with product_id)
INSERT INTO quote_bom_items (tenant_id, quotation_id, panel_id, bom_id, product_id, resolution_status, description, quantity, rate, discount_pct, net_rate, amount, rate_source, is_price_missing, cost_head_id, sequence_order)
SELECT 1, q.id, qp.id, qb.id, p.id, 'L2', 'Schneider Acti9 MCB 100A', 1, 5000.00, 10.00, 4500.00, 4500.00, 'PRICELIST', false, ch.id, 2
FROM quotations q, quote_panels qp, quote_boms qb, products p, cost_heads ch
WHERE q.quote_no = 'Q-2025-001' AND q.tenant_id = 1
  AND qp.quotation_id = q.id
  AND qb.quotation_id = q.id AND qb.panel_id = qp.id
  AND p.sku = 'SCH-ACTI9-MCB-100A' AND p.tenant_id = 1
  AND ch.code = 'OEM_MATERIAL' AND ch.tenant_id = 1;

-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Verify tenant and user setup
SELECT 'Tenant Setup' as validation, COUNT(*) as count FROM tenants WHERE code = 'DEMO001';
SELECT 'Admin User' as validation, COUNT(*) as count FROM users WHERE email = 'admin@demo.com';
SELECT 'Roles' as validation, COUNT(*) as count FROM roles WHERE tenant_id = 1;

-- Verify CIM taxonomy
SELECT 'Categories' as validation, COUNT(*) as count FROM categories WHERE tenant_id = 1;
SELECT 'Products' as validation, COUNT(*) as count FROM products WHERE tenant_id = 1;
SELECT 'Generic Product' as validation, COUNT(*) as count FROM products WHERE tenant_id = 1 AND generic_product_id IS NULL;
SELECT 'Specific Product with SKU' as validation, COUNT(*) as count FROM products WHERE tenant_id = 1 AND sku IS NOT NULL;

-- Verify pricing
SELECT 'Price Lists' as validation, COUNT(*) as count FROM price_lists WHERE tenant_id = 1;
SELECT 'Prices' as validation, COUNT(*) as count FROM prices WHERE tenant_id = 1 AND status = 'ACTIVE';

-- Verify Master BOM
SELECT 'Master BOMs' as validation, COUNT(*) as count FROM master_boms WHERE tenant_id = 1;
SELECT 'Master BOM Items (L0/L1)' as validation, COUNT(*) as count FROM master_bom_items WHERE master_bom_id = 1;
SELECT 'G1 Guardrail: product_id must be NULL' as validation, COUNT(*) as count FROM master_bom_items WHERE master_bom_id = 1 AND product_id IS NULL;

-- Verify Quotation
SELECT 'Quotations' as validation, COUNT(*) as count FROM quotations WHERE tenant_id = 1;
SELECT 'Quote Panels' as validation, COUNT(*) as count FROM quote_panels;
SELECT 'Quote BOMs' as validation, COUNT(*) as count FROM quote_boms;
SELECT 'Quote BOM Items (Unresolved)' as validation, COUNT(*) as count FROM quote_bom_items WHERE resolution_status IN ('L0', 'L1') AND product_id IS NULL;
SELECT 'Quote BOM Items (Resolved)' as validation, COUNT(*) as count FROM quote_bom_items WHERE resolution_status = 'L2' AND product_id IS NOT NULL;

-- Verify Step-2 design decisions
SELECT 'Multi-SKU: parent_line_id exists' as validation, COUNT(*) as count FROM quote_bom_items WHERE parent_line_id IS NOT NULL;
SELECT 'Customer: customer_name_snapshot exists' as validation, COUNT(*) as count FROM quotations WHERE customer_name_snapshot IS NOT NULL;
SELECT 'Resolution: L0/L1/L2 support' as validation, COUNT(DISTINCT resolution_status) as distinct_levels FROM quote_bom_items;

