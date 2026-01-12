# SCHNEIDER CATALOG MASTER  
## Catalog Conversion & Import Tracker (Pre-Phase-5)

**Status:** ACTIVE  
**Purpose:** Single control-plane document to track Schneider catalog completion in NSW canonical format.  
**Scope:** Schneider Electric (all product families)  
**Relation to Phase-5:** INPUT ASSET ONLY (Phase-5 execution paused intentionally)

---

## 1. What This Document Is (and Is Not)

### IS
- A **status tracker** for Schneider catalog conversion
- A **reference index** for FINAL CSVs and profile versions
- The **single source of truth** for "what is done vs pending" for Schneider

### IS NOT
- A step-by-step how-to (see SOP instead)
- A place for profile tuning notes
- A Phase-5 execution document

---

## 2. Canonical References

- **General SOP:**  
  `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md`

- **Tooling Root:**  
  `tools/catalog_pipeline/`

- **Import API:**  
  `POST /api/v1/catalog/skus/import`

- **Dev API Port:**  
  `8011` (NSW Estimation – local/dev)

---

## 3. Schneider Product Family Tracker

| Family Code | Family Name | Profile | FINAL CSV | SKUs | Imported | Status | Notes |
|-----------|------------|---------|-----------|------|----------|--------|------|
| LC1E | Easy TeSys Power Contactors | schneider_contactors_v1.yml | ✔ FINAL_2025-12-26 | 29 | ✔ | ✅ Complete | All expected 3P SKUs extracted (29/29); includes LC1E630 (see LC1E_MISSING_SKUS_ANALYSIS.md) |
| LP1K | TeSys K Control Relays | schneider_lp1k_v1.yml | ✔ FINAL_2025-12-26 | 6 | ✔ | ✅ Complete | DC control only; AC refs handled under LC1K |
| LC1D | TeSys Deca Power Contactors | — | — | — | — | ⏳ Pending | — |
| GV | Motor Protection / MPCB | — | — | — | — | ⏳ Pending | — |
| EOCR | Electronic Overload Relays | — | — | — | ⏳ Pending | — |
| ACC | Accessories | — | — | — | — | 📋 Deferred | See SCHNEIDER_ACCESSORIES_PLAN.md |

**Legend**
- ⏳ Pending – not started
- ⚙ In Progress – profile/TEST ongoing
- ✅ FINAL Ready – FINAL CSV generated, ready for import
- ✅ Complete – FINAL imported successfully
- 📋 Deferred – planned for later (see SCHNEIDER_ACCESSORIES_PLAN.md)

---

## 4. Completed Family Summary

### 4.1 LC1E – Easy TeSys Power Contactors

- **Profile:** `schneider_lc1e_v1.yml`
- **FINAL CSV:**  
  `tools/catalog_pipeline/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv`
- **SKUs Extracted:** 29 (all expected 3P SKUs)
- **Large Frame SKUs Extracted:** LC1E120, LC1E200, LC1E300, LC1E500, LC1E50, LC1E630
- **Coverage:** 100% of expected 3P SKUs (29/29)
- **CatalogItem Created:**  
  `SCHNEIDER__EASY_TESYS_POWER_CONTACTORS_LC1E_3P`
- **Import Mode:** FINAL (ready for re-import with updated CSV)
- **Verification:** Passed (prices, archive, snapshot) for extracted SKUs
- **Fixes Applied (2025-12-26):** 
  1. Section marker fix (CRITICAL) - FRAME rows with SKU data now processed
  2. Price fallback logic enhanced - handles position 9 for large frames
  3. Series detection improved - SKU prefix inference for large frames
  4. **Multi-space cell splitting** - handles merged Excel cells (enabled LC1E630 extraction)
- **Reference:** See `LC1E_MISSING_SKUS_ANALYSIS.md` for detailed analysis and fixes applied

This family serves as the **reference baseline** for all subsequent Schneider families.

**Note (2025-12-26):** ✅ **FULLY FIXED** - All expected 3P SKUs now extracted. Improvement: 23 → 29 SKUs (+6 large frames including LC1E630). All fixes verified and working.

### 4.2 LP1K – TeSys K Control Relays

- **Profile:** `schneider_lp1k_v1.yml`
- **FINAL CSV:**  
  `tools/catalog_pipeline/output/final/schneider_Schneider_LP1K_FINAL_2025-12-26_normalized_20251226_130950.csv`
- **SKUs Imported:** 6
- **CatalogItem Created:** 1 (TeSys K Control Relays (LP1K))
- **Import Mode:** FINAL
- **Batch ID:** `870e813a-e17e-4cc1-92a8-5e7848d8a48f`
- **Price Rows Inserted:** 6
- **Scope:** DC control SKUs only (LP1K prefix). AC control references (LC1K) handled separately under LC1K family.
- **Verification:** All 6 LP1K SKUs from source file captured and imported successfully
- **Status:** ✅ Complete — Scope locked. LP1K DC control SKUs fully extracted and imported. AC control references intentionally excluded and will be processed under LC1K.

---

## 5. Rules for Updating This Tracker

1. One row per product family
2. Only update:
   - Profile name
   - FINAL CSV reference
   - SKU count
   - Import status
3. Do NOT include:
   - Column quirks
   - Profile tuning notes
   - Debug details  
   (These belong in per-family WORK files)

---

## 6. Relationship to Per-Family WORK Files

Each family listed above must have a corresponding execution file:

docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/
├── SCHNEIDER_LC1E_WORK.md
├── SCHNEIDER_LP1K_WORK.md
├── SCHNEIDER_LC1D_WORK.md
├── SCHNEIDER_ACCESSORIES_PLAN.md
└── …

These WORK files:
- Capture operational details
- Are temporary during derivation
- Feed improvements back into the SOP

---

## 7. Exit Criteria for Schneider Track

Schneider catalog work is considered **complete** when:

- All target families are marked ✅ Complete
- Each family has:
  - FINAL CSV
  - Versioned profile
  - Successful import record
- No further Schneider-specific rule changes are pending

Only after this point do we **resume Phase-5 execution**.

---

## 8. Phase-5 Resume Marker (Locked)

When Schneider catalog completion is done, the **first Phase-5 task** will be:

> Catalog-driven BOM → multi-SKU → quotation line mapping  
> (using full Schneider catalog as test dataset)

This document will then be marked **FROZEN**.

---

**Document Control**
- Changes allowed: Status updates only
- Structural changes require SOP update
- Owner: Catalog Pipeline Track

