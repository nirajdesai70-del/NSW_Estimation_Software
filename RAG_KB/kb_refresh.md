# KB Refresh — Cursor Task

**Version:** 1.0  
**Date:** 2025-12-27  
**Purpose:** Compile Phase-5 + supporting structures into `/RAG_KB/phase5_pack/` and update the master

---

## Goal

Build/update the curated Knowledge Pack that RAG will index. This process:
1. Scans Phase-5 folders and extracts latest authoritative files
2. Builds structured knowledge pack with proper metadata
3. Generates master consolidation file in latest canonical format
4. Produces delta reports and gap analysis

---

## Steps (Execute in Order)

### Step 1: Scan Repository Areas (Read-Only)

Read from these repo areas to build the knowledge pack:

#### A) Phase-5 Documentation (`docs/PHASE_5/`)
- **00_GOVERNANCE/** - All governance docs, decision registers, policies
- **01_REFERENCE/** - Legacy review, fundamentals alignment
- **02_FREEZE_GATE/** - Freeze checklists, evidence
- **03_DATA_DICTIONARY/** - Data dictionary, validation rules, naming conventions
- **04_SCHEMA_CANON/** - Schema canonical, ER diagrams, table inventory
- **05_TRACEABILITY/** - Trace maps, requirement maps
- **06_IMPLEMENTATION_REFERENCE/** - Implementation roadmap, explosion logic
- **CANONICAL/** - Canonical structures (L2 import, Excel template)
- **INPUT_ASSETS/** - Input asset documentation

**Latest File Selection Rules:**
- Prefer files with `CANONICAL` or `FINAL` in name/metadata
- Otherwise use most recently modified file per folder
- Ignore: `_old`, `copy`, `v0`, `.bak`, `DRAFT` (unless explicitly marked canonical)

#### B) Catalog Pipeline (`tools/catalog_pipeline_v2/`)
- **scripts/** - All Python scripts (build_l2, derive_l1, extract_canonical, etc.)
- **README.md** - Pipeline documentation
- **OPTION_B_EXECUTION_PLAN.md** - Latest execution plan
- **OPTION_B_REVIEW.md** - Review documentation
- **NEXT_STEPS_LC1E.md** - Status and next steps

#### C) Supporting Structures
- **docs/NSW_ESTIMATION_MASTER.md** - Master execution plan
- **docs/NSW_ESTIMATION_BASELINE.md** - Baseline documentation
- **features/** - Feature documentation (latest only, per module)
- **changes/** - Change registers (summaries only)
- **trace/** - Trace documentation (latest per phase)

#### D) Chat Mirror (`RAG_KB/chat_mirror/`)
- All `.md` files with proper metadata headers
- Include in knowledge pack with WORKING authority (unless promoted)

---

### Step 2: Build Knowledge Pack Components

#### 2.1: Create `00_INDEX.json` (Manifest)

```json
{
  "version": "1.0",
  "last_refresh": "YYYY-MM-DDTHH:MM:SS",
  "files": [
    {
      "namespace": "phase5_docs",
      "folder": "docs/PHASE_5/00_GOVERNANCE",
      "filename": "PHASE_5_CHARTER.md",
      "status": "CANONICAL",
      "last_modified": "2025-01-27",
      "authority": "CANONICAL",
      "kb_path": "phase5_pack/04_RULES_LIBRARY/governance/PHASE_5_CHARTER.md"
    }
    // ... more entries
  ],
  "statistics": {
    "total_files": 0,
    "canonical_count": 0,
    "working_count": 0,
    "draft_count": 0
  }
}
```

**Rules:**
- One entry per unique folder (latest file only)
- Include full metadata: namespace, status, authority, version
- Track file counts by authority level

#### 2.2: Create `00_FOLDER_MAP.md` (Human-Readable Structure)

```markdown
# Phase 5 Folder Structure Map

## docs/PHASE_5/
### 00_GOVERNANCE/
  - Latest: PHASE_5_CHARTER.md (CANONICAL)
  - Files: [list all, highlight latest]
### 01_REFERENCE/
  - Latest: [filename] (STATUS)
...
```

**Purpose:** Visual representation of folder structure + latest file per folder

#### 2.3: Build `03_FEATURE_FLAGS.md`

Extract all feature flags, defaults, scopes, and phase mapping from:
- Phase-5 governance docs
- Execution plans
- Implementation roadmaps

**Format:**
```markdown
# Feature Flags Registry

## Flag: [Name]
- **Default**: [value]
- **Scope**: [phase/module]
- **Source**: [doc reference]
- **Status**: CANONICAL | WORKING
```

#### 2.4: Build `02_DECISIONS_LOG.md`

Extract only LOCKED/CANONICAL decisions from:
- `PHASE_5_DECISIONS_REGISTER.md`
- `PHASE_5_DECISION_SUMMARY.md`
- Decision Capture Rules
- ADR documents

**Format:**
```markdown
# Decisions Log

## Decision: [Title]
- **Date**: YYYY-MM-DD
- **Status**: LOCKED
- **Source**: [file path + section]
- **Rationale**: [why this decision]
- **Impact**: [what it affects]
```

#### 2.5: Build `04_RULES_LIBRARY/` (Organized by Domain)

Copy latest rules files into organized structure:

```
04_RULES_LIBRARY/
├── governance/
│   ├── PHASE_5_CHARTER.md
│   ├── PHASE_5_MODE_POLICY.md
│   └── DECISION_CAPTURE_RULES.md
├── catalog/
│   ├── SCHNEIDER_FINAL_RULES_v1.2.md
│   └── CATALOG_INTERPRETATION_RULES.md
├── l1_l2/
│   ├── L1_L2_EXPLOSION_LOGIC.md
│   └── SCHNEIDER_L1_L2_EXPANSION_LOGIC.md
├── make_series/
│   └── [make/series policy rules]
└── bundling/
    └── [bundling rules: built-in vs separate SKU]
```

**Rules:**
- Only copy CANONICAL or latest WORKING files
- Preserve source attribution in file header
- Maintain folder hierarchy where logical

#### 2.6: Build `05_IMPLEMENTATION_NOTES/`

Copy implementation artifacts:
- Scripts from `tools/catalog_pipeline_v2/scripts/`
- Schema files from `docs/PHASE_5/04_SCHEMA_CANON/`
- Migration/seed scripts (if any)

**Format:** Copy with metadata header:
```markdown
---
Source: [original path]
KB_Namespace: implementation_artifacts
Status: WORKING
Last_Updated: [date]
---
[file content]
```

#### 2.7: Build `06_INPUT_SNAPSHOTS/` (Summaries Only)

For large files (XLSX, PDF), create summary documents:
- Catalog export summaries
- Price list version notes
- Mapping table summaries

**Do NOT copy full XLSX/PDF files** - create markdown summaries instead.

#### 2.8: Build `07_TRACKERS_EXPORT/`

Copy tracker summaries:
- Gap registers
- Change registers
- Task registers (if relevant to Phase 5)

**Format:** Latest only, markdown summaries preferred.

#### 2.9: Build `01_CANONICAL_MASTER.md` (Master Consolidation)

**This is the single source of truth.** Build using the format from latest Phase-5 master document.

**Template Structure:**
```markdown
# Phase 5 Master Consolidation

**Version:** [auto-increment]
**Last Updated:** [refresh timestamp]
**Generated By:** KB Refresh Process

---

## Metadata
- KB Version: [from 00_INDEX.json]
- Source Files: [count from manifest]
- Authority Breakdown: CANONICAL: X, WORKING: Y, DRAFT: Z

## Purpose
[From Phase 5 Charter]

## Canonical Definitions (Locked)
[Extract from CANONICAL sources only]

## Phase-5 Scope & Entry Gates
[From governance docs]

## Work Completed
### By Category
- Governance: [list completed items]
- Data Dictionary: [list]
- Schema: [list]
- Implementation: [list]

### Evidence
- [Links to source files with versions]

## Work Pending
- [From execution plans, next steps docs]

## Decisions Log Summary
- [Top-level decisions, link to full log]

## Risk Register
- [High-priority risks from governance docs]

## Implementation Notes
- [Key implementation patterns, cursor-ready]

## Appendices
- [Links to scripts, data models, sample inputs]
```

**Critical Rules:**
- **Never overwrite locked sections** - append new version blocks instead
- **Cite sources** for every major section
- **Preserve authority tags** (CANONICAL sections remain immutable)
- **Use latest canonical format** as template

---

### Step 3: Produce Delta Reports

#### 3.1: `DELTA_SINCE_LAST.md`

```markdown
# Delta Report - KB Refresh

**Refresh Date:** YYYY-MM-DD HH:MM:SS
**Previous Refresh:** YYYY-MM-DD HH:MM:SS

## New Files Added
- [list new files with paths]

## Files Updated
- [list changed files with change type]

## Files Removed/Deprecated
- [list deprecated files]

## Authority Changes
- [files promoted to CANONICAL]
- [files demoted to WORKING]

## Master File Changes
- [sections added/modified in 01_CANONICAL_MASTER.md]
```

#### 3.2: `RISKS_AND_GAPS.md`

```markdown
# Risks and Gaps Report

**Generated:** YYYY-MM-DD

## Blocking Issues
- [list critical blockers]

## High Priority Gaps
- [missing canonical sources]
- [incomplete implementations]

## Informational Items
- [notes, warnings, recommendations]
```

---

### Step 4: Validation Checks

Before completing refresh, validate:

- [ ] `00_INDEX.json` is valid JSON
- [ ] All CANONICAL files have proper metadata
- [ ] No locked sections were overwritten in master file
- [ ] All citations include file path + version
- [ ] Folder map accurately reflects structure
- [ ] Delta report captures all changes

---

## Output Requirements

### Deterministic Output
- No invented fields. If unknown, list as `OPEN` and point to missing source.
- All timestamps in ISO 8601 format
- All file paths relative to repo root

### File Locations
- All outputs go to `/RAG_KB/phase5_pack/`
- Delta reports go to `/RAG_KB/build_reports/`
- Do NOT modify source files in `docs/PHASE_5/` (read-only)

---

## Usage

Run this refresh process:
1. **Manually**: When you complete a major Phase-5 milestone
2. **On Trigger**: When Phase-5 files change (via CI/webhook)
3. **Scheduled**: Daily at low-traffic time (optional)

After refresh:
- RAG indexer picks up new/changed files in `/RAG_KB/phase5_pack/`
- Query service uses updated KB
- Doc builder regenerates master from latest pack

---

## Error Handling

If refresh fails:
- Preserve previous KB state (no partial updates)
- Log error details to `build_reports/ERROR_LOG.md`
- Report which step failed and why
- Suggest remediation steps

---

## Change Log

- **v1.0** (2025-12-27): Initial KB refresh instructions

