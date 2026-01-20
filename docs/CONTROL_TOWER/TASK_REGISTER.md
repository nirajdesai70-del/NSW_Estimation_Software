# Task Register (Append-Only)
## NSW Estimation Software — CI & Security Gates

**Rule:** Append-only. Don’t delete rows; mark DONE/DEFERRED/BLOCKED with date + proof.  
**Status:** PENDING | IN_PROGRESS | DONE | BLOCKED | DEFERRED

---

## Current “Next 10”
1) Keep CI green on PRs (security-gates + quality-gates)
2) Periodic ZAP target review & rules.tsv housekeeping
3) Add coverage trend badge (optional)
4) Add CODEOWNERS (optional)
5) Add release/tag policy note (optional)

---

## Task Table

| ID | Track | Title | Status | Gate / Proof | Primary Paths | Notes |
|---|---|---|---|---|---|---|
| GATE-20260119-001 | Tooling | Repo-local hooks wired (pre-commit, commit-msg, pre-push) | **DONE — 2026-01-20** | Hooks executable; local run green | `.githooks/*`, `.pre-commit-config.yaml`, `CONTRIBUTING.md`, `tools/cleanup_mac_artifacts.sh` | Uses `core.hooksPath=.githooks`; blocks macOS artifacts; runs `pre-commit` per stage. |
| CI-20260119-001 | CI | Security + Quality workflows green on PR | **DONE — 2026-01-20** | PR **#11** all checks passed | `.github/workflows/security.yml`, `.github/workflows/quality.yml`, `.github/workflows/ui-tests.yml` | Security: secrets_scan / sca_pip_audit / sast_bandit / ZAP. Quality: lint / types / backend-tests / frontend-build. |
| P9-SEC-001 | Security | SCA (pip-audit) severity gate + expiring waivers | **DONE — 2026-01-20** | SARIF emitted; gate via `tools/security/pip_audit_gate.py` | `tools/security/pip_audit_gate.py`, `WORKING_REVIEWED_SET/00_GOVERNANCE/{WAIVERS.md,waivers_sca.json}` | **HIGH** blocks; **MEDIUM** needs waiver; **LOW** non-blocking. |
| P9-SEC-001b | Security | ZAP: warn on non-main, **blocking on main** | **DONE — 2026-01-20** | First green on **main** run `21161866511`; required on main | `.github/workflows/security.yml`, `.zap/rules.tsv` | `continue-on-error` conditional; `-l HIGH`; artifacts uploaded. |
| GOV-E22-20260119-001 | Governance | Enable required checks on `main` | **DONE — 2026-01-20** | Required contexts set (`strict=true`) | Branch protection (GitHub settings) | Required: `security-gates / OWASP ZAP Baseline (warn-only)`, `security-gates / sca_pip_audit`, `security-gates / secrets_scan`, `security-gates / sast_bandit`, `quality-gates / python-lint`, `quality-gates / type-check`, `quality-gates / backend-tests`, `quality-gates / frontend-build`. UI tests remain optional. |
| GOV-E25A-20260119-001 | Governance | Coverage floor (backend) | **DONE — 2026-01-20** | `--cov-fail-under=70` enforced in CI | `.github/workflows/quality.yml` | Scope: `WORKING_REVIEWED_SET/backend/app`; uploads `coverage.xml`. |

---

## How to update
- Add new rows below, **never** edit existing text except status/date and proof.
- For ZAP: keep `.zap/rules.tsv` entries time-boxed with expiry notes.
- For SCA waivers: update `waivers_sca.json` with `rule_id`, `expires_on`, `owner`, `rationale`, `scope`, `link`.

