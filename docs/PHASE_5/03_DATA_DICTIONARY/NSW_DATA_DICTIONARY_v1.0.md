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
**Purpose:** Buyable product master  
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
- `prices.product_id` → `products.id`

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

