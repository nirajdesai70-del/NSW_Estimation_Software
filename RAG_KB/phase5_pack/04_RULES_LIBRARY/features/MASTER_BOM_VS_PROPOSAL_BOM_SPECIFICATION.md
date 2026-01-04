---
Source: features/master_bom/_general/MASTER_BOM_VS_PROPOSAL_BOM_SPECIFICATION.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T01:43:16.858585
KB_Path: phase5_pack/04_RULES_LIBRARY/features/MASTER_BOM_VS_PROPOSAL_BOM_SPECIFICATION.md
---

> Source: source_snapshot/MASTER_BOM_VS_PROPOSAL_BOM_SPECIFICATION.md
> Bifurcated into: features/master_bom/_general/MASTER_BOM_VS_PROPOSAL_BOM_SPECIFICATION.md
> Module: Master BOM > General (Comparison)
> Date: 2025-12-17 (IST)

# Master BOM vs Proposal BOM - Detailed Specification

## 📋 CURRENT STATE ANALYSIS

### Master BOM Structure

#### Index Page (`masterbom/index.blade.php`)
- **Layout:**
  - Uses `@extends('layouts.app')`
  - Has `@section('titleright')` with "Add New" button
  - Uses `<x-nepl-table>` component
  - Same JavaScript initialization

- **Columns:**
  1. Sr No (auto-indexed)
  2. BOM Name (sortable)
  3. Unique No (sortable)
  4. Description (not sortable)

- **Actions:**
  1. Copy (blue icon, `la la-copy`)
  2. Edit (green icon, `la la-edit`)
  3. Delete (red icon, `la la-trash-o`)

- **Features:**
  - Search functionality
  - Show entries dropdown (10, 25, 50, 100)
  - Pagination
  - Sortable columns

#### Edit Page (`masterbom/edit.blade.php`)
- **Layout:**
  - Header with "Back" button
  - BOM Details section (Name, Unique No, Description)
  - Items table with:
    - Category dropdown
    - Sub Category dropdown
    - Product Type dropdown
    - Generic dropdown
    - Description field
    - QTY field (integer only)
    - Delete button (X)
  - "+ Add More" button
  - Save/Cancel buttons

#### Controller Functions
- `index()` - List with pagination
- `create()` - Show create form
- `store()` - Save new BOM
- `edit($id)` - Show edit form
- `update($id)` - Update BOM
- `copy($id)` - Copy BOM
- `destroy($id)` - Delete BOM
- `addmore()` - AJAX add item row
- `remove()` - AJAX remove item
- `getsubcategory()` - AJAX cascade
- `getproducttype()` - AJAX cascade
- `getdescription()` - AJAX cascade

---

### Proposal BOM Structure (Current)

#### Index Page (`proposal-bom/index.blade.php`)
- **Layout:**
  - Uses `@extends('layouts.app')`
  - ❌ Missing `@section('titleright')` (no "Add New" button - correct, as Proposal BOMs come from quotations)
  - Uses `<x-nepl-table>` component
  - Same JavaScript initialization

- **Columns:**
  1. Sr No (auto-indexed)
  2. BOM Name (sortable) - with Level badge
  3. Quotation (not sortable, clickable link)
  4. Project (not sortable)
  5. Customer (not sortable)
  6. Components (not sortable, badge display)

- **Actions:**
  1. View only (blue icon, `la la-eye`)

- **Features:**
  - Search functionality
  - Show entries dropdown
  - Pagination
  - Sortable columns

#### Show Page (`proposal-bom/show.blade.php`)
- **Layout:**
  - Header with "Back to List" button
  - BOM Details section (read-only)
  - Components table (read-only)

#### Controller Functions
- `index()` - List with pagination
- `show($id)` - View details (read-only)

---

## 🎯 STANDARDIZATION REQUIREMENTS

### 1. Index Page Standardization

**Both should have:**
- ✅ Same layout structure
- ✅ Same NEPL table component usage
- ✅ Same JavaScript initialization
- ✅ Same search functionality
- ✅ Same pagination controls
- ✅ Same "Show entries" dropdown

**Differences (by design):**
- Master BOM: Has "Add New" button (creates new BOM)
- Proposal BOM: No "Add New" button (BOMs come from past quotations)

**Actions to add to Proposal BOM:**
- ✅ View (already exists)
- ➕ Copy/Reuse (similar to Master BOM Copy) - Reuse in new quotation
- ➕ Promote to Master BOM (convert Proposal BOM to Master BOM template)

### 2. Show/Edit Page Standardization

**Master BOM Edit Page Structure:**
```
┌─────────────────────────────────────────┐
│ Master BOM Edit              [← Back]   │
├─────────────────────────────────────────┤
│ BOM Details:                            │
│   Name: [input]                         │
│   Unique No: [input]                    │
│   Description: [input]                  │
├─────────────────────────────────────────┤
│ Items:                    [+ Add More]  │
│ ┌─────────────────────────────────────┐ │
│ │ Cat │ SubCat │ Type │ Gen │ Desc │Qty│X│
│ │ ... │  ...   │ ...  │ ... │ ...  │1 │X│
│ └─────────────────────────────────────┘ │
│ [Save] [Cancel]                         │
└─────────────────────────────────────────┘
```

**Proposal BOM Show Page Should Match:**
```
┌─────────────────────────────────────────┐
│ Proposal BOM - {Name}        [← Back]   │
├─────────────────────────────────────────┤
│ BOM Details: (read-only)                │
│   BOM Name: {value}                     │
│   Quotation: {link}                     │
│   Project: {value}                      │
│   Customer: {value}                     │
│   Level: {badge}                        │
│   Quantity: {value}                     │
│   Created: {date}                       │
│   Source: {badge if from Master BOM}    │
├─────────────────────────────────────────┤
│ Components: ({count})                   │
│ ┌─────────────────────────────────────┐ │
│ │ Sr│Cat│Sub│Item│Gen│Make│Ser│Desc│SKU│Qty│Rate│Disc│Net│Amt│
│ │ 1 │...│...│... │...│... │...│... │...│ 1 │0.00│0% │...│...│
│ └─────────────────────────────────────┘ │
│ [Reuse in Quotation] [Promote to Master]│
└─────────────────────────────────────────┘
```

### 3. UI Standardization Rules

**All pages should follow Master BOM index page style:**
- Same card structure (`card nepl-table-wrapper`)
- Same header structure (`card-header d-flex justify-content-between`)
- Same title style (`nepl-page-title`)
- Same table component (`<x-nepl-table>`)
- Same JavaScript patterns
- Same CSS classes

---

## 📝 IMPLEMENTATION PLAN

### Step 1: Update Proposal BOM Index Page
- ✅ Already matches structure
- ➕ Add "Copy/Reuse" action
- ➕ Add "Promote to Master BOM" action (optional)

### Step 2: Update Proposal BOM Show Page
- Match Master BOM Edit page layout structure
- Keep read-only (appropriate for Proposal BOM)
- Add action buttons: "Reuse in Quotation", "Promote to Master BOM"

### Step 3: Add Missing Functions to Proposal BOM Controller
- `copy()` or `reuse()` - Reuse Proposal BOM in new quotation
- `promoteToMaster()` - Convert Proposal BOM to Master BOM template

### Step 4: Standardize All Internal Pages
- Ensure all edit/create/show pages follow same structure
- Use consistent card layouts
- Use consistent button styles
- Use consistent table structures

---

## ✅ SPECIFICATION COMPLETE

Ready to implement changes.


