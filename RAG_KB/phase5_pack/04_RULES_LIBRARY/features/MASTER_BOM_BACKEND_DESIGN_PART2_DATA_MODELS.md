---
Source: features/master_bom/structure/MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T01:38:30.958366
KB_Path: phase5_pack/04_RULES_LIBRARY/features/MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md
---

> Source: source_snapshot/MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md
> Bifurcated into: features/master_bom/structure/MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md
> Module: Master BOM > Structure
> Date: 2025-12-17 (IST)

# Master BOM Backend Design - Part 2: Data Models & Relationships

**Document:** MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete data model structure, database schema, and all relationships for the Master BOM module.

---

## 🗄️ Database Schema

### master_boms Table

**Purpose:** Store master BOM templates (reusable BOM headers)

**Key Columns:**
- `MasterBomId` (PK) - Primary key, auto-increment
- `Name` - Master BOM name (required)
- `Status` - Status flag (0=Active, 1=Deleted)
- `created_at` - Created timestamp
- `updated_at` - Updated timestamp

**Indexes:**
- PRIMARY KEY (MasterBomId)

**Relationships:**
- Has many MasterBomItem
- Referenced by QuotationSaleBom (MasterBomId - reference only)

---

### master_bom_items Table

**Purpose:** Store items in master BOM templates

**Key Columns:**
- `MasterBomItemId` (PK) - Primary key, auto-increment
- `MasterBomId` (FK) - Foreign key to master_boms
- `ProductId` (FK) - Foreign key to products (Generic product only, ProductType = 1)
- `Quantity` - Template quantity (default quantity)
- `Status` - Status flag (0=Active, 1=Deleted)
- `created_at` - Created timestamp
- `updated_at` - Updated timestamp

**Indexes:**
- PRIMARY KEY (MasterBomItemId)
- INDEX (MasterBomId)
- INDEX (ProductId)

**Relationships:**
```sql
FOREIGN KEY (MasterBomId) REFERENCES master_boms(MasterBomId)
FOREIGN KEY (ProductId) REFERENCES products(ProductId)
```

**Important Rule:**
- ProductId must reference Generic Product only (ProductType = 1)
- No Make/Series in master BOM items
- No pricing in master BOM items

---

## 📊 Model Structure

### MasterBom Model

**File:** `app/Models/MasterBom.php`  
**Table:** `master_boms`  
**Primary Key:** MasterBomId

**Fillable Fields:**
```php
protected $fillable = [
    'MasterBomId',
    'Name',
    'Status',
];
```

**Relationships:**
```php
// MasterBom hasMany MasterBomItem
public function items()
{
    return $this->hasMany(MasterBomItem::class, 'MasterBomId', 'MasterBomId');
}

// MasterBom hasMany QuotationSaleBom (reference only)
public function quotationBoms()
{
    return $this->hasMany(QuotationSaleBom::class, 'MasterBomId', 'MasterBomId');
}
```

---

### MasterBomItem Model

**File:** `app/Models/MasterBomItem.php`  
**Table:** `master_bom_items`  
**Primary Key:** MasterBomItemId

**Fillable Fields:**
```php
protected $fillable = [
    'MasterBomItemId',
    'MasterBomId',
    'ProductId',    // Generic product only
    'Quantity',    // Template quantity
    'Status',
];
```

**Relationships:**
```php
// MasterBomItem belongsTo MasterBom
public function masterBom()
{
    return $this->belongsTo(MasterBom::class, 'MasterBomId', 'MasterBomId');
}

// MasterBomItem belongsTo Product (Generic only)
public function product()
{
    return $this->belongsTo(Product::class, 'ProductId', 'ProductId');
}
```

---

## 🔗 Complete Relationship Map

### Master BOM Structure

```
MasterBom (1)
    │
    └─── MasterBomItem (N)
            │
            └─── Product (Generic) (1)
                    │
                    ├─── Category
                    ├─── SubCategory
                    ├─── Item
                    │
                    └─── Product (Specific) (N) [after Make/Series selection in quotation]
```

---

### Master BOM → Proposal BOM Flow

```
MasterBom (Template)
    │
    └─── MasterBomItem (Template Items)
            │
            └─── Product (Generic)
                    │
                    └─── [Copy Process]
                            │
                            └─── QuotationSaleBom (Proposal BOM)
                                    │
                                    └─── QuotationSaleBomItem (Proposal Items)
                                            │
                                            └─── Product (Specific) [after Make/Series selection]
```

---

## 📊 Relationship Details

### MasterBom → MasterBomItem

**Type:** One-to-Many (1:N)

**Implementation:**
```php
// In MasterBom model
public function items()
{
    return $this->hasMany(MasterBomItem::class, 'MasterBomId', 'MasterBomId');
}

// Usage
$masterBom = MasterBom::with('items')->find($masterBomId);
$items = $masterBom->items; // Collection of master BOM items
```

**Business Rules:**
- One master BOM can have multiple items
- One item belongs to one master BOM
- Items reference generic products only

---

### MasterBomItem → Product

**Type:** Many-to-One (N:1)

**Implementation:**
```php
// In MasterBomItem model
public function product()
{
    return $this->belongsTo(Product::class, 'ProductId', 'ProductId');
}

// Usage
$item = MasterBomItem::with('product')->find($itemId);
$productName = $item->product->Name;
```

**Business Rules:**
- MasterBomItem.ProductId must be Generic Product (ProductType = 1)
- No Make/Series in master BOM items
- Product must exist

---

### MasterBom → QuotationSaleBom (Reference)

**Type:** One-to-Many (1:N) - Reference only

**Implementation:**
```php
// In MasterBom model
public function quotationBoms()
{
    return $this->hasMany(QuotationSaleBom::class, 'MasterBomId', 'MasterBomId');
}

// Usage
$masterBom = MasterBom::with('quotationBoms')->find($masterBomId);
$proposalBoms = $masterBom->quotationBoms; // All proposal BOMs copied from this master
```

**Business Rules:**
- MasterBomId in QuotationSaleBom is reference only
- Changes to Master BOM don't affect existing Proposal BOMs
- Used for tracking which master BOM was copied

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial data models document | Part 2 of Master BOM backend design series |

---

**Previous:** [Part 1: Foundation & Architecture](MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md)  
**Next:** [Part 3: Master BOM Structure](MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md)

