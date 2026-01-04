# NSW Data Platform — Governance & Structure

## Purpose
This platform enforces a strict separation between:
- **Data (SoR)**
- **Rules & Logic (SoE)**
- **Working Files (SoW)**
- **Historical Artifacts (ARCH)**

This prevents data corruption, rule leakage, and future ambiguity.

---

## Core Principle (Non-Negotiable)

> **SoR = Data | SoE = Rules | SoW = Work | ARCH = History**

If a file is in the wrong zone, it is invalid by definition.

---

## Folder Structure

```
NSW_Estimation_Software/
├── SoR/        # System of Record (DATA ONLY)
├── SoE/        # System of Explanation (RULES / LOGIC)
├── SoW/        # System of Work (TEMP / OPERATIONS)
├── ARCH/       # Archived / Dead / Historical
├── catalog_pipeline_v2/  # LIVE EXECUTION SYSTEM
├── DATA_MIGRATION_ARCHIVE/  # Historical migration inputs
└── README_SOURCE_OF_TRUTH.md  # Lock file
```

---

## SoR — System of Record (DATA)

- Contains **authoritative datasets**
- Read-only for most users
- Used by estimation, AI, validation, and testing
- One dataset per category per version

**Location:** `SoR/<CATEGORY>/v<version>/`

**Naming:** `SoR_<CATEGORY>_DATASET_v<version>_CLEAN.xlsx`

❌ No rules  
❌ No experiments  
❌ No temporary work  

**See:** `SoR/README.md` for details

---

## SoE — System of Explanation (RULES)

- Explains how to interpret SoR
- Attribute definitions
- QC logic
- Naming conventions

**Location:** `SoE/<CATEGORY>/`

**Naming:** `SoE_<CATEGORY>_<PURPOSE>_v<version>_CLEAN.<ext>`

❌ No live data  

**See:** `SoE/README.md` for details

---

## SoW — System of Work (WORKSPACE)

- Temporary extraction
- AI experiments
- Price imports
- Engineer scratch files

**Location:** `SoW/<CATEGORY>/`

**Naming:** `SoW_<CATEGORY>_<PURPOSE>_<SESSION>.<ext>`

❌ Never treated as truth  

**See:** `SoW/README.md` for details

---

## ARCH — Archive

- Old versions
- Deprecated datasets
- Historical references

**Location:** `ARCH/<date>_<description>/` or `ARCH/<CATEGORY>/PRE_v<version>/`

**Naming:** `ARCH_<CATEGORY>_<PURPOSE>_<date>.<ext>`

❌ Never reused  
❌ Never copied forward  

**See:** `ARCH/README.md` for details

---

## catalog_pipeline_v2 — LIVE EXECUTION SYSTEM

**This is the ONLY active catalog pipeline.**

All new series (LC1E, MCCB, ACB, etc.) must be built inside:
```
catalog_pipeline_v2/active/<vendor>/<series>/
```

**See:** `README_SOURCE_OF_TRUTH.md` for details

---

## Golden Rule

> **If a file is not in SoR, it is NOT DATA.**

> **If a file is not in SoE, it is NOT a RULE.**

> **If a file is not in catalog_pipeline_v2/active, it is NOT LIVE.**

---

## File Classification Model

Every Excel / CSV / DB-export file must declare ONE of the following roles:

| Code | Meaning | Editable | Used for |
|------|---------|----------|----------|
| **SoR** | System of Record | ❌ No | Real data |
| **SoE** | System of Explanation | ❌ No | Rules / logic |
| **SoW** | System of Work | ✅ Yes | Temporary / ops |
| **ARCH** | Archive | ❌ No | History only |

---

## Naming Convention

**Pattern:**
```
<Role>_<Category>_<Purpose>_v<Version>_<State>.<ext>
```

**Examples:**
- `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`
- `SoE_CONTACTOR_RULEBOOK_v1.2_CLEAN.md`
- `SoW_LC1E_EXTRACTION_WORKING.xlsx`
- `ARCH_CONTACTOR_DATASET_PRE_v1.4.xlsx`

---

## Usage Rules

1. **SoR** = Read-only data truth
2. **SoE** = Read-only rules and logic
3. **SoW** = Temporary experiments (can delete)
4. **ARCH** = Historical reference (never reuse)

---

## For Engineers

✅ **Allowed:**
- Work in `catalog_pipeline_v2/active/`
- Reference `SoR/` for data
- Reference `SoE/` for rules
- Experiment in `SoW/`

❌ **Not Allowed:**
- Creating files at root
- Modifying SoR without approval
- Treating SoW as authoritative
- Reusing ARCH files

---

## For AI / Cursor

When processing catalog data:
1. ✅ Use `catalog_pipeline_v2/active/` for execution
2. ✅ Use `SoR/` for authoritative data
3. ✅ Use `SoE/` for rules and definitions
4. ❌ Do NOT use root-level Excel files
5. ❌ Do NOT use archived systems

---

**This structure prevents confusion, data corruption, and future rework.**



