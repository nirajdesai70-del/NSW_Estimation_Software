# Phase 6 Unified Task & Todo List
## Consolidated from All Reviewed Documents

**Date:** 2025-01-27  
**Status:** IN PROGRESS  
**Purpose:** Unified list of all tasks and todos extracted from Phase 6 documents

---

## 📊 Summary

- **Total Tasks Identified:** 150+ tasks
- **Tasks Completed:** 8 tasks (Week 1-4)
- **Tasks Pending:** 142+ tasks
- **Tracks:** 7 tracks (A, A-R, B, C, D0, D, E)

---

## 🔒 Locked Invariants (Rules)

1. **Copy-never-link** - Never link, always copy
2. **QCD/QCA separation** - Cost summary reads QCA only
3. **No costing breakup in quotation view** - Summary-only display
4. **Fabrication remains summary-only** - No detailed breakdown
5. **Schema canon frozen (Phase-6)** - Schema canon is frozen during Phase 6
6. **All changes are additive + read-only** - No destructive changes
7. **Phase-6 Rule:** "Phase-6 may add features, but may not change meaning. Phase-6 must preserve all legacy capabilities through copy-never-link reuse."

---

## 📋 Tasks by Track

### Track A: Productisation (45 tasks)

#### Week 1: Quotation & Panel UI
- [ ] **P6-UI-001:** Quotation list page
- [ ] **P6-UI-002:** Quotation create page
- [ ] **P6-UI-003:** Quotation detail page
- [ ] **P6-UI-004:** Panel detail page (with Cost Adders section - UPDATE)
- [ ] **P6-UI-005:** Panel create/edit forms
- [ ] **P6-QUO-001A:** Ensure quotation creation stores customer_name_snapshot always
- [ ] **P6-QUO-001B:** Allow customer_id optional (future normalization)

#### Week 2: Feeder/BOM Hierarchy UI + Guardrails
- [ ] **P6-UI-006:** Feeder list page
- [ ] **P6-UI-007:** Feeder create/edit forms
- [ ] **P6-UI-008:** BOM detail page
- [ ] **P6-UI-009:** BOM item add/edit/delete
- [ ] **P6-UI-010:** BOM hierarchy visualization
- [ ] **P6-UI-010A:** BOM item quantity editing
- [ ] **P6-BOM-TRACK-001:** Populate BOM tracking fields on create/copy
- [ ] **P6-BOM-TRACK-002:** Update is_modified/modified_by/modified_at on edits
- [ ] **P6-BOM-TRACK-003:** UI indicator "modified vs original" (read-only badge)

#### Week 3: Pricing UX + Cost Engine + Reuse
- [ ] **P6-UI-011:** Pricing resolution display (PRICELIST/MANUAL/FIXED)
- [ ] **P6-UI-012:** Pricing override UI
- [ ] **P6-UI-013:** Locking behaviour visibility (line-item)
- [ ] **P6-UI-014:** Error & warning surfacing
- [ ] **P6-UI-015:** L0 → L1 → L2 resolution UX
- [ ] **P6-UI-016:** Resolution status indicators
- [ ] **P6-VAL-001:** Implement runtime guardrails G1-G8 in service layer
- [ ] **P6-VAL-002:** Ensure DB CHECK/constraints enforced & migrations match Schema Canon
- [ ] **P6-VAL-003:** API validation parity with 02_VALIDATION_MATRIX.md
- [ ] **P6-VAL-004:** Guardrail test suite (unit + integration)

#### Week 4: Multi-SKU & Resolution Constraints
- [ ] **P6-SKU-001:** Implement multi-SKU line grouping via parent_line_id
- [ ] **P6-SKU-002:** metadata_json structure + UI safe editing rules
- [ ] **P6-SKU-003:** Validation & UI display of multi-SKU groups
- [ ] **P6-RES-023:** Enforce resolution constraints exactly as Schema Canon
- [ ] **P6-RES-024:** Errors must map to B3 error taxonomy codes

#### Week 5: Locking Verification
- [ ] **P6-LOCK-000:** Verify no higher-level locking introduced (schema + UI)

#### Week 6: Discount Editor
- [ ] **P6-DISC-001:** Implement Discount Editor screen /quotation/{id}/discount
- [ ] **P6-DISC-002:** Filters (Make/Category/Item/Desc/SKU/Panel/BOM)
- [ ] **P6-DISC-003:** Preview + Apply (transaction)
- [ ] **P6-DISC-004:** Audit log entry + approval rules (tie to Track C)

---

### Track A-R: Reuse & Legacy Parity (7 tasks)

#### Week 2.5: Reuse Foundations
- [ ] **P6-UI-REUSE-001:** Copy quotation (deep copy)
- [ ] **P6-UI-REUSE-002:** Copy panel into quotation

#### Week 3: Feeder & BOM Reuse
- [ ] **P6-UI-REUSE-003:** Copy feeder (Level-0 BOM)
- [ ] **P6-UI-REUSE-004:** Copy BOM under feeder
- [ ] **P6-UI-REUSE-005:** Apply Master BOM template

#### Week 4: Editability & Guardrails Validation
- [ ] **P6-UI-REUSE-006:** Post-reuse editability check
- [ ] **P6-UI-REUSE-007:** Guardrail enforcement after reuse

---

### Track B: Catalog Tooling (16 tasks)

#### Week 3-6: Catalog Management
- [ ] **B-001:** Catalog import UI
- [ ] **B-002:** Catalog import scripts
- [ ] **B-003:** Series-wise catalog onboarding
- [ ] **B-004:** Validation previews (before publish)
- [ ] **B-005:** Catalog governance enforcement
- [ ] **B-006:** Catalog search and filtering
- [ ] **B-007:** Catalog export functionality
- [ ] **B-008:** Catalog validation workflows
- [ ] **B-009:** Catalog item management UI
- [ ] **B-010:** Catalog category management
- [ ] **B-011:** Catalog attribute management
- [ ] **B-012:** Catalog type management
- [ ] **B-013:** Catalog subcategory management
- [ ] **B-014:** Catalog import validation
- [ ] **B-015:** Catalog publish workflow
- [ ] **B-016:** Catalog versioning

---

### Track C: Operational Readiness (12 tasks)

#### Week 7-8: Operations
- [ ] **C-001:** Role-based access (basic)
- [ ] **C-002:** User management UI
- [ ] **C-003:** Role management UI
- [ ] **C-004:** Permission configuration
- [ ] **C-005:** Approval flows (price changes, overrides)
- [ ] **C-006:** Approval workflow UI
- [ ] **C-007:** Audit visibility (read-only)
- [ ] **C-008:** Audit log UI
- [ ] **C-009:** Initial SOPs documentation
- [ ] **C-010:** Deployment scripts
- [ ] **C-011:** Monitoring setup
- [ ] **C-012:** Error handling framework

---

### Track D0: Costing Engine Foundations (14 tasks)

#### Week 3: Cost Heads Seeding
- [ ] **P6-COST-D0-008:** Seed generic cost heads for cost adders
  - MATERIAL, BUSBAR, FABRICATION, LABOUR, TRANSPORTATION, ERECTION, COMMISSIONING, MISC

#### Week 4: Cost Template & Sheet Tables
- [ ] **P6-COST-D0-009:** Create cost template master tables
- [ ] **P6-COST-D0-010:** Create cost sheet runtime tables

#### Week 5: Cost Sheet Calculation & Roll-Up
- [ ] **P6-COST-D0-011:** Implement cost sheet calculation engine
- [ ] **P6-COST-D0-012:** Implement cost adder roll-up generator
- [ ] **P6-COST-D0-013:** Implement QCA (Quote Cost Adders) dataset

#### Week 6: Cost Adders Integration & Gate
- [ ] **P6-COST-D0-014:** Update D0 Gate checklist to include cost adders

#### Existing Track D0 Tasks
- [ ] **P6-COST-D0-001:** Effective quantity engine (BaseQty → EffQtyPerPanel → EffQtyTotal)
- [ ] **P6-COST-D0-002:** CostHead mapping precedence (D-006)
- [ ] **P6-COST-D0-003:** Canonical dataset: QuotationCostDetail (QCD) + JSON export endpoint
- [ ] **P6-COST-D0-004:** Numeric validation vs reference Excel
- [ ] **P6-COST-D0-005:** Performance hardening gate for "large quotations"
- [ ] **P6-COST-D0-006:** D0 Gate signoff (QCD v1.0 stable + QCA v1.0 stable)
- [ ] **P6-COST-D0-007:** Cost Adders engine (cost templates, cost sheets, QCA dataset)

---

### Track D: Costing & Reporting (20 tasks)

#### Week 7: Cost Adders UI Foundation
- [ ] **P6-COST-019:** Add Cost Adders section to Panel Detail page
- [ ] **P6-COST-020:** Implement cost sheet editor UI
- [ ] **P6-COST-003-UPDATE:** Include cost adders in snapshot
- [ ] **P6-COST-004-UPDATE:** Include cost adders in panel summary

#### Week 8: CostHead Pivot & Reporting
- [ ] **P6-COST-006-UPDATE:** Include cost adders in CostHead pivot
- [ ] **P6-COST-005:** CostHead system UI
- [ ] **P6-COST-007:** Global dashboard for margins
- [ ] **P6-COST-008:** Global dashboard for hit rates
- [ ] **P6-COST-009:** Global dashboard for cost drivers

#### Week 10: Excel Export
- [ ] **P6-COST-015-UPDATE:** Include cost adders in Excel export

#### Existing Track D Tasks
- [ ] **P6-COST-001:** Costing Pack per quotation (snapshot)
- [ ] **P6-COST-002:** Panel summary view
- [ ] **P6-COST-010:** Cost reporting UI
- [ ] **P6-COST-011:** Cost drift detection UI
- [ ] **P6-COST-012:** Cost integrity checks UI
- [ ] **P6-COST-013:** Cost analysis tools
- [ ] **P6-COST-014:** Cost comparison tools
- [ ] **P6-COST-016:** Cost export functionality
- [ ] **P6-COST-017:** Cost dashboard widgets
- [ ] **P6-COST-018:** Cost reporting templates

---

### Track E: Canon Implementation & Contract Enforcement (29 tasks)

#### Week 0-1: Database Implementation
- [ ] **P6-DB-001:** Choose DB creation approach (DDL vs migrations) and lock method
- [ ] **P6-DB-002:** Implement DB schema from Schema Canon v1.0 (DDL or migrations)
- [ ] **P6-DB-003:** Execute seed script (C5) on dev/stage
- [ ] **P6-DB-004:** Schema parity gate (DB == Canon v1.0)
- [ ] **P6-DB-005:** Seed cost template master data
- [ ] **P6-DB-006:** Add baseline indexes per Canon + performance assumptions

#### Week 0-6: Guardrails & API
- [ ] **P6-GUARD-001:** Implement guardrails G1-G8 runtime enforcement
- [ ] **P6-GUARD-002:** Guardrail test suite
- [ ] **P6-API-001:** Implement API endpoints per 01_API_SURFACE_MAP.md (optional/deferred)
- [ ] **P6-API-002:** Apply JSON schemas per OpenAPI skeleton (optional/deferred)
- [ ] **P6-API-003:** Validation matrix parity (optional/deferred)
- [ ] **P6-API-004:** Error taxonomy + request_id propagation (optional/deferred)
- [ ] **P6-API-005:** Contract tests (optional/deferred)
- [ ] **P6-API-006:** Versioning policy implementation (optional/deferred)

#### Week 0-6: Multi-SKU & Other
- [ ] **P6-MULTI-SKU-001:** Multi-SKU linkage (D-007) implementation
- [ ] **P6-DISCOUNT-001:** Discount Editor (legacy parity)
- [ ] **P6-BOM-TRACK-001:** BOM tracking fields runtime behavior
- [ ] **P6-CUSTOMER-001:** Customer snapshot handling (D-009)
- [ ] **P6-RESOLUTION-001:** Resolution constraints enforcement (A10)

---

### Week 0: Entry Gate & Setup (8 tasks)

#### Entry Criteria Verification
- [ ] **P6-ENTRY-001:** Verify SPEC-5 v1.0 frozen ✅
- [ ] **P6-ENTRY-002:** Verify Schema Canon locked ✅
- [ ] **P6-ENTRY-003:** Verify Decision Register closed ✅
- [ ] **P6-ENTRY-004:** Verify Freeze Gate Checklist 100% verified ✅
- [ ] **P6-ENTRY-005:** Verify Core resolution engine tested ✅
- [ ] **P6-ENTRY-006:** Naming conventions compliance check

#### Setup Tasks
- [ ] **P6-SETUP-001:** Create Phase-6 project structure
- [ ] **P6-SETUP-002:** Review Phase-5 deliverables
- [ ] **P6-SETUP-003:** Create Phase-6 task register
- [ ] **P6-SETUP-004:** Create Costing manual structure
- [ ] **P6-SETUP-005:** Freeze Costing Engine Contract (QCD v1.0)
- [ ] **P6-SETUP-006:** Define D0 Gate checklist (QCD readiness)
- [ ] **P6-SETUP-007:** Review Phase-5 deliverables for implementation obligations
- [ ] **P6-SETUP-008:** Create module folder boundaries + PR rules

---

### Week 4: Cost Summary APIs (Track D) - COMPLETED ✅

- [x] **D-001:** Quotation lifecycle visibility (read-only)
  - Added `quotation_state`, `state_timestamp`
  - Tests: `test_quotation_state_visibility.py`, `test_freeze_immutability_cost_adders.py`
- [x] **D-002:** Cost integrity guardrails (drift detection)
  - Added `integrity_status`, `integrity_hash`, `integrity_reasons`
  - Service: `app/services/cost_integrity_service.py`
  - Tests: `test_cost_integrity_hash_stable.py`, `test_cost_integrity_hash_changes_on_qca_update.py`
- [x] **D-003:** Expanded summary read APIs (render helpers)
  - Added `panel_count`, `has_catalog_bindings`, `cost_head_codes`
  - Fixed mutable default: `integrity_reasons` uses `Field(default_factory=list)`
  - Tests: `test_cost_summary_no_breakup_strict.py`, `test_cost_summary_render_helpers.py`
- [x] **D-004:** Consolidated checks + API surface guard
  - Consolidated runner: `scripts/run_phase6_week4_checks.sh`
  - API surface whitelist guard: `test_cost_summary_top_level_whitelist.py`

---

### Week 1: Schema Canon Setup (Track E) - COMPLETED ✅

- [x] **E-001:** Database setup from Schema Canon
- [x] **E-002:** Canon drift detection
- [ ] **E-003:** Canon validation tools (pending)
- [ ] **E-004:** Schema migration scripts (pending)

---

### Week 3: Regression Tests - COMPLETED ✅

- [x] **REGRESSION-001:** Regression tests created (3 tests)
- [x] **REGRESSION-002:** All tests passing (0.32-0.46s execution time)

---

## 🚨 Gaps & Issues

### Technical Gaps
1. **QCD Contract Update Required** - Must update to v1.1 to include cost adders
2. **Template Line Structure Finalization** - Must be finalized before implementation
3. **Performance Testing with Cost Adders** - Must remain acceptable

### Process Gaps
4. **Infrastructure Setup Tasks Missing** - Need to add to Week 0
5. **Tool License Approval Process** - Need to define approval process

### Documentation Gaps
6. **Week 2-3 Evidence Missing** - Need complete evidence packs
7. **Week-by-Week Detailed Plans Missing** - Some week plans are empty
8. **Some Files Empty** - Need to investigate and restore from different commits

---

## 📊 Task Statistics

### By Status
- **Completed:** 8 tasks (5%)
- **In Progress:** 0 tasks
- **Pending:** 142+ tasks (95%)

### By Track
- **Track A:** 45 tasks
- **Track A-R:** 7 tasks
- **Track B:** 16 tasks
- **Track C:** 12 tasks
- **Track D0:** 14 tasks
- **Track D:** 20 tasks
- **Track E:** 29 tasks
- **Week 0:** 8 tasks
- **Other:** 10+ tasks

### By Priority
- **P0 (Critical):** 20 tasks (Track E, Track D0)
- **P1 (High):** 60 tasks (Track A, Track D)
- **P2 (Medium):** 50 tasks (Track B, Track C, Track A-R)
- **P3 (Low):** 20+ tasks (Other)

---

## 🎯 Next Steps

1. **Continue Review**
   - Review remaining week plans
   - Review additional governance documents
   - Extract more tasks and todos

2. **Unify Task List**
   - Remove duplicates
   - Organize by week and track
   - Add dependencies
   - Add priorities

3. **Create Task Matrix**
   - Use template from PHASE_6_MATRIX_TEMPLATES.md
   - Populate with all tasks
   - Link to work breakdown
   - Link to rules

---

**Status:** IN PROGRESS  
**Total Tasks:** 150+ tasks  
**Tasks Reviewed:** 150+ tasks  
**Next Action:** Continue reviewing files and extracting tasks
