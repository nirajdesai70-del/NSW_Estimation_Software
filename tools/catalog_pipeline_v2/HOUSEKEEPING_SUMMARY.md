# Catalog Pipeline v2 - Housekeeping Summary

**Date**: 2026-01-03  
**Status**: 📋 PLANNED → 🚀 READY FOR EXECUTION

---

## 🎯 What We're Doing

**Lightweight but disciplined housekeeping** to prevent the `catalog_pipeline_v2/` folder from drifting into ambiguity.

**Key Principle:** Freeze what is live, archive what is historical, clearly mark what is temporary.

---

## 📁 What Gets Organized

### ✅ What We DO
1. **Create `ARCH_EXECUTION/`** - Archive execution debris from previous iterations
2. **Tag scripts** - Mark active vs legacy scripts with status comments
3. **Archive output debris** - Move temporary/test/debug files to `ARCH_EXECUTION/`
4. **Archive documentation** - Move historical execution docs to `ARCH_EXECUTION/`
5. **Create README files** - Document the structure

### ❌ What We DON'T Do
- Delete any files (only move/archive)
- Touch `active/`, `archives/`, `templates/`, `freeze_docs/`
- Refactor working scripts
- Over-organize into deep trees

---

## 🚀 How to Execute

### Recommended: Python Script (Safe Version)

```bash
cd tools/catalog_pipeline_v2

# Preview Phase 1 (recommended first)
python3 execute_housekeeping.py --phase1-only --dry-run

# Execute Phase 1 (safe cleanup, no script moves)
python3 execute_housekeeping.py --phase1-only

# After confirming pipeline works, run Phase 2
python3 execute_housekeeping.py
```

**Safety features:**
- ✅ Full backup before any changes
- ✅ Safe script tagging (only shebang files)
- ✅ Stub files for moved scripts (prevents broken references)
- ✅ Two-phase approach (Phase 1 safe, Phase 2 script moves)
- ✅ Dry-run mode for preview

See [`HOUSEKEEPING_EXECUTION_GUIDE.md`](HOUSEKEEPING_EXECUTION_GUIDE.md) for detailed instructions.

### Alternative: Bash Script (Original)

```bash
cd tools/catalog_pipeline_v2
./EXECUTE_HOUSEKEEPING.sh
```

**Note:** The Python version (`execute_housekeeping.py`) is recommended as it includes additional safety features.

---

## 📋 Structure After Housekeeping

```
catalog_pipeline_v2/
├── active/                    # ✅ UNTOUCHED - Current work
├── archives/                  # ✅ UNTOUCHED - Frozen history
├── templates/                 # ✅ UNTOUCHED - Reusable templates
├── freeze_docs/               # ✅ UNTOUCHED - Frozen documentation
│
├── ARCH_EXECUTION/            # 🆕 NEW - Execution debris archive
│   ├── 2025-12_ITERATION_1/
│   ├── 2025-12_ITERATION_2/
│   └── README.md
│
├── scripts/                   # 📝 ORGANIZED
│   ├── [active scripts]       # Tagged: # STATUS: ACTIVE
│   ├── legacy/                # Tagged: # STATUS: LEGACY
│   └── README.md
│
├── output/                    # 🧹 CLEANED
│   └── [only active outputs or empty]
│
├── README.md                  # ✅ KEPT - Main documentation
├── OPERATING_MODEL.md         # ✅ KEPT - Operating model
├── NEXT_SERIES_BOOTSTRAP.md   # ✅ KEPT - Bootstrap guide
└── HOUSEKEEPING_PLAN.md       # 📋 This plan
```

---

## ✅ Success Criteria

Housekeeping is complete when:

1. ✅ All active scripts are tagged with `# STATUS: ACTIVE`
2. ✅ All legacy scripts are in `scripts/legacy/` and tagged
3. ✅ All execution debris is in `ARCH_EXECUTION/`
4. ✅ `output/` folder is clean (only active outputs or empty)
5. ✅ Root-level docs are either governance/reference or archived
6. ✅ README files document the structure
7. ✅ Active scripts still work (backward compatibility maintained)

---

## 🔄 Going Forward

**This is the last structural cleanup.**

After this, the discipline is:

- **New work** → goes to `SoW/`
- **Final data** → goes to `SoR/`
- **Old execution junk** → goes to `ARCH_EXECUTION/` (or `ARCH/` after freeze)
- **Nothing accumulates** in live paths

**One-Line Golden Rule:**
> If a file is not part of today's execution OR not explicitly CLEAN, it must live in `ARCH_EXECUTION` or `SoW` — never alongside active work.

---

## 📚 Related Documents

- [`HOUSEKEEPING_PLAN.md`](HOUSEKEEPING_PLAN.md) - Detailed plan with full checklist
- [`EXECUTE_HOUSEKEEPING.sh`](EXECUTE_HOUSEKEEPING.sh) - Automated execution script
- [`OPERATING_MODEL.md`](OPERATING_MODEL.md) - Operating model (governance)
- [`README.md`](README.md) - Main pipeline documentation

---

**Ready to execute?** Run `./EXECUTE_HOUSEKEEPING.sh` or follow the manual checklist in `HOUSEKEEPING_PLAN.md`.

