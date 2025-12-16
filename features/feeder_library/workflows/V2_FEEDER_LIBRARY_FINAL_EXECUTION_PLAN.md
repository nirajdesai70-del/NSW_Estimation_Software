> Source: source_snapshot/V2_FEEDER_LIBRARY_FINAL_EXECUTION_PLAN.md
> Bifurcated into: features/feeder_library/workflows/V2_FEEDER_LIBRARY_FINAL_EXECUTION_PLAN.md
> Module: Feeder Library > Workflows
> Date: 2025-12-17 (IST)

# V2 Feeder Library - Final Execution Plan (A+C Hybrid)

**Date:** December 2025  
**Status:** 📋 **READY FOR EXECUTION - AWAITING FINAL CONFIRMATION**

---

## 🎯 EXECUTIVE SUMMARY

**Goal:** Implement Feeder Library using master_boms (Option A) + Feeder Library UI (Option C) hybrid approach, with full backward compatibility for existing data.

**Key Principles:**
- ✅ No changes to CostingService or QuotationQuantityService (already correct)
- ✅ No destructive database migrations
- ✅ Virtual feeder interpretation for legacy data (in-memory only)
- ✅ Feeder templates stored as canonical Qty=1, regardless of source
- ✅ Phases 1-4 are safe and additive
- ⚠️ Phase 5 (Legacy Step Page) deferred until V2 is stable

---

## 📊 CURRENT STATE ANALYSIS

### ✅ What's Working

1. **Database Schema:**
   - ✅ `quotation_sale_boms` has Level, FeederName, BomName, ParentBomId
   - ✅ V2 hierarchy fields exist

2. **V2 Panel:**
   - ✅ "Add Feeder" button exists
   - ✅ Feeder display works
   - ✅ `applyFeederReuse()` exists

3. **Services:**
   - ✅ CostingService: Correct (sums Amounts only)
   - ✅ QuotationQuantityService: Correct (EffQtyPerPanel, TotalQty)

### ❌ What's Missing

1. **master_boms:**
   - ❌ Missing `TemplateType` field
   - ❌ Missing `IsActive` field
   - ❌ Missing `DefaultFeederName` field

2. **Feeder Library:**
   - ❌ No `FeederTemplateController`
   - ❌ No `/feeder-library` routes
   - ❌ No Feeder Library UI pages

3. **V2 Panel:**
   - ❌ Missing "Add Feeder from Library" button
   - ❌ Missing `applyFeederTemplate()` method

4. **Legacy Data Integration:**
   - ⚠️ V2 panel may not handle virtual feeders for legacy data correctly
   - Need to verify and enhance if needed

---

## 🔧 PHASE 1: DATABASE & MODEL (Foundation)

### Step 1.1: Migration - Add Template Fields to master_boms

**File:** `database/migrations/YYYY_MM_DD_HHMMSS_add_template_fields_to_master_boms.php`

```php
Schema::table('master_boms', function (Blueprint $table) {
    $table->string('TemplateType', 50)
          ->nullable()
          ->index()
          ->comment('FEEDER, PANEL, GENERIC, etc.');
    
    $table->boolean('IsActive')
          ->default(1)
          ->index()
          ->comment('1 = Active / in library, 0 = Archived');
    
    $table->string('DefaultFeederName', 191)
          ->nullable()
          ->comment('Suggested feeder name when applying template');
});
```

**Risk:** ✅ **LOW** - Only adding fields, no data changes

---

### Step 1.2: Update MasterBom Model

**File:** `app/Models/MasterBom.php`

```php
protected $fillable = [
    'MasterBomId', 'Name','UniqueNo','Description',
    'TemplateType',      // NEW
    'IsActive',          // NEW
    'DefaultFeederName', // NEW
];

protected $casts = [
    'IsActive' => 'boolean',
];

public function scopeFeederTemplates($query)
{
    return $query->where('TemplateType', 'FEEDER')
                 ->where('IsActive', 1);
}

public function scopeTemplates($query)
{
    return $query->whereNotNull('TemplateType');
}
```

**Risk:** ✅ **LOW** - Model updates only

---

## 🔧 PHASE 2: FEEDER LIBRARY BACKEND

### Step 2.1: Create FeederTemplateController

**File:** `app/Http/Controllers/FeederTemplateController.php`

**Methods:**
- `index()` - List TemplateType='FEEDER' templates (paginated)
- `show($id)` - View template details + component list
- `create()` - Show create form
- `store(Request $request)` - Create new template
- `edit($id)` - Show edit form
- `update(Request $request, $id)` - Update template
- `toggleActive($id)` - Archive/activate template

**Key Rules:**
- Only show TemplateType='FEEDER' templates
- Filter by IsActive=1 by default
- Support search/filter by Name, Category, etc.

**Risk:** ✅ **LOW** - New controller, doesn't touch existing code

---

### Step 2.2: Add Routes

**File:** `routes/web.php`

```php
Route::prefix('feeder-library')->middleware(['auth'])->group(function () {
    Route::get('/', [FeederTemplateController::class, 'index'])->name('feeder-library.index');
    Route::get('/create', [FeederTemplateController::class, 'create'])->name('feeder-library.create');
    Route::post('/', [FeederTemplateController::class, 'store'])->name('feeder-library.store');
    Route::get('/{id}', [FeederTemplateController::class, 'show'])->name('feeder-library.show');
    Route::get('/{id}/edit', [FeederTemplateController::class, 'edit'])->name('feeder-library.edit');
    Route::put('/{id}', [FeederTemplateController::class, 'update'])->name('feeder-library.update');
    Route::patch('/{id}/toggle', [FeederTemplateController::class, 'toggleActive'])->name('feeder-library.toggle');
});
```

**Risk:** ✅ **LOW** - New routes only

---

## 🔧 PHASE 3: FEEDER LIBRARY UI

### Step 3.1: Create Views

**Files:**
- `resources/views/feeder-library/index.blade.php` - List templates
- `resources/views/feeder-library/show.blade.php` - View template details
- `resources/views/feeder-library/create.blade.php` - Create form
- `resources/views/feeder-library/edit.blade.php` - Edit form

**Key Features:**
- Table with columns: Name, DefaultFeederName, UniqueNo, Description, Status, Actions
- Search/filter functionality
- Pagination
- Use existing `<x-nepl-table>` component if available

**Risk:** ✅ **LOW** - New views only

---

### Step 3.2: Add Navigation Link

**File:** Navigation/sidebar (wherever master BOM link exists)

Add: "Feeder Library" link pointing to `/feeder-library`

**Risk:** ✅ **LOW** - Navigation update only

---

## 🔧 PHASE 4: V2 PANEL "ADD FEEDER FROM LIBRARY"

### Step 4.1: Add Button to V2 Panel

**File:** `resources/views/quotation/v2/panel.blade.php` (near line 307)

```html
<button type="button" 
        class="btn btn-outline-primary btn-sm" 
        onclick="openFeederLibraryModal({{ $quotation->QuotationId }}, {{ $panel->QuotationSaleId }})">
    <i class="la la-clone"></i> Add Feeder from Library
</button>
```

**Placement:** Next to existing "Add Feeder" and "Reuse Feeder" buttons

**Risk:** ✅ **LOW** - Additive only

---

### Step 4.2: Create Feeder Library Modal

**File:** `resources/views/quotation/v2/_feeder_library_modal.blade.php`

**Features:**
- Modal with search/filter
- Table/list of TemplateType='FEEDER' templates
- Form fields:
  - Select Template (dropdown/table selection)
  - Feeder Name (textbox, pre-filled with template.DefaultFeederName)
  - Feeder Qty (number, default 1, min 1)
- "Apply" button that calls `applyFeederTemplate()`

**Risk:** ✅ **LOW** - New modal only

---

### Step 4.3: Add JavaScript Function

**File:** `resources/views/quotation/v2/panel.blade.php` (in script section)

```javascript
function openFeederLibraryModal(quotationId, panelId) {
    // Load feeder templates via AJAX
    // Show modal with template list
    // On "Apply", call applyFeederTemplate route
}
```

**Risk:** ✅ **LOW** - New JS function only

---

### Step 4.4: Add Controller Method - applyFeederTemplate

**File:** `app/Http/Controllers/QuotationV2Controller.php`

**Method:** `applyFeederTemplate(Request $request, $quotationId, $panelId)`

**Validation:**
- MasterBomId exists, TemplateType='FEEDER', IsActive=1
- FeederName (optional, default from template.DefaultFeederName)
- Qty (numeric, min 1, default 1)

**Logic:**
1. Create new feeder row in `quotation_sale_boms`:
   - `QuotationId` = $quotationId
   - `QuotationSaleId` = $panelId
   - `FeederName` = requested name (or template.DefaultFeederName)
   - `Level` = 0
   - `ParentBomId` = NULL
   - `Qty` = requested Qty (default 1)
   - `Status` = 0

2. For each `master_bom_items` row under this MasterBomId:
   - Create `quotation_sale_bom_items` under this new feeder
   - Use `master_bom_items.Qty` as `ItemQtyPerBom`
   - **DO NOT multiply by feeder Qty or panel Qty** - QuotationQuantityService handles that

3. Return JSON success with new feeder data

**Important Rules:**
- Template represents ONE canonical feeder (Qty=1)
- When applied, create ONE feeder row
- User sets FeederQty on that row as needed
- Do NOT duplicate tree for Qty > 1

**Risk:** ✅ **LOW** - New method, doesn't change existing logic

---

### Step 4.5: Add Route for applyFeederTemplate

**File:** `routes/web.php`

```php
Route::post('/quotation/{quotation}/panel/{panel}/feeder/apply-template', 
    [QuotationV2Controller::class, 'applyFeederTemplate'])
    ->name('quotation.v2.applyFeederTemplate');
```

**Risk:** ✅ **LOW** - New route only

---

## 🔧 PHASE 5: LEGACY DATA INTEGRATION (Virtual Feeders)

### Step 5.1: Enhance V2 Panel Feeder Loading

**File:** `app/Http/Controllers/QuotationV2Controller.php` (panel method)

**Current Logic (around line 85-110):**
- Loads feeders with `Level = 0`
- Handles legacy `Level = NULL`

**Enhancement Needed:**
- If NO Level = 0 rows exist, but BOMs with `ParentBomId = NULL` exist:
  - Treat each as "virtual feeder" (in-memory only)
  - Build tree structure:
    - Virtual Feeder (from top BOM)
      - BOM1 (Level = 1, ParentBomId = virtual feeder id)
      - BOM2 (Level = 2, ParentBomId = BOM1 id)

**Naming Rules:**
- Virtual feeder name = `FeederName` if present
- Else = `BomName` if present
- Else = "Feeder {n}" (1-based index)

**Important:**
- This is IN-MEMORY interpretation only
- Do NOT modify database
- CostingService and QuotationQuantityService must work with this structure

**Risk:** ⚠️ **MEDIUM** - Changes tree building logic
**Mitigation:** Test thoroughly with legacy data

---

## 🔧 PHASE 6: LEGACY STEP PAGE (DEFERRED)

**Status:** ⏸️ **DEFERRED** - Will implement after V2 is fully stable

**Reason:** Medium risk, changes existing workflow

**Future Implementation:**
- Add Feeder section to legacy step page
- Update `getMasterBom()` to require Feeder parent
- Add backward compatibility for Level = NULL BOMs

---

## 📋 EXECUTION CHECKLIST

### Phase 1: Database & Model
- [ ] Create migration: `add_template_fields_to_master_boms`
- [ ] Update `MasterBom` model (fillable, casts, scopes)
- [ ] Run migration
- [ ] Test model scopes

### Phase 2: Feeder Library Backend
- [ ] Create `FeederTemplateController`
- [ ] Implement all CRUD methods
- [ ] Add routes
- [ ] Test API endpoints

### Phase 3: Feeder Library UI
- [ ] Create `index.blade.php` (list view)
- [ ] Create `show.blade.php` (detail view)
- [ ] Create `create.blade.php` (create form)
- [ ] Create `edit.blade.php` (edit form)
- [ ] Add navigation link

### Phase 4: V2 Panel Integration
- [ ] Add "Add Feeder from Library" button
- [ ] Create `_feeder_library_modal.blade.php`
- [ ] Add `openFeederLibraryModal()` JS function
- [ ] Add `applyFeederTemplate()` method
- [ ] Add route for apply template
- [ ] Test end-to-end flow

### Phase 5: Legacy Data Integration
- [ ] Review current V2 panel feeder loading logic
- [ ] Enhance to handle virtual feeders
- [ ] Test with legacy data (Level = NULL BOMs)
- [ ] Verify CostingService still works
- [ ] Verify QuotationQuantityService still works

---

## ⚠️ CRITICAL RULES (NON-NEGOTIABLE)

1. **DO NOT change CostingService or QuotationQuantityService**
   - They are already correct
   - Only use them, don't modify

2. **DO NOT modify existing database records**
   - Virtual feeder interpretation is in-memory only
   - No destructive migrations

3. **Feeder Template = Canonical Qty=1**
   - Library stores one feeder pattern
   - Multiplicity handled by FeederQty in target quotation

4. **Backward Compatibility**
   - Old quotations with Level = NULL BOMs must still work
   - V2 panel must handle both real feeders and virtual feeders

5. **Component Qty from Template**
   - Use `master_bom_items.Qty` as `ItemQtyPerBom`
   - Do NOT multiply by feeder Qty or panel Qty
   - QuotationQuantityService handles multipliers

---

## 🧪 TESTING REQUIREMENTS

### Test 1: Feeder Template Creation
- Create Master BOM with TemplateType='FEEDER'
- Verify it appears in `/feeder-library`
- Verify it's filterable by TemplateType

### Test 2: Apply Feeder Template
- In V2 panel, click "Add Feeder from Library"
- Select a template
- Verify:
  - One new `quotation_sale_boms` row with Level=0
  - Components copied to `quotation_sale_bom_items`
  - FeederQty = 1 (default)
  - FeederName = template.DefaultFeederName (or user input)

### Test 3: Virtual Feeder Interpretation
- Load V2 panel with legacy data (Level = NULL BOMs)
- Verify:
  - Top-level BOMs shown as "virtual feeders"
  - Tree structure correct
  - CostingService calculates correctly
  - QuotationQuantityService calculates correctly

### Test 4: Quantity/Cost Consistency
- Create panel with feeder from library
- Add components
- Verify:
  - EffQtyPerPanel = FeederQty × BomQtyChain × ItemQty
  - TotalQty = PanelQty × EffQtyPerPanel
  - Amount = NetRate × TotalQty
  - Panel cost = sum of component Amounts

---

## 📝 QUESTIONS ANSWERED (LOCKED-IN)

1. **Backward Compatibility:**
   - ✅ New quotations → full V2 with feeders
   - ✅ Old quotations → unchanged, virtual feeder interpretation in-memory only
   - ✅ No auto-migration of existing data

2. **Default Feeder:**
   - ✅ Name = "Feeder 1" (or user input)
   - ✅ Qty = 1.00 (default, user can change)

3. **Implementation Order:**
   - ✅ Phases 1-4 first (Feeder Library + V2 button)
   - ✅ Phase 5 (Legacy integration) after V2 stable
   - ⏸️ Phase 6 (Legacy Step Page) deferred

4. **Migration Strategy:**
   - ✅ No automatic migration now
   - ✅ Virtual feeder interpretation in-memory only
   - ✅ Future: Optional manual migration tool

5. **Feeder Naming:**
   - ✅ Preserve original names from old data
   - ✅ Allow renaming when reusing
   - ✅ Library stores DefaultFeederName for suggestions

6. **Feeder Template Qty:**
   - ✅ Library stores canonical Qty=1
   - ✅ Source Qty > 1 doesn't create multiple templates
   - ✅ Target usage starts with Qty=1, user controls multiplicity

---

## ✅ STATUS

**Analysis:** ✅ **COMPLETE**  
**Plan:** ✅ **REVISED & READY**  
**Code Review:** ✅ **DONE**  
**Execution:** ⏸️ **AWAITING FINAL CONFIRMATION**

**Ready to execute:** ✅ **YES** (after your final confirmation)

---

**Next Step:** Awaiting your final clear idea/confirmation before execution.


