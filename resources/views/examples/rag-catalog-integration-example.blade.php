{{-- 
UI CONTEXT: REFERENCE HARNESS ONLY
Purpose: Validate RAG API, latency, citations, feedback loop
NOT Phase-5 UI design
--}}
@extends('layouts.app')

@section('title', 'RAG – Catalog Mapping (Example)')

@push('styles')
    {{-- RAG UI styles --}}
    <link rel="stylesheet" href="{{ asset('css/rag-ui.css') }}">
@endpush

@section('content')
<div class="container-fluid py-4">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        RAG – Catalog Mapping (Test Harness)
                    </h4>
                </div>

                <div class="card-body" id="ragCatalogSection">
                    <p class="text-muted">
                        This page is a <strong>live integration harness</strong> for testing RAG UI
                        before embedding it into real catalog / item master screens.
                    </p>

                    {{-- Product Description --}}
                    <div class="mb-3">
                        <label for="productDescription" class="form-label">
                            Product Description <span class="text-danger">*</span>
                        </label>

                        <textarea
                            id="productDescription"
                            class="form-control"
                            rows="3"
                            placeholder="Enter product description (e.g. Schneider 3P MCCB 63A thermal magnetic)..."
                        ></textarea>

                        <small class="text-muted">
                            Type a description (min 10–12 chars) to activate RAG suggestions.
                        </small>
                    </div>

                    {{-- RAG Actions --}}
                    <div class="mt-3 d-flex gap-2 align-items-center">
                        <button
                            type="button"
                            class="btn btn-sm btn-primary"
                            id="ragSuggestBtn"
                            style="display:none;"
                        >
                            Ask RAG for Suggestions
                        </button>

                        {{-- Explain-Why Drawer --}}
                        <x-rag-explain-why
                            :query="''"
                            :context="['screen' => 'catalog']"
                            trigger-text="Explain why"
                            trigger-class="btn btn-sm btn-outline-info"
                        />
                    </div>

                    <hr class="my-4">

                    {{-- Mock Mapping Fields --}}
                    <h6 class="text-muted">Mock Mapping Fields (for UI context)</h6>

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Category</label>
                            <select class="form-control">
                                <option>— Select Category —</option>
                                <option>Electrical</option>
                                <option>Automation</option>
                                <option>Protection</option>
                            </select>
                        </div>

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Subcategory</label>
                            <select class="form-control">
                                <option>— Select Subcategory —</option>
                                <option>MCCB</option>
                                <option>MCB</option>
                                <option>ACB</option>
                            </select>
                        </div>
                    </div>

                    <div class="alert alert-info mt-3">
                        <strong>Note:</strong>
                        RAG is currently <em>read-only</em>.
                        It explains suggestions but does not auto-apply values yet.
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@push('scripts')
    {{-- RAG UI JS --}}
    <script src="{{ asset('js/rag-ui.js') }}"></script>

    <script>
    (function () {
        // Scope to this card section to avoid conflicts with multiple RAG components
        const section = document.getElementById('ragCatalogSection');
        if (!section) return;

        const desc = document.getElementById('productDescription');
        const btn  = document.getElementById('ragSuggestBtn');

        if (!desc || !btn) return;

        function buildQuery(text) {
            return `Suggest Category, Subcategory, and key Attributes for this product description:\n${text}`;
        }

        // Helper: find wrapper scoped to this section
        function getRagWrapper() {
            return section.querySelector('.rag-explain-why-wrapper');
        }

        desc.addEventListener('input', function () {
            const text = (desc.value || '').trim();

            if (text.length >= 12) {
                btn.style.display = 'inline-block';

                const wrapper = getRagWrapper();
                if (wrapper) {
                    wrapper.dataset.query = buildQuery(text);
                }
            } else {
                btn.style.display = 'none';
            }
        });

        btn.addEventListener('click', function () {
            const text = (desc.value || '').trim();
            if (!text) return;

            const wrapper = getRagWrapper();
            if (!wrapper) return;

            wrapper.dataset.query = buildQuery(text);

            const trigger = wrapper.querySelector('.rag-explain-trigger');
            if (trigger) trigger.click();
        });
    })();
    </script>
@endpush
