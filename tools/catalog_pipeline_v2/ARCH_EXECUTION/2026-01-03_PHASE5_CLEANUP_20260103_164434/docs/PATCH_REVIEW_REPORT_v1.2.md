# Patch Review Report - v1.2 Changes

**Date:** 2025-01-XX  
**Status:** REVIEW ONLY - NO EXECUTION YET  
**Purpose:** Comprehensive analysis of required changes, conflicts, and gaps before implementation

---

## Executive Summary

This report analyzes patch notes for v1.2 updates to:
1. `NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md`
2. `NSW_SHEET_SET_INDEX_v1.md`
3. `migrate_sku_price_pack.py` (Script A)
4. Additional clarifications and operating reality documentation

**Critical Finding:** There is a **fundamental semantic conflict** between current freeze document and patch requirements regarding SC_Lx vs Capability separation.

---

## 1. CRITICAL CONFLICTS IDENTIFIED

### 1.1 SC_Lx vs Capability Semantic Conflict (HIGHEST PRIORITY)

**Current State (v1):**
- Line 62: `SC_L1…SC_L4` → `Capability_Class_1…4` (Capability grouping axes)
- Line 182-185: Contactor example shows `Capability_Class_2: AC Coil`, `Capability_Class_3: AC1 / AC3`
- Lines 45-58 in script: Auto-maps `SC_Lx` → `capability_class_x`

**Patch Requirement (v1.2):**
- SC_Lx = **Structural / Construction Layers (SCL)** ONLY
- SC_Lx describes physical construction (Frame, Poles, Actuation, Mounting, Terminals, Zones, Enclosure, Variants)
- SC_Lx MUST NOT be used for options, features, or capabilities
- Capability is a **separate concept** using `capability_codes` and optional `capability_class_1…4`

**Conflict Severity:** 🔴 **CRITICAL - SEMANTIC REVERSAL**

**Impact:**
- Current freeze document incorrectly treats SC_Lx as capability grouping
- Script A incorrectly auto-maps SC_Lx to capability_class_x
- Contactor example contradicts Option B (coil at L2, not L1)
- This affects all future catalog work

**Resolution Required:**
- Complete rewrite of SC_Lx definition section
- Remove auto-mapping from script
- Fix Contactor example to align with Option B
- Add explicit "Structural vs Capability Separation" section

---

### 1.2 Contactor Example Contradiction

**Current State (v1):**
- Lines 182-185: Shows `Capability_Class_2: AC Coil`, `Capability_Class_3: AC1 / AC3`

**Patch Requirement:**
- Option B: Coil voltage is SKU-defining and kept at L2, not part of L1 generic identity
- AC1/AC3 are rating contexts (L1 spec / SKU_RATINGS), not capability class
- Coil voltage should NOT appear in Capability_Class fields

**Conflict Severity:** 🔴 **CRITICAL - DOCTRINE VIOLATION**

**Resolution Required:**
- Rewrite Contactor example completely
- Remove coil voltage from Capability_Class examples
- Clarify AC1/AC3 as ratings, not capability

---

### 1.3 Generic Naming Rule Missing

**Current State (v1):**
- No explicit rule about vendor/series neutrality in generic names

**Patch Requirement:**
- Generic names must be vendor- and series-neutral
- Do NOT include OEM name (Schneider), Series (LC1E), Family (GZ1E, NSX, NW)
- Make/Series allowed only at L2 (SKU level)

**Conflict Severity:** 🟡 **MEDIUM - MISSING GUARDRAIL**

**Resolution Required:**
- Add "Generic Naming Neutrality" section
- Add validation warning in script

---

## 2. REQUIRED CHANGES BY DOCUMENT

### 2.1 NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md

#### Change A1: Add "Engineering Bank Operating Reality" Section (NEW)

**Location:** Add as Section 0 (before Section 1)

**Content Required:**
- Structural vs Capability vs Attribute separation
- Generic naming neutrality rule
- Layer discipline (L1 = facts only, L2 = rules)
- Sheet semantics (Engineering Bank canonical meanings)
- AI safety boundary

**Status:** ⚠️ **NEW SECTION - MUST ADD**

---

#### Change A2: Fix SC_Lx Definition (CRITICAL REWRITE)

**Current Location:** Section 2, World C, Lines 59-69

**Current Text:**
```
SC_L1…SC_L4 | Capability_Class_1…4 | Capability grouping axes
```

**Required Replacement:**
- Add new section: "Structural vs Capability Separation (MANDATORY)"
- SC_Lx = Structural / Construction Layers (SCL) ONLY
- Explicit list of what SC_Lx represents (Frame, Poles, Actuation, Mounting, Terminals, Zones, Enclosure, Variants)
- Explicit list of what SC_Lx MUST NOT represent (options, features, capabilities, business grouping)
- Capability is separate concept using `capability_codes` and optional `capability_class_1…4`
- SC_Lx and capability_class_x are distinct and must not be merged

**Status:** 🔴 **CRITICAL - SEMANTIC CORRECTION**

---

#### Change A3: Add "Do Not Force Fill" Rule

**Location:** Add under Section 3 (Level definitions) or new rules section

**Content Required:**
- Universal Population Rule for SC_Lx and ATTR_*
- Populate only if explicitly defined in OEM catalog
- Do NOT substitute series, family, or marketing names
- Do NOT guess or infer
- Leave blank if not explicitly stated
- Applies across all product types

**Status:** 🟡 **NEW RULE - MUST ADD**

---

#### Change A4: Add Generic Naming Rule

**Location:** Add as new section or under Section 4 (Naming conventions)

**Content Required:**
- Generic names must be vendor- and series-neutral
- Do NOT include: OEM name, Series, Family
- Make/Series allowed only at L2 (SKU level)
- Examples of correct vs incorrect

**Status:** 🟡 **NEW RULE - MUST ADD**

---

#### Change A5: Fix Contactor Example

**Current Location:** Section 6, Lines 172-185

**Current Text:**
```
- Capability_Class_2: AC Coil
- Capability_Class_3: AC1 / AC3
```

**Required Replacement:**
- Remove coil voltage from Capability_Class examples
- Add: "Coil voltage: L2 only (SKU differentiator)"
- Add: "AC1/AC3: rating context (L1 spec / SKU_RATINGS), not capability"
- Update Capability examples to show: WITH_OLR; AUX_CONTACT
- Update Capability_Class examples to show construction/operation/functional/accessory classes (if needed)

**Status:** 🔴 **CRITICAL - EXAMPLE CORRECTION**

---

#### Change A6: Fix business_subcategory Statement

**Current Location:** Section 2, World A, Line 34

**Current Text:**
```
Current Code Usage: ✅ business_subcategory already used in codebase (aligned!)
```

**Required Replacement:**
```
Current Code Usage: ✅ business_subcategory exists in codebase and is treated as legacy alias for business_segment during transition. This prevents future teams from thinking "SubCategory is the right word".
```

**Status:** 🟡 **CLARIFICATION - MUST UPDATE**

---

#### Change A7: Add "Two-Worlds" Warning Block

**Location:** Add after World A + World C sections (after Section 2)

**Content Required:**
- Hard rule: Business Category/Segment and Engineering Capability/Class are different axes
- Forbidden: mapping between them without explicit mapping artifact
- Reference to BUSINESS_TAXONOMY_TO_ENGINEERING_CAPABILITY_MAP.md (if exists)

**Status:** 🟡 **NEW WARNING - MUST ADD**

---

#### Change A8: Explicitly Separate "Capability" vs "Feature Line"

**Location:** Add paragraph in Section 2, World C

**Content Required:**
- Capability = inclusion/exclusion flag set (multi-select)
- Feature Line = separate L1 line only when it can affect L2 explosion or vendor variability
- Aligns with Doctrine sections T and V

**Status:** 🟡 **CLARIFICATION - MUST ADD**

---

#### Change A9: Tighten SC_Lx Rename Scope

**Current Location:** Section 4, Lines 124-125

**Current Text:**
```
- capability_class_1 … capability_class_4 (preferred)
- SC_L1 … SC_L4 (legacy, supported during transition)
```

**Required Addition:**
- In transitional phase, data model remains SC_L1–SC_L4 in storage where required
- capability_class_x may be used as UI/documentation alias
- Avoid breaking migrations
- Matches "193 usages" reality and keeps it implementation-safe

**Status:** 🟡 **CLARIFICATION - MUST ADD**

---

#### Change A10: Add "Business Segment vs Item/ProductType Name Collision" Section

**Location:** Add as new section or under Section 2

**Content Required:**
- Name overlap is allowed (e.g., Business Segment = Contactor, Item/ProductType = Contactor)
- Business Segment is classification; Item/ProductType is engineering identity
- Never infer mapping based on identical text labels

**Status:** 🟡 **NEW SECTION - MUST ADD**

---

### 2.2 NSW_SHEET_SET_INDEX_v1.md

#### Change B1: Add Engineering Bank Mapping Table

**Location:** Add as new section (e.g., Section 2.5 or new Section 3.6)

**Content Required:**
- Mapping table:
  - Cursor/Pipeline Sheet → Engineering Bank Sheet
  - NSW_SKU_MASTER_CANONICAL → DATA_SKU_PRICE_LIST
  - NSW_ACCESSORY_SKU_MASTER → DATA_ACCESSORY_PRICE_LIST
  - NSW_CATALOG_CHAIN_MASTER → DATA_ITEM_MASTER (Layer-1 minimal intent)
  - NSW_PRICE_MATRIX_CANONICAL → PRICE_MATRIX (separate commercial layer)
- Note: Engineering Bank naming is authoritative for AI-assisted catalog work

**Status:** 🟡 **NEW MAPPING - MUST ADD**

---

#### Change B2: Clarify Catalog Chain vs L1 Parse Sheets

**Current Location:** Section 3.2, Lines 78-81, and Section 5, Line 168

**Current Text:**
```
⚠️ NSW_L1_CONFIG_LINES - Currently generated, but different concept
⚠️ NSW_CATALOG_CHAIN_MASTER - Not yet generated (recommended new sheet)
...
Decision Required: Clarify relationship between NSW_L1_CONFIG_LINES and NSW_CATALOG_CHAIN_MASTER.
```

**Required Replacement:**
- Decision CLOSED: NSW_CATALOG_CHAIN_MASTER is canonical for continuity
- NSW_L1_CONFIG_LINES is legacy parse output and becomes archive-ready after chain verification QC
- NSW_L1_CONFIG_LINES is a parsing artifact (duty×voltage expansion)
- NSW_CATALOG_CHAIN_MASTER is the canonical L0/L1/L2 continuity sheet

**Status:** 🟡 **DECISION CLOSURE - MUST UPDATE**

---

#### Change B3: Update NSW_L2_PRODUCTS Status

**Current Location:** Section 3.1, Line 41, and Section 5, Line 154

**Current Text:**
```
NSW_L2_PRODUCTS | ACTIVE | ... | NSW_L2_PRODUCTS
...
NSW_L2_PRODUCTS (if superseded) | LEGACY | SKU list migrated to SKU Master
```

**Required Replacement:**
- NSW_L2_PRODUCTS = legacy alias/compat export, not the master
- Authoritative SKU list is NSW_SKU_MASTER_CANONICAL
- Update "Current Name in Code" column to reflect legacy status

**Status:** 🟡 **STATUS CLARIFICATION - MUST UPDATE**

---

#### Change B4: Update "Not Yet Generated" Statements

**Current Location:** Multiple sections (3.4, 3.5, Section 4)

**Current Text:**
```
❌ NSW_SKU_RATINGS - Not yet generated (recommended addition)
❌ Dictionary sheets not yet generated (recommended addition)
```

**Required Replacement:**
- Update to: "Generated and active" or "Reference-active" or "Locked"
- Per ARCHIVE_AND_MIGRATION_PLAN_v1.1.md, these are already generated

**Status:** 🟡 **STATUS UPDATE - MUST FIX**

---

#### Change B5: Add Alias Support Block

**Location:** Add as new section or under Section 2 (Terminology Reminder)

**Content Required:**
- Alias support during transition:
  - business_subcategory is a legacy alias for business_segment
  - SC_L1..SC_L4 are legacy aliases for capability_class_1..4
- Keeps two freeze docs consistent

**Status:** 🟡 **ALIGNMENT - MUST ADD**

---

### 2.3 migrate_sku_price_pack.py (Script A)

#### Change C1: Remove Forced SC → Capability Mapping (CRITICAL)

**Current Location:** Lines 44-58

**Current Code:**
```python
sc_mappings = {
    'SC_L1': 'capability_class_1',
    'SC_L2': 'capability_class_2',
    'SC_L3': 'capability_class_3',
    'SC_L4': 'capability_class_4',
    ...
}
```

**Required Replacement:**
- Remove auto-mapping of SC_Lx to capability_class_x
- Add comment: "SC_Lx are preserved as SCL (Structural Construction Layer)"
- Add comment: "Capability mapping must be explicit and source-driven"
- Add comment: "Do NOT auto-map SC_Lx to capability_class_x"
- Only rename if source column explicitly indicates capability
- Keep business_subcategory → business_segment mapping

**Status:** 🔴 **CRITICAL - LOGIC REMOVAL**

---

#### Change C2: Add Generic Naming Validation

**Location:** Add new function and call after migration

**Content Required:**
- Function: `check_generic_name_neutrality(df)`
- Check for forbidden tokens: ['schneider', 'abb', 'siemens', 'lc1', 'gz1', 'nsx', 'nw']
- Check columns: ['generic_item_name', 'generic_item_description']
- Warning only (non-blocking)
- Print warnings if found

**Status:** 🟡 **NEW VALIDATION - MUST ADD**

---

## 3. GAPS IDENTIFIED

### 3.1 Missing Documentation

1. **Engineering Bank Operating Reality Section**
   - Not present in any freeze document
   - Required as authoritative override for ambiguous interpretations
   - Should be Section 0 in Terminology Freeze doc

2. **Layer Separation Document**
   - Price List vs Engineering BOM separation discussed but not formalized
   - Should be separate document or major section

3. **Voltage Handling Clarification**
   - Contactor coil voltage (attribute) vs MCCB/ACB MX/MN voltage (accessory attribute)
   - Discussed but not documented in freeze docs

4. **AI Safety Boundary**
   - Mentioned in patch notes but not in current freeze docs
   - Should be in Engineering Bank Operating Reality section

### 3.2 Missing Validation Rules

1. **Generic Naming Validation**
   - Not implemented in script
   - Should be warning-only check

2. **SC_Lx Population Validation**
   - No check for forced population
   - Should validate "only populate if explicitly defined"

### 3.3 Missing Cross-References

1. **Engineering Bank Sheet Mapping**
   - No mapping table between Cursor pipeline sheets and Engineering Bank sheets
   - Should be in Sheet Set Index

2. **Document Dependencies**
   - No clear statement of which documents override which
   - Engineering Bank Operating Reality should be highest priority

---

## 4. DEPENDENCIES AND EXECUTION ORDER

### 4.1 Critical Path (Must Do First)

1. **Fix SC_Lx Definition** (Change A2)
   - Blocks all other changes
   - Must be done before script changes
   - Affects all future catalog work

2. **Remove SC_Lx Auto-Mapping from Script** (Change C1)
   - Depends on Change A2
   - Prevents incorrect data migration

3. **Fix Contactor Example** (Change A5)
   - Depends on Change A2
   - Prevents confusion in future work

### 4.2 High Priority (Do Next)

4. **Add Engineering Bank Operating Reality** (Change A1)
   - Provides authoritative context for all other changes
   - Should be done early

5. **Update business_subcategory Statement** (Change A6)
   - Clarifies legacy alias status
   - Prevents future confusion

6. **Add Generic Naming Rule** (Change A4)
   - Prevents data quality issues
   - Add validation in script (Change C2)

### 4.3 Medium Priority (Can Do in Parallel)

7. **Add "Do Not Force Fill" Rule** (Change A3)
8. **Add "Two-Worlds" Warning** (Change A7)
9. **Separate Capability vs Feature Line** (Change A8)
10. **Tighten SC_Lx Rename Scope** (Change A9)
11. **Add Name Collision Section** (Change A10)
12. **Add Engineering Bank Mapping** (Change B1)
13. **Clarify Catalog Chain** (Change B2)
14. **Update Sheet Statuses** (Change B3, B4)
15. **Add Alias Support Block** (Change B5)

---

## 5. CONFLICT RESOLUTION STRATEGY

### 5.1 SC_Lx Semantic Conflict

**Resolution Approach:**
1. Accept patch requirement as correct (SC_Lx = SCL, not capability)
2. Document this as a correction to v1, not a new interpretation
3. Update all references consistently
4. Remove auto-mapping from script immediately

**Rationale:**
- Patch aligns with Engineering Bank reality
- Current v1 definition contradicts Option B and doctrine
- Correction prevents future errors

### 5.2 Contactor Example Conflict

**Resolution Approach:**
1. Rewrite example to align with Option B
2. Remove coil voltage from Capability_Class
3. Clarify AC1/AC3 as ratings
4. Update capability examples to show actual capabilities

**Rationale:**
- Example must match doctrine
- Option B is locked decision
- Prevents confusion in future work

---

## 6. RISK ASSESSMENT

### 6.1 High Risk Changes

1. **SC_Lx Definition Change**
   - Risk: Breaking existing code that assumes SC_Lx = capability
   - Mitigation: Phased approach, support both during transition
   - Impact: All catalog work going forward

2. **Script Auto-Mapping Removal**
   - Risk: Data migration may miss capability data
   - Mitigation: Explicit capability column detection
   - Impact: Migration accuracy

### 6.2 Medium Risk Changes

3. **Generic Naming Validation**
   - Risk: False positives on valid generic names
   - Mitigation: Warning-only, not blocking
   - Impact: Data quality improvement

4. **Sheet Status Updates**
   - Risk: Confusion about which sheets are authoritative
   - Mitigation: Clear documentation
   - Impact: Workflow clarity

---

## 7. RECOMMENDED EXECUTION PLAN

### Phase 1: Critical Fixes (Do First)

1. ✅ Add Engineering Bank Operating Reality section (Section 0)
2. ✅ Fix SC_Lx definition (Section 2, World C)
3. ✅ Remove SC_Lx auto-mapping from script
4. ✅ Fix Contactor example
5. ✅ Update business_subcategory statement

### Phase 2: Important Additions

6. ✅ Add Generic Naming Rule
7. ✅ Add Generic Naming Validation to script
8. ✅ Add "Do Not Force Fill" Rule
9. ✅ Add "Two-Worlds" Warning
10. ✅ Add Engineering Bank Mapping table

### Phase 3: Clarifications and Updates

11. ✅ Separate Capability vs Feature Line
12. ✅ Tighten SC_Lx Rename Scope
13. ✅ Add Name Collision Section
14. ✅ Clarify Catalog Chain decision
15. ✅ Update sheet statuses
16. ✅ Add Alias Support Block

### Phase 4: Validation and Testing

17. ✅ Test script changes on sample data
18. ✅ Validate all examples in freeze docs
19. ✅ Cross-check all cross-references
20. ✅ Final review before freeze

---

## 8. ACCEPTANCE CRITERIA

Before marking v1.2 as complete:

- [ ] All critical conflicts resolved
- [ ] SC_Lx correctly defined as SCL (not capability)
- [ ] Script does not auto-map SC_Lx to capability_class_x
- [ ] Contactor example aligns with Option B
- [ ] Engineering Bank Operating Reality section added
- [ ] Generic naming rule and validation added
- [ ] All sheet statuses updated accurately
- [ ] All cross-references verified
- [ ] No contradictions between documents
- [ ] Script tested on sample data

---

## 9. OPEN QUESTIONS

1. **Capability Class Fields:**
   - If SC_Lx are SCL, what should capability_class_1..4 represent?
   - Are they still needed, or should we use only capability_codes?

2. **Migration Strategy:**
   - How to handle existing data that has SC_Lx populated as capabilities?
   - Should we create a migration script to separate SCL from capability?

3. **Document Versioning:**
   - Should this be v1.2 or v2.0 (given semantic reversal)?
   - How to handle version history?

4. **Engineering Bank Integration:**
   - How detailed should the Engineering Bank mapping be?
   - Should we create a separate mapping document?

---

## 10. NEXT STEPS

1. **Review this report** with stakeholders
2. **Resolve open questions** before execution
3. **Approve execution plan** and priorities
4. **Execute Phase 1** (Critical Fixes)
5. **Validate changes** before proceeding to Phase 2
6. **Complete all phases** systematically
7. **Final review** before freezing v1.2

---

**END OF REPORT**

**Status:** ⚠️ **REVIEW COMPLETE - AWAITING APPROVAL FOR EXECUTION**

