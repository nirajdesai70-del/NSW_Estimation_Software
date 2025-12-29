# Phase 5 Pre-Implementation Open Points Review

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Purpose:** Comprehensive review of all open points that must be resolved before Phase 5 implementation begins

---

## 📋 Executive Summary

This document consolidates all open points, pending items, and blockers identified across multiple work sessions and agents. It provides a clear action plan for closing these points before Phase 5 implementation.

**Key Finding:** Phase 5 design work is largely complete, but several freeze gate verification items and design decisions need to be finalized before implementation can begin.

---

## 🎯 Work Done Summary

### Phase 5 Design Work Completed

1. ✅ **Data Dictionary v1.0** - FROZEN (`NSW_DATA_DICTIONARY_v1.0.md`)
   - Entity definitions complete
   - Business rules documented
   - Validation guardrails G1-G8 defined
   - Module ownership matrix complete
   - Naming conventions frozen

2. ✅ **Schema Canon v1.0** - FREEZE-READY (`NSW_SCHEMA_CANON_v1.0.md`)
   - Complete DDL ready
   - All tables defined
   - Relationships mapped
   - Constraints documented

3. ✅ **Governance Documents** - CANONICAL
   - Phase 5 Charter
   - Scope Separation Policy
   - Legacy vs NSW Coexistence Policy
   - UI Context Classification Policy
   - Master Data Governance Rules

4. ✅ **Prerequisites Integration** - COMPLETE
   - All 6 prerequisites tracked and applied via Pending Inputs Register
   - Decision coverage proven
   - Fundamentals baseline established

5. ✅ **Validation Guardrails** - FROZEN (G1-G8)
   - All 8 guardrails documented and frozen
   - Enforcement layers specified

---

## ⚠️ Open Points That Must Be Closed

### Category A: Freeze Gate Verification Items

These items are **BLOCKING** SPEC-5 v1.0 freeze according to `SPEC_5_FREEZE_GATE_CHECKLIST.md`.

#### A1. BOM Tracking Fields Verification ⏳ PENDING

**Status:** Needs verification against schema DDL

**Required Verification:**
- [ ] `quote_boms.origin_master_bom_id` - Verify FK exists
- [ ] `quote_boms.origin_master_bom_version` - Verify field exists
- [ ] `quote_boms.instance_sequence_no` - Verify field exists
- [ ] `quote_boms.is_modified` - Verify boolean field exists
- [ ] `quote_boms.modified_by` - Verify FK exists
- [ ] `quote_boms.modified_at` - Verify timestamp exists

**Action Required:**
1. Review `NSW_SCHEMA_CANON_v1.0.md` Section "quote_boms" table
2. Verify all fields exist in schema DDL
3. Update compliance matrix in `SPEC_5_FREEZE_GATE_CHECKLIST.md`

**Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` Section 1

**Impact:** BLOCKING - Cannot freeze schema without verification

---

#### A2. IsLocked Scope - Already Resolved ✅

**Status:** ✅ VERIFIED - D-005 APPROVED

**Decision:** Locking applies at line-item level only (`quote_bom_items.is_locked`) for MVP

**Evidence:**
- D-005 in Decision Register: APPROVED
- Documented in `LOCKING_POLICY.md`
- Schema includes only `quote_bom_items.is_locked` field

**Action:** ✅ No action needed - Already resolved

---

#### A3. CostHead System Verification ⏳ PARTIALLY COMPLETE

**Status:** Resolution order documented, but schema verification needed

**Completed:**
- ✅ CostHead resolution order documented in `COSTHEAD_RULES.md`
- ✅ D-006 APPROVED: `products.cost_head_id` added for defaults
- ✅ Resolution precedence: item → product → system default

**Required Verification:**
- [ ] Verify `cost_heads` table exists in schema DDL
- [ ] Verify `quote_bom_items.cost_head_id` FK exists
- [ ] Verify `products.cost_head_id` FK exists (from D-006)

**Action Required:**
1. Review `NSW_SCHEMA_CANON_v1.0.md` for cost_heads table
2. Verify FKs exist in schema DDL
3. Update compliance matrix

**Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` Section 3

**Impact:** BLOCKING - Must verify before freeze

---

#### A4. Validation Guardrails G1-G8 ✅ COMPLETE

**Status:** ✅ FROZEN

**Evidence:**
- All 8 guardrails documented in `VALIDATION_GUARDRAILS_G1_G7.md`
- G8 (L1-SKU reuse) added and frozen
- Enforcement layers specified

**Action:** ✅ No action needed - Complete

---

#### A5. AI Scope Declaration ✅ COMPLETE

**Status:** ✅ VERIFIED

**Decision:** Phase-5 = Schema reservation only, Post-Phase-5 = Implementation

**Evidence:**
- Documented in `NSW_DATA_DICTIONARY_v1.0.md` Section "6. AI Scope Declaration"
- `ai_call_logs` table exists in schema

**Action:** ✅ No action needed - Complete

---

#### A6. Module Ownership Matrix ✅ COMPLETE

**Status:** ✅ VERIFIED

**Evidence:**
- Complete mapping in `MODULE_OWNERSHIP_MATRIX.md`
- All tables mapped to owner modules

**Action:** ✅ No action needed - Complete

---

#### A7. Naming Conventions ✅ COMPLETE

**Status:** ✅ FROZEN

**Evidence:**
- Complete standards in `NAMING_CONVENTIONS.md`
- All conventions documented

**Action:** ✅ No action needed - Complete

---

#### A8. Design Decisions - Multi-SKU Linkage ✅ COMPLETE

**Status:** ✅ LOCKED - D-007 APPROVED

**Decision:** Use both `parent_line_id` + `metadata_json`

**Evidence:**
- D-007 in Decision Register: APPROVED
- Schema includes both fields

**Action:** ✅ No action needed - Complete

---

#### A9. Design Decision - Customer Normalization ⏳ PENDING

**Status:** ⏳ NEEDS DECISION

**Required Decision:**
- Lock approach: `customer_name` (text, snapshot) + `customer_id` (optional FK, nullable)

**Recommended Approach (from SPEC_5_FREEZE_RECOMMENDATIONS.md):**
- Keep `quotations.customer_name` as display snapshot
- Add `quotations.customer_id` FK as optional (nullable)

**Required Actions:**
1. [ ] Create Decision Register entry (D-009 or similar)
2. [ ] Review and approve decision
3. [ ] Verify/add `quotations.customer_id` to schema DDL if not present
4. [ ] Verify `customers` table exists
5. [ ] Document decision rationale

**Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_RECOMMENDATIONS.md` Section "Step C: Lock 3 Design Decisions" item 2

**Impact:** BLOCKING - Schema freeze requires locked decision

**Estimated Effort:** 1-2 hours (decision + schema verification)

---

#### A10. Design Decision - Resolution Level Constraints ⏳ PENDING

**Status:** ⏳ NEEDS DECISION LOCK

**Required Decision:**
- Lock rules: L0/L1/L2 allowed at all levels with explicit rules
- MBOM rules: L0/L1/L2 if product_id rules respected
- QUO rules: L0/L1/L2 if pricing + locking rules respected

**Required Actions:**
1. [ ] Verify `master_bom_items.resolution_level` exists in schema
2. [ ] Verify/add `quote_bom_items.resolution_level` to schema DDL
3. [ ] Create Decision Register entry if needed
4. [ ] Document explicit rules in Data Dictionary
5. [ ] Add constraints documentation

**Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_RECOMMENDATIONS.md` Section "Step C: Lock 3 Design Decisions" item 3

**Impact:** BLOCKING - Schema freeze requires locked decision

**Estimated Effort:** 2-3 hours (verification + documentation)

---

### Category B: Pending Inputs Register Items

#### PI-007: Fundamentals Gap Analysis Integration ⏳ IN REVIEW

**Status:** ⏳ IN_REVIEW (per PENDING_INPUTS_REGISTER.md)

**Source:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`

**What It Influences:** dictionary, schema, alignment

**Required Actions:**
1. [ ] Review gap analysis document
2. [ ] Address gaps through decisions or documentation updates
3. [ ] Update Pending Inputs Register status (IN_REVIEW → APPLIED or REJECTED)
4. [ ] Link to Decision Register entries if decisions made

**Source:** `docs/PHASE_5/00_GOVERNANCE/PENDING_INPUTS_REGISTER.md` PI-007

**Impact:** MEDIUM - Should be addressed before Phase 5 execution

**Estimated Effort:** 4-6 hours (review + address gaps)

---

### Category C: Documentation Completeness

#### C1. Freeze Gate Compliance Matrix ⏳ NEEDS COMPLETION

**Status:** ⏳ Partial completion needed

**Required Actions:**
1. [ ] Complete verification of all items in `SPEC_5_FREEZE_GATE_CHECKLIST.md`
2. [ ] Mark all items as ✅ VERIFIED or document exceptions
3. [ ] Get compliance matrix approval

**Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md`

**Impact:** BLOCKING - Required for SPEC-5 v1.0 freeze

**Estimated Effort:** 3-4 hours (verification + documentation)

---

#### C2. SPEC-5 Documentation Patching ⏳ PENDING

**Status:** ⏳ Needs completion after freeze gate verification

**Required Actions:**
1. [ ] Add missing sections to SPEC-5 (if any identified during verification)
2. [ ] Update compliance matrix with final status
3. [ ] Patch SPEC-5 with all governance sections (if needed)

**Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_RECOMMENDATIONS.md` Section "Step D: Patch SPEC-5"

**Impact:** BLOCKING - Required for freeze

**Estimated Effort:** 2-3 hours (documentation updates)

---

## 📊 Open Points Summary Table

| ID | Category | Item | Status | Impact | Effort | Action Required |
|----|----------|------|--------|--------|--------|-----------------|
| A1 | Freeze Gate | BOM Tracking Fields Verification | ⏳ PENDING | BLOCKING | 1-2h | Verify schema DDL |
| A3 | Freeze Gate | CostHead Schema Verification | ⏳ PENDING | BLOCKING | 1h | Verify schema DDL |
| A9 | Freeze Gate | Customer Normalization Decision | ⏳ PENDING | BLOCKING | 1-2h | Lock decision + verify schema |
| A10 | Freeze Gate | Resolution Level Constraints | ⏳ PENDING | BLOCKING | 2-3h | Verify schema + document rules |
| PI-007 | Pending Inputs | Fundamentals Gap Analysis | ⏳ IN_REVIEW | MEDIUM | 4-6h | Review + address gaps |
| C1 | Documentation | Freeze Gate Compliance Matrix | ⏳ PENDING | BLOCKING | 3-4h | Complete verification |
| C2 | Documentation | SPEC-5 Documentation Patching | ⏳ PENDING | BLOCKING | 2-3h | Patch documentation |

**Total Estimated Effort:** 14-21 hours

---

## 🎯 Priority Order for Closure

### Priority 1: BLOCKING Items (Must Complete Before Freeze)

1. **A9 + A10: Lock Design Decisions** (2-4 hours)
   - Customer normalization decision
   - Resolution level constraints verification
   - These unlock schema freeze

2. **A1 + A3: Schema Field Verification** (2-3 hours)
   - BOM tracking fields verification
   - CostHead system verification
   - Quick verification tasks

3. **C1: Complete Compliance Matrix** (3-4 hours)
   - Final verification of all items
   - Mark status in checklist
   - Get approval

4. **C2: Patch SPEC-5 Documentation** (2-3 hours)
   - Add any missing governance sections
   - Update compliance matrix
   - Final documentation polish

### Priority 2: MEDIUM Priority (Should Complete Before Execution)

5. **PI-007: Fundamentals Gap Analysis** (4-6 hours)
   - Review gap analysis
   - Address gaps through decisions
   - Update Pending Inputs Register

---

## ✅ Action Plan to Close Open Points

### Step 1: Schema Field Verification (2-3 hours)

**Tasks:**
1. Open `NSW_SCHEMA_CANON_v1.0.md`
2. Verify BOM tracking fields (A1):
   - Search for `quote_boms` table definition
   - Verify: `origin_master_bom_id`, `origin_master_bom_version`, `instance_sequence_no`, `is_modified`, `modified_by`, `modified_at`
   - Update compliance matrix status
3. Verify CostHead fields (A3):
   - Search for `cost_heads` table
   - Verify: `quote_bom_items.cost_head_id`, `products.cost_head_id`
   - Update compliance matrix status

**Deliverable:** Updated compliance matrix with verification status

---

### Step 2: Lock Remaining Design Decisions (3-5 hours)

**Tasks:**

#### A9: Customer Normalization Decision
1. Review `SPEC_5_FREEZE_RECOMMENDATIONS.md` recommendation
2. Create Decision Register entry (D-009 or next available)
3. Document decision: `customer_name` (text) + `customer_id` (nullable FK)
4. Verify `quotations.customer_id` exists in schema DDL
5. Verify `customers` table exists
6. Update Decision Register with schema references

#### A10: Resolution Level Constraints
1. Verify `master_bom_items.resolution_level` exists in schema
2. Verify `quote_bom_items.resolution_level` exists in schema
3. Review existing rules documentation
4. Create/update Decision Register entry if needed
5. Document explicit MBOM and QUO rules
6. Add constraints documentation to Data Dictionary

**Deliverable:** Decision Register entries with schema verification

---

### Step 3: Complete Compliance Matrix (3-4 hours)

**Tasks:**
1. Open `SPEC_5_FREEZE_GATE_CHECKLIST.md`
2. For each item in compliance matrix:
   - Verify status from Step 1 and Step 2
   - Mark as ✅ VERIFIED or document exception
   - Add verification notes
3. Review all sections:
   - BOM Tracking Fields (Section 1)
   - IsLocked Fields (Section 2) - Already verified
   - CostHead System (Section 3)
   - Validation Guardrails (Section 4) - Already complete
   - AI Entities (Section 5) - Already verified
   - Module Ownership (Section 6) - Already complete
   - Naming Conventions (Section 7) - Already complete
   - Design Decisions (Section 8)
4. Get approval for compliance matrix

**Deliverable:** Completed compliance matrix with all items verified

---

### Step 4: Patch SPEC-5 Documentation (2-3 hours)

**Tasks:**
1. Review `SPEC_5_FREEZE_RECOMMENDATIONS.md` Section "Step D"
2. Identify any missing governance sections
3. Patch SPEC-5 with missing sections (if any):
   - Validation Guardrails section (already documented separately)
   - Module Ownership Matrix (already documented separately)
   - Naming Conventions (already documented separately)
   - Ensure all sections are linked/referenced
4. Update compliance matrix final status
5. Final documentation review

**Deliverable:** SPEC-5 v1.0 ready for freeze

---

### Step 5: Review Fundamentals Gap Analysis (4-6 hours) - OPTIONAL PRIORITY

**Tasks:**
1. Open `FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`
2. Review all identified gaps
3. For each gap:
   - Determine if already addressed in Phase 5 design
   - If not addressed, create decision or documentation update
   - Link to Decision Register if decision made
4. Update PENDING_INPUTS_REGISTER.md:
   - Change PI-007 status from IN_REVIEW to APPLIED or REJECTED
   - Add decision links
   - Add notes

**Deliverable:** PI-007 resolved, Pending Inputs Register updated

---

## 📝 Required Inputs for Closing Open Points

### Internal Inputs (Available in Repository) ✅

#### Input 1: Schema Canon Document Access
- **Source:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- **Purpose:** Verify field existence for A1, A3, A9, A10
- **Availability:** ✅ Available (internal)

#### Input 2: Freeze Gate Checklist
- **Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md`
- **Purpose:** Guide verification process (C1)
- **Availability:** ✅ Available (internal)

#### Input 3: Freeze Recommendations
- **Source:** `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_RECOMMENDATIONS.md`
- **Purpose:** Guide design decisions (A9, A10) - **RECOMMENDATIONS PROVIDED**
- **Availability:** ✅ Available (internal, recommendations included)

#### Input 4: Fundamentals Gap Analysis
- **Source:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`
- **Purpose:** Review gaps (PI-007)
- **Availability:** ✅ Available (internal)

#### Input 5: Decision Register Template
- **Source:** `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md`
- **Purpose:** Create new decisions (A9, A10)
- **Availability:** ✅ Available (internal)

#### Input 6: Pending Inputs Register
- **Source:** `docs/PHASE_5/00_GOVERNANCE/PENDING_INPUTS_REGISTER.md`
- **Purpose:** Update PI-007 status
- **Availability:** ✅ Available (internal)

---

### External Inputs Required ⚠️

#### External Input 1: Design Decision Approval (A9, A10) ⚠️ **MINIMAL EXTERNAL INPUT**

**What's Needed:**
- For **A9 (Customer Normalization):** Recommendation already provided - just needs approval
  - Recommendation: `customer_name` (text) + `customer_id` (nullable FK)
  - This is a technical design decision - can proceed with recommendation if no business objection

- For **A10 (Resolution Level Constraints):** Rules already documented - just needs verification
  - Rules are technical constraints - verification only, no business input needed

**Who Provides Input:**
- **Architecture:** Approve technical decisions (recommendations already exist)
- **Execution Team:** Approve feasibility (should be straightforward)

**Action Required:**
- Create Decision Register entries (D-009, D-010)
- Get Architecture + Execution Team approval (30 min review)

**Estimated External Time:** 30 minutes (review/approval only)

---

#### External Input 2: Compliance Matrix Approval (C1) ⚠️ **REQUIRED**

**What's Needed:**
- Approval of completed compliance matrix verification
- Confirmation that all items are verified correctly

**Who Provides Input:**
- **Architecture:** Approve verification completeness
- **Execution Team:** Approve verification accuracy
- **Governance:** Approve scope compliance

**Action Required:**
- Complete internal verification first (3-4 hours internal work)
- Present completed matrix for approval (1 hour review meeting)

**Estimated External Time:** 1 hour (review meeting)

---

#### External Input 3: Final SPEC-5 v1.0 Freeze Approval ⚠️ **REQUIRED**

**What's Needed:**
- Final approval to freeze SPEC-5 v1.0 as canonical specification
- Approval that all freeze gate criteria are met

**Who Provides Input:**
- **Architecture:** Final architecture approval
- **Execution Team:** Final execution feasibility approval
- **Governance:** Final scope compliance approval
- **Stakeholders:** Final business sign-off

**Action Required:**
- Complete all internal work first (all steps 1-4)
- Present complete SPEC-5 v1.0 for final freeze approval

**Estimated External Time:** 1-2 hours (final review meeting)

---

## 🔍 External Input Summary

| External Input | Type | Who | When | Time Required | Can Proceed Without? |
|----------------|------|-----|------|---------------|---------------------|
| Design Decision Approval (A9, A10) | Approval | Architecture + Execution | After Step 2 | 30 min | ❌ No (blocking) |
| Compliance Matrix Approval (C1) | Approval | Architecture + Execution + Governance | After Step 3 | 1 hour | ❌ No (blocking) |
| Final SPEC-5 Freeze Approval | Approval | All stakeholders | After Step 4 | 1-2 hours | ❌ No (blocking) |

**Total External Time Required:** 2.5 - 3.5 hours

**Key Point:** All recommendations and decisions are already provided in documentation. External input is primarily **approval/review** rather than **decision-making**. The technical team can proceed with recommendations and present for approval.

---

## ✅ Success Criteria

Phase 5 is ready for implementation when:

1. ✅ All BLOCKING items (A1, A3, A9, A10, C1, C2) are complete
2. ✅ Compliance matrix shows all items as ✅ VERIFIED
3. ✅ All design decisions are locked (Decision Register entries approved)
4. ✅ SPEC-5 v1.0 documentation is complete and patched
5. ✅ Freeze approval obtained for SPEC-5 v1.0
6. ⚠️ PI-007 resolved (recommended, not blocking)

---

## 🔗 Related Documents

- `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_GATE_CHECKLIST.md` - Compliance matrix
- `docs/PHASE_5/02_FREEZE_GATE/SPEC_5_FREEZE_RECOMMENDATIONS.md` - Freeze recommendations
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` - Schema DDL
- `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md` - Decision Register
- `docs/PHASE_5/00_GOVERNANCE/PENDING_INPUTS_REGISTER.md` - Pending Inputs
- `docs/PHASE_5/03_DATA_DICTIONARY/NSW_DATA_DICTIONARY_v1.0.md` - Data Dictionary
- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md` - Gap Analysis

---

## 📌 Next Steps

### Internal Work (Can Proceed Immediately)

1. **Immediate:** Begin Step 1 (Schema Field Verification) - 2-3 hours
   - ✅ No external input needed - pure verification work

2. **Next:** Complete Step 2 (Lock Design Decisions) - 3-5 hours
   - ✅ Can use existing recommendations
   - ⚠️ Need external approval (30 min) - can schedule after completion

3. **Then:** Complete Step 3 (Compliance Matrix) - 3-4 hours
   - ✅ No external input needed for verification
   - ⚠️ Need external approval (1 hour) - can schedule after completion

4. **Finally:** Complete Step 4 (Documentation Patching) - 2-3 hours
   - ✅ No external input needed - documentation work

5. **Optional:** Complete Step 5 (Gap Analysis Review) - 4-6 hours
   - ✅ No external input needed - internal review

### External Approval Required (Schedule After Internal Work)

- **Step 2 Approval:** Design decisions (A9, A10) - 30 minutes
- **Step 3 Approval:** Compliance matrix - 1 hour  
- **Final Freeze Approval:** SPEC-5 v1.0 freeze - 1-2 hours

**Total Internal Time:** 10-15 hours  
**Total External Approval Time:** 2.5-3.5 hours  
**Total Time to Close:** 12.5-18.5 hours

**After completion:** SPEC-5 v1.0 can be frozen and Phase 5 implementation can begin.

---

## ✅ Can Work Proceed Without External Input?

**Answer: YES, for internal work. NO, for final approvals.**

**Internal Work (Steps 1-4):** ✅ Can proceed immediately
- All documentation is available
- Recommendations are provided
- Technical verification can be done independently

**External Approvals:** ⚠️ Required, but can be scheduled after internal work
- Approvals are review-based (not decision-making)
- Can prepare all materials first, then schedule approval meetings
- Recommendations exist, so approvals should be straightforward

---

**Document Status:** ✅ CANONICAL  
**Last Updated:** 2025-01-27  
**Next Review:** After open points are closed  
**Owner:** Phase 5 Governance Team

