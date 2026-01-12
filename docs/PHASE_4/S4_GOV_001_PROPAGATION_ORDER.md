# S4-GOV-001 — Propagation Order + All-or-Nothing Rule
#
# Task coverage:
# - NSW-P4-S4-GOV-001 (G2)
#
# Status: ACTIVE (S4)
# Last Updated: 2025-12-18

---

## Scope + Fence

- **Governance control document only**
- **No code changes**
- **No execution authorization**
- Defines mandatory propagation sequence and adoption rules for all S4 work

**S4 Guardrails:**
- ✅ Allowed: define execution order, freeze adoption rules, document dependency graph, establish rollback sequencing, define rollback checkpoints + stop conditions, define evidence pointers
- ❌ Not allowed: any QUO-V2 PROTECTED edits unless G4 approvals and QUO-REVERIFY is PASS, any "cleanup refactor" not tied to a named gap/task, any endpoint/schema change without being attached to a specific S4 task

---

## 1) Objective (Frozen)

Establish controlling rails for S4 propagation to ensure:
- Safe dependency-ordered rollout
- No partial adoption states
- Predictable rollback sequences
- Evidence consistency across all propagation tasks

---

## 2) Propagation Order (Authoritative)

S4 propagation must follow this **mandatory sequence**:

### 2.1 Primary Sequence (Canonical Order)

**Rule:** S4 propagation must follow this strict dependency order:

| Stage | Module Group | Objective | Risk Level | Gate | Blocking Dependencies |
|-------|--------------|-----------|------------|------|---------------------|
| **S4.1** | SHARED | Contract surface adoption + optional extraction wiring | HIGH | G3 | None (foundation layer) |
| **S4.2** | CIM | Migrate CIM consumers to SHARED CatalogLookupContract | HIGH | G3 | S4.1 complete |
| **S4.3** | BOM | MBOM → FEED → PBOM: adopt contracts; wire copy paths | HIGH | G3 | S4.1 complete |
| **S4.4** | QUO Legacy | Consumption migration + extraction targets | HIGH | G3 | S4.1, S4.2, S4.3 complete |
| **S4.5** | QUO-V2 | Only after NSW-P4-S2-QUO-REVERIFY-001 PASS + G4 go-ahead | PROTECTED | G4 | S4.1, S4.2, S4.3, S4.4 complete + QUO-REVERIFY PASS |

**Why this order:** Avoids changing producers and consumers in the same blast-radius window without stable contracts.

**Rule:** Each stage must be **complete** (evidence recorded, rollback verified, checkpoints passed) before next stage begins.

### 2.2 Module Order (Secondary, Within Each Stage)

When multiple tasks exist within a stage, use this priority order:

1. Dashboard / Shared / Ops
2. Master (Org / Vendor / PDF)
3. Employee / Role
4. Component / Item Master
5. Master BOM
6. Feeder Library
7. Proposal BOM
8. Quotation (Legacy)
9. Quotation V2 (always last)

**Rule:** Module order is advisory; S-stage sequence is mandatory.

---

## 3) All-or-Nothing Adoption Rule (Frozen)

### 3.1 Rule Definition

**When a contract is propagated, ALL consumers must adopt it within the same propagation stage. No partial adoption allowed.**

### 3.2 What This Means

| Scenario | Allowed? | Evidence Required |
|----------|----------|-------------------|
| Extract CatalogLookup to SHARED controller; all consumers updated in same batch | ✅ Yes | Consumer adoption checklist |
| Extract CatalogLookup to SHARED controller; 2/5 consumers updated | ❌ No | Stage blocked until all consumers migrated |
| Extract CatalogLookup to SHARED controller; legacy QUO deferred to S4.4 | ✅ Yes (if explicitly deferred) | Deferral decision logged in S4.4 scope |

### 3.3 Deferral Rules

Deferral is allowed **only** if:
1. Deferral decision is documented before stage start
2. Deferred consumers are explicitly listed in next stage scope
3. COMPAT endpoints remain available until S5 Bundle-C pass (mandatory lifecycle rule)
4. No consumer is "stuck" between old and new contracts

**Rule:** Deferral is exception, not default. Prefer complete adoption within stage.

### 3.4 COMPAT Endpoint Lifecycle Rule (Frozen)

**COMPAT endpoints must remain alive until S5 Bundle-C pass.**

- COMPAT endpoints (e.g., `product.get*`, `masterbom.get*`) are bridge endpoints
- They remain available during S4 propagation as fallback
- Removal is authorized only after S5 Bundle-C (Catalog Validity) passes
- No COMPAT endpoint deletions in S4 without explicit S5 approval

**Why:** Prevents breakage during transition; allows rollback if needed.

---

## 4) Dependency Graph (Frozen)

### 4.1 Contract Propagation Dependencies

```
SHARED Contracts (S4.1)
    │
    ├─→ CIM Consumers (S4.2)
    │
    ├─→ BOM Consumers (S4.3)
    │   │
    │   └─→ Copy-History Implementation (S4.3)
    │
    └─→ QUO Legacy (S4.4)
        │
        └─→ QUO-V2 (S4.5) [PROTECTED]
```

### 4.2 Task Dependencies Within Stages

**S4.1 (SHARED):**
- Extract CatalogLookupController → Extract ReuseSearchController (optional; may be parallel)
- Both extractions must complete before consumers can migrate

**S4.3 (BOM):**
- Copy-history implementation (NSW-P4-S4-COPY-HIST-GAP-004) → Copy-wiring verification (NSW-P4-S4-COPY-WIRE-GAP-007)

**S4.4 (QUO Legacy):**
- SHARED contract adoption → BOM contract adoption (sequential)

**S4.5 (QUO-V2):**
- All S4.1–S4.4 complete → QUO-V2 wrapper adoption (if needed)

---

## 5) Rollback Discipline (Checkpoints + Stop Conditions)

### 5.1 Rollback Checkpoints (CP0-CP3)

For each batch, enforce these checkpoints:

| Checkpoint | Definition | Evidence Required |
|------------|------------|-------------------|
| **CP0 (Baseline)** | Commit hash + current routes snapshot + "known-good" smoke notes | Git commit hash, route list snapshot, smoke test results |
| **CP1 (After code change)** | Build/lint pass + minimal smoke checks | Lint output, basic smoke test results |
| **CP2 (After wiring)** | Run bundle(s) for the batch | Bundle A/B/C test results |
| **CP3 (Evidence pack)** | Update evidence pointers + close checklist | Evidence folder updated, task checklist complete |

**Rule:** Each checkpoint must be recorded before proceeding to next checkpoint. CP0 is mandatory before any code changes.

### 5.2 Rollback Order (Reverse of Propagation)

Rollback must follow **reverse stage order**:

1. **S4.5** rollback first (if executed)
2. **S4.4** rollback second
3. **S4.3** rollback third
4. **S4.2** rollback fourth
5. **S4.1** rollback last (foundation must remain until all dependents rolled back)

### 5.3 Rollback Evidence Requirements

Each rollback must provide:
- Reverse migration scripts (if DB changes)
- Route handler reversion (if controller moved)
- Consumer reversion checklist
- Bundle C verification (catalog validity restored)
- Checkpoint restoration proof (CP0 state restored)

**Rule:** Rollback must restore system to CP0 baseline state.

### 5.4 Stop Conditions (Automatic Rollback Triggers)

Execution **must stop immediately** and rollback if any of these conditions occur:

| Stop Condition | Description | Authority Reference |
|----------------|-------------|---------------------|
| Runtime auto-create master pattern | Any runtime code creates masters (Category/Item/Product/Attribute/Make/Series) outside MASTER module | Phase-5 Governance Firewall (ADR-005) |
| Breaking payload shape change | SHARED contract endpoint payload shape changed in breaking way | S3 contract freeze documents |
| QUO-V2 PROTECTED touch without G4 | QUO-V2 PROTECTED surface touched without explicit G4 approval and QUO-REVERIFY PASS | Execution Rulebook Section 4.3 |
| Copy-never-link breach | Apply flow creates duplicates/links instead of copy (violates copy-never-link rule) | S3 BOM Alignment + Master BOM Rules |
| COMPAT endpoint removed prematurely | COMPAT endpoint removed before S5 Bundle-C pass | Section 3.4 (COMPAT lifecycle rule) |

**Rule:** Stop conditions trigger immediate rollback to last checkpoint. No partial fixes allowed.

---

## 6) Evidence Consistency Rules (Frozen)

All S4 propagation tasks must record:

| Evidence Type | Required For | Format |
|---------------|--------------|--------|
| Route mapping | Controller extractions | Before/after route handler table |
| Consumer checklist | Consumer migrations | Adopter list + verification status |
| Bundle test results | All HIGH/PROTECTED tasks | Bundle A/B/C pass/fail evidence |
| Rollback drill | All HIGH/PROTECTED tasks | Rollback rehearsal log |

**Rule:** Evidence must be stored in standardized locations per task (see Master Task List).

---

## 6) S4 Batch Sequencing (Recommended)

### 6.1 Batch Mapping to Execution Files

S4 execution is organized into batches that map to existing batch files:

| Batch | Name | File Reference | Primary Objective | Dependencies |
|-------|------|----------------|-------------------|--------------|
| **Batch-S4-1** | SHARED | `docs/PHASE_4/S4_BATCH_1_TASKS.md` | Adopt/stabilize SHARED contract surfaces (no removals) | None (foundation) |
| **Batch-S4-2** | CIM | TBD | Migrate CIM screens off `product.get*` COMPAT endpoints to CatalogLookupContract; keep COMPAT alive | Batch-S4-1 complete |
| **Batch-S4-3** | BOM | TBD | MBOM adoption; FEED adoption + prep for reuse/clear semantics wiring; PBOM adoption | Batch-S4-1 complete |
| **Batch-S4-4** | Copy wiring + history | TBD | BOM-GAP-007 wiring reachability verification (end-to-end); BOM-GAP-004 implement copy-history emission + evidence collection | Batch-S4-3 complete |
| **Batch-S4-5** | QUO Legacy | `docs/PHASE_4/S4_BATCH_3_TASKS.md` | Migrate QUO legacy internal consumption toward contracts; prepare extraction targets for SHARED endpoints (no breaking route changes) | Batch-S4-1, S4-2, S4-3 complete |
| **Batch-S4-6** | QUO-V2 | TBD | Only after QUO-REVERIFY PASS + G4 approvals | Batch-S4-5 complete + NSW-P4-S2-QUO-REVERIFY-001 PASS |

### 6.2 Batch Success Criteria

Each batch is **SUCCESS** only if:
- All intended consumers in the batch have been updated
- Backward compatibility remains (COMPAT endpoints stay alive until S5 Bundle-C pass)
- Regression bundle for that batch is green
- All checkpoints (CP0-CP3) recorded

If any consumer fails or regressions appear:
- Roll back the entire batch to the last checkpoint (see Section 5.1)
- Do not partially ship mixed contract adoption states

---

## 7) Execution Blocking Rules (Frozen)

### 7.1 Hard Blocks

S4 propagation is **blocked** if:
- S3 alignment documents are incomplete
- Any HIGH/PROTECTED task lacks rollback plan
- Bundle A/B/C test infrastructure is unavailable
- Previous stage evidence is missing

### 7.2 Soft Blocks (Warning Only)

S4 propagation **warns** (but does not block) if:
- Compat endpoints are removed before all consumers migrated
- Route names changed without explicit approval
- Payload shapes modified without contract freeze update

---

## 8) Evidence Minimum for S4-GOV-001

This document serves as the governance note containing:
- Propagation order (Section 2)
- All-or-nothing rule (Section 3)
- Rollback checkpoints + stop conditions (Section 5)
- Batch mapping (Section 6)
- Links to: MASTER_TASK_LIST.md, GAP_GATEBOARD.md, S4_EXECUTION_CHECKLIST.md

**Evidence location:** `docs/PHASE_4/S4_GOV_001_PROPAGATION_ORDER.md`

---

## 9) Exit Criteria (S4-GOV-001)

S4-GOV-001 is **COMPLETE** when:

- [x] Propagation order documented and frozen
- [x] All-or-nothing rule defined and examples provided
- [x] COMPAT endpoint lifecycle rule defined
- [x] Dependency graph mapped
- [x] Rollback checkpoints (CP0-CP3) established
- [x] Stop conditions documented
- [x] Batch sequencing mapped to execution files
- [x] Evidence consistency rules defined
- [x] Execution blocking rules documented

---

## Status

**NSW-P4-S4-GOV-001:** ✅ Complete  
**Next:** Batch-S4-1 (SHARED) can begin - `docs/PHASE_4/S4_BATCH_1_TASKS.md`

**Pre-execution checklist:**
- [ ] S3 alignment documents complete (SHARED, CIM, BOM, QUO, COPY-HIST-GAP-004)
- [ ] Rollback plans exist for all HIGH/PROTECTED tasks
- [ ] Bundle A/B/C test infrastructure ready
- [ ] CP0 checkpoints can be established (git baseline ready)

---

## 10) Legacy vs NSW Semantic Boundary (Critical)

### 10.1 Boundary Rule

**S4 SHARED contracts are Legacy Lookup Contracts v1, not NSW Canonical Contracts.**

S4 standardizes how legacy lookups are consumed (reduces drift, centralizes behavior).  
Phase-5 defines NSW canonical contracts separately (clean rebuild, firewall governance).  
Legacy and NSW are two different truth layers (explicit separation).

### 10.2 Naming Convention

| Contract | Internal Name (Docs) | Layer | Purpose |
|----------|----------------------|-------|---------|
| `CatalogLookupContract` | **Legacy CatalogLookupContract v1** | Legacy/NEPL | Standardize legacy lookup consumption |
| `ReuseSearchContract` | **Legacy ReuseSearchContract v1** | Legacy/NEPL | Standardize legacy reuse search |
| NSW Catalog Contract | **NSW Canonical Catalog Contract** | NSW | Clean canonical lookup for NSW (Phase-5) |

**Rule:** In S4 docs, refer to SHARED contracts as "Legacy CatalogLookupContract v1" (even if file name stays the same).

### 10.3 What S4 Does NOT Do

- ❌ Does NOT redefine master semantics
- ❌ Does NOT create NSW canonical contracts
- ❌ Does NOT migrate legacy data
- ❌ Does NOT change what Category/Item/etc. mean in legacy

**S4 only standardizes how legacy lookups are consumed.**

### 10.4 Full Boundary Document

**Reference:** `docs/PHASE_4/LEGACY_VS_NSW_SEMANTIC_BOUNDARY.md`

This document provides:
- Complete explanation of two truth layers (Legacy vs NSW)
- Naming conventions and documentation rules
- Mental model for S4 vs Phase-5 work
- Implementation checklist

**All S4 work must respect this boundary to prevent semantic confusion.**

---

## Authority References

- Master Task List: `docs/PHASE_4/MASTER_TASK_LIST.md`
- GAP Gateboard: `docs/PHASE_4/GAP_GATEBOARD.md`
- S4 Execution Checklist: `docs/PHASE_4/S4_EXECUTION_CHECKLIST.md`
- S4 Propagation Plan: `docs/PHASE_4/S4_PROPAGATION_PLAN.md`
- S4 Batch Files: `docs/PHASE_4/S4_BATCH_1_TASKS.md`, `docs/PHASE_4/S4_BATCH_3_TASKS.md`, etc.
- S3 Alignment: `docs/PHASE_4/S3_SHARED_ALIGNMENT.md`, `docs/PHASE_4/S3_CIM_ALIGNMENT.md`, `docs/PHASE_4/S3_BOM_ALIGNMENT.md`, `docs/PHASE_4/S3_COPY_HIST_GAP_004_ALIGNMENT.md`
- Refactor Sequence: `docs/PHASE_3/02_REFACTOR_ROADMAP/REFACTOR_SEQUENCE.md`
- Testing Gates: `docs/PHASE_3/06_TESTING_GATES/TESTING_AND_RELEASE_GATES.md`
- Execution Rulebook: `docs/PHASE_3/07_RULEBOOK/EXECUTION_RULEBOOK.md`
- Phase-5 Governance Firewall: `docs/PHASE_5/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md`
- **Legacy vs NSW Boundary:** `docs/PHASE_4/LEGACY_VS_NSW_SEMANTIC_BOUNDARY.md` ⭐

---

