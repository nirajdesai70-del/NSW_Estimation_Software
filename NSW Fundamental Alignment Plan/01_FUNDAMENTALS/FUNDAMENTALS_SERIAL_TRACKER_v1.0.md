# FUNDAMENTALS SERIAL TRACKER — v1.0 (Planning → Execution)

**Project:** NSW Estimation Software  
**Owner:** Niraj  
**Status:** 📋 ACTIVE TRACKER  
**Baseline:** FUNDAMENTALS_BASELINE_BUNDLE_v1.0  
**Rule:** A → B → C → D → E only (no skipping)

---

## A) Freeze Fundamentals Baseline (Gate G-A)

- [x] **A1** — Freeze baseline bundle  
  Evidence: `FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` marked frozen ✅

- [x] **A2** — Freeze verification pack  
  Evidence:  
  - `FUNDAMENTALS_VERIFICATION_QUERIES.md` ✅
  - `FUNDAMENTALS_VERIFICATION_CHECKLIST.md` ✅

- [x] **A3** — Freeze patch + SOP pack  
  Evidence:  
  - `PATCH_PLAN.md` ✅  
  - `EXECUTION_WINDOW_SOP.md` ✅

- [x] **A4** — Create patch register  
  Evidence: `PATCH_REGISTER.md` (P1–P4 listed) ✅

✅ **Gate G-A Exit:** A1–A4 complete ✅ **COMPLETE**

---

## B) Embed Patch Governance into Fundamentals Docs (Gate G-B)

- [x] **B1** — Add "Conditional Patch Governance" section into baseline bundle  
  Evidence: Updated `FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` ✅

- [x] **B2** — Add patch references into each fundamentals doc  
  Evidence:  
  - Feeder Master doc references P1/P3 ✅
  - Proposal BOM Master doc references P2/P3 ✅
  - Hierarchy doc references SOP ✅
  - Mapping doc references Patch Register ✅

✅ **Gate G-B Exit:** B1–B2 complete ✅ **COMPLETE**

---

## C) Integrate into Existing BOM Planning System (Gate G-C)

- [x] **C1** — Update Master Planning Index  
  Evidence: `PLANNING/MASTER_PLANNING_INDEX.md` includes "0) Fundamentals Gap Correction" ✅

- [x] **C2** — Update BOM Gap Register  
  Evidence: `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` includes GAP-001/002/005/006 + patch links ✅

- [x] **C3** — Update Execution Readiness Checklist  
  Evidence: `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md` includes fundamentals section + links ✅

- [x] **C4** — Integrate requirements into contracts/principles/flows (requirements only)  
  Evidence (as applicable):  
  - `PLANNING/RELEASE_PACKS/PHASE2/02_BOM_ENGINE_CONTRACT.md` includes: TemplateType='FEEDER', QuotationId validation, copy-never-link guard ✅  
  - `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md` reinforced ✅  
  - `PLANNING/FEEDER_BOM/FEEDER_BOM_CANONICAL_FLOW.md` includes filter + guard steps ✅

✅ **Gate G-C Exit:** C1–C4 complete ✅ **COMPLETE**

---

## D) Create Fundamentals Release Pack (Gate G-D)

- [x] **D1** — Create folder structure  
  Evidence: `PLANNING/RELEASE_PACKS/FUNDAMENTALS/` exists ✅

- [x] **D2** — Create runbook + status + rollback docs  
  Evidence:  
  - `00_README_RUNBOOK.md` ✅
  - `STATUS.md` ✅
  - `04_RISKS_AND_ROLLBACK.md` ✅

- [x] **D3** — Add verification pack into release pack  
  Evidence: `02_VERIFICATION/` contains queries + checklist (linked) ✅

- [x] **D4** — Add patch pack into release pack  
  Evidence: `03_PATCHES/` contains patch plan + patch register (linked) ✅

✅ **Gate G-D Exit:** D1–D4 complete ✅ **COMPLETE**

---

## E) Execution Window Run (Gate G-E) — ONLY AFTER APPROVAL

### Pre-conditions (must be true)
- [ ] Execution window approved
- [ ] DB backup confirmed
- [ ] Evidence folder created

### Execution steps
- [ ] **E1** — Preflight (branch/commit/clean state + backup proof)  
- [ ] **E2** — Run VQ-001…VQ-005 (read-only) + capture evidence  
- [ ] **E3** — Patch decision gate (only if failures)  
- [ ] **E4** — Apply approved patches (if any) + evidence + rollback plan ready  
- [ ] **E5** — Re-verify all checks + final sign-off summary

✅ **Gate G-E Exit:** Fundamentals verified and signed (PASS / PASS WITH PATCHES)

---

## Notes / Decisions Log
- Decision A: Feeder Master = `master_boms` where TemplateType='FEEDER'
- Decision B: Proposal BOM Master = Quotation root (`QuotationId`)
- No schema changes permitted in fundamentals window

---

END

