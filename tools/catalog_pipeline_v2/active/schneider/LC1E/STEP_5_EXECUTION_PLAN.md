# Step 5: Build NSW Master Workbook - Execution Plan

**Date:** 2026-01-03  
**Status:** 🟡 READY FOR VERIFICATION  
**Prerequisites:** ✅ Step 2, 3, 4 complete and validated

---

## 🎯 Objective

Build the final NSW format workbook (PRIMARY freeze artifact) from canonical, L2, and L1 intermediate files.

**Deliverable:** `NSW_LC1E_WEF_2025-07-15_v1.xlsx`

---

## 📋 Execution Steps

### Step 5.1: Build NSW Master Workbook

**Script:** `scripts/build_nsw_workbook_from_canonical.py` ✅ (Real implementation, not placeholder)

**Command:**
```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software/tools/catalog_pipeline_v2/active/schneider/LC1E

python3 ../../../scripts/build_nsw_workbook_from_canonical.py \
  --canonical 02_outputs/LC1E_CANONICAL_v1.xlsx \
  --series LC1E \
  --series_name "Easy TeSys" \
  --wef 2025-07-15 \
  --pricelist_ref "WEF 15 Jul 2025" \
  --out 02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx
```

**Note:** This script builds from canonical only (does not require --l2 or --l1 arguments).

**Input Files:**
- ✅ `02_outputs/LC1E_CANONICAL_v1.xlsx` (23 canonical rows, 59 coil prices)
- ✅ `02_outputs/LC1E_L2_tmp.xlsx` (59 SKUs, 59 price rows)
- ✅ `02_outputs/LC1E_L1_tmp.xlsx` (118 L1 lines, 354 attributes)

**Expected Output:**
- `02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx` (NSW format workbook)

---

## ✅ Gate Checks (Post-Execution)

### Gate A: File Exists and Structure

**Check:**
```bash
ls -lh 02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx
```

**Expected:** File exists, reasonable size (> 10K)

---

### Gate B: Sheet Names and Row Counts

**Check:**
```bash
python3 - <<'PY'
import openpyxl
wb=openpyxl.load_workbook("02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx", data_only=True)
print("Sheet names:", wb.sheetnames)
for s in wb.sheetnames:
    ws=wb[s]
    print(f"{s}: {max(ws.max_row-1,0)} rows, {ws.max_column} cols")
PY
```

**Expected Sheets (per v1.2 CLEAN index):**
- `NSW_SKU_MASTER_CANONICAL` (or `NSW_L2_PRODUCTS`) - L2 SKU identity
- `NSW_PRICE_MATRIX_CANONICAL` (or `NSW_PRICE_MATRIX`) - Price truth
- `NSW_CATALOG_CHAIN_MASTER` - L0/L1/L2 continuity
- `NSW_L1_CONFIG_LINES` - L1 configuration lines
- `NSW_SKU_RATINGS` (if applicable)
- `NSW_ACCESSORY_SKU_MASTER` (if applicable - may be empty for LC1E)

**Expected Row Counts (Gate B2 - Enhanced):**
- NSW_L2_PRODUCTS (or NSW_SKU_MASTER_CANONICAL): ~59 rows (matches canonical coil prices)
- NSW_PRICE_MATRIX: ~59 rows (matches canonical coil prices)
- NSW_L1_CONFIG_LINES: Should match L1 derivation logic (duty×voltage combinations)
- Catalog chain: Should link L0/L1/L2

**Critical:** Must NOT be empty sheets (prevents "file exists but empty" false passes)

---

### Gate C: Generic Naming Neutrality (L1 Sheets Only)

**Check:**
```bash
python3 - <<'PY'
import re, openpyxl

def token_hit(text, token):
    if not isinstance(text, str):
        return False
    pattern = rf"\b{re.escape(token)}\b"
    return re.search(pattern, text, re.IGNORECASE) is not None

bad = ["SCHNEIDER","LC1E","TESYS","EASY TESYS","NSX","NW","NT"]
wb=openpyxl.load_workbook("02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx", data_only=True)

# Check only L1 sheets (NSW_L1_CONFIG_LINES, NSW_CATALOG_CHAIN_MASTER if it has L1 data)
l1_sheets = [s for s in wb.sheetnames if "L1" in s.upper() or "CHAIN" in s.upper()]
hits=[]

for s in l1_sheets:
    ws=wb[s]
    headers={ws.cell(1,c).value: c for c in range(1, ws.max_column+1) if isinstance(ws.cell(1,c).value,str)}
    cols=[h for h in headers if "name" in h.lower() or "desc" in h.lower() or "generic" in h.lower()]
    for h in cols:
        c=headers[h]
        for r in range(2, ws.max_row+1):
            v=ws.cell(r,c).value
            if isinstance(v,str):
                for t in bad:
                    if token_hit(v, t):
                        hits.append((s,r,h,t,v))

print("BAD NAME HITS (L1 sheets only):", len(hits))
for x in hits[:20]:
    print(x)
PY
```

**Target:** BAD NAME HITS: 0

---

### Gate D: SC_Lx Structural-Only Check

**Check:**
```bash
python3 - <<'PY'
import re, openpyxl
wb=openpyxl.load_workbook("02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx", data_only=True)
bad = re.compile(r"(AC1|AC3|KW|HP|WITH_|AUX|SHUNT|UV|DRAWOUT|COIL|V\b|VOLT)", re.I)

def check_sc(sheet):
    ws=wb[sheet]
    headers={ws.cell(1,c).value: c for c in range(1, ws.max_column+1) if isinstance(ws.cell(1,c).value,str)}
    sc_cols=[h for h in headers if h and h.upper().startswith("SC_L")]
    hits=[]
    for h in sc_cols:
        c=headers[h]
        for r in range(2, ws.max_row+1):
            v=ws.cell(r,c).value
            if isinstance(v,str) and bad.search(v):
                hits.append((sheet,r,h,v))
    return hits

hits=[]
for s in wb.sheetnames:
    hits += check_sc(s)

print("SC_Lx BAD HITS:", len(hits))
for x in hits[:25]:
    print(x)
PY
```

**Target:** SC_Lx BAD HITS: 0

**Rule:** SC_Lx must NOT contain:
- Coil voltage
- AC1/AC3 duty/rating
- kW/HP
- Capability tokens (WITH_*, AUX, SHUNT, UV, DRAWOUT)

---

### Gate E: Capability Separation

**Check:**
```bash
python3 - <<'PY'
import openpyxl
wb=openpyxl.load_workbook("02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx", data_only=True)

for s in wb.sheetnames:
    ws=wb[s]
    headers={ws.cell(1,c).value: c for c in range(1, ws.max_column+1) if isinstance(ws.cell(1,c).value,str)}
    
    sc_cols=[h for h in headers if h and h.upper().startswith("SC_L")]
    cap_cols=[h for h in headers if "capability" in h.lower()]
    
    if sc_cols or cap_cols:
        print(f"\nSheet: {s}")
        if sc_cols:
            print(f"  SC_Lx columns: {sc_cols}")
        if cap_cols:
            print(f"  Capability columns: {cap_cols}")
PY
```

**Expected:**
- SC_Lx columns present (structural only)
- `capability_codes` column present (if capabilities exist)
- No SC_Lx → capability_class mapping

---

### Gate F: Layer Discipline

**Check:**
- [ ] L0/L1/L2 boundaries respected
- [ ] Make/Series/Price are L2-only
- [ ] Generic names are L0/L1-only (vendor/series-neutral)
- [ ] Prices only in price matrix

**Manual Review:**
- Verify L2 sheets contain Make, Series, SKU, Price
- Verify L1 sheets contain generic descriptors (no OEM/series)
- Verify price matrix structure is correct

---

## 📊 Success Criteria

**Step 5 passes if:**
- [x] File exists and is readable
- [ ] All expected sheets present
- [ ] Row counts match expected (L2: ~59, L1: ~118, Price: ~59)
- [ ] Generic naming: 0 hits in L1 sheets
- [ ] SC_Lx: 0 hits (structural-only)
- [ ] Capability uses `capability_codes` (not SC_Lx)
- [ ] Layer discipline respected

---

## ⚠️ Known Issues / Warnings

1. **IsAccessory warning** (from Step 4): Non-blocking for LC1E (0 accessories)
2. **RATING_MAP empty**: Expected for LC1E (ratings in canonical, not separate map)

---

## 🚀 Next Steps (After Step 5 Passes)

1. **Step 6: QC** - Create QC summary document
2. **Step 7: Governance Review** - Upload to ChatGPT
3. **Step 8: Archive** - If approved

---

## 📝 Notes

- This is the PRIMARY freeze artifact
- Must comply with v1.2 CLEAN rules
- No manual edits - all data from pipeline

---

**Status:** Ready for verification and execution.

