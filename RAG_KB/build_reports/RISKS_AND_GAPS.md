# Risks and Gaps Report

**Generated (UTC):** 2025-12-28T00:24:18.638946
**KB Version:** 1.0

## Blocking Issues
- None detected (baseline heuristics).

## High Priority Gaps

## Missing Front-Matter Headers
93 Phase-5 files are missing front-matter headers (Status/Version):
- `docs/PHASE_5/00_GOVERNANCE/ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md`
- `docs/PHASE_5/00_GOVERNANCE/DECISION_CAPTURE_RULES.md`
- `docs/PHASE_5/00_GOVERNANCE/EXPLORATION_MODE_SETUP_SUMMARY.md`
- `docs/PHASE_5/00_GOVERNANCE/FEATURE_DISCOVERY_LOG.md`
- `docs/PHASE_5/00_GOVERNANCE/FUNDAMENTALS_SOURCE_OF_TRUTH.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/INDEX.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/README.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.2.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_FINAL_RULES_v1.0.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_FINAL_RULES_v1.2.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L1_L2_EXPANSION_LOGIC_v1.0.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`
- `docs/PHASE_5/00_GOVERNANCE/Knowledge_Base/SCHNEIDER_V1.2_VERIFICATION_COMPLETE.md`
- `docs/PHASE_5/00_GOVERNANCE/LEGACY_VS_NSW_COEXISTENCE_POLICY.md`
- `docs/PHASE_5/00_GOVERNANCE/MASTER_DOCUMENTS_TO_PHASE5_MAPPING.md`
- `docs/PHASE_5/00_GOVERNANCE/NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md`
- `docs/PHASE_5/00_GOVERNANCE/PENDING_INPUTS_REGISTER.md`
- `docs/PHASE_5/00_GOVERNANCE/PHASE_4_5_FOLDER_MAPPING_GUIDE.md`
- `docs/PHASE_5/00_GOVERNANCE/PHASE_4_CLOSURE_VALIDATION_AUDIT.md`
- ... (73 more files)

**Recommendation:** Add front-matter headers with Status and Version to ensure proper ranking.

## Broken _ACTIVE_FILE.txt References
- None detected (all _ACTIVE_FILE.txt markers are valid).

## Coverage Notes
- Namespace `catalog_pipeline`: 2 files
- Namespace `changes`: 10 files
- Namespace `features`: 69 files
- Namespace `master_docs`: 2 files
- Namespace `phase5_docs`: 14 files
- Namespace `rag_governance`: 4 files
- Namespace `trace`: 3 files

## Input/Binary Handling
- PDFs/XLSX are summarized only (no binary ingestion). Add manual summaries for critical inputs if needed.

## Next Actions
- Promote true LOCKED decisions into `phase5_pack/02_DECISIONS_LOG.md`.
- Populate `03_FEATURE_FLAGS.md` from Phase-5 sources.
- After master + risks are stable, proceed to indexer/query upgrade.

