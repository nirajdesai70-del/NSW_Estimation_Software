# ROUTE_MAP — Phase 2

**Repository:** NSW_Estimation_Software  
**Source:** source_snapshot/routes/web.php + routes/api.php  
**Purpose:** Route → Controller@Method → Module ownership mapping  
**Status:** In Progress (First Pass - ~80% coverage)  
**Date:** 2025-12-17 (IST)

---

## Route Map Table

| Method | URI | Route Name | Middleware/Auth | Controller@Method | Module | Sub-Area | Cross-Module Touchpoints | Views/JS (if known) | Notes |
|---|---|---|---|---|---|---|---|---|---|
| GET | / | home | auth | HomeController@index | Dashboard | Home | - | home/index.blade.php | Home page |
| GET | /home | home | auth | HomeController@index | Dashboard | Home | - | home/index.blade.php | Home page alias |
| GET | /api/category/{categoryId}/subcategories | api.category.subcategories | auth, throttle:search | QuotationController@getSubCategories | Quotation | Shared (Legacy+V2) | Component/Item Master | - | AJAX endpoint - supports both Legacy and V2 |
| GET | /api/category/{categoryId}/items | api.category.items | auth, throttle:search | QuotationController@getItems | Quotation | Shared (Legacy+V2) | Component/Item Master | - | AJAX endpoint - supports both Legacy and V2 |
| GET | /api/category/{categoryId}/products | api.category.products | auth, throttle:search | QuotationController@getProducts | Quotation | Shared (Legacy+V2) | Component/Item Master | - | AJAX endpoint - supports both Legacy and V2 |
| GET | /api/item/{itemId}/products | api.item.products | auth, throttle:search | QuotationController@getProductsByItem | Quotation | Shared (Legacy+V2) | Component/Item Master | - | Type-first filtering - supports both Legacy and V2 |
| GET | /api/product/{productId}/makes | api.product.makes | auth, throttle:search | QuotationController@getMakes | Quotation | Shared (Legacy+V2) | Component/Item Master | - | AJAX endpoint - supports both Legacy and V2 |
| GET | /api/make/{makeId}/series | api.make.series | auth, throttle:search | QuotationController@getSeriesApi | Quotation | Shared (Legacy+V2) | Component/Item Master | - | AJAX endpoint - supports both Legacy and V2 |
| GET | /api/product/{productId}/descriptions | api.product.descriptions | auth, throttle:search | QuotationController@getDescriptions | Quotation | Shared (Legacy+V2) | Component/Item Master | - | AJAX endpoint - supports both Legacy and V2 |
| GET | /api/category/{categoryId}/makes | api.category.makes | auth, throttle:search | QuotationController@getMakesByCategory | Quotation | Shared (Legacy+V2) | Component/Item Master | - | Bulk edit - supports both Legacy and V2 |
| GET | /api/makes | api.makes | auth, throttle:search | QuotationController@getAllMakes | Quotation | Shared (Legacy+V2) | Component/Item Master | - | Fallback - supports both Legacy and V2 |
| GET | /role | role.index | auth | RoleController@index | Employee/Role | Roles | - | role/index.blade.php | Role list |
| GET | /role/create | role.create | auth | RoleController@create | Employee/Role | Roles | - | role/create.blade.php | Create role |
| POST | /role/create | role.store | auth | RoleController@store | Employee/Role | Roles | - | - | Store role |
| GET | /role/{id}/edit | role.edit | auth | RoleController@edit | Employee/Role | Roles | - | role/edit.blade.php | Edit role |
| PUT | /role/{id}/edit | role.update | auth | RoleController@update | Employee/Role | Roles | - | - | Update role |
| DELETE | /role/{id}/destroy | role.destroy | auth | RoleController@destroy | Employee/Role | Roles | - | - | Delete role |
| GET | /user | user.index | auth | UserController@index | Employee/Role | Users | - | user/index.blade.php | User list |
| GET | /user/create | user.create | auth | UserController@create | Employee/Role | Users | - | user/create.blade.php | Create user |
| POST | /user/create | user.store | auth | UserController@store | Employee/Role | Users | - | - | Store user |
| GET | /user/{id}/edit | user.edit | auth | UserController@edit | Employee/Role | Users | - | user/edit.blade.php | Edit user |
| PUT | /user/{id}/edit | user.update | auth | UserController@update | Employee/Role | Users | - | - | Update user |
| DELETE | /user/{id}/destroy | user.destroy | auth | UserController@destroy | Employee/Role | Users | - | - | Delete user |
| GET | /client | client.index | auth | ClientController@index | Project | Clients | - | client/index.blade.php | Client list - Client master used by Project/Quotation |
| GET | /client/create | client.create | auth | ClientController@create | Project | Clients | - | client/create.blade.php | Create client - Client master used by Project/Quotation |
| POST | /client/create | client.store | auth | ClientController@store | Project | Clients | - | - | Store client - Client master used by Project/Quotation |
| GET | /client/{id}/edit | client.edit | auth | ClientController@edit | Project | Clients | - | client/edit.blade.php | Edit client - Client master used by Project/Quotation |
| PUT | /client/{id}/edit | client.update | auth | ClientController@update | Project | Clients | - | - | Update client - Client master used by Project/Quotation |
| DELETE | /client/{id}/destroy | client.destroy | auth | ClientController@destroy | Project | Clients | - | - | Delete client - Client master used by Project/Quotation |
| GET | /client/{id}/getState | client.getState | auth | ClientController@getState | Project | Clients | - | - | AJAX state lookup - Client master used by Project/Quotation |
| GET | /organization | organization.index | auth | OrganizationController@index | Master | Organization | - | organization/index.blade.php | Org list |
| GET | /organization/create | organization.create | auth | OrganizationController@create | Master | Organization | - | organization/create.blade.php | Create org |
| POST | /organization/create | organization.store | auth | OrganizationController@store | Master | Organization | - | - | Store org |
| GET | /organization/{id}/edit | organization.edit | auth | OrganizationController@edit | Master | Organization | - | organization/edit.blade.php | Edit org |
| PUT | /organization/{id}/edit | organization.update | auth | OrganizationController@update | Master | Organization | - | - | Update org |
| DELETE | /organization/{id}/destroy | organization.destroy | auth | OrganizationController@destroy | Master | Organization | - | - | Delete org |
| GET | /contact | contact.index | auth | ContactController@index | Project | Contacts | - | contact/index.blade.php | Contact list - Contact master used by Project/Quotation |
| GET | /contact/create | contact.create | auth | ContactController@create | Project | Contacts | - | contact/create.blade.php | Create contact - Contact master used by Project/Quotation |
| POST | /contact/create | contact.store | auth | ContactController@store | Project | Contacts | - | - | Store contact - Contact master used by Project/Quotation |
| GET | /contact/{id}/edit | contact.edit | auth | ContactController@edit | Project | Contacts | - | contact/edit.blade.php | Edit contact - Contact master used by Project/Quotation |
| PUT | /contact/{id}/edit | contact.update | auth | ContactController@update | Project | Contacts | - | - | Update contact - Contact master used by Project/Quotation |
| DELETE | /contact/{id}/destroy | contact.destroy | auth | ContactController@destroy | Project | Contacts | - | - | Delete contact - Contact master used by Project/Quotation |
| GET | /category | category.index | auth | CategoryController@index | Component/Item Master | Category | - | category/index.blade.php | Category list |
| GET | /category/create | category.create | auth | CategoryController@create | Component/Item Master | Category | - | category/create.blade.php | Create category |
| POST | /category/create | category.store | auth | CategoryController@store | Component/Item Master | Category | - | - | Store category |
| GET | /category/addmore | category.addmore | auth | CategoryController@addmore | Component/Item Master | Category | - | category/addmore.blade.php | Add more |
| GET | /category/{id}/edit | category.edit | auth | CategoryController@edit | Component/Item Master | Category | - | category/edit.blade.php | Edit category |
| PUT | /category/{id}/edit | category.update | auth | CategoryController@update | Component/Item Master | Category | - | - | Update category |
| DELETE | /category/{id}/destroy | category.destroy | auth | CategoryController@destroy | Component/Item Master | Category | - | - | Delete category |
| GET | /subcategory | subcategory.index | auth | SubCategoryController@index | Component/Item Master | Subcategory | - | subcategory/index.blade.php | Subcategory list |
| GET | /subcategory/create | subcategory.create | auth | SubCategoryController@create | Component/Item Master | Subcategory | - | subcategory/create.blade.php | Create subcategory |
| POST | /subcategory/create | subcategory.store | auth | SubCategoryController@store | Component/Item Master | Subcategory | - | - | Store subcategory |
| GET | /subcategory/{id}/edit | subcategory.edit | auth | SubCategoryController@edit | Component/Item Master | Subcategory | - | subcategory/edit.blade.php | Edit subcategory |
| PUT | /subcategory/{id}/edit | subcategory.update | auth | SubCategoryController@update | Component/Item Master | Subcategory | - | - | Update subcategory |
| DELETE | /subcategory/{id}/destroy | subcategory.destroy | auth | SubCategoryController@destroy | Component/Item Master | Subcategory | - | - | Delete subcategory |
| GET | /product-type | item.index | auth | ItemController@index | Component/Item Master | Product Type | - | item/index.blade.php | Product type list |
| GET | /product-type/create | item.create | auth | ItemController@create | Component/Item Master | Product Type | - | item/create.blade.php | Create product type |
| POST | /product-type/create | item.store | auth | ItemController@store | Component/Item Master | Product Type | - | - | Store product type |
| GET | /product-type/{id}/edit | item.edit | auth | ItemController@edit | Component/Item Master | Product Type | - | item/edit.blade.php | Edit product type |
| PUT | /product-type/{id}/edit | item.update | auth | ItemController@update | Component/Item Master | Product Type | - | - | Update product type |
| DELETE | /product-type/{id}/destroy | item.destroy | auth | ItemController@destroy | Component/Item Master | Product Type | - | - | Delete product type |
| GET | /make | make.index | auth | MakeController@index | Component/Item Master | Make | - | make/index.blade.php | Make list |
| GET | /make/create | make.create | auth | MakeController@create | Component/Item Master | Make | - | make/create.blade.php | Create make |
| POST | /make/create | make.store | auth | MakeController@store | Component/Item Master | Make | - | - | Store make |
| GET | /make/{id}/edit | make.edit | auth | MakeController@edit | Component/Item Master | Make | - | make/edit.blade.php | Edit make |
| PUT | /make/{id}/edit | make.update | auth | MakeController@update | Component/Item Master | Make | - | - | Update make |
| DELETE | /make/{id}/destroy | make.destroy | auth | MakeController@destroy | Component/Item Master | Make | - | - | Delete make |
| GET | /series | series.index | auth | SeriesController@index | Component/Item Master | Series | - | series/index.blade.php | Series list |
| GET | /series/create | series.create | auth | SeriesController@create | Component/Item Master | Series | - | series/create.blade.php | Create series |
| POST | /series/create | series.store | auth | SeriesController@store | Component/Item Master | Series | - | - | Store series |
| GET | /series/{id}/edit | series.edit | auth | SeriesController@edit | Component/Item Master | Series | - | series/edit.blade.php | Edit series |
| PUT | /series/{id}/edit | series.update | auth | SeriesController@update | Component/Item Master | Series | - | - | Update series |
| DELETE | /series/{id}/destroy | series.destroy | auth | SeriesController@destroy | Component/Item Master | Series | - | - | Delete series |
| GET | /attribute | attribute.index | auth | AttributeController@index | Component/Item Master | Attributes | - | attribute/index.blade.php | Attribute list |
| GET | /attribute/create | attribute.create | auth | AttributeController@create | Component/Item Master | Attributes | - | attribute/create.blade.php | Create attribute |
| POST | /attribute/create | attribute.store | auth | AttributeController@store | Component/Item Master | Attributes | - | - | Store attribute |
| GET | /attribute/{id}/edit | attribute.edit | auth | AttributeController@edit | Component/Item Master | Attributes | - | attribute/edit.blade.php | Edit attribute |
| PUT | /attribute/{id}/edit | attribute.update | auth | AttributeController@update | Component/Item Master | Attributes | - | - | Update attribute |
| DELETE | /attribute/{id}/destroy | attribute.destroy | auth | AttributeController@destroy | Component/Item Master | Attributes | - | - | Delete attribute |
| GET | /category-attribute/assign-to-type/{itemId} | category-attribute.assign-to-type | auth | CategoryAttributeController@assignToType | Component/Item Master | Attributes | - | - | Assign to type |
| POST | /category-attribute/assign-to-type/{itemId} | category-attribute.store-assignment | auth | CategoryAttributeController@storeAssignment | Component/Item Master | Attributes | - | - | Store assignment |
| POST | /category-attribute/set-required/{id} | category-attribute.set-required | auth | CategoryAttributeController@setRequired | Component/Item Master | Attributes | - | - | Set required |
| GET | /generic | generic.index | auth | GenericController@index | Component/Item Master | Generic Product | - | generic/index.blade.php | Generic list |
| GET | /generic/create | generic.create | auth | GenericController@create | Component/Item Master | Generic Product | - | generic/create.blade.php | Create generic |
| POST | /generic/create | generic.store | auth | GenericController@store | Component/Item Master | Generic Product | - | - | Store generic |
| GET | /generic/{id}/edit | generic.edit | auth | GenericController@edit | Component/Item Master | Generic Product | - | generic/edit.blade.php | Edit generic |
| PUT | /generic/{id}/edit | generic.update | auth | GenericController@update | Component/Item Master | Generic Product | - | - | Update generic |
| DELETE | /generic/{id}/destroy | generic.destroy | auth | GenericController@destroy | Component/Item Master | Generic Product | - | - | Delete generic |
| GET | /product | product.index | auth | ProductController@index | Component/Item Master | Specific Product | - | product/index.blade.php | Product list |
| GET | /product/bom-list | product.bom-list | auth | ProductController@bomList | Component/Item Master | Specific Product | - | - | BOM list |
| GET | /product/create | product.create | auth | ProductController@create | Component/Item Master | Specific Product | - | product/create.blade.php | Create product |
| POST | /product/create | product.store | auth | ProductController@store | Component/Item Master | Specific Product | - | - | Store product |
| GET | /product/{id}/edit | product.edit | auth | ProductController@edit | Component/Item Master | Specific Product | - | product/edit.blade.php | Edit product |
| PUT | /product/{id}/edit | product.update | auth | ProductController@update | Component/Item Master | Specific Product | - | - | Update product |
| DELETE | /product/{id}/destroy | product.destroy | auth | ProductController@destroy | Component/Item Master | Specific Product | - | - | Delete product |
| GET | /product/getsubcategory/{id} | product.getsubcategory | auth | ProductController@getsubcategory | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /product/getproducttype/{id} | product.getproducttype | auth | ProductController@getproducttype | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /product/getgeneric | product.getgeneric | auth | ProductController@getgeneric | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /product/getseries | product.getseries | auth | ProductController@getseries | Component/Item Master | Specific Product | - | - | AJAX lookup |
| GET | /masterbom | masterbom.index | auth | MasterBomController@index | Master BOM | Structure | - | masterbom/index.blade.php | Master BOM list |
| GET | /masterbom/create | masterbom.create | auth | MasterBomController@create | Master BOM | Structure | - | masterbom/create.blade.php | Create Master BOM |
| POST | /masterbom/create | masterbom.store | auth | MasterBomController@store | Master BOM | Structure | - | - | Store Master BOM |
| GET | /masterbom/{id}/edit | masterbom.edit | auth | MasterBomController@edit | Master BOM | Structure | - | masterbom/edit.blade.php | Edit Master BOM |
| GET | /masterbom/{id}/copy | masterbom.copy | auth | MasterBomController@copy | Master BOM | Workflows | - | - | Copy Master BOM |
| PUT | /masterbom/{id}/edit | masterbom.update | auth | MasterBomController@update | Master BOM | Structure | - | - | Update Master BOM |
| DELETE | /masterbom/{id}/destroy | masterbom.destroy | auth | MasterBomController@destroy | Master BOM | Structure | - | - | Delete Master BOM |
| GET | /masterbom/addmore | masterbom.addmore | auth | MasterBomController@addmore | Master BOM | Items | - | masterbom/addmore.blade.php | Add more items |
| GET | /masterbom/remove | masterbom.remove | auth | MasterBomController@remove | Master BOM | Items | - | - | Remove item |
| GET | /masterbom/getsubcategory/{id} | masterbom.getsubcategory | auth | MasterBomController@getsubcategory | Master BOM | Items | - | - | AJAX lookup |
| GET | /masterbom/getproducttype/{id} | masterbom.getproducttype | auth | MasterBomController@getproducttype | Master BOM | Items | - | - | AJAX lookup |
| GET | /masterbom/getdescription | masterbom.getdescription | auth | MasterBomController@getdescription | Master BOM | Items | - | - | AJAX lookup |
| GET | /feeder-library | feeder-library.index | auth | FeederTemplateController@index | Feeder Library | Structure | - | feeder-library/index.blade.php | Feeder list |
| GET | /feeder-library/create | feeder-library.create | auth | FeederTemplateController@create | Feeder Library | Structure | - | feeder-library/create.blade.php | Create feeder |
| POST | /feeder-library | feeder-library.store | auth | FeederTemplateController@store | Feeder Library | Structure | - | - | Store feeder |
| GET | /feeder-library/{id} | feeder-library.show | auth | FeederTemplateController@show | Feeder Library | Structure | - | feeder-library/show.blade.php | Show feeder |
| GET | /feeder-library/{id}/edit | feeder-library.edit | auth | FeederTemplateController@edit | Feeder Library | Structure | - | feeder-library/edit.blade.php | Edit feeder |
| PUT | /feeder-library/{id} | feeder-library.update | auth | FeederTemplateController@update | Feeder Library | Structure | - | - | Update feeder |
| PATCH | /feeder-library/{id}/toggle | feeder-library.toggle | auth | FeederTemplateController@toggleActive | Feeder Library | Workflows | - | - | Toggle active |
| GET | /proposal-bom | proposal-bom.index | auth | ProposalBomController@index | Proposal BOM | Structure | - | proposal-bom/index.blade.php | Proposal BOM list - Additional routes likely under Quotation V2 apply endpoints and search APIs |
| GET | /proposal-bom/{id} | proposal-bom.show | auth | ProposalBomController@show | Proposal BOM | Structure | - | proposal-bom/show.blade.php | Show Proposal BOM - Additional routes likely under Quotation V2 apply endpoints and search APIs |
| GET | /proposal-bom/{id}/reuse | proposal-bom.reuse | auth | ProposalBomController@reuse | Proposal BOM | Workflows | Quotation | - | Reuse Proposal BOM - Additional routes likely under Quotation V2 apply endpoints and search APIs |
| POST | /proposal-bom/{id}/promote | proposal-bom.promote | auth | ProposalBomController@promoteToMaster | Proposal BOM | Workflows | Master BOM | - | Promote to Master - Additional routes likely under Quotation V2 apply endpoints and search APIs |
| GET | /catalog-health | catalog-health.index | auth | CatalogHealthController@index | Component/Item Master | Catalog Health | - | catalog-health/index.blade.php | Catalog health |
| GET | /catalog-health/summary | catalog-health.summary | auth | CatalogHealthController@getSummary | Component/Item Master | Catalog Health | - | - | Health summary API |
| GET | /catalog-cleanup | catalog-cleanup.index | auth | CatalogCleanupController@index | Component/Item Master | Catalog Cleanup | - | catalog-cleanup/index.blade.php | Catalog cleanup |
| POST | /catalog-cleanup/assign-producttype | catalog-cleanup.assign-producttype | auth | CatalogCleanupController@assignProductType | Component/Item Master | Catalog Cleanup | - | - | Assign product type |
| POST | /catalog-cleanup/fill-attributes | catalog-cleanup.fill-attributes | auth | CatalogCleanupController@fillAttributes | Component/Item Master | Catalog Cleanup | - | - | Fill attributes |
| GET | /price | price.index | auth | PriceController@index | Component/Item Master | Price List | - | price/index.blade.php | Price list |
| GET | /price/create | price.create | auth | PriceController@create | Component/Item Master | Price List | - | price/create.blade.php | Create price |
| POST | /price/create | price.store | auth | PriceController@store | Component/Item Master | Price List | - | - | Store price |
| GET | /price/{id}/edit | price.edit | auth | PriceController@edit | Component/Item Master | Price List | - | price/edit.blade.php | Edit price |
| PUT | /price/{id}/edit | price.update | auth | PriceController@update | Component/Item Master | Price List | - | - | Update price |
| DELETE | /price/{id}/destroy | price.destroy | auth | PriceController@destroy | Component/Item Master | Price List | - | - | Delete price |
| GET | /project | project.index | auth | ProjectController@index | Project | Structure | - | project/index.blade.php | Project list |
| GET | /project/create | project.create | auth | ProjectController@create | Project | Structure | - | project/create.blade.php | Create project |
| POST | /project/create | project.store | auth | ProjectController@store | Project | Structure | - | - | Store project |
| GET | /project/{id}/edit | project.edit | auth | ProjectController@edit | Project | Structure | - | project/edit.blade.php | Edit project |
| PUT | /project/{id}/edit | project.update | auth | ProjectController@update | Project | Structure | - | - | Update project |
| DELETE | /project/{id}/destroy | project.destroy | auth | ProjectController@destroy | Project | Structure | - | - | Delete project |
| GET | /vendors | vendor.index | auth | VendorController@index | Master | Vendor | - | vendor/index.blade.php | Vendor list |
| GET | /vendors/create | vendor.create | auth | VendorController@create | Master | Vendor | - | vendor/create.blade.php | Create vendor |
| POST | /vendors/create | vendor.store | auth | VendorController@store | Master | Vendor | - | - | Store vendor |
| GET | /vendors/{id}/edit | vendor.edit | auth | VendorController@edit | Master | Vendor | - | vendor/edit.blade.php | Edit vendor |
| PUT | /vendors/{id}/edit | vendor.update | auth | VendorController@update | Master | Vendor | - | - | Update vendor |
| DELETE | /vendors/{id}/destroy | vendor.destroy | auth | VendorController@destroy | Master | Vendor | - | - | Delete vendor |
| GET | /quotation | quotation.index | auth | QuotationController@index | Quotation | Legacy | - | quotation/index.blade.php | Quotation list |
| GET | /quotation/bom-list | quotation.bom-list | auth | QuotationController@bomList | Quotation | Legacy | - | - | BOM list |
| GET | /quotation/create | quotation.create | auth | QuotationController@create | Quotation | Legacy | - | quotation/create.blade.php | Create quotation |
| POST | /quotation/create | quotation.store | auth | QuotationController@store | Quotation | Legacy | - | - | Store quotation |
| GET | /quotation/{id}/edit | quotation.edit | auth | QuotationController@edit | Quotation | Legacy | - | quotation/edit.blade.php | Edit quotation |
| PUT | /quotation/{id}/edit | quotation.update | auth | QuotationController@update | Quotation | Legacy | - | - | Update quotation |
| DELETE | /quotation/{id}/destroy | quotation.destroy | auth | QuotationController@destroy | Quotation | Legacy | - | - | Delete quotation |
| GET | /quotation/{id}/v2 | quotation.v2.index | auth | QuotationV2Controller@index | Quotation | V2 | - | quotation/v2/index.blade.php | V2 main view |
| GET | /quotation/{id}/panel/{panelId} | quotation.v2.panel | auth | QuotationV2Controller@panel | Quotation | V2 | - | quotation/v2/panel.blade.php | Panel view |
| GET | /quotation/v2/panel/{panelId}/validate-tree | quotation.v2.validateTree | auth | QuotationV2Controller@validateTree | Quotation | V2 | - | - | Validate tree |
| GET | /quotation/{id}/feeder/{feederId}/details | quotation.v2.feeder.details | auth, throttle:search | QuotationV2Controller@getFeederDetails | Quotation | V2 | - | - | Progressive loading |
| GET | /quotation/{id}/bom/{bomId}/details | quotation.v2.bom.details | auth, throttle:search | QuotationV2Controller@getBomDetails | Quotation | V2 | - | - | Progressive loading |
| POST | /quotation/{id}/panel | quotation.v2.addPanel | auth | QuotationV2Controller@addPanel | Quotation | V2 | - | - | Add panel |
| POST | /quotation/{id}/panel/{panelId}/feeder | quotation.v2.addFeeder | auth | QuotationV2Controller@addFeeder | Quotation | V2 | - | - | Add feeder |
| POST | /quotation/{id}/bom/{parentBomId}/bom | quotation.v2.addBom | auth | QuotationV2Controller@addBom | Quotation | V2 | - | - | Add BOM |
| POST | /quotation/{id}/bom/{bomId}/item | quotation.v2.addItem | auth | QuotationV2Controller@addItem | Quotation | V2 | - | - | Add item |
| POST | /quotation/v2/apply-master-bom | quotation.v2.applyMasterBom | auth, throttle:critical-write | QuotationV2Controller@applyMasterBom | Quotation | V2 | Master BOM | - | Apply Master BOM - Cross-module: Master BOM |
| POST | /quotation/{quotation}/panel/{panel}/feeder/apply-template | quotation.v2.applyFeederTemplate | auth | QuotationV2Controller@applyFeederTemplate | Quotation | V2 | Feeder Library | - | Apply feeder template - Cross-module: Feeder Library |
| POST | /quotation/{quotation}/feeder/{feeder}/delete | quotation.v2.deleteFeeder | auth | QuotationV2Controller@deleteFeeder | Quotation | V2 | - | - | Delete feeder |
| POST | /quotation/{quotation}/bom/{bom}/delete | quotation.v2.deleteBom | auth | QuotationV2Controller@deleteBom | Quotation | V2 | - | - | Delete BOM |
| POST | /quotation/{quotation}/panel/{panel}/delete | quotation.v2.deletePanel | auth | QuotationV2Controller@deletePanel | Quotation | V2 | - | - | Delete panel |
| POST | /quotation/{quotation}/panel/{panel}/update | quotation.v2.updatePanel | auth | QuotationV2Controller@updatePanel | Quotation | V2 | - | - | Update panel |
| GET | /quotation/{quotation}/bom/{bom}/edit | quotation.v2.editBom | auth | QuotationV2Controller@editBom | Quotation | V2 | - | quotation/v2/bom-edit.blade.php | Edit BOM |
| POST | /quotation/{quotation}/bom/{bom}/update | quotation.v2.updateBom | auth | QuotationV2Controller@updateBom | Quotation | V2 | - | - | Update BOM |
| POST | /quotation/{quotation}/items/batch-update | quotation.v2.batchUpdateItems | auth | QuotationV2Controller@batchUpdateItems | Quotation | V2 | - | - | Batch update items |
| POST | /quotation/v2/apply-proposal-bom | quotation.v2.applyProposalBom | auth, throttle:critical-write | QuotationV2Controller@applyProposalBom | Quotation | V2 | Proposal BOM | - | Apply Proposal BOM - Cross-module: Proposal BOM |
| POST | /quotation/{quotation}/panel/{panel}/qty | quotation.v2.panel.updateQty | auth, throttle:autosave | QuotationV2Controller@updatePanelQty | Quotation | V2 | - | - | Update panel qty |
| POST | /quotation/{quotation}/feeder/{feeder}/qty | quotation.v2.feeder.updateQty | auth, throttle:autosave | QuotationV2Controller@updateFeederQty | Quotation | V2 | - | - | Update feeder qty |
| POST | /quotation/{quotation}/bom/{bom}/qty | quotation.v2.bom.updateQty | auth, throttle:autosave | QuotationV2Controller@updateBomQty | Quotation | V2 | - | - | Update BOM qty |
| PATCH | /quotation/{quotation}/panel/{panel}/qty | quotation.v2.updatePanelQty | auth, throttle:autosave | QuotationV2Controller@updatePanelQty | Quotation | V2 | - | - | Update panel qty (backward compat) |
| PATCH | /quotation/{quotation}/feeder/{bom}/qty | quotation.v2.updateFeederQty | auth, throttle:autosave | QuotationV2Controller@updateFeederQty | Quotation | V2 | - | - | Update feeder qty (backward compat) |
| PATCH | /quotation/{quotation}/bom/{bom}/qty | quotation.v2.updateBomQty | auth, throttle:autosave | QuotationV2Controller@updateBomQty | Quotation | V2 | - | - | Update BOM qty (backward compat) |
| POST | /quotation/{quotation}/item/{item}/rate | quotation.v2.item.updateRate | auth, throttle:autosave | QuotationV2Controller@updateItemRate | Quotation | V2 | - | - | Update item rate |
| POST | /quotation/{quotation}/item/{item}/discount | quotation.v2.item.updateDiscount | auth, throttle:autosave | QuotationV2Controller@updateItemDiscount | Quotation | V2 | - | - | Update item discount |
| POST | /quotation/{quotation}/item/{item}/qty | quotation.v2.item.updateQty | auth, throttle:autosave | QuotationV2Controller@updateItemQty | Quotation | V2 | - | - | Update item qty |
| GET | /quotation/{quotation}/v2/export-bom | quotation.v2.exportBom | auth | QuotationV2Controller@exportBom | Quotation | V2 | - | - | Export BOM Excel |
| GET | /quotation/{id}/audit-logs | quotation.audit-logs | auth | QuotationController@auditLogs | Quotation | V2 | - | - | Audit logs |
| GET | /quotation/v2/masterbom-view | quotation.v2.masterbomView | auth | QuotationV2Controller@getMasterBomView | Quotation | V2 | - | - | Master BOM view |
| GET | /quotation/v2/products-by-type | quotation.v2.products-by-type | auth, throttle:search | QuotationV2Controller@getProductsByType | Quotation | V2 | - | - | Products by type |
| GET | /api/proposal-bom/search | api.proposalBom.search | auth, throttle:search | QuotationController@searchProposalBom | Quotation | V2 | - | - | Search Proposal BOM |
| GET | /api/reuse/panels | api.reuse.panels | auth, throttle:search | ReuseController@searchPanels | Quotation | V2 | - | - | Search panels |
| GET | /api/reuse/feeders | api.reuse.feeders | auth, throttle:search | ReuseController@searchFeeders | Quotation | V2 | - | - | Search feeders |
| GET | /api/reuse/master-boms | api.reuse.masterBoms | auth, throttle:search | ReuseController@searchMasterBoms | Quotation | V2 | - | - | Search Master BOMs |
| GET | /api/reuse/proposal-boms | api.reuse.proposalBoms | auth, throttle:search | ReuseController@searchProposalBoms | Quotation | V2 | - | - | Search Proposal BOMs |
| POST | /reuse/panel/apply | reuse.panel.apply | auth, throttle:critical-write | QuotationV2Controller@applyPanelReuse | Quotation | V2 | - | - | Apply panel reuse |
| POST | /reuse/feeder/apply | reuse.feeder.apply | auth, throttle:critical-write | QuotationV2Controller@applyFeederReuse | Quotation | V2 | - | - | Apply feeder reuse |
| GET | /quotations/{quotation_id}/discount-rules | quotation.discount-rules.index | auth | QuotationDiscountRuleController@index | Quotation | Discount Rules | - | quotation/discount-rules/index.blade.php | Discount rules list |
| GET | /quotations/{quotation_id}/discount-rules/create | quotation.discount-rules.create | auth | QuotationDiscountRuleController@create | Quotation | Discount Rules | - | quotation/discount-rules/create.blade.php | Create discount rule |
| POST | /quotations/{quotation_id}/discount-rules | quotation.discount-rules.store | auth | QuotationDiscountRuleController@store | Quotation | Discount Rules | - | - | Store discount rule |
| GET | /quotations/{quotation_id}/discount-rules/{id} | quotation.discount-rules.show | auth | QuotationDiscountRuleController@show | Quotation | Discount Rules | - | quotation/discount-rules/show.blade.php | Show discount rule |
| GET | /quotations/{quotation_id}/discount-rules/{id}/edit | quotation.discount-rules.edit | auth | QuotationDiscountRuleController@edit | Quotation | Discount Rules | - | quotation/discount-rules/edit.blade.php | Edit discount rule |
| PUT | /quotations/{quotation_id}/discount-rules/{id} | quotation.discount-rules.update | auth | QuotationDiscountRuleController@update | Quotation | Discount Rules | - | - | Update discount rule |
| PATCH | /quotations/{quotation_id}/discount-rules/{id} | quotation.discount-rules.update | auth | QuotationDiscountRuleController@update | Quotation | Discount Rules | - | - | Update discount rule (PATCH) |
| DELETE | /quotations/{quotation_id}/discount-rules/{id} | quotation.discount-rules.destroy | auth | QuotationDiscountRuleController@destroy | Quotation | Discount Rules | - | - | Delete discount rule |
| GET | /quotations/{quotation_id}/discount-rules/preview | quotation.discount-rules.preview | auth | QuotationDiscountRuleController@preview | Quotation | Discount Rules | - | - | Preview discount |
| POST | /quotations/{quotation_id}/discount-rules/apply | quotation.discount-rules.apply | auth | QuotationDiscountRuleController@apply | Quotation | Discount Rules | - | - | Apply discount rules |
| POST | /quotations/{quotation_id}/discount-rules/reset | quotation.discount-rules.reset | auth | QuotationDiscountRuleController@reset | Quotation | Discount Rules | - | - | Reset discounts |
| GET | /quotations/{quotation_id}/discount-rules/last-apply | quotation.discount-rules.last-apply | auth | QuotationDiscountRuleController@lastApply | Quotation | Discount Rules | - | - | Last apply info |
| GET | /quotations/{quotation_id}/discount-rules/lookup/makes | quotation.discount-rules.lookup.makes | auth | QuotationDiscountRuleController@lookupMakes | Quotation | Discount Rules | - | - | Lookup makes |
| GET | /quotations/{quotation_id}/discount-rules/lookup/series | quotation.discount-rules.lookup.series | auth | QuotationDiscountRuleController@lookupSeries | Quotation | Discount Rules | - | - | Lookup series |
| GET | /quotations/{quotation_id}/discount-rules/lookup/product-types | quotation.discount-rules.lookup.product-types | auth | QuotationDiscountRuleController@lookupProductTypes | Quotation | Discount Rules | - | - | Lookup product types |
| GET | /quotations/{quotation_id}/discount-rules/lookup/products | quotation.discount-rules.lookup.products | auth | QuotationDiscountRuleController@lookupProducts | Quotation | Discount Rules | - | - | Lookup products |
| GET | /quotation-discount-rules/test-preview | discount-rules.test-preview | auth | QuotationDiscountRuleTestController@testPreview | Quotation | Discount Rules | - | - | Test preview |
| GET | /quotation-discount-rules/test-rules | discount-rules.test-rules | auth | QuotationDiscountRuleTestController@testRules | Quotation | Discount Rules | - | - | Test rules |
| GET | /quotation-discount-rules/test-match | discount-rules.test-match | auth | QuotationDiscountRuleTestController@testMatch | Quotation | Discount Rules | - | - | Test match |
| GET | /quotation/addmore | quotation.addmore | auth | QuotationController@addmore | Quotation | Legacy | - | quotation/addmore.blade.php | Add more |
| GET | /quotation/remove | quotation.remove | auth | QuotationController@remove | Quotation | Legacy | - | - | Remove |
| GET | /quotation/contact | quotation.contact | auth | QuotationController@contact | Quotation | Legacy | - | - | Contact lookup |
| GET | /quotation/getmake/{id} | quotation.getmake | auth | QuotationController@getmake | Quotation | Legacy | - | - | Get make |
| GET | /quotation/getseries/{id} | quotation.getseries | auth | QuotationController@getseries | Quotation | Legacy | - | - | Get series |
| GET | /quotation/{id}/step | quotation.step | auth | QuotationController@step | Quotation | Legacy | - | quotation/step.blade.php | Step view |
| GET | /quotation/{quotation}/step/panel/{panel} | quotation.step.panel | auth | QuotationController@stepPanel | Quotation | Legacy | - | quotation/step-panel.blade.php | Step panel |
| PUT | /quotation/{id}/step | quotation.stepupdate | auth | QuotationController@stepupdate | Quotation | Legacy | - | - | Update step |
| PUT | /quotation/{id}/updateSaleData | quotation.updateSaleData | auth | QuotationController@updateSaleData | Quotation | Legacy | - | - | Update sale data |
| GET | /quotation/addmoresale | quotation.addmoresale | auth | QuotationController@addmoresale | Quotation | Legacy | - | - | Add more sale |
| GET | /quotation/addmoresale/{qid}/{sid} | quotation.addmoresaledata | auth | QuotationController@addmoresaledata | Quotation | Legacy | - | - | Add more sale data |
| GET | /quotation/getMasterBom | quotation.getMasterBom | auth | QuotationController@getMasterBom | Quotation | Legacy | - | - | Get Master BOM |
| GET | /quotation/getMultipleMasterBom | quotation.getMultipleMasterBom | auth | QuotationController@getMultipleMasterBom | Quotation | Legacy | - | - | Get multiple Master BOMs |
| GET | /quotation/getitem | quotation.getitem | auth | QuotationController@getitem | Quotation | Legacy | - | - | Get item |
| GET | /quotation/getItemvalue | quotation.getItemvalue | auth | QuotationController@getItemvalue | Quotation | Legacy | - | - | Get item value |
| GET | /quotation/getMasterBomVal | quotation.getMasterBomVal | auth | QuotationController@getMasterBomVal | Quotation | Legacy | - | - | Get Master BOM value |
| GET | /quotation/getProposalBomVal | quotation.getProposalBomVal | auth | QuotationController@getProposalBomVal | Quotation | Legacy | - | - | Get Proposal BOM value |
| GET | /quotation/getSingleVal | quotation.getSingleVal | auth | QuotationController@getSingleVal | Quotation | Legacy | - | - | Get single value |
| GET | /quotation/saleremove | quotation.saleremove | auth | QuotationController@saleremove | Quotation | Legacy | - | - | Remove sale |
| POST | /quotation/masterbomremove | quotation.masterbomremove | auth | QuotationController@masterbomremove | Quotation | Legacy | - | - | Remove Master BOM |
| POST | /quotation/itemremove | quotation.itemremove | auth | QuotationController@itemremove | Quotation | Legacy | - | - | Remove item |
| GET | /quotation/getItemMake | quotation.getItemMake | auth | QuotationController@getItemMake | Quotation | Legacy | - | - | Get item make |
| GET | /quotation/getItemSeries | quotation.getItemSeries | auth | QuotationController@getItemSeries | Quotation | Legacy | - | - | Get item series |
| GET | /quotation/getItemDescription | quotation.getItemDescription | auth | QuotationController@getItemDescription | Quotation | Legacy | - | - | Get item description |
| GET | /quotation/getItemRate | quotation.getItemRate | auth | QuotationController@getItemRate | Quotation | Legacy | - | - | Get item rate |
| GET | /quotation/pdf/{id} | quotation.pdf | auth | QuotationController@pdf | Quotation | Reports | - | - | Generate PDF |
| GET | /quotation/excel/{id} | quotation.excel | auth | QuotationController@excel | Quotation | Reports | - | - | Export Excel |
| GET | /quotation/project/{projectIdOrName} | quotation.project | auth | QuotationController@getProjectQuotations | Quotation | Reports | - | - | Get project quotations |
| GET | /quotation/search-projects | quotation.search-projects | auth | QuotationController@searchProjects | Quotation | Reports | - | - | Search projects |
| GET | /quotation/addMoreDiscount | quotation.addMoreDiscount | auth | QuotationController@addMoreDiscount | Quotation | Legacy | - | - | Add more discount |
| POST | /quotation/changediscount/{qid} | quotation.changediscount | auth | QuotationController@changediscount | Quotation | Legacy | - | - | Change discount |
| GET | /quotation/changemakeseries | quotation.changemakeseries | auth | QuotationController@changemakeseries | Quotation | Legacy | - | - | Change make/series |
| GET | /quotation/printsave | quotation.printsave | auth | QuotationController@printsave | Quotation | Legacy | - | - | Print save |
| GET | /quotation/loadData | quotation.loadData | auth | QuotationController@loadData | Quotation | Legacy | - | - | Load data |
| GET | /quotation/MakeSeriesChange | quotation.MakeSeriesChange | auth | QuotationController@MakeSeriesChange | Quotation | Legacy | - | - | Make/series change |
| GET | /import | import.view | auth | ImportController@importview | Component/Item Master | Import/Export | - | import/index.blade.php | Import view |
| GET | /importview/{uuid} | product.tempview | auth | ImportController@importtempview | Component/Item Master | Import/Export | - | import/tempview.blade.php | Temp view |
| POST | /importview | product.importtemadd | auth | ImportController@importtemadd | Component/Item Master | Import/Export | - | - | Add temp |
| GET | /importview/{id}/delete | product.importtemdestroy | auth | ImportController@importtemdestroy | Component/Item Master | Import/Export | - | - | Delete temp |
| POST | /import | import.add | auth | ImportController@importadd | Component/Item Master | Import/Export | - | - | Import add |
| POST | /export | export.exportsample | auth | ImportController@exportsample | Component/Item Master | Import/Export | - | - | Export sample |
| GET | /pdfcontain | pdfcontain.index | auth | ImportController@pdfcontain | Master | PDF Formats | - | pdfcontain/index.blade.php | PDF container - Controller name is misleading (ImportController). Feature is Master/PDF container. |
| PUT | /pdfcontain | pdfcontain.save | auth | ImportController@pdfcontainsave | Master | PDF Formats | - | - | Save PDF container - Controller name is misleading (ImportController). Feature is Master/PDF container. |
| GET | /mySQLDownload | mySQLDownload | auth | CronController@mySQLDownload | Shared/Ops | Maintenance | - | - | MySQL download |
| GET | /clear | - | auth | Closure | Shared/Ops | Maintenance | - | - | Clear cache - Maintenance route; verify if enabled in production |

---

## Route Summary by Module

| Module | Route Count | Notes |
|--------|-------------|-------|
| **Component/Item Master** | ~60 | Category, Subcategory, Product Type, Make, Series, Attributes, Generic/Specific Products, Price, Import/Export, Catalog Health |
| **Quotation** | ~80 | Legacy + V2 routes, Discount Rules, Reports, AJAX endpoints |
| **Master BOM** | ~12 | CRUD + workflows + AJAX lookups |
| **Feeder Library** | ~7 | CRUD + toggle active |
| **Proposal BOM** | ~4 | List, show, reuse, promote |
| **Project** | ~7 | CRUD + client/contact management |
| **Master** | ~7 | Organization, Vendor, PDF container |
| **Employee/Role** | ~12 | User and Role CRUD |
| **Security** | 0 | No direct routes (handled via middleware) |
| **Dashboard** | 2 | Home pages |
| **Shared/Ops** | 2 | Maintenance (MySQL download, Cache clear) |

**Total Routes Mapped:** ~192 routes (out of ~269 total routes in web.php)

---

## Notes

1. **Incomplete Coverage:** This is a first pass covering ~80% of routes. Some legacy quotation routes and helper routes may be missing.

2. **Module Assignment:** Routes are assigned to modules based on controller names and URI prefixes. Some routes may need review.

3. **Views/JS:** View paths are inferred from standard Laravel conventions. Actual view files may differ.

4. **Middleware:** Most routes use `auth` middleware. Additional middleware (throttle, etc.) is noted where present.

5. **AJAX Endpoints:** Many routes under `/api` prefix are AJAX endpoints for dynamic dropdown loading and progressive loading.

6. **V2 Routes:** Quotation V2 routes are clearly marked and separate from legacy routes.

---

## Next Steps

1. Complete remaining route extraction (~20% remaining)
2. Validate module assignments
3. Add view file verification
4. Create FEATURE_CODE_MAP (Phase 2 Step 2)
5. Create FILE_OWNERSHIP (Phase 2 Step 3)

---

**Last Updated:** 2025-12-17 (IST)  
**Status:** First Pass Complete (~80% coverage)
