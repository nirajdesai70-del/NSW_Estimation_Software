# Standing Verification Instruction - Dual Reference Verification

**Version:** 2.1  
**Status:** 🔒 ACTIVE - STANDING INSTRUCTION  
**Effective From:** 2026-01-03  
**Supersedes:** v2.0  
**Valid Until:** End-to-End Software Development Complete  
**Owner:** Development Team  

---

## 🎯 Purpose

This document establishes a **mandatory standing instruction** requiring **PARALLEL verification** of all new builds and features against:

1. **Legacy Project** (`project/nish/`) - To ensure no functionality loss and continuous improvement
2. **NSW Fundamental Alignment Plan** (`NSW Fundamental Alignment Plan/`) - To ensure compliance with Phase 4/4.5 standards and fundamentals

**Dual verification ensures:**
1. ✅ **Business intent preserved** - Critical business decisions from legacy are not missed (Track A)
2. ✅ **NSW Standards compliance** - New work adheres to NSW Fundamental Alignment Plan (Phase 4/4.5) (Track B)
3. ✅ **Fundamentals alignment** - Follows master fundamentals, governance rules, and design standards (Track B)
4. ✅ **Progressive verification** - Each development stage includes dual verification
5. ✅ **Complete coverage** - Verification continues until full end-to-end software development is complete

**Important:** Track A does NOT enforce legacy schema parity, data migration, or technical implementation matching. It protects business intent only.

---

## ⚠️ CRITICAL RULE — Dual Verification (Track A + Track B)

**Version 2.1 Locked:**

1. **Track B (NSW Fundamentals) is ALWAYS mandatory and blocking.**
   - Builds must comply with NSW Fundamentals, Canonical Rules (L0/L1/L2), and governance standards.
   - Track B failures block completion.

2. **Track A (Legacy project/nish/) is a Business-Decision Reference Audit ONLY.**
   - **Purpose:** Ensure we are not missing business logic or business decisions.
   - **NOT purpose:** Legacy data migration, schema parity, or table-format alignment.
   - **Blocking condition:** Track A blocks completion ONLY when an item is explicitly tagged **RETAIN** and is not satisfied in the new build.

3. **Default assumption:**
   - All legacy items are **REPLACE** unless explicitly tagged **RETAIN**.

4. **Conflict resolution:**
   - If Track A and Track B conflict, Track B always wins.
   - New system is built strictly according to Schema Canon v1.0/v1.4 and NSW Fundamentals.

---

## 📋 Scope and Applicability

### When This Applies

- ✅ **Every new build** - Any new build or major component
- ✅ **Every feature addition** - New features or functionality
- ✅ **Every module completion** - Before module closure
- ✅ **Every integration point** - API endpoints, database schemas, UI components
- ✅ **Every stage gate** - Before moving to next development stage

### Valid Until

This instruction remains active until:
- ✅ Full end-to-end software development is complete
- ✅ All RETAIN-tagged business decisions from legacy are satisfied
- ✅ Final system validation confirms no missing functionality

---

## 🔍 Dual Verification Framework

## Track A: Legacy Business-Decision Reference Audit (`project/nish/`)

**Version:** 2.1  
**Status:** 🔒 ACTIVE  
**Applicability:** All Phase-5 and later builds  
**Blocking Rule:** ONLY for RETAIN-tagged items

---

### A.1 Purpose (Re-scoped)

Track A exists only to ensure that critical business decisions from the legacy system (`project/nish/`) are not accidentally missed during the new Phase-5 implementation.

**Track A is NOT intended to:**
- ❌ Migrate legacy data
- ❌ Align legacy schemas or tables
- ❌ Reproduce legacy technical implementations
- ❌ Enforce behavioral parity where the new system intentionally differs

**The new Phase-5 system is authoritative** and is built strictly according to:
- Schema Canon v1.0 / v1.4
- NSW Fundamentals
- Phase-5 governance rules

**Legacy is reference only, not canonical.**

---

### A.2 What Track A Checks (Allowed Scope)

Track A checks **business decisions only**, including:

#### 1) Quotation & Commercial Decisions
- Quotation lifecycle expectations
- Quotation numbering intent
- Panel / feeder / BOM conceptual flow (not schema)

#### 2) Pricing Decisions
- WEF date usage expectations
- Price list precedence logic (conceptual)
- Discount governance intent (not formula parity)

#### 3) Locking & Control Decisions
- When locking applies
- Who can lock / unlock
- Approval intent

#### 4) Audit & Compliance Decisions
- Which user actions must be auditable
- Traceability expectations

**These checks are conceptual, not technical.**

---

### A.3 What Track A Explicitly Does NOT Check

The following are **OUT OF SCOPE** and must never block a build:
- ❌ Legacy database schemas
- ❌ Legacy table structures
- ❌ Legacy data formats
- ❌ Legacy import pipelines
- ❌ Legacy calculation implementations
- ❌ Legacy bugs or workarounds
- ❌ Legacy UI layouts

**There is NO legacy data migration in Phase-5.**

---

### A.4 Mandatory Tagging Rule (RETAIN / REPLACE / DROP)

Every legacy reference identified under Track A **MUST** be tagged as one of the following:

#### 🔴 RETAIN (Blocking)
- A business decision that **must exist** in the new system
- If missing → build is **BLOCKED**

#### 🟡 REPLACE (Non-blocking)
- Business intent is covered, but:
  - Implemented differently, or
  - Improved, or
  - Re-architected
- Documentation required, but does **NOT** block

#### ⚪ DROP (Non-blocking)
- Legacy behavior intentionally removed
- Must be documented with rationale
- Does **NOT** block

**Default rule:** If not explicitly tagged → treated as **REPLACE**

---

### A.5 Blocking Rule (Very Important)

**Track A blocks a build ONLY if:**
- A legacy item is tagged **RETAIN**
- **AND** the corresponding business decision is not implemented in the new system

All other cases are non-blocking.

---

### A.6 Track A Verification Checklist (v2.1)

#### Step A1 — Identify Legacy References
- [ ] Identify relevant legacy modules in `project/nish/`
- [ ] Extract business decisions only (not schema/code)

#### Step A2 — Tag Each Decision
- [ ] For each identified decision: RETAIN / REPLACE / DROP selected
- [ ] Rationale documented

#### Step A3 — Validate RETAIN Items (Blocking)
- [ ] Each RETAIN decision exists in new build
- [ ] Evidence recorded (API, logic, workflow)

#### Step A4 — Document Non-Blocking Items
- [ ] REPLACE decisions documented
- [ ] DROP decisions justified

---

### A.7 Track A Output Artifact (Required)

Each build must produce a short **Track A Business Decision Audit** (see `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md`):

**Required sections:**
- RETAIN (Blocking) - Status: SATISFIED / MISSING
- REPLACE (Non-blocking) - New approach documented
- DROP (Non-blocking) - Rationale documented

**Only RETAIN = MISSING can block.**

---

### A.8 Authority Statement (Track A)

Track A exists to protect business intent, not legacy design.

The new system is not judged by how closely it looks like legacy, but by whether it honors required business decisions.

---

### A.9 Relationship with Track B

- **Track B (NSW Fundamentals & Governance)** → Always mandatory and blocking
- **Track A (Legacy Business Reference)** → Blocking only for RETAIN

**If Track A and Track B conflict:**
- Track B always wins

---

### A.10 Version Note

This Track A definition (v2.1) supersedes all previous legacy-parity or migration language.

Effective immediately for Phase-5 and onward.

---

### Verification Track B: NSW Fundamental Alignment Plan (`NSW Fundamental Alignment Plan/`)

#### Stage B1: Fundamentals Alignment

**Objective:** Verify compliance with NSW Master Fundamentals and standards

| Check Item | Description | Reference Document | Verification Method |
|------------|-------------|-------------------|---------------------|
| Master Fundamentals | Compliance with v2.0 fundamentals | `01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md` | Review against master doctrine |
| Canonical Rules | L0/L1/L2 definitions compliance | `02_GOVERNANCE/NEPL_CANONICAL_RULES.md` | Verify layer definitions |
| Master Reference | 9-layer compliance (A-I) | `01_FUNDAMENTALS/MASTER_REFERENCE.md` | Check layer alignment |
| Governance Standards | NEPL standards compliance | `02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md` | Verify against governance rules |
| Design Documents | Component design alignment | `05_DESIGN_DOCUMENTS/` (relevant component) | Compare with design docs |
| Gap Register | Gap closure verification | `02_GOVERNANCE/BOM_GAP_REGISTER.md`, `03_GAP_REGISTERS/` | Verify gaps are addressed |

**Output:** Fundamentals alignment report

#### Stage B2: Standards Compliance

**Objective:** Verify adherence to Phase 4/4.5 standards and patterns

| Check Item | Description | Reference Document | Verification Method |
|------------|-------------|-------------------|---------------------|
| Architecture Patterns | Follows NSW architecture standards | `05_DESIGN_DOCUMENTS/` (component designs) | Compare architecture |
| Implementation Mapping | Matches implementation patterns | `01_FUNDAMENTALS/IMPLEMENTATION_MAPPING.md` | Verify codebase mapping |
| Verification Queries | Passes verification queries | `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md` | Run verification queries |
| Verification Checklist | Meets checklist requirements | `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` | Complete checklist |
| Phase Requirements | Meets Phase 4/4.5 requirements | `04_PHASES/` (relevant phase docs) | Verify phase compliance |

**Output:** Standards compliance report

---

---

#### Stage B3: Gap Register Verification (NSW Fundamentals)

**Objective:** Ensure all gaps identified in NSW Fundamental Alignment Plan are addressed

| Check Item | Gap Register Reference | Gap Description | New Implementation | Status |
|------------|----------------------|-----------------|-------------------|--------|
| Gap 1 | [Register file] | [Gap description] | [How addressed] | ✅/⚠️/❌ |
| Gap 2 | [Register file] | [Gap description] | [How addressed] | ✅/⚠️/❌ |
| Gap 3 | [Register file] | [Gap description] | [How addressed] | ✅/⚠️/❌ |
| ... | ... | ... | ... | ... |

**Gap Registers to Check:**
- `02_GOVERNANCE/BOM_GAP_REGISTER.md` - Primary gap register
- `03_GAP_REGISTERS/PROPOSAL_BOM_GAP_REGISTER_R1.md` - Proposal BOM gaps
- `03_GAP_REGISTERS/MASTER_BOM_GAP_REGISTER_R1.md` - Master BOM gaps
- Component-specific gap registers in `05_DESIGN_DOCUMENTS/`

**Output:** Gap register verification report

---

### Combined Verification: Cross-Reference Check

**Objective:** Ensure no conflicts between Track A (business decisions) and Track B (fundamentals)

| Check Item | Track A Business Decision | Track B Requirement | Conflict? | Resolution |
|------------|--------------------------|---------------------|-----------|------------|
| Decision 1 | [RETAIN/REPLACE/DROP] | [Fundamental requirement] | ✅ No / ⚠️ Yes | [If conflict: Track B wins] |
| Decision 2 | [RETAIN/REPLACE/DROP] | [Fundamental requirement] | ✅ No / ⚠️ Yes | [If conflict: Track B wins] |
| ... | ... | ... | ... | ... |

**Conflict Resolution Rule:** If Track A and Track B conflict, **Track B always wins**.

**Output:** Cross-reference verification report

---

## 📝 Verification Checklist Template

Use this checklist for every build/feature/module:

### Pre-Verification Setup

- [ ] **Track A (Legacy):** Identify relevant legacy components in `project/nish/`
- [ ] **Track A (Legacy):** Access legacy system/codebase for reference
- [ ] **Track A (Legacy):** Review legacy documentation and schemas
- [ ] **Track B (NSW Fundamentals):** Identify relevant documents in `NSW Fundamental Alignment Plan/`
- [ ] **Track B (NSW Fundamentals):** Review master fundamentals and governance rules
- [ ] **Track B (NSW Fundamentals):** Review relevant design documents and gap registers
- [ ] Set up comparison workspace/tools for both tracks

### Track A: Legacy Project Verification

#### Feature Completeness (Legacy)

- [ ] List all legacy features related to new build
- [ ] Verify each feature exists in new build (or justified as deprecated)
- [ ] Document any missing features with action plan
- [ ] Verify feature parity (same or better functionality)

#### Quality Improvements (Legacy)

- [ ] Review legacy code for known issues
- [ ] Verify improvements are implemented in new build
- [ ] Document how each legacy issue is addressed
- [ ] Verify no new issues introduced

#### Business Logic Completeness (Legacy)

- [ ] Identify relevant legacy business decisions for this module
- [ ] Tag each decision: RETAIN / REPLACE / DROP
- [ ] For RETAIN decisions: verify presence in new build (blocking)
- [ ] For REPLACE/DROP: document rationale (non-blocking)

### Track B: NSW Fundamental Alignment Plan Verification

#### Fundamentals Alignment

- [ ] Review `01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md` for compliance
- [ ] Verify L0/L1/L2 definitions per `02_GOVERNANCE/NEPL_CANONICAL_RULES.md`
- [ ] Check 9-layer compliance per `01_FUNDAMENTALS/MASTER_REFERENCE.md`
- [ ] Verify governance standards per `02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md`

#### Design Document Alignment

- [ ] Review relevant component design in `05_DESIGN_DOCUMENTS/`
- [ ] Verify implementation matches design specifications
- [ ] Check design patterns and architecture compliance
- [ ] Verify component integration points

#### Gap Register Verification

- [ ] Review `02_GOVERNANCE/BOM_GAP_REGISTER.md` for related gaps
- [ ] Review component-specific gap registers
- [ ] Verify all related gaps are addressed in new build
- [ ] Document gap closure or deferral with justification

#### Verification Queries and Checklists

- [ ] Run verification queries from `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md`
- [ ] Complete verification checklist from `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md`
- [ ] Verify Phase 4/4.5 requirements per `04_PHASES/` documents
- [ ] Check implementation mapping per `01_FUNDAMENTALS/IMPLEMENTATION_MAPPING.md`

### Combined Standards Compliance

- [ ] Verify architecture follows NSW standards (Track B) AND new build standards
- [ ] Verify database schema follows NSW design (Track B) AND Phase 5 schema
- [ ] Verify API design follows NSW patterns (Track B) AND new API standards
- [ ] Verify code organization follows NSW structure (Track B) AND new structure
- [ ] Verify documentation meets NSW standards (Track B) AND new doc standards

### Testing

- [ ] Create test cases based on legacy functionality
- [ ] Verify new build passes legacy-equivalent tests
- [ ] Test edge cases identified in legacy system
- [ ] Verify error handling is improved

### Documentation

- [ ] Document verification findings
- [ ] Document any gaps and resolutions
- [ ] Document improvements over legacy
- [ ] Update build ticket with verification status

---

## 🔄 Dual Verification Process Flow

```
1. START: New Build/Feature Request
   ↓
   ├─────────────────────────────────────┬─────────────────────────────────────┐
   │ TRACK A: Legacy Project             │ TRACK B: NSW Fundamentals            │
   │ (`project/nish/`)                   │ (`NSW Fundamental Alignment Plan/`)  │
   │                                     │                                     │
2A. Identify Legacy Reference Points     │ 2B. Identify NSW Fundamentals Docs   │
   ↓                                     │     ↓                                │
3A. Extract Legacy Functionality         │ 3B. Review Master Fundamentals       │
   ↓                                     │     ↓                                │
4A. Map Legacy → New Build               │ 4B. Review Governance Rules          │
   ↓                                     │     ↓                                │
5A. Perform Gap Analysis (Legacy)        │ 5B. Review Design Documents          │
   ↓                                     │     ↓                                │
6A. Identify Legacy Issues/Defects       │ 6B. Review Gap Registers             │
   ↓                                     │     ↓                                │
7A. Verify Improvements (Legacy)         │ 7B. Run Verification Queries         │
   ↓                                     │     ↓                                │
8A. Validate RETAIN Items (Blocking)      │ 8B. Complete Verification Checklist  │
   ↓                                     │     ↓                                │
   └─────────────────────────────────────┴─────────────────────────────────────┘
   ↓
9. COMBINED VERIFICATION
   ├─→ RETAIN Item Missing (Track A)? → Add business decision → Loop back to 8A
   ├─→ Fundamentals Non-Compliant (Track B)? → Refactor → Loop back to 3B
   ├─→ Gaps Not Closed (Track B)? → Address gaps → Loop back to 6B
   ├─→ Track A/B Conflict? → Track B wins → Document → Continue
   └─→ All Verified? → Continue
   ↓
10. Create Combined Verification Report (Track A + Track B)
   ↓
11. Review and Sign-off
   ├─→ Issues Found? → Loop back to appropriate track/step
   └─→ Approved? → Mark Complete
   ↓
12. END: Build/Feature Complete
```

**Key Points:**
- Tracks A and B run in **PARALLEL** (can be done simultaneously)
- **Track B must PASS** (always blocking)
- **Track A blocks only for RETAIN items** (non-blocking otherwise)
- Combined verification ensures no conflicts between tracks
- If conflict: Track B always wins

---

## 📊 Verification Report Template

### Verification Report: [Build/Feature Name]

**Date:** [YYYY-MM-DD]  
**Verifier:** [Name]  
**Build/Feature:** [Name and version]  
**Legacy Reference:** `project/nish/` [specific components]

---

#### Executive Summary

- **Overall Status:** ✅ PASS / ⚠️ PASS WITH NOTES / ❌ FAIL
- **Track A (Legacy) Status:** ✅/⚠️/❌
- **Track B (NSW Fundamentals) Status:** ✅/⚠️/❌
- **Key Findings:** [Summary of major findings from both tracks]
- **Recommendations:** [Action items if any]

---

#### TRACK A: Legacy Business-Decision Reference Audit

##### 1. RETAIN Items (Blocking)

| # | Legacy Business Decision | Evidence in New System | Status |
|---|-------------------------|----------------------|--------|
| 1 | [Decision description] | [API/logic/workflow] | ✅ SATISFIED / ❌ MISSING |
| 2 | [Decision description] | [API/logic/workflow] | ✅ SATISFIED / ❌ MISSING |
| ... | ... | ... | ... |

**Summary:** [Number of RETAIN items, satisfied, missing]

---

##### 2. REPLACE Items (Non-blocking)

| # | Legacy Business Decision | New Approach | Notes |
|---|-------------------------|--------------|-------|
| 1 | [Decision description] | [New implementation] | [Rationale] |
| 2 | [Decision description] | [New implementation] | [Rationale] |
| ... | ... | ... | ... |

**Summary:** [Number of REPLACE items documented]

---

##### 3. DROP Items (Non-blocking)

| # | Legacy Business Decision | Rationale for Drop |
|---|-------------------------|-------------------|
| 1 | [Decision description] | [Justification] |
| 2 | [Decision description] | [Justification] |
| ... | ... | ... |

**Summary:** [Number of DROP items documented]

---

#### TRACK B: NSW Fundamental Alignment Plan Verification

##### 3. Fundamentals Alignment

| Category | Requirement | Status | Notes |
|----------|-------------|--------|-------|
| Architecture | [Standard] | ✅/⚠️/❌ | [Notes] |
| Database | [Standard] | ✅/⚠️/❌ | [Notes] |
| API | [Standard] | ✅/⚠️/❌ | [Notes] |
| Code | [Standard] | ✅/⚠️/❌ | [Notes] |
| Testing | [Standard] | ✅/⚠️/❌ | [Notes] |
| Documentation | [Standard] | ✅/⚠️/❌ | [Notes] |

**Summary:** [Compliance status]

##### 4. Design Document Alignment

| Component | Design Document | Status | Notes |
|-----------|----------------|--------|-------|
| [Component 1] | [Design doc path] | ✅/⚠️/❌ | [Notes] |
| [Component 2] | [Design doc path] | ✅/⚠️/❌ | [Notes] |
| ... | ... | ... | ... |

**Summary:** [Alignment status]

---

##### 5. Gap Register Verification

| Gap ID | Register | Gap Description | New Implementation | Status |
|--------|----------|-----------------|-------------------|--------|
| [Gap 1] | [Register] | [Description] | [How addressed] | ✅/⚠️/❌ |
| [Gap 2] | [Register] | [Description] | [How addressed] | ✅/⚠️/❌ |
| ... | ... | ... | ... | ... |

**Summary:** [Gap closure status]

---

##### 6. Verification Queries and Checklists

| Check Item | Reference | Status | Notes |
|------------|-----------|--------|-------|
| Verification Queries | `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md` | ✅/⚠️/❌ | [Results] |
| Verification Checklist | `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` | ✅/⚠️/❌ | [Results] |
| Phase Requirements | `04_PHASES/` | ✅/⚠️/❌ | [Results] |
| Implementation Mapping | `01_FUNDAMENTALS/IMPLEMENTATION_MAPPING.md` | ✅/⚠️/❌ | [Results] |

**Summary:** [Verification status]

---

#### COMBINED: Cross-Reference Check

| Track A Decision | Track B Requirement | Conflict? | Resolution |
|------------------|---------------------|-----------|------------|
| [RETAIN/REPLACE/DROP] | [Fundamental requirement] | ✅ No / ⚠️ Yes | [If conflict: Track B wins] |
| [RETAIN/REPLACE/DROP] | [Fundamental requirement] | ✅ No / ⚠️ Yes | [If conflict: Track B wins] |
| ... | ... | ... | ... |

**Summary:** [Conflicts identified, resolved per Track B authority]

---

#### 7. Action Items (Combined from Both Tracks)

- [ ] **Action 1:** [Description] - Owner: [Name] - Due: [Date]
- [ ] **Action 2:** [Description] - Owner: [Name] - Due: [Date]
- ... 

---

#### 8. Sign-off

**Verified By:** [Name]  
**Date:** [YYYY-MM-DD]  
**Approval:** ✅ APPROVED / ⚠️ APPROVED WITH NOTES / ❌ NOT APPROVED

**Next Steps:** [What needs to happen next]

---

## 🔗 Reference Documents

### Track A: Legacy Project Reference
- `project/nish/README.md` - Legacy project overview
- `project/nish/` - Legacy codebase (read-only reference)
- Legacy schema documentation (in `project/nish/02_LEGACY_SCHEMA/`)

### Track B: NSW Fundamental Alignment Plan Reference

#### Core Fundamentals
- `NSW Fundamental Alignment Plan/00_INDEX.md` - Master index and navigation
- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md` - ⭐ Master doctrine (FUNDAMENTALS v2.0)
- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_REFERENCE.md` - Complete 9-layer documentation (A-I)
- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/IMPLEMENTATION_MAPPING.md` - Codebase implementation mapping

#### Governance and Standards
- `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md` - ⭐ Frozen L0/L1/L2 definitions
- `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md` - Cumulative verification approach
- `NSW Fundamental Alignment Plan/02_GOVERNANCE/BOM_GAP_REGISTER.md` - Primary gap register

#### Gap Registers
- `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/` - All gap registers
- `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/PROPOSAL_BOM_GAP_REGISTER_R1.md` - Proposal BOM gaps
- `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/MASTER_BOM_GAP_REGISTER_R1.md` - Master BOM gaps

#### Design Documents
- `NSW Fundamental Alignment Plan/05_DESIGN_DOCUMENTS/` - All component design documents
- Component-specific designs (Feeder BOM, Master BOM, Panel BOM, Proposal BOM, etc.)

#### Verification
- `NSW Fundamental Alignment Plan/07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md` - Verification queries
- `NSW Fundamental Alignment Plan/07_VERIFICATION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` - Verification checklist
- `NSW Fundamental Alignment Plan/07_VERIFICATION/PHASE2_2_VERIFICATION_SQL.md` - SQL verification

#### Phase Documents
- `NSW Fundamental Alignment Plan/04_PHASES/` - Phase 4/4.5 execution documents
- `NSW Fundamental Alignment Plan/04_PHASES/MASTER_PLANNING_INDEX.md` - Master planning index
- `NSW Fundamental Alignment Plan/04_PHASES/PHASES_1_5_COMPLETE_REVIEW.md` - Complete phase status

### Current Project Standards (Additional)
- `NEW_BUILD_ARCHITECTURE.md` - Architecture standards
- `docs/PHASE_5/` - Phase 5 standards and schemas
- `IMPORTER_BUILD_TICKET.md` - Current build specifications
- `GAP_B_VERIFICATION_REPORT.md` - Previous verification example

---

## ⚙️ Integration with Development Workflow

### When to Verify

1. **During Design Phase**
   - Verify design covers all legacy features
   - Verify design addresses legacy issues

2. **During Implementation Phase**
   - Verify implementation matches design
   - Verify no legacy functionality is missed

3. **Before Code Review**
   - Complete verification checklist
   - Submit verification report with PR

4. **Before Testing Phase**
   - Verify test cases cover legacy functionality
   - Verify edge cases from legacy are tested

5. **Before Deployment**
   - Final verification against legacy
   - Ensure all gaps are closed

### Verification Gates

**Gate 1: Design Review**
- ✅ **Track A:** Feature mapping complete (legacy)
- ✅ **Track A:** Gap analysis done (legacy)
- ✅ **Track A:** Design addresses legacy issues
- ✅ **Track B:** Fundamentals alignment verified
- ✅ **Track B:** Design documents reviewed
- ✅ **Track B:** Gap registers checked
- ✅ **Combined:** Design follows new standards

**Gate 2: Implementation Review**
- ✅ **Track A:** Implementation matches legacy functionality
- ✅ **Track A:** All legacy features implemented
- ✅ **Track A:** Legacy improvements implemented
- ✅ **Track B:** Implementation matches NSW fundamentals
- ✅ **Track B:** Governance standards verified
- ✅ **Track B:** Verification queries passed
- ✅ **Combined:** Standards compliance verified

**Gate 3: Pre-Deployment Review**
- ✅ **Track A:** Legacy verification complete
- ✅ **Track B:** NSW Fundamentals verification complete
- ✅ **Combined:** All verification checklists complete
- ✅ **Combined:** Verification report approved
- ✅ **Combined:** No critical gaps in either track

---

## 📈 Tracking and Reporting

### Verification Status Dashboard

Track verification status for all builds/features:

| Build/Feature | Legacy Reference | Status | Verifier | Date | Report Link |
|---------------|------------------|--------|----------|------|-------------|
| [Build 1] | [Legacy component] | ✅/⚠️/❌ | [Name] | [Date] | [Link] |
| [Build 2] | [Legacy component] | ✅/⚠️/❌ | [Name] | [Date] | [Link] |
| ... | ... | ... | ... | ... | ... |

### Monthly Verification Summary

- Total builds verified: [Number]
- Features preserved: [Number]
- Issues addressed: [Number]
- Standards compliance: [Percentage]
- Outstanding gaps: [Number]

---

## 🚨 Escalation Process

### If Verification Fails

1. **Immediate Actions:**
   - Document all gaps and issues
   - Create action items with owners
   - Block build/feature completion until resolved

2. **Resolution Process:**
   - Assign owners to action items
   - Set deadlines for fixes
   - Re-verify after fixes

3. **Exception Process:**
   - Any deviation from legacy functionality MUST be documented
   - Requires explicit approval with justification
   - Must be signed off by project lead

### If Standards Not Met

1. **Immediate Actions:**
   - Document non-compliance
   - Create refactoring plan
   - Block build/feature completion until compliant

2. **Resolution Process:**
   - Refactor to meet standards
   - Re-verify compliance
   - Document any exceptions with approval

---

## ✅ Completion Criteria

A build/feature is considered verified and complete when **BOTH tracks pass**:

### Track A: Legacy Business-Decision Reference Audit ✅
- [x] All RETAIN-tagged business decisions are satisfied
- [x] REPLACE items documented with rationale
- [x] DROP items justified
- [x] Track A Business Decision Audit complete

### Track B: NSW Fundamental Alignment Plan Verification ✅
- [x] Master Fundamentals v2.0 compliance verified
- [x] NEPL Canonical Rules (L0/L1/L2) compliance verified
- [x] Governance standards compliance verified
- [x] Relevant design documents alignment verified
- [x] All related gaps from gap registers addressed
- [x] Verification queries passed
- [x] Verification checklist completed
- [x] NSW Fundamentals verification report complete

### Combined Verification ✅
- [x] Both Track A and Track B reports approved
- [x] No conflicts between tracks identified
- [x] All new standards are followed (or exceptions approved)
- [x] Combined verification report complete and approved
- [x] All action items from both tracks are resolved
- [x] Sign-off obtained from reviewer

---

## 📝 Notes and Best Practices

### Best Practices

1. **Start Early:** Begin verification during design phase, not after implementation
2. **Document Everything:** Keep detailed notes of legacy functionality and issues
3. **Automate Where Possible:** Create scripts to compare schemas, APIs, etc.
4. **Regular Reviews:** Don't wait until end - verify incrementally
5. **Collaborate:** Work with team members familiar with legacy system

### Common Pitfalls to Avoid

- ❌ Assuming legacy functionality is not needed without verification
- ❌ Skipping verification due to time constraints
- ❌ Not documenting gaps and assumptions
- ❌ Verifying only happy path, missing edge cases
- ❌ Not updating verification as legacy understanding improves

---

## 🔄 Document Maintenance

**Review Frequency:** Monthly or after major architectural changes  
**Owner:** Development Team Lead  
**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-03 | Initial standing instruction (legacy verification only) | Development Team |
| 2.0 | 2026-01-03 | Added parallel verification with NSW Fundamental Alignment Plan (Track B) | Development Team |
| 2.1 | 2026-01-03 | Re-scoped Track A to Business-Decision Reference Audit only; RETAIN/REPLACE/DROP tagging; removed migration/schema parity requirements | Development Team |

**Authority Lock:** Any future change that alters blocking rules or Track A scope requires a major version bump (v3.0).

---

## 📞 Questions or Issues?

For questions about this verification process, contact:
- **Process Owner:** [Name/Team]
- **Legacy System Expert:** [Name/Team]
- **Technical Lead:** [Name/Team]

---

**Status:** 🔒 ACTIVE - STANDING INSTRUCTION  
**This instruction remains in effect until end-to-end software development is complete.**

