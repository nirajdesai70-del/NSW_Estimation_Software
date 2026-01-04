# RAG Implementation Guide

**Version:** 1.0  
**Date:** 2025-12-27  
**Purpose:** Step-by-step guide to implement and use the RAG system

---

## Overview

This guide walks you through implementing and using the RAG (Retrieval Augmented Generation) system for NSW Estimation Phase 5.

**Three Connection Points:**
1. **Repo → KB Pack** (Refresh runner) ✅ Implemented
2. **KB Pack → Index** (Indexer) 🔨 Skeleton ready
3. **Index → Query** (Query service) 🔨 Skeleton ready

---

## Phase 1: First KB Refresh (Do This First)

### Prerequisites
- Python 3.7+
- Phase 5 documentation exists in `docs/PHASE_5/`

### Step 1.1: Dry Run

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
python3 tools/kb_refresh/run_kb_refresh.py --dry-run --verbose
```

**Expected:** See list of files that would be processed

### Step 1.2: Actual Refresh

```bash
python3 tools/kb_refresh/run_kb_refresh.py
```

**Expected Outputs:**
- `RAG_KB/phase5_pack/00_INDEX.json` - File manifest
- `RAG_KB/phase5_pack/00_FOLDER_MAP.md` - Folder structure
- `RAG_KB/phase5_pack/04_RULES_LIBRARY/` - Copied files with metadata
- `RAG_KB/build_reports/DELTA_SINCE_LAST.md` - Change report

### Step 1.3: Verify

```bash
# Check index
cat RAG_KB/phase5_pack/00_INDEX.json | jq '.statistics'

# Check folder map
head -50 RAG_KB/phase5_pack/00_FOLDER_MAP.md

# Check delta
cat RAG_KB/build_reports/DELTA_SINCE_LAST.md
```

**If Issues:**
- Check `tools/kb_refresh/run_kb_refresh.py` line 30-60 (SCAN_ROOTS config)
- Verify Phase 5 paths exist
- Run with `--verbose` for detailed output

---

## Phase 2: Implement Keyword Indexing

### Step 2.1: Install Dependencies

```bash
# SQLite3 is built-in, no install needed
# But you may want to add for progress bars:
pip install tqdm
```

### Step 2.2: Implement Keyword Index

Edit `services/kb_indexer/keyword_index.py`:

1. **Implement `create_tables()`:**
   ```python
   def create_tables(self):
       cursor = self.conn.cursor()
       cursor.execute("""
           CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(
               content,
               title,
               file_path,
               namespace,
               authority,
               kb_path,
               last_modified
           );
       """)
       self.conn.commit()
   ```

2. **Implement `add_document()`:**
   ```python
   def add_document(self, doc_id: str, content: str, metadata: Dict):
       cursor = self.conn.cursor()
       cursor.execute("""
           INSERT INTO documents (
               content, title, file_path, namespace, authority, kb_path, last_modified
           ) VALUES (?, ?, ?, ?, ?, ?, ?)
       """, (
           content,
           metadata.get('filename', ''),
           metadata.get('source_path', ''),
           metadata.get('namespace', ''),
           metadata.get('authority', 'WORKING'),
           metadata.get('kb_path', ''),
           metadata.get('last_modified', '')
       ))
       self.conn.commit()
   ```

3. **Implement `search()`:**
   ```python
   def search(self, query: str, limit: int = 10) -> List[Dict]:
       cursor = self.conn.cursor()
       cursor.execute("""
           SELECT 
               file_path, namespace, authority, kb_path, last_modified,
               bm25(documents) as rank
           FROM documents
           WHERE documents MATCH ?
           ORDER BY rank
           LIMIT ?
       """, (query, limit))
       
       results = []
       for row in cursor.fetchall():
           results.append({
               'file_path': row[0],
               'namespace': row[1],
               'authority': row[2],
               'kb_path': row[3],
               'last_modified': row[4],
               'rank': row[5]
           })
       return results
   ```

### Step 2.3: Wire Up Indexer

Edit `services/kb_indexer/indexer.py`:

1. Import keyword index:
   ```python
   from keyword_index import KeywordIndex
   ```

2. In `index_documents()`, add:
   ```python
   index_path = self.index_root / "keyword_index.db"
   with KeywordIndex(index_path) as ki:
       ki.create_tables()
       
       for file_entry in files:
           kb_path = KB_PACK_ROOT / file_entry['kb_path']
           if kb_path.exists():
               with open(kb_path, 'r') as f:
                   content = f.read()
               ki.add_document(
                   file_entry['kb_path'],
                   content,
                   file_entry
               )
   ```

### Step 2.4: Test

```bash
python3 services/kb_indexer/indexer.py --rebuild --verbose
```

**Expected:** Keyword index database created at `RAG_INDEX/keyword_index.db`

---

## Phase 3: Implement Query Service

### Step 3.1: Install Dependencies

```bash
pip install flask
```

### Step 3.2: Wire Up Query Service

Edit `services/kb_query/query_service.py`:

1. Import keyword index:
   ```python
   from pathlib import Path
   import sys
   sys.path.append(str(Path(__file__).parent.parent / "kb_indexer"))
   from keyword_index import KeywordIndex
   ```

2. In `__init__`, initialize keyword index:
   ```python
   keyword_index_path = self.index_root / "keyword_index.db"
   if keyword_index_path.exists():
       self.keyword_index = KeywordIndex(keyword_index_path)
   ```

3. In `query()`, use keyword search:
   ```python
   results = self.search_keyword(query_text, limit=limit * 2)  # Get more for filtering
   
   # Filter by namespace/authority if specified
   if namespace:
       results = [r for r in results if r.get('namespace') == namespace]
   if authority:
       results = [r for r in results if r.get('authority') == authority]
   
   # Limit results
   results = results[:limit]
   
   # Generate answer (simplified - you'll enhance this)
   answer_parts = []
   citations = []
   
   for result in results:
       citations.append(self.format_citation(result))
       answer_parts.append(f"Found in {result['file_path']}")
   
   return {
       "answer": "\n".join(answer_parts),
       "citations": citations,
       "kb_version": self._get_kb_version(),
       "index_version": self._get_index_version(),
   }
   ```

### Step 3.3: Test Query Service

```bash
# CLI test
python3 services/kb_query/query_service.py "What is Phase 5 scope?"

# Server test
python3 services/kb_query/query_server.py --port 8000

# In another terminal:
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are Phase 5 governance rules?"}'
```

---

## Phase 4: Vector Indexing (Optional, Advanced)

### Step 4.1: Choose Backend

**Option A: FAISS (Local, Fast)**
```bash
pip install faiss-cpu sentence-transformers
```

**Option B: pgvector (Postgres, Shared)**
```bash
# Requires Postgres setup with pgvector extension
pip install pgvector psycopg2 sentence-transformers
```

### Step 4.2: Implement Vector Index

Edit `services/kb_indexer/vector_index.py`:

1. **For FAISS:**
   ```python
   import faiss
   import numpy as np
   from sentence_transformers import SentenceTransformer
   
   class VectorIndex:
       def __init__(self, index_path: Path, backend: str = "faiss"):
           self.index_path = index_path
           self.model = SentenceTransformer('all-MiniLM-L6-v2')
           self.index = None
           self.id_to_metadata = {}
           
       def initialize(self):
           dimension = 384  # all-MiniLM-L6-v2 dimension
           self.index = faiss.IndexFlatL2(dimension)
           
       def generate_embedding(self, text: str) -> np.ndarray:
           return self.model.encode(text)
           
       def add_document(self, doc_id: str, embedding: List[float], metadata: Dict):
           embedding_array = np.array([embedding], dtype='float32')
           self.index.add(embedding_array)
           self.id_to_metadata[self.index.ntotal - 1] = metadata
           
       def search(self, query_embedding: np.ndarray, limit: int = 10) -> List[Dict]:
           distances, indices = self.index.search(query_embedding, limit)
           results = []
           for idx, dist in zip(indices[0], distances[0]):
               if idx in self.id_to_metadata:
                   results.append({
                       **self.id_to_metadata[idx],
                       'distance': float(dist)
                   })
           return results
   ```

2. Wire up in `indexer.py` (similar to keyword index)

### Step 4.3: Hybrid Search

In `query_service.py`, combine keyword + vector:

```python
def query(self, ...):
    # Get keyword results
    keyword_results = self.search_keyword(query_text, limit=limit)
    
    # Get vector results
    query_embedding = self.vector_index.generate_embedding(query_text)
    vector_results = self.vector_index.search(query_embedding, limit=limit)
    
    # Merge and rank (simple: union, prefer keyword for exact matches)
    combined = {r['kb_path']: r for r in keyword_results}
    for r in vector_results:
        if r['kb_path'] not in combined:
            combined[r['kb_path']] = r
    
    results = list(combined.values())[:limit]
    # ... format response
```

---

## Phase 5: Automation & CI/CD

### Step 5.1: Pre-commit Hook (Already Created)

The hook is at `.git/hooks/pre-commit`. It checks:
- Phase 5 doc changes → warns if delta not updated
- "DECISION:" in commit → requires chat_mirror file

**To install:**
```bash
chmod +x .git/hooks/pre-commit
```

**To test:**
```bash
tools/kb_refresh/pre-commit-check.sh
```

### Step 5.2: CI Workflow (Optional)

Create `.github/workflows/kb_refresh.yml`:

```yaml
name: KB Refresh

on:
  push:
    paths:
      - 'docs/PHASE_5/**'
      - 'tools/catalog_pipeline_v2/**'

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run KB Refresh
        run: |
          python3 tools/kb_refresh/run_kb_refresh.py
      - name: Commit Changes
        run: |
          git config user.name "KB Refresh Bot"
          git config user.email "bot@example.com"
          git add RAG_KB/
          git commit -m "Auto: KB refresh after Phase 5 changes" || exit 0
          git push || exit 0
```

---

## Troubleshooting

### Refresh Script

**"No files found"**
- Check `SCAN_ROOTS` configuration matches your repo
- Verify Phase 5 paths exist

**"Permission denied"**
- Make script executable: `chmod +x tools/kb_refresh/run_kb_refresh.py`

### Indexer

**"Keyword index DB locked"**
- Close any other processes using the database
- Check file permissions

**"No module named 'faiss'"**
- Install: `pip install faiss-cpu`

### Query Service

**"Index not found"**
- Run indexer first: `python3 services/kb_indexer/indexer.py --rebuild`

**"Empty results"**
- Check index was built correctly
- Verify KB pack has content

---

## Next Steps

1. ✅ Run first KB refresh
2. ✅ Implement keyword indexing
3. ✅ Test query service
4. ⏳ Implement vector indexing (optional)
5. ⏳ Set up CI/CD automation
6. ⏳ Add telemetry capture (future)
7. ⏳ Add evaluation metrics (future)

---

## References

- **Setup**: `RAG_KB/SETUP_COMPLETE.md`
- **Connections**: `RAG_KB/CONNECTIONS_COMPLETE.md`
- **Rulebook**: `RAG_KB/RAG_RULEBOOK.md`
- **Refresh Spec**: `RAG_KB/kb_refresh.md`

