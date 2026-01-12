# Governance: Freeze v1.2 CLEAN — Motor Control Equipment

**Status:** 🟢 ACTIVE  
**Scope:** ALL Motor Control Equipment (MCE)  
**Freeze Basis:** `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md`

---

## 📋 Purpose

This folder contains **universal governance documents** that apply to ALL Motor Control Equipment items processed through the Phase-5 catalog pipeline.

**Why Shared?** These documents prevent duplicate "living docs" from diverging across series (LC1D, LC1E, MPCB, MCCB, ACB, accessories).

---

## 📁 Documents

| Document | Purpose |
|----------|---------|
| `SOR_CONTRACT__MOTOR_CONTROL_EQUIPMENT.md` | System of Record contract — defines authoritative data |
| `SOE_CONSUMPTION_GUIDE__MOTOR_CONTROL_EQUIPMENT.md` | System of Engagement guide — defines UI/estimation consumption rules |
| `ALIGNMENT_MATRIX__PHASE5.md` | Governance truth matrix — maps rules → implementation → verification |
| `ALIGNMENT_PACKAGE_SUMMARY.md` | Summary of alignment package |
| `POINTERS_TEMPLATE.md` | Template for series-specific POINTERS.md files |
| `gate_i_column_contract.py` | Gate I validator script (column contract validation) |

---

## 🔗 How to Use

**For Each Series (LC1D, LC1E, MPCB, etc.):**

1. **Create a pointer file** in `active/schneider/<SERIES>/04_docs/POINTERS.md`
2. **Link to these universal docs** (see LC1E example)
3. **Keep series-specific docs local** (QC summaries, execution plans, local notes)

**Example Structure:**
```
active/schneider/LC1E/04_docs/
  ├── POINTERS.md          (points to governance/)
  ├── QC_SUMMARY.md        (LC1E-specific)
  └── LOCAL_NOTES.md       (LC1E-specific, if needed)
```

---

## 📝 Maintenance

**When to Update:**

- **New series processed:** Add entry to Alignment Matrix "Series Processed" table
- **New artifact frozen:** Add entry to SoR Contract "Artifact Registry"
- **Real issue arises:** Follow review & correction process in each document

**Principle:** Rules are required, but when they become roadblocks, we review carefully and adopt what's useful.

---

## 🚀 Replication for Next Series

**To replicate for LC1D, MPCB, etc.:**

1. Use the same contracts (no changes needed)
2. Update Alignment Matrix → add "Series Processed" entry
3. Update SoR Artifact Registry → add new frozen file row
4. Create series-specific QC summary
5. Create `POINTERS.md` in series folder:
   - Copy `POINTERS_TEMPLATE.md` from this governance folder
   - Edit only: series name, dates, and SoR artifact path

**Do NOT create new SoR/SoE docs per series** — that's the point of umbrella governance.

---

**Last Updated:** 2026-01-03  
**Next Review:** When next series is processed, or when real issues arise.

