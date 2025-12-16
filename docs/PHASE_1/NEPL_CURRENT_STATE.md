# NEPL Estimation Software - Current State Documentation

**Version:** 1.0  
**Date:** 2025-12-16  
**Status:** Baseline Documentation

## Purpose

This document captures the factual, current state of the NEPL Estimation Software (V2) as it exists today. This serves as the foundation for:
- Understanding what actually works
- Identifying what needs to be preserved
- Creating the migration path to NSW Estimation Software

---

## 1. Modules Currently in Use

### 1.1 Core Modules
- [ ] **Estimation Engine**
  - Description: Core logic for estimation calculations
  - Status: Active/Inactive
  - Dependencies: [List dependencies]
  
- [ ] **Panel Management**
  - Description: 
  - Status: 
  - Dependencies: 

- [ ] **Feeder Management**
  - Description: 
  - Status: 
  - Dependencies: 

- [ ] **BOM (Bill of Materials) Management**
  - Description: 
  - Status: 
  - Dependencies: 

- [ ] **Item Management**
  - Description: 
  - Status: 
  - Dependencies: 

- [ ] **Quotation Management**
  - Description: 
  - Status: 
  - Dependencies: 

- [ ] **Component Master**
  - Description: 
  - Status: 
  - Dependencies: 

- [ ] **Item Master**
  - Description: 
  - Status: 
  - Dependencies: 

### 1.2 Supporting Modules
- [ ] **Category/Subcategory/Type/Attribute Management**
- [ ] **Costing Logic (Manual + Assisted)**
- [ ] **User Management**
- [ ] **Project Management**
- [ ] **Reporting Module**

---

## 2. Screens and User Flows

### 2.1 Main Navigation Flow
```
[Main Dashboard]
    ├── [Panel Management]
    │   ├── Create Panel
    │   ├── Edit Panel
    │   └── View Panel Details
    ├── [Feeder Management]
    │   ├── Create Feeder
    │   ├── Edit Feeder
    │   └── View Feeder Details
    ├── [BOM Management]
    │   ├── Create BOM
    │   ├── Edit BOM
    │   └── View BOM Details
    ├── [Item Management]
    │   ├── Create Item
    │   ├── Edit Item
    │   └── View Item Details
    └── [Quotation Management]
        ├── Create Quotation
        ├── Edit Quotation
        └── View Quotation
```

### 2.2 Screen Details

#### Screen: [Screen Name]
- **URL/Route:** 
- **Purpose:** 
- **Key Actions:**
  - [ ] Action 1
  - [ ] Action 2
- **Data Displayed:**
  - Field 1
  - Field 2
- **User Interactions:**
  - Click events
  - Form submissions
  - Navigation

---

## 3. Data Entities and Relationships

### 3.1 Core Entities

#### Entity: Category
- **Description:** 
- **Key Fields:**
  - id
  - name
  - description
  - created_at
  - updated_at
- **Relationships:**
  - Has many: Subcategories

#### Entity: Subcategory
- **Description:** 
- **Key Fields:**
  - id
  - name
  - category_id
  - description
- **Relationships:**
  - Belongs to: Category
  - Has many: Types

#### Entity: Type
- **Description:** 
- **Key Fields:**
  - id
  - name
  - subcategory_id
  - description
- **Relationships:**
  - Belongs to: Subcategory
  - Has many: Attributes

#### Entity: Attribute
- **Description:** 
- **Key Fields:**
  - id
  - name
  - type_id
  - value_type
- **Relationships:**
  - Belongs to: Type

#### Entity: Item
- **Description:** 
- **Key Fields:**
  - id
  - name
  - code
  - description
  - category_id
  - subcategory_id
  - type_id
- **Relationships:**
  - Belongs to: Category, Subcategory, Type
  - Has many: BOM Items

#### Entity: Component
- **Description:** 
- **Key Fields:**
  - id
  - name
  - code
  - description
- **Relationships:**
  - Used in: BOMs

#### Entity: BOM (Bill of Materials)
- **Description:** 
- **Key Fields:**
  - id
  - name
  - description
  - panel_id
  - feeder_id
- **Relationships:**
  - Belongs to: Panel, Feeder
  - Has many: BOM Items

#### Entity: BOM Item
- **Description:** 
- **Key Fields:**
  - id
  - bom_id
  - item_id
  - component_id
  - quantity
  - unit_price
  - total_price
- **Relationships:**
  - Belongs to: BOM, Item, Component

#### Entity: Panel
- **Description:** 
- **Key Fields:**
  - id
  - name
  - description
  - project_id
- **Relationships:**
  - Belongs to: Project
  - Has many: Feeders

#### Entity: Feeder
- **Description:** 
- **Key Fields:**
  - id
  - name
  - description
  - panel_id
- **Relationships:**
  - Belongs to: Panel
  - Has many: BOMs

#### Entity: Quotation
- **Description:** 
- **Key Fields:**
  - id
  - quotation_number
  - project_id
  - status
  - total_amount
  - created_at
  - updated_at
- **Relationships:**
  - Belongs to: Project
  - Has many: Quotation Items

#### Entity: Project
- **Description:** 
- **Key Fields:**
  - id
  - name
  - description
  - client_name
  - status
- **Relationships:**
  - Has many: Panels, Quotations

### 3.2 Entity Relationship Diagram (Text Representation)
```
Project
  ├── Panel
  │   └── Feeder
  │       └── BOM
  │           └── BOM Item
  │               ├── Item (via item_id)
  │               └── Component (via component_id)
  └── Quotation
      └── Quotation Item

Category
  └── Subcategory
      └── Type
          └── Attribute
              └── Item
```

---

## 4. Known Pain Points (Without Fixing)

### 4.1 Functional Issues
- [ ] Issue 1: Description
  - Impact: 
  - Frequency: 
  - Workaround: 

### 4.2 Data Issues
- [ ] Issue 1: Description
  - Impact: 
  - Frequency: 
  - Workaround: 

### 4.3 UI/UX Issues
- [ ] Issue 1: Description
  - Impact: 
  - Frequency: 
  - Workaround: 

### 4.4 Performance Issues
- [ ] Issue 1: Description
  - Impact: 
  - Frequency: 
  - Workaround: 

---

## 5. Business Logic Flow

### 5.1 Estimation Flow
```
1. Create/Select Project
2. Create Panel
3. Create Feeder (linked to Panel)
4. Create BOM (linked to Feeder)
5. Add Items/Components to BOM
6. System calculates:
   - Item quantities
   - Component quantities
   - Unit prices
   - Total prices
7. Generate Quotation from BOM
8. Finalize Quotation
```

### 5.2 Costing Logic
- **Manual Costing:**
  - User enters unit prices
  - System calculates totals
  
- **Assisted Costing:**
  - System suggests prices based on:
    - Historical data
    - Item master prices
    - Component master prices

### 5.3 Validation Rules
- [ ] Rule 1: Description
- [ ] Rule 2: Description
- [ ] Rule 3: Description

---

## 6. Technology Stack

### 6.1 Frontend
- Framework: 
- UI Library: 
- State Management: 
- Build Tool: 

### 6.2 Backend
- Framework: 
- Database: 
- ORM: 
- API: 

### 6.3 Infrastructure
- Hosting: 
- CI/CD: 
- Version Control: 

---

## 7. Current Version Information

- **Version:** V2
- **Last Major Update:** 
- **Active Features:** 
- **Deprecated Features:** 

---

## 8. Notes and Observations

### 8.1 Terminology Inconsistencies
- [ ] Term 1: Used as X in Module A, but as Y in Module B

### 8.2 Code Organization
- [ ] Observation 1
- [ ] Observation 2

### 8.3 Data Quality
- [ ] Observation 1
- [ ] Observation 2

---

## Next Steps

1. Complete all sections with actual data from NEPL V2 system
2. Validate with stakeholders
3. Use as reference for Phase 2 (Legacy Analysis)
4. Use as baseline for NSW development

---

**Document Owner:** [Name]  
**Last Updated:** [Date]  
**Review Date:** [Date]

