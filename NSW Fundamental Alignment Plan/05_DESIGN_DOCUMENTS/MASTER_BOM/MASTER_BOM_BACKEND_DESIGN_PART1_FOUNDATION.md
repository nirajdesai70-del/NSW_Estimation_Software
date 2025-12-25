# Master BOM Backend Design - Part 1: Foundation & Architecture

**Document:** MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md  
**Version:** 1.1  
**Date:** December 2025

---

## 📋 Overview

This document describes the foundational architecture and basic structure of the Master BOM Backend System. Master BOM serves as reusable templates that can be copied into quotations as Proposal BOMs.

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

- **Proposal/Specific BOM = Quotation-specific instance**
  - Multiple Proposal BOMs can exist for one Master BOM
  - Must resolve L1 → L2 before finalization

---

## 🏗️ Basic Structure

### System Architecture

The Master BOM Backend follows a **layered architecture** pattern:

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│  (Blade Views, AJAX Endpoints, API Responses)            │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│                    CONTROLLER LAYER                       │
│  (MasterBomController, Request Validation)               │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│                    MODEL LAYER                            │
│  (Eloquent ORM Models, Relationships)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────┐
│                    DATABASE LAYER                        │
│  (MySQL Tables, Foreign Keys, Indexes)                  │
└──────────────────────────────────────────────────────────┘
```

---

## 🧩 Core Components

### 1. Master BOM Engine

**Purpose:** Main master BOM management engine

**Key Components:**
- **MasterBomController** - Main controller handling all master BOM operations
- **MasterBom Model** - Eloquent ORM model for master BOM header
- **MasterBomItem Model** - Eloquent ORM model for master BOM items

**Location:**
- Controller: `app/Http/Controllers/MasterBomController.php`
- Models: `app/Models/MasterBom.php`, `app/Models/MasterBomItem.php`

---

### 2. Data Models

**Master BOM Models:**
- `MasterBom` - Master BOM header (template)
- `MasterBomItem` - Items in master BOM template

**Related Models:**
- `Product` - Generic products (referenced by MasterBomItem)
- `Category`, `SubCategory`, `Item` - Product hierarchy

---

## 🎯 Design Principles

### 1. Template Concept

**Rule:** Master BOM is a template, not an instance

**Characteristics:**
- Reusable across multiple quotations
- Contains generic products only (ProductType = 1)
- Template quantities (default quantities)
- No pricing (pricing loaded when copied to quotation)
- No Make/Series (selected when copied to quotation)

---

### 2. Copy Rule (Non-Negotiable)

**Rule:** Always copy Master BOM, never link directly

**Implementation:**
- When adding Master BOM to quotation, copy all items
- Create new `QuotationSaleBom` and `QuotationSaleBomItem` records
- Set `MasterBomId` for reference only (not for linking)
- Changes to Master BOM don't affect existing quotations

**Why:**
- Independence: Each quotation has its own BOM structure
- Flexibility: Can modify proposal BOM without affecting master
- History: Preserves quotation state at time of creation

---

### 3. Generic Products Only

**Rule:** Master BOM items reference generic products only

**Implementation:**
- MasterBomItem.ProductId must point to ProductType = 1 (Generic)
- No Make/Series in master BOM items
- Make/Series selected when copying to quotation

**Why:**
- Templates should be generic
- Specific product selection happens in quotation context
- Allows flexibility in quotation

---

### 4. Template Quantities

**Rule:** Master BOM contains template quantities

**Implementation:**
- MasterBomItem.Quantity is template quantity
- When copied to quotation, quantity is copied
- User can modify quantity in quotation

**Example:**
```
Master BOM: "Standard Panel Components"
  Item 1: Circuit Breaker, Quantity = 12 (template)
  
When copied to quotation:
  Proposal Item: Circuit Breaker, Qty = 12 (copied)
  User can change to Qty = 15 (modified in quotation)
```

---

## 🛠️ Technology Stack

### Framework
- **Laravel** - PHP framework (version 8.x+)
- **Eloquent ORM** - Database abstraction layer

### Database
- **MySQL** - Relational database (InnoDB engine)
- **Foreign Keys** - Referential integrity
- **Indexes** - Performance optimization

---

## 📊 System Flow

### Request Flow

```
1. HTTP Request → MasterBomController
2. Controller validates input
3. Controller loads models (with relationships)
4. Controller performs operations (CRUD)
5. Controller formats response (JSON/View)
6. Response sent to client
```

### Data Flow

```
1. User creates master BOM → MasterBom model
2. User adds items to master BOM → MasterBomItem model
3. User creates quotation → Quotation model
4. User adds master BOM to quotation → Copy process
5. System copies master BOM → QuotationSaleBom (Proposal BOM)
6. System copies items → QuotationSaleBomItem (Proposal Items)
7. User selects Make/Series → Updates Proposal Items
```

---

## 🔗 Master BOM in System Context

### Position in Hierarchy

```
Product Master
    └─── Generic Product
            │
            └─── Master BOM (Template)
                    │
                    └─── Master BOM Item
                            │
                            └─── Generic Product (reference)
                                    │
                                    └─── [Copy Process]
                                            │
                                            └─── Proposal BOM (in Quotation)
                                                    │
                                                    └─── Proposal Item
                                                            │
                                                            └─── Specific Product (after Make/Series selection)
```

### Purpose

**Master BOM serves as:**
- Reusable BOM templates
- Standard component lists
- Quick quotation creation
- Consistency across quotations
- Template for common assemblies

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial foundation document | Part 1 of Master BOM backend design series |
| 1.1 | 2025-12-19 | Phase-3 | Inserted canonical L0/L1/L2 definitions; terminology aligned | Phase-3: Rule Compliance Review |

---

**Next:** [Part 2: Data Models & Relationships](MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md)

