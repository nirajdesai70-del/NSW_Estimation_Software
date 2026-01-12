# Housekeeping Execution Guide

**Date**: 2026-01-03  
**Script**: `execute_housekeeping.py` (Python, safe version)

---

## 🎯 What This Script Does

**Safe housekeeping** with:
- ✅ Full backup of `scripts/` before any changes
- ✅ Safe script tagging (only shebang files, checks for existing tags)
- ✅ Stub files for moved scripts (prevents broken references)
- ✅ Two-phase approach (Phase 1 safe, Phase 2 script moves)
- ✅ Dry-run mode for preview

---

## 🚀 Quick Start

### Option 1: Safe Phase 1 Only (Recommended First)

```bash
cd tools/catalog_pipeline_v2

# Preview what will happen (dry-run)
python3 execute_housekeeping.py --phase1-only --dry-run

# Execute Phase 1 (safe cleanup, no script moves)
python3 execute_housekeeping.py --phase1-only
```

**What Phase 1 does:**
- Creates `ARCH_EXECUTION/` structure
- Backs up `scripts/` folder
- Archives output debris (tmp/test/debug files)
- Archives historical documentation
- **Does NOT move or tag scripts**

### Option 2: Full Housekeeping (After Phase 1 Works)

```bash
cd tools/catalog_pipeline_v2

# Preview full housekeeping
python3 execute_housekeeping.py --dry-run

# Execute full housekeeping (Phase 1 + Phase 2)
python3 execute_housekeeping.py
```

**What Phase 2 adds:**
- Tags active scripts (safely, only shebang files)
- Moves legacy scripts to `scripts/legacy/`
- Moves one-off scripts to `ARCH_EXECUTION/one_off_scripts/`
- Creates stub files for moved scripts (prevents broken references)

---

## 📋 Command Options

```bash
python3 execute_housekeeping.py [OPTIONS]

Options:
  --phase1-only    Run only Phase 1 (safe cleanup, no script moves)
  --dry-run        Preview changes without making them
  -h, --help       Show help message
```

---

## ✅ Safety Features

### 1. Full Backup
- `scripts/` folder is backed up to `ARCH_EXECUTION/.../backup/scripts/`
- Created before any modifications

### 2. Safe Script Tagging
- Only tags files with shebang (`#!/usr/bin/env python3`)
- Checks for existing tags (won't duplicate)
- Skips files without shebang (no docstring breaking)

### 3. Stub Files for Moved Scripts
- When one-off scripts are moved, stub files are created at original locations
- Stub files print helpful error message and point to archive location
- Prevents broken references in docs/templates

### 4. Two-Phase Approach
- **Phase 1**: Safe (outputs + docs only)
- **Phase 2**: Script organization (run after confirming Phase 1 works)

---

## 📁 What Gets Created

```
catalog_pipeline_v2/
├── ARCH_EXECUTION/
│   └── 2026-01-03_PHASE5_CLEANUP_<timestamp>/
│       ├── backup/
│       │   └── scripts/          # Full backup
│       ├── tmp_outputs/          # Temporary files
│       ├── test_outputs/         # Test files
│       ├── debug/                 # Debug files
│       ├── docs/                  # Historical docs
│       ├── one_off_scripts/       # Moved scripts (Phase 2)
│       └── README.md             # Archive index
│
├── scripts/
│   ├── [active scripts]           # Tagged (Phase 2)
│   ├── legacy/                    # Legacy scripts (Phase 2)
│   └── README.md                  # Script index
```

---

## 🔍 Dry-Run Mode

Always preview changes first:

```bash
python3 execute_housekeeping.py --phase1-only --dry-run
```

This shows what would happen without making any changes.

---

## ⚠️ Important Notes

1. **No files are deleted** - Everything is moved/archived
2. **Scripts remain at root** - Active scripts stay at `scripts/` root for template compatibility
3. **Stub files** - Moved scripts have stubs at original locations (prevents breaks)
4. **Backward compatible** - Template scripts (`templates/run_pipeline.sh`) continue to work

---

## 🎯 Recommended Workflow

### Step 1: Preview Phase 1
```bash
python3 execute_housekeeping.py --phase1-only --dry-run
```

### Step 2: Execute Phase 1
```bash
python3 execute_housekeeping.py --phase1-only
```

### Step 3: Verify Pipeline Still Works
```bash
# Test that pipeline execution still works
cd active/schneider/LC1E
./run_pipeline.sh  # or test with a new series
```

### Step 4: Run Phase 2 (After Confirming Step 3)
```bash
python3 execute_housekeeping.py  # Full housekeeping
```

---

## 🐛 Troubleshooting

### Script Tagging Failed
- **Cause**: File doesn't have shebang or already tagged
- **Action**: Script skips it safely (no error)

### Stub File Created
- **Cause**: One-off script was moved
- **Action**: Stub file points to archive location. If needed, copy script back from archive.

### Template Script Breaks
- **Cause**: Script path changed
- **Action**: Active scripts remain at root, so this shouldn't happen. If it does, check `templates/run_pipeline.sh` paths.

---

## 📚 Related Documents

- [`HOUSEKEEPING_PLAN.md`](HOUSEKEEPING_PLAN.md) - Detailed plan
- [`HOUSEKEEPING_SUMMARY.md`](HOUSEKEEPING_SUMMARY.md) - Quick summary
- [`README.md`](README.md) - Main pipeline documentation

---

**Ready to execute?** Start with Phase 1 dry-run:

```bash
cd tools/catalog_pipeline_v2
python3 execute_housekeeping.py --phase1-only --dry-run
```

