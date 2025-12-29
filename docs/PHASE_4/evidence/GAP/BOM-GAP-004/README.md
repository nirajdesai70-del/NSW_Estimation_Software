# BOM-GAP-004 Evidence Folder

**Gap:** Copy operations missing copy-history (migration + runtime record)  
**Status:** ⏳ PARTIAL (S3 alignment complete; S4 implementation pending)  
**Owner:** BOM  
**Closure Stage/Gate:** S4/G3

---

## Evidence Structure

Evidence must be collected for each apply path:

```
BOM-GAP-004/
├── MBOM/
│   ├── EVIDENCE.md
│   ├── R1_request.json
│   ├── R1_response.json
│   ├── S1_snapshot.sql.txt
│   ├── S2_snapshot.sql.txt
│   ├── migration_status.txt
│   └── history_row_sample.json
├── FEED/
│   └── (same structure as MBOM)
├── PBOM/
│   └── (same structure as MBOM)
└── README.md (this file)
```

---

## Evidence Requirements (Per Apply Path)

### Standard Artifacts

1. **`EVIDENCE.md`** - One-page summary of copy-history verification
2. **`R1_request.json`** - Apply request (API/UI)
3. **`R1_response.json`** - Apply response
4. **`S1_snapshot.sql.txt`** - DB snapshot before apply
5. **`S2_snapshot.sql.txt`** - DB snapshot after apply showing history row

### Additional Artifacts (BOM-GAP-004)

6. **`migration_status.txt`** - Migration application status
7. **`history_row_sample.json`** - Sample copy-history row evidence

---

## Apply Surfaces Under Test

| Apply Surface | Route | Evidence Folder |
|---------------|-------|-----------------|
| MBOM apply | `quotation.v2.applyMasterBom` | `MBOM/` |
| FEED apply | `quotation.v2.applyFeederTemplate` | `FEED/` |
| PBOM apply | `quotation.v2.applyProposalBom` | `PBOM/` |

---

## Copy History Contract (Minimum Required Fields)

Each history row must contain:
- SourceType (MBOM / FEED / PBOM)
- SourceId (Template or source BOM ID)
- TargetQuotationId (Quotation receiving the copy)
- TargetBomId (QuotationSaleBom created/updated)
- OperationType (APPLY / REUSE / COPY)
- Actor (User / system)
- CreatedAt (Timestamp)

---

## Closure Criteria

BOM-GAP-004 is CLOSED when:
- [x] S3 alignment complete (expectations frozen)
- [ ] All three apply paths (MBOM/FEED/PBOM) have complete evidence
- [ ] History rows are created for all successful apply operations
- [ ] Evidence demonstrates copy-history integrity
- [ ] Regression bundle is green

---

## Authority References

- Alignment Blueprint: `docs/PHASE_4/S3_COPY_HIST_GAP_004_ALIGNMENT.md`
- GAP Gateboard: `docs/PHASE_4/GAP_GATEBOARD.md`
- Evidence Standard: `docs/PHASE_4/evidence/GAP/README.md`

---

**Last Updated:** 2025-12-18

