# Phase 6 Governance Rules
## Phase 6 First Rule & Conflict Resolution

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** ACTIVE  
**Purpose:** Establish governance rules for Phase 6, including the "Phase 6 First" rule for conflict resolution

---

## 🎯 Phase 6 First Rule (Primary Governance Rule)

### The Rule

**"Phase 6 logic is the first right of working. When there is a conflict between old NEPL software logic and new Phase 6 logic, Phase 6 new adoption will prevail, but not compromising any function."**

### Interpretation

1. **Phase 6 Logic Takes Precedence**
   - When Phase 6 design/logic conflicts with NEPL legacy logic, Phase 6 logic is adopted
   - Phase 6 represents the new system design and should be the primary reference

2. **Functionality Must Be Preserved**
   - **Critical:** No function from NEPL can be lost
   - All NEPL capabilities must be preserved in Phase 6
   - Phase 6 may add new features, but cannot remove existing functionality

3. **Verify Before Adopting**
   - Before adopting Phase 6 logic, verify that all NEPL functions are covered
   - If a function is missing in Phase 6, it must be added (not skipped)

4. **Document All Decisions**
   - All conflicts and resolutions must be documented in `PHASE_6_DECISION_REGISTER.md`
   - Decision rationale must be clear
   - Function preservation verification must be recorded

5. **Test Equivalence**
   - After adopting Phase 6 logic, test that all NEPL functions still work
   - Verify no regression in functionality
   - Document test results

---

## 🔄 Conflict Resolution Process

### Step 1: Identify Conflict
- Document the conflict clearly
- Identify which NEPL function/logic conflicts with Phase 6
- Identify which Phase 6 logic conflicts with NEPL

### Step 2: Verify Functionality
- List all NEPL functions related to the conflict
- Verify each function is covered in Phase 6 design
- Identify any missing functions

### Step 3: Document Decision
- Record in `PHASE_6_DECISION_REGISTER.md`
- Document: Conflict, NEPL functions, Phase 6 approach, Function preservation verification
- Assign decision ID (e.g., P6-DEC-001)

### Step 4: Test Equivalence
- Test that Phase 6 implementation preserves all NEPL functions
- Verify no functionality loss
- Document test results

### Step 5: Adopt Phase 6
- Implement Phase 6 logic
- Ensure all NEPL functions are preserved
- Mark decision as implemented

---

## 📋 Core Governance Principles

### Principle 1: Phase 6 Rule (Locked)
**"Phase-6 may add features, but may not change meaning."**

- ✅ Can add: UI layers, tooling, workflows, derived datasets, dashboards, exports
- ✅ Can add: Reuse workflows, legacy parity features
- ❌ Cannot change: Schema semantics, guardrails, locked decisions, resolution logic

**Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md` (Section 8)

---

### Principle 2: Function Preservation (Non-Negotiable)
**All NEPL functions must be preserved in Phase 6.**

- ✅ All NEPL modules must work in Phase 6
- ✅ All NEPL workflows must be preserved
- ✅ All NEPL calculations must produce same results
- ❌ No function can be removed or disabled

**Source:** `PHASE_6_NEPL_BASELINE_REVIEW.md` (Section: What Must Be Preserved)

---

### Principle 3: Additive Only
**Phase 6 can only add, never remove or change meaning.**

- ✅ Add new features
- ✅ Add enhancements
- ✅ Add new capabilities
- ❌ Remove existing features
- ❌ Change existing behavior meaning
- ❌ Break existing functionality

**Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md` (Section 9)

---

### Principle 4: Schema Canon is Frozen
**Phase 5 Schema Canon v1.0 is frozen and cannot be changed in Phase 6.**

- ✅ Can add new tables (with approval)
- ✅ Can add new columns (with approval)
- ❌ Cannot change existing table structures
- ❌ Cannot change existing column meanings
- ❌ Cannot remove existing tables/columns

**Source:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`

---

### Principle 5: Guardrails Are Enforced
**Phase 5 Guardrails (G-01 to G-08) must be enforced in Phase 6.**

- ✅ All guardrails must be implemented
- ✅ All guardrails must be tested
- ✅ Guardrail violations must be prevented
- ❌ Cannot bypass guardrails
- ❌ Cannot disable guardrails

**Source:** `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` (Section: Canonical Validation Guardrails)

---

### Principle 6: Locked Decisions Are Immutable
**Phase 5 Locked Decisions (D-005, D-006, D-007, D-009, etc.) cannot be changed.**

- ✅ Must implement locked decisions as specified
- ✅ Must preserve decision intent
- ❌ Cannot change locked decision logic
- ❌ Cannot override locked decisions

**Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md`

---

### Principle 7: Copy-Never-Link Rule
**All reuse operations must copy, never link.**

- ✅ Copy quotations, panels, feeders, BOMs
- ✅ All copies are independent
- ❌ Never create links between instances
- ❌ Never share mutable state

**Source:** `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md`

---

### Rule 7: Decision vs Working Truth

**Purpose:** Prevent RAG contamination and maintain clear separation between decision rationale and working truth.

#### The Rule

**"Only documents in `01_MASTER_DOCUMENTS/`, `03_MATRICES/`, and `09_SPECIFICATIONS/` are Working Truth. All rationale, debates, and tradeoffs live in Decision RAG + Decision Register. Cursor execution may read decisions, but may write only to Working Truth sources."**

#### Working Truth Sources (Authoritative)

These folders contain documents that Cursor/RAG can **write to**:

1. **01_MASTER_DOCUMENTS/** - Master planning documents
2. **03_MATRICES/** - Task lists and tracking matrices
3. **09_SPECIFICATIONS/** - Technical specifications
4. **12_ARCHITECTURE/** - Architecture documents (when populated)

#### Decision Truth Sources (Read-Only for Cursor)

These folders contain documents that Cursor/RAG can **read from** but **cannot write to**:

1. **00_GOVERNANCE/03_DECISIONS/** - Decision documents
2. **00_GOVERNANCE/00_RULES/** - Governance rules (except updates via Decision Register)
3. **06_REVIEWS_AND_VERIFICATION/** - Review documents
4. **10_EVIDENCE/** - Evidence packs (immutable)

#### Enforcement

- **Cursor/RAG writes:** Only to Working Truth sources
- **Cursor/RAG reads:** Can read from all sources
- **Decision rationale:** Must be in Decision Register, not in Working Truth documents
- **Tradeoffs and alternatives:** Documented in Decision RAG, not in specifications

#### Rationale

This separation prevents:
- RAG contamination of working documents with decision rationale
- Specs becoming bloated with "why" instead of "what"
- Ambiguity about what is authoritative vs what is historical context

**Source:** Phase 6 New Project Folder Plan Review (2025-01-27)

---

## 🚨 Conflict Resolution Examples

### Example 1: Calculation Formula Conflict

**Conflict:** NEPL uses `Amount = Qty × Rate`, Phase 6 uses `Amount = Qty × NetRate`

**Resolution:**
1. Verify: Both preserve calculation functionality ✅
2. Decision: Phase 6 logic adopted (NetRate includes discount)
3. Function Preservation: ✅ Verified - both calculate amounts correctly
4. Test: ✅ Both produce equivalent results
5. Decision ID: P6-DEC-001

**Result:** Phase 6 logic adopted, functionality preserved

---

### Example 2: Table Structure Conflict

**Conflict:** NEPL has `items` table, Phase 6 splits into `l1_intent_lines` + `catalog_skus`

**Resolution:**
1. Verify: All NEPL item functions covered in Phase 6 ✅
2. Decision: Phase 6 structure adopted (L1/L2 split)
3. Function Preservation: ✅ Verified - all item functions work with L1/L2
4. Test: ✅ All item operations work correctly
5. Decision ID: P6-DEC-002

**Result:** Phase 6 structure adopted, functionality preserved through transformation

---

### Example 3: Workflow Conflict

**Conflict:** NEPL workflow is Project → Panel → Feeder → BOM, Phase 6 is Quotation → Panel → BOM

**Resolution:**
1. Verify: All NEPL workflow functions covered in Phase 6 ✅
2. Decision: Phase 6 workflow adopted (quotation-centric)
3. Function Preservation: ✅ Verified - all workflow functions preserved
4. Test: ✅ All workflow operations work correctly
5. Decision ID: P6-DEC-003

**Result:** Phase 6 workflow adopted, functionality preserved

---

## 📊 Decision Authority

### Who Can Make Decisions?

1. **Phase 6 Team Lead:** Day-to-day implementation decisions
2. **Product Owner:** Feature scope and priority decisions
3. **Phase 5 Senate:** Schema and guardrail decisions (requires Phase 5 approval)
4. **Architecture Team:** Technical architecture decisions

### Decision Escalation

- **Low Risk:** Team Lead decision
- **Medium Risk:** Product Owner approval
- **High Risk:** Phase 5 Senate approval required
- **Critical Risk:** Full governance review

---

## ✅ Verification Checklist

Before adopting Phase 6 logic in a conflict:

- [ ] All NEPL functions related to conflict identified
- [ ] Each function verified in Phase 6 design
- [ ] Missing functions added to Phase 6 (if any)
- [ ] Decision documented in Decision Register
- [ ] Function preservation verified
- [ ] Test plan created
- [ ] Tests executed and passed
- [ ] Decision approved by appropriate authority

---

## 🔗 Related Documents

- **Phase 6 Kickoff Charter:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_KICKOFF_CHARTER.md`
- **Phase 6 Execution Plan:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **NEPL Baseline Review:** `PHASE_6_NEPL_BASELINE_REVIEW.md`
- **Decision Register:** `PHASE_6_DECISION_REGISTER.md`
- **Schema Canon:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Data Dictionary:** `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md`

---

**Status:** ACTIVE  
**Last Updated:** 2025-01-27  
**Next Review:** As conflicts arise
