# FILE_OWNERSHIP — Phase 2

**Repository:** NSW_Estimation_Software  
**Purpose:** Assign module ownership + risk level to key code files for safe change control  
**Source:** source_snapshot/app + ROUTE_MAP + FEATURE_CODE_MAP  
**Status:** In Progress (First Pass)  
**Date:** 2025-12-17 (IST)

---

## Ownership Table

| File Path (source_snapshot/...) | Type | Owner Module | Sub-Area | Risk Level | Why it matters | Change Rule | Related Routes/Features |
|---|---|---|---|---|---|---|---|
| `app/Http/Controllers/HomeController.php` | Controller | Dashboard | Home | MEDIUM | Dashboard entry point | Normal testing | `home` (GET `/`, `/home`) |
| `app/Http/Controllers/CategoryController.php` | Controller | Component/Item Master | Category | MEDIUM | Category CRUD operations | Normal testing | `category.*` |
| `app/Http/Controllers/SubCategoryController.php` | Controller | Component/Item Master | Subcategory | MEDIUM | Subcategory CRUD operations | Normal testing | `subcategory.*` |
| `app/Http/Controllers/ItemController.php` | Controller | Component/Item Master | Product Type | MEDIUM | Product Type CRUD operations | Normal testing | `item.*` (product-type) |
| `app/Http/Controllers/AttributeController.php` | Controller | Component/Item Master | Attributes | MEDIUM | Attribute CRUD operations | Normal testing | `attribute.*` |
| `app/Http/Controllers/CategoryAttributeController.php` | Controller | Component/Item Master | Attributes | MEDIUM | Category-attribute assignment | Normal testing | `category-attribute.*` |
| `app/Http/Controllers/ProductAttributeController.php` | Controller | Component/Item Master | Attributes | MEDIUM | Product attribute management | Normal testing | TBD (verify routes) |
| `app/Http/Controllers/MakeController.php` | Controller | Component/Item Master | Make | MEDIUM | Make CRUD operations | Normal testing | `make.*` |
| `app/Http/Controllers/SeriesController.php` | Controller | Component/Item Master | Series | MEDIUM | Series CRUD operations | Normal testing | `series.*` |
| `app/Http/Controllers/GenericController.php` | Controller | Component/Item Master | Generic Product | MEDIUM | Generic product CRUD | Normal testing | `generic.*` |
| `app/Http/Controllers/ProductController.php` | Controller | Component/Item Master | Specific Product | MEDIUM | Specific product CRUD | Normal testing | `product.*` |
| `app/Http/Controllers/PriceController.php` | Controller | Component/Item Master | Price List | MEDIUM | Price list CRUD | Normal testing | `price.*` |
| `app/Http/Controllers/ImportController.php` | Controller | Component/Item Master + Master | Import/Export + PDF Formats | HIGH | Split ownership: Import routes (Component/Item Master) + pdfcontain (Master/PDF) | Review required | `import.*` (Component/Item Master), `pdfcontain.*` (Master) |
| `app/Http/Controllers/CatalogHealthController.php` | Controller | Component/Item Master | Catalog Health | MEDIUM | Catalog health monitoring | Normal testing | `catalog-health.*` |
| `app/Http/Controllers/CatalogCleanupController.php` | Controller | Component/Item Master | Catalog Cleanup | MEDIUM | Catalog cleanup operations | Normal testing | `catalog-cleanup.*` |
| `app/Http/Controllers/QuotationController.php` | Controller | Quotation | Legacy | HIGH | Legacy quotation workflow; widely used | Review required | `quotation.*` (Legacy), `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*` (Shared APIs) |
| `app/Http/Controllers/QuotationV2Controller.php` | Controller | Quotation | V2 | PROTECTED | Core V2 quotation logic; Panel/Feeder/BOM hierarchy | Review + regression test | `quotation.v2.*`, `reuse.*` |
| `app/Http/Controllers/QuotationDiscountRuleController.php` | Controller | Quotation | Discount Rules | HIGH | Discount rule management and application | Review required | `quotation.discount-rules.*` |
| `app/Http/Controllers/QuotationDiscountRuleTestController.php` | Controller | Quotation | Discount Rules | MEDIUM | Discount rule testing utilities | Normal testing | `discount-rules.test-*` |
| `app/Http/Controllers/ReuseController.php` | Controller | Quotation | V2 | MEDIUM | Reuse search endpoints | Normal testing | `api.reuse.*` |
| `app/Http/Controllers/MasterBomController.php` | Controller | Master BOM | Structure | HIGH | Master BOM CRUD; used by Quotation V2 | Review required | `masterbom.*` |
| `app/Http/Controllers/FeederTemplateController.php` | Controller | Feeder Library | Structure | HIGH | Feeder template CRUD; used by Quotation V2 | Review required | `feeder-library.*` |
| `app/Http/Controllers/ProposalBomController.php` | Controller | Proposal BOM | Structure | HIGH | Proposal BOM management; used by Quotation V2 | Review required | `proposal-bom.*` |
| `app/Http/Controllers/ProjectController.php` | Controller | Project | Structure | MEDIUM | Project CRUD operations | Normal testing | `project.*` |
| `app/Http/Controllers/ClientController.php` | Controller | Project | Clients | MEDIUM | Client CRUD; used by Project/Quotation | Normal testing | `client.*` |
| `app/Http/Controllers/ContactController.php` | Controller | Project | Contacts | MEDIUM | Contact CRUD; used by Project/Quotation | Normal testing | `contact.*` |
| `app/Http/Controllers/OrganizationController.php` | Controller | Master | Organization | MEDIUM | Organization CRUD; master data | Normal testing | `organization.*` |
| `app/Http/Controllers/VendorController.php` | Controller | Master | Vendor | MEDIUM | Vendor CRUD; master data | Normal testing | `vendor.*` |
| `app/Http/Controllers/UserController.php` | Controller | Employee/Role | Users | MEDIUM | User CRUD; authentication | Normal testing | `user.*` |
| `app/Http/Controllers/RoleController.php` | Controller | Employee/Role | Roles | MEDIUM | Role CRUD; authorization | Normal testing | `role.*` |
| `app/Http/Controllers/CronController.php` | Controller | Shared/Ops | Maintenance | LOW | Maintenance operations | Normal testing | `mySQLDownload` |
| `app/Services/QuotationQuantityService.php` | Service | Quotation | V2 | PROTECTED | Core quantity calculation logic; used by CostingService | Review + regression test | Quotation V2 quantity updates |
| `app/Services/CostingService.php` | Service | Quotation | V2 | PROTECTED | Core costing calculations (SUM(AmountTotal) rule); critical business logic | Review + regression test | Quotation V2 costing, panel/feeder/BOM cost roll-up |
| `app/Services/DiscountRuleApplyService.php` | Service | Quotation | Discount Rules | PROTECTED | Discount rule application logic | Review + regression test | `quotation.discount-rules.apply` |
| `app/Services/QuotationDiscountRuleService.php` | Service | Quotation | Discount Rules | PROTECTED | Discount rule business logic | Review + regression test | `quotation.discount-rules.*` |
| `app/Services/DeletionPolicyService.php` | Service | Shared | General | PROTECTED | Deletion policy enforcement; prevents data loss | Review + regression test | Used by QuotationController |
| `app/Models/Quotation.php` | Model | Quotation | Core | PROTECTED | Core quotation entity; central to system | Review + regression test | All quotation routes |
| `app/Models/QuotationSale.php` | Model | Quotation | V2 | PROTECTED | Panel/Sale entity; V2 hierarchy root | Review + regression test | Quotation V2 panel operations |
| `app/Models/QuotationSaleBom.php` | Model | Quotation | V2 | PROTECTED | BOM entity; V2 hierarchy component | Review + regression test | Quotation V2 BOM operations, Proposal BOM |
| `app/Models/QuotationSaleBomItem.php` | Model | Quotation | V2 | PROTECTED | BOM item entity; V2 hierarchy leaf | Review + regression test | Quotation V2 item operations |
| `app/Models/MasterBom.php` | Model | Master BOM | Core | PROTECTED | Master BOM template entity; reusable templates | Review + regression test | Master BOM routes, Quotation V2 apply-master-bom |
| `app/Models/MasterBomItem.php` | Model | Master BOM | Core | PROTECTED | Master BOM item entity | Review + regression test | Master BOM routes |
| `app/Models/Category.php` | Model | Component/Item Master | Core | HIGH | Category entity; widely referenced | Review required | Category routes, used by Quotation APIs |
| `app/Models/Product.php` | Model | Component/Item Master | Core | HIGH | Product entity; widely referenced | Review required | Product routes, used by Quotation APIs |
| `app/Models/Project.php` | Model | Project | Core | HIGH | Project entity; links to quotations | Review required | Project routes, used by Quotation |

---

## Risk Levels

- **PROTECTED:** Core business logic; changes require review + regression test
- **HIGH:** Widely used; changes can break multiple modules
- **MEDIUM:** Module-scoped; normal testing
- **LOW:** Isolated; minimal risk

---

## Notes

### Split Ownership Files

- **ImportController:** Split between Component/Item Master (import routes) and Master (pdfcontain routes). Changes require coordination.

### Cross-Module Dependencies

- **QuotationV2Controller:** Uses Master BOM, Feeder Library, Proposal BOM via apply routes
- **QuotationController:** Uses Component/Item Master via AJAX endpoints
- **ClientController/ContactController:** Used by both Project and Quotation modules

### Protected Services

- **CostingService:** Implements critical SUM(AmountTotal) rule. Any changes must preserve this business rule.
- **QuotationQuantityService:** Used by CostingService. Changes must maintain consistency.

---

**Last Updated:** 2025-12-17 (IST)  
**Status:** First Pass Complete (50 rows - Controllers + Protected Services/Models)

