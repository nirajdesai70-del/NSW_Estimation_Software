"""
API Error Helper

Convenience function for raising standardized API errors.
Ensures all raised errors are compatible with the global exception handler.
"""
from typing import Union, Dict, Any
from fastapi import HTTPException


def raise_api_error(
    *,
    status_code: int,
    error_code: str,
    detail: Union[str, Dict[str, Any]],
):
    """
    Raise a standardized API error.

    Supports:
    - detail as string
    - detail as structured dict (e.g. validation summaries)

    Both are compatible with the global exception handler.

    Args:
        status_code: HTTP status code (e.g. 400, 404, 409)
        error_code: Canonical error code (e.g. CONFLICT_LINE_ITEM_LOCKED)
        detail: Human-readable error message (string) or structured dict

    Example:
        from app.core.raise_api_error import raise_api_error
        from app.core.error_codes import ErrorCodes

        # Simple error
        raise_api_error(
            status_code=409,
            error_code=ErrorCodes.CONFLICT_LINE_ITEM_LOCKED,
            detail="LINE_ITEM_LOCKED",
        )

        # Structured validation error
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.CONFLICT_IMPORT_HAS_ERRORS,
            detail={
                "message": "Cannot commit import with validation errors. Fix errors first.",
                "summary": summary,
            },
        )
    """
    raise HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code,
            "detail": detail,
        },
    )

