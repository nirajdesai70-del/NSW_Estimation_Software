# NEPL Cumulative Verification Standard  
**Version:** 1.1_20251219  
**Status:** 🔒 MASTER — GOVERNANCE STANDARD  
**Date:** 2025-12-18  
**Frozen:** 2025-12-18  
**Last Updated:** 2025-12-19 (Phase-3: L0-L1-L2 canonical definitions)

**Purpose:**  
To enforce a **progressive, cumulative verification process** across the entire NEPL software, ensuring that all modules remain aligned with the frozen Item Master and quotation design — without architectural drift.

---

## 1. WHY THIS STANDARD EXISTS

NEPL is a **large, evolving system**.  
A one-time design review is insufficient.

This standard ensures:
- Foundational concepts are **never reinterpreted**
- Each new module is validated **in context of all previous decisions**
- Design correctness and code correctness evolve together

This enables **dual verification**:
1. **Design verification** (human, architectural)
2. **Code verification** (Cursor / static analysis / service review)

---

## 2. CORE PRINCIPLE — CUMULATIVE VERIFICATION (LOCKED)

> **No module is reviewed in isolation.  
Every module review re-validates all previously frozen foundations.**

This rule applies **without exception**.

---

## 3. FROZEN FOUNDATIONS (REFERENCE BASE)

The following are **frozen and non-negotiable**:

### 3.1 L0–L1–L2 Layer Definitions (Canonical)

> **📌 Canonical Reference:** For the authoritative single source of truth on L0/L1/L2 rules, see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` (Section 1.1).

- **L0 = Generic Item Master (Functional Family)**
  - Example: MCC / MCCB / ACB
  - No technical specification, no make, no series, no SKU
  - Unique; never duplicated; never used directly in any BOM
  - ProductType = 1 (Generic Product)

- **L1 = Specific Item Master (Technical Variant, Make-agnostic)**
  - Example: MCCB 25A, 25kA / 35kA / 50kA
  - Derived from L0 + technical spec set
  - Unique; never duplicated; reusable
  - ProductType = 1 (Generic Product)
  - **Master BOM operates at L1**
  - **Master BOM must not contain L2**

- **L2 = Catalog Item (Make + Series + SKU/Model)**
  - Example: Schneider / ABB / Siemens model variants
  - Derived from L1 + Make + Series (+ SKU/Model)
  - Unique; never duplicated; reusable
  - ProductType = 2 (Specific Product)
  - **Proposal/Specific BOM operates at L2**
  - **Proposal/Specific BOM = Quotation-specific instance**
  - Multiple Proposal BOMs can exist for one Master BOM
  - Must resolve L1 → L2 before finalization

### 3.2 Item Master Standard
   - Category ≠ Item/ProductType
   - SubCategories are additive
   - Accessories are not Items
   - Attributes are vendor-neutral
   - L0 / L1 / L2 inheritance model (as defined in 3.1)

### 3.3 Generic Item Master
   - Generic Product (ProductType = 1) = L0/L1 carrier
   - Specific Product (ProductType = 2) = L2 carrier
   - No SKU or pricing logic at Generic level (L0/L1)
   - Master BOM uses L1 only (Generic Products)

### 3.4 Quotation Design
   - L0 → Budgetary / FEED (Generic concept, no BOM)
   - L1 → Technical offer (Master BOM template)
   - L2 → Commercial offer (Proposal BOM with resolved products)
   - Price refresh controlled and versioned

### 3.5 Phase 8 SKU Governance
   - Make.RequiresSku enforcement
   - OEM vs INTERNAL SKU separation
   - OEM price import only for SkuType=OEM
   - Internal SKU never receives OEM-imported prices

These foundations are **never reopened** during later reviews.

---

## 4. VERIFICATION CHAIN (PROCESS FLOW)

```

Item Master (Frozen)
↓
Generic Item Master (Reviewed & Frozen)
↓
Module 1 Review
↓
Module 2 Review
↓
Module 3 Review
↓
...
↓
Final System Validation

```

At **every step**:
- Earlier layers are re-validated
- No backward drift is permitted

---

## 5. MANDATORY REVIEW SCOPE (EVERY TIME)

For **every document, module, or feature**, the following must be reviewed:

### A. Item Master Alignment
- ☐ Category ≠ Item maintained
- ☐ No new Item/ProductType introduced implicitly
- ☐ SubCategory usage remains additive
- ☐ No accessories promoted to Item

### B. Generic Item Master Alignment
- ☐ Generic Product (ProductType=1) used only for L0/L1
- ☐ No SKU / Make / price logic at Generic level (L0/L1)
- ☐ Attributes remain vendor-neutral
- ☐ L1 completeness rules respected
- ☐ Master BOM uses L1 only (Generic Products)

### C. L0 / L1 / L2 Integrity
- ☐ L0 = Generic Item Master (functional family, never used in BOM)
- ☐ L1 = Technical variant (make-agnostic, used in Master BOM)
- ☐ L2 = Catalog item (make + series + SKU, used in Proposal BOM)
- ☐ Master BOM operates at L1 only (must not contain L2)
- ☐ Proposal BOM operates at L2 (resolves L1 → L2)
- ☐ Inheritance preserved (no data loss)

### D. Quotation Alignment
- ☐ Module supports quotation lifecycle
- ☐ No pricing shortcuts introduced
- ☐ No quotation logic bypasses Item Master
- ☐ Price refresh remains controlled

### E. Phase 8 SKU Governance
- ☐ Make.RequiresSku honored
- ☐ Internal SKU generated only when allowed
- ☐ OEM price import filtered to SkuType=OEM
- ☐ No INTERNAL SKU receives OEM pricing

If **any one** of the above fails → **module is NOT approved**.

---

## 6. STANDARD REVIEW FORMAT (MANDATORY)

Every module must be reviewed using the **NEPL Standard Review Format**, containing:

1. Context & Scope
2. Category Verification
3. SubCategory Verification
4. Item/ProductType Verification
5. Attribute & L1 Spec Verification
6. L0/L1/L2 Resolution Verification
7. SKU Governance Verification
8. Quotation Flow Verification
9. Anti-pattern Detection
10. Final Verdict & Sign-off

No document is considered "complete" without this review.

---

## 7. GENERIC ITEM MASTER — SPECIAL STATUS

### 7.1 Dual Role

> **Generic Item Master is both:**
> - A foundational design
> - A recurring validation reference

It must be re-checked during:
- BOM design
- Pricing logic
- Quotation UI
- Import/export services
- Reporting & analytics

---

### 7.2 Drift Detection Rule (HARD)

If a later module:
- Assumes a different meaning of Generic Item Master, or
- Forces a change in Generic Item Master

Then:
- ❌ The module is incorrect
- ❌ The Generic Item Master is NOT changed
- ✅ The module must be corrected

This prevents "local fixes breaking global logic".

---

## 8. DUAL VERIFICATION MODEL (YOU + CURSOR)

This document is designed for **dual usage**:

### 8.1 Design-Level Verification (You / Team)
- Concept review
- Structural correctness
- Long-term maintainability

### 8.2 Code-Level Verification (Cursor)
Cursor must verify:
- Database schema consistency
- Service-layer enforcement
- Controller behavior
- No logic bypasses frozen standards

Cursor should treat this document as:
> **The single source of truth**

---

## 9. ACCEPTANCE & FREEZE RULE

A module is considered **accepted** only when:

- ☐ Design review passes using this standard
- ☐ Cursor verification finds no violations
- ☐ All conflicts are resolved in the module (not in foundations)

Only then may the module be marked **CLOSED**.

---

## 10. FINAL GOVERNANCE STATEMENT (LOCKED)

> **NEPL uses a cumulative verification methodology.  
All modules are reviewed against Item Master, Generic Item Master, Quotation Design, and SKU Governance — repeatedly and progressively.  
No later module is allowed to redefine earlier concepts.  
This standard governs all current and future development.**

---

## 11. HOW TO USE THIS FILE (INSTRUCTIONS)

1. Store this file in `/docs/NEPL_STANDARDS/00_BASELINE_FREEZE/`
2. Reference it in every design and code review
3. Ask Cursor to:
   - Validate code against this document
   - Flag violations explicitly
4. Do not allow exceptions without written approval

---

## 12. REVIEW RECORD TEMPLATE (MANDATORY OUTPUT)

Every module review must produce a record using this template:

- **Module/Doc Name:**  
- **Version/Commit:**  
- **Reviewer (Design):**  
- **Reviewer (Cursor/Code):**  
- **Date:**  
- **Scope:** (what was checked)
- **Result:** PASS / PASS WITH NOTES / FAIL  
- **Findings:**  
  1)  
  2)  
- **Actions Required:**  
  1)  
  2)  
- **Closure Statement:** "Module verified against cumulative standard v1.0 and approved."

---

## 13. CURSOR PROMPT BLOCK (COPY/PASTE)

Use this exact prompt in Cursor for code verification:

> Verify the module/codebase against `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md`.  
> Output must include:  
> 1) PASS/FAIL for each checklist section (Item Master, Generic Item Master, L0/L1/L2, Quotation, Phase 8 SKU).  
> 2) Exact file paths + function names where violations occur.  
> 3) Proposed code-level fixes that preserve frozen foundations (do not redesign Item Master).  
> 4) A short Review Record using the template in Section 12.

---

## Change Log

| Version | Date (IST) | Change Type | Summary |
|---------|------------|-------------|---------|
| v1.0 | 2025-12-18 | Freeze | Initial master standard — cumulative verification methodology |
| v1.1_20251219 | 2025-12-19 | Phase-3 | Added canonical L0-L1-L2 layer definitions; clarified Generic/Specific Product mapping; updated verification checklists |

---

**END OF DOCUMENT**

