# S2 Execution Checklist (Isolation) — Phase 4
#
# Scope: Execution-safe isolation planning + boundary hardening.
# Rule: No QUO-V2 isolation work until NSW-P4-S2-QUO-REVERIFY-001 (G4) is executed and approved.
# Rule: Do NOT edit Phase-3 docs (frozen). Produce execution artifacts under docs/PHASE_4 only.
#
# Status: ACTIVE
# Last Updated: 2025-12-18

---

## S2 Entry Conditions (must be true)

- S0 is **CLOSED WITH CONDITIONS** (see `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`)
- S1 **Ownership Lock** is effective (owners + risks fenced)
- QUO‑V2 is explicitly **fenced** behind `NSW-P4-S2-QUO-REVERIFY-001` (G4)
- Gate-0 "Template Data Readiness" rule is declared (BOM-GAP-013):
  - applies to FEED/PBOM/MBOM apply verification planning
  - read-only SQL evidence only (no data fixes in S2)
  - recorded in `docs/PHASE_4/GAP_GATEBOARD.md`

---

## S2 Operating Rules (non-negotiable)

- **No behavior change** in S2. Create seams, boundaries, and contracts only.
- **No propagation** (S4) and **no alignment** (S3) in S2.
- **No direct edits** to PROTECTED scope (QUO‑V2 core, costing/qty services) in S2.

---

## Gate-0: Template Data Readiness (BOM-GAP-013) — S2 Declaration Only (Read-Only)

**Purpose:** Prevent later verification runs from failing due to empty templates (0 rows in `master_bom_items`).

**S2 Scope:** Declaration + evidence procedure only.
- ✅ Allowed in S2: define the rule, define the SQL, define where evidence will be stored
- ❌ Not allowed in S2: fixing templates, inserting data, changing selection logic

### Gate-0 Rule (must be satisfied before any apply verification window)
A template (MasterBomId) is "ready" only if:

- `COUNT(master_bom_items WHERE MasterBomId = TEMPLATE_ID) > 0`

### Required Evidence (store outputs; attach in GAP_GATEBOARD)
Create evidence file(s) under:
- `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/`

SQL to run (read-only):
1. `SELECT COUNT(*) AS item_count FROM master_bom_items WHERE MasterBomId = <TEMPLATE_ID>;`
2. `SELECT <TEMPLATE_ID> AS template_id, COUNT(*) AS item_count FROM master_bom_items WHERE MasterBomId = <TEMPLATE_ID>;` *(same, but explicit for logs)*

### Pass/Fail Decision
- **PASS:** item_count > 0 → template can be used for R1/R2 verification later
- **FAIL:** item_count = 0 → do not proceed with apply verification; record FAIL and choose a different template (no DB edits in S2)

**Authority:** `docs/PHASE_4/GAP_GATEBOARD.md` (Lane-A gap BOM-GAP-013)

---

## Execution Order (safe)

0. **S2.0 GOV** — create/refresh `GAP_GATEBOARD.md` + declare Gate-0 Template Data Readiness (read-only)
1. **S2.1 SHARED** — contracts first, then split planning
2. **S2.2 CIM** — import split isolation + catalog single-path plan
3. (Later, after SHARED+CIM) MBOM → FEED → PBOM → QUO(legacy)  
4. **QUO‑V2 deferred** until re-verify task is executed (G4)

---

## Active S2 Work Packages (this run)

### S2.0 — GOV (first)

- **NSW-P4-S2-GOV-GAP-001 (G2)**: Create/refresh Phase-4 Gap Gateboard (Lane-A vs Lane-B), assign closure owners, define evidence pointers
- **NSW-P4-S2-GOV-DATA-013 (G2)**: Declare Gate-0 Template Data Readiness rule + evidence location (read-only)

**Deliverable:** `docs/PHASE_4/GAP_GATEBOARD.md`

### S2.1 — SHARED

- **NSW-P4-S2-SHARED-001 (G3)**: Shared utilities contract (Catalog lookup + Reuse search)
- **NSW-P4-S2-SHARED-002 (G3)**: Shared controller split plan (no moves)

**Deliverable:** `docs/PHASE_4/S2_SHARED_ISOLATION.md`

### S2.2 — CIM (next)

- **NSW-P4-S2-CIM-001 (G3)**: Import split isolation (CIM vs MASTER/PDF) + adapter seam spec
- **NSW-P4-S2-CIM-002 (G3)**: Catalog resolution single-path plan (no execution)

**Deliverable:** `docs/PHASE_4/S2_CIM_ISOLATION.md`

---

## References (authority)

- Batch-2 task list (planning source): `docs/PHASE_3/04_TASK_REGISTER/BATCH_2_S2.md`
- Gate rules: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Rulebook: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`
- Trace maps: `trace/phase_2/ROUTE_MAP.md`, `trace/phase_2/FEATURE_CODE_MAP.md`, `trace/phase_2/FILE_OWNERSHIP.md`
- Execution posture + S0/S1 fence: `docs/PHASE_4/PHASE_4_EXECUTION_CONTEXT.md`


