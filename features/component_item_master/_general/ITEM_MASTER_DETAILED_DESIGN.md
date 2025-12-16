> Source: source_snapshot/ITEM_MASTER_DETAILED_DESIGN.md
> Bifurcated into: features/component_item_master/ITEM_MASTER_DETAILED_DESIGN.md
> Module: Component / Item Master > General
> Date: 2025-12-17 (IST)

# Item Master Detailed Design & Architecture

**Document:** ITEM_MASTER_DETAILED_DESIGN.md  
**Version:** 1.0  
**Date:** December 2025  
**Status:** 🔴 **STANDING INSTRUCTION - PERMANENT STANDARD**

---

## 📋 Table of Contents

1. [Item Master Overview](#1-item-master-overview)
2. [Item Master Structure & Components](#2-item-master-structure--components)
3. [Component Connections & Relationships](#3-component-connections--relationships)
4. [Resolution Levels (L0/L1/L2)](#4-resolution-levels-l0l1l2)
5. [Item Creation Principles](#5-item-creation-principles)
6. [Generic vs Specific Items](#6-generic-vs-specific-items)
7. [Master BOM System](#7-master-bom-system)
8. [Proposal BOM System](#8-proposal-bom-system)
9. [Feeder Master & Panel Master](#9-feeder-master--panel-master)
10. [Pricing Integration](#10-pricing-integration)
11. [Design Principles & Maintenance](#11-design-principles--maintenance)

---

## 1. Item Master Overview

### 1.1 Purpose

The **Item Master** is the central catalog system that stores all buyable components/products used in quotations. It serves as:

- **Product Catalog:** Centralized repository of all components
- **Pricing Source:** Links to price lists for commercial rates
- **BOM Foundation:** Base for building Master BOMs and Proposal BOMs
- **Attribute Repository:** Stores technical specifications via attributes

### 1.2 Core Concept

**Item Master = Product Master = Component Master**

All three terms refer to the same entity: the `products` table, which contains:
- Generic products (ProductType = 1)
- Specific products (ProductType = 2)
- Complete product hierarchy (Category → SubCategory → Type → Product)

---

## 2. Item Master Structure & Components

### 2.1 Complete Hierarchy

```
Category (Required)
  └── SubCategory (Optional)
        └── Item/ProductType (Optional, stored in `items` table)
              └── Generic Product (ProductType = 1)
                    └── Make (Optional)
                          └── Series (Optional)
                                └── Specific Product (ProductType = 2)
```

### 2.2 Database Tables

#### 2.2.1 Categories Table (`categories`)

**Purpose:** Top-level classification

**Key Columns:**
- `CategoryId` (PK, Auto-increment)
- `Name` (Required)
- `Details` (Optional)

**Examples:**
- "Electrical Panels"
- "Cables"
- "Transformers"
- "Protection Devices"

**Relationships:**
- `hasMany` SubCategories
- `hasMany` Items
- `hasMany` Products

**Model:** `App\Models\Category`

---

#### 2.2.2 SubCategories Table (`sub_categories`)

**Purpose:** Sub-classification within categories

**Key Columns:**
- `SubCategoryId` (PK, Auto-increment)
- `CategoryId` (FK, Required)
- `Name` (Required)
- `Details` (Optional)

**Examples (under "Electrical Panels"):**
- "Distribution Panels"
- "Control Panels"
- "Motor Control Centers"

**Relationships:**
- `belongsTo` Category
- `hasMany` Items
- `hasMany` Products

**Model:** `App\Models\SubCategory`

---

#### 2.2.3 Items Table (`items` - Used as ProductType)

**Purpose:** Functional type/classification (ProductType)

**Key Columns:**
- `ItemId` (PK, Auto-increment)
- `CategoryId` (FK, Required)
- `SubCategoryId` (FK, Optional)
- `Name` (Required)
- `Details` (Optional)

**Note:** This table is used as "ProductType" or "Type" in the system.

**Examples (under "Protection Devices" → "Circuit Breakers"):**
- "MCCB Feeder"
- "MCCB Incomer"
- "MCB"
- "Contactor"

**Relationships:**
- `belongsTo` Category
- `belongsTo` SubCategory
- `hasMany` Products

**Model:** `App\Models\Item`

---

#### 2.2.4 Products Table (`products`)

**Purpose:** Actual buyable items (Component Master)

**Key Columns:**
- `ProductId` (PK, Auto-increment)
- `Name` (Required)
- `CategoryId` (FK, Required)
- `SubCategoryId` (FK, Optional)
- `ItemId` (FK, Optional - ProductType)
- `ProductType` (Required: 1=Generic, 2=Specific)
- `GenericId` (FK, Self-reference - links Specific to Generic)
- `MakeId` (FK, Optional)
- `SeriesId` (FK, Optional)
- `SKU` (Optional)
- `Description` (Optional)
- `Generic` (Optional - legacy field)
- `UOM` (Unit of Measure)
- `Status` (0=Active, 1=Deleted)

**Product Types:**
- **ProductType = 1:** Generic Product (base product without make/series)
- **ProductType = 2:** Specific Product (variant with make/series/SKU)

**Self-Reference:**
- `GenericId` links Specific Products (Type=2) back to Generic Product (Type=1)

**Relationships:**
- `belongsTo` Category
- `belongsTo` SubCategory
- `belongsTo` Item (ProductType)
- `belongsTo` Make
- `belongsTo` Series
- `belongsTo` Generic (self-reference)
- `hasMany` Specific Products (reverse of Generic)
- `hasMany` Prices
- `hasMany` ProductAttributes
- `belongsToMany` Attributes (via product_attributes)

**Model:** `App\Models\Product`

---

#### 2.2.5 Makes Table (`makes`)

**Purpose:** OEM brands/manufacturers

**Key Columns:**
- `MakeId` (PK, Auto-increment)
- `Name` (Required)
- `Status` (0=Active, 1=Deleted)

**Examples:**
- "Schneider Electric"
- "ABB"
- "Siemens"
- "L&T"

**Model:** `App\Models\Make`

---

#### 2.2.6 Series Table (`series`)

**Purpose:** OEM product series/families

**Key Columns:**
- `SeriesId` (PK, Auto-increment)
- `Name` (Required)
- `Status` (0=Active, 1=Deleted)

**Examples:**
- "SIVACON S8"
- "Acti9"
- "iID"
- "PowerPact"

**Model:** `App\Models\Series`

---

#### 2.2.7 Attributes System

**Three-Table Structure:**

**1. Attributes Table (`attributes`)**
- `AttributeId` (PK)
- `Name` (e.g., "Voltage", "Current Rating", "IP Rating")
- `DataType` (Text, Number, Enum, etc.)
- `IsActive` (0/1)

**2. Category Attributes Table (`category_attributes`)**
- `CategoryAttributeId` (PK)
- `CategoryId` (FK)
- `SubCategoryId` (FK, Optional)
- `ItemId` (FK, Optional)
- `AttributeId` (FK)
- **Purpose:** Defines which attributes apply to which category/subcategory/type

**3. Product Attributes Table (`product_attributes`)**
- `ProductAttributeId` (PK)
- `ProductId` (FK)
- `AttributeId` (FK)
- `Value` (Actual value, e.g., "415V", "100A", "IP54")
- `DisplayValue` (Formatted display)
- `SortOrder` (Display order)

**Key Rule:**
- **Attribute definition** belongs to **Type(ProductType)** via `category_attributes`
- **Attribute values** belong to **Product** via `product_attributes`

---

#### 2.2.8 Prices Table (`prices`)

**Purpose:** Commercial rates per product with effective dates

**Key Columns:**
- `PriceId` (PK, Auto-increment)
- `ProductId` (FK, Required)
- `Rate` (Required, Decimal)
- `EffectiveDate` (Required, Date)
- `Status` (0=Active, 1=Deleted)

**Purpose:**
- Centralized rate management
- Version control via EffectiveDate
- Historical rate tracking
- Automatic rate updates for PRICELIST items

**Model:** `App\Models\Price`

---

## 3. Component Connections & Relationships

### 3.1 Foreign Key Relationships

```sql
-- Products relationships
products.CategoryId → categories.CategoryId
products.SubCategoryId → sub_categories.SubCategoryId
products.ItemId → items.ItemId
products.GenericId → products.ProductId (self-reference)
products.MakeId → makes.MakeId
products.SeriesId → series.SeriesId

-- Items relationships
items.CategoryId → categories.CategoryId
items.SubCategoryId → sub_categories.SubCategoryId

-- SubCategories relationships
sub_categories.CategoryId → categories.CategoryId

-- Prices relationships
prices.ProductId → products.ProductId

-- Attributes relationships
category_attributes.CategoryId → categories.CategoryId
category_attributes.AttributeId → attributes.AttributeId
product_attributes.ProductId → products.ProductId
product_attributes.AttributeId → attributes.AttributeId
```

### 3.2 Eloquent Relationships

#### Category Model Relationships:
```php
// Category hasMany SubCategories
public function subcategories()

// Category hasMany Items
public function items()

// Category hasMany Products
public function products()
```

#### Product Model Relationships:
```php
// Product belongsTo Category
public function category()

// Product belongsTo SubCategory
public function subcategory()

// Product belongsTo Item (ProductType)
public function item()

// Product belongsTo Make
public function make()

// Product belongsTo Series
public function series()

// Product belongsTo Generic (self-reference)
public function generic()

// Product hasMany Specific Products
public function specificProducts()

// Product hasMany Prices
public function prices()

// Product hasOne Current Price (latest effective)
public function currentPrice()

// Product belongsToMany Attributes
public function attributes()
```

### 3.3 Data Flow Connections

```
User Input → Category Selection
    ↓
SubCategory Selection (optional)
    ↓
Item/ProductType Selection (optional)
    ↓
Generic Product Selection (ProductType=1)
    ↓
Make Selection (optional)
    ↓
Series Selection (optional)
    ↓
Specific Product Selection (ProductType=2)
    ↓
Price Lookup (from prices table)
    ↓
Attribute Values (from product_attributes)
    ↓
BOM Item Creation (quotation_sale_bom_items)
```

---

## 4. Resolution Levels (L0/L1/L2)

### 4.1 Level Definitions

**Resolution Levels** define the specificity of a BOM item:

#### L0 - Generic Placeholder
- **Definition:** Unresolved generic descriptor
- **ProductId:** NULL (not allowed)
- **Content:** `GenericDescriptor` (text description)
- **Example:** "MCCB 100A", "Cable 3.5 Core"
- **Use Case:** Early design phase, placeholder items
- **Pricing:** Not priceable (Rate=0, Amount=0)
- **Status:** Incomplete, requires resolution

#### L1 - Defined Specification
- **Definition:** Specification defined but not yet mapped to product
- **ProductId:** NULL (not allowed)
- **Content:** `DefinedSpecJson` (structured specification)
- **Example:** `{"Voltage": "415V", "Current": "100A", "Breaking": "25kA"}`
- **Use Case:** Specification known, product selection pending
- **Pricing:** Not priceable (Rate=0, Amount=0)
- **Status:** Incomplete, requires product mapping

#### L2 - Resolved Product
- **Definition:** Fully resolved to specific ProductId
- **ProductId:** Required (must exist)
- **Content:** ProductId reference to `products` table
- **Example:** ProductId = 12345 (specific MCCB product)
- **Use Case:** Production BOM, ready for pricing
- **Pricing:** Priceable (Rate from prices table or manual)
- **Status:** Complete, ready for costing

### 4.2 Level Implementation

#### Master BOM Items (MasterBomItem)

**Allowed Levels:** L0, L1 only

**Fields:**
```php
'ResolutionStatus' => 'L0' | 'L1'
'ProductId' => NULL (forced by guardrail)
'GenericDescriptor' => string (for L0)
'DefinedSpecJson' => JSON (for L1)
'SpecKey' => string (optional identifier)
```

**Validation Rules:**
- L0/L1: ProductId must be NULL
- L1: DefinedSpecJson required
- L0: GenericDescriptor recommended (warning if missing)
- L2: NOT allowed in Master BOM

**Model:** `App\Models\MasterBomItem`

**Guardrail (Model Boot Hook):**
```php
protected static function boot()
{
    static::saving(function ($item) {
        $resolutionStatus = $item->ResolutionStatus ?? 'L0';
        
        // G1: If L0 or L1, force ProductId to NULL
        if (in_array($resolutionStatus, ['L0', 'L1'])) {
            $item->ProductId = null;
        }
    });
}
```

---

#### Production BOM Items (QuotationSaleBomItem)

**Allowed Levels:** L2 only (currently)

**Fields:**
```php
'ProductId' => Required (integer)
'ResolutionStatus' => 'L2' (implicit, not stored)
'Rate' => decimal (from prices or manual)
'Discount' => decimal (percentage)
'NetRate' => decimal (calculated)
'Amount' => decimal (calculated)
'RateSource' => 'PRICELIST' | 'MANUAL_WITH_DISCOUNT' | 'FIXED_NO_DISCOUNT' | 'UNRESOLVED'
'IsPriceMissing' => boolean (computed)
```

**Validation Rules:**
- ProductId: Required
- Rate: Required (or IsPriceMissing=1)
- ResolutionStatus: Implicitly L2 (not stored, always resolved)

**Model:** `App\Models\QuotationSaleBomItem`

---

### 4.3 Level Conversion Flow

```
Master BOM (L0/L1)
    ↓
[User applies Master BOM to Quotation]
    ↓
Proposal BOM Created (copied from Master)
    ↓
[User resolves items]
    ↓
L0 → L1: Add DefinedSpecJson
    ↓
L1 → L2: Map to ProductId
    ↓
Production BOM Item (L2, ProductId required)
    ↓
Price Lookup (from prices table)
    ↓
Costing Calculation
```

### 4.4 Level Reflection in UI

#### Master BOM Edit Screen:
- **L0 Items:** Show GenericDescriptor field
- **L1 Items:** Show DefinedSpecJson editor
- **ProductId Field:** Hidden/disabled (not allowed)

#### Proposal BOM Screen:
- **L0 Items:** Display GenericDescriptor, show "Resolve" button
- **L1 Items:** Display DefinedSpecJson, show "Map to Product" button
- **L2 Items:** Display Product name, show price and costing

#### Production BOM Screen:
- **All Items:** L2 only, ProductId required
- **Missing ProductId:** Flagged as `IsPriceMissing=1`, `RateSource=UNRESOLVED`

---

## 5. Item Creation Principles

### 5.1 Standard Product Creation Workflow

#### Step 1: Taxonomy Setup (Once per Type)

1. **Create Category**
   - Navigate to: Master Data → Category
   - Enter: Name (e.g., "Protection Devices")
   - Save

2. **Create SubCategory** (Optional)
   - Navigate to: Master Data → SubCategory
   - Select: Category
   - Enter: Name (e.g., "Circuit Breakers")
   - Save

3. **Create Type/ProductType** (Optional)
   - Navigate to: Master Data → Item (Product Type)
   - Select: Category, SubCategory (optional)
   - Enter: Name (e.g., "MCCB Feeder")
   - Save

4. **Map Attributes to Type**
   - Navigate to: Master Data → Category Attributes
   - Select: Category, SubCategory, Item
   - Map: Attributes (e.g., Voltage, Current Rating, Breaking Capacity)
   - Save

---

#### Step 2: Create Make & Series

1. **Create Make**
   - Navigate to: Master Data → Make
   - Enter: Name (e.g., "Schneider Electric")
   - Save

2. **Create Series**
   - Navigate to: Master Data → Series
   - Enter: Name (e.g., "Acti9")
   - **Note:** Series can be linked to Make via `series_makes` table

---

#### Step 3: Create Generic Product (ProductType = 1)

**Navigate to:** Master Data → Generic Product Master

**Required Fields:**
- `CategoryId` (Required)
- `ItemId` (ProductType, Recommended)
- `Name` (Required)
- `ProductType` = 1 (Generic)

**Optional Fields:**
- `SubCategoryId`
- `Description`
- `SKU`
- `UOM`

**Attribute Values:**
- After saving, assign attribute values via Product Attributes screen
- Attributes available based on Category/SubCategory/Item mapping

**Example:**
```
Category: Protection Devices
SubCategory: Circuit Breakers
Item: MCCB Feeder
Name: MCCB 100A Standard
ProductType: 1 (Generic)
Attributes:
  - Voltage: 415V
  - Current Rating: 100A
  - Breaking Capacity: 25kA
```

---

#### Step 4: Create Specific Product (ProductType = 2)

**Navigate to:** Master Data → Specific Product Master

**Required Fields:**
- `CategoryId` (Required)
- `GenericId` (Required - links to Generic Product)
- `Name` (Required)
- `ProductType` = 2 (Specific)

**Optional Fields:**
- `SubCategoryId`
- `ItemId`
- `MakeId`
- `SeriesId`
- `SKU` (Recommended for specific products)
- `Description`

**Attribute Values:**
- Inherits attributes from Generic Product
- Can override or add specific values

**Example:**
```
GenericId: [Generic Product: MCCB 100A Standard]
MakeId: Schneider Electric
SeriesId: Acti9
Name: Acti9 iC60N 100A
SKU: A9N61616
ProductType: 2 (Specific)
Attributes:
  - Voltage: 415V (inherited)
  - Current Rating: 100A (inherited)
  - Breaking Capacity: 25kA (inherited)
  - Model: iC60N (specific)
```

---

#### Step 5: Add Price

**Navigate to:** Master Data → Price List

**Required Fields:**
- `ProductId` (Required)
- `Rate` (Required, Decimal)
- `EffectiveDate` (Required, Date)

**Purpose:**
- Centralized rate management
- Version control via EffectiveDate
- Automatic rate updates for PRICELIST items

**Example:**
```
ProductId: [Specific Product: Acti9 iC60N 100A]
Rate: 2500.00
EffectiveDate: 2025-01-01
```

---

### 5.2 Item Creation Rules

#### Rule 1: Category is Required
- Every product must have a CategoryId
- Category drives attribute schema
- Category determines available SubCategories and Items

#### Rule 2: ProductType is Required
- Must be 1 (Generic) or 2 (Specific)
- Generic products can exist without Make/Series
- Specific products must have GenericId

#### Rule 3: GenericId Self-Reference
- Specific products (Type=2) must reference Generic product (Type=1)
- GenericId links Specific → Generic
- Enables product variant management

#### Rule 4: Attribute Mapping
- Attributes defined at Category/SubCategory/Item level
- Attribute values assigned at Product level
- Products must satisfy required attributes for their Type

#### Rule 5: Make/Series Optional
- Products can exist without Make/Series
- Make/Series used for vendor-specific products
- Series typically linked to Make

---

## 6. Generic vs Specific Items

### 6.1 Generic Items (ProductType = 1)

#### Definition
**Generic Items** are base products without vendor-specific details (Make/Series).

#### Characteristics
- **ProductType:** 1
- **MakeId:** NULL (typically)
- **SeriesId:** NULL (typically)
- **GenericId:** NULL (self-reference not used)
- **Purpose:** Template/base product
- **Use Case:** Early design, placeholder, catalog building

#### Example
```
ProductId: 1001
Name: "MCCB 100A Standard"
CategoryId: 1 (Protection Devices)
SubCategoryId: 5 (Circuit Breakers)
ItemId: 10 (MCCB Feeder)
ProductType: 1 (Generic)
MakeId: NULL
SeriesId: NULL
Attributes:
  - Voltage: 415V
  - Current Rating: 100A
  - Breaking Capacity: 25kA
```

#### When to Use
- Building product catalog
- Early quotation design
- Placeholder items in Master BOM
- Template products for variants

---

### 6.2 Specific Items (ProductType = 2)

#### Definition
**Specific Items** are vendor-specific products with Make/Series/SKU details.

#### Characteristics
- **ProductType:** 2
- **GenericId:** Required (links to Generic Product)
- **MakeId:** Optional (but recommended)
- **SeriesId:** Optional (but recommended)
- **SKU:** Recommended for specific products
- **Purpose:** Production-ready product
- **Use Case:** Final quotation, pricing, procurement

#### Example
```
ProductId: 2001
Name: "Acti9 iC60N 100A"
CategoryId: 1 (Protection Devices)
SubCategoryId: 5 (Circuit Breakers)
ItemId: 10 (MCCB Feeder)
ProductType: 2 (Specific)
GenericId: 1001 (links to Generic: "MCCB 100A Standard")
MakeId: 50 (Schneider Electric)
SeriesId: 25 (Acti9)
SKU: "A9N61616"
Attributes:
  - Voltage: 415V (inherited from Generic)
  - Current Rating: 100A (inherited from Generic)
  - Breaking Capacity: 25kA (inherited from Generic)
  - Model: iC60N (specific)
```

#### When to Use
- Production BOMs
- Final quotations
- Pricing and costing
- Procurement orders

---

### 6.3 Generic vs Specific Relationship

```
Generic Product (ProductType=1)
    ├── Specific Product A (ProductType=2, GenericId=Generic.ProductId)
    ├── Specific Product B (ProductType=2, GenericId=Generic.ProductId)
    └── Specific Product C (ProductType=2, GenericId=Generic.ProductId)
```

**Key Points:**
- One Generic can have many Specifics
- Each Specific links back to Generic via GenericId
- Specifics inherit attributes from Generic
- Specifics add vendor-specific details (Make/Series/SKU)

---

### 6.4 Basis of Generic vs Specific

#### Generic Items Basis:
1. **Functional Classification:** What it does (MCCB, MCB, Contactor)
2. **Technical Specifications:** Voltage, Current, Breaking Capacity
3. **Catalog Organization:** Base products for variant creation
4. **Design Phase:** Early design, placeholder items

#### Specific Items Basis:
1. **Vendor Selection:** Which manufacturer (Schneider, ABB, Siemens)
2. **Model/Series:** Specific product line (Acti9, SIVACON S8)
3. **SKU/Part Number:** Exact part identifier
4. **Production Phase:** Final quotation, pricing, procurement

---

## 7. Master BOM System

### 7.1 Master BOM Definition

**Master BOM** is a reusable template BOM that contains generic/specification-level items (L0/L1 only). It serves as a template for creating Proposal BOMs.

#### Key Characteristics:
- **Template Type:** Reusable across multiple quotations
- **Resolution Levels:** L0 and L1 only (no L2, no ProductId)
- **No Pricing:** Cannot have prices (not priceable)
- **Purpose:** Design template, specification template
- **Storage:** `master_boms` and `master_bom_items` tables

---

### 7.2 Master BOM Structure

#### Master BOM Header (`master_boms`)

**Key Columns:**
- `MasterBomId` (PK)
- `Name` (Required)
- `UniqueNo` (Required, Unique)
- `Description` (Optional)
- `TemplateType` (FEEDER, PANEL, GENERIC, etc.)
- `IsActive` (1=Active, 0=Archived)
- `DefaultFeederName` (Optional - suggested name when applying)

**Model:** `App\Models\MasterBom`

**Scopes:**
```php
// Get only feeder templates
MasterBom::feederTemplates()->get();

// Get all templates
MasterBom::templates()->get();

// Get only active templates
MasterBom::active()->get();
```

---

#### Master BOM Items (`master_bom_items`)

**Key Columns:**
- `MasterBomItemId` (PK)
- `MasterBomId` (FK)
- `ProductId` (NULL - not allowed for L0/L1)
- `Quantity` (Required)
- `UOM` (Unit of Measure)
- `ResolutionStatus` (Required: 'L0' or 'L1')
- `GenericDescriptor` (For L0 - text description)
- `DefinedSpecJson` (For L1 - JSON specification)
- `SpecKey` (Optional identifier)

**Model:** `App\Models\MasterBomItem`

**Validation Rules (B4 Rules):**
1. ResolutionStatus must be L0 or L1 (L2 not allowed)
2. If L0/L1, ProductId must be NULL
3. L1 items must have DefinedSpecJson
4. L0 items should have GenericDescriptor (warning if missing)

**Guardrail (Model Boot Hook):**
```php
protected static function boot()
{
    static::saving(function ($item) {
        $resolutionStatus = $item->ResolutionStatus ?? 'L0';
        
        // G1: If L0 or L1, force ProductId to NULL
        if (in_array($resolutionStatus, ['L0', 'L1'])) {
            $item->ProductId = null;
        }
    });
}
```

---

### 7.3 Master BOM Creation Process

#### Step 1: Create Master BOM Header

**Navigate to:** Master Data → Master BOM → Create

**Required Fields:**
- `Name` (e.g., "Distribution Panel Standard Components")
- `UniqueNo` (Unique identifier)
- `Description` (Optional)

**Optional Fields:**
- `TemplateType` (FEEDER, PANEL, GENERIC)
- `DefaultFeederName` (Suggested name when applying)

**Process:**
1. Enter Name and UniqueNo
2. Save (creates header only)
3. Edit to add items

---

#### Step 2: Add Master BOM Items

**Navigate to:** Master Data → Master BOM → Edit

**For Each Item:**

**L0 Item (Generic Placeholder):**
- Select: ResolutionStatus = L0
- Enter: GenericDescriptor (e.g., "MCCB 100A")
- Enter: Quantity
- Enter: UOM
- Save

**L1 Item (Defined Specification):**
- Select: ResolutionStatus = L1
- Enter: DefinedSpecJson (e.g., `{"Voltage": "415V", "Current": "100A"}`)
- Enter: Quantity
- Enter: UOM
- Save

**Validation:**
- ProductId field is hidden/disabled (not allowed)
- ResolutionStatus must be L0 or L1
- L1 must have DefinedSpecJson
- L0 should have GenericDescriptor

---

### 7.4 Master BOM Conversion: Generic to Specific

#### Conversion Flow

```
Master BOM (L0/L1)
    ↓
[User applies Master BOM to Quotation]
    ↓
Proposal BOM Created (copied from Master)
    ↓
[User resolves items in Proposal BOM]
    ↓
L0 → L1: Add DefinedSpecJson
    ↓
L1 → L2: Map to ProductId
    ↓
Production BOM Item (L2, ProductId required)
    ↓
Price Lookup (from prices table)
    ↓
Costing Calculation
```

#### Level-by-Level Conversion

**L0 → L1 Conversion:**
1. User selects L0 item in Proposal BOM
2. User clicks "Define Specification"
3. User enters specification details:
   - Voltage: 415V
   - Current: 100A
   - Breaking Capacity: 25kA
4. System saves as DefinedSpecJson
5. ResolutionStatus updated to L1

**L1 → L2 Conversion:**
1. User selects L1 item in Proposal BOM
2. User clicks "Map to Product"
3. System shows product search:
   - Filter by Category → SubCategory → Item
   - Filter by Make/Series (optional)
   - Show products matching DefinedSpecJson
4. User selects ProductId
5. System updates:
   - ProductId = selected product
   - ResolutionStatus = L2 (implicit)
   - Rate = from prices table (if available)
   - RateSource = PRICELIST (or UNRESOLVED if no price)

**L2 Production BOM Item:**
- ProductId: Required
- Rate: From prices table or manual
- RateSource: PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT, or UNRESOLVED
- IsPriceMissing: Computed (Rate=0 and not client supplied)
- Ready for costing

---

### 7.5 Master BOM Maintenance

#### Archiving
- Set `IsActive = 0` to archive (not delete)
- Archived BOMs not shown in active templates
- Can be reactivated later

#### Editing
- Can edit Name, Description, TemplateType
- Can add/remove items
- Can modify quantities
- Changes don't affect existing Proposal BOMs (they're copied)

#### Copying
- Can copy Master BOM to create new template
- Useful for creating variants
- Maintains all items and quantities

---

### 7.6 Master BOM Use Cases

1. **Standard Panel Templates:**
   - Pre-defined panel configurations
   - Common component lists
   - Reusable across quotations

2. **Feeder Templates:**
   - Standard feeder configurations
   - Common component sets
   - Quick feeder creation

3. **Specification Templates:**
   - L1 items with DefinedSpecJson
   - Technical specification templates
   - Design phase templates

4. **Placeholder Templates:**
   - L0 items with GenericDescriptor
   - Early design phase
   - Incomplete specifications

---

## 8. Proposal BOM System

### 8.1 Proposal BOM Definition

**Proposal BOM** is a UX feature that allows users to browse and reuse past Production BOMs (from completed quotations) as templates for new quotations.

#### Key Characteristics:
- **Source:** Past Production BOMs (from completed quotations)
- **Resolution Level:** L2 only (fully resolved with ProductId)
- **Pricing:** May have prices (from original quotation)
- **Purpose:** Reuse successful BOMs, quick quotation creation
- **Storage:** Same tables as Production BOMs (`quotation_sale_boms`, `quotation_sale_bom_items`)

---

### 8.2 Proposal BOM vs Master BOM

| Feature | Master BOM | Proposal BOM |
|---------|------------|--------------|
| **Resolution Levels** | L0, L1 only | L2 only |
| **ProductId** | Not allowed | Required |
| **Pricing** | Not priceable | May have prices |
| **Source** | Created as template | From past quotations |
| **Purpose** | Design template | Reuse successful BOMs |
| **Maintenance** | Manual creation/editing | Auto-created from quotations |

---

### 8.3 Proposal BOM Creation

#### Automatic Creation
- When a quotation is completed/approved, its Production BOMs become available as Proposal BOMs
- No manual creation needed
- System automatically marks completed quotations as "Proposal BOM sources"

#### Manual Selection
- User browses past quotations
- User selects a Production BOM from past quotation
- System copies BOM structure to new quotation
- User can modify as needed

---

### 8.4 Proposal BOM Design Basis

#### Design Principles:
1. **Copy, Never Link:** Always copy BOM structure, never link directly
2. **Independent Instance:** Each Proposal BOM is independent
3. **Modifiable:** User can modify copied BOM
4. **Price Refresh:** Prices can be refreshed from current price list

#### Implementation:
```php
// Copy Proposal BOM to new quotation
$sourceBom = QuotationSaleBom::find($proposalBomId);
$newBom = new QuotationSaleBom();
$newBom->QuotationSaleId = $newPanelId;
$newBom->MasterBomId = $sourceBom->MasterBomId; // Reference only
$newBom->BomName = $sourceBom->BomName;
$newBom->Qty = $sourceBom->Qty;
// ... copy other fields
$newBom->save();

// Copy items
foreach ($sourceBom->item()->where('Status', 0)->get() as $sourceItem) {
    $newItem = new QuotationSaleBomItem();
    $newItem->QuotationSaleBomId = $newBom->QuotationSaleBomId;
    $newItem->ProductId = $sourceItem->ProductId; // Copy ProductId
    $newItem->Qty = $sourceItem->Qty; // Copy quantity
    $newItem->Rate = $sourceItem->Rate; // Copy rate (can be refreshed)
    // ... copy other fields
    $newItem->save();
}
```

---

### 8.5 Proposal BOM Maintenance

#### Browsing
- User can browse past quotations
- Filter by category, date, client
- View BOM structure before copying

#### Copying
- User selects Proposal BOM
- System copies to new quotation
- User can modify structure and quantities
- Prices can be refreshed from current price list

#### Updating
- After copying, Proposal BOM becomes Production BOM
- User can modify items, quantities, prices
- Changes don't affect original Proposal BOM

---

### 8.6 Proposal BOM Use Cases

1. **Reuse Successful BOMs:**
   - Copy BOMs from successful quotations
   - Quick quotation creation
   - Proven configurations

2. **Similar Projects:**
   - Similar client requirements
   - Similar technical specifications
   - Quick adaptation

3. **Standard Configurations:**
   - Common panel configurations
   - Standard feeder setups
   - Proven component combinations

---

## 9. Feeder Master & Panel Master

### 9.1 Feeder Master Definition

**Feeder Master** is a Master BOM with `TemplateType = 'FEEDER'` that serves as a template for creating feeders in quotations.

#### Key Characteristics:
- **TemplateType:** FEEDER
- **Resolution Levels:** L0, L1 only (no L2, no ProductId)
- **Purpose:** Standard feeder template
- **Default Name:** `DefaultFeederName` field suggests name when applying

---

### 9.2 Feeder Master Creation

#### Step 1: Create Master BOM with TemplateType = FEEDER

**Navigate to:** Master Data → Master BOM → Create

**Fields:**
- `Name`: "Standard Feeder Template"
- `UniqueNo`: "FEEDER-001"
- `TemplateType`: FEEDER
- `DefaultFeederName`: "Feeder 1" (suggested name)
- `IsActive`: 1

**Save**

---

#### Step 2: Add Feeder Master Items

**Navigate to:** Master Data → Master BOM → Edit

**Add Items (L0 or L1):**
- MCCB (L0 or L1)
- Contactor (L0 or L1)
- Cable (L0 or L1)
- etc.

**Save**

---

#### Step 3: Apply Feeder Master to Quotation

**In Quotation V2 Panel Screen:**
1. User clicks "Add Feeder from Template"
2. System shows list of Feeder Masters (`TemplateType = 'FEEDER'`)
3. User selects Feeder Master
4. System creates new Feeder (QuotationSaleBom with Level=0)
5. System copies items from Feeder Master
6. System sets `OriginMasterBomId` for reference
7. User resolves items (L0→L1→L2) as needed

---

### 9.3 Panel Master Definition

**Panel Master** is a Master BOM with `TemplateType = 'PANEL'` that serves as a template for creating panels in quotations.

#### Key Characteristics:
- **TemplateType:** PANEL
- **Resolution Levels:** L0, L1 only (no L2, no ProductId)
- **Purpose:** Standard panel template
- **Structure:** May contain multiple feeders (hierarchical)

---

### 9.4 Panel Master Creation

#### Step 1: Create Master BOM with TemplateType = PANEL

**Navigate to:** Master Data → Master BOM → Create

**Fields:**
- `Name`: "Standard Distribution Panel"
- `UniqueNo`: "PANEL-001"
- `TemplateType`: PANEL
- `IsActive`: 1

**Save**

---

#### Step 2: Add Panel Master Items

**Navigate to:** Master Data → Master BOM → Edit

**Add Items (L0 or L1):**
- Incomer MCCB (L0 or L1)
- Busbar (L0 or L1)
- Feeder components (L0 or L1)
- etc.

**Note:** Panel Masters can reference Feeder Masters (hierarchical structure)

---

#### Step 3: Apply Panel Master to Quotation

**In Quotation V2 Screen:**
1. User clicks "Add Panel from Template"
2. System shows list of Panel Masters (`TemplateType = 'PANEL'`)
3. User selects Panel Master
4. System creates new Panel (QuotationSale)
5. System creates Feeders (QuotationSaleBom with Level=0)
6. System copies items from Panel Master
7. System sets `OriginMasterBomId` for reference
8. User resolves items (L0→L1→L2) as needed

---

### 9.5 Feeder/Panel Master Working Principles

#### Principle 1: Copy, Never Link
- Always copy Master BOM structure to quotation
- Never link directly
- Changes to Master BOM don't affect existing quotations

#### Principle 2: Resolution Required
- Master BOM items are L0/L1 (not resolved)
- User must resolve to L2 (ProductId) in quotation
- Resolution happens in Proposal BOM/Production BOM

#### Principle 3: Hierarchical Structure
- Panel Masters can contain multiple feeders
- Feeder Masters contain components
- System maintains hierarchy when copying

#### Principle 4: Instance Tracking
- `OriginMasterBomId` tracks source Master BOM
- `OriginMasterBomVersion` tracks version (future)
- `InstanceSequenceNo` tracks instance number

---

### 9.6 Feeder/Panel Master Maintenance

#### Archiving
- Set `IsActive = 0` to archive
- Archived templates not shown in active list
- Can be reactivated

#### Editing
- Can edit Name, Description, TemplateType
- Can add/remove items
- Can modify quantities
- Changes don't affect existing quotations (they're copied)

#### Versioning (Future)
- `OriginMasterBomVersion` field for version tracking
- Track changes over time
- Reference specific versions

---

## 10. Pricing Integration

### 10.1 Pricing Connection to Item Master

#### Price List Structure

**Prices Table (`prices`):**
- `PriceId` (PK)
- `ProductId` (FK to products - Required)
- `Rate` (Decimal - Required)
- `EffectiveDate` (Date - Required)
- `Status` (0=Active, 1=Deleted)

**Relationship:**
```
Product (products table)
    ↓
hasMany Prices (prices table)
    ↓
Latest Effective Price (EffectiveDate ≤ today)
    ↓
Rate used in Quotation BOM Items
```

---

### 10.2 Pricing Flow

#### Step 1: Product Selection
- User selects ProductId in BOM item
- System looks up Product in `products` table

#### Step 2: Price Lookup
- System queries `prices` table:
  ```sql
  SELECT Rate FROM prices
  WHERE ProductId = ?
    AND EffectiveDate <= CURDATE()
    AND Status = 0
  ORDER BY EffectiveDate DESC
  LIMIT 1
  ```

#### Step 3: Rate Assignment
- If price found:
  - `Rate` = Price from prices table
  - `RateSource` = 'PRICELIST'
  - `IsPriceMissing` = 0
- If price not found:
  - `Rate` = 0
  - `RateSource` = 'UNRESOLVED'
  - `IsPriceMissing` = 1

#### Step 4: Manual Override (Optional)
- User can override rate manually
- Requires permission
- `RateSource` = 'MANUAL_WITH_DISCOUNT' or 'FIXED_NO_DISCOUNT'
- `ManualOverrideReason` required

---

### 10.3 Rate Source Types

#### PRICELIST (Default)
- **Source:** Prices table
- **Update:** Automatic when price list updated
- **Override:** Can be overridden with permission
- **Use Case:** Standard products

#### MANUAL_WITH_DISCOUNT
- **Source:** User-entered rate
- **Discount:** Percentage discount applies
- **Calculation:** `NetRate = Rate × (1 - Discount/100)`
- **Requirement:** Permission + ManualOverrideReason
- **Use Case:** Negotiated rates, special pricing

#### FIXED_NO_DISCOUNT
- **Source:** User-entered rate
- **Discount:** Ignored (always 0)
- **Calculation:** `NetRate = Rate`
- **Requirement:** Permission + ManualOverrideReason
- **Use Case:** Fixed rates, no discount allowed

#### UNRESOLVED (System-Assigned Only)
- **Source:** System-assigned when price missing
- **Rate:** 0
- **NetRate:** 0
- **Amount:** 0
- **Requirement:** Users cannot set this manually
- **Use Case:** Missing prices, incomplete items

---

### 10.4 Pricing in Master BOM vs Production BOM

#### Master BOM (L0/L1)
- **ProductId:** NULL (not allowed)
- **Rate:** Not applicable (not priceable)
- **Purpose:** Design template, no pricing

#### Production BOM (L2)
- **ProductId:** Required
- **Rate:** From prices table or manual
- **RateSource:** PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT, or UNRESOLVED
- **Purpose:** Production BOM, ready for costing

---

### 10.5 Price List Maintenance

#### Adding Prices
1. Navigate to: Master Data → Price List
2. Select: ProductId
3. Enter: Rate
4. Enter: EffectiveDate
5. Save

#### Updating Prices
1. Navigate to: Master Data → Price List
2. Find: ProductId
3. Add: New price row with new EffectiveDate
4. System automatically uses latest effective price

#### Price History
- All prices preserved (Status=0 for active, Status=1 for deleted)
- EffectiveDate tracks when price was valid
- Historical quotations maintain original rates

---

## 11. Design Principles & Maintenance

### 11.1 Core Design Principles

#### Principle 1: Separation of Concerns
- **Master Data:** Product catalog, Master BOMs (templates)
- **Production Data:** Quotation BOMs, Proposal BOMs (instances)
- **Never mix:** Master BOMs cannot have ProductId, Production BOMs must have ProductId

#### Principle 2: Copy, Never Link
- Always copy Master BOM to quotation
- Never link directly
- Changes to Master BOM don't affect existing quotations

#### Principle 3: Resolution Levels
- **Master BOM:** L0/L1 only (generic/specification)
- **Production BOM:** L2 only (resolved with ProductId)
- **Conversion:** L0 → L1 → L2 (user-driven)

#### Principle 4: Pricing Integration
- Prices linked to ProductId
- Price list is single source of truth
- Manual overrides require permission
- Missing prices flagged automatically

#### Principle 5: Soft Delete
- Always use `Status = 0` (Active) or `Status = 1` (Deleted)
- Never hard delete
- All queries filter by `Status = 0`

---

### 11.2 Maintenance Guidelines

#### Product Master Maintenance
- **Add Products:** Follow standard workflow (Category → SubCategory → Item → Product)
- **Update Products:** Edit via Generic/Specific Product Master screens
- **Archive Products:** Set `Status = 1` (soft delete)
- **Price Updates:** Add new price row with new EffectiveDate

#### Master BOM Maintenance
- **Create Templates:** Use Master BOM create screen
- **Edit Templates:** Modify items, quantities, descriptions
- **Archive Templates:** Set `IsActive = 0`
- **Copy Templates:** Create variants from existing templates

#### Proposal BOM Maintenance
- **Browse:** View past quotations
- **Copy:** Select and copy to new quotation
- **Modify:** Edit after copying (becomes Production BOM)

#### Price List Maintenance
- **Add Prices:** New price row per product
- **Update Prices:** New row with new EffectiveDate (preserves history)
- **Archive Prices:** Set `Status = 1` (soft delete)

---

### 11.3 Data Integrity Rules

#### Rule 1: ProductId Requirement
- Production BOM items must have ProductId (L2)
- Missing ProductId = `IsPriceMissing=1`, `RateSource=UNRESOLVED`
- Cannot finalize/export without ProductId

#### Rule 2: Category Requirement
- Every product must have CategoryId
- Category drives attribute schema
- Category determines available SubCategories and Items

#### Rule 3: GenericId Self-Reference
- Specific products (Type=2) must have GenericId
- GenericId links to Generic product (Type=1)
- Enables product variant management

#### Rule 4: Resolution Status Validation
- Master BOM: L0/L1 only, ProductId must be NULL
- Production BOM: L2 only, ProductId required
- Validation enforced at model level (guardrails)

#### Rule 5: Price List Priority
- Default rate source = Price List (`PRICELIST`)
- Manual overrides require permission and reason
- Missing prices flagged automatically

---

### 11.4 Best Practices

#### Product Creation
1. **Start with Taxonomy:** Category → SubCategory → Item
2. **Create Generic First:** ProductType=1, then create Specifics
3. **Map Attributes:** Define schema at Type level, assign values at Product level
4. **Add Prices:** Create price list entries for production-ready products

#### Master BOM Creation
1. **Use L0 for Placeholders:** Generic descriptors for early design
2. **Use L1 for Specifications:** DefinedSpecJson for known specifications
3. **Never Use L2:** Master BOMs are templates, not production BOMs
4. **Set TemplateType:** FEEDER, PANEL, or GENERIC for organization

#### Proposal BOM Usage
1. **Browse Past Quotations:** Find similar successful BOMs
2. **Copy Structure:** Always copy, never link
3. **Refresh Prices:** Update rates from current price list
4. **Modify as Needed:** Adapt to new requirements

#### Price List Management
1. **Version Control:** Use EffectiveDate for price changes
2. **Historical Preservation:** Never delete prices, use Status=1
3. **Regular Updates:** Keep price list current
4. **Missing Price Flags:** Monitor and resolve UNRESOLVED items

---

---

## 12. Practical Examples & Use Cases

### 12.1 Complete Product Creation Example

#### Scenario: Create a Schneider Acti9 MCCB Product

**Step 1: Setup Taxonomy (One-time)**
```
Category: "Protection Devices" (already exists)
SubCategory: "Circuit Breakers" (already exists)
Item: "MCCB Feeder" (already exists)
```

**Step 2: Create Generic Product**
```
Navigate: Master Data → Generic Product Master → Create

Fields:
- Category: Protection Devices
- SubCategory: Circuit Breakers
- Item: MCCB Feeder
- Name: "MCCB 100A Standard"
- ProductType: 1 (Generic)
- Description: "Standard MCCB 100A"

Attributes (after saving):
- Voltage: 415V
- Current Rating: 100A
- Breaking Capacity: 25kA
- IP Rating: IP20
```

**Step 3: Create Make & Series (if not exists)**
```
Navigate: Master Data → Make → Create
- Name: "Schneider Electric"
- Save

Navigate: Master Data → Series → Create
- Name: "Acti9"
- Save
```

**Step 4: Create Specific Product**
```
Navigate: Master Data → Specific Product Master → Create

Fields:
- Category: Protection Devices
- SubCategory: Circuit Breakers
- Item: MCCB Feeder
- GenericId: [Select: MCCB 100A Standard]
- MakeId: Schneider Electric
- SeriesId: Acti9
- Name: "Acti9 iC60N 100A"
- SKU: "A9N61616"
- ProductType: 2 (Specific)
- Description: "Schneider Acti9 iC60N 100A MCCB"

Attributes (inherited from Generic):
- Voltage: 415V
- Current Rating: 100A
- Breaking Capacity: 25kA
- IP Rating: IP20
- Model: iC60N (specific)
```

**Step 5: Add Price**
```
Navigate: Master Data → Price List → Create

Fields:
- ProductId: [Select: Acti9 iC60N 100A]
- Rate: 2500.00
- EffectiveDate: 2025-01-01
- Save
```

**Result:**
- Generic Product created (ProductType=1)
- Specific Product created (ProductType=2, GenericId links to Generic)
- Price added to price list
- Product ready for use in quotations

---

### 12.2 Master BOM Creation Example

#### Scenario: Create Standard Distribution Panel Master BOM

**Step 1: Create Master BOM Header**
```
Navigate: Master Data → Master BOM → Create

Fields:
- Name: "Standard Distribution Panel Components"
- UniqueNo: "DP-STD-001"
- Description: "Standard components for distribution panel"
- TemplateType: PANEL
- DefaultFeederName: "Feeder 1"
- IsActive: 1
- Save
```

**Step 2: Add Master BOM Items (L0/L1)**

**Item 1: MCCB (L0 - Generic Placeholder)**
```
ResolutionStatus: L0
GenericDescriptor: "MCCB 100A"
Quantity: 12
UOM: Pcs
```

**Item 2: Contactor (L1 - Defined Specification)**
```
ResolutionStatus: L1
DefinedSpecJson: {
  "Voltage": "415V",
  "Current": "25A",
  "Type": "3-Pole",
  "Coil": "230V AC"
}
Quantity: 6
UOM: Pcs
```

**Item 3: Cable (L0 - Generic Placeholder)**
```
ResolutionStatus: L0
GenericDescriptor: "Cable 3.5 Core 2.5sqmm"
Quantity: 50
UOM: Mtr
```

**Result:**
- Master BOM created with L0/L1 items
- No ProductId (not allowed)
- No pricing (not priceable)
- Ready to use as template

---

### 12.3 Master BOM to Production BOM Conversion Example

#### Scenario: Apply Master BOM to Quotation and Resolve Items

**Step 1: Apply Master BOM to Quotation**
```
In Quotation V2 Panel Screen:
1. Click "Add BOM from Template"
2. Select: "Standard Distribution Panel Components"
3. System creates Proposal BOM (copied from Master)
4. Items are L0/L1 (not resolved)
```

**Step 2: Resolve L0 Item (MCCB)**
```
Current State:
- ResolutionStatus: L0
- GenericDescriptor: "MCCB 100A"
- ProductId: NULL

Action:
1. Click "Resolve Item"
2. Option A: Define Specification (L0 → L1)
   - Enter DefinedSpecJson:
     {
       "Voltage": "415V",
       "Current": "100A",
       "Breaking": "25kA"
     }
   - ResolutionStatus updated to L1

3. Option B: Map to Product (L0 → L2)
   - Search products: Category → SubCategory → Item
   - Select: "Acti9 iC60N 100A" (ProductId: 2001)
   - System updates:
     - ProductId: 2001
     - ResolutionStatus: L2 (implicit)
     - Rate: 2500.00 (from prices table)
     - RateSource: PRICELIST
     - IsPriceMissing: 0
```

**Step 3: Resolve L1 Item (Contactor)**
```
Current State:
- ResolutionStatus: L1
- DefinedSpecJson: {"Voltage": "415V", "Current": "25A", ...}
- ProductId: NULL

Action:
1. Click "Map to Product"
2. System filters products matching DefinedSpecJson
3. Select: "Schneider LC1D25" (ProductId: 3001)
4. System updates:
   - ProductId: 3001
   - ResolutionStatus: L2 (implicit)
   - Rate: 1200.00 (from prices table)
   - RateSource: PRICELIST
   - IsPriceMissing: 0
```

**Result:**
- All items resolved to L2 (ProductId required)
- Prices loaded from price list
- Ready for costing calculation

---

### 12.4 Feeder Master Application Example

#### Scenario: Create Feeder from Feeder Master Template

**Step 1: Create Feeder Master (if not exists)**
```
Navigate: Master Data → Master BOM → Create

Fields:
- Name: "Standard Motor Feeder"
- UniqueNo: "FEEDER-MOTOR-001"
- TemplateType: FEEDER
- DefaultFeederName: "Motor Feeder 1"
- IsActive: 1
- Save

Add Items:
- MCCB 63A (L0)
- Contactor 25A (L1)
- Overload Relay (L0)
- Pushbutton Set (L0)
```

**Step 2: Apply Feeder Master to Quotation**
```
In Quotation V2 Panel Screen:
1. Click "Add Feeder from Template"
2. System shows list of Feeder Masters
3. Select: "Standard Motor Feeder"
4. System creates:
   - New Feeder (QuotationSaleBom, Level=0)
   - FeederName: "Motor Feeder 1" (from DefaultFeederName)
   - OriginMasterBomId: [Feeder Master ID]
   - Items copied from Feeder Master (L0/L1)
```

**Step 3: Resolve Feeder Items**
```
User resolves each item:
- MCCB 63A (L0) → Map to Product → "Acti9 iC60N 63A" (L2)
- Contactor 25A (L1) → Already has spec → Map to Product → "Schneider LC1D25" (L2)
- Overload Relay (L0) → Map to Product → "Schneider LRE35" (L2)
- Pushbutton Set (L0) → Map to Product → "Schneider XB2B" (L2)
```

**Result:**
- Feeder created from template
- All items resolved to L2
- Prices loaded
- Ready for costing

---

### 12.5 Proposal BOM Reuse Example

#### Scenario: Reuse Successful BOM from Past Quotation

**Step 1: Browse Past Quotations**
```
Navigate: Quotation V2 → Browse Past Quotations

Filter:
- Client: "ABC Industries"
- Date Range: Last 6 months
- Status: Completed/Approved

Results:
- Quotation #Q-2025-001: Distribution Panel for ABC Industries
  - Panel: Main Distribution Panel
    - Feeder 1: Motor Control
    - Feeder 2: Lighting
    - BOM: Standard Components
```

**Step 2: Select and Copy Proposal BOM**
```
1. Select: "Standard Components" BOM from Quotation #Q-2025-001
2. Click "Copy to New Quotation"
3. System copies:
   - BOM structure (QuotationSaleBom)
   - All items (QuotationSaleBomItem)
   - ProductId, Quantities, Rates
4. System creates new BOM in current quotation
```

**Step 3: Modify as Needed**
```
User can modify:
- Quantities (adjust for new requirements)
- Products (replace with different products)
- Prices (refresh from current price list)
- Add/remove items
```

**Result:**
- BOM copied from successful quotation
- User modified for new requirements
- Ready for new quotation

---

## 13. Visual Diagrams & Data Flow

### 13.1 Complete Item Master Hierarchy Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ITEM MASTER SYSTEM                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│  Category    │ (Required)
│  - Name      │
└──────┬───────┘
       │
       ├─────────────────┐
       │                   │
┌──────▼───────┐    ┌──────▼───────┐
│ SubCategory  │    │    Item      │ (ProductType)
│ - Name       │    │  - Name      │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └───────────┬───────┘
                   │
         ┌─────────▼─────────┐
         │   Generic Product  │ (ProductType = 1)
         │   - Name           │
         │   - GenericId: NULL│
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │   Make (Optional)  │
         │   - Name           │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │  Series (Optional)  │
         │   - Name             │
         └─────────┬───────────┘
                   │
         ┌─────────▼───────────┐
         │  Specific Product   │ (ProductType = 2)
         │   - Name             │
         │   - GenericId: → Generic│
         │   - MakeId: → Make  │
         │   - SeriesId: → Series│
         │   - SKU              │
         └─────────┬───────────┘
                   │
         ┌─────────▼───────────┐
         │      Price List      │
         │   - Rate             │
         │   - EffectiveDate    │
         └──────────────────────┘
```

---

### 13.2 Resolution Level Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              RESOLUTION LEVEL CONVERSION FLOW               │
└─────────────────────────────────────────────────────────────┘

MASTER BOM (Template)
┌─────────────────────┐
│  L0: Generic         │  ┌──────────────────────┐
│  - GenericDescriptor │  │  L1: Specification  │
│  - ProductId: NULL  │  │  - DefinedSpecJson   │
│  - Not Priceable     │  │  - ProductId: NULL  │
└─────────────────────┘  │  - Not Priceable     │
         │                └──────────────────────┘
         │                         │
         │                         │
         └─────────────┬───────────┘
                       │
         [User applies Master BOM to Quotation]
                       │
                       ▼
         PROPOSAL BOM (Copied from Master)
         ┌─────────────────────┐
         │  L0: Generic         │  ┌──────────────────────┐
         │  - GenericDescriptor │  │  L1: Specification   │
         │  - ProductId: NULL  │  │  - DefinedSpecJson   │
         │  - Not Priceable     │  │  - ProductId: NULL   │
         └─────────────────────┘  │  - Not Priceable      │
                   │               └──────────────────────┘
                   │                         │
         [User resolves]            [User resolves]
                   │                         │
         L0 → L1: Add DefinedSpecJson       │
                   │                         │
                   └───────────┬─────────────┘
                               │
                   L1 → L2: Map to ProductId
                               │
                               ▼
         PRODUCTION BOM (Resolved)
         ┌─────────────────────┐
         │  L2: Resolved        │
         │  - ProductId: Required│
         │  - Rate: From Price   │
         │  - RateSource: PRICELIST│
         │  - Priceable         │
         └─────────────────────┘
```

---

### 13.3 Master BOM to Production BOM Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│         MASTER BOM → PRODUCTION BOM DATA FLOW              │
└─────────────────────────────────────────────────────────────┘

STEP 1: Master BOM (Template)
┌──────────────────────────────┐
│ master_boms                   │
│ - MasterBomId: 100            │
│ - Name: "Standard Panel"       │
│ - TemplateType: PANEL          │
└──────────────┬────────────────┘
               │
               │ hasMany
               ▼
┌──────────────────────────────┐
│ master_bom_items              │
│ - MasterBomItemId: 1          │
│ - MasterBomId: 100            │
│ - ResolutionStatus: L0        │
│ - GenericDescriptor: "MCCB"    │
│ - ProductId: NULL             │
│ - Quantity: 12               │
└──────────────────────────────┘

                    │
                    │ [User applies to Quotation]
                    ▼

STEP 2: Proposal BOM (Copied)
┌──────────────────────────────┐
│ quotation_sale_boms           │
│ - QuotationSaleBomId: 500     │
│ - MasterBomId: 100 (reference)│
│ - OriginMasterBomId: 100      │
│ - BomName: "Standard Panel"   │
└──────────────┬────────────────┘
               │
               │ hasMany
               ▼
┌──────────────────────────────┐
│ quotation_sale_bom_items      │
│ - QuotationSaleBomItemId: 1000│
│ - QuotationSaleBomId: 500     │
│ - ResolutionStatus: L0        │
│ - GenericDescriptor: "MCCB"   │
│ - ProductId: NULL            │
│ - Qty: 12                    │
└──────────────────────────────┘

                    │
                    │ [User resolves: L0 → L2]
                    ▼

STEP 3: Production BOM (Resolved)
┌──────────────────────────────┐
│ quotation_sale_bom_items      │
│ - QuotationSaleBomItemId: 1000│
│ - QuotationSaleBomId: 500     │
│ - ProductId: 2001 (required)  │
│ - Qty: 12                     │
│ - Rate: 2500.00 (from prices)│
│ - RateSource: PRICELIST       │
│ - IsPriceMissing: 0           │
│ - Amount: 30000.00            │
└──────────────────────────────┘
```

---

### 13.4 Pricing Integration Flow

```
┌─────────────────────────────────────────────────────────────┐
│              PRICING INTEGRATION FLOW                        │
└─────────────────────────────────────────────────────────────┘

PRODUCT SELECTION
┌─────────────────┐
│  ProductId: 2001│
│  Name: "Acti9..."│
└────────┬────────┘
         │
         │ Lookup
         ▼
┌─────────────────┐
│  prices table    │
│  - ProductId: 2001│
│  - Rate: 2500.00 │
│  - EffectiveDate:│
│    2025-01-01    │
│  - Status: 0     │
└────────┬────────┘
         │
         │ Filter: EffectiveDate <= today
         │ Order: EffectiveDate DESC
         │ Limit: 1
         ▼
┌─────────────────┐
│  Latest Price    │
│  Rate: 2500.00   │
└────────┬────────┘
         │
         │ Assign to BOM Item
         ▼
┌──────────────────────────────┐
│ quotation_sale_bom_items      │
│ - ProductId: 2001            │
│ - Rate: 2500.00              │
│ - RateSource: PRICELIST      │
│ - IsPriceMissing: 0          │
│ - Discount: 0                │
│ - NetRate: 2500.00           │
│ - Amount: 2500.00 × Qty      │
└──────────────────────────────┘

IF PRICE NOT FOUND:
┌──────────────────────────────┐
│ quotation_sale_bom_items      │
│ - ProductId: 2001            │
│ - Rate: 0                     │
│ - RateSource: UNRESOLVED      │
│ - IsPriceMissing: 1           │
│ - NetRate: 0                  │
│ - Amount: 0                   │
└──────────────────────────────┘
```

---

## 14. Step-by-Step Workflows

### 14.1 Complete Product Setup Workflow

#### Workflow: Setup Complete Product Catalog Entry

**Prerequisites:**
- Category exists
- SubCategory exists (optional)
- Item/ProductType exists (optional)

**Steps:**

1. **Create Generic Product**
   ```
   Navigation: Master Data → Generic Product Master → Create
   
   Form Fields:
   - Category: [Select from dropdown]
   - SubCategory: [Select from dropdown, optional]
   - Item: [Select from dropdown, optional]
   - Name: [Enter product name]
   - Description: [Enter description, optional]
   - SKU: [Enter SKU, optional]
   - UOM: [Select unit of measure]
   - ProductType: 1 (Generic) [Auto-set]
   
   Actions:
   - Click "Save"
   - System creates Generic Product
   - ProductId assigned
   ```

2. **Assign Attributes**
   ```
   Navigation: Master Data → Product Attributes → [Select Product]
   
   Actions:
   - System shows applicable attributes (based on Category/SubCategory/Item)
   - Enter attribute values:
     * Voltage: 415V
     * Current Rating: 100A
     * Breaking Capacity: 25kA
   - Click "Save"
   ```

3. **Create Make & Series (if needed)**
   ```
   Navigation: Master Data → Make → Create
   - Name: "Schneider Electric"
   - Save
   
   Navigation: Master Data → Series → Create
   - Name: "Acti9"
   - Save
   ```

4. **Create Specific Product**
   ```
   Navigation: Master Data → Specific Product Master → Create
   
   Form Fields:
   - Category: [Select same as Generic]
   - SubCategory: [Select same as Generic, optional]
   - Item: [Select same as Generic, optional]
   - GenericId: [Select Generic Product created in Step 1]
   - MakeId: [Select Make, optional]
   - SeriesId: [Select Series, optional]
   - Name: [Enter specific product name]
   - SKU: [Enter SKU, recommended]
   - Description: [Enter description]
   - ProductType: 2 (Specific) [Auto-set]
   
   Actions:
   - Click "Save"
   - System creates Specific Product
   - GenericId links to Generic Product
   ```

5. **Add Price**
   ```
   Navigation: Master Data → Price List → Create
   
   Form Fields:
   - ProductId: [Select Specific Product]
   - Rate: [Enter rate, decimal]
   - EffectiveDate: [Select date]
   
   Actions:
   - Click "Save"
   - System creates price entry
   - Product ready for use in quotations
   ```

**Completion:**
- Generic Product created
- Specific Product created
- Attributes assigned
- Price added
- Product ready for quotations

---

### 14.2 Master BOM Creation Workflow

#### Workflow: Create Reusable Master BOM Template

**Steps:**

1. **Create Master BOM Header**
   ```
   Navigation: Master Data → Master BOM → Create
   
   Form Fields:
   - Name: [Enter BOM name]
   - UniqueNo: [Enter unique number]
   - Description: [Enter description, optional]
   - TemplateType: [Select: FEEDER, PANEL, or GENERIC]
   - DefaultFeederName: [Enter default name, optional]
   - IsActive: 1 [Default]
   
   Actions:
   - Click "Save"
   - System creates Master BOM header
   - MasterBomId assigned
   ```

2. **Add Master BOM Items**
   ```
   Navigation: Master Data → Master BOM → Edit → [Select BOM]
   
   For Each Item:
   
   Option A: L0 Item (Generic Placeholder)
   - ResolutionStatus: L0
   - GenericDescriptor: [Enter text description]
   - Quantity: [Enter quantity]
   - UOM: [Select unit of measure]
   - ProductId: [Hidden/Disabled - not allowed]
   
   Option B: L1 Item (Defined Specification)
   - ResolutionStatus: L1
   - DefinedSpecJson: [Enter JSON specification]
     Example:
     {
       "Voltage": "415V",
       "Current": "100A",
       "Breaking": "25kA"
     }
   - Quantity: [Enter quantity]
   - UOM: [Select unit of measure]
   - ProductId: [Hidden/Disabled - not allowed]
   
   Actions:
   - Click "Add Item" for each item
   - Click "Save" after all items added
   ```

3. **Validate Master BOM**
   ```
   System Validation:
   - ResolutionStatus must be L0 or L1
   - ProductId must be NULL (enforced by guardrail)
   - L1 items must have DefinedSpecJson
   - L0 items should have GenericDescriptor (warning if missing)
   ```

**Completion:**
- Master BOM created
- Items added (L0/L1 only)
- No ProductId (not allowed)
- No pricing (not priceable)
- Ready to use as template

---

### 14.3 Apply Master BOM to Quotation Workflow

#### Workflow: Use Master BOM Template in Quotation

**Prerequisites:**
- Quotation exists
- Panel exists in quotation
- Master BOM exists (L0/L1 items)

**Steps:**

1. **Select Master BOM**
   ```
   Navigation: Quotation V2 → Panel → [Select Panel]
   
   Actions:
   - Click "Add BOM from Template"
   - System shows list of Master BOMs
   - Select Master BOM
   - Click "Apply"
   ```

2. **System Creates Proposal BOM**
   ```
   System Actions (Automatic):
   - Creates QuotationSaleBom record
   - Sets MasterBomId (reference only)
   - Sets OriginMasterBomId (tracks source)
   - Copies all MasterBomItems to QuotationSaleBomItems
   - Maintains ResolutionStatus (L0/L1)
   - ProductId remains NULL
   ```

3. **Resolve Items (User Action)**
   ```
   For Each Item:
   
   If L0 (Generic Placeholder):
   - Option 1: Define Specification (L0 → L1)
     * Click "Define Specification"
     * Enter DefinedSpecJson
     * Save
   
   - Option 2: Map to Product (L0 → L2)
     * Click "Map to Product"
     * Search products (Category → SubCategory → Item)
     * Select ProductId
     * System updates:
       - ProductId assigned
       - ResolutionStatus = L2 (implicit)
       - Rate loaded from prices table
       - RateSource = PRICELIST (or UNRESOLVED)
   
   If L1 (Defined Specification):
   - Click "Map to Product"
   - System filters products matching DefinedSpecJson
   - Select ProductId
   - System updates:
     - ProductId assigned
     - ResolutionStatus = L2 (implicit)
     - Rate loaded from prices table
     - RateSource = PRICELIST (or UNRESOLVED)
   ```

4. **Verify Resolution**
   ```
   System Checks:
   - All items have ProductId (L2)
   - All items have Rate (or IsPriceMissing=1)
   - All items ready for costing
   ```

**Completion:**
- Proposal BOM created from Master BOM
- All items resolved to L2
- Prices loaded
- Ready for costing calculation

---

## 15. Troubleshooting Guide

### 15.1 Common Issues & Solutions

#### Issue 1: Product Not Found in Price List

**Symptoms:**
- ProductId exists in BOM item
- Rate = 0
- RateSource = UNRESOLVED
- IsPriceMissing = 1

**Causes:**
- Price not added to prices table
- EffectiveDate is in future
- Price Status = 1 (deleted)

**Solutions:**
1. **Add Price:**
   ```
   Navigation: Master Data → Price List → Create
   - ProductId: [Select product]
   - Rate: [Enter rate]
   - EffectiveDate: [Select date <= today]
   - Status: 0 (Active)
   - Save
   ```

2. **Check EffectiveDate:**
   ```
   Query: SELECT * FROM prices 
   WHERE ProductId = ? 
   AND EffectiveDate <= CURDATE() 
   AND Status = 0
   ORDER BY EffectiveDate DESC
   ```

3. **Reactivate Price:**
   ```
   If price exists but Status = 1:
   - Update Status = 0
   - Or create new price row
   ```

---

#### Issue 2: Master BOM Item Has ProductId (Should Be NULL)

**Symptoms:**
- Master BOM item shows ProductId
- Validation error when saving
- Error: "Master BOM items with ResolutionStatus L0/L1 cannot have ProductId"

**Causes:**
- User tried to set ProductId manually
- Data corruption
- Guardrail not working

**Solutions:**
1. **Check ResolutionStatus:**
   ```
   If ResolutionStatus = L0 or L1:
   - ProductId must be NULL
   - Clear ProductId field
   ```

2. **Verify Guardrail:**
   ```
   Model: MasterBomItem
   Boot hook should force ProductId = NULL for L0/L1
   ```

3. **Fix Data:**
   ```
   UPDATE master_bom_items
   SET ProductId = NULL
   WHERE ResolutionStatus IN ('L0', 'L1')
   AND ProductId IS NOT NULL
   ```

---

#### Issue 3: Cannot Resolve L0 Item to L2

**Symptoms:**
- L0 item in Proposal BOM
- "Map to Product" button not working
- No products found in search

**Causes:**
- No products exist for Category/SubCategory/Item
- Products not created yet
- Search filters too restrictive

**Solutions:**
1. **Create Products:**
   ```
   Follow Product Creation Workflow
   - Create Generic Product
   - Create Specific Product
   - Add Price
   ```

2. **Check Product Filters:**
   ```
   Verify:
   - Category matches
   - SubCategory matches (if used)
   - Item matches (if used)
   - Product Status = 0 (Active)
   ```

3. **Broaden Search:**
   ```
   Try searching without SubCategory/Item filters
   - Search by Category only
   - Then filter manually
   ```

---

#### Issue 4: Price Not Updating After Price List Change

**Symptoms:**
- Price list updated
- BOM items still show old rate
- RateSource = PRICELIST

**Causes:**
- RateSource = MANUAL_WITH_DISCOUNT or FIXED_NO_DISCOUNT (manual override)
- EffectiveDate not updated
- Cache not cleared

**Solutions:**
1. **Check RateSource:**
   ```
   If RateSource = PRICELIST:
   - System should auto-update
   - Check if new price EffectiveDate <= today
   ```

2. **Refresh Prices:**
   ```
   Navigation: Quotation V2 → Panel → [Select Panel]
   - Click "Refresh Prices from Price List"
   - System updates all PRICELIST items
   ```

3. **Clear Cache:**
   ```
   If using cache:
   - Clear cache
   - Reload quotation
   ```

---

#### Issue 5: Generic Product Has No Specific Products

**Symptoms:**
- Generic Product exists (ProductType = 1)
- No Specific Products linked
- Cannot select in BOM (only Generic available)

**Causes:**
- Specific Products not created
- GenericId not set in Specific Products
- Specific Products Status = 1 (deleted)

**Solutions:**
1. **Create Specific Products:**
   ```
   Follow Product Creation Workflow
   - Create Specific Product
   - Set GenericId to Generic Product
   - Add Make/Series (optional)
   - Add Price
   ```

2. **Check GenericId:**
   ```
   Verify Specific Products have correct GenericId:
   SELECT * FROM products
   WHERE GenericId = [Generic ProductId]
   AND ProductType = 2
   AND Status = 0
   ```

3. **Reactivate Specific Products:**
   ```
   If Status = 1:
   - Update Status = 0
   - Or create new Specific Products
   ```

---

### 15.2 Data Validation Queries

#### Query 1: Find Master BOM Items with ProductId (Should Be NULL)
```sql
SELECT 
    mbi.MasterBomItemId,
    mbi.MasterBomId,
    mb.Name AS BomName,
    mbi.ResolutionStatus,
    mbi.ProductId,
    mbi.GenericDescriptor,
    mbi.DefinedSpecJson
FROM master_bom_items mbi
JOIN master_boms mb ON mbi.MasterBomId = mb.MasterBomId
WHERE mbi.ResolutionStatus IN ('L0', 'L1')
AND mbi.ProductId IS NOT NULL;
```

#### Query 2: Find Production BOM Items Without ProductId (Should Have ProductId)
```sql
SELECT 
    qsbi.QuotationSaleBomItemId,
    qsbi.QuotationSaleBomId,
    qsb.BomName,
    qsbi.ProductId,
    qsbi.Rate,
    qsbi.RateSource,
    qsbi.IsPriceMissing
FROM quotation_sale_bom_items qsbi
JOIN quotation_sale_boms qsb ON qsbi.QuotationSaleBomId = qsb.QuotationSaleBomId
WHERE qsbi.Status = 0
AND qsbi.ProductId IS NULL;
```

#### Query 3: Find Products Without Prices
```sql
SELECT 
    p.ProductId,
    p.Name,
    p.ProductType,
    p.CategoryId,
    c.Name AS CategoryName
FROM products p
LEFT JOIN categories c ON p.CategoryId = c.CategoryId
LEFT JOIN prices pr ON p.ProductId = pr.ProductId 
    AND pr.EffectiveDate <= CURDATE() 
    AND pr.Status = 0
WHERE p.Status = 0
AND p.ProductType = 2  -- Specific products only
AND pr.PriceId IS NULL;
```

#### Query 4: Find BOM Items with Missing Prices
```sql
SELECT 
    qsbi.QuotationSaleBomItemId,
    qsbi.ProductId,
    p.Name AS ProductName,
    qsbi.Rate,
    qsbi.RateSource,
    qsbi.IsPriceMissing
FROM quotation_sale_bom_items qsbi
LEFT JOIN products p ON qsbi.ProductId = p.ProductId
WHERE qsbi.Status = 0
AND qsbi.ProductId IS NOT NULL
AND (qsbi.IsPriceMissing = 1 OR qsbi.Rate = 0);
```

---

## 16. Code Examples

### 16.1 Product Creation Code Example

```php
// Create Generic Product
$genericProduct = Product::create([
    'CategoryId' => 1,  // Protection Devices
    'SubCategoryId' => 5,  // Circuit Breakers
    'ItemId' => 10,  // MCCB Feeder
    'Name' => 'MCCB 100A Standard',
    'ProductType' => 1,  // Generic
    'Description' => 'Standard MCCB 100A',
    'UOM' => 'Pcs',
    'Status' => 0
]);

// Create Specific Product
$specificProduct = Product::create([
    'CategoryId' => 1,
    'SubCategoryId' => 5,
    'ItemId' => 10,
    'GenericId' => $genericProduct->ProductId,  // Link to Generic
    'MakeId' => 50,  // Schneider Electric
    'SeriesId' => 25,  // Acti9
    'Name' => 'Acti9 iC60N 100A',
    'SKU' => 'A9N61616',
    'ProductType' => 2,  // Specific
    'Description' => 'Schneider Acti9 iC60N 100A MCCB',
    'UOM' => 'Pcs',
    'Status' => 0
]);

// Add Price
Price::create([
    'ProductId' => $specificProduct->ProductId,
    'Rate' => 2500.00,
    'EffectiveDate' => '2025-01-01',
    'Status' => 0
]);
```

---

### 16.2 Master BOM Creation Code Example

```php
// Create Master BOM Header
$masterBom = MasterBom::create([
    'Name' => 'Standard Distribution Panel Components',
    'UniqueNo' => 'DP-STD-001',
    'Description' => 'Standard components for distribution panel',
    'TemplateType' => 'PANEL',
    'DefaultFeederName' => 'Feeder 1',
    'IsActive' => 1
]);

// Add L0 Item (Generic Placeholder)
MasterBomItem::create([
    'MasterBomId' => $masterBom->MasterBomId,
    'ResolutionStatus' => 'L0',
    'GenericDescriptor' => 'MCCB 100A',
    'ProductId' => null,  // Not allowed for L0/L1
    'Quantity' => 12,
    'UOM' => 'Pcs'
]);

// Add L1 Item (Defined Specification)
MasterBomItem::create([
    'MasterBomId' => $masterBom->MasterBomId,
    'ResolutionStatus' => 'L1',
    'DefinedSpecJson' => [
        'Voltage' => '415V',
        'Current' => '25A',
        'Type' => '3-Pole',
        'Coil' => '230V AC'
    ],
    'ProductId' => null,  // Not allowed for L0/L1
    'Quantity' => 6,
    'UOM' => 'Pcs'
]);
```

---

### 16.3 Apply Master BOM to Quotation Code Example

```php
// Apply Master BOM to Quotation
public function applyMasterBom($quotationSaleId, $masterBomId)
{
    $masterBom = MasterBom::with('masterbomitem')->findOrFail($masterBomId);
    $panel = QuotationSale::findOrFail($quotationSaleId);
    
    // Create Proposal BOM (copied from Master)
    $proposalBom = QuotationSaleBom::create([
        'QuotationSaleId' => $quotationSaleId,
        'QuotationId' => $panel->QuotationId,
        'MasterBomId' => $masterBomId,  // Reference only
        'OriginMasterBomId' => $masterBomId,  // Track source
        'BomName' => $masterBom->Name,
        'Level' => 1,  // BOM level
        'ParentBomId' => null,
        'Qty' => 1,
        'Status' => 0
    ]);
    
    // Copy items from Master BOM
    foreach ($masterBom->masterbomitem as $masterItem) {
        QuotationSaleBomItem::create([
            'QuotationSaleId' => $quotationSaleId,
            'QuotationId' => $panel->QuotationId,
            'QuotationSaleBomId' => $proposalBom->QuotationSaleBomId,
            'ProductId' => null,  // L0/L1 items don't have ProductId
            'Qty' => $masterItem->Quantity,
            'Rate' => 0,  // Not priceable yet
            'RateSource' => 'UNRESOLVED',
            'IsPriceMissing' => 1,
            'Status' => 0
        ]);
    }
    
    return $proposalBom;
}
```

---

### 16.4 Resolve Item to L2 Code Example

```php
// Resolve L0/L1 Item to L2 (Map to Product)
public function resolveItem($itemId, $productId)
{
    $item = QuotationSaleBomItem::findOrFail($itemId);
    
    // Validate ProductId exists
    $product = Product::findOrFail($productId);
    
    // Update item
    $item->ProductId = $productId;
    $item->Status = 0;
    
    // Lookup price
    $price = Price::where('ProductId', $productId)
        ->where('EffectiveDate', '<=', now())
        ->where('Status', 0)
        ->orderBy('EffectiveDate', 'DESC')
        ->first();
    
    if ($price) {
        $item->Rate = $price->Rate;
        $item->RateSource = QuotationSaleBomItem::RATE_SOURCE_PRICELIST;
        $item->IsPriceMissing = 0;
    } else {
        $item->Rate = 0;
        $item->RateSource = QuotationSaleBomItem::RATE_SOURCE_UNRESOLVED;
        $item->IsPriceMissing = 1;
    }
    
    // Calculate NetRate and Amount
    $item->NetRate = $item->Rate;  // No discount initially
    // Amount will be calculated by QuotationQuantityService × NetRate
    
    $item->save();
    
    return $item;
}
```

---

## 17. Code File Mapping & Matrix

### 17.1 Purpose

This section maps database tables, features, and work items to their corresponding code files. This matrix helps understand:
- Which code files handle which database tables
- Which controllers manage which features
- Which services contain business logic
- Relationships between code files and work items

**Use Case:** Create final matrix of code files and their relationships with other work.

---

### 17.2 Database Table to Model Mapping

#### Item Master Tables

| Database Table | Model File | Primary Key | Key Relationships |
|----------------|------------|-------------|-------------------|
| `categories` | `app/Models/Category.php` | `CategoryId` | hasMany SubCategories, Items, Products |
| `sub_categories` | `app/Models/SubCategory.php` | `SubCategoryId` | belongsTo Category, hasMany Items, Products |
| `items` | `app/Models/Item.php` | `ItemId` | belongsTo Category, SubCategory, hasMany Products |
| `products` | `app/Models/Product.php` | `ProductId` | belongsTo Category, SubCategory, Item, Make, Series, Generic |
| `makes` | `app/Models/Make.php` | `MakeId` | hasMany Products |
| `series` | `app/Models/Series.php` | `SeriesId` | hasMany Products |
| `prices` | `app/Models/Price.php` | `PriceId` | belongsTo Product |
| `attributes` | `app/Models/Attribute.php` | `AttributeId` | belongsToMany Products |
| `category_attributes` | `app/Models/CategoryAttribute.php` | `CategoryAttributeId` | belongsTo Category, Attribute |
| `product_attributes` | `app/Models/ProductAttribute.php` | `ProductAttributeId` | belongsTo Product, Attribute |

#### Master BOM Tables

| Database Table | Model File | Primary Key | Key Relationships |
|----------------|------------|-------------|-------------------|
| `master_boms` | `app/Models/MasterBom.php` | `MasterBomId` | hasMany MasterBomItems |
| `master_bom_items` | `app/Models/MasterBomItem.php` | `MasterBomItemId` | belongsTo MasterBom, Product (nullable) |

#### Quotation Tables

| Database Table | Model File | Primary Key | Key Relationships |
|----------------|------------|-------------|-------------------|
| `quotations` | `app/Models/Quotation.php` | `QuotationId` | hasMany QuotationSales, QuotationDiscounts |
| `quotation_sales` | `app/Models/QuotationSale.php` | `QuotationSaleId` | belongsTo Quotation, hasMany QuotationSaleBoms |
| `quotation_sale_boms` | `app/Models/QuotationSaleBom.php` | `QuotationSaleBomId` | belongsTo QuotationSale, MasterBom, hasMany QuotationSaleBomItems |
| `quotation_sale_bom_items` | `app/Models/QuotationSaleBomItem.php` | `QuotationSaleBomItemId` | belongsTo QuotationSaleBom, Product, Make, Series |
| `quotation_make_series` | `app/Models/QuotationMakeSeries.php` | `QuotationMakeSeriesId` | belongsTo Quotation, Category, Make, Series |
| `quotation_discounts` | `app/Models/QuotationDiscount.php` | `QuotationDiscountId` | belongsTo Quotation |
| `quotation_discount_rules` | `app/Models/QuotationDiscountRule.php` | `QuotationDiscountRuleId` | hasMany DiscountRuleApplySnapshots |

#### Audit & Logging Tables

| Database Table | Model File | Primary Key | Purpose |
|----------------|------------|-------------|---------|
| `pricing_audit_logs` | `app/Models/PricingAuditLog.php` | `PricingAuditLogId` | Tracks price changes |
| `discount_rule_apply_audit_logs` | `app/Models/DiscountRuleApplyAuditLog.php` | `AuditLogId` | Tracks discount rule applications |
| `discount_rule_apply_snapshots` | `app/Models/DiscountRuleApplySnapshot.php` | `SnapshotId` | Stores discount rule snapshots |

---

### 17.3 Feature to Controller Mapping

#### Item Master Features

| Feature/Work Item | Controller File | Key Methods | Related Models |
|-------------------|-----------------|-------------|----------------|
| **Category Management** | `app/Http/Controllers/CategoryController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Category |
| **SubCategory Management** | `app/Http/Controllers/SubCategoryController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | SubCategory |
| **Item/ProductType Management** | `app/Http/Controllers/ItemController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Item |
| **Generic Product Management** | `app/Http/Controllers/GenericController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Product (ProductType=1) |
| **Specific Product Management** | `app/Http/Controllers/ProductController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Product (ProductType=2) |
| **Make Management** | `app/Http/Controllers/MakeController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Make |
| **Series Management** | `app/Http/Controllers/SeriesController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Series |
| **Price List Management** | `app/Http/Controllers/PriceController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Price, Product |
| **Attribute Management** | `app/Http/Controllers/AttributeController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Attribute |
| **Category Attribute Mapping** | `app/Http/Controllers/CategoryAttributeController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | CategoryAttribute |
| **Product Attribute Values** | `app/Http/Controllers/ProductAttributeController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | ProductAttribute |

#### Master BOM Features

| Feature/Work Item | Controller File | Key Methods | Related Models |
|-------------------|-----------------|-------------|----------------|
| **Master BOM Management** | `app/Http/Controllers/MasterBomController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()`, `copy()` | MasterBom, MasterBomItem |
| **Feeder Template Management** | `app/Http/Controllers/FeederTemplateController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | MasterBom (TemplateType=FEEDER) |
| **Proposal BOM Management** | `app/Http/Controllers/ProposalBomController.php` | `index()`, `browse()`, `copy()`, `apply()` | QuotationSaleBom, MasterBom |

#### Quotation V2 Features

| Feature/Work Item | Controller File | Key Methods | Related Models |
|-------------------|-----------------|-------------|----------------|
| **Quotation V2 Main** | `app/Http/Controllers/QuotationV2Controller.php` | `index()`, `panel()`, `addPanel()`, `addFeeder()`, `addBom()`, `addItem()`, `updateItemQty()`, `updateItemRate()`, `deleteItem()`, `getBomChildren()`, `getCosting()`, `export()` | Quotation, QuotationSale, QuotationSaleBom, QuotationSaleBomItem |
| **Quotation Legacy** | `app/Http/Controllers/QuotationController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()`, `step()` | Quotation, QuotationSale, QuotationSaleBom, QuotationSaleBomItem |
| **Quotation Discount Rules** | `app/Http/Controllers/QuotationDiscountRuleController.php` | `index()`, `create()`, `store()`, `edit()`, `update()`, `destroy()`, `test()` | QuotationDiscountRule |
| **Quotation Discount Rule Testing** | `app/Http/Controllers/QuotationDiscountRuleTestController.php` | `test()`, `apply()` | QuotationDiscountRule, QuotationSaleBomItem |

#### Catalog & Maintenance Features

| Feature/Work Item | Controller File | Key Methods | Related Models |
|-------------------|-----------------|-------------|----------------|
| **Catalog Health Check** | `app/Http/Controllers/CatalogHealthController.php` | `index()`, `check()`, `report()` | Product, Price, Category, SubCategory, Item |
| **Catalog Cleanup** | `app/Http/Controllers/CatalogCleanupController.php` | `index()`, `cleanup()`, `archive()` | Product, Price, MasterBom |
| **Reuse Past Quotations** | `app/Http/Controllers/ReuseController.php` | `index()`, `browse()`, `copy()` | Quotation, QuotationSale, QuotationSaleBom |

---

### 17.4 Business Logic to Service Mapping

| Business Logic/Feature | Service File | Key Methods | Related Models |
|------------------------|--------------|-------------|----------------|
| **Quantity Calculations** | `app/Services/QuotationQuantityService.php` | `calculate()`, `getEffectiveQtyPerPanel()`, `getTotalQty()` | QuotationSaleBomItem, QuotationSaleBom, QuotationSale |
| **Costing Calculations** | `app/Services/CostingService.php` | `componentCost()`, `bomCost()`, `feederCost()`, `panelCost()`, `quotationCost()` | QuotationSaleBomItem, QuotationSaleBom, QuotationSale, Quotation |
| **Deletion Policy** | `app/Services/DeletionPolicyService.php` | `canDelete()`, `validateDeletion()`, `getDependencies()` | All Models |
| **Discount Rule Application** | `app/Services/DiscountRuleApplyService.php` | `applyRules()`, `calculateDiscount()`, `getApplicableRules()` | QuotationDiscountRule, QuotationSaleBomItem |
| **Product Attribute Management** | `app/Services/ProductAttributeService.php` | `getApplicableAttributes()`, `syncAttributes()`, `validateAttributes()` | Product, CategoryAttribute, ProductAttribute |
| **Auto Naming** | `app/Services/AutoNamingService.php` | `generateName()`, `suggestName()` | Product, QuotationSaleBom |
| **Quotation Discount Rule Logic** | `app/Services/QuotationDiscountRuleService.php` | `evaluate()`, `match()`, `calculate()` | QuotationDiscountRule |

---

### 17.5 UI View to Controller Mapping

#### Item Master Views

| View File | Controller | Purpose |
|-----------|------------|---------|
| `resources/views/category/index.blade.php` | CategoryController | List categories |
| `resources/views/category/create.blade.php` | CategoryController | Create category form |
| `resources/views/category/edit.blade.php` | CategoryController | Edit category form |
| `resources/views/subcategory/index.blade.php` | SubCategoryController | List subcategories |
| `resources/views/item/index.blade.php` | ItemController | List items/product types |
| `resources/views/generic/index.blade.php` | GenericController | List generic products |
| `resources/views/generic/create.blade.php` | GenericController | Create generic product form |
| `resources/views/generic/edit.blade.php` | GenericController | Edit generic product form |
| `resources/views/product/index.blade.php` | ProductController | List specific products |
| `resources/views/product/create.blade.php` | ProductController | Create specific product form |
| `resources/views/product/edit.blade.php` | ProductController | Edit specific product form |
| `resources/views/price/index.blade.php` | PriceController | List prices |
| `resources/views/price/create.blade.php` | PriceController | Create price form |

#### Master BOM Views

| View File | Controller | Purpose |
|-----------|------------|---------|
| `resources/views/masterbom/index.blade.php` | MasterBomController | List master BOMs |
| `resources/views/masterbom/create.blade.php` | MasterBomController | Create master BOM form |
| `resources/views/masterbom/edit.blade.php` | MasterBomController | Edit master BOM form |

#### Quotation V2 Views

| View File | Controller | Purpose |
|-----------|------------|---------|
| `resources/views/quotation/v2/index.blade.php` | QuotationV2Controller | List panels for quotation |
| `resources/views/quotation/v2/panel.blade.php` | QuotationV2Controller | Panel details with feeder/BOM tree |
| `resources/views/quotation/v2/_feeder.blade.php` | QuotationV2Controller | Feeder component (partial) |
| `resources/views/quotation/v2/_items_table.blade.php` | QuotationV2Controller | Items table component (partial) |
| `resources/views/quotation/v2/_reuse_filter_modal.blade.php` | ReuseController | Reuse past quotations modal |

---

### 17.6 Complete Work Item Matrix

#### Work Item: Product Master Management

| Component | Code File | Type | Purpose |
|-----------|-----------|------|---------|
| **Database** | `products` table | Table | Stores generic and specific products |
| **Model** | `app/Models/Product.php` | Model | Eloquent model for products |
| **Controller** | `app/Http/Controllers/GenericController.php` | Controller | Generic product CRUD (ProductType=1) |
| **Controller** | `app/Http/Controllers/ProductController.php` | Controller | Specific product CRUD (ProductType=2) |
| **Service** | `app/Services/ProductAttributeService.php` | Service | Product attribute management |
| **View** | `resources/views/generic/*.blade.php` | View | Generic product UI |
| **View** | `resources/views/product/*.blade.php` | View | Specific product UI |

#### Work Item: Master BOM Management

| Component | Code File | Type | Purpose |
|-----------|-----------|------|---------|
| **Database** | `master_boms` table | Table | Stores master BOM templates |
| **Database** | `master_bom_items` table | Table | Stores master BOM items (L0/L1) |
| **Model** | `app/Models/MasterBom.php` | Model | Eloquent model for master BOMs |
| **Model** | `app/Models/MasterBomItem.php` | Model | Eloquent model for master BOM items |
| **Controller** | `app/Http/Controllers/MasterBomController.php` | Controller | Master BOM CRUD operations |
| **View** | `resources/views/masterbom/*.blade.php` | View | Master BOM UI |

#### Work Item: Quotation V2 BOM Management

| Component | Code File | Type | Purpose |
|-----------|-----------|------|---------|
| **Database** | `quotation_sale_boms` table | Table | Stores quotation BOMs (feeders/BOMs) |
| **Database** | `quotation_sale_bom_items` table | Table | Stores BOM items (components, L2) |
| **Model** | `app/Models/QuotationSaleBom.php` | Model | Eloquent model for quotation BOMs |
| **Model** | `app/Models/QuotationSaleBomItem.php` | Model | Eloquent model for BOM items |
| **Controller** | `app/Http/Controllers/QuotationV2Controller.php` | Controller | Quotation V2 operations |
| **Service** | `app/Services/QuotationQuantityService.php` | Service | Quantity calculations |
| **Service** | `app/Services/CostingService.php` | Service | Costing calculations |
| **View** | `resources/views/quotation/v2/*.blade.php` | View | Quotation V2 UI |

#### Work Item: Pricing Management

| Component | Code File | Type | Purpose |
|-----------|-----------|------|---------|
| **Database** | `prices` table | Table | Stores product prices with effective dates |
| **Model** | `app/Models/Price.php` | Model | Eloquent model for prices |
| **Controller** | `app/Http/Controllers/PriceController.php` | Controller | Price CRUD operations |
| **Model** | `app/Models/PricingAuditLog.php` | Model | Tracks price changes |
| **View** | `resources/views/price/*.blade.php` | View | Price list UI |

#### Work Item: Quantity Calculation

| Component | Code File | Type | Purpose |
|-----------|-----------|------|---------|
| **Service** | `app/Services/QuotationQuantityService.php` | Service | Quantity calculation engine |
| **Formula** | `EffQtyPerPanel = FeederQty × BOMQty × ItemQty` | Rule | Protected formula |
| **Formula** | `TotalQty = PanelQty × EffQtyPerPanel` | Rule | Protected formula |
| **Model** | `app/Models/QuotationSaleBomItem.php` | Model | Stores item quantities |
| **Model** | `app/Models/QuotationSaleBom.php` | Model | Stores BOM quantities |
| **Model** | `app/Models/QuotationSale.php` | Model | Stores panel quantities |

#### Work Item: Costing Calculation

| Component | Code File | Type | Purpose |
|-----------|-----------|------|---------|
| **Service** | `app/Services/CostingService.php` | Service | Costing calculation engine |
| **DTO** | `app/Services/DTOs/ComponentCostDto.php` | DTO | Component cost data structure |
| **DTO** | `app/Services/DTOs/BomCostDto.php` | DTO | BOM cost data structure |
| **DTO** | `app/Services/DTOs/FeederCostDto.php` | DTO | Feeder cost data structure |
| **DTO** | `app/Services/DTOs/PanelCostDto.php` | DTO | Panel cost data structure |
| **Formula** | `Amount = NetRate × TotalQty` | Rule | Protected formula |
| **Formula** | `Roll-up = SUM(Amount)` | Rule | Protected formula (no multipliers) |

---

### 17.7 Code File Dependencies Matrix

#### QuotationV2Controller Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `QuotationQuantityService` | Service | Quantity calculations |
| `CostingService` | Service | Costing calculations |
| `DeletionPolicyService` | Service | Deletion validation |
| `Quotation` | Model | Quotation data |
| `QuotationSale` | Model | Panel data |
| `QuotationSaleBom` | Model | Feeder/BOM data |
| `QuotationSaleBomItem` | Model | Component data |
| `MasterBom` | Model | Master BOM templates |
| `Product` | Model | Product catalog |

#### CostingService Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `QuotationQuantityService` | Service | Get effective quantities |
| `QuotationSaleBomItem` | Model | Component data |
| `QuotationSaleBom` | Model | BOM data |
| `QuotationSale` | Model | Panel data |
| `Quotation` | Model | Quotation data |

#### QuotationQuantityService Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `QuotationSaleBomItem` | Model | Item quantities |
| `QuotationSaleBom` | Model | BOM quantities |
| `QuotationSale` | Model | Panel quantities |

#### MasterBomController Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `MasterBom` | Model | Master BOM data |
| `MasterBomItem` | Model | Master BOM items |
| `Product` | Model | Product catalog (for reference) |
| `Category` | Model | Category data |
| `SubCategory` | Model | SubCategory data |
| `Item` | Model | Item/ProductType data |

---

### 17.8 Protected Code Files

| Code File | Protection Level | Reason | Modification Policy |
|-----------|------------------|--------|---------------------|
| `app/Services/QuotationQuantityService.php` | 🔴 **PROTECTED** | Core quantity calculation engine | Requires explicit approval |
| `app/Services/CostingService.php` | 🔴 **PROTECTED** | Core costing calculation engine | Requires explicit approval |
| `app/Services/DeletionPolicyService.php` | 🔴 **PROTECTED** | Soft delete validation rules | Requires explicit approval |
| Database Schema (Status, Level, ParentBomId columns) | 🔴 **PROTECTED** | Critical for data integrity | Requires migration plan |

---

### 17.9 Route to Controller Mapping

#### Item Master Routes

| Route Pattern | Controller | Method | Purpose |
|---------------|------------|--------|---------|
| `GET /category` | CategoryController | `index()` | List categories |
| `GET /category/create` | CategoryController | `create()` | Show create form |
| `POST /category` | CategoryController | `store()` | Create category |
| `GET /category/{id}/edit` | CategoryController | `edit()` | Show edit form |
| `PUT /category/{id}` | CategoryController | `update()` | Update category |
| `DELETE /category/{id}` | CategoryController | `destroy()` | Delete category |
| `GET /generic` | GenericController | `index()` | List generic products |
| `GET /product` | ProductController | `index()` | List specific products |
| `GET /price` | PriceController | `index()` | List prices |

#### Master BOM Routes

| Route Pattern | Controller | Method | Purpose |
|---------------|------------|--------|---------|
| `GET /masterbom` | MasterBomController | `index()` | List master BOMs |
| `GET /masterbom/create` | MasterBomController | `create()` | Show create form |
| `POST /masterbom` | MasterBomController | `store()` | Create master BOM |
| `GET /masterbom/{id}/edit` | MasterBomController | `edit()` | Show edit form |
| `PUT /masterbom/{id}` | MasterBomController | `update()` | Update master BOM |
| `DELETE /masterbom/{id}` | MasterBomController | `destroy()` | Delete master BOM |
| `GET /masterbom/{id}/copy` | MasterBomController | `copy()` | Copy master BOM |

#### Quotation V2 Routes

| Route Pattern | Controller | Method | Purpose |
|---------------|------------|--------|---------|
| `GET /quotation/{id}/v2` | QuotationV2Controller | `index()` | List panels |
| `GET /quotation/{id}/panel/{panelId}` | QuotationV2Controller | `panel()` | Show panel details |
| `POST /quotation/{id}/panel` | QuotationV2Controller | `addPanel()` | Add panel |
| `POST /quotation/{id}/panel/{panelId}/feeder` | QuotationV2Controller | `addFeeder()` | Add feeder |
| `POST /quotation/{id}/panel/{panelId}/bom` | QuotationV2Controller | `addBom()` | Add BOM |
| `POST /quotation/{id}/panel/{panelId}/item` | QuotationV2Controller | `addItem()` | Add item |
| `PUT /quotation/item/{itemId}/qty` | QuotationV2Controller | `updateItemQty()` | Update item quantity |
| `PUT /quotation/item/{itemId}/rate` | QuotationV2Controller | `updateItemRate()` | Update item rate |
| `DELETE /quotation/item/{itemId}` | QuotationV2Controller | `deleteItem()` | Delete item |
| `GET /quotation/bom/{bomId}/children` | QuotationV2Controller | `getBomChildren()` | Get child BOMs |
| `GET /quotation/{id}/costing` | QuotationV2Controller | `getCosting()` | Get costing data |
| `GET /quotation/{id}/export` | QuotationV2Controller | `export()` | Export quotation |

---

### 17.10 Complete Code File Inventory

#### Models (app/Models/)

| Model File | Database Table | Key Features |
|-----------|----------------|--------------|
| `Category.php` | `categories` | Top-level classification |
| `SubCategory.php` | `sub_categories` | Sub-classification |
| `Item.php` | `items` | ProductType/Type classification |
| `Product.php` | `products` | Generic and specific products |
| `Make.php` | `makes` | OEM brands |
| `Series.php` | `series` | OEM series |
| `Price.php` | `prices` | Product pricing |
| `Attribute.php` | `attributes` | Attribute definitions |
| `CategoryAttribute.php` | `category_attributes` | Attribute schema mapping |
| `ProductAttribute.php` | `product_attributes` | Product attribute values |
| `MasterBom.php` | `master_boms` | Master BOM templates |
| `MasterBomItem.php` | `master_bom_items` | Master BOM items (L0/L1) |
| `Quotation.php` | `quotations` | Quotation header |
| `QuotationSale.php` | `quotation_sales` | Panel level |
| `QuotationSaleBom.php` | `quotation_sale_boms` | Feeder/BOM level |
| `QuotationSaleBomItem.php` | `quotation_sale_bom_items` | Component level (L2) |
| `QuotationMakeSeries.php` | `quotation_make_series` | Quotation make/series selections |
| `QuotationDiscount.php` | `quotation_discounts` | Quotation-level discounts |
| `QuotationDiscountRule.php` | `quotation_discount_rules` | Discount rules |
| `PricingAuditLog.php` | `pricing_audit_logs` | Price change audit |
| `DiscountRuleApplyAuditLog.php` | `discount_rule_apply_audit_logs` | Discount rule audit |
| `DiscountRuleApplySnapshot.php` | `discount_rule_apply_snapshots` | Discount rule snapshots |

#### Controllers (app/Http/Controllers/)

| Controller File | Primary Feature | Key Models Used |
|----------------|-----------------|-----------------|
| `CategoryController.php` | Category management | Category |
| `SubCategoryController.php` | SubCategory management | SubCategory |
| `ItemController.php` | Item/ProductType management | Item |
| `GenericController.php` | Generic product management | Product |
| `ProductController.php` | Specific product management | Product |
| `MakeController.php` | Make management | Make |
| `SeriesController.php` | Series management | Series |
| `PriceController.php` | Price list management | Price, Product |
| `AttributeController.php` | Attribute management | Attribute |
| `CategoryAttributeController.php` | Category attribute mapping | CategoryAttribute |
| `ProductAttributeController.php` | Product attribute values | ProductAttribute |
| `MasterBomController.php` | Master BOM management | MasterBom, MasterBomItem |
| `FeederTemplateController.php` | Feeder template management | MasterBom |
| `ProposalBomController.php` | Proposal BOM management | QuotationSaleBom, MasterBom |
| `QuotationV2Controller.php` | Quotation V2 operations | Quotation, QuotationSale, QuotationSaleBom, QuotationSaleBomItem |
| `QuotationController.php` | Legacy quotation operations | Quotation, QuotationSale, QuotationSaleBom, QuotationSaleBomItem |
| `QuotationDiscountRuleController.php` | Discount rule management | QuotationDiscountRule |
| `CatalogHealthController.php` | Catalog health checks | Product, Price, Category, SubCategory, Item |
| `CatalogCleanupController.php` | Catalog cleanup | Product, Price, MasterBom |
| `ReuseController.php` | Reuse past quotations | Quotation, QuotationSale, QuotationSaleBom |

#### Services (app/Services/)

| Service File | Primary Feature | Key Models Used |
|--------------|-----------------|-----------------|
| `QuotationQuantityService.php` | Quantity calculations | QuotationSaleBomItem, QuotationSaleBom, QuotationSale |
| `CostingService.php` | Costing calculations | QuotationSaleBomItem, QuotationSaleBom, QuotationSale, Quotation |
| `DeletionPolicyService.php` | Deletion validation | All Models |
| `DiscountRuleApplyService.php` | Discount rule application | QuotationDiscountRule, QuotationSaleBomItem |
| `ProductAttributeService.php` | Product attribute management | Product, CategoryAttribute, ProductAttribute |
| `AutoNamingService.php` | Auto naming | Product, QuotationSaleBom |
| `QuotationDiscountRuleService.php` | Discount rule logic | QuotationDiscountRule |

#### DTOs (app/Services/DTOs/)

| DTO File | Purpose | Used By |
|----------|---------|---------|
| `ComponentCostDto.php` | Component cost data structure | CostingService |
| `BomCostDto.php` | BOM cost data structure | CostingService |
| `FeederCostDto.php` | Feeder cost data structure | CostingService |
| `PanelCostDto.php` | Panel cost data structure | CostingService |

---

### 17.11 Cross-Reference Summary

#### For Product Master Work:
- **Database:** `products` table
- **Model:** `Product.php`
- **Controllers:** `GenericController.php`, `ProductController.php`
- **Service:** `ProductAttributeService.php`
- **Views:** `resources/views/generic/*.blade.php`, `resources/views/product/*.blade.php`

#### For Master BOM Work:
- **Database:** `master_boms`, `master_bom_items` tables
- **Models:** `MasterBom.php`, `MasterBomItem.php`
- **Controller:** `MasterBomController.php`
- **Views:** `resources/views/masterbom/*.blade.php`

#### For Quotation V2 Work:
- **Database:** `quotation_sale_boms`, `quotation_sale_bom_items` tables
- **Models:** `QuotationSaleBom.php`, `QuotationSaleBomItem.php`
- **Controller:** `QuotationV2Controller.php`
- **Services:** `QuotationQuantityService.php`, `CostingService.php`
- **Views:** `resources/views/quotation/v2/*.blade.php`

#### For Pricing Work:
- **Database:** `prices` table
- **Model:** `Price.php`
- **Controller:** `PriceController.php`
- **Model:** `PricingAuditLog.php` (audit)
- **Views:** `resources/views/price/*.blade.php`

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial comprehensive document | Complete item master design with all sections |
| 1.1 | 2025-12-15 | Auto | Added practical examples, workflows, troubleshooting, and code examples | Added sections 12-16 with practical content |

---

**END OF DOCUMENT**

**This document is a PERMANENT STANDARD for all item master, BOM, and pricing work.**

