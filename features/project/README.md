# Project Module

## Overview

The Project module manages projects, which link clients to quotations and organize work by project. Projects serve as containers for quotations and provide project-level orchestration, status management, and reporting.

## Key Concepts

- **Project = Container for Quotations**: Projects organize multiple quotations under a single project
- **Project ↔ Client Relationship**: Projects belong to clients (N:1 relationship)
- **Project ↔ Quotation Relationship**: Projects contain quotations (1:N relationship)
- **Project Numbering**: Sequential numbering system (YYMMDD### format)
- **Project Status**: Lifecycle management (create, edit, close, approvals)

## Baseline Status

- **Status:** ✅ FROZEN
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 09A + 10 (micro-batch)
- **Total Files:** 18 (15 features including 2 stubs + 3 changes)

> **Note:** "Total Files Frozen" counts module-curated artifacts only (feature docs, change docs, stubs). Git "Files Changed" includes scaffolding/README/index updates, folder structure, and other repository infrastructure files.

> **Note:** Batch 09A includes 13 files due to high-value backend design series coverage; Batch 10 micro-batch added 3 additional high-value files.

## Primary References

### General
- `_general/PROJECT_BACKEND_DESIGN_INDEX.md` - Master index for backend design series
- `_general/10_CLIENT_PROJECT_MODULE.md` - Complete module overview
- `_general/PROJECT_BACKEND_DESIGN_PART1_FOUNDATION.md` - Foundation and architecture
- `_general/PROJECT_BACKEND_DESIGN_PART10_INTERCONNECTIONS.md` - Interconnections and data flow

### Structure
- `structure/PROJECT_BACKEND_DESIGN_PART2_DATA_MODELS.md` - Data models and relationships
- `structure/PROJECT_BACKEND_DESIGN_PART3_STRUCTURE.md` - Project structure and hierarchy
- `structure/PROJECT_BACKEND_DESIGN_PART4_NUMBERING.md` - Project numbering system

### Workflows
- `workflows/PROJECT_BACKEND_DESIGN_PART8_OPERATIONS.md` - Project operations and workflows

### Linkage to Quotation
- `linkage_to_quotation/PROJECT_QUOTATION_ARCHITECTURE_ANALYSIS.md` - Architecture analysis
- `linkage_to_quotation/PROJECT_QUOTATION_API_USAGE.md` - API usage and integration

### Status/Approvals
- `status_approvals/PROJECT_BACKEND_DESIGN_PART5_RULES.md` - Business rules and validation
- `status_approvals/NEPL_PROJECT_CHANGE_MANAGEMENT_STANDARD.md` - Change management standard

### Reports
- `reports/COSTING_DASHBOARD_PROJECT_BRIEF.md` - Costing dashboard brief

## Change References

- `../changes/project/migration/PROJECT_ARCHITECTURE_COMPLETE.md` - Architecture fix completion
- `../changes/project/migration/PROJECT_ARCHITECTURE_FIX_SUMMARY.md` - Architecture fix summary
- `../changes/project/migration/PROJECT_V2_IMPLEMENTATION_PLAN.md` - V2 implementation plan

## Sub-Modules (Areas)

1. `_general/` — **General Overview** (index, module overview, foundation, interconnections)
2. `structure/` — **Structure** (data models, structure, numbering system)
3. `workflows/` — **Workflows** (operations, create/edit/close flows)
4. `linkage_to_quotation/` — **Linkage to Quotation** (architecture, API usage)
5. `status_approvals/` — **Status/Approvals** (rules, change management standard)
6. `reports/` — **Reports** (costing dashboard, summaries)
7. `permissions/` — **Permissions** (role/access rules - see README for references)
8. `milestones/` — **Milestones** (milestone definitions - see README for references)

## Directory Structure

```
features/project/
├── README.md (this file)
├── _general/ (4 files)
├── structure/ (3 files)
├── workflows/ (1 file)
├── linkage_to_quotation/ (2 files)
├── status_approvals/ (2 files)
├── reports/ (1 file)
├── permissions/ (README stub)
└── milestones/ (README stub)

changes/project/
├── migration/ (3 files - architecture fixes + V2 plan)
├── fixes/ (empty)
└── validation/ (empty)
```

## Next Steps

1. **Validation:** Review all placements and structure
2. **Next Module:** Proceed to next module bifurcation (Master: Org/Vendor/PDF, Employee/Role, etc.)
3. **Future Enhancement:** Add permissions/milestones docs if found

