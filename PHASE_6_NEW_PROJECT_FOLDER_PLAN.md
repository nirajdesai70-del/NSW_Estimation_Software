# Phase 6 New Project Folder Plan
## NSW Estimation Software V1.0 - Fresh Project Structure Plan

**Date:** 2025-01-27  
**Status:** 📋 PLAN FOR REVIEW  
**Purpose:** Plan for creating fresh "NSW Estimation Software V1.0" folder with organized Phase 6 documentation

---

## 🎯 Objective

Create a **clean, organized reference folder** (`NSW Estimation Software V1.0`) that:
- Contains all Phase 6 planning and documentation files
- Has proper folder structure and organization
- Serves as reference and governance baseline
- Remains clean (docs only initially)
- Allows gradual code/file migration as needed

---

## 📁 Proposed Folder Structure

### Root: `/Volumes/T9/Projects/NSW Estimation Software V1.0/`

```
NSW Estimation Software V1.0/
├── 00_GOVERNANCE/
│   ├── 00_RULES/
│   │   ├── PHASE_6_GOVERNANCE_RULES.md
│   │   ├── PHASE_6_DECISION_REGISTER.md
│   │   └── PHASE_6_EMPTY_DOCUMENTS_REGISTER.md
│   ├── 01_SCOPE/
│   │   ├── PHASE_6_NEW_SYSTEM_SCOPE.md
│   │   ├── PHASE_6_FINAL_SCOPE_CONFIRMATION.md
│   │   ├── PHASE_6_SCOPE_GAP_ANALYSIS.md
│   │   └── PHASE_6_SCOPE_REVIEW_SUMMARY.md
│   ├── 02_PLANNING/
│   │   ├── PHASE_6_EXECUTION_PLAN.md
│   │   ├── PHASE_6_COMPLETE_SCOPE_AND_TASKS.md
│   │   ├── PHASE_6_CORRECTED_PLAN_SUMMARY.md
│   │   ├── PHASE_6_REVISION_SUMMARY.md
│   │   └── PHASE_6_CONSOLIDATION_SUMMARY.md
│   └── 03_DECISIONS/
│       └── (Decision documents)
│
├── 01_MASTER_DOCUMENTS/
│   ├── PHASE_6_FINAL_MASTER_CONSOLIDATED_PLAN.md ⭐ PRIMARY
│   ├── PHASE_6_MASTER_CONSOLIDATED.md
│   ├── PHASE_6_COMPLETE_TRACE_AND_PLAN_UPDATE.md
│   └── PHASE_6_REVIEW_COMPLETE_CONFIRMATION.md
│
├── 02_WEEK_PLANS/
│   ├── WEEK_0/
│   │   ├── PHASE6_WEEK0_DETAILED_PLAN.md
│   │   ├── PHASE6_WEEK0_EVIDENCE_PACK.md
│   │   └── WEEK0_CLOSURE_RECORD.md
│   ├── WEEK_1/
│   │   ├── PHASE6_WEEK1_DETAILED_PLAN.md
│   │   └── PHASE6_WEEK1_EVIDENCE_PACK.md
│   ├── WEEK_2/
│   │   ├── PHASE6_WEEK2_DETAILED_PLAN.md
│   │   └── PHASE6_WEEK2_EVIDENCE_PACK.md
│   ├── ... (Weeks 3-12)
│   └── WEEK_8_5/
│       └── PHASE6_WEEK8_5_DETAILED_PLAN.md
│
├── 03_MATRICES/
│   ├── PHASE6_DOCUMENT_REVIEW_MATRIX.md
│   ├── PHASE6_DOCUMENT_REVIEW_MATRIX_W0_W4_ONLY.md
│   ├── PHASE_6_UNIFIED_TASK_LIST.md
│   └── PHASE6_MATRIX_VERIFICATION_RESULTS.md
│
├── 04_TASKS_AND_TRACKS/
│   ├── TRACK_A/
│   ├── TRACK_A_R/
│   ├── TRACK_B/
│   ├── TRACK_C/
│   ├── TRACK_D0/
│   ├── TRACK_D/
│   ├── TRACK_E/
│   └── TRACK_F/ (if approved)
│
├── 05_GAPS_AND_ALARMS/
│   ├── PHASE_6_SCOPE_GAP_ANALYSIS.md
│   ├── PHASE_6_COMPLETE_REPLICATION_PLAN.md
│   ├── PHASE_6_VERIFIED_ROUTE_MAPPING.md
│   └── Compliance_Alarms_Register.md
│
├── 06_REVIEWS_AND_VERIFICATION/
│   ├── PHASE_6_COMPLETE_REVIEW_FINAL.md
│   ├── PHASE_6_ALL_RESTORED_FILES_REVIEW_FINAL.md
│   ├── PHASE_6_REMAINING_FILES_REVIEW_FINAL.md
│   ├── PHASE_6_100_PERCENT_COVERAGE_COMPLETE.md
│   ├── PHASE6_COMPREHENSIVE_VERIFICATION_REPORT.md
│   └── PHASE_6_COMPLETE_VERIFICATION_CHECKLIST.md
│
├── 07_LEGACY_PARITY/
│   ├── PHASE_6_LEGACY_PARITY_ADDITION.md
│   ├── PHASE_6_LEGACY_PARITY_CHECKLIST.md
│   ├── PHASE_6_NEPL_BASELINE_REVIEW.md
│   ├── PHASE_6_NEPL_REVIEW_VERIFICATION.md
│   └── PHASE_6_NISH_MAPPING_MATRIX_REVIEW.md
│
├── 08_EXECUTION/
│   ├── PHASE6_EXECUTION_ORDER_AND_START_CHECKLIST.md
│   ├── PHASE6_WEEK1_DAILY_EXECUTION_CHECKLIST.md
│   ├── PHASE6_WEEK1_TO_WEEK3_TASK_GRID.md
│   └── PHASE6_WEEK2_REUSE_PARITY_MATRIX.md
│
├── 09_SPECIFICATIONS/
│   ├── COSTING/
│   │   ├── COSTING_VIEW_RULES.md
│   │   ├── QCD_CONTRACT_v1.0.md
│   │   ├── D0_GATE_CHECKLIST.md
│   │   └── COST_TEMPLATE_SEED.md
│   ├── INFRASTRUCTURE/
│   │   ├── PHASE_6_INFRASTRUCTURE_AND_TOOLS.md
│   │   └── PHASE_6_TIMEFRAME_AND_COST_ESTIMATION.md
│   └── COST_ADDERS/
│       ├── PHASE_6_COST_ADDERS_FINAL_SPEC.md
│       ├── PHASE_6_COST_ADDERS_INTEGRATION_SUMMARY.md
│       └── PHASE_6_COST_ADDERS_TASK_INSERTS.md
│
├── 10_EVIDENCE/
│   ├── WEEK0_RUN_20260112_140401/
│   │   ├── WEEK0_SUMMARY.md
│   │   ├── WEEK0_COMPLETION_STATUS.md
│   │   ├── WEEK0_VERIFICATION_REPORT.md
│   │   ├── WEEK0_COMPLIANCE_DOCS/
│   │   └── WEEK0_PENDING_DOCS/
│   └── (Other week evidence packs)
│
├── 11_REFERENCE/
│   ├── PHASE_6_ALL_FILES_COMPREHENSIVE_INVENTORY.md
│   ├── PHASE_6_MASTER_FILE_INVENTORY.md
│   ├── PHASE_6_COMPLETE_FILE_DISCOVERY.md
│   └── PHASE_6_FILE_ACCESS_STRATEGY.md
│
└── README.md (Project overview and navigation guide)
```

---

## 📋 Document Transfer Plan

### Phase 1: Core Master Documents (Priority 1)

**Transfer these first:**
1. `PHASE_6_FINAL_MASTER_CONSOLIDATED_PLAN.md` → `01_MASTER_DOCUMENTS/`
2. `PHASE_6_MASTER_CONSOLIDATED.md` → `01_MASTER_DOCUMENTS/`
3. `PHASE_6_COMPLETE_TRACE_AND_PLAN_UPDATE.md` → `01_MASTER_DOCUMENTS/`
4. `PHASE_6_REVIEW_COMPLETE_CONFIRMATION.md` → `01_MASTER_DOCUMENTS/`

**Rationale:** These are the primary reference documents.

---

### Phase 2: Governance Documents (Priority 1)

**Transfer:**
1. `PHASE_6_GOVERNANCE_RULES.md` → `00_GOVERNANCE/00_RULES/`
2. `PHASE_6_DECISION_REGISTER.md` → `00_GOVERNANCE/00_RULES/`
3. `PHASE_6_EMPTY_DOCUMENTS_REGISTER.md` → `00_GOVERNANCE/00_RULES/`
4. `PHASE_6_NEW_SYSTEM_SCOPE.md` → `00_GOVERNANCE/01_SCOPE/`
5. `PHASE_6_FINAL_SCOPE_CONFIRMATION.md` → `00_GOVERNANCE/01_SCOPE/`
6. `PHASE_6_SCOPE_GAP_ANALYSIS.md` → `00_GOVERNANCE/01_SCOPE/`
7. `PHASE_6_SCOPE_REVIEW_SUMMARY.md` → `00_GOVERNANCE/01_SCOPE/`
8. `PHASE_6_EXECUTION_PLAN.md` → `00_GOVERNANCE/02_PLANNING/`
9. `PHASE_6_COMPLETE_SCOPE_AND_TASKS.md` → `00_GOVERNANCE/02_PLANNING/`
10. `PHASE_6_CORRECTED_PLAN_SUMMARY.md` → `00_GOVERNANCE/02_PLANNING/`
11. `PHASE_6_REVISION_SUMMARY.md` → `00_GOVERNANCE/02_PLANNING/`
12. `PHASE_6_CONSOLIDATION_SUMMARY.md` → `00_GOVERNANCE/02_PLANNING/`

**Rationale:** Governance documents establish rules and scope.

---

### Phase 3: Week Plans (Priority 2)

**Transfer all week plans:**
- `PHASE6_WEEK0_DETAILED_PLAN.md` through `PHASE6_WEEK12_DETAILED_PLAN.md` → `02_WEEK_PLANS/WEEK_X/`
- `PHASE6_WEEK8_5_DETAILED_PLAN.md` → `02_WEEK_PLANS/WEEK_8_5/`
- All evidence packs → `02_WEEK_PLANS/WEEK_X/` or `10_EVIDENCE/`

**Rationale:** Week plans provide execution roadmap.

---

### Phase 4: Matrices and Task Lists (Priority 2)

**Transfer:**
1. `PHASE6_DOCUMENT_REVIEW_MATRIX.md` → `03_MATRICES/`
2. `PHASE6_DOCUMENT_REVIEW_MATRIX_W0_W4_ONLY.md` → `03_MATRICES/`
3. `PHASE_6_UNIFIED_TASK_LIST.md` → `03_MATRICES/`
4. `PHASE6_MATRIX_VERIFICATION_RESULTS.md` → `03_MATRICES/`

**Rationale:** Matrices provide tracking and verification.

---

### Phase 5: Reviews and Verification (Priority 2)

**Transfer:**
1. `PHASE_6_COMPLETE_REVIEW_FINAL.md` → `06_REVIEWS_AND_VERIFICATION/`
2. `PHASE_6_ALL_RESTORED_FILES_REVIEW_FINAL.md` → `06_REVIEWS_AND_VERIFICATION/`
3. `PHASE_6_REMAINING_FILES_REVIEW_FINAL.md` → `06_REVIEWS_AND_VERIFICATION/`
4. `PHASE_6_100_PERCENT_COVERAGE_COMPLETE.md` → `06_REVIEWS_AND_VERIFICATION/`
5. `PHASE6_COMPREHENSIVE_VERIFICATION_REPORT.md` → `06_REVIEWS_AND_VERIFICATION/`
6. `PHASE_6_COMPLETE_VERIFICATION_CHECKLIST.md` → `06_REVIEWS_AND_VERIFICATION/`

**Rationale:** Review documents provide verification and completeness.

---

### Phase 6: Legacy Parity (Priority 2)

**Transfer:**
1. `PHASE_6_LEGACY_PARITY_ADDITION.md` → `07_LEGACY_PARITY/`
2. `PHASE_6_LEGACY_PARITY_CHECKLIST.md` → `07_LEGACY_PARITY/`
3. `PHASE_6_NEPL_BASELINE_REVIEW.md` → `07_LEGACY_PARITY/`
4. `PHASE_6_NEPL_REVIEW_VERIFICATION.md` → `07_LEGACY_PARITY/`
5. `PHASE_6_NISH_MAPPING_MATRIX_REVIEW.md` → `07_LEGACY_PARITY/`

**Rationale:** Legacy parity ensures completeness.

---

### Phase 7: Execution Documents (Priority 2)

**Transfer:**
1. `PHASE6_EXECUTION_ORDER_AND_START_CHECKLIST.md` → `08_EXECUTION/`
2. `PHASE6_WEEK1_DAILY_EXECUTION_CHECKLIST.md` → `08_EXECUTION/`
3. `PHASE6_WEEK1_TO_WEEK3_TASK_GRID.md` → `08_EXECUTION/`
4. `PHASE6_WEEK2_REUSE_PARITY_MATRIX.md` → `08_EXECUTION/`

**Rationale:** Execution documents provide operational guidance.

---

### Phase 8: Specifications (Priority 3)

**Transfer:**
1. `docs/PHASE_6/COSTING_VIEW_RULES.md` → `09_SPECIFICATIONS/COSTING/`
2. `docs/PHASE_6/WEEK0_CLOSURE_RECORD.md` → `09_SPECIFICATIONS/COSTING/`
3. `docs/PHASE_6/WEEK0_DAY7_VALIDATION_GATE.md` → `09_SPECIFICATIONS/COSTING/`
4. `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COST_ADDERS_FINAL_SPEC.md` → `09_SPECIFICATIONS/COST_ADDERS/`
5. `docs/PHASE_5/00_GOVERNANCE/PHASE_6_INFRASTRUCTURE_AND_TOOLS.md` → `09_SPECIFICATIONS/INFRASTRUCTURE/`
6. `docs/PHASE_5/00_GOVERNANCE/PHASE_6_TIMEFRAME_AND_COST_ESTIMATION.md` → `09_SPECIFICATIONS/INFRASTRUCTURE/`

**Rationale:** Specifications provide technical details.

---

### Phase 9: Evidence Files (Priority 3)

**Transfer:**
- `evidence/PHASE6_WEEK0_RUN_20260112_140401/` → `10_EVIDENCE/WEEK0_RUN_20260112_140401/`
- All other evidence packs → `10_EVIDENCE/`

**Rationale:** Evidence provides audit trail.

---

### Phase 10: Reference Documents (Priority 3)

**Transfer:**
1. `PHASE_6_ALL_FILES_COMPREHENSIVE_INVENTORY.md` → `11_REFERENCE/`
2. `PHASE_6_MASTER_FILE_INVENTORY.md` → `11_REFERENCE/`
3. `PHASE_6_COMPLETE_FILE_DISCOVERY.md` → `11_REFERENCE/`
4. `PHASE_6_FILE_ACCESS_STRATEGY.md` → `11_REFERENCE/`

**Rationale:** Reference documents provide file tracking.

---

## 🔒 Rules and Governance for New Folder

### Rule 1: Documentation-Only Initially

- **Phase 1:** Only documentation files transferred
- **Phase 2:** Code files copied/transferred only when needed for implementation
- **Rationale:** Keep folder clean and organized

---

### Rule 2: Folder Structure Lock

- **Once created:** Folder structure is locked
- **Changes require:** Governance approval via Decision Register
- **Rationale:** Maintain organization and findability

---

### Rule 3: File Naming Convention

- **Format:** `PHASE_6_<CATEGORY>_<DESCRIPTION>.md`
- **Examples:**
  - `PHASE_6_GOVERNANCE_RULES.md`
  - `PHASE_6_WEEK0_DETAILED_PLAN.md`
  - `PHASE_6_COMPLETE_REVIEW_FINAL.md`
- **Rationale:** Consistent naming for easy search

---

### Rule 4: Master Document Authority

- **Primary Reference:** `01_MASTER_DOCUMENTS/PHASE_6_FINAL_MASTER_CONSOLIDATED_PLAN.md`
- **All other documents:** Support and detail documents
- **Rationale:** Single source of truth

---

### Rule 5: Code Migration Strategy

- **When to migrate code:**
  - Only when actively working on that component
  - Copy, don't move (keep original in source folder)
  - Update documentation to reference new location
- **Rationale:** Gradual migration, maintain source

---

### Rule 6: Evidence Preservation

- **All evidence:** Preserved in `10_EVIDENCE/`
- **Week evidence:** Organized by week
- **Rationale:** Complete audit trail

---

## 📝 Transfer Script Plan

### Option 1: Manual Transfer (Recommended Initially)

**Steps:**
1. Create folder structure
2. Copy files one phase at a time
3. Verify each phase before proceeding
4. Update cross-references

**Pros:** Controlled, verifiable  
**Cons:** Time-consuming

---

### Option 2: Automated Script

**Script would:**
1. Create folder structure
2. Copy files based on mapping
3. Update cross-references
4. Generate transfer log

**Pros:** Fast, repeatable  
**Cons:** Requires verification

---

## 🎯 Recommended Approach

### Step 1: Create Folder Structure ✅

Create the folder structure first (empty folders).

### Step 2: Transfer Phase 1 (Master Documents) ✅

Transfer the 4 master documents first.

### Step 3: Review and Verify ✅

Review folder structure and transferred files.

### Step 4: Transfer Remaining Phases ✅

Transfer remaining documents phase by phase.

### Step 5: Create README ✅

Create comprehensive README for navigation.

### Step 6: Lock Structure ✅

Lock folder structure and document in governance.

---

## 📋 File Mapping Table

| Source File | Destination | Priority | Notes |
|-------------|-------------|----------|-------|
| `PHASE_6_FINAL_MASTER_CONSOLIDATED_PLAN.md` | `01_MASTER_DOCUMENTS/` | P0 | Primary reference |
| `PHASE_6_GOVERNANCE_RULES.md` | `00_GOVERNANCE/00_RULES/` | P0 | Core rules |
| `PHASE_6_DECISION_REGISTER.md` | `00_GOVERNANCE/00_RULES/` | P0 | Decision tracking |
| `PHASE6_WEEK0_DETAILED_PLAN.md` | `02_WEEK_PLANS/WEEK_0/` | P1 | Week plans |
| `PHASE_6_UNIFIED_TASK_LIST.md` | `03_MATRICES/` | P1 | Task tracking |
| `PHASE_6_COMPLETE_REVIEW_FINAL.md` | `06_REVIEWS_AND_VERIFICATION/` | P1 | Review summary |
| `PHASE_6_LEGACY_PARITY_CHECKLIST.md` | `07_LEGACY_PARITY/` | P1 | Parity verification |
| `PHASE6_EXECUTION_ORDER_AND_START_CHECKLIST.md` | `08_EXECUTION/` | P1 | Execution guide |
| `docs/PHASE_6/COSTING_VIEW_RULES.md` | `09_SPECIFICATIONS/COSTING/` | P2 | Technical spec |
| `evidence/PHASE6_WEEK0_RUN_20260112_140401/` | `10_EVIDENCE/WEEK0_RUN_20260112_140401/` | P2 | Evidence |

---

## 📝 README Template

```markdown
# NSW Estimation Software V1.0
## Phase 6 Planning and Documentation

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** Documentation Phase

---

## 📚 Quick Navigation

### Primary Documents
- **Master Plan:** `01_MASTER_DOCUMENTS/PHASE_6_FINAL_MASTER_CONSOLIDATED_PLAN.md`
- **Governance Rules:** `00_GOVERNANCE/00_RULES/PHASE_6_GOVERNANCE_RULES.md`
- **Execution Guide:** `08_EXECUTION/PHASE6_EXECUTION_ORDER_AND_START_CHECKLIST.md`

### Week Plans
- Week 0-12: `02_WEEK_PLANS/WEEK_X/`

### Matrices
- Task List: `03_MATRICES/PHASE_6_UNIFIED_TASK_LIST.md`
- Document Review: `03_MATRICES/PHASE6_DOCUMENT_REVIEW_MATRIX.md`

---

## 🎯 Purpose

This folder contains all Phase 6 planning, documentation, and governance files.
It serves as the reference baseline for NSW Estimation Software V1.0 development.

---

## 📁 Folder Structure

[Detailed folder structure explanation]

---

## 🔒 Rules

1. Documentation-only initially
2. Folder structure locked
3. Code migration only when needed
4. Master document is authority
5. Evidence preserved

---

## 📝 Next Steps

1. Review this plan
2. Approve folder structure
3. Execute transfer
4. Create README
5. Lock structure
```

---

## ✅ Verification Checklist

### Before Transfer

- [ ] Folder structure approved
- [ ] File mapping verified
- [ ] Transfer plan approved
- [ ] Rules and governance approved

### During Transfer

- [ ] Phase 1 complete (Master Documents)
- [ ] Phase 2 complete (Governance)
- [ ] Phase 3 complete (Week Plans)
- [ ] Phase 4 complete (Matrices)
- [ ] Phase 5 complete (Reviews)
- [ ] Phase 6 complete (Legacy Parity)
- [ ] Phase 7 complete (Execution)
- [ ] Phase 8 complete (Specifications)
- [ ] Phase 9 complete (Evidence)
- [ ] Phase 10 complete (Reference)

### After Transfer

- [ ] All files transferred
- [ ] Folder structure verified
- [ ] Cross-references updated
- [ ] README created
- [ ] Structure locked

---

## 🎯 Recommendations

### Immediate Actions

1. **Review this plan** - Verify folder structure and transfer approach
2. **Approve structure** - Confirm organization makes sense
3. **Create folder structure** - Create empty folders first
4. **Transfer Phase 1** - Start with master documents
5. **Verify and iterate** - Review after each phase

### Short-term Actions

6. **Complete all transfers** - Transfer all documentation
7. **Create README** - Navigation guide
8. **Lock structure** - Document in governance
9. **Update cross-references** - Fix any broken links

### Medium-term Actions

10. **Code migration planning** - Plan when to migrate code files
11. **Reference folder maintenance** - Keep reference folder updated
12. **Documentation updates** - Update docs as code migrates

---

## 📊 Estimated File Count

**Total Files to Transfer:** ~138+ files

**By Category:**
- Master Documents: 4 files
- Governance: 20+ files
- Week Plans: 13 files + evidence
- Matrices: 5+ files
- Reviews: 10+ files
- Legacy Parity: 5+ files
- Execution: 5+ files
- Specifications: 10+ files
- Evidence: 50+ files
- Reference: 5+ files

---

## 🔒 Governance Lock Statement

**Once folder structure is created and approved:**
- Structure is **LOCKED**
- Changes require **governance approval**
- Documented in **Decision Register**
- Rationale required for any changes

---

**Status:** 📋 PLAN FOR REVIEW  
**Date:** 2025-01-27  
**Next Action:** Review plan, approve structure, then execute transfer
