---
Status: DRAFT
Version: v1.0
Owner: Phase 5 Senate
Last_Updated: 2026-01-27
Scope: Phase-5 Category-B Error Taxonomy & Response Format
---

# Error Taxonomy

**Purpose:** Standardized error codes, messages, and HTTP status mapping for all API endpoints.

**Principle:** Fail-fast with clear, actionable error messages.

---

## Error Response Format

### Standard Error Response

```json
{
  "detail": "Error message or object",
  "error_code": "ERROR_CODE",
  "request_id": "uuid-v4",
  "version": "v1"
}
```

### Validation Error Response (Multi-Field)

```json
{
  "detail": {
    "message": "Validation failed",
    "summary": {
      "rows_total": 100,
      "rows_valid": 95,
      "rows_error": 5
    },
    "errors_sample": [
      {
        "row": 2,
        "field": "sku_code",
        "error": "Invalid SKU (must be at least 3 chars and contain letters)",
        "value": "AB"
      }
    ]
  }
}
```

---

## HTTP Status Code Mapping

| Status Code | Usage | Error Code Prefix |
|-------------|-------|-------------------|
| 400 | Bad Request (validation errors) | `VALIDATION_*` |
| 401 | Unauthorized (missing/invalid auth) | `AUTH_*` |
| 403 | Forbidden (insufficient permissions) | `PERMISSION_*` |
| 404 | Not Found (resource doesn't exist) | `NOT_FOUND_*` |
| 409 | Conflict (business rule violation) | `CONFLICT_*` |
| 422 | Unprocessable Entity (semantic validation) | `SEMANTIC_*` |
| 500 | Internal Server Error | `INTERNAL_*` |
| 503 | Service Unavailable | `SERVICE_*` |

---

## Error Codes

### Validation Errors (400)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `VALIDATION_MISSING_REQUIRED` | Missing required columns: {columns} | `POST /api/v1/catalog/skus/import` | CSV import |
| `VALIDATION_INVALID_PRICE` | Invalid price (must be numeric >= 0) | `POST /api/v1/catalog/skus/import` | Price field |
| `VALIDATION_INVALID_CURRENCY` | Must be 3-letter code (e.g., INR, USD) | `POST /api/v1/catalog/skus/import` | Currency field |
| `VALIDATION_INVALID_SKU` | Invalid SKU (must be at least 3 chars and contain letters) | `POST /api/v1/catalog/skus/import` | SKU code |
| `VALIDATION_INVALID_STAGE` | Only FINAL imports allowed | `POST /api/v1/catalog/skus/import` | Import stage |
| `VALIDATION_INVALID_PAGINATION` | limit must be between 1 and 200 | All GET list endpoints | Pagination |
| `VALIDATION_MISSING_TENANT` | X-Tenant-ID header required | All endpoints | Tenant isolation |

---

### Authentication Errors (401)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `AUTH_MISSING_TOKEN` | Authorization header required | All protected endpoints | Missing JWT |
| `AUTH_INVALID_TOKEN` | Invalid or expired token | All protected endpoints | Token validation |
| `AUTH_TOKEN_EXPIRED` | Token has expired | All protected endpoints | Token expiry |

---

### Permission Errors (403)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `PERMISSION_INSUFFICIENT_ROLE` | Only Reviewer and Approver roles allowed | `POST /api/v1/quotation/{id}/pricing/apply-recalc` | Role check |
| `PERMISSION_BULK_DISALLOWED` | Only Operator, Reviewer, Approver roles allowed | `PUT /api/v1/quotation/{id}/discount/quotation` | Role check |

**Note:** Role-based errors include actor roles in audit log.

---

### Not Found Errors (404)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `NOT_FOUND_ITEM` | Item not found | `GET /api/v1/catalog/items/{id}` | Item lookup |
| `NOT_FOUND_SKU` | SKU not found | `GET /api/v1/catalog/skus/{id}` | SKU lookup |
| `NOT_FOUND_QUOTATION` | Quotation not found for tenant | `GET /api/v1/quotation/{id}` | Quotation lookup |
| `NOT_FOUND_LINE_ITEM` | Line item not found | `DELETE /api/v1/quotation/{id}/bom/item/{line_id}` | Line item lookup |

---

### Conflict Errors (409)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `CONFLICT_LINE_ITEM_LOCKED` | LINE_ITEM_LOCKED | `DELETE /api/v1/quotation/{id}/bom/item/{line_id}` | A5.2: is_locked enforcement |
| `CONFLICT_IMPORT_HAS_ERRORS` | Cannot commit import with validation errors. Fix errors first. | `POST /api/v1/catalog/skus/import` | Import validation |
| `CONFLICT_UPDATE_FAILED` | Quotation discount update failed (rowcount mismatch) | `PUT /api/v1/quotation/{id}/discount/quotation` | Update verification |
| `CONFLICT_APPLY_RECALC_FAILED` | Apply-Recalc failed: quotation not updated (rowcount mismatch) | `POST /api/v1/quotation/{id}/pricing/apply-recalc` | Update verification |

---

### Semantic Validation Errors (422)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `SEMANTIC_INVALID_TAX_MODE` | Invalid tax_mode on quotation | `POST /api/v1/quotation/{id}/pricing/preview` | Tax mode validation |
| `SEMANTIC_MISSING_DECISION_ID` | decision_id required for apply-recalc | `POST /api/v1/quotation/{id}/pricing/apply-recalc` | Audit requirement |

---

### Internal Server Errors (500)

| Error Code | Message | Endpoint | Context |
|------------|---------|----------|---------|
| `INTERNAL_QUERY_FAILED` | Query failed: {error} | `POST /api/v1/quotation/{id}/pricing/preview` | Database error |
| `INTERNAL_IMPORT_FAILED` | Import failed: {error} | `POST /api/v1/catalog/skus/import` | Import processing error |

---

## Error Code Format

**Pattern:** `{CATEGORY}_{SPECIFIC_ERROR}`

- **Category:** VALIDATION, AUTH, PERMISSION, NOT_FOUND, CONFLICT, SEMANTIC, INTERNAL, SERVICE
- **Specific Error:** Descriptive, uppercase, underscore-separated

**Examples:**
- `VALIDATION_INVALID_PRICE`
- `PERMISSION_INSUFFICIENT_ROLE`
- `CONFLICT_LINE_ITEM_LOCKED`

---

## Request ID Propagation

All error responses include `request_id` (UUID v4) for traceability.

**Implementation:**
- Generate at request entry (middleware)
- Include in all responses (success and error)
- Log in audit trail

---

## Version Header

All error responses include `version` field (e.g., `"v1"`) for API version tracking.

---

## Error Handling Best Practices

1. **Fail-Fast:** Validate at API layer before DB write
2. **Clear Messages:** Include field name, expected format, actual value
3. **Actionable:** Tell user how to fix the error
4. **Consistent:** Use standard error codes across all endpoints
5. **Traceable:** Include request_id for debugging
6. **Auditable:** Log errors to audit_logs table

---

## Implementation Plan (B3)

### Request ID Middleware

**Purpose:** Generate and propagate `request_id` (UUID v4) for all requests.

**Design:**
- Middleware runs at request entry (before route handlers)
- Generates UUID v4 and stores in request state
- Adds `X-Request-ID` response header
- Makes `request_id` available to all handlers via `request.state.request_id`

**FastAPI Implementation:**
```python
# app/middleware/request_id.py
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

**Integration:**
```python
# app/main.py
from app.middleware.request_id import RequestIDMiddleware

app.add_middleware(RequestIDMiddleware)
```

---

### Error Response Wrapper

**Purpose:** Standardize all error responses to match Error Taxonomy format.

**Design:**
- Exception handler intercepts `HTTPException` and unhandled exceptions
- Wraps error into standard format: `{detail, error_code, request_id, version}`
- Maps HTTP status codes to error code prefixes
- Extracts `request_id` from request state

**FastAPI Implementation:**
```python
# app/core/exceptions.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

def get_error_code_from_status(status_code: int, detail: str) -> str:
    """Map HTTP status to error code prefix"""
    if status_code == 400:
        return "VALIDATION_ERROR"  # Or parse from detail
    elif status_code == 401:
        return "AUTH_MISSING_TOKEN"
    elif status_code == 403:
        return "PERMISSION_INSUFFICIENT_ROLE"
    elif status_code == 404:
        return "NOT_FOUND_RESOURCE"
    elif status_code == 409:
        return "CONFLICT_BUSINESS_RULE"
    elif status_code == 422:
        return "SEMANTIC_VALIDATION_ERROR"
    elif status_code == 500:
        return "INTERNAL_SERVER_ERROR"
    else:
        return "UNKNOWN_ERROR"

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Standardize HTTPException responses"""
    request_id = getattr(request.state, "request_id", None)
    error_code = get_error_code_from_status(exc.status_code, exc.detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": error_code,
            "request_id": request_id or "unknown",
            "version": "v1"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions"""
    request_id = getattr(request.state, "request_id", None)
    logger.exception(f"Unhandled exception: {exc}", extra={"request_id": request_id})
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "request_id": request_id or "unknown",
            "version": "v1"
        }
    )
```

**Integration:**
```python
# app/main.py
from app.core.exceptions import (
    http_exception_handler,
    general_exception_handler
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
```

---

### Error Code Constants

**Purpose:** Centralize error codes for consistency.

**Design:**
- Create `app/core/error_codes.py` with all error code constants
- Use constants in exception handlers and endpoint code
- Enables IDE autocomplete and prevents typos

**Implementation:**
```python
# app/core/error_codes.py
class ErrorCodes:
    # Validation (400)
    VALIDATION_MISSING_REQUIRED = "VALIDATION_MISSING_REQUIRED"
    VALIDATION_INVALID_PRICE = "VALIDATION_INVALID_PRICE"
    VALIDATION_INVALID_CURRENCY = "VALIDATION_INVALID_CURRENCY"
    VALIDATION_INVALID_SKU = "VALIDATION_INVALID_SKU"
    VALIDATION_INVALID_STAGE = "VALIDATION_INVALID_STAGE"
    VALIDATION_INVALID_PAGINATION = "VALIDATION_INVALID_PAGINATION"
    VALIDATION_MISSING_TENANT = "VALIDATION_MISSING_TENANT"
    
    # Auth (401)
    AUTH_MISSING_TOKEN = "AUTH_MISSING_TOKEN"
    AUTH_INVALID_TOKEN = "AUTH_INVALID_TOKEN"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    
    # Permission (403)
    PERMISSION_INSUFFICIENT_ROLE = "PERMISSION_INSUFFICIENT_ROLE"
    PERMISSION_BULK_DISALLOWED = "PERMISSION_BULK_DISALLOWED"
    
    # Not Found (404)
    NOT_FOUND_ITEM = "NOT_FOUND_ITEM"
    NOT_FOUND_SKU = "NOT_FOUND_SKU"
    NOT_FOUND_QUOTATION = "NOT_FOUND_QUOTATION"
    NOT_FOUND_LINE_ITEM = "NOT_FOUND_LINE_ITEM"
    
    # Conflict (409)
    CONFLICT_LINE_ITEM_LOCKED = "CONFLICT_LINE_ITEM_LOCKED"
    CONFLICT_IMPORT_HAS_ERRORS = "CONFLICT_IMPORT_HAS_ERRORS"
    CONFLICT_UPDATE_FAILED = "CONFLICT_UPDATE_FAILED"
    CONFLICT_APPLY_RECALC_FAILED = "CONFLICT_APPLY_RECALC_FAILED"
    
    # Semantic (422)
    SEMANTIC_INVALID_TAX_MODE = "SEMANTIC_INVALID_TAX_MODE"
    SEMANTIC_MISSING_DECISION_ID = "SEMANTIC_MISSING_DECISION_ID"
    
    # Internal (500)
    INTERNAL_QUERY_FAILED = "INTERNAL_QUERY_FAILED"
    INTERNAL_IMPORT_FAILED = "INTERNAL_IMPORT_FAILED"
```

---

### Usage in Endpoints

**Before (inconsistent):**
```python
raise HTTPException(status_code=404, detail="Item not found")
```

**After (standardized):**
```python
from app.core.error_codes import ErrorCodes
from app.core.exceptions import StandardHTTPException

raise StandardHTTPException(
    status_code=404,
    error_code=ErrorCodes.NOT_FOUND_ITEM,
    detail="Item not found"
)
```

Or use helper:
```python
from app.core.exceptions import raise_not_found

raise_not_found(ErrorCodes.NOT_FOUND_ITEM, "Item not found")
```

---

## Next Steps

1. ✅ **Design complete** — Middleware and exception handler plan documented
2. ⏳ **Implement request_id middleware** — Add `RequestIDMiddleware` to `app/middleware/`
3. ⏳ **Implement error wrapper** — Add exception handlers to `app/core/exceptions.py`
4. ⏳ **Add error code constants** — Create `app/core/error_codes.py`
5. ⏳ **Update existing endpoints** — Replace `HTTPException` with standardized format
6. ⏳ **Add error code documentation** — Update OpenAPI spec with error response examples


