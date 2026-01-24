# Cost Template Seed Specification (Spec-Only)

**Version:** v1.0  
**Status:** ✅ SPEC ONLY (Week-0)  
**Date:** 2026-01-12  
**Phase:** Phase-6 Week-0

> **Critical:** No DB mutation in Week-0. This is a specification document only.

---

## Schema Authority Statement (Mandatory)

All table structures, column definitions, constraints, enums, and data meanings are governed exclusively by:

**`docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`**

Phase-6 Week-0 introduces **no schema additions, deletions, or reinterpretations**.  
This document defines **logical seed intent only**, fully aligned to the frozen Canon.

---

## 1. Purpose

This document defines the **logical seed intent** required for costing templates to operate consistently across quotations.

**Scope (Week-0):**
- ✅ Logical seed categories definition
- ✅ Illustrative example data (intent only)
- ✅ Logical validation rules
- ❌ No table or column definitions (already defined in Canon)
- ❌ No DB mutations
- ❌ No seed script execution

**Execution Note:**  
Seed implementation will occur in Phase-6 Track E (Week-1+), using this document as the **authoritative seed intent**.

---

## 1.1 Canon Mapping (Evidence Only)

This specification references the following **frozen Canon sections**.  
No physical table names are asserted here.

- **Canonical inventory:**  
  `Section 4 — Canonical Table Inventory`
  - Quotation & costing context: **4.4 QUO**
  - Pricing inputs & rate sources: **4.5 PRICING**
  - Shared master/reference entities (e.g., heads, buckets): **4.7 SHARED**
  - Audit/versioning fields: **4.8 AUDIT**

- **Enums & constraints:**  
  `Section 5 — Canonical Enums / Check Constraints`

- **Seed design reference:**  
  `Section 8 — Seed Script (Design Validation Artifact)`

All references in this document are **evidence-aligned** to the above sections.

---

## 2. Seed Entities & Fields

> **Important:**  
> Seed entities below express **intent only**.  
> Exact records, constraints, and physical mappings must conform to Canon v1.0 at implementation time.

### 2.1 Cost Head Entity (Seed Intent)

**Logical Entity:** Cost Head Types

**Canonical Reference:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 4.7 (SHARED) and Section 4.4 (QUO)`  
(Constraints/enums governed by Section 5)

**Required Logical Fields (as per Canon):**
- `id` (primary identifier)
- `name` (e.g., MATERIAL, BUSBAR, FABRICATION, LABOUR)
- `category` (CostBucket enum: MATERIAL, LABOUR, OTHER)
- `tenant_id` (tenant isolation context)

**Seed Rows (Illustrative — Intent Only):**

| name | category | Description |
|------|----------|-------------|
| MATERIAL | MATERIAL | Base material costs derived from BOM |
| BUSBAR | MATERIAL | Busbar material costs |
| FABRICATION | MATERIAL | Fabrication costs (summary bucket) |
| LABOUR | LABOUR | Labour costs |
| TRANSPORTATION | OTHER | Transportation costs |
| ERECTION | LABOUR | Erection labour costs |
| COMMISSIONING | OTHER | Commissioning costs |
| MISC | OTHER | Miscellaneous costs |

> **Note:**  
> Illustrative rows below express **seed intent** only.  
> Exact records must match Canon v1.0 definitions and constraints at implementation time.

**Source of Truth:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 4 (Canonical Table Inventory), primarily **4.7 SHARED** and **4.4 QUO**; constraints/enums in **Section 5**.

---

### 2.2 Cost Template Types (Logical Seed)

**Logical Entity:** Template Type Categories

**Canonical Reference:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 4.4 (QUO) and Section 5 (Enums/Constraints)`

**Required Logical Fields (as per Canon):**
- Template type identifier
- Template name
- Default calculation mode
- Default UOM (unit of measure)

**Seed Rows (Illustrative — Intent Only):**

| Type | Name | Default Calc Mode | Default UOM |
|------|------|-------------------|-------------|
| LUMP_SUM | Lump Sum | LUMP_SUM | — |
| QTY_RATE | Quantity × Rate | QTY_RATE | Each |
| KG_RATE | Weight × Rate | KG_RATE | kg |
| METER_RATE | Length × Rate | METER_RATE | meter |
| HOUR_RATE | Time × Rate | HOUR_RATE | hour |
| PERCENT_OF_BASE | Percentage of Base | PERCENT_OF_BASE | % |

> **Note:**  
> Illustrative rows express **seed intent** only.  
> Exact records must match Canon v1.0 definitions and constraints at implementation time.

**Source of Truth:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 4.4 (QUO) and Section 5 (Enums/Constraints)`

---

### 2.3 Default Cost Adders (Logical Seed)

**Logical Entity:** Default Cost Adder Profiles

**Canonical Reference:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 4.4 (QUO) and Section 4.7 (SHARED)`

**Required Logical Fields (as per Canon):**
- Adder name
- Cost head reference
- Default rate (if applicable)
- Default UOM

**Seed Rows (Illustrative — Intent Only):**

| Adder Name | Cost Head | Default Rate | Default UOM | Notes |
|------------|-----------|--------------|-------------|-------|
| Standard Busbar | BUSBAR | — | — | Per panel calculation |
| Basic Fabrication | FABRICATION | — | — | Per panel calculation |
| Standard Labour | LABOUR | — | — | Per panel calculation |
| Standard Transport | TRANSPORTATION | — | — | Per panel calculation |
| Standard Erection | ERECTION | — | — | Per panel calculation |
| Standard Commissioning | COMMISSIONING | — | — | Percentage of base |

> **Note:**  
> Illustrative rows express **seed intent** only.  
> Exact records must match Canon v1.0 definitions and constraints at implementation time.

**Source of Truth:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 4.4 (QUO) and Section 4.7 (SHARED)`  
Business rules are governed by Phase-5 Decision Register and Canon constraints.

---

## 3. Validation Rules (Logical)

> **Important:**  
> All validation rules below are **logical specifications**.  
> Actual DB constraints, enums, and uniqueness rules are defined in Schema Canon v1.0 (Section 5).

### 3.1 Non-Null Constraints (Logical)

The following fields must be non-null in seed data:
- Cost head name
- Cost head category
- Template type identifier
- Template name
- Adder name (if applicable)

**Canon Reference:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 5 (Canonical Enums / Check Constraints)`

---

### 3.2 Allowed Values (Logical)

**Cost Head Categories:**
- MATERIAL
- LABOUR
- OTHER

**Calculation Modes:**
- LUMP_SUM
- QTY_RATE
- KG_RATE
- METER_RATE
- HOUR_RATE
- PERCENT_OF_BASE

**Canon Reference:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 5 (Canonical Enums / Check Constraints)`

---

### 3.3 Uniqueness Keys (Logical)

**Cost Heads:**
- `(tenant_id, name)` must be unique

**Template Types:**
- Template type identifier must be unique per tenant

**Canon Reference:**  
`NSW_SCHEMA_CANON_v1.0.md → Section 5 (Canonical Enums / Check Constraints)`

---

## 4. Execution Note

**Week-0 Status:** ✅ SPEC DEFINED

**Implementation:**
- Seed script to be created in Week-1+ (Track E)
- Seed execution to be performed in Week-1+ (Track E)
- No DB mutations in Week-0

**Spec Completeness:**
- ✅ Logical entities defined
- ✅ Example rows provided
- ✅ Validation rules specified
- ✅ Source of truth referenced (Canon)

This spec is concrete enough that engineering can write a seed script without guessing.

---

## 5. References

- **Schema Canon v1.0:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Canonical Table Inventory:** Section 4 (4.4 QUO, 4.7 SHARED)
- **Enums & Constraints:** Section 5
- **Seed Design Reference:** Section 8 (Seed Script — Design Validation Artifact)
- **Week-0 Evidence:**  
  `evidence/PHASE6_WEEK0_RUN_20260112_140401/`

---

## 6. Specification Acceptance

**P6-DB-005:** ✅ **COMPLETE** (Spec-Only)

This specification is defined and ready for seed script implementation in Phase-6 Track E (Week-1+).

**Seed Intent Governance:**  
Seed intent is governed by `NSW_SCHEMA_CANON_v1.0.md → Section 8 (Seed Script — Design Validation Artifact)`.  
Week-0 provides specification only (no DB mutation).

---

**End of Document**
