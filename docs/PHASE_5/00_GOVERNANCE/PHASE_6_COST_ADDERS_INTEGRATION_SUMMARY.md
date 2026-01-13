# Phase-6 Cost Adders Integration Summary

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ✅ INTEGRATED INTO EXECUTION PLAN  
**Reference:** Cost Adders Final Spec + Task Inserts + Integration Analysis

---

## 🎯 Executive Summary

Cost Adders feature has been fully integrated into Phase-6 Execution Plan v1.4 and Complete Scope & Task Summary v1.4.

**Impact:**
- ✅ **10 new tasks** added across Track D0, Track D, and Track E
- ✅ **5 existing tasks** updated to include cost adders
- ✅ **1 task** updated with cost adders placeholder
- ✅ **Total task count:** ~133 tasks (was ~123)
- ✅ **Timeline:** No extension (parallel execution)

---

## 📋 Integration Details

### Track D0: Costing Engine Foundations (7 new tasks)

**Week 3:**
- **P6-COST-D0-008:** Seed generic cost heads for cost adders
  - BUSBAR, FABRICATION, LABOUR, TRANSPORTATION, ERECTION, COMMISSIONING, MISC
  - CostBucket mapping for summary roll-up lines

**Week 4:**
- **P6-COST-D0-009:** Create cost template master tables
  - `cost_templates` and `cost_template_lines` tables
  - `line_cost_bucket` field for per-line CostBucket

- **P6-COST-D0-010:** Create cost sheet runtime tables
  - `quote_cost_sheets`, `quote_cost_sheet_lines`, `quote_cost_adders` tables
  - Summary roll-up structure

**Week 5:**
- **P6-COST-D0-011:** Implement cost sheet calculation engine
  - LUMP_SUM, QTY_RATE, KG_RATE, METER_RATE, HOUR_RATE, PERCENT_OF_BASE calc modes

- **P6-COST-D0-012:** Implement cost adder roll-up generator
  - Auto-upsert to `quote_cost_adders` on sheet save/approve
  - PanelQty multiplication

- **P6-COST-D0-013:** Implement QCA (Quote Cost Adders) dataset
  - Canonical dataset from `quote_cost_adders` table
  - JSON export endpoint: `/quotation/{id}/export/cost-adders/json`

**Week 6:**
- **P6-COST-D0-014:** Update D0 Gate checklist to include cost adders
  - QCD (BOM-only) + QCA (cost adders) both functional
  - Performance acceptable with cost adders

---

### Track D: Costing & Reporting (2 new tasks + 5 updated)

**New Tasks (Week 7):**
- **P6-COST-019:** Add Cost Adders section to Panel Detail page
  - Display cost adders list (one row per cost head)
  - Status indicators, "Add Cost Adder" button
  - Navigation to cost sheet editor

- **P6-COST-020:** Implement cost sheet editor UI
  - Editable qty/rate rows
  - Auto-calculate amounts
  - Save/Approve/Lock buttons

**Updated Tasks:**
- **P6-COST-003:** Costing snapshot now includes QCD + QCA
- **P6-COST-004:** Panel summary now includes cost adders breakdown
- **P6-COST-006:** CostHead grouping now includes cost adders (BUSBAR, FABRICATION, etc.)
- **P6-COST-007:** Pivot tables now include cost adders
- **P6-COST-015:** Excel export now includes cost adders detail sheet

---

### Track E: Canon Implementation (1 new task)

**Week 1-2:**
- **P6-DB-005:** Seed cost template master data
  - Minimal templates for each cost head (FABRICATION, BUSBAR, LABOUR, etc.)
  - Template lines with calc_mode and line_cost_bucket

---

### Track A: Productisation (1 updated task)

**Week 2:**
- **P6-UI-004:** Panel details page now includes Cost Adders section placeholder
  - Section header and disabled "Add Cost Adder" button
  - Full implementation in Track D, Week 7

---

## 📊 Updated Statistics

### Task Counts
- **Track D0:** 14 tasks (was 7) - +7 cost adders tasks
- **Track D:** 20 tasks (was 18) - +2 new, +5 updated
- **Track E:** ~29 tasks (was ~28) - +1 cost template seed
- **Track A:** 33 tasks (1 updated with placeholder)
- **Total:** ~133 tasks (was ~123) - +10 new tasks

### Timeline
- **No formal extension required** - all tasks fit within existing 10-12 week timeline
- **Buffer recommended: +1 week** - for unexpected issues or complexity
- **Parallel execution** - cost adders work runs in parallel with existing tracks

---

## 🔗 Key Design Decisions (From Final Spec)

### Data Model
- ✅ **QCD remains BOM-only** (stable contract v1.0)
- ✅ **QCA is separate dataset** (cost adders summary)
- ✅ **Costing Pack consumes QCD + QCA** together

### CostBucket Mapping
- **Summary Level:** Uses `cost_heads.category` (default bucket)
  - FABRICATION → MATERIAL (summary)
  - BUSBAR → MATERIAL
  - LABOUR → LABOUR
  - TRANSPORTATION → OTHER
  - ERECTION → LABOUR
  - COMMISSIONING → OTHER

- **Detail Level:** Uses `line_cost_bucket` per template line
  - Fabrication sheet: Steel=MATERIAL, Coating=OTHER, Manpower=LABOUR

### Calc Modes
- ✅ LUMP_SUM, QTY_RATE, KG_RATE, METER_RATE, HOUR_RATE, PERCENT_OF_BASE

### Approval Workflow
- ✅ Simple status field (DRAFT → APPROVED → LOCKED)
- ✅ Manual "Approve" button (no approval queue in Phase-6)
- ✅ Full workflow deferred to Phase-7

---

## ✅ Phase-5 Compliance

- ✅ **No schema meaning changes** (additive tables only)
- ✅ **QCD contract remains stable** (v1.0, BOM-only)
- ✅ **QCA is new dataset** (does not break QCD contract)
- ✅ **No guardrail changes**
- ✅ **No API contract violations**
- ✅ **Fully compliant with Phase-6 rule**

---

## 📚 Related Documents

- **Cost Adders Final Spec:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COST_ADDERS_FINAL_SPEC.md`
- **Task Inserts:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COST_ADDERS_TASK_INSERTS.md`
- **Integration Analysis:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COST_ADDERS_INTEGRATION_ANALYSIS.md`
- **Phase-6 Execution Plan v1.4:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Phase-6 Complete Scope v1.4:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COMPLETE_SCOPE_AND_TASKS.md`

---

**Document Status:** ✅ INTEGRATION COMPLETE  
**Last Updated:** 2025-01-27  
**Next Action:** Begin Phase-6 execution with Cost Adders tasks included

