# S3-COPY-HIST-GAP-004 — Copy History Integrity Alignment Pack
#
# Task coverage:
# - NSW-P4-S3-COPY-HIST-GAP-004 (G3)
#
# Status: ACTIVE (S3)
# Last Updated: 2025-12-18

---

## Scope + Fence

- **Planning + alignment only**
- **No implementation**
- **No schema changes**
- **No apply behavior changes**
- Defines mandatory copy-history expectations and evidence rules

---

## 1) Problem Definition (Frozen)

Copy/apply flows currently lack a guaranteed, verifiable history trail across all BOM paths.

This creates:
- Weak rollback confidence
- Incomplete reuse audit
- Ambiguous provenance during regression

---

## 2) Apply Surfaces Requiring Copy History

| Apply Surface | Route | Owner |
|---------------|-------|-------|
| MBOM apply | `quotation.v2.applyMasterBom` | QUO |
| FEED apply | `quotation.v2.applyFeederTemplate` | QUO |
| PBOM apply | `quotation.v2.applyProposalBom` | QUO |

**Rule:** Every successful execution of the above must emit a copy-history record.

---

## 3) Minimum Copy History Contract (Frozen)

Each apply operation must result in one history row with:

| Field | Description |
|-------|-------------|
| SourceType | MBOM / FEED / PBOM |
| SourceId | Template or source BOM ID |
| TargetQuotationId | Quotation receiving the copy |
| TargetBomId | QuotationSaleBom created/updated |
| OperationType | APPLY / REUSE / COPY |
| Actor | User / system |
| CreatedAt | Timestamp |

**Rule:** One apply execution → at least one history row; duplicates are allowed only if OperationType differs (APPLY vs REUSE vs COPY).

Exact table/column names are not frozen in S3 — only the existence and semantics.

---

## 4) Evidence Requirements (S3 declaration)

### Required Evidence Pattern (per apply path)

| Step | Evidence |
|------|----------|
| R1 | Apply request (API/UI) |
| S1 | DB snapshot before apply |
| R2 | Apply response |
| S2 | DB snapshot after apply showing history row |

### Evidence location:

```
docs/PHASE_4/evidence/GAP/BOM-GAP-004/
  ├─ MBOM/
  ├─ FEED/
  └─ PBOM/
```

---

## 5) What Is Frozen in S3

- Copy history is mandatory
- Applies to all BOM apply paths
- History absence = test failure
- Gap classified as Lane-A

---

## 6) What Is Explicitly NOT Changed

- No DB schema finalized
- No history table created in S3
- No controller edits
- No service refactors
- No retroactive history generation

---

## 7) S4 Propagation Hooks

| Task | Description |
|------|-------------|
| NSW-P4-S4-COPY-HIST-GAP-004 | Implement copy-history creation |
| NSW-P4-S4-COPY-WIRE-GAP-007 | Ensure wiring reaches history logic |
| NSW-P4-S5-GOV-003 | Rollback certification depends on this |

---

## 8) Exit Criteria (S3-COPY-HIST-GAP-004)

S3-COPY-HIST-GAP-004 is **COMPLETE** when:

- [x] Copy history expectation documented
- [x] All apply surfaces mapped
- [x] Evidence rules frozen
- [x] S4 hooks declared
- [x] Lane-A classification recorded in GAP_GATEBOARD

---

## Status

**NSW-P4-S3-COPY-HIST-GAP-004:** ✅ Complete  
**Next:** S4 execution can begin with copy-history implementation

---

## Authority References

- Master Task List: `docs/PHASE_4/MASTER_TASK_LIST.md`
- GAP Gateboard: `docs/PHASE_4/GAP_GATEBOARD.md`
- S3 BOM Alignment: `docs/PHASE_4/S3_BOM_ALIGNMENT.md`
- S3 QUO Alignment: `docs/PHASE_4/S3_QUO_ALIGNMENT.md`
- S3 Execution Checklist: `docs/PHASE_4/S3_EXECUTION_CHECKLIST.md`

---

