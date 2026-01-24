# PHASE-6 | WEEK-0 — Evidence Pack (Frozen)

**Scope:** Week-0 only  
**Mode:** Read-only verification  
**Outputs:** `scripts/run_week0_checks.sh` + evidence folder artifacts

---

## Week-0 Objectives (Frozen)

### A) Environment sanity
- Backend is reachable on the expected health endpoint
- Dev helper scripts (if present) pass without deviation
- Capture system/toolchain baseline evidence

### B) Begin P6-ENTRY-001
- Create an auditable, time-stamped evidence snapshot for readiness
- No schema meaning changes
- No migrations
- No auto-fixes

---

## How to Run (Single Command)

From repo root:

```bash
chmod +x scripts/run_week0_checks.sh
./scripts/run_week0_checks.sh
```

Optional overrides:

```bash
# If your backend health endpoint differs
PHASE6_BACKEND_URL="http://localhost:8003/health" ./scripts/run_week0_checks.sh

# If you want to annotate expected ports (evidence only)
PHASE6_PORTS="8003,8000,8011" ./scripts/run_week0_checks.sh
```

---

## What Gets Produced

Evidence folder:
- `evidence/PHASE6_WEEK0_RUN_<timestamp>/WEEK0_SUMMARY.md`
- `evidence/PHASE6_WEEK0_RUN_<timestamp>/P6_ENTRY_001_ENV_SANITY.md`
- Raw logs:
  - `backend_health.txt`
  - `tool_versions.txt`
  - `ports_snapshot.txt`
  - `git_status.txt`, `git_head.txt`, `git_branch.txt`, `git_diffstat.txt` (if git exists)
  - `optional_status_dev.txt` (if scripts/status_dev.sh exists)
  - `optional_smoke_dev.txt` (if scripts/smoke_dev.sh exists)

---

## PASS/FAIL Rules (Week-0)

### HARD FAIL (runner stops)
- Backend health endpoint is not reachable
- `scripts/status_dev.sh` exists but fails
- `scripts/smoke_dev.sh` exists but fails
- Missing Week-0 deliverables:
  - `scripts/run_week0_checks.sh`
  - `PHASE6_WEEK0_EVIDENCE_PACK.md` (repo root or docs/PHASE_6/)

### Recorded (not a fail)
- Working tree not clean (captured in git evidence)

Week-0 is evidence-first. We record drift; we do not correct drift here.

---

## P6-ENTRY-001 (Definition)

**Entry ID:** P6-ENTRY-001  
**Title:** Environment Sanity & Readiness Evidence  
**Evidence:** `P6_ENTRY_001_ENV_SANITY.md` + `WEEK0_SUMMARY.md` + raw logs

**Acceptance criteria:**
- Health check passes
- Evidence snapshot exists with timestamped folder
- Summary is generated and includes the key outputs inline

---

## What to Post Back to Master Thread (Minimal)

Paste:
1. The path of the evidence folder (timestamped)
2. The contents (or excerpt) of:
   - `WEEK0_SUMMARY.md`
   - Any failing log if Week-0 stops

**Example:**
- Evidence: `evidence/PHASE6_WEEK0_RUN_20260112_133000/`
- Summary: `.../WEEK0_SUMMARY.md`
- P6-ENTRY-001: `.../P6_ENTRY_001_ENV_SANITY.md`

---

## Stop/Deviation Protocol (Frozen)

If any HARD FAIL happens:
- Do not run any Week-1+ tasks
- Do not modify schema meaning
- Do not attempt "quick fixes" inside the Week-0 runner
- Report the failure back to the Phase-6 master thread with:
  - Failure reason
  - Evidence file path(s)
  - Exact log snippet from the failing output file

---
