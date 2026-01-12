# Phase-6 Kickoff Charter

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT → READY FOR APPROVAL  
**Owner:** Product + Engineering  
**Pre-Requisite:** SPEC-5 v1.0 FROZEN ✅

---

## 1. Phase-6 Purpose

**Phase-6: Productisation & Controlled Expansion**

Phase-6 converts a **correct system** into a **usable product**.

**Phase-5 ensured:**
- Truth is correct
- Rules are enforceable
- Architecture is future-proof

**Phase-6 ensures:**
- Humans can use it
- Catalogs can scale
- Pricing flows are reliable
- Errors are handled gracefully

---

## 2. Phase-6 Scope (What is IN)

### A. Productisation

- Quotation UI (Panels, BOM, Items)
- L0 → L1 → L2 resolution UX
- Pricing resolution UX (PRICELIST / MANUAL / FIXED)
- Locking behaviour visibility (line-item)
- Error & warning surfacing (price missing, unresolved)

### B. Catalog Tooling (Not Catalog Completion)

- Catalog import UI / scripts
- Series-wise catalog onboarding
- Validation previews (before publish)
- Catalog governance enforcement

### C. Operational Readiness

- Role-based access (basic)
- Approval flows (price changes, overrides)
- Audit visibility (read-only)
- Initial SOPs

---

## 3. Explicit Non-Goals

Phase-6 does **NOT** include:
- ❌ Full Schneider catalog completion
- ❌ All OEM onboarding
- ❌ Legacy migration
- ❌ Performance tuning at scale
- ❌ External customer rollout

Those belong to Phase-7.

---

## 4. Phase-6 Entry Criteria

**All must be true:**
- ✅ SPEC-5 v1.0 frozen
- ✅ Schema Canon locked
- ✅ Decision Register closed
- ✅ Freeze Gate Checklist 100% verified
- ✅ Core resolution engine tested

---

## 5. Phase-6 Exit Criteria

Phase-6 is complete when:
- ✅ A quotation can be created end-to-end
- ✅ L1 selection reliably maps to L2 SKUs
- ✅ Pricing resolution works with overrides
- ✅ Catalog entries can be added safely
- ✅ Errors are explainable to users

**Exit Artifact:** NSW v0.6 – Internal Product Ready

---

## 6. High-Level Timeline

| Track | Duration |
|-------|----------|
| UI + Workflow | 4-6 weeks |
| Catalog Tooling | 3-4 weeks |
| Governance & SOP | 2 weeks |
| Stabilisation | 2 weeks |
| **Total** | **~8-12 weeks** |

---

## 7. Key Risks & Controls

| Risk | Control |
|------|---------|
| Catalog chaos | Series-wise SOP (see Catalog Governance SOP) |
| Over-engineering UI | MVP screens only |
| Scope creep | Phase-6 Charter is binding |
| Schema changes | New decision only (v1.1) |

---

## 8. Phase-6 Rule (Lock This Sentence)

**Phase-6 may add features, but may not change meaning.**

---

## 9. Relationship to Phase-5

### What Phase-5 Delivered
- Frozen schema and semantics
- Correct resolution engines
- Governance structure

### What Phase-6 Adds
- Usability (UI)
- Tooling (catalog management)
- Operational workflows (approvals, access)

### What Phase-6 Does NOT Change
- Schema semantics
- Guardrails
- Core business rules
- Locking model
- Resolution logic

---

## 10. Success Metrics

Phase-6 success is measured by:
- ✅ Internal users can create quotations without errors
- ✅ Catalog entries can be imported safely
- ✅ Pricing overrides work correctly
- ✅ Audit trail is visible and complete
- ✅ Errors are understandable and actionable

---

**Last Updated:** 2025-01-27  
**Status:** DRAFT → Ready for Phase-5 completion  
**Next Review:** After SPEC-5 v1.0 freeze approval

