# Cleanup Execution Summary

**Date:** 2026-01-03  
**Status:** ✅ Structure Created — Manual Steps Required

---

## ✅ What Has Been Created

### 1. Root-Level Lock File
- ✅ `README_SOURCE_OF_TRUTH.md` — Declares `catalog_pipeline_v2/` as only live system

### 2. Folder Structure
- ✅ `SoR/` — System of Record (DATA)
  - `SoR/CONTACTOR/v1.4/` — Ready for contactor dataset
  - `SoR/README.md` — SoR governance rules
- ✅ `SoE/` — System of Explanation (RULES)
  - `SoE/CONTACTOR/` — Ready for contactor rules
  - `SoE/README.md` — SoE governance rules
- ✅ `SoW/` — System of Work (TEMP)
  - `SoW/CONTACTOR/` — Ready for temporary work
  - `SoW/README.md` — SoW governance rules
- ✅ `ARCH/` — Archive
  - `ARCH/2026-01-03_PRE_CLEANUP/` — Ready for old files
  - `ARCH/README.md` — Archive governance rules
- ✅ `DATA_MIGRATION_ARCHIVE/ItemMaster_Revisions/` — Ready for migration files

### 3. Documentation
- ✅ `README_PLATFORM.md` — Complete platform governance guide
- ✅ `SoR/CONTACTOR/v1.4/README_DATASET_CONTROL.md` — Content for Excel file
- ✅ `SoR/TEMPLATE_SOR_FILE_STRUCTURE.md` — Template for future categories

---

## 🔧 Manual Steps Required

### Step 1: Locate and Rename Contactor Dataset

**Find this file:**
- `ITEM_Master_020126_v1.4_NORMALIZED_GAPS0.xlsx`

**Rename to:**
- `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`

**Move to:**
- `SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`

---

### Step 2: Add README_DATASET_CONTROL Sheet to Excel

**Action:**
1. Open `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`
2. Create a new sheet named `README_DATASET_CONTROL` (first sheet)
3. Copy content from: `SoR/CONTACTOR/v1.4/README_DATASET_CONTROL.md`
4. Format as a table in Excel
5. Lock the sheet (protect structure)

**Data Sheets to Declare:**
- `item_tesys_eocr_work`
- `item_tesys_protect_work`
- `item_giga_series_work`
- `item_k_series_work`
- `item_capacitor_duty_work`
- `nsw_item_master_engineering_view`
- `accessory_master`

**Excluded Sheets:**
- `accessory_master_archive_old` (and any other `*_archive_*` sheets)

---

### Step 3: Apply Excel Protection

**On Data Sheets:**
- Lock all cells (allow filter/sort only)
- Set tab color to 🟦 Blue

**On README Sheet:**
- Lock the sheet
- Set tab color to 🟩 Green

**On Archive Sheets:**
- Lock the sheet
- Set tab color to 🟥 Red

**Workbook Protection:**
- Protect workbook structure (optional password)

---

### Step 4: Move Revised ItemMaster Folder

**Find:**
- `Revised ItemMaster/` folder (likely at root or in tools/)

**Move to:**
- `DATA_MIGRATION_ARCHIVE/ItemMaster_Revisions/Revised ItemMaster/`

**Why:**
- It's migration input, not execution truth
- Keeps root clean
- Prevents accidental reuse

---

### Step 5: Archive Old Root-Level Folders

**Find and move to `ARCH/2026-01-03_PRE_CLEANUP/`:**
- `input/` (if at root)
- `output/` (if at root)
- `logs/` (if at root)
- `scripts/` (if at root, and not part of catalog_pipeline_v2)
- `templates/` (if at root, and not part of catalog_pipeline_v2)

**Note:** Only move root-level folders. Keep `catalog_pipeline_v2/scripts/` and `catalog_pipeline_v2/templates/` as they are.

---

### Step 6: Archive Old Pipeline (if not already done)

**Verify:**
- `catalog_pipeline/` (v1) is already in `ARCHIVE/2025-12-26_catalog_pipeline_v1/`

**If not, move it:**
- `ARCH/2026-01-03_PRE_CLEANUP/catalog_pipeline/`

---

## 📋 Verification Checklist

After completing manual steps:

- [ ] `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx` exists in `SoR/CONTACTOR/v1.4/`
- [ ] Excel file has `README_DATASET_CONTROL` as first sheet
- [ ] Data sheets are listed in README_DATASET_CONTROL
- [ ] Data sheets are locked and blue
- [ ] Archive sheets are red and excluded
- [ ] `Revised ItemMaster/` moved to `DATA_MIGRATION_ARCHIVE/`
- [ ] Root-level `input/`, `output/`, `logs/` moved to ARCH (if they existed)
- [ ] Root is clean (only `catalog_pipeline_v2/`, `SoR/`, `SoE/`, `SoW/`, `ARCH/`, docs)

---

## 🎯 Final Structure (Target State)

```
NSW_Estimation_Software/
├── README_SOURCE_OF_TRUTH.md          ✅ Created
├── README_PLATFORM.md                 ✅ Created
│
├── catalog_pipeline_v2/               ✅ LIVE (keep as-is)
│   ├── active/
│   ├── scripts/
│   ├── templates/
│   └── ...
│
├── SoR/                               ✅ Created
│   ├── README.md
│   ├── CONTACTOR/
│   │   └── v1.4/
│   │       └── SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx  ⚠️ Move & rename
│   └── TEMPLATE_SOR_FILE_STRUCTURE.md
│
├── SoE/                               ✅ Created
│   ├── README.md
│   └── CONTACTOR/                     (ready for rules)
│
├── SoW/                               ✅ Created
│   ├── README.md
│   └── CONTACTOR/                     (ready for temp work)
│
├── ARCH/                              ✅ Created
│   ├── README.md
│   ├── 2026-01-03_PRE_CLEANUP/        (move old files here)
│   └── 2025-12-26_catalog_pipeline_v1/  (already exists)
│
└── DATA_MIGRATION_ARCHIVE/            ✅ Created
    └── ItemMaster_Revisions/           (move Revised ItemMaster here)
```

---

## 🧭 Golden Rules (Locked)

1. **If it's not in `catalog_pipeline_v2/active`, it's not live.**
2. **If it's not in `SoR/`, it's not data.**
3. **If it's not in `SoE/`, it's not a rule.**
4. **If it's in `ARCH/`, it's dead — never reuse.**

---

## 🚀 Next Steps (After Cleanup)

1. **Bootstrap MCCB** using LC1E Phase-5 template
2. **Create SoR_MPCB_DATASET_v1.0_CLEAN.xlsx** using template
3. **Create SoE_CONTACTOR_RULEBOOK** from existing logic
4. **Train team** on SoR/SoE/SoW/ARCH discipline

---

**Structure is ready. Complete manual steps to finish cleanup.**



