# Phase-6 Legacy Parity Addition Summary

**Version:** 1.3  
**Date:** 2025-01-27  
**Status:** ADDED TO EXECUTION PLAN  
**Based On:** Nish Review Report + Legacy Parity Analysis

---

## 🎯 Purpose

This document summarizes the addition of Track A-R (Reuse & Legacy Parity) to Phase-6 Execution Plan v1.3, ensuring all legacy capabilities from Phase-1–4 and Nish system are preserved in NSW.

---

## 📋 What Was Added

### Track A-R: Reuse & Legacy Parity (NEW)
**7 tasks, Weeks 2-4**

**Purpose:** Guarantee that nothing users could do in Nish / Phase-1–4 is lost in NSW.

**Key Capabilities:**
1. **Quotation Reuse** - Copy old quotation → modify
2. **Panel Reuse** - Copy panel subtree into quotation
3. **Feeder Reuse** - Copy feeder (Level-0 BOM) + subtree
4. **BOM Reuse** - Copy BOM from past quotation
5. **Master BOM Apply** - Apply Master BOM template
6. **Post-Reuse Editability** - All copied content editable until locked
7. **Guardrail Enforcement** - G1-G8 enforced after reuse

---

## 🔄 Canonical Workflow Statement

**Once a quotation exists, the user must have three equivalent entry paths:**

### Path A — Reuse an existing quotation (fastest)
- Pick an old quotation (or old panel within it)
- Copy it into a new quotation (or reuse within same quote)
- Modify: panel qty, feeder qty, BOM qty, items, pricing

### Path B — Create a new quotation + reuse building blocks
- Create new quotation, then inside it:
  1. Add a panel
  2. Under panel: Reuse a feeder from same quotation OR past project/quotation OR create new
  3. Under feeder: Apply Master BOM template OR reuse previous project BOM OR create new BOM manually
  4. Under BOM: Edit existing items, add items, delete items, resolve L0→L1→L2, then pricing resolution

### Path C — Create from template first (structured start)
- Create quotation → add panel → add feeder → apply Master BOM
- Then modify as needed

---

## 📊 New Tasks Added

### Week 2.5: Reuse Foundations (2 tasks)

- **P6-UI-REUSE-001:** Copy quotation (deep copy)
  - Copy full hierarchy: panels → feeders → BOMs → items
  - Populate BOM tracking fields
  - Preserve pricing fields
  - UI action: "Create quotation from existing quotation"

- **P6-UI-REUSE-002:** Copy panel into quotation
  - Copy panel subtree (feeders → BOMs → items)
  - Source: same quotation OR past quotation
  - Editable until locked

### Week 3: Feeder & BOM Reuse (3 tasks)

- **P6-UI-REUSE-003:** Copy feeder (Level-0 BOM)
  - Copy feeder + full subtree
  - Source: same quotation OR past quotation
  - Target: selected panel
  - Preserve hierarchy & quantities

- **P6-UI-REUSE-004:** Copy BOM under feeder
  - Copy BOM subtree (child BOMs + items)
  - Source: past project / quotation
  - Target: feeder or parent BOM
  - Mark copied BOM as instance (copy-never-link)

- **P6-UI-REUSE-005:** Apply Master BOM template
  - Apply Master BOM (L1 products only)
  - Populate origin_master_bom_id
  - Immediately enter L0→L1→L2 resolution flow

### Week 4: Editability & Guardrails Validation (2 tasks)

- **P6-UI-REUSE-006:** Post-reuse editability check
  - Verify all copied content is editable
  - Add / remove / replace items allowed
  - Quantity changes allowed
  - Pricing overrides allowed
  - Locking respected (D-005)

- **P6-UI-REUSE-007:** Guardrail enforcement after reuse
  - Verify G1-G8 enforced on reused content
  - Test guardrail enforcement after each reuse operation

---

## 🔐 Legacy Parity Verification Gate (NEW)

**Location:** Week 8.5 (before Integration)

**Purpose:** Verify all legacy capabilities preserved through reuse workflows

**Gate Checklist:**
- **P6-GATE-LEGACY-001:** Quotation reuse verified
- **P6-GATE-LEGACY-002:** Panel reuse verified
- **P6-GATE-LEGACY-003:** Feeder reuse verified
- **P6-GATE-LEGACY-004:** BOM reuse verified
- **P6-GATE-LEGACY-005:** Post-reuse guardrails verified
- **P6-GATE-LEGACY-006:** Legacy parity checklist complete

**Gate Rule:** Phase-6 cannot proceed to Integration unless all legacy parity items are verified.

**Reference:** `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`

---

## 📋 Legacy Parity Checklist Created

**File:** `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`

**Sections:**
- A. Quotation Lifecycle & Reuse (5 items)
- B. Panel / Feeder / BOM Reuse (8 items)
- C. BOM & Item Editability (5 items)
- D. Pricing, Discount & Bulk Operations (5 items)
- E. Quantity & Cost Semantics (6 items)
- F. Masters & Catalog (6 items)
- G. Navigation & Dashboard Parity (4 items)
- H. Audit, History & Safety (3 items)
- I. Customer & Project Management (3 items)
- J. Catalog UI Views (3 items)

**Total:** 48 verification items

---

## ✅ What This Does NOT Change

- ✅ Does NOT change Schema Canon v1.0
- ✅ Does NOT change Guardrails G1–G8
- ✅ Does NOT change Locking scope (line-item only)
- ✅ Does NOT change Resolution semantics (L0/L1/L2)
- ✅ Does NOT change Pricing meaning
- ✅ Does NOT introduce new tables or fields
- ✅ Does NOT introduce new business rules

**This is purely execution completeness and UX parity.**

---

## 📊 Updated Statistics

### Track Count
- **Before:** 6 tracks (A, B, C, D0, D, E)
- **After:** 7 tracks (A, A-R, B, C, D0, D, E)
- **Change:** Track A-R added

### Task Count
- **Before:** ~110 tasks
- **After:** ~123 tasks
- **Added:** 13 tasks (7 reuse tasks + 6 gate tasks)

### Duration
- **Before:** 10-12 weeks
- **After:** 10-12 weeks (unchanged, parallel execution)

---

## 🔗 Integration Points

### With Track A (Productisation)
- Reuse workflows use same UI components
- Reuse workflows respect locking visibility
- Reuse workflows respect error/warning surfacing

### With Track E (Canon Implementation)
- Reuse workflows populate BOM tracking fields (P6-BOM-TRACK-001)
- Reuse workflows enforce guardrails (P6-VAL-001..004)
- Reuse workflows respect resolution constraints (P6-RES-023)

### With Track C (Operational Readiness)
- Reuse workflows respect approval flows
- Reuse workflows create audit log entries

### With Integration Week
- Reuse workflow integration test (P6-INT-007)
- End-to-end reuse → pricing → costing flow

---

## 🎯 Success Criteria

Track A-R is **COMPLETE** when:

- ✅ Quotation reuse works (copy old quotation → modify)
- ✅ Panel reuse works (copy panel subtree)
- ✅ Feeder reuse works (copy Level-0 BOM + subtree)
- ✅ BOM reuse works (copy BOM from past quotation)
- ✅ Master BOM application works
- ✅ All reused content editable until locked
- ✅ All guardrails enforced after reuse
- ✅ Legacy Parity Gate PASSED

---

## 📝 Updated Phase-6 Rule

**Phase-6 may add features, but may not change meaning.**
**Phase-6 must preserve all legacy capabilities through copy-never-link reuse.**

---

## 🔗 Related Documents

- **Phase-6 Execution Plan v1.3:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Legacy Parity Checklist:** `docs/PHASE_6/VERIFICATION/PHASE_6_LEGACY_PARITY_CHECKLIST.md`
- **Nish Review Report:** `project/nish/PHASE_6_NISH_REVIEW_REPORT.md`
- **Nish System Reference:** `project/nish/NISH_SYSTEM_REFERENCE.md`

---

**Last Updated:** 2025-01-27  
**Status:** ADDED TO EXECUTION PLAN  
**Next Action:** Begin execution with Track A-R tasks in Weeks 2-4

