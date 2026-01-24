# Security Promotion Plan

**Status:** ACTIVE  
**Owner:** Security Gates  
**Scope:** Security gates promotion rules and rollout log

---

## Rollout Log (Append-Only)

- 2026-01-20 — ZAP Baseline promoted to blocking on `main` and added as a required status check. Non-main branches remain warn-only. First green proof run: 21161866511.
- 2026-01-24 — Reverted direct commit that added `docs/badges/.keep` via PR **#28** (revert **5d420d0**). Guardrail reaffirmed: PR-only on `main`; badge updates via CI-opened PR.