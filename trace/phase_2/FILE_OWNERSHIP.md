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
| `source_snapshot/app/Http/Controllers/HomeController.php` | Controller | Dashboard | Home | MEDIUM | Dashboard entry point; cross-module dashboard counts (queries Quotation/Client) | Normal testing | `home` (GET `/`, `/home`) |
| `source_snapshot/app/Http/Controllers/CategoryController.php` | Controller | Component/Item Master | Category | MEDIUM | Category CRUD operations | Normal testing | `category.*` |
| `source_snapshot/app/Http/Controllers/SubCategoryController.php` | Controller | Component/Item Master | Subcategory | MEDIUM | Subcategory CRUD operations | Normal testing | `subcategory.*` |
| `source_snapshot/app/Http/Controllers/ItemController.php` | Controller | Component/Item Master | Product Type | MEDIUM | Product Type CRUD operations | Normal testing | `item.*` (product-type) |
| `source_snapshot/app/Http/Controllers/AttributeController.php` | Controller | Component/Item Master | Attributes | MEDIUM | Attribute CRUD operations | Normal testing | `attribute.*` |
| `source_snapshot/app/Http/Controllers/CategoryAttributeController.php` | Controller | Component/Item Master | Attributes (Type Mapping) | HIGH | Type↔attribute mapping affects product validity; cascades into product creation + imports | Review + regression on product creation + imports | `category-attribute.*` |
| `source_snapshot/app/Http/Controllers/ProductAttributeController.php` | Controller | Component/Item Master | Attributes | MEDIUM | Product attribute management | Normal testing | No direct routes found in ROUTE_MAP (verify web.php). Used by Import flows. |
| `source_snapshot/app/Http/Controllers/MakeController.php` | Controller | Component/Item Master | Make | MEDIUM | Make CRUD operations | Normal testing | `make.*` |
| `source_snapshot/app/Http/Controllers/SeriesController.php` | Controller | Component/Item Master | Series | MEDIUM | Series CRUD operations | Normal testing | `series.*` |
| `source_snapshot/app/Http/Controllers/GenericController.php` | Controller | Component/Item Master | Generic Product | MEDIUM | Generic product CRUD | Normal testing | `generic.*` |
| `source_snapshot/app/Http/Controllers/ProductController.php` | Controller | Component/Item Master | Specific Product | MEDIUM | Specific product CRUD | Normal testing | `product.*` |
| `source_snapshot/app/Http/Controllers/PriceController.php` | Controller | Component/Item Master | Price List | HIGH | Price affects quotation costing, discounts, and audits | Review + sample quotation + discount check | `price.*` |
| `source_snapshot/app/Http/Controllers/ImportController.php` | Controller | Component/Item Master + Master | Import/Export + PDF Formats | HIGH | Split ownership: Import routes (Component/Item Master) + pdfcontain (Master/PDF); touches settings table (pdfcontain) | Review required | `import.*` (Component/Item Master), `pdfcontain.*` (Master) |
| `source_snapshot/app/Http/Controllers/CatalogHealthController.php` | Controller | Component/Item Master | Catalog Health | MEDIUM | Catalog health monitoring | Normal testing | `catalog-health.*` |
| `source_snapshot/app/Http/Controllers/CatalogCleanupController.php` | Controller | Component/Item Master | Catalog Cleanup | HIGH | Catalog cleanup operations; data mutation risk | Review + backup + controlled test | `catalog-cleanup.*` |
| `source_snapshot/app/Http/Controllers/QuotationController.php` | Controller | Quotation | Legacy | HIGH | Legacy quotation workflow; widely used | Review required | `quotation.*` (Legacy), `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*` (Shared APIs) |
| `source_snapshot/app/Http/Controllers/QuotationV2Controller.php` | Controller | Quotation | V2 | PROTECTED | Core V2 quotation logic; Panel/Feeder/BOM hierarchy | Review + regression test | `quotation.v2.*`, `reuse.*`, `quotation.v2.applyMasterBom`, `quotation.v2.applyFeederTemplate`, `quotation.v2.applyProposalBom` |
| `source_snapshot/app/Http/Controllers/QuotationDiscountRuleController.php` | Controller | Quotation | Discount Rules | HIGH | Discount rule management and application | Review required | `quotation.discount-rules.*` |
| `source_snapshot/app/Http/Controllers/QuotationDiscountRuleTestController.php` | Controller | Quotation | Discount Rules | MEDIUM | Discount rule testing utilities | Normal testing | `discount-rules.test-*` |
| `source_snapshot/app/Http/Controllers/ReuseController.php` | Controller | Quotation | V2 | HIGH | Reuse search endpoints; cross-module + search perf sensitive | Review + perf testing | `api.reuse.*` |
| `source_snapshot/app/Http/Controllers/MasterBomController.php` | Controller | Master BOM | Structure | HIGH | Master BOM CRUD; used by Quotation V2 | Review required | `masterbom.*` |
| `source_snapshot/app/Http/Controllers/FeederTemplateController.php` | Controller | Feeder Library | Structure | HIGH | Feeder template CRUD; used by Quotation V2 | Review required | `feeder-library.*` |
| `source_snapshot/app/Http/Controllers/ProposalBomController.php` | Controller | Proposal BOM | Structure | HIGH | Proposal BOM management; used by Quotation V2 | Review required | `proposal-bom.*` |
| `source_snapshot/app/Http/Controllers/ProjectController.php` | Controller | Project | Structure | MEDIUM | Project CRUD operations | Normal testing | `project.*` |
| `source_snapshot/app/Http/Controllers/ClientController.php` | Controller | Project | Clients | MEDIUM | Client CRUD; used by Project/Quotation | Normal testing | `client.*` |
| `source_snapshot/app/Http/Controllers/ContactController.php` | Controller | Project | Contacts | MEDIUM | Contact CRUD; used by Project/Quotation | Normal testing | `contact.*` |
| `source_snapshot/app/Http/Controllers/OrganizationController.php` | Controller | Master | Organization | MEDIUM | Organization CRUD; master data | Normal testing | `organization.*` |
| `source_snapshot/app/Http/Controllers/VendorController.php` | Controller | Master | Vendor | MEDIUM | Vendor CRUD; master data | Normal testing | `vendor.*` |
| `source_snapshot/app/Http/Controllers/UserController.php` | Controller | Employee/Role | Users | MEDIUM | User CRUD; authentication | Normal testing | `user.*` |
| `source_snapshot/app/Http/Controllers/RoleController.php` | Controller | Employee/Role | Roles | MEDIUM | Role CRUD; authorization | Normal testing | `role.*` |
| `source_snapshot/app/Http/Controllers/CronController.php` | Controller | Shared/Ops | Maintenance | HIGH | Operational DB dump/export | Restrict access + verify production enablement | `mySQLDownload` |
| `source_snapshot/routes/web.php` | Route File | Shared/Ops | Maintenance | HIGH | Contains maintenance closure routes (e.g., `/clear`) | Review + verify production enablement | `/clear` (Closure) |
| `source_snapshot/routes/api.php` | Route File | Quotation | Shared APIs | HIGH | Contains throttled search APIs used by Quotation (Legacy+V2) | Review + verify throttling | `api.category.*`, `api.item.*`, `api.product.*`, `api.make.*`, `api.reuse.*` |
| `source_snapshot/app/Services/QuotationQuantityService.php` | Service | Quotation | V2 | PROTECTED | Core quantity calculation logic; used by CostingService | Review + regression test | Quotation V2 quantity updates |
| `source_snapshot/app/Services/CostingService.php` | Service | Quotation | V2 | PROTECTED | Core costing calculations (SUM(AmountTotal) rule); critical business logic | Review + regression test | Quotation V2 costing, panel/feeder/BOM cost roll-up |
| `source_snapshot/app/Services/DiscountRuleApplyService.php` | Service | Quotation | Discount Rules | PROTECTED | Discount rule application logic | Review + regression test | `quotation.discount-rules.apply` |
| `source_snapshot/app/Services/QuotationDiscountRuleService.php` | Service | Quotation | Discount Rules | PROTECTED | Discount rule business logic | Review + regression test | `quotation.discount-rules.*` |
| `source_snapshot/app/Services/DeletionPolicyService.php` | Service | Shared | General | PROTECTED | Deletion policy enforcement; prevents data loss | Review + regression test | Used by QuotationController |
| `source_snapshot/app/Models/Quotation.php` | Model | Quotation | Core | PROTECTED | Core quotation entity; central to system | Review + regression test | All quotation routes |
| `source_snapshot/app/Models/QuotationSale.php` | Model | Quotation | V2 | PROTECTED | Panel/Sale entity; V2 hierarchy root | Review + regression test | Quotation V2 panel operations |
| `source_snapshot/app/Models/QuotationSaleBom.php` | Model | Quotation | V2 | PROTECTED | BOM entity; V2 hierarchy component | Review + regression test | Quotation V2 BOM operations, Proposal BOM |
| `source_snapshot/app/Models/QuotationSaleBomItem.php` | Model | Quotation | V2 | PROTECTED | BOM item entity; V2 hierarchy leaf | Review + regression test | Quotation V2 item operations |
| `source_snapshot/app/Models/MasterBom.php` | Model | Master BOM | Core | PROTECTED | Master BOM template entity; reusable templates | Review + regression test | Master BOM routes, Quotation V2 apply-master-bom |
| `source_snapshot/app/Models/MasterBomItem.php` | Model | Master BOM | Core | PROTECTED | Master BOM item entity | Review + regression test | Master BOM routes |
| `source_snapshot/app/Models/Category.php` | Model | Component/Item Master | Core | HIGH | Category entity; widely referenced | Review required | Category routes, used by Quotation APIs |
| `source_snapshot/app/Models/Product.php` | Model | Component/Item Master | Core | HIGH | Product entity; widely referenced | Review required | Product routes, used by Quotation APIs |
| `source_snapshot/app/Models/Project.php` | Model | Project | Core | HIGH | Project entity; links to quotations | Review required | Project routes, used by Quotation |

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

