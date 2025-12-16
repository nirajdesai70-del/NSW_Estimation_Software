# NEPL Estimation Software - UI Behaviour Map

**Version:** 1.0  
**Date:** 2025-12-16  
**Status:** Baseline Documentation

## Purpose

This document maps the user interface interactions to system behaviors and data operations. It captures what users see, what they can do, and what happens behind the scenes. This is critical for preserving functionality during UI refactoring.

---

## 1. Navigation and Layout

### 1.1 Main Layout Structure
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

### 1.2 Navigation Behavior
- **Click on Menu Item:**
  - User Action: Click navigation menu item
  - System Action: Navigate to corresponding route
  - Data Loaded: List view of selected entity
  - UI Update: Highlight active menu item, show content area

---

## 2. Dashboard Screen

### 2.1 Screen Overview
- **Route:** `/dashboard`
- **Purpose:** Overview of projects, recent activities, statistics

### 2.2 User Interactions

#### View Dashboard
- **User Action:** Navigate to dashboard
- **System Action:** 
  - Load recent projects
  - Load recent quotations
  - Calculate statistics (total projects, active quotations, etc.)
- **Data Displayed:**
  - Recent Projects (list)
  - Recent Quotations (list)
  - Statistics Cards (counts, totals)
- **UI Elements:**
  - Project cards (clickable)
  - Quotation cards (clickable)
  - Statistics widgets

#### Click on Project Card
- **User Action:** Click on a project card
- **System Action:** Navigate to project detail page
- **Data Loaded:** Project details, associated panels, quotations
- **UI Update:** Show project detail view

---

## 3. Project Management Screens

### 3.1 Project List Screen
- **Route:** `/projects`
- **Purpose:** List all projects

#### View Project List
- **User Action:** Navigate to projects
- **System Action:** 
  - Query database for all projects
  - Apply filters if any
  - Apply pagination
- **Data Displayed:**
  - Table/List with columns:
    - Project Name
    - Client Name
    - Status
    - Created Date
    - Actions (Edit, Delete, View)
- **UI Elements:**
  - Search bar
  - Filter dropdowns
  - Pagination controls
  - "Create New Project" button

#### Create New Project
- **User Action:** Click "Create New Project" button
- **System Action:** Show project creation form
- **UI Update:** Display modal or navigate to form page
- **Form Fields:**
  - Project Name (required)
  - Client Name (required)
  - Description (optional)
  - Status (dropdown)
- **Validation:**
  - Project Name: Required, min 3 characters
  - Client Name: Required
- **Submit Behavior:**
  - User Action: Click "Save" button
  - System Action: 
    - Validate form
    - Create project record in database
    - Show success message
    - Navigate to project detail page

#### Edit Project
- **User Action:** Click "Edit" on project row
- **System Action:** 
  - Load project data
  - Populate form with existing data
- **UI Update:** Show edit form (modal or page)
- **Submit Behavior:**
  - User Action: Click "Update" button
  - System Action: 
    - Validate form
    - Update project record
    - Show success message
    - Refresh project list

#### Delete Project
- **User Action:** Click "Delete" on project row
- **System Action:** 
  - Show confirmation dialog
  - If confirmed: Delete project (or soft delete)
  - Check for dependencies (panels, quotations)
- **UI Update:** 
  - Show confirmation dialog
  - Remove from list if deleted
  - Show error if has dependencies

### 3.2 Project Detail Screen
- **Route:** `/projects/:id`
- **Purpose:** View and manage project details

#### View Project Details
- **User Action:** Navigate to project detail
- **System Action:** 
  - Load project data
  - Load associated panels
  - Load associated quotations
- **Data Displayed:**
  - Project information section
  - Panels list
  - Quotations list
- **UI Elements:**
  - Edit button
  - Delete button
  - "Add Panel" button
  - "Create Quotation" button

---

## 4. Panel Management Screens

### 4.1 Panel List Screen
- **Route:** `/panels` or `/projects/:projectId/panels`
- **Purpose:** List panels (all or filtered by project)

#### View Panel List
- **User Action:** Navigate to panels
- **System Action:** 
  - Query panels (optionally filtered by project)
  - Load associated project names
- **Data Displayed:**
  - Table with columns:
    - Panel Name
    - Project Name
    - Feeder Count
    - Status
    - Actions
- **UI Elements:**
  - Filter by project dropdown
  - "Create Panel" button

#### Create Panel
- **User Action:** Click "Create Panel"
- **System Action:** Show panel creation form
- **Form Fields:**
  - Panel Name (required)
  - Project (dropdown, required)
  - Code (optional)
  - Description (optional)
- **Submit Behavior:**
  - Create panel record
  - Link to selected project
  - Navigate to panel detail

### 4.2 Panel Detail Screen
- **Route:** `/panels/:id`
- **Purpose:** View panel details and manage feeders

#### View Panel Details
- **User Action:** Navigate to panel detail
- **System Action:** 
  - Load panel data
  - Load associated feeders
- **Data Displayed:**
  - Panel information
  - Feeders list
- **UI Elements:**
  - "Add Feeder" button
  - Edit/Delete panel buttons

---

## 5. Feeder Management Screens

### 5.1 Feeder List Screen
- **Route:** `/feeders` or `/panels/:panelId/feeders`
- **Purpose:** List feeders (all or filtered by panel)

#### View Feeder List
- **User Action:** Navigate to feeders
- **System Action:** 
  - Query feeders (optionally filtered by panel)
  - Load associated panel names
- **Data Displayed:**
  - Table with columns:
    - Feeder Name
    - Panel Name
    - BOM Count
    - Status
    - Actions

#### Create Feeder
- **User Action:** Click "Create Feeder"
- **System Action:** Show feeder creation form
- **Form Fields:**
  - Feeder Name (required)
  - Panel (dropdown, required)
  - Code (optional)
  - Description (optional)
- **Submit Behavior:**
  - Create feeder record
  - Link to selected panel
  - Navigate to feeder detail

---

## 6. BOM Management Screens

### 6.1 BOM List Screen
- **Route:** `/boms` or `/feeders/:feederId/boms`
- **Purpose:** List BOMs (all or filtered by feeder)

#### View BOM List
- **User Action:** Navigate to BOMs
- **System Action:** 
  - Query BOMs (optionally filtered by feeder)
  - Load associated feeder/panel/project names
  - Calculate total amounts
- **Data Displayed:**
  - Table with columns:
    - BOM Name
    - Feeder Name
    - Panel Name
    - Project Name
    - Total Amount
    - Status
    - Actions

#### Create BOM
- **User Action:** Click "Create BOM"
- **System Action:** Show BOM creation form
- **Form Fields:**
  - BOM Name (required)
  - Feeder (dropdown, required)
  - Description (optional)
- **Submit Behavior:**
  - Create BOM record
  - Link to selected feeder
  - Navigate to BOM detail/editing screen

### 6.2 BOM Detail/Edit Screen
- **Route:** `/boms/:id`
- **Purpose:** View and edit BOM items

#### View BOM Items
- **User Action:** Navigate to BOM detail
- **System Action:** 
  - Load BOM data
  - Load BOM items (with item/component details)
  - Calculate totals
- **Data Displayed:**
  - BOM information section
  - BOM Items table:
    - Item/Component Name
    - Quantity
    - Unit Price
    - Total Price
    - Actions (Edit, Delete)
  - Grand Total
- **UI Elements:**
  - "Add Item" button
  - "Add Component" button
  - "Save BOM" button
  - "Generate Quotation" button

#### Add Item to BOM
- **User Action:** Click "Add Item"
- **System Action:** 
  - Show item selection dialog/search
  - User selects item
  - Show quantity and price input form
- **Form Fields:**
  - Item (pre-selected from search)
  - Quantity (required, > 0)
  - Unit Price (required, >= 0)
  - Notes (optional)
- **Submit Behavior:**
  - Create BOM Item record
  - Link to BOM and selected Item
  - Calculate total_price (quantity × unit_price)
  - Update BOM total_amount
  - Refresh BOM items list

#### Add Component to BOM
- **User Action:** Click "Add Component"
- **System Action:** 
  - Show component selection dialog/search
  - User selects component
  - Show quantity and price input form
- **Form Fields:**
  - Component (pre-selected from search)
  - Quantity (required, > 0)
  - Unit Price (required, >= 0)
  - Notes (optional)
- **Submit Behavior:**
  - Create BOM Item record
  - Link to BOM and selected Component
  - Calculate total_price
  - Update BOM total_amount
  - Refresh BOM items list

#### Edit BOM Item
- **User Action:** Click "Edit" on BOM item row
- **System Action:** 
  - Load BOM item data
  - Show edit form
- **Editable Fields:**
  - Quantity
  - Unit Price
  - Notes
- **Submit Behavior:**
  - Update BOM Item record
  - Recalculate total_price
  - Update BOM total_amount
  - Refresh list

#### Delete BOM Item
- **User Action:** Click "Delete" on BOM item row
- **System Action:** 
  - Show confirmation dialog
  - If confirmed: Delete BOM Item record
  - Recalculate BOM total_amount
- **UI Update:** Remove from list, update total

#### Generate Quotation from BOM
- **User Action:** Click "Generate Quotation"
- **System Action:** 
  - Create new Quotation record
  - Create Quotation Items from BOM Items
  - Link quotation to project
  - Navigate to quotation detail/edit screen
- **Data Created:**
  - Quotation with quotation_number (auto-generated)
  - Quotation Items (one per BOM Item)

---

## 7. Item and Component Management Screens

### 7.1 Item Master Screen
- **Route:** `/items`
- **Purpose:** Manage item master catalog

#### View Item List
- **User Action:** Navigate to items
- **System Action:** 
  - Query all items
  - Load category/subcategory/type information
- **Data Displayed:**
  - Table with columns:
    - Item Code
    - Item Name
    - Category
    - Subcategory
    - Type
    - Unit
    - Base Price
    - Status
    - Actions

#### Create Item
- **User Action:** Click "Create Item"
- **System Action:** Show item creation form
- **Form Fields:**
  - Item Code (required, unique)
  - Item Name (required)
  - Category (dropdown, required)
  - Subcategory (dropdown, filtered by category)
  - Type (dropdown, filtered by subcategory)
  - Unit (required)
  - Base Price (optional)
  - Description (optional)
- **Submit Behavior:**
  - Validate code uniqueness
  - Create item record
  - Navigate to item detail

### 7.2 Component Master Screen
- **Route:** `/components`
- **Purpose:** Manage component master catalog

#### View Component List
- **User Action:** Navigate to components
- **System Action:** Query all components
- **Data Displayed:**
  - Table with columns:
    - Component Code
    - Component Name
    - Unit
    - Base Price
    - Status
    - Actions

#### Create Component
- **User Action:** Click "Create Component"
- **System Action:** Show component creation form
- **Form Fields:**
  - Component Code (required, unique)
  - Component Name (required)
  - Unit (required)
  - Base Price (optional)
  - Description (optional)
- **Submit Behavior:**
  - Validate code uniqueness
  - Create component record
  - Navigate to component detail

---

## 8. Quotation Management Screens

### 8.1 Quotation List Screen
- **Route:** `/quotations`
- **Purpose:** List all quotations

#### View Quotation List
- **User Action:** Navigate to quotations
- **System Action:** 
  - Query all quotations
  - Load associated project names
- **Data Displayed:**
  - Table with columns:
    - Quotation Number
    - Project Name
    - Total Amount
    - Status
    - Valid Until
    - Created Date
    - Actions

### 8.2 Quotation Detail/Edit Screen
- **Route:** `/quotations/:id`
- **Purpose:** View and edit quotation

#### View Quotation Details
- **User Action:** Navigate to quotation detail
- **System Action:** 
  - Load quotation data
  - Load quotation items
  - Calculate totals
- **Data Displayed:**
  - Quotation header information
  - Quotation Items table
  - Grand Total
- **UI Elements:**
  - "Add Item" button
  - "Add Component" button
  - "Add from BOM" button
  - "Save" button
  - "Send" button
  - "Print/Export" button

#### Add Item to Quotation
- **User Action:** Click "Add Item"
- **System Action:** 
  - Show item selection
  - Show quantity/price form
- **Submit Behavior:**
  - Create Quotation Item record
  - Update quotation total_amount
  - Refresh list

---

## 9. Master Data Management Screens

### 9.1 Category Management
- **Route:** `/masters/categories`
- **Purpose:** Manage category master

#### View Categories
- **User Action:** Navigate to categories
- **System Action:** Query all categories
- **Data Displayed:** Category list with actions

#### Create/Edit Category
- **User Action:** Click create/edit
- **System Action:** Show form
- **Validation:** Name must be unique
- **Submit Behavior:** Save category, refresh list

### 9.2 Subcategory Management
- **Route:** `/masters/subcategories`
- **Similar pattern to Categories**

### 9.3 Type Management
- **Route:** `/masters/types`
- **Similar pattern to Categories**

### 9.4 Attribute Management
- **Route:** `/masters/attributes`
- **Similar pattern to Categories**

---

## 10. What is Locked vs Editable

### 10.1 Locked Fields (Read-only)
- **Quotation Number:** Auto-generated, cannot be edited
- **Created At:** System timestamp, read-only
- **Calculated Totals:** Auto-calculated, read-only (but can be overridden in some cases)
- **Project Link (in Panel):** Cannot be changed after creation
- **Panel Link (in Feeder):** Cannot be changed after creation
- **Feeder Link (in BOM):** Cannot be changed after creation

### 10.2 Editable Fields
- **Names, Descriptions:** Always editable (unless entity is locked)
- **Quantities, Prices:** Editable until quotation is finalized
- **Status Fields:** Editable based on workflow rules
- **Notes:** Always editable

### 10.3 Conditional Editing
- **BOM Items:** Editable if BOM status is "draft"
- **Quotation Items:** Editable if quotation status is "draft"
- **Master Data:** Editable if not used in active BOMs/Quotations

---

## 11. Validation Timing

### 11.1 Real-time Validation
- **Field Format:** Validated on blur/change
- **Required Fields:** Validated on submit
- **Unique Constraints:** Validated on submit (async check)

### 11.2 On-Save Validation
- **Business Rules:** Validated when saving
- **Referential Integrity:** Checked on save
- **Calculations:** Performed on save

### 11.3 On-Submit Validation
- **Complete Form:** Validated on final submit
- **Dependencies:** Checked before allowing submission

---

## 12. Cost Impact Calculations

### 12.1 When Calculations Occur
- **On BOM Item Add/Edit:** Recalculate BOM total
- **On Quotation Item Add/Edit:** Recalculate quotation total
- **On Price Change:** Recalculate affected totals
- **On Quantity Change:** Recalculate affected totals

### 12.2 Calculation Display
- **BOM Item Total:** Shown in BOM items table
- **BOM Grand Total:** Shown at bottom of BOM
- **Quotation Total:** Shown in quotation header and footer

---

## Next Steps

1. Complete all sections with actual UI behavior from NEPL V2
2. Add screenshots/mockups if available
3. Validate with user testing
4. Use as reference for UI refactoring in NSW
5. Ensure no behavior is lost during migration

---

**Document Owner:** [Name]  
**Last Updated:** [Date]  
**Review Date:** [Date]

