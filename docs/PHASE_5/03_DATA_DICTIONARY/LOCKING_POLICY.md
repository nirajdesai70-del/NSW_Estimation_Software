# Locking Policy

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** FROZEN  
**Owner:** Phase 5 Senate  
**Purpose:** Define locking semantics for deletion protection and workflow control

---

## Purpose

This document defines the locking policy for NSW quotation system. Locking prevents deletion and modification of critical data at various hierarchy levels. This is an MVP policy focused on line-item level locking, with optional future extensions.

---

## Scope Declaration

### MVP Scope: Line-Item Level Locking

**Decision:** Locking applies at the **line-item level** (`quote_bom_items.is_locked`) for MVP.

**Rationale:**
- Simplest implementation
- Sufficient for MVP deletion protection
- Can be extended later if needed

**Tables with `is_locked` field:**
- `quote_bom_items` (line items) - **MVP REQUIRED**

**Tables explicitly excluded from MVP:**
- `quotations` - No locking at quotation level in MVP
- `quote_panels` - No locking at panel level in MVP
- `quote_boms` - No locking at BOM level in MVP

**Future Extension Option:**
- Locking can be extended to panel/BOM/quotation levels in future phases
- Extension requires explicit decision and policy update

---

## What "Locked" Prevents

### Deletion Protection

**When `is_locked = true`:**
- Item cannot be deleted (soft delete prevented)
- DeletionPolicyService checks `is_locked` before allowing deletion
- Attempted deletion returns error: "Item is locked and cannot be deleted"

**When `is_locked = false`:**
- Item can be deleted normally (subject to other business rules)
- Soft delete allowed (Status = 1)

### Edit Protection (Optional - Future)

**Current MVP:** Locking does NOT prevent edits in MVP.

**Future Consideration:**
- Locking may prevent edits in future phases
- Locking may prevent reprice operations
- Locking may prevent resolve operations
- These are **NOT in MVP scope**

---

## Lock State Transitions

### Who Can Lock

**Locking Authority:**
- **Estimator:** Can lock items (default permission)
- **Reviewer:** Can lock items (default permission)
- **Admin:** Can lock/unlock items (full control)
- **Viewer:** Cannot lock items (read-only)

**Locking Trigger:**
- Manual lock by user (UI action: "Lock Item")
- Automatic lock (future: on approval, on finalization)
- System lock (future: on export, on production)

### Who Can Unlock

**Unlocking Authority:**
- **Admin:** Can unlock any item (full control)
- **Reviewer:** Can unlock items they locked (self-unlock)
- **Estimator:** Cannot unlock (locked items require review)
- **Viewer:** Cannot unlock (read-only)

**Unlocking Trigger:**
- Manual unlock by authorized user (UI action: "Unlock Item")
- System unlock (future: on revision, on reset)

### Lock State Machine

```
[Unlocked] (is_locked = false)
    │
    │ User locks item
    │ (requires permission)
    │
    ▼
[Locked] (is_locked = true)
    │
    │ Admin/Reviewer unlocks
    │ (requires permission)
    │
    ▼
[Unlocked] (is_locked = false)
```

**State Transitions:**
- `false → true`: Lock operation (requires lock permission)
- `true → false`: Unlock operation (requires unlock permission)
- `true → true`: No-op (already locked)
- `false → false`: No-op (already unlocked)

---

## Implementation Details

### Database Schema

**Table: `quote_bom_items`**

```sql
is_locked BOOLEAN DEFAULT false NOT NULL
```

**Index:**
- Index on `is_locked` for filtering locked items
- Composite index: `(quotation_id, is_locked)` for quotation-level queries

### Service Layer

**Service: `DeletionPolicyService`**

**Method: `canDelete(QuotationSaleBomItem $item): bool`**

```php
public function canDelete(QuotationSaleBomItem $item): bool
{
    // G1: Check if item is locked
    if ($item->is_locked) {
        return false; // Cannot delete locked item
    }
    
    // Other deletion rules...
    return true;
}
```

**Error Response:**
```json
{
    "success": false,
    "message": "Item is locked and cannot be deleted",
    "item_id": 12345
}
```

---

## Business Rules

### Rule 1: Lock Prevents Deletion

**Rule:** If `is_locked = true`, item cannot be deleted.

**Enforcement:**
- DeletionPolicyService checks `is_locked` before deletion
- UI disables delete button for locked items
- API returns error if deletion attempted on locked item

### Rule 2: Lock Does Not Prevent Edits (MVP)

**Rule:** Locking does NOT prevent edits in MVP.

**Enforcement:**
- Locked items can still be edited (rate, quantity, description)
- Locked items can still be repriced
- Locked items can still be resolved (L0/L1 → L2)

**Future Consideration:**
- Locking may prevent edits in future phases
- Requires explicit policy update

### Rule 3: Lock Persists Across Revisions

**Rule:** Lock state is copied to new revision.

**Enforcement:**
- When creating quotation revision, locked items remain locked
- User can unlock in new revision if needed
- Lock state is independent per revision

### Rule 4: Lock Audit Trail (Future)

**Rule:** Lock/unlock operations should be audited (future).

**Enforcement:**
- Log who locked/unlocked item
- Log when lock/unlock occurred
- Log reason for lock (optional)

**MVP Status:** Not required in MVP, but recommended for future.

---

## Use Cases

### Use Case 1: Protect Critical Items

**Scenario:** Estimator wants to protect specific items from accidental deletion.

**Steps:**
1. User selects item in quotation
2. User clicks "Lock Item" button
3. System sets `is_locked = true`
4. Item cannot be deleted until unlocked

### Use Case 2: Review Workflow

**Scenario:** Reviewer locks items after review to prevent changes.

**Steps:**
1. Reviewer reviews quotation
2. Reviewer locks reviewed items
3. Items cannot be deleted
4. Admin can unlock if changes needed

### Use Case 3: Production Protection

**Scenario:** Items are locked when quotation is finalized/exported.

**Steps:**
1. Quotation is finalized
2. System automatically locks all items
3. Items cannot be deleted
4. Admin can unlock if revision needed

**MVP Status:** Automatic locking on finalization is **future enhancement**, not in MVP.

---

## Future Extensions

### Extension 1: Hierarchy-Level Locking

**Option:** Extend locking to panel/BOM/quotation levels.

**Tables to add `is_locked`:**
- `quote_panels` (panel-level lock)
- `quote_boms` (BOM-level lock)
- `quotations` (quotation-level lock)

**Decision Required:**
- When to extend (post-MVP)
- Locking precedence (item lock overrides panel lock?)
- Locking propagation (lock panel → lock all items?)

### Extension 2: Edit Protection

**Option:** Locking prevents edits, not just deletion.

**Changes Required:**
- Update LockingPolicyService to check `is_locked` before edits
- Update UI to disable edit controls for locked items
- Update API to reject edit requests on locked items

**Decision Required:**
- When to implement (post-MVP)
- Which operations are blocked (edit rate? edit quantity? edit description?)

### Extension 3: Lock Reasons

**Option:** Track reason for locking.

**Schema Addition:**
```sql
locked_by BIGINT UNSIGNED NULL
locked_at TIMESTAMP NULL
lock_reason VARCHAR(255) NULL
```

**Decision Required:**
- When to implement (post-MVP)
- What reasons to track (review, production, manual, etc.)

---

## References

- `PHASE_5_PENDING_UPGRADES_INTEGRATION.md` - Section 1.5 (Deletion Policy - IsLocked Field)
- `SPEC_5_FREEZE_GATE_CHECKLIST.md` - Section 2 (IsLocked Fields)
- `DeletionPolicyService` - Implementation service

---

## Change Log

### v1.0 (2025-01-27) - FROZEN

- Initial MVP locking policy (line-item level only)

**Freeze Date:** 2025-01-27  
**Freeze Reason:** Frozen after Phase-5 Senate review. All Step-1 requirements verified and approved.

---

**Status:** FROZEN  
**Frozen:** 2025-01-27 after Phase-5 Senate review

