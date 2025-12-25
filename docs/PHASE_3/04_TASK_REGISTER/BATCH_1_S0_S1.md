# Batch-1 — S0 Verification + S1 Ownership

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Batch:** B1  
**Coverage:** S0 + S1  
**Status:** ACTIVE (Planning Only)  
**Last Updated:** 2025-12-18 (IST)

**Authority:**
- Risk/ownership: `trace/phase_2/FILE_OWNERSHIP.md`
- Sequencing: `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- Gates: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Governance: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`

---

## 1. Batch Purpose

Batch-1 establishes the **minimum verification + ownership certainty** required before any Isolation (S2) planning begins.

This batch produces:
- confirmed Phase 3 doc integrity
- protected-zone existence confirmation (read-only)
- trace gap log (no fixing)
- shared endpoints mapped to cross-module bundles
- ownership boundaries and exceptions list (S1)

---

## 2. Batch Task List (Authoritative)

| Task ID | S-Stage | Module | Sub-Area | Type | Risk | Gate | Objective (1 line) | In Scope (explicit) | Forbidden | Cross-Module Touchpoints | Evidence Required | Approvals Required | Rollback Required | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NSW-P4-S0-GOV-001 | S0 | GOV | Phase 3 Index | Governance | LOW | G0 | Verify canonical folder + links are correct and single-source | `docs/PHASE_3/**`, `PHASE_3_INDEX.md` | Any nish edits | None | Updated links + “no duplicates” note | Arch: No / Exec: No / Release: No | No | Planned |
| NSW-P4-S0-GOV-002 | S0 | GOV | Protected Zone | Verification | HIGH | G3 | Confirm protected files exist in nish and match Phase 3 docs | **Read-only:** file existence + class names only | Full file dumps; any edits | Quotation + Costing | Existence log (paths + class names) | Arch: Yes / Exec: Yes / Release: No | Yes (defined) | Planned |
| NSW-P4-S0-GOV-003 | S0 | GOV | Trace Coverage | Governance | MEDIUM | G2 | Identify ROUTE_MAP/FEATURE_CODE_MAP gaps and log as tasks | `trace/phase_2/*` | Adding assumptions | All modules | Gap list + created task stubs | Arch: No / Exec: No / Release: No | No | Planned |
| NSW-P4-S0-GOV-004 | S0 | GOV | Doc Consistency | Governance | LOW | G0 | Remove outdated “next I can generate” text and align next-step footer | `PHASE_3_EXECUTION_PLAN.md` | Any meaning change | None | Footer standardized + note | Arch: No / Exec: No / Release: No | No | Planned |
| NSW-P4-S0-SHARED-001 | S0 | SHARED | Shared Endpoints | Verification | HIGH | G3 | Identify shared endpoints and bind to bundles A/B/C | `ROUTE_MAP`, `FEATURE_CODE_MAP` | Any refactor suggestion | Reuse + dropdown APIs | Bundle mapping table | Arch: Yes / Exec: Yes / Release: No | Yes (defined) | Planned |
| NSW-P4-S0-CIM-001 | S0 | CIM | Import Split | Verification | HIGH | G3 | Confirm ImportController split ownership points (CIM vs Master/PDF) | Trace review + controller list | Any controller edits | Master/PDFContain | Split-ownership map | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S0-MBOM-001 | S0 | MBOM | Apply Touchpoints | Verification | HIGH | G3 | Verify Master BOM routes + apply touchpoints are mapped | Trace review only | Any apply change | Quotation V2 apply | Touchpoint list | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S0-FEED-001 | S0 | FEED | Apply Touchpoints | Verification | HIGH | G3 | Verify Feeder routes + apply touchpoints are mapped | Trace review only | Any apply change | Quotation V2 apply | Touchpoint list | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S0-PBOM-001 | S0 | PBOM | Apply Touchpoints | Verification | HIGH | G3 | Verify Proposal BOM routes + apply touchpoints are mapped | Trace review only | Any apply change | Quotation V2 apply | Touchpoint list | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S0-QUO-001 | S0 | QUO | Quotation Legacy | Verification | HIGH | G3 | Verify legacy quotation routes/controllers are fully mapped | Trace review only | Pricing changes | Dropdown APIs | Dependency list | Arch: Yes / Exec: Yes / Release: No | Yes | Planned |
| NSW-P4-S0-QUO-002 | S0 | QUO | Quotation V2 | Verification | PROTECTED | G4 | Verify V2 protected zone + apply bundles are documented | Docs + trace only | Direct edits | MBOM/FEED/PBOM apply | Protected checklist + bundles A/B | Arch: Yes / Exec: Yes / Release: Yes | Yes (validated) | Planned |

---

## 3. S1 Placeholder (Ownership) — To be Expanded After S0 Close

S1 tasks will be expanded into full cards after S0 completion. Initial placeholders:

| Placeholder Task ID | S-Stage | Module | Objective | Status |
|---|---|---|---|---|
| NSW-P4-S1-GOV-001 | S1 | GOV | Reconcile planned file list vs FILE_OWNERSHIP and confirm risk levels | Planned |
| NSW-P4-S1-GOV-002 | S1 | GOV | Produce “ownership exceptions list” (mixed-responsibility files) for S2 split planning | Planned |
| NSW-P4-S1-ALL-001 | S1 | ALL | Create module boundary blocks (in-scope + forbidden callers) for CIM/MBOM/FEED/PBOM/QUO | Planned |

---

## 4. Read-only nish access policy for Batch-1

Allowed only for `NSW-P4-S0-GOV-002`:
- Confirm file path exists
- Confirm class name exists
- Confirm method name exists (if needed)

Not allowed:
- full file paste
- any edits
- any “quick fix testing”

---

## 5. Batch-1 Exit Criteria

Batch-1 is complete when:
- S0 tasks are marked Done with evidence links
- S1 placeholders are ready to be expanded into full task cards
- ownership exceptions list exists (even if empty)

Next batch:
- **Batch-2 — S2 Isolation task cards**

Batch-2 file:
- `docs/PHASE_3/04_TASK_REGISTER/BATCH_2_S2.md`


