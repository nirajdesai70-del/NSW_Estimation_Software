# NEPL Canonical Rules (Single Source of Truth)

**File:** docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md  
**Version:** v1.0_2025-12-19  
**Status:** 🔒 FROZEN (Phase-4 Canonical Rules)  
**Purpose:** Single source of truth for all NEPL governance rules. All future code and documentation must reference this file.

---

## ⚠️ CRITICAL: This is the Anchor File

**Before making ANY code or documentation changes:**
1. Read this file completely
2. Understand the L0/L1/L2 layer model
3. Verify your change does not violate frozen rules
4. Reference this file in your documentation

**This file is FROZEN. Changes require:**
- Change-control note
- Version bump
- Approval from governance lead

---

## 1. L0/L1/L2 Layer Definitions (FROZEN)

### 1.1 Layer Hierarchy

- **L0 = Generic Item Master (Functional Family)**
  - Example: MCC / MCCB / ACB
  - No technical specification, no make, no series, no SKU
  - Unique; never duplicated; never used directly in any BOM
  - ProductType = 1 (Generic Product)

- **L1 = Technical Variant (Make-agnostic)**
  - Example: MCCB 25A, 25kA / 35kA / 50kA
  - Derived from L0 + technical spec set
  - Unique; never duplicated; reusable
  - ProductType = 1 (Generic Product)
  - **Master BOM operates at L1**
  - **Master BOM must not contain L2**

- **L2 = Catalog Item (Make + Series + SKU/Model)**
  - Example: Schneider / ABB / Siemens model variants
  - Derived from L1 + Make + Series (+ SKU/Model)
  - Unique; never duplicated; reusable
  - ProductType = 2 (Specific Product)
  - **Proposal/Specific BOM operates at L2**
  - **Proposal/Specific BOM = Quotation-specific instance**
  - Multiple Proposal BOMs can exist for one Master BOM
  - Must resolve L1 → L2 before finalization

### 1.2 Layer Usage Rules

**L0 Rules:**
- L0 is FROZEN
- Any change requires change-control note + version bump
- L0 products are NEVER used directly in any BOM
- L0 products are ProductType = 1

**L1 Rules:**
- L1 is used in Master BOM only
- Master BOM must NOT contain L2 products
- L1 products are ProductType = 1
- No L2 fields (MakeId, SeriesId, SKU) on L1 products

**L2 Rules:**
- L2 is used in Proposal BOM only
- Proposal BOM must ALWAYS use L2 products in final state
- L2 products are ProductType = 2
- L2 products require MakeId > 0 and SeriesId > 0

---

## 2. Master BOM vs Proposal BOM Rules

### 2.1 Master BOM Rules

- **Layer:** L1 only (Generic products, ProductType = 1)
- **Purpose:** Technical variant template (make-agnostic)
- **Content:** Generic products derived from L0 + technical specs
- **Forbidden:**
  - ❌ L2 products (ProductType = 2)
  - ❌ MakeId or SeriesId fields
  - ❌ SKU-level pricing
  - ❌ Direct use in quotations (must copy to Proposal BOM first)

### 2.2 Proposal BOM Rules

- **Layer:** L2 only (Specific products, ProductType = 2)
- **Purpose:** Quotation-specific instance with resolved products
- **Content:** Specific products (Make + Series + SKU)
- **Required:**
  - ✅ ProductType = 2 (Specific Product)
  - ✅ MakeId > 0
  - ✅ SeriesId > 0 (unless explicitly exempted)
  - ✅ GenericId present (for traceability to L1)
- **Forbidden:**
  - ❌ ProductType = 1 in final persisted state
  - ❌ MakeId = 0 or SeriesId = 0 in final persisted state
  - ❌ Raw DB inserts bypassing validation
  - ❌ Direct `QuotationSaleBomItem::create()` outside `ProposalBomItemWriter`

### 2.3 Copy Semantics (L1 → L2 Resolution)

When copying from Master BOM to Proposal BOM:
- **Source:** Master BOM (L1, Generic products)
- **Target:** Proposal BOM (L2, Specific products)
- **Process:** L1 → L2 resolution
- **Transitional State:** Generic products acceptable as INTERMEDIATE state only
- **Finalization:** Must resolve to Specific (ProductType=2, MakeId>0, SeriesId>0) before finalization

---

## 3. Resolution-B Rules (CLOSED)

**Status:** ✅ CLOSED (Option-A Implemented + Runtime Verified)  
**Reference:** `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md`

### 3.1 L2 Write Requirements

A Proposal BOM item (`QuotationSaleBomItem`) write is allowed **ONLY** when ALL of the following are true:

1. **ProductType = 2** (Specific Product)
   - Generic products (ProductType=1) are FORBIDDEN in final persisted state
   - Exception: Transitional state during L1→L2 resolution (must resolve before finalization)

2. **GenericId is present**
   - Must reference the underlying Generic product (L0/L1 layer)
   - Required for traceability and resolution context

3. **MakeId > 0**
   - Must be a valid Make identifier
   - Default to 0 is FORBIDDEN in final state
   - Exception: Explicitly flagged "pending resolution" state (must resolve before finalization)

4. **SeriesId > 0** (unless explicitly exempted)
   - Must be a valid Series identifier
   - Default to 0 is FORBIDDEN in final state
   - Exception: Explicitly exempted products (documented, rare)

5. **Status = 0** (Active) implies all above requirements
   - Any Proposal BOM item with Status=0 and usable in costing/export/apply must satisfy all L2 requirements
   - Soft-deleted items (Status=1) are exempt from validation

### 3.2 Write Gateway Enforcement

**All Proposal BOM writes MUST go through `ProposalBomItemWriter` service:**
- ✅ Use `ProposalBomItemWriter::createItem()`
- ✅ Use `ProposalBomItemWriter::createFromMasterBom()`
- ✅ Use `ProposalBomItemWriter::createFromFeederTemplate()`
- ✅ Use `ProposalBomItemWriter::createFromProposalBom()`
- ✅ Use `ProposalBomItemWriter::resolveItem()`
- ❌ FORBIDDEN: Direct `QuotationSaleBomItem::create()` outside gateway
- ❌ FORBIDDEN: Raw DB inserts (`DB::table('quotation_sale_bom_items')->insert()`)

**Reference:** `docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md`

### 3.3 Raw DB Inserts Are Forbidden

Direct database inserts into `quotation_sale_bom_items` are FORBIDDEN:
- `DB::table('quotation_sale_bom_items')->insert()` — FORBIDDEN
- `DB::insert()` targeting `quotation_sale_bom_items` — FORBIDDEN

**Rationale:**
- Bypasses application validation
- Bypasses business rules
- Creates audit trail gaps
- Introduces data integrity risks

**Exception:**
- Data migration scripts (must be explicitly approved, documented, and one-time)

### 3.4 Reuse/Apply Must CLEAR or MERGE Explicitly

When applying/reusing Proposal BOM items:
- **Default behavior:** CLEAR existing items before copying
- **Merge mode:** Only if explicitly flagged (rare, must be documented)

**Forbidden patterns:**
- Apply without clearing → creates duplicate stacking
- Silent merge without explicit flag → creates confusion and potential data corruption

---

## 4. Transitional State Rules + ensureResolved Requirement

### 4.1 Transitional State Definition

During L1→L2 resolution (copy from Master BOM/Feeder):
- **Copy phase:** Generic ProductId is acceptable
  - `ProductId` from Master BOM (Generic, ProductType=1)
  - `MakeId = 0`, `SeriesId = 0`
- **Resolution phase:** Must resolve before finalization
  - User selects Make/Series
  - System updates to Specific product (ProductType=2)
  - Sets `MakeId > 0`, `SeriesId > 0`
- **Finalization phase:** All L2 requirements must be met
  - `Status = 0` implies `ProductType = 2`, `MakeId > 0`, `SeriesId > 0`

### 4.2 ensureResolved Requirement

**All Proposal BOM finalization/export/apply operations MUST call `ensureResolved()`:**
- Blocks finalization if any items are in transitional state (ProductType=1 or MakeId=0/SeriesId=0)
- Forces explicit L1→L2 resolution before persistence
- Prevents transitional state from being used in costing/export/apply operations

**Forbidden:**
- Persisting transitional state as "final" (Status=0 with ProductType=1 or MakeId=0)
- Allowing transitional state to be used in costing/export/apply operations

**Reference:** `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md` (Section: ensureResolved Requirement)

---

## 5. DB Verification Pack References

All governance documents must include DB verification sections where applicable. Before final acceptance/production freeze, execute DB verification and update status from **DB-PENDING → VERIFIED**.

**DB Verification Pack locations:**
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md` (Section: 🔍 DB Verification Pack)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md` (Section: 🔍 DB Verification Pack)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` (DB verification items)

**DB Verification Requirements:**
- Verify no ProductType=1 items in Proposal BOM final state
- Verify no ProductType=2 items with MakeId=0 or SeriesId=0
- Verify all write operations go through gateway
- Verify L0/L1/L2 integrity in database

---

## 6. Code Enforcement Rules

### 6.1 Forbidden Patterns

**NEVER reintroduce these patterns:**
- ❌ `DB::table('quotation_sale_bom_items')->insert(...)`
- ❌ `QuotationSaleBomItem::create(...)` outside `ProposalBomItemWriter`
- ❌ `MakeId => 0 ?? 0` (silent default to zero)
- ❌ `SeriesId => 0 ?? 0` (silent default to zero)
- ❌ ProductType=1 in Proposal BOM final state
- ❌ L2 fields (MakeId, SeriesId) on ProductType=1 products

### 6.2 Required Patterns

**ALWAYS use these patterns:**
- ✅ `ProposalBomItemWriter::createItem(...)` for new items
- ✅ `ProposalBomItemWriter::createFromMasterBom(...)` for Master BOM copies
- ✅ `ProposalBomItemWriter::createFromFeederTemplate(...)` for Feeder copies
- ✅ `ProposalBomItemWriter::resolveItem(...)` for Make/Series resolution
- ✅ `ensureResolved()` before finalization/export/apply
- ✅ Explicit validation errors (no silent failures)

---

## 7. Documentation Rules

### 7.1 Canonical Reference Requirement

All relevant documentation must either:
- Include the canonical L0/L1/L2 block (Section 1.1), OR
- Reference this canonical rules file

**This avoids duplication and drift.**

### 7.2 Documentation Update Rules

When updating documentation:
1. Check if L0/L1/L2 definitions are needed
2. If yes, either:
   - Copy Section 1.1 verbatim, OR
   - Add reference: "See `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` for L0/L1/L2 definitions"
3. Ensure Resolution-B rules are referenced where applicable
4. Ensure Master BOM vs Proposal BOM rules are clear

---

## 8. Change Control

### 8.1 Frozen Rules

The following are FROZEN and require change-control approval:
- L0/L1/L2 layer definitions (Section 1.1)
- Master BOM vs Proposal BOM rules (Section 2)
- Resolution-B rules (Section 3) — CLOSED, no changes allowed
- Transitional state rules (Section 4)

### 8.2 Change Process

To modify frozen rules:
1. Create change-control note with justification
2. Version bump this file
3. Update all referencing documentation
4. Get approval from governance lead
5. Update change log

---

## 9. References

### 9.1 Core Standards
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md` — Cumulative verification methodology
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md` — Product archival rules

### 9.2 Resolution-B Documents
- `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md` — Resolution-B summary (CLOSED)
- `docs/RESOLUTION_B/RESOLUTION_B_RULES.md` — Detailed Resolution-B rules
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md` — Write gateway design
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_PATHS.md` — Write paths inventory

### 9.3 Gap Registers
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` — Proposal BOM gaps
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` — Master BOM gaps

---

## 10. Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0_2025-12-19 | 2025-12-19 | Phase-4: Initial canonical rules file created. Consolidated L0/L1/L2, Master BOM vs Proposal BOM, Resolution-B, and transitional state rules into single source of truth. |

---

**END OF DOCUMENT**

