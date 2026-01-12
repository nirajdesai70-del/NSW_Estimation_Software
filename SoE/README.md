# SoE — System of Explanation (RULES / LOGIC)

## Purpose
This folder contains **rules, logic, and governance** that explain how to interpret and use SoR data.

---

## Core Principle

> **SoR = Data | SoE = Rules | SoW = Work | ARCH = History**

If a file is not in **SoE**, it is **NOT a rule**.

---

## Structure

```
SoE/
└── <CATEGORY>/
    ├── SoE_<CATEGORY>_RULEBOOK_v<version>_CLEAN.md
    ├── SoE_<CATEGORY>_ATTRIBUTE_DEFINITION.xlsx
    └── SoE_<CATEGORY>_QC_RULES.md
```

---

## Rules

✅ **Allowed:**
- Rulebooks and definitions
- Attribute specifications
- QC logic and validation rules
- Naming conventions
- Governance documentation

❌ **Not Allowed:**
- Live data (use SoR for that)
- Temporary experiments (use SoW for that)
- Historical archives (use ARCH for that)

---

## File Naming Convention

**Pattern:**
```
SoE_<CATEGORY>_<PURPOSE>_v<version>_<STATE>.<ext>
```

**Examples:**
- `SoE_CONTACTOR_RULEBOOK_v1.2_CLEAN.md`
- `SoE_CONTACTOR_ATTRIBUTE_DEFINITION.xlsx`
- `SoE_CONTACTOR_QC_RULES.md`
- `SoE_NSWARE_TERMINOLOGY_FREEZE_v1.2_CLEAN.md`

**Purposes:**
- `RULEBOOK` → Complete rules and logic
- `ATTRIBUTE_DEFINITION` → Column/field specifications
- `QC_RULES` → Quality control logic
- `TERMINOLOGY_FREEZE` → Frozen terminology

---

## Usage

1. **Reference** when building new categories
2. **Read-only** for most users
3. **Admin-only edits** for rule changes
4. **Version control** — archive old versions to `ARCH/`

---

## Relationship to SoR

- **SoR** contains the data
- **SoE** explains how to read and use that data
- **SoE** defines what is valid/invalid
- **SoE** provides the logic for transformations

---

## Golden Rule

> **SoE explains facts. SoR holds facts.**



