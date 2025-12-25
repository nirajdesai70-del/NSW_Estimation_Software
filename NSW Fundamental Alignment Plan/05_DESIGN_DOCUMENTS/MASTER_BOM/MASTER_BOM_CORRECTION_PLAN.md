# Master BOM — Correction Plan (Round-1)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md  
**Version:** v1.0_20251218  
**Date (IST):** 2025-12-18  
**Status:** ⏳ **EVIDENCE-BASED (DESIGN-IMPORT PENDING + DB-PENDING)**

## ✅ Standard Remark: Evidence-Based Review (DB Pending)

**Remark (Scope & Evidence Tier):**  
This Master BOM review is executed using the authoritative Master BOM design pack (Index/Plan + Parts 1–11) and code references where available. The design pack is **not yet imported/registered into this repo workspace for evidence-path referencing**, therefore Design Evidence is marked **IMPORT-PENDING**. Live database verification is not available as of **2025-12-18**, therefore all data-integrity outcomes that require runtime/DB proof are marked **DB-PENDING** and must be validated before any “final freeze” is treated as production-confirmed.

**Reminder (Mandatory DB Verification Later):**  
Before final acceptance / production freeze, execute the DB Verification Pack and update DB evidence from **DB-PENDING → VERIFIED**.

### Status wording (when DB is the only missing evidence)
If DB evidence is not available, but design/code evidence is complete, use:
**Status: ⏳ EVIDENCE-BASED (DB-PENDING)**

---

## Evidence Format (Mandatory)
Use one of:
- `Evidence: <file>:<section>`
- `Evidence: <file>:Lx–Ly` (if line references are available)

---

## 1) Executive Objective

Unblock Master BOM governance review by satisfying Round‑0 readiness prerequisites, then execute Round‑1 cumulative review and produce evidence-driven PASS/FAIL outcomes.

- Evidence: `CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md:§1`
- Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§4`

| Axis | Status | Meaning |
|---|---|---|
| Design Evidence | IMPORT-PENDING | Design pack exists externally (authoritative) but is not yet registered in this repo workspace for evidence-path referencing |
| Code Evidence | PARTIAL (EXTERNAL) | Code evidence captured from external Laravel path; not yet imported/registered into this workspace |
| DB Evidence | DB-PENDING | No DB access available today; runtime data integrity proof pending |

---

## 2) Constraints (Governed)

- **No code changes** unless a **data-corrupting risk** is confirmed; otherwise plan only.
  - Evidence: `CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md:L33–L35`
- Round‑1 must not be marked **repo‑verified** while Design Evidence is IMPORT-PENDING (design pack not yet registered in repo workspace).
  - Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§1`

---

## 3) Dependencies

| Dependency | Status | Evidence |
|---|---|---|
| Master BOM design artifacts (Index/Plan + Parts 1–11) | ⏳ IMPORT-PENDING | Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:§3` |
| Specific Item Master “plan recorded” evidence registered in workspace | ✅ VERIFIED | Evidence: `docs/SPECIFIC_ITEM_MASTER/PLAN/SPECIFIC_ITEM_MASTER_DETAILED_DESIGN.md:L1–L6` |
| Generic Item Master FROZEN | ✅ Present | Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:L21–L24` |
| Archival standard present | ✅ Present | Evidence: `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md:L21–L24` |

---

## 4) Planned Work Batches

### Batch A — Unblock Round‑0 (Docs/Governance)
- **Scope**: Close MB-GAP-001 [Cross-Layer], MB-GAP-002 [Cross-Layer]
- **Inputs**:
  - Evidence: `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:§3`
- **Actions**:
  - Import/register Master BOM design artifacts (Index/Plan + Parts 1–11) into this workspace, with governed filenames (or formally revise the playbook if filenames/locations differ).
  - Import/register the Specific Item Master “plan recorded” artifact into this workspace (implementation can be deferred; dependency is governance evidence).
- **Acceptance criteria**:
  - Design Evidence axis updated from **IMPORT-PENDING → VERIFIED** (repo-resolvable evidence-path references)
  - Round‑0 checklist table updated accordingly (no false FAIL due to import status)
  - Specific Item Master plan-recorded dependency closed (MB-GAP-002 resolved).

### Batch B — Code alignment (Master BOM identity + archival)
- **Scope**: Close MB-GAP-003 [L1 Layer], MB-GAP-004 [L1 Layer]
- **Inputs**:
  - Evidence: `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md:§3` (MB-GAP-003 [L1], MB-GAP-004 [L1])
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L25–L49` (B4 rule: L0/L1 ⇒ ProductId must be NULL)
  - Evidence: `/Users/nirajdesai/Projects/nish/app/Http/Controllers/MasterBomController.php:L287–L299` (hard delete in `destroy()`)
- **Actions**:
  - Update governed Master BOM docs to explicitly state the identity anchor: Master BOM items are L1 spec templates; `ProductId` is `NULL` by design (B4). Master BOM operates at L1 layer.
  - Record the governed deletion/archival policy decision for Master BOM templates (soft delete approach and “no delete if referenced” rule).
  - Produce an implementation plan (planned change) to remove/replace hard deletes for Master BOM and Master BOM items (choose `Status` flag or Laravel `SoftDeletes`).
- **Acceptance criteria**:
  - Doc wording updated and evidence-referenced (identity anchor and enforcement stage clarified).
  - Delete policy decided and recorded (soft delete mechanism chosen + “inactive vs delete” rule).
  - Planned implementation captured (work items / owner / timeline), without making code changes in this governed docs repo.

### Batch C — Execute Round‑1 (after Round‑0 PASS)
- **Scope**: Run cumulative Master BOM review sections and record PASS / PASS WITH NOTES / FAIL with evidence.
- **Inputs**:
  - Evidence: `CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md:§4`
- **Actions**:
  - Execute and complete `MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md`.
  - Update `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` for every FAIL/NOTE with evidence and severity.
  - Convert gaps into an actionable correction plan (this file) with acceptance criteria.
- **Acceptance criteria**:
  - Round‑1 has explicit evidence for each section outcome.
  - All CRITICAL (data‑corrupting) gaps are either closed or explicitly blocked with owner/timeline (governance decision).

### Batch D — DB Verification Pack + Remedies (after DB access is available)
- **Scope**: Convert DB-PENDING items into VERIFIED evidence (or gaps) and apply remedies where required
- **Inputs**: DB Verification Pack (see Remark section in this document; also referenced in other Master BOM outputs)
- **Actions**:
  - Run schema/key checks (`SHOW CREATE TABLE ...`) and confirm constraints match design intent.
  - Run resolution enforcement verification (Master BOM items are `L0`/`L1` only; `ProductId` must remain `NULL` for `L0`/`L1`) and remediate any violations (CRITICAL).
  - Execute copy-never-link runtime test and remediate any linkage (CRITICAL).
  - Verify soft-delete behavior (`Status=1`) and no cascading deletes into quotation/proposal BOM.
  - Verify no pricing/SKU leakage at Master BOM stage.
- **Acceptance criteria**:
  - DB evidence updated from **DB-PENDING → VERIFIED** (or gaps raised with severity + owner/timeline).

---

## 5) Timeline (Week-level)

- **Week 0**: Batch A (unblock Round‑0)
- **Week 1**: Batch B (policy + plan alignment) + Batch C (execute Round‑1 and finalize gap register + correction plan)

---

## 6) Ownership Suggestion

- **Docs/Governance**: Provide Master BOM design artifacts + Specific Item Master completion evidence
- **Cursor Execution**: Re-run Round‑0 then execute Round‑1 with evidence capture

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | Created correction plan; limited to unblocking Round-0 prerequisites because Round-1 is not executed |
| v1.0_20251218 | 2025-12-18 | Amended Batch D wording to Resolution enforcement; Week-1 wording updated to policy+plan alignment |
| v1.0_20251218 | 2025-12-18 | Amended: Batch A dependencies satisfied; MB-GAP-002 closed. |
| v1.1_20251219 | 2025-12-19 | Phase-3: Added layer labels to gap references (L1 layer context) |


