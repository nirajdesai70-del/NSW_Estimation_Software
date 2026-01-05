#!/usr/bin/env python3
"""
KB Query Server - FastAPI HTTP API server for query service

Usage:
    python3 query_server.py [--port 8099] [--host 0.0.0.0]
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import argparse
import uvicorn

from query_service import QueryService

# Initialize FastAPI app
app = FastAPI(
    title="RAG KB Query Service",
    description="Fast query API for RAG Knowledge Base with hybrid search",
    version="1.0.0"
)

# Initialize query service (global instance)
query_service = QueryService()


# Request/Response models
class QueryRequest(BaseModel):
    """Query request model"""
    query: str = Field(..., description="Query string to search")
    namespace: Optional[str] = Field(None, description="Optional namespace filter (e.g., 'phase5_docs')")
    authority: Optional[str] = Field(None, description="Optional authority filter (e.g., 'CANONICAL')")
    limit: int = Field(10, ge=1, le=100, description="Max results to return (1-100)")


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    citations: list
    kb_version: str
    index_version: str
    result_count: int


class VersionResponse(BaseModel):
    """Version response model"""
    kb_version: str
    index_version: str


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    keyword_backend: str
    kb_version: str
    index_version: str
    keyword_docs: int


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health():
    """Health check endpoint with backend and index stats"""
    try:
        # Get stats from keyword index
        stats = query_service.keyword_index.get_stats()
        keyword_doc_count = stats.get("document_count", 0)
        
        return {
            "status": "ok",
            "keyword_backend": "bm25",
            "kb_version": query_service._get_kb_version(),
            "index_version": query_service._get_index_version(),
            "keyword_docs": keyword_doc_count,
        }
    except Exception as e:
        # Return error status if stats unavailable
        return {
            "status": "error",
            "keyword_backend": "bm25",
            "kb_version": "unknown",
            "index_version": "unknown",
            "keyword_docs": 0,
        }


@app.post("/query", response_model=QueryResponse, tags=["query"])
def query(request: QueryRequest):
    """
    Query the knowledge base using hybrid search (BM25 + semantic)
    
    Returns results with citations and version headers.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query is required and cannot be empty")
    
    try:
        result = query_service.query(
            query_text=request.query,
            namespace=request.namespace,
            authority=request.authority,
            limit=request.limit,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.get("/version", response_model=VersionResponse, tags=["system"])
def version():
    """Get KB and index versions"""
    return {
        "kb_version": query_service._get_kb_version(),
        "index_version": query_service._get_index_version(),
    }


@app.get("/", tags=["system"])
def root():
    """Root endpoint with API information"""
    return {
        "service": "RAG KB Query Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)",
            "version": "/version",
            "docs": "/docs",
        }
    }


def main():
    parser = argparse.ArgumentParser(description="KB Query Server (FastAPI)")
    parser.add_argument("--port", type=int, default=8099, help="Port number (default: 8099)")
    parser.add_argument("--host", default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (development)")
    args = parser.parse_args()

    print(f"Starting KB Query Server on {args.host}:{args.port}")
    print(f"API Documentation: http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()

