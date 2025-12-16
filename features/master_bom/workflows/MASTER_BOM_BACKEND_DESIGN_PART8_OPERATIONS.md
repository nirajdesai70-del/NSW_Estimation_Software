> Source: source_snapshot/MASTER_BOM_BACKEND_DESIGN_PART8_OPERATIONS.md
> Bifurcated into: features/master_bom/workflows/MASTER_BOM_BACKEND_DESIGN_PART8_OPERATIONS.md
> Module: Master BOM > Workflows
> Date: 2025-12-17 (IST)

# Master BOM Backend Design - Part 8: Operation Level Details

**Document:** MASTER_BOM_BACKEND_DESIGN_PART8_OPERATIONS.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document provides detailed operation-level workflows for all major operations in the Master BOM module.

---

## 🔄 Operation 1: Create Master BOM

### Step-by-Step Operation Flow

**Step 1: Validate Input**
```php
$validated = $request->validate([
    'Name' => 'required|string|max:255',
    'items' => 'required|array|min:1',
    'items.*.ProductId' => 'required|exists:products,ProductId',
    'items.*.Quantity' => 'required|numeric|min:0.01',
]);
```

**Step 2: Validate Products are Generic**
```php
foreach ($validated['items'] as $item) {
    $product = Product::find($item['ProductId']);
    if ($product->ProductType != 1) {
        return redirect()->back()
            ->with('error', 'Master BOM items must use generic products only');
    }
}
```

**Step 3: Create Master BOM Header**
```php
$masterBom = MasterBom::create([
    'Name' => $validated['Name'],
    'Status' => 0, // Active
]);
```

**Step 4: Create Master BOM Items**
```php
foreach ($validated['items'] as $item) {
    MasterBomItem::create([
        'MasterBomId' => $masterBom->MasterBomId,
        'ProductId' => $item['ProductId'], // Generic product
        'Quantity' => $item['Quantity'], // Template quantity
        'Status' => 0, // Active
    ]);
}
```

**Step 5: Return Response**
```php
return redirect()->route('masterbom.index')
    ->with('success', 'Master BOM created successfully');
```

---

## 🔄 Operation 2: Add Item to Master BOM

### Step-by-Step Operation Flow

**Step 1: Validate Input**
```php
$validated = $request->validate([
    'MasterBomId' => 'required|exists:master_boms,MasterBomId',
    'ProductId' => 'required|exists:products,ProductId',
    'Quantity' => 'required|numeric|min:0.01',
]);
```

**Step 2: Validate Product is Generic**
```php
$product = Product::find($validated['ProductId']);
if ($product->ProductType != 1) {
    return response()->json([
        'error' => 'Master BOM items must use generic products only'
    ], 422);
}
```

**Step 3: Create Master BOM Item**
```php
$item = MasterBomItem::create([
    'MasterBomId' => $validated['MasterBomId'],
    'ProductId' => $validated['ProductId'],
    'Quantity' => $validated['Quantity'],
    'Status' => 0,
]);
```

**Step 4: Return Response**
```php
return response()->json([
    'success' => true,
    'item' => $item,
    'message' => 'Item added successfully'
]);
```

---

## 🔄 Operation 3: Update Master BOM

### Step-by-Step Operation Flow

**Step 1: Validate Input**
```php
$validated = $request->validate([
    'Name' => 'required|string|max:255',
    'items' => 'required|array|min:1',
    'items.*.ProductId' => 'required|exists:products,ProductId',
    'items.*.Quantity' => 'required|numeric|min:0.01',
]);
```

**Step 2: Validate Products are Generic**
```php
foreach ($validated['items'] as $item) {
    $product = Product::find($item['ProductId']);
    if ($product->ProductType != 1) {
        return redirect()->back()
            ->with('error', 'Master BOM items must use generic products only');
    }
}
```

**Step 3: Update Master BOM Header**
```php
$masterBom = MasterBom::findOrFail($id);
$masterBom->Name = $validated['Name'];
$masterBom->save();
```

**Step 4: Soft Delete Existing Items**
```php
MasterBomItem::where('MasterBomId', $id)
    ->update(['Status' => 1]);
```

**Step 5: Create New Items**
```php
foreach ($validated['items'] as $item) {
    MasterBomItem::create([
        'MasterBomId' => $masterBom->MasterBomId,
        'ProductId' => $item['ProductId'],
        'Quantity' => $item['Quantity'],
        'Status' => 0,
    ]);
}
```

**Step 6: Return Response**
```php
return redirect()->route('masterbom.index')
    ->with('success', 'Master BOM updated successfully');
```

---

## 🔄 Operation 4: Delete Master BOM

### Step-by-Step Operation Flow

**Step 1: Soft Delete All Items**
```php
MasterBomItem::where('MasterBomId', $id)
    ->update(['Status' => 1]);
```

**Step 2: Soft Delete Master BOM**
```php
MasterBom::where('MasterBomId', $id)
    ->update(['Status' => 1]);
```

**Step 3: Return Response**
```php
return redirect()->route('masterbom.index')
    ->with('success', 'Master BOM deleted successfully');
```

**Note:** Existing Proposal BOMs are not affected (already copied)

---

## 🔄 Operation 5: Copy Master BOM to Quotation

### Step-by-Step Operation Flow

**Step 1: Load Master BOM**
```php
$masterBom = MasterBom::with('items.product')->findOrFail($masterBomId);
```

**Step 2: Create Proposal BOM Header**
```php
$proposalBom = new QuotationSaleBom();
$proposalBom->QuotationSaleId = $panelId;
$proposalBom->QuotationId = $quotationId;
$proposalBom->MasterBomId = $masterBomId; // Reference only
$proposalBom->MasterBomName = $masterBom->Name;
$proposalBom->BomName = $masterBom->Name;
$proposalBom->Level = $requestedLevel; // 1 or 2
$proposalBom->ParentBomId = $parentBomId;
$proposalBom->Qty = $requestedQty;
$proposalBom->Status = 0;
$proposalBom->save();
```

**Step 3: Copy Master BOM Items**
```php
foreach ($masterBom->items as $masterItem) {
    $proposalItem = new QuotationSaleBomItem();
    $proposalItem->QuotationSaleBomId = $proposalBom->QuotationSaleBomId;
    $proposalItem->QuotationSaleId = $panelId;
    $proposalItem->QuotationId = $quotationId;
    $proposalItem->ProductId = $masterItem->ProductId; // Generic product
    $proposalItem->Qty = $masterItem->Quantity; // Copy quantity
    $proposalItem->Rate = 0; // Not yet set
    $proposalItem->RateSource = 'UNRESOLVED';
    $proposalItem->IsPriceMissing = 1;
    $proposalItem->Status = 0;
    $proposalItem->save();
}
```

**Step 4: Return Response**
```php
return response()->json([
    'success' => true,
    'bom' => $proposalBom,
    'items_count' => count($masterBom->items),
    'message' => 'Master BOM copied successfully'
]);
```

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial operations document | Part 8 of Master BOM backend design series |

---

**Previous:** [Part 7: Master Data Integration](MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md)  
**Next:** [Part 9: Logic Level Details](MASTER_BOM_BACKEND_DESIGN_PART9_LOGIC.md)

