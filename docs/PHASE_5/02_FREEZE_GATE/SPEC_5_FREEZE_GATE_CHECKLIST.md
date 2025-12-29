# SPEC-5 Freeze Gate Checklist - Pending Upgrades Compliance Matrix

**Date:** 2025-01-27  
**Status:** 📋 MANDATORY VERIFICATION BEFORE FREEZE  
**Purpose:** Verify SPEC-5 v1.0 compliance with Phase 5 requirements from `PHASE_5_PENDING_UPGRADES_INTEGRATION.md`

---

## 🎯 Freeze Gate Rule

**SPEC-5 v1.0 CANNOT be frozen until ALL items in this checklist are verified and documented.**

This checklist ensures no governance fields or business rules are missed, preventing rework during implementation.

---

## 📊 Compliance Matrix

| Required Component | SPEC-5 Status | Verification Location | Action Required | Status |
|-------------------|---------------|----------------------|-----------------|--------|
| **1. BOM Tracking Fields** | ✅ **VERIFIED** | Schema DDL: `quote_boms` table | All fields verified in schema | ✅ VERIFIED |
| 1.1 `origin_master_bom_id` | ✅ | `quote_boms` table | **VERIFIED:** BIGINT NULL, FK to `master_boms.id` (line 843, FK line 856) | ✅ VERIFIED |
| 1.2 `origin_master_bom_version` | ✅ | `quote_boms` table | **VERIFIED:** VARCHAR(50) NULL (line 844) | ✅ VERIFIED |
| 1.3 `instance_sequence_no` | ✅ | `quote_boms` table | **VERIFIED:** INTEGER NULL (line 845) | ✅ VERIFIED |
| 1.4 `is_modified` | ✅ | `quote_boms` table | **VERIFIED:** BOOLEAN NOT NULL DEFAULT false (line 846) | ✅ VERIFIED |
| 1.5 `modified_by` | ✅ | `quote_boms` table | **VERIFIED:** BIGINT NULL, FK to `users.id` (line 847, FK line 857) | ✅ VERIFIED |
| 1.6 `modified_at` | ✅ | `quote_boms` table | **VERIFIED:** TIMESTAMP NULL (line 848) | ✅ VERIFIED |
| **2. IsLocked Fields** | ✅ **VERIFIED** | Quotation tables | Scope explicitly declared per D-005 | ✅ VERIFIED |
| 2.1 `quote_bom_items.is_locked` | ✅ | `quote_bom_items` table | **VERIFIED:** BOOLEAN NOT NULL DEFAULT false (line 890, index line 926) - D-005 APPROVED | ✅ VERIFIED |
| 2.2 `quote_panels.is_locked` | ✅ | `quote_panels` table | **EXCLUDED (MVP):** Per D-005, locking only at line-item level in MVP | ✅ EXCLUDED |
| 2.3 `quote_boms.is_locked` | ✅ | `quote_boms` table | **EXCLUDED (MVP):** Per D-005, locking only at line-item level in MVP | ✅ EXCLUDED |
| 2.4 `quotations.is_locked` | ✅ | `quotations` table | **EXCLUDED (MVP):** Per D-005, locking only at line-item level in MVP | ✅ EXCLUDED |
| 2.5 Locking scope declaration | ✅ | Data Dictionary | **VERIFIED:** Documented in LOCKING_POLICY.md (line-item level only in MVP) - D-005 APPROVED | ✅ VERIFIED |
| **3. CostHead System** | ✅ **VERIFIED** | Schema DDL + Data Dictionary | All components verified | ✅ VERIFIED |
| 3.1 `cost_heads` table | ✅ | Schema DDL | **VERIFIED:** Table exists with id, code, name, category, priority (lines 964-983) | ✅ VERIFIED |
| 3.2 `quote_bom_items.cost_head_id` | ✅ | `quote_bom_items` table | **VERIFIED:** BIGINT NULL, FK to `cost_heads.id` (line 891, FK line 906) | ✅ VERIFIED |
| 3.3 `products.cost_head_id` (optional) | ✅ | `products` table | **VERIFIED:** BIGINT NULL, FK to `cost_heads.id` (D-006 APPROVED, line 367, FK line 378) | ✅ VERIFIED |
| 3.4 CostHead resolution order | ✅ | Data Dictionary | **VERIFIED:** Documented in COSTHEAD_RULES.md with explicit precedence order | ✅ VERIFIED |
| **4. Validation Guardrails G1-G7** | ✅ **COMPLETE** | Data Dictionary + Schema notes | **VERIFIED:** All 7 guardrails documented in VALIDATION_GUARDRAILS_G1_G7.md | ✅ VERIFIED |
| 4.1 G1: Master BOM rejects ProductId | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with enforcement layer | ✅ VERIFIED |
| 4.2 G2: Production BOM requires ProductId | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with enforcement layer | ✅ VERIFIED |
| 4.3 G3: IsPriceMissing normalizes Amount | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with normalization rules | ✅ VERIFIED |
| 4.4 G4: RateSource consistency | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with consistency rules | ✅ VERIFIED |
| 4.5 G5: UNRESOLVED normalizes values | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with normalization rules | ✅ VERIFIED |
| 4.6 G6: FIXED_NO_DISCOUNT forces Discount=0 | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with enforcement rules | ✅ VERIFIED |
| 4.7 G7: All discounts are percentage-based | ✅ | Data Dictionary rules | **VERIFIED:** Explicitly documented with range validation | ✅ VERIFIED |
| **5. AI Entities** | ✅ **COVERED** | Schema DDL | Verify tables exist | ✅ VERIFIED |
| 5.1 `ai_call_logs` table | ✅ | Schema DDL | Table exists with required fields | ✅ |
| 5.2 AI scope declaration | ✅ | Data Dictionary | **VERIFIED:** Documented in NSW_DATA_DICTIONARY_v1.0.md section "6. AI Scope Declaration" | ✅ VERIFIED |
| **6. Module Ownership Mapping** | ✅ **COMPLETE** | Data Dictionary | **VERIFIED:** Complete mapping in MODULE_OWNERSHIP_MATRIX.md | ✅ VERIFIED |
| 6.1 Auth module tables | ✅ | Module ownership matrix | **VERIFIED:** All AUTH tables mapped (tenants, users, roles, etc.) | ✅ VERIFIED |
| 6.2 CIM module tables | ✅ | Module ownership matrix | **VERIFIED:** All CIM tables mapped (categories, products, etc.) | ✅ VERIFIED |
| 6.3 MBOM module tables | ✅ | Module ownership matrix | **VERIFIED:** All MBOM tables mapped (master_boms, master_bom_items) | ✅ VERIFIED |
| 6.4 QUO module tables | ✅ | Module ownership matrix | **VERIFIED:** All QUO tables mapped (quotations, panels, boms, items) | ✅ VERIFIED |
| 6.5 PRICING module tables | ✅ | Module ownership matrix | **VERIFIED:** All PRICING tables mapped (price_lists, prices) | ✅ VERIFIED |
| 6.6 AUDIT module tables | ✅ | Module ownership matrix | **VERIFIED:** All AUDIT tables mapped (audit_logs, bom_change_logs, etc.) | ✅ VERIFIED |
| 6.7 AI module tables | ✅ | Module ownership matrix | **VERIFIED:** All AI tables mapped (ai_call_logs, etc.) | ✅ VERIFIED |
| **7. Naming Conventions** | ✅ **COMPLETE** | Data Dictionary | **VERIFIED:** Complete naming standards in NAMING_CONVENTIONS.md | ✅ VERIFIED |
| 7.1 Table naming | ✅ | Naming conventions | **VERIFIED:** Documented (snake_case, plural) | ✅ VERIFIED |
| 7.2 Column naming | ✅ | Naming conventions | **VERIFIED:** Documented (snake_case, singular) | ✅ VERIFIED |
| 7.3 FK naming | ✅ | Naming conventions | **VERIFIED:** Documented pattern ({table_singular}_id) | ✅ VERIFIED |
| 7.4 Enum naming | ✅ | Naming conventions | **VERIFIED:** Documented (UPPER_SNAKE_CASE) | ✅ VERIFIED |
| 7.5 Timestamp naming | ✅ | Naming conventions | **VERIFIED:** Documented ({action}_at pattern) | ✅ VERIFIED |
| 7.6 ID strategy | ✅ | Naming conventions | **VERIFIED:** Documented (bigserial for MVP, UUID reserved) | ✅ VERIFIED |
| 7.7 Tenant isolation convention | ✅ | Naming conventions | **VERIFIED:** Documented (tenant_id everywhere) | ✅ VERIFIED |
| **8. Design Decisions** | ✅ **LOCKED** | Schema Design | All 3 decisions locked | ✅ VERIFIED |
| 8.1 Multi-SKU linkage | ✅ | Schema DDL | **LOCKED:** D-007 APPROVED - parent_line_id + metadata_json (both) | ✅ VERIFIED |
| 8.2 Customer normalization | ✅ | Schema DDL | **LOCKED:** D-009 APPROVED - customer_name_snapshot (text) + customer_id (nullable FK) | ✅ VERIFIED |
| 8.3 Resolution level constraints | ✅ | Schema DDL + Data Dictionary | **VERIFIED IN SCHEMA:** master_bom_items.resolution_status (L0/L1), quote_bom_items.resolution_status (L0/L1/L2), CHECK constraint enforces L2 => product_id NOT NULL | ✅ VERIFIED |

---

## ✅ Verification Steps

### Step 1: Schema DDL Verification
- [ ] Open SPEC-5 schema DDL section
- [ ] For each item in compliance matrix, verify field/table exists
- [ ] Check data types, constraints, FKs are correct
- [ ] Mark status in compliance matrix

### Step 2: Data Dictionary Verification
- [ ] Open SPEC-5 Data Dictionary section (or create if missing)
- [ ] Verify business rules are documented
- [ ] Verify Validation Guardrails G1-G7 are explicitly listed
- [ ] Verify CostHead resolution order is documented
- [ ] Verify IsLocked scope is explicitly declared

### Step 3: Module Ownership & Naming
- [ ] Create Module Ownership Matrix (if missing)
- [ ] Create Naming Conventions section (if missing)
- [ ] Map all tables to owner modules
- [ ] Document all naming standards

### Step 4: Design Decision Lock
- [x] Lock Multi-SKU linkage strategy (parent_line_id + metadata_json) - **D-007 APPROVED**
- [x] Lock Customer normalization approach (customer_name_snapshot + optional customer_id) - **D-009 APPROVED**
- [x] Lock Resolution level constraints (L0/L1/L2 at all levels with rules) - **VERIFIED IN SCHEMA**

### Step 5: Documentation Patch
- [ ] Add missing sections to SPEC-5
- [ ] Update compliance matrix with final status
- [ ] Mark all items as ✅ VERIFIED or document exceptions

---

## 🚦 Freeze Gate Criteria

**SPEC-5 v1.0 can be frozen ONLY when:**

1. ✅ All BOM tracking fields verified in schema
2. ✅ IsLocked scope explicitly declared (added fields or explicit exclusion)
3. ✅ CostHead system verified + resolution order documented
4. ✅ Validation Guardrails G1-G8 explicitly documented in Data Dictionary
5. ✅ AI scope explicitly declared (schema reservation vs implementation)
6. ✅ Module ownership matrix complete (all tables mapped)
7. ✅ Naming conventions documented (all standards written)
8. ✅ Three design decisions locked (Multi-SKU: D-007 ✅, Customer: D-009 ✅, Resolution levels: ✅ VERIFIED)

---

## 📝 Action Items

### Immediate (Before Freeze)

1. [ ] **Verify schema DDL** against compliance matrix
2. [ ] **Document Validation Guardrails G1-G7** in Data Dictionary section
3. [ ] **Create Module Ownership Matrix** mapping all tables to modules
4. [ ] **Create Naming Conventions** section with all standards
5. [ ] **Declare IsLocked scope** (which tables have is_locked, or explicit exclusion)
6. [ ] **Document CostHead resolution order** (item → product → system default)
7. [ ] **Declare AI scope** (Phase-5 schema reservation, Post-Phase-5 implementation)
8. [x] **Lock Multi-SKU design decision** (D-007 APPROVED - parent_line_id + metadata_json)
8b. [x] **Lock Customer normalization design decision** (D-009 APPROVED - customer_name_snapshot + optional customer_id)
8c. [x] **Lock Resolution level constraints design decision** (VERIFIED IN SCHEMA - master_bom_items L0/L1 only, quote_bom_items L0/L1/L2 with CHECK constraints)
9. [ ] **Update compliance matrix** with final verification status
10. [ ] **Get stakeholder approval** for freeze gate criteria

### Post-Freeze (Phase 5 Execution)

- [ ] Use compliance matrix as reference during Phase 5 Step 1 (Data Dictionary)
- [ ] Use compliance matrix as reference during Phase 5 Step 2 (Schema Design)
- [ ] Verify all items are covered in frozen deliverables

---

## 📌 Notes

### IsLocked Scope Decision

**Decision D-005 (APPROVED):** IsLocked only at line-item level (MVP)

**Locking Scope Declaration:**
Per Decision D-005, locking is enforced only at `quote_bom_items` (line level) in MVP. Higher-level locking (quotation/panel/bom) is deferred and not part of Phase-5 freeze gate.

**Rationale:**
- Simpler implementation, sufficient for MVP deletion protection
- Can be extended later if needed
- Aligns with MVP scope to keep initial implementation focused

**Implementation:**
- ✅ `quote_bom_items.is_locked` - VERIFIED in schema (line 890)
- ❌ `quote_panels.is_locked` - EXCLUDED (MVP)
- ❌ `quote_boms.is_locked` - EXCLUDED (MVP)
- ❌ `quotations.is_locked` - EXCLUDED (MVP)

**Decision Register Reference:** D-005 in `docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md`

### CostHead Product Default

**Option A:** Add `products.cost_head_id` for default CostHead
- Pros: Product-level defaults, cleaner resolution
- Cons: Additional field

**Option B:** CostHead only at line-item level
- Pros: Simpler, explicit per item
- Cons: No product defaults

**Recommendation:** Document decision in Data Dictionary

---

**Last Updated:** 2025-01-27  
**Status:** ✅ FREEZE GATE VERIFICATION COMPLETE  
**Next Action:** Final freeze approval (stakeholder sign-off)

## Verification Evidence Summary

### A1: BOM Tracking Fields - ✅ VERIFIED
**Evidence:** `NSW_SCHEMA_CANON_v1.0.md` `quote_boms` table (lines 832-867):
- `origin_master_bom_id` BIGINT NULL, FK to `master_boms.id` (line 843, FK line 856)
- `origin_master_bom_version` VARCHAR(50) NULL (line 844)
- `instance_sequence_no` INTEGER NULL (line 845)
- `is_modified` BOOLEAN NOT NULL DEFAULT false (line 846)
- `modified_by` BIGINT NULL, FK to `users.id` (line 847, FK line 857)
- `modified_at` TIMESTAMP NULL (line 848)

### A3: CostHead System - ✅ VERIFIED
**Evidence:** `NSW_SCHEMA_CANON_v1.0.md`:
- `cost_heads` table exists (lines 964-983) with id, code, name, category, priority
- `quote_bom_items.cost_head_id` BIGINT NULL, FK to `cost_heads.id` (line 891, FK line 906)
- `products.cost_head_id` BIGINT NULL, FK to `cost_heads.id` (D-006 APPROVED, line 367, FK line 378)
- Resolution order documented in `COSTHEAD_RULES.md`

### A9: Customer Normalization - ✅ VERIFIED (D-009 APPROVED)
**Evidence:** `NSW_SCHEMA_CANON_v1.0.md` `quotations` table (lines 779-802):
- `customer_id` BIGINT NULL, FK to `customers.id` (line 784, FK line 792)
- `customer_name_snapshot` VARCHAR(255) NULL (line 785)
- Decision documented as D-009 in Decision Register

### A10: Resolution Level Constraints - ✅ VERIFIED IN SCHEMA
**Evidence:** `NSW_SCHEMA_CANON_v1.0.md`:
- `master_bom_items.resolution_status` VARCHAR(10) CHECK (L0, L1) - L0/L1 only (line 723)
- `quote_bom_items.resolution_status` VARCHAR(10) CHECK (L0, L1, L2) - L0/L1/L2 allowed (line 892)
- CHECK constraint `chk_quote_bom_item_resolution` enforces: L2 => product_id NOT NULL (lines 907-910)

### A2: IsLocked Fields - ✅ VERIFIED (Per D-005)
**Evidence:** `NSW_SCHEMA_CANON_v1.0.md` + Decision Register D-005:
- `quote_bom_items.is_locked` BOOLEAN NOT NULL DEFAULT false - VERIFIED (line 890)
- `quote_panels.is_locked` - EXCLUDED (MVP, per D-005)
- `quote_boms.is_locked` - EXCLUDED (MVP, per D-005)
- `quotations.is_locked` - EXCLUDED (MVP, per D-005)
- Locking scope declaration: Documented in LOCKING_POLICY.md and D-005

