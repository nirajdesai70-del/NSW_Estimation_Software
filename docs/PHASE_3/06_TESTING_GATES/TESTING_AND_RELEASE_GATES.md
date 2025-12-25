# Testing & Release Gates — Phase 3

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE  
**Date:** 2025-12-17 (IST)

---

## 1. Purpose

Define **mandatory testing and release gates** to ensure NSW execution is safe, predictable, and reversible.

No task can move forward without satisfying its gate.

---

## 2. Gate Levels

| Gate | Applies To |
|---|---|
| G0 | Governance / Documentation |
| G1 | LOW risk tasks |
| G2 | MEDIUM risk tasks |
| G3 | HIGH risk tasks |
| G4 | PROTECTED tasks |

---

## 3. Gate Requirements

### G0 — Governance

- Task registered
- Ownership confirmed
- No code touched

---

### G1 — LOW Risk

- Basic functional verification
- No cross-module impact

---

### G2 — MEDIUM Risk

- Module-level regression
- UI verification

---

### G3 — HIGH Risk

- Module regression
- Cross-module test bundle
- Rollback validated

---

### G4 — PROTECTED

- Full regression suite
- Apply-flow bundle tested
- Costing validation
- Explicit approval recorded

---

## 4. Mandatory Cross-Module Test Bundles

### Bundle A — Quotation V2 Apply

Must pass together:
- applyMasterBom
- applyFeederTemplate
- applyProposalBom

---

### Bundle B — Costing Integrity

- Panel → Feeder → BOM cost roll-up
- Discount application
- Audit log consistency

---

### Bundle C — Catalog Validity

- Product creation
- Import validation
- Attribute enforcement

---

## 5. Release Rules

A task can be released only if:
- Its gate is passed
- Rollback path exists (if required)
- No unresolved risk flags

---

## 6. Rollback Rules

Rollback must be:
- documented
- executable within same deployment window
- tested for HIGH/PROTECTED tasks

---

## 7. Post-Release Monitoring

Required for HIGH and PROTECTED:
- error logs
- costing anomalies
- performance regressions

---

## 8. References

- `docs/PHASE_3/05_RISK_CONTROL/RISK_CONTROL_MATRIX.md`
- `trace/phase_2/FILE_OWNERSHIP.md`

