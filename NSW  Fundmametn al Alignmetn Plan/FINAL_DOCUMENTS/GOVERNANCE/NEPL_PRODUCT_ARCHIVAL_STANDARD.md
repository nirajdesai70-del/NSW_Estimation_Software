# NEPL Product Archival & Deletion Standard  
**Version:** 1.1_20251219  
**Date (IST):** 2025-12-18 11:45  
**Status:** 🔒 MASTER — PERMANENT STANDARD  
**Applies to:** Products (Generic + Specific), Item Master, BOM, Quotation references  
**Policy:** No hard delete in production.  
**Last Updated:** 2025-12-19 (Phase-3: L0-L1-L2 layer context)

---

## 1) Objective

Define a single, unambiguous approach to "delete" so the system remains:
- audit-safe
- traceable
- consistent with quotation history
- consistent with BOM reuse
- consistent with governance standards

---

## 2) Definitions (Locked)

### 2.1 Layer Context (Reference: NEPL_CANONICAL_RULES)

> **📌 Canonical Reference:** For the authoritative single source of truth on L0/L1/L2 rules, see `docs/NEPL_STANDARDS/00_BASELINE_FREEZE/NEPL_CANONICAL_RULES.md` (Section 1.1).

- **L0/L1 (Generic Products):** ProductType = 1
  - L0 = Generic Item Master (functional family, never used in BOM)
  - L1 = Technical variant (make-agnostic, used in Master BOM)
- **L2 (Specific Products):** ProductType = 2
  - L2 = Catalog item (make + series + SKU, used in Proposal BOM)

### 2.2 "Delete" means Archive (Soft Delete)
- Implemented as: `products.Status = 1`
- Product remains in DB for traceability
- Hidden from default UI listings and selectors

### 2.3 Hard delete is prohibited
- `DELETE FROM products ...` is NOT allowed in production.
- Hard delete is allowed only in controlled dev/test reset scripts (never in UI/controllers).

---

## 3) Archival Rules (Generic vs Specific)

### 3.1 Generic Product (ProductType=1) archival rules
A Generic Product can be archived only if ALL are true:

1. No Specific products exist:
   - `products.ProductType=2 AND products.GenericId = <Generic ProductId> AND Status=0`
2. Not referenced in Master BOM (if your Master BOM stores ProductId references):
   - `master_bom_items.ProductId = <Generic ProductId>` (or equivalent)
3. Not referenced in Quotation BOMs (optional but recommended):
   - `quotation_sale_bom_items.ProductId = <Generic ProductId>` (if ever stored)

If any dependency exists → archive must be blocked with a precise reason.

### 3.2 Specific Product (ProductType=2) archival rules
A Specific Product can be archived only if ALL are true:

1. Not referenced by active quotations (recommended):
   - If referenced, allow archive only if quotation stores snapshot rates & does not need product lookup
2. Not referenced in open procurement workflows (if applicable)

---

## 4) Canonical Service Method (Only Approved Implementation)

Create a dedicated service:

`app/Services/ProductArchiveService.php`

### Method: archiveProduct()

```php
public function archiveProduct(int $productId, array $context = []): array
{
    $product = Product::where('ProductId', $productId)->firstOrFail();

    // Block hard delete always
    // Use Status=1 archival only
    if ((int)$product->Status === 1) {
        return [
            'success' => true,
            'status' => 'ALREADY_ARCHIVED',
            'message' => 'Product is already archived.',
        ];
    }

    // Dependency checks
    $dependencies = [];

    // 1) If generic, block if any active specifics exist
    if ((int)$product->ProductType === 1) {
        $hasSpecifics = Product::where('ProductType', 2)
            ->where('GenericId', $product->ProductId)
            ->where('Status', 0)
            ->exists();

        if ($hasSpecifics) {
            $dependencies[] = 'SPECIFIC_PRODUCTS_EXIST';
        }

        // 2) Block if used in Master BOM (adjust table/field names to actual schema)
        $usedInMasterBom = DB::table('master_bom_items')
            ->where('ProductId', $product->ProductId)
            ->whereIn('ResolutionStatus', ['L0','L1']) // if applicable
            ->exists();

        if ($usedInMasterBom) {
            $dependencies[] = 'REFERENCED_IN_MASTER_BOM';
        }

        // 3) Optional: block if used in quotation BOMs
        $usedInQuotation = DB::table('quotation_sale_bom_items')
            ->where('ProductId', $product->ProductId)
            ->where('Status', 0)
            ->exists();

        if ($usedInQuotation) {
            $dependencies[] = 'REFERENCED_IN_QUOTATION';
        }
    }

    // If blocked, return precise message
    if (!empty($dependencies)) {
        return [
            'success' => false,
            'status' => 'BLOCKED',
            'dependencies' => $dependencies,
            'message' => $this->formatArchiveBlockedMessage($dependencies),
        ];
    }

    // Archive (soft delete)
    $product->Status = 1;
    $product->save();

    // Optional: audit log (recommended)
    // ProductArchiveAuditLog::create([...])

    return [
        'success' => true,
        'status' => 'ARCHIVED',
        'message' => 'Product archived successfully.',
    ];
}

private function formatArchiveBlockedMessage(array $deps): string
{
    // Priority messaging
    if (in_array('SPECIFIC_PRODUCTS_EXIST', $deps)) {
        return 'Blocked: Specific products exist for this Generic. Archive specific products first or reassign them.';
    }
    if (in_array('REFERENCED_IN_MASTER_BOM', $deps)) {
        return 'Blocked: Product is referenced in Master BOM. Remove/replace references before archiving.';
    }
    if (in_array('REFERENCED_IN_QUOTATION', $deps)) {
        return 'Blocked: Product is referenced in quotations. Archiving is not allowed unless quotation snapshots are independent.';
    }
    return 'Blocked: Product has dependencies and cannot be archived.';
}
```

---

## 5) UI / Controller Contract (Even if UI is deferred)

Any UI/controller that performs deletion must:

* call `ProductArchiveService::archiveProduct()`
* never call `->delete()`
* show the exact returned message
* display dependency codes if blocked

---

## 6) Standard Messages (No Confusion)

### Success

* `Product archived successfully.`

### Blocked (Generic)

* `Blocked: Specific products exist for this Generic. Archive specific products first or reassign them.`

### Blocked (BOM)

* `Blocked: Product is referenced in Master BOM. Remove/replace references before archiving.`

### Blocked (Quotation)

* `Blocked: Product is referenced in quotations. Archiving is not allowed unless quotation snapshots are independent.`

---

## 7) Change Log

| Version | Date (IST)       | Change Type | Summary                                                    |
| ------- | ---------------- | ----------- | ---------------------------------------------------------- |
| v1.0    | 2025-12-18 11:45 | Freeze      | Canonical archival standard + dependency checks + messages |
| v1.1_20251219 | 2025-12-19 | Phase-3 | Added L0-L1-L2 layer context reference to definitions |

---

**END OF DOCUMENT**

