# Phase-5 Readiness Package for Cursor Implementation

**Date:** 2025-01-27  
**Purpose:** Deliverable package for Phase-5 design implementation in Cursor  
**Status:** Ready for SPEC-5 stepwise execution

---

## 📋 Item 1: Phase-5 Document Index

### Complete File Listing: `docs/PHASE_5/`

```
docs/PHASE_5/
├── README.md                                    # Phase-5 directory index & overview
├── QUICK_REFERENCE.md                           # One-page decision summary
├── PHASE_5_SCOPE_FENCE.md                       # Authoritative scope definition (FROZEN)
├── PHASE_5_EXECUTION_SUMMARY.md                 # Pre-execution review document
├── PHASE_5_PENDING_UPGRADES_INTEGRATION.md      # Integration guide mapping pending upgrades to Phase-5 steps
├── SCOPE_SEPARATION.md                          # Detailed separation explanation
├── POST_PHASE_5_IMPLEMENTATION_ROADMAP.md       # Post-Phase-5 implementation plan
│
├── ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md   # Architecture Decision Record for master data governance
├── NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md  # Master data creation & import governance rules (FROZEN)
├── LEGACY_VS_NSW_COEXISTENCE_POLICY.md          # Coexistence policy for Phase-4 and Phase-5
│
├── STAKEHOLDER_BRIEF_WHY_NO_LEGACY_MIGRATION.md # One-page stakeholder brief
├── NEPL_TO_NSW_EXTRACTION.md                   # Legacy extraction reference
├── NISH_PENDING_WORK_EXTRACTED.md               # Legacy work notes
│
└── PHASE_4_CLOSURE_VALIDATION_AUDIT.md          # Phase-4 closure validation audit
```

### Key Design Documents (Priority Order)

1. **`PHASE_5_SCOPE_FENCE.md`** - Authoritative scope (Step 1 & 2 only)
2. **`PHASE_5_EXECUTION_SUMMARY.md`** - Pre-execution review with integration guide references
3. **`PHASE_5_PENDING_UPGRADES_INTEGRATION.md`** - Maps pending upgrades to Phase-5 steps
4. **`NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md`** - Master data governance rules (part of Step 1)
5. **`POST_PHASE_5_IMPLEMENTATION_ROADMAP.md`** - Post-Phase-5 implementation plan

### Related Phase-5 Design Documents (Outside `docs/PHASE_5/`)

- **Schema Extraction Plan:** `project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` (template, pending extraction)
- **Item Master Design:** `features/component_item_master/_general/ITEM_MASTER_DETAILED_DESIGN.md` (current canonical model)

---

## 📊 Item 2: Current Canonical Data Model Draft

### 2.1 Primary Data Model Source

**File:** `features/component_item_master/_general/ITEM_MASTER_DETAILED_DESIGN.md`

**Status:** Current canonical model (STANDING INSTRUCTION - PERMANENT STANDARD)

### 2.2 Core Hierarchy Structure

```
Category (Required)
  └── SubCategory (Optional)
        └── Item/ProductType (Optional, stored in `items` table)
              └── Generic Product (ProductType = 1) [L1]
                    └── Make (Optional)
                          └── Series (Optional)
                                └── Specific Product (ProductType = 2) [L2]
```

### 2.3 Database Tables (Canonical Model)

#### CIM Module (Component Item Master)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `categories` | Top-level classification | `CategoryId` (PK), `Name` (Required) |
| `sub_categories` | Sub-classification | `SubCategoryId` (PK), `CategoryId` (FK), `Name` |
| `items` | ProductType/Type classification | `ItemId` (PK), `CategoryId` (FK), `SubCategoryId` (FK), `Name` |
| `products` | Buyable items (Component Master) | `ProductId` (PK), `ProductType` (1=Generic/L1, 2=Specific/L2), `GenericId` (self-ref), `CategoryId`, `SubCategoryId`, `ItemId`, `MakeId`, `SeriesId`, `SKU` |
| `makes` | OEM brands/manufacturers | `MakeId` (PK), `Name` |
| `series` | OEM product series/families | `SeriesId` (PK), `Name` |
| `attributes` | Attribute definitions | `AttributeId` (PK), `Name`, `DataType` |
| `category_attributes` | Category-attribute assignments | `CategoryAttributeId` (PK), `CategoryId`, `SubCategoryId`, `ItemId`, `AttributeId` |
| `product_attributes` | Product attribute values | `ProductAttributeId` (PK), `ProductId`, `AttributeId`, `Value` |
| `prices` | Commercial rates per product | `PriceId` (PK), `ProductId` (FK), `Rate`, `EffectiveDate` |

#### MBOM Module (Master BOM)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `master_boms` | Master BOM templates | `MasterBomId` (PK), `Name` |
| `master_bom_items` | Master BOM components | `MasterBomItemId` (PK), `MasterBomId` (FK), `ProductId` (FK, Generic only, ProductType=1) |

#### PBOM Module (Proposal BOM)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `proposal_boms` | Proposal BOM instances | `ProposalBomId` (PK) |
| `proposal_bom_items` | Proposal BOM components | `ProposalBomItemId` (PK), `ProposalBomId` (FK), `ProductId` (FK) |

#### QUO Module (Quotation)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `quotations` | Quotation headers | `QuotationId` (PK) |
| `quotation_sales` | Panels | `QuotationSaleId` (PK), `QuotationId` (FK) |
| `quotation_sale_boms` | Feeders/BOMs | `QuotationSaleBomId` (PK), `QuotationSaleId` (FK) |
| `quotation_sale_bom_items` | BOM components | `QuotationSaleBomItemId` (PK), `QuotationSaleBomId` (FK), `ProductId` (FK) |

### 2.4 Key Data Model Concepts

#### ProductType Enumeration
- **ProductType = 1:** Generic Product (L1, template product, no Make/Series)
  - Used in Master BOMs only
  - Can have Specific variants (ProductType=2) via `GenericId` self-reference
- **ProductType = 2:** Specific Product (L2, concrete product with Make/Series/SKU)
  - Used in Proposal/Quotation BOMs
  - Must link to Generic via `GenericId`

#### L0/L1/L2 Resolution Levels
- **L0:** Generic placeholder (text descriptor only, no ProductId)
- **L1:** Generic Product (ProductType=1, defined in `products` table)
- **L2:** Specific Product (ProductType=2, defined in `products` table with Make/Series)

#### Multi-SKU per Line Item
- **ACB + UV/OV add-ons:** Multiple SKUs can be associated with a single line item
- **Make-wise bundling vs separate SKU:** Business rule determines if bundled or separate

#### BOM Editability + History Rule
- **Copy/reuse must stay editable:** When BOM is copied/reused, it becomes editable
- **Backup retained:** Original BOM is preserved as backup/history

### 2.5 Import Template (CSV Headers)

**Source:** `features/component_item_master/import_export/guides/22_DATA_IMPORT_FLOW.md`

#### Product Import Template

**Required Columns:**
- `Category` (Required)
- `Generic` (Required - Generic Product Name)

**Optional Columns:**
- `SubCategory`
- `Item`
- `SKU`
- `Make`
- `Series`
- `Description`

**Example Row:**
```
Category | SubCategory | Item | Generic | SKU | Make | Series | Description
Electrical Panels | Distribution | Indoor | Panel Enclosure 100A | PE-100A-IN | Siemens | SIVACON S8 | Indoor Panel 100A IP54
```

#### Price Import Template

**Required Columns:**
- `SKU` OR `Product Name`
- `Rate`
- `Effective Date`

**Example Row:**
```
SKU | Product Name | Rate | Effective Date
PE-100A-IN | Panel Enclosure 100A | 800.00 | 2022-07-01
```

### 2.6 Sample JSON Structure (Inferred from Model)

**Generic Product (L1):**
```json
{
  "ProductId": 501,
  "Name": "MCCB 100A Standard",
  "ProductType": 1,
  "CategoryId": 10,
  "SubCategoryId": 25,
  "ItemId": 50,
  "GenericId": null,
  "MakeId": null,
  "SeriesId": null,
  "SKU": null,
  "UOM": "Pcs"
}
```

**Specific Product (L2):**
```json
{
  "ProductId": 502,
  "Name": "Acti9 iC60N 100A",
  "ProductType": 2,
  "CategoryId": 10,
  "SubCategoryId": 25,
  "ItemId": 50,
  "GenericId": 501,
  "MakeId": 5,
  "SeriesId": 8,
  "SKU": "A9N61616",
  "UOM": "Pcs"
}
```

**L1→L2 Explosion Example:**
```json
{
  "LineItemId": 1001,
  "ProductId": 501,
  "ProductType": 1,
  "Quantity": 12,
  "ExplodedSKUs": [
    {
      "ProductId": 502,
      "SKU": "A9N61616",
      "Quantity": 6,
      "IsAddOn": false
    },
    {
      "ProductId": 503,
      "SKU": "UV-ADDON-100A",
      "Quantity": 6,
      "IsAddOn": true,
      "ParentSKU": "A9N61616"
    }
  ]
}
```

### 2.7 Schema Status

**Current State:**
- ✅ **Canonical model defined** in `ITEM_MASTER_DETAILED_DESIGN.md`
- ⏳ **Schema extraction pending** in `project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` (template only)
- ✅ **Import templates documented** in import guides
- ✅ **Business rules captured** in governance documents

**Phase-5 Deliverables (To Be Created):**
- `NSW_DATA_DICTIONARY_v1.0.md` (Step 1 output - FROZEN)
- `NSW_SCHEMA_CANON_v1.0.md` (Step 2 output - FROZEN)
- ER Diagram (Step 2 output)

---

## 🔗 Integration Points

### Pending Upgrades Integration

**Reference:** `docs/PHASE_5/02_FREEZE_GATE/PHASE_5_PENDING_UPGRADES_INTEGRATION.md`

This document maps pending upgrade requirements to Phase-5 steps:
- **Step 1:** BOM tracking semantics, CostHead entity, AI entities, validation rules
- **Step 2:** BOM tracking fields, CostHead tables, AI tables, IsLocked fields, audit tables

### Two Truth Layers Rule

**Reference:** Phase-4 vs Phase-5 split documentation

- **Phase-4 Layer:** Legacy-compatible, transitional
- **Phase-5 Layer:** Canonical, clean definitions

### Master Data Governance

**Reference:** `docs/PHASE_5/00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md`

**Key Rules:**
1. **No Auto-Create Masters Rule** - Prevents category/subcategory/item explosion
2. **Import Approval Queue Policy** - Unknown masters require human approval
3. **Canonical Resolver Rules** - Imports must match canonical entities

---

## ✅ Readiness Checklist

- [x] Phase-5 document index compiled
- [x] Current canonical data model identified
- [x] Import templates documented
- [x] Sample JSON structures inferred
- [x] Integration points mapped
- [ ] **Next:** Phase-5 Readiness Review (1 page)
- [ ] **Next:** SPEC-5 stepwise execution in Cursor

---

**Last Updated:** 2025-01-27  
**Status:** Ready for Phase-5 Readiness Review

