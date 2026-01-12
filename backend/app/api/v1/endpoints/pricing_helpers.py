"""
Pricing helper functions for endpoints
"""
from typing import Optional
from fastapi import Header, Request

from app.core.raise_api_error import raise_api_error
from app.core.error_codes import ErrorCodes


def get_tenant_id_from_request(
    x_tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-ID"),
) -> int:
    """
    Extract and validate X-Tenant-ID header.
    
    Phase-5: Stub implementation using header.
    TODO: Replace with proper JWT/auth middleware.
    
    Args:
        x_tenant_id: X-Tenant-ID header value
        
    Returns:
        Tenant ID (integer)
        
    Raises:
        HTTPException: If header is missing or invalid
    """
    if not x_tenant_id:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_MISSING_TENANT,
            detail="X-Tenant-ID header required",
        )
    try:
        return int(x_tenant_id)
    except ValueError:
        raise_api_error(
            status_code=400,
            error_code=ErrorCodes.VALIDATION_ERROR,
            detail="X-Tenant-ID must be an integer",
        )

