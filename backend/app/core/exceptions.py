"""
Exception Handlers

Standardizes all error responses to match Error Taxonomy format:
{detail, error_code, request_id, version}
"""
from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.error_codes import ErrorCodes


API_VERSION = "v1"


def _get_request_id(request: Request) -> str:
    """Extract request_id from request state, defaulting to 'unknown' if not set."""
    return getattr(request.state, "request_id", "unknown")


def _default_error_code_for_status(status_code: int) -> str:
    """
    Map HTTP status code to default error code.
    
    Note: This is a fallback. Prefer explicit error_code via HTTPException.detail dict.
    """
    if status_code == 400:
        return ErrorCodes.VALIDATION_ERROR
    if status_code == 401:
        return ErrorCodes.AUTH_INVALID_TOKEN
    if status_code == 403:
        return ErrorCodes.PERMISSION_DENIED
    if status_code == 404:
        return ErrorCodes.NOT_FOUND_RESOURCE
    if status_code == 409:
        return ErrorCodes.CONFLICT_BUSINESS_RULE
    if status_code == 422:
        return ErrorCodes.SEMANTIC_VALIDATION_ERROR
    return ErrorCodes.INTERNAL_SERVER_ERROR


def _extract_error_code_and_detail(exc_detail: Any, status_code: int) -> tuple[str, Any]:
    """
    Extract error_code and detail from exception detail.
    
    Supports both:
      - detail="LINE_ITEM_LOCKED" (legacy format)
      - detail={"error_code": "...", "detail": "..."}  (preferred explicit format)
    """
    if isinstance(exc_detail, dict):
        error_code = exc_detail.get("error_code") or _default_error_code_for_status(status_code)
        detail = exc_detail.get("detail", exc_detail)  # if no 'detail', keep dict
        return error_code, detail

    # string / list / other primitives
    return _default_error_code_for_status(status_code), exc_detail


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Standardize HTTPException responses to Error Taxonomy format.
    """
    request_id = _get_request_id(request)
    error_code, detail = _extract_error_code_and_detail(exc.detail, exc.status_code)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": detail,
            "error_code": error_code,
            "request_id": request_id,
            "version": API_VERSION,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    FastAPI/Pydantic validation errors (422) wrapped into standard format.
    
    We keep exc.errors() as detail for debuggability; can add nicer shape later.
    """
    request_id = _get_request_id(request)
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "message": "Validation failed",
                "errors": exc.errors(),
            },
            "error_code": ErrorCodes.SEMANTIC_VALIDATION_ERROR,
            "request_id": request_id,
            "version": API_VERSION,
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unhandled exceptions (500).
    
    Note: In production, you may want to log the full exception trace here.
    """
    request_id = _get_request_id(request)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": ErrorCodes.INTERNAL_SERVER_ERROR,
            "request_id": request_id,
            "version": API_VERSION,
        },
    )

