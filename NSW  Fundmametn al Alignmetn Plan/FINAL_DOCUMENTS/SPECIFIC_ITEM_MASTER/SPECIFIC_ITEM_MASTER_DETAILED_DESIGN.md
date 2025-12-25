# Specific Item Master Detailed Design & Architecture

**Document:** SPECIFIC_ITEM_MASTER_DETAILED_DESIGN.md  
**Version:** 1.1  
**Date:** December 2025  
**Status:** 🔴 **STANDING INSTRUCTION - PERMANENT STANDARD**

---

## 📋 Table of Contents

1. [L0–L1–L2 Layer Definitions](#l0l1l2-layer-definitions-frozen)
2. [Specific Item Master Overview](#1-specific-item-master-overview)
3. [Database Structure](#2-database-structure)
4. [Model Design](#3-model-design)
5. [Controller Design](#4-controller-design)
6. [Views & UI](#5-views--ui)
7. [Relationships & Dependencies](#6-relationships--dependencies)
8. [Workflows & Operations](#7-workflows--operations)
9. [Code Examples](#8-code-examples)
10. [Troubleshooting](#9-troubleshooting)
11. [Complete Code File Mapping](#10-complete-code-file-mapping)

---

## 🎯 L0–L1–L2 Layer Definitions (Frozen)

- **L0 = Generic Item Master (Functional Family)**
  - Example: MCC / MCCB / ACB
  - No technical specification, no make, no series, no SKU
  - Unique; never duplicated; never used directly in any BOM

- **L1 = Specific Item Master (Technical Variant, Make-agnostic)**
  - Example: MCCB 25A, 25kA / 35kA / 50kA
  - Derived from L0 + technical spec set
  - Unique; never duplicated; reusable
  - **Master BOM operates at L1**
  - **Master BOM must not contain L2**

- **L2 = Catalog Item (Make + Series + SKU/Model)**
  - Example: Schneider / ABB / Siemens model variants
  - Derived from L1 + Make + Series (+ SKU/Model)
  - Unique; never duplicated; reusable
  - **Proposal/Specific BOM operates at L2**
  - **Specific Item Master operates at L2**

- **Proposal/Specific BOM = Quotation-specific instance**
  - Multiple Proposal BOMs can exist for one Master BOM
  - Must resolve L1 → L2 before finalization

### L2 Layer Definition for Specific Item Master

**Critical Rule:** Specific Item Master operates exclusively at L2 layer.

**Characteristics:**
- Specific Item Master manages L2 products (ProductType=2)
- L2 products have Make + Series + SKU/Model
- L2 products are derived from L1 (Generic products with technical specs) + Make + Series
- L2 products are unique and never duplicated (reuse existing L2, never recreate)
- L2 products are used in Proposal BOMs (quotation-specific instances)

---

## 1. Specific Item Master Overview

### 1.1 Purpose

**Specific Item Master** manages specific products (ProductType = 2) in the system. Specific products are vendor-specific products with Make/Series/SKU details. They are production-ready products that can be priced and used in quotations.

**Key Roles:**
- **Production-Ready Product:** Fully specified product ready for quotations
- **Vendor-Specific:** Has Make/Series/SKU details
- **ProductType = 2:** Identified by ProductType field
- **Links to Generic:** Links back to Generic Product via GenericId
- **Priced:** Has price list entries for costing
- **Attribute Repository:** Stores technical specifications via attributes

### 1.2 Position in Hierarchy

```
Category (Required)
  └── SubCategory (Optional)
        └── Item/ProductType (Optional)
              └── Generic Product (ProductType = 1)
                    └── Make (Optional)
                          └── Series (Optional)
                                └── Specific Product (ProductType = 2) ← YOU ARE HERE
```

### 1.3 Core Characteristics

- **ProductType:** Always 2 (Specific)
- **GenericId:** Required (links to Generic Product)
- **MakeId:** Optional (vendor brand)
- **SeriesId:** Optional (vendor series)
- **SKU:** Recommended (specific part number)
- **Purpose:** Production-ready product for quotations
- **Use Case:** Final quotation, pricing, procurement

### 1.4 Specific vs Generic

| Feature | Generic Product | Specific Product |
|---------|----------------|------------------|
| **ProductType** | 1 | 2 |
| **GenericId** | NULL | Links to Generic Product |
| **MakeId** | NULL | Optional (vendor brand) |
| **SeriesId** | NULL | Optional (vendor series) |
| **SKU** | NULL | Recommended |
| **Purpose** | Template | Production-ready |
| **Pricing** | Not typically priced | Priced |

---

## 2. Database Structure

### 2.1 Products Table (Specific Products)

**Table Name:** `products`

**Note:** Specific products are stored in the same `products` table as generic products, differentiated by `ProductType = 2`.

| Column | Type | Key | Null | Default | Description |
|--------|------|-----|------|---------|-------------|
| `ProductId` | INT | PK, AI | NO | - | Primary key, auto-increment |
| `Name` | VARCHAR(255) | | NO | - | Product name (required, unique) |
| `CategoryId` | INT | FK | NO | - | Foreign key to categories (required) |
| `SubCategoryId` | INT | FK | YES | NULL | Foreign key to sub_categories (optional) |
| `ItemId` | INT | FK | YES | NULL | Foreign key to items (ProductType, recommended) |
| `ProductType` | TINYINT | | NO | 2 | Always 2 for specific products |
| `GenericId` | INT | FK | YES | NULL | Foreign key to Generic Product (required) |
| `MakeId` | INT | FK | YES | NULL | Foreign key to makes (optional) |
| `SeriesId` | INT | FK | YES | NULL | Foreign key to series (optional) |
| `SKU` | VARCHAR(255) | | YES | NULL | SKU/Part number (recommended) |
| `Description` | TEXT | | YES | NULL | Product description |
| `UOM` | VARCHAR(32) | | YES | NULL | Unit of measure |
| `Status` | TINYINT | | NO | 0 | 0=Active, 1=Deleted |
| `IsAttributeComplete` | TINYINT | | NO | 0 | 0=Incomplete, 1=Complete |
| `created_at` | TIMESTAMP | | YES | NULL | Record creation timestamp |
| `updated_at` | TIMESTAMP | | YES | NULL | Record update timestamp |

**Key Constraints:**
- `ProductType = 2` for specific products
- `GenericId` is required (links to Generic Product)
- `Name` must be unique
- `CategoryId` is required
- `SKU` is recommended for specific products

---

## 3. Model Design

### 3.1 Model File

**File:** `app/Models/Product.php`

**Namespace:** `App\Models`

**Base Class:** `Illuminate\Database\Eloquent\Model`

### 3.2 Model Code

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    use HasFactory;
    
    protected $primaryKey = 'ProductId';
    
    protected $fillable = [
        'ProductId', 'Name', 'Generic', 'SKU', 'MakeId', 'CategoryId', 'SubCategoryId', 'ItemId', 'SeriesId', 'ProductType', 'Description',
        'Status', 'GenericId','UOM'
    ];

    public static $producttype = [
        '1' => 'Generic Product',
        '2' => 'Specific Product',
        '3' => 'Product Price'
    ];

    // Relationships for specific products (ProductType = 2)
    public function category()
    {
        return $this->belongsTo(Category::class, 'CategoryId', 'CategoryId');
    }
    
    public function subcategory()
    {
        return $this->belongsTo(SubCategory::class, 'SubCategoryId', 'SubCategoryId');
    }
    
    public function item()
    {
        return $this->belongsTo(Item::class, 'ItemId', 'ItemId');
    }
    
    public function generic()
    {
        return $this->belongsTo(Product::class, 'GenericId', 'ProductId');
    }
    
    public function make()
    {
        return $this->belongsTo(Make::class, 'MakeId', 'MakeId');
    }
    
    public function series()
    {
        return $this->belongsTo(Series::class, 'SeriesId', 'SeriesId');
    }
    
    // Price relationships
    public function prices()
    {
        return $this->hasMany(Price::class, 'ProductId', 'ProductId');
    }
    
    // Current/latest price (most recent effective price)
    public function currentPrice()
    {
        return $this->hasOne(Price::class, 'ProductId', 'ProductId')
            ->where('EffectiveDate', '<=', now())
            ->where('Status', 0)
            ->orderBy('EffectiveDate', 'DESC');
    }
    
    // Attribute relationships
    public function productAttributes()
    {
        return $this->hasMany(ProductAttribute::class, 'ProductId', 'ProductId')
                    ->orderBy('SortOrder');
    }
}
```

### 3.3 Model Properties for Specific Products

#### Primary Key
- **Field:** `ProductId`
- **Type:** Integer (Auto-increment)

#### Fillable Fields
- `ProductId` - Primary key
- `Name` - Product name (required, unique)
- `CategoryId` - Foreign key to Category (required)
- `SubCategoryId` - Foreign key to SubCategory (optional)
- `ItemId` - Foreign key to Item/ProductType (optional but recommended)
- `ProductType` - Always 2 for specific products
- `GenericId` - Foreign key to Generic Product (required)
- `MakeId` - Foreign key to Make (optional)
- `SeriesId` - Foreign key to Series (optional)
- `SKU` - SKU/Part number (recommended)
- `Description` - Product description (optional)
- `UOM` - Unit of measure (optional)
- `Status` - 0=Active, 1=Deleted
- `IsAttributeComplete` - 0=Incomplete, 1=Complete

#### Key Constants

**ProductType Values:**
```php
public static $producttype = [
    '1' => 'Generic Product',
    '2' => 'Specific Product',
    '3' => 'Product Price'
];
```

**For Specific Products:**
- `ProductType = 2` (always)

### 3.4 Model Relationships

#### Parent Relationships

**1. belongsTo Category**
```php
public function category()
```
- **Related Model:** `Category`
- **Foreign Key:** `products.CategoryId`
- **Local Key:** `categories.CategoryId`
- **Purpose:** Get the parent category
- **Required:** Yes

**2. belongsTo SubCategory**
```php
public function subcategory()
```
- **Related Model:** `SubCategory`
- **Foreign Key:** `products.SubCategoryId`
- **Local Key:** `sub_categories.SubCategoryId`
- **Purpose:** Get the parent subcategory
- **Optional:** Yes

**3. belongsTo Item (ProductType)**
```php
public function item()
```
- **Related Model:** `Item`
- **Foreign Key:** `products.ItemId`
- **Local Key:** `items.ItemId`
- **Purpose:** Get the ProductType
- **Optional:** Yes (but recommended)

**4. belongsTo Generic Product**
```php
public function generic()
```
- **Related Model:** `Product` (self-reference, ProductType = 1)
- **Foreign Key:** `products.GenericId`
- **Local Key:** `products.ProductId`
- **Purpose:** Get the parent generic product
- **Required:** Yes

**5. belongsTo Make**
```php
public function make()
```
- **Related Model:** `Make`
- **Foreign Key:** `products.MakeId`
- **Local Key:** `makes.MakeId`
- **Purpose:** Get the vendor brand
- **Optional:** Yes

**6. belongsTo Series**
```php
public function series()
```
- **Related Model:** `Series`
- **Foreign Key:** `products.SeriesId`
- **Local Key:** `series.SeriesId`
- **Purpose:** Get the vendor series
- **Optional:** Yes

#### Child Relationships

**1. hasMany ProductAttributes**
```php
public function productAttributes()
```
- **Related Model:** `ProductAttribute`
- **Foreign Key:** `product_attributes.ProductId`
- **Local Key:** `products.ProductId`
- **Purpose:** Get all attribute values for this product
- **Ordered by:** SortOrder

**2. hasMany Prices**
```php
public function prices()
```
- **Related Model:** `Price`
- **Foreign Key:** `prices.ProductId`
- **Local Key:** `products.ProductId`
- **Purpose:** Get all price list entries for this product

**3. hasOne Current Price**
```php
public function currentPrice()
```
- **Related Model:** `Price`
- **Foreign Key:** `prices.ProductId`
- **Local Key:** `products.ProductId`
- **Purpose:** Get the latest effective price
- **Filtered by:** EffectiveDate <= today, Status = 0
- **Ordered by:** EffectiveDate DESC

### 3.5 Model Usage Examples

#### Get Specific Product with Relationships
```php
$specificProduct = Product::where('ProductType', 2)
    ->with(['category', 'subcategory', 'item', 'generic', 'make', 'series', 'productAttributes.attribute', 'prices'])
    ->find(1);
```

#### Get Specific Product with Current Price
```php
$specificProduct = Product::where('ProductType', 2)
    ->with('currentPrice')
    ->find(1);
    
$currentPrice = $specificProduct->currentPrice;
if ($currentPrice) {
    echo $currentPrice->Rate; // Latest effective price
}
```

#### Get Specific Products by Generic Product
```php
$genericProduct = Product::where('ProductType', 1)->find(1001);
$specificProducts = Product::where('ProductType', 2)
    ->where('GenericId', $genericProduct->ProductId)
    ->get();
```

#### Get Specific Products by Make/Series
```php
$specificProducts = Product::where('ProductType', 2)
    ->where('MakeId', 50) // Schneider Electric
    ->where('SeriesId', 25) // Acti9
    ->get();
```

---

## 4. Controller Design

### 4.1 Controller File

**File:** `app/Http/Controllers/ProductController.php`

**Namespace:** `App\Http\Controllers`

**Base Class:** `App\Http\Controllers\Controller`

### 4.2 Controller Methods

#### 4.2.1 index() - List Specific Products

**Route:** `GET /product`

**Purpose:** Display list of all specific products with relationships and prices

**Key Features:**
- Pagination support (25 items per page default)
- Category filtering (optional)
- Eager loading of relationships (category, subcategory, item, generic, prices)
- Price display (latest effective price)
- NEPL Table Component integration
- Filterable and sortable

**Code:**
```php
public function index(Request $request)
{
    $categoryFilter = $request->query('category');
    $categoryName = null;
    $categoryId = $categoryFilter;
    
    // Use Eloquent with eager loading instead of raw SQL
    $query = Product::where('ProductType', 2)
        ->with([
            'category',
            'subcategory', 
            'item',
            'generic',
            'prices' => function($q) {
                // Get latest price per product
                $q->orderBy('EffectiveDate', 'DESC')
                  ->orderBy('PriceId', 'DESC')
                  ->limit(1);
            }
        ]);
    
    if ($categoryFilter) {
        $category = Category::find($categoryFilter);
        $categoryName = $category ? $category->Name : null;
        $query->where('CategoryId', $categoryFilter);
    }
    
    // Add pagination to prevent memory issues
    $perPage = $request->get('per_page', 25);
    $products = $query->orderBy('ProductId', 'DESC')->paginate($perPage)->appends($request->query());
    
    // NEPL Table Component columns
    $columns = [
        ['key' => 'Name', 'label' => 'Product Name', 'sortable' => true],
        ['key' => 'SKU', 'label' => 'SKU', 'sortable' => true],
        ['key' => 'generic_name', 'label' => 'Generic', 'render' => function ($p) {
            return e(optional($p->generic)->Name ?? '-');
        }],
        ['key' => 'category_name', 'label' => 'Category', 'render' => function ($p) {
            return e(optional($p->category)->Name ?? '-');
        }],
        ['key' => 'subcategory_name', 'label' => 'SubCategory', 'render' => function ($p) {
            return e(optional($p->subcategory)->Name ?? '-');
        }],
        ['key' => 'price', 'label' => 'Price', 'render' => function ($p) {
            $price = $p->prices->first();
            return $price ? number_format($price->Rate, 2) : '0.00';
        }],
    ];
    
    // Action buttons
    $actions = [
        ['type' => 'edit', 'route' => 'product.edit', 'param' => 'ProductId'],
        ['type' => 'delete', 'route' => 'product.destroy', 'param' => 'ProductId'],
    ];
    
    // Get categories for filter dropdown
    $categories = Category::orderBy('Name')->pluck('Name', 'CategoryId')->toArray();
    
    return view('product.index', compact('products', 'categoryName', 'categoryId', 'columns', 'actions', 'categories'));
}
```

**Query Parameters:**
- `category` - Filter by CategoryId
- `per_page` - Items per page (default: 25)

**Response Data:**
- `$products` - Paginated collection of specific products
- `$categoryName` - Category name (if filtered)
- `$categoryId` - Category ID (if filtered)
- `$columns` - Table column definitions
- `$actions` - Action button definitions
- `$categories` - All categories (for filter dropdown)

---

#### 4.2.2 create() - Show Create Form

**Route:** `GET /product/create`

**Purpose:** Display form to create new specific product

**Code:**
```php
public function create()
{
    $category = Category::pluck('Name', 'CategoryId')->ToArray();
    return view('product.create', compact('category'));
}
```

**Response Data:**
- `$category` - All categories (for dropdown selection)

**Note:** SubCategory, Item, Generic, Make, Series are loaded dynamically via AJAX based on Category selection.

---

#### 4.2.3 store() - Create Specific Product

**Route:** `POST /product`

**Purpose:** Create new specific product

**Validation:** Handled by `StoreProductRequest`

**Key Features:**
- Creates specific product (ProductType = 2)
- Validates GenericId (required)
- Validates ItemId (soft enforcement)
- Handles attribute values
- Validates required attributes (soft/hard enforcement)
- Sets IsAttributeComplete flag

**Code:**
```php
public function store(StoreProductRequest $request)
{
    // Soft enforcement - allow admin bypass with warning
    if (empty($request->ItemId) || $request->ItemId == 0) {
        if (!Auth::user() || !method_exists(Auth::user(), 'isAdmin') || !Auth::user()->isAdmin()) {
            return redirect()->back()
                ->with('error', 'Product Type (Item) is required. Please select a Product Type.')
                ->withInput();
        }
        \Log::warning('Product created without ProductType by admin', [
            'user_id' => Auth::id(),
            'product_name' => $request->Name
        ]);
    }

    $product['Name'] = $request->Name;
    $product['CategoryId'] = $request->CategoryId;
    $product['SubCategoryId'] = $request->SubCategoryId;
    $product['ItemId'] = $request->ItemId;
    $product['SeriesId'] = $request->SeriesId ?? 0;
    $product['MakeId'] = $request->MakeId ?? 0;
    $product['SKU'] = $request->SKU;
    $product['GenericId'] = $request->GenericId; // Required
    $product['Description'] = $request->Description;
    $product['ProductType'] = 2; // Specific product
    $product['UOM'] = $request->UOM;

    $pr = Product::create($product);
    
    // Check for missing required attributes (soft/hard enforcement)
    $attributeService = new \App\Services\ProductAttributeService();
    $attrData = $request->input('attributes', []);
    
    // Check if product has missing required attributes
    if ($pr->ItemId && $pr->ItemId != 0) {
        $missingAttributes = $attributeService->getMissingRequiredAttributes($pr, $attrData);
        $validationErrors = $attributeService->validateRequiredAttributes($pr, $attrData);
        
        if (!empty($missingAttributes) || !empty($validationErrors)) {
            // Check enforcement mode from config
            $enforceRequired = config('catalog.enforce_required_attributes', false);
            
            if ($enforceRequired) {
                // Hard enforcement: Block save and delete the created product
                $pr->delete();
                
                $errorMessages = !empty($validationErrors) 
                    ? $validationErrors 
                    : array_map(function($attr) { return $attr->Name; }, $missingAttributes);
                
                return redirect()->back()
                    ->withInput()
                    ->withErrors(['attributes' => $errorMessages])
                    ->with('error', 'Please fill in all required attributes: ' . implode(', ', $errorMessages));
            }
            
            // Soft enforcement: Mark as incomplete and allow save with warning
            $pr->IsAttributeComplete = false;
            $pr->save();
            
            // Log warning
            \Log::warning("Product {$pr->ProductId} created with missing required attributes", [
                'product_id' => $pr->ProductId,
                'product_name' => $pr->Name,
                'missing_attributes' => array_map(function($attr) { return $attr->Name; }, $missingAttributes)
            ]);
            
            // Show warning message but allow save
            $missingNames = implode(', ', array_map(function($attr) { return $attr->Name; }, $missingAttributes));
            
            return redirect()->route('product.index')
                ->with('success', __('Product added successfully.'))
                ->with('attribute_warning', "Product saved, but missing required attributes: {$missingNames}");
        } else {
            // All required attributes present
            $pr->IsAttributeComplete = true;
            $pr->save();
        }
    } else {
        // No ProductType - mark as incomplete
        $pr->IsAttributeComplete = false;
        $pr->save();
    }
    
    return redirect()->route('product.index')->with('success', __('Product added successfully.'));
}
```

**Request Data:**
- `Name` (required) - Product name (unique)
- `CategoryId` (required) - Parent category
- `SubCategoryId` (optional) - Parent subcategory
- `ItemId` (required) - ProductType (soft enforcement)
- `GenericId` (required) - Parent generic product
- `MakeId` (optional) - Vendor brand
- `SeriesId` (optional) - Vendor series
- `SKU` (optional) - SKU/Part number
- `Description` (optional) - Product description
- `UOM` (optional) - Unit of measure
- `attributes[]` (optional) - Attribute values

**Response:**
- Redirect to index with success message
- May include attribute warning if required attributes missing

---

#### 4.2.4 edit() - Show Edit Form

**Route:** `GET /product/{ProductId}/edit`

**Purpose:** Display form to edit existing specific product

**Key Features:**
- Eager loads product with all relationships
- Loads applicable attributes using ProductAttributeService
- Shows required attributes
- Loads Generic products for dropdown
- Loads Make/Series for dropdown

**Code:**
```php
public function edit($ProductId)
{
    // Eager load product with relationships including attributes
    $product = Product::with([
        'category',
        'subcategory',
        'item',
        'productAttributes.attribute'
    ])->where('ProductId', $ProductId)->first();
    
    $category = Category::pluck('Name', 'CategoryId')->ToArray();
    $subcategory = SubCategory::where('CategoryId', $product->CategoryId)->pluck('Name', 'SubCategoryId')->ToArray();

    // Load Make for category
    $make = MakeCategory::join('makes', 'makes.MakeId', '=', 'make_categories.MakeId')
        ->where('CategoryId', $product->CategoryId)
        ->pluck('makes.Name', 'makes.MakeId')
        ->toArray();
    
    // Load Series for category and make
    $series = SeriesCategory::join('series', 'series.SeriesId', '=', 'series_categories.SeriesId')
        ->join('series_makes', 'series.SeriesId', '=', 'series_makes.SeriesId')
        ->where('series_categories.CategoryId', $product->CategoryId)
        ->where('series_makes.MakeId', $product->MakeId)
        ->pluck('series.Name', 'series.SeriesId')
        ->toArray();

    $item = Item::where('CategoryId', $product->CategoryId)->pluck('Name', 'ItemId')->ToArray();

    // Load Generic products for category/subcategory/item
    $Generic = Product::where('CategoryId', $product->CategoryId);
    if($product->SubCategoryId != 0){
        $Generic = $Generic->where('SubCategoryId', $product->SubCategoryId);
    }
    if($product->ItemId != 0){
        $Generic = $Generic->where('ItemId', $product->ItemId);
    }
    $Generic = $Generic->where('ProductType', 1)
        ->groupby('ProductId', 'Name')
        ->pluck('Name', 'ProductId')
        ->toArray();
    
    // Get applicable attributes using ProductAttributeService
    $attributeService = new \App\Services\ProductAttributeService();
    $applicableAttributes = $attributeService->getApplicableAttributesForProduct($product);
    
    // Get all attributes for the dropdown
    $allAttributes = Attribute::orderBy('Name')->get(['AttributeId', 'Name', 'Code', 'Unit', 'ValueType']);
    
    // Get required attribute IDs for marking in the view
    $requiredAttributeIds = collect();
    if ($product->ItemId) {
        $requiredAttributes = $attributeService->getRequiredAttributes($product->ItemId);
        $requiredAttributeIds = $requiredAttributes->pluck('AttributeId');
    }
    
    return view('product.edit', compact('product', 'category', 'subcategory', 'make', 'item', 'series', 'Generic', 'applicableAttributes', 'allAttributes', 'requiredAttributeIds', 'attributeService'));
}
```

**Response Data:**
- `$product` - Product model with relationships
- `$category` - All categories (for dropdown)
- `$subcategory` - SubCategories for selected category
- `$make` - Makes for selected category
- `$series` - Series for selected category and make
- `$item` - Items for selected category
- `$Generic` - Generic products for selected category/subcategory/item
- `$applicableAttributes` - Attributes applicable to this product
- `$allAttributes` - All available attributes
- `$requiredAttributeIds` - Required attribute IDs
- `$attributeService` - ProductAttributeService instance

---

#### 4.2.5 update() - Update Specific Product

**Route:** `PUT /product/{ProductId}`

**Purpose:** Update existing specific product

**Validation:** Handled by `UpdateProductRequest`

**Key Features:**
- Updates product fields
- Handles attribute values (new system)
- Validates required attributes (soft/hard enforcement)
- Updates IsAttributeComplete flag
- Supports GenericId change

**Code:**
```php
public function update(UpdateProductRequest $request, $ProductId)
{
    // Update product
    Product::where('ProductId', $ProductId)->update([
        'Name' => $request->Name,
        'GenericId' => $request->GenericId,
        'CategoryId' => $request->CategoryId,
        'SubCategoryId' => $request->SubCategoryId,
        'ItemId' => $request->ItemId,
        'SeriesId' => $request->SeriesId ?? 0,
        'MakeId' => $request->MakeId ?? 0,
        'SKU' => $request->SKU,
        'Description' => $request->Description,
        'UOM' => $request->UOM
    ]);

    // Check for missing required attributes (soft enforcement)
    $attributeService = new \App\Services\ProductAttributeService();
    $product = Product::findOrFail($ProductId);
    
    $attrData = $request->input('attributes', []);
    
    // Validate against the ItemId from request
    $requestItemId = $request->ItemId ?? $product->ItemId;
    $missingAttributes = [];
    $validationErrors = [];
    
    if ($requestItemId && $requestItemId != 0) {
        $tempProduct = clone $product;
        $tempProduct->ItemId = $requestItemId;
        
        $missingAttributes = $attributeService->getMissingRequiredAttributes($tempProduct, $attrData);
        $validationErrors = $attributeService->validateRequiredAttributes($tempProduct, $attrData);
        
        // Check enforcement mode from config
        $enforceRequired = config('catalog.enforce_required_attributes', false);
        
        if (!empty($validationErrors)) {
            if ($enforceRequired) {
                // Hard enforcement: Block save
                return redirect()->back()
                    ->withInput()
                    ->withErrors(['attributes' => $validationErrors])
                    ->with('error', 'Please fill in all required attributes: ' . implode(', ', $validationErrors));
            }
            // Soft enforcement: Continue with warning
        }
    }
    
    // Handle Product Attributes
    $currentAttributeIds = ProductAttribute::where('ProductId', $ProductId)
        ->pluck('AttributeId')
        ->toArray();
    
    $newAttributeIds = [];
    
    foreach ($attrData as $key => $row) {
        $attributeId = $row['AttributeId'] ?? $key;
        
        if (empty($attributeId) || $attributeId == '0') {
            continue;
        }
        
        $value = trim($row['Value'] ?? '');
        $displayValue = trim($row['DisplayValue'] ?? '');
        
        // Validate ValueType if attribute exists
        $attribute = Attribute::find($attributeId);
        if ($attribute && $attribute->ValueType === 'number' && $value && !is_numeric($value)) {
            return redirect()->back()
                ->withInput()
                ->with('error', "Attribute '{$attribute->Name}' requires a numeric value.");
        }
        
        // If value is empty, delete existing if any
        if (empty($value)) {
            ProductAttribute::where('ProductId', $ProductId)
                ->where('AttributeId', $attributeId)
                ->delete();
            continue;
        }
        
        // Update or create ProductAttribute
        ProductAttribute::updateOrCreate(
            [
                'ProductId' => $ProductId,
                'AttributeId' => $attributeId,
            ],
            [
                'Value' => $value,
                'DisplayValue' => $displayValue ?: null,
            ]
        );
        
        $newAttributeIds[] = $attributeId;
    }
    
    // Remove attributes that are no longer in the request
    $attributesToRemove = array_diff($currentAttributeIds, $newAttributeIds);
    if (!empty($attributesToRemove)) {
        ProductAttribute::where('ProductId', $ProductId)
            ->whereIn('AttributeId', $attributesToRemove)
            ->delete();
    }

    // Re-check attribute completeness after saving
    $updatedProduct = Product::findOrFail($ProductId);
    $isAttributeComplete = 1;
    $missingAttributesForWarning = [];
    
    if ($updatedProduct->ItemId && $updatedProduct->ItemId != 0) {
        $finalAttrData = [];
        $savedAttributes = ProductAttribute::where('ProductId', $ProductId)->get();
        foreach ($savedAttributes as $pa) {
            $finalAttrData[$pa->AttributeId] = [
                'Value' => $pa->Value,
                'DisplayValue' => $pa->DisplayValue
            ];
        }
        
        $missingAttributesForWarning = $attributeService->getMissingRequiredAttributes($updatedProduct, $finalAttrData);
        
        if (!empty($missingAttributesForWarning)) {
            $isAttributeComplete = 0;
        }
    }
    
    // Update IsAttributeComplete flag
    Product::where('ProductId', $ProductId)->update([
        'IsAttributeComplete' => $isAttributeComplete
    ]);
    
    // Prepare redirect message
    $redirect = redirect()->route('product.index');
    
    if ($isAttributeComplete) {
        $redirect->with('success', __('Product Updated successfully.'));
    } else {
        // Soft enforcement: Show success but with warning
        $missingNames = $missingAttributesForWarning->pluck('Name')->implode(', ');
        $redirect->with('success', __('Product Updated successfully.'))
                 ->with('attribute_warning', "Product saved, but missing required attributes: {$missingNames}")
                 ->with('missing_attributes', $missingAttributesForWarning->pluck('AttributeId')->toArray());
    }
    
    return $redirect;
}
```

**Request Data:**
- `Name` (required) - Product name (unique except current)
- `GenericId` (required) - Parent generic product
- `CategoryId` (required) - Parent category
- `SubCategoryId` (optional) - Parent subcategory
- `ItemId` (optional) - ProductType
- `MakeId` (optional) - Vendor brand
- `SeriesId` (optional) - Vendor series
- `SKU` (optional) - SKU/Part number
- `Description` (optional) - Product description
- `UOM` (optional) - Unit of measure
- `attributes[]` (optional) - Attribute values

**Response:**
- Redirect to index with success message
- May include attribute warning if required attributes missing

---

#### 4.2.6 destroy() - Delete Specific Product

**Route:** `DELETE /product/{ProductId}`

**Purpose:** Delete specific product (if no prices exist)

**Validation:** Checks if prices exist before deletion

**Code:**
```php
public function destroy($ProductId)
{
    $products = Price::where('ProductId', $ProductId)->first();
    if($products){
        $data['message'] = 'There are many Price Assign to this Product.';
        $data['success'] = 'error';
    } else {
        $data['message'] = 'Product deleted successfully.';
        $data['success'] = 'success';
        Product::where('ProductId', $ProductId)->delete();
    }
    return $data;
}
```

**Validation Rule:**
- Cannot delete if price entries exist with this ProductId
- Hard delete (soft delete via Status field not used in this controller)

**Response:**
- JSON with `success` and `message` keys

---

### 4.3 Request Validation

#### StoreProductRequest

**File:** `app/Http/Requests/StoreProductRequest.php`

**Validation Rules:**
```php
'Name' => 'required|unique:products',
'CategoryId' => 'required|exists:categories,CategoryId',
'GenericId' => 'required|exists:products,ProductId',
'ItemId' => 'required|exists:items,ItemId',
'SubCategoryId' => 'nullable|exists:sub_categories,SubCategoryId',
'MakeId' => 'nullable|exists:makes,MakeId',
'SeriesId' => 'nullable|exists:series,SeriesId',
'SKU' => 'nullable|string|max:255',
'Description' => 'nullable|string',
'UOM' => 'nullable|string|max:32',
```

#### UpdateProductRequest

**File:** `app/Http/Requests/UpdateProductRequest.php`

**Validation Rules:**
```php
'Name' => 'required|unique:products,Name,' . $this->ProductId . ',ProductId',
'CategoryId' => 'required|exists:categories,CategoryId',
'GenericId' => 'required|exists:products,ProductId',
'ItemId' => 'required|exists:items,ItemId',
'SubCategoryId' => 'nullable|exists:sub_categories,SubCategoryId',
'MakeId' => 'nullable|exists:makes,MakeId',
'SeriesId' => 'nullable|exists:series,SeriesId',
'SKU' => 'nullable|string|max:255',
'Description' => 'nullable|string',
'UOM' => 'nullable|string|max:32',
```

---

## 5. Views & UI

### 5.1 View Files

#### 5.1.1 Index View

**File:** `resources/views/product/index.blade.php`

**Purpose:** Display list of specific products

**Features:**
- NEPL Table Component
- Pagination (25 items per page default)
- Category filtering dropdown
- Eager loaded relationships (category, subcategory, item, generic, prices)
- Price display (latest effective price)
- Filterable and sortable columns

**Columns:**
- Name (sortable)
- SKU (sortable)
- Generic (from relationship - links to generic product)
- Category (from relationship)
- SubCategory (from relationship)
- Price (latest effective price from prices table)

**Action Buttons:**
- Edit (route: product.edit)
- Delete (route: product.destroy)

**Filter Options:**
- Category dropdown (filters products by CategoryId)

---

#### 5.1.2 Create View

**File:** `resources/views/product/create.blade.php`

**Purpose:** Form to create new specific product

**Form Fields:**
- Category (required, dropdown - all categories)
- SubCategory (optional, dropdown - loaded via AJAX based on Category)
- Item/ProductType (optional, dropdown - loaded via AJAX based on Category)
- Generic Product (required, dropdown - loaded via AJAX based on Category/SubCategory/Item)
- Make (optional, dropdown - loaded via AJAX based on Category)
- Series (optional, dropdown - loaded via AJAX based on Category and Make)
- Name (required, text input - unique)
- SKU (optional, text input - recommended)
- Description (optional, textarea)
- UOM (optional, text input)
- Attributes (optional, dynamic table - loaded via AJAX based on Category/SubCategory/Item)

**Features:**
- Cascade dropdowns (Category → SubCategory → Item → Generic)
- Make/Series cascade (Category → Make → Series)
- AJAX loading for all dependent dropdowns
- Dynamic attribute table
- Required attribute validation
- Generic product selection (required)
- AJAX support for inline modals

**Cascade Behavior:**
1. User selects Category
2. System loads SubCategories for that Category (AJAX)
3. User selects SubCategory (optional)
4. System loads Items for that Category (AJAX)
5. User selects Item (optional but recommended)
6. System loads Generic Products for Category/SubCategory/Item (AJAX)
7. User selects Generic Product (required)
8. System loads Makes for that Category (AJAX)
9. User selects Make (optional)
10. System loads Series for that Category and Make (AJAX)
11. User selects Series (optional)
12. System loads applicable attributes (AJAX)

---

#### 5.1.3 Edit View

**File:** `resources/views/product/edit.blade.php`

**Purpose:** Form to edit existing specific product

**Form Fields (pre-filled):**
- Category (required, dropdown, pre-selected)
- SubCategory (optional, dropdown, pre-selected)
- Item/ProductType (optional, dropdown, pre-selected)
- Generic Product (required, dropdown, pre-selected)
- Make (optional, dropdown, pre-selected)
- Series (optional, dropdown, pre-selected)
- Name (required, text input, pre-filled)
- SKU (optional, text input, pre-filled)
- Description (optional, textarea, pre-filled)
- UOM (optional, text input, pre-filled)
- Attributes (dynamic table, pre-filled with existing values)

**Features:**
- Pre-filled with existing data
- Cascade dropdowns (Category → SubCategory → Item → Generic)
- Make/Series cascade (Category → Make → Series)
- Dynamic attribute table with existing values
- Required attributes marked
- Can add/remove attributes
- Can change Generic Product
- Update button

**Attribute Display:**
- Shows applicable attributes based on ProductType (ItemId) priority
- Shows required attributes (marked)
- Shows currently assigned attributes (pre-filled)
- Inherits attributes from Generic Product (can modify)
- Allows manual addition of attributes
- Supports both new and legacy attribute systems

---

### 5.2 UI Components

#### Cascade Dropdowns

**Category → SubCategory → Item → Generic:**
- Category selection triggers SubCategory loading
- SubCategory selection triggers Item loading
- Item selection triggers Generic Product loading
- Generic Product selection (required)

**Category → Make → Series:**
- Category selection triggers Make loading
- Make selection triggers Series loading
- Series selection (optional)

**AJAX Endpoints:**
- `/getSubcategory/{categoryId}` - Get subcategories for category
- `/getItem/{categoryId}` - Get items for category
- `/getGeneric/{categoryId}/{subCategoryId}/{itemId}` - Get generic products
- `/getMake/{categoryId}` - Get makes for category
- `/getSeries/{categoryId}/{makeId}` - Get series for category and make
- Attribute loading handled by ProductAttributeService

#### Attribute Table

**Dynamic Table Features:**
- Rows added/removed dynamically
- Required attributes marked with asterisk (*)
- Value type validation (number, text, enum)
- Unit display (from attribute definition)
- Display value formatting (Value + Unit)
- Inherits values from Generic Product (can modify)

**Attribute Actions:**
- Add attribute (from dropdown)
- Remove attribute (button)
- Edit attribute value (inline)
- Inherit from Generic (button - copies from Generic Product)

#### Price Display

**Price Column:**
- Shows latest effective price from prices table
- Format: Currency format (e.g., "2,500.00")
- If no price: Shows "0.00"
- Links to price list management (optional)

---

## 6. Relationships & Dependencies

### 6.1 Database Relationships

#### Many-to-One Relationships

**Specific Product → Category**
```sql
products.CategoryId = categories.CategoryId
WHERE products.ProductType = 2
```
- Specific product must belong to one category (required)
- Category can have many specific products

**Specific Product → SubCategory**
```sql
products.SubCategoryId = sub_categories.SubCategoryId
WHERE products.ProductType = 2
```
- Specific product can belong to one subcategory (optional)
- SubCategory can have many specific products

**Specific Product → Item (ProductType)**
```sql
products.ItemId = items.ItemId
WHERE products.ProductType = 2
```
- Specific product can belong to one item/product type (optional but recommended)
- Item can have many specific products

**Specific Product → Generic Product**
```sql
products.GenericId = generic_product.ProductId
WHERE products.ProductType = 2 AND generic_product.ProductType = 1
```
- Specific product must belong to one generic product (required)
- Generic product can have many specific products
- Self-reference relationship

**Specific Product → Make**
```sql
products.MakeId = makes.MakeId
WHERE products.ProductType = 2
```
- Specific product can belong to one make (optional)
- Make can have many specific products

**Specific Product → Series**
```sql
products.SeriesId = series.SeriesId
WHERE products.ProductType = 2
```
- Specific product can belong to one series (optional)
- Series can have many specific products

#### One-to-Many Relationships

**Specific Product → ProductAttributes**
```sql
product_attributes.ProductId = products.ProductId
WHERE products.ProductType = 2
```
- Specific product can have many attribute values
- Each attribute value is a ProductAttribute record

**Specific Product → Prices**
```sql
prices.ProductId = products.ProductId
WHERE products.ProductType = 2
```
- Specific product can have many price entries
- Each price entry has EffectiveDate for version control

---

### 6.2 Eloquent Relationships

#### Parent Relationships

**belongsTo Category**
```php
$specificProduct->category
```
- Returns Category model
- Foreign key: `products.CategoryId`
- Required relationship

**belongsTo SubCategory**
```php
$specificProduct->subcategory
```
- Returns SubCategory model (or null)
- Foreign key: `products.SubCategoryId`
- Optional relationship

**belongsTo Item (ProductType)**
```php
$specificProduct->item
```
- Returns Item model (or null)
- Foreign key: `products.ItemId`
- Optional but recommended relationship

**belongsTo Generic Product**
```php
$specificProduct->generic
```
- Returns Generic Product model (ProductType = 1)
- Foreign key: `products.GenericId`
- Required relationship
- Self-reference

**belongsTo Make**
```php
$specificProduct->make
```
- Returns Make model (or null)
- Foreign key: `products.MakeId`
- Optional relationship

**belongsTo Series**
```php
$specificProduct->series
```
- Returns Series model (or null)
- Foreign key: `products.SeriesId`
- Optional relationship

#### Child Relationships

**hasMany ProductAttributes**
```php
$specificProduct->productAttributes
```
- Returns collection of ProductAttribute models
- Foreign key: `product_attributes.ProductId`
- Ordered by SortOrder

**hasMany Prices**
```php
$specificProduct->prices
```
- Returns collection of Price models
- Foreign key: `prices.ProductId`

**hasOne Current Price**
```php
$specificProduct->currentPrice
```
- Returns single Price model (latest effective)
- Foreign key: `prices.ProductId`
- Filtered by EffectiveDate <= today, Status = 0
- Ordered by EffectiveDate DESC

---

### 6.3 Reverse Relationships

#### Generic Product hasMany Specific Products
```php
$genericProduct->specificProducts
```
- Returns collection of Specific Product models (ProductType = 2)
- Foreign key: `products.GenericId`
- Self-reference relationship

#### Category hasMany Specific Products
```php
$category->products()->where('ProductType', 2)
```
- Returns collection of Specific Product models
- Foreign key: `products.CategoryId`
- Filtered by `ProductType = 2`

#### Make hasMany Specific Products
```php
Make::find($makeId)->products()->where('ProductType', 2)
```
- Returns collection of Specific Product models
- Foreign key: `products.MakeId`
- Filtered by `ProductType = 2`

#### Series hasMany Specific Products
```php
Series::find($seriesId)->products()->where('ProductType', 2)
```
- Returns collection of Specific Product models
- Foreign key: `products.SeriesId`
- Filtered by `ProductType = 2`

---

### 6.4 Dependencies

#### Specific Product Dependencies (What Specific Product Needs)

**Models:**
- `Category` - Required parent (CategoryId)
- `SubCategory` - Optional parent (SubCategoryId)
- `Item` - Optional parent (ItemId - ProductType)
- `Product` (Generic) - Required parent (GenericId)
- `Make` - Optional parent (MakeId)
- `Series` - Optional parent (SeriesId)
- `ProductAttribute` - For attribute values
- `Price` - For price list entries

**Controllers:**
- `ProductController` - Main controller
- `CategoryController` - Parent controller
- `SubCategoryController` - Parent controller
- `ItemController` - Parent controller
- `GenericController` - Parent controller (for Generic Product)
- `MakeController` - Parent controller
- `SeriesController` - Parent controller
- `PriceController` - For price management

**Services:**
- `ProductAttributeService` - For attribute resolution and validation

---

#### Specific Product Dependents (What Depends on Specific Product)

**Models that use Specific Product:**
- `Price` - Stores price entries (ProductId required)
- `ProductAttribute` - Stores attribute values
- `QuotationSaleBomItem` - References ProductId (L2 only)
- `MasterBomItem` - Cannot reference specific products (L0/L1 only)

**Controllers that use Specific Product:**
- `QuotationV2Controller` - Uses specific products for BOM items
- `PriceController` - Manages prices for specific products
- `ProductAttributeController` - Manages attributes for specific products

---

### 6.5 Specific Product Lifecycle

```
Generic Product Exists
    ↓
Create Specific Product (ProductType = 2, GenericId = Generic.ProductId)
    ↓
Select Make/Series (optional)
    ↓
Enter SKU (recommended)
    ↓
Assign Attribute Values (inherits from Generic, can modify)
    ↓
Add Price (from Price List)
    ↓
[Specific Product Ready for Quotations]
    ↓
Use in Quotation BOM Items (L2, ProductId required)
    ↓
Price Lookup (from prices table)
    ↓
Costing Calculation
```

---

## 7. Workflows & Operations

### 7.1 Create Specific Product Workflow

#### Step 1: Navigate to Specific Product Master
```
Navigation: Master Data → Specific Product Master
Action: Click "Create Specific Product" button
```

#### Step 2: Select Taxonomy
```
Form Fields:
- Category: [Select from dropdown] (required)
  → System loads SubCategories via AJAX
- SubCategory: [Select from dropdown] (optional)
  → System loads Items via AJAX
- Item/ProductType: [Select from dropdown] (recommended)
  → System loads Generic Products via AJAX
```

#### Step 3: Select Generic Product
```
Form Fields:
- Generic Product: [Select from dropdown] (required)
  → Shows generic products for selected Category/SubCategory/Item
  → User must select a Generic Product
```

#### Step 4: Select Vendor Details (Optional)
```
Form Fields:
- Make: [Select from dropdown] (optional)
  → System loads Makes for selected Category via AJAX
- Series: [Select from dropdown] (optional)
  → System loads Series for selected Category and Make via AJAX
```

#### Step 5: Enter Product Details
```
Form Fields:
- Name: "Acti9 iC60N 100A" (required, unique)
- SKU: "A9N61616" (recommended)
- Description: "Schneider Acti9 iC60N 100A MCCB" (optional)
- UOM: "Pcs" (optional)
```

#### Step 6: Assign Attribute Values
```
System Actions:
1. Loads applicable attributes based on Category/SubCategory/Item
2. Pre-fills attribute values from Generic Product (inheritance)
3. Shows required attributes (marked with *)
4. User can:
   - Modify inherited attribute values
   - Add new attributes
   - Remove attributes
```

#### Step 7: Submit Form
```
Action: Click "Save" button
System Actions:
1. Validates Name (required, unique)
2. Validates GenericId (required, must exist)
3. Validates ItemId (required - soft enforcement)
4. Validates required attributes (soft/hard enforcement)
5. Creates Product record (ProductType = 2)
6. Creates ProductAttribute records (if provided)
7. Sets IsAttributeComplete flag
8. Returns success message (may include attribute warning)
```

#### Step 8: Add Price
```
Navigation: Master Data → Price List → Create
Form Fields:
- ProductId: [Select: Specific Product created in Step 7]
- Rate: 2500.00
- EffectiveDate: 2025-01-01
Action: Save
```

#### Step 9: Verify Creation
```
Navigation: Specific Product Master List
Verify:
- New specific product appears in list
- Generic Product shown correctly
- Make/Series shown correctly (if selected)
- SKU shown correctly
- Price shown correctly (if added)
- Can edit/delete specific product
- Ready for use in quotations
```

---

### 7.2 Edit Specific Product Workflow

#### Step 1: Navigate to Specific Product List
```
Navigation: Master Data → Specific Product Master
Action: Click "Edit" button for specific product
```

#### Step 2: Modify Product
```
Form Fields (pre-filled):
- Category: [Current category] (can change)
- SubCategory: [Current subcategory] (can change)
- Item/ProductType: [Current item] (can change)
- Generic Product: [Current generic] (can change)
- Make: [Current make] (can change)
- Series: [Current series] (can change)
- Name: "Acti9 iC60N 100A" (can modify)
- SKU: "A9N61616" (can modify)
- Description: "Schneider Acti9 iC60N 100A MCCB" (can modify)
- Attributes: [Current values] (can modify)
```

#### Step 3: Update Attributes
```
System Actions:
1. Loads applicable attributes (may change if ItemId changed)
2. Shows existing attribute values (pre-filled)
3. Shows inherited values from Generic Product
4. Shows required attributes (marked)
5. User can:
   - Modify existing attribute values
   - Add new attributes
   - Remove attributes
   - Inherit from Generic (copy from Generic Product)
```

#### Step 4: Submit Changes
```
Action: Click "Update" button
System Actions:
1. Validates Name (required, unique except current)
2. Validates GenericId (required, must exist)
3. Validates required attributes (soft/hard enforcement)
4. Updates Product record
5. Updates ProductAttribute records
6. Updates IsAttributeComplete flag
7. Returns success message (may include attribute warning)
```

#### Step 5: Verify Update
```
Navigation: Specific Product Master List
Verify:
- Product name/details updated
- Generic Product updated (if changed)
- Make/Series updated (if changed)
- Attributes updated
- IsAttributeComplete flag updated
- Warning shown if required attributes missing (soft enforcement)
```

---

### 7.3 Delete Specific Product Workflow

#### Step 1: Navigate to Specific Product List
```
Navigation: Master Data → Specific Product Master
Action: Click "Delete" button for specific product
```

#### Step 2: System Validation
```
System Checks:
- Are there price entries with ProductId = this ProductId?
  - YES → Error: "There are many Price Assign to this Product."
  - NO → Proceed with deletion
```

#### Step 3: Deletion Result
```
If Validation Passes:
- Specific product deleted (hard delete)
- ProductAttribute records deleted (cascade)
- Success message: "Product deleted successfully."

If Validation Fails:
- Specific product NOT deleted
- Error message: "There are many Price Assign to this Product."
```

---

### 7.4 Add Price to Specific Product Workflow

#### Step 1: Navigate to Price List
```
Navigation: Master Data → Price List → Create
```

#### Step 2: Select Product
```
Form Fields:
- ProductId: [Select: Specific Product] (required)
  → Shows only specific products (ProductType = 2)
```

#### Step 3: Enter Price Details
```
Form Fields:
- Rate: 2500.00 (required, decimal)
- EffectiveDate: 2025-01-01 (required, date)
```

#### Step 4: Submit Form
```
Action: Click "Save" button
System Actions:
1. Validates ProductId (required, must exist)
2. Validates Rate (required, decimal)
3. Validates EffectiveDate (required, date)
4. Creates Price record
5. Returns success message
```

#### Step 5: Verify Price
```
Navigation: Specific Product Master List
Verify:
- Price shown in product list
- Latest effective price displayed
- Can add multiple prices with different EffectiveDate
```

---

### 7.5 Inherit Attributes from Generic Product Workflow

#### Step 1: Navigate to Specific Product Edit
```
Navigation: Master Data → Specific Product Master → Edit
View: Product edit form with attributes table
```

#### Step 2: Click "Inherit from Generic" Button
```
Action: Click "Inherit from Generic" button
System Actions:
1. Loads attribute values from Generic Product (GenericId)
2. Pre-fills attribute table with Generic's values
3. User can modify inherited values
```

#### Step 3: Modify Inherited Values (Optional)
```
User Actions:
- Modify inherited attribute values
- Add new attributes
- Remove attributes
```

#### Step 4: Save Changes
```
Action: Click "Update" button
System Actions:
1. Updates ProductAttribute records
2. Inherited values saved
3. Modified values saved
4. Returns success message
```

---

## 8. Code Examples

### 8.1 Create Specific Product

```php
// Simple specific product creation
$specificProduct = Product::create([
    'Name' => 'Acti9 iC60N 100A',
    'CategoryId' => 1, // Protection Devices
    'SubCategoryId' => 5, // Circuit Breakers
    'ItemId' => 10, // MCCB Feeder
    'GenericId' => 1001, // Links to Generic Product
    'MakeId' => 50, // Schneider Electric
    'SeriesId' => 25, // Acti9
    'SKU' => 'A9N61616',
    'ProductType' => 2, // Specific
    'Description' => 'Schneider Acti9 iC60N 100A MCCB',
    'UOM' => 'Pcs',
    'Status' => 0,
]);

// Specific product with attributes (inherited from Generic)
$genericProduct = Product::where('ProductType', 1)->find(1001);
$specificProduct = Product::create([
    'Name' => 'Acti9 iC60N 100A',
    'CategoryId' => $genericProduct->CategoryId,
    'SubCategoryId' => $genericProduct->SubCategoryId,
    'ItemId' => $genericProduct->ItemId,
    'GenericId' => $genericProduct->ProductId,
    'MakeId' => 50,
    'SeriesId' => 25,
    'SKU' => 'A9N61616',
    'ProductType' => 2,
]);

// Inherit attributes from Generic Product
$genericAttributes = ProductAttribute::where('ProductId', $genericProduct->ProductId)->get();
foreach ($genericAttributes as $genericAttr) {
    ProductAttribute::create([
        'ProductId' => $specificProduct->ProductId,
        'AttributeId' => $genericAttr->AttributeId,
        'Value' => $genericAttr->Value, // Inherit value
        'DisplayValue' => $genericAttr->DisplayValue, // Inherit display value
    ]);
}
```

---

### 8.2 Get Specific Product with Relationships

```php
// Get specific product with all relationships
$specificProduct = Product::where('ProductType', 2)
    ->with(['category', 'subcategory', 'item', 'generic', 'make', 'series', 'productAttributes.attribute', 'prices'])
    ->find(1);

// Get specific product with current price
$specificProduct = Product::where('ProductType', 2)
    ->with('currentPrice')
    ->find(1);
    
$currentPrice = $specificProduct->currentPrice;
if ($currentPrice) {
    echo $currentPrice->Rate; // Latest effective price
}

// Get specific product with generic product
$specificProduct = Product::where('ProductType', 2)
    ->with('generic')
    ->find(1);
    
echo $specificProduct->generic->Name; // Generic product name
```

---

### 8.3 Get Specific Products by Criteria

```php
// Get all specific products
$specificProducts = Product::where('ProductType', 2)->get();

// Get specific products by generic product
$genericProduct = Product::where('ProductType', 1)->find(1001);
$specificProducts = Product::where('ProductType', 2)
    ->where('GenericId', $genericProduct->ProductId)
    ->get();

// Get specific products by make
$specificProducts = Product::where('ProductType', 2)
    ->where('MakeId', 50) // Schneider Electric
    ->get();

// Get specific products by make and series
$specificProducts = Product::where('ProductType', 2)
    ->where('MakeId', 50)
    ->where('SeriesId', 25) // Acti9
    ->get();

// Get specific products in a category
$specificProducts = Product::where('ProductType', 2)
    ->where('CategoryId', 1)
    ->get();
```

---

### 8.4 Get Applicable Attributes for Specific Product

```php
use App\Services\ProductAttributeService;

$specificProduct = Product::where('ProductType', 2)->find(1);
$service = new ProductAttributeService();

// Get applicable attributes
$applicableAttributes = $service->getApplicableAttributesForProduct($specificProduct);

foreach ($applicableAttributes as $categoryAttribute) {
    $attribute = $categoryAttribute->attribute;
    echo $attribute->Name . ' (' . $attribute->Unit . ')';
    if ($categoryAttribute->IsRequired) {
        echo ' [Required]';
    }
}
```

---

### 8.5 Inherit Attributes from Generic Product

```php
$specificProduct = Product::where('ProductType', 2)->find(1);
$genericProduct = $specificProduct->generic; // Get parent generic product

// Get generic product attributes
$genericAttributes = ProductAttribute::where('ProductId', $genericProduct->ProductId)->get();

// Copy attributes to specific product
foreach ($genericAttributes as $genericAttr) {
    ProductAttribute::updateOrCreate(
        [
            'ProductId' => $specificProduct->ProductId,
            'AttributeId' => $genericAttr->AttributeId,
        ],
        [
            'Value' => $genericAttr->Value, // Inherit value
            'DisplayValue' => $genericAttr->DisplayValue, // Inherit display value
        ]
    );
}
```

---

### 8.6 Get Current Price for Specific Product

```php
$specificProduct = Product::where('ProductType', 2)->find(1);

// Get latest effective price
$currentPrice = Price::where('ProductId', $specificProduct->ProductId)
    ->where('EffectiveDate', '<=', now())
    ->where('Status', 0)
    ->orderBy('EffectiveDate', 'DESC')
    ->first();

if ($currentPrice) {
    echo $currentPrice->Rate; // Current price
} else {
    echo 'No price found';
}

// Using relationship
$currentPrice = $specificProduct->currentPrice;
if ($currentPrice) {
    echo $currentPrice->Rate;
}
```

---

### 8.7 Check Specific Product Usage

```php
// Check if specific product has prices
$specificProduct = Product::find(1);
$hasPrices = $specificProduct->prices()->exists();

// Count prices
$priceCount = $specificProduct->prices()->count();

// Check if specific product is used in quotations
$usedInQuotations = QuotationSaleBomItem::where('ProductId', $specificProduct->ProductId)
    ->where('Status', 0)
    ->exists();

// Check if specific product can be deleted
$canDelete = !$specificProduct->prices()->exists();
```

---

## 9. Troubleshooting

### 9.1 Common Issues

#### Issue 1: Cannot Delete Specific Product

**Symptoms:**
- Delete button shows error
- Message: "There are many Price Assign to this Product."

**Cause:**
- Price entries exist with this ProductId
- Specific product is referenced by price list

**Solution:**
1. **Check Prices:**
   ```php
   $prices = Price::where('ProductId', $productId)->get();
   ```

2. **Delete Prices:**
   ```php
   Price::where('ProductId', $productId)->delete();
   ```

3. **Then Delete Product:**
   ```php
   Product::where('ProductId', $productId)->delete();
   ```

---

#### Issue 2: Specific Product Name Not Unique

**Symptoms:**
- Validation error when creating/updating
- Message: "The name has already been taken."

**Cause:**
- Another product (generic or specific) with same name exists

**Solution:**
1. **Check Existing Products:**
   ```php
   $existing = Product::where('Name', $name)->first();
   ```

2. **Use Different Name:**
   - Choose unique name
   - Or update existing product instead

---

#### Issue 3: Generic Product Not Found

**Symptoms:**
- Generic Product dropdown is empty
- Cannot select Generic Product

**Cause:**
- No generic products exist for selected Category/SubCategory/Item
- Generic products filtered incorrectly

**Solution:**
1. **Check Generic Products:**
   ```php
   $genericProducts = Product::where('ProductType', 1)
       ->where('CategoryId', $categoryId)
       ->where('SubCategoryId', $subCategoryId)
       ->where('ItemId', $itemId)
       ->get();
   ```

2. **Create Generic Product First:**
   - Navigate to Generic Product Master
   - Create generic product for the Category/SubCategory/Item
   - Then create specific product

---

#### Issue 4: Attributes Not Inheriting from Generic

**Symptoms:**
- Specific product edit form shows no attributes
- Generic product has attributes but not showing

**Cause:**
- Attributes not loaded from Generic Product
- Inheritance not triggered

**Solution:**
1. **Check Generic Product Attributes:**
   ```php
   $genericProduct = $specificProduct->generic;
   $genericAttributes = ProductAttribute::where('ProductId', $genericProduct->ProductId)->get();
   ```

2. **Manually Inherit:**
   - Click "Inherit from Generic" button in edit form
   - Or manually copy attributes via code (see Code Examples)

---

#### Issue 5: Price Not Showing

**Symptoms:**
- Specific product shows "0.00" price
- Price exists in prices table

**Cause:**
- EffectiveDate is in future
- Price Status = 1 (deleted)
- Query filtering incorrectly

**Solution:**
1. **Check Price EffectiveDate:**
   ```php
   $price = Price::where('ProductId', $productId)
       ->where('EffectiveDate', '<=', now())
       ->where('Status', 0)
       ->orderBy('EffectiveDate', 'DESC')
       ->first();
   ```

2. **Update EffectiveDate:**
   ```php
   Price::where('PriceId', $priceId)->update([
       'EffectiveDate' => now()->format('Y-m-d')
   ]);
   ```

---

### 9.2 Data Validation Queries

#### Query 1: Find Specific Products Without Generic Product
```sql
SELECT 
    p.ProductId,
    p.Name,
    p.SKU,
    p.GenericId
FROM products p
WHERE p.ProductType = 2
AND (p.GenericId IS NULL OR p.GenericId = 0);
```

#### Query 2: Find Specific Products Without Prices
```sql
SELECT 
    p.ProductId,
    p.Name,
    p.SKU,
    COUNT(pr.PriceId) as price_count
FROM products p
LEFT JOIN prices pr ON p.ProductId = pr.ProductId AND pr.Status = 0
WHERE p.ProductType = 2
GROUP BY p.ProductId, p.Name, p.SKU
HAVING price_count = 0;
```

#### Query 3: Find Specific Products by Generic Product
```sql
SELECT 
    p.ProductId,
    p.Name,
    p.SKU,
    gp.Name AS GenericName
FROM products p
JOIN products gp ON p.GenericId = gp.ProductId
WHERE p.ProductType = 2
AND gp.ProductType = 1
AND gp.ProductId = 1001;
```

#### Query 4: Find Specific Products with Most Prices
```sql
SELECT 
    p.ProductId,
    p.Name,
    p.SKU,
    COUNT(pr.PriceId) as price_count
FROM products p
LEFT JOIN prices pr ON p.ProductId = pr.ProductId AND pr.Status = 0
WHERE p.ProductType = 2
GROUP BY p.ProductId, p.Name, p.SKU
ORDER BY price_count DESC
LIMIT 10;
```

---

## 10. Complete Code File Mapping

### 10.1 Database

| Component | File/Table | Type | Purpose |
|-----------|-----------|------|---------|
| **Table** | `products` | Database Table | Stores specific products (ProductType = 2) |
| **Primary Key** | `ProductId` | INT, AI | Unique identifier |
| **Foreign Key** | `CategoryId` | INT, FK | References categories table (required) |
| **Foreign Key** | `SubCategoryId` | INT, FK | References sub_categories table (optional) |
| **Foreign Key** | `ItemId` | INT, FK | References items table (optional but recommended) |
| **Foreign Key** | `GenericId` | INT, FK | References products table (self-reference, required) |
| **Foreign Key** | `MakeId` | INT, FK | References makes table (optional) |
| **Foreign Key** | `SeriesId` | INT, FK | References series table (optional) |
| **Table** | `product_attributes` | Database Table | Stores attribute values for specific products |
| **Table** | `prices` | Database Table | Stores price entries for specific products |

---

### 10.2 Models

| Component | File | Type | Purpose |
|-----------|------|------|---------|
| **Model** | `app/Models/Product.php` | Eloquent Model | Specific product data access (ProductType = 2) |
| **Relationships** | `belongsTo Category` | Relationship | Parent category |
| **Relationships** | `belongsTo SubCategory` | Relationship | Parent subcategory |
| **Relationships** | `belongsTo Item` | Relationship | Parent item/product type |
| **Relationships** | `belongsTo Generic Product` | Relationship | Parent generic product (self-reference) |
| **Relationships** | `belongsTo Make` | Relationship | Vendor brand |
| **Relationships** | `belongsTo Series` | Relationship | Vendor series |
| **Relationships** | `hasMany ProductAttributes` | Relationship | Attribute values |
| **Relationships** | `hasMany Prices` | Relationship | Price list entries |
| **Relationships** | `hasOne Current Price` | Relationship | Latest effective price |

---

### 10.3 Controllers

| Component | File | Type | Purpose |
|-----------|------|------|---------|
| **Controller** | `app/Http/Controllers/ProductController.php` | Controller | Specific product CRUD operations |
| **Method** | `index()` | GET | List specific products |
| **Method** | `create()` | GET | Show create form |
| **Method** | `store()` | POST | Create specific product |
| **Method** | `edit()` | GET | Show edit form |
| **Method** | `update()` | PUT | Update specific product |
| **Method** | `destroy()` | DELETE | Delete specific product |

---

### 10.4 Services

| Component | File | Type | Purpose |
|-----------|------|------|---------|
| **Service** | `app/Services/ProductAttributeService.php` | Service | Attribute resolution and validation |

---

### 10.5 Views

| Component | File | Type | Purpose |
|-----------|------|------|---------|
| **View** | `resources/views/product/index.blade.php` | Blade View | Specific product list |
| **View** | `resources/views/product/create.blade.php` | Blade View | Create specific product form |
| **View** | `resources/views/product/edit.blade.php` | Blade View | Edit specific product form |

---

### 10.6 Routes

| Route | Method | Controller | Action | Purpose |
|-------|--------|------------|--------|---------|
| `/product` | GET | ProductController | `index()` | List specific products |
| `/product/create` | GET | ProductController | `create()` | Show create form |
| `/product` | POST | ProductController | `store()` | Create specific product |
| `/product/{id}/edit` | GET | ProductController | `edit()` | Show edit form |
| `/product/{id}` | PUT | ProductController | `update()` | Update specific product |
| `/product/{id}` | DELETE | ProductController | `destroy()` | Delete specific product |

---

### 10.7 Dependencies

#### Specific Product Depends On:
- `Category` model (required - CategoryId)
- `SubCategory` model (optional - SubCategoryId)
- `Item` model (optional but recommended - ItemId)
- `Product` model (Generic, required - GenericId)
- `Make` model (optional - MakeId)
- `Series` model (optional - SeriesId)
- `ProductAttribute` model (for attribute values)
- `Price` model (for price list entries)
- `ProductAttributeService` (for attribute resolution)

#### Depends On Specific Product:
- `Price` model (ProductId required)
- `ProductAttribute` model (ProductId required)
- `QuotationSaleBomItem` model (ProductId required for L2)
- `QuotationV2Controller` (uses specific products for BOM items)
- `PriceController` (manages prices for specific products)

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial comprehensive document | Complete specific item master design |
| 1.1 | 2025-12-19 | Phase-3 | Inserted canonical L0/L1/L2 definitions; terminology aligned | Phase-3: Rule Compliance Review |

---

**END OF DOCUMENT**

**This document is a PERMANENT STANDARD for all specific item master-related work.**
