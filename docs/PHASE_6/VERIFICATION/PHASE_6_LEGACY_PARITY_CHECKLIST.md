# Phase-6 Legacy Parity Verification Checklist

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** VERIFICATION CHECKLIST  
**Purpose:** Ensure nothing that existed in legacy (Phase-1–4 + Nish) is missed during Phase-6 execution, while respecting Phase-5 Canon (no schema meaning change).

**Rule:** Legacy is reference, NSW Canon is authority.

---

## Legend

- **NSW Equivalent** = Where / how the legacy capability is handled in NSW
- **Phase-6 Task ID** = Track + task where this must be verified
- **Status** = To be filled during execution (⬜ Not Started / 🟡 In Progress / ✅ Verified)

---

## A. Quotation Lifecycle & Reuse (CRITICAL)

| # | Legacy Capability | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------------|----------------|-----------------|--------|
| A1 | Create quotation from scratch | Quotation Shell (quotations) | P6-UI-001 | ⬜ |
| A2 | Generate quotation from BOM | Apply Master BOM into quotation panel | P6-UI-009 / P6-UI-REUSE-005 | ⬜ |
| A3 | Copy old quotation and modify | Copy quotation (deep copy, copy-never-link) | P6-UI-REUSE-001 | ⬜ |
| A4 | Modify copied quotation freely | Edit copied hierarchy until locked | P6-UI-REUSE-001 / P6-UI-REUSE-006 | ⬜ |
| A5 | Quotation revisions (implicit) | ParentId / revision chain | Phase-5 Canon + P6-COST-EVAL | ⬜ |

---

## B. Panel / Feeder / BOM Reuse (POST-QUOTATION WORKFLOW)

| # | Legacy Capability | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------------|----------------|-----------------|--------|
| B1 | Create panel under project | Create panel under quotation | P6-UI-005 | ⬜ |
| B2 | Reuse panel from past project | Copy panel subtree into quotation | P6-UI-REUSE-002 | ⬜ |
| B3 | Create feeder under panel | Level-0 BOM under panel | P6-UI-008 | ⬜ |
| B4 | Reuse feeder from past project | Copy feeder (Level-0 BOM + subtree) | P6-UI-REUSE-003 | ⬜ |
| B5 | Create BOM under feeder | Level-1 / Level-2 BOM | P6-UI-009 | ⬜ |
| B6 | Reuse BOM from previous project | Copy BOM subtree under feeder | P6-UI-REUSE-004 | ⬜ |
| B7 | Use Master BOM template | Apply Master BOM (L1 only) | P6-UI-REUSE-005 | ⬜ |
| B8 | Create BOM inside quotation | Quote BOM creation (not template) | P6-UI-009 | ⬜ |

**✅ This directly reflects the clarification:**
"After quotation, either reuse existing structures or create fresh ones inside the quotation."

---

## C. BOM & Item Editability

| # | Legacy Capability | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------------|----------------|-----------------|--------|
| C1 | Add items under BOM | Add Quote BOM Items | P6-UI-010 | ⬜ |
| C2 | Edit item quantity | Editable Qty until locked | P6-UI-010 | ⬜ |
| C3 | Delete items | Allowed until locked | P6-UI-025 | ⬜ |
| C4 | Edit reused BOM items | Edit after copy | P6-UI-REUSE-004 / P6-UI-REUSE-006 | ⬜ |
| C5 | BOM edit tracking | origin_master_bom_id + is_modified | P6-BOM-TRACK-001 / P6-BOM-TRACK-002 | ⬜ |

---

## D. Pricing, Discount & Bulk Operations

| # | Legacy Capability | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------------|----------------|-----------------|--------|
| D1 | Base price on item | SKU price list | P6-UI-013 | ⬜ |
| D2 | Override unit price | MANUAL / FIXED RateSource | P6-UI-012 / P6-UI-014 / P6-UI-015 | ⬜ |
| D3 | Apply discount | Discount % (guardrail G-07) | P6-UI-014 | ⬜ |
| D4 | Bulk discount editing | Discount Editor screen | P6-DISC-001 → P6-DISC-004 | ⬜ |
| D5 | Discount approval | Approval flow (optional) | P6-OPS-004 / P6-DISC-004 | ⬜ |

---

## E. Quantity & Cost Semantics (ENGINE PARITY)

| # | Legacy / Excel Logic | NSW Equivalent | Phase-6 Task ID | Status |
|---|---------------------|----------------|-----------------|--------|
| E1 | Item qty per BOM | ItemQtyPerBom | Phase-5 Canon | ⬜ |
| E2 | BOM qty multiplier | BOM Qty chain | P6-COST-D0-001 | ⬜ |
| E3 | Feeder qty multiplier | Level-0 BOM Qty | P6-COST-D0-001 | ⬜ |
| E4 | Panel qty multiplier | Panel Qty | P6-COST-D0-001 | ⬜ |
| E5 | Excel-style total qty | EffectiveQtyTotal | P6-COST-D0-001 | ⬜ |
| E6 | Cost by category/make | QCD aggregation | P6-COST-007 | ⬜ |

---

## F. Masters & Catalog (Legacy → NSW)

| # | Legacy Menu | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------|----------------|-----------------|--------|
| F1 | Categories | Categories (CIM) | P6-CAT-005 | ⬜ |
| F2 | Subcategories | Subcategories | P6-CAT-005 | ⬜ |
| F3 | Types | Product Types | P6-CAT-005 | ⬜ |
| F4 | Attributes | Attributes + options | P6-CAT-005 | ⬜ |
| F5 | Items | L1 Intent Lines | P6-CAT-006 | ⬜ |
| F6 | Components | L2 SKUs | P6-CAT-006 | ⬜ |

---

## G. Navigation & Dashboard Parity

| # | Legacy Screen | NSW Equivalent | Phase-6 Task ID | Status |
|---|---------------|----------------|-----------------|--------|
| G1 | Dashboard home | Global dashboard | P6-COST-009 | ⬜ |
| G2 | Recent projects | Project / quotation list | P6-UI-001 | ⬜ |
| G3 | Recent quotations | Quotation list | P6-UI-001 | ⬜ |
| G4 | Cost summaries | Costing Pack | P6-COST-003 | ⬜ |

---

## H. Audit, History & Safety

| # | Legacy Capability | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------------|----------------|-----------------|--------|
| H1 | created_at / updated_at | Full audit trail | P6-OPS-007 / P6-OPS-008 | ⬜ |
| H2 | No delete protection | Line-item locking (D-005) | P6-UI-025 | ⬜ |
| H3 | No change history | Audit logs | P6-OPS-008 | ⬜ |

---

## I. Customer & Project Management (UX Parity)

| # | Legacy Capability | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------------|----------------|-----------------|--------|
| I1 | Customer contacts | customer_name_snapshot + metadata_json | P6-UI-001A / P6-UI-001B | ⬜ |
| I2 | Projects navigation | Project list / filters | P6-UI-001 | ⬜ |
| I3 | Project → Quotation link | Quotation list filtered by project | P6-UI-001 | ⬜ |

---

## J. Catalog UI Views (L1 vs L2 Separation)

| # | Legacy Menu | NSW Equivalent | Phase-6 Task ID | Status |
|---|-------------|----------------|-----------------|--------|
| J1 | "Items" menu | L1 Intent Lines view | P6-CAT-006 | ⬜ |
| J2 | "Components" menu | L2 SKUs view | P6-CAT-006 | ⬜ |
| J3 | Make/Series/SKU filters | Catalog filters | P6-CAT-006 | ⬜ |

---

## Final Verification Rule

Phase-6 is **COMPLETE** only when:

- ⬜ All rows above are marked ✅ Verified
- ⬜ No legacy workflow is blocked or impossible
- ⬜ No Phase-5 Canon rule is violated
- ⬜ Reuse + edit workflows work smoothly inside quotation
- ⬜ Legacy Parity Gate (P6-GATE-LEGACY-001 through P6-GATE-LEGACY-006) is PASSED

---

## Related Documents

- **Phase-6 Execution Plan:** `docs/PHASE_5/00_GOVERNANCE/PHASE_6_EXECUTION_PLAN.md`
- **Legacy Parity Gate:** Week 8.5 in Phase-6 Execution Plan
- **Nish System Reference:** `project/nish/NISH_SYSTEM_REFERENCE.md`
- **Nish Review Report:** `project/nish/PHASE_6_NISH_REVIEW_REPORT.md`

---

**Last Updated:** 2025-01-27  
**Status:** VERIFICATION CHECKLIST - Ready for Execution  
**Next Action:** Use this checklist during Phase-6 execution to verify legacy parity

