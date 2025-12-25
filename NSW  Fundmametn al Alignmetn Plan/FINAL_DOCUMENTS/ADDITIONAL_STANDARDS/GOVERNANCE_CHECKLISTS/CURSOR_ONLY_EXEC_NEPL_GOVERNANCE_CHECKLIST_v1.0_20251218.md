# Cursor-Only Execution Checklist — NEPL Governance Workflow (Reusable)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md  
**Version:** v1.1_20251219  
**Date (IST):** 2025-12-18  
**Status:** 🔒 GOVERNED CHECKLIST  
**Last Updated:** 2025-12-19 (Phase-3: L0-L1-L2 reference)  

---

## Purpose (Operational Only)

Execute the **NEPL governance workflow** as a repeatable Cursor runbook for:
- Category
- SubCategory
- Attributes
- Item / ProductType
- Master BOM
- Any future module (Pricing, SKU, Variant, etc.)

**Rule:** No implementation unless a **data-corrupting risk** is confirmed. Otherwise: plan only.

---

## Evidence Format (Mandatory)

Use one of:
- `Evidence: <file>:<section>`
- `Evidence: <file>:Lx–Ly` (if line references are available)

Evidence must be **quotes or references**, not opinion.

---

## Outputs (Template Set for Any Module)

Create (module-specific names, same structure):
- `<MODULE>_ROUND0_READINESS_<version>.md`
- `<MODULE>_CUMULATIVE_REVIEW_R1_<version>.md`
- `<MODULE>_GAP_REGISTER_R1_<version>.md`
- `<MODULE>_CORRECTION_PLAN_<version>.md`

Each output must include:
- Title + Version + Date (IST) + Status
- Evidence format standard
- Change Log table at end

---

## STEP 0 — Confirm “Frozen Meaning” Exists (Standards First)

**Goal:** Lock semantics before touching schema/UI/logic.

Cursor must confirm:
- The **cumulative standard** exists and is the active reference base.
- Any relevant permanent standards (e.g., archival/deletion standard) exist.

**STOP if missing:**
- If the governing standard(s) are not present → output **BLOCKED** and stop.

**Minimum evidence:**
- `Evidence: NEPL_CUMULATIVE_VERIFICATION_STANDARD_*.md:<Foundations section>`
- `Evidence: NEPL_PRODUCT_ARCHIVAL_STANDARD_*.md:<Definitions section>` (if applicable)

---

## STEP 1 — Execute Governed Round-1 Review (Same Sections Every Time)

**Goal:** Evaluate current system against frozen meaning.

Mandatory sections (do not change section names):
1. Category compliance
2. SubCategory compliance (exception-aware)
3. Item / ProductType compliance
4. Attribute & L1 spec compliance
5. L0/L1/L2 integrity (see NEPL_CUMULATIVE_VERIFICATION_STANDARD §3.1 for canonical definitions)
6. Generic vs Specific separation (L0/L1 = Generic ProductType=1, L2 = Specific ProductType=2)
7. Pricing / SKU non-leakage
8. Copy-vs-link rules (where applicable)
9. Archival / deletion rules

For each section: **PASS / PASS WITH EXCEPTION / FAIL**

**STOP rule:**
- If any section is **FAIL** with **data-corrupting risk** → mark **CRITICAL** and proceed to STEP 3 (Immediate Fix recommendation).
- If FAIL is **non-corrupting** → record as planned gap and proceed (no code changes).

**Evidence requirement:** Each PASS/FAIL must cite evidence.

---

## STEP 2 — Enforce OR Explicitly Exception (Never Leave Ambiguity)

**Goal:** For every rule, do one of the following — no gray zone.

Per rule:
- If enforceable without disruption/corruption → enforce (service/schema/validation), and record evidence.
- If enforcement risks disruption → record a **transitional exception**:
  - Name it (e.g., `EX-SUBCAT-001`)
  - Scope it
  - Define expiry condition
  - Mark as ACTIVE and governed

**Forbidden:** Temporary hacks without an exception record.

---

## STEP 3 — Fix Only What Is Data-Corrupting

**Goal:** Stability over perfection.

Classification:
- **CRITICAL (data-corrupting)** → recommend **Immediate** fix before freeze.
- **Non-corrupting gaps** → **Planned**, no coding now.

Gap Register must include for each gap:
- Gap ID: `<MODULE>-GAP-###` (sequential)
- Category: Schema / Service / Logic / Validation / UX / Governance / Docs
- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Evidence
- Impact (quotation / reuse / audit / pricing / data integrity)
- Fix Type: Immediate (CRITICAL only) / Planned
- Recommendation (1–3 actionable bullets)

---

## STEP 4 — Round-2 Approval + FREEZE

**Goal:** Close interpretation permanently.

Cursor must confirm:
- All **CRITICAL** actions are closed (or explicitly blocked with owner/timeline).
- Exceptions are explicitly acknowledged and recorded.

Then publish:
- Round-2 final approval record (module-specific)
- Freeze notice (module-specific)

**After freeze:**
- No later module may reinterpret frozen meaning.
- Drift must be corrected in the later module (not by rewriting foundations).

---

## Commit Rules (Mandatory When Artifacts Are Generated)

When the module’s four outputs are created/updated:
- `git add` the module’s four files
- Commit message (module substituted accordingly):
  - `<MODULE> review Round-0/R1 + gap register + correction plan (<version>)`

---

## Cursor Final Output Requirements (Per Run)

Cursor must output:
1) Status table:
   - Round-0: PASS/BLOCKED
   - Round-1: PASS / PASS WITH EXCEPTION / FAIL
2) Gap counts by severity
3) List of CRITICAL gaps (if any)
4) Commit hash (if committed)

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | Cursor-only operational checklist derived from the governed NEPL governance workflow |
| v1.1_20251219 | 2025-12-19 | Phase-3: Added reference to canonical L0-L1-L2 definitions in master standard |


