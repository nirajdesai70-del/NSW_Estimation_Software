# Authority Matrix (Canonical)

**Purpose:** Single source of truth for “where to look” and “what is authoritative”.

## Core rules
- **Zone A is truth** (canonical operational work).
- **Zone C is intake** (adopted-from-V1 items must be promoted or remain explicitly intake).
- **Zone B is reference only** (legacy is never authoritative).
- **V1.0 folder is baseline reference only** (external; never edited as part of execution).

## Authority table
| Topic | Authority (SoT) | Allowed secondary | Disallowed |
|---|---|---|---|
| Execution docs | `docs/PHASE_*`, `docs/MASTER_EXECUTION_PLAN.md` | `docs/MIGRATION/ADOPTED_FROM_V1/` (temporary) | Direct links into external V1.0 paths |
| Governance rules | `docs/GOVERNANCE/` | — | Legacy as SoT |
| SCA waivers (pip-audit) | `docs/GOVERNANCE/waivers_sca.json` | — | Any waivers under `WORKING_REVIEWED_SET/`, `legacy/`, or external V1.0 paths |
| Ports & endpoints | `ops/ports.env` + `docs/CONTROL_TOWER/PORT_REGISTRY.md` | Compose files (must match ports.env) | Doc-only drift, baseline-only port docs |
| Link audits | `docs/MIGRATION/LINK_AUDIT/` | — | Ignoring broken links in `docs/` |
| Trace maps | `trace/phase_2/` | — | Ad-hoc copies |

