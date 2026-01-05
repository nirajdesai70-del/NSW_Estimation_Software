# Phase-3 RAG KB Updates

**Date:** 2026-01-05  
**Version:** rag-kb-v1.0-bm25-sha256  
**Status:** ✅ COMPLETE

---

## Summary

Phase-3 RAG KB updates implement deterministic BM25 indexing with strict SHA256 content hashing and atomic metadata persistence. This ensures reproducible builds and eliminates mtime-based fallback behavior.

---

## Key Changes

### 1. Strict SHA256 Content Hashing
- **Before:** Used file modification time (mtime) as fallback for content change detection
- **After:** Strict SHA256 content hashing only (no mtime fallback)
- **Impact:** Deterministic behavior, reproducible builds

### 2. BM25 Dirty Flag + Deterministic Rebuild
- **Dirty flag:** Tracks when index needs rebuild (`_dirty` flag)
- **Rebuild trigger:** Rebuild happens on `close()` if dirty flag is set
- **Deterministic ordering:** Corpus and doc_ids are sorted by doc_id for consistent ordering
- **Impact:** Rebuilds only when needed, consistent index structure

### 3. Atomic Metadata Save
- **Method:** `_save_metadata_atomic()`
- **Process:** Write to temp file → fsync → atomic rename
- **Location:** `{index_path.stem}_metadata.json` (e.g., `keyword_index_metadata.json`)
- **Impact:** Prevents corruption from partial writes

### 4. Response Field: `keyword_backend`
- **New field:** Query responses now include `keyword_backend: "bm25"`
- **Purpose:** Indicates which backend is being used for keyword search
- **Impact:** API consumers can detect backend type

---

## Index Metadata File Location

**File:** `RAG_INDEX/keyword_index_metadata.json`

**Structure:**
```json
{
  "metadata": { "doc_id": {...} },
  "doc_ids": [...],
  "corpus": [...],
  "updated_at": "ISO timestamp"
}
```

**Note:** Metadata is persisted alongside the BM25 index structure (corpus + doc_ids) for fast loading.

---

## Usage Commands

### Refresh KB (Update Content)
```bash
python3 tools/kb_refresh/run_kb_refresh.py
```
- Updates KB pack from source
- Regenerates `RAG_KB/phase5_pack/00_INDEX.json`
- Uses strict SHA256 for change detection

### Rebuild Index
```bash
cd services/kb_indexer
python3 indexer.py --rebuild
```
- Wipes existing index artifacts
- Rebuilds BM25 and vector indexes from scratch
- Deterministic ordering (sorted by doc_id)

### Update Index (Incremental)
```bash
cd services/kb_indexer
python3 indexer.py --update
```
- Adds/updates documents incrementally
- Uses dirty flag for deferred rebuild
- Atomic save on close()

### Smoke Query Test
```bash
# Start query service
cd services/kb_query
python3 query_server.py

# Test query (in another terminal)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "top_k": 5}'

# Response includes keyword_backend field
```

---

## Response Format

Query responses now include:

```json
{
  "results": [...],
  "keyword_backend": "bm25",
  "stats": {...}
}
```

**Field:** `keyword_backend`  
**Value:** `"bm25"` (indicates rank-bm25 library is used)  
**Purpose:** Allows API consumers to detect backend type

---

## Technical Details

### Dirty Flag Behavior
- Set when documents are added/updated
- Triggers rebuild on `close()` if dirty
- Otherwise saves metadata atomically

### Deterministic Ordering
- `doc_ids` and `corpus` are sorted by `doc_id` on load
- Ensures consistent index structure across rebuilds
- Prevents non-deterministic ordering issues

### Atomic Save Process
1. Write data to `{filename}.tmp`
2. Call `fsync()` to ensure write to disk
3. Atomic rename: `{filename}.tmp` → `{filename}`
4. Prevents partial/corrupted metadata files

---

## Migration Notes

**No migration required** — changes are backward compatible:
- Existing metadata files load correctly
- Old indexes continue to work
- New indexes use improved persistence

**Recommendation:** Run `--rebuild` once to benefit from deterministic ordering.

---

**Tag:** `rag-kb-v1.0-bm25-sha256`  
**Commit:** See git log for implementation details

