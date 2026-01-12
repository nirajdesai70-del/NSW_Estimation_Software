# Phase-6 — Week-4 Evidence Pack

**Project:** NSW Estimation Software  
**Phase:** Phase-6  
**Week:** Week-4  
**Prepared By:** (fill)  
**Date:** (fill)  
**Status:** ✅ CLOSED (Day-1..Day-4)

---

## 1) Locked Invariants (Do Not Break)

- Copy-never-link
- QCD/QCA separation (Cost summary reads QCA only)
- No costing breakup in quotation view (summary-only)
- Fabrication remains summary-only
- Schema canon frozen (Phase-6)
- All changes are additive + read-only

---

## 2) Week-4 Deliverables Summary

### Day-1 — Quotation lifecycle visibility (read-only)
- Added `quotation_state`, `state_timestamp`
- Tests:
  - `tests/quotation/test_quotation_state_visibility.py`
  - `tests/quotation/test_freeze_immutability_cost_adders.py` (gated by `NSW_FROZEN_QID`)

### Day-2 — Cost integrity guardrails (drift detection)
- Added `integrity_status`, `integrity_hash`, `integrity_reasons`
- Added `app/services/cost_integrity_service.py`
- Tests:
  - `tests/integrity/test_cost_integrity_hash_stable.py`
  - `tests/integrity/test_cost_integrity_hash_changes_on_qca_update.py`

### Day-3 — Expanded summary read APIs (render helpers; no breakup)
- Added `panel_count`, `has_catalog_bindings`, `cost_head_codes`
- Fixed mutable default: `integrity_reasons` uses `Field(default_factory=list)`
- Tests:
  - `tests/summary/test_cost_summary_no_breakup_strict.py`
  - `tests/summary/test_cost_summary_render_helpers.py`

### Day-4 — Consolidated checks + API surface guard
- Consolidated runner:
  - `scripts/run_phase6_week4_checks.sh`
- API surface whitelist guard:
  - `tests/summary/test_cost_summary_top_level_whitelist.py`

---

## 3) Commands Executed (Copy/Paste)

### Backend health
```bash
curl -sf http://localhost:8003/health
```

### Consolidated Week-4 checks
```bash
./scripts/run_phase6_week4_checks.sh
```

---

## 4) Output Evidence (paste latest run output)

```
======================================
 Phase-6 | Week-4 Consolidated Checks
======================================
Checking backend health…
✅ Backend reachable

Running schema canon drift check…
== Schema Drift Check ==
DB: localhost:5433/nsw_estimation
Snapshot: docs/00_GOVERNANCE/schema_snapshot/schema_canon_v1.sql
-- Checking tenant_id NOT NULL on QUO tables
   table_name    | column_name | is_nullable 
-----------------+-------------+-------------
 quote_bom_items | tenant_id   | NO
 quote_boms      | tenant_id   | NO
 quote_panels    | tenant_id   | NO
(3 rows)

-- Checking QCA uniqueness index
       indexname        
------------------------
 quote_cost_adders_pkey
 uq_qca_panel_costhead
(2 rows)

PASS: Minimal canon drift checks completed (Week-1 scope).

Running Week-3 Day-4 checks…
======================================
 Phase-6 | Week-3 Day-4 Checks
======================================
Checking backend health…
✅ Backend reachable

Running canon drift check…
== Schema Drift Check ==
DB: localhost:5433/nsw_estimation
Snapshot: docs/00_GOVERNANCE/schema_snapshot/schema_canon_v1.sql
-- Checking tenant_id NOT NULL on QUO tables
   table_name    | column_name | is_nullable 
-----------------+-------------+-------------
 quote_bom_items | tenant_id   | NO
 quote_boms      | tenant_id   | NO
 quote_panels    | tenant_id   | NO
(3 rows)

-- Checking QCA uniqueness index
       indexname        
------------------------
 quote_cost_adders_pkey
 uq_qca_panel_costhead
(2 rows)

PASS: Minimal canon drift checks completed (Week-1 scope).

Running Week-3 tests…
...                                                                      [100%]
3 passed in 0.46s

======================================
 ✅ Week-3 Day-4 Checks PASSED
======================================

Running Week-4 Day-1 checks…
======================================
 Phase-6 | Week-4 Day-1 Checks
======================================
Checking backend health…
✅ Backend reachable

Running canon drift check…
== Schema Drift Check ==
DB: localhost:5433/nsw_estimation
Snapshot: docs/00_GOVERNANCE/schema_snapshot/schema_canon_v1.sql
-- Checking tenant_id NOT NULL on QUO tables
   table_name    | column_name | is_nullable 
-----------------+-------------+-------------
 quote_bom_items | tenant_id   | NO
 quote_boms      | tenant_id   | NO
 quote_panels    | tenant_id   | NO
(3 rows)

-- Checking QCA uniqueness index
       indexname        
------------------------
 quote_cost_adders_pkey
 uq_qca_panel_costhead
(2 rows)

PASS: Minimal canon drift checks completed (Week-1 scope).

Running Week-3 regression tests…
...                                                                      [100%]
3 passed in 0.32s

Running Week-4 Day-1 tests…
..                                                                       [100%]
2 passed in 0.26s

======================================
 ✅ Week-4 Day-1 Checks PASSED
======================================

Running Week-4 Day-2 checks…
======================================
 Phase-6 | Week-4 Day-2 Checks
======================================
Checking backend health…
✅ Backend reachable

Running canon drift check…
== Schema Drift Check ==
DB: localhost:5433/nsw_estimation
Snapshot: docs/00_GOVERNANCE/schema_snapshot/schema_canon_v1.sql
-- Checking tenant_id NOT NULL on QUO tables
   table_name    | column_name | is_nullable 
-----------------+-------------+-------------
 quote_bom_items | tenant_id   | NO
 quote_boms      | tenant_id   | NO
 quote_panels    | tenant_id   | NO
(3 rows)

-- Checking QCA uniqueness index
       indexname        
------------------------
 quote_cost_adders_pkey
 uq_qca_panel_costhead
(2 rows)

PASS: Minimal canon drift checks completed (Week-1 scope).

Running Week-3 regression tests…
...                                                                      [100%]
3 passed in 0.31s

Running Week-4 Day-1 tests…
..                                                                       [100%]
2 passed in 0.26s

Running Week-4 Day-2 tests…
..                                                                       [100%]
2 passed in 0.34s

======================================
 ✅ Week-4 Day-2 Checks PASSED
======================================

Running Week-4 Day-3 checks…
======================================
 Phase-6 | Week-4 Day-3 Checks
======================================
Checking backend health…
✅ Backend reachable

Running canon drift check…
== Schema Drift Check ==
DB: localhost:5433/nsw_estimation
Snapshot: docs/00_GOVERNANCE/schema_snapshot/schema_canon_v1.sql
-- Checking tenant_id NOT NULL on QUO tables
   table_name    | column_name | is_nullable 
-----------------+-------------+-------------
 quote_bom_items | tenant_id   | NO
 quote_boms      | tenant_id   | NO
 quote_panels    | tenant_id   | NO
(3 rows)

-- Checking QCA uniqueness index
       indexname        
------------------------
 quote_cost_adders_pkey
 uq_qca_panel_costhead
(2 rows)

PASS: Minimal canon drift checks completed (Week-1 scope).

Running Week-3 regression tests…
...                                                                      [100%]
3 passed in 0.34s

Running Week-4 Day-1 tests…
..                                                                       [100%]
2 passed in 0.25s

Running Week-4 Day-2 tests…
..                                                                       [100%]
2 passed in 0.34s

Running Week-4 Day-3 tests…
..                                                                       [100%]
2 passed in 0.17s

======================================
 ✅ Week-4 Day-3 Checks PASSED
======================================

Running Week-4 Day-4 API surface guard…
.                                                                        [100%]
1 passed in 0.16s

======================================
 ✅ Phase-6 | Week-4 Consolidated Checks PASSED
======================================
```

---

## 5) API Response Evidence (sample)

```bash
curl -s -H "X-Tenant-ID: 1" -H "X-User-ID: 1" \
  http://localhost:8003/api/v1/quotation/4/cost-summary | jq
```

**Sample Response:**
```json
{
    "quotation_id": 4,
    "panels": [
        {
            "panel_id": 8,
            "currency": "INR",
            "cost_heads": {
                "BUSBAR": 3500.0,
                "LABOUR": 3000.0
            }
        }
    ],
    "quotation_state": "DRAFT",
    "state_timestamp": "2026-01-11T08:06:05.650320+00:00",
    "integrity_status": "OK",
    "integrity_hash": "da80b99c6ff9da99df7e104fa8c5373bc19409a25e590bbc5629f990f43312fc",
    "integrity_reasons": [],
    "panel_count": 1,
    "has_catalog_bindings": true,
    "cost_head_codes": [
        "BUSBAR",
        "LABOUR"
    ]
}
```

**Verified top-level keys (all present):**
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

## 6) Notes / Deviations

- None (unless recorded here)

---

## 7) Commit Hash Placeholders

- Week-4 Day-1: (fill)
- Week-4 Day-2: (fill)
- Week-4 Day-3: (fill)
- Week-4 Day-4: (fill)

---
