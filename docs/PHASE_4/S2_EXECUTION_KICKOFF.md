# S2 Execution Kickoff Pack - Phase 4

**Version:** 1.0 - LOCKED  
**Date:** 2025-12-18  
**Status:** 🔒 LOCKED - Authoritative Execution Plan  
**Purpose:** Definitive execution order, DoD, and evidence expectations for S2 Isolation

---

## ✅ Corrections Applied

- **Tracker Fixed:** S0 now correctly shows 11/11 tasks (was 2/2)

---

## 🎯 Phase-4 Execution Order (Authoritative - LOCKED)

We will execute S2 in this exact sequence:

1. **S2.1 GOV** (contracts + exception→task stubs)
2. **S2.2 SHARED** (define shared contracts + split mixed controllers)
3. **S2.3 CIM** (ImportController seam + single catalog resolution path plan)
4. **S2.5 BOM modules** (MBOM → FEED → PBOM contracts)
5. **S2.4 MASTER/EMP** (cross-cutting touchpoints)
6. **S2.6 QUO** (legacy first; QUO-V2 only after REVERIFY)

**Reason:** SHARED contracts become dependency anchor; QUO-V2 stays blocked until reverify.

---

## 📋 S2 "Definition of Done" (DoD) - LOCKED

To avoid "documentation says isolated but code still tangled", each S2 task must end with:

### A) Contract File Frozen (doc)
**Required Deliverable:** `docs/PHASE_4/S2_<MODULE>_ISOLATION.md` updated with:
- Owned entrypoints
- Forbidden callers
- Adapter seam (where future wrappers will attach)
- Consumer list (who must migrate in S4)

### B) Evidence Pointers
**Required Links:**
- Controller/service file list (from FILE_OWNERSHIP)
- Route names touched
- "Touchpoint list" from S0
- Cross-module call sites (even if not edited yet)

### C) Gate Stamp (G2/G3/G4)
**Required:** Add one line "Gate satisfied by: [evidence description]" inside the S2 doc (keeps audit trail clean).

---

## 🚀 First 3 Tasks - Today's Kickoff

### Task 1 — NSW-P4-S2-GOV-001 (G3 / HIGH)

**Objective:** Convert ownership exceptions into split/adapter task stubs  
**Output:** Exception→Task mapping table (single canonical table)

**What to produce (minimum):**
- For each exception file:
  - Owning module
  - "Methods owned by X"
  - Adapter seam name (e.g., SharedCatalogLookupAdapter)
  - Future propagation tasks (S4 consumer list)

**Why first:** It prevents re-discovering the same split logic later in SHARED/CIM/BOM.

**Evidence Location:** Exception→Task mapping table in S2 execution doc

---

### Task 2 — NSW-P4-S2-GOV-002 (G3 / HIGH)

**Objective:** Create boundary blocks per module  
**Output:** `docs/PHASE_4/S2_BOUNDARY_BLOCKS.md` (or add into each S2_* file)

**Boundary block template (use verbatim pattern):**
- Module owns: …
- Module may call: …
- Module must not call: …
- Allowed cross-module entrypoints: (contracts only)
- Forbidden direct DB writes / forbidden service calls: …

**Evidence Location:** Boundary blocks document

---

### Task 3 — NSW-P4-S2-SHARED-001 (G3 / HIGH)

**Objective:** Declare shared utility contracts  
**Output:** `docs/PHASE_4/S2_SHARED_ISOLATION.md` updated with 2 contract stubs:
- CatalogLookupContract
- ReuseSearchContract

**Each contract must define:**
- Inputs/outputs (payload fields)
- Error contract
- Caching/lookup rules (if any)
- Logging requirements
- Versioning rule (future-proof)

**Evidence Location:** S2_SHARED_ISOLATION.md

---

## ⚠️ QUO-V2 Blocker Handling

In S2.6, run QUO-REVERIFY-001 early, but keep QUO-V2 refactors blocked until it passes.

### Task — NSW-P4-S2-QUO-REVERIFY-001 (G4 / PROTECTED)

**Goal:** Verify routes ↔ controller methods in the actual Laravel execution root (not snapshot confusion).

**Pass/Fail criteria (simple):**
- For each route listed as mismatch:
  - Route exists ✅/❌
  - Controller exists ✅/❌
  - Method exists ✅/❌
  - If not: identify actual handler (or confirm dead route)

**Output:** A 1-page evidence note in `docs/PHASE_4/S2_QUO_LEGACY_ISOLATION.md` + the exact file paths confirmed.

---

## ✅ S2 Completion Criteria (LOCKED)

S2 is "done" only when these are true:

- [ ] Each module has its `S2_*_ISOLATION.md` updated and internally consistent
- [ ] SHARED contracts are declared and referenced by CIM/BOM/QUO plans
- [ ] Forbidden callers list exists for every module
- [ ] QUO-REVERIFY-001 is completed (even if QUO-V2 stays blocked afterwards)
- [ ] "Consumer migration list" exists for S4 (per contract)

---

## 📝 Execution Notes

- **No behavior change** in S2. Create seams, boundaries, and contracts only.
- **No propagation** (S4) and **no alignment** (S3) in S2.
- **No direct edits** to PROTECTED scope (QUO-V2 core, costing/qty services) in S2.
- All deliverables go under `docs/PHASE_4/` only (Phase 3 docs remain frozen).

---

## 🔗 Authority References

- **Batch-2 tasks:** `docs/PHASE_3/04_TASK_REGISTER/BATCH_2_S2.md`
- **FILE_OWNERSHIP:** `trace/phase_2/FILE_OWNERSHIP.md`
- **S2 Checklist:** `docs/PHASE_4/S2_EXECUTION_CHECKLIST.md`
- **Rulebook:** `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`

---

**Document Status:** 🔒 LOCKED - Authoritative  
**Execution Start:** Immediate  
**Last Updated:** 2025-12-18

