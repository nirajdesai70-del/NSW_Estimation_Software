> Source: source_snapshot/NEPL_MASTER_COMPONENT_CATALOG_MODEL_V1.1.md
> Bifurcated into: features/component_item_master/NEPL_MASTER_COMPONENT_CATALOG_MODEL_V1.1.md
> Module: Component / Item Master > General
> Date: 2025-12-17 (IST)

# NEPL Master Component & Catalog Model

**Version:** v1.1 (Operational Master Document)  
**Date:** December 2025  
**Status:** 🔴 **STANDING INSTRUCTION - PERMANENT STANDARD**

**Scope:** Category/SubCategory/Type(ProductType) + Attributes + Product Master + Make/Series + Pricelist + V2 BOM Lines

**Purpose:** Single source of truth for component taxonomy, product creation, pricing, and V2 usage.

---

## 🎯 STANDING INSTRUCTION

**This document is a PERMANENT STANDARD** that must be followed for:
- ✅ All component/product management
- ✅ All V2 BOM operations
- ✅ All catalog building
- ✅ All AI/automation work
- ✅ All future development

**See also:** `STANDING_INSTRUCTIONS.md` for complete list of permanent project rules.

---

## 1) Non-negotiable Ground Rules

### R1 — Two separate concepts exist

1. **Catalog Product (Product Master)** = buyable part (can be priced)
   - Stored in: `products` table
   - Has: CategoryId, TypeId(ItemId), MakeId, SeriesId, SKU, Attributes, Price

2. **V2 BOM Line (QuotationSaleBomItem)** = usage row referencing a ProductId at a specific tree location
   - Stored in: `quotation_sale_bom_items` table
   - Has: ProductId (reference), Qty, Rate, Discount, NetRate, Amount
   - **Not a master** - only a usage record

---

### R2 — Taxonomy drives everything

- **Category + SubCategory + Type(ProductType)** define what it is
- **Attributes** define what it must satisfy
- **Make/Series** define vendor family
- **Price list** defines commercial rate

---

### R3 — Do not mix generic placeholders with priced catalog

- Generic placeholders are allowed (future L0/L1)
- **Pricing and totals are valid only with a real ProductId (L2)**

---

### R4 — Costing Contract is permanent

**From V2_FINAL_COSTING_SPECIFICATION.md:**
- `AmountTotal = NetRate × TotalQty`
- Roll-ups = `SUM(AmountTotal)` only
- **No extra multipliers at rollup levels**

**This rule is NON-NEGOTIABLE and protected by `CAREFUL_CHANGE_PROTOCOL.md`**

---

## 2) Correct Naming (Permanent Terms)

### 2.1 Current DB objects (as-is)

| Term | Database Table | Notes |
|------|----------------|-------|
| Category | `categories` | Top-level classification |
| SubCategory | `sub_categories` | Sub-classification |
| Type / ProductType | `items` | Currently used as "Type" - functional classification |
| Product Master / Item Master / Component Master | `products` | **This is your "Component Master"** |
| Make | `makes` | OEM brand |
| Series | `series` | OEM family under make |
| Price List | `prices` | Commercial rates |

### 2.2 V2 objects

- `quotation_sale_bom_items` = **component usage rows**
- **Not a master** - only references ProductId
- Must reference ProductId (unless later L0/L1 staging is introduced)

✅ **Therefore:** Your "Component Master" is the **PRODUCTS table**, and "component line" is only a usage record.

---

## 3) Correct Hierarchy & Keys

### 3.1 Master data hierarchy

```
Category → SubCategory → Type(ProductType) → Product
```

**Level Definitions:**
- **Category:** broad family (Protection, Switching, Metering, etc.)
- **SubCategory:** subgroup (MCCB, MCB, Contactor, VFD, etc.)
- **Type/ProductType:** functional usage (MCCB Feeder, MCCB Incomer, Lamp, Pushbutton, etc.)
- **Product:** actual purchasable part tied to Make/Series and price

### 3.2 Attribute mapping rule (most important)

**Rule:**
- **Attribute definition** belongs to **Type(ProductType)**
- **Attribute values** belong to **Product (ProductId)**

**Implementation:**
- `category_attributes` (with Type scope) = schema definition
- `product_attributes` = actual values per product

---

## 4) Product Master Must Be Visible (UI)

### 4.1 Product Master location

- **Table:** `products`
- **UI screens:**
  - Generic Product Master (`/generic`)
  - Specific Product Master (`/product`)

### 4.2 Sidebar grouping (required)

**Create sidebar group:**

```
COMPONENT / ITEM MASTER
  ├── Category
  ├── SubCategory
  ├── Product Type (Item)
  ├── Attributes
  ├── Make
  ├── Series
  ├── Generic Product Master
  ├── Specific Product Master
  ├── Price List
  └── Import/Export
```

**This removes 80% confusion for users.**

---

## 5) Standard Product/Component Creation Workflow (Operational)

### Step 1 — Taxonomy setup (once per type)

1. Create Category
2. Create SubCategory
3. Create Type (ProductType)
4. Map Attributes to Type (schema)

### Step 2 — Create Make & Series

- **Make** = OEM brand
- **Series** = OEM family under that make

**Validation:** Series cannot exist without Make.

### Step 3 — Create Product Master (Catalog Product)

**Minimum required fields:**
- `CategoryId` (required)
- `TypeId` (ItemId/ProductTypeId) **required**
- `MakeId/SeriesId` (if used)
- `SKU` / `ModelNo` / `Description`
- Attribute values (`product_attributes`) as per schema

### Step 4 — Add Price

- Price row in `prices` table:
  - `ProductId` + `EffectiveDate` + `Rate`
- V2 pulls latest effective rate unless override allowed via `RateSource`.

---

## 6) V2 Interlink Contract (How V2 must use catalog master)

### 6.1 Adding item into V2 BOM lines

**In V2 Add Item Modal:**

**Filter dropdown using:**
1. Category → SubCategory → Type(ProductType)
2. Show Make + Series filters (optional)
3. Then select ProductId (final)

**Rule:** V2 BOM item must reference ProductId (for current L2-only workflow).

### 6.2 Make/Series usage in V2

**Two valid patterns (choose one default and keep consistent):**

- **Pattern A (recommended):** Make/Series derived from Product Master only
- **Pattern B:** Make/Series selectable per BOM item line (but must still map to ProductId)

### 6.3 Pricing pull rule

**When ProductId selected:**

1. Look up price:
   - Latest effective price for that ProductId
2. Set:
   - `RateSource` = `PRICELIST`
   - `Rate` = fetched rate
   - Allow override if permission exists (`RateSource` = `MANUAL`)

---

## 7) Resolution Model Alignment (Future-proof, no rebuild)

### Phase A (current)

- All V2 BOM lines are **L2** (ProductId-based, priced/priceable)

### Phase B (next)

**Add on `quotation_sale_bom_items`:**
- `ResolutionStatus` (L0/L1/L2)
- `DefinedSpecJson` (L1)
- `IsPriceMissing` flag (required)

**Rules:**
- L0/L1 → `AmountTotal=0` and flagged incomplete
- L2 → `AmountTotal` uses standard V2 costing contract

### Phase C (optional clean separation)

Add `generic_components` later if required. Not mandatory now.

---

## 8) UI Views (Prevent confusion by separation)

### 8.1 Master screens (catalog building)

Category/SubCategory/Type/Attributes/Make/Series/Product/Price

### 8.2 V2 Engineering View (tree)

- Structure + quantities
- Minimal commercial fields
- No consolidation

### 8.3 V2 Pricing View

- Quantities + Rate/Discount/NetRate/Amount
- Bulk discount tools
- Missing price flags

### 8.4 Costing pack/export

**Consolidation key:**
```
ProductId + MakeId + SeriesId + RateSource + IsClientSupplied
(+ Description only if variants are differentiated by description)
```

---

## 9) Logic Contract: Category/SubCategory/Type drives behaviour

### 9.1 Validation rules

- Product must have Type(ProductTypeId)
- Product must satisfy required attributes for that Type
- Type-specific constraints can be added later (IEC rule checks)

### 9.2 Suggestion hooks (for AI later)

- Co-occurrence and substitution should anchor at:
  - **TypeId** primarily (stable)
  - **ProductId** secondarily (exact part)

---

## 10) Glossary (1-liners)

- **Type(ProductType):** functional classification used for schema + filtering
- **Product Master:** buyable item + make/series + attributes + pricing
- **Component line (V2):** usage row referencing ProductId under a BOM node
- **Generic placeholder (future):** unresolved line without product pricing

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-12 | User | Initial draft | Structural foundation |
| 1.1 | 2025-12-12 | Auto | Registered as permanent standard | Added standing instruction status, tightened definitions, added interlink contracts |

---

**END OF STANDARD**

**This is now a PERMANENT STANDARD for all component/catalog work.**
