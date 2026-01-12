# Development Database Setup

## Quick Start

### 0. Start Backend with Postgres

**Recommended:** Use the run script (guarantees Postgres connection):

```bash
./backend/scripts/run_backend_postgres.sh
```

This script:
- Sets `DATABASE_URL` to Postgres
- Starts uvicorn with reload
- Works with Shortcuts/automation

**Alternative:** Manual export
```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/nsw_dev"
cd backend
uvicorn app.main:app --reload --port 8003
```

### 1. Start Postgres Container

```bash
docker rm -f nsw_pg >/dev/null 2>&1 || true

docker run -d \
  --name nsw_pg \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=nsw_dev \
  -p 5433:5432 \
  postgres:16-alpine
```

### 2. Apply Schema

```bash
cat docs/PHASE_5/04_SCHEMA_CANON/DDL/schema.sql | docker exec -i nsw_pg psql -U postgres -d nsw_dev
```

### 3. Seed Test Data (Optional)

```bash
cat backend/scripts/seed_dev_data.sql | docker exec -i nsw_pg psql -U postgres -d nsw_dev
```

### 4. Start Backend with Postgres

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/nsw_dev"
cd backend
uvicorn app.main:app --reload --port 8003
```

## Verify Setup

### Check Tables Created
```bash
docker exec -i nsw_pg psql -U postgres -d nsw_dev -c "select count(*) as tables from information_schema.tables where table_schema='public';"
```
Expected: 34 tables

### Test BOM Explode (Unmapped)
```bash
curl -s -X POST http://127.0.0.1:8003/api/v1/bom/explode \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: 1" \
  -d '{"l1_intent_line_ids":[999999]}' | python -m json.tool
```

Expected: HTTP 200 with `unmapped[]` containing the ID, not 500.

### Test BOM Explode (Happy Path - after seeding)
```bash
curl -s -X POST http://127.0.0.1:8003/api/v1/bom/explode \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: 1" \
  -d '{"l1_intent_line_ids":[1001],"include_sku":true,"aggregate_by_sku":true}' | python -m json.tool
```

Expected: HTTP 200 with `items[]` containing catalog_sku_id=501.

## Clean Up

```bash
docker stop nsw_pg
# Or delete completely:
docker rm -f nsw_pg
```

## Seed Data Details

The seed script (`seed_dev_data.sql`) creates:
- Tenant ID: 1
- Category ID: 1
- Product Type ID: 1
- Catalog SKU ID: 501 (oem_catalog_no: 'DEV-SKU-001')
- L1 Intent Line ID: 1001
- L1->L2 Mapping ID: 9001

## Dependencies

Ensure `psycopg2-binary` is installed:
```bash
pip install psycopg2-binary
```

## Expected Test Outputs

### Unmapped Test (L1_NOT_FOUND)
```bash
curl -s -X POST http://127.0.0.1:8003/api/v1/bom/explode \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: 1" \
  -d '{"l1_intent_line_ids":[999999]}' | python -m json.tool
```

**Expected Response:**
```json
{
    "tenant_id": 1,
    "input": {
        "l1_intent_line_ids": [999999]
    },
    "summary": {
        "l1_lines_requested": 1,
        "l1_lines_found": 0,
        "mappings_found": 0,
        "skus_found": 0,
        "unmapped_l1_lines": 1
    },
    "unmapped": [
        {
            "l1_intent_line_id": 999999,
            "reason": "L1_NOT_FOUND"
        }
    ],
    "items": [],
    "warnings": ["HAS_UNMAPPED_L1_LINES"]
}
```

### Happy-Path Test (Seeded Data)
```bash
curl -s -X POST http://127.0.0.1:8003/api/v1/bom/explode \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: 1" \
  -d '{"l1_intent_line_ids":[1001],"include_sku":true,"aggregate_by_sku":true}' | python -m json.tool
```

**Expected Response:**
```json
{
    "tenant_id": 1,
    "input": {
        "l1_intent_line_ids": [1001]
    },
    "summary": {
        "l1_lines_requested": 1,
        "l1_lines_found": 1,
        "mappings_found": 1,
        "skus_found": 1,
        "unmapped_l1_lines": 0
    },
    "unmapped": [],
    "items": [
        {
            "catalog_sku_id": 501,
            "make": "DEV-MAKE",
            "oem_catalog_no": "DEV-SKU-001",
            "uom": "EA",
            "sku_code": "DEV-SKU-001",
            "name": "DEV-MAKE",
            "mapping_count": 1,
            "mapping_types": ["BASE"],
            "l1_sources": [
                {
                    "l1_intent_line_id": 1001,
                    "mapping_type": "BASE",
                    "is_primary": true
                }
            ]
        }
    ],
    "warnings": []
}
```

### Missing Tenant Test (Error Envelope)
```bash
curl -s -X POST http://127.0.0.1:8003/api/v1/bom/explode \
  -H "Content-Type: application/json" \
  -d '{"l1_intent_line_ids":[1001]}' | python -m json.tool
```

**Expected Response:**
```json
{
    "detail": "X-Tenant-ID header required",
    "error_code": "VALIDATION_MISSING_TENANT",
    "request_id": "...",
    "version": "v1"
}
```

