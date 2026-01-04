# Decision Candidates Report

**Generated:** 2025-12-28T00:24:18.716990
**Purpose:** Lists all decision candidates found during extraction, including those not eligible for promotion.

---

## Eligible for Promotion (0)

These decisions are from CANONICAL/LOCKED sources and will be promoted to `02_DECISIONS_LOG.md`:


## Not Eligible (42)

These decisions are from WORKING/DRAFT sources and remain as candidates only:

- **🔐 Why this split is the right decision** from `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md` (Status: WORKING)
  - Excerpt: Governance Benefits
	•	Phase 5 stays clean and defensible
	•	NSW schema is not polluted by legacy mistakes
	•	Migration risk is isolated and optional
...

- **📋 Decision Context** from `docs/PHASE_5/00_GOVERNANCE/SCOPE_SEPARATION.md` (Status: WORKING)
  - Excerpt: **Business Constraints:**
- No business cutover pressure
- No need for full historical continuity
- Willingness to redesign UI
- Clear quality issues ...

- **Decision** from `docs/PHASE_5/00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` (Status: WORKING)
  - Excerpt: Adopt a **Master Data Governance Firewall** as a canonical architecture rule-set:

### 1. No Auto-Create Masters (Hard Constraint)

Runtime code (cont...

- **ADR Decision** from `docs/PHASE_5/00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md` (Status: WORKING)
  - Excerpt: Context: ... Decision: ...

- **Phase 5 Decisions Register** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md` (Status: WORKING)
  - Excerpt: **Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
Record all architectural and design decision...

- **Decision Format** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md` (Status: WORKING)
  - Excerpt: Each decision follows this structure:
- **Decision ID:** D-XXX
- **Date:** YYYY-MM-DD
- **Decision:** Clear statement of what was decided
- **Rational...

- **Decisions** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md` (Status: WORKING)
  - Excerpt: ### D-001: Phase 5 Scope - Analysis Only
**Date:** 2025-12-18  
**Decision:** Phase 5 is limited to canonical data definition and schema design only. ...

- **📋 Decision Context & Rationale** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_EXECUTION_SUMMARY.md` (Status: WORKING)
  - Excerpt: ### Business Constraints
- ✅ No business cutover pressure
- ✅ No need for full historical continuity
- ✅ Willingness to redesign UI
- ✅ Clear quality ...

- **✅ Key Decisions Summary** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_EXECUTION_SUMMARY.md` (Status: WORKING)
  - Excerpt: | Decision | Status | Rationale |
|----------|--------|-----------|
| Phase 5 includes only Step 1 & 2 | ✅ Approved | Clean canonical definition first...

- **Design Decisions (Lock Before Schema Freeze)** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_READINESS_REVIEW_CONSOLIDATED.md` (Status: WORKING)
  - Excerpt: 🟡 **8. Multi-SKU Linkage Strategy**
- **Recommendation:** Use both `parent_line_id` (grouping) + `metadata_json` (flexibility)
- **Status:** Decision ...

- **Decision Capture Required** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_MODE_POLICY.md` (Status: WORKING)
  - Excerpt: **CRITICAL RULE:** Schema and rule changes MUST create Decision Register entry BEFORE making the change.

**What qualifies as a decision:**
- Any chan...

- **Prerequisite-to-Decision Mapping** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_PREREQUISITES_INTEGRATION.md` (Status: WORKING)
  - Excerpt: The following table shows how each prerequisite was integrated through decisions and artifacts:

| Prerequisite | Covered by Decision | Artifact Evide...

- **🎯 Decision Framework: Where Does a File Belong?** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_FILE_ORGANIZATION_POLICY.md` (Status: WORKING)
  - Excerpt: ### Use This Decision Tree:

```
Is this Phase 5 canonical work?
├─ YES → docs/PHASE_5/ (appropriate senate folder)
│   ├─ Governance → 00_GOVERNANCE/...

- **Use This Decision Tree:** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_FILE_ORGANIZATION_POLICY.md` (Status: WORKING)
  - Excerpt: ```
Is this Phase 5 canonical work?
├─ YES → docs/PHASE_5/ (appropriate senate folder)
│   ├─ Governance → 00_GOVERNANCE/
│   ├─ Data Dictionary → 03_...

- **🎯 Decision: Where Does a File Belong?** from `docs/PHASE_5/00_GOVERNANCE/QUICK_REFERENCE_FILE_ORGANIZATION.md` (Status: WORKING)
  - Excerpt: ```
Is this Phase 5 canonical work?
├─ YES → docs/PHASE_5/ (senate folder)
│
├─ NO → Is this legacy analysis?
│   ├─ YES → project/nish/ (keep as-is)
...

- **Phase 5 Decision Summary - Quick Reference** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISION_SUMMARY.md` (Status: WORKING)
  - Excerpt: **Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DECISION REQUIRED  
**Purpose:** Quick decision-making guide for Phase 5 changes

---

## Critic...

- **Quick Decision Matrix** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISION_SUMMARY.md` (Status: WORKING)
  - Excerpt: | Question | Answer |
|----------|--------|
| Does Phase 5 break? | ❌ NO - Only design assumptions tightened |
| Does catalog import change? | ❌ NO - ...

- **3. DECISION_CAPTURE_RULES.md** from `docs/PHASE_5/00_GOVERNANCE/EXPLORATION_MODE_SETUP_SUMMARY.md` (Status: WORKING)
  - Excerpt: - Defines what qualifies as a decision
- Specifies required fields for decision entries
- Documents decision capture process
- Provides examples and t...

- **PHASE_5_DECISIONS_REGISTER.md** from `docs/PHASE_5/00_GOVERNANCE/EXPLORATION_MODE_SETUP_SUMMARY.md` (Status: WORKING)
  - Excerpt: - Added D-008: Exploration Mode Policy decision
- Documents rationale for open-gate exploration approach...

- **Decision Capture Rules** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: **Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose

Define what qualifies as a "decision" durin...

- **What Qualifies as a Decision?** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: A decision is any change or choice that:

1. **Modifies canonical outputs:**
   - Changes to `NSW_SCHEMA_CANON_v1.0.md` (tables, fields, relationships...

- **What Does NOT Qualify as a Decision?** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: - **Documentation clarifications:** Adding examples, improving explanations, fixing typos
- **Formatting changes:** Reorganizing sections, improving r...

- **Required Fields for Each Decision** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: ### Core Fields (Required)

| Field | Description | Example |
|-------|-------------|---------|
| **Decision ID** | Unique identifier (D-###) | D-008 ...

- **Decision Capture Process** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: ### Step 1: Identify Decision

When making a change, ask:
- Does this modify canonical outputs?
- Does this establish or change a rule?
- Does this di...

- **Step 1: Identify Decision** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: When making a change, ask:
- Does this modify canonical outputs?
- Does this establish or change a rule?
- Does this diverge from baseline?
- Does thi...

- **Step 2: Create Decision Entry** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: 1. Get next Decision ID from `PHASE_5_DECISIONS_REGISTER.md`
2. Fill in all required fields
3. Cite Fundamentals baseline (even if diverging)
4. Link ...

- **Decision Status Lifecycle** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: ```
NEW (discovered)
  ↓
PENDING (under evaluation)
  ↓
APPROVED (decision made, change implemented)
  ↓
SUPERSEDED (replaced by new decision)
```

--...

- **Example 1: Schema Change Decision** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: **Decision ID:** D-008  
**Date:** 2025-01-27  
**Decision:** Add `import_batch_id` to `products` table for import governance  
**Rationale:** Enables...

- **Example 2: Divergence Decision** from `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md` (Status: WORKING)
  - Excerpt: **Decision ID:** D-009  
**Date:** 2025-01-27  
**Decision:** Use `customer_name` (text) + optional `customer_id` (FK) instead of mandatory `customer_...

- **Legacy → Canonical Decisions** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_COMPLETE_ALIGNMENT_SUMMARY.md` (Status: WORKING)
  - Excerpt: ```
project/nish/ (read-only)
    ↓
Legacy Review (what not to do)
    ↓
Legacy-to-Canonical Mapping
    ↓
Canonical Decisions (Data Dictionary + Sche...

- **A8. Design Decision: Multi-SKU Linkage** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_TASK_LIST.md` (Status: WORKING)
  - Excerpt: - [ ] **A8.1:** Lock decision: Use `parent_line_id` + `metadata_json` (both)
- [ ] **A8.2:** Verify/add `quote_bom_items.parent_line_id` to schema DDL...

- **A9. Design Decision: Customer Normalization** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_TASK_LIST.md` (Status: WORKING)
  - Excerpt: - [ ] **A9.1:** Lock decision: `customer_name` (text, snapshot) + `customer_id` (optional FK, nullable)
- [ ] **A9.2:** Verify `quotations.customer_na...

- **A10. Design Decision: Resolution Level Constraints** from `docs/PHASE_5/00_GOVERNANCE/PHASE_5_TASK_LIST.md` (Status: WORKING)
  - Excerpt: - [ ] **A10.1:** Lock decision: L0/L1/L2 allowed at all levels with explicit rules
- [ ] **A10.2:** Verify `master_bom_items.resolution_level` exists
...

- **2.4 Import Decision Logging** from `docs/PHASE_5/00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md` (Status: WORKING)
  - Excerpt: **Table:** `import_decision_log`

**Purpose:** Audit trail of all import decisions (accept/reject/queue)

**Columns:**
- `DecisionId` (PK)
- `ImportRu...

- **B) Decision Closure** from `docs/PHASE_5/00_GOVERNANCE/STABILIZATION_EXIT_CRITERIA.md` (Status: WORKING)
  - Excerpt: **Criterion:** All items in `02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` sections 1–8 are ✅ VERIFIED, and all "PENDING" design decisions are resol...

- **Knowledge Base Decision Document** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md` (Status: WORKING)
  - Excerpt: **Status:** REVIEW_REQUIRED  
**Date:** 2025-01-XX  
**Purpose:** Single authoritative reference for Schneider catalog (Page 8 to End) interpretation,...

- **6. Final Decision Rules (Frozen)** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md` (Status: WORKING)
  - Excerpt: ### 🔒 Rule 1: Pole Count → SC_L1

Pole count belongs to SC_L1 (Construction). It defines physical construction, not rating.

---

### 🔒 Rule 2: AC1 / ...

- **Engineering Decision Documentation** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/README.md` (Status: WORKING)
  - Excerpt: **Purpose:** Capture engineering decisions, rules, and interpretations before they are finalized and moved to working folders.

**Workflow:**
1. **Dec...

- **All Engineering Decision Documents** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/INDEX.md` (Status: WORKING)
  - Excerpt: **Last Updated:** 2025-01-XX

---...

- **Voltage Mapping Decisions** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/INDEX.md` (Status: WORKING)
  - Excerpt: *(To be added)*...

- **Knowledge Base Decision Document** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.2.md` (Status: WORKING)
  - Excerpt: **Status:** LOCKED – ENGINEERING CONSISTENT (v1.2)  
**Date:** 2025-01-XX  
**Purpose:** Single authoritative reference for Schneider catalog (Page 8 ...

- **6. Final Decision Rules (Frozen)** from `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.2.md` (Status: WORKING)
  - Excerpt: ### 🔒 Rule 1: Pole Count → SC_L1

Pole count belongs to SC_L1 (Construction). It defines physical construction, not rating.

---

### 🔒 Rule 2: AC1 / ...


---

**Note:** Non-eligible decisions can be promoted after their source documents are promoted to CANONICAL status.
