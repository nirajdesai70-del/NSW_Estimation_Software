# NSW Estimation Software

![Security Gates](https://github.com/nirajdesai70-del/NSW_Estimation_Software/actions/workflows/security.yml/badge.svg)
![Quality Gates](https://github.com/nirajdesai70-del/NSW_Estimation_Software/actions/workflows/quality.yml/badge.svg)
![Coverage](docs/badges/coverage.svg)

**New Generation Software** - Evolved from NEPL Estimation Software V2

## Overview

NSW Estimation Software is a structured evolution of the NEPL Estimation Software, designed to preserve core V2 logic while adding enhancements, improvements, and new capabilities. This project follows a rigorous 5-phase framework to ensure zero regression risk and a clear evolution path.

---

## Project Structure

```
NSW_Estimation_Software/
├── docs/
│   ├── NSW_ESTIMATION_BASELINE.md          # Master baseline document (FROZEN)
│   ├── PHASE_1/                             # Restructure Present NEPL Work
│   │   ├── NEPL_CURRENT_STATE.md
│   │   ├── NEPL_DATA_STRUCTURE.md
│   │   └── NEPL_UI_BEHAVIOUR_MAP.md
│   ├── PHASE_2/                             # Legacy Analysis & Migration Trace
│   │   ├── LEGACY_SYSTEM_FACTS.md
│   │   └── MIGRATION_TRACE_REPORT.md
│   ├── PHASE_3/                             # Gap & Impact Analysis
│   │   ├── GAP_ANALYSIS.md
│   │   └── IMPACT_MATRIX.md
│   ├── PHASE_4/                             # Rectification Strategy
│   │   └── NEPL_RECTIFICATION_PLAN.md
│   └── PHASE_5/                             # NSW Readiness Extraction
│       └── NEPL_TO_NSW_EXTRACTION.md
└── README.md
```

---

## Framework Overview

This project follows a **5-Phase Restructuring → Analysis → Rectification Framework** to ensure a safe and structured evolution from NEPL V2 to NSW.

### Phase 1: Restructure Present NEPL Work
**Objective:** Establish a clean, factual snapshot of what actually exists today.

**Deliverables:**
- `NEPL_CURRENT_STATE.md` - Modules, screens, flows, and pain points
- `NEPL_DATA_STRUCTURE.md` - Data entities, relationships, and hierarchies
- `NEPL_UI_BEHAVIOUR_MAP.md` - UI interactions mapped to system behaviors

**Status:** ✅ Documentation templates created

---

### Phase 2: Legacy Analysis & Migration Trace
**Objective:** Understand what existed earlier and what was migrated, skipped, or altered.

**Deliverables:**
- `LEGACY_SYSTEM_FACTS.md` - Facts about the legacy system
- `MIGRATION_TRACE_REPORT.md` - Critical trace of migration decisions

**Status:** ✅ Documentation templates created

---

### Phase 3: Gap & Impact Analysis
**Objective:** Identify what broke, why, and what must be corrected.

**Deliverables:**
- `GAP_ANALYSIS.md` - Structural, behavioral, terminology, UI, and data gaps
- `IMPACT_MATRIX.md` - Impact assessment for each gap

**Status:** ✅ Documentation templates created

---

### Phase 4: Rectification Strategy (NEPL Only)
**Objective:** Define safe corrections without destabilizing production.

**Deliverables:**
- `NEPL_RECTIFICATION_PLAN.md` - Safe correction strategies

**Status:** ✅ Documentation templates created

---

### Phase 5: NSW Readiness Extraction
**Objective:** Derive NSW requirements from analyzed NEPL state.

**Deliverables:**
- `NEPL_TO_NSW_EXTRACTION.md` - What must remain, what can improve, what to avoid

**Status:** ✅ Documentation templates created

---

## Master Baseline Document

The **`NSW_ESTIMATION_BASELINE.md`** is the **FROZEN** structural baseline that governs all development. It defines:

- ✅ **What stays** (Core business logic, data structures, workflows)
- ✅ **What refines** (UI improvements, validation enhancements)
- ✅ **What extends** (AI layer, audit visibility, new features)
- ❌ **What's out of scope** (Pricing formula changes, data relationship rewrites)

**Rule:** This chart governs everything. No feature, UI change, or enhancement happens without mapping to this baseline.

---

## Core Principles

### 1. Logic First, UI Second
- Business logic drives UI
- UI never drives logic
- Logic is immutable

### 2. Additive Only
- Enhancements don't remove functionality
- Enhancements don't change existing behavior
- Enhancements only add new capabilities

### 3. Chart Governs Everything
- No feature without baseline mapping
- No change without baseline update
- Baseline is single source of truth

### 4. Zero Regression Risk
- All NEPL V2 functionality preserved
- All calculations remain exact
- All workflows maintained

---

## Structural Layers

### Layer 1 — Business Objects (Stable)
These do not change between NEPL → NSW:
- Category, Subcategory, Type, Attribute
- Item, Component
- BOM, Quotation, Project, Panel, Feeder

### Layer 2 — Logical Flow (Frozen)
Core V2 truth that must be preserved:
```
Project → Panel → Feeder → BOM → BOM Item → Item/Component
Category → Subcategory → Type → Attribute → Item
```

### Layer 3 — NSW Enhancements (Additive Only)
Where NSW differentiates without breaking NEPL:
- Validation matrices
- Dependency checks
- AI suggestion layer (non-blocking)
- Rule hints / warnings
- UI clarity improvements
- Audit visibility

---

## Versioning Model

- **NEPL V2** = Reference truth (baseline)
- **NSW v1.0** = Structured refinement (preserves all V2 logic)
- **NSW v1.x** = Enhancements only (additive changes)
- **NSW v2.0** = Only after full baseline freeze

---

## Getting Started

### For Developers

1. **Read the Master Baseline:** Start with `docs/NSW_ESTIMATION_BASELINE.md`
2. **Understand Current State:** Review Phase 1 documents
3. **Review Gaps:** Check Phase 3 documents for known issues
4. **Follow the Framework:** All changes must map to baseline

### For Project Managers

1. **Review Baseline:** Understand what's locked vs. what can change
2. **Track Progress:** Use phase documents to track completion
3. **Ensure Compliance:** Verify all changes map to baseline

### For Stakeholders

1. **Understand Scope:** Review baseline for in-scope vs. out-of-scope
2. **Review Enhancements:** Check Phase 5 for planned improvements
3. **Track Risks:** Review Phase 3 for identified gaps and impacts

---

## Next Steps

1. ✅ **Complete Phase 1:** Fill in actual NEPL V2 state data
2. ⏳ **Complete Phase 2:** Document legacy system and migration trace
3. ⏳ **Complete Phase 3:** Identify and analyze gaps
4. ⏳ **Complete Phase 4:** Create rectification plan
5. ⏳ **Complete Phase 5:** Extract NSW requirements
6. ⏳ **Begin NSW Development:** Based on completed baseline

---

## Important Notes

- **This is not a UI sketch or feature wishlist** - It's a transition map
- **All documentation must be completed** before NSW development begins
- **Baseline is FROZEN** - Changes require formal approval
- **No ad-hoc fixes** - Everything must map to baseline

---

## Contributing

All contributions must:
1. Map to the baseline document
2. Follow the 5-phase framework
3. Be additive only (no breaking changes)
4. Include proper documentation

---

## License

[To be determined]

---

## Contact

[To be added]

---

**Last Updated:** 2025-12-16
**Baseline Version:** 1.0 (FROZEN)
