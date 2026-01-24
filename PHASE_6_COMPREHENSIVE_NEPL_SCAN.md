# Phase 6 Comprehensive NEPL Scan
## Complete Review of NEPL Estimation Software Legacy System

**Date:** 2025-01-27  
**Status:** ✅ COMPLETE  
**Purpose:** Comprehensive scan and review of all NEPL Estimation Software functions, features, and working patterns

---

## 🎯 Executive Summary

This document provides a comprehensive scan of **NEPL Estimation Software V2** - the legacy system that Phase 6 must preserve and enhance. This scan covers all functions, features, workflows, data structures, and business rules.

**Critical Rule:** NEPL V2 is the **reference truth**. Phase 6 must preserve all functionality while adding enhancements.

**Note:** This document consolidates information from the detailed `PHASE_6_NEPL_BASELINE_REVIEW.md`. For detailed function-by-function documentation, refer to that document.

---

## 📋 Scan Coverage

### ✅ Functions Scanned:

1. ✅ **Company/Tenant Setup** - Documented
2. ✅ **Customer Management** - Documented
3. ⚠️ **Contact Person Management** - Partially documented (needs completion)
4. ✅ **Item Management** - Fully documented
5. ✅ **Category Management** - Fully documented
6. ✅ **Master BOM** - Documented
7. ✅ **Proposal BOM** - Documented
8. ✅ **Feeder Management** - Fully documented
9. ✅ **Quotation Management** - Fully documented
10. ✅ **Panel Management** - Fully documented
11. ✅ **Project Management** - Fully documented
12. ⚠️ **PDF Export** - Partially documented (needs completion)
13. ⚠️ **Excel Export** - Partially documented (needs completion)
14. ✅ **Component Master** - Documented
15. ✅ **BOM Management** - Documented
16. ✅ **Pricing & Discount** - Documented
17. ✅ **Calculation Formulas** - Documented (FROZEN)

---

## 📊 System Overview

### Core Architecture
```
Project
  └── Panel
      └── Feeder (Level-0 BOM)
          └── BOM (Level-1/2 BOM)
              └── BOM Items
                  ├── Item (from Item Master)
                  └── Component (from Component Master)

Category
  └── Subcategory
      └── Type
          └── Attribute
              └── Item (uses hierarchy)
```

### Core Modules (8 modules)
1. Project Management
2. Panel Management
3. Feeder Management
4. BOM Management
5. Item Master Management
6. Component Master Management
7. Quotation Management
8. Master Data Management (Category Hierarchy)

---

## 💰 Calculation Formulas (FROZEN)

### Item-Level Calculation
```
NetRate = BaseRate × (1 - Discount/100)
AmountTotal = NetRate × TotalQty
```

### Roll-Up Calculations (Golden Rule)
```
BOM_TotalCost = SUM(All BOM Item AmountTotal)
Feeder_TotalCost = SUM(All Component AmountTotal in Feeder)
Panel_TotalCost = SUM(All Component AmountTotal in Panel)
Quotation_Total = SUM(All Quotation Item AmountTotal)
```

**Critical:** NO multipliers at roll-up level. Only SUM of AmountTotal.

---

## 🔄 NEPL → NSW Key Transformations

### Transformation 1: Multi-Tenant Isolation
- **NEPL:** No tenant concept
- **NSW:** All tables have `tenant_id` (except `tenants`)

### Transformation 2: L1/L2 Split
- **NEPL:** Single `items` table
- **NSW:** Split into `l1_intent_lines` + `catalog_skus` + `l1_l2_mappings`

### Transformation 3: BOM Hierarchy Restructure
- **NEPL:** Project → Panel → Feeder → BOM
- **NSW:** Quotation → Panel → BOM (level=0/1/2)

### Transformation 4: Pricing Model Upgrade
- **NEPL:** Base price on items → unit price on BOM items
- **NSW:** Price lists → SKU prices (L2) → Quote BOM item rates (with rate_source)

### Transformation 5: RBAC Addition
- **NEPL:** Basic users only
- **NSW:** Full RBAC (roles, permissions, user_roles)

### Transformation 6: CostHead System Addition
- **NEPL:** No cost head categorization
- **NSW:** CostHead system (MATERIAL, LABOUR, OTHER buckets)

---

## ⚠️ Gaps Identified

### Functions Not Fully Documented:
1. ⚠️ **Contact Person Management**
   - Found in PDF generation but not fully documented
   - Need to review: Contact CRUD, Contact-Customer relationship

2. ⚠️ **PDF Export Details**
   - Found in codebase but not in baseline review
   - Need to document: PDF template, fields included, formatting

3. ⚠️ **Excel Export Details**
   - Found in codebase but not in baseline review
   - Need to document: Excel format, columns, export logic

4. ⚠️ **Company/Organization Setup**
   - Found in PDF generation but not fully documented
   - Need to review: Company master, logo, address, contact info

---

## ✅ What Must Be Preserved

### Non-Negotiable Functions:
1. ✅ Estimation Logic (Panel → Feeder → BOM → Item)
2. ✅ Category / Subcategory / Type / Attribute Hierarchy
3. ✅ Item Master and Component Master
4. ✅ BOM Calculation Logic
5. ✅ Quotation Lifecycle
6. ✅ BOM Reuse Capabilities
7. ✅ Pricing Override Capability

---

## 📊 Data Model Summary

### NEPL Tables (~20 tables)
- **Auth:** `users`
- **Master Data:** `categories`, `sub_categories`, `types`, `attributes`, `items`, `components`
- **Project/Customer:** `projects`, `clients`, `panels`, `feeders`
- **BOM:** `boms`, `bom_items`, `master_boms`, `proposal_boms`
- **Quotation:** `quotations`, `quotation_items`

### NSW Tables (34 tables)
- **Auth:** `tenants`, `users`, `roles`, `user_roles`
- **CIM:** 12 tables (categories, subcategories, product_types, attributes, l1_intent_lines, catalog_skus, etc.)
- **MBOM:** 2 tables
- **QUO:** 5 tables
- **PRICING:** 3 tables
- **SHARED:** 3 tables
- **TAX:** 1 table
- **AUDIT:** 1 table
- **AI:** 1 table

---

## 🔗 Related Documents

- **Detailed Baseline Review:** `PHASE_6_NEPL_BASELINE_REVIEW.md` (comprehensive function-by-function documentation)
- **Review Verification:** `PHASE_6_NEPL_REVIEW_VERIFICATION.md` (function coverage check)
- **NISH Review Report:** `project/nish/PHASE_6_NISH_REVIEW_REPORT.md` (business flows and data model)

---

**Status:** ✅ COMPLETE  
**Last Updated:** 2025-01-27  
**Next Action:** Complete remaining gap reviews (Contact Person, PDF/Excel, Company)
