# Phase-6 Cost Adders Integration - Analysis & Planning Review

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ANALYSIS COMPLETE - READY FOR DECISION  
**Purpose:** Comprehensive analysis of Cost Adders feature integration into Phase-6, identifying changes, roadblocks, and required inputs

---

## 🎯 Executive Summary

**Problem:** Current Phase-6 plan covers BOM material costing only. Real-world panel estimation requires additional cost categories (Fabrication, Busbar, Labour, Transportation, Erection, Commissioning) that are missing from the plan.

**Solution:** Add Cost Adders feature as internal costing sheets (not Excel-dependent) that integrate cleanly with existing BOM costing.

**Impact:** 
- ✅ **Phase-5 Safe:** No schema meaning changes, fully additive
- ⚠️ **Phase-6 Scope Expansion:** Adds ~15-20 tasks across Track D0 and Track D
- ⚠️ **Timeline Impact:** May extend Track D0 by 1-2 weeks, Track D by 1 week
- ✅ **Critical for Completeness:** Without this, estimation system is incomplete

---

## 1. What Changes Are Needed in Phase-6 Planning

### 1.1 Track D0 - Costing Engine Foundations (Weeks 3-6)

**Current State:** Track D0 focuses on BOM costing only (EffectiveQty, CostHead mapping, QCD generator).

**Required Changes:**

#### NEW: Cost Category Master Seeding (Week 3)
- [ ] **P6-COST-D0-008:** Seed generic cost categories
  - MATERIAL (already exists via BOM)
  - BUSBAR
  - FABRICATION
  - LABOUR
  - TRANSPORTATION
  - ERECTION
  - COMMISSIONING
  - MISC
  - **File:** `docs/PHASE_6/COSTING/COST_CATEGORY_SEED.md`
  - **Dependency:** Must complete before cost templates

#### NEW: Cost Template Master Tables (Week 4)
- [ ] **P6-COST-D0-009:** Create cost template master tables
  - `cost_templates` table (one per cost category)
  - `cost_template_lines` table (rows per template)
  - Migration script
  - **File:** `docs/PHASE_6/COSTING/COST_TEMPLATE_SCHEMA.md`
  - **Dependency:** After cost categories seeded

#### NEW: Cost Sheet Runtime Tables (Week 4)
- [ ] **P6-COST-D0-010:** Create cost sheet instance tables
  - `quote_cost_sheets` table (one per panel per cost category)
  - `quote_cost_sheet_lines` table (instantiated template lines)
  - Migration script
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_SCHEMA.md`
  - **Dependency:** After template tables

#### NEW: Cost Sheet Calculation Engine (Week 5)
- [ ] **P6-COST-D0-011:** Implement cost sheet calculation logic
  - Row-level calculation (qty × rate, lump sum, etc.)
  - Sheet total calculation
  - Validation (no negative values, locked rows)
  - **File:** `docs/PHASE_6/COSTING/COST_SHEET_CALCULATION.md`
  - **Dependency:** After runtime tables

#### UPDATE: QCD Generator to Include Cost Adders (Week 5)
- [ ] **P6-COST-D0-012:** Extend QCD generator to include cost adders
  - QCD_BOM = existing BOM-derived rows
  - QCD_ADDERS = pseudo rows from quote_cost_sheet_lines
  - QCD_ALL = union for pivots
  - **File:** `docs/PHASE_6/COSTING/QCD_ADDERS_INTEGRATION.md`
  - **Dependency:** After cost sheet calculation engine
  - **Impact:** This is a **critical change** - QCD contract must be updated

#### UPDATE: D0 Gate Checklist (Week 6)
- [ ] **P6-COST-D0-013:** Update D0 Gate to include cost adders
  - Cost adders included in QCD
  - Cost adders included in totals
  - Performance acceptable with cost adders
  - **File:** `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md` (update)

**Track D0 Impact:**
- **New Tasks:** 6 tasks
- **Updated Tasks:** 2 tasks (QCD generator, D0 Gate)
- **Timeline Extension:** +1 week (Week 7 becomes part of D0)

---

### 1.2 Track D - Costing & Reporting (Weeks 7-10)

**Current State:** Track D focuses on Costing Pack UI consuming QCD only.

**Required Changes:**

#### NEW: Panel UI - Cost Adders Section (Week 7)
- [ ] **P6-COST-019:** Add Cost Adders section to Panel Detail page
  - Display existing cost adders (FAB/BUS/LAB/etc.)
  - Status indicators (Draft/Approved/Locked)
  - Total amount per cost adder
  - "Add Cost Adder" button
  - **File:** `docs/PHASE_6/UI/PANEL_COST_ADDERS_DESIGN.md`
  - **Dependency:** Track A Panel UI must be complete (Week 2)

#### NEW: Cost Sheet Editor UI (Week 7-8)
- [ ] **P6-COST-020:** Implement cost sheet editor
  - Create route: `/quotation/{id}/panel/{panelId}/cost-sheet/{sheetId}`
  - Table view with editable qty/rate
  - Auto-calculate amount per row
  - Total at bottom
  - Save/Approve/Lock buttons
  - **File:** `docs/PHASE_6/UI/COST_SHEET_EDITOR_DESIGN.md`
  - **Dependency:** After cost sheet calculation engine

#### UPDATE: Costing Pack Snapshot (Week 7)
- [ ] **P6-COST-003-UPDATE:** Include cost adders in snapshot
  - Total BOM cost (from QCD_BOM)
  - Total Cost Adders (from QCD_ADDERS)
  - Combined total
  - **Impact:** Minor update to existing task

#### UPDATE: Panel Summary View (Week 7)
- [ ] **P6-COST-004-UPDATE:** Include cost adders in panel summary
  - Panel BOM cost
  - Panel Cost Adders breakdown (by category)
  - Panel Total Cost
  - **Impact:** Minor update to existing task

#### UPDATE: CostHead Pivot (Week 8)
- [ ] **P6-COST-006-UPDATE:** Include cost adders in CostHead pivot
  - MATERIAL → drill by Make (existing)
  - BUSBAR → drill by sheet lines (new)
  - FABRICATION → drill by sheet lines (new)
  - LABOUR → drill by sheet lines (new)
  - TRANSPORTATION / ERECTION / COMMISSIONING (new)
  - **Impact:** Moderate update to existing task

#### UPDATE: Excel Export (Week 10)
- [ ] **P6-COST-015-UPDATE:** Include cost adders in Excel export
  - Sheet 1: Panel summary (BOM + Adders)
  - Sheet 2: Detailed BOM (QCD_BOM)
  - Sheet 3: Cost Adders detail (QCD_ADDERS)
  - Sheet 4: Pivot shells
  - **Impact:** Moderate update to existing task

**Track D Impact:**
- **New Tasks:** 2 tasks (Panel UI, Cost Sheet Editor)
- **Updated Tasks:** 4 tasks (Snapshot, Panel Summary, CostHead Pivot, Excel Export)
- **Timeline Extension:** +1 week (Week 11 becomes part of Track D)

---

### 1.3 Track A - Panel UI (Weeks 1-6)

**Required Changes:**

#### UPDATE: Panel Details Page (Week 2)
- [ ] **P6-UI-004-UPDATE:** Add Cost Adders section to panel details
  - Display cost adders list
  - "Add Cost Adder" button
  - Navigation to cost sheet editor
  - **Impact:** Minor update to existing task
  - **Dependency:** Must coordinate with Track D0 for data model

**Track A Impact:**
- **Updated Tasks:** 1 task
- **Timeline Impact:** None (parallel work)

---

### 1.4 Track E - Canon Implementation (Weeks 0-6)

**Required Changes:**

#### NEW: Cost Template Seed Data (Week 1-2)
- [ ] **P6-DB-005:** Seed cost template master data
  - Fabrication template (standard lines)
  - Busbar template (standard lines)
  - Labour template (standard lines)
  - Transportation template
  - Erection template
  - Commissioning template
  - **File:** `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`
  - **Dependency:** After cost_templates table created

**Track E Impact:**
- **New Tasks:** 1 task
- **Timeline Impact:** None (parallel work)

---

## 2. Roadblocks & Issues

### 2.1 Critical Roadblocks (Must Resolve Before Execution)

#### 🔴 ROADBLOCK #1: QCD Contract Change
**Issue:** QCD v1.0 contract (defined in Track D0) must be updated to include cost adders.

**Impact:**
- QCD schema must support both BOM items and cost adders
- All consumers of QCD must handle both types
- Excel export must handle both types
- Dashboard aggregations must handle both types

**Resolution:**
- Update QCD contract to v1.1 (additive only, backward compatible)
- Document QCD_ADDERS structure
- Update all QCD consumers

**Timeline Impact:** +2 days for contract update + testing

**Can Be Managed:** ✅ Yes, but requires careful versioning

---

#### 🔴 ROADBLOCK #2: Cost Category Seed Data
**Issue:** Cost categories (BUSBAR, FABRICATION, etc.) must exist before templates can be created.

**Impact:**
- Templates reference cost_head_id
- Cannot create templates without cost categories
- Seed data must be tenant-scoped

**Resolution:**
- Seed cost categories in Track E (Week 1-2)
- Ensure tenant_id is properly set
- Verify cost categories exist before template creation

**Timeline Impact:** None (parallel work)

**Can Be Managed:** ✅ Yes, straightforward

---

#### 🔴 ROADBLOCK #3: Panel UI Dependency
**Issue:** Cost Adders UI requires Panel Detail page to be complete (Track A, Week 2).

**Impact:**
- Cannot implement Cost Adders UI until Panel UI exists
- Must coordinate between Track A and Track D

**Resolution:**
- Track A completes Panel UI in Week 2
- Track D starts Cost Adders UI in Week 7 (after D0 Gate)
- No blocking dependency

**Timeline Impact:** None (sequential dependency already planned)

**Can Be Managed:** ✅ Yes, dependency is clear

---

### 2.2 Moderate Roadblocks (Can Be Managed with Planning)

#### ⚠️ ROADBLOCK #4: Template Line Structure
**Issue:** Template line structure (calc_mode, default values) must be finalized before implementation.

**Impact:**
- Templates must support: LUMP_SUM, QTY_RATE, KG_RATE, METER_RATE, HOUR_RATE, PERCENT_OF_BASE
- Default values must be defined
- Formula rules must be clear

**Resolution:**
- Finalize template line structure in Week 3 (before implementation)
- Document calc_mode enum
- Create template examples

**Timeline Impact:** None (design work)

**Can Be Managed:** ✅ Yes, requires design decision

**Required Input:** Template line structure confirmation

---

#### ⚠️ ROADBLOCK #5: Cost Sheet Approval Workflow
**Issue:** Cost sheets need approval/locking workflow, but Track C (Operational Readiness) starts in Week 7.

**Impact:**
- Cost sheets have status (DRAFT/APPROVED/LOCKED)
- Approval workflow may not be ready
- Locking may conflict with line-item locking (D-005)

**Resolution:**
- Use simple status field (no complex workflow in Phase-6)
- Locking at sheet level (not line-item level)
- Full approval workflow deferred to Phase-7

**Timeline Impact:** None (simplified approach)

**Can Be Managed:** ✅ Yes, simplified approach acceptable

**Required Input:** Approval workflow scope confirmation

---

#### ⚠️ ROADBLOCK #6: Performance with Cost Adders
**Issue:** QCD generation performance must remain acceptable when cost adders are included.

**Impact:**
- QCD generation time may increase
- Dashboard aggregations may slow down
- Excel export may be slower

**Resolution:**
- Include cost adders in performance testing (Track D0, Week 6)
- Optimize queries if needed
- Set performance targets: < 5 seconds for typical quotation

**Timeline Impact:** +1 day for performance testing

**Can Be Managed:** ✅ Yes, performance testing already planned

---

### 2.3 Low-Priority Issues (Can Be Deferred)

#### ℹ️ ISSUE #7: Feeder-Level Cost Adders
**Issue:** Cost adders are panel-level only in Phase-6, but feeder-level may be needed later.

**Impact:**
- Current design supports panel-level only
- Feeder-level requires schema change (quote_bom_id FK)

**Resolution:**
- Defer feeder-level to Phase-7
- Schema supports it (nullable quote_bom_id FK)
- No blocking issue

**Timeline Impact:** None (deferred)

**Can Be Managed:** ✅ Yes, deferred to Phase-7

---

#### ℹ️ ISSUE #8: Template Versioning
**Issue:** Templates may need versioning for historical tracking.

**Impact:**
- Current design has version field but no versioning logic
- Historical cost sheets may reference old template versions

**Resolution:**
- Defer versioning logic to Phase-7
- Store template_id in cost sheet (snapshot approach)
- No blocking issue

**Timeline Impact:** None (deferred)

**Can Be Managed:** ✅ Yes, deferred to Phase-7

---

## 3. What Can Be Managed vs. What Cannot

### 3.1 ✅ Can Be Managed (With Planning)

| Item | Management Strategy | Timeline Impact |
|------|-------------------|-----------------|
| **QCD Contract Update** | Version to v1.1 (additive), update consumers | +2 days |
| **Cost Category Seeding** | Seed in Track E (Week 1-2), parallel work | None |
| **Template Structure** | Finalize in Week 3, document examples | None |
| **Panel UI Dependency** | Sequential dependency already planned | None |
| **Performance Testing** | Include in D0 Gate, optimize if needed | +1 day |
| **Approval Workflow** | Simplified approach (status field only) | None |
| **Excel Export Update** | Add new sheet for cost adders | +1 day |

**Total Manageable Timeline Impact:** +4 days (~1 week buffer)

---

### 3.2 ❌ Cannot Be Managed (Must Accept or Defer)

| Item | Why Cannot Be Managed | Recommendation |
|------|----------------------|----------------|
| **Schema Changes** | Phase-5 freeze prevents schema meaning changes | ✅ Acceptable - new tables are additive |
| **QCD Contract Change** | Required for cost adders integration | ✅ Acceptable - v1.1 is additive, backward compatible |
| **Timeline Extension** | Additional work requires time | ✅ Acceptable - +1-2 weeks is reasonable |
| **Template Design Decision** | Must finalize before implementation | ⚠️ **REQUIRES INPUT** - See Section 4 |

---

## 4. Points Requiring Further Input

### 4.1 🔴 CRITICAL: Template Line Structure

**Question:** What is the exact structure of template lines?

**Required Details:**
1. **Calc Modes:** Confirm all calc modes needed:
   - ✅ LUMP_SUM
   - ✅ QTY × RATE
   - ✅ KG × RATE
   - ✅ METER × RATE
   - ✅ HOUR × RATE
   - ❓ PERCENT_OF_BASE (for commissioning/contingency) - **NEED CONFIRMATION**

2. **Default Values:** Should templates have default qty/rate values?
   - ❓ Default qty per line?
   - ❓ Default rate per line?
   - ❓ Or always require user input?

3. **Formula Rules:** Any complex formulas needed?
   - ❓ Simple qty × rate only?
   - ❓ Or formulas like "base_cost × 1.1" (10% markup)?

**Decision Needed:** Template line structure must be finalized in Week 3 (before implementation).

**Impact if Delayed:** Blocks P6-COST-D0-009 (template tables) and P6-COST-D0-011 (calculation engine).

---

### 4.2 🔴 CRITICAL: Cost Category → CostHead Mapping

**Question:** How do cost adders map to CostHead system?

**Required Details:**
1. **Mapping Rule:** Each cost adder type maps to one CostHead:
   - Fabrication → FABRICATION cost_head
   - Busbar → BUSBAR cost_head
   - Labour → LABOUR cost_head
   - Transportation → TRANSPORTATION cost_head
   - Erection → ERECTION cost_head
   - Commissioning → COMMISSIONING cost_head
   - ✅ **CONFIRMED** - This mapping is correct

2. **CostBucket Mapping:** What CostBucket for each?
   - MATERIAL → MATERIAL bucket ✅
   - BUSBAR → MATERIAL or OTHER? ❓
   - FABRICATION → MATERIAL or OTHER? ❓
   - LABOUR → LABOUR bucket ✅
   - TRANSPORTATION → OTHER bucket ✅
   - ERECTION → LABOUR or OTHER? ❓
   - COMMISSIONING → OTHER bucket ✅

**Decision Needed:** CostBucket mapping must be finalized in Week 3.

**Impact if Delayed:** Blocks cost category seeding and template creation.

---

### 4.3 ⚠️ MODERATE: Template Seed Data Content

**Question:** What are the standard template lines for each cost adder type?

**Required Details:**
1. **Fabrication Template:** What are the standard lines?
   - ❓ Panel fabrication base
   - ❓ Powder coating
   - ❓ Wiring labour
   - ❓ Other standard lines?

2. **Busbar Template:** What are the standard lines?
   - ❓ Busbar copper (kg × rate)
   - ❓ Busbar aluminium (kg × rate)
   - ❓ Busbar cutting/fabrication (hours × rate)
   - ❓ Other standard lines?

3. **Labour Template:** What are the standard lines?
   - ❓ Wiring labour (hours × rate)
   - ❓ Assembly labour (hours × rate)
   - ❓ Testing labour (hours × rate)
   - ❓ Other standard lines?

**Decision Needed:** Template seed data can be finalized in Week 4-5 (after template structure).

**Impact if Delayed:** Blocks P6-DB-005 (template seed data), but can use minimal templates initially.

**Recommendation:** Start with minimal templates (1-2 lines each), expand later.

---

### 4.4 ⚠️ MODERATE: Approval Workflow Scope

**Question:** What approval workflow is needed for cost sheets in Phase-6?

**Required Details:**
1. **Status Field:** Simple status (DRAFT/APPROVED/LOCKED) sufficient?
   - ✅ **ASSUMED YES** - Simple approach for Phase-6

2. **Approval Process:** Manual approval or automated?
   - ❓ Manual "Approve" button sufficient?
   - ❓ Or need approval queue (Track C integration)?

3. **Locking Behavior:** How does locking work?
   - ❓ Lock entire sheet (all lines)?
   - ❓ Or lock individual lines (like BOM items)?

**Decision Needed:** Approval workflow scope must be finalized in Week 3.

**Impact if Delayed:** Blocks P6-COST-020 (cost sheet editor UI).

**Recommendation:** Use simple status field (DRAFT/APPROVED/LOCKED) with manual approval button. Full workflow deferred to Phase-7.

---

### 4.5 ℹ️ LOW-PRIORITY: Panel Qty Impact on Cost Adders

**Question:** Do cost adders automatically multiply by PanelQty?

**Required Details:**
1. **Multiplication Rule:** If PanelQty=2, should fabrication cost double?
   - ❓ Yes, automatically multiply by PanelQty
   - ❓ No, cost adders are already total (not per-panel)

2. **Per-Panel vs. Total:** Are cost adders per-panel or total?
   - ❓ Per-panel (multiply by PanelQty)
   - ❓ Total (already includes PanelQty)

**Decision Needed:** Can be finalized in Week 5 (during calculation engine implementation).

**Impact if Delayed:** None (calculation logic can be adjusted).

**Recommendation:** Start with per-panel (multiply by PanelQty), allow override if needed.

---

## 5. Recommended Action Plan

### 5.1 Immediate Actions (Before Phase-6 Starts)

1. **Finalize Template Line Structure** (Week 0)
   - Confirm calc modes
   - Confirm default value approach
   - Document template line structure

2. **Finalize Cost Category Mapping** (Week 0)
   - Confirm CostBucket mapping
   - Seed cost categories in Track E

3. **Update Phase-6 Execution Plan** (Week 0)
   - Add new tasks to Track D0
   - Add new tasks to Track D
   - Update dependencies
   - Update timeline (add 1-2 weeks buffer)

### 5.2 During Phase-6 Execution

1. **Week 3:** Finalize template structure, seed cost categories
2. **Week 4:** Create template and cost sheet tables, implement calculation engine
3. **Week 5:** Extend QCD generator, update D0 Gate
4. **Week 7:** Implement Panel UI, Cost Sheet Editor
5. **Week 8:** Update Costing Pack to include cost adders
6. **Week 10:** Update Excel export

### 5.3 Risk Mitigation

1. **Template Seed Data:** Start with minimal templates, expand later
2. **Performance:** Include cost adders in performance testing
3. **Approval Workflow:** Use simple approach, defer complex workflow to Phase-7
4. **Timeline:** Add 1-2 weeks buffer for unexpected issues

---

## 6. Summary Table

| Category | Count | Status |
|----------|-------|--------|
| **New Tasks Required** | 9 tasks | ⏳ Pending |
| **Updated Tasks Required** | 7 tasks | ⏳ Pending |
| **Critical Roadblocks** | 3 | ⚠️ Require Resolution |
| **Moderate Roadblocks** | 3 | ✅ Can Be Managed |
| **Low-Priority Issues** | 2 | ✅ Deferred |
| **Required Inputs** | 5 questions | ⚠️ Need Answers |
| **Timeline Impact** | +1-2 weeks | ⚠️ Acceptable |

---

## 7. Next Steps

### 7.1 Before Phase-6 Execution

1. ✅ **Review this analysis document**
2. ⚠️ **Answer critical questions** (Section 4.1, 4.2)
3. ⚠️ **Finalize template structure** (Section 4.1)
4. ✅ **Update Phase-6 Execution Plan** with new tasks
5. ✅ **Update timeline** (add 1-2 weeks buffer)

### 7.2 During Phase-6 Execution

1. **Week 0:** Finalize all design decisions
2. **Week 3:** Implement cost categories and templates
3. **Week 4-5:** Implement cost sheets and QCD integration
4. **Week 7-8:** Implement UI and Costing Pack updates
5. **Week 10:** Complete Excel export updates

---

**Document Status:** ✅ ANALYSIS COMPLETE  
**Next Action:** Review and answer critical questions (Section 4)  
**Owner:** Product + Engineering  
**Last Updated:** 2025-01-27

