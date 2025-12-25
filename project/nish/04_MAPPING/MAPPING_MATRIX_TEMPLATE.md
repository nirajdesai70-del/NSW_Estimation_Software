# Legacy to NSW Mapping Matrix Template

**Purpose:** Map every legacy column to NSW target, with transform rules and risk flags  
**Status:** ⏳ Pending  
**Date Created:** 2025-12-18

---

## 🎯 Objective

Create **Deliverable C: Mapping Matrix (Legacy → NSW)** that maps every legacy column to its NSW target with:
- Target table.column
- Transform rules
- Key mapping rules
- Data quality checks
- Migration priority
- Risk flags

---

## 📊 Mapping Matrix Structure

### Excel Format: `LEGACY_TO_NSW_MAPPING.xlsx`

**Sheet 1: Column Mapping**
| Legacy Table | Legacy Column | Legacy Type | NSW Table | NSW Column | NSW Type | Transform Rule | Priority | Risk | Status |
|--------------|---------------|-------------|-----------|------------|----------|----------------|----------|------|--------|
| products | ProductId | INT | products | ProductId | INT | PRESERVE | P0 | LOW | ⏳ Pending |
| products | Name | VARCHAR | products | Name | VARCHAR | PRESERVE | P0 | LOW | ⏳ Pending |
| products | CategoryId | INT | products | CategoryId | INT | PRESERVE | P0 | MEDIUM | ⏳ Pending |

**Sheet 2: Table Mapping**
| Legacy Table | NSW Table | Mapping Type | Notes | Status |
|--------------|-----------|--------------|-------|--------|
| products | products | DIRECT | Same table name, check column differences | ⏳ Pending |
| old_boms | master_boms | SPLIT | Legacy BOM split into Master and Proposal | ⏳ Pending |

**Sheet 3: Key Mapping**
| Legacy Table | Legacy PK | NSW Table | NSW PK | Mapping Rule | Preserve Old ID? | Status |
|--------------|-----------|-----------|--------|--------------|------------------|--------|
| products | ProductId | products | ProductId | DIRECT | YES | ⏳ Pending |

**Sheet 4: Risk Register**
| Risk ID | Legacy Table.Column | Issue | Impact | Mitigation | Status |
|---------|---------------------|-------|--------|------------|--------|
| RISK-001 | products.ProductType | Enum values differ | HIGH | Create mapping table | ⏳ Pending |

---

## 🔄 Transform Rules

### Rule Types

1. **PRESERVE:** Direct copy, no transformation
   - Example: `products.Name` → `products.Name`

2. **RENAME:** Same data, different column name
   - Example: `old_products.ProductName` → `products.Name`

3. **CONVERT:** Data type conversion
   - Example: `old_products.Price` (VARCHAR) → `products.Rate` (DECIMAL)

4. **NORMALIZE:** Data cleanup/normalization
   - Example: `old_products.Category` (free text) → `products.CategoryId` (FK lookup)

5. **DERIVE:** Calculate from other columns
   - Example: `products.Amount` = `products.Quantity * products.Rate`

6. **SPLIT:** One legacy column → multiple NSW columns
   - Example: `old_boms.BomType` → `master_boms.TemplateType` OR `proposal_boms.InstanceType`

7. **JOIN:** Multiple legacy columns → one NSW column
   - Example: `old_products.Make` + `old_products.Series` → `products.MakeId` + `products.SeriesId`

8. **MAP:** Enum/value mapping
   - Example: `old_products.Status` ('A'/'I') → `products.Status` (1/0)

9. **DEFAULT:** No source, use default value
   - Example: `products.created_at` (not in legacy) → `NOW()`

10. **SKIP:** Legacy column not needed in NSW
    - Example: `old_products.LegacyField` → (not migrated)

---

## 🎯 Migration Priority

### P0 (Critical - Must Migrate)
- Master data tables (categories, products, makes, series)
- Core business tables (quotations, projects)
- **Blockers:** Cannot proceed without these

### P1 (High - Should Migrate)
- BOM structures (master_boms, proposal_boms)
- Commercial data (quotation items, pricing)
- **Impact:** Business functionality depends on these

### P2 (Medium - Nice to Have)
- Audit/history tables
- Lookup/reference data
- **Impact:** Limited business impact if missing

### P3 (Low - Optional)
- Logs, temporary data
- **Impact:** Can be regenerated or skipped

---

## ⚠️ Risk Levels

### LOW
- Direct mapping, no transformation
- Same data types
- No business logic changes

### MEDIUM
- Minor transformation (rename, convert type)
- Some data cleanup needed
- Enum mapping required

### HIGH
- Complex transformation (split, join, derive)
- Data quality issues expected
- Business logic changes

### CRITICAL (Migration Blocker)
- Semantic mismatch (same name, different meaning)
- Cannot map without business decision
- Data loss risk

---

## 📋 Mapping Process

### Step 1: Table-Level Mapping

**For each legacy table:**
1. Identify corresponding NSW table(s)
2. Determine mapping type (DIRECT, SPLIT, JOIN, SKIP)
3. Document in Table Mapping sheet

**Mapping Types:**
- **DIRECT:** One-to-one table mapping
- **SPLIT:** One legacy table → multiple NSW tables
- **JOIN:** Multiple legacy tables → one NSW table
- **SKIP:** Legacy table not needed in NSW

---

### Step 2: Column-Level Mapping

**For each legacy column:**
1. Identify target NSW table.column
2. Determine transform rule
3. Document data quality checks needed
4. Assign priority and risk level
5. Document in Column Mapping sheet

---

### Step 3: Key Mapping

**For each primary key:**
1. Determine if old ID should be preserved
2. Document mapping rule (DIRECT, REMAP, COMPOSITE)
3. Document in Key Mapping sheet

**Key Mapping Rules:**
- **PRESERVE:** Keep old ID (e.g., `ProductId` stays same)
- **REMAP:** Generate new ID, maintain mapping table
- **COMPOSITE:** Combine multiple legacy keys into one

---

### Step 4: Risk Identification

**For each mapping, identify:**
1. Data quality risks (nulls, orphans, invalid codes)
2. Semantic drift risks (same name, different meaning)
3. Transformation complexity risks
4. Document in Risk Register

---

## 🔍 Data Quality Checks

### Pre-Migration Checks

**For each legacy table:**
- [ ] Row count validation
- [ ] NULL value analysis
- [ ] Orphan FK check
- [ ] Duplicate key check
- [ ] Invalid enum value check
- [ ] Data type validation

### Post-Migration Validation

**For each migrated table:**
- [ ] Row count matches (or expected difference documented)
- [ ] No orphan FKs
- [ ] No duplicate keys
- [ ] Business totals match (e.g., quotation totals)

---

## 📝 Mapping Checklist

- [ ] Complete table-level mapping
- [ ] Complete column-level mapping
- [ ] Complete key mapping
- [ ] Identify all transform rules
- [ ] Assign priorities (P0/P1/P2/P3)
- [ ] Assign risk levels (LOW/MEDIUM/HIGH/CRITICAL)
- [ ] Document data quality checks
- [ ] Create risk register
- [ ] Generate Excel mapping matrix
- [ ] Review and validate completeness

---

## 🚀 Next Steps After Mapping

1. Review mapping matrix for completeness
2. Identify migration blockers (CRITICAL risks)
3. Create migration scripts (draft, not executed)
4. Begin migration strategy (Deliverable D)

---

**Last Updated:** 2025-12-18  
**Status:** Ready to Execute (after Deliverables A & B complete)  
**Estimated Time:** 8-12 hours

