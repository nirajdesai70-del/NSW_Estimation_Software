---
Source: RAG_KB/RAG_RULEBOOK.md
KB_Namespace: rag_governance
Status: CANONICAL
Last_Updated: 2025-12-27T22:23:40.353995
KB_Path: phase5_pack/04_RULES_LIBRARY/rag_governance/RAG_RULEBOOK.md
---
# RAG RULEBOOK — NSW Estimation (Phase 5)

## Objective

Maintain a curated Knowledge Pack for RAG so it can:
1. Understand full Phase-5 plan + feature flags + supporting structures
2. Stay updated with repo changes automatically
3. Learn from exported ChatGPT decisions safely
4. Provide 360° assistance for NSW Estimation Software while staying containerized

---

## Golden Rule

**RAG indexes ONLY `/RAG_KB/` (curated).**  
**No direct indexing of entire repo.**

---

## Knowledge Pack Structure

```
/RAG_KB/
├── phase5_pack/
│   ├── 00_INDEX.json                    # File manifest (latest-only per folder)
│   ├── 00_FOLDER_MAP.md                 # Human-readable folder structure map
│   ├── 01_CANONICAL_MASTER.md           # Single structured master (auto-generated)
│   ├── 02_DECISIONS_LOG.md              # Locked decisions + rationale
│   ├── 03_FEATURE_FLAGS.md              # Feature flags, defaults, scopes
│   ├── 04_RULES_LIBRARY/                # Rules organized by domain
│   │   ├── make_series_policy.md
│   │   ├── bundling_rules.md
│   │   ├── l1_l2_explosion.md
│   │   └── kvu_rules.md
│   ├── 05_IMPLEMENTATION_NOTES/         # Scripts, migrations, converters
│   ├── 06_INPUT_SNAPSHOTS/              # Catalog exports, price lists (summaries)
│   └── 07_TRACKERS_EXPORT/              # Gap register, change register summaries
├── chat_mirror/                         # Exported ChatGPT conversations
│   └── YYYY-MM-DD_topic.md
└── build_reports/                       # KB refresh outputs
    ├── DELTA_SINCE_LAST.md
    └── RISKS_AND_GAPS.md
```

---

## Authority Levels (Mandatory Tagging)

Every file/section must have explicit authority status:

- **CANONICAL**: Locked truth, overrides everything else
- **WORKING**: Current but not locked, subject to change
- **DRAFT**: Ideas, proposals, not authoritative
- **DEPRECATED**: Retained for history only, not used for recommendations

**Default Authority:**
- Phase-5 docs: CANONICAL if explicitly marked, else WORKING
- Chat mirror files: WORKING (must be promoted to become CANONICAL)
- Implementation scripts: WORKING
- Input snapshots: WORKING (versioned)

---

## Folder-Aware Latest-File Ingestion Rules

### Rule 1: Latest File Selection
- **Default**: Most recently modified file per folder
- **Override**: If folder contains a `FINAL`/`CANONICAL` marker, prefer that even if older
- **Ignore**: Drafts, temp, backup, `_old`, `copy`, `v0`, `.bak` files (configurable patterns)

### Rule 2: Folder Structure Preservation
- RAG understands full Phase-5 folder structure
- But ingests only latest authoritative file per folder
- Folder map (`00_FOLDER_MAP.md`) shows structure without ingesting junk

### Rule 3: No Direct Repo Indexing
- RAG never indexes `docs/PHASE_5/` directly
- All ingestion goes through curated `/RAG_KB/phase5_pack/`
- This ensures clean, fast, accurate retrieval

---

## Chat Mirror Integration

### Export Rule (ENFORCED)
Any chat that introduces a decision, structure, or strategy must be saved into `RAG_KB/chat_mirror/` before it is considered known by the project.

**Enforcement:**
- Pre-commit hook checks: If commit message contains "DECISION:", a chat_mirror file for today must exist
- CI/CD check: Phase 5 doc changes should trigger KB refresh
- Manual: Always export important chat decisions to `chat_mirror/YYYY-MM-DD_<topic>.md`

### File Format
Each chat mirror file must have metadata header:
```markdown
---
Source: ChatGPT Project Discussion
Date: YYYY-MM-DD
Phase: Phase-5 (or relevant phase)
Status: WORKING (default) | CANONICAL (if promoted)
Scope: Brief topic description
Authority: Informational (unless promoted)
---
```

### Promotion Process
- Chat mirror content is WORKING by default
- To become CANONICAL:
  1. Extract decision/rule into `02_DECISIONS_LOG.md`
  2. Update `01_CANONICAL_MASTER.md` with new content
  3. Mark chat mirror section as "Promoted to CANONICAL on YYYY-MM-DD"

---

## Update Policy

Any changes to Phase-5 docs, rules, feature flags, scripts, or inputs must trigger:

1. **Rebuild** of `01_CANONICAL_MASTER.md` (using locked format)
2. **Update** of `00_INDEX.json` (latest-only manifest)
3. **Update** of `00_FOLDER_MAP.md` (structure visualization)
4. **Update** of `DELTA_SINCE_LAST.md` (what changed)
5. **Re-index** for RAG (vector + keyword indexes)

### Trigger Events
- New commit in `docs/PHASE_5/` or `tools/catalog_pipeline_v2/`
- New file in `chat_mirror/`
- Manual refresh command: `kb_refresh`

---

## Locked Content Protection

### Immutability Rules
- CANONICAL sections in master file are **immutable**
- Updates to locked content must:
  - Create new version block (append-only)
  - Change lock status explicitly (via Decision Register)
  - Never overwrite in-place

### Version Blocking
Every update creates version metadata:
- `Version`
- `Date`
- `UpdatedBy` (system or user)
- `ChangeReason`

---

## RAG Container Architecture

### Container Separation (Performance + Safety)

1. **kb-indexer** (Background)
   - Reads `/RAG_KB/**`
   - Builds embeddings + keyword index
   - Writes to `/RAG_INDEX/` (separate from source)
   - Runs on schedule or file-change triggers

2. **kb-query** (Fast Response)
   - Serves endpoints: answer, cite, summarize, diff
   - Uses `/RAG_INDEX/` only (read-only)
   - No heavy indexing at query time

3. **kb-docbuilder** (Deterministic)
   - Regenerates `01_CANONICAL_MASTER.md` from repo evidence
   - Produces delta reports
   - Runs on refresh triggers

---

## Domain Boundaries

### What RAG Knows (NSW Estimation Scope Only)

1. **Phase-5 Documentation**
   - Execution plans, locked rules, checklists, ADRs
   - Governance policies, decision registers

2. **Catalog + Pricing Artifacts**
   - Normalized catalog XLSX exports
   - Source price list PDFs/XLSX (summaries)
   - Mapping rules, delta history

3. **Rules Engine Knowledge**
   - Make/Series policy tables
   - L1→L2 explosion rules
   - Bundling rules (built-in vs separate SKU)
   - Attribute KVU rules

4. **Implementation Artifacts**
   - Import scripts, seed scripts, migrations
   - Conversion scripts, rule evaluation code
   - Schema DDL, test data

5. **Telemetry (Future)**
   - User accept/reject signals
   - Override reasons, error types
   - Manual pricing events

### What RAG Does NOT Know
- External general knowledge (unless explicitly in chat mirror)
- Draft files without status tags
- Deprecated or archived content (unless tagged for history)

---

## Retrieval Weighting

RAG retrieval prioritizes by authority:
1. **CANONICAL** (highest weight)
2. **WORKING** (medium weight)
3. **DRAFT** (low weight, for context only)
4. **DEPRECATED** (excluded from recommendations, available for history)

Within same authority, recency matters (newer versions preferred).

---

## Citation Requirements

Every RAG response must include:
- **Source file**: Exact path relative to repo root
- **Section/heading**: Where the information comes from
- **Version**: KB version + source file version
- **Authority status**: CANONICAL/WORKING/DRAFT
- **Date**: When the source was last updated

Format: `[Source: docs/PHASE_5/00_GOVERNANCE/PHASE_5_CHARTER.md § Purpose | v1.0 | CANONICAL | 2025-01-27]`

---

## Continuous Improvement Loop

### Weekly Evaluation Metrics
- Top failure modes (suggestions rejected)
- Override rate (AI suggestions vs user choices)
- Manual pricing rate (should decrease over time)
- "Unknown mapping" count (catalog gaps)
- Precision/recall on golden question set

### KB Refresh Cadence
- **Automatic**: On commit/change triggers
- **Manual**: `kb_refresh` command anytime
- **Scheduled**: Daily at low-traffic time (optional)

---

## Change Log

- **v1.0** (2025-12-27): Initial rulebook creation, establishing RAG governance framework

---

## References

- Phase-5 governance approach (entry gates, locked rules, two-truth layers)
- Catalog + L1/L2 + make/series policy framework
- NSW v1.3 model principles (L1 intent + L2 SKU pricing, KVU attributes)
- Phase 5 goal: stable rule engine + repeatable price list import + future-proof AI layer

