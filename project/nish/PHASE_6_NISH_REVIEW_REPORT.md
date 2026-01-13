# Phase-6 Nish Review Report

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** COMPLETE  
**Purpose:** Extract Nish legacy system information, compare with Phase 1-4 captured data, and create Phase-6 execution sequence

---

## Executive Summary

This report extracts business flows, data model, and application usage patterns from **Project/Nish** (legacy system) based on:
- Phase 1-4 documentation analysis
- Phase 5 NSW Schema Canon v1.0 (FROZEN)
- Phase 5 NSW Data Dictionary v1.0 (FROZEN)

**Key Finding:** Phase 1-4 captured comprehensive Nish/NEPL system information. This report synthesizes that information and maps it to NSW Phase 5 frozen schema to create Phase-6 execution sequence.

**Critical Rule:** Nish is used as **requirements reference only**. NSW Schema Canon v1.0 remains the authoritative source. No Nish DB migration. No schema changes to NSW.

---

## Deliverable 1: Nish Baseline Map

### 1.1 Business Flows (Extracted from Phase 1-4)

#### A. Company/Tenant Setup
**From Phase 1-4:**
- **NEPL Structure:** Projects → Clients (implicit tenant)
- **Flow:** 
  1. Create Project
  2. Assign Client to Project
  3. Project contains Panels
- **Screens:** Project List → Project Create → Project Detail
- **Tables Used:** `projects`, `clients` (implicit)

**Nish Reality:**
- No explicit tenant table in legacy
- Multi-tenancy handled via project/client separation
- **Gap:** No tenant isolation layer

---

#### B. Admin Panel: Roles + Permissions + Users/Team
**From Phase 1-4:**
- **NEPL Structure:** Users exist but roles/permissions not explicitly documented
- **Flow:**
  1. User management (implicit)
  2. No explicit role assignment documented
- **Screens:** User menu in header (mentioned but not detailed)
- **Tables Used:** `users` (assumed)

**Nish Reality:**
- Basic user authentication
- **Gap:** No RBAC system documented
- **Gap:** No role/permission tables in Phase 1-4 capture

---

#### C. Customer Onboarding
**From Phase 1-4:**
- **NEPL Structure:** Clients linked to Projects
- **Flow:**
  1. Create Project
  2. Assign Client Name (required field)
  3. Client appears in Project Detail
- **Screens:** Project Create Form → Client Name field
- **Tables Used:** `clients` (linked to `projects`)

**Nish Reality:**
- Client is required field in Project creation
- Client name stored in project (may be denormalized)
- **Gap:** No standalone customer master management screen documented

---

#### D. Project / Quotation Creation
**From Phase 1-4:**
- **NEPL Structure:** Project → Panel → Feeder → BOM → Quotation
- **Flow:**
  1. Create Project (with Client)
  2. Create Panel (under Project)
  3. Create Feeder (under Panel)
  4. Create BOM (under Feeder)
  5. Add Items/Components to BOM
  6. Generate Quotation from BOM
- **Screens:**
  - Project List → Project Create
  - Panel List → Panel Create
  - Feeder List → Feeder Create
  - BOM Detail → Add Item/Component
  - BOM Detail → Generate Quotation
- **Tables Used:** 
  - `projects`, `panels`, `feeders`, `boms`, `bom_items`, `quotations`, `quotation_items`

**Nish Reality:**
- Clear hierarchy: Project → Panel → Feeder → BOM → Quotation
- BOM can contain Items OR Components (mutually exclusive)
- Quotation can be generated from BOM or created manually
- **Key Flow:** BOM is the central artifact

---

#### E. Item/Master Data Management
**From Phase 1-4:**
- **NEPL Structure:** Category → Subcategory → Type → Attribute → Item
- **Flow:**
  1. Manage Categories (Masters/Categories)
  2. Manage Subcategories (filtered by Category)
  3. Manage Types (filtered by Subcategory)
  4. Manage Attributes (filtered by Type)
  5. Create Items (linked to Category/Subcategory/Type)
  6. Items have Item Attributes (via junction table)
- **Screens:**
  - Masters → Categories
  - Masters → Subcategories
  - Masters → Types
  - Masters → Attributes
  - Items → Item List → Item Create
- **Tables Used:**
  - `categories`, `sub_categories`, `types`, `attributes`, `items`, `item_attributes`

**Nish Reality:**
- Hierarchical master data structure
- Items are catalog entries
- Components are separate (not in hierarchy)
- **Key Distinction:** Items vs Components (both can be in BOMs)

---

#### F. BOM Building + Reuse + Editability
**From Phase 1-4:**
- **NEPL Structure:** Master BOM (template) → Proposal BOM (instance)
- **Flow:**
  1. Create Master BOM (template with L1/Generic products)
  2. Create Proposal BOM from Master BOM (instance with L2/Specific products)
  3. Edit Proposal BOM items (quantity, price)
  4. BOM items can be Items OR Components
- **Screens:**
  - BOM Detail → Add Item
  - BOM Detail → Add Component
  - BOM Detail → Edit Item
  - BOM Detail → Delete Item
- **Tables Used:**
  - `master_boms`, `master_bom_items`, `proposal_boms`, `proposal_bom_items`
  - OR: `boms`, `bom_items` (depending on version)

**Nish Reality:**
- Master BOM = Template (L1 products)
- Proposal BOM = Instance (L2 products)
- BOM items editable until quotation finalized
- **Key Rule:** Master BOM uses L1, Proposal/Quotation BOM uses L2

---

#### G. Pricing & Discount Approvals
**From Phase 1-4:**
- **NEPL Structure:** Base Price on Items/Components → Quotation Pricing
- **Flow:**
  1. Items/Components have `base_price`
  2. BOM Items have `unit_price` (can override base_price)
  3. Quotation Items have `unit_price` (can override)
  4. Totals calculated: quantity × unit_price
- **Screens:**
  - Item Master → Base Price field
  - BOM Detail → Unit Price (editable)
  - Quotation Detail → Unit Price (editable)
- **Tables Used:**
  - `items.base_price`, `components.base_price`
  - `bom_items.unit_price`, `quotation_items.unit_price`

**Nish Reality:**
- Simple pricing model: base_price → unit_price override
- No explicit discount rules documented
- No approval workflow documented
- **Gap:** No price list management
- **Gap:** No discount rule engine

---

#### H. Audit / History / Export
**From Phase 1-4:**
- **NEPL Structure:** Created/Updated timestamps on all tables
- **Flow:**
  1. System tracks `created_at`, `updated_at` on all entities
  2. No explicit audit log table documented
  3. No history/versioning documented
- **Screens:** Not explicitly documented
- **Tables Used:** All tables have `created_at`, `updated_at`

**Nish Reality:**
- Basic timestamp tracking
- **Gap:** No audit log table
- **Gap:** No history/versioning for BOM edits
- **Gap:** No export functionality documented

---

### 1.2 Data Model (Extracted from Phase 1-4)

#### Table Groups

**A. Auth / Security (Minimal)**
- `users` - User accounts (basic, no roles documented)

**B. Master Data**
- `categories` - Top-level classification
- `sub_categories` - Second-level (linked to category)
- `types` - Third-level (linked to subcategory)
- `attributes` - Fourth-level (linked to type)
- `items` - Catalog items (linked to category/subcategory/type)
- `components` - Component master (separate from items)
- `item_attributes` - Junction table (items ↔ attributes)

**C. Project / Customer**
- `projects` - Project master
- `clients` - Client master (linked to projects)
- `panels` - Panel master (linked to project)
- `feeders` - Feeder master (linked to panel)

**D. BOM**
- `boms` - BOM master (linked to feeder)
- `bom_items` - BOM line items (links to item OR component)
- `master_boms` - Master BOM templates (L1 products)
- `master_bom_items` - Master BOM line items (L1 only)
- `proposal_boms` - Proposal BOM instances (L2 products)
- `proposal_bom_items` - Proposal BOM line items (L2 only)

**E. Quotation**
- `quotations` - Quotation header (linked to project)
- `quotation_items` - Quotation line items (links to BOM/item/component)

**F. Pricing (Minimal)**
- No explicit price list table documented
- Pricing stored on items/components (`base_price`)
- Pricing stored on BOM/quotation items (`unit_price`)

**G. Audit (Minimal)**
- No audit log table documented
- Only `created_at`, `updated_at` timestamps

---

### 1.3 How the App Uses Tables (From Phase 1-4 UI Behavior Map)

#### Write Operations (Which screens write to which tables)

| Screen | Tables Written | Operation |
|--------|---------------|-----------|
| Project Create | `projects` | INSERT |
| Project Edit | `projects` | UPDATE |
| Panel Create | `panels` | INSERT |
| Feeder Create | `feeders` | INSERT |
| BOM Create | `boms` | INSERT |
| BOM Item Add | `bom_items` | INSERT |
| BOM Item Edit | `bom_items` | UPDATE |
| BOM Item Delete | `bom_items` | DELETE |
| Item Create | `items` | INSERT |
| Component Create | `components` | INSERT |
| Category Create | `categories` | INSERT |
| Quotation Generate | `quotations`, `quotation_items` | INSERT |
| Quotation Item Add | `quotation_items` | INSERT |

#### Read Operations (Which screens read from which tables)

| Screen | Tables Read | Purpose |
|--------|------------|---------|
| Dashboard | `projects`, `quotations` | List recent items |
| Project List | `projects` | List all projects |
| Project Detail | `projects`, `panels`, `quotations` | Show project info |
| Panel List | `panels`, `projects` | List panels with project names |
| Feeder List | `feeders`, `panels` | List feeders with panel names |
| BOM Detail | `boms`, `bom_items`, `items`, `components` | Show BOM with item details |
| Item List | `items`, `categories`, `sub_categories`, `types` | List items with taxonomy |
| Item Create Form | `categories`, `sub_categories`, `types` | Dropdowns for selection |
| Quotation List | `quotations`, `projects` | List quotations |
| Quotation Detail | `quotations`, `quotation_items`, `items`, `components` | Show quotation |

#### State Transitions

| Entity | States | Transition Trigger |
|--------|--------|-------------------|
| BOM | draft → active → locked | User action (not documented) |
| Quotation | draft → sent → accepted/rejected | User action (not documented) |
| Project | active → inactive | Soft delete (is_active flag) |

---

## Deliverable 2: Nish → NSW Mapping Sheet

### 2.1 Entity Mapping Matrix

| Nish Entity | Nish Table(s) | NSW Entity | NSW Table(s) | Mapping Notes | Status |
|-------------|---------------|------------|---------------|---------------|--------|
| **AUTH** |
| User | `users` | User | `users` | Direct mapping, but NSW adds tenant_id | ✅ Mapped |
| Role | (not in Nish) | Role | `roles` | NEW in NSW - RBAC system | 🆕 New |
| Tenant | (not in Nish) | Tenant | `tenants` | NEW in NSW - multi-tenant isolation | 🆕 New |
| **MASTER DATA** |
| Category | `categories` | Category | `categories` | Direct mapping, NSW adds tenant_id | ✅ Mapped |
| Subcategory | `sub_categories` | Subcategory | `subcategories` | Direct mapping, name change | ✅ Mapped |
| Type | `types` | Product Type | `product_types` | Direct mapping, NSW adds nullable subcategory | ✅ Mapped |
| Attribute | `attributes` | Attribute | `attributes` | Direct mapping, NSW adds category-level schema | ✅ Mapped |
| Item | `items` | Product (Legacy) | `products` | Direct mapping, but marked LEGACY in NSW | ⚠️ Legacy |
| Item | `items` | L1 Intent Line | `l1_intent_lines` | Nish items → NSW L1 (engineering meaning) | 🔄 Transform |
| Item | `items` | L2 SKU | `catalog_skus` | Nish items → NSW L2 (commercial SKU) | 🔄 Transform |
| Component | `components` | (no direct equivalent) | - | Components may map to L2 SKUs or remain separate | ❓ TBD |
| **BOM** |
| Master BOM | `master_boms` | Master BOM | `master_boms` | Direct mapping, NSW enforces L0/L1 only | ✅ Mapped |
| Master BOM Item | `master_bom_items` | Master BOM Item | `master_bom_items` | Direct mapping, NSW rejects product_id (G-01) | ✅ Mapped |
| Proposal BOM | `proposal_boms` | (no direct equivalent) | - | Proposal BOM → Quote BOM in NSW | 🔄 Transform |
| Proposal BOM Item | `proposal_bom_items` | Quote BOM Item | `quote_bom_items` | Proposal → Quote transformation | 🔄 Transform |
| **QUOTATION** |
| Quotation | `quotations` | Quotation | `quotations` | Direct mapping, NSW adds tenant_id, status enum | ✅ Mapped |
| Quotation Item | `quotation_items` | Quote BOM Item | `quote_bom_items` | Consolidated with Proposal BOM Items | 🔄 Transform |
| **PROJECT/CUSTOMER** |
| Project | `projects` | Project | `projects` | Direct mapping, NSW adds tenant_id | ✅ Mapped |
| Client | `clients` | Customer | `customers` | Direct mapping, name change | ✅ Mapped |
| Panel | `panels` | Quote Panel | `quote_panels` | Panel moved under quotation in NSW | 🔄 Transform |
| Feeder | `feeders` | Quote BOM (level=0) | `quote_boms` | Feeder becomes level=0 BOM in NSW | 🔄 Transform |
| BOM | `boms` | Quote BOM (level=1/2) | `quote_boms` | BOM becomes level=1/2 in NSW hierarchy | 🔄 Transform |
| **PRICING** |
| Base Price | `items.base_price` | SKU Price | `sku_prices` | Pricing moves to L2 SKU level in NSW | 🔄 Transform |
| Unit Price | `bom_items.unit_price` | Quote BOM Item Rate | `quote_bom_items.rate` | Direct mapping, but NSW adds rate_source enum | ✅ Mapped |
| (not in Nish) | - | Price List | `price_lists` | NEW in NSW - price list management | 🆕 New |
| (not in Nish) | - | Discount Rule | `discount_rules` | NEW in NSW - discount rule engine | 🆕 New |
| **AUDIT** |
| Timestamps | `*.created_at`, `*.updated_at` | Timestamps | `*.created_at`, `*.updated_at` | Direct mapping | ✅ Mapped |
| (not in Nish) | - | Audit Log | `audit_logs` | NEW in NSW - append-only audit trail | 🆕 New |

### 2.2 Key Transformations

#### Transformation 1: Item → L1/L2 Split
- **Nish:** Single `items` table with category/subcategory/type
- **NSW:** Split into:
  - `l1_intent_lines` - Engineering meaning (Duty, Rating, Voltage, etc.)
  - `catalog_skus` - Commercial SKU (Make, OEM catalog number)
  - `l1_l2_mappings` - Bridge table (many L1 → one L2)

#### Transformation 2: BOM Hierarchy Restructure
- **Nish:** Project → Panel → Feeder → BOM → BOM Items
- **NSW:** Quotation → Panel → BOM (level=0/1/2) → BOM Items
- **Key Change:** Feeder becomes level=0 BOM, BOM becomes level=1/2

#### Transformation 3: Pricing Model Upgrade
- **Nish:** Base price on items, unit price on BOM items
- **NSW:** Price list → SKU prices (L2 level) → Quote BOM item rates (with rate_source enum)

#### Transformation 4: Multi-Tenant Isolation
- **Nish:** No tenant concept
- **NSW:** All tables have `tenant_id` (except `tenants`)

---

## Deliverable 3: Phase-6 Execution Sequence

### 3.1 Recommended Sequence (Based on Nish Flow Analysis)

**Sequence Rationale:** Derived from Nish business flows, mapped to NSW frozen schema, ordered by dependency.

#### **Step 1: Tenant/Company Setup** ✅ FOUNDATION
**Why First:** All other entities depend on tenant isolation.

**Nish Reference:**
- No explicit tenant in Nish (implicit via projects/clients)
- **NSW Requirement:** Multi-tenant isolation mandatory

**NSW Implementation:**
- Create `tenants` table (already in schema)
- Tenant creation UI
- Tenant selection/context in UI

**Dependencies:** None (root entity)

**Deliverables:**
- Tenant creation form
- Tenant context selector
- Tenant isolation enforcement in API

---

#### **Step 2: Roles/Permissions + Team** ✅ FOUNDATION
**Why Second:** User management needed before any data entry.

**Nish Reference:**
- Basic users exist, no RBAC documented
- **NSW Requirement:** RBAC system (roles, permissions, user_roles)

**NSW Implementation:**
- Create `roles` table (already in schema)
- Create `user_roles` junction table (already in schema)
- Role management UI
- User creation with role assignment
- Permission enforcement in API

**Dependencies:** Step 1 (tenants)

**Deliverables:**
- Role management UI
- User creation/editing form with role assignment
- Permission middleware/guards

---

#### **Step 3: Customer Onboarding** ✅ FOUNDATION
**Why Third:** Customers needed before projects/quotations.

**Nish Reference:**
- Clients linked to projects
- Client name required in project creation
- **NSW Requirement:** Customer master (`customers` table)

**NSW Implementation:**
- Create `customers` table (already in schema)
- Customer list UI
- Customer create/edit form
- Customer selection in quotation creation

**Dependencies:** Step 1 (tenants)

**Deliverables:**
- Customer list screen
- Customer create/edit form
- Customer dropdown in quotation form

---

#### **Step 4: Quotation Shell (Create/List/View)** ✅ CORE WORKFLOW
**Why Fourth:** Quotation is the central commercial artifact.

**Nish Reference:**
- Quotations linked to projects
- Quotation number auto-generated
- Quotation status (draft, sent, accepted, rejected)
- **NSW Requirement:** Quotation workspace (`quotations` table)

**NSW Implementation:**
- Create `quotations` table (already in schema)
- Quotation list UI
- Quotation create form (customer selection, quote_no generation)
- Quotation detail view (header only, no BOM yet)

**Dependencies:** Step 1 (tenants), Step 3 (customers)

**Deliverables:**
- Quotation list screen
- Quotation create form
- Quotation detail view (header)
- Quote number generation logic

---

#### **Step 5: Master Data Ingestion (Import/Seed)** ✅ CATALOG FOUNDATION
**Why Fifth:** Master data needed before BOM building.

**Nish Reference:**
- Category → Subcategory → Type → Attribute hierarchy
- Items with category/subcategory/type
- **NSW Requirement:** Category tree + L1/L2 catalog

**NSW Implementation:**
- Create category tree (`categories`, `subcategories`, `product_types`)
- Create attribute schema (`attributes`, `attribute_options`)
- Import/seed L1 intent lines (`l1_intent_lines`, `l1_attributes`)
- Import/seed L2 SKUs (`catalog_skus`)
- Create L1→L2 mappings (`l1_l2_mappings`)

**Dependencies:** Step 1 (tenants)

**Deliverables:**
- Category management UI
- Attribute schema management
- L1 intent line import tool
- L2 SKU import tool
- L1→L2 mapping tool

---

#### **Step 6: BOM Layer (Reuse/Edit Rules)** ✅ CORE WORKFLOW
**Why Sixth:** BOM building is core estimation activity.

**Nish Reference:**
- Master BOM (template) → Proposal BOM (instance)
- BOM items editable until quotation finalized
- **NSW Requirement:** Master BOM + Quote BOM hierarchy

**NSW Implementation:**
- Create Master BOM UI (`master_boms`, `master_bom_items`)
- Create Quote BOM hierarchy UI (`quote_panels`, `quote_boms`, `quote_bom_items`)
- BOM item add/edit/delete
- L0 → L1 → L2 resolution UX
- BOM reuse/copy functionality

**Dependencies:** Step 1 (tenants), Step 4 (quotations), Step 5 (master data)

**Deliverables:**
- Master BOM list/create/edit
- Quote Panel create/edit
- Quote BOM (Feeder/BOM) create/edit
- Quote BOM Item add/edit/delete
- L0/L1/L2 resolution UI
- BOM copy/reuse functionality

---

#### **Step 7: Pricing + Approval Flow** ✅ COMMERCIAL LOGIC
**Why Seventh:** Pricing needed after BOM structure exists.

**Nish Reference:**
- Base price on items → unit price on BOM items
- No explicit price list or discount rules
- **NSW Requirement:** Price lists + SKU prices + discount rules

**NSW Implementation:**
- Create price list management (`price_lists`)
- Import SKU prices (`sku_prices`)
- Price resolution engine (PRICELIST / MANUAL / FIXED)
- Discount rule engine (`discount_rules`)
- Pricing approval workflow (if needed)

**Dependencies:** Step 1 (tenants), Step 5 (L2 SKUs), Step 6 (BOM items)

**Deliverables:**
- Price list management UI
- SKU price import tool
- Price resolution UI (show rate_source, allow override)
- Discount rule management UI
- Pricing approval workflow (if required)

---

#### **Step 8: Audit/Export** ✅ OPERATIONAL READINESS
**Why Eighth:** Audit and export needed after core functionality works.

**Nish Reference:**
- Only created_at/updated_at timestamps
- No audit log or export documented
- **NSW Requirement:** Audit trail + export functionality

**NSW Implementation:**
- Create audit log table (`audit_logs`)
- Audit logging middleware
- Export functionality (PDF, Excel)
- Audit log viewer UI

**Dependencies:** All previous steps

**Deliverables:**
- Audit logging infrastructure
- Audit log viewer UI
- Quotation export (PDF/Excel)
- BOM export (PDF/Excel)

---

### 3.2 Execution Dependencies Graph

```
Step 1: Tenants
  └── Step 2: Roles/Users
  └── Step 3: Customers
  └── Step 5: Master Data
      └── Step 6: BOM Layer
          └── Step 4: Quotation Shell
              └── Step 7: Pricing
                  └── Step 8: Audit/Export
```

**Note:** Step 4 (Quotation) can start after Step 3, but Step 6 (BOM) needs Step 5 (Master Data) first.

---

### 3.3 Phase-6 Execution Checklist

#### Phase-6 Gate 1: Foundation Ready
- [ ] Step 1: Tenant setup complete
- [ ] Step 2: Roles/Users complete
- [ ] Step 3: Customers complete

#### Phase-6 Gate 2: Core Workflow Ready
- [ ] Step 4: Quotation shell complete
- [ ] Step 5: Master data ingestion complete
- [ ] Step 6: BOM layer complete

#### Phase-6 Gate 3: Commercial Logic Ready
- [ ] Step 7: Pricing + approval flow complete

#### Phase-6 Gate 4: Operational Ready
- [ ] Step 8: Audit/Export complete

---

## 4. Comparison: Phase 1-4 vs Phase 5 NSW

### 4.1 What Phase 1-4 Captured

**✅ Captured:**
- Complete data structure (Category → Subcategory → Type → Attribute → Item)
- BOM hierarchy (Project → Panel → Feeder → BOM)
- Quotation structure
- UI behavior map (screens, flows, interactions)
- Master data management flows

**⚠️ Gaps in Phase 1-4:**
- No explicit tenant/role/permission structure
- No L1/L2 split documented
- No price list management
- No discount rules
- No audit log
- No multi-tenant isolation

### 4.2 What Phase 5 NSW Added

**🆕 New in NSW:**
- Multi-tenant isolation (`tenants`, `tenant_id` everywhere)
- RBAC system (`roles`, `user_roles`)
- L1/L2 split (`l1_intent_lines`, `catalog_skus`, `l1_l2_mappings`)
- Price list management (`price_lists`, `sku_prices`)
- Discount rules (`discount_rules`)
- Audit trail (`audit_logs`)
- Guardrails (G-01 to G-08)

**🔄 Transformed in NSW:**
- Item → L1 Intent Line + L2 SKU
- BOM hierarchy restructured (Feeder → level=0 BOM)
- Pricing model upgraded (base_price → SKU prices)
- Quotation structure enhanced (status enum, tax_mode)

### 4.3 Alignment Status

| Aspect | Phase 1-4 | Phase 5 NSW | Alignment |
|--------|-----------|-------------|-----------|
| Master Data Hierarchy | ✅ Captured | ✅ Enhanced | ✅ Aligned |
| BOM Structure | ✅ Captured | ✅ Restructured | ⚠️ Needs Mapping |
| Quotation Flow | ✅ Captured | ✅ Enhanced | ✅ Aligned |
| Pricing Model | ⚠️ Basic | ✅ Advanced | 🔄 Upgrade Path |
| Multi-Tenancy | ❌ Missing | ✅ Added | 🆕 New |
| RBAC | ❌ Missing | ✅ Added | 🆕 New |
| Audit | ❌ Missing | ✅ Added | 🆕 New |

---

## 5. Risks and Mitigations

### Risk 1: Nish Flow Assumptions
**Risk:** Phase 1-4 documentation may not capture all Nish flows.

**Mitigation:**
- Use Nish as reference only, not authority
- Validate flows during Phase-6 implementation
- Add missing flows as discovered

### Risk 2: L1/L2 Transformation Complexity
**Risk:** Nish items → NSW L1/L2 split is non-trivial.

**Mitigation:**
- Start with simple L1→L2 mappings
- Build mapping tool incrementally
- Validate mappings with business users

### Risk 3: BOM Hierarchy Restructure
**Risk:** Nish Project→Panel→Feeder→BOM → NSW Quotation→Panel→BOM hierarchy change.

**Mitigation:**
- Build UI that matches NSW schema (not Nish)
- Document transformation clearly
- Test with sample data

### Risk 4: Pricing Model Upgrade
**Risk:** Nish simple pricing → NSW price list/SKU prices is complex.

**Mitigation:**
- Build price import tool first
- Validate price resolution logic
- Allow manual overrides (FIXED_NO_DISCOUNT)

---

## 6. Next Steps

### Immediate Actions
1. ✅ **This Report Complete** - Nish baseline map, mapping sheet, execution sequence created
2. ⏳ **Review with Team** - Validate execution sequence with stakeholders
3. ⏳ **Lock Phase-6 Sequence** - Finalize execution order after review
4. ⏳ **Start Step 1** - Begin tenant/company setup implementation

### Phase-6 Kickoff
- Use this report as input to Phase-6 execution plan
- Reference Nish flows during implementation
- Validate NSW schema alignment continuously
- Document any deviations from this plan

---

## 7. Appendix

### A. Nish Table Inventory (From Phase 1-4)

**Auth:**
- `users`

**Master Data:**
- `categories`
- `sub_categories`
- `types`
- `attributes`
- `items`
- `components`
- `item_attributes`

**Project/Customer:**
- `projects`
- `clients`
- `panels`
- `feeders`

**BOM:**
- `boms`
- `bom_items`
- `master_boms`
- `master_bom_items`
- `proposal_boms`
- `proposal_bom_items`

**Quotation:**
- `quotations`
- `quotation_items`

**Total:** ~20 tables (estimated from Phase 1-4 documentation)

### B. NSW Table Inventory (From Phase 5)

**Total:** 34 tables across 9 modules

**Modules:**
- AUTH (4 tables)
- CIM (12 tables)
- MBOM (2 tables)
- QUO (5 tables)
- PRICING (3 tables)
- SHARED (3 tables)
- TAX (1 table)
- AUDIT (1 table)
- AI (1 table)

### C. Key Differences Summary

| Aspect | Nish | NSW | Impact |
|--------|------|-----|--------|
| Tables | ~20 | 34 | More structure in NSW |
| Multi-Tenancy | No | Yes | All tables need tenant_id |
| RBAC | Basic | Full | Roles/permissions system |
| L1/L2 Split | No | Yes | Items split into L1/L2 |
| Pricing | Simple | Advanced | Price lists + SKU prices |
| Audit | Timestamps | Full log | Audit trail table |
| BOM Hierarchy | Project-based | Quotation-based | Structural change |

---

**Report Status:** ✅ COMPLETE  
**Next Review:** Phase-6 Kickoff  
**Owner:** Phase-6 Execution Team

---

**Last Updated:** 2025-01-27  
**Version:** 1.0

