# RAG Catalog Integration - Test Harness

## ✅ Setup Complete

The RAG UI integration test harness is now ready for validation.

### Files Updated

1. **Example View**: `resources/views/examples/rag-catalog-integration-example.blade.php`
   - Production-ready test harness
   - Uses hardened RAG components
   - Includes "Ask RAG" button + explain drawer

2. **Route Added**: `routes/rag.php`
   - GET `/examples/rag-catalog` → test harness page
   - Protected by `auth` middleware

## 🚀 Quick Start

### Step 1: Enable Feature Flags

Add to `.env`:

```env
RAG_UI_ENABLED=true
RAG_EXPLAIN_WHY_ENABLED=true
```

Then clear config cache:

```bash
php artisan config:clear
```

### Step 2: Access Test Page

Navigate to:

```
/examples/rag-catalog
```

(Requires authentication)

### Step 3: Test Checklist

- [ ] Page loads without errors
- [ ] Product description textarea is visible
- [ ] Type 12+ characters → "Ask RAG for Suggestions" button appears
- [ ] Click "Ask RAG" → offcanvas drawer opens
- [ ] Loading spinner shows
- [ ] Answer appears in drawer
- [ ] Citations list appears with authority badges
- [ ] Best authority badge shows in drawer header
- [ ] KB version and index version display in footer
- [ ] Latency shows in footer
- [ ] "Explain why" button works independently
- [ ] Multiple drawers can exist on same page (no ID collision)

### Step 4: Test Error Handling

- [ ] If `kb_query` service is down → graceful error message
- [ ] Rate limiting works (30 requests/minute)
- [ ] CSRF token is included in requests

## 🔧 Integration Pattern

When ready to integrate into real screens, use this pattern:

```blade
{{-- Product Description --}}
<div class="mb-3">
    <label for="productDescription" class="form-label">
        Product Description
    </label>
    <textarea id="productDescription" class="form-control" rows="3"></textarea>
</div>

{{-- RAG Actions --}}
<div class="mt-3 d-flex gap-2 align-items-center">
    <button type="button" class="btn btn-sm btn-primary" id="ragSuggestBtn" style="display:none;">
        Ask RAG for Suggestions
    </button>
    <x-rag-explain-why
        :query="''"
        :context="['screen' => 'catalog']"
        trigger-text="Explain why"
        trigger-class="btn btn-sm btn-outline-info"
    />
</div>

@push('scripts')
<script src="{{ asset('js/rag-ui.js') }}"></script>
<script>
(function () {
    const desc = document.getElementById('productDescription');
    const btn = document.getElementById('ragSuggestBtn');
    if (!desc || !btn) return;

    function buildQuery(text) {
        return `Suggest Category, Subcategory, and key Attributes for this product description:\n${text}`;
    }

    desc.addEventListener('input', function () {
        const text = (desc.value || '').trim();
        if (text.length >= 12) {
            btn.style.display = 'inline-block';
            const wrapper = document.querySelector('.rag-explain-why-wrapper');
            if (wrapper) wrapper.dataset.query = buildQuery(text);
        } else {
            btn.style.display = 'none';
        }
    });

    btn.addEventListener('click', function () {
        const text = (desc.value || '').trim();
        if (!text) return;
        const wrapper = document.querySelector('.rag-explain-why-wrapper');
        if (!wrapper) return;
        wrapper.dataset.query = buildQuery(text);
        const trigger = wrapper.querySelector('.rag-explain-trigger');
        if (trigger) trigger.click();
    });
})();
</script>
@endpush
```

## 📋 Next Steps

1. **Validate test harness** → Ensure all checklist items pass
2. **Create real catalog screen** → `resources/views/catalog/mapping.blade.php`
3. **Copy integration pattern** → Use exact same block from test harness
4. **Extend to other screens** → L1→L2, pricing import, etc.

## 🔍 Troubleshooting

### Drawer doesn't open
- Check browser console for errors
- Verify Bootstrap 5 is loaded
- Check that `rag-ui.js` is loaded

### No response from RAG
- Check `kb_query` service is running
- Verify `/ui/rag/query` endpoint returns 200
- Check Laravel logs for errors

### CSRF errors
- Verify `<meta name="csrf-token">` exists in layout
- Check that `rag-ui.js` reads CSRF token correctly

### Rate limiting
- Test with 30+ rapid requests
- Should see 429 status after limit

## 📚 References

- RAG UI Components: `resources/views/components/rag-*.blade.php`
- RAG Controller: `app/Http/Controllers/RagController.php`
- RAG Service: `app/Services/RagQueryService.php`
- RAG Routes: `routes/rag.php`
- RAG JS: `public/js/rag-ui.js`
- RAG CSS: `public/css/rag-ui.css`

