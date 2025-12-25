# Files Requiring Detailed Study — Priority List

**Date:** 2025-12-18  
**Purpose:** List of files from NSW Fundamental Alignment Plan that require detailed study  
**Status:** 📋 EVALUATION COMPLETE

---

## Summary

After comprehensive review of the NSW Fundamental Alignment Plan, the following files require detailed study before integration into our work:

- **Priority 1 (Critical):** 3 files — 4-7 hours
- **Priority 2 (Important):** 2 files — 1.5-3 hours
- **Priority 3 (Reference):** 4 files — 1-2 hours
- **Total:** 9 files — 6.5-12 hours

---

## Priority 1: Critical (Must Review in Detail)

### 1. MASTER_REFERENCE.md

**File Path:** `NSW Fundamental Alignment Plan/MASTER_REFERENCE.md`

**Why Critical:**
- Core reference document for all 9 fundamentals layers
- Single source of truth for layer definitions
- Essential for Phase 5 NSW requirements extraction
- Directly aligns with Phase 1 baseline work

**Time Required:** 2-3 hours

**Focus Areas:**
1. **Layer Definitions (A through I):**
   - Category / Subcategory / Type(Item) / Attributes
   - Item/Component List
   - Generic Item Master (L0/L1)
   - Specific Item Master (L2)
   - Master BOM (generic, L1)
   - Master BOM (specific) — NOT FOUND
   - Proposal BOM + Proposal Sub-BOM (L2)
   - Feeder BOM
   - Panel BOM

2. **Source-of-Truth Files:**
   - Document references for each layer
   - Baseline freeze documents
   - Gap registers
   - Implementation blueprints

3. **Key Rules:**
   - Copy-never-link rules
   - ProductType rules (L1 vs L2)
   - Layer compliance rules
   - Write gateway rules

4. **Known Gaps:**
   - Gap-to-layer mapping
   - Open gaps per layer
   - Gap closure criteria

5. **Legacy Data Integrity:**
   - Problem statement
   - Symptoms
   - Risk impact
   - Remediation sequencing

**Questions to Answer:**
- How do layer definitions align with our Phase 1 baselines?
- What gaps exist that we need to address?
- How does legacy data integrity affect our work?
- What source-of-truth files do we need to reference?

---

### 2. GAP_REGISTERS_GUIDE.md

**File Path:** `NSW Fundamental Alignment Plan/GAP_REGISTERS_GUIDE.md`

**Why Critical:**
- Essential for structured gap management
- DOC-CLOSED vs RUN-CLOSED distinction
- Gap status tracking procedures
- Layer-to-gap mapping

**Time Required:** 1-2 hours

**Focus Areas:**
1. **Gap Register Structure:**
   - What gap registers exist
   - Gap register files and locations
   - Gap ID format and naming

2. **Status Fields:**
   - OPEN status
   - PARTIALLY RESOLVED status
   - CLOSED status
   - DOC-CLOSED vs RUN-CLOSED distinction

3. **Update Procedures:**
   - How to update gap status
   - When to update (during execution windows)
   - Who updates (execution engineer, gap owner)
   - Evidence requirements

4. **Layer Mapping:**
   - Which gaps affect which layers
   - Gap-to-layer relationships
   - Layer compliance verification

5. **Gap Register Files:**
   - BOM Gap Register (primary)
   - Proposal BOM Gap Register
   - Master BOM Gap Register
   - Fundamentals Gap Correction TODO

**Questions to Answer:**
- How do we integrate gap registers into Phase 5?
- What gaps are currently OPEN that we need to address?
- How do we track gap closure during NSW development?
- What evidence is required to close gaps?

---

### 3. ADOPTION_STRATEGIC_ANALYSIS.md

**File Path:** `NSW Fundamental Alignment Plan/ADOPTION_STRATEGIC_ANALYSIS.md`

**Why Critical:**
- Strategic adoption guidance
- Value assessment
- Integration feasibility analysis
- Risk assessment and mitigation

**Time Required:** 1-2 hours

**Focus Areas:**
1. **Value Assessment:**
   - Is it really useful? (YES — High Value)
   - Did it add value? (YES — Significant Value)
   - Value score: 9/10

2. **Integration Feasibility:**
   - Can we plug it in? (YES — With Minimal Disruption)
   - Integration complexity: LOW
   - Time required: 4-6 hours (planning)
   - Disruption risk: LOW (5-10%)

3. **Challenges and Risks:**
   - Schema verification required (MEDIUM)
   - Legacy data integrity (HIGH)
   - Code locality (LOW)
   - Panel Master discovery (MEDIUM)

4. **Adoption Strategy:**
   - Parallel with Phase 5 planning
   - Incremental integration
   - Non-blocking approach

5. **Timeline and Effort:**
   - Planning work: 4-6 hours
   - Execution work: 10-20 hours
   - Total: 14-26 hours

**Questions to Answer:**
- What is the recommended adoption strategy?
- What are the key challenges and how do we mitigate them?
- How much time and effort is required?
- What is the disruption risk?

---

## Priority 2: Important (Should Review in Detail)

### 4. IMPLEMENTATION_MAPPING.md

**File Path:** `NSW Fundamental Alignment Plan/IMPLEMENTATION_MAPPING.md`

**Why Important:**
- Shows current implementation status
- Target architecture definition
- Delta table (what needs to be implemented)
- Execution mapping bridge

**Time Required:** 1-2 hours

**Focus Areas:**
1. **Current Implementation Signals:**
   - What exists in codebase
   - What is INFERRED vs CONFIRMED-IN-REPO
   - Schema verification requirements

2. **Target Architecture:**
   - Canonical flow (Thin Controller → BomEngine → History → Gates)
   - Architecture principles
   - Service layer design

3. **Delta Table:**
   - Layer-by-layer implementation mapping
   - Required additions/changes
   - Risks and verification gates

4. **Execution Mapping:**
   - Screen → API → Service → DB bridge
   - Validation trigger points
   - Write gates to screens

5. **Code Locality Note:**
   - Codebase in separate repository
   - Code references are INFERRED
   - Verification required

**Questions to Answer:**
- What is the current implementation status?
- What needs to be implemented for NSW?
- How do we verify code locations?
- What is the target architecture?

---

### 5. PATCH_APPENDIX_v1.1.md

**File Path:** `NSW Fundamental Alignment Plan/PATCH_APPENDIX_v1.1.md`

**Why Important:**
- Audit-safe guardrails
- Badge system (CONFIRMED-IN-REPO, INFERRED, DOC-CLOSED, RUN-CLOSED)
- Schema inference rules
- Legacy data integrity strategy

**Time Required:** 30 minutes - 1 hour

**Focus Areas:**
1. **Badge System:**
   - CONFIRMED-IN-REPO badge
   - INFERRED badge
   - DOC-CLOSED badge
   - RUN-CLOSED badge

2. **Schema Inference Rules:**
   - When to use INFERRED
   - When to use CONFIRMED-IN-REPO
   - How to verify schemas

3. **Legacy Data Integrity Strategy:**
   - Problem acknowledgment
   - Remediation approach
   - Evidence requirements

4. **Audit-Safe Practices:**
   - How to prevent overstating
   - Truth level transparency
   - Documentation standards

**Questions to Answer:**
- How do we apply the badge system to our documentation?
- What are the schema inference rules?
- How do we handle legacy data integrity?
- What are the audit-safe practices?

---

## Priority 3: Reference (Review as Needed)

### 6. FILE_LINK_GRAPH.md

**File Path:** `NSW Fundamental Alignment Plan/FILE_LINK_GRAPH.md`

**Why Reference:**
- Document dependency map
- Navigation tool
- Shows document relationships

**Time Required:** 30 minutes - 1 hour

**Focus Areas:**
- Document relationships
- Bridge documents
- Downstream dependents
- Navigation paths

**When to Review:**
- When navigating between documents
- When understanding document dependencies
- When finding related documents

---

### 7. INDEX.md

**File Path:** `NSW Fundamental Alignment Plan/INDEX.md`

**Why Reference:**
- Master index and navigation
- Quick reference to all documents
- File locations

**Time Required:** 15-30 minutes

**Focus Areas:**
- Pack contents listing
- Quick navigation
- File locations
- Document relationships

**When to Review:**
- When first exploring the pack
- When looking for specific documents
- When understanding pack structure

---

### 8. ADOPTION_QUICK_ANSWERS.md

**File Path:** `NSW Fundamental Alignment Plan/ADOPTION_QUICK_ANSWERS.md`

**Why Reference:**
- Quick answers to common questions
- Quick reference for adoption decision
- Timeline and effort estimates

**Time Required:** 15-30 minutes

**Focus Areas:**
- 10 key questions answered
- Quick reference
- Timeline and effort
- Final recommendation

**When to Review:**
- When making quick decisions
- When answering stakeholder questions
- When estimating effort

---

### 9. v1.1_UPDATE_SUMMARY.md

**File Path:** `NSW Fundamental Alignment Plan/v1.1_UPDATE_SUMMARY.md`

**Why Reference:**
- Version history
- Changes from v1.0 to v1.1
- Update summary

**Time Required:** 15 minutes

**Focus Areas:**
- Version changes
- Updates summary
- Date corrections

**When to Review:**
- When understanding version history
- When checking for updates

---

## Study Plan

### Week 1: Priority 1 Documents (4-7 hours)

**Day 1-2:**
- Review MASTER_REFERENCE.md (2-3 hours)
- Document layer definitions alignment
- Identify gaps and issues

**Day 3:**
- Review GAP_REGISTERS_GUIDE.md (1-2 hours)
- Understand gap management structure
- Plan gap tracking integration

**Day 4:**
- Review ADOPTION_STRATEGIC_ANALYSIS.md (1-2 hours)
- Make adoption decision
- Plan integration approach

---

### Week 2: Priority 2 Documents (1.5-3 hours)

**Day 1:**
- Review IMPLEMENTATION_MAPPING.md (1-2 hours)
- Understand current vs target state
- Plan implementation mapping

**Day 2:**
- Review PATCH_APPENDIX_v1.1.md (30 minutes - 1 hour)
- Understand badge system
- Plan audit-safe practices

---

### Week 3: Priority 3 Documents (1-2 hours, as needed)

- Review FILE_LINK_GRAPH.md (30 minutes - 1 hour)
- Review INDEX.md (15-30 minutes)
- Review ADOPTION_QUICK_ANSWERS.md (15-30 minutes)
- Review v1.1_UPDATE_SUMMARY.md (15 minutes)

---

## Study Checklist

### Priority 1 Checklist

- [ ] **MASTER_REFERENCE.md**
  - [ ] Read all 9 layer sections
  - [ ] Document layer definitions alignment with Phase 1
  - [ ] Identify source-of-truth files
  - [ ] List key rules per layer
  - [ ] Document known gaps per layer
  - [ ] Review legacy data integrity section

- [ ] **GAP_REGISTERS_GUIDE.md**
  - [ ] Understand gap register structure
  - [ ] Understand status fields (OPEN, PARTIALLY RESOLVED, CLOSED)
  - [ ] Understand DOC-CLOSED vs RUN-CLOSED
  - [ ] Review update procedures
  - [ ] Review layer mapping
  - [ ] List all gap register files

- [ ] **ADOPTION_STRATEGIC_ANALYSIS.md**
  - [ ] Review value assessment
  - [ ] Review integration feasibility
  - [ ] Review challenges and risks
  - [ ] Review adoption strategy
  - [ ] Review timeline and effort
  - [ ] Make adoption decision

---

### Priority 2 Checklist

- [ ] **IMPLEMENTATION_MAPPING.md**
  - [ ] Review current implementation signals
  - [ ] Review target architecture
  - [ ] Review delta table
  - [ ] Review execution mapping
  - [ ] Review code locality note

- [ ] **PATCH_APPENDIX_v1.1.md**
  - [ ] Understand badge system
  - [ ] Understand schema inference rules
  - [ ] Review legacy data integrity strategy
  - [ ] Review audit-safe practices

---

### Priority 3 Checklist (As Needed)

- [ ] **FILE_LINK_GRAPH.md** — Review when navigating documents
- [ ] **INDEX.md** — Review when first exploring pack
- [ ] **ADOPTION_QUICK_ANSWERS.md** — Review for quick reference
- [ ] **v1.1_UPDATE_SUMMARY.md** — Review for version history

---

## Output Deliverables

After detailed study, create:

1. **Layer Definitions Alignment Document**
   - How Fundamentals layers align with Phase 1 baselines
   - Gaps and differences
   - Integration points

2. **Gap Management Integration Plan**
   - How to integrate gap registers into Phase 5
   - Gap tracking procedures
   - Gap closure criteria

3. **Implementation Mapping Plan**
   - Current state assessment
   - Target architecture alignment
   - Implementation requirements

4. **Adoption Decision Document**
   - Final adoption decision
   - Integration approach
   - Timeline and effort

---

**Status:** ✅ **COMPLETE**  
**Next Action:** Begin Priority 1 document review (4-7 hours)

---

**END OF FILES FOR DETAILED STUDY**

