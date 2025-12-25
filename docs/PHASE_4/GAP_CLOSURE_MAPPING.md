# Gap Closure Mapping - Phase 4 Coverage Analysis

**Version:** 1.0  
**Date:** 2025-12-18  
**Status:** ACTIVE - Analysis Document  
**Purpose:** Map identified gaps (BOM-GAP-*, PB-GAP-*, MB-GAP-*) to Phase 4 tasks or separate work

---

## 🔍 Gap Status Summary

### Open Gaps Identified

| Gap ID | Description | Status | Severity | Phase 4 Coverage | Action Needed |
|--------|-------------|--------|----------|------------------|---------------|
| BOM-GAP-001 | Feeder Template Apply Creates New Feeder Every Time | ⏳ OPEN | High | ❓ Need Analysis | Determine if covered by S2/S3/S4 |
| BOM-GAP-002 | Feeder Template Apply Missing Clear-Before-Copy | ⏳ OPEN | High | ❓ Need Analysis | Determine if covered by S2/S3/S4 |
| BOM-GAP-004 | BOM Copy Operations Missing History/Backup | ⏳ PARTIALLY RESOLVED | High | ❓ Need Analysis | Verify if fully addressed |
| BOM-GAP-005 | BOM Node Edits Missing History/Backup | ⏳ OPEN | Medium | ❓ Need Analysis | Determine if covered |
| BOM-GAP-006 | Lookup Pipeline Preservation Not Verified | ⏳ OPEN | Medium | ❓ Need Analysis | May be covered by S3 alignment |
| BOM-GAP-007 | Copy Operations Not Implemented | ⏳ PARTIALLY RESOLVED | High | ❓ Need Analysis | Verify if fully addressed |
| BOM-GAP-013 | Template Data Missing (Phase-2 Data Readiness) | ⏳ OPEN | High | ❓ Need Analysis | Separate from refactoring? |
| PB-GAP-003 | Quantity chain correctness + feeder discovery edge cases | ⏳ OPEN | - | ❓ Need Analysis | Determine if covered |
| PB-GAP-004 | Instance isolation under reuse/apply flows | ⏳ OPEN | - | ❓ Need Analysis | May be covered by S2 isolation |
| MB-GAP-001 | [See gap register] | ⏳ OPEN | - | ❓ Need Analysis | Determine if covered |

### Closed Gaps

| Gap ID | Description | Status | Notes |
|--------|-------------|--------|-------|
| PB-GAP-001 | L2 Write Enforcement Missing | ✅ CLOSED | Already fixed |
| PB-GAP-002 | Illegal Defaults (MakeId=0, SeriesId=0) | ✅ CLOSED | Already fixed |
| BOM-GAP-003 | Line Item Edits Missing History/Backup | ✅ CLOSED | Already fixed |

---

## 📊 Phase 4 Coverage Analysis

### Question: Are these gaps covered by Phase 4 refactoring tasks?

**Phase 4 Focus:**
- S2: Isolation (boundaries, contracts)
- S3: Alignment (standardize interfaces)
- S4: Propagation (migrate to contracts)
- S5: Regression testing

**Gap Types vs Phase 4:**
- **Isolation/Structure gaps** → Likely covered by S2/S3
- **Behavior gaps** → May need separate fix tasks
- **History/Backup gaps** → Separate feature work
- **Data readiness gaps** → Separate work

---

## 🎯 Gap Coverage Assessment

### Gaps Potentially Covered by Phase 4

#### PB-GAP-004: Instance isolation under reuse/apply flows
**Coverage:** ✅ Likely covered by S2 Isolation
- S2 tasks create boundaries and isolation contracts
- Apply flows get wrapper seams
- **Action:** Verify S2 QUO/BOM isolation addresses this

#### BOM-GAP-006: Lookup Pipeline Preservation Not Verified
**Coverage:** ✅ Likely covered by S3 Alignment
- S3 aligns catalog resolution to single path
- Contract-based lookups ensure preservation
- **Action:** Verify S3 alignment covers this

---

### Gaps Needing Separate Tasks (Not Covered by Refactoring)

#### BOM-GAP-001: Feeder Template Apply Creates New Feeder Every Time
**Type:** Behavioral fix  
**Coverage:** ❌ NOT covered by refactoring  
**Action:** Needs separate Phase 4 fix task

#### BOM-GAP-002: Feeder Template Apply Missing Clear-Before-Copy
**Type:** Behavioral fix  
**Coverage:** ❌ NOT covered by refactoring  
**Action:** Needs separate Phase 4 fix task

#### BOM-GAP-004/005/007: History/Backup Missing
**Type:** Feature addition  
**Coverage:** ❌ NOT covered by refactoring  
**Action:** Separate feature tasks (may be post-Phase 4)

#### BOM-GAP-013: Template Data Missing
**Type:** Data readiness  
**Coverage:** ❌ NOT covered by refactoring  
**Action:** Separate data preparation work

---

## 📋 Recommended Actions

### Option 1: Add Gap Fix Tasks to Phase 4 (If Critical)

**If these gaps must be fixed before Phase 4 completion:**

1. **Create new Phase 4 tasks for critical gaps:**
   - NSW-P4-S4-FEED-FIX-001: Fix BOM-GAP-001 (Feeder reuse detection)
   - NSW-P4-S4-FEED-FIX-002: Fix BOM-GAP-002 (Clear-before-copy)
   - Add to appropriate S-stage (likely S4 after propagation)

2. **Include in Master Task List:**
   - Update `MASTER_TASK_LIST.md` with gap fix tasks
   - Follow same gate discipline (G3/G4 as appropriate)

### Option 2: Defer to Post-Phase 4 (If Not Critical)

**If these gaps can wait until after refactoring:**

1. **Create separate "Gap Closure" workstream:**
   - After Phase 4 S5 completes
   - Before Phase 5 starts
   - Separate task register for gap fixes

2. **Keep Phase 4 focused on refactoring:**
   - Phase 4 = Structural fixes (isolation, alignment)
   - Gap fixes = Behavioral/Feature fixes (separate)

---

## ✅ Decision Needed

**Questions to Answer:**

1. **Are BOM-GAP-001, BOM-GAP-002 critical?**
   - Must they be fixed in Phase 4?
   - Or can they wait until after refactoring?

2. **Are history/backup gaps (BOM-GAP-004/005/007) required?**
   - Are these blockers for Phase 4 completion?
   - Or are they enhancements for later?

3. **Is BOM-GAP-013 (data readiness) blocking?**
   - Can Phase 4 proceed without this?
   - Or is this a prerequisite?

4. **Should gap fixes be:**
   - **Option A:** Part of Phase 4 tasks (add to Master Task List)
   - **Option B:** Separate workstream after Phase 4
   - **Option C:** Post-Phase 4, pre-Phase 5 work

---

## 📝 Current Master Task List Status

**Current Coverage:**
- ✅ Refactoring tasks (S0-S5): 39 tasks
- ❌ Gap fix tasks: 0 tasks
- ❓ Gap coverage: Not yet analyzed

**If gaps need Phase 4 tasks:**
- Master Task List needs expansion
- Gap fix tasks added to appropriate S-stage
- Total tasks may increase (39 + gap fixes)

---

## 🔗 References

**Gap Registers:**
- `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/`
- `docs/NSW_ESTIMATION_MASTER.md` (Gap Register Summary)

**Phase 4 Tasks:**
- `docs/PHASE_4/MASTER_TASK_LIST.md`
- `docs/PHASE_3/04_TASK_REGISTER/` (Batch files)

---

**Last Updated:** 2025-12-18  
**Status:** ⏳ PENDING DECISION - Need gap fix strategy confirmed

