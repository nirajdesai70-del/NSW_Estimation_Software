# Phase-6 Document Review Matrix

**Purpose:** Track 6 document reviews to reconcile Phase-6 execution against baseline plans and derive final decisions.  
**Created:** 2025-01-27  
**Status:** Review 6 of 6 Complete - Reconciliation Finalized

---

## Review Status Overview

| Review # | Document Name | Review Date | Status | Key Focus |
|----------|--------------|-------------|--------|-----------|
| 1 | Phase-6 Execution Plan v1.4 (2025-01-27) | 2025-01-27 | ✅ COMPLETE | Baseline plan reconciliation (Weeks 0-4) |
| 2 | Phase-6 Complete Scope & Task Summary v1.4 | 2025-01-27 | ✅ COMPLETE | Scope confirmation & gap validation (Weeks 0-4) |
| 3 | Phase-6 Execution Plan Revision Summary v1.2 | 2025-01-27 | ✅ COMPLETE | Compliance obligations & alarm prioritization |
| 4 | Phase-6 Execution Plan (Corrected Version Summary v1.2) | 2025-01-27 | ✅ COMPLETE | Final baseline reconciliation & track structure clarification |
| 5 | Legacy Parity Verification Checklist v1.0 (2025-01-27) | 2025-01-27 | ✅ COMPLETE | Parity evidence layer & verification mapping |
| 6 | Phase-6 Legacy Parity Addition Summary v1.3 | 2025-01-27 | ✅ COMPLETE | Track A-R canonical confirmation & final reconciliation lock |

---

## Review 1: Phase-6 Execution Plan v1.4 (2025-01-27)

### Document Metadata
- **Document:** Phase-6 Execution Plan v1.4 (2025-01-27)
- **Review Date:** 2025-01-27
- **Reviewer:** Reconciliation Analysis
- **Review Type:** Baseline Plan Validation
- **Scope:** Weeks 0-4 Planned Deliverables vs. Actual Evidence

### Key Findings Summary

#### ✅ Proven Delivered (Evidence Exists)
1. **Week-4 Read-Only Hardening:** Complete with evidence pack
   - Quotation lifecycle visibility (state, timestamp)
   - Cost integrity guardrails (hash, reasons)
   - Render helpers (panel_count, has_catalog_bindings, cost_head_codes)
   - Consolidated runners and whitelist guards

2. **Database & Schema:**
   - Schema drift check script exists and passes
   - DB schema parity validated

3. **Reuse/Copy Endpoints:**
   - Copy quotation/panel/feeder/BOM endpoints exist
   - Reuse invariant tests exist

4. **Development Infrastructure:**
   - Dev automation scripts exist and pass
   - Frontend/backend operational
   - Smoke test scripts functional

#### ⚠️ Planned but NOT Proven (Gaps Identified)

**Week-0 Setup Gaps:**
- Setup documentation (task register, QCD contract, D0 checklist) missing
- Naming convention compliance check not evidenced
- Cost template master data seeding not proven

**Week-1/2 UI Gaps:**
- Add Panel functionality (STUB exists, not implemented)
- Add Feeder functionality missing
- Add BOM functionality missing
- Add Item functionality missing
- BOM tree/hierarchy UI missing
- Customer name snapshot handling not proven
- Quantity persistence verification missing

**Week-2-4 Guardrails Gaps:**
- Guardrails G1-G8 runtime enforcement not proven
- Guardrail test suite missing
- API validation parity not proven
- Error taxonomy mapping missing

**Week-2.5-4 Reuse Gaps:**
- Master BOM apply functionality missing
- Post-reuse editability validation missing
- Guardrails enforced after reuse not proven

**Week-3 Pricing UX Gaps:**
- RateSource selector UI missing
- Pricing modes (auto/manual/fixed) UI missing
- Pricing status indicators missing

**Week-4 Resolution UX Gaps:**
- L0→L1→L2 resolution UX missing
- Resolution constraints enforcement missing
- Error taxonomy mapping (B3) missing

### Critical Alarms Identified

| Alarm ID | Category | Severity | Description | Impact |
|----------|----------|----------|-------------|--------|
| 🔴 ALARM-SETUP | Week-0 Setup | CRITICAL | Setup docs/gates missing (task register, QCD contract, D0 checklist) | Blocks governance compliance |
| 🔴 ALARM-CORE-CRUD | Week-1/2 UI | CRITICAL | Add Panel/Feeder/BOM/Item flows missing | Core functionality gaps |
| 🔴 ALARM-GUARDRAILS | Week-2-4 Validation | CRITICAL | Guardrails G1-G8 runtime + tests missing | Data integrity risks |
| 🔴 ALARM-MASTER-BOM | Track A-R Reuse | CRITICAL | Master BOM apply + post-reuse editability missing | Reuse workflow incomplete |
| 🔴 ALARM-PRICING-UX | Week-3 UI | CRITICAL | RateSource pricing UX missing | Pricing resolution incomplete |
| 🔴 ALARM-RESOLUTION-UX | Week-4 UI | CRITICAL | L0→L1→L2 resolution UX missing | Core resolution flow missing |

### Detailed Work Matrix (Weeks 0-4)

#### Week-0 — Entry Gate & Setup (Track E + Setup)

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-ENTRY-001..005 | Verify SPEC-5, Schema Canon, decisions, freeze gate, core engine | Entry gate stated passed; repo proof doc needed | ⚠️ PARTIAL | 🟡 |
| P6-ENTRY-006 | Naming convention compliance check | No evidence | ❌ MISSING | 🔴 |
| P6-SETUP-001 | Create Phase-6 project structure (docs/PHASE_6/*) | docs path in .cursorignore; evidence pack exists elsewhere | ⚠️ PARTIAL | 🟡 |
| P6-SETUP-002 | Review Phase-5 deliverables | Not found | ❌ MISSING | 🟠 |
| P6-SETUP-003 | Phase-6 task register | Not found | ❌ MISSING | 🔴 |
| P6-SETUP-004 | Costing manual structure | Not found | ❌ MISSING | 🟠 |
| P6-SETUP-005 | Freeze QCD contract v1.0 doc | Not found | ❌ MISSING | 🔴 |
| P6-SETUP-006 | D0 gate checklist doc | Not found | ❌ MISSING | 🔴 |
| P6-SETUP-007 | Review Phase-5 deliverables for implementation obligations | Not found | ❌ MISSING | 🟠 |
| P6-SETUP-008 | Module boundaries + PR rules | Not found | ❌ MISSING | 🟠 |
| P6-DB-001 | Choose DB creation method doc | Not found | ❌ MISSING | 🟠 |
| P6-DB-002..004 | DB schema + seeds + schema parity gate | ✅ drift check exists + passes | ✅ DONE | — |
| P6-DB-005 | Seed cost template master data | Not proven (QCA exists but not templates/sheets) | ❌ MISSING | 🔴 |

**Week-0 Plan Status:** ⚠️ PARTIAL (setup docs/gates missing)

---

#### Week-1 — Quotation & Panel UI (Track A)

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-UI-001 | Design quotation overview | Not found | ❌ MISSING | 🟠 |
| P6-UI-002 | Implement quotation overview page | React pages exist but not stated as "full overview UI" | ⚠️ PARTIAL | 🟡 |
| P6-UI-003 | Design panel details page | Not found | ❌ MISSING | 🟠 |
| P6-UI-004 | Implement panel details page | Partial view exists | ⚠️ PARTIAL | 🟡 |
| P6-UI-005 | Add Panel functionality | STUB exists; not implemented | ❌ MISSING | 🔴 |
| P6-UI-001A | customer_name_snapshot always stored | Not proven | ❌ MISSING | 🔴 |
| P6-UI-001B | customer_id nullable support | Not proven | ❌ MISSING | 🟠 |

**Week-1 Plan Status:** ⚠️ PARTIAL (Add Panel + customer snapshot missing)

---

#### Week-2 — Feeder/BOM Hierarchy UI + Guardrails Start (Track A + Track E)

**Track A UI:**

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-UI-006 | Design BOM hierarchy view | Not found | ❌ MISSING | 🟠 |
| P6-UI-007 | Implement BOM tree view | Not found | ❌ MISSING | 🔴 |
| P6-UI-008 | Add Feeder | Not found | ❌ MISSING | 🔴 |
| P6-UI-009 | Add BOM | Not found | ❌ MISSING | 🔴 |
| P6-UI-010 | Item list display (full) | Partial listing exists | ⚠️ PARTIAL | 🟡 |
| P6-UI-010A | Quantity persistence verification | Not found | ❌ MISSING | 🔴 |

**Track E Guardrails:**

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-VAL-001 | Guardrails G1–G8 runtime | Not proven | ❌ MISSING | 🔴 |
| P6-VAL-002 | DB constraints aligned | drift check covers some constraints; guardrails not proven | ⚠️ PARTIAL | 🟡 |
| P6-VAL-003 | API validation parity | Not proven | ❌ MISSING | 🔴 |
| P6-VAL-004 | Guardrail test suite | Not proven | ❌ MISSING | 🔴 |

**Week-2 Plan Status:** ⚠️ PARTIAL (CRUD flows + guardrails missing)

---

#### Week-2.5–4 — Track A-R Reuse & Legacy Parity

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| REUSE-001..004 | Copy quotation/panel/feeder/BOM | ✅ endpoints + reuse tests exist | ✅ DONE | — |
| REUSE-005 | Apply Master BOM template | Not proven | ❌ MISSING | 🔴 |
| REUSE-006 | Post-reuse editability validation | Not proven | ❌ MISSING | 🔴 |
| REUSE-007 | Guardrails enforced after reuse | Not proven | ❌ MISSING | 🔴 |

**Track A-R Status:** ⚠️ PARTIAL (copy flows done, master apply + editability missing)

---

#### Week-3 — Pricing Resolution UX (Track A) + Cost Adders Foundations (Track D0/E)

**Track A Pricing UX:**

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-UI-011..016 | Pricing UX complete (RateSource selector + modes + indicators) | Not proven | ❌ MISSING | 🔴 |

**Track D0/E Costing Foundations:**

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-COST-D0-008 | cost heads seeded | Cost heads behaving (BUSBAR/LABOUR etc.) → likely seeded | ⚠️ PARTIAL | 🟡 |
| P6-COST-D0-009..010 | cost templates + cost sheets tables | Not proven | ❌ MISSING | 🔴 |
| P6-DB-005 | template seed data | Not proven | ❌ MISSING | 🔴 |
| P6-COST-D0-013 | QCA dataset + JSON export | QCA behavior via quote_cost_adders; export endpoint not proven | ⚠️ PARTIAL | 🟡 |

**Week-3 Plan Status:** ⚠️ PARTIAL (pricing UX + cost templates missing)

---

#### Week-4 — Resolution UX (Track A) + Read-Only Hardening

**Planned Resolution UX (Track A):**

| Task ID | Planned Deliverable | Evidence Found | Status | Alarm |
|---------|---------------------|----------------|--------|-------|
| P6-UI-017..022 | L0→L1→L2 resolution UX | Not proven | ❌ MISSING | 🔴 |
| P6-RES-023 | Resolution constraints enforced | Not proven | ❌ MISSING | 🔴 |
| P6-RES-024 | Error taxonomy mapping | Not proven | ❌ MISSING | 🔴 |

**Actual Week-4 Work (Read-Only Hardening):**

| Task ID | Deliverable | Evidence Found | Status | Alarm |
|---------|-------------|----------------|--------|-------|
| Week-4 Day-1..4 | State + integrity + render helpers + evidence | ✅ evidence pack + tests + runner | ✅ DONE | — |

**Week-4 Plan Status:** ⚠️ PARTIAL (resolution UX missing, read-only hardening complete)

**Note:** Week-4 read-only hardening is real and complete, but it is NOT the same as the planned "resolution UX" from v1.4. This is a thread-drift issue.

---

### Review 1 Conclusions

#### Status Corrections Required

1. **Week-0 Status:** Should be ⚠️ PARTIAL (not CLOSED) until setup docs/gates exist
2. **Week-1 Status:** Should be ⚠️ PARTIAL (not CLOSED) until Add Panel + customer snapshot delivered
3. **Week-2 Status:** Should be ⚠️ PARTIAL (not CLOSED) until CRUD flows + guardrails delivered
4. **Week-3 Status:** Should be ⚠️ PARTIAL (not CLOSED) until pricing UX + cost templates delivered
5. **Week-4 Status:** Should be ⚠️ PARTIAL (resolution UX missing; read-only hardening complete but separate)

#### Key Risks Identified

1. **Governance Compliance Risk:** Missing setup docs (task register, QCD contract, D0 checklist) may block formal closure
2. **Functional Completeness Risk:** Core CRUD flows (Add Panel/Feeder/BOM/Item) are missing, creating functionality gaps
3. **Data Integrity Risk:** Guardrails G1-G8 runtime enforcement missing creates data quality risks
4. **Integration Risk:** Continuing with Week-5+ without plugging CRUD + guardrails will cause major integration pain
5. **Thread Drift Risk:** Actual work (read-only hardening) differs from planned work (resolution UX), requiring reconciliation

#### Next Review Recommendations

**Recommended Documents for Review 2-6:**
1. Phase-6 Kickoff Charter (to confirm acceptance criteria and any defers)
2. Phase-5 Canonical Working Record extract (to verify what was already implemented pre-Phase-6)
3. Week-0/Week-1 closure records / task register docs (if they exist)
4. Guardrails specification document (to verify G1-G8 requirements)
5. UI/UX design specifications (to verify planned UI deliverables)
6. Legacy parity documentation (to verify reuse requirements)

---

## Review 2: Phase-6 Complete Scope & Task Summary v1.4

### Document Metadata
- **Document:** Phase-6 Complete Scope & Task Summary v1.4
- **Review Date:** 2025-01-27
- **Reviewer:** Reconciliation Analysis
- **Review Type:** Scope Confirmation & Gap Validation
- **Scope:** Weeks 0-4 Scope Expansion & Task Atomicity

### Key Findings Summary

#### ✅ Critical Confirmation
1. **No New Scope Added:** Document 02/06 does NOT add new scope beyond Document 01/06
   - Expands tasks into atomic, testable units
   - Confirms which items were ALWAYS planned for Weeks 0-4
   - Validates that gaps identified in Review 1 are REAL gaps, not misplacement

2. **No False Alarms:** After reading Doc 02/06, none of the previously raised alarms are invalidated
   - All "missing" items listed for Weeks 0-4 are explicitly listed in this doc under Weeks 0-4
   - No tasks were actually planned for Week-5+ but wrongly assumed missing
   - ✅ Review 1 alarm instinct was CORRECT

3. **Gap Classification Framework:** Doc 02/06 enables cleaner gap classification into four types:
   - **DOC-ONLY:** Planned doc but code exists → Write doc only
   - **UI-MISSING:** Backend exists, UI missing → UI sprint
   - **ENGINE-MISSING:** Core logic not implemented → Backend sprint
   - **VERIFY-MISSING:** Feature exists but no proof → Tests + evidence

### Critical Alarms Identified

| Alarm ID | Category | Severity | Description | Status After Review 2 |
|----------|----------|----------|-------------|----------------------|
| 🔴 ALARM-SETUP | Week-0 Setup | CRITICAL | Setup docs/gates missing (task register, QCD contract, D0 checklist) | ✅ CONFIRMED (Final) |
| 🔴 ALARM-CORE-CRUD | Week-1/2 UI | CRITICAL | Add Panel/Feeder/BOM/Item flows missing | ✅ CONFIRMED (Final) |
| 🔴 ALARM-GUARDRAILS | Week-2-4 Validation | CRITICAL | Guardrails G1-G8 runtime + tests missing | ✅ CONFIRMED (Final) |
| 🔴 ALARM-MASTER-BOM | Track A-R Reuse | CRITICAL | Master BOM apply + post-reuse editability missing | ✅ CONFIRMED (Final) |
| 🔴 ALARM-PRICING-UX | Week-3 UI | CRITICAL | RateSource pricing UX missing | ✅ CONFIRMED (Final) |
| 🔴 ALARM-RESOLUTION-UX | Week-4 UI | CRITICAL | L0→L1→L2 resolution UX missing | ✅ CONFIRMED (Final) |

**All alarms from Review 1 are CONFIRMED as TRUE GAPS (not thread artifacts).**

### Detailed Work Matrix (Weeks 0-4) - Updated & Cleaned

#### Week-0 — Entry Gate & Setup (Track E + Setup)

| Task ID | Planned in Doc | Evidence Found | Status | Alarm |
|---------|----------------|----------------|--------|-------|
| P6-ENTRY-001..005 | Yes | Claimed passed, no doc yet | ⚠️ PARTIAL | 🟡 |
| P6-ENTRY-006 (Naming) | Yes | None | ❌ MISSING | 🔴 |
| P6-SETUP-001 (Structure) | Yes | Partial (folders exist, no spec) | ⚠️ PARTIAL | 🟡 |
| P6-SETUP-002 (Review Phase-5 deliverables) | Yes | None | ❌ MISSING | 🟠 |
| P6-SETUP-003 (Task register) | Yes | None | ❌ MISSING | 🔴 |
| P6-SETUP-005 (QCD contract doc) | Yes | None | ❌ MISSING | 🔴 |
| P6-SETUP-006 (D0 checklist doc) | Yes | None | ❌ MISSING | 🔴 |
| P6-SETUP-007 (Review Phase-5 for implementation obligations) | Yes | None | ❌ MISSING | 🟠 |
| P6-DB-002..004 | Yes | Schema + drift checks | ✅ DONE | — |
| P6-DB-005 (Cost template seed data) | Yes | Not proven | ❌ MISSING | 🔴 |

**Week-0 Plan Status:** ⚠️ PARTIAL (cannot be closed per plan)

---

#### Week-1 — Quotation & Panel UI (Track A)

| Task ID | Planned | Evidence | Status | Alarm |
|---------|---------|----------|--------|-------|
| P6-UI-001 (Design) | Yes | None | ❌ MISSING | 🟠 |
| P6-UI-002 (Overview UI) | Yes | Basic view only | ⚠️ PARTIAL | 🟡 |
| P6-UI-005 (Add Panel) | Yes | STUB only | ❌ MISSING | 🔴 |
| P6-UI-001A (Customer snapshot) | Yes | Not proven | ❌ MISSING | 🔴 |
| P6-UI-001B (customer_id nullable) | Yes | Not proven | ❌ MISSING | 🟠 |

**Week-1 Plan Status:** ⚠️ PARTIAL (read-only ≠ complete)

---

#### Week-2 — Feeder/BOM UI + Guardrails Start (Track A + Track E)

**Track A (UI):**

| Task ID | Planned | Evidence | Status | Alarm |
|---------|---------|----------|--------|-------|
| P6-UI-007 (BOM tree UI) | Yes | None | ❌ MISSING | 🔴 |
| P6-UI-008 (Add Feeder) | Yes | None | ❌ MISSING | 🔴 |
| P6-UI-009 (Add BOM) | Yes | None | ❌ MISSING | 🔴 |
| P6-UI-010 (Item list) | Yes | Partial | ⚠️ PARTIAL | 🟡 |
| P6-UI-010A (Qty persistence verify) | Yes | None | ❌ MISSING | 🔴 |

**Track E (Guardrails):**

| Task ID | Planned | Evidence | Status | Alarm |
|---------|---------|----------|--------|-------|
| P6-VAL-001..004 (G1–G8 + tests) | Yes | None | ❌ MISSING | 🔴 |

**Week-2 Plan Status:** ⚠️ PARTIAL (critical gaps remain)

---

#### Week-2.5–4 — Reuse & Legacy Parity (Track A-R)

| Task ID | Planned | Evidence | Status | Alarm |
|---------|---------|----------|--------|-------|
| REUSE-001..004 (copy flows) | Yes | APIs + tests | ✅ DONE | — |
| REUSE-005 (Apply Master BOM) | Yes | None | ❌ MISSING | 🔴 |
| REUSE-006 (Post-reuse editability verify) | Yes | None | ❌ MISSING | 🔴 |
| REUSE-007 (Guardrails after reuse) | Yes | None | ❌ MISSING | 🔴 |

**Track A-R Status:** ⚠️ PARTIAL

---

#### Week-3 — Pricing Resolution UX (Track A)

| Task ID | Planned | Evidence | Status | Alarm |
|---------|---------|----------|--------|-------|
| P6-UI-011..016 (Pricing UX) | Yes | None | ❌ MISSING | 🔴 |

**Week-3 Plan Status:** ⚠️ PARTIAL

---

#### Week-4 — Resolution UX vs Read-Only Hardening

| Scope | Planned | Evidence | Status |
|-------|---------|----------|--------|
| L0→L1→L2 Resolution UX (UI) | Yes | None | ❌ MISSING |
| Resolution constraints + taxonomy | Yes | None | ❌ MISSING |
| Read-only state/integrity/helpers | Not core UX | Evidence pack | ✅ DONE |

**Week-4 Status (Corrected):**
- **Resolution UX:** ❌ NOT DONE
- **Read-only governance hardening:** ✅ DONE
- **Overall Week-4 per plan:** ⚠️ PARTIAL

**This resolves the "Week-4 closed vs not closed" confusion cleanly.**

---

### Review 2 Conclusions

#### Key Validations

1. **Review 1 Accuracy Confirmed:** All gaps identified in Review 1 are validated as REAL gaps
   - No false alarms
   - All missing items were explicitly planned for Weeks 0-4
   - No scope misplacement discovered

2. **Gap Classification Framework Established:** Four gap types identified to reduce rework:
   - DOC-ONLY → Write doc only
   - UI-MISSING → UI sprint
   - ENGINE-MISSING → Backend sprint
   - VERIFY-MISSING → Tests + evidence

3. **Week-4 Status Clarified:**
   - Resolution UX (planned): ❌ NOT DONE
   - Read-only hardening (actual): ✅ DONE
   - Overall Week-4: ⚠️ PARTIAL per plan

#### Status Corrections (Final for Weeks 0-4)

1. **Week-0 Status:** ⚠️ PARTIAL (cannot be closed per plan)
2. **Week-1 Status:** ⚠️ PARTIAL (read-only ≠ complete)
3. **Week-2 Status:** ⚠️ PARTIAL (critical gaps remain)
4. **Week-3 Status:** ⚠️ PARTIAL
5. **Week-4 Status:** ⚠️ PARTIAL (resolution UX missing; read-only hardening complete but separate)

#### Alarms Finalized

All 6 critical alarms from Review 1 are **CONFIRMED as FINAL** for Weeks 0-4:
- ✅ ALARM-SETUP: CONFIRMED
- ✅ ALARM-CORE-CRUD: CONFIRMED
- ✅ ALARM-GUARDRAILS: CONFIRMED
- ✅ ALARM-MASTER-BOM: CONFIRMED
- ✅ ALARM-PRICING-UX: CONFIRMED
- ✅ ALARM-RESOLUTION-UX: CONFIRMED

These are TRUE GAPS, not thread artifacts.

#### Next Steps Recommendations

1. **Freeze "Reconciled Truth":**
   - Weeks 0-3 = PARTIAL
   - Week-4 = Read-only DONE, UX PENDING
   - Phase-6 = OPEN

2. **Create PHASE6_GAP_REGISTER_W0_W4.md:**
   - Derived directly from confirmed alarms
   - Single source of truth for gaps

3. **Begin Week-wise Detailing:**
   - Start with Week-1 (Add Panel + Customer snapshot)
   - NOT Week-5 yet (Week-5 depends on Week-1/2 closure)

---

## Review 3: Phase-6 Execution Plan Revision Summary v1.2

### Document Metadata
- **Document:** Phase-6 Execution Plan Revision Summary v1.2
- **Review Date:** 2025-01-27
- **Reviewer:** Reconciliation Analysis
- **Review Type:** Compliance Obligations & Alarm Prioritization
- **Scope:** Phase-5 Compliance Requirements vs Phase-6 Planned Tasks

### Key Findings Summary

#### ✅ Critical Insight: Compliance vs Optional Classification

This document explains what was added to correct the original Phase-6 plan based on Phase-5 obligations. It distinguishes between:
- **Compliance-Critical Items:** Non-negotiable Phase-5 compliance obligations (must exist for Phase-6 sign-off)
- **Optional/Deferable Items:** Can be deferred if properly documented

#### ✅ Compliance-Critical Items (Mandatory for Phase-5 Compliance)

These are NOT "nice-to-have UI" - they are required for Phase-5 compliance:

1. **Database Track E (Weeks 0-1):** Mandatory
2. **Guardrails G1-G8 (Week 3):** Mandatory runtime enforcement + tests
3. **BOM tracking runtime behavior (Week 2):** Mandatory
4. **Multi-SKU linkage (Week 4):** Mandatory
5. **Customer snapshot handling (Week 1):** Mandatory
6. **Resolution constraints enforcement + taxonomy mapping (Week 4):** Mandatory
7. **Locking scope verification (Week 5):** Mandatory
8. **Discount Editor (Week 6):** Mandatory

#### ✅ Optional/Deferable Items

- **Track F (API contracts):** Optional/deferable to Phase-7, but requires defer memo at closure
  - Absence of Track F code is NOT an alarm unless defer memo cannot be located near closure
  - Marked as "DEFER-ALLOWED (needs memo at closure)"

### Compliance Alarms Identified (Upgraded from Regular Alarms)

The following gaps were already identified, but Doc 03/06 upgrades them from "missing planned tasks" → **Phase-5 Compliance Blockers**:

| Obligation | Task IDs | Week | Status | Alarm Level |
|------------|----------|------|--------|-------------|
| Customer snapshot handling | P6-QUO-001A/B (same as P6-UI-001A/B) | W1 | ❌ Missing evidence | 🔴 **COMPLIANCE** |
| BOM tracking runtime | P6-BOM-TRACK-001..003 | W2 | ❌ Missing evidence | 🔴 **COMPLIANCE** |
| Guardrails runtime + tests | P6-VAL-001..004 | W3 | ❌ Missing evidence | 🔴 **COMPLIANCE** |
| Multi-SKU linkage | P6-SKU-001..003 | W4 | ❌ Missing evidence | 🔴 **COMPLIANCE** |
| Resolution constraints + taxonomy | P6-RES-023..024 | W4 | ❌ Missing evidence | 🔴 **COMPLIANCE** |
| Naming/Module rules | P6-ENTRY-006, P6-SETUP-004/005 | W0 | ❌ Missing evidence | 🟠 (becomes 🔴 if governance requires) |

**Interpretation:** Even if UI is delayed, these compliance items must exist (at least backend enforcement + tests + docs where mandated), or Phase-6 cannot be signed off.

### Track F (API Contracts) Handling

**Status:** Optional/Deferable (requires defer memo at closure)

**Matrix Treatment:**
- Until Week-12 closure, Track F tasks are marked: **"DEFER-ALLOWED (needs memo at closure)"**
- If defer memo cannot be located near closure → 🔴 ALARM at that time
- **No premature alarms** for Track F absence

### Detailed Compliance Matrix (Weeks 0-4)

#### Week-0 Compliance Items

| Task ID | Compliance Obligation | Evidence Status | Alarm Level |
|---------|----------------------|-----------------|-------------|
| P6-ENTRY-006 | Naming convention compliance | ❌ Missing | 🟠 → 🔴 (if governance requires) |
| P6-SETUP-004/005 | Module boundaries + Naming rules | ❌ Missing | 🟠 → 🔴 (if governance requires) |

#### Week-1 Compliance Items

| Task ID | Compliance Obligation | Evidence Status | Alarm Level |
|---------|----------------------|-----------------|-------------|
| P6-QUO-001A/B (P6-UI-001A/B) | Customer snapshot handling (mandatory) | ❌ Missing | 🔴 **COMPLIANCE** |

#### Week-2 Compliance Items

| Task ID | Compliance Obligation | Evidence Status | Alarm Level |
|---------|----------------------|-----------------|-------------|
| P6-BOM-TRACK-001..003 | BOM tracking runtime behavior (mandatory) | ❌ Missing | 🔴 **COMPLIANCE** |

#### Week-3 Compliance Items

| Task ID | Compliance Obligation | Evidence Status | Alarm Level |
|---------|----------------------|-----------------|-------------|
| P6-VAL-001..004 | Guardrails G1-G8 runtime + tests (mandatory) | ❌ Missing | 🔴 **COMPLIANCE** |

#### Week-4 Compliance Items

| Task ID | Compliance Obligation | Evidence Status | Alarm Level |
|---------|----------------------|-----------------|-------------|
| P6-SKU-001..003 | Multi-SKU linkage (mandatory) | ❌ Missing | 🔴 **COMPLIANCE** |
| P6-RES-023..024 | Resolution constraints + taxonomy mapping (mandatory) | ❌ Missing | 🔴 **COMPLIANCE** |

### Review 3 Conclusions

#### Key Validations

1. **Compliance Obligations Clarified:** Document distinguishes mandatory Phase-5 compliance items from optional features
2. **Alarm Prioritization:** Several gaps upgraded from "missing planned tasks" to "Phase-5 Compliance Blockers"
3. **Track F Clarification:** API contracts track is optional/deferable (not an alarm unless defer memo missing at closure)

#### Status Corrections Required (Compliance-Based)

Corrected labels for Weeks 0-4 (as of Review 3):

1. **Week-0:** ⚠️ PARTIAL (docs/gates missing; naming/module rules may be compliance-critical)
2. **Week-1:** ⚠️ PARTIAL (customer snapshot COMPLIANCE item missing + add panel missing)
3. **Week-2:** ⚠️ PARTIAL (BOM tracking COMPLIANCE item missing; CRUD missing)
4. **Week-3:** ⚠️ PARTIAL (guardrails COMPLIANCE items missing; pricing UX missing)
5. **Week-4:** ⚠️ PARTIAL (multi-SKU + resolution constraints COMPLIANCE items missing; resolution UX missing)
6. **Week-4 Day-1..4 read-only hardening:** ✅ DONE (separately evidenced)

This resolves the "thread shift confusion" - now we have the plan basis to correct status labels with compliance obligations in mind.

#### Critical Risk Updated

**Compliance Risk:** If we proceed to Week-5+ without implementing compliance obligations (guardrails, tracking, snapshots), integration will collapse later AND Phase-6 cannot be signed off.

#### Next Steps Recommendations

**Recommended Documents for Review 4-6:**
1. Phase-6 Kickoff Charter (defines acceptance/exit gates and allowed defers)
2. Phase-5 Detailed Working Record Gap Analysis (tells what must be implemented for compliance)
3. Week-0 closure record / Entry Gate checklist (might clear multiple Week-0 alarms)
4. Track F defer memo (if exists, confirms Track F deferral)
5. Compliance verification documentation (if any exists)

---

## Review 4: Phase-6 Execution Plan (Corrected Version Summary v1.2)

### Document Metadata
- **Document:** Phase-6 Execution Plan (Corrected Version Summary v1.2)
- **Review Date:** 2025-01-27
- **Reviewer:** Reconciliation Analysis
- **Review Type:** Final Baseline Reconciliation & Track Structure Clarification
- **Scope:** Corrected Track Structure (D0, E re-org) & Final Week 0-4 Status

### Key Findings Summary

#### ✅ Critical Clarifications (Removes Ambiguity)

This document provides the final baseline reconciliation by:

1. **Track D0 is now explicit and engine-first:**
   - QCD/QCA foundations are separate from UI/reporting
   - Cost templates + sheets tables are Track D0 (not Track E)

2. **All Phase-5 obligations are centralized in Track E:**
   - Guardrails, BOM tracking, multi-SKU, snapshot, resolution constraints are NOT UI scope
   - These are engine/compliance items (Track E), not UI items (Track A)

3. **Track A = UI only:**
   - Track A gaps are pure UI gaps, not engine gaps
   - Clear separation between UI work and engine work

4. **Week-4 confusion resolved:**
   - Week-4 UI resolution ≠ Week-4 read-only governance hardening
   - Week-4 evidence pack is valid but covers a different slice (governance hardening)
   - Week-4 UI resolution work is still missing

This lets us shrink false gaps and relabel weeks correctly.

#### ✅ Final Corrected Week Status (Authoritative)

| Week | Status | Reason |
|------|--------|--------|
| Week-0 | ⚠️ PARTIAL | Entry gate logic ok, setup + gate docs missing |
| Week-1 | ⚠️ PARTIAL | Read APIs exist; snapshot + add panel missing |
| Week-2 | ⚠️ PARTIAL | Reuse copy ok; CRUD + BOM tracking missing |
| Week-3 | ⚠️ PARTIAL | Cost adders backend ok; guardrails + pricing UX missing |
| Week-4 | ⚠️ PARTIAL | Read-only governance done; resolution UX + multi-SKU missing |

**Important:**
- ✅ No week before Week-5 is fully closed per corrected plan
- ✅ Week-4 "Day-1..4" closure remains valid as a sub-deliverable (governance hardening)

### Final Work Matrix (Weeks 0-4) - Corrected

#### Week-0 — Entry Gate & Setup (Track E)

| Task | Planned | Evidence | Status | Alarm |
|------|---------|----------|--------|-------|
| Entry gate checks (P6-ENTRY-001..005) | Yes | Claimed, no doc | ⚠️ PARTIAL | 🟡 |
| Naming conventions (P6-ENTRY-006) | Yes | None | ❌ MISSING | 🔴 |
| Phase-6 task register (P6-SETUP-003) | Yes | None | ❌ MISSING | 🔴 |
| Review Phase-5 deliverables (P6-SETUP-002) | Yes | None | ❌ MISSING | 🟠 |
| Costing manual structure (P6-SETUP-004) | Yes | None | ❌ MISSING | 🔴 |
| QCD contract freeze doc (P6-SETUP-005) | Yes | None | ❌ MISSING | 🔴 |
| D0 gate checklist doc (P6-SETUP-006) | Yes | None | ❌ MISSING | 🔴 |
| Review Phase-5 for implementation obligations (P6-SETUP-007) | Yes | None | ❌ MISSING | 🟠 |
| DB schema + parity (P6-DB-002..004) | Yes | Drift checks exist | ✅ DONE | — |
| Cost template seed data (P6-DB-005) | Yes | Not proven | ❌ MISSING | 🔴 |

**Week-0 Status:** ⚠️ PARTIAL

---

#### Week-1 — Quotation & Panel UI (Track A) + Snapshot (Track E)

| Task | Track | Status | Alarm |
|------|-------|--------|-------|
| Quotation overview UI | A | ⚠️ PARTIAL | 🟡 |
| Add Panel (P6-UI-005) | A | ❌ MISSING | 🔴 |
| customer_name_snapshot | E | ❌ MISSING | 🔴 |
| customer_id nullable | E | ❌ MISSING | 🟠 |

**Week-1 Status:** ⚠️ PARTIAL (core CRUD missing)

---

#### Week-2 — Feeder/BOM UI + Tracking + Reuse (Track A, A-R, E)

**What is DONE:**
- ✅ Quotation / Panel / Feeder / BOM copy APIs
- ✅ Copy-never-link invariants tested

**What is MISSING:**

| Task | Track | Status | Alarm |
|------|-------|--------|-------|
| Add Feeder | A | ❌ MISSING | 🔴 |
| Add BOM | A | ❌ MISSING | 🔴 |
| Add Item | A | ❌ MISSING | 🔴 |
| BOM tree UI | A | ❌ MISSING | 🔴 |
| Quantity persistence verification | E | ❌ MISSING | 🔴 |
| BOM tracking runtime fields | E | ❌ MISSING | 🔴 |
| Master BOM apply | A-R | ❌ MISSING | 🔴 |

**Week-2 Status:** ⚠️ PARTIAL (compliance gaps remain)

---

#### Week-3 — Guardrails + Cost Engine + Pricing UX (Track E, D0, A)

**What is DONE:**
- ✅ Cost adders backend (QCA)
- ✅ Cost summary APIs + tests

**What is MISSING (now clearly Track-E, not Track-A confusion):**

| Task | Track | Status | Alarm |
|------|-------|--------|-------|
| Guardrails G1-G8 runtime | E | ❌ MISSING | 🔴 |
| Guardrail test suite | E | ❌ MISSING | 🔴 |
| Pricing UX (RateSource etc.) | A | ❌ MISSING | 🔴 |
| Cost templates + sheets tables | D0 | ❌ MISSING | 🔴 |
| QCD generator + JSON | D0 | ❌ MISSING | 🔴 |

**Week-3 Status:** ⚠️ PARTIAL

---

#### Week-4 — Resolution UX + Governance (Track A, E, A-R)

**What is DONE:**
- ✅ Read-only lifecycle visibility
- ✅ Integrity hash
- ✅ Render helpers
- ✅ Evidence pack
- ✅ Consolidated runners

**What is MISSING per corrected plan:**

| Task | Track | Status | Alarm |
|------|-------|--------|-------|
| L0→L1→L2 resolution UI | A | ❌ MISSING | 🔴 |
| Resolution constraints enforcement | E | ❌ MISSING | 🔴 |
| Error taxonomy mapping | E | ❌ MISSING | 🔴 |
| Multi-SKU linkage | E | ❌ MISSING | 🔴 |
| Post-reuse guardrail validation | A-R / E | ❌ MISSING | 🔴 |

**Week-4 Status:** ⚠️ PARTIAL (UI + canon enforcement pending)

---

### Review 4 Conclusions

#### Key Validations

1. **Track Structure Clarified:**
   - Track D0 = Engine-first (QCD/QCA foundations, templates, sheets)
   - Track E = Phase-5 compliance obligations (guardrails, tracking, snapshots, constraints)
   - Track A = UI only (pure UI gaps, not engine gaps)

2. **Week-4 Confusion Resolved:**
   - Week-4 UI resolution ≠ Week-4 read-only governance hardening
   - Week-4 evidence pack is valid (governance hardening slice)
   - Week-4 UI resolution work is still missing

3. **False Gaps Eliminated:**
   - All gaps are now clearly classified by track
   - No confusion between UI gaps and engine gaps
   - Clear separation enables accurate planning

#### Final Alarm Status (Authoritative)

After Doc 04/06, these alarms are FINAL and legitimate:

**🔴 Compliance ALARMS (must be addressed before Phase-6 close):**
- Entry-gate setup docs (Week-0)
- Customer snapshot handling (Week-1)
- CRUD (Add Panel/Feeder/BOM/Item) (Weeks 1–2)
- Guardrails G1-G8 runtime + tests (Week-3)
- QCD generator + D0 Gate (Weeks 3–6)
- BOM tracking runtime behavior (Week-2)
- Multi-SKU linkage (Week-4)
- Resolution constraints enforcement (Week-4)
- Master BOM apply + post-reuse validation (Weeks 2–4)

**🟡 No false alarms remain.**
Everything missing is explicitly planned in the corrected baseline.

#### Status Corrections (Final for Weeks 0-4)

1. **Week-0:** ⚠️ PARTIAL (entry gate logic ok, setup + gate docs missing)
2. **Week-1:** ⚠️ PARTIAL (read APIs exist; snapshot + add panel missing)
3. **Week-2:** ⚠️ PARTIAL (reuse copy ok; CRUD + BOM tracking missing)
4. **Week-3:** ⚠️ PARTIAL (cost adders backend ok; guardrails + pricing UX missing)
5. **Week-4:** ⚠️ PARTIAL (read-only governance done; resolution UX + multi-SKU missing)

**Critical Note:** No week before Week-5 is fully closed per corrected plan.

#### Next Steps (Ready)

Now that all four baseline documents are reconciled:

**We are READY to:**
1. Freeze "Phase-6 Reconciled Truth"
2. Generate: PHASE6_GAP_REGISTER_W0_W4.md
3. Then detail weeks one by one, starting from Week-1 (not Week-5)

**We should NOT:**
- Jump to Week-5
- Assume Week-0..4 are "closed"
- Re-audit again

---

## Review 5: Legacy Parity Verification Checklist v1.0 (2025-01-27)

### Document Metadata
- **Document:** Legacy Parity Verification Checklist v1.0 (2025-01-27)
- **Review Date:** 2025-01-27
- **Reviewer:** Reconciliation Analysis
- **Review Type:** Parity Evidence Layer & Verification Mapping
- **Scope:** Week-8.5 Gate Input & Parity Verification Requirements

### Key Findings Summary

#### ✅ Critical Insight: Parity Verification Layer

This document introduces an additional dimension to the matrix:
- **Parity Verification Rows:** Each checklist item maps to Phase-6 Task IDs with required evidence types
- **Week-8.5 Gate Input:** This checklist defines what "parity done" actually means
- **Parity Evidence Requirements:** UI flow, API endpoint, test evidence required for each parity item

#### ✅ What's Already Partially Covered (Backend Exists)

Even though many UI items are missing, we already have:

**Reuse APIs exist (partial parity coverage):**
- ✅ A3 Copy old quotation and modify → P6-UI-REUSE-001 (backend exists)
- ✅ B2 Reuse panel → REUSE-002 (backend exists)
- ✅ B4 Reuse feeder → REUSE-003 (backend exists)
- ✅ B6 Reuse BOM → REUSE-004 (backend exists)

**Current Status for Reuse Items:**
- ✅ API capability exists
- ❌ Parity not verified until UI + post-reuse edit validation exists
- **Status:** Implemented (backend), Verification pending

#### ⚠️ Parity Blockers (Match Current Alarms)

These parity items directly match our current alarms and are parity-critical:

| Parity Ref | Checklist Item | Task ID | Current Status | Alarm |
|------------|----------------|---------|----------------|-------|
| B1 | Add panel | P6-UI-005 | ❌ Missing | 🔴 Blocker |
| B3 | Add feeder | P6-UI-008 | ❌ Missing | 🔴 Blocker |
| B5 | Add BOM | P6-UI-009 | ❌ Missing | 🔴 Blocker |
| C1 | Add items | P6-UI-010 | ⚠️ Partial | 🔴 Blocker |
| C4 | Edit reused items | REUSE-006 | ❌ Missing | 🔴 Blocker |
| C5 | Tracking fields | BOM-TRACK-001/002 | ❌ Missing | 🔴 Blocker |
| D1–D3 | Pricing | UI-012..015 | ❌ Missing | 🔴 Blocker |
| D4 | Discount editor | DISC-001..004 | ❌ Missing | 🔴 Blocker |
| E1–E5 | EffectiveQty | COST-D0-001 | ❌ Missing | 🔴 Blocker |
| F1–F6 | Catalog onboarding | CAT-005..006 | ❌ Missing | 🔴 Blocker |
| H1–H3 | Audit / locking | OPS-007/008, UI-025 | ⏳ Pending | 🔴 Blocker |
| I1 | Customer snapshot | UI-001A/001B | ❌ Missing | 🔴 Blocker |
| J1–J3 | Catalog views | CAT-006 | ❌ Missing | 🔴 Blocker |

**Critical Confirmation:** Week 0–4 gaps are not "extra"; they are **parity-critical**. Week-8.5 gate cannot pass without closing these blockers.

### New Alarm Type: Parity Evidence

#### 🔴 ALARM-PARITY-EVIDENCE

**Definition:** If a reuse API exists but lacks:
- UI action
- Editability verification
- Guardrail validation after reuse

Then parity gate will fail even though backend exists.

**Current Examples:**
- REUSE-001..004 are implemented (backend), but:
- REUSE-006 (post-reuse editability) is missing → parity failure later
- REUSE-007 (guardrail validation after reuse) is missing → parity failure later

#### New Parity Alarms Identified

| Alarm ID | Task ID | Parity Ref | Description | Status |
|----------|---------|------------|-------------|--------|
| 🔴 ALARM-PARITY-EDITABILITY | REUSE-006 | C4 | Post-reuse editability verification missing | OPEN |
| 🔴 ALARM-PARITY-GUARDRAILS | REUSE-007 | C5 (partial) | Guardrail validation after reuse missing | OPEN |

### Parity Verification Matrix (Selected Items - Weeks 0-4)

| Task ID | Week | Track | Planned | Implemented | Evidence | Parity Ref | Parity Evidence Required | Parity Status |
|---------|------|-------|---------|-------------|----------|------------|-------------------------|---------------|
| P6-UI-REUSE-001 | W2.5 | A-R | Yes | ✅ API exists | tests/reuse | A3 | UI flow + editability | 🟡 Backend only |
| REUSE-002 | W2.5 | A-R | Yes | ✅ API exists | tests/reuse | B2 | UI flow + editability | 🟡 Backend only |
| REUSE-003 | W2.5 | A-R | Yes | ✅ API exists | tests/reuse | B4 | UI flow + editability | 🟡 Backend only |
| REUSE-004 | W2.5 | A-R | Yes | ✅ API exists | tests/reuse | B6 | UI flow + editability | 🟡 Backend only |
| REUSE-006 | W2.5-4 | A-R | Yes | ❌ Missing | none | C4 | Editability verification | 🔴 Blocker |
| REUSE-007 | W2.5-4 | A-R/E | Yes | ❌ Missing | none | C5 (partial) | Guardrail validation | 🔴 Blocker |
| P6-UI-005 | W1 | A | Yes | ❌ Missing | none | B1 | UI flow + API | 🔴 Blocker |
| P6-UI-008 | W2 | A | Yes | ❌ Missing | none | B3 | UI flow + API | 🔴 Blocker |
| P6-UI-009 | W2 | A | Yes | ❌ Missing | none | B5 | UI flow + API | 🔴 Blocker |
| P6-UI-010 | W2 | A | Yes | ⚠️ Partial | partial | C1 | UI flow + API | 🔴 Blocker |
| BOM-TRACK-001/002 | W2 | E | Yes | ❌ Missing | none | C5 | Tracking fields | 🔴 Blocker |
| P6-UI-001A/001B | W1 | E | Yes | ❌ Missing | none | I1 | Customer snapshot | 🔴 Blocker |

### Review 5 Conclusions

#### Key Validations

1. **Parity Evidence Layer Established:**
   - Parity verification requirements now mapped to Phase-6 tasks
   - Workflow proof required, not just endpoints
   - Week-8.5 gate requirements clarified

2. **Backend vs Parity Gap Identified:**
   - Reuse APIs (REUSE-001..004) exist but parity not verified
   - Requires UI + editability + guardrail validation for parity
   - Current status: Implemented (backend), Verification pending

3. **Parity Blockers Confirmed:**
   - All Week 0–4 gaps are parity-critical (not optional)
   - Week-8.5 gate cannot pass without closing these blockers
   - Gap register must include parity verification requirements

#### New Alarms Added

- 🔴 ALARM-PARITY-EDITABILITY (REUSE-006): Post-reuse editability verification missing
- 🔴 ALARM-PARITY-GUARDRAILS (REUSE-007): Guardrail validation after reuse missing

#### Critical Risk

**Parity Verification Risk:** Thinking "reuse APIs done" equals "legacy parity done" is dangerous without editability + guardrail verification. Parity requires workflow proof, not just endpoints.

#### Next Steps Recommendations

**Recommended Documents for Review 6:**
1. Phase-6 Kickoff Charter (defines acceptance/exit gates and any allowed defers)
2. Phase-5 Error Taxonomy doc ref or any error envelope spec
3. Any existing Week-0/Week-1 closure record in repo (can clear many Week-0 alarms quickly)

---

## Review 6: Phase-6 Legacy Parity Addition Summary v1.3

### Document Metadata
- **Document:** Phase-6 Legacy Parity Addition Summary v1.3
- **Review Date:** 2025-01-27
- **Reviewer:** Reconciliation Analysis
- **Review Type:** Track A-R Canonical Confirmation & Final Reconciliation Lock
- **Scope:** Track A-R Obligations & Legacy Parity Gate Requirements

### Key Findings Summary

#### ✅ Critical Confirmations (Locks Reconciliation)

This document completes the reconciliation by confirming three critical points:

**A. Track A-R is now CANONICAL:**
- Reuse & Legacy Parity is NOT an enhancement
- It is a Phase-6 execution obligation
- Failure to complete Track A-R = Phase-6 cannot close
- This validates all earlier ALARM-PARITY flags

**B. Reuse is not just "copy APIs":**
- Reuse is complete only when:
  - Copied content is editable
  - Guardrails apply
  - UX flows exist
- Backend copy endpoints alone ≠ parity
- UI + editability + guardrail validation are mandatory
- This exactly matches the gap we already identified

**C. Legacy Parity Gate (Week 8.5) is HARD:**
- This is NOT a checklist for comfort
- It is a BLOCKING gate
- Phase-6 cannot proceed to Integration unless all legacy parity items are verified
- Any missing item in the checklist = future hard stop, not a soft TODO

#### ✅ Reuse Workflows Clarified (Canonical Paths)

Doc 06/06 clarifies the canonical reuse paths, which we must use later when designing UI:

**Path A — Reuse entire quotation**
**Path B — Create new quotation + reuse building blocks**
**Path C — Template-first (Master BOM)**

**Critical Implication:**
- Add Panel / Add Feeder / Add BOM / Add Item are NOT optional CRUD
- They are required to support Path B and Path C
- So CRUD gaps (Week-1/2) are parity-blocking, not just usability gaps

### Track A-R Final Status Matrix (After Doc 06/06)

| Task ID | Planned | Evidence Today | Status | Alarm |
|---------|---------|----------------|--------|-------|
| P6-UI-REUSE-001 (Copy quotation) | Yes | API + tests | 🟡 Backend-only | 🔴 PARITY |
| P6-UI-REUSE-002 (Copy panel) | Yes | API + tests | 🟡 Backend-only | 🔴 PARITY |
| P6-UI-REUSE-003 (Copy feeder) | Yes | API + tests | 🟡 Backend-only | 🔴 PARITY |
| P6-UI-REUSE-004 (Copy BOM) | Yes | API + tests | 🟡 Backend-only | 🔴 PARITY |
| P6-UI-REUSE-005 (Apply Master BOM) | Yes | None | ❌ Missing | 🔴 PARITY |
| P6-UI-REUSE-006 (Post-reuse editability) | Yes | None | ❌ Missing | 🔴 PARITY |
| P6-UI-REUSE-007 (Guardrails after reuse) | Yes | None | ❌ Missing | 🔴 PARITY |

**Track A-R Conclusion:** PARTIAL with compliance blockers (cannot close Phase-6 without completion)

### Review 6 Conclusions

#### Key Validations

1. **Track A-R Canonical Status Confirmed:**
   - Track A-R is NOT optional
   - It is a Phase-6 execution obligation
   - Failure to complete = Phase-6 cannot close

2. **Reuse Completeness Definition Locked:**
   - Backend APIs alone ≠ parity
   - Requires UI + editability + guardrail validation
   - Matches gaps already identified

3. **Legacy Parity Gate is Hard Blocking:**
   - Week-8.5 gate is mandatory
   - All parity items must be verified
   - Missing items = hard stop, not soft TODO

4. **Reuse Workflows Canonical:**
   - Path A: Reuse entire quotation
   - Path B: Create new + reuse building blocks
   - Path C: Template-first (Master BOM)
   - CRUD gaps block Path B and Path C

#### Final Alarm Status (After All 6 Documents)

After processing all six documents, the following alarms are now fully confirmed:

**🔴 COMPLIANCE & PARITY ALARMS (cannot be ignored):**

1. **Week-0 Setup & Gates:**
   - Task register
   - QCD contract freeze
   - D0 checklist
   - Naming / module rules

2. **Week-1 Core CRUD:**
   - Add Panel
   - Customer snapshot handling

3. **Week-2 Hierarchy Creation:**
   - Add Feeder / Add BOM / Add Item
   - BOM tree UI
   - Quantity persistence verification
   - BOM tracking runtime behavior

4. **Week-3 Engine & Guardrails:**
   - Guardrails G1–G8 runtime + tests
   - QCD generator + JSON
   - Cost templates & sheets (Track D0)
   - Pricing UX (RateSource, manual/fixed)

5. **Week-4 Resolution & Parity:**
   - L0→L1→L2 resolution UX
   - Resolution constraints enforcement
   - Error taxonomy mapping
   - Multi-SKU linkage
   - Master BOM apply
   - Post-reuse editability verification
   - Guardrails enforcement after reuse

**🟢 No false alarms remain.**
Everything missing is explicitly required by one or more of the six baseline documents.

#### Reconciliation Status: COMPLETE

**What we now have:**
- ✅ Complete baseline scope (Docs 01–06/06)
- ✅ Corrected track structure (A, A-R, B, C, D0, D, E)
- ✅ Authoritative gap truth for Weeks 0–4
- ✅ Parity checklist mapped to tasks
- ✅ Clear separation of UI vs Engine vs Canon obligations
- ✅ Track A-R canonical status confirmed

**This is the last reconciliation step.**
No more documents are required to understand Phase-6 scope.
Reconciliation is COMPLETE and LOCKED.

---

## Consolidated Alarms Register

### Compliance Alarms (🔴 COMPLIANCE) - Phase-5 Compliance Blockers

These are mandatory for Phase-6 sign-off (not optional UI features):

| Alarm ID | First Identified | Status | Resolution | Notes |
|----------|------------------|--------|------------|-------|
| ALARM-SETUP-DOCS | Review 1 | 🔴 **COMPLIANCE** | - | Entry-gate setup docs (Week-0) - Finalized in Review 4 |
| ALARM-CUSTOMER-SNAPSHOT | Review 1 (as P6-UI-001A/B) | 🔴 **COMPLIANCE** | - | Customer snapshot handling (P6-QUO-001A/B) - Upgraded to Compliance in Review 3, finalized in Review 4 |
| ALARM-CRUD | Review 1 | 🔴 **COMPLIANCE** | - | Add Panel/Feeder/BOM/Item (Weeks 1-2) - Finalized in Review 4 |
| ALARM-BOM-TRACKING | Review 3 | 🔴 **COMPLIANCE** | - | BOM tracking runtime behavior (P6-BOM-TRACK-001..003) - Mandatory Week-2 compliance, finalized in Review 4 |
| ALARM-GUARDRAILS | Review 1 | 🔴 **COMPLIANCE** | - | Guardrails G1-G8 runtime + tests (P6-VAL-001..004) - Upgraded to Compliance in Review 3, finalized in Review 4 |
| ALARM-QCD-D0-GATE | Review 4 | 🔴 **COMPLIANCE** | - | QCD generator + D0 Gate (Weeks 3-6) - Track D0 explicit, finalized in Review 4 |
| ALARM-MULTI-SKU | Review 3 | 🔴 **COMPLIANCE** | - | Multi-SKU linkage (P6-SKU-001..003) - Mandatory Week-4 compliance, finalized in Review 4 |
| ALARM-RESOLUTION-CONSTRAINTS | Review 1 (as part of ALARM-RESOLUTION-UX) | 🔴 **COMPLIANCE** | - | Resolution constraints + taxonomy (P6-RES-023..024) - Upgraded to Compliance in Review 3, finalized in Review 4 |
| ALARM-MASTER-BOM-REUSE | Review 1 | 🔴 **COMPLIANCE** | - | Master BOM apply + post-reuse validation (Weeks 2-4) - Finalized in Review 4, Track A-R confirmed canonical in Review 6 |

### Parity Alarms (🔴 PARITY) - Legacy Parity Blockers

These are mandatory for Week-8.5 gate pass (parity verification requirements):

| Alarm ID | First Identified | Status | Resolution | Notes |
|----------|------------------|--------|------------|-------|
| ALARM-PARITY-EDITABILITY | Review 5 | 🔴 **PARITY** | - | Post-reuse editability verification (REUSE-006, Parity C4) - Blocks Week-8.5 gate |
| ALARM-PARITY-GUARDRAILS | Review 5 | 🔴 **PARITY** | - | Guardrail validation after reuse (REUSE-007, Parity C5 partial) - Blocks Week-8.5 gate |

**Note:** Reuse APIs (REUSE-001..004) exist at backend but parity verification pending - requires UI + editability + guardrails for parity proof.

**Track A-R Status (After Review 6):** CANONICAL - Not optional, Phase-6 execution obligation. Failure to complete Track A-R = Phase-6 cannot close. Backend APIs alone ≠ parity (requires UI + editability + guardrail validation).

### Critical Alarms (🔴) - Functional Gaps (UI)

| Alarm ID | First Identified | Status | Resolution | Notes |
|----------|------------------|--------|------------|-------|
| ALARM-PRICING-UX | Review 1 | ✅ CONFIRMED (Final) | - | RateSource pricing UX (Track A) - Pure UI gap, finalized in Review 4 |
| ALARM-RESOLUTION-UX | Review 1 | ✅ CONFIRMED (Final) | - | L0→L1→L2 resolution UI (Track A) - Pure UI gap, separate from compliance constraints, finalized in Review 4 |

### High Priority Alarms (🟠)

| Alarm ID | First Identified | Status | Resolution | Notes |
|----------|------------------|--------|------------|-------|
| ALARM-NAMING-MODULE-RULES | Review 1 (as P6-ENTRY-006, P6-SETUP-004/005) | 🟠 (becomes 🔴 if governance requires) | - | Naming convention + module boundaries - May be compliance-critical depending on governance |

### Medium Priority Items (🟡)

| Item ID | First Identified | Status | Resolution | Notes |
|---------|------------------|--------|------------|-------|
| *To be populated as reviews progress* | - | - | - | - |

### Deferrable Items (DEFER-ALLOWED)

| Item ID | First Identified | Status | Resolution | Notes |
|---------|------------------|--------|------------|-------|
| Track F (API Contracts) | Review 3 | DEFER-ALLOWED | Needs defer memo at closure | Optional/deferable to Phase-7. Not an alarm unless defer memo missing at closure. |

---

## Consolidated Status Matrix (All Reviews)

### Week-by-Week Status (Consolidated)

| Week | Planned Scope | Evidence Status | Consolidated Status | Last Updated |
|------|---------------|-----------------|---------------------|--------------|
| Week-0 | Entry Gate & Setup | ⚠️ PARTIAL | ⚠️ PARTIAL (entry gate logic ok, setup + gate docs missing) | Review 4 |
| Week-1 | Quotation & Panel UI + Snapshot | ⚠️ PARTIAL | ⚠️ PARTIAL (read APIs exist; snapshot + add panel missing) | Review 4 |
| Week-2 | Feeder/BOM UI + Tracking + Reuse | ⚠️ PARTIAL | ⚠️ PARTIAL (reuse copy ok; CRUD + BOM tracking missing) | Review 4 |
| Week-3 | Guardrails + Cost Engine + Pricing UX | ⚠️ PARTIAL | ⚠️ PARTIAL (cost adders backend ok; guardrails + pricing UX missing) | Review 4 |
| Week-4 | Resolution UX + Governance | ⚠️ PARTIAL | ⚠️ PARTIAL (read-only governance done; resolution UX + multi-SKU missing) | Review 4 |

### Track-by-Track Status (Consolidated)

| Track | Planned Scope | Evidence Status | Consolidated Status | Last Updated |
|------|---------------|-----------------|---------------------|--------------|
| Track A (UI) | Quotation/Panel/Feeder/BOM/Pricing/Resolution UX | ⚠️ PARTIAL | ⚠️ PARTIAL (pure UI gaps, not engine gaps) | Review 4 |
| Track A-R (Reuse) | Copy flows + Master BOM + Post-reuse validation | ⚠️ PARTIAL | ⚠️ PARTIAL (CANONICAL - copy flows backend-only, master apply + editability + guardrails missing) | Review 6 |
| Track E (Compliance) | Guardrails, tracking, snapshots, constraints, multi-SKU | ⚠️ PARTIAL | ⚠️ PARTIAL (**COMPLIANCE** - mandatory, Phase-5 obligations) | Review 4 |
| Track D0 (Engine) | QCD/QCA foundations, templates, sheets, QCD generator | ⚠️ PARTIAL | ⚠️ PARTIAL (engine-first, separate from UI/reporting) | Review 4 |
| Track F (API Contracts) | API contract specifications | DEFER-ALLOWED | DEFER-ALLOWED (needs memo at closure) | Review 4 |

---

## Final Decisions (All 6 Reviews Complete - Ready for Decision Making)

### Decision 1: Overall Phase-6 Status Assessment
**Status:** *Ready for Decision - All 6 reviews complete, reconciliation finalized*

**Options:**
- ✅ ON TRACK: All critical items delivered, gaps are acceptable/minor
- ⚠️ AT RISK: Significant gaps identified, remediation plan required
- ❌ OFF TRACK: Critical path items missing, major replan required

**Decision Rationale:**
*To be populated after Review 6*

---

### Decision 2: Week 0-4 Closure Status
**Status:** *Ready for Decision - All 6 reviews complete, reconciliation finalized*

**Options:**
- ✅ CLOSED: All planned deliverables proven with evidence
- ⚠️ PARTIAL CLOSURE: Some deliverables delivered, gaps documented and accepted
- ❌ NOT CLOSED: Critical gaps remain, closure not acceptable

**Decision Rationale:**
*To be populated after Review 6*

---

### Decision 3: Critical Alarms Resolution Plan
**Status:** *Ready for Decision - All 6 reviews complete, reconciliation finalized*

**Resolution Approach:**
*To be populated after Review 6*

**Timeline:**
*To be populated after Review 6*

**Ownership:**
*To be populated after Review 6*

---

### Decision 4: Thread Drift Reconciliation
**Status:** *Ready for Decision - All 6 reviews complete, reconciliation finalized*

**Issue:** Week-4 planned work (resolution UX) differs from actual work (read-only hardening)

**Options:**
- Accept read-only hardening as Week-4 scope (update plan retroactively)
- Defer resolution UX to later week
- Execute resolution UX in addition to read-only hardening

**Decision:**
*To be populated after Review 6*

---

### Decision 5: Path Forward (Week 5+)
**Status:** *Ready for Decision - All 6 reviews complete, reconciliation finalized*

**Options:**
- Continue as planned (Week 5+ proceed)
- Remediate gaps first (pause Week 5+ until gaps closed)
- Hybrid approach (continue with parallel gap remediation)

**Decision:**
*To be populated after Review 6*

---

## Review Process Notes

### Review Methodology
1. Each review analyzes a specific document/set of documents
2. Findings are registered in the matrix with evidence status
3. Alarms are raised for critical missing items
4. Status updates are applied to consolidated matrices
5. After all 6 reviews, final decisions are derived

### Evidence Standards
- ✅ DONE: Concrete evidence exists (tests, code, docs, scripts)
- ⚠️ PARTIAL: Some evidence exists but not the planned deliverable
- ❌ MISSING: Planned but no evidence found

### Alarm Severity Levels
- 🔴 **COMPLIANCE**: Phase-5 compliance blockers - mandatory for Phase-6 sign-off (cannot be deferred)
- 🔴 **PARITY**: Legacy parity blockers - mandatory for Week-8.5 gate pass (cannot be deferred)
- 🔴 CRITICAL: Blocks closure or creates major risk
- 🟠 HIGH: Important but may be deferred with justification
- 🟡 MEDIUM: Should be addressed but not blocking
- DEFER-ALLOWED: Optional/deferable items (require defer memo at closure)

### Gap Classification Framework (Established in Review 2)
Gaps are classified into four types to reduce rework:
- **DOC-ONLY:** Planned doc but code exists → Write doc only
- **UI-MISSING:** Backend exists, UI missing → UI sprint
- **ENGINE-MISSING:** Core logic not implemented → Backend sprint
- **VERIFY-MISSING:** Feature exists but no proof → Tests + evidence

---

## Change Log

| Date | Review # | Change Description | Updated By |
|------|----------|-------------------|------------|
| 2025-01-27 | Review 1 | Initial matrix created with Review 1 findings | Reconciliation Analysis |
| 2025-01-27 | Review 2 | Review 2 completed: Phase-6 Complete Scope & Task Summary v1.4 reconciled. All alarms from Review 1 confirmed as FINAL. Gap classification framework established. Week-4 status clarified (Resolution UX NOT DONE; Read-only hardening DONE). Status corrections finalized for Weeks 0-4. | Reconciliation Analysis |
| 2025-01-27 | Review 3 | Review 3 completed: Phase-6 Execution Plan Revision Summary v1.2 reconciled. Compliance obligations clarified (mandatory vs optional). 5 alarms upgraded to COMPLIANCE status (Customer snapshot, BOM tracking, Guardrails, Multi-SKU, Resolution constraints). Track F marked as DEFER-ALLOWED. Status corrections updated with compliance-based labels for Weeks 0-4. | Reconciliation Analysis |
| 2025-01-27 | Review 4 | Review 4 completed: Phase-6 Execution Plan (Corrected Version Summary v1.2) reconciled. Track structure clarified (D0 explicit/engine-first, E centralized/compliance, A = UI only). Week-4 confusion resolved (UI resolution ≠ governance hardening). Final baseline reconciliation complete. All alarms finalized. No false alarms remain. Status corrections finalized for Weeks 0-4 (all PARTIAL before Week-5). | Reconciliation Analysis |
| 2025-01-27 | Review 5 | Review 5 completed: Legacy Parity Verification Checklist v1.0 reconciled. Parity evidence layer established. Reuse APIs confirmed as backend-only (parity verification pending). All Week 0-4 gaps confirmed as parity-critical (not optional). 2 new parity alarms added (ALARM-PARITY-EDITABILITY, ALARM-PARITY-GUARDRAILS). Parity verification matrix added. Week-8.5 gate requirements clarified. | Reconciliation Analysis |
| 2025-01-27 | Review 6 | Review 6 completed: Phase-6 Legacy Parity Addition Summary v1.3 reconciled. Track A-R confirmed as CANONICAL (not optional, Phase-6 execution obligation). Reuse completeness definition locked (requires UI + editability + guardrails, not just APIs). Legacy Parity Gate confirmed as hard blocking (Week-8.5). Reuse workflows canonical paths clarified (Path A/B/C). Track A-R final status matrix completed. All alarms finalized. Reconciliation COMPLETE and LOCKED. | Reconciliation Analysis |

---

**Document Status:** ✅ Review 6 of 6 Complete - Reconciliation FINALIZED and LOCKED

**Next Action:** Choose one of the following:
1. "Generate PHASE-6 Gap Register (Weeks 0-4)" → Single clean document listing actionable gaps
2. "Start Week-0 closure documentation" → Close Week-0 properly (docs + gates)
3. "Start Week-1 detailed plan (Add Panel + Snapshot)" → Begin execution planning

**Reconciled Truth (FINAL After Review 6 - Reconciliation COMPLETE):**
- ✅ Complete baseline scope (Docs 01–06/06) reconciled
- ✅ Corrected track structure: D0 (engine), E (compliance), A (UI only), A-R (CANONICAL)
- ✅ Authoritative gap truth for Weeks 0-4 established
- ✅ Parity checklist mapped to tasks
- ✅ Clear separation of UI vs Engine vs Canon obligations
- ✅ Track A-R confirmed as CANONICAL (Phase-6 execution obligation, not optional)
- ✅ Reuse completeness definition locked (UI + editability + guardrails required)
- ✅ Legacy Parity Gate confirmed as hard blocking (Week-8.5)
- ✅ Reuse workflows canonical paths clarified (Path A/B/C)
- Weeks 0-4 = PARTIAL (no week before Week-5 is fully closed per corrected plan)
- Week-4 = Read-only governance DONE (sub-deliverable), UI resolution PENDING
- Phase-6 = OPEN
- All alarms finalized (9 compliance alarms, 2 UI alarms, 2 parity alarms, no false alarms)
- Track F = DEFER-ALLOWED (needs memo at closure)
- **Reconciliation COMPLETE and LOCKED - No more documents required to understand Phase-6 scope**
