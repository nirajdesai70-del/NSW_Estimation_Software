# 📘 NEPL / NSW Estimation

## Master Fundamentals + Catalog & Resolution Standard

**Version:** v2.0 (Consolidated Master — Duplication Removed, Nothing Omitted)  
**Status:** DRAFT FOR FREEZE  
**Date:** 2025-01-XX  
**Applies To:** Item Master, Catalog building, Master BOM, Proposal/Production BOM, OEM price list imports, pricing refresh, L0/L1/L2 logic, multi-SKU explosion, vendor variability, reuse/editability, validation, audit

---

### A.0) Legacy vs NSW Semantic Boundary (Critical)

**⚠️ IMPORTANT:** This document defines **NSW canonical semantics for Phase 5**, not legacy semantics.

**Two Truth Layers:**
- **Legacy Truth:** Current production database and UI behavior (operational truth for legacy/V2 runtime only)
- **NSW Truth:** Clean rebuild with redefined semantics (future canonical truth for NSW only)

**Explicit Rule:**
- ❌ **FORBIDDEN:** No one may claim "legacy category/subcategory/type = NSW category/subcategory/type" without an explicit mapping document
- ✅ **REQUIRED:** Phase 5 defines NSW canonical model separately from legacy
- ✅ **REQUIRED:** Any semantic equivalence claims must be documented in a separate mapping project

**Phase 5 Applicability:**
- This document governs Phase 5 Data Dictionary and Canonical Schema design
- Phase 4 (Legacy Stabilization) is complete and separate
- Phase 5 work must respect this boundary to prevent mapping legacy masters to NSW canonical entities

**Reference:** `docs/PHASE_5/LEGACY_VS_NSW_COEXISTENCE_POLICY.md`, `docs/PHASE_5/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md`

---

## A) Executive Rules Snapshot

1. Category ≠ Item/ProductType (even if names sometimes match).
2. SubCategories are additive (a product can have multiple SubCategories at the same time).
3. L0 → L1 → L2 is inheritance-based (once defined, it stays valid at higher levels).
4. Specification does NOT mean specific. Ratings/features are L1 until OEM identity is chosen.
5. L2 requires OEM identity + price reference (Make + OEM Catalog No + PriceListRef).
6. Price updates are versioned (insert new price rows; never overwrite old prices).
7. L1 does NOT own price (all price truth lives at L2/SKU level only).
8. Features are separate L1 lines (not flags on base item) for consistent intent representation.

---

## B) Purpose

This master standard defines the single correct way to model products so that:
- Estimation stays fast (L0/L1 workflow remains practical)
- Product data remains consistent and governable
- OEM price list mapping + frequent updates become repeatable and safe
- Multi-SKU items (base + add-ons) are handled correctly
- Reuse/copy never breaks editability and audit
- Vendor differences are handled transparently at L2 resolution

---

## C) Master Hierarchy (Frozen)

```
CATEGORY
└── SUBCATEGORY (multiple, additive)
     └── ITEM / PRODUCT TYPE (core device)
          └── GENERIC PRODUCT (spec template: L0/L1)
               └── SPECIFIC PRODUCT (OEM SKU + pricing: L2)
```

**Key intent of each layer:**
- **Category** = business grouping
- **SubCategory** = additive configuration capabilities / options
- **Item/ProductType** = engineering object
- **Generic Product** = spec-level template (L0/L1)
- **Specific Product** = OEM orderable SKU (L2)

---

## D) Critical Clarification: Category vs Item/ProductType

### D.1 Definitions

**CATEGORY — Business Classification**

Category answers: "Which broad family does this belong to?"
Used for navigation, reporting, grouping, and catalog organization.
- Stable and limited in count
- Does not define the specification logic
- Not used for OEM resolution

**ITEM / PRODUCT TYPE — Engineering Identity**

Item answers: "What is the actual device being specified and quoted?"
Used to enforce L1 completeness and guide OEM mapping at L2.
- Drives mandatory attributes
- Drives L1 validation
- Drives L2 matching

### D.2 Golden Rule (Locked)

Category is a grouping bucket. Item/ProductType is the engineering object.
Even when names match (e.g., "ACB"), their roles are still different.

### D.3 Proof: Examples where Category ≠ Item (Mandatory Reference)

| Scenario | Category | Item/ProductType |
|----------|----------|------------------|
| Protection Devices | Protection Devices | ACB / MCCB / MCB / RCCB |
| Motor Control | Motor Control | Contactor / Soft Starter / VFD |
| Control Power | Control Power | Control Transformer / SMPS |
| Instrumentation | Instrumentation | Energy Meter / CT / VT |
| Cables | Cables | LT Power Cable / Control Cable / Instrument Cable |
| Automation | Automation | PLC / HMI / I/O Module |
| Panel Accessories | Panel Accessories | Fan / Space Heater / Panel Light |

✅ **Governance rule:** If a Category contains more than one possible Item, Category and Item are obviously not the same concept.

**⚠️ Note on Examples:**
In legacy DB, Category name may equal Item name (e.g., "Category: ACB"). In NSW canonical model, Category must be business grouping (e.g., "Category: Protection Devices"), and Item is the engineering identity (e.g., "Item: ACB"). All examples in this document use NSW canonical structure unless explicitly marked as legacy examples.

---

## E) SubCategory Model (Additive Composition Standard)

### E.1 Definition

SubCategory represents a configuration capability or option under a Category.
Multiple SubCategories can apply simultaneously to one product definition.

**SubCategory is not mutually exclusive.**
**It is a compositional feature set.**

### E.2 Example (ACB)

**Category:** ACB (legacy naming; in NEPL this is typically Item/ProductType; business Category can be Protection Devices)

**Possible SubCategories (examples):**
- Mechanical Operated / Manual Operated
- Electrical Operated / Motor Operated
- Shunt Trip
- Closing Coil
- Aux Contacts
- Drawout / Withdrawable
- Fixed

A single ACB definition may use:
- Mechanical/Manual Operated + Shunt Trip + Aux Contacts (together)

### E.3 Important boundary: "Optional items" vs "Standalone SKUs"
- If OEM sells an option only as part of the device configuration, keep it as SubCategory/Attribute.
- If OEM sells it as an independent priced SKU, it may exist as a separate product line (still governed by Category/Item rules).

### E.4 Schema Note: Multi-SubCategory Implementation (NSW Canonical Schema)

**Legacy vs NSW:**
- Legacy DB may store single `SubCategoryId` on Product table (1:1 relationship)
- NSW canonical schema will support multiple SubCategories via junction table (many-to-many relationship)

**NSW Schema Intent:**
- Junction table: `l1_subcategory_selections` (or equivalent)
- Links: `l1_id` → `subcategory_id`
- Allows multiple SubCategories per L1 line (BASE or FEATURE)

**Until Phase 5 schema is built:**
- Treat "multi-SubCategory" as canonical intent (this document)
- Legacy mapping (if ever needed) must handle 1:1 → many-to-many transformation separately

---

## F) What is an "Accessory" (Locked Rule)

Coils / contacts / add-ons (e.g., Shunt Trip Coil, Aux Contacts, Closing Coil, OLR) must not become Item/ProductType.

They exist as:
- SubCategories (capability selection)
- and/or Attributes (technical details like voltage, NO/NC count, range)

**Specific clarification (OLR rule):**
OLR is not an Item/ProductType.
It is handled as SubCategory/Attribute (e.g., "With OLR") attached to a core device chain (commonly Contactor/Motor-control assemblies, and optionally where your estimation model demands it).

### F.2 Standalone Accessory SKU Handling (Locked)

**If an accessory is sold as a standalone priced SKU:**
- It must NOT become a new Item/ProductType
- It becomes: **Feature L1 line (intent) + L2 SKU (commercial)**
- The Feature L1 line links to the base item via `parent_base_l1_id`
- The L2 SKU is resolved per make/series feature policy (ADDON_SKU_REQUIRED)

**Example:**
- Standalone "Shunt Trip Coil" sold separately → Feature L1 line (Feature_Code=SHUNT) + L2 SKU (resolved per vendor)
- NOT → New Item/ProductType called "Shunt Trip Coil"

---

## G) L0 / L1 / L2 Resolution Standard (Inheritance Model)

### G.1 Meaning of each level
- **L0 (Functional intent):** device + feature composition, no ratings
- **L1 (Technical spec):** adds ratings/specs, still non-specific
- **L2 (Specific OEM):** resolves to Make + OEM Catalog No + PriceListRef (+ price)

### G.2 Inheritance rule (Locked)

**Once green, always green.**
Anything defined at L0 remains valid at L1 and L2.
Anything defined at L1 remains valid at L2.
Higher levels add, never remove.

### G.3 L0/L1/L2 Matrix (Corrected Final)

🟢 = present/inherited, ⚪ = not yet defined

| Element | L0 | L1 | L2 |
|---------|----|----|----|
| Category | 🟢 | 🟢 | 🟢 |
| SubCategories (multiple) | 🟢 | 🟢 | 🟢 |
| Item/ProductType | 🟢 | 🟢 | 🟢 |
| Generic Descriptor | 🟢 | 🟢 | 🟢 |
| Functional features (operation/options) | 🟢 | 🟢 | 🟢 |
| Technical ratings (A/kA/V/Poles/etc.) | ⚪ | 🟢 | 🟢 |
| DefinedSpecJson | ⚪ | 🟢 | 🟢 |
| Make | ⚪ | ⚪ | 🟢 |
| Series/Range/Model | ⚪ | ⚪ | 🟢 |
| OEM Catalog No / MPN | ⚪ | ⚪ | 🟢 |
| ProductId (resolved) | ⚪ | ⚪ | 🟢 |
| Price + PriceListRef | ⚪ | ⚪ | 🟢 |

### G.4 ACB example (Locked, correct)
- **L0:** "ACB mechanical/manual operated 4P with shunt"
- **L1:** "ACB 1600A 4P with shunt"
- **L2:** Make + Model + OEM Catalog No + PriceListRef + Price

---

## H) Catalog Objects: Generic Product vs Specific Product

### H.1 Generic Product (ProductType = 1)

**Purpose:** spec template; supports L0/L1 and Master BOM definitions
- No OEM commitment
- No mandatory Make
- Attributes represent the spec

### H.2 Specific Product (ProductType = 2)

**Purpose:** OEM orderable SKU; supports L2 and pricing

**Mandatory (no exceptions):**
- Make
- OEM Catalog No / MPN
- (Recommended) OEM Series/Range/Model label
- PriceListRef linkage via prices

---

## I) Mandatory L1 Attributes (Per Category/Item) — Standard Set (Minimum)

L1 must be "spec-ready". These are minimum mandatory fields.

### I.1 ACB / MCCB

**Mandatory:**
- Rated Current (A)
- Poles (3P/4P)
- Breaking Capacity (kA)

**Optional (feature-level):**
- Operation Type (Mech/Manual / Elec/Motor)
- Shunt Trip (Y/N) + voltage (if Y)
- Closing Coil (Y/N) + voltage (if Y)
- Aux Contacts (count/type)
- Drawout/Fixed

### I.2 MCB

**Mandatory:**
- Rated Current (A)
- Poles
- Curve (B/C/D)

**Optional:**
- Breaking capacity

### I.3 RCCB

**Mandatory:**
- Rated Current (A)
- Poles
- Sensitivity (mA)
- Type (AC/A/B)

**Optional:**
- Breaking capacity (if relevant)

### I.4 Contactor (Motor Control)

**Mandatory:**
- AC3 Rating (A)
- Coil Voltage
- Poles

**Optional:**
- With OLR (Y/N) + OLR range (if Y)
- Aux contacts

### I.5 VFD

**Mandatory:**
- Motor kW/HP
- Supply voltage
- Output current

**Optional:**
- Communication protocol
- IP rating / enclosure

### I.6 Soft Starter

**Mandatory:**
- Motor kW/HP
- Supply voltage
- Current rating

**Optional:**
- Bypass requirement

### I.7 Cables

**Mandatory:**
- Conductor (Cu/Al)
- Cores
- Size (sqmm)
- Voltage grade

**Optional:**
- Armour

### I.8 Control Power (Transformer / SMPS)

**Mandatory:**
- Input voltage
- Output voltage
- VA rating (transformer) / current rating (SMPS)

### I.9 Instrumentation (Energy Meter)

**Mandatory:**
- Voltage system (1P/3P)
- Class
- Communication requirement (if applicable)

---

## J) Mandatory L2 Fields (OEM Specific) — Locked

A product is L2 only if all below are present:
- Make
- OEM Catalog No / MPN
- PriceListRef
- Currency
- Region
- Effective date for pricing

**L2 Validation Rule (Hard):**
If Make or OEM Catalog No is missing → NOT L2.
If PriceListRef is missing → price cannot be treated as OEM price list driven.

---

## K) OEM Price List Compatibility Standard

### K.1 Why this exists

OEM price lists change frequently. NEPL must support:
- repeated imports
- versioning
- safe updates
- historical audit

### K.2 Mapping keys (Locked)

**Primary matching key:**
- (Make + OEM Catalog No)

Never match by description as the primary key.

### K.3 Pricing policy (Locked)
- Never overwrite old prices
- Insert new price rows with effective dates
- Quotation refresh updates only PRICELIST-based items

---

## L) Price Data Structure Standard (Minimum Fields)

Price record must contain:
- ProductId
- Rate
- EffectiveFrom
- Currency (default INR if India)
- Region (default INDIA)
- PriceListRef (document/version label)

**Recommended:**
- PriceListVersion
- EffectiveTo (optional)

---

## M) Standard Import + Update SOP (OEM Price List)

**Step 1 — Import raw rows (staging)**
Store OEM sheet rows as-is (staging table or import log):
- OemName/Make
- OemCatalogNo
- Description
- Rate
- Currency
- EffectiveFrom
- PriceListRef

**Step 2 — Match or create Specific Products**
For each row:
- match by (Make + OemCatalogNo)
- if missing:
  - create Specific Product (ProductType=2)
  - link to Generic Product via GenericId (manual or guided mapping)
  - set lifecycle ACTIVE

**Step 3 — Insert price record (versioned)**
- add new price row (do not overwrite)
- set effective date + pricelist reference

**Step 4 — Refresh quotations safely**
Only items with:
- RateSource = PRICELIST
are refreshed. Manual overrides remain untouched.

### M.5 Import Governance Roles (ADR-005 Alignment)

**Mapping Approval:**
- Generic Product → Specific Product mapping is governed by **Engineering/Admin role only**
- Mapping must be approved before import completes
- No runtime auto-create mapping during quotation usage (tie to ADR-005 firewall)

**Import Process:**
1. **Staging:** Raw import rows stored in staging table
2. **Validation:** Check for unknown masters (Make, Generic Product, etc.)
3. **Approval Queue:** Unknown masters queued for admin approval/mapping
4. **Approved Import:** Only proceed after all masters resolved and mapping approved
5. **Audit Trail:** All mapping decisions logged with approver, timestamp, reason

**Forbidden:**
- ❌ Runtime auto-creation of Generic Product mapping during import
- ❌ Auto-create mapping during quotation usage
- ❌ Import completion without approval for unknown masters

**Reference:** `docs/PHASE_5/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md`

---

## N) Data Entry Templates (Ready-to-use)

### N.1 L0/L1 Generic Product Template

| Field | Example |
|-------|---------|
| Category | ACB (legacy naming; NEPL category can be Protection Devices) |
| SubCategories (multi) | Mechanical Operated; Shunt Trip; Aux Contacts |
| Item/ProductType | ACB |
| Generic Descriptor (L0) | ACB mechanical 4P with shunt |
| DefinedSpecJson (L1) | {RatedCurrent:1600A, Poles:4P, kA:65, ShuntTrip:true} |

### N.2 L2 Specific Product Template

| Field | Example |
|-------|---------|
| GenericId | (link to L1 generic) |
| Make | Schneider |
| OEM Series/Range | Masterpact MTZ |
| OEM Catalog No / MPN | MTZ2-16-H1-ST |
| LifecycleStatus | ACTIVE |

### N.3 OEM Price Import Template

| Field | Example |
|-------|---------|
| Make | Schneider |
| OEM Catalog No | MTZ2-16-H1-ST |
| Rate | 125000 |
| Currency | INR |
| EffectiveFrom | 2025-01-01 |
| PriceListRef | Schneider India Pricelist Jan 2025 |

---

## O) 10-Category Validation Examples (Must be used for testing)

| # | Category | Item/ProductType | L0 (Functional) | L1 (Spec) | L2 (Specific) |
|---|----------|------------------|-----------------|-----------|---------------|
| 1 | Protection Devices | ACB | Mech + Shunt | +1600A 4P 65kA | Make+CatalogNo+PriceListRef |
| 2 | Protection Devices | MCCB | Fixed trip | +100A 3P 25kA | Make+CatalogNo+PriceListRef |
| 3 | Protection Devices | MCB | Curve C | +16A 1P 10kA | Make+CatalogNo+PriceListRef |
| 4 | Protection Devices | RCCB | Type A | +63A 4P 30mA | Make+CatalogNo+PriceListRef |
| 5 | Motor Control | Contactor | With OLR (feature) | +25A AC3 Coil 230VAC | Make+CatalogNo+PriceListRef |
| 6 | Motor Control | VFD | Comm required | +15kW 415V | Make+Model+PriceListRef |
| 7 | Motor Control | Soft Starter | Bypass req | +30kW 415V | Make+Model+PriceListRef |
| 8 | Cables | LT Power Cable | Armoured | +3.5C 240sqmm 1.1kV | Brand+construction code+PriceListRef |
| 9 | Instrumentation | Energy Meter | Comm required | +Class 1, 3P | Make+Model+PriceListRef |
| 10 | Control Power | SMPS / Transformer | Panel supply | +415/24V, rating | Make+Model+PriceListRef |

---

## P) Governance & Hard Validation Rules (Mandatory)

1. Every product record must have: Category, Item/ProductType
2. SubCategories are selectable as multi-set, not single-choice.
3. L0/L1 are not specific by definition.
4. L2 requires: Make + OEM Catalog No + PriceListRef
5. No accessory terms (OLR, shunt trip, aux contact, closing coil) may be created as Item/ProductType.
6. Price imports must match by (Make + OEM Catalog No), not by description.
7. L1 does NOT own price (all price truth lives at L2/SKU level only).
8. Features are separate L1 lines (base + feature lines grouped).

---

## Q) Final Freeze Statement (Authoritative)

NEPL uses a device-centric, inheritance-based catalog model.
Category is business classification. Item/ProductType is engineering identity.
SubCategories are additive and define configuration capabilities.
L0 defines intent, L1 defines ratings, L2 defines OEM commitment via Make + OEM Catalog No + PriceListRef.
All definitions persist across levels. This standard is permanent.

---

## R) NSW Estimation Fundamentals Layer (General, Not Catalog-Only)

### R.1 Core Doctrine (Non-Negotiable)
- Intent must be separated from Commerce.
- Structure must be separated from Price.
- Reuse must never reduce editability.

### R.2 Objects and Levels (Canonical)

#### R.2.1 L0 — Concept / Template Layer (Mandatory)

**Contains:**
- Category
- Item/ProductType
- Allowed SubCategories (definitions only)
- Allowed Attributes (definitions only)
- Default assumptions (optional)

**Does NOT contain:**
- Quantity
- Project context
- SKU
- Price
- Vendor

#### R.2.2 L1 — Logical Line Item (Intent + Spec)

**Contains:**
- Selected SubCategories
- Attribute values (Value + Unit)
- Feature intent (represented as separate L1 feature lines; see Section V)
- Quantity
- Notes

**Does NOT contain:**
- SKU
- Price ownership

#### R.2.3 L2 — SKU Line Items (Commercial Layer)

**Rules:**
- Each L2 row = exactly one SKU
- Each L2 row must reference parent L1
- 1 L1 → N L2 is valid and expected

---

## S) SubCategory vs Attribute Doctrine (Exhaustive, No Gaps)

### S.1 Memory Rule
- **SubCategory** decides "IS THIS INCLUDED?"
- **Attribute** decides "WITH WHAT VALUE / RATING?"

### S.2 SubCategories (Layered, Additive)
- **SC_L1** — Construction/Form (Fixed/Withdrawable/Armoured/Unarmoured)
- **SC_L2** — Operation/Actuation (Manual/Electrical/Motor)
- **SC_L3** — Functional Features (UV/OV/Shunt/Shielded/Earth Fault)
- **SC_L4** — Accessories (Aux contacts/alarms/interlocks)

**Rules:**
- Not numeric
- Not priced
- Not SKU
- Multiple can apply

### S.3 Attributes (Key–Value–Unit) (Locked)

All attributes are stored as:
- AttributeCode
- AttributeValue
- AttributeUnit

Unit remains fixed for that AttributeCode; only value changes.

**Applicability:**
- Item-level attributes (always applicable)
- SubCategory-linked attributes (conditional; must not exist if SubCategory not selected)

### S.4 Composite Attribute: Voltage (Locked)

Voltage is an attribute group:
- VOLTAGE_TYPE = AC/DC
- VOLTAGE_VALUE = 24/48/110/230/415
- FREQUENCY = 50/60 Hz (AC only)

Voltage is never a SubCategory.

### S.5 Strict Forbidden
- Add-ons as attributes with price
- Numeric values as SubCategories
- Mixed tokens "1600A" stored as one field
- SKUs at L1
- SubCategories with numeric values

---

## T) Multi-SKU, L1→L2 Explosion + Vendor Variability (LOCKED GOVERNANCE)

### T.1 Core Problem (Clarified)

A single selected item may consist of:
- Base item SKU (main device)
- Multiple add-on / sub-category SKUs (UV, OV, Shunt, Aux, etc.)

Add-ons may have independent part numbers and prices and are conditionally applicable.
If not modeled properly:
- Price import breaks
- BOM explodes incorrectly
- Future reuse/edit becomes unsafe

### T.2 Principle to Lock (Non-Negotiable)

SKU ≠ Item ≠ BOM Line
They are related, but not the same object.

### T.3 Canonical Model (Recommended)

#### T.3.1 Item (Logical Selection Layer)

What user selects in UI.
**No price here.**

#### T.3.2 SKU (Commercial / Part Layer)

Base SKU (mandatory) and add-on SKU (optional, conditional).
Each SKU has supplier part number, price, validity, brand mapping.

#### T.3.3 Item–SKU Mapping Table (Key Table)

**Fields:** item_id, sku_id, role, rule_expression, qty_formula, sequence, mapping_rule_id (recommended)

Mapping is engineering-controlled, not catalog-imported.

### T.4 Catalog Price Import (SKU-only, Locked)
- Import SKU master + SKU price records (versioned)
- Do not import item definitions, feature logic, or item–SKU mapping

### T.5 L1 → L2 Explosion Layer (Mandatory)
- 1 L1 → N L2 is expected
- Each L2 row = one SKU
- Each L2 row references parent L1 (or parent L1 group; see pseudocode section AA.2)

**Pricing roll-up (clarified):**

BOM / Quotation totals are computed by summing L2 lines (derived, not stored at L1).

**Trigger + idempotency (clarified):**

Snapshot → clear L2 children → regenerate using mapping + make/series feature policy → apply allowed overrides → recompute derived totals.

### T.6 Vendor Variability (Make/Series Context)

**Patterns:**
- INCLUDED_IN_BASE
- ADDON_SKU_REQUIRED
- BUNDLED_ALTERNATE_BASE_SKU

**Feature policy table:**
make, series, item_type, feature, handling_type, sku_id/rule
**Priority:** series → make → global → else BLOCK

### T.7 Validation Gates
- Base SKU missing → HARD BLOCK
- Feature selected but policy missing → HARD BLOCK
- ADDON required but SKU missing → HARD BLOCK
- INCLUDED but base SKU missing in catalog → HARD BLOCK
- L2 orphan lines → INVALID STATE

### T.8 Audit & History

Track before/after L2 sets, trigger source, actor, timestamp, regen/manual/import indicator.

---

## U) Pricing Ownership — Corrected and Locked (Patch Integrated)

### U.1 What must NOT be stated
- "L1 Total = Σ (L2 Qty × L2 Unit Price)" as a stored/owned value
- "L1 has price" directly or indirectly

### U.2 Correct model
- L1 does NOT store price
- L2 owns unit price (SKU truth)
- BOM/quotation totals are derived from L2

---

## V) L1 Feature Lines Standard (LOCKED)

### V.1 Standardized intent representation
- **One BASE L1 line** = main item intent/spec
- **Separate FEATURE L1 lines** = UV/OV/Shunt/Aux/Shield/Armour/etc.
- **Grouped by L1_Group_Id**

### V.2 L2 resolution per make/series

Each FEATURE L1 line resolves into one of:
- **INCLUDED_IN_BASE** → no L2 SKU line
- **ADDON_SKU_REQUIRED** → one L2 SKU line
- **BUNDLED_ALTERNATE_BASE** → swap base SKU, no feature SKU line

### V.3 Minimal data structure

**L1:**
- l1_group_id
- l1_line_type (BASE/FEATURE)
- feature_code (FEATURE)
- parent_base_l1_id (FEATURE → BASE)

**L2:**
- parent link (BASE or FEATURE line)
- resolution_type (INCLUDED/ADDON/BUNDLED_BASE)
- resolved_sku_id (if any)

### V.4 Feature Lines vs SubCategory vs Attribute Bridge (Critical)

**When to use Feature Lines:**
- Feature lines are the UI-visible intent record for features that may affect SKU explosion
- Use Feature lines when the feature:
  - May require separate SKU (ADDON_SKU_REQUIRED per vendor)
  - May affect base SKU selection (BUNDLED_ALTERNATE_BASE)
  - Needs explicit visibility in estimation intent (UV, OV, Shunt, Aux, Shield, Armour, etc.)

**When SubCategory selection remains on BASE line:**
- Use SubCategory selection when the feature:
  - Is purely descriptive (doesn't affect SKU explosion)
  - Is always INCLUDED_IN_BASE for all vendors
  - Doesn't need separate L1 line representation

**Bridge Rule:**
- **SubCategory selection** can either:
  - Remain as selection on BASE line (simple cases)
  - OR become one FEATURE line (recommended when it affects SKU explosion or vendor variability)
- **Attributes** always attach to L1 lines (BASE or FEATURE) via GENERIC_ATTRIBUTES table
- **Feature lines** make vendor variability explicit and traceable at L1 intent layer

**Example Decision Tree:**
- "Shunt Trip" → Feature line (affects SKU explosion per vendor)
- "Fixed" vs "Withdrawable" → SubCategory on BASE (always INCLUDED, no SKU impact)
- "Armoured" → Feature line (affects SKU/cost per vendor)

---

## W) Attribute Set Model + UX Controls (v1.3+ and v1.3.1)

### W.1 Universal attribute-set model
- GENERIC_MASTER (intent rows)
- GENERIC_ATTRIBUTES (KVU rows)
- ATTRIBUTE_MASTER (dictionary + validation)

### W.2 Value + Unit separation

Unit fixed per code; value changes.

### W.3 Friendly entry (dropdown / range)
- picklists for discrete values
- numeric range for continuous values

---

## X) Cable Handling Capability (Must be supported)

Cable system must support:
- **Category** = Cables
- **Item/ProductType** = Power Cable / Control Cable / Instrument Cable
- **SubCategories:** armour/shielding variants as additive selections
- **Attributes:** voltage grade, size, conductor material/finish, cores/pairs, armour type, shield material/coverage, sheath/insulation types, etc.

---

## Y) Use & Governance Roles (RBAC for Phase 5)

### Y.1 Master Data Creation Roles

**Category / SubCategory / Item/ProductType Creation:**
- **Role:** Admin only
- **Access:** MASTER module UI-only creation forms
- **Audit:** All creation must be logged (who/when/why)
- **Forbidden:** Runtime auto-creation (enforced by ADR-005 firewall)

**Generic L1 Product Templates:**
- **Role:** Engineering
- **Access:** MASTER module template creation/editing
- **Purpose:** Define spec templates for Master BOM usage
- **Audit:** Template creation/edits logged

**Specific L2 Product (SKU) Creation:**
- **Role:** Admin / Procurement (with Engineering approval for mapping)
- **Access:** Via controlled import pipeline (pre-approved masters only)
- **Purpose:** Create orderable SKUs from OEM price lists
- **Audit:** All SKU creation logged with price list reference

**Price List Import:**
- **Role:** Procurement / Admin (staging)
- **Approval:** Engineering approval required for Generic→Specific mapping
- **Process:** Staging → Validation → Approval Queue → Approved Import
- **Audit:** All import decisions logged (see Section M.5)

**Price Override in Quotations:**
- **Role:** Quotation role (permission-based)
- **Access:** Manual override with audit trail
- **Restriction:** Only for specific quotation context, not master data change

### Y.2 Import Governance Alignment

All import processes must align with:
- **ADR-005:** Master Data Governance Firewall (no auto-create)
- **Section M.5:** Import Governance Roles (approval workflow)
- **Phase 5 Schema:** Approval queue tables support (import_pending_master_approval_queue, import_decision_log, etc.)

### Y.3 Phase 5 RBAC Design Requirements

Phase 5 schema and service design must support:
- Role-based creation permissions (Admin, Engineering, Procurement)
- Approval queue workflows (for unknown masters, mapping decisions)
- Audit trails (who created what, when, why, approved by whom)
- Firewall enforcement (no runtime auto-create outside MASTER module)

---

## Z) Governance Freeze Statements

### Z.1 Fundamentals Freeze

This document defines the fundamental meaning, level, reuse behaviour, and derivation of all NSW Estimation objects. Catalog, pricing, BOM, UI, and AI logic are derived implementations, not independent definitions.

### Z.2 Catalog & Resolution Freeze

This document defines the only correct interpretation of Catalog, Item, Feature, SKU, and BOM behaviour in NSW Estimation. Any implementation, import, or UI flow not aligned with this document is invalid.

---

## AA) Implementation Specifications (Integrated Deliverables)

**See also:** `v1.3_WORKBOOK_README.md` for philosophy, usage guide, and Do/Don't checklist.

### AA.1 PART 1 — v1.3.2 Excel Layout (Final, Feature-as-Separate-L1)

#### Sheet: GENERIC_MASTER (L1 — Intent Layer)

**Identity & grouping**
- L1_Id
- L1_Group_Id
- L1_Line_Type (BASE/FEATURE)
- Parent_Base_L1_Id (FEATURE only)
- Feature_Code (FEATURE only)

**Engineering definition**
- Category
- Item_ProductType
- GenericLevel (L0/L1)
- GenericDescriptor

**Configuration**
- SC_L1_Construction
- SC_L2_Operation
- SC_L3_FeatureClass
- SC_L4_AccessoryClass

**Governance**
- Requested_By_User
- Notes
- Status

#### Sheet: GENERIC_ATTRIBUTES (KVU)
- L1_Id (links to BASE/FEATURE)
- AttributeCode
- AttributeValue
- AttributeUnit
- ValueType
- AppliesToFeature
- Confidence
- Source

#### Sheet: ATTRIBUTE_MASTER (Dictionary + Validation + Dropdown Control)

**Required columns:**
- AttributeCode (PK, unique)
- AttributeName
- DataType (NUMBER/ENUM/BOOL/TEXT)
- FixedUnit (unit locking per code)
- ValueEntryMode (PICKLIST / NUMERIC_RANGE / FREE_TEXT)
- AllowedValuesList (for PICKLIST mode)
- MinValue, MaxValue, Step (for NUMERIC_RANGE mode)
- AppliesTo_ItemProductType (nullable)
- AppliesTo_SubCategory (nullable)
- RequiredAtLevel (L1 mandatory / optional)
- ValidationRule (optional)

**Purpose:** Controlled dictionary to avoid column explosion. Supports ACB + Cable + Meter + Lug without changing sheet structure.

---

#### Sheet: FEATURE_MASTER (Feature Code Dictionary)

**Required columns:**
- Feature_Code (PK, unique: UV, OV, SHUNT, AUX, SHIELD, ARMOUR, etc.)
- Feature_Label (human-readable name)
- AppliesTo_ItemProductType (nullable - if null, applies to all)
- DefaultRequired (BOOLEAN, optional)
- Feature_Description (TEXT, optional - for documentation)

**Purpose:** Standardizes feature codes, prevents typos, supports data quality. Follows controlled dictionary pattern (like ATTRIBUTE_MASTER).

---

#### Sheet: MAKE_SERIES_FEATURE_POLICY (Vendor Variability Control)

**Required columns:**
- Make (FK or text)
- Series (nullable, FK or text)
- Item_ProductType (FK or text)
- Feature_Code (FK to FEATURE_MASTER)
- Handling_Type (ENUM: INCLUDED_IN_BASE / ADDON_SKU_REQUIRED / BUNDLED_ALTERNATE_BASE)
- Priority (INTEGER: 1=Series-specific, 2=Make-specific, 3=Global default) - **Required for deterministic resolution**
- Addon_SKU_Code (nullable, text - SKU code if ADDON)
- Base_Variant_Rule (nullable, text - rule expression if BUNDLED)
- EffectiveFrom (DATE, optional - for policy versioning)
- EffectiveTo (DATE, optional - for policy versioning)

**Purpose:** Bridge from L1 feature lines → L2 SKU behavior. Handles vendor variability (Schneider vs ABB/Siemens) cleanly.

**Resolution Priority (enforced by Priority column):**
1. Series-specific (Priority=1)
2. Make-specific (Priority=2)
3. Global default (Priority=3)
4. Else → BLOCK (no policy = error)

**Reference:** Section T.6 (Vendor Variability), Section AA.2 (L2 Explosion Pseudocode)

---

### AA.2 PART 2 — L2 Explosion Service (Final Pseudocode)

```
function explode_L1_group_to_L2(group_id, make, series):

    base_line = get L1 where group_id and L1_Line_Type='BASE'
    feature_lines = get L1 where group_id and L1_Line_Type='FEATURE'

    archive_L2_lines(group_id)
    delete L2 lines where parent_group_id = group_id

    base_sku = resolve_base_sku(item_type, make, series, base_attributes)
    resolved_base_sku = base_sku

    L2_lines = []

    for feature in feature_lines:
        policy = get_feature_policy(item_type, feature_code, make, series)
        if policy missing: HARD_ERROR

        if INCLUDED_IN_BASE: continue
        if ADDON_SKU_REQUIRED: add L2 line linked to FEATURE with sku_id
        if BUNDLED_ALTERNATE_BASE: resolved_base_sku = apply_base_variant_rule(...)

    prepend L2 BASE line linked to BASE with resolved_base_sku
    save L2_lines
    recompute BOM totals (derived only)
    return L2_lines
```

**Guarantees:**
- 1 L1 Group → 1..N L2 lines
- No double counting
- Vendor variability handled
- Features visible at L1
- Prices only at SKU/L2
- Fully idempotent
- Audit-safe

---

## ✅ Freeze Checkpoint

When you're satisfied, reply with exactly:

**"Freeze Master Doctrine v2.0"**

…and we proceed to the next three derived artifacts (DB schema, CSV templates, service specs) strictly from this document.

---

**END OF MASTER FUNDAMENTALS v2.0**
