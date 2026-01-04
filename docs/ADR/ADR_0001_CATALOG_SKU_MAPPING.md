# ADR-0001: Catalog + SKU Mapping Strategy

**Status:** APPROVED  
**Date:** 2025-12-26  
**Context:** Multi-SKU reality in legacy system  
**Decision:** Canonical SKU mapping and import strategy

---

## Context

The legacy system has a critical reality that must be handled correctly from the start:

> **"One L1 can map to multiple SKUs; some makes bundle addons in main SKU; some have separate SKUs."**

This means:
- A single catalog item (L1) can explode into multiple SKUs
- Some manufacturers bundle addons into the main SKU
- Some manufacturers use separate SKUs for addons
- Price lists are **SKU-level truth**, not item-level truth
- BOM explosion must handle multi-SKU → multi-line-items correctly

**Problem:** If we don't model this correctly from the start, we'll have to rewrite import logic and BOM explosion later.

---

## Decision

We will implement a **SKU-centric catalog model** with explicit SKU types and clear mapping rules.

---

## SKU Types

### PRIMARY
- The main SKU for a catalog item
- Always present when item is used
- Has base price

### BUILT_IN
- Addon bundled into the main SKU
- Price is included in PRIMARY SKU price
- Not a separate line item
- Example: "Switch with built-in indicator"

### ADDON
- Optional addon that can be added
- Separate SKU, separate line item
- Has its own price
- Example: "Additional indicator light"

### OPTIONAL
- Optional component that may or may not be included
- Separate SKU if included
- Separate line item if included
- Example: "Optional mounting bracket"

### MANDATORY_SPLIT
- Required component that must be a separate SKU
- Always creates separate line item
- Always included in BOM explosion
- Example: "Main unit + separate power supply (mandatory)"

---

## Data Model Rules

### Rule 1: L1 → Explodes into One or More Priced Lines

**Rule:** When a catalog item (L1) is used in a BOM, it explodes into one or more quotation line items based on its SKU mapping.

**Implementation:**
- Catalog item has one PRIMARY SKU (always)
- Catalog item may have zero or more additional SKUs (BUILT_IN, ADDON, OPTIONAL, MANDATORY_SPLIT)
- BOM explosion logic checks SKU type to determine line item creation

**Example:**
```
L1: "Panel Switch"
  - PRIMARY: "SW-123" ($100)
  - BUILT_IN: "LED-IND" (included, no separate line)
  - ADDON: "EXT-BRACKET" ($20, optional, separate line if added)
  - MANDATORY_SPLIT: "PSU-5V" ($15, always separate line)

BOM Explosion Result:
  Line 1: SW-123 ($100) - includes LED-IND
  Line 2: PSU-5V ($15) - mandatory
  Line 3: EXT-BRACKET ($20) - if optional addon selected
```

---

### Rule 2: Imported Price List is SKU-Level Truth

**Rule:** Price lists are imported at the **SKU level**, not the item level. Each SKU has its own price.

**Implementation:**
- Price import accepts SKU codes and prices
- Price lookup is by SKU code, not item code
- Item-level price is derived from PRIMARY SKU price
- Multiple SKUs for same item can have different prices

**Example:**
```
Price List Import:
  SKU: SW-123 → Price: $100
  SKU: PSU-5V → Price: $15
  SKU: EXT-BRACKET → Price: $20

Catalog Item: "Panel Switch"
  - PRIMARY: SW-123 ($100 from price list)
  - MANDATORY_SPLIT: PSU-5V ($15 from price list)
  - ADDON: EXT-BRACKET ($20 from price list)
```

---

### Rule 3: Multi-SKU Becomes Multiple Quotation Line Items

**Rule:** When a catalog item with multiple SKUs is used, it creates multiple quotation line items based on SKU type rules.

**Line Item Creation Rules:**
- **PRIMARY:** Always creates one line item
- **BUILT_IN:** Never creates separate line item (included in PRIMARY)
- **ADDON:** Creates line item only if explicitly added
- **OPTIONAL:** Creates line item only if included
- **MANDATORY_SPLIT:** Always creates separate line item

**Implementation:**
- BOM explosion logic iterates through SKUs
- Applies line item creation rules based on SKU type
- Aggregates prices correctly (PRIMARY includes BUILT_IN prices)

---

## Database Schema (High-Level)

```
catalog_items
  - id
  - item_code (L1 code)
  - name
  - description
  - ...

catalog_skus
  - id
  - catalog_item_id (FK)
  - sku_code
  - sku_type (PRIMARY, BUILT_IN, ADDON, OPTIONAL, MANDATORY_SPLIT)
  - name
  - description
  - is_active
  - ...

sku_prices
  - id
  - sku_id (FK)
  - price_list_id (FK)
  - price
  - effective_date
  - ...

price_lists
  - id
  - name
  - effective_date
  - ...
```

---

## Import Workflow

### Step 1: Import Catalog Items
- Import items with their basic information
- Create catalog_items records

### Step 2: Import SKU Mappings
- Import SKU codes and their types
- Link SKUs to catalog items
- Create catalog_skus records

### Step 3: Import Price List
- Import prices by SKU code (not item code)
- Create sku_prices records linked to price_list
- Validate all SKUs have prices (or mark as missing)

### Step 4: Validation
- Ensure every catalog item has exactly one PRIMARY SKU
- Ensure all PRIMARY SKUs have prices
- Warn about missing prices for optional SKUs

---

## BOM Explosion Logic (Future)

When exploding a BOM:

1. For each BOM line item referencing a catalog item:
   - Get all SKUs for that catalog item
   - Filter by SKU type rules:
     - PRIMARY → always include
     - BUILT_IN → include (but don't create separate line)
     - MANDATORY_SPLIT → always include as separate line
     - ADDON/OPTIONAL → include only if selected
   - Create quotation line items accordingly
   - Aggregate prices (PRIMARY + BUILT_IN prices together)

2. Price calculation:
   - PRIMARY SKU price + all BUILT_IN SKU prices = base line item price
   - Each MANDATORY_SPLIT SKU = separate line item with its price
   - Each ADDON/OPTIONAL SKU (if included) = separate line item with its price

---

## Consequences

### Positive
- ✅ Handles multi-SKU reality correctly from the start
- ✅ Clear separation between item-level and SKU-level data
- ✅ Price lists are SKU-centric (matches reality)
- ✅ BOM explosion logic is straightforward
- ✅ No need to rewrite import logic later

### Negative
- ⚠️ More complex initial schema (but necessary)
- ⚠️ Import workflow has multiple steps (but clear)
- ⚠️ Need to validate SKU mappings during import

### Risks Mitigated
- ✅ Prevents "one item = one SKU" assumption
- ✅ Prevents "price at item level" assumption
- ✅ Prevents BOM explosion rewrite later

---

## Implementation Sequence

1. **Create database schema** (catalog_items, catalog_skus, sku_prices, price_lists)
2. **Implement catalog item import** (basic item data)
3. **Implement SKU mapping import** (item → SKU relationships with types)
4. **Implement price list import** (SKU-level prices)
5. **Implement validation** (ensure PRIMARY SKUs exist and have prices)
6. **Implement BOM explosion** (multi-SKU → multi-line-items)

---

## References

- Legacy system analysis: Multi-SKU reality identified
- Phase 5 fundamentals: Deterministic engine principle
- BOM explosion requirements: L1 → L2, multi-SKU → multi-line-items

---

## Change Log

- **v1.0 (2025-12-26):** Initial ADR created to establish SKU mapping strategy

---

**END OF ADR-0001**

