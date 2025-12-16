> Source: source_snapshot/docs/03_MODULES/07_QUOTATION_MODULE.md
> Bifurcated into: features/quotation/_general/07_QUOTATION_MODULE.md
> Module: Quotation > General (Overview)
> Date: 2025-12-17 (IST)

# Quotation Module - Complete Deep Dive

**Document:** 07_QUOTATION_MODULE.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Module Overview

**Purpose:** Core business module managing complete quotation lifecycle

**Importance:** ⭐⭐⭐⭐⭐ (CRITICAL - Main feature of application)

**Components:**
- 1 Controller (1,927 lines!)
- 6 Models (Quotation, QuotationSale, QuotationSaleBom, QuotationSaleBomItem, QuotationMakeSeries, QuotationDiscount)
- 8 Views
- 40+ Routes
- 5 Database Tables

---

## Module Architecture

```
QUOTATION MODULE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FRONTEND (Views)
┌─────────────────────────────────────────────────────────┐
│ resources/views/quotation/                              │
│ ├── index.blade.php          List all quotations        │
│ ├── create.blade.php         Create form (basic info)   │
│ ├── edit.blade.php           Edit form (with items)     │
│ ├── saleitem.blade.php       Sale item partial (AJAX)   │
│ ├── bom.blade.php            BOM partial (AJAX)         │
│ ├── item.blade.php           Item partial (AJAX)        │
│ ├── masterbom.blade.php      Master BOM selector        │
│ └── quotationPDF.blade.php   PDF template              │
└─────────────────────────────────────────────────────────┘
                    ↓ HTTP Requests ↓
┌─────────────────────────────────────────────────────────┐
│ ROUTES (routes/web.php)                                 │
│ ├── Resource Routes (7)                                 │
│ │   GET    /quotation              → index             │
│ │   GET    /quotation/create       → create            │
│ │   POST   /quotation              → store             │
│ │   GET    /quotation/{id}         → show              │
│ │   GET    /quotation/{id}/edit    → edit              │
│ │   PUT    /quotation/{id}         → update            │
│ │   DELETE /quotation/{id}         → destroy           │
│ │                                                        │
│ ├── Custom Routes (30+)                                 │
│ │   POST   /quotation/revision/{id}                    │
│ │   POST   /quotation/addmoresale                      │
│ │   POST   /quotation/addmorebom                       │
│ │   POST   /quotation/addmoreitem                      │
│ │   GET    /quotation/pdf/{id}                         │
│ │   GET    /quotation/excel/{id}                       │
│ │   GET    /quotation/generic/{id}                     │
│ │   GET    /quotation/make/{id}                        │
│ │   GET    /quotation/series/{id}                      │
│ │   GET    /quotation/description/{id}                 │
│ │   GET    /quotation/price/{id}                       │
│ │   ... and more                                        │
└─────────────────────────────────────────────────────────┘
                    ↓ Controller Methods ↓
┌─────────────────────────────────────────────────────────┐
│ CONTROLLER (app/Http/Controllers/QuotationController)   │
│                                                          │
│ Core CRUD Methods:                                       │
│ ├── index()           List quotations                   │
│ ├── create()          Show create form                  │
│ ├── store()           Save new quotation                │
│ ├── edit($id)         Show edit form                    │
│ ├── update($id)       Update quotation                  │
│ └── destroy($id)      Delete quotation                  │
│                                                          │
│ Item Management (AJAX):                                  │
│ ├── addmoresale()     Add sale item (returns HTML)      │
│ ├── addmorebom()      Add BOM (returns HTML)            │
│ ├── addmoreitem()     Add item (returns HTML)           │
│ ├── quotationItem($id) Get items for edit               │
│                                                          │
│ Product Selection (AJAX):                                │
│ ├── getGeneric()      Get generic products              │
│ ├── getMake()         Get makes for category            │
│ ├── getSeries()       Get series for make               │
│ ├── getDescription()  Get product SKUs                  │
│ ├── getPrice()        Get product price                 │
│                                                          │
│ Master BOM:                                              │
│ ├── getMasterBomItem($id) Get BOM for copying           │
│ ├── getMasterBom()    Get BOM list                      │
│ ├── getMasterBomVal() Get BOM details                   │
│                                                          │
│ Operations:                                              │
│ ├── revision($id)     Create revision                   │
│ ├── quotationPdf($id) Generate PDF                      │
│ ├── quotationExcelExport($id) Export Excel              │
│ ├── updatePrintType($id) Update print flag              │
│                                                          │
│ [1,927 lines of complex business logic!]                │
└─────────────────────────────────────────────────────────┘
                    ↓ Data Operations ↓
┌─────────────────────────────────────────────────────────┐
│ MODELS (app/Models/)                                     │
│                                                          │
│ Quotation.php         Main quotation header             │
│ QuotationSale.php     Sale items                        │
│ QuotationSaleBom.php  BOMs under sales                  │
│ QuotationSaleBomItem.php Items in BOMs                  │
│ QuotationMakeSeries.php  Make/Series selections         │
│ QuotationDiscount.php    Discount records               │
└─────────────────────────────────────────────────────────┘
                    ↓ Persistence ↓
┌─────────────────────────────────────────────────────────┐
│ DATABASE (MySQL)                                         │
│                                                          │
│ quotations                Main table                     │
│ quotation_sales           Sale items                    │
│ quotation_sale_boms       BOMs                          │
│ quotation_sale_bom_items  Items                         │
│ quotation_make_series     Selections                    │
│ quotation_discounts       Discounts                     │
└─────────────────────────────────────────────────────────┘
```

---

## Controller Methods Reference

### Index Methods

#### index() - List Quotations
**Purpose:** Display all active quotations  
**Route:** GET /quotation  
**Returns:** quotation.index view with quotation list

```php
public function index()
{
    $quotations = Quotation::where('Status',0)
        ->orderBy('QuotationNo', 'DESC')
        ->get();
    return view('quotation.index', compact('quotations'));
}
```

**View Shows:**
- Quotation Number
- Client Name
- Project Name
- Date Created
- Actions: Edit, PDF, Excel, Revision, Delete

---

### Create Methods

#### create() - Show Create Form
**Purpose:** Display form to create new quotation  
**Route:** GET /quotation/create  
**Returns:** quotation.create view

```php
public function create()
{
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

**Form Fields:**
- Client (dropdown)
- Project (dropdown)
- Contact (dropdown)
- Sales Person (dropdown)
- Employee (dropdown)
- Quotation Number (auto or manual)
- Make/Series selections (optional, multiple)

---

#### store() - Save New Quotation
**Purpose:** Process and save new quotation  
**Route:** POST /quotation  
**Parameters:** Request with form data  
**Returns:** Redirect to quotation list

**Process:**
1. Validate required fields
2. Generate quotation number (if auto)
3. Create quotation record
4. Save make/series selections
5. Redirect with success message

**Business Logic:**
```php
// Quotation number generation
$date = date('ymd'); // e.g., "220716"

// Find max number for today
$maxNumber = DB::select(
    "SELECT MAX(RIGHT(QuotationNo, 3)) as max 
     FROM quotations 
     WHERE QuotationNo LIKE ?",
    [$date.'%']
)[0]->max;

// Increment or start at 001
$sequential = $maxNumber ? ($maxNumber + 1) : 1;
$QuotationNo = $date . str_pad($sequential, 3, '0', STR_PAD_LEFT);
// Result: 220716001, 220716002, etc.
```

---

### Edit Methods

#### edit($id) - Show Edit Form
**Purpose:** Display form to edit existing quotation with items  
**Route:** GET /quotation/{id}/edit  
**Returns:** quotation.edit view

```php
public function edit($id)
{
    $quotation = Quotation::find($id);
    
    // Load dropdown data
    $client = Client::pluck('ClientName', 'ClientId')->ToArray();
    $project = Project::pluck('Name', 'ProjectId')->ToArray();
    // ... more dropdowns
    
    return view('quotation.edit', compact('quotation', ...));
}
```

**View Features:**
- Edit basic info (client, project, etc.)
- Add/edit/delete sale items
- Add/edit/delete BOMs
- Add/edit/delete items
- Real-time calculation
- Save button

---

#### update($id) - Save Changes
**Purpose:** Process and save quotation changes  
**Route:** PUT /quotation/{id}  
**Returns:** Redirect to quotation list

**Complex Processing:**
```
1. Validate input
2. Update quotation header
3. Soft delete existing items (Status=1)
4. Loop through submitted sales:
   For each sale:
     a. Create QuotationSale record
     b. Loop through BOMs:
        For each BOM:
          - Create QuotationSaleBom record
          - Loop through items:
            * Create QuotationSaleBomItem record
5. Call quotationAmount() stored procedure
6. Redirect with success
```

**Why Soft Delete?**
- Keeps data integrity
- Allows recovery if needed
- Simple logic (delete all, re-insert)
- Works with complex nested structure

---

### AJAX Methods (Item Management)

#### addmoresale() - Add Sale Item
**Purpose:** Generate HTML for new sale item form  
**Route:** POST /quotation/addmoresale  
**Returns:** HTML partial (saleitem.blade.php)

```php
public function addmoresale(Request $request)
{
    $count = $request->count;  // Item counter
    $QuotationId = $request->qid;
    
    $quotation = Quotation::find($QuotationId);
    $quotationSale = [];  // Empty for new
    $MasterBom = MasterBom::pluck('Name', 'MasterBomId')->ToArray();
    $Category = Category::pluck('Name', 'CategoryId')->ToArray();
    
    return view('quotation.saleitem', compact(
        'count', 'quotationSale', 'MasterBom', 'Category', ...
    ));
}
```

**Returns HTML:**
```html
<div class="sale-item" id="sale_1">
  <input name="Name_1" placeholder="Sale Name">
  <input name="SaleCustomName_1" placeholder="Display Name">
  <input name="Qty_1" type="number">
  <input name="Rate_1" type="number">
  <button onclick="addBOM(1)">Add BOM</button>
  <div id="bom_container_1"></div>
</div>
```

**JavaScript Inserts This Into Page**

---

#### addmorebom() - Add BOM
**Purpose:** Generate HTML for new BOM form under sale  
**Route:** POST /quotation/addmorebom  
**Returns:** HTML partial (bom.blade.php)

```php
public function addmorebom(Request $request)
{
    $count = $request->count;  // BOM counter
    $sid = $request->sid;      // Sale ID
    $QuotationId = $request->qid;
    
    $bomData = [];  // Empty for new
    $Category = Category::pluck('Name', 'CategoryId')->ToArray();
    
    return view('quotation.bom', compact(
        'count', 'sid', 'bomData', 'Category', ...
    ));
}
```

---

#### addmoreitem() - Add Item
**Purpose:** Generate HTML for new item form under BOM  
**Route:** POST /quotation/addmoreitem  
**Returns:** HTML partial (item.blade.php)

```php
public function addmoreitem(Request $request)
{
    $count = $request->count;   // Item counter
    $sid = $request->sid;       // Sale ID
    $bid = $request->bid;       // BOM ID
    $QuotationId = $request->qid;
    
    $itemData = [];  // Empty for new
    $Category = Category::pluck('Name', 'CategoryId')->ToArray();
    
    return view('quotation.item', compact(
        'count', 'sid', 'bid', 'itemData', 'Category', ...
    ));
}
```

**Returns:** Complete item form with cascading dropdowns

---

### AJAX Methods (Product Selection)

#### getGeneric() - Get Generic Products
**Purpose:** Return generic products for selected category  
**Route:** GET /quotation/generic/{categoryId}  
**Returns:** JSON array of products

```php
public function getGeneric(Request $request) 
{
    $CategoryId = $request->id;
    $SubCategoryId = $request->SubCategoryId ?? 0;
    $ItemId = $request->ItemId ?? 0;
    
    $Generic = Product::where('CategoryId', $CategoryId)
        ->where('ProductType', 1) // Generic
        ->where('Status', 0);
    
    if($SubCategoryId) {
        $Generic = $Generic->where('SubCategoryId', $SubCategoryId);
    }
    
    if($ItemId) {
        $Generic = $Generic->where('ItemId', $ItemId);
    }
    
    return response()->json(
        $Generic->pluck('Name','ProductId')->toArray()
    );
}
```

**Returns:**
```json
{
  "250": "Distribution Panel - 100A",
  "251": "Distribution Panel - 200A",
  "252": "Distribution Panel - 400A"
}
```

---

#### getMake() - Get Makes
**Purpose:** Return makes for selected category  
**Route:** GET /quotation/make/{categoryId}  
**Returns:** JSON array of makes

```php
public function getMake(Request $request)
{
    $CategoryId = $request->CategoryId;
    
    $Make = MakeCategory::join('makes', 'makes.MakeId', '=', 'make_categories.MakeId')
        ->where('make_categories.CategoryId', $CategoryId)
        ->pluck('makes.Name', 'makes.MakeId')
        ->toArray();
    
    return response()->json($Make);
}
```

---

#### getSeries() - Get Series
**Purpose:** Return series for selected make and category  
**Route:** GET /quotation/series/{makeId}?categoryId=X  
**Returns:** JSON array of series

```php
public function getSeries(Request $request)
{
    $MakeId = $request->id;
    $CategoryId = $request->CategoryId;
    
    $Series = SeriesMake::join('series', 'series.SeriesId', '=', 'series_makes.SeriesId')
        ->join('series_categories', 'series.SeriesId', '=', 'series_categories.SeriesId')
        ->where('series_makes.MakeId', $MakeId)
        ->where('series_categories.CategoryId', $CategoryId)
        ->select('series.Name', 'series.SeriesId')
        ->get();
    
    return response()->json($Series);
}
```

---

#### getDescription() - Get Product SKUs
**Purpose:** Return specific products (SKUs) for selection  
**Route:** GET /quotation/description/{seriesId}  
**Returns:** JSON array of products

```php
public function getDescription(Request $request)
{
    $SeriesId = $request->id;
    $ProductId = $request->ProductId;  // Generic
    $MakeId = $request->MakeId;
    
    $Description = Product::where('GenericId', $ProductId)
        ->where('MakeId', $MakeId)
        ->where('SeriesId', $SeriesId)
        ->where('ProductType', 2)  // Specific product
        ->select('SKU', 'Description', 'ProductId')
        ->get();
    
    return response()->json($Description);
}
```

---

#### getPrice() - Get Product Price
**Purpose:** Return current price for product  
**Route:** GET /quotation/price/{productId}  
**Returns:** JSON with rate and SKU

```php
public function getPrice(Request $request)
{
    $ProductId = $request->id;
    $date = date('Y-m-d');
    
    // Get latest price effective today or before
    $Rate = Price::where('ProductId', $ProductId)
        ->where('EffectiveDate', '<=', $date)
        ->orderBy('EffectiveDate', 'DESC')
        ->first();
    
    return response()->json([
        'rate' => $Rate ? $Rate->Rate : 0,
        'sku' => $request->sku
    ]);
}
```

**Frontend Auto-fills Rate Field**

---

### Master BOM Methods

#### getMasterBomItem($id) - Get BOM for Copying
**Purpose:** Load master BOM to copy to quotation  
**Route:** GET /quotation/masterbom/{saleId}  
**Returns:** masterbom.blade.php view (modal)

```php
public function getMasterBomItem($id)
{
    $quotationSale = QuotationSale::find($id);
    $MasterBom = MasterBom::pluck('Name', 'MasterBomId')->ToArray();
    
    return view('quotation.masterbom', compact('MasterBom', ...));
}
```

**View Shows:**
- Dropdown of master BOMs
- Preview of BOM items
- Add BOM button

---

#### getMasterBomVal() - Get BOM Details
**Purpose:** Load master BOM items for preview/copying  
**Route:** POST /quotation/masterbom/value  
**Returns:** JSON with BOM items

```php
public function getMasterBomVal(Request $request)
{
    $MasterBomId = $request->id;
    
    $MasterBomItem = MasterBomItem::where('MasterBomId', $MasterBomId)
        ->with('product')
        ->get();
    
    $items = [];
    foreach($MasterBomItem as $item) {
        $items[] = [
            'ProductId' => $item->ProductId,
            'ProductName' => $item->product->Name,
            'Quantity' => $item->Quantity,
            // ... load makes, series, etc.
        ];
    }
    
    return response()->json($items);
}
```

**Frontend Creates Item Forms for Each**

---

### Operation Methods

#### revision($id) - Create Revision
**Purpose:** Copy entire quotation to new revision  
**Route:** POST /quotation/revision/{id}  
**Returns:** Redirect to edit new revision

**See Document 18 for complete details**

**Summary:**
1. Generate revision number (R001, R002, etc.)
2. Copy quotation header
3. Copy all sales, BOMs, and items
4. Redirect to edit

---

#### quotationPdf($id) - Generate PDF
**Purpose:** Create PDF document of quotation  
**Route:** GET /quotation/pdf/{id}  
**Returns:** PDF download

```php
public function quotationPdf($id)
{
    // Load all data
    $quotation = Quotation::with([
        'client', 'project', 'contact', 
        'sales.boms.items'
    ])->find($id);
    
    // Build structured data
    $allData = $this->buildQuotationStructure($quotation);
    
    // Render PDF
    $pdf = PDF::loadView('quotation.quotationPDF', compact(
        'quotation', 'client', 'allData', ...
    ));
    
    $pdf->setPaper('A4', 'portrait');
    
    // Download
    return $pdf->download('Quotation_' . $quotation->QuotationNo . '.pdf');
}
```

**PDF Includes:**
- Company header
- Client details
- Quotation number and date
- All sale items, BOMs, items
- Quantities, rates, amounts
- Totals and discounts
- Terms and conditions
- Signature block

---

#### quotationExcelExport($id) - Export Excel
**Purpose:** Export quotation to Excel format  
**Route:** GET /quotation/excel/{id}  
**Returns:** Excel file download

```php
public function quotationExcelExport($id)
{
    return Excel::download(
        new QuotationExport($id), 
        'Quotation_'.$id.'.xlsx'
    );
}
```

**Uses:** Maatwebsite/Excel package  
**Export Class:** app/Exports/QuotationExport.php

---

### Utility Methods

#### updatePrintType($id) - Update Print Flag
**Purpose:** Mark quotation as ready for printing  
**Route:** POST /quotation/printtype/{id}  
**Business Rule:** Only set if all items have make/series

```php
public function updatePrintType($id)
{
    $quotation = Quotation::find($id);
    
    // Check if any items missing make/series
    $incompleteItems = QuotationSaleBomItem::where('QuotationId', $id)
        ->where('Status', 0)
        ->where(function($q) {
            $q->where('MakeId', 0)->orWhere('SeriesId', 0);
        })
        ->count();
    
    if($incompleteItems == 0) {
        // All items complete
        Quotation::where('QuotationId', $id)->update(['PrintType' => 1]);
    }
}
```

**PrintType Values:**
- 0 = Not ready (items incomplete)
- 1 = Ready for PDF generation

---

## Database Schema Details

### quotations Table

**Primary Key:** QuotationId  
**Unique Key:** QuotationNo  
**Relationships:** 
- belongsTo: Client, Project, Contact, User (Sales), User (Employee)
- hasMany: QuotationSale, QuotationMakeSeries

**Key Columns:**
```sql
QuotationId      INT PRIMARY KEY AUTO_INCREMENT
QuotationNo      VARCHAR(20) UNIQUE NOT NULL  -- YYMMDD###R###
ParentId         INT NULL                     -- For revisions
ClientId         INT NOT NULL FK → clients
ProjectId        INT NOT NULL FK → projects
ContactId        INT NOT NULL FK → contacts
SalesId          INT NOT NULL FK → users
EmployeeId       INT NOT NULL FK → users
CategoryId       INT NULL
MakeId           INT NULL
SeriesId         INT NULL
Discount         DECIMAL(10,2) NULL
PrintType        TINYINT DEFAULT 0
Status           TINYINT DEFAULT 0            -- 0=Active, 1=Deleted
created_at       TIMESTAMP
updated_at       TIMESTAMP
```

---

### quotation_sales Table

**Primary Key:** QuotationSaleId  
**Relationships:**
- belongsTo: Quotation
- hasMany: QuotationSaleBom

**Key Columns:**
```sql
QuotationSaleId  INT PRIMARY KEY AUTO_INCREMENT
QuotationId      INT NOT NULL FK → quotations
SaleId           INT NULL                     -- Optional product reference
Name             VARCHAR(255)
SaleCustomName   VARCHAR(255)                -- Display name
Qty              DECIMAL(10,2)
Rate             DECIMAL(10,2)
Amount           DECIMAL(10,2)                -- Qty × Rate
Margin           DECIMAL(10,2)                -- Margin %
MarginAmount     DECIMAL(10,2)
MarginTotal      DECIMAL(10,2)
Status           TINYINT DEFAULT 0
created_at       TIMESTAMP
updated_at       TIMESTAMP
```

---

### quotation_sale_boms Table

**Primary Key:** QuotationSaleBomId  
**Relationships:**
- belongsTo: Quotation, QuotationSale
- hasMany: QuotationSaleBomItem

**Key Columns:**
```sql
QuotationSaleBomId INT PRIMARY KEY AUTO_INCREMENT
QuotationId        INT NOT NULL FK → quotations
QuotationSaleId    INT NOT NULL FK → quotation_sales
MasterBomId        INT NULL FK → master_boms      -- If from template
MasterBomName      VARCHAR(255)
Qty                DECIMAL(10,2)
Rate               DECIMAL(10,2)
Amount             DECIMAL(10,2)
Status             TINYINT DEFAULT 0
created_at         TIMESTAMP
updated_at         TIMESTAMP
```

---

### quotation_sale_bom_items Table

**Primary Key:** QuotationSaleBomItemId  
**Relationships:**
- belongsTo: Quotation, QuotationSale, QuotationSaleBom, Product, Make, Series

**Key Columns:**
```sql
QuotationSaleBomItemId INT PRIMARY KEY AUTO_INCREMENT
QuotationId            INT NOT NULL FK → quotations
QuotationSaleId        INT NOT NULL FK → quotation_sales
QuotationSaleBomId     INT NOT NULL FK → quotation_sale_boms
ProductId              INT NOT NULL FK → products           -- Generic
MakeId                 INT NULL FK → makes
SeriesId               INT NULL FK → series
Description            INT NULL FK → products               -- Specific SKU
Remark                 TEXT
Qty                    DECIMAL(10,2)
Rate                   DECIMAL(10,2)
Discount               DECIMAL(10,2)
NetRate                DECIMAL(10,2)                        -- Rate after discount
Amount                 DECIMAL(10,2)                        -- Qty × NetRate
Status                 TINYINT DEFAULT 0
created_at             TIMESTAMP
updated_at             TIMESTAMP
```

---

## Business Logic Rules

### Quotation Number Generation

**Format:** YYMMDD### or YYMMDD###R###

**Rules:**
1. Date-based prefix (6 digits: YYMMDD)
2. Sequential number (3 digits: 001-999)
3. Resets each day
4. Revisions append R### (R001, R002, etc.)
5. Must be unique

**Examples:**
```
220716001     = July 16, 2022, First quotation
220716002     = July 16, 2022, Second quotation
220716001R001 = Revision 1 of 220716001
220716001R002 = Revision 2 of 220716001
220717001     = July 17, 2022, First quotation (resets)
```

---

### Amount Calculations

**Item Level:**
```
NetRate = Rate × (1 - Discount/100)
Amount = Qty × NetRate
```

**BOM Level:**
```
BOM Amount = Sum of all Item Amounts
```

**Sale Level:**
```
Sale Amount = Sum of all BOM Amounts
(or direct if no BOMs)
```

**Quotation Level:**
```
Subtotal = Sum of all Sale Amounts
Discount = Subtotal × (Discount%/100)
Total = Subtotal - Discount
```

**Stored Procedure:**
```sql
CALL quotationAmount(QuotationId)
-- Updates all amounts and totals
-- Cascades calculations from items → BOMs → sales → quotation
```

---

### Status Management

**Status Values:**
- 0 = Active (visible, editable)
- 1 = Deleted (soft delete, hidden)

**Applied To:**
- Quotations
- Sales
- BOMs  
- Items

**Query Pattern:**
```sql
WHERE Status = 0  -- Show only active records
```

**Deletion:**
```sql
UPDATE quotations SET Status = 1 WHERE QuotationId = ?
-- Never actually DELETE, always soft delete
```

---

## View Structure

### index.blade.php - List View

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Quotations                       [+ Create Quotation]      │
├────────────────────────────────────────────────────────────┤
│ Search: [_____________] [🔍]                               │
├────────────────────────────────────────────────────────────┤
│ Quotation No │ Client        │ Project  │ Date   │ Actions│
├──────────────┼───────────────┼──────────┼────────┼────────┤
│ 220716003    │ ABC Ind.      │ Factory  │ Jul 16 │ [✏️📄]│
│ 220716002    │ XYZ Corp      │ Office   │ Jul 16 │ [✏️📄]│
│ 220716001    │ DEF Ltd       │ Plant    │ Jul 16 │ [✏️📄]│
└──────────────┴───────────────┴──────────┴────────┴────────┘
│ Showing 1 to 3 of 45 entries            [Pagination]      │
└────────────────────────────────────────────────────────────┘
```

**Actions:**
- ✏️ Edit
- 📄 PDF
- 📊 Excel
- 🔄 Revision
- 🗑️ Delete

---

### create.blade.php - Create Form

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Create Quotation                                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Basic Information                                           │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ Client *        [Select Client ▼____________]        │  │
│ │ Project *       [Select Project ▼___________]        │  │
│ │ Contact *       [Select Contact ▼___________]        │  │
│ │ Sales Person *  [Select Sales ▼_____________]        │  │
│ │ Employee *      [Select Employee ▼__________]        │  │
│ │                                                        │  │
│ │ Quotation Number:                                     │  │
│ │ ○ Auto-generate  ○ Manual [____________]             │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                             │
│ Make/Series Selection (Optional)                            │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ Row 1: [Category▼] [Make▼] [Series▼] [Delete]       │  │
│ │ [+ Add More]                                          │  │
│ └──────────────────────────────────────────────────────┘  │
│                                                             │
│ [Cancel]                              [Save Quotation]     │
└────────────────────────────────────────────────────────────┘
```

---

### edit.blade.php - Edit Form

**Most Complex View!**

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Edit Quotation: #220716001                  [Print Ready?] │
├────────────────────────────────────────────────────────────┤
│ Basic Information (editable)                                │
│ Client, Project, Contact, etc. [dropdowns]                 │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ SALE ITEMS                        [+ Add Sale Item]        │
│                                                             │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ ▼ Sale Item #1: Distribution Panel       [Collapse]  │  │
│ │ ┌────────────────────────────────────────────────────┤  │
│ │ │ Name: Distribution Panel                           │  │
│ │ │ Custom: Complete DP System - 100A                  │  │
│ │ │ Qty: 2  Rate: 50,000  Amount: 100,000             │  │
│ │ │                                                     │  │
│ │ │ [+ Add BOM] [+ Add Master BOM]                    │  │
│ │ │                                                     │  │
│ │ │ ┌──────────────────────────────────────────────┐  │  │
│ │ │ │ ▼ BOM #1: Panel Components    [Collapse]     │  │  │
│ │ │ │ ┌────────────────────────────────────────────┤  │  │
│ │ │ │ │ Name: Panel Components                     │  │  │
│ │ │ │ │ Qty: 2  Rate: 50,000                       │  │  │
│ │ │ │ │                                             │  │  │
│ │ │ │ │ [+ Add Item]                               │  │  │
│ │ │ │ │                                             │  │  │
│ │ │ │ │ ┌──────────────────────────────────────┐  │  │  │
│ │ │ │ │ │ Item #1: Panel Enclosure   [Delete]  │  │  │  │
│ │ │ │ │ │ Siemens SIVACON S8-100A              │  │  │  │
│ │ │ │ │ │ SKU: SIV-S8-100A-IP54                │  │  │  │
│ │ │ │ │ │ Qty: 2  Rate: 25,000  Amt: 50,000   │  │  │  │
│ │ │ │ │ └──────────────────────────────────────┘  │  │  │
│ │ │ │ │ ... more items ...                         │  │  │
│ │ │ │ └────────────────────────────────────────────┘  │  │
│ │ │ └──────────────────────────────────────────────┘  │  │
│ │ │ ... more BOMs ...                                 │  │
│ │ └────────────────────────────────────────────────────┘  │
│ └──────────────────────────────────────────────────────┘  │
│ ... more sale items ...                                    │
│                                                             │
│ TOTALS:                                                     │
│ Subtotal: 2,500,000                                        │
│ Discount: -125,000 (5%)                                    │
│ Total: 2,375,000                                           │
│                                                             │
│ [Cancel]                            [Update Quotation]     │
└────────────────────────────────────────────────────────────┘
```

**Dynamic Features:**
- Collapsible sections
- Add/remove items dynamically
- Real-time calculations
- AJAX loading
- Nested structure (3 levels deep!)

---

## Common Use Cases

### Use Case 1: Create Simple Quotation

**Scenario:** Single product, no BOM

**Steps:**
1. Create quotation (basic info)
2. Edit quotation
3. Add sale item
4. Enter product name, qty, rate
5. Save
6. Generate PDF

**Result:** Simple quotation with one line item

---

### Use Case 2: Create Complex Quotation

**Scenario:** Multiple products with BOMs

**Steps:**
1. Create quotation (basic info)
2. Edit quotation
3. Add sale item #1
4. Add BOM to sale #1
5. Add 10 items to BOM
6. Add another BOM
7. Add 5 items
8. Add sale item #2
9. Add BOM with 8 items
10. Save
11. Generate PDF

**Result:** Complex quotation with nested structure

---

### Use Case 3: Use Master BOM

**Scenario:** Standard assembly

**Steps:**
1. Create quotation
2. Edit quotation
3. Add sale item
4. Click "Add Master BOM"
5. Select BOM template
6. All items auto-added
7. Adjust quantities if needed
8. Save

**Result:** Quotation with pre-configured BOM

---

### Use Case 4: Create Revision

**Scenario:** Client wants changes

**Steps:**
1. Find original quotation
2. Click "Revision"
3. New quotation created (R001)
4. Edit revision
5. Change prices/quantities
6. Save
7. Generate PDF
8. Send to client

**Result:** Updated quotation, original preserved

---

## Performance Considerations

### Large Quotations

**Problem:** 100+ items = slow page load

**Solutions:**
1. Lazy loading (load items on demand)
2. Pagination of items
3. Collapsible sections (collapse by default)
4. AJAX updates (don't reload entire page)

---

### Database Optimization

**Indexes Needed:**
```sql
CREATE INDEX idx_quotation_no ON quotations(QuotationNo);
CREATE INDEX idx_quotation_client ON quotations(ClientId);
CREATE INDEX idx_quotation_project ON quotations(ProjectId);
CREATE INDEX idx_quotation_status ON quotations(Status);
CREATE INDEX idx_sale_quotation ON quotation_sales(QuotationId);
CREATE INDEX idx_bom_quotation ON quotation_sale_boms(QuotationId);
CREATE INDEX idx_item_quotation ON quotation_sale_bom_items(QuotationId);
```

---

### Stored Procedure

**quotationAmount(QuotationId)**

**Purpose:** Calculate all amounts in one operation

**Benefits:**
- Single database call
- Atomic operation
- Faster than multiple updates
- Maintains consistency

**Usage:**
```sql
CALL quotationAmount(123);
-- Updates amounts for quotation ID 123
```

---

## Summary

### Module Statistics

- **Lines of Code:** 1,927 (controller only!)
- **Routes:** 40+
- **Views:** 8
- **Models:** 6
- **Database Tables:** 6
- **Complexity:** Very High (nested 3 levels)

### Key Features

✅ Complete CRUD operations  
✅ Complex nested structure  
✅ Dynamic item management  
✅ Product selection cascade  
✅ Master BOM integration  
✅ Revision system  
✅ PDF generation  
✅ Excel export  
✅ Real-time calculations  
✅ Soft delete (data preservation)

### Critical Files

1. **QuotationController.php** - 1,927 lines of business logic
2. **edit.blade.php** - Most complex view
3. **quotations table** - Central data store
4. **quotationAmount()** - Calculation stored procedure

---

**End of Document 07 - Quotation Module**

[← Back to Database Schema](04_DATABASE_SCHEMA.md) | [Next: Product Module →](08_PRODUCT_MODULE.md)

