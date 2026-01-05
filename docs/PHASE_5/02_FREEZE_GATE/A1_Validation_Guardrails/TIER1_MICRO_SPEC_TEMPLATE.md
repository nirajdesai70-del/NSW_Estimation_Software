# Tier-1 Micro-Spec Template (FREEZE-GATE CANON)

**Document Type:** Tier-1 Rule Micro-Specification  
**Applies To:** A1 / A4 / A5 / A6 (High-risk rules only)  
**Status:** 🔒 CANONICAL (once approved)  
**Change Control:** Phase-5 Senate approval required  
**Date:** 2026-01-27  
**Purpose:** Standardized template for governance-grade, developer-executable, audit-defensible rule specifications that protect critical business logic and prevent misinterpretation.

⸻

## 1️⃣ Rule Identifier

- **Rule ID:** (e.g., G-04, A5-LOCK-01, A4-PROV-01)
- **Category:** Validation / Governance / Runtime Control / Provenance
- **Phase Introduced:** Phase-5
- **Risk Class:** 🔴 Tier-1 (Financial / Audit / Legal)

⸻

## 2️⃣ Intent (What This Rule Protects)

Describe in one paragraph:
- What problem this rule prevents
- What could go wrong if this rule is violated
- Why this rule exists beyond "because schema says so"

**Audience:** Management, auditors, reviewers

⸻

## 3️⃣ Business Rationale (Why This Must Exist)

Explicitly state:
- Financial risk prevented
- Audit risk prevented
- User behavior risk prevented
- Why "common sense" is not sufficient

**Answers:** "Why can't developers just handle this ad-hoc?"

⸻

## 4️⃣ Canonical Scope (Where It Applies)

| Dimension | Applies | Notes |
|-----------|---------|-------|
| Schema | ✅ / ❌ | CHECK / FK / absence |
| Service Layer | ✅ / ❌ | Mandatory or planned |
| Compute Engine | ✅ / ❌ | Deterministic behavior |
| API / Validator | ✅ / ❌ | Early rejection |
| Audit | ✅ / ❌ | Required / optional |
| UI | ❌ | UI never authoritative |

⸻

## 5️⃣ Schema Behavior (Hard Guarantees)

Describe exact schema facts, not intentions:
- Table(s)
- Column(s)
- Constraints
- Defaults
- **Explicit absences (very important)**

**Example structure:**

```
Table: quote_bom_items
Column: rate_source
Type: VARCHAR
Constraint: CHECK ( … )
Default: UNRESOLVED
```

**If absence is part of the rule, document it explicitly.**

⸻

## 6️⃣ Runtime Enforcement Semantics (Authoritative)

**This is the most important section.**

### 6.1 Allowed States

List all allowed states explicitly.

### 6.2 Blocked States

List all blocked states and why.

### 6.3 When Enforcement Happens

- On create
- On update
- On delete
- On preview
- On apply-recalc

**Be precise.**

⸻

## 7️⃣ Compute / Engine Semantics

Define:
- How calculations behave under this rule
- What happens to totals
- What happens to derived fields

**Prevents:** "silent math drift"

⸻

## 8️⃣ Audit & Traceability Expectations

Specify:
- Which actions must emit audit events
- What minimum fields must be captured
- When audit is recommended vs mandatory

**Protects:** Legal defensibility

⸻

## 9️⃣ Explicit Non-Goals (VERY IMPORTANT)

List what this rule does NOT do, even if tempting.

**Examples:**
- Does NOT block edits
- Does NOT cascade to parent
- Does NOT auto-correct user input

**Prevents:** Scope creep

⸻

## 🔟 Failure & Recovery Semantics

Describe:
- What error is returned
- Who can recover
- Whether recovery is manual or automatic

**Avoids:** Undefined runtime behavior

⸻

## 1️⃣1️⃣ Future Extension Rules (Controlled)

State:
- What could be extended in future
- What MUST happen before extension:
  - Decision
  - Migration
  - Doc update
  - Audit update

⸻

## 1️⃣2️⃣ Freeze-Gate Declaration

- **Status:** 🔒 LOCKED
- **Effective Date:** YYYY-MM-DD
- **Change Requires:** Phase-5 Senate approval

⸻

---

**Template Version:** 1.0  
**Template Freeze Date:** 2026-01-27  
**Usage:** All Tier-1 rule specifications (A1 guardrails G-04/G-06/G-08, A4 provenance fields, A5 locking, A6 CostHead)

