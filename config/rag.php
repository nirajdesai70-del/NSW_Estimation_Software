<?php

/**
 * RAG Configuration
 * 
 * Configuration for RAG UI integration
 */

return [
    /*
    |--------------------------------------------------------------------------
    | RAG Query Service URL
    |--------------------------------------------------------------------------
    |
    | Base URL for the RAG query service (kb_query).
    | Default assumes Docker service name, but can be overridden for local dev.
    |
    */
    'query_service_url' => env('RAG_QUERY_SERVICE_URL', 'http://kb_query:8099'),

    /*
    |--------------------------------------------------------------------------
    | Timeout (seconds)
    |--------------------------------------------------------------------------
    |
    | Request timeout for RAG queries. Should be 2.5-4 seconds as per spec.
    |
    */
    'timeout' => env('RAG_TIMEOUT', 3.0),

    /*
    |--------------------------------------------------------------------------
    | Retry Count
    |--------------------------------------------------------------------------
    |
    | Number of retries on failure (default: 1 retry = 2 total attempts).
    |
    */
    'retry_count' => env('RAG_RETRY_COUNT', 1),

    /*
    |--------------------------------------------------------------------------
    | Cache TTL (seconds)
    |--------------------------------------------------------------------------
    |
    | Cache time-to-live for query results. Default: 5 minutes (300 seconds).
    | Set to 0 to disable caching.
    |
    */
    'cache_ttl' => env('RAG_CACHE_TTL', 300),

    /*
    |--------------------------------------------------------------------------
    | Feature Flags
    |--------------------------------------------------------------------------
    |
    | Control RAG UI features via feature flags.
    |
    */
    'ui_enabled' => env('RAG_UI_ENABLED', false),
    'explain_why_enabled' => env('RAG_EXPLAIN_WHY_ENABLED', false),
    'gov_alerts_enabled' => env('RAG_GOV_ALERTS_ENABLED', false),

    /*
    |--------------------------------------------------------------------------
    | Telemetry
    |--------------------------------------------------------------------------
    |
    | Enable telemetry logging for RAG queries to track usage patterns,
    | query performance, and citation selection for continuous learning.
    |
    */
    'telemetry_enabled' => env('RAG_TELEMETRY_ENABLED', true),
    'telemetry_log_channel' => env('RAG_TELEMETRY_LOG_CHANNEL', 'rag_telemetry'),

    /*
    |--------------------------------------------------------------------------
    | Feedback
    |--------------------------------------------------------------------------
    |
    | Enable feedback logging for RAG queries to track user satisfaction,
    | identify problematic queries, and improve knowledge base coverage.
    |
    */
    'feedback_enabled' => env('RAG_FEEDBACK_ENABLED', true),
    'feedback_log_channel' => env('RAG_FEEDBACK_LOG_CHANNEL', 'rag_feedback'),
];

