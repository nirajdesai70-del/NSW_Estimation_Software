# Archive Plan v1.0 → v1.1 Diff Summary

**Date:** 2025-01-XX  
**Purpose:** Document changes from v1.0 to v1.1  
**Status:** FINAL - FROZEN

---

## 📄 Document IDs (Canonical Filenames)

**Canonical Documents:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` (canonical)
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` (canonical)
- `ARCHIVE_PLAN_v1.0_TO_v1.1_DIFF.md` (this file)

**Location:** `tools/catalog_pipeline_v2/` (root) → will move to `sku_price_pack/.../freeze_docs/`

---

## ✅ Summary

**Status:** ✅ APPROVED with 5 patches applied

**Result:** v1.1 is **FINAL - FROZEN** and ready for execution.

---

## 🔧 Patches Applied

### Patch 1: Clarify NSW_L2_PRODUCTS Status

**Changed:**
- ❌ OLD: "NSW_L2_PRODUCTS → migrate to SKU master"
- ✅ NEW: "NSW_L2_PRODUCTS is legacy parse/compat output. Authoritative SKU list is NSW_SKU_MASTER_CANONICAL."

**Impact:** Prevents accidental future edits in wrong sheet.

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Sections 2.1, 4.1, 5.1
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - Multiple sections

---

### Patch 2: Update "Not yet generated" Statements

**Changed:**
- ❌ OLD: "NSW_SKU_RATINGS not yet generated"
- ❌ OLD: "NSW_CATALOG_CHAIN_MASTER not yet generated"
- ❌ OLD: "Dictionary sheets not generated"
- ✅ NEW: "Already generated and active/reference-active/locked"

**Impact:** Keeps documentation truthful and avoids doubt.

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Sections 1.2, 2.1, 4.2
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - Multiple sections

---

### Patch 3: Catalog Chain - Remove Ambiguity

**Changed:**
- ❌ OLD: "Decision required: Clarify relationship between NSW_L1_CONFIG_LINES and NSW_CATALOG_CHAIN_MASTER"
- ✅ NEW: "Decision CLOSED: NSW_CATALOG_CHAIN_MASTER is canonical. NSW_L1_CONFIG_LINES is legacy parse output (archive after QC)."

**Impact:** Prevents reopening debate, clarifies canonical vs legacy.

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Section 11 (new Decision Log section)
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - Key Decisions section

---

### Patch 4: Migration Script - Split Responsibility

**Changed:**
- ❌ OLD: Single script `migrate_to_freeze_structure.py`
- ✅ NEW: Two scripts:
  - Script A: `migrate_sku_price_pack.py` (migrate SKU + price + ratings + accessories)
  - Script B: `build_catalog_chain_master.py` (rebuild catalog chain from canonical)

**Impact:** Reduces risk, reflects real dependencies (migration vs rebuild).

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Section 5 (completely rewritten)
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - Two Migration Scripts section

---

### Patch 5: Add Explicit Scope Lock

**Changed:**
- ❌ OLD: No explicit scope statement
- ✅ NEW: Added "SCOPE LOCK" section at top:
  - "This migration applies only to the SKU + Price Creation Pack."
  - "It does NOT implement estimation runtime logic (feature explosion, BOM, quotation rules)."

**Impact:** Prevents future scope creep.

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - New section at top
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - New section at top

---

## 📁 Additional Changes

### Folder Structure Update

**Changed:**
- ❌ OLD: Separate `canonical/` and `nsw_master/` folders
- ✅ NEW: Single `sku_price_pack/` folder with:
  - `NSW_SKU_PRICE_PACK_MASTER.xlsx` (single authoritative workbook)
  - `freeze_docs/` subfolder
  - `qc/` subfolder

**Impact:** Prevents confusion between "canonical outputs" and "master workbook".

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Section 4.1
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - New File Structure section

---

### Freeze Gate Checklist Added

**Changed:**
- ❌ OLD: Basic archive checklist
- ✅ NEW: Comprehensive "Freeze Gate" checklist (mandatory before archiving):
  - Price QC count stable
  - SKU master completeness check passes
  - Chain master validated
  - Freeze docs v1.1 committed
  - Sheet index v1.1 aligns
  - Migration scripts tested
  - Data integrity verified

**Acceptance Criteria:**
- **Freeze gate is PASSED only when every checkbox is ✅ and evidence links are recorded in `qc/`**

**Impact:** Ensures quality gates before archiving and makes gate enforceable.

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Section 3.2 (completely rewritten)
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - Freeze Gate Checklist section

---

### Migration vs Rework Clarification

**Changed:**
- ❌ OLD: "Canonical extraction output → NSW_CATALOG_CHAIN_MASTER (restructure)"
- ✅ NEW: Explicitly states:
  - ✅ Can be migrated: SKU, Price, Ratings, Accessories, Source lineage
  - ⚠️ Needs rework: Catalog Chain Master (must be rebuilt, not migrated)
  - Reason: L0/L1 naming rules corrected (no OEM series at L0/L1; **Option B: coil voltage is SKU-defining and kept at L2; not part of L1 generic identity**)

**Impact:** Clear separation of migration vs rebuild.

**Files Changed:**
- `ARCHIVE_AND_MIGRATION_PLAN_v1.1.md` - Sections 2.1, 2.2
- `ARCHIVE_QUICK_REFERENCE_v1.1.md` - What Can Be Migrated section

---

## 📊 Summary of Changes

| Category | v1.0 | v1.1 | Impact |
|----------|------|------|--------|
| NSW_L2_PRODUCTS status | Implied active | Explicitly legacy/compat | Prevents wrong edits |
| Sheet generation status | "Not yet generated" | "Already generated" | Truthful documentation |
| Catalog Chain decision | "Decision required" | "Decision CLOSED" | Prevents debate |
| Migration scripts | Single script | Two scripts (A + B) | Reduces risk |
| Scope lock | Implicit | Explicit | Prevents scope creep |
| Folder structure | Separate folders | Single `sku_price_pack/` | Prevents confusion |
| Freeze gate | Basic checklist | Comprehensive gate | Quality assurance |

---

## ✅ Validation

**All patches applied successfully:**
- ✅ Patch 1: NSW_L2_PRODUCTS status clarified
- ✅ Patch 2: "Not yet generated" statements updated
- ✅ Patch 3: Catalog Chain decision closed
- ✅ Patch 4: Migration scripts split (A + B)
- ✅ Patch 5: Scope lock added

**Additional improvements:**
- ✅ Folder structure updated
- ✅ Freeze gate checklist added
- ✅ Migration vs rework clarified

---

## 🎯 Next Steps

1. ✅ **v1.1 documents created** - Ready for review
2. ⚠️ **Final review** - Verify all patches applied correctly
3. ⚠️ **Commit to freeze_docs/** - After approval
4. ⚠️ **Create migration scripts** - Script A and Script B
5. ⚠️ **Execute migration** - After freeze gate passes

---

**Status:** ✅ DIFF COMPLETE - v1.1 READY FOR EXECUTION

