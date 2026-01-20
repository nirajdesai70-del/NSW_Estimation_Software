# Waivers (Time‑Bound Exceptions)
## NSW Estimation Software V1.x

**Rule:** Waivers are the exception, not the default. Every waiver must be **owned**, **time‑bound**, and linked to a remediation issue.

---

## 1) SCA (pip-audit) waivers

**File:** `WORKING_REVIEWED_SET/00_GOVERNANCE/waivers_sca.json`

**Format (JSON list):**
- `rule_id`: vulnerability ID as reported in SARIF (`result.ruleId`) (e.g., `PYSEC-...` / `GHSA-...`)
- `expires_on`: ISO date `YYYY-MM-DD`
- `owner`: accountable person/team (email ok)
- `rationale`: why it is temporarily acceptable + mitigation plan
- `scope` (optional): requirements surface (path) or component scope
- `link` (optional): issue/PR URL tracking remediation

**Gating policy (Phase‑1):**
- **HIGH (CVSS ≥ 7.0)**: **always blocks** (no waivers).
- **MEDIUM (CVSS ≥ 4.0 and < 7.0)**: allowed **only with a valid (non-expired) waiver**.
- **LOW (< 4.0)**: non-blocking.

---

## 2) ZAP waivers

ZAP suppression/downgrade is managed in `.zap/rules.tsv` (see Security workflow).

