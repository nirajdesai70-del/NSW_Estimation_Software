# Phase-6 Week-4 Detailed Plan

**Week:** Week-4 (Resolution UX + Multi-SKU + Canon Enforcement + Parity Validation)  
**Status:** ⚠️ PARTIAL (Week-4B read-only hardening DONE; Week-4A planned scope pending)  
**Closure Status:** ⏳ Pending completion of planned Week-4 scope  
**Date Created:** 2025-01-27  
**Last Updated:** 2025-01-27

---

## Executive Summary

Week-4 delivers the resolution UX layer and canon enforcement that makes NSW a usable estimator product. This includes L0→L1→L2 resolution UX, resolution constraints enforcement, multi-SKU linkage support, and post-reuse editability verification. Week-4 also includes governance hardening work that was already completed (Week-4B sub-closure).

**Key Deliverables:**
- L0→L1→L2 Resolution UX (Track A)
- Resolution constraints enforcement + error taxonomy mapping (Track E)
- Multi-SKU linkage support (Track E)
- Post-reuse editability verification + guardrails-after-reuse verification (Track A-R)
- Read-only governance hardening (Week-4B - already completed)

**Critical Alarms (From Matrix):**
- 🔴 **4 Compliance Alarms** (must resolve before Phase-6 closure)
  - ALARM-RESOLUTION-CONSTRAINTS (P6-RES-023/024)
  - ALARM-MULTI-SKU (P6-SKU-001..003)
  - ALARM-REUSE-EDITABILITY (P6-REUSE-006)
  - ALARM-REUSE-GUARDRAILS (P6-REUSE-007)
- 🟠 **High Priority Items** (design documentation)
- 🟡 **Medium Priority Items** (UI polish, non-critical enhancements)

**Note:** Week-4 has two distinct scopes: Week-4A (planned resolution/Multi-SKU/parity) and Week-4B (read-only hardening - already completed with evidence).

---

## Week-4 Task Breakdown

### Track: Resolution UX (Track A) + Canon Enforcement (Track E) + Multi-SKU (Track E) + Post-Reuse Validation (Track A-R) + Read-Only Hardening (Week-4B)

#### Track A - Resolution UX (Week-4A Planned Scope)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-UI-017 | Design L0→L1→L2 resolution UX | `docs/PHASE_6/UI/L0_L1_L2_RESOLUTION_UX.md` | ❌ MISSING | 🟠 | Design document with L0/L1/L2 selection interfaces, flow visualization, status indicators |
| P6-UI-018 | Implement L0 selection UI | UI + API integration (generic product selection) | ❌ MISSING | 🔴 **COMPLIANCE** | L0 selection interface with category/subcategory filters, generic product search/select. Part of ALARM-RESOLUTION-UX |
| P6-UI-019 | Implement L1 resolution UI | UI + service integration (intent-based selection) | ❌ MISSING | 🔴 **COMPLIANCE** | L1 resolution interface with intent-based selection (voltage, duty, attributes), L1 line groups display. Part of ALARM-RESOLUTION-UX |
| P6-UI-020 | Implement L2 selection UI | UI + SKU binding (SKU selection from L1 candidates) | ❌ MISSING | 🔴 **COMPLIANCE** | L2 selection interface with SKU selection from L1 candidates, price availability display. Part of ALARM-RESOLUTION-UX |
| P6-UI-021 | Implement resolution flow visualization | UI component (current stage, resolution path, unresolved warnings) | ❌ MISSING | 🟠 | Resolution flow visualization showing L0→L1→L2 progression, navigation between stages |
| P6-UI-022 | Implement resolution status indicators | Item/BOM/panel indicators (L0 selected, L1 resolved, L2 resolved, missing resolution) | ❌ MISSING | 🔴 **COMPLIANCE** | Visual status indicators at component/BOM/panel levels for resolution status. Part of ALARM-RESOLUTION-UX |

**Track A (Resolution UX) Status:** ❌ MISSING (Week-4A planned scope - not implemented)

---

#### Track E - Resolution Constraints & Error Taxonomy (Week-4A Planned Scope)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-RES-023 | Enforce resolution constraints | Service + DB parity proof (MBOM vs QUO constraints) | ❌ MISSING | 🔴 **COMPLIANCE** | Enforce MBOM: L0/L1 only, no ProductId; QUO: L0/L1/L2 allowed, L2 requires ProductId. Part of ALARM-RESOLUTION-CONSTRAINTS |
| P6-RES-024 | Error taxonomy mapping | Standard error envelope + B3 codes + request_id propagation | ❌ MISSING | 🔴 **COMPLIANCE** | Map resolution errors to B3 error taxonomy codes, ensure error messages match taxonomy, HTTP status codes match taxonomy. Part of ALARM-RESOLUTION-CONSTRAINTS |

**Track E (Resolution Constraints) Status:** ❌ MISSING (Week-4A planned scope - compliance obligation)

---

#### Track E - Multi-SKU Linkage (Week-4A Planned Scope)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-SKU-001 | parent_line_id grouping rules | Backend support + schema usage (grouping rules for multi-SKU lines) | ❌ MISSING | 🔴 **COMPLIANCE** | parent_line_id grouping rules for multi-SKU linkage. Part of ALARM-MULTI-SKU (mandatory Week-4 compliance) |
| P6-SKU-002 | UI rendering grouped lines | UI grouping + indicators (display of grouped multi-SKU lines) | ❌ MISSING | 🔴 **COMPLIANCE** | UI rendering for grouped multi-SKU lines with grouping indicators. Part of ALARM-MULTI-SKU |
| P6-SKU-003 | Safe metadata_json edit | Validation + UI safe editor (metadata_json safe edit rules) | ❌ MISSING | 🔴 **COMPLIANCE** | Safe editor for metadata_json with schema validation, validation rules for metadata_json edits. Part of ALARM-MULTI-SKU |

**Track E (Multi-SKU) Status:** ❌ MISSING (Week-4A planned scope - mandatory Week-4 compliance)

---

#### Track A-R - Post-Reuse Validation (Week-4A Planned Scope)

| Task ID | Task Description | Planned Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|---------------------|-----------------|-------------|-------|
| P6-REUSE-006 | Post-reuse editability verification | Verification report + tests (items remain editable after reuse) | ❌ MISSING | 🔴 **COMPLIANCE** | Verify items remain editable after reuse (quotation/panel/feeder/BOM/master BOM apply). Part of ALARM-REUSE-EDITABILITY |
| P6-REUSE-007 | Guardrails after reuse verification | Verification report + tests (guardrails enforced on reused content) | ❌ MISSING | 🔴 **COMPLIANCE** | Verify guardrails G1-G8 enforced on reused content, test guardrail enforcement after each reuse operation. Part of ALARM-REUSE-GUARDRAILS |

**Track A-R (Post-Reuse Validation) Status:** ❌ MISSING (Week-4A planned scope - compliance obligation)

---

#### Week-4B - Read-Only Governance Hardening (Already Completed)

| Task ID | Task Description | Deliverable | Evidence Status | Alarm Level | Notes |
|---------|------------------|-------------|-----------------|-------------|-------|
| Week-4B-001 | State visibility fields | Quotation state + timestamp in cost-summary | ✅ DONE | — | State visibility fields added to cost summary |
| Week-4B-002 | Integrity fields + hash | Integrity hash + drift reasons | ✅ DONE | — | Integrity hash calculation and drift reason tracking |
| Week-4B-003 | Render helpers | Render helpers for cost summary | ✅ DONE | — | Render helpers implemented and tested |
| Week-4B-004 | Strict no-breakup denylist | API whitelist guard + denylist | ✅ DONE | — | Strict no-breakup denylist enforcement |
| Week-4B-005 | API top-level whitelist | Top-level API whitelist guard | ✅ DONE | — | API whitelist guard for top-level endpoints |
| Week-4B-006 | Consolidated runner | Week-4 consolidated runner script | ✅ DONE | — | scripts/run_phase6_week4_checks.sh |
| Week-4B-007 | Evidence pack | Week-4 evidence documentation | ✅ DONE | — | evidence/PHASE6_WEEK4_EVIDENCE_PACK.md |

**Week-4B Status:** ✅ CLOSED (Sub-deliverable completed with evidence)

**Evidence:** `evidence/PHASE6_WEEK4_EVIDENCE_PACK.md` + `scripts/run_phase6_week4_checks.sh`

---

## Alarm Summary for Week-4

**Source:** Phase-6 Document Review Matrix → "Consolidated Alarms Register"  
**Status:** All alarms from matrix included and verified

---

### 🔴 Compliance Alarms (Must Resolve Before Phase-6 Closure)

These alarms are **mandatory** for Phase-6 sign-off. They block governance compliance and cannot be deferred.

| Alarm ID | First Identified | Task ID(s) | Description | Status | Resolution Required |
|----------|------------------|------------|-------------|--------|---------------------|
| **ALARM-RESOLUTION-CONSTRAINTS** | Review 1 (Finalized Review 4) | P6-RES-023, P6-RES-024 | Resolution constraints enforced + error taxonomy mapping | ❌ MISSING | Implement resolution constraints enforcement + error taxonomy mapping (B3 codes) |
| **ALARM-MULTI-SKU** | Review 3 (Finalized Review 4) | P6-SKU-001..003 | Multi-SKU linkage (mandatory Week-4 compliance) | ❌ MISSING | Implement parent_line_id grouping + UI rendering + safe metadata_json edit |
| **ALARM-REUSE-EDITABILITY** | Review 1 (Finalized Review 4) | P6-REUSE-006 | Post-reuse editability verification missing | ❌ MISSING | Verify items remain editable after reuse (all reuse operations) |
| **ALARM-REUSE-GUARDRAILS** | Review 1 (Finalized Review 4) | P6-REUSE-007 | Guardrail validation after reuse missing | ❌ MISSING | Verify guardrails G1-G8 enforced on reused content |

**Alarm Details:**

#### ALARM-RESOLUTION-CONSTRAINTS (Compliance)
- **Tasks Affected:** P6-RES-023, P6-RES-024
- **Impact:** Canon enforcement requirement. Resolution constraints must be enforced exactly as Schema Canon specifies.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (upgraded from Review 3)
- **Resolution:** 
  - P6-RES-023: Enforce resolution constraints exactly as Schema Canon
    - Enforce MBOM: L0/L1 only, no ProductId
    - Enforce QUO: L0/L1/L2 allowed, L2 requires ProductId
    - Enforce CHECK constraints at DB level
    - Enforce constraints at service level
    - Enforce constraints at UI level (prevent invalid selections)
  - P6-RES-024: Errors must map to B3 error taxonomy codes
    - Review error taxonomy from Phase-5 (03_ERROR_TAXONOMY.md)
    - Map resolution errors to taxonomy codes
    - Ensure error messages match taxonomy
    - Ensure HTTP status codes match taxonomy
    - Ensure request_id propagation
- **Notes:** Resolution constraints enforcement is a canon enforcement requirement. Must be implemented for Phase-6 sign-off.

#### ALARM-MULTI-SKU (Compliance - Mandatory Week-4)
- **Tasks Affected:** P6-SKU-001, P6-SKU-002, P6-SKU-003
- **Impact:** Phase-5 compliance obligation. Multi-SKU linkage is mandatory Week-4 compliance, blocking Phase-6 sign-off.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm (mandatory Week-4)
- **Resolution:** 
  - P6-SKU-001: Implement parent_line_id grouping rules
    - Backend support for parent_line_id grouping
    - Schema usage for multi-SKU grouping
    - Grouping rules implementation
  - P6-SKU-002: Implement UI rendering for grouped lines
    - UI grouping display
    - Grouping indicators
    - Multi-SKU line visualization
  - P6-SKU-003: Implement safe metadata_json edit
    - Safe editor for metadata_json
    - Schema validation for metadata_json
    - Validation rules for metadata_json edits
- **Notes:** Multi-SKU linkage is a mandatory Week-4 compliance obligation. Must be implemented for Phase-6 sign-off.

#### ALARM-REUSE-EDITABILITY (Compliance)
- **Tasks Affected:** P6-REUSE-006
- **Impact:** Legacy parity requirement. Post-reuse editability verification is mandatory for reuse workflows.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-REUSE-006: Implement post-reuse editability verification
    - Verify items remain editable after quotation copy
    - Verify items remain editable after panel copy
    - Verify items remain editable after feeder copy
    - Verify items remain editable after BOM copy
    - Verify items remain editable after master BOM apply
    - Test editability after each reuse operation
    - Verification report + tests
- **Notes:** Post-reuse editability verification ensures legacy parity. Must be verified for Phase-6 sign-off.

#### ALARM-REUSE-GUARDRAILS (Compliance)
- **Tasks Affected:** P6-REUSE-007
- **Impact:** Legacy parity requirement. Guardrail validation after reuse is mandatory for reuse workflows.
- **Matrix Status:** Finalized in Review 4 as **COMPLIANCE** alarm
- **Resolution:** 
  - P6-REUSE-007: Implement guardrails after reuse verification
    - Verify G1-G8 enforced on reused content
    - Test guardrail enforcement after quotation copy
    - Test guardrail enforcement after panel copy
    - Test guardrail enforcement after feeder copy
    - Test guardrail enforcement after BOM copy
    - Test guardrail enforcement after master BOM apply
    - Verification report + tests
- **Notes:** Guardrail validation after reuse ensures legacy parity. Must be verified for Phase-6 sign-off.

---

### 🟠 High Priority Alarms (Should Resolve)

These alarms should be resolved but are not blocking Phase-6 closure.

| Alarm ID | Task ID | Description | Status | Action Required |
|----------|---------|-------------|--------|-----------------|
| ALARM-UI-017 | P6-UI-017 | Design L0→L1→L2 resolution UX | ❌ MISSING | Create design document: `docs/PHASE_6/UI/L0_L1_L2_RESOLUTION_UX.md` |
| ALARM-UI-021 | P6-UI-021 | Resolution flow visualization | ❌ MISSING | Implement resolution flow visualization UI component |
| ALARM-SKU-CONTRACT | P6-SKU-001..003 | Multi-SKU JSON contract doc | ❌ MISSING | Create contract document: `docs/PHASE_6/SKU/MULTI_SKU_CONTRACT.md` (optional but recommended) |

---

### 🟡 Medium Priority (Non-Critical Enhancements)

These items are enhancements and not blocking Phase-6 closure.

| Task ID | Description | Status | Action Required |
|---------|-------------|--------|-----------------|
| UI Polish | UI polish, non-critical animations | ⏳ DEFERRED | UI polish and animations (non-critical, can be deferred) |
| Search UX | Search UX enhancements | ⏳ DEFERRED | Search UX enhancements (non-critical, can be deferred) |

---

## Verification Against Review Matrix

### ✅ Items Captured from Matrix

All Week-4 tasks from the Phase-6 Document Review Matrix are included:
- ✅ P6-UI-017..022 (Resolution UX - 6 tasks)
- ✅ P6-RES-023/024 (Resolution constraints + error taxonomy - 2 tasks)
- ✅ P6-SKU-001..003 (Multi-SKU linkage - 3 tasks)
- ✅ P6-REUSE-006/007 (Post-reuse validation - 2 tasks)
- ✅ Week-4B read-only hardening (7 tasks - already completed)

### ⚠️ Items Requiring Verification

1. **Resolution UX Implementation (P6-UI-017..022)**
   - Need to verify L0/L1/L2 selection UIs exist
   - Need to verify resolution flow visualization exists
   - Need to verify status indicators work
   - Current status: ❌ MISSING (needs verification)

2. **Resolution Constraints Enforcement (P6-RES-023/024)**
   - Need to verify constraints are enforced at DB/service/UI levels
   - Need to verify error taxonomy mapping works
   - Current status: ❌ MISSING (needs verification)

3. **Multi-SKU Linkage (P6-SKU-001..003)**
   - Need to verify parent_line_id grouping works
   - Need to verify UI rendering for grouped lines works
   - Need to verify safe metadata_json edit works
   - Current status: ❌ MISSING (needs verification)

4. **Post-Reuse Validation (P6-REUSE-006/007)**
   - Need to verify editability verification exists
   - Need to verify guardrails verification exists
   - Current status: ❌ MISSING (needs verification)

5. **Week-4B Read-Only Hardening**
   - ✅ Already verified: evidence/PHASE6_WEEK4_EVIDENCE_PACK.md exists
   - ✅ Already verified: scripts/run_phase6_week4_checks.sh exists
   - Current status: ✅ DONE (sub-closure completed)

---

## Week-4 Closure Criteria

### Required for Closure

**Week-4B (Already Completed):**
1. ✅ State visibility fields implemented
2. ✅ Integrity fields + hash implemented
3. ✅ Render helpers implemented
4. ✅ Strict no-breakup denylist implemented
5. ✅ API top-level whitelist implemented
6. ✅ Consolidated runner exists
7. ✅ Evidence pack complete

**Week-4A (Required to Close Week-4 Overall):**
1. ⏳ **Resolution UX Implemented** (P6-UI-017..022)
2. ⏳ **Resolution Constraints Enforced** (P6-RES-023)
3. ⏳ **Error Taxonomy Mapping Implemented** (P6-RES-024)
4. ⏳ **Multi-SKU Grouping Implemented** (P6-SKU-001..003)
5. ⏳ **Post-Reuse Editability Verified** (P6-REUSE-006)
6. ⏳ **Guardrails After Reuse Verified** (P6-REUSE-007)
7. ⏳ **All Week-4A Tests Passing** (Resolution + Multi-SKU + Reuse tests)
8. ⏳ **Design Documents Created** (P6-UI-017, optional: Multi-SKU contract)
9. ⏳ **All Compliance Alarms Resolved** (4 compliance alarms)
10. ⏳ **Week-4A Evidence Pack Complete** (separate from Week-4B)
11. ⏳ **No Canon Meaning Changes** (canon respected)

### Current Closure Status

- **Week-4B Status:** ✅ CLOSED (Sub-deliverable completed with evidence)
- **Week-4A Status:** ❌ MISSING (Planned scope not implemented)
- **Overall Week-4 Status:** ⚠️ PARTIAL (Week-4B done; Week-4A pending)
- **Compliance Alarms:** ❌ 4 alarms need resolution (ALARM-RESOLUTION-CONSTRAINTS, ALARM-MULTI-SKU, ALARM-REUSE-EDITABILITY, ALARM-REUSE-GUARDRAILS)
- **Formal Sign-off:** ⏳ PENDING (Week-4A must be completed for Week-4 closure)

**Closure Rule:** Week-4 overall can be marked CLOSED only if Week-4A (planned resolution/Multi-SKU/parity scope) is completed. Week-4B is already closed as a sub-deliverable.

---

## Dependencies

### Requires

- **Week-2:** Hierarchy CRUD (feeder/BOM/item) for realistic resolution flows
- **Week-3:** Pricing UX not strictly required to show resolution flow, but required to complete end-to-end estimator workflow
- **Week-3:** Guardrails runtime enforcement (P6-VAL-001..004) for guardrails-after-reuse verification

### Blocks

- **Week-5:** Locking visibility relies on resolution status indicators
- **Week-6:** Error/warning surfacing relies on error taxonomy mapping
- **Week-8.5:** Legacy parity gate readiness depends on post-reuse validation completion

---

## Risks & Mitigations

### Risk 1: Implementing Resolution UI Without Enforcing Constraints → Silent Canon Violations

**Mitigation:** Enforce P6-RES-023 at service layer first; UI is consumer. Implement constraints at DB/service levels before UI implementation.

### Risk 2: Multi-SKU Introduces Uncontrolled metadata_json Edits

**Mitigation:** Safe editor + schema validation + tests (P6-SKU-003). Implement validation rules before enabling metadata_json edits.

### Risk 3: Week-4B Work Mistaken as Week-4 Closure

**Mitigation:** Keep Week-4A evidence pack separate and mandatory. Week-4B is sub-closure only; Week-4A must be completed for overall closure.

### Risk 4: Resolution UX Implemented Without Error Taxonomy → Inconsistent Error Handling

**Mitigation:** Implement error taxonomy mapping (P6-RES-024) together with resolution UX. Ensure error codes/messages match taxonomy.

---

## Next Steps

### Immediate Actions Required

#### Priority 1: Resolve Compliance Alarms (Blocking)

1. **ALARM-RESOLUTION-CONSTRAINTS Resolution**
   - P6-RES-023: Implement resolution constraints enforcement
   - P6-RES-024: Implement error taxonomy mapping
   - Tests: test_resolution_constraints.py, test_error_taxonomy_mapping.py

2. **ALARM-MULTI-SKU Resolution**
   - P6-SKU-001: Implement parent_line_id grouping rules
   - P6-SKU-002: Implement UI rendering for grouped lines
   - P6-SKU-003: Implement safe metadata_json edit
   - Tests: test_multi_sku_grouping.py, test_metadata_json_safe_edit.py

3. **ALARM-REUSE-EDITABILITY Resolution**
   - P6-REUSE-006: Implement post-reuse editability verification
   - Tests: test_post_reuse_editability.py

4. **ALARM-REUSE-GUARDRAILS Resolution**
   - P6-REUSE-007: Implement guardrails after reuse verification
   - Tests: test_reuse_guardrails_validation.py

#### Priority 2: Complete Resolution UX (Blocking)

5. **Resolution UX Implementation**
   - P6-UI-017: Create design document
   - P6-UI-018: Implement L0 selection UI
   - P6-UI-019: Implement L1 resolution UI
   - P6-UI-020: Implement L2 selection UI
   - P6-UI-021: Implement resolution flow visualization
   - P6-UI-022: Implement resolution status indicators
   - Tests: test_l0_l1_l2_flow.py

#### Priority 3: Verification

6. **Implementation Verification**
   - Verify resolution UX works (all modes)
   - Verify constraints enforcement works
   - Verify multi-SKU grouping works
   - Verify post-reuse validation works
   - Verify all tests pass
   - Verify Week-4A evidence pack complete

---

## Implementation Artifacts

### Expected Artifacts (Week-4A Planned Scope)

1. **Scripts:**
   - `scripts/run_week4A_checks.sh` - Week-4A verification runner (new)
     - Runs all Week-4A tests (resolution + multi-SKU + reuse validation)
     - Verifies API endpoints
     - Validates resolution constraints enforcement
     - Validates multi-SKU grouping
     - Validates post-reuse validation
     - Generates Week-4A evidence summary
   - `scripts/run_phase6_week4_checks.sh` - Week-4B runner (already exists)

2. **Tests:**
   - `tests/resolution/test_l0_l1_l2_flow.py` - Resolution UX flow tests
     - Test L0 selection
     - Test L1 resolution
     - Test L2 selection
     - Test resolution flow visualization
     - Test status indicators
   - `tests/resolution/test_resolution_constraints.py` - Resolution constraints enforcement tests
     - Test MBOM constraints (L0/L1 only, no ProductId)
     - Test QUO constraints (L0/L1/L2 allowed, L2 requires ProductId)
     - Test DB constraint enforcement
     - Test service-level enforcement
     - Test UI-level enforcement
   - `tests/resolution/test_error_taxonomy_mapping.py` - Error taxonomy mapping tests
     - Test error codes match taxonomy
     - Test error messages match taxonomy
     - Test HTTP status codes match taxonomy
     - Test request_id propagation
   - `tests/sku/test_multi_sku_grouping.py` - Multi-SKU grouping tests
     - Test parent_line_id grouping rules
     - Test grouping backend support
     - Test schema usage
   - `tests/sku/test_metadata_json_safe_edit.py` - Metadata JSON safe edit tests
     - Test safe editor validation
     - Test schema validation
     - Test validation rules
   - `tests/reuse/test_post_reuse_editability.py` - Post-reuse editability tests
     - Test editability after quotation copy
     - Test editability after panel copy
     - Test editability after feeder copy
     - Test editability after BOM copy
     - Test editability after master BOM apply
   - `tests/reuse/test_reuse_guardrails_validation.py` - Guardrails after reuse tests
     - Test guardrails enforcement after quotation copy
     - Test guardrails enforcement after panel copy
     - Test guardrails enforcement after feeder copy
     - Test guardrails enforcement after BOM copy
     - Test guardrails enforcement after master BOM apply

3. **Evidence:**
   - `evidence/PHASE6_WEEK4A_EVIDENCE_PACK.md` - Week-4A evidence documentation (new)
     - API endpoint documentation
     - Test results summary
     - Resolution UX screenshots
     - Multi-SKU grouping examples
     - Post-reuse validation results
     - Guardrails validation results
   - `evidence/PHASE6_WEEK4_EVIDENCE_PACK.md` - Week-4B evidence documentation (already exists, keep unchanged)

4. **API Endpoints:**
   - GET /api/v1/quotation/{id}/resolution/l0 - L0 selection endpoint
   - GET /api/v1/quotation/{id}/resolution/l1 - L1 resolution endpoint
   - GET /api/v1/quotation/{id}/resolution/l2 - L2 selection endpoint
   - POST /api/v1/quotation/{id}/resolution/resolve - Resolution endpoint
   - GET /api/v1/quotation/{id}/sku/grouped - Multi-SKU grouped lines endpoint
   - PUT /api/v1/quotation/{id}/item/{itemId}/metadata - Metadata JSON update endpoint

5. **Frontend Components:**
   - L0 selection component (generic product search/select)
   - L1 resolution component (intent-based selection)
   - L2 selection component (SKU selection)
   - Resolution flow visualization component
   - Resolution status indicator component
   - Multi-SKU grouping display component
   - Metadata JSON safe editor component

6. **Backend Services:**
   - Resolution service (L0/L1/L2 resolution logic)
   - Resolution constraints service (constraint enforcement)
   - Error taxonomy service (error mapping)
   - Multi-SKU grouping service (parent_line_id grouping)
   - Metadata JSON validation service (safe edit validation)

7. **Documentation:**
   - `docs/PHASE_6/UI/L0_L1_L2_RESOLUTION_UX.md` - Resolution UX design document
   - `docs/PHASE_6/VALIDATION/RESOLUTION_CONSTRAINTS_ENFORCEMENT.md` - Resolution constraints documentation
   - `docs/PHASE_6/SKU/MULTI_SKU_CONTRACT.md` - Multi-SKU contract document (optional but recommended)

### Verification Checklist (Week-4A)

- [ ] Verify scripts/run_week4A_checks.sh exists
- [ ] Verify all Week-4A test files exist and pass
- [ ] Verify all API endpoints exist and work
- [ ] Verify all UI components exist and work
- [ ] Verify resolution constraints enforcement works (P6-RES-023)
- [ ] Verify error taxonomy mapping works (P6-RES-024)
- [ ] Verify multi-SKU grouping works (P6-SKU-001..003)
- [ ] Verify post-reuse editability verification works (P6-REUSE-006)
- [ ] Verify guardrails after reuse verification works (P6-REUSE-007)
- [ ] Verify evidence/PHASE6_WEEK4A_EVIDENCE_PACK.md exists
- [ ] Verify all tests pass in Week-4A runner
- [ ] Verify no canon meaning changes introduced

---

## Decision Point

**Week-4 Closure Status:**
- ⏳ **PENDING COMPLETION** (Week-4A planned scope)

**Options:**
1. **"Close Week-4 and start Week-5 detailed plan"** - If all Week-4A implementation artifacts verified and tests passing
2. **"Verify Week-4A implementation"** - If artifacts need verification
3. **"Complete Week-4A implementation"** - If resolution UX, multi-SKU, or post-reuse validation still missing

**Note:** Week-4B is already closed as a sub-deliverable. Week-4A must be completed for overall Week-4 closure.

---

## References

- **Phase-6 Document Review Matrix:** `PHASE6_DOCUMENT_REVIEW_MATRIX.md` (Master tracking file)
- **Phase-6 Execution Plan v1.4:** `PHASE_6_EXECUTION_PLAN.md` (Source of Week-4 tasks)
- **Week-4B Evidence Pack:** `evidence/PHASE6_WEEK4_EVIDENCE_PACK.md` (Read-only hardening evidence)
- **Week-4B Runner:** `scripts/run_phase6_week4_checks.sh` (Read-only hardening runner)
- **Review Matrix Alarms Section:** See `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → "Consolidated Alarms Register"
- **Error Taxonomy:** `docs/PHASE_5/03_ERROR_TAXONOMY.md` (for error taxonomy mapping)

---

## Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Total Tasks (Week-4A)** | 13 | All captured from matrix |
| **Total Tasks (Week-4B)** | 7 | Already completed |
| **Compliance Alarms** | 4 | 🔴 Must resolve |
| **High Priority Alarms** | 3 | 🟠 Should resolve |
| **Medium Priority Items** | 2 | 🟡 Can be deferred |
| **Completed Tasks (Week-4A)** | 0 | None fully complete |
| **Completed Tasks (Week-4B)** | 7 | ✅ All complete |
| **Missing Tasks (Week-4A)** | 13 | ❌ MISSING (need implementation/verification) |

---

## Alarm Resolution Checklist

### Compliance Alarms (Must Resolve)

- [ ] **ALARM-RESOLUTION-CONSTRAINTS:** Implement resolution constraints enforcement + error taxonomy mapping (P6-RES-023, P6-RES-024)
- [ ] **ALARM-MULTI-SKU:** Implement parent_line_id grouping + UI rendering + safe metadata_json edit (P6-SKU-001..003)
- [ ] **ALARM-REUSE-EDITABILITY:** Implement post-reuse editability verification (P6-REUSE-006)
- [ ] **ALARM-REUSE-GUARDRAILS:** Implement guardrails after reuse verification (P6-REUSE-007)

### High Priority Alarms (Should Resolve)

- [ ] **ALARM-UI-017:** Create L0→L1→L2 resolution UX design document (P6-UI-017)
- [ ] **ALARM-UI-021:** Implement resolution flow visualization (P6-UI-021)
- [ ] **ALARM-SKU-CONTRACT:** Create Multi-SKU contract document (optional but recommended)

### Documentation Tasks

- [ ] Complete resolution UX implementation (P6-UI-018..022)
- [ ] Complete resolution constraints enforcement (P6-RES-023/024)
- [ ] Complete multi-SKU implementation (P6-SKU-001..003)
- [ ] Complete post-reuse validation (P6-REUSE-006/007)
- [ ] Verify all implementation artifacts exist
- [ ] Verify all tests pass
- [ ] Verify Week-4A evidence pack is complete
- [ ] Verify no canon meaning changes introduced

---

**Document Status:** ✅ Complete - All alarms from matrix included  
**Last Verified:** 2025-01-27  
**Next Review:** After Week-4A implementation verification

**Note:** Week-4 has two distinct scopes: Week-4A (planned resolution/Multi-SKU/parity - pending) and Week-4B (read-only hardening - already closed with evidence). Week-4 overall closure requires Week-4A completion.
