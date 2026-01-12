# Inventory CSV Files - Content Explanation

**Question:** Do the CSV inventory files contain table structure metadata or actual data records?

**Answer:** ✅ **SCHEMA METADATA ONLY** - They contain table structure information, NOT actual data records.

---

## What the CSV Files Contain

### 1. Key-Only Inventory CSV
**File:** `NSW_SCHEMA_TABLE_INVENTORY_KEY_ONLY_v1.0.csv`

**Content:** Schema metadata (one row per table)

**Columns:**
- `module` - Module name (AUTH, CIM, MBOM, etc.)
- `table_name` - Table name
- `tenant_scoped` - Y/N for tenant isolation
- `primary_key` - Primary key column name
- `unique_keys` - Unique constraint definitions
- `foreign_keys` - Foreign key relationships
- `checks` - CHECK constraint definitions
- `indexes` - Index names
- `notes` - Additional notes

**Example Row:**
```csv
AI,ai_call_logs,N,id,—,tenant_id->tenants.id (RESTRICT),—,idx_ai_call_logs_tenant_id; ix_ai_call_logs_3660124,
```

**Count:** 30 rows (one per table) + 1 header row = 31 lines total

---

### 2. Full Inventory CSV (Missing/Empty)
**File:** `NSW_SCHEMA_TABLE_INVENTORY_v1.0.csv`

**Intended Content:** Schema metadata (one row per column)

**Intended Columns:**
- `table_name` - Table name
- `column_name` - Column name
- `data_type` - Data type (BIGINT, VARCHAR, etc.)
- `nullable` - NULL/NOT NULL
- `default` - Default value
- `pk` - Is primary key (Y/N)
- `fk_ref` - Foreign key reference
- `indexes` - Index names
- `module_owner` - Module name

**Intended Count:** ~300+ rows (one row per column across all 34 tables)

**Current Status:** File exists but only contains header row (not generated/committed)

---

### 3. Diff View CSV
**File:** `NSW_INVENTORY_DIFF_VIEW_v1.0.csv`

**Content:** Comparison metadata between full and key-only inventories

**Columns:**
- `table_name` - Table name
- `in_full` - Y/N present in full inventory
- `in_key_only` - Y/N present in key-only inventory
- `status` - MATCH / IN_FULL_ONLY / IN_KEY_ONLY_ONLY
- `full_module` - Module from full inventory
- `key_module` - Module from key-only inventory
- `module_match` - Y/N modules match

**Count:** 30 rows (one per table) + 1 header row = 31 lines total

---

## What They Do NOT Contain

❌ **No actual data records:**
- No INSERT statements
- No customer records
- No product records
- No quotation data
- No price data
- No user accounts
- No business data

✅ **Only schema structure:**
- Table definitions
- Column definitions
- Constraint definitions
- Relationship definitions
- Index definitions

---

## Where Actual Data Lives

### 1. Seed Script (Design Validation)
**File:** `SEED_DESIGN_VALIDATION.sql`

**Content:** INSERT statements with sample data for testing/validation

**Example:**
```sql
INSERT INTO tenants (code, name, status) VALUES
('DEMO001', 'Demo Tenant', 'ACTIVE');

INSERT INTO categories (tenant_id, code, name, description, is_active) VALUES
(1, 'ELEC_PANEL', 'Electrical Panel', 'Electrical panel components', true);
```

**Purpose:** Demonstrate schema structure with sample data, validate relationships

---

### 2. Database Tables (Runtime)
**Location:** PostgreSQL database after deployment

**Content:** Actual business data inserted by applications/users

**Purpose:** Production/development data storage

---

## Summary Comparison

| File Type | Contains | Purpose | Example |
|-----------|----------|---------|---------|
| **Inventory CSVs** | ✅ Schema metadata only | Documentation, reference, validation | Table names, columns, constraints |
| **Seed SQL** | ✅ Sample INSERT data | Design validation, testing | INSERT INTO tenants... |
| **Database Tables** | ✅ Actual business data | Production/development storage | Real customer records, quotations |

---

## Why This Matters

1. **Inventory CSVs = Structure Documentation**
   - Describe HOW tables are structured
   - Used for schema design reference
   - Used for DDL generation validation
   - Used for documentation purposes

2. **Seed SQL = Sample Data**
   - Provides example INSERT statements
   - Used to test schema structure
   - Used to validate relationships
   - Not production data

3. **Database Tables = Real Data**
   - Contains actual business records
   - Inserted by applications/users
   - Changes over time
   - Production/development data

---

## Conclusion

✅ **Inventory CSV files contain ONLY schema metadata (structure information)**

❌ **Inventory CSV files do NOT contain actual data records (item data, business data)**

The CSV files are **metadata inventories** that document the schema structure, not data repositories.

---

**Last Updated:** 2026-01-06

