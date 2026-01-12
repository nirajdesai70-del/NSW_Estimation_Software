---
Status: CANONICAL
Version: 1.0
Owner: Phase 5 Governance
Updated: 2025-01-27
Scope: UI Classification Policy
---

# UI Context Classification Policy

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose

This document establishes the classification rule for UI code to prevent conceptual drift and decision pollution between **Reference Harness UI** (built in existing NEPL app for validation) and **Phase-5 UI Design** (future clean slate design).

This policy prevents prototype/harness UI from being confused with final Phase-5 UI design, ensuring clean architectural boundaries.

---

## ⚠️ Critical Rule

**Any UI implementation done inside the existing NEPL Estimation Software is PROTOTYPE / HARNESS ONLY and MUST NOT be treated as Phase-5 UI design.**

---

## UI Context Classifications

### 🔧 REFERENCE HARNESS (Track A)

**Definition:** UI code built inside the existing NEPL Estimation Software for behavior validation, API testing, and telemetry collection.

**Purpose:**
- Validate RAG API integration
- Test latency and error handling
- Validate citation display and feedback loops
- Validate Blade/JS interaction patterns
- Collect telemetry data

**Classification Label:** `REFERENCE HARNESS`

**Examples:**
- RAG UI components (`resources/views/components/rag-*.blade.php`)
- Example integration pages (`resources/views/examples/rag-*.blade.php`)
- Any Blade templates created to test RAG API behavior

**What It Is:**
- ✅ Implementation scaffolding for validation
- ✅ Visual harness for testing
- ✅ Prototype for behavior verification

**What It Is NOT:**
- ❌ Phase-5 UI design
- ❌ Final UI implementation
- ❌ Migration target
- ❌ Production UI for NSW

**Status:** Temporary, for validation only

---

### 🎨 PHASE-5 UI DESIGN (Track B)

**Definition:** Clean slate UI design that will be created after Phase-5 Schema Freeze, based on Phase-5 canonical data dictionary and schema.

**Purpose:**
- Define UI principles
- Create screen inventory
- Design component system
- Establish navigation model
- Create final production UI

**Classification Label:** `PHASE-5 UI`

**When:** Starts only after Phase-5 Schema Freeze (post-Phase-5)

**Status:** Future work, not yet started

---

## Two-Track Model

### Track A: Behavior Validation (Current)

**Location:** Existing NEPL Estimation Software  
**Scope:** RAG API validation, latency testing, citation display  
**Timeline:** Ongoing (until Phase-5 UI design begins)  
**Purpose:** Validate RAG integration behavior  

**Files:**
- `resources/views/components/rag-*.blade.php`
- `resources/views/examples/rag-*.blade.php`
- Related JavaScript and CSS files

---

### Track B: Phase-5 UI Design (Future)

**Location:** Separate chat + clean specs  
**Scope:** Complete UI design from scratch  
**Timeline:** After Phase-5 Schema Freeze  
**Purpose:** Design final NSW UI  

**Approach:**
- New chat session (separate from validation work)
- Clean UI principles document
- Screen inventory
- Component system design
- Navigation model
- Treat NEPL UI only as "what to avoid" and "what to simplify"
- No code reuse from Reference Harness

---

## Enforcement Mechanisms

### 1. Banner Comments (Required)

**Rule:** Every Reference Harness UI file MUST include a banner comment at the top.

**Standard Banner:**
```blade
{{-- 
UI CONTEXT: REFERENCE HARNESS ONLY
Purpose: Validate RAG API, latency, citations, feedback loop
NOT Phase-5 UI design
--}}
```

**Location:** Top of every Blade template file used for validation

**Enforcement:** Manual review during code reviews

---

### 2. Mental Bucket Classification

**Rule:** All Reference Harness work must be mentally classified as:

**"RAG UI Harness for Behaviour Validation"**

**NOT:**
- "Phase-5 UI"
- "Final screen design"
- "Production UI"

**Purpose:** Prevents 80% of future confusion through correct mental framing

---

### 3. Documentation Separation

**Rule:** Reference Harness UI documentation must be kept separate from Phase-5 UI design documentation.

**Current Documentation:**
- `RAG_KB/UI_IMPLEMENTATION_SUMMARY.md` - Reference Harness implementation
- `RAG_KB/UI_INTEGRATION_GUIDE.md` - Reference Harness integration guide

**Future Documentation:**
- Phase-5 UI design documents (to be created in separate location)
- UI principles document
- Screen inventory
- Component system spec

---

### 4. RAG KB Exclusion (Already Enforced)

**Rule:** RAG KB does NOT ingest Blade/UI code as truth.

**Current Status:** ✅ Already enforced

**How It Works:**
- RAG KB indexer only reads from `RAG_KB/phase5_pack/`
- `resources/views/` is NOT indexed
- Only documented decisions, rules, governance, and summaries are ingested
- Legacy UI code cannot pollute KB

**Verification:**
- Indexer source: `services/kb_indexer/indexer.py`
- Indexer reads from: `RAG_KB/phase5_pack/` (via manifest)
- UI files location: `resources/views/` (excluded by design)

---

## Risks Prevented

This policy prevents:

1. **Conceptual Drift:**
   - Subconsciously copying legacy UI flows
   - Inheriting old screen logic
   - Justifying decisions with "we already did this in NEPL"

2. **Decision Pollution:**
   - Mixing Phase-5 specs with Phase-4/legacy assumptions
   - Treating prototype UI as production design
   - Confusing validation harness with final UI

3. **Architectural Confusion:**
   - Assuming Reference Harness UI = Phase-5 UI
   - Using prototype code as migration target
   - Building Phase-5 UI on top of harness patterns

---

## Integration with Existing Governance

### Phase-5 Charter Alignment

**Reference:** `PHASE_5_CHARTER.md`

**Key Rule:** "No UI before Schema Freeze"

**Alignment:**
- Reference Harness = validation/testing only (allowed)
- Phase-5 UI Design = post-Schema Freeze (future)
- This policy clarifies the distinction

---

### Legacy vs NSW Coexistence Policy

**Reference:** `LEGACY_VS_NSW_COEXISTENCE_POLICY.md`

**Alignment:**
- Reference Harness = Legacy UI layer (NEPL app)
- Phase-5 UI = NSW UI layer (future clean design)
- Same two-truth model applies to UI classification

---

### Scope Separation Policy

**Reference:** `SCOPE_SEPARATION.md`

**Alignment:**
- Phase-5 = Canonical definition only (documents)
- Reference Harness UI = Not part of Phase-5 scope
- Phase-5 UI Design = Post-Phase-5 work

---

## When Phase-5 UI Design Actually Starts

**Trigger Statement:** "Start Phase-5 UI design (clean slate)"

**Actions:**
1. Open new chat session (separate from validation work)
2. Create UI principles document
3. Create screen inventory
4. Design component system
5. Establish navigation model
6. Treat NEPL UI only as:
   - "What to avoid"
   - "What to simplify"
7. No code reuse from Reference Harness

**Prerequisites:**
- Phase-5 Schema Freeze complete
- Canonical data dictionary frozen
- Canonical schema frozen
- Phase-5 governance approval

---

## Summary Statement

**Key Rule:**
> Any UI implementation done inside the existing NEPL Estimation Software is **REFERENCE HARNESS ONLY** and MUST NOT be treated as Phase-5 UI design.

**Classification:**
- **Track A (Current):** Reference Harness UI in NEPL app = validation only
- **Track B (Future):** Phase-5 UI Design = clean slate after Schema Freeze

**Protection:**
- Banner comments enforce classification
- Mental framing prevents confusion
- RAG KB excludes UI code
- Documentation separation maintains boundaries

**Result:**
- Zero technical conflict
- Zero long-term architectural confusion
- Clean separation between validation and design

---

## Change Log

- **v1.0 (2025-01-27):** Initial policy created to prevent UI classification confusion

---

**Document Status:** ✅ **CANONICAL**  
**Last Updated:** 2025-01-27  
**Next Review:** After Phase-5 UI design begins  
**Owner:** Phase-5 Governance Team

