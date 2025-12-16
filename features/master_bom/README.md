---
title: "Master BOM"
feature: "Master BOM"
module: "Master BOM"
status: "active"
source: "NEPL V2"
last_verified: "2025-12-17"
owners: ["Niraj", "DevTeam"]
---

# Master BOM

**Sidebar Label:** Master BOM  
**Purpose:** Reusable BOM templates that can be copied into quotations as Proposal BOMs.

## Baseline Status
- **Status:** ✅ FROZEN
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 05–06
- **Total Files:** 12 (12 features + 0 changes)

### Primary References
- `_general/09_BOM_MODULE.md` - Complete module overview
- `_general/MASTER_BOM_BACKEND_DESIGN_INDEX.md` - Backend design index
- `structure/MASTER_BOM_BACKEND_DESIGN_PART3_STRUCTURE.md` - BOM structure
- `_general/MASTER_BOM_VS_PROPOSAL_BOM_SPECIFICATION.md` - Master vs Proposal BOM comparison

## Sub-Modules (Areas)

1. `_general/` — **General Overview** (module overview, foundation, comparison)
2. `structure/` — **Structure** (hierarchy, data models, BOM structure)
3. `items/` — **Items** (item rows, components, quantities - see README for current references)
4. `validation/` — **Validation** (business rules, constraints, validation rules)
5. `import_export/` — **Import/Export** (Excel import, bulk uploads, export formats)
6. `workflows/` — **Workflows** (create/edit/clone/approve flows, operations)
7. `reports/` — **Reports** (BOM summaries, print/export - none found yet)

## Rules (Documentation Governance)

- Folder names are **system-safe slugs** (no spaces, stable).
- This is a **shadow structure** (documentation-only). It does not affect application routing.
- Files can be **copied** into these folders without deleting originals.
- Master BOM items must use generic products only (ProductType = 1).
- Master BOM is always copied to quotations, never linked directly.

## Cross-links
- Related feature areas: Quotation (Proposal BOM), Component/Item Master (product linking)
- Change history: `changes/master_bom/` (data fixes, validation, migration notes)

