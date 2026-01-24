# QCD Contract v1.0 (Costing Engine Contract Freeze)

**Version:** v1.0  
**Status:** ✅ FROZEN (Week-0)  
**Date:** 2026-01-12  
**Phase:** Phase-6 Week-0

> **Critical:** This document freezes the costing engine contract only.  
> No implementation, DB mutation, or schema meaning change is permitted in Week-0.

---

## Schema Authority Statement (Mandatory)

All table structures, column definitions, constraints, enums, and data meanings are governed exclusively by:

**`docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`**

Phase-6 Week-0 introduces **no schema additions, deletions, or reinterpretations**.  
This document defines the **logical contract** (inputs → outputs → invariants) only.

---

## 1. Purpose

This document freezes the **Quotation Cost Detail (QCD)** contract to ensure deterministic, auditable costing behavior throughout Phase-6 execution.

**Scope (Week-0):**
- ✅ Contract definition (inputs, outputs, invariants)
- ✅ Canon-aligned references
- ❌ No implementation changes
- ❌ No DB writes or migrations
- ❌ No UI or API expansion
- ❌ No performance tuning

---

## 1.1 Canon Mapping (Evidence Only)

This contract references the following **frozen Canon sections**.  
No physical table names or endpoints are asserted here.

- **Canonical inventory:**  
  `Section 4 — Canonical Table Inventory`
  - Core item & component context: **4.2 CIM**
  - BOM structure & quantities: **4.3 MBOM**
  - Quotation & costing aggregation: **4.4 QUO**
  - Pricing inputs & rate sources: **4.5 PRICING**
  - Shared reference/master entities: **4.7 SHARED**
  - Audit & versioning fields: **4.8 AUDIT**

- **Enums & constraints:**  
  `Section 5 — Canonical Enums / Check Constraints`

- **DDL authority:**  
  `Section 7 — DDL (Authoritative)`

- **Seed design reference (if applicable):**  
  `Section 8 — Seed Script (Design Validation Artifact)`

All references in this document are **evidence-aligned** to the above sections.

---

## 2. Contract Definition

### 2.1 Inputs (Contract)

The costing engine consumes the following **logical inputs**, as defined in the Schema Canon v1.0.

**Item & BOM Context**
- Item identity and attributes  
  *(Canon: Section 4.2 CIM)*
- BOM structure, quantities, and roll-ups  
  *(Canon: Section 4.3 MBOM)*

**Quotation Context**
- Quotation identifiers and grouping context  
  *(Canon: Section 4.4 QUO)*

**Pricing Context**
- Rate source (e.g., pricelist-derived, manual with discount, fixed)  
- Discount values where applicable  
  *(Canon: Section 4.5 PRICING; enums per Section 5)*

**Shared Reference Data**
- Cost head / bucket references
- Calculation modes and UOM context (logical)  
  *(Canon: Section 4.7 SHARED; enums per Section 5)*

**Audit Context**
- Request identifiers
- Versioning markers  
  *(Canon: Section 4.8 AUDIT)*

> **Note:**  
> All field names, constraints, and allowed values are governed by the Canon.  
> This contract does not redefine any structure.

---

### 2.2 Outputs (Contract)

The costing engine produces **deterministic, auditable cost aggregates**.

**Logical Output Set (QCD)**
- Extended cost at line-item level
- Aggregated costs at BOM, panel, and quotation levels
- Cost breakdown by logical cost head/bucket
- Effective quantity calculations (as per Canon-governed rules)
- Audit and versioning metadata

**Output Forms**
- Machine-readable export (e.g., JSON)
- Human-readable export (e.g., spreadsheet)

> **Note:**  
> Output *formats* may evolve in Phase-6 UI/API tracks,  
> but **output meaning and aggregation rules are frozen by this contract**.

---

### 2.3 Invariants / Non-Negotiables

The following invariants are **mandatory** and **non-negotiable**:

1. **No Silent Coercions**
   - All type conversions must be explicit
   - All null handling must be documented
   - No implicit defaults that change meaning

2. **Deterministic Output**
   - Same inputs → same outputs (always)
   - No time-dependent calculations (except audit timestamps)
   - No random or pseudo-random values

3. **Audit Trail Required**
   - Every calculation must be traceable
   - Request ID propagation mandatory
   - Version tracking mandatory

4. **No Schema Meaning Changes**
   - Cannot change field meanings without Canon bump
   - Cannot add new required fields without Canon bump
   - Cannot remove fields without Canon bump

5. **Engine-First Principle**
   - Engine is source of truth
   - Excel is consumer, not driver
   - All displays use QCD aggregates

---

## 3. Out of Scope (Week-0)

The following are **explicitly out of scope** for Week-0:

- Implementation changes
- DB writes or schema mutations
- Seed execution
- UI or API expansion
- Performance optimization

**Evaluation Timing:**  
Contract adherence is evaluated during **D0 Gate signoff** (per plan), not executed in Week-0.

---

## 4. Evidence / References

- **Schema Canon v1.0:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Enums & constraints:** Canon Section 5
- **Week-0 Evidence:**  
  `evidence/PHASE6_WEEK0_RUN_20260112_140401/`
- **Task Register:**  
  `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`

---

## 5. Version Control

**Version:** v1.0  
**Frozen Date:** 2026-01-12  
**Frozen By:** Phase-6 Week-0 Governance

**Change Control:**
- Any contract changes require Phase-6 Decision Register approval
- Contract version bump requires explicit governance approval
- No silent contract changes allowed

---

## 6. Contract Acceptance

**P6-SETUP-005:** ✅ **COMPLETE**  
This contract is frozen and binding for Phase-6 execution.

---

**End of Document**
