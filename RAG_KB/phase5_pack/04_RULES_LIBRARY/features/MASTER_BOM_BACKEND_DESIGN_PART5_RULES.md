---
Source: features/master_bom/validation/MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T01:38:50.659499
KB_Path: phase5_pack/04_RULES_LIBRARY/features/MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md
---

> Source: source_snapshot/MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md
> Bifurcated into: features/master_bom/validation/MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md
> Module: Master BOM > Validation
> Date: 2025-12-17 (IST)

# Master BOM Backend Design - Part 5: Business Rules & Validation

**Document:** MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes all business rules, validation rules, and constraints for the Master BOM module.

---

## 🔒 Protected Rules

### Rule 1: Copy Rule (Non-Negotiable)

**Rule:** Always copy Master BOM, never link directly

**Implementation:**
- When adding Master BOM to quotation, copy all items
- Create new `QuotationSaleBom` and `QuotationSaleBomItem` records
- Set `MasterBomId` for reference only (not for linking)
- Changes to Master BOM don't affect existing quotations

**Status:** 🔴 **NON-NEGOTIABLE**

---

### Rule 2: Generic Products Only

**Rule:** Master BOM items must reference generic products only

**Implementation:**
- MasterBomItem.ProductId must point to ProductType = 1 (Generic)
- No Make/Series in master BOM items
- Validation: Check ProductType when adding items

**Validation:**
```php
$product = Product::find($productId);
if ($product->ProductType != 1) {
    return response()->json([
        'error' => 'Master BOM items must use generic products only'
    ], 422);
}
```

---

### Rule 3: Template Quantities

**Rule:** Master BOM contains template quantities

**Implementation:**
- MasterBomItem.Quantity is template quantity
- When copied to quotation, quantity is copied
- User can modify quantity in quotation

**Business Logic:**
- Template quantity provides default
- Not enforced in quotation (can be changed)

---

## ✅ Validation Rules

### Master BOM Creation Rules

**Required Fields:**
- `Name` - Master BOM name (required, max 255 characters)

**Optional Fields:**
- None (simple structure)

**Validation:**
```php
[
    'Name' => 'required|string|max:255',
]
```

---

### Master BOM Item Creation Rules

**Required Fields:**
- `MasterBomId` - Must exist in master_boms table
- `ProductId` - Must exist in products table, must be Generic (ProductType = 1)
- `Quantity` - Must be numeric, must be > 0

**Validation:**
```php
[
    'MasterBomId' => 'required|integer|exists:master_boms,MasterBomId',
    'ProductId' => 'required|integer|exists:products,ProductId',
    'Quantity' => 'required|numeric|min:0.01',
]
```

**Custom Validation:**
```php
// Check ProductType
$product = Product::find($request->ProductId);
if ($product->ProductType != 1) {
    return response()->json([
        'error' => 'Master BOM items must use generic products only'
    ], 422);
}
```

---

## 🚫 Constraints

### Database Constraints

**master_boms Table:**
- PRIMARY KEY (MasterBomId)
- UNIQUE constraint on Name (if implemented)

**master_bom_items Table:**
- PRIMARY KEY (MasterBomItemId)
- FOREIGN KEY (MasterBomId) REFERENCES master_boms(MasterBomId)
- FOREIGN KEY (ProductId) REFERENCES products(ProductId)

---

### Application Constraints

**Product Type Constraint:**
- MasterBomItem.ProductId must reference ProductType = 1 (Generic)
- Enforced at application level (validation)

**Quantity Constraint:**
- MasterBomItem.Quantity must be > 0
- Enforced at validation level

---

## 📝 Business Rules

### Rule 1: Master BOM Name Required

**Rule:** Master BOM must have a name

**Implementation:**
- Name is required
- Must be descriptive
- Should be unique (for easy identification)

---

### Rule 2: Master BOM Can Have Multiple Items

**Rule:** One master BOM can have multiple items

**Implementation:**
- No limit on number of items
- Items can be added/removed
- Items can be reordered (if UI supports)

---

### Rule 3: Master BOM Items Reference Generic Products

**Rule:** Items must reference generic products only

**Implementation:**
- ProductId must point to ProductType = 1
- No Make/Series selection in master BOM
- Make/Series selected when copying to quotation

---

### Rule 4: Template Quantities

**Rule:** Quantities are templates, not fixed

**Implementation:**
- Quantity copied to quotation
- Can be modified in quotation
- Provides starting point only

---

### Rule 5: Soft Delete

**Rule:** Use Status column for soft delete

**Implementation:**
- Status = 0 (Active)
- Status = 1 (Deleted)
- Filter by Status = 0 when loading

**Note:** Check if soft delete is implemented or hard delete is used

---

## 🔍 Deletion Rules

### Master BOM Deletion

**Rule:** Can delete master BOM if no active items

**Implementation:**
```php
// Check if master BOM has items
$items = MasterBomItem::where('MasterBomId', $masterBomId)
    ->where('Status', 0)
    ->count();

if ($items > 0) {
    // Option 1: Prevent deletion
    return response()->json(['error' => 'Cannot delete - has items'], 422);
    
    // Option 2: Soft delete items first
    MasterBomItem::where('MasterBomId', $masterBomId)->update(['Status' => 1]);
}

// Delete master BOM
MasterBom::where('MasterBomId', $masterBomId)->update(['Status' => 1]);
```

**Business Logic:**
- Check for active items
- If items exist, either prevent deletion or soft delete items first
- Then soft delete master BOM

---

### Master BOM Item Deletion

**Rule:** Can delete item from master BOM

**Implementation:**
```php
// Soft delete item
MasterBomItem::where('MasterBomItemId', $itemId)
    ->update(['Status' => 1]);
```

**Impact:**
- Item removed from master BOM
- Existing Proposal BOMs not affected (already copied)

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial business rules document | Part 5 of Master BOM backend design series |

---

**Previous:** [Part 4: Master BOM to Proposal BOM Copy Process](MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md)  
**Next:** [Part 6: Backend Services & Controllers](MASTER_BOM_BACKEND_DESIGN_PART6_SERVICES.md)

