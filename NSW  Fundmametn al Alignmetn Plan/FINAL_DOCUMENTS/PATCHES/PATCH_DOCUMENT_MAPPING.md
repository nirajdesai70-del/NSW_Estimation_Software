# Patch-to-Document Mapping — Quick Reference

**Project:** NSW Estimation Software  
**Purpose:** Quick reference for which patches go in which documents  
**Status:** 📋 REFERENCE DOCUMENT

---

## 📋 PATCH SUMMARY TABLE

| Patch ID | Patch Name | Primary Document | Integration Documents | When Applied |
|----------|------------|------------------|----------------------|--------------|
| **P1** | Feeder Template Filter | `PATCH_PLAN.md` | `BOM_ENGINE_CONTRACT.md`<br>`FEEDER_BOM_CANONICAL_FLOW.md` | If VQ-005 fails |
| **P2** | Quotation Ownership | `PATCH_PLAN.md` | `BOM_ENGINE_CONTRACT.md`<br>`BOM_GAP_REGISTER.md`<br>`EXECUTION_READINESS_CHECKLIST.md` | If VQ-004 fails |
| **P3** | Copy-Never-Link Guard | `PATCH_PLAN.md` | `BOM_PRINCIPLE_LOCKED.md`<br>`BOM_ENGINE_CONTRACT.md`<br>`FEEDER_BOM_CANONICAL_FLOW.md` | If VQ-005 shows mutation |
| **P4** | Legacy Normalization | `PATCH_PLAN.md` | `RELEASE_PACKS/PHASE2/04_EXECUTION_SCRIPTS/`<br>`RELEASE_PACKS/PHASE2/06_RISKS_AND_ROLLBACK.md` | Last resort only |

---

## 🔗 DETAILED PATCH MAPPING

### Patch P1 — Feeder Template Filter Standardization

**Primary Location:**
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P1)

**Integration Points:**
1. **`PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md`**
   - Add requirement: "All feeder template queries MUST filter `TemplateType='FEEDER'`"
   - Update method signature documentation

2. **`PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md`**
   - Add step: "Filter templates by TemplateType='FEEDER'"
   - Update flow diagram

3. **`PLANNING/GOVERNANCE/BOM_ENGINE_BLUEPRINT.md`** (if exists)
   - Add filter requirement to blueprint

**Documentation Updates When Applied:**
- ✅ Update BOM Engine contract
- ✅ Update canonical flow
- ✅ Mark GAP-001 closed in gap register

---

### Patch P2 — Quotation Ownership Enforcement

**Primary Location:**
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P2)

**Integration Points:**
1. **`PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md`**
   - Add validation: "QuotationId MUST be present for all runtime entity creation"
   - Add error handling for missing QuotationId

2. **`PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`**
   - Link P2 to ownership-related gaps
   - Update gap closure status

3. **`PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md`**
   - Add check: "Verify QuotationId present in all runtime entities"

**Documentation Updates When Applied:**
- ✅ Update BOM Engine contract
- ✅ Update gap register
- ✅ Update execution checklist
- ✅ Mark GAP-002 closed

---

### Patch P3 — Copy-Never-Link Enforcement Guard

**Primary Location:**
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P3)

**Integration Points:**
1. **`PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md`**
   - Reinforce copy-never-link principle
   - Add guard requirement

2. **`PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md`**
   - Add guard: "Reject writes to master_boms during quotation context"
   - Add validation method

3. **`PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md`**
   - Add guard step to flow
   - Update flow diagram

**Documentation Updates When Applied:**
- ✅ Update BOM principle document
- ✅ Update BOM Engine contract
- ✅ Update canonical flow
- ✅ Mark GAP-006 closed (if related)

---

### Patch P4 — Legacy Data Normalization (Optional)

**Primary Location:**
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` (Section 2, P4)

**Integration Points:**
1. **`PLANNING/RELEASE_PACKS/PHASE2/04_EXECUTION_SCRIPTS/`**
   - Create: `normalize_legacy_data.sql`
   - Document normalization process

2. **`PLANNING/RELEASE_PACKS/PHASE2/06_RISKS_AND_ROLLBACK.md`**
   - Add normalization risk section
   - Document rollback procedure

**Documentation Updates When Applied:**
- ✅ Create normalization script
- ✅ Update risks document
- ✅ Document in execution summary

---

## 📁 DOCUMENT INTEGRATION LOCATIONS

### Main Planning Documents

| Document | Location | Integration Action |
|----------|----------|-------------------|
| **MASTER_PLANNING_INDEX.md** | `PLANNING/MASTER_PLANNING_INDEX.md` | Add fundamentals section (Phase-0 or before Phase-1) |
| **BOM_GAP_REGISTER.md** | `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` | Add fundamentals gaps section |
| **EXECUTION_READINESS_CHECKLIST.md** | `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md` | Add fundamentals readiness section |

### Phase-Specific Documents

| Document | Location | Integration Action |
|----------|----------|-------------------|
| **BOM_ENGINE_CONTRACT.md** | `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` | Add patch requirements (P1, P2, P3) |
| **FEEDER_BOM_CANONICAL_FLOW.md** | `PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md` | Add patch steps (P1, P3) |
| **BOM_PRINCIPLE_LOCKED.md** | `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md` | Reinforce copy-never-link (P3) |

### Release Pack Structure

| Folder | Location | Contents |
|--------|----------|----------|
| **FUNDAMENTALS/** | `PLANNING/RELEASE_PACKS/FUNDAMENTALS/` | Fundamentals release pack (to be created) |
| **EXECUTION_SCRIPTS/** | `PLANNING/RELEASE_PACKS/PHASE2/04_EXECUTION_SCRIPTS/` | Normalization script (P4) |

---

## 🔄 INTEGRATION WORKFLOW

### Step 1: Review Patch Plan
- [ ] Review `PATCH_PLAN.md`
- [ ] Understand all 4 patches
- [ ] Understand trigger conditions

### Step 2: Identify Integration Points
- [ ] Map patches to existing documents (use table above)
- [ ] Identify which documents need updates
- [ ] Plan update sequence

### Step 3: Update Master Planning Index
- [ ] Add fundamentals section to `MASTER_PLANNING_INDEX.md`
- [ ] Reference fundamentals release pack
- [ ] Update phase status

### Step 4: Update Gap Register
- [ ] Add fundamentals gaps (GAP-001, GAP-002, GAP-005, GAP-006)
- [ ] Link patches to gaps
- [ ] Set gap status

### Step 5: Update Execution Readiness
- [ ] Add fundamentals section to checklist
- [ ] Link to fundamentals documents
- [ ] Add patch plan review

### Step 6: Create Release Pack Structure
- [ ] Create `PLANNING/RELEASE_PACKS/FUNDAMENTALS/` folder
- [ ] Create release pack documents
- [ ] Link to existing fundamentals documents

### Step 7: Update Phase Documents (When Patches Applied)
- [ ] Update BOM Engine contract (if P1, P2, P3 applied)
- [ ] Update canonical flow (if P1, P3 applied)
- [ ] Update BOM principle (if P3 applied)
- [ ] Create normalization script (if P4 applied)

---

## ✅ INTEGRATION CHECKLIST

### Immediate (Planning Phase)
- [ ] Review patch integration plan
- [ ] Create fundamentals release pack structure
- [ ] Update master planning index
- [ ] Update gap register
- [ ] Update execution readiness checklist

### During Execution (If Patches Applied)
- [ ] Update BOM Engine contract
- [ ] Update canonical flow
- [ ] Update BOM principle (if P3)
- [ ] Create normalization script (if P4)
- [ ] Update gap register (mark gaps closed)
- [ ] Document in execution summary

---

## 📊 QUICK REFERENCE: PATCH → DOCUMENT

```
P1 (Feeder Filter)
  → PATCH_PLAN.md (primary)
  → BOM_ENGINE_CONTRACT.md (integration)
  → FEEDER_BOM_CANONICAL_FLOW.md (integration)

P2 (Quotation Ownership)
  → PATCH_PLAN.md (primary)
  → BOM_ENGINE_CONTRACT.md (integration)
  → BOM_GAP_REGISTER.md (integration)
  → EXECUTION_READINESS_CHECKLIST.md (integration)

P3 (Copy-Never-Link Guard)
  → PATCH_PLAN.md (primary)
  → BOM_PRINCIPLE_LOCKED.md (integration)
  → BOM_ENGINE_CONTRACT.md (integration)
  → FEEDER_BOM_CANONICAL_FLOW.md (integration)

P4 (Legacy Normalization)
  → PATCH_PLAN.md (primary)
  → EXECUTION_SCRIPTS/ (integration)
  → RISKS_AND_ROLLBACK.md (integration)
```

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial patch-to-document mapping created |

---

**END OF PATCH DOCUMENT MAPPING**

