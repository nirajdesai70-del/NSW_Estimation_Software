# L1/L2 Explosion Logic - Corrected Rules

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** LOCKED - FINAL  
**Purpose:** Corrected explosion logic rules based on price list working insights

---

## Core Principle (LOCKED)

> **"Multiple L1 rows may legally map to the same L2 SKU."**

**This is the key Phase 5 correction.**

---

## What Changed

### ❌ OLD (Implicit, Wrong)

**Assumption:**
```
Different duty / rating = different SKU
```

**Explosion Logic:**
```
Duty × Rating × Voltage → multiple L2 rows
```

**Problem:**
- Created duplicate SKUs for same OEM catalog number
- Price inconsistency
- Frame/pole misuse as multipliers

---

### ✅ CORRECT (Locked Now)

**Model:**
```
Same SKU
Multiple L1 interpretations
Same price
```

**Explosion Logic:**
```
Engineering interpretation → multiple L1 rows
Commercial reality → single L2 row
```

**Result:**
- One SKU per OEM catalog number
- Multiple L1 interpretations
- Price reused correctly

---

## Correct Explosion Flow

### User Intent → Engineering Specs → SKU Resolution

```
User intent (L0)
   ↓
Engineering specs (L1a, L1b, L1c…)
   ↓
SKU resolution (many L1 → same L2 allowed)
```

---

## Explosion Service Logic

### FOR EACH L1: Resolve Base SKU

**✅ CORRECT Logic:**

```php
FOR EACH L1:
   Resolve base SKU
   Resolve feature SKUs (if ADDON required)
```

**❌ NOT:**

```php
Multiply SKU per attribute
```

---

## Concrete Rules

### Rule 1: SKU Reuse is Allowed and Expected ✅

**Multiple L1 lines may legally map to the same L2 SKU.**

**Example:**
```
L1-A: AC1, 20A, 3P, 220V → LC1E0601
L1-B: AC3, 6A, 3P, 220V → LC1E0601
L1-C: AC1, 20A, 3P, 415V → LC1E0601
L1-D: AC3, 6A, 3P, 415V → LC1E0601

All map to same L2 SKU (LC1E0601) with same price (₹2875)
```

---

### Rule 2: Duty/Rating Never Creates SKU ❌

**Duty (AC1/AC3) and rating differences do NOT create new SKUs.**

**Only OEM catalog number change creates new SKU:**

| Situation | Result |
|-----------|--------|
| LC1E0601 → LC1E0601M | ✅ New L2 (catalog number changed) |
| LC1E0601 → LC1E0601N5 | ✅ New L2 (catalog number changed) |
| Same reference, different AC1/AC3 | ❌ No new L2 (different L1 only) |
| Same reference, different current rating | ❌ No new L2 (different L1 only) |

---

### Rule 3: Frame is NEVER a Multiplier ❌

**Frame is physical size. Frame may change with poles/current. But frame itself does NOT create new L2.**

**Only SKU change does.**

---

### Rule 4: SC-L Layers Never Multiply SKUs ❌

| Layer | What it controls | Multiplies SKU? |
|-------|------------------|-----------------|
| SC-L1 Construction | Frame / Form | ❌ No |
| SC-L2 Operation | Poles / Actuation | ❌ No |
| SC-L3 Feature Class | AC1 / AC3 / Breaking Capacity | ❌ No |
| SC-L4 Accessory Class | Aux / Coil / OLR / Interlock | ❌ No (unless ADDON SKU) |

**Only feature policy may create extra SKUs, not attributes.**

---

### Rule 5: Accessories Resolve Via Feature Policy ✅

**Accessories (Aux contacts, overloads, interlocks, suppressors):**
- Do NOT multiply per base SKU
- Exist as SC-L4 feature lines
- Resolve to L2 only if OEM policy requires ADDON SKU
- One accessory definition → reusable across many L1s

**Feature Policy Types:**
- `INCLUDED_IN_BASE` → No SKU created
- `ADDON_SKU_REQUIRED` → Creates separate L2 SKU
- `BUNDLED_ALTERNATE_BASE` → Creates alternate base SKU

---

## Example: LC1E0601 Explosion

### L2 (Single Row - Commercial Truth)

```
SKU: LC1E0601
Make: Schneider
Price: ₹2875
```

---

### L1 (Multiple Rows - Engineering Interpretations)

**L1-A (AC1 use-case):**
```
Category: Motor Control
Item/ProductType: Contactor
SubCategories:
  SC_L2 Operation: 3 Pole
  SC_L3 Feature Class: AC1
Attributes:
  DUTY = AC1
  CURRENT = 20 A
  HP = 3
  kW = 2.2
Parent L2 SKU: LC1E0601
```

**L1-B (AC3 use-case):**
```
Category: Motor Control
Item/ProductType: Contactor
SubCategories:
  SC_L2 Operation: 3 Pole
  SC_L3 Feature Class: AC3
Attributes:
  DUTY = AC3
  CURRENT = 6 A
  HP = 3
  kW = 2.2
Parent L2 SKU: LC1E0601
```

**L1-C (AC1, 415V use-case):**
```
Category: Motor Control
Item/ProductType: Contactor
SubCategories:
  SC_L2 Operation: 3 Pole
  SC_L3 Feature Class: AC1
Attributes:
  DUTY = AC1
  CURRENT = 20 A
  VOLTAGE = 415V
  HP = 3
  kW = 2.2
Parent L2 SKU: LC1E0601
```

**L1-D (AC3, 415V use-case):**
```
Category: Motor Control
Item/ProductType: Contactor
SubCategories:
  SC_L2 Operation: 3 Pole
  SC_L3 Feature Class: AC3
Attributes:
  DUTY = AC3
  CURRENT = 6 A
  VOLTAGE = 415V
  HP = 3
  kW = 2.2
Parent L2 SKU: LC1E0601
```

**Result:**
- ✔ One SKU (LC1E0601)
- ✔ One price (₹2875)
- ✔ Four L1 interpretations
- ✔ No duplication
- ✔ Price reused correctly

---

## Implementation Contract

### L1 → L2 Explosion Service

**Input:**
- L1 intent lines (BASE + FEATURE)
- L1 attributes
- Feature policy rules

**Process:**
1. For each L1 BASE line:
   - Resolve base SKU (by Make, Series, Item, attributes)
   - Check if SKU exists in L2
   - If not, create L2 SKU (or block per ADR-005)
   - Map L1 → L2 (many-to-one allowed)

2. For each L1 FEATURE line:
   - Check feature policy
   - If `ADDON_SKU_REQUIRED`, resolve addon SKU
   - If `INCLUDED_IN_BASE`, use base SKU
   - If `BUNDLED_ALTERNATE_BASE`, resolve alternate base SKU

**Output:**
- L1 lines with L2 SKU mappings
- Multiple L1 → Same L2 allowed

---

## Validation Rules

### L1 Validation

**Must Allow:**
- ✅ Same SKU mapping for multiple L1 rows
- ✅ Multiple L1 rows with different attributes mapping to same L2

**Must NOT Assume:**
- ❌ 1 L1 → 1 SKU (wrong assumption)
- ❌ Unique SKU per L1 (wrong constraint)

---

### L2 Validation

**Must Enforce:**
- ✅ One SKU per OEM catalog number
- ✅ Price lives at L2 only
- ✅ No engineering attributes in L2

**Must NOT Store:**
- ❌ AC1/AC3 rating rows
- ❌ Duty-wise current rows
- ❌ Frame as multiplier
- ❌ Accessory compatibility

---

## Database Schema Requirements

### L1 Table

**Must Support:**
- ✅ Foreign key to L2 (many-to-one relationship)
- ✅ Multiple L1 rows → Same L2 SKU

**Schema:**
```sql
CREATE TABLE l1_intent_lines (
    id BIGSERIAL PRIMARY KEY,
    l2_sku_id BIGINT NOT NULL,  -- FK to catalog_skus
    -- ... other L1 fields
    FOREIGN KEY (l2_sku_id) REFERENCES catalog_skus(id)
);

-- Multiple L1 rows can have same l2_sku_id (this is correct)
```

---

### L2 Table

**Must Enforce:**
- ✅ Unique constraint: (Make, OEM_Catalog_No)
- ✅ One row per OEM catalog number

**Schema:**
```sql
CREATE TABLE catalog_skus (
    id BIGSERIAL PRIMARY KEY,
    make VARCHAR(255) NOT NULL,
    oem_catalog_no VARCHAR(100) NOT NULL,
    -- ... other L2 fields
    UNIQUE (make, oem_catalog_no)  -- One SKU per catalog number
);
```

---

## Price Refresh Impact

### Example: LC1E0601 Price Update

**Before:**
```
L2: LC1E0601, Price: ₹2875
L1-A: AC1 → LC1E0601
L1-B: AC3 → LC1E0601
L1-C: AC1, 415V → LC1E0601
L1-D: AC3, 415V → LC1E0601
```

**Price Update:**
```
L2: LC1E0601, Price: ₹3000 (updated once)
```

**After:**
```
L2: LC1E0601, Price: ₹3000
L1-A: AC1 → LC1E0601 (automatically gets ₹3000)
L1-B: AC3 → LC1E0601 (automatically gets ₹3000)
L1-C: AC1, 415V → LC1E0601 (automatically gets ₹3000)
L1-D: AC3, 415V → LC1E0601 (automatically gets ₹3000)
```

**Result:**
- ✅ One price update
- ✅ All L1 interpretations automatically reflect new price
- ✅ No duplication, no reconciliation needed

---

## Golden Sentence

> **"Different engineering interpretations of the same OEM product are represented as multiple L1 lines referencing a single L2 SKU."**

**This sentence alone resolves the confusion permanently.**

---

## References

- **Phase 5 Impact Assessment:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_PRICE_LIST_IMPACT_ASSESSMENT.md`
- **Schneider L2/L1 Differentiation:** `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`
- **L2 Import Structure:** `docs/PHASE_5/CANONICAL/L2_IMPORT_STRUCTURE_v1.3.1.md`
- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`

---

**Document Status:** ✅ **LOCKED - FINAL**

**Next Step:** Use this logic in Phase 5 implementation.

