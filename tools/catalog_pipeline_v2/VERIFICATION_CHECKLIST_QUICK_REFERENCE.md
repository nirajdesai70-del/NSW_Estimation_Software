# Verification Checklist - Quick Reference

**Version:** 2.1  
**Quick Reference:** For detailed instructions, see `STANDING_VERIFICATION_INSTRUCTION.md` (v2.1)  
**Purpose:** Fast checklist for **DUAL verification** of each build/feature:
- **Track A:** Legacy Business-Decision Reference Audit (`project/nish/`) - Blocking only for RETAIN items
- **Track B:** NSW Fundamental Alignment Plan (`NSW Fundamental Alignment Plan/`) - Always mandatory and blocking

---

## 🚀 Quick Start Checklist (Dual Verification)

### TRACK A: Legacy Business-Decision Reference Audit (~15-20 min)

**Purpose:** Ensure no critical business decision from legacy is missed.  
**NOT for:** Data migration, schema parity, table alignment, or technical comparison.

#### Step A1: Identify Legacy Business Decisions (5 min)

- [ ] Check `TRACK_A_RETAIN_REGISTER.md` for existing RETAIN decisions
- [ ] Identify relevant legacy area(s) in `project/nish/`
- [ ] Extract business decisions only (quotation lifecycle, pricing, locking, audit)
- [ ] Ignore legacy DB schema, code structure, and UI layouts
- [ ] **If no legacy decisions found → Track A = N/A, auto-PASS**
- [ ] **If new RETAIN discovered → add to RETAIN register**

#### Step A2: Tag Each Decision (5-10 min)

- [ ] Tag each decision: **RETAIN** (blocking) / **REPLACE** (non-blocking) / **DROP** (non-blocking)
- [ ] If not tagged → treated as REPLACE by default
- [ ] Use `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md`

#### Step A3: Validate RETAIN Items (Blocking Check) (5 min)

- [ ] For each RETAIN decision: confirm exists in new build
- [ ] Evidence recorded (API, workflow, rule, config)
- [ ] If any RETAIN item is missing → BUILD BLOCKED

#### Step A4: Document Non-Blocking Items (5 min)

- [ ] REPLACE decisions documented with brief rationale
- [ ] DROP decisions documented with brief justification

### TRACK B: NSW Fundamental Alignment Plan Verification (~30 min)

#### Step B1: Fundamentals Alignment (10 min)

- [ ] Review `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- [ ] Verify L0/L1/L2 compliance per `02_GOVERNANCE/NEPL_CANONICAL_RULES.md`
- [ ] Check governance standards per `02_GOVERNANCE/NEPL_CUMULATIVE_VERIFICATION_STANDARD.md`

#### Step B2: Design Document & Gap Register Check (15 min)

- [ ] Review relevant design docs in `05_DESIGN_DOCUMENTS/`
- [ ] Check gap registers: `02_GOVERNANCE/BOM_GAP_REGISTER.md`
- [ ] Verify related gaps are addressed
- [ ] Run verification queries from `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md`

#### Step B3: Standards Compliance (5 min)

- [ ] Complete verification checklist: `07_VERIFICATION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md`
- [ ] Verify Phase 4/4.5 requirements

### COMBINED: Documentation & Sign-off (10 min)

- [ ] Complete verification report (both tracks)
- [ ] Complete Track A worksheet (RETAIN/REPLACE/DROP)
- [ ] Document any conflicts (Track B wins)
- [ ] Update build ticket with verification status

**Total Time:** ~55-60 minutes per build/feature (both tracks)

---

## 📋 Detailed Checklist

### Pre-Verification (Both Tracks)

#### Track A: Legacy Business Decisions
- [ ] Legacy reference identified: `project/nish/` [component path]
- [ ] Business decisions extracted (not schema/code)
- [ ] Track A worksheet ready: `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md`

#### Track B: NSW Fundamentals
- [ ] NSW Fundamentals docs identified: `NSW Fundamental Alignment Plan/` [relevant paths]
- [ ] Master Fundamentals reviewed
- [ ] Design documents identified
- [ ] Gap registers checked

### TRACK A: Legacy Business-Decision Reference Audit

#### RETAIN Items (Blocking)

- [ ] RETAIN item 1: [Business decision] - Evidence: [API/logic/workflow] - Status: ✅ SATISFIED / ❌ MISSING
- [ ] RETAIN item 2: [Business decision] - Evidence: [API/logic/workflow] - Status: ✅ SATISFIED / ❌ MISSING
- [ ] RETAIN item 3: [Business decision] - Evidence: [API/logic/workflow] - Status: ✅ SATISFIED / ❌ MISSING
- [ ] ... (add more as needed)
- [ ] **Rule:** If any RETAIN item is MISSING → BUILD BLOCKED

#### REPLACE Items (Non-blocking)

- [ ] REPLACE item 1: [Business decision] - New approach: [Implementation] - Notes: [Rationale]
- [ ] REPLACE item 2: [Business decision] - New approach: [Implementation] - Notes: [Rationale]
- [ ] ... (add more as needed)

#### DROP Items (Non-blocking)

- [ ] DROP item 1: [Business decision] - Rationale: [Justification]
- [ ] DROP item 2: [Business decision] - Rationale: [Justification]
- [ ] ... (add more as needed)

#### Track A Tagging Quick Reference

- **🔴 RETAIN** → blocking (must exist in new system)
- **🟡 REPLACE** → note only (handled differently/improved)
- **⚪ DROP** → note only (intentionally removed)

### TRACK B: NSW Fundamental Alignment Plan Verification

#### Fundamentals Alignment

- [ ] Master Fundamentals v2.0 compliance: ✅ / ⚠️ / ❌
- [ ] L0/L1/L2 canonical rules compliance: ✅ / ⚠️ / ❌
- [ ] Governance standards compliance: ✅ / ⚠️ / ❌
- [ ] 9-layer compliance (A-I): ✅ / ⚠️ / ❌

#### Design Document Alignment

- [ ] Component design reviewed: ✅ / ❌
- [ ] Implementation matches design: ✅ / ⚠️ / ❌
- [ ] Architecture patterns followed: ✅ / ⚠️ / ❌

#### Gap Register Verification

- [ ] Gap register reviewed: ✅ / ❌
- [ ] Related gaps addressed: ✅ / ⚠️ / ❌
- [ ] Gap closures documented: ✅ / ❌

#### Verification Queries & Checklists

- [ ] Verification queries run: ✅ / ❌
- [ ] Verification checklist completed: ✅ / ❌
- [ ] Phase 4/4.5 requirements met: ✅ / ⚠️ / ❌

### COMBINED: Standards Compliance

- [ ] Architecture: ✅ Compliant / ⚠️ Deviation / ❌ Non-compliant (Track B + New)
- [ ] Database Schema: ✅ Compliant / ⚠️ Deviation / ❌ Non-compliant (Track B + Phase 5)
- [ ] API Design: ✅ Compliant / ⚠️ Deviation / ❌ Non-compliant (Track B + New)
- [ ] Code Organization: ✅ Compliant / ⚠️ Deviation / ❌ Non-compliant (Track B + New)
- [ ] Testing: ✅ Compliant / ⚠️ Deviation / ❌ Non-compliant (Track B + New)
- [ ] Documentation: ✅ Compliant / ⚠️ Deviation / ❌ Non-compliant (Track B + New)

### Final Verification

- [ ] Verification report completed
- [ ] All action items created
- [ ] Sign-off obtained
- [ ] Build ticket updated

---

## ⚠️ Red Flags (Block Build)

Stop and fix if you find:

### Track A (Legacy Business Decisions)
- ❌ RETAIN-tagged business decision missing (blocking)
- ❌ RETAIN items not properly validated

### Track B (NSW Fundamentals)
- ❌ Master Fundamentals non-compliance
- ❌ L0/L1/L2 canonical rules violation
- ❌ Governance standards violation
- ❌ Critical gap not addressed
- ❌ Design document misalignment

### Combined
- ❌ Major standards non-compliance
- ❌ Missing documentation
- ❌ Conflicts between Track A and Track B

---

## ✅ Pass Criteria

Build/feature passes verification when **BOTH tracks pass**:

### Track A (Legacy Business Decisions)
- ✅ All RETAIN items satisfied
- ✅ REPLACE/DROP items documented
- ✅ Track A worksheet completed

### Track B (NSW Fundamentals)
- ✅ Master Fundamentals compliance verified
- ✅ Canonical rules compliance verified
- ✅ Governance standards compliance verified
- ✅ Design document alignment verified
- ✅ Related gaps addressed
- ✅ Verification queries passed

### Combined
- ✅ Standards compliance verified
- ✅ Verification report complete (both tracks)
- ✅ No conflicts between tracks
- ✅ Approved by reviewer

---

## 📝 Quick Verification Report Template

```markdown
# Verification Report: [Build/Feature Name]

**Date:** [Date]  
**Verifier:** [Name]  
**Legacy Reference:** [Path in project/nish/]  
**NSW Fundamentals Reference:** [Path in NSW Fundamental Alignment Plan/]

## Summary
- Overall Status: ✅ PASS / ⚠️ PASS WITH NOTES / ❌ FAIL
- Track A (Legacy Business Decisions) Status: ✅ / ⚠️ / ❌
- Track B (NSW Fundamentals) Status: ✅ / ⚠️ / ❌
- RETAIN Items: [Number satisfied / Number total]
- Standards: ✅ / ⚠️ / ❌

## Track A: Legacy Business-Decision Reference Audit (v2.1)
- RETAIN Items: [Number satisfied / Number total]
- REPLACE Items: [Number documented]
- DROP Items: [Number documented]
- Track A Worksheet: [Link/completed]

## Track B: NSW Fundamentals Verification
- Fundamentals Alignment: [Status]
- Design Documents: [Status]
- Gap Registers: [Status]
- Verification Queries: [Status]

## Key Findings
1. [Finding 1 - Track A]
2. [Finding 2 - Track B]
3. [Finding 3 - Combined]

## Action Items
- [ ] [Action 1]
- [ ] [Action 2]

## Sign-off
- Verified By: [Name]
- Date: [Date]
- Status: ✅ APPROVED
```

---

**Quick Links:**
- Full Instructions: `STANDING_VERIFICATION_INSTRUCTION.md` (v2.1)
- Track A Worksheet: `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md` (v1.0)
- Track A RETAIN Register: `TRACK_A_RETAIN_REGISTER.md` (v1.0) - Check existing RETAIN decisions first
- **Track A - Legacy Reference:** `project/nish/README.md`
- **Track B - NSW Fundamentals Index:** `NSW Fundamental Alignment Plan/00_INDEX.md`
- **Track B - Master Fundamentals:** `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- **Track B - Canonical Rules:** `NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md`
- Architecture Standards: `NEW_BUILD_ARCHITECTURE.md`

