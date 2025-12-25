# Phase 5 Mode Policy

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose

This document establishes the operating mode for Phase 5 and defines when transitions between modes occur.

## Current Mode

**🔓 OPEN_GATE_EXPLORATION**

**Effective Date:** 2025-01-27  
**Status:** ACTIVE

## Mode Definitions

### 🔓 OPEN_GATE_EXPLORATION

**Purpose:** Allow intentional exploration, learning, and discovery while maintaining controlled capture of decisions.

**Characteristics:**
- **Gates:** OPEN (no hard entry gate checklist)
- **Prerequisites:** Reference inputs, not blockers
- **Decision Capture:** REQUIRED (all changes must be logged)
- **Freeze:** NOT ALLOWED (premature freezes are blocked)
- **Schema Changes:** ALLOWED (REQUIRES Decision Register entry FIRST)
- **Rule Changes:** ALLOWED (REQUIRES Decision Register entry FIRST)
- **New Features:** ALLOWED (with feature discovery log entry)

**Governance Controls:**
- **Schema/Rule Changes:** MUST create Decision Register entry BEFORE making the change
- All changes must be logged in Decision Register or Feature Discovery Log
- All schema changes must reference Fundamentals baseline
- All divergences from legacy must be documented with rationale
- Weekly cadence: Change Summary + Readiness Score

**Exit Criteria:** See `STABILIZATION_EXIT_CRITERIA.md`

---

### 🔒 STABILIZATION

**Purpose:** Natural stabilization after exploration slows, patterns repeat, decisions stop changing weekly.

**Characteristics:**
- **Gates:** CONTROLLED (decision capture still required)
- **Prerequisites:** All pending inputs reviewed and decisioned
- **Decision Capture:** REQUIRED (final decisions being locked)
- **Freeze:** PREPARING (exit criteria being met)
- **Schema Changes:** RESTRICTED (only clarifications, no DDL modifications)
- **Rule Changes:** RESTRICTED (only clarifications)
- **New Features:** DEFERRED (captured for post-freeze)

**Governance Controls:**
- Weekly checkpoint against exit criteria
- All pending decisions must be resolved
- Schema churn must be zero for 7 consecutive days
- Fundamentals compliance verified

**Exit Criteria:** All stabilization exit criteria met → transition to FREEZE

---

### ❄️ FREEZE

**Purpose:** Lock Step-2 (Schema Design) after natural stabilization.

**Characteristics:**
- **Gates:** CLOSED (no changes without governance approval)
- **Prerequisites:** All verified and documented
- **Decision Capture:** ARCHIVED (decisions register locked)
- **Freeze:** ACTIVE (Step-2 frozen)
- **Schema Changes:** BLOCKED (requires governance exception)
- **Rule Changes:** BLOCKED (requires governance exception)
- **New Features:** DEFERRED (post-implementation)

**Governance Controls:**
- All changes require governance approval
- Exception process documented
- Freeze declaration published

---

## Mode Transition Rules

### Exploration → Stabilization

**Trigger:** When ALL of the following are true:
1. Schema churn stability: No DDL changes to `NSW_SCHEMA_CANON_v1.0.md` for 7 consecutive days (or only documentation clarifications)
2. Decision closure: All items in `SPEC_5_FREEZE_GATE_CHECKLIST.md` sections 1–8 are ✅ VERIFIED
3. Fundamentals compliance: Each major schema section contains "Alignment Note" referencing v2.0 fundamentals
4. Traceability completeness: `PHASE_5_REQUIREMENT_TRACE.md` shows ≥ 95% requirements covered
5. Implementation readiness: Seed validation script covers required scenarios

**Process:**
1. Weekly checkpoint evaluation (see `STABILIZATION_CHECKPOINT_LOG.md`)
2. When all criteria met → declare mode transition
3. Update this document with new mode and date

---

### Stabilization → Freeze

**Trigger:** When ALL stabilization exit criteria are met AND:
1. Final verification pass completed
2. Freeze declaration prepared
3. All stakeholders notified

**Process:**
1. Final checkpoint pass
2. Freeze declaration published
3. Mode updated to FREEZE
4. Step-2 locked

---

## Current Mode Operating Rules

### Decision Capture Required

**CRITICAL RULE:** Schema and rule changes MUST create Decision Register entry BEFORE making the change.

**What qualifies as a decision:**
- Any change to canonical schema (tables, fields, relationships) → **REQUIRES Decision Register entry FIRST**
- Any change to business rules or validation guardrails → **REQUIRES Decision Register entry FIRST**
- Any divergence from Fundamentals baseline
- Any rejection of legacy pattern
- Any new feature or capability addition
- Any change to naming conventions or standards

**Required fields:**
- Decision ID (from Decision Register)
- Date
- Rationale
- Impact scope
- Fundamentals alignment citation
- Status (NEW/APPROVED/SUPERSEDED)

### No Silent Edits

**Rule:** Any change to canonical outputs must be logged in:
- Decision Register (for decisions)
- Feature Discovery Log (for new ideas)
- Pending Inputs Register (for prerequisites being integrated)

**Enforcement:**
- Commit messages must reference decision/feature ID
- Weekly Change Summary must list all changes

### Fundamentals Alignment

**Rule:** Every decision must cite at least one of:
- `FUNDAMENTALS_SOURCE_OF_TRUTH.md`
- `NSW_FUNDAMENTALS_ALIGNMENT_PLAN_REGISTER.md`
- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md`
- `NSW Fundamental Alignment Plan/01_FUNDAMENTALS/FUNDAMENTALS_v2.0_PHASE_5_GAP_ANALYSIS.md`

**Purpose:** Ensure traceability to baseline, even when diverging.

---

## Weekly Cadence (Exploration Mode

### Monday: Change Summary
- List all changes from previous week
- Update Decision Register
- Update Feature Discovery Log
- Update Pending Inputs Register

### Wednesday: Readiness Check
- Evaluate against Stabilization Exit Criteria
- Update Stabilization Checkpoint Log
- Identify blockers or risks

### Friday: Open Items Review
- Review pending decisions
- Review new feature discoveries
- Plan next week's exploration

---

## Mode History

| Date | Mode | Trigger | Notes |
|------|------|---------|-------|
| 2025-01-27 | OPEN_GATE_EXPLORATION | Initial setup | Exploration mode established |

---

## Change Log

- **v1.0 (2025-01-27):** Initial mode policy created, Exploration mode declared active

---

**END OF MODE POLICY**

