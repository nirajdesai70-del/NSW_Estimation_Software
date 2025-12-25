# Fundamentals v2.0 — Phase 5 Gap Analysis & Correction Plan

**Version:** 1.0  
**Date:** 2025-01-XX  
**Status:** EVALUATION & PROPOSED PLAN (No Implementation Yet)  
**Purpose:** Identify gaps between Fundamentals v2.0 and Phase 4/5 work, propose corrections for Phase 5

---

## Executive Summary

This document identifies gaps between the Fundamentals v2.0 master doctrine and Phase 4/5 planning work, proposes corrections that must be handled in Phase 5, and ensures no conflicts with Phase 4 closure.

**Key Finding:** ✅ No conflicts with Phase-4 work. Fundamentals v2.0 defines future canonical semantics (Phase 5), while Phase 4 focused on transport/stability (Legacy). Clear separation maintained.

---

## 1. Boundary Analysis: Fundamentals v2.0 vs Phase 4/5

### 1.1 Two Truth Layers (Confirmed Alignment)

**Phase 4 Scope (Legacy Stabilization):**
- Transport layer standardization (SHARED endpoints)
- Legacy payloads preserved (COMPAT endpoints)
- Contract-first approach for stability
- No semantic redefinition

**Fundamentals v2.0 Scope (NSW Canonical Semantics):**
- Category/SubCategory/Item/ProductType definitions
- L0/L1/L2 resolution model
- SKU explosion logic
- Price ownership rules
- Feature lines standard

**✅ Separation Confirmed:**
- Phase 4 = transport + stability (no meaning change)
- Phase 5 = semantics + canonical dictionary (meaning redefined)
- Fundamentals v2.0 does not conflict because Phase 4 didn't redefine meaning

**Reference:** `docs/PHASE_5/LEGACY_VS_NSW_COEXISTENCE_POLICY.md`

---

## 2. Identified Gaps & Corrections Required

### Gap 1: SubCategory Multiplicity vs Legacy DB Reality

**Issue:**
Fundamentals v2.0 states: "SubCategories are additive (a product can have multiple SubCategories at the same time)."

Legacy DB likely stores single `SubCategoryId` on Product table, not multiple.

**Impact:**
- Phase 5 schema design needs to support multi-SubCategory via junction table
- Legacy mapping cannot assume 1:1 relationship
- Documentation needs to clarify: canonical intent vs legacy constraint

**Correction Required:**
- ✅ Add schema note in Fundamentals v2.0 (Section E.4)
- ✅ Document junction table intent for Phase 5 schema design
- ✅ Clarify legacy vs NSW separation

**Phase 5 Action:**
- Design `l1_subcategory_selections` junction table in canonical schema
- Define migration mapping rules (if legacy mapping ever needed)

---

### Gap 2: Category vs Item/ProductType Naming Confusion

**Issue:**
Fundamentals v2.0 correctly states Category ≠ Item, but examples use "Category: ACB" which can cause confusion (since ACB is actually an Item, not a business Category).

**Impact:**
- Teams may conflate legacy naming with NSW canonical structure
- Examples could be misinterpreted as NSW structure

**Correction Required:**
- ✅ Clarify in examples (Section D.3)
- ✅ Add note: "In legacy DB, Category name may equal Item name. In NSW, Category must be business grouping (e.g., Protection Devices), Item is ACB."

**Phase 5 Action:**
- Data Dictionary must explicitly define Category as business grouping only
- Examples must use correct NSW structure (Category=Protection Devices, Item=ACB)

---

### Gap 3: Accessory SKU Handling Rule Incomplete

**Issue:**
Fundamentals v2.0 forbids accessories (Shunt, Aux, OLR, etc.) becoming Item/ProductType, but doesn't clarify: what if accessory is a standalone priced SKU?

**Impact:**
- Ambiguity: standalone accessory SKUs need clear handling path
- Risk of creating new Item/ProductType incorrectly

**Correction Required:**
- ✅ Add rule in Section F
- ✅ Clarify: Standalone priced accessory SKUs become Feature L1 line + L2 SKU, NOT new Item/ProductType

**Phase 5 Action:**
- Data Dictionary must include accessory handling rules
- Schema design must support Feature→SKU mapping for accessories

---

### Gap 4: Feature Lines vs SubCategory vs Attribute Bridge Missing

**Issue:**
Fundamentals v2.0 has:
- Section S: SubCategory vs Attribute Doctrine
- Section V: L1 Feature Lines Standard

But no clear guidance on when SubCategory selection becomes a Feature line vs stays on BASE line.

**Impact:**
- Developers won't know when to use Feature lines vs SubCategory selection
- Inconsistent implementation risk

**Correction Required:**
- ✅ Add bridge section (Section V.4)
- ✅ Clarify: Feature lines are UI-visible intent record; SubCategory selection can remain on BASE or become FEATURE line (recommended when it affects SKU explosion)

**Phase 5 Action:**
- Data Dictionary must define Feature line creation rules
- Schema design must support both patterns
- Service specs must clarify Feature line generation logic

---

### Gap 5: Import SOP Missing Governance Roles

**Issue:**
Section M (Import SOP) says "link to Generic via manual/guided mapping" but doesn't specify who approves mapping.

**Impact:**
- Conflicts with ADR-005 (Master Data Governance Firewall)
- No clear approval workflow
- Risk of unauthorized master creation

**Correction Required:**
- ✅ Add governance section (Section M.5)
- ✅ Clarify: Mapping is governed by Engineering/Admin role only
- ✅ No runtime auto-create mapping during quotation usage (tie to ADR-005 firewall)

**Phase 5 Action:**
- Import governance must align with ADR-005
- Service specs must enforce role-based approval
- Schema must support approval queue tables

---

### Gap 6: Legacy vs NSW Semantic Boundary Note Missing

**Issue:**
Fundamentals v2.0 doesn't explicitly state that it defines NSW canonical semantics, not legacy semantics.

**Impact:**
- Risk of applying NSW rules to legacy system
- Confusion about when rules apply

**Correction Required:**
- ✅ Add boundary note at beginning (Section A.1)
- ✅ Clarify: This document defines NSW canonical semantics for Phase 5, not legacy semantics

**Phase 5 Action:**
- All Phase 5 documentation must explicitly reference NSW canonical model
- Mapping to legacy (if ever needed) must be separate project

---

### Gap 7: Governance Roles Not Documented

**Issue:**
Fundamentals v2.0 doesn't specify who can create what (Category/SubCategory/Item/Generic L1/SKU prices).

**Impact:**
- No RBAC guidance for Phase 5 design
- Unclear ownership and approval workflows

**Correction Required:**
- ✅ Add governance roles section (New Section: Use & Governance)
- ✅ Define: Who can create Category/SubCategory/Item (Admin only), Generic L1 (Engineering), SKU prices (Procurement/Admin), etc.

**Phase 5 Action:**
- RBAC design must enforce role-based creation
- Service contracts must include role validation
- Schema must support audit trails

---

## 3. Correction Plan for Phase 5

### Priority 1: Essential Corrections (Must Fix Before Freeze)

1. **Legacy vs NSW Boundary Note** (Section A.1)
   - Add explicit note that this is NSW canonical, not legacy
   - Clarify Phase 5 applicability

2. **SubCategory Schema Note** (Section E.4)
   - Document multi-SubCategory junction table intent
   - Clarify legacy vs NSW separation

3. **Accessory SKU Rule** (Section F.2)
   - Add standalone accessory SKU handling rule
   - Clarify Feature line + L2 SKU pattern

4. **Feature/SubCategory Bridge** (Section V.4)
   - Add guidance on when to use Feature lines vs SubCategory selection
   - Document SKU explosion impact

5. **Import Governance** (Section M.5)
   - Add role-based approval requirements
   - Tie to ADR-005 firewall

6. **Governance Roles** (New Section: Use & Governance)
   - Define who can create what
   - Document approval workflows

### Priority 2: Phase 5 Implementation Alignment

1. **Data Dictionary Alignment**
   - Ensure all Fundamentals v2.0 rules translate to Data Dictionary
   - Cross-reference Fundamentals sections in Dictionary

2. **Schema Design Alignment**
   - Junction tables for multi-SubCategory
   - Feature line support (l1_group_id, l1_line_type, etc.)
   - Approval queue tables (per ADR-005)

3. **Service Spec Alignment**
   - L2 explosion service must match pseudocode (Section Z.2)
   - Import services must enforce ADR-005 firewall
   - Feature line generation must follow Section V rules

---

## 4. Phase 5 Execution Plan

### Step 1: Apply Corrections to Fundamentals v2.0

**Action:** Insert 5 corrections into master document
- Legacy vs NSW boundary note
- Multi-SubCategory schema note
- Accessory SKU rule
- Feature/SubCategory bridge
- Import governance roles
- Governance roles section

**Status:** 📋 Proposed (awaiting review)

### Step 2: Freeze Fundamentals v2.0

**Prerequisite:** All corrections applied and reviewed

**Action:** Declare "Freeze Master Doctrine v2.0"

**Status:** 📋 Pending

### Step 3: Create Phase 5 Data Dictionary

**Reference:** Fundamentals v2.0 (all sections)

**Output:** `NSW_DATA_DICTIONARY_v1.0.md`

**Must Include:**
- All entity definitions from Fundamentals
- All rules and constraints
- All governance requirements
- Cross-references to Fundamentals sections

**Status:** 📋 Planned

### Step 4: Design Phase 5 Canonical Schema

**Reference:** Fundamentals v2.0 (Excel layout + schema notes)

**Output:** `NSW_SCHEMA_CANON_v1.0.md` + ERD

**Must Include:**
- Tables matching Excel layout (GENERIC_MASTER, GENERIC_ATTRIBUTES, etc.)
- Junction tables (multi-SubCategory, etc.)
- Approval queue tables (ADR-005)
- All constraints and relationships

**Status:** 📋 Planned

### Step 5: Define Service Specifications

**Reference:** Fundamentals v2.0 (Section Z.2: L2 Explosion Pseudocode)

**Output:** Service specifications for:
- L2 Explosion Service
- Import Services (with ADR-005 enforcement)
- Feature Line Generation Service
- Master Data Creation Services (role-based)

**Status:** 📋 Planned

---

## 5. Risk Mitigation

### Risk 1: Applying NSW Rules to Legacy

**Mitigation:**
- Explicit boundary note in Fundamentals
- Phase 5 scope explicitly excludes legacy
- Coexistence policy already established

### Risk 2: Schema Design Mismatch

**Mitigation:**
- Fundamentals v2.0 Excel layout provides exact structure
- Schema design must match Excel layout exactly
- Junction tables explicitly documented

### Risk 3: Import Governance Violation

**Mitigation:**
- ADR-005 already defines firewall rules
- Fundamentals must reference ADR-005
- Service specs must enforce ADR-005

### Risk 4: Feature Line Confusion

**Mitigation:**
- Bridge section clarifies when to use Feature lines
- Examples show BASE + FEATURE pattern
- Pseudocode shows exact logic

---

## 6. Dependencies & Constraints

### Phase 4 Dependencies

✅ **None** — Phase 4 complete, no blockers

### Phase 5 Prerequisites

✅ **All Met:**
- Phase 4 complete
- Fundamentals v2.0 ready for corrections
- ADR-005 approved
- Coexistence policy established

### External Constraints

- ADR-005: Master Data Governance Firewall (must align)
- Phase 5 Scope Fence: Analysis-only, no implementation
- Legacy vs NSW Boundary: Must maintain separation

---

## 7. Success Criteria

Phase 5 Gap Correction is complete when:

1. ✅ All 6 gaps corrected in Fundamentals v2.0
2. ✅ Fundamentals v2.0 frozen and approved
3. ✅ Data Dictionary references Fundamentals correctly
4. ✅ Schema design matches Fundamentals Excel layout
5. ✅ Service specs align with Fundamentals pseudocode
6. ✅ Governance roles documented and aligned with ADR-005

---

## 8. Next Steps

1. **Review this gap analysis** (current step)
2. **Apply 5 corrections to Fundamentals v2.0** (proposed)
3. **Review corrected Fundamentals v2.0**
4. **Freeze Master Doctrine v2.0**
5. **Proceed with Phase 5 Data Dictionary**

---

**Document Status:** 📋 EVALUATION & PROPOSED PLAN  
**Next Action:** Apply corrections to Fundamentals v2.0  
**Owner:** Phase 5 Governance Team

