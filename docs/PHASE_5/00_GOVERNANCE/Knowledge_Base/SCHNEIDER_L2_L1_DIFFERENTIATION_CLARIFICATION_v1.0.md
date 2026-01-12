# Schneider L2/L1 Differentiation Clarification v1.0
## Final Alignment - L2 vs L1 Separation

**Status:** LOCKED  
**Date:** 2025-01-XX  
**Purpose:** Final clarification on L2 vs L1 differentiation, resolving confusion around AC1/AC3, duty, and ratings  
**Related:** `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md`

---

## Document Control

- **Version:** 1.0
- **Classification:** Engineering Decision - Final Clarification
- **Lock Status:** LOCKED
- **Supersedes:** Any earlier confusion about L2 multiplication for duty/ratings

---

## 1. The Core Question

**Question:** "Do we distinguish two different items at L2 when same OEM catalog number has different AC1/AC3 ratings?"

**Answer:** NO. You do NOT distinguish "two different items" at L2. You distinguish them at L1. L2 stays the same.

---

## 2. What Your ORIGINAL Rule Has Always Been (And Still Is)

From NSW fundamentals:

**L2 rows are created ONLY when the OEM catalog number changes.**
**Attributes explain behaviour; SKU defines commerce.**

That means:
- ✅ Duty (AC1 / AC3) → attribute
- ✅ Frame size → attribute
- ✅ Rated current difference → attribute
- ✅ HP / kW difference → attribute
- ✅ Pole count → attribute
- ✅ Accessory presence → SC_L4
- ✅ Voltage → attribute
- ✅ Same catalog number = SAME L2, even if table shows multiple rows

**Nothing in your doctrine ever said "AC1 and AC3 create two L2 SKUs".**

---

## 3. Where the Contradiction Crept In

The confusion came from mixing two different observations:

### A. OEM TABLE STRUCTURE (what Schneider prints)

Schneider prints multiple rows for the same reference because:
- AC1 and AC3 ratings are different
- Current limits change
- They want engineers to read limits correctly

**⚠️ But table rows ≠ SKU rows**

### B. TEMPORARY DEBUGGING WORK

While debugging LP1K and LC1D, we temporarily:
- Counted table rows
- Counted duty rows
- Counted voltage rows

This was diagnostic, not semantic.

**❌ That temporary counting looked like SKU multiplication, but it was never meant to become NSW truth.**

---

## 4. The CORRECT Frozen Rule

### 🔒 Rule 1 — L2 is SKU, not behaviour

**Each distinct OEM catalog number = exactly one L2 row.**

**No exceptions.**

---

### 🔒 Rule 2 — Table rows do NOT imply SKU rows

**Multiple rows in OEM price list do NOT create multiple L2 rows unless the catalog number itself changes.**

AC1 / AC3 rows are engineering disclosure, not commerce.

---

### 🔒 Rule 3 — Duty is ALWAYS attribute

**If same catalog number shows:**
- AC1 → 20A
- AC3 → 6A

**Then:**

**L2 SKU:**
```
SKU: LC1E0601
Make: Schneider
Price: ₹XXXX
```

**L1 Attributes (multiple L1 lines, same L2):**

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

**Result:**
- ✔ One SKU
- ✔ One price
- ✔ Two duty attributes
- ✔ No multiplication

---

### 🔒 Rule 4 — Frame is NEVER a multiplier

**Frame is physical size.**
**Frame may change with poles/current.**
**But frame itself does NOT create new L2.**

**Only SKU change does.**

---

### 🔒 Rule 5 — When multiplication DOES happen

**Only when OEM reference changes:**

| Situation | Result |
|-----------|--------|
| LC1E0601 → LC1E0601M | ✅ New L2 |
| LC1E0601 → LC1E0601N5 | ✅ New L2 |
| Same reference, different AC1/AC3 | ❌ No new L2 |
| Same reference, different current rating | ❌ No new L2 |

---

## 5. Where Differentiation Happens in NSW (Layer by Layer)

### L2 — Commercial Identity (Unchanged)

**One SKU. One price. One OEM catalog number.**

**Example:**
```
L2:
  SKU: LC1E0601
  Make: Schneider
  Price: ₹XXXX
```

**No duplication. No ambiguity.**

---

### L1 — Engineering Intent (This is where the split happens)

**You create two L1 rows, not two L2 rows.**

**Both L1 rows point to the same L2 SKU.**

**Example — LC1E0601:**

**L1-A (AC1 use-case):**
- Category: Motor Control
- Item/ProductType: Contactor
- SubCategories: SC_L2 Operation: 3 Pole, SC_L3 Feature Class: AC1
- Attributes: AC1_CURRENT = 20 A, HP = 3, kW = 2.2
- Parent L2 SKU: LC1E0601

**L1-B (AC3 use-case):**
- Category: Motor Control
- Item/ProductType: Contactor
- SubCategories: SC_L2 Operation: 3 Pole, SC_L3 Feature Class: AC3
- Attributes: AC3_CURRENT = 6 A, HP = 3, kW = 2.2
- Parent L2 SKU: LC1E0601

**Result:**
- ✔ Same SKU
- ✔ Same price
- ✔ Different engineering meaning
- ✔ Fully traceable

---

## 6. Why This is NOT a Contradiction

**You are NOT creating two "items" in the commercial sense.**

**You are creating:**
- Two L1 intent lines
- Referencing one L2 SKU

**This is exactly what your doctrine says:**

> "L1 represents engineering intent and specification.  
> L2 represents commercial realization."

---

## 7. Clean Mental Model (Use This Going Forward)

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

## 8. One Golden Sentence

> **"Different engineering interpretations of the same OEM product are represented as multiple L1 lines referencing a single L2 SKU."**

**That sentence alone resolves the confusion permanently.**

---

## 9. What is Now LOCKED (No Ambiguity)

### 1) L2 is NOT multiplied for AC1 / AC3 / ratings

- One OEM catalog number = one L2 SKU
- Price belongs only to L2
- Duty, rating, usage differences do NOT create new L2s

### 2) Differentiation happens ONLY at L1

- Each engineering interpretation becomes a separate L1 line
- Multiple L1 lines can reference the same L2 SKU
- This is intentional and correct

### 3) Frame is NOT a multiplier

- Frame = physical construction characteristic
- It may change because of poles/current, but it is NOT independently multiplied
- Multipliers are only:
  - Poles (if SKU changes)
  - Coil voltage (if SKU suffix changes)
  - OEM-defined variants

### 4) AC1 / AC3 logic clarified (critical)

- AC1 and AC3 are ratings of the same device
- Often: Same SKU, Same price, Different current values
- Therefore: Two L1 lines, One L2

### 5) Accessories clarified (no explosion)

- Aux contacts, overloads, interlocks, suppressors:
  - Do NOT multiply per base SKU
  - Exist as SC-L4 feature lines
  - Resolve to L2 only if OEM policy requires ADDON SKU
  - One accessory definition → reusable across many L1s

---

## 10. What We Do NOT Discard

**Nothing is thrown away.**

**Archive policy (recommended):**
- Keep all work
- Mark earlier drafts as: ARCHIVED / SUPERSEDED
- Reason: These files capture decision evolution, useful for:
  - Audit
  - Future OEM onboarding
  - Explaining "why this model exists"

---

## 11. Final Confirmation

**Freeze:**
> "L2 rows are created only per distinct OEM catalog number.  
> All AC1/AC3, current, frame, pole, voltage differences are attributes or SC layers, not SKU multipliers."

**And:**
> "Same OEM catalog number → one L2 SKU.  
> Different duty / rating / use-case → separate L1 lines.  
> L1 → L2 is many-to-one."

**If YES, then:**
- ✅ LC1E work is correct
- ✅ LC1D correction stands
- ✅ LC1K can proceed cleanly
- ✅ No rework needed

---

## 12. References

- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Schneider Catalog Rules:** `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md`

---

**Document Status:** ✅ **LOCKED - FINAL**

**Next Action:** Apply these rules to LC1D FINAL, then proceed to LC1K.

