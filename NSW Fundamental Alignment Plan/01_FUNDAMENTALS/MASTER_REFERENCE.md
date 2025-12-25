# Fundamentals Master Reference — Complete Layer Documentation

**Version:** v1.1  
**Date:** 2025-12-XX (Placeholder; derives from repo doc dates)  
**Status:** 📋 PLANNING MODE ONLY (No Runtime Testing)  
**Purpose:** Complete reference for all fundamentals layers (purpose/definition/usage/procedure/files/gaps)  
**Source of Truth:** Repository content only (no invented schemas/fields)

**⚠️ CRITICAL:** See [PATCH_APPENDIX_v1.1.md](./PATCH_APPENDIX_v1.1.md) for audit-safe guardrails, schema inference rules, and legacy data integrity strategy.

---

## Universal Badge Legend

All schema/implementation references use these badges:

| Badge | Meaning |
|-------|---------|
| **CONFIRMED-IN-REPO** | Explicitly found in repository (migration/model/query file reference) |
| **INFERRED** | Hypothesis based on usage patterns or documentation references |
| **DOC-CLOSED** | Documentation/spec frozen; planning complete; no runtime validation |
| **RUN-CLOSED** | Verified via SQL/API requests + evidence archive; runtime validated |

**Rule:** Any table/field naming shown as schema is hypothesis unless backed by an explicit migration/model/query file reference. Hypotheses must be tagged as **INFERRED** and never treated as truth.

---

## Document Structure

This document covers all fundamentals layers in canonical sequence:

1. **A. Category / Subcategory / Type(Item) / Attributes**
2. **B. Item/Component List (catalog / component base list)**
3. **C. Generic Item Master**
4. **D. Specific Item Master**
5. **E. Master BOM (generic)**
6. **F. Master BOM (specific)** — NOT FOUND IN REPO (needs decision)
7. **G. Proposal BOM + Proposal Sub-BOM**
8. **H. Feeder BOM**
9. **I. Panel BOM**

Each layer section includes:
- Purpose (why this exists)
- Definition (what exactly it is in our system)
- Where Used (which module/screens/services use it)
- How Used (workflow + data flow; upstream inputs → outputs)
- Importance (what breaks if this is wrong)
- Planned Procedure (our planned governance + steps; execution gates if any)
- Source-of-Truth Files (absolute file list with paths)
- Key Rules (copy-never-link, Status=0 visibility, thin controller, etc. — only if documented)
- Known Gaps / Open Items (with references to gap registers or TODOs)

---

## A. Category / Subcategory / Type(Item) / Attributes

### Purpose

Category, Subcategory, Type (Item), and Attributes form the foundational classification hierarchy for products in the NSW Estimation Software. This hierarchy enables:
- Product grouping and filtering
- Lookup pipeline navigation (Category → Subcategory → Item → Product)
- Vendor-neutral attribute definition
- Product identity anchoring (Item/ProductType is the device identity anchor)

### Definition

**Category:**
- Used only for grouping/filtering
- No device identity derived from Category
- Schema: `categories` table — **INFERRED** (no migration found in repo)

**Subcategory:**
- Additive feature-like subcategories expressed via attributes/tags
- Primary SubCategory is consistent
- Exception: EX-SUBCAT-001 (SubCategory additive transitional exception)
- Schema: `subcategories` table — **INFERRED** (no migration found in repo)

**Type(Item):**
- Item/ProductType is the device identity anchor
- ProductType = 1 (Generic Product) for L0/L1
- ProductType = 2 (Specific Product) for L2
- Schema: `items` or `products` table with `ProductType` field — **INFERRED** (referenced in docs, no migration verified)

**Attributes:**
- Vendor-neutral attributes
- Attributes are not device identity (Category ≠ Item/ProductType)
- Used for technical specifications (make-agnostic)

### Where Used

- **Product lookup flows:** Category → Subcategory → Item → Product navigation
- **Master BOM creation:** L1 products reference Item/ProductType
- **Proposal BOM resolution:** L1 → L2 resolution uses Item/ProductType context
- **Product search:** SKU search operates within Item/ProductType context
- **Attribute filtering:** Attributes used for product selection

### How Used

**Workflow:**
1. User navigates Category → Subcategory → Item/ProductType
2. System resolves to Generic Product (L0/L1, ProductType=1) or Specific Product (L2, ProductType=2)
3. Attributes provide vendor-neutral technical specs
4. Lookup pipeline: Category → Subcategory → Item → Product → Make → Series → SKU

**Data Flow:**
- **Upstream:** Category/Subcategory/Item definitions (design-time)
- **Downstream:** Product resolution → Master BOM items → Proposal BOM items

### Importance

**What breaks if this is wrong:**
- Product lookup pipeline breaks (Category → Subcategory → Item chain)
- Product identity confusion (Category used as identity instead of Item/ProductType)
- Attribute mapping failures (vendor-neutral attributes not preserved)
- Master BOM → Proposal BOM resolution fails (L1 → L2 resolution requires Item/ProductType)

### Planned Procedure

**Governance:**
- Category compliance: Category used only for grouping/filtering
- SubCategory compliance: EX-SUBCAT-001 exception-aware
- Item/ProductType compliance: Item/ProductType is device identity anchor
- Attributes compliance: Vendor-neutral attributes maintained

**Execution Gates:**
- See `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md` for verification checklist

### Source-of-Truth Files

- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — L0/L1/L2 layer definitions, Category/Subcategory/Item rules
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md` — Category/Subcategory/Item verification methodology
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_EXEC_MASTER_BOM_REVIEW_PLAYBOOK_v1.0_20251218.md` — Category/Subcategory/Item compliance checks
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/CURSOR_ONLY_EXEC_NEPL_GOVERNANCE_CHECKLIST_v1.0_20251218.md` — Governance checklist

### Key Rules

1. **Category ≠ Item/ProductType:** Category is grouping only, not device identity
2. **Item/ProductType is identity anchor:** Device identity comes from Item/ProductType, not Category
3. **Attributes are vendor-neutral:** Attributes do not include make/series/SKU
4. **SubCategory exception:** EX-SUBCAT-001 (additive transitional exception)

### Known Gaps / Open Items

- **NOT FOUND IN REPO:** Explicit Category/Subcategory/Item schema definitions (inferred from usage)
- **NOT FOUND IN REPO:** Explicit Attribute schema definition (inferred from usage)
- See `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CUMULATIVE_VERIFICATION_STANDARD_v1.0_20251218.md` for verification requirements

---

## B. Item/Component List (catalog / component base list)

### Purpose

Item/Component List serves as the catalog or component base list that contains all available products/components in the system. This is the master product catalog that feeds into Generic Item Master and Specific Item Master.

### Definition

**Item/Component List:**
- Master catalog of all products/components
- Contains both Generic products (ProductType=1) and Specific products (ProductType=2)
- Base reference for all BOM operations
- Schema: `products` table — **INFERRED** (referenced in docs, no migration verified)

### Where Used

- **Product selection:** Users select products from catalog
- **Master BOM creation:** Master BOM items reference products from catalog
- **Proposal BOM resolution:** L1 → L2 resolution uses catalog products
- **Product lookup:** SKU search operates on catalog

### How Used

**Workflow:**
1. Products defined in catalog (Item/Component List)
2. Master BOM references Generic products (ProductType=1) from catalog
3. Proposal BOM references Specific products (ProductType=2) from catalog
4. Product resolution: L1 (Generic) → L2 (Specific) uses catalog

**Data Flow:**
- **Upstream:** Product definitions (design-time)
- **Downstream:** Generic Item Master, Specific Item Master, Master BOM, Proposal BOM

### Importance

**What breaks if this is wrong:**
- Product references break (BOM items reference non-existent products)
- Product lookup fails (SKU search cannot find products)
- L1 → L2 resolution fails (Generic → Specific product mapping broken)

### Planned Procedure

**Governance:**
- Product catalog integrity maintained
- ProductType consistency (L0/L1 = ProductType=1, L2 = ProductType=2)
- Product archival rules enforced (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md`)

### Source-of-Truth Files

- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — ProductType rules (L0/L1 = ProductType=1, L2 = ProductType=2)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md` — Product archival rules
- **NOT FOUND IN REPO:** Explicit Item/Component List schema definition (inferred from usage)

### Key Rules

1. **ProductType consistency:** L0/L1 products are ProductType=1, L2 products are ProductType=2
2. **Product archival:** Generic products cannot be archived if Specific products exist (see archival standard)

### Known Gaps / Open Items

- **NOT FOUND IN REPO:** Explicit Item/Component List schema definition (inferred from `products` table usage)
- **NOT FOUND IN REPO:** Explicit catalog management procedures

---

## C. Generic Item Master

### Purpose

Generic Item Master represents L0/L1 layer products (Functional Family and Technical Variant, make-agnostic). These are generic products used in Master BOM only, never directly in Proposal BOM final state.

### Definition

**Generic Item Master:**
- **L0 = Generic Item Master (Functional Family):** Example: MCC / MCCB / ACB
  - No technical specification, no make, no series, no SKU
  - Unique; never duplicated; never used directly in any BOM
  - ProductType = 1 (Generic Product)

- **L1 = Technical Variant (Make-agnostic):** Example: MCCB 25A, 25kA / 35kA / 50kA
  - Derived from L0 + technical spec set
  - Unique; never duplicated; reusable
  - ProductType = 1 (Generic Product)
  - **Master BOM operates at L1**

**Schema:** `products` table where `ProductType = 1` — **INFERRED** (referenced in docs, no migration verified)

### Where Used

- **Master BOM:** Master BOM items reference Generic products (L1, ProductType=1)
- **L1 → L2 resolution:** Generic products resolve to Specific products during Proposal BOM creation
- **Product lookup:** Generic products are searchable but not used in Proposal BOM final state

### How Used

**Workflow:**
1. Generic products defined in Generic Item Master (L0/L1, ProductType=1)
2. Master BOM references Generic products (L1)
3. When copying Master BOM to Proposal BOM:
   - Generic products copied initially (transitional state)
   - User selects Make/Series
   - System resolves to Specific product (L2, ProductType=2)
   - Proposal BOM final state uses Specific products only

**Data Flow:**
- **Upstream:** Product definitions (design-time)
- **Downstream:** Master BOM items → Proposal BOM items (via L1 → L2 resolution)

### Importance

**What breaks if this is wrong:**
- Master BOM cannot reference Generic products (violates L1-only rule)
- L1 → L2 resolution fails (Generic → Specific mapping broken)
- Proposal BOM may contain Generic products in final state (violates L2-only rule)

### Planned Procedure

**Governance:**
- Generic Item Master Round-1 and Round-2 reviews completed (see freeze notice)
- ProductResolutionService enforces L2 rules
- ProductArchiveService active
- EX-SUBCAT-001 acknowledged

**Execution Gates:**
- Generic Item Master frozen (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md`)

### Source-of-Truth Files

- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — L0/L1 layer definitions, Generic Item Master rules
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_FREEZE_v1.0_20251218.md` — Freeze declaration
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_FINAL_v1.0_20251218.md` — Round-2 review
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md` — Archival rules

### Key Rules

1. **L0/L1 = ProductType=1:** Generic products are ProductType=1
2. **Master BOM operates at L1:** Master BOM must use Generic products (L1) only
3. **Never used in Proposal BOM final state:** Generic products are transitional only
4. **No L2 fields:** Generic products have no MakeId, SeriesId, SKU

### Known Gaps / Open Items

- **NOT FOUND IN REPO:** Explicit Generic Item Master schema definition (inferred from `products` table with `ProductType=1`)
- Generic Item Master frozen (Round-2 complete, see freeze notice)

---

## D. Specific Item Master

### Purpose

Specific Item Master represents L2 layer products (Catalog Item with Make + Series + SKU). These are specific products used in Proposal BOM only, never in Master BOM.

### Definition

**Specific Item Master:**
- **L2 = Catalog Item (Make + Series + SKU/Model):** Example: Schneider / ABB / Siemens model variants
  - Derived from L1 + Make + Series (+ SKU/Model)
  - Unique; never duplicated; reusable
  - ProductType = 2 (Specific Product)
  - **Proposal/Specific BOM operates at L2**
  - **Proposal/Specific BOM = Quotation-specific instance**
  - Multiple Proposal BOMs can exist for one Master BOM
  - Must resolve L1 → L2 before finalization

**Schema:** `products` table where `ProductType = 2`, with `MakeId > 0` and `SeriesId > 0` — **INFERRED** (referenced in docs, no migration verified)

### Where Used

- **Proposal BOM:** Proposal BOM items reference Specific products (L2, ProductType=2)
- **L1 → L2 resolution:** Generic products resolve to Specific products during Proposal BOM creation
- **Product lookup:** Specific products are searchable by Make/Series/SKU

### How Used

**Workflow:**
1. Specific products defined in Specific Item Master (L2, ProductType=2)
2. When copying Master BOM to Proposal BOM:
   - Generic products copied initially (transitional state)
   - User selects Make/Series
   - System resolves to Specific product (L2, ProductType=2)
   - Proposal BOM final state uses Specific products only

**Data Flow:**
- **Upstream:** Generic Item Master (L1) → Specific Item Master (L2) resolution
- **Downstream:** Proposal BOM items (L2 only)

### Importance

**What breaks if this is wrong:**
- Proposal BOM may contain Generic products in final state (violates L2-only rule)
- ProductType=2 items missing MakeId/SeriesId (violates L2 requirements)
- L1 → L2 resolution fails (Generic → Specific mapping broken)

### Planned Procedure

**Governance:**
- Specific Item Master Round-0 Readiness checklist (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND0_READINESS_v1.0_20251218.md`)
- Pre-conditions: Generic Item Master frozen, ProductResolutionService enforces L2 rules
- Specific Item Master Round-1 kickoff (see readiness checklist)

**Execution Gates:**
- Specific Item Master Round-0 Readiness (all pre-conditions must be met)

### Source-of-Truth Files

- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — L2 layer definitions, Specific Item Master rules
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND0_READINESS_v1.0_20251218.md` — Round-0 readiness checklist
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND1_CHECKLIST.md` — Round-1 checklist
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND1_KICKOFF_TEMPLATE.md` — Round-1 kickoff template

### Key Rules

1. **L2 = ProductType=2:** Specific products are ProductType=2
2. **Proposal BOM operates at L2:** Proposal BOM must use Specific products (L2) only in final state
3. **MakeId > 0 and SeriesId > 0:** Specific products require Make and Series
4. **Never used in Master BOM:** Specific products are Proposal BOM only

### Known Gaps / Open Items

- **NOT FOUND IN REPO:** Explicit Specific Item Master schema definition (inferred from `products` table with `ProductType=2`)
- Specific Item Master Round-0 Readiness checklist exists (see readiness document)
- See `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/SPECIFIC_ITEM_MASTER_ROUND0_READINESS_v1.0_20251218.md` for gap revalidation

---

## E. Master BOM (generic)

### Purpose

Master BOM serves as the design-time template for BOM structures. Master BOM operates at L1 only (Generic products, ProductType=1), defining technical variants (make-agnostic) that can be copied to Proposal BOM.

### Definition

**Master BOM:**
- Design-time template definition
- **Layer:** L1 only (Generic products, ProductType = 1)
- **Purpose:** Technical variant template (make-agnostic)
- **Content:** Generic products derived from L0 + technical specs
- **Schema:** `master_boms` table where `TemplateType = 'BOM'` — **INFERRED** (referenced in docs, no migration verified)

**Key Characteristics:**
- One Master BOM → Many Proposal BOMs (across quotations)
- Master BOM items reference Generic products (L1, ProductType=1)
- Master BOM never contains L2 products (ProductType=2)
- Master BOM is copied (not linked) to Proposal BOM

### Where Used

- **BOM template selection:** Users select Master BOM template to apply to quotation
- **Proposal BOM creation:** Master BOM copied to Proposal BOM (L1 → L2 resolution)
- **BOM structure definition:** Master BOM defines allowed BOM structure

### How Used

**Workflow:**
1. Master BOM defined (design-time, L1 products only)
2. User selects Master BOM template for quotation
3. System copies Master BOM to Proposal BOM:
   - Generic products copied initially (transitional state)
   - User selects Make/Series for each product
   - System resolves to Specific products (L2, ProductType=2)
   - Proposal BOM final state uses Specific products only

**Data Flow:**
- **Upstream:** Generic Item Master (L1 products)
- **Downstream:** Proposal BOM (via copy operation with L1 → L2 resolution)

### Importance

**What breaks if this is wrong:**
- Master BOM contains L2 products (violates L1-only rule)
- Proposal BOM creation fails (L1 → L2 resolution broken)
- Copy-never-link violated (Master BOM mutated by Proposal BOM)

### Planned Procedure

**Governance:**
- Master BOM correction plan (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md`)
- Master BOM gap register (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md`)
- Master BOM cumulative review (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md`)

**Execution Gates:**
- Master BOM Round-0 Readiness (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md`)

### Source-of-Truth Files

- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — Master BOM rules (L1 only, ProductType=1)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CORRECTION_PLAN_v1.0_20251218.md` — Correction plan
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` — Gap register
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_CUMULATIVE_REVIEW_R1_v1.0_20251218.md` — Cumulative review
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_ROUND0_READINESS_v1.0_20251218.md` — Round-0 readiness
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Canonical hierarchy (BOM Master definition)

### Key Rules

1. **L1 only:** Master BOM must use Generic products (L1, ProductType=1) only
2. **No L2 products:** Master BOM must not contain L2 products (ProductType=2)
3. **Copy-never-link:** Proposal BOMs are copies, not links to Master BOM
4. **No upward mutation:** Proposal BOMs never mutate Master BOM

### Known Gaps / Open Items

- See `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/MASTER_BOM_GAP_REGISTER_R1_v1.0_20251218.md` for gap entries
- Master BOM correction plan exists (see correction plan document)

---

## F. Master BOM (specific)

### Status

**NOT FOUND IN REPO (needs decision)**

No explicit documentation found for "Master BOM (specific)" as a separate layer. Based on canonical rules:
- Master BOM operates at L1 only (Generic products)
- Specific products (L2) are used in Proposal BOM only

**Possible interpretations:**
1. This layer does not exist (Master BOM is always generic/L1)
2. This refers to a future enhancement (not yet documented)
3. This refers to a different concept (needs clarification)

**Recommendation:** Clarify with stakeholders whether "Master BOM (specific)" is a valid layer or should be removed from the sequence.

---

## G. Proposal BOM + Proposal Sub-BOM

### Purpose

Proposal BOM serves as the runtime, quotation-specific instance of a BOM structure. Proposal BOM operates at L2 only (Specific products, ProductType=2), created by copying from Master BOM with L1 → L2 resolution.

### Definition

**Proposal BOM:**
- Runtime, quotation-specific instance
- **Layer:** L2 only (Specific products, ProductType = 2)
- **Purpose:** Quotation-specific instance with resolved products
- **Content:** Specific products (Make + Series + SKU)
- **Schema:** `quotation_sale_boms` table (executable BOMs) — **INFERRED** (referenced in docs, no migration verified)

**Proposal Sub-BOM:**
- Nested BOM within Proposal BOM
- Same L2 requirements as Proposal BOM
- Hierarchical structure (BOM → Sub-BOM → Items)

**Key Characteristics:**
- One Proposal BOM Master (QuotationId) owns all Proposal BOMs
- Proposal BOMs are copies (not links) from Master BOM
- Proposal BOM final state uses Specific products (L2, ProductType=2) only
- Proposal BOM items reference Item Master (ProductType=2)

### Where Used

- **Quotation creation:** Proposal BOMs created when applying Master BOM to quotation
- **BOM editing:** Users edit Proposal BOM items (quantity, Make/Series, etc.)
- **Costing/export:** Proposal BOMs used for pricing calculations and export
- **BOM reuse:** Proposal BOMs can be reused across quotations (copy operation)

### How Used

**Workflow:**
1. User selects Master BOM template for quotation
2. System copies Master BOM to Proposal BOM:
   - Generic products copied initially (transitional state, ProductType=1)
   - User selects Make/Series for each product
   - System resolves to Specific product (L2, ProductType=2)
   - Proposal BOM final state uses Specific products only
3. Users can edit Proposal BOM items (quantity, attributes, etc.)
4. Proposal BOM used for costing/export/apply operations

**Data Flow:**
- **Upstream:** Master BOM (L1) → Proposal BOM (L2) via copy with L1 → L2 resolution
- **Downstream:** Proposal BOM Items → Costing/Export/Apply operations

### Importance

**What breaks if this is wrong:**
- Proposal BOM contains Generic products in final state (violates L2-only rule)
- ProductType=2 items missing MakeId/SeriesId (violates L2 requirements)
- Copy-never-link violated (Proposal BOM mutates Master BOM)
- Costing/export fails (incomplete product resolution)

### Planned Procedure

**Governance:**
- Proposal BOM correction plan (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CORRECTION_PLAN_v1.0_2025-12-19.md`)
- Proposal BOM gap register (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md`)
- Proposal BOM cumulative review (see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md`)
- Resolution-B rules (see `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md`)

**Execution Gates:**
- Proposal BOM verification gates (see gap register for gate structure)

### Source-of-Truth Files

- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` — Proposal BOM rules (L2 only, ProductType=2)
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CORRECTION_PLAN_v1.0_2025-12-19.md` — Correction plan
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` — Gap register
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_CUMULATIVE_REVIEW_R1_v1.0_2025-12-19.md` — Cumulative review
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_HIERARCHY_CLARIFICATION_v1.0_2025-12-19.md` — Hierarchy clarification
- `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md` — Resolution-B rules (L2 write requirements)
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md` — Write gateway design
- `PLANNING/FUNDAMENTS_CORRECTION/PROPOSAL_BOM_MASTER_BACKEND_DESIGN_v1.0.md` — Proposal BOM Master design
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Canonical hierarchy (Proposal BOM definition)

### Key Rules

1. **L2 only:** Proposal BOM must use Specific products (L2, ProductType=2) only in final state
2. **MakeId > 0 and SeriesId > 0:** Specific products require Make and Series
3. **Copy-never-link:** Proposal BOMs are copies, not links from Master BOM
4. **No upward mutation:** Proposal BOMs never mutate Master BOM
5. **Write gateway:** All Proposal BOM writes must go through `ProposalBomItemWriter` gateway
6. **ensureResolved requirement:** All Proposal BOM finalization/export/apply operations must call `ensureResolved()`

### Known Gaps / Open Items

- See `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md` for gap entries
- Proposal BOM correction plan exists (see correction plan document)
- Resolution-B rules implemented (see Resolution-B summary)

---

## H. Feeder BOM

### Purpose

Feeder BOM serves as the design-time template for feeder types. Feeder Master defines feeder type, allowed BOM structure, and default behavior, reusable across multiple panels. Feeder Instances are runtime copies of Feeder Master.

### Definition

**Feeder Master (Design-time):**
- Design-time definition of a feeder type
- **Schema:** `master_boms` table where `TemplateType = 'FEEDER'` — **INFERRED** (referenced in docs, no migration verified)
- **Key:** `MasterBomId` (serves as FeederMasterId)
- **Purpose:** Canonical feeder definition (what a feeder is conceptually)
- **Reusable:** One Feeder Master → Many Feeder Instances (across all panels)

**Feeder Instance (Runtime):**
- Runtime copy of Feeder Master
- **Schema:** `quotation_sale_boms` table where `MasterBomId` references Feeder Master — **INFERRED** (referenced in docs, no migration verified)
- **Key:** `QuotationSaleBomId`
- **Purpose:** Quotation-specific feeder instance
- **Ownership:** Belongs to Proposal BOM Master (QuotationId)

**Key Characteristics:**
- Feeder Master is NOT tied to a single panel
- Feeder Instances are copies (not links) from Feeder Master
- Copy-never-link: Feeder Instances never mutate Feeder Master
- Clear-before-copy: Template apply clears existing before copying

### Where Used

- **Feeder template selection:** Users select Feeder Master template to apply to panel
- **Feeder instance creation:** Feeder Master copied to Feeder Instance (runtime)
- **Panel BOM structure:** Feeder Instances are part of Panel BOM structure

### How Used

**Workflow:**
1. Feeder Master defined (design-time, `TemplateType='FEEDER'`)
2. User selects Feeder Master template for panel
3. System applies Feeder template:
   - Detects existing feeder (reuse detection by: QuotationId, QuotationSaleId, MasterBomId, FeederName, Level=0, ParentBomId=NULL, Status=0)
   - If match found → reuse existing feeder
   - If not found → create new feeder
   - Clear-before-copy: Soft-delete existing items before copying
   - Copy items from Feeder Master to Feeder Instance
4. Feeder Instance can be edited (items, quantity, etc.)

**Data Flow:**
- **Upstream:** Feeder Master (design-time) → Feeder Instance (runtime) via copy operation
- **Downstream:** Feeder Instance → Proposal BOMs → Proposal BOM Items

### Importance

**What breaks if this is wrong:**
- Feeder template apply creates duplicate feeders (no reuse detection)
- Feeder items stack instead of being replaced (no clear-before-copy)
- Feeder Instances mutate Feeder Master (copy-never-link violated)
- Feeder Master not correctly identified (TemplateType filter missing)

### Planned Procedure

**Governance:**
- Feeder Master design frozen (see `PLANNING/FUNDAMENTS_CORRECTION/FEEDER_MASTER_BACKEND_DESIGN_v1.0.md`)
- Fundamentals gap correction (see `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md`)
- Feeder BOM planning (see `PLANNING/FEEDER_BOM/` directory)

**Execution Gates:**
- Fundamentals verification gates (G1-G4, see `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md`)
- Feeder BOM execution gates (Gate-0 through Gate-3, see `docs/FEEDER_BOM/PHASE2_EXECUTION_CHECKLIST.md`)

### Source-of-Truth Files

- `PLANNING/FUNDAMENTS_CORRECTION/FEEDER_MASTER_BACKEND_DESIGN_v1.0.md` — Feeder Master design (frozen)
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_BASELINE_BUNDLE_v1.0.md` — Fundamentals baseline (Feeder Master definition)
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Canonical hierarchy (Feeder Master definition)
- `PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md` — Master→Instance mapping (L1: Feeder Master → Feeder Instance)
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_QUERIES.md` — Verification queries (VQ-001, VQ-002 for Feeder Master)
- `PLANNING/FUNDAMENTS_CORRECTION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md` — Verification checklist (G1: Feeder Master Verification)
- `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` — BOM gap register (BOM-GAP-001, BOM-GAP-002 for Feeder)
- `docs/FEEDER_BOM/` — Feeder BOM documentation directory

### Key Rules

1. **Feeder Master = master_boms where TemplateType='FEEDER':** Feeder Master is logical abstraction over `master_boms`
2. **Copy-never-link:** Feeder Instances are copies, not links from Feeder Master
3. **No upward mutation:** Feeder Instances never mutate Feeder Master
4. **Reuse detection:** Feeder template apply detects existing feeder (QuotationId, QuotationSaleId, MasterBomId, FeederName, Level=0, ParentBomId=NULL, Status=0)
5. **Clear-before-copy:** Template apply clears existing items before copying

### Known Gaps / Open Items

- **BOM-GAP-001:** Feeder Template Apply Creates New Feeder Every Time (No Reuse Detection) — OPEN (see `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`)
- **BOM-GAP-002:** Feeder Template Apply Missing Clear-Before-Copy (Duplicate Stacking) — OPEN (see `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md`)
- See `PLANNING/GOVERNANCE/BOM_GAP_REGISTER.md` for complete gap list

---

## I. Panel BOM

### Purpose

Panel BOM serves as the top-level container for all feeders and BOMs within a panel. Panel BOM is the runtime instance of a Panel Master, containing Feeder Instances and Proposal BOMs.

### Definition

**Panel Master (Design-time):**
- Design-time definition of a panel type
- Defines panel structure and allowed feeders
- **Schema:** Panel definition — **INFERRED** (Panel Master concept exists in planning but schema not confirmed in repo)

**Panel Master Discovery Checklist:**
1. **Exact model/table/template type:** Where is Panel Master stored? (Table name, TemplateType value, etc.)
2. **Feeder attachment:** How do Feeder Masters attach to Panel Master? (FK relationship, junction table, etc.)
3. **Panel metadata:** Where does panel name/type, default feeders, etc. live? (Columns, related tables, etc.)
4. **Panel lookup:** How is Panel Master identified/retrieved? (Query pattern, filter criteria, etc.)

**Status:** **INFERRED** — Panel Master concept exists in planning but schema not confirmed in repo. Discovery checklist must be completed before implementation.

**Proposal Panel (Runtime):**
- Runtime copy of Panel Master
- **Schema:** `quotation_sale` table where `QuotationId` references Proposal BOM Master — **INFERRED** (referenced in docs, no migration verified)
- **Key:** `QuotationSaleId`
- **Purpose:** Quotation-specific panel instance
- **Ownership:** Belongs to Proposal BOM Master (QuotationId)

**Panel BOM Structure:**
- Proposal Panel contains Feeder Instances
- Feeder Instances contain Proposal BOMs
- Proposal BOMs contain Proposal BOM Items

**Key Characteristics:**
- Panel BOM is the top-level container (L0 in runtime hierarchy)
- Proposal Panels are copies (not links) from Panel Master
- Copy-never-link: Proposal Panels never mutate Panel Master
- Panel copy operations copy entire tree (feeders → BOMs → items)

### Where Used

- **Panel creation:** Proposal Panels created when creating quotation
- **Panel copy:** Panel BOM can be copied to another quotation (entire tree copy)
- **Feeder management:** Feeder Instances are added to Proposal Panel
- **BOM structure:** Panel BOM defines overall BOM structure for quotation

### How Used

**Workflow:**
1. Panel Master defined (design-time)
2. User creates quotation (Proposal BOM Master)
3. System creates Proposal Panel (runtime copy of Panel Master)
4. User adds Feeder Instances to Proposal Panel
5. Feeder Instances contain Proposal BOMs
6. Proposal BOMs contain Proposal BOM Items
7. Panel BOM can be copied to another quotation (entire tree copy)

**Data Flow:**
- **Upstream:** Panel Master (design-time) → Proposal Panel (runtime) via copy operation
- **Downstream:** Proposal Panel → Feeder Instances → Proposal BOMs → Proposal BOM Items

### Importance

**What breaks if this is wrong:**
- Panel copy fails (entire tree not copied)
- Panel structure breaks (feeders/BOMs not properly contained)
- Copy-never-link violated (Proposal Panels mutate Panel Master)
- Panel ownership breaks (Proposal Panels not properly owned by Proposal BOM Master)

### Planned Procedure

**Governance:**
- Panel BOM planning complete (PB0-PB6, see `PLANNING/PANEL_BOM/MASTER_INDEX.md`)
- Panel BOM gates (Gate-0 through Gate-5, see `PLANNING/PANEL_BOM/GATES_TRACKER.md`)
- Panel BOM execution deferred until approval (see `PLANNING/PANEL_BOM/MASTER_INDEX.md`)

**Execution Gates:**
- Gate-0: Panel Source Readiness
- Gate-1: Schema + History Readiness
- Gate-2: Controller/Route Wiring
- Gate-3: R1/S1/R2/S2 Sequence
- Gate-4: Rollup Verification
- Gate-5: Lookup Integrity

### Source-of-Truth Files

- `PLANNING/PANEL_BOM/MASTER_INDEX.md` — Panel BOM master index
- `PLANNING/PANEL_BOM/PANEL_BOM_PLANNING_TRACK.md` — Planning track (PB0-PB6)
- `PLANNING/PANEL_BOM/PANEL_BOM_TODO_TRACKER.md` — TODO tracker
- `PLANNING/PANEL_BOM/GATES_TRACKER.md` — Gates tracker (Gate-0 through Gate-5)
- `PLANNING/PANEL_BOM/CANONICAL_FLOW.md` — Canonical flow (frozen)
- `PLANNING/PANEL_BOM/COPY_RULES.md` — Copy rules (frozen)
- `PLANNING/PANEL_BOM/QUANTITY_CONTRACT.md` — Quantity contract (frozen)
- `PLANNING/FUNDAMENTS_CORRECTION/CANONICAL_BOM_HIERARCHY_v1.0.md` — Canonical hierarchy (Panel Master definition)
- `PLANNING/FUNDAMENTS_CORRECTION/MASTER_INSTANCE_MAPPING_v1.0.md` — Master→Instance mapping (L0: Panel Master → Proposal Panel)

### Key Rules

1. **Panel Master → Proposal Panel:** Proposal Panels are copies, not links from Panel Master
2. **Copy-never-link:** Proposal Panels never mutate Panel Master
3. **Panel copy:** Panel copy operations copy entire tree (feeders → BOMs → items)
4. **Ownership:** Proposal Panels belong to Proposal BOM Master (QuotationId)

### Known Gaps / Open Items

- Panel BOM planning complete (PB0-PB6, see `PLANNING/PANEL_BOM/MASTER_INDEX.md`)
- Panel BOM execution deferred until approval (see `PLANNING/PANEL_BOM/MASTER_INDEX.md`)
- See `PLANNING/PANEL_BOM/GATES_TRACKER.md` for gate status

---

## Summary: Layer Sequence and Dependencies

**Canonical Sequence:**
1. Category → Subcategory → Type(Item) → Attributes
2. Item/Component List (catalog)
3. Generic Item Master (L0/L1, ProductType=1)
4. Specific Item Master (L2, ProductType=2)
5. Master BOM (generic, L1)
6. Master BOM (specific) — NOT FOUND IN REPO (needs decision)
7. Proposal BOM + Proposal Sub-BOM (L2)
8. Feeder BOM (design-time: Feeder Master, runtime: Feeder Instance)
9. Panel BOM (design-time: Panel Master, runtime: Proposal Panel)

**Dependencies:**
- Generic Item Master (L0/L1) → Specific Item Master (L2) resolution
- Master BOM (L1) → Proposal BOM (L2) via copy with L1 → L2 resolution
- Feeder Master → Feeder Instance via copy operation
- Panel Master → Proposal Panel via copy operation
- Proposal BOM Master (QuotationId) owns all runtime entities

---

## Legacy Data Integrity & Remediation Strategy

### Problem Statement

The NSW Estimation Software has a fundamental legacy data integrity problem:
- Imported SQL with incorrect relational linking
- Item master polluted / hierarchy disturbed
- Thousands of items needing reconciliation
- Lookup pipeline failures due to broken references
- Inability to create new items correctly

This is a **non-negotiable fundamental blocker** that must be addressed before other fundamentals work can proceed reliably.

### Symptoms

1. **Orphan Items:** Items without valid Category/Subcategory/Item references
2. **Wrong Joins:** Incorrect relational linking between tables
3. **Missing Make/Series Mapping:** ProductType=2 items missing MakeId/SeriesId
4. **Hierarchy Disturbance:** Category → Subcategory → Item chain broken
5. **Lookup Pipeline Failures:** SKU search fails due to broken references

### Risk Impact

- **Lookup Pipeline Failures:** Category → Subcategory → Item → Product chain broken
- **Inability to Create New Items:** Cannot create items correctly due to polluted master
- **BOM Resolution Failures:** L1 → L2 resolution fails due to broken product references
- **Costing/Export Failures:** Incomplete product resolution causes calculation errors

### Remediation Sequencing

**Phase 1: Clean Masters**
1. Identify and isolate clean master data
2. Document current state (orphan items, broken references)
3. Create clean master baseline

**Phase 2: Mapping**
1. Map legacy data to clean master structure
2. Create reconciliation rules
3. Document mapping decisions

**Phase 3: Controlled Data Corrections**
1. Apply corrections in controlled batches
2. Verify each batch before proceeding
3. Capture evidence for each correction

**Phase 4: Verification**
1. Verify lookup pipeline integrity
2. Verify product resolution works
3. Verify BOM operations work with cleaned data

### Evidence Requirements

- **Before State:** SQL queries showing orphan items, broken references
- **Mapping Decisions:** Documented reconciliation rules
- **Correction Evidence:** SQL output for each correction batch
- **After State:** SQL queries verifying integrity restored

### Status

**NOT FOUND IN REPO:** Legacy data integrity remediation plan not found in repository.

**Recommendation:** Create dedicated remediation plan document before proceeding with other fundamentals work.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | 2025-01-XX | Initial master reference created from repository content |
| v1.1 | 2025-12-XX | Added badge legend, INFERRED tags, legacy data integrity section, date corrections |

---

**END OF MASTER REFERENCE**

