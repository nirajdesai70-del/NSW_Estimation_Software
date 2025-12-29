# Schneider Catalog - Final Rules v1.2
## Extracted and Locked Rules for Implementation

**Status:** LOCKED  
**Date:** 2025-01-XX  
**Purpose:** Single-page reference of final, locked rules for Schneider catalog interpretation  
**Source:** Compiled from `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md` and `SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`

**v1.2:** SC_L alignment + duty clarification corrected; no semantic conflicts.

---

## Document Control

- **Version:** 1.2
- **Classification:** Engineering Rules - Implementation Reference
- **Lock Status:** LOCKED
- **Usage:** Reference document for all Schneider catalog work

---

## 🔒 RULE 1: L2 Generation - The Fundamental Truth

**L2 rows are NEVER created by combinatorial multiplication.**

**L2 rows = the number of explicitly priced variants shown in the OEM price list (i.e., distinct commercial SKUs).**

**The ONLY valid L2 count formula:**
```
L2_row_count = count(distinct (Make, OEM_Catalog_No)) in price list
```

**What this means:**
- ✅ L2 rows come ONLY from catalog SKUs / priced lines
- ❌ No artificial multiplication
- ❌ No inferred combinations beyond what OEM priced
- ❌ Frame × Poles × Duty × Voltage is NOT an L2 generator (it's an analysis lens only)

---

## 🔒 RULE 2: L2 Row Key (Commercial Truth)

**L2 row is uniquely identified by:**
- `Make + OEM_Catalog_No` (completed SKU)
- `PriceListRef + EffectiveFrom` (for versioning)

**L2 rows are created ONLY when:**
- ✅ OEM Catalog No changes (including suffix completion) → multiple L2 rows
- ✅ Same base reference but OEM catalog number changes via suffix → multiple L2 rows
- ❌ If OEM does not list a combination → we do NOT invent it

**Note:** Price variation is handled via price history records for the same SKU, not by duplicating SKUs.

---

## 🔒 RULE 3: Table Rows ≠ SKU Rows ≠ L2 Rows

**Multiple rows in OEM price list do NOT create multiple L2 rows unless the catalog number itself changes.**

**AC1 / AC3 rows are engineering disclosure, not commerce.**

**Example:**
- OEM table shows: AC1 → 20A, AC3 → 6A (same SKU)
- NSW creates: ONE L2 SKU with TWO L1 lines (different SC_L3 + attributes)

**Important:** OEM table rows may show AC1/AC3 ratings separately for the same SKU; this is engineering disclosure, not commercial SKU separation.

---

## 🔒 RULE 4: Duty (AC1 / AC3) Handling

**Duty class (AC1/AC3) is SC_L3 (Feature Class). Duty-specific rating values (current A, kW, HP) are stored as KVU attributes on the L1 line. Duty does not create additional L2 rows unless OEM SKU changes.**

| Condition | NSW Treatment |
|-----------|---------------|
| Same SKU, same price | Single L2 row |
| AC1/AC3 give different currents | SC_L3 label + Attribute values differ |
| Different SKU for duty | Separate L2 rows |
| Different price for duty | Price history record (same SKU) |

**Therefore:**
- ✅ AC1 / AC3 only causes L2 multiplication if SKU changes
- ✅ AC1 / AC3 = SC_L3 (Feature Class) at L1
- ✅ Duty-specific ratings (current, kW, HP) = KVU attributes at L1
- ❌ They do NOT create extra L2 rows

**Correct Modeling:**
- **L2 (SKU layer):** One row per SKU from price list, price stored once
- **L1 (spec layer):** Multiple L1 lines referencing same L2 SKU:
  - **L1 line #1:** SC_L3=AC1, attributes: CURRENT=20A, KW=2.2, HP=3
  - **L1 line #2:** SC_L3=AC3, attributes: CURRENT=6A, KW=2.2, HP=3
  - Both reference same L2 SKU if OEM SKU doesn't change

---

## 🔒 RULE 5: Frame Handling

**Frame is NEVER a multiplier.**

**Frame is a derived construction label (physical size). It does NOT create new L2 rows by itself.**

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

**This is classification, not multiplication.**

**Causal order (locked):**
```
Pole / voltage / duty (when priced) ⇒ SKU changes ⇒ frame label follows
```

**NOT:**
```
frame ⇒ SKU changes
```

---

## 🔒 RULE 6: Pole Handling

**Pole is a multiplier ONLY when OEM differentiates.**

**Poles can generate multiple L2 rows ONLY when the catalog provides distinct priced SKUs/lines per pole variant.**

- ✅ If 3P vs 4P has different SKU/price → multiple L2 rows
- ❌ If same SKU → single L2 with attribute POLES

**Frame and Pole Coexistence:**
- Frame and Pole are BOTH SC_L1 and can coexist:
  - `SC_L1 = { FRAME_1, POLE_3 }`
  - `SC_L1 = { FRAME_1, POLE_4 }`
- But Frame is derived, Pole may cause SKU multiplication

---

## 🔒 RULE 7: Voltage Handling

**Voltage is always an Attribute (KVU), never a SubCategory, never SC_L1–SC_L4.**

**Voltage causes L2 multiplication ONLY when:**
- ✅ SKU suffix changes (e.g., M7/F7/N7/BD/FD/MD)
- ❌ Same SKU, different voltage rating → attribute only

**Note:** Price differences are handled via price history records, not SKU duplication.

---

## 🔒 RULE 8: Accessories Handling

**Accessories are SC_L4 and must NOT be multiplied per duty/pole/frame/voltage.**

**Why:**
- Accessories are compatible add-ons
- They are not duty-specific
- They are not construction-specific
- They are reusable across many L1/L2 selections

**Correct accessory modeling:**
- One accessory SKU = one L2 row
- Do NOT duplicate accessory for AC1 vs AC3
- Do NOT duplicate for voltage
- Do NOT duplicate for frame

**Accessory explosion happens only when selected, not in catalog import.**

**Examples:**
- Aux contact block → SC_L4 (Accessory Class)
- Mechanical interlock → SC_L4
- Surge suppressor → SC_L4
- Power connector → SC_L4
- Terminal block → SC_L4
- Reversing kit → SC_L4
- Star–delta kit → SC_L4

---

## 🔒 RULE 9: L1 vs L2 Differentiation

**You do NOT distinguish "two different items" at L2. You distinguish them at L1. L2 stays the same.**

**Differentiation happens ONLY at L1:**
- Each engineering interpretation becomes a separate L1 line
- Multiple L1 lines can reference the same L2 SKU
- This is intentional and correct

**Golden Sentence:**
> **"Different engineering interpretations of the same OEM product are represented as multiple L1 lines referencing a single L2 SKU."**

**Example:**
- **L2:** One SKU (LC1E0601), one price
- **L1-A:** AC1 use-case (CURRENT = 20A), references LC1E0601
- **L1-B:** AC3 use-case (CURRENT = 6A), references LC1E0601

**Result:**
- ✔ Same SKU
- ✔ Same price
- ✔ Different engineering meaning
- ✔ Fully traceable

---

## 🔒 RULE 10: Clean Mental Model

**Think in three questions only:**

1. **Did Schneider change the catalog number?**
   - If yes → new L2
   - If no → same L2

2. **Did price change?**
   - If yes → new price row (same SKU, new version)
   - If no → same L2

3. **Did behaviour/spec change?**
   - Attribute / SC_Lx / Feature line
   - Never SKU split

**That's it. No other rule needed.**

---

## 🔒 RULE 11: What CAUSES Multiple L2 Rows

**L2 rows are created ONLY when:**

| Dimension | Layer | Causes L2 Multiplication? | Condition |
|-----------|-------|---------------------------|-----------|
| Frame | SC_L1 | ❌ NO | Frame is derived, never multiplies |
| Pole | SC_L1 | ✅ YES | Only if OEM provides distinct SKU/price per pole |
| Coil voltage | Attribute | ✅ YES | Only if SKU suffix changes (M7/F7/N7/BD/FD/MD etc.) |
| Duty (AC1 / AC3) | SC_L3 | ✅ YES | Only if SKU changes |
| Breaking capacity | Attribute | ✅ YES | Only if SKU changes |
| Voltage class (500V / 690V) | Attribute | ✅ YES | Only if SKU changes |

---

## 🔒 RULE 12: What DOES NOT Multiply

| Item | Layer | Multiply? | Reason |
|------|-------|-----------|--------|
| Frame | SC_L1 | ❌ No | Derived classification |
| Aux contacts | SC_L4 | ❌ No | Compatible add-on, reusable |
| Surge suppressor | SC_L4 | ❌ No | Compatible add-on, reusable |
| Mechanical interlock | SC_L4 | ❌ No | Compatible add-on, reusable |
| Power connector | SC_L4 | ❌ No | Compatible add-on, reusable |
| OLR (when sold separately) | Feature L1 + L2 | ❌ No | Separate SKU, not multiplied |
| Spare coil (no price) | L1 only | ❌ No | No price = L1 only |

---

## 🔒 RULE 13: SC Layer Mapping

| Layer | Purpose | Nature | Examples |
|-------|---------|--------|----------|
| **SC_L1** | Construction / Form | Enumerated, non-numeric | Frame size (derived), Pole count (2P/3P/4P), Fixed/Plug-in |
| **SC_L2** | Operation / Actuation | Enumerated | AC Coil / DC Coil, Manual / Electrical, Rotary / Toggle |
| **SC_L3** | Functional Duty / Class | Enumerated | AC1 / AC3 (Feature Class), Capacitor Duty, Thermal / Magnetic |
| **SC_L4** | Accessory / Extension Class | Enumerated (may repeat) | Aux contacts, Thermal overload, Surge suppressor, Mechanical interlock |

**Hard Rules:**
- SC layers are not numeric
- SC layers are not priced
- SC layers do not carry values
- Values always go to Attributes (KVU)

---

## 🔒 RULE 14: Catalog Imports are L2-Only

- No L1 creation from price list
- No Category/SubCategory creation
- Only SKU truth

**Frame/Poles/Duty/Voltage are used ONLY to:**
- Classify the L2 row (SC_L1..SC_L4 + Attributes)
- Group L2 rows into an L1 template later
- Derive missing L1 fields for engineer completion

**They do NOT generate new SKUs.**

---

## 🔒 RULE 15: SKU Suffix Rule

- Final SKU must match OEM completion rule
- Never infer suffix unless catalog explicitly defines it

---

## 🔒 RULE 16: Unified Rule for ALL Schneider Pages

**Single Governing Rule:**
> **L2 rows = count of distinct (Make, OEM_Catalog_No) in price list**

**If the OEM reference changes → new L2 SKU**  
**If only rating changes (same SKU) → attributes only, NOT new L2 row**  
**If only accessory applicability exists → single accessory SKU (SC_L4)**

---

## Summary: The Correct, Unbroken Chain

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

## Final Freeze Statement

**LOCKED:**
> "L2 rows are created only per distinct OEM Catalog No (Make + OEM_Catalog_No). AC1/AC3 duty creates separate L1 lines, not separate L2 rows. Frame is derived and never multiplies. Accessories are SC_L4 and never multiply base SKUs."

**AND:**
> "Same OEM catalog number → one L2 SKU.  
> Different duty / rating / use-case → separate L1 lines.  
> L1 → L2 is many-to-one."

---

**Document Status:** ✅ **LOCKED - FINAL RULES**

**Usage:** Reference this document for all Schneider catalog interpretation work.

**Next Action:** Apply these rules to LC1D FINAL, then proceed to LC1K.

