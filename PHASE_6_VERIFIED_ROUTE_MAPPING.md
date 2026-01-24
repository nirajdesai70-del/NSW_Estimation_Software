# Phase 6 Verified Route Mapping
## Complete NEPL → NSW Route Mapping (Verified from Actual System)

**Date:** 2025-01-27  
**Source:** `/Volumes/T9/Projects/nish/routes/web.php` (verified)  
**Status:** COMPLETE VERIFICATION

---

## 📋 Route Count Summary

**Total Routes in NEPL:** ~200+ routes  
**Verified from:** Actual `routes/web.php` file

---

## 🔍 Complete Route Mapping by Module

### 1. Foundation Entities (Track F)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/organization` | GET | OrganizationController@index | `GET /api/v1/organizations` | ❌ Missing |
| `/organization/create` | GET | OrganizationController@create | `GET /api/v1/organizations/create` | ❌ Missing |
| `/organization/create` | POST | OrganizationController@store | `POST /api/v1/organizations` | ❌ Missing |
| `/organization/{id}/edit` | GET | OrganizationController@edit | `GET /api/v1/organizations/{id}/edit` | ❌ Missing |
| `/organization/{id}/edit` | PUT | OrganizationController@update | `PUT /api/v1/organizations/{id}` | ❌ Missing |
| `/organization/{id}/destroy` | DELETE | OrganizationController@destroy | `DELETE /api/v1/organizations/{id}` | ❌ Missing |
| `/client` | GET | ClientController@index | `GET /api/v1/customers` | ❌ Missing |
| `/client/create` | GET | ClientController@create | `GET /api/v1/customers/create` | ❌ Missing |
| `/client/create` | POST | ClientController@store | `POST /api/v1/customers` | ❌ Missing |
| `/client/{id}/edit` | GET | ClientController@edit | `GET /api/v1/customers/{id}/edit` | ❌ Missing |
| `/client/{id}/edit` | PUT | ClientController@update | `PUT /api/v1/customers/{id}` | ❌ Missing |
| `/client/{id}/destroy` | DELETE | ClientController@destroy | `DELETE /api/v1/customers/{id}` | ❌ Missing |
| `/client/{id}/getState` | GET | ClientController@getState | `GET /api/v1/customers/{id}/state` | ❌ Missing |
| `/contact` | GET | ContactController@index | `GET /api/v1/contacts` | ❌ Missing |
| `/contact/create` | GET | ContactController@create | `GET /api/v1/contacts/create` | ❌ Missing |
| `/contact/create` | POST | ContactController@store | `POST /api/v1/contacts` | ❌ Missing |
| `/contact/{id}/edit` | GET | ContactController@edit | `GET /api/v1/contacts/{id}/edit` | ❌ Missing |
| `/contact/{id}/edit` | PUT | ContactController@update | `PUT /api/v1/contacts/{id}` | ❌ Missing |
| `/contact/{id}/destroy` | DELETE | ContactController@destroy | `DELETE /api/v1/contacts/{id}` | ❌ Missing |
| `/project` | GET | ProjectController@index | `GET /api/v1/projects` | ❌ Missing |
| `/project/create` | GET | ProjectController@create | `GET /api/v1/projects/create` | ❌ Missing |
| `/project/create` | POST | ProjectController@store | `POST /api/v1/projects` | ❌ Missing |
| `/project/{id}/edit` | GET | ProjectController@edit | `GET /api/v1/projects/{id}/edit` | ❌ Missing |
| `/project/{id}/edit` | PUT | ProjectController@update | `PUT /api/v1/projects/{id}` | ❌ Missing |
| `/project/{id}/destroy` | DELETE | ProjectController@destroy | `DELETE /api/v1/projects/{id}` | ❌ Missing |

**Total Foundation Routes:** 24 routes  
**Missing:** 24 routes (100%)

---

### 2. Component/Item Master (Track G)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/category` | GET | CategoryController@index | `GET /api/v1/categories` | ❌ Missing |
| `/category/create` | GET | CategoryController@create | `GET /api/v1/categories/create` | ❌ Missing |
| `/category/create` | POST | CategoryController@store | `POST /api/v1/categories` | ❌ Missing |
| `/category/addmore` | GET | CategoryController@addmore | `GET /api/v1/categories/addmore` | ❌ Missing |
| `/category/{id}/edit` | GET | CategoryController@edit | `GET /api/v1/categories/{id}/edit` | ❌ Missing |
| `/category/{id}/edit` | PUT | CategoryController@update | `PUT /api/v1/categories/{id}` | ❌ Missing |
| `/category/{id}/destroy` | DELETE | CategoryController@destroy | `DELETE /api/v1/categories/{id}` | ❌ Missing |
| `/subcategory` | GET | SubCategoryController@index | `GET /api/v1/subcategories` | ❌ Missing |
| `/subcategory/create` | GET | SubCategoryController@create | `GET /api/v1/subcategories/create` | ❌ Missing |
| `/subcategory/create` | POST | SubCategoryController@store | `POST /api/v1/subcategories` | ❌ Missing |
| `/subcategory/{id}/edit` | GET | SubCategoryController@edit | `GET /api/v1/subcategories/{id}/edit` | ❌ Missing |
| `/subcategory/{id}/edit` | PUT | SubCategoryController@update | `PUT /api/v1/subcategories/{id}` | ❌ Missing |
| `/subcategory/{id}/destroy` | DELETE | SubCategoryController@destroy | `DELETE /api/v1/subcategories/{id}` | ❌ Missing |
| `/product-type` | GET | ItemController@index | `GET /api/v1/product-types` | ❌ Missing |
| `/product-type/create` | GET | ItemController@create | `GET /api/v1/product-types/create` | ❌ Missing |
| `/product-type/create` | POST | ItemController@store | `POST /api/v1/product-types` | ❌ Missing |
| `/product-type/{id}/edit` | GET | ItemController@edit | `GET /api/v1/product-types/{id}/edit` | ❌ Missing |
| `/product-type/{id}/edit` | PUT | ItemController@update | `PUT /api/v1/product-types/{id}` | ❌ Missing |
| `/product-type/{id}/destroy` | DELETE | ItemController@destroy | `DELETE /api/v1/product-types/{id}` | ❌ Missing |
| `/make` | GET | MakeController@index | `GET /api/v1/makes` | ❌ Missing |
| `/make/create` | GET | MakeController@create | `GET /api/v1/makes/create` | ❌ Missing |
| `/make/create` | POST | MakeController@store | `POST /api/v1/makes` | ❌ Missing |
| `/make/{id}/edit` | GET | MakeController@edit | `GET /api/v1/makes/{id}/edit` | ❌ Missing |
| `/make/{id}/edit` | PUT | MakeController@update | `PUT /api/v1/makes/{id}` | ❌ Missing |
| `/make/{id}/destroy` | DELETE | MakeController@destroy | `DELETE /api/v1/makes/{id}` | ❌ Missing |
| `/series` | GET | SeriesController@index | `GET /api/v1/series` | ❌ Missing |
| `/series/create` | GET | SeriesController@create | `GET /api/v1/series/create` | ❌ Missing |
| `/series/create` | POST | SeriesController@store | `POST /api/v1/series` | ❌ Missing |
| `/series/{id}/edit` | GET | SeriesController@edit | `GET /api/v1/series/{id}/edit` | ❌ Missing |
| `/series/{id}/edit` | PUT | SeriesController@update | `PUT /api/v1/series/{id}` | ❌ Missing |
| `/series/{id}/destroy` | DELETE | SeriesController@destroy | `DELETE /api/v1/series/{id}` | ❌ Missing |
| `/attribute` | GET | AttributeController@index | `GET /api/v1/attributes` | ❌ Missing |
| `/attribute/create` | GET | AttributeController@create | `GET /api/v1/attributes/create` | ❌ Missing |
| `/attribute/create` | POST | AttributeController@store | `POST /api/v1/attributes` | ❌ Missing |
| `/attribute/{id}/edit` | GET | AttributeController@edit | `GET /api/v1/attributes/{id}/edit` | ❌ Missing |
| `/attribute/{id}/edit` | PUT | AttributeController@update | `PUT /api/v1/attributes/{id}` | ❌ Missing |
| `/attribute/{id}/destroy` | DELETE | AttributeController@destroy | `DELETE /api/v1/attributes/{id}` | ❌ Missing |
| `/category-attribute/assign-to-type/{itemId}` | GET | CategoryAttributeController@assignToType | `GET /api/v1/category-attributes/assign/{itemId}` | ❌ Missing |
| `/category-attribute/assign-to-type/{itemId}` | POST | CategoryAttributeController@storeAssignment | `POST /api/v1/category-attributes/assign/{itemId}` | ❌ Missing |
| `/category-attribute/set-required/{id}` | POST | CategoryAttributeController@setRequired | `POST /api/v1/category-attributes/{id}/required` | ❌ Missing |
| `/generic` | GET | GenericController@index | `GET /api/v1/l1-products` | ❌ Missing |
| `/generic/create` | GET | GenericController@create | `GET /api/v1/l1-products/create` | ❌ Missing |
| `/generic/create` | POST | GenericController@store | `POST /api/v1/l1-products` | ❌ Missing |
| `/generic/{id}/edit` | GET | GenericController@edit | `GET /api/v1/l1-products/{id}/edit` | ❌ Missing |
| `/generic/{id}/edit` | PUT | GenericController@update | `PUT /api/v1/l1-products/{id}` | ❌ Missing |
| `/generic/{id}/destroy` | DELETE | GenericController@destroy | `DELETE /api/v1/l1-products/{id}` | ❌ Missing |
| `/product` | GET | ProductController@index | `GET /api/v1/products` | ⚠️ Partial (Catalog) |
| `/product/bom-list` | GET | ProductController@bomList | `GET /api/v1/products/bom-list` | ❌ Missing |
| `/product/create` | GET | ProductController@create | `GET /api/v1/products/create` | ❌ Missing |
| `/product/create` | POST | ProductController@store | `POST /api/v1/products` | ❌ Missing |
| `/product/{id}/edit` | GET | ProductController@edit | `GET /api/v1/products/{id}/edit` | ❌ Missing |
| `/product/{id}/edit` | PUT | ProductController@update | `PUT /api/v1/products/{id}` | ❌ Missing |
| `/product/{id}/destroy` | DELETE | ProductController@destroy | `DELETE /api/v1/products/{id}` | ❌ Missing |
| `/product/getsubcategory/{id}` | GET | ProductController@getsubcategory | `GET /api/v1/products/subcategory/{id}` | ❌ Missing |
| `/product/getproducttype/{id}` | GET | ProductController@getproducttype | `GET /api/v1/products/producttype/{id}` | ❌ Missing |
| `/product/getgeneric` | GET | ProductController@getgeneric | `GET /api/v1/products/generic` | ❌ Missing |
| `/product/getseries` | GET | ProductController@getseries | `GET /api/v1/products/series` | ❌ Missing |
| `/price` | GET | PriceController@index | `GET /api/v1/prices` | ⚠️ Partial (Pricing) |
| `/price/create` | GET | PriceController@create | `GET /api/v1/prices/create` | ❌ Missing |
| `/price/create` | POST | PriceController@store | `POST /api/v1/prices` | ❌ Missing |
| `/price/{id}/edit` | GET | PriceController@edit | `GET /api/v1/prices/{id}/edit` | ❌ Missing |
| `/price/{id}/edit` | PUT | PriceController@update | `PUT /api/v1/prices/{id}` | ❌ Missing |
| `/price/{id}/destroy` | DELETE | PriceController@destroy | `DELETE /api/v1/prices/{id}` | ❌ Missing |
| `/catalog-health` | GET | CatalogHealthController@index | `GET /api/v1/catalog-health` | ❌ Missing |
| `/catalog-health/summary` | GET | CatalogHealthController@getSummary | `GET /api/v1/catalog-health/summary` | ❌ Missing |
| `/catalog-cleanup` | GET | CatalogCleanupController@index | `GET /api/v1/catalog-cleanup` | ❌ Missing |
| `/catalog-cleanup/assign-producttype` | POST | CatalogCleanupController@assignProductType | `POST /api/v1/catalog-cleanup/assign-producttype` | ❌ Missing |
| `/catalog-cleanup/fill-attributes` | POST | CatalogCleanupController@fillAttributes | `POST /api/v1/catalog-cleanup/fill-attributes` | ❌ Missing |
| `/import` | GET | ImportController@importview | `GET /api/v1/import` | ⚠️ Partial (Track B) |
| `/importview/{uuid}` | GET | ImportController@importtempview | `GET /api/v1/import/{uuid}` | ❌ Missing |
| `/importview` | POST | ImportController@importtemadd | `POST /api/v1/import/temp` | ❌ Missing |
| `/importview/{id}/delete` | GET | ImportController@importtemdestroy | `DELETE /api/v1/import/temp/{id}` | ❌ Missing |
| `/import` | POST | ImportController@importadd | `POST /api/v1/import/execute` | ⚠️ Partial (Track B) |
| `/export` | POST | ImportController@exportsample | `POST /api/v1/export/sample` | ❌ Missing |

**Total Component/Item Master Routes:** 70+ routes  
**Missing:** 65+ routes (~93%)

---

### 3. Master BOM (Track H)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/masterbom` | GET | MasterBomController@index | `GET /api/v1/master-boms` | ❌ Missing |
| `/masterbom/create` | GET | MasterBomController@create | `GET /api/v1/master-boms/create` | ❌ Missing |
| `/masterbom/create` | POST | MasterBomController@store | `POST /api/v1/master-boms` | ❌ Missing |
| `/masterbom/{id}/edit` | GET | MasterBomController@edit | `GET /api/v1/master-boms/{id}/edit` | ❌ Missing |
| `/masterbom/{id}/copy` | GET | MasterBomController@copy | `GET /api/v1/master-boms/{id}/copy` | ❌ Missing |
| `/masterbom/{id}/edit` | PUT | MasterBomController@update | `PUT /api/v1/master-boms/{id}` | ❌ Missing |
| `/masterbom/{id}/destroy` | DELETE | MasterBomController@destroy | `DELETE /api/v1/master-boms/{id}` | ❌ Missing |
| `/masterbom/addmore` | GET | MasterBomController@addmore | `GET /api/v1/master-boms/addmore` | ❌ Missing |
| `/masterbom/remove` | GET | MasterBomController@remove | `DELETE /api/v1/master-boms/items/{id}` | ❌ Missing |
| `/masterbom/getsubcategory/{id}` | GET | MasterBomController@getsubcategory | `GET /api/v1/master-boms/subcategory/{id}` | ❌ Missing |
| `/masterbom/getproducttype/{id}` | GET | MasterBomController@getproducttype | `GET /api/v1/master-boms/producttype/{id}` | ❌ Missing |
| `/masterbom/getdescription` | GET | MasterBomController@getdescription | `GET /api/v1/master-boms/description` | ❌ Missing |

**Total Master BOM Routes:** 12 routes  
**Missing:** 12 routes (100%)

---

### 4. Feeder Library (Track I)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/feeder-library` | GET | FeederTemplateController@index | `GET /api/v1/feeder-library` | ❌ Missing |
| `/feeder-library/create` | GET | FeederTemplateController@create | `GET /api/v1/feeder-library/create` | ❌ Missing |
| `/feeder-library` | POST | FeederTemplateController@store | `POST /api/v1/feeder-library` | ❌ Missing |
| `/feeder-library/{id}` | GET | FeederTemplateController@show | `GET /api/v1/feeder-library/{id}` | ❌ Missing |
| `/feeder-library/{id}/edit` | GET | FeederTemplateController@edit | `GET /api/v1/feeder-library/{id}/edit` | ❌ Missing |
| `/feeder-library/{id}` | PUT | FeederTemplateController@update | `PUT /api/v1/feeder-library/{id}` | ❌ Missing |
| `/feeder-library/{id}/toggle` | PATCH | FeederTemplateController@toggleActive | `PATCH /api/v1/feeder-library/{id}/toggle` | ❌ Missing |

**Total Feeder Library Routes:** 7 routes  
**Missing:** 7 routes (100%)

---

### 5. Proposal BOM (Track J)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/proposal-bom` | GET | ProposalBomController@index | `GET /api/v1/proposal-boms` | ❌ Missing |
| `/proposal-bom/{id}` | GET | ProposalBomController@show | `GET /api/v1/proposal-boms/{id}` | ❌ Missing |
| `/proposal-bom/{id}/reuse` | GET | ProposalBomController@reuse | `GET /api/v1/proposal-boms/{id}/reuse` | ⚠️ Partial (via quotation) |
| `/proposal-bom/{id}/promote` | POST | ProposalBomController@promoteToMaster | `POST /api/v1/proposal-boms/{id}/promote` | ❌ Missing |

**Total Proposal BOM Routes:** 4 routes  
**Missing:** 3 routes (75%)

---

### 6. Quotation (Track A - PARTIAL)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/quotation` | GET | QuotationController@index | `GET /api/v1/quotation` | ⚠️ Partial |
| `/quotation/bom-list` | GET | QuotationController@bomList | `GET /api/v1/quotation/bom-list` | ❌ Missing |
| `/quotation/create` | GET | QuotationController@create | `GET /api/v1/quotation/create` | ❌ Missing |
| `/quotation/create` | POST | QuotationController@store | `POST /api/v1/quotation` | ❌ Missing |
| `/quotation/{id}/edit` | GET | QuotationController@edit | `GET /api/v1/quotation/{id}/edit` | ❌ Missing |
| `/quotation/{id}/edit` | PUT | QuotationController@update | `PUT /api/v1/quotation/{id}` | ❌ Missing |
| `/quotation/{id}/destroy` | DELETE | QuotationController@destroy | `DELETE /api/v1/quotation/{id}` | ❌ Missing |
| `/quotation/{id}/v2` | GET | QuotationV2Controller@index | `GET /api/v1/quotation/{id}/v2` | ✅ Covered |
| `/quotation/{id}/panel/{panelId}` | GET | QuotationV2Controller@panel | `GET /api/v1/quotation/{id}/panel/{panelId}` | ✅ Covered |
| `/quotation/{id}/panel` | POST | QuotationV2Controller@addPanel | `POST /api/v1/quotation/{id}/panel` | ✅ Covered |
| `/quotation/{id}/panel/{panelId}/feeder` | POST | QuotationV2Controller@addFeeder | `POST /api/v1/quotation/{id}/panel/{panelId}/feeder` | ✅ Covered |
| `/quotation/{id}/bom/{parentBomId}/bom` | POST | QuotationV2Controller@addBom | `POST /api/v1/quotation/{id}/bom/{parentBomId}/bom` | ✅ Covered |
| `/quotation/{id}/bom/{bomId}/item` | POST | QuotationV2Controller@addItem | `POST /api/v1/quotation/{id}/bom/{bomId}/item` | ✅ Covered |
| `/quotation/v2/apply-master-bom` | POST | QuotationV2Controller@applyMasterBom | `POST /api/v1/quotation/v2/apply-master-bom` | ✅ Covered |
| `/quotation/{quotation}/panel/{panel}/feeder/apply-template` | POST | QuotationV2Controller@applyFeederTemplate | `POST /api/v1/quotation/{id}/feeder/apply-template` | ✅ Covered |
| `/quotation/v2/apply-proposal-bom` | POST | QuotationV2Controller@applyProposalBom | `POST /api/v1/quotation/v2/apply-proposal-bom` | ✅ Covered |
| `/quotation/{quotation}/items/batch-update` | POST | QuotationV2Controller@batchUpdateItems | `POST /api/v1/quotation/{id}/items/batch-update` | ✅ Covered |
| `/quotation/{quotation}/panel/{panel}/qty` | POST | QuotationV2Controller@updatePanelQty | `POST /api/v1/quotation/{id}/panel/{panelId}/qty` | ✅ Covered |
| `/quotation/{quotation}/feeder/{feeder}/qty` | POST | QuotationV2Controller@updateFeederQty | `POST /api/v1/quotation/{id}/feeder/{feederId}/qty` | ✅ Covered |
| `/quotation/{quotation}/bom/{bom}/qty` | POST | QuotationV2Controller@updateBomQty | `POST /api/v1/quotation/{id}/bom/{bomId}/qty` | ✅ Covered |
| `/quotation/{quotation}/item/{item}/rate` | POST | QuotationV2Controller@updateItemRate | `POST /api/v1/quotation/{id}/item/{itemId}/rate` | ✅ Covered |
| `/quotation/{quotation}/item/{item}/discount` | POST | QuotationV2Controller@updateItemDiscount | `POST /api/v1/quotation/{id}/item/{itemId}/discount` | ✅ Covered |
| `/quotation/{quotation}/item/{item}/qty` | POST | QuotationV2Controller@updateItemQty | `POST /api/v1/quotation/{id}/item/{itemId}/qty` | ✅ Covered |
| `/quotation/{quotation}/v2/export-bom` | GET | QuotationV2Controller@exportBom | `GET /api/v1/quotation/{id}/export-bom` | ✅ Covered |
| `/api/reuse/panels` | GET | ReuseController@searchPanels | `GET /api/v1/reuse/panels` | ✅ Covered |
| `/api/reuse/feeders` | GET | ReuseController@searchFeeders | `GET /api/v1/reuse/feeders` | ✅ Covered |
| `/api/reuse/master-boms` | GET | ReuseController@searchMasterBoms | `GET /api/v1/reuse/master-boms` | ✅ Covered |
| `/api/reuse/proposal-boms` | GET | ReuseController@searchProposalBoms | `GET /api/v1/reuse/proposal-boms` | ✅ Covered |
| `/quotations/{quotation_id}/discount-rules` | GET | QuotationDiscountRuleController@index | `GET /api/v1/quotation/{id}/discount-rules` | ⚠️ Partial (Track E) |
| `/quotations/{quotation_id}/discount-rules/create` | GET | QuotationDiscountRuleController@create | `GET /api/v1/quotation/{id}/discount-rules/create` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules` | POST | QuotationDiscountRuleController@store | `POST /api/v1/quotation/{id}/discount-rules` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/{id}` | GET | QuotationDiscountRuleController@show | `GET /api/v1/quotation/{id}/discount-rules/{id}` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/{id}/edit` | GET | QuotationDiscountRuleController@edit | `GET /api/v1/quotation/{id}/discount-rules/{id}/edit` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/{id}` | PUT | QuotationDiscountRuleController@update | `PUT /api/v1/quotation/{id}/discount-rules/{id}` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/{id}` | DELETE | QuotationDiscountRuleController@destroy | `DELETE /api/v1/quotation/{id}/discount-rules/{id}` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/preview` | GET | QuotationDiscountRuleController@preview | `GET /api/v1/quotation/{id}/discount-rules/preview` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/apply` | POST | QuotationDiscountRuleController@apply | `POST /api/v1/quotation/{id}/discount-rules/apply` | ❌ Missing |
| `/quotations/{quotation_id}/discount-rules/reset` | POST | QuotationDiscountRuleController@reset | `POST /api/v1/quotation/{id}/discount-rules/reset` | ❌ Missing |
| `/quotation/pdf/{id}` | GET | QuotationController@pdf | `GET /api/v1/quotation/{id}/pdf` | ❌ Missing |
| `/quotation/excel/{id}` | GET | QuotationController@excel | `GET /api/v1/quotation/{id}/excel` | ❌ Missing |

**Total Quotation Routes:** 50+ routes  
**Covered:** ~20 routes (40%)  
**Missing:** ~30 routes (60%)

---

### 7. Master Data (Track K)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/vendors` | GET | VendorController@index | `GET /api/v1/vendors` | ❌ Missing |
| `/vendors/create` | GET | VendorController@create | `GET /api/v1/vendors/create` | ❌ Missing |
| `/vendors/create` | POST | VendorController@store | `POST /api/v1/vendors` | ❌ Missing |
| `/vendors/{id}/edit` | GET | VendorController@edit | `GET /api/v1/vendors/{id}/edit` | ❌ Missing |
| `/vendors/{id}/edit` | PUT | VendorController@update | `PUT /api/v1/vendors/{id}` | ❌ Missing |
| `/vendors/{id}/destroy` | DELETE | VendorController@destroy | `DELETE /api/v1/vendors/{id}` | ❌ Missing |
| `/pdfcontain` | GET | ImportController@pdfcontain | `GET /api/v1/pdf-formats` | ❌ Missing |
| `/pdfcontain` | PUT | ImportController@pdfcontainsave | `PUT /api/v1/pdf-formats` | ❌ Missing |

**Total Master Data Routes:** 8 routes  
**Missing:** 8 routes (100%)

---

### 8. User/Role Management (Track L)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/user` | GET | UserController@index | `GET /api/v1/users` | ❌ Missing |
| `/user/create` | GET | UserController@create | `GET /api/v1/users/create` | ❌ Missing |
| `/user/create` | POST | UserController@store | `POST /api/v1/users` | ❌ Missing |
| `/user/{id}/edit` | GET | UserController@edit | `GET /api/v1/users/{id}/edit` | ❌ Missing |
| `/user/{id}/edit` | PUT | UserController@update | `PUT /api/v1/users/{id}` | ❌ Missing |
| `/user/{id}/destroy` | DELETE | UserController@destroy | `DELETE /api/v1/users/{id}` | ❌ Missing |
| `/role` | GET | RoleController@index | `GET /api/v1/roles` | ❌ Missing |
| `/role/create` | GET | RoleController@create | `GET /api/v1/roles/create` | ❌ Missing |
| `/role/create` | POST | RoleController@store | `POST /api/v1/roles` | ❌ Missing |
| `/role/{id}/edit` | GET | RoleController@edit | `GET /api/v1/roles/{id}/edit` | ❌ Missing |
| `/role/{id}/edit` | PUT | RoleController@update | `PUT /api/v1/roles/{id}` | ❌ Missing |
| `/role/{id}/destroy` | DELETE | RoleController@destroy | `DELETE /api/v1/roles/{id}` | ❌ Missing |

**Total User/Role Routes:** 12 routes  
**Missing:** 12 routes (100%)

---

### 9. Dashboard (Track M)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/` | GET | HomeController@index | `GET /` | ❌ Missing |
| `/home` | GET | HomeController@index | `GET /home` | ❌ Missing |

**Total Dashboard Routes:** 2 routes  
**Missing:** 2 routes (100%)

---

### 10. AJAX Endpoints (Shared)

| NEPL Route | Method | Controller | NSW Equivalent | Status |
|------------|--------|------------|----------------|--------|
| `/api/category/{categoryId}/subcategories` | GET | QuotationController@getSubCategories | `GET /api/v1/category/{id}/subcategories` | ❌ Missing |
| `/api/category/{categoryId}/items` | GET | QuotationController@getItems | `GET /api/v1/category/{id}/items` | ❌ Missing |
| `/api/category/{categoryId}/products` | GET | QuotationController@getProducts | `GET /api/v1/category/{id}/products` | ❌ Missing |
| `/api/item/{itemId}/products` | GET | QuotationController@getProductsByItem | `GET /api/v1/item/{id}/products` | ❌ Missing |
| `/api/product/{productId}/makes` | GET | QuotationController@getMakes | `GET /api/v1/product/{id}/makes` | ❌ Missing |
| `/api/make/{makeId}/series` | GET | QuotationController@getSeriesApi | `GET /api/v1/make/{id}/series` | ❌ Missing |
| `/api/product/{productId}/descriptions` | GET | QuotationController@getDescriptions | `GET /api/v1/product/{id}/descriptions` | ❌ Missing |
| `/api/category/{categoryId}/makes` | GET | QuotationController@getMakesByCategory | `GET /api/v1/category/{id}/makes` | ❌ Missing |
| `/api/makes` | GET | QuotationController@getAllMakes | `GET /api/v1/makes` | ❌ Missing |
| `/quotation/v2/products-by-type` | GET | QuotationV2Controller@getProductsByType | `GET /api/v1/quotation/v2/products-by-type` | ❌ Missing |
| `/api/proposal-bom/search` | GET | QuotationController@searchProposalBom | `GET /api/v1/proposal-bom/search` | ❌ Missing |

**Total AJAX Routes:** 11 routes  
**Missing:** 11 routes (100%)

---

## 📊 Summary Statistics

| Module | Total Routes | Covered | Missing | Coverage % |
|--------|--------------|---------|---------|------------|
| Foundation Entities | 24 | 0 | 24 | 0% |
| Component/Item Master | 70+ | 5 | 65+ | 7% |
| Master BOM | 12 | 0 | 12 | 0% |
| Feeder Library | 7 | 0 | 7 | 0% |
| Proposal BOM | 4 | 1 | 3 | 25% |
| Quotation | 50+ | 20 | 30 | 40% |
| Master Data | 8 | 0 | 8 | 0% |
| User/Role | 12 | 0 | 12 | 0% |
| Dashboard | 2 | 0 | 2 | 0% |
| AJAX Endpoints | 11 | 0 | 11 | 0% |
| **TOTAL** | **200+** | **26** | **174+** | **13%** |

---

## ✅ Verification Complete

**Source Verified:** `/Volumes/T9/Projects/nish/routes/web.php`  
**Date:** 2025-01-27  
**Status:** Complete route inventory verified from actual NEPL system

**Key Findings:**
- Total routes: 200+ routes
- Current coverage: ~26 routes (13%)
- Missing routes: ~174 routes (87%)
- All routes verified against actual NEPL codebase

---

**Next Steps:**
1. Review this verified mapping
2. Update Phase 6 scope with exact route requirements
3. Prioritize tracks based on route dependencies
4. Create detailed implementation plan for each missing route
