{{-- 
UI CONTEXT: REFERENCE HARNESS ONLY
Purpose: Validate RAG API, latency, citations, feedback loop
NOT Phase-5 UI design
--}}
{{-- RAG Explain-Why Drawer Component --}}
{{-- Usage: <x-rag-explain-why :query="'your query'" :context="['screen' => 'catalog']" /> --}}

@props([
    'query' => '',
    'context' => [],
    'triggerText' => 'Explain why',
    'triggerClass' => 'btn btn-sm btn-outline-info',
])

@php $drawerId = 'ragExplainDrawer_' . uniqid(); @endphp

@if(config('rag.explain_why_enabled', false) && config('rag.ui_enabled', false))
    <div class="rag-explain-why-wrapper" data-query="{{ $query }}" data-context="{{ json_encode($context) }}" data-drawer-id="{{ $drawerId }}">
        <button 
            type="button" 
            class="rag-explain-trigger {{ $triggerClass }}"
            data-bs-toggle="offcanvas"
            data-bs-target="#{{ $drawerId }}"
            aria-controls="{{ $drawerId }}"
        >
            <i class="fas fa-question-circle me-1"></i>
            {{ $triggerText }}
        </button>

        {{-- Offcanvas Drawer --}}
        <div 
            class="offcanvas offcanvas-end" 
            tabindex="-1" 
            id="{{ $drawerId }}"
            aria-labelledby="{{ $drawerId }}Label"
        >
            <div class="offcanvas-header border-bottom">
                <h5 class="offcanvas-title" id="{{ $drawerId }}Label">
                    <i class="fas fa-lightbulb me-2"></i>
                    Why this suggestion?
                    <span id="{{ $drawerId }}BestAuthority" class="ms-2"></span>
                </h5>
                <button 
                    type="button" 
                    class="btn-close" 
                    data-bs-dismiss="offcanvas"
                    aria-label="Close"
                ></button>
            </div>
            
            <div class="offcanvas-body">
                {{-- Loading State --}}
                <div class="rag-explain-loading text-center py-5" style="display: none;">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-3 text-muted">Querying knowledge base...</p>
                </div>

                {{-- Error State --}}
                <div class="rag-explain-error alert alert-warning" style="display: none;">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <span class="rag-explain-error-text"></span>
                </div>

                {{-- Answer Section --}}
                <div class="rag-explain-answer" style="display: none;">
                    <div class="mb-4">
                        <h6 class="text-muted mb-2">Answer</h6>
                        <div class="rag-answer-text p-3 bg-light rounded"></div>
                    </div>
                </div>

                {{-- Citations Section --}}
                <div class="rag-explain-citations" style="display: none;">
                    <h6 class="text-muted mb-3">
                        <i class="fas fa-book me-2"></i>
                        Citations
                        <span class="rag-citation-count badge bg-secondary ms-2"></span>
                    </h6>
                    <div class="rag-citations-list list-group"></div>
                </div>

                {{-- Feedback Section --}}
                <div class="rag-feedback mt-3" style="display:none;">
                    <h6 class="text-muted mb-2">Was this helpful?</h6>
                    <div class="d-flex gap-2 align-items-center">
                        <button type="button" class="btn btn-sm btn-outline-success rag-feedback-up">👍 Helpful</button>
                        <button type="button" class="btn btn-sm btn-outline-danger rag-feedback-down">👎 Not Helpful</button>
                        <small class="text-muted rag-feedback-status ms-2"></small>
                    </div>
                </div>

                {{-- Version Footer --}}
                <div class="rag-explain-footer mt-4 pt-3 border-top" style="display: none;">
                    <small class="text-muted">
                        <i class="fas fa-info-circle me-1"></i>
                        KB Version: <span class="rag-kb-version">unknown</span> | 
                        Index Version: <span class="rag-index-version">unknown</span>
                        <span class="rag-latency ms-2"></span>
                    </small>
                </div>
            </div>
        </div>
    </div>
@endif

