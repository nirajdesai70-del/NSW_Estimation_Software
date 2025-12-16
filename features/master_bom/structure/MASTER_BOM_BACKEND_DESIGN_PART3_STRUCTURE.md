> Source: source_snapshot/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md
> Bifurcated into: features/master_bom/structure/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md
> Module: Master BOM > Structure
> Date: 2025-12-17 (IST)

# Master BOM Backend Design - Part 3: Master BOM Structure

**Document:** MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete structure of the Master BOM entity, its items, attributes, fields, and its position in the system.

---

## 🏗️ Master BOM Entity Structure

### MasterBom Entity

**Table:** `master_boms`  
**Model:** `MasterBom`  
**Purpose:** Reusable BOM template (header)

**Key Attributes:**
- `MasterBomId` - Primary key
- `Name` - Master BOM name (required)
- `Status` - Status flag (0=Active, 1=Deleted)

**Structure:**
```
MasterBom
    ├─── MasterBomId (PK)
    ├─── Name (required)
    ├─── Status (0=Active, 1=Deleted)
    └─── MasterBomItem[] (items collection)
```

---

### MasterBomItem Entity

**Table:** `master_bom_items`  
**Model:** `MasterBomItem`  
**Purpose:** Items in master BOM template

**Key Attributes:**
- `MasterBomItemId` - Primary key
- `MasterBomId` - Foreign key to master_boms
- `ProductId` - Foreign key to products (Generic only)
- `Quantity` - Template quantity (default quantity)

**Structure:**
```
MasterBomItem
    ├─── MasterBomItemId (PK)
    ├─── MasterBomId (FK)
    ├─── ProductId (FK - Generic Product only)
    ├─── Quantity (template quantity)
    └─── Status (0=Active, 1=Deleted)
```

---

## 📊 Field Details

### MasterBom Fields

**MasterBomId:**
- Type: Integer (Primary Key)
- Auto-increment: Yes
- Purpose: Unique identifier

**Name:**
- Type: String (VARCHAR 255)
- Required: Yes
- Purpose: Master BOM name/identifier
- Example: "Standard Distribution Panel - 100A"

**Status:**
- Type: TinyInt
- Required: Yes (default 0)
- Values: 0=Active, 1=Deleted
- Purpose: Soft delete flag

---

### MasterBomItem Fields

**MasterBomItemId:**
- Type: Integer (Primary Key)
- Auto-increment: Yes
- Purpose: Unique identifier

**MasterBomId:**
- Type: Integer (Foreign Key)
- Required: Yes
- References: `master_boms.MasterBomId`
- Purpose: Links item to master BOM

**ProductId:**
- Type: Integer (Foreign Key)
- Required: Yes
- References: `products.ProductId`
- **Constraint:** Must be Generic Product (ProductType = 1)
- Purpose: References generic product

**Quantity:**
- Type: Numeric (DECIMAL)
- Required: Yes
- Purpose: Template quantity (default quantity)
- Example: 12 (twelve units per BOM)

**Status:**
- Type: TinyInt
- Required: Yes (default 0)
- Values: 0=Active, 1=Deleted
- Purpose: Soft delete flag

---

## 🎯 Master BOM Characteristics

### Template Characteristics

**1. Reusability:**
- Can be used in unlimited quotations
- Same master BOM can be copied multiple times
- Changes to master BOM affect future copies only

**2. Generic Products:**
- Items reference generic products only
- No Make/Series in master BOM
- Make/Series selected when copying to quotation

**3. Template Quantities:**
- Quantities are templates/defaults
- Can be modified in quotation
- Provides starting point for quotation

**4. No Pricing:**
- Master BOM has no pricing
- Pricing loaded when copied to quotation
- Price comes from prices table

---

## 📋 Master BOM Structure Example

### Example Master BOM

```
MasterBom: "Standard Distribution Panel - 100A"
    MasterBomId: 5
    Name: "Standard Distribution Panel - 100A"
    Status: 0 (Active)
    
    Items:
        Item 1:
            MasterBomItemId: 25
            MasterBomId: 5
            ProductId: 305 (Generic: "Panel Enclosure Indoor")
            Quantity: 1
            Status: 0
        
        Item 2:
            MasterBomItemId: 26
            MasterBomId: 5
            ProductId: 310 (Generic: "Main Circuit Breaker 100A")
            Quantity: 1
            Status: 0
        
        Item 3:
            MasterBomItemId: 27
            MasterBomId: 5
            ProductId: 315 (Generic: "Branch MCB 10A")
            Quantity: 12
            Status: 0
        
        Item 4:
            MasterBomItemId: 28
            MasterBomId: 5
            ProductId: 320 (Generic: "Busbar 100A")
            Quantity: 1
            Status: 0
```

---

## 🔗 Master BOM in System Context

### Position in System

```
Product Master
    └─── Generic Product (ProductType = 1)
            │
            └─── Master BOM (Template) ← CURRENT LEVEL
                    │
                    └─── Master BOM Item
                            │
                            └─── Generic Product (reference)
                                    │
                                    └─── [When copied to quotation]
                                            │
                                            └─── Proposal BOM
                                                    │
                                                    └─── Proposal Item
                                                            │
                                                            └─── Specific Product (after Make/Series selection)
```

---

### Master BOM Role

**Master BOM serves as:**
1. **Template Library** - Reusable BOM templates
2. **Standard Lists** - Standard component lists for common assemblies
3. **Quick Creation** - Enables quick quotation creation
4. **Consistency** - Ensures consistency across quotations
5. **Starting Point** - Provides starting point for quotation BOMs

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial structure document | Part 3 of Master BOM backend design series |

---

**Previous:** [Part 2: Data Models & Relationships](MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md)  
**Next:** [Part 4: Master BOM to Proposal BOM Copy Process](MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md)

