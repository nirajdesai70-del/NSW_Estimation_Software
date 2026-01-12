# LC1E Page-8 — FINAL SEMANTIC FREEZE

**Status**: 🔒 **FROZEN - DO NOT RE-INTERPRET**  
**Scope**: Page-8 only (3P AC Control, all frames on this page)  
**Date**: 2025-01-XX  
**Objective**: Zero ambiguity for Cursor extraction + NSW L0/L1/L2 + Variant system

---

## 🎯 FREEZE DECISION

**Decision LC1E-P8-FREEZE-01 (LOCKED)**
Page-8 LC1E semantics are correct, complete, and internally consistent.
No further interpretation logic is required.
Cursor must follow these rules verbatim.

**Any Cursor mismatch = script bug, not data ambiguity.**

---

## 1️⃣ Frame Semantics — CORRECT & COMPLETE

### Catalog Reality
- Frame is shown once per block (merged cell)
- Subsequent rows inherit the same frame until the next frame label

### Frozen Rules

**FRAME-1** → LC1E0601 … LC1E2510  
**FRAME-2** → LC1E3201 … LC1E40B10  
**FRAME-3** → LC1E40, LC1E50, LC1E65  
**FRAME-4** → LC1E80, LC1E95

### Implementation Note for Cursor
- Frame must be **stateful carry-forward**, never row-local.
- When a FRAME- row is encountered, update current_frame_label.
- All subsequent rows inherit this frame until the next FRAME- row.

---

## 2️⃣ Base Reference Normalization — CORRECT

### Catalog Issues Handled
- `*`, `**` (asterisks)
- Trailing space + 0 artifacts
- Mixed formats (LC1E40B01*, LC1E40* 0)

### Frozen Examples
- `LC1E0601* 0` → `LC1E0601`
- `LC1E40B01*` → `LC1E40B01`
- `LC1E40* 0` → `LC1E40`

### Normalization Rule
```python
# Remove trailing stars, #, and spaces
base_ref = re.sub(r'\*+\s*$', '', base_ref)
base_ref = re.sub(r'#+\s*$', '', base_ref)
base_ref = base_ref.strip()
```

**No phantom base refs detected.**

---

## 3️⃣ Duty Semantics (AC-1 / AC-3) — CORRECT

### Catalog Reality
- AC-1 and AC-3 are **ratings**, not SKUs
- Same product, different operating current

### Frozen Rules
- AC-1 / AC-3 → **L1 selection dimension**
- For each priced voltage:
  - **Two L1 rows** (one AC1, one AC3)
  - `duty_current_A`:
    - AC1 → catalog AC-1 value
    - AC3 → catalog AC-3 value

### Example
Catalog row:
```
AC-1: 36A | AC-3: 25A | HP: 15 | kW: 11
```

Produces two L1 rows:
```
duty_class: AC1 | duty_current_A: 36 | motor_hp: 15 | motor_kw: 11
duty_class: AC3 | duty_current_A: 25 | motor_hp: 15 | motor_kw: 11
```

**No SKU explosion.**

---

## 4️⃣ HP Semantics — CORRECT & NOW LOCKED

### Catalog Reality
- HP is printed once per row
- HP does **not** change with duty
- Sometimes printed as range (e.g., 25/30)

### Decision HP-LC1E-01 (LOCKED)
**HP is a fixed engineering attribute derived directly from the catalog.**
Ranges use the minimum value.
HP is stored only at L1 level and never drives variants, pricing, or L2 identity.

### Nature of HP in the Catalog
- HP is an **engineering rating**, exactly like kW.
- It is **NOT** a selection dimension.
- It does **NOT** create variants.
- It does **NOT** belong in L2 identity.

**So HP behaves exactly like motor_kw, not like voltage or duty.**

### Canonical Rules (How HP is Stored)

**Rule HP-1 (Direct mapping):**
- If a single HP value is printed → store it directly.
- Example: `15 HP` → `motor_hp = 15`

**Rule HP-2 (Range handling):**
- If HP is printed as a range (e.g. `25/30 HP`):
  - Store **minimum value only**
  - Add note in `notes_raw`

```
motor_hp = 25
notes_raw += "HP_RANGE=25/30; motor_hp=min=25"
```

**Rule HP-3 (No derived conversion):**
- Do **NOT** derive HP from kW.
- Do **NOT** recompute HP using formulas.
- HP must remain **catalog-truth**, not calculated.

**This is critical for auditability.**

### Where HP Lives in NSW

| Layer | HP present? | Why |
|-------|-------------|-----|
| L2 | ❌ No | L2 is identity only |
| Variant | ❌ No | HP is not a variant |
| Price matrix | ❌ No | Price independent of HP |
| L1 | ✅ Yes | Engineering selection context |

**So:**
```
NSW_L1_CONFIG_LINES.motor_hp
```
**is the only place HP exists.**

### Relationship Between HP and Duty (Important)

Even though the catalog prints AC-1 / AC-3 currents, **HP does not change with duty** in LC1E.

**Therefore:**
- For a given base reference:
  - `motor_hp` is **identical** for AC1 and AC3 L1 lines.
  - Only `duty_current_A` changes.

**This prevents phantom duplication.**

### Example (Page-8)

Catalog row:
```
AC-1: 36A | AC-3: 25A | HP: 15 | kW: 11
```

Produces two L1 rows:
```
duty_class: AC1 | duty_current_A: 36 | motor_hp: 15 | motor_kw: 11
duty_class: AC3 | duty_current_A: 25 | motor_hp: 15 | motor_kw: 11
```

**No HP branching. No conversion.**

---

## 5️⃣ kW Semantics — CORRECT

### Same Logic as HP

- kW is **engineering context**
- Range → **minimum value only**
- Stored only in L1
- Same for AC-1 and AC-3

### Frozen Rules
- If kW is a range (e.g., `25/30`):
  - Store minimum: `motor_kw = 25`
  - Note in `notes_raw`: `KW_RANGE=25/30; motor_kw=min=25`

---

## 6️⃣ Voltage / Coil Code Semantics — CORRECT

### Catalog Reality
- Prices differ by coil voltage
- Same base product
- Voltage code appended to reference for pricing only

### Frozen Rules
- Coil code = **VARIANT**, not SKU
- L2 has **no voltage**
- Pricing lives only in `NSW_PRICE_MATRIX`
- Variant examples:
  - `M7` → 220V AC
  - `N5` → 415V AC

### Important
Completed reference (`LC1E0601M7`) is **trace only**, never identity.

---

## 7️⃣ Aux Contacts — CORRECT

### Catalog Reality
- NO / NC columns may show `–`
- Some rows show both `1 / 1`

### Frozen Rules
- `–` → `0`
- Stored as:
  - `aux_no`
  - `aux_nc`
- Used only for:
  - Filtering
  - Generic descriptor
  - Engineering clarity

---

## 8️⃣ Generic Descriptor — CORRECT

### Frozen Format

```
Power Contactor – Easy TeSys – 3P | AC1 | 220V AC | 15kW @ 415V | Aux 1NO+1NC
```

- Series name, not code
- Human readable
- Stable across price updates

---

## 9️⃣ L0 / L1 / L2 Separation — CLEAN

| Layer | Status |
|-------|--------|
| L2 identity | ✅ Base ref only |
| Variants | ✅ Voltage only |
| L1 | ✅ Duty + engineering |
| Price | ✅ Variant matrix |
| SKU explosion | ❌ None |

**This is exactly what NSW Phase-5 expects.**

---

## 🔒 Why This Fixes Cursor Failures

### Previously
- Cursor saw HP sometimes aligned with AC-3 and sometimes not.
- No rule told it whether HP was duty-specific or shared.

### Now
- HP is **duty-independent** and **base-specific**.
- Cursor can copy HP blindly into both AC1/AC3 L1 rows.

---

## 📋 Canonical Column Contract (Page-8)

### Required Columns in LC1E_CANONICAL_ROWS

| Column | Type | Rule |
|--------|------|------|
| `base_ref_clean` | string | Normalized base ref (no *, no coil suffix) |
| `frame_label` | string | FRAME-1 through FRAME-4 (carry-forward) |
| `ac1_current_a` | float | AC-1 current rating |
| `ac3_current_a` | float | AC-3 current rating |
| `motor_hp` | float | HP rating (direct from catalog, min if range) |
| `motor_kw` | float | kW rating (direct from catalog, min if range) |
| `aux_no_count` | int | NO aux contacts (0 if `–`) |
| `aux_nc_count` | int | NC aux contacts (0 if `–`) |
| `notes_raw` | string | Range notes (HP_RANGE, KW_RANGE) |

### Required Columns in LC1E_COIL_CODE_PRICES

| Column | Type | Rule |
|--------|------|------|
| `base_ref_clean` | string | Links to canonical row |
| `coil_code` | string | M7, N5 (3P AC only on Page-8) |
| `voltage_type` | string | AC |
| `voltage_value` | int | 220 (M7), 415 (N5) |
| `completed_sku` | string | base_ref_clean + coil_code |
| `price` | float | Numeric price (>= 100 threshold) |

---

## 🚫 What NOT to Do

1. ❌ **Do NOT** derive HP from kW using formulas
2. ❌ **Do NOT** create separate HP variants
3. ❌ **Do NOT** put HP in L2 identity
4. ❌ **Do NOT** make HP duty-specific (it's base-specific)
5. ❌ **Do NOT** re-interpret Page-8 semantics
6. ❌ **Do NOT** create SKUs from AC1/AC3 differences

---

## ✅ Extraction Pseudocode (Page-8)

```python
# For each data row in Page-8 section:

# 1. Extract base reference
base_ref_raw = find_base_ref_in_row(row)
base_ref_clean = normalize_base_ref(base_ref_raw)  # Remove *, spaces

# 2. Carry forward frame (stateful)
if row_contains_FRAME_label(row):
    current_frame = extract_frame_label(row)
frame_label = current_frame  # Use carried-forward frame

# 3. Extract ratings (duty-independent)
ac1_current = extract_ac1_current(row)
ac3_current = extract_ac3_current(row)
hp = extract_hp(row)  # Direct value, min if range
kw = extract_kw(row)  # Direct value, min if range

# 4. Extract aux contacts
aux_no = extract_aux_no(row)  # 0 if "-"
aux_nc = extract_aux_nc(row)  # 0 if "-"

# 5. Extract coil prices (only if price >= 100)
for coil_code in ['M7', 'N5']:
    price = extract_price_for_coil(row, coil_code)
    if price and price >= 100:
        # Create coil price row
        coil_price_row = {
            'base_ref_clean': base_ref_clean,
            'coil_code': coil_code,
            'completed_sku': base_ref_clean + coil_code,
            'price': price
        }
        coil_prices.append(coil_price_row)

# 6. Create canonical row (once per base_ref)
canonical_row = {
    'base_ref_clean': base_ref_clean,
    'frame_label': frame_label,
    'ac1_current_a': ac1_current,
    'ac3_current_a': ac3_current,
    'motor_hp': hp,  # Same for AC1 and AC3
    'motor_kw': kw,  # Same for AC1 and AC3
    'aux_no_count': aux_no,
    'aux_nc_count': aux_nc,
    'notes_raw': build_range_notes(hp, kw)
}
canonical_rows.append(canonical_row)
```

---

## 📝 Next Steps

With Frame + BaseRef + Duty + Voltage + kW + HP all frozen:

👉 **Cursor can now correctly regenerate Page-8 without guessing.**

### Apply Same Model To:
1. **Page-9** (3P DC Control) = same L1/L2/variant logic
2. **Page-10** (Accessories) = FEATURE L1 (separate)
3. Coil voltage still variant

---

## 🔗 Related Documents

- `LC1E_PRICELIST_STRUCTURE.md` - Physical structure analysis
- `LC1E_STATUS.md` - Execution status
- `README.md` - Archive overview

---

**END OF FREEZE DOCUMENT**

**Do not re-interpret. Follow rules verbatim.**

