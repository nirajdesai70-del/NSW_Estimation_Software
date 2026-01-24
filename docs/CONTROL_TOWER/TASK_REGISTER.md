# Task Register (Append-Only)
## NSW Estimation Software — CI & Security Gates

**Rule:** Append-only. Don’t delete rows; mark DONE/DEFERRED/BLOCKED with date + proof.  
**Status:** PENDING | IN_PROGRESS | DONE | BLOCKED | DEFERRED

---

## Current “Next 10”
1) Keep CI green on PRs (security-gates + quality-gates)
2) Periodic ZAP target review & rules.tsv housekeeping
3) Add coverage trend badge (optional)
4) Add release/tag policy note (optional)
5) GOV-E22 Phase-1: conversation resolution + latest-push approval (2026-01-21)
6) GOV-E22 Phase-2: CODEOWNERS + code-owner reviews (2026-01-22)
7) GOV-E22 Phase-3: linear history + disable merge commits (2026-01-23)
8) GOV-E22 Phase-4 (optional): signed commits + no admin bypass (2026-01-30)

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
| GOV-ROLL-20260121-001 | Governance | Phase 1: require conversation resolution + latest push approval | PENDING | Branch rule updated (date + screenshot) | Branch protection (GitHub settings) | Low-friction hygiene; no impact on check runtime. |
| GOV-ROLL-20260121-002 | Governance | Phase 2: CODEOWNERS include collaborator + require code-owner reviews | PENDING | CODEOWNERS updated + rule enabled (date) | `.github/CODEOWNERS`, branch protection | Prevents self-approval deadlocks. |
| GOV-ROLL-20260121-003 | Governance | Phase 3: require linear history + disable merge commits | PENDING | Merge strategy + rule updated (date) | Repo settings → Merge button; Branch protection | Squash-only history. |
| GOV-ROLL-20260121-004 | Governance | Phase 4 (optional): signed commits + no admin bypass | PENDING | Rule updated + signed commit proof | Branch protection | Only after team signs commits reliably. |

---

## Governance Phases (Owners + Dates)

| ID | Track | Title | Status | Owner | Due | Gate / Proof | Notes |
|---|---|---|---|---|---|---|---|
| GOV-E22-P1-20260121 | Governance | Phase-1: Enable **Conversation Resolution** + **Latest-push approval** on `main` | PENDING | Repo Admin (Niraj) | 2026-01-21 | Branch protection JSON shows `"required_conversation_resolution":true` and `"require_last_push_approval":true` | No code changes. Toggle 2 checkboxes on the `main` branch rule. |
| GOV-E22-P2-20260122 | Governance | Phase-2: **CODEOWNERS** + **Require code-owner reviews** | PENDING | Repo Admin + Collaborator (code owner) | 2026-01-22 | PR adding `.github/CODEOWNERS` merged; branch rule shows `"require_code_owner_reviews":true` | CODEOWNERS: `* @nirajdesai70-del @zk7m4x5kzv-maker`. Ensure collaborator can approve PRs. |
| GOV-E22-P3-20260123 | Governance | Phase-3: **Linear history** + **Disable merge commits** (Squash-only) | PENDING | Repo Admin | 2026-01-23 | Branch rule shows `"required_linear_history":true`; repo settings allow squash only | Improves history hygiene; keeps blame clean. |
| GOV-E22-P4-20260130 | Governance | Phase-4 (optional): **Signed commits** + **No admin bypass** | PENDING | Repo Admin + Devs | 2026-01-30 | Branch rule shows `"required_signatures":true` and `"enforce_admins":true`; one green PR merged with verified commit | Turn on after team confirms signing setup. |

---

## How to update
- Add new rows below, **never** edit existing text except status/date and proof.
- For ZAP: keep `.zap/rules.tsv` entries time-boxed with expiry notes.
- For SCA waivers: update `waivers_sca.json` with `rule_id`, `expires_on`, `owner`, `rationale`, `scope`, `link`.

