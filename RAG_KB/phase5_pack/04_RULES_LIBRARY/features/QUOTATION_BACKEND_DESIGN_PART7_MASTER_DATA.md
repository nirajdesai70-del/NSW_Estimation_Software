---
Source: features/quotation/_general/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T02:13:13.487030
KB_Path: phase5_pack/04_RULES_LIBRARY/features/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md
---

> Source: source_snapshot/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md
> Bifurcated into: features/master/organization/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md
> Module: Master > Organization
> Date: 2025-12-17 (IST)

# Quotation Backend Design - Part 7: Master Data Integration

**Document:** QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes how the quotation system integrates with master data: Organization, Client, Project, Component/Catalog, Category/SubCategory/Item, Master BOM, and Product Master.

---

## 🏢 Organization → Client → Project → Quotation Flow

### Organization

**Table:** `organizations`  
**Model:** `Organization`  
**Purpose:** Company/organization master

**Key Attributes:**
- `OrganizationId` (PK)
- `Name` - Organization name
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Organization hasMany Client
```

**Connection to Quotation:**
```
Organization → Client → Project → Quotation
```

---

### Client

**Table:** `clients`  
**Model:** `Client`  
**Purpose:** Customer companies

**Key Attributes:**
- `ClientId` (PK)
- `OrganizationId` (FK) - Foreign key to organizations
- `ClientName` - Client name
- `Email`, `Mobile`, `Address` - Contact information
- `CountryId`, `StateId` - Location
- `GSTNo`, `PANNo` - Tax/ID numbers
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Client belongsTo Organization
Client belongsTo Country
Client belongsTo State
Client hasMany Contact
Client hasMany Project
Client hasMany Quotation
```

**Connection to Quotation:**
```php
// In Quotation model
public function client()
{
    return $this->belongsTo(Client::class, 'ClientId', 'ClientId');
}

// Usage
$quotation = Quotation::with('client')->find($id);
$clientName = $quotation->client->ClientName;
```

---

### Project

**Table:** `projects`  
**Model:** `Project`  
**Purpose:** Client projects

**Key Attributes:**
- `ProjectId` (PK)
- `ClientId` (FK) - Foreign key to clients
- `ProjectNo` - Project number (YYMMDD001 format)
- `Name` - Project name
- `Location` - Project location
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Project belongsTo Client
Project hasMany Quotation
```

**Connection to Quotation:**
```php
// In Quotation model
public function project()
{
    return $this->belongsTo(Project::class, 'ProjectId', 'ProjectId');
}

// Usage
$quotation = Quotation::with('project')->find($id);
$projectName = $quotation->project->Name;
```

**Complete Flow:**
```
Organization (1) ──→ (N) Client
Client (1) ──→ (N) Project
Project (1) ──→ (N) Quotation
```

---

## 📦 Product Master Integration

### Product Hierarchy

**Complete Hierarchy:**
```
Category (Required)
  └── SubCategory (Optional)
      └── Item (Optional - Product Type)
          └── Generic Product (Required for BOM items)
              └── Make (Optional - Brand/Manufacturer)
                  └── Series (Optional - Product Line)
                      └── Specific Product (Optional - SKU)
```

---

### Category

**Table:** `categories`  
**Model:** `Category`  
**Purpose:** Product categories

**Key Attributes:**
- `CategoryId` (PK)
- `Name` - Category name
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Category hasMany SubCategory
Category hasMany Item
Category hasMany Product
Category belongsToMany Make (via make_categories)
Category belongsToMany Series (via series_categories)
Category belongsToMany Attribute (via category_attributes)
```

**Connection to Quotation:**
- Categories used for filtering products when adding components
- QuotationMakeSeries links Category to Make/Series selections

---

### SubCategory

**Table:** `sub_categories`  
**Model:** `SubCategory`  
**Purpose:** Product sub-categories

**Key Attributes:**
- `SubCategoryId` (PK)
- `CategoryId` (FK) - Foreign key to categories
- `Name` - Sub-category name
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
SubCategory belongsTo Category
SubCategory hasMany Product
```

**Connection to Quotation:**
- Used for product filtering and organization
- Displayed in component detail tree view

---

### Item (Product Type)

**Table:** `items`  
**Model:** `Item`  
**Purpose:** Product types/items

**Key Attributes:**
- `ItemId` (PK)
- `CategoryId` (FK) - Foreign key to categories
- `Name` - Item name
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Item belongsTo Category
Item hasMany Product
```

**Connection to Quotation:**
- Required for all products (ProductType requirement)
- Used for product filtering and organization
- Displayed in component detail tree view

---

### Product (Generic & Specific)

**Table:** `products`  
**Model:** `Product`  
**Purpose:** Generic and specific products

**Product Types:**
- **Generic Product (ProductType = 1):** Base product without Make/Series
- **Specific Product (ProductType = 2):** Product with Make/Series (SKU)

**Key Attributes:**
- `ProductId` (PK)
- `GenericId` (FK) - Foreign key to products (self-reference for specific products)
- `CategoryId` (FK) - Foreign key to categories
- `SubCategoryId` (FK) - Foreign key to sub_categories
- `ItemId` (FK) - Foreign key to items (Product Type)
- `ProductType` - 1=Generic, 2=Specific
- `Name` - Product name
- `SKU` - Stock keeping unit (for specific products)
- `Description` - Product description
- `MakeId` (FK) - Make/brand (for specific products)
- `SeriesId` (FK) - Series (for specific products)
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Product belongsTo Category
Product belongsTo SubCategory
Product belongsTo Item
Product belongsTo Product (as GenericId - self-reference)
Product belongsTo Make
Product belongsTo Series
Product hasMany Product (as specific products)
Product hasMany Price
Product hasMany QuotationSaleBomItem
Product hasMany MasterBomItem
```

**Connection to Quotation:**
```php
// In QuotationSaleBomItem model
public function product()
{
    return $this->belongsTo(Product::class, 'ProductId', 'ProductId');
}

// Usage
$item = QuotationSaleBomItem::with('product')->find($id);
$productName = $item->product->Name;
$categoryName = $item->product->category->Name;
```

---

### Make & Series

**Make Table:** `makes`  
**Model:** `Make`  
**Purpose:** Brands/manufacturers

**Series Table:** `series`  
**Model:** `Series`  
**Purpose:** Product series

**Connection to Quotation:**
- QuotationMakeSeries links Category to Make/Series selections per quotation
- Components reference Make/Series for specific product selection

```php
// In QuotationSaleBomItem model
public function make()
{
    return $this->belongsTo(Make::class, 'MakeId', 'MakeId');
}

public function series()
{
    return $this->belongsTo(Series::class, 'SeriesId', 'SeriesId');
}
```

---

## 📋 Master BOM Integration

### Master BOM

**Table:** `master_boms`  
**Model:** `MasterBom`  
**Purpose:** Reusable BOM templates

**Key Attributes:**
- `MasterBomId` (PK)
- `Name` - BOM name
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
MasterBom hasMany MasterBomItem
MasterBom hasMany QuotationSaleBom (as reference)
```

---

### Master BOM Item

**Table:** `master_bom_items`  
**Model:** `MasterBomItem`  
**Purpose:** Items in master BOM templates

**Key Attributes:**
- `MasterBomItemId` (PK)
- `MasterBomId` (FK) - Foreign key to master_boms
- `ProductId` (FK) - Foreign key to products (generic only)
- `Quantity` - Template quantity
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
MasterBomItem belongsTo MasterBom
MasterBomItem belongsTo Product (generic product only)
```

**Important Rule:**
- Master BOM items reference **generic products only** (ProductType = 1)
- When copied to quotation, user selects Make/Series to create specific product

---

### Master BOM → Proposal BOM Copy Process

**Rule:** Always copy Master BOM, never link directly

**Process:**

**Step 1: Select Master BOM**
```php
$masterBom = MasterBom::find($masterBomId);
```

**Step 2: Create Proposal BOM**
```php
$proposalBom = new QuotationSaleBom();
$proposalBom->QuotationSaleId = $panelId;
$proposalBom->MasterBomId = $masterBomId; // Reference only
$proposalBom->BomName = $masterBom->Name;
$proposalBom->Level = 1; // Or appropriate level
$proposalBom->save();
```

**Step 3: Copy Master BOM Items**
```php
foreach ($masterBom->items as $masterItem) {
    $proposalItem = new QuotationSaleBomItem();
    $proposalItem->QuotationSaleBomId = $proposalBom->QuotationSaleBomId;
    $proposalItem->ProductId = $masterItem->ProductId; // Generic product
    $proposalItem->Qty = $masterItem->Quantity; // Copy quantity
    $proposalItem->save();
    
    // User will later select Make/Series to create specific product reference
}
```

**Step 4: User Selects Make/Series**
```php
// User selects Make/Series for each component
$proposalItem->MakeId = $selectedMakeId;
$proposalItem->SeriesId = $selectedSeriesId;

// Find or create specific product
$specificProduct = Product::where('GenericId', $proposalItem->ProductId)
    ->where('MakeId', $selectedMakeId)
    ->where('SeriesId', $selectedSeriesId)
    ->first();

if ($specificProduct) {
    $proposalItem->ProductId = $specificProduct->ProductId; // Update to specific
}
```

**Key Points:**
- Master BOM is copied, not linked
- Changes to Master BOM don't affect existing quotations
- Each quotation has independent BOM structure
- MasterBomId stored for reference only

---

## 🏷️ Attribute System

### Attributes

**Table:** `attributes`  
**Model:** `Attribute`  
**Purpose:** Product attributes (Voltage, Current, IP Rating, etc.)

**Key Attributes:**
- `AttributeId` (PK)
- `Name` - Attribute name
- `Type` - Attribute type
- `Status` - 0=Active, 1=Deleted

**Relationships:**
```php
Attribute belongsToMany Category (via category_attributes)
Attribute belongsToMany Product (via product_attributes)
```

**Connection to Quotation:**
- Attributes used for product specification
- Displayed in component detail tree view
- Used for filtering and organization
- **Attributes do NOT affect cost calculations**

---

## 🔗 Complete Integration Map

### Organization to Quotation

```
Organization
  └── Client
      └── Project
          └── Quotation
              └── QuotationSale (Panel)
                  └── QuotationSaleBom (Feeder/BOM)
                      └── QuotationSaleBomItem (Component)
                          └── Product
                              ├── Category
                              ├── SubCategory
                              ├── Item
                              ├── Make
                              └── Series
```

### Master BOM to Proposal BOM

```
MasterBom
  └── MasterBomItem
      └── Product (Generic)
          └── [Copy Process]
              └── QuotationSaleBom (Proposal BOM)
                  └── QuotationSaleBomItem (Proposal Item)
                      └── Product (Specific - after Make/Series selection)
```

### Product to Component

```
Category → SubCategory → Item → Product (Generic)
  └── Product (Specific) [with Make/Series]
      └── Price
          └── [Used in]
              └── QuotationSaleBomItem (Component)
```

---

## 📊 Data Flow Examples

### Example 1: Adding Component from Product Master

**Step 1: User Selects Category**
```php
$category = Category::find($categoryId);
```

**Step 2: User Selects SubCategory (Optional)**
```php
$subCategory = SubCategory::where('CategoryId', $categoryId)
    ->find($subCategoryId);
```

**Step 3: User Selects Item (Product Type)**
```php
$item = Item::where('CategoryId', $categoryId)
    ->find($itemId);
```

**Step 4: System Shows Generic Products**
```php
$genericProducts = Product::where('CategoryId', $categoryId)
    ->where('ProductType', 1) // Generic only
    ->get();
```

**Step 5: User Selects Generic Product**
```php
$genericProduct = Product::find($genericProductId);
```

**Step 6: System Shows Makes/Series**
```php
$makes = MakeCategory::where('CategoryId', $categoryId)
    ->with('make')
    ->get()
    ->pluck('make');

$series = SeriesCategory::where('CategoryId', $categoryId)
    ->with('series')
    ->get()
    ->pluck('series');
```

**Step 7: User Selects Make/Series**
```php
$make = Make::find($makeId);
$series = Series::find($seriesId);
```

**Step 8: System Finds/Creates Specific Product**
```php
$specificProduct = Product::where('GenericId', $genericProductId)
    ->where('MakeId', $makeId)
    ->where('SeriesId', $seriesId)
    ->first();

if (!$specificProduct) {
    // Create specific product
    $specificProduct = new Product();
    $specificProduct->GenericId = $genericProductId;
    $specificProduct->MakeId = $makeId;
    $specificProduct->SeriesId = $seriesId;
    $specificProduct->ProductType = 2;
    // ... set other fields
    $specificProduct->save();
}
```

**Step 9: System Gets Price**
```php
$rate = $this->getItemRate($specificProduct->ProductId);
```

**Step 10: System Creates Component**
```php
$component = new QuotationSaleBomItem();
$component->QuotationSaleBomId = $bomId;
$component->ProductId = $specificProduct->ProductId;
$component->MakeId = $makeId;
$component->SeriesId = $seriesId;
$component->Rate = $rate;
$component->RateSource = $rate > 0 ? 'PRICELIST' : 'UNRESOLVED';
$component->save();
```

---

### Example 2: Adding Master BOM to Quotation

**Step 1: User Selects Master BOM**
```php
$masterBom = MasterBom::with('items.product')->find($masterBomId);
```

**Step 2: System Creates Proposal BOM**
```php
$proposalBom = new QuotationSaleBom();
$proposalBom->QuotationSaleId = $panelId;
$proposalBom->MasterBomId = $masterBomId; // Reference
$proposalBom->BomName = $masterBom->Name;
$proposalBom->Level = 1;
$proposalBom->save();
```

**Step 3: System Copies Master BOM Items**
```php
foreach ($masterBom->items as $masterItem) {
    $proposalItem = new QuotationSaleBomItem();
    $proposalItem->QuotationSaleBomId = $proposalBom->QuotationSaleBomId;
    $proposalItem->ProductId = $masterItem->ProductId; // Generic
    $proposalItem->Qty = $masterItem->Quantity; // Copy quantity
    $proposalItem->save();
}
```

**Step 4: User Selects Make/Series for Each Component**
```php
// User selects Make/Series via UI
// System updates component with Make/Series
// System finds/creates specific product
// System gets price for specific product
```

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial master data integration document | Part 7 of backend design series |

---

**Previous:** [Part 6: Pricing & Discount Rules](QUOTATION_BACKEND_DESIGN_PART6_PRICING.md)  
**Next:** [Part 8: Backend Services & Controllers](QUOTATION_BACKEND_DESIGN_PART8_SERVICES.md)

