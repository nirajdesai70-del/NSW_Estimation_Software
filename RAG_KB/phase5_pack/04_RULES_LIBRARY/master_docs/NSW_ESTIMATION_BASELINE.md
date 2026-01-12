---
Source: docs/NSW_ESTIMATION_BASELINE.md
KB_Namespace: master_docs
Status: WORKING
Last_Updated: 2025-12-17T00:03:30.512088
KB_Path: phase5_pack/04_RULES_LIBRARY/master_docs/NSW_ESTIMATION_BASELINE.md
---

# NSW Estimation Software - Baseline Definition

**Version:** 1.0  
**Date:** 2025-12-16  
**Status:** Master Baseline Document

## Purpose

This chart/document is not a UI sketch or a feature wishlist. It is a transition map that:
- Locks the functional truth of NEPL Estimation (V2)
- Defines what stays, what refines, what extends
- Prevents ad-hoc fixes and repeated breakage
- Becomes the single reference for: Architecture, UI work, Data model, AI add-on, Future versions

**Rule:** This chart governs everything. No feature, UI change, or enhancement happens without mapping to this baseline.

---

## 1. Purpose of This Chart (Why It Exists)

This chart is not a UI sketch or a feature wishlist. It is a transition map that:

1. **Locks the functional truth of NEPL Estimation (V2)**
   - Captures what actually works
   - Documents current behavior
   - Prevents assumptions

2. **Defines what stays, what refines, what extends**
   - Clear boundaries
   - No ambiguity
   - Structured evolution

3. **Prevents ad-hoc fixes and repeated breakage**
   - Single source of truth
   - No conflicting changes
   - Controlled evolution

4. **Becomes the single reference for:**
   - Architecture decisions
   - UI work
   - Data model design
   - AI add-on development
   - Future versions

---

## 2. Scope Boundary (Non-Negotiable)

### What is IN Scope

✅ **Estimation logic (Panels → Feeders → BOM → Items)**
- Core business process
- Must be preserved exactly
- No changes to calculation logic

✅ **Category / Subcategory / Type / Attribute flow**
- Fundamental data structure
- Must preserve hierarchy
- May improve UI presentation

✅ **Item Master, Component Master**
- Core master data
- Must preserve structure
- May enhance functionality

✅ **Quotation lifecycle**
- Business process
- Must preserve workflow
- May improve UI

✅ **Costing logic (manual + assisted)**
- Core functionality
- Must preserve calculations
- May enhance assistance

✅ **UI refactoring only in appearance, not behavior**
- Visual improvements allowed
- Behavioral changes require approval
- Must maintain functionality

---

### What is OUT of Scope (for now)

❌ **Changing pricing formula**
- Formulas are locked
- No changes without formal approval
- Requires impact analysis

❌ **Rewriting V2 data relationships**
- Relationships are locked
- No structural changes
- Preserve referential integrity

❌ **Replacing NEPL database logic**
- Database logic is locked
- No migration to different database
- Preserve existing queries

❌ **New workflows without mapping**
- All workflows must map to baseline
- No ad-hoc workflows
- Requires baseline update first

---

## 3. Structural Layers (How to Read the Chart)

**Your chart should always be read top → down, never left → right.**

### Layer 1 — Business Objects (Stable)

These do not change between NEPL → NSW:

- **Category**
- **Subcategory**
- **Type**
- **Attribute**
- **Item / Component**
- **BOM**
- **Quotation**
- **Project**

**Rule:** These entities and their core properties are immutable.

---

### Layer 2 — Logical Flow (Frozen)

This is V2 truth and must be preserved:

```
Project
  └── Panel
      └── Feeder
          └── BOM
              └── BOM Item
                  ├── Item (via item_id)
                  └── Component (via component_id)
                  └── Quantity × Unit Price = Total Price

Category
  └── Subcategory
      └── Type
          └── Attribute
              └── Item (uses hierarchy)
```

**Rule:** No shortcuts. No reverse dependencies. No UI-driven logic.

**Key Flows:**
1. **Estimation Flow:** Project → Panel → Feeder → BOM → Items/Components → Quotation
2. **Master Data Flow:** Category → Subcategory → Type → Attribute → Item
3. **Calculation Flow:** BOM Items → Calculate Totals → Update BOM Total → Generate Quotation

---

### Layer 3 — NSW Enhancements (Additive Only)

This is where NSW differentiates, without breaking NEPL:

✅ **Validation matrices**
- Add validation rules
- Don't change existing validations
- Enhance data quality

✅ **Dependency checks**
- Check relationships before actions
- Prevent invalid operations
- Improve data integrity

✅ **AI suggestion layer (non-blocking)**
- Suggest items, prices, etc.
- Optional, not required
- Doesn't block user actions

✅ **Rule hints / warnings**
- Guide users
- Prevent mistakes
- Improve UX

✅ **UI clarity improvement**
- Better labels
- Better organization
- Better feedback

✅ **Audit visibility**
- Track changes
- Show history
- Improve transparency

**Rule:** All enhancements are additive. Nothing is removed or changed.

---

## 4. Interconnection Process (Execution Rules)

This chart must drive three documents, always together:

### File 1 — Master Baseline (Why & What)
- Purpose
- Definition
- Fixed rules
- Non-negotiable
- Version guardrails

**This Document:** NSW_ESTIMATION_BASELINE.md

---

### File 2 — Connection Matrix (How Things Talk)

A table showing:
- Entity relationships
- Data flow
- API contracts
- Integration points

**File:** `docs/CONNECTION_MATRIX.md` (to be created)

---

### File 3 — Execution Mapping (Where It Appears)

Mapping showing:
- Screen / Section
- Visible fields
- Editable vs locked
- Validation timing
- Cost impact

**File:** `docs/EXECUTION_MAPPING.md` (to be created)

---

## 5. Versioning & Escalation Model

### Version Rules

- **NEPL V2 = Reference truth**
  - This is what we're preserving
  - No changes to V2 logic
  - V2 is the baseline

- **NSW v1.0 = Structured refinement**
  - First NSW version
  - Preserves all V2 logic
  - Adds enhancements only

- **NSW v1.x = Enhancements only**
  - Minor versions
  - Additive changes only
  - No breaking changes

- **NSW v2.0 = Only after full freeze**
  - Major version
  - Requires full baseline freeze
  - Requires formal approval

---

### Escalation Rules

If something:
- **Breaks data chain → ❌ reject**
  - Must maintain data integrity
  - No broken relationships
  - No orphaned records

- **Duplicates logic → ❌ reject**
  - No duplicate implementations
  - Single source of truth
  - Reuse existing logic

- **Bypasses hierarchy → ❌ reject**
  - Must follow hierarchy
  - No shortcuts
  - No reverse dependencies

- **Is UI-only cosmetic → ✅ allow**
  - Visual changes OK
  - No logic changes
  - No data changes

---

## 6. What We Do Next (Clear Next Steps)

### Step 1: Freeze this chart as "NSW Estimation – Structural Baseline v1.0"
- [ ] Review and approve baseline
- [ ] Version control baseline
- [ ] Communicate to team
- [ ] Make baseline immutable

---

### Step 2: Create:
- [x] **Master Baseline Document** (This document)
- [ ] **Connection Matrix** (Excel / MD)
  - Entity relationships
  - Data flow
  - API contracts
- [ ] **Execution Mapping File**
  - Screen mappings
  - Field mappings
  - Validation mappings

---

### Step 3: Only then:
- [ ] **UI appearance upgrade**
  - Based on baseline
  - No behavior changes
  - Visual improvements only

- [ ] **AI layer design**
  - Based on baseline
  - Non-blocking
  - Additive only

- [ ] **Validation enhancement**
  - Based on baseline
  - Additive validation
  - No breaking changes

---

## 7. 5R Summary (One-Page Closure)

### Result
- ✅ Single source of truth
- ✅ Zero regression risk
- ✅ Clear NEPL → NSW evolution path

### Risk
- ❌ Skipping baseline = repeat failure
- ❌ UI changes driving logic
- ❌ Unmapped AI features

### Rule
- ✅ V2 logic untouched
- ✅ Additive only
- ✅ Chart governs everything

### Roadmap
1. Freeze chart
2. Build 3 baseline files
3. UI refinement
4. AI augmentation

### Reference
- NEPL Estimation V2
- Existing BOM & Quotation logic
- Current UI audit notes

---

## 8. Governing Principles

### Principle 1: Logic First, UI Second
- Business logic drives UI
- UI never drives logic
- Logic is immutable

### Principle 2: Additive Only
- Enhancements don't remove
- Enhancements don't change
- Enhancements only add

### Principle 3: Chart Governs Everything
- No feature without baseline mapping
- No change without baseline update
- Baseline is single source of truth

### Principle 4: Version Control
- All changes are versioned
- All changes are documented
- All changes are approved

---

## Next Steps

1. ✅ Freeze this baseline document
2. Create Connection Matrix
3. Create Execution Mapping
4. Begin NSW development based on baseline
5. Maintain baseline as single source of truth

---

**Document Owner:** [Name]  
**Version:** 1.0  
**Last Updated:** 2025-12-16  
**Status:** FROZEN - Structural Baseline v1.0

