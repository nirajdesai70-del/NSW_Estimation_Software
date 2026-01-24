# Phase-6 Execution Plan

**Version:** 1.4 (Cost Adders Integrated)  
**Date:** 2025-01-27  
**Status:** READY FOR APPROVAL  
**Revision:** Added Cost Adders feature (Track D0 + Track D) + Cost template seed (Track E)  
**Owner:** Product + Engineering  
**Pre-Requisite:** SPEC-5 v1.0 FROZEN ✅  
**Reference:** Phase-6 Kickoff Charter + Phase-5 Canonical Working Record

---

## 🎯 Executive Summary

Phase-6 converts a **correct system** (Phase-5) into a **usable product**. This execution plan breaks down the Phase-6 Charter into actionable tasks organized by track, week, and dependency.

**Total Duration:** 10-12 weeks  
**Tracks:** 7 parallel tracks (A, A-R, B, C, D0, D, E)  
**Exit Artifact:** NSW v0.6 – Internal Product Ready

**Key Additions:**
- **v1.3:** Track A-R (Reuse & Legacy Parity) ensures all legacy capabilities preserved through reuse workflows
- **v1.4:** Cost Adders feature integrated (cost templates, cost sheets, QCA dataset) for complete panel costing

---

## 🔒 Phase-6 Rule (Lock This Sentence – Extended)

**Phase-6 may add features, but may not change meaning.**
**Phase-6 must preserve all legacy capabilities through copy-never-link reuse.**

- ✅ Can add UI layers, tooling, workflows, derived datasets (QCD), dashboards, exports
- ✅ Can add reuse workflows (quotation, panel, feeder, BOM copy)
- ✅ Can add legacy parity features (contacts, project navigation, catalog views)
- ❌ Cannot change schema semantics, guardrails, locked decisions (D-005/006/007/009), resolution constraints, API contract meaning

---

## 📋 Phase-6 Scope Overview

### Track A: Productisation (6 weeks, 33 tasks)
- Quotation UI (Panels, BOM, Items)
- L0 → L1 → L2 resolution UX
- Pricing resolution UX (PRICELIST / MANUAL / FIXED)
- Locking behaviour visibility (line-item)
- Error & warning surfacing
- Customer snapshot handling

### Track A-R: Reuse & Legacy Parity (Weeks 2-4, 7 tasks) ⭐ NEW
- Quotation reuse (copy old quotation → modify)
- Panel reuse (copy panel subtree)
- Feeder reuse (copy Level-0 BOM + subtree)
- BOM reuse (copy BOM from past quotation)
- Master BOM template application
- Post-reuse editability verification
- Guardrail enforcement after reuse

### Track B: Catalog Tooling (3-4 weeks)
- Catalog import UI / scripts
- Series-wise catalog onboarding
- Validation previews (before publish)
- Catalog governance enforcement

### Track C: Operational Readiness (2 weeks)
- Role-based access (basic)
- Approval flows (price changes, overrides)
- Audit visibility (read-only)
- Initial SOPs

### Track D0: Costing Engine Foundations (Weeks 3-6) ⭐ NEW
- Effective quantity engine (BaseQty → EffQtyPerPanel → EffQtyTotal)
- CostHead mapping precedence (D-006)
- Canonical dataset: QuotationCostDetail (QCD) + JSON export endpoint
- Cost Adders engine (cost templates, cost sheets, QCA dataset) ⭐ NEW
- Numeric validation vs reference Excel (engine-first; Excel is consumer)
- Performance hardening gate for "large quotations"
- D0 Gate signoff (QCD v1.0 stable + QCA v1.0 stable)

### Track D: Costing & Reporting (3-4 weeks, 20 tasks) ⭐ MODIFIED
- Costing Pack per quotation (snapshot, panel summary, pivots)
- Cost Adders UI (panel section, cost sheet editor) ⭐ NEW
- Global dashboard for margins, hit rates, cost drivers
- CostHead system UI
- Excel export functionality
- **Consumes QCD + QCA (no duplicate calculators)** ✏️

### Track E: Canon Implementation & Contract Enforcement (Weeks 0-6) ⭐ NEW
This track ensures Phase-6 actually implements Phase-5 frozen items:
- DB creation/migrations from Schema Canon v1.0 + seed execution
- Guardrails G1-G8 runtime enforcement + tests
- API contract implementation (B1-B4) OR explicit defer decision
- Multi-SKU linkage (D-007) implementation
- Discount Editor (legacy parity; replaces heavy structure bulk discount)
- BOM tracking fields runtime behavior
- Customer snapshot handling (D-009)
- Resolution constraints enforcement (A10)

---

## 🗓️ Week-by-Week Execution Plan

### Week 0: Entry Gate & Setup

**Status:** ⏳ PENDING (Blocked until Phase-5 complete)

#### Entry Criteria Verification
- [ ] **P6-ENTRY-001:** Verify SPEC-5 v1.0 frozen ✅
- [ ] **P6-ENTRY-002:** Verify Schema Canon locked ✅
- [ ] **P6-ENTRY-003:** Verify Decision Register closed ✅
- [ ] **P6-ENTRY-004:** Verify Freeze Gate Checklist 100% verified ✅
- [ ] **P6-ENTRY-005:** Verify Core resolution engine tested ✅
- [ ] **P6-ENTRY-006:** Naming conventions compliance check for new migrations/models/routes
  - Verify all new code follows Phase-5 naming conventions
  - Table naming: snake_case, plural
  - Column naming: snake_case, singular
  - FK naming: {table_singular}_id
  - Enum naming: UPPER_SNAKE_CASE

#### Setup Tasks
- [ ] **P6-SETUP-001:** Create Phase-6 project structure
  - Create `docs/PHASE_6/` directory
  - Create `docs/PHASE_6/UI/`, `docs/PHASE_6/CATALOG/`, `docs/PHASE_6/OPS/`, `docs/PHASE_6/COSTING/` subdirectories
  - Set up task tracking system

- [ ] **P6-SETUP-002:** Review Phase-5 deliverables
  - Review Schema Canon v1.0
  - Review API contracts
  - Review resolution engine documentation
  - Identify integration points

- [ ] **P6-SETUP-003:** Create Phase-6 task register
  - Initialize task tracking (spreadsheet or project tool)
  - Assign initial task owners
  - Set up weekly review cadence

- [ ] **P6-SETUP-004:** Create Costing manual structure
  - Create `docs/PHASE_6/COSTING/MANUAL/` directory
  - Create `docs/PHASE_6/COSTING/MANUAL/00_MANUAL_INDEX.md` (index only)
  - Structure for costing engine documentation

- [ ] **P6-SETUP-005:** Freeze Costing Engine Contract (QCD v1.0)
  - EffectiveQty formulas frozen
  - CostBucket + CostHead semantics frozen
  - Excel is consumer, not driver
  - QCD JSON schema defined
  - **File:** `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`

- [ ] **P6-SETUP-006:** Define D0 Gate checklist (QCD readiness)
  - QCD generator functional
  - QCD JSON endpoint working
  - Numeric validation passing
  - Performance acceptable for large quotations
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`

- [ ] **P6-SETUP-007:** Review Phase-5 deliverables for implementation obligations
  - Review Category A: Freeze Gate (A1-A10)
  - Review Category B: API Contracts (B1-B4)
  - Review Category C: Schema Canon (C1-C6)
  - Review Category D: Freeze & Approval
  - Identify all implementation obligations for Phase-6

- [ ] **P6-SETUP-008:** Create module folder boundaries + PR rules
  - Create folder structure: `/app/Modules/AUTH`, `/app/Modules/CIM`, `/app/Modules/MBOM`, `/app/Modules/QUO`, `/app/Modules/PRICING`, `/app/Modules/AUDIT`, `/app/Modules/AI`
  - Define module ownership boundaries per Phase-5 Module Ownership Matrix
  - Create PR checklist: "owner module touched?"
  - Set up change control triggers

**Deliverable:** Phase-6 Entry Gate PASSED, structure + gates ready

---

### Weeks 0-6: Track E - Canon Implementation & Contract Enforcement

**Goal:** Implement Phase-5 frozen items (DB, guardrails, API, multi-SKU, discount editor)

#### Week 0-1: Database Implementation from Schema Canon

- [ ] **P6-DB-001:** Choose DB creation approach (DDL vs migrations) and lock method for Canon v1.0
  - Review Schema Canon v1.0 DDL
  - Decide: Direct DDL execution OR Laravel migrations
  - Lock chosen method
  - **File:** `docs/PHASE_6/DB/DB_CREATION_METHOD.md`

- [ ] **P6-DB-002:** Implement DB schema from Schema Canon v1.0 (DDL or migrations)
  - Create Laravel migration files from DDL (if migrations chosen)
  - OR execute DDL directly (if DDL chosen)
  - Ensure all 34 tables are covered
  - Ensure all constraints (PK, FK, CHECK, UNIQUE) are included
  - Ensure all indexes per Schema Canon are included
  - **File:** `docs/PHASE_6/DB/SCHEMA_MIGRATION_PLAN.md`

- [ ] **P6-DB-003:** Execute seed script (C5) on dev/stage
  - Review seed script requirements from Schema Canon
  - Execute seed scripts
  - Verify seed data populated
  - Verify referential integrity maintained

- [ ] **P6-DB-004:** Schema parity gate (DB == Canon v1.0)
  - Compare actual database schema with Schema Canon
  - Verify table structures match
  - Verify column types match
  - Verify constraints match
  - Verify indexes match
  - Document any discrepancies
  - **File:** `docs/PHASE_6/DB/SCHEMA_PARITY_REPORT.md`
  - **Gate:** Must pass before proceeding to UI work

#### Week 1-2: Cost Template Seed Data (NEW - Cost Adders)

- [ ] **P6-DB-005:** Seed cost template master data
  - Create minimal templates for each cost head:
    - FABRICATION template (3 lines):
      - Steel Sheet (QTY_RATE, CostBucket: MATERIAL)
      - Powder Coating/Jobwork (QTY_RATE, CostBucket: OTHER)
      - Fabrication Manpower (HOUR_RATE, CostBucket: LABOUR)
    - BUSBAR template (2 lines):
      - Copper busbar material (KG_RATE, CostBucket: MATERIAL)
      - Busbar fabrication (HOUR_RATE, CostBucket: LABOUR)
    - LABOUR template (3 lines):
      - Wiring labour (HOUR_RATE, CostBucket: LABOUR)
      - Assembly labour (HOUR_RATE, CostBucket: LABOUR)
      - Testing labour (HOUR_RATE, CostBucket: LABOUR)
    - TRANSPORTATION template (2 lines):
      - Transport (LUMP_SUM, CostBucket: OTHER)
      - Packing (LUMP_SUM, CostBucket: OTHER)
    - ERECTION template (1 line):
      - Site erection labour (HOUR_RATE, CostBucket: LABOUR)
    - COMMISSIONING template (1 line):
      - Commissioning (PERCENT_OF_BASE or LUMP_SUM, CostBucket: OTHER)
  - Set calc_mode and line_cost_bucket per line
  - Default qty/rate = blank (user enters)
  - Tenant-scoped seed data
  - **File:** `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`
  - **Dependency:** After cost_templates table created (P6-COST-D0-009)

**Deliverable:** Database created and verified against Schema Canon v1.0 + Cost template seed data ready

---

### Week 1-2: Track A - Core Quotation UI Foundation

**Goal:** Basic quotation creation and panel management UI

#### Week 1: Quotation & Panel UI

- [ ] **P6-UI-001:** Design quotation overview page
  - Quotation header (Client, Project, Quotation No)
  - Panel list with summary cards
  - Add Panel button
  - Navigation to panel details
  - **File:** `docs/PHASE_6/UI/QUOTATION_OVERVIEW_DESIGN.md`

- [ ] **P6-UI-002:** Implement quotation overview page
  - Create route: `/quotation/{id}/v2`
  - Create view: `resources/views/quotation/v2/index.blade.php`
  - Create controller method: `QuotationV2Controller@index`
  - Display panel list with counts (feeders, items)
  - Display pricing status indicators

- [ ] **P6-UI-003:** Design panel details page
  - Panel header (name, Qty, Rate, Amount)
  - Feeder list (Level=0 BOMs)
  - Add Feeder button
  - Navigation to feeder/BOM details
  - **File:** `docs/PHASE_6/UI/PANEL_DETAILS_DESIGN.md`

- [ ] **P6-UI-004:** Implement panel details page
  - Create route: `/quotation/{id}/panel/{panelId}`
  - Create view: `resources/views/quotation/v2/panel.blade.php`
  - Create controller method: `QuotationV2Controller@panel`
  - Display feeder list with hierarchy
  - **NEW:** Add Cost Adders section (placeholder, full implementation in Track D, Week 7)
    - Display section header
    - "Add Cost Adder" button (disabled until Track D)
  - **Note:** Full Cost Adders UI implemented in P6-COST-019 (Track D, Week 7)

- [ ] **P6-UI-005:** Implement add panel functionality
  - Create route: `POST /quotation/{id}/panel`
  - Create controller method: `QuotationV2Controller@addPanel`
  - Form validation
  - Database insert
  - Redirect to panel details

- [ ] **P6-UI-001A:** Ensure customer_name_snapshot always stored (D-009)
  - When creating quotation, always populate `customer_name_snapshot`
  - If customer_id provided, copy customer name to snapshot
  - If customer_id NULL, use provided customer name for snapshot
  - Integration with quotation creation flow

- [ ] **P6-UI-001B:** customer_id remains nullable (D-009)
  - Ensure customer_id can be NULL
  - Support quotation creation without customer_id
  - Support future customer normalization

**Deliverable:** Quotation overview and panel management UI functional, customer snapshot handling implemented

#### Week 2: Feeder & BOM Hierarchy UI + Track E Continuation

**Track E Tasks (Week 2-4): Guardrails Runtime Enforcement**

- [ ] **P6-VAL-001:** Implement runtime guardrails G1-G8 in service layer
  - Implement G1: Master BOM rejects ProductId (service validation)
  - Implement G2: Production BOM requires ProductId (service validation)
  - Implement G3: IsPriceMissing normalizes Amount (pricing service)
  - Implement G4: RateSource consistency (pricing service)
  - Implement G5: UNRESOLVED normalizes values (pricing service)
  - Implement G6: FIXED_NO_DISCOUNT forces Discount=0 (discount service)
  - Implement G7: Discount range validation 0-100 (discount service)
  - Implement G8: L1-SKU reuse allowed (L1 validation service)
  - **File:** `docs/PHASE_6/VALIDATION/GUARDRAILS_IMPLEMENTATION.md`

- [ ] **P6-VAL-002:** Ensure DB constraints/normalization aligns with guardrail docs
  - Verify all CHECK constraints from Schema Canon are in migrations
  - Verify G7 discount range constraint (0-100) in DB
  - Verify resolution_status constraints in DB
  - Verify ProductId constraints in DB
  - Test constraint enforcement

- [ ] **P6-VAL-003:** API validation parity with 02_VALIDATION_MATRIX.md
  - Review validation matrix from Phase-5
  - Implement API validation matching DB guardrails
  - Ensure all 8 guardrails validated at API layer
  - Map validation errors to error taxonomy codes

- [ ] **P6-VAL-004:** Guardrail test suite (unit + integration)
  - Create unit tests for each guardrail (G1-G8)
  - Create integration tests for guardrail enforcement
  - Test normalization behavior
  - Test constraint violations
  - Test error messages

#### Week 2: Feeder & BOM Hierarchy UI

- [ ] **P6-UI-006:** Design BOM hierarchy tree view
  - Collapsible tree structure
  - Feeder (Level 0) → BOM L1 (Level 1) → BOM L2 (Level 2)
  - Component list at each level
  - **File:** `docs/PHASE_6/UI/BOM_HIERARCHY_DESIGN.md`

- [ ] **P6-UI-007:** Implement BOM hierarchy tree view
  - Create recursive partial: `_bom_tree.blade.php`
  - Create feeder partial: `_feeder.blade.php`
  - Create BOM partial: `_bom.blade.php`
  - JavaScript for expand/collapse
  - Visual hierarchy indicators

- [ ] **P6-UI-008:** Implement add feeder functionality
  - Create route: `POST /quotation/{id}/panel/{panelId}/feeder`
  - Create controller method: `QuotationV2Controller@addFeeder`
  - Form with feeder name, quantity
  - Database insert with Level=0

- [ ] **P6-UI-009:** Implement add BOM functionality
  - Create route: `POST /quotation/{id}/bom/{parentBomId}/bom`
  - Create controller method: `QuotationV2Controller@addBom`
  - Support Level 1 and Level 2
  - Parent-child relationship handling

- [ ] **P6-UI-010:** Implement component/item list display
  - Create component row partial: `_item.blade.php`
  - Display: Category, SubCategory, Item, Generic
  - Display: Make, Series, Description, SKU
  - Display: Qty, Rate, Amount
  - Basic styling

- [ ] **P6-UI-010A:** Verify raw quantity persistence
  - PanelQty stored correctly
  - FeederQty (L0) stored correctly
  - BomQty (L1+) stored correctly
  - ItemQtyPerBom stored correctly
  - Verify quantities persist through create/edit operations

---

### Week 2-3: Track A-R - Reuse & Legacy Parity Foundations ⭐ NEW

**Goal:** Enable reuse workflows (quotation, panel, feeder, BOM) to preserve legacy flexibility

#### Week 2.5: Reuse Foundations

- [ ] **P6-UI-REUSE-001:** Copy quotation (deep copy)
  - Create route: `POST /quotation/{id}/copy`
  - Create controller method: `QuotationV2Controller@copyQuotation`
  - Copy full hierarchy: panels → feeders → BOMs → items
  - Populate BOM tracking fields:
    - `origin_master_bom_id` (if from master)
    - `instance_sequence_no` (increment)
    - `is_modified = false` (initial state)
  - Preserve pricing fields (RateSource, Discount, etc.)
  - UI action: "Create quotation from existing quotation"
  - **File:** `docs/PHASE_6/UI/QUOTATION_REUSE_DESIGN.md`

- [ ] **P6-UI-REUSE-002:** Copy panel into quotation
  - Create route: `POST /quotation/{id}/panel/copy`
  - Create controller method: `QuotationV2Controller@copyPanel`
  - Copy panel subtree (feeders → BOMs → items)
  - Source: same quotation OR past quotation
  - Target: selected quotation
  - Preserve quantities and pricing
  - Editable until locked
  - UI action: "Copy panel from existing quotation"

**Deliverable:** Quotation and panel reuse functional

---

#### Week 3: Feeder & BOM Reuse

- [ ] **P6-UI-REUSE-003:** Copy feeder (Level-0 BOM)
  - Create route: `POST /quotation/{id}/panel/{panelId}/feeder/copy`
  - Create controller method: `QuotationV2Controller@copyFeeder`
  - Copy feeder (Level-0 BOM) + full subtree
  - Source: same quotation OR past quotation
  - Target: selected panel
  - Must preserve hierarchy & quantities
  - Preserve BOM tracking fields
  - UI action: "Copy feeder from existing quotation"

- [ ] **P6-UI-REUSE-004:** Copy BOM under feeder
  - Create route: `POST /quotation/{id}/bom/{parentBomId}/bom/copy`
  - Create controller method: `QuotationV2Controller@copyBom`
  - Copy BOM subtree (child BOMs + items)
  - Source: past project / quotation
  - Target: feeder or parent BOM
  - Mark copied BOM as instance (copy-never-link)
  - Populate `origin_master_bom_id` if from master
  - Populate `instance_sequence_no`
  - UI action: "Copy BOM from existing quotation"

- [ ] **P6-UI-REUSE-005:** Apply Master BOM template
  - Create route: `POST /quotation/{id}/bom/{parentBomId}/master-bom/{masterBomId}`
  - Create controller method: `QuotationV2Controller@applyMasterBom`
  - Apply Master BOM (L1 products only per Phase-5 Canon)
  - Populate `origin_master_bom_id`
  - Populate `instance_sequence_no`
  - Immediately enter L0→L1→L2 resolution flow
  - UI action: "Apply Master BOM template"
  - Integration with Master BOM selection UI

**Deliverable:** Feeder, BOM, and Master BOM reuse functional

---

#### Week 4: Editability & Guardrails Validation

- [ ] **P6-UI-REUSE-006:** Post-reuse editability check
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

- [ ] **P6-UI-REUSE-007:** Guardrail enforcement after reuse
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

**Deliverable:** Post-reuse editability verified, guardrails enforced

---

**Deliverable:** Complete quotation hierarchy UI (Panels → Feeders → BOMs → Items) with quantity persistence verified + Reuse workflows functional

---

### Week 3-4: Track A - Pricing & Resolution UX

**Goal:** Pricing resolution UI and L0→L1→L2 resolution UX

#### Week 3: Pricing Resolution UI

- [ ] **P6-UI-011:** Design pricing resolution UX
  - RateSource dropdown (PRICELIST / MANUAL / FIXED)
  - Price display with source indicator
  - Override controls
  - Discount input (for MANUAL)
  - **File:** `docs/PHASE_6/UI/PRICING_RESOLUTION_UX.md`

- [ ] **P6-UI-012:** Implement RateSource selector
  - Add RateSource dropdown to component row
  - Three options: PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT
  - JavaScript handler: `handleRateSourceChange()`
  - Show/hide relevant fields based on selection

- [ ] **P6-UI-013:** Implement price auto-population
  - Integrate with Phase-5 price resolution engine
  - Auto-populate from pricelist when RateSource=PRICELIST
  - Display price source (pricelist SKU, manual entry, fixed)
  - Handle missing price scenarios

- [ ] **P6-UI-014:** Implement manual pricing controls
  - Discount percentage input (for MANUAL_WITH_DISCOUNT)
  - Base price display
  - Calculated price display
  - JavaScript: `calculateManualPrice()`

- [ ] **P6-UI-015:** Implement fixed pricing controls
  - Fixed price input (for FIXED_NO_DISCOUNT)
  - No discount allowed
  - Price confirmation checkbox
  - JavaScript: `handleFixedPrice()`

- [ ] **P6-UI-016:** Implement pricing status indicators
  - Visual indicators: ✅ Priced, ⚠️ Missing Price, ⚠️ Unresolved
  - Component-level status
  - BOM-level summary
  - Panel-level summary
  - Quotation-level summary

**Deliverable:** Complete pricing resolution UI with all RateSource modes

#### Week 4: L0→L1→L2 Resolution UX

- [ ] **P6-UI-017:** Design L0→L1→L2 resolution UX
  - L0 selection interface (generic product selection)
  - L1 selection interface (intent-based selection)
  - L2 selection interface (SKU selection)
  - Resolution flow visualization
  - **File:** `docs/PHASE_6/UI/L0_L1_L2_RESOLUTION_UX.md`

- [ ] **P6-UI-018:** Implement L0 selection UI
  - Generic product search/select
  - Category/SubCategory filters
  - Display generic product details
  - Integration with catalog_products table

- [ ] **P6-UI-019:** Implement L1 resolution UI
  - Intent-based selection (voltage, duty, attributes)
  - Display L1 line groups
  - Display L1 intent lines
  - Show mapping to L2 candidates
  - Integration with l1_line_groups, l1_intent_lines

- [ ] **P6-UI-020:** Implement L2 resolution UI
  - SKU selection from L1 candidates
  - Display SKU details (from catalog_skus)
  - Show price availability
  - Confirm selection
  - Integration with l1_l2_mappings

- [ ] **P6-UI-021:** Implement resolution flow visualization
  - Show current resolution stage (L0 → L1 → L2)
  - Display resolution path
  - Show unresolved warnings
  - Navigation between stages

- [ ] **P6-UI-022:** Implement resolution status indicators
  - L0 selected ✅
  - L1 resolved ✅
  - L2 resolved ✅
  - Missing resolution ⚠️
  - Component-level and BOM-level indicators

- [ ] **P6-RES-023:** Enforce resolution constraints exactly as Schema Canon
  - Enforce MBOM: L0/L1 only, no ProductId
  - Enforce QUO: L0/L1/L2 allowed, L2 requires ProductId
  - Enforce CHECK constraints at DB level
  - Enforce constraints at service level
  - Enforce constraints at UI level (prevent invalid selections)

- [ ] **P6-RES-024:** Errors must map to B3 error taxonomy codes
  - Review error taxonomy from Phase-5 (03_ERROR_TAXONOMY.md)
  - Map resolution errors to taxonomy codes
  - Ensure error messages match taxonomy
  - Ensure HTTP status codes match taxonomy
  - Ensure request_id propagation

**Deliverable:** Complete L0→L1→L2 resolution UX flow + resolution constraints

---

### Week 5-6: Track A - Locking & Error Handling

**Goal:** Locking visibility and error/warning surfacing

#### Week 5: Locking Behaviour Visibility

- [ ] **P6-UI-023:** Design locking visibility UX
  - Visual indicators for locked items
  - Lock status display (locked/unlocked)
  - Lock reason display
  - Lock prevention UI (disable edits)
  - **File:** `docs/PHASE_6/UI/LOCKING_VISIBILITY_UX.md`

- [ ] **P6-UI-024:** Implement lock status display
  - Visual lock icon on locked items
  - Lock status badge
  - Lock timestamp display
  - Lock reason tooltip

- [ ] **P6-UI-025:** Implement lock prevention UI
  - Disable edit controls for locked items
  - Disable delete for locked items
  - Show lock message on interaction attempt
  - Integration with Phase-5 is_locked enforcement

- [ ] **P6-UI-026:** Implement lock status summary
  - Panel-level lock count
  - BOM-level lock count
  - Quotation-level lock summary
  - Visual lock status dashboard

- [ ] **P6-UI-027:** Implement lock/unlock controls (admin)
  - Unlock button (admin only)
  - Lock confirmation dialog
  - Unlock confirmation dialog
  - Audit log entry

- [ ] **P6-LOCK-000:** Verify no higher-level locking introduced (schema + UI)
  - Verify no is_locked field on quote_boms (BOM level)
  - Verify no is_locked field on quote_panels (Panel level)
  - Verify no is_locked field on quotations (Quotation level)
  - Verify locking only at quote_bom_items level (line-item only)
  - Document locking scope per D-005 decision

**Deliverable:** Complete locking visibility and prevention UI + locking scope verification

#### Week 6: Error & Warning Surfacing

- [ ] **P6-UI-028:** Design error/warning surfacing UX
  - Error message display
  - Warning message display
  - Inline validation errors
  - Summary error panel
  - **File:** `docs/PHASE_6/UI/ERROR_WARNING_UX.md`

- [ ] **P6-UI-029:** Implement price missing warnings
  - Detect missing prices (RateSource=PRICELIST but no price found)
  - Display warning icon on component
  - Warning message: "Price not found in pricelist"
  - Action: Switch to MANUAL or FIXED

- [ ] **P6-UI-030:** Implement unresolved warnings
  - Detect unresolved L0/L1/L2
  - Display warning icon
  - Warning message: "L1/L2 not resolved"
  - Action: Complete resolution flow

- [ ] **P6-UI-031:** Implement validation error display
  - Form validation errors
  - Inline error messages
  - Field-level error indicators
  - Summary error list

- [ ] **P6-UI-032:** Implement error summary panel
  - Quotation-level error count
  - Panel-level error count
  - BOM-level error count
  - Expandable error details
  - Navigation to error location

- [ ] **P6-UI-033:** Implement user-friendly error messages
  - Convert technical errors to user-friendly messages
  - Provide actionable guidance
  - Link to help documentation
  - Error code reference

**Deliverable:** Complete error and warning surfacing system

---

### Weeks 3-6: Track D0 - Costing Engine Foundations (NEW)

**Goal:** Build canonical costing engine (QCD) before UI/reporting

#### Week 3: Quantity + Cost Engine Base

- [ ] **P6-COST-D0-001:** Implement EffectiveQty logic (trait/helper)
  - BaseQty → EffQtyPerPanel → EffQtyTotal formulas
  - Integration with QuotationQuantityService
  - Protected formula (cannot be changed)
  - **File:** `docs/PHASE_6/COSTING/MANUAL/EFFECTIVE_QTY_FORMULAS.md`

- [ ] **P6-COST-D0-002:** Implement CostHead mapping precedence (D-006)
  - Item override (highest priority)
  - Product default (medium priority)
  - System default (lowest priority)
  - Integration with CostHead resolution service
  - **File:** `docs/PHASE_6/COSTING/MANUAL/COSTHEAD_PRECEDENCE.md`

- [ ] **P6-COST-D0-003:** Implement QCD generator + JSON endpoint
  - Create QuotationCostDetail (QCD) canonical dataset (BOM-only, stable contract)
  - Generate QCD for quotation
  - Create JSON export endpoint: `/quotation/{id}/export/cost-detail/json`
  - QCD schema definition
  - **File:** `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`

#### Week 3: Cost Heads Seeding (NEW - Cost Adders)

- [ ] **P6-COST-D0-008:** Seed generic cost heads for cost adders
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

#### Week 4: Export Baseline + Numeric Validation + Cost Template & Sheet Tables (NEW - Cost Adders)

- [ ] **P6-COST-D0-004:** QCD Excel export (sheet-1 only, minimal formatting)
  - Export QCD to Excel format
  - Sheet 1: Panel summary (minimal formatting)
  - Basic Excel structure
  - **File:** `docs/PHASE_6/COSTING/MANUAL/EXCEL_EXPORT_STRUCTURE.md`

- [ ] **P6-COST-D0-005:** Numeric validation vs Excel reference (engine-first)
  - Compare QCD engine output with reference Excel
  - Validate numeric accuracy
  - Engine is source of truth, Excel is consumer
  - Document any discrepancies
  - **File:** `docs/PHASE_6/COSTING/MANUAL/NUMERIC_VALIDATION.md`

- [ ] **P6-COST-D0-009:** Create cost template master tables
  - `cost_templates` table (one per cost head)
  - `cost_template_lines` table (rows per template)
  - Migration script
  - Fields:
    - cost_templates: id, tenant_id, cost_head_id, name, version, is_active
    - cost_template_lines: id, cost_template_id, line_name, calc_mode, default_uom, default_rate, line_cost_bucket (MATERIAL/LABOUR/OTHER, nullable), sort_order
  - **Note:** `line_cost_bucket` allows each template line to have its own CostBucket (e.g., Fabrication sheet: steel=MATERIAL, coating=OTHER, manpower=LABOUR)
  - **File:** `docs/PHASE_6/COSTING/COST_TEMPLATE_SCHEMA.md`
  - **Dependency:** After cost heads seeded (P6-COST-D0-008)

- [ ] **P6-COST-D0-010:** Create cost sheet runtime tables
  - `quote_cost_sheets` table (one per panel per cost head)
  - `quote_cost_sheet_lines` table (instantiated template lines)
    - Include `line_cost_bucket` field (inherited from template, can override)
  - `quote_cost_adders` table (summary roll-up, one per panel per cost head)
    - Summary bucket comes from `cost_heads.category` (not aggregated from lines)
  - Migration script
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_SCHEMA.md`
  - **Dependency:** After template tables (P6-COST-D0-009)

#### Week 5-6: Performance + Gate + Cost Sheet Calculation & Roll-Up (NEW - Cost Adders)

- [ ] **P6-COST-D0-011:** Implement cost sheet calculation engine
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

- [ ] **P6-COST-D0-012:** Implement cost adder roll-up generator
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

- [ ] **P6-COST-D0-013:** Implement QCA (Quote Cost Adders) dataset
  - QCA = canonical dataset from quote_cost_adders table
  - One row per panel per cost head (summary)
  - JSON export endpoint: `/quotation/{id}/export/cost-adders/json`
  - QCA schema definition
  - **Note:** QCD remains BOM-only (stable contract)
  - **File:** `docs/PHASE_6/COSTING/QCA_CONTRACT_v1.0.md`
  - **Dependency:** After roll-up generator (P6-COST-D0-012)

- [ ] **P6-COST-D0-006:** Performance hardening for large quotations
  - Test with large quotations (100+ panels, 1000+ items)
  - Optimize QCD generation performance
  - Optimize quantity calculations
  - Optimize CostHead resolution
  - Optimize cost adders calculation and roll-up
  - Performance targets: < 5 seconds for typical quotation

- [ ] **P6-COST-D0-014:** Update D0 Gate checklist to include cost adders
  - QCD generator functional (BOM-only, unchanged)
  - QCA generator functional (cost adders summary)
  - Cost sheet calculation engine working
  - Roll-up generator working
  - Performance acceptable with cost adders (< 5 seconds for typical quotation)
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md` (update)
  - **Gate:** Must pass before Track D (Costing & Reporting) can proceed

- [ ] **P6-COST-D0-007:** D0 Gate signoff (QCD v1.0 stable + QCA v1.0 stable)
  - QCD generator functional (BOM-only)
  - QCA generator functional (cost adders)
  - QCD JSON endpoint working
  - QCA JSON endpoint working
  - Numeric validation passing
  - Performance acceptable for large quotations (with cost adders)
  - **Gate:** Must pass before Track D (Costing & Reporting) can proceed
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_SIGNOFF.md`

**Deliverable:** QCD v1.0 stable, D0 Gate passed

---

### Week 3-6: Track B - Catalog Tooling (Parallel)

**Goal:** Catalog import UI, validation, and governance

#### Week 3: Catalog Import UI Foundation

- [ ] **P6-CAT-001:** Design catalog import UI
  - File upload interface
  - Series selection
  - Import preview
  - Validation results display
  - **File:** `docs/PHASE_6/CATALOG/CATALOG_IMPORT_UI_DESIGN.md`

- [ ] **P6-CAT-002:** Implement catalog file upload
  - Create route: `/catalog/import`
  - Create view: `resources/views/catalog/import.blade.php`
  - File upload form (XLSX, CSV)
  - Series dropdown selection
  - Upload progress indicator

- [ ] **P6-CAT-003:** Implement catalog import parser
  - Parse XLSX/CSV files
  - Validate file format
  - Extract SKU data
  - Extract price data
  - Error handling for malformed files

- [ ] **P6-CAT-004:** Implement import preview
  - Display parsed data preview
  - Show record count
  - Show validation status
  - Allow edit before import

**Deliverable:** Catalog import UI with file upload and preview

#### Week 4: Series-wise Catalog Onboarding

- [ ] **P6-CAT-005:** Design series onboarding workflow
  - Series selection
  - Template selection
  - Data mapping
  - Validation rules
  - **File:** `docs/PHASE_6/CATALOG/SERIES_ONBOARDING_WORKFLOW.md`

- [ ] **P6-CAT-006:** Implement series selection
  - Series dropdown (LC1E, etc.)
  - Series-specific templates
  - Series-specific validation rules
  - Integration with catalog_series table

- [ ] **P6-CAT-007:** Implement data mapping UI
  - Column mapping interface
  - Source column → target field mapping
  - Mapping validation
  - Save mapping template

- [ ] **P6-CAT-008:** Implement series-specific import scripts
  - LC1E import script
  - Generic import script template
  - Series-specific transformation logic
  - Integration with catalog pipeline

**Deliverable:** Series-wise catalog onboarding workflow

#### Week 5: Validation Previews

- [ ] **P6-CAT-009:** Design validation preview system
  - Pre-import validation
  - Validation rule display
  - Validation results summary
  - Error/warning details
  - **File:** `docs/PHASE_6/CATALOG/VALIDATION_PREVIEW_DESIGN.md`

- [ ] **P6-CAT-010:** Implement pre-import validation
  - Run validation rules before import
  - Check required fields
  - Check data types
  - Check referential integrity
  - Check business rules

- [ ] **P6-CAT-011:** Implement validation results display
  - Validation summary (pass/fail/warning count)
  - Detailed validation errors
  - Validation warnings
  - Line-by-line validation status

- [ ] **P6-CAT-012:** Implement validation rule configuration
  - Series-specific validation rules
  - Custom validation rules
  - Rule priority
  - Rule enable/disable

**Deliverable:** Validation preview system before publish

#### Week 6: Catalog Governance Enforcement

- [ ] **P6-CAT-013:** Design catalog governance UI
  - Governance dashboard
  - Approval workflow
  - Change tracking
  - **File:** `docs/PHASE_6/CATALOG/CATALOG_GOVERNANCE_UI.md`

- [ ] **P6-CAT-014:** Implement catalog approval workflow
  - Submit for approval
  - Approval queue
  - Approve/reject actions
  - Approval comments
  - Integration with Phase-5 Catalog Governance SOP

- [ ] **P6-CAT-015:** Implement change tracking
  - Track catalog changes
  - Change history display
  - Diff view (before/after)
  - Change author and timestamp

- [ ] **P6-CAT-016:** Implement governance enforcement
  - Prevent unauthorized changes
  - Enforce approval workflow
  - Enforce validation rules
  - Audit log integration

**Deliverable:** Catalog governance enforcement system

---

### Weeks 3-6: Track E Continuation - API Contracts, Multi-SKU, Discount Editor

#### Week 3-6: API Contracts (B1-B4) Implementation OR Explicit Defer

- [ ] **P6-API-001:** Implement endpoints per 01_API_SURFACE_MAP.md
  - Review API Surface Map from Phase-5
  - Implement all read endpoints
  - Implement all write endpoints
  - Ensure endpoint paths match contract
  - **File:** `docs/PHASE_6/API/ENDPOINT_IMPLEMENTATION.md`

- [ ] **P6-API-002:** Request/response schemas per OpenAPI skeleton
  - Review OpenAPI skeleton from Phase-5
  - Implement request validation per schemas
  - Implement response formatting per schemas
  - Ensure schema compliance

- [ ] **P6-API-003:** Error taxonomy + request_id propagation
  - Review error taxonomy from Phase-5 (03_ERROR_TAXONOMY.md)
  - Implement error code mapping
  - Implement error envelope format
  - Implement request_id generation and propagation
  - Ensure HTTP status codes match taxonomy

- [ ] **P6-API-004:** Versioning rules applied
  - Review versioning policy from Phase-5 (04_VERSIONING_POLICY.md)
  - Implement URL-based versioning (v1)
  - Implement backward compatibility checks
  - Document version bump process

- [ ] **P6-API-005:** Contract tests
  - Create contract tests for all endpoints
  - Test request/response schemas
  - Test validation rules
  - Test error responses
  - Test versioning compliance

- [ ] **P6-API-DECISION:** If deferring, write signed "defer to Phase-7" memo
  - Document decision to defer API implementation
  - Get stakeholder sign-off
  - Document in Phase-6 closure report
  - **File:** `docs/PHASE_6/API/API_DEFER_DECISION.md`

#### Week 3-6: Multi-SKU Linkage (D-007)

- [ ] **P6-SKU-001:** Implement parent_line_id grouping + metadata_json rules
  - Support parent_line_id for grouping related SKUs
  - Define metadata_json structure for multi-SKU
  - Group creation/editing logic
  - Integration with BOM item creation

- [ ] **P6-SKU-002:** UI rendering of grouped multi-SKU lines
  - Display multi-SKU groups in UI
  - Show group relationships
  - Visual grouping indicators
  - Handle group operations (add/remove from group)

- [ ] **P6-SKU-003:** Safe edit validation for metadata_json
  - Create UI for editing metadata_json (safe editing)
  - Validate metadata_json structure
  - Store metadata_json with BOM items
  - Validation rules enforcement

#### Week 2-4: BOM Tracking Fields Runtime Behavior

- [ ] **P6-BOM-TRACK-001:** Populate BOM tracking fields on create/copy
  - When creating BOM from master, populate `origin_master_bom_id`
  - When creating BOM instance, populate `instance_sequence_no`
  - When copying BOM, increment `instance_sequence_no`
  - Integration with BOM creation/copy logic

- [ ] **P6-BOM-TRACK-002:** Update is_modified/modified_by/modified_at on edits
  - When BOM item is edited, set `is_modified = true`
  - Populate `modified_by` with current user
  - Populate `modified_at` with current timestamp
  - Integration with BOM edit logic

- [ ] **P6-BOM-TRACK-003:** UI indicator "modified vs original" (read-only badge)
  - Display badge on BOMs that are modified
  - Show "Modified" indicator on BOM items
  - Show modification timestamp
  - Read-only display (no edit capability)

#### Week 3-6: Discount Editor (Legacy Parity / Performance)

- [ ] **P6-DISC-001:** Implement /quotation/{id}/discount
  - Create route: `/quotation/{id}/discount`
  - Create view: `resources/views/quotation/discount.blade.php`
  - Create controller: `QuotationDiscountController@index`
  - Display discount editor interface
  - **File:** `docs/PHASE_6/UI/DISCOUNT_EDITOR_DESIGN.md`

- [ ] **P6-DISC-002:** Filters (Make/Category/Item/Desc/SKU/Panel/Feeder/BOM)
  - Filter by Make
  - Filter by Category/SubCategory/Item
  - Filter by Description
  - Filter by SKU
  - Filter by Panel
  - Filter by Feeder
  - Filter by BOM
  - Multi-filter support

- [ ] **P6-DISC-003:** Preview + Apply (transaction) + audit log
  - Preview discount changes before applying
  - Show affected items count
  - Show total discount impact
  - Apply discounts in transaction
  - Rollback on error
  - Log all bulk discount operations

- [ ] **P6-DISC-004:** Hook approvals (Track C) for bulk updates if required
  - Require approval for large discount changes (configurable threshold)
  - Integration with Track C approval workflow
  - Audit trail for discount changes

**Deliverable:** API contracts implemented OR deferred, Multi-SKU linkage functional, Discount Editor functional

---

### Week 7-8: Track C - Operational Readiness (Parallel)

**Goal:** Role-based access, approval flows, audit visibility

#### Week 7: Role-based Access & Approval Flows

- [ ] **P6-OPS-001:** Design role-based access system
  - Role definitions (Admin, Catalog Manager, User, Viewer)
  - Permission matrix
  - Access control rules
  - **File:** `docs/PHASE_6/OPS/ROLE_BASED_ACCESS_DESIGN.md`

- [ ] **P6-OPS-002:** Implement basic role system
  - Create roles table (if not exists)
  - Create user_roles table
  - Role assignment UI
  - Role-based route protection

- [ ] **P6-OPS-003:** Implement permission checks
  - Middleware for role checking
  - Controller-level permission checks
  - View-level permission checks
  - API-level permission checks

- [ ] **P6-OPS-004:** Design approval flows
  - Price change approval
  - Override approval
  - Catalog change approval
  - **File:** `docs/PHASE_6/OPS/APPROVAL_FLOWS_DESIGN.md`

- [ ] **P6-OPS-005:** Implement price change approval
  - Submit price change request
  - Approval queue for price changes
  - Approve/reject with comments
  - Notification system

- [ ] **P6-OPS-006:** Implement override approval
  - Submit override request
  - Approval queue for overrides
  - Approve/reject with comments
  - Override reason tracking

**Deliverable:** Role-based access and approval flows functional

#### Week 8: Audit Visibility & SOPs

- [ ] **P6-OPS-007:** Design audit visibility UI
  - Audit log display
  - Filter and search
  - Export functionality
  - **File:** `docs/PHASE_6/OPS/AUDIT_VISIBILITY_DESIGN.md`

- [ ] **P6-OPS-008:** Implement audit log display
  - Create route: `/audit/logs`
  - Create view: `resources/views/audit/logs.blade.php`
  - Display audit entries (read-only)
  - Filter by user, action, date range
  - Search functionality

- [ ] **P6-OPS-009:** Implement audit log details
  - Detailed audit entry view
  - Before/after values
  - Change diff display
  - User and timestamp information

- [ ] **P6-OPS-010:** Create initial SOPs
  - Catalog import SOP
  - Price approval SOP
  - Override approval SOP
  - Error handling SOP
  - **File:** `docs/PHASE_6/OPS/INITIAL_SOPS.md`

- [ ] **P6-OPS-011:** Implement audit export
  - Export audit logs to CSV
  - Export audit logs to PDF
  - Date range selection
  - Filter preservation in export

- [ ] **P6-OPS-012:** Costing Pack/dashboard/export permissions + bulk discount approval hook
  - Role-based access for costing features
  - Dashboard access permissions
  - Export permissions
  - Bulk discount approval hook (integration with P6-DISC-004)

**Deliverable:** Complete audit visibility and initial SOPs + costing permissions

---

### Week 7-10: Track D - Costing & Reporting (Parallel)

**Goal:** Costing Pack per quotation, global dashboard, Excel exports

#### Week 7: Costing Pack Foundation

- [ ] **P6-COST-001:** Design Costing Pack UI
  - Costing Pack per quotation structure
  - Snapshot view design
  - Panel summary view design
  - Pivot table design
  - **File:** `docs/PHASE_6/COSTING/COSTING_PACK_DESIGN.md`
  - **Reference:** `features/project/reports/COSTING_DASHBOARD_PROJECT_BRIEF.md`

- [ ] **P6-COST-002:** Confirm D0 Gate passed (QCD stable)
  - Verify D0 Gate signoff complete
  - Verify QCD v1.0 stable
  - Verify QCD JSON endpoint functional
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_VERIFICATION.md`

- [ ] **P6-COST-003:** Implement quotation costing snapshot
  - Create route: `/quotation/{id}/costing/snapshot`
  - Create view: `resources/views/quotation/costing/snapshot.blade.php`
  - Display quotation-level costing summary
  - Display total cost, margin, hit rate
  - **Data source: QCD aggregates (not "CostingService")**

- [ ] **P6-COST-004:** Implement panel summary view
  - Create route: `/quotation/{id}/costing/panels`
  - Create view: `resources/views/quotation/costing/panels.blade.php`
  - Display panel-level costing breakdown
  - Display panel costs, margins, quantities
  - Panel cost per unit display
  - **Data source: QCD aggregates**

**Deliverable:** Costing Pack foundation with snapshot and panel summary

#### Week 8: Costing Pack Details & Pivots

- [ ] **P6-COST-005:** Implement BOM/Feeder costing breakdown
  - Display feeder-level costing
  - Display BOM-level costing
  - Display component-level costing
  - Hierarchy visualization
  - **Derived via QCD + tree**

- [ ] **P6-COST-006:** Implement CostHead grouping (now mandatory)
  - CostHead category display
  - CostHead-based cost aggregation
  - CostBucket mappings
  - CostHead pivot view
  - Integration with Phase-5 CostHead system

- [ ] **P6-COST-007:** Implement pivot tables
  - Panel × CostHead pivot
  - Feeder × Component pivot
  - CostHead × Panel pivot
  - **Must include CostHead pivot + Category/Make/RateSource**
  - Interactive pivot controls
  - Export pivot data

- [ ] **P6-COST-008:** Implement costing pack navigation
  - Tab navigation (Snapshot, Panels, Breakdown, Pivots)
  - Breadcrumb navigation
  - Quick links between views
  - Print-friendly views

**Deliverable:** Complete Costing Pack with all views and pivots

#### Week 9: Global Dashboard

- [ ] **P6-COST-009:** Design global dashboard
  - Margins dashboard design
  - Hit rates dashboard design
  - Cost drivers dashboard design
  - KPI visualization design
  - **File:** `docs/PHASE_6/COSTING/GLOBAL_DASHBOARD_DESIGN.md`

- [ ] **P6-COST-010:** Implement margins dashboard
  - Create route: `/dashboard/margins`
  - Create view: `resources/views/dashboard/margins.blade.php`
  - Display quotation margins
  - Margin trends over time
  - Margin by panel/feeder
  - Target margin comparison
  - **All dashboard aggregations come from QCD across quotations**

- [ ] **P6-COST-011:** Implement hit rates dashboard
  - Create route: `/dashboard/hit-rates`
  - Create view: `resources/views/dashboard/hit-rates.blade.php`
  - Display quotation hit rates
  - Hit rate trends
  - Hit rate by client/project
  - Win/loss analysis
  - **All dashboard aggregations come from QCD across quotations**

- [ ] **P6-COST-012:** Implement cost drivers dashboard
  - Create route: `/dashboard/cost-drivers`
  - Create view: `resources/views/dashboard/cost-drivers.blade.php`
  - Display top cost drivers
  - CostHead analysis
  - Component cost analysis
  - Cost trend analysis
  - **All dashboard aggregations come from QCD across quotations**

- [ ] **P6-COST-013:** Implement dashboard filters
  - Date range filters
  - Client/project filters
  - Panel/feeder filters
  - CostHead filters
  - Filter persistence

**Deliverable:** Global dashboard with margins, hit rates, and cost drivers

#### Week 10: Excel Export & Integration

- [ ] **P6-COST-014:** Design Excel export functionality
  - Export formats (XLSX, CSV)
  - Export templates
  - Export data structure
  - **File:** `docs/PHASE_6/COSTING/EXCEL_EXPORT_DESIGN.md`

- [ ] **P6-COST-015:** Implement Costing Pack Excel export (engine-first)
  - Export should be engine-first
  - Sheet 1: Panel summary (BOM + Cost Adders totals)
  - Sheet 2: Detailed BOM (QCD - BOM items only)
  - Sheet 3: Cost Adders detail (QCA - summary lines, with drill-down to sheet lines)
  - Sheet 4: Pivot shells (optional)
  - Excel formatting (headers, formulas)
  - **Note:** Charts/graphs optional unless requested
  - **Data source: QCD (BOM) + QCA (Adders)**

- [ ] **P6-COST-016:** Implement dashboard Excel export
  - Export margins dashboard data
  - Export hit rates dashboard data
  - Export cost drivers dashboard data
  - Export filtered views

- [ ] **P6-COST-017:** Implement costing calculation UI integration
  - Real-time costing calculation display (from QCD)
  - Cost recalculation triggers (regenerate QCD)
  - Cost validation indicators
  - Cost discrepancy warnings
  - **Integration with QCD generator (not separate CostingService)**

- [ ] **P6-COST-018:** Implement costing pack access control
  - Role-based access (Finance, Sales, Management)
  - Dashboard access permissions
  - Export permissions
  - Integration with Track C role system

**Deliverable:** Complete costing & reporting system with Excel exports

---

### Week 8.5: Legacy Parity Verification Gate ⭐ NEW

**Goal:** Verify all legacy capabilities preserved through reuse workflows

#### Legacy Parity Gate Checklist

- [ ] **P6-GATE-LEGACY-001:** Quotation reuse verified
  - Copy old quotation → modify works
  - Full hierarchy copied correctly
  - BOM tracking fields populated
  - Editability maintained

- [ ] **P6-GATE-LEGACY-002:** Panel reuse verified
  - Copy panel subtree works
  - Source: same or past quotation
  - Editability maintained

- [ ] **P6-GATE-LEGACY-003:** Feeder reuse verified
  - Copy feeder (Level-0 BOM) works
  - Full subtree copied
  - Editability maintained

- [ ] **P6-GATE-LEGACY-004:** BOM reuse verified
  - Copy BOM from past quotation works
  - Master BOM application works
  - Copy-never-link semantics respected
  - Editability maintained

- [ ] **P6-GATE-LEGACY-005:** Post-reuse guardrails verified
  - All guardrails (G1-G8) enforced
  - No schema canon violations
  - Locking scope respected (D-005)

- [ ] **P6-GATE-LEGACY-006:** Legacy parity checklist complete
  - Reference: `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`
  - All checklist items verified
  - No legacy workflow blocked

**Gate Rule:** Phase-6 cannot proceed to Integration unless all legacy parity items are verified.

**Deliverable:** Legacy Parity Gate PASSED

---

### Week 9-10: Integration & Stabilisation

**Goal:** End-to-end integration, bug fixes, UX polish

#### Week 9: End-to-End Integration

- [ ] **P6-INT-001:** End-to-end quotation creation test
  - Create quotation
  - Add panel
  - Add feeder
  - Add BOM
  - Add components
  - Complete L0→L1→L2 resolution
  - Set pricing
  - Lock items
  - Verify audit trail

- [ ] **P6-INT-002:** End-to-end catalog import test
  - Upload catalog file
  - Select series
  - Map columns
  - Run validation
  - Submit for approval
  - Approve import
  - Verify data in system

- [ ] **P6-INT-006:** End-to-end costing pack test
  - Create quotation with panels/feeders/BOMs
  - Generate costing pack
  - Verify snapshot calculations
  - Verify panel summary
  - Verify pivot tables
  - Export to Excel
  - Verify global dashboard data

- [ ] **P6-INT-003:** Integration testing
  - UI → API integration tests
  - Resolution engine integration tests
  - Pricing engine integration tests
  - Locking engine integration tests
  - Catalog pipeline integration tests
  - Guardrails enforcement integration tests
  - BOM tracking integration tests
  - Multi-SKU integration tests

- [ ] **P6-INT-004:** Cross-track integration
  - Database → All tracks (schema foundation)
  - Catalog import → Quotation UI
  - Pricing resolution → UI display
  - Guardrails → All services (enforcement)
  - Locking → UI visibility
  - Audit → UI display
  - Costing engine → Costing Pack UI
  - Quotation UI → Costing Pack
  - Costing Pack → Global Dashboard
  - API contracts → UI (if API track implemented)
  - BOM tracking → UI display
  - Multi-SKU → UI display
  - Discount Editor → Approval workflow

- [ ] **P6-INT-005:** Performance testing
  - Quotation load time
  - Catalog import performance
  - UI responsiveness
  - Database query optimization

**Deliverable:** End-to-end integration verified

#### Week 10: Stabilisation & Polish

- [ ] **P6-STAB-001:** Bug fixes
  - Fix identified bugs
  - Fix UI inconsistencies
  - Fix validation issues
  - Fix integration issues

- [ ] **P6-STAB-002:** UX polish
  - Improve error messages
  - Improve loading states
  - Improve visual feedback
  - Improve navigation flow

- [ ] **P6-STAB-003:** Documentation updates
  - Update user documentation
  - Update API documentation
  - Update SOPs
  - Create user guides

- [ ] **P6-STAB-004:** User acceptance testing
  - Internal user testing
  - Collect feedback
  - Address critical issues
  - Sign-off preparation

- [ ] **P6-STAB-005:** Final verification
  - Verify all exit criteria met
  - Verify all success metrics met
  - Prepare Phase-6 closure report
  - Prepare handover to Phase-7

**Deliverable:** Stabilised NSW v0.6 ready for internal use

---

### Week 11-12: Buffer & Phase-6 Closure

**Goal:** Buffer for unexpected issues, final closure

#### Week 11: Buffer Week
- [ ] **P6-BUF-001:** Address any remaining issues
- [ ] **P6-BUF-002:** Final testing
- [ ] **P6-BUF-003:** Documentation finalisation

#### Week 12: Phase-6 Closure

- [ ] **P6-CLOSE-001:** Phase-6 exit criteria verification
  - ✅ A quotation can be created end-to-end
  - ✅ L1 selection reliably maps to L2 SKUs
  - ✅ Pricing resolution works with overrides
  - ✅ Catalog entries can be added safely
  - ✅ Errors are explainable to users

- [ ] **P6-CLOSE-002:** Success metrics verification
  - ✅ Internal users can create quotations without errors
  - ✅ Catalog entries can be imported safely
  - ✅ Pricing overrides work correctly
  - ✅ Audit trail is visible and complete
  - ✅ Errors are understandable and actionable

- [ ] **P6-CLOSE-003:** Create Phase-6 closure report
  - Summary of deliverables
  - Lessons learned
  - Known issues
  - Recommendations for Phase-7

- [ ] **P6-CLOSE-004:** Handover to Phase-7
  - Document system state
  - Document outstanding items
  - Prepare Phase-7 kickoff materials

- [ ] **P6-CLOSE-005:** Canon compliance signoff
  - Schema parity (Canon v1.0)
  - Guardrails runtime parity (G1–G8)
  - API parity (or defer memo exists)
  - Locking scope respected (D-005)
  - CostHead precedence respected (D-006)
  - Multi-SKU linkage present (D-007)
  - Discount Editor delivered (legacy parity)
  - Customer snapshot handling (D-009)
  - Resolution constraints enforced (A10)
  - **File:** `docs/PHASE_6/CLOSURE/CANON_COMPLIANCE_SIGNOFF.md`

**Deliverable:** Phase-6 COMPLETE, NSW v0.6 released, Canon compliance verified

---

## 📊 Task Summary

### Track A: Productisation (UI + Workflow)
- **Total Tasks:** 33 tasks (core UI tasks)
- **Duration:** 6 weeks (Weeks 1-6)

### Track A-R: Reuse & Legacy Parity ⭐ NEW
- **Total Tasks:** 7 tasks
- **Duration:** 3 weeks (Weeks 2-4, parallel with Track A)
- **Key Deliverables:**
  - Quotation reuse (copy old quotation → modify)
  - Panel reuse (copy panel subtree)
  - Feeder reuse (copy Level-0 BOM + subtree)
  - BOM reuse (copy BOM from past quotation)
  - Master BOM template application
  - Post-reuse editability verification
  - Guardrail enforcement after reuse
- **Key Deliverables:**
  - Quotation overview and panel management UI
  - BOM hierarchy tree view
  - Pricing resolution UI
  - L0→L1→L2 resolution UX
  - Locking visibility
  - Error/warning surfacing

### Track B: Catalog Tooling
- **Total Tasks:** 16 tasks
- **Duration:** 4 weeks (Weeks 3-6, parallel)
- **Key Deliverables:**
  - Catalog import UI
  - Series-wise onboarding
  - Validation previews
  - Catalog governance enforcement

### Track C: Operational Readiness
- **Total Tasks:** 12 tasks
- **Duration:** 2 weeks (Weeks 7-8, parallel)
- **Key Deliverables:**
  - Role-based access
  - Approval flows
  - Audit visibility
  - Initial SOPs

### Track D0: Costing Engine Foundations ⭐ NEW
- **Total Tasks:** 14 tasks (7 original + 7 cost adders)
- **Duration:** 4 weeks (Weeks 3-6, parallel)
- **Key Deliverables:**
  - EffectiveQty engine
  - CostHead mapping precedence
  - QCD generator + JSON endpoint (BOM-only)
  - Cost Adders engine (templates, sheets, QCA) ⭐ NEW
  - Excel export baseline
  - Performance hardening
  - D0 Gate signoff (QCD + QCA)

### Track D: Costing & Reporting ⭐ MODIFIED
- **Total Tasks:** 20 tasks (18 original + 2 cost adders)
- **Duration:** 4 weeks (Weeks 7-10, parallel)
- **Key Change:** Consumes QCD + QCA (no duplicate calculators)
- **New Features:** Cost Adders UI (panel section, cost sheet editor)

### Track E: Canon Implementation & Contract Enforcement ⭐ NEW
- **Total Tasks:** ~28 tasks (DB + Guardrails + API + Multi-SKU + Discount Editor + BOM tracking + Customer snapshot + Resolution constraints)

### Legacy Parity Gate ⭐ NEW
- **Total Tasks:** 6 tasks
- **Duration:** 0.5 weeks (Week 8.5)
- **Key Deliverables:**
  - Quotation reuse verified
  - Panel reuse verified
  - Feeder reuse verified
  - BOM reuse verified
  - Post-reuse guardrails verified
  - Legacy parity checklist complete
- **Duration:** 6 weeks (Weeks 0-6, parallel)
- **Key Deliverables:**
  - Database created from Schema Canon
  - Guardrails G1-G8 runtime enforcement
  - API contracts implemented OR deferred
  - Multi-SKU linkage functional
  - Discount Editor functional
  - BOM tracking fields runtime behavior
  - Customer snapshot handling
  - Resolution constraints enforced
- **Key Deliverables:**
  - Costing Pack per quotation (snapshot, panel summary, pivots)
  - Global dashboard (margins, hit rates, cost drivers)
  - CostHead system UI
  - Excel export functionality
  - Costing calculation engine UI integration

### Track A-R: Reuse & Legacy Parity ⭐ NEW
- **Total Tasks:** 7 tasks
- **Duration:** 3 weeks (Weeks 2-4, parallel)
- **Key Deliverables:**
  - Quotation reuse (copy old quotation → modify)
  - Panel reuse (copy panel subtree)
  - Feeder reuse (copy Level-0 BOM + subtree)
  - BOM reuse (copy BOM from past quotation)
  - Master BOM template application
  - Post-reuse editability verification
  - Guardrail enforcement after reuse

### Legacy Parity Gate ⭐ NEW
- **Total Tasks:** 6 tasks
- **Duration:** 0.5 weeks (Week 8.5)
- **Key Deliverables:**
  - Quotation reuse verified
  - Panel reuse verified
  - Feeder reuse verified
  - BOM reuse verified
  - Post-reuse guardrails verified
  - Legacy parity checklist complete

### Integration & Stabilisation
- **Total Tasks:** 12 tasks
- **Duration:** 2 weeks (Weeks 9-10)
- **Key Deliverables:**
  - End-to-end integration
  - Reuse workflow integration test
  - Bug fixes
  - UX polish
  - User acceptance testing

### Closure
- **Total Tasks:** 5 tasks
- **Duration:** 2 weeks (Weeks 11-12)
- **Key Deliverables:**
  - Exit criteria verification
  - Canon compliance signoff
  - Phase-6 closure report
  - Handover to Phase-7

**Grand Total:** ~133 tasks over 10-12 weeks

**Breakdown:**
- Track A: Productisation - 33 tasks (1 updated for cost adders placeholder)
- Track A-R: Reuse & Legacy Parity - 7 tasks
- Track B: Catalog Tooling - 16 tasks
- Track C: Operational Readiness - 12 tasks
- Track D0: Costing Engine Foundations - 14 tasks (7 original + 7 cost adders) ⭐ NEW
- Track D: Costing & Reporting - 20 tasks (18 original + 2 cost adders, 5 updated) ⭐ NEW
- Track E: Canon Implementation - ~29 tasks (28 original + 1 cost template seed) ⭐ NEW
- Legacy Parity Gate - 6 tasks
- Integration & Stabilisation - 12 tasks
- Closure - 5 tasks

---

## 🔗 Dependencies

### Critical Path
1. **Week 0:** Entry gate must pass before any work begins
2. **Week 0-1:** Database implementation must complete before UI work (Track E)
3. **Week 1-2:** UI foundation must be complete before pricing/resolution UX
4. **Week 2-3:** Reuse workflows can start in parallel with BOM UI (Track A-R)
5. **Week 3-4:** Pricing UX must be complete before error handling
6. **Week 3-4:** Guardrails enforcement must be complete before UI validation (P6-VAL-001..004)
7. **Week 3-4:** API contracts can run in parallel (Track E, optional)
8. **Week 4:** Post-reuse editability and guardrails must be verified (Track A-R)
9. **Week 5-6:** Locking visibility must be complete before error handling
10. **Week 7-8:** Operational readiness needed for costing access control
11. **Week 8.5:** Legacy Parity Gate must pass before integration
12. **Week 9-10:** All tracks must be complete before integration
13. **Week 11-12:** Integration must be complete before closure

### Parallel Execution
- **Track E (Canon Implementation)** - DB portion must complete before all other tracks (Weeks 0-1)
- **Track E (Canon Implementation)** - Guardrails, API, Multi-SKU, Discount Editor can run in parallel (Weeks 2-6)
- **Track A-R (Reuse & Legacy Parity)** can run in parallel with Track A (Weeks 2-4)
- **Track B (Catalog Tooling)** can run in parallel with Track A (Weeks 3-6)
- **Track D0 (Costing Engine)** can run in parallel with Track A/B/E (Weeks 3-6)
- **Track C (Operational Readiness)** can run in parallel with Track D start (Weeks 7-8)
- **Track D (Costing & Reporting)** requires D0 Gate passed, can run in parallel with Track C (Weeks 7-10)
- **Legacy Parity Gate** must pass before integration (Week 8.5)
- **Integration** requires all tracks complete + Legacy Parity Gate passed (Week 9)

---

## ⚠️ Key Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| UI complexity exceeds timeline | High | MVP screens only, defer polish to Phase-7 |
| Catalog import complexity | Medium | Start with single series (LC1E), expand later |
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
- ❌ Cannot change schema semantics
- ❌ Cannot change guardrails
- ❌ Cannot change core business rules
- ❌ Cannot change locking model
- ❌ Cannot change resolution logic

---

## 🎯 Success Metrics

Phase-6 success is measured by:

1. **Usability**
   - ✅ Internal users can create quotations without errors
   - ✅ Average quotation creation time < 15 minutes
   - ✅ User satisfaction score > 4/5

2. **Catalog Management**
   - ✅ Catalog entries can be imported safely
   - ✅ Import validation catches 95%+ of errors before publish
   - ✅ Series onboarding time < 2 hours per series

3. **Pricing**
   - ✅ Pricing overrides work correctly
   - ✅ Price resolution accuracy > 99%
   - ✅ Override approval time < 24 hours

4. **Audit & Governance**
   - ✅ Audit trail is visible and complete
   - ✅ All changes are audited
   - ✅ Approval workflows are enforced

5. **Error Handling**
   - ✅ Errors are understandable and actionable
   - ✅ Error resolution time < 5 minutes
   - ✅ User-reported error rate < 5%

---

## 🔗 Related Documents

- **Phase-6 Charter:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md`
- **Phase-6 Legacy Parity Checklist:** `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`
- **Phase-5 Execution Plan:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_EXECUTION_PLAN_UPDATED.md`
- **Phase-5 Detailed Working Record:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DETAILED_WORKING_RECORD.md`
- **Catalog Governance SOP:** `docs/PHASE_5/00_GOVERNANCE/CATALOG_GOVERNANCE_SOP.md`
- **Schema Canon:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Decision Register:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md`
- **Nish System Reference:** `project/nish/NISH_SYSTEM_REFERENCE.md`
- **Nish Review Report:** `project/nish/PHASE_6_NISH_REVIEW_REPORT.md`

---

## 📅 Timeline Summary

| Phase | Weeks | Duration | Status |
|-------|-------|----------|--------|
| **Entry Gate** | Week 0 | 1 week | ⏳ PENDING |
| **Track A: Productisation** | Weeks 1-6 | 6 weeks | ⏳ PENDING |
| **Track A-R: Reuse & Legacy Parity** | Weeks 2-4 | 3 weeks | ⏳ PENDING |
| **Track B: Catalog Tooling** | Weeks 3-6 | 4 weeks | ⏳ PENDING |
| **Track C: Operational Readiness** | Weeks 7-8 | 2 weeks | ⏳ PENDING |
| **Track D0: Costing Engine Foundations** | Weeks 3-6 | 4 weeks | ⏳ PENDING |
| **Track D: Costing & Reporting** | Weeks 7-10 | 4 weeks | ⏳ PENDING |
| **Track E: Canon Implementation** | Weeks 0-6 | 6 weeks | ⏳ PENDING |
| **Legacy Parity Gate** | Week 8.5 | 0.5 weeks | ⏳ PENDING |
| **Integration & Stabilisation** | Weeks 9-10 | 2 weeks | ⏳ PENDING |
| **Buffer & Closure** | Weeks 11-12 | 2 weeks | ⏳ PENDING |
| **TOTAL** | **Weeks 0-12** | **12-13 weeks** | ⏳ PENDING |

---

**Last Updated:** 2025-01-27  
**Status:** v1.3 (Legacy Parity Added) → Ready for Phase-5 completion  
**Next Action:** Wait for Phase-5 completion → Begin Week 0 entry gate verification

---

## 📋 Version History

- **v1.0:** Initial Phase-6 Execution Plan
- **v1.1:** Added costing dashboard feature (Track D)
- **v1.2 (Corrected):** Added Track D0, reorganized Track E, QCD emphasis
- **v1.3 (Legacy Parity Added):** Added Track A-R (Reuse & Legacy Parity) + Legacy Parity Verification Gate
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
