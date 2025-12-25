# Fundamentals Verification Checklist — v1.0

**Freeze:** ✅ FROZEN v1.0  
**Freeze Date:** 2025-12-22 (IST)  
**Change Control:** Any edits require change log entry + reason + version bump

**Project:** NSW Estimation Software  
**Purpose:** Gate-based verification checklist for fundamentals baseline alignment  
**Status:** 🔒 FROZEN (Reference Only)  
**Execution:** Use during execution window (see `EXECUTION_WINDOW_SOP.md`)

---

## Verification Framework

### Gate Structure
- **G1:** Feeder Master Verification
- **G2:** Proposal BOM Master Verification
- **G3:** Hierarchy Verification
- **G4:** Master→Instance Mapping Verification

### Execution Rule
All gates must PASS before execution window can close.  
If any gate fails → proceed to patch decision gate (see `EXECUTION_WINDOW_SOP.md`).

---

## G1: Feeder Master Verification

### G1.1: Feeder Masters Exist
- [ ] VQ-001 executed
- [ ] At least one Feeder Master found
- [ ] All Feeder Masters have `TemplateType='FEEDER'`
- [ ] All Feeder Masters have `Status=0` (active)
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-001.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G1.2: Feeder Master Identity
- [ ] All Feeder Masters have valid `MasterBomId`
- [ ] All Feeder Masters have non-null `MasterBomName`
- [ ] No duplicate Feeder Master identities
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G1.3: Feeder Master → Instance Relationship
- [ ] VQ-002 executed
- [ ] Feeder Instances correctly reference Feeder Masters via `MasterBomId`
- [ ] No orphan Feeder Instances (invalid `MasterBomId`)
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-002.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G1.4: Clear-Before-Copy Verification
- [ ] VQ-002b executed
- [ ] No duplicate stacking detected (same Feeder Master + Quotation + Panel)
- [ ] Clear-before-copy principle maintained
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-002b.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

**G1 Overall Status:** ⬜ PASS / ⬜ FAIL

**If FAIL:** Consider P1 (Feeder Template Filter Standardization) or P3 (Clear-Before-Copy).

---

## G2: Proposal BOM Master Verification

### G2.1: Proposal BOM Master Ownership
- [ ] VQ-003 executed
- [ ] All quotations have valid Proposal BOM Master identity (`QuotationId`)
- [ ] Ownership graph is complete
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-003.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G2.2: Orphan Runtime Entities Check
- [ ] VQ-003b executed
- [ ] Zero orphan runtime entities (all have valid `QuotationId`)
- [ ] No orphan `quotation_sale` rows
- [ ] No orphan `quotation_sale_boms` rows
- [ ] No orphan `quotation_sale_bom_items` rows
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-003b.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G2.3: Ownership Completeness
- [ ] All runtime entities belong to exactly one Proposal BOM Master
- [ ] Ownership is transitive (items → BOMs → feeders → panels → quotation)
- [ ] No cross-quotation references
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

**G2 Overall Status:** ⬜ PASS / ⬜ FAIL

**If FAIL:** Apply P2 (Quotation Ownership Enforcement).

---

## G3: Hierarchy Verification

### G3.1: Design-Time Hierarchy
- [ ] Panel Master → Feeder Master relationship exists
- [ ] Feeder Master → BOM Master relationship exists
- [ ] BOM Master → BOM Item Master relationship exists
- [ ] All masters correctly identified by `TemplateType`
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G3.2: Runtime Hierarchy
- [ ] Proposal BOM Master → Proposal Panels relationship exists
- [ ] Proposal Panels → Feeder Instances relationship exists
- [ ] Feeder Instances → Proposal BOMs relationship exists
- [ ] Proposal BOMs → Proposal BOM Items relationship exists
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G3.3: Copy-Never-Link Verification
- [ ] VQ-005 executed
- [ ] No master mutation from runtime operations
- [ ] Copy-never-link principle maintained
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-005.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

**G3 Overall Status:** ⬜ PASS / ⬜ FAIL

**If FAIL:** Apply P3 (Copy-Never-Link Enforcement Guard).

---

## G4: Master→Instance Mapping Verification

### G4.1: L0 Mapping (Panel Master → Proposal Panel)
- [ ] Proposal Panels correctly reference Panel Master definitions
- [ ] Panel type consistency verified
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G4.2: L1 Mapping (Feeder Master → Feeder Instance)
- [ ] VQ-002 executed (already covered in G1.3)
- [ ] Feeder Instances correctly reference Feeder Masters via `MasterBomId`
- [ ] One Feeder Master → Many Feeder Instances relationship verified
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G4.3: L2 Mapping (BOM Master → Proposal BOM)
- [ ] VQ-004 executed
- [ ] Proposal BOMs correctly reference BOM Masters
- [ ] No orphan Proposal BOMs
- [ ] Evidence captured: `evidence/fundamentals/execution_window_YYYYMMDD/verification/VQ-004.txt`

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G4.4: L2 Items Mapping (Item Master → Proposal BOM Item)
- [ ] Proposal BOM Items correctly reference Item Master (ProductType=2)
- [ ] Item resolution verified
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

### G4.5: Root Mapping (Proposal BOM Master)
- [ ] VQ-003 executed (already covered in G2.1)
- [ ] All runtime entities have valid `QuotationId` root reference
- [ ] Ownership graph complete
- [ ] Evidence captured

**Gate Status:** ⬜ PASS / ⬜ FAIL

**G4 Overall Status:** ⬜ PASS / ⬜ FAIL

**If FAIL:** Consider P2 (Quotation Ownership Enforcement) or P4 (Legacy Data Normalization).

---

## Overall Verification Summary

**Execution Date:** _______________  
**Executed By:** _______________  

| Gate | Status | Evidence Location | Notes |
|------|--------|-------------------|-------|
| G1 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| G2 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| G3 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |
| G4 | ⬜ PASS / ⬜ FAIL | _______________ | _______________ |

**Overall Status:** ⬜ ALL GATES PASS / ⬜ GATE FAILURES DETECTED

**Patch Decision:**
- ⬜ NO PATCHES REQUIRED (all gates pass)
- ⬜ PATCHES REQUIRED (see PATCH_REGISTER.md for applied patches)

**Final Sign-Off:**
- ⬜ PASS (no patches)
- ⬜ PASS WITH PATCHES (patches applied and verified)
- ⬜ FAIL (rollback required)

**Signed By:** _______________  
**Date:** _______________

---

## Conditional Patch Governance (Reference)

This document is governed by:
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md`
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md`

Patches are **conditional** and may be applied only if verification fails (G1-G4).
Any applied patch must be logged in PATCH_REGISTER with evidence.

---

**END OF FUNDAMENTALS VERIFICATION CHECKLIST**

