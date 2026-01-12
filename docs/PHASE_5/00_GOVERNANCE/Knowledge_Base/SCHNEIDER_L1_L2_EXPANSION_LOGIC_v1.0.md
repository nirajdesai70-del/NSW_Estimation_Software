# Schneider L1/L2 Expansion Logic v1.0
## Final Clarification - The "6 Lines" Question Resolved

**Status:** LOCKED  
**Date:** 2025-01-XX  
**Purpose:** Final clarification on L1 vs L2 expansion logic, resolving the "6 lines" question and completing SKU expansion rules  
**Related:** `SCHNEIDER_FINAL_RULES_v1.2.md`, `SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`

---

## Document Control

- **Version:** 1.0
- **Classification:** Engineering Decision - Final Clarification
- **Lock Status:** LOCKED
- **Supersedes:** Any confusion about L1/L2 expansion ratios

---

## 1. The "6 Lines" Question - Direct Answer

**Question:** "Can we have 6 L1 lines for one L2 SKU?"

**Answer:** YES — different voltage variants can create multiple L1 lines AND different SC_L3 duty classes (AC1/AC3) can create multiple L1 lines.

**So you can end up with 6 L1 lines BUT they may still all point to the same single L2 SKU — unless the SKU changes.**

---

## 2. The Locked Rule That Controls Everything

**L2 changes only when OEM Catalog Number changes.**  
**L1 changes whenever engineering meaning changes.**

**So:**
- ✅ Voltage change → engineering meaning changes → new L1
- ✅ Duty change (AC1 / AC3) → engineering meaning changes → new L1
- ✅ SKU stays same → L2 stays one

---

## 3. Concrete Example (LC1E0601)

**From catalog:**
- SKU: LC1E0601
- Same price
- AC1 and AC3 ratings shown
- Coil voltage variants: 220V AC, 415V AC
- No SKU suffix difference

### L2 Layer (Commercial Truth)

**L2_SKU_PRICE → ONLY ONE ROW**

| Make | OEM_Catalog_No | Price |
|------|----------------|-------|
| Schneider | LC1E0601 | ₹2875 |

✔ One SKU  
✔ One price  
✔ No multiplication

### L1 Layer (Engineering Intent)

**Variables that change meaning:**
- Duty (SC_L3): AC1, AC3 → 2 variants
- Voltage (Attribute): 220V, 415V → 2 variants

**That gives:**
- 2 (Duty) × 2 (Voltage) = **4 L1 lines**

**If there were 3 voltages, then:**
- 2 (Duty) × 3 (Voltage) = **6 L1 lines**

### Example: 4 L1 Lines (Same SKU)

**L1_LINES:**

| L1_Id | SC_L3_Set | L2_OEM_Catalog_No |
|-------|-----------|-------------------|
| L1-001 | AC1 | LC1E0601 |
| L1-002 | AC3 | LC1E0601 |
| L1-003 | AC1 | LC1E0601 |
| L1-004 | AC3 | LC1E0601 |

**L1_ATTRIBUTES_KVU:**

| L1_Id | Attribute | Value | Unit |
|-------|-----------|-------|------|
| L1-001 | VOLTAGE | 220 | V |
| L1-001 | VOLTAGE_TYPE | AC | — |
| L1-001 | CURRENT | 20 | A |
| L1-002 | VOLTAGE | 220 | V |
| L1-002 | CURRENT | 6 | A |
| L1-003 | VOLTAGE | 415 | V |
| L1-003 | CURRENT | 20 | A |
| L1-004 | VOLTAGE | 415 | V |
| L1-004 | CURRENT | 6 | A |

✔ Engineering-correct  
✔ Audit-safe  
✔ No SKU duplication

---

## 4. Important Boundary (Do NOT Cross)

### ❌ What we do NOT do
- Do not create 6 L2 rows
- Do not multiply SKUs
- Do not create fake SKU variants

### ✅ What we DO
- Create multiple L1 lines
- All reference same L2 SKU
- Let quotation logic sum price once per selected L1 group

---

## 5. When Voltage DOES Create Multiple L2 Rows

**Only when OEM catalog number changes, e.g.:**
- LC1E0601M7 → 220V
- LC1E0601N5 → 415V

**Then:**
- L2 rows = 2
- L1 lines per L2 = duty variations (AC1/AC3)

**Still no combinatorial explosion.**

---

## 6. Final Truth Table (Use This Forever)

| Change | New L1? | New L2? |
|--------|---------|---------|
| Duty AC1 → AC3 | ✅ Yes | ❌ No |
| Voltage 220 → 415 | ✅ Yes | ❌ No |
| Pole change | ✅ Yes | ❌ No (unless SKU changes) |
| Frame change | ❌ Derived | ❌ No |
| SKU suffix changes | — | ✅ Yes |
| Price changes | — | ✅ New price row |

---

## 7. One-Line Mental Model

> **"Every unique engineering meaning is an L1 line.  
> Every unique commercial reference is an L2 row."**

---

## 8. Completed SKU Expansion Logic (Critical Correction)

### 8.1 The Critical Clarification

**LC1D09* is NOT a final SKU.**  
**It is a base reference placeholder that must be completed by coil-voltage code.**

**Schneider explicitly says:** "Reference to be completed by adding coil voltage code"

### 8.2 Corrected, Frozen Rule

**L2 is created by COMPLETED OEM catalog numbers:**

```
L2 rows = count(distinct (Make, Completed OEM_Catalog_No)) present in the price list.
```

**Where:**
- LC1D09* is not a completed OEM_Catalog_No
- It must become:
  - LC1D09M7 (220V AC coil)
  - LC1D09N7 (415V AC coil)
  - LC1D09F7 (110V AC coil)
  - LC1D09BD (24V DC coil)
  - LC1D09FD (110V DC coil)
  - LC1D09MD (220V DC coil)

**So yes: those are distinct catalog numbers / SKUs at L2.**

### 8.3 Completion Logic

**When you see "* Reference to be completed by adding coil voltage code":**

**Base reference + column coil-code = completed SKU**

**AC coil code columns:**
- F7 / M7 / N7 → completed SKU suffix

**DC coil code columns:**
- BD / FD / MD → completed SKU suffix

**Low-consumption code columns:**
- BL / FL / ML (and the "EHE/KUE/BBE…" blocks) → completed SKU suffix

### 8.4 What Stays True (Still Locked)

**AC1 / AC3 still does NOT multiply L2**

In the table, AC1 and AC3 are simply showing two ratings for the same base device.

**So:**
- AC1 vs AC3 = L1 meaning
- Voltage code completion = L2 SKU identity

**Example:**

For the same completed SKU LC1D09M7:
- AC1 current and AC3 current differ
- That creates two L1 interpretations (AC1 line, AC3 line)
- Both reference the same L2 SKU LC1D09M7

**So we keep the clean separation:**
- L2 = completed SKU
- L1 = engineering interpretation (AC1/AC3)

---

## 9. Final Reconciliation

### ✅ L2 is NOT "one base reference"

**L2 is "one completed orderable catalog number".**

### ✅ L1 is NOT "one SKU"

**L1 is "one engineering intent line".**
- AC1 vs AC3 → separate L1
- Each L1 references one L2 completed SKU

---

## 10. LC1D Completed SKU Expansion Example

### A. AC COIL – STANDARD (M7 / N7 / F7)

| Base Reference | Coil Code | Voltage | Completed L2 SKU | Price (₹) |
|----------------|-----------|---------|------------------|-----------|
| LC1D09* | M7 | 220V AC | LC1D09M7 | 2135 |
| LC1D09* | N7 | 415V AC | LC1D09N7 | 2135 |
| LC1D09* | F7 | 110V AC | LC1D09F7 | 2135 |
| LC1D12* | M7 | 220V AC | LC1D12M7 | 2405 |
| LC1D12* | N7 | 415V AC | LC1D12N7 | 2405 |
| LC1D12* | F7 | 110V AC | LC1D12F7 | 2405 |

### B. DC COIL – STANDARD (BD / FD / MD)

| Base Reference | Coil Code | Voltage | Completed L2 SKU | Price (₹) |
|----------------|-----------|---------|------------------|-----------|
| LC1D09* | BD | 24V DC | LC1D09BD | 3420 |
| LC1D09* | FD | 110V DC | LC1D09FD | 3300 |
| LC1D09* | MD | 220V DC | LC1D09MD | 3420 |

### C. L1 Derivation from Completed L2

**For each completed L2 SKU (e.g., LC1D09M7):**

**Create 2 L1 lines (if both AC1 and AC3 ratings exist):**

| L1_Id | SC_L3 | Voltage | Current | L2_SKU |
|-------|-------|---------|---------|--------|
| L1-001 | AC1 | 220V | 20A | LC1D09M7 |
| L1-002 | AC3 | 220V | 6A | LC1D09M7 |

**Both reference the same L2 SKU.**

---

## 11. LC1K/LP1K Completed SKU Expansion

### Coil-code Mapping (as per Schneider tables)

**AC control columns → LC1K completed SKUs:**
- B7 = 24V
- F7 = 110V
- M7 = 220V
- N7 = 415V

**DC control columns → LP1K completed SKUs:**
- BD = 24V
- FD = 110V
- MD = 220V

### Example Expansion (LC1K0601* row)

**AC control (LC1K*):**

| Base | Coil code | Voltage | Completed SKU | Price |
|------|-----------|---------|---------------|-------|
| LC1K0601 | B7 | 24V | LC1K0601B7 | 1830 |
| LC1K0601 | F7 | 110V | LC1K0601F7 | 1830 |
| LC1K0601 | M7 | 220V | LC1K0601M7 | 1830 |
| LC1K0601 | N7 | 415V | LC1K0601N7 | 2225 |

**DC control (LP1K*):**

| Base | Coil code | Voltage | Completed SKU | Price |
|------|-----------|---------|---------------|-------|
| LP1K0601 | BD | 24V | LP1K0601BD | 2860 |
| LP1K0601 | FD | 110V | LP1K0601FD | 3455 |
| LP1K0601 | MD | 220V | LP1K0601MD | (blank → skipped if "-") |

**This exactly matches the logic:**
✅ Same base reference, different coil code → different completed SKU → separate L2.

---

## 12. Auto-L1 Derivation Rules

### 12.1 Inputs (What the System Already Has)

From completed SKU expansion map, each L2 row already contains:
- Make
- Completed_OEM_Catalog_No (e.g., LC1D09M7, LC1D09BD, LC1DT20BD, LP1D65008FD, etc.)
- Price
- CoilCode (M7/N7/F7/BD/FD/MD/BL/EL…)
- VoltageType (AC/DC)
- VoltageValue (220/415/110/24/48…)

**These L2 rows are commercial truth.**

### 12.2 Derivation Objective

Create L1 lines that capture engineering intent variations, without multiplying L2 incorrectly.

**Key locked rules applied:**
- Duty (AC1/AC3) → separate L1 lines (SC_L3), not L2
- Voltage → separate L1 lines (attribute) when needed for engineering selection
- Many L1 lines may map to the same L2 (allowed)
- But in LC1D case, voltage suffix changes create separate L2, so each L2 already corresponds to one voltage.

**So for LC1D series the main L1 split is AC1 vs AC3.**

### 12.3 L1 BASE Line Creation Rule

**For each completed L2 SKU:**

**Create one L1 BASE line per duty class present in catalog table:**
- L1(BASE, SC_L3=AC1)
- L1(BASE, SC_L3=AC3)

**Both reference the same completed L2 SKU.**

**L1 BASE columns (core):**
- Category = Motor Control
- Item_ProductType = Contactor
- Business_SubCategory = Power Contactor (or Capacitor Duty when LP1D / LC1DT indicates capacitor/bundled series)
- SC_L1_Set = {POLES_3 or POLES_4} (derived from SKU family LC1D vs LC1DT vs LP1D)
- SC_L2_Set = {COIL_AC or COIL_DC} (derived from CoilCode group: M7/N7/F7 = AC; BD/FD/MD/BL/EL = DC)
- SC_L3_Set = {AC1} OR {AC3}
- SC_L4_Set = {AUX_1NO_1NC} (if printed as standard; else blank and handled as features later)

**L1 Attributes (KVU):**

Attach to each L1 line:
- VOLTAGE_TYPE = AC/DC (from L2)
- VOLTAGE_VALUE = 24/110/220/415 etc (from L2)
- DUTY_CLASS = AC1 or AC3 (from L1 SC_L3)
- CURRENT_A = value from AC1/AC3 columns for that base reference (from catalog row)
- KW = from table
- HP = from table

**Important:** current/kW/HP values come from the catalog table for the base reference LC1Dxx*, not from the coil suffix.

### 12.4 Output Counts Logic (for LC1D family)

**If a completed L2 SKU is a standard contactor and catalog provides both AC1+AC3 ratings:**
- 2 L1 lines per L2 SKU (AC1 + AC3)

**If catalog provides only one duty class (rare):**
- 1 L1 line per L2 SKU

---

## 13. Final Truth for LC1D

### What is TRUE
- ✅ L2 = completed OEM catalog numbers only
- ✅ Coil voltage does create multiple L2 rows (when SKU suffix changes)
- ✅ AC1 / AC3 never creates L2 split
- ✅ Frame never creates L2 split
- ✅ Accessories never multiply L2

### What This Gives You
- ✅ A clean, exhaustive L2 SKU list
- ✅ Fully aligned with NSW Fundamentals v2.0
- ✅ Safe for Phase-5 import
- ✅ L1 derivation becomes deterministic and reversible

---

## 14. Summary - The Complete Picture

### L2 Generation
- **Rule:** L2 rows = count(distinct (Make, Completed OEM_Catalog_No))
- **When:** Only when OEM catalog number changes (including suffix completion)
- **Example:** LC1D09M7, LC1D09N7, LC1D09BD are separate L2 SKUs

### L1 Generation
- **Rule:** L1 lines = engineering interpretations per L2 SKU
- **When:** When engineering meaning changes (duty, voltage interpretation)
- **Example:** For LC1D09M7, create 2 L1 lines (AC1 and AC3) if both ratings exist

### The "6 Lines" Answer
- **YES:** You can have 6 L1 lines (2 duty × 3 voltage)
- **BUT:** They all point to the same L2 SKU unless SKU changes
- **When SKU changes:** Each completed SKU gets its own L2 row, then L1 lines are derived per L2

---

## 15. References

- **NSW Fundamentals v2.0:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Schneider Final Rules:** `SCHNEIDER_FINAL_RULES_v1.2.md`
- **L2/L1 Differentiation:** `SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`

---

**Document Status:** ✅ **LOCKED - FINAL**

**Next Action:** Apply these rules to LC1D FINAL, LC1K, and all subsequent Schneider series.

