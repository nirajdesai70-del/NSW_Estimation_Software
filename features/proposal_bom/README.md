# Proposal BOM Module

## Overview

Proposal BOM (Bill of Materials) represents quotation-specific BOM instances created from Master BOM templates or reused from previous quotations. Unlike Master BOMs which are reusable templates, Proposal BOMs are independent instances that can be modified without affecting their source templates.

## Key Concepts

- **Proposal BOM = Quotation Instance**: Each Proposal BOM is tied to a specific quotation
- **Always Copy Rule**: When Master BOM is selected, components are copied (not linked)
- **Independence**: Changes to Master BOM don't affect existing Proposal BOMs
- **Reusability**: Proposal BOMs can be reused in new quotations
- **Promotion**: Modified Proposal BOMs can be promoted to Master BOM templates

## Baseline Status

- **Status:** ✅ FROZEN
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 08
- **Total Files:** 11 (9 features + 2 changes)

> **Note:** "Total Files Frozen" counts module-curated artifacts only (feature docs, change docs, stubs). Git "Files Changed" includes scaffolding/README/index updates, folder structure, and other repository infrastructure files.

## Primary References

### General
- `_general/V2_MASTER_BOM_VS_PROPOSAL_BOM_ANALYSIS.md` - Detailed comparison and analysis
- `_general/V2_MASTER_PROPOSAL_BOM_REVIEW_SUMMARY.md` - Review and analysis summary
- `_general/PROPOSAL_BOM_PHASE_2_FEATURES.md` - Phase 2 feature specifications

### Structure
- `structure/MASTER_BOM_BACKEND_DESIGN_PART4_COPY_PROCESS.md` - Copy process from Master BOM to Proposal BOM

### Workflows
- `workflows/V2_MASTER_PROPOSAL_BOM_FINAL_PLAN.md` - Final implementation plan
- `workflows/V2_MASTER_PROPOSAL_BOM_IMPLEMENTATION_PLAN.md` - Implementation plan
- `workflows/PROPOSAL_BOM_ENHANCEMENT_PLAN.md` - Enhancement plan
- `workflows/V2_PROPOSAL_BOM_SIDEBAR_AND_AUTO_NAMING_PLAN.md` - Sidebar and auto-naming plan

### Validation
- `validation/PROPOSAL_BOM_MULTI_FILTER_PROPOSAL.md` - Multi-filter search proposal

## Change References

- `../changes/proposal_bom/migration/PROPOSAL_BOM_COMPLETE_STATUS_REPORT.md` - Phase completion status report
- `../changes/proposal_bom/validation/PROPOSAL_BOM_PHASE_2_COMPLETE_ANALYSIS.md` - Phase 2 analysis
- `../changes/proposal_bom/validation/PROPOSAL_BOM_PHASE_2_REVIEW.md` - Phase 2 review

## Sub-Modules (Areas)

1. `_general/` — **General Overview** (analysis, review, features)
2. `structure/` — **Structure** (copy process, hierarchy)
3. `items/` — **Items** (item rows, components, quantities - see README for references)
4. `validation/` — **Validation** (filtering, rules, constraints)
5. `import_export/` — **Import/Export** (templates, bulk operations - see README for references)
6. `workflows/` — **Workflows** (create, reuse, promote, enhance)
7. `reports/` — **Reports** (export, print - see README for references)
8. `comparison/` — **Comparison** (Master BOM vs Proposal BOM - see README for references)

## Directory Structure

```
features/proposal_bom/
├── README.md (this file)
├── _general/ (3 files)
├── structure/ (1 file)
├── items/ (README stub)
├── validation/ (1 file)
├── import_export/ (README stub)
├── workflows/ (4 files)
├── reports/ (README stub)
└── comparison/ (README stub)

changes/proposal_bom/
├── migration/ (1 file - status report)
└── validation/ (2 files - phase analysis/review)
```

## Next Steps

1. **Validation:** Review all placements and structure
2. **Next Module:** Proceed to next module bifurcation (Project, Master, Employee/Role, etc.)
3. **Future Enhancement:** Add items/import/reports/comparison docs if found

