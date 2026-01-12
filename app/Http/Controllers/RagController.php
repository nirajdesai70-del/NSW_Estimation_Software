<?php

namespace App\Http\Controllers;

use App\Services\RagQueryService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;

/**
 * RAG UI Adapter Controller
 * 
 * Provides a Laravel backend adapter for the RAG query service.
 * Handles timeouts, retries, and graceful degradation.
 */
class RagController extends Controller
{
    protected $ragService;

    public function __construct(RagQueryService $ragService)
    {
        $this->ragService = $ragService;
    }

    /**
     * POST /ui/rag/query
     * 
     * UI-friendly RAG query endpoint with context support
     * 
     * Request body:
     * {
     *   "query": "string",
     *   "context": {
     *     "screen": "catalog|l1_l2|quotation|pricing_import",
     *     "tenant": "optional",
     *     "make": "optional",
     *     "series": "optional",
     *     "sku": "optional",
     *     "item": "optional"
     *   },
     *   "top_k": 8
     * }
     * 
     * Response:
     * {
     *   "answer": "string",
     *   "citations": [...],
     *   "kb_version": "string",
     *   "index_version": "string",
     *   "latency_ms": 123
     * }
     */
    public function query(Request $request): JsonResponse
    {
        // Validate request
        $validator = Validator::make($request->all(), [
            'query' => 'required|string|min:1|max:1000',
            'context' => 'sometimes|array',
            'context.screen' => 'sometimes|string|in:catalog,l1_l2,quotation,pricing_import',
            'context.tenant' => 'sometimes|string|max:100',
            'context.make' => 'sometimes|string|max:100',
            'context.series' => 'sometimes|string|max:100',
            'context.sku' => 'sometimes|string|max:100',
            'context.item' => 'sometimes|string|max:100',
            'top_k' => 'sometimes|integer|min:1|max:20',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error' => 'Validation failed',
                'errors' => $validator->errors(),
            ], 422);
        }

        $query = $request->input('query');
        $context = $request->input('context', []);
        $topK = $request->input('top_k', 8);

        // Check feature flag
        if (!config('rag.ui_enabled', false)) {
            return response()->json([
                'answer' => 'RAG UI is currently disabled.',
                'citations' => [],
                'kb_version' => 'unknown',
                'index_version' => 'unknown',
                'latency_ms' => 0,
            ], 503);
        }

        $startTime = microtime(true);

        try {
            // Build enhanced query with context
            $enhancedQuery = $this->enhanceQueryWithContext($query, $context);

            // Call RAG service
            $result = $this->ragService->query($enhancedQuery, $topK);

            $latency = round((microtime(true) - $startTime) * 1000);

            $normalizedCitations = $this->normalizeCitations($result['citations'] ?? []);

            // Log telemetry for successful query
            $this->logTelemetry($request, [
                'ts' => now()->toIso8601String(),
                'status' => 'ok',
                'user_id' => optional($request->user())->id,
                'screen' => $context['screen'] ?? null,
                'query' => $query,
                'enhanced_query' => $enhancedQuery,
                'top_k' => $topK,
                'best_authority' => $this->bestAuthority($normalizedCitations),
                'citations' => array_slice($normalizedCitations, 0, 10),
                'kb_version' => $result['kb_version'] ?? 'unknown',
                'index_version' => $result['index_version'] ?? 'unknown',
                'latency_ms' => $latency,
            ]);

            // Normalize response for UI
            return response()->json([
                'answer' => $result['answer'] ?? 'No answer available.',
                'citations' => $normalizedCitations,
                'best_authority' => $this->bestAuthority($normalizedCitations),
                'kb_version' => $result['kb_version'] ?? 'unknown',
                'index_version' => $result['index_version'] ?? 'unknown',
                'latency_ms' => $latency,
            ]);

        } catch (\Exception $e) {
            Log::error('RAG query failed', [
                'query' => $query,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString(),
            ]);

            $latency = round((microtime(true) - $startTime) * 1000);

            // Log telemetry for failed query
            $this->logTelemetry($request, [
                'ts' => now()->toIso8601String(),
                'status' => 'error',
                'user_id' => optional($request->user())->id,
                'screen' => $context['screen'] ?? null,
                'query' => $query ?? null,
                'top_k' => $topK ?? null,
                'latency_ms' => $latency,
                'error' => $e->getMessage(),
            ]);

            // Graceful degradation: return empty response
            return response()->json([
                'answer' => 'RAG service is currently unavailable. Please try again later.',
                'citations' => [],
                'kb_version' => 'unknown',
                'index_version' => 'unknown',
                'latency_ms' => $latency,
                'error' => config('app.debug') ? $e->getMessage() : null,
            ], 503);
        }
    }

    /**
     * Enhance query with context information
     * 
     * Uses structured JSON format for better retrieval consistency
     */
    protected function enhanceQueryWithContext(string $query, array $context): string
    {
        if (empty($context)) {
            return $query;
        }

        // Use deterministic JSON format for context
        $contextJson = json_encode($context, JSON_UNESCAPED_SLASHES);
        return $query . "\n\n[CONTEXT] " . $contextJson;
    }

    /**
     * Normalize citations to match UI contract
     * 
     * Handles both query_service format (file) and expected UI format (source_path, kb_path)
     */
    protected function normalizeCitations(array $citations): array
    {
        return array_map(function ($citation) {
            // Query service returns 'file' field, but UI expects 'source_path' and 'kb_path'
            $file = $citation['file'] ?? $citation['source_path'] ?? '';
            $kbPath = $citation['kb_path'] ?? $file;
            $sourcePath = $citation['source_path'] ?? $file;
            
            return [
                'kb_path' => $kbPath,
                'source_path' => $sourcePath,
                'title' => $citation['title'] ?? '',
                'authority' => strtoupper($citation['authority'] ?? 'WORKING'),
                'last_modified' => $citation['last_modified'] ?? '',
                'score' => floatval($citation['score'] ?? 0.0),
            ];
        }, $citations);
    }

    /**
     * Compute best authority from citations
     * 
     * Priority: CANONICAL > WORKING > DRAFT > DEPRECATED
     * 
     * @param array $citations
     * @return string
     */
    protected function bestAuthority(array $citations): string
    {
        if (empty($citations)) {
            return 'WORKING';
        }

        $authorityPriority = [
            'CANONICAL' => 4,
            'WORKING' => 3,
            'DRAFT' => 2,
            'DEPRECATED' => 1,
        ];

        $bestAuthority = 'WORKING';
        $bestPriority = 0;

        foreach ($citations as $citation) {
            $auth = strtoupper($citation['authority'] ?? 'WORKING');
            $priority = $authorityPriority[$auth] ?? 0;
            
            if ($priority > $bestPriority) {
                $bestPriority = $priority;
                $bestAuthority = $auth;
            }
        }

        return $bestAuthority;
    }

    /**
     * Log telemetry data for RAG queries
     * 
     * Logs to a dedicated JSONL channel for easy parsing and analysis.
     * Each log entry is a single JSON object on one line.
     * 
     * @param Request $request
     * @param array $payload
     * @return void
     */
    protected function logTelemetry(Request $request, array $payload): void
    {
        if (!config('rag.telemetry_enabled', false)) {
            return;
        }

        $channel = config('rag.telemetry_log_channel', 'rag_telemetry');

        // Force JSONL: one valid JSON object per line
        Log::channel($channel)->info(json_encode($payload, JSON_UNESCAPED_SLASHES));
    }

    /**
     * Log feedback data for RAG queries
     * 
     * Logs to a dedicated JSONL channel for easy parsing and analysis.
     * Each log entry is a single JSON object on one line.
     * 
     * @param Request $request
     * @param array $payload
     * @return void
     */
    protected function logFeedback(Request $request, array $payload): void
    {
        if (!config('rag.feedback_enabled', false)) {
            return;
        }

        $channel = config('rag.feedback_log_channel', 'rag_feedback');

        // Force JSONL: one valid JSON object per line
        Log::channel($channel)->info(json_encode($payload, JSON_UNESCAPED_SLASHES));
    }

    /**
     * POST /ui/rag/feedback
     * 
     * UI feedback endpoint for RAG queries
     * 
     * Request body:
     * {
     *   "query": "string",
     *   "rating": "up|down",
     *   "context": {...},
     *   "best_authority": "string",
     *   "citations": [...],
     *   "comment": "string",
     *   "latency_ms": 123
     * }
     * 
     * Response:
     * {
     *   "ok": true
     * }
     */
    public function feedback(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'query' => 'required|string|min:1|max:1000',
            'rating' => 'required|string|in:up,down',
            'context' => 'sometimes|array',
            'best_authority' => 'sometimes|string|max:20',
            'citations' => 'sometimes|array',
            'comment' => 'sometimes|string|max:500',
            'latency_ms' => 'sometimes|integer|min:0|max:600000',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => 'Validation failed', 'errors' => $validator->errors()], 422);
        }

        $payload = [
            'ts' => now()->toIso8601String(),
            'user_id' => optional($request->user())->id,
            'status' => 'feedback',
            'rating' => $request->input('rating'),
            'query' => $request->input('query'),
            'context' => $request->input('context', []),
            'best_authority' => $request->input('best_authority', null),
            'citations' => array_slice($request->input('citations', []), 0, 10),
            'latency_ms' => $request->input('latency_ms', null),
            'comment' => $request->input('comment', null),
        ];

        $this->logFeedback($request, $payload);

        return response()->json(['ok' => true]);
    }
}

