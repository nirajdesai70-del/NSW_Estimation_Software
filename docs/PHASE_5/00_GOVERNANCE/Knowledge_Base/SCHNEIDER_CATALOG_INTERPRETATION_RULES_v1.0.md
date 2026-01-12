# Schneider Catalog Interpretation Rules v1.0
## Knowledge Base Decision Document

**Status:** REVIEW_REQUIRED  
**Date:** 2025-01-XX  
**Purpose:** Single authoritative reference for Schneider catalog (Page 8 to End) interpretation, aligned strictly to NSW Estimation Fundamentals v2.0  
**Scope:** LC1E, LP1K, LC1D, MPCB, Control Relays, Capacitor Duty Contactors, Overload Relays, Circuit Breakers, Switches/Isolators  
**Reviewers:** Engineering + Procurement  
**Dependency:** LC1E, LP1K completed; LC1D pending

---

## Document Control

- **Version:** 1.2 (SC_L alignment + duty clarification corrected; no semantic conflicts)
- **Classification:** Engineering Decision
- **Lock Status:** PENDING REVIEW
- **Next Action:** Engineering sign-off required before LC1K processing begins
- **Transfer Path:** Once confirmed → `docs/PHASE_5/ENGINEERING_REVIEW/` or `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/`
- **Last Updated:** 2025-01-XX (v1.2: SC_L alignment + duty clarification corrected)

---

## 0. CRITICAL: L2 Generation Rule (Locked - Do Not Violate)

### 🔒 The Fundamental Truth (NSW Rule)

**L2 rows are NEVER created by combinatorial multiplication.**

**L2 rows = the number of explicitly priced variants shown in the OEM price list (i.e., distinct commercial SKUs).**

**The ONLY valid L2 count formula:**
```
L2_row_count = count(distinct (Make, OEM_Catalog_No)) in price list
```

### What This Means

- ✅ **L2 rows come ONLY from catalog SKUs / priced lines**
- ❌ **No artificial multiplication**
- ❌ **No inferred combinations beyond what OEM priced**
- ❌ **Frame × Poles × Duty × Voltage is NOT an L2 generator** (it's an analysis lens only)

### L2 Row Key (Commercial Truth)

L2 row is uniquely identified by:
- `Make + OEM_Catalog_No` (completed SKU)
- `PriceListRef + EffectiveFrom` (for versioning)

### When Multiple L2 Rows Are Created

L2 rows are created ONLY when:
- ✅ OEM Catalog No changes (including suffix completion) → multiple L2 rows
- ✅ Same base reference but OEM catalog number changes via suffix → multiple L2 rows

**Note:** Price variation is handled via price history records for the same SKU, not by duplicating SKUs.
- ❌ If OEM does not list a combination → we do NOT invent it

### How Frame/Poles/Duty/Voltage Are Used

They are used ONLY to:
- Classify the L2 row (SC_L1..SC_L4 + Attributes)
- Group L2 rows into an L1 template later
- Derive missing L1 fields for engineer completion

**They do NOT generate new SKUs.**

---

## 1. Locked Definitions (Reference - NSW Fundamentals v2.0)

| Concept | NSW Meaning | Notes |
|---------|-------------|-------|
| **Category** | Business grouping (NOT item) | Used for business classification only |
| **Item/ProductType** | Engineering identity | Contactor, Control Relay, MPCB, Circuit Breaker |
| **SubCategory** | Business subcategory (one per L2 row) | Power Contactor, Capacitor Duty Contactor, Control Relay |
| **SC_L1–SC_L4** | Supporting subcategory layers (additive, non-numeric) | Construction, Operation, Feature Class, Accessory Class |
| **Attributes** | KVU (Value + Unit) | Never stored in SC layers |
| **SKU** | Exists only at L2 | Price truth exists only at L2 |
| **Accessories** | SC_L4 and/or Feature L1 lines with L2 SKUs | NOT attributes; NOT items |

**🔒 Hard Rules:**
- Voltage is an Attribute (type + value), never a SubCategory
- SubCategories are additive and non-numeric
- L1 has no price; L2 is SKU-only pricing
- Attributes are KVU only (never mixed tokens)

---

## 2. SC Layer Mapping (Final - Locked)

### 2.1 SC_L1 - Construction / Form

**Purpose:** Physical construction or frame/form factor  
**Nature:** Enumerated, non-numeric  
**Examples:**
- Frame size (Frame 1, Frame 2, Frame 3) - **DERIVED, NOT MULTIPLIER**
- Pole count (2P, 3P, 4P) - **MULTIPLIER ONLY IF SKU CHANGES**
- Fixed / Plug-in

**🔒 Critical Rule 1: Frame is NOT a Multiplier**

Frame is a **derived construction label** (physical size). It does NOT create new L2 rows by itself.

**Frame is determined from:**
- Current rating band
- Mechanical platform
- Sometimes pole count
- Sometimes duty

**Frame assignment rule:**
Frame can be assigned by a deterministic banding table, e.g.:
- `FRAME_1`: AC3 current ≤ 32A
- `FRAME_2`: 33–65A
- `FRAME_3`: 66–115A
- etc.

**This is classification, not multiplication.**

**Causal order (locked):**
```
Pole / voltage / duty (when priced) ⇒ SKU changes ⇒ frame label follows
```

**NOT:**
```
frame ⇒ SKU changes
```

**🔒 Critical Rule 2: Pole is a Multiplier ONLY When OEM Differentiates**

Poles can generate multiple L2 rows ONLY when the catalog provides distinct priced SKUs/lines per pole variant.

- ✅ If 3P vs 4P has different SKU/price → multiple L2 rows
- ❌ If same SKU → single L2 with attribute POLES

**🔒 Critical Rule 3: Frame and Pole Coexistence**

Frame and Pole are BOTH SC_L1 and can coexist:
- `SC_L1 = { FRAME_1, POLE_3 }`
- `SC_L1 = { FRAME_1, POLE_4 }`
- `SC_L1 = { FRAME_2, POLE_3 }`

**Why:** Both define physical construction. They are not alternatives, not mutually exclusive. But Frame is derived, Pole may cause SKU multiplication.

---

### 2.2 SC_L2 - Operation / Actuation

**Purpose:** How the device operates  
**Nature:** Enumerated  
**Examples:**
- AC Coil / DC Coil
- Manual / Electrical
- Rotary / Toggle / Pushbutton

---

### 2.3 SC_L3 - Functional Duty / Class

**Purpose:** Electrical duty or application class  
**Nature:** Enumerated  
**Examples:**
- AC1 / AC3
- Capacitor Duty
- Thermal / Magnetic (for MPCB)

**🔒 Critical Rule: Duty (AC1 / AC3) Handling (LOCKED)**

**Duty (AC1 / AC3) is an ATTRIBUTE, not SKU, unless SKU changes.**

| Condition | NSW Treatment |
|-----------|---------------|
| Same SKU, same price | Single L2 row |
| AC1/AC3 give different currents | Attribute values differ |
| Different SKU for duty | Separate L2 rows |
| Different price for duty | Separate L2 rows |

**Therefore:**
- ✅ AC1 / AC3 only causes L2 multiplication if SKU or price changes
- ❌ Otherwise: AC1, AC3 are engineering attributes at L1
- ❌ They do NOT create extra L2 rows

**Why This Matters:**
- OEM catalogs often show duty rows to communicate engineering limits, not pricing
- Table rows ≠ SKU rows
- Table rows ≠ L2 rows

**Correct Modeling:**
- **L2 (SKU layer):** One row per SKU from price list, price stored once
- **L1 (spec layer):** Multiple attribute sets attached to same SKU context:
  - `DUTY_CLASS = AC1, CURRENT = 20A`
  - `DUTY_CLASS = AC3, CURRENT = 6A`

**This is perfectly aligned with:**
- KVU model
- "Specification ≠ Specific" rule
- L1 owns spec, L2 owns price

---

### 2.4 SC_L4 - Accessory / Extension Class

**Purpose:** Add-on capability blocks  
**Nature:** Enumerated (may repeat)  
**Examples:**
- Aux contacts (1NO/1NC, 2NO/2NC)
- Thermal overload
- Surge suppressor
- Mechanical interlock
- Power connector
- Terminal blocks
- Reversing kits
- Star-delta kits

**🔒 Critical Rule:** Accessories are SC_L4 and must NOT be multiplied per duty/pole/frame/voltage

**Why:**
- Accessories are compatible add-ons
- They are not duty-specific
- They are not construction-specific
- They are reusable across many L1/L2 selections

---

## 3. Canonical Mapping by Item/ProductType

### 3.1 Contactor (LC1E / LC1D / Deca Series)

#### A) LC1E – Easy TeSys Power Contactors (Pages 8–9)

| Layer | What Goes Here | Examples from Catalog |
|-------|----------------|---------------------|
| **Item/ProductType** | Contactor | — |
| **SubCategory** | Power Contactor | — |
| **SC_L1** | Frame + Poles | Frame-1, 3P / 4P |
| **SC_L2** | Coil type | AC Coil / DC Coil |
| **SC_L3** | Duty Class | AC1, AC3 |
| **SC_L4** | Add-ons | 1NO/1NC, 2NO/2NC, Surge suppressor |

**Attributes (KVU) – attached to BASE L1:**
- `AC_CURRENT` = 6, 9, 12, 18 A
- `MOTOR_HP` = 3, 5.5, 7.5
- `MOTOR_KW` = 2.2, 4, 7.5
- `COIL_VOLTAGE` = 220V AC, 415V AC
- `VOLTAGE_TYPE` = AC

**L2 Generation Rule (Page 8 example - CORRECTED):**

For LC1E0601:
- **Only create L2 rows for SKUs actually present in price list**
- If price list shows LC1E0601M7 (220V) and LC1E0601F7 (415V) as separate SKUs → 2 L2 rows
- If AC1/AC3 appear as separate priced rows with different prices → separate L2 rows
- If AC1/AC3 are same SKU, same price → single L2 row with duty as SC_L3 + attributes

**Result:** L2 row count = count of distinct SKUs in price list, NOT theoretical combinations.

---

#### B) LC1D – TeSys Deca Power Contactors (Pages 12–13)

| Layer | Meaning | Examples |
|-------|---------|----------|
| **SC_L1** | Construction | 3P / 4P |
| **SC_L2** | Operation | AC Coil / DC Coil |
| **SC_L3** | Duty | AC3 / Capacitor duty |
| **SC_L4** | Accessories | Thermal overload, Aux contacts |

**Attributes:**
- `AC3_CURRENT` (Numeric)
- `MOTOR_KW` / `HP` (Numeric)
- `COIL_VOLTAGE` (24V DC / 110V / 220V)
- `OVERLOAD_RANGE` (0.25–0.4 etc.)

**Note:** Thermal overload = SC_L4 + attribute (range). Not a new item, not attribute-only.

---

#### C) Capacitor Duty Contactors (Pages 20–21)

| Layer | Meaning |
|-------|---------|
| **Item/ProductType** | Contactor |
| **SubCategory** | Capacitor Duty (distinct from standard motor duty) |
| **SC_L4** | Built-in NO/NC configurations |

**🔒 Critical Rule:** Even if price equals standard LC1D, DO NOT merge. Separate L2 rows mandatory.

---

### 3.2 Control Relay (LP1K - TeSys K, Pages 18–19)

| Layer | Meaning |
|-------|---------|
| **Item/ProductType** | Control Relay |
| **SubCategory** | Control Relay |
| **SC_L1** | Construction (Poles if applicable) |
| **SC_L2** | Operation (AC / DC) |
| **SC_L3** | Duty (AC3 where applicable) |
| **SC_L4** | Aux contacts |

**Attributes:**
- Coil voltage
- Contact configuration count

**Rule:** Each voltage variant → separate L2 SKU

---

### 3.3 MPCB – Motor Protection Circuit Breaker (Pages 13, 46)

| Layer | Meaning |
|-------|---------|
| **Item/ProductType** | MPCB |
| **SubCategory** | Circuit Breaker – Motor Protection |
| **SC_L1** | Construction (Pole count) |
| **SC_L2** | Operation (Manual / Rotary / Push) |
| **SC_L3** | Protection Class (Thermal / Magnetic) |
| **SC_L4** | Accessories (Handle, interlock, aux) |

**Attributes:**
- `VOLTAGE_CLASS` = 500V / 690V
- `BREAKING_CAPACITY` = 50kA / 85kA / 110kA
- `OVERLOAD_SETTING` = 0.1 / 0.16

**L2 Generation Rule (CORRECTED):** Only create L2 rows for SKUs actually present in price list

**Example (CORRECTED):** If price list shows 12 distinct MPCB SKUs (different voltage/kA combinations), then 12 L2 rows. NOT: 2 × 3 × 2 = 12 (that's analysis, not generation).

---

### 3.4 Overload Relay (Pages 12, 41–45)

| Layer | Meaning |
|-------|---------|
| **Item/ProductType** | Overload Relay |
| **SubCategory** | Thermal OLR / Electronic OLR |
| **SC_L1** | Adjustable / Fixed |
| **SC_L2** | Operation (Manual / Auto reset) |
| **SC_L3** | Class (10A, 20A, etc.) |
| **SC_L4** | Accessories (Display, communication) |

**Attributes:**
- Current Range (A)
- Reset type
- Ground fault
- Communication protocol

**Rule:** Each configuration = separate L2 SKU

---

### 3.5 Circuit Breaker (Pages 46–49)

| Layer | Meaning |
|-------|---------|
| **Item/ProductType** | Circuit Breaker |
| **SubCategory** | Circuit Breaker |
| **SC_L1** | Construction (Pole count) |
| **SC_L2** | Operation (Rotary / Toggle / Pushbutton) |
| **SC_L3** | Protection Class |
| **SC_L4** | Accessories (Handles, interlocks) |

**Attributes:**
- Voltage
- Breaking Capacity (kA)

---

### 3.6 Switch / Isolator (Page 50+)

| Layer | Meaning |
|-------|---------|
| **Item/ProductType** | Switch / Isolator |
| **SubCategory** | Switch / Isolator |
| **SC_L1** | Construction (Pole count) |
| **SC_L2** | Operation (Manual / Motorized) |
| **SC_L3** | Duty Class |
| **SC_L4** | Accessories |

**Attributes:**
- Voltage
- Current

---

## 4. L2 Generation Rules (Final - Locked - CRITICAL CORRECTION)

### 4.1 The Correct L2 Generation Approach

**🔒 Fundamental Rule (Do Not Violate):**

L2 rows are created ONLY when the price list gives a distinct commercial SKU/price line.

**What We DO:**
1. Extract only priced SKUs from the price list (e.g., LC1D*, LC1DT*, LP1D*)
2. Create one L2 row per distinct OEM catalog number found in the price list
3. Attach classification fields:
   - SC_L1: frame/poles (if present, derived)
   - SC_L3: AC1/AC3/capacitor duty (if present, as SC_L3 Feature Class unless SKU changes)
   - Voltage as attributes (if present)
   - SC_L4 accessories (if mentioned)

**What We DO NOT Do:**
- ❌ Do NOT generate the cross-product of frame × poles × duty × voltage
- ❌ Do NOT create "missing voltage variants" that aren't priced/listed
- ❌ Do NOT multiply accessories

### 4.2 What CAUSES Multiple L2 Rows (When OEM Differentiates)

| Dimension | Layer | Causes L2 Multiplication? | Condition |
|-----------|-------|---------------------------|-----------|
| Frame | SC_L1 | ❌ NO | Frame is derived, never multiplies |
| Pole | SC_L1 | ✅ YES | Only if OEM provides distinct SKU/price per pole |
| Coil voltage | Attribute | ✅ YES | Only if SKU suffix changes (M7/F7/N7/BD/FD/MD etc.) |
| Duty (AC1 / AC3) | SC_L3 | ✅ YES | Only if SKU changes |
| Breaking capacity | Attribute | ✅ YES | Only if SKU changes |
| Voltage class (500V / 690V) | Attribute | ✅ YES | Only if SKU changes |

**The Correct Formula (Truth-Based):**
```
L2_row_count = count(distinct (Make, OEM_Catalog_No)) in price list
```

**NOT:**
```
❌ L2 rows = Frame × Pole × Duty × Voltage × Breaking Capacity
```

**This is an analysis lens, not an L2 row generator.**

---

### 4.2 What DOES NOT Multiply

| Item | Layer | Multiply? | Reason |
|------|-------|-----------|--------|
| Aux contacts | SC_L4 | ❌ No | Compatible add-on, reusable |
| Surge suppressor | SC_L4 | ❌ No | Compatible add-on, reusable |
| Mechanical interlock | SC_L4 | ❌ No | Compatible add-on, reusable |
| Power connector | SC_L4 | ❌ No | Compatible add-on, reusable |
| OLR (when sold separately) | Feature L1 + L2 | ❌ No | Separate SKU, not multiplied |
| Spare coil (no price) | L1 only | ❌ No | No price = L1 only |

**🔒 Locked Rule:** Accessories are single SC_L4 SKUs. They are NOT multiplied per duty/pole/frame/voltage.

---

## 5. Page-wise Interpretation (Page 8 to End)

### Page 8 — Easy TeSys Contactors (AC Control)

- **Item/ProductType:** Contactor
- **SubCategory:** Power Contactor
- **SC_L1:** Frame (e.g., Frame 1)
- **SC_L1:** Poles (3P / 4P)
- **SC_L3:** Duty (AC1, AC3)
- **SC_L4:** Aux contacts (e.g., 1NO/1NC)
- **Attributes:** Rated Current (A), HP, kW, Coil Voltage (AC 220V, AC 415V)
- **Rule:** Each reference generates L2 rows **only for SKUs actually present in price list**. AC1/AC3 are SC_L3 (Feature Class) unless SKU changes.

**Important:** OEM table rows may show AC1/AC3 ratings separately for the same SKU; this is engineering disclosure, not commercial SKU separation.

---

### Page 9 — DC Control & 4-Pole Variants

- DC coil variants: Voltage attribute = 24V DC (no AC voltage multiplication)
- 4‑pole tables: Poles = 4P (SC_L1)
- If voltage classes exist, create separate L2 rows **only if distinct SKU/price per voltage**

---

### Page 10 — Accessories

- Aux contact blocks, surge suppressors, mechanical interlocks
- **Treatment:** SC_L4 only. Each accessory reference = separate L2 SKU
- **Never merge accessories into base SKU**

---

### Page 11 — Technical Notes

- **Ignored for catalog import. No SKUs.**

---

### Page 12 — Thermal Overload Relays

- **Item/ProductType:** Overload Relay
- **SubCategory:** Thermal OLR
- **SC_L1:** Adjustable / Fixed
- **Attributes:** Current Range (A)
- Accessories remain SC_L4

---

### Pages 13–16 — MPCB

- **Item/ProductType:** MPCB (Motor Protection Circuit Breaker)
- **Attributes:** Voltage Class (500V/690V), Breaking Capacity (kA)
- **SC_L4:** Accessories
- **L2 Generation rule:** Only create L2 rows for SKUs actually present in price list. Voltage × kA is analysis, not generation.

---

### Pages 17 — Series Knowledge

- **Reference only.** Used to understand K / Deca / Giga / Ultra / Island positioning

---

### Pages 18–19 — TeSys K Control Relays

- **Item/ProductType:** Control Relay
- **Attributes:** Coil Type (AC/DC), Coil Voltage
- **SC_L4:** Contact configuration (e.g., 2NO+2NC)
- **Rule:** Same base reference × voltage variants = multiple L2 rows **only if SKU suffix changes or price differs**

---

### Pages 20–21 — Capacitor Duty Contactors

- **Item/ProductType:** Contactor
- **SubCategory:** Capacitor Duty (distinct from standard motor duty)
- **SC_L4:** Built-in NO/NC configurations
- **Important:** Even if price equals standard LC1D, DO NOT merge. Separate L2 rows mandatory

---

### Pages 22–27 — Deca Series (Repetition)

- AC1/AC3 duty × Poles × Voltage × Accessories
- **CORRECTED:** L2 rows = count of distinct SKUs in price list. No combinatorial multiplication.

---

### Pages 28–35 — Power Connection & Kits

- Terminal blocks, busbars, reversing kits, star-delta kits, timers
- **Treatment:** SC_L4 accessories. Separate L2 SKUs only

---

### Pages 36–40 — Higher Rating Contactors

- Same as Page 8/22. AC1/AC3, poles, voltage, accessories

---

### Pages 41–45 — Thermal & Electronic OLR

- **Item/ProductType:** Overload Relay
- **Attributes:** Range, reset, class, display, ground fault, communication
- Each configuration = separate L2 SKU

---

### Pages 46–49 — Circuit Breakers

- **Item/ProductType:** Circuit Breaker
- **Attributes:** Voltage, kA
- **SC_L1/2:** Operation (rotary/toggle/pushbutton)
- **SC_L4:** Handles/interlocks

---

### Page 50+ — Switches / Isolators

- **Item/ProductType:** Switch / Isolator
- **Attributes:** Voltage, current
- **SC_L1:** Poles
- **SC_L4:** Accessories

---

## 6. Final Decision Rules (Frozen)

### 🔒 Rule 1: Pole Count → SC_L1

Pole count belongs to SC_L1 (Construction). It defines physical construction, not rating.

---

### 🔒 Rule 2: AC1 / AC3 / Capacitor Duty → SC_L3

AC1 / AC3 / Capacitor duty are SC_L3 (Feature Class), NOT SubCategory, NOT Attribute.

**Why:**
- They describe duty/application behavior
- They change rating values (A, kW, HP)
- They do not change physical construction

---

### 🔒 Rule 3: Voltage → Attribute (Never SC)

Voltage is always an Attribute (KVU), never a SubCategory, never SC_L1–SC_L4.

---

### 🔒 Rule 4: Accessories → SC_L4 (+ Attributes if Needed)

Aux / OLR / Suppressor → SC_L4 (+ attributes if needed)

**Critical:** Accessories are NOT multiplied per duty/pole/frame/voltage. They are single SKUs, reusable across selections.

---

### 🔒 Rule 5: L2 Generation Formula (CORRECTED)

**L2 rows are NEVER created by combinatorial multiplication.**

**The ONLY valid formula:**
```
L2_row_count = count(distinct (Make, OEM_Catalog_No)) in price list
```

**What this means:**
- ✅ L2 rows = number of explicitly priced variants shown in OEM price list
- ✅ Each distinct commercial SKU = one L2 row
- ❌ Frame × Pole × Duty × Voltage is NOT an L2 generator (it's analysis only)

**Example (LC1D - Correct Approach):**
1. Extract all SKUs actually present in catalog for LC1D scope (LC1D / LC1DT / LP1D where applicable)
2. Count distinct OEM catalog numbers
3. That count = L2 row count

**NOT:**
- ❌ 6 frames × 2 poles × 2 duty × 4 voltages = 96 L2 rows (WRONG)

**If you want a secondary "expected combinations" check, that's a QA/coverage report, not L2 creation.**

---

### 🔒 Rule 6: Frame and Pole Coexistence

Frame and Pole are BOTH SC_L1 and can coexist:
- `SC_L1 = { FRAME_1, POLE_3 }`
- `SC_L1 = { FRAME_1, POLE_4 }`

They are not alternatives, not mutually exclusive.

---

### 🔒 Rule 7: Catalog Imports are L2-Only

- No L1 creation from price list
- No Category/SubCategory creation
- Only SKU truth

---

### 🔒 Rule 8: AC1 / AC3 Rule (CORRECTED)

- Duty class (AC1/AC3) is SC_L3 (Feature Class); duty-specific ratings are KVU attributes. Duty does not create additional L2 rows unless SKU changes
- Catalog table rows may show multiple duty ratings for the same SKU; these do NOT create multiple L2 rows
- Only if SKU changes → separate L2 rows
- Uniform treatment across ALL pages

---

### 🔒 Rule 9: SKU Suffix Rule

- Final SKU must match OEM completion rule
- Never infer suffix unless catalog explicitly defines it

---

### 🔒 Rule 10: Accessories Never Multiply

- Always SC_L4
- Never Item/ProductType
- Never Attribute
- Single SKU per accessory type
- Reusable across selections

---

## 7. Doctrine Alignment Verification

### ✅ Section A (Executive Rules): Fully Aligned

- Category ≠ Item/ProductType ✓
- SubCategories additive ✓
- L0→L1→L2 inheritance ✓
- L1 does NOT own price ✓
- Features are separate L1 lines ✓

---

### ✅ Section E (SubCategory Model): Fully Aligned

- Multi-SubCategory support ✓
- SC_L1–SC_L4 are additive ✓

---

### ✅ Section V (L1 Feature Lines Standard): Fully Aligned

- BASE + FEATURE lines ✓
- L1_Group_Id grouping ✓

---

### ✅ Section T.6 (Vendor Variability): Fully Aligned

- MAKE_SERIES_FEATURE_POLICY matches T.6 ✓
- Handling types match ✓

---

### ✅ Section AA.1 (Excel Layout): Fully Aligned

- All structures match Fundamentals v2.0 ✓

---

## 8. Page-to-L2 Extraction Checklist (Engineer Sign-off)

| Page | Item/ProductType | SKU Base Detected | Expansion Applied (Voltage/Duty/Poles) | Accessories (SC_L4) Added | Verified (✔/✖) |
|------|----------------|-------------------|----------------------------------------|---------------------------|-----------------|
| 8 | Contactor (LC1E) | Yes | Distinct SKUs only (AC1/AC3 as attributes unless SKU changes) | Yes | |
| 9 | Contactor | Yes | Distinct SKUs only (DC/4P if SKU differs) | Yes | |
| 10 | Accessories | Yes | N/A | Yes | |
| 12 | Overload Relay | Yes | Distinct SKUs only | Yes | |
| 13–16 | MPCB | Yes | Distinct SKUs only (voltage/kA if SKU differs) | Yes | |
| 18–19 | Control Relay | Yes | Distinct SKUs only (voltage if SKU differs) | Yes | |
| 20–21 | Capacitor Duty Contactor | Yes | Distinct SKUs only | Yes | |
| 22–27 | Contactor (Deca) | Yes | Distinct SKUs only (no multiplication) | Yes | |
| 28–35 | Accessories | Yes | N/A | Yes | |
| 41–45 | OLR | Yes | Distinct SKUs only | Yes | |
| 46–49 | Circuit Breaker | Yes | Distinct SKUs only (voltage/kA if SKU differs) | Yes | |
| 50+ | Switch/Isolator | Yes | Distinct SKUs only (voltage/poles if SKU differs) | Yes | |

---

## 9. Engineer Validation Checklist

### 9.1 Identity & Scope Check (Must Pass)

| Check | Yes / No |
|-------|----------|
| Make identified (e.g., Schneider) | |
| Series identified (e.g., Easy TeSys / TeSys Deca / TeSys K) | |
| Item/ProductType correct (Contactor / Control Relay / MPCB / Switch) | |
| No accessory treated as Item/ProductType | |
| Spare coils without price kept at L1 only | |

**❌ If any fails → STOP**

---

### 9.2 SubCategory & SC_L Mapping (Locked)

**Business SubCategory (one only):**
- Examples: Power Contactor, Capacitor Duty Contactor, Control Relay, MPCB

**Supporting SubCategories (SC_L1 → SC_L4):**

| Layer | Meaning | Examples |
|-------|---------|----------|
| SC_L1 (Construction) | Physical build | Frame size, 3P / 4P |
| SC_L2 (Operation) | Actuation | Manual / Electrical / Magnetic |
| SC_L3 (Feature Class) | Duty / Function | AC1 / AC3 / Capacitor Duty |
| SC_L4 (Accessory Class) | Add-ons | Aux contacts, surge suppressor |

**⚠️ AC1 / AC3 MUST be SC_L3 (not SubCategory, not Attribute)**  
**⚠️ Accessories MUST be SC_L4 and never multiplied**

---

### 9.3 Attribute Validation (KVU Model)

For each L2 row, confirm:

| Attribute | Required |
|-----------|----------|
| Rated Current (A) | ✅ |
| Poles (3P / 4P) | ✅ |
| Duty Rating (AC1 / AC3) | ✅ |
| kW | ✅ |
| HP | ✅ |
| Coil Voltage (AC/DC + value) | ✅ |
| Frequency (AC only) | ✅ |
| Breaking Capacity (if MPCB) | Conditional |

**❌ Mixed tokens like "25A" or "7.5kW" in one cell → INVALID**

---

### 9.4 L2 SKU Rules (Hard)

| Rule | Status |
|------|--------|
| SKU = OEM reference number | Mandatory |
| SKU changes when coil voltage suffix changes | Mandatory |
| SKU changes when breaking capacity changes | Mandatory |
| Price attached ONLY at L2 | Mandatory |
| L1 must not store price | Mandatory |

---

### 9.5 L2 Generation Rules (Engineer Sanity Check - CORRECTED)

**🔒 CRITICAL:** L2 rows are NEVER created by combinatorial multiplication.

**L2 rows are created ONLY when:**
- ✅ Distinct SKU exists in price list (OEM catalog number changes)
- ✅ SKU suffix changes (e.g., M7/F7/N7 for voltage)
- ✅ SKU suffix changes (e.g., M7/F7/N7 for voltage)

**What CAUSES multiple L2 rows (when OEM differentiates):**
- ✅ Poles → only if distinct SKU/price per pole
- ✅ Coil Voltage → only if SKU suffix changes
- ✅ AC1 vs AC3 → only if SKU changes
- ✅ Breaking Capacity → only if SKU changes
- ✅ Voltage Class → only if SKU changes

**What DOES NOT multiply:**
- ❌ Frame (derived, never multiplies)
- ❌ Aux contacts (SC_L4, never multiply)
- ❌ Mechanical interlock (SC_L4, never multiply)
- ❌ Surge suppressor (SC_L4, never multiply)
- ❌ Power connector (SC_L4, never multiply)

**The ONLY valid formula:**
```
L2_row_count = count(distinct (Make, OEM_Catalog_No)) in price list
```

---

### 9.6 L0 / L1 Derivation Safety Check

| Question | Expected |
|----------|----------|
| Can Make be removed and row still be meaningful? | YES → becomes L1 |
| Are mandatory L1 attributes present? | YES |
| Are SubCategories additive and non-numeric? | YES |
| Can accessories be selected later without duplication? | YES |

**If YES to all → Catalog is NSW-ready.**

---

### 9.7 Engineer Sign-off

- [ ] No SKU missing from price list
- [ ] No SKU duplicated incorrectly
- [ ] No accessory exploded incorrectly
- [ ] AC1 / AC3 handled consistently
- [ ] Ready for Phase-5 L2 import

**Engineer Name:** ________  
**Date:** ________

---

## 10. Unified Rule for ALL Schneider Pages (8 → End)

### 🔑 Single Governing Rule (CORRECTED)

**L2 rows = count of distinct (Make, OEM_Catalog_No) in price list**

**If the OEM reference changes → new L2 SKU**  
**If only rating changes (same SKU) → attributes only, NOT new L2 row**  
**If only accessory applicability exists → single accessory SKU (SC_L4)**

---

### Page Patterns Mapped Cleanly

| Page Type | NSW Interpretation |
|-----------|-------------------|
| AC1 / AC3 tables | SC_L3 (Feature Class) + attributes (unless SKU changes) |
| Voltage columns | Attribute → separate L2 only if SKU changes |
| 3P / 4P tables | SC_L1 → separate L2 only if SKU changes |
| Frame variants | SC_L1 (derived, never multiplies) |
| Capacitor duty | SubCategory (business) |
| MPCB breaking capacity | Attribute → separate L2 only if SKU changes |
| Control relay voltage | Attribute → separate L2 only if SKU changes |
| Accessories pages | SC_L4 single SKUs (never multiply) |

---

## 11. Why This Does NOT Break Fundamentals

This approach:
- ✅ Keeps Category ≠ Item
- ✅ Keeps SubCategory additive
- ✅ Keeps SC_L1–SC_L4 meaningful
- ✅ Keeps L1 price-free
- ✅ Keeps L2 SKU-only pricing
- ✅ Prevents catalog explosion
- ✅ Makes UI selection sane
- ✅ Makes vendor variability manageable

**Most importantly:** It preserves engineering intent and commercial truth separately.

---

## 12. The Correct, Unbroken Chain

```
OEM Price List (Page-wise)
        ↓
Extract Distinct SKUs Only
(Make + OEM_Catalog_No)
        ↓
L2 Rows (One row per distinct SKU)
        ↓
Classify with SC_L1-4 + Attributes
(Frame derived, Duty as SC_L3 unless SKU changes)
        ↓
Auto-derivation rules
        ↓
L1 abstraction (engineer-selected)
        ↓
L0 intent template
```

**Nothing skips layers.**  
**Nothing reverses ownership.**  
**Nothing violates inheritance.**

---

## 13. Gap Check — Are We Missing Anything?

### Covered ✅
- Poles
- AC1 / AC3
- Voltage variants
- Capacitor duty
- Thermal overload
- Aux contacts
- Breaking capacity
- MPCB operation variants

### Explicitly Deferred (Correctly) ⏳
- Spare coils (no price → L1 only)
- Mounting hardware
- Minor mechanical kits

### Forbidden ❌
- Turning accessories into Items
- Storing numeric values in SC layers
- Treating Series as SubCategory

**No doctrine gaps found.**

---

## 14. Next Steps

1. **Review this document** (current step)
2. **Engineering sign-off** required
3. **Apply to LC1D FINAL** L2 generation
4. **Reuse blindly for:**
   - ABB
   - Siemens
   - L&T

---

## 15. Document Transfer Path

**Current Location:** `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/`  
**After Review & Confirmation:** Transfer to:
- `docs/PHASE_5/ENGINEERING_REVIEW/` (if engineering review document)
- OR `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/` (if catalog interpretation guide)

**Decision:** To be determined after review

---

## 16. References

- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Table Structure Review:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/v1.3_TABLE_STRUCTURE_REVIEW.md`
- **Schneider Catalog Master:** `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER_CATALOG_MASTER.md`

---

**Document Status:** ✅ **READY FOR REVIEW** (v1.1 - Critical corrections applied)

**Critical Updates in v1.1:**
- ✅ L2 generation rule corrected: No combinatorial multiplication
- ✅ Frame handling corrected: Derived, not multiplier
- ✅ Duty handling corrected: Attribute unless SKU/price changes
- ✅ All multiplication rules corrected to reflect truth-based approach

**Next Action:** Engineering team review and sign-off required before LC1K processing begins.

