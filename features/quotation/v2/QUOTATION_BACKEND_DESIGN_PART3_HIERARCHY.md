> Source: source_snapshot/QUOTATION_BACKEND_DESIGN_PART3_HIERARCHY.md
> Bifurcated into: features/quotation/v2/QUOTATION_BACKEND_DESIGN_PART3_HIERARCHY.md
> Module: Quotation > V2
> Date: 2025-12-17 (IST)

# Quotation Backend Design - Part 3: Quotation Hierarchy Structure

**Document:** QUOTATION_BACKEND_DESIGN_PART3_HIERARCHY.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete hierarchical structure of quotations: Panel → Feeder → BOM1 → BOM2 → Component. This is the core structure that organizes all quotation data.

---

## 🏗️ Hierarchy Overview

### Complete Hierarchy Tree

```
QUOTATION (Header)
    │
    └─── PANEL (QuotationSale)
            │
            ├─── FEEDER 1 (QuotationSaleBom, Level=0)
            │       │
            │       ├─── BOM1-A (QuotationSaleBom, Level=1)
            │       │       │
            │       │       ├─── BOM2-X (QuotationSaleBom, Level=2)
            │       │       │       └─── Component 1 (QuotationSaleBomItem)
            │       │       │       └─── Component 2 (QuotationSaleBomItem)
            │       │       │
            │       │       ├─── BOM2-Y (QuotationSaleBom, Level=2)
            │       │       │       └─── Component 3 (QuotationSaleBomItem)
            │       │       │
            │       │       └─── Component 4 (QuotationSaleBomItem) [Direct under BOM1]
            │       │
            │       └─── Component 5 (QuotationSaleBomItem) [Direct under Feeder]
            │
            ├─── FEEDER 2 (QuotationSaleBom, Level=0)
            │       └─── BOM1-B (QuotationSaleBom, Level=1)
            │               └─── Component 6 (QuotationSaleBomItem)
            │
            └─── FEEDER 3 (QuotationSaleBom, Level=0)
                    └─── Component 7 (QuotationSaleBomItem) [Direct under Feeder]
```

---

## 📊 Level 1: Quotation (Header)

### Entity: Quotation

**Table:** `quotations`  
**Model:** `Quotation`  
**Purpose:** Main quotation document header

**Key Attributes:**
- `QuotationId` - Primary key
- `QuotationNo` - Unique quotation number (YYMMDD001)
- `ClientId` - Customer company
- `ProjectId` - Client project
- `ContactId` - Contact person
- `SalesId` - Sales person
- `EmployeeId` - Responsible employee
- `ParentId` - Parent quotation (for revisions)
- `Discount` - Overall quotation discount

**Relationships:**
- **belongsTo:** Client, Project, Contact, User (Sales), User (Employee)
- **hasMany:** QuotationSale (Panels), QuotationMakeSeries

**Business Rules:**
- One quotation belongs to one client
- One quotation belongs to one project
- One quotation can have multiple panels
- Quotation can have revisions (ParentId links to original)

**Example:**
```
Quotation #220716001
├── Client: Tech Industries
├── Project: Factory Setup
├── Contact: John Doe
├── Sales Person: Jane Smith
└── Panels: 3 panels
```

---

## 📊 Level 2: Panel (QuotationSale)

### Entity: Panel / QuotationSale

**Table:** `quotation_sales`  
**Model:** `QuotationSale`  
**Purpose:** Top-level deliverable in quotation (e.g., "MCC Panel", "DB Panel")

**Key Attributes:**
- `QuotationSaleId` - Primary key
- `QuotationId` - Foreign key to quotations
- `Name` - Panel name
- `Qty` - Panel quantity (number of identical panels)
- `Rate` - Panel rate (if direct sale, rarely used)
- `Amount` - Panel amount
- `Margin`, `MarginAmount`, `MarginTotal` - Margin tracking

**Relationships:**
- **belongsTo:** Quotation
- **hasMany:** QuotationSaleBom (Feeders), QuotationSaleBomItem (Direct components)

**Business Rules:**
- One panel belongs to one quotation
- One panel can have multiple feeders
- PanelQty (Qty) is the multiplier for all components
- Panel can have direct components (rare, usually under feeders)

**Example:**
```
Panel: "MCC Panel"
├── PanelQty: 2 (two identical panels)
├── Feeders: 3 feeders
└── Direct Components: 0 (all under feeders)
```

**V2 Naming:**
- In V2, `QuotationSale` is called **Panel**
- Legacy code may still use "Sale" terminology

---

## 📊 Level 3: Feeder (QuotationSaleBom, Level=0)

### Entity: Feeder

**Table:** `quotation_sale_boms`  
**Model:** `QuotationSaleBom`  
**Level:** 0  
**Purpose:** Repeated functional assembly inside a panel (e.g., "Incomer", "Outgoing Feeder-A")

**Key Attributes:**
- `QuotationSaleBomId` - Primary key
- `QuotationSaleId` - Foreign key to quotation_sales (panel)
- `QuotationId` - Foreign key to quotations (for quick access)
- `Level` - Must be 0 for feeders
- `ParentBomId` - Must be NULL for feeders
- `FeederName` - Feeder name
- `Qty` - Feeder quantity (how many times feeder appears per panel)
- `Rate`, `Amount` - Optional rate/amount

**Identification Rules:**
A BOM is a feeder if:
- `Level = 0` AND `ParentBomId = NULL` (Standard V2)
- OR `Level = NULL` AND `ParentBomId = NULL` (Legacy compatibility)
- OR `Level >= 1` AND `ParentBomId = NULL` (Orphaned BOMs treated as feeders)

**Relationships:**
- **belongsTo:** QuotationSale (Panel), Quotation
- **hasMany:** QuotationSaleBom (Child BOMs - BOM1), QuotationSaleBomItem (Direct components)

**Business Rules:**
- One feeder belongs to one panel
- One feeder can have multiple BOM1 children
- FeederQty (Qty) is the multiplier for all components under this feeder
- Feeder can have direct components (components directly under feeder, not under BOM)

**Example:**
```
Feeder: "Incomer"
├── FeederQty: 1 (one incomer per panel)
├── BOM1 Children: 2 BOM1s
└── Direct Components: 0 (all under BOM1s)
```

---

## 📊 Level 4: BOM1 (QuotationSaleBom, Level=1)

### Entity: BOM1

**Table:** `quotation_sale_boms`  
**Model:** `QuotationSaleBom`  
**Level:** 1  
**Purpose:** Nested assembly under feeder

**Key Attributes:**
- `QuotationSaleBomId` - Primary key
- `QuotationSaleId` - Foreign key to quotation_sales (panel)
- `QuotationId` - Foreign key to quotations
- `Level` - Must be 1 for BOM1
- `ParentBomId` - Foreign key to feeder's QuotationSaleBomId
- `BomName` - BOM name
- `Qty` - BOM1 quantity (how many times BOM1 appears under feeder)
- `Rate`, `Amount` - Optional rate/amount

**Relationships:**
- **belongsTo:** QuotationSale (Panel), Quotation, QuotationSaleBom (Parent Feeder)
- **hasMany:** QuotationSaleBom (Child BOMs - BOM2), QuotationSaleBomItem (Direct components)

**Business Rules:**
- One BOM1 belongs to one feeder
- One BOM1 can have multiple BOM2 children
- BOM1Qty (Qty) is the multiplier for all components under this BOM1
- BOM1 can have direct components (components directly under BOM1, not under BOM2)

**Example:**
```
BOM1: "Main Circuit Assembly"
├── BOM1Qty: 2 (two assemblies per feeder)
├── BOM2 Children: 3 BOM2s
└── Direct Components: 1 component (direct under BOM1)
```

---

## 📊 Level 5: BOM2 (QuotationSaleBom, Level=2)

### Entity: BOM2

**Table:** `quotation_sale_boms`  
**Model:** `QuotationSaleBom`  
**Level:** 2  
**Purpose:** Nested assembly under BOM1 (leaf BOM level)

**Key Attributes:**
- `QuotationSaleBomId` - Primary key
- `QuotationSaleId` - Foreign key to quotation_sales (panel)
- `QuotationId` - Foreign key to quotations
- `Level` - Must be 2 for BOM2
- `ParentBomId` - Foreign key to BOM1's QuotationSaleBomId
- `BomName` - BOM name
- `Qty` - BOM2 quantity (how many times BOM2 appears under BOM1)
- `Rate`, `Amount` - Optional rate/amount

**Relationships:**
- **belongsTo:** QuotationSale (Panel), Quotation, QuotationSaleBom (Parent BOM1)
- **hasMany:** QuotationSaleBomItem (Components only - BOM2 is leaf level)

**Business Rules:**
- One BOM2 belongs to one BOM1
- BOM2 is a leaf node (cannot have child BOMs)
- BOM2Qty (Qty) is the multiplier for all components under this BOM2
- BOM2 contains only components (no direct child BOMs)

**Example:**
```
BOM2: "Breaker Assembly"
├── BOM2Qty: 3 (three assemblies per BOM1)
└── Components: 5 components (all under BOM2)
```

---

## 📊 Level 6: Component (QuotationSaleBomItem)

### Entity: Component

**Table:** `quotation_sale_bom_items`  
**Model:** `QuotationSaleBomItem`  
**Purpose:** Actual purchasable item/line (product)

**Key Attributes:**
- `QuotationSaleBomItemId` - Primary key
- `QuotationSaleId` - Foreign key to quotation_sales (panel)
- `QuotationId` - Foreign key to quotations
- `QuotationSaleBomId` - Foreign key to parent BOM/Feeder
- `ProductId` - Foreign key to products (specific product)
- `MakeId` - Make/brand selection
- `SeriesId` - Series selection
- `Qty` - Item quantity per BOM (ItemQtyPerBom)
- `Rate` - Base rate
- `Discount` - Discount percentage (0-100)
- `NetRate` - Calculated: Rate × (1 - Discount/100)
- `Amount` - Calculated: NetRate × TotalQty
- `Description` - Product description
- `Remark` - Additional remarks
- `RateSource` - PRICELIST / MANUAL_WITH_DISCOUNT / FIXED_NO_DISCOUNT
- `IsClientSupplied` - 0=Normal, 1=Client supplied (zero cost)
- `IsPriceMissing` - Price missing flag
- `Status` - 0=Active, 1=Deleted

**Relationships:**
- **belongsTo:** QuotationSale (Panel), Quotation, QuotationSaleBom (Parent BOM/Feeder), Product, Make, Series

**Business Rules:**
- One component belongs to one BOM/Feeder
- Component references specific product (ProductId)
- ItemQty (Qty) is quantity per immediate parent BOM
- Component can be at any level: directly under Feeder, BOM1, or BOM2

**Example:**
```
Component: "MCB 10A"
├── ProductId: 315 (Specific product)
├── Make: Schneider
├── Series: Easy9
├── ItemQty: 12 (twelve units per BOM)
├── Rate: 50.00
├── Discount: 10%
├── NetRate: 45.00
└── Amount: Calculated from TotalQty
```

---

## 🔗 Hierarchy Storage in Database

### How Hierarchy is Stored

**Single Table Design:**
- All BOMs (Feeders, BOM1, BOM2) are stored in `quotation_sale_boms` table
- Differentiation by `Level` column:
  - `Level = 0` → Feeder
  - `Level = 1` → BOM1
  - `Level = 2` → BOM2
- Hierarchy maintained by `ParentBomId`:
  - Feeder: `ParentBomId = NULL`
  - BOM1: `ParentBomId = Feeder's QuotationSaleBomId`
  - BOM2: `ParentBomId = BOM1's QuotationSaleBomId`

**Components:**
- All components stored in `quotation_sale_bom_items` table
- `QuotationSaleBomId` links component to parent BOM/Feeder
- Components can be at any level (directly under Feeder, BOM1, or BOM2)

---

## 🔍 Hierarchy Navigation

### Walking Up the Tree

**From Component to Panel:**
```php
$item = QuotationSaleBomItem::find($itemId);
$bom = $item->bom; // Parent BOM/Feeder
$panel = $item->quotationSale; // Panel

// Walk up BOM chain
$currentBom = $bom;
while ($currentBom->parentBom) {
    $currentBom = $currentBom->parentBom;
    // $currentBom is now feeder (Level 0)
}
```

**From Panel to All Components:**
```php
$panel = QuotationSale::find($panelId);
$feeders = $panel->feeders; // All feeders (Level 0)

foreach ($feeders as $feeder) {
    $childBoms = $feeder->childBoms; // All BOM1 children
    $directItems = $feeder->item; // Direct components under feeder
    
    foreach ($childBoms as $bom1) {
        $bom2Children = $bom1->childBoms; // All BOM2 children
        $directItems = $bom1->item; // Direct components under BOM1
        
        foreach ($bom2Children as $bom2) {
            $items = $bom2->item; // Components under BOM2
        }
    }
}
```

---

## 📐 Hierarchy Rules

### 1. Level Rules

- **Level 0:** Feeder (top level under panel)
- **Level 1:** BOM1 (under feeder)
- **Level 2:** BOM2 (under BOM1, leaf level)
- **Level NULL:** Treated as Level 0 for backward compatibility

### 2. Parent Rules

- **Feeder:** `ParentBomId = NULL`
- **BOM1:** `ParentBomId = Feeder's QuotationSaleBomId`
- **BOM2:** `ParentBomId = BOM1's QuotationSaleBomId`

### 3. Component Rules

- Component's `QuotationSaleBomId` points to immediate parent (Feeder, BOM1, or BOM2)
- Component's `QuotationSaleId` points to panel (for quick access)
- Component's `QuotationId` points to quotation (for quick access)

### 4. Quantity Rules

- **PanelQty:** Multiplies all components in panel
- **FeederQty:** Multiplies all components under feeder
- **BOM1Qty:** Multiplies all components under BOM1
- **BOM2Qty:** Multiplies all components under BOM2
- **ItemQty:** Quantity per immediate parent BOM

**Final Quantity Calculation:**
```
TotalQty = PanelQty × FeederQty × BOM1Qty × BOM2Qty × ItemQty
```

---

## 🎯 Common Patterns

### Pattern 1: Simple Panel (No BOMs)

```
Panel: "Simple Panel"
└─── Feeder: "Main"
    └─── Component 1
    └─── Component 2
```

### Pattern 2: Panel with BOM1 Only

```
Panel: "Standard Panel"
└─── Feeder: "Incomer"
    └─── BOM1: "Circuit Assembly"
        └─── Component 1
        └─── Component 2
```

### Pattern 3: Panel with BOM1 and BOM2

```
Panel: "Complex Panel"
└─── Feeder: "Incomer"
    └─── BOM1: "Main Assembly"
        └─── BOM2: "Breaker Assembly"
            └─── Component 1
            └─── Component 2
        └─── BOM2: "Terminal Assembly"
            └─── Component 3
```

### Pattern 4: Multiple Feeders

```
Panel: "Multi-Feeder Panel"
├─── Feeder: "Incomer"
│   └─── BOM1: "Incomer Assembly"
│       └─── Component 1
├─── Feeder: "Outgoing-1"
│   └─── BOM1: "Outgoing Assembly"
│       └─── Component 2
└─── Feeder: "Outgoing-2"
    └─── BOM1: "Outgoing Assembly"
        └─── Component 3
```

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial hierarchy document | Part 3 of backend design series |

---

**Previous:** [Part 2: Data Models & Relationships](QUOTATION_BACKEND_DESIGN_PART2_DATA_MODELS.md)  
**Next:** [Part 4: Quantity Calculation System](QUOTATION_BACKEND_DESIGN_PART4_QUANTITY.md)

