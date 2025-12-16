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

### Models (from controller imports)
- `Quotation` (HomeController)
- `QuotationSale` (HomeController)
- `Client` (HomeController)

### Services
- TBD

### Views
- `resources/views/home.blade.php` (verified from HomeController@index: `view('home')`)
- Note: `resources/views/home/index.blade.php` does not exist

### JS
- TBD

### Routes (from ROUTE_MAP)
- GET `/` (home)
- GET `/home` (home)

### Database Touchpoints
- `quotations` (via Quotation model)
- `quotation_sales` (via QuotationSale model)
- `clients` (via Client model)

---

## Component/Item Master

### Controllers
- `CategoryController`
- `SubCategoryController`
- `ItemController`
- `AttributeController`
- `CategoryAttributeController`
- `ProductAttributeController`
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
- `Attribute` (CategoryController, AttributeController, ImportController)
- `AttributeTemp` (ImportController)
- `CategoryAttribute` (CategoryController, CategoryAttributeController, ImportController)
- `CategoryAttributeTemp` (ImportController)
- `Product` (CategoryController, ProductController, ImportController)
- `ProductAttribute` (ImportController)
- `ProductAttributeTemp` (ImportController)
- `Make` (MakeController, ImportController)
- `MakeCategory` (ImportController)
- `Series` (SeriesController, ImportController)
- `SeriesCategory` (ImportController)
- `SeriesMake` (ImportController)
- `Generic` (GenericController)
- `Price` (PriceController, ImportController)
- `TempProduct` (ImportController)
- `MasterBom` (ImportController)
- `Setting` (ImportController)
- TBD (additional models from CatalogHealthController, CatalogCleanupController)

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
- `resources/views/import/product.blade.php` (used by ImportController@importview for `/import` route)
- `resources/views/product/tempview.blade.php` (used by ImportController@importtempview for `/importview/{uuid}` route)
- Note: No `import/index.blade.php` exists; import view is `import/product.blade.php`
- `resources/views/catalog-health/` (index.blade.php)
- `resources/views/catalog-cleanup/` (index.blade.php)

### JS
- `public/js/component-item-master/*` (TBD - verify)
- `resources/js/component-item-master/*` (TBD - verify)

### Routes (from ROUTE_MAP)
- `category.*`, `subcategory.*`, `item.*` (product-type), `make.*`, `series.*`, `attribute.*`, `category-attribute.*`, `generic.*`, `product.*`, `price.*`, `import.*`, `catalog-health.*`, `catalog-cleanup.*`

### Database Touchpoints
- `categories`
- `sub_categories`
- `items` (product_types)
- `attributes`
- `category_attributes`
- `product_attributes`
- `makes`
- `make_categories`
- `series`
- `series_categories`
- `series_makes`
- `products`
- `generic_products`
- `prices`
- `temp_products`
- `attribute_temps`
- `category_attribute_temps`
- `product_attribute_temps`

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

### Views (verified from directory structure and controller view calls)
- `resources/views/quotation/` (Legacy - verified from directory structure)
  - `index.blade.php`
  - `create.blade.php`
  - `edit.blade.php`
  - `bom-list.blade.php`
  - `step.blade.php`
  - `pdf.blade.php`
  - `audit-logs.blade.php`
  - Additional legacy views (item.blade.php, line.blade.php, make_series.blade.php, masterbom.blade.php, stepedit.blade.php, steppopup.blade.php, linepopup.blade.php, discount.blade.php)
- `resources/views/quotation/v2/` (V2 - verified from directory structure and QuotationV2Controller view calls)
  - `index.blade.php` (verified: `view('quotation.v2.index')`)
  - `panel.blade.php` (verified: `view('quotation.v2.panel')`)
  - `masterbom.blade.php`
  - `_bom.blade.php`
  - `_feeder.blade.php`
  - `_items_table.blade.php`
  - `_masterbom_modal.blade.php` (verified: `view('quotation.v2._masterbom_modal')`)
  - `_feeder_library_modal.blade.php`
  - `_reuse_filter_modal.blade.php`
  - Additional V2 partials/modals (_edit_panel_qty_modal.blade.php, _edit_feeder_qty_modal.blade.php, _edit_bom_qty_modal.blade.php, _global_bulk_edit_modal.blade.php, _multi_edit_modal.blade.php, _reuse_filter_modal_step.blade.php)
- `resources/views/quotation/v2/discount_rules/` (verified from QuotationDiscountRuleController view calls)
  - `index.blade.php` (verified: `view('quotation.v2.discount_rules.index')`)
  - `create.blade.php` (verified: `view('quotation.v2.discount_rules.create')`)
  - `show.blade.php` (verified: `view('quotation.v2.discount_rules.show')`)
  - `edit.blade.php` (verified: `view('quotation.v2.discount_rules.edit')`)

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

### Database Touchpoints
- `quotations`
- `quotation_sales`
- `quotation_sale_boms`
- `quotation_sale_bom_items`
- `quotation_discount_rules`
- `pricing_audit_logs`
- `clients`
- `projects`

---

## Master BOM

### Controllers
- `MasterBomController`

### Models (from controller imports)
- `Category` (MasterBomController)
- `Item` (MasterBomController)
- `MasterBom` (MasterBomController)
- `MasterBomItem` (MasterBomController)
- `Product` (MasterBomController)
- `QuotationSaleBom` (MasterBomController - reference-only import for compatibility/reuse; not a Master BOM table)
- `SubCategory` (MasterBomController)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/masterbom/` (index.blade.php, create.blade.php, edit.blade.php, addmore.blade.php, copy.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `masterbom.*`

### Database Touchpoints
- `master_boms`
- `master_bom_items`
- `categories`
- `sub_categories`
- `items`
- `products`
- `quotation_sale_boms` (for reference)

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-master-bom route)
- Uses Component/Item Master (item/product lookups via AJAX)

---

## Feeder Library

### Controllers
- `FeederTemplateController`

### Models (from controller imports)
- `MasterBom` (FeederTemplateController - uses MasterBom with TemplateType='FEEDER')

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/feeder-library/` (index.blade.php, create.blade.php, edit.blade.php, show.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `feeder-library.*`

### Database Touchpoints
- `master_boms` (with TemplateType='FEEDER')

### Cross-Module Touchpoints
- Used by Quotation V2 (apply-feeder-template route)
- Reuse/search endpoints touch this feature via Quotation reuse APIs (`api.reuse.feeders`)
- Uses Master BOM concepts (structure integration)

---

## Proposal BOM

### Controllers
- `ProposalBomController`

### Models (from controller imports)
- `QuotationSaleBom` (ProposalBomController - Proposal BOMs are stored in quotation_sale_boms table)

### Services
- TBD

### Views (verified from directory structure)
- `resources/views/proposal-bom/` (index.blade.php, show.blade.php)

### JS
- TBD

### Routes (from ROUTE_MAP)
- `proposal-bom.*`
- **Note:** Routes likely incomplete; cross-check with controllers and route files. Additional routes likely under Quotation V2 apply endpoints (`quotation.v2.applyProposalBom`) and search APIs (`api.reuse.proposalBoms`).

### Database Touchpoints
- `quotation_sale_boms` (Proposal BOMs stored here - verify discriminator fields used for Proposal BOM identification)

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
- `Project` (ProjectController)
- `Quotation` (ProjectController)
- `Client` (ProjectController, ClientController, also used by Quotation controllers)
- `Contact` (ContactController)
- `State` (ClientController - getState route)
- `Country` (ClientController)
- `Organization` (ClientController)

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

### Database Touchpoints
- `projects`
- `quotations`
- `clients`
- `contacts`
- `states`

### Cross-Module Touchpoints
- Links to Quotation (project-quotation relationship via Quotation model)
- Client/Contact masters used by Project/Quotation

---

## Master

### Controllers
- `OrganizationController`
- `VendorController`
- `ImportController` (pdfcontain methods only)
  - **Note:** Shared controller - also used by Component/Item Master Import routes. Controller name is misleading; pdfcontain feature is Master/PDF container, not Import.

### Models (from controller imports)
- `Organization` (OrganizationController)
- `Vendor` (VendorController)
- `Setting` (ImportController - pdfcontain uses Setting model)

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

### Database Touchpoints
- `organizations`
- `vendors`
- `settings` (PDF container configuration)

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
- `User` (UserController, RoleController)
- `Role` (UserController, RoleController)

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

### Database Touchpoints
- `users`
- `roles`

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

### Database Touchpoints
- TBD (maintenance operations may touch multiple tables)

### Cross-Module Touchpoints
- Maintenance operations affecting all modules

---

## Protected/Core Files (Do Not Refactor Casually)

These files contain critical business logic and must be protected during NSW refactoring:

### Quotation Module
- `source_snapshot/app/Services/QuotationQuantityService.php` - Core quantity calculation logic
- `source_snapshot/app/Services/CostingService.php` - Core costing calculations (SUM(AmountTotal) rule)
- `source_snapshot/app/Services/DiscountRuleApplyService.php` - Discount rule application logic
- `source_snapshot/app/Services/QuotationDiscountRuleService.php` - Discount rule business logic

### Component/Item Master Module
- `source_snapshot/app/Services/ProductAttributeService.php` - Product attribute management logic (if exists)
- `source_snapshot/app/Helpers/ProductHelper.php` - Product helper functions (if exists)

### General
- `source_snapshot/app/Services/DeletionPolicyService.php` - Deletion policy enforcement
- `source_snapshot/app/Services/AutoNamingService.php` - Auto-naming logic (if exists)

### Models (Core Business Objects - Protected)
- `source_snapshot/app/Models/Quotation.php` - Core quotation entity
- `source_snapshot/app/Models/QuotationSale.php` - Panel/Sale entity
- `source_snapshot/app/Models/QuotationSaleBom.php` - BOM entity
- `source_snapshot/app/Models/QuotationSaleBomItem.php` - BOM item entity
- `source_snapshot/app/Models/MasterBom.php` - Master BOM template entity
- `source_snapshot/app/Models/MasterBomItem.php` - Master BOM item entity
- `source_snapshot/app/Models/Category.php` - Category entity
- `source_snapshot/app/Models/Product.php` - Product entity
- `source_snapshot/app/Models/Project.php` - Project entity

**Note:** These files implement core business logic that must be preserved in NSW. Changes require careful review and testing.

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
