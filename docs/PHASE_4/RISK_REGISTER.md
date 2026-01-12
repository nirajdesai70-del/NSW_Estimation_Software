# Phase 4 — Risk Register

This file records **known risks** discovered during Phase‑4 execution, without mixing remediation into unrelated batches.

---

## RISK-DATA-001 — Legacy master data attachment / upload mapping drift

- **Title:** Tavase basic tables not properly attached / legacy uploads may be mis-mapped
- **Observed:** Potential FK/link inconsistencies or wrong landing tables for historical uploads (symptoms: “selection feels wrong” while flows still function).
- **Impact:** Catalog browsing, dropdown integrity, BOM reuse accuracy, reporting correctness.
- **Scope fence:** **Not part of S4 Batch‑2** (UI caller migration). Do **not** change schema/data/selection semantics inside S4 propagation work.
- **Next action (later):** Create a controlled read-only audit task (e.g., **DATA-INTEGRITY-001**) after S4/S5 propagation stabilizes:
  - orphan / missing-reference checks
  - verify expected relationships (Category/SubCategory/Item/Product/Make/Series)
  - map which legacy upload batch caused drift
  - decide correction strategy (data fix vs mapping fix vs both) with evidence/approvals







