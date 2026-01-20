---
Status: WORKING
Version: 1.0
Owner: RAG UI Integration
Updated: 2025-01-27
Scope: UI Integration
---

# RAG UI Integration Guide

## Overview

This guide explains how to integrate RAG UI components into the NSW Estimation Software Laravel application.

## Architecture

```
┌─────────────────┐
│  Laravel UI     │
│  (Blade/JS)     │
└────────┬────────┘
         │ POST /ui/rag/query
         ▼
┌─────────────────┐
│ RagController   │  ← Laravel Adapter
│ (Laravel)       │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│ kb_query:8099   │  ← RAG Query Service
│ (FastAPI)       │
└─────────────────┘
```

## Installation Steps

### 1. Register Routes

Add to `routes/web.php` or include the route file:

```php
// Option A: Include route file
require __DIR__.'/rag.php';

// Option B: Add directly to web.php
Route::middleware(['auth'])->group(function () {
    Route::post('/ui/rag/query', [App\Http\Controllers\RagController::class, 'query'])
        ->name('rag.query');
});
```

### 2. Add Configuration

Add to `.env`:

```env
# RAG Configuration
RAG_QUERY_SERVICE_URL=http://kb_query:8099
RAG_TIMEOUT=3.0
RAG_RETRY_COUNT=1
RAG_CACHE_TTL=300

# Feature Flags
RAG_UI_ENABLED=true
RAG_EXPLAIN_WHY_ENABLED=true
RAG_GOV_ALERTS_ENABLED=false
```

For local development (if RAG service runs on localhost):

```env
RAG_QUERY_SERVICE_URL=http://localhost:8099
```

### 3. Include Assets

Add to your main layout (`resources/views/layouts/app.blade.php`):

```blade
{{-- In <head> section --}}
<link rel="stylesheet" href="{{ asset('css/rag-ui.css') }}">

{{-- Before closing </body> --}}
<script src="{{ asset('js/rag-ui.js') }}"></script>
```

### 4. Use Components

#### Explain-Why Drawer

Add to any view where you want to show RAG explanations:

```blade
<x-rag-explain-why 
    :query="'How do I map this product to a category?'"
    :context="['screen' => 'catalog', 'item' => $product->Name]"
    trigger-text="Why this suggestion?"
/>
```

#### Authority Badge

Display authority status:

```blade
<x-rag-authority-badge :authority="'CANONICAL'" size="sm" />
```

## Integration Examples

### Example 1: Catalog Mapping Screen

In `resources/views/import/product.blade.php`:

```blade
@push('plugin_js')
<script>
    // When user types product description
    document.getElementById('productDescription').addEventListener('input', function(e) {
        const description = e.target.value;
        if (description.length > 10) {
            // Show "Ask RAG" button
            const ragButton = document.getElementById('ragSuggestButton');
            if (ragButton) {
                ragButton.style.display = 'block';
                ragButton.dataset.query = `Suggest category and attributes for: ${description}`;
            }
        }
    });
</script>
@endpush

{{-- In the form --}}
<div class="mb-3">
    <label>Product Description</label>
    <input type="text" id="productDescription" class="form-control" />
    
    <div id="ragSuggestButton" style="display: none;" class="mt-2">
        <x-rag-explain-why 
            :query="''"
            :context="['screen' => 'catalog']"
            trigger-text="Ask RAG for suggestions"
        />
    </div>
</div>
```

### Example 2: L1 → L2 Explosion Preview

In quotation panel view:

```blade
<div class="alert alert-info">
    <strong>Suggested SKUs:</strong> {{ implode(', ', $suggestedSkus) }}
    
    <x-rag-explain-why 
        :query="'Why these SKUs for L1 explosion?'"
        :context="['screen' => 'l1_l2', 'make' => $make, 'series' => $series]"
        trigger-text="Why these SKUs?"
        trigger-class="btn btn-sm btn-link"
    />
</div>
```

### Example 3: Pricing Import Validation

In pricing import validation screen:

```blade
@foreach($flaggedItems as $item)
    <div class="card mb-2">
        <div class="card-body">
            <h6>{{ $item->description }}</h6>
            <p class="text-danger">Flagged: {{ $item->reason }}</p>
            
            <x-rag-explain-why 
                :query="'Why is this item flagged: {{ $item->reason }}?'"
                :context="['screen' => 'pricing_import', 'sku' => $item->sku]"
                trigger-text="Explain why flagged"
            />
        </div>
    </div>
@endforeach
```

## API Contract

### Request

```json
{
  "query": "string",
  "context": {
    "screen": "catalog|l1_l2|quotation|pricing_import",
    "tenant": "optional",
    "make": "optional",
    "series": "optional",
    "sku": "optional",
    "item": "optional"
  },
  "top_k": 8
}
```

### Response

```json
{
  "answer": "string",
  "citations": [
    {
      "kb_path": "phase5_pack/...",
      "source_path": "docs/PHASE_5/...",
      "authority": "CANONICAL|WORKING|DRAFT",
      "last_modified": "ISO string",
      "score": 0.0
    }
  ],
  "kb_version": "string",
  "index_version": "string",
  "latency_ms": 123
}
```

## Feature Flags

Control RAG UI features via environment variables:

- `RAG_UI_ENABLED`: Global on/off switch
- `RAG_EXPLAIN_WHY_ENABLED`: Enable/disable explain-why drawer
- `RAG_GOV_ALERTS_ENABLED`: Enable/disable governance alerts widget (future)

## Caching

Query results are cached for 5 minutes (300 seconds) by default. Adjust via `RAG_CACHE_TTL`.

Cache keys include: query text, limit, namespace, authority.

## Error Handling

The adapter gracefully degrades if the RAG service is unavailable:

- Returns 503 status with empty citations
- Logs errors for debugging
- UI shows user-friendly error message

## Testing

### Manual Test

1. Start RAG query service:
   ```bash
   docker-compose -f docker-compose.rag.yml up kb_query
   ```

2. Enable feature flags in `.env`

3. Visit a page with RAG component

4. Click "Explain why" button

5. Verify drawer opens and shows citations

### API Test

```bash
curl -X POST http://your-app.test/ui/rag/query \
  -H "Content-Type: application/json" \
  -H "<CSRF_HEADER>: <csrf-token>" \
  -d '{
    "query": "How do I map products to categories?",
    "context": {"screen": "catalog"},
    "top_k": 5
  }'
```

## Troubleshooting

### RAG service unreachable

- Check `RAG_QUERY_SERVICE_URL` in `.env`
- Verify RAG service is running: `docker ps | grep kb_query`
- Check network connectivity: `curl http://kb_query:8099/health`

### Citations not showing

- Check browser console for JavaScript errors
- Verify CSRF token is present in page
- Check Laravel logs: `storage/logs/laravel.log`

### Feature flag not working

- Clear config cache: `php artisan config:clear`
- Verify `.env` values are correct
- Check `config/rag.php` exists

## Next Steps

1. **Governance Alerts Widget** (future)
   - Read `RISKS_AND_GAPS.md`
   - Display broken files, missing headers, canonical coverage

2. **More Integration Points**
   - Quotation validation
   - Master BOM suggestions
   - Attribute mapping assistance

3. **Performance Optimization**
   - Implement request debouncing
   - Add client-side caching
   - Optimize citation rendering

## References

- RAG Rulebook: `RAG_KB/RAG_RULEBOOK.md`
- Query Service: `services/kb_query/query_server.py`
- Governance: `RAG_KB/build_reports/RISKS_AND_GAPS.md`

