# CI Maintenance Checklist

**Scope:** NSW_Estimation_Software
**Owner:** CI/Governance
**Purpose:** Keep gates healthy with low-touch, regularized checks.

---

## Day-0 (after merge)
- Confirm required checks on `main` (security + quality) show as required.
- Verify `docs/badges/coverage.svg` renders in README.
- Verify `CI_BOT_TOKEN` scope: repo-only + Contents/Pull requests/Workflows (R/W).

## Weekly (10–15 min)
- **Pipeline health:** Check latest `security.yml` + `quality.yml` main runs.
- **Badge PR flow:** Merge any open badge PR; note any new failure patterns.
- **ZAP target sanity:** Ensure `ZAP_TARGET_URL` resolves; prune expired entries in `.zap/rules.tsv`.
- **Coverage watch:** If coverage drops >3 pts, tag PRs with tests-needed.

## Monthly (30 min)
- **Token rotation:** Rotate `CI_BOT_TOKEN` (every 90 days) and test badge PR creation.
- **CODEOWNERS accuracy:** Update owners/paths if org or repo structure changed.
- **Threshold tune:** If coverage stable, consider raising floor by +5.

## Quarterly (60 min)
- **Security review:** Run ZAP with extended window; remove stale suppressions.
- **SCA waivers:** Review `docs/GOVERNANCE/waivers_sca.json` for expiries.
- **Workflow currency:** Bump core actions to latest minors and validate a green PR.

## Event-driven
- **Team changes:** Update `.github/CODEOWNERS`.
- **Policy changes:** Re-sync required check names if GitHub renames jobs.
- **ZAP target changes:** Update `ZAP_TARGET_URL` and run a main security job.

## Remediation (if needed)
- **Broken gate on main:** Open a Fix Gates PR (revert or hot-fix); no direct push.
- **Badge PR churn:** Only open badge PR when change ≥0.5% or run weekly.
