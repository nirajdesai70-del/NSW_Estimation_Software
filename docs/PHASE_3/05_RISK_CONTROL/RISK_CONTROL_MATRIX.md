# Risk Control Matrix — Phase 3

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE  
**Date:** 2025-12-17 (IST)

---

## 1. Purpose

Provide a **single source of truth** for managing risk during NSW execution.

This matrix governs:
- who can touch what
- what tests are mandatory
- when execution must stop

---

## 2. Risk Categories

| Level | Meaning |
|---|---|
| PROTECTED | Core business logic – zero tolerance |
| HIGH | Cross-module or financially sensitive |
| MEDIUM | Module-contained |
| LOW | Isolated |

---

## 3. Control Matrix

| Risk | Allowed Action | Mandatory Controls | Rollback | Approval |
|---|---|---|---|---|
| PROTECTED | Wrapper only | Regression + cross-module tests | Required | Mandatory |
| HIGH | Wrapper / parallel | Module + cross-module tests | Required | Mandatory |
| MEDIUM | Replace allowed | Module tests | Optional | Optional |
| LOW | Replace allowed | Basic tests | Optional | No |

---

## 4. Automatic Stop Conditions

Execution **must stop immediately** if:

- PROTECTED file edited directly
- Costing SUM(AmountTotal) rule altered
- Quotation V2 apply flows broken
- No rollback defined for HIGH/PROTECTED
- Cross-module change without coordination

---

## 5. High-Risk Zones

### Quotation Core

- QuotationV2Controller
- CostingService
- QuotationQuantityService

### Catalog Integrity

- CategoryAttributeController
- CatalogCleanupController
- ImportController

### Reuse & Apply

- ReuseController
- applyMasterBom / applyFeederTemplate / applyProposalBom

---

## 6. Risk Escalation Path

1. Identify risk from FILE_OWNERSHIP
2. Apply stricter gate if unsure
3. Escalate to PROTECTED if business impact unclear
4. Defer execution if safety cannot be proven

---

## 7. Auditability

Every HIGH or PROTECTED task must have:
- task ID
- owner
- approval record
- test evidence

---

## 8. References

- `trace/phase_2/FILE_OWNERSHIP.md`
- `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`

