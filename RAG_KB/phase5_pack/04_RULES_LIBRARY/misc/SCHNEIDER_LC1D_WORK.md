---
Source: docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/SCHNEIDER_LC1D_WORK.md
KB_Namespace: phase5_docs
Status: WORKING
Last_Updated: 2025-12-27T19:04:42.472622
KB_Path: phase5_pack/04_RULES_LIBRARY/misc/SCHNEIDER_LC1D_WORK.md
---

# SCHNEIDER LC1D — WORK FILE
## Catalog Conversion Execution Notes

**Family Code:** LC1D  
**Family Name:** TeSys Deca Power Contactors  
**OEM:** Schneider Electric  
**Status:** ⏳ Pending  
**Profile:** schneider_lc1d_v1.yml  
**Started On:** <YYYY-MM-DD>  
**Completed On:** <YYYY-MM-DD>

---

## 1. Purpose of This File

This document captures **family-specific execution details** while converting the Schneider LC1D catalog into NSW canonical CSV format.

It exists to:
- Record **data quirks and exceptions**
- Track **profile tuning decisions**
- Document **why rules were adjusted**
- Support **SOP derivation**

⚠️ This file is **not canonical**. Once the SOP stabilizes, this becomes reference-only.

---

## 2. Scope Lock (Very Important)

### Catalog Ownership Rule (AUTHORITATIVE)
**If a catalog item appears under the LC1D series section in the price list, it MUST be considered part of the LC1D catalog family — regardless of where a similar base series appears elsewhere.**

This applies even if:
- The base contactor series appears in another section (e.g., standard motor duty)
- The same core contactor is reused for capacitor duty, special pole configuration, bundled NO/NC, AC/DC coil variants
- Schneider uses LP1D references inside LC1D tables

👉 **Context of appearance in the catalog defines catalog ownership, not electrical similarity.**

### Included (Unified Scope)
- **ALL SKUs appearing under LC1D/TeSys Deca sections:**
  - LC1D* (all variants - standard, capacitor duty, special applications)
  - LC1DT* (capacitor duty variants)
  - LC1D*A (special variants)
  - LP1D* when shown inside LC1D tables (as Schneider's extended references)
  - All pole counts (2P / 3P / 4P)
  - All coil types (AC / DC)
  - All coil voltages (24V / 110V / 220V / others)
  - All applications (motor duty, capacitor duty, special)

### Explicitly Excluded (Handled Elsewhere)
- Accessories (LAD, LA, LB, etc.) - will be handled as separate accessory families
- Pure control relays (LP1K) - handled as separate LP1K family
- LC1K tables that are not inside LC1D sections - handled separately

**Note:** This unified approach preserves all LC1D variants as catalog data. Phase-5 BOM logic and quotation rules will handle application-specific logic (motor vs capacitor duty, bundled vs composable) later, without requiring catalog re-import.

---

## 3. Source Artifacts

### 3.1 Original Sources
- **XLSX Source:**  
  `tools/catalog_pipeline/input/raw/schneider/master/Switching _Pricelist_WEF 15th Jul 25.xlsx`
- **WEF / Revision Date:** 15th July 2025
- **Pages Covered:** TeSys Deca Power Contactors section (LC1D)

### 3.2 XLSX Conversion
- **Converted XLSX:**  
  `tools/catalog_pipeline/input/raw/schneider/master/Switching _Pricelist_WEF 15th Jul 25.xlsx`
- **Conversion Tool Used:** Standard PDF-to-XLSX converter
- **Manual Cleanup Performed:**  
  - [ ] Removed headers/footers  
  - [ ] Merged split tables  
  - [ ] Other: Master source file stored in master/ directory

---

## 4. Profile Configuration

### 4.1 Profile File
- `tools/catalog_pipeline/profiles/schneider/schneider_lc1d_v1.yml`

### 4.2 Key Profile Decisions
- **Column Mapping:**  
  - SKU column index: 6 (after collapsing row to non-empty cells)  
  - Price column index: 7 (MRP column)  
- **Series Detection:**  
  - Heading-based: Yes (primary method)  
  - Prefix-based fallback: Yes (LC1D prefix mapping)
- **Scope Filter:**  
  - Applied: Yes  
  - Pattern(s): `"TeSys Deca Power Contactors (LC1D)"`
- **Strategy:** Extract only LC1D power contactor SKUs. Accessories and control relays (LP1K/LC1K) handled separately.

---

## 5. Step-by-Step Execution

### Step 1: Create WORK File

✅ File created: `SCHNEIDER_LC1D_WORK.md`

### Step 2: Prepare TEST Input

```bash
mkdir -p tools/catalog_pipeline/input/test/schneider/lc1d
cp tools/catalog_pipeline/input/raw/schneider/master/Switching\ _Pricelist_WEF\ 15th\ Jul\ 25.xlsx \
   tools/catalog_pipeline/input/test/schneider/lc1d/Schneider_LC1D_TEST1.xlsx
```

### Step 3: TEST Normalization

```bash
cd tools/catalog_pipeline
python normalize.py \
  --profile profiles/schneider/schneider_lc1d_v1.yml \
  --file input/test/schneider/lc1d/Schneider_LC1D_TEST1.xlsx \
  --mode test
```

**Review:**
- `output/test/`
- `errors/test/`
- `logs/test/*.json`

**PASS Criteria:**
- Only LC1D SKUs
- Prices present and numeric
- No LP1K / LC1K bleed
- Stable row count across reruns

### Step 4: FINAL Freeze

```bash
mkdir -p tools/catalog_pipeline/input/final/schneider/lc1d
cp tools/catalog_pipeline/input/test/schneider/lc1d/Schneider_LC1D_TEST1.xlsx \
   tools/catalog_pipeline/input/final/schneider/lc1d/Schneider_LC1D_FINAL_$(date +%Y-%m-%d).xlsx
```

### Step 5: FINAL Normalization

```bash
python normalize.py \
  --profile profiles/schneider/schneider_lc1d_v1.yml \
  --file input/final/schneider/lc1d/Schneider_LC1D_FINAL_$(date +%Y-%m-%d).xlsx \
  --mode final
```

### Step 6: Import (Mandatory Order)

**Dry-run:**

```bash
curl -X POST "http://localhost:8011/api/v1/catalog/skus/import?dry_run=true" \
  -F "file=@tools/catalog_pipeline/output/final/*LC1D*normalized*.csv"
```

**Commit:**

```bash
curl -X POST "http://localhost:8011/api/v1/catalog/skus/import?dry_run=false" \
  -F "file=@tools/catalog_pipeline/output/final/*LC1D*normalized*.csv"
```

### Step 7: Verification

**Expected after LC1D:**
- CatalogItems: 3 (LC1E, LP1K, LC1D)
- LC1D SKUs visible via:

```bash
curl "http://localhost:8011/api/v1/catalog/skus?make=Schneider" | jq '.total'
```

---

## 6. TEST Normalization Notes

### 6.1 TEST Runs
| Run | Date | Rows Output | Issues Found | Action Taken |
|----|------|-------------|--------------|--------------|
| T1 | 2025-12-26 | 16 | Only capacitor duty table extracted | Updated normalize.py to scan cells 0-3 for LC1D patterns |
| T2 | 2025-12-26 | 32 | Price extraction issues for single-cell format rows; 7 SKUs still missing | Enhanced SKU detection; price extraction needs refinement for single-cell format |

### 6.2 Table Structure Discovery

LC1D has TWO different table structures in the Excel file:

1. **Capacitor Duty Table** (rows ~471-485):
   - Multi-column format
   - SKU at collapsed index 3
   - Prices in subsequent columns (M7/N7/F7 voltages)
   - ✅ Working correctly

2. **Standard Motor Duty Table** (rows ~532-545):
   - Single-cell format (all data in one Excel cell)
   - SKU and prices in same collapsed cell (index 0)
   - Enhanced normalize.py to parse within cell content for prices
   - ✅ Mostly working (28/32 SKUs have correct prices)

**Total LC1D SKUs in Excel:** 41 (37 LC1D + 4 LP1D)  
**Currently extracted:** 32 SKUs (78% coverage)  
**SKUs with correct prices:** 28 SKUs (87.5% of extracted)  
**SKUs needing manual price verification:** 4 SKUs (see below)  
**Missing SKUs:** 9 SKUs (LC1D115A, LC1D12, LC1D18, LC1D38, LC1D50A, LC1D65A, LC1D95, LC1D40, LC1D80)

**SKUs Requiring Manual Price Verification:**
- LC1D09 (extracted price: 1, expected: ~4420)
- LC1DT20 (extracted price: 1, expected: ~4080)
- LC1DT60A (extracted price: 1, expected: ~16910)
- LC1D40008 (extracted price: 2, expected: verify from Excel)

**Enhancement Applied:** Updated normalize.py to scan within single-cell content for prices after SKU detection, with price range validation (1000-100000 INR).

### 6.2 Common Issues Observed
- SKU format inconsistencies:
  - e.g. `<example>`
- Price formatting:
  - e.g. commas, ranges, "On Request"
- Header noise / section bleed:
  - e.g. `<example>`

---

## 7. FINAL Freeze

### 7.1 FINAL Source
- **FINAL XLSX:**  
  `tools/catalog_pipeline/input/final/schneider/lc1d/Schneider_LC1D_FINAL_<YYYY-MM-DD>.xlsx`

### 7.2 FINAL Output
- **FINAL CSV:**  
  `tools/catalog_pipeline/output/final/schneider_<Family>_FINAL_<YYYY-MM-DD>_normalized_<timestamp>.csv`
- **Profile Version:** `v1`
- **Rows Output:** <count>

⚠️ FINAL artifacts are **immutable**.

---

## 8. Import Verification

### 8.1 Dry-Run
- Result: ⏳ Pending
- Errors (if any): TBD

### 8.2 Commit Import
- **Batch ID:** TBD
- **CatalogItem Created:** TBD
- **SKUs Imported:** TBD
- **Price Rows Inserted:** TBD

---

## 9. Exceptions & Decisions

### 9.1 Scope Decisions
- **LC1D power contactors only:** Profile extracts only LC1D SKUs. Accessories and control relays (LP1K/LC1K) are excluded and will be handled under separate family profiles.
- **Accessories excluded:** Auxiliary contacts (LAD, LA, LB, etc.), coils, and mounting kits are not included. These will be handled as separate accessory families per `SCHNEIDER_ACCESSORIES_PLAN.md`.

### 9.2 Pricing Strategy
- **MRP extraction:** Profile selects MRP prices from column index 7 (after row collapsing).
- **Price extraction:** Uses standard column mapping based on collapsed row structure.

### 9.3 SKU Validation
- **Prefix-based:** Only SKUs starting with "LC1D" are extracted.
- **Pattern:** LC1D#### format expected.

---

## 10. SOP Feedback (Important)

List **generalizable learnings** that should feed back into the SOP:

- [ ] New ignore rule discovered
- [ ] Better series detection pattern
- [ ] Column-shift heuristic needed
- [ ] Validation rule refinement

> These items must be reviewed when updating  
> `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md`

---

## 11. Definition of DONE (LC1D)

LC1D is DONE when:
- ✅ Profile schneider_lc1d_v1.yml frozen
- ✅ FINAL CSV generated
- ✅ Import committed
- ✅ Documented in:
  - SCHNEIDER_CATALOG_MASTER.md
  - SCHNEIDER_LC1D_WORK.md
- ✅ No scope ambiguity

---

## 12. Completion Declaration

When done, fill this:

> **Status:** ✅ Complete  
> **FINAL CSV Imported Successfully**  
> **No pending issues for LC1D**

---

## 13. Next Family Pointer

Next family to process:
- **LC1K** — TeSys K Power Contactors (AC control references)

---

**Document Lifecycle**
- Active during execution
- Read-only after completion
- Archived once Schneider track is complete

