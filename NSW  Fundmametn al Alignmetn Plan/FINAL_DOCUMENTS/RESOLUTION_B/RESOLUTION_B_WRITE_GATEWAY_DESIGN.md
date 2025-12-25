# Resolution-B Write Gateway Design

**File:** docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md  
**Version:** v1.0_2025-12-19  
**Status:** 📋 DESIGN (No Implementation Yet)  
**Phase:** Resolution-B Analysis (Phase-4 Implementation Pending)

---

## Purpose

Design a centralized write gateway service that enforces all L2 (Specific Item) requirements for Proposal BOM writes. This document contains DESIGN ONLY (pseudocode). Implementation will occur in Phase-4.

---

## Design Objectives

1. **Single Point of Entry:** All Proposal BOM writes go through gateway
2. **Centralized Validation:** All L2 requirements enforced in one place
3. **Consistent Behavior:** Same validation rules across all write paths
4. **Audit Trail:** All writes logged with validation results
5. **Error Handling:** Explicit exceptions, no silent failures
6. **Transitional State Support:** Handles L1→L2 resolution workflows

---

## Service Structure

### Service Name
`ProposalBomItemWriter`

### Location
`app/Services/ProposalBomItemWriter.php`

### Dependencies
- `QuotationSaleBomItem` (Eloquent model)
- `Product` (Eloquent model)
- Validation service/logging

---

## Public Methods

### 1. createItem()

**Purpose:** Create a new Proposal BOM item with full L2 validation.

**Signature (Pseudocode):**
```php
/**
 * Create a new Proposal BOM item
 * 
 * @param array $data Item data (ProductId, MakeId, SeriesId, Qty, etc.)
 * @param array $options Options (allowTransitionalState, mergeMode, etc.)
 * @return QuotationSaleBomItem Created item
 * @throws ValidationException If validation fails
 */
public function createItem(array $data, array $options = []): QuotationSaleBomItem
```

**Validation Steps (Pseudocode):**
```
1. Extract and validate required fields:
   - QuotationSaleBomId (required)
   - ProductId (required)
   - Qty (required, > 0)

2. Load and validate Product:
   - Product must exist
   - IF allowTransitionalState option is FALSE (default):
     - Product.ProductType MUST be 2 (Specific)
     - Product.MakeId MUST match data['MakeId'] (if provided)
     - Product.SeriesId MUST match data['SeriesId'] (if provided)
   - IF allowTransitionalState option is TRUE:
     - Product.ProductType can be 1 (Generic) OR 2 (Specific)
     - Mark item as "pending resolution" (internal flag)

3. Validate MakeId and SeriesId:
   - IF Product.ProductType == 2:
     - MakeId MUST be > 0
     - SeriesId MUST be > 0 (unless product is explicitly exempted)
     - MakeId MUST match Product.MakeId
     - SeriesId MUST match Product.SeriesId
   - IF Product.ProductType == 1 AND allowTransitionalState:
     - MakeId can be 0 (intermediate state)
     - SeriesId can be 0 (intermediate state)
     - Item MUST be marked as "pending resolution"

4. Validate GenericId:
   - IF Product.ProductType == 2:
     - GenericId should be Product.GenericId (for traceability)

5. Execute create:
   - QuotationSaleBomItem::create([...])
   - Log write operation (who, when, what, validation result)

6. Return created item
```

**Example Usage (Pseudocode):**
```php
// Standard create (L2 only)
$item = $writer->createItem([
    'QuotationSaleBomId' => $bomId,
    'ProductId' => $specificProductId, // ProductType=2
    'MakeId' => $makeId, // > 0
    'SeriesId' => $seriesId, // > 0
    'Qty' => 10,
]);

// Transitional state (L1→L2 resolution)
$item = $writer->createItem([
    'QuotationSaleBomId' => $bomId,
    'ProductId' => $genericProductId, // ProductType=1
    'MakeId' => 0, // Will be resolved later
    'SeriesId' => 0, // Will be resolved later
    'Qty' => 10,
], [
    'allowTransitionalState' => true, // Explicit flag
]);
```

---

### 2. updateItem()

**Purpose:** Update an existing Proposal BOM item with validation.

**Signature (Pseudocode):**
```php
/**
 * Update an existing Proposal BOM item
 * 
 * @param int $itemId QuotationSaleBomItemId
 * @param array $data Update data
 * @return QuotationSaleBomItem Updated item
 * @throws ValidationException If validation fails
 * @throws NotFoundException If item not found
 */
public function updateItem(int $itemId, array $data): QuotationSaleBomItem
```

**Validation Steps (Pseudocode):**
```
1. Load existing item:
   - Item must exist
   - Item.Status must be 0 (active) - soft-deleted items cannot be updated

2. IF ProductId is being updated:
   - Apply same Product validation as createItem()
   - ProductType cannot change from 2 to 1 (downgrade forbidden)
   - ProductType can change from 1 to 2 (resolution allowed)

3. IF MakeId or SeriesId is being updated:
   - IF new Product.ProductType == 2:
     - MakeId MUST be > 0
     - SeriesId MUST be > 0
     - Must match Product.MakeId/SeriesId

4. Execute update:
   - $item->update($data)
   - Log update operation

5. Return updated item
```

---

### 3. createFromMasterBom()

**Purpose:** Create Proposal BOM items from Master BOM (L1→L2 resolution workflow).

**Signature (Pseudocode):**
```php
/**
 * Create Proposal BOM items by copying from Master BOM
 * 
 * @param int $quotationSaleBomId Target Proposal BOM ID
 * @param int $masterBomId Source Master BOM ID
 * @param array $options Options (clearExisting, allowTransitionalState)
 * @return array Created items
 * @throws ValidationException If validation fails
 */
public function createFromMasterBom(
    int $quotationSaleBomId,
    int $masterBomId,
    array $options = []
): array
```

**Workflow (Pseudocode):**
```
1. Load Master BOM and items:
   - Master BOM must exist
   - Load MasterBomItems (L1 items with Generic products)

2. IF clearExisting option is true (default):
   - Delete existing Proposal BOM items (soft delete: Status=1)
   - Prevents duplicate stacking

3. FOR EACH MasterBomItem:
   - Create Proposal BOM item:
     - ProductId = MasterBomItem.ProductId (Generic, ProductType=1)
     - MakeId = 0 (intermediate state)
     - SeriesId = 0 (intermediate state)
     - Mark as "pending resolution" (internal flag)
   - Use createItem() with allowTransitionalState=true

4. Log operation:
   - Source: Master BOM
   - Target: Proposal BOM
   - Items created: count
   - All items marked as "pending resolution"

5. Return created items
```

**Example Usage (Pseudocode):**
```php
// Copy from Master BOM (creates transitional state items)
$items = $writer->createFromMasterBom(
    $quotationSaleBomId,
    $masterBomId,
    [
        'clearExisting' => true, // Default: clear before copy
        'allowTransitionalState' => true, // Explicit flag
    ]
);

// Items are created with ProductType=1, MakeId=0, SeriesId=0
// User must resolve (select Make/Series) before finalization
```

---

### 4. createFromFeederTemplate()

**Purpose:** Create Proposal BOM items from Feeder template (similar to Master BOM).

**Signature (Pseudocode):**
```php
/**
 * Create Proposal BOM items by copying from Feeder template
 * 
 * @param int $quotationSaleBomId Target Proposal BOM ID
 * @param int $feederTemplateId Source Feeder template ID
 * @param array $options Options (clearExisting, allowTransitionalState)
 * @return array Created items
 * @throws ValidationException If validation fails
 */
public function createFromFeederTemplate(
    int $quotationSaleBomId,
    int $feederTemplateId,
    array $options = []
): array
```

**Workflow:** Similar to `createFromMasterBom()` (L1→L2 resolution workflow).

---

### 5. createFromProposalBom()

**Purpose:** Create Proposal BOM items by copying from another Proposal BOM (reuse/apply).

**Signature (Pseudocode):**
```php
/**
 * Create Proposal BOM items by copying from another Proposal BOM
 * 
 * @param int $targetQuotationSaleBomId Target Proposal BOM ID
 * @param int $sourceQuotationSaleBomId Source Proposal BOM ID
 * @param array $options Options (clearExisting, merge)
 * @return array Created items
 * @throws ValidationException If validation fails
 */
public function createFromProposalBom(
    int $targetQuotationSaleBomId,
    int $sourceQuotationSaleBomId,
    array $options = []
): array
```

**Workflow (Pseudocode):**
```
1. Load source Proposal BOM and items:
   - Source BOM must exist
   - Load QuotationSaleBomItems (should already be L2, ProductType=2)

2. Validate source items:
   - All items MUST be L2 (ProductType=2, MakeId>0, SeriesId>0)
   - If any item is not L2, throw exception

3. IF merge option is false (default):
   - Delete existing target BOM items (soft delete: Status=1)
   - Prevents duplicate stacking

4. IF merge option is true:
   - Check for duplicates (same ProductId + MakeId + SeriesId)
   - If duplicate found, skip or update (based on options)

5. FOR EACH source item:
   - Create target item:
     - Copy all fields (ProductId, MakeId, SeriesId, Qty, etc.)
     - ProductId must be ProductType=2 (already validated)
     - MakeId and SeriesId must be > 0 (already validated)
   - Use createItem() WITHOUT allowTransitionalState (source is already L2)

6. Log operation:
   - Source: Proposal BOM
   - Target: Proposal BOM
   - Items created: count
   - Merge mode: true/false

7. Return created items
```

**Example Usage (Pseudocode):**
```php
// Apply/reuse Proposal BOM (clear and copy)
$items = $writer->createFromProposalBom(
    $targetBomId,
    $sourceBomId,
    [
        'clearExisting' => true, // Default: clear before copy
        'merge' => false, // Default: no merge
    ]
);

// Apply/reuse with merge
$items = $writer->createFromProposalBom(
    $targetBomId,
    $sourceBomId,
    [
        'merge' => true, // Explicit merge flag
    ]
);
```

---

### 6. resolveItem()

**Purpose:** Resolve transitional state item to L2 (L1→L2 resolution completion).

**Signature (Pseudocode):**
```php
/**
 * Resolve transitional state item to L2 (complete L1→L2 resolution)
 * 
 * @param int $itemId QuotationSaleBomItemId
 * @param int $makeId Selected Make ID
 * @param int $seriesId Selected Series ID
 * @return QuotationSaleBomItem Resolved item
 * @throws ValidationException If validation fails
 * @throws NotFoundException If item not found
 */
public function resolveItem(int $itemId, int $makeId, int $seriesId): QuotationSaleBomItem
```

**Workflow (Pseudocode):**
```
1. Load existing item:
   - Item must exist
   - Item must be in transitional state (ProductType=1 OR MakeId=0 OR SeriesId=0)

2. Validate MakeId and SeriesId:
   - MakeId MUST be > 0
   - SeriesId MUST be > 0

3. Resolve to Specific product:
   - Find Specific product: Product::where('GenericId', $item->ProductId)
     ->where('MakeId', $makeId)
     ->where('SeriesId', $seriesId)
     ->where('ProductType', 2)
     ->first()
   - If not found, throw exception

4. Update item:
   - ProductId = resolved Specific product ID
   - MakeId = $makeId
   - SeriesId = $seriesId
   - Remove "pending resolution" flag (internal)

5. Log resolution:
   - Item ID
   - Generic ProductId → Specific ProductId
   - MakeId, SeriesId

6. Return resolved item
```

**Example Usage (Pseudocode):**
```php
// Resolve transitional item (user selects Make/Series)
$resolvedItem = $writer->resolveItem(
    $itemId,
    $makeId, // > 0
    $seriesId // > 0
);
// Item is now L2: ProductType=2, MakeId>0, SeriesId>0
```

---

## Validation Rules (Centralized)

### Rule 1: ProductType Validation
```
IF allowTransitionalState is FALSE (default):
    Product.ProductType MUST be 2 (Specific)

IF allowTransitionalState is TRUE:
    Product.ProductType can be 1 (Generic) OR 2 (Specific)
    Item MUST be marked as "pending resolution"
```

### Rule 2: MakeId Validation
```
IF Product.ProductType == 2:
    MakeId MUST be > 0
    MakeId MUST match Product.MakeId

IF Product.ProductType == 1 AND allowTransitionalState:
    MakeId can be 0 (intermediate state)
```

### Rule 3: SeriesId Validation
```
IF Product.ProductType == 2:
    SeriesId MUST be > 0 (unless product is explicitly exempted)
    SeriesId MUST match Product.SeriesId

IF Product.ProductType == 1 AND allowTransitionalState:
    SeriesId can be 0 (intermediate state)
```

### Rule 4: GenericId Traceability
```
IF Product.ProductType == 2:
    GenericId should be Product.GenericId (for traceability)
```

### Rule 5: Status Validation
```
Active items (Status=0) MUST satisfy all L2 requirements:
    - ProductType = 2
    - MakeId > 0
    - SeriesId > 0

Soft-deleted items (Status=1) are exempt from validation
```

---

## Error Handling

### Exception Types

**ValidationException:**
- Validation rule violated
- Missing required fields
- Invalid values (MakeId=0, ProductType=1, etc.)

**NotFoundException:**
- Item not found
- Product not found
- BOM not found

**StateException:**
- Invalid state transition (e.g., ProductType 2→1)
- Item not in expected state (e.g., resolving non-transitional item)

### Error Messages

Explicit error messages indicating:
- Which rule was violated
- What value was provided
- What value is required
- How to fix

Example:
```
"Proposal BOM items require Specific products (ProductType=2). 
Provided product has ProductType=1. 
Use allowTransitionalState option if creating intermediate state item."
```

---

## Logging and Audit Trail

All write operations log:
- **Who:** User ID (from auth context)
- **When:** Timestamp
- **What:** Operation type (create, update, resolve, copy, etc.)
- **Where:** Item ID(s), BOM ID(s)
- **Validation Result:** Passed/Failed, reason if failed
- **Source:** Master BOM, Feeder template, Proposal BOM, manual add, etc.

---

## Migration Strategy (Phase-4)

### Step 1: Create Service
- Implement `ProposalBomItemWriter` service with all methods
- Add unit tests

### Step 2: Migrate Write Paths
- Update `applyMasterBom()` to use `createFromMasterBom()`
- Update `applyFeederTemplate()` to use `createFromFeederTemplate()`
- Update `applyProposalBom()` to use `createFromProposalBom()`
- Update `addItem()` to use `createItem()`
- Update `updateMakeSeries()` to use `resolveItem()`
- Update import commands to use appropriate methods

### Step 3: Remove Raw DB Inserts
- Replace `DB::table('quotation_sale_bom_items')->insert()` with service methods

### Step 4: Validation
- All write paths must use gateway
- No direct `QuotationSaleBomItem::create()` calls outside service
- Audit script to verify no bypasses

---

## References

- `RESOLUTION_B_RULES.md` — L2 write enforcement rules
- `RESOLUTION_B_WRITE_PATHS.md` — Complete write path inventory
- `RESOLUTION_B_ILLEGAL_DEFAULTS.md` — Illegal default patterns
- `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Copy operations design
- `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — Business rules

