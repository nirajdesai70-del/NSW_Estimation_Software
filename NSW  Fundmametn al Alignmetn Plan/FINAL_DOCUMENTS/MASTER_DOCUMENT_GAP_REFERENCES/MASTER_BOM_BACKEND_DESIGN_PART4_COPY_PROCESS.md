# Master BOM Backend Design - Part 4: Master BOM to Proposal BOM Copy Process

**Document:** MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md  
**Version:** 1.1  
**Date:** December 2025

---

## 📋 Overview

This document describes the complete process of copying Master BOM to Proposal BOM in quotations. This is a critical process that ensures independence between templates and instances.

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

### L1 → L2 Resolution Process

**Copy Process Layer Flow:**
1. **Source (L1):** Master BOM contains L1 items (Generic products, no Make/Series)
2. **Copy:** L1 items are copied to Proposal BOM (still L1, no Make/Series)
3. **Resolution:** User selects Make/Series → L1 items resolve to L2 (Specific products)
4. **Final State:** Proposal BOM contains L2 items (Specific products with Make/Series/SKU)

**Critical Rule:** Master BOM stays at L1. Proposal BOM must resolve to L2 before finalization.

---

## 🔒 Golden Rule (Non-Negotiable)

**Rule:** Always copy Master BOM, never link directly

**Critical Principles:**
- ✅ Master BOM is copied, not linked
- ✅ Changes to Master BOM don't affect existing Proposal BOMs
- ✅ Each Proposal BOM is independent
- ✅ MasterBomId stored for reference only

---

## 🔄 Copy Process Overview

### High-Level Flow

```
Step 1: User selects Master BOM in quotation
    ↓
Step 2: System loads Master BOM with items
    ↓
Step 3: System creates Proposal BOM header
    ↓
Step 4: System copies all Master BOM items
    ↓
Step 5: User selects Make/Series for each item
    ↓
Step 6: System creates/updates specific products
    ↓
Step 7: System loads prices for specific products
    ↓
Step 8: Proposal BOM ready for use
```

---

## 📊 Step-by-Step Copy Process

### Step 1: Load Master BOM

**Process:**
```php
$masterBom = MasterBom::with('items.product')->find($masterBomId);

// Verify master BOM exists
if (!$masterBom) {
    return response()->json(['error' => 'Master BOM not found'], 404);
}
```

**Data Loaded:**
- Master BOM header (Name, etc.)
- All Master BOM items
- Product information for each item (Generic products)

---

### Step 2: Create Proposal BOM Header

**Process:**
```php
$proposalBom = new QuotationSaleBom();
$proposalBom->QuotationSaleId = $panelId;
$proposalBom->QuotationId = $quotationId;
$proposalBom->MasterBomId = $masterBomId; // REFERENCE ONLY
$proposalBom->MasterBomName = $masterBom->Name; // Copy name
$proposalBom->BomName = $masterBom->Name; // Or custom name
$proposalBom->Level = $requestedLevel; // 1 or 2
$proposalBom->ParentBomId = $parentBomId; // If under another BOM
$proposalBom->Qty = $requestedQty; // BOM quantity
$proposalBom->Status = 0; // Active
$proposalBom->save();
```

**Key Points:**
- MasterBomId stored for reference only
- Name copied from master BOM
- Independent record created
- No link to master BOM (can be deleted independently)

---

### Step 3: Copy Master BOM Items

**Process:**
```php
foreach ($masterBom->items as $masterItem) {
    // Create proposal item
    $proposalItem = new QuotationSaleBomItem();
    $proposalItem->QuotationSaleBomId = $proposalBom->QuotationSaleBomId;
    $proposalItem->QuotationSaleId = $panelId;
    $proposalItem->QuotationId = $quotationId;
    $proposalItem->ProductId = $masterItem->ProductId; // GENERIC PRODUCT
    $proposalItem->Qty = $masterItem->Quantity; // COPY QUANTITY
    $proposalItem->Status = 0; // Active
    
    // Pricing not yet set
    $proposalItem->Rate = 0;
    $proposalItem->RateSource = 'UNRESOLVED';
    $proposalItem->IsPriceMissing = 1;
    
    $proposalItem->save();
}
```

**Key Points:**
- Each item is copied (new record)
- ProductId points to Generic Product
- Quantity copied from master
- Pricing not set (will be resolved later)

---

### Step 4: User Selects Make/Series

**Process:**
```php
// For each proposal item, user selects Make/Series via UI
foreach ($proposalItems as $proposalItem) {
    // User selects Make/Series
    $makeId = $request->make_id;
    $seriesId = $request->series_id;
    
    // Find or create specific product
    $genericProduct = Product::find($proposalItem->ProductId);
    $specificProduct = Product::where('GenericId', $genericProduct->ProductId)
        ->where('MakeId', $makeId)
        ->where('SeriesId', $seriesId)
        ->where('ProductType', 2)
        ->first();
    
    if (!$specificProduct) {
        // Create specific product
        $specificProduct = new Product();
        $specificProduct->GenericId = $genericProduct->ProductId;
        $specificProduct->CategoryId = $genericProduct->CategoryId;
        $specificProduct->SubCategoryId = $genericProduct->SubCategoryId;
        $specificProduct->ItemId = $genericProduct->ItemId;
        $specificProduct->ProductType = 2; // Specific
        $specificProduct->MakeId = $makeId;
        $specificProduct->SeriesId = $seriesId;
        $specificProduct->Name = $genericProduct->Name;
        $specificProduct->Status = 0;
        $specificProduct->save();
    }
    
    // Update proposal item with specific product
    $proposalItem->ProductId = $specificProduct->ProductId;
    $proposalItem->MakeId = $makeId;
    $proposalItem->SeriesId = $seriesId;
    $proposalItem->save();
}
```

**Key Points:**
- Make/Series selected per item
- Specific product found or created
- Proposal item updated with specific product

---

### Step 5: Load Prices

**Process:**
```php
foreach ($proposalItems as $proposalItem) {
    // Get price for specific product
    $date = date('Y-m-d');
    $price = Price::where('ProductId', $proposalItem->ProductId)
        ->where('EffectiveDate', '<=', $date)
        ->where('Status', 0)
        ->orderBy('EffectiveDate', 'DESC')
        ->first();
    
    if ($price) {
        $proposalItem->Rate = $price->Rate;
        $proposalItem->RateSource = 'PRICELIST';
        $proposalItem->IsPriceMissing = 0;
    } else {
        $proposalItem->Rate = 0;
        $proposalItem->RateSource = 'UNRESOLVED';
        $proposalItem->IsPriceMissing = 1;
    }
    
    $proposalItem->save();
}
```

**Key Points:**
- Price loaded from prices table
- Most recent effective date price selected
- If no price, flagged as missing

---

## 🔒 Independence Rules

### Rule 1: No Direct Link

**Rule:** Proposal BOM is independent of Master BOM

**Implementation:**
- MasterBomId stored for reference only
- No foreign key constraint (or soft constraint)
- Can delete Master BOM without affecting Proposal BOMs
- Can modify Proposal BOM without affecting Master BOM

---

### Rule 2: Changes Don't Propagate

**Rule:** Changes to Master BOM don't affect existing Proposal BOMs

**Example:**
```
Master BOM "Panel A" has 5 items
  → Copied to Quotation 1 (Proposal BOM has 5 items)
  
User adds 6th item to Master BOM "Panel A"
  → Master BOM now has 6 items
  → Quotation 1 Proposal BOM still has 5 items (unchanged)
  
User creates new Quotation 2
  → Copies Master BOM "Panel A"
  → Proposal BOM has 6 items (includes new item)
```

---

### Rule 3: Can Modify Proposal BOM

**Rule:** Proposal BOM can be modified independently

**Allowed Modifications:**
- Add items to Proposal BOM
- Remove items from Proposal BOM
- Change quantities
- Change Make/Series
- Change rates/discounts

**Master BOM:**
- Remains unchanged
- Still available for future quotations

---

## 📊 Copy Process Examples

### Example 1: Simple Copy

**Master BOM:**
```
Name: "Standard Panel Components"
Items:
  - Item 1: Generic Product A, Qty = 1
  - Item 2: Generic Product B, Qty = 12
```

**After Copy to Quotation:**
```
Proposal BOM:
  Name: "Standard Panel Components" (copied)
  MasterBomId: 5 (reference)
  
  Items:
    - Item 1: Generic Product A, Qty = 1 (copied)
    - Item 2: Generic Product B, Qty = 12 (copied)
```

**After Make/Series Selection:**
```
Proposal BOM Items:
  - Item 1: Specific Product (Make: Siemens, Series: S8), Qty = 1
  - Item 2: Specific Product (Make: ABB, Series: Tmax), Qty = 12
```

---

### Example 2: Copy with Modifications

**Master BOM:**
```
Name: "Panel Components"
Items:
  - Item 1: Generic Product A, Qty = 1
  - Item 2: Generic Product B, Qty = 10
```

**After Copy and User Modifications:**
```
Proposal BOM:
  Name: "Panel Components" (copied, can be renamed)
  Items:
    - Item 1: Generic Product A, Qty = 1 (unchanged)
    - Item 2: Generic Product B, Qty = 15 (modified by user)
    - Item 3: Generic Product C, Qty = 5 (added by user)
```

**Master BOM:**
- Still has original 2 items
- Unchanged by Proposal BOM modifications

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial copy process document | Part 4 of Master BOM backend design series |
| 1.1 | 2025-12-19 | Phase-3 | Inserted canonical L0/L1/L2 definitions; terminology aligned | Phase-3: Rule Compliance Review |

---

**Previous:** [Part 3: Master BOM Structure](MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md)  
**Next:** [Part 5: Business Rules & Validation](MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md)

