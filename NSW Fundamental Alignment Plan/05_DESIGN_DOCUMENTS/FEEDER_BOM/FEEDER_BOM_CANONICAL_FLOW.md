# Feeder BOM Canonical Execution Flow

**Version:** v1.0  
**Date:** 2025-01-XX  
**Status:** 🔒 LOCKED (Canonical Reference)

---

## Purpose

This document defines the **single, canonical execution path** for Feeder BOM operations. All implementations must follow this flow. Any deviation is out-of-scope.

---

## Canonical Flow

```
┌─────────────────┐
│   UI Request    │
│ (applyFeeder)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ QuotationV2Controller       │
│ (THIN LAYER)                │
│                             │
│ 1. Validate input           │
│ 2. Call BomEngine           │
│ 3. Return engine response   │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ BomEngine::copyFeederTree() │
│                             │
│ 1. Gate-0: Template check   │
│ 2. Filter: TemplateType='FEEDER' (MUST) │
│ 3. Guard: QuotationId validation (MUST) │
│ 4. Guard: Copy-never-link (MUST) │
│ 5. Detect/reuse feeder      │
│ 6. Clear-before-copy        │
│ 7. Copy items (new IDs)     │
│ 8. Record history           │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ BomHistoryService           │
│                             │
│ Record in bom_copy_history  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Verification Gates          │
│                             │
│ Gate-0: Template N > 0      │
│ R1/S1: First apply          │
│ R2/S2: Re-apply             │
│ A3: Status distribution     │
│ A4: Duplicate detection     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Phase-5 Freeze              │
│                             │
│ Gap register updates        │
│ Documentation freeze         │
└─────────────────────────────┘
```

---

## Component Responsibilities

### 1. UI Layer
- **Responsibility:** User interaction only
- **No business logic**
- **Sends request → Receives response**

### 2. QuotationV2Controller (THIN)
- **Responsibility:**
  - Input validation (required fields, types)
  - Call `BomEngine::copyFeederTree()`
  - Return engine response (no transformation)
- **MUST NOT:**
  - Create `QuotationSaleBom` directly
  - Create `QuotationSaleBomItem` directly
  - Perform business logic
  - Transform engine response

### 3. BomEngine::copyFeederTree()
- **Responsibility:**
  - Gate-0: Validate template has items (N > 0)
  - **Filter step (MUST):** Filter feeder templates by `TemplateType='FEEDER'` (fundamentals requirement)
  - **Guard step (MUST):** Validate QuotationId is provided and valid (fundamentals requirement)
  - **Guard step (MUST):** Enforce copy-never-link (reject any master mutation attempts) (fundamentals requirement)
  - Detect existing feeder (reuse if found)
  - Clear-before-copy (soft-delete existing items)
  - Copy items (new IDs, copy-never-link)
  - Record copy history
- **Returns:**
  ```php
  [
      'feeder_id' => int,
      'feeder_reused' => bool,
      'items_created' => int,
      'items_deleted' => int,
      'copy_history_id' => string,
      'id_mapping' => array,
  ]
  ```

### 4. BomHistoryService
- **Responsibility:**
  - Record copy operation in `bom_copy_history`
  - Capture source/target snapshots
  - Store ID mappings
- **Table:** `bom_copy_history`

### 5. Verification Gates
- **Gate-0:** Template must have N > 0 items
- **R1/S1:** First apply verification
- **R2/S2:** Re-apply verification
- **A3:** Status distribution query
- **A4:** Duplicate detection query

---

## Execution Rules

### ✅ ALLOWED
- Controller calls `BomEngine::copyFeederTree()`
- Engine performs all business logic
- History service records operations
- Verification queries run after execution

### ❌ FORBIDDEN
- Controller creates BOM/items directly
- Controller performs business logic
- Direct DB writes outside engine
- Skipping verification gates
- Modifying engine response in controller

---

## Input/Output Contract

### Input (Controller receives from UI)
```php
[
    'quotation_id' => int,
    'quotation_sale_id' => int,
    'template_id' => int,  // MasterBomId
    'feeder_name' => string,
    'qty' => float,  // Optional
]
```

### Output (Controller returns to UI)
```php
[
    'success' => bool,
    'message' => string,
    'feeder_id' => int,
    'template_id' => int,
    'feeder_reused' => bool,
    'deleted_count' => int,
    'inserted_count' => int,
]
```

**Note:** Controller maps engine response to UI format (field name mapping only, no logic).

---

## Verification Sequence

### After First Apply (R1)
1. Execute `applyFeederTemplate()` API
2. Capture `feeder_id` from response
3. Verify `feeder_reused: false`
4. Run A3 query → Verify Status=0: N items, Status=1: 0 items
5. Run A4 query → Verify 0 rows (no duplicates)
6. Check copy history written

### After Second Apply (R2 - Same Parameters)
1. Execute `applyFeederTemplate()` API with **same parameters**
2. Verify `feeder_reused: true`
3. Verify `feeder_id` matches first apply
4. Verify `deleted_count > 0` (clear-before-copy worked)
5. Run A3 query → Verify Status=0: N items (same), Status=1: N items (previous items soft-deleted)
6. Run A4 query → Verify 0 rows (no duplicates)
7. Check copy history updated

---

## Error Handling

### Gate-0 Failure (0-item template)
- **Action:** Throw exception
- **Message:** "Template must have at least 1 item"
- **Code:** BOM-GAP-013

### Template Not Found
- **Action:** Throw exception
- **Message:** "Master BOM (feeder template) not found: {id}"

### Database Transaction Failure
- **Action:** Rollback transaction
- **Log:** Error details
- **Return:** Error response to UI

---

## History Recording

Every `copyFeederTree()` operation **MUST** record:
- Source snapshot (Master BOM + items)
- Target snapshot (Proposal BOM + items)
- ID mappings (bom_mapping, item_mapping)
- Operation type: `COPY_FEEDER_TREE`
- User ID
- Timestamp

**Table:** `bom_copy_history`

---

## Alignment with Phase-1 → Phase-5

### Phase-1 (History Foundation)
- ✅ Uses `BomHistoryService`
- ✅ Records in `bom_copy_history`
- ✅ Captures snapshots

### Phase-2 (Copy Semantics + Idempotency)
- ✅ Copy-never-link (new IDs)
- ✅ Reuse existing feeder
- ✅ Clear-before-copy
- ✅ Idempotent re-apply

### Phase-4 (Lookup Integrity)
- ✅ Preserves lookup pipeline
- ✅ Items remain editable
- ✅ No orphaned references

### Phase-5 (Freeze & Audit)
- ✅ Verification gates
- ✅ Evidence collection
- ✅ Gap register updates

---

## Out-of-Scope

The following are **explicitly out-of-scope** for Feeder BOM:
- Direct DB writes in controller
- Master BOM modifications
- Item Master modifications
- Specific Item modifications
- Proposal BOM modifications (outside copy operation)
- Nested BOM handling (handled separately)
- Panel tree copy (handled separately)

---

## References

- `BomEngine.php` - Engine implementation
- `BomHistoryService.php` - History service
- `FEEDER_BOM_TODO_TRACKER.md` - Phase tracking
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` - Canonical rules

---

**END OF DOCUMENT**

