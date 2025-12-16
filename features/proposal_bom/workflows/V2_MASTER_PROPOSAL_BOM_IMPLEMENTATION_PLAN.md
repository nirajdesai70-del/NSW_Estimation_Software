> Source: source_snapshot/V2_MASTER_PROPOSAL_BOM_IMPLEMENTATION_PLAN.md
> Bifurcated into: features/proposal_bom/workflows/V2_MASTER_PROPOSAL_BOM_IMPLEMENTATION_PLAN.md
> Module: Proposal BOM > Workflows
> Date: 2025-12-17 (IST)

# Master BOM vs Proposal BOM - Detailed Implementation Plan

## 📋 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-11 | Auto | Initial implementation plan | Detailed phased approach with code changes |

---

## 🔍 CURRENT STATE VERIFICATION

### ✅ What We Already Do Correctly

1. **"Always Copy" Rule:**
   - ✅ When Master BOM is selected, we COPY components (lines 744-808 in QuotationV2Controller)
   - ✅ We create new `QuotationSaleBomItem` records (not linking)
   - ✅ Master BOM remains independent

2. **MasterBomId Reference:**
   - ✅ We set `MasterBomId` on `quotation_sale_boms` (line 678)
   - ✅ This is a reference for tracking, NOT a direct link
   - ✅ Components are copied independently

3. **Service-Based Computation:**
   - ✅ `QuotationQuantityService` handles all quantities
   - ✅ `CostingService` handles all costs
   - ✅ Both are protected and not modified

4. **Soft Delete:**
   - ✅ Using `Status = 1` (consistent across system)
   - ✅ All queries filter `WHERE Status = 0`

### ❌ What We Need to Add

1. **Modification Tracking:**
   - Missing: `IsModified`, `ModifiedBy`, `ModifiedAt`, `OriginMasterBomId`
   - Current: We have `MasterBomId` but don't track if BOM was modified

2. **Orchestration Function:**
   - Missing: Centralized `applyProposalBomChange()` function
   - Current: Operations call recalculation separately

3. **Promotion Feature:**
   - Missing: "Promote to Master BOM" functionality
   - Current: No way to save Proposal BOM as Master BOM

4. **Bulk Edit Modal:**
   - Missing: Full multi-edit UI
   - Current: Structure ready, modal not implemented

---

## 📊 PROPOSAL ALIGNMENT CHECK

| Proposal Concept | Current State | Alignment | Action Needed |
|-----------------|---------------|-----------|---------------|
| Master BOM = Library | ✅ We have `master_boms` | ✅ Aligned | Document terminology |
| Proposal BOM = Instance | ✅ We have `quotation_sale_boms` | ✅ Aligned | Document terminology |
| Always Copy Rule | ✅ We copy components | ✅ Aligned | Document and enforce |
| Service-only computation | ✅ Already enforced | ✅ Aligned | Add explicit checks |
| Soft delete | ✅ Using `Status = 1` | ✅ Aligned | Document standard |
| Recalculation cascade | ✅ Already implemented | ✅ Aligned | Use orchestration |
| Modification tracking | ❌ Not implemented | ⚠️ Gap | Add fields + logic |
| Orchestration function | ❌ Not implemented | ⚠️ Gap | Create service |
| Promotion feature | ❌ Not implemented | ⚠️ Gap | Add functionality |
| Bulk operations | ⚠️ Partial | ⚠️ Partial | Complete modal |

**Overall Assessment:** ✅ **90% aligned** - Most concepts already implemented, need to add tracking, orchestration, and promotion.

---

## 🎯 RECOMMENDATION

**✅ YES - This proposal is VERY USEFUL and should be adopted**

**Why:**
1. **Fills important gaps** - Modification tracking, orchestration, promotion
2. **Improves maintainability** - Clear terminology, standard patterns
3. **Enhances functionality** - Bulk operations, audit trail, promotion
4. **Prevents bugs** - Orchestration ensures consistency
5. **Aligns with existing code** - 90% already matches

**Adaptation:**
- Keep `Status = 1` soft delete (don't switch to `deleted_at`)
- Implement in phases (not all at once)
- Maintain backward compatibility

---

## 📋 DETAILED IMPLEMENTATION PLAN

### Phase 1: Terminology & Documentation (1-2 hours) ⭐ START HERE

**Goal:** Establish clear terminology and document existing behavior

**Tasks:**

1. **Create Terminology Document:**
   - `V2_TERMINOLOGY.md` - Master BOM vs Proposal BOM definitions
   - Document "Always Copy" rule
   - Document service-only computation rule

2. **Update Code Comments:**
   - Add comments in `QuotationV2Controller@applyMasterBom`:
     ```php
     /**
      * Apply Master BOM to Proposal BOM
      * 
      * GOLDEN RULE: Always copies components, never links directly.
      * This ensures Master BOM remains independent and reusable.
      * 
      * Creates new Proposal BOM instance with copied components.
      */
     ```

3. **Update UI Labels:**
   - Change "Master BOM" button to "Use Master BOM" (clarifies it's a copy)
   - Add tooltips explaining Master vs Proposal BOM

**Files:**
- `V2_TERMINOLOGY.md` (NEW)
- `app/Http/Controllers/QuotationV2Controller.php` (comments)
- `resources/views/quotation/v2/_bom.blade.php` (labels)

**Risk:** ⭐ Low - Documentation only

---

### Phase 2: Modification Tracking (2-3 hours)

**Goal:** Track when Proposal BOMs are modified from their origin

**Tasks:**

1. **Create Migration:**
   ```php
   // database/migrations/YYYY_MM_DD_add_modification_tracking_to_quotation_sale_boms.php
   Schema::table('quotation_sale_boms', function (Blueprint $table) {
       $table->boolean('IsModified')->default(false)->after('MasterBomName');
       $table->unsignedInteger('ModifiedBy')->nullable()->after('IsModified');
       $table->timestamp('ModifiedAt')->nullable()->after('ModifiedBy');
       $table->unsignedInteger('OriginMasterBomId')->nullable()->after('ModifiedAt');
       $table->string('OriginMasterVersion', 50)->nullable()->after('OriginMasterBomId');
       
       $table->index('IsModified');
       $table->index('OriginMasterBomId');
       $table->foreign('ModifiedBy')->references('id')->on('users')->onDelete('set null');
       $table->foreign('OriginMasterBomId')->references('MasterBomId')->on('master_boms')->onDelete('set null');
   });
   ```

2. **Update Model:**
   ```php
   // app/Models/QuotationSaleBom.php
   protected $fillable = [
       // ... existing fields ...
       'IsModified',
       'ModifiedBy',
       'ModifiedAt',
       'OriginMasterBomId',
       'OriginMasterVersion'
   ];
   
   protected $casts = [
       'IsModified' => 'boolean',
       'ModifiedAt' => 'datetime'
   ];
   ```

3. **Update BOM Creation Logic:**
   - In `applyMasterBom()`: Set `OriginMasterBomId = MasterBomId`, `IsModified = false`
   - In `applyProposalBom()`: Set `OriginMasterBomId` from source if it has one
   - In `addBom()`: Set `IsModified = false` (new BOM, not from template)

4. **Update BOM Edit Logic:**
   - In `updateBom()`: Set `IsModified = true`, `ModifiedBy = auth()->id()`, `ModifiedAt = now()`
   - In component add/edit/delete: Mark parent BOM as modified
   - Create helper method: `markBomAsModified($bomId)`

**Files:**
- Migration file (NEW)
- `app/Models/QuotationSaleBom.php`
- `app/Http/Controllers/QuotationV2Controller.php` (applyMasterBom, updateBom, addItem, etc.)

**Risk:** ⭐⭐ Medium - Database changes, but backward compatible (nullable fields)

---

### Phase 3: Orchestration Function (3-4 hours)

**Goal:** Create centralized function to ensure chain integrity

**Tasks:**

1. **Create BomChangeOrchestrator Service:**
   ```php
   // app/Services/BomChangeOrchestrator.php
   class BomChangeOrchestrator {
       public function applyProposalBomChange($quotationId, $proposalBomRootId, $changeSet) {
           DB::beginTransaction();
           try {
               // 1. Apply changes (add/edit/delete)
               $this->applyChanges($changeSet);
               
               // 2. Mark BOM as modified if needed
               if ($changeSet['markModified'] ?? false) {
                   $this->markBomAsModified($proposalBomRootId);
               }
               
               // 3. Commit transaction
               DB::commit();
               
               // 4. Recalculate quantities
               $this->recalculateQuantities($proposalBomRootId);
               
               // 5. Recalculate costs
               $this->recalculateCosts($proposalBomRootId);
               
               // 6. Roll-up to quotation
               $this->rollupToQuotation($quotationId);
               
               // 7. Audit log
               $this->logChange($quotationId, $proposalBomRootId, $changeSet);
               
               return ['success' => true];
           } catch (\Exception $e) {
               DB::rollBack();
               throw $e;
           }
       }
   }
   ```

2. **Refactor Existing Operations:**
   - `addItem()` - Use orchestrator
   - `updateItemQty()` - Use orchestrator
   - `updateItemRate()` - Use orchestrator
   - `updateItemDiscount()` - Use orchestrator
   - `deleteBom()` - Use orchestrator
   - `itemremove()` - Use orchestrator
   - `batchUpdateItems()` - Use orchestrator

3. **Add Helper Methods:**
   - `recalculateQuantities($bomId)` - Calls QuotationQuantityService
   - `recalculateCosts($bomId)` - Calls CostingService
   - `rollupToQuotation($quotationId)` - Rolls up to quotation level
   - `markBomAsModified($bomId)` - Sets modification flags
   - `logChange(...)` - Audit logging

**Files:**
- `app/Services/BomChangeOrchestrator.php` (NEW)
- `app/Http/Controllers/QuotationV2Controller.php` (refactor)
- `app/Http/Controllers/QuotationController.php` (itemremove refactor)

**Risk:** ⭐⭐ Medium - Refactoring existing code, but improves consistency

---

### Phase 4: Promotion Feature (2-3 hours)

**Goal:** Allow promoting Proposal BOM to Master BOM

**Tasks:**

1. **Add "Promote to Master BOM" Button:**
   - In `_bom.blade.php` header
   - Only show if BOM has components
   - Check user role (optional)

2. **Create Promotion Method:**
   ```php
   // app/Http/Controllers/QuotationV2Controller.php
   public function promoteToMasterBom(Request $request, $quotationId, $bomId) {
       // 1. Validate BOM exists and belongs to quotation
       // 2. Get all components in BOM
       // 3. Create new Master BOM record
       // 4. Copy components to master_bom_items
       // 5. Store provenance (quotation, customer, date)
       // 6. Return success
   }
   ```

3. **Add Route:**
   ```php
   Route::post('quotation/{quotation}/bom/{bom}/promote', 
       [QuotationV2Controller::class, 'promoteToMasterBom'])
       ->name('quotation.v2.promoteToMasterBom');
   ```

4. **Create Promotion Modal:**
   - Ask for Master BOM name
   - Show preview of components
   - Confirm promotion

**Files:**
- `app/Http/Controllers/QuotationV2Controller.php` (promoteToMasterBom method)
- `resources/views/quotation/v2/_bom.blade.php` (button)
- `resources/views/quotation/v2/_promote_bom_modal.blade.php` (NEW)
- `routes/web.php` (route)

**Risk:** ⭐⭐ Low-Medium - New feature, doesn't affect existing code

---

### Phase 5: Complete Bulk Operations (4-5 hours)

**Goal:** Implement full bulk edit functionality

**Tasks:**

1. **Create Multi-Edit Modal:**
   ```blade
   <!-- resources/views/quotation/v2/_multi_edit_modal.blade.php -->
   - Show selected components list
   - Bulk operations:
     * Set quantity (absolute, add delta, multiply factor)
     * Set make/series
     * Apply discount %
     * Apply rate logic
     * Delete selected
     * Replace with new component
   ```

2. **Implement Bulk Operations:**
   - Update `openMultiEditModal()` to show modal
   - Update `batchUpdateItems()` to handle all operations
   - Use orchestration function for all bulk operations

3. **Add Validation:**
   - Validate all selected items belong to same quotation
   - Validate user has permission
   - Show confirmation with impact summary

**Files:**
- `resources/views/quotation/v2/_multi_edit_modal.blade.php` (NEW)
- `resources/views/quotation/v2/panel.blade.php` (update openMultiEditModal)
- `app/Http/Controllers/QuotationV2Controller.php` (enhance batchUpdateItems)

**Risk:** ⭐⭐ Medium - Completing existing structure

---

### Phase 6: Audit Trail (1-2 hours)

**Goal:** Log all BOM changes for audit

**Tasks:**

1. **Add Audit Logging:**
   - In `BomChangeOrchestrator@logChange()`:
     ```php
     Log::info('BOM Change', [
         'quotation_id' => $quotationId,
         'bom_id' => $bomId,
         'user_id' => auth()->id(),
         'action' => $changeSet['action'],
         'items_affected' => count($changeSet['items']),
         'before_summary' => $beforeSummary,
         'after_summary' => $afterSummary,
         'timestamp' => now()
     ]);
     ```

2. **Optional: Create Audit Table:**
   - If detailed audit needed, create `bom_change_logs` table
   - Store before/after values
   - Queryable for reports

**Files:**
- `app/Services/BomChangeOrchestrator.php` (logChange method)
- Optional: Migration for `bom_change_logs` table

**Risk:** ⭐ Low - Additive feature

---

## 🔧 STANDARD RULES - GLOBAL IMPLEMENTATION

### Rule 1: Terminology Standard

**Implementation:**
- Update all UI labels to use "Master BOM" and "Proposal BOM"
- Update code comments
- Create terminology glossary

**Files to Update:**
- All Blade files with BOM references
- Controller comments
- Service comments

---

### Rule 2: Always Copy Rule

**Implementation:**
- Verify `applyMasterBom()` already copies (✅ it does)
- Add explicit validation to prevent direct linking
- Document in code comments

**Code Check:**
```php
// ✅ VERIFIED: applyMasterBom() creates new QuotationSaleBomItem records
// ✅ VERIFIED: Components are copied, not linked
// ✅ VERIFIED: Master BOM remains independent
```

---

### Rule 3: Service-Only Computation

**Implementation:**
- Add explicit checks in controllers
- Add code comments
- Add validation to prevent UI calculations

**Code Pattern:**
```php
// ✅ CORRECT: Use service
$qtyData = app(QuotationQuantityService::class)->calculate($item);

// ❌ WRONG: Don't calculate in controller
// $totalQty = $item->Qty * $bom->Qty; // DON'T DO THIS
```

---

### Rule 4: Soft Delete Standard

**Implementation:**
- Document `Status = 1` as standard
- Verify all queries use `WHERE Status = 0`
- Add global scope if needed

**Code Pattern:**
```php
// ✅ CORRECT: Always filter by Status
QuotationSaleBom::where('Status', 0)->get();

// ❌ WRONG: Missing Status filter
// QuotationSaleBom::all(); // DON'T DO THIS
```

---

### Rule 5: Recalculation Cascade

**Implementation:**
- Use orchestration function for all changes
- Ensure cascade: Component → BOM → Feeder → Panel → Quotation
- Document cascade order

**Code Pattern:**
```php
// ✅ CORRECT: Use orchestrator
$orchestrator->applyProposalBomChange($quotationId, $bomId, $changeSet);

// ❌ WRONG: Manual recalculation
// $item->save();
// $costingService->recalculatePanel($panel); // DON'T DO THIS DIRECTLY
```

---

### Rule 6: Orchestration Function

**Implementation:**
- Create `BomChangeOrchestrator` service
- Refactor all operations to use it
- Add validation to prevent bypassing

**Code Pattern:**
```php
// ✅ CORRECT: Use orchestrator
$orchestrator->applyProposalBomChange($quotationId, $bomId, [
    'action' => 'update',
    'items' => [...],
    'markModified' => true
]);

// ❌ WRONG: Direct changes
// $item->update([...]);
// $costingService->recalculatePanel($panel); // DON'T BYPASS ORCHESTRATOR
```

---

## 📝 IMPLEMENTATION ORDER (RECOMMENDED)

### Week 1: Foundation
1. **Phase 1: Terminology** (1-2 hours) ⭐ START HERE
   - Immediate clarity, no risk

2. **Phase 2: Modification Tracking** (2-3 hours)
   - Enables other features
   - Backward compatible

### Week 2: Core Features
3. **Phase 3: Orchestration Function** (3-4 hours)
   - Improves consistency
   - Foundation for other features

4. **Phase 4: Promotion Feature** (2-3 hours)
   - High value for users
   - Independent feature

### Week 3: Enhancements
5. **Phase 5: Complete Bulk Operations** (4-5 hours)
   - Completing existing work
   - High efficiency gain

6. **Phase 6: Audit Trail** (1-2 hours)
   - Good for compliance
   - Low risk

**Total Estimated Time:** 13-19 hours over 3 weeks

---

## ⚠️ RISKS & MITIGATION

### Risk 1: Breaking Existing Functionality
**Mitigation:**
- Implement in phases
- Test each phase thoroughly
- Maintain backward compatibility
- Use feature flags if needed

### Risk 2: Performance Impact
**Mitigation:**
- Orchestration function should batch operations
- Use transactions efficiently
- Monitor performance
- Cache where appropriate

### Risk 3: Data Migration
**Mitigation:**
- New fields are nullable
- Existing data remains valid
- Migration is backward compatible
- Test migration on staging first

---

## ✅ BENEFITS SUMMARY

1. **Clear Terminology:** Easier to understand and maintain
2. **Modification Tracking:** Know which BOMs were customized
3. **Orchestration:** Prevents bugs, ensures consistency
4. **Promotion:** Reuse successful BOMs as templates
5. **Bulk Operations:** Efficient multi-component editing
6. **Audit Trail:** Compliance and debugging
7. **Standard Rules:** Consistent behavior across system

---

## 🎯 FINAL RECOMMENDATION

**✅ PROCEED with implementation in phases:**

1. **Start with Phase 1** (Terminology) - Immediate value, zero risk
2. **Then Phase 2** (Modification Tracking) - Enables other features
3. **Then Phase 3** (Orchestration) - Improves consistency
4. **Then Phases 4-6** as needed

**This approach:**
- ✅ Minimizes risk
- ✅ Provides incremental value
- ✅ Maintains backward compatibility
- ✅ Aligns with existing architecture (90% match)

**Ready to proceed?** Start with Phase 1 (Terminology) - it's documentation only and provides immediate clarity.


