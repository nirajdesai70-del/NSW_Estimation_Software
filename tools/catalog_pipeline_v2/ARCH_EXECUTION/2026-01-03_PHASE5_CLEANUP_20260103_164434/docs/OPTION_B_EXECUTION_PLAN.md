# Option B Execution Plan - Gaps Addressed & Ready for Implementation

## ✅ Review Verdict

**Option B is CORRECT and SHOULD BE ADOPTED** with 4 mandatory patches. All patches are necessary, but there are **4 critical gaps** that must be addressed before execution.

---

## 🔴 CRITICAL GAP 1: LC1E Canonical Table Does NOT Exist

**Status**: BLOCKER - Must be resolved first

**Issue**: All patches assume a populated LC1E canonical table, but it doesn't exist yet.

**Action Required**:
1. Build LC1E canonical table from raw pricelist (`Switching _All_WEF 15th Jul 25.xlsx`)
2. Extract pages 8-10 into 3 sheets:
   - `LC1E_CANONICAL_ROWS` (base refs + AC1/AC3 ratings + HP/kW)
   - `LC1E_COIL_CODE_PRICES` (completed SKUs: base + coil code + price)
   - `LC1E_ACCESSORY_SKUS` (accessory SKUs with proper tagging)

**Next Step**: Proceed with building canonical table (Step 0)

---

## ⚠️ GAP 2: M5 vs M7 Coil Code Ambiguity

**Status**: Needs Verification Before Patch 1

**Issue**: Observation mentions M5 (220V) but current code has M7 (220V). Are these:
- Same coil code, different naming variant?
- Different coil codes (different families/characteristics)?

**Action Required**:
- Inspect raw pricelist to see if M5 and M7 both appear as separate columns
- If M5 = M7 (same thing): Don't add duplicate entry
- If M5 ≠ M7 (truly different): Add M5 to COIL_CODE_MAP

**Recommendation**: After building canonical table, check for M5 vs M7 before adding to coil map.

---

## ⚠️ GAP 3: Unknown Canonical Column Names for IsAccessory Detection

**Status**: Needs Inspection After Step 0

**Issue**: Patch 3 requires `IsAccessory` flag based on canonical columns, but we don't know the exact column names yet.

**Action Required**:
- After building canonical table, inspect column structure
- Support these patterns (in priority order):
  1. `SC_L4_AccessoryClass` (preferred - from NSW schema)
  2. `AccessoryClass` (alternative)
  3. `is_accessory` (boolean flag)
  4. `SC_L4` (short form)
- If none exist: Set `IsAccessory = False` (safer than wrong detection)

**Recommendation**: Implement flexible detection that tries multiple column name patterns.

---

## ⚠️ GAP 4: SC_L2_Operation Missing Range Code Handling

**Status**: Enhancement Needed (Not in Observation)

**Issue**: Current code sets `SC_L2_Operation = voltage_type + ' Coil'` for all SKUs, but coil range codes (BBE, BNE, EHE, KUE) should show "AC/DC Coil Range".

**Action Required**:
- In Script B `create_l1_base_lines()`, check if voltage is None (range code)
- If range code: `SC_L2_Operation = f"{voltage_type} Coil Range"`
- Otherwise: `SC_L2_Operation = f"{voltage_type} Coil"`

**Recommendation**: Add this enhancement alongside Patch 4.

---

## 📋 Revised Implementation Order (With Gaps Addressed)

### Step 0: Build LC1E Canonical Table (BLOCKER) 🔴
- Parse raw pricelist XLSX (pages 8-10)
- Create 3-sheet canonical workbook
- Verify column structure for Patch 3

**Output**: `output/lc1e/LC1E_CANONICAL_ROWS_v1.xlsx`

### Step 1: Patch Script A - LC1E Coil Codes ✅
**Actions**:
1. Add to `COIL_CODE_MAP`:
   - N5: 415V AC (confirmed needed)
   - M5WB: 220V AC, 4P variant (confirmed needed)
   - N5WB: 415V AC, 4P variant (confirmed needed)
   - M5: 220V AC (verify if different from M7 first)

2. Update `COIL_SUFFIX_PATTERN`:
   - Add: `N5|M5WB|N5WB|M5` (verify M5 first)

3. Update `detect_input_mode()` RAW coil columns list:
   - Add: `'N5', 'M5WB', 'N5WB'` (and 'M5' if verified)

**Files**: `scripts/build_l2_from_canonical.py`

### Step 2: Patch Script B - Duty Per Base_Ref (CRITICAL BUG FIX) 🔴
**Actions**:
1. Create helper function:
   ```python
   def duties_for_base(base_ref, rating_map):
       if rating_map is None or len(rating_map) == 0:
           return ['AC1', 'AC3']  # Safe default for contactors
       duties = rating_map[rating_map['Base_Ref'] == base_ref]['DutyClass'].dropna().unique().tolist()
       return duties if duties else ['AC1', 'AC3']  # Fallback
   ```

2. Replace global `available_duties` with per-base lookup:
   - Inside `for base_ref, group in ...` loop
   - Call `duties_for_base(base_ref, rating_map)`
   - Use returned duties list

**Files**: `scripts/derive_l1_from_l2.py` (Line ~137-178)

### Step 3: Patch Script A + B - Accessory Tagging ✅
**Actions**:

**Script A (`build_l2_sku_master()`)**:
1. Add `IsAccessory` column (default False)
2. Set `IsAccessory = True` if canonical source has:
   - `SC_L4_AccessoryClass` non-empty, OR
   - `AccessoryClass` non-empty, OR
   - `is_accessory == True`, OR
   - `SC_L4` non-empty
3. Support multiple column name patterns (flexible detection)

**Script B (`create_l1_feature_lines_for_accessories()`)**:
1. Replace keyword detection with: `l2_sku_master[l2_sku_master['IsAccessory'] == True]`
2. Locked values:
   - `Item_ProductType = "Contactor"` (locked rule)
   - `Business_SubCategory = "Power Contactor"` (locked rule)
3. Group ID: `GRP-{Make}-{SeriesBucket}-ACCESSORIES` (e.g., `GRP-Schneider-LC1E-ACCESSORIES`)
4. Do NOT multiply across duty/voltage

**Files**: `scripts/build_l2_from_canonical.py`, `scripts/derive_l1_from_l2.py`

### Step 4: Patch Script B - Voltage De-Dup + Range Code SC_L2 ✅
**Actions**:
1. Add voltage variant de-dup (before L1 line creation):
   ```python
   seen = set()
   unique_variants = []
   for v in voltage_variants:
       key = (v['sku'], v['voltage'], v['voltage_type'])
       if key not in seen:
           unique_variants.append(v)
           seen.add(key)
   ```

2. Fix `SC_L2_Operation` for range codes:
   ```python
   if voltage_info['voltage'] is None:  # Range code
       sc_l2_operation = f"{voltage_info['voltage_type']} Coil Range"
   else:
       sc_l2_operation = f"{voltage_info['voltage_type']} Coil"
   ```

**Files**: `scripts/derive_l1_from_l2.py` (Line ~157-195)

### Step 5: Run Pipeline End-to-End ✅
```bash
# Step 1: Build L2
python3 scripts/lc1e_build_l2.py \
  --canonical output/lc1e/LC1E_CANONICAL_ROWS_v1.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out output/lc1e/LC1E_L2_tmp.xlsx

# Step 2: Derive L1
python3 scripts/derive_l1_from_l2.py \
  --l2 output/lc1e/LC1E_L2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out output/lc1e/LC1E_L1_tmp.xlsx

# Step 3: Build Engineer Review Workbook
python3 scripts/build_master_workbook.py \
  --l2 output/lc1e/LC1E_L2_tmp.xlsx \
  --l1 output/lc1e/LC1E_L1_tmp.xlsx \
  --out output/lc1e/LC1E_ENGINEER_REVIEW_v1.xlsx
```

### Step 6: Validate Output Counts ✅
Check:
- L2_SKU_MASTER rows (should match completed SKUs with prices)
- RATING_MAP rows (should have AC1 + AC3 per base ref)
- L1_LINES BASE count (should be duty × voltage combinations)
- L1_LINES FEATURE count (should match accessory SKUs)
- L1_ATTRIBUTES_KVU rows (should be > L1 BASE count)

---

## ✅ Summary of Gaps & Solutions

| Gap | Status | Solution | Priority |
|-----|--------|----------|----------|
| LC1E Canonical Table Missing | 🔴 BLOCKER | Build from raw pricelist (Step 0) | CRITICAL |
| M5 vs M7 Ambiguity | ⚠️ Verify | Inspect raw data before adding to map | HIGH |
| IsAccessory Column Names Unknown | ⚠️ After Step 0 | Support multiple column name patterns | HIGH |
| SC_L2_Operation Range Code Missing | ⚠️ Enhancement | Add "Coil Range" handling | MEDIUM |

---

## 🎯 Recommendation

**PROCEED WITH OPTION B** after addressing Gap 1 (build canonical table first).

**Execution Priority**:
1. ✅ Step 0: Build canonical table (BLOCKER)
2. ✅ Step 2: Patch duty-per-base (CRITICAL bug fix)
3. ✅ Step 1: Add coil codes (enables LC1E support)
4. ✅ Step 3: Accessory tagging (correctness improvement)
5. ✅ Step 4: Voltage de-dup + range code handling (polish)

All patches are necessary and correct. The gaps are addressable during implementation.

