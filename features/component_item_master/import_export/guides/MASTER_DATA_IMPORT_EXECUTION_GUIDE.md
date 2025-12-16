> Source: source_snapshot/MASTER_DATA_IMPORT_EXECUTION_GUIDE.md
> Bifurcated into: features/component_item_master/import_export/MASTER_DATA_IMPORT_EXECUTION_GUIDE.md
> Module: Component / Item Master > Import/Export
> Date: 2025-12-17 (IST)

# Master Data Import - Step-by-Step Execution Guide

## ⚠️ IMPORTANT: Read This First

**This import is DESTRUCTIVE:**
- Each table will be **TRUNCATED** (all current data deleted)
- Then replaced with data from legacy backup
- **Any manual edits/new rows in current DB will be lost**
- **No duplicates possible** (because we wipe first)

**Before starting:**
1. ✅ **MANDATORY: Take a full backup of your current database** (see Section 1.4)
2. ✅ Review which tables you're okay resetting
3. ✅ Always use `--dry-run` first to see counts

---

## 1. One-Time Setup

### 1.1 Create Legacy Database

```bash
mysql -u root -p -e "CREATE DATABASE nepl_legacy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 1.2 Import Legacy Backup

```bash
# From project root directory
mysql -u root -p nepl_legacy < 1764929861_ready.sql
```

### 1.3 Configure .env

Add these lines to your `.env` file:

```env
LEGACY_DB_HOST=127.0.0.1
LEGACY_DB_PORT=3306
LEGACY_DB_DATABASE=nepl_legacy
LEGACY_DB_USERNAME=root
LEGACY_DB_PASSWORD=your_mysql_password_here
```

Then clear config cache:

```bash
php artisan config:clear
php artisan config:cache
```

### 1.4 Backup Current Database

**CRITICAL - Do this before any import!**

#### Option 1: Use the Backup Script (Recommended)

```bash
# From project root
./backup_before_import.sh
```

This script will:
- Read database credentials from `.env`
- Create a timestamped backup in `database/backups/`
- Show you the backup file location and restore command

#### Option 2: Manual Backup Command

```bash
# Get your database name from .env first
# Then run:
mysqldump -u root -p your_current_db_name > backup_before_master_import_$(date +%Y%m%d_%H%M%S).sql
```

Replace `your_current_db_name` with your actual database name from `.env` (DB_DATABASE).

**Example:**
```bash
# If DB_DATABASE=nish in your .env:
mysqldump -u root -p nish > backup_before_master_import_$(date +%Y%m%d_%H%M%S).sql
```

#### Option 3: Backup Specific Tables Only (If You Want to Be Selective)

If you only want to backup the master tables that will be affected:

```bash
mysqldump -u root -p your_db_name \
  clients projects categories sub_categories items products master_boms master_bom_items \
  > backup_master_tables_only_$(date +%Y%m%d_%H%M%S).sql
```

**⚠️ Important:** Even if you backup only master tables, the import will still affect those tables. Make sure you're comfortable with losing current data in those tables.

#### Verify Backup Was Created

```bash
# Check backup file exists and has content
ls -lh database/backups/backup_before_master_import_*.sql

# Or if using manual backup:
ls -lh backup_before_master_import_*.sql
```

The backup file should be several MB in size (depending on your data volume).

---

## 2. Pre-Import Verification

### 2.1 Test Legacy Connection

```bash
php artisan master-data:import --dry-run
```

**Expected output:**
- ✓ Legacy database connection successful
- Current Database Counts: (shows current DB counts)
- Legacy Database Counts: (shows legacy DB counts)
- Dry-run mode: No data imported.

**If connection fails:**
- Check `.env` LEGACY_DB_* variables
- Verify `nepl_legacy` database exists
- Verify backup file was imported successfully

---

## 3. Step-by-Step Import Process

**Import Order (respects FK dependencies):**
1. clients
2. projects
3. categories
4. subcategories
5. items
6. products
7. master_boms
8. master_bom_items

### Step 1: Import Clients

```bash
# 1. Dry-run to see counts
php artisan master-data:import --table=clients --dry-run

# 2. Review the counts - are you okay resetting clients?
# If YES, proceed:

# 3. Real import (with confirmation)
php artisan master-data:import --table=clients

# OR skip confirmation with --force:
php artisan master-data:import --table=clients --force

# 4. Validate
php artisan master-data:validate
```

**What happens:**
- All current clients → DELETED
- All legacy clients → INSERTED
- No duplicates possible

**After import, verify:**
```sql
SELECT COUNT(*) FROM clients;
SELECT COUNT(DISTINCT ClientId) FROM clients;
-- These two numbers should match
```

---

### Step 2: Import Projects

```bash
php artisan master-data:import --table=projects --dry-run
php artisan master-data:import --table=projects --force
php artisan master-data:validate
```

**Note:** Projects table doesn't have ClientId FK in current schema (uses ClientName as string), so FK validation may not catch project→client mismatches.

---

### Step 3: Import Categories

```bash
php artisan master-data:import --table=categories --dry-run
php artisan master-data:import --table=categories --force
php artisan master-data:validate
```

**This is the foundation** - subcategories and items depend on categories.

---

### Step 4: Import Subcategories

```bash
php artisan master-data:import --table=subcategories --dry-run
php artisan master-data:import --table=subcategories --force
php artisan master-data:validate
```

**Validation will check:** All SubCategoryId → CategoryId references are valid.

---

### Step 5: Import Items

```bash
php artisan master-data:import --table=items --dry-run
php artisan master-data:import --table=items --force
php artisan master-data:validate
```

**Validation will check:** All ItemId → CategoryId references are valid.

---

### Step 6: Import Products

```bash
php artisan master-data:import --table=products --dry-run
php artisan master-data:import --table=products --force
php artisan master-data:validate
```

**This is the largest table** - may take longer.

**Validation will check:**
- Products → Categories
- Products → SubCategories
- Products → Items

---

### Step 7: Import Master BOMs

```bash
php artisan master-data:import --table=master_boms --dry-run
php artisan master-data:import --table=master_boms --force
php artisan master-data:validate
```

---

### Step 8: Import Master BOM Items

```bash
php artisan master-data:import --table=master_bom_items --dry-run
php artisan master-data:import --table=master_bom_items --force
php artisan master-data:validate
```

**Validation will check:** All MasterBomItemId → ProductId references are valid.

---

## 4. Import All Tables at Once (Alternative)

If you're confident and want to import everything:

```bash
# 1. Dry-run all
php artisan master-data:import --dry-run

# 2. Review counts - are you okay resetting ALL master tables?

# 3. Import all (with confirmations)
php artisan master-data:import

# OR skip all confirmations:
php artisan master-data:import --force

# 4. Validate everything
php artisan master-data:validate
```

---

## 5. Post-Import Verification

### 5.1 Check for Duplicates

Run these queries for each table (should return 0 rows):

```sql
-- Products
SELECT ProductId, COUNT(*) 
FROM products
GROUP BY ProductId
HAVING COUNT(*) > 1;

-- Categories
SELECT CategoryId, COUNT(*) 
FROM categories
GROUP BY CategoryId
HAVING COUNT(*) > 1;

-- Clients
SELECT ClientId, COUNT(*) 
FROM clients
GROUP BY ClientId
HAVING COUNT(*) > 1;

-- Projects
SELECT ProjectId, COUNT(*) 
FROM projects
GROUP BY ProjectId
HAVING COUNT(*) > 1;
```

### 5.2 Verify Counts Match

```sql
-- Compare total vs distinct counts (should match)
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT ProductId) as distinct_ids
FROM products;
```

### 5.3 Run Full Validation

```bash
php artisan master-data:validate
```

**Expected output:**
- ✓ All subcategories have valid CategoryId references
- ✓ All items have valid CategoryId references
- ✓ All products have valid references
- ✓ All master BOM items have valid ProductId references

**If errors found:**
- Review the example invalid rows listed
- May need to fix data in legacy DB or adjust import logic

---

## 6. Troubleshooting

### Issue: Connection Failed

**Error:** `Cannot connect to legacy database`

**Fix:**
1. Check `.env` has correct LEGACY_DB_* variables
2. Verify `nepl_legacy` database exists: `mysql -u root -p -e "SHOW DATABASES;"`
3. Verify backup was imported: `mysql -u root -p nepl_legacy -e "SHOW TABLES;"`
4. Clear config: `php artisan config:clear && php artisan config:cache`

### Issue: Foreign Key Violations

**Error:** `Integrity constraint violation`

**Fix:**
1. Check import order - must follow FK dependencies
2. Run `php artisan master-data:validate` to see which FKs are broken
3. May need to fix data in legacy DB before importing

### Issue: Table Not Found

**Error:** `Table 'nepl_legacy.xxx' doesn't exist`

**Fix:**
1. Verify backup file was imported correctly
2. Check table name matches (case-sensitive)
3. May need to adjust table name in import method

### Issue: Imported Wrong Data

**Fix:**
1. **Restore from backup immediately:**
   ```bash
   # If you used the backup script:
   mysql -u root -p your_db_name < database/backups/backup_before_master_import_YYYYMMDD_HHMMSS.sql
   
   # Or if manual backup:
   mysql -u root -p your_db_name < backup_before_master_import_YYYYMMDD_HHMMSS.sql
   ```
2. Verify restore worked: `php artisan master-data:import --dry-run` (should show original counts)
3. Review what went wrong
4. Re-run import with correct source (after fixing the issue)

---

## 7. What Gets Imported

### ✅ Master Data Tables (Safe to Import)
- `clients` - Client companies
- `projects` - Client projects
- `categories` - Product categories
- `sub_categories` - Product subcategories
- `items` - Product types/items
- `products` - Product catalog
- `master_boms` - Master BOM templates
- `master_bom_items` - Master BOM components

### ❌ NOT Imported (V2 Data Protected)
- `quotations` - Quotation headers
- `quotation_sales` - Panels
- `quotation_sale_boms` - Feeders/BOMs
- `quotation_sale_bom_items` - Components
- Any V2-specific columns or tables

---

## 8. Safety Checklist

Before running any import:

- [ ] **Full database backup created** (use `./backup_before_import.sh` or manual mysqldump)
- [ ] **Backup file verified** (exists, has content, know restore command)
- [ ] Legacy database (`nepl_legacy`) created and populated
- [ ] `.env` configured with LEGACY_DB_* variables
- [ ] `--dry-run` executed and counts reviewed
- [ ] Confirmed which tables you're okay resetting
- [ ] Ready to lose current data in those tables
- [ ] Know how to restore backup if needed (see Section 9.1)

---

## 9. Backup & Restore Commands

### 9.1 Create Backup

```bash
# Automated script (recommended)
./backup_before_import.sh

# Manual command
mysqldump -u root -p your_db_name > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 9.2 Restore Backup

```bash
# If something goes wrong, restore immediately:
mysql -u root -p your_db_name < database/backups/backup_before_master_import_YYYYMMDD_HHMMSS.sql

# Or if manual backup:
mysql -u root -p your_db_name < backup_before_master_import_YYYYMMDD_HHMMSS.sql
```

**⚠️ Warning:** Restoring will overwrite current database with backup state. Only do this if you need to undo the import.

### 9.3 Verify Backup Integrity

```bash
# Check backup file exists and has reasonable size
ls -lh database/backups/backup_*.sql

# Test restore to a temporary database (optional, advanced)
mysql -u root -p -e "CREATE DATABASE test_restore;"
mysql -u root -p test_restore < database/backups/backup_before_master_import_YYYYMMDD_HHMMSS.sql
mysql -u root -p -e "DROP DATABASE test_restore;"
```

---

## 10. Quick Reference Commands

```bash
# Test connection
php artisan master-data:import --dry-run

# Import single table
php artisan master-data:import --table=categories --force

# Import all tables
php artisan master-data:import --force

# Validate integrity
php artisan master-data:validate

# Clear config cache
php artisan config:clear && php artisan config:cache
```

---

## 11. Next Steps After Import

Once master data is imported:

1. ✅ Verify V2 quotation pages still work
2. ✅ Check that Master BOM reuse can find imported BOMs
3. ✅ Verify product selection in Add Component modal works
4. ✅ Test that legacy quotation pages can open old offers
5. ⏸️ **Then** we can plan legacy quotation → V2 migration (separate task)

---

**End of Execution Guide**
