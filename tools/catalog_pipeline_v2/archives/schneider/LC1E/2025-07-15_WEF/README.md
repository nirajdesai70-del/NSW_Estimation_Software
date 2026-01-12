# LC1E Series - Frozen Archive (2025-07-15 WEF)

**Archive Date**: 2026-01-03  
**Status**: ✅ **FROZEN - CANONICAL**  
**Governance Approval**: ✅ **APPROVED — READY TO FREEZE**

---

## ⚠️ IMPORTANT: DO NOT USE ARCHIVED FILES

**Pre-v1.2 CLEAN LC1E outputs are archived here for historical reference only.**

**Canonical source (USE THIS):**
```
active/schneider/LC1E/02_outputs/NSW_LC1E_WEF_2025-07-15_v1.xlsx
```

This is the **single source of truth** for LC1E catalog data under NSW v1.2 CLEAN rules.

---

## Archive Contents

This archive contains:
- Pre-v1.2 CLEAN LC1E outputs (historical reference)
- Old validation reports
- Legacy format workbooks

**These files are NOT compliant with v1.2 CLEAN rules and should NOT be used for new work.**

---

## Canonical Freeze Artifact

**File**: `NSW_LC1E_WEF_2025-07-15_v1.xlsx`  
**Location**: `active/schneider/LC1E/02_outputs/`  
**Status**: ✅ **FROZEN - CANONICAL**

**Compliance**:
- ✅ NSW v1.2 CLEAN compliant
- ✅ SC_Lx structural-only (no duty/coil/rating tokens)
- ✅ Generic naming series-neutral (L1 descriptors)
- ✅ Layer discipline respected (L0/L1/L2 boundaries)
- ✅ Sheet set matches v1.2 CLEAN intent

**Governance Review**: Approved 2026-01-03  
**QC Summary**: `active/schneider/LC1E/03_qc/QC_SUMMARY.md`

---

## What Changed (v1.2 CLEAN Adoption)

**Replacement Strategy**: This release **replaces** all previous LC1E outputs. No alignment or migration with old files is required.

**Key Changes**:
1. Generic descriptors are series-neutral (removed "LC1E" from L1 generic_descriptor)
2. SC_Lx contains only structural identifiers
3. NSW format workbook structure (not legacy engineer review format)
4. Full series extraction (not Page-8 only)

**Historical Note**: Previous Page-8 golden vs rebuilt validation (Dec 2025) showed mismatches. This is expected and not a gating requirement, as this release adopts the new v1.2 CLEAN pipeline as canonical replacement.

---

## Archive Structure

```
archives/schneider/LC1E/2025-07-15_WEF/
├── 00_inputs/          # Historical input files
├── 01_scripts/         # Scripts used for this freeze
├── 02_outputs/         # Pre-v1.2 outputs (archived)
├── 03_qc/              # Historical QC reports
├── 04_docs/            # Documentation
├── 05_decisions/       # Governance decisions
└── README.md           # This file
```

---

## Freeze Declaration

**Effective Date**: 2026-01-03  
**Frozen By**: ChatGPT Governance Review  
**Freeze Status**: ✅ **ACTIVE**

This LC1E catalog output is now the **canonical baseline** for all future work.

**No modifications** to the frozen file are permitted without:
1. New governance review
2. Version increment (v1 → v2)
3. New freeze declaration

---

## References

- **NSW v1.2 CLEAN Rules**: `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md`
- **Sheet Set Index**: `NSW_SHEET_SET_INDEX_v1.2_CLEAN.md`
- **QC Summary**: `active/schneider/LC1E/03_qc/QC_SUMMARY.md`
- **Governance Review**: `active/schneider/LC1E/03_qc/STEP_7_GOVERNANCE_REVIEW_PROMPT.md`

---

**Archive Maintained By**: Cursor (Automated)  
**Last Updated**: 2026-01-03
