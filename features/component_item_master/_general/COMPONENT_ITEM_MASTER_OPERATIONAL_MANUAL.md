> Source: source_snapshot/docs/07_USER_GUIDES/COMPONENT_ITEM_MASTER_OPERATIONAL_MANUAL.md
> Bifurcated into: features/component_item_master/COMPONENT_ITEM_MASTER_OPERATIONAL_MANUAL.md
> Module: Component / Item Master > General
> Date: 2025-12-17 (IST)

# Component/Item Master - Operational and Maintenance Manual

**Document:** COMPONENT_ITEM_MASTER_OPERATIONAL_MANUAL.md  
**Version:** 1.0  
**Last Updated:** December 2025  
**Status:** ✅ **OPERATIONAL GUIDE**

**Purpose:** Complete operational, configuration, and maintenance manual for Component/Item Master system for end users and system administrators.

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Frontend Technical Architecture](#frontend-technical-architecture)
4. [Database Schema (For Understanding)](#database-schema-for-understanding)
5. [Frontend View Development and Customization](#frontend-view-development-and-customization)
6. [Component Master Operations](#component-master-operations)
7. [Item Master Operations](#item-master-operations)
8. [Configuration Procedures](#configuration-procedures)
9. [Maintenance Procedures](#maintenance-procedures)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Best Practices](#best-practices)
12. [Quick Reference](#quick-reference)
13. [Revision History](#revision-history)

---

## 🎯 Introduction

### Purpose of This Manual

This manual provides **step-by-step operational procedures** for managing the Component/Item Master system. It is designed for:

- **System Administrators** - Daily operations and maintenance
- **Product Managers** - Product catalog configuration
- **End Users** - Basic operations and data entry

### What This Manual Covers

✅ **Operational Procedures** - How to perform daily tasks  
✅ **Configuration Steps** - How to set up and configure  
✅ **Maintenance Tasks** - How to maintain data quality  
✅ **Troubleshooting** - How to resolve common issues  
✅ **Best Practices** - Recommended approaches  

### What This Manual Does NOT Cover

❌ Backend programming code (PHP controllers, models)  
❌ API endpoints and programming  
❌ Server-side logic implementation  

### What This Manual DOES Cover (Technical)

✅ **Frontend Technical Architecture** - View structure, UI components, frontend technologies  
✅ **Database Schema** - Table structures and relationships (for understanding data)  
✅ **Frontend View Development** - How to customize and develop views  

---

## 📊 System Overview

### What is Component Master?

**Component Master** is a simple reference system for basic component identification. It stores component names and details for quick lookup and reference.

**Key Features:**
- Simple component name storage
- Quick lookup and reference
- Basic component categorization

### What is Item Master?

**Item Master (Product Type)** is a functional classification system in the product hierarchy. It helps organize products by their functional type or purpose.

**Key Features:**
- Product type classification
- Category-based organization
- Attribute assignment capability
- Product relationship tracking

### System Hierarchy

```
COMPONENT MASTER
└── Component (Simple Reference)
    └── Name, Details

ITEM MASTER (Product Hierarchy)
└── Category
    └── SubCategory (Optional)
        └── Item (Product Type)
            └── Products (Generic & Specific)
```

### When to Use Component vs Item

**Use Component Master when:**
- You need a simple reference/lookup
- Basic component identification is sufficient
- No complex relationships needed

**Use Item Master when:**
- You need functional product classification
- Products need to be organized by type
- Attributes need to be assigned to product types
- Products will be created under this classification

---

## 🏗️ Frontend Technical Architecture

### View File Structure

The Component/Item Master system uses **Blade templates** (Laravel's templating engine) for frontend views.

**Component Master Views:**
```
resources/views/component/
├── index.blade.php      → Component list page
├── create.blade.php     → Create component form
└── edit.blade.php       → Edit component form
```

**Item Master Views:**
```
resources/views/item/
├── index.blade.php      → Item/Product Type list page
├── create.blade.php     → Create item form
└── edit.blade.php       → Edit item form
```

### Layout Structure

All views extend the main application layout:

```blade
@extends('layouts.app')

@section('title', 'Page Title')
@section('header_title', 'Page Header')

@section('content')
    <!-- Page content here -->
@endsection

@section('vendor_js')
    <!-- Vendor JavaScript files -->
@endsection

@section('plugin_js')
    <!-- Custom JavaScript -->
@endsection
```

**Layout Components:**
- `layouts.app` - Main application layout
- `layouts.sidebar` - Left navigation menu
- `layouts.navbar` - Top navigation bar
- `layouts.breadcrumbs` - Navigation breadcrumbs
- `layouts.footer` - Page footer

### UI Components Used

#### 1. NEPL Standard Table Component

**Component:** `<x-nepl-table>`

**Location:** `resources/views/components/nepl-table.blade.php`

**Usage:**
```blade
<x-nepl-table
    id="componentTable"
    :columns="$columns"
    :rows="$components"
    :actions="$actions"
    :pagination="$components"
    :searchable="true"
    :showEntries="true"
    :pageLength="25"
    :showIndex="true"
/>
```

**Parameters:**
- `id` - Unique table identifier
- `columns` - Array of column definitions
- `rows` - Data rows to display
- `actions` - Action buttons (edit, delete, etc.)
- `pagination` - Pagination object
- `searchable` - Enable search functionality
- `showEntries` - Show entries dropdown
- `pageLength` - Default items per page
- `showIndex` - Show serial number column

**Features:**
- Automatic pagination
- Search functionality
- Sortable columns
- Action buttons
- Responsive design
- Custom column rendering

#### 2. Form Components

**Laravel Collective Forms:**
```blade
{{ Form::open(['route' => ['component.store'], 'method' => 'POST']) }}
    {{ Form::label('Name', __('Name *')) }}
    {{ Form::text('Name', null, ['class' => 'form-control', 'required' => true]) }}
    {{ Form::close() }}
```

**Form Elements:**
- `Form::text()` - Text input
- `Form::select()` - Dropdown select
- `Form::label()` - Form label
- `Form::open()` / `Form::close()` - Form wrapper

#### 3. Select2 Dropdown

**Usage:**
```blade
{{ Form::select('CategoryId', $category, null, ['class' => 'form-control select2']) }}
```

**JavaScript Initialization:**
```javascript
$('.select2').select2();
```

**Features:**
- Searchable dropdown
- Better UX for long lists
- Custom styling

### Frontend Technologies

**CSS Framework:**
- Bootstrap 4 (via app-assets)
- Custom NEPL styles (nepl-table, nepl-form-input classes)

**JavaScript Libraries:**
- jQuery
- DataTables (for table functionality)
- Select2 (for dropdowns)
- Custom NEPL JavaScript (`public/js/nepl-tables.js`)

**CSS Files:**
- `app-assets/vendors/css/tables/datatable/datatables.min.css`
- Custom NEPL styles

**JavaScript Files:**
- `app-assets/vendors/js/tables/datatable/datatables.min.js`
- `public/js/nepl-tables.js` (NEPL custom table functions)

### Page Structure

**Component Index Page Structure:**
```blade
@extends('layouts.app')
├── @section('title') - Page title
├── @section('header_title') - Header title
├── @section('titleright') - Top-right buttons (Add New)
├── @section('content')
│   └── <section>
│       └── <div class="card nepl-table-wrapper">
│           └── <x-nepl-table> - Table component
├── @section('vendor_js') - Vendor JavaScript
└── @section('plugin_js') - Custom JavaScript
```

**Component Create/Edit Page Structure:**
```blade
@extends('layouts.app')
├── @section('title') - Page title
├── @section('header_title') - Header title
├── @section('titleright') - Back button
├── @section('content')
│   └── <section>
│       └── <div class="card">
│           └── {{ Form::open() }}
│               └── Form fields
│               └── Submit/Cancel buttons
└── @section('script') - Form JavaScript
```

### CSS Classes Used

**Table Classes:**
- `nepl-table-wrapper` - Table container
- `nepl-table` - Main table
- `nepl-standard-table` - Standard table styling
- `nepl-table-header` - Table header cells
- `nepl-table-body` - Table body cells
- `nepl-table-actions` - Action column cells

**Form Classes:**
- `form-control` - Standard form input
- `form-control-sm` - Small form input
- `nepl-form-input` - NEPL custom input styling
- `select2` - Select2 dropdown

**Layout Classes:**
- `card` - Card container
- `card-header` - Card header
- `card-body` - Card body
- `card-footer` - Card footer

---

## 🗄️ Database Schema (For Understanding)

### Component Table Schema

**Table Name:** `components`

**Purpose:** Stores basic component reference information

**Structure:**
| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| ComponentId | BIGINT | Primary key (auto-increment) | PRIMARY KEY |
| Name | VARCHAR(255) | Component name | NULL allowed |
| Details | VARCHAR(255) | Component description | NULL allowed |
| created_at | TIMESTAMP | Creation timestamp | NULL allowed |
| updated_at | TIMESTAMP | Update timestamp | NULL allowed |

**Key Points:**
- Simple standalone table
- No foreign key relationships
- No soft delete (hard delete only)
- Minimal structure for basic reference

**Data Example:**
```
ComponentId: 1
Name: "Circuit Breaker"
Details: "Standard circuit breaker component"
created_at: 2025-01-15 10:30:00
updated_at: 2025-01-15 10:30:00
```

### Item Table Schema

**Table Name:** `items`

**Purpose:** Stores product type/item classification information

**Structure:**
| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| ItemId | INT | Primary key (auto-increment) | PRIMARY KEY |
| CategoryId | INT | Foreign key to categories | NOT NULL, FK |
| SubCategoryId | INT | Foreign key to sub_categories | NULL allowed, FK |
| Name | VARCHAR(255) | Item/Product Type name | NOT NULL |
| Details | TEXT | Item description | NULL allowed |
| Status | TINYINT | 0=Active, 1=Deleted | NOT NULL, DEFAULT 0 |
| created_at | TIMESTAMP | Creation timestamp | NULL allowed |
| updated_at | TIMESTAMP | Update timestamp | NULL allowed |

**Key Points:**
- Part of product hierarchy
- Required relationship to Category
- Optional relationship to SubCategory
- Soft delete support (Status field)
- Referenced by products table

**Data Example:**
```
ItemId: 10
CategoryId: 1 (Electrical Panels)
SubCategoryId: 5 (Distribution Panels)
Name: "Indoor Distribution Panel"
Details: "Standard indoor distribution panel type"
Status: 0 (Active)
created_at: 2025-01-15 10:30:00
updated_at: 2025-01-15 10:30:00
```

### Database Relationships

**Component Table:**
- No relationships (standalone)

**Item Table Relationships:**
```
categories (1) ──→ (N) items
    CategoryId (FK)

sub_categories (1) ──→ (N) items
    SubCategoryId (FK)

items (1) ──→ (N) products
    ItemId (referenced by products.ItemId)
```

**Relationship Diagram:**
```
┌──────────────┐
│  categories  │
└──────┬───────┘
       │ CategoryId (FK)
       │
       ▼
┌──────────────┐
│    items     │
└──────┬───────┘
       │ ItemId
       │
       ▼
┌──────────────┐
│   products   │
└──────────────┘
```

**Understanding Relationships:**
- Each Item must belong to a Category
- Each Item can optionally belong to a SubCategory
- Multiple Products can use the same Item (ItemId)
- Products reference ItemId to classify by type

**Data Flow:**
1. Create Category first
2. Create SubCategory (optional) under Category
3. Create Item under Category/SubCategory
4. Create Products using Item (ItemId)

---

## 🎨 Frontend View Development and Customization

### Customizing Component List View

**File:** `resources/views/component/index.blade.php`

**Adding New Column:**

1. **Update Controller** (backend provides data):
   ```php
   $columns = [
       ['key' => 'Name', 'label' => 'Name', 'sortable' => true],
       ['key' => 'Details', 'label' => 'Details', 'sortable' => false],
       // Add new column
       ['key' => 'NewField', 'label' => 'New Column', 'sortable' => true],
   ];
   ```

2. **View automatically displays** new column via `<x-nepl-table>` component

**Custom Column Rendering:**

```php
$columns = [
    ['key' => 'Name', 'label' => 'Name', 'sortable' => true],
    [
        'key' => 'Status',
        'label' => 'Status',
        'render' => function ($row) {
            $status = $row->Status ?? 0;
            $badge = $status == 0 ? 'success' : 'secondary';
            $text = $status == 0 ? 'Active' : 'Inactive';
            return '<span class="badge badge-' . $badge . '">' . $text . '</span>';
        }
    ],
];
```

**Adding Custom Action Button:**

```php
$actions = [
    ['type' => 'edit', 'route' => 'component.edit', 'param' => 'ComponentId'],
    ['type' => 'delete', 'route' => 'component.destroy', 'param' => 'ComponentId'],
    // Add custom action
    [
        'type' => 'view',
        'route' => 'component.view',
        'param' => 'ComponentId',
        'icon' => 'la la-eye',
        'class' => 'info',
        'title' => 'View Details'
    ],
];
```

### Customizing Component Create/Edit Form

**File:** `resources/views/component/create.blade.php`

**Adding New Form Field:**

```blade
<div class="col-md-12">
    <div class="form-group">
        {{ Form::label('NewField', __('New Field')) }}
        {{ Form::text('NewField', null, ['class' => 'form-control', 'id' => 'NewField']) }}
    </div>
</div>
```

**Adding Validation:**

```blade
{{ Form::text('NewField', null, [
    'class' => 'form-control',
    'required' => true,  // HTML5 validation
    'id' => 'NewField'
]) }}
```

**Adding Dropdown:**

```blade
<div class="form-group">
    {{ Form::label('CategoryId', __('Category')) }}
    {{ Form::select('CategoryId', $categories, null, [
        'class' => 'form-control select2',
        'id' => 'CategoryId'
    ]) }}
</div>
```

**Adding JavaScript:**

```blade
@section('script')
<script>
    // Initialize Select2
    $('.select2').select2();
    
    // Custom validation
    $('#CreateRole').on('submit', function(e) {
        var newField = $('#NewField').val();
        if (!newField) {
            alert('New Field is required');
            e.preventDefault();
            return false;
        }
    });
</script>
@endsection
```

### Customizing Item List View

**File:** `resources/views/item/index.blade.php`

**Adding Category Filter Display:**

```blade
@if(isset($categoryName))
<div class="alert alert-info">
    <i class="la la-filter"></i> Showing items for Category: <strong>{{ $categoryName }}</strong>
    <div class="float-right">
        <a href="{{ route('category.index') }}" class="btn btn-sm btn-secondary">
            <i class="la la-arrow-left"></i> Back to Category
        </a>
        <a href="{{ route('item.index') }}" class="btn btn-sm btn-light">Clear Filter</a>
    </div>
</div>
@endif
```

**Custom Column with Link:**

```php
$columns = [
    [
        'key' => 'usage',
        'label' => 'Usage',
        'render' => function ($i) {
            $count = $i->product_count ?? 0;
            if ($count > 0) {
                return '<a href="' . route('product.index') . '?item=' . $i->ItemId . '" 
                    class="badge badge-info">' . $count . ' Products</a>';
            }
            return '<span class="badge badge-secondary">0 Products</span>';
        }
    ],
];
```

### Customizing Item Create/Edit Form

**File:** `resources/views/item/create.blade.php`

**Dynamic SubCategory Dropdown:**

```blade
<div class="form-group">
    {{ Form::label('SubCategoryId', __('Sub Category')) }}
    {{ Form::select('SubCategoryId', ['' => '*'], null, [
        'class' => 'form-control',
        'id' => 'SubCategoryId'
    ]) }}
</div>
```

**JavaScript for Dynamic Dropdown:**

```blade
@section('script')
<script>
    $(document).on('change', '#CategoryId', function() {
        var categoryId = this.value;
        
        // AJAX call to get subcategories
        $.ajax({
            url: '/api/category/' + categoryId + '/subcategories',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                var options = '<option value="">*</option>';
                data.subcategories.forEach(function(item) {
                    options += '<option value="' + item.SubCategoryId + '">' + item.Name + '</option>';
                });
                $('#SubCategoryId').html(options);
            }
        });
    });
</script>
@endsection
```

### Styling Customization

**Custom CSS Classes:**

Add to your custom CSS file:

```css
/* Custom component styles */
.component-custom-class {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
}

/* Custom table cell styles */
.nepl-table-body.custom-cell {
    font-weight: bold;
    color: #007bff;
}
```

**Using Custom Classes in Views:**

```blade
<div class="component-custom-class">
    <!-- Content -->
</div>
```

### JavaScript Customization

**Custom Table Initialization:**

```blade
@section('plugin_js')
<script>
    $(document).ready(function() {
        var tableId = 'componentTable';
        
        // Initialize DataTables with custom options
        var table = initNeplTable(tableId, {
            paging: false,
            info: false,
            ordering: true,
            searching: true,
            // Custom options
            order: [[1, 'asc']],  // Sort by second column
            pageLength: 50
        });
        
        // Custom search handler
        $('#' + tableId + '_search').on('keyup', function() {
            table.search($(this).val()).draw();
        });
        
        // Custom row click handler
        $('#' + tableId + ' tbody').on('click', 'tr', function() {
            var data = table.row(this).data();
            // Custom action
            console.log('Row clicked:', data);
        });
    });
</script>
@endsection
```

### Best Practices for View Development

1. **Use NEPL Standard Components**
   - Always use `<x-nepl-table>` for tables
   - Follow NEPL CSS class naming
   - Maintain consistency

2. **Form Validation**
   - Use HTML5 validation (`required` attribute)
   - Add JavaScript validation for complex rules
   - Show clear error messages

3. **Responsive Design**
   - Use Bootstrap grid system
   - Test on mobile devices
   - Ensure tables are scrollable

4. **Performance**
   - Use pagination for large datasets
   - Lazy load dropdowns if needed
   - Minimize JavaScript in views

5. **Accessibility**
   - Use proper form labels
   - Add ARIA attributes where needed
   - Ensure keyboard navigation works

6. **Code Organization**
   - Keep JavaScript in `@section('plugin_js')`
   - Use external JS files for complex logic
   - Comment complex code sections

---

## 🔧 Component Master Operations

### Operation 1: View Component List

**Purpose:** View all components in the system

**Steps:**

1. **Navigate to Component List**
   - From main menu, go to: **Component** (or navigate to Component section)
   - Component list page will open

2. **View Components**
   - List shows all components
   - Columns displayed:
     - **Name** - Component name
     - **Details** - Component description
   - Components are sorted alphabetically by name

3. **Search Components** (Optional)
   - Use search box at top-right
   - Type component name or details
   - List filters automatically

4. **Navigate Pages** (If many components)
   - Use pagination controls at bottom
   - Shows "Showing X to Y of Z entries"
   - Click page numbers or Next/Previous

**Time Required:** 1 minute

---

### Operation 2: Create New Component

**Purpose:** Add a new component to the system

**Steps:**

1. **Open Component List**
   - Navigate to Component section
   - View existing components

2. **Click "Add New Component" Button**
   - Look for "+" button in top-right corner
   - Or click "Add New Component" link
   - Create form will open

3. **Fill Component Information**
   
   **Required Field:**
   - **Name** - Enter component name
     - Example: "Circuit Breaker"
     - Example: "Contactors"
     - Example: "Relays"
     - Use clear, descriptive names
     - Use title case (e.g., "Circuit Breaker" not "circuit breaker")
   
   **Optional Field:**
   - **Details** - Enter component description
     - Example: "Standard circuit breaker components"
     - Example: "Electrical contactors for motor control"
     - Provide additional context if helpful

4. **Save Component**
   - Click **"Save"** or **"Submit"** button
   - System validates that Name is provided
   - If Name is missing, error message appears

5. **Verify Creation**
   - You will be redirected to component list
   - Success message appears: "Component added successfully"
   - New component appears in the list
   - Verify name and details are correct

**Validation Rules:**
- Name is required (cannot be empty)
- No duplicate checking (same name can exist multiple times)

**Time Required:** 2-3 minutes

**Tips:**
- Use consistent naming conventions
- Keep names clear and descriptive
- Fill Details field if it adds value

---

### Operation 3: Edit Existing Component

**Purpose:** Update component information

**Steps:**

1. **Open Component List**
   - Navigate to Component section
   - Find component to edit

2. **Click Edit Button**
   - Find the component row
   - Click **Edit** icon/button (usually pencil icon)
   - Edit form will open with current data

3. **Modify Component Information**
   - **Name** - Update if needed
     - Cannot be empty (required field)
   - **Details** - Update if needed
     - Can be left empty (optional field)

4. **Save Changes**
   - Click **"Update"** or **"Save"** button
   - System validates Name is provided
   - If validation fails, error message appears

5. **Verify Update**
   - You will be redirected to component list
   - Success message appears: "Component Updated successfully"
   - Updated component shows new information
   - Verify changes are correct

**Time Required:** 2-3 minutes

**Note:** Changes take effect immediately. No impact on other records.

---

### Operation 4: Delete Component

**Purpose:** Remove component from system

**Steps:**

1. **Open Component List**
   - Navigate to Component section
   - Find component to delete

2. **Click Delete Button**
   - Find the component row
   - Click **Delete** icon/button (usually trash icon)
   - Confirmation may appear (depending on system settings)

3. **Confirm Deletion**
   - If confirmation dialog appears, click **"Confirm"** or **"Yes"**
   - Component is deleted immediately

4. **Verify Deletion**
   - Component disappears from list
   - Success message appears: "Component deleted successfully"
   - Component cannot be recovered (permanent deletion)

**Warning:** 
- ⚠️ **Permanent Deletion** - Component cannot be recovered after deletion
- ⚠️ **No Dependencies Checked** - Ensure component is not used elsewhere before deleting

**Time Required:** 1 minute

**Best Practice:** Review component usage before deletion. If unsure, keep the component.

---

## 📦 Item Master Operations

### Operation 5: View Item List

**Purpose:** View all items (product types) in the system

**Steps:**

1. **Navigate to Item List**
   - From main menu, go to: **Product Type** (or navigate to Item section)
   - Item list page will open

2. **View Items**
   - List shows all items
   - Columns displayed:
     - **Item Name** - Product type name
     - **Category** - Category this item belongs to
     - **Details** - Item description
     - **Usage** - Number of products using this item type
   - Items are sorted alphabetically by name

3. **Filter by Category** (Optional)
   - If you came from Category page, items are filtered automatically
   - Filter indicator shows at top: "Showing items for Category: [Category Name]"
   - Click **"Clear Filter"** to view all items

4. **Search Items** (Optional)
   - Use search box at top-right
   - Type item name, category, or details
   - List filters automatically

5. **View Product Usage**
   - **Usage** column shows number of products using this item
   - Click on usage count (e.g., "5 Products") to view those products
   - Opens product list filtered by this item type

6. **Navigate Pages** (If many items)
   - Use pagination controls at bottom
   - Shows "Showing X to Y of Z entries"
   - Click page numbers or Next/Previous

**Time Required:** 1-2 minutes

---

### Operation 6: Create New Item (Product Type)

**Purpose:** Add a new item/product type to the system

**Prerequisites:**
- ✅ Category must exist in system
- ✅ SubCategory must exist (if you want to use it)

**Steps:**

1. **Open Item List**
   - Navigate to Product Type section
   - View existing items

2. **Click "Add New Item" Button**
   - Look for "+" button in top-right corner
   - Or click "Add New Item" link
   - Create form will open

3. **Fill Item Information**
   
   **Required Fields:**
   - **Category** - Select from dropdown
     - Click dropdown to see available categories
     - Select appropriate category
     - Example: "Electrical Panels"
     - Example: "Cables"
     - **Cannot be empty** - must select a category
   
   - **Name** - Enter item/product type name
     - Example: "Indoor Distribution Panel"
     - Example: "Outdoor Distribution Panel"
     - Example: "Armored Cable"
     - Example: "Flexible Cable"
     - Use functional classification names
     - Be specific and descriptive
     - Use title case
     - **Cannot be empty** - must provide name
   
   **Optional Fields:**
   - **SubCategory** - Select from dropdown (if available)
     - Dropdown populates based on selected Category
     - Select if you want to further classify
     - Example: "Distribution Panels" (under Electrical Panels)
     - Can be left empty
   
   - **Details** - Enter item description
     - Example: "Standard indoor distribution panel type for residential/commercial use"
     - Example: "Armored cable suitable for underground installation"
     - Provide additional context if helpful
     - Can be left empty

4. **Save Item**
   - Click **"Save"** or **"Submit"** button
   - System validates:
     - Name is provided
     - Category is selected
   - If validation fails, error message appears showing what's missing

5. **Verify Creation**
   - You will be redirected to item list
   - Success message appears: "Product Type added successfully"
   - New item appears in the list
   - Verify:
     - Name is correct
     - Category name is displayed correctly
     - Usage count shows "0 Products" (initially)
     - Details are correct (if provided)

**Validation Rules:**
- Name is required (cannot be empty)
- Category is required (must select from dropdown)
- SubCategory is optional (can be left empty)
- Details is optional (can be left empty)

**Time Required:** 3-5 minutes

**Tips:**
- Plan item structure before creation
- Use functional classification names
- Be specific and descriptive
- Consider product classification needs
- Fill Details field for documentation

---

### Operation 7: Edit Existing Item

**Purpose:** Update item/product type information

**Steps:**

1. **Open Item List**
   - Navigate to Product Type section
   - Find item to edit

2. **Click Edit Button**
   - Find the item row
   - Click **Edit** icon/button (usually pencil icon)
   - Edit form will open with current data

3. **Modify Item Information**
   - **Category** - Update if needed
     - Select different category from dropdown
     - **Warning:** Changing category may affect product classification
   
   - **SubCategory** - Update if needed
     - Select different subcategory or clear selection
     - Dropdown updates based on selected category
   
   - **Name** - Update if needed
     - Cannot be empty (required field)
   
   - **Details** - Update if needed
     - Can be left empty (optional field)

4. **Save Changes**
   - Click **"Update"** or **"Save"** button
   - System validates:
     - Name is provided
     - Category is selected
   - If validation fails, error message appears

5. **Verify Update**
   - You will be redirected to item list
   - Success message appears: "Product Type Updated successfully"
   - Updated item shows new information
   - Verify:
     - Name is correct
     - Category name is displayed correctly
     - Usage count remains accurate
     - Details are correct (if provided)

**Impact of Changes:**
- Changing Category/SubCategory affects product classification
- Products using this item type will reflect new category
- Review product impact before making category changes

**Time Required:** 3-5 minutes

**Best Practice:** Review product usage before changing category to understand impact.

---

### Operation 8: Delete Item (Product Type)

**Purpose:** Remove item/product type from system

**Prerequisites:**
- ✅ No products must be using this item type
- ✅ Check usage count before attempting deletion

**Steps:**

1. **Open Item List**
   - Navigate to Product Type section
   - Find item to delete

2. **Check Product Usage**
   - Look at **Usage** column for the item
   - If count is **0 Products**:
     - Safe to delete
     - Proceed to step 3
   - If count is **> 0** (e.g., "5 Products"):
     - ⚠️ **Cannot delete** - products are using this item
     - Click on usage count to see which products
     - You must either:
       - Delete those products first, OR
       - Reassign those products to different item type, OR
       - Keep the item (recommended if products are active)

3. **Click Delete Button** (Only if usage = 0)
   - Find the item row
   - Click **Delete** icon/button (usually trash icon)
   - System checks for products using this item
   - If products exist, deletion is blocked

4. **Handle Deletion Result**
   
   **If Deletion Succeeds:**
   - Item disappears from list
   - Success message appears: "Product Type deleted successfully"
   - Item cannot be recovered (permanent deletion)
   
   **If Deletion Fails:**
   - Error message appears: "There are many Product Create to this Product Type."
   - Item remains in list
   - You must handle products first (see step 2)

**Error Handling:**
- If products exist, you cannot delete the item
- System prevents deletion to maintain data integrity
- Must delete or reassign products first

**Time Required:** 2-5 minutes (depending on product handling)

**Best Practice:** 
- Always check usage count before attempting deletion
- Review products using the item
- Consider keeping item if products are active
- Only delete if absolutely necessary and no products exist

---

### Operation 9: Assign Attributes to Item

**Purpose:** Define required attributes for product type

**Steps:**

1. **Open Item List**
   - Navigate to Product Type section
   - Find item to assign attributes

2. **Click "Assign Attributes" Button**
   - Find the item row
   - Click **"Assign Attributes"** icon/button (usually list/info icon)
   - Attribute assignment page will open

3. **View Available Attributes**
   - List shows available attributes in system
   - Attributes are defined at category level
   - Example attributes:
     - Voltage
     - Current Rating
     - IP Rating
     - Number of Ways
     - Material
     - Color

4. **Select Attributes**
   - Check boxes for attributes to assign to this item type
   - Select attributes relevant to this product type
   - Example: For "Indoor Distribution Panel", select:
     - Voltage
     - Current Rating
     - IP Rating
     - Number of Ways

5. **Save Assignment**
   - Click **"Save"** or **"Assign"** button
   - Attributes are linked to item type
   - Assignment is saved

6. **Verify Assignment**
   - Return to item list
   - Attributes are now required for products using this item type
   - When creating products under this item type, these attributes must be filled

**Impact:**
- Products using this item type must have values for assigned attributes
- Attribute values are required during product creation
- Ensures consistent product data

**Time Required:** 3-5 minutes

**Best Practice:**
- Assign relevant attributes early
- Review attribute assignments regularly
- Keep attribute list focused and manageable

---

### Operation 10: Filter Items by Category

**Purpose:** View items for a specific category

**Method 1: From Category List**

1. **Navigate to Category List**
   - Go to Category section
   - View categories

2. **Click on Category**
   - Find category to view items for
   - Click on category name or "View Items" link
   - Item list opens filtered by this category

3. **View Filtered Items**
   - Item list shows only items for selected category
   - Filter indicator shows at top: "Showing items for Category: [Category Name]"
   - All items displayed belong to this category

4. **Clear Filter** (Optional)
   - Click **"Clear Filter"** button
   - Or navigate directly to Product Type section
   - All items are displayed

**Method 2: Direct Navigation**

1. **Navigate to Item List**
   - Go to Product Type section
   - View all items

2. **Use Category Filter** (If available)
   - Look for category filter dropdown
   - Select category from dropdown
   - List filters automatically

**Time Required:** 1 minute

**Use Case:** 
- View all product types for "Electrical Panels" category
- Organize items by category
- Better category-based management

---

## ⚙️ Configuration Procedures

### Configuration 1: Initial System Setup

**Purpose:** Set up Component/Item Master system for first-time use

**Steps:**

1. **Verify System Access**
   - Ensure you have appropriate user permissions
   - Login to system
   - Verify Component and Product Type sections are visible

2. **Review Existing Data**
   - Check if any components/items already exist
   - Review existing structure
   - Understand current organization

3. **Plan Structure** (For Item Master)
   - Identify categories needed
   - Plan item types for each category
   - Document naming conventions
   - Plan attribute assignments

4. **Create Categories** (If needed)
   - Navigate to Category section
   - Create required categories
   - Example: "Electrical Panels", "Cables", "Transformers"

5. **Create SubCategories** (If needed)
   - Navigate to SubCategory section
   - Create subcategories under categories
   - Example: "Distribution Panels" under "Electrical Panels"

6. **Create Items** (Product Types)
   - Navigate to Product Type section
   - Create item types for each category
   - Follow naming conventions
   - Assign to appropriate categories

7. **Assign Attributes**
   - For each item type, assign relevant attributes
   - Ensure attributes are defined at category level first
   - Assign attributes that products will need

8. **Create Components** (If needed)
   - Navigate to Component section
   - Create basic component references
   - Use for simple lookups

**Time Required:** 2-4 hours (depending on complexity)

**Best Practice:** 
- Plan structure before implementation
- Document naming conventions
- Start with most important categories
- Build incrementally

---

### Configuration 2: Setting Up New Product Line

**Purpose:** Configure system for a new product line

**Steps:**

1. **Create Category** (If new)
   - Navigate to Category section
   - Create new category for product line
   - Example: "Motor Controls"

2. **Create SubCategories** (If needed)
   - Navigate to SubCategory section
   - Create subcategories under new category
   - Example: "VFDs", "Starters", "Contactors"

3. **Create Item Types**
   - Navigate to Product Type section
   - Create item types for each subcategory
   - Example:
     - "Variable Frequency Drive - 1HP to 5HP"
     - "Variable Frequency Drive - 5HP to 10HP"
     - "Direct Online Starter"
     - "Star-Delta Starter"

4. **Assign Attributes**
   - For each item type, assign relevant attributes
   - Example attributes for VFDs:
     - Voltage
     - Power Rating (HP/kW)
     - Control Type
     - Enclosure Type

5. **Verify Configuration**
   - Review item list for new category
   - Verify all item types are created
   - Verify attributes are assigned
   - Test by creating a sample product

**Time Required:** 1-2 hours

---

## 🔧 Maintenance Procedures

### Maintenance 1: Regular Data Review

**Purpose:** Maintain data quality and organization

**Frequency:** Monthly or Quarterly

**Steps:**

1. **Review Component List**
   - Navigate to Component section
   - Review all components
   - Identify:
     - Duplicate components
     - Obsolete components
     - Components with unclear names
     - Missing details

2. **Review Item List**
   - Navigate to Product Type section
   - Review all items
   - Check:
     - Item names are clear and descriptive
     - Items are in correct categories
     - Usage counts are accurate
     - Attributes are assigned appropriately

3. **Clean Up Components**
   - Delete obsolete components (if safe)
   - Update unclear component names
   - Add missing details
   - Consolidate duplicates (if appropriate)

4. **Clean Up Items**
   - Update unclear item names
   - Move items to correct categories (if needed)
   - Review and update attribute assignments
   - Document any changes

5. **Document Changes**
   - Note any changes made
   - Update naming conventions if needed
   - Share updates with team

**Time Required:** 1-2 hours

---

### Maintenance 2: Category Reorganization

**Purpose:** Reorganize items when category structure changes

**Steps:**

1. **Plan Reorganization**
   - Identify items to move
   - Identify target categories
   - Document changes needed

2. **Review Product Impact**
   - For each item to move:
     - Check usage count
     - Review products using this item
     - Understand impact of category change

3. **Update Items**
   - Edit each item
   - Change category assignment
   - Update subcategory if needed
   - Save changes

4. **Verify Changes**
   - Review item list
   - Verify items are in correct categories
   - Check product relationships are maintained

5. **Test Product Creation**
   - Create test product under moved item
   - Verify category assignment is correct
   - Verify attributes are still assigned

**Time Required:** 2-4 hours (depending on number of items)

**Warning:** Category changes affect product classification. Review impact carefully.

---

### Maintenance 3: Attribute Review and Update

**Purpose:** Review and update attribute assignments for item types

**Frequency:** Quarterly or when product requirements change

**Steps:**

1. **Review Current Attributes**
   - For each item type:
     - View assigned attributes
     - Review if attributes are still relevant
     - Identify missing attributes
     - Identify unnecessary attributes

2. **Update Attribute Assignments**
   - Navigate to item list
   - Click "Assign Attributes" for each item
   - Add missing attributes
   - Remove unnecessary attributes
   - Save changes

3. **Verify Product Impact**
   - Check products using updated items
   - Ensure products have values for required attributes
   - Update products if needed

4. **Document Changes**
   - Note attribute changes
   - Update documentation
   - Inform team of changes

**Time Required:** 1-2 hours

---

## 🔍 Troubleshooting Guide

### Issue 1: Component Not Appearing in List

**Symptoms:**
- Component was created but not visible in list
- Component missing after creation

**Possible Causes:**
1. Component is on a different page (pagination)
2. Search filter is active
3. Component was not saved successfully

**Solutions:**

**Solution 1: Check Pagination**
- Look at bottom of list for pagination controls
- Navigate to different pages
- Component may be on page 2, 3, etc.

**Solution 2: Clear Search Filter**
- Check if search box has text
- Clear search box
- Component should appear if it matches

**Solution 3: Verify Creation**
- Try creating component again
- Check for error messages
- Verify all required fields are filled
- Contact system administrator if issue persists

**Prevention:**
- Always verify component appears after creation
- Note which page component is on
- Use search to find components

---

### Issue 2: Cannot Delete Item - "Products Exist" Error

**Symptoms:**
- Delete button shows error message
- Message: "There are many Product Create to this Product Type."
- Item cannot be deleted

**Cause:**
- Products in system are using this item type
- System prevents deletion to maintain data integrity

**Solutions:**

**Solution 1: Review Products**
1. Check usage count in item list
2. Click on usage count (e.g., "5 Products")
3. View products using this item
4. Decide: Delete products or keep item

**Solution 2: Delete Products** (If appropriate)
1. Navigate to products using this item
2. Delete products (if safe to do so)
3. Return to item list
4. Delete item (usage count should be 0)

**Solution 3: Reassign Products** (If appropriate)
1. Navigate to products using this item
2. Edit each product
3. Change item type to different item
4. Save changes
5. Return to item list
6. Delete item (usage count should be 0)

**Solution 4: Keep Item** (Recommended)
- If products are active, keep the item
- Item can remain in system even if not actively used
- No harm in keeping unused items

**Prevention:**
- Always check usage count before attempting deletion
- Review products before deleting items
- Consider keeping items if products are active

---

### Issue 3: Category Dropdown Empty When Creating Item

**Symptoms:**
- Category dropdown is empty
- Cannot select category
- Cannot create item

**Possible Causes:**
1. No categories exist in system
2. All categories are inactive/deleted
3. System configuration issue

**Solutions:**

**Solution 1: Create Categories**
1. Navigate to Category section
2. Check if categories exist
3. If no categories, create required categories
4. Return to Product Type section
5. Category dropdown should populate

**Solution 2: Check Category Status**
1. Navigate to Category section
2. Check if categories are active
3. If categories are deleted/inactive, restore or create new
4. Return to Product Type section

**Solution 3: Contact Administrator**
- If categories exist but dropdown is empty
- Contact system administrator
- May be system configuration issue

**Prevention:**
- Ensure categories exist before creating items
- Maintain category master data
- Regular review of category list

---

### Issue 4: SubCategory Not Appearing in Dropdown

**Symptoms:**
- Selected category but SubCategory dropdown is empty
- SubCategory not loading

**Possible Causes:**
1. No subcategories exist for selected category
2. Subcategories are inactive/deleted
3. Browser/JavaScript issue

**Solutions:**

**Solution 1: Check SubCategories**
1. Navigate to SubCategory section
2. Filter by selected category
3. Check if subcategories exist for this category
4. If none exist, create subcategories or proceed without subcategory

**Solution 2: Create SubCategories** (If needed)
1. Navigate to SubCategory section
2. Create subcategories for the category
3. Return to Product Type section
4. Select category again
5. SubCategory dropdown should populate

**Solution 3: Proceed Without SubCategory**
- SubCategory is optional
- Can create item without subcategory
- Leave SubCategory field empty

**Solution 4: Browser Issue**
- Refresh page
- Clear browser cache
- Try different browser
- Contact administrator if issue persists

**Prevention:**
- Create subcategories before creating items (if needed)
- SubCategory is optional - not required for item creation

---

### Issue 5: Validation Error When Saving

**Symptoms:**
- Form shows error message
- Cannot save component/item
- Red error text appears

**Common Causes:**
1. Required field is empty
2. Invalid data entered
3. System validation failed

**Solutions:**

**Solution 1: Check Required Fields**
- **For Component:** Name is required
- **For Item:** Name and Category are required
- Fill all required fields
- Error message will indicate which field is missing

**Solution 2: Review Error Message**
- Read error message carefully
- Error message indicates what's wrong
- Example: "Name field is required"
- Fix indicated issue

**Solution 3: Check Data Format**
- Ensure text fields contain valid text
- Avoid special characters if causing issues
- Use standard text format

**Solution 4: Retry Save**
- Fix issues indicated by error
- Click Save again
- Should save successfully

**Prevention:**
- Always fill required fields
- Read form labels carefully
- Review data before saving

---

### Issue 6: Item Usage Count Shows Zero But Products Exist

**Symptoms:**
- Usage count shows "0 Products"
- But products exist that should use this item
- Count seems incorrect

**Possible Causes:**
1. Products not properly linked to item
2. Products have different item type assigned
3. Data inconsistency

**Solutions:**

**Solution 1: Check Product Item Assignment**
1. Navigate to Product section
2. Filter by this item type
3. Check if products are assigned to this item
4. If not, products need to be updated

**Solution 2: Update Products**
1. For each product using this item:
   - Edit product
   - Verify item type is selected correctly
   - Save product
2. Return to item list
3. Usage count should update

**Solution 3: Contact Administrator**
- If products are correctly assigned but count is wrong
- Contact system administrator
- May be data synchronization issue

**Prevention:**
- Always verify item assignment when creating products
- Regular data review
- Maintain data consistency

---

## ✅ Best Practices

### Component Master Best Practices

1. **Naming Consistency**
   - Use consistent naming conventions
   - Use title case (e.g., "Circuit Breaker" not "circuit breaker")
   - Keep names clear and descriptive
   - Document naming rules for team

2. **Details Field Usage**
   - Fill Details field if it adds value
   - Use for clarification, not duplication
   - Keep details concise
   - Don't duplicate name in details

3. **Regular Review**
   - Review component list periodically
   - Remove obsolete components
   - Update unclear names
   - Maintain data quality

4. **Avoid Overuse**
   - Use components for simple reference only
   - Don't duplicate product data
   - Use Product Master for actual products

---

### Item Master Best Practices

1. **Hierarchy Planning**
   - Plan item structure before creation
   - Consider product classification needs
   - Maintain consistent hierarchy levels
   - Document structure decisions

2. **Naming Strategy**
   - Use functional classification names
   - Be specific and descriptive
   - Avoid generic names like "Type 1", "Type 2"
   - Use title case consistently

3. **Category Organization**
   - Organize items by category logically
   - Use category filtering effectively
   - Maintain category structure
   - Review category assignments regularly

4. **Attribute Management**
   - Assign relevant attributes early
   - Review attribute assignments regularly
   - Keep attribute list focused
   - Remove unnecessary attributes

5. **Product Relationship Awareness**
   - Always check usage count before deletion
   - Understand impact of changes
   - Review products before modifying items
   - Maintain data integrity

6. **Documentation**
   - Document item purposes
   - Use Details field for notes
   - Maintain item catalog documentation
   - Share updates with team

---

### General Best Practices

1. **Data Entry**
   - Fill all required fields
   - Use consistent naming
   - Add details when helpful
   - Review before saving

2. **Data Maintenance**
   - Regular data review
   - Clean up obsolete records
   - Update unclear names
   - Maintain data quality

3. **Error Handling**
   - Read error messages carefully
   - Fix issues before retrying
   - Contact administrator if needed
   - Document recurring issues

4. **Team Communication**
   - Share naming conventions
   - Document structure decisions
   - Communicate changes
   - Maintain consistency

---

## 📖 Quick Reference

### Component Master Quick Reference

| Operation | Route | Required Fields | Time |
|-----------|-------|----------------|------|
| View List | Component section | - | 1 min |
| Create | Component → Add New | Name | 2-3 min |
| Edit | Component → Edit button | Name | 2-3 min |
| Delete | Component → Delete button | - | 1 min |

**Validation:**
- Name: Required
- Details: Optional

---

### Item Master Quick Reference

| Operation | Route | Required Fields | Time |
|-----------|-------|----------------|------|
| View List | Product Type section | - | 1-2 min |
| Create | Product Type → Add New | Name, Category | 3-5 min |
| Edit | Product Type → Edit button | Name, Category | 3-5 min |
| Delete | Product Type → Delete button | Usage = 0 | 2-5 min |
| Assign Attributes | Product Type → Assign Attributes | - | 3-5 min |
| Filter by Category | Category → View Items | - | 1 min |

**Validation:**
- Name: Required
- Category: Required
- SubCategory: Optional
- Details: Optional

**Deletion Rules:**
- Cannot delete if products use this item
- Check usage count before deletion
- Must delete/reassign products first

---

### Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Name field is required" | Name is empty | Fill Name field |
| "Category field is required" | Category not selected | Select category |
| "There are many Product Create to this Product Type" | Products exist | Delete/reassign products or keep item |
| Component/Item not appearing | Pagination/Search | Check pages, clear search |

---

## 📚 Revision History

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial operational manual created | Separated from technical document, focused on user operations only |
| 1.1 | 2025-12-15 | Auto | Added frontend technical architecture, database schema, and view development sections | Includes frontend architecture, database schema for understanding, and view customization guide |

---

**END OF DOCUMENT**

**This manual provides complete operational, configuration, and maintenance procedures for Component/Item Master system. Use this guide for daily operations, system configuration, and troubleshooting.**

