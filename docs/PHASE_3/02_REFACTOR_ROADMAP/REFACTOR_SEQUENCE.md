# Refactor Sequence — S0–S5 Control Stages + Module Order Mapping

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** ACTIVE (Roadmap / Control Model)  
**Date:** 2025-12-18 (IST)

---

## 1. Purpose

Phase 3 uses **one primary sequencing model** for safe execution control (**S0–S5**) and a **secondary module prioritization order** used *inside* the execution stages.

This eliminates “two competing roadmaps”:
- **S0–S5** is the governance/control sequence (verification → ownership → isolation → alignment → propagation → regression gate)
- **Module Order** is a sub-plan for what to prioritize within S2/S3/S4

---

## 2. Sequencing Hierarchy (Non-Negotiable)

1. **Primary:** S0 → S5 (execution control stages)
2. **Secondary:** Module order (priority list) applied only within **S2/S3/S4**

If there is any conflict, **S0–S5 wins**.

---

## 3. S0–S5 Control Stages (Definition)

### S0 — Verification (Inputs Locked)

Goal: confirm planning inputs are complete and frozen.

Must exist and be treated read-only:
- Phase 1 baselines (freeze register + module freezes)
- Phase 2 trace maps (ROUTE_MAP / FEATURE_CODE_MAP / FILE_OWNERSHIP)
- Phase 3 governance docs (this pack)

### S1 — Ownership (Risk → Rules)

Goal: convert FILE_OWNERSHIP into operational enforcement.

Outputs:
- confirmed file owners
- risk classification per file/task
- declared “hands-off” zones (PROTECTED)
- approved allowed patterns (wrapper/adapter for protected core)

### S2 — Isolation (Safe Entry Points)

Goal: isolate modules and establish safe entry points before change.

Typical outputs:
- boundaries, wrappers, adapters
- isolation plan that avoids touching PROTECTED logic directly
- rollback approach for HIGH/PROTECTED tasks

### S3 — Alignment (Standardize Within Boundaries)

Goal: align module behavior and interfaces without cross-module breakage.

Typical outputs:
- consistent validations and data contracts
- standardized reuse/apply expectations
- documentation updates to keep traceability current

### S4 — Propagation (Upstream → Downstream Rollout)

Goal: roll aligned changes through dependent modules in dependency order.

Rule:
- upstream foundations first (catalog/templates)
- quotation execution last

### S5 — Regression Gate (Evidence + Approval)

Goal: prove nothing breaks, especially protected cross-module flows.

Minimum:
- apply-flow bundle coverage (Master BOM + Feeder + Proposal → Quotation)
- costing integrity checks
- rollback readiness validated
- approval recorded for HIGH/PROTECTED

---

## 4. Module Order (Used inside S2/S3/S4)

This is the **priority order** for selecting work packages within S2/S3/S4:

1. Dashboard / Shared / Ops
2. Master (Org / Vendor / PDF)
3. Employee / Role
4. Component / Item Master
5. Master BOM
6. Feeder Library
7. Proposal BOM
8. Quotation (Legacy)
9. Quotation V2 (always last)

Note:
- Quotation V2 work packages should not be approved for execution until upstream modules have completed relevant S4 propagation and are gated by S5 regression requirements.

---

## 5. Mapping: Where Module Order Applies

| Control Stage | Module Order Applies? | Why |
|---|---:|---|
| S0 (Verification) | No | Inputs readiness only |
| S1 (Ownership) | No | Risk/ownership enforcement only |
| S2 (Isolation) | Yes | Safe entry points by priority |
| S3 (Alignment) | Yes | Standardize by priority |
| S4 (Propagation) | Yes | Rollout by dependency order |
| S5 (Regression Gate) | No | Global bundles & approvals |

---

## 6. References

- `docs/PHASE_3/PHASE_3_EXECUTION_PLAN.md`
- `trace/phase_2/FILE_OWNERSHIP.md`
- `trace/phase_2/ROUTE_MAP.md`
- `trace/phase_2/FEATURE_CODE_MAP.md`

