# Path Move Register (Append-Only)

**Rule:** Append-only. Never delete entries. Never rewrite history.

## Entries

| Date | From | To | Type | Status | Owner | Reason | Notes |
|---|---|---|---|---|---|---|---|
| 2026-01-21 | `V1:.githooks/README.md` | `docs/MIGRATION/ADOPTED_FROM_V1/.githooks/README.md` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |
| 2026-01-21 | `V1:.github/workflows/security.yml` | `docs/MIGRATION/ADOPTED_FROM_V1/.github/workflows/security.yml` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |
| 2026-01-21 | `V1:.pre-commit-config.yaml` | `docs/MIGRATION/ADOPTED_FROM_V1/.pre-commit-config.yaml` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |
| 2026-01-21 | `V1:CONTRIBUTING.md` | `docs/MIGRATION/ADOPTED_FROM_V1/CONTRIBUTING.md` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |
| 2026-01-21 | `V1:docs/CONTROL_TOWER/TASK_REGISTER.md` | `docs/MIGRATION/ADOPTED_FROM_V1/docs/CONTROL_TOWER/TASK_REGISTER.md` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |
| 2026-01-21 | `V1:tools/cleanup_mac_artifacts.sh` | `docs/MIGRATION/ADOPTED_FROM_V1/tools/cleanup_mac_artifacts.sh` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |
| 2026-01-21 | `V1:tools/security/pip_audit_gate.py` | `docs/MIGRATION/ADOPTED_FROM_V1/tools/security/pip_audit_gate.py` | ADOPTED_FROM_V1 | DONE | Phase-C | Intake lane copy (Zone C) | Promotion to Zone A pending review |

| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/.githooks/README.md` | `docs/MIGRATION/ADOPTED_FROM_V1/ROOT_CONFIGS/.githooks/README.md` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | Root config intake moved to ROOT_CONFIGS bucket |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/.github/workflows/security.yml` | `docs/MIGRATION/ADOPTED_FROM_V1/ROOT_CONFIGS/.github/workflows/security.yml` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | Root config intake moved to ROOT_CONFIGS bucket |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/.pre-commit-config.yaml` | `docs/MIGRATION/ADOPTED_FROM_V1/ROOT_CONFIGS/.pre-commit-config.yaml` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | Root config intake moved to ROOT_CONFIGS bucket |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/tools/cleanup_mac_artifacts.sh` | `tools/MIGRATION/ADOPTED_FROM_V1/cleanup_mac_artifacts.sh` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | Tool intake moved under tools/MIGRATION/ADOPTED_FROM_V1 |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/tools/security/pip_audit_gate.py` | `tools/MIGRATION/ADOPTED_FROM_V1/security/pip_audit_gate.py` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | Tool intake moved under tools/MIGRATION/ADOPTED_FROM_V1 |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/CONTRIBUTING.md` | `docs/MIGRATION/ADOPTED_FROM_V1/CONTRIBUTING.md` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | No-op (already correct Zone C doc intake) |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/docs/CONTROL_TOWER/TASK_REGISTER.md` | `docs/MIGRATION/ADOPTED_FROM_V1/docs/CONTROL_TOWER/TASK_REGISTER.md` | ZONE_C_PATH_FIX | ZONE_C_PATH_FIX | Phase-C | Align Zone C lanes per approved plan (docs vs tools vs root configs) | No-op (already correct Zone C doc intake) |

| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/docs/CONTROL_TOWER/TASK_REGISTER.md` | `docs/CONTROL_TOWER/TASK_REGISTER.md` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake + diff review | Docs-only promotion (no runtime impact) |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/CONTRIBUTING.md` | `CONTRIBUTING.md` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake + diff review | Docs-only promotion (no runtime impact) |

| 2026-01-21 | `tools/MIGRATION/ADOPTED_FROM_V1/security/pip_audit_gate.py` | `tools/security/pip_audit_gate.py` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake + dependency-first check | Created (no prior file); no baseline absolute paths |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/ROOT_CONFIGS/.github/workflows/security.yml` | `.github/workflows/security.yml` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake + dependency check (gate script exists) | Created (no prior file); references `tools/security/pip_audit_gate.py` |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/ROOT_CONFIGS/.pre-commit-config.yaml` | `.pre-commit-config.yaml` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake + light pre-check | Created (no prior file); requires local pre-commit install to activate |
| 2026-01-21 | `docs/MIGRATION/ADOPTED_FROM_V1/ROOT_CONFIGS/.githooks/README.md` | `.githooks/README.md` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake | Created (no prior file); documentation-only |
| 2026-01-21 | `tools/MIGRATION/ADOPTED_FROM_V1/cleanup_mac_artifacts.sh` | `tools/cleanup_mac_artifacts.sh` | PROMOTED_TO_ZONE_A | ACTIVE | Phase-C | Promoted after Zone C intake | Created (no prior file); ensure executable bit locally if needed |

| 2026-01-21 | `.github/workflows/security.yml` | `.github/workflows/security.yml` | POST_PROMOTION_ADJUSTMENT | ACTIVE | Phase-C | Align waivers to canonical governance path; remove legacy reference-pack surfaces from CI targets | Waivers now `docs/GOVERNANCE/waivers_sca.json`; removed `WORKING_REVIEWED_SET/...` requirements + bandit target |
| 2026-01-21 | `tools/security/pip_audit_gate.py` | `tools/security/pip_audit_gate.py` | POST_PROMOTION_ADJUSTMENT | ACTIVE | Phase-C | Align waivers to canonical governance path | Default waivers path now `docs/GOVERNANCE/waivers_sca.json` |

