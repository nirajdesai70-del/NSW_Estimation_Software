# NEPL Estimation Software - Data Structure Documentation

**Version:** 1.0  
**Date:** 2025-12-16  
**Status:** Baseline Documentation

## Purpose

This document provides a detailed breakdown of the data structures, relationships, and hierarchies used in NEPL Estimation Software V2. This serves as the technical foundation for understanding data flow and ensuring data integrity during the NSW migration.

---

## 1. Category / Subcategory / Type / Attribute Hierarchy

### 1.1 Hierarchy Structure
```
Category (Level 1)
  └── Subcategory (Level 2)
      └── Type (Level 3)
          └── Attribute (Level 4)
              └── Item (Uses the hierarchy)
```

### 1.2 Category
**Purpose:** Top-level classification for all items

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| name | String | Yes | Category name |
| code | String | No | Category code |
| description | Text | No | Category description |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Name must be unique
- Cannot be deleted if has subcategories

**Relationships:**
- Has many: Subcategories
- Has many: Items (direct)

---

### 1.3 Subcategory
**Purpose:** Second-level classification under Category

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| category_id | Integer | Yes | Foreign key to Category |
| name | String | Yes | Subcategory name |
| code | String | No | Subcategory code |
| description | Text | No | Subcategory description |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Name must be unique within category
- Cannot be deleted if has types

**Relationships:**
- Belongs to: Category
- Has many: Types
- Has many: Items (direct)

---

### 1.4 Type
**Purpose:** Third-level classification under Subcategory

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| subcategory_id | Integer | Yes | Foreign key to Subcategory |
| name | String | Yes | Type name |
| code | String | No | Type code |
| description | Text | No | Type description |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Name must be unique within subcategory
- Cannot be deleted if has attributes

**Relationships:**
- Belongs to: Subcategory
- Has many: Attributes
- Has many: Items (direct)

---

### 1.5 Attribute
**Purpose:** Fourth-level classification under Type, defines item properties

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| type_id | Integer | Yes | Foreign key to Type |
| name | String | Yes | Attribute name |
| value_type | String | Yes | Data type (string, integer, decimal, boolean) |
| default_value | String | No | Default value |
| is_required | Boolean | No | Required flag |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Name must be unique within type
- Value type must be valid

**Relationships:**
- Belongs to: Type
- Used by: Items (via item_attributes junction table)

---

## 2. Item vs Component Reality

### 2.1 Item
**Purpose:** Represents a catalog item that can be used in BOMs

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| name | String | Yes | Item name |
| code | String | Yes | Item code (unique) |
| description | Text | No | Item description |
| category_id | Integer | Yes | Foreign key to Category |
| subcategory_id | Integer | No | Foreign key to Subcategory |
| type_id | Integer | No | Foreign key to Type |
| unit | String | Yes | Unit of measurement |
| base_price | Decimal | No | Base price |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Code must be unique
- Must belong to at least Category

**Relationships:**
- Belongs to: Category, Subcategory (optional), Type (optional)
- Has many: BOM Items
- Has many: Item Attributes (via junction table)

**Usage:**
- Items are selected from master catalog
- Items are added to BOMs
- Items have pricing information

---

### 2.2 Component
**Purpose:** Represents a component that can be used in BOMs (may differ from Items)

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| name | String | Yes | Component name |
| code | String | Yes | Component code (unique) |
| description | Text | No | Component description |
| unit | String | Yes | Unit of measurement |
| base_price | Decimal | No | Base price |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Code must be unique
- Not linked to Category/Subcategory/Type hierarchy

**Relationships:**
- Has many: BOM Items

**Usage:**
- Components are selected from component master
- Components are added to BOMs
- Components have pricing information

**Key Difference from Items:**
- Components are NOT part of Category/Subcategory/Type hierarchy
- Components may be more generic or reusable across categories

---

## 3. BOM Levels as Implemented (Not Idealized)

### 3.1 BOM Structure
```
Project
  └── Panel
      └── Feeder
          └── BOM
              └── BOM Items
                  ├── Item (with quantity, price)
                  └── Component (with quantity, price)
```

### 3.2 BOM Entity
**Purpose:** Bill of Materials linked to a Feeder

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| name | String | Yes | BOM name |
| description | Text | No | BOM description |
| feeder_id | Integer | Yes | Foreign key to Feeder |
| status | String | Yes | Status (draft, active, locked) |
| total_amount | Decimal | No | Calculated total |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Must belong to a Feeder
- Cannot be deleted if has BOM Items

**Relationships:**
- Belongs to: Feeder
- Has many: BOM Items

**Calculation Logic:**
- Total amount = Sum of (BOM Item quantity × BOM Item unit_price)

---

### 3.3 BOM Item Entity
**Purpose:** Links Items or Components to a BOM with quantities and prices

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| bom_id | Integer | Yes | Foreign key to BOM |
| item_id | Integer | No | Foreign key to Item (nullable) |
| component_id | Integer | No | Foreign key to Component (nullable) |
| quantity | Decimal | Yes | Quantity |
| unit_price | Decimal | Yes | Unit price |
| total_price | Decimal | Yes | Calculated (quantity × unit_price) |
| notes | Text | No | Additional notes |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Must have either item_id OR component_id (not both, not neither)
- Quantity must be > 0
- Unit price must be >= 0

**Relationships:**
- Belongs to: BOM
- Belongs to: Item (optional)
- Belongs to: Component (optional)

**Business Rules:**
- If item_id is set, component_id must be null
- If component_id is set, item_id must be null
- Total price is auto-calculated but can be overridden

---

## 4. Quotation Linkage

### 4.1 Quotation Entity
**Purpose:** Represents a quotation document for a project

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| quotation_number | String | Yes | Unique quotation number |
| project_id | Integer | Yes | Foreign key to Project |
| status | String | Yes | Status (draft, sent, accepted, rejected) |
| total_amount | Decimal | No | Total quotation amount |
| valid_until | Date | No | Quotation validity date |
| notes | Text | No | Additional notes |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Quotation number must be unique
- Must belong to a Project

**Relationships:**
- Belongs to: Project
- Has many: Quotation Items

---

### 4.2 Quotation Item Entity
**Purpose:** Links BOMs or individual items to a Quotation

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| quotation_id | Integer | Yes | Foreign key to Quotation |
| bom_id | Integer | No | Foreign key to BOM (nullable) |
| item_id | Integer | No | Foreign key to Item (nullable) |
| component_id | Integer | No | Foreign key to Component (nullable) |
| quantity | Decimal | Yes | Quantity |
| unit_price | Decimal | Yes | Unit price |
| total_price | Decimal | Yes | Calculated total |
| description | Text | No | Item description |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Constraints:**
- Must have at least one of: bom_id, item_id, or component_id
- Quantity must be > 0

**Relationships:**
- Belongs to: Quotation
- Belongs to: BOM (optional)
- Belongs to: Item (optional)
- Belongs to: Component (optional)

**Linkage Logic:**
- Quotation can be created from:
  1. Entire BOM (bom_id set)
  2. Individual Items (item_id set)
  3. Individual Components (component_id set)
  4. Mixed (multiple quotation items)

---

## 5. Panel and Feeder Structure

### 5.1 Panel Entity
**Purpose:** Represents an electrical panel in a project

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| name | String | Yes | Panel name |
| code | String | No | Panel code |
| description | Text | No | Panel description |
| project_id | Integer | Yes | Foreign key to Project |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Relationships:**
- Belongs to: Project
- Has many: Feeders

---

### 5.2 Feeder Entity
**Purpose:** Represents a feeder within a panel

**Fields:**
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | Integer | Yes | Primary key |
| name | String | Yes | Feeder name |
| code | String | No | Feeder code |
| description | Text | No | Feeder description |
| panel_id | Integer | Yes | Foreign key to Panel |
| is_active | Boolean | Yes | Active status |
| created_at | DateTime | Yes | Creation timestamp |
| updated_at | DateTime | Yes | Update timestamp |

**Relationships:**
- Belongs to: Panel
- Has many: BOMs

---

## 6. Data Integrity Rules

### 6.1 Cascade Rules
- Deleting a Project → Cascade delete Panels, Quotations
- Deleting a Panel → Cascade delete Feeders
- Deleting a Feeder → Cascade delete BOMs
- Deleting a BOM → Cascade delete BOM Items
- Deleting a Category → Prevent if has Subcategories
- Deleting a Subcategory → Prevent if has Types
- Deleting a Type → Prevent if has Attributes

### 6.2 Referential Integrity
- All foreign keys must reference existing records
- Soft deletes preferred over hard deletes for master data

### 6.3 Business Rules
- BOM Item must have either Item OR Component (not both)
- Quotation Item must have at least one reference (BOM, Item, or Component)
- All prices must be non-negative
- All quantities must be positive

---

## 7. Data Migration Considerations

### 7.1 Critical Data
- Master data (Categories, Items, Components) must be preserved
- Active Projects and Quotations must be preserved
- Historical data should be archived, not deleted

### 7.2 Data Quality Issues
- [ ] Identify orphaned records
- [ ] Identify missing required fields
- [ ] Identify inconsistent relationships
- [ ] Identify duplicate records

---

## Next Steps

1. Validate this structure against actual NEPL V2 database schema
2. Document any discrepancies
3. Use as reference for Phase 2 (Migration Trace)
4. Use as baseline for NSW data model design

---

**Document Owner:** [Name]  
**Last Updated:** [Date]  
**Review Date:** [Date]

