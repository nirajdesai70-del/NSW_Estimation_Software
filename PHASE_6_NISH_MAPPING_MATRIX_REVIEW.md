# Phase 6 NISH Mapping Matrix Review
## Review of Partially Covered Points from Mapping Matrix Template

**Date:** 2025-01-27  
**Status:** IN PROGRESS  
**Purpose:** Review and complete partially covered points from `project/nish/04_MAPPING/MAPPING_MATRIX_TEMPLATE.md`

---

## 📋 Source Document

**File:** `project/nish/04_MAPPING/MAPPING_MATRIX_TEMPLATE.md`  
**Purpose:** Map every legacy column to NSW target, with transform rules and risk flags  
**Status:** ⏳ Pending (Template with checklist items)

---

## ✅ Mapping Checklist Review

### From MAPPING_MATRIX_TEMPLATE.md (Lines 207-218)

#### 1. Complete table-level mapping
- **Status:** ✅ PARTIALLY COMPLETE
- **Coverage:** ~85%
- **Completed:**
  - ✅ NEPL → NSW table mapping identified in `PHASE_6_NISH_REVIEW_REPORT.md` (Section 2.1)
  - ✅ Mapping types identified (DIRECT, SPLIT, JOIN, TRANSFORM)
  - ✅ Key transformations documented (Items → L1/L2, Feeders → BOM level=0, etc.)
- **Missing:**
  - ⚠️ Complete Excel mapping matrix not generated
  - ⚠️ Some edge case tables not mapped (e.g., `contacts`, `organizations`)
  - ⚠️ Table-by-table detailed mapping document not created

#### 2. Complete column-level mapping
- **Status:** ⚠️ PARTIALLY COMPLETE
- **Coverage:** ~60%
- **Completed:**
  - ✅ High-level column mappings identified in review reports
  - ✅ Key transformations documented (tenant_id addition, renames, etc.)
  - ✅ Field-level changes documented (e.g., `sub_categories` → `subcategories`)
- **Missing:**
  - ❌ Detailed column-by-column mapping for each table
  - ❌ Transform rules not fully specified per column
  - ❌ Data type conversions not documented
  - ❌ Default value mappings not documented

#### 3. Complete key mapping
- **Status:** ⚠️ PARTIALLY COMPLETE
- **Coverage:** ~70%
- **Completed:**
  - ✅ Primary key preservation strategy identified (preserve old IDs where possible)
  - ✅ Key transformations documented (e.g., Items split affects PK strategy)
- **Missing:**
  - ❌ Table-by-table PK mapping decisions
  - ❌ Composite key handling not documented
  - ❌ ID remapping strategy for split tables (Items → L1/L2)
  - ❌ Foreign key mapping strategy

#### 4. Identify all transform rules
- **Status:** ✅ MOSTLY COMPLETE
- **Coverage:** ~90%
- **Completed:**
  - ✅ Transform rule types identified (PRESERVE, RENAME, SPLIT, JOIN, etc.)
  - ✅ Key transformations documented:
     - Items → L1/L2 Split (SPLIT)
     - Feeders → BOM level=0 (TRANSFORM)
     - Panels → quote_panels under quotation (TRANSFORM)
     - Clients → customers (RENAME)
     - Base price → sku_prices (EXTRACT)
- **Missing:**
  - ⚠️ Some edge case transform rules not documented
  - ⚠️ Complex transformations need detailed logic

#### 5. Assign priorities (P0/P1/P2/P3)
- **Status:** ⚠️ PARTIALLY COMPLETE
- **Coverage:** ~50%
- **Completed:**
  - ✅ Priority framework defined in template
  - ✅ Some tables identified as P0 (masters, core business)
- **Missing:**
  - ❌ Table-by-table priority assignment
  - ❌ Column-by-column priority assignment
  - ❌ Migration ordering based on priorities

#### 6. Assign risk levels (LOW/MEDIUM/HIGH/CRITICAL)
- **Status:** ⚠️ PARTIALLY COMPLETE
- **Coverage:** ~40%
- **Completed:**
  - ✅ Risk framework defined in template
  - ✅ Some high-risk transformations identified (L1/L2 split, BOM hierarchy restructure)
- **Missing:**
  - ❌ Table-by-table risk assessment
  - ❌ Column-by-column risk assessment
  - ❌ Risk mitigation strategies per risk item

#### 7. Document data quality checks
- **Status:** ⚠️ PARTIALLY COMPLETE
- **Coverage:** ~30%
- **Completed:**
  - ✅ Data quality check framework defined in template
  - ✅ Some checks identified (orphan FKs, null values)
- **Missing:**
  - ❌ Table-specific data quality checks
  - ❌ Pre-migration validation queries
  - ❌ Post-migration validation queries
  - ❌ Data quality baseline metrics

#### 8. Create risk register
- **Status:** ⚠️ PARTIALLY COMPLETE
- **Coverage:** ~50%
- **Completed:**
  - ✅ Risk framework defined
  - ✅ Some risks identified in review reports:
     - L1/L2 transformation complexity
     - BOM hierarchy restructure
     - Pricing model upgrade
- **Missing:**
  - ❌ Complete risk register with all identified risks
  - ❌ Risk mitigation plans
  - ❌ Risk ownership assignments

#### 9. Generate Excel mapping matrix
- **Status:** ❌ NOT STARTED
- **Coverage:** 0%
- **Missing:**
  - ❌ Excel file not created
  - ❌ Column Mapping sheet not populated
  - ❌ Table Mapping sheet not populated
  - ❌ Key Mapping sheet not populated
  - ❌ Risk Register sheet not populated

#### 10. Review and validate completeness
- **Status:** ⏳ IN PROGRESS
- **Coverage:** ~60%
- **Completed:**
  - ✅ High-level review completed
  - ✅ Gaps identified
- **Missing:**
  - ❌ Detailed validation of all mappings
  - ❌ Stakeholder review
  - ❌ Sign-off on mapping decisions

---

## 📊 Detailed Gap Analysis

### Table-Level Mapping Gaps

| NEPL Table | Mapping Status | Gap Details |
|------------|----------------|-------------|
| `contacts` | ⚠️ PARTIAL | Found in PDF generation but not fully mapped to NSW |
| `organizations` | ⚠️ PARTIAL | Found in PDF generation but not fully mapped to NSW |
| `users` | ✅ COMPLETE | Mapped to `users` with tenant_id + RBAC |
| `categories` | ✅ COMPLETE | Mapped to `categories` with tenant_id |
| `sub_categories` | ✅ COMPLETE | Mapped to `subcategories` (renamed) |
| `types` | ✅ COMPLETE | Mapped to `product_types` (renamed) |
| `items` | ⚠️ PARTIAL | Split transformation documented but detailed mapping pending |
| `components` | ❓ TBD | Mapping strategy not finalized |
| `master_boms` | ✅ COMPLETE | Mapped with tenant_id + guardrails |
| `proposal_boms` | ⚠️ PARTIAL | Transform to quote_boms documented but detailed mapping pending |
| `boms` | ✅ COMPLETE | Mapped to `quote_boms` (level=1/2) |
| `feeders` | ✅ COMPLETE | Mapped to `quote_boms` (level=0) |
| `panels` | ✅ COMPLETE | Mapped to `quote_panels` under quotation |
| `projects` | ✅ COMPLETE | Mapped with tenant_id |
| `clients` | ✅ COMPLETE | Mapped to `customers` (renamed) |
| `quotations` | ✅ COMPLETE | Mapped with tenant_id + enhancements |
| `quotation_items` | ⚠️ PARTIAL | Consolidated to quote_bom_items but detailed mapping pending |

### Column-Level Mapping Gaps

**Critical Missing Mappings:**

1. **Items → L1/L2 Split:**
   - ❌ Which columns go to `l1_intent_lines`?
   - ❌ Which columns go to `catalog_skus`?
   - ❌ How to handle `base_price`? (→ `sku_prices`)
   - ❌ How to handle attributes? (→ `l1_attributes` vs product attributes)

2. **Contacts Table:**
   - ❌ Full column list not documented
   - ❌ Mapping to NSW not determined (may be in `customers` or separate table)
   - ❌ Contact-Customer relationship not mapped

3. **Organizations/Company:**
   - ❌ Full column list not documented
   - ❌ Mapping to NSW not determined (may be tenant-level or separate)
   - ❌ Company logo/address fields not mapped

4. **Pricing Fields:**
   - ❌ `items.base_price` → `sku_prices` detailed mapping pending
   - ❌ `bom_items.unit_price` → `quote_bom_items.rate` with rate_source enum
   - ❌ Discount fields mapping pending

5. **Audit Fields:**
   - ✅ `created_at`, `updated_at` → preserved
   - ❌ New `audit_logs` table structure not fully mapped

### Transform Rules Gaps

**Missing Detailed Rules:**

1. **SPLIT Transformations:**
   - ❌ Items → L1/L2: Detailed split logic not documented
   - ❌ Which attributes go to L1 vs L2?
   - ❌ How to handle Make/Series? (L2 only)

2. **JOIN Transformations:**
   - ❌ `quotation_items` + `proposal_bom_items` → `quote_bom_items`: Consolidation logic not detailed
   - ❌ How to handle conflicting fields?

3. **DERIVE Transformations:**
   - ❌ `quote_bom_items.rate_source`: How to derive from legacy data?
   - ❌ `quote_bom_items.cost_head_id`: Default assignment logic?

4. **MAP Transformations:**
   - ❌ Status code mappings not documented
   - ❌ Enum value mappings not documented

### Priority Assignment Gaps

**Missing Priorities:**

- ❌ Complete P0 list (critical tables)
- ❌ Complete P1 list (high priority)
- ❌ Complete P2 list (medium priority)
- ❌ Complete P3 list (low priority)
- ❌ Migration ordering based on priorities

### Risk Assessment Gaps

**Missing Risk Assessments:**

1. **Data Quality Risks:**
   - ❌ Orphaned records assessment
   - ❌ NULL value analysis
   - ❌ Duplicate key analysis
   - ❌ Invalid enum value analysis

2. **Transformation Risks:**
   - ❌ L1/L2 split complexity risk (HIGH - documented)
   - ❌ BOM hierarchy restructure risk (HIGH - documented)
   - ❌ Pricing model upgrade risk (MEDIUM - documented)
   - ❌ Contact/Company mapping risk (UNKNOWN - not assessed)

3. **Business Logic Risks:**
   - ❌ Calculation formula preservation risk
   - ❌ Workflow preservation risk
   - ❌ Data loss risk

---

## 🎯 Action Plan to Complete Mapping Matrix

### Immediate Actions (High Priority)

1. **Complete Contact/Company Mapping**
   - Review `contacts` table structure
   - Review `organizations` table structure
   - Determine NSW mapping (separate tables or integrated)
   - Document column mappings

2. **Complete Items → L1/L2 Detailed Mapping**
   - Document which columns → `l1_intent_lines`
   - Document which columns → `catalog_skus`
   - Document `l1_l2_mappings` bridge table structure
   - Document attribute handling (L1 vs L2)

3. **Complete Column-Level Mappings**
   - For each NEPL table, map every column to NSW
   - Document transform rules per column
   - Document data type conversions
   - Document default values

4. **Create Excel Mapping Matrix**
   - Create `LEGACY_TO_NSW_MAPPING.xlsx`
   - Populate Column Mapping sheet
   - Populate Table Mapping sheet
   - Populate Key Mapping sheet
   - Populate Risk Register sheet

### Short-term Actions (Medium Priority)

5. **Complete Priority Assignment**
   - Assign P0/P1/P2/P3 to all tables
   - Assign priorities to columns (if needed)
   - Create migration ordering based on priorities

6. **Complete Risk Assessment**
   - Assess all tables for risks
   - Assess all columns for risks
   - Create complete risk register
   - Document mitigation strategies

7. **Complete Data Quality Checks**
   - Create pre-migration validation queries
   - Create post-migration validation queries
   - Document data quality baseline metrics
   - Document expected data quality issues

### Long-term Actions (Lower Priority)

8. **Review and Validation**
   - Detailed review of all mappings
   - Stakeholder review
   - Sign-off on mapping decisions
   - Update mapping matrix based on feedback

---

## 📋 Completion Checklist

### Table-Level Mapping
- [x] High-level table mapping identified
- [x] Mapping types identified (DIRECT, SPLIT, JOIN, TRANSFORM)
- [ ] Complete Excel table mapping sheet
- [ ] All edge case tables mapped (contacts, organizations)
- [ ] Table-by-table detailed mapping document

### Column-Level Mapping
- [x] High-level column mappings identified
- [ ] Complete column-by-column mapping for all tables
- [ ] Transform rules specified per column
- [ ] Data type conversions documented
- [ ] Default value mappings documented

### Key Mapping
- [x] Primary key preservation strategy identified
- [ ] Table-by-table PK mapping decisions
- [ ] Composite key handling documented
- [ ] ID remapping strategy for split tables
- [ ] Foreign key mapping strategy

### Transform Rules
- [x] Transform rule types identified
- [x] Key transformations documented
- [ ] All edge case transform rules documented
- [ ] Complex transformation logic detailed

### Priority Assignment
- [x] Priority framework defined
- [ ] Complete P0/P1/P2/P3 assignment for all tables
- [ ] Migration ordering based on priorities

### Risk Assessment
- [x] Risk framework defined
- [x] Some risks identified
- [ ] Complete risk register
- [ ] Risk mitigation plans
- [ ] Risk ownership assignments

### Data Quality Checks
- [x] Data quality check framework defined
- [ ] Table-specific data quality checks
- [ ] Pre-migration validation queries
- [ ] Post-migration validation queries
- [ ] Data quality baseline metrics

### Excel Matrix Generation
- [ ] Excel file created
- [ ] Column Mapping sheet populated
- [ ] Table Mapping sheet populated
- [ ] Key Mapping sheet populated
- [ ] Risk Register sheet populated

### Review and Validation
- [x] High-level review completed
- [x] Gaps identified
- [ ] Detailed validation of all mappings
- [ ] Stakeholder review
- [ ] Sign-off on mapping decisions

---

## 📊 Overall Completion Status

| Category | Completion | Status |
|----------|------------|--------|
| Table-Level Mapping | ~85% | ✅ MOSTLY COMPLETE |
| Column-Level Mapping | ~60% | ⚠️ PARTIALLY COMPLETE |
| Key Mapping | ~70% | ⚠️ PARTIALLY COMPLETE |
| Transform Rules | ~90% | ✅ MOSTLY COMPLETE |
| Priority Assignment | ~50% | ⚠️ PARTIALLY COMPLETE |
| Risk Assessment | ~40% | ⚠️ PARTIALLY COMPLETE |
| Data Quality Checks | ~30% | ⚠️ PARTIALLY COMPLETE |
| Risk Register | ~50% | ⚠️ PARTIALLY COMPLETE |
| Excel Matrix | 0% | ❌ NOT STARTED |
| Review & Validation | ~60% | ⚠️ PARTIALLY COMPLETE |

**Overall Completion:** ~55%

---

## 🎯 Next Steps

1. **Complete Contact/Company Review** (High Priority)
   - Review `contacts` and `organizations` tables
   - Document NSW mapping

2. **Complete Items → L1/L2 Detailed Mapping** (High Priority)
   - Document column-by-column split logic
   - Document attribute handling

3. **Create Excel Mapping Matrix** (High Priority)
   - Generate Excel file with all sheets
   - Populate with current mappings

4. **Complete Priority & Risk Assignment** (Medium Priority)
   - Assign priorities to all tables
   - Complete risk register

5. **Complete Data Quality Checks** (Medium Priority)
   - Create validation queries
   - Document baseline metrics

---

**Status:** MAPPING MATRIX REVIEW IN PROGRESS  
**Completion:** ~55% of mapping matrix checklist items  
**Critical Gaps:** Contact/Company mapping, Items L1/L2 detailed mapping, Excel matrix generation  
**Next:** Complete high-priority gaps and generate Excel matrix
