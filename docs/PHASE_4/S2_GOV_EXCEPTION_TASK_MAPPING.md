# S2 GOV-001: Exception → Task Mapping Table

**Task ID:** NSW-P4-S2-GOV-001  
**Status:** ✅ Complete  
**Gate:** G3  
**Risk:** HIGH  
**Date:** 2025-12-18

---

## Objective

Convert ownership exceptions into split/adapter task stubs to prevent re-discovering the same split logic later in SHARED/CIM/BOM.

---

## Exception → Task Mapping Table (Canonical)

**NOTE:**  
This table includes both:
1) **S1 Ownership Exceptions** (file-level split ownership from FILE_OWNERSHIP.md), and
2) **S2 Architectural Exceptions** (logical or target-ownership mismatches discovered during isolation).

Only category (1) was required to appear in S1 GOV-002. Category (2) entries are intentional architectural exceptions discovered during S2 isolation planning.

| Exception File/Area | Owning Module(s) | Methods/Routes Owned By | Why Exception | Split Target (Future) | Adapter/Wrapper Needed | Proposed Task ID(s) | Future S4 Tasks |
|---------------------|------------------|-------------------------|---------------|----------------------|------------------------|---------------------|-----------------|
| `ImportController.php` | CIM + MASTER | **CIM:** `/import*` routes<br>**MASTER:** `/pdfcontain*` routes | Controller hosts both CIM import and Master/PDF container operations | `CIM/ImportController`<br>`MASTER/PdfContainController` | Adapter for shared `Setting` table access (PDF formats) | NSW-P4-S2-CIM-001<br>NSW-P4-S2-MASTER-001 | S4: Migrate consumers to split controllers |
| `QuotationController` shared API methods | QUO (current)<br>SHARED (target) | **QUO-owned but shared:**<br>`api.category.*`<br>`api.item.*`<br>`api.product.*`<br>`api.make.*`<br>`api.makes` | Quotation owns dropdown APIs used by legacy+V2 and other modules | `SHARED/CatalogLookupController` | Contract + adapter to CIM for catalog data | NSW-P4-S2-SHARED-001<br>NSW-P4-S2-SHARED-002<br>NSW-P4-S2-CIM-002 | S4: Migrate CIM, MBOM, FEED, PBOM, QUO to CatalogLookupContract |
| `routes/api.php` | QUO (current)<br>SHARED (target) | Shared endpoint route definitions:<br>- Catalog lookup routes<br>- Reuse search routes | Shared endpoints live in Quotation module route file | Extract route groups to SHARED boundary | Route-group adapter (Phase-4) | NSW-P4-S2-SHARED-002 | S4: Route migration to SHARED namespace |
| `QuotationV2Controller` apply + core | QUO (PROTECTED) | **PROTECTED Core:**<br>V2 quotation logic<br>**Apply endpoints:**<br>`quotation.v2.applyMasterBom`<br>`quotation.v2.applyFeederTemplate`<br>`quotation.v2.applyProposalBom` | PROTECTED; cross-module apply bundles require wrapper-only access | Wrapper-only seams (no split) | Wrappers around apply + costing/qty services | NSW-P4-S2-QUO-002<br>NSW-P4-S2-QUO-003<br>**BLOCKED** until NSW-P4-S2-QUO-REVERIFY-001 | S4: Adopt wrapper entry points for V2 apply flows |
| `ReuseController.php` | QUO (current)<br>SHARED (target) | **QUO-owned but shared:**<br>`api.reuse.*` routes | Reuse search endpoints used cross-module | `SHARED/ReuseSearchController` | Contract for reuse search | NSW-P4-S2-SHARED-001<br>NSW-P4-S2-SHARED-002 | S4: Migrate consumers to ReuseSearchContract |

---

## Detailed Split Analysis

### 1. ImportController Split

**Current State:**
- Single controller: `source_snapshot/app/Http/Controllers/ImportController.php`
- CIM routes: `/import*` (Component/Item Master import/export)
- MASTER routes: `/pdfcontain*` (PDF container formats from Settings table)

**Split Target:**
- `CIM/ImportController`: Import/export for products, categories, items
- `MASTER/PdfContainController`: PDF format management

**Adapter Seam:**
- `PdfContainSettingsAdapter`: Adapter for CIM to access PDF settings (via MASTER contract)
- Prevents CIM from directly accessing Settings table

**Future S4 Tasks:**
- Migrate CIM import consumers
- Migrate PDF container consumers
- Remove old ImportController

---

### 2. QuotationController Shared API Split

**Current State:**
- `QuotationController` owns both:
  - Legacy quotation logic (QUO-owned)
  - Shared catalog lookup APIs (should be SHARED-owned)

**Shared API Methods (to extract):**
- `getSubCategories()` → `api.category.subcategories`
- `getItems()` → `api.category.items`
- `getProducts()` → `api.category.products`
- `getProductsByItem()` → `api.item.products`
- `getMakes()` → `api.product.makes`
- `getSeriesApi()` → `api.make.series`
- `getDescriptions()` → `api.product.descriptions`
- `getMakesByCategory()` → `api.category.makes`
- `getAllMakes()` → `api.makes`

**Split Target:**
- `SHARED/CatalogLookupController`: All catalog lookup endpoints
- `QUO/QuotationController`: Legacy quotation logic only

**Adapter Seam:**
- `CatalogLookupContract`: Contract defining inputs/outputs
- Adapter to CIM models for data access

**Future S4 Tasks:**
- Migrate CIM consumers (views/JS) to CatalogLookupContract
- Migrate MBOM consumers to CatalogLookupContract
- Migrate FEED consumers to CatalogLookupContract
- Migrate PBOM consumers to CatalogLookupContract
- Migrate QUO legacy consumers to CatalogLookupContract
- Remove compat endpoints after S5 validation

---

### 3. Routes/API File Split

**Current State:**
- `routes/api.php` contains shared endpoint route definitions
- Routes are in QUO module namespace

**Split Target:**
- Extract catalog lookup route group to SHARED
- Extract reuse search route group to SHARED
- Keep QUO-specific routes in QUO namespace

**Adapter Seam:**
- Route-group adapter maintains backward compatibility during transition
- Route aliases for deprecation period

**Future S4 Tasks:**
- Migrate route definitions
- Update route references
- Remove old route definitions after S5

---

### 4. QuotationV2Controller (PROTECTED - No Split)

**Current State:**
- PROTECTED core: V2 quotation logic
- Apply endpoints: Master BOM, Feeder, Proposal BOM apply
- Costing/Quantity services: Core business logic

**Approach:**
- **NO SPLIT** - Wrapper-only seams
- Wrappers around apply endpoints
- Wrappers around costing/qty services

**Adapter Seam:**
- `V2ApplyWrapper`: Wrapper for apply endpoints (Bundle A)
- `CostingServiceWrapper`: Wrapper for costing logic (Bundle B)
- `QuantityServiceWrapper`: Wrapper for quantity logic (Bundle B)

**BLOCKER:**
- Must complete NSW-P4-S2-QUO-REVERIFY-001 first
- Verify routes ↔ controller methods match

**Future S4 Tasks:**
- Adopt wrapper entry points for V2 apply flows
- Migrate apply callers to wrapper interfaces

---

### 5. ReuseController Split

**Current State:**
- `ReuseController` owns reuse search endpoints
- Used by multiple modules for BOM/item reuse

**Shared API Methods (to extract):**
- All `api.reuse.*` routes

**Split Target:**
- `SHARED/ReuseSearchController`: Reuse search endpoints

**Adapter Seam:**
- `ReuseSearchContract`: Contract defining search inputs/outputs

**Future S4 Tasks:**
- Migrate consumers to ReuseSearchContract
- Remove old ReuseController after S5

---

## Consumer Migration List (S4 Preparation)

### CatalogLookupContract Consumers (Future S4 Tasks)

| Consumer Module | Current Endpoint | Target Contract | S4 Task |
|----------------|------------------|-----------------|---------|
| CIM (Product create/edit) | `product.getsubcategory`<br>`product.getproducttype` | `CatalogLookupContract` | NSW-P4-S4-CIM-001 |
| MBOM (BOM create/edit/copy) | `masterbom.getsubcategory`<br>`masterbom.getdescription` | `CatalogLookupContract` | NSW-P4-S4-MBOM-001 |
| FEED (Template operations) | Internal catalog lookups | `CatalogLookupContract` | NSW-P4-S4-FEED-001 |
| PBOM (BOM operations) | Internal catalog lookups | `CatalogLookupContract` | NSW-P4-S4-PBOM-001 |
| QUO Legacy | `product.*` AJAX endpoints | `CatalogLookupContract` | NSW-P4-S4-QUO-001 |
| QUO V2 | `api.category.*`<br>`api.item.*`<br>`api.product.*` | `CatalogLookupContract` | NSW-P4-S4-QUO-001 |

### ReuseSearchContract Consumers (Future S4 Tasks)

| Consumer Module | Current Endpoint | Target Contract | S4 Task |
|----------------|------------------|-----------------|---------|
| QUO V2 | `api.reuse.*` | `ReuseSearchContract` | NSW-P4-S4-QUO-001 |
| MBOM | Internal reuse searches | `ReuseSearchContract` | NSW-P4-S4-MBOM-001 |
| FEED | Internal reuse searches | `ReuseSearchContract` | NSW-P4-S4-FEED-001 |
| PBOM | Internal reuse searches | `ReuseSearchContract` | NSW-P4-S4-PBOM-001 |

---

## Evidence

**Authority References:**
- FILE_OWNERSHIP: `trace/phase_2/FILE_OWNERSHIP.md`
- Batch-2 Planning: `docs/PHASE_3/04_TASK_REGISTER/BATCH_2_S2.md` (Section 6.1)
- S1 Exceptions: `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md` (Section 2)

**Gate Satisfied By:**
- Exception mapping table completed and verified against FILE_OWNERSHIP
- All split targets identified
- All adapter seams defined
- Consumer migration list prepared for S4

---

**Task Status:** ✅ Complete  
**Next Task:** NSW-P4-S2-GOV-002 (Boundary Blocks)

