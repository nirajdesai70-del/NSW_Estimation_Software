# Phase 5 Preparation: Contactor (LC1E) Sheet Build

**Date:** 2026-01-03  
**Status:** 🟡 PREPARATION - READY FOR EXECUTION  
**Aligned With:** NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md

---

## 🎯 Phase 5 Objective

Build the Contactor (LC1E) sheet using the corrected pipeline scripts, ensuring full compliance with freeze v1.2 rules.

**Deliverable:** `NSW_LC1E_WEF_<DATE>_v1.xlsx` (canonical NSW format workbook)

### Terminology lock (do not mix)

- **"Layer-1 / Layer-2"** = operating modes:
  - Layer-1 Mode: Price List → Item Master (facts only)
  - Layer-2 Mode: Engineering/BOM (rules + dependencies + QC)
- **"L0 / L1 / L2"** = NSW levels:
  - L0 intent, L1 spec, L2 OEM SKU + price

This prevents the exact "L1 facts / L2 rules" confusion from reappearing.

---

## ✅ Prerequisites (Completed)

### Phase 2: Master File Alignment ✅
- ✅ TERMINOLOGY_ALIASES fixed (SC_Lx → SCL)
- ✅ Generic naming sanitized
- ✅ SC_Lx verified as structural-only
- ✅ Normalized file: `ITEM_Master_020126_v1.4_NORMALIZED.xlsx`

### Phase 3: Freeze Documents ✅
- ✅ `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md` (canonical)
- ✅ `NSW_SHEET_SET_INDEX_v1.2_CLEAN.md` (canonical)
- ✅ All 10 fixes applied to terminology freeze
- ✅ All 5 fixes applied to sheet index

### Phase 4: Script Corrections ✅
- ✅ `migrate_sku_price_pack.py` fixed:
  - Removed SC_Lx → capability_class_x auto-mapping
  - Added generic naming validator (warning-only)
  - Enhanced warning format for actionable review
- ✅ Scripts aligned with freeze v1.2 rules

---

## 📋 Phase 5 Execution Plan

### Step 1: Input File Preparation

**Location:** `active/schneider/LC1E/00_inputs/`

**Required Files:**
- `Switching _All_WEF 15th Jul 25.xlsx` (or latest pricelist)
- `Switching _All_WEF 15th Jul 25.pdf` (optional, for reference)

**Validation:**
- [ ] Input file exists and is readable
- [ ] File contains LC1E pricelist data (pages 8-10)
- [ ] Date/WEF information is clear

### Script naming reality check (mandatory before run)

Before execution, list actual scripts present in:
- `active/schneider/LC1E/01_scripts/`
- `scripts/`

Update this document to match the actual filenames before running.

This avoids false-starts.

---

### Step 2: Canonical Extraction

**Script:** `scripts/lc1e_extract_canonical.py`

**Command:**
```bash
cd active/schneider/LC1E/
python ../../scripts/lc1e_extract_canonical.py \
  --input_xlsx 00_inputs/Switching_All_WEF_15th_Jul_25.xlsx \
  --out 02_outputs/LC1E_CANONICAL_v1.xlsx
```

**Expected Output:**
- `LC1E_CANONICAL_ROWS` sheet (base reference rows with AC1/AC3 ratings)
- `LC1E_COIL_CODE_PRICES` sheet (completed SKU rows from coil columns)
- `LC1E_ACCESSORY_SKUS` sheet (accessory SKUs from page 10)

**Validation Checklist:**
- [ ] Canonical extraction completes without errors
- [ ] Row counts match expected (verify against source)
- [ ] Generic names validated (no OEM/series leakage)
- [ ] SC_Lx columns contain structural data only (no capability)
- [ ] Generic naming warnings reviewed (if any)

---

### Step 3: Build L2 from Canonical

**Script:** `scripts/lc1e_build_l2.py`

**Command:**
```bash
python ../../scripts/lc1e_build_l2.py \
  --canonical 02_outputs/LC1E_CANONICAL_v1.xlsx \
  --pricelist_ref "WEF 15 Jul 2025" \
  --effective_from 2025-07-15 \
  --currency INR \
  --region INDIA \
  --out 02_outputs/LC1E_L2_tmp.xlsx
```

**Validation Checklist:**
- [ ] L2 build completes without errors
- [ ] All SKUs have required fields (make, series, SKU, price)
- [ ] Generic names are vendor/series-neutral
- [ ] SC_Lx columns preserved as-is (not mapped to capability_class)
- [ ] Price matrix structure correct
- [ ] Generic naming warnings reviewed (if any)

---

### Step 4: Derive L1 from L2

**Script:** `scripts/derive_l1_from_l2.py`

**Command:**
```bash
python ../../scripts/derive_l1_from_l2.py \
  --l2 02_outputs/LC1E_L2_tmp.xlsx \
  --l1_mode duty_x_voltage \
  --include_accessories true \
  --out 02_outputs/LC1E_L1_tmp.xlsx
```

**Validation Checklist:**
- [ ] L1 derivation completes without errors
- [ ] L1 lines created for all duty×voltage combinations
- [ ] Generic names remain vendor/series-neutral
- [ ] No SC_Lx → capability_class mapping
- [ ] Attributes (ATTR_*) populated only if explicitly in source

---

### Step 5: Build NSW Master Workbook

**Script:** `scripts/build_nsw_workbook_from_canonical.py` (or `build_master_workbook.py`)

**Command:**
```bash
python ../../scripts/build_nsw_workbook_from_canonical.py \
  --canonical 02_outputs/LC1E_CANONICAL_v1.xlsx \
  --l2 02_outputs/LC1E_L2_tmp.xlsx \
  --l1 02_outputs/LC1E_L1_tmp.xlsx \
  --out 02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx
```

**Expected Output Sheets:**
- `NSW_SKU_MASTER_CANONICAL` (L2 SKU identity)
- `NSW_PRICE_MATRIX_CANONICAL` (Price truth)
- `NSW_CATALOG_CHAIN_MASTER` (L0/L1/L2 continuity)
- `NSW_L1_CONFIG_LINES` (L1 configuration lines)
- `NSW_SKU_RATINGS` (if applicable)
- `NSW_ACCESSORY_SKU_MASTER` (if applicable)

**Validation Checklist:**
- [ ] NSW workbook structure matches LC1E v6 pattern
- [ ] All sheets present and populated
- [ ] Column names align with freeze v1.2 terminology
- [ ] Generic names validated (no OEM/series in generic fields)
- [ ] SC_Lx columns are structural-only (SCL)
- [ ] Capability uses `capability_codes` (not SC_Lx)
- [ ] Layer discipline respected (L0/L1/L2 boundaries)

---

### Step 6: Quality Control

**Template:** `templates/QC_SUMMARY_TEMPLATE.md`

**Actions:**
1. Copy template to `03_qc/QC_SUMMARY.md`
2. Fill out QC checklist:
   - Row counts (canonical, L2, L1, variants)
   - Sanity checks (frame, duty, voltage, pricing)
   - Generic naming validation
   - SC_Lx vs capability separation
   - Layer discipline compliance
3. Document any warnings or issues

**QC Checklist:**
- [ ] Row counts match expected
- [ ] No generic naming violations (OEM/series in generic fields)
- [ ] SC_Lx contains structural data only
- [ ] Capability uses `capability_codes` column
- [ ] L0/L1/L2 boundaries respected
- [ ] Price matrix structure correct
- [ ] All required columns present
- [ ] No data loss during transformation

---

### Step 7: ChatGPT Review (Governance)

**AI safety:**
- Do NOT upload the v1.4 MASTER Engineering Bank to AI tools.
- Upload only AI-SAFE workbooks or output artifacts intended for review.

**Upload Artifacts:**
1. `NSW_LC1E_WEF_2025-07-15_v1.xlsx` (final NSW workbook)
2. `03_qc/QC_SUMMARY.md` (QC checklist)

**Review Questions:**
- "Review this NSW file and QC summary for LC1E"
- "Is this ready to freeze?"
- "Verify compliance with freeze v1.2 rules"

**Expected Response:**
- ✅ "OK to freeze" OR
- ❌ "Fix these issues: [list]"

---

### Step 8: Archive (If Approved)

**Actions:**
1. Move to `archives/schneider/LC1E/2025-07-15_WEF/`
2. Organize files:
   - `00_inputs/` - Original pricelist files
   - `01_scripts/` - Scripts used (if modified)
   - `02_outputs/` - Final NSW workbook
   - `03_qc/` - QC summary
   - `04_docs/` - Any series-specific notes
   - `05_decisions/` - ChatGPT review decision
3. Create `README.md` with summary

---

## 🔍 Critical Compliance Checks

### Freeze v1.2 Rule Compliance

**Must Verify:**
1. **SC_Lx = SCL (Structural Only)**
   - [ ] SC_Lx columns contain frame, poles, actuation, mounting, terminals, zones, enclosure, variants
   - [ ] SC_Lx does NOT contain capability/options/features
   - [ ] No SC_Lx → capability_class_x mapping
   - [ ] SC_Lx must NOT contain:
     - [ ] Coil voltage
     - [ ] AC1/AC3 duty/rating
     - [ ] kW/HP
     - [ ] Capability tokens (WITH_*, AUX, SHUNT, UV, DRAWOUT)

2. **Generic Naming Neutrality**
   - [ ] Generic names (l0_name, l1_name) are vendor/series-neutral
   - [ ] No OEM names (Schneider, ABB, Siemens, etc.)
   - [ ] No series names (LC1E, GZ1E, NSX, etc.)
   - [ ] Make/Series only in L2 identity fields

3. **Layer Discipline**
   - [ ] Phase-5 pipeline is Catalog Pipeline Mode (still not BOM)
   - [ ] It is allowed to build:
     - [ ] NSW_CATALOG_CHAIN_MASTER
     - [ ] NSW_L1_CONFIG_LINES
   - [ ] But it must not apply:
     - [ ] Accessory dependency enforcement
     - [ ] BOM explosion
     - [ ] Runtime QC gating beyond reporting
   - [ ] Catalog pipeline mode: data + deterministic derivations (no BOM dependency enforcement)
   - [ ] L0/L1/L2 are engineering levels (intent/spec/SKU)
   - [ ] Make/Series/Price are L2-only

4. **Capability Separation**
   - [ ] Capability uses `capability_codes` column
   - [ ] Capability is separate from SC_Lx
   - [ ] No auto-mapping between SC_Lx and capability

---

## ⚠️ Known Issues & Warnings

### Generic Naming Validator
- Script will warn if OEM/series found in generic fields
- Warnings are non-blocking (review and fix manually)
- Format: `WARN GenericNaming: sheet=<name> row=<idx> col=<col> token=<token> value="<value>"`
- **Enforcement:** If generic naming warnings occur:
  - Fix the source naming generator (preferred)
  - OR apply a controlled post-processing cleanup step
  - Do NOT manually edit hundreds of rows without logging the change

### SC_Lx Preservation
- SC_Lx columns are preserved as-is (not renamed)
- Do NOT interpret SC_Lx as capability
- Capability must use separate `capability_codes` column

---

## 📚 Reference Documents

**Canonical (Use These):**
- `freeze_docs/NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md`
- `freeze_docs/NSW_SHEET_SET_INDEX_v1.2_CLEAN.md`

**Scripts:**
- `scripts/migrate_sku_price_pack.py` (Phase 4 fixed)
- `scripts/lc1e_extract_canonical.py`
- `scripts/lc1e_build_l2.py`
- `scripts/derive_l1_from_l2.py`
- `scripts/build_nsw_workbook_from_canonical.py`

**Templates:**
- `templates/QC_SUMMARY_TEMPLATE.md`
- `templates/run_pipeline.sh`

**Operating Model:**
- `OPERATING_MODEL.md` (Cursor + ChatGPT workflow)

---

## ✅ Phase 5 Readiness Checklist

**Before Starting:**
- [x] Phase 2 complete (master file normalized)
- [x] Phase 3 complete (freeze docs v1.2 CLEAN)
- [x] Phase 4 complete (scripts fixed)
- [ ] Input files prepared
- [ ] Scripts reviewed and understood
- [ ] Freeze v1.2 rules understood
- [ ] QC template ready

**Ready to Execute:** ✅ YES

---

## 🚀 Next Steps

1. **Prepare input files** in `active/schneider/LC1E/00_inputs/`
2. **Review scripts** to understand extraction logic
3. **Run Step 1** (Canonical Extraction)
4. **Validate output** against freeze v1.2 rules
5. **Continue through steps** with validation at each stage
6. **Upload to ChatGPT** for final review
7. **Archive** if approved

---

**Status:** Ready for execution. All prerequisites complete. Freeze v1.2 rules locked and scripts aligned.

