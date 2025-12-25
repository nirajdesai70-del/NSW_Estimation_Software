# Post-Phase 5 Implementation Roadmap

**Version:** 1.0  
**Date:** December 18, 2025  
**Status:** 📋 Planning - Integrated Pending Upgrades  
**Purpose:** Comprehensive implementation plan for all pending upgrades after Phase 5 completion

---

## 🎯 Overview

This document integrates all pending upgrades into a structured implementation roadmap that can be executed after Phase 5 (Data Dictionary & Schema Design) completes. All upgrades are organized by priority and implementation phase to ensure nothing is missed and work proceeds efficiently.

**Prerequisites:**
- ✅ Phase 5 Step 1: NSW Canonical Data Dictionary (FROZEN)
- ✅ Phase 5 Step 2: NSW Canonical Schema (FROZEN)

**Total Estimated Effort:** ~150-200 hours (code/UI) + ~40-50 days (costing/AI)

---

## 📊 Implementation Phases

### Phase 5.1: Critical Foundation (HIGH Priority)
**Duration:** ~2-3 weeks  
**Effort:** ~40-50 hours

### Phase 5.2: Core Enhancements (HIGH Priority)
**Duration:** ~3-4 weeks  
**Effort:** ~50-60 hours

### Phase 5.3: Advanced Features (MEDIUM Priority)
**Duration:** ~4-6 weeks  
**Effort:** ~60-80 hours

### Phase 5.4: Costing Engine (HIGH Priority)
**Duration:** ~4-5 weeks  
**Effort:** ~19-28 days

### Phase 5.5: AI Implementation (MEDIUM-HIGH Priority)
**Duration:** ~5-7 weeks  
**Effort:** ~25-35 days

### Phase 5.6: Long-term Upgrades (LOW Priority)
**Duration:** ~6-8 weeks  
**Effort:** ~65-90 hours

---

## 🔴 PHASE 5.1: Critical Foundation (HIGH Priority)

**Status:** ⏸️ PENDING  
**Priority:** HIGH  
**Duration:** 2-3 weeks  
**Effort:** ~40-50 hours

### 1.1 Validation Guardrails Testing ⚠️
**Status:** Implementation Complete, Testing Pending  
**Effort:** 4-6 hours  
**Priority:** HIGH

**All 7 Guardrails Implemented, Testing Needed:**
- [ ] Test G1: Master BOM rejects ProductId
- [ ] Test G2: Production BOM requires ProductId
- [ ] Test G3: IsPriceMissing normalizes Amount
- [ ] Test G4: RateSource consistency
- [ ] Test G5: UNRESOLVED normalizes values
- [ ] Test G6: FIXED_NO_DISCOUNT forces Discount=0
- [ ] Test G7: All discounts are percentage-based

**Implementation Notes:**
- Guardrails are already implemented in code
- Need comprehensive test suite
- Test with edge cases and invalid inputs
- Document test results

---

### 1.2 BOM Instance Identity Enhancement
**Status:** ⏸️ PENDING  
**Effort:** 6-8 hours  
**Priority:** HIGH

**Database Migrations:**
- [ ] Create migration: Add `OriginMasterBomId` column to `quotation_sale_boms`
- [ ] Create migration: Add `OriginMasterBomVersion` column to `quotation_sale_boms`
- [ ] Create migration: Add `InstanceSequenceNo` column to `quotation_sale_boms`
- [ ] Run migration: `php artisan migrate`

**Model Updates:**
- [ ] Add fields to `$fillable` in `QuotationSaleBom.php`
- [ ] Add optional `originMasterBom()` relationship

**Service Updates:**
- [ ] Enhance `generateBomName()` to accept `$instanceSequenceNo`
- [ ] Ensure sequence increments: BOM-01, BOM-02, etc.
- [ ] Check existing names to avoid duplicates

**Controller Updates:**
- [ ] Store `OriginMasterBomId` when Master BOM applied
- [ ] Set `InstanceSequenceNo` on BOM creation
- [ ] Update `applyMasterBom()` method

**Testing:**
- [ ] Test BOM creation with sequence
- [ ] Test Master BOM application stores origin
- [ ] Verify unique names generated

---

### 1.3 Add Component Button Fix
**Status:** ⏸️ PENDING  
**Effort:** 2-3 hours  
**Priority:** HIGH

**Files Affected:**
- `resources/views/quotation/steppopup.blade.php`
- `resources/views/quotation/linepopup.blade.php`
- `resources/views/quotation/step.blade.php`

**Requirements:**
- [ ] Add "Add Component" button to `steppopup.blade.php` (existing panels)
- [ ] Add "Add Component" button to `linepopup.blade.php` (new panels)
- [ ] Create `addComponentDirectly()` function in `step.blade.php`
- [ ] Button should create empty BOM and allow adding components
- [ ] Follow existing button patterns and styling

**Note:** This was previously fixed but removed during restoration. Needs to be re-implemented.

---

### 1.4 V2 Costing UI Improvements - Critical Fixes
**Status:** ⏸️ PENDING  
**Effort:** 4-6 hours  
**Priority:** HIGH

**Step 3.1: Fix Expand/Collapse (HIGH Priority)**
- [ ] Implement localStorage state tracking
- [ ] Store expanded BOM/Feeder IDs in Set
- [ ] Save to localStorage on expand/collapse
- [ ] Restore from localStorage on page load
- [ ] Fix bug where all items expand/collapse together

**Step 3.2: Fix Column Hide/Show (HIGH Priority)**
- [ ] Review current column hide/show implementation
- [ ] Fix bug where hidden columns still show
- [ ] Fix bug where table breaks when columns hidden
- [ ] Ensure critical columns (Qty, Rate, Total) cannot be hidden
- [ ] Fix state persistence in localStorage

---

## 🟡 PHASE 5.2: Core Enhancements (HIGH Priority)

**Status:** ⏸️ PENDING  
**Priority:** HIGH  
**Duration:** 3-4 weeks  
**Effort:** ~50-60 hours

### 2.1 Master BOM vs Proposal BOM Enhancements
**Status:** ⏸️ PENDING  
**Effort:** 15-20 hours  
**Priority:** MEDIUM-HIGH

#### Phase 1: Terminology & Documentation (1-2 hours)
- [ ] Create `V2_TERMINOLOGY.md` document
- [ ] Add code comments explaining Master BOM vs Proposal BOM
- [ ] Update UI labels ("Use Master BOM" instead of "Master BOM")
- [ ] Document "Always Copy" rule

#### Phase 2: Modification Tracking (2-3 hours)
- [ ] Create migration for:
  - `IsModified` (boolean)
  - `ModifiedBy` (user ID)
  - `ModifiedAt` (timestamp)
  - `OriginMasterBomId` (reference)
  - `OriginMasterVersion` (string)
- [ ] Update `QuotationSaleBom` model
- [ ] Update BOM creation logic to set tracking fields
- [ ] Update BOM edit logic to mark as modified
- [ ] Create `markBomAsModified()` helper method

#### Phase 3: Orchestration Function (3-4 hours)
- [ ] Create `BomChangeOrchestrator` service
- [ ] Implement `applyProposalBomChange()` method
- [ ] Refactor existing operations to use orchestrator:
  - `addItem()`
  - `updateItemQty()`
  - `updateItemRate()`
  - `updateItemDiscount()`
  - `deleteBom()`
  - `itemremove()`
  - `batchUpdateItems()`
- [ ] Ensure all changes go through orchestrator

#### Phase 4: Promotion Feature (1-2 hours remaining)
**Status:** ⚠️ PARTIALLY DONE (Backend done, UI missing)
- [ ] "Promote to Master BOM" button in V2 panel BOM header
- [ ] Button in `_bom.blade.php` (similar to "Edit BOM" button)
- [ ] Modal or confirmation for promotion

#### Phase 5: Complete Bulk Operations (4-5 hours)
**Status:** Structure ready, modal not implemented
- [ ] `_multi_edit_modal.blade.php` - Full multi-edit UI
- [ ] `openMultiEditModal()` function - Currently placeholder
- [ ] Bulk operations in modal:
  - Set quantity (all selected)
  - Set make/series (all selected)
  - Apply discount % (all selected)
  - Replace component (all selected)
- [ ] Validation for bulk operations

#### Phase 6: Audit Trail (1-2 hours)
- [ ] Add audit logging in `BomChangeOrchestrator` (when created)
- [ ] Log: who, what, when, before/after values
- [ ] Optional: Create `bom_change_logs` table
- [ ] Optional: Create audit log view page

---

### 2.2 Sprint-4 UI Components (Discount Rules)
**Status:** ⏸️ PENDING (Backend 100% Complete, UI 0%)  
**Effort:** 25-35 hours  
**Priority:** HIGH

**Reference:** `SPRINT4_UI_TODO_LIST.md`

#### Core UI Components (12-16 hours)
- [ ] **S4-07: Discount Rules Table** (4-6 hours)
  - Use `nepl-standard-table` class
  - Display all discount rules for quotation
  - Show columns: Rule Name, Scope Type, Discount (%), Priority, Apply On, Status, Actions
  - Actions: Edit, Delete, Toggle Status
  - Empty state message when no rules

- [ ] **S4-08: Add/Edit Rule Modal** (5-7 hours)
  - Modal form with all rule fields
  - Scope Type dropdown (GLOBAL, MAKE, MAKE_SERIES, PRODUCT_TYPE, PRODUCT)
  - Conditional fields (Make/Series/Product based on scope)
  - Select2 for all dropdowns
  - Make → Series dependency (AJAX load)
  - Product selector: searchable, minimum 2 characters
  - Form validation (client-side + server-side)
  - AJAX form submission

- [ ] **S4-09: Preview Modal** (3-4 hours)
  - Show preview summary
  - Show sample matches (first 10-20 items)
  - Show FIXED items sample (if any)
  - Override manual checkbox
  - Apply button with confirmation

#### Action Buttons (4-6 hours)
- [ ] **S4-10: Apply Rules Action** (2-3 hours)
  - "Apply Rules" button in discount rules panel
  - Confirmation dialog
  - Success/error notifications
  - Refresh table after apply

- [ ] **S4-15: Reset Button** (2-3 hours)
  - "Reset Last Apply" button
  - Only visible when audit log exists
  - Confirmation dialog
  - Success/error notifications

#### Dropdown Selectors (4-6 hours)
- [ ] **S4-16: Make Selector** (1 hour)
  - Select2 dropdown for Make selection
  - Searchable dropdown
  - Load from: `GET /quotation/{id}/discount-rules/lookup/makes`

- [ ] **S4-17: Series Selector** (1-2 hours)
  - Select2 dropdown for Series selection
  - Dependency: Only enabled when Make is selected
  - AJAX Loading: Load series when Make changes
  - Load from: `GET /quotation/{id}/discount-rules/lookup/series?make_id={id}`

- [ ] **S4-18: Product Type Selector** (1 hour)
  - Select2 dropdown for Product Type selection
  - Load from: `GET /quotation/{id}/discount-rules/lookup/product-types`

- [ ] **S4-19: Product Selector** (1-2 hours)
  - Select2 dropdown for Product selection
  - Searchable: Minimum 2 characters before search
  - AJAX Loading: Load products when Product Type selected
  - Load from: `GET /quotation/{id}/discount-rules/lookup/products?product_type_id={id}`

#### JavaScript Integration (3-4 hours)
- [ ] **JavaScript File** (`public/js/quotation_discount_rules.js`)
  - Select2 initialization for all dropdowns
  - Make → Series dependency handling
  - Product Type → Product dependency handling
  - AJAX form submissions (create, update, delete)
  - Table refresh after operations
  - Modal handling (open, close, reset)
  - Preview modal integration
  - Apply button handling
  - Reset button handling
  - Success/error notification handling
  - Loading states (disable buttons, show spinners)
  - Form validation (client-side)
  - Event delegation for dynamic content

#### Sprint-3 Polish Items (3-4 hours)
- [ ] **S4-20: Fix Blank Square Button** (1 hour)
  - Find blank square button in panel header
  - Either remove it or convert to proper "Panel Actions (⋮)" dropdown menu

- [ ] **S4-21: Remove Duplicate Add Feeder** (1 hour)
  - Find "Add Feeder" button in feeder cards
  - Remove it (keep only in panel header)

- [ ] **S4-22: Add Discount Icon Tooltips** (1-2 hours)
  - Add hover tooltips for discount icons:
    - 🏷️ "Pricelist source"
    - ✏️ "Manual override"
    - 🔒 "Fixed/no discount"
    - ⚠️ "Missing price / unresolved"
    - 🧮 "Discount applied"

---

### 2.3 UI Standardization Global Audit
**Status:** ⏸️ IN PROGRESS (7/29+ pages complete)  
**Effort:** 15-20 hours  
**Priority:** HIGH

**Reference:** `UI_STANDARDIZATION_GLOBAL_AUDIT.md`

#### Completed Pages (7):
- ✅ Make
- ✅ Series
- ✅ Category
- ✅ Product
- ✅ Product Type (Item)
- ✅ Generic
- ✅ Attribute

#### Pending Pages (22+):

**High Priority (11 pages):**
- [ ] SubCategory
- [ ] Client
- [ ] Contact
- [ ] Project
- [ ] Quotation (list page)
- [ ] Master BOM
- [ ] Price List
- [ ] User
- [ ] Role
- [ ] Employee
- [ ] Company

**Medium Priority (11+ pages):**
- [ ] Catalog Health
- [ ] Catalog Cleanup
- [ ] Other admin/management pages

#### Standardization Requirements:
- [ ] Dual Search & Filters (all in ONE input-group)
- [ ] Table Styling (`nepl-standard-table` class)
- [ ] Font Styles (`nepl-page-title`, `nepl-small-text`)
- [ ] Colors (consistent color scheme)
- [ ] Filter Types (Select2 dropdowns, client-side filtering)
- [ ] No Full Page Reloads (AJAX updates only)
- [ ] Table Layout (`table-layout: auto` with `min-width`)

---

### 2.4 V2 Costing UI Improvements - Remaining
**Status:** ⏸️ PENDING  
**Effort:** 2-3 hours  
**Priority:** MEDIUM

**Step 3.3: Implement Mode Toggle (MEDIUM Priority)**
- [ ] Add mode toggle buttons (Engineer / Pricing / Full)
- [ ] Define column visibility sets
- [ ] Implement JS to toggle columns based on mode
- [ ] Persist mode preference in localStorage

**Step 3.4: Frozen Left Columns (LOW Priority - Optional)**
- [ ] Use CSS `position: sticky` for first 2-3 columns
- [ ] Test horizontal scrolling
- [ ] Ensure it works with column hide/show

---

## 🟢 PHASE 5.3: Advanced Features (MEDIUM Priority)

**Status:** ⏸️ PENDING  
**Priority:** MEDIUM  
**Duration:** 4-6 weeks  
**Effort:** ~60-80 hours

### 3.1 Code-Level TODOs (In Code Comments)
**Status:** ⏸️ PENDING  
**Effort:** 5-8 hours  
**Priority:** LOW-MEDIUM

#### 3.1.1 DeletionPolicyService - IsLocked Field
**Location:** `app/Services/DeletionPolicyService.php`  
**Lines:** 49, 123, 191, 250

**TODO:**
```php
// TODO: Add IsLocked field check when database field is added
```

**Action:** Add `IsLocked` field to:
- `quotation_sales` table (for panels)
- `quotation_sale_boms` table (for feeders/BOMs)
- `quotation_sale_bom_items` table (for components)

**Priority:** LOW - Feature not yet needed

#### 3.1.2 BOM Edit Modal - Dedicated Page
**Location:** `resources/views/quotation/v2/panel.blade.php`  
**Line:** 2043

**Current:** `editBom()` function scrolls to and highlights BOM  
**Needed:** Full dedicated edit page/modal for BOM editing

**Priority:** LOW - Current solution works

#### 3.1.3 Multi-Edit Modal - Implementation
**Location:** `resources/views/quotation/v2/panel.blade.php`  
**Line:** 2122

**Current:** Placeholder function  
**Needed:** Complete multi-edit modal UI and functionality

**Priority:** MEDIUM - Part of Phase 5.2 (Bulk Operations)

#### 3.1.4 Recalculation TODOs - Optional
**Location:** `app/Http/Controllers/QuotationV2Controller.php`  
**Lines:** 2018, 2087, 2154

**Status:** Optional - CostingService already handles this  
**Action:** Can be removed or left as-is (not critical)

**Priority:** LOW - Already handled by CostingService

---

### 3.2 Phase 2: Discount Application Table (UI)
**Status:** ⏸️ PENDING  
**Effort:** 16-24 hours  
**Priority:** MEDIUM

**Reference:** `FINAL_CONSOLIDATED_IMPLEMENTATION_PLAN.md`

#### UI Tasks:
- [ ] **Task 2.3: Discount Application UI** (2-3 days)
  - Views + Controllers
  - Rule management interface

**Note:** Backend tasks (2.1, 2.2, 2.4) are in backend work document.

---

### 3.3 Phase 3: Customer/Division/Contact (UI)
**Status:** ⏸️ PENDING  
**Effort:** 8 hours  
**Priority:** MEDIUM

**Reference:** `FINAL_CONSOLIDATED_IMPLEMENTATION_PLAN.md`

#### UI Tasks:
- [ ] **Task 3.4: UI Forms & Lists** (1 day)
  - View files
  - Form layouts
  - List views

**Note:** Backend tasks (3.1, 3.2, 3.3) are in backend work document.

---

### 3.4 Phase 4-6: UI Features
**Status:** ⏸️ PENDING  
**Effort:** 24-40 hours  
**Priority:** LOW

#### Phase 4: Revision Workflow Wizard (UI) (2 days)
- [ ] Comparison UI
- [ ] Revision review interface

#### Phase 5: PDF Versioning UI (1 day)
- [ ] Version comparison view
- [ ] PDF preview interface

#### Phase 6: Accessory Rules UI (1-2 days)
- [ ] Rule management interface
- [ ] Rule application preview

---

## 💰 PHASE 5.4: Costing Engine Implementation (HIGH Priority)

**Status:** ⏸️ PENDING  
**Priority:** HIGH  
**Duration:** 4-5 weeks  
**Effort:** ~19-28 days  
**Reference:** `COSTING_PLAN_COMPLETE_TODO_LIST.md`

### 4.1 Phase-1: Core Engine (P0 - Critical) - 5-7 days

**Backend Services:**
- [ ] **Create V2BomCostService**
  - Method: `getBomComponentCost(QuotationSaleBom $bom): array`
  - Method: `getBomChildCost(QuotationSaleBom $bom, array &$cache = []): array`
  - Method: `getBomTotalCost(QuotationSaleBom $bom, array &$cache = []): array`
  - Method: `getFeederCost(QuotationSaleBom $feeder): array`
  - Method: `getPanelCost(QuotationSale $panel): array`
  - Implement caching strategy
  - Handle null/zero quantities gracefully
  - Handle missing relationships
  - Prevent circular references

- [ ] **Create QuotationCostDetailService**
  - Method: `getRowsForQuotation(int $quotationId): Collection`
  - Helper: `buildBomPath($bom)` - Construct hierarchical path
  - Helper: `mapCostBucket($item)` - Map to MATERIAL/LABOUR/OTHER
  - Helper: `mapCostHead($item)` - Map to CostHead with priority logic
  - Helper: `getRevisionCode($quotation)` - Derive from ParentId/PrintType
  - Helper: `getQuotationStatus($quotation)` - Derive from PrintType/ParentId
  - Helper: `getFeederId($bom)` - Extract Level 0 BOM ID
  - Helper: `getFeederName($bom)` - Extract Level 0 BOM name
  - Integration with V2BomCostService
  - Integration with QuotationQuantityService
  - Eager loading to avoid N+1 queries
  - Generate all 49 columns correctly

**Export System:**
- [ ] **Create QuotationCostDetailExport**
  - Implements: `FromCollection`, `WithHeadings`
  - 49-column Excel export
  - Column order matches spec exactly
  - Proper heading names

- [ ] **Create QuotationExportController**
  - Method: `costDetail(Quotation $quotation)` - Excel export
  - Method: `costDetailJson(Quotation $quotation)` - JSON export
  - Proper file naming
  - Error handling

- [ ] **Add Export Routes**
  - Route: `GET /quotation/{quotation}/export/cost-detail`
  - Route: `GET /quotation/{quotation}/export/cost-detail/json`
  - Add to `routes/web.php`
  - Test routes work

**CostHead System:**
- [ ] **Create CostHead Migrations**
  - Migration: `create_cost_heads_table.php`
  - Migration: `add_cost_head_id_to_products_table.php`
  - Migration: `add_cost_head_id_to_quotation_sale_bom_items_table.php`
  - Run migrations

- [ ] **Create CostHead Model & Seeder**
  - File: `app/Models/CostHead.php`
  - File: `database/seeders/CostHeadSeeder.php`
  - Seed initial cost heads (OEM_MATERIAL, NEPL_BUS, NEPL_FAB, etc.)
  - Run seeder

**Model Enhancements:**
- [ ] **Add items() alias to QuotationSaleBom**
  - Add method: `public function items() { return $this->item(); }`
  - Test relationship works

- [ ] **Create HasEffectiveQuantity Trait (Optional)**
  - Accessor: `base_item_qty`
  - Accessor: `bom_qty_product`
  - Accessor: `effective_qty_per_panel`
  - Accessor: `effective_qty_total`
  - Add trait to `QuotationSaleBomItem` model
  - Test accessors work

**UI Hooks:**
- [ ] **Add Export Button to V2 Header**
  - Button: "Export Cost Sheet (Excel)"
  - Links to export route
  - Icon: `la-file-excel-o`

- [ ] **Add Export Icon to Quotation List**
  - Icon in action column
  - Tooltip: "Export Cost Detail"
  - Links to export route

**Testing:**
- [ ] **Unit Tests**
  - Test V2BomCostService methods
  - Test QuotationCostDetailService
  - Test quantity calculations
  - Test cost calculations

- [ ] **Integration Tests**
  - Test service composition
  - Test export functionality
  - Test with complex quotations (nested BOMs)

---

### 4.2 Phase-2: Costing Pack Foundation (P1 - High Priority) - 3-4 days

**Costing Snapshot Strip:**
- [ ] **Create Top Strip Component**
  - Display: Client, Project, Quotation No, Revision
  - Display: Total Cost (from V2BomCostService)
  - Display: Total Selling Price
  - Display: Gross Margin (₹ & %)
  - Input: Overhead % (editable)
  - Input: Target Margin % (editable)
  - Real-time calculation updates
  - CSS styling matching NEPL UI

**Panel Cost Summary Table:**
- [ ] **Create Panel Summary Table**
  - Use `<x-nepl-table>` component
  - Columns: Panel Name, Qty, Unit Cost, Total Cost, Selling Price, Margin %, Margin ₹
  - Data from V2BomCostService
  - Click row → drill-down to Feeder/BOM tree
  - "View Detailed BOM" icon → opens modal/pane
  - Responsive design

**Cost Pivot Tabs:**
- [ ] **Create Tab Navigation**
  - Tab A: Cost by Category
  - Tab B: Cost by Make
  - Tab C: Cost by RateSource
  - Data aggregation from QuotationCostDetail

**Panel Drilldown:**
- [ ] **Integrate V2 Engineering View**
  - Reuse existing V2 BOM tree view
  - Show: Panel → Feeder → BOM → Items
  - Node metrics: Material/Labour/Other, Total Cost, % of Panel Cost
  - Expand/collapse functionality

---

### 4.3 Phase-2.5: Excel Export Enhancement (P1 - High Priority) - 2-3 days

- [ ] **Create QuotationCostingExport**
  - Sheet 1: Panel_Cost_Summary
  - Sheet 2: Detailed_BOM
  - Sheet 3: Pivots (pre-filled pivot table shells)

- [ ] **Add Export Route**
  - Route: `GET /quotation/{quotation}/export/costing`
  - Controller method: `QuotationExportController::costing()`
  - File naming: `Quotation_{No}_CostingPack.xlsx`
  - Test export works

---

### 4.4 Phase-3: Costing Pack - Advanced Features (P2 - Medium Priority) - 2-3 days

- [ ] **Cost by CostHead Pivot Tab**
- [ ] **Offer View Integration**
- [ ] **Enhanced Panel Drilldown**

---

### 4.5 Phase-4: Evaluation Module (P2 - Medium Priority) - 2-3 days

- [ ] **Revision Comparison View**
- [ ] **Option Comparison View**
- [ ] **Estimated vs Actual (Future)**

---

### 4.6 Phase-5: Estimation Dashboard (P2 - Medium Priority) - 3-4 days

**KPI Tiles:**
- [ ] **Create Dashboard Layout**
  - Tile: Quotations Created (count + value)
  - Tile: Orders Won (count + value)
  - Tile: Hit Rate (value & count)
  - Tile: Average Margin on Won
  - Tile: Average Discount vs List
  - Click actions → navigate to filtered Quotation List

**Filters:**
- [ ] **Add Filter Controls**
  - Period filter (Week/Month/Quarter/Year)
  - Client filter
  - Category filter
  - Estimator filter
  - Apply filters to all tiles and tables

**Cost Drivers:**
- [ ] **Top 10 Cost Categories Table**
- [ ] **Top 10 Makes Table**
- [ ] **Manual Pricing Share Table/Chart**
- [ ] **Client-wise Margin Distribution Table**

---

## 🤖 PHASE 5.5: AI Implementation (MEDIUM-HIGH Priority)

**Status:** ⏸️ PENDING  
**Priority:** MEDIUM-HIGH  
**Duration:** 5-7 weeks  
**Effort:** ~25-35 days  
**Reference:** `AI_IMPLEMENTATION_TODO_LIST.md`

### 5.1 Phase-1: AI Foundation (P0 - Critical) - 8-10 days

**1.1 Golden Rulebook System:**
- [ ] **Create Rulebook Folder Structure**
  - Create `/docs/nepl_rules/` folder
  - Create `/docs/nepl_rules/iec/` subfolder
  - Create `/docs/archive/` folder for old logic
  - Document folder structure in README

- [ ] **Create Rulebook Template**
  - File: `/docs/nepl_rules/TEMPLATE_RULEBOOK.md`
  - Include: STATUS, VERSION, EFFECTIVE_FROM tags
  - Document versioning process

- [ ] **Create Initial Rulebooks**
  - `NEPL_Rulebook_Panel_Design.md` (basic structure)
  - `NEPL_Rulebook_BOM_Logic.md` (basic structure)
  - `NEPL_Rulebook_Discount_Policy.md` (basic structure)
  - `NEPL_Rulebook_Switchgear_Selection.md` (basic structure)
  - Mark all as STATUS: FINAL, VERSION: 1.0

- [ ] **Create IEC 61439 Summary**
  - File: `/docs/nepl_rules/iec/IEC_61439_Application_Guide_for_NEPL.md`
  - Include: Basic voltage/kW/frame rating rules
  - Mark as STATUS: FINAL, VERSION: 1.0

- [ ] **Update DocIndexer Logic** (if exists)
  - Only index files with STATUS: FINAL
  - Only index from `/docs/nepl_rules/`
  - Ignore `/docs/archive/` and `/notes/`

**1.2 AI Gateway Architecture:**
- [ ] **Create AI Module Folder Structure**
  - Create `/app/Services/Ai/` folder
  - Create `/app/Services/Ai/Prompts/` subfolder
  - Create `/app/Services/Ai/Transformers/` subfolder
  - Create `/app/Services/Ai/Models/` subfolder (for future ML)

- [ ] **Create AiGateway Service**
  - Static methods:
    - `suggestComponent($payload)`
    - `priceSanityCheck($payload)`
    - `missingComponents($payload)`
    - `discountPatternCheck($payload)`
    - `buildOptionVariant($payload)`
    - `explainCostDriver($payload)`
    - `targetMarginHelper($payload)`
  - Private helpers:
    - `loadPrompt($filename)`
    - `logCall($endpoint, $request, $response)`
    - `validatePayload($payload, $rules)`

- [ ] **Create AiClient Service**
  - Method: `send($prompt, $context = [])`
  - Integration with OpenAI/GPT API
  - Handle: model name, temperature, token limits
  - Error handling and retries
  - JSON output formatting

- [ ] **Create AiRuleEngine Service**
  - Hard rule enforcement:
    - `validateVoltageCompatibility()`
    - `validateKWRating()`
    - `validateFrameRating()`
    - `enforceAllowedMakes()`
    - `enforceAllowedItems()`
    - `applySubstitutionRules()`
  - Safety filters:
    - `removeHallucinatedFields()`
    - `confirmOutputIsWhitelisted()`
    - `blockUnsafeSuggestions()`

- [ ] **Create AI Controller**
  - Methods:
    - `suggestComponent(Request $r)`
    - `priceSanityCheck(Request $r)`
    - `missingComponents(Request $r)`
    - `discountPatternCheck(Request $r)`
    - `buildOptionVariant(Request $r)`
    - `explainCostDriver(Request $r)`
    - `targetMarginHelper(Request $r)`
  - Each method:
    - Validates request
    - Calls AiGateway
    - Returns JSON response
    - Try/catch with clean errors
    - Enforces authentication

- [ ] **Create API Routes**
  - `POST /ai/suggest-component`
  - `POST /ai/price-sanity-check`
  - `POST /ai/missing-components`
  - `POST /ai/discount-pattern-check`
  - `POST /ai/build-option`
  - `POST /ai/explain-cost-driver`
  - `POST /ai/target-margin-helper`
  - All routes require authentication
  - Add rate limiting (if needed)

**1.3 AI Logging & Audit:**
- [ ] **Create AI Call Logs Migration**
  - Fields: `id`, `user_id`, `quotation_id`, `panel_id`, `feeder_id`, `bom_item_id`
  - `endpoint` (varchar)
  - `request_json` (longtext)
  - `response_json` (longtext)
  - `final_action` (enum: accepted/rejected/modified)
  - `status` (enum: ok/warning/error)
  - `created_at`, `updated_at`
  - Indexes: `quotation_id`, `panel_id`, `endpoint`, `user_id`

- [ ] **Create AiCallLog Model**
  - Fillable fields
  - Relationships: `user()`, `quotation()`, `panel()`, `feeder()`
  - Scopes: `byQuotation()`, `byUser()`, `byEndpoint()`, `errors()`

- [ ] **Implement Logging in AiGateway**
  - Log every AI call
  - Log request payload
  - Log AI response
  - Log final user action (accepted/rejected/modified)
  - Log errors with stack trace

**1.4 Prompt Templates:**
- [ ] **Create Prompt Template Files**
  - `/app/Services/Ai/Prompts/suggest_component.txt`
  - `/app/Services/Ai/Prompts/price_sanity.txt`
  - `/app/Services/Ai/Prompts/missing_components.txt`
  - `/app/Services/Ai/Prompts/discount_pattern.txt`
  - `/app/Services/Ai/Prompts/option_builder.txt`
  - `/app/Services/Ai/Prompts/cost_driver.txt`
  - `/app/Services/Ai/Prompts/target_margin.txt`

- [ ] **Each Prompt Must Include:**
  - System instructions (use NEPL data only)
  - Business rule constraints
  - Output format (strict JSON)
  - Safety instructions (never hallucinate)
  - Version tag (VERSION: 1.0)

---

### 5.2 Phase-2: Core AI Features (P1 - High Priority) - 10-15 days

**2.1 Smart Component Suggestion:**
- [ ] **Create Selection Patterns Table**
- [ ] **Create Batch Job to Populate Patterns**
- [ ] **Implement suggestComponent Logic**
- [ ] **UI Integration: V2 BOM Row**
  - Add "AI Suggest" button/icon next to component selector
  - Show suggestions in dropdown/popup
  - User can click to apply suggestion
  - Log user action (accepted/rejected)

**2.2 Price Sanity Check:**
- [ ] **Create Price Distribution Table**
- [ ] **Create Batch Job to Calculate Distributions**
- [ ] **Implement priceSanityCheck Logic**
- [ ] **UI Integration: Rate Column**
  - On rate field blur: Call `/ai/price-sanity-check`
  - Show inline warning icon
  - Hover/click shows message
  - Log user action (acknowledged/ignored)

**2.3 Missing Components Detector:**
- [ ] **Create Co-Occurrence Table**
- [ ] **Create Batch Job to Calculate Co-Occurrences**
- [ ] **Implement missingComponents Logic**
- [ ] **UI Integration: BOM Summary**
  - Right panel: "Recommended Additions"
  - Show cards for each recommendation
  - [Add to BOM] button
  - Log user action (added/ignored)

**2.4 Discount Pattern Checker:**
- [ ] **Create Discount Behavior Table**
- [ ] **Create Batch Job to Calculate Discount Patterns**
- [ ] **Implement discountPatternCheck Logic**
- [ ] **UI Integration: Panel Summary / Costing Pack**
  - "AI Check" button
  - Modal shows warnings and recommendations
  - Log user action (acknowledged/modified/ignored)

---

### 5.3 Phase-3: Advanced AI Features (P2 - Medium Priority) - 7-10 days

**3.1 Option Builder (A/B/C Variants):**
- [ ] **Create Substitution Matrix Table**
- [ ] **Create Substitution Matrix Seeder**
- [ ] **Implement buildOptionVariant Logic**
- [ ] **UI Integration: Panel Summary**
  - Button: "Generate Option B/C (AI)"
  - Modal with checkboxes: Economy / Premium
  - Shows cost delta
  - Log user action (created/ignored)

**3.2 Cost Driver Explanation:**
- [ ] **Implement explainCostDriver Logic**
- [ ] **UI Integration: Costing Pack**
  - AI block: "Top Cost Drivers"
  - Lists top 3 contributors with narrative explanation
  - Log user action (viewed/ignored)

**3.3 Target Margin Helper:**
- [ ] **Implement targetMarginHelper Logic**
- [ ] **UI Integration: Feeder/Panel/Quotation Summary**
  - Input field: "Target Margin %"
  - Button: "AI Generate Discount Profile"
  - Modal shows suggested discount adjustments
  - User can apply or modify
  - Log user action (applied/modified/ignored)

**3.4 Expanded IEC 61439 Rules:**
- [ ] **Expand IEC Application Guide**
- [ ] **Create IEC Rules Database Tables**
- [ ] **Enhance AiRuleEngine with IEC Rules**

**3.5 AI Maintenance & Health Page:**
- [ ] **Create Routine Logs Table**
- [ ] **Create Maintenance Controller**
- [ ] **Create Maintenance View**
- [ ] **Create Scheduled Commands**
- [ ] **Register Scheduled Tasks**
- [ ] **Add Route**

---

## 🔵 PHASE 5.6: Long-term Upgrades (LOW Priority)

**Status:** ⏸️ PENDING  
**Priority:** LOW  
**Duration:** 6-8 weeks  
**Effort:** ~65-90 hours

### 6.1 Framework & Technology Upgrades
**Status:** ⏸️ PENDING  
**Effort:** 40-60 hours  
**Priority:** LOW (Long-term)

#### Laravel & PHP Upgrade
- [ ] Upgrade Laravel from 8.65 to 10/11
- [ ] Upgrade PHP from 7.3/8.0 to 8.2+
- [ ] Test on Laravel 9 first
- [ ] Fix deprecated code
- [ ] Update all dependencies

#### Frontend Modernization
- [ ] Consider Vue 3, React, or modern Blade components
- [ ] Current: Blade + jQuery
- [ ] Estimated: 80-120 hours (separate project)

#### Performance Optimizations
- [ ] Implement caching strategy (8-12 hours)
- [ ] Add pagination (4-6 hours)
- [ ] Add database indexes for performance
- [ ] Implement eager loading to prevent N+1 queries

---

### 6.2 Documentation TODOs
**Status:** ⏸️ PENDING  
**Effort:** 25-30 hours  
**Priority:** MEDIUM-LOW

**Critical Gaps:**
- [ ] `35_DEPLOYMENT_GUIDE.md` - Deployment procedures
- [ ] `44_BACKUP_RESTORE.md` - Backup/restore procedures
- [ ] `45_ENVIRONMENT_SETUP.md` - Environment setup guide

**Important Gaps:**
- [ ] `46_ERROR_HANDLING.md` - Error handling guide
- [ ] `47_TESTING_STRATEGY.md` - Testing strategy
- [ ] `48_RELEASE_PROCESS.md` - Release process

---

## 📋 Implementation Sequence

### Recommended Execution Order

1. **Phase 5.1: Critical Foundation** (2-3 weeks)
   - Validation Guardrails Testing
   - BOM Instance Identity Enhancement
   - Add Component Button Fix
   - V2 Costing UI Critical Fixes

2. **Phase 5.2: Core Enhancements** (3-4 weeks)
   - Master BOM vs Proposal BOM Enhancements
   - Sprint-4 UI Components (Discount Rules)
   - UI Standardization Global Audit
   - V2 Costing UI Remaining

3. **Phase 5.4: Costing Engine** (4-5 weeks) - Can run parallel with 5.2
   - Core Engine
   - Costing Pack Foundation
   - Excel Export Enhancement
   - Advanced Features
   - Evaluation Module
   - Estimation Dashboard

4. **Phase 5.3: Advanced Features** (4-6 weeks) - Can run parallel with 5.4
   - Code-Level TODOs
   - Discount Application Table UI
   - Customer/Division/Contact UI
   - Phase 4-6 UI Features

5. **Phase 5.5: AI Implementation** (5-7 weeks) - After 5.4 foundation
   - AI Foundation
   - Core AI Features
   - Advanced AI Features

6. **Phase 5.6: Long-term Upgrades** (6-8 weeks) - Ongoing/Background
   - Framework & Technology Upgrades
   - Documentation TODOs

---

## 📊 Summary by Priority

### 🔴 HIGH PRIORITY (Do First)

**Phase 5.1: Critical Foundation (~40-50 hours)**
- Validation Guardrails Testing (4-6 hours)
- BOM Instance Identity Enhancement (6-8 hours)
- Add Component Button Fix (2-3 hours)
- V2 Costing UI Critical Fixes (4-6 hours)

**Phase 5.2: Core Enhancements (~50-60 hours)**
- Master BOM vs Proposal BOM Enhancements (15-20 hours)
- Sprint-4 UI Components (25-35 hours)
- UI Standardization Global Audit (15-20 hours)

**Phase 5.4: Costing Engine (~19-28 days)**
- Phase-1: Core Engine (5-7 days)
- Phase-2: Costing Pack Foundation (3-4 days)

**Total High Priority:** ~90-110 hours + 8-11 days

---

### 🟡 MEDIUM PRIORITY (Do When Time Permits)

**Phase 5.3: Advanced Features (~60-80 hours)**
- Code-Level TODOs (5-8 hours)
- Discount Application Table UI (16-24 hours)
- Customer/Division/Contact UI (8 hours)
- Phase 4-6 UI Features (24-40 hours)
- V2 Costing UI Remaining (2-3 hours)

**Phase 5.4: Costing Engine - Advanced (~7-10 days)**
- Phase-2.5: Excel Export Enhancement (2-3 days)
- Phase-3: Advanced Features (2-3 days)
- Phase-4: Evaluation Module (2-3 days)
- Phase-5: Estimation Dashboard (3-4 days)

**Phase 5.5: AI Implementation (~25-35 days)**
- Phase-1: AI Foundation (8-10 days)
- Phase-2: Core AI Features (10-15 days)
- Phase-3: Advanced AI Features (7-10 days)

**Total Medium Priority:** ~60-80 hours + 32-45 days

---

### 🟢 LOW PRIORITY (Nice to Have)

**Phase 5.6: Long-term Upgrades (~65-90 hours)**
- Framework & Technology Upgrades (40-60 hours)
- Documentation TODOs (25-30 hours)

**Total Low Priority:** ~65-90 hours

---

## 🔗 Integration with Phase 5

### During Phase 5 (Analysis Only)

**Step 1: Freeze NSW Canonical Data Dictionary**
- When defining entities, consider:
  - BOM Instance Identity fields (OriginMasterBomId, InstanceSequenceNo)
  - Modification tracking fields (IsModified, ModifiedBy, ModifiedAt)
  - CostHead entity definitions
  - AI-related entities (if needed)

**Step 2: Define NSW Canonical Schema**
- When designing schema, include:
  - All migration fields from Phase 5.1 and 5.2
  - CostHead tables
  - AI logging tables
  - Audit trail tables

### After Phase 5 (Implementation)

**Use this roadmap** to execute all pending upgrades in the structured phases defined above.

---

## 📚 Reference Documents

- `ALL_PENDING_UPGRADES_CONSOLIDATED.md` - Complete inventory (if exists)
- `COSTING_PLAN_COMPLETE_TODO_LIST.md` - Costing engine tasks
- `AI_IMPLEMENTATION_TODO_LIST.md` - AI feature tasks
- `SPRINT4_UI_TODO_LIST.md` - Sprint-4 UI components
- `UI_STANDARDIZATION_GLOBAL_AUDIT.md` - UI standardization audit
- `V2_COSTING_TODO_LIST.md` - V2 costing UI tasks

---

**Status:** ✅ Complete Integration  
**Last Updated:** December 18, 2025  
**Next Update:** As Phase 5 completes and implementation begins

