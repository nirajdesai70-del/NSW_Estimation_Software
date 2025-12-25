# PATCH REGISTER — FUNDAMENTALS (Phase-0)

**Project:** NSW Estimation Software  
**Status:** 📋 Register (Planning → Execution Evidence)  
**Rule:** If any patch is applied, it MUST be logged here with evidence pointers.  
**Baseline:** FUNDAMENTALS_BASELINE_BUNDLE_v1.0

---

## 1) Patch Register Table

| Patch ID | Patch Name | Trigger (Verification) | Status | Applied In Window | Commit / Ref | Evidence Path | Notes |
|---------|------------|------------------------|--------|-------------------|--------------|--------------|------|
| P1 | Feeder Template Filter Standardization | VQ-005 (unexpected non-FEEDER template usage) | PLANNED | — | — | — | Enforce TemplateType='FEEDER' in all feeder template fetches |
| P2 | Quotation Ownership Enforcement | VQ-004 (QuotationId IS NULL) / VQ-003 ownership mismatch | PLANNED | — | — | — | Guardrails + optional repair script (requires explicit approval) |
| P3 | Copy-Never-Link Enforcement Guard | VQ-005 indicates master mutation risk | PLANNED | — | — | — | Service-layer guard: reject writes to master_boms in quotation context |
| P4 | Legacy Data Normalization (Last Resort) | Any systemic legacy corruption found | PLANNED | — | — | — | Requires separate approval + backup + rollback-ready |

---

## 2) Patch Logging Rules (LOCKED)

When any patch is applied, you must fill:
- Applied In Window (e.g., fundamentals_execution_window_YYYYMMDD)
- Commit / Ref (commit hash or patch artifact)
- Evidence Path (before/after VQ outputs + screenshots)
- Notes (what was changed + why)

If NO patches are applied:
- Leave Status = PLANNED
- Add a single note in execution summary: "No patches triggered; baseline verified."

---

## 3) Execution Window Notes

**Execution Window:** fundamentals_execution_window_20251222
- No patches applied.
- VQ-005 revealed legacy TemplateType NULL rows.
- Logged as future normalization (not Phase-0 blocking).

END

