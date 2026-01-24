# Phase 6 New System Scope
## Complete Scope Definition for NSW Estimation Software

**Version:** 1.4 (Cost Adders Integrated)  
**Date:** 2025-01-27  
**Status:** ACTIVE  
**Purpose:** Define the complete scope of Phase 6 - what is being built in the new NSW system

---

## 🎯 Executive Summary

**Phase-6: Productisation & Controlled Expansion**

Phase-6 converts a **correct system** (Phase-5) into a **usable product** with complete costing and reporting capabilities, while preserving all legacy capabilities through reuse workflows.

**Total Duration:** 10-12 weeks  
**Total Tracks:** 7 parallel tracks (A, A-R, B, C, D0, D, E)  
**Total Tasks:** ~133 tasks  
**Exit Artifact:** NSW v0.6 – Internal Product Ready

---

## 📊 Complete Scope by Track

### Track A: Productisation (6 weeks, 33 tasks)

**Purpose:** Build complete quotation creation and management UI

**Scope:**
- Quotation overview and panel management
- BOM hierarchy tree view (Panel → Feeder → BOM L1 → BOM L2 → Components)
- Pricing resolution UX (PRICELIST / MANUAL / FIXED)
- L0 → L1 → L2 resolution flow
- Locking behaviour visibility
- Error & warning surfacing
- Customer snapshot handling (D-009)

**Key Deliverables:**
- Quotation overview page
- Panel details page
- BOM hierarchy tree view
- Item selection and resolution UI
- Pricing resolution UI
- Error/warning display

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md` (Track A)

---

### Track A-R: Reuse & Legacy Parity (3 weeks, 7 tasks) ⭐ NEW

**Purpose:** Preserve all legacy capabilities through reuse workflows

**Scope:**
- Quotation reuse (copy old quotation → modify)
- Panel reuse (copy panel subtree)
- Feeder reuse (copy Level-0 BOM + subtree)
- BOM reuse (copy BOM from past quotation)
- Master BOM template application
- Post-reuse editability verification
- Guardrail enforcement after reuse

**Key Deliverables:**
- Quotation copy functionality
- Panel copy functionality
- Feeder copy functionality
- BOM copy functionality
- Master BOM application UI
- Legacy parity verification

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_LEGACY_PARITY_ADDITION.md`

---

### Track B: Catalog Tooling (4 weeks, 16 tasks)

**Purpose:** Enable safe catalog import and governance

**Scope:**
- Catalog import UI with file upload
- Series-wise catalog onboarding
- Pre-import validation previews
- Catalog governance enforcement and approval workflows

**Key Deliverables:**
- Catalog import UI
- Validation preview system
- Catalog governance workflows
- Series-wise onboarding process

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md` (Track B)

---

### Track C: Operational Readiness (2 weeks, 12 tasks)

**Purpose:** Enable role-based access and approval workflows

**Scope:**
- Basic role-based access control
- Approval flows (price changes, overrides)
- Audit visibility (read-only)
- Initial SOPs
- Costing Pack/dashboard/export permissions

**Key Deliverables:**
- RBAC system implementation
- Approval workflow UI
- Audit log viewer
- Permission management

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md` (Track C)

---

### Track D0: Costing Engine Foundations (4 weeks, 14 tasks) ⭐ NEW

**Purpose:** Build canonical costing engine (QCD + QCA) before UI/reporting

**Scope:**
- Effective quantity engine (BaseQty → EffQtyPerPanel → EffQtyTotal)
- CostHead mapping precedence (D-006)
- QuotationCostDetail (QCD) canonical dataset (BOM-only, stable contract)
- Cost Adders engine (cost templates, cost sheets, QCA dataset) ⭐ NEW
- QCD + QCA JSON export endpoints
- Numeric validation vs reference Excel (engine-first)
- Performance hardening for large quotations (with cost adders)
- D0 Gate signoff (QCD v1.0 stable + QCA v1.0 stable)

**Key Deliverables:**
- QCD generator (canonical dataset)
- QCA generator (cost adders dataset)
- Effective quantity calculator
- CostHead resolution engine
- JSON export endpoints
- Performance optimization

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COST_ADDERS_FINAL_SPEC.md`

---

### Track D: Costing & Reporting (4 weeks, 20 tasks) ⭐ MODIFIED

**Purpose:** Replace manual Excel costing with automated costing engine and dashboards

**Scope:**
- Costing Pack per quotation (snapshot, panel summary, pivots)
- Cost Adders UI (panel section, cost sheet editor) ⭐ NEW
- Global dashboard (margins, hit rates, cost drivers)
- CostHead system UI
- Excel export functionality (includes cost adders)
- **Consumes QCD + QCA (no duplicate calculators)** ✏️

**Key Deliverables:**
- Costing Pack UI
- Cost Adders editor
- Global dashboard
- Excel export with cost adders
- CostHead management UI

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md` (Track D)

---

### Track E: Canon Implementation & Contract Enforcement (6 weeks, ~29 tasks) ⭐ NEW

**Purpose:** Implement all Phase-5 frozen items

**Scope:**
- DB creation/migrations from Schema Canon v1.0 + seed execution
- Cost template seed data (Cost Adders) ⭐ NEW
- Guardrails G1-G8 runtime enforcement + tests
- API contract implementation (B1-B4) OR explicit defer decision
- Multi-SKU linkage (D-007) implementation
- Discount Editor (legacy parity)
- BOM tracking fields runtime behavior
- Customer snapshot handling (D-009)
- Resolution constraints enforcement (A10)

**Key Deliverables:**
- Database migrations from Schema Canon
- Guardrail enforcement
- API contracts
- Multi-SKU linkage
- Discount Editor
- BOM tracking

**Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md` (Track E)

---

## 🔒 Phase 6 Rule (Locked)

**"Phase-6 may add features, but may not change meaning."**

**Extended Rule:**
- ✅ Can add: UI layers, tooling, workflows, derived datasets (QCD, QCA), dashboards, exports
- ✅ Can add: Reuse workflows (quotation, panel, feeder, BOM copy)
- ✅ Can add: Legacy parity features (contacts, project navigation, catalog views)
- ❌ Cannot change: Schema semantics, guardrails, locked decisions (D-005/006/007/009), resolution constraints, API contract meaning

**Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md` (Section 8)

---

## 📋 Locked Invariants (Non-Negotiable)

### Invariant 1: Schema Canon is Frozen
- Phase 5 Schema Canon v1.0 is frozen
- Cannot change existing table structures
- Can add new tables/columns with approval

### Invariant 2: Guardrails Must Be Enforced
- G-01 to G-08 must be implemented
- Guardrail violations must be prevented
- Cannot bypass guardrails

### Invariant 3: Locked Decisions Are Immutable
- D-005, D-006, D-007, D-009 cannot be changed
- Must implement as specified
- Must preserve decision intent

### Invariant 4: Function Preservation
- All NEPL functions must be preserved
- No function can be lost
- All capabilities must work in Phase 6

### Invariant 5: Copy-Never-Link Rule
- All reuse operations must copy, never link
- All copies are independent
- Never share mutable state

### Invariant 6: Calculation Formulas Are Frozen
- All calculation formulas are locked
- Must preserve exact formulas
- Cannot change calculation logic

### Invariant 7: Costing Contract is Permanent
- `AmountTotal = NetRate × TotalQty`
- Roll-ups = `SUM(AmountTotal)` only
- No extra multipliers at rollup levels

**Source:** `PHASE_6_NEPL_BASELINE_REVIEW.md` (Section: What Must Be Preserved)

---

## 🎯 Entry Criteria

**All must be true:**
- ✅ SPEC-5 v1.0 frozen
- ✅ Schema Canon locked
- ✅ Decision Register closed
- ✅ Freeze Gate Checklist 100% verified
- ✅ Core resolution engine tested

**Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md` (Section 4)

---

## ✅ Exit Criteria

Phase-6 is complete when:
- ✅ A quotation can be created end-to-end
- ✅ L1 selection reliably maps to L2 SKUs
- ✅ Pricing resolution works with overrides
- ✅ Catalog entries can be added safely
- ✅ Errors are explainable to users
- ✅ All legacy capabilities preserved (Track A-R)
- ✅ Costing engine stable (QCD + QCA v1.0)
- ✅ Costing Pack functional

**Exit Artifact:** NSW v0.6 – Internal Product Ready

**Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md` (Section 5)

---

## 📊 Timeline Overview

| Track | Duration | Start Week | End Week |
|-------|----------|------------|----------|
| Track E (Canon) | 6 weeks | Week 0 | Week 6 |
| Track A (UI) | 6 weeks | Week 1 | Week 6 |
| Track A-R (Reuse) | 3 weeks | Week 2 | Week 4 |
| Track B (Catalog) | 4 weeks | Week 3 | Week 6 |
| Track C (Ops) | 2 weeks | Week 7 | Week 8 |
| Track D0 (Costing Engine) | 4 weeks | Week 3 | Week 6 |
| Track D (Costing UI) | 4 weeks | Week 7 | Week 10 |
| Integration | 2 weeks | Week 9 | Week 10 |
| Closure | 2 weeks | Week 11 | Week 12 |

**Total:** 10-12 weeks

---

## 🔗 Related Documents

- **Complete Scope & Tasks:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COMPLETE_SCOPE_AND_TASKS.md`
- **Execution Plan:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Kickoff Charter:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md`
- **Legacy Parity:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_LEGACY_PARITY_ADDITION.md`
- **Cost Adders Spec:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COST_ADDERS_FINAL_SPEC.md`

---

**Status:** ACTIVE  
**Last Updated:** 2025-01-27  
**Next Review:** As scope changes
