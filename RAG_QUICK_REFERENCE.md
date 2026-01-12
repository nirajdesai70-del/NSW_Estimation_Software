# RAG Quick Reference Guide

## Where RAG is Working

### 1. **RAG Service Paths**

#### Backend Service (Python)
- **Service Location**: `services/kb_query/`
  - `query_server.py` - Main HTTP server
  - `query_service.py` - Query logic with hybrid search
- **Default URL**: `http://kb_query:8099` (Docker) or `http://localhost:8099` (local)
- **Health Endpoint**: `http://localhost:8099/health`
- **Query Endpoint**: `http://localhost:8099/query`

#### Laravel Integration (PHP)
- **Service Class**: `app/Services/RagQueryService.php`
- **Controller**: `app/Http/Controllers/RagController.php`
- **Routes**: `routes/rag.php`
- **Config**: `config/rag.php`

#### Knowledge Base
- **KB Source**: `RAG_KB/` directory
- **Index Storage**: `RAG_INDEX/` directory
  - `keyword_index.db` - BM25 keyword index
  - `vector_index.faiss` - FAISS vector index
  - `vector_index.faiss.metadata.json` - Vector metadata
  - `index_metadata.json` - Index metadata

#### Docker Configuration
- **Docker Compose**: `docker-compose.rag.yml`
- **Service Name**: `kb_query`
- **Port Mapping**: `8011:8099` (host:container)

---

## How to Check if RAG is Working

### Method 1: Quick Health Check (Recommended)

```bash
# Check if the RAG service is running
curl http://localhost:8099/health
```

**Expected Response:**
```json
{"status":"ok"}
```

**If you get an error:**
- Service might not be running
- Check Docker: `docker-compose ps` (look for `kb_query` service)
- Check logs: `docker-compose logs kb_query`

---

### Method 2: Use the Validation Script

```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software
./validate_rag_setup.sh
```

This script will:
1. Enable RAG feature flags in `.env`
2. Clear Laravel config cache
3. Check `kb_query` service health
4. Show route information

---

### Method 3: Test via Laravel API

#### Step 1: Enable Feature Flags
Add to your `.env` file:
```env
RAG_UI_ENABLED=true
RAG_EXPLAIN_WHY_ENABLED=true
RAG_QUERY_SERVICE_URL=http://localhost:8099
```

#### Step 2: Clear Config Cache
```bash
php artisan config:clear
```

#### Step 3: Test the API Endpoint
```bash
# Make sure you're authenticated first, then:
curl -X POST http://localhost:8000/ui/rag/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "What is the catalog structure?",
    "context": {"screen": "catalog"},
    "top_k": 5
  }'
```

**Expected Response:**
```json
{
  "answer": "Based on the knowledge base...",
  "citations": [...],
  "kb_version": "...",
  "index_version": "...",
  "latency_ms": 123
}
```

---

### Method 4: Test via Browser UI

1. **Start the RAG service** (if using Docker):
   ```bash
   docker-compose -f docker-compose.rag.yml up -d kb_query
   ```

2. **Access the test harness**:
   ```
   http://localhost:8000/examples/rag-catalog
   ```
   (Requires authentication)

3. **Test Checklist**:
   - [ ] Type 12+ characters in description field
   - [ ] "Ask RAG for Suggestions" button appears
   - [ ] Click button → drawer opens with loading spinner
   - [ ] Answer appears in drawer
   - [ ] Citations list appears with authority badges
   - [ ] Best authority badge shows in drawer header
   - [ ] Footer shows KB version, index version, and latency

---

### Method 5: Check Service Status

#### Check if Docker service is running:
```bash
docker-compose -f docker-compose.rag.yml ps
```

#### Check service logs:
```bash
docker-compose -f docker-compose.rag.yml logs kb_query
```

#### Check if port is accessible:
```bash
# Check if port 8099 is listening
lsof -i :8099
# or
netstat -an | grep 8099
```

---

### Method 6: Test Direct Python Service

If running the Python service directly (not Docker):

```bash
cd /Volumes/T9/Projects/Projects/NSW_Estimation_Software
python3 services/kb_query/query_server.py --port 8099 --host 0.0.0.0
```

Then in another terminal:
```bash
curl http://localhost:8099/health
curl -X POST http://localhost:8099/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "top_k": 5}'
```

---

## Troubleshooting

### RAG Service Not Responding

1. **Check if service is running:**
   ```bash
   docker-compose -f docker-compose.rag.yml ps
   ```

2. **Start the service:**
   ```bash
   docker-compose -f docker-compose.rag.yml up -d kb_query
   ```

3. **Check service logs:**
   ```bash
   docker-compose -f docker-compose.rag.yml logs -f kb_query
   ```

4. **Verify index files exist:**
   ```bash
   ls -lh RAG_INDEX/
   ```
   Should see:
   - `keyword_index.db`
   - `vector_index.faiss`
   - `vector_index.faiss.metadata.json`
   - `index_metadata.json`

### Laravel Can't Connect to RAG Service

1. **Check `.env` configuration:**
   ```env
   RAG_QUERY_SERVICE_URL=http://localhost:8099
   # or if using Docker network:
   RAG_QUERY_SERVICE_URL=http://kb_query:8099
   ```

2. **Clear Laravel config cache:**
   ```bash
   php artisan config:clear
   ```

3. **Check Laravel logs:**
   ```bash
   tail -f storage/logs/laravel.log
   ```

### Index Files Missing

If `RAG_INDEX/` is empty or missing files:

1. **Rebuild the index:**
   ```bash
   docker-compose -f docker-compose.rag.yml run --rm kb_indexer
   ```

2. **Or run indexer directly:**
   ```bash
   python3 services/kb_indexer/indexer.py --rebuild --verbose
   ```

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `config/rag.php` | Laravel RAG configuration |
| `docker-compose.rag.yml` | Docker service definitions |
| `services/kb_query/query_server.py` | Python HTTP server |
| `services/kb_query/query_service.py` | Query logic |
| `app/Services/RagQueryService.php` | Laravel service wrapper |
| `routes/rag.php` | API routes |

---

## Quick Status Check Command

Run this to get a complete status:

```bash
echo "=== RAG Service Status ===" && \
echo "1. Health Check:" && \
curl -s http://localhost:8099/health || echo "❌ Service not reachable" && \
echo "" && \
echo "2. Docker Status:" && \
docker-compose -f docker-compose.rag.yml ps kb_query 2>/dev/null || echo "❌ Docker not running or service not found" && \
echo "" && \
echo "3. Index Files:" && \
ls -lh RAG_INDEX/*.{db,faiss,json} 2>/dev/null | wc -l | xargs echo "Index files found:" && \
echo "" && \
echo "4. Laravel Config:" && \
grep -E "RAG_UI_ENABLED|RAG_QUERY_SERVICE_URL" .env 2>/dev/null || echo "❌ .env not found or RAG config missing"
```

---

## Summary

**RAG is working under these paths:**
- **Service**: `services/kb_query/` (Python service on port 8099)
- **Integration**: `app/Services/RagQueryService.php` (Laravel wrapper)
- **Routes**: `routes/rag.php` → `/ui/rag/query`
- **Knowledge Base**: `RAG_KB/` (source) → `RAG_INDEX/` (indexed)

**To check if RAG is working:**
1. ✅ Run: `curl http://localhost:8099/health` → Should return `{"status":"ok"}`
2. ✅ Or run: `./validate_rag_setup.sh` → Automated validation
3. ✅ Or test via browser: `http://localhost:8000/examples/rag-catalog`





