"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.core.config import settings
from app.core.middleware.request_id import RequestIDMiddleware
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from app.api.v1.router import api_router

app = FastAPI(
    title="NSW Estimation Software API",
    description="New build - FastAPI backend for NSW Estimation Software",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Request ID Middleware (must be before CORS to ensure request_id is available)
app.add_middleware(RequestIDMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers (standardize all error responses)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NSW Estimation Software API",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "nsw-api"}


def custom_openapi():
    """Custom OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="NSW Estimation Software API",
        version="0.1.0",
        description="New build - FastAPI backend for NSW Estimation Software",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    """
    Direct execution entry point for development.
    Usage: python -m app.main
    """
    import uvicorn
    from app.core.config import settings
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )


