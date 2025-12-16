> Source: source_snapshot/QUOTATION_BACKEND_DESIGN_PART5_COSTING.md
> Bifurcated into: features/quotation/costing/QUOTATION_BACKEND_DESIGN_PART5_COSTING.md
> Module: Quotation > Costing
> Date: 2025-12-17 (IST)

# Quotation Backend Design - Part 5: Costing System

**Document:** QUOTATION_BACKEND_DESIGN_PART5_COSTING.md  
**Version:** 1.0  
**Date:** December 2025

---

## 📋 Overview

This document describes the costing system, which calculates costs at all hierarchy levels. The costing formulas are **permanent and non-negotiable**. The golden rule is: **SUM(AmountTotal) only, NO multipliers at roll-up level**.

---

## 🔒 Protected Service

**Service:** `CostingService`  
**Location:** `app/Services/CostingService.php`  
**Status:** 🔴 **PROTECTED CODE - DO NOT MODIFY WITHOUT APPROVAL**

---

## 🏆 Golden Rule (Non-Negotiable)

```
All roll-up costs = SUM(Component AmountTotal)
Where AmountTotal = NetRate × TotalQty
```

**Critical Principles:**
- ✅ Component-level: `AmountTotal = NetRate × TotalQty` (authoritative)
- ✅ BOM-level: `BOM_TotalCost = sum(Component AmountTotal)` (NO multipliers)
- ✅ Feeder-level: `Feeder_TotalCost = sum(Component AmountTotal)` (NO multipliers)
- ✅ Panel-level: `Panel_TotalCost = sum(Component AmountTotal)` (NO multipliers)
- ❌ **NEVER multiply roll-ups by PanelQty, FeederQty, or BOMQty**

---

## 💰 Component-Level Cost

### Formula

```
NetRate = Rate × (1 - Discount/100)
AmountTotal = NetRate × TotalQty
```

**Where:**
- `Rate` = Base rate from prices table or manual
- `Discount` = Discount percentage (0-100)
- `TotalQty` = Total quantity (from QuotationQuantityService)

**Special Cases:**
- If `IsClientSupplied = 1`: `Rate = 0`, `NetRate = 0`, `AmountTotal = 0`
- If `IsPriceMissing = 1`: `Rate = 0`, `NetRate = 0`, `AmountTotal = 0`

### Implementation

**Service Method:**
```php
public function componentCost(QuotationSaleBomItem $item): ComponentCostDto
```

**Calculation:**
```php
// Get effective quantities
$qtyData = $this->quantityService->calculate($item);

$baseRate = (float) ($item->Rate ?? 0);
$discountPercent = (float) ($item->Discount ?? 0);

// NetRate = Rate - (Rate × Discount / 100)
$netRate = $baseRate - ($baseRate * $discountPercent / 100);
$netRate = max(0, $netRate); // Ensure non-negative

$effQtyTotal = (float) ($qtyData['effective_qty_total'] ?? 0);

// TotalCost = NetRate × EffQtyTotal
$totalCost = $netRate * $effQtyTotal;
```

**Returns:**
```php
ComponentCostDto {
    baseRate: float,           // Original rate
    netRate: float,            // Rate after discount
    effQtyPerPanel: float,     // For display
    effQtyTotal: float,        // TotalQty (authoritative)
    totalCost: float,          // AmountTotal (authoritative)
}
```

---

## 📊 BOM-Level Cost

### BOM2 Cost (Leaf BOM)

**Definition:** BOM2 contains only components (no child BOMs)

**Formula:**
```
BOM2_TotalCost = SUM(AmountTotal of all components directly under this BOM2)
```

**Implementation:**
```php
public function bomCost(QuotationSaleBom $bom): BomCostDto
{
    $componentCostUnit = 0.0;
    
    // Sum direct components
    $items = $bom->item()->where('Status', 0)->get();
    foreach ($items as $item) {
        $componentCost = $this->componentCost($item);
        $componentCostUnit += $componentCost->totalCost; // Sum AmountTotal
    }
    
    // For BOM2, no child BOMs
    $childBomCostUnit = 0.0;
    
    // Total cost
    $totalCost = $componentCostUnit + $childBomCostUnit;
    
    return new BomCostDto(...);
}
```

**Example:**
```
BOM2 contains:
  - Component C1: AmountTotal = 2,160.00
  - Component C2: AmountTotal = 1,200.00
  
BOM2_TotalCost = 2,160.00 + 1,200.00 = 3,360.00
```

---

### BOM1 Cost (Split Required)

**Definition:** BOM1 may contain direct components AND multiple BOM2 children

**Formula:**
```
BOM1_ComponentCost = SUM(AmountTotal of components directly under BOM1)
BOM1_ChildBOMCost = SUM(BOM2_TotalCost of ALL child BOM2 nodes)
BOM1_TotalCost = BOM1_ComponentCost + BOM1_ChildBOMCost
```

**Implementation:**
```php
// Calculate cost of direct components
$componentCostUnit = 0.0;
$items = $bom->item()->where('Status', 0)->get();
foreach ($items as $item) {
    $componentCost = $this->componentCost($item);
    $componentCostUnit += $componentCost->totalCost;
}

// Calculate cost of child BOMs (recursive)
$childBomCostUnit = 0.0;
$childBoms = $bom->childBoms()->where('Status', 0)->get();
foreach ($childBoms as $childBom) {
    $childBomCost = $this->bomCost($childBom); // Recursive
    $childBomCostUnit += $childBomCost->totalCost; // Sum AmountTotal
}

// Total cost
$totalCost = $componentCostUnit + $childBomCostUnit;
```

**Example:**
```
BOM1 contains:
  - Direct Component D1: AmountTotal = 500.00
  - BOM2-A: BOM2_TotalCost = 3,360.00
  - BOM2-B: BOM2_TotalCost = 1,200.00
  
BOM1_ComponentCost = 500.00
BOM1_ChildBOMCost = 3,360.00 + 1,200.00 = 4,560.00
BOM1_TotalCost = 500.00 + 4,560.00 = 5,060.00
```

**Critical Rule:**
- If BOM1 has multiple BOM2 children → add each BOM2_TotalCost
- **No multipliers applied** - just sum the BOM2_TotalCost values
- Each BOM2_TotalCost already includes all multipliers (in component AmountTotal)

---

## 🔌 Feeder-Level Cost

### Formula

```
Feeder_TotalCost = SUM(AmountTotal of direct components under feeder)
                 + SUM(BOM1_TotalCost of ALL BOM1 nodes under feeder)
```

**Rules:**
- FeederQty is already included in component TotalQty
- **Do NOT multiply feeder totals by FeederQty**
- Simply sum all component AmountTotal values (direct + via BOMs)

### Implementation

```php
public function feederCost(QuotationSaleBom $feeder): FeederCostDto
{
    $totalCost = 0.0;
    
    // Sum all BOM1 costs under this feeder
    $childBoms = $feeder->childBoms()->where('Status', 0)->where('Level', 1)->get();
    foreach ($childBoms as $childBom) {
        $bomCost = $this->bomCost($childBom);
        $totalCost += $bomCost->totalCost; // Sum AmountTotal
    }
    
    // Add cost of any direct components under feeder
    $items = $feeder->item()->where('Status', 0)->get();
    foreach ($items as $item) {
        $componentCost = $this->componentCost($item);
        $totalCost += $componentCost->totalCost; // Sum AmountTotal
    }
    
    return new FeederCostDto(...);
}
```

**Example:**
```
Feeder contains:
  - Direct Component E1: AmountTotal = 200.00
  - BOM1-A: BOM1_TotalCost = 5,060.00
  - BOM1-B: BOM1_TotalCost = 2,000.00
  
Feeder_TotalCost = 200.00 + 5,060.00 + 2,000.00 = 7,260.00
```

---

## 🎛️ Panel-Level Cost

### Formula

```
Panel_TotalCost = SUM(Feeder_TotalCost of ALL feeders under this panel)
```

**Equivalently:**
```
Panel_TotalCost = SUM(AmountTotal of ALL components belonging to this panel)
```

**Rules:**
- PanelQty is already included in component TotalQty
- **Do NOT multiply panel totals by PanelQty**
- This is the final quotation cost for this panel

### Implementation

```php
public function panelCost(QuotationSale $panel): PanelCostDto
{
    $totalCost = 0.0;
    
    // Get all feeders for this panel
    $feeders = QuotationSaleBom::where('QuotationSaleId', $panel->QuotationSaleId)
        ->where('Status', 0)
        ->where(function($query) {
            $query->where(function($q) {
                $q->where('Level', 0)->whereNull('ParentBomId');
            })->orWhere(function($q) {
                $q->whereNull('Level')->whereNull('ParentBomId');
            });
        })
        ->get();
    
    foreach ($feeders as $feeder) {
        $feederCost = $this->feederCost($feeder);
        $totalCost += $feederCost->totalCost; // Sum AmountTotal
    }
    
    return new PanelCostDto(...);
}
```

**Example:**
```
Panel contains:
  - Feeder F1: Feeder_TotalCost = 7,260.00
  - Feeder F2: Feeder_TotalCost = 2,500.00
  
Panel_TotalCost = 7,260.00 + 2,500.00 = 9,760.00
```

---

## 🎯 Cost Calculation Hierarchy

### Complete Flow

```
Component Level:
  AmountTotal = NetRate × TotalQty
  ↓
BOM2 Level:
  BOM2_TotalCost = SUM(Component AmountTotal)
  ↓
BOM1 Level:
  BOM1_TotalCost = SUM(Direct Component AmountTotal) + SUM(BOM2_TotalCost)
  ↓
Feeder Level:
  Feeder_TotalCost = SUM(Direct Component AmountTotal) + SUM(BOM1_TotalCost)
  ↓
Panel Level:
  Panel_TotalCost = SUM(Feeder_TotalCost)
```

**Key Point:** At each level, we **SUM AmountTotal values**, never multiply by quantities.

---

## 📐 Per-Panel Display Costs

### Calculation Method

**Rule:** Compute separately, do NOT derive by dividing totals

**Formula:**
```
BOM_costPerPanel = SUM(NetRate × EffQtyPerPanel for components in BOM subtree)
Feeder_costPerPanel = SUM(NetRate × EffQtyPerPanel for feeder subtree)
Panel_costPerPanel = SUM(NetRate × EffQtyPerPanel for panel subtree)
```

**Why Not Divide:**
- Dividing totals by PanelQty fails when FeederQty/BOMQty distort totals
- Example: If FeederQty = 2, dividing total by PanelQty gives wrong per-panel cost
- **Always compute per-panel costs by summing AmountPerPanel values**

**Example:**
```
Component C1:
  NetRate = 90.00
  EffQtyPerPanel = 30
  AmountPerPanel = 90.00 × 30 = 2,700.00

Component C2:
  NetRate = 50.00
  EffQtyPerPanel = 20
  AmountPerPanel = 50.00 × 20 = 1,000.00

BOM_costPerPanel = 2,700.00 + 1,000.00 = 3,700.00
```

**NOT:**
```
❌ BOM_costPerPanel = BOM_TotalCost / PanelQty  // WRONG!
```

---

## 🔄 CostingService Architecture

### Service Class

**Location:** `app/Services/CostingService.php`

**Dependencies:**
- `QuotationQuantityService` - For quantity calculations

**Main Methods:**
- `componentCost(QuotationSaleBomItem $item): ComponentCostDto`
- `bomCost(QuotationSaleBom $bom): BomCostDto`
- `feederCost(QuotationSaleBom $feeder): FeederCostDto`
- `panelCost(QuotationSale $panel): PanelCostDto`

**Caching:**
- Cost cache to prevent recalculation
- Cache keyed by entity ID
- Cleared when quantities/rates change

---

## 📊 DTOs (Data Transfer Objects)

### ComponentCostDto

```php
class ComponentCostDto {
    public float $baseRate;           // Original rate
    public float $netRate;            // Rate after discount
    public float $effQtyPerPanel;     // For display
    public float $effQtyTotal;        // TotalQty (authoritative)
    public float $totalCost;          // AmountTotal (authoritative)
}
```

### BomCostDto

```php
class BomCostDto {
    public float $componentCostUnit;   // Direct components (for BOM1 split)
    public float $childBomCostUnit;    // Child BOMs (for BOM1 split)
    public float $unitCost;            // Per panel (display)
    public float $totalCost;           // Authoritative (sum of AmountTotal)
    public float $bomQty;             // Reference only
}
```

### FeederCostDto

```php
class FeederCostDto {
    public float $unitCost;           // Per panel (display)
    public float $totalCost;          // Authoritative
    public float $feederQty;          // Reference only
}
```

### PanelCostDto

```php
class PanelCostDto {
    public float $unitCost;           // Per panel (display)
    public float $totalCost;           // Authoritative
    public float $panelQty;            // Reference only
}
```

---

## ✅ Validation & Edge Cases

### Client-Supplied Items

**Rule:** If `IsClientSupplied = 1`, cost is zero

```php
if ($item->IsClientSupplied == 1) {
    $baseRate = 0;
    $netRate = 0;
    $totalCost = 0;
}
```

**Impact:**
- Included in roll-ups (but contributes 0)
- Shows in UI with zero cost
- Flagged as client-supplied

---

### Missing Prices

**Rule:** If `IsPriceMissing = 1`, cost is zero

```php
if ($item->IsPriceMissing == 1) {
    $baseRate = 0;
    $netRate = 0;
    $totalCost = 0;
}
```

**Impact:**
- Included in roll-ups (but contributes 0)
- Flagged as unpriced in UI
- Requires price resolution before finalization

---

### Empty BOMs

**Rule:** BOMs with no items have cost = 0

```php
$items = $bom->item()->where('Status', 0)->get();
if ($items->isEmpty()) {
    $totalCost = 0.0;
}
```

**Impact:**
- Included in roll-ups (but contributes 0)
- Shows in UI with zero cost

---

## 🚫 Never Do These

### ❌ Never Multiply Rollups by Quantities

```php
// WRONG!
$bomTotalCost = $componentCostUnit * $bomQty; // ❌

// CORRECT!
$bomTotalCost = $componentCostUnit; // ✅ (already includes multipliers)
```

### ❌ Never Use EffQtyPerPanel for Costing

```php
// WRONG!
$cost = $netRate * $effQtyPerPanel * $panelQty; // ❌

// CORRECT!
$cost = $netRate * $totalQty; // ✅ (TotalQty already includes PanelQty)
```

### ❌ Never Divide Totals to Get Per-Panel Costs

```php
// WRONG!
$costPerPanel = $totalCost / $panelQty; // ❌ (fails with FeederQty/BOMQty)

// CORRECT!
$costPerPanel = sum($netRate * $effQtyPerPanel for all components); // ✅
```

---

## ✅ Always Do These

### ✅ Always Sum AmountTotal

```php
// CORRECT!
$bomTotalCost = sum($component->totalCost for all components); // ✅
```

### ✅ Always Use TotalQty for Component AmountTotal

```php
// CORRECT!
$amountTotal = $netRate * $totalQty; // ✅
```

### ✅ Always Compute Per-Panel Costs Separately

```php
// CORRECT!
$costPerPanel = sum($netRate * $effQtyPerPanel for all components); // ✅
```

---

## 📚 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-15 | Auto | Initial costing document | Part 5 of backend design series |

---

**Previous:** [Part 4: Quantity Calculation System](QUOTATION_BACKEND_DESIGN_PART4_QUANTITY.md)  
**Next:** [Part 6: Pricing & Discount Rules](QUOTATION_BACKEND_DESIGN_PART6_PRICING.md)

