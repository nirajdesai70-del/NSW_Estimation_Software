# Phase 5 Requirement Traceability Matrix

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** DRAFT  
**Owner:** Phase 5 Senate  

## Purpose
Map every Phase 5 requirement to its source, coverage location, and evidence. Ensures no requirement is missed.

## Source of Truth
- **Canonical:** This is the authoritative requirement trace matrix

## Requirement Sources

1. **SPEC-5:** SPEC-5 Review & Working Draft
2. **Pending Upgrades:** Phase 5 Pending Upgrades Integration Guide
3. **TfNSW:** TfNSW context and estimation requirements
4. **Legacy:** Legacy system analysis (what not to do)
5. **Freeze Gate:** Freeze Gate Checklist requirements

---

## Requirement Trace Matrix

| Req ID | Source | Requirement | Covered In | Evidence | Status |
|--------|--------|-------------|------------|----------|--------|
| R-001 | Pending Upgrades | BOM Instance Identity (origin_master_bom_id, instance_sequence_no) | Data Dictionary: QuotationSaleBom entity | Schema: quote_boms table | ⏳ PENDING |
| R-002 | Pending Upgrades | BOM Modification Tracking (is_modified, modified_by, modified_at) | Data Dictionary: QuotationSaleBom entity | Schema: quote_boms table | ⏳ PENDING |
| R-003 | Pending Upgrades | Validation Guardrails G1-G7 | Data Dictionary: Validation Guardrails section | Rules documentation | ⏳ PENDING |
| R-004 | Pending Upgrades | CostHead System (cost_heads table + FKs) | Data Dictionary: CostHead entity | Schema: cost_heads table | ⏳ PENDING |
| R-005 | Pending Upgrades | CostHead Resolution Order | Data Dictionary: CostHead Rules | Business rules doc | ⏳ PENDING |
| R-006 | Pending Upgrades | AI Entities (ai_call_logs table) | Data Dictionary: AI entities | Schema: ai_call_logs table | ⏳ PENDING |
| R-007 | Pending Upgrades | IsLocked Field (scope decision) | Data Dictionary: Locking Policy | Schema: is_locked fields | ⏳ PENDING |
| R-008 | Pending Upgrades | Audit Trail (bom_change_logs) | Data Dictionary: Audit requirements | Schema: audit tables | ⏳ PENDING |
| R-009 | Freeze Gate | BOM Tracking Fields Verification | Freeze Evidence: Schema Verification | Schema DDL | ⏳ PENDING |
| R-010 | Freeze Gate | IsLocked Scope Declaration | Data Dictionary: Locking Policy | Decision register | ⏳ PENDING |
| R-011 | Freeze Gate | CostHead Resolution Order Documentation | Data Dictionary: CostHead Rules | Business rules doc | ⏳ PENDING |
| R-012 | Freeze Gate | Validation Guardrails G1-G7 Explicit Documentation | Data Dictionary: Validation Guardrails | Rules documentation | ⏳ PENDING |
| R-013 | Freeze Gate | AI Scope Declaration | Data Dictionary: AI entities | Scope declaration | ⏳ PENDING |
| R-014 | Freeze Gate | Module Ownership Matrix | Data Dictionary: Module Ownership Matrix | Ownership matrix doc | ⏳ PENDING |
| R-015 | Freeze Gate | Naming Conventions Documentation | Data Dictionary: Naming Conventions | Naming conventions doc | ⏳ PENDING |
| R-016 | SPEC-5 | Master BOM L0/L1 only (no ProductId) | Data Dictionary: Master BOM entity | Schema: master_bom_items constraints | ⏳ PENDING |
| R-017 | SPEC-5 | Copy-never-link rule | Data Dictionary: BOM Copy semantics | Business rules doc | ⏳ PENDING |
| R-018 | SPEC-5 | Multi-tenant design | Data Dictionary: Tenant isolation | Schema: tenant_id everywhere | ⏳ PENDING |
| R-019 | SPEC-5 | Master data governance (no auto-create, approval queue) | Data Dictionary: Master data governance | Governance rules doc | ⏳ PENDING |
| R-020 | TfNSW | Change/Variation Estimation support | Data Dictionary: Quotation entity | Schema: quotation tables | ⏳ PENDING |

---

## Coverage Summary

| Source | Total Requirements | Covered | Pending | % Complete |
|--------|-------------------|---------|---------|------------|
| Pending Upgrades | 8 | 0 | 8 | 0% |
| Freeze Gate | 7 | 0 | 7 | 0% |
| SPEC-5 | 4 | 0 | 4 | 0% |
| TfNSW | 1 | 0 | 1 | 0% |
| **Total** | **20** | **0** | **20** | **0%** |

---

## Next Actions

1. ⏳ Complete Step 1 (Data Dictionary) - will cover R-001 through R-020
2. ⏳ Complete Step 2 (Schema Design) - will provide evidence for all requirements
3. ⏳ Complete Freeze Gate verification - will mark requirements as verified
4. ⏳ Update trace matrix as work progresses

---

## Change Log
- v1.0: Created requirement trace matrix with initial requirements

