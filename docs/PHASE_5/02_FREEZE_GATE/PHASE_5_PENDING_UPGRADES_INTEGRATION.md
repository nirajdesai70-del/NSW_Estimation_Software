# Phase 5 - Pending Upgrades Integration Guide

**Version:** 1.0  
**Date:** December 18, 2025  
**Status:** 📋 Integration Guide for Phase 5 Execution  
**Purpose:** Map all pending upgrades to Phase 5 steps to avoid rework

---

## 🎯 Purpose

This document maps each pending upgrade to the **specific Phase 5 step** where it must be considered during execution. When executing Phase 5, reference this guide to ensure all future requirements are captured in the Data Dictionary and Schema Design.

**Critical Rule:** Consider these during Phase 5 analysis/design work, NOT as implementation tasks.

**How to Use:**
1. **During Step 1 (Data Dictionary):** Reference Section 1 to define entities, relationships, and business rules
2. **During Step 2 (Schema Design):** Reference Section 2 to include all required fields and tables
3. **Check off items** as you consider them during Phase 5 execution

---

## 📊 Quick Reference - What Goes Where

| Pending Upgrade | Step 1 (Data Dictionary) | Step 2 (Schema Design) | Notes |
|----------------|-------------------------|------------------------|-------|
| **BOM Instance Identity** | ✅ Define entity semantics, relationships | ✅ Add fields to `quotation_sale_boms` | origin_master_bom_id, instance_sequence_no, etc. |
| **BOM Modification Tracking** | ✅ Define modification semantics | ✅ Add is_modified, modified_by, modified_at fields | Track when Proposal BOM is modified |
| **Validation Guardrails** | ✅ Document as business rules | ✅ Define constraint types | 7 guardrail rules |
| **CostHead System** | ✅ Define CostHead entity | ✅ Create `cost_heads` table + FK fields | For costing engine |
| **AI Implementation** | ✅ Define AI entities | ✅ Create AI tables (ai_call_logs, etc.) | 6+ AI-related tables |
| **IsLocked Field** | ✅ Define locking semantics | ✅ Add is_locked to quotation tables | For deletion policy |
| **Audit Trail** | ✅ Define audit requirements | ✅ Create bom_change_logs table | Optional but recommended |
| **UI Components** | ❌ N/A | ❌ N/A | UI-only, no schema impact |
| **Code Implementation** | ❌ N/A | ❌ N/A | Code-only, no schema impact |
| **Framework Upgrades** | ❌ N/A | ❌ N/A | Code-only, no schema impact |

---

## 📊 Integration Summary

| Upgrade Category | Step 1 (Data Dictionary) | Step 2 (Schema Design) |
|------------------|--------------------------|------------------------|
| **BOM Enhancements** | Business rules, entity semantics | Table fields, relationships |
| **Validation Guardrails** | Business rules, constraints | Constraint definitions |
| **Costing Engine** | CostHead entity definition | CostHead tables, cost tracking fields |
| **AI Implementation** | AI entity definitions, rules | AI logging tables, rule tables |
| **UI Components** | N/A (UI only) | N/A (UI only) |
| **Framework Upgrades** | N/A (code only) | N/A (code only) |

---

## 🔴 STEP 1: FREEZE NSW CANONICAL DATA DICTIONARY

### Integration Points for Step 1

When defining entities, relationships, and business rules in Step 1, **consider the following pending upgrades:**

---

### 1.1 BOM Instance Identity & Tracking

**When:** Defining `QuotationSaleBom` entity and relationships

**Consider:**

#### Entity: QuotationSaleBom
- [ ] **OriginMasterBomId** (reference field)
  - **Semantic:** Links Proposal BOM to its source Master BOM
  - **Business Rule:** Nullable (only set when Master BOM is applied)
  - **Relationship:** References `master_boms.id` (or equivalent)
  
- [ ] **OriginMasterBomVersion** (string field)
  - **Semantic:** Version of Master BOM at time of application
  - **Business Rule:** Captured when Master BOM is applied, immutable
  
- [ ] **InstanceSequenceNo** (integer field)
  - **Semantic:** Sequence number for multiple instances of same Master BOM
  - **Business Rule:** Auto-increments per panel (BOM-01, BOM-02, etc.)
  - **Naming Convention:** Used in `generateBomName()` function

#### Entity: QuotationSaleBom (Modification Tracking)
- [ ] **IsModified** (boolean field)
  - **Semantic:** Indicates if Proposal BOM has been modified from Master BOM
  - **Business Rule:** False initially, set to true on any edit
  
- [ ] **ModifiedBy** (user reference)
  - **Semantic:** User who first modified the BOM
  - **Business Rule:** Nullable (only set when IsModified = true)
  - **Relationship:** References `users.id`
  
- [ ] **ModifiedAt** (timestamp field)
  - **Semantic:** Timestamp of first modification
  - **Business Rule:** Nullable (only set when IsModified = true)

**Document in Data Dictionary:**
- Master BOM vs Proposal BOM relationship semantics
- "Always Copy" rule (Proposal BOMs are always copies, never links)
- Modification tracking business rules
- Instance naming conventions

---

### 1.2 Validation Guardrails (Business Rules)

**When:** Defining business rules and constraints

**Consider:**

#### Guardrail Rules (Document as Business Rules):
- [ ] **G1: Master BOM rejects ProductId**
  - **Rule:** Master BOM items cannot have ProductId set
  - **Constraint Type:** Business rule (enforced in code)
  
- [ ] **G2: Production BOM requires ProductId**
  - **Rule:** Proposal BOM items must have ProductId when used in production
  - **Constraint Type:** Business rule (enforced in code)
  
- [ ] **G3: IsPriceMissing normalizes Amount**
  - **Rule:** When IsPriceMissing = true, Amount should be normalized to 0 or null
  - **Constraint Type:** Business rule (data normalization)
  
- [ ] **G4: RateSource consistency**
  - **Rule:** RateSource must be consistent with discount application
  - **Constraint Type:** Business rule (data integrity)
  
- [ ] **G5: UNRESOLVED normalizes values**
  - **Rule:** When RateSource = UNRESOLVED, certain fields must be normalized
  - **Constraint Type:** Business rule (data normalization)
  
- [ ] **G6: FIXED_NO_DISCOUNT forces Discount=0**
  - **Rule:** When RateSource = FIXED_NO_DISCOUNT, Discount must be 0
  - **Constraint Type:** Business rule (data integrity)
  
- [ ] **G7: All discounts are percentage-based**
  - **Rule:** Discount values are always percentages (0-100)
  - **Constraint Type:** Business rule (data format)

**Document in Data Dictionary:**
- All 7 guardrail rules as business constraints
- Data normalization rules
- RateSource enum values and their implications

---

### 1.3 CostHead Entity Definition

**When:** Defining cost-related entities

**Consider:**

#### Entity: CostHead
- [ ] **CostHead** (new entity)
  - **Semantic:** Categorizes costs into buckets (MATERIAL, LABOUR, OTHER)
  - **Examples:** OEM_MATERIAL, NEPL_BUS, NEPL_FAB, LABOUR, OVERHEAD, etc.
  - **Business Rule:** Required for costing engine calculations
  - **Ownership:** Costing module

**Document in Data Dictionary:**
- CostHead entity definition
- CostHead enum values (OEM_MATERIAL, NEPL_BUS, NEPL_FAB, LABOUR, OVERHEAD, etc.)
- CostHead priority logic (for mapping items to cost heads)
- Relationship: Products can have default CostHead
- Relationship: BOM Items can override CostHead

---

### 1.4 AI Implementation Entities

**When:** Defining AI-related entities and rules

**Consider:**

#### Entity: AiCallLog
- [ ] **AiCallLog** (new entity for audit)
  - **Semantic:** Logs all AI API calls for audit and learning
  - **Business Rule:** Required for AI feature audit trail
  - **Ownership:** AI module

#### Entity: SelectionPattern (for AI)
- [ ] **SelectionPattern** (new entity)
  - **Semantic:** Patterns learned from historical component selections
  - **Business Rule:** Used by AI for component suggestions
  - **Ownership:** AI module

#### Entity: PriceDistribution (for AI)
- [ ] **PriceDistribution** (new entity)
  - **Semantic:** Statistical distribution of prices for price sanity checks
  - **Business Rule:** Used by AI for price validation
  - **Ownership:** AI module

#### Entity: CoOccurrence (for AI)
- [ ] **CoOccurrence** (new entity)
  - **Semantic:** Component co-occurrence patterns for missing component detection
  - **Business Rule:** Used by AI for missing component suggestions
  - **Ownership:** AI module

#### Entity: DiscountBehavior (for AI)
- [ ] **DiscountBehavior** (new entity)
  - **Semantic:** Historical discount patterns for discount validation
  - **Business Rule:** Used by AI for discount pattern checking
  - **Ownership:** AI module

#### Entity: SubstitutionMatrix (for AI)
- [ ] **SubstitutionMatrix** (new entity)
  - **Semantic:** Component substitution rules for option building
  - **Business Rule:** Used by AI for generating option variants
  - **Ownership:** AI module

**Document in Data Dictionary:**
- All AI-related entities
- AI rulebook references (IEC 61439 rules, etc.)
- AI audit requirements

---

### 1.5 Deletion Policy - IsLocked Field

**When:** Defining deletion and locking semantics

**Consider:**

#### Entity: QuotationSale (Panel)
- [ ] **IsLocked** (boolean field)
  - **Semantic:** Prevents deletion when locked
  - **Business Rule:** Used by DeletionPolicyService
  - **Priority:** LOW (not yet needed, but define semantics)

#### Entity: QuotationSaleBom (BOM/Feeder)
- [ ] **IsLocked** (boolean field)
  - **Semantic:** Prevents deletion when locked
  - **Business Rule:** Used by DeletionPolicyService
  - **Priority:** LOW (not yet needed, but define semantics)

#### Entity: QuotationSaleBomItem (Component)
- [ ] **IsLocked** (boolean field)
  - **Semantic:** Prevents deletion when locked
  - **Business Rule:** Used by DeletionPolicyService
  - **Priority:** LOW (not yet needed, but define semantics)

**Document in Data Dictionary:**
- Locking semantics for deletion protection
- When and how IsLocked is set/unset
- Relationship to DeletionPolicyService business rules

---

### 1.6 Audit Trail Requirements

**When:** Defining audit and change tracking

**Consider:**

#### Entity: BomChangeLog (optional)
- [ ] **BomChangeLog** (new entity, optional)
  - **Semantic:** Audit log for BOM changes
  - **Business Rule:** Optional but recommended for audit trail
  - **Fields:** Who, what, when, before/after values
  - **Ownership:** BOM module

**Document in Data Dictionary:**
- Audit trail requirements
- Change logging semantics
- Who/what/when/before/after pattern

---

## 🔵 STEP 2: DEFINE NSW CANONICAL SCHEMA (DESIGN ONLY)

### Integration Points for Step 2

When designing tables, columns, and relationships in Step 2, **include the following fields and tables:**

---

### 2.1 BOM Instance Identity & Tracking - Schema Design

**Table: `quotation_sale_boms`**

**Add Columns:**
- [ ] `origin_master_bom_id` (bigint unsigned, nullable)
  - **FK:** References `master_boms.id` (or equivalent table)
  - **Index:** Yes (for lookups)
  - **Default:** NULL
  - **Comment:** "Links to source Master BOM when Master BOM is applied"
  
- [ ] `origin_master_bom_version` (varchar(50), nullable)
  - **Index:** No
  - **Default:** NULL
  - **Comment:** "Version of Master BOM at time of application"
  
- [ ] `instance_sequence_no` (integer unsigned, nullable)
  - **Index:** Yes (composite with panel_id for uniqueness)
  - **Default:** NULL
  - **Comment:** "Sequence number for multiple instances (BOM-01, BOM-02, etc.)"
  
- [ ] `is_modified` (boolean, default false)
  - **Index:** Yes (for filtering modified BOMs)
  - **Default:** false
  - **Comment:** "Indicates if Proposal BOM has been modified from Master BOM"
  
- [ ] `modified_by` (bigint unsigned, nullable)
  - **FK:** References `users.id`
  - **Index:** Yes
  - **Default:** NULL
  - **Comment:** "User who first modified the BOM"
  
- [ ] `modified_at` (timestamp, nullable)
  - **Index:** Yes
  - **Default:** NULL
  - **Comment:** "Timestamp of first modification"

**Schema Considerations:**
- Composite unique constraint: `(panel_id, origin_master_bom_id, instance_sequence_no)` if needed
- Index on `origin_master_bom_id` for reverse lookups
- Index on `is_modified` for filtering

---

### 2.2 CostHead System - Schema Design

**Table: `cost_heads` (NEW TABLE)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `code` (varchar(50), unique, not null)
  - **Examples:** OEM_MATERIAL, NEPL_BUS, NEPL_FAB, LABOUR, OVERHEAD
- [ ] `name` (varchar(255), not null)
- [ ] `category` (enum: MATERIAL, LABOUR, OTHER)
- [ ] `priority` (integer, default 0)
  - **Comment:** "Used for mapping priority when multiple cost heads apply"
- [ ] `description` (text, nullable)
- [ ] `is_active` (boolean, default true)
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Table: `products`**

**Add Column:**
- [ ] `cost_head_id` (bigint unsigned, nullable)
  - **FK:** References `cost_heads.id`
  - **Index:** Yes
  - **Default:** NULL
  - **Comment:** "Default CostHead for this product"

**Table: `quotation_sale_bom_items`**

**Add Column:**
- [ ] `cost_head_id` (bigint unsigned, nullable)
  - **FK:** References `cost_heads.id`
  - **Index:** Yes
  - **Default:** NULL
  - **Comment:** "Override CostHead for this item (overrides product default)"

**Schema Considerations:**
- Index on `cost_heads.code` for lookups
- Index on `cost_heads.category` for filtering
- Foreign key constraints with appropriate cascade rules

---

### 2.3 AI Implementation - Schema Design

**Table: `ai_call_logs` (NEW TABLE)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `user_id` (bigint unsigned, nullable)
  - **FK:** References `users.id`
- [ ] `quotation_id` (bigint unsigned, nullable)
  - **FK:** References `quotations.id`
- [ ] `panel_id` (bigint unsigned, nullable)
  - **FK:** References `quotation_sales.id`
- [ ] `feeder_id` (bigint unsigned, nullable)
  - **FK:** References `quotation_sale_boms.id`
- [ ] `bom_item_id` (bigint unsigned, nullable)
  - **FK:** References `quotation_sale_bom_items.id`
- [ ] `endpoint` (varchar(100), not null)
  - **Examples:** suggest-component, price-sanity-check, missing-components
- [ ] `request_json` (longtext, not null)
- [ ] `response_json` (longtext, not null)
- [ ] `final_action` (enum: accepted, rejected, modified, nullable)
- [ ] `status` (enum: ok, warning, error, default 'ok')
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Indexes:**
- [ ] Index on `quotation_id`
- [ ] Index on `panel_id`
- [ ] Index on `endpoint`
- [ ] Index on `user_id`
- [ ] Index on `created_at` (for time-based queries)

**Table: `selection_patterns` (NEW TABLE - for AI)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `context_hash` (varchar(255), unique, not null)
  - **Comment:** "Hash of context (panel type, feeder type, etc.)"
- [ ] `component_id` (bigint unsigned, not null)
  - **FK:** References `products.id`
- [ ] `frequency` (integer, default 0)
- [ ] `confidence_score` (decimal(5,2), nullable)
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Table: `price_distributions` (NEW TABLE - for AI)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `product_id` (bigint unsigned, not null)
  - **FK:** References `products.id`
- [ ] `mean_price` (decimal(15,2))
- [ ] `median_price` (decimal(15,2))
- [ ] `std_deviation` (decimal(15,2))
- [ ] `min_price` (decimal(15,2))
- [ ] `max_price` (decimal(15,2))
- [ ] `sample_count` (integer)
- [ ] `last_calculated_at` (timestamp)
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Table: `co_occurrences` (NEW TABLE - for AI)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `component_a_id` (bigint unsigned, not null)
  - **FK:** References `products.id`
- [ ] `component_b_id` (bigint unsigned, not null)
  - **FK:** References `products.id`
- [ ] `co_occurrence_count` (integer, default 0)
- [ ] `confidence_score` (decimal(5,2), nullable)
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Table: `discount_behaviors` (NEW TABLE - for AI)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `make_id` (bigint unsigned, nullable)
  - **FK:** References `makes.id`
- [ ] `series_id` (bigint unsigned, nullable)
  - **FK:** References `series.id`
- [ ] `product_type_id` (bigint unsigned, nullable)
  - **FK:** References `product_types.id`
- [ ] `avg_discount_pct` (decimal(5,2))
- [ ] `min_discount_pct` (decimal(5,2))
- [ ] `max_discount_pct` (decimal(5,2))
- [ ] `sample_count` (integer)
- [ ] `last_calculated_at` (timestamp)
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Table: `substitution_matrices` (NEW TABLE - for AI)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `source_component_id` (bigint unsigned, not null)
  - **FK:** References `products.id`
- [ ] `target_component_id` (bigint unsigned, not null)
  - **FK:** References `products.id`
- [ ] `substitution_type` (enum: economy, premium, equivalent)
- [ ] `cost_delta` (decimal(15,2), nullable)
  - **Comment:** "Cost difference (target - source)"
- [ ] `is_approved` (boolean, default false)
- [ ] `created_at` (timestamp)
- [ ] `updated_at` (timestamp)

**Schema Considerations:**
- All AI tables should have appropriate indexes
- Consider partitioning for large tables (ai_call_logs)
- Foreign key constraints with appropriate cascade rules

---

### 2.4 Deletion Policy - IsLocked Field - Schema Design

**Table: `quotation_sales` (Panels)**

**Add Column:**
- [ ] `is_locked` (boolean, default false)
  - **Index:** Yes (for filtering locked items)
  - **Default:** false
  - **Comment:** "Prevents deletion when locked"

**Table: `quotation_sale_boms` (BOMs/Feeders)**

**Add Column:**
- [ ] `is_locked` (boolean, default false)
  - **Index:** Yes (for filtering locked items)
  - **Default:** false
  - **Comment:** "Prevents deletion when locked"

**Table: `quotation_sale_bom_items` (Components)**

**Add Column:**
- [ ] `is_locked` (boolean, default false)
  - **Index:** Yes (for filtering locked items)
  - **Default:** false
  - **Comment:** "Prevents deletion when locked"

---

### 2.5 Audit Trail - Schema Design

**Table: `bom_change_logs` (NEW TABLE - Optional)**

**Create Table:**
- [ ] `id` (bigint unsigned, primary key)
- [ ] `bom_id` (bigint unsigned, not null)
  - **FK:** References `quotation_sale_boms.id`
- [ ] `user_id` (bigint unsigned, not null)
  - **FK:** References `users.id`
- [ ] `action` (varchar(50), not null)
  - **Examples:** created, modified, item_added, item_updated, item_deleted
- [ ] `field_name` (varchar(100), nullable)
  - **Comment:** "Field that changed (if applicable)"
- [ ] `before_value` (text, nullable)
- [ ] `after_value` (text, nullable)
- [ ] `metadata` (json, nullable)
  - **Comment:** "Additional context about the change"
- [ ] `created_at` (timestamp)

**Indexes:**
- [ ] Index on `bom_id`
- [ ] Index on `user_id`
- [ ] Index on `created_at`
- [ ] Index on `action`

**Schema Considerations:**
- Consider partitioning by `created_at` for large tables
- JSON column for flexible metadata storage

---

## 📋 Execution Checklist

### During Step 1 (Data Dictionary):

- [ ] Review BOM Instance Identity requirements → Define entity semantics
- [ ] Review Validation Guardrails → Document as business rules
- [ ] Review CostHead requirements → Define CostHead entity
- [ ] Review AI requirements → Define AI entities
- [ ] Review IsLocked requirements → Define locking semantics
- [ ] Review Audit Trail requirements → Define audit entities
- [ ] Document all relationships and business rules
- [ ] Lock all entity definitions

### During Step 2 (Schema Design):

- [ ] Add BOM tracking fields to `quotation_sale_boms` table
- [ ] Create `cost_heads` table
- [ ] Add `cost_head_id` to `products` and `quotation_sale_bom_items`
- [ ] Create all AI-related tables (`ai_call_logs`, `selection_patterns`, etc.)
- [ ] Add `is_locked` to `quotation_sales`, `quotation_sale_boms`, `quotation_sale_bom_items`
- [ ] Create `bom_change_logs` table (optional)
- [ ] Define all indexes and foreign keys
- [ ] Document all constraints
- [ ] Create ER diagram including all new tables/fields
- [ ] Update table inventory

---

## 🚫 What NOT to Include in Phase 5

These are **implementation-only** and should NOT be in Phase 5:

- ❌ UI Components (Sprint-4 UI, UI Standardization) - These are UI-only, no schema impact
- ❌ Code Implementation (BomChangeOrchestrator, services) - These are code-only
- ❌ Framework Upgrades (Laravel/PHP upgrade) - These are code-only
- ❌ Documentation TODOs - These are documentation-only

**Note:** UI, code, and framework work will be done in post-Phase 5 implementation. Phase 5 only covers data dictionary and schema design.

---

## 🔗 Reference Documents

- `POST_PHASE_5_IMPLEMENTATION_ROADMAP.md` - Complete list of all pending upgrades
- `PHASE_5_SCOPE_FENCE.md` - Phase 5 scope definition
- `PHASE_5_EXECUTION_SUMMARY.md` - Phase 5 execution plan

---

**Status:** ✅ Ready for Phase 5 Execution  
**Last Updated:** December 18, 2025  
**Use During:** Phase 5 Step 1 and Step 2 execution

