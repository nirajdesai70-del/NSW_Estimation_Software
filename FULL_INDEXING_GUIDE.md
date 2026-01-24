# Full Indexing Guide

## Problem
The KB indexer was only indexing 104 files from the curated manifest (`00_INDEX.json`), but there are **1,131 markdown files** in the `RAG_KB` directory.

## Solution
Added a `--full` flag to the indexer that scans and indexes **ALL markdown files** in the `RAG_KB` directory, bypassing the curated manifest.

## How to Use Full Indexing

### Option 1: Direct Python Script (Recommended)
```bash
cd /Volumes/T9/Projects/NSW_Estimation_Software
python3 services/kb_indexer/indexer.py --rebuild --verbose --full
```

### Option 2: Use the Helper Script
```bash
/Volumes/T9/Projects/NSW_Estimation_Software/scripts/rebuild_kb_full.sh
```

### Option 3: Docker Compose with Environment Variable
```bash
cd /Volumes/T9/Projects/NSW_Estimation_Software
KB_INDEXER_FULL=1 docker compose -f docker-compose.rag.yml --profile index run --rm kb_indexer
```

### Option 4: Update Your macOS Shortcut Script

Update `/Users/nirajdesai/bin/rebuild_kb.sh` to add the `--full` flag:

**Change this line:**
```bash
docker compose -f "$COMPOSE" --profile index run --rm kb_indexer
```

**To this:**
```bash
KB_INDEXER_FULL=1 docker compose -f "$COMPOSE" --profile index run --rm kb_indexer
```

Or if you want to run it directly without Docker:
```bash
cd "$NSW_ROOT" || exit 1
python3 services/kb_indexer/indexer.py --rebuild --verbose --full
```

## What Gets Indexed

### Normal Mode (Default)
- Only files listed in `RAG_KB/phase5_pack/00_INDEX.json`
- Curated subset selected by `kb_refresh` script
- Currently: **104 files**

### Full Mode (`--full` flag)
- **ALL** markdown files in `RAG_KB` directory (recursive)
- Excludes: `_old`, `_copy`, `_backup`, `.git`, `__pycache__`, `build_reports`, etc.
- Currently: **~1,131 files**

## Expected Output

When running with `--full`, you should see:
```
============================================================
KB Indexer
============================================================
KB Version: 1.0-full
KB Last Refresh: 2026-01-13T...
Mode: FULL INDEXING (all markdown files)

Rebuilding all indexes...
Wiping existing index artifacts...

Scanning all markdown files in RAG_KB...
Found 1131 markdown files to index
Indexing documents...
Built chunk universe: XXXX chunks
...
Indexed XXXX chunks from 1131 files

============================================================
Indexing Complete!
============================================================
Keyword Index: XXXX documents
Vector Index: XXXX documents
```

## Files Modified

1. ✅ `services/kb_indexer/indexer.py` - Added `--full` flag and `scan_all_files()` method
2. ✅ `docker-compose.rag.yml` - Added support for `KB_INDEXER_FULL` environment variable
3. ✅ `scripts/rebuild_kb_full.sh` - Created helper script for full indexing

## Notes

- Full indexing will take longer than normal indexing (more files to process)
- The index will be larger (more chunks = more storage)
- All markdown files in `RAG_KB` will be searchable, not just curated ones
- You can still use normal mode (without `--full`) to index only the curated manifest
