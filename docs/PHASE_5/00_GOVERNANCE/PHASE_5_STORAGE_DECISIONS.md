# Phase-5 Storage Decisions - SC_Lx and Accessory Compatibility

**Date:** 2026-01-03  
**Status:** ✅ LOCKED  
**Owner:** Phase 5 Senate  
**Purpose:** Explicit storage decisions for SC_Lx structural classification and accessory compatibility

---

## Decision D-SCL-01: SC_Lx Storage Location

### ✅ DECISION: Option A - JSONB Column in catalog_skus

**Selected Option:** Store SC_L1 through SC_L8 as JSONB column in `catalog_skus` table

**Implementation:**
```sql
ALTER TABLE catalog_skus 
ADD COLUMN sc_struct_jsonb JSONB;

CREATE INDEX idx_catalog_skus_sc_struct ON catalog_skus USING GIN (sc_struct_jsonb);
```

**Structure:**
```json
{
  "l1": "FRAME-1",
  "l2": "3P",
  "l3": "AC_COIL",
  "l4": "ACCESSORY_CLASS",
  "l5": null,
  "l6": null,
  "l7": null,
  "l8": null
}
```

**Rationale:**
1. ✅ Lowest migration complexity (single column addition)
2. ✅ No additional joins required
3. ✅ Works for all product types uniformly
4. ✅ Queryable using PostgreSQL JSONB operators
5. ✅ Fast to implement for Week-1/2
6. ✅ Can normalize to separate table in Phase-6 if needed

**Alternative Considered:**
- Option B: Separate `catalog_sku_structure` table
- **Rejected:** More tables/joins, slower implementation, not needed for Phase-5

**Status:** ✅ **LOCKED** - Implement in Week-1 Day 1-2 migrations

---

## Decision D-ACC-01: Accessory Compatibility Storage

### ✅ DECISION: Option A - Reference Table

**Selected Option:** Create `accessory_compatibility` table as reference data

**Implementation:**
```sql
CREATE TABLE accessory_compatibility (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    parent_make VARCHAR(100) NOT NULL,
    parent_series_code VARCHAR(100) NOT NULL,
    accessory_sku_code VARCHAR(255) NOT NULL,
    applies_to_range TEXT,
    notes TEXT,
    source_page VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

CREATE INDEX idx_accessory_compatibility_tenant_id ON accessory_compatibility(tenant_id);
CREATE INDEX idx_accessory_compatibility_parent ON accessory_compatibility(parent_make, parent_series_code);
CREATE INDEX idx_accessory_compatibility_accessory ON accessory_compatibility(accessory_sku_code);
```

**Rationale:**
1. ✅ Clean, explicit structure
2. ✅ Easy to query and display
3. ✅ Stable schema (no JSON parsing needed)
4. ✅ Reference data only (no enforcement in Phase-5)
5. ✅ Can be extended later without breaking changes

**Alternative Considered:**
- Option B: JSONB column in catalog_skus or separate compat_map table
- **Rejected:** Less explicit, harder to query, more complex

**Enforcement Policy:**
- ✅ **Phase-5:** Store and query only (reference data)
- ❌ **Phase-5:** No enforcement logic (no blocking of incompatible accessories)
- 🔮 **Phase-6+:** Enforcement rules engine (future)

**Status:** ✅ **LOCKED** - Implement in Week-1 Day 1-2 migrations

---

## Schema Canon Updates Required

### Update 1: catalog_skus table

Add to `NSW_SCHEMA_CANON_v1.0.md`:

```sql
ALTER TABLE catalog_skus 
ADD COLUMN sc_struct_jsonb JSONB;

CREATE INDEX idx_catalog_skus_sc_struct ON catalog_skus USING GIN (sc_struct_jsonb);
```

**Version:** v1.1 (additive change, non-breaking)

### Update 2: accessory_compatibility table

Add to `NSW_SCHEMA_CANON_v1.0.md`:

```sql
CREATE TABLE accessory_compatibility (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    parent_make VARCHAR(100) NOT NULL,
    parent_series_code VARCHAR(100) NOT NULL,
    accessory_sku_code VARCHAR(255) NOT NULL,
    applies_to_range TEXT,
    notes TEXT,
    source_page VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

CREATE INDEX idx_accessory_compatibility_tenant_id ON accessory_compatibility(tenant_id);
CREATE INDEX idx_accessory_compatibility_parent ON accessory_compatibility(parent_make, parent_series_code);
CREATE INDEX idx_accessory_compatibility_accessory ON accessory_compatibility(accessory_sku_code);
```

**Version:** v1.1 (new table, non-breaking)

---

## Impact on Importer

### SC_Lx Processing

**Source:** `SC_L1` through `SC_L8` columns from normalized master

**Processing:**
```python
sc_struct = {
    "l1": row.get("SC_L1"),
    "l2": row.get("SC_L2"),
    "l3": row.get("SC_L3"),
    "l4": row.get("SC_L4"),
    "l5": row.get("SC_L5"),
    "l6": row.get("SC_L6"),
    "l7": row.get("SC_L7"),
    "l8": row.get("SC_L8")
}
# Remove None/null values
sc_struct = {k: v for k, v in sc_struct.items() if v is not None and v != ""}

# Insert into catalog_skus.sc_struct_jsonb
```

### Accessory Compatibility Processing

**Source:** `ACCESSORY_COMPATIBILITY` sheet from normalized master

**Processing:**
```python
# For each row in ACCESSORY_COMPATIBILITY sheet:
insert into accessory_compatibility (
    tenant_id,
    parent_make,
    parent_series_code,
    accessory_sku_code,
    applies_to_range,
    notes,
    source_page
) values (...)
```

---

## Migration Scripts Required

### Migration 1: Add SC_Lx JSONB column

**File:** `backend/alembic/versions/XXXX_add_sc_struct_to_catalog_skus.py`

**Content:**
- Add `sc_struct_jsonb JSONB` column to `catalog_skus`
- Create GIN index on JSONB column
- No data migration needed (populated by importer)

### Migration 2: Create accessory_compatibility table

**File:** `backend/alembic/versions/XXXX_create_accessory_compatibility.py`

**Content:**
- Create `accessory_compatibility` table
- Create indexes
- No initial data (populated by importer)

---

## Testing Requirements

### SC_Lx Storage Test

1. Import LC1D row with SC_L1='FRAME-1', SC_L2='3P'
2. Verify `catalog_skus.sc_struct_jsonb` contains correct JSON
3. Query using JSONB operators: `WHERE sc_struct_jsonb->>'l1' = 'FRAME-1'`
4. Verify works for EOCR, MPCB, Accessories (all product types)

### Accessory Compatibility Test

1. Import `ACCESSORY_COMPATIBILITY` sheet
2. Verify rows inserted into `accessory_compatibility` table
3. Query compatibility: `SELECT * FROM accessory_compatibility WHERE parent_series_code = 'LC1D'`
4. Verify no enforcement logic (can add incompatible accessories in Phase-5)

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-01-03 | D-SCL-01: JSONB column in catalog_skus | Fast implementation, works for all product types |
| 2026-01-03 | D-ACC-01: Reference table for compatibility | Clean structure, easy to query, reference only |

---

**Status:** ✅ **DECISIONS LOCKED**  
**Next Action:** Implement in Week-1 Day 1-2 migrations

