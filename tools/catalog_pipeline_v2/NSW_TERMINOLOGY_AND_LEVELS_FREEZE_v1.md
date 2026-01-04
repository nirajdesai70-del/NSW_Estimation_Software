# NSW Terminology & Levels Freeze v1

**Status:** FINAL FOR PROJECT USE  
**Date:** 2025-01-XX  
**Scope:** Naming only (no semantic change), to eliminate confusion across business classification vs engineering configuration vs SKU pricing.

---

## 1) Why this file exists

We discovered repeated confusion because the same words ("Category", "SubCategory") were being used in two different worlds:
1. **Business/Catalog classification**
2. **Engineering configuration/capability selection**

This file introduces non-conflicting terminology while preserving NSW Doctrine v2.0 meaning.

**Reference:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`

---

## 2) The three worlds (frozen)

### World A — Business/Catalog Classification

**Used for:** navigation, reporting, catalog grouping

| Old term | New term | Meaning |
|----------|----------|---------|
| Category | **Business Category** | Business grouping bucket (e.g., Motor Control, Protection Devices) |
| SubCategory (business) | **Business Segment** | Sub-group inside Business Category (e.g., Contactor, MCCB, ACB) |

**Rule:** Business Category/Segment is classification only; it does not define specs or pricing.

**Current Code Usage:** ✅ `business_subcategory` already used in codebase (aligned!)

---

### World B — Engineering Object Model (NSW levels)

**Used for:** specification + resolution path

| Term | Meaning |
|------|---------|
| **Item/ProductType** | Engineering identity of the device (e.g., Contactor, MCCB, ACB, VFD) |
| **L0** | Generic intent template (no numeric ratings) |
| **L1** | Generic spec (numeric ratings/specs; still non-OEM) |
| **L2** | OEM specific SKU (Make + Series/Model + MPN/SKU + PriceListRef + Price) |

**Hard rule:** Make/Series/SKU/Price are L2-only.

**Current Code Usage:** ✅ `item_producttype`, L0/L1/L2 concepts well-established

---

### World C — Engineering Capability Selection

**Used for:** included/excluded options, features, add-ons (not business segment)

| Old term | New term | Meaning |
|----------|----------|---------|
| SubCategory (engineering capability) | **Capability** | Additive option/capability selection (WITH_OLR, AUX_CONTACT, SHUNT, DRAWOUT, etc.) |
| SC_L1…SC_L4 | **Capability_Class_1…4** | Capability grouping axes (construction/operation/functional/accessory class) |
| Feature line | **Feature Line** | Separate L1 line representing feature intent that may affect SKU resolution |

**Rule:** Capability is not numeric, not priced, can be multiple. Numeric values belong to Attributes (KVU) at L1.

**Current Code Usage:** ⚠️ `SC_L1`, `SC_L2`, `SC_L3`, `SC_L4` used extensively (193 matches) - **Phased rename recommended**

**Migration Note:** During transition, code supports both `SC_Lx` and `capability_class_x` for backward compatibility.

---

## 3) Level definitions (frozen)

### L0 (Generic intent)

**Contains:**
- Business Category, Business Segment
- Item/ProductType
- Capability selections (as labels only)
- Generic descriptor

**Does NOT contain:**
- numeric ratings (A/kA/kW/V/Poles)
- make/series/SKU/price

### L1 (Generic spec)

**Adds:**
- numeric ratings/specs via KVU attributes

**Still does NOT contain:**
- make/series/SKU/price

### L2 (Specific OEM)

**Adds:**
- make
- series/model
- OEM catalog number / SKU
- price list reference + price

**Reference:** `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md` (Section 1.1)

---

## 4) Naming conventions (recommended, project-wide)

### Recommended column names

Use these names to avoid collisions:

**Business:**
- `business_category`
- `business_segment`

**Engineering:**
- `item_producttype`
- `l0_code`, `l0_name`
- `l1_code`, `l1_name`

**Capability selection:**
- `capability_codes` (semicolon list or junction table later)
- `capability_class_1` … `capability_class_4` (preferred)
- `SC_L1` … `SC_L4` (legacy, supported during transition)

**Specific:**
- `make`
- `oem_series` or `series_bucket`
- `sku_code` or `oem_catalog_no`
- `price_list_ref`
- `effective_from`, `rate_inr`

**Current Code Alignment:**
- ✅ `business_subcategory` - Already aligned
- ✅ `item_producttype` - Already aligned
- ⚠️ `SC_L1` through `SC_L4` - Legacy, will be renamed to `capability_class_1-4`

---

## 5) Project update instruction (for Cursor)

### What must be updated

1. **Replace generic use of "SubCategory" into:**
   - `business_segment` when referring to classification
   - `capability` when referring to options/features

2. **Ensure all documentation, sheets, and schemas keep:**
   - Business Category/Segment separate from capability selection

3. **Enforce L0/L1/L2 separation:**
   - L0 no ratings
   - L1 ratings (KVU)
   - L2 SKU + price only

4. **Phased SC_Lx rename:**
   - New code: Use `capability_class_1-4`
   - Legacy code: Support both `SC_Lx` and `capability_class_x` during transition
   - Documentation: Use `capability_class_x` terminology

### What must NOT be changed

- ❌ No semantic re-interpretation of NSW Doctrine v2.0
- ❌ Only terminology + column label alignment
- ❌ No breaking changes to active code (phased approach)

---

## 6) Quick examples (for clarity)

### Contactor

- **Business Category:** Motor Control
- **Business Segment:** Contactor
- **Item/ProductType:** Contactor
- **L0:** Power Contactor
- **L1:** Power Contactor – 3P | 2.2kW @ 415V
- **L2:** Schneider LC1E… (SKU) + price
- **Capability:** WITH_OLR; AUX_CONTACT
- **Capability_Class_1:** Base Contactor
- **Capability_Class_2:** AC Coil
- **Capability_Class_3:** AC1 / AC3
- **Capability_Class_4:** AUX (if accessory)

### MCCB

- **Business Category:** Protection Devices
- **Business Segment:** MCCB
- **Item/ProductType:** MCCB
- **L0:** MCCB
- **L1:** MCCB – 100A | 3P | 25kA
- **L2:** Schneider/ABB SKU + price
- **Capability:** SHUNT; UV; AUX_CONTACT
- **Capability_Class_1:** Frame Size
- **Capability_Class_2:** Fixed / Plug-in
- **Capability_Class_3:** Breaking Capacity Class
- **Capability_Class_4:** Accessory Class

---

## 7) Migration path

### Phase 1: Freeze (Immediate)
- ✅ Create this freeze document
- ✅ Update documentation to reference freeze
- ✅ New code uses freeze terminology

### Phase 2: Transition (Short-term)
- ⚠️ Support both `SC_Lx` and `capability_class_x` in code
- ⚠️ Update documentation to use new terminology
- ⚠️ Add `business_` prefix where Category is used

### Phase 3: Full Migration (Medium-term)
- ⚠️ Rename `SC_Lx` → `capability_class_x` in all code
- ⚠️ Remove backward compatibility after full migration
- ⚠️ Update all sheet references

---

## 8) Freeze statement

This terminology is **mandatory** across:
- Documentation
- Excel sheets
- DB schema
- Import pipelines
- UI labels

It is intended to eliminate naming ambiguity while preserving NSW Doctrine v2.0 semantics.

**No semantic changes** - only terminology + column label alignment.

---

## 9) References

- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md` - Master fundamentals
- `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md` - L0/L1/L2 definitions
- `tools/catalog_pipeline_v2/FREEZE_DOCUMENTS_REVIEW.md` - Review and assessment

---

**END OF DOCUMENT**


