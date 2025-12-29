# NSW Data Dictionary v1.0

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Purpose:** Canonical data dictionary for NSW system - single source of truth for entity definitions, relationships, and business rules

---

## Source of Truth Statement

**This document is the CANONICAL source of truth for:**
- Entity definitions and semantics
- Entity relationships and foreign keys
- Business rules and constraints
- Data validation rules
- Module ownership

**All implementation must align with this dictionary. Changes require Phase 5 Senate approval.**

---

## Table of Contents

1. [Overview](#overview)
2. [Core Entities](#core-entities)
3. [Entity Relationships](#entity-relationships)
4. [Business Rules](#business-rules)
5. [Supporting Documents](#supporting-documents)
6. [Change Log](#change-log)

---

## Overview

### Purpose

The NSW Data Dictionary defines the canonical data model for the NSW (New System) estimation software. It provides:
- Complete entity definitions
- Relationship mappings
- Business rule specifications
- Validation guardrails
- Module ownership

### Scope

**Phase 5 Scope:**
- Step 1: Data Dictionary (this document) - **FROZEN** ✅
- Step 2: Schema Design (separate document) - Pending

**Out of Scope:**
- Implementation code
- API design (reference only)
- UI design (reference only)

---

## Core Entities

### AUTH Module Entities

#### Tenant

**Entity:** `tenants`  
**Purpose:** Multi-tenant isolation root  
**Owner:** AUTH

**Key Attributes:**
- `id` - Primary key (bigserial)
- `code` - Tenant code (unique identifier)
- `name` - Tenant name
- `status` - Active/Inactive status

**Business Rules:**
- All other tables reference `tenant_id` for isolation
- Tenant is root of data isolation hierarchy

---

#### User

**Entity:** `users`  
**Purpose:** User accounts and authentication  
**Owner:** AUTH

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `email` - User email (unique per tenant)
- `name` - User display name
- `password_hash` - Encrypted password
- `status` - Active/Inactive status

**Business Rules:**
- Users are scoped to tenant
- Email must be unique within tenant
- Password must be encrypted

---

#### Role

**Entity:** `roles`  
**Purpose:** Role definitions for RBAC  
**Owner:** AUTH

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `name` - Role name (e.g., 'admin', 'estimator', 'reviewer')
- `description` - Role description

**Business Rules:**
- Roles are scoped to tenant
- Standard roles: admin, estimator, reviewer, viewer

---

### CIM Module Entities (Component/Item Master)

#### Category

**Entity:** `categories`  
**Purpose:** Top-level product taxonomy  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `name` - Category name
- `code` - Category code (unique per tenant)
- `description` - Category description
- `is_active` - Active status

**Business Rules:**
- Categories are scoped to tenant
- Code must be unique within tenant
- Category drives attribute schema

---

#### Product

**Entity:** `products`  
**Purpose:** Buyable product master (Legacy - will be replaced by L2 SKUs)  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `category_id` - Foreign key to categories
- `subcategory_id` - Foreign key to subcategories (nullable)
- `product_type_id` - Foreign key to product_types (nullable)
- `make_id` - Foreign key to makes (nullable)
- `series_id` - Foreign key to series (nullable)
- `sku` - Product SKU
- `name` - Product name
- `description` - Product description
- `cost_head_id` - Foreign key to cost_heads (nullable, optional in MVP)
- `is_active` - Active status

**Business Rules:**
- Products are scoped to tenant
- Category is required
- SKU should be unique within tenant
- Product can have default CostHead (optional in MVP)
- **Note:** Legacy entity - will be replaced by L2 SKU model in Phase 5

---

#### L1 Intent Line

**Entity:** `l1_intent_lines`  
**Purpose:** Engineering interpretation layer (L1) - carries all engineering meaning  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `category_id` - Foreign key to categories
- `subcategory_id` - Foreign key to subcategories (nullable)
- `product_type_id` - Foreign key to product_types
- `make_id` - Foreign key to makes (nullable)
- `series_id` - Foreign key to series (nullable)
- `series_bucket` - Series bucket identifier (e.g., LC1E, LC1D, LP1K)
- `line_type` - Line type (BASE, FEATURE)
- `line_group_id` - Foreign key to l1_line_groups (nullable, for grouping related L1 lines)
- `description` - Engineering description
- `is_active` - Active status
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- L1 lines are scoped to tenant
- L1 carries all engineering meaning (Duty, Rating, Voltage, Poles, etc.)
- Multiple L1 lines can map to the same L2 SKU (many-to-one relationship)
- L1 BASE lines represent base product interpretations
- L1 FEATURE lines represent accessory/feature interpretations
- **G8 Guardrail:** L1 lines can legally map to the same L2 SKU (SKU reuse is allowed and expected)

---

#### L1 Attribute

**Entity:** `l1_attributes`  
**Purpose:** Key-Value-Unit (KVU) attributes for L1 intent lines  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `l1_intent_line_id` - Foreign key to l1_intent_lines
- `attribute_code` - Attribute code (e.g., 'DUTY', 'RATING_AC1', 'RATING_AC3', 'VOLTAGE', 'POLES')
- `value_text` - Text value (nullable)
- `value_number` - Numeric value (nullable)
- `value_unit` - Unit of measure (e.g., 'A', 'V', 'P')
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- L1 attributes are scoped to tenant
- Each L1 line can have multiple attributes (one-to-many)
- Attributes define engineering meaning (Duty, Rating, Voltage, etc.)
- Attributes are used for L1 → L2 explosion logic

---

#### L1 Line Group

**Entity:** `l1_line_groups`  
**Purpose:** Groups related L1 lines (e.g., BASE + FEATURE lines)  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `group_name` - Group name/identifier
- `description` - Group description
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- L1 line groups are scoped to tenant
- Groups can contain multiple L1 lines (BASE + FEATURE lines)
- Used for organizing related engineering interpretations

---

#### L2 SKU (Catalog SKU)

**Entity:** `catalog_skus` (also referenced as `l2_skus`)  
**Purpose:** Commercial SKU layer (L2) - SKU-pure, commercial truth only  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `make` - Make name (e.g., 'Schneider')
- `oem_catalog_no` - OEM catalog number (SKU) - unique per make
- `oem_series_range` - OEM series range (e.g., 'Easy TeSys', 'TeSys Deca')
- `series_bucket` - Series bucket identifier (e.g., LC1E, LC1D, LP1K)
- `item_producttype` - Item product type (e.g., 'Contactor', 'Control Relay', 'MPCB')
- `business_subcategory` - Business subcategory (e.g., 'Power Contactor', 'Control Relay')
- `uom` - Unit of measure (default: 'EA')
- `is_active` - Active status
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- L2 SKUs are scoped to tenant
- **SKU-pure rule:** One L2 row per distinct OEM catalog number
- **No engineering meaning:** L2 does NOT contain Duty, Rating, Voltage, Poles, etc.
- **Unique constraint:** (make, oem_catalog_no) must be unique
- **Many-to-one mapping:** Multiple L1 lines can map to the same L2 SKU
- Price lives at L2 SKU level (via sku_prices table)

---

#### L2 Price (SKU Price)

**Entity:** `sku_prices` (also referenced as `l2_prices`)  
**Purpose:** Price history for L2 SKUs (append-only)  
**Owner:** PRICING

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `catalog_sku_id` - Foreign key to catalog_skus (L2 SKU)
- `price_list_id` - Foreign key to price_lists
- `pricelist_ref` - Price list reference identifier
- `rate` - Price rate (numeric)
- `currency` - Currency code (default: 'INR')
- `region` - Region identifier (default: 'INDIA')
- `effective_from` - Effective date (date)
- `effective_to` - Effective to date (nullable)
- `import_batch_id` - Foreign key to import_batches (nullable)
- `source_file` - Source file name (nullable)
- `source_row` - Source row number (nullable)
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- L2 prices are scoped to tenant
- **Append-only rule:** Never overwrite, always insert new rows
- Price lookup: WHERE effective_from <= CURDATE() AND (effective_to IS NULL OR effective_to >= CURDATE()) ORDER BY effective_from DESC LIMIT 1
- Multiple prices per SKU allowed (historical price tracking)
- Price refresh updates L2 SKU prices, automatically reflects in all L1 interpretations

---

#### L1 to L2 Mapping

**Entity:** `l1_l2_mappings`  
**Purpose:** Maps L1 intent lines to L2 SKUs (many-to-one relationship)  
**Owner:** CIM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `l1_intent_line_id` - Foreign key to l1_intent_lines
- `catalog_sku_id` - Foreign key to catalog_skus (L2 SKU)
- `mapping_type` - Mapping type (BASE, FEATURE_ADDON, FEATURE_INCLUDED, FEATURE_BUNDLED)
- `is_primary` - Primary mapping flag (for BASE lines)
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- L1 to L2 mappings are scoped to tenant
- **Many-to-one rule:** Multiple L1 lines can map to the same L2 SKU
- **G8 Guardrail:** SKU reuse is allowed and expected
- BASE lines typically have one primary mapping
- FEATURE lines can have multiple mappings based on feature policy

---

### MBOM Module Entities (Master BOM)

#### Master BOM

**Entity:** `master_boms`  
**Purpose:** Reusable BOM templates  
**Owner:** MBOM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `name` - BOM template name
- `unique_no` - Unique identifier
- `description` - BOM description
- `template_type` - Template type (FEEDER, PANEL, GENERIC)
- `is_active` - Active status

**Business Rules:**
- Master BOMs are scoped to tenant
- Master BOMs are templates (L0/L1 items only)
- Copy-never-link rule: Always copy, never link directly

---

#### Master BOM Item

**Entity:** `master_bom_items`  
**Purpose:** Master BOM line items (templates)  
**Owner:** MBOM

**Key Attributes:**
- `id` - Primary key (bigserial)
- `master_bom_id` - Foreign key to master_boms
- `resolution_status` - Resolution level (L0 or L1 only)
- `generic_descriptor` - Generic description (for L0)
- `defined_spec_json` - JSON specification (for L1)
- `product_id` - **MUST BE NULL** (enforced by G1 guardrail)
- `quantity` - Template quantity
- `uom` - Unit of measure

**Business Rules:**
- **G1 Guardrail:** ProductId MUST be NULL (L0/L1 only)
- L0: Generic placeholder (GenericDescriptor required)
- L1: Defined specification (DefinedSpecJson required)
- L2: NOT allowed in Master BOM

---

### QUO Module Entities (Quotation)

#### Quotation

**Entity:** `quotations`  
**Purpose:** Quotation header  
**Owner:** QUO

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `quote_no` - Quotation number (unique per tenant)
- `customer_name` - Customer name (text field, optional FK in future)
- `project_id` - Foreign key to projects (nullable)
- `status` - Quotation status (DRAFT, APPROVED, FINALIZED)
- `created_by` - Foreign key to users
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- Quotations are scoped to tenant
- Quote number must be unique within tenant
- Status workflow: DRAFT → APPROVED → FINALIZED

---

#### Quote Panel

**Entity:** `quote_panels`  
**Purpose:** Panel/Sale item level  
**Owner:** QUO

**Key Attributes:**
- `id` - Primary key (bigserial)
- `quotation_id` - Foreign key to quotations
- `name` - Panel name
- `quantity` - Panel quantity
- `rate` - Panel rate (calculated from BOMs)
- `amount` - Panel amount (calculated)
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- Panels belong to quotation
- Panel amount = sum of all BOM amounts under panel
- Panel can have direct items or BOMs

---

#### Quote BOM

**Entity:** `quote_boms`  
**Purpose:** BOM/Feeder level (hierarchical)  
**Owner:** QUO

**Key Attributes:**
- `id` - Primary key (bigserial)
- `quotation_id` - Foreign key to quotations
- `panel_id` - Foreign key to quote_panels
- `parent_bom_id` - Foreign key to quote_boms (nullable, for hierarchy)
- `level` - BOM level (0=Feeder, 1=BOM1, 2=BOM2)
- `name` - BOM name
- `quantity` - BOM quantity
- `rate` - BOM rate (calculated from items)
- `amount` - BOM amount (calculated)
- `origin_master_bom_id` - Foreign key to master_boms (nullable, reference only)
- `origin_master_bom_version` - Master BOM version at application time
- `instance_sequence_no` - Sequence number for multiple instances
- `is_modified` - Modified from Master BOM flag
- `modified_by` - Foreign key to users (nullable)
- `modified_at` - Modification timestamp (nullable)
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- BOMs belong to panel
- BOM hierarchy: Level 0 (Feeder) → Level 1 (BOM1) → Level 2 (BOM2)
- Parent BOM ID links hierarchy
- Origin Master BOM ID is reference only (copy-never-link)
- Instance sequence number for multiple instances of same Master BOM

---

#### Quote BOM Item

**Entity:** `quote_bom_items`  
**Purpose:** BOM line item (component)  
**Owner:** QUO

**Key Attributes:**
- `id` - Primary key (bigserial)
- `quotation_id` - Foreign key to quotations
- `panel_id` - Foreign key to quote_panels
- `bom_id` - Foreign key to quote_boms
- `product_id` - Foreign key to products (required for L2)
- `make_id` - Foreign key to makes (nullable)
- `series_id` - Foreign key to series (nullable)
- `quantity` - Item quantity per BOM
- `rate` - Item rate
- `discount` - Discount percentage (0-100)
- `net_rate` - Calculated: Rate × (1 - Discount/100)
- `amount` - Calculated: NetRate × TotalQty
- `rate_source` - Rate source enum (PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT, UNRESOLVED)
- `is_price_missing` - Price missing flag
- `is_client_supplied` - Client supplied flag (zero cost)
- `is_locked` - Locked flag (prevents deletion)
- `cost_head_id` - Foreign key to cost_heads (nullable, item override)
- `resolution_status` - Resolution level (L2 for production BOM)
- `description` - Item description
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**Business Rules:**
- **G2 Guardrail:** ProductId required for L2 (resolved state)
- **G3 Guardrail:** IsPriceMissing normalizes Rate/Net/Amount to 0
- **G4 Guardrail:** RateSource consistency rules
- **G5 Guardrail:** UNRESOLVED normalizes all pricing fields
- **G6 Guardrail:** FIXED_NO_DISCOUNT forces Discount=0
- **G7 Guardrail:** Discount is percentage-based (0-100)
- Locking prevents deletion (is_locked = true)
- CostHead resolution: Item override → Product default → System default

---

### PRICING Module Entities

#### Price List

**Entity:** `price_lists`  
**Purpose:** Price list headers  
**Owner:** PRICING

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `name` - Price list name
- `code` - Price list code
- `effective_date` - Effective date
- `is_active` - Active status

**Business Rules:**
- Price lists are scoped to tenant
- Effective date determines active price list

---

#### Price

**Entity:** `prices`  
**Purpose:** Product prices with effective dates  
**Owner:** PRICING

**Key Attributes:**
- `id` - Primary key (bigserial)
- `tenant_id` - Foreign key to tenants
- `product_id` - Foreign key to products
- `rate` - Price rate
- `effective_date` - Effective date
- `status` - Active/Deleted status

**Business Rules:**
- Prices are scoped to tenant
- Product can have multiple prices (historical)
- Latest effective price is used (EffectiveDate <= current date)
- Price lookup: WHERE EffectiveDate <= CURDATE() ORDER BY EffectiveDate DESC LIMIT 1

---

### SHARED Entities

#### Cost Head

**Entity:** `cost_heads`  
**Purpose:** Cost categorization for costing engine  
**Owner:** SHARED

**Key Attributes:**
- `id` - Primary key (bigserial)
- `code` - Cost head code (e.g., 'OEM_MATERIAL', 'LABOUR')
- `name` - Cost head name
- `category` - Cost head category (MATERIAL, LABOUR, OTHER)
- `priority` - Mapping priority
- `description` - Description
- `is_active` - Active status

**Business Rules:**
- CostHead is used for cost summary grouping
- Precedence: Item override → Product default → System default
- See COSTHEAD_RULES.md for details

---

## Entity Relationships

### Relationship Diagram

```
tenants (AUTH)
  ├── users (AUTH)
  │   └── roles (AUTH) [many-to-many]
  ├── categories (CIM)
  │   ├── subcategories (CIM)
  │   │   ├── product_types (CIM)
  │   │   └── products (CIM)
  │   │       ├── prices (PRICING)
  │   │       └── quote_bom_items (QUO)
  ├── master_boms (MBOM)
  │   └── master_bom_items (MBOM)
  ├── quotations (QUO)
  │   ├── quote_panels (QUO)
  │   │   └── quote_boms (QUO)
  │   │       ├── quote_boms (QUO) [self-reference, hierarchy]
  │   │       └── quote_bom_items (QUO)
  │   │           ├── products (CIM)
  │   │           └── cost_heads (SHARED)
  └── cost_heads (SHARED)
```

### Key Relationships

#### AUTH Relationships
- `users.tenant_id` → `tenants.id`
- `roles.tenant_id` → `tenants.id`
- `user_roles.user_id` → `users.id`
- `user_roles.role_id` → `roles.id`

#### CIM Relationships
- `products.tenant_id` → `tenants.id`
- `products.category_id` → `categories.id`
- `products.cost_head_id` → `cost_heads.id` (optional, future)
- `l1_intent_lines.tenant_id` → `tenants.id`
- `l1_intent_lines.category_id` → `categories.id`
- `l1_intent_lines.product_type_id` → `product_types.id`
- `l1_intent_lines.make_id` → `makes.id` (nullable)
- `l1_intent_lines.series_id` → `series.id` (nullable)
- `l1_intent_lines.line_group_id` → `l1_line_groups.id` (nullable)
- `l1_attributes.tenant_id` → `tenants.id`
- `l1_attributes.l1_intent_line_id` → `l1_intent_lines.id`
- `l1_line_groups.tenant_id` → `tenants.id`
- `catalog_skus.tenant_id` → `tenants.id`
- `l1_l2_mappings.tenant_id` → `tenants.id`
- `l1_l2_mappings.l1_intent_line_id` → `l1_intent_lines.id`
- `l1_l2_mappings.catalog_sku_id` → `catalog_skus.id`
- **Many-to-one:** Multiple `l1_intent_lines` → same `catalog_skus` (via `l1_l2_mappings`)

#### MBOM Relationships
- `master_boms.tenant_id` → `tenants.id`
- `master_bom_items.master_bom_id` → `master_boms.id`
- `master_bom_items.product_id` → **MUST BE NULL** (G1 guardrail)

#### QUO Relationships
- `quotations.tenant_id` → `tenants.id`
- `quotations.created_by` → `users.id`
- `quote_panels.quotation_id` → `quotations.id`
- `quote_boms.quotation_id` → `quotations.id`
- `quote_boms.panel_id` → `quote_panels.id`
- `quote_boms.parent_bom_id` → `quote_boms.id` (self-reference, hierarchy)
- `quote_boms.origin_master_bom_id` → `master_boms.id` (reference only)
- `quote_boms.modified_by` → `users.id`
- `quote_bom_items.quotation_id` → `quotations.id`
- `quote_bom_items.panel_id` → `quote_panels.id`
- `quote_bom_items.bom_id` → `quote_boms.id`
- `quote_bom_items.product_id` → `products.id` (required for L2)
- `quote_bom_items.cost_head_id` → `cost_heads.id` (item override)

#### PRICING Relationships
- `prices.tenant_id` → `tenants.id`
- `prices.product_id` → `products.id` (legacy)
- `sku_prices.tenant_id` → `tenants.id`
- `sku_prices.catalog_sku_id` → `catalog_skus.id` (L2 SKU)
- `sku_prices.price_list_id` → `price_lists.id`
- `sku_prices.import_batch_id` → `import_batches.id` (nullable)

---

## Business Rules

### Core Business Rules

#### Rule 1: Multi-Tenant Isolation

**Rule:** All tables (except `tenants`) must have `tenant_id` for data isolation.

**Enforcement:**
- Database constraint: `tenant_id NOT NULL`
- Foreign key: `tenant_id → tenants.id`
- Index on `tenant_id` for filtered queries

#### Rule 2: Copy-Never-Link (Master BOM)

**Rule:** Master BOMs are always copied to quotations, never linked directly.

**Enforcement:**
- `quote_boms.origin_master_bom_id` is reference only
- Changes to Master BOM do not affect existing quotations
- Copy creates new `quote_boms` and `quote_bom_items` records

#### Rule 3: Resolution Status Rules

**Rule:** 
- Master BOM: L0/L1 only, ProductId MUST be NULL (G1)
- Production BOM: L2 only, ProductId required (G2)

**Enforcement:**
- G1 Guardrail: Model boot hook forces ProductId = NULL for L0/L1
- G2 Guardrail: Validation requires ProductId for L2
- See VALIDATION_GUARDRAILS_G1_G7.md

#### Rule 4: Costing Calculation

**Rule:** All roll-up costs = SUM(Component AmountTotal), NO multipliers at roll-up level.

**Enforcement:**
- Component: `AmountTotal = NetRate × TotalQty`
- BOM: `BOM_TotalCost = sum(Component AmountTotal)`
- Panel: `Panel_TotalCost = sum(Component AmountTotal)`
- Quotation: `Quotation_TotalCost = sum(Component AmountTotal)`

#### Rule 5: Locking Prevents Deletion

**Rule:** If `is_locked = true`, item cannot be deleted.

**Enforcement:**
- DeletionPolicyService checks `is_locked` before deletion
- Locking applies at line-item level in MVP
- See LOCKING_POLICY.md

#### Rule 6: CostHead Precedence

**Rule:** CostHead resolution: Item override → Product default → System default.

**Enforcement:**
- Resolution algorithm checks precedence order
- See COSTHEAD_RULES.md

#### Rule 7: L1/L2 Differentiation and Explosion

**Rule:** 
- L2 = Commercial truth only (SKU-pure, one row per OEM catalog number)
- L1 = Engineering interpretation (carries all engineering meaning)
- Multiple L1 lines can map to the same L2 SKU (many-to-one)
- Price lives at L2 SKU level
- L1 → L2 explosion: Resolve base SKU + feature SKUs (if ADDON required)

**Enforcement:**
- L2 import: Only SKU-commercial fields allowed (no Duty, Rating, Voltage, etc.)
- L1 derivation: System derives L1 lines from L2 using engineering rules
- G8 Guardrail: L1-SKU reuse is allowed and expected
- Explosion logic: FOR EACH L1 → Resolve base SKU + Resolve feature SKUs (if ADDON)
- See L1_L2_EXPLOSION_LOGIC.md for detailed rules

#### Rule 8: L1 Validation and SKU Reuse

**Rule:** 
- Multiple L1 lines can legally map to the same L2 SKU
- Same SKU can serve multiple L1 interpretations (e.g., AC1 and AC3 ratings)
- Engineers validate attributes and interpretations, not SKUs or prices
- SKU reuse is expected and correct behavior

**Enforcement:**
- G8 Guardrail: L1 validation rules must allow SKU reuse
- UI must not assume 1 L1 → 1 SKU
- Validation: Check L1 attributes, not SKU uniqueness
- See VALIDATION_GUARDRAILS_G1_G8.md for G8 rule details

---

## Supporting Documents

This Data Dictionary references the following supporting documents:

### 1. Validation Guardrails

**Document:** `VALIDATION_GUARDRAILS_G1_G7.md`

**Purpose:** Defines the seven validation guardrails (G1-G7) for data integrity.

**Key Rules:**
- G1: Master BOM rejects ProductId
- G2: Production BOM requires ProductId
- G3: IsPriceMissing normalizes Rate/Net/Amount
- G4: RateSource consistency rules
- G5: UNRESOLVED normalization rules
- G6: FIXED_NO_DISCOUNT forces Discount=0
- G7: Discount is percentage-based (0-100)
- G8: L1-SKU reuse is allowed and expected (many-to-one mapping)

---

### 2. Locking Policy

**Document:** `LOCKING_POLICY.md`

**Purpose:** Defines locking semantics for deletion protection.

**Key Rules:**
- MVP: Locking at line-item level (`quote_bom_items.is_locked`)
- Lock prevents deletion (not edits in MVP)
- Lock state transitions and permissions

---

### 3. CostHead Rules

**Document:** `COSTHEAD_RULES.md`

**Purpose:** Defines CostHead entity, precedence order, and mapping rules.

**Key Rules:**
- Precedence: Item override → Product default → System default
- CostHead resolution algorithm
- Cost summary grouping

---

### 4. Module Ownership Matrix

**Document:** `MODULE_OWNERSHIP_MATRIX.md`

**Purpose:** Maps every table to its owner module.

**Key Rules:**
- Single owner per table
- Owner approves changes
- Foreign keys require coordination

---

### 5. Naming Conventions

**Document:** `NAMING_CONVENTIONS.md`

**Purpose:** Defines naming standards for tables, columns, FKs, enums, timestamps.

**Key Rules:**
- Tables: snake_case, plural
- Columns: snake_case, singular
- Foreign keys: `{table_singular}_id`
- Enums: UPPER_SNAKE_CASE
- Timestamps: `{action}_at`
- IDs: bigserial (UUID option for future)

---

### 6. AI Scope Declaration

**Purpose:** Defines the scope of AI-related entities and features in Phase 5.

**Phase 5 Scope:**
- **Schema Reservation Only:** AI-related tables are defined in schema design for future implementation
- **Implementation Status:** Deferred to Post-Phase 5 implementation
- **Tables Reserved:** `ai_call_logs` table structure is defined in schema but not implemented in MVP

**Business Rules:**
- AI entities are reserved in schema for audit and learning capabilities
- No AI business logic or services are implemented in Phase 5 MVP
- AI features are planned for Post-Phase 5 implementation
- Schema design includes `ai_call_logs` table structure to support future AI features

**References:**
- See `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` for AI implementation roadmap
- See Schema Design (Step 2) for AI table definitions

---

## Change Log

### v1.1 (2025-01-27) - UPDATED

**Updates:**
- Added L1/L2 entities (l1_intent_lines, l1_attributes, l1_line_groups, catalog_skus, sku_prices, l1_l2_mappings)
- Added L1/L2 differentiation rules (Rule 7)
- Added L1 validation and SKU reuse rules (Rule 8)
- Added G8 guardrail reference
- Updated entity relationships to include L1/L2 mappings
- Updated pricing relationships to include L2 price model

**Change Reason:** Phase 5 impact assessment - L1/L2 differentiation and SKU reuse requirements

---

### v1.0 (2025-01-27) - FROZEN

**Initial Release:**
- Core entity definitions
- Entity relationships
- Business rules
- References to supporting documents

**Freeze Date:** 2025-01-27  
**Freeze Reason:** Frozen after Phase-5 Senate review. All Step-1 requirements verified and approved.

---

## Next Steps

1. **Review:** Phase 5 Senate reviews all 6 documents
2. **Approve:** Stakeholder approval for freeze
3. **Freeze:** Mark as FROZEN after approval
4. **Step 2:** Proceed to Schema Design (Step 2)

---

**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Frozen:** 2025-01-27 after Phase-5 Senate review

