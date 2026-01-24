# Phase 6 New Project Folder Plan - Review & Recommendations
## Enhanced Plan Review with Constitutional Layer Additions

**Date:** 2025-01-27  
**Status:** 📋 REVIEW COMPLETE - AWAITING APPROVAL  
**Reviewer:** AI Assistant  
**Purpose:** Review suggested enhancements and provide recommendations

---

## 🎯 Executive Summary

**Overall Assessment:** ✅ **APPROVE WITH MINOR REFINEMENTS**

The suggested enhancements elevate the plan from "enterprise-grade" to "world-class" by adding:
- Constitutional layer (00_CANON/) to prevent interpretation drift
- Architecture separation (12_ARCHITECTURE/) for future-proofing
- Decision vs Working Truth enforcement
- Enhanced evidence discipline
- Sharpened execution sequence

**Recommendation:** Proceed with all suggested additions, with minor refinements noted below.

---

## ✅ Approved Additions (No Changes Needed)

### 1. 00_CANON/ Folder - **APPROVED**

**Status:** ✅ Ready to implement as-is

**Rationale:**
- Prevents ambiguity when Cursor + RAG are active
- Constitutional layer that stabilizes governance
- All 5 files are well-structured and future-proof

**Files to Create:**
1. `TERMINOLOGY_CANON.md` ✅
2. `NAMING_CONVENTIONS.md` ✅
3. `VERSIONING_RULES.md` ✅
4. `FILE_AUTHORITY_HIERARCHY.md` ✅
5. `FREEZE_POLICY.md` ✅

**Action:** Create these files exactly as provided in the suggestion.

---

### 2. 12_ARCHITECTURE/ Folder - **APPROVED**

**Status:** ✅ Ready to implement

**Rationale:**
- Separates architecture from planning (common mistake prevention)
- Needed very soon for system design
- Keeps structure clean and organized

**Proposed Structure:**
```
12_ARCHITECTURE/
├── SYSTEM_OVERVIEW.md
├── DATA_MODEL.md
├── ESTIMATION_ENGINE.md
├── API_BOUNDARIES.md
└── FUTURE_EXTENSION_POINTS.md
```

**Action:** Create empty folder structure now, populate as architecture work begins.

---

### 3. Decision vs Working Truth Rule - **APPROVED**

**Status:** ✅ Ready to add to governance

**Proposed Rule Addition:**
- Only documents in `01_MASTER_DOCUMENTS`, `03_MATRICES`, and `09_SPECIFICATIONS` are Working Truth
- All rationale, debates, tradeoffs live in Decision RAG + Decision Register
- Cursor execution may read decisions, but may write only working truth

**Action:** Add this rule to `PHASE_6_GOVERNANCE_RULES.md` under a new section "Rule 7: Decision vs Working Truth".

---

### 4. Evidence Discipline Enhancement - **APPROVED**

**Status:** ✅ Ready to implement

**Proposed Structure:**
```
10_EVIDENCE/
├── WEEK0_RUN_YYYYMMDD_HHMMSS/
│   ├── _INDEX.md
│   ├── SUMMARY.md
│   ├── VERIFICATION.md
│   └── RAW/
```

**Rule:** Evidence folders are immutable once closed.

**Action:** 
- Update `10_EVIDENCE/` structure in plan
- Add immutability rule to governance
- Create `_INDEX.md` template for evidence packs

---

### 5. Sharpened Execution Sequence - **APPROVED**

**Status:** ✅ Ready to adopt

**Proposed Phases:**
- Phase A: Skeleton Lock (Manual)
- Phase B: Canonical Transfer (Manual)
- Phase C: Cursor-assisted consolidation
- Phase D: Decision RAG sync
- Phase E: GitHub baseline

**Action:** Replace current "Recommended Approach" section with this sequence.

---

## 🔧 Recommended Refinements

### Refinement 1: 04_TASKS_AND_TRACKS/ README

**Issue:** Tracks need clarification in the plan document itself.

**Recommendation:** Add a README section to the plan explaining tracks:

```markdown
### Track Definitions

- **TRACK_A:** Legacy Business Decision Verification (RETAIN/REPLACE/DROP tagging)
- **TRACK_A_R:** Track A Review/Retrospective
- **TRACK_B:** NSW Fundamentals Alignment (always mandatory, blocking)
- **TRACK_C:** Phase-6 Preparation (UI wireframes, API contracts, tooling)
- **TRACK_D0:** D0 Gate Checklist (validation gate)
- **TRACK_D:** Additional execution track (TBD)
- **TRACK_E:** Additional execution track (TBD)
- **TRACK_F:** Conditional track (if approved)

**Authority:** Track B > Track A when conflicts arise
```

**Action:** Add this to the plan document under `04_TASKS_AND_TRACKS/` section.

---

### Refinement 2: README Enhancement

**Issue:** README template needs "Where to Add" and "What NOT to Add" sections.

**Recommendation:** Add these sections to README template:

```markdown
## 📍 Where to Add New Documents

- **New governance rules:** `00_GOVERNANCE/00_RULES/`
- **New scope documents:** `00_GOVERNANCE/01_SCOPE/`
- **New planning documents:** `00_GOVERNANCE/02_PLANNING/`
- **New decisions:** `00_GOVERNANCE/03_DECISIONS/`
- **New week plans:** `02_WEEK_PLANS/WEEK_X/`
- **New matrices:** `03_MATRICES/`
- **New specifications:** `09_SPECIFICATIONS/<CATEGORY>/`
- **New architecture docs:** `12_ARCHITECTURE/`
- **Evidence:** `10_EVIDENCE/WEEKX_RUN_YYYYMMDD_HHMMSS/`

## ⛔ What NOT to Add Here

- **Code files** (until actively working on that component)
- **Temporary/scratch files** (use project root for temporary work)
- **Duplicate documents** (reference existing, don't copy)
- **Personal notes** (use personal workspace)
- **Outdated versions** (archive or delete, don't accumulate)
- **Files not following naming convention** (see `00_CANON/NAMING_CONVENTIONS.md`)
```

**Action:** Add to README template in plan document.

---

### Refinement 3: Canon File Authority Hierarchy Update

**Issue:** The `FILE_AUTHORITY_HIERARCHY.md` includes `12_ARCHITECTURE/` but it's not in the original plan.

**Recommendation:** Update the original plan's folder structure to include `12_ARCHITECTURE/` explicitly, and ensure authority hierarchy matches.

**Action:** Update folder structure diagram in plan to include `12_ARCHITECTURE/` between `11_REFERENCE/` and `README.md`.

---

### Refinement 4: Freeze Declaration Document

**Issue:** Suggestion mentions creating a Freeze Declaration but doesn't specify exact location.

**Recommendation:** Create:
```
00_GOVERNANCE/00_RULES/V1_0_CANON_FREEZE_DECLARATION.md
```

**Content should include:**
- Declaration date
- What is frozen (structure, canon, rules)
- Effective version (V1.0)
- Change control process
- Reference to Decision Register

**Action:** Draft this document after CANON files are created.

---

### Refinement 5: Phase-6 Naming Context Note

**Issue:** Suggestion mentions adding a note about Phase-6 naming vs V1.0/V2.0 coexistence.

**Recommendation:** Add to README:

```markdown
## 📌 Phase-6 Naming Context

Phase-6 documents represent the design & consolidation phase of NSW Estimation Software V1.0. 

**Important:**
- Filenames use `PHASE_6_*` prefix (correct for migration context)
- This folder is the birthplace of NSW Estimation Software V1.0
- Future phases (V1.1, V2.0) will coexist without renaming Phase-6 artefacts
- Phase-6 documents remain authoritative for V1.0 baseline
```

**Action:** Add to README template.

---

## ⚠️ Potential Conflicts & Resolutions

### Conflict 1: Authority Hierarchy vs Master Document Rule

**Issue:** 
- Plan says: "Master Document Authority" (Rule 4) - `01_MASTER_DOCUMENTS/PHASE_6_FINAL_MASTER_CONSOLIDATED_PLAN.md` is primary
- Canon says: Authority hierarchy places `01_MASTER_DOCUMENTS/` at top, but `09_SPECIFICATIONS/` and `03_MATRICES/` are also Working Truth

**Resolution:** ✅ No conflict - these are complementary:
- Master Document = single source of truth for overall plan
- Authority Hierarchy = conflict resolution when documents disagree
- Working Truth = what Cursor/RAG can write to (broader than just master)

**Action:** Clarify in governance that Rule 4 and Authority Hierarchy work together.

---

### Conflict 2: Evidence Location

**Issue:** 
- Plan shows evidence in `02_WEEK_PLANS/WEEK_X/` AND `10_EVIDENCE/`
- Suggestion shows evidence only in `10_EVIDENCE/`

**Resolution:** ✅ Clarify:
- Week plans reference evidence (links/pointers)
- Actual evidence files live in `10_EVIDENCE/`
- Evidence packs are immutable once closed

**Action:** Update plan to clarify evidence location policy.

---

## 📋 Updated Folder Structure (Final)

```
NSW Estimation Software V1.0/
├── 00_CANON/                          ⭐ NEW
│   ├── TERMINOLOGY_CANON.md
│   ├── NAMING_CONVENTIONS.md
│   ├── VERSIONING_RULES.md
│   ├── FILE_AUTHORITY_HIERARCHY.md
│   └── FREEZE_POLICY.md
│
├── 00_GOVERNANCE/
│   ├── 00_RULES/
│   │   ├── PHASE_6_GOVERNANCE_RULES.md
│   │   ├── PHASE_6_DECISION_REGISTER.md
│   │   ├── PHASE_6_EMPTY_DOCUMENTS_REGISTER.md
│   │   └── V1_0_CANON_FREEZE_DECLARATION.md  ⭐ NEW
│   ├── 01_SCOPE/
│   ├── 02_PLANNING/
│   └── 03_DECISIONS/
│
├── 01_MASTER_DOCUMENTS/
├── 02_WEEK_PLANS/
├── 03_MATRICES/
├── 04_TASKS_AND_TRACKS/
│   └── README.md                       ⭐ NEW (explains tracks)
│
├── 05_GAPS_AND_ALARMS/
├── 06_REVIEWS_AND_VERIFICATION/
├── 07_LEGACY_PARITY/
├── 08_EXECUTION/
├── 09_SPECIFICATIONS/
├── 10_EVIDENCE/
│   └── WEEK0_RUN_YYYYMMDD_HHMMSS/
│       ├── _INDEX.md                   ⭐ NEW
│       ├── SUMMARY.md
│       ├── VERIFICATION.md
│       └── RAW/
│
├── 11_REFERENCE/
├── 12_ARCHITECTURE/                    ⭐ NEW
│   ├── SYSTEM_OVERVIEW.md
│   ├── DATA_MODEL.md
│   ├── ESTIMATION_ENGINE.md
│   ├── API_BOUNDARIES.md
│   └── FUTURE_EXTENSION_POINTS.md
│
└── README.md (Enhanced with new sections)
```

---

## ✅ Implementation Checklist

### Phase A: Skeleton Lock (Manual)

- [ ] Create complete folder structure (including 00_CANON/ and 12_ARCHITECTURE/)
- [ ] Create 5 CANON files exactly as provided
- [ ] Create 12_ARCHITECTURE/ folder structure (empty files OK)
- [ ] Create 04_TASKS_AND_TRACKS/README.md with track definitions
- [ ] Create enhanced README.md with new sections
- [ ] Lock structure in Decision Register

### Phase B: Canonical Transfer (Manual)

- [ ] Transfer Priority 0 & 1 documents
- [ ] Verify all references
- [ ] Update cross-references to new structure
- [ ] Create V1_0_CANON_FREEZE_DECLARATION.md
- [ ] Add "Decision vs Working Truth" rule to governance
- [ ] Freeze structure

### Phase C: Cursor-assisted Consolidation

- [ ] Use Cursor to cross-link documents
- [ ] Generate indexes
- [ ] Validate completeness
- [ ] Push Working Truth into Working RAG

### Phase D: Decision RAG Sync

- [ ] Summarize structure rationale
- [ ] Document exclusions and priorities
- [ ] Push to Decision RAG

### Phase E: GitHub Baseline

- [ ] Create repo (if not exists)
- [ ] Commit docs only
- [ ] Tag: `nsw-estimation-v1-docs-freeze`

---

## 🎯 Final Recommendation

**APPROVE** all suggested enhancements with the refinements noted above.

**Next Steps:**
1. ✅ Review this document
2. ✅ Approve refinements (or suggest modifications)
3. ✅ Proceed with Phase A (Skeleton Lock)
4. ✅ Create CANON files
5. ✅ Continue with enhanced execution sequence

---

## 📝 Questions for Approval

1. **00_CANON/ files:** Approve exact content as provided? ✅
2. **12_ARCHITECTURE/:** Create empty structure now? ✅
3. **Track definitions:** Approve README content for 04_TASKS_AND_TRACKS/? ✅
4. **Evidence structure:** Approve _INDEX.md template approach? ✅
5. **Freeze Declaration:** Create immediately after CANON? ✅
6. **Execution sequence:** Replace current approach with sharpened sequence? ✅

---

**Status:** 📋 REVIEW COMPLETE - AWAITING APPROVAL  
**Date:** 2025-01-27  
**Next Action:** User approval → Proceed with Phase A implementation
