# Phase 4 & 5 Folder Mapping Guide - Complete Navigation

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
This document provides complete mapping of all four key folders (Features, NSW Fundamental Alignment Plan, Planning, Project) to Phase 4 & 5 work, showing **WHERE** to go, **WHEN** to access, and **WHY** each folder is relevant.

## Source of Truth
- **Canonical:** This is the authoritative mapping guide for Phase 4 & 5 alignment
- **Fundamentals baseline:** See `FUNDAMENTALS_SOURCE_OF_TRUTH.md`
- **Fundamentals Alignment Plan register:** `01_REFERENCE/NSW_FUNDAMENTALS_ALIGNMENT_PLAN_REGISTER.md`

---

## 🗂️ Overview: Four Key Folders

| Folder | Purpose | Phase 4 Relevance | Phase 5 Relevance | Status |
|--------|---------|-------------------|-------------------|--------|
| **`features/`** | Feature documentation & design specs | ✅ Source for baseline requirements | ✅ Canonical data model source | ✅ Mapped |
| **`NSW Fundamental Alignment Plan/`** | Master alignment & fundamentals | ✅ Master plan reference | ✅ Design principles & standards | ✅ Mapped |
| **`PLANNING/`** | Execution planning & gap tracking | ✅ Gap execution instructions | ✅ Planning policies reference | ✅ Mapped |
| **`project/nish/`** | Legacy analysis work (read-only) | ✅ Legacy context | ✅ Reference only (not canonical) | ✅ Mapped |

---

## 📁 Folder 1: `features/` - Feature Documentation

### **WHERE** to Go

```
features/
├── component_item_master/     # PRIMARY: Canonical data model
│   ├── _general/
│   │   └── ITEM_MASTER_DETAILED_DESIGN.md  ⭐ CANONICAL MODEL
│   ├── import_export/
│   │   └── guides/22_DATA_IMPORT_FLOW.md   ⭐ Import templates
│   └── README.md
├── master_bom/                # Master BOM specifications
├── proposal_bom/              # Proposal BOM specifications
├── quotation/                 # Quotation specifications
├── project/                   # Project specifications
├── feeder_library/            # Feeder library specifications
├── master/                    # Master data specifications
├── employee/                  # Employee/role specifications
└── FEATURE_INDEX.md           # Complete feature index
```

### **WHEN** to Access

| Phase | Step | When | Files to Access |
|-------|------|------|-----------------|
| **Phase 4** | All steps | When understanding feature requirements | `features/*/README.md` |
| **Phase 5** | **Step 1: Data Dictionary** | **Primary source for canonical data model** | `features/component_item_master/_general/ITEM_MASTER_DETAILED_DESIGN.md` |
| **Phase 5** | **Step 1: Data Dictionary** | When defining import rules | `features/component_item_master/import_export/guides/*.md` |
| **Phase 5** | **Step 2: Schema Design** | When validating schema against requirements | All feature READMEs |
| **Post-Phase 5** | Implementation | When building feature modules | Feature-specific folders |

### **WHY** It's Relevant

1. **Canonical Data Model Source** ⭐
   - **File:** `features/component_item_master/_general/ITEM_MASTER_DETAILED_DESIGN.md`
   - **Why:** This is the **STANDING INSTRUCTION - PERMANENT STANDARD** for Phase 5 Step 1
   - **Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_READINESS_PACKAGE.md` (line 45, 53)
   - **Use:** Extract entity definitions, relationships, business rules

2. **Import Template Source**
   - **File:** `features/component_item_master/import_export/guides/22_DATA_IMPORT_FLOW.md`
   - **Why:** Defines CSV headers and import templates for Data Dictionary
   - **Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_READINESS_PACKAGE.md` (line 134)

3. **Feature Requirements Baseline**
   - **Files:** All `features/*/README.md` files
   - **Why:** Phase 4 closure audit references feature gaps
   - **Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_4_CLOSURE_VALIDATION_AUDIT.md` (multiple audit items)

4. **Change History**
   - **Files:** `changes/*/` folders (not in features/, but related)
   - **Why:** Track what changed from baseline

### ✅ Coverage Verification

- [x] **Phase 5 Step 1:** Canonical model explicitly referenced
- [x] **Phase 5 Step 1:** Import templates explicitly referenced
- [x] **Phase 4 Audit:** Feature gaps mapped to feature folders
- [x] **Feature Index:** Complete index available at `features/FEATURE_INDEX.md`

---

## 📁 Folder 2: `NSW Fundamental Alignment Plan/` - Master Alignment

### **WHERE** to Go

```
NSW Fundamental Alignment Plan/
├── 00_INDEX.md                                    ⭐ START HERE
├── 01_FUNDAMENTALS/                               ⭐ Core design principles
│   ├── MASTER_FUNDAMENTALS_v2.0.md                ⭐ PRIMARY FUNDAMENTALS
│   ├── FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md  ⭐ Phase 5 alignment
│   ├── CANONICAL_BOM_HIERARCHY_v1.0.md            ⭐ BOM hierarchy rules
│   ├── IMPLEMENTATION_MAPPING.md                  ⭐ Implementation guide
│   └── README.md
├── 02_GOVERNANCE/                                 ⭐ Governance standards
│   ├── NEPL_CANONICAL_RULES.md                    ⭐ Business rules
│   ├── NEPL_CUMULATIVE_VERIFICATION_STANDARD.md   ⭐ Verification rules
│   └── README.md
├── 03_GAP_REGISTERS/                              ⭐ Gap tracking
│   ├── BOM_GAP_REGISTER.md                        ⭐ BOM gaps
│   ├── MASTER_BOM_GAP_REGISTER_R1.md
│   └── PROPOSAL_BOM_GAP_REGISTER_R1.md
├── 04_PHASES/                                     ⭐ Phase execution
│   ├── PHASE_NAVIGATION_MAP.md                    ⭐ Navigation guide
│   ├── PHASE_WISE_CHECKLIST.md                    ⭐ Checklists
│   ├── PHASES_3_4_5_MASTER_PLAN.md                ⭐ Master plan
│   └── PHASES_3_4_5_TODO_TRACKER.md               ⭐ TODO tracking
├── 05_DESIGN_DOCUMENTS/                           ⭐ Design specs
│   ├── FEEDER_BOM/
│   ├── GENERIC_ITEM_MASTER/
│   ├── MASTER_BOM/
│   ├── PROPOSAL_BOM/
│   └── README.md
├── 06_PATCHES/                                    # Patch documentation
├── 07_VERIFICATION/                               # Verification tools
├── 08_REVIEWS_AND_ANALYSIS/                       # Reviews
├── 09_CODE_AND_SCRIPTS/                           # Code reference
└── 10_STANDARDS_AND_TEMPLATES/                    ⭐ Templates
    ├── CURSOR_PLAYBOOKS/
    ├── GOVERNANCE_CHECKLISTS/
    └── TEMPLATES/
```

### **WHEN** to Access

| Phase | Step | When | Files to Access |
|-------|------|------|-----------------|
| **Phase 4** | Planning | When aligning with master plan | `04_PHASES/PHASES_3_4_5_MASTER_PLAN.md` |
| **Phase 4** | Execution | When tracking gaps | `03_GAP_REGISTERS/*.md` |
| **Phase 5** | **Step 1: Data Dictionary** | **When defining canonical entities** | `01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md` |
| **Phase 5** | **Step 1: Data Dictionary** | **When validating against fundamentals** | `01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md` |
| **Phase 5** | **Step 1: Data Dictionary** | **When defining BOM hierarchy** | `01_FUNDAMENTALS/CANONICAL_BOM_HIERARCHY_v1.0.md` |
| **Phase 5** | **Step 1: Data Dictionary** | **When defining business rules** | `02_GOVERNANCE/NEPL_CANONICAL_RULES.md` |
| **Phase 5** | **Step 2: Schema Design** | **When validating schema** | `02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md` |
| **Phase 5** | Freeze Gate | When verifying compliance | `10_STANDARDS_AND_TEMPLATES/GOVERNANCE_CHECKLISTS/*.md` |
| **Post-Phase 5** | Implementation | When building features | `05_DESIGN_DOCUMENTS/*/` |

### **WHY** It's Relevant

1. **Master Fundamentals** ⭐
   - **File:** `01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
   - **Governance:** See `docs/PHASE_5/00_GOVERNANCE/FUNDAMENTALS_SOURCE_OF_TRUTH.md` for authoritative source of truth
   - **Register:** See `docs/PHASE_5/01_REFERENCE/NSW_FUNDAMENTALS_ALIGNMENT_PLAN_REGISTER.md` for complete folder registration
   - **Why:** Defines core design principles that Phase 5 must align with
   - **Use:** Ensures Data Dictionary follows master design principles

2. **Phase 5 Gap Analysis** ⭐
   - **File:** `01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`
   - **Why:** Explicitly analyzes how Fundamentals align with Phase 5
   - **Use:** Verify Phase 5 Step 1 & Step 2 align with fundamentals

3. **Canonical BOM Hierarchy** ⭐
   - **File:** `01_FUNDAMENTALS/CANONICAL_BOM_HIERARCHY_v1.0.md`
   - **Why:** Defines BOM structure rules for Phase 5 Data Dictionary
   - **Use:** Define Master BOM vs Quote BOM semantics in Step 1

4. **Business Rules** ⭐
   - **File:** `02_GOVERNANCE/NEPL_CANONICAL_RULES.md`
   - **Why:** Canonical business rules that must be captured in Data Dictionary
   - **Use:** Ensure all rules are documented in Step 1

5. **Verification Standard** ⭐
   - **File:** `02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md`
   - **Why:** Defines verification criteria for Phase 5 freeze gate
   - **Use:** Validate Step 2 Schema Design meets standards

6. **Master Plan Alignment**
   - **File:** `04_PHASES/PHASES_3_4_5_MASTER_PLAN.md`
   - **Why:** Shows how Phase 4 & 5 fit into overall master plan
   - **Use:** Ensure Phase 5 deliverables align with master plan milestones

### ✅ Coverage Verification

- [x] **Phase 5 Step 1:** Fundamentals explicitly guide Data Dictionary
- [x] **Phase 5 Step 1:** Gap analysis validates alignment
- [x] **Phase 5 Step 1:** BOM hierarchy rules defined
- [x] **Phase 5 Step 1:** Business rules catalogued
- [x] **Phase 5 Step 2:** Verification standard referenced
- [x] **Phase 4:** Master plan alignment verified
- [x] **Gap Registers:** Phase 4 gaps tracked

---

## 📁 Folder 3: `PLANNING/` - Execution Planning

### **WHERE** to Go

```
PLANNING/
├── README.md                           # Planning overview
├── PLANNING_MODE_POLICY.md             ⭐ Planning policy
├── TRANSITION_PLAN.md                  ⭐ Phase transitions
├── SETUP_COMPLETE.md                   # Setup status
├── EXECUTION/
│   └── PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md  ⭐ Gap execution
├── VERIFICATION/
│   └── PB_GAP_004_QUICK_START.md      ⭐ Quick start guide
└── PRESERVED_WORK/                     # Test cases & results
    ├── test_cases/
    ├── fixtures/
    └── results/
```

### **WHEN** to Access

| Phase | Step | When | Files to Access |
|-------|------|------|-----------------|
| **Phase 4** | Gap Execution | When executing gap fixes | `EXECUTION/PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md` |
| **Phase 4** | Verification | When verifying gap fixes | `VERIFICATION/PB_GAP_004_QUICK_START.md` |
| **Phase 5** | Planning | When understanding planning policies | `PLANNING_MODE_POLICY.md` |
| **Phase 5** | Transition | When transitioning from Phase 4 | `TRANSITION_PLAN.md` |
| **Phase 5** | Verification | When verifying test cases | `PRESERVED_WORK/test_cases/` |

### **WHY** It's Relevant

1. **Gap Execution Instructions** ⭐
   - **File:** `EXECUTION/PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md`
   - **Why:** Phase 4 gap fixes that affect Phase 5 design
   - **Use:** Ensure Phase 5 Data Dictionary accounts for gap fixes

2. **Planning Policy** ⭐
   - **File:** `PLANNING_MODE_POLICY.md`
   - **Why:** Defines how planning work relates to Phase 5
   - **Use:** Understand scope boundaries

3. **Transition Plan** ⭐
   - **File:** `TRANSITION_PLAN.md`
   - **Why:** Shows how Phase 4 work transitions to Phase 5
   - **Use:** Ensure smooth handover

4. **Verification Tools**
   - **Files:** `VERIFICATION/*.md` and `PRESERVED_WORK/test_cases/`
   - **Why:** Test cases preserved from Phase 4 for Phase 5 validation
   - **Use:** Validate Phase 5 deliverables

### ✅ Coverage Verification

- [x] **Phase 4:** Gap execution instructions mapped
- [x] **Phase 4:** Verification tools mapped
- [x] **Phase 5:** Planning policy referenced
- [x] **Phase 5:** Transition plan available

---

## 📁 Folder 4: `project/nish/` - Legacy Analysis (Read-Only)

### **WHERE** to Go

```
project/nish/
├── README.md                           # Legacy analysis overview
├── 03_NSW_SCHEMA/
│   └── NSW_SCHEMA_CANON.md             ⭐ Schema template (read-only)
└── [other legacy analysis work]
```

### **WHEN** to Access

| Phase | Step | When | Files to Access |
|-------|------|------|-----------------|
| **Phase 4** | Legacy Analysis | When understanding legacy context | `project/nish/README.md` |
| **Phase 5** | **Step 2: Schema Design** | **Reference only (NOT canonical)** | `03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` |
| **Phase 5** | Reference | When understanding what NOT to do | All files (read-only) |

### **WHY** It's Relevant

1. **Schema Template (Reference Only)** ⚠️
   - **File:** `project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md`
   - **Why:** Template exists, but **NOT canonical** - Phase 5 creates canonical version
   - **Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_READINESS_PACKAGE.md` (line 44, 234)
   - **Use:** Reference structure only, Phase 5 Step 2 creates canonical schema

2. **Legacy Context (What NOT to Do)**
   - **Files:** All `project/nish/` files
   - **Why:** Legacy analysis shows anti-patterns to avoid
   - **Reference:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md` (line 39)
   - **Use:** Understand legacy decisions we won't repeat

### ⚠️ Critical Rules

1. **Read-Only Policy:** `project/nish/` is **READ-ONLY** reference
2. **NOT Canonical:** Legacy work is **NOT** canonical truth
3. **No Code Reuse:** Do NOT copy code or schema from legacy
4. **Reference Only:** Use to understand context, not as source of truth

### ✅ Coverage Verification

- [x] **Phase 5 Step 2:** Schema template location documented (reference only)
- [x] **Read-Only Policy:** Explicitly declared in Phase 5 governance
- [x] **Not Canonical:** Clear distinction from Phase 5 canonical work

---

## 🔄 Complete Navigation Map

### Phase 4 → Phase 5 Workflow

```
Phase 4 Planning
    ↓
PLANNING/EXECUTION/*.md (Gap instructions)
    ↓
Phase 4 Execution
    ↓
features/*/ (Feature requirements)
    ↓
NSW Fundamental Alignment Plan/03_GAP_REGISTERS/*.md (Gap tracking)
    ↓
Phase 4 Closure
    ↓
docs/PHASE_5/00_GOVERNANCE/PHASE_4_CLOSURE_VALIDATION_AUDIT.md
    ↓
Phase 5 Step 1: Data Dictionary
    ↓
features/component_item_master/_general/ITEM_MASTER_DETAILED_DESIGN.md ⭐
    ↓
NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md ⭐
    ↓
NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md ⭐
    ↓
docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md (FROZEN)
    ↓
Phase 5 Step 2: Schema Design
    ↓
docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md (FROZEN)
    ↓
project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md (Reference only - NOT canonical)
    ↓
NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md
    ↓
docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md (FROZEN)
```

---

## ✅ Completeness Verification Checklist

### Folder 1: `features/`
- [x] Canonical model explicitly mapped (`ITEM_MASTER_DETAILED_DESIGN.md`)
- [x] Import templates mapped (`import_export/guides/*.md`)
- [x] Feature index available (`FEATURE_INDEX.md`)
- [x] Phase 4 audit references mapped
- [x] **WHERE/WHEN/WHY** documented above

### Folder 2: `NSW Fundamental Alignment Plan/`
- [x] Master fundamentals mapped (`MASTER_FUNDAMENTALS_v2.0.md`)
- [x] Phase 5 gap analysis mapped (`FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`)
- [x] BOM hierarchy rules mapped (`CANONICAL_BOM_HIERARCHY_v1.0.md`)
- [x] Business rules mapped (`NEPL_CANONICAL_RULES.md`)
- [x] Verification standard mapped (`NEPL_CUMULATIVE_VERIFICATION_STANDARD.md`)
- [x] Master plan mapped (`PHASES_3_4_5_MASTER_PLAN.md`)
- [x] **WHERE/WHEN/WHY** documented above

### Folder 3: `PLANNING/`
- [x] Gap execution instructions mapped (`EXECUTION/PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md`)
- [x] Planning policy mapped (`PLANNING_MODE_POLICY.md`)
- [x] Transition plan mapped (`TRANSITION_PLAN.md`)
- [x] Verification tools mapped (`VERIFICATION/*.md`)
- [x] **WHERE/WHEN/WHY** documented above

### Folder 4: `project/nish/`
- [x] Schema template location documented (reference only)
- [x] Read-only policy explicitly stated
- [x] Not canonical distinction clear
- [x] **WHERE/WHEN/WHY** documented above

---

## 📋 Quick Reference: When to Use Which Folder

| Need | Folder | File |
|------|--------|------|
| **Canonical data model** | `features/` | `component_item_master/_general/ITEM_MASTER_DETAILED_DESIGN.md` |
| **Import templates** | `features/` | `component_item_master/import_export/guides/*.md` |
| **Design principles** | `NSW Fundamental Alignment Plan/` | `01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md` |
| **BOM hierarchy rules** | `NSW Fundamental Alignment Plan/` | `01_FUNDAMENTALS/CANONICAL_BOM_HIERARCHY_v1.0.md` |
| **Business rules** | `NSW Fundamental Alignment Plan/` | `02_GOVERNANCE/NEPL_CANONICAL_RULES.md` |
| **Verification standard** | `NSW Fundamental Alignment Plan/` | `02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md` |
| **Gap execution** | `PLANNING/` | `EXECUTION/PB_GAP_004_P5_EXECUTION_INSTRUCTIONS.md` |
| **Schema reference** | `project/nish/` | `03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` (read-only) |

---

## 🎯 Summary

**All four folders are mapped and integrated into Phase 4 & 5 work:**

1. ✅ **`features/`** - Primary source for canonical data model (Phase 5 Step 1)
2. ✅ **`NSW Fundamental Alignment Plan/`** - Design principles, rules, and standards (Phase 5 Step 1 & 2)
3. ✅ **`PLANNING/`** - Gap execution and transition planning (Phase 4 → Phase 5)
4. ✅ **`project/nish/`** - Legacy reference only (read-only, not canonical)

**Navigation is clear:** WHERE (file paths), WHEN (phase/step), WHY (purpose) all documented above.

**Nothing is missed:** Complete verification checklist confirms all key files mapped.

---

## Change Log
- v1.0: Created complete folder mapping guide with WHERE/WHEN/WHY navigation

