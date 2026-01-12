# Gap Evidence Artifacts

**Purpose:** Standardized evidence storage for all Phase 4 Lane-A gap closures.

**Rule:** All gap evidence must be stored in `docs/PHASE_4/evidence/GAP/<GAP-ID>/`

---

## Standard Artifacts (All Gaps)

Each gap evidence folder must contain the following standard artifacts:

### Required Files

1. **`EVIDENCE.md`**
   - One-page summary of gap closure
   - Includes: gap description, closure approach, verification method, results

2. **`R1_request.json`**
   - Request payload evidence (API request or operation input)

3. **`R1_response.json`**
   - Response payload evidence (API response or operation output)
   - Must show successful closure/verification

4. **`S1_snapshot.sql.txt`**
   - State snapshot before gap closure operation
   - SQL query results showing pre-closure state

5. **`S2_snapshot.sql.txt`**
   - State snapshot after gap closure operation
   - SQL query results showing post-closure state
   - Must demonstrate gap is closed

---

## Additional Artifacts (BOM-GAP-004, BOM-GAP-007)

For copy-history and copy-wiring gaps, also include:

6. **`migration_status.txt`**
   - Migration application status
   - Confirms migration has been applied

7. **`history_row_sample.json`**
   - Sample copy-history row evidence
   - Demonstrates history tracking is working

---

## Gate-0 Artifacts (BOM-GAP-013 Only)

For template data readiness, also reference:

- **Gate-0 count files:** `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/TEMPLATE_<ID>_count.txt`
- **S1/S2 snapshots:** Stored in `docs/PHASE_4/evidence/GAP/BOM-GAP-013/`

**Note:** `docs/PHASE_4/evidence/GAP/BOM-GAP-013/` must still contain the standard 5 artifacts (EVIDENCE.md, R1_request.json, R1_response.json, S1_snapshot.sql.txt, S2_snapshot.sql.txt) even though Gate-0 count evidence is stored separately.

---

## Folder Structure Example

```
docs/PHASE_4/evidence/GAP/
├── BOM-GAP-001/
│   ├── EVIDENCE.md
│   ├── R1_request.json
│   ├── R1_response.json
│   ├── S1_snapshot.sql.txt
│   └── S2_snapshot.sql.txt
├── BOM-GAP-002/
│   └── ...
└── README.md (this file)
```

---

## Closure Requirements

**No closure will be accepted without these artifacts in the evidence folder.**

Before marking a gap as CLOSED:
1. ✅ All required artifacts present
2. ✅ Evidence demonstrates gap is closed
3. ✅ Regression bundle is green
4. ✅ Evidence folder follows naming convention

---

## Exception Process

If exception approval is required:
- Decision Log entry: `EXC-<gap-id>-001`
- Reason documented
- Risk acceptance recorded
- Alternative verification provided

---

**Authority:** GAP_GATEBOARD.md Section 2  
**Last Updated:** 2025-12-18

