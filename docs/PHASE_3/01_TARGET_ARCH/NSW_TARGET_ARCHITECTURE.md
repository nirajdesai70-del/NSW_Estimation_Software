# NSW Target Architecture — Phase 3

**Repository:** NSW_Estimation_Software  
**Phase:** Phase 3 – Planning & Roadmap  
**Status:** DRAFT (Planning Only)  
**Date:** 2025-12-17 (IST)

---

## 1. Purpose

Define the target architecture for **NSW Estimation Software** as an evolution of **NEPL Estimation Software (nish)**, using:
- Phase 1 frozen baselines (what exists)
- Phase 2 traceability maps (how it works)
- FILE_OWNERSHIP risk rules (what must not break)

This document defines the target **logical architecture** (not code refactor instructions).

---

## 2. Architecture Goals

1. **Safety-first evolution**
   - Protect core costing and V2 hierarchy logic
2. **Module boundaries enforced**
   - One module owns one responsibility
3. **Cross-module touchpoints explicit**
   - Apply/reuse flows tested together
4. **Traceability-driven execution**
   - ROUTE_MAP + FEATURE_CODE_MAP + FILE_OWNERSHIP govern changes
5. **Operational clarity**
   - Reduce “hidden dependencies” and controller ambiguity

---

## 3. Non-Negotiable Constraints

- No changes to PROTECTED logic without approval gates
- No code duplication across modules
- No refactors that break Laravel conventions
- No “move everything” reorganization; adopt incremental, module-wise isolation

---

## 4. Target Logical Layers

### 4.1 Presentation Layer
- Blade views + modular JS assets
- Goal: consistent module-based UI structure (without breaking current)

### 4.2 Routing Layer
- Routes remain canonical entry points
- Goal: route groups clearly map to modules and sub-areas

### 4.3 Controller Layer
- Current controllers remain, but target state is:
  - module-scoped responsibilities
  - reduced shared controllers (except explicitly declared shared)

### 4.4 Service Layer
- Services hold business logic
- Target:
  - PROTECTED services remain stable
  - introduce wrappers/adapters for enhancements

### 4.5 Domain Model Layer
- Eloquent models for core entities
- Target:
  - stable core models
  - controlled additions only

### 4.6 Cross-Cutting Layer
- Security, audit, throttling, deletion policies
- Target:
  - central security module documentation
  - explicit policy enforcement

---

## 5. Canonical Modules (Target Names)

These modules are the official NSW structural units:

- Dashboard
- Component/Item Master
- Quotation (Legacy + V2)
- Master BOM
- Feeder Library
- Proposal BOM
- Project
- Master (Org/Vendor/PDF/Templates/Defaults)
- Employee/Role
- Security (Cross-cutting)
- Shared/Ops (Cross-cutting)

---

## 6. Cross-Module Touchpoints (Must Remain Explicit)

### 6.1 Quotation V2 Apply Flows
- applyMasterBom → touches Master BOM
- applyFeederTemplate → touches Feeder Library
- applyProposalBom → touches Proposal BOM

### 6.2 Reuse Search
- panels/feeders/master-boms/proposal-boms reuse endpoints

### 6.3 Shared Dropdown APIs
- category/item/product/make/series endpoints used by Legacy + V2

### 6.4 ImportController Split Ownership
- Import/Export (Component/Item Master)
- pdfcontain (Master/PDF)

---

## 7. Protected/Core Zone (Architecture Rule)

The following are “hands-off core” and can only be changed via wrapper approach:

### Services (PROTECTED)
- CostingService (SUM(AmountTotal) rule)
- QuotationQuantityService
- DiscountRuleApplyService
- QuotationDiscountRuleService
- DeletionPolicyService

### Controllers (PROTECTED/HIGH)
- QuotationV2Controller (PROTECTED)
- QuotationController (HIGH)
- ReuseController (HIGH)

### Core Models (PROTECTED/HIGH)
- Quotation, QuotationSale, QuotationSaleBom, QuotationSaleBomItem
- MasterBom, MasterBomItem
- Category, Product, Project (HIGH)

**Allowed pattern:** wrapper/adapters, not direct logic rewrites.

---

## 8. Target State Outcomes

At the end of NSW evolution, the system should have:

1. Clear module ownership for all routes and files
2. Cross-module flows validated as a single test group
3. Reduced coupling between catalog → templates → quotation execution
4. Stable protected core with extensibility through wrapper patterns
5. Documentation and traceability continuously updated

---

## 9. Architecture Acceptance Criteria (Phase 3)

This target architecture is accepted when:
- module boundaries are agreed and stable
- protected zones are enforced in planning documents
- cross-module touchpoints have test gating defined
- migration strategy supports safe staged execution

---

## 10. References

- `trace/phase_2/ROUTE_MAP.md`
- `trace/phase_2/FEATURE_CODE_MAP.md`
- `trace/phase_2/FILE_OWNERSHIP.md`
- `docs/PHASE_1/BASELINE_FREEZE_REGISTER.md`

