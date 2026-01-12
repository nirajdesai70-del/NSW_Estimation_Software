---
Status: WORKING
Version: 1.0
Owner: RAG UI Integration
Updated: 2025-01-27
Scope: Setup Instructions
---

# RAG UI Integration - Quick Setup

## Pre-Implementation Review Summary

### ✅ Suggestions Implemented
- **Read-only assist first**: UI components are read-only (no auto-write)
- **Feature flags**: All RAG UI features behind flags
- **Citations first-class**: Citations displayed prominently with authority badges

### ⚠️ Risks Mitigated
- **Latency**: 3s timeout + caching (5min TTL) + graceful degradation
- **Service outages**: Retry logic (1 retry) + fallback to empty response
- **Trust**: Citations always shown with authority badges and version stamps

### ✅ Gaps Closed
- **Standard response schema**: Normalized in `RagController`
- **UI-side caching**: HTTP client caching + browser-level
- **Consistent render location**: Blade component `<x-rag-explain-why>`

## Installation Checklist

### Step 1: Copy Files to Laravel App

Copy these files to your Laravel application:

```
app/Http/Controllers/RagController.php
app/Services/RagQueryService.php
config/rag.php
routes/rag.php
resources/views/components/rag-explain-why.blade.php
resources/views/components/rag-authority-badge.blade.php
public/js/rag-ui.js
public/css/rag-ui.css
```

### Step 2: Register Routes

**Option A:** Include route file in `routes/web.php`:

```php
require __DIR__.'/rag.php';
```

**Option B:** Add to `routes/web.php` directly:

```php
Route::middleware(['auth'])->group(function () {
    Route::post('/ui/rag/query', [App\Http\Controllers\RagController::class, 'query'])
        ->name('rag.query');
});
```

### Step 3: Add Environment Variables

Add to `.env`:

```env
# RAG Query Service
RAG_QUERY_SERVICE_URL=http://kb_query:8099
RAG_TIMEOUT=3.0
RAG_RETRY_COUNT=1
RAG_CACHE_TTL=300

# Feature Flags (start with false, enable after testing)
RAG_UI_ENABLED=false
RAG_EXPLAIN_WHY_ENABLED=false
RAG_GOV_ALERTS_ENABLED=false
```

**For local development** (if RAG runs on localhost):

```env
RAG_QUERY_SERVICE_URL=http://localhost:8099
```

### Step 4: Include Assets

Add to your main layout (`resources/views/layouts/app.blade.php` or equivalent):

**In `<head>` section:**
```blade
<link rel="stylesheet" href="{{ asset('css/rag-ui.css') }}">
```

**Before closing `</body>`:**
```blade
<script src="{{ asset('js/rag-ui.js') }}"></script>
```

### Step 5: Clear Config Cache

```bash
php artisan config:clear
php artisan config:cache
```

### Step 6: Test

1. **Start RAG service:**
   ```bash
   docker-compose -f docker-compose.rag.yml up kb_query
   ```

2. **Enable feature flag:**
   ```env
   RAG_UI_ENABLED=true
   RAG_EXPLAIN_WHY_ENABLED=true
   ```
   Then: `php artisan config:clear`

3. **Add component to a test view:**
   ```blade
   <x-rag-explain-why 
       :query="'How do I map products to categories?'"
       :context="['screen' => 'catalog']"
   />
   ```

4. **Visit page and click "Explain why"**

## Verification

### ✅ Backend Adapter Working
- [ ] Route `/ui/rag/query` responds (check with `php artisan route:list | grep rag`)
- [ ] Controller exists: `app/Http/Controllers/RagController.php`
- [ ] Service exists: `app/Services/RagQueryService.php`
- [ ] Config exists: `config/rag.php`

### ✅ RAG Service Reachable
```bash
curl http://kb_query:8099/health
# Should return: {"status":"ok"}
```

### ✅ UI Components Loaded
- [ ] Check browser console: no JavaScript errors
- [ ] CSS loaded: check Network tab for `rag-ui.css`
- [ ] JS loaded: check Network tab for `rag-ui.js`

### ✅ Feature Flags Work
- [ ] Component hidden when `RAG_UI_ENABLED=false`
- [ ] Component visible when `RAG_UI_ENABLED=true`

## First Integration Point: Catalog Mapping

See `resources/views/examples/rag-catalog-integration-example.blade.php` for a complete example.

**Quick integration in existing catalog view:**

```blade
{{-- In your product import/mapping view --}}
<div class="mb-3">
    <label>Product Description</label>
    <input type="text" id="productDesc" class="form-control" />
    
    <div class="mt-2">
        <x-rag-explain-why 
            :query="'Suggest category and attributes for this product'"
            :context="['screen' => 'catalog']"
            trigger-text="Ask RAG for suggestions"
        />
    </div>
</div>
```

## Troubleshooting

### "RAG service is currently unavailable"
- Check RAG service is running: `docker ps | grep kb_query`
- Verify URL in `.env`: `RAG_QUERY_SERVICE_URL`
- Test connectivity: `curl http://kb_query:8099/health`

### Component not showing
- Check feature flags: `RAG_UI_ENABLED=true` and `RAG_EXPLAIN_WHY_ENABLED=true`
- Clear config: `php artisan config:clear`
- Check Blade component exists: `resources/views/components/rag-explain-why.blade.php`

### JavaScript errors
- Verify CSRF token in page: `<meta name="csrf-token" content="...">`
- Check `rag-ui.js` is loaded (Network tab)
- Check browser console for errors

### Citations empty
- Check Laravel logs: `storage/logs/laravel.log`
- Verify RAG service returns data: `curl -X POST http://kb_query:8099/query -H "Content-Type: application/json" -d '{"query":"test","limit":5}'`

## Next Steps

1. **Test in catalog mapping screen** (recommended first integration)
2. **Add to L1→L2 explosion preview** (Option B)
3. **Add to pricing import validation** (Option C)
4. **Implement governance alerts widget** (future)

## References

- Full integration guide: `RAG_KB/UI_INTEGRATION_GUIDE.md`
- RAG rulebook: `RAG_KB/RAG_RULEBOOK.md`
- Query service: `services/kb_query/query_server.py`

