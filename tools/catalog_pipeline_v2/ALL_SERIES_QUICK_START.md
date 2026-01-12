# All Series Processing - Quick Start Guide

**Date:** 2026-01-03  
**Reference:** `ALL_SERIES_PROCESSING_PLAN.md` (detailed plan)  
**Source File (Normalized):** `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`  
**Location:** `tools/catalog_pipeline_v2/input/reviseditemmaster/`

**Note:** Use the normalized file (same data, cleaned/aligned structure) instead of TESYS_PROTECT_ITEM_FULL_WORK.xlsx

---

## 📊 Series Summary

| Series | Items | Source Sheet | Priority | Complexity |
|--------|-------|--------------|----------|------------|
| ✅ LC1E | 165 | Master View | ✅ Done | Low |
| ⏳ LC1D | 332 | Master View | 🔥 High | Low (similar to LC1E) |
| ⏳ GIG | 40 | GIGA_SERIES_WORK | 🔥 High | Low |
| ⏳ CAPACITOR_DUTY | 13 | CAPACITOR_DUTY_WORK | 🔥 High | Low |
| ⏳ LC1K | 83 | K_SERIES_WORK | 🟡 Medium | Medium (mixed types) |
| ⏳ EOCR | 44 | EOCR_WORK | 🟡 Medium | Medium (different type) |
| ⏳ PROTECT | 22 | PROTECT_WORK | 🟡 Medium | Medium (overlaps) |
| ⏳ ACCESSORIES | 158 | ACCESSORIES_MASTER | 🟢 Low | High (special structure) |
| ⏳ COMPATIBILITY | 169 | ACCESSORY_COMPATIBILITY | 🟢 Low | Low (reference data) |

**Total:** 1,026 items  
**Completed:** 165 (16%)  
**Remaining:** 861 (84%)

---

## 🚀 Recommended Execution Order

### Phase 1: Quick Wins (Similar to LC1E)
1. **LC1D** (332 items) - Extract from master, reuse LC1E patterns
2. **GIG** (40 items) - Similar structure
3. **CAPACITOR_DUTY** (13 items) - Small, straightforward

### Phase 2: Analysis Required
4. **LC1K** (83 items) - Mixed product types
5. **EOCR** (44 items) - Different product type
6. **PROTECT** (22 items) - Overlap resolution

### Phase 3: Special Cases
7. **ACCESSORIES** (158 items) - Different structure
8. **COMPATIBILITY** (169 mappings) - Reference data

---

## 📋 What Needs to Be Done

### For Each Series:

1. **Extract Data** from source file
   - Create extraction script
   - Output: `{SERIES}_CANONICAL_v1.xlsx`

2. **Build L2** (SKU layer)
   - Identity + SKU codes
   - Output: `{SERIES}_L2_tmp.xlsx`

3. **Derive L1** (Configuration layer)
   - Duty × Voltage × Attributes
   - Output: `{SERIES}_L1_tmp.xlsx`

4. **Generate NSW Workbook**
   - Final Phase 5 format
   - Output: `NSW_{SERIES}_WEF_2025-07-15_v1.xlsx`

5. **QC Validation**
   - All gates (A through I)
   - Output: `QC_SUMMARY.md`

6. **Governance Review**
   - ChatGPT approval
   - Output: Approval status

7. **Archive**
   - Move to archives folder
   - Mark as complete

---

## 🎯 Expected Outputs

### Per Series:
- ✅ `NSW_{SERIES}_WEF_2025-07-15_v1.xlsx` (Primary freeze artifact)
- ✅ `{SERIES}_CANONICAL_v1.xlsx` (Intermediate)
- ✅ `{SERIES}_L2_tmp.xlsx` (Intermediate)
- ✅ `{SERIES}_L1_tmp.xlsx` (Intermediate)
- ✅ `QC_SUMMARY.md` (Validation)
- ✅ `ALIGNMENT_PACKAGE_SUMMARY.md` (Documentation)

### Overall:
- ✅ 8 NSW format workbooks (one per series)
- ✅ Complete catalog coverage
- ✅ All validation gates passed
- ✅ All series approved and archived

---

## 🛠️ How to Do It

### Step 1: Start with LC1D

```bash
# 1. Create LC1D folder structure
mkdir -p active/schneider/LC1D/{00_inputs,01_scripts,02_outputs,03_qc,04_docs}

# 2. Extract LC1D from normalized master view
python scripts/extract_lc1d_from_master.py \
  --input tools/catalog_pipeline_v2/input/reviseditemmaster/ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx \
  --sheet NSW_ITEM_MASTER_ENGINEER_VIEW \
  --filter "series_code == 'LC1D'" \
  --out active/schneider/LC1D/00_inputs/LC1D_CANONICAL_v1.xlsx

# 3. Follow LC1E pipeline steps 2-5
# (Reuse LC1E scripts, adapt for LC1D)
```

### Step 2: Reuse LC1E Patterns

For LC1D, GIG, CAPACITOR_DUTY:
- Copy LC1E extraction script
- Modify series-specific logic
- Follow same 8-step process

### Step 3: Adapt for Special Cases

For LC1K, EOCR, PROTECT, ACCESSORIES:
- Analyze attribute structure
- Adapt L1 derivation rules
- May need product-type-specific logic

---

## 📊 Progress Tracking

Update this table as you complete each series:

| Series | Status | Output | QC | Review | Archive |
|--------|--------|--------|----|----|--------|
| LC1E | ✅ Complete | ✅ | ✅ | ⏳ | ⏳ |
| LC1D | ⏳ | - | - | - | - |
| GIG | ⏳ | - | - | - | - |
| CAPACITOR_DUTY | ⏳ | - | - | - | - |
| LC1K | ⏳ | - | - | - | - |
| EOCR | ⏳ | - | - | - | - |
| PROTECT | ⏳ | - | - | - | - |
| ACCESSORIES | ⏳ | - | - | - | - |
| COMPATIBILITY | ⏳ | - | - | - | - |

---

## ✅ Success Criteria

**Per Series:**
- ✅ All Phase 5 validation gates passed
- ✅ NSW format workbook generated
- ✅ QC summary created
- ✅ Governance review approved
- ✅ Outputs archived

**Overall:**
- ✅ All 8 series processed
- ✅ Complete catalog coverage
- ✅ All outputs validated

---

## 📝 Next Action

**Start with LC1D:**
1. Extract LC1D data from `NSW_ITEM_MASTER_ENGINEER_VIEW`
2. Create extraction script (reuse LC1E pattern)
3. Follow Phase 5 pipeline steps 2-5
4. Generate NSW workbook
5. Run QC validation

**See:** `ALL_SERIES_PROCESSING_PLAN.md` for detailed plan

