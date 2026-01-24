# Fix for start_all_with_rag.sh - Orphan Container Warnings

## Problem
The script shows warnings about orphan containers:
- `nsw_kb_indexer_decisions`
- `nsw_kb_query_decisions`  
- `nsw_postgres`
- `nsw_kb_indexer`
- `nsw_kb_query`

These warnings occur because Docker Compose detects containers that are no longer defined in the compose files.

## Solution
Add the `--remove-orphans` flag to Docker Compose commands.

## Changes Required

Update `/Users/nirajdesai/bin/start_all_with_rag.sh` with these two changes:

### Change 1: Line ~60 (RAG Query startup)
**Find:**
```bash
docker compose -f docker-compose.rag.yml --profile rag up -d
```

**Replace with:**
```bash
docker compose -f docker-compose.rag.yml --profile rag up -d --remove-orphans
```

### Change 2: Line ~85 (PostgreSQL startup)
**Find:**
```bash
docker compose --profile db up -d postgres
```

**Replace with:**
```bash
docker compose --profile db up -d --remove-orphans postgres
```

## Quick Fix Command

Run this to update your script automatically:

```bash
# Backup first
cp /Users/nirajdesai/bin/start_all_with_rag.sh /Users/nirajdesai/bin/start_all_with_rag.sh.backup

# Apply fixes
sed -i '' 's|docker compose -f docker-compose.rag.yml --profile rag up -d|docker compose -f docker-compose.rag.yml --profile rag up -d --remove-orphans|g' /Users/nirajdesai/bin/start_all_with_rag.sh
sed -i '' 's|docker compose --profile db up -d postgres|docker compose --profile db up -d --remove-orphans postgres|g' /Users/nirajdesai/bin/start_all_with_rag.sh
```

## Or Copy the Fixed Version

A fixed version is available at:
```
/Volumes/T9/Projects/NSW_Estimation_Software/scripts/start_all_with_rag_FIXED.sh
```

Copy it to replace your current script:
```bash
cp /Volumes/T9/Projects/NSW_Estimation_Software/scripts/start_all_with_rag_FIXED.sh /Users/nirajdesai/bin/start_all_with_rag.sh
chmod +x /Users/nirajdesai/bin/start_all_with_rag.sh
```

## What This Does

The `--remove-orphans` flag tells Docker Compose to:
1. Remove containers that are no longer defined in the compose files
2. Clean up the orphaned containers automatically
3. Prevent the warning messages from appearing

## Result

After applying this fix, when you run "Start All With RAG" from your macOS Shortcuts:
- ✅ No more orphan container warnings
- ✅ Clean startup without error dialogs
- ✅ All services start properly
