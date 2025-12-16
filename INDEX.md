# NSW Estimation Software — Documentation Index

**Repository:** NSW_Estimation_Software  
**Purpose:** Shadow repository for documenting, analyzing, and evolving NEPL Estimation Software into NSW Estimation Software  
**Status:** Phase 1 Complete ✅

---

## 📋 What This Repository Is

This is a **shadow repository** that serves as a documentation and analysis workspace for evolving the NEPL Estimation Software into NSW Estimation Software. It contains:

- **Documentation:** Curated feature documentation, workflows, and specifications
- **Change History:** Migration notes, fixes, and implementation artifacts
- **Trace Maps:** Feature-to-code mappings (Phase 2)
- **Analysis:** Gap analysis, improvement plans, and NSW specifications

**Important:** This repository does **not** modify the original `nish` repository. All changes are documented here for future NSW implementation.

---

## 🗂️ Repository Structure

```
NSW_Estimation_Software/
├── source_snapshot/     # Read-only mirror of nish repository
├── features/            # Curated feature documentation by module
├── changes/             # Change history, migrations, fixes
├── trace/               # Feature-to-code mappings (Phase 2)
├── docs/                # Documentation indices and summaries
└── scripts/             # Utility scripts (snapshot copy, etc.)
```

---

## 📚 Module Documentation

### Core Modules (Frozen Baselines)

| Module | Baseline Tag | README | Status |
|--------|-------------|--------|--------|
| **Component/Item Master** | `BASELINE_COMPONENT_ITEM_MASTER_20251217` | [`features/component_item_master/README.md`](features/component_item_master/README.md) | ✅ Frozen |
| **Quotation** | `BASELINE_QUOTATION_20251217` | [`features/quotation/README.md`](features/quotation/README.md) | ✅ Frozen |
| **Master BOM** | `BASELINE_MASTER_BOM_20251217` | [`features/master_bom/README.md`](features/master_bom/README.md) | ✅ Frozen |
| **Feeder Library** | `BASELINE_FEEDER_LIBRARY_20251217` | [`features/feeder_library/README.md`](features/feeder_library/README.md) | ✅ Frozen |
| **Proposal BOM** | `BASELINE_PROPOSAL_BOM_20251217` | [`features/proposal_bom/README.md`](features/proposal_bom/README.md) | ✅ Frozen |
| **Project** | `BASELINE_PROJECT_20251217` | [`features/project/README.md`](features/project/README.md) | ✅ Frozen |
| **Master** | `BASELINE_MASTER_20251217` | [`features/master/README.md`](features/master/README.md) | ✅ Frozen |
| **Employee/Role** | `BASELINE_EMPLOYEE_ROLE_20251217` | [`features/employee/README.md`](features/employee/README.md) | ✅ Frozen |

### Cross-Cutting Modules

| Module | README | Status |
|--------|--------|--------|
| **Security** | [`features/security/README.md`](features/security/README.md) | Cross-Cutting |

---

## 📖 Key Documentation

### Phase 1 — Baseline Capture

- **[Baseline Freeze Register](docs/PHASE_1/BASELINE_FREEZE_REGISTER.md)** - Complete list of frozen baselines
- **[Phase 1 Closure Summary](docs/PHASE_1/PHASE_1_CLOSURE_SUMMARY.md)** - Phase 1 completion summary
- **[Feature Index](features/FEATURE_INDEX.md)** - Quick reference to all module features
- **[Change Index](changes/CHANGE_INDEX.md)** - Change history by module

### Phase 2 — Traceability & Mapping

- **[Phase 2 Closure Summary](docs/PHASE_2/PHASE_2_CLOSURE_SUMMARY.md)** - Phase 2 completion summary
- **[Route Map](trace/phase_2/ROUTE_MAP.md)** - Route → Controller@Method → Module mapping (~80% coverage)
- **[Feature Code Map](trace/phase_2/FEATURE_CODE_MAP.md)** - Feature → Controllers → Services → Models → Views mapping
- **[File Ownership](trace/phase_2/FILE_OWNERSHIP.md)** - File ownership + risk level matrix (52 files)

### Trace Documentation (Phase 1)

- **[Batch Summaries](trace/phase_1/)** - Bifurcation summaries for each batch
- **[Baseline Freeze Notes](trace/phase_1/)** - Detailed freeze documentation for each module

---

## 🧭 How to Navigate

### For Feature Documentation

1. Start with **[Feature Index](features/FEATURE_INDEX.md)** for module overview
2. Navigate to specific module README (e.g., `features/quotation/README.md`)
3. Follow module-specific documentation structure

### For Change History

1. Start with **[Change Index](changes/CHANGE_INDEX.md)** for change overview
2. Navigate to module-specific change folders (e.g., `changes/quotation/v2/`)

### For Baseline Information

1. Check **[Baseline Freeze Register](docs/PHASE_1/BASELINE_FREEZE_REGISTER.md)** for all baselines
2. Review individual baseline freeze notes in `trace/` directory

---

## 🔍 Quick Links

### Module READMEs

- [Component/Item Master](features/component_item_master/README.md)
- [Quotation](features/quotation/README.md)
- [Master BOM](features/master_bom/README.md)
- [Feeder Library](features/feeder_library/README.md)
- [Proposal BOM](features/proposal_bom/README.md)
- [Project](features/project/README.md)
- [Master](features/master/README.md)
- [Employee/Role](features/employee/README.md)

### Documentation

- [Baseline Freeze Register](docs/PHASE_1/BASELINE_FREEZE_REGISTER.md)
- [Feature Index](features/FEATURE_INDEX.md)
- [Change Index](changes/CHANGE_INDEX.md)
- [Phase 1 Closure Summary](docs/PHASE_1/PHASE_1_CLOSURE_SUMMARY.md)

---

## 📊 Repository Statistics

- **Baselines Frozen:** 8
- **Cross-Cutting Modules:** 1 (Security)
- **Last Batch Completed:** 10C
- **Total Batches Executed:** 01-10C (with A/B/C suffixes)
- **Phase 1 Status:** ✅ Complete
- **Phase 2 Status:** ✅ Complete
- **Files Mapped (Phase 2):** 52 (Controllers + Services + Models)

---

## 🚀 Phase Status

**Phase 1:** ✅ Complete - Baseline Capture (8 modules frozen)  
**Phase 2:** ✅ Complete - Traceability & Mapping (Route/Feature/File ownership maps)  
**Phase 3:** 🔄 Next - NSW Implementation Planning

---

**Last Updated:** 2025-12-17 (IST)  
**Repository Status:** Phase 1 Complete ✅

