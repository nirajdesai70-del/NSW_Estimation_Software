---
title: "Feeder Library"
feature: "Feeder Library"
module: "Feeder Library"
status: "active"
source: "NEPL V2"
last_verified: "2025-12-17"
owners: ["Niraj", "DevTeam"]
---

# Feeder Library

**Sidebar Label:** Feeder Library  
**Purpose:** Define feeder templates, structure, rules, and how feeders integrate with BOM & Quotation V2.

## Baseline Status
- **Status:** ✅ FROZEN
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 07
- **Total Files:** 10 (4 features + 6 changes)

### Primary References
- `_general/V2_FEEDER_LIBRARY_COMPREHENSIVE_ANALYSIS.md` - Comprehensive analysis and current state
- `_general/V2_FEEDER_LIBRARY_CONSOLIDATED_EXECUTION_PLAN.md` - Consolidated execution plan and strategy

### Change References
- `../changes/feeder_library/validation/V2_FEEDER_IMPLEMENTATION_GAP_ANALYSIS.md` - Implementation gap analysis
- `../changes/feeder_library/validation/V2_FEEDER_LEVEL_MISSING_ANALYSIS.md` - Missing level analysis
- `../changes/feeder_library/validation/V2_STEP_PAGE_FEEDER_ISSUE_ANALYSIS.md` - Step page issue analysis
- `../changes/feeder_library/validation/V2_FEEDER_LIBRARY_PHASE_1_2_COMPLETE.md` - Phase 1 & 2 completion status
- `../changes/feeder_library/validation/V2_FEEDER_LIBRARY_PHASE_3_COMPLETE.md` - Phase 3 completion status
- `../changes/feeder_library/validation/V2_FEEDER_LIBRARY_PHASE_1_2_TEST_RESULTS.md` - Phase 1 & 2 test results

## Sub-Modules (Areas)

1. `_general/` — **General Overview** (comprehensive analysis, strategy, execution plans)
2. `structure/` — **Structure** (hierarchy, levels, template structure - see README for references)
3. `items/` — **Items** (item rows, components, quantities - see README for references)
4. `validation/` — **Validation** (business rules, constraints - see changes/validation for analysis docs)
5. `import_export/` — **Import/Export** (import/export templates - see README for references)
6. `workflows/` — **Workflows** (create/edit/clone flows, execution plans, testing guides)
7. `reports/` — **Reports** (reports, summaries - see README for references)

## Rules (Documentation Governance)

- Folder names are **system-safe slugs** (no spaces, stable).
- This is a **shadow structure** (documentation-only). It does not affect application routing.
- Files can be **copied** into these folders without deleting originals.
- Feeder Library uses `master_boms` table with `TemplateType='FEEDER'` (no new tables).
- Feeder templates are canonical (Qty=1 in library, regardless of source Qty).

## Cross-links
- Related feature areas: Master BOM (template structure), Quotation V2 (feeder integration), Proposal BOM
- Change history: `changes/feeder_library/validation/` (gap analysis, missing level, issues, phase completion)

