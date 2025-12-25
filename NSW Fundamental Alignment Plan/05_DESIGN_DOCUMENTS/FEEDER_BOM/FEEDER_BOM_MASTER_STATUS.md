# Feeder BOM Master Status

**Project:** NSW Estimation Software  
**Area:** Feeder Template Apply / Re-Apply (PB-GAP-004 + BOM-GAP-001/002/007/013)  
**Mode:** 📋 PLANNING ONLY (No runtime execution now)  
**Date:** 2025-12-21  
**Canonical Governance:** PLANNING/MASTER_PLANNING_INDEX.md  
**Status:** ✅ Planning Complete (F0-F2 Locked), Execution Deferred

---

## Canonical Flow

The canonical execution path for Feeder BOM operations is locked: **UI/API Request → Controller (Thin Layer) → BomEngine::copyFeederTree() → bom_copy_history insert → Verification (Gate-0 → R1 → S1 → R2 → S2) → Phase-4 lookup integrity check → Phase-5 freeze + closure**. The Controller MUST be thin (validate input, call BomEngine, return response) and MUST NOT perform direct DB writes, business logic, or copy operations. All business logic resides in BomEngine, which handles feeder reuse detection, clear-before-copy semantics, item copying with copy-never-link pattern, and copy history recording using NEPL PascalCase column names.

---

## Current Lock State

| Phase | Status | Lock Type | Notes |
|-------|--------|-----------|-------|
| **F0** | ✅ **COMPLETE** | Planning Locked | Normalization complete. All 6 tasks done. Old docs stamped, conflicts removed, canonical flow locked. |
| **F1** | ✅ **COMPLETE** | Planning Locked | Gate-0 data readiness locked. Mandatory rule enforced: Gate-0 must pass before R1. Template shortlist blank until execution window. BOM-GAP-013 prevention mechanism in place. |
| **F2** | ✅ **COMPLETE** | Planning Locked | Thin Controller Contract locked. MUST/MUST NOT clauses explicit in both controller patch doc and Phase-2 runbook. Contract prevents architectural drift. |
| **F3** | ⏳ **BLOCKED** | Execution Deferred | Engine verification (Gate-3: R1/S1/R2/S2) blocked until execution window. Requires EXECUTION_APPROVAL signed, Window-A start, and Phase-2 Gate-1/Gate-2 complete. |
| **F4** | ⏳ **BLOCKED** | Execution Deferred | Lookup integrity verification (Phase-4 Gate-3) blocked until execution window. Requires F3 complete and Window-B start (or combined window). |
| **F5** | ⏳ **BLOCKED** | Execution Deferred | Closure pack blocked until post-execution. Requires F3 complete (Gate-3 PASS evidence) and all evidence files committed. |
| **F6** | ⏳ **BLOCKED** | Execution Deferred | Freeze & audit (Phase-5) blocked until all phases complete. Requires F5 complete, all phases PASS, and Phase-5 Gate-2 complete. |

**Execution Deferred Until:**
- Fundamentals folder planning complete
- EXECUTION_APPROVAL signed
- Explicit Window-A start declared

---

## Evidence Readiness Snapshot

| Window | Phase | Gate | Evidence File | Status | Notes |
|--------|-------|------|---------------|--------|-------|
| Window-A | Phase-2 | Gate-0 | `evidence/PHASE2/G0_template_itemcount.txt` | ⬜ PENDING | TEMPLATE_ID and N must be recorded. Mandatory before R1. |
| Window-A | Phase-2 | Gate-1 | `evidence/PHASE2/G1_bom_copy_history_schema.txt` | ⬜ PENDING | Schema verification (bom_copy_history table structure). PascalCase column names verified. |
| Window-A | Phase-2 | Gate-2 | `evidence/PHASE2/G2_controller_wiring.txt` | ⬜ PENDING | Controller wiring proof (route + controller + method call). Thin controller contract verified. |
| Window-A | Phase-2 | Gate-3 | `evidence/PHASE2/S1_sql_output.txt` | ⬜ PENDING | S1 verification: copy history + no duplicates + status distribution. |
| Window-A | Phase-2 | Gate-3 | `evidence/PHASE2/S2_sql_output.txt` | ⬜ PENDING | S2 verification: 2 history rows + clear-before-copy evidence. |
| Window-A | Phase-2 | Gate-3 | `evidence/PHASE2/R1.json` (or in header) | ⬜ PENDING | R1 response JSON. inserted_count must match N from Gate-0. |
| Window-A | Phase-2 | Gate-3 | `evidence/PHASE2/R2.json` (or in header) | ⬜ PENDING | R2 response JSON. feeder_reused=true, deleted_count>0 verification. |
| Window-B | Phase-4 | Gate-3 | `evidence/PHASE4/lookup_integrity_output.txt` | ⬜ PENDING | Lookup integrity verification SQL output. L1-L5 checks. |

**Status Legend:**
- ⬜ PENDING: Evidence not yet collected (execution blocked)
- ✅ PASS: Evidence collected and gate passed
- ❌ FAIL: Evidence collected and gate failed (stop-rule applied)
- ⏸️ BLOCKED: Evidence collection blocked (dependency not met)

---

## Next Actionable Planning-Only Step

**Current Focus:** Maintain documentation consistency and ensure all planning artifacts reference correct sources.

**Immediate Actions (Planning-Only):**
1. Review all Feeder BOM planning documents for consistency with locked F0-F2 state
2. Ensure all runbooks reference correct Gate-0 source (`master_bom_items`, not `quotation_sale_bom_items`)
3. Verify thin controller contract is consistently stated across all relevant docs
4. Confirm all evidence file stubs exist and are properly referenced
5. Maintain planning-only language throughout (no runtime execution language)

**No Runtime Actions:**
- ❌ No database queries
- ❌ No code changes
- ❌ No UI testing
- ❌ No migration execution
- ❌ No evidence file population (execution window only)

---

## Stop Rule

**If any Gate fails → STOP → capture evidence → no patching in same window unless explicitly approved.**

This rule applies to all execution windows (Window-A, Window-B, or combined windows). Evidence must be captured immediately upon gate failure, and no further patching or execution may proceed in the same window without explicit approval documented in the execution approval process.

---

## Related Documents

### Planning Artifacts
- `PLANNING/FEEDER_BOM/FEEDER_BOM_ROADMAP_TODO_TRACKER.md` — Roadmap tracker
- `PLANNING/FEEDER_BOM/FEEDER_BOM_PLAN_NORMALIZATION.md` — Normalization (F0)
- `PLANNING/FEEDER_BOM/FEEDER_BOM_EXECUTION_READINESS_SUMMARY.md` — Execution readiness (F1/F2 locks)
- `PLANNING/FEEDER_BOM/FEEDER_BOM_KANBAN.md` — Kanban board
- `PLANNING/FEEDER_BOM/FEEDER_BOM_TODO_LIST.md` — TODO checklist

### Gate-0 Documentation (F1)
- `PLANNING/RELEASE_PACKS/PHASE2/07_DATA_READINESS/DATA_READINESS_GATE.md`
- `PLANNING/RELEASE_PACKS/PHASE2/07_DATA_READINESS/TEMPLATE_SHORTLIST.md`

### Controller Documentation (F2)
- `PLANNING/IMPLEMENTATION/PHASE2_1_CONTROLLER_PATCH.md`
- `PLANNING/RELEASE_PACKS/PHASE2/00_README_RUNBOOK.md`

### Execution Support
- `PLANNING/EXECUTION/EVIDENCE_INDEX.md` — Evidence index
- `PLANNING/EXECUTION/TESTING_TODO_BACKLOG.md` — Testing backlog
- `PLANNING/EXECUTION/EXECUTION_READINESS_CHECKLIST.md` — Execution readiness checklist
- `PLANNING/MASTER_PLANNING_INDEX.md` — Master planning index

---

**END OF FEEDER BOM MASTER STATUS**

