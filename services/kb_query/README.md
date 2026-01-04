# KB Query Service

**Purpose:** Fast query API for RAG Knowledge Base

## Architecture

- **Input:** Reads from `RAG_INDEX/` (built by indexer)
- **Output:** Answers with citations (file + version + authority)

## API Endpoints

### POST /query
Query the knowledge base

**Request:**
```json
{
  "query": "What are the Phase 5 governance rules?",
  "namespace": "phase5_docs",  // optional filter
  "authority": "CANONICAL",    // optional filter
  "limit": 10
}
```

**Response:**
```json
{
  "answer": "...",
  "citations": [
    {
      "file": "docs/PHASE_5/00_GOVERNANCE/PHASE_5_CHARTER.md",
      "section": "Purpose",
      "authority": "CANONICAL",
      "version": "1.0",
      "last_modified": "2025-01-27"
    }
  ],
  "kb_version": "1.0",
  "index_version": "0.1"
}
```

## Implementation

- Fast retrieval from pre-built indexes
- Hybrid search (keyword + vector)
- Citation requirements enforced
- Namespace/authority filtering

## Usage

```bash
# Start query service
python3 services/kb_query/query_server.py --port 8000

# Or use as library
from kb_query import QueryService
service = QueryService()
results = service.query("your question")
```

