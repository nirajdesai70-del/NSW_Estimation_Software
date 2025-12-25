# Legacy Schema Extraction Plan

**Purpose:** Extract complete database schema from legacy system (`/Users/nirajdesai/Projects/nish/`)  
**Status:** ⏳ Pending  
**Date Created:** 2025-12-18

---

## 🎯 Objective

Extract and document the legacy database schema to create **Deliverable A: Legacy DB Truth Pack**.

---

## 📍 Source Location

**Primary Source:** `/Users/nirajdesai/Projects/nish/`

**Expected Sources:**
1. **SQL Dump Files:**
   - `NEPLQUOTEDB.sql` (if exists)
   - `1764929861_ready.sql` (if exists)
   - Any other `.sql` backup files

2. **Database Connection:**
   - Database name: `nish` or `nepl_quotation` (check which exists)
   - May need to connect to legacy database if still running

3. **Codebase Analysis:**
   - Migration files in `database/migrations/` (if Laravel)
   - Model files in `app/Models/` (if Laravel)
   - Any schema documentation

---

## 📋 Extraction Steps

### Step 1: Identify Source Files

```bash
# Check for SQL dump files
find /Users/nirajdesai/Projects/nish -name "*.sql" -type f

# Check for database folder
ls -la /Users/nirajdesai/Projects/nish/database/

# Check for migrations
ls -la /Users/nirajdesai/Projects/nish/database/migrations/ 2>/dev/null
```

**Action Items:**
- [ ] List all SQL dump files found
- [ ] Identify which SQL file is the most recent/complete
- [ ] Check if legacy database is still accessible
- [ ] Document source file locations

---

### Step 2: Extract Table List

**Method A: From SQL Dump**
```bash
# Extract CREATE TABLE statements
grep -i "CREATE TABLE" /Users/nirajdesai/Projects/nish/NEPLQUOTEDB.sql | sed 's/CREATE TABLE //' | sed 's/ (.*//' | sort

# Count tables
grep -i "CREATE TABLE" /Users/nirajdesai/Projects/nish/NEPLQUOTEDB.sql | wc -l
```

**Method B: From Database (if accessible)**
```sql
-- List all tables
SHOW TABLES;

-- Get table count
SELECT COUNT(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'nish';
```

**Output:** List of all table names

---

### Step 3: Extract Table Structures

**For each table, extract:**
- Column names
- Data types
- Nullability (NULL/NOT NULL)
- Default values
- Primary keys
- Foreign keys
- Unique constraints
- Indexes

**Method A: From SQL Dump**
```bash
# Extract full CREATE TABLE for a specific table
grep -A 50 "CREATE TABLE.*table_name" /Users/nirajdesai/Projects/nish/NEPLQUOTEDB.sql
```

**Method B: From Database (if accessible)**
```sql
-- Get table structure
SHOW CREATE TABLE table_name;

-- Get column details
DESCRIBE table_name;

-- Get foreign keys
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'nish'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Get indexes
SHOW INDEX FROM table_name;
```

**Output:** Complete table structure for each table

---

### Step 4: Extract Row Counts

**Method A: From SQL Dump**
```bash
# Extract INSERT statements and count
grep -c "INSERT INTO.*table_name" /Users/nirajdesai/Projects/nish/NEPLQUOTEDB.sql
```

**Method B: From Database (if accessible)**
```sql
-- Get row count for each table
SELECT 
    table_name,
    table_rows
FROM information_schema.tables
WHERE table_schema = 'nish'
ORDER BY table_rows DESC;
```

**Output:** Row count per table

---

### Step 5: Extract Sample Data

**For each table, extract:**
- 5-10 sample rows (anonymized if contains PII)
- Representative data showing data patterns

**Method: From Database (if accessible)**
```sql
-- Get sample rows
SELECT * FROM table_name LIMIT 10;
```

**Output:** Sample data CSV/JSON per table

---

### Step 6: Classify Tables by Domain

**Classification:**
1. **Masters:** category, subcategory, item, product, make, series, attributes
2. **BOM Structures:** master_bom, master_bom_items, proposal_bom, proposal_bom_items
3. **Commercial:** quotation, quotation_sales, quotation_sale_boms, quotation_sale_bom_items
4. **Security/Org:** users, roles, permissions
5. **Audit/History:** bom_history, copy_history, logs
6. **Lookup/Reference:** price_lists, discount_rules, etc.

**Output:** Table classification list

---

## 📊 Output Format

### Excel Export: `LEGACY_SCHEMA_INVENTORY.xlsx`

**Sheets:**
1. **Table List:** All tables with row counts
2. **Table Structures:** Full column definitions per table
3. **Foreign Keys:** All FK relationships
4. **Indexes:** All indexes per table
5. **Sample Data:** Sample rows per table

### JSON Export: `LEGACY_SCHEMA.json`

```json
{
  "database": "nish",
  "extraction_date": "2025-12-18",
  "tables": [
    {
      "name": "products",
      "row_count": 1234,
      "columns": [
        {
          "name": "ProductId",
          "type": "INT",
          "nullable": false,
          "default": null,
          "primary_key": true
        }
      ],
      "foreign_keys": [],
      "indexes": []
    }
  ]
}
```

### Markdown Report: `LEGACY_SCHEMA_REPORT.md`

**Sections:**
1. Executive Summary
2. Table Inventory
3. Schema Details (per table)
4. Relationships Diagram
5. Data Quality Notes
6. Known Issues

---

## 🔍 Data Quality Checks

**During extraction, flag:**
- [ ] Tables with 0 rows (empty tables)
- [ ] Tables with very large row counts (performance risk)
- [ ] Missing foreign keys (orphan risk)
- [ ] Inconsistent naming conventions
- [ ] Missing indexes on FK columns
- [ ] Tables with no clear purpose

---

## ⚠️ Known Challenges

### Challenge 1: Multiple SQL Files
- **Issue:** May have multiple SQL dumps (old vs new)
- **Solution:** Use most recent, document which file used

### Challenge 2: Database Not Accessible
- **Issue:** Legacy database may not be running
- **Solution:** Extract from SQL dump only

### Challenge 3: Incomplete SQL Dump
- **Issue:** SQL dump may be missing some tables
- **Solution:** Document missing tables, flag as incomplete

### Challenge 4: V2 vs Legacy Confusion
- **Issue:** `/Users/nirajdesai/Projects/nish/` may have both legacy and v2 code
- **Solution:** Identify which is which, extract legacy schema only

---

## 📝 Extraction Checklist

- [ ] Identify source files (SQL dumps, database)
- [ ] Extract table list
- [ ] Extract table structures (columns, types, constraints)
- [ ] Extract foreign keys
- [ ] Extract indexes
- [ ] Extract row counts
- [ ] Extract sample data (anonymized)
- [ ] Classify tables by domain
- [ ] Generate Excel export
- [ ] Generate JSON export
- [ ] Generate Markdown report
- [ ] Review and validate completeness

---

## 🚀 Next Steps After Extraction

1. Review `LEGACY_SCHEMA_REPORT.md` for completeness
2. Compare with NSW schema (Deliverable B)
3. Identify gaps and mismatches
4. Begin mapping matrix (Deliverable C)

---

**Last Updated:** 2025-12-18  
**Status:** Ready to Execute  
**Estimated Time:** 4-6 hours

