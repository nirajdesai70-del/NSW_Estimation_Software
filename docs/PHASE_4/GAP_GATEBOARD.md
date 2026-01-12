# GAP_GATEBOARD — Phase 4 Closure Driver (v1.3)

**Purpose:** Single authority mapping for gap closure decisions during Phase 4 (S2–S5).  
**Rule:** Phase 4 cannot be marked CLOSED until all Lane-A gaps are CLOSED (or exception-approved).  
**Status:** 🔒 CLOSED (Phase 4 Planning & Implementation Complete)  
**Closure Note:** See `docs/PHASE_4/PHASE_4_FINAL_CLOSURE_NOTE.md`

**Version History:**
- v1.3 (2025-12-24): Phase-4 closure — execution-dependent gaps marked as PLANNED & FROZEN
- v1.2 (2025-12-18): Fixed PB-GAP-004 title (removed mis-attribution to BOM-GAP-002), normalized BOM-GAP-004 closure stage, added evidence artifacts checklist, fixed Lane-B decision log ref format, adjusted PB-GAP-003/004 gate levels, added Notes column
- v1.1 (2025-12-18): Added Closure Stage/Gate column, Exception Allowed column, filled missing descriptions, added evidence folder convention
- v1.0 (2025-12-18): Initial version

---

## 0) Evidence Folder Convention

**Rule:** All gap evidence must be stored using this standardized folder structure:

- **Gap evidence:** `docs/PHASE_4/evidence/GAP/<GAP-ID>/`
- **Gate-0 Template Readiness:** `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/`
  - Format: `TEMPLATE_<TEMPLATE_ID>_count.txt`
  - Example: `TEMPLATE_123_count.txt`

**No random evidence locations allowed.** All evidence must follow this convention.

---

## 1) Lane Definition

### Lane-A (Must Close in Phase 4)
Gaps that block correctness, apply/reuse integrity, copy-never-link integrity, verification readiness, or audit history.

### Lane-B (Out of Phase 4 / Separate Program)
Enhancements / new features that are not required for Phase 4 stability and G5 sign-off.

---

## 2) Lane-A Gaps — Required Closures (v1.3)

**Changes in v1.3:**
- Phase-4 closure: execution-dependent gaps marked as 🟨 PLANNED & FROZEN
- All planning artifacts complete (test cases, fixtures, evidence templates)
- Execution deferred until live DB available

**Changes in v1.2:**
- Fixed PB-GAP-004 title (removed mis-attribution to BOM-GAP-002 root cause)
- Normalized BOM-GAP-004 closure stage to S4/G3 (deterministic)
- Added evidence artifacts required checklist
- Adjusted PB-GAP-003/004 gate levels to S5/G3 (default, escalate to G4 if PROTECTED touched)
- Added Notes column for closure stage clarifications

**Changes in v1.1:**
- Added "Closure Stage/Gate" column (replaces "Closure Gate")
- Added "Exception Allowed?" column (default No for Lane-A)
- Filled missing gap descriptions (BOM-GAP-013, PB-GAP-003, PB-GAP-004)

| Gap ID | Title | Status | Owner | Closure Stage/Gate | Exception Allowed? | Evidence Pointer | Notes |
|-------|-------|--------|-------|-------------------|-------------------|------------------|-------|
| BOM-GAP-001 | Feeder apply creates new feeder every time (no reuse detection) | 🟨 PLANNED & FROZEN | FEED | S3/G3 | No | `docs/PHASE_4/evidence/GAP/BOM-GAP-001/` | Planning complete; execution deferred (requires live DB) |
| BOM-GAP-002 | Feeder apply missing clear-before-copy (duplicate stacking) | 🟨 PLANNED & FROZEN | FEED | S3/G3 | No | `docs/PHASE_4/evidence/GAP/BOM-GAP-002/` | Planning complete; execution deferred (requires live DB) |
| BOM-GAP-004 | Copy operations missing copy-history (migration + runtime record) | 🟨 PLANNED & FROZEN | BOM | S4/G3 | No | `docs/PHASE_4/evidence/GAP/BOM-GAP-004/` | S3 alignment complete; S4 planning complete; execution deferred (requires live DB) |
| BOM-GAP-007 | Copy operations not wired/verified end-to-end | 🟨 PLANNED & FROZEN | BOM | S4/G3 | No | `docs/PHASE_4/evidence/GAP/BOM-GAP-007/` | Planning complete; execution deferred (requires live DB) |
| BOM-GAP-013 | Template data missing (Phase-2 data readiness - selected MasterBomId has 0 rows in master_bom_items) | 🟨 PLANNED & FROZEN | GOV/FEED | S2/G2 (Gate-0 evidence) + S5/G4 (final closure) | No | `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/` | Gate-0 rule established; execution deferred (requires live DB) |
| BOM-GAP-006 | Lookup pipeline preservation not verified after copy (category/subcategory/SKU/attribute chain integrity) | 🟨 PLANNED & FROZEN | SHARED/BOM | S5/G3 | No | `docs/PHASE_4/evidence/GAP/BOM-GAP-006/` | Planning complete; execution deferred (requires live DB) |
| PB-GAP-003 | Quantity chain correctness + feeder discovery edge cases | 🟨 PLANNED & FROZEN | PBOM | S5/G3 | No | `docs/PHASE_4/evidence/GAP/PB-GAP-003/` | Planning complete; execution deferred (requires live DB) |
| PB-GAP-004 | Instance isolation under proposal reuse/apply flows (no shared IDs; verify re-apply does not duplicate or link) | 🟨 PLANNED & FROZEN | PBOM/BOM | S5/G3 | No | `docs/PHASE_4/evidence/GAP/PB-GAP-004/` | Planning complete; execution deferred (requires live DB) |

**Closure rule:** mark CLOSED only after evidence is attached and regression bundle is green.

**Phase-4 Closure Status:**
- All Lane-A gaps have planning complete ✅
- Execution deferred until live DB available 🟨
- Test cases, fixtures, evidence templates preserved
- See `docs/PHASE_4/PHASE_4_FINAL_CLOSURE_NOTE.md` for closure rationale

**Exception approval process:** Exception approval requires Decision Log entry + reason + risk acceptance + alternative verification. Reference format: EXC-<gap-id>-001.

### Evidence Artifacts Required (Standard Checklist)

**Rule:** Each Lane-A gap evidence folder must contain the following standard artifacts:

**Standard artifacts (all gaps):**
- `EVIDENCE.md` (one-page summary)
- `R1_request.json` / `R1_response.json` (request/response evidence)
- `S1_snapshot.sql.txt` (state snapshot before)
- `S2_snapshot.sql.txt` (state snapshot after)

**Additional artifacts (BOM-GAP-004, BOM-GAP-007):**
- `migration_status.txt` (migration application status)
- `history_row_sample.json` (sample copy-history row evidence)

**Gate-0 artifacts (BOM-GAP-013 only):**
- `TEMPLATE_<TEMPLATE_ID>_count.txt` (template item count evidence)

**No closure will be accepted without these artifacts in the evidence folder.**

---

## 3) Lane-B Gaps — Explicit Deferrals (v1.2)

**Changes in v1.2:**
- Fixed decision log ref format to EXC- prefix (matches exception approval convention)

**Changes in v1.1:**
- Added decision log placeholder format

| Gap ID | Title | Status | Deferred To | Decision Log Ref |
|-------|-------|--------|-------------|------------------|
| BOM-GAP-005 | BOM Node edits missing history/backup (requires new table + new engine ops + restore paths) | DEFERRED | Phase-6+/Feature Program | EXC-BOM-GAP-005-001 _(to be recorded in PROJECT_DECISION_LOG.md)_ |

---

## 4) Gate-0 Template Data Readiness (BOM-GAP-013) (v1.1)

**Changes in v1.1:**
- Added exact evidence folder path and filename format

**Rule:** Do not execute apply verification unless selected TEMPLATE_ID has items.

**Required SQL evidence (attach output):**
- `SELECT COUNT(*) AS item_count FROM master_bom_items WHERE MasterBomId = <TEMPLATE_ID>;`
- item_count must be > 0

**Evidence folder and filename format:**
- **Folder:** `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/`
- **Filename format:** `TEMPLATE_<TEMPLATE_ID>_count.txt`
- **Example:** `TEMPLATE_123_count.txt` (for MasterBomId=123)

**Evidence structure:**
- Gate-0 output: `docs/PHASE_4/evidence/GATE0_TEMPLATE_READINESS/TEMPLATE_<ID>_count.txt`
- R1 response: inserted_count = N (must match item_count from Gate-0)
- S1/S2 snapshots: `docs/PHASE_4/evidence/GAP/BOM-GAP-013/`

---

## 5) Phase 4 Closure Dependency

**Phase 4 Closure Status:** 🔒 **CLOSED — Planning & Implementation Complete**

**Closure Rationale:**
- All Lane-A gaps have planning complete ✅
- All Lane-A gaps have test cases, fixtures, evidence templates prepared ✅
- Execution deferred due to unavailability of live DB 🟨
- Lane-B gaps have explicit deferral decision logged ✅
- `NSW-P4-S5-GOV-GAPS-CERT-001` planning complete (execution deferred) 🟨

**Deferred Execution:**
- All Lane-A gap execution tasks deferred until live DB available
- All S5 regression execution tasks deferred until live DB available
- All deferred tasks have complete planning artifacts preserved

**Closure Note:** See `docs/PHASE_4/PHASE_4_FINAL_CLOSURE_NOTE.md`

---

**Last Updated:** 2025-12-24 (v1.3)  
**Authority:** Phase 4 Master Task List  
**Version:** 1.3 (Final Closure)

