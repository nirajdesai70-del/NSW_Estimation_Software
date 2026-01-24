# Phase-6 Week-3 Detailed Plan

**Week:** Week-3 (Pricing Resolution UX + Cost Engine Foundations + Guardrails Runtime)  
**Status:** ⚠️ PARTIAL (Cost adders backend exists; pricing UX + guardrails + QCD missing)  
**Closure Status:** ⏳ Pending completion  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-3 introduces pricing resolution UX, costing engine foundations (QCD), and guardrails runtime enforcement. This is the first high-coupling week, bringing together UI (Track A), engine foundations (Track D0), and compliance validation (Track E). Week-3 also continues reuse workflows (Track A-R) if Week-2 readiness allows.

**Key Deliverables:**
- Pricing Resolution UX (RateSource selector, auto-pricing, manual/fixed pricing, status indicators)
- Costing Engine Foundations (QCD generator, EffectiveQty logic, cost heads seeding)
- Guardrails G1-G8 Runtime Enforcement (compliance - mandatory)
- Reuse continuation (copy feeder/BOM, master BOM apply if ready)

**Critical Alarms (From Matrix):**
- 🔴 **3 Compliance Alarms** (must resolve before Phase-6 closure)
  - ALARM-GUARDRAILS (P6-VAL-001..004 - mandatory Weeks 2-4)
  - ALARM-PRICING-UX (P6-UI-011..016 - pricing resolution UX)
  - ALARM-QCD-D0-GATE (P6-COST-D0-001..003, P6-COST-D0-008..010, P6-COST-D0-013 - QCD generator + D0 Gate)
- 🟠 **High Priority Items** (design documentation, reuse continuation)
- 🟡 **Medium Priority Items** (partial evidence, needs completion)

**Note:** Week-3 is not about dashboards, exports, or deep costing pack UIs. It focuses on making quotation lines price-resolvable and canon-valid, and starting engine-first costing foundations.

---

## Week-3 Task Breakdown

### Track: Pricing Resolution UX (Track A) + Cost Engine Foundations (Track D0) + Guardrails Runtime (Track E) + Reuse Continuation (Track A-R)

#### Track A - Pricing Resolution UX

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-011 | Design pricing resolution UX | `docs/PHASE_6/UI/PRICING_RESOLUTION_UX.md` | ❌ MISSING | 🟠 | Design document with RateSource selector, pricing modes, status indicators |
| P6-UI-012 | Implement RateSource selector | UI component + API write (PRICELIST/MANUAL_WITH_DISCOUNT/FIXED_NO_DISCOUNT) | ❌ MISSING | 🔴 **COMPLIANCE** | RateSource selector dropdown/radio buttons. Part of ALARM-PRICING-UX |
| P6-UI-013 | Implement price auto-population | Service behavior + UI display (populate from pricelist for PRICELIST mode) | ❌ MISSING | 🔴 **COMPLIANCE** | Auto-populate rate from pricelist when RateSource=PRICELIST. Part of ALARM-PRICING-UX |
| P6-UI-014 | Implement manual pricing controls | UI + calculation logic (discount-driven calculation) | ❌ MISSING | 🔴 **COMPLIANCE** | Manual pricing with discount input and calculation. Part of ALARM-PRICING-UX |
| P6-UI-015 | Implement fixed pricing controls | UI + validation (no discount allowed for FIXED_NO_DISCOUNT) | ❌ MISSING | 🔴 **COMPLIANCE** | Fixed pricing mode with discount disabled/forced to 0. Part of ALARM-PRICING-UX |
| P6-UI-016 | Implement pricing status indicators | Component/BOM/panel summary indicators (priced/missing/unresolved) | ❌ MISSING | 🔴 **COMPLIANCE** | Visual indicators for pricing status at item/BOM/panel levels. Part of ALARM-PRICING-UX |

**Track A Status:** ❌ MISSING (Pricing UX not implemented - all tasks missing)

**Scope Guard:** No costing breakup. No dashboard. Focus on pricing resolution only.

---

#### Track D0 - Costing Engine Foundations (Engine-First Approach)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-COST-D0-001 | EffectiveQty logic | Service/helper for EffectiveQty calculation | ❌ MISSING | 🔴 **COMPLIANCE** | EffectiveQty = PanelQty × FeederQty × BomQtyChain × ItemQty. Part of ALARM-QCD-D0-GATE |
| P6-COST-D0-002 | CostHead precedence | Resolution service for cost head precedence | ❌ MISSING | 🟠 | Cost head precedence logic (BUSBAR/LABOUR/etc.). Not blocking but important |
| P6-COST-D0-003 | QCD generator + JSON endpoint | Endpoint + schema doc (BOM-only dataset) | ❌ MISSING | 🔴 **COMPLIANCE** | QCD JSON export endpoint (BOM-only, no costing breakup). Part of ALARM-QCD-D0-GATE |
| P6-COST-D0-008 | Cost heads seeded | Seed proof (cost heads: BUSBAR, LABOUR, etc.) | ⚠️ PARTIAL | 🟡 | Cost heads behaving (BUSBAR/LABOUR etc.) → likely seeded, needs verification |
| P6-COST-D0-009 | Cost templates tables | Cost template tables in schema | ❌ MISSING | 🔴 **COMPLIANCE** | Cost template tables (if not in schema yet). Part of ALARM-QCD-D0-GATE. **IMPORTANT:** Only implement if these tables already exist in Schema Canon v1.0. If not present, create a defer memo and move table creation to a Canon-v1.1 decision (Senate). |
| P6-COST-D0-010 | Cost sheets runtime tables | Cost sheet runtime tables in schema | ❌ MISSING | 🔴 **COMPLIANCE** | Cost sheet runtime tables (if not in schema yet). Part of ALARM-QCD-D0-GATE. **IMPORTANT:** Only implement if these tables already exist in Schema Canon v1.0. If not present, create a defer memo and move table creation to a Canon-v1.1 decision (Senate). |
| P6-COST-D0-013 | QCA dataset + JSON export | QCA behavior + export endpoint | ⚠️ PARTIAL | 🟡 | QCA behavior via quote_cost_adders; export endpoint not proven |
| P6-DB-005 | Cost template seed data | Template seed data specification | ❌ MISSING | 🔴 **COMPLIANCE** | Cost template seed data (from Week-0 alarm). Part of ALARM-QCD-D0-GATE |

**Track D0 Status:** ⚠️ PARTIAL (Cost adders backend exists; QCD generator + tables missing)

**Important:** Any DB work must be within Canon tables already frozen. No semantic change. QCD contract v1.0 frozen (Week-0 governance pack).

---

#### Track E - Guardrails Runtime Enforcement (Compliance Obligation - Weeks 2-4)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-VAL-001 | Guardrails G1-G8 runtime enforcement | Service validations (G1-G8 enforcement) | ❌ MISSING | 🔴 **COMPLIANCE** | Runtime enforcement of guardrails G1-G8. Part of ALARM-GUARDRAILS (Weeks 2-4) |
| P6-VAL-002 | DB constraint parity | Parity proof doc + drift checks | ⚠️ PARTIAL | 🔴 **COMPLIANCE** | DB constraints aligned with guardrails. Drift check covers some constraints; guardrails not proven. Part of ALARM-GUARDRAILS |
| P6-VAL-003 | API validation parity | API behavior equals 02_VALIDATION_MATRIX.md | ❌ MISSING | 🔴 **COMPLIANCE** | API validation matching validation matrix. Part of ALARM-GUARDRAILS |
| P6-VAL-004 | Guardrail test suite | Unit + integration tests | ❌ MISSING | 🔴 **COMPLIANCE** | Test suite for guardrails G1-G8. Part of ALARM-GUARDRAILS |

**Track E (Guardrails) Status:** ❌ MISSING (Compliance obligation - Weeks 2-4, blocking Phase-6 sign-off)

**Week-3 Focus Guard:** Implement guardrails for pricing + item constraints, not for future modules.

---

#### Track A-R - Reuse Continuation (Week-3 Slice)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-REUSE-003 | Copy feeder completion | Endpoint + UI action (if not fully verified) | ⚠️ PARTIAL | 🟠 | Copy feeder endpoint exists; needs verification/completion |
| P6-REUSE-004 | Copy BOM completion | Endpoint + UI action (if not fully verified) | ⚠️ PARTIAL | 🟠 | Copy BOM endpoint exists; needs verification/completion |
| P6-REUSE-005 | Apply Master BOM | Endpoint + UI action (if Week-2 readiness allows) | ❌ MISSING | 🔴 **COMPLIANCE** | Master BOM apply workflow. Part of ALARM-REUSE (if scheduled in Week-3) |

**Track A-R Status:** ⚠️ PARTIAL (Copy endpoints exist; master apply + verification missing)

**Note:** If Week-2 CRUD is not executed yet, REUSE UI work must be stubbed but not blocked.

---

## Alarm Summary for Week-3

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-GUARDRAILS** | Review 1 (Finalized Review 4) | P6-VAL-001..004 | Guardrails G1-G8 runtime + tests (Weeks 2-4) | ❌ MISSING | Implement guardrails runtime enforcement + DB parity + API parity + tests |
| **ALARM-PRICING-UX** | Review 1 (Finalized Review 4) | P6-UI-011..016 | Pricing resolution UX (RateSource selector + modes + indicators) | ❌ MISSING | Implement RateSource selector + auto-pricing + manual/fixed pricing + status indicators |
| **ALARM-QCD-D0-GATE** | Review 4 (Finalized Review 4) | P6-COST-D0-001..003, P6-COST-D0-008..010, P6-COST-D0-013, P6-DB-005 | QCD generator + D0 Gate (Weeks 3-6) | ❌ MISSING | Implement QCD generator + cost templates/sheets tables + seed data + QCA export |
| **ALARM-REUSE** (Week-3 portion) | Review 1 (Finalized Review 4) | P6-REUSE-005 | Master BOM apply (if scheduled in Week-3) | ❌ MISSING | Implement master BOM apply workflow (if Week-2 readiness allows) |

**Alarm Details:**

#### ALARM-GUARDRAILS (Compliance - Weeks 2-4)
- **Tasks Affected:** P6-VAL-001, P6-VAL-002, P6-VAL-003, P6-VAL-004
- **Impact:** Phase-5 compliance obligation. Guardrails G1-G8 runtime enforcement is mandatory (Weeks 2-4).
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (Weeks 2-4)
- **Resolution:** 
  - P6-VAL-001: Implement guardrails G1-G8 runtime enforcement
    - G1: Master BOM rejects ProductId (service validation)
    - G2: Production BOM requires ProductId (service validation)
    - G3: IsPriceMissing normalizes Amount (pricing service)
    - G4: RateSource consistency (pricing service)
    - G5: UNRESOLVED normalizes values (pricing service)
    - G6: FIXED_NO_DISCOUNT forces Discount=0 (discount service)
    - G7: Discount range validation 0-100 (discount service)
    - G8: L1-SKU reuse allowed (L1 validation service)
  - P6-VAL-002: Ensure DB constraint parity
    - Verify all CHECK constraints from Schema Canon are in migrations
    - Verify G7 discount range constraint (0-100) in DB
    - Verify resolution_status constraints in DB
    - Verify ProductId constraints in DB
    - Test constraint enforcement
  - P6-VAL-003: Implement API validation parity
    - Review validation matrix from Phase-5 (02_VALIDATION_MATRIX.md)
    - Implement API validation matching DB guardrails
    - Ensure all 8 guardrails validated at API layer
    - Map validation errors to error taxonomy codes
  - P6-VAL-004: Implement guardrail test suite
    - Create unit tests for each guardrail (G1-G8)
    - Create integration tests for guardrail enforcement
    - Test normalization behavior
    - Test constraint violations
    - Test error messages
- **Notes:** Guardrails G1-G8 runtime enforcement is a Phase-5 compliance obligation. Must be implemented during Weeks 2-4 for Phase-6 sign-off. Week-3 focus: pricing + item constraints.

#### ALARM-PRICING-UX (Compliance)
- **Tasks Affected:** P6-UI-011..016
- **Impact:** Core functionality gap. Pricing resolution UX is mandatory for quotation pricing workflow.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-UI-012: Implement RateSource selector
    - Dropdown/radio buttons for RateSource selection
    - Options: PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT
    - API write to quotation_sale_bom_items.RateSource
  - P6-UI-013: Implement price auto-population
    - When RateSource=PRICELIST, auto-populate rate from pricelist
    - Service behavior + UI display
    - Handle pricelist lookup by ProductId
  - P6-UI-014: Implement manual pricing controls
    - Discount input field
    - Discount-driven calculation (NetRate = Rate × (1 - Discount/100))
    - UI controls for manual rate + discount
  - P6-UI-015: Implement fixed pricing controls
    - Fixed price input
    - Discount disabled/forced to 0 for FIXED_NO_DISCOUNT
    - Validation: no discount allowed
  - P6-UI-016: Implement pricing status indicators
    - Visual indicators at component/BOM/panel levels
    - Statuses: priced, missing, unresolved
    - Color coding or icons
- **Notes:** Pricing resolution UX enables quotation pricing workflow. All three RateSource modes must be supported.

#### ALARM-QCD-D0-GATE (Compliance - Weeks 3-6)
- **Tasks Affected:** P6-COST-D0-001..003, P6-COST-D0-008..010, P6-COST-D0-013, P6-DB-005
- **Impact:** Track D0 compliance. QCD generator and D0 Gate are mandatory for costing engine foundations.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (Weeks 3-6)
- **Resolution:** 
  - P6-COST-D0-001: Implement EffectiveQty logic
    - EffectiveQty = PanelQty × FeederQty × BomQtyChain × ItemQty
    - Service/helper for EffectiveQty calculation
    - Use in QCD generation
  - P6-COST-D0-003: Implement QCD generator + JSON endpoint
    - QCD JSON export endpoint (BOM-only dataset)
    - No costing breakup (per QCD contract v1.0)
    - Stable schema
  - P6-COST-D0-009/010: Implement cost templates/sheets tables (if not in schema)
    - Cost template tables (if schema allows)
    - Cost sheet runtime tables (if schema allows)
    - No semantic change (within Canon)
  - P6-COST-D0-008: Verify/complete cost heads seeding
    - Cost heads: BUSBAR, LABOUR, etc.
    - Seed verification
  - P6-DB-005: Implement cost template seed data
    - Cost template seed data specification
    - Seed data for cost templates
  - P6-COST-D0-013: Complete QCA dataset + JSON export
    - QCA behavior verification (quote_cost_adders exists)
    - QCA JSON export endpoint
- **Notes:** QCD contract v1.0 frozen (Week-0 governance pack). Engine-first approach. BOM-only dataset (no costing breakup). Any DB work within Canon tables only.

#### ALARM-REUSE (Week-3 Portion - Compliance)
- **Tasks Affected:** P6-REUSE-005 (Master BOM apply)
- **Impact:** Legacy parity requirement. Master BOM apply workflow is mandatory for reuse functionality.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-REUSE-005: Implement master BOM apply workflow
    - Master BOM selection UI
    - Copy master BOM to quotation workflow
    - Apply master BOM to panel/feeder
    - Handle master BOM hierarchy
- **Notes:** If Week-2 CRUD is not executed yet, REUSE UI work must be stubbed but not blocked. Master BOM apply may start in Week-3 if Week-2 readiness allows.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-UI-011 | P6-UI-011 | Design pricing resolution UX | ❌ MISSING | Create design document: `docs/PHASE_6/UI/PRICING_RESOLUTION_UX.md` |
| ALARM-COST-D0-002 | P6-COST-D0-002 | CostHead precedence | ❌ MISSING | Implement cost head precedence logic (BUSBAR/LABOUR/etc.) |
| ALARM-REUSE-003 | P6-REUSE-003 | Copy feeder completion | ⚠️ PARTIAL | Verify/complete copy feeder endpoint |
| ALARM-REUSE-004 | P6-REUSE-004 | Copy BOM completion | ⚠️ PARTIAL | Verify/complete copy BOM endpoint |

---

### 🟡 Medium Priority (Partial Evidence - Needs Completion)

These items have partial evidence but need completion.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| P6-COST-D0-008 | Cost heads seeded | ⚠️ PARTIAL | Verify cost heads seeding (BUSBAR/LABOUR/etc. behaving, needs verification) |
| P6-COST-D0-013 | QCA dataset + JSON export | ⚠️ PARTIAL | Verify QCA behavior (quote_cost_adders exists); implement/verify export endpoint |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-3 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-UI-011..016 (Pricing Resolution UX)
- ✅ P6-COST-D0-001..003 (QCD generator foundations)
- ✅ P6-COST-D0-008..010 (Cost heads + tables)
- ✅ P6-COST-D0-013 (QCA dataset)
- ✅ P6-DB-005 (Cost template seed data)
- ✅ P6-VAL-001..004 (Guardrails runtime)
- ✅ P6-REUSE-003..005 (Reuse continuation)

### ⚠️ Items Requiring Verification

1. **Pricing UX Implementation (P6-UI-011..016)**
   - Need to verify RateSource selector exists
   - Need to verify auto-pricing works
   - Need to verify manual/fixed pricing works
   - Need to verify status indicators work
   - Current status: ❌ MISSING (needs verification)

2. **QCD Generator (P6-COST-D0-001..003)**
   - Need to verify EffectiveQty logic exists
   - Need to verify QCD JSON endpoint exists
   - Current status: ❌ MISSING (needs verification)

3. **Cost Templates/Sheets Tables (P6-COST-D0-009/010)**
   - Need to verify tables exist in schema
   - Need to verify tables are within Canon
   - Current status: ❌ MISSING (needs verification)

4. **Guardrails Runtime Enforcement (P6-VAL-001..004)**
   - Need to verify guardrails G1-G8 are enforced
   - Need to verify DB constraint parity
   - Need to verify API validation parity
   - Need to verify test suite exists
   - Current status: ❌ MISSING (needs verification)

5. **Reuse Continuation (P6-REUSE-003..005)**
   - Need to verify copy feeder/BOM endpoints complete
   - Need to verify master BOM apply exists
   - Current status: ⚠️ PARTIAL (copy endpoints exist; master apply missing)

---

## Week-3 Closure Criteria

### Required for Closure

1. ⏳ **Guardrails G1-G8 Runtime Enforcement Implemented** (P6-VAL-001..004)
2. ⏳ **Pricing UX Complete** (P6-UI-011..016 - all RateSource modes)
3. ⏳ **QCD Generator + JSON Endpoint Implemented** (P6-COST-D0-001..003)
4. ⏳ **Cost Templates/Sheets Tables Verified/Created** (P6-COST-D0-009/010)
5. ⏳ **Cost Heads Seeding Verified** (P6-COST-D0-008)
6. ⏳ **Cost Template Seed Data Implemented** (P6-DB-005)
7. ⏳ **QCA Export Endpoint Verified/Implemented** (P6-COST-D0-013)
8. ⏳ **All Tests Passing** (Guardrails + pricing + QCD tests)
9. ⏳ **Design Documents Created** (P6-UI-011)
10. ⏳ **All Compliance Alarms Resolved** (4 compliance alarms)
11. ⏳ **Reuse Continuation Verified** (P6-REUSE-003..005 - if scheduled)
12. ⏳ **No "Meaning Change" Introduced** (canon respected)

### Current Closure Status

- **Structural Completion:** ⏳ PENDING (No scutwork plan mentioned yet)
- **Implementation Status:** ⚠️ PARTIAL (Cost adders backend exists; pricing UX + guardrails + QCD missing)
- **Compliance Alarms:** ❌ 4 alarms need resolution (ALARM-GUARDRAILS, ALARM-PRICING-UX, ALARM-QCD-D0-GATE, ALARM-REUSE Week-3 portion)
- **Formal Sign-off:** ⏳ PENDING

**Closure Rule:** Week-3 is CLOSED only if guardrails + pricing UX + QCD generator are implemented and tested, and no "meaning change" introduced (canon respected).

---

## Dependencies

### Requires

- **Week-1:** Add Panel + snapshot rules (planned/completed)
- **Week-2:** Hierarchy CRUD plan exists (execution can lag, but APIs should exist for full pricing context)

### Blocks

- **Week-5/6:** Locking and error UX relies on guardrails and pricing statuses being stable
- **Track D (Week-7):** Costing pack depends on D0 foundations (QCD generator)

---

## Risks & Mitigations

### Risk 1: Pricing UX Implemented Without Guardrails Parity → Inconsistent Data

**Mitigation:** Implement guardrails + pricing together; single runner gate.

### Risk 2: QCD Scope Creep Into Costing Breakup or UI Details

**Mitigation:** QCD contract frozen (Week-0 governance pack); keep BOM-only; reject new fields.

### Risk 3: Master BOM Apply Attempted Before CRUD Hierarchy Stable

**Mitigation:** Allow API-only readiness; UI enablement gated.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Resolve Compliance Alarms (Blocking)

1. **ALARM-GUARDRAILS Resolution**
   - P6-VAL-001: Implement guardrails G1-G8 runtime enforcement
   - P6-VAL-002: Ensure DB constraint parity
   - P6-VAL-003: Implement API validation parity
   - P6-VAL-004: Implement guardrail test suite
   - Tests: test_guardrails_g1_g8.py

2. **ALARM-PRICING-UX Resolution**
   - P6-UI-012: Implement RateSource selector
   - P6-UI-013: Implement price auto-population
   - P6-UI-014: Implement manual pricing controls
   - P6-UI-015: Implement fixed pricing controls
   - P6-UI-016: Implement pricing status indicators
   - Tests: test_ratesource_selector.py, test_price_resolution_pricelist.py, test_manual_with_discount.py, test_fixed_no_discount.py, test_pricing_status_indicators.py

3. **ALARM-QCD-D0-GATE Resolution**
   - P6-COST-D0-001: Implement EffectiveQty logic
   - P6-COST-D0-003: Implement QCD generator + JSON endpoint
   - P6-COST-D0-009/010: Verify/create cost templates/sheets tables
   - P6-COST-D0-008: Verify cost heads seeding
   - P6-DB-005: Implement cost template seed data
   - P6-COST-D0-013: Complete QCA export endpoint
   - Tests: test_qcd_json_export.py, test_effective_qty.py

4. **ALARM-REUSE Resolution (Week-3 Portion)**
   - P6-REUSE-005: Implement master BOM apply workflow (if Week-2 readiness allows)
   - Tests: test_master_bom_apply.py

#### Priority 2: Complete Documentation

5. **Design Documents**
   - P6-UI-011: Create pricing resolution UX design document

6. **Implementation Completion**
   - P6-REUSE-003: Verify/complete copy feeder endpoint
   - P6-REUSE-004: Verify/complete copy BOM endpoint
   - P6-COST-D0-002: Implement cost head precedence logic

#### Priority 3: Verification

7. **Implementation Verification**
   - Verify guardrails enforcement works
   - Verify pricing UX works (all modes)
   - Verify QCD generator works
   - Verify cost templates/sheets tables exist
   - Verify all tests pass

---

## Implementation Artifacts

### Expected Artifacts

1. **Scripts:**
   - `scripts/run_week3_checks.sh` - Week-3 verification runner
     - Runs all Week-3 tests (guardrails + pricing + QCD)
     - Verifies API endpoints
     - Validates guardrails enforcement
     - Validates pricing UX functionality
     - Validates QCD generator
     - Generates evidence summary

2. **Tests:**
   - `tests/pricing/test_ratesource_selector.py` - RateSource selector tests
     - Test RateSource selection (PRICELIST/MANUAL_WITH_DISCOUNT/FIXED_NO_DISCOUNT)
     - Test API write to RateSource field
     - Test UI component behavior
   - `tests/pricing/test_price_resolution_pricelist.py` - Price auto-population tests
     - Test auto-populate rate from pricelist (PRICELIST mode)
     - Test pricelist lookup by ProductId
     - Test service behavior + UI display
   - `tests/pricing/test_manual_with_discount.py` - Manual pricing tests
     - Test discount input and calculation
     - Test NetRate calculation (Rate × (1 - Discount/100))
     - Test manual rate + discount controls
   - `tests/pricing/test_fixed_no_discount.py` - Fixed pricing tests
     - Test fixed price input
     - Test discount disabled/forced to 0 (FIXED_NO_DISCOUNT)
     - Test validation: no discount allowed
   - `tests/pricing/test_pricing_status_indicators.py` - Pricing status indicator tests
     - Test status indicators at component/BOM/panel levels
     - Test statuses: priced, missing, unresolved
     - Test color coding/icons
   - `tests/guardrails/test_guardrails_g1_g8.py` - Guardrails runtime enforcement tests
     - Test guardrails G1-G8 enforcement
     - Test normalization behavior
     - Test constraint violations
     - Test error messages
     - Test DB constraint parity
     - Test API validation parity
   - `tests/qcd/test_qcd_json_export.py` - QCD generator tests
     - Test QCD JSON export endpoint
     - Test BOM-only dataset structure
     - Test stable schema
     - Test no costing breakup (per QCD contract)
   - `tests/qcd/test_effective_qty.py` - EffectiveQty logic tests
     - Test EffectiveQty calculation (PanelQty × FeederQty × BomQtyChain × ItemQty)
     - Test service/helper behavior

3. **Evidence:**
   - `evidence/PHASE6_WEEK3_EVIDENCE_PACK.md` - Week-3 evidence documentation
     - API endpoint documentation
     - Test results summary
     - Pricing UI screenshots (minimal)
     - API sample outputs
     - Test runner output
     - QCD JSON sample output

4. **API Endpoints:**
   - PUT/PATCH /api/v1/quotation/{id}/panel/{panelId}/bom/{bomId}/item/{itemId}/ratesource - Update RateSource
   - GET /api/v1/quotation/{id}/panel/{panelId}/bom/{bomId}/item/{itemId}/price - Get price (auto-populate from pricelist)
   - PUT/PATCH /api/v1/quotation/{id}/panel/{panelId}/bom/{bomId}/item/{itemId}/price - Update price (manual/fixed)
   - GET /api/v1/quotation/{id}/qcd - QCD JSON export endpoint
   - GET /api/v1/quotation/{id}/qca - QCA JSON export endpoint (if not exists)
   - POST /api/v1/quotation/{id}/panel/{panelId}/master-bom/apply - Master BOM Apply API (if Week-2 readiness allows)

5. **Frontend Components:**
   - RateSource selector component (dropdown/radio buttons)
   - Price auto-population component
   - Manual pricing controls (discount input + calculation)
   - Fixed pricing controls (fixed price input, discount disabled)
   - Pricing status indicator component (priced/missing/unresolved)

6. **Backend Services:**
   - Pricing service (RateSource handling, auto-population, manual/fixed pricing)
   - Guardrails validation service (G1-G8 enforcement)
   - QCD generator service (EffectiveQty logic, QCD JSON generation)
   - Cost head precedence service

7. **Database Changes:**
   - quotation_sale_bom_items table (existing)
     - RateSource (ENUM: PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT)
     - Discount, NetRate, Amount
   - Cost template tables (if not in schema - within Canon)
   - Cost sheet runtime tables (if not in schema - within Canon)
   - Cost heads seeding (BUSBAR, LABOUR, etc.)
   - Cost template seed data

### Verification Checklist

- [ ] Verify scripts/run_week3_checks.sh exists and runs all tests
- [ ] Verify all test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify guardrails enforcement works (P6-VAL-001..004)
- [ ] Verify pricing UX works (all RateSource modes) (P6-UI-011..016)
- [ ] Verify QCD generator works (P6-COST-D0-001..003)
- [ ] Verify cost templates/sheets tables exist (P6-COST-D0-009/010)
- [ ] Verify cost heads seeding (P6-COST-D0-008)
- [ ] Verify cost template seed data (P6-DB-005)
- [ ] Verify QCA export endpoint (P6-COST-D0-013)
- [ ] Verify evidence/PHASE6_WEEK3_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-3 runner
- [ ] Verify no "meaning change" introduced (canon respected)

---

## Decision Point

**Week-3 Closure Status:**
- ⏳ **PENDING COMPLETION**

**Options:**
1. **"Close Week-3 and start Week-4 detailed plan"** - If all implementation artifacts verified and tests passing
2. **"Verify Week-3 implementation"** - If artifacts need verification
3. **"Complete Week-3 implementation"** - If guardrails, pricing UX, or QCD still missing

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-3 tasks)
- **QCD Contract v1.0:** (Week-0 governance pack - frozen)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"
- **Validation Matrix:** `docs/PHASE_5/02_VALIDATION_MATRIX.md` (for API validation parity)

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks** | 18 | All captured from matrix |
| **Compliance Alarms** | 4 | 🔴 Must resolve |
| **High Priority Alarms** | 4 | 🟠 Should resolve |
| **Medium Priority Items** | 2 | 🟡 Needs completion |
| **Completed Tasks** | 0 | None fully complete |
| **Partial Tasks** | 4 | ⚠️ PARTIAL (P6-COST-D0-008, P6-COST-D0-013, P6-REUSE-003/004) |
| **Missing Tasks** | 14 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-GUARDRAILS:** Implement guardrails G1-G8 runtime enforcement + DB parity + API parity + tests (P6-VAL-001..004)
- [ ] **ALARM-PRICING-UX:** Implement RateSource selector + auto-pricing + manual/fixed pricing + status indicators (P6-UI-011..016)
- [ ] **ALARM-QCD-D0-GATE:** Implement QCD generator + cost templates/sheets tables + seed data + QCA export (P6-COST-D0-001..003, P6-COST-D0-008..010, P6-COST-D0-013, P6-DB-005)
- [ ] **ALARM-REUSE (Week-3 portion):** Implement master BOM apply workflow (P6-REUSE-005 - if Week-2 readiness allows)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-UI-011:** Create pricing resolution UX design document (P6-UI-011)
- [ ] **ALARM-COST-D0-002:** Implement cost head precedence logic (P6-COST-D0-002)
- [ ] **ALARM-REUSE-003:** Verify/complete copy feeder endpoint (P6-REUSE-003)
- [ ] **ALARM-REUSE-004:** Verify/complete copy BOM endpoint (P6-REUSE-004)

### Documentation Tasks

- [ ] Complete pricing resolution UX design document
- [ ] Verify/complete reuse endpoints
- [ ] Verify cost heads seeding
- [ ] Verify QCA export endpoint
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify evidence pack is complete
- [ ] Verify no "meaning change" introduced (canon respected)

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After implementation verification
