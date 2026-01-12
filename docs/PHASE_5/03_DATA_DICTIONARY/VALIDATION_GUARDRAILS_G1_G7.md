# Validation Guardrails G1-G8

**Version:** 1.1  
**Date:** 2025-01-27  
**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Purpose:** Canonical business rules for data validation and normalization

---

## Purpose

This document defines the eight validation guardrails (G1-G8) that enforce data integrity and business rules across the NSW system. These guardrails are **non-negotiable** and must be enforced at the appropriate layer (database, service, or worker).

---

## Guardrail Rules

### G1: Master BOM Rejects ProductId

**What it means:**
- Master BOM items (templates) must NOT have a ProductId set
- Master BOM items are generic placeholders (L0) or defined specifications (L1)
- ProductId is only allowed in Production/Quotation BOM items (L2)

**When it applies:**
- When creating or updating Master BOM items
- When applying Master BOM to quotation (ProductId must remain NULL)
- During Master BOM validation

**Normalization rules:**
- If ResolutionStatus is L0 or L1, ProductId MUST be NULL
- If ProductId is provided for L0/L1, it must be forced to NULL (silent normalization)
- L2 is NOT allowed in Master BOM (enforced separately)

**Enforcement layer:**
- **Primary:** Service validation (MasterBomItem model boot hook)
- **Secondary:** Database constraint (CHECK constraint if supported)
- **Validation point:** Before save/update operations

**Example:**
```php
// Master BOM item with L0 resolution
ResolutionStatus: 'L0'
GenericDescriptor: 'MCCB 100A'
ProductId: NULL (forced by G1)

// Attempt to set ProductId on L0 item
ResolutionStatus: 'L0'
ProductId: 12345  // ❌ Violates G1
// System normalizes: ProductId → NULL
```

---

### G2: Production/Quote BOM Requires ProductId at "Resolved" State

**What it means:**
- Production BOM items (QuotationSaleBomItem) must have ProductId when in resolved state
- Resolved state = L2 (fully mapped to specific product)
- ProductId is required for pricing and costing calculations

**When it applies:**
- When creating or updating Quotation BOM items
- When resolving items from L0/L1 to L2
- Before finalizing quotation (all items must be L2 with ProductId)
- During pricing calculations

**Normalization rules:**
- If ResolutionStatus is L2, ProductId MUST be set (NOT NULL)
- If ProductId is missing for L2 item:
  - Set `IsPriceMissing = true`
  - Set `RateSource = 'UNRESOLVED'`
  - Set `Rate = 0`
  - Set `Amount = 0`
- Cannot finalize/export quotation with unresolved items

**Enforcement layer:**
- **Primary:** Service validation (QuotationSaleBomItem model)
- **Secondary:** Database constraint (NOT NULL on ProductId when ResolutionStatus = L2)
- **Validation point:** Before save, before quotation finalization

**Example:**
```php
// Valid Production BOM item
ResolutionStatus: 'L2'
ProductId: 12345  // ✅ Required
Rate: 50.00
IsPriceMissing: false

// Invalid Production BOM item
ResolutionStatus: 'L2'
ProductId: NULL  // ❌ Violates G2
// System sets: IsPriceMissing = true, RateSource = 'UNRESOLVED', Rate = 0
```

---

### G3: IsPriceMissing Normalizes Rate/Net/Amount

**What it means:**
- When `IsPriceMissing = true`, all pricing fields must be normalized to zero or null
- Prevents inconsistent state where price is missing but amounts are non-zero
- Ensures costing calculations are accurate

**When it applies:**
- When `IsPriceMissing` is set to true
- When price lookup fails (no price found in prices table)
- When ProductId is missing (triggers IsPriceMissing)
- During price recalculation

**Normalization rules:**
- If `IsPriceMissing = true`:
  - `Rate` → 0 (or NULL)
  - `NetRate` → 0 (or NULL)
  - `Amount` → 0 (or NULL)
  - `RateSource` → 'UNRESOLVED'
- If `IsPriceMissing = false`:
  - Rate must be set from price list or manual entry
  - Normal pricing calculations apply

**Enforcement layer:**
- **Primary:** Service validation (pricing calculation service)
- **Secondary:** Database trigger (if supported)
- **Validation point:** On price calculation, on IsPriceMissing change

**Example:**
```php
// Price missing scenario
IsPriceMissing: true
Rate: 0  // ✅ Normalized
NetRate: 0  // ✅ Normalized
Amount: 0  // ✅ Normalized
RateSource: 'UNRESOLVED'

// Price found scenario
IsPriceMissing: false
Rate: 50.00  // From prices table
NetRate: 45.00  // Rate × (1 - Discount/100)
Amount: 450.00  // NetRate × Qty
RateSource: 'PRICELIST'
```

---

### G4: RateSource Consistency Rules

**What it means:**
- RateSource enum value must be consistent with actual rate source
- RateSource determines how rate was obtained and how it can be modified
- Prevents inconsistent state between RateSource and actual pricing data

**When it applies:**
- When setting RateSource
- When updating rate manually
- During price lookup
- When applying discounts

**Normalization rules:**
- `RateSource = 'PRICELIST'`:
  - Rate must come from prices table
  - Can be overridden with permission (changes to 'MANUAL_WITH_DISCOUNT' or 'FIXED_NO_DISCOUNT')
  - Discount applies normally
- `RateSource = 'MANUAL_WITH_DISCOUNT'`:
  - Rate is manually entered
  - Discount applies (NetRate = Rate × (1 - Discount/100))
  - Requires permission + ManualOverrideReason
- `RateSource = 'FIXED_NO_DISCOUNT'`:
  - Rate is manually entered
  - Discount is ignored (NetRate = Rate, discount_pct = 0)
  - Requires permission + ManualOverrideReason
- `RateSource = 'UNRESOLVED'`:
  - Rate = 0, NetRate = 0, Amount = 0
  - IsPriceMissing = true
  - ProductId may be missing

**Enforcement layer:**
- **Primary:** Service validation (pricing service)
- **Secondary:** Business logic in rate calculation
- **Validation point:** On rate update, on RateSource change

**Example:**
```php
// PRICELIST source
RateSource: 'PRICELIST'
Rate: 50.00  // From prices table
Discount: 10%
NetRate: 45.00  // ✅ Consistent

// FIXED_NO_DISCOUNT source
RateSource: 'FIXED_NO_DISCOUNT'
Rate: 50.00  // Manual entry
Discount: 0  // ✅ Forced to 0 by G6
NetRate: 50.00  // ✅ No discount applied
```

---

### G5: UNRESOLVED Normalization Rules

**What it means:**
- When RateSource = 'UNRESOLVED', all pricing-related fields must be normalized
- UNRESOLVED indicates item cannot be priced (missing product or price)
- Ensures consistent state for unresolved items

**When it applies:**
- When RateSource is set to 'UNRESOLVED'
- When ProductId is missing
- When price lookup fails
- During item resolution workflow

**Normalization rules:**
- If `RateSource = 'UNRESOLVED'`:
  - `Rate` → 0
  - `NetRate` → 0
  - `Amount` → 0
  - `IsPriceMissing` → true
  - `Discount` → 0 (or NULL)
- Cannot transition from UNRESOLVED to other RateSource without setting ProductId and rate

**Enforcement layer:**
- **Primary:** Service validation (pricing service)
- **Secondary:** Business logic in rate calculation
- **Validation point:** On RateSource change, on price calculation

**Example:**
```php
// UNRESOLVED state
RateSource: 'UNRESOLVED'
ProductId: NULL  // Missing
Rate: 0  // ✅ Normalized
NetRate: 0  // ✅ Normalized
Amount: 0  // ✅ Normalized
IsPriceMissing: true
Discount: 0
```

---

### G6: FIXED_NO_DISCOUNT Forces Discount=0

**What it means:**
- When RateSource = 'FIXED_NO_DISCOUNT', discount must be zero
- FIXED_NO_DISCOUNT indicates rate is fixed and cannot be discounted
- Prevents discount application on fixed-rate items

**When it applies:**
- When RateSource is set to 'FIXED_NO_DISCOUNT'
- When attempting to apply discount to FIXED_NO_DISCOUNT item
- During discount calculation

**Normalization rules:**
- If `RateSource = 'FIXED_NO_DISCOUNT'`:
  - `Discount` → 0 (forced)
  - `NetRate` = `Rate` (no discount applied)
  - Discount field is disabled/read-only in UI
- If discount is attempted on FIXED_NO_DISCOUNT item:
  - Discount is silently set to 0
  - Warning logged (optional)

**Enforcement layer:**
- **Primary:** Service validation (discount service)
- **Secondary:** Business logic in discount calculation
- **Validation point:** On discount update, on RateSource change

**Example:**
```php
// FIXED_NO_DISCOUNT item
RateSource: 'FIXED_NO_DISCOUNT'
Rate: 50.00
Discount: 0  // ✅ Forced to 0
NetRate: 50.00  // ✅ No discount applied

// Attempt to set discount
RateSource: 'FIXED_NO_DISCOUNT'
Discount: 10  // ❌ Attempted
// System normalizes: Discount → 0
```

---

### G7: Discount is Percentage-Based and Range-Validated (0-100)

**What it means:**
- All discounts are percentage-based (0-100%)
- Discount values must be within valid range
- Discount is applied as: NetRate = Rate × (1 - Discount/100)

**When it applies:**
- When setting discount value
- During discount calculation
- When importing discount data
- During price recalculation

**Normalization rules:**
- Discount must be between 0 and 100 (inclusive)
- If discount < 0: normalize to 0
- If discount > 100: normalize to 100 (or reject with error)
- Discount is stored as decimal (e.g., 10.5 for 10.5%)
- Special case: FIXED_NO_DISCOUNT forces discount = 0 (G6)

**Enforcement layer:**
- **Primary:** Database constraint (CHECK constraint: discount >= 0 AND discount <= 100)
- **Secondary:** Service validation (discount service)
- **Validation point:** On discount update, on save

**Example:**
```php
// Valid discount
Discount: 10  // ✅ 10%
NetRate: 45.00  // Rate 50.00 × (1 - 10/100) = 45.00

// Invalid discount (normalized)
Discount: 150  // ❌ Out of range
// System normalizes: Discount → 100 (or rejects with error)

// Zero discount
Discount: 0  // ✅ No discount
NetRate: 50.00  // Rate unchanged
```

---

### G8: L1-SKU Reuse is Allowed and Expected

**What it means:**
- Multiple L1 intent lines can legally map to the same L2 SKU (many-to-one relationship)
- Same SKU can serve multiple L1 interpretations (e.g., AC1 and AC3 ratings for same SKU)
- SKU reuse is expected and correct behavior, not an error
- Engineers validate attributes and interpretations, not SKU uniqueness

**When it applies:**
- When creating or updating L1 intent lines
- When mapping L1 lines to L2 SKUs
- During L1 → L2 explosion logic
- During L1 validation

**Normalization rules:**
- Multiple L1 lines can map to the same `catalog_sku_id` in `l1_l2_mappings` table
- L1 validation must NOT reject SKU reuse
- UI must NOT assume 1 L1 → 1 SKU relationship
- Validation should check L1 attributes (Duty, Rating, Voltage, etc.), not SKU uniqueness
- Example: LC1E0601 SKU can map to:
  - L1-A: AC1, 20A, 3P, 220V
  - L1-B: AC3, 6A, 3P, 220V
  - L1-C: AC1, 20A, 3P, 415V
  - L1-D: AC3, 6A, 3P, 415V
  - All map to same SKU (LC1E0601) ✅

**Enforcement layer:**
- **Primary:** Service validation (L1 validation service)
- **Secondary:** Business logic in L1 → L2 explosion
- **Validation point:** On L1 creation/update, on L1 → L2 mapping, during explosion

**Example:**
```php
// Valid: Multiple L1 lines mapping to same SKU
L1 Line A:
  Duty: AC1
  Rating: 20A
  Voltage: 220V
  Poles: 3P
  → Maps to SKU: LC1E0601 ✅

L1 Line B:
  Duty: AC3
  Rating: 6A
  Voltage: 220V
  Poles: 3P
  → Maps to SKU: LC1E0601 ✅ (Same SKU, different interpretation)

// Invalid: Rejecting SKU reuse
L1 Line A → SKU: LC1E0601
L1 Line B → SKU: LC1E0601
// ❌ System rejects: "SKU already mapped" (WRONG - violates G8)
// ✅ System allows: SKU reuse is expected
```

---

## Enforcement Summary

| Guardrail | Primary Enforcement | Secondary Enforcement | Validation Point |
|-----------|---------------------|----------------------|------------------|
| G1 | Service (Model Boot) | DB Constraint | Before save |
| G2 | Service (Model) | DB Constraint | Before save, before finalize |
| G3 | Service (Pricing) | DB Trigger | On price calculation |
| G4 | Service (Pricing) | Business Logic | On rate update |
| G5 | Service (Pricing) | Business Logic | On RateSource change |
| G6 | Service (Discount) | Business Logic | On discount update |
| G7 | DB Constraint | Service (Discount) | On discount update, on save |
| G8 | Service (L1 Validation) | Business Logic | On L1 creation/update, on L1→L2 mapping |

---

## References

- `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` - Section 1.2 (Validation Guardrails)
- `SPEC_5_FREEZE_GATE_CHECKLIST.md` - Section 4 (Validation Guardrails G1-G8)
- `ITEM_MASTER_DETAILED_DESIGN.md` - Resolution Status and Guardrail Implementation
- `L1_L2_EXPLOSION_LOGIC.md` - L1/L2 differentiation and explosion rules
- `PHASE_5_PRICE_LIST_IMPACT_ASSESSMENT.md` - L1/L2 differentiation requirements

---

## Change Log

### v1.1 (2025-01-27) - UPDATED

**Updates:**
- Added G8: L1-SKU reuse is allowed and expected
- Updated enforcement summary table
- Updated references to include L1/L2 documents

**Change Reason:** Phase 5 impact assessment - L1/L2 differentiation and SKU reuse requirements

---

### v1.0 (2025-01-27) - FROZEN

- Initial canonical definition of G1-G7 guardrails

**Freeze Date:** 2025-01-27  
**Freeze Reason:** Frozen after Phase-5 Senate review. All Step-1 requirements verified and approved.

---

**Status:** FROZEN  
**Frozen:** 2025-01-27 after Phase-5 Senate review

