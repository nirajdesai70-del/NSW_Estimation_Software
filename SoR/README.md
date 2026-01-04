# SoR — System of Record (DATA)

## Purpose
This folder contains **authoritative datasets** — the single source of truth for all engineering and catalog data.

---

## Core Principle

> **SoR = Data | SoE = Rules | SoW = Work | ARCH = History**

If a file is not in **SoR**, it is **NOT DATA**.

---

## Structure

```
SoR/
└── <CATEGORY>/
    └── v<version>/
        └── SoR_<CATEGORY>_DATASET_v<version>_CLEAN.xlsx
```

---

## Rules

✅ **Allowed:**
- Authoritative datasets only
- One dataset per category per version
- Read-only for most users
- Used by estimation, AI, validation, testing

❌ **Not Allowed:**
- Rules or logic files
- Experiments or temporary work
- Working scratch files
- Multiple versions of same dataset (archive old ones)

---

## Current Datasets

### CONTACTOR
- **Location:** `SoR/CONTACTOR/v1.4/`
- **File:** `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`
- **Status:** ✅ Authoritative
- **Data Sheets:** See README_DATASET_CONTROL inside file

---

## File Naming Convention

**Pattern:**
```
SoR_<CATEGORY>_DATASET_v<version>_<STATE>.xlsx
```

**Examples:**
- `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`
- `SoR_MPCB_DATASET_v1.0_CLEAN.xlsx`
- `SoR_MCCB_DATASET_v1.0_CLEAN.xlsx`

**States:**
- `CLEAN` → Approved, final
- `WORKING` → In progress (temporary)
- `DRAFT` → Unstable (temporary)

---

## Usage

1. **Read-only access** for most users
2. **Admin-only edits** for data correction
3. **Reference only** — never modify for new categories
4. **Version control** — archive old versions to `ARCH/`

---

## Golden Rule

> **If a file does not start with `SoR_`, it is NOT data.**



