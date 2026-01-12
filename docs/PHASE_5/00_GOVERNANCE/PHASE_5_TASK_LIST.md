# Phase-5 Task List & Execution Plan

**Date:** 2025-01-27  
**Status:** Ready for Execution  
**Based On:** `PHASE_5_READINESS_REVIEW_CONSOLIDATED.md`

---

## 🎯 Overview

This task list is derived from the Phase-5 Readiness Review and organizes work into actionable items for Phase-5 execution.

**Phase-5 Definition:** Canonical Estimation Platform Build (New Truth Layer)  
**Primary Objective:** Change/variation estimation for live systems  
**Scope:** Step 1 (Data Dictionary) + Step 2 (Schema Design) — Analysis & Design Only

---

## 📋 Task Categories

### Category A: Freeze Gate Verification (MANDATORY BEFORE FREEZE)

**Status:** ⚠️ BLOCKING — Cannot freeze SPEC-5 v1.0 until complete

#### A1. Validation Guardrails G1-G8 Documentation
- [ ] **A1.1:** Review existing guardrail implementations
- [ ] **A1.2:** Document G1: Master BOM rejects ProductId (explicit business rule)
- [ ] **A1.3:** Document G2: Production BOM requires ProductId (explicit business rule)
- [ ] **A1.4:** Document G3: IsPriceMissing normalizes Amount (explicit business rule)
- [ ] **A1.5:** Document G4: RateSource consistency (explicit business rule)
- [x] **A1.6:** Document G5: UNRESOLVED normalizes values (explicit business rule)
- [x] **A1.7:** Document G6: FIXED_NO_DISCOUNT forces Discount=0 (explicit business rule)
- [x] **A1.8:** Document G7: All discounts are percentage-based (explicit business rule)
- [x] **A1.9:** Document G8: L1-SKU reuse is allowed and expected (explicit business rule)
- [x] **A1.10:** Add "Canonical Validation Guardrails" section to Data Dictionary
- [x] **A1.11:** Specify enforcement layer for each guardrail (business rule / DB constraint / service-level check)

**Deliverable:** Guardrails section in Data Dictionary with all 8 rules explicitly documented

---

#### A2. Module Ownership Matrix
- [ ] **A2.1:** List all tables in SPEC-5 schema DDL
- [ ] **A2.2:** Map Auth module tables (tenants, users, roles, user_roles, audit_log)
- [ ] **A2.3:** Map CIM module tables (categories, subcategories, types, attributes, products, etc.)
- [ ] **A2.4:** Map MBOM module tables (master_boms, master_bom_items)
- [ ] **A2.5:** Map QUO module tables (quotations, quote_panels, quote_boms, quote_bom_items, etc.)
- [ ] **A2.6:** Map PRICING module tables (price_lists, prices, import_batches, import_approval_queue)
- [ ] **A2.7:** Map AUDIT module tables (audit_log, bom_change_logs if exists)
- [ ] **A2.8:** Map AI module tables (ai_call_logs, etc.)
- [ ] **A2.9:** Create ownership matrix table/document
- [x] **A2.10:** Add to Data Dictionary Step 1 deliverable

**Deliverable:** Complete module ownership matrix mapping all tables to owner modules

---

#### A3. Naming Conventions Documentation
- [ ] **A3.1:** Document table naming convention (snake_case, plural, etc.)
- [ ] **A3.2:** Document column naming convention
- [ ] **A3.3:** Document FK naming pattern (table_id, etc.)
- [ ] **A3.4:** Document enum naming standard
- [ ] **A3.5:** Document timestamp naming (created_at, updated_at, etc.)
- [ ] **A3.6:** Document ID strategy (bigserial vs UUID)
- [ ] **A3.7:** Document tenant isolation convention (tenant_id everywhere)
- [ ] **A3.8:** Create naming conventions section
- [x] **A3.9:** Add to Data Dictionary Step 1 deliverable

**Deliverable:** Complete naming conventions documentation with all standards

---

#### A4. BOM Tracking Fields Verification
- [ ] **A4.1:** Verify `quote_boms.origin_master_bom_id` exists in SPEC-5 schema DDL
- [ ] **A4.2:** Verify `quote_boms.origin_master_bom_version` exists
- [ ] **A4.3:** Verify `quote_boms.instance_sequence_no` exists
- [ ] **A4.4:** Verify `quote_boms.is_modified` exists
- [ ] **A4.5:** Verify `quote_boms.modified_by` exists
- [ ] **A4.6:** Verify `quote_boms.modified_at` exists
- [ ] **A4.7:** Verify FK relationships are correct
- [ ] **A4.8:** Verify indexes are appropriate
- [ ] **A4.9:** Document verification results in compliance matrix
- [ ] **A4.10:** Update SPEC-5 schema DDL if fields are missing

**Deliverable:** Verification that all BOM tracking fields exist in schema DDL

---

#### A5. IsLocked Scope Declaration
- [ ] **A5.1:** Review current IsLocked field coverage in SPEC-5 schema
- [ ] **A5.2:** Decision: IsLocked at line-item only OR all quotation levels?
- [ ] **A5.3:** If all levels: Verify/add `quote_panels.is_locked`
- [ ] **A5.4:** If all levels: Verify/add `quote_boms.is_locked`
- [ ] **A5.5:** If all levels: Verify/add `quotations.is_locked`
- [ ] **A5.6:** Document decision in Data Dictionary
- [ ] **A5.7:** Document locking semantics (when/how IsLocked is set/unset)
- [ ] **A5.8:** Document relationship to DeletionPolicyService business rules
- [ ] **A5.9:** Update compliance matrix with decision
- [ ] **A5.10:** Update SPEC-5 schema DDL if needed

**Deliverable:** Explicit IsLocked scope declaration (line-item only or all levels)

---

#### A6. CostHead Resolution Order Documentation
- [ ] **A6.1:** Verify `cost_heads` table exists in SPEC-5 schema DDL
- [ ] **A6.2:** Verify `quote_bom_items.cost_head_id` FK exists
- [ ] **A6.3:** Decision: Add `products.cost_head_id` for default CostHead?
- [ ] **A6.4:** If yes: Add `products.cost_head_id` to schema DDL
- [ ] **A6.5:** Document CostHead resolution order in Data Dictionary:
  - Priority 1: BOM Item override (quote_bom_items.cost_head_id)
  - Priority 2: Product default (products.cost_head_id if exists)
  - Priority 3: System default (if any)
- [ ] **A6.6:** Document precedence rules
- [ ] **A6.7:** Add to Data Dictionary Step 1 deliverable

**Deliverable:** CostHead resolution order explicitly documented with precedence rules

---

#### A7. AI Scope Declaration
- [ ] **A7.1:** Verify `ai_call_logs` table exists in SPEC-5 schema DDL
- [ ] **A7.2:** List all AI-related tables
- [ ] **A7.3:** Document AI scope declaration:
  - Phase-5: Schema reservation only (tables exist, no logic)
  - Post-Phase-5: Population + logic implementation
- [ ] **A7.4:** Add to Data Dictionary Step 1 deliverable

**Deliverable:** AI scope explicitly declared (schema reservation vs implementation)

---

#### A8. Design Decision: Multi-SKU Linkage
- [ ] **A8.1:** Lock decision: Use `parent_line_id` + `metadata_json` (both)
- [ ] **A8.2:** Verify/add `quote_bom_items.parent_line_id` to schema DDL
- [ ] **A8.3:** Verify/add `quote_bom_items.metadata_json` to schema DDL
- [ ] **A8.4:** Document decision rationale (grouping + flexibility)
- [ ] **A8.5:** Document usage patterns in Data Dictionary

**Deliverable:** Multi-SKU linkage strategy locked and documented

---

#### A9. Design Decision: Customer Normalization
- [ ] **A9.1:** Lock decision: `customer_name` (text, snapshot) + `customer_id` (optional FK, nullable)
- [ ] **A9.2:** Verify `quotations.customer_name` exists in schema DDL
- [ ] **A9.3:** Verify/add `quotations.customer_id` (nullable FK) to schema DDL
- [ ] **A9.4:** Verify `customers` table exists
- [ ] **A9.5:** Document decision rationale (forward compatibility)
- [ ] **A9.6:** Document usage in Data Dictionary

**Deliverable:** Customer normalization approach locked and documented

---

#### A10. Design Decision: Resolution Level Constraints
- [ ] **A10.1:** Lock decision: L0/L1/L2 allowed at all levels with explicit rules
- [ ] **A10.2:** Verify `master_bom_items.resolution_level` exists
- [ ] **A10.3:** Verify/add `quote_bom_items.resolution_level` to schema DDL
- [ ] **A10.4:** Document MBOM rules: L0/L1/L2 if product_id rules respected
- [ ] **A10.5:** Document QUO rules: L0/L1/L2 if pricing + locking rules respected
- [ ] **A10.6:** Add constraints documentation to Data Dictionary

**Deliverable:** Resolution level constraints locked and documented with explicit rules

---

### Category B: Phase-5 Step 1 — Data Dictionary (Can Begin Immediately)

**Status:** ✅ READY TO START — Can proceed in parallel with freeze gate verification

#### B1. Entity Definitions
- [ ] **B1.1:** Define Category entity (business semantics, not legacy structure)
- [ ] **B1.2:** Define SubCategory entity
- [ ] **B1.3:** Define Type/Item entity
- [ ] **B1.4:** Define Attribute entity
- [ ] **B1.5:** Define Product entity (Legacy - will be replaced by L2 SKUs)
- [ ] **B1.6:** Define L1 Intent Line entity (engineering interpretation layer)
- [ ] **B1.7:** Define L1 Attribute entity (KVU attributes for L1 lines)
- [ ] **B1.8:** Define L1 Line Group entity (groups related L1 lines)
- [ ] **B1.9:** Define L2 SKU (Catalog SKU) entity (SKU-pure, commercial truth only)
- [ ] **B1.10:** Define L2 Price (SKU Price) entity (append-only price history)
- [ ] **B1.11:** Define L1 to L2 Mapping entity (many-to-one relationship)
- [ ] **B1.12:** Define Master BOM entity
- [ ] **B1.13:** Define Master BOM Item entity (L0/L1 only, no ProductId)
- [ ] **B1.14:** Define Quotation entity
- [ ] **B1.15:** Define Panel entity
- [ ] **B1.16:** Define BOM Group/Feeder entity
- [ ] **B1.17:** Define Quotation BOM Item entity
- [ ] **B1.18:** Define all other entities (Customer, Price, etc.)

**Deliverable:** Complete entity definitions in Data Dictionary (including L1/L2 entities)

---

#### B2. Relationship Semantics
- [ ] **B2.1:** Define Category → SubCategory → Type → Attribute hierarchy
- [ ] **B2.2:** Define Generic → Specific product relationship
- [ ] **B2.3:** Define Master BOM → Master BOM Items relationship
- [ ] **B2.4:** Define Quotation → Panel → BOM Group → Items hierarchy
- [ ] **B2.5:** Define Master BOM → Quotation BOM (copy-never-link) relationship
- [ ] **B2.6:** Define BOM hierarchy (parent-child BOM nesting)
- [ ] **B2.7:** Define Tenant → Customer → Quotation hierarchy
- [ ] **B2.8:** Document all allowed relationships

**Deliverable:** Complete relationship definitions in Data Dictionary

---

#### B3. Business Rules Documentation
- [ ] **B3.1:** Document copy-never-link rule
- [ ] **B3.2:** Document full editability after copy rule
- [ ] **B3.3:** Document history retention rules
- [ ] **B3.4:** Document multi-SKU explosion rules
- [ ] **B3.5:** Document L1/L2 differentiation rules (L2 = SKU-pure, L1 = engineering meaning)
- [ ] **B3.6:** Document L1 → L2 explosion logic (many-to-one mapping, SKU reuse)
- [ ] **B3.7:** Document L1 validation rules (SKU reuse allowed, validate attributes not SKU uniqueness)
- [ ] **B3.8:** Document master data governance rules (no auto-create, approval queue)
- [ ] **B3.9:** Document resolution level rules (L0/L1/L2 at all levels)
- [ ] **B3.10:** Document BOM hierarchy rules (any BOM can be parent/child)
- [ ] **B3.11:** Document tenant isolation rules
- [ ] **B3.12:** Document pricing rules (effective dating, RateSource semantics, L2 price model)
- [ ] **B3.13:** Include Validation Guardrails G1-G8 (from Category A1)

**Deliverable:** Complete business rules section in Data Dictionary (including L1/L2 rules)

---

#### B4. Field-Level Semantics
- [ ] **B4.1:** Document field-level meaning (business semantics) for all entities
- [ ] **B4.2:** Document required vs optional fields
- [ ] **B4.3:** Document default values and their meaning
- [ ] **B4.4:** Document enum values and their business meaning
- [ ] **B4.5:** Document timestamp fields and their usage

**Deliverable:** Complete field-level semantics in Data Dictionary

---

#### B5. Create Data Dictionary Document
- [ ] **B5.1:** Compile all entity definitions
- [ ] **B5.2:** Compile all relationships
- [ ] **B5.3:** Compile all business rules
- [ ] **B5.4:** Compile field-level semantics
- [ ] **B5.5:** Include module ownership matrix (from Category A2)
- [ ] **B5.6:** Include naming conventions (from Category A3)
- [ ] **B5.7:** Include all locked design decisions
- [ ] **B5.8:** Review and refine
- [ ] **B5.9:** Get stakeholder approval
- [ ] **B5.10:** Freeze as `NSW_DATA_DICTIONARY_v1.0.md`

**Deliverable:** Frozen Data Dictionary v1.0 document

---

### Category C: Phase-5 Step 2 — Schema Design (Requires Step 1 Complete)

**Status:** ⏳ GATED — Cannot start until Step 1 is complete and approved

#### C1. Translate Data Dictionary to Schema
- [ ] **C1.1:** Create table list from entity definitions
- [ ] **C1.2:** Map each entity to table structure (including L1/L2 entities)
- [ ] **C1.3:** Define L1/L2 tables: `l1_line_groups`, `l1_intent_lines`, `l1_attributes`, `catalog_skus`, `l1_l2_mappings`, `sku_prices`
- [ ] **C1.4:** Define column data types
- [ ] **C1.5:** Define column constraints (NOT NULL, DEFAULT, etc.)
- [ ] **C1.6:** Ensure many-to-one L1→L2 mapping (no unique constraint on `catalog_sku_id` in `l1_l2_mappings`)
- [ ] **C1.7:** Review against SPEC-5 schema DDL

**Deliverable:** Complete table structure design (including L1/L2 tables)

---

#### C2. Define Relationships & Constraints
- [ ] **C2.1:** Define primary keys for all tables
- [ ] **C2.2:** Define foreign key relationships
- [ ] **C2.3:** Define unique constraints
- [ ] **C2.4:** Define check constraints (e.g., Generic vs Specific product_type rules)
- [ ] **C2.5:** Define composite unique constraints (e.g., tenant_id + name)
- [ ] **C2.6:** Verify all relationships from Data Dictionary are represented

**Deliverable:** Complete relationship and constraint definitions

---

#### C3. Create ER Diagram
- [ ] **C3.1:** Create visual ER diagram showing all tables
- [ ] **C3.2:** Show relationships and cardinality
- [ ] **C3.3:** Export in multiple formats (PNG, PDF, draw.io)
- [ ] **C3.4:** Include legend and conventions

**Deliverable:** ER Diagram in multiple formats

---

#### C4. Generate Table Inventory
- [ ] **C4.1:** Create table inventory (Excel/CSV format)
- [ ] **C4.2:** List all tables with columns, data types, constraints
- [ ] **C4.3:** Include module ownership mapping
- [ ] **C4.4:** Include relationship summary

**Deliverable:** Table inventory in Excel/CSV format

---

#### C5. Create Seed Script (Design Validation Artifact)
- [ ] **C5.1:** Review SPEC-5 seed script
- [ ] **C5.2:** Create seed script SQL that demonstrates all relationships
- [ ] **C5.3:** Include tenant + users + roles setup
- [ ] **C5.4:** Include CIM masters (Category → SubCategory → Type → Attributes)
- [ ] **C5.5:** Include Products (Generic L1 + Specific L2)
- [ ] **C5.6:** Include Price lists and prices
- [ ] **C5.7:** Include Master BOM template (L0/L1 items)
- [ ] **C5.8:** Include Sample quotation workspace (L2 resolved items)
- [ ] **C5.9:** Validate seed script against schema design
- [ ] **C5.10:** Document as design validation artifact (not for execution in Phase 5)

**Deliverable:** Seed script SQL as design validation artifact

---

#### C6. Create Schema Canon Document
- [ ] **C6.1:** Compile complete DDL (ready-to-run SQL)
- [ ] **C6.2:** Include column definitions with business meaning
- [ ] **C6.3:** Include relationship documentation
- [ ] **C6.4:** Include constraints documentation
- [ ] **C6.5:** Include seed script (as appendix)
- [ ] **C6.6:** Include ER diagram
- [ ] **C6.7:** Include table inventory
- [ ] **C6.8:** Review and refine
- [ ] **C6.9:** Get stakeholder approval
- [ ] **C6.10:** Freeze as `NSW_SCHEMA_CANON_v1.0.md`

**Deliverable:** Frozen Schema Canon v1.0 document

---

### Category D: Freeze Gate Completion & SPEC-5 v1.0 Freeze

**Status:** ⏳ BLOCKED — Requires all Category A items complete

#### D1. Complete Compliance Matrix
- [ ] **D1.1:** Complete all items in `SPEC_5_FREEZE_GATE_CHECKLIST.md`
- [ ] **D1.2:** Mark all items as ✅ VERIFIED or document exceptions
- [ ] **D1.3:** Get compliance matrix approval

**Deliverable:** Completed compliance matrix with all items verified

---

#### D2. Patch SPEC-5 with Missing Sections
- [ ] **D2.1:** Add Validation Guardrails G1-G7 section
- [ ] **D2.2:** Add Module Ownership Matrix
- [ ] **D2.3:** Add Naming Conventions section
- [ ] **D2.4:** Add IsLocked scope declaration
- [ ] **D2.5:** Add CostHead resolution order
- [ ] **D2.6:** Add AI scope declaration
- [ ] **D2.7:** Lock all design decisions

**Deliverable:** SPEC-5 v1.0 patched with all missing governance sections

---

#### D3. Final Freeze Approval
- [ ] **D3.1:** Review complete SPEC-5 v1.0
- [ ] **D3.2:** Verify all freeze gate criteria met
- [ ] **D3.3:** Get architecture approval
- [ ] **D3.4:** Get execution team approval
- [ ] **D3.5:** Get stakeholder approval
- [ ] **D3.6:** Freeze SPEC-5 v1.0 as authoritative specification

**Deliverable:** SPEC-5 v1.0 frozen and approved

---

## 📊 Task Status Summary

| Category | Status | Items | Completed | Remaining |
|----------|--------|-------|-----------|-----------|
| **Category A: Freeze Gate Verification** | ⚠️ BLOCKING | 10 groups | 0 | 100+ tasks |
| **Category B: Step 1 - Data Dictionary** | ✅ READY | 5 groups | 0 | 50+ tasks |
| **Category C: Step 2 - Schema Design** | ⏳ GATED | 6 groups | 0 | 50+ tasks |
| **Category D: Freeze & Approval** | ⏳ BLOCKED | 3 groups | 0 | 15+ tasks |

---

## 🎯 Execution Priority

1. **Immediate:** Complete Category A (Freeze Gate Verification) — MANDATORY
2. **Parallel:** Begin Category B (Data Dictionary Step 1) — CAN START NOW
3. **After Step 1:** Complete Category C (Schema Design Step 2) — GATED
4. **After Freeze Gate:** Complete Category D (Freeze & Approval) — BLOCKED

---

**Last Updated:** 2025-01-27  
**Status:** Ready for Execution  
**Next Action:** Begin Category A freeze gate verification + Category B Step 1 in parallel

