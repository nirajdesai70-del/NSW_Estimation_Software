# Phase-6 Complete Scope & Task Summary

**Version:** 1.4 (Cost Adders Integrated)  
**Date:** 2025-01-27  
**Status:** COMPREHENSIVE SCOPE DOCUMENT  
**Reference:** Phase-6 Execution Plan v1.4 & Kickoff Charter + Phase-5 Canonical Working Record + Cost Adders Final Spec

---

## 🎯 Executive Summary

**Phase-6: Productisation & Controlled Expansion**

Phase-6 converts a **correct system** (Phase-5) into a **usable product** with complete costing and reporting capabilities, while preserving all legacy capabilities through reuse workflows.

**Total Duration:** 10-12 weeks  
**Total Tracks:** 7 parallel tracks (A, A-R, B, C, D0, D, E)  
**Total Tasks:** ~133 tasks  
**Exit Artifact:** NSW v0.6 – Internal Product Ready

**Key Additions:**
- **v1.3:** Track A-R (Reuse & Legacy Parity) ensures all legacy capabilities from Phase-1–4 and Nish system are preserved
- **v1.4:** Cost Adders feature integrated (cost templates, cost sheets, QCA dataset) for complete panel costing

---

## 📊 Complete Scope Overview

### Track A: Productisation (6 weeks, 33 tasks)
**Purpose:** Build complete quotation creation and management UI

**Key Features:**
- Quotation overview and panel management
- BOM hierarchy tree view (Panel → Feeder → BOM L1 → BOM L2 → Components)
- Pricing resolution UX (PRICELIST / MANUAL / FIXED)
- L0 → L1 → L2 resolution flow
- Locking behaviour visibility
- Error & warning surfacing
- Customer snapshot handling

### Track A-R: Reuse & Legacy Parity (3 weeks, 7 tasks) ⭐ NEW
**Purpose:** Preserve all legacy capabilities through reuse workflows

**Key Features:**
- Quotation reuse (copy old quotation → modify)
- Panel reuse (copy panel subtree)
- Feeder reuse (copy Level-0 BOM + subtree)
- BOM reuse (copy BOM from past quotation)
- Master BOM template application
- Post-reuse editability verification
- Guardrail enforcement after reuse

### Track B: Catalog Tooling (4 weeks, 16 tasks)
**Purpose:** Enable safe catalog import and governance

**Key Features:**
- Catalog import UI with file upload
- Series-wise catalog onboarding
- Pre-import validation previews
- Catalog governance enforcement and approval workflows

### Track C: Operational Readiness (2 weeks, 12 tasks)
**Purpose:** Enable role-based access and approval workflows

**Key Features:**
- Basic role-based access control
- Approval flows (price changes, overrides)
- Audit visibility (read-only)
- Initial SOPs
- Costing Pack/dashboard/export permissions

### Track D0: Costing Engine Foundations (4 weeks, 14 tasks) ⭐ NEW
**Purpose:** Build canonical costing engine (QCD + QCA) before UI/reporting

**Key Features:**
- Effective quantity engine (BaseQty → EffQtyPerPanel → EffQtyTotal)
- CostHead mapping precedence (D-006)
- QuotationCostDetail (QCD) canonical dataset (BOM-only, stable contract)
- Cost Adders engine (cost templates, cost sheets, QCA dataset) ⭐ NEW
- QCD + QCA JSON export endpoints
- Numeric validation vs reference Excel (engine-first)
- Performance hardening for large quotations (with cost adders)
- D0 Gate signoff (QCD v1.0 stable + QCA v1.0 stable)

### Track D: Costing & Reporting (4 weeks, 20 tasks) ⭐ MODIFIED
**Purpose:** Replace manual Excel costing with automated costing engine and dashboards

**Key Features:**
- Costing Pack per quotation (snapshot, panel summary, pivots)
- Cost Adders UI (panel section, cost sheet editor) ⭐ NEW
- Global dashboard (margins, hit rates, cost drivers)
- CostHead system UI
- Excel export functionality (includes cost adders)
- **Consumes QCD + QCA (no duplicate calculators)** ✏️

### Track E: Canon Implementation & Contract Enforcement (6 weeks, ~29 tasks) ⭐ NEW
**Purpose:** Implement all Phase-5 frozen items

**Key Features:**
- DB creation/migrations from Schema Canon v1.0 + seed execution
- Cost template seed data (Cost Adders) ⭐ NEW
- Guardrails G1-G8 runtime enforcement + tests
- API contract implementation (B1-B4) OR explicit defer decision
- Multi-SKU linkage (D-007) implementation
- Discount Editor (legacy parity)
- BOM tracking fields runtime behavior
- Customer snapshot handling (D-009)
- Resolution constraints enforcement (A10)

### Legacy Parity Gate (0.5 weeks, 6 tasks) ⭐ NEW
**Purpose:** Verify all legacy capabilities preserved

**Key Features:**
- Quotation reuse verified
- Panel reuse verified
- Feeder reuse verified
- BOM reuse verified
- Post-reuse guardrails verified
- Legacy parity checklist complete

### Integration & Stabilisation (2 weeks, 12 tasks)
**Purpose:** End-to-end integration, bug fixes, UX polish

### Closure (2 weeks, 5 tasks)
**Purpose:** Exit criteria verification, canon compliance signoff, and handover

---

## 📋 Complete Task List by Track

## TRACK A: PRODUCTISATION (33 Tasks)

### Week 1: Quotation & Panel UI (5 tasks)

#### P6-UI-001: Design quotation overview page
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/QUOTATION_OVERVIEW_DESIGN.md`
- **Details:**
  - Quotation header (Client, Project, Quotation No)
  - Panel list with summary cards
  - Add Panel button
  - Navigation to panel details
  - Pricing status indicators

#### P6-UI-002: Implement quotation overview page
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/quotation/{id}/v2`
- **Views:** `resources/views/quotation/v2/index.blade.php`
- **Controller:** `QuotationV2Controller@index`
- **Features:**
  - Display panel list with counts (feeders, items)
  - Display pricing status indicators
  - Navigation to panel details

#### P6-UI-003: Design panel details page
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/PANEL_DETAILS_DESIGN.md`
- **Details:**
  - Panel header (name, Qty, Rate, Amount)
  - Feeder list (Level=0 BOMs)
  - Add Feeder button
  - Navigation to feeder/BOM details

#### P6-UI-004: Implement panel details page
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/quotation/{id}/panel/{panelId}`
- **Views:** `resources/views/quotation/v2/panel.blade.php`
- **Controller:** `QuotationV2Controller@panel`
- **Features:**
  - Display feeder list with hierarchy

#### P6-UI-005: Implement add panel functionality
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/panel`
- **Controller:** `QuotationV2Controller@addPanel`
- **Features:**
  - Form validation
  - Database insert
  - Redirect to panel details

#### P6-UI-001A: Ensure customer_name_snapshot always stored (D-009)
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - When creating quotation, always populate `customer_name_snapshot`
  - If customer_id provided, copy customer name to snapshot
  - If customer_id NULL, use provided customer name for snapshot
  - Integration with quotation creation flow

#### P6-UI-001B: customer_id remains nullable (D-009)
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Ensure customer_id can be NULL
  - Support quotation creation without customer_id
  - Support future customer normalization

---

### Week 2: Feeder & BOM Hierarchy UI (5 tasks)

#### P6-UI-006: Design BOM hierarchy tree view
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/BOM_HIERARCHY_DESIGN.md`
- **Details:**
  - Collapsible tree structure
  - Feeder (Level 0) → BOM L1 (Level 1) → BOM L2 (Level 2)
  - Component list at each level

#### P6-UI-007: Implement BOM hierarchy tree view
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Partials:**
  - `_bom_tree.blade.php` (recursive)
  - `_feeder.blade.php`
  - `_bom.blade.php`
- **Features:**
  - JavaScript for expand/collapse
  - Visual hierarchy indicators

#### P6-UI-008: Implement add feeder functionality
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/panel/{panelId}/feeder`
- **Controller:** `QuotationV2Controller@addFeeder`
- **Features:**
  - Form with feeder name, quantity
  - Database insert with Level=0

#### P6-UI-009: Implement add BOM functionality
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/bom/{parentBomId}/bom`
- **Controller:** `QuotationV2Controller@addBom`
- **Features:**
  - Support Level 1 and Level 2
  - Parent-child relationship handling

#### P6-UI-010: Implement component/item list display
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Partials:** `_item.blade.php`
- **Features:**
  - Display: Category, SubCategory, Item, Generic
  - Display: Make, Series, Description, SKU
  - Display: Qty, Rate, Amount
  - Basic styling

#### P6-UI-010A: Verify raw quantity persistence
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - PanelQty stored correctly
  - FeederQty (L0) stored correctly
  - BomQty (L1+) stored correctly
  - ItemQtyPerBom stored correctly
  - Verify quantities persist through create/edit operations

---

### Week 3: Pricing Resolution UI (6 tasks)

#### P6-UI-011: Design pricing resolution UX
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/PRICING_RESOLUTION_UX.md`
- **Details:**
  - RateSource dropdown (PRICELIST / MANUAL / FIXED)
  - Price display with source indicator
  - Override controls
  - Discount input (for MANUAL)

#### P6-UI-012: Implement RateSource selector
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - RateSource dropdown to component row
  - Three options: PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT
  - JavaScript handler: `handleRateSourceChange()`
  - Show/hide relevant fields based on selection

#### P6-UI-013: Implement price auto-population
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Integration:** Phase-5 price resolution engine
- **Features:**
  - Auto-populate from pricelist when RateSource=PRICELIST
  - Display price source (pricelist SKU, manual entry, fixed)
  - Handle missing price scenarios

#### P6-UI-014: Implement manual pricing controls
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Discount percentage input (for MANUAL_WITH_DISCOUNT)
  - Base price display
  - Calculated price display
  - JavaScript: `calculateManualPrice()`

#### P6-UI-015: Implement fixed pricing controls
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Fixed price input (for FIXED_NO_DISCOUNT)
  - No discount allowed
  - Price confirmation checkbox
  - JavaScript: `handleFixedPrice()`

#### P6-UI-016: Implement pricing status indicators
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Visual indicators: ✅ Priced, ⚠️ Missing Price, ⚠️ Unresolved
  - Component-level status
  - BOM-level summary
  - Panel-level summary
  - Quotation-level summary

---

### Week 4: L0→L1→L2 Resolution UX (6 tasks)

#### P6-UI-017: Design L0→L1→L2 resolution UX
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/L0_L1_L2_RESOLUTION_UX.md`
- **Details:**
  - L0 selection interface (generic product selection)
  - L1 selection interface (intent-based selection)
  - L2 selection interface (SKU selection)
  - Resolution flow visualization

#### P6-UI-018: Implement L0 selection UI
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Integration:** catalog_products table
- **Features:**
  - Generic product search/select
  - Category/SubCategory filters
  - Display generic product details

#### P6-UI-019: Implement L1 resolution UI
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Integration:** l1_line_groups, l1_intent_lines
- **Features:**
  - Intent-based selection (voltage, duty, attributes)
  - Display L1 line groups
  - Display L1 intent lines
  - Show mapping to L2 candidates

#### P6-UI-020: Implement L2 resolution UI
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Integration:** l1_l2_mappings, catalog_skus
- **Features:**
  - SKU selection from L1 candidates
  - Display SKU details
  - Show price availability
  - Confirm selection

#### P6-UI-021: Implement resolution flow visualization
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Show current resolution stage (L0 → L1 → L2)
  - Display resolution path
  - Show unresolved warnings
  - Navigation between stages

#### P6-UI-022: Implement resolution status indicators
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - L0 selected ✅
  - L1 resolved ✅
  - L2 resolved ✅
  - Missing resolution ⚠️
  - Component-level and BOM-level indicators

#### P6-RES-023: Enforce resolution constraints exactly as Schema Canon
- **Type:** Implementation
- **Deliverable:** Functional enforcement
- **Features:**
  - Enforce MBOM: L0/L1 only, no ProductId
  - Enforce QUO: L0/L1/L2 allowed, L2 requires ProductId
  - Enforce CHECK constraints at DB level
  - Enforce constraints at service level
  - Enforce constraints at UI level (prevent invalid selections)

#### P6-RES-024: Errors must map to B3 error taxonomy codes
- **Type:** Implementation
- **Deliverable:** Functional error mapping
- **Features:**
  - Review error taxonomy from Phase-5 (03_ERROR_TAXONOMY.md)
  - Map resolution errors to taxonomy codes
  - Ensure error messages match taxonomy
  - Ensure HTTP status codes match taxonomy
  - Ensure request_id propagation

---

### Week 5: Locking Behaviour Visibility (5 tasks)

#### P6-UI-023: Design locking visibility UX
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/LOCKING_VISIBILITY_UX.md`
- **Details:**
  - Visual indicators for locked items
  - Lock status display (locked/unlocked)
  - Lock reason display
  - Lock prevention UI (disable edits)

#### P6-UI-024: Implement lock status display
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Visual lock icon on locked items
  - Lock status badge
  - Lock timestamp display
  - Lock reason tooltip

#### P6-UI-025: Implement lock prevention UI
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Integration:** Phase-5 is_locked enforcement
- **Features:**
  - Disable edit controls for locked items
  - Disable delete for locked items
  - Show lock message on interaction attempt

#### P6-UI-026: Implement lock status summary
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Panel-level lock count
  - BOM-level lock count
  - Quotation-level lock summary
  - Visual lock status dashboard

#### P6-UI-027: Implement lock/unlock controls (admin)
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Unlock button (admin only)
  - Lock confirmation dialog
  - Unlock confirmation dialog
  - Audit log entry

#### P6-LOCK-000: Verify no higher-level locking introduced (schema + UI)
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Verify no is_locked field on quote_boms (BOM level)
  - Verify no is_locked field on quote_panels (Panel level)
  - Verify no is_locked field on quotations (Quotation level)
  - Verify locking only at quote_bom_items level (line-item only)
  - Document locking scope per D-005 decision

---

### Week 6: Error & Warning Surfacing (6 tasks)

#### P6-UI-028: Design error/warning surfacing UX
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/UI/ERROR_WARNING_UX.md`
- **Details:**
  - Error message display
  - Warning message display
  - Inline validation errors
  - Summary error panel

#### P6-UI-029: Implement price missing warnings
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Detect missing prices (RateSource=PRICELIST but no price found)
  - Display warning icon on component
  - Warning message: "Price not found in pricelist"
  - Action: Switch to MANUAL or FIXED

#### P6-UI-030: Implement unresolved warnings
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Detect unresolved L0/L1/L2
  - Display warning icon
  - Warning message: "L1/L2 not resolved"
  - Action: Complete resolution flow

#### P6-UI-031: Implement validation error display
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Form validation errors
  - Inline error messages
  - Field-level error indicators
  - Summary error list

#### P6-UI-032: Implement error summary panel
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Quotation-level error count
  - Panel-level error count
  - BOM-level error count
  - Expandable error details
  - Navigation to error location

#### P6-UI-033: Implement user-friendly error messages
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Convert technical errors to user-friendly messages
  - Provide actionable guidance
  - Link to help documentation
  - Error code reference

---

## TRACK A-R: REUSE & LEGACY PARITY (7 Tasks) ⭐ NEW

**Purpose:** Preserve all legacy capabilities through reuse workflows

### Week 2.5: Reuse Foundations (2 tasks)

#### P6-UI-REUSE-001: Copy quotation (deep copy)
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/copy`
- **Controller:** `QuotationV2Controller@copyQuotation`
- **Features:**
  - Copy full hierarchy: panels → feeders → BOMs → items
  - Populate BOM tracking fields:
    - `origin_master_bom_id` (if from master)
    - `instance_sequence_no` (increment)
    - `is_modified = false` (initial state)
  - Preserve pricing fields (RateSource, Discount, etc.)
  - UI action: "Create quotation from existing quotation"
  - **File:** `docs/PHASE_6/UI/QUOTATION_REUSE_DESIGN.md`

#### P6-UI-REUSE-002: Copy panel into quotation
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/panel/copy`
- **Controller:** `QuotationV2Controller@copyPanel`
- **Features:**
  - Copy panel subtree (feeders → BOMs → items)
  - Source: same quotation OR past quotation
  - Target: selected quotation
  - Preserve quantities and pricing
  - Editable until locked
  - UI action: "Copy panel from existing quotation"

---

### Week 3: Feeder & BOM Reuse (3 tasks)

#### P6-UI-REUSE-003: Copy feeder (Level-0 BOM)
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/panel/{panelId}/feeder/copy`
- **Controller:** `QuotationV2Controller@copyFeeder`
- **Features:**
  - Copy feeder (Level-0 BOM) + full subtree
  - Source: same quotation OR past quotation
  - Target: selected panel
  - Must preserve hierarchy & quantities
  - Preserve BOM tracking fields
  - UI action: "Copy feeder from existing quotation"

#### P6-UI-REUSE-004: Copy BOM under feeder
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/bom/{parentBomId}/bom/copy`
- **Controller:** `QuotationV2Controller@copyBom`
- **Features:**
  - Copy BOM subtree (child BOMs + items)
  - Source: past project / quotation
  - Target: feeder or parent BOM
  - Mark copied BOM as instance (copy-never-link)
  - Populate `origin_master_bom_id` if from master
  - Populate `instance_sequence_no`
  - UI action: "Copy BOM from existing quotation"

#### P6-UI-REUSE-005: Apply Master BOM template
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Routes:** `POST /quotation/{id}/bom/{parentBomId}/master-bom/{masterBomId}`
- **Controller:** `QuotationV2Controller@applyMasterBom`
- **Features:**
  - Apply Master BOM (L1 products only per Phase-5 Canon)
  - Populate `origin_master_bom_id`
  - Populate `instance_sequence_no`
  - Immediately enter L0→L1→L2 resolution flow
  - UI action: "Apply Master BOM template"
  - Integration with Master BOM selection UI

---

### Week 4: Editability & Guardrails Validation (2 tasks)

#### P6-UI-REUSE-006: Post-reuse editability check
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Verify all copied content is editable
  - Add / remove / replace items allowed
  - Quantity changes allowed
  - Pricing overrides allowed
  - Locking respected (D-005) - line-item only
  - Test editability after:
    - Quotation copy
    - Panel copy
    - Feeder copy
    - BOM copy
    - Master BOM application
  - **File:** `docs/PHASE_6/UI/REUSE_EDITABILITY_VALIDATION.md`

#### P6-UI-REUSE-007: Guardrail enforcement after reuse
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Verify G1-G8 enforced on reused content
  - G1: No ProductId leaks into Master BOM
  - G2: Production BOM requires ProductId at L2
  - G3: IsPriceMissing normalizes Amount
  - G4: RateSource consistency
  - G5: UNRESOLVED normalizes values
  - G6: FIXED_NO_DISCOUNT forces Discount=0
  - G7: Discount range validation 0-100
  - G8: L1-SKU reuse allowed
  - Test guardrail enforcement after each reuse operation
  - **File:** `docs/PHASE_6/VALIDATION/REUSE_GUARDRAIL_VALIDATION.md`

---

## TRACK B: CATALOG TOOLING (16 Tasks)

### Week 3: Catalog Import UI Foundation (4 tasks)

#### P6-CAT-001: Design catalog import UI
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/CATALOG/CATALOG_IMPORT_UI_DESIGN.md`
- **Details:**
  - File upload interface
  - Series selection
  - Import preview
  - Validation results display

#### P6-CAT-002: Implement catalog file upload
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/catalog/import`
- **Views:** `resources/views/catalog/import.blade.php`
- **Features:**
  - File upload form (XLSX, CSV)
  - Series dropdown selection
  - Upload progress indicator

#### P6-CAT-003: Implement catalog import parser
- **Type:** Implementation
- **Deliverable:** Functional backend service
- **Features:**
  - Parse XLSX/CSV files
  - Validate file format
  - Extract SKU data
  - Extract price data
  - Error handling for malformed files

#### P6-CAT-004: Implement import preview
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Display parsed data preview
  - Show record count
  - Show validation status
  - Allow edit before import

---

### Week 4: Series-wise Catalog Onboarding (4 tasks)

#### P6-CAT-005: Design series onboarding workflow
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/CATALOG/SERIES_ONBOARDING_WORKFLOW.md`
- **Details:**
  - Series selection
  - Template selection
  - Data mapping
  - Validation rules

#### P6-CAT-006: Implement series selection
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Integration:** catalog_series table
- **Features:**
  - Series dropdown (LC1E, etc.)
  - Series-specific templates
  - Series-specific validation rules

#### P6-CAT-007: Implement data mapping UI
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Column mapping interface
  - Source column → target field mapping
  - Mapping validation
  - Save mapping template

#### P6-CAT-008: Implement series-specific import scripts
- **Type:** Implementation
- **Deliverable:** Functional backend scripts
- **Features:**
  - LC1E import script
  - Generic import script template
  - Series-specific transformation logic
  - Integration with catalog pipeline

---

### Week 5: Validation Previews (4 tasks)

#### P6-CAT-009: Design validation preview system
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/CATALOG/VALIDATION_PREVIEW_DESIGN.md`
- **Details:**
  - Pre-import validation
  - Validation rule display
  - Validation results summary
  - Error/warning details

#### P6-CAT-010: Implement pre-import validation
- **Type:** Implementation
- **Deliverable:** Functional backend service
- **Features:**
  - Run validation rules before import
  - Check required fields
  - Check data types
  - Check referential integrity
  - Check business rules

#### P6-CAT-011: Implement validation results display
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Validation summary (pass/fail/warning count)
  - Detailed validation errors
  - Validation warnings
  - Line-by-line validation status

#### P6-CAT-012: Implement validation rule configuration
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Series-specific validation rules
  - Custom validation rules
  - Rule priority
  - Rule enable/disable

---

### Week 6: Catalog Governance Enforcement (4 tasks)

#### P6-CAT-013: Design catalog governance UI
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/CATALOG/CATALOG_GOVERNANCE_UI.md`
- **Details:**
  - Governance dashboard
  - Approval workflow
  - Change tracking

#### P6-CAT-014: Implement catalog approval workflow
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Integration:** Phase-5 Catalog Governance SOP
- **Features:**
  - Submit for approval
  - Approval queue
  - Approve/reject actions
  - Approval comments

#### P6-CAT-015: Implement change tracking
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Track catalog changes
  - Change history display
  - Diff view (before/after)
  - Change author and timestamp

#### P6-CAT-016: Implement governance enforcement
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Prevent unauthorized changes
  - Enforce approval workflow
  - Enforce validation rules
  - Audit log integration

---

## TRACK C: OPERATIONAL READINESS (12 Tasks)

### Week 7: Role-based Access & Approval Flows (6 tasks)

#### P6-OPS-001: Design role-based access system
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/OPS/ROLE_BASED_ACCESS_DESIGN.md`
- **Details:**
  - Role definitions (Admin, Catalog Manager, User, Viewer)
  - Permission matrix
  - Access control rules

#### P6-OPS-002: Implement basic role system
- **Type:** Implementation
- **Deliverable:** Functional backend system
- **Database:**
  - Create roles table (if not exists)
  - Create user_roles table
- **Features:**
  - Role assignment UI
  - Role-based route protection

#### P6-OPS-003: Implement permission checks
- **Type:** Implementation
- **Deliverable:** Functional middleware/guards
- **Features:**
  - Middleware for role checking
  - Controller-level permission checks
  - View-level permission checks
  - API-level permission checks

#### P6-OPS-004: Design approval flows
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/OPS/APPROVAL_FLOWS_DESIGN.md`
- **Details:**
  - Price change approval
  - Override approval
  - Catalog change approval

#### P6-OPS-005: Implement price change approval
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Submit price change request
  - Approval queue for price changes
  - Approve/reject with comments
  - Notification system

#### P6-OPS-006: Implement override approval
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Submit override request
  - Approval queue for overrides
  - Approve/reject with comments
  - Override reason tracking

---

### Week 8: Audit Visibility & SOPs (5 tasks)

#### P6-OPS-007: Design audit visibility UI
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/OPS/AUDIT_VISIBILITY_DESIGN.md`
- **Details:**
  - Audit log display
  - Filter and search
  - Export functionality

#### P6-OPS-008: Implement audit log display
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/audit/logs`
- **Views:** `resources/views/audit/logs.blade.php`
- **Features:**
  - Display audit entries (read-only)
  - Filter by user, action, date range
  - Search functionality

#### P6-OPS-009: Implement audit log details
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Detailed audit entry view
  - Before/after values
  - Change diff display
  - User and timestamp information

#### P6-OPS-010: Create initial SOPs
- **Type:** Documentation
- **Deliverable:** SOP documents
- **File:** `docs/PHASE_6/OPS/INITIAL_SOPS.md`
- **Content:**
  - Catalog import SOP
  - Price approval SOP
  - Override approval SOP
  - Error handling SOP

#### P6-OPS-011: Implement audit export
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Export audit logs to CSV
  - Export audit logs to PDF
  - Date range selection
  - Filter preservation in export

---

## TRACK D0: COSTING ENGINE FOUNDATIONS (7 Tasks) ⭐ NEW

**Purpose:** Build canonical costing engine (QCD) before UI/reporting

### Week 3: Quantity + Cost Engine Base (3 tasks)

#### P6-COST-D0-001: Implement EffectiveQty logic (trait/helper)
- **Type:** Implementation
- **Deliverable:** Functional service/trait
- **Features:**
  - BaseQty → EffQtyPerPanel → EffQtyTotal formulas
  - Integration with QuotationQuantityService
  - Protected formula (cannot be changed)
  - **File:** `docs/PHASE_6/COSTING/MANUAL/EFFECTIVE_QTY_FORMULAS.md`

#### P6-COST-D0-002: Implement CostHead mapping precedence (D-006)
- **Type:** Implementation
- **Deliverable:** Functional service
- **Features:**
  - Item override (highest priority)
  - Product default (medium priority)
  - System default (lowest priority)
  - Integration with CostHead resolution service
  - **File:** `docs/PHASE_6/COSTING/MANUAL/COSTHEAD_PRECEDENCE.md`

#### P6-COST-D0-003: Implement QCD generator + JSON endpoint
- **Type:** Implementation
- **Deliverable:** Functional service + API endpoint
- **Routes:** `/quotation/{id}/export/cost-detail/json`
- **Features:**
  - Create QuotationCostDetail (QCD) canonical dataset (BOM-only, stable contract)
  - Generate QCD for quotation
  - QCD schema definition
  - JSON export endpoint
  - **File:** `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`

#### P6-COST-D0-008: Seed generic cost heads for cost adders ⭐ NEW
- **Type:** Implementation
- **Deliverable:** Seed data populated
- **Features:**
  - Seed cost heads in `cost_heads` table:
    - MATERIAL (already exists via BOM)
    - BUSBAR
    - FABRICATION
    - LABOUR
    - TRANSPORTATION
    - ERECTION
    - COMMISSIONING
    - MISC
  - Set CostBucket mapping (for summary roll-up lines):
    - BUSBAR → MATERIAL
    - FABRICATION → MATERIAL (summary line bucket; detail lines can be MATERIAL/LABOUR/OTHER)
    - LABOUR → LABOUR
    - TRANSPORTATION → OTHER
    - ERECTION → LABOUR
    - COMMISSIONING → OTHER
  - **Note:** Summary bucket comes from cost_heads.category; detail line buckets set in template lines
  - Tenant-scoped seed data
  - **File:** `docs/PHASE_6/COSTING/COST_HEADS_SEED.md`
  - **Dependency:** After cost_heads table exists (Track E, Week 0-1)

---

### Week 4: Export Baseline + Numeric Validation (2 tasks)

#### P6-COST-D0-004: QCD Excel export (sheet-1 only, minimal formatting)
- **Type:** Implementation
- **Deliverable:** Functional export feature
- **Features:**
  - Export QCD to Excel format
  - Sheet 1: Panel summary (minimal formatting)
  - Basic Excel structure
  - **File:** `docs/PHASE_6/COSTING/MANUAL/EXCEL_EXPORT_STRUCTURE.md`

#### P6-COST-D0-005: Numeric validation vs Excel reference (engine-first)
- **Type:** Verification
- **Deliverable:** Validation report
- **Features:**
  - Compare QCD engine output with reference Excel
  - Validate numeric accuracy
  - Engine is source of truth, Excel is consumer
  - Document any discrepancies
  - **File:** `docs/PHASE_6/COSTING/MANUAL/NUMERIC_VALIDATION.md`

#### P6-COST-D0-009: Create cost template master tables ⭐ NEW
- **Type:** Implementation
- **Deliverable:** Database tables created
- **Features:**
  - `cost_templates` table (one per cost head)
  - `cost_template_lines` table (rows per template)
  - Migration script
  - Fields:
    - cost_templates: id, tenant_id, cost_head_id, name, version, is_active
    - cost_template_lines: id, cost_template_id, line_name, calc_mode, default_uom, default_rate, line_cost_bucket (MATERIAL/LABOUR/OTHER, nullable), sort_order
  - **Note:** `line_cost_bucket` allows each template line to have its own CostBucket (e.g., Fabrication sheet: steel=MATERIAL, coating=OTHER, manpower=LABOUR)
  - **File:** `docs/PHASE_6/COSTING/COST_TEMPLATE_SCHEMA.md`
  - **Dependency:** After cost heads seeded (P6-COST-D0-008)

#### P6-COST-D0-010: Create cost sheet runtime tables ⭐ NEW
- **Type:** Implementation
- **Deliverable:** Database tables created
- **Features:**
  - `quote_cost_sheets` table (one per panel per cost head)
  - `quote_cost_sheet_lines` table (instantiated template lines)
    - Include `line_cost_bucket` field (inherited from template, can override)
  - `quote_cost_adders` table (summary roll-up, one per panel per cost head)
    - Summary bucket comes from `cost_heads.category` (not aggregated from lines)
  - Migration script
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_SCHEMA.md`
  - **Dependency:** After template tables (P6-COST-D0-009)

---

### Week 5-6: Performance + Gate + Cost Sheet Calculation & Roll-Up (NEW - Cost Adders)

#### P6-COST-D0-011: Implement cost sheet calculation engine ⭐ NEW
- **Type:** Implementation
- **Deliverable:** Functional calculation engine
- **Features:**
  - Row-level calculation:
    - LUMP_SUM: amount = rate
    - QTY_RATE: amount = qty × rate
    - KG_RATE: amount = qty × rate (qty in kg)
    - METER_RATE: amount = qty × rate (qty in meters)
    - HOUR_RATE: amount = qty × rate (qty in hours)
    - PERCENT_OF_BASE: amount = base_cost × (rate / 100) (Commissioning only)
  - Sheet total calculation: SUM(all line amounts)
  - Validation (no negative values, locked rows)
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_CALCULATION.md`
  - **Dependency:** After runtime tables (P6-COST-D0-010)

#### P6-COST-D0-012: Implement cost adder roll-up generator ⭐ NEW
- **Type:** Implementation
- **Deliverable:** Functional roll-up service
- **Features:**
  - When cost sheet saved/approved:
    - Calculate sheet total: SUM(quote_cost_sheet_lines.amount)
    - Upsert row in quote_cost_adders:
      - quotation_id, quote_panel_id, cost_head_id
      - amount = sheet_total × PanelQty (per-panel multiplication)
      - status = sheet status
      - source_sheet_id = sheet.id
      - **Note:** Summary bucket comes from cost_heads.category (not aggregated from line buckets)
  - **Critical:** Roll-up line uses `cost_heads.category` (default bucket) for reporting; sheet line buckets (`line_cost_bucket`) are for drill-down analysis only. Do not aggregate line buckets into the summary bucket.
  - Auto-recalculate on sheet line changes
  - **File:** `docs/PHASE_6/COSTING/COST_ADDER_ROLLUP.md`
  - **Dependency:** After calculation engine (P6-COST-D0-011)

#### P6-COST-D0-013: Implement QCA (Quote Cost Adders) dataset ⭐ NEW
- **Type:** Implementation
- **Deliverable:** Functional service + API endpoint
- **Routes:** `/quotation/{id}/export/cost-adders/json`
- **Features:**
  - QCA = canonical dataset from quote_cost_adders table
  - One row per panel per cost head (summary)
  - JSON export endpoint
  - QCA schema definition
  - **Note:** QCD remains BOM-only (stable contract)
  - **File:** `docs/PHASE_6/COSTING/QCA_CONTRACT_v1.0.md`
  - **Dependency:** After roll-up generator (P6-COST-D0-012)

#### P6-COST-D0-014: Update D0 Gate checklist to include cost adders ⭐ NEW
- **Type:** Gate Verification
- **Deliverable:** Updated gate checklist
- **Gate Checklist:**
  - QCD generator functional (BOM-only, unchanged)
  - QCA generator functional (cost adders summary)
  - Cost sheet calculation engine working
  - Roll-up generator working
  - Performance acceptable with cost adders (< 5 seconds for typical quotation)
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md` (update)
  - **Gate:** Must pass before Track D (Costing & Reporting) can proceed

#### P6-COST-D0-006: Performance hardening for large quotations
- **Type:** Optimization
- **Deliverable:** Performance report
- **Features:**
  - Test with large quotations (100+ panels, 1000+ items)
  - Optimize QCD generation performance
  - Optimize quantity calculations
  - Optimize CostHead resolution
  - Optimize cost adders calculation and roll-up
  - Performance targets: < 5 seconds for typical quotation

#### P6-COST-D0-007: D0 Gate signoff (QCD v1.0 stable + QCA v1.0 stable)
- **Type:** Gate Verification
- **Deliverable:** Gate signoff document
- **Gate Checklist:**
  - QCD generator functional (BOM-only)
  - QCA generator functional (cost adders)
  - QCD JSON endpoint working
  - QCA JSON endpoint working
  - Numeric validation passing
  - Performance acceptable for large quotations (with cost adders)
  - **Gate:** Must pass before Track D (Costing & Reporting) can proceed
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_SIGNOFF.md`

---

## TRACK D: COSTING & REPORTING (18 Tasks) ⭐ MODIFIED

**Purpose:** Replace manual Excel costing with automated costing engine and dashboards
**Key Change:** Consumes QCD only (no duplicate calculators)

### Week 7: Costing Pack Foundation (4 tasks)

#### P6-COST-001: Design Costing Pack UI
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/COSTING/COSTING_PACK_DESIGN.md`
- **Reference:** `features/project/reports/COSTING_DASHBOARD_PROJECT_BRIEF.md`
- **Details:**
  - Costing Pack per quotation structure
  - Snapshot view design
  - Panel summary view design
  - Pivot table design

#### P6-COST-002: Confirm D0 Gate passed (QCD stable)
- **Type:** Gate Verification
- **Deliverable:** Gate verification document
- **File:** `docs/PHASE_6/COSTING/D0_GATE_VERIFICATION.md`
- **Verification:**
  - Verify D0 Gate signoff complete
  - Verify QCD v1.0 stable
  - Verify QCD JSON endpoint functional

#### P6-COST-003: Implement quotation costing snapshot
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/quotation/{id}/costing/snapshot`
- **Views:** `resources/views/quotation/costing/snapshot.blade.php`
- **Data Source:** QCD aggregates (not "CostingService")
- **Features:**
  - Display quotation-level costing summary
  - Display total cost, margin, hit rate
  - Aggregate from QCD dataset

#### P6-COST-004: Implement panel summary view
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/quotation/{id}/costing/panels`
- **Views:** `resources/views/quotation/costing/panels.blade.php`
- **Data Source:** QCD aggregates
- **Features:**
  - Display panel-level costing breakdown
  - Display panel costs, margins, quantities
  - Panel cost per unit display
  - Aggregate from QCD dataset

---

### Week 8: Costing Pack Details & Pivots (4 tasks)

#### P6-COST-005: Implement BOM/Feeder costing breakdown
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Data Source:** Derived via QCD + tree
- **Features:**
  - Display feeder-level costing
  - Display BOM-level costing
  - Display component-level costing
  - Hierarchy visualization
  - Derived from QCD dataset

#### P6-COST-006: Implement CostHead grouping
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Integration:** Phase-5 CostHead system
- **Features:**
  - CostHead category display
  - CostHead-based cost aggregation
  - CostBucket mappings
  - CostHead pivot view

#### P6-COST-007: Implement pivot tables
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Panel × CostHead pivot
  - Feeder × Component pivot
  - CostHead × Panel pivot
  - **Must include CostHead pivot + Category/Make/RateSource**
  - Interactive pivot controls
  - Export pivot data

#### P6-COST-008: Implement costing pack navigation
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Tab navigation (Snapshot, Panels, Breakdown, Pivots)
  - Breadcrumb navigation
  - Quick links between views
  - Print-friendly views

---

### Week 9: Global Dashboard (5 tasks)

#### P6-COST-009: Design global dashboard
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/COSTING/GLOBAL_DASHBOARD_DESIGN.md`
- **Details:**
  - Margins dashboard design
  - Hit rates dashboard design
  - Cost drivers dashboard design
  - KPI visualization design

#### P6-COST-010: Implement margins dashboard
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/dashboard/margins`
- **Views:** `resources/views/dashboard/margins.blade.php`
- **Data Source:** All dashboard aggregations come from QCD across quotations
- **Features:**
  - Display quotation margins
  - Margin trends over time
  - Margin by panel/feeder
  - Target margin comparison

#### P6-COST-011: Implement hit rates dashboard
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/dashboard/hit-rates`
- **Views:** `resources/views/dashboard/hit-rates.blade.php`
- **Data Source:** All dashboard aggregations come from QCD across quotations
- **Features:**
  - Display quotation hit rates
  - Hit rate trends
  - Hit rate by client/project
  - Win/loss analysis

#### P6-COST-012: Implement cost drivers dashboard
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/dashboard/cost-drivers`
- **Views:** `resources/views/dashboard/cost-drivers.blade.php`
- **Data Source:** All dashboard aggregations come from QCD across quotations
- **Features:**
  - Display top cost drivers
  - CostHead analysis
  - Component cost analysis
  - Cost trend analysis

#### P6-COST-013: Implement dashboard filters
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Date range filters
  - Client/project filters
  - Panel/feeder filters
  - CostHead filters
  - Filter persistence

---

### Week 10: Excel Export & Integration (5 tasks)

#### P6-COST-014: Design Excel export functionality
- **Type:** Design
- **Deliverable:** Design document
- **File:** `docs/PHASE_6/COSTING/EXCEL_EXPORT_DESIGN.md`
- **Details:**
  - Export formats (XLSX, CSV)
  - Export templates
  - Export data structure

#### P6-COST-015: Implement Costing Pack Excel export (engine-first)
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Export should be engine-first
  - Sheet 1: Panel summary
  - Sheet 2: Detailed BOM (QCD)
  - Sheet 3: Pivot shells (optional)
  - Excel formatting (headers, formulas)
  - **Note:** Charts/graphs optional unless requested

#### P6-COST-016: Implement dashboard Excel export
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Export margins dashboard data
  - Export hit rates dashboard data
  - Export cost drivers dashboard data
  - Export filtered views

#### P6-COST-017: Implement costing calculation UI integration
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Integration:** QCD generator (not separate CostingService)
- **Features:**
  - Real-time costing calculation display (from QCD)
  - Cost recalculation triggers (regenerate QCD)
  - Cost validation indicators
  - Cost discrepancy warnings

#### P6-COST-018: Implement costing pack access control
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Integration:** Track C role system
- **Features:**
  - Role-based access (Finance, Sales, Management)
  - Dashboard access permissions
  - Export permissions

---

## TRACK E: CANON IMPLEMENTATION & CONTRACT ENFORCEMENT (~28 Tasks) ⭐ NEW

**Purpose:** Implement all Phase-5 frozen items

### Weeks 0-1: Database Implementation from Schema Canon (4 tasks)

#### P6-DB-001: Choose DB creation approach (DDL vs migrations) and lock method for Canon v1.0
- **Type:** Decision
- **Deliverable:** Decision document
- **File:** `docs/PHASE_6/DB/DB_CREATION_METHOD.md`
- **Features:**
  - Review Schema Canon v1.0 DDL
  - Decide: Direct DDL execution OR Laravel migrations
  - Lock chosen method

#### P6-DB-002: Implement DB schema from Schema Canon v1.0 (DDL or migrations)
- **Type:** Implementation
- **Deliverable:** Database created
- **Features:**
  - Create Laravel migration files from DDL (if migrations chosen)
  - OR execute DDL directly (if DDL chosen)
  - Ensure all 34 tables are covered
  - Ensure all constraints (PK, FK, CHECK, UNIQUE) are included
  - Ensure all indexes per Schema Canon are included
  - **File:** `docs/PHASE_6/DB/SCHEMA_MIGRATION_PLAN.md`

#### P6-DB-003: Execute seed script (C5) on dev/stage
- **Type:** Implementation
- **Deliverable:** Seed data populated
- **Features:**
  - Review seed script requirements from Schema Canon
  - Execute seed scripts
  - Verify seed data populated
  - Verify referential integrity maintained

#### P6-DB-004: Schema parity gate (DB == Canon v1.0)
- **Type:** Verification
- **Deliverable:** Parity report
- **Gate:** Must pass before proceeding to UI work
- **Features:**
  - Compare actual database schema with Schema Canon
  - Verify table structures match
  - Verify column types match
  - Verify constraints match
  - Verify indexes match
  - Document any discrepancies
  - **File:** `docs/PHASE_6/DB/SCHEMA_PARITY_REPORT.md`

---

### Weeks 2-4: Guardrails Runtime Enforcement (4 tasks)

#### P6-VAL-001: Implement runtime guardrails G1-G8 in service layer
- **Type:** Implementation
- **Deliverable:** Functional service layer
- **Features:**
  - Implement G1: Master BOM rejects ProductId (service validation)
  - Implement G2: Production BOM requires ProductId (service validation)
  - Implement G3: IsPriceMissing normalizes Amount (pricing service)
  - Implement G4: RateSource consistency (pricing service)
  - Implement G5: UNRESOLVED normalizes values (pricing service)
  - Implement G6: FIXED_NO_DISCOUNT forces Discount=0 (discount service)
  - Implement G7: Discount range validation 0-100 (discount service)
  - Implement G8: L1-SKU reuse allowed (L1 validation service)
  - **File:** `docs/PHASE_6/VALIDATION/GUARDRAILS_IMPLEMENTATION.md`

#### P6-VAL-002: Ensure DB constraints/normalization aligns with guardrail docs
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Verify all CHECK constraints from Schema Canon are in migrations
  - Verify G7 discount range constraint (0-100) in DB
  - Verify resolution_status constraints in DB
  - Verify ProductId constraints in DB
  - Test constraint enforcement

#### P6-VAL-003: API validation parity with 02_VALIDATION_MATRIX.md
- **Type:** Implementation
- **Deliverable:** Functional API validation
- **Features:**
  - Review validation matrix from Phase-5
  - Implement API validation matching DB guardrails
  - Ensure all 8 guardrails validated at API layer
  - Map validation errors to error taxonomy codes

#### P6-VAL-004: Guardrail test suite (unit + integration)
- **Type:** Testing
- **Deliverable:** Test suite
- **Features:**
  - Create unit tests for each guardrail (G1-G8)
  - Create integration tests for guardrail enforcement
  - Test normalization behavior
  - Test constraint violations
  - Test error messages

---

### Weeks 3-6: API Contracts (B1-B4) Implementation OR Explicit Defer (6 tasks)

#### P6-API-001: Implement endpoints per 01_API_SURFACE_MAP.md
- **Type:** Implementation
- **Deliverable:** Functional API endpoints
- **Features:**
  - Review API Surface Map from Phase-5
  - Implement all read endpoints
  - Implement all write endpoints
  - Ensure endpoint paths match contract
  - **File:** `docs/PHASE_6/API/ENDPOINT_IMPLEMENTATION.md`

#### P6-API-002: Request/response schemas per OpenAPI skeleton
- **Type:** Implementation
- **Deliverable:** Functional API schemas
- **Features:**
  - Review OpenAPI skeleton from Phase-5
  - Implement request validation per schemas
  - Implement response formatting per schemas
  - Ensure schema compliance

#### P6-API-003: Error taxonomy + request_id propagation
- **Type:** Implementation
- **Deliverable:** Functional error handling
- **Features:**
  - Review error taxonomy from Phase-5 (03_ERROR_TAXONOMY.md)
  - Implement error code mapping
  - Implement error envelope format
  - Implement request_id generation and propagation
  - Ensure HTTP status codes match taxonomy

#### P6-API-004: Versioning rules applied
- **Type:** Implementation
- **Deliverable:** Functional versioning
- **Features:**
  - Review versioning policy from Phase-5 (04_VERSIONING_POLICY.md)
  - Implement URL-based versioning (v1)
  - Implement backward compatibility checks
  - Document version bump process

#### P6-API-005: Contract tests
- **Type:** Testing
- **Deliverable:** Test suite
- **Features:**
  - Create contract tests for all endpoints
  - Test request/response schemas
  - Test validation rules
  - Test error responses
  - Test versioning compliance

#### P6-API-DECISION: If deferring, write signed "defer to Phase-7" memo
- **Type:** Decision Documentation
- **Deliverable:** Deferral memo
- **Features:**
  - Document decision to defer API implementation
  - Get stakeholder sign-off
  - Document in Phase-6 closure report
  - **File:** `docs/PHASE_6/API/API_DEFER_DECISION.md`

---

### Weeks 3-6: Multi-SKU Linkage (D-007) (3 tasks)

#### P6-SKU-001: Implement parent_line_id grouping + metadata_json rules
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Support parent_line_id for grouping related SKUs
  - Define metadata_json structure for multi-SKU
  - Group creation/editing logic
  - Integration with BOM item creation

#### P6-SKU-002: UI rendering of grouped multi-SKU lines
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Display multi-SKU groups in UI
  - Show group relationships
  - Visual grouping indicators
  - Handle group operations (add/remove from group)

#### P6-SKU-003: Safe edit validation for metadata_json
- **Type:** Implementation
- **Deliverable:** Functional validation
- **Features:**
  - Create UI for editing metadata_json (safe editing)
  - Validate metadata_json structure
  - Store metadata_json with BOM items
  - Validation rules enforcement

---

### Weeks 3-6: Discount Editor (Legacy Parity / Performance) (4 tasks)

#### P6-DISC-001: Implement /quotation/{id}/discount
- **Type:** Implementation
- **Deliverable:** Functional UI page
- **Routes:** `/quotation/{id}/discount`
- **Views:** `resources/views/quotation/discount.blade.php`
- **Controller:** `QuotationDiscountController@index`
- **Features:**
  - Display discount editor interface
  - **File:** `docs/PHASE_6/UI/DISCOUNT_EDITOR_DESIGN.md`

#### P6-DISC-002: Filters (Make/Category/Item/Desc/SKU/Panel/Feeder/BOM)
- **Type:** Implementation
- **Deliverable:** Functional filters
- **Features:**
  - Filter by Make
  - Filter by Category/SubCategory/Item
  - Filter by Description
  - Filter by SKU
  - Filter by Panel
  - Filter by Feeder
  - Filter by BOM
  - Multi-filter support

#### P6-DISC-003: Preview + Apply (transaction) + audit log
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - Preview discount changes before applying
  - Show affected items count
  - Show total discount impact
  - Apply discounts in transaction
  - Rollback on error
  - Log all bulk discount operations

#### P6-DISC-004: Hook approvals (Track C) for bulk updates if required
- **Type:** Implementation
- **Deliverable:** Functional approval integration
- **Features:**
  - Require approval for large discount changes (configurable threshold)
  - Integration with Track C approval workflow
  - Audit trail for discount changes

---

### Weeks 2-4: BOM Tracking Fields Runtime Behavior (3 tasks)

#### P6-BOM-TRACK-001: Populate BOM tracking fields on create/copy
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - When creating BOM from master, populate `origin_master_bom_id`
  - When creating BOM instance, populate `instance_sequence_no`
  - When copying BOM, increment `instance_sequence_no`
  - Integration with BOM creation/copy logic

#### P6-BOM-TRACK-002: Update is_modified/modified_by/modified_at on edits
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - When BOM item is edited, set `is_modified = true`
  - Populate `modified_by` with current user
  - Populate `modified_at` with current timestamp
  - Integration with BOM edit logic

#### P6-BOM-TRACK-003: UI indicator "modified vs original" (read-only badge)
- **Type:** Implementation
- **Deliverable:** Functional UI component
- **Features:**
  - Display badge on BOMs that are modified
  - Show "Modified" indicator on BOM items
  - Show modification timestamp
  - Read-only display (no edit capability)

---

### Week 1: Customer Snapshot Handling (2 tasks)

#### P6-UI-001A: Ensure customer_name_snapshot always stored (D-009)
- **Type:** Implementation
- **Deliverable:** Functional feature
- **Features:**
  - When creating quotation, always populate `customer_name_snapshot`
  - If customer_id provided, copy customer name to snapshot
  - If customer_id NULL, use provided customer name for snapshot
  - Integration with quotation creation flow

#### P6-UI-001B: customer_id remains nullable (D-009)
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Ensure customer_id can be NULL
  - Support quotation creation without customer_id
  - Support future customer normalization

---

### Week 4: Resolution Constraints Enforcement (2 tasks)

#### P6-RES-023: Enforce resolution constraints exactly as Schema Canon
- **Type:** Implementation
- **Deliverable:** Functional enforcement
- **Features:**
  - Enforce MBOM: L0/L1 only, no ProductId
  - Enforce QUO: L0/L1/L2 allowed, L2 requires ProductId
  - Enforce CHECK constraints at DB level
  - Enforce constraints at service level
  - Enforce constraints at UI level (prevent invalid selections)

#### P6-RES-024: Errors must map to B3 error taxonomy codes
- **Type:** Implementation
- **Deliverable:** Functional error mapping
- **Features:**
  - Review error taxonomy from Phase-5 (03_ERROR_TAXONOMY.md)
  - Map resolution errors to taxonomy codes
  - Ensure error messages match taxonomy
  - Ensure HTTP status codes match taxonomy
  - Ensure request_id propagation

---

### Week 5: Locking Scope Verification (1 task)

#### P6-LOCK-000: Verify no higher-level locking introduced (schema + UI)
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Verify no is_locked field on quote_boms (BOM level)
  - Verify no is_locked field on quote_panels (Panel level)
  - Verify no is_locked field on quotations (Quotation level)
  - Verify locking only at quote_bom_items level (line-item only)
  - Document locking scope per D-005 decision

---

## LEGACY PARITY VERIFICATION GATE (6 Tasks) ⭐ NEW

**Purpose:** Verify all legacy capabilities preserved through reuse workflows

### Week 8.5: Legacy Parity Gate Checklist

#### P6-GATE-LEGACY-001: Quotation reuse verified
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Copy old quotation → modify works
  - Full hierarchy copied correctly
  - BOM tracking fields populated
  - Editability maintained

#### P6-GATE-LEGACY-002: Panel reuse verified
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Copy panel subtree works
  - Source: same or past quotation
  - Editability maintained

#### P6-GATE-LEGACY-003: Feeder reuse verified
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Copy feeder (Level-0 BOM) works
  - Full subtree copied
  - Editability maintained

#### P6-GATE-LEGACY-004: BOM reuse verified
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - Copy BOM from past quotation works
  - Master BOM application works
  - Copy-never-link semantics respected
  - Editability maintained

#### P6-GATE-LEGACY-005: Post-reuse guardrails verified
- **Type:** Verification
- **Deliverable:** Verification report
- **Features:**
  - All guardrails (G1-G8) enforced
  - No schema canon violations
  - Locking scope respected (D-005)

#### P6-GATE-LEGACY-006: Legacy parity checklist complete
- **Type:** Verification
- **Deliverable:** Checklist completion
- **Features:**
  - Reference: `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`
  - All checklist items verified
  - No legacy workflow blocked

**Gate Rule:** Phase-6 cannot proceed to Integration unless all legacy parity items are verified.

---

## INTEGRATION & STABILISATION (12 Tasks)

### Week 9: End-to-End Integration (5 tasks)

#### P6-INT-001: End-to-end quotation creation test
- **Type:** Testing
- **Deliverable:** Test results
- **Test Flow:**
  - Create quotation
  - Add panel
  - Add feeder
  - Add BOM
  - Add components
  - Complete L0→L1→L2 resolution
  - Set pricing
  - Lock items
  - Verify audit trail

#### P6-INT-002: End-to-end catalog import test
- **Type:** Testing
- **Deliverable:** Test results
- **Test Flow:**
  - Upload catalog file
  - Select series
  - Map columns
  - Run validation
  - Submit for approval
  - Approve import
  - Verify data in system

#### P6-INT-003: Integration testing
- **Type:** Testing
- **Deliverable:** Test results
- **Tests:**
  - UI → API integration tests
  - Resolution engine integration tests
  - Pricing engine integration tests
  - Locking engine integration tests
  - Catalog pipeline integration tests

#### P6-INT-004: Cross-track integration
- **Type:** Testing
- **Deliverable:** Test results
- **Integration Points:**
  - Catalog import → Quotation UI
  - Pricing resolution → UI display
  - Locking → UI visibility
  - Audit → UI display
  - Costing engine → Costing Pack UI
  - Quotation UI → Costing Pack
  - Costing Pack → Global Dashboard

#### P6-INT-005: Performance testing
- **Type:** Testing
- **Deliverable:** Performance report
- **Tests:**
  - Quotation load time
  - Catalog import performance
  - UI responsiveness
  - Database query optimization

#### P6-INT-006: End-to-end costing pack test
- **Type:** Testing
- **Deliverable:** Test results
- **Test Flow:**
  - Create quotation with panels/feeders/BOMs
  - Generate QCD
  - Generate costing pack (from QCD)
  - Verify snapshot calculations
  - Verify panel summary
  - Verify pivot tables
  - Export to Excel
  - Verify global dashboard data

#### P6-INT-006A: Validate QCD parity inside UI flows
- **Type:** Verification
- **Deliverable:** Validation report
- **Features:**
  - Snapshot totals == Panel totals == Export totals
  - All costing displays use same QCD source
  - No calculation discrepancies
  - **File:** `docs/PHASE_6/INTEGRATION/QCD_PARITY_VALIDATION.md`

#### P6-INT-007: Reuse workflow integration test
- **Type:** Testing
- **Deliverable:** Test results
- **Test Flow:**
  - Test quotation copy → modify → pricing → costing
  - Test panel copy → modify → pricing → costing
  - Test feeder copy → modify → pricing → costing
  - Test BOM copy → modify → pricing → costing
  - Test Master BOM apply → resolution → pricing → costing
  - Verify all reuse workflows work end-to-end
  - Verify guardrails enforced throughout
  - **File:** `docs/PHASE_6/INTEGRATION/REUSE_WORKFLOW_INTEGRATION.md`

---

### Week 10: Stabilisation & Polish (5 tasks)

#### P6-STAB-001: Bug fixes
- **Type:** Bug Fix
- **Deliverable:** Fixed bugs
- **Scope:**
  - Fix identified bugs
  - Fix UI inconsistencies
  - Fix validation issues
  - Fix integration issues

#### P6-STAB-002: UX polish
- **Type:** Enhancement
- **Deliverable:** Polished UI
- **Scope:**
  - Improve error messages
  - Improve loading states
  - Improve visual feedback
  - Improve navigation flow

#### P6-STAB-003: Documentation updates
- **Type:** Documentation
- **Deliverable:** Updated documentation
- **Scope:**
  - Update user documentation
  - Update API documentation
  - Update SOPs
  - Create user guides

#### P6-STAB-004: User acceptance testing
- **Type:** Testing
- **Deliverable:** UAT results
- **Scope:**
  - Internal user testing
  - Collect feedback
  - Address critical issues
  - Sign-off preparation

#### P6-STAB-005: Final verification
- **Type:** Verification
- **Deliverable:** Verification report
- **Scope:**
  - Verify all exit criteria met
  - Verify all success metrics met
  - Prepare Phase-6 closure report
  - Prepare handover to Phase-7

---

## CLOSURE (4 Tasks)

### Week 11: Buffer Week (3 tasks)

#### P6-BUF-001: Address any remaining issues
- **Type:** Bug Fix/Enhancement
- **Deliverable:** Resolved issues

#### P6-BUF-002: Final testing
- **Type:** Testing
- **Deliverable:** Final test results

#### P6-BUF-003: Documentation finalisation
- **Type:** Documentation
- **Deliverable:** Final documentation

---

### Week 12: Phase-6 Closure (4 tasks)

#### P6-CLOSE-001: Phase-6 exit criteria verification
- **Type:** Verification
- **Deliverable:** Exit criteria report
- **Criteria:**
  - ✅ A quotation can be created end-to-end
  - ✅ L1 selection reliably maps to L2 SKUs
  - ✅ Pricing resolution works with overrides
  - ✅ Catalog entries can be added safely
  - ✅ Errors are explainable to users

#### P6-CLOSE-002: Success metrics verification
- **Type:** Verification
- **Deliverable:** Metrics report
- **Metrics:**
  - ✅ Internal users can create quotations without errors
  - ✅ Catalog entries can be imported safely
  - ✅ Pricing overrides work correctly
  - ✅ Audit trail is visible and complete
  - ✅ Errors are understandable and actionable

#### P6-CLOSE-003: Create Phase-6 closure report
- **Type:** Documentation
- **Deliverable:** Closure report
- **Content:**
  - Summary of deliverables
  - Lessons learned
  - Known issues
  - Recommendations for Phase-7

#### P6-CLOSE-004: Handover to Phase-7
- **Type:** Handover
- **Deliverable:** Handover package
- **Content:**
  - Document system state
  - Document outstanding items
  - Prepare Phase-7 kickoff materials

#### P6-CLOSE-005: Canon compliance signoff
- **Type:** Verification
- **Deliverable:** Compliance signoff document
- **File:** `docs/PHASE_6/CLOSURE/CANON_COMPLIANCE_SIGNOFF.md`
- **Checklist:**
  - Schema parity (Canon v1.0)
  - Guardrails runtime parity (G1–G8)
  - API parity (or defer memo exists)
  - Locking scope respected (D-005)
  - CostHead precedence respected (D-006)
  - Multi-SKU linkage present (D-007)
  - Discount Editor delivered (legacy parity)
  - Customer snapshot handling (D-009)
  - Resolution constraints enforced (A10)

---

## 📊 Task Summary by Track

| Track | Tasks | Duration | Weeks | Status |
|-------|-------|----------|-------|--------|
| **Track A: Productisation** | 33 | 6 weeks | 1-6 | ⏳ PENDING |
| **Track A-R: Reuse & Legacy Parity** | 7 | 3 weeks | 2-4 | ⏳ PENDING |
| **Track B: Catalog Tooling** | 16 | 4 weeks | 3-6 | ⏳ PENDING |
| **Track C: Operational Readiness** | 12 | 2 weeks | 7-8 | ⏳ PENDING |
| **Track D0: Costing Engine Foundations** | 14 | 4 weeks | 3-6 | ⏳ PENDING |
| **Track D: Costing & Reporting** | 20 | 4 weeks | 7-10 | ⏳ PENDING |
| **Track E: Canon Implementation** | ~29 | 6 weeks | 0-6 | ⏳ PENDING |
| **Legacy Parity Gate** | 6 | 0.5 weeks | 8.5 | ⏳ PENDING |
| **Integration & Stabilisation** | 12 | 2 weeks | 9-10 | ⏳ PENDING |
| **Closure** | 5 | 2 weeks | 11-12 | ⏳ PENDING |
| **Entry Gate & Setup** | 3 | 1 week | 0 | ⏳ PENDING |
| **TOTAL** | **~133 tasks** | **10-12 weeks** | **0-12** | ⏳ PENDING |

---

## 🗓️ Timeline Overview

### Week 0: Entry Gate & Setup
- Entry criteria verification
- Project structure setup
- Task register creation

### Weeks 1-2: Track A Foundation
- Quotation & Panel UI
- Feeder & BOM Hierarchy UI

### Weeks 0-1: Track E Foundation (Database)
- **Track E:** Database implementation from Schema Canon
- **Gate:** Schema parity gate must pass before UI work

### Weeks 2-4: Track A + Track A-R + Track E (Parallel)
- **Track A:** Pricing Resolution UI, L0→L1→L2 Resolution UX
- **Track A-R:** Reuse workflows (quotation, panel, feeder, BOM)
- **Track E:** Guardrails enforcement, BOM tracking, Multi-SKU, Discount Editor

### Weeks 3-4: Track A + Track B + Track D0 + Track E (Parallel)
- **Track A:** Pricing Resolution UI, L0→L1→L2 Resolution UX
- **Track B:** Catalog Import UI, Series Onboarding
- **Track D0:** Costing Engine Foundations (QCD)
- **Track E:** API contracts, Multi-SKU, Discount Editor

### Weeks 5-6: Track A + Track B + Track D0 + Track E (Parallel)
- **Track A:** Locking Visibility, Error Handling
- **Track B:** Validation Previews, Governance Enforcement
- **Track D0:** Performance hardening, D0 Gate signoff
- **Track E:** API contracts completion

### Weeks 7-8: Track C + Track D (Parallel)
- **Track C:** Role-based Access, Approval Flows, Audit Visibility
- **Track D:** Costing Pack Foundation, Details & Pivots (requires D0 Gate passed)

### Week 8.5: Legacy Parity Gate
- **Legacy Parity Gate:** Verify all reuse workflows and legacy capabilities

### Weeks 9-10: Track D + Integration (Parallel)
- **Track D:** Global Dashboard, Excel Export
- **Integration:** End-to-end testing, cross-track integration, reuse workflow integration
- **Stabilisation:** Bug fixes, UX polish, UAT

### Weeks 11-12: Buffer & Closure
- Buffer week for remaining issues
- Exit criteria verification
- Phase-6 closure report
- Handover to Phase-7

---

## 🎯 Exit Criteria

Phase-6 is complete when ALL below are true:

1. ✅ A quotation can be created end-to-end
2. ✅ L1 selection reliably maps to L2 SKUs
3. ✅ Pricing resolution works with overrides
4. ✅ Catalog entries can be added safely
5. ✅ Errors are explainable to users
6. ✅ Costing Pack is functional per quotation
7. ✅ Global dashboard shows margins, hit rates, cost drivers
8. ✅ Excel exports work for costing and dashboards
9. ✅ Reuse workflows work (quotation, panel, feeder, BOM)
10. ✅ All legacy capabilities preserved
11. ✅ Canon compliance verified (schema, guardrails, decisions)

**Exit Artifact:** NSW v0.6 – Internal Product Ready

---

## 📈 Success Metrics

### Usability
- ✅ Internal users can create quotations without errors
- ✅ Average quotation creation time < 15 minutes
- ✅ User satisfaction score > 4/5

### Catalog Management
- ✅ Catalog entries can be imported safely
- ✅ Import validation catches 95%+ of errors before publish
- ✅ Series onboarding time < 2 hours per series

### Pricing
- ✅ Pricing overrides work correctly
- ✅ Price resolution accuracy > 99%
- ✅ Override approval time < 24 hours

### Costing & Reporting
- ✅ Costing Pack generates correctly for all quotations
- ✅ Global dashboard loads in < 5 seconds
- ✅ Excel exports match UI data 100%

### Audit & Governance
- ✅ Audit trail is visible and complete
- ✅ All changes are audited
- ✅ Approval workflows are enforced

### Error Handling
- ✅ Errors are understandable and actionable
- ✅ Error resolution time < 5 minutes
- ✅ User-reported error rate < 5%

---

## 🔗 Key Dependencies

### Critical Path
1. **Week 0:** Entry gate must pass before any work begins
2. **Week 1-2:** UI foundation must be complete before pricing/resolution UX
3. **Week 3-4:** Pricing UX must be complete before error handling
4. **Week 5-6:** Locking visibility must be complete before error handling
5. **Week 7-8:** Operational readiness needed for costing access control
6. **Week 9-10:** All tracks must be complete before integration
7. **Week 11-12:** Integration must be complete before closure

### Parallel Execution
- **Track B (Catalog Tooling)** runs in parallel with Track A (Weeks 3-6)
- **Track C (Operational Readiness)** runs in parallel with Track D start (Weeks 7-8)
- **Track D (Costing & Reporting)** runs in parallel with Track C (Weeks 7-10)
- **Integration** requires all tracks complete (Week 9)

---

## ⚠️ Key Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| UI complexity exceeds timeline | High | MVP screens only, defer polish to Phase-7 |
| Catalog import complexity | Medium | Start with single series (LC1E), expand later |
| Costing engine integration issues | High | Early integration testing, weekly checkpoints |
| Integration issues | High | Weekly integration checkpoints, early testing |
| Scope creep | High | Phase-6 Charter is binding, change control process |
| Schema changes needed | High | New decision only (v1.1), must go through Phase-5 Senate |

---

## 📝 Phase-6 Rule (Lock This Sentence)

**Phase-6 may add features, but may not change meaning.**

This means:
- ✅ Can add UI layers
- ✅ Can add tooling
- ✅ Can add workflows
- ✅ Can add costing dashboards
- ❌ Cannot change schema semantics
- ❌ Cannot change guardrails
- ❌ Cannot change core business rules
- ❌ Cannot change locking model
- ❌ Cannot change resolution logic

---

## 📚 Related Documents

- **Phase-6 Charter:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md`
- **Phase-6 Execution Plan:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Phase-5 Execution Plan:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_EXECUTION_PLAN_UPDATED.md`
- **Costing Dashboard Brief:** `features/project/reports/COSTING_DASHBOARD_PROJECT_BRIEF.md`
- **Catalog Governance SOP:** `docs/PHASE_5/00_GOVERNANCE/CATALOG_GOVERNANCE_SOP.md`
- **Schema Canon:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Decision Register:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md`

---

**Last Updated:** 2025-01-27  
**Status:** v1.3 (Legacy Parity Added) - COMPREHENSIVE SCOPE DOCUMENT - Ready for Review  
**Total Tasks:** ~123 tasks across 7 tracks over 10-12 weeks

---

## 📋 Version History

- **v1.0:** Initial Phase-6 Complete Scope & Task Summary
- **v1.3 (Legacy Parity Added):** Added Track A-R, Track D0, Track E, Legacy Parity Gate, updated all task details
- **v1.4 (Cost Adders Integrated):** Added Cost Adders feature (Track D0 + Track D) + Cost template seed (Track E)

---

## ✅ Legacy Parity Coverage Summary

**Track A-R ensures:**
- ✅ Quotation reuse (copy old quotation → modify)
- ✅ Panel reuse (copy panel subtree)
- ✅ Feeder reuse (copy Level-0 BOM + subtree)
- ✅ BOM reuse (copy BOM from past quotation)
- ✅ Master BOM template application
- ✅ Post-reuse editability verification
- ✅ Guardrail enforcement after reuse

**Legacy Parity Gate ensures:**
- ✅ All legacy workflows preserved
- ✅ No Phase-5 Canon violations
- ✅ Reuse + edit workflows work smoothly

**Reference:** `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`

