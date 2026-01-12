# Decision Capture Rules

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose

Define what qualifies as a "decision" during Phase 5 exploration and what information must be captured for each decision.

## What Qualifies as a Decision?

A decision is any change or choice that:

1. **Modifies canonical outputs:**
   - Changes to `NSW_SCHEMA_CANON_v1.0.md` (tables, fields, relationships, constraints)
   - Changes to `NSW_DATA_DICTIONARY_v1.0.md` (entities, rules, semantics)
   - Changes to governance documents in `00_GOVERNANCE/`

2. **Establishes or changes business rules:**
   - Validation guardrails (G1-G7)
   - CostHead resolution rules
   - Locking policies
   - Naming conventions
   - Module ownership assignments

3. **Diverges from baseline:**
   - Any choice to diverge from Fundamentals v2.0
   - Any rejection of legacy pattern
   - Any new pattern not in baseline

4. **Introduces new capabilities:**
   - New tables or modules
   - New features or functionality
   - New integration points

5. **Resolves ambiguity:**
   - Choices between multiple valid options
   - Scope decisions (what to include/exclude)
   - Implementation approach decisions

## What Does NOT Qualify as a Decision?

- **Documentation clarifications:** Adding examples, improving explanations, fixing typos
- **Formatting changes:** Reorganizing sections, improving readability
- **Reference updates:** Updating links, adding cross-references
- **Status updates:** Marking items complete, updating progress

**Note:** If unsure, err on the side of capturing it as a decision. Better to over-capture than under-capture.

---

## Required Fields for Each Decision

### Core Fields (Required)

| Field | Description | Example |
|-------|-------------|---------|
| **Decision ID** | Unique identifier (D-###) | D-008 |
| **Date** | Decision date (YYYY-MM-DD) | 2025-01-27 |
| **Decision** | Clear statement of what was decided | "Use both parent_line_id and metadata_json for multi-SKU linkage" |
| **Rationale** | Why this decision was made | "Provides both relational query capability and flexible metadata storage" |
| **Alternatives Considered** | Other options evaluated | "Option A: parent_line_id only, Option B: metadata_json only" |
| **Impact** | What this affects (modules, tables, rules) | "QUO module, quote_bom_items table, multi-SKU explosion logic" |
| **Status** | PENDING / APPROVED / SUPERSEDED | APPROVED |

### Alignment Fields (Required)

| Field | Description | Example |
|-------|-------------|---------|
| **Fundamentals Citation** | Reference to Fundamentals baseline | "MASTER_FUNDAMENTALS_v2.0.md Section 3.2" |
| **Alignment Status** | ALIGNED / DIVERGED / EXTENDED | ALIGNED |
| **Divergence Rationale** | If diverging, why? | (if ALIGNED, leave blank) |

### Traceability Fields (Required)

| Field | Description | Example |
|-------|-------------|---------|
| **Related Feature ID** | If from Feature Discovery Log | FD-003 |
| **Related Pending Input** | If from Pending Inputs Register | PI-001 |
| **Schema Impact** | Specific tables/fields changed | "quote_bom_items.parent_line_id, quote_bom_items.metadata_json" |
| **Dictionary Impact** | Specific dictionary sections changed | "NSW_DATA_DICTIONARY_v1.0.md Section 4.3.2" |

### Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Risk Assessment** | Potential risks or concerns | "Requires careful metadata structure design" |
| **Implementation Notes** | Notes for implementers | "Ensure both fields are populated for multi-SKU items" |
| **Review Date** | When to review this decision | 2025-02-15 |
| **Superseded By** | If superseded, link to new decision | D-012 |

---

## Decision Capture Process

### Step 1: Identify Decision

When making a change, ask:
- Does this modify canonical outputs?
- Does this establish or change a rule?
- Does this diverge from baseline?
- Does this introduce new capability?
- Does this resolve ambiguity?

If YES to any → This is a decision.

### Step 2: Create Decision Entry

1. Get next Decision ID from `PHASE_5_DECISIONS_REGISTER.md`
2. Fill in all required fields
3. Cite Fundamentals baseline (even if diverging)
4. Link to related Feature Discovery or Pending Input if applicable

### Step 3: Update Related Documents

1. Make the actual change (schema, dictionary, etc.)
2. Update Decision Register with new entry
3. Update Feature Discovery Log status if applicable
4. Update Pending Inputs Register status if applicable
5. Update traceability mapping if requirement impact

### Step 4: Commit with Reference

Commit message format:
```
Phase5: schema canon - <topic> (D-###)
Phase5: data dictionary - <topic> (D-###)
Phase5: governance - <topic> (D-###)
```

---

## Decision Status Lifecycle

```
NEW (discovered)
  ↓
PENDING (under evaluation)
  ↓
APPROVED (decision made, change implemented)
  ↓
SUPERSEDED (replaced by new decision)
```

---

## Examples

### Example 1: Schema Change Decision

**Decision ID:** D-008  
**Date:** 2025-01-27  
**Decision:** Add `import_batch_id` to `products` table for import governance  
**Rationale:** Enables tracking of which import batch created each product, supports auditability  
**Alternatives Considered:** Option A: No tracking (rejected - no auditability), Option B: Separate audit table only (rejected - less efficient queries)  
**Impact:** CIM module, `products` table, import process  
**Status:** APPROVED  
**Fundamentals Citation:** MASTER_FUNDAMENTALS_v2.0.md Section 5.1 (Import Expectations)  
**Alignment Status:** ALIGNED  
**Related Feature ID:** FD-001  
**Schema Impact:** `products.import_batch_id` (FK to `import_batches.id`)

### Example 2: Divergence Decision

**Decision ID:** D-009  
**Date:** 2025-01-27  
**Decision:** Use `customer_name` (text) + optional `customer_id` (FK) instead of mandatory `customer_id` only  
**Rationale:** Supports ad-hoc quotations without requiring customer master data setup, aligns with MVP scope  
**Alternatives Considered:** Option A: Mandatory customer_id only (rejected - too restrictive for MVP), Option B: customer_name only (rejected - loses normalization benefits)  
**Impact:** QUO module, `quotations` table, customer management  
**Status:** APPROVED  
**Fundamentals Citation:** (No direct citation - this is an MVP scope decision)  
**Alignment Status:** EXTENDED  
**Divergence Rationale:** Fundamentals assume customer master exists, but MVP allows ad-hoc quotations  
**Schema Impact:** `quotations.customer_name` (text, required), `quotations.customer_id` (FK, nullable)

---

## Change Log

- **v1.0 (2025-01-27):** Initial decision capture rules created

---

**END OF DECISION CAPTURE RULES**

