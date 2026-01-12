# Catalog Import Test Guide

This guide walks you through testing the catalog import endpoint with all the fixes applied.

## Prerequisites

1. **Database running**: Ensure PostgreSQL is running (via docker-compose or directly)
2. **Backend server running**: FastAPI server should be running on port 8003
3. **Migrations applied**: Alembic migrations should be up to date

## Step 1: Check Database & Run Migrations

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # or: . venv/bin/activate

# Check current migration status
alembic current

# If no migrations applied, run them
alembic upgrade head

# Verify tables exist
alembic history
```

**Expected output**: Should show both migrations:
- `f43171814116` - create catalog tables
- `6fbca98f32b1` - catalog current price + skuprice audit + make nullable

## Step 2: Start Backend Server (if not running)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8003
```

**Verify server is running**:
```bash
curl http://localhost:8003/
# Should return: {"message":"NSW Estimation Software API",...}
```

## Step 3: Run Automated Tests

### Option A: Python Test Script (Recommended)

```bash
cd backend
source venv/bin/activate
python3 test_catalog_import.py
```

This script will:
1. ✅ Check if server is running
2. ✅ Verify catalog endpoints are registered
3. ✅ Find the FINAL CSV file
4. ✅ Test dry_run=true (validation only)
5. ✅ Test dry_run=false (actual import) - with confirmation prompt
6. ✅ Verify GET endpoints work

### Option B: Manual curl Tests

#### Test 1: Dry Run (Validation Only)

```bash
curl -X POST "http://localhost:8003/api/v1/catalog/skus/import?dry_run=true" \
  -F "file=@../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv" \
  | python3 -m json.tool
```

**Expected response**:
```json
{
  "batch_id": "uuid-here",
  "source_file": "schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv",
  "rows_total": 25,
  "rows_valid": 25,
  "rows_error": 0,
  "dry_run": true,
  "errors_sample": []
}
```

#### Test 2: Actual Import (Commit to Database)

```bash
curl -X POST "http://localhost:8003/api/v1/catalog/skus/import?dry_run=false" \
  -F "file=@../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv" \
  | python3 -m json.tool
```

**Expected response**:
```json
{
  "batch_id": "uuid-here",
  "source_file": "schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv",
  "rows_total": 25,
  "rows_valid": 25,
  "rows_error": 0,
  "dry_run": false,
  "items_created": 1,
  "skus_created": 25,
  "skus_updated": 0,
  "prices_inserted": 25,
  "price_list_id": 1,
  "price_list_name": "Schneider - schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv"
}
```

#### Test 3: Verify GET Endpoints

```bash
# List SKUs
curl "http://localhost:8003/api/v1/catalog/skus?limit=5" | python3 -m json.tool

# List items
curl "http://localhost:8003/api/v1/catalog/items?limit=5" | python3 -m json.tool
```

## Step 4: Verify Database

Connect to PostgreSQL and verify data:

```bash
# Using psql (if available)
psql -h localhost -p 5433 -U nsw_user -d nsw_estimation

# Or using docker
docker exec -it nsw_postgres psql -U nsw_user -d nsw_estimation
```

**SQL Queries**:

```sql
-- Check catalog items created
SELECT id, item_code, name, make, category FROM catalog_items;

-- Check SKUs created
SELECT id, sku_code, make, series, current_price, current_currency 
FROM catalog_skus 
ORDER BY created_at DESC 
LIMIT 10;

-- Check price history
SELECT sp.id, cs.sku_code, sp.price, sp.currency, sp.import_batch_id, sp.source_file
FROM sku_prices sp
JOIN catalog_skus cs ON sp.sku_id = cs.id
ORDER BY sp.created_at DESC
LIMIT 10;

-- Check price list
SELECT id, name, currency, effective_from, is_active FROM price_lists;
```

## Test Scenarios

### ✅ Test FINAL-only Enforcement

Try importing a TEST file (should be rejected):

```bash
curl -X POST "http://localhost:8003/api/v1/catalog/skus/import?dry_run=true" \
  -F "file=@../tools/price_normalizer/output/test/schneider_Schneider_Switching_Controlling_TEST1_normalized_20251226_090751.csv" \
  | python3 -m json.tool
```

**Expected**: Should return errors with "Only FINAL imports allowed"

### ✅ Test Idempotent PriceList

Import the same FINAL file twice:

```bash
# First import
curl -X POST "http://localhost:8001/api/v1/catalog/skus/import?dry_run=false" \
  -F "file=@../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv"

# Second import (should reuse same PriceList)
curl -X POST "http://localhost:8001/api/v1/catalog/skus/import?dry_run=false" \
  -F "file=@../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv"
```

**Expected**: Both should succeed, and the same `price_list_id` should be reused.

## Troubleshooting

### Server returns 404

- Check if server is running: `curl http://localhost:8003/`
- Check server logs for import errors
- Verify endpoint is registered: `curl http://localhost:8003/openapi.json | grep catalog`

### Import fails with validation errors

- Check CSV format matches expected columns
- Verify `import_stage` is "FINAL" (not "TEST")
- Check required fields: make, sku_code, uom, list_price, currency

### Database connection errors

- Verify PostgreSQL is running: `docker ps | grep postgres`
- Check DATABASE_URL in `.env` file
- Verify migrations are applied: `alembic current`

### Migration errors

If you see "multiple heads" error:

```bash
# Check migration history
alembic history

# If two migrations both have down_revision=None, fix the chain:
# Edit 6fbca98f32b1 migration to have down_revision='f43171814116'
```

## Summary

After running all tests, you should have:

1. ✅ Database tables created (catalog_items, catalog_skus, sku_prices, price_lists)
2. ✅ FINAL CSV imported successfully
3. ✅ Catalog items created (grouped by series)
4. ✅ SKUs created with current_price snapshot
5. ✅ Price history archived in sku_prices table
6. ✅ GET endpoints returning data

All 5 fixes are verified:
- ✅ Fix 1: FINAL-only enforcement
- ✅ Fix 2: Stable item_code (slugify)
- ✅ Fix 3: PriceList idempotent reuse
- ✅ Fix 4: CatalogSku.make NOT NULL
- ✅ Fix 5: SkuPrice audit fields

