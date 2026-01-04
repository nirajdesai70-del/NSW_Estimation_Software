# KB Indexer Service

**Purpose:** Build searchable indexes (vector + keyword) from RAG Knowledge Pack

## Architecture

- **Input:** `RAG_KB/phase5_pack/` and `RAG_KB/chat_mirror/`
- **Output:** `RAG_INDEX/` (separate from source KB)

## Indexing Strategy

### Hybrid Retrieval (Recommended)

1. **Keyword Index** (Fast, exact matches)
   - SQLite FTS5 (Full-Text Search)
   - BM25 ranking
   - Fast for exact terms, file paths, etc.

2. **Vector Index** (Semantic similarity)
   - Local: FAISS or SQLite with embeddings
   - Scalable: Postgres + pgvector (future)
   - Good for semantic queries

### Implementation Options

**Option A: SQLite-based (Fastest to start)**
- FTS5 for keyword search
- Vector store using SQLite + extension or FAISS
- Zero infrastructure, fast for single-machine

**Option B: Postgres + pgvector (Better governance)**
- Full-text search via Postgres
- pgvector for embeddings
- Shared KB across multiple users/devices

## Structure

```
services/kb_indexer/
├── indexer.py          # Main indexer logic
├── keyword_index.py    # Keyword/FTS indexing
├── vector_index.py     # Embedding/vector indexing
├── config.py           # Configuration
└── requirements.txt    # Dependencies
```

## Usage

```bash
# Build indexes
python3 services/kb_indexer/indexer.py --rebuild

# Incremental update
python3 services/kb_indexer/indexer.py --update
```

## Next Steps

1. Implement keyword index (SQLite FTS5)
2. Implement vector index (FAISS or pgvector)
3. Add chunking strategy for long documents
4. Add namespace/authority filtering
5. Version the index alongside KB version

