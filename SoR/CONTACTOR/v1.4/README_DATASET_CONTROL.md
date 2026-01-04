# README_DATASET_CONTROL

**This content should be added as the FIRST sheet inside:**
`SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`

**Sheet Name:** `README_DATASET_CONTROL`

---

## 1. Dataset Identity

| Field | Value |
|-------|-------|
| Dataset Role | SoR – System of Record |
| Dataset Scope | CONTACTOR ONLY |
| Dataset Purpose | Authoritative engineering & catalog data |
| Version | v1.4 |
| State | CLEAN (Post-normalization, approved) |
| Owner | Engineering Governance |
| Change Policy | Controlled (Admin only) |

---

## 2. What This File IS

- ✅ Single source of truth for Contactor-related data
- ✅ Used for testing, validation, estimation, and AI-assisted workflows
- ✅ Contains real, authoritative data
- ✅ May be read by tools, scripts, AI, and engineers

---

## 3. What This File IS NOT

- ❌ Not a working scratch file
- ❌ Not a rulebook
- ❌ Not a temporary extraction
- ❌ Not reusable for MPCB / MCCB / ACB / VFD
- ❌ Not to be duplicated for new categories

---

## 4. Authoritative Data Sheets (ONLY THESE CONTAIN DATA)

| Sheet Name | Status |
|------------|--------|
| item_tesys_eocr_work | ✅ DATA |
| item_tesys_protect_work | ✅ DATA |
| item_giga_series_work | ✅ DATA |
| item_k_series_work | ✅ DATA |
| item_capacitor_duty_work | ✅ DATA |
| nsw_item_master_engineering_view | ✅ DATA |
| accessory_master | ✅ DATA |

**Rule:** Any logic, test, validation, or review must source data only from this list.

---

## 5. Non-Data / Governance Sheets

| Sheet Pattern | Rule |
|---------------|------|
| *_archive_* | ❌ Historical only (e.g., accessory_master_archive_old) |
| README_* | ❌ Explanation only |
| LOG_* / TRACE_* | ❌ Audit only |
| Any future rules | ❌ Must move to SoE file |

**Rule:** These sheets must NOT be treated as data sources.

---

## 6. Excluded / Archive Sheets

| Sheet Name | Status |
|------------|--------|
| accessory_master_archive_old | ❌ Historical only. Must NOT be used. |

**Rule:** Archive sheets are read-only historical debris. Do not read, merge, or reuse.

---

## 7. Usage Rules (MANDATORY)

1. Do not edit data sheets without approval
2. Do not add MPCB/MCCB data here
3. Do not copy this file for other categories
4. Any transformation must reference this file as input only
5. AI tools may READ this file, never MODIFY it

---

## 8. Golden Rule

> **If a file is not named `SoR_CONTACTOR_DATASET_*`, it is NOT data.**

---

## 9. Change Log

| Date | Version | Change |
|------|---------|--------|
| 2026-01-03 | v1.4 | Dataset locked and standardized |

---

## 10. Scope and Limits

**Category Coverage:**
- CONTACTOR items only

**Explicit Exclusions:**
- MPCB
- MCCB
- ACB
- VFD
- Any other category

**Purpose:**
- Testing and validation
- Reference for engineering work
- Input to estimation workflows

**This file must NOT be used as a base for MCCB, MPCB, ACB, or other categories.**

---

**END OF README_DATASET_CONTROL**



