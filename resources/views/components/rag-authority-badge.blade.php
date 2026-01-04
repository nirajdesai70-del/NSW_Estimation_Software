{{-- 
UI CONTEXT: REFERENCE HARNESS ONLY
Purpose: Validate RAG API, latency, citations, feedback loop
NOT Phase-5 UI design
--}}
{{-- RAG Authority Badge Component --}}
{{-- Usage: <x-rag-authority-badge :authority="'CANONICAL'" /> --}}

@props([
    'authority' => 'WORKING',
    'size' => 'sm', // sm, md, lg
])

@php
    $authority = strtoupper($authority ?? 'WORKING');
    $badgeClasses = [
        'CANONICAL' => 'bg-success text-white',
        'WORKING' => 'bg-warning text-dark',
        'DRAFT' => 'bg-secondary text-white',
        'DEPRECATED' => 'bg-danger text-white',
    ];
    $badgeClass = $badgeClasses[$authority] ?? $badgeClasses['WORKING'];
    
    $icons = [
        'CANONICAL' => '✅',
        'WORKING' => '⚠️',
        'DRAFT' => '🧪',
        'DEPRECATED' => '❌',
    ];
    $icon = $icons[$authority] ?? '⚠️';
    
    $sizeClass = match($size) {
        'sm' => 'badge-sm',
        'md' => '',
        'lg' => 'badge-lg',
        default => '',
    };
@endphp

<span class="badge {{ $badgeClass }} {{ $sizeClass }}" title="Authority: {{ $authority }}">
    {{ $icon }} {{ $authority }}
</span>

