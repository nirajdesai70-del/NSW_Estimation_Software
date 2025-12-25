# Resolution-B Rules (L2 Write Enforcement)

**File:** docs/RESOLUTION_B/RESOLUTION_B_RULES.md  
**Version:** v1.0_2025-12-19  
**Status:** 🔒 FROZEN (Phase-3 Complete, Resolution-B Analysis)  
**Scope:** Proposal BOM (QuotationSaleBomItem) L2 write enforcement

---

## Objective

Ensure all Proposal BOM write operations enforce L2 (Specific Item) discipline:
- Only Specific products (ProductType=2) can be persisted in final state
- MakeId and SeriesId must be present and valid
- No silent defaults that bypass validation
- No raw DB inserts that bypass application logic

---

## 1. L2 Write Requirements

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

---

## 2. Master BOM and Feeder Templates Are NEVER L2

- **Master BOM (L1):** Operates at L1 layer with Generic products (ProductType=1) or ProductId=NULL (spec template)
- **Feeder Templates:** Same as Master BOM (L1 layer, Generic products)
- **Proposal BOM:** ALWAYS L2 at final state (Specific products, ProductType=2)

**Copy semantics:**
- Copying from Master BOM/Feeder to Proposal BOM is L1→L2 resolution
- Generic products from source are acceptable as INTERMEDIATE state
- Must resolve to Specific (ProductType=2, MakeId>0, SeriesId>0) before finalization

---

## 3. Proposal BOM Is ALWAYS L2 at Final State

- All Proposal BOM items in final persisted state (Status=0) must use Specific products
- No exceptions for "convenience" or "legacy compatibility"
- Transitional states are allowed ONLY during active resolution workflows

---

## 4. Raw DB Inserts Are Forbidden

Direct database inserts into `quotation_sale_bom_items` are FORBIDDEN:
- `DB::table('quotation_sale_bom_items')->insert()` — FORBIDDEN
- `DB::insert()` targeting `quotation_sale_bom_items` — FORBIDDEN
- Only allowed via:
  - Eloquent model methods (`QuotationSaleBomItem::create()`, `update()`, `updateOrCreate()`)
  - Through centralized write gateway (Phase-4)

**Rationale:**
- Bypasses application validation
- Bypasses business rules
- Creates audit trail gaps
- Introduces data integrity risks

**Exception:**
- Data migration scripts (must be explicitly approved, documented, and one-time)

---

## 5. Reuse/Apply Must CLEAR or MERGE Explicitly

When applying/reusing Proposal BOM items:
- **Default behavior:** CLEAR existing items before copying
- **Merge mode:** Only if explicitly flagged (rare, must be documented)

**Forbidden patterns:**
- Apply without clearing → creates duplicate stacking
- Silent merge without explicit flag → creates confusion and potential data corruption

**Required pattern:**
```php
// CORRECT: Clear before apply
$quotation->quotationSaleBomItems()->delete(); // or soft delete
// Then apply new items

// CORRECT: Explicit merge flag
$options = ['merge' => true]; // Must be explicit
applyProposalBom($source, $target, $options);
```

---

## 6. Write Path Validation Order

All write paths must validate in this order:

1. **Product exists and is ProductType=2** (or transitional state is explicitly allowed)
2. **MakeId and SeriesId are valid** (if ProductType=2)
3. **GenericId is present** (for traceability)
4. **No duplicate stacking** (if apply/reuse operation)
5. **Persist only if all validations pass**

---

## 7. Transitional State Rules

During L1→L2 resolution (copy from Master BOM/Feeder):

1. **Copy phase:** Generic ProductId is acceptable
   - `ProductId` from Master BOM (Generic, ProductType=1)
   - `MakeId = 0`, `SeriesId = 0`

2. **Resolution phase:** Must resolve before finalization
   - User selects Make/Series
   - System updates to Specific product (ProductType=2)
   - Sets `MakeId > 0`, `SeriesId > 0`

3. **Finalization phase:** All L2 requirements must be met
   - `Status = 0` implies `ProductType = 2`, `MakeId > 0`, `SeriesId > 0`

**Forbidden:**
- Persisting transitional state as "final" (Status=0 with ProductType=1 or MakeId=0)
- Allowing transitional state to be used in costing/export/apply operations

---

## 8. Validation Failure Handling

If validation fails:
- **DO NOT** persist the item
- **DO** return explicit error message indicating which requirement failed
- **DO** log the validation failure for audit
- **DO NOT** silently default to invalid values

**Forbidden patterns:**
```php
// FORBIDDEN: Silent default
$makeId = $request->makeId ?? 0; // NO - violates L2 requirement

// FORBIDDEN: Silent bypass
if (!$makeId) { $makeId = 0; } // NO - violates L2 requirement
```

**Required pattern:**
```php
// REQUIRED: Explicit validation
if ($product->ProductType != 2) {
    throw new ValidationException("Proposal BOM requires Specific products (ProductType=2)");
}
if (!$makeId || $makeId <= 0) {
    throw new ValidationException("MakeId is required and must be > 0");
}
```

---

## 9. Audit Trail Requirements

All Proposal BOM writes must:
- Log the write operation (who, when, what, why)
- Record validation results (passed/failed, reason if failed)
- Track source (Master BOM copy, Feeder template, manual add, reuse, etc.)

---

## 10. Phase-4 Implementation Strategy

Phase-4 will implement:
- Centralized write gateway service (`ProposalBomItemWriter`)
- All write paths migrate to use gateway
- Gateway enforces all rules above
- Existing controllers become thin wrappers around gateway

**Current phase (Resolution-B analysis):**
- Identify all write paths
- Document violations
- Design gateway interface
- NO code changes yet

---

## References

- `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:PB-GAP-001` — Transitional Generic → Specific state
- `PROPOSAL_BOM_GAP_REGISTER_R1_v1.0_2025-12-19.md:PB-GAP-002` — Enforcement location for "Specific products only"
- `PROPOSAL_BOM_BACKEND_DESIGN_PART5_RULES.md` — Rules enforce "Specific products only"
- `PROPOSAL_BOM_BACKEND_DESIGN_PART4_OPERATIONS.md` — Copy step sets ProductId from Master BOM item (generic)

