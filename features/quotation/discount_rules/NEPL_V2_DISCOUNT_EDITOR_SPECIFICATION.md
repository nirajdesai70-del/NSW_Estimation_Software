> Source: source_snapshot/NEPL_V2_DISCOUNT_EDITOR_SPECIFICATION.md
> Bifurcated into: features/quotation/discount_rules/NEPL_V2_DISCOUNT_EDITOR_SPECIFICATION.md
> Module: Quotation > Discount Rules
> Date: 2025-12-17 (IST)

# NEPL V2 – Discount Editor Specification

**Date:** December 2025  
**Status:** ✅ Approved  
**Purpose:** Ensure we never lose the core requirement for bulk discount handling in V2.

---

## 🔥 Background / Problem

The current Structure tab is extremely heavy (large DOM, nested BOMs) and becomes slow or unresponsive.

But it contains a critical business function: applying bulk discounts across many items based on:

- Make
- Category
- Product Type / Item
- Attribute
- Description
- Specific SKU
- Panel / Feeder / BOM

**This MUST remain in the system, but it cannot stay inside the heavy Structure tab.**

---

## 🎯 Goal

Create a dedicated, fast, filter-based V2 Discount Editor to replace discount operations currently happening in Structure tab.

This will allow discount rules to be applied across hundreds of items in seconds.

---

## 📌 Requirements (Must-Have)

### 1. New Screen: "Discount Editor"

- **Route:** `/quotation/{id}/discount`
- **Access from:**
  - Quotation List page
  - V2 Panel View header ("Edit Discounts")

---

### 2. Filter Panel (top of screen)

User can filter all BOM items by:

- Make (multi-select)
- Category
- Product Type / Item
- Attribute
- Description ("contains")
- SKU / Product Id
- Panel
- Feeder (optional)
- BOM (optional)

**Buttons:**
- Apply Filters
- Clear Filters

---

### 3. Results Grid (middle section)

Use **NEPL standard table component** `<x-nepl-table>`.

**Columns:**
- Panel
- Feeder
- BOM
- Item Name / Description
- Make
- Category
- Qty
- Rate
- Current Discount
- Current Net Rate
- Amount
- Checkbox (for selective application)

**NEPL Table Pattern:**
- Top-left: Show entries
- Top-right: Search box
- Bottom-left: Showing X to Y of Z
- Bottom-right: Pagination

---

### 4. Discount Rule Block (bottom section)

**Parameters:**
- Rule Type: Percentage (Phase 1), Flat (Phase 2)
- Discount Value: Numeric input
- Apply To:
  - All filtered rows
  - Only selected rows

**Buttons:**
- Preview (calculate changes locally)
- Apply & Save (writes to DB)

**Preview should show:**
- X rows affected
- Total discount change
- New total quotation amount

---

### 5. Backend Requirements

When user applies discount:

- Query `quotation_sale_bom_items` using filters
- Restrict to selected rows if needed
- For each row:
  ```
  NewDiscount = Input %
  NetRate = Rate - (Rate * Discount%)
  Amount = NetRate * Qty
  ```
- Update all rows in a transaction
- Recalculate quotation totals
- Return updated grid + success message

**Reuses logic from:**
- `QuotationController@changediscount()`

---

### 6. Long-Term Goal

- Structure tab becomes read-only summary
- Discount operations fully moved to Discount Editor
- Performance + usability drastically improved

---

## ⭐ Final Note

**"Discount Editor is the long-term replacement for all discount handling inside Structure tab. Structure tab will become summary-only after this implementation."**

---

## 📚 Related Documents

- `NEPL_TABLE_COMPONENT_PLAN.md` - Standard table component specification
- `NEPL_STANDARD_LIST_PATTERN.md` - Standard list pattern requirements
- `NEPL_TABLE_COMPONENT_IMPLEMENTATION.md` - Implementation details

---

## 🔖 Tags

#discount-editor #v2 #bulk-discount #structure-tab-replacement #performance #filter-based #quotation-management
