# Running Catalog Import Tests

## Current Status

✅ **Migrations Applied**: Both migrations are now applied
- `f43171814116` - create catalog tables
- `6fbca98f32b1` - catalog current price + skuprice audit + make nullable

⚠️ **Server Issue**: The running server instance appears to be an older version that doesn't have the catalog endpoints registered.

## Solution: Restart the Server

The server needs to be restarted to pick up the latest code changes. Here's how:

### Step 1: Stop Current Server

Find and stop the running server:

```bash
# Find the process
ps aux | grep uvicorn

# Kill it (replace PID with actual process ID)
kill <PID>

# Or if running in a terminal, just press Ctrl+C
```

### Step 2: Start Fresh Server

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8003
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8003 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Verify Endpoints

In a new terminal, verify the endpoints are registered:

```bash
curl http://localhost:8003/openapi.json | python3 -m json.tool | grep -A 2 "catalog"
```

You should see catalog endpoints listed.

### Step 4: Run Tests

```bash
cd backend
source venv/bin/activate
python3 test_catalog_import.py
```

## Alternative: Manual Testing

If the automated script doesn't work, test manually:

### Test 1: Dry Run

```bash
curl -X POST "http://localhost:8003/api/v1/catalog/skus/import?dry_run=true" \
  -F "file=@../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv" \
  | python3 -m json.tool
```

### Test 2: Check Database

```bash
# Connect to database
docker exec -it nsw_postgres psql -U nsw_user -d nsw_estimation

# Or if using local postgres
psql -h localhost -p 5433 -U nsw_user -d nsw_estimation
```

Then run:
```sql
SELECT COUNT(*) FROM catalog_items;
SELECT COUNT(*) FROM catalog_skus;
SELECT COUNT(*) FROM sku_prices;
```

## Expected Results

After restarting the server and running tests:

1. ✅ Dry run should return validation results
2. ✅ Commit should create:
   - 1 catalog item (grouped by series)
   - 25 SKUs (one per row in CSV)
   - 25 price records in sku_prices
   - 1 price list

3. ✅ GET endpoints should return data:
   ```bash
   curl "http://localhost:8003/api/v1/catalog/skus?limit=5"
   ```

## Troubleshooting

### Server still returns 404

- Check server logs for import errors
- Verify `app/api/v1/router.py` includes catalog router
- Check `app/main.py` includes the API router

### Import fails with errors

- Check CSV has `import_stage=FINAL` (not TEST)
- Verify all required columns: make, sku_code, uom, list_price, currency
- Check database connection in `.env` file

### Migration errors

If you see "multiple heads" or other migration issues:

```bash
alembic history
alembic heads
alembic merge -m "merge heads" heads
alembic upgrade head
```

