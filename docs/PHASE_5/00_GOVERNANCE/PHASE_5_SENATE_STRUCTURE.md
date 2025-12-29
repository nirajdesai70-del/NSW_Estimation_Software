# Phase 5 Senate Structure - Visual Guide

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
Visual representation of the Phase 5 Senate folder structure and file organization.

## Source of Truth
- **Canonical:** This is the authoritative structure guide

---

## Complete Structure

```
docs/PHASE_5/
│
├── 00_GOVERNANCE/                          # Phase 5 governance, scope, decisions
│   ├── PHASE_5_CHARTER.md                  ✅ Created
│   ├── PHASE_5_SCOPE_FENCE.md              ⏳ Move from root
│   ├── PHASE_5_GLOSSARY.md                 ✅ Created
│   ├── PHASE_5_DECISIONS_REGISTER.md       ✅ Created
│   ├── PHASE_5_RISK_REGISTER.md            ✅ Created
│   ├── PHASE_5_DOC_INDEX.md                ✅ Created
│   ├── PHASE_5_MASTER_ALIGNMENT.md         ✅ Created
│   ├── PHASE_5_EXECUTION_CHECKLIST.md      ✅ Created
│   ├── PHASE_5_COMPLETE_ALIGNMENT_SUMMARY.md ✅ Created
│   ├── PHASE_5_EXECUTION_SUMMARY.md       ⏳ Move from root
│   ├── PHASE_5_READINESS_PACKAGE.md       ⏳ Move from root
│   ├── PHASE_5_READINESS_REVIEW_CONSOLIDATED.md ⏳ Move from root
│   ├── PHASE_5_TASK_LIST.md                ⏳ Move from root
│   ├── LEGACY_VS_NSW_COEXISTENCE_POLICY.md ⏳ Move from root
│   ├── SCOPE_SEPARATION.md                 ⏳ Move from root
│   ├── STAKEHOLDER_BRIEF_WHY_NO_LEGACY_MIGRATION.md ⏳ Move from root
│   ├── NSW_MASTER_DATA_CREATION_AND_IMPORT_GOVERNANCE.md ⏳ Move from root
│   ├── ADR-005_MASTER_DATA_GOVERNANCE_FIREWALL.md ⏳ Move from root
│   └── PHASE_4_CLOSURE_VALIDATION_AUDIT.md ⏳ Move from root
│
├── 01_REFERENCE/                            # Legacy review & TfNSW context (read-only)
│   ├── LEGACY_REVIEW/
│   │   ├── LEGACY_SYSTEM_OVERVIEW.md        ✅ Created (placeholder)
│   │   ├── LEGACY_DATA_MODEL_NOTES.md       ⏳ Create placeholder
│   │   ├── LEGACY_BOM_BEHAVIOR.md           ⏳ Create placeholder
│   │   ├── LEGACY_PRICING_LOGIC.md          ⏳ Create placeholder
│   │   ├── LEGACY_GAPS_ANTIPATTERNS.md      ✅ Created (placeholder)
│   │   ├── NEPL_TO_NSW_EXTRACTION.md       ⏳ Move from root
│   │   └── NISH_PENDING_WORK_EXTRACTED.md   ⏳ Move from root
│   └── TFNSW_CONTEXT/
│       ├── ESTIMATION_METHOD_NOTES.md       ⏳ Create placeholder
│       ├── CHANGE_VARIATION_RULES.md        ⏳ Create placeholder
│       └── AUDIT_EXPECTATIONS.md            ⏳ Create placeholder
│
├── 02_FREEZE_GATE/                          # Freeze verification & evidence
│   ├── SPEC_5_FREEZE_GATE_CHECKLIST.md     ⏳ Move from root
│   ├── SPEC_5_FREEZE_RECOMMENDATIONS.md    ⏳ Move from root
│   ├── PHASE_5_PENDING_UPGRADES_INTEGRATION.md ⏳ Move from root
│   └── FREEZE_EVIDENCE/
│       ├── SCHEMA_VERIFICATION.md          ✅ Created
│       ├── RULES_VERIFICATION.md           ✅ Created
│       └── OWNERSHIP_NAMING_VERIFICATION.md ✅ Created
│
├── 03_DATA_DICTIONARY/                      # Step 1 outputs (FROZEN when complete)
│   ├── NSW_DATA_DICTIONARY_v1.0.md         ⏳ Step 1 output
│   ├── VALIDATION_GUARDRAILS_G1_G7.md      ⏳ Step 1 output
│   ├── COSTHEAD_RULES.md                   ⏳ Step 1 output
│   ├── LOCKING_POLICY.md                   ⏳ Step 1 output
│   ├── NAMING_CONVENTIONS.md               ⏳ Step 1 output
│   └── MODULE_OWNERSHIP_MATRIX.md          ⏳ Step 1 output
│
├── 04_SCHEMA_CANON/                         # Step 2 outputs (FROZEN when complete)
│   ├── NSW_SCHEMA_CANON_v1.0.md            ⏳ Step 2 output
│   ├── ER_DIAGRAM/
│   │   ├── ER_MAIN.drawio                  ⏳ Step 2 output
│   │   ├── ER_MAIN.png                     ⏳ Step 2 output
│   │   └── ER_MAIN.pdf                     ⏳ Step 2 output
│   ├── TABLE_INVENTORY.csv                 ⏳ Step 2 output
│   └── SEED_DESIGN_VALIDATION.sql          ⏳ Step 2 output
│
├── 05_TRACEABILITY/                         # Requirement traceability matrices
│   ├── PHASE_5_REQUIREMENT_TRACE.md        ✅ Created
│   ├── FILE_TO_REQUIREMENT_MAP.csv         ✅ Created
│   └── LEGACY_TO_CANONICAL_MAP.md          ✅ Created
│
├── 06_IMPLEMENTATION_REFERENCE/              # Post-Phase 5 planning (reference only)
│   ├── SPEC_5_REVIEW_AND_WORKING_DRAFT.md  ⏳ Move from root
│   ├── POST_PHASE_5_IMPLEMENTATION_ROADMAP.md ⏳ Move from root
│   ├── API_DESIGN_REFERENCE.md             ⏳ Extract from SPEC-5
│   ├── UI_WIREFRAME_REFERENCE.md           ⏳ Extract from SPEC-5
│   ├── CI_CD_REFERENCE.md                  ⏳ Extract from SPEC-5
│   └── DEPLOYMENT_REFERENCE.md             ⏳ Extract from SPEC-5
│
├── 99_ARCHIVE/                              # Superseded documents
│   ├── DRAFTS/
│   │   ├── README.md                       ⏳ Move from root
│   │   └── QUICK_REFERENCE.md              ⏳ Move from root
│   └── SUPERSEDED/
│
└── README.md                                ✅ Created (new senate README)

Legend:
✅ = Created/Complete
⏳ = Pending (move/create/extract)
```

---

## File Status Summary

### Created (15 files)
- Governance: 9 files
- Traceability: 3 files
- Freeze Evidence: 3 files

### To Move (15 files)
- Governance: 9 files
- Freeze Gate: 3 files
- Legacy Reference: 2 files
- Implementation Reference: 2 files
- Archive: 2 files

### To Create (18 files)
- Legacy Review: 4 placeholders
- TfNSW Context: 3 placeholders
- Data Dictionary: 6 outputs (Step 1)
- Schema Canon: 6 outputs (Step 2)
- Implementation Reference: 4 extracts

---

## Change Log
- v1.0: Created structure guide

