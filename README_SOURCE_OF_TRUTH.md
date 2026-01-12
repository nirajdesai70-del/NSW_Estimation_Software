# SOURCE OF TRUTH

**As of 2026-01-03**

---

## 🔒 SINGLE SOURCE OF TRUTH

**`catalog_pipeline_v2/`** is the **ONLY** active catalog pipeline system.

All new series (LC1E, MCCB, ACB, etc.) must be built inside:
```
catalog_pipeline_v2/active/<vendor>/<series>/
```

---

## ❌ NOT SOURCE OF TRUTH

Any Excel or CSV file **outside** `catalog_pipeline_v2/` is **NOT** a live artifact.

This includes:
- Files at root level
- Files in `input/`, `output/`, `logs/` at root
- Old `catalog_pipeline/` (v1) - now archived
- Transitional migration files

---

## 📁 FOLDER MEANINGS

| Folder | Status | Purpose |
|--------|--------|---------|
| `catalog_pipeline_v2/` | ✅ **LIVE** | Active execution system |
| `SoR/` | ✅ **DATA** | System of Record (authoritative datasets) |
| `SoE/` | ✅ **RULES** | System of Explanation (rules, logic, governance) |
| `SoW/` | ⚠️ **WORK** | System of Work (temporary, experiments) |
| `ARCHIVE/` | 📦 **HISTORY** | Archived legacy systems |
| `DATA_MIGRATION_ARCHIVE/` | 📦 **REFERENCE** | Historical migration inputs |

---

## 🚫 DEPRECATED (DO NOT USE)

- `input/` at root → deprecated
- `output/` at root → deprecated  
- `logs/` at root → deprecated
- `scripts/` at root → deprecated
- `templates/` at root → deprecated
- `catalog_pipeline/` (v1) → archived

---

## ✅ WORKING DISCIPLINE

**Allowed:**
- Work only inside `catalog_pipeline_v2/active/<vendor>/<series>/`
- Reference `SoR/` for authoritative data
- Reference `SoE/` for rules and logic

**Not Allowed:**
- Creating Excel files at root
- Running scripts from root
- Uploading root files to AI
- Referencing old `output/` paths
- Using archived files for new work

---

## 🧭 GOLDEN RULE

> **If it's not under `catalog_pipeline_v2/active`, it's not live.**

---

## 📌 FOR AI / CURSOR

When processing catalog data:
1. ✅ Use `catalog_pipeline_v2/active/` for execution
2. ✅ Use `SoR/` for authoritative data
3. ✅ Use `SoE/` for rules and definitions
4. ❌ Do NOT use root-level Excel files
5. ❌ Do NOT use archived systems

---

**This document prevents future drift and confusion.**



