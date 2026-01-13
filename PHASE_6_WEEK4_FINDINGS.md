# Phase 6 Week 4 Findings
## Extracted from PHASE6_WEEK4_EVIDENCE_PACK.md

**Date:** 2025-01-27  
**Status:** EXTRACTED  
**Source:** `evidence/PHASE6_WEEK4_EVIDENCE_PACK.md`

---

## 🔒 Locked Invariants (Do Not Break)

These invariants must be documented in the Rules Matrix:

1. **Copy-never-link** - Never link, always copy
2. **QCD/QCA separation** - Cost summary reads QCA only
3. **No costing breakup in quotation view** - Summary-only display
4. **Fabrication remains summary-only** - No detailed breakdown
5. **Schema canon frozen (Phase-6)** - Schema canon is frozen during Phase 6
6. **All changes are additive + read-only** - No destructive changes

---

## 📋 Week 4 Deliverables

### Day-1 — Quotation lifecycle visibility (read-only)
- **Added Fields:**
  - `quotation_state`
  - `state_timestamp`
- **Tests Created:**
  - `tests/quotation/test_quotation_state_visibility.py`
  - `tests/quotation/test_freeze_immutability_cost_adders.py` (gated by `NSW_FROZEN_QID`)

### Day-2 — Cost integrity guardrails (drift detection)
- **Added Fields:**
  - `integrity_status`
  - `integrity_hash`
  - `integrity_reasons`
- **Service Created:**
  - `app/services/cost_integrity_service.py`
- **Tests Created:**
  - `tests/integrity/test_cost_integrity_hash_stable.py`
  - `tests/integrity/test_cost_integrity_hash_changes_on_qca_update.py`

### Day-3 — Expanded summary read APIs (render helpers; no breakup)
- **Added Fields:**
  - `panel_count`
  - `has_catalog_bindings`
  - `cost_head_codes`
- **Fixed:**
  - Mutable default: `integrity_reasons` uses `Field(default_factory=list)`
- **Tests Created:**
  - `tests/summary/test_cost_summary_no_breakup_strict.py`
  - `tests/summary/test_cost_summary_render_helpers.py`

### Day-4 — Consolidated checks + API surface guard
- **Consolidated Runner:**
  - `scripts/run_phase6_week4_checks.sh`
- **API Surface Whitelist Guard:**
  - `tests/summary/test_cost_summary_top_level_whitelist.py`

---

## 🧪 Test Coverage

### Week 3 Regression Tests
- 3 tests passing (0.32-0.46s)

### Week 4 Tests
- Day-1: 2 tests passing (0.26s)
- Day-2: 2 tests passing (0.34s)
- Day-3: 2 tests passing (0.17s)
- Day-4: 1 test passing (0.16s)

**Total Week 4 Tests:** 7 new tests + 3 regression tests = 10 tests total

---

## 📊 API Response Structure

### Cost Summary API Response
```json
{
    "quotation_id": 4,
    "panels": [...],
    "quotation_state": "DRAFT",
    "state_timestamp": "2026-01-11T08:06:05.650320+00:00",
    "integrity_status": "OK",
    "integrity_hash": "...",
    "integrity_reasons": [],
    "panel_count": 1,
    "has_catalog_bindings": true,
    "cost_head_codes": ["BUSBAR", "LABOUR"]
}
```

### Verified Top-Level Keys
- ✅ `quotation_id`
- ✅ `panels`
- ✅ `quotation_state`
- ✅ `state_timestamp`
- ✅ `integrity_status`
- ✅ `integrity_hash`
- ✅ `integrity_reasons`
- ✅ `panel_count`
- ✅ `has_catalog_bindings`
- ✅ `cost_head_codes`

---

## 🔗 Dependencies

### Week 4 Dependencies on Week 3
- Week 4 builds on Week 3 work
- Week 3 regression tests must pass before Week 4 tests
- Schema canon drift checks from Week 1 scope continue

### Schema Canon Checks
- Checking `tenant_id NOT NULL` on QUO tables:
  - `quote_bom_items`
  - `quote_boms`
  - `quote_panels`
- Checking QCA uniqueness index:
  - `quote_cost_adders_pkey`
  - `uq_qca_panel_costhead`

---

## 📝 Actions for Matrix Population

### Rules Matrix
- [ ] Add all 6 locked invariants as rules
- [ ] Mark as HIGH priority
- [ ] Mark as ACTIVE status
- [ ] Reference: `PHASE6_WEEK4_EVIDENCE_PACK.md`

### Tasks Matrix
- [ ] Add Day-1 task: Quotation lifecycle visibility
- [ ] Add Day-2 task: Cost integrity guardrails
- [ ] Add Day-3 task: Expanded summary read APIs
- [ ] Add Day-4 task: Consolidated checks + API surface guard
- [ ] Link to test files created
- [ ] Link to service files created

### Work Breakdown Matrix
- [ ] Add Week 4 work items
- [ ] Break down into Day-1 through Day-4 sub-items
- [ ] Link to tasks
- [ ] Link to tests

### Sequence Matrix
- [ ] Document Week 4 sequence
- [ ] Document dependencies on Week 3
- [ ] Document test execution order

---

## 🚨 Gaps Identified

### Missing Information
- [ ] Week 1-3 evidence packs not found
- [ ] Week 1-3 deliverables not documented
- [ ] Full execution timeline not clear
- [ ] Track assignments for Week 4 work unclear

### Questions
- Which track(s) does Week 4 work belong to?
- What are the Week 1-3 deliverables?
- What is the full Phase 6 timeline?
- Are there other weeks beyond Week 4?

---

**Status:** EXTRACTED  
**Next Action:** Add to Rules Matrix and Tasks Matrix
