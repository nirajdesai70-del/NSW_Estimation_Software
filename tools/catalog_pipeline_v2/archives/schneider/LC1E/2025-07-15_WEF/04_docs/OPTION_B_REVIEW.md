# Option B (Unified Generic Pipeline) - Review & Gap Analysis

## ✅ Observation Summary

The observation proposes adopting Option B with 4 mandatory patches to make the unified pipeline LC1E-safe. This is the **correct approach** - it keeps a single canonical engine for future Schneider updates while adding LC1E-specific support.

## 📋 Patch-by-Patch Review

### ✅ Patch 1: Script A - Add LC1E Coil Codes + Suffix Regex

**Status**: REQUIRED ✅

**Current State**:
- `COIL_CODE_MAP` has: M7, N7, F7, B7, BD, FD, MD, BL, FL, ML, EL
- Missing: **N5, M5WB, N5WB, M5** (mentioned in observation)
- `COIL_SUFFIX_PATTERN` doesn't include N5, M5WB, N5WB, M5
- RAW mode coil columns detection doesn't include N5, M5WB, N5WB, M5

**Gap Identified**:
- Observation mentions **M5 (220V)** appearing in higher-frame blocks - this needs verification
- Need to confirm: Is M5 different from M7? (Both are 220V AC based on observation)

**Action Required**:
1. Add N5 (415V AC) - confirmed needed for LC1E
2. Add M5WB (220V AC, 4P variant) - confirmed needed
3. Add N5WB (415V AC, 4P variant) - confirmed needed
4. **Verify M5**: If M5 appears as separate from M7 in the raw data, add it. If it's just a variant name for M7, don't duplicate.

**Implementation Priority**: HIGH - Without this, LC1E SKUs will be missed or mis-completed.

---

### ✅ Patch 2: Script B - Fix Duty Expansion (Per Base_Ref, Not Global)

**Status**: CRITICAL BUG FIX ✅

**Current State** (Line 137 in `derive_l1_from_l2.py`):
```python
available_duties = rating_map['DutyClass'].unique().tolist() if len(rating_map) > 0 else []
...
for duty in available_duties if available_duties else ['']:  # Line 178 - GLOBAL!
```

**Problem**:
- Uses **global** duty list for ALL base refs
- This creates phantom AC1/AC3 lines for base refs that don't have those duties
- Example: If RATING_MAP has AC1/AC3 for LC1D09 but only AC3 for LC1E0601, the code will still create AC1 lines for LC1E0601

**Fix Required**:
- Create `duties_for_base(base_ref, rating_map)` helper function
- Filter rating_map by Base_Ref before extracting duties
- Use filtered duties per base_ref iteration

**Implementation Priority**: CRITICAL - This is a correctness bug that produces wrong L1 combinations.

---

### ✅ Patch 3: Script B - Replace Keyword Accessory Detection (Canonical-Tag Driven)

**Status**: REQUIRED ✅

**Current State** (Lines 258-270 in `derive_l1_from_l2.py`):
- Uses keyword matching on `Item_ProductType`, `Business_SubCategory`, `SeriesBucket`
- Keywords: 'aux', 'auxiliary', 'accessory', 'overload', 'olr', 'suppressor', 'interlock'

**Problems**:
1. **Over-broad detection**: May misclassify non-accessories
2. **Under-detection**: May miss accessories with different naming
3. **Not deterministic**: Depends on string matching, not canonical truth

**Fix Required**:
1. **In Script A** (`build_l2_sku_master()`): Add `IsAccessory` column
   - Set `IsAccessory = True` if source has `SC_L4_AccessoryClass` non-empty
   - Or if canonical table has explicit `is_accessory` / `AccessoryClass` column
   - Default to `False` (safer than wrong classification)

2. **In Script B** (`create_l1_feature_lines_for_accessories()`):
   - Replace keyword detection with: `l2_sku_master[l2_sku_master['IsAccessory'] == True]`
   - Locked values:
     - `Item_ProductType = "Contactor"` (as per locked rules)
     - `Business_SubCategory = "Power Contactor"` (as per locked rules)
   - Place in isolated group: `GRP-{Make}-{SeriesBucket}-ACCESSORIES` (e.g., `GRP-Schneider-LC1E-ACCESSORIES`)

**Gap Identified**:
- Need to know canonical table column names to implement `IsAccessory` detection in Script A
- Observation says: "If expanded_df contains SC_L4_AccessoryClass and it's non-empty → IsAccessory=True"
- But we need to check if this column exists in the actual canonical tables

**Implementation Priority**: HIGH - Current approach is unsafe and non-deterministic.

---

### ⚠️ Patch 4: Voltage De-Dup & Range Code Handling

**Status**: ENHANCEMENT (Partially Already Handled) ⚠️

**Current State** (Lines 157-175 in `derive_l1_from_l2.py`):
- Already has logic to handle range codes (voltage = None)
- But no explicit de-dup of voltage variants by (sku, voltage, voltage_type) tuple

**Gap Identified**:
- Observation suggests skipping range-code variants in duty×voltage explosion
- Current code includes them with `voltage=None`
- Need decision: Include range codes as L1 lines (with voltage=None) or skip them?

**Recommendation**:
- **Include range codes** as L1 lines (current behavior is fine)
- They'll have `voltage=None` in KVU, which is acceptable
- Engineer can review and validate
- But add explicit de-dup to avoid duplicate L1 lines

**Action Required**:
- Add de-dup logic before creating L1 lines (using tuple: (sku, voltage, voltage_type))
- Keep range code handling as-is (include them with voltage=None)

**Implementation Priority**: MEDIUM - Current behavior is acceptable, but de-dup improves correctness.

---

## 🎯 Critical Missing Piece

**LC1E Canonical Table Does NOT Exist Yet**

This is the blocker. The patches assume:
- A populated LC1E canonical table with base_refs, AC1/AC3 ratings, coil code prices
- Accessory rows with proper tagging

**Current Status**:
- ✅ Pipeline scripts exist
- ✅ Rules are locked
- ❌ **LC1E canonical data does NOT exist**
- ⚠️ Raw pricelist files are located but not yet parsed

**Action Required BEFORE Patches**:
1. **Build LC1E canonical table from raw pricelist**
   - Extract pages 8-10 (LC1E tables)
   - Create 3 sheets:
     - `LC1E_CANONICAL_ROWS` (base refs + AC1/AC3 ratings)
     - `LC1E_COIL_CODE_PRICES` (completed SKUs with prices)
     - `LC1E_ACCESSORY_SKUS` (accessory SKUs)

2. **Verify column structure** of canonical tables to implement:
   - `IsAccessory` detection (Patch 3)
   - RATING_MAP extraction (Script A)
   - Coil code column detection (Script A)

---

## 📝 Implementation Order (Locked)

1. **Step 0**: Build LC1E canonical table from raw pricelist (BLOCKER)
2. **Step 1**: Patch Script A (coil codes + regex + RAW columns) - Patch 1
3. **Step 2**: Patch Script B duty-per-base - Patch 2 (CRITICAL)
4. **Step 3**: Add IsAccessory column in Script A, rewrite accessory detection in Script B - Patch 3
5. **Step 4**: Add voltage de-dup in Script B - Patch 4
6. **Step 5**: Run pipeline end-to-end and validate counts

---

## ⚠️ Additional Gaps & Recommendations

### Gap 1: Coil Code M5 vs M7 Confusion

**Issue**: Observation mentions M5 (220V) but current map has M7 (220V). Are these different?

**Recommendation**:
- Inspect raw pricelist to see if M5 and M7 both appear
- If M5 is just a naming variant for M7, don't add duplicate entry
- If M5 is truly different (different voltage/family), add it

### Gap 2: Accessory Tagging Column Name Unknown

**Issue**: To implement Patch 3, we need to know canonical table column names.

**Recommendation**:
- After Step 0 (building canonical table), inspect columns
- Add IsAccessory logic based on actual column names
- Support fallback patterns: `SC_L4_AccessoryClass`, `AccessoryClass`, `is_accessory`, `SC_L4`

### Gap 3: RAW Mode Coil Column Detection

**Issue**: Script A's `detect_input_mode()` only checks for ['M7', 'N7', 'F7', 'B7', 'BD', 'FD', 'MD']

**Action Required**:
- Extend to include: 'N5', 'M5WB', 'N5WB', 'M5' (if verified)

### Gap 4: SC_L2_Operation for Coil Range Codes

**Issue**: Current code sets `SC_L2_Operation = voltage_type + ' Coil'` for all SKUs, but range codes should be "AC/DC Coil Range"

**Action Required**:
- Check if voltage is None (range code)
- If range code: `SC_L2_Operation = f"{voltage_type} Coil Range"`
- Otherwise: `SC_L2_Operation = f"{voltage_type} Coil"`

---

## ✅ Final Verdict

**Option B is CORRECT and SHOULD BE ADOPTED** with the following notes:

1. ✅ All 4 patches are necessary and correct
2. ⚠️ Must complete Step 0 (build canonical table) BEFORE applying patches
3. ⚠️ Need to verify M5 vs M7 before adding to coil map
4. ⚠️ Need canonical table structure to implement Patch 3 correctly
5. ✅ Implementation order is correct
6. ✅ Priority: Patch 2 (duty-per-base) is CRITICAL bug fix

**Next Immediate Action**: Build LC1E canonical table from raw pricelist, then proceed with patches in order.

