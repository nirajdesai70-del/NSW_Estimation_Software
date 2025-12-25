# Patch Appendix v1.1 — Audit-Safe Guardrails

**Version:** v1.1  
**Date:** 2025-12-XX (Placeholder; derives from repo doc dates)  
**Status:** 📋 PLANNING MODE ONLY  
**Purpose:** Addresses identified gaps in v1.0 to make pack audit-proof

---

## Universal Badge Legend

All documents in this pack must use these badges to indicate truth level:

| Badge | Meaning | Usage |
|-------|---------|-------|
| **CONFIRMED-IN-REPO** | Explicitly found in repository (migration/model/query file reference) | Use when file path exists and content verified |
| **INFERRED** | Hypothesis based on usage patterns or documentation references | Use when schema/field names are assumed from context |
| **DOC-CLOSED** | Documentation/spec frozen; planning complete; no runtime validation | Use for documentation-only closure |
| **RUN-CLOSED** | Verified via SQL/API requests + evidence archive; runtime validated | Use when runtime evidence exists |

**Rule:** Any table/field naming shown as schema is hypothesis unless backed by an explicit migration/model/query file reference. Hypotheses must be tagged as **INFERRED** and never treated as truth.

---

## Gap 1: Schema Inference vs Repo-Only Claim

### Problem
Pack claims "Source of Truth: Repository content only (no invented schemas/fields)" but uses inferred schemas without explicit tagging.

### Fix Applied
All schema references now tagged:
- **CONFIRMED-IN-REPO:** When migration/model/query file exists
- **INFERRED:** When schema is assumed from documentation context

### Examples
- `categories` table → **INFERRED** (no migration found)
- `products` table with `ProductType` → **INFERRED** (referenced in docs, no migration verified)
- `master_boms` table → **INFERRED** (referenced in docs, no migration verified)
- `quotation_sale_boms` table → **INFERRED** (referenced in docs, no migration verified)

---

## Gap 2: Date/Version Metadata Inconsistency

### Problem
Pack uses "2025-01-XX" but referenced work is Dec 2025 (20251218, 20251219, 20251222).

### Fix Applied
- Updated date format: **2025-12-XX** (placeholder; derives from repo doc dates)
- Added explicit note: "Date is placeholder; derives from repo doc dates."

---

## Gap 3: Closure Language Mixing DOC vs RUN

### Problem
"Fundamentals gaps CLOSED" mixes documentation closure with runtime closure.

### Fix Applied
Two closure levels introduced:
- **DOC-CLOSED:** Planning/spec frozen; no runtime validation
- **RUN-CLOSED:** Verified via SQL/requests + evidence archive

### Status Updates
- Fundamentals Gap Correction: **DOC-CLOSED** (Phase-0 execution complete, documentation frozen)
- BOM-GAP-001 (Feeder reuse): **OPEN** (runtime implementation pending)
- BOM-GAP-002 (Clear-before-copy): **OPEN** (runtime implementation pending)
- BOM-GAP-003 (Line item history): **RUN-CLOSED** (Phase-1A PASS, evidence attached)
- BOM-GAP-004 (Copy history): **PARTIALLY RESOLVED** (code exists, verification pending)
- BOM-GAP-005 (BOM node history): **NOT IMPLEMENTED** (planned for Phase-3)
- BOM-GAP-006 (Lookup pipeline): **OPEN** (needs verification)

---

## Gap 4: Legacy Data Integrity Problem

### Problem
Pack treats system as "logically clean" but real-world fundamental blocker is legacy data integrity (imported SQL, incorrect relational linking, polluted item master, hierarchy disturbance).

### Fix Applied
Added dedicated section: **Legacy Data Integrity & Remediation Strategy**

See section below for full details.

---

## Gap 5: Code Locality Reality

### Problem
Pack references `app/Services/BomEngine.php` but repository may be documentation-only with actual Laravel code in separate repository or `source_snapshot/` directory.

### Fix Applied
Added "Codebase Locality" preface to IMPLEMENTATION_MAPPING.md:

> **⚠️ CODEBASE LOCALITY NOTE:**  
> This repository (`NSW_Estimation_Software_Fundamentals`) is a **documentation/standards-only** repository. The actual Laravel application codebase (containing `app/Services/BomEngine.php`, `app/Http/Controllers/`, etc.) is in a **separate repository** or may be located in `source_snapshot/` directory.  
> **All code paths must be confirmed under the actual Laravel root.** Mapping remains provisional until verified.

---

## Gap 6: Panel Master Definition Ungrounded

### Problem
Panel BOM section says Panel Master schema "NOT FOUND" but assumes `quotation_sale` + Panel copy operations.

### Fix Applied
Added "Panel Master Discovery Checklist":

1. **Exact model/table/template type:** Where is Panel Master stored?
2. **Feeder attachment:** How do Feeder Masters attach to Panel Master?
3. **Panel metadata:** Where does panel name/type, default feeders, etc. live?
4. **Panel lookup:** How is Panel Master identified/retrieved?

**Status:** **INFERRED** — Panel Master concept exists in planning but schema not confirmed in repo.

---

## Gap 7: ProductType/MakeId/SeriesId Naming Assumption

### Problem
Pack relies heavily on `ProductType=1/2`, `MakeId > 0`, `SeriesId > 0` without confirming these are actual column names.

### Fix Applied
Separated logical rules from physical implementation:

- **Logical Rule:** Generic vs Specific must be distinguishable (L0/L1 = Generic, L2 = Specific)
- **Physical Implementation:** `ProductType` column → **INFERRED** (referenced in docs, no migration verified)
- **Physical Implementation:** `MakeId` and `SeriesId` columns → **INFERRED** (referenced in docs, no migration verified)

All schema references tagged **INFERRED** unless migration/model file explicitly found.

---

## Gap 8: UI/Controller Integration Layer Underrepresented

### Problem
Pack mentions "thin controller" generally but lacks grounded "screen → API → service → DB" map.

### Fix Applied
Added "Execution Mapping Bridge" section to IMPLEMENTATION_MAPPING.md:

**Screen → Action → Endpoint → Service → Gates → Evidence Queries**

Example:
- **Screen:** Quotation BOM Editor
- **Action:** Apply Feeder Template
- **Endpoint:** `POST /quotation/{quotation}/panel/{panel}/feeder/apply-template`
- **Service:** `BomEngine::copyFeederTree()`
- **Gates:** Gate-0 (Source Readiness), Gate-1 (Schema), Gate-2 (Wiring), Gate-3 (R1/S1/R2/S2)
- **Evidence:** R1 JSON, S1 SQL, R2 JSON, S2 SQL

---

## Legacy Data Integrity & Remediation Strategy

### Problem Statement

The NSW Estimation Software has a fundamental legacy data integrity problem:
- Imported SQL with incorrect relational linking
- Item master polluted / hierarchy disturbed
- Thousands of items needing reconciliation
- Lookup pipeline failures due to broken references
- Inability to create new items correctly

This is a **non-negotiable fundamental blocker** that must be addressed before other fundamentals work can proceed reliably.

### Symptoms

1. **Orphan Items:** Items without valid Category/Subcategory/Item references
2. **Wrong Joins:** Incorrect relational linking between tables
3. **Missing Make/Series Mapping:** ProductType=2 items missing MakeId/SeriesId
4. **Hierarchy Disturbance:** Category → Subcategory → Item chain broken
5. **Lookup Pipeline Failures:** SKU search fails due to broken references

### Risk Impact

- **Lookup Pipeline Failures:** Category → Subcategory → Item → Product chain broken
- **Inability to Create New Items:** Cannot create items correctly due to polluted master
- **BOM Resolution Failures:** L1 → L2 resolution fails due to broken product references
- **Costing/Export Failures:** Incomplete product resolution causes calculation errors

### Remediation Sequencing

**Phase 1: Clean Masters**
1. Identify and isolate clean master data
2. Document current state (orphan items, broken references)
3. Create clean master baseline

**Phase 2: Mapping**
1. Map legacy data to clean master structure
2. Create reconciliation rules
3. Document mapping decisions

**Phase 3: Controlled Data Corrections**
1. Apply corrections in controlled batches
2. Verify each batch before proceeding
3. Capture evidence for each correction

**Phase 4: Verification**
1. Verify lookup pipeline integrity
2. Verify product resolution works
3. Verify BOM operations work with cleaned data

### Evidence Requirements

- **Before State:** SQL queries showing orphan items, broken references
- **Mapping Decisions:** Documented reconciliation rules
- **Correction Evidence:** SQL output for each correction batch
- **After State:** SQL queries verifying integrity restored

### Status

**NOT FOUND IN REPO:** Legacy data integrity remediation plan not found in repository.

**Recommendation:** Create dedicated remediation plan document before proceeding with other fundamentals work.

---

## Implementation Status Corrections

### Runtime Claims vs Planning Claims

All implementation status must be tagged:

| Status | Meaning | Evidence Required |
|--------|---------|-------------------|
| **DOC-CLOSED** | Documentation complete | Documentation file exists |
| **RUN-CLOSED** | Runtime verified | SQL output, API responses, test results |
| **PARTIALLY RESOLVED** | Code exists, verification pending | Code file exists, evidence pending |
| **NOT IMPLEMENTED** | Not started | No code, no evidence |

### Examples

- **"Phase-0 execution complete PASS WITH NOTES"** → **DOC-CLOSED** (documentation frozen, no runtime evidence linked)
- **"Gate-1 PASS — bom_copy_history schema verified"** → **RUN-CLOSED** (if runtime evidence exists) or **DOC-CLOSED** (if planning-only)
- **"Resolution-B rules implemented"** → **PARTIALLY RESOLVED** (code exists, verification pending) or **DOC-CLOSED** (documented design only)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial pack created |
| v1.1 | 2025-12-XX | Patch appendix added (audit-safe guardrails, legacy data integrity, closure language fixes) |

---

**END OF PATCH APPENDIX v1.1**

