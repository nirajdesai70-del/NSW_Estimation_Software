# Quick Reference: SoR / SoE / SoW / ARCH

**One-page cheat sheet for daily use.**

---

## 🧭 The Law

> **SoR = Data | SoE = Rules | SoW = Work | ARCH = History**

---

## 📁 Where Things Go

| What | Where | Example |
|------|-------|---------|
| **Data** | `SoR/<CATEGORY>/v<version>/` | `SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx` |
| **Rules** | `SoE/<CATEGORY>/` | `SoE/CONTACTOR/SoE_CONTACTOR_RULEBOOK_v1.2_CLEAN.md` |
| **Temp Work** | `SoW/<CATEGORY>/` | `SoW/LC1E/SoW_LC1E_EXTRACTION_WORKING.xlsx` |
| **Old Stuff** | `ARCH/<date>_<desc>/` | `ARCH/2026-01-03_PRE_CLEANUP/` |
| **Live Execution** | `catalog_pipeline_v2/active/<vendor>/<series>/` | `catalog_pipeline_v2/active/schneider/LC1E/` |

---

## 🏷️ Naming Rules

### SoR (Data)
```
SoR_<CATEGORY>_DATASET_v<version>_<STATE>.xlsx
```
- `CLEAN` = Approved
- `WORKING` = In progress
- `DRAFT` = Unstable

### SoE (Rules)
```
SoE_<CATEGORY>_<PURPOSE>_v<version>_CLEAN.<ext>
```
- `RULEBOOK`, `ATTRIBUTE_DEFINITION`, `QC_RULES`, etc.

### SoW (Work)
```
SoW_<CATEGORY>_<PURPOSE>_<SESSION>.<ext>
```
- Temporary, can delete

### ARCH (History)
```
ARCH_<CATEGORY>_<PURPOSE>_<date>.<ext>
```
- Never reuse

---

## ✅ Allowed Actions

| Zone | Read | Edit | Delete | Reference in Code |
|------|------|------|---------|-------------------|
| **SoR** | ✅ Yes | ❌ Admin only | ❌ No | ✅ Yes |
| **SoE** | ✅ Yes | ❌ Admin only | ❌ No | ✅ Yes |
| **SoW** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **ARCH** | ✅ Yes | ❌ No | ⚠️ With approval | ❌ No |

---

## ❌ Never Do This

- ❌ Create Excel files at root
- ❌ Use root-level `input/`, `output/`, `logs/`
- ❌ Copy ARCH files to active locations
- ❌ Treat SoW files as authoritative
- ❌ Mix data and rules in same file
- ❌ Reuse CONTACTOR dataset for MCCB/MPCB

---

## 🔍 How to Find Things

**Need data?** → `SoR/`  
**Need rules?** → `SoE/`  
**Need to experiment?** → `SoW/`  
**Need to execute?** → `catalog_pipeline_v2/active/`  
**Need history?** → `ARCH/`

---

## 📌 For CONTACTOR Specifically

**Data File:**
- `SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`

**Data Sheets (only these):**
1. `item_tesys_eocr_work`
2. `item_tesys_protect_work`
3. `item_giga_series_work`
4. `item_k_series_work`
5. `item_capacitor_duty_work`
6. `nsw_item_master_engineering_view`
7. `accessory_master`

**Excluded:**
- `accessory_master_archive_old` (and any `*_archive_*`)

---

## 🚀 For New Categories (MPCB, MCCB, ACB)

1. Create `SoR/<CATEGORY>/v1.0/`
2. Use template: `SoR/TEMPLATE_SOR_FILE_STRUCTURE.md`
3. Name: `SoR_<CATEGORY>_DATASET_v1.0_CLEAN.xlsx`
4. Add `README_DATASET_CONTROL` sheet
5. List data sheets explicitly
6. Never copy CONTACTOR file

---

## 🆘 Emergency Decision Tree

**"Where does this file go?"**

1. Is it authoritative data? → `SoR/`
2. Is it a rule/definition? → `SoE/`
3. Is it temporary/experiment? → `SoW/`
4. Is it old/deprecated? → `ARCH/`
5. Is it live execution? → `catalog_pipeline_v2/active/`

**"Is this file correct?"**

1. Is it in `SoR/`? → Yes, it's data
2. Is it in `SoE/`? → Yes, it's a rule
3. Is it in `catalog_pipeline_v2/active/`? → Yes, it's live
4. Otherwise → Check if it should be archived

---

**Print this and pin it. Use it daily.**



