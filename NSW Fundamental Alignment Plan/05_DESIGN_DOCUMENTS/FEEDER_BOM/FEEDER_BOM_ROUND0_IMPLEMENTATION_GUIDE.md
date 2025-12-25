# Feeder BOM Round-0 Implementation Guide

**File:** docs/FEEDER_BOM/FEEDER_BOM_ROUND0_IMPLEMENTATION_GUIDE.md  
**Version:** v1.1_2025-12-19  
**Status:** ⏳ PENDING IMPLEMENTATION (Approved, Not Executed)  
**Phase:** Feeder BOM Round-0

**⚠️ Implementation Status:**
- Design-approved, code-change identified, execution intentionally deferred
- No live database changes have been executed
- Implementation will occur only when explicitly authorized to "Start Feeder BOM execution"

---

## Purpose

This document provides the exact implementation steps for Feeder BOM Round-0, focusing on `applyFeederTemplate()` method in `QuotationV2Controller`. This implementation aligns with PB-GAP-004 semantics (clear-before-copy + writer-only) and follows NEPL_CANONICAL_RULES.md.

---

## Step 0 — Governance Pre-Check ✅

**Status:** ✅ PASSED

```bash
./scripts/governance/validate_phase4_gates.sh
```

**Result:** All critical gates passed (0 violations, 0 warnings)

---

## Step 1 — Round-0 Acceptance Contract

### Acceptance Criteria

1. ✅ Creates Level=0 + ParentBomId=NULL feeder node
2. ✅ Copies template items only into that feeder's QuotationSaleBomId
3. ✅ Items created via ProposalBomItemWriter (no raw inserts)
4. ✅ No duplicate stacking on repeated apply:
   - After apply #1 and apply #2, run A3/A4 (quick validation)
   - Must show no duplicates in Status=0 set
5. ✅ If items are generic/transitional (allowed), ensure finalization/export is blocked until resolved (ensureResolved())

---

## Step 2 — Implementation: applyFeederTemplate()

### ⚠️ CRITICAL CORRECTIONS

1. **Re-Apply to Same Feeder:** `applyFeederTemplate()` currently creates a NEW feeder each time. For clear-before-copy to work, we must **reuse existing feeders** when re-applying the same template.

2. **Writer Loop is Valid:** The code uses `$writer->create([...])` in a loop (not `createFromFeederTemplate()`). This is valid as long as writes go through the writer gateway.

### Current State

- `applyFeederTemplate()` creates a new feeder node every time
- Items are copied via `$writer->create([...])` in a loop (valid implementation)
- **MISSING:** Re-apply to same feeder logic
- **MISSING:** Clear-before-copy semantics (soft delete Status=1 before inserting)

### Required Changes

**File:** `app/Http/Controllers/QuotationV2Controller.php`  
**Method:** `applyFeederTemplate()`

#### Change 1: Re-Apply to Same Feeder (CRITICAL)

**Before creating a new feeder, detect if one already exists:**

```php
// Try to find existing feeder with same characteristics
$existingFeeder = QuotationSaleBom::where('QuotationId', $quotationId)
    ->where('QuotationSaleId', $quotationSaleId)
    ->where('MasterBomId', $templateId)
    ->where('MasterBomName', $feederName) // Adjust field name as needed
    ->where('Level', 0)
    ->whereNull('ParentBomId')
    ->where('Status', 0)
    ->first();

if ($existingFeeder) {
    // Reuse existing feeder
    $feederId = $existingFeeder->QuotationSaleBomId;
    $feederReused = true;
} else {
    // Create new feeder (existing logic)
    $feeder = QuotationSaleBom::create([...]);
    $feederId = $feeder->QuotationSaleBomId;
    $feederReused = false;
}
```

#### Change 2: Add Clear-Before-Copy Logic

**Only when reusing existing feeder, clear items before copying:**

```php
$deletedCount = 0;
if ($feederReused) {
    // Clear existing items (soft delete: Status=1) before copying
    // This prevents duplicate stacking on repeated apply
    $deletedCount = QuotationSaleBomItem::where('QuotationSaleBomId', $feederId)
        ->where('Status', 0)
        ->update(['Status' => 1]);
    
    \Log::info('Feeder Template Apply: Cleared existing items', [
        'feeder_id' => $feederId,
        'template_id' => $templateId,
        'deleted_count' => $deletedCount,
    ]);
}
```

**Placement:** This should be executed **BEFORE** the writer loop that copies template items.

#### Change 3: Copy Template Items (Writer Loop)

**The existing writer loop is valid. Ensure it uses `allowTransitionalState => true`:**

```php
$writer = app(ProposalBomItemWriter::class);
$createdItems = [];

foreach ($templateItems as $templateItem) {
    $item = $writer->create([
        'QuotationSaleBomId' => $feederId,
        'ProductId' => $templateItem->ProductId, // May be generic (ProductType=1)
        'MakeId' => 0, // Transitional state
        'SeriesId' => 0, // Transitional state
        'Qty' => $templateItem->Qty,
        // ... other fields ...
    ], [
        'allowTransitionalState' => true, // Allow generic items (L1→L2 resolution)
    ]);
    
    $createdItems[] = $item;
}
```

#### Change 3: Add Audit Logging

**After the copy operation, add comprehensive logging:**

```php
\Log::info('Feeder Template Apply: Completed', [
    'feeder_id' => $feederId,
    'template_id' => $templateId,
    'rows_soft_deleted' => $deletedCount,
    'rows_inserted' => count($createdItems),
    'items_created' => array_map(function($item) {
        return [
            'id' => $item->QuotationSaleBomItemId,
            'product_id' => $item->ProductId,
            'make_id' => $item->MakeId,
            'series_id' => $item->SeriesId,
        ];
    }, $createdItems),
]);
```

### Complete Method Structure (Pseudocode)

```php
public function applyFeederTemplate(Request $request)
{
    // 1. Validate input (feederId, templateId)
    $feederId = $request->input('feeder_id');
    $templateId = $request->input('template_id');
    
    // 2. Verify feeder exists and is Level=0, ParentBomId=NULL
    $feeder = QuotationSaleBom::findOrFail($feederId);
    if ($feeder->Level != 0 || $feeder->ParentBomId !== null) {
        throw new ValidationException('Feeder must be Level=0 with ParentBomId=NULL');
    }
    
    // 3. CLEAR-BEFORE-COPY: Soft delete existing items
    $deletedCount = QuotationSaleBomItem::where('QuotationSaleBomId', $feederId)
        ->where('Status', 0)
        ->update(['Status' => 1]);
    
    \Log::info('Feeder Template Apply: Cleared existing items', [
        'feeder_id' => $feederId,
        'template_id' => $templateId,
        'deleted_count' => $deletedCount,
    ]);
    
    // 4. Copy template items via gateway (copy-never-link)
    $createdItems = ProposalBomItemWriter::createFromFeederTemplate(
        $feederId,
        $templateId,
        [
            'clearExisting' => false, // Already cleared above
            'allowTransitionalState' => true, // Allow generic items (L1→L2 resolution)
        ]
    );
    
    // 5. Audit logging
    \Log::info('Feeder Template Apply: Completed', [
        'feeder_id' => $feederId,
        'template_id' => $templateId,
        'rows_soft_deleted' => $deletedCount,
        'rows_inserted' => count($createdItems),
    ]);
    
    // 6. Return response
    return response()->json([
        'success' => true,
        'feeder_id' => $feederId,
        'template_id' => $templateId,
        'deleted_count' => $deletedCount,
        'inserted_count' => count($createdItems),
    ]);
}
```

---

## Step 3 — In-Work Validation: A3/A4 Queries

### A3: Status Distribution Check

**Purpose:** Verify status distribution after apply operation (should show soft-deleted items as Status=1, new items as Status=0)

**Query:**
```sql
-- A3: Status distribution for feeder after apply
-- Replace {{FEEDER_ID}} with actual feeder QuotationSaleBomId

SELECT 
    Status,
    COUNT(*) AS item_count,
    MIN(created_at) AS earliest_created,
    MAX(created_at) AS latest_created
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = {{FEEDER_ID}}
GROUP BY Status
ORDER BY Status;
```

**Expected Result:**
- Status=0: Count of newly inserted items (should match rows_inserted from audit log)
- Status=1: Count of soft-deleted items (should match rows_soft_deleted from audit log)
- After second apply on same feeder: Status=1 count should increase, Status=0 count should remain same (no duplicates)

### A4: Duplicate Detection Check

**Purpose:** Verify no duplicate items in Status=0 set (same ProductId + MakeId + SeriesId combination)

**Query:**
```sql
-- A4: Duplicate detection in Status=0 set
-- Replace {{FEEDER_ID}} with actual feeder QuotationSaleBomId

SELECT 
    ProductId,
    MakeId,
    SeriesId,
    COUNT(*) AS duplicate_count,
    GROUP_CONCAT(QuotationSaleBomItemId ORDER BY QuotationSaleBomItemId) AS item_ids
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = {{FEEDER_ID}}
  AND Status = 0
GROUP BY ProductId, MakeId, SeriesId
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, ProductId;
```

**Expected Result:**
- **After first apply:** Should return 0 rows (no duplicates)
- **After second apply (same feeder):** Should return 0 rows (clear-before-copy prevents duplicates)

**Stop Condition:**
- If A4 returns any rows → **STOP** and run full A3-A6 verification pack immediately

---

## Step 4 — Validation Workflow

### After Each Apply Operation

1. **Run A3 Query:**
   - Verify status distribution is as expected
   - Check that Status=0 count matches inserted count
   - Check that Status=1 count includes previously active items

2. **Run A4 Query:**
   - Verify no duplicates in Status=0 set
   - If duplicates found → **STOP** and escalate

3. **Compare with Audit Log:**
   - Verify `rows_soft_deleted` matches Status=1 count (accounting for previous soft-deletes)
   - Verify `rows_inserted` matches Status=0 count

### After Two Applies (Same Feeder)

1. **First Apply:**
   - Run A3/A4
   - Record: Status=0 count = N1, Status=1 count = M1

2. **Second Apply (same feeder):**
   - Run A3/A4
   - Expected: Status=0 count = N1 (same, no duplicates)
   - Expected: Status=1 count = M1 + N1 (previous active items now soft-deleted)
   - Expected: A4 returns 0 rows (no duplicates)

---

## Step 5 — Rules Compliance

### NEPL_CANONICAL_RULES.md Compliance

✅ **Copy-Never-Link (Section 3.4):**
- Clear-before-copy prevents duplicate stacking
- Items created via `ProposalBomItemWriter` (no raw inserts)
- New independent rows created (no linking)

✅ **Write Gateway Enforcement (Section 3.2):**
- All writes go through `ProposalBomItemWriter::createFromFeederTemplate()`
- No direct `QuotationSaleBomItem::create()` calls
- No raw DB inserts

✅ **Transitional State Rules (Section 4):**
- `allowTransitionalState => true` allows generic items during copy
- `ensureResolved()` must be called before finalization/export
- Generic items (ProductType=1) acceptable as intermediate state only

✅ **Soft Delete (Section 3.4):**
- Clear operation uses soft delete (Status=1)
- No hard deletes

---

## Step 6 — Testing Checklist

### Pre-Implementation
- [ ] Governance pre-check passed
- [ ] Current `applyFeederTemplate()` implementation reviewed
- [ ] `ProposalBomItemWriter::createFromFeederTemplate()` implementation reviewed

### Implementation
- [ ] Clear-before-copy logic added (soft delete Status=1)
- [ ] Audit logging added (target feeder id, template id, rows soft-deleted, rows inserted)
- [ ] `createFromFeederTemplate()` call updated with correct options
- [ ] No raw DB inserts introduced
- [ ] No direct `QuotationSaleBomItem::create()` calls

### Post-Implementation Validation
- [ ] First apply: Run A3/A4, verify no duplicates
- [ ] Second apply (same feeder): Run A3/A4, verify no duplicates
- [ ] Audit log matches A3 status distribution
- [ ] A4 returns 0 rows (no duplicates)

---

## Step 7 — A3/A4 SQL Queries (Ready to Use)

### A3: Status Distribution (Feeder Template Apply)

```sql
-- A3: Status distribution for feeder after apply
-- Usage: Replace {{FEEDER_ID}} with actual feeder QuotationSaleBomId
-- Run after each applyFeederTemplate() call

SELECT 
    Status,
    COUNT(*) AS item_count,
    MIN(created_at) AS earliest_created,
    MAX(created_at) AS latest_created,
    MIN(updated_at) AS earliest_updated,
    MAX(updated_at) AS latest_updated
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = {{FEEDER_ID}}
GROUP BY Status
ORDER BY Status;
```

### A4: Duplicate Detection (Feeder Template Apply)

```sql
-- A4: Duplicate detection in Status=0 set
-- Usage: Replace {{FEEDER_ID}} with actual feeder QuotationSaleBomId
-- Run after each applyFeederTemplate() call
-- Expected: 0 rows (no duplicates)

SELECT 
    ProductId,
    MakeId,
    SeriesId,
    COUNT(*) AS duplicate_count,
    GROUP_CONCAT(QuotationSaleBomItemId ORDER BY QuotationSaleBomItemId) AS item_ids,
    GROUP_CONCAT(created_at ORDER BY QuotationSaleBomItemId) AS created_times
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = {{FEEDER_ID}}
  AND Status = 0
GROUP BY ProductId, MakeId, SeriesId
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, ProductId;
```

### A3/A4 Combined (Quick Check)

```sql
-- Combined A3/A4 check for quick validation
-- Usage: Replace {{FEEDER_ID}} with actual feeder QuotationSaleBomId

-- A3: Status distribution
SELECT 
    'A3_STATUS_DIST' AS check_type,
    Status,
    COUNT(*) AS item_count
FROM quotation_sale_bom_items
WHERE QuotationSaleBomId = {{FEEDER_ID}}
GROUP BY Status

UNION ALL

-- A4: Duplicate count
SELECT 
    'A4_DUPLICATES' AS check_type,
    -1 AS Status,  -- Placeholder
    COUNT(*) AS item_count
FROM (
    SELECT 
        ProductId,
        MakeId,
        SeriesId
    FROM quotation_sale_bom_items
    WHERE QuotationSaleBomId = {{FEEDER_ID}}
      AND Status = 0
    GROUP BY ProductId, MakeId, SeriesId
    HAVING COUNT(*) > 1
) AS duplicates;
```

---

## Step 8 — Expected Outputs

### After First Apply

**A3 Output:**
```
Status | item_count
-------|-----------
   0   |     N1    (newly inserted items)
   1   |     M1    (previously soft-deleted, if any)
```

**A4 Output:**
```
(0 rows) - No duplicates
```

**Audit Log:**
```
Feeder Template Apply: Completed
- feeder_id: 123
- template_id: 456
- rows_soft_deleted: M1
- rows_inserted: N1
```

### After Second Apply (Same Feeder)

**A3 Output:**
```
Status | item_count
-------|-----------
   0   |     N1    (same count, no duplicates)
   1   |  M1 + N1  (previous active items now soft-deleted)
```

**A4 Output:**
```
(0 rows) - No duplicates (clear-before-copy worked)
```

**Audit Log:**
```
Feeder Template Apply: Completed
- feeder_id: 123
- template_id: 456
- rows_soft_deleted: N1 (items from first apply)
- rows_inserted: N1 (new items from second apply)
```

---

## Step 9 — Stop Conditions

### If A4 Returns Duplicates

**Immediate Actions:**
1. **STOP** all Feeder BOM work
2. Run full A3-A6 verification pack on affected feeder
3. Report findings with complete A3-A6 output
4. Review clear-before-copy implementation
5. Fix root cause before proceeding

### If Status Distribution Unexpected

**Check:**
- Audit log matches A3 counts
- Clear operation executed before copy
- No merge mode accidentally enabled
- No concurrent applies on same feeder

---

## Step 10 — References

### Canonical Rules
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md`
  - Section 3.2: Write Gateway Enforcement
  - Section 3.4: Reuse/Apply Must CLEAR or MERGE Explicitly
  - Section 4: Transitional State Rules

### Design Documents
- `docs/RESOLUTION_B/RESOLUTION_B_WRITE_GATEWAY_DESIGN.md`
  - Section 4: `createFromFeederTemplate()` design
- `docs/RESOLUTION_B/RESOLUTION_B_SUMMARY.md`
  - Section: applyFeederTemplate() migration status

### Gap Register
- `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/PB_GAP_004_INSTANCE_ISOLATION_VERIFICATION_v1.0_2025-12-19.md`
  - Section 8: In-Work Validation Instructions (A3/A4)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0_2025-12-19 | 2025-12-19 | Initial Feeder BOM Round-0 implementation guide created with clear-before-copy semantics, A3/A4 validation queries, and complete workflow |

---

**END OF DOCUMENT**

