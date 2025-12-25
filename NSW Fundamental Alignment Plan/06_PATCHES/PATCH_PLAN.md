# PATCH PLAN — FUNDAMENTALS REALIGNMENT (CONDITIONAL)

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Baseline:** FUNDAMENTALS_BASELINE_BUNDLE_v1.0  
**Status:** 📋 PATCH PLAN ONLY (Apply only if verification fails)  
**Execution:** ❌ Not applied unless triggered by verification findings

---

## 0) Purpose

This document defines **pre-approved patch candidates** that may be applied **only if** read-only verification proves misalignment with the frozen fundamentals baseline.

If all verification checks pass → **NO PATCHES ARE APPLIED**.

---

## 1) Patch Governance Rules (LOCKED)

1. Patches are **conditional**, not mandatory
2. Patches apply **only inside approved execution windows**
3. Each patch:
   - Has a trigger condition
   - Has a defined blast radius
   - Has rollback steps
4. No patch may:
   - Introduce new tables
   - Change schema
   - Break copy-never-link

---

## 2) Patch Candidates

---

### P1 — Feeder Template Filter Standardization

**Problem Trigger**
- Any code path retrieves feeder templates without enforcing:
  ```sql
  TemplateType = 'FEEDER'
  ```

**Verification Trigger**
- VQ-005 returns unexpected rows
- Manual code scan shows feeder templates fetched as generic master BOMs

**Patch Action**
- Update queries / repository methods to explicitly filter:
  ```php
  where('TemplateType', 'FEEDER')
  ```

**Scope**
- Service / repository layer only
- No DB changes

**Blast Radius**
- Feeder creation
- Feeder reuse
- Feeder copy flows

**Rollback**
- Revert commit
- No data impact

---

### P2 — Quotation Ownership Enforcement

**Problem Trigger**
- Runtime entities exist without valid QuotationId
- Orphan rows detected by VQ-004

**Patch Action**
- Add guardrails:
  - Runtime creation must fail if QuotationId missing
  - Optional backfill (read-only decision first):
    ```sql
    UPDATE quotation_sale_boms
    SET QuotationId = :derived_value
    WHERE QuotationId IS NULL;
    ```

**Scope**
- Validation layer
- Optional one-time data repair

**Blast Radius**
- Proposal BOM creation
- Feeder instantiation

**Rollback**
- Guardrails removable
- Data repair requires backup restore (must snapshot first)

---

### P3 — Copy-Never-Link Enforcement Guard

**Problem Trigger**
- Runtime edits mutate master rows
- Runtime flows update master_boms

**Patch Action**
- Add validation guard:
  - Reject writes to master_boms during quotation context
  - Add explicit flags / checks in service layer

**Scope**
- Service layer only

**Blast Radius**
- BOM editing
- Feeder configuration

**Rollback**
- Remove guard
- No data loss

---

### P4 — Legacy Data Normalization (Optional)

**Problem Trigger**
- Legacy imports violate fundamentals
- Mixed TemplateType usage
- Inconsistent MasterBomId references

**Patch Action**
- Create one-time SQL normalization script
- Script must be:
  - Reviewed
  - Dry-run executed
  - Evidence captured

**Scope**
- Data only
- No code behavior change

**Rollback**
- Restore DB snapshot

---

## 3) Patch Application Order (If Needed)

1. P1 — Feeder template filtering
2. P2 — Quotation ownership enforcement
3. P3 — Copy-never-link guard
4. P4 — Legacy normalization (last resort)

---

## 4) Patch Decision Matrix

| Verification Result | Action |
|-------------------|--------|
| All checks pass | ❌ No patches |
| Minor query misalignment | Apply P1 |
| Ownership gaps | Apply P2 |
| Mutation risk | Apply P3 |
| Legacy data corruption | Consider P4 |

---

## 5) Evidence Requirements (Mandatory)

Each applied patch must include:
- Trigger evidence (query output / log)
- Patch commit hash
- Before/after verification results
- Rollback confirmation

---

**END OF PATCH PLAN**

