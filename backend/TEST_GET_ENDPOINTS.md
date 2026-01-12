# GET Endpoints Test Guide

All 4 GET endpoints have been implemented and are ready for testing.

## Implemented Endpoints

### 1. GET /api/v1/catalog/items
- **Pagination**: `limit`, `offset`
- **Search**: `q` matches `item_code` or `name`
- **Filter**: `make`

### 2. GET /api/v1/catalog/items/{item_id}
- Returns item details + all its SKUs
- Includes current price snapshot from each SKU

### 3. GET /api/v1/catalog/skus
- **Pagination**: `limit`, `offset`
- **Search**: `q` matches `sku_code`, `name`, or `description`
- **Filters**: `make`, `item_id`

### 4. GET /api/v1/catalog/skus/{sku_id}
- Returns SKU details + price history (latest 50)
- Includes `import_batch_id` and `source_file` for audit trail

## Quick Tests

**Note**: The server should be running on port 8001 (or 8011 if you've configured it differently).

### Test 1: List Items
```bash
curl "http://localhost:8001/api/v1/catalog/items?limit=10" | python3 -m json.tool
```

### Test 2: List Items with Search
```bash
curl "http://localhost:8001/api/v1/catalog/items?q=Schneider&limit=10" | python3 -m json.tool
```

### Test 3: List Items by Make
```bash
curl "http://localhost:8001/api/v1/catalog/items?make=Schneider&limit=10" | python3 -m json.tool
```

### Test 4: Get Item by ID (with SKUs)
```bash
# First, get an item ID from the list endpoint
ITEM_ID=1
curl "http://localhost:8001/api/v1/catalog/items/$ITEM_ID" | python3 -m json.tool
```

### Test 5: List SKUs
```bash
curl "http://localhost:8001/api/v1/catalog/skus?limit=10" | python3 -m json.tool
```

### Test 6: List SKUs with Search
```bash
curl "http://localhost:8001/api/v1/catalog/skus?q=LC1E&limit=10" | python3 -m json.tool
```

### Test 7: List SKUs by Make
```bash
curl "http://localhost:8001/api/v1/catalog/skus?make=Schneider&limit=10" | python3 -m json.tool
```

### Test 8: List SKUs by Item ID
```bash
ITEM_ID=1
curl "http://localhost:8001/api/v1/catalog/skus?item_id=$ITEM_ID&limit=10" | python3 -m json.tool
```

### Test 9: Get SKU by ID (with Price History)
```bash
# First, get a SKU ID from the list endpoint
SKU_ID=1
curl "http://localhost:8001/api/v1/catalog/skus/$SKU_ID" | python3 -m json.tool
```

## Expected Response Formats

### List Items Response
```json
{
  "total": 1,
  "limit": 50,
  "offset": 0,
  "items": [
    {
      "id": 1,
      "item_code": "SCHNEIDER__EASY_TESYS_POWER_CONTACTORS_LC1E_3P",
      "name": "Easy TeSys Power Contactors (LC1E, 3P)",
      "make": "Schneider",
      "category": "Contactor",
      "is_active": true,
      "created_at": "2025-12-26T...",
      "updated_at": "2025-12-26T..."
    }
  ]
}
```

### Get Item Response (with SKUs)
```json
{
  "id": 1,
  "item_code": "SCHNEIDER__EASY_TESYS_POWER_CONTACTORS_LC1E_3P",
  "name": "Easy TeSys Power Contactors (LC1E, 3P)",
  "description": null,
  "make": "Schneider",
  "category": "Contactor",
  "is_active": true,
  "created_at": "2025-12-26T...",
  "updated_at": "2025-12-26T...",
  "skus": [
    {
      "id": 1,
      "sku_code": "LC1E40B01",
      "sku_type": "PRIMARY",
      "name": "LC1E40B01",
      "description": "Contactor | FRAME-1 | AC1=50 A | AC3=40 A | HP=29 | kW=22 | Aux(NO/NC)=-/1",
      "make": "Schneider",
      "uom": "EA",
      "is_active": true,
      "current_price": "7680.00",
      "current_currency": "INR",
      "current_price_updated_at": "2025-12-26T..."
    }
  ]
}
```

### List SKUs Response
```json
{
  "total": 25,
  "limit": 50,
  "offset": 0,
  "skus": [
    {
      "id": 1,
      "catalog_item_id": 1,
      "sku_code": "LC1E40B01",
      "sku_type": "PRIMARY",
      "name": "LC1E40B01",
      "make": "Schneider",
      "uom": "EA",
      "is_active": true,
      "current_price": "7680.00",
      "current_currency": "INR",
      "current_price_updated_at": "2025-12-26T..."
    }
  ]
}
```

### Get SKU Response (with Price History)
```json
{
  "id": 1,
  "catalog_item_id": 1,
  "sku_code": "LC1E40B01",
  "sku_type": "PRIMARY",
  "name": "LC1E40B01",
  "description": "Contactor | FRAME-1 | AC1=50 A | AC3=40 A | HP=29 | kW=22 | Aux(NO/NC)=-/1",
  "make": "Schneider",
  "uom": "EA",
  "is_active": true,
  "current_price": "7680.00",
  "current_currency": "INR",
  "current_price_updated_at": "2025-12-26T...",
  "price_history": [
    {
      "id": 1,
      "price_list_id": 1,
      "price": "7680.00",
      "currency": "INR",
      "effective_from": "2025-12-26T...",
      "effective_to": null,
      "import_batch_id": "uuid-here",
      "source_file": "schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv",
      "created_at": "2025-12-26T..."
    }
  ]
}
```

## Testing After Import

1. **Import data first** (if not already done):
   ```bash
   curl -X POST "http://localhost:8001/api/v1/catalog/skus/import?dry_run=false" \
     -F "file=@../tools/price_normalizer/output/final/schneider_Schneider_LC1E_Contactors_FINAL_2025-12-26_normalized_20251226_091423.csv"
   ```

2. **Then test GET endpoints** to verify the imported data is accessible.

## Notes

- All endpoints return paginated results with `total`, `limit`, and `offset`
- Search uses case-insensitive `ILIKE` matching
- Price values are returned as strings to avoid precision issues
- Price history is limited to latest 50 records per SKU
- All endpoints include proper error handling (404 for not found)

