-- NSW Schema Canon v1.0 - DDL (Blueprint-driven)
-- Generated: 2026-01-05 20:39:54
-- Blueprint: CATEGORY_C_STEP1_BLUEPRINT.md
-- Inventory: NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- AUTH.tenants
-- Purpose: Multi-tenant isolation root
-- Notes: Root tenant table; all other tenant_id FKs point here
CREATE TABLE tenants (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- AI.ai_call_logs
-- Purpose: AI advisory call log (reserved)
-- Notes: Reservation only in Phase-5; AI is advisory-only and must not mutate money fields
CREATE TABLE ai_call_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    actor_user_id BIGINT,
    context VARCHAR(120),
    request_json JSONB NOT NULL,
    response_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- AUDIT.audit_logs
-- Purpose: Append-only audit trail
-- Notes: entity_id); INDEX(created_at)"
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    actor_user_id BIGINT,
    entity_table VARCHAR(120) NOT NULL,
    entity_id BIGINT NOT NULL,
    action VARCHAR(60) NOT NULL,
    payload_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.catalog_skus
-- Purpose: L2 commercial SKU identity (SKU-pure)
-- Notes: make
CREATE TABLE catalog_skus (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    make VARCHAR(120) NOT NULL,
    oem_catalog_no VARCHAR(120) NOT NULL,
    oem_series_range VARCHAR(120),
    series_bucket VARCHAR(50),
    item_producttype VARCHAR(120),
    business_subcategory VARCHAR(120),
    uom VARCHAR(20) NOT NULL DEFAULT 'EA',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.categories
-- Purpose: Top-level taxonomy category
-- Notes: code)"
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(80) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.attributes
-- Purpose: Attribute schema per category
-- Notes: category_id
CREATE TABLE attributes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    attribute_code VARCHAR(80) NOT NULL,
    name VARCHAR(200) NOT NULL,
    data_type VARCHAR(30) NOT NULL,
    unit VARCHAR(30),
    is_required BOOLEAN NOT NULL DEFAULT false,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.attribute_options
-- Purpose: Allowed values for attributes
-- Notes: Option values can be text or numeric; display_label required
CREATE TABLE attribute_options (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    attribute_id BIGINT NOT NULL,
    value_text VARCHAR(200),
    value_number NUMERIC(18,6),
    display_label VARCHAR(200) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- SHARED.cost_heads
-- Purpose: Cost bucket master
-- Notes: Classification only; precedence: item override → product default → tenant/system default
CREATE TABLE cost_heads (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(80) NOT NULL,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(30) NOT NULL,
    priority INTEGER,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- SHARED.customers
-- Purpose: Customer master reference
-- Notes: Quotation uses customer_name snapshot; customer_id is non-authoritative reference
CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    customer_code VARCHAR(80),
    name VARCHAR(255) NOT NULL,
    legal_name VARCHAR(255),
    gstin VARCHAR(30),
    address_text TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- QUO.discount_rules
-- Purpose: Discount rules (quotation-scoped policy / JSON)
-- Notes: Schema placeholder: rule_json stores logic; enforcement in QUO compute/resolver
CREATE TABLE discount_rules (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    rule_json JSONB,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.l1_line_groups
-- Purpose: Group container for related L1 lines
-- Notes: group_name)"
CREATE TABLE l1_line_groups (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    group_name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.makes
-- Purpose: Make master (optional/reserved)
-- Notes: code)"
CREATE TABLE makes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(80) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- MBOM.master_boms
-- Purpose: Master BOM template header (source-of-truth)
-- Notes: unique_no)"
CREATE TABLE master_boms (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    unique_no VARCHAR(80) NOT NULL,
    description TEXT,
    template_type VARCHAR(30) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- MBOM.master_bom_items
-- Purpose: Master BOM template line (L0/L1 only)
-- Notes: G-01: product_id must be NULL; do NOT FK product_id; defined_spec_json JSONB optional
CREATE TABLE master_bom_items (
    id BIGSERIAL PRIMARY KEY,
    master_bom_id BIGINT NOT NULL,
    resolution_status VARCHAR(10) NOT NULL,
    generic_descriptor TEXT,
    defined_spec_json JSONB,
    product_id BIGINT,
    quantity NUMERIC(18,6) NOT NULL DEFAULT 1,
    uom VARCHAR(20) NOT NULL DEFAULT 'EA',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- PRICING.price_lists
-- Purpose: Price list header
-- Notes: name)"
CREATE TABLE price_lists (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    vendor VARCHAR(120),
    published_at DATE,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    region VARCHAR(30) NOT NULL DEFAULT 'INDIA',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- SHARED.projects
-- Purpose: Project master (optional/reserved)
-- Notes: code)"
CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(80) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- AUTH.roles
-- Purpose: RBAC roles
-- Notes: name)"
CREATE TABLE roles (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(80) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.series
-- Purpose: Series master (optional/reserved)
-- Notes: code); INDEX(make_id)"
CREATE TABLE series (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    make_id BIGINT,
    code VARCHAR(80) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.subcategories
-- Purpose: Second-level taxonomy under category
-- Notes: category_id
CREATE TABLE subcategories (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(80) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.product_types
-- Purpose: Device identity anchor (Type/ProductType)
-- Notes: Nullable subcategory_id requires partial uniques (Phase-5 friendly)
CREATE TABLE product_types (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    subcategory_id BIGINT,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(80) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.l1_intent_lines
-- Purpose: L1 engineering interpretation line
-- Notes: Engineering-only; no SKU/price; series_bucket optional text
CREATE TABLE l1_intent_lines (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    subcategory_id BIGINT,
    product_type_id BIGINT NOT NULL,
    make_id BIGINT,
    series_id BIGINT,
    series_bucket VARCHAR(50),
    line_type VARCHAR(20) NOT NULL,
    line_group_id BIGINT,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.l1_attributes
-- Purpose: L1 KVU attributes per intent line
-- Notes: KVU carrier: attribute_code + (value_text/value_number) + optional unit
CREATE TABLE l1_attributes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    l1_intent_line_id BIGINT NOT NULL,
    attribute_code VARCHAR(80) NOT NULL,
    value_text VARCHAR(200),
    value_number NUMERIC(18,6),
    value_unit VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.l1_l2_mappings
-- Purpose: L1→L2 mapping bridge
-- Notes: G-08: DO NOT add unique on catalog_sku_id; many L1 lines can map to same SKU
CREATE TABLE l1_l2_mappings (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    l1_intent_line_id BIGINT NOT NULL,
    catalog_sku_id BIGINT NOT NULL,
    mapping_type VARCHAR(30) NOT NULL,
    is_primary BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- CIM.products
-- Purpose: Legacy/transitional product identity for QUO binding
-- Notes: LEGACY/TRANSITIONAL: commercial binding in QUO during Phase-5; pricing truth migrates to L2 SKUs
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    subcategory_id BIGINT,
    product_type_id BIGINT,
    make_id BIGINT,
    series_id BIGINT,
    sku VARCHAR(120),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cost_head_id BIGINT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- PRICING.prices
-- Purpose: Legacy product pricing timeline (transitional)
-- Notes: product_id
CREATE TABLE prices (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    price_list_id BIGINT,
    rate NUMERIC(18,2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    effective_from DATE NOT NULL,
    effective_to DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- TAX.tax_profiles
-- Purpose: GST tax profile master
-- Notes: name)"
CREATE TABLE tax_profiles (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    cgst_pct NUMERIC(6,2),
    sgst_pct NUMERIC(6,2),
    igst_pct NUMERIC(6,2),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- AUTH.users
-- Purpose: User accounts/authentication
-- Notes: email)"
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(200) NOT NULL,
    password_hash TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- PRICING.import_batches
-- Purpose: Import lineage header
-- Notes: Links to source_file and imported_at; supports sku_prices lineage
CREATE TABLE import_batches (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    source_file VARCHAR(255),
    imported_by BIGINT,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- QUO.quotations
-- Purpose: Quotation workspace root
-- Notes: Snapshot totals written on Apply-Recalc only; status DRAFT/APPROVED/FINALIZED
CREATE TABLE quotations (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quote_no VARCHAR(80) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_id BIGINT,
    project_id BIGINT,
    status VARCHAR(30) NOT NULL DEFAULT 'DRAFT',
    discount_pct NUMERIC(6,2) NOT NULL DEFAULT 0,
    tax_profile_id BIGINT,
    tax_mode VARCHAR(20),
    taxable_base NUMERIC(18,2),
    cgst_pct_snapshot NUMERIC(6,2),
    sgst_pct_snapshot NUMERIC(6,2),
    igst_pct_snapshot NUMERIC(6,2),
    cgst_amount NUMERIC(18,2),
    sgst_amount NUMERIC(18,2),
    igst_amount NUMERIC(18,2),
    tax_amount_total NUMERIC(18,2),
    grand_total NUMERIC(18,2),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- QUO.quote_panels
-- Purpose: Panel container under quotation
-- Notes: Panel totals computed; optional UNIQUE(quotation_id,name) later
CREATE TABLE quote_panels (
    id BIGSERIAL PRIMARY KEY,
    quotation_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    quantity NUMERIC(18,6) NOT NULL DEFAULT 1,
    rate NUMERIC(18,2),
    amount NUMERIC(18,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- QUO.quote_boms
-- Purpose: BOM/Feeder container under panel (hierarchical)
-- Notes: Feeder is level=0; origin_master_bom_id is reference-only (NO FK)
CREATE TABLE quote_boms (
    id BIGSERIAL PRIMARY KEY,
    quotation_id BIGINT NOT NULL,
    panel_id BIGINT NOT NULL,
    parent_bom_id BIGINT,
    level INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    quantity NUMERIC(18,6) NOT NULL DEFAULT 1,
    rate NUMERIC(18,2),
    amount NUMERIC(18,2),
    origin_master_bom_id BIGINT,
    origin_master_bom_version VARCHAR(30),
    instance_sequence_no INTEGER,
    is_modified BOOLEAN NOT NULL DEFAULT false,
    modified_by BIGINT,
    modified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- QUO.quote_bom_items
-- Purpose: Leaf line item with pricing + resolution
-- Notes: Monetary fields normalized by compute rules (G-03/G-05); override_rate requires reason + attribution
CREATE TABLE quote_bom_items (
    id BIGSERIAL PRIMARY KEY,
    quotation_id BIGINT NOT NULL,
    panel_id BIGINT NOT NULL,
    bom_id BIGINT NOT NULL,
    parent_line_id BIGINT,
    product_id BIGINT,
    make_id BIGINT,
    series_id BIGINT,
    category_id BIGINT,
    quantity NUMERIC(18,6) NOT NULL DEFAULT 1,
    rate NUMERIC(18,2) NOT NULL DEFAULT 0,
    discount_pct NUMERIC(6,2) NOT NULL DEFAULT 0,
    discount_source VARCHAR(30),
    net_rate NUMERIC(18,2) NOT NULL DEFAULT 0,
    amount NUMERIC(18,2) NOT NULL DEFAULT 0,
    rate_source VARCHAR(30) NOT NULL DEFAULT 'UNRESOLVED',
    is_price_missing BOOLEAN NOT NULL DEFAULT false,
    is_client_supplied BOOLEAN NOT NULL DEFAULT false,
    is_locked BOOLEAN NOT NULL DEFAULT false,
    cost_head_id BIGINT,
    resolution_status VARCHAR(10) NOT NULL DEFAULT 'L0',
    description TEXT,
    metadata_json JSONB,
    sequence_order INTEGER NOT NULL DEFAULT 0,
    override_rate NUMERIC(18,2),
    override_reason TEXT,
    overridden_by BIGINT,
    overridden_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- PRICING.sku_prices
-- Purpose: L2 SKU price timeline (append-only)
-- Notes: catalog_sku_id
CREATE TABLE sku_prices (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    catalog_sku_id BIGINT NOT NULL,
    price_list_id BIGINT,
    pricelist_ref VARCHAR(120),
    rate NUMERIC(18,2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    region VARCHAR(30) NOT NULL DEFAULT 'INDIA',
    effective_from DATE NOT NULL,
    effective_to DATE,
    import_batch_id BIGINT,
    source_file VARCHAR(255),
    source_row INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- AUTH.user_roles
-- Purpose: User↔Role assignment junction
-- Notes: Surrogate PK + composite unique; ON DELETE CASCADE from users; RESTRICT from roles
CREATE TABLE user_roles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Constraints / Indexes

ALTER TABLE tenants ADD CONSTRAINT uq_tenants_1 UNIQUE (code);
CREATE INDEX ix_tenants_7733510 ON tenants (code);
CREATE INDEX ix_tenants_5211746 ON tenants (name);
ALTER TABLE ai_call_logs ADD CONSTRAINT fk_ai_call_logs_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
CREATE INDEX idx_ai_call_logs_tenant_id ON ai_call_logs (tenant_id);
CREATE INDEX ix_ai_call_logs_3660124 ON ai_call_logs (created_at);
ALTER TABLE audit_logs ADD CONSTRAINT fk_audit_logs_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
CREATE INDEX idx_audit_logs_tenant_id ON audit_logs (tenant_id);
ALTER TABLE catalog_skus ADD CONSTRAINT fk_catalog_skus_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE catalog_skus ADD CONSTRAINT uq_catalog_skus_1 UNIQUE (tenant_id,make,oem_catalog_no);
CREATE INDEX idx_catalog_skus_tenant_id ON catalog_skus (tenant_id);
ALTER TABLE categories ADD CONSTRAINT fk_categories_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE categories ADD CONSTRAINT uq_categories_1 UNIQUE (tenant_id,code);
CREATE INDEX idx_categories_tenant_id ON categories (tenant_id);
ALTER TABLE attributes ADD CONSTRAINT fk_attributes_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE attributes ADD CONSTRAINT fk_attributes_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT;
ALTER TABLE attributes ADD CONSTRAINT uq_attributes_1 UNIQUE (tenant_id,category_id,attribute_code);
CREATE INDEX idx_attributes_tenant_id ON attributes (tenant_id);
CREATE INDEX ix_attributes_8866781 ON attributes (category_id);
ALTER TABLE attribute_options ADD CONSTRAINT fk_attribute_options_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE attribute_options ADD CONSTRAINT fk_attribute_options_attribute_id FOREIGN KEY (attribute_id) REFERENCES attributes(id) ON DELETE RESTRICT;
ALTER TABLE attribute_options ADD CONSTRAINT ck_attribute_options__check_1_1 CHECK (value_text IS NOT NULL OR value_number IS NOT NULL);
CREATE INDEX idx_attribute_options_tenant_id ON attribute_options (tenant_id);
CREATE INDEX ix_attribute_options_9596317 ON attribute_options (attribute_id);
ALTER TABLE cost_heads ADD CONSTRAINT fk_cost_heads_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE cost_heads ADD CONSTRAINT uq_cost_heads_1 UNIQUE (tenant_id,code);
ALTER TABLE cost_heads ADD CONSTRAINT ck_cost_heads__category_in_material_1 CHECK (category IN ('MATERIAL','LABOUR','OTHER'));
CREATE INDEX idx_cost_heads_tenant_id ON cost_heads (tenant_id);
CREATE INDEX ix_cost_heads_5160345 ON cost_heads (tenant_id,code);
ALTER TABLE customers ADD CONSTRAINT fk_customers_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
CREATE UNIQUE INDEX ux_customers_1 ON customers (tenant_id,customer_code) WHERE customer_code IS NOT NULL;
CREATE INDEX idx_customers_tenant_id ON customers (tenant_id);
CREATE INDEX ix_customers_5211746 ON customers (name);
CREATE INDEX ix_customers_6178489 ON customers (customer_code);
ALTER TABLE discount_rules ADD CONSTRAINT fk_discount_rules_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
CREATE INDEX idx_discount_rules_tenant_id ON discount_rules (tenant_id);
CREATE INDEX ix_discount_rules_3964938 ON discount_rules (is_active);
ALTER TABLE l1_line_groups ADD CONSTRAINT fk_l1_line_groups_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE l1_line_groups ADD CONSTRAINT uq_l1_line_groups_1 UNIQUE (tenant_id,group_name);
CREATE INDEX idx_l1_line_groups_tenant_id ON l1_line_groups (tenant_id);
ALTER TABLE makes ADD CONSTRAINT fk_makes_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE makes ADD CONSTRAINT uq_makes_1 UNIQUE (tenant_id,code);
CREATE INDEX idx_makes_tenant_id ON makes (tenant_id);
ALTER TABLE master_boms ADD CONSTRAINT fk_master_boms_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE master_boms ADD CONSTRAINT uq_master_boms_1 UNIQUE (tenant_id,unique_no);
CREATE INDEX idx_master_boms_tenant_id ON master_boms (tenant_id);
ALTER TABLE master_bom_items ADD CONSTRAINT fk_master_bom_items_master_bom_id FOREIGN KEY (master_bom_id) REFERENCES master_boms(id) ON DELETE CASCADE;
ALTER TABLE master_bom_items ADD CONSTRAINT ck_master_bom_items__g01_product_id_null_1 CHECK (product_id IS NULL);
ALTER TABLE master_bom_items ADD CONSTRAINT ck_master_bom_items__resolution_status_in_l0_2 CHECK (resolution_status IN ('L0','L1'));
CREATE INDEX ix_master_bom_items_3811610 ON master_bom_items (master_bom_id);
ALTER TABLE price_lists ADD CONSTRAINT fk_price_lists_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE price_lists ADD CONSTRAINT uq_price_lists_1 UNIQUE (tenant_id,name);
CREATE INDEX idx_price_lists_tenant_id ON price_lists (tenant_id);
ALTER TABLE projects ADD CONSTRAINT fk_projects_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE projects ADD CONSTRAINT uq_projects_1 UNIQUE (tenant_id,code);
CREATE INDEX idx_projects_tenant_id ON projects (tenant_id);
ALTER TABLE roles ADD CONSTRAINT fk_roles_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE roles ADD CONSTRAINT uq_roles_1 UNIQUE (tenant_id,name);
CREATE INDEX idx_roles_tenant_id ON roles (tenant_id);
ALTER TABLE series ADD CONSTRAINT fk_series_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE series ADD CONSTRAINT fk_series_make_id FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL;
ALTER TABLE series ADD CONSTRAINT uq_series_1 UNIQUE (tenant_id,code);
CREATE INDEX idx_series_tenant_id ON series (tenant_id);
ALTER TABLE subcategories ADD CONSTRAINT fk_subcategories_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE subcategories ADD CONSTRAINT fk_subcategories_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT;
ALTER TABLE subcategories ADD CONSTRAINT uq_subcategories_1 UNIQUE (tenant_id,category_id,code);
CREATE INDEX idx_subcategories_tenant_id ON subcategories (tenant_id);
CREATE INDEX ix_subcategories_8866781 ON subcategories (category_id);
ALTER TABLE product_types ADD CONSTRAINT fk_product_types_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE product_types ADD CONSTRAINT fk_product_types_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT;
ALTER TABLE product_types ADD CONSTRAINT fk_product_types_subcategory_id FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL;
CREATE UNIQUE INDEX ux_product_types_1 ON product_types (tenant_id,category_id,code) WHERE subcategory_id IS NULL;
CREATE UNIQUE INDEX ux_product_types_2 ON product_types (tenant_id,subcategory_id,code) WHERE subcategory_id IS NOT NULL;
CREATE INDEX idx_product_types_tenant_id ON product_types (tenant_id);
CREATE INDEX ix_product_types_8866781 ON product_types (category_id);
CREATE INDEX ix_product_types_9216437 ON product_types (subcategory_id);
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT;
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_subcategory_id FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL;
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_product_type_id FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE RESTRICT;
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_line_group_id FOREIGN KEY (line_group_id) REFERENCES l1_line_groups(id) ON DELETE SET NULL;
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_make_id FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL;
ALTER TABLE l1_intent_lines ADD CONSTRAINT fk_l1_intent_lines_series_id FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL;
ALTER TABLE l1_intent_lines ADD CONSTRAINT ck_l1_intent_lines__line_type_in_base_1 CHECK (line_type IN ('BASE','FEATURE'));
CREATE INDEX idx_l1_intent_lines_tenant_id ON l1_intent_lines (tenant_id);
CREATE INDEX ix_l1_intent_lines_8866781 ON l1_intent_lines (category_id);
CREATE INDEX ix_l1_intent_lines_6282744 ON l1_intent_lines (product_type_id);
CREATE INDEX ix_l1_intent_lines_496622 ON l1_intent_lines (line_group_id);
ALTER TABLE l1_attributes ADD CONSTRAINT fk_l1_attributes_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE l1_attributes ADD CONSTRAINT fk_l1_attributes_l1_intent_line_id FOREIGN KEY (l1_intent_line_id) REFERENCES l1_intent_lines(id) ON DELETE CASCADE;
ALTER TABLE l1_attributes ADD CONSTRAINT ck_l1_attributes__check_1_1 CHECK (value_text IS NOT NULL OR value_number IS NOT NULL);
ALTER TABLE l1_attributes ADD CONSTRAINT ck_l1_attributes__check_2_2 CHECK (value_number IS NULL OR value_unit IS NOT NULL);
CREATE INDEX idx_l1_attributes_tenant_id ON l1_attributes (tenant_id);
CREATE INDEX ix_l1_attributes_8018998 ON l1_attributes (l1_intent_line_id);
ALTER TABLE l1_l2_mappings ADD CONSTRAINT fk_l1_l2_mappings_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE l1_l2_mappings ADD CONSTRAINT fk_l1_l2_mappings_l1_intent_line_id FOREIGN KEY (l1_intent_line_id) REFERENCES l1_intent_lines(id) ON DELETE CASCADE;
ALTER TABLE l1_l2_mappings ADD CONSTRAINT fk_l1_l2_mappings_catalog_sku_id FOREIGN KEY (catalog_sku_id) REFERENCES catalog_skus(id) ON DELETE RESTRICT;
ALTER TABLE l1_l2_mappings ADD CONSTRAINT ck_l1_l2_mappings__mapping_type_in_base_1 CHECK (mapping_type IN ('BASE','FEATURE_ADDON','FEATURE_INCLUDED','FEATURE_BUNDLED'));
CREATE INDEX idx_l1_l2_mappings_tenant_id ON l1_l2_mappings (tenant_id);
CREATE INDEX ix_l1_l2_mappings_8018998 ON l1_l2_mappings (l1_intent_line_id);
CREATE INDEX ix_l1_l2_mappings_4277999 ON l1_l2_mappings (catalog_sku_id);
ALTER TABLE products ADD CONSTRAINT fk_products_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE products ADD CONSTRAINT fk_products_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT;
ALTER TABLE products ADD CONSTRAINT fk_products_subcategory_id FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL;
ALTER TABLE products ADD CONSTRAINT fk_products_product_type_id FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE SET NULL;
ALTER TABLE products ADD CONSTRAINT fk_products_cost_head_id FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id) ON DELETE SET NULL;
ALTER TABLE products ADD CONSTRAINT fk_products_make_id FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL;
ALTER TABLE products ADD CONSTRAINT fk_products_series_id FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL;
CREATE INDEX idx_products_tenant_id ON products (tenant_id);
CREATE INDEX ix_products_8866781 ON products (category_id);
CREATE INDEX ix_products_9216437 ON products (subcategory_id);
CREATE INDEX ix_products_6282744 ON products (product_type_id);
CREATE INDEX ix_products_3451423 ON products (cost_head_id);
ALTER TABLE prices ADD CONSTRAINT fk_prices_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE prices ADD CONSTRAINT fk_prices_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT;
ALTER TABLE prices ADD CONSTRAINT fk_prices_price_list_id FOREIGN KEY (price_list_id) REFERENCES price_lists(id) ON DELETE SET NULL;
CREATE INDEX idx_prices_tenant_id ON prices (tenant_id);
CREATE INDEX ix_prices_1297945 ON prices (product_id);
ALTER TABLE tax_profiles ADD CONSTRAINT fk_tax_profiles_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE tax_profiles ADD CONSTRAINT uq_tax_profiles_1 UNIQUE (tenant_id,name);
CREATE INDEX idx_tax_profiles_tenant_id ON tax_profiles (tenant_id);
ALTER TABLE users ADD CONSTRAINT fk_users_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE users ADD CONSTRAINT uq_users_1 UNIQUE (tenant_id,email);
CREATE INDEX idx_users_tenant_id ON users (tenant_id);
ALTER TABLE import_batches ADD CONSTRAINT fk_import_batches_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE import_batches ADD CONSTRAINT fk_import_batches_imported_by FOREIGN KEY (imported_by) REFERENCES users(id) ON DELETE SET NULL;
CREATE INDEX idx_import_batches_tenant_id ON import_batches (tenant_id);
CREATE INDEX ix_import_batches_9261862 ON import_batches (imported_at);
ALTER TABLE quotations ADD CONSTRAINT fk_quotations_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE quotations ADD CONSTRAINT fk_quotations_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL;
ALTER TABLE quotations ADD CONSTRAINT fk_quotations_project_id FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL;
ALTER TABLE quotations ADD CONSTRAINT fk_quotations_tax_profile_id FOREIGN KEY (tax_profile_id) REFERENCES tax_profiles(id) ON DELETE SET NULL;
ALTER TABLE quotations ADD CONSTRAINT fk_quotations_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;
ALTER TABLE quotations ADD CONSTRAINT uq_quotations_1 UNIQUE (tenant_id,quote_no);
ALTER TABLE quotations ADD CONSTRAINT ck_quotations__g07_discount_range_1 CHECK (discount_pct BETWEEN 0 AND 100);
ALTER TABLE quotations ADD CONSTRAINT ck_quotations__tax_mode_in_cgst_sgst_2 CHECK (tax_mode IS NULL OR tax_mode IN ('CGST_SGST','IGST'));
CREATE INDEX idx_quotations_tenant_id ON quotations (tenant_id);
CREATE INDEX ix_quotations_6677035 ON quotations (tenant_id,quote_no);
CREATE INDEX ix_quotations_8757321 ON quotations (created_by);
CREATE INDEX ix_quotations_4779167 ON quotations (customer_id);
CREATE INDEX ix_quotations_8099790 ON quotations (project_id);
ALTER TABLE quote_panels ADD CONSTRAINT fk_quote_panels_quotation_id FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE;
CREATE INDEX ix_quote_panels_9678619 ON quote_panels (quotation_id);
ALTER TABLE quote_boms ADD CONSTRAINT fk_quote_boms_quotation_id FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE;
ALTER TABLE quote_boms ADD CONSTRAINT fk_quote_boms_panel_id FOREIGN KEY (panel_id) REFERENCES quote_panels(id) ON DELETE CASCADE;
ALTER TABLE quote_boms ADD CONSTRAINT fk_quote_boms_parent_bom_id FOREIGN KEY (parent_bom_id) REFERENCES quote_boms(id) ON DELETE CASCADE;
ALTER TABLE quote_boms ADD CONSTRAINT ck_quote_boms__level_in_0_1 CHECK (level IN (0,1,2));
CREATE INDEX ix_quote_boms_9678619 ON quote_boms (quotation_id);
CREATE INDEX ix_quote_boms_3823478 ON quote_boms (panel_id);
CREATE INDEX ix_quote_boms_800653 ON quote_boms (parent_bom_id);
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_quotation_id FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_panel_id FOREIGN KEY (panel_id) REFERENCES quote_panels(id) ON DELETE CASCADE;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_bom_id FOREIGN KEY (bom_id) REFERENCES quote_boms(id) ON DELETE CASCADE;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_parent_line_id FOREIGN KEY (parent_line_id) REFERENCES quote_bom_items(id) ON DELETE SET NULL;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_cost_head_id FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id) ON DELETE SET NULL;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_overridden_by FOREIGN KEY (overridden_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_make_id FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL;
ALTER TABLE quote_bom_items ADD CONSTRAINT fk_quote_bom_items_series_id FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL;
ALTER TABLE quote_bom_items ADD CONSTRAINT ck_quote_bom_items__g07_discount_range_1 CHECK (discount_pct BETWEEN 0 AND 100);
ALTER TABLE quote_bom_items ADD CONSTRAINT ck_quote_bom_items__g06_fixed_no_discount_2 CHECK (rate_source <> 'FIXED_NO_DISCOUNT' OR discount_pct = 0);
ALTER TABLE quote_bom_items ADD CONSTRAINT ck_quote_bom_items__g02_l2_requires_product_3 CHECK (resolution_status <> 'L2' OR product_id IS NOT NULL);
ALTER TABLE quote_bom_items ADD CONSTRAINT ck_quote_bom_items__rate_source_in_pricelist_4 CHECK (rate_source IN ('PRICELIST','MANUAL_WITH_DISCOUNT','FIXED_NO_DISCOUNT','UNRESOLVED'));
ALTER TABLE quote_bom_items ADD CONSTRAINT ck_quote_bom_items__resolution_status_in_l0_5 CHECK (resolution_status IN ('L0','L1','L2'));
CREATE INDEX ix_quote_bom_items_9678619 ON quote_bom_items (quotation_id);
CREATE INDEX ix_quote_bom_items_3823478 ON quote_bom_items (panel_id);
CREATE INDEX ix_quote_bom_items_5507248 ON quote_bom_items (bom_id);
CREATE INDEX ix_quote_bom_items_644078 ON quote_bom_items (parent_line_id);
CREATE INDEX ix_quote_bom_items_1297945 ON quote_bom_items (product_id);
CREATE INDEX ix_quote_bom_items_3451423 ON quote_bom_items (cost_head_id);
CREATE INDEX ix_quote_bom_items_8866781 ON quote_bom_items (category_id);
ALTER TABLE sku_prices ADD CONSTRAINT fk_sku_prices_tenant_id FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE RESTRICT;
ALTER TABLE sku_prices ADD CONSTRAINT fk_sku_prices_catalog_sku_id FOREIGN KEY (catalog_sku_id) REFERENCES catalog_skus(id) ON DELETE RESTRICT;
ALTER TABLE sku_prices ADD CONSTRAINT fk_sku_prices_price_list_id FOREIGN KEY (price_list_id) REFERENCES price_lists(id) ON DELETE SET NULL;
ALTER TABLE sku_prices ADD CONSTRAINT fk_sku_prices_import_batch_id FOREIGN KEY (import_batch_id) REFERENCES import_batches(id) ON DELETE SET NULL;
CREATE INDEX idx_sku_prices_tenant_id ON sku_prices (tenant_id);
CREATE INDEX ix_sku_prices_4277999 ON sku_prices (catalog_sku_id);
ALTER TABLE user_roles ADD CONSTRAINT fk_user_roles_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;
ALTER TABLE user_roles ADD CONSTRAINT fk_user_roles_role_id FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT;
ALTER TABLE user_roles ADD CONSTRAINT uq_user_roles_1 UNIQUE (user_id,role_id);
CREATE INDEX ix_user_roles_491839 ON user_roles (user_id);
CREATE INDEX ix_user_roles_4109801 ON user_roles (role_id);

-- END
