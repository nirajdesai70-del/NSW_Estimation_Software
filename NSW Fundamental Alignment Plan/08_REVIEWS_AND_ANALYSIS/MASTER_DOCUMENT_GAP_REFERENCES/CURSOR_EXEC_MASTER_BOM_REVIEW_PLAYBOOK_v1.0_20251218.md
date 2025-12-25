# Cursor Execution Playbook — Master BOM Review (Cumulative Governance)
**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md  
**Version:** v1.1_20251219  
**Date (IST):** 2025-12-18  
**Status:** 🔒 GOVERNED PLAYBOOK  
**Last Updated:** 2025-12-19 (Phase-3: L0-L1-L2 canonical definitions)

## Primary Standards
- NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md
- NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md
- EX-SUBCAT-001 (SubCategory additive transitional exception)

## Reference Index
- MASTER_BOM_BACKEND_DESIGN_INDEX.md (Parts 1–11)
- MASTER_BOM_BACKEND_DESIGN_PLAN.md

---

## 0) Objective

Execute a governed review of **Master BOM** against frozen fundamentals:
- Category / SubCategory / Item / ProductType / Attributes
- Item Master + Generic Item Master (FROZEN)
- Specific Item Master (Reviewed + plan recorded; implementation may be deferred)
- L0/L1/L2 integrity (see NEPL_CUMULATIVE_VERIFICATION_STANDARD §3.1 for canonical definitions)
- Copy-never-link rule
- Pricing/SKU governance non-leakage
- Archival / deletion standards

Non-negotiables:
- **Master BOM operates at L1 only (Generic Products, ProductType = 1)**
- **Master BOM must not contain L2 (Specific Products)**
- **Always copy, never link Master BOM to quotations**
- **Proposal BOM operates at L2 (resolves L1 → L2)**

**Implementation Rule:**  
No code changes unless a **data-corrupting risk** is confirmed. Otherwise: plan only.

---

## 1) Workspace Preconditions (STOP if missing)

Cursor must confirm these files exist in the workspace:
- MASTER_BOM_BACKEND_DESIGN_INDEX.md
- MASTER_BOM_BACKEND_DESIGN_PLAN.md
- MASTER_BOM_BACKEND_DESIGN_PART1_FOUNDATION.md
- MASTER_BOM_BACKEND_DESIGN_PART2_DATA_MODELS.md
- MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md
- MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md
- MASTER_BOM_BACKEND_DESIGN_PART5_RULES.md
- MASTER_BOM_BACKEND_DESIGN_PART6_SERVICES.md
- MASTER_BOM_BACKEND_DESIGN_PART7_MASTER_DATA.md
- MASTER_BOM_BACKEND_DESIGN_PART8_OPERATIONS.md
- MASTER_BOM_BACKEND_DESIGN_PART9_LOGIC.md
- MASTER_BOM_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md
- MASTER_BOM_BACKEND_DESIGN_PART11_CODEBASE.md

If missing:
- Output a “BLOCKED” status
- List missing files
- Stop execution (do not generate Round-1 outputs)

---

## 2) Required Outputs (Files to Create)

Create these files in:
`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/`

A) `MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md`  
B) `MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md`  
C) `MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md`  
D) `MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md`  

Each file must contain:
- Title + Version + Date (IST) + Status
- Evidence format standard: “Evidence: `<file>:<section>` (or `<file>:Lx–Ly` if available)”
- “Change Log” table at end

---

## 3) Round-0 Readiness Checklist (Create File A)

Confirm all are TRUE:
- Generic Item Master is **FROZEN**
- Specific Item Master is **Reviewed + plan recorded**
- NEPL archival standard exists
- EX-SUBCAT-001 is active
- Master BOM Parts 1–11 + Index + Plan exist

If any dependency missing:
- Round-0 = BLOCKED
- List missing items
- Stop (do not proceed to Round-1)

---

## 4) Round-1 Review Execution (Create File B)

For each section, mark: PASS / PASS WITH NOTES / FAIL

### Section 1 — Category compliance
- Category used only for grouping/filtering
- No device identity derived from Category

### Section 2 — SubCategory compliance (EX-SUBCAT-001 aware)
- System does not assume fixed SubCategory enumeration
- Primary SubCategory is consistent; feature-like subcategories expressed via attributes/tags

### Section 3 — Item/ProductType compliance
- Item/ProductType is device identity anchor
- No accessory terms promoted to Item

### Section 4 — Attributes compliance
- L0/L1 supported (descriptor + spec)
- No vendor fields required in Master BOM
- Required attribute policy documented (soft/hard) and scope clarified

### Section 5 — Item Master + Product rule (CRITICAL)
- Master BOM items reference **generic products only (ProductType=1)**
- No ProductType=2 allowed in Master BOM items

### Section 6 — Generic Item Master alignment (FROZEN)
- No SKU/Make/Series/Price logic inside generic layer
- No write-path mutates generic into L2

### Section 7 — Specific Item Master alignment (PLANNED)
- Make/Series selection happens only during quotation resolution/copy stage
- Not inside Master BOM

### Section 8 — L0/L1/L2 integrity
- Master BOM supports L0/L1 only
- L2 resolution occurs after copy into quotation/proposal layer

### Section 9 — Copy-never-link rule (CRITICAL)
- Copy algorithm exists and is enforced
- Edits to Master BOM do not affect copied instances

### Section 10 — Pricing / SKU governance non-leakage
- No price joins at Master BOM stage
- No SKU enforcement at Master BOM stage

### Section 11 — Archival / deletion governance
- No hard deletes
- Soft delete only + correct dependency checks/messages

---

## 5) Gap Register (Create File C)

For every FAIL or NOTE:
- Gap ID: `MB-GAP-###` (sequential)
- Category: Schema / Service / Logic / Validation / UX / Governance / Docs
- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Evidence: file + section + short quote/snippet reference
- Impact: quotation / reuse / audit / pricing risk / data integrity
- Fix Type:
  - “Immediate” ONLY if data-corrupting
  - Otherwise “Planned”
- Recommendation: 1–3 bullets (actionable)

---

## 6) Correction Plan + Timeline (Create File D)

Convert Gap Register into:
- Batches (Immediate / Phase-Integration / Later)
- Dependencies
- Timeline (week-level is fine)
- Ownership suggestion (Dev / QA / Docs / Ops)
- Acceptance criteria per batch

Rules:
- Data-corrupting gaps → Immediate fix recommended
- Enhancements → Planned (no coding now)

---

## 7) Codebase Cross-check (Only if code exists)

If Laravel code exists in the workspace:
- Scan `MasterBomController`, `MasterBom`, `MasterBomItem`
- Confirm ProductType=1 enforcement on create/update
- Confirm copy-never-link is enforced
- Confirm deletes are soft (Status flag)
- Confirm no pricing joins inside Master BOM stage

If code is not present:
- State: “Code verification not executed in this workspace”
- Provide a follow-up prompt for the Laravel repo path/review

---

## 8) Commit Rules (Mandatory)

After generating files A–D:
- `git add` the four files
- Commit message:
  `Master BOM review Round-0/R1 + gap register + correction plan (v1.0_20251218)`

---

## 9) Cursor Final Output Requirements

Cursor must output:
1) Status table:
   - Round-0: PASS/BLOCKED
   - Round-1: PASS / PASS WITH NOTES / FAIL
2) Gap counts by severity
3) List of CRITICAL gaps (if any)
4) Commit hash (if committed)

---

## Change Log
| Version | Date (IST) | Change |
|---|---|---|
| v1.0_20251218 | 2025-12-18 | Initial governed playbook for Master BOM review |
| v1.1_20251219 | 2025-12-19 | Phase-3: Added reference to canonical L0-L1-L2 definitions; clarified Master BOM = L1, Proposal BOM = L2 |



