# NSW Estimation – Phase-6

## Week-0 Execution Checklist & Closure Gate

**Purpose**  
Convert the approved Week-0 plan into certified Phase-6 execution reality, and formally decide whether Week-0 can be closed.

**Rule of Use**
- Treat this as a gate document, not a suggestion list
- Each item must be marked PASS / FAIL / N/A with evidence
- Only failed items are fixed — nothing extra is added

---

## DAY-1 — Entry Gate & Canon Protection

### D1-01 — Phase-5 Canon Read-Only Lock
**Expected**
- `CANON_READ_ONLY.md` exists
- Explicit mention of:
  - Schema Canon v1.0 frozen
  - Decisions D-005 / 006 / 007 / 009 frozen
  - Guardrails G1–G8 frozen

**Verify**
- File exists in repo root or `/docs/governance`
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D1-02 — Schema Snapshot Reference
**Expected**
- Schema snapshot file (SQL or diagram) committed
- Clearly marked REFERENCE ONLY
- No migration files modified after Phase-5

**Verify**
- Snapshot present
- No migration files modified after Phase-5
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D1-03 — Feature-Only Rule Declared
**Expected**
- README or governance doc states:
  - "Phase-6 may add features but may not change meaning"

**Verify**
- Text visible in README / governance section
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D1-04 — Decision Register Closure Verified
**Expected**
- Explicit statement that Phase-5 decisions are closed

**Verify**
- Reference in governance docs
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## DAY-2 — Infrastructure Baseline Gate

### D2-01 — Backend Stack Verification
**Expected**
- FastAPI running
- Laravel `/nish` marked read-only / legacy

**Verify**
- `GET /health` returns OK
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D2-02 — Database Loaded from Schema Canon v1.0
**Expected**
- PostgreSQL schema matches Canon v1.0

**Verify**
- Table names & columns align
- No ad-hoc schema additions
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D2-03 — Docker Compose Compliance
**Expected**
- Services: API + PostgreSQL only
- ❌ Redis
- ❌ Paid services

**Verify**
- `docker-compose.yml` reviewed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D2-04 — Structured Logging Enabled
**Expected**
- Logs in structured (JSON or key-value) format

**Verify**
- Console output verified
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## DAY-3 — Data Boundary Definition (Structural Only)

### D3-01 — QCD Boundary Verified
**Expected**
- BOM tables exist (`quote_bom_items`, etc.)
- No cost fields in BOM tables

**Verify**
- DB schema inspection
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D3-02 — QCA Table Exists
**Expected**
- `quote_cost_adders` table exists
- One row per panel × cost head

**Verify**
- DB schema verified
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D3-03 — Service-Layer Separation Declared
**Expected**
- Separate service/interface for QCD vs QCA
- No cross-write logic

**Verify**
- Code structure / interfaces reviewed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## DAY-4 — Reuse Engine Skeleton (Stub Level)

### D4-01 — Copy Quotation Endpoint
**Expected**
- Endpoint exists
- Deep copy (new IDs)

**Verify**
- API test performed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D4-02 — Copy Panel / Feeder / BOM Endpoints
**Expected**
- Endpoints exist for all reuse types

**Verify**
- API routes visible
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D4-03 — Copy-Never-Link Verified
**Expected**
- No shared foreign keys after copy

**Verify**
- DB inspection after copy
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D4-04 — Tracking Fields Populated
**Expected**
- `origin_master_bom_id`
- `instance_sequence_no`
- `is_modified`

**Verify**
- DB row inspection
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## DAY-5 — UI Skeleton Gate

### D5-01 — Navigation Path Exists
**Expected**
- Quotation → Panel → Feeder → BOM reachable

**Verify**
- Manual UI navigation tested
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D5-02 — UI Is Cost-Neutral
**Expected**
- No costing fields editable or visible

**Verify**
- UI review completed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## DAY-6 — Costing Rules Definition (No UI)

### D6-01 — Costing View Rules Documented
**Expected**
- Document defining:
  - Quotation = summary only
  - Cost sheet = detailed breakup

**Verify**
- Doc exists
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D6-02 — Fabrication Special Rule Declared
**Expected**
- FABRICATION → MATERIAL (quotation)
- Internal split preserved, hidden

**Verify**
- Rules doc + service stub reviewed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## DAY-7 — Week-0 Validation Gate

### D7-01 — Sample Quotation Created
**Expected**
- Quotation with:
  - Panel
  - Feeder
  - BOM

**Verify**
- UI + DB check performed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D7-02 — Reuse Tested End-to-End
**Expected**
- Copy → edit → save works

**Verify**
- Manual test performed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

### D7-03 — Canon Violation Check
**Expected**
- No schema meaning changes

**Verify**
- Diff / review completed
- Status: ⬜ PASS ⬜ FAIL
- Evidence: ______________________

---

## 🔒 WEEK-0 CLOSURE DECISION

### Closure Rule
- ❌ Any FAIL = Week-0 remains OPEN
- ✅ All PASS = Week-0 CLOSED

**Week-0 Status:**
- ⬜ CLOSED — proceed to Week-1
- ⬜ OPEN — fix only failed items above

**Closure Signed By:** ____________________  
**Date:** ____________________

---

## What Happens Next (Do Not Skip)

Once Week-0 is formally CLOSED, the next mandatory sequence is:

1️⃣ Generate Week-1 to Week-3 Task Grid (Track-wise)  
2️⃣ Generate Week-8.5 Legacy Parity Gate Checklist  
3️⃣ Lock execution cadence

---

**Document Status:** ✅ EXECUTION CHECKLIST READY  
**Last Updated:** 2025-01-27  
**Next Action:** Execute Week-0 checklist, then proceed to next document generation
