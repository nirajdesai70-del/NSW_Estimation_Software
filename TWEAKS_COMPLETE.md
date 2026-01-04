# High-Leverage Tweaks Complete

**Date:** 2025-12-26  
**Status:** ✅ COMPLETE

---

## Changes Applied

### 1. ✅ Date Consistency Fix
- Updated all documentation dates from `2025-01-27` to `2025-12-26`
- Files updated:
  - `NEW_BUILD_SETUP_COMPLETE.md`
  - `NEW_BUILD_ARCHITECTURE.md`
  - `QUICK_START.md` (if dates present)

### 2. ✅ Dev-Only Mode Policy Created
- **File:** `docs/GOVERNANCE/DEV_ONLY_MODE_POLICY.md`
- **Rules established:**
  - PostgreSQL is dev-only
  - Legacy MySQL is reference-only
  - No live sync
  - Imports are one-way seed snapshots only
  - No AI/NL→SQL in runtime paths

### 3. ✅ Database Naming + Alembic Standardization
- **Updated:** `backend/app/core/database.py`
  - Added automatic psycopg driver conversion
  - Ensures `postgresql+psycopg://` format for Alembic compatibility
  - Single SQLAlchemy Base clearly documented
  
- **Updated:** `backend/alembic/env.py`
  - Added psycopg driver conversion for Alembic migrations
  - Ensures consistent driver usage

- **Updated:** `.env.example` reference
  - Changed `DATABASE_URL` format to `postgresql+psycopg://`

### 4. ✅ CORS + Auth Token Flow Hardening
- **Updated:** `backend/app/core/config.py`
  - CORS origins restricted to `http://localhost:3000` and `http://127.0.0.1:3000` only

- **Updated:** `frontend/src/services/api.ts`
  - Enhanced 401 error handling with token refresh
  - Refresh token attempt on 401
  - Retry original request after refresh
  - Clean logout if refresh fails

### 5. ✅ Catalog + SKU Mapping ADR Created
- **File:** `docs/ADR/ADR_0001_CATALOG_SKU_MAPPING.md`
- **Establishes:**
  - SKU types: PRIMARY, BUILT_IN, ADDON, OPTIONAL, MANDATORY_SPLIT
  - Rule: L1 → explodes into one or more priced lines
  - Rule: Imported price list is SKU-level truth
  - Output: multi-SKU becomes multiple quotation line items
  - Implementation sequence defined

---

## Current Database Configuration

### `backend/app/core/database.py`
```python
# Single SQLAlchemy Base for all models
Base = declarative_base()

# Automatic psycopg driver conversion
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://") and "+psycopg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
```

### `backend/alembic/env.py`
```python
# Import Base from database module
from app.core.database import Base

# Target metadata for autogenerate
target_metadata = Base.metadata

# Psycopg driver conversion for Alembic
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://") and "+psycopg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
config.set_main_option("sqlalchemy.url", database_url)
```

**Status:** ✅ Migrations are correctly wired. Single Base, proper driver, target_metadata set correctly.

---

## Ready for Catalog + SKU Import Implementation

All high-leverage tweaks complete. The system is now ready for:
1. Catalog + SKU import implementation
2. Database schema creation following ADR-0001
3. BOM explosion logic with multi-SKU support

---

**END OF TWEAKS COMPLETE**

