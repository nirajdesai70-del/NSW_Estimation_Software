# P6-DB-001 — Database Creation Method (DDL vs Migrations)

**Phase:** Phase-6  
**Week:** Week-0  
**Document ID:** P6-DB-001  
**Version:** v1.0  
**Status:** ✅ DECIDED  
**Date:** 2026-01-12

---

## 1. Purpose

This document records the **database creation approach** for Phase-6 to ensure
Canon alignment, repeatability, and auditability.

**Scope (Week-0):**
- ✅ Decision and rationale
- ✅ Governance alignment
- ❌ No DB creation
- ❌ No migrations execution
- ❌ No schema meaning changes

---

## 2. Authorities & References

- **Schema Authority:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **DDL Authority:**  
  `NSW_SCHEMA_CANON_v1.0.md → Section 7 (DDL — Authoritative)`
- **Seed Design Reference:**  
  `NSW_SCHEMA_CANON_v1.0.md → Section 8 (Seed Script — Design Validation Artifact)`
- **Governance:**  
  `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`

---

## 3. Options Considered

### Option A — DDL-First (Canon-Driven)
- Create databases using **authoritative DDL** from the Schema Canon.
- Enforce parity via schema drift checks.
- Use migrations **only after** Canon changes are approved.

**Pros**
- Canon is the single source of truth
- Deterministic environments (dev/stage/prod)
- Simplified audit and rollback
- Clear governance boundaries

**Cons**
- Less flexibility for ad-hoc changes (by design)

---

### Option B — Migrations-First
- Build schema incrementally via migrations.
- Canon maintained as documentation mirror.

**Pros**
- Flexible for rapid iteration

**Cons**
- Risk of Canon drift
- Higher governance overhead
- Harder parity assurance across environments

---

## 4. Decision

**Chosen Approach:** ✅ **DDL-First (Canon-Driven)**

---

## 5. Rationale

- Schema Canon v1.0 is already **frozen and authoritative**.
- Section 7 of the Canon provides **authoritative DDL**, suitable for environment creation.
- Drift validation tooling (`check_schema_drift.sh`) enforces parity.
- Reduces operational and audit risk during Phase-6 execution.
- Aligns with Week-0 governance principle: Canon is the source of truth.

---

## 6. Implementation Policy (Forward-Looking)

> **Note:** This section defines policy only. No execution occurs in Week-0.

- **Initial DB creation:** Use Canon DDL (Section 7).
- **Incremental changes:**  
  - Require Canon version bump
  - Require Phase-6 Decision Register approval
  - Implement via controlled migrations if approved
- **Seeds:**  
  - Follow Canon Section 8 + Phase-6 seed specifications
  - Execute only in approved execution weeks

---

## 7. Guardrails

- No schema meaning changes without Canon approval.
- All environments must pass schema drift validation.
- Emergency fixes require post-facto governance documentation.
- Migrations are only used post-Canon-approval (not for initial creation).

---

## 8. Conclusion

The **DDL-first, Canon-driven** approach is adopted for Phase-6.

**P6-DB-001:** ✅ **COMPLETE**

---

## References

- **Schema Canon v1.0:**  
  `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Schema Drift Check:**  
  `scripts/check_schema_drift.sh`
- **Phase-6 Task Register:**  
  `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`
- **Cost Template Seed Spec:**  
  `docs/PHASE_6/DB/COST_TEMPLATE_SEED.md`

---

**End of Document**
