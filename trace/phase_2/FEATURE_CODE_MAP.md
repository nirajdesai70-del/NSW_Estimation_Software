# FEATURE_CODE_MAP — Phase 2

**Repository:** NSW_Estimation_Software  
**Source:** source_snapshot (controllers/services/models/views/js) + ROUTE_MAP  
**Purpose:** Feature/module → code files → UI assets → routes mapping  
**Status:** In Progress (First Pass - Evidence-Based)  
**Date:** 2025-12-17 (IST)

---

## Dashboard

### Controllers
- `App\Http\Controllers\HomeController`

### Models
- TBD (scan controller imports)

### Services
- TBD

### Views
- `resources/views/home.blade.php` (verify)
- `resources/views/home/index.blade.php` (TBD - verify)

### JS
- TBD

### Routes (from ROUTE_MAP)
- GET `/` (home)
- GET `/home` (home)

---

## Component/Item Master

### Controllers
- `CategoryController`
- `SubCategoryController`
- `ItemController`
- `AttributeController`
- `CategoryAttributeController`
- `MakeController`
- `SeriesController`
- `GenericController`
- `ProductController`
- `PriceController`
- `ImportController`
- `CatalogHealthController`
- `CatalogCleanupController`

### Models (from controller imports)
- `Category` (CategoryController)
- `SubCategory` (CategoryController, SubCategoryController)
- `Item` (CategoryController, ItemController)
- `Attribute` (CategoryController, AttributeController)
- `CategoryAttribute` (CategoryController, CategoryAttributeController)
- `Product` (CategoryController, ProductController)
- `Make` (MakeController)
- `Series` (SeriesController)
- `Generic` (GenericController)
- `Price` (PriceController)
- `TempProduct` (ImportController)
- TBD (additional models from other controllers)

### Services
- TBD (scanning controller imports)

### Views (verified from directory structure)
- `resources/views/category/` (index.blade.php, create.blade.php, edit.blade.php, addmore.blade.php)
- `resources/views/subcategory/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/item/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/attribute/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/category-attribute/` (assign-to-type.blade.php)
- `resources/views/make/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/series/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/generic/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/product/` (index.blade.php, create.blade.php, edit.blade.php, bom-list.blade.php, tempview.blade.php)
- `resources/views/price/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/import/` (product.blade.php)
- `resources/views/catalog-health/` (index.blade.php)
- `resources/views/catalog-cleanup/` (index.blade.php)

### JS
- `public/js/component-item-master/*` (TBD - verify)
- `resources/js/component-item-master/*` (TBD - verify)

### Routes (from ROUTE_MAP)
- `category.*`, `subcategory.*`, `item.*` (product-type), `make.*`, `series.*`, `attribute.*`, `category-attribute.*`, `generic.*`, `product.*`, `price.*`, `import.*`, `catalog-health.*`, `catalog-cleanup.*`

### Cross-Module Touchpoints
- Used by Quotation (via AJAX endpoints: `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`)
- Used by Master BOM (item/product lookups)

---

## Quotation

### Sub-areas
- **Legacy:** Original quotation workflow
- **V2:** Panel → Feeder → BOM hierarchy
- **Discount Rules:** Discount rule management and application
- **Reports:** PDF/Excel exports
- **Shared APIs:** Legacy+V2 dropdown endpoints

### Controllers
- `QuotationController` (Legacy)
- `QuotationV2Controller` (V2)
- `QuotationDiscountRuleController`
- `QuotationDiscountRuleTestController`
- `ReuseController`

### Models (from controller imports)
- `Quotation` (QuotationController, QuotationV2Controller)
- `QuotationSale` (QuotationV2Controller)
- `QuotationSaleBom` (QuotationV2Controller)
- `QuotationSaleBomItem` (QuotationV2Controller)
- `QuotationDiscountRule` (QuotationDiscountRuleController)
- `PricingAuditLog` (QuotationV2Controller)
- `Client` (QuotationController, QuotationV2Controller)
- `Project` (QuotationV2Controller)
- TBD (additional models)

### Services (from controller imports)
- `QuotationQuantityService` (QuotationV2Controller)
- `CostingService` (QuotationV2Controller)
- `DiscountRuleApplyService` (QuotationDiscountRuleController)
- `QuotationDiscountRuleService` (QuotationDiscountRuleController)
- TBD (additional services)

### Views (verified from directory structure)
- `resources/views/quotation/` (Legacy)
  - `index.blade.php`
  - `create.blade.php`
  - `edit.blade.php`
  - `bom-list.blade.php`
  - `step.blade.php`
  - `pdf.blade.php`
  - `audit-logs.blade.php`
  - Additional legacy views (item.blade.php, line.blade.php, etc.)
- `resources/views/quotation/v2/` (V2)
  - `index.blade.php`
  - `panel.blade.php`
  - `masterbom.blade.php`
  - `_bom.blade.php`
  - `_feeder.blade.php`
  - `_items_table.blade.php`
  - `_masterbom_modal.blade.php`
  - `_feeder_library_modal.blade.php`
  - `_reuse_filter_modal.blade.php`
  - Additional V2 partials/modals
- `resources/views/quotation/discount-rules/` (TBD - verify if exists)

### JS
- `public/js/quotation/*` (TBD - verify)
- `resources/js/quotation/*` (TBD - verify)

### Routes (from ROUTE_MAP)
- `quotation.*` (Legacy)
- `quotation.v2.*` (V2)
- `quotation.discount-rules.*`
- `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.makes` (Shared APIs)
- `api.reuse.*` (Reuse search)
- `reuse.*` (Reuse apply)

### Cross-Module Touchpoints

#### Master BOM Integration
- **Route:** `quotation.v2.applyMasterBom` → `QuotationV2Controller@applyMasterBom`
- **Touchpoint:** Master BOM module
- **Purpose:** Apply Master BOM template to Quotation V2

#### Feeder Library Integration
- **Route:** `quotation.v2.applyFeederTemplate` → `QuotationV2Controller@applyFeederTemplate`
- **Touchpoint:** Feeder Library module
- **Purpose:** Apply Feeder template to Quotation V2 panel

#### Proposal BOM Integration
- **Route:** `quotation.v2.applyProposalBom` → `QuotationV2Controller@applyProposalBom`
- **Touchpoint:** Proposal BOM module
- **Purpose:** Apply Proposal BOM to Quotation V2

#### Reuse Search Endpoints
- **Routes:** `api.reuse.panels`, `api.reuse.feeders`, `api.reuse.masterBoms`, `api.reuse.proposalBoms`
- **Touchpoint:** Quotation V2 (panels/feeders), Master BOM, Proposal BOM
- **Purpose:** Search and reuse existing panels, feeders, Master BOMs, Proposal BOMs

#### Component/Item Master Integration
- **Routes:** `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.makes`
- **Touchpoint:** Component/Item Master module
- **Purpose:** AJAX lookups for category/subcategory/item/product/make/series (supports both Legacy and V2)

---

## Master BOM

### Controllers
- `MasterBomController`

### Models (from controller imports)
- `MasterBom` (inferred from MasterBomController)
- `MasterBomItem` (inferred from routes)
- TBD (scan controller imports)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/masterbom/` (index.blade.php, create.blade.php, edit.blade.php, addmore.blade.php, copy.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `masterbom.*`

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-master-bom route)
- Uses Component/Item Master (item/product lookups via AJAX)

---

## Feeder Library

### Controllers
- `FeederTemplateController`

### Models
- TBD (scan controller imports)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/feeder-library/` (index.blade.php, create.blade.php, edit.blade.php, show.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `feeder-library.*`

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-feeder-template route)
- Uses Master BOM concepts (structure integration)

---

## Proposal BOM

### Controllers
- `ProposalBomController`

### Models
- TBD (scan controller imports)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/proposal-bom/` (index.blade.php, show.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `proposal-bom.*`
- **Note:** Routes likely incomplete; cross-check with controllers and route files. Additional routes likely under Quotation V2 apply endpoints (`quotation.v2.applyProposalBom`) and search APIs (`api.reuse.proposalBoms`).

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-proposal-bom route, search APIs)
- Can be promoted to Master BOM (promote route)
- Uses Master BOM concepts (structure)

---

## Project

### Controllers
- `ProjectController`
- `ClientController`
- `ContactController`

### Models (from controller imports)
- `Project` (inferred from ProjectController)
- `Client` (inferred from ClientController, also used by Quotation controllers)
- `Contact` (inferred from ContactController)
- `State` (ClientController - getState route)
- TBD (additional models)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/project/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/client/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/contact/` (index.blade.php, create.blade.php, edit.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `project.*`
- `client.*`
- `contact.*`

### Cross-Module Touchpoints
- Links to Quotation (project-quotation relationship via Quotation model)
- Client/Contact masters used by Project/Quotation

---

## Master

### Controllers
- `OrganizationController`
- `VendorController`
- `ImportController` (pdfcontain methods only - note: controller name is misleading, feature is Master/PDF container)

### Models (from controller imports)
- `Organization` (inferred from OrganizationController)
- `Vendor` (inferred from VendorController)
- TBD (PDF container model)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/organization/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/vendor/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/pdfcontain/` (index.blade.php)

### JS
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

## Employee/Role

### Controllers
- `UserController`
- `RoleController`

### Models (from controller imports)
- `User` (inferred from UserController)
- `Role` (inferred from RoleController)
- TBD (scan controller imports)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/user/` (index.blade.php, create.blade.php, edit.blade.php)
- `resources/views/role/` (index.blade.php, create.blade.php, edit.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `user.*`
- `role.*`

### Cross-Module Touchpoints
- Used by all modules (authentication/authorization via middleware)
- Security policies apply system-wide

---

## Security Module (Cross-Cutting)

### Controllers
- TBD (Security handled via middleware: `auth`, `throttle`, CSRF, etc.)

### Models
- TBD

### Services
- TBD

### Views
- TBD

### JS
- TBD

### Routes (from ROUTE_MAP)
- No direct routes (handled via middleware: `auth`, `throttle:search`, `throttle:autosave`, `throttle:critical-write`, etc.)

### Cross-Module Touchpoints
- Applies to all modules (authentication, authorization, CSRF, SQL injection, XSS protection)

---

## Shared/Ops

### Controllers / Closures
- `CronController@mySQLDownload`
- `/clear` (Closure - maintenance route; verify if enabled in production)

### Models
- TBD

### Services
- TBD

### Views
- TBD

### JS
- TBD

### Routes (from ROUTE_MAP)
- `mySQLDownload`
- `clear` (Maintenance route; verify if enabled in production)

### Cross-Module Touchpoints
- Maintenance operations affecting all modules

---

## Next Steps

1. **Complete Model Discovery:** Scan all controller imports to identify all models
2. **Complete Service Discovery:** Identify all service classes and their usage
3. **Verify View Structure:** Confirm all view file locations and naming
4. **Map JS Files:** Identify JavaScript files per module from `public/js/` and `resources/js/`
5. **Complete Cross-Module Touchpoints:** Document all inter-module dependencies
6. **Generate FILE_OWNERSHIP:** Mark protected/core files

---

**Last Updated:** 2025-12-17 (IST)  
**Status:** First Pass Complete (Evidence-Based - Models/Services from controller imports, Views from directory structure)
