# CostHead Rules

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Purpose:** Define CostHead entity, precedence order, and mapping rules for costing engine

---

## Purpose

This document defines the CostHead system for categorizing costs into buckets (MATERIAL, LABOUR, OTHER) for costing engine calculations. CostHead determines how costs are grouped and reported in cost summaries.

---

## CostHead Entity Definition

### Entity: CostHead

**Semantic:** Categorizes costs into buckets for costing engine calculations.

**Examples:**
- `OEM_MATERIAL` - Original Equipment Manufacturer materials
- `NEPL_BUS` - NEPL busbar materials
- `NEPL_FAB` - NEPL fabrication materials
- `LABOUR` - Labor costs
- `OVERHEAD` - Overhead costs
- `OTHER` - Other miscellaneous costs

**Category Types:**
- `MATERIAL` - Material costs (OEM_MATERIAL, NEPL_BUS, NEPL_FAB, etc.)
- `LABOUR` - Labor costs (LABOUR, etc.)
- `OTHER` - Other costs (OVERHEAD, OTHER, etc.)

**Business Rule:** Required for costing engine calculations. Every costable item must have a CostHead assigned.

---

## Precedence Order (Resolution Logic)

### Explicit Precedence Order

CostHead is resolved using the following precedence order (highest to lowest):

1. **Item Override** (Highest Priority)
   - `quote_bom_items.cost_head_id` - Direct override at line-item level
   - If set, this value is used (overrides all defaults)

2. **Product Default** (Medium Priority)
   - `products.cost_head_id` - Default CostHead for the product
   - Used if item override is not set
   - **Decision:** Product default is **OPTIONAL** in MVP (can be added later)

3. **System Default** (Lowest Priority)
   - System-wide default CostHead
   - Used if neither item override nor product default is set
   - Typically `OTHER` or a configurable system default

### Resolution Algorithm

```php
function resolveCostHead(QuotationSaleBomItem $item): CostHead
{
    // 1. Check item override (highest priority)
    if ($item->cost_head_id !== null) {
        return CostHead::find($item->cost_head_id);
    }
    
    // 2. Check product default (medium priority)
    $product = $item->product;
    if ($product && $product->cost_head_id !== null) {
        return CostHead::find($product->cost_head_id);
    }
    
    // 3. Use system default (lowest priority)
    return CostHead::getSystemDefault(); // e.g., 'OTHER'
}
```

### Precedence Examples

**Example 1: Item Override**
```
Item: quote_bom_items.id = 123
Item cost_head_id: 5 (LABOUR)  ← Used (highest priority)
Product cost_head_id: 2 (OEM_MATERIAL)  ← Ignored
System default: 7 (OTHER)  ← Ignored
Result: LABOUR
```

**Example 2: Product Default**
```
Item: quote_bom_items.id = 456
Item cost_head_id: NULL  ← Not set
Product cost_head_id: 2 (OEM_MATERIAL)  ← Used (medium priority)
System default: 7 (OTHER)  ← Ignored
Result: OEM_MATERIAL
```

**Example 3: System Default**
```
Item: quote_bom_items.id = 789
Item cost_head_id: NULL  ← Not set
Product cost_head_id: NULL  ← Not set
System default: 7 (OTHER)  ← Used (lowest priority)
Result: OTHER
```

---

## Mapping Guidance

### How Defaults Are Assigned

#### Product Default Assignment

**When:** During product creation or update.

**Process:**
1. User creates/edits product in Component/Item Master
2. User selects default CostHead for product
3. System stores `products.cost_head_id`
4. All future BOM items using this product inherit this CostHead (unless overridden)

**Recommendation:**
- Assign CostHead based on product category/type
- MATERIAL products → OEM_MATERIAL or NEPL_BUS or NEPL_FAB
- LABOUR services → LABOUR
- Generic products → System default or prompt user

**MVP Status:** Product default is **OPTIONAL** in MVP. Can be added in future phase.

#### Item Override Assignment

**When:** During quotation BOM item creation or update.

**Process:**
1. User creates/edits BOM item in quotation
2. User can override CostHead for this specific item
3. System stores `quote_bom_items.cost_head_id`
4. This override takes precedence over product default

**Use Cases:**
- Special material handling (e.g., custom fabrication)
- Labor cost override for specific items
- Cost categorization adjustment per quotation

#### System Default Configuration

**When:** System initialization or configuration update.

**Process:**
1. Admin configures system-wide default CostHead
2. System stores default CostHead ID in configuration
3. All items without override or product default use this

**Default Value:** Typically `OTHER` or first CostHead in system.

---

## What Happens If Missing

### Missing CostHead Scenario

**Scenario:** Item has no CostHead assigned (all three levels are NULL).

**Resolution:**
1. System uses **system default** CostHead
2. Warning logged (optional): "Item has no CostHead, using system default"
3. Item is still costable (not blocked)

**Alternative (Stricter):**
- Reject item creation if CostHead cannot be resolved
- Require user to explicitly assign CostHead
- **Decision:** Use system default (lenient) for MVP

### Missing CostHead in Cost Summary

**Scenario:** Cost summary calculation encounters item with missing CostHead.

**Resolution:**
1. Use system default for calculation
2. Group under system default CostHead in summary
3. Log warning for audit

---

## Database Schema

### Table: `cost_heads`

```sql
CREATE TABLE cost_heads (
    id BIGINT UNSIGNED PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,  -- e.g., 'OEM_MATERIAL'
    name VARCHAR(255) NOT NULL,  -- e.g., 'OEM Material'
    category ENUM('MATERIAL', 'LABOUR', 'OTHER') NOT NULL,
    priority INTEGER DEFAULT 0,  -- For mapping priority when multiple apply
    description TEXT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Indexes:**
- Index on `code` (unique lookup)
- Index on `category` (filtering by category)

### Table: `quote_bom_items`

**Add Column:**
```sql
cost_head_id BIGINT UNSIGNED NULL,
FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id)
```

**Index:**
- Index on `cost_head_id` (for cost summary grouping)

### Table: `products` (Optional - Future)

**Add Column (Optional in MVP):**
```sql
cost_head_id BIGINT UNSIGNED NULL,
FOREIGN KEY (cost_head_id) REFERENCES cost_heads(id)
```

**Index:**
- Index on `cost_head_id` (for product default lookup)

**MVP Decision:** Product default is **OPTIONAL** in MVP. Can be added in future phase.

---

## Business Rules

### Rule 1: Precedence Order is Fixed

**Rule:** Precedence order (Item → Product → System) is fixed and cannot be changed.

**Enforcement:**
- Resolution algorithm enforces precedence
- No configuration to change precedence order
- Precedence is documented and canonical

### Rule 2: Item Override Takes Highest Priority

**Rule:** If item has `cost_head_id` set, it always takes precedence.

**Enforcement:**
- Resolution algorithm checks item override first
- Product default and system default are ignored if item override exists

### Rule 3: System Default is Fallback

**Rule:** System default is used when no other CostHead is available.

**Enforcement:**
- Resolution algorithm uses system default as last resort
- System default must exist (created during system initialization)
- Missing system default is system error (not user error)

### Rule 4: CostHead Must Be Active

**Rule:** Only active CostHeads can be assigned.

**Enforcement:**
- Validation checks `is_active = true` before assignment
- Inactive CostHeads are filtered from selection lists
- Existing assignments to inactive CostHeads remain valid (historical data)

---

## Use Cases

### Use Case 1: Standard Material Costing

**Scenario:** Standard OEM material item with product default.

**Steps:**
1. Product has `cost_head_id = 2` (OEM_MATERIAL)
2. User adds item to quotation BOM
3. System resolves CostHead: Product default → OEM_MATERIAL
4. Item is grouped under MATERIAL category in cost summary

### Use Case 2: Custom Material Override

**Scenario:** User wants to override CostHead for specific item.

**Steps:**
1. Product has `cost_head_id = 2` (OEM_MATERIAL)
2. User adds item to quotation BOM
3. User overrides CostHead to `cost_head_id = 3` (NEPL_FAB)
4. System resolves CostHead: Item override → NEPL_FAB
5. Item is grouped under MATERIAL category (NEPL_FAB) in cost summary

### Use Case 3: New Product Without Default

**Scenario:** New product without CostHead default.

**Steps:**
1. Product has `cost_head_id = NULL` (no default)
2. User adds item to quotation BOM
3. User does not override CostHead
4. System resolves CostHead: System default → OTHER
5. Item is grouped under OTHER category in cost summary

---

## Cost Summary Grouping

### Cost Summary by CostHead

**Grouping Logic:**
- Group all items by resolved CostHead
- Sum amounts within each CostHead group
- Display summary by CostHead category (MATERIAL, LABOUR, OTHER)

**Example Summary:**
```
MATERIAL:
  - OEM_MATERIAL: $50,000
  - NEPL_BUS: $20,000
  - NEPL_FAB: $15,000
  Total MATERIAL: $85,000

LABOUR:
  - LABOUR: $30,000
  Total LABOUR: $30,000

OTHER:
  - OVERHEAD: $10,000
  - OTHER: $5,000
  Total OTHER: $15,000

Grand Total: $130,000
```

---

## References

- `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` - Section 1.3 (CostHead Entity Definition)
- `SPEC_5_FREEZE_GATE_CHECKLIST.md` - Section 3 (CostHead System)
- Costing engine implementation

---

## Change Log

### v1.0 (2025-01-27) - FROZEN

- Initial CostHead rules with precedence order and mapping guidance

**Freeze Date:** 2025-01-27  
**Freeze Reason:** Frozen after Phase-5 Senate review. All Step-1 requirements verified and approved.

---

**Status:** FROZEN  
**Frozen:** 2025-01-27 after Phase-5 Senate review

