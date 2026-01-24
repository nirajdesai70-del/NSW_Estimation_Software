# P6-SETUP-008 — Module Boundaries & PR Rules

**Phase:** Phase-6  
**Week:** Week-0  
**Document ID:** P6-SETUP-008  
**Version:** v1.0  
**Status:** ✅ COMPLETE  
**Date:** 2026-01-12

---

## 1. Purpose

This document defines **module boundaries** and **pull request (PR) governance rules** for Phase-6.  
Its objective is to prevent scope bleed, uncontrolled coupling, and Canon violations during execution.

**Scope (Week-0):**
- ✅ Define logical module boundaries
- ✅ Define PR and review rules
- ❌ No folder refactoring
- ❌ No code movement
- ❌ No ownership reassignment

---

## 2. Authority & Governance

All Phase-6 work must comply with the following authorities:

- **Schema Authority:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Contract Authority:**  
  `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
- **Task Authority:**  
  `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`
- **Gate Authority:**  
  `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`
- **Category D Freeze:**  
  `docs/PHASE_5/02_CATEGORY_D_FREEZE/`

No PR may violate these authorities without explicit Phase-6 governance approval.

---

## 3. Module Boundary Definitions

The following **logical module boundaries** are enforced for Phase-6.  
These are **conceptual boundaries**, independent of physical folder layout.

---

### 3.1 Core Resolution Engine

**Responsibility**
- Core resolution logic
- Canon-aligned computations
- Deterministic evaluation

**Must Not**
- Contain UI logic
- Contain presentation formatting
- Bypass Canon constraints

---

### 3.2 Catalog & Master Data

**Responsibility**
- Item, catalog, and reference data handling
- Canon-aligned master entities

**Must Not**
- Contain costing calculations
- Embed business-specific overrides

---

### 3.3 Costing Engine (QCD / QCA)

**Responsibility**
- Cost aggregation per QCD Contract
- Cost head/bucket logic
- Quantity roll-ups

**Must Not**
- Read from UI spreadsheets as source of truth
- Modify schema meanings
- Contain UI rendering logic

---

### 3.4 Database & Persistence Layer

**Responsibility**
- Canon-aligned schema persistence
- Seed execution (approved weeks only)
- Migration or DDL execution (as per DB creation method)

**Must Not**
- Implement business logic
- Bypass Canon drift checks

---

### 3.5 API Layer

**Responsibility**
- Expose engine outputs
- Enforce input validation
- Maintain backward compatibility

**Must Not**
- Reinterpret Canon-defined fields
- Perform core costing calculations

---

### 3.6 UI & Reporting

**Responsibility**
- Visualization and reporting
- User interaction and workflows

**Must Not**
- Compute authoritative costs
- Override engine outputs

---

## 4. Pull Request (PR) Rules

### 4.1 General Rules

- One PR = **one logical change**
- PR must map to **exactly one Task ID** from Phase-6 Task Register
- No undocumented work allowed
- Evidence links required for:
  - Compliance tasks
  - Gate-impacting changes

---

### 4.2 Canon-Impacting Changes

Any PR that:
- Touches schema-related code
- Alters data meanings
- Affects Canon-aligned behavior

**Requires:**
- Phase-6 Decision Register entry
- Explicit governance approval
- Updated evidence artifacts

---

### 4.3 Costing Engine PRs

- Must reference **QCD Contract v1.0**
- Must not introduce implicit logic
- Determinism must be preserved
- Audit fields must remain intact

---

### 4.4 Database PRs

- Must align with DB creation method decision
- Must pass schema drift validation
- Seed execution only in approved weeks

---

### 4.5 Category D Freeze PRs

- Must not modify Category D frozen artifacts
- Must respect Category D freeze boundaries
- Requires explicit approval if touching Category D scope

---

### 4.6 Review & Approval

- Minimum one functional reviewer
- Compliance tasks require governance reviewer
- Reviewer must verify:
  - Canon alignment
  - Contract adherence
  - Task ID presence
  - Category D freeze compliance (if applicable)

---

## 5. Enforcement

- PRs violating these rules **must not be merged**
- Repeated violations escalate to Phase-6 governance review
- Emergency fixes still require post-facto documentation

---

## 6. Week-0 Status

- Boundaries: ✅ DEFINED
- PR Rules: ✅ DEFINED
- Enforcement: Starts Phase-6 execution

**P6-SETUP-008:** ✅ **COMPLETE**

---

## 7. References

- Schema Canon v1.0  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- QCD Contract v1.0  
  `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
- Phase-6 Task Register  
  `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`
- D0 Gate Checklist  
  `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`
- Category D Freeze  
  `docs/PHASE_5/02_CATEGORY_D_FREEZE/`

---

**End of Document**
