# Execution Rulebook — Phase 3 (Phase 4 Execution Governance)

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE (FINAL)  
**Version:** 1.1  
**Date:** 2025-12-18 (IST)  
**Last Updated:** 2025-12-18 (IST)

**Version History:**
- v1.1 (2025-12-18): Added Section 12 — Document Versioning Rule (strict enforcement rule)
- v1.0 (2025-12-18): Initial version

---

## 1. Purpose (Planning Artifact Only)

This rulebook defines the **non-negotiable execution governance** for Phase 4 work:
- gate-by-gate enforcement rules
- approval authority and evidence requirements
- rollback doctrine
- “hands-off” doctrine for PROTECTED logic
- automatic stop/abort conditions

This is **documentation only**. No code changes are implied by this document.

---

## 2. Definitions (Control Model)

### 2.1 S0–S5 Control Stages (Primary)

The primary execution control sequence is **S0 → S5**, defined in:
- `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`

### 2.2 Module Order (Secondary)

Module order is a **secondary priority list** used only inside **S2/S3/S4**.  
If there is any conflict, **S0–S5 wins**.

### 2.3 Risk Levels (Authority)

Risk classification is authoritative and comes from:
- `trace/phase_2/FILE_OWNERSHIP.md`

Controls are governed by:
- `docs/PHASE_3/05_RISK_CONTROL/RISK_CONTROL_MATRIX.md`
- `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`

---

## 3. Task Identity Standard (Single Source)

All executable work must be represented by a task entry and must use:

**NSW-P4-<S_STAGE>-<MODULE>-###**

Examples:
- NSW-P4-S0-GOV-001
- NSW-P4-S2-CIM-001
- NSW-P4-S4-QUO-005

Minimum rule:
- **No task ID → no work**

---

## 4. Execution Discipline (Non-Negotiable)

Before touching any file in Phase 4 execution:
- Confirm the task exists in `docs/PHASE_3/04_TASK_REGISTER/TASK_REGISTER.md`
- Confirm the task ID includes the correct **S-stage**
- Confirm file ownership + risk level via `trace/phase_2/FILE_OWNERSHIP.md`
- Confirm the required gate level (G0–G4) and evidence expectations
- Confirm rollback feasibility if the task is HIGH/PROTECTED

---

## 5. Protected-Core Doctrine (Hands-Off Zones)

PROTECTED logic must not be changed directly without explicit approval and regression evidence.

Allowed patterns (high-level):
- wrappers/adapters/decorators
- controlled delegation

Disallowed pattern:
- direct edits to PROTECTED logic without satisfying PROTECTED gate rules (G4)

---

## 6. Approval Authority (Who Approves What)

To avoid “who signed this?” ambiguity, approvals are separated:

| Approval Type | Purpose | Required For | Approving Role (Named Authority) | Evidence Required |
|---|---|---|---|---|
| Architectural Approval | Confirms approach is aligned to target architecture, boundaries, and S-stage | Any HIGH/PROTECTED task; any cross-module touchpoint; any boundary change | **Planning Authority / Architecture Owner** | Written decision + references |
| Execution Approval | Confirms readiness to execute (gates, rollback, tests) | HIGH/PROTECTED tasks | **Nish Execution Lead / Reviewer** | Gate evidence checklist + rollback |
| Release Approval | Confirms release readiness after tests | HIGH/PROTECTED tasks; any change with cross-module bundle impact | **Release Owner** | Test evidence + sign-off |

Notes:
- MEDIUM/LOW tasks may be approved via normal review practice, but must still have a task entry and correct S-stage assignment.
- If roles are not yet assigned by name, they must be assigned **before execution begins**.

---

## 7. Gate-by-Gate Enforcement Rules (G0–G4)

Gate definitions and required test bundles are defined in:
- `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`

This section defines the **enforcement rules** that must be met before a task can proceed.

### G0 — Governance / Planning

Allowed actions:
- documentation updates
- task creation and refinement
- risk classification and ownership confirmation

Mandatory evidence:
- task entry exists with correct ID and S-stage
- references to Phase 1/2 artifacts are recorded

### G1 — LOW Risk Execution

Mandatory evidence:
- task entry + file list
- basic verification evidence recorded (what was checked)

### G2 — MEDIUM Risk Execution

Mandatory evidence:
- task entry + file list + ownership confirmation
- module-level regression definition and evidence

### G3 — HIGH Risk Execution

Mandatory evidence:
- task entry + explicit cross-module touchpoints (if any)
- defined cross-module test bundle(s) where applicable
- rollback steps written and feasible
- recorded approvals (architectural + execution)

### G4 — PROTECTED Execution

Mandatory evidence:
- task entry + explicit PROTECTED scope statement
- wrapper/adapter approach confirmed (no direct protected edits without explicit exception approval)
- full regression evidence as defined in testing gates
- costing integrity evidence where applicable
- rollback validated
- recorded approvals (architectural + execution + release)

---

## 8. Automatic Stop / Abort Conditions (Mandatory)

Execution must **stop immediately** (abort current work package) if any of the following occurs:

- **Unapproved work**
  - a change is attempted without a task ID
  - a change is attempted that is not described by the registered task scope
- **S-stage violation**
  - task is executed outside its declared S-stage (e.g., propagation work attempted during isolation)
- **PROTECTED breach**
  - PROTECTED file/area is edited directly without satisfying G4 evidence and approvals
- **Rollback invalidation**
  - rollback path becomes infeasible or untestable mid-execution
- **Gate failure**
  - required gate evidence cannot be produced
  - required cross-module test bundle fails and cannot be resolved within the approved scope
- **Ownership ambiguity**
  - file ownership/risk classification cannot be confirmed from FILE_OWNERSHIP

Abort protocol (minimum):
- stop changes for the task immediately
- document the stop reason in the task entry
- escalate to the approving roles in Section 6
- re-scope or re-register a new task if needed (do not “continue anyway”)

---

## 9. Rollback Doctrine + Validation Checklist

Rule: **No rollback = no execution** for HIGH and PROTECTED tasks.

### Rollback validation checklist (HIGH/PROTECTED)

- [ ] rollback steps are written in task entry
- [ ] rollback can be executed within the same release window
- [ ] rollback does not require “heroic” manual edits or unknown procedures
- [ ] rollback is compatible with the gate level (G3/G4)
- [ ] rollback is validated (evidence recorded)

---

## 10. Evidence & Audit Trail (Minimum Requirements)

For every task:
- task entry updated with file list and scope
- ownership + risk level recorded
- gate level recorded
- evidence recorded (tests/verification per gate)

For HIGH/PROTECTED tasks additionally:
- approvals recorded (per Section 6)
- rollback validation evidence recorded
- stop/abort events (if any) recorded with resolution decision

---

## 11. Change Control for This Rulebook

This file is **ACTIVE (FINAL)** for Phase 3 governance.

Any change to this rulebook requires:
- a governance task entry (NSW-P4-S0-GOV-###)
- architectural approval
- index/reference updates if file paths are impacted

---

## 12. Document Versioning Rule (Strict — Non-Negotiable)

**Effective Date:** 2025-12-18  
**Rule Status:** ACTIVE — STRICT ENFORCEMENT  
**Applies To:** All documentation files (markdown, text, planning artifacts)

### 12.1 Core Rule

**When modifying existing documents, always add versioned sections rather than replacing entire file content.**

This rule ensures:
- ✅ Traceability of all changes
- ✅ Ability to copy only modified portions for review
- ✅ Preservation of historical content
- ✅ Clear audit trail of document evolution

### 12.2 Required Format for Document Modifications

When modifying an existing document, follow this structure:

```markdown
---

## [Section Title] (v2.0) — [Date]

**[Previous version preserved above]**

### Changes in this version:
- [Brief description of what changed]
- [Reference to task ID if applicable]

[New or modified content here]

**Version Info:**
- Version: 2.0
- Date: YYYY-MM-DD
- Modified By: [task/author reference]
- Previous Version: 1.0 (preserved above)
```

### 12.3 What Must Be Versioned

**All modifications to existing documents must be versioned:**
- ✅ Section additions
- ✅ Section modifications
- ✅ Table updates
- ✅ Content corrections
- ✅ Reference updates
- ✅ Status changes

**Exceptions (allowed without versioning):**
- ❌ Fixing typos only (no content change)
- ❌ Formatting-only changes (whitespace, markdown syntax cleanup with no semantic change)
- ❌ Initial document creation (first version)

### 12.4 Version Numbering Convention

- **v1.0** — Initial version
- **v1.1, v1.2, ...** — Minor updates (additions, clarifications, non-breaking changes)
- **v2.0, v3.0, ...** — Major updates (structural changes, significant rewrites)

For each versioned section, include:
- Version number
- Date of modification
- Task ID (if applicable)
- Brief change description

### 12.5 Enforcement

**This rule is NON-NEGOTIABLE for Phase 4 execution.**

Before modifying any document:
1. Confirm the document already exists (if so, versioning is required)
2. Identify which section(s) need modification
3. Add a new versioned section rather than replacing old content
4. Preserve previous version content above the new version
5. Document the change with version metadata

**Violations:**
- Replacing entire document content without versioning is considered a governance violation
- Must be corrected immediately by adding versioned section structure
- Requires task entry for correction (NSW-P4-S0-GOV-###)

### 12.6 Example Structure

```
## Original Section (v1.0)

[Original content here]

---

## Original Section (v2.0) — 2025-12-18

**Changes in v2.0:**
- Added gap closure task mapping
- Updated task counts
- Reference: NSW-P4-S2-GOV-GAP-001

[Modified or new content here]

**Version Info:**
- Version: 2.0
- Date: 2025-12-18
- Modified By: NSW-P4-S2-GOV-GAP-001
- Previous Version: 1.0
```

---

## 13. References

- `docs/PHASE_3/PHASE_3_EXECUTION_PLAN.md`
- `docs/PHASE_3/PHASE_3_INDEX.md`
- `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- `docs/PHASE_3/04_TASK_REGISTER/TASK_REGISTER.md`
- `docs/PHASE_3/05_RISK_CONTROL/RISK_CONTROL_MATRIX.md`
- `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
