# Database + Migration Setup Complete

**Date:** 2025-12-26  
**Status:** ✅ READY FOR FIRST MIGRATION

---

## Critical Fixes Applied

### 1. ✅ SQLAlchemy 2.0 Style Base
- **Updated:** `backend/app/core/database.py`
- **Change:** Upgraded from `declarative_base()` to `DeclarativeBase` class
- **Result:** Modern, future-proof base class

```python
class Base(DeclarativeBase):
    """SQLAlchemy 2.0 style declarative base for all models"""
    pass
```

### 2. ✅ Model Import in Alembic
- **Updated:** `backend/alembic/env.py`
- **Change:** Added `import app.models` before `target_metadata = Base.metadata`
- **Result:** Alembic can now see all tables during autogenerate

### 3. ✅ Type & Default Comparison
- **Updated:** `backend/alembic/env.py`
- **Change:** Added `compare_type=True` and `compare_server_default=True` to both migration functions
- **Result:** Alembic will detect column type and default value changes

### 4. ✅ Models Structure Created
- **Created:** `backend/app/models/__init__.py`
- **Created:** `backend/app/models/catalog.py`
- **Result:** First model set ready (CatalogItem, CatalogSku, PriceList, SkuPrice)

### 5. ✅ SKU-First Endpoints
- **Updated:** `backend/app/api/v1/endpoints/catalog.py`
- **Change:** Restructured to SKU-first with proper endpoints
- **Result:** `/catalog/skus/import` is the main import endpoint

---

## Router Structure (Verified)

**Path Structure:**
```
main.py: app.include_router(api_router, prefix="/api/v1")
  └─> router.py: api_router.include_router(catalog.router, prefix="/catalog")
      └─> Final paths:
          - GET /api/v1/catalog/items
          - GET /api/v1/catalog/items/{item_id}
          - GET /api/v1/catalog/skus
          - GET /api/v1/catalog/skus/{sku_id}
          - POST /api/v1/catalog/skus/import
```

✅ **No double prefixes** - Clean path structure

---

## Current File Contents

### `backend/app/core/database.py`
```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """SQLAlchemy 2.0 style declarative base for all models"""
    pass
```

### `backend/alembic/env.py`
```python
# IMPORTANT: Import models so metadata is populated
import app.models  # noqa: F401

target_metadata = Base.metadata

# Both migration functions have:
context.configure(
    ...
    compare_type=True,
    compare_server_default=True,
)
```

### `backend/app/models/__init__.py`
```python
from .catalog import *  # noqa: F401, F403
```

---

## Catalog Model Schema (v1)

### Tables Created:
1. **catalog_items** - Item grouping/browse entity
2. **catalog_skus** - SKU (pricing truth) with SKU types
3. **price_lists** - Price list containers
4. **sku_prices** - SKU-level prices

### Key Features:
- SKU types: PRIMARY, BUILT_IN, ADDON, OPTIONAL, MANDATORY_SPLIT
- Unique constraint: `(make, sku_code)` for SKUs
- Foreign keys with CASCADE deletes
- Indexes on search fields

---

## Next Steps

### Step 1: Run First Migration
```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "init catalog sku model"
alembic upgrade head
```

### Step 2: Verify Tables Created
```bash
# Connect to Postgres and verify
psql -U nsw_user -d nsw_estimation -c "\dt"
```

Expected tables:
- catalog_items
- catalog_skus
- price_lists
- sku_prices
- alembic_version

### Step 3: Test Endpoints
```bash
# Start server
uvicorn app.main:app --reload --port 8001

# Test health
curl http://localhost:8001/health

# Test catalog endpoints (will return empty for now)
curl http://localhost:8001/api/v1/catalog/items
curl http://localhost:8001/api/v1/catalog/skus
```

---

## Price List Import Schema (v1)

**Minimum Required Columns:**
- `make` - Manufacturer name
- `sku_code` - SKU code (or part_no)
- `description` - SKU description
- `uom` - Unit of measure
- `list_price` - Price value
- `currency` - Currency code (optional, default: INR)
- `effective_from` - Effective date (optional)

**CSV/XLSX Format:**
```csv
make,sku_code,description,uom,list_price,currency,effective_from
Schneider,SW-123,Panel Switch,EA,100.00,INR,2025-01-01
Schneider,PSU-5V,Power Supply,EA,15.00,INR,2025-01-01
```

---

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| SQLAlchemy Base | ✅ | 2.0 style DeclarativeBase |
| Alembic Config | ✅ | Model imports + compare flags |
| Model Structure | ✅ | Catalog models created |
| Endpoints | ✅ | SKU-first endpoints ready |
| Router Paths | ✅ | Clean /api/v1/catalog/* paths |
| Migration Ready | ✅ | Ready to run first migration |

---

## Verification Checklist

- [x] Base uses DeclarativeBase (SQLAlchemy 2.0)
- [x] Models imported in env.py
- [x] compare_type and compare_server_default enabled
- [x] Catalog models created with SKU types
- [x] Endpoints restructured to SKU-first
- [x] Router paths verified (no double prefixes)
- [x] Price list schema documented

---

**Status:** ✅ **READY FOR FIRST MIGRATION**

Run `alembic revision --autogenerate -m "init catalog sku model"` to create your first migration.

---

**END OF SETUP COMPLETE**

