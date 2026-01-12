<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Cache;
use Exception;

/**
 * RAG Query Service
 * 
 * Handles HTTP communication with the RAG query service (kb_query).
 * Implements timeout, retry logic, and caching.
 */
class RagQueryService
{
    protected $baseUrl;
    protected $timeout;
    protected $retryCount;
    protected $cacheTtl;

    public function __construct()
    {
        $this->baseUrl = config('rag.query_service_url', 'http://kb_query:8099');
        $this->timeout = config('rag.timeout', 3.0); // seconds
        $this->retryCount = config('rag.retry_count', 1);
        $this->cacheTtl = config('rag.cache_ttl', 300); // 5 minutes
    }

    /**
     * Query the RAG service
     * 
     * @param string $queryText
     * @param int $limit
     * @param string|null $namespace
     * @param string|null $authority
     * @return array
     * @throws Exception
     */
    public function query(
        string $queryText,
        int $limit = 10,
        ?string $namespace = null,
        ?string $authority = null
    ): array {
        // Check cache first
        $cacheKey = $this->getCacheKey($queryText, $limit, $namespace, $authority);
        $cached = Cache::get($cacheKey);
        
        if ($cached !== null) {
            Log::debug('RAG query cache hit', ['key' => $cacheKey]);
            return $cached;
        }

        // Build request payload
        $payload = [
            'query' => $queryText,
            'top_k' => $limit,
            'limit' => $limit,   // keep for backward-compat
        ];

        if ($namespace !== null) {
            $payload['namespace'] = $namespace;
        }

        if ($authority !== null) {
            $payload['authority'] = $authority;
        }

        // Attempt request with retries
        $lastException = null;
        
        for ($attempt = 0; $attempt <= $this->retryCount; $attempt++) {
            try {
                $response = Http::timeout($this->timeout)
                    ->post("{$this->baseUrl}/query", $payload);

                if ($response->successful()) {
                    $result = $response->json();
                    
                    // Cache successful response
                    Cache::put($cacheKey, $result, $this->cacheTtl);
                    
                    return $result;
                }

                // If not successful, throw exception
                throw new Exception("RAG service returned status {$response->status()}: {$response->body()}");

            } catch (\Illuminate\Http\Client\ConnectionException $e) {
                $lastException = $e;
                Log::warning("RAG query attempt {$attempt} failed (connection)", [
                    'error' => $e->getMessage(),
                ]);
                
                // Wait before retry (exponential backoff)
                if ($attempt < $this->retryCount) {
                    usleep(100000 * ($attempt + 1)); // 100ms, 200ms, etc.
                }
                
            } catch (\Illuminate\Http\Client\RequestException $e) {
                $lastException = $e;
                Log::warning("RAG query attempt {$attempt} failed (request)", [
                    'error' => $e->getMessage(),
                ]);
                
                // Don't retry on 4xx errors (client errors)
                if ($e->response && $e->response->status() >= 400 && $e->response->status() < 500) {
                    throw $e;
                }
                
                // Wait before retry
                if ($attempt < $this->retryCount) {
                    usleep(100000 * ($attempt + 1));
                }
                
            } catch (Exception $e) {
                $lastException = $e;
                Log::error("RAG query attempt {$attempt} failed (unexpected)", [
                    'error' => $e->getMessage(),
                ]);
                
                // Don't retry on unexpected errors
                throw $e;
            }
        }

        // All retries exhausted
        throw new Exception(
            "RAG query failed after {$this->retryCount} retries: " . 
            ($lastException ? $lastException->getMessage() : 'Unknown error')
        );
    }

    /**
     * Get health status of RAG service
     */
    public function health(): bool
    {
        try {
            $response = Http::timeout(2)
                ->get("{$this->baseUrl}/health");
            
            return $response->successful() && 
                   ($response->json()['status'] ?? null) === 'ok';
        } catch (Exception $e) {
            Log::debug('RAG health check failed', ['error' => $e->getMessage()]);
            return false;
        }
    }

    /**
     * Get KB and index versions
     */
    public function getVersions(): array
    {
        try {
            $response = Http::timeout(2)
                ->get("{$this->baseUrl}/version");
            
            if ($response->successful()) {
                return $response->json();
            }
        } catch (Exception $e) {
            Log::debug('RAG version check failed', ['error' => $e->getMessage()]);
        }

        return [
            'kb_version' => 'unknown',
            'index_version' => 'unknown',
        ];
    }

    /**
     * Generate cache key for query
     */
    protected function getCacheKey(
        string $query,
        int $limit,
        ?string $namespace,
        ?string $authority
    ): string {
        $parts = [
            'rag_query',
            md5($query),
            $limit,
            $namespace ?? 'null',
            $authority ?? 'null',
        ];
        
        return implode(':', $parts);
    }
}

