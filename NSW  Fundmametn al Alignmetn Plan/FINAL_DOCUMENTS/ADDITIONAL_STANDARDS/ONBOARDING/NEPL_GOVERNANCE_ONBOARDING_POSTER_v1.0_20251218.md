# NEPL_GOVERNANCE_ONBOARDING_POSTER_v1.0_20251218
**Source of truth:** `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md`  
**Version:** v1.1_20251219  
**Date (IST):** 2025-12-18  
**Status:** 🔒 GOVERNANCE-GRADE / ONBOARDING AID  
**Last Updated:** 2025-12-19 (Phase-3: L0-L1-L2 reference)  

---

## What this is
This poster is a **1-page operational summary** of the governed NEPL workflow. It does **not** replace the checklist; it helps new engineers follow it without drifting.

## Roles (division of responsibility)
- **ChatGPT**: meaning, governance, decisions, exceptions
- **Cursor**: deterministic execution, evidence capture, artifact generation, commits
- **GitHub**: immutable trace

## Non‑negotiables (read first)
- **Meaning first**: lock semantics before touching schema/UI/logic.
- **Evidence, not opinion**: every PASS/FAIL/exception must cite evidence.
- **No implementation unless data‑corrupting risk is confirmed** (otherwise: plan only).
- **No hacks**: exceptions are first‑class governed artifacts (named, scoped, expiry).
- **Freeze after Round‑2 approval** (never after Round‑1).

---

## Mandatory evidence format
Use one of:
- `Evidence: <file>:<section>`
- `Evidence: <file>:Lx–Ly` (if line references are available)

---

## The 5‑step governed flow (run exactly in order)

### STEP 0 — Confirm “Frozen Meaning” Exists (Standards First)
**Goal:** lock semantics before touching schema/UI/logic.  
**STOP if missing:** if governing standard(s) are not present → output **BLOCKED** and stop.

### STEP 1 — Governed Round‑1 Review (same sections every time)
For each section: **PASS / PASS WITH EXCEPTION / FAIL** (with evidence).
1. Category compliance
2. SubCategory compliance (exception-aware)
3. Item / ProductType compliance
4. Attribute & L1 spec compliance
5. L0/L1/L2 integrity (see NEPL_CUMULATIVE_VERIFICATION_STANDARD §3.1)
6. Generic vs Specific separation (L0/L1 = Generic, L2 = Specific)
7. Pricing / SKU non-leakage
8. Copy-vs-link rules (where applicable)
9. Archival / deletion rules

**STOP rule:** if any FAIL has **data-corrupting risk** → mark **CRITICAL** → go to STEP 3 (Immediate Fix recommendation).

### STEP 2 — Enforce OR Explicitly Exception (never leave ambiguity)
Per rule, do one:
- **Enforce** if enforceable without disruption/corruption (record evidence), or
- **Transitional exception** (e.g., `EX-SUBCAT-001`): name, scope, expiry, ACTIVE/governed.

**Forbidden:** temporary hacks without an exception record.

### STEP 3 — Fix Only What Is Data‑Corrupting
**Classification:**
- **CRITICAL (data-corrupting)** → recommend **Immediate** fix before freeze.
- **Non-corrupting gaps** → **Planned**, no coding now.

### STEP 4 — Round‑2 Approval + FREEZE
Before FREEZE, confirm:
- all **CRITICAL** actions are closed (or explicitly blocked with owner/timeline)
- exceptions are explicitly acknowledged and recorded

**After FREEZE:** later modules must not reinterpret frozen meaning; drift is corrected in the later module (not by rewriting foundations).

---

## The 4 required outputs (every module, same structure)
Create module-specific names with this structure:
- `<MODULE>_ROUND0_READINESS_<version>.md`
- `<MODULE>_CUMULATIVE_REVIEW_R1_<version>.md`
- `<MODULE>_GAP_REGISTER_R1_<version>.md`
- `<MODULE>_CORRECTION_PLAN_<version>.md`

Each file must include:
- Title + Version + Date (IST) + Status
- Evidence format standard
- Change Log table at end

---

## Commit rule (when artifacts are generated)
- `git add` the module’s four files
- Commit message:
  - `<MODULE> review Round-0/R1 + gap register + correction plan (<version>)`

---

## Cursor final output requirements (per run)
Cursor must output:
1) Status table: Round-0 (PASS/BLOCKED), Round-1 (PASS / PASS WITH EXCEPTION / FAIL)  
2) Gap counts by severity  
3) List of CRITICAL gaps (if any)  
4) Commit hash (if committed)  

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | 1-page onboarding poster derived from the approved Cursor-only NEPL governance checklist |
| v1.1_20251219 | 2025-12-19 | Phase-3: Added reference to canonical L0-L1-L2 definitions |


