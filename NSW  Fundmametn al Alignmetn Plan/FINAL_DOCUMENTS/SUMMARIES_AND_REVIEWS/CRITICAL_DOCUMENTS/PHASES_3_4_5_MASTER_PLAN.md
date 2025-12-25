# Phases 3-5 Master Planning Document

**Project:** NSW Estimation Software  
**Mode:** 📋 PLANNING ONLY (No runtime execution)  
**Date:** 2025-12-21  
**Status:** 📋 PLANNING IN PROGRESS  
**Canonical Reference:** `PLANNING/MASTER_PLANNING_INDEX.md`

---

## 🎯 Purpose

This document captures the complete planning for:
- **Phase-3:** BOM Node History & Restore
- **Phase-4:** Lookup Pipeline Verification
- **Phase-5:** Hardening & Freeze

**Rule:** This is a planning artifact only. No runtime execution until all phases are READY and execution window is approved.

---

## 📋 Phase Sequence & Dependencies

```
Phase-1: ✅ PASS (History foundation)
    ↓
Phase-2: 📌 READY (Feeder template apply)
    ↓
Phase-3: 📌 READY (BOM node history + restore)
    ↓
Phase-4: 📌 READY (Lookup pipeline verification)
    ↓
Phase-5: 📌 READY (Hardening + audit + freeze)
```

**Dependency Rule:** Each phase builds on previous phases. Phase-3 requires Phase-2 READY. Phase-4 requires Phase-3 READY. Phase-5 requires all previous phases READY.

**Execution Window Rule:** Execution window todos will be created only after Phase-5 becomes READY and `EXECUTION_APPROVAL.md` exists. Execution strategy decision (combined vs split windows) is deferred until Phase-5 READY.

---

## 🔷 Phase-3: BOM Node History & Restore

### Objective
- Track structural BOM edits (rename, qty, reparent)
- Enable history-safe restore

### Status
**Current:** 📌 READY (Gate-1 planning complete)  
**Gate-2/3:** ⏳ BLOCKED (execution window required)

### Deliverables (Complete)
- [x] BOM node history table schema
- [x] Restore semantics (point-in-time)
- [x] Verification queries
- [x] BomEngine methods for node operations
- [x] Rollback procedures

### Release Pack Structure (Created)
```
PLANNING/RELEASE_PACKS/PHASE3/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 01_ARCH_DECISIONS.md
├─ 02_EVENT_MODEL.md
├─ 03_SCHEMA_NODE_HISTORY.md
├─ 04_BOMENGINE_NODE_OPS_CONTRACT.md
├─ 05_VERIFICATION/
│  ├─ NODE_HISTORY_VERIFICATION.sql
│  └─ RESTORE_VERIFICATION.sql
└─ 06_RISKS_AND_ROLLBACK.md
```

### Gap Mapping
- **BOM-GAP-005, 010, 011, 012:** BOM Node History & Restore
  - Closure path: Gate-3 evidence (execution window required)

---

## 🔷 Phase-4: Lookup Pipeline Verification

### Objective
- Validate Category → SubCategory → Generic → Item
- Prevent broken or partial lookup chains

### Status
**Current:** 📌 READY (Gate-1 planning complete)  
**Gate-2/3:** ⏳ BLOCKED (execution window required)

### Deliverables (Complete)
- [x] Lookup integrity rules (L1-L5)
- [x] Verification SQL queries
- [x] Failure modes + rollback
- [x] Repair procedures

### Release Pack Structure (Created)
```
PLANNING/RELEASE_PACKS/PHASE4/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 01_SCOPE_LOCK.md
├─ 02_LOOKUP_INTEGRITY_RULES.md
├─ 03_SCHEMA_OPTIONAL_AUDIT_TABLE.md
├─ 04_VERIFICATION/
│  └─ LOOKUP_INTEGRITY_VERIFICATION.sql
├─ 05_FAILURE_MODES_AND_REPAIR.md
└─ 06_RISKS_AND_ROLLBACK.md
```

### Gap Mapping
- **BOM-GAP-006:** Lookup Pipeline Preservation Not Verified After Copy
  - Closure path: Verification SQL + repair playbook (Gate-3 evidence)

---

## 🔷 Phase-5: Hardening & Freeze

### Objective
- System-wide consistency
- Audit completeness
- Release freeze

### Status
**Current:** 📌 READY (Gate-1 planning complete)  
**Gate-2/3:** ⏳ BLOCKED (execution window required)

### Deliverables (Complete)
- [x] Cross-phase audit checklist
- [x] Freeze checklist
- [x] Final rollback policy
- [x] System-wide verification
- [x] Release readiness criteria

### Release Pack Structure (Created)
```
PLANNING/RELEASE_PACKS/PHASE5/
├─ 00_README_RUNBOOK.md
├─ STATUS.md
├─ 01_AUDIT_CHECKLIST.md
├─ 02_FREEZE_CHECKLIST.md
├─ 03_ROLLBACK_POLICY.md
├─ 04_EXECUTION_SCRIPTS/
├─ 05_VERIFICATION/
└─ 06_RISKS_AND_ROLLBACK.md
```

---

## 📝 Planning Capture Area

### Phase-3 Detailed Planning
<!-- Paste Phase-3 planning details here -->


### Phase-4 Detailed Planning
<!-- Paste Phase-4 planning details here -->


### Phase-5 Detailed Planning
<!-- Paste Phase-5 planning details here -->


---

## 🔗 Related Documents

- **Master Index:** `PLANNING/MASTER_PLANNING_INDEX.md`
- **Phase-2 Release Pack:** `PLANNING/RELEASE_PACKS/PHASE2/`
- **Gap Register:** `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`

---

## ⚠️ Planning Mode Rules

- ✅ All planning happens in this workspace only
- ⛔ No runtime workspace (`/Projects/nish`) modifications
- ✅ Planning artifacts only (no code execution)
- ✅ Update `MASTER_PLANNING_INDEX.md` when phases move to READY

## 🚫 Execution Window Governance

**PRE-EXECUTION DRAFT (BLOCKED):**
- ❌ **Blocked until Phase-5 is READY + `EXECUTION_APPROVAL.md` exists**
- ❌ No execution window todos should be created until all phases (1-5) are READY
- ❌ Execution strategy decision (combined vs split windows) is deferred until Phase-5 READY
- ✅ Execution todos will be created only after Phase-5 READY

**Gate Status Definitions:**
- **PASS** = Evidence captured (runtime validation complete)
- **READY** = Planning complete; no runtime work; evidence not captured
- **BLOCKED** = Execution window required (gates remain READY until execution approval)
- **PLANNED** = Not yet packaged

---

**END OF PHASES 3-5 MASTER PLANNING**

