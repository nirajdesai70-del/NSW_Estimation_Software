> Source: source_snapshot/docs/05_WORKFLOWS/17_QUOTATION_CREATION_FLOW.md
> Bifurcated into: features/quotation/workflows/17_QUOTATION_CREATION_FLOW.md
> Module: Quotation > Workflows
> Date: 2025-12-17 (IST)

# Quotation Creation Flow - Complete Step-by-Step Guide

**Document:** 17_QUOTATION_CREATION_FLOW.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Complete Workflow Diagram](#complete-workflow-diagram)
4. [Detailed Step-by-Step Process](#detailed-step-by-step-process)
5. [Technical Flow](#technical-flow)
6. [Code References](#code-references)
7. [Business Rules](#business-rules)
8. [Troubleshooting](#troubleshooting)

---

## Overview

**Purpose:** This document provides COMPLETE, DETAILED instructions for creating a quotation in the NEPL system, from start to finish.

**Time Required:** 10-30 minutes (depending on complexity)

**User Role:** Sales Person / Quotation Creator

**Result:** A complete quotation ready for PDF generation and client delivery

---

## Prerequisites

### Before You Start, Ensure:

✅ **Master Data Exists:**
- Client created in system
- Project created for client
- Contact person added to client
- Products exist in catalog
- Pricing set for products
- (Optional) Master BOMs created

✅ **User Has Permissions:**
- Logged in as Sales Person or Admin
- Access to Quotation module

✅ **Information Ready:**
- Client name and project details
- Contact person for quotation
- List of products/services to quote
- Quantities needed
- Any special requirements

---

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUOTATION CREATION WORKFLOW                       │
└─────────────────────────────────────────────────────────────────────┘

PHASE 1: NAVIGATION & INITIALIZATION
┌────────────────────┐
│  User Dashboard    │
└────────────────────┘
         │
         │ Click "Quotations" in sidebar
         ▼
┌────────────────────┐
│ Quotation List     │
│ (index page)       │
└────────────────────┘
         │
         │ Click "Create Quotation" button
         ▼
┌────────────────────────────────────────────────────────────────────┐
│                    QUOTATION CREATE FORM                            │
│  Route: GET /quotation/create                                      │
│  Controller: QuotationController@create()                          │
│  View: resources/views/quotation/create.blade.php                  │
└────────────────────────────────────────────────────────────────────┘

PHASE 2: BASIC INFORMATION ENTRY
┌────────────────────────────────────────────────────────────────────┐
│  FORM FIELDS (All Required):                                       │
│                                                                     │
│  1. Client          [Dropdown: Select Client ▼]                    │
│  2. Project         [Dropdown: Select Project ▼]                   │
│  3. Contact Person  [Dropdown: Select Contact ▼]                   │
│  4. Sales Person    [Dropdown: Select Sales Person ▼]              │
│  5. Employee        [Dropdown: Select Employee ▼]                  │
│  6. Quotation No.   [○ Auto-generate  ○ Manual Entry]             │
│                                                                     │
│  MAKE/SERIES SELECTION (Optional - for filtering):                 │
│  Row 1: Category [▼] | Make [▼] | Series [▼] | [Delete]          │
│         [+ Add More Make/Series]                                   │
│                                                                     │
│  [Save Quotation] button                                           │
└────────────────────────────────────────────────────────────────────┘
         │
         │ User fills all fields and clicks "Save"
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  SERVER-SIDE PROCESSING                                            │
│  Route: POST /quotation/store                                      │
│  Controller: QuotationController@store(Request $request)           │
│                                                                     │
│  Steps:                                                             │
│  1. Validate input (all required fields present)                   │
│  2. Generate Quotation Number:                                     │
│     - If Auto: YYMMDD + next sequential (e.g., 220716001)         │
│     - If Manual: Use provided number                               │
│  3. Create quotation record in database                            │
│  4. Create make/series selection records (if provided)             │
│  5. Redirect to quotation list with success message                │
└────────────────────────────────────────────────────────────────────┘
         │
         │ Success! Quotation created
         ▼
┌────────────────────┐
│ Quotation List     │
│ (shows new quote)  │
└────────────────────┘
         │
         │ User clicks "Edit" on new quotation
         ▼
┌────────────────────────────────────────────────────────────────────┐
│                    QUOTATION EDIT PAGE                              │
│  Route: GET /quotation/{id}/edit                                   │
│  Controller: QuotationController@edit($id)                         │
│  View: resources/views/quotation/edit.blade.php                    │
└────────────────────────────────────────────────────────────────────┘

PHASE 3: ADDING SALE ITEMS (Core Content)
┌────────────────────────────────────────────────────────────────────┐
│  QUOTATION EDIT PAGE - Main Content Area                           │
│                                                                     │
│  Basic Info (Read-only): Client, Project, Contact, etc.           │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  SALE ITEMS SECTION                                       │    │
│  │  [+ Add Sale Item] button                                 │    │
│  └──────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
         │
         │ User clicks "Add Sale Item"
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  AJAX CALL                                                          │
│  Route: POST /quotation/addmoresale                                │
│  Controller: QuotationController@addmoresale(Request)              │
│  Returns: HTML partial (saleitem.blade.php)                        │
│                                                                     │
│  Process:                                                           │
│  1. Load quotation data                                            │
│  2. Load available products/BOMs                                   │
│  3. Generate sale item form HTML                                   │
│  4. Return HTML to browser                                         │
└────────────────────────────────────────────────────────────────────┘
         │
         │ HTML inserted into page
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  SALE ITEM FORM (Dynamically Added)                                │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Sale Item #1                                [Collapse ▼]  │    │
│  │  ─────────────────────────────────────────────────────    │    │
│  │  Sale Name:        [Text Input________________]           │    │
│  │  Custom Name:      [Text Input________________]           │    │
│  │  Quantity:         [Number: 1__]                          │    │
│  │  Rate:             [Number: 0.00___]                      │    │
│  │  Amount:           [Calculated: 0.00]                     │    │
│  │                                                             │    │
│  │  [+ Add BOM]  [+ Add Master BOM]                          │    │
│  │                                                             │    │
│  │  BOM Items: (None yet)                                     │    │
│  └──────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
         │
         │ User fills sale item details
         │ Then clicks "Add BOM" or "Add Master BOM"
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  CHOICE: Add BOM or Add Master BOM?                                │
└────────────────────────────────────────────────────────────────────┘
         │
         ├──── Option A: Add BOM (Custom BOM) ────┐
         │                                          │
         │                                          ▼
         │                         ┌─────────────────────────────────┐
         │                         │  AJAX CALL                       │
         │                         │  POST /quotation/addmorebom      │
         │                         │  Returns: bom.blade.php          │
         │                         └─────────────────────────────────┘
         │                                          │
         │                                          ▼
         │                         ┌─────────────────────────────────┐
         │                         │  BOM FORM (Under Sale Item)     │
         │                         │  ┌───────────────────────────┐ │
         │                         │  │ BOM #1      [Collapse ▼]  │ │
         │                         │  │ BOM Name: [Input______]   │ │
         │                         │  │ Quantity: [1__]           │ │
         │                         │  │ Rate: [0.00]              │ │
         │                         │  │                            │ │
         │                         │  │ [+ Add Item]              │ │
         │                         │  │                            │ │
         │                         │  │ BOM Items: (None yet)     │ │
         │                         │  └───────────────────────────┘ │
         │                         └─────────────────────────────────┘
         │                                          │
         │                                          ▼
         │                         (Continue to Add Items)
         │
         └──── Option B: Add Master BOM (From Template) ────┐
                                                              │
                                                              ▼
                                ┌──────────────────────────────────┐
                                │  MODAL POPUP                      │
                                │  "Select Master BOM"              │
                                │                                   │
                                │  [Dropdown: Master BOM List ▼]   │
                                │                                   │
                                │  Master BOM Items Preview:        │
                                │  - Product A (Qty: 2)            │
                                │  - Product B (Qty: 5)            │
                                │  - Product C (Qty: 1)            │
                                │                                   │
                                │  [Cancel] [Add BOM]              │
                                └──────────────────────────────────┘
                                                              │
                                                              │ User selects BOM and clicks "Add"
                                                              ▼
                                ┌──────────────────────────────────┐
                                │  AJAX CALL                        │
                                │  Controller processes Master BOM  │
                                │  Copies all items to quotation    │
                                │  Returns updated HTML             │
                                └──────────────────────────────────┘
                                                              │
                                                              ▼
                                ┌──────────────────────────────────┐
                                │  BOM + ALL ITEMS ADDED            │
                                │  (Pre-populated from template)    │
                                └──────────────────────────────────┘

PHASE 4: ADDING BOM ITEMS
         │
         │ User clicks "Add Item" in BOM
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  AJAX CALL                                                          │
│  Route: POST /quotation/addmoreitem                                │
│  Controller: QuotationController@addmoreitem(Request)              │
│  Returns: item.blade.php                                           │
└────────────────────────────────────────────────────────────────────┘
         │
         │ HTML inserted
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  BOM ITEM FORM (Dynamically Added)                                 │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Item #1                                  [Delete]         │    │
│  │  ──────────────────────────────────────────────────       │    │
│  │  Sr. No: 1                                                 │    │
│  │                                                             │    │
│  │  Product Selection:                                         │    │
│  │  Category:     [Dropdown ▼] → Loads SubCategories         │    │
│  │  SubCategory:  [Dropdown ▼] → Loads Items                 │    │
│  │  Item:         [Dropdown ▼] → Loads Generic Products      │    │
│  │  Generic:      [Dropdown ▼] → Loads Makes                 │    │
│  │  Make:         [Dropdown ▼] → Loads Series                │    │
│  │  Series:       [Dropdown ▼] → Loads Descriptions          │    │
│  │  Description:  [Dropdown ▼] → Sets Rate automatically     │    │
│  │                                                             │    │
│  │  SKU:          [Auto-filled from selection]                │    │
│  │  Remark:       [Text area________________]                 │    │
│  │  Quantity:     [Number: 1__]                               │    │
│  │  Rate:         [Number: 0.00___] (auto-loaded from price) │    │
│  │  Discount:     [Number: 0.00___]                           │    │
│  │  Net Rate:     [Calculated: Rate - Discount]              │    │
│  │  Amount:       [Calculated: Qty × Net Rate]               │    │
│  └──────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
         │
         │ User selects product through cascading dropdowns
         │ Each selection triggers AJAX to load next level
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  CASCADE AJAX CALLS (Automatic as user selects):                   │
│                                                                     │
│  1. Select Category → GET /quotation/generic/{categoryId}         │
│     → Returns: Generic products for category                       │
│                                                                     │
│  2. Select Generic → GET /quotation/make/{genericId}               │
│     → Returns: Makes available for this generic                    │
│                                                                     │
│  3. Select Make → GET /quotation/series/{makeId}                   │
│     → Returns: Series available for this make                      │
│                                                                     │
│  4. Select Series → GET /quotation/description/{seriesId}          │
│     → Returns: Specific products (SKUs)                            │
│                                                                     │
│  5. Select Description → GET /quotation/price/{productId}          │
│     → Returns: Current price for product                           │
│     → Auto-fills Rate field                                        │
└────────────────────────────────────────────────────────────────────┘
         │
         │ Product fully configured with rate
         │ User can add more items or save
         ▼

PHASE 5: SAVING THE QUOTATION
┌────────────────────────────────────────────────────────────────────┐
│  User clicks "Update Quotation" button                             │
└────────────────────────────────────────────────────────────────────┘
         │
         │ Full page submit with all data
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  SERVER-SIDE PROCESSING                                            │
│  Route: PUT /quotation/{id}                                        │
│  Controller: QuotationController@update(Request, $id)              │
│                                                                     │
│  Process (Complex!):                                                │
│  1. Validate all input data                                        │
│  2. Update quotation header                                        │
│  3. Delete existing sale items (Status=1)                          │
│  4. Loop through submitted sale items:                             │
│     For each sale:                                                  │
│       a. Create/update QuotationSale record                        │
│       b. Loop through BOMs for this sale:                          │
│          - Create/update QuotationSaleBom record                   │
│          - Loop through items in this BOM:                         │
│            * Create QuotationSaleBomItem record                    │
│            * Save: Product, Make, Series, Qty, Rate, Amount        │
│  5. Call stored procedure: quotationAmount($quotationId)           │
│     - Calculates and updates all totals                            │
│  6. Redirect to quotation list with success                        │
└────────────────────────────────────────────────────────────────────┘
         │
         │ Success!
         ▼
┌────────────────────┐
│ Quotation List     │
│ (updated quote)    │
└────────────────────┘

PHASE 6: GENERATING PDF (Optional)
         │
         │ User clicks "PDF" icon
         ▼
┌────────────────────────────────────────────────────────────────────┐
│  PDF GENERATION                                                     │
│  Route: GET /quotation/pdf/{id}                                    │
│  Controller: QuotationController@quotationPdf($id)                 │
│  View: resources/views/quotation/quotationPDF.blade.php            │
│  Library: DomPDF                                                   │
│                                                                     │
│  Process:                                                           │
│  1. Load quotation with all relationships                          │
│  2. Load client, project, contact details                          │
│  3. Load all sale items, BOMs, and items                           │
│  4. Render PDF template with data                                  │
│  5. Generate PDF file                                              │
│  6. Download/Display to user                                       │
└────────────────────────────────────────────────────────────────────┘
         │
         │ PDF ready for client
         ▼
┌────────────────────┐
│ PDF Downloaded     │
│ (Ready to send)    │
└────────────────────┘

END OF WORKFLOW
```

---

## Detailed Step-by-Step Process

### STEP 1: Navigate to Quotation Creation

**1.1 From Dashboard**
- Log in to the system
- You see the main dashboard with sidebar navigation
- **Action:** Click "Quotations" in the left sidebar

**URL:** `/home` → `/quotation`

**What Happens Behind the Scenes:**
```php
// Route: GET /quotation
// Controller: QuotationController@index()
// File: app/Http/Controllers/QuotationController.php:44

public function index()
{
    // Loads all active quotations
    $quotations = Quotation::where('Status',0)
        ->orderBy('QuotationNo', 'DESC')
        ->get();
    
    return view('quotation.index', compact('quotations'));
}
```

**1.2 Quotation List Page**
- You see a table of existing quotations
- Columns: Quotation No, Client, Project, Date, Actions
- **Action:** Click "Create Quotation" button (top right)

**URL:** `/quotation` → `/quotation/create`

---

### STEP 2: Fill Basic Quotation Information

**2.1 Create Form Loads**

**What You See:**
- Page title: "Create Quotation"
- Form with multiple fields
- All fields marked with red * are required

**What Happens Behind the Scenes:**
```php
// Route: GET /quotation/create
// Controller: QuotationController@create()
// File: app/Http/Controllers/QuotationController.php:56

public function create()
{
    // Load data for dropdowns
    $client = Client::pluck('ClientName', 'ClientId')->ToArray();
    $project = Project::pluck('Name', 'ProjectId')->ToArray();
    $quotations = Quotation::pluck('QuotationNo', 'QuotationNo')->ToArray();
    $contact = Contact::pluck('ContactName','ContactId')->ToArray();
    $salesPerson = User::where('Status',1)->pluck('name','id')->ToArray();
    
    return view('quotation.create', compact(
        'client','project','quotations','contact','salesPerson'
    ));
}
```

**2.2 Fill Required Fields**

**Field 1: Client** *
- **Type:** Dropdown
- **Options:** All active clients in system
- **Purpose:** Identifies the customer for this quotation
- **Action:** Select client from dropdown
- **Example:** "ABC Industries Ltd."
- **Database:** Links to `clients.ClientId`

**Field 2: Project** *
- **Type:** Dropdown
- **Options:** All projects (filtered by client recommended)
- **Purpose:** Associates quotation with a specific project
- **Action:** Select project from dropdown
- **Example:** "Factory Expansion Phase 2"
- **Database:** Links to `projects.ProjectId`

**Field 3: Contact Person** *
- **Type:** Dropdown
- **Options:** All contacts (filtered by client recommended)
- **Purpose:** Primary contact for this quotation
- **Action:** Select contact from dropdown
- **Example:** "John Smith - Purchase Manager"
- **Database:** Links to `contacts.ContactId`

**Field 4: Sales Person** *
- **Type:** Dropdown
- **Options:** All active users
- **Purpose:** Sales representative handling this quotation
- **Action:** Select sales person (usually yourself)
- **Example:** "Sarah Johnson"
- **Database:** Links to `users.id` (SalesId column)

**Field 5: Employee** *
- **Type:** Dropdown  
**Options:** All active users
- **Purpose:** Employee responsible for quotation execution
- **Action:** Select employee
- **Example:** "Mike Chen - Project Manager"
- **Database:** Links to `users.id` (EmployeeId column)

**Field 6: Quotation Number**
- **Type:** Radio button choice + text input
- **Options:**
  - ○ Auto-generate (Recommended)
  - ○ Manual entry
- **Purpose:** Unique identifier for quotation
- **Action:** 
  - If Auto: Leave radio selected (default)
  - If Manual: Select manual, enter custom number
- **Format:** YYMMDD### (e.g., 220716001)
- **Auto-generation:** System generates next sequential number for today's date
- **Example:** 
  - Auto: 241204001 (Dec 4, 2024, quotation #1)
  - Manual: CUSTOM-2024-001

**2.3 Optional: Make/Series Selection**

**Purpose:** Pre-filter products for faster selection later

**Row Layout:**
```
Category: [Dropdown ▼] | Make: [Dropdown ▼] | Series: [Dropdown ▼] | [Delete ✕]
```

**Actions:**
- Select Category (e.g., "Electrical Panels")
- Select Make (e.g., "Siemens")
- Select Series (e.g., "SIVACON S8")
- Click "+ Add More Make/Series" to add additional rows
- This helps filter products when adding items later

**Database:** Saved to `quotation_make_series` table

---

### STEP 3: Save Initial Quotation

**3.1 Click "Save Quotation" Button**

**What Happens:**
1. Browser validates required fields
2. If valid, form submits to server
3. Server processes the request

**Server-Side Processing (Detailed):**

```php
// Route: POST /quotation/store
// Controller: QuotationController@store(Request $request)
// File: app/Http/Controllers/QuotationController.php:66

public function store(Request $request)
{
    // STEP 1: Validation
    $validation = [
        'ClientId'    => 'required',
        'ProjectId'   => 'required',
        'ContactId'   => 'required',
        'SalesId'     => 'required',
        'EmployeeId'  => 'required',
    ];
    
    $validator = Validator::make($request->all(), $validation);
    
    if ($validator->fails()) {
        return redirect()->back()->with('error', 'Please fill all required fields');
    }
    
    // STEP 2: Generate or use Quotation Number
    $QuotationNo = $request->QuotationNo;
    $date = date('ymd'); // e.g., "220716"
    
    if($QuotationNo == 0) { // Auto-generate
        // Query: Find highest quotation number for today
        $v_StartNo1 = DB::select(
            "SELECT CONCAT(?, LPAD(CAST(MAX(RIGHT(QuotationNo, 3)) + 1 AS CHAR), 3, '0')) AS MaxNumber 
             FROM quotations 
             WHERE QuotationNo LIKE ?",
            [$date, $date.'%']
        );
        
        // If quotations exist today, increment; otherwise start at 001
        $QuotationNo = $v_StartNo1[0]->MaxNumber != null 
            ? $v_StartNo1[0]->MaxNumber 
            : $date.'001';
            
        // Example results:
        // - First quote today: 220716001
        // - Second quote today: 220716002
        // - Tenth quote today: 220716010
    }
    
    // STEP 3: Create Quotation Record
    $Quotation = [
        'ClientId'    => $request->ClientId,
        'ProjectId'   => $request->ProjectId,
        'ContactId'   => $request->ContactId,
        'SalesId'     => $request->SalesId,
        'EmployeeId'  => $request->EmployeeId,
        'QuotationNo' => $QuotationNo,
        'Status'      => 0, // Active
    ];
    
    $quotation = Quotation::create($Quotation);
    $QuotationId = $quotation->QuotationId; // Get new ID
    
    // STEP 4: Save Make/Series Selections (if provided)
    $counts = $request->count; // Number of make/series rows
    
    if($request->has('QuotationMakeSeriesId')) {
        foreach($counts as $count){
            $CategoryId = $request->{'CategoryId_'.$count};
            $MakeId = $request->{'MakeId_'.$count};
            $SeriesId = $request->{'SeriesId_'.$count};
            
            if($CategoryId || $MakeId || $SeriesId) {
                QuotationMakeSeries::create([
                    'QuotationId' => $QuotationId,
                    'CategoryId'  => $CategoryId ?? 0,
                    'MakeId'      => $MakeId ?? 0,
                    'SeriesId'    => $SeriesId ?? 0,
                ]);
            }
        }
    }
    
    // STEP 5: Success! Redirect to list
    return redirect()->route('quotation.index')
        ->with('success', 'Quotation created successfully! Quotation No: ' . $QuotationNo);
}
```

**3.2 Success Message**
- You're redirected to quotation list
- Green success message appears
- New quotation appears in the table
- **Next Action:** Click "Edit" icon on the new quotation

---

### STEP 4: Edit Quotation to Add Items

**4.1 Navigate to Edit Page**
- From quotation list, click Edit icon (pencil) for your new quotation
- **URL:** `/quotation/{id}/edit`

**What Loads:**

```php
// Controller: QuotationController@edit($id)
// File: app/Http/Controllers/QuotationController.php:164

public function edit($id)
{
    // Load quotation
    $quotation = Quotation::find($id);
    
    // Load related data for dropdowns
    $client = Client::pluck('ClientName', 'ClientId')->ToArray();
    $project = Project::pluck('Name', 'ProjectId')->ToArray();
    $contact = Contact::pluck('ContactName','ContactId')->ToArray();
    $salesPerson = User::where('Status',1)->pluck('name','id')->ToArray();
    $category = Category::pluck('Name', 'CategoryId')->ToArray();
    
    // Load existing make/series selections
    $makeSeriesSelections = QuotationMakeSeries::where('QuotationId', $id)->get();
    
    return view('quotation.edit', compact(
        'quotation', 'client', 'project', 'contact', 
        'salesPerson', 'category', 'makeSeriesSelections'
    ));
}
```

**Page Layout:**

```
┌────────────────────────────────────────────────────────────────┐
│ Edit Quotation: #220716001                                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ BASIC INFORMATION (Editable)                                   │
│ Client:        ABC Industries Ltd. [▼]                         │
│ Project:       Factory Expansion [▼]                           │
│ Contact:       John Smith [▼]                                  │
│ Sales Person:  Sarah Johnson [▼]                               │
│ Employee:      Mike Chen [▼]                                   │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ SALE ITEMS                                                      │
│ [+ Add Sale Item] button                                       │
│                                                                 │
│ (Currently empty - no sale items yet)                          │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ [Update Quotation] button                                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### STEP 5: Add Sale Items

**5.1 Click "Add Sale Item"**

**What Happens:**
1. JavaScript triggers AJAX call
2. Server generates HTML for sale item form
3. HTML inserted into page dynamically

**AJAX Request:**
```javascript
// Client-side JavaScript
$.ajax({
    url: '/quotation/addmoresale',
    type: 'POST',
    data: {
        count: nextItemCount,
        qid: quotationId,
        _token: csrfToken
    },
    success: function(response) {
        // Insert HTML into page
        $('#saleItemsContainer').append(response);
    }
});
```

**Server Processing:**
```php
// Controller: QuotationController@addmoresale(Request $request)
// Returns: HTML partial view

public function addmoresale(Request $request)
{
    $count = $request->count; // Item counter
    $QuotationId = $request->qid;
    $quotation = Quotation::find($QuotationId);
    
    // Load data for dropdowns
    $quotationSale = []; // Empty for new item
    $MasterBom = MasterBom::pluck('Name', 'MasterBomId')->ToArray();
    $Category = Category::pluck('Name', 'CategoryId')->ToArray();
    
    // Render partial view
    return view('quotation.saleitem', compact(
        'count', 'quotationSale', 'MasterBom', 
        'Category', 'QuotationId', 'quotation'
    ));
}
```

**5.2 Sale Item Form Appears**

**Form Fields:**

```
┌────────────────────────────────────────────────────────────────┐
│ SALE ITEM #1                                    [Collapse ▼]   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Sale Name: [Text input____________________________________]    │
│ Purpose: Name of the product/service being sold               │
│ Example: "Distribution Panel Assembly"                        │
│                                                                 │
│ Custom Name: [Text input__________________________________]    │
│ Purpose: Display name for quotation/PDF                       │
│ Example: "Complete Distribution Panel System - 100A"          │
│                                                                 │
│ Quantity: [Number: 1___]                                       │
│ Purpose: Number of units                                       │
│ Example: 2 (two assemblies)                                   │
│                                                                 │
│ Rate: [Number: 0.00_____]                                      │
│ Purpose: Price per unit                                        │
│ Example: 50000.00                                              │
│                                                                 │
│ Amount: [Calculated: 100000.00]                                │
│ Purpose: Total (Qty × Rate)                                    │
│ Auto-calculated, read-only                                     │
│                                                                 │
│ Margin %: [Number: 0___]                                       │
│ Purpose: Profit margin percentage                              │
│ Example: 15                                                    │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ [+ Add BOM]  [+ Add Master BOM]                               │
│                                                                 │
│ BOM ITEMS: (None yet)                                          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**5.3 Fill Sale Item Details**
- Enter sale name
- Enter custom display name (optional)
- Enter quantity
- Enter rate (price per unit)
- Amount auto-calculates (Qty × Rate)
- Add margin if needed

---

### STEP 6: Add BOM to Sale Item

**6.1 Choose Method**

**Option A: Add Custom BOM**
- Click "+ Add BOM" button
- Creates empty BOM form
- You manually add items

**Option B: Add Master BOM (Template)**
- Click "+ Add Master BOM" button
- Modal popup appears
- Select from pre-created BOM templates
- All items auto-populated

Let's detail both options...

**6.2 Option A: Add Custom BOM**

**Click "+ Add BOM"**

**AJAX Call:**
```javascript
$.ajax({
    url: '/quotation/addmorebom',
    type: 'POST',
    data: {
        count: bomCounter,
        sid: saleItemId,
        qid: quotationId,
        _token: csrfToken
    },
    success: function(html) {
        $('#bomContainer_' + saleItemId).append(html);
    }
});
```

**BOM Form Appears:**

```
┌────────────────────────────────────────────────────────────────┐
│   BOM #1                                        [Collapse ▼]   │
│   ────────────────────────────────────────────────────────     │
│                                                                 │
│   BOM Name: [Text input_______________________________]        │
│   Purpose: Name of this BOM                                    │
│   Example: "Panel Components"                                  │
│                                                                 │
│   Quantity: [Number: 1___]                                     │
│   Rate: [Number: 0.00_____]                                    │
│   Amount: [Calculated]                                         │
│                                                                 │
│   [+ Add Item]                                                 │
│                                                                 │
│   BOM ITEMS: (None yet)                                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**Continue to Step 7 to add items to this BOM**

**6.3 Option B: Add Master BOM**

**Click "+ Add Master BOM"**

**Modal Opens:**

```
┌────────────────────────────────────────────────────────────────┐
│ Select Master BOM                                      [✕ Close]│
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Master BOM: [Dropdown ▼ Select a BOM template.........] │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ BOM PREVIEW:                                                    │
│ (Select a BOM to see items)                                    │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ [Cancel]                               [Add BOM to Quotation]  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**User Selects BOM:**
- Choose master BOM from dropdown
- Preview shows all items in template
- Click "Add BOM to Quotation"

**What Happens:**
```php
// System copies entire BOM structure:
// 1. Creates QuotationSaleBom record
// 2. For each MasterBomItem:
//    - Creates QuotationSaleBomItem
//    - Copies: ProductId, Quantity
//    - Loads current price for product
```

**Result:**
- BOM + all items appear in quotation
- All pre-configured
- User can still edit quantities/rates

---

### STEP 7: Add Items to BOM

**7.1 Click "+ Add Item" in BOM**

**AJAX Call:**
```php
// Controller: QuotationController@addmoreitem(Request $request)
// Returns: item.blade.php HTML
```

**Item Form Appears:**

```
┌────────────────────────────────────────────────────────────────┐
│ Item #1                                          [Delete ✕]    │
├────────────────────────────────────────────────────────────────┤
│ Sr. No: 1                                                      │
│                                                                 │
│ PRODUCT SELECTION (Cascading Dropdowns):                       │
│                                                                 │
│ Category:     [Select Category ▼__________________]           │
│               ↓ (On select: loads subcategories & generics)   │
│                                                                 │
│ SubCategory:  [Select SubCategory ▼_______________]           │
│               ↓ (Optional: refines product list)              │
│                                                                 │
│ Item:         [Select Item ▼______________________]           │
│               ↓ (Optional: further refines)                   │
│                                                                 │
│ Generic:      [Select Generic Product ▼___________]           │
│               ↓ (On select: loads available makes)            │
│                                                                 │
│ Make:         [Select Make/Brand ▼________________]           │
│               ↓ (On select: loads available series)           │
│                                                                 │
│ Series:       [Select Series ▼____________________]           │
│               ↓ (On select: loads specific products)          │
│                                                                 │
│ Description:  [Select Product SKU ▼_______________]           │
│               ↓ (On select: auto-loads price)                 │
│                                                                 │
│ ─────────────────────────────────────────────────────────────  │
│                                                                 │
│ SKU:          [Auto-filled]                                    │
│ Remark:       [Text area for notes_______________]            │
│                                                                 │
│ Quantity:     [Number: 1___]                                   │
│ Rate:         [Number: 0.00_____] ← Auto-loaded from prices   │
│ Discount %:   [Number: 0___]                                   │
│ Net Rate:     [Calculated: Rate × (1 - Discount/100)]        │
│ Amount:       [Calculated: Quantity × Net Rate]               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**7.2 Product Selection Process (CASCADE)**

This is the CORE of the product selection system!

**Step 1: Select Category**
```javascript
// User selects category: "Electrical Panels"
// Triggers AJAX:
$.get('/quotation/generic/' + categoryId, function(data) {
    // Populates Generic dropdown with products in this category
    $('#generic_dropdown').html(data);
});
```

**Server Side:**
```php
// Controller: QuotationController@getGeneric(Request $request)
public function getGeneric(Request $request) 
{
    $CategoryId = $request->id;
    $SubCategoryId = $request->SubCategoryId ?? 0;
    $ItemId = $request->ItemId ?? 0;
    
    // Query: Get generic products for category
    $Generic = Product::where('CategoryId', $CategoryId)
        ->where('ProductType', 1) // 1 = Generic
        ->where('Status', 0); // Active
    
    if($SubCategoryId != 0) {
        $Generic = $Generic->where('SubCategoryId', $SubCategoryId);
    }
    
    if($ItemId != 0) {
        $Generic = $Generic->where('ItemId', $ItemId);
    }
    
    $Generic = $Generic->pluck('Name','ProductId')->toArray();
    
    return response()->json($Generic);
}
```

**Step 2: Select Generic Product**
```javascript
// User selects: "Distribution Panel - 100A"
// Generic ProductId: 250
// Triggers AJAX:
$.get('/quotation/make/' + genericId, function(data) {
    // Populates Make dropdown
    $('#make_dropdown').html(data);
});
```

**Server Side:**
```php
// Controller: QuotationController@getMake(Request $request)
public function getMake(Request $request)
{
    $CategoryId = $request->CategoryId;
    $ProductId = $request->id; // Generic product
    
    // Get makes that are:
    // 1. Associated with this category
    // 2. Have products under this generic
    
    $Make = MakeCategory::join('makes', 'makes.MakeId', '=', 'make_categories.MakeId')
        ->where('make_categories.CategoryId', $CategoryId)
        ->pluck('makes.Name', 'makes.MakeId')
        ->toArray();
    
    return response()->json($Make);
}
```

**Step 3: Select Make**
```javascript
// User selects: "Siemens"
// MakeId: 5
// Triggers AJAX:
$.get('/quotation/series/' + makeId + '?categoryId=' + categoryId, 
    function(data) {
        // Populates Series dropdown
        $('#series_dropdown').html(data);
    }
);
```

**Server Side:**
```php
// Controller: QuotationController@getSeries(Request $request)
public function getSeries(Request $request)
{
    $MakeId = $request->id;
    $CategoryId = $request->CategoryId;
    
    // Get series for this make and category
    $Series = SeriesMake::join('series', 'series.SeriesId', '=', 'series_makes.SeriesId')
        ->join('series_categories', 'series.SeriesId', '=', 'series_categories.SeriesId')
        ->where('series_makes.MakeId', $MakeId)
        ->where('series_categories.CategoryId', $CategoryId)
        ->select('series.Name', 'series.SeriesId')
        ->get();
    
    return response()->json($Series);
}
```

**Step 4: Select Series**
```javascript
// User selects: "SIVACON S8"
// SeriesId: 7
// Triggers AJAX:
$.get('/quotation/description/' + seriesId + 
    '?genericId=' + genericId + '&makeId=' + makeId,
    function(data) {
        // Populates Description dropdown (specific SKUs)
        $('#description_dropdown').html(data);
    }
);
```

**Server Side:**
```php
// Controller: QuotationController@getDescription(Request $request)
public function getDescription(Request $request)
{
    $SeriesId = $request->id;
    $ProductId = $request->ProductId; // Generic
    $MakeId = $request->MakeId;
    
    // Get specific products (SKUs) matching criteria
    $Description = Product::where('GenericId', $ProductId)
        ->where('MakeId', $MakeId)
        ->where('SeriesId', $SeriesId)
        ->where('ProductType', 2) // 2 = Specific product
        ->select('SKU', 'Description', 'ProductId')
        ->get();
    
    return response()->json($Description);
}
```

**Step 5: Select Description (Final Product)**
```javascript
// User selects specific SKU: "SIV-S8-100A-IP54"
// ProductId: 455
// Triggers AJAX to get price:
$.get('/quotation/price/' + productId, function(data) {
    // Auto-fills Rate field with current price
    $('#rate_field').val(data.rate);
    $('#sku_field').val(data.sku);
});
```

**Server Side:**
```php
// Controller: QuotationController@getPrice(Request $request)
public function getPrice(Request $request)
{
    $ProductId = $request->id;
    $date = date('Y-m-d');
    
    // Get latest price effective on or before today
    $Rate = Price::where('ProductId', $ProductId)
        ->where('EffectiveDate', '<=', $date)
        ->orderBy('EffectiveDate', 'DESC')
        ->first();
    
    $data = [
        'rate' => $Rate ? $Rate->Rate : 0,
        'sku' => $request->sku
    ];
    
    return response()->json($data);
}
```

**7.3 Complete Item Details**
- Product now fully selected
- Rate auto-filled from price database
- User enters:
  - Quantity (how many of this item)
  - Discount (if any)
  - Remark (optional notes)
- System auto-calculates:
  - Net Rate = Rate × (1 - Discount/100)
  - Amount = Quantity × Net Rate

**Example:**
```
Product: Siemens SIVACON S8-100A Panel
Quantity: 2
Rate: 45,000.00 (auto-loaded)
Discount: 5%
Net Rate: 42,750.00 (calculated)
Amount: 85,500.00 (calculated)
```

---

### STEP 8: Repeat for All Items

**8.1 Add More Items**
- Click "+ Add Item" again in same BOM
- Repeat product selection process
- Build complete BOM with all components

**8.2 Add More BOMs**
- Click "+ Add BOM" in sale item
- Add different BOM (e.g., "Accessories", "Installation")
- Add items to each BOM

**8.3 Add More Sale Items**
- Click "+ Add Sale Item" at top
- Create additional top-level items
- Each can have its own BOMs and items

**Typical Structure:**
```
Quotation #220716001
├── Sale Item 1: "Main Distribution Panel"
│   ├── BOM 1: "Panel Components"
│   │   ├── Item 1: Panel enclosure
│   │   ├── Item 2: Circuit breakers (x12)
│   │   └── Item 3: Busbars
│   └── BOM 2: "Accessories"
│       ├── Item 1: Cable glands
│       └── Item 2: Terminal blocks
├── Sale Item 2: "Sub-Distribution Panel"
│   └── BOM 1: "Sub-Panel Components"
│       ├── Item 1: Sub-panel enclosure
│       └── Item 2: MCBs (x6)
└── Sale Item 3: "Installation Services"
    └── BOM 1: "Labor"
        ├── Item 1: Installation labor
        └── Item 2: Testing & commissioning
```

---

### STEP 9: Save Complete Quotation

**9.1 Review Before Saving**
- Scroll through entire quotation
- Verify all items correct
- Check quantities and rates
- Ensure totals look correct

**9.2 Click "Update Quotation"**

**What Happens (Complex Server Processing):**

```php
// Controller: QuotationController@update(Request $request, $id)
// This is the MOST COMPLEX method!

public function update(Request $request, $id)
{
    // STEP 1: Validate
    $validation = [
        'ClientId'   => 'required',
        'ProjectId'  => 'required',
        'ContactId'  => 'required',
        'SalesId'    => 'required',
        'EmployeeId' => 'required',
    ];
    
    $validator = Validator::make($request->all(), $validation);
    if ($validator->fails()) {
        return redirect()->back()->with('error', 'Validation failed');
    }
    
    // STEP 2: Update quotation header
    $QuotationNo = $request->QuotationNo;
    $date = date('ymd');
    
    if($QuotationNo == 0) {
        // Generate new number if needed
        $v_StartNo1 = DB::select(/*...*/);
        $QuotationNo = $v_StartNo1[0]->MaxNumber ?? $date.'001';
    }
    
    Quotation::where('QuotationId', $id)->update([
        'ClientId'    => $request->ClientId,
        'ProjectId'   => $request->ProjectId,
        'ContactId'   => $request->ContactId,
        'SalesId'     => $request->SalesId,
        'EmployeeId'  => $request->EmployeeId,
        'QuotationNo' => $QuotationNo,
        'CategoryId'  => $request->CategoryId ?? 0,
        'MakeId'      => $request->MakeId ?? 0,
        'SeriesId'    => $request->SeriesId ?? 0,
        'Discount'    => $request->Discount ?? 0,
    ]);
    
    // STEP 3: Soft delete existing items (prepare for re-insert)
    QuotationSale::where('QuotationId', $id)->update(['Status' => 1]);
    QuotationSaleBom::where('QuotationId', $id)->update(['Status' => 1]);
    QuotationSaleBomItem::where('QuotationId', $id)->update(['Status' => 1]);
    
    // STEP 4: Process all submitted sale items
    $s_counts = $request->s_count; // Array of sale item indices
    
    if($request->has('QuotationSaleId')) {
        foreach($s_counts as $s_count) {
            // Get sale item data
            $SaleId = $request->{'SaleId_'.$s_count};
            $Name = $request->{'Name_'.$s_count};
            $SaleCustomName = $request->{'SaleCustomName_'.$s_count};
            $Qty = $request->{'Qty_'.$s_count};
            $Rate = $request->{'Rate_'.$s_count};
            $Amount = $Qty * $Rate;
            
            // Create QuotationSale record
            $quotationSale = QuotationSale::create([
                'QuotationId'    => $id,
                'SaleId'         => $SaleId,
                'Name'           => $Name,
                'SaleCustomName' => $SaleCustomName,
                'Qty'            => $Qty,
                'Rate'           => $Rate,
                'Amount'         => $Amount,
                'Margin'         => $request->{'Margin_'.$s_count} ?? 0,
                'MarginAmount'   => $request->{'MarginAmount_'.$s_count} ?? 0,
                'MarginTotal'    => $request->{'MarginTotal_'.$s_count} ?? 0,
                'Status'         => 0,
            ]);
            
            $QuotationSaleId = $quotationSale->QuotationSaleId;
            
            // STEP 5: Process BOMs for this sale item
            $b_counts = $request->{'b_count_'.$s_count}; // BOM indices for this sale
            
            if($b_counts && $request->has('QuotationSaleBomId_'.$s_count)) {
                foreach($b_counts as $b_count) {
                    // Get BOM data
                    $MasterBomId = $request->{'MasterBomId_'.$s_count.'_'.$b_count};
                    $MasterBomName = $request->{'MasterBomName_'.$s_count.'_'.$b_count};
                    $BomQty = $request->{'BomQty_'.$s_count.'_'.$b_count};
                    $BomRate = $request->{'BomRate_'.$s_count.'_'.$b_count};
                    $BomAmount = $BomQty * $BomRate;
                    
                    // Create QuotationSaleBom record
                    $quotationSaleBom = QuotationSaleBom::create([
                        'QuotationId'     => $id,
                        'QuotationSaleId' => $QuotationSaleId,
                        'MasterBomId'     => $MasterBomId,
                        'MasterBomName'   => $MasterBomName,
                        'Qty'             => $BomQty,
                        'Rate'            => $BomRate,
                        'Amount'          => $BomAmount,
                        'Status'          => 0,
                    ]);
                    
                    $QuotationSaleBomId = $quotationSaleBom->QuotationSaleBomId;
                    
                    // STEP 6: Process items for this BOM
                    $i_counts = $request->{'i_count_'.$s_count.'_'.$b_count}; // Item indices
                    
                    if($i_counts && $request->has('QuotationSaleBomItemId_'.$s_count.'_'.$b_count)) {
                        foreach($i_counts as $i_count) {
                            // Get item data
                            $ProductId = $request->{'ProductId_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $MakeId = $request->{'ItemMakeId_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $SeriesId = $request->{'ItemSeriesId_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $Description = $request->{'Description_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $Remark = $request->{'Remark_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $ItemQty = $request->{'ItemQty_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $ItemRate = $request->{'ItemRate_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $ItemDiscount = $request->{'ItemDiscount_'.$s_count.'_'.$b_count.'_'.$i_count};
                            $NetRate = $ItemRate * (1 - $ItemDiscount/100);
                            $ItemAmount = $ItemQty * $NetRate;
                            
                            // Create QuotationSaleBomItem record
                            QuotationSaleBomItem::create([
                                'QuotationId'        => $id,
                                'QuotationSaleId'    => $QuotationSaleId,
                                'QuotationSaleBomId' => $QuotationSaleBomId,
                                'ProductId'          => $ProductId,
                                'MakeId'             => $MakeId,
                                'SeriesId'           => $SeriesId,
                                'Description'        => $Description,
                                'Remark'             => $Remark,
                                'Qty'                => $ItemQty,
                                'Rate'               => $ItemRate,
                                'Discount'           => $ItemDiscount,
                                'NetRate'            => $NetRate,
                                'Amount'             => $ItemAmount,
                                'Status'             => 0,
                            ]);
                        }
                    }
                }
            }
        }
    }
    
    // STEP 7: Calculate totals using stored procedure
    DB::select("CALL quotationAmount(?)", [$id]);
    // This stored procedure:
    // - Sums all item amounts
    // - Applies discounts
    // - Calculates margins
    // - Updates quotation totals
    
    // STEP 8: Success!
    return redirect()->route('quotation.index')
        ->with('success', 'Quotation updated successfully!');
}
```

**Data Saved:**
```
Database Records Created:
- 1 Quotation (header) - UPDATED
- 3 QuotationSale records (sale items)
- 5 QuotationSaleBom records (BOMs across all sales)
- 23 QuotationSaleBomItem records (individual items)
Total: 32 database records for one complete quotation!
```

---

### STEP 10: Generate PDF (Optional)

**10.1 From Quotation List**
- Find your quotation
- Click PDF icon (document icon)
- **URL:** `/quotation/pdf/{id}`

**10.2 PDF Generation Process**

```php
// Controller: QuotationController@quotationPdf($id)
public function quotationPdf($id)
{
    // STEP 1: Load all data
    $quotation = Quotation::with([
        'client',
        'project',
        'contact',
        'sales',      // Sales items
        'sales.boms', // BOMs for each sale
        'sales.boms.items' // Items for each BOM
    ])->find($id);
    
    $client = $quotation->client;
    $project = $quotation->project;
    $contact = $quotation->contact;
    $salesPerson = $quotation->salesPerson;
    $employee = $quotation->employee;
    
    // STEP 2: Load sale items with nested structure
    $quotationSaleData = QuotationSale::where('QuotationId', $id)
        ->where('Status', 0)
        ->get();
    
    $allData = [];
    foreach($quotationSaleData as $sale) {
        $saleData = [
            'Name' => $sale->SaleCustomName,
            'Qty' => $sale->Qty,
            'BOMs' => []
        ];
        
        // Load BOMs for this sale
        $boms = QuotationSaleBom::where('QuotationSaleId', $sale->QuotationSaleId)
            ->where('Status', 0)
            ->get();
        
        foreach($boms as $bom) {
            $bomData = [
                'Name' => $bom->MasterBomName,
                'Items' => []
            ];
            
            // Load items for this BOM
            $items = QuotationSaleBomItem::where('QuotationSaleBomId', $bom->QuotationSaleBomId)
                ->where('Status', 0)
                ->get();
            
            foreach($items as $item) {
                $bomData['Items'][] = [
                    'Product' => $item->product->Name,
                    'Make' => $item->make->Name,
                    'Series' => $item->series->Name,
                    'SKU' => $item->description->SKU,
                    'Qty' => $item->Qty,
                    'Rate' => $item->Rate,
                    'Amount' => $item->Amount,
                    'Remark' => $item->Remark,
                ];
            }
            
            $saleData['BOMs'][] = $bomData;
        }
        
        $allData[] = $saleData;
    }
    
    // STEP 3: Render PDF template
    $pdf = PDF::loadView('quotation.quotationPDF', compact(
        'quotation', 'client', 'project', 'contact', 
        'salesPerson', 'employee', 'allData'
    ));
    
    // STEP 4: Configure PDF settings
    $pdf->setPaper('A4', 'portrait');
    $pdf->setOptions([
        'isHtml5ParserEnabled' => true,
        'isRemoteEnabled' => true,
        'defaultFont' => 'Arial'
    ]);
    
    // STEP 5: Download PDF
    $filename = 'Quotation_' . $quotation->QuotationNo . '.pdf';
    return $pdf->download($filename);
}
```

**PDF Template Layout:**

```
┌────────────────────────────────────────────────────────────────┐
│                   COMPANY HEADER                                │
│              NISH ELECTROMATION                                 │
│           Contact Details, Logo, etc.                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ QUOTATION NO: 220716001                DATE: July 16, 2022     │
│                                                                 │
│ TO:                                                             │
│ ABC Industries Ltd.                                            │
│ Attn: John Smith                                               │
│ Contact: +91-XXXXXXXXXX                                        │
│                                                                 │
│ PROJECT: Factory Expansion Phase 2                             │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ITEMS & PRICING                                                │
│                                                                 │
│ 1. MAIN DISTRIBUTION PANEL                                     │
│    Qty: 2  Rate: 50,000  Amount: 100,000                      │
│                                                                 │
│    Panel Components:                                            │
│    ┌────┬───────────────────┬─────┬──────┬─────────┬────────┐│
│    │ Sr │ Description       │ Qty │ Rate │ Discount│ Amount ││
│    ├────┼───────────────────┼─────┼──────┼─────────┼────────┤│
│    │ 1  │ Panel Enclosure   │  2  │25000 │   0%    │ 50,000 ││
│    │    │ Siemens SIVACON   │     │      │         │        ││
│    │    │ S8-100A-IP54      │     │      │         │        ││
│    ├────┼───────────────────┼─────┼──────┼─────────┼────────┤│
│    │ 2  │ Circuit Breaker   │ 24  │ 1500 │   5%    │ 34,200 ││
│    │    │ ABB Tmax XT1      │     │      │         │        ││
│    └────┴───────────────────┴─────┴──────┴─────────┴────────┘│
│    ...more items...                                            │
│                                                                 │
│ 2. SUB-DISTRIBUTION PANEL                                      │
│    ...similar structure...                                     │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ SUMMARY:                                                        │
│ Subtotal:            2,500,000                                 │
│ Discount (5%):        -125,000                                 │
│ GST (18%):            427,500                                  │
│ ────────────────────────────────                               │
│ TOTAL:              2,802,500                                  │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ TERMS & CONDITIONS:                                            │
│ - Delivery: 4-6 weeks                                          │
│ - Payment: 50% advance, 50% on delivery                       │
│ - Warranty: 12 months                                          │
│ - Validity: 30 days                                            │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ For NISH ELECTROMATION                                         │
│                                                                 │
│ _______________________                                         │
│ Authorized Signatory                                           │
│                                                                 │
│ Sales Person: Sarah Johnson                                    │
│ Date: July 16, 2022                                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**PDF Downloaded!**
- Professional quotation ready to send to client
- All details included
- Company branding applied
- Ready for printing

---

## Technical Flow Summary

### Complete Request/Response Cycle

```
USER ACTION               ROUTE                    CONTROLLER METHOD              DATABASE OPERATIONS
───────────────────────── ──────────────────────── ────────────────────────────── ─────────────────────────
1. Click "Quotations"     GET /quotation           index()                        SELECT quotations
   
2. Click "Create"         GET /quotation/create    create()                       SELECT clients, projects,
                                                                                   contacts, users
   
3. Fill form, submit      POST /quotation/store    store(Request)                 INSERT quotation
                                                                                   INSERT quotation_make_series
   
4. Click "Edit"           GET /quotation/1/edit    edit($id)                      SELECT quotation + relations
   
5. Click "Add Sale"       POST /addmoresale        addmoresale(Request)           SELECT quotation data
   (AJAX)                                                                          Returns HTML partial
   
6. Select Category        GET /generic/{id}        getGeneric(Request)            SELECT products
   (AJAX)                                                                          WHERE Category + Type=1
   
7. Select Generic         GET /make/{id}           getMake(Request)               SELECT makes
   (AJAX)                                                                          JOIN make_categories
   
8. Select Make            GET /series/{id}         getSeries(Request)             SELECT series
   (AJAX)                                                                          JOIN series_makes
   
9. Select Series          GET /description/{id}    getDescription(Request)        SELECT products
   (AJAX)                                                                          WHERE Generic+Make+Series
   
10. Select Description    GET /price/{id}          getPrice(Request)              SELECT prices
    (AJAX)                                                                         WHERE Product + EffDate
   
11. Click "Update"        PUT /quotation/1         update(Request, $id)           UPDATE quotation
                                                                                   DELETE (soft) old items
                                                                                   INSERT sale items
                                                                                   INSERT BOMs
                                                                                   INSERT BOM items
                                                                                   CALL quotationAmount()
   
12. Click "PDF"           GET /quotation/pdf/1     quotationPdf($id)              SELECT quotation + all
                                                                                   nested relations
                                                                                   Generate PDF file
```

---

## Business Rules

### Quotation Number Generation
- **Format:** YYMMDD### (6-digit date + 3-digit sequential)
- **Example:** 220716001 = 2022-07-16, quotation #1 of the day
- **Auto-increment:** Per day (resets each day)
- **Manual override:** Allowed if needed
- **Uniqueness:** Enforced by database unique constraint

### Product Hierarchy Rules
- **Category:** Always required
- **SubCategory:** Optional (refines category)
- **Item:** Optional (refines further)
- **Generic:** Required for BOM items
- **Make:** Optional (brand preference)
- **Series:** Optional (specific product line)
- **Description:** Final SKU selection

### Pricing Rules
- **Base Rate:** From `prices` table
- **Effective Date:** Uses price where EffectiveDate <= current date
- **Latest Price:** If multiple prices, uses most recent
- **Discount:** Applied per item (percentage)
- **Net Rate:** Rate × (1 - Discount/100)
- **Amount:** Quantity × Net Rate

### Calculation Hierarchy
```
Item Amount = Qty × Net Rate
↓
BOM Amount = Sum of all Item Amounts
↓
Sale Amount = Sum of all BOM Amounts (or direct if no BOMs)
↓
Quotation Total = Sum of all Sale Amounts
↓
Apply Quotation-level Discount
↓
Add Taxes (if configured)
↓
Final Total
```

### Revision System
- **New Revision:** Creates copy of entire quotation
- **Revision Number:** Original + R + sequential (220716001R001)
- **ParentId:** Links to original quotation
- **Data Copy:** All sales, BOMs, and items copied
- **Independence:** Revisions can be edited independently

---

## Troubleshooting

### Common Issues

**Issue 1: "Quotation number already exists"**
- **Cause:** Manual number conflicts with existing
- **Solution:** Use auto-generate or choose different number

**Issue 2: "Dropdown empty after selecting category"**
- **Cause:** No products exist for that category
- **Solution:** Add products to category first, or select different category

**Issue 3: "Price shows as 0.00"**
- **Cause:** No price set for product, or price expired
- **Solution:** Add price in Price Management, ensure effective date is valid

**Issue 4: "BOM items not saving"**
- **Cause:** JavaScript error, or missing required fields
- **Solution:** Check browser console, ensure all fields filled

**Issue 5: "PDF generation fails"**
- **Cause:** DomPDF error, usually template issue
- **Solution:** Check Laravel log (storage/logs/laravel.log)

**Issue 6: "Amounts not calculating"**
- **Cause:** JavaScript not running, or invalid numbers
- **Solution:** Ensure Qty and Rate are valid numbers

**Issue 7: "Can't add items to BOM"**
- **Cause:** BOM not saved yet, or AJAX error
- **Solution:** Ensure BOM created before adding items

---

## Tips & Best Practices

### For Faster Quotation Creation

1. **Use Master BOMs:** Create templates for common assemblies
2. **Pre-fill Make/Series:** Use initial selections to filter products
3. **Copy Previous:** Use revision system to copy similar quotations
4. **Keyboard Shortcuts:** Tab through fields for faster data entry

### For Accurate Quotations

1. **Verify Products:** Ensure correct SKU selected
2. **Check Prices:** Confirm rates match current pricing
3. **Review Quantities:** Double-check quantities before saving
4. **Test Calculations:** Verify amounts calculate correctly
5. **Preview PDF:** Generate PDF to check formatting

### For Better Organization

1. **Naming Convention:** Use clear, descriptive names for sales/BOMs
2. **Logical Grouping:** Group related items in same BOM
3. **Consistent Structure:** Use similar structure across quotations
4. **Add Remarks:** Include notes for special requirements

---

## Summary

You now have **COMPLETE, DETAILED knowledge** of the quotation creation process!

### Key Takeaways:

1. **Two-Phase Process:**
   - Create basic quotation first
   - Edit to add detailed items

2. **Hierarchical Structure:**
   - Quotation → Sales → BOMs → Items

3. **Smart Product Selection:**
   - Cascading dropdowns
   - Auto-price loading
   - Flexible hierarchy

4. **Automated Calculations:**
   - Item amounts
   - BOM totals
   - Quotation grand total

5. **Professional Output:**
   - PDF generation
   - Excel export
   - Client-ready documents

### Next Steps:

- **Practice:** Create a test quotation to familiarize yourself
- **Master BOMs:** Learn to create reusable templates (see 19_BOM_CREATION_FLOW.md)
- **Revisions:** Learn revision workflow (see 18_QUOTATION_REVISION_FLOW.md)
- **Reporting:** Understand quotation reports (see 13_REPORTS_EXPORTS.md)

---

**End of Document 17 - Quotation Creation Flow**

[← Back to Index](00_MASTER_DOCUMENTATION_INDEX.md) | [Next: Quotation Revision Flow →](18_QUOTATION_REVISION_FLOW.md)

