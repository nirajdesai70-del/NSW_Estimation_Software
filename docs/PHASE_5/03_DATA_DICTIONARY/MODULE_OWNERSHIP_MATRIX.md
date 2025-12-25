# Module Ownership Matrix

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Purpose:** Map every database table to its owner module for change control and responsibility

---

## Purpose

This document maps every table in the NSW schema to its owner module. Module ownership determines:
- Who is responsible for schema changes
- Who approves modifications
- Who maintains business logic
- Who handles data integrity

**Modules:**
- **AUTH** - Authentication, Authorization, Tenants, Users, Roles
- **CIM** - Component/Item Master (Categories, Products, Attributes)
- **MBOM** - Master BOM (Templates)
- **QUO** - Quotation (Quotations, Panels, BOMs, Items)
- **PRICING** - Pricing (Price Lists, Prices)
- **AUDIT** - Audit Trail (Change Logs, Audit Logs)
- **AI** - AI Features (AI Call Logs, Patterns, Distributions)

---

## Table Ownership Mapping

### AUTH Module

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `tenants` | Multi-tenant isolation | AUTH | Root tenant entity |
| `users` | User accounts | AUTH | User authentication |
| `roles` | Role definitions | AUTH | Role-based access control |
| `permissions` | Permission definitions | AUTH | Permission matrix |
| `user_roles` | User-role assignments | AUTH | Many-to-many relationship |
| `role_permissions` | Role-permission assignments | AUTH | Many-to-many relationship |

**AUTH Module Responsibility:**
- User authentication and authorization
- Multi-tenant data isolation
- Role and permission management
- Access control policies

---

### CIM Module (Component/Item Master)

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `categories` | Product categories | CIM | Top-level taxonomy |
| `subcategories` | Product subcategories | CIM | Second-level taxonomy |
| `product_types` | Product types (items) | CIM | Third-level taxonomy |
| `attributes` | Product attributes | CIM | Attribute definitions |
| `category_attributes` | Category-attribute mapping | CIM | Which attributes apply to which categories |
| `products` | Product master | CIM | Buyable products |
| `product_attributes` | Product-attribute values | CIM | Product attribute data |
| `makes` | Make/brand | CIM | Vendor brands |
| `series` | Product series | CIM | Product lines |
| `generic_products` | Generic product references | CIM | Generic-specific relationships |

**CIM Module Responsibility:**
- Product catalog management
- Taxonomy (Category/SubCategory/Type) management
- Attribute schema and values
- Product master data integrity
- Make/Series management

---

### MBOM Module (Master BOM)

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `master_boms` | Master BOM templates | MBOM | Reusable BOM templates |
| `master_bom_items` | Master BOM line items | MBOM | Template items (L0/L1 only) |

**MBOM Module Responsibility:**
- Master BOM template creation and management
- Template integrity (L0/L1 only, no ProductId)
- Template application to quotations (read-only contract)
- Copy-never-link rule enforcement

---

### QUO Module (Quotation)

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `quotations` | Quotation headers | QUO | Top-level quotation entity |
| `quote_panels` | Panels/Sales items | QUO | Panel-level items |
| `quote_boms` | BOMs/Feeders | QUO | BOM hierarchy (Level 0/1/2) |
| `quote_bom_items` | BOM line items | QUO | Component items (L2 resolved) |
| `quotation_revisions` | Quotation revisions | QUO | Revision tracking |
| `quotation_status_history` | Status change history | QUO | Status workflow tracking |

**QUO Module Responsibility:**
- Quotation creation and management
- Panel/BOM/Item hierarchy
- BOM application from Master BOM
- Pricing and costing calculations
- Revision management
- Status workflow

---

### PRICING Module

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `price_lists` | Price list headers | PRICING | Price list definitions |
| `prices` | Product prices | PRICING | Price entries with effective dates |
| `price_list_versions` | Price list versioning | PRICING | Historical price tracking |

**PRICING Module Responsibility:**
- Price list management
- Product pricing
- Price effective date tracking
- Price history and versioning
- Price lookup for quotations

---

### AUDIT Module

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `audit_logs` | General audit trail | AUDIT | System-wide audit logging |
| `bom_change_logs` | BOM change history | AUDIT | BOM modification tracking |
| `quotation_change_logs` | Quotation change history | AUDIT | Quotation modification tracking |

**AUDIT Module Responsibility:**
- Audit trail management
- Change logging (who/what/when/before/after)
- Compliance and audit reporting
- Historical data tracking

---

### AI Module

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `ai_call_logs` | AI API call logs | AI | AI feature audit trail |
| `selection_patterns` | Component selection patterns | AI | Learned patterns for suggestions |
| `price_distributions` | Price statistical distributions | AI | Price sanity checking |
| `co_occurrences` | Component co-occurrence patterns | AI | Missing component detection |
| `discount_behaviors` | Historical discount patterns | AI | Discount validation |
| `substitution_matrices` | Component substitution rules | AI | Option building |

**AI Module Responsibility:**
- AI feature implementation (Post-Phase 5)
- AI pattern learning and storage
- AI call logging and audit
- AI rule management

**Note:** AI tables are **Phase-5 schema reservation** for Post-Phase-5 implementation. Schema is designed but not implemented in Phase 5.

---

### SHARED/Cross-Module Tables

| Table Name | Purpose | Owner | Notes |
|------------|---------|-------|-------|
| `cost_heads` | Cost head definitions | SHARED | Used by QUO for costing, but master data |
| `projects` | Project management | SHARED | Used by QUO, but separate entity |
| `customers` | Customer master | SHARED | Used by QUO, but separate entity (future) |

**SHARED Module Responsibility:**
- Cross-module master data
- Shared entities used by multiple modules
- Coordination required for changes

---

## Ownership Rules

### Rule 1: Single Owner Per Table

**Rule:** Each table has exactly one owner module.

**Enforcement:**
- Ownership is explicit and documented
- Changes require owner module approval
- Cross-module changes require coordination

### Rule 2: Owner Approves Changes

**Rule:** Owner module must approve all schema changes to their tables.

**Enforcement:**
- Schema changes require owner review
- Foreign key additions require both owner approvals
- Index changes require owner approval

### Rule 3: Owner Maintains Business Logic

**Rule:** Owner module maintains business logic for their tables.

**Enforcement:**
- Business rules are owned by module
- Validation logic is owned by module
- Service layer is owned by module

### Rule 4: Foreign Keys Require Coordination

**Rule:** Foreign keys between modules require coordination.

**Enforcement:**
- FK from QUO to CIM requires both approvals
- FK from QUO to MBOM requires both approvals
- FK from QUO to PRICING requires both approvals

---

## Module Boundaries

### AUTH ↔ CIM

**Boundary:** No direct coupling. CIM uses AUTH for user context (tenant_id).

**FKs:**
- `products.created_by` → `users.id` (optional)
- `categories.created_by` → `users.id` (optional)

### AUTH ↔ QUO

**Boundary:** QUO uses AUTH for user context and permissions.

**FKs:**
- `quotations.created_by` → `users.id`
- `quote_bom_items.modified_by` → `users.id`

### CIM ↔ QUO

**Boundary:** QUO references CIM products (read-only catalog lookup).

**FKs:**
- `quote_bom_items.product_id` → `products.id`
- `quote_bom_items.make_id` → `makes.id`
- `quote_bom_items.series_id` → `series.id`

**Contract:** QUO reads CIM products via catalog lookup contract. CIM owns product master data.

### MBOM ↔ QUO

**Boundary:** QUO applies MBOM templates (copy-never-link).

**FKs:**
- `quote_boms.origin_master_bom_id` → `master_boms.id` (reference only)

**Contract:** QUO reads MBOM templates via template snapshot contract. MBOM owns template data. QUO owns application logic.

### PRICING ↔ QUO

**Boundary:** QUO references PRICING for rate lookup.

**FKs:**
- `quote_bom_items.rate_source` references pricing (indirect)

**Contract:** QUO reads prices via price lookup contract. PRICING owns price master data.

### QUO ↔ AUDIT

**Boundary:** QUO writes to AUDIT for change tracking.

**FKs:**
- `bom_change_logs.bom_id` → `quote_boms.id`
- `quotation_change_logs.quotation_id` → `quotations.id`

**Contract:** QUO writes audit logs. AUDIT owns audit trail management.

### QUO ↔ AI

**Boundary:** QUO writes to AI for AI feature data (Post-Phase 5).

**FKs:**
- `ai_call_logs.quotation_id` → `quotations.id`
- `ai_call_logs.bom_item_id` → `quote_bom_items.id`

**Contract:** QUO writes AI logs. AI owns AI feature logic (Post-Phase 5).

---

## Change Control Process

### Schema Change Request

1. **Identify Owner:** Determine table owner from this matrix
2. **Request Approval:** Get owner module approval
3. **Coordinate FKs:** If FK crosses modules, get both approvals
4. **Document Change:** Update schema documentation
5. **Update Matrix:** Update this matrix if ownership changes

### Cross-Module Changes

**Example:** Adding FK from `quote_bom_items` to `cost_heads`.

**Process:**
1. Identify owners: QUO (quote_bom_items) and SHARED (cost_heads)
2. Get QUO approval for FK addition
3. Get SHARED approval for FK target
4. Coordinate change timing
5. Document in both modules

---

## References

- `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` - Section 1.6 (Module Ownership)
- `SPEC_5_FREEZE_GATE_CHECKLIST.md` - Section 6 (Module Ownership Mapping)
- `FILE_OWNERSHIP.md` - Code-level ownership mapping

---

## Change Log

### v1.0 (2025-01-27) - FROZEN

- Initial module ownership matrix for all tables

**Freeze Date:** 2025-01-27  
**Freeze Reason:** Frozen after Phase-5 Senate review. All Step-1 requirements verified and approved.

---

**Status:** FROZEN  
**Frozen:** 2025-01-27 after Phase-5 Senate review

