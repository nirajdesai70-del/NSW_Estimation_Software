# Pending Inputs Register

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose

Track pending inputs from master documents, prerequisites, and other sources without turning them into blockers. This register ensures nothing is forgotten while maintaining exploration flexibility.

## Entry Format

Each entry follows this structure:

| Field | Description | Required |
|-------|-------------|----------|
| **PI-ID** | Pending Input ID (PI-###) | Yes |
| **Date Added** | Date added to register (YYYY-MM-DD) | Yes |
| **Pending Item** | Description of the pending item | Yes |
| **Source File** | Path to source document | Yes |
| **What It Influences** | dictionary/schema/api/ui/rules | Yes |
| **Status** | NOTED / IN_REVIEW / APPLIED / REJECTED | Yes |
| **Decision Link** | Decision Register ID if decisioned | No |
| **Notes** | Additional context | No |

---

## Status Definitions

- **NOTED:** Item identified, not yet reviewed
- **IN_REVIEW:** Under active consideration
- **APPLIED:** Integrated into Phase 5 design (decision made)
- **REJECTED:** Evaluated and explicitly rejected (rationale documented)

---

## Pending Inputs

### PI-001: NEPL Canonical Rules Integration
**Date Added:** 2025-01-27  
**Pending Item:** Review and integrate NEPL canonical rules from `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md`  
**Source File:** `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md`  
**What It Influences:** rules, validation, governance  
**Status:** NOTED  
**Decision Link:** (pending)  
**Notes:** This is a reference input, not a blocker. Rules should be reviewed and either applied or explicitly diverged from with rationale.

---

### PI-002: Fundamentals Pack Baseline Review
**Date Added:** 2025-01-27  
**Pending Item:** Ensure all Phase 5 design decisions reference Fundamentals v2.0 baseline from `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`  
**Source File:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`  
**What It Influences:** dictionary, schema, rules  
**Status:** IN_REVIEW  
**Decision Link:** (ongoing - multiple decisions reference this)  
**Notes:** This is the authoritative baseline. All decisions must cite this file, even when diverging.

---

### PI-003: Gap Registers Integration
**Date Added:** 2025-01-27  
**Pending Item:** Review gap registers for insights: BOM_GAP_REGISTER, MASTER_BOM_GAP_REGISTER_R1, PROPOSAL_BOM_GAP_REGISTER_R1  
**Source File:** `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/`  
**What It Influences:** schema, rules, validation  
**Status:** NOTED  
**Decision Link:** (pending)  
**Notes:** Gap registers contain learning from earlier phases. Review for insights, not as blockers.

---

### PI-004: Naming Conventions Review
**Date Added:** 2025-01-27  
**Pending Item:** Review naming conventions from master documents and ensure Phase 5 naming aligns or explicitly diverges  
**Source File:** Multiple (to be identified)  
**What It Influences:** dictionary, schema, naming  
**Status:** IN_REVIEW  
**Decision Link:** (see NAMING_CONVENTIONS.md)  
**Notes:** Phase 5 has its own naming conventions document. Verify alignment or document divergence.

---

### PI-005: Code Review Patterns
**Date Added:** 2025-01-27  
**Pending Item:** Review code review patterns and standards from master documents for reference  
**Source File:** (to be identified)  
**What It Influences:** (reference only, not Phase 5 scope)  
**Status:** NOTED  
**Decision Link:** (N/A - reference only)  
**Notes:** This is for reference only, not a Phase 5 deliverable.

---

### PI-006: Governance Standards Review
**Date Added:** 2025-01-27  
**Pending Item:** Review governance standards from master documents as quality lens for Phase 5 governance  
**Source File:** `NSW Fundamental Alignment Plan/02_GOVERNANCE/`  
**What It Influences:** governance, quality  
**Status:** IN_REVIEW  
**Decision Link:** (ongoing - governance files reference these)  
**Notes:** Use as quality lens, not as strict requirements.

---

### PI-007: Fundamentals Gap Analysis Integration
**Date Added:** 2025-01-27  
**Pending Item:** Review and address items from `FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`  
**Source File:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`  
**What It Influences:** dictionary, schema, alignment  
**Status:** IN_REVIEW  
**Decision Link:** (multiple decisions may reference this)  
**Notes:** This identifies gaps between Fundamentals v2.0 and Phase 5. Review and address through decisions.

---

## Summary by Status

| Status | Count | Items |
|--------|-------|-------|
| NOTED | 3 | PI-001, PI-003, PI-005 |
| IN_REVIEW | 4 | PI-002, PI-004, PI-006, PI-007 |
| APPLIED | 0 | — |
| REJECTED | 0 | — |

---

## Integration Policy

### How to Handle Pending Inputs

1. **NOTED → IN_REVIEW:**
   - When starting to evaluate the item
   - Update status and add notes

2. **IN_REVIEW → APPLIED:**
   - When decision is made to integrate
   - Create Decision Register entry
   - Link Decision ID
   - Update status

3. **IN_REVIEW → REJECTED:**
   - When decision is made to reject
   - Create Decision Register entry with rejection rationale
   - Link Decision ID
   - Update status

4. **Keep Register Updated:**
   - Weekly review of pending items
   - Update status as items progress
   - Add new items as they are discovered

---

## Change Log

- **v1.0 (2025-01-27):** Initial pending inputs register created with items from master documents mapping

---

**END OF PENDING INPUTS REGISTER**

