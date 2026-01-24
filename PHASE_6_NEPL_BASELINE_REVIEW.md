# Phase 6 NEPL Baseline Review
## Complete Review of NEPL Estimation Software Legacy System

**Date:** 2025-01-27  
**Status:** IN PROGRESS  
**Purpose:** Comprehensive baseline review of NEPL Estimation Software - all functions, features, and working patterns

---

## 🎯 Executive Summary

This document provides a comprehensive baseline review of **NEPL Estimation Software V2** - the legacy system that Phase 6 must preserve and enhance. This review covers:

- **All Core Functions:** What the system does
- **All Features:** What capabilities exist
- **All Workflows:** How users interact with the system
- **All Data Structures:** How data is organized
- **All Business Rules:** What rules govern the system

**Critical Rule:** NEPL V2 is the **reference truth**. Phase 6 must preserve all functionality while adding enhancements.

---

## 📋 NEPL System Overview

### System Identity
- **System Name:** NEPL Estimation Software
- **Version:** V2 (Current Production Version)
- **Purpose:** Electrical panel estimation and quotation generation
- **Status:** Active production system
- **Technology:** Legacy system (Laravel-based, read-only reference)

### Core Purpose
NEPL Estimation Software enables users to:
1. Create and manage projects
2. Build electrical panel estimations (Panel → Feeder → BOM → Items)
3. Generate quotations from BOMs
4. Manage master data (Items, Components, Categories)
5. Track costing and pricing

---

## 🏗️ Core Architecture & Data Hierarchy

### Primary Data Hierarchy
```
Project
  └── Panel
      └── Feeder (Level-0 BOM)
          └── BOM (Level-1/2 BOM)
              └── BOM Items
                  ├── Item (from Item Master)
                  └── Component (from Component Master)
                  └── Quantity × Unit Price = Total Price

Category
  └── Subcategory
      └── Type
          └── Attribute
              └── Item (uses hierarchy)
```

**Key Rule:** This hierarchy is **FROZEN**. No shortcuts, no reverse dependencies, no UI-driven logic.

---

## 📊 Core Modules & Functions

### Module 1: Project Management

#### Functions
1. **Create Project**
   - User enters: Project Name, Client Name (required)
   - System creates: Project record
   - Links: Project to Client (implicit)

2. **View Project List**
   - Displays: All projects with client names
   - Shows: Project status, creation date
   - Actions: Edit, Delete, View Details

3. **View Project Details**
   - Displays: Project information
   - Shows: Associated panels list
   - Shows: Associated quotations list
   - Actions: Add Panel, Create Quotation

4. **Edit Project**
   - Editable: Project name, client name, description
   - Validation: Required fields must be filled

5. **Delete Project**
   - Checks: Dependencies (panels, quotations)
   - Prevents: Deletion if has dependencies

#### Data Structure
- **Table:** `projects`
- **Key Fields:** id, name, client_name, description, status, created_at, updated_at
- **Relationships:** Has many Panels, Has many Quotations

---

### Module 2: Panel Management

#### Functions
1. **Create Panel**
   - User enters: Panel Name, Project (dropdown), Code (optional), Description
   - System creates: Panel record linked to Project
   - Navigates: To Panel Detail page

2. **View Panel List**
   - Displays: All panels with project names
   - Shows: Feeder count, status
   - Filters: By project (optional)

3. **View Panel Details**
   - Displays: Panel information
   - Shows: Associated feeders list
   - Actions: Add Feeder, Edit Panel, Delete Panel

4. **Edit Panel**
   - Editable: Panel name, code, description
   - Locked: Project link (cannot change after creation)

5. **Delete Panel**
   - Checks: Dependencies (feeders)
   - Prevents: Deletion if has feeders

#### Data Structure
- **Table:** `panels`
- **Key Fields:** id, name, code, description, project_id, is_active, created_at, updated_at
- **Relationships:** Belongs to Project, Has many Feeders

---

### Module 3: Feeder Management

#### Functions
1. **Create Feeder**
   - User enters: Feeder Name, Panel (dropdown), Code (optional), Description
   - System creates: Feeder record linked to Panel
   - Navigates: To Feeder Detail page

2. **View Feeder List**
   - Displays: All feeders with panel names
   - Shows: BOM count, status
   - Filters: By panel (optional)

3. **View Feeder Details**
   - Displays: Feeder information
   - Shows: Associated BOMs list
   - Actions: Add BOM, Edit Feeder, Delete Feeder

4. **Edit Feeder**
   - Editable: Feeder name, code, description
   - Locked: Panel link (cannot change after creation)

5. **Delete Feeder**
   - Checks: Dependencies (BOMs)
   - Prevents: Deletion if has BOMs

#### Data Structure
- **Table:** `feeders`
- **Key Fields:** id, name, code, description, panel_id, is_active, created_at, updated_at
- **Relationships:** Belongs to Panel, Has many BOMs

**Note:** In NSW, Feeder becomes **Level-0 BOM** (`quote_boms` with `level=0`)

---

### Module 4: BOM (Bill of Materials) Management

#### Functions
1. **Create BOM**
   - User enters: BOM Name, Feeder (dropdown), Description
   - System creates: BOM record linked to Feeder
   - Navigates: To BOM Detail/Edit screen

2. **View BOM List**
   - Displays: All BOMs with feeder/panel/project names
   - Shows: Total amount, status
   - Filters: By feeder (optional)

3. **View/Edit BOM Detail**
   - Displays: BOM information section
   - Shows: BOM Items table with:
     - Item/Component Name
     - Quantity
     - Unit Price
     - Total Price (auto-calculated)
     - Actions (Edit, Delete)
   - Shows: Grand Total (auto-calculated)
   - Actions: Add Item, Add Component, Save BOM, Generate Quotation

4. **Add Item to BOM**
   - User action: Click "Add Item"
   - System shows: Item selection dialog/search
   - User selects: Item from catalog
   - User enters: Quantity (> 0), Unit Price (>= 0), Notes (optional)
   - System creates: BOM Item record
   - System calculates: total_price = quantity × unit_price
   - System updates: BOM total_amount
   - UI refreshes: BOM items list

5. **Add Component to BOM**
   - User action: Click "Add Component"
   - System shows: Component selection dialog/search
   - User selects: Component from component master
   - User enters: Quantity, Unit Price, Notes
   - System creates: BOM Item record (with component_id, item_id=null)
   - System calculates: total_price
   - System updates: BOM total_amount

6. **Edit BOM Item**
   - Editable: Quantity, Unit Price, Notes
   - Locked: Item/Component (cannot change after creation)
   - System recalculates: total_price, BOM total_amount

7. **Delete BOM Item**
   - System shows: Confirmation dialog
   - If confirmed: Deletes BOM Item record
   - System recalculates: BOM total_amount

8. **Generate Quotation from BOM**
   - User action: Click "Generate Quotation"
   - System creates: Quotation record with auto-generated quotation_number
   - System creates: Quotation Items (one per BOM Item)
   - System links: Quotation to project
   - System navigates: To quotation detail/edit screen

#### Data Structure
- **Table:** `boms`
- **Key Fields:** id, name, description, feeder_id, status, total_amount, created_at, updated_at
- **Relationships:** Belongs to Feeder, Has many BOM Items

- **Table:** `bom_items`
- **Key Fields:** id, bom_id, item_id (nullable), component_id (nullable), quantity, unit_price, total_price, notes
- **Constraints:** Must have either item_id OR component_id (not both, not neither)
- **Business Rule:** total_price = quantity × unit_price (auto-calculated)

**Key Rules:**
- BOM Item must have either Item OR Component (mutually exclusive)
- Quantity must be > 0
- Unit Price must be >= 0
- Total Price is auto-calculated but can be overridden

**Note:** In NSW, BOM becomes **Level-1/2 BOM** (`quote_boms` with `level=1` or `level=2`)

---

### Module 5: Item Master Management

#### Functions
1. **View Item List**
   - Displays: All items with category/subcategory/type information
   - Columns: Item Code, Item Name, Category, Subcategory, Type, Unit, Base Price, Status, Actions
   - Filters: By category, subcategory, type (optional)
   - Search: By code, name

2. **Create Item**
   - User enters:
     - Item Code (required, unique)
     - Item Name (required)
     - Category (dropdown, required)
     - Subcategory (dropdown, filtered by category)
     - Type (dropdown, filtered by subcategory)
     - Unit (required)
     - Base Price (optional)
     - Description (optional)
   - System validates: Code uniqueness
   - System creates: Item record
   - System navigates: To item detail

3. **Edit Item**
   - Editable: All fields except code (if used in active BOMs)
   - Validation: Code uniqueness (if changed)

4. **Delete Item**
   - Checks: Usage in BOMs/Quotations
   - Prevents: Deletion if used in active BOMs

#### Data Structure
- **Table:** `items`
- **Key Fields:** id, name, code (unique), description, category_id, subcategory_id (optional), type_id (optional), unit, base_price, is_active
- **Relationships:** 
  - Belongs to Category, Subcategory (optional), Type (optional)
  - Has many BOM Items
  - Has many Item Attributes (via junction table)

**Key Rules:**
- Item Code must be unique
- Must belong to at least Category
- Can optionally belong to Subcategory and Type

**Note:** In NSW, Items split into:
- **L1 Intent Lines** (`l1_intent_lines`) - Engineering meaning
- **L2 SKUs** (`catalog_skus`) - Commercial SKU
- **L1→L2 Mappings** (`l1_l2_mappings`) - Bridge table

---

### Module 6: Component Master Management

#### Functions
1. **View Component List**
   - Displays: All components
   - Columns: Component Code, Component Name, Unit, Base Price, Status, Actions
   - Search: By code, name

2. **Create Component**
   - User enters:
     - Component Code (required, unique)
     - Component Name (required)
     - Unit (required)
     - Base Price (optional)
     - Description (optional)
   - System validates: Code uniqueness
   - System creates: Component record
   - System navigates: To component detail

3. **Edit Component**
   - Editable: All fields except code (if used in active BOMs)

4. **Delete Component**
   - Checks: Usage in BOMs/Quotations
   - Prevents: Deletion if used

#### Data Structure
- **Table:** `components`
- **Key Fields:** id, name, code (unique), description, unit, base_price, is_active
- **Relationships:** Has many BOM Items

**Key Difference from Items:**
- Components are **NOT** part of Category/Subcategory/Type hierarchy
- Components are more generic/reusable across categories
- Components may map to L2 SKUs in NSW or remain separate

---

### Module 7: Quotation Management

#### Functions
1. **View Quotation List**
   - Displays: All quotations with project names
   - Columns: Quotation Number, Project Name, Total Amount, Status, Valid Until, Created Date, Actions
   - Filters: By project, status (optional)

2. **Create Quotation**
   - **Method 1:** Generate from BOM
     - User action: Click "Generate Quotation" on BOM detail
     - System creates: Quotation + Quotation Items from BOM Items
   - **Method 2:** Create manually
     - User enters: Project, Customer Name
     - System creates: Quotation with auto-generated quotation_number
     - User adds: Items/Components manually

3. **View/Edit Quotation Detail**
   - Displays: Quotation header information
   - Shows: Quotation Items table
   - Shows: Grand Total
   - Actions: Add Item, Add Component, Add from BOM, Save, Send, Print/Export

4. **Add Item to Quotation**
   - User selects: Item from catalog
   - User enters: Quantity, Unit Price
   - System creates: Quotation Item record
   - System updates: Quotation total_amount

5. **Add Component to Quotation**
   - Similar to Add Item, but uses Component

6. **Add from BOM**
   - User selects: BOM
   - System creates: Quotation Items from BOM Items

7. **Send Quotation**
   - Changes status: draft → sent
   - May trigger: Email notification (if configured)

8. **Print/Export Quotation**
   - Generates: PDF or Excel export
   - Includes: All quotation items, totals, project/customer info

#### Data Structure
- **Table:** `quotations`
- **Key Fields:** id, quotation_number (unique, auto-generated), project_id, status, total_amount, valid_until, notes, created_at, updated_at
- **Relationships:** Belongs to Project, Has many Quotation Items

- **Table:** `quotation_items`
- **Key Fields:** id, quotation_id, bom_id (nullable), item_id (nullable), component_id (nullable), quantity, unit_price, total_price, description
- **Constraints:** Must have at least one of: bom_id, item_id, or component_id

**Quotation Status Flow:**
- draft → sent → accepted/rejected

**Note:** In NSW, Quotation structure enhanced with:
- `tenant_id` (multi-tenant isolation)
- `status` enum (more structured)
- `customer_name_snapshot` (D-009)
- `customer_id` (optional, future normalization)

---

### Module 8: Master Data Management (Category Hierarchy)

#### Functions

##### Category Management
1. **View Categories**
   - Displays: All categories
   - Actions: Create, Edit, Delete

2. **Create Category**
   - User enters: Category Name, Code (optional), Description
   - System validates: Name uniqueness
   - System creates: Category record

3. **Edit Category**
   - Editable: Name, code, description
   - Prevents: Deletion if has subcategories

##### Subcategory Management
1. **View Subcategories**
   - Displays: Subcategories filtered by category
   - Shows: Parent category name

2. **Create Subcategory**
   - User selects: Category (required)
   - User enters: Subcategory Name, Code, Description
   - System validates: Name uniqueness within category

3. **Edit Subcategory**
   - Editable: Name, code, description
   - Prevents: Deletion if has types

##### Type Management
1. **View Types**
   - Displays: Types filtered by subcategory
   - Shows: Parent subcategory name

2. **Create Type**
   - User selects: Subcategory (required)
   - User enters: Type Name, Code, Description
   - System validates: Name uniqueness within subcategory

3. **Edit Type**
   - Editable: Name, code, description
   - Prevents: Deletion if has attributes

##### Attribute Management
1. **View Attributes**
   - Displays: Attributes filtered by type
   - Shows: Parent type name

2. **Create Attribute**
   - User selects: Type (required)
   - User enters: Attribute Name, Value Type (string/integer/decimal/boolean), Default Value, Is Required flag
   - System validates: Name uniqueness within type

3. **Edit Attribute**
   - Editable: Name, value_type, default_value, is_required

#### Data Structure
- **Table:** `categories`
- **Key Fields:** id, name (unique), code, description, is_active
- **Relationships:** Has many Subcategories, Has many Items (direct)

- **Table:** `sub_categories`
- **Key Fields:** id, category_id, name (unique within category), code, description, is_active
- **Relationships:** Belongs to Category, Has many Types, Has many Items (direct)

- **Table:** `types`
- **Key Fields:** id, subcategory_id, name (unique within subcategory), code, description, is_active
- **Relationships:** Belongs to Subcategory, Has many Attributes, Has many Items (direct)

- **Table:** `attributes`
- **Key Fields:** id, type_id, name (unique within type), value_type, default_value, is_required, is_active
- **Relationships:** Belongs to Type, Used by Items (via item_attributes junction table)

- **Table:** `item_attributes` (Junction Table)
- **Key Fields:** id, item_id, attribute_id, value
- **Relationships:** Links Items to Attributes

**Hierarchy Rules:**
- Category → Subcategory → Type → Attribute → Item
- Items can belong directly to Category, or to Category+Subcategory, or to Category+Subcategory+Type
- Attributes are linked to Items via junction table (many-to-many)

---

## 🔄 Core Business Workflows

### Workflow 1: Complete Estimation Flow

**Purpose:** Create a complete estimation from project to quotation

**Steps:**
1. **Create Project**
   - User creates project with client name
   - System creates project record

2. **Create Panel**
   - User creates panel under project
   - System creates panel record linked to project

3. **Create Feeder**
   - User creates feeder under panel
   - System creates feeder record linked to panel

4. **Create BOM**
   - User creates BOM under feeder
   - System creates BOM record linked to feeder

5. **Add Items/Components to BOM**
   - User adds items or components to BOM
   - For each item/component:
     - User selects: Item or Component
     - User enters: Quantity, Unit Price
     - System calculates: Total Price = Quantity × Unit Price
     - System creates: BOM Item record
   - System calculates: BOM Total = Sum of all BOM Item totals

6. **Generate Quotation**
   - User clicks "Generate Quotation"
   - System creates: Quotation record
   - System creates: Quotation Items from BOM Items
   - System links: Quotation to project
   - System navigates: To quotation detail

7. **Finalize Quotation**
   - User reviews quotation
   - User can: Edit items, add items, remove items
   - User sends: Quotation (status: draft → sent)

**Data Flow:**
```
Project → Panel → Feeder → BOM → BOM Items → Quotation → Quotation Items
```

---

### Workflow 2: Master Data Setup Flow

**Purpose:** Set up the category hierarchy and item catalog

**Steps:**
1. **Create Categories**
   - User creates top-level categories
   - System creates category records

2. **Create Subcategories**
   - User creates subcategories under categories
   - System creates subcategory records

3. **Create Types**
   - User creates types under subcategories
   - System creates type records

4. **Create Attributes**
   - User creates attributes under types
   - System creates attribute records

5. **Create Items**
   - User creates items linked to category/subcategory/type
   - User assigns item attributes (via junction table)
   - System creates item records

6. **Create Components**
   - User creates components (independent of category hierarchy)
   - System creates component records

**Data Flow:**
```
Category → Subcategory → Type → Attribute → Item
Component (independent)
```

---

### Workflow 3: BOM Building & Reuse Flow

**Purpose:** Build BOMs and reuse existing BOMs

**Steps:**
1. **Create Master BOM (Template)**
   - User creates master BOM with L1/Generic products
   - System creates master BOM record
   - System creates master BOM items

2. **Create Proposal BOM from Master BOM**
   - User selects: Master BOM
   - User creates: Proposal BOM instance
   - System creates: Proposal BOM record
   - System creates: Proposal BOM items (copied from master, but editable)
   - System enters: L0→L1→L2 resolution flow

3. **Edit Proposal BOM**
   - User can: Add items, remove items, edit quantities, edit prices
   - System updates: Proposal BOM items
   - System recalculates: Totals

4. **Reuse BOM from Past Quotation**
   - User selects: Past quotation/project
   - User copies: BOM from past quotation
   - System creates: New BOM with copied items
   - All copied content: Editable until locked

**Key Rules:**
- Master BOM = Template (L1 products only)
- Proposal BOM = Instance (L2 products)
- BOM items editable until quotation finalized
- Copy-never-link: Always copy, never link

**Note:** In NSW, this becomes:
- Master BOM → Quote BOM (with L0/L1/L2 levels)
- Reuse workflows (Track A-R)

---

### Workflow 4: Pricing & Costing Flow

**Purpose:** Set prices and calculate costs

**Steps:**
1. **Set Base Prices**
   - User sets: Base price on Items/Components
   - System stores: base_price in items/components tables

2. **BOM Item Pricing**
   - When adding item to BOM:
     - System suggests: Base price from item master
     - User can: Override with unit_price
     - System calculates: total_price = quantity × unit_price

3. **Quotation Item Pricing**
   - When generating quotation:
     - System copies: unit_price from BOM items
     - User can: Override unit_price in quotation
     - System calculates: total_price

4. **Quotation Total**
   - System calculates: Quotation Total = Sum of all quotation item totals

**Pricing Model:**
- **Base Price:** Stored on Items/Components (master data)
- **Unit Price:** Stored on BOM Items/Quotation Items (can override base_price)
- **Total Price:** Auto-calculated (quantity × unit_price)

**Note:** In NSW, this becomes:
- Price Lists → SKU Prices (L2 level)
- Rate Source enum (PRICELIST / MANUAL / FIXED)
- Discount Rules engine

---

## 📱 User Interface & Screens

### Main Navigation
```
[Header]
  ├── Logo/Branding
  ├── Navigation Menu
  │   ├── Dashboard
  │   ├── Projects
  │   ├── Panels
  │   ├── Feeders
  │   ├── BOMs
  │   ├── Items
  │   ├── Components
  │   ├── Quotations
  │   └── Masters
  │       ├── Categories
  │       ├── Subcategories
  │       ├── Types
  │       └── Attributes
  └── User Menu

[Main Content Area]
  └── [Dynamic Content based on route]

[Footer]
  └── Copyright/Version Info
```

### Screen Inventory

#### 1. Dashboard Screen
- **Route:** `/dashboard`
- **Purpose:** Overview of projects, recent activities, statistics
- **Displays:**
  - Recent Projects (list)
  - Recent Quotations (list)
  - Statistics Cards (counts, totals)
- **Actions:**
  - Click project card → Navigate to project detail
  - Click quotation card → Navigate to quotation detail

#### 2. Project List Screen
- **Route:** `/projects`
- **Purpose:** List all projects
- **Displays:**
  - Table: Project Name, Client Name, Status, Created Date, Actions
- **Actions:**
  - Create New Project
  - Edit Project
  - Delete Project
  - View Project Details

#### 3. Project Detail Screen
- **Route:** `/projects/:id`
- **Purpose:** View and manage project details
- **Displays:**
  - Project information section
  - Panels list
  - Quotations list
- **Actions:**
  - Add Panel
  - Create Quotation
  - Edit Project
  - Delete Project

#### 4. Panel List Screen
- **Route:** `/panels` or `/projects/:projectId/panels`
- **Purpose:** List panels
- **Displays:**
  - Table: Panel Name, Project Name, Feeder Count, Status, Actions
- **Actions:**
  - Create Panel
  - Filter by project

#### 5. Panel Detail Screen
- **Route:** `/panels/:id`
- **Purpose:** View panel details and manage feeders
- **Displays:**
  - Panel information
  - Feeders list
- **Actions:**
  - Add Feeder
  - Edit Panel
  - Delete Panel

#### 6. Feeder List Screen
- **Route:** `/feeders` or `/panels/:panelId/feeders`
- **Purpose:** List feeders
- **Displays:**
  - Table: Feeder Name, Panel Name, BOM Count, Status, Actions
- **Actions:**
  - Create Feeder
  - Filter by panel

#### 7. BOM List Screen
- **Route:** `/boms` or `/feeders/:feederId/boms`
- **Purpose:** List BOMs
- **Displays:**
  - Table: BOM Name, Feeder Name, Panel Name, Project Name, Total Amount, Status, Actions
- **Actions:**
  - Create BOM
  - Filter by feeder

#### 8. BOM Detail/Edit Screen
- **Route:** `/boms/:id`
- **Purpose:** View and edit BOM items
- **Displays:**
  - BOM information section
  - BOM Items table:
    - Item/Component Name
    - Quantity
    - Unit Price
    - Total Price (auto-calculated)
    - Actions (Edit, Delete)
  - Grand Total
- **Actions:**
  - Add Item
  - Add Component
  - Edit BOM Item
  - Delete BOM Item
  - Save BOM
  - Generate Quotation

#### 9. Item Master Screen
- **Route:** `/items`
- **Purpose:** Manage item master catalog
- **Displays:**
  - Table: Item Code, Item Name, Category, Subcategory, Type, Unit, Base Price, Status, Actions
- **Actions:**
  - Create Item
  - Edit Item
  - Delete Item
  - Filter by category/subcategory/type
  - Search by code/name

#### 10. Component Master Screen
- **Route:** `/components`
- **Purpose:** Manage component master catalog
- **Displays:**
  - Table: Component Code, Component Name, Unit, Base Price, Status, Actions
- **Actions:**
  - Create Component
  - Edit Component
  - Delete Component
  - Search by code/name

#### 11. Quotation List Screen
- **Route:** `/quotations`
- **Purpose:** List all quotations
- **Displays:**
  - Table: Quotation Number, Project Name, Total Amount, Status, Valid Until, Created Date, Actions
- **Actions:**
  - Create Quotation
  - Filter by project/status

#### 12. Quotation Detail/Edit Screen
- **Route:** `/quotations/:id`
- **Purpose:** View and edit quotation
- **Displays:**
  - Quotation header information
  - Quotation Items table
  - Grand Total
- **Actions:**
  - Add Item
  - Add Component
  - Add from BOM
  - Save
  - Send
  - Print/Export

#### 13. Master Data Management Screens
- **Routes:**
  - `/masters/categories`
  - `/masters/subcategories`
  - `/masters/types`
  - `/masters/attributes`
- **Purpose:** Manage category hierarchy
- **Pattern:** Similar CRUD operations for each level

---

## 🔐 Business Rules & Constraints

### Data Integrity Rules

1. **Referential Integrity**
   - All foreign keys must reference existing records
   - Cannot delete parent if has children
   - Cascade deletes where appropriate

2. **BOM Item Rules**
   - Must have either Item OR Component (not both, not neither)
   - Quantity must be > 0
   - Unit Price must be >= 0
   - Total Price = Quantity × Unit Price (auto-calculated)

3. **Quotation Item Rules**
   - Must have at least one of: bom_id, item_id, or component_id
   - Quantity must be > 0

4. **Master Data Rules**
   - Item Code must be unique
   - Component Code must be unique
   - Category Name must be unique
   - Subcategory Name must be unique within category
   - Type Name must be unique within subcategory
   - Attribute Name must be unique within type

### Workflow Rules

1. **BOM Status Rules**
   - BOM status: draft → active → locked
   - BOM items editable if status is "draft"
   - Cannot edit locked BOMs

2. **Quotation Status Rules**
   - Quotation status: draft → sent → accepted/rejected
   - Quotation items editable if status is "draft"
   - Cannot edit sent/accepted/rejected quotations

3. **Project Status Rules**
   - Project status: active → inactive
   - Soft delete (is_active flag)

### Calculation Rules

1. **BOM Total Calculation**
   - BOM Total = Sum of all BOM Item total_price values
   - Auto-calculated on BOM Item add/edit/delete

2. **Quotation Total Calculation**
   - Quotation Total = Sum of all Quotation Item total_price values
   - Auto-calculated on Quotation Item add/edit/delete

3. **BOM Item Total Calculation**
   - BOM Item Total = Quantity × Unit Price
   - Auto-calculated but can be overridden

---

## 🎯 Key Features & Capabilities

### Feature 1: Estimation Building
- **Capability:** Build complete estimations (Project → Panel → Feeder → BOM → Items)
- **User Actions:** Create, edit, delete at each level
- **System Behavior:** Maintains hierarchy, calculates totals

### Feature 2: Master Data Management
- **Capability:** Manage category hierarchy and item/component catalog
- **User Actions:** CRUD operations on categories, subcategories, types, attributes, items, components
- **System Behavior:** Enforces hierarchy, validates uniqueness

### Feature 3: Quotation Generation
- **Capability:** Generate quotations from BOMs or create manually
- **User Actions:** Generate from BOM, add items manually, edit, send
- **System Behavior:** Auto-generates quotation numbers, calculates totals

### Feature 4: Pricing Management
- **Capability:** Set base prices on items/components, override in BOMs/quotations
- **User Actions:** Set base prices, override unit prices
- **System Behavior:** Suggests base prices, allows overrides, calculates totals

### Feature 5: BOM Reuse
- **Capability:** Reuse BOMs from master templates or past quotations
- **User Actions:** Create master BOM, apply to proposal, copy from past
- **System Behavior:** Copies BOM items, makes them editable

### Feature 6: Data Hierarchy Navigation
- **Capability:** Navigate through project → panel → feeder → BOM hierarchy
- **User Actions:** Click through hierarchy, view details at each level
- **System Behavior:** Loads related data, maintains context

---

## ⚠️ Known Limitations & Gaps

### Technical Limitations
1. **No Multi-Tenant Isolation**
   - No tenant concept
   - Multi-tenancy handled via project/client separation
   - **NSW Enhancement:** Adds tenant_id everywhere

2. **No RBAC System**
   - Basic user authentication only
   - No roles/permissions documented
   - **NSW Enhancement:** Adds full RBAC system

3. **No Audit Trail**
   - Only created_at/updated_at timestamps
   - No audit log table
   - **NSW Enhancement:** Adds audit_logs table

4. **No Price List Management**
   - Simple base_price on items
   - No price list system
   - **NSW Enhancement:** Adds price_lists and sku_prices

5. **No Discount Rules**
   - No discount rule engine
   - Manual price overrides only
   - **NSW Enhancement:** Adds discount_rules table

### Functional Gaps
1. **No L1/L2 Split**
   - Single items table
   - No engineering vs commercial separation
   - **NSW Enhancement:** Splits into L1 Intent Lines and L2 SKUs

2. **No BOM History/Versioning**
   - No history tracking for BOM edits
   - **NSW Enhancement:** Adds BOM tracking fields

3. **No Export Functionality Documented**
   - No explicit export features documented
   - **NSW Enhancement:** Adds PDF/Excel export

---

## 📊 Data Model Summary

### Core Tables (Estimated ~20 tables)

**Auth:**
- `users`

**Master Data:**
- `categories`
- `sub_categories`
- `types`
- `attributes`
- `items`
- `components`
- `item_attributes` (junction)

**Project/Customer:**
- `projects`
- `clients`
- `panels`
- `feeders`

**BOM:**
- `boms`
- `bom_items`
- `master_boms` (optional)
- `master_bom_items` (optional)
- `proposal_boms` (optional)
- `proposal_bom_items` (optional)

**Quotation:**
- `quotations`
- `quotation_items`

**Total:** ~20 tables (estimated from Phase 1-4 documentation)

---

## 💰 Calculation Formulas & Business Logic

### Core Calculation Formulas (FROZEN - DO NOT CHANGE)

#### Formula 1: Item-Level Calculation
```
NetRate = BaseRate × (1 - Discount/100)
AmountTotal = NetRate × TotalQty
```

**Where:**
- `BaseRate` = Price per unit (from prices table or manual entry)
- `Discount` = Discount percentage (0-100)
- `TotalQty` = Total quantity (from QuotationQuantityService)

**Special Cases:**
- If `IsClientSupplied = 1`: `Rate = 0`, `NetRate = 0`, `AmountTotal = 0`
- If `IsPriceMissing = 1`: `Rate = 0`, `NetRate = 0`, `AmountTotal = 0`

#### Formula 2: BOM Total Calculation
```
BOM_TotalCost = SUM(All BOM Item AmountTotal)
```

**Golden Rule:** NO multipliers at roll-up level. Only SUM of component AmountTotal.

#### Formula 3: Feeder Total Calculation
```
Feeder_TotalCost = SUM(All Component AmountTotal in Feeder)
```

**Golden Rule:** NO multipliers. Only SUM.

#### Formula 4: Panel Total Calculation
```
Panel_TotalCost = SUM(All Component AmountTotal in Panel)
```

**Golden Rule:** NO multipliers. Only SUM.

#### Formula 5: Quotation Total Calculation
```
Quotation_Total = SUM(All Quotation Item AmountTotal)
```

**Golden Rule:** NO multipliers. Only SUM.

### Discount Calculation

#### Discount Editor Functionality
- **Route:** `/quotation/{id}/discount`
- **Purpose:** Apply bulk discounts across many items
- **Filters:** Make, Category, Product Type, Attribute, Description, SKU, Panel, Feeder, BOM
- **Rule Types:**
  - Percentage discount (Phase 1)
  - Flat discount (Phase 2)
- **Calculation:**
  ```
  NewDiscount = Input %
  NetRate = Rate - (Rate × Discount%)
  Amount = NetRate × Qty
  ```

### Costing Service (Protected Code)
- **Service:** `CostingService`
- **Status:** 🔴 **PROTECTED CODE - DO NOT MODIFY WITHOUT APPROVAL**
- **Golden Rule:** All roll-up costs = SUM(Component AmountTotal)
- **Where:** AmountTotal = NetRate × TotalQty

---

## 🔄 NEPL → NSW Key Transformations

### Transformation 1: Multi-Tenant Isolation
- **NEPL:** No tenant concept
- **NSW:** All tables have `tenant_id` (except `tenants`)
- **Impact:** All queries must filter by tenant_id

### Transformation 2: L1/L2 Split
- **NEPL:** Single `items` table
- **NSW:** Split into `l1_intent_lines` + `catalog_skus` + `l1_l2_mappings`
- **Impact:** Items must be mapped to L1/L2 during migration

### Transformation 3: BOM Hierarchy Restructure
- **NEPL:** Project → Panel → Feeder → BOM
- **NSW:** Quotation → Panel → BOM (level=0/1/2)
- **Impact:** Feeder becomes level=0 BOM, BOM becomes level=1/2

### Transformation 4: Pricing Model Upgrade
- **NEPL:** Base price on items → unit price on BOM items
- **NSW:** Price lists → SKU prices (L2) → Quote BOM item rates (with rate_source)
- **Impact:** Pricing logic more complex, supports multiple price lists

### Transformation 5: RBAC Addition
- **NEPL:** Basic users only
- **NSW:** Full RBAC (roles, permissions, user_roles)
- **Impact:** Access control more granular

### Transformation 6: CostHead System Addition
- **NEPL:** No cost head categorization
- **NSW:** CostHead system (MATERIAL, LABOUR, OTHER buckets)
- **Impact:** Costs categorized for reporting and analysis

---

## ✅ What Must Be Preserved in Phase 6

### Non-Negotiable Functions
1. ✅ **Estimation Logic (Panel → Feeder → BOM → Item)**
   - Must preserve exactly
   - No changes to calculation logic

2. ✅ **Category / Subcategory / Type / Attribute Hierarchy**
   - Must preserve structure
   - May improve UI presentation

3. ✅ **Item Master and Component Master**
   - Must preserve structure
   - May enhance functionality

4. ✅ **BOM Calculation Logic**
   - Must preserve exactly
   - No changes to formulas

5. ✅ **Quotation Lifecycle**
   - Must preserve workflow
   - May improve UI

6. ✅ **BOM Reuse Capabilities**
   - Must preserve reuse functionality
   - Must preserve copy-never-link rule

7. ✅ **Pricing Override Capability**
   - Must preserve ability to override prices
   - Must preserve base_price → unit_price flow

---

## 🚨 What Must NOT Be Repeated

### Mistakes to Avoid
1. ❌ **UI-Driven Logic Changes**
   - Logic should drive UI, not vice versa
   - **NSW Prevention:** Always design logic first, then UI

2. ❌ **Inconsistent Naming**
   - **NSW Prevention:** Establish naming conventions from start

3. ❌ **Skipping Baseline Documentation**
   - **NSW Prevention:** Complete all baseline documents before development

4. ❌ **Breaking Data Relationships**
   - **NSW Prevention:** Preserve all relationships, validate before changes

---

## 📋 Phase 6 Requirements Based on NEPL Baseline

### Must-Have Features (Legacy Parity)
1. ✅ All NEPL functions must work in NSW
2. ✅ All NEPL workflows must be preserved
3. ✅ All NEPL data relationships must be maintained
4. ✅ All NEPL business rules must be enforced

### Enhancement Opportunities
1. ✅ Better UI/UX (visual improvements)
2. ✅ Multi-tenant isolation
3. ✅ RBAC system
4. ✅ Audit trail
5. ✅ Price list management
6. ✅ Discount rules
7. ✅ L1/L2 split (engineering vs commercial)
8. ✅ Better validation
9. ✅ Export functionality

---

## 🎯 Next Steps for Phase 6

### Immediate Actions
1. **Validate NEPL Baseline**
   - Review this document with stakeholders
   - Confirm all functions are captured
   - Identify any missing functions

2. **Map NEPL Functions to Phase 6 Tracks**
   - Map each NEPL function to Phase 6 track
   - Ensure all functions are covered
   - Document any gaps

3. **Create Legacy Parity Checklist**
   - Create checklist of all NEPL functions
   - Verify each function in NSW
   - Document any deviations

### Short-term Actions
4. **Document NEPL Workflows in Detail**
   - Document each workflow step-by-step
   - Capture all user actions
   - Capture all system behaviors

5. **Create NEPL → NSW Mapping Matrix**
   - Map each NEPL screen to NSW screen
   - Map each NEPL function to NSW function
   - Document transformations

---

**Status:** BASELINE REVIEW IN PROGRESS  
**Last Updated:** 2025-01-27  
**Next Action:** Continue reviewing NEPL documents and complete baseline
