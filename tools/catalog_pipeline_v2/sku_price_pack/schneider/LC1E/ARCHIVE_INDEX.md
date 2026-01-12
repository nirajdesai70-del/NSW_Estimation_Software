# Archive Index - PRE_FREEZE_ARCHIVE

**Date:** 2025-01-XX  
**Status:** ARCHIVE INDEX  
**Purpose:** Catalog of all files archived in PRE_FREEZE_ARCHIVE

---

## Archive Location

**Path:** `archives/schneider/LC1E/2025-07-15_WEF/PRE_FREEZE_ARCHIVE/`

---

## Archive Categories

### 00_legacy_outputs/

**Purpose:** Old format outputs (before freeze)

**Files:**
- `NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx` - Legacy engineer review workbook
- `LC1E_ENGINEER_REVIEW_v1.xlsx` - Legacy LC1E engineer review
- `LC1E_CANONICAL_v1.xlsx` - Legacy canonical format (if different structure)

**Reason:** Old format, replaced by new freeze structure

**Archive Date:** _TBD_

---

### 01_temporary_files/

**Purpose:** Temp files (can regenerate)

**Files:**
- `LC1E_L1_tmp.xlsx` - Temporary L1 intermediate file
- `LC1E_L2_tmp.xlsx` - Temporary L2 intermediate file
- `l1_tmp.xlsx` - Temporary L1 file
- `l2_tmp.xlsx` - Temporary L2 file

**Reason:** Temporary intermediate files, can be regenerated from canonical

**Archive Date:** _TBD_

---

### 02_rebuild_tests/

**Purpose:** Rebuild test files

**Files:**
- (14 files from `rebuild_check/` directory)
  - `LC1E_CANONICAL_FINAL.xlsx`
  - `LC1E_CANONICAL_fixed.xlsx`
  - `LC1E_CANONICAL_IMPROVED.xlsx`
  - `LC1E_CANONICAL_rebuild.xlsx`
  - `LC1E_L1_rebuild.xlsx`
  - `LC1E_L2_rebuild.xlsx`
  - `NSW_LC1E_WEF_2025-07-15_COMPLETE.xlsx`
  - `NSW_LC1E_WEF_2025-07-15_FIXED.xlsx`
  - `NSW_LC1E_WEF_2025-07-15_rebuild_FINAL.xlsx`
  - `NSW_LC1E_WEF_2025-07-15_rebuild_v2.xlsx`
  - `NSW_LC1E_WEF_2025-07-15_rebuild.xlsx`
  - `NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW_rebuild.xlsx`
  - `VALIDATION_IMPROVED.txt`
  - `VALIDATION_REPORT.txt`

**Reason:** Test/rebuild attempts, not needed for production

**Archive Date:** _TBD_

---

### 03_legacy_scripts/

**Purpose:** Old scripts (reference only)

**Files:**
- `build_l2_from_canonical.py` - Old version (superseded)
- `derive_l1_from_l2.py` - Old version (superseded)
- `build_master_workbook.py` - Old version (superseded)

**Reason:** Superseded by new scripts, keep for reference

**Archive Date:** _TBD_

---

### 04_documentation/

**Purpose:** Pre-freeze documentation

**Files:**
- (Existing documentation from `04_docs/`)
- Migration notes (to be added)

**Reason:** Historical reference

**Archive Date:** _TBD_

---

## Archive Summary

| Category | File Count | Total Size | Status |
|----------|------------|------------|--------|
| 00_legacy_outputs/ | _TBD_ | _TBD_ | ⬜ PENDING |
| 01_temporary_files/ | _TBD_ | _TBD_ | ⬜ PENDING |
| 02_rebuild_tests/ | 14 | _TBD_ | ⬜ PENDING |
| 03_legacy_scripts/ | 3 | _TBD_ | ⬜ PENDING |
| 04_documentation/ | _TBD_ | _TBD_ | ⬜ PENDING |

---

## Archive Process

**Pre-Archive Checklist:**
- [ ] Freeze gate checklist passed (all items ✅)
- [ ] All evidence files saved in `qc/QC_EXPORTS/`
- [ ] Migration scripts tested and validated
- [ ] New master workbook created and validated

**Archive Actions:**
- [ ] Create `PRE_FREEZE_ARCHIVE/` directory structure
- [ ] Move files to appropriate archive categories
- [ ] Update this index with file counts and dates
- [ ] Create archive manifest (optional)

---

## Notes

- All archived files are **reference-only** - not deleted
- Archive structure allows easy retrieval if needed
- Archive index should be updated as files are moved

---

**Last Updated:** 2025-01-XX


