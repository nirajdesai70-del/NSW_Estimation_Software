# RAG Knowledge Base — NSW Estimation Phase 5

**Version:** 1.0  
**Date:** 2025-12-27  
**Status:** ACTIVE

---

## Overview

This is the curated Knowledge Base (KB) for the RAG (Retrieval Augmented Generation) system supporting NSW Estimation Software Phase 5. The KB serves as the single source of truth for RAG, ensuring AI assistance is grounded in canonical Phase 5 knowledge.

---

## Structure

```
RAG_KB/
├── RAG_RULEBOOK.md              # Governance rules for RAG KB
├── kb_refresh.md                # Instructions for refreshing KB
├── phase5_pack/                 # Curated knowledge pack (RAG indexes this)
│   ├── 00_INDEX.json            # File manifest (latest-only per folder)
│   ├── 00_FOLDER_MAP.md         # Human-readable folder structure
│   ├── 01_CANONICAL_MASTER.md   # Single structured master (auto-generated)
│   ├── 02_DECISIONS_LOG.md      # Locked decisions + rationale
│   ├── 03_FEATURE_FLAGS.md      # Feature flags registry
│   ├── 04_RULES_LIBRARY/        # Rules organized by domain
│   ├── 05_IMPLEMENTATION_NOTES/ # Scripts, migrations, converters
│   ├── 06_INPUT_SNAPSHOTS/      # Catalog/price list summaries
│   └── 07_TRACKERS_EXPORT/      # Tracker summaries
├── chat_mirror/                 # Exported ChatGPT conversations
│   └── 2025-12-27_phase5_rag_strategy.md
└── build_reports/               # KB refresh outputs
    ├── DELTA_SINCE_LAST.md
    └── RISKS_AND_GAPS.md
```

---

## Golden Rule

**RAG indexes ONLY `/RAG_KB/` (curated).**  
**No direct indexing of entire repo.**

---

## Quick Start

### First Time Setup

1. **Review Rulebook:** Read `RAG_RULEBOOK.md` to understand governance
2. **Run First Refresh:** Execute `kb_refresh` process (see `kb_refresh.md`)
3. **Validate Output:** Check `phase5_pack/01_CANONICAL_MASTER.md` matches latest Phase 5 format
4. **Review Gaps:** Check `build_reports/RISKS_AND_GAPS.md` for missing sources

### Ongoing Operations

- **Manual Refresh:** Run `kb_refresh` after major Phase 5 milestones
- **Chat Export:** Export important ChatGPT conversations to `chat_mirror/`
- **Review Delta:** Check `build_reports/DELTA_SINCE_LAST.md` after each refresh

---

## Key Concepts

### Authority Levels
- **CANONICAL**: Locked truth, highest authority
- **WORKING**: Current but not locked
- **DRAFT**: Ideas, not authoritative
- **DEPRECATED**: Historical only

### Latest-File Ingestion
- RAG understands full Phase 5 folder structure
- But ingests only latest authoritative file per folder
- Prevents junk/draft pollution

### Chat Mirror Learning
- ChatGPT conversations exported to `chat_mirror/`
- Default status: WORKING
- Must be promoted to CANONICAL via Decisions Log

---

## Documentation

- **`RAG_RULEBOOK.md`**: Complete governance framework
- **`kb_refresh.md`**: Step-by-step refresh instructions
- **`phase5_pack/00_FOLDER_MAP.md`**: Folder structure visualization
- **`phase5_pack/01_CANONICAL_MASTER.md`**: Single source of truth (auto-generated)

---

## Integration with RAG System

### Indexer Container
- Reads `/RAG_KB/phase5_pack/` only
- Builds embeddings + keyword index
- Writes to `/RAG_INDEX/` (separate from source)

### Query Container
- Uses `/RAG_INDEX/` for fast retrieval
- Returns answers with citations (file + version + authority)

### Doc Builder Container
- Regenerates `01_CANONICAL_MASTER.md` from repo evidence
- Produces delta reports on refresh triggers

---

## Change Log

- **v1.0** (2025-12-27): Initial RAG KB structure created with rulebook, refresh instructions, and placeholder files

---

## Next Steps

1. ✅ Structure created
2. ✅ Rulebook documented
3. ✅ Chat conversation uploaded
4. ⏳ **Run first kb_refresh** (next action)
5. ⏳ Validate master consolidation
6. ⏳ Set up RAG containers (indexer/query/doc-builder)

---

## References

- Phase 5 Charter: `docs/PHASE_5/00_GOVERNANCE/PHASE_5_CHARTER.md`
- NSW Master Plan: `docs/NSW_ESTIMATION_MASTER.md`
- Catalog Pipeline: `tools/catalog_pipeline_v2/README.md`

