# Data Semantics Lock - Entity Definitions

**Purpose:** Define what each entity means before mapping any field. This prevents "semantic drift" where same field names have different meanings.

**Status:** ⏳ In Progress  
**Date Created:** 2025-12-18  
**Last Updated:** 2025-12-18

---

## 🎯 Critical Rule

**Before mapping any field, we must define what each entity means.**

This document locks the semantic definitions to prevent wrong mapping decisions.

---

## 📋 Core Entity Definitions

### 1. Product / Item / Component Hierarchy

#### **Product**
- **Definition:** A catalog entry that can be used in BOMs. Can be Generic (L1) or Specific (L2).
- **Types:**
  - **Type 1 (Generic):** Template product without Make/Series. Used as parent for variants.
  - **Type 2 (Specific):** Concrete product with Make/Series. Used in actual BOMs.
- **Layers:**
  - **L0 (Generic):** Base product without attributes
  - **L1 (Generic):** Product with Category/Subcategory/Type/Attributes, but no Make/Series
  - **L2 (Specific):** Product with Make/Series, ready for use in BOMs
- **Key Fields:**
  - `ProductType` (1=Generic, 2=Specific)
  - `GenericId` (self-reference for L2 → L1 link)
  - `CategoryId`, `SubCategoryId`, `ItemId`
  - `MakeId`, `SeriesId` (only for Type 2)

#### **Item (Product Type)**
- **Definition:** Classification level below Subcategory. Defines the "type" of product (e.g., "MCB", "RCCB", "Panel").
- **Relationship:** Category → Subcategory → Item → Product
- **Usage:** Used for filtering and grouping products

#### **Component**
- **Definition:** A product that appears in a BOM (Master BOM or Proposal BOM).
- **Relationship:** Component is a Product used in a BOM context
- **Key Distinction:** Product is catalog, Component is usage

---

### 2. BOM Hierarchy

#### **Master BOM**
- **Definition:** Template BOM structure. Contains L1 (Generic) products only.
- **Purpose:** Reusable template for creating Proposal BOMs
- **Key Fields:**
  - `MasterBomId` (PK)
  - `Name`, `UniqueNo`
  - `ProductId` (must be L1/Generic, NOT L2/Specific)
- **Relationships:**
  - `master_bom_items` → `products` (L1 only)

#### **Proposal BOM**
- **Definition:** Instance BOM created from Master BOM. Contains L2 (Specific) products.
- **Purpose:** Actual BOM used in quotations/projects
- **Key Fields:**
  - `ProposalBomId` (PK)
  - `MasterBomId` (FK to master template)
  - `ProductId` (must be L2/Specific, NOT L1/Generic)
- **Relationships:**
  - `proposal_bom_items` → `products` (L2 only)
  - `proposal_boms` → `master_boms` (template link)

#### **BOM Item**
- **Definition:** A single line item in a BOM (Master or Proposal).
- **Key Fields:**
  - `Quantity`
  - `ProductId` (L1 for Master, L2 for Proposal)
  - `Amount`, `Rate`, `Discount`
- **Relationships:**
  - `master_bom_items` → `master_boms`
  - `proposal_bom_items` → `proposal_boms`

---

### 3. Quotation Hierarchy

#### **Quotation**
- **Definition:** Commercial document containing panels and pricing.
- **Key Fields:**
  - `QuotationId` (PK)
  - `QuotationNo` (unique identifier)
  - `ClientId` (FK)
  - `Status` (draft, sent, approved, etc.)
- **Relationships:**
  - `quotations` → `clients`
  - `quotations` → `quotation_sales` (panels)

#### **Panel (QuotationSale)**
- **Definition:** Top-level container in a quotation. Contains feeders/BOMs.
- **V2 Structure:** Panel → Feeder → BOM L1 → BOM L2 → Components
- **Key Fields:**
  - `QuotationSaleId` (PK)
  - `QuotationId` (FK)
  - `Name` (panel name)
  - `Level` (0 = Panel, 1 = Feeder, 2 = BOM L1, 3 = BOM L2)
- **Relationships:**
  - `quotation_sales` → `quotations`
  - `quotation_sales` → `quotation_sale_boms` (feeders/BOMs)

#### **Feeder / BOM (QuotationSaleBom)**
- **Definition:** Feeder (Level 1) or BOM (Level 2) within a panel.
- **V2 Structure:**
  - **Level 1 (Feeder):** Container for BOMs
  - **Level 2 (BOM):** Container for components
- **Key Fields:**
  - `QuotationSaleBomId` (PK)
  - `QuotationSaleId` (FK to panel)
  - `ParentBomId` (self-reference for BOM hierarchy)
  - `Level` (1 = Feeder, 2 = BOM)
  - `FeederName`, `BomName`
- **Relationships:**
  - `quotation_sale_boms` → `quotation_sales` (panel)
  - `quotation_sale_boms` → `quotation_sale_bom_items` (components)

#### **Component Item (QuotationSaleBomItem)**
- **Definition:** A product/component in a quotation BOM.
- **Key Fields:**
  - `QuotationSaleBomItemId` (PK)
  - `QuotationSaleBomId` (FK to BOM)
  - `ProductId` (FK to products, must be L2/Specific)
  - `Quantity`, `Rate`, `Amount`, `Discount`
- **Relationships:**
  - `quotation_sale_bom_items` → `quotation_sale_boms`
  - `quotation_sale_bom_items` → `products` (L2 only)

---

### 4. Master Data Hierarchy

#### **Category**
- **Definition:** Top-level product classification (e.g., "Electrical Panels", "Cables").
- **Key Fields:**
  - `CategoryId` (PK)
  - `Name`
- **Relationships:**
  - `categories` → `sub_categories`
  - `categories` → `products`

#### **Subcategory**
- **Definition:** Second-level classification under Category (e.g., "Distribution Panels", "Control Panels").
- **Key Fields:**
  - `SubCategoryId` (PK)
  - `CategoryId` (FK)
  - `Name`
- **Relationships:**
  - `sub_categories` → `categories`
  - `sub_categories` → `items`
  - `sub_categories` → `products`

#### **Item (Product Type)**
- **Definition:** Third-level classification (e.g., "MCB", "RCCB", "Panel Board").
- **Key Fields:**
  - `ItemId` (PK)
  - `SubCategoryId` (FK)
  - `Name`
- **Relationships:**
  - `items` → `sub_categories`
  - `items` → `products`

#### **Make**
- **Definition:** Manufacturer brand (e.g., "Siemens", "ABB", "Schneider").
- **Key Fields:**
  - `MakeId` (PK)
  - `Name`
- **Relationships:**
  - `makes` → `series`
  - `makes` → `products` (via MakeId)

#### **Series**
- **Definition:** Product series under a Make (e.g., "SIVACON S8", "SIMARIS").
- **Key Fields:**
  - `SeriesId` (PK)
  - `MakeId` (FK)
  - `Name`
- **Relationships:**
  - `series` → `makes`
  - `series` → `products` (via SeriesId)

---

### 5. Project Hierarchy

#### **Project**
- **Definition:** Client project containing quotations or direct panels (V2).
- **Key Fields:**
  - `ProjectId` (PK)
  - `ProjectNo` (unique identifier)
  - `ClientId` (FK)
  - `Name`, `Location`
- **Relationships:**
  - `projects` → `clients`
  - `projects` → `quotations` (legacy)
  - `projects` → `quotation_sales` (V2 direct panels)

#### **Project Panel (V2)**
- **Definition:** Direct panel in a project (V2 structure, bypasses quotation).
- **Key Fields:**
  - `QuotationSaleId` (PK, same table as quotation panels)
  - `ProjectId` (FK, nullable)
  - `QuotationId` (NULL for V2 projects)
- **Note:** Uses same `quotation_sales` table with `ProjectId` instead of `QuotationId`

---

### 6. Pricing and Commercial

#### **Price List**
- **Definition:** Master pricing data for products.
- **Key Fields:**
  - `PriceListId` (PK)
  - `ProductId` (FK)
  - `Rate` (unit price)
  - `EffectiveDate`
- **Relationships:**
  - `price_lists` → `products`

#### **Discount Rule**
- **Definition:** Rule for applying discounts to quotation items.
- **Key Fields:**
  - `DiscountRuleId` (PK)
  - `ScopeType` (GLOBAL, MAKE, MAKE_SERIES, PRODUCT_TYPE, PRODUCT)
  - `ScopeId` (FK to scope entity)
  - `Discount` (percentage)
  - `Priority`
- **Relationships:**
  - `quotation_discount_rules` → various scope entities

---

## 🔒 Semantic Lock Rules

### Rule 1: Product Type Consistency
- **L1 (Generic) products** can ONLY appear in Master BOMs
- **L2 (Specific) products** can ONLY appear in Proposal BOMs and Quotation BOMs
- **Violation:** If legacy system has L2 in Master BOM, this is a migration blocker

### Rule 2: BOM Layer Consistency
- **Master BOM** = Template, L1 products only
- **Proposal BOM** = Instance, L2 products only
- **Quotation BOM** = Commercial, L2 products only

### Rule 3: Hierarchy Consistency
- **Category → Subcategory → Item → Product** (master data)
- **Quotation → Panel → Feeder → BOM → Component** (commercial)
- **Project → Panel → Feeder → BOM → Component** (V2 commercial)

### Rule 4: ID Strategy
- **Legacy:** Integer auto-increment IDs
- **NSW:** Integer auto-increment IDs (preserved)
- **Migration:** Old IDs preserved where possible, remapped only if necessary

---

## ⚠️ Known Semantic Drift Risks

### Risk 1: "ProductId" Meaning Mismatch
- **Legacy:** May use ProductId to mean different things (L1 vs L2)
- **NSW:** Strictly L1 for Master BOM, L2 for Proposal/Quotation BOM
- **Mitigation:** Check all legacy BOM tables for ProductType consistency

### Risk 2: "BOM" vs "Feeder" Naming
- **Legacy:** May not distinguish Feeder from BOM
- **NSW:** Clear hierarchy: Panel → Feeder (Level 1) → BOM (Level 2)
- **Mitigation:** Map legacy BOMs to appropriate level based on structure

### Rule 3: Status Code Mismatch
- **Legacy:** May have different status codes/enums
- **NSW:** Standardized status codes
- **Mitigation:** Create status code mapping table

---

## 📝 Mapping Decision Log

| Date | Entity | Legacy Meaning | NSW Meaning | Decision | Risk Level |
|------|--------|---------------|------------|----------|------------|
| 2025-12-18 | Product | TBD | TBD | TBD | TBD |

---

## ✅ Sign-Off

**Semantic definitions locked:** ⏳ Pending  
**Ready for schema extraction:** ⏳ Pending  
**Ready for mapping:** ⏳ Pending

---

**Last Updated:** 2025-12-18  
**Next Review:** After legacy schema extraction

