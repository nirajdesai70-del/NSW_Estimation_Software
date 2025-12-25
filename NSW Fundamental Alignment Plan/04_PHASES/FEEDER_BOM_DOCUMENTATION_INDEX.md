# Feeder BOM — Complete Documentation Index

**Generated:** 2025-01-XX  
**Purpose:** Comprehensive index of all Feeder BOM planning, implementation, and documentation files  
**Total Files:** 30+ documents

---

## 📋 Table of Contents

1. [Planning Documents (P0-P6)](#planning-documents-p0-p6)
2. [Round-0 Implementation Documents](#round-0-implementation-documents)
3. [Phase 2 Execution Documents](#phase-2-execution-documents)
4. [PB-GAP-004 Verification Documents](#pb-gap-004-verification-documents)
5. [Execution Support Documents](#execution-support-documents)
6. [Status & Tracking Documents](#status--tracking-documents)
7. [Release Pack Documents](#release-pack-documents)

---

## 1. Planning Documents (P0-P6)

### P1: Baseline (As-Is State)
- **`PLANNING/BASELINE/FEEDER_BOM_AS_IS.md`**
  - Current state snapshot
  - Known failure modes
  - Why PB-GAP-004 exists

### P2: Design (To-Be State)
- **`PLANNING/DESIGN/FEEDER_BOM_TO_BE.md`**
  - Target behavior specification
  - Idempotent apply semantics
  - Clear-before-copy rules

### P3: Verification Contract
- **`PLANNING/VERIFICATION/FEEDER_BOM_VERIFICATION_CONTRACT_P3.md`**
  - PASS/FAIL criteria
  - A3/A4 query definitions
  - Test execution steps
  - Evidence requirements

### P4: Implementation Plan
- **`PLANNING/IMPLEMENTATION/FEEDER_BOM_IMPLEMENTATION_PLAN_P4.md`**
  - Step-by-step implementation checklist
  - Code touchpoints
  - Database queries
  - Testing strategy
  - Risk mitigation

### P5: Execution Runbook
- **`PLANNING/EXECUTION/FEEDER_BOM_EXECUTION_RUNBOOK_P5.md`**
  - Operational checklist
  - Implementation steps
  - Verification steps
  - Evidence pack template
  - Rollback procedures

### P6: Closure Pack
- **`PLANNING/CLOSURE/PB_GAP_004_CLOSURE_PACK_P6.md`**
  - Paste-ready closure statement
  - Evidence format templates
  - Gap register update content

---

## 2. Round-0 Implementation Documents

**Location:** `docs/FEEDER_BOM/`

### Main Documents
- **`FEEDER_BOM_ROUND0_SUMMARY.md`**
  - Implementation summary
  - Acceptance criteria
  - Validation queries (A3/A4)
  - Expected results

- **`FEEDER_BOM_ROUND0_IMPLEMENTATION_GUIDE.md`**
  - Complete implementation guide
  - A3/A4 validation SQL queries
  - Validation workflow
  - Rules compliance checklist
  - Testing checklist

- **`FEEDER_BOM_ROUND0_CODE_CHANGES.md`**
  - Exact code changes needed
  - Complete method structure reference
  - Required imports
  - Validation queries

### Status & Execution Documents
- **`FEEDER_BOM_ROUND0_EXECUTION_STATUS.md`**
  - Current execution status
  - Phase completion tracking
  - Pending actions

- **`FEEDER_BOM_ROUND0_EXECUTION_CHECKLIST.md`**
  - Step-by-step execution checklist
  - Validation steps

- **`FEEDER_BOM_ROUND0_STATUS_UPDATE.md`**
  - Status updates
  - Progress tracking

### Supporting Documents
- **`FEEDER_BOM_ROUND0_COMPLETE_METHOD.md`**
  - Complete method reference
  - Full code structure

- **`FEEDER_BOM_ROUND0_CORRECTIONS.md`**
  - Corrections and fixes
  - Critical changes

### Root Level Status
- **`FEEDER_BOM_ROUND0_EXECUTION_STATUS.md`** (root)
  - High-level execution status

---

## 3. Phase 2 Execution Documents

**Location:** `docs/FEEDER_BOM/`

### Wiring & Implementation
- **`FEEDER_ENDPOINT_WIRING_PHASE2_1.md`**
  - Endpoint wiring instructions
  - Controller patch details

- **`PHASE2_1_WIRING_EXECUTION.md`**
  - Wiring execution steps
  - BomEngine integration

### Verification
- **`PHASE2_2_VERIFICATION_SQL.md`**
  - SQL verification queries
  - Evidence capture instructions

### Execution Tracking
- **`PHASE2_EXECUTION_CHECKLIST.md`**
  - Phase 2 execution checklist
  - Gate tracking

- **`PHASE2_EXECUTION_SUMMARY.md`**
  - Phase 2 summary
  - Quick start guide
  - Status tracking

### Controller Implementation
- **`PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`**
  - Controller patch instructions
  - BomEngine wiring

---

## 4. PB-GAP-004 Verification Documents

**Location:** `PLANNING/VERIFICATION/`

### Main Verification Contract
- **`FEEDER_BOM_VERIFICATION_CONTRACT_P3.md`** (covered in P3 section)

### Quick Start & Instructions
- **`PB_GAP_004_QUICK_START.md`**
  - Quick start guide
  - Test execution steps

- **`PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md`**
  - P5 execution instructions
  - Detailed steps

### Test Data & Fixtures
- **`PB_GAP_004_TEST_FIXTURES.md`**
  - Test fixture requirements
  - Sample data setup

- **`PB_GAP_004_FIXTURE_DISCOVERY_QUERIES.md`**
  - Queries to discover test fixtures
  - Data readiness checks

### Verification Queries
- **`PB_GAP_004_VERIFICATION_QUERIES.sql`**
  - SQL queries for verification
  - A3/A4 query definitions

### Results & Troubleshooting
- **`PB_GAP_004_RESULTS_TEMPLATE.md`**
  - Results template
  - Evidence format

- **`PB_GAP_004_TROUBLESHOOTING.md`**
  - Common issues
  - Troubleshooting guide

### Gap Register Reference
- **`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PB_GAP_004_INSTANCE_ISOLATION_VERIFICATION_v1.0_2025-12-19.md`**
  - Original gap definition
  - In-work validation instructions

---

## 5. Execution Support Documents

**Location:** `PLANNING/EXECUTION/`

### Readiness & Approval
- **`EXECUTION_READINESS_CHECKLIST.md`**
  - Pre-execution checklist
  - Hard preconditions
  - Window-A/Window-B readiness

- **`EXECUTION_APPROVAL.md`**
  - Execution authorization
  - Window dates

- **`EXECUTION_WINDOW_TODO.md`**
  - Window execution TODO list

### Window-A Documents
- **`WINDOW_A_PREFLIGHT.md`**
  - Window-A preflight checks
  - Pre-execution verification

- **`WINDOW_A_START_PACK.md`**
  - Window-A start instructions
  - Command references

- **`WINDOW_A_COMMAND_BLOCK.md`**
  - Window-A command block
  - SQL commands

- **`WINDOW_A_EVIDENCE_HEADER_TEMPLATE.md`**
  - Evidence header template
  - Format requirements

### Window-B Documents
- **`WINDOW_B_PREFLIGHT.md`**
  - Window-B preflight checks
  - Pre-execution verification

- **`WINDOW_B_START_PACK.md`**
  - Window-B start instructions
  - Command references

- **`WINDOW_B_EVIDENCE_HEADER_TEMPLATE.md`**
  - Evidence header template
  - Format requirements

### Phase 2 Staging
- **`PHASE2_STAGING_EXECUTION_CHECKLIST.md`**
  - Phase 2 staging checklist
  - Gate verification

---

## 6. Status & Tracking Documents

### Root Level
- **`FEEDER_BOM_ROUND0_EXECUTION_STATUS.md`** (root)
  - High-level execution status
  - Phase completion

### Phase 2 Status
- **`PHASE2_EXECUTION_STATUS.md`** (root)
  - Phase 2 execution status

---

## 7. Release Pack Documents

**Location:** `PLANNING/RELEASE_PACKS/PHASE2/`

### Main Documents
- **`00_README_RUNBOOK.md`**
  - Phase 2 runbook
  - Complete guide

- **`01_ARCH_DECISIONS.md`**
  - Architectural decisions
  - Design choices

- **`02_BOM_ENGINE_CONTRACT.md`**
  - BomEngine API contract
  - Method specifications

- **`STATUS.md`**
  - Phase 2 status tracking

### Data & Configuration
- **`03_APPLY_FEEDER_TEMPLATE_IO.json`**
  - API input/output specification
  - JSON schema

- **`07_DATA_READINESS/`**
  - **`DATA_READINESS_GATE.md`** — Data readiness criteria
  - **`TEMPLATE_SHORTLIST.md`** — Template selection guide

### Execution Scripts
- **`04_EXECUTION_SCRIPTS/`**
  - **`apply_feeder_template.sql`** — SQL execution script
  - **`copy_history.sql`** — Copy history queries
  - **`rollback.sql`** — Rollback script

### Verification
- **`05_VERIFICATION/`**
  - **`S1_S2_VERIFICATION.sql`** — S1/S2 verification queries
  - **`SCORECARD.md`** — Verification scorecard

### Risk & Alignment
- **`06_RISKS_AND_ROLLBACK.md`**
  - Risk assessment
  - Rollback procedures

- **`ALIGNMENT_CHECK.md`**
  - Alignment verification
  - Consistency checks

---

## 📊 Document Statistics

### By Category
- **Planning Documents (P0-P6):** 6 files
- **Round-0 Implementation:** 8 files
- **Phase 2 Execution:** 5 files
- **PB-GAP-004 Verification:** 8 files
- **Execution Support:** 10 files
- **Release Pack (Phase 2):** 11+ files

### By Location
- **`PLANNING/`:** ~25 files
- **`docs/FEEDER_BOM/`:** 13 files
- **Root level:** 2 status files

---

## 🎯 Recommended Review Order

### For Understanding the Plan
1. `PLANNING/BASELINE/FEEDER_BOM_AS_IS.md` — Understand current state
2. `PLANNING/DESIGN/FEEDER_BOM_TO_BE.md` — Understand target state
3. `PLANNING/VERIFICATION/FEEDER_BOM_VERIFICATION_CONTRACT_P3.md` — Understand verification
4. `PLANNING/IMPLEMENTATION/FEEDER_BOM_IMPLEMENTATION_PLAN_P4.md` — Understand implementation
5. `PLANNING/EXECUTION/FEEDER_BOM_EXECUTION_RUNBOOK_P5.md` — Understand execution

### For Implementation
1. `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_SUMMARY.md` — Quick overview
2. `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_IMPLEMENTATION_GUIDE.md` — Detailed guide
3. `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_CODE_CHANGES.md` — Code changes
4. `FEEDER_BOM_ROUND0_EXECUTION_STATUS.md` — Current status

### For Execution
1. `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md` — Pre-execution
2. `PLANNING/EXECUTION/FEEDER_BOM_EXECUTION_RUNBOOK_P5.md` — Execution steps
3. `PLANNING/VERIFICATION/PB_GAP_004_QUICK_START.md` — Quick reference
4. `docs/FEEDER_BOM/FEEDER_BOM_ROUND0_EXECUTION_CHECKLIST.md` — Checklist

### For Verification
1. `PLANNING/VERIFICATION/FEEDER_BOM_VERIFICATION_CONTRACT_P3.md` — Contract
2. `PLANNING/VERIFICATION/PB_GAP_004_VERIFICATION_QUERIES.sql` — SQL queries
3. `PLANNING/VERIFICATION/PB_GAP_004_RESULTS_TEMPLATE.md` — Results format

### For Closure
1. `PLANNING/CLOSURE/PB_GAP_004_CLOSURE_PACK_P6.md` — Closure pack
2. `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PB_GAP_004_INSTANCE_ISOLATION_VERIFICATION_v1.0_2025-12-19.md` — Original gap

---

## 🔗 Key Cross-References

### Gap Register
- **`PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`** — Main gap register (update after closure)

### Master Planning
- **`PLANNING/MASTER_PLANNING_INDEX.md`** — Master planning index

### Standards
- **`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md`** — Canonical rules reference

---

## 📝 Notes

- All planning documents are **planning-only** (no code changes, no DB writes)
- Execution documents require authorization and controlled environment
- Verification requires A3/A4 SQL queries to pass
- Closure requires evidence pack (R1/R2/S1/S2)

---

**END OF DOCUMENTATION INDEX**

