# FEATURE_CODE_MAP — Phase 2

**Repository:** NSW_Estimation_Software  
**Source:** ROUTE_MAP.md + source_snapshot codebase  
**Purpose:** Feature → Controllers → Services → Models → Views → JS mapping  
**Status:** In Progress (First Pass)  
**Date:** 2025-12-17 (IST)

---

## Overview

This map connects each frozen module baseline to its implementation code. It is generated from:
- Route-to-controller mappings (ROUTE_MAP.md)
- Controller file analysis (imports, method signatures)
- View directory structure
- Model and Service directory structure

**Note:** This is a first pass. Unknowns are marked as "TBD" and will be completed in subsequent passes.

---

## Dashboard Module

### Controllers
- `HomeController`

### Models
- TBD

### Services
- TBD

### Views
- `resources/views/home/index.blade.php`

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `home` (GET `/`, `/home`)

### Cross-Module Touchpoints
- None

---

## Component/Item Master Module

### Controllers
- `CategoryController`
- `SubCategoryController`
- `ItemController` (Product Type)
- `MakeController`
- `SeriesController`
- `AttributeController`
- `CategoryAttributeController`
- `GenericController`
- `ProductController` (Specific Product)
- `PriceController`
- `ImportController`
- `CatalogHealthController`
- `CatalogCleanupController`

### Models
- `Category` (inferred from CategoryController)
- `SubCategory` (inferred from SubCategoryController)
- `Item` / `ProductType` (inferred from ItemController)
- `Make` (inferred from MakeController)
- `Series` (inferred from SeriesController)
- `Attribute` (inferred from AttributeController)
- `CategoryAttribute` (inferred from CategoryAttributeController)
- `Generic` (inferred from GenericController)
- `Product` (inferred from ProductController)
- `Price` (inferred from PriceController)
- TBD (additional models)

### Services
- TBD (scanning for services)

### Views
- `resources/views/category/` (index, create, edit, addmore)
- `resources/views/subcategory/` (index, create, edit)
- `resources/views/item/` or `resources/views/product-type/` (index, create, edit)
- `resources/views/make/` (index, create, edit)
- `resources/views/series/` (index, create, edit)
- `resources/views/attribute/` (index, create, edit)
- `resources/views/generic/` (index, create, edit)
- `resources/views/product/` (index, create, edit, bom-list)
- `resources/views/price/` (index, create, edit)
- `resources/views/import/` (importview, importtempview)
- `resources/views/catalog-health/` (index)
- `resources/views/catalog-cleanup/` (index)
- TBD (verify actual view structure)

### JS Files
- TBD (check `public/js/` and `resources/js/`)

### Routes (from ROUTE_MAP)
- `category.*`, `subcategory.*`, `item.*`, `make.*`, `series.*`, `attribute.*`, `category-attribute.*`, `generic.*`, `product.*`, `price.*`, `import.*`, `catalog-health.*`, `catalog-cleanup.*`

### Cross-Module Touchpoints
- Used by Quotation (via AJAX endpoints)
- Used by Master BOM (item/product lookups)

---

## Quotation Module

### Controllers
- `QuotationController` (Legacy)
- `QuotationV2Controller` (V2)
- `QuotationDiscountRuleController`
- `QuotationDiscountRuleTestController`
- `ReuseController`

### Models
- `Quotation` (inferred from QuotationController)
- `QuotationSaleBom` (inferred from legacy routes)
- `QuotationDiscountRule` (inferred from QuotationDiscountRuleController)
- `Panel` (inferred from V2 routes)
- `Feeder` (inferred from V2 routes)
- `Bom` / `BomItem` (inferred from V2 routes)
- TBD (additional models)

### Services
- TBD (scanning for Quotation-related services)

### Views
- `resources/views/quotation/` (index, create, edit, addmore, step, step-panel, bom-list)
- `resources/views/quotation/v2/` (index, panel, bom-edit)
- `resources/views/quotation/discount-rules/` (index, create, edit, show)
- TBD (verify actual view structure)

### JS Files
- TBD (check `public/js/quotation/` and `resources/js/quotation/`)

### Routes (from ROUTE_MAP)
- `quotation.*` (Legacy)
- `quotation.v2.*` (V2)
- `quotation.discount-rules.*`
- `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.makes` (AJAX endpoints)
- `api.reuse.*` (Reuse search)
- `reuse.*` (Reuse apply)

### Cross-Module Touchpoints

#### Master BOM Integration
- Route: `quotation.v2.applyMasterBom` → `QuotationV2Controller@applyMasterBom`
- Touchpoint: Master BOM module
- Purpose: Apply Master BOM template to Quotation V2

#### Feeder Library Integration
- Route: `quotation.v2.applyFeederTemplate` → `QuotationV2Controller@applyFeederTemplate`
- Touchpoint: Feeder Library module
- Purpose: Apply Feeder template to Quotation V2 panel

#### Proposal BOM Integration
- Route: `quotation.v2.applyProposalBom` → `QuotationV2Controller@applyProposalBom`
- Touchpoint: Proposal BOM module
- Purpose: Apply Proposal BOM to Quotation V2

#### Component/Item Master Integration
- Routes: `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.makes`
- Touchpoint: Component/Item Master module
- Purpose: AJAX lookups for category/subcategory/item/product/make/series

---

## Master BOM Module

### Controllers
- `MasterBomController`

### Models
- `MasterBom` (inferred from MasterBomController)
- `MasterBomItem` (inferred from addmore/remove routes)
- TBD (additional models)

### Services
- TBD

### Views
- `resources/views/masterbom/` (index, create, edit, addmore)
- TBD (verify actual view structure)

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `masterbom.*`

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-master-bom route)
- Uses Component/Item Master (item/product lookups)

---

## Feeder Library Module

### Controllers
- `FeederTemplateController`

### Models
- `FeederTemplate` (inferred from FeederTemplateController)
- TBD (additional models)

### Services
- TBD

### Views
- `resources/views/feeder-library/` (index, create, show, edit)
- TBD (verify actual view structure)

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `feeder-library.*`

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-feeder-template route)
- Uses Master BOM concepts (structure integration)

---

## Proposal BOM Module

### Controllers
- `ProposalBomController`

### Models
- `ProposalBom` (inferred from ProposalBomController)
- TBD (additional models)

### Services
- TBD

### Views
- `resources/views/proposal-bom/` (index, show)
- TBD (verify actual view structure)

### Routes (from ROUTE_MAP)
- `proposal-bom.*`
- Note: Additional routes likely under Quotation V2 apply endpoints and search APIs

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-proposal-bom route, search APIs)
- Can be promoted to Master BOM (promote route)
- Uses Master BOM concepts (structure)

---

## Project Module

### Controllers
- `ProjectController`
- `ClientController`
- `ContactController`

### Models
- `Project` (inferred from ProjectController)
- `Client` (inferred from ClientController)
- `Contact` (inferred from ContactController)
- TBD (additional models)

### Services
- TBD

### Views
- `resources/views/project/` (index, create, edit)
- `resources/views/client/` (index, create, edit)
- `resources/views/contact/` (index, create, edit)
- TBD (verify actual view structure)

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `project.*`
- `client.*`
- `contact.*`

### Cross-Module Touchpoints
- Links to Quotation (project-quotation relationship)
- Client/Contact masters used by Project/Quotation

---

## Master Module

### Controllers
- `OrganizationController`
- `VendorController`
- `ImportController` (PDF container methods: `pdfcontain`, `pdfcontainsave`)

### Models
- `Organization` (inferred from OrganizationController)
- `Vendor` (inferred from VendorController)
- TBD (PDF container model)

### Services
- TBD

### Views
- `resources/views/organization/` (index, create, edit)
- `resources/views/vendor/` (index, create, edit)
- `resources/views/pdfcontain/` (index)
- TBD (verify actual view structure)

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `organization.*`
- `vendor.*`
- `pdfcontain.*` (Note: Controller name is misleading - ImportController, but feature is Master/PDF container)

### Cross-Module Touchpoints
- Organization used by Project/Quotation (master data)
- Vendor used by Component/Item Master (Make/Series concepts)
- PDF container used by Quotation (PDF generation)

---

## Employee/Role Module

### Controllers
- `UserController`
- `RoleController`

### Models
- `User` (inferred from UserController)
- `Role` (inferred from RoleController)
- TBD (additional models)

### Services
- TBD

### Views
- `resources/views/user/` (index, create, edit)
- `resources/views/role/` (index, create, edit)
- TBD (verify actual view structure)

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `user.*`
- `role.*`

### Cross-Module Touchpoints
- Used by all modules (authentication/authorization)
- Security policies apply system-wide

---

## Security Module (Cross-Cutting)

### Controllers
- TBD (Security handled via middleware)

### Models
- TBD

### Services
- TBD

### Views
- TBD

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- No direct routes (handled via middleware: `auth`, `throttle`, etc.)

### Cross-Module Touchpoints
- Applies to all modules (authentication, authorization, CSRF, SQL injection, XSS protection)

---

## Shared/Ops Module

### Controllers
- `CronController` (mySQLDownload)
- `Closure` (clear cache route)

### Models
- TBD

### Services
- TBD

### Views
- TBD

### JS Files
- TBD

### Routes (from ROUTE_MAP)
- `mySQLDownload`
- `clear` (Maintenance route; verify if enabled in production)

### Cross-Module Touchpoints
- Maintenance operations affecting all modules

---

## Next Steps

1. **Complete Model Discovery:** Scan controller imports to identify all models
2. **Complete Service Discovery:** Identify service classes and their usage
3. **Verify View Structure:** Confirm actual view file locations
4. **Map JS Files:** Identify JavaScript files per module
5. **Complete Cross-Module Touchpoints:** Document all inter-module dependencies
6. **Generate FILE_OWNERSHIP:** Mark protected/core files

---

**Last Updated:** 2025-12-17 (IST)  
**Status:** First Pass Complete (TBD items to be completed in next pass)

