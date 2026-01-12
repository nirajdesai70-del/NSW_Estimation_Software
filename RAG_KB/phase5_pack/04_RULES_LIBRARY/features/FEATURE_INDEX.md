---
Source: features/FEATURE_INDEX.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T02:46:38.052158
KB_Path: phase5_pack/04_RULES_LIBRARY/features/FEATURE_INDEX.md
---

# Feature Index — Module Documentation Quick Reference

**Date:** 2025-12-17 (IST)  
**Status:** Phase 1 Complete ✅

---

## Module Overview

| Module | Baseline Tag | Primary Reference | Change Evidence | Status |
|--------|-------------|-------------------|-----------------|--------|
| **Component/Item Master** | `BASELINE_COMPONENT_ITEM_MASTER_20251217` | `_general/08_PRODUCT_MODULE.md` | `changes/component_item_master/` | ✅ Frozen |
| **Quotation** | `BASELINE_QUOTATION_20251217` | `_general/07_QUOTATION_MODULE.md` | `changes/quotation/` | ✅ Frozen |
| **Master BOM** | `BASELINE_MASTER_BOM_20251217` | `_general/09_BOM_MODULE.md` | `changes/master_bom/` | ✅ Frozen |
| **Feeder Library** | `BASELINE_FEEDER_LIBRARY_20251217` | `_general/V2_FEEDER_LIBRARY_COMPREHENSIVE_ANALYSIS.md` | `changes/feeder_library/` | ✅ Frozen |
| **Proposal BOM** | `BASELINE_PROPOSAL_BOM_20251217` | `_general/V2_MASTER_BOM_VS_PROPOSAL_BOM_ANALYSIS.md` | `changes/proposal_bom/` | ✅ Frozen |
| **Project** | `BASELINE_PROJECT_20251217` | `_general/PROJECT_BACKEND_DESIGN_INDEX.md` | `changes/project/` | ✅ Frozen |
| **Master** | `BASELINE_MASTER_20251217` | `_general/MASTER_MODULE_OVERVIEW.md` | `changes/master/` | ✅ Frozen |
| **Employee/Role** | `BASELINE_EMPLOYEE_ROLE_20251217` | `_general/12_USER_MANAGEMENT.md` | `changes/employee/` | ✅ Frozen |

---

## Component/Item Master

**Baseline:** `BASELINE_COMPONENT_ITEM_MASTER_20251217`  
**Batches:** 01-02  
**Primary Reference:** `features/component_item_master/_general/08_PRODUCT_MODULE.md`

**Key Areas:**
- Category, Subcategory, Product Type
- Attributes, Make, Series
- Generic/Specific Products
- Price Lists
- Import/Export
- Catalog Health

**Change Evidence:** `changes/component_item_master/`

---

## Quotation

**Baseline:** `BASELINE_QUOTATION_20251217`  
**Batches:** 03-04  
**Primary Reference:** `features/quotation/_general/07_QUOTATION_MODULE.md`

**Key Areas:**
- Quotation V2 (Panel/Feeder/BOM hierarchy)
- Discount Rules
- Costing
- Workflows
- Reports/Exports

**Change Evidence:** `changes/quotation/`

---

## Master BOM

**Baseline:** `BASELINE_MASTER_BOM_20251217`  
**Batches:** 05-06  
**Primary Reference:** `features/master_bom/_general/09_BOM_MODULE.md`

**Key Areas:**
- Structure
- Items
- Validation
- Import/Export
- Workflows

**Change Evidence:** `changes/master_bom/`

---

## Feeder Library

**Baseline:** `BASELINE_FEEDER_LIBRARY_20251217`  
**Batches:** 07  
**Primary Reference:** `features/feeder_library/_general/V2_FEEDER_LIBRARY_COMPREHENSIVE_ANALYSIS.md`

**Key Areas:**
- Structure
- Items
- Validation
- Workflows

**Change Evidence:** `changes/feeder_library/`

---

## Proposal BOM

**Baseline:** `BASELINE_PROPOSAL_BOM_20251217`  
**Batches:** 08  
**Primary Reference:** `features/proposal_bom/_general/V2_MASTER_BOM_VS_PROPOSAL_BOM_ANALYSIS.md`

**Key Areas:**
- Structure
- Workflows
- Linkage to Quotation
- Validation

**Change Evidence:** `changes/proposal_bom/`

---

## Project

**Baseline:** `BASELINE_PROJECT_20251217`  
**Batches:** 09A + 10A  
**Primary Reference:** `features/project/_general/PROJECT_BACKEND_DESIGN_INDEX.md`

**Key Areas:**
- Structure
- Workflows
- Linkage to Quotation
- Status/Approvals
- Reports

**Change Evidence:** `changes/project/`

---

## Master (Org/Vendor/PDF)

**Baseline:** `BASELINE_MASTER_20251217`  
**Batches:** 10B  
**Primary Reference:** `features/master/_general/MASTER_MODULE_OVERVIEW.md`

**Key Areas:**
- Organization (references Project/Quotation)
- Vendor (references Component/Item Master)
- PDF Formats (references Quotation)
- Templates
- Defaults

**Change Evidence:** `changes/master/` (minimal)

**Note:** Master module is reference-based (stubs only), with operational workflows in owning modules.

---

## Employee/Role

**Baseline:** `BASELINE_EMPLOYEE_ROLE_20251217`  
**Batches:** 10C  
**Primary Reference:** `features/employee/_general/12_USER_MANAGEMENT.md`

**Key Areas:**
- Users
- Roles
- Permissions (references Security)
- Workflows
- Audit

**Change Evidence:** `changes/employee/` (security docs in `changes/security/`)

---

## Security (Cross-Cutting)

**Status:** Created during Batch 10C  
**Primary Reference:** `features/security/_general/36_SECURITY_GUIDE.md`  
**Change Evidence:** `changes/security/phase_1/`

**Key Areas:**
- Authentication
- Authorization
- Security Best Practices

**Note:** Security is a cross-cutting concern, not a standalone baseline.

---

## Navigation

- **Module READMEs:** See [INDEX.md](../INDEX.md) for links
- **Baseline Register:** [docs/PHASE_1/BASELINE_FREEZE_REGISTER.md](../docs/PHASE_1/BASELINE_FREEZE_REGISTER.md)
- **Change Index:** [changes/CHANGE_INDEX.md](../changes/CHANGE_INDEX.md)

---

**Last Updated:** 2025-12-17 (IST)

