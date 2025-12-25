# Panel BOM Quantity Contract

**File:** PLANNING/PANEL_BOM/QUANTITY_CONTRACT.md  
**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** ✅ FROZEN (PB0.3) — Already Verified  
**Purpose:** Lock the quantity multiplication contract for Panel BOM (already verified and locked)

---

## ⚠️ CRITICAL: FROZEN CONTRACT

This document locks the **quantity multiplication contract** for Panel BOM. This contract has **already been verified and locked** per user confirmation.

**Mode:** Planning-only (execution deferred)  
**Governance:** Aligned with Feeder BOM methodology  
**Reference:** `PANEL_BOM_PLANNING_TRACK.md` PB0.3  
**Verification Status:** ✅ **ALREADY VERIFIED**

---

## 1) Quantity Contract (Locked)

### 1.1 Core Principle

**Panel quantity multiply happens ONCE, and only ONCE.**

- Component level: `ItemQty × BOMQty` (standard BOM multiplication)
- Panel level: Multiply once by `PanelQty` (inside `quotationAmount()`)
- **No other multipliers anywhere** in the quantity chain

### 1.2 Multiplication Chain

**The only canonical multiplication chain:**

```
Item Master (BaseQty = 1)
    ↓
Master BOM Item (Qty multiplier)
    ↓
Proposal BOM Item (ItemQty × BOMQty)
    ↓
Proposal BOM (rollup)
    ↓
Feeder (rollup)
    ↓
Panel (PanelQty multiplier applied ONCE)
    ↓
Proposal Amount (quotationAmount())
```

### 1.3 Multiplication Rules

**Component Level (Item → BOM):**
- `ItemQty` (from Item Master)
- `BOMQty` (from Proposal BOM Item)
- **Result:** `ItemQty × BOMQty` (applied at item level)

**Panel Level (Panel → Proposal):**
- `PanelQty` (from Proposal Panel)
- Applied **once** inside `quotationAmount()` calculation
- **Result:** All panel-level quantities multiplied by `PanelQty`

**Forbidden Multiplications:**
- ❌ No double multiplication of `PanelQty`
- ❌ No multiplication at feeder level (feeders are containers, not multipliers)
- ❌ No multiplication at BOM level beyond item-level `BOMQty`
- ❌ No additional multipliers in rollup calculations

---

## 2) Verification Status

### 2.1 Already Verified

**Status:** ✅ **VERIFIED AND LOCKED**

Per user confirmation, the quantity contract has already been verified:
- Panel qty multiply happens once
- Quantity chain is correct
- No double multiplication issues
- Rollup calculations are correct

### 2.2 Verification Evidence

**Evidence location (when available):**
- Panel rollup verification documents
- Quantity contract verification SQL/queries
- `quotationAmount()` calculation review

**Note:** Verification details are tracked separately (may be in PB-VER-001 or similar).

---

## 3) Alignment with Feeder BOM

### 3.1 Feeder BOM Quantity Rules

Feeder BOM does **not** have quantity multiplication:
- Feeders are containers (Level=0 BOMs)
- Feeder items follow standard `ItemQty × BOMQty` multiplication
- No feeder-level quantity multiplier

### 3.2 Panel BOM Quantity Rules

Panel BOM **adds** panel-level multiplication:
- Panel is above feeder in hierarchy
- Panel quantity multiplies all contained quantities
- Applied once at panel level (inside `quotationAmount()`)

### 3.3 Integration

**When Panel contains Feeders:**

1. Feeder items: `ItemQty × BOMQty` (feeder-level calculation)
2. Feeder rollup: Sum of all feeder items
3. Panel rollup: Sum of all feeders
4. Panel multiplication: `PanelQty × PanelRollup` (applied once)

**Result:** Clean, single multiplication at panel level

---

## 4) Implementation Contract

### 4.1 Calculation Location

**Panel quantity multiplication happens inside `quotationAmount()`:**

- Function: `quotationAmount()` (or equivalent)
- Location: Service layer (e.g., `BomEngine` or `QuotationService`)
- Input: Panel-level quantities (already rolled up)
- Operation: Multiply by `PanelQty`
- Output: Final proposal amount

### 4.2 Code Contract

**Expected pattern (illustrative, not implementation spec):**

```php
// ✅ CORRECT: Multiply once at panel level
function quotationAmount(QuotationSale $panel) {
    $panelRollup = calculatePanelRollup($panel); // Sum of feeders
    return $panelRollup * $panel->PanelQty; // Multiply once
}

// ❌ FORBIDDEN: Double multiplication
function quotationAmount(QuotationSale $panel) {
    $feederRollup = calculateFeederRollup($panel);
    $panelRollup = $feederRollup * $panel->PanelQty; // First multiply
    return $panelRollup * $panel->PanelQty; // ❌ Second multiply (FORBIDDEN)
}
```

**Note:** This is planning-only documentation. Actual implementation will be verified during execution window.

---

## 5) Exit Criteria (PB0.3)

- [x] Quantity contract document created
- [x] Multiplication chain locked
- [x] Multiplication rules locked
- [x] Verification status confirmed (already verified)
- [x] Alignment with Feeder BOM documented
- [x] Implementation contract documented

**Status:** ✅ **COMPLETE** — Quantity contract locked (already verified)

---

## 6) References

### Internal Documents
- `PLANNING/PANEL_BOM/CANONICAL_FLOW.md` - Canonical flow (PB0.1)
- `PLANNING/PANEL_BOM/COPY_RULES.md` - Copy rules (PB0.2)
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` - Main planning track

### External References
- Panel Master design Part-9 (Logic) - Business logic and calculations
- Panel rollup verification documents (PB-VER-001, when available)
- Feeder BOM quantity rules (reference: no feeder-level multiplication)

---

**END OF DOCUMENT**

