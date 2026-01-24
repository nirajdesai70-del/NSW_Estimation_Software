# Phase 6 Complete Replication Plan
## Full NEPL System → NSW Replication Mapping

**Date:** 2025-01-27  
**Status:** COMPREHENSIVE REPLICATION PLAN  
**Purpose:** Map ALL NEPL features to NSW Phase 6+ implementation

---

## 🎯 Executive Summary

**Goal:** Replicate the **complete NEPL Estimation Software** from `project/nish` with all modifications into NSW system.

**Current Phase 6 Status:** Only covers ~30% of NEPL functionality (Quotation V2, partial BOM, partial Catalog, Costing)

**Required:** Complete replication of all 8 core modules + all workflows + all features

---

## 📊 NEPL System Inventory (VERIFIED FROM ACTUAL SYSTEM)

### Module Breakdown (Verified from `/Volumes/T9/Projects/nish/routes/web.php`)

| Module | Routes | Controllers | Key Features | Phase 6 Status |
|--------|--------|-------------|--------------|----------------|
| **Component/Item Master** | 60+ | 11 controllers | Categories, Subcategories, Items, Products, Makes, Series, Attributes, Pricing, Import/Export, Catalog Health | ❌ **NOT COVERED** |
| **Quotation** | 80+ | 3 controllers | Legacy + V2, Discount Rules, Reports, AJAX endpoints, Reuse | ⚠️ **PARTIAL** (V2 only) |
| **Master BOM** | 12 | 1 controller | CRUD, workflows, AJAX lookups, copy | ❌ **NOT COVERED** |
| **Feeder Library** | 7 | 1 controller | CRUD, toggle active | ❌ **NOT COVERED** |
| **Proposal BOM** | 4 | 1 controller | List, show, reuse, promote | ❌ **NOT COVERED** |
| **Project** | 6 | 1 controller | Projects CRUD | ❌ **NOT COVERED** |
| **Client/Contact** | 12 | 2 controllers | Clients, Contacts CRUD | ❌ **NOT COVERED** |
| **Master** | 7 | 2 controllers | Organization, Vendor, PDF container | ❌ **NOT COVERED** |
| **Employee/Role** | 12 | 2 controllers | Users, Roles, Permissions | ❌ **NOT COVERED** |
| **Dashboard** | 2 | 1 controller | Home, Statistics | ❌ **NOT COVERED** |
| **Import/Export** | 6 | 1 controller | Catalog import, export sample | ⚠️ **PARTIAL** (Track B) |
| **Security** | 0 | Middleware | Auth, Authorization, CSRF | ⚠️ **PARTIAL** |

**Total Routes:** ~200+ routes across 11 modules  
**Phase 6 Coverage:** ~30 routes (Quotation V2, partial Catalog, Costing)  
**Gap:** ~170 routes missing (~85% of system)

### Actual Controllers Found in NEPL System

**Component/Item Master:**
- `CategoryController`
- `SubCategoryController`
- `ItemController` (Product Types)
- `MakeController`
- `SeriesController`
- `AttributeController`
- `CategoryAttributeController`
- `GenericController` (L1 Products)
- `ProductController` (L2 Products)
- `PriceController`
- `ImportController`
- `CatalogHealthController`
- `CatalogCleanupController`

**Quotation:**
- `QuotationController` (Legacy)
- `QuotationV2Controller` (V2)
- `QuotationDiscountRuleController`
- `QuotationDiscountRuleTestController`
- `ReuseController`

**BOM Management:**
- `MasterBomController`
- `FeederTemplateController`
- `ProposalBomController`

**Project/Client:**
- `ProjectController`
- `ClientController`
- `ContactController`

**Master Data:**
- `OrganizationController`
- `VendorController`

**User Management:**
- `UserController`
- `RoleController`

**Other:**
- `HomeController`
- `CronController`

---

## 🔍 Complete Feature Mapping

### 1. Foundation Entities (Track F - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Organizations** | `/organization/*` | `organizations` table | ❌ Missing | P0 |
| **Customers** | `/client/*` | `customers` table | ❌ Missing | P0 |
| **Contacts** | `/contact/*` | `contacts` table | ❌ Missing | P0 |
| **Projects** | `/project/*` | `projects` table | ❌ Missing | P0 |

**Required Work:**
- Track F: Foundation Entities Management (3-4 weeks, 20 tasks)
- API endpoints for all CRUD operations
- UI for all CRUD operations
- Integration with quotation creation

---

### 2. Component/Item Master Module (Track G - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Categories** | `/category/*` | `categories` table | ❌ Missing | P0 |
| **Subcategories** | `/subcategory/*` | `subcategories` table | ❌ Missing | P0 |
| **Product Types/Items** | `/product-type/*` | `product_types` table | ❌ Missing | P0 |
| **Makes** | `/make/*` | `makes` table | ❌ Missing | P0 |
| **Series** | `/series/*` | `series` table | ❌ Missing | P0 |
| **Attributes** | `/attribute/*` | `attributes` table | ❌ Missing | P0 |
| **Category Attributes** | `/category-attribute/*` | `category_attributes` table | ❌ Missing | P0 |
| **Generic Products (L1)** | `/generic/*` | `l1_intent_lines` | ❌ Missing | P0 |
| **Specific Products (L2)** | `/product/*` | `catalog_skus` | ⚠️ Partial (Catalog import only) | P0 |
| **Pricing** | `/price/*` | `sku_prices` | ⚠️ Partial (Pricing import only) | P0 |
| **Import/Export** | `/import*`, `/export*` | Catalog import UI | ⚠️ Partial (Track B) | P1 |
| **Catalog Health** | `/catalog-health/*` | - | ❌ Missing | P2 |
| **Catalog Cleanup** | `/catalog-cleanup/*` | - | ❌ Missing | P2 |

**Required Work:**
- Track G: Component/Item Master Management (4-5 weeks, ~40 tasks)
- Full CRUD for all master data entities
- L1/L2 product management
- Attribute management
- Pricing management
- Import/Export workflows
- Catalog health/cleanup tools

---

### 3. Master BOM Module (Track H - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Master BOM List** | `/masterbom` | `master_boms` table | ❌ Missing | P0 |
| **Create Master BOM** | `/masterbom/create` | Master BOM creation | ❌ Missing | P0 |
| **Edit Master BOM** | `/masterbom/{id}/edit` | Master BOM editing | ❌ Missing | P0 |
| **Copy Master BOM** | `/masterbom/{id}/copy` | Master BOM copy | ❌ Missing | P0 |
| **Add BOM Items** | `/masterbom/addmore` | Master BOM items | ❌ Missing | P0 |
| **Remove BOM Items** | `/masterbom/remove` | Master BOM items | ❌ Missing | P0 |
| **AJAX Lookups** | `/masterbom/get*` | Product lookups | ❌ Missing | P0 |

**Required Work:**
- Track H: Master BOM Management (3-4 weeks, ~25 tasks)
- Full CRUD for Master BOMs
- Master BOM item management
- L1 product selection
- Copy/reuse workflows
- Integration with quotation creation

---

### 4. Feeder Library Module (Track I - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Feeder List** | `/feeder-library` | Feeder templates | ❌ Missing | P0 |
| **Create Feeder** | `/feeder-library/create` | Feeder creation | ❌ Missing | P0 |
| **Edit Feeder** | `/feeder-library/{id}/edit` | Feeder editing | ❌ Missing | P0 |
| **Show Feeder** | `/feeder-library/{id}` | Feeder details | ❌ Missing | P0 |
| **Toggle Active** | `/feeder-library/{id}/toggle` | Feeder status | ❌ Missing | P0 |

**Required Work:**
- Track I: Feeder Library Management (2-3 weeks, ~15 tasks)
- Full CRUD for Feeder templates
- Feeder structure management
- Active/inactive status
- Integration with quotation creation

---

### 5. Proposal BOM Module (Track J - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Proposal BOM List** | `/proposal-bom` | Proposal BOMs | ❌ Missing | P0 |
| **Show Proposal BOM** | `/proposal-bom/{id}` | Proposal BOM details | ❌ Missing | P0 |
| **Reuse Proposal BOM** | `/proposal-bom/{id}/reuse` | Proposal BOM reuse | ⚠️ Partial (via quotation) | P0 |
| **Promote to Master** | `/proposal-bom/{id}/promote` | Promote workflow | ❌ Missing | P1 |

**Required Work:**
- Track J: Proposal BOM Management (2-3 weeks, ~15 tasks)
- Proposal BOM list/view
- Proposal BOM reuse workflows
- Promote to Master BOM
- Integration with quotation creation

---

### 6. Quotation Module (Track A - PARTIAL)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Quotation List** | `/quotation` | Quotation list | ⚠️ Partial | P0 |
| **Create Quotation** | `/quotation/create` | Quotation creation | ❌ Missing | P0 |
| **Edit Quotation** | `/quotation/{id}/edit` | Quotation editing | ❌ Missing | P0 |
| **Quotation V2** | `/quotation/{id}/v2` | Quotation V2 UI | ✅ Covered (Track A) | P0 |
| **Panel Management** | `/quotation/{id}/panel/*` | Panel CRUD | ✅ Covered (Track A) | P0 |
| **Feeder Management** | `/quotation/{id}/feeder/*` | Feeder CRUD | ✅ Covered (Track A) | P0 |
| **BOM Management** | `/quotation/{id}/bom/*` | BOM CRUD | ✅ Covered (Track A) | P0 |
| **Item Management** | `/quotation/{id}/item/*` | Item CRUD | ✅ Covered (Track A) | P0 |
| **Discount Rules** | `/quotation/{id}/discount` | Discount editor | ⚠️ Partial (Track E) | P0 |
| **Reports/PDF** | `/quotation/{id}/pdf` | PDF generation | ❌ Missing | P1 |
| **Reuse Workflows** | `/api/reuse/*` | Copy workflows | ✅ Covered (Track A-R) | P0 |

**Required Work:**
- Complete quotation creation/edit UI
- PDF generation
- Additional reports
- Legacy quotation support (if needed)

---

### 7. Project Module (Track F - PARTIAL)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Project List** | `/project` | Project list | ❌ Missing | P0 |
| **Create Project** | `/project/create` | Project creation | ❌ Missing | P0 |
| **Edit Project** | `/project/{id}/edit` | Project editing | ❌ Missing | P0 |
| **Client Management** | `/client/*` | Customer management | ❌ Missing (Track F) | P0 |
| **Contact Management** | `/contact/*` | Contact management | ❌ Missing (Track F) | P0 |

**Required Work:**
- Track F: Foundation Entities (includes Projects, Clients, Contacts)
- Full CRUD for all entities
- Integration with quotations

---

### 8. Master Module (Track K - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Organization** | `/organization/*` | Organizations | ❌ Missing (Track F) | P0 |
| **Vendor** | `/vendors/*` | Vendors | ❌ Missing | P1 |
| **PDF Container** | `/pdfcontain/*` | PDF formats | ❌ Missing | P1 |

**Required Work:**
- Track K: Master Data Management (2-3 weeks, ~15 tasks)
- Vendor management
- PDF format configuration
- Integration with quotations

---

### 9. Employee/Role Module (Track L - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **User Management** | `/user/*` | Users | ❌ Missing | P0 |
| **Role Management** | `/role/*` | Roles | ❌ Missing | P0 |
| **Permissions** | Middleware | Permissions | ⚠️ Partial (Track C) | P0 |

**Required Work:**
- Track L: User & Role Management (2-3 weeks, ~20 tasks)
- Full CRUD for users
- Full CRUD for roles
- Permission management
- Integration with Track C (RBAC)

---

### 10. Dashboard Module (Track M - NEW)

| NEPL Feature | NEPL Route | NSW Equivalent | Phase 6 Status | Priority |
|--------------|------------|----------------|----------------|----------|
| **Home Dashboard** | `/` or `/home` | Dashboard | ❌ Missing | P0 |
| **Statistics** | Dashboard widgets | Statistics | ❌ Missing | P0 |
| **Recent Activities** | Dashboard widgets | Activity feed | ❌ Missing | P1 |

**Required Work:**
- Track M: Dashboard (1-2 weeks, ~10 tasks)
- Home dashboard UI
- Statistics widgets
- Recent activities
- Navigation structure

---

## 📋 Complete Task Breakdown

### New Tracks Required

| Track | Module | Duration | Tasks | Priority |
|-------|--------|----------|-------|----------|
| **Track F** | Foundation Entities | 3-4 weeks | 20 | P0 |
| **Track G** | Component/Item Master | 4-5 weeks | 40 | P0 |
| **Track H** | Master BOM | 3-4 weeks | 25 | P0 |
| **Track I** | Feeder Library | 2-3 weeks | 15 | P0 |
| **Track J** | Proposal BOM | 2-3 weeks | 15 | P0 |
| **Track K** | Master (Vendor/PDF) | 2-3 weeks | 15 | P1 |
| **Track L** | User/Role Management | 2-3 weeks | 20 | P0 |
| **Track M** | Dashboard | 1-2 weeks | 10 | P0 |

**Total Additional:** 18-25 weeks, ~160 tasks

### Existing Tracks (Phase 6)

| Track | Module | Duration | Tasks | Status |
|-------|--------|----------|-------|--------|
| **Track A** | Quotation UI | 6 weeks | 33 | ✅ In Progress |
| **Track A-R** | Reuse & Legacy Parity | 3 weeks | 7 | ✅ Planned |
| **Track B** | Catalog Tooling | 4 weeks | 16 | ✅ Planned |
| **Track C** | Operational Readiness | 2 weeks | 12 | ✅ Planned |
| **Track D0** | Costing Engine | 4 weeks | 14 | ✅ Planned |
| **Track D** | Costing & Reporting | 4 weeks | 20 | ✅ Planned |
| **Track E** | Canon Implementation | 6 weeks | 29 | ✅ Planned |

**Total Existing:** 29 weeks, ~131 tasks

---

## 🗓️ Revised Phase 6 Timeline

### Current Phase 6: 10-12 weeks
### Revised Phase 6 (Complete Replication): 28-37 weeks

**Breakdown:**
- Existing Tracks: 29 weeks
- New Tracks (P0 only): 18-25 weeks
- Integration & Stabilization: 2 weeks
- Buffer: 2 weeks

**Total:** 51-58 weeks (~12-14 months)

---

## 🎯 Priority-Based Phasing

### Phase 6.1: Foundation (Weeks 1-8)
- Track F: Foundation Entities (3-4 weeks)
- Track L: User/Role Management (2-3 weeks)
- Track M: Dashboard (1-2 weeks)
- Track E: Canon Implementation (6 weeks) - Parallel

### Phase 6.2: Master Data (Weeks 9-18)
- Track G: Component/Item Master (4-5 weeks)
- Track H: Master BOM (3-4 weeks)
- Track I: Feeder Library (2-3 weeks)
- Track J: Proposal BOM (2-3 weeks)
- Track K: Master (Vendor/PDF) (2-3 weeks) - Lower priority

### Phase 6.3: Quotation & Costing (Weeks 19-29)
- Track A: Quotation UI (6 weeks)
- Track A-R: Reuse & Legacy Parity (3 weeks)
- Track B: Catalog Tooling (4 weeks)
- Track D0: Costing Engine (4 weeks)
- Track D: Costing & Reporting (4 weeks)
- Track C: Operational Readiness (2 weeks)

### Phase 6.4: Integration & Stabilization (Weeks 30-32)
- End-to-end integration
- Bug fixes
- UX polish
- Documentation

---

## ✅ Verification Checklist

### Module Coverage

- [ ] Foundation Entities (Organizations, Customers, Contacts, Projects)
- [ ] Component/Item Master (Categories, Subcategories, Items, Products, Makes, Series, Attributes, Pricing)
- [ ] Master BOM (CRUD, workflows, reuse)
- [ ] Feeder Library (CRUD, templates)
- [ ] Proposal BOM (List, view, reuse, promote)
- [ ] Quotation (Legacy + V2, all workflows)
- [ ] Project (Full CRUD)
- [ ] Master (Organization, Vendor, PDF)
- [ ] Employee/Role (Users, Roles, Permissions)
- [ ] Dashboard (Home, Statistics, Navigation)

### Feature Coverage

- [ ] All CRUD operations for all entities
- [ ] All workflows (create, edit, copy, reuse, promote)
- [ ] All import/export functionality
- [ ] All reports and PDF generation
- [ ] All AJAX endpoints
- [ ] All search/filter functionality
- [ ] All validation and error handling
- [ ] All audit trails

---

## 📝 Recommendations

### Option 1: Complete Replication (Recommended)
- Add all 8 new tracks (F-M)
- Complete replication of NEPL system
- Timeline: 51-58 weeks
- **Pros:** Complete system, no gaps
- **Cons:** Long timeline

### Option 2: Phased Approach
- Phase 6: Core functionality (Tracks A-E, F, L, M)
- Phase 7: Master Data (Tracks G-K)
- **Pros:** Faster initial delivery
- **Cons:** Incomplete system in Phase 6

### Option 3: Minimal Viable Product
- Phase 6: Only critical paths (Quotation creation → Costing)
- Defer all master data management to Phase 7
- **Pros:** Fastest delivery
- **Cons:** Manual workarounds required

---

## 🔗 Related Documents

- **Gap Analysis:** `PHASE_6_SCOPE_GAP_ANALYSIS.md`
- **Scope Review:** `PHASE_6_SCOPE_REVIEW_SUMMARY.md`
- **NEPL Reference:** `project/nish/NISH_SYSTEM_REFERENCE.md`
- **Route Map:** `trace/phase_2/ROUTE_MAP.md`
- **Feature Map:** `trace/phase_2/FEATURE_CODE_MAP.md`

---

**Conclusion:** To replicate the complete NEPL system, Phase 6 needs to expand from 10-12 weeks to 28-37 weeks (or 51-58 weeks for complete replication including all features). This requires adding 8 new tracks (F-M) with ~160 additional tasks.
