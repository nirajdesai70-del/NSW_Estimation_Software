# Phase-6 Execution Plan Revision Summary

**Version:** 1.2  
**Date:** 2025-01-27  
**Status:** REVISED  
**Based On:** Phase-5 Detailed Working Record Gap Analysis

---

## 🎯 Revision Purpose

This revision incorporates all Phase-5 implementation obligations that were missing from the original Phase-6 plan. The gap analysis identified critical items that Phase-6 must implement to comply with Phase-5 frozen specifications.

---

## 📋 What Was Added

### 1. Database Implementation Track (Track E) - NEW
**6 tasks, Weeks 0-1**

- **P6-DB-001:** Convert Schema Canon DDL into migrations
- **P6-DB-002:** Create seed script structure
- **P6-DB-003:** Execute migrations (dev/staging)
- **P6-DB-004:** Execute seed scripts (dev/staging)
- **P6-DB-005:** Schema parity check: migrations == Schema Canon v1.0
- **P6-DB-006:** Add baseline indexes per Canon + performance assumptions

**Rationale:** Phase-5 froze Schema Canon but did not create database. Phase-6 must implement the frozen schema.

---

### 2. API Contract Implementation Track (Track F) - NEW (Optional/Deferred)
**6 tasks, Weeks 3-6**

- **P6-API-001:** Implement API endpoints per 01_API_SURFACE_MAP.md
- **P6-API-002:** Apply JSON schemas per OpenAPI skeleton
- **P6-API-003:** Validation matrix parity
- **P6-API-004:** Error taxonomy + request_id propagation
- **P6-API-005:** Contract tests
- **P6-API-006:** Versioning policy implementation

**Rationale:** Phase-5 froze API contracts (Category B). Phase-6 should implement them OR explicitly defer to Phase-7.

**Note:** Marked as optional/deferred - can be implemented in Phase-7 if UI-first approach is taken.

---

### 3. Runtime Guardrails Enforcement (Added to Track A)
**4 tasks, Week 3**

- **P6-VAL-001:** Implement runtime guardrails G1-G8 in service layer
- **P6-VAL-002:** Ensure DB CHECK/constraints enforced & migrations match Schema Canon
- **P6-VAL-003:** API validation parity with 02_VALIDATION_MATRIX.md
- **P6-VAL-004:** Guardrail test suite (unit + integration)

**Rationale:** Phase-5 documented guardrails G1-G8 but did not implement them. Phase-6 must enforce them at runtime.

---

### 4. BOM Tracking Fields Runtime Behavior (Added to Track A)
**3 tasks, Week 2**

- **P6-BOM-TRACK-001:** Populate BOM tracking fields on create/copy
- **P6-BOM-TRACK-002:** Update is_modified/modified_by/modified_at on edits
- **P6-BOM-TRACK-003:** UI indicator "modified vs original" (read-only badge)

**Rationale:** Phase-5 verified tracking fields exist in schema but did not implement runtime behavior.

---

### 5. Multi-SKU Linkage Support (Added to Track A)
**3 tasks, Week 4**

- **P6-SKU-001:** Implement multi-SKU line grouping via parent_line_id
- **P6-SKU-002:** metadata_json structure + UI safe editing rules
- **P6-SKU-003:** Validation & UI display of multi-SKU groups

**Rationale:** Phase-5 locked multi-SKU support (A8, D-007) but Phase-6 plan did not include implementation.

---

### 6. Discount Editor (Legacy Parity) (Added to Track A)
**4 tasks, Week 6**

- **P6-DISC-001:** Implement Discount Editor screen /quotation/{id}/discount
- **P6-DISC-002:** Filters (Make/Category/Item/Desc/SKU/Panel/BOM)
- **P6-DISC-003:** Preview + Apply (transaction)
- **P6-DISC-004:** Audit log entry + approval rules (tie to Track C)

**Rationale:** Critical legacy feature missing from Phase-6 plan. Estimators need bulk discount editing capability.

---

### 7. Customer Snapshot Handling (Added to Track A)
**2 tasks, Week 1**

- **P6-QUO-001A:** Ensure quotation creation stores customer_name_snapshot always
- **P6-QUO-001B:** Allow customer_id optional (future normalization)

**Rationale:** Phase-5 locked customer normalization decision (A9, D-009) but Phase-6 plan did not include implementation.

---

### 8. Resolution Constraints Enforcement (Added to Track A)
**2 tasks, Week 4**

- **P6-RES-023:** Enforce resolution constraints exactly as Schema Canon
- **P6-RES-024:** Errors must map to B3 error taxonomy codes

**Rationale:** Phase-5 locked resolution constraints (A10) but Phase-6 plan did not explicitly enforce them.

---

### 9. Locking Scope Verification (Added to Track A)
**1 task, Week 5**

- **P6-LOCK-000:** Verify no higher-level locking introduced (schema + UI)

**Rationale:** Phase-5 locked line-item locking only (A5, D-005). Phase-6 must verify no scope creep.

---

### 10. Entry Gate Enhancements (Week 0)
**2 tasks added**

- **P6-ENTRY-006:** Naming conventions compliance check
- **P6-SETUP-004:** Review Phase-5 deliverables for implementation obligations
- **P6-SETUP-005:** Create module folder boundaries + PR rules

**Rationale:** Prevent naming drift and ensure module ownership boundaries are enforced.

---

## 📊 Impact Summary

### Task Count Changes
- **Original:** ~92 tasks
- **Revised:** ~110 tasks
- **Added:** ~18 tasks

### Track Changes
- **Original:** 4 tracks (A, B, C, D)
- **Revised:** 6 tracks (A, B, C, D, E, F)
- **New Tracks:** E (Database), F (API - optional)

### Duration Changes
- **Original:** 8-12 weeks
- **Revised:** 12-13 weeks
- **Reason:** Database implementation (Week 0-1) must complete before UI work

### Track A Expansion
- **Original:** 33 tasks
- **Revised:** 45 tasks
- **Added:** 12 tasks (guardrails, BOM tracking, multi-SKU, discount editor, customer snapshot, resolution constraints, locking verification)

---

## ⚠️ Critical Dependencies

### Must Complete First
1. **Track E (Database)** - Weeks 0-1 must complete before all other tracks
2. **Track A Guardrails** - Week 3 must complete before UI validation works correctly

### Can Defer
1. **Track F (API Contracts)** - Can be deferred to Phase-7 if UI-first approach is taken
   - If deferred, explicitly document in Phase-6 closure report
   - Ensure UI can work without API layer initially

---

## ✅ Compliance Checklist

Phase-6 now explicitly addresses:

- [x] Category A (Freeze Gate): All A1-A10 implementation obligations
- [x] Category B (API Contracts): Implementation OR explicit deferral
- [x] Category C (Schema Canon): Database creation and execution
- [x] Category D (Freeze & Approval): Decision implementation
- [x] Legacy Parity: Discount Editor (critical operational feature)

---

## 📝 Notes

1. **API Track (F) is Optional:** If team takes UI-first approach, API implementation can be deferred to Phase-7. However, if API is needed for integration testing, it should be implemented in Phase-6.

2. **Database Track (E) is Mandatory:** Cannot proceed with any UI work until database exists. This is the foundation.

3. **Guardrails are Critical:** Runtime enforcement of G1-G8 is required for data integrity. Cannot be deferred.

4. **Discount Editor is High Priority:** Missing this will cause operational pain for estimators. Should not be deferred.

5. **Module Ownership:** New setup task ensures Phase-5 ownership matrix is enforced in code structure.

---

## 🔗 Related Documents

- **Phase-5 Detailed Working Record:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DETAILED_WORKING_RECORD.md`
- **Phase-6 Execution Plan v1.2:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Phase-6 Complete Scope:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_COMPLETE_SCOPE_AND_TASKS.md`

---

**Last Updated:** 2025-01-27  
**Status:** REVISED - Ready for Review  
**Next Action:** Review revised plan and approve or request further changes
