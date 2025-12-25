# Proposal BOM — Correction Plan (Round-1)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CORRECTION_PLAN_v1.0_2025-12-19.md  
**Version:** v1.0_2025-12-19  
**Date (IST):** 2025-12-19  
**Status:** ⏳ **EVIDENCE-BASED (DB-PENDING)**

## ✅ Standard Remark: Evidence-Based Review (DB Pending)

**Remark (Scope & Evidence Tier):**  
This Proposal BOM review is executed using the authoritative Master BOM design pack (Index/Plan + Parts 1–11) which contains Proposal BOM design specifications. The design pack is **imported/registered into this repo workspace for evidence-path referencing** under `docs/MASTER_BOM/DESIGN/`, therefore Design Evidence is marked **VERIFIED**. Live database verification is not available as of **2025-12-19**, therefore all data-integrity outcomes that require runtime/DB proof are marked **DB-PENDING** and must be validated before any "final freeze" is treated as production-confirmed.

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

Unblock Proposal BOM governance review by executing Round‑1 cumulative review and producing evidence-driven PASS/FAIL outcomes with remediation plans for identified gaps.

- Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§5`
- Evidence: `PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md:§0`

| Axis | Status | Meaning |
|---|---|---|
| Design Evidence | VERIFIED | Design pack registered under `docs/MASTER_BOM/DESIGN/` (contains Proposal BOM specifications) |
| Code Evidence | NOT VERIFIED | Code evidence not available in this workspace |
| DB Evidence | DB-PENDING | No DB access available today; runtime data integrity proof pending |

---

## 2) Constraints (Governed)

- **No code changes** unless a **data-corrupting risk** is confirmed; otherwise plan only.
  - Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§0` — "This Round-0 does not: Touch DB, Implement code"
- Round‑1 must not be marked **repo‑verified** while DB Evidence is DB-PENDING (runtime verification required).
  - Evidence: `PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md:§0`
- **Upstream inputs treated as correct** (not debated here):
  - Item Master = trusted foundation
  - Generic Item Master = frozen
  - Master BOM = closed / audit-ready
  - Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§0`

---

## 3) Dependencies

| Dependency | Status | Evidence |
|---|---|---|
| Master BOM design artifacts (Index/Plan + Parts 1–11) | ✅ VERIFIED | Evidence: `docs/MASTER_BOM/DESIGN/MASTER_BOM_BACKEND_DESIGN_INDEX.md:§📚 Document Structure` |
| Master BOM = closed / audit-ready | ✅ Present | Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§0` |
| Generic Item Master FROZEN | ✅ Present | Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§0` |
| Round-0 Readiness = ✅ READY FOR ROUND-1 | ✅ Present | Evidence: `PROPOSAL_BOM_ROUND0_READINESS_v1.0_2025-12-19.md:§5` |

---

## 4) Planned Work Batches

### Batch A — DB Verification Pack + Remedies (CRITICAL)
- **Scope**: Convert DB-PENDING items into VERIFIED evidence (or gaps) and apply remedies where required
- **Inputs**: 
  - Evidence: `PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md:§🔍 DB Verification Pack (Run Later) + Remedies`
  - Evidence: `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§✅ DB-PENDING verification items`
- **Actions**:
  - **A1) Schema & Keys Verification**
    - Run `SHOW CREATE TABLE quotation_sale_boms;` and `SHOW CREATE TABLE quotation_sale_bom_items;`
    - Confirm keys/columns match design: `QuotationSaleBomId`, `QuotationSaleBomItemId`, `ProductId`, `Level`, `ParentBomId`, `Qty`, `Rate`, `RateSource`, `IsPriceMissing`, `Status`, timestamps
    - Verify FK integrity (or explicit documented reason if FK not present)
    - **Remedy**: If missing columns/keys, add migration (planned unless corrupting)
    - **Remedy**: If FK missing and causing orphans, add FK OR add scheduled integrity job (priority based on impact)
  
  - **A2) Specific Product Enforcement Verification (CRITICAL)**
    - Execute SQL to verify all active Proposal BOM items (Status=0) have ProductType=2 (Specific) in final persisted state
    - Verify no Proposal BOM items with ProductType=1 (Generic) exist in "final" state
    - Verify MakeId and SeriesId are required when ProductType=2
    - **Remedy**: If any violations found → **CRITICAL** data integrity — quarantine/fix data + enforce hard guards in service validation (Immediate)
    - **Remedy**: Add application-level guard to prevent saving Proposal BOM items with Generic ProductId unless explicitly marked as "pending resolution"
    - **Remedy**: Add validation rule: Proposal BOM items with Status=0 must have ProductType=2 (Specific)
  
  - **A3) Copy-Never-Link Independence Verification (CRITICAL)**
    - Execute runtime test: Create Master BOM → copy to quotation → edit Master BOM → confirm Proposal BOM unchanged
    - Verify Proposal BOM rows are copies (Master BOM edits do not mutate copied BOM rows)
    - **Remedy**: If linkage exists → **CRITICAL** logic defect — patch copy implementation immediately (Immediate)
  
  - **A4) Hierarchy Integrity Verification (CRITICAL)**
    - Execute SQL to verify:
      - Level 0 (Feeder) has no ParentBomId
      - Level 1 (BOM1) has ParentBomId pointing to Level 0
      - Level 2 (BOM2) has ParentBomId pointing to Level 1
      - No nesting beyond Level 2
    - **Remedy**: If violations exist → **CRITICAL** data integrity — quarantine/fix data + enforce validation guards (Immediate)
    - **Remedy**: Add validation to prevent invalid hierarchy structures
  
  - **A5) Quantity Chain & Roll-up Logic Verification**
    - Verify quantity chain correctly walks up to Level 0 (feeder) for roll-up calculations
    - Verify no double-multiplication in roll-ups (SUM only at roll-up, not nested multiplication)
    - **Remedy**: If logic errors exist → HIGH priority — fix calculation logic (Planned)
  
  - **A6) Soft Delete (Archival) Verification**
    - Verify deletes set `Status=1` (no hard deletes)
    - Verify delete doesn't cascade incorrectly
    - **Remedy**: If hard deletes exist, convert to soft-delete or enforce archival policy in service layer

- **Acceptance criteria**:
  - DB evidence updated from **DB-PENDING → VERIFIED** (or gaps raised with severity + owner/timeline)
  - All CRITICAL data integrity violations are quarantined/fixed with hard guards
  - Validation rules added to prevent future violations

---

### Batch B — Code Verification & Enforcement (PB-GAP-001 [Proposal-Resolution], PB-GAP-002 [Proposal-Resolution])
- **Scope**: Verify and enforce "Specific products only" rule across all write paths
- **Inputs**:
  - Evidence: `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§3 PB-GAP-001` — Transitional Generic → Specific state verification
  - Evidence: `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§3 PB-GAP-002` — Enforcement location for "Specific products only" rule
- **Actions**:
  - **B1) Transitional State Verification (PB-GAP-001)**
    - Audit all Proposal BOM item creation/update operations to verify transitional generic state is acceptable under L2 discipline
    - Verify transitional state is allowed only as controlled intermediate state, never persisted as "final"
    - Verify all downstream logic (pricing, validation, export, costing) does not incorrectly treat generic as valid "final"
    - Add application-level guard to prevent saving Proposal BOM items with Generic ProductId unless explicitly marked as "pending resolution"
    - Add validation rule: Proposal BOM items with Status=0 must have ProductType=2 (Specific)
    - **Remedy**: If violations found, quarantine/fix data and add hard guards
  
  - **B2) Enforcement Coverage Verification (PB-GAP-002)**
    - Audit all write paths for Proposal BOM items:
      - Copy-from-master operation
      - Add-item operation (manual item addition)
      - Update Make/Series operation
      - Apply/reuse flows (if any)
      - Promote flows (if any)
    - Verify consistent validation rule: Proposal BOM items must use Specific products (ProductType=2) with MakeId and SeriesId required
    - Consider centralizing validation logic in a shared service/validator to ensure consistency
    - Add integration tests to verify validation on all write paths
    - **Remedy**: If enforcement missing on any path, add validation guards

- **Acceptance criteria**:
  - All write paths enforce "Specific products only" rule consistently
  - Validation logic centralized to prevent drift
  - Integration tests verify validation on all paths
  - Transitional generic state is controlled and never persisted as "final"

---

### Batch C — Quantity Chain & Hierarchy Logic (PB-GAP-003 [Cross-Layer])
- **Scope**: Verify and fix quantity chain correctness and hierarchy edge cases
- **Inputs**:
  - Evidence: `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§3 PB-GAP-003` — Quantity chain correctness + "feeder discovery" edge cases
- **Actions**:
  - **C1) Hierarchy Rules Documentation**
    - Document explicit hierarchy rules:
      - Level 0 (Feeder) must have no ParentBomId
      - Level 1 (BOM1) must have ParentBomId pointing to Level 0
      - Level 2 (BOM2) must have ParentBomId pointing to Level 1
      - No nesting beyond Level 2
    - Add validation to prevent invalid hierarchy structures (e.g., Level 1 without Level 0 parent)
  
  - **C2) Quantity Chain Logic Verification**
    - Verify quantity chain logic handles all valid hierarchy configurations
    - Verify correct handling when Level 1 is attached directly under panel (if allowed) vs strict "Level 1 under Level 0" model
    - Audit roll-up calculation logic to ensure SUM only (no nested multiplication)
    - Add unit tests for quantity chain edge cases:
      - Level 1 attached directly under panel (if allowed)
      - Level 1 under Level 0 (standard case)
      - Level 2 under Level 1
      - Multiple Level 1 BOMs under same Level 0
    - **Remedy**: If logic errors found, fix calculation logic (HIGH priority)

- **Acceptance criteria**:
  - Hierarchy rules explicitly documented and validated
  - Quantity chain logic verified for all edge cases
  - Roll-up calculations use SUM only (no double-multiplication)
  - Unit tests cover all edge cases

---

### Batch D — Instance Isolation Verification (PB-GAP-004 [Cross-Layer])
- **Scope**: Verify instance isolation under reuse/apply flows
- **Inputs**:
  - Evidence: `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§3 PB-GAP-004` — Instance isolation under reuse/apply flows
- **Actions**:
  - **D1) Reuse/Apply Flow Audit**
    - Audit all "apply / reuse / promote" flows to confirm they create new independent Proposal BOM instances (copy semantics)
    - Verify foreign keys (e.g., MasterBomId, ParentBomId) are used for reference/tracking only, not for behavioral linking
    - Check for any database triggers, cascading updates, or application-level logic that might create hidden links between Proposal BOM instances
  
  - **D2) Integration Tests**
    - Add integration tests to verify:
      - Applying a Proposal BOM creates a new independent instance
      - Changes to source Proposal BOM do not affect applied/target Proposal BOM
      - Reuse operations create independent copies
      - Promote operations maintain instance isolation
  
  - **D3) Documentation**
    - Document explicit rule: All Proposal BOM operations must maintain instance isolation (copy-never-link)
    - **Remedy**: If hidden linking found, remove linking and ensure copy semantics

- **Acceptance criteria**:
  - All reuse/apply flows create independent instances (copy semantics)
  - No hidden linking between Proposal BOM instances
  - Integration tests verify instance isolation
  - Explicit rule documented

---

## 5) Timeline (Week-level)

- **Week 0**: Batch A (DB Verification Pack) — **CRITICAL** (must execute first to identify data integrity issues)
- **Week 1**: Batch B (Code Verification & Enforcement) + Batch C (Quantity Chain & Hierarchy Logic)
- **Week 2**: Batch D (Instance Isolation Verification) + Final gap closure

**Note**: Batch A (DB Verification) is **CRITICAL** and must be executed first to identify any data-corrupting risks that require immediate remediation.

---

## 6) Ownership Suggestion

- **DB Verification**: Database team / Backend team
- **Code Verification & Enforcement**: Backend team
- **Quantity Chain & Hierarchy Logic**: Backend team / Logic team
- **Instance Isolation Verification**: Backend team / Integration team
- **Documentation**: Technical writer / Backend team

---

## 7) Severity Escalation Rules

- **HIGH → CRITICAL**: If DB verification reveals:
  - Proposal BOM items with Generic products (ProductType=1) in final persisted state
  - Invalid hierarchy structures (e.g., Level 1 without Level 0 parent, nesting beyond Level 2)
  - Hidden linking between Proposal BOM instances causing unexpected data mutations

- **Immediate Action Required**: Any CRITICAL gap must be quarantined/fixed with hard guards before proceeding with other batches.

---

## Change Log

| Version | Date (IST) | Change |
|---|---|---|
| v1.0_2025-12-19 | 2025-12-19 | Created correction plan with remediation steps for PB-GAP-001 through PB-GAP-004 based on Round-0 Focus Zones FZ-01 to FZ-04 |
| v1.1_2025-12-19 | 2025-12-19 | Phase-3: Added layer labels to gap references (Proposal-Resolution and Cross-Layer context) |

