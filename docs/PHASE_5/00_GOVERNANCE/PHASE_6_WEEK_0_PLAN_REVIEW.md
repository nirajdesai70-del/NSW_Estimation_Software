# Phase-6 Week-0 Plan Review & Confirmation

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ✅ CONFIRMED WITH NOTES  
**Reference:** Phase-6 Execution Plan v1.4 + Complete Scope v1.4

---

## ✅ Overall Assessment

**The Week-0 plan is APPROVED with minor clarifications.**

The plan provides a solid execution foundation that aligns with Phase-6 scope while establishing critical boundaries early. Some tasks are "skeleton/stub" implementations that enable parallel work, which is appropriate for Week-0.

---

## 📋 Day-by-Day Alignment Check

### Day 1 — Entry Gate & Guardrail Lock ✅ **ALIGNED**

**Your Plan:**
- Freeze Phase-5 artifacts (read-only markers)
- Create CANON_READ_ONLY.md
- Add schema snapshot (reference only)
- Define "feature-only" rule in repo README

**Execution Plan Mapping:**
- ✅ P6-ENTRY-001 to P6-ENTRY-006 (Entry Criteria Verification)
- ✅ P6-SETUP-001 (Phase-6 project structure)
- ✅ P6-SETUP-007 (Review Phase-5 deliverables for implementation obligations)

**Confirmation:** ✅ **FULLY ALIGNED**

**Recommendation:** Add explicit reference to Schema Canon v1.0 lock and Decision Register closure verification.

---

### Day 2 — Infrastructure Baseline ✅ **ALIGNED**

**Your Plan:**
- FastAPI app bootstrapped
- PostgreSQL schema loaded (Phase-5)
- Docker compose (API + DB only)
- Logging config (structured logs)
- GET /health returns OK
- App runs without Redis or paid tools

**Execution Plan Mapping:**
- ✅ Infrastructure Gate Checklist (from PHASE_6_INFRASTRUCTURE_AND_TOOLS.md)
- ⚠️ **Note:** Execution Plan doesn't explicitly call out FastAPI bootstrap, but Infrastructure Gate implies it

**Confirmation:** ✅ **ALIGNED** (Infrastructure Gate covers this)

**Recommendation:** 
- Ensure PostgreSQL schema is loaded from Schema Canon v1.0 (Track E, P6-DB-002)
- Verify Docker compose excludes Redis (per infrastructure clarifications)
- Confirm structured logging uses standard format (JSON recommended)

---

### Day 3 — Data Boundary Setup (QCD / QCA) ⚠️ **EARLY BUT ACCEPTABLE**

**Your Plan:**
- Lock QCD tables as BOM-only
- Create QCA summary table (panel × cost head)
- Add service-layer separation (no cross-writes)
- BOM cannot store cost adders
- QCA enforces one row per cost head per panel

**Execution Plan Mapping:**
- ⚠️ **Track D0:** QCD/QCA are Track D0 tasks (Weeks 3-6)
- ✅ **Track E:** Database schema creation (Week 0-1) includes all tables
- ✅ **Clarification:** Structural separation (table boundaries) is appropriate for Week 0

**Confirmation:** ✅ **ACCEPTABLE** (Structural boundaries only, not full implementation)

**Clarification Needed:**
- **QCD tables:** These are `quote_bom_items` and related BOM tables (already in Schema Canon)
- **QCA tables:** These are `quote_cost_adders` (from Cost Adders feature, Track D0)
- **Action:** Ensure `quote_cost_adders` table exists in schema (from Track D0, P6-COST-D0-010)
- **Service-layer separation:** Define interfaces/contracts only, not full implementation

**Recommendation:** 
- Day 3 should focus on **schema boundaries** and **service contracts**, not full QCD/QCA generators
- Full QCD/QCA implementation remains in Track D0 (Weeks 3-6)

---

### Day 4 — Reuse Engine Skeleton ⚠️ **EARLY BUT ACCEPTABLE**

**Your Plan:**
- APIs for: Copy quotation, Copy panel subtree, Copy feeder, Copy BOM
- Tracking fields auto-populated
- Copied entities are fully editable
- No foreign-key linkage to source objects

**Execution Plan Mapping:**
- ⚠️ **Track A-R:** Reuse workflows are Track A-R (Weeks 2-4)
- ✅ **Skeleton/Stub:** Creating API endpoints with basic copy logic is acceptable for Week 0

**Confirmation:** ✅ **ACCEPTABLE** (Skeleton implementation to enable parallel work)

**Clarification Needed:**
- **Skeleton scope:** Endpoints should exist with basic copy logic (deep copy, no links)
- **Full implementation:** Remains in Track A-R (P6-UI-REUSE-001 to P6-UI-REUSE-007)
- **BOM tracking fields:** `origin_master_bom_id`, `instance_sequence_no`, `is_modified` (from Schema Canon)

**Recommendation:**
- Day 4 should create **stub endpoints** with basic copy-never-link logic
- Full reuse workflows (UI, validation, guardrails) remain in Track A-R (Weeks 2-4)

---

### Day 5 — UI Skeleton (React) ✅ **ALIGNED**

**Your Plan:**
- Screens: Quotation list, Quotation detail, Panel tree, Feeder → BOM editor
- Wire to mock APIs if needed
- User can traverse full quotation → BOM path
- No costing logic yet, UI only

**Execution Plan Mapping:**
- ✅ **Track A Week 1:** Quotation & Panel UI (P6-UI-001 to P6-UI-005)
- ✅ **Skeleton/Stub:** Navigation and basic UI structure is appropriate for Week 0

**Confirmation:** ✅ **FULLY ALIGNED**

**Recommendation:**
- Day 5 should create **navigation structure** and **placeholder components**
- Full UI implementation remains in Track A (Weeks 1-6)
- Mock APIs are acceptable for Week 0

---

### Day 6 — Costing View Rules Enforcement ⚠️ **EARLY BUT ACCEPTABLE**

**Your Plan:**
- Quotation summary: One line per cost head only
- Fabrication: Appears as MATERIAL in quotation
- Internal breakup stored but hidden
- No UI path exposes fabrication breakup in quotation

**Execution Plan Mapping:**
- ⚠️ **Track D:** Costing Pack is Track D (Weeks 7-10)
- ✅ **Rules enforcement:** Defining rules early is appropriate for Week 0

**Confirmation:** ✅ **ACCEPTABLE** (Rules definition only, not full UI)

**Clarification Needed:**
- **Rules definition:** Document the costing view rules (commercial view vs cost sheet view)
- **Implementation:** Full Costing Pack UI remains in Track D (P6-COST-001 to P6-COST-018)
- **Fabrication special rule:** This aligns with Cost Adders feature (FABRICATION cost head → MATERIAL bucket in summary)

**Recommendation:**
- Day 6 should **document rules** and **add validation stubs** in service layer
- Full Costing Pack UI remains in Track D (Weeks 7-10)

---

### Day 7 — Week-0 Validation Gate ✅ **ALIGNED**

**Your Plan:**
- One sample quotation created end-to-end
- Reuse works (copy → edit)
- QCD/QCA separation validated
- No canon violations observed
- Gate Decision: ✅ Proceed to Week-1 execution

**Execution Plan Mapping:**
- ✅ Entry Gate completion (P6-ENTRY-001 to P6-ENTRY-006)
- ✅ Infrastructure Gate completion (from Infrastructure document)
- ✅ Schema parity gate (P6-DB-004) - if database is ready

**Confirmation:** ✅ **FULLY ALIGNED**

**Recommendation:**
- Day 7 should verify:
  - ✅ Canon protection enforced (Day 1)
  - ✅ Infrastructure ready (Day 2)
  - ✅ Data boundaries defined (Day 3)
  - ✅ Reuse skeleton functional (Day 4)
  - ✅ UI navigation works (Day 5)
  - ✅ Costing rules documented (Day 6)
  - ✅ Sample quotation created end-to-end (basic flow)

---

## 🔍 Key Observations

### ✅ Strengths

1. **Early Boundary Definition:** Establishing QCD/QCA separation and reuse rules early prevents architectural drift
2. **Skeleton Approach:** Creating stubs/skeletons enables parallel work without blocking
3. **Canon Protection:** Day 1 focus on canon lock is critical for Phase-6 success
4. **Infrastructure First:** Day 2 ensures development environment is ready

### ⚠️ Clarifications Needed

1. **QCD/QCA Scope:** Day 3 should focus on **structural boundaries** (tables, service contracts), not full implementation
2. **Reuse Scope:** Day 4 should create **stub endpoints** with basic copy logic, not full Track A-R implementation
3. **Costing Rules:** Day 6 should **document rules** and add **validation stubs**, not full Costing Pack UI

### 📝 Missing from Week-0 Plan

1. **Track E Database Implementation:** Week 0-1 includes database schema creation from Schema Canon (P6-DB-002)
   - **Recommendation:** Add to Day 2 or Day 3 (schema loading from Canon)
2. **Module Folder Boundaries:** P6-SETUP-008 (module folder structure) not explicitly called out
   - **Recommendation:** Add to Day 1 or Day 2

---

## ✅ Final Confirmation

**Week-0 Plan Status:** ✅ **APPROVED WITH CLARIFICATIONS**

**Approved Scope:**
- ✅ Day 1: Entry Gate & Guardrail Lock (canon protection)
- ✅ Day 2: Infrastructure Baseline (FastAPI + PostgreSQL + Docker)
- ✅ Day 3: Data Boundary Setup (QCD/QCA **structural separation only**)
- ✅ Day 4: Reuse Engine Skeleton (**stub endpoints** with basic copy logic)
- ✅ Day 5: UI Skeleton (React navigation structure)
- ✅ Day 6: Costing View Rules Enforcement (**rules documentation** + validation stubs)
- ✅ Day 7: Week-0 Validation Gate

**Clarifications Applied:**
- Day 3: Structural boundaries only (tables, service contracts), not full QCD/QCA generators
- Day 4: Stub endpoints with basic copy-never-link logic, not full Track A-R implementation
- Day 6: Rules documentation + validation stubs, not full Costing Pack UI

**Additional Recommendations:**
- Ensure Day 2 includes database schema loading from Schema Canon v1.0 (Track E, P6-DB-002)
- Consider adding module folder structure setup (P6-SETUP-008) to Day 1 or Day 2

---

## 🎯 Next Steps

1. **Proceed with Week-0 execution** using the approved plan
2. **Document clarifications** in Week-0 execution log
3. **Week-1 Planning:** Generate Week-1 to Week-3 task grid (Track-wise) with acceptance criteria
4. **Legacy Parity Gate:** Define Week 8.5 checklist upfront (as requested)

---

**Document Status:** ✅ **CONFIRMED**  
**Last Updated:** 2025-01-27  
**Next Action:** Begin Week-0 execution
