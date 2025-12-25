# Cursor Verification Prompt — Product Delete/Archive Compliance  
**Purpose:** Verify no hard delete operations exist for products and archival follows standard  
**Standard:** `NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md`  
**Date (IST):** 2025-12-18  

---

## Copy/Paste This Prompt into Cursor

```
Verify the codebase against NEPL_PRODUCT_ARCHIVAL_STANDARD_v1.0_20251218.md.

Search for ALL product deletion/archive operations and verify:

1. NO hard delete operations (STRICT):
   Search patterns (must include):

   * Product::destroy(
   * Product::where(...)->delete(
   * Product::query()->delete(
   * ->delete() on Product instances ($product->delete())
   * ->destroy() calls in controllers/services
   * DB::table('products')->delete(
   * DB::table('products')->where(...)->delete(
   * DB::statement("DELETE FROM products")
   * forceDelete() if SoftDeletes is introduced

   If found, flag as VIOLATION with:

   * exact file path + line number
   * snippet
   * impact statement
   * required fix

2. Soft delete compliance (REQUIRED):

   * Archive must be Status = 1 (not hard delete)
   * Preferred and required path: ProductArchiveService::archiveProduct($productId)
   * If any custom archival exists (Status=1 directly), verify:
     a) dependency checks exist (specific products, BOM refs, quotations)
     b) blocked messages are precise
     c) consistent with NEPL_PRODUCT_ARCHIVAL_STANDARD

3. Controller/Service verification:

   * Check all controllers for destroy()/delete() methods or routes
   * Check all services for product deletion logic
   * Verify they call ProductArchiveService, not direct delete/update

4. Dependency checks:
   Verify archival checks:

   * Generic product: blocks if specific products exist (GenericId references)
   * Blocks if referenced in Master BOM
   * Blocks if referenced in quotations (as per policy)
     Flag any archival that does not check dependencies.

Output format:

* PASS/FAIL per check (1..4)
* For each violation:

  * File path + line number
  * Current code snippet
  * Why it violates the standard
  * Required fix (use ProductArchiveService or compliant dependency-checked Status=1 archival)
```

---

## Expected Output Format

```
VERIFICATION RESULTS:

1. Hard Delete Check: ❌ FAIL

   * File: app/Http/Controllers/ProductController.php
   * Line: 45
   * Code: $product->delete();
   * Fix: Replace with ProductArchiveService::archiveProduct($productId)

2. Soft Delete Compliance: ⚠️ PARTIAL

   * File: app/Services/CustomProductService.php
   * Line: 120
   * Code: $product->Status = 1; $product->save();
   * Issue: Missing dependency checks + inconsistent messaging
   * Fix: Use ProductArchiveService::archiveProduct()

3. Controller/Service Verification: ✅ PASS

   * No delete paths outside ProductArchiveService found

4. Dependency Checks: ❌ FAIL

   * File: app/Services/CustomProductService.php
   * Line: 120
   * Issue: No dependency checks before archival
   * Fix: Use ProductArchiveService which includes dependency checks
```

---

**END OF PROMPT**

