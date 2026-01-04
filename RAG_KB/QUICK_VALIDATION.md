# Quick RAG Validation - Run These Commands

## Option 1: Use the Validation Script

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software
./validate_rag_setup.sh
```

## Option 2: Manual Commands

### 1. Enable Feature Flags

```bash
cd /Users/nirajdesai/Projects/NSW_Estimation_Software

# Add or update in .env file
echo "RAG_UI_ENABLED=true" >> .env
echo "RAG_EXPLAIN_WHY_ENABLED=true" >> .env

# Or edit .env manually and add:
# RAG_UI_ENABLED=true
# RAG_EXPLAIN_WHY_ENABLED=true
```

### 2. Clear Config Cache

```bash
php artisan config:clear
```

### 3. Check kb_query Service

```bash
# Try localhost first
curl http://localhost:8099/health

# If using Docker, try:
curl http://kb_query:8099/health

# Or from within docker container:
docker exec -it <container_name> curl http://kb_query:8099/health
```

**Expected response:**
```json
{"status":"ok"}
```

### 4. Access Test Harness

Open in browser:
```
http://localhost:8000/examples/rag-catalog
```
(Adjust port if your Laravel app uses a different port)

### 5. Test Checklist

- [ ] Type 12+ characters in description field
- [ ] "Ask RAG for Suggestions" button appears
- [ ] Click button → drawer opens with loading spinner
- [ ] Answer appears in drawer
- [ ] Citations list appears with authority badges
- [ ] Best authority badge shows in drawer header
- [ ] Footer shows KB version, index version, and latency
- [ ] "Explain why" button works independently
- [ ] Stop kb_query → graceful error message
- [ ] Spam click 40 times → throttle kicks in (429/503)

## Troubleshooting

### .env file not found
- Create `.env` file from `.env.example` if it exists
- Or manually create `.env` in project root

### artisan command not found
- Make sure you're in the Laravel project root
- Check if `artisan` file exists: `ls -la artisan`

### kb_query not reachable
- Check if service is running: `docker-compose ps`
- Check service logs: `docker-compose logs kb_query`
- Verify port 8099 is not blocked

### Route not found (404)
- Make sure routes are loaded: `php artisan route:list | grep rag`
- Check if route file is included in `RouteServiceProvider` or `bootstrap/app.php`

## Expected Test Results

### Successful Query Response:
```json
{
  "answer": "Based on the product description...",
  "citations": [
    {
      "kb_path": "phase5_pack/...",
      "source_path": "...",
      "title": "...",
      "authority": "CANONICAL",
      "last_modified": "...",
      "score": 0.85
    }
  ],
  "best_authority": "CANONICAL",
  "kb_version": "2025-01-XX",
  "index_version": "v1.0",
  "latency_ms": 234
}
```

### Error Response (Service Down):
```json
{
  "answer": "RAG service is currently unavailable. Please try again later.",
  "citations": [],
  "kb_version": "unknown",
  "index_version": "unknown",
  "latency_ms": 123
}
```

## Report Back

After testing, provide:
1. ✅ One successful response JSON (trim citations if long)
2. ❌ Any errors encountered (if any)
3. ✅ Checklist completion status

