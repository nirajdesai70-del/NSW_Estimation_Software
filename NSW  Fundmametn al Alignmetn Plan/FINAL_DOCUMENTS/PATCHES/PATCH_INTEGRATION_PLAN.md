# Patch Integration Plan — Fundamentals Gap Correction

**Project:** NSW Estimation Software  
**Purpose:** Map patches to documents and integrate with existing BOM planning structure  
**Status:** 📋 PLANNING (Integration Plan)  
**Date:** 2025-01-XX

---

## 📋 EXECUTIVE SUMMARY

This document maps:
1. **Which patches go in which documents**
2. **How to integrate fundamentals work with existing BOM planning**
3. **Where patch plan fits in the overall structure**

---

## 1️⃣ PATCH-TO-DOCUMENT MAPPING

### Patch P1 — Feeder Template Filter Standardization

**Patch Location:**
- **Primary:** `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P1)
- **Integration Points:**
  - `PLANNING/GOVERNANCE/BOM_ENGINE_BLUEPRINT.md` (if exists, add filter requirement)
  - `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` (add TemplateType filter to contract)
  - `PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md` (add filter requirement to flow)

**When Applied:**
- During Phase-2 execution window (if verification fails)
- Or during fundamentals execution window (if triggered)

**Documentation Updates Required:**
- Update BOM Engine contract to require TemplateType='FEEDER' filter
- Update Feeder BOM canonical flow to include filter step
- Add to verification queries (VQ-005 already covers this)

---

### Patch P2 — Quotation Ownership Enforcement

**Patch Location:**
- **Primary:** `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P2)
- **Integration Points:**
  - `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` (if ownership gaps found)
  - `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` (add QuotationId validation)
  - `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md` (add ownership check)

**When Applied:**
- During fundamentals execution window (if VQ-004 fails)
- Or during Phase-2 execution window (if ownership issues found)

**Documentation Updates Required:**
- Add QuotationId validation to BOM Engine contract
- Update gap register if ownership gaps are identified
- Add ownership verification to execution checklist

---

### Patch P3 — Copy-Never-Link Enforcement Guard

**Patch Location:**
- **Primary:** `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P3)
- **Integration Points:**
  - `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md` (reinforce copy-never-link)
  - `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` (add guard requirement)
  - `PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md` (add guard to flow)

**When Applied:**
- During fundamentals execution window (if VQ-005 shows mutation risk)
- Or during Phase-2 execution window (if mutation detected)

**Documentation Updates Required:**
- Reinforce copy-never-link in BOM Principle document
- Add guard requirement to BOM Engine contract
- Update canonical flow to include guard

---

### Patch P4 — Legacy Data Normalization (Optional)

**Patch Location:**
- **Primary:** `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P4)
- **Integration Points:**
  - `PLANNING/RELEASE_PACKS/PHASE2/04_EXECUTION_SCRIPTS/` (add normalization script)
  - `PLANNING/RELEASE_PACKS/PHASE2/06_RISKS_AND_ROLLBACK.md` (add normalization risk)

**When Applied:**
- Only if legacy data corruption is found
- Requires separate approval (last resort)

**Documentation Updates Required:**
- Create normalization script in execution scripts folder
- Document normalization process in risks document
- Add to execution checklist as optional step

---

## 2️⃣ INTEGRATION WITH EXISTING BOM PLANNING

### 2.1 Master Planning Index Integration

**File:** `PLANNING/MASTER_PLANNING_INDEX.md`

**Integration Point:**
- Add new section: **"Fundamentals Gap Correction"** (before Phase-1 or as Phase-0)

**Proposed Addition:**
```markdown
## 0) Fundamentals Gap Correction (Foundation)

### Objective
- Close GAP-001 (Feeder Master definition)
- Close GAP-002 (Proposal BOM Master definition)
- Close GAP-005 (Canonical hierarchy)
- Close GAP-006 (Master→Instance mapping)

**Status:** 📌 **READY** (Planning Complete)

### Canonical Pack
```
PLANNING/FUNDAMENTS_CORRECTION/
├─ FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md
├─ FEEDER_MASTER_BACKEND_DESIGN_v1.0.md
├─ PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md
├─ CANONICAL_BOM_HIERARCHY_v1.0.md
├─ MASTER_INSTANCE_MAPPING_v1.0.md
├─ FUNDAMENTALS_VERIFICATION_QUERIES.md
├─ FUNDAMENTALS_VERIFICATION_CHECKLIST.md
├─ PATCH_PLAN.md
└─ EXECUTION_WINDOW_SOP.md
```

### Gate State
- **Gate-1:** 📌 READY (planning completeness verified)
- **Gate-2:** ⏳ BLOCKED (execution window - requires execution approval)
- **Gate-3:** ⏳ BLOCKED (verification - requires Gate-2 completion)

### Rule
- ❌ No runtime/DB/UI work until execution window
```

**Action Required:**
- [ ] Add fundamentals section to MASTER_PLANNING_INDEX.md
- [ ] Update phase numbering if needed
- [ ] Cross-reference with other phases

---

### 2.2 BOM Gap Register Integration

**File:** `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`

**Integration Points:**
- Add fundamentals gaps (GAP-001, GAP-002, GAP-005, GAP-006) to gap register
- Link patches to gaps (P1→GAP-001, P2→GAP-002, etc.)

**Proposed Addition:**
```markdown
## Fundamentals Gaps (New Section)

### GAP-001 — Feeder Master Definition Missing
- **Status:** 📌 READY (documentation frozen)
- **Closure Path:** Verification (VQ-001, VQ-002) + Patch P1 (if needed)
- **Patch:** P1 (Feeder Template Filter Standardization)
- **Reference:** `PLANNING/FUNDAMENTS_CORRECTION/FEEDER_MASTER_BACKEND_DESIGN_v1.0.md`

### GAP-002 — Proposal BOM Master Container Missing
- **Status:** 📌 READY (documentation frozen)
- **Closure Path:** Verification (VQ-003, VQ-004) + Patch P2 (if needed)
- **Patch:** P2 (Quotation Ownership Enforcement)
- **Reference:** `PLANNING/FUNDAMENTS_CORRECTION/PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md`

### GAP-005 — Canonical Hierarchy Missing
- **Status:** 📌 READY (documentation frozen)
- **Closure Path:** Documentation review (no patches needed)
- **Reference:** `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md`

### GAP-006 — Master→Instance Mapping Missing
- **Status:** 📌 READY (documentation frozen)
- **Closure Path:** Documentation review + Verification (VQ-005)
- **Patch:** P3 (Copy-Never-Link Enforcement Guard) if needed
- **Reference:** `PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md`
```

**Action Required:**
- [ ] Add fundamentals gaps section to BOM_GAP_REGISTER.md
- [ ] Link patches to gaps
- [ ] Update gap status as verification completes

---

### 2.3 Release Pack Structure Integration

**Proposed Structure:**
```
PLANNING/RELEASE_PACKS/FUNDAMENTALS/
├─ 00_README_RUNBOOK.md (references EXECUTION_WINDOW_SOP.md)
├─ STATUS.md
├─ 01_BASELINE_BUNDLE.md (link to FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md)
├─ 02_VERIFICATION/
│  ├─ VERIFICATION_QUERIES.md (link to FUNDAMENTALS_VERIFICATION_QUERIES.md)
│  └─ VERIFICATION_CHECKLIST.md (link to FUNDAMENTALS_VERIFICATION_CHECKLIST.md)
├─ 03_PATCHES/
│  └─ PATCH_PLAN.md (link to PATCH_PLAN.md)
└─ 04_RISKS_AND_ROLLBACK.md
```

**Action Required:**
- [ ] Create `PLANNING/RELEASE_PACKS/FUNDAMENTALS/` folder
- [ ] Create release pack structure
- [ ] Link to existing fundamentals documents
- [ ] Create STATUS.md for fundamentals phase

---

### 2.4 Execution Readiness Checklist Integration

**File:** `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md`

**Integration Points:**
- Add fundamentals verification to checklist
- Add patch plan review to checklist

**Proposed Addition:**
```markdown
## Fundamentals Gap Correction Readiness

- [ ] Fundamentals baseline bundle reviewed (`PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md`)
- [ ] Verification queries reviewed (`PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md`)
- [ ] Verification checklist reviewed (`PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md`)
- [ ] Patch plan reviewed (`PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`)
- [ ] Execution SOP reviewed (`PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`)
- [ ] Fundamentals gaps understood (GAP-001, GAP-002, GAP-005, GAP-006)
```

**Action Required:**
- [ ] Add fundamentals section to execution readiness checklist
- [ ] Link to all fundamentals documents

---

## 3️⃣ DOCUMENT INTEGRATION MATRIX

| Document | Integration Location | Action Required |
|----------|---------------------|-----------------|
| **FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md** | `PLANNING/RELEASE_PACKS/FUNDAMENTALS/01_BASELINE_BUNDLE.md` | Create release pack, link to bundle |
| **FEEDER_MASTER_BACKEND_DESIGN_v1.0.md** | `PLANNING/FUNDAMENTS_CORRECTION/` (keep) | Reference from release pack |
| **PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md** | `PLANNING/FUNDAMENTS_CORRECTION/` (keep) | Reference from release pack |
| **CANONICAL_BOM_HIERARCHY_v1.0.md** | `PLANNING/FUNDAMENTS_CORRECTION/` (keep) | Reference from release pack |
| **MASTER_INSTANCE_MAPPING_v1.0.md** | `PLANNING/FUNDAMENTS_CORRECTION/` (keep) | Reference from release pack |
| **FUNDAMENTALS_VERIFICATION_QUERIES.md** | `PLANNING/RELEASE_PACKS/FUNDAMENTALS/02_VERIFICATION/` | Copy or link to release pack |
| **FUNDAMENTALS_VERIFICATION_CHECKLIST.md** | `PLANNING/RELEASE_PACKS/FUNDAMENTALS/02_VERIFICATION/` | Copy or link to release pack |
| **PATCH_PLAN.md** | `PLANNING/RELEASE_PACKS/FUNDAMENTALS/03_PATCHES/` | Copy or link to release pack |
| **EXECUTION_WINDOW_SOP.md** | `PLANNING/RELEASE_PACKS/FUNDAMENTALS/00_README_RUNBOOK.md` | Reference from runbook |

---

## 4️⃣ PATCH APPLICATION WORKFLOW

### 4.1 When Patches Are Applied

**Scenario 1: Fundamentals Execution Window**
- Verification runs (VQ-001 through VQ-005)
- If any fail → Patch decision gate (Phase 2 of SOP)
- Approved patches applied → Re-verification

**Scenario 2: Phase-2 Execution Window**
- Phase-2 verification runs
- If fundamentals-related issues found → Reference PATCH_PLAN.md
- Apply relevant patches (P1, P2, or P3)

**Scenario 3: Phase-3/4/5 Execution Window**
- Cross-phase verification runs
- If fundamentals violations found → Reference PATCH_PLAN.md
- Apply relevant patches

---

### 4.2 Patch Documentation Updates

**When Patch P1 Applied:**
- [ ] Update `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` (add TemplateType filter)
- [ ] Update `PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md` (add filter step)
- [ ] Update `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` (mark GAP-001 closed)

**When Patch P2 Applied:**
- [ ] Update `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` (add QuotationId validation)
- [ ] Update `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` (mark GAP-002 closed)
- [ ] Update `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md` (add ownership check)

**When Patch P3 Applied:**
- [ ] Update `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md` (reinforce copy-never-link)
- [ ] Update `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` (add guard)
- [ ] Update `PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md` (add guard)

**When Patch P4 Applied:**
- [ ] Create normalization script in `PLANNING/RELEASE_PACKS/PHASE2/04_EXECUTION_SCRIPTS/`
- [ ] Update `PLANNING/RELEASE_PACKS/PHASE2/06_RISKS_AND_ROLLBACK.md` (add normalization risk)
- [ ] Document in execution summary

---

## 5️⃣ INTEGRATION CHECKLIST

### Phase 1: Document Structure
- [ ] Create `PLANNING/RELEASE_PACKS/FUNDAMENTALS/` folder
- [ ] Create release pack structure (00-04 folders)
- [ ] Create STATUS.md for fundamentals phase
- [ ] Create 00_README_RUNBOOK.md (references EXECUTION_WINDOW_SOP.md)

### Phase 2: Master Index Integration
- [ ] Add fundamentals section to `PLANNING/MASTER_PLANNING_INDEX.md`
- [ ] Update phase numbering if needed
- [ ] Cross-reference with other phases

### Phase 3: Gap Register Integration
- [ ] Add fundamentals gaps to `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`
- [ ] Link patches to gaps
- [ ] Update gap status tracking

### Phase 4: Execution Readiness Integration
- [ ] Add fundamentals section to `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md`
- [ ] Link to all fundamentals documents
- [ ] Add patch plan review

### Phase 5: Cross-Reference Updates
- [ ] Update all documents that reference BOM planning to include fundamentals
- [ ] Update cross-references in existing BOM documents
- [ ] Verify all links work

---

## 6️⃣ RECOMMENDED INTEGRATION ORDER

1. **First:** Create release pack structure (Phase 1)
2. **Second:** Update master planning index (Phase 2)
3. **Third:** Update gap register (Phase 3)
4. **Fourth:** Update execution readiness (Phase 4)
5. **Fifth:** Cross-reference updates (Phase 5)

---

## 7️⃣ INTEGRATION SUMMARY

### Documents Created (Fundamentals)
- ✅ PATCH_PLAN.md (created)
- ✅ EXECUTION_WINDOW_SOP.md (created)
- ⏳ FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md (to be created)
- ⏳ Individual design documents (to be created)
- ⏳ Verification queries (to be created)
- ⏳ Verification checklist (to be created)

### Documents to Update (Integration)
- ⏳ MASTER_PLANNING_INDEX.md (add fundamentals section)
- ⏳ BOM_GAP_REGISTER.md (add fundamentals gaps)
- ⏳ EXECUTION_READINESS_CHECKLIST.md (add fundamentals section)
- ⏳ BOM_ENGINE_CONTRACT.md (add patch requirements if patches applied)
- ⏳ FEEDER_BOM_CANONICAL_FLOW.md (add patch requirements if patches applied)

### Release Pack Structure (New)
- ⏳ `PLANNING/RELEASE_PACKS/FUNDAMENTALS/` (to be created)
- ⏳ Release pack documents (to be created)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial patch integration plan created |

---

**END OF PATCH INTEGRATION PLAN**

