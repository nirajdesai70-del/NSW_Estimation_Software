# SCHNEIDER LP1K — WORK FILE
## Catalog Conversion Execution Notes

**Family Code:** LP1K  
**Family Name:** TeSys K Control Relays  
**OEM:** Schneider Electric  
**Status:** ✅ Complete  
**Profile:** schneider_lp1k_v1.yml  
**Started On:** 2025-12-26  
**Completed On:** 2025-12-26

---

## 1. Purpose of This File

This document captures **family-specific execution details** while converting the Schneider LP1K catalog into NSW canonical CSV format.

It exists to:
- Record **data quirks and exceptions**
- Track **profile tuning decisions**
- Document **why rules were adjusted**
- Support **SOP derivation**

⚠️ This file is **not canonical**. Once the SOP stabilizes, this becomes reference-only.

---

## 2. Source Artifacts

### 2.1 Original Sources
- **XLSX Source:**  
  `tools/catalog_pipeline/input/raw/schneider/master/Switching _Pricelist_WEF 15th Jul 25.xlsx`
- **WEF / Revision Date:** 15th July 2025
- **Pages Covered:** TeSys K Control Relays section (DC control reference LP1K)

### 2.2 XLSX Conversion
- **Converted XLSX:**  
  `tools/catalog_pipeline/input/raw/schneider/master/Switching _Pricelist_WEF 15th Jul 25.xlsx`
- **Conversion Tool Used:** Standard PDF-to-XLSX converter
- **Manual Cleanup Performed:**  
  - [x] Removed headers/footers  
  - [x] Merged split tables  
  - [x] Other: Master source file stored in master/ directory

---

## 3. Profile Configuration

### 3.1 Profile File
- `tools/catalog_pipeline/profiles/schneider/schneider_lp1k_v1.yml`

### 3.2 Key Profile Decisions
- **Column Mapping:**  
  - SKU column index: 6 (DC Control Reference column, after collapsing)  
  - Price column index: 7 (BD 24V price column; fallback to FD/MD if empty)  
- **Series Detection:**  
  - Heading-based: Yes (primary method)  
  - Prefix-based fallback: Yes (LP1K prefix mapping)
- **Scope Filter:**  
  - Applied: Yes  
  - Pattern(s): `"TeSys K Control Relays (LP1K)"` (DC control only)
- **Strategy:** Extract only DC control SKUs (LP1K...). AC control SKUs (LC1K...) handled separately.

---

## 4. TEST Normalization Notes

### 4.1 TEST Runs
| Run | Date | Rows Output | Issues Found | Action Taken |
|----|------|-------------|--------------|--------------|
| T1 | 2025-12-26 | 6 | Initial extraction successful | Profile tuning for column mapping |
| Final | 2025-12-26 | 6 | None | Ready for FINAL |

### 4.2 Common Issues Observed
- SKU format: Consistent LP1K prefix pattern (LP1K0601, LP1K0610, etc.)
- Price formatting: BD/24V prices extracted correctly (fallback to FD/MD if needed)
- Header noise: Successfully filtered out AC control references (LC1K) and section headers

### 4.3 Coverage Verification
- **Total LP1K SKUs present in source:** 6
- **All 6 extracted and priced:** ✅
- **Coverage limitation:** Source does not list additional LP1K SKUs; remaining candidate SKUs belong to other families (LC1E/LC1K/etc.)

---

## 5. FINAL Freeze

### 5.1 FINAL Source
- **FINAL XLSX:**  
  `tools/catalog_pipeline/input/final/schneider/lp1k/Schneider_LP1K_FINAL_2025-12-26.xlsx`

### 5.2 FINAL Output
- **FINAL CSV:**  
  `tools/catalog_pipeline/output/final/schneider_Schneider_LP1K_FINAL_2025-12-26_normalized_20251226_130950.csv`
- **Profile Version:** `v1`
- **Rows Output:** 6

⚠️ FINAL artifacts are **immutable**.

### 5.3 Final Notes
- LP1K DC control SKUs — fully extracted (6 SKUs)
- AC control references (LC1K) handled separately under LC1K family
- Pricing selection: BD/24V first, with fallback to FD/MD if needed

---

## 6. Import Verification

### 6.1 Dry-Run
- Result: ✅ Pass
- Batch ID: `c677448f-b935-41f8-a799-4429bc772dab`
- Rows Valid: 6
- Rows Error: 0
- Errors (if any): None

### 6.2 Commit Import
- **Batch ID:** `870e813a-e17e-4cc1-92a8-5e7848d8a48f`
- **CatalogItem Created:** 1 (TeSys K Control Relays (LP1K))
- **SKUs Imported:** 6
- **Price Rows Inserted:** 6
- **Price List ID:** 2
- **Price List Name:** Schneider - schneider_Schneider_LP1K_FINAL_2025-12-26_normalized_20251226_130950.csv

---

## 7. Exceptions & Decisions

### 7.1 Scope Decisions
- **DC control only:** Profile extracts only LP1K (DC control) SKUs. AC control SKUs (LC1K prefix) are excluded and will be handled under separate LC1K family profile.
- **Accessories excluded:** Auxiliary contacts (LAD, LA, LB, etc.), coils, and mounting kits are not included. These will be handled as separate accessory families per `SCHNEIDER_ACCESSORIES_PLAN.md`.

### 7.2 Pricing Strategy
- **BD/24V priority:** Profile selects BD (24V DC) prices first, with fallback to FD (110V) or MD (220V) if BD is empty.
- **Price extraction:** Uses `scan_forward_from_sku_raw` to find prices in adjacent columns.

### 7.3 SKU Validation
- **Prefix-based:** Only SKUs starting with "LP1K" are extracted.
- **Pattern:** LP1K#### format (e.g., LP1K0601, LP1K0610).

---

## 8. SOP Feedback (Important)

List **generalizable learnings** that should feed back into the SOP:

- [ ] New ignore rule discovered
- [ ] Better series detection pattern
- [ ] Column-shift heuristic needed
- [ ] Validation rule refinement

> These items must be reviewed when updating  
> `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md`

---

## 9. Completion Declaration

> **Status:** ✅ Complete  
> **FINAL CSV:** Ready for import (6 SKUs extracted)  
> **Coverage:** All LP1K DC control SKUs from source file captured  
> **No pending issues for LP1K main series**  
> **Note:** Accessories deferred per `SCHNEIDER_ACCESSORIES_PLAN.md`

### 🔒 LP1K Scope — OFFICIALLY CLOSED

**Declaration (Locked):**

LP1K DC control SKUs — fully extracted; AC references handled under LC1K

**What this means (no ambiguity going forward):**
- ✅ LP1K family is COMPLETE
- Scope: DC control relays only
- SKUs extracted: 6
- Pricing verified and correct
- ❌ AC control references (LC1K…) are explicitly OUT OF SCOPE
- They will be handled under a separate LC1K family
- No overlap, no reprocessing, no mixed logic

**This is the right engineering decision, not a compromise.**

> LP1K DC control SKUs fully extracted. AC control references intentionally excluded and will be processed under LC1K.

---

## 10. Next Family Pointer

Next family to process:
- **LC1D** — TeSys Deca Power Contactors

---

**Document Lifecycle**
- Active during execution
- Read-only after completion
- Archived once Schneider track is complete

