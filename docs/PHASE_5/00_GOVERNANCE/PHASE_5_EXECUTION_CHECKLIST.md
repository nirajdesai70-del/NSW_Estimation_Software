# Phase 5 Execution Checklist

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
Step-by-step checklist to ensure Phase 5 execution is complete and nothing is missed.

## Source of Truth
- **Canonical:** This is the authoritative execution checklist

---

## Pre-Execution (Governance)

- [x] Phase 5 scope fence approved
- [x] Phase 5 readiness review complete
- [x] Senate structure created
- [x] Governance documents created
- [x] Traceability framework created
- [ ] Legacy review framework ready
- [ ] Freeze gate checklist ready

---

## Step 1: Freeze NSW Canonical Data Dictionary

### Preparation
- [ ] Review Pending Upgrades Integration Guide (Section 1)
- [ ] Review Freeze Gate Checklist (requirements)
- [ ] Review Legacy Gaps & Anti-Patterns

### Entity Definitions
- [ ] CIM entities (Category/SubCategory/Type/Attribute)
- [ ] Product model (Generic vs Specific)
- [ ] Master BOM vs Quote BOM semantics
- [ ] BOM hierarchy and relationships

### Business Rules
- [ ] Copy-never-link rule
- [ ] Multi-SKU explosion semantics
- [ ] Editability + history rules
- [ ] Validation Guardrails G1-G7 (explicit)
- [ ] CostHead semantics + precedence
- [ ] IsLocked semantics (scope decision)
- [ ] Master data governance rules

### Documentation
- [ ] Module ownership matrix
- [ ] Naming conventions
- [ ] All entities documented
- [ ] All relationships documented
- [ ] All business rules documented

### Deliverable
- [ ] `NSW_DATA_DICTIONARY_v1.0.md` complete
- [ ] All Step 1 requirements covered (trace matrix)
- [ ] Data Dictionary approved
- [ ] Data Dictionary FROZEN

---

## Step 2: Define NSW Canonical Schema

### Preparation
- [ ] Data Dictionary FROZEN (Step 1 complete)
- [ ] Review Pending Upgrades Integration Guide (Section 2)
- [ ] Review Freeze Gate Checklist (schema requirements)

### Schema Design
- [ ] Core schema (tenant, auth, RBAC)
- [ ] CIM master tables
- [ ] Pricing tables (effective dating)
- [ ] Master BOM tables
- [ ] Quote BOM + BOM tracking fields
- [ ] History + audit tables
- [ ] CostHead tables + FKs
- [ ] AI tables (schema reservation)
- [ ] All FKs and constraints defined

### Design Artifacts
- [ ] ER diagram created
- [ ] Table inventory complete
- [ ] Seed script (design validation)
- [ ] All tables mapped to modules

### Verification
- [ ] BOM tracking fields verified
- [ ] IsLocked fields verified (scope declared)
- [ ] CostHead system verified
- [ ] Validation Guardrails constraints defined
- [ ] AI scope declared
- [ ] Module ownership verified
- [ ] Naming conventions applied

### Deliverable
- [ ] `NSW_SCHEMA_CANON_v1.0.md` complete
- [ ] ER diagram complete
- [ ] Table inventory complete
- [ ] Seed script complete
- [ ] All Step 2 requirements covered (trace matrix)
- [ ] Schema approved
- [ ] Schema FROZEN

---

## Freeze Gate Verification

### Schema Verification
- [ ] BOM tracking fields verified (evidence documented)
- [ ] IsLocked scope verified (evidence documented)
- [ ] CostHead system verified (evidence documented)
- [ ] All constraints verified

### Rules Verification
- [ ] Validation Guardrails G1-G7 verified (evidence documented)
- [ ] CostHead rules verified (evidence documented)
- [ ] Locking rules verified (evidence documented)
- [ ] BOM rules verified (evidence documented)

### Ownership & Naming Verification
- [ ] Module ownership verified (evidence documented)
- [ ] Naming conventions verified (evidence documented)

### Compliance Matrix
- [ ] Freeze Gate Checklist complete
- [ ] All items verified
- [ ] Evidence documented
- [ ] Compliance matrix signed off

### Approval
- [ ] Governance approval obtained
- [ ] Freeze gate passed
- [ ] Phase 5 complete

---

## Post-Phase 5 (Not in Phase 5 Scope)

- [ ] Use Implementation Reference documents
- [ ] Begin Post-Phase 5 implementation roadmap
- [ ] Phase 5 deliverables handed over to implementation team

---

## Change Log
- v1.0: Created execution checklist

