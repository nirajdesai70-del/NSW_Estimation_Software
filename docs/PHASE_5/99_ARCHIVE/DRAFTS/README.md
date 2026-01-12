# Phase 5 Senate - NSW Estimation Software

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
This is the Phase 5 Senate workspace - the canonical source of truth for Phase 5 analysis and design work.

## Quick Navigation

- **Start Here:** [`00_GOVERNANCE/PHASE_5_MASTER_ALIGNMENT.md`](00_GOVERNANCE/PHASE_5_MASTER_ALIGNMENT.md) - Complete alignment guide
- **Folder Mapping:** [`00_GOVERNANCE/PHASE_4_5_FOLDER_MAPPING_GUIDE.md`](00_GOVERNANCE/PHASE_4_5_FOLDER_MAPPING_GUIDE.md) ⭐ - Complete WHERE/WHEN/WHY for all 4 folders
- **Document Index:** [`00_GOVERNANCE/PHASE_5_DOC_INDEX.md`](00_GOVERNANCE/PHASE_5_DOC_INDEX.md) - All files mapped
- **Requirement Trace:** [`05_TRACEABILITY/PHASE_5_REQUIREMENT_TRACE.md`](05_TRACEABILITY/PHASE_5_REQUIREMENT_TRACE.md) - Requirements tracking

---

## Senate Structure

```
docs/PHASE_5/
├── 00_GOVERNANCE/          # Phase 5 governance, scope, decisions
├── 01_REFERENCE/           # Legacy review & TfNSW context (read-only reference)
├── 02_FREEZE_GATE/         # Freeze verification & evidence
├── 03_DATA_DICTIONARY/     # Step 1 outputs (FROZEN when complete)
├── 04_SCHEMA_CANON/        # Step 2 outputs (FROZEN when complete)
├── 05_TRACEABILITY/        # Requirement traceability matrices
├── 06_IMPLEMENTATION_REFERENCE/  # Post-Phase 5 planning (reference only)
└── 99_ARCHIVE/             # Superseded documents
```

---

## Phase 5 Scope

**Phase 5 is analysis-only:**
- **Step 1:** Freeze NSW Canonical Data Dictionary
- **Step 2:** Define NSW Canonical Schema (Design Only)

**Phase 5 does NOT include:**
- Implementation (backend, frontend, deployment)
- Legacy data migration
- Runtime testing

---

## Master Plan Alignment

Phase 5 aligns with **Master Plan P1 + P2**:
- **P1:** Canonical Data Dictionary (2-3 weeks) = **Phase 5 Step 1**
- **P2:** Canonical Schema Design (2-3 weeks) = **Phase 5 Step 2**

**Note:** Master Plan P5 (System Integration & QA) is post-implementation, different from our Phase 5.

---

## Key Documents

### Governance
- [`PHASE_5_CHARTER.md`](00_GOVERNANCE/PHASE_5_CHARTER.md) - Phase 5 charter
- [`PHASE_5_SCOPE_FENCE.md`](00_GOVERNANCE/PHASE_5_SCOPE_FENCE.md) - Scope definition
- [`PHASE_5_MASTER_ALIGNMENT.md`](00_GOVERNANCE/PHASE_5_MASTER_ALIGNMENT.md) - Complete alignment guide

### Freeze Gate
- [`SPEC_5_FREEZE_GATE_CHECKLIST.md`](02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md) - Freeze verification
- [`PHASE_5_PENDING_UPGRADES_INTEGRATION.md`](02_FREEZE_GATE/PHASE_5_PENDING_UPGRADES_INTEGRATION.md) - Integration guide

### Traceability
- [`PHASE_5_REQUIREMENT_TRACE.md`](05_TRACEABILITY/PHASE_5_REQUIREMENT_TRACE.md) - Requirements tracking
- [`FILE_TO_REQUIREMENT_MAP.csv`](05_TRACEABILITY/FILE_TO_REQUIREMENT_MAP.csv) - File mapping

---

## Three-Truth Model

1. **Truth-A (Canonical):** `docs/PHASE_5/` - Write only here
2. **Truth-B (Legacy Reference):** `project/nish/` - READ-ONLY
3. **Truth-C (Implementation):** Post-Phase 5 only

---

## Critical Rules

1. **Freeze Discipline:** No schema change after Phase 2 without governance approval
2. **Legacy Policy:** `project/nish/` is read-only reference, no code reuse
3. **Scope Fence:** No analytics/BI in Phase 5, focus on change estimation
4. **Traceability:** Every requirement must be mapped to deliverables

---

## Execution Status

| Step | Status | Deliverable |
|------|--------|-------------|
| Step 1: Data Dictionary | ⏳ PENDING | `03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` |
| Step 2: Schema Design | ⏳ PENDING | `04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` |
| Freeze Gate | ⏳ PENDING | Freeze Evidence + Approval |

---

## Next Actions

1. ✅ Senate structure created
2. ✅ Governance documents created
3. ✅ Traceability framework created
4. ⏳ Complete Step 1: Data Dictionary
5. ⏳ Complete Step 2: Schema Design
6. ⏳ Complete Freeze Gate verification

---

## Change Log
- v1.0: Created Phase 5 Senate README
