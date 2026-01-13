# Phase-6 Execution Plan - Corrected Version Summary

**Version:** 1.2 (Corrected)  
**Date:** 2025-01-27  
**Status:** READY FOR APPROVAL  
**Based On:** User's Corrected Plan + Phase-5 Canonical Working Record

---

## 🎯 Key Corrections Made

This summary highlights the key corrections applied to align with the user's corrected plan structure.

---

## ✅ Major Structural Changes

### 1. Track D0: Costing Engine Foundations (NEW)
**Weeks 3-6, 7 tasks**

**Purpose:** Build canonical costing engine (QCD) before UI/reporting

**Key Features:**
- EffectiveQty engine (BaseQty → EffQtyPerPanel → EffQtyTotal)
- CostHead mapping precedence (D-006)
- QuotationCostDetail (QCD) canonical dataset
- QCD JSON export endpoint
- Numeric validation vs reference Excel (engine-first)
- Performance hardening for large quotations
- **D0 Gate signoff** (QCD v1.0 stable)

**Rationale:** Separates costing engine implementation from UI/reporting. Ensures engine is stable before building dashboards.

---

### 2. Track E: Canon Implementation & Contract Enforcement (REORGANIZED)
**Weeks 0-6, ~28 tasks**

**Purpose:** Implement all Phase-5 frozen items in one cohesive track

**Consolidates:**
- Database implementation (Weeks 0-1)
- Guardrails runtime enforcement (Weeks 2-4)
- API contracts implementation OR defer (Weeks 3-6)
- Multi-SKU linkage (D-007) (Weeks 3-6)
- Discount Editor (Weeks 3-6)
- BOM tracking fields runtime behavior (Weeks 2-4)
- Customer snapshot handling (Week 1)
- Resolution constraints enforcement (Week 4)

**Rationale:** All Phase-5 implementation obligations grouped together for better coordination and compliance tracking.

---

### 3. Track D: Costing & Reporting (MODIFIED)
**Weeks 7-10, 18 tasks**

**Key Change:** **Consumes QCD only (no duplicate calculators)**

**Before:** Referenced "CostingService" integration  
**After:** All costing displays use QCD aggregates from Track D0

**Impact:**
- P6-COST-002: Changed from "Review CostingService" to "Confirm D0 Gate passed"
- P6-COST-003/004: Data source explicitly QCD aggregates
- P6-COST-005: Derived via QCD + tree
- P6-COST-015: Engine-first Excel export (Sheet 1: Panel summary, Sheet 2: QCD, Sheet 3: Pivot shells)
- P6-COST-017: Integration with QCD generator (not separate CostingService)

**Rationale:** Single source of truth (QCD) prevents calculation discrepancies and ensures consistency.

---

## 📋 New Tasks Added

### Week 0 Setup (NEW)
- **P6-SETUP-004:** Create Costing manual structure
- **P6-SETUP-005:** Freeze Costing Engine Contract (QCD v1.0)
- **P6-SETUP-006:** Define D0 Gate checklist (QCD readiness)

### Week 1 (NEW)
- **P6-UI-001A:** Ensure customer_name_snapshot always stored (D-009)
- **P6-UI-001B:** customer_id remains nullable (D-009)

### Week 2 (NEW)
- **P6-UI-010A:** Verify raw quantity persistence (PanelQty, FeederQty, BomQty, ItemQtyPerBom)

### Track D0 (ALL NEW)
- **P6-COST-D0-001:** Implement EffectiveQty logic
- **P6-COST-D0-002:** Implement CostHead mapping precedence (D-006)
- **P6-COST-D0-003:** Implement QCD generator + JSON endpoint
- **P6-COST-D0-004:** QCD Excel export (sheet-1 only)
- **P6-COST-D0-005:** Numeric validation vs Excel reference
- **P6-COST-D0-006:** Performance hardening for large quotations
- **P6-COST-D0-007:** D0 Gate signoff (QCD v1.0 stable)

### Track C (NEW)
- **P6-OPS-012:** Costing Pack/dashboard/export permissions + bulk discount approval hook

### Integration (NEW)
- **P6-INT-006A:** Validate QCD parity inside UI flows

### Closure (NEW)
- **P6-CLOSE-005:** Canon compliance signoff

---

## 🔄 Tasks Moved/Reorganized

### Moved to Track E (Canon Implementation)

**From Track A:**
- Runtime guardrails enforcement (P6-VAL-001..004) → Track E Weeks 2-4
- BOM tracking fields (P6-BOM-TRACK-001..003) → Track E Weeks 2-4
- Multi-SKU linkage (P6-SKU-001..003) → Track E Weeks 3-6
- Discount Editor (P6-DISC-001..004) → Track E Weeks 3-6
- Customer snapshot (P6-QUO-001A/B) → Track E Week 1
- Resolution constraints (P6-RES-023/024) → Track E Week 4

**From Separate Tracks:**
- Database implementation (P6-DB-001..004) → Track E Weeks 0-1
- API contracts (P6-API-001..006) → Track E Weeks 3-6

**Rationale:** All Phase-5 implementation obligations in one track for better coordination.

---

## ✏️ Tasks Modified

### Track D Costing Tasks (Modified to use QCD)

- **P6-COST-002:** Changed from "Review CostingService" to "Confirm D0 Gate passed"
- **P6-COST-003:** Data source changed to "QCD aggregates"
- **P6-COST-004:** Data source changed to "QCD aggregates"
- **P6-COST-005:** Changed to "Derived via QCD + tree"
- **P6-COST-007:** Added requirement "Must include CostHead pivot + Category/Make/RateSource"
- **P6-COST-010/011/012:** Added note "All dashboard aggregations come from QCD across quotations"
- **P6-COST-015:** Changed to "Engine-first Excel export" with specific sheet structure
- **P6-COST-017:** Changed to "Integration with QCD generator (not separate CostingService)"

---

## 🚫 Tasks Removed/Consolidated

### Removed from Track A (Moved to Track E)
- All guardrails enforcement tasks (now in Track E)
- All BOM tracking tasks (now in Track E)
- All multi-SKU tasks (now in Track E)
- All discount editor tasks (now in Track E)
- Customer snapshot tasks (now in Track E)
- Resolution constraint tasks (now in Track E)

**Rationale:** Track A focuses on UI only. Track E handles all Phase-5 implementation obligations.

---

## 📊 Updated Statistics

### Track Count
- **Before:** 6 tracks (A, B, C, D, E, F)
- **After:** 6 tracks (A, B, C, D0, D, E)
- **Change:** Track F (API) merged into Track E, Track D0 added

### Task Distribution
- **Track A:** 33 tasks (reduced from 45, moved implementation tasks to Track E)
- **Track B:** 16 tasks (unchanged)
- **Track C:** 12 tasks (11 + 1 new)
- **Track D0:** 7 tasks (NEW)
- **Track D:** 18 tasks (modified to use QCD)
- **Track E:** ~28 tasks (consolidated from multiple sources)
- **Integration:** 11 tasks (10 + 1 new)
- **Closure:** 5 tasks (4 + 1 new)

### Duration
- **Before:** 12-13 weeks
- **After:** 10-12 weeks
- **Rationale:** Better parallelization with Track D0 and Track E reorganization

---

## 🔒 New Gates & Signoffs

### D0 Gate (NEW)
**Purpose:** Ensure QCD v1.0 is stable before building costing UI/reporting

**Checklist:**
- QCD generator functional
- QCD JSON endpoint working
- Numeric validation passing
- Performance acceptable for large quotations

**Location:** Week 6, P6-COST-D0-007

**Blocks:** Track D (Costing & Reporting) cannot proceed until D0 Gate passed

---

### Canon Compliance Signoff (NEW)
**Purpose:** Verify all Phase-5 frozen items are implemented correctly

**Checklist:**
- Schema parity (Canon v1.0)
- Guardrails runtime parity (G1–G8)
- API parity (or defer memo exists)
- Locking scope respected (D-005)
- CostHead precedence respected (D-006)
- Multi-SKU linkage present (D-007)
- Discount Editor delivered (legacy parity)
- Customer snapshot handling (D-009)
- Resolution constraints enforced (A10)

**Location:** Week 12, P6-CLOSE-005

**Blocks:** Phase-6 closure

---

## 📝 Key Principles Applied

### 1. Engine-First Approach
- QCD is the canonical dataset
- Excel is a consumer, not driver
- All costing displays use QCD aggregates
- No duplicate calculators

### 2. Single Source of Truth
- QCD for all costing calculations
- Schema Canon for database structure
- Phase-5 frozen contracts for API/validation

### 3. Gate-Based Progression
- D0 Gate before Track D
- Schema parity gate before UI work
- Canon compliance signoff before closure

### 4. Implementation Obligations Grouped
- All Phase-5 implementation in Track E
- Better coordination and compliance tracking
- Clear separation: UI (Track A) vs Implementation (Track E)

---

## ✅ Alignment with Corrected Plan

### Matches User's Corrected Plan:
- ✅ Track D0 added (Costing Engine Foundations)
- ✅ Track E reorganized (Canon Implementation)
- ✅ QCD emphasis throughout
- ✅ D0 Gate signoff
- ✅ Costing manual structure
- ✅ Raw quantity persistence verification
- ✅ Canon compliance signoff
- ✅ Engine-first Excel export
- ✅ All costing tasks modified to use QCD
- ✅ All Phase-5 implementation tasks in Track E

### Additional Improvements:
- ✅ BOM tracking tasks explicitly in Track E
- ✅ Customer snapshot tasks explicitly in Track E
- ✅ Resolution constraint tasks explicitly in Track E
- ✅ Clear task numbering and organization
- ✅ Updated dependencies and parallel execution

---

## 🔗 Related Documents

- **Phase-6 Execution Plan v1.2 (Corrected):** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Phase-6 Revision Summary:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_REVISION_SUMMARY.md`
- **Phase-5 Detailed Working Record:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DETAILED_WORKING_RECORD.md`

---

**Last Updated:** 2025-01-27  
**Status:** CORRECTED - Ready for Review  
**Next Action:** Review corrected plan and approve or request further changes

