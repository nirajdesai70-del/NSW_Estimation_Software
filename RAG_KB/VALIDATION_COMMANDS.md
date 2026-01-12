# RAG UI Validation - Quick Commands

## Step 1: Enable Feature Flags

```bash
# Add to .env file
echo "RAG_UI_ENABLED=true" >> .env
echo "RAG_EXPLAIN_WHY_ENABLED=true" >> .env

# Clear config cache
php artisan config:clear
```

Or manually edit `.env`:
```env
RAG_UI_ENABLED=true
RAG_EXPLAIN_WHY_ENABLED=true
```

## Step 2: Verify kb_query Service

### If using Docker:
```bash
# From host machine
curl http://localhost:8099/health

# Or from within docker network
docker exec -it <container_name> curl http://kb_query:8099/health
```

### If running locally:
```bash
curl http://localhost:8099/health
```

**Expected response:**
```json
{"status":"ok"}
```

## Step 3: Access Test Harness

Navigate to:
```
http://your-app-url/examples/rag-catalog
```

(Requires authentication)

## Step 4: UX Checklist

- [ ] Type 12+ chars → "Ask RAG for Suggestions" button appears
- [ ] Click button → drawer opens + loading spinner shows
- [ ] Answer appears in drawer
- [ ] Citations appear with authority badges (CANONICAL/WORKING/DRAFT)
- [ ] Header shows best authority badge
- [ ] Footer shows KB version, index version, and latency
- [ ] "Explain why" button works independently
- [ ] Stop kb_query service → graceful error message appears
- [ ] Spam click 40 times → throttle kicks in (429 or 503)

## Step 5: Test Error Handling

### Test Service Down:
```bash
# Stop kb_query service
docker-compose stop kb_query
# or
pkill -f kb_query
```

Then try query → should show graceful error message.

### Test Rate Limiting:
Rapidly click "Ask RAG" button 40+ times → should see throttle response after 30 requests.

## Expected Response Format

### Successful Response:
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
  "latency_ms": 123,
  "error": "..."
}
```

### Rate Limit Response:
HTTP 429 Too Many Requests (or 503 if handled by adapter)

## Troubleshooting

### Drawer doesn't open
- Check browser console (F12)
- Verify Bootstrap 5 is loaded
- Check `rag-ui.js` is loaded (Network tab)

### No response from RAG
- Check Laravel logs: `storage/logs/laravel.log`
- Verify `/ui/rag/query` endpoint: `curl -X POST http://your-app-url/ui/rag/query -H "Content-Type: application/json" -d '{"query":"test","top_k":5}'`
- Check `kb_query` service logs

### CSRF errors
- Verify `<meta name="csrf-token">` in page source
- Check browser console for CSRF token errors

### Config not updating
```bash
php artisan config:clear
php artisan cache:clear
```

## Report Back

After testing, provide:
1. One successful response JSON (trim citations if long)
2. Any errors encountered (if any)
3. Checklist completion status

