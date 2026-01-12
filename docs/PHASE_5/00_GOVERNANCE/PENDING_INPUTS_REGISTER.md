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
**Status:** ✅ APPLIED  
**Decision Link:** D-005 (IsLocked Scope)  
**Notes:** Rules reviewed and applied via D-005. Locking rules integrated into schema design. Canonical rules inform Phase-5 governance approach.

---

### PI-002: Fundamentals Pack Baseline Review
**Date Added:** 2025-01-27  
**Pending Item:** Ensure all Phase 5 design decisions reference Fundamentals v2.0 baseline from `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`  
**Source File:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`  
**What It Influences:** dictionary, schema, rules  
**Status:** ✅ APPLIED  
**Decision Link:** D-006 (CostHead Product Default), D-007 (Multi-SKU Linkage Strategy)  
**Notes:** Fundamentals v2.0 established as authoritative baseline (see `FUNDAMENTALS_SOURCE_OF_TRUTH.md`). All Phase-5 decisions cite Fundamentals baseline. D-006 and D-007 demonstrate Fundamentals alignment. Schema canon contains Fundamentals citations throughout.

---

### PI-003: Gap Registers Integration
**Date Added:** 2025-01-27  
**Pending Item:** Review gap registers for insights: BOM_GAP_REGISTER, MASTER_BOM_GAP_REGISTER_R1, PROPOSAL_BOM_GAP_REGISTER_R1  
**Source File:** `NSW Fundamental Alignment Plan/03_GAP_REGISTERS/`  
**What It Influences:** schema, rules, validation  
**Status:** ✅ APPLIED  
**Decision Link:** D-005 (IsLocked Scope)  
**Notes:** Gap register learnings applied via D-005. Gap insights inform schema design decisions. Registers serve as reference for "what not to do" patterns.

---

### PI-004: Naming Conventions Review
**Date Added:** 2025-01-27  
**Pending Item:** Review naming conventions from master documents and ensure Phase 5 naming aligns or explicitly diverges  
**Source File:** `docs/PHASE_5/03_DATA_DICTIONARY/NAMING_CONVENTIONS.md`  
**What It Influences:** dictionary, schema, naming  
**Status:** ✅ APPLIED  
**Decision Link:** (FROZEN in Step-1 — see NAMING_CONVENTIONS.md)  
**Notes:** Naming conventions established and FROZEN in Step-1. Document is canonical reference for Phase-5 naming standards. All schema design follows these conventions.

---

### PI-005: Code Review Patterns
**Date Added:** 2025-01-27  
**Pending Item:** Review code review patterns and standards from master documents for reference  
**Source File:** `project/nish/` (read-only reference)  
**What It Influences:** (reference only, not Phase 5 scope)  
**Status:** ✅ NOTED  
**Decision Link:** D-002 (Legacy Reference Policy)  
**Notes:** Code reference established as read-only via D-002. `project/nish/` serves as "what not to do" reference only. No code reuse or schema copying. Reference-only status documented.

---

### PI-006: Governance Standards Review
**Date Added:** 2025-01-27  
**Pending Item:** Review governance standards from master documents as quality lens for Phase 5 governance  
**Source File:** `NSW Fundamental Alignment Plan/02_GOVERNANCE/`  
**What It Influences:** governance, quality  
**Status:** ✅ APPLIED  
**Decision Link:** D-008 (Exploration Mode Policy)  
**Notes:** Governance standards operationalized via D-008 and `PHASE_5_MODE_POLICY.md`. Standards inform weekly cadence, decision capture requirements, and mode transition rules. Standards applied as quality lens, not strict blockers.

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
| NOTED | 1 | PI-005 (reference-only) |
| IN_REVIEW | 1 | PI-007 |
| APPLIED | 5 | PI-001, PI-002, PI-003, PI-004, PI-006 |
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
- **v1.1 (2025-01-27):** Updated all Phase-5 prerequisites (PI-001 through PI-006) with decision links and APPLIED status where completed. All prerequisites from master documents now tracked and integrated.

---

**END OF PENDING INPUTS REGISTER**

