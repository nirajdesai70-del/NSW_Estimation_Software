# Fundamentals File Link Graph — Document Dependency Map

**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** 📋 PLANNING MODE ONLY  
**Purpose:** Linking map showing how documents connect across the whole fundamentals stack

---

## ASCII Dependency Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNDAMENTALS STACK                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   BASELINE    │   │   GOVERNANCE │   │  IMPLEMENTATION│
│   FREEZE      │   │   & GAPS     │   │   & SERVICES  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│              CANONICAL HIERARCHY                              │
│  (Design-time Masters → Runtime Instances)                    │
└──────────────────────────────────────────────────────────────┘
        │
        ├─── Panel Master → Proposal Panel
        ├─── Feeder Master → Feeder Instance
        ├─── BOM Master → Proposal BOM
        └─── Item Master → Proposal BOM Item
```

---

## Concept → Primary File → Supporting Files → Downstream Dependents

### A. Category / Subcategory / Type(Item) / Attributes

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Category/Subcategory/Item Rules** | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md` | Generic Item Master<br>Specific Item Master<br>Master BOM<br>Proposal BOM |

### B. Item/Component List

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Product Catalog** | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md` | Generic Item Master<br>Specific Item Master |

### C. Generic Item Master

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Generic Item Master (L0/L1)** | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md` | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_FINAL_v1.0_20251218.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` | Master BOM<br>Proposal BOM (L1→L2 resolution) |

### D. Specific Item Master

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Specific Item Master (L2)** | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND0_READINESS_v1.0_20251218.md` | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND1_CHECKLIST.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND1_KICKOFF_TEMPLATE.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` | Proposal BOM |

### E. Master BOM (generic)

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Master BOM (L1)** | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md` | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` | Proposal BOM |

### F. Master BOM (specific)

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Master BOM (specific)** | **NOT FOUND IN REPO (needs decision)** | N/A | N/A |

### G. Proposal BOM + Proposal Sub-BOM

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Proposal BOM (L2)** | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CORRECTION_PLAN_v1.0_2025-12-19.md` | `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md`<br>`docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_HIERARCHY_CLARIFICATION_v1.0_2025-12-19.md`<br>`docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md`<br>`docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` | Feeder BOM<br>Panel BOM |

### H. Feeder BOM

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Feeder Master** | `PLANNING/FUNDAMENTS_CORRECTION/FEEDER_MASTER_BACKEND_DESIGN_v1.0.md` | `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md`<br>`PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`<br>`docs/FEEDER_BOM/` | Panel BOM |

### I. Panel BOM

| Concept | Primary File | Supporting Files | Downstream Dependents |
|---------|-------------|-----------------|----------------------|
| **Panel BOM** | `PLANNING/PANEL_BOM/MASTER_INDEX.md` | `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md`<br>`PLANNING/PANEL_BOM/PANEL_BOM_TODO_TRACKER.md`<br>`PLANNING/PANEL_BOM/GATES_TRACKER.md`<br>`PLANNING/PANEL_BOM/CANONICAL_FLOW.md`<br>`PLANNING/PANEL_BOM/COPY_RULES.md`<br>`PLANNING/PANEL_BOM/QUANTITY_CONTRACT.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md`<br>`PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md` | Proposal BOM Master |

---

## Bridge Documents (Critical Cross-References)

### 1. Canonical Hierarchy

**File:** `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md`

**Purpose:** Defines the complete design-time vs runtime hierarchy

**Bridges:**
- Design-time masters (Panel Master, Feeder Master, BOM Master)
- Runtime instances (Proposal BOM Master, Proposal Panels, Feeder Instances, Proposal BOMs)
- Copy-never-link rules
- Hierarchy rules

**Referenced by:**
- All layer design documents
- Master→Instance mapping
- Fundamentals baseline bundle
- Panel BOM planning
- Feeder BOM planning

---

### 2. Master→Instance Mapping

**File:** `PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md`

**Purpose:** Complete mapping table showing master→instance relationships

**Bridges:**
- L0: Panel Master → Proposal Panel
- L1: Feeder Master → Feeder Instance
- L2: BOM Master → Proposal BOM
- L2 Items: Item Master → Proposal BOM Item
- Root: Proposal BOM Master (QuotationId)

**Referenced by:**
- Fundamentals baseline bundle
- Verification queries
- Panel BOM planning
- Feeder BOM planning

---

### 3. Fundamentals Baseline Bundle

**File:** `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md`

**Purpose:** Canonical fundamentals baseline (Feeder Master, Proposal BOM Master, hierarchy, mapping)

**Bridges:**
- Feeder Master definition
- Proposal BOM Master definition
- Canonical hierarchy
- Master→Instance mapping
- Gap fix plan
- Verification framework

**Referenced by:**
- All fundamentals documents
- Execution window SOP
- Verification queries
- Verification checklist
- Patch plan

---

### 4. NEPL Canonical Rules

**File:** `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md`

**Purpose:** Single source of truth for all NEPL governance rules

**Bridges:**
- L0/L1/L2 layer definitions
- Master BOM vs Proposal BOM rules
- Resolution-B rules
- Transitional state rules
- Code enforcement rules

**Referenced by:**
- All NEPL standards documents
- Generic Item Master
- Specific Item Master
- Master BOM
- Proposal BOM
- Gap registers

---

### 5. BOM Engine Blueprint

**File:** `PLANNING/GOVERNANCE/BOM_ENGINE_BLUEPRINT.md`

**Purpose:** Centralized service API design for BOM operations

**Bridges:**
- Copy operations (Master BOM → Proposal BOM, Proposal BOM → Proposal BOM, Feeder, Panel)
- Line item operations (add/edit/delete/replace)
- BOM node operations (update)
- History operations (backup & history)
- Lookup pipeline operations

**Referenced by:**
- BOM gap register
- Implementation plan
- Controller integration patterns

---

### 6. Execution Packs

**Execution Window SOP:**
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md` — Fundamentals execution window
- `docs/FEEDER_BOM/PHASE2_EXECUTION_CHECKLIST.md` — Feeder BOM execution
- `PLANNING/PANEL_BOM/GATES_TRACKER.md` — Panel BOM execution gates

**Evidence Templates:**
- `PLANNING/PANEL_BOM/WINDOW_PB_EVIDENCE_HEADER_TEMPLATE.md` — Panel BOM evidence template
- `evidence/fundamentals/execution_window_YYYYMMDD/` — Fundamentals evidence structure

**Bridges:**
- Planning documents → Execution procedures
- Verification queries → Evidence capture
- Execution gates → Closure criteria

---

## Document Dependency Flow

### Design-Time → Runtime Flow

```
NEPL Canonical Rules
    ↓
Generic Item Master (L0/L1)
    ↓
Master BOM (L1)
    ↓
Feeder Master (L1)
    ↓
Panel Master (L0)
    ↓
┌─────────────────────────────────────┐
│   CANONICAL HIERARCHY              │
│   (Design-time → Runtime mapping)  │
└─────────────────────────────────────┘
    ↓
Proposal BOM Master (QuotationId)
    ↓
Proposal Panel (L0)
    ↓
Feeder Instance (L1)
    ↓
Proposal BOM (L2)
    ↓
Proposal BOM Item (L2, ProductType=2)
```

### Governance → Implementation Flow

```
BOM Principle Locked
    ↓
BOM Gap Register
    ↓
BOM Engine Blueprint
    ↓
BOM Engine Implementation Plan
    ↓
Controller Integration
    ↓
Verification & Evidence
```

### Gap Correction → Execution Flow

```
Fundamentals Gap Correction TODO
    ↓
Fundamentals Baseline Bundle
    ↓
Verification Queries
    ↓
Verification Checklist
    ↓
Execution Window SOP
    ↓
Patch Plan (conditional)
    ↓
Evidence Capture
    ↓
Closure Declaration
```

---

## Key File Categories

### Baseline Freeze Documents
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/` — All frozen baseline documents
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` — Fundamentals baseline

### Governance Documents
- `PLANNING/GOVERNANCE/BOM_PRINCIPLE_LOCKED.md` — BOM principle (5 rules)
- `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` — BOM gap register
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` — Proposal BOM gaps
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` — Master BOM gaps

### Implementation Documents
- `PLANNING/GOVERNANCE/BOM_ENGINE_BLUEPRINT.md` — BOM Engine API design
- `PLANNING/GOVERNANCE/BOM_ENGINE_IMPLEMENTATION_PLAN.md` — Implementation plan
- `app/Services/BomEngine.php` — BOM Engine service (implementation)
- `app/Services/BomHistoryService.php` — History service (implementation)

### Verification Documents
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` — Verification queries
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` — Verification checklist
- `docs/FEEDER_BOM/PHASE2_2_VERIFICATION_SQL.md` — Feeder BOM verification SQL

### Execution Documents
- `PLANNING/FUNDAMENTS_CORRECTION/EXECUTION_WINDOW_SOP.md` — Execution window SOP
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_PLAN.md` — Patch plan
- `PLANNING/FUNDAMENTS_CORRECTION/PATCH_REGISTER.md` — Patch register

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial file link graph created from repository content |

---

**END OF FILE LINK GRAPH**

