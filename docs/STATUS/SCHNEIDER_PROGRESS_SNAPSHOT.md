# Schneider Catalog Progress Snapshot

**Last Updated:** 2025-12-26  
**Status:** IN PROGRESS (1 of 6 families complete)  
**Purpose:** Track Schneider catalog conversion progress and identify next execution point.

---

## 1. Source Material Overview

### 1.1 Primary Source
- **File:** `Switching _Pricelist_WEF 15th Jul 25.xlsx`
- **WEF Date:** 15th July 2025
- **Location:** `tools/catalog_pipeline/input/raw/schneider/lc1e/`
- **Content:** Multiple Schneider product families in single XLSX

### 1.2 Families Identified
Based on source file structure and profile mappings:

1. ✅ **LC1E** — Easy TeSys Power Contactors (3P) — **COMPLETE**
2. ⏳ **LP1K** — TeSys K Control Relays — **PENDING**
3. ⏳ **LC1D** — TeSys Deca Power Contactors — **PENDING**
4. ⏳ **GV** — Motor Protection / MPCB — **PENDING**
5. ⏳ **EOCR** — Electronic Overload Relays — **PENDING**
6. ⏳ **ACC** — Accessories (aux contacts, coils, etc.) — **PENDING** (optional)

---

## 2. Completed Family: LC1E

### 2.1 Profile
- **File:** `tools/catalog_pipeline/profiles/schneider/schneider_lc1e_v1.yml`
- **Version:** v1 (FROZEN)
- **Scope:** LC1E 3P contactors only

### 2.2 FINAL Artifacts
- **FINAL XLSX:**  
  `tools/catalog_pipeline/input/final/schneider/lc1e/Schneider_LC1E_Contactors_FINAL_2025-12-26.xlsx`
- **FINAL CSV:**  
  `tools/catalog_pipeline/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv`

### 2.3 Import Results
- **SKUs Imported:** 23
- **CatalogItem:** `SCHNEIDER__EASY_TESYS_POWER_CONTACTORS_LC1E_3P`
- **Import Date:** 2025-12-26
- **Status:** ✅ Verified and operational

### 2.4 Reference Documents
- **WORK File:** `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/SCHNEIDER_LC1E_WORK.md`
- **Milestone:** `docs/MILESTONES/M01_CATALOG_LC1E_DONE.md`

---

## 3. Pending Families

### 3.1 LP1K — TeSys K Control Relays
- **Status:** ⏳ Pending
- **Priority:** HIGH (next target)
- **Source:** Same XLSX file, different section
- **Profile Needed:** `schneider_lp1k_v1.yml`
- **Estimated SKUs:** TBD (to be determined during TEST)

### 3.2 LC1D — TeSys Deca Power Contactors
- **Status:** ⏳ Pending
- **Priority:** MEDIUM
- **Source:** Same XLSX file
- **Profile Needed:** `schneider_lc1d_v1.yml`

### 3.3 GV — Motor Protection / MPCB
- **Status:** ⏳ Pending
- **Priority:** MEDIUM
- **Source:** Same XLSX file
- **Profile Needed:** `schneider_gv_v1.yml`

### 3.4 EOCR — Electronic Overload Relays
- **Status:** ⏳ Pending
- **Priority:** LOW
- **Source:** Same XLSX file
- **Profile Needed:** `schneider_eocr_v1.yml`

### 3.5 ACC — Accessories
- **Status:** ⏳ Pending
- **Priority:** LOW (optional)
- **Source:** Same XLSX file (may be inline with other families)
- **Profile Needed:** `schneider_acc_v1.yml` (if handled separately)

---

## 4. Next Execution Point

### 4.1 Recommended Next Family
**LP1K (TeSys K Control Relays)**

**Rationale:**
- Next logical family in Schneider product hierarchy
- Profile template exists (from LC1E)
- Similar structure expected (can reuse column mapping patterns)

### 4.2 Execution Steps (High-Level)

1. **Create WORK File:**
   - Copy template: `SCHNEIDER_<FAMILY>_WORK.md`
   - Rename to: `SCHNEIDER_LP1K_WORK.md`
   - Fill in family-specific details

2. **Create Profile:**
   - Copy `schneider_lc1e_v1.yml` as starting point
   - Create `schneider_lp1k_v1.yml`
   - Adjust:
     - Series detection patterns
     - Scope filter (LP1K only)
     - Column mappings (if different)

3. **TEST Normalization:**
   - Copy source XLSX to `input/test/schneider/lp1k/`
   - Run: `python normalize.py --profile profiles/schneider/schneider_lp1k_v1.yml --file input/test/schneider/lp1k/<file>.xlsx --mode test`
   - Iterate until PASS criteria met

4. **FINAL Freeze:**
   - Copy XLSX to `input/final/schneider/lp1k/`
   - Rename: `Schneider_LP1K_FINAL_<YYYY-MM-DD>.xlsx`
   - Run FINAL normalization

5. **Import:**
   - Dry-run: `POST /api/v1/catalog/skus/import?dry_run=true`
   - Commit: `POST /api/v1/catalog/skus/import?dry_run=false`

6. **Update Tracker:**
   - Update `SCHNEIDER_CATALOG_MASTER.md`
   - Mark LP1K as ✅ Complete

---

## 5. Source File Structure Notes

### 5.1 Multi-Family XLSX
The source XLSX contains multiple families. Each family will:
- Use its own profile (with scope filter)
- Produce its own FINAL CSV
- Be imported separately

### 5.2 Reusing Source
- Same source XLSX can be used for all families
- Each family extracts only its section via scope filter
- No need to split XLSX manually

---

## 6. Progress Metrics

| Family | Status | SKUs | Profile | FINAL CSV | Imported |
|--------|--------|------|---------|-----------|----------|
| LC1E | ✅ Complete | 23 | v1 | ✅ | ✅ |
| LP1K | ⏳ Pending | — | — | — | — |
| LC1D | ⏳ Pending | — | — | — | — |
| GV | ⏳ Pending | — | — | — | — |
| EOCR | ⏳ Pending | — | — | — | — |
| ACC | ⏳ Pending | — | — | — | — |

**Overall Progress:** 1/6 families (16.7%)

---

## 7. Blockers / Dependencies

- None identified. Ready to proceed with LP1K.

---

**Next Action:** Create `SCHNEIDER_LP1K_WORK.md` and begin profile derivation.

