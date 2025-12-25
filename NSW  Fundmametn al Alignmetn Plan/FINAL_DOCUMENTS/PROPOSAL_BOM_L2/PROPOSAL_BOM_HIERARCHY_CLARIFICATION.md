# Proposal BOM Hierarchy Clarification (Code-Aligned)

**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_HIERARCHY_CLARIFICATION_v1.0_2025-12-19.md  
**Version:** v1.0_2025-12-19  
**Date:** 2025-12-19  
**Status:** ✅ FROZEN (Phase-5 PB-GAP-003 Closure)  
**Purpose:** Clarifies Proposal BOM hierarchy definitions to align with code-truth, resolving spec contradiction identified in PB-GAP-003.

---

## ⚠️ CRITICAL: This Document Resolves PB-GAP-003

This document provides the authoritative definition of Proposal BOM hierarchy levels, aligned with actual code implementation. This resolves the spec contradiction identified in PB-GAP-003 where design documents suggested "BOM1 can be child of Panel" while code enforces "BOM1 must have ParentBomId pointing to Level 0 (Feeder)".

**Reference:** `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§3 PB-GAP-003`

---

## 1. Hierarchy Level Definitions (Code-Aligned)

### 1.1 Level 0 — Feeder

**Definition:**
- **Level = 0** AND **ParentBomId IS NULL**

**OR (Legacy Feeder Support):**
- **Level = 1** AND **ParentBomId IS NULL**

**Purpose:**
- Top-level container in Proposal BOM hierarchy
- Acts as root for quantity roll-up calculations
- Quantity chain logic walks up to Level 0 (or legacy Level 1 with no parent) to find feeder

**Code Evidence:**
- QuantityService treats Level 1 with no parent as feeder-equivalent (legacy support)
- Reference: `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-04`

**Rules:**
- ✅ Feeder must have no ParentBomId
- ✅ Legacy feeder (Level=1, ParentBomId=NULL) is supported for backward compatibility
- ✅ Quantity roll-up calculations use feeder as root

---

### 1.2 Level 1 — BOM1

**Definition:**
- **Level = 1** AND **ParentBomId points to Level 0 (Feeder)**

**Purpose:**
- First-level child BOM under Feeder
- Contains items/components that belong to the feeder assembly

**Rules:**
- ✅ BOM1 must have ParentBomId pointing to Level 0 (Feeder)
- ❌ BOM1 CANNOT be child of Panel (this was the spec contradiction)
- ❌ BOM1 CANNOT have ParentBomId pointing to another Level 1 BOM
- ✅ Exception: Legacy feeder case (Level=1, ParentBomId=NULL) is treated as feeder, not BOM1

**Clarification:**
- The design document statement "BOM1 = Child of Feeder or Panel" was incorrect
- Code implementation enforces: BOM1 must be child of Feeder only
- Legacy feeder (Level=1, ParentBomId=NULL) is NOT a BOM1; it is a feeder-equivalent

---

### 1.3 Level 2 — BOM2

**Definition:**
- **Level = 2** AND **ParentBomId points to Level 1 (BOM1)**

**Purpose:**
- Second-level child BOM under BOM1
- Contains sub-components of BOM1 items

**Rules:**
- ✅ BOM2 must have ParentBomId pointing to Level 1 (BOM1)
- ❌ BOM2 CANNOT have ParentBomId pointing to Level 0 (Feeder)
- ❌ No nesting beyond Level 2

---

## 2. Hierarchy Rules Summary

### 2.1 Valid Hierarchy Structures

```
Level 0 (Feeder) [ParentBomId = NULL]
    └─── Level 1 (BOM1) [ParentBomId = Feeder]
            └─── Level 2 (BOM2) [ParentBomId = BOM1]
```

**OR (Legacy Support):**

```
Level 1 (Legacy Feeder) [ParentBomId = NULL, treated as feeder-equivalent]
    └─── Level 1 (BOM1) [ParentBomId = Legacy Feeder]
            └─── Level 2 (BOM2) [ParentBomId = BOM1]
```

### 2.2 Invalid Hierarchy Structures (FORBIDDEN)

- ❌ Level 1 with ParentBomId pointing to Panel (not a valid parent)
- ❌ Level 1 with ParentBomId pointing to another Level 1 (must point to Level 0)
- ❌ Level 2 with ParentBomId pointing to Level 0 (must point to Level 1)
- ❌ Level 2 with ParentBomId pointing to another Level 2 (must point to Level 1)
- ❌ Any nesting beyond Level 2

---

## 3. Quantity Chain Logic

### 3.1 Feeder Discovery

Quantity chain logic walks up the BOM hierarchy to find the feeder (root):

1. **Standard Case:** Walk up to Level 0 (where ParentBomId IS NULL)
2. **Legacy Case:** If Level 1 with ParentBomId IS NULL, treat as feeder-equivalent

**Code Implementation:**
- QuantityService handles both standard and legacy feeder cases
- Reference: `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-04`

### 3.2 Roll-up Calculations

- ✅ SUM only at roll-up (no nested multiplication)
- ✅ Quantity chain correctly walks up to Level 0 (or legacy Level 1 with no parent)
- ✅ No double-multiplication in roll-ups

---

## 4. Validation Rules

### 4.1 Hierarchy Validation

When creating/updating Proposal BOM items:

1. **Level 0 (Feeder):**
   - ✅ Must have ParentBomId = NULL
   - ✅ Level must be 0 (or 1 for legacy feeder)

2. **Level 1 (BOM1):**
   - ✅ Must have ParentBomId pointing to Level 0 (Feeder)
   - ❌ Cannot have ParentBomId = NULL (unless it's a legacy feeder, which is not a BOM1)
   - ❌ Cannot have ParentBomId pointing to Panel or another Level 1

3. **Level 2 (BOM2):**
   - ✅ Must have ParentBomId pointing to Level 1 (BOM1)
   - ❌ Cannot have ParentBomId pointing to Level 0 or another Level 2

### 4.2 Database Integrity Checks

**DB Verification Queries:**

```sql
-- Verify Level 0 (Feeder) has no ParentBomId
SELECT * FROM quotation_sale_boms 
WHERE Level = 0 AND ParentBomId IS NOT NULL;

-- Verify Level 1 (BOM1) has ParentBomId pointing to Level 0
SELECT b1.* FROM quotation_sale_boms b1
LEFT JOIN quotation_sale_boms b2 ON b1.ParentBomId = b2.QuotationSaleBomId
WHERE b1.Level = 1 
AND (b1.ParentBomId IS NULL OR b2.Level != 0);

-- Verify Level 2 (BOM2) has ParentBomId pointing to Level 1
SELECT b1.* FROM quotation_sale_boms b1
LEFT JOIN quotation_sale_boms b2 ON b1.ParentBomId = b2.QuotationSaleBomId
WHERE b1.Level = 2 
AND (b1.ParentBomId IS NULL OR b2.Level != 1);
```

---

## 5. Spec Correction Summary

### 5.1 What Was Wrong

**Original Spec (Contradictory):**
- Part 3: "BOM1 = Child of Feeder or Panel" (allowed Level 1 attachment directly under panel)
- Part 5: "Level 1 must have ParentBomId pointing to Level 0" (required Level 0 parent)

**Contradiction:** These two statements cannot both be true.

### 5.2 Corrected Spec (Code-Aligned)

**Feeder Definition:**
- Level = 0 OR (Level = 1 AND ParentBomId IS NULL) (legacy feeder)

**BOM1 Definition:**
- Level = 1 AND ParentBomId points to Feeder (Level 0)

**Clarification:**
- ❌ BOM1 CANNOT be child of Panel
- ✅ BOM1 must be child of Feeder (Level 0) only
- ✅ Legacy feeder (Level=1, ParentBomId=NULL) is supported but is NOT a BOM1; it is feeder-equivalent

---

## 6. References

### 6.1 Related Documents

- `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:§3 PB-GAP-003` — Original gap identification
- `PROPOSAL_BOM_CODE_EVIDENCE_PACK_R1_v1.0_2025-12-19.md:CE-04` — Code evidence for legacy feeder support
- `NEPL_CANONICAL_RULES.md` — Canonical rules (L0/L1/L2 layer definitions)

### 6.2 Design Documents (External References)

**Note:** The following design documents are referenced in gap registers but are not present in this repository:
- `PROPOSAL_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md` — Referenced in PB-GAP-003
- `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — Referenced in PB-GAP-003

**Action Required:** If these design documents exist externally, they should be updated to match the hierarchy definitions in this document.

---

## 7. Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0_2025-12-19 | 2025-12-19 | Phase-5 PB-GAP-003: Initial hierarchy clarification document created. Defines Feeder, BOM1, BOM2 based on code-truth. Resolves spec contradiction. |

---

## 8. Closure Status

**PB-GAP-003 Status:** ✅ CLOSED (Doc-Aligned)

**Closure Evidence:**
- ✅ Hierarchy definitions clarified and aligned with code-truth
- ✅ Spec contradiction resolved (BOM1 cannot be child of Panel)
- ✅ Legacy feeder support documented
- ✅ Validation rules defined

**Next Steps:**
- Update gap register to mark PB-GAP-003 as CLOSED
- Reference this document in future Proposal BOM design work

---

**END OF DOCUMENT**

