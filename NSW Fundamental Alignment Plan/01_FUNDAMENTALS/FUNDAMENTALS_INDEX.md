# Fundamentals Master Reference Pack — Index

**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** 📋 PLANNING MODE ONLY  
**Purpose:** Index of all files in the Fundamentals Master Reference Pack

---

## Master Reference Pack Contents

This pack contains 7 documents:

1. **[MASTER_FUNDAMENTALS_v2.0.md](./MASTER_FUNDAMENTALS_v2.0.md)** — ⭐ **MASTER DOCTRINE** — Complete fundamentals + catalog & resolution standard (v2.0, DRAFT FOR FREEZE) — **AUTHORITATIVE SOURCE**
2. **[MASTER_REFERENCE.md](./MASTER_REFERENCE.md)** — Complete layer documentation (purpose/definition/usage/procedure/files/gaps)
3. **[FILE_LINK_GRAPH.md](./FILE_LINK_GRAPH.md)** — Document dependency map and linking structure
4. **[GAP_REGISTERS_GUIDE.md](./GAP_REGISTERS_GUIDE.md)** — How to use gap registers (purpose/status/updates/layer mapping)
5. **[IMPLEMENTATION_MAPPING.md](./IMPLEMENTATION_MAPPING.md)** — Codebase implementation mapping (current state/target architecture/delta table/sequenced plan)
6. **[PATCH_APPENDIX_v1.1.md](./PATCH_APPENDIX_v1.1.md)** — Audit-safe guardrails, schema inference rules, legacy data integrity strategy
7. **[INDEX.md](./INDEX.md)** — This file (index of all pack contents)

---

## Quick Navigation

### By Layer

- **A. Category / Subcategory / Type(Item) / Attributes** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#a-category--subcategory--typeitem--attributes)
- **B. Item/Component List** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#b-itemcomponent-list-catalog--component-base-list)
- **C. Generic Item Master** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#c-generic-item-master)
- **D. Specific Item Master** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#d-specific-item-master)
- **E. Master BOM (generic)** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#e-master-bom-generic)
- **F. Master BOM (specific)** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#f-master-bom-specific)
- **G. Proposal BOM + Proposal Sub-BOM** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#g-proposal-bom--proposal-sub-bom)
- **H. Feeder BOM** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#h-feeder-bom)
- **I. Panel BOM** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md#i-panel-bom)

### By Topic

- **⭐ Master Doctrine (Fundamentals + Catalog + Resolution)** → See [MASTER_FUNDAMENTALS_v2.0.md](./MASTER_FUNDAMENTALS_v2.0.md) — **AUTHORITATIVE SOURCE**
- **Gap Registers** → See [GAP_REGISTERS_GUIDE.md](./GAP_REGISTERS_GUIDE.md)
- **Document Dependencies** → See [FILE_LINK_GRAPH.md](./FILE_LINK_GRAPH.md)
- **Implementation Status** → See [IMPLEMENTATION_MAPPING.md](./IMPLEMENTATION_MAPPING.md)
- **Layer Definitions** → See [MASTER_REFERENCE.md](./MASTER_REFERENCE.md)

---

## Most Important Existing Repo Files

### Canonical Hierarchy

- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Canonical BOM hierarchy (design-time vs runtime)
- `PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md` — Master→Instance mapping table

### Baseline Freeze

- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` — Fundamentals baseline bundle (frozen)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — NEPL canonical rules (frozen)

### Runbooks

- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md` — Execution window SOP
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` — Verification queries
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` — Verification checklist

### Verification SQL

- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` — Fundamentals verification queries (VQ-001 through VQ-005)
- `docs/FEEDER_BOM/PHASE2_2_VERIFICATION_SQL.md` — Feeder BOM verification SQL (R1/S1/R2/S2)

### Evidence Templates

- `PLANNING/PANEL_BOM/WINDOW_PB_EVIDENCE_HEADER_TEMPLATE.md` — Panel BOM evidence template
- `evidence/fundamentals/execution_window_20251222/` — Fundamentals evidence structure

### Gap Registers

- `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` — BOM gap register (primary)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` — Proposal BOM gap register
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` — Master BOM gap register

### Implementation Blueprints

- `PLANNING/GOVERNANCE/BOM_ENGINE_BLUEPRINT.md` — BOM Engine API design
- `PLANNING/GOVERNANCE/BOM_ENGINE_IMPLEMENTATION_PLAN.md` — Implementation plan
- `app/Services/BomEngine.php` — BOM Engine service (implementation)
- `app/Services/BomHistoryService.php` — History service (implementation)

### Layer-Specific Design Documents

- `PLANNING/FUNDAMENTS_CORRECTION/FEEDER_MASTER_BACKEND_DESIGN_v1.0.md` — Feeder Master design (frozen)
- `PLANNING/FUNDAMENTS_CORRECTION/PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md` — Proposal BOM Master design (frozen)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md` — Generic Item Master freeze
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND0_READINESS_v1.0_20251218.md` — Specific Item Master readiness

### Planning Tracks

- `PLANNING/PANEL_BOM/MASTER_INDEX.md` — Panel BOM master index
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` — Panel BOM planning track (PB0-PB6)
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_GAP_CORRECTION_TODO.md` — Fundamentals gap correction TODO (✅ COMPLETE)

### Resolution-B Documents

- `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md` — Resolution-B summary
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md` — Write gateway design
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_PATHS.md` — Write paths inventory

---

## How to Use This Pack

### For Understanding Fundamentals

1. **Start with [MASTER_FUNDAMENTALS_v2.0.md](./MASTER_FUNDAMENTALS_v2.0.md)** for the authoritative master doctrine (fundamentals + catalog + resolution standard)
2. Review **[MASTER_REFERENCE.md](./MASTER_REFERENCE.md)** to understand each layer (9 layers A-I)
3. Use **[FILE_LINK_GRAPH.md](./FILE_LINK_GRAPH.md)** to navigate document dependencies
4. Refer to **[GAP_REGISTERS_GUIDE.md](./GAP_REGISTERS_GUIDE.md)** to understand gap status

### For Implementation Planning

1. Review **[IMPLEMENTATION_MAPPING.md](./IMPLEMENTATION_MAPPING.md)** for current state and target architecture
2. Check **[GAP_REGISTERS_GUIDE.md](./GAP_REGISTERS_GUIDE.md)** for open gaps
3. Follow sequenced implementation plan in **[IMPLEMENTATION_MAPPING.md](./IMPLEMENTATION_MAPPING.md)**

### For Gap Management

1. Use **[GAP_REGISTERS_GUIDE.md](./GAP_REGISTERS_GUIDE.md)** to understand gap register structure
2. Check gap status in gap registers (see "Most Important Existing Repo Files" above)
3. Update gap registers during execution windows (see gap register update procedures)

### For Execution Windows

1. Review **[MASTER_REFERENCE.md](./MASTER_REFERENCE.md)** for layer definitions
2. Use verification queries from `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md`
3. Follow execution window SOP from `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md`
4. Capture evidence per evidence templates

---

## Document Relationships

### Master Reference Pack Documents

```
INDEX.md (This file)
    ↓
MASTER_REFERENCE.md (Main document)
    ├──→ FILE_LINK_GRAPH.md (Document dependencies)
    ├──→ GAP_REGISTERS_GUIDE.md (Gap management)
    └──→ IMPLEMENTATION_MAPPING.md (Codebase mapping)
```

### External Document References

- **Canonical Hierarchy** → Referenced by all layer sections
- **Gap Registers** → Referenced in GAP_REGISTERS_GUIDE.md
- **Implementation Blueprints** → Referenced in IMPLEMENTATION_MAPPING.md
- **Verification Queries** → Referenced in MASTER_REFERENCE.md (Planned Procedure sections)

---

## File Locations

### Master Reference Pack

**Location:** `PLANNING/FUNDAMENTS/MASTER_REFERENCE_PACK/`

**Files:**
- `MASTER_REFERENCE.md`
- `FILE_LINK_GRAPH.md`
- `GAP_REGISTERS_GUIDE.md`
- `IMPLEMENTATION_MAPPING.md`
- `INDEX.md` (this file)

### Related Directories

- `PLANNING/FUNDAMENTS_CORRECTION/` — Fundamentals correction documents
- `PLANNING/GOVERNANCE/` — Governance and gap registers
- `PLANNING/PANEL_BOM/` — Panel BOM planning
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/` — Frozen baseline documents
- `docs/FEEDER_BOM/` — Feeder BOM documentation
- `docs/RESOLUTION_B/` — Resolution-B documents
- `evidence/` — Evidence archive

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial index created for Fundamentals Master Reference Pack |
| v1.1 | 2025-12-XX | Added PATCH_APPENDIX_v1.1.md reference, date corrections |
| v1.2 | 2025-01-XX | Added MASTER_FUNDAMENTALS_v2.0.md as authoritative master doctrine reference |

---

**END OF INDEX**

