# Migration Strategy & Cutover Plan

**Purpose:** Define migration approach, ordering, and validation gates  
**Status:** ⏳ Pending  
**Date Created:** 2025-12-18

---

## 🎯 Objective

Create **Deliverable D: Migration Strategy + Cutover Plan** that defines:
- Migration modes (lift & shift / transform & load / hybrid)
- Order of migration (masters → relationships → BOM → quotations)
- Rollback strategy
- Validation gates (row counts, referential integrity, business totals)

---

## 🔄 Migration Modes

### Mode 1: Lift & Shift (Rarely Safe)

**Description:** Direct copy of data with minimal transformation.

**When to Use:**
- Identical schema (legacy = NSW)
- No business logic changes
- No data quality issues

**Risks:**
- ⚠️ Rarely applicable (schema usually differs)
- ⚠️ May copy bad data
- ⚠️ No data quality improvement

**Example:**
```sql
-- Direct INSERT (only if schemas match exactly)
INSERT INTO nsw.products 
SELECT * FROM legacy.products;
```

---

### Mode 2: Transform & Load (Most Realistic) ⭐ RECOMMENDED

**Description:** Extract, transform, validate, then load into NSW.

**When to Use:**
- Schema differences exist
- Data transformation needed
- Data quality improvements required

**Process:**
1. Extract from legacy
2. Transform (rename, convert, normalize, map)
3. Validate (data quality checks)
4. Load into NSW

**Example:**
```sql
-- Transform and load
INSERT INTO nsw.products (ProductId, Name, CategoryId, ProductType)
SELECT 
    ProductId,
    ProductName,  -- renamed
    (SELECT CategoryId FROM nsw.categories WHERE Name = legacy.products.Category),  -- normalized
    CASE Status WHEN 'A' THEN 1 ELSE 0 END  -- mapped
FROM legacy.products;
```

---

### Mode 3: Hybrid (Master First, Transactional Later)

**Description:** Migrate master data first, then transactional data.

**When to Use:**
- Large master data sets
- Complex dependencies
- Need to validate masters before transactions

**Process:**
1. Migrate masters (categories, products, makes, series)
2. Validate masters
3. Migrate relationships (BOMs, quotations)
4. Validate relationships

---

## 📊 Migration Ordering (Safe Default)

### Phase 1: Lookup + Enums (Foundation)

**Tables:**
- `makes` (manufacturer brands)
- `series` (product series)
- `categories` (product categories)
- `sub_categories` (subcategories)
- `items` (product types)
- `attributes` (attribute definitions)

**Rationale:** These are referenced by other tables. Must be migrated first.

**Validation:**
- [ ] Row counts match
- [ ] No duplicates
- [ ] All required records present

---

### Phase 2: Category/Subcategory/Type/Attributes (Master Data)

**Tables:**
- `category_attributes` (category-attribute assignments)
- `product_attributes` (product attribute values)

**Rationale:** Depends on Phase 1, referenced by products.

**Validation:**
- [ ] All FKs valid (no orphans)
- [ ] Attribute assignments complete

---

### Phase 3: L0/L1/L2 Items (Product Catalog)

**Tables:**
- `products` (L0/L1/L2 products)

**Rationale:** Core product catalog, depends on Phase 1 & 2.

**Critical Checks:**
- [ ] L1 products (Generic) identified correctly
- [ ] L2 products (Specific) have Make/Series
- [ ] ProductType consistency (1=Generic, 2=Specific)
- [ ] GenericId links valid (L2 → L1)

**Validation:**
- [ ] Row counts match (or expected difference documented)
- [ ] No orphan FKs (CategoryId, MakeId, SeriesId)
- [ ] ProductType distribution matches expectations

---

### Phase 4: Make/Series Catalogs (If Separate)

**Tables:**
- (if makes/series have additional data beyond Phase 1)

**Rationale:** Complete manufacturer catalog.

---

### Phase 5: Master BOM (L1 Only)

**Tables:**
- `master_boms` (BOM templates)
- `master_bom_items` (BOM components)

**Critical Checks:**
- [ ] Only L1 (Generic) products in master_bom_items
- [ ] No L2 (Specific) products in master BOMs
- [ ] BOM structure integrity

**Validation:**
- [ ] All ProductId in master_bom_items are L1
- [ ] BOM item counts match
- [ ] No orphan BOM items

---

### Phase 6: Proposal BOM Instances (L2 Only)

**Tables:**
- `proposal_boms` (BOM instances)
- `proposal_bom_items` (BOM components)

**Critical Checks:**
- [ ] Only L2 (Specific) products in proposal_bom_items
- [ ] No L1 (Generic) products in proposal BOMs
- [ ] MasterBomId links valid

**Validation:**
- [ ] All ProductId in proposal_bom_items are L2
- [ ] MasterBomId FKs valid
- [ ] BOM item counts match

---

### Phase 7: Feeder/Panel Tree (V2 Structure)

**Tables:**
- `quotation_sales` (panels)
- `quotation_sale_boms` (feeders/BOMs)
- `quotation_sale_bom_items` (components)

**Critical Checks:**
- [ ] Panel → Feeder → BOM hierarchy correct
- [ ] Level field correct (0=Panel, 1=Feeder, 2=BOM)
- [ ] ParentBomId links valid

**Validation:**
- [ ] Hierarchy integrity (no circular references)
- [ ] Level distribution matches expectations
- [ ] All FKs valid

---

### Phase 8: Quotations + Commercial Totals

**Tables:**
- `quotations` (quotation headers)
- `quotation_discount_rules` (discount rules)
- (quotation items already in Phase 7)

**Critical Checks:**
- [ ] Quotation totals match legacy
- [ ] Discount calculations correct
- [ ] Pricing aggregates match

**Validation:**
- [ ] Row counts match
- [ ] Quotation totals reconciled
- [ ] Business totals match (sum of items = quotation total)

---

### Phase 9: History + Audit (Optional but Recommended)

**Tables:**
- `bom_history` (if exists)
- `copy_history` (if exists)
- `logs` (if exists)

**Rationale:** Preserve audit trail and history.

**Validation:**
- [ ] History records linked correctly
- [ ] No orphan history records

---

## ✅ Validation Gates

### Gate 1: Row Count Reconciliation

**For each migrated table:**
```sql
-- Expected vs Actual
SELECT 
    'products' as table_name,
    (SELECT COUNT(*) FROM legacy.products) as legacy_count,
    (SELECT COUNT(*) FROM nsw.products) as nsw_count,
    (SELECT COUNT(*) FROM legacy.products) - (SELECT COUNT(*) FROM nsw.products) as difference;
```

**Acceptance Criteria:**
- Difference = 0 (or documented expected difference)
- No unexplained row loss

---

### Gate 2: Orphan FK Checks

**For each FK relationship:**
```sql
-- Find orphan records
SELECT COUNT(*) as orphan_count
FROM nsw.products p
LEFT JOIN nsw.categories c ON p.CategoryId = c.CategoryId
WHERE c.CategoryId IS NULL;
```

**Acceptance Criteria:**
- Orphan count = 0
- All FKs valid

---

### Gate 3: Duplicate Key Checks

**For each unique constraint:**
```sql
-- Find duplicates
SELECT ProductNo, COUNT(*) as count
FROM nsw.products
GROUP BY ProductNo
HAVING count > 1;
```

**Acceptance Criteria:**
- No duplicates (or documented expected duplicates)

---

### Gate 4: Business Totals

**Quotation Totals:**
```sql
-- Compare legacy vs NSW quotation totals
SELECT 
    q.QuotationId,
    q.Total as legacy_total,
    SUM(qsbi.Amount) as nsw_calculated_total,
    ABS(q.Total - SUM(qsbi.Amount)) as difference
FROM nsw.quotations q
JOIN nsw.quotation_sales qs ON q.QuotationId = qs.QuotationId
JOIN nsw.quotation_sale_boms qsb ON qs.QuotationSaleId = qsb.QuotationSaleId
JOIN nsw.quotation_sale_bom_items qsbi ON qsb.QuotationSaleBomId = qsbi.QuotationSaleBomId
GROUP BY q.QuotationId;
```

**Acceptance Criteria:**
- Difference < 0.01 (rounding tolerance)
- Business totals match

---

### Gate 5: Data Quality Checks

**For each critical field:**
- [ ] No NULLs in required fields
- [ ] No invalid enum values
- [ ] No negative quantities/amounts
- [ ] Dates in valid range

---

## 🔄 Rollback Strategy

### Rollback Triggers

**Trigger rollback if:**
- Row count difference > 5% (unexplained)
- Orphan FKs > 0
- Business totals mismatch > 1%
- Data quality issues > threshold

### Rollback Process

1. **Stop migration immediately**
2. **Document issue** (what failed, why)
3. **Restore from backup** (if data written)
4. **Fix issue** (mapping, transform, data quality)
5. **Re-run migration** (after fix validated)

### Backup Strategy

**Before migration:**
- [ ] Full database backup
- [ ] Backup timestamp recorded
- [ ] Restore procedure tested

**During migration:**
- [ ] Transaction-based (can rollback)
- [ ] Checkpoint after each phase
- [ ] Validation after each phase

---

## 📋 Migration Execution Checklist

### Pre-Migration
- [ ] Complete Deliverable A (Legacy Schema)
- [ ] Complete Deliverable B (NSW Schema)
- [ ] Complete Deliverable C (Mapping Matrix)
- [ ] Review and approve migration strategy
- [ ] Create database backup
- [ ] Test restore procedure
- [ ] Prepare migration scripts (draft)

### Phase Execution
- [ ] Phase 1: Lookup + Enums
- [ ] Phase 2: Category/Subcategory/Type/Attributes
- [ ] Phase 3: L0/L1/L2 Items
- [ ] Phase 4: Make/Series Catalogs
- [ ] Phase 5: Master BOM
- [ ] Phase 6: Proposal BOM
- [ ] Phase 7: Feeder/Panel Tree
- [ ] Phase 8: Quotations + Commercial
- [ ] Phase 9: History + Audit

### Post-Migration
- [ ] Run all validation gates
- [ ] Document any issues
- [ ] Sign-off on migration completion
- [ ] Update migration status

---

## 🚀 Next Steps

1. Complete Deliverables A, B, C first
2. Review this strategy
3. Create detailed migration scripts (draft)
4. Test migration on sample data
5. Execute full migration (after approval)

---

**Last Updated:** 2025-12-18  
**Status:** Ready to Execute (after Deliverables A, B, C complete)  
**Estimated Time:** 4-6 hours (strategy) + execution time TBD

