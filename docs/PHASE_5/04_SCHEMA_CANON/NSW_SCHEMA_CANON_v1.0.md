# NSW Schema Canon v1.0

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT  
**Owner:** Phase 5 Senate  
**Purpose:** Canonical schema definition for NSW system - single source of truth for database structure

---

## Source of Truth Statement

**This document is the CANONICAL source of truth for:**
- Table definitions and structures
- Column definitions and data types
- Foreign key relationships
- Indexes and constraints
- Database-level business rules

**All database implementation must align with this schema. Changes require Phase 5 Senate approval.**

---

## Table of Contents

1. [Schema Principles](#schema-principles)
2. [DDL Definitions](#ddl-definitions)
3. [Constraints and Guardrails](#constraints-and-guardrails)
4. [Step-2 Design Decisions](#step-2-design-decisions)
5. [Indexes Summary](#indexes-summary)
6. [Change Log](#change-log)

---

## Schema Principles

### 1. Multi-Tenant Isolation

**Principle:** All tables (except `tenants`) must include `tenant_id` for data isolation.

**Implementation:**
- `tenant_id BIGINT NOT NULL` on all tenant-scoped tables
- Foreign key: `tenant_id REFERENCES tenants(id)`
- Index on `tenant_id` for filtered queries
- Composite indexes: `(tenant_id, other_columns)` for multi-tenant queries

### 2. Soft Delete Strategy

**Principle:** Use `is_active` boolean or `status` enum for soft deletes (where applicable).

**Implementation:**
- `is_active BOOLEAN NOT NULL DEFAULT true` on tables that support soft delete
- OR `status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'` with CHECK constraint for status-based soft delete
- `true`/`'ACTIVE'` = active, `false`/`'INACTIVE'` = soft deleted
- Index on `is_active` or `status` for filtering active records
- Query pattern: `WHERE is_active = true` or `WHERE status = 'ACTIVE'`

### 3. Timestamp Strategy

**Principle:** All tables include `created_at` and `updated_at` timestamps.

**Implementation:**
- `created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP`
- `updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP`
- Auto-update `updated_at` on row modification (database trigger or application layer)

### 4. ID Strategy

**Principle:** Use `BIGSERIAL` for primary keys (PostgreSQL).

**Implementation:**
- `id BIGSERIAL PRIMARY KEY`
- Sequential auto-incrementing IDs
- UUID option reserved for future consideration

### 5. Naming Conventions

**Principle:** Follow naming conventions defined in `NAMING_CONVENTIONS.md`.

**Implementation:**
- Tables: `snake_case`, plural (e.g., `quote_bom_items`)
- Columns: `snake_case`, singular (e.g., `product_id`)
- Foreign keys: `{table_singular}_id` (e.g., `product_id`)
- Enums: `UPPER_SNAKE_CASE` (e.g., `'PRICELIST'`)
- Timestamps: `{action}_at` (e.g., `created_at`)

---

## DDL Definitions

### AUTH Module Tables

#### tenants

```sql
CREATE TABLE tenants (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tenants_code ON tenants(code);
CREATE INDEX idx_tenants_status ON tenants(status);
```

#### users

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE')),
    email_verified_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
```

#### roles

```sql
CREATE TABLE roles (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, name)
);

CREATE INDEX idx_roles_tenant_id ON roles(tenant_id);
```

#### user_roles

```sql
CREATE TABLE user_roles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE (user_id, role_id)
);

CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
```

#### permissions (Optional - reserved for future)

```sql
CREATE TABLE permissions (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, resource, action)
);

CREATE INDEX idx_permissions_tenant_id ON permissions(tenant_id);
CREATE INDEX idx_permissions_resource ON permissions(resource);
```

#### role_permissions (Optional - reserved for future)

```sql
CREATE TABLE role_permissions (
    id BIGSERIAL PRIMARY KEY,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE (role_id, permission_id)
);

CREATE INDEX idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX idx_role_permissions_permission_id ON role_permissions(permission_id);
```

---

### CIM Module Tables (Component/Item Master)

#### categories

```sql
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, code)
);

CREATE INDEX idx_categories_tenant_id ON categories(tenant_id);
CREATE INDEX idx_categories_code ON categories(code);
CREATE INDEX idx_categories_is_active ON categories(is_active);
```

#### subcategories

```sql
CREATE TABLE subcategories (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, category_id, code)
);

CREATE INDEX idx_subcategories_tenant_id ON subcategories(tenant_id);
CREATE INDEX idx_subcategories_category_id ON subcategories(category_id);
CREATE INDEX idx_subcategories_is_active ON subcategories(is_active);
```

#### product_types

```sql
CREATE TABLE product_types (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, category_id, code)
);

CREATE INDEX idx_product_types_tenant_id ON product_types(tenant_id);
CREATE INDEX idx_product_types_category_id ON product_types(category_id);
CREATE INDEX idx_product_types_is_active ON product_types(is_active);
```

#### attributes

```sql
CREATE TABLE attributes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) NOT NULL CHECK (data_type IN ('TEXT', 'NUMBER', 'ENUM', 'BOOLEAN', 'DATE')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, name)
);

CREATE INDEX idx_attributes_tenant_id ON attributes(tenant_id);
CREATE INDEX idx_attributes_is_active ON attributes(is_active);
```

#### category_attributes

```sql
CREATE TABLE category_attributes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    attribute_id BIGINT NOT NULL,
    is_required BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES attributes(id) ON DELETE CASCADE,
    UNIQUE (category_id, attribute_id)
);

CREATE INDEX idx_category_attributes_tenant_id ON category_attributes(tenant_id);
CREATE INDEX idx_category_attributes_category_id ON category_attributes(category_id);
CREATE INDEX idx_category_attributes_attribute_id ON category_attributes(attribute_id);
```

#### makes

```sql
CREATE TABLE makes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, name)
);

CREATE INDEX idx_makes_tenant_id ON makes(tenant_id);
CREATE INDEX idx_makes_is_active ON makes(is_active);
```

#### series

```sql
CREATE TABLE series (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    make_id BIGINT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL,
    UNIQUE (tenant_id, make_id, name)
);

CREATE INDEX idx_series_tenant_id ON series(tenant_id);
CREATE INDEX idx_series_make_id ON series(make_id);
CREATE INDEX idx_series_is_active ON series(is_active);
```

#### products

```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    subcategory_id BIGINT NULL,
    product_type_id BIGINT NULL,
    generic_product_id BIGINT NULL,
    make_id BIGINT NULL,
    series_id BIGINT NULL,
    sku VARCHAR(100),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cost_head_id BIGINT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL,
    FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE SET NULL,
    FOREIGN KEY (generic_product_id) REFERENCES products(id) ON DELETE SET NULL,
    FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL,
    FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id) ON DELETE SET NULL
);

CREATE INDEX idx_products_tenant_id ON products(tenant_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_subcategory_id ON products(subcategory_id);
CREATE INDEX idx_products_product_type_id ON products(product_type_id);
CREATE INDEX idx_products_generic_product_id ON products(generic_product_id);
CREATE INDEX idx_products_make_id ON products(make_id);
CREATE INDEX idx_products_series_id ON products(series_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_cost_head_id ON products(cost_head_id);
CREATE INDEX idx_products_is_active ON products(is_active);
CREATE UNIQUE INDEX idx_products_tenant_sku ON products(tenant_id, sku) WHERE sku IS NOT NULL;
```

#### product_attributes

```sql
CREATE TABLE product_attributes (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    attribute_id BIGINT NOT NULL,
    value_text TEXT,
    value_number NUMERIC(15,2),
    value_boolean BOOLEAN,
    value_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES attributes(id) ON DELETE CASCADE,
    UNIQUE (product_id, attribute_id)
);

CREATE INDEX idx_product_attributes_tenant_id ON product_attributes(tenant_id);
CREATE INDEX idx_product_attributes_product_id ON product_attributes(product_id);
CREATE INDEX idx_product_attributes_attribute_id ON product_attributes(attribute_id);
```

---

### PRICING Module Tables

#### price_lists

```sql
CREATE TABLE price_lists (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    effective_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, code)
);

CREATE INDEX idx_price_lists_tenant_id ON price_lists(tenant_id);
CREATE INDEX idx_price_lists_code ON price_lists(code);
CREATE INDEX idx_price_lists_effective_date ON price_lists(effective_date);
CREATE INDEX idx_price_lists_is_active ON price_lists(is_active);
```

#### prices

```sql
CREATE TABLE prices (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    price_list_id BIGINT NULL,
    rate NUMERIC(15,2) NOT NULL CHECK (rate >= 0),
    effective_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'DELETED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (price_list_id) REFERENCES price_lists(id) ON DELETE SET NULL
);

CREATE INDEX idx_prices_tenant_id ON prices(tenant_id);
CREATE INDEX idx_prices_product_id ON prices(product_id);
CREATE INDEX idx_prices_price_list_id ON prices(price_list_id);
CREATE INDEX idx_prices_effective_date ON prices(effective_date);
CREATE INDEX idx_prices_status ON prices(status);
CREATE INDEX idx_prices_lookup ON prices(product_id, effective_date, status) WHERE status = 'ACTIVE';
```

#### import_batches (Optional - for price import tracking)

```sql
CREATE TABLE import_batches (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    price_list_id BIGINT NULL,
    file_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')),
    total_rows INTEGER DEFAULT 0,
    processed_rows INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    imported_by BIGINT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (price_list_id) REFERENCES price_lists(id) ON DELETE SET NULL,
    FOREIGN KEY (imported_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_import_batches_tenant_id ON import_batches(tenant_id);
CREATE INDEX idx_import_batches_price_list_id ON import_batches(price_list_id);
CREATE INDEX idx_import_batches_status ON import_batches(status);
```

#### import_approval_queue (Optional - for price import approval workflow)

```sql
CREATE TABLE import_approval_queue (
    id BIGSERIAL PRIMARY KEY,
    import_batch_id BIGINT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
    requested_by BIGINT NOT NULL,
    approved_by BIGINT NULL,
    approved_at TIMESTAMP NULL,
    comments TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (import_batch_id) REFERENCES import_batches(id) ON DELETE CASCADE,
    FOREIGN KEY (requested_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_import_approval_queue_import_batch_id ON import_approval_queue(import_batch_id);
CREATE INDEX idx_import_approval_queue_status ON import_approval_queue(status);
```

---

### MBOM Module Tables (Master BOM)

#### master_boms

```sql
CREATE TABLE master_boms (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    unique_no VARCHAR(100),
    description TEXT,
    template_type VARCHAR(50) NOT NULL CHECK (template_type IN ('FEEDER', 'PANEL', 'GENERIC')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

CREATE INDEX idx_master_boms_tenant_id ON master_boms(tenant_id);
CREATE INDEX idx_master_boms_unique_no ON master_boms(unique_no);
CREATE INDEX idx_master_boms_template_type ON master_boms(template_type);
CREATE INDEX idx_master_boms_is_active ON master_boms(is_active);
```

#### master_bom_items

```sql
CREATE TABLE master_bom_items (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    master_bom_id BIGINT NOT NULL,
    resolution_status VARCHAR(10) NOT NULL CHECK (resolution_status IN ('L0', 'L1')),
    generic_descriptor VARCHAR(500),
    defined_spec_json JSONB,
    product_id BIGINT NULL CHECK (product_id IS NULL),
    quantity NUMERIC(10,3) NOT NULL DEFAULT 1.0 CHECK (quantity > 0),
    uom VARCHAR(50),
    sequence_order INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (master_bom_id) REFERENCES master_boms(id) ON DELETE CASCADE,
    CONSTRAINT chk_master_bom_item_l0_l1 CHECK (
        (resolution_status = 'L0' AND generic_descriptor IS NOT NULL AND defined_spec_json IS NULL) OR
        (resolution_status = 'L1' AND defined_spec_json IS NOT NULL AND generic_descriptor IS NULL)
    )
);

CREATE INDEX idx_master_bom_items_tenant_id ON master_bom_items(tenant_id);
CREATE INDEX idx_master_bom_items_master_bom_id ON master_bom_items(master_bom_id);
CREATE INDEX idx_master_bom_items_resolution_status ON master_bom_items(resolution_status);
```

**Note:** G1 Guardrail enforced: `product_id` MUST be NULL for all master_bom_items (CHECK constraint ensures this).

---

### CUSTOMER Module Tables

#### customers

```sql
CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, code)
);

CREATE INDEX idx_customers_tenant_id ON customers(tenant_id);
CREATE INDEX idx_customers_code ON customers(code);
CREATE INDEX idx_customers_status ON customers(status);
```

**Note:** Minimal customers table for MVP. Additional fields (address, contact info, etc.) can be added in future phases.

---

### QUO Module Tables (Quotation)

#### quotations

```sql
CREATE TABLE quotations (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quote_no VARCHAR(100) NOT NULL,
    customer_id BIGINT NULL,
    customer_name_snapshot VARCHAR(255),
    project_id BIGINT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'APPROVED', 'FINALIZED', 'CANCELLED')),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    UNIQUE (tenant_id, quote_no)
);

CREATE INDEX idx_quotations_tenant_id ON quotations(tenant_id);
CREATE INDEX idx_quotations_quote_no ON quotations(quote_no);
CREATE INDEX idx_quotations_customer_id ON quotations(customer_id);
CREATE INDEX idx_quotations_status ON quotations(status);
CREATE INDEX idx_quotations_created_by ON quotations(created_by);
```

**Note:** Customer normalization decision (Step-2): Both `customer_id` (optional FK) and `customer_name_snapshot` (text) are included.

#### quote_panels

```sql
CREATE TABLE quote_panels (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quotation_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity NUMERIC(10,3) NOT NULL DEFAULT 1.0 CHECK (quantity > 0),
    rate NUMERIC(15,2) DEFAULT 0 CHECK (rate >= 0),
    amount NUMERIC(15,2) DEFAULT 0 CHECK (amount >= 0),
    sequence_order INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE
);

CREATE INDEX idx_quote_panels_tenant_id ON quote_panels(tenant_id);
CREATE INDEX idx_quote_panels_quotation_id ON quote_panels(quotation_id);
CREATE INDEX idx_quote_panels_sequence_order ON quote_panels(quotation_id, sequence_order);
```

#### quote_boms

```sql
CREATE TABLE quote_boms (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quotation_id BIGINT NOT NULL,
    panel_id BIGINT NOT NULL,
    parent_bom_id BIGINT NULL,
    level INTEGER NOT NULL DEFAULT 0 CHECK (level >= 0 AND level <= 2),
    name VARCHAR(255) NOT NULL,
    quantity NUMERIC(10,3) NOT NULL DEFAULT 1.0 CHECK (quantity > 0),
    rate NUMERIC(15,2) DEFAULT 0 CHECK (rate >= 0),
    amount NUMERIC(15,2) DEFAULT 0 CHECK (amount >= 0),
    origin_master_bom_id BIGINT NULL,
    origin_master_bom_version VARCHAR(50),
    instance_sequence_no INTEGER NULL,
    is_modified BOOLEAN NOT NULL DEFAULT false,
    modified_by BIGINT NULL,
    modified_at TIMESTAMP NULL,
    sequence_order INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE,
    FOREIGN KEY (panel_id) REFERENCES quote_panels(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_bom_id) REFERENCES quote_boms(id) ON DELETE CASCADE,
    FOREIGN KEY (origin_master_bom_id) REFERENCES master_boms(id) ON DELETE SET NULL,
    FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_quote_boms_tenant_id ON quote_boms(tenant_id);
CREATE INDEX idx_quote_boms_quotation_id ON quote_boms(quotation_id);
CREATE INDEX idx_quote_boms_panel_id ON quote_boms(panel_id);
CREATE INDEX idx_quote_boms_parent_bom_id ON quote_boms(parent_bom_id);
CREATE INDEX idx_quote_boms_origin_master_bom_id ON quote_boms(origin_master_bom_id);
CREATE INDEX idx_quote_boms_level ON quote_boms(level);
CREATE INDEX idx_quote_boms_is_modified ON quote_boms(is_modified);
```

#### quote_bom_items

```sql
CREATE TABLE quote_bom_items (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quotation_id BIGINT NOT NULL,
    panel_id BIGINT NOT NULL,
    bom_id BIGINT NOT NULL,
    parent_line_id BIGINT NULL,
    product_id BIGINT NULL,
    make_id BIGINT NULL,
    series_id BIGINT NULL,
    quantity NUMERIC(10,3) NOT NULL DEFAULT 1.0 CHECK (quantity > 0),
    rate NUMERIC(15,2) DEFAULT 0 CHECK (rate >= 0),
    discount_pct NUMERIC(5,2) DEFAULT 0 CHECK (discount_pct >= 0 AND discount_pct <= 100),
    net_rate NUMERIC(15,2) DEFAULT 0 CHECK (net_rate >= 0),
    amount NUMERIC(15,2) DEFAULT 0 CHECK (amount >= 0),
    rate_source VARCHAR(50) NOT NULL DEFAULT 'UNRESOLVED' CHECK (rate_source IN ('PRICELIST', 'MANUAL_WITH_DISCOUNT', 'FIXED_NO_DISCOUNT', 'UNRESOLVED')),
    is_price_missing BOOLEAN NOT NULL DEFAULT false,
    is_client_supplied BOOLEAN NOT NULL DEFAULT false,
    is_locked BOOLEAN NOT NULL DEFAULT false,
    cost_head_id BIGINT NULL,
    resolution_status VARCHAR(10) NOT NULL CHECK (resolution_status IN ('L0', 'L1', 'L2')),
    description VARCHAR(500),
    metadata_json JSONB,
    sequence_order INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE,
    FOREIGN KEY (panel_id) REFERENCES quote_panels(id) ON DELETE CASCADE,
    FOREIGN KEY (bom_id) REFERENCES quote_boms(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_line_id) REFERENCES quote_bom_items(id) ON DELETE SET NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
    FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE SET NULL,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL,
    FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id) ON DELETE SET NULL,
    CONSTRAINT chk_quote_bom_item_resolution CHECK (
        (resolution_status = 'L2' AND product_id IS NOT NULL) OR
        (resolution_status IN ('L0', 'L1') AND product_id IS NULL)
    ),
    CONSTRAINT chk_quote_bom_item_rate_source CHECK (
        (rate_source = 'FIXED_NO_DISCOUNT' AND discount_pct = 0) OR
        (rate_source != 'FIXED_NO_DISCOUNT')
    )
);

CREATE INDEX idx_quote_bom_items_tenant_id ON quote_bom_items(tenant_id);
CREATE INDEX idx_quote_bom_items_quotation_id ON quote_bom_items(quotation_id);
CREATE INDEX idx_quote_bom_items_panel_id ON quote_bom_items(panel_id);
CREATE INDEX idx_quote_bom_items_bom_id ON quote_bom_items(bom_id);
CREATE INDEX idx_quote_bom_items_parent_line_id ON quote_bom_items(parent_line_id);
CREATE INDEX idx_quote_bom_items_product_id ON quote_bom_items(product_id);
CREATE INDEX idx_quote_bom_items_cost_head_id ON quote_bom_items(cost_head_id);
CREATE INDEX idx_quote_bom_items_resolution_status ON quote_bom_items(resolution_status);
CREATE INDEX idx_quote_bom_items_rate_source ON quote_bom_items(rate_source);
CREATE INDEX idx_quote_bom_items_is_locked ON quote_bom_items(is_locked);
CREATE INDEX idx_quote_bom_items_is_price_missing ON quote_bom_items(is_price_missing);
```

**Note:** Multi-SKU linkage decision (Step-2): `parent_line_id` and `metadata_json` are included for multi-SKU support.

**Note:** Resolution level decision (Step-2): `resolution_status` supports L0/L1/L2 with validation rules enforced via CHECK constraints.

#### quote_bom_item_history (Optional - for audit trail)

```sql
CREATE TABLE quote_bom_item_history (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    quote_bom_item_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('CREATED', 'UPDATED', 'DELETED', 'RESOLVED', 'PRICE_CHANGED')),
    changed_by BIGINT NULL,
    old_values JSONB,
    new_values JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (quote_bom_item_id) REFERENCES quote_bom_items(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_quote_bom_item_history_tenant_id ON quote_bom_item_history(tenant_id);
CREATE INDEX idx_quote_bom_item_history_item_id ON quote_bom_item_history(quote_bom_item_id);
CREATE INDEX idx_quote_bom_item_history_created_at ON quote_bom_item_history(created_at);
CREATE INDEX idx_quote_bom_item_history_action ON quote_bom_item_history(action);
```

---

### SHARED Module Tables

#### cost_heads

```sql
CREATE TABLE cost_heads (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    code VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('MATERIAL', 'LABOUR', 'OTHER')),
    priority INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    UNIQUE (tenant_id, code)
);

CREATE INDEX idx_cost_heads_tenant_id ON cost_heads(tenant_id);
CREATE INDEX idx_cost_heads_code ON cost_heads(code);
CREATE INDEX idx_cost_heads_category ON cost_heads(category);
CREATE INDEX idx_cost_heads_is_active ON cost_heads(is_active);
```

**Note:** `cost_heads` is tenant-scoped to allow different tenants to have their own cost head codes and governance.

---

### AUDIT Module Tables

#### audit_logs

```sql
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    user_id BIGINT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id BIGINT NOT NULL,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_audit_logs_tenant_id ON audit_logs(tenant_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

#### bom_change_logs (Optional)

```sql
CREATE TABLE bom_change_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    bom_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN ('CREATED', 'MODIFIED', 'ITEM_ADDED', 'ITEM_UPDATED', 'ITEM_DELETED')),
    field_name VARCHAR(100),
    before_value TEXT,
    after_value TEXT,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (bom_id) REFERENCES quote_boms(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE INDEX idx_bom_change_logs_tenant_id ON bom_change_logs(tenant_id);
CREATE INDEX idx_bom_change_logs_bom_id ON bom_change_logs(bom_id);
CREATE INDEX idx_bom_change_logs_user_id ON bom_change_logs(user_id);
CREATE INDEX idx_bom_change_logs_created_at ON bom_change_logs(created_at);
CREATE INDEX idx_bom_change_logs_action ON bom_change_logs(action);
```

---

### AI Module Tables (Schema Reservation - Post-Phase 5 Implementation)

#### ai_call_logs

```sql
CREATE TABLE ai_call_logs (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    user_id BIGINT NULL,
    quotation_id BIGINT NULL,
    panel_id BIGINT NULL,
    feeder_id BIGINT NULL,
    bom_item_id BIGINT NULL,
    endpoint VARCHAR(100) NOT NULL,
    request_json JSONB NOT NULL,
    response_json JSONB NOT NULL,
    final_action VARCHAR(50) CHECK (final_action IN ('ACCEPTED', 'REJECTED', 'MODIFIED')),
    status VARCHAR(20) NOT NULL DEFAULT 'OK' CHECK (status IN ('OK', 'WARNING', 'ERROR')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE SET NULL,
    FOREIGN KEY (panel_id) REFERENCES quote_panels(id) ON DELETE SET NULL,
    FOREIGN KEY (feeder_id) REFERENCES quote_boms(id) ON DELETE SET NULL,
    FOREIGN KEY (bom_item_id) REFERENCES quote_bom_items(id) ON DELETE SET NULL
);

CREATE INDEX idx_ai_call_logs_tenant_id ON ai_call_logs(tenant_id);
CREATE INDEX idx_ai_call_logs_user_id ON ai_call_logs(user_id);
CREATE INDEX idx_ai_call_logs_quotation_id ON ai_call_logs(quotation_id);
CREATE INDEX idx_ai_call_logs_endpoint ON ai_call_logs(endpoint);
CREATE INDEX idx_ai_call_logs_created_at ON ai_call_logs(created_at);
```

**Note:** AI tables are schema reservations for Post-Phase 5 implementation. Structure is defined but not implemented in Phase 5 MVP.

---

## Constraints and Guardrails

### G1: Master BOM Rejects ProductId

**Enforcement:**
- Database constraint: `CHECK (product_id IS NULL)` on `master_bom_items`
- Application layer: Model boot hook enforces ProductId = NULL for L0/L1

**Implementation:**
```sql
-- Already enforced in master_bom_items table definition
product_id BIGINT NULL CHECK (product_id IS NULL)
```

### G2: Production BOM Requires ProductId at L2

**Enforcement:**
- Database constraint: CHECK constraint ensures L2 requires ProductId
- Application layer: Validation requires ProductId for L2 resolution

**Implementation:**
```sql
-- Enforced in quote_bom_items table definition
CONSTRAINT chk_quote_bom_item_resolution CHECK (
    (resolution_status = 'L2' AND product_id IS NOT NULL) OR
    (resolution_status IN ('L0', 'L1') AND product_id IS NULL)
)
```

### G3: IsPriceMissing Normalizes Amount

**Enforcement:**
- Application layer: Service-level normalization sets Rate/NetRate/Amount to 0 when IsPriceMissing = true
- Database constraint: No direct constraint (service-level rule)

### G4: RateSource Consistency

**Enforcement:**
- Database constraint: CHECK constraint on `rate_source` enum values
- Application layer: Business logic ensures RateSource consistency with discount application

**Implementation:**
```sql
-- Enforced in quote_bom_items table definition
rate_source VARCHAR(50) NOT NULL DEFAULT 'UNRESOLVED' 
    CHECK (rate_source IN ('PRICELIST', 'MANUAL_WITH_DISCOUNT', 'FIXED_NO_DISCOUNT', 'UNRESOLVED'))
```

### G5: UNRESOLVED Normalizes Values

**Enforcement:**
- Application layer: Service-level normalization clears pricing fields when RateSource = 'UNRESOLVED'
- Database constraint: No direct constraint (service-level rule)

### G6: FIXED_NO_DISCOUNT Forces Discount=0

**Enforcement:**
- Database constraint: CHECK constraint ensures discount_pct = 0 when rate_source = 'FIXED_NO_DISCOUNT'
- Application layer: Business logic enforces discount = 0 for FIXED_NO_DISCOUNT

**Implementation:**
```sql
-- Enforced in quote_bom_items table definition
CONSTRAINT chk_quote_bom_item_rate_source CHECK (
    (rate_source = 'FIXED_NO_DISCOUNT' AND discount_pct = 0) OR
    (rate_source != 'FIXED_NO_DISCOUNT')
)
```

### G7: All Discounts are Percentage-Based (0-100)

**Enforcement:**
- Database constraint: CHECK constraint ensures discount_pct is between 0 and 100
- Application layer: Validation ensures discount values are percentages

**Implementation:**
```sql
-- Enforced in quote_bom_items table definition
discount_pct NUMERIC(5,2) DEFAULT 0 CHECK (discount_pct >= 0 AND discount_pct <= 100)
```

---

## Step-2 Design Decisions

### Decision 1: Multi-SKU Linkage

**Decision:** Support multi-SKU linkage via `parent_line_id` + `metadata_json`.

**Implementation:**
- Added `parent_line_id BIGINT NULL` to `quote_bom_items` (self-referencing FK)
- Added `metadata_json JSONB` to `quote_bom_items` for flexible metadata storage
- `parent_line_id` references `quote_bom_items.id` (nullable for standalone items)
- `metadata_json` stores SKU-specific metadata (e.g., variant information, additional attributes)

**Rationale:**
- Allows hierarchical item relationships (parent-child SKU linkages)
- Flexible metadata storage without schema changes
- Supports complex product configurations

**Schema Location:**
- `quote_bom_items.parent_line_id`
- `quote_bom_items.metadata_json`

---

### Decision 2: Customer Normalization

**Decision:** Support both `customer_id` (optional FK) and `customer_name_snapshot` (text).

**Implementation:**
- Added `customer_id BIGINT NULL` to `quotations` (optional FK for future customer table)
- Added `customer_name_snapshot VARCHAR(255)` to `quotations` (text field for historical snapshot)
- Both fields are nullable and independent

**Rationale:**
- `customer_id`: Provides structured reference for future customer master table integration
- `customer_name_snapshot`: Preserves historical customer name at quotation creation time
- Dual approach ensures both structured data and historical accuracy

**Schema Location:**
- `quotations.customer_id`
- `quotations.customer_name_snapshot`

---

### Decision 3: Resolution Levels (L0/L1/L2)

**Decision:** Support resolution levels L0/L1/L2 across MBOM and QUO with explicit rules.

**Implementation:**
- `master_bom_items.resolution_status`: CHECK constraint allows only L0/L1
- `quote_bom_items.resolution_status`: CHECK constraint allows L0/L1/L2
- Validation rules:
  - L0/L1: `product_id` MUST be NULL (template/placeholder)
  - L2: `product_id` MUST be NOT NULL (resolved/production)
- Resolution level constraints enforced via CHECK constraints

**Rationale:**
- Clear separation between template (MBOM: L0/L1) and production (QUO: L2) states
- Explicit validation rules prevent invalid state transitions
- Database-level enforcement ensures data integrity

**Schema Location:**
- `master_bom_items.resolution_status` (L0/L1 only)
- `quote_bom_items.resolution_status` (L0/L1/L2)
- `quote_bom_items` CHECK constraint: `chk_quote_bom_item_resolution`

---

## Indexes Summary

### Performance Indexes

All tables include indexes on:
- Primary key (`id`)
- Foreign keys (for join performance)
- `tenant_id` (for multi-tenant filtering)
- Status/active flags (for filtering)
- Lookup columns (e.g., `sku`, `code`, `email`)

### Composite Indexes

Key composite indexes:
- `(tenant_id, email)` on `users` (unique constraint)
- `(tenant_id, code)` on various tables (unique constraints)
- `(product_id, effective_date, status)` on `prices` (for price lookup)
- `(quotation_id, sequence_order)` on `quote_panels` and `quote_boms` (for ordering)

### Query Optimization Indexes

- `idx_prices_lookup`: Optimized for price lookup queries (WHERE product_id = X AND effective_date <= CURDATE AND status = 'ACTIVE')
- `idx_quote_bom_items_resolution_status`: For filtering by resolution status
- `idx_quote_bom_items_rate_source`: For filtering by rate source

---

## Change Log

### v1.0 (2025-01-27) - DRAFT → FREEZE-READY

**Initial Release:**
- Complete DDL for all MVP tables
- AUTH, CIM, PRICING, MBOM, QUO, SHARED, AUDIT, AI modules
- Constraints reflecting G1-G7 guardrails
- Step-2 design decisions locked (Multi-SKU, Customer, Resolution levels)
- Indexes and foreign keys defined

**Step-2 Freeze Gate Fixes (2025-01-27):**
- **Tenant Scoping Consistency:** Added `tenant_id` to all transactional tables:
  - QUO: `quote_panels`, `quote_boms`, `quote_bom_items`, `quote_bom_item_history`
  - MBOM: `master_bom_items`
  - CIM: `product_attributes`, `category_attributes`
  - AUDIT: `bom_change_logs`
- **Soft Delete Strategy:** Updated principle to use `is_active`/`status` instead of `deleted_at` (consistent with existing implementation)
- **Cost Heads Scoping:** Made `cost_heads` tenant-scoped with `tenant_id`, unique `(tenant_id, code)`, and FK to tenants
- **Customers Table:** Added minimal `customers` table (tenant-scoped) and FK from `quotations.customer_id` to `customers.id`

**Status:** FREEZE-READY (Pending final freeze gate approval)  
**Next Steps:** Final freeze gate verification, mark as FROZEN

---

**Status:** DRAFT  
**Owner:** Phase 5 Senate  
**Created:** 2025-01-27

