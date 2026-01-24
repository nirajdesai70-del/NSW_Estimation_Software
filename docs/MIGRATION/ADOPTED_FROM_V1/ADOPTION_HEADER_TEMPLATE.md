# Adoption Header Template (Zone C Intake)

**Scope:** Use this header when copying any V1.0 baseline artifact into Zone C (`docs/MIGRATION/ADOPTED_FROM_V1/…`).

**Rule:** Zone C items are **intake**. Promotion to Zone A happens later with `docs/GOVERNANCE/PATH_MOVE_REGISTER.md` entries + redirect stubs as needed.

---

## Markdown (`.md`) header (prepend at top)

```markdown
---
adoption:
  status: ADOPTED_FROM_V1
  adopted_on: 2026-01-21
  origin_root: "NSW Estimation Software V1.0"
  origin_path: "<V1_REL_PATH>"
  owner: "<OWNER>"
  reason: "Phase C intake (governance-controlled adoption)."
---

```

## YAML (`.yml/.yaml`) header (prepend at top)

```yaml
# adoption:
#   status: ADOPTED_FROM_V1
#   adopted_on: 2026-01-21
#   origin_root: "NSW Estimation Software V1.0"
#   origin_path: "<V1_REL_PATH>"
#   owner: "<OWNER>"
#   reason: "Phase C intake (governance-controlled adoption)."

```

## Python (`.py`) header (prepend at top)

```python
# adoption:
#   status: ADOPTED_FROM_V1
#   adopted_on: 2026-01-21
#   origin_root: "NSW Estimation Software V1.0"
#   origin_path: "<V1_REL_PATH>"
#   owner: "<OWNER>"
#   reason: "Phase C intake (governance-controlled adoption)."

```

## Shell (`.sh`) header (prepend at top, after shebang if present)

```bash
# adoption:
#   status: ADOPTED_FROM_V1
#   adopted_on: 2026-01-21
#   origin_root: "NSW Estimation Software V1.0"
#   origin_path: "<V1_REL_PATH>"
#   owner: "<OWNER>"
#   reason: "Phase C intake (governance-controlled adoption)."

```

