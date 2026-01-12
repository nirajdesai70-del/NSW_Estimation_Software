# ARCH — Archive (DEAD / HISTORY)

## Purpose
This folder contains **archived, deprecated, and historical** files that are no longer active.

---

## Core Principle

> **SoR = Data | SoE = Rules | SoW = Work | ARCH = History**

If a file is in **ARCH**, it is **DEAD** — never reuse, never copy forward.

---

## Structure

```
ARCH/
├── 2026-01-03_PRE_CLEANUP/
│   ├── Old catalog_pipeline/ (v1)
│   ├── Root-level input/output/logs/
│   └── Transitional migration files
└── <CATEGORY>/
    └── PRE_v<version>/
        └── ARCH_<CATEGORY>_<PURPOSE>_<date>.xlsx
```

---

## Rules

✅ **Allowed:**
- Old versions of datasets
- Deprecated systems
- Historical references
- Pre-cleanup artifacts

❌ **Not Allowed:**
- Reusing archived files
- Copying archived files forward
- Treating archived files as current
- Modifying archived files

---

## File Naming Convention

**Pattern:**
```
ARCH_<CATEGORY>_<PURPOSE>_<date>.<ext>
```

**Examples:**
- `ARCH_CONTACTOR_DATASET_PRE_v1.4.xlsx`
- `ARCH_LC1E_ENGINEER_REVIEW_2024.xlsx`
- `ARCH_OLD_PRICE_LISTS.xlsx`

---

## Usage

- ✅ **Read-only** for historical reference
- ✅ **Never modify** archived files
- ✅ **Never copy** to active locations
- ❌ **Never reference** in production
- ❌ **Never reuse** for new work

---

## Lifecycle

1. Files moved here when deprecated
2. Kept for historical reference only
3. Can be deleted if no longer needed (with approval)

---

## Golden Rule

> **ARCH remembers mistakes. SoR holds facts.**



