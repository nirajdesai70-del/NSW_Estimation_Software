> Source: source_snapshot/V2_PROPOSAL_BOM_SIDEBAR_AND_AUTO_NAMING_PLAN.md
> Bifurcated into: features/proposal_bom/workflows/V2_PROPOSAL_BOM_SIDEBAR_AND_AUTO_NAMING_PLAN.md
> Module: Proposal BOM > Workflows
> Date: 2025-12-17 (IST)

# Proposal BOM Sidebar & Auto-Naming Standard - Implementation Plan

## 📋 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-11 | Auto | Initial plan | Re-establish Proposal BOM sidebar, implement auto-naming standard |

---

## 🔍 CURRENT STATE ANALYSIS

### ✅ What We Have

1. **Master BOM Sidebar:**
   - ✅ Exists in sidebar (`/masterbom`)
   - ✅ Route: `masterbom.index`
   - ✅ Controller: `MasterBomController`

2. **Feeder Library Sidebar:**
   - ✅ Exists in sidebar (`/feeder-library`)
   - ✅ Route: `feeder-library.index`
   - ✅ Controller: `FeederTemplateController`

3. **Proposal BOM Functionality:**
   - ✅ `applyProposalBom()` method exists
   - ✅ Routes exist: `quotation.v2.applyProposalBom`, `api.reuse.proposalBoms`
   - ✅ Can select Proposal BOM from past quotations
   - ❌ **NO sidebar link** - Missing!

4. **Auto-Naming:**
   - ⚠️ **Partial implementation** - Need to check current state
   - Need to standardize for Panel/Feeder/BOM

### ❌ What We're Missing

1. **Proposal BOM Sidebar Link:**
   - No menu item in sidebar
   - No dedicated Proposal BOM listing page
   - No controller for Proposal BOM management

2. **Auto-Naming Standard:**
   - Not consistently applied
   - Need standard for Panel/Feeder/BOM
   - Need fallback when name not provided

---

## 🎯 REQUIREMENTS

### 1. Re-establish Proposal BOM Sidebar

**Goal:** Add Proposal BOM menu item in sidebar with proper listing page

**What it should show:**
- List of all Proposal BOMs (from `quotation_sale_boms`)
- Filter by quotation, project, customer
- Show BOM details (name, components count, quotation info)
- Allow viewing, reusing, promoting to Master BOM

**Similar to:**
- Master BOM listing (`/masterbom`)
- Feeder Library listing (`/feeder-library`)

---

### 2. Auto-Naming Standard

**Goal:** If engineer doesn't provide name, auto-generate standard name

**Pattern (IMPROVED - More Identifiable):**
- **Prefix Priority (use first available):**
  1. Project Name (if available)
  2. Customer Name (if project not available)
  3. Quotation Subject/Description (if neither available)
  4. Generic (if nothing available)

- **Naming Examples:**
  - **Panel:** "{ProjectName} Panel 1", "{CustomerName} Panel 1", "{QuotationSubject} Panel 1", or "Panel 1" (fallback)
  - **Feeder:** "{ProjectName} Feeder 1", "{CustomerName} Feeder 1", "{QuotationSubject} Feeder 1", or "Feeder 1" (fallback)
  - **BOM 1:** "{ProjectName} BOM 1", "{CustomerName} BOM 1", "{QuotationSubject} BOM 1", or "BOM 1" (fallback)
  - **BOM 2:** "{ProjectName} BOM2-1", "{CustomerName} BOM2-1", "{QuotationSubject} BOM2-1", or "BOM2-1" (fallback)

**Rules:**
- Auto-increment based on existing count in same parent
- If name provided, use it (no auto-generation)
- If name empty/null, generate auto-name with prefix
- Prefix makes names identifiable and less confusing
- Apply globally across all creation points

---

## 📋 IMPLEMENTATION PLAN

### Phase 1: Create Proposal BOM Controller & Views (2-3 hours)

**Goal:** Create Proposal BOM listing page similar to Master BOM

**Tasks:**

1. **Create ProposalBomController:**
   ```php
   // app/Http/Controllers/ProposalBomController.php
   class ProposalBomController extends Controller {
       public function index() {
           // List all Proposal BOMs from quotation_sale_boms
           // Filter by Status = 0
           // Show: BOM Name, Quotation, Project, Customer, Component Count
           // Allow filtering/searching
       }
       
       public function show($id) {
           // Show Proposal BOM details
           // Show components
           // Show quotation context
       }
   }
   ```

2. **Create Views:**
   - `resources/views/proposal-bom/index.blade.php` - Listing page
   - `resources/views/proposal-bom/show.blade.php` - Detail page
   - Use `<x-nepl-table>` component for consistency

3. **Add Routes:**
   ```php
   Route::prefix('proposal-bom')->group(function () {
       Route::get('/', [ProposalBomController::class, 'index'])->name('proposal-bom.index');
       Route::get('/{id}', [ProposalBomController::class, 'show'])->name('proposal-bom.show');
   });
   ```

4. **Add Sidebar Link:**
   ```blade
   <!-- resources/views/layouts/sidebar.blade.php -->
   <li class="nav-item">
       <a href="{{ route('proposal-bom.index') }}">
           <i class="la la-file-text"></i><span class="menu-title">Proposal BOM</span>
       </a>
   </li>
   ```

**Files:**
- `app/Http/Controllers/ProposalBomController.php` (NEW)
- `resources/views/proposal-bom/index.blade.php` (NEW)
- `resources/views/proposal-bom/show.blade.php` (NEW)
- `resources/views/layouts/sidebar.blade.php` (add link)
- `routes/web.php` (add routes)

**Risk:** ⭐⭐ Low-Medium - New feature, doesn't affect existing code

---

### Phase 2: Implement Auto-Naming Service (2-3 hours)

**Goal:** Create centralized auto-naming service for Panel/Feeder/BOM

**Tasks:**

1. **Create AutoNamingService:**
   ```php
   // app/Services/AutoNamingService.php
   class AutoNamingService {
   /**
    * Generate auto name for Panel
    * Pattern: "{Prefix} Panel 1", "{Prefix} Panel 2", ...
    * Prefix priority: Project Name > Customer Name > Quotation Subject > Generic
    */
   public function generatePanelName($quotationId, $providedName = null) {
       if (!empty($providedName) && trim($providedName) !== '') {
           return trim($providedName);
       }
       
       // Get quotation with relationships
       $quotation = Quotation::with(['project', 'client'])->find($quotationId);
       
       // Determine prefix (priority: Project > Customer > Subject > Generic)
       $prefix = $this->getNamingPrefix($quotation);
       
       $existingCount = QuotationSale::where('QuotationId', $quotationId)
           ->where('Status', 0)
           ->count();
       
       return $prefix . ' Panel ' . ($existingCount + 1);
   }
       
   /**
    * Generate auto name for Feeder
    * Pattern: "{Prefix} Feeder 1", "{Prefix} Feeder 2", ...
    * Prefix priority: Project Name > Customer Name > Quotation Subject > Generic
    */
   public function generateFeederName($panelId, $providedName = null) {
       if (!empty($providedName) && trim($providedName) !== '') {
           return trim($providedName);
       }
       
       // Get panel and quotation with relationships
       $panel = QuotationSale::with(['quotation.project', 'quotation.client'])->find($panelId);
       $quotation = $panel->quotation ?? null;
       
       // Determine prefix (priority: Project > Customer > Subject > Generic)
       $prefix = $this->getNamingPrefix($quotation);
       
       $existingCount = QuotationSaleBom::where('QuotationSaleId', $panelId)
           ->where('Level', 0)
           ->where('Status', 0)
           ->count();
       
       return $prefix . ' Feeder ' . ($existingCount + 1);
   }
       
   /**
    * Generate auto name for BOM
    * Pattern: "{Prefix} BOM 1", "{Prefix} BOM 2", ... (for BOM1)
    * Pattern: "{Prefix} BOM2-1", "{Prefix} BOM2-2", ... (for BOM2)
    * Prefix priority: Project Name > Customer Name > Quotation Subject > Generic
    */
   public function generateBomName($parentBomId, $level, $providedName = null) {
       if (!empty($providedName) && trim($providedName) !== '') {
           return trim($providedName);
       }
       
       // Get parent BOM and quotation with relationships
       $parentBom = QuotationSaleBom::with(['quotation.project', 'quotation.client'])->findOrFail($parentBomId);
       $quotation = $parentBom->quotation ?? null;
       
       // Determine prefix (priority: Project > Customer > Subject > Generic)
       $prefix = $this->getNamingPrefix($quotation);
       
       if ($level == 1) {
           // BOM1 under Feeder
           $existingCount = QuotationSaleBom::where('ParentBomId', $parentBomId)
               ->where('Level', 1)
               ->where('Status', 0)
               ->count();
           return $prefix . ' BOM 1' . ($existingCount > 0 ? '-' . ($existingCount + 1) : '');
       } else if ($level == 2) {
           // BOM2 under BOM1
           $existingCount = QuotationSaleBom::where('ParentBomId', $parentBomId)
               ->where('Level', 2)
               ->where('Status', 0)
               ->count();
           return $prefix . ' BOM2-' . ($existingCount + 1);
       }
       
       return $prefix . ' BOM ' . $level;
   }
   
   /**
    * Get naming prefix from quotation
    * Priority: Project Name > Customer Name > Quotation Subject > Empty (generic)
    */
   private function getNamingPrefix($quotation) {
       if (!$quotation) {
           return ''; // Generic (no prefix)
       }
       
       // Priority 1: Project Name
       if ($quotation->project && !empty($quotation->project->Name)) {
           return trim($quotation->project->Name);
       }
       
       // Priority 2: Customer Name (from client relationship)
       // Note: Client model uses 'ClientName' field, not 'Name'
       if ($quotation->client && !empty($quotation->client->ClientName)) {
           return trim($quotation->client->ClientName);
       }
       
       // Priority 3: Quotation Subject/Description
       if (!empty($quotation->Subject)) {
           return trim($quotation->Subject);
       }
       
       // Fallback: Empty (generic naming)
       return '';
   }
   }
   ```

2. **Update Controllers to Use Auto-Naming:**
   - `addPanel()` - Use `AutoNamingService::generatePanelName()`
   - `addFeeder()` - Use `AutoNamingService::generateFeederName()`
   - `addBom()` - Use `AutoNamingService::generateBomName()`
   - `applyFeederTemplate()` - Use auto-naming if name not provided

3. **Update Request Validation:**
   - Make name fields optional (nullable)
   - Auto-generate if not provided

**Files:**
- `app/Services/AutoNamingService.php` (NEW)
- `app/Http/Controllers/QuotationV2Controller.php` (update addPanel, addFeeder, addBom)
- `app/Http/Requests/AddPanelRequest.php` (make SaleCustomName nullable)
- `app/Http/Requests/AddFeederRequest.php` (make FeederName nullable)
- `app/Http/Requests/AddBomRequest.php` (make BomName nullable)

**Risk:** ⭐⭐ Medium - Changes existing creation logic, but backward compatible

---

### Phase 3: Ensure Proposal BOM Links Everywhere (1-2 hours)

**Goal:** Add Proposal BOM links in all relevant places

**Tasks:**

1. **Add Links in V2 Panel:**
   - Already have "Proposal BOM" button in BOM header
   - Verify it works correctly

2. **Add Links in Legacy Step Page:**
   - Already have "Proposal BOM" button
   - Verify it works correctly

3. **Add Links in Proposal BOM Listing:**
   - "View" link → Detail page
   - "Reuse" link → Apply to current quotation
   - "Promote to Master BOM" link (if promotion feature exists)

4. **Add Links in Master BOM Page:**
   - Cross-reference: "See Proposal BOMs using this Master BOM"
   - Show usage count

**Files:**
- `resources/views/proposal-bom/index.blade.php` (add action links)
- `resources/views/proposal-bom/show.blade.php` (add reuse/promote buttons)
- `resources/views/quotation/v2/_bom.blade.php` (verify Proposal BOM button)
- `resources/views/quotation/steppopup.blade.php` (verify Proposal BOM button)

**Risk:** ⭐ Low - Adding links, no logic changes

---

### Phase 4: Standardize Auto-Naming Documentation (1 hour)

**Goal:** Document auto-naming as standard instruction

**Tasks:**

1. **Create Standard Instructions Document:**
   - `V2_AUTO_NAMING_STANDARD.md`
   - Document naming patterns
   - Document when auto-naming applies
   - Document how to override

2. **Add Code Comments:**
   - Document auto-naming in controllers
   - Document in service methods

3. **Update UI Tooltips:**
   - Add tooltips explaining auto-naming
   - "Leave empty for auto-generated name"

**Files:**
- `V2_AUTO_NAMING_STANDARD.md` (NEW)
- Code comments in controllers and service

**Risk:** ⭐ Low - Documentation only

---

## 🔧 STANDARD RULES TO IMPLEMENT

### Rule 1: Auto-Naming Standard (IMPROVED - More Identifiable)

**Prefix Priority (use first available):**
1. **Project Name** (if `ProjectId` exists and project has `Name`)
2. **Customer Name** (if `ClientId` exists and client has `Name`)
3. **Quotation Subject/Description** (if available in quotations table)
4. **Quotation Number** (as fallback identifier)
5. **Generic** (if nothing available - no prefix)

**Naming Pattern:**
- **Panel:** "{Prefix} Panel 1", "{Prefix} Panel 2", ... or "Panel 1" (if no prefix)
- **Feeder:** "{Prefix} Feeder 1", "{Prefix} Feeder 2", ... or "Feeder 1" (if no prefix)
- **BOM 1:** "{Prefix} BOM 1", "{Prefix} BOM 2", ... or "BOM 1" (if no prefix)
- **BOM 2:** "{Prefix} BOM2-1", "{Prefix} BOM2-2", ... or "BOM2-1" (if no prefix)

**Examples:**
- If Project Name = "ABC Building" → "ABC Building Panel 1", "ABC Building Feeder 1"
- If Customer Name = "XYZ Corp" → "XYZ Corp Panel 1", "XYZ Corp Feeder 1"
- If Quotation Subject = "Main Distribution" → "Main Distribution Panel 1"
- If nothing available → "Panel 1", "Feeder 1" (generic)

**Rules:**
- If name provided → Use it (no auto-generation)
- If name empty/null → Generate auto-name with prefix
- Count existing items in same parent for numbering
- Prefix makes names identifiable and less confusing
- Apply globally across all creation methods

**Implementation:**
- Use `AutoNamingService` for all name generation
- `getNamingPrefix()` method determines prefix based on priority
- Apply in all creation methods (`addPanel`, `addFeeder`, `addBom`)
- Document in code comments

---

### Rule 2: Proposal BOM Sidebar

**Menu Item:**
- Add "Proposal BOM" in sidebar (after "Feeder Library")
- Icon: `la la-file-text`
- Route: `/proposal-bom`

**Listing Page:**
- Show all Proposal BOMs from `quotation_sale_boms`
- Filter by: Quotation, Project, Customer, Date
- Columns: BOM Name, Quotation, Project, Customer, Components, Actions
- Actions: View, Reuse, Promote (if applicable)

**Links:**
- Ensure Proposal BOM links work in:
  - V2 Panel (BOM header)
  - Legacy Step Page
  - Proposal BOM listing page
  - Master BOM page (cross-reference)

---

## 📝 DETAILED IMPLEMENTATION

### Step 1: Create ProposalBomController

```php
// app/Http/Controllers/ProposalBomController.php
namespace App\Http\Controllers;

use App\Models\QuotationSaleBom;
use App\Models\Quotation;
use Illuminate\Http\Request;

class ProposalBomController extends Controller
{
    public function index(Request $request)
    {
        $query = QuotationSaleBom::with(['quotation.client', 'quotation.project', 'quotationSale'])
            ->where('Status', 0)
            ->whereNotNull('BomName'); // Only BOMs with names (not just feeders)
        
        // Filter by quotation if provided
        if ($request->has('quotation_id')) {
            $query->where('QuotationId', $request->quotation_id);
        }
        
        // Filter by project if provided
        if ($request->has('project_id')) {
            $query->whereHas('quotation', function($q) use ($request) {
                $q->where('ProjectId', $request->project_id);
            });
        }
        
        // Get component counts
        $proposalBoms = $query->get()->map(function($bom) {
            $bom->component_count = $bom->item()->where('Status', 0)->count();
            return $bom;
        });
        
        return view('proposal-bom.index', compact('proposalBoms'));
    }
    
    public function show($id)
    {
        $bom = QuotationSaleBom::with([
            'quotation.client',
            'quotation.project',
            'quotationSale',
            'item.product',
            'item.make',
            'item.series'
        ])->findOrFail($id);
        
        $items = $bom->item()->where('Status', 0)->get();
        
        return view('proposal-bom.show', compact('bom', 'items'));
    }
}
```

---

### Step 2: Create AutoNamingService

```php
// app/Services/AutoNamingService.php
namespace App\Services;

use App\Models\Quotation;
use App\Models\QuotationSale;
use App\Models\QuotationSaleBom;

class AutoNamingService
{
    /**
     * Generate auto name for Panel
     * 
     * STANDARD RULE: If name not provided, auto-generate with prefix:
     * Pattern: "{Prefix} Panel 1", "{Prefix} Panel 2", ...
     * Prefix priority: Project Name > Customer Name > Quotation Subject/No > Generic
     */
    public function generatePanelName($quotationId, $providedName = null)
    {
        if (!empty($providedName) && trim($providedName) !== '') {
            return trim($providedName);
        }
        
        // Get quotation with relationships
        $quotation = Quotation::with(['project', 'client'])->find($quotationId);
        
        // Determine prefix (priority: Project > Customer > Subject/No > Generic)
        $prefix = $this->getNamingPrefix($quotation);
        
        $existingCount = QuotationSale::where('QuotationId', $quotationId)
            ->where('Status', 0)
            ->count();
        
        $name = 'Panel ' . ($existingCount + 1);
        return $prefix ? $prefix . ' ' . $name : $name;
    }
    
    /**
     * Generate auto name for Feeder
     * 
     * STANDARD RULE: If name not provided, auto-generate with prefix:
     * Pattern: "{Prefix} Feeder 1", "{Prefix} Feeder 2", ...
     * Prefix priority: Project Name > Customer Name > Quotation Subject/No > Generic
     */
    public function generateFeederName($panelId, $providedName = null)
    {
        if (!empty($providedName) && trim($providedName) !== '') {
            return trim($providedName);
        }
        
        // Get panel and quotation with relationships
        $panel = QuotationSale::with(['quotation.project', 'quotation.client'])->find($panelId);
        $quotation = $panel->quotation ?? null;
        
        // Determine prefix (priority: Project > Customer > Subject/No > Generic)
        $prefix = $this->getNamingPrefix($quotation);
        
        $existingCount = QuotationSaleBom::where('QuotationSaleId', $panelId)
            ->where('Level', 0)
            ->where('Status', 0)
            ->count();
        
        $name = 'Feeder ' . ($existingCount + 1);
        return $prefix ? $prefix . ' ' . $name : $name;
    }
    
    /**
     * Generate auto name for BOM
     * 
     * STANDARD RULE: If name not provided, auto-generate with prefix:
     * Pattern: "{Prefix} BOM 1", "{Prefix} BOM 2", ... (for BOM1)
     * Pattern: "{Prefix} BOM2-1", "{Prefix} BOM2-2", ... (for BOM2)
     * Prefix priority: Project Name > Customer Name > Quotation Subject/No > Generic
     */
    public function generateBomName($parentBomId, $level, $providedName = null)
    {
        if (!empty($providedName) && trim($providedName) !== '') {
            return trim($providedName);
        }
        
        // Get parent BOM and quotation with relationships
        $parentBom = QuotationSaleBom::with(['quotation.project', 'quotation.client'])->findOrFail($parentBomId);
        $quotation = $parentBom->quotation ?? null;
        
        // Determine prefix (priority: Project > Customer > Subject/No > Generic)
        $prefix = $this->getNamingPrefix($quotation);
        
        if ($level == 1) {
            // BOM1 under Feeder
            $existingCount = QuotationSaleBom::where('ParentBomId', $parentBomId)
                ->where('Level', 1)
                ->where('Status', 0)
                ->count();
            
            $name = 'BOM 1' . ($existingCount > 0 ? '-' . ($existingCount + 1) : '');
            return $prefix ? $prefix . ' ' . $name : $name;
        } else if ($level == 2) {
            // BOM2 under BOM1
            $existingCount = QuotationSaleBom::where('ParentBomId', $parentBomId)
                ->where('Level', 2)
                ->where('Status', 0)
                ->count();
            
            $name = 'BOM2-' . ($existingCount + 1);
            return $prefix ? $prefix . ' ' . $name : $name;
        }
        
        // Fallback
        $name = 'BOM ' . $level;
        return $prefix ? $prefix . ' ' . $name : $name;
    }
    
    /**
     * Get naming prefix from quotation
     * 
     * Priority order:
     * 1. Project Name (if ProjectId exists and project has Name)
     * 2. Customer Name (if ClientId exists and client has Name)
     * 3. Quotation Subject/Description (if available)
     * 4. Quotation Number (if available)
     * 5. Empty string (generic naming - no prefix)
     * 
     * @param Quotation|null $quotation
     * @return string
     */
    private function getNamingPrefix($quotation)
    {
        if (!$quotation) {
            return ''; // Generic (no prefix)
        }
        
        // Priority 1: Project Name
        if ($quotation->project && !empty($quotation->project->Name)) {
            return trim($quotation->project->Name);
        }
        
        // Priority 2: Customer Name (from client relationship)
        // Note: Client model uses 'ClientName' field, not 'Name'
        if ($quotation->client && !empty($quotation->client->ClientName)) {
            return trim($quotation->client->ClientName);
        }
        
        // Priority 3: Quotation Subject/Description (if field exists)
        // Note: Check if quotations table has Subject or Description field
        if (isset($quotation->Subject) && !empty($quotation->Subject)) {
            return trim($quotation->Subject);
        }
        if (isset($quotation->Description) && !empty($quotation->Description)) {
            return trim($quotation->Description);
        }
        
        // Priority 4: Quotation Number (as fallback identifier)
        if (!empty($quotation->QuotationNo)) {
            return trim($quotation->QuotationNo);
        }
        
        // Fallback: Empty (generic naming)
        return '';
    }
}
```

---

### Step 3: Update Controllers

**Update `addPanel()`:**
```php
use App\Services\AutoNamingService;

public function addPanel(AddPanelRequest $request, $quotationId)
{
    $autoNaming = app(AutoNamingService::class);
    $panelName = $autoNaming->generatePanelName($quotationId, $request->SaleCustomName);
    
    $panel = QuotationSale::create([
        'QuotationId' => $quotationId,
        'SaleCustomName' => $panelName, // Use auto-generated if not provided
        // ... rest
    ]);
}
```

**Update `addFeeder()`:**
```php
public function addFeeder(AddFeederRequest $request, $quotationId, $panelId)
{
    $autoNaming = app(AutoNamingService::class);
    $feederName = $autoNaming->generateFeederName($panelId, $request->FeederName);
    
    $feeder = QuotationSaleBom::create([
        // ...
        'FeederName' => $feederName, // Use auto-generated if not provided
        // ...
    ]);
}
```

**Update `addBom()`:**
```php
public function addBom(AddBomRequest $request, $quotationId, $parentBomId)
{
    $autoNaming = app(AutoNamingService::class);
    $bomName = $autoNaming->generateBomName($parentBomId, $request->Level, $request->BomName);
    
    $bom = QuotationSaleBom::create([
        // ...
        'BomName' => $bomName, // Use auto-generated if not provided
        // ...
    ]);
}
```

---

## 📋 FILES TO CREATE/MODIFY

### New Files:
1. `app/Http/Controllers/ProposalBomController.php`
2. `app/Services/AutoNamingService.php`
3. `resources/views/proposal-bom/index.blade.php`
4. `resources/views/proposal-bom/show.blade.php`
5. `V2_AUTO_NAMING_STANDARD.md`

### Modified Files:
1. `resources/views/layouts/sidebar.blade.php` (add Proposal BOM link)
2. `app/Http/Controllers/QuotationV2Controller.php` (use AutoNamingService)
3. `app/Http/Requests/AddPanelRequest.php` (make SaleCustomName nullable)
4. `app/Http/Requests/AddFeederRequest.php` (make FeederName nullable)
5. `app/Http/Requests/AddBomRequest.php` (make BomName nullable)
6. `routes/web.php` (add Proposal BOM routes)

---

## ✅ TESTING CHECKLIST

- [ ] Proposal BOM appears in sidebar
- [ ] Proposal BOM listing page loads correctly
- [ ] Proposal BOM detail page shows components
- [ ] Proposal BOM links work from V2 panel
- [ ] Proposal BOM links work from legacy step page
- [ ] Auto-naming works for Panel (if name not provided)
- [ ] Auto-naming works for Feeder (if name not provided)
- [ ] Auto-naming works for BOM (if name not provided)
- [ ] Manual names still work (if name provided)
- [ ] Auto-naming increments correctly

---

## 🎯 IMPLEMENTATION ORDER

1. **Phase 1: Proposal BOM Sidebar** (2-3 hours)
   - Create controller and views
   - Add sidebar link
   - Test listing page

2. **Phase 2: Auto-Naming Service** (2-3 hours)
   - Create service
   - Update controllers
   - Test auto-naming

3. **Phase 3: Links Everywhere** (1-2 hours)
   - Verify all links work
   - Add missing links

4. **Phase 4: Documentation** (1 hour)
   - Document standard
   - Add code comments

**Total: 6-9 hours**

---

## ⚠️ RISKS & MITIGATION

### Risk 1: Breaking Existing Names
**Mitigation:**
- Auto-naming only applies if name is empty/null
- Existing names preserved
- Backward compatible

### Risk 2: Performance on Listing
**Mitigation:**
- Use eager loading
- Add pagination
- Add indexes if needed

---

## ✅ BENEFITS

1. **Proposal BOM Visibility:** Engineers can see all Proposal BOMs in one place
2. **Reusability:** Easy to find and reuse Proposal BOMs
3. **Auto-Naming:** Consistent naming when engineers don't provide names
4. **Standard Rules:** Clear instructions for naming
5. **Better Organization:** Proper sidebar structure

---

## 🎉 SUMMARY

**Two main tasks:**
1. ✅ Re-establish Proposal BOM sidebar (controller, views, routes, sidebar link)
2. ✅ Implement auto-naming standard (service, apply to Panel/Feeder/BOM, document)

**Both are valuable and should be implemented!**

Ready to proceed? Start with Phase 1 (Proposal BOM Sidebar) or Phase 2 (Auto-Naming)?


