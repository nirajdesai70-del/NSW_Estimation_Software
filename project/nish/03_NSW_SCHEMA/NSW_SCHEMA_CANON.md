# NSW Target Canonical Data Dictionary

**Purpose:** Document the final NSW database schema from migrations/models  
**Status:** ⏳ Pending Extraction  
**Date Created:** 2025-12-18

---

## 🎯 Objective

Extract and document the NSW target database schema to create **Deliverable B: NSW Target Canonical Data Dictionary**.

This document defines:
- Final table list (from migrations)
- Column definitions (meaning, not just name)
- PK/FK relationships
- Enumerations/lookup references
- Owner module (CIM / MBOM / PBOM / FEED / PANEL / QUO)

---

## 📍 Source Location

**Primary Sources:**
1. **Migrations:** `source_snapshot/database/migrations/` (if exists)
2. **Models:** `source_snapshot/app/Models/` (if exists)
3. **Documentation:** Existing schema docs in `features/` folders

**Note:** This is a shadow repo. Actual codebase may be in `/Users/nirajdesai/Projects/nish/`. Extract from available sources.

---

## 📋 Extraction Steps

### Step 1: Identify Migration Files

```bash
# Check for migrations
find . -path "*/database/migrations/*.php" -type f

# List all migration files
ls -la source_snapshot/database/migrations/ 2>/dev/null
```

**Action Items:**
- [ ] List all migration files
- [ ] Identify which migrations are most recent
- [ ] Check for rollback migrations
- [ ] Document migration order

---

### Step 2: Extract Table Definitions from Migrations

**For each migration file, extract:**
- Table name (from `Schema::create()` or `Schema::table()`)
- Column definitions
- Indexes
- Foreign keys
- Constraints

**Example Pattern:**
```php
Schema::create('products', function (Blueprint $table) {
    $table->id('ProductId');
    $table->string('Name');
    // ... extract all columns
});
```

**Output:** Complete table structure from migrations

---

### Step 3: Extract Model Definitions

**For each model file, extract:**
- Table name (from `$table` property)
- Fillable fields (from `$fillable` array)
- Relationships (from relationship methods)
- Scopes and accessors

**Example Pattern:**
```php
class Product extends Model
{
    protected $table = 'products';
    protected $fillable = ['Name', 'CategoryId', ...];
    // ... extract relationships
}
```

**Output:** Model-to-table mapping and relationships

---

### Step 4: Classify Tables by Module

**Module Classification:**
- **CIM (Component Item Master):** categories, sub_categories, items, products, makes, series, attributes
- **MBOM (Master BOM):** master_boms, master_bom_items
- **PBOM (Proposal BOM):** proposal_boms, proposal_bom_items
- **FEED (Feeder Library):** (may use master_boms with TemplateType)
- **PANEL (Panel Management):** quotation_sales (panels)
- **QUO (Quotation):** quotations, quotation_sales, quotation_sale_boms, quotation_sale_bom_items
- **PROJ (Project):** projects
- **SEC (Security):** users, roles, permissions
- **SHARED:** clients, price_lists, etc.

**Output:** Table-to-module mapping

---

### Step 5: Document Column Semantics

**For each column, document:**
- **Name:** Column name
- **Type:** Data type
- **Meaning:** What does this column represent? (not just name)
- **Nullable:** Can it be NULL?
- **Default:** Default value
- **Enum Values:** If enum, list all possible values
- **Business Rule:** Any business logic associated

**Example:**
```markdown
### products.ProductType
- **Type:** TINYINT
- **Meaning:** Product classification level (Generic vs Specific)
- **Nullable:** NO
- **Default:** NULL
- **Enum Values:**
  - 1 = Generic (L1, template product)
  - 2 = Specific (L2, concrete product with Make/Series)
- **Business Rule:** Type 1 products can only appear in Master BOMs. Type 2 products can only appear in Proposal/Quotation BOMs.
```

---

### Step 6: Document Relationships

**For each foreign key, document:**
- **From Table.Column:** Source
- **To Table.Column:** Target
- **Relationship Type:** One-to-One, One-to-Many, Many-to-Many
- **Cascade Rules:** ON DELETE, ON UPDATE
- **Business Meaning:** Why does this relationship exist?

**Example:**
```markdown
### products.CategoryId → categories.CategoryId
- **Type:** One-to-Many (one category has many products)
- **Cascade:** RESTRICT (cannot delete category with products)
- **Business Meaning:** Every product must belong to a category for classification
```

---

## 📊 Output Format

### Excel Export: `NSW_SCHEMA_DICTIONARY.xlsx`

**Sheets:**
1. **Table List:** All tables with module ownership
2. **Column Definitions:** Full column semantics per table
3. **Relationships:** All FK relationships with business meaning
4. **Enumerations:** All enum values and meanings
5. **Module Index:** Tables grouped by module

### Markdown Report: `NSW_SCHEMA_CANON.md` (this file)

**Sections:**
1. Executive Summary
2. Table Inventory by Module
3. Schema Details (per table)
4. Relationships Diagram
5. Enumeration Reference
6. Business Rules Index

---

## 🗄️ Table Inventory (To Be Populated)

### CIM Module (Component Item Master)

| Table | Purpose | Row Count (Est.) | Status |
|-------|---------|------------------|--------|
| categories | Product categories | TBD | ⏳ Pending |
| sub_categories | Product subcategories | TBD | ⏳ Pending |
| items | Product types | TBD | ⏳ Pending |
| products | Product catalog | TBD | ⏳ Pending |
| makes | Manufacturer brands | TBD | ⏳ Pending |
| series | Product series | TBD | ⏳ Pending |
| attributes | Attribute definitions | TBD | ⏳ Pending |
| category_attributes | Category-attribute assignments | TBD | ⏳ Pending |
| product_attributes | Product attribute values | TBD | ⏳ Pending |

### MBOM Module (Master BOM)

| Table | Purpose | Row Count (Est.) | Status |
|-------|---------|------------------|--------|
| master_boms | Master BOM templates | TBD | ⏳ Pending |
| master_bom_items | Master BOM components | TBD | ⏳ Pending |

### PBOM Module (Proposal BOM)

| Table | Purpose | Row Count (Est.) | Status |
|-------|---------|------------------|--------|
| proposal_boms | Proposal BOM instances | TBD | ⏳ Pending |
| proposal_bom_items | Proposal BOM components | TBD | ⏳ Pending |

### QUO Module (Quotation)

| Table | Purpose | Row Count (Est.) | Status |
|-------|---------|------------------|--------|
| quotations | Quotation headers | TBD | ⏳ Pending |
| quotation_sales | Panels | TBD | ⏳ Pending |
| quotation_sale_boms | Feeders/BOMs | TBD | ⏳ Pending |
| quotation_sale_bom_items | BOM components | TBD | ⏳ Pending |
| quotation_discount_rules | Discount rules | TBD | ⏳ Pending |

### PROJ Module (Project)

| Table | Purpose | Row Count (Est.) | Status |
|-------|---------|------------------|--------|
| projects | Project headers | TBD | ⏳ Pending |

### SHARED Module

| Table | Purpose | Row Count (Est.) | Status |
|-------|---------|------------------|--------|
| clients | Client companies | TBD | ⏳ Pending |
| price_lists | Product pricing | TBD | ⏳ Pending |
| users | System users | TBD | ⏳ Pending |
| roles | User roles | TBD | ⏳ Pending |

---

## 📝 Extraction Checklist

- [ ] Identify all migration files
- [ ] Extract table definitions from migrations
- [ ] Extract model definitions
- [ ] Classify tables by module
- [ ] Document column semantics (meaning, not just name)
- [ ] Document relationships with business meaning
- [ ] Document enumerations
- [ ] Generate Excel export
- [ ] Generate Markdown report
- [ ] Review and validate completeness
- [ ] Tag tables as CONFIRMED-IN-REPO or INFERRED

---

## 🔍 Data Quality Checks

**During extraction, flag:**
- [ ] Tables defined in migrations but no model exists
- [ ] Models exist but no migration (orphan models)
- [ ] Missing foreign key constraints in migrations
- [ ] Inconsistent naming conventions
- [ ] Missing indexes on FK columns
- [ ] Tables with unclear purpose

---

## ⚠️ Known Challenges

### Challenge 1: Shadow Repo Limitations
- **Issue:** This is a documentation repo, actual code may be elsewhere
- **Solution:** Extract from available sources, mark as INFERRED if needed

### Challenge 2: Migration Order
- **Issue:** Migrations may have dependencies
- **Solution:** Analyze migration timestamps and dependencies

### Challenge 3: Missing Semantics
- **Issue:** Migrations don't document "meaning" of columns
- **Solution:** Infer from model relationships and existing documentation

---

## 🚀 Next Steps After Extraction

1. Review `NSW_SCHEMA_CANON.md` for completeness
2. Compare with Legacy schema (Deliverable A)
3. Identify gaps and mismatches
4. Begin mapping matrix (Deliverable C)

---

**Last Updated:** 2025-12-18  
**Status:** Ready to Execute  
**Estimated Time:** 6-8 hours

