> Source: source_snapshot/PROPOSAL_BOM_ENHANCEMENT_PLAN.md
> Bifurcated into: features/proposal_bom/workflows/PROPOSAL_BOM_ENHANCEMENT_PLAN.md
> Module: Proposal BOM > Workflows
> Date: 2025-12-17 (IST)

# Proposal BOM Enhancement Plan

## 📋 Overview

This document outlines the plan to:
1. Apply all Master BOM corrections to Proposal BOM (same tree + pricing logic)
2. Add **optional** enhanced search functionality for Proposal BOM with partial matching
3. Ensure Proposal BOM import works independently of search (search is helper, not requirement)

**CORE PRINCIPLE:** Search is optional sugar - never a gate. Proposal BOMs must be usable without search.

---

## 1️⃣ Part 1: Apply Master BOM Fixes to Proposal BOM

### Current Issues to Fix:
- ✅ Primary key handling (if any models use `id` instead of custom keys)
- ✅ Description null handling
- ✅ Error handling and validation
- ✅ Same applyMasterBom logic for Proposal BOM

### Files to Update:
1. `app/Http/Controllers/QuotationV2Controller.php`
   - Create `applyProposalBom()` method (similar to `applyMasterBom()`)
   - Handle Proposal BOM application (type=2 uses `QuotationSaleBomId` instead of `MasterBomId`)
   - Copy items from source BOM to target BOM

2. `resources/views/quotation/v2/panel.blade.php`
   - Update `selectProposalBom()` to show same modal structure as Master BOM
   - Add "Save & Apply" button for Proposal BOM
   - Wire up `applyProposalBomToFeeder()` function

3. `app/Http/Controllers/QuotationController.php`
   - Review `getProposalBomVal()` for same fixes applied to `getMasterBomVal()`

---

## 2️⃣ Part 2: Enhanced Search for Proposal BOM (OPTIONAL HELPER)

### ⚠️ CRITICAL REQUIREMENT: Search is Optional, Never Mandatory

**Design Rules:**
1. **Search is optional sugar** - Proposal BOM must work without search
2. **Default list on open** - User must see list immediately without typing
3. **No validation blocking** - Never require search terms to apply BOM
4. **Graceful degradation** - If search fails, show fallback list and continue

### Requirements:
- **Multi-level Filter Search**: Search across Customer → Project → Panel → Feeder → BOM
- **Partial Matching**: Search with indicative words using LIKE '%term%'
- **Examples**:
  - "amans" → Shows all clients with "amans" in name
  - "vfd" → Shows all panels with "vfd" in name
  - "132 kw" → Shows all feeders with "132 kw" in name
- **Real-time Search**: As user types, filter the dropdown options
- **Default List**: Show last 50 active Proposal BOMs when dropdown opens (no typing required)

### Technical Approach:

#### Option A: Select2 with AJAX Search (Recommended - IMPLEMENT THIS)
**How it works:**
1. Replace static dropdown with Select2 AJAX
2. Create new API endpoint: `GET /api/proposal-bom/search?q=term`
3. **On dropdown open:** Load default 50 results immediately (no typing required)
4. **As user types:** Send search query to API (minimumInputLength = 2 for typing only)
5. API searches across multiple fields using LIKE queries
6. Return filtered results with formatted display text
7. Select2 shows filtered options in real-time

**API Behavior:**
```php
// If q is empty → return default 50 Proposal BOMs (recent/active)
// If q is not empty → filter using LIKE %term%
```

**Search Fields (Partial Matching with LIKE '%term%'):**
```sql
WHERE qsb.Status = 0 AND (
  clients.ClientName LIKE '%q%' OR
  projects.Name LIKE '%q%' OR
  quotation_sales.SaleCustomName LIKE '%q%' OR
  quotation_sale_boms.FeederName LIKE '%q%' OR
  quotation_sale_boms.BomName LIKE '%q%' OR
  quotations.QuotationNo LIKE '%q%'
)
LIMIT 50
```

**Display Format (Single Line):**
```
<BOM Name> — <Panel Name> — <Project Name> — <Client Name> — <Quotation No>
Example: "Starter BOM — VFD PANEL 15KW — Factory Phase-1 — Amans Ltd — QT-2024-001"
```

**Failure Handling:**
- If API fails → Show toast "Search unavailable - showing default list"
- Load fallback static list (server-side generated)
- Never block user from continuing

#### Option B: Multi-Field Search Form (Alternative)
**How it works:**
1. Add search form above Proposal BOM dropdown
2. Separate fields: Client, Project, Panel, Feeder
3. User fills in any combination of fields
4. Filter dropdown options based on entered values
5. All fields support partial matching

**Pros:**
- More structured search
- Clear what each field filters
- Easy to understand

**Cons:**
- Takes more screen space
- Requires more clicks

---

## 3️⃣ Implementation Details

### Step 1: Fix Proposal BOM Apply Logic (Core Function - Independent of Search)

**Core Principle:** Proposal BOM import must work even if search is not used.

**New Route:**
```php
Route::post('quotation/v2/apply-proposal-bom', [QuotationV2Controller::class, 'applyProposalBom'])
    ->name('quotation.v2.applyProposalBom');
```

**New Method: `applyProposalBom()`**
- Accepts: `QuotationId`, `QuotationSaleBomId` (target), `SourceQuotationSaleBomId` (source)
- **Tree Integration:**
  - If applied under Feeder → create BOM L1 with correct Level, ParentBomId
  - If applied under BOM → create BOM L2 with correct Level, ParentBomId
  - Preserve: FeederName, BomName, Level, ParentBomId
- Loads items from source BOM (`getProposalBomVal`)
- Creates items in target BOM
- **Phase 1 Pricing Logic:**
  - Preserve RateSource from source
  - If price exists → set IsPriceConfirmed = 1
  - If price = 0 → IsPriceConfirmed = 0 (warning displayed)
  - Handle Description null (same fixes as Master BOM)

### Step 2: Create Enhanced Search API (OPTIONAL HELPER)

**⚠️ IMPORTANT:** This API is optional helper - Proposal BOM import must work without it.

**New Route:**
```php
Route::get('api/proposal-bom/search', [QuotationController::class, 'searchProposalBom'])
    ->name('api.proposalBom.search');
```

**New Method: `searchProposalBom(Request $request)`**

**CRITICAL BEHAVIOR:**
- If `q` (search term) is empty → Return default 50 Proposal BOMs (recent/active)
- If `q` is not empty → Filter using LIKE '%term%' across all fields
- Never require search term to return results

```php
public function searchProposalBom(Request $request) {
    $search = $request->input('q', ''); // Search query from Select2
    $searchTerm = '%' . $search . '%';
    
    $query = "
        SELECT 
            qsb.QuotationSaleBomId,
            CONCAT(
                COALESCE(qsb.BomName, qsb.MasterBomName, mb.Name, 'Unnamed'), ' — ',
                COALESCE(qs.SaleCustomName, ''), ' — ',
                p.Name, ' — ',
                c.ClientName, ' — ',
                q.QuotationNo
            ) as text
        FROM quotation_sale_boms qsb
        LEFT JOIN master_boms mb ON qsb.MasterBomId = mb.MasterBomId
        JOIN quotation_sales qs ON qs.QuotationSaleId = qsb.QuotationSaleId
        JOIN quotations q ON q.QuotationId = qsb.QuotationId
        JOIN projects p ON p.ProjectId = q.ProjectId
        JOIN clients c ON c.ClientId = q.ClientId
        WHERE qsb.Status = 0
    ";
    
    $params = [];
    if (!empty($search)) {
        // Apply partial matching filters
        $query .= " AND (
            c.ClientName LIKE ? OR
            p.Name LIKE ? OR
            qs.SaleCustomName LIKE ? OR
            qsb.FeederName LIKE ? OR
            qsb.BomName LIKE ? OR
            q.QuotationNo LIKE ?
        )";
        $params = array_fill(0, 6, $searchTerm);
    }
    
    $query .= " ORDER BY qsb.updated_at DESC LIMIT 50";
    
    $results = DB::select($query, $params);
    
    // Format for Select2
    $formatted = array_map(function($item) {
        return [
            'id' => $item->QuotationSaleBomId,
            'text' => $item->text
        ];
    }, $results);
    
    return response()->json(['results' => $formatted]);
}
```

**Frontend: Select2 AJAX Configuration**

**CRITICAL:** Must show default list on open, not force typing.

```javascript
$('#proposalBomSelect').select2({
    ajax: {
        url: '/api/proposal-bom/search',
        dataType: 'json',
        delay: 300, // Debounce typing
        data: function (params) {
            return {
                q: params.term || '', // Search term (empty string if no input)
                page: params.page
            };
        },
        processResults: function (data) {
            return {
                results: data.results || []
            };
        },
        cache: true,
        // Load default list immediately on open
        transport: function (params, success, failure) {
            var $request = $.ajax(params);
            $request.then(success);
            $request.fail(function(xhr) {
                // If API fails, show warning but don't block
                console.warn('Search API failed, using fallback');
                toastr.warning('Search unavailable - showing default list', 'Info');
                // Load fallback list or use empty results
                success({results: []});
            });
            return $request;
        }
    },
    placeholder: 'Search by Client, Project, Panel, Feeder, BOM, or Quotation No...',
    minimumInputLength: 0, // Allow opening without typing
    width: '100%',
    // Load default list when dropdown opens (even without typing)
    language: {
        inputTooShort: function() {
            return 'Type to search or select from list...';
        }
    }
});

// Load default list immediately when Select2 opens
$('#proposalBomSelect').on('select2:open', function() {
    // Trigger initial load if no data loaded yet
    var $select = $(this);
    if ($select.find('option').length <= 1) {
        // Manually trigger AJAX load for empty search
        $select.select2('open');
        $.ajax({
            url: '/api/proposal-bom/search',
            data: { q: '' },
            success: function(data) {
                if (data.results && data.results.length > 0) {
                    data.results.forEach(function(item) {
                        var option = new Option(item.text, item.id, false, false);
                        $select.append(option);
                    });
                    $select.trigger('change');
                }
            }
        });
    }
});
```

**Alternative Simpler Approach (Recommended):**
- Pre-load default list server-side in the modal
- Then enhance with AJAX search when user types
- This guarantees list is always available

---

## 4️⃣ Search Examples & User Flow

### Flow 1: User Opens Dropdown Without Typing (Default List)
- **User clicks:** Proposal BOM dropdown
- **System:** Immediately loads last 50 active Proposal BOMs
- **User:** Sees list, selects one, continues
- **Result:** Works perfectly without any search typing

### Flow 2: User Types to Filter (Optional Enhancement)
- **User types:** "amans"
- **System searches:** `clients.ClientName LIKE '%amans%'` (partial match)
- **Results:** All Proposal BOMs from clients with "amans" in name
- **Display:** "Starter BOM — VFD PANEL — Factory — **Amans** Ltd — QT-2024-001"

### Example 2: Search by Panel
- **User types:** "vfd"
- **System searches:** `quotation_sales.SaleCustomName LIKE '%vfd%'` (partial match)
- **Results:** All Proposal BOMs from panels with "vfd" in name
- **Display:** "Starter BOM — **VFD Panel** 15KW — Factory — XYZ Corp — QT-2024-002"

### Example 3: Search by Feeder
- **User types:** "132 kw"
- **System searches:** `quotation_sale_boms.FeederName LIKE '%132 kw%'` (partial match)
- **Results:** All Proposal BOMs from feeders with "132 kw" in name
- **Display:** "Motor Starter — Motor Control Panel — **132 KW Feeder** — Factory — ABC Corp — QT-2024-003"

### Example 4: Multi-field Search (Searches All Fields)
- **User types:** "amans"
- **System searches:** ClientName, ProjectName, PanelName, FeederName, BOMName, QuotationNo (any field)
- **Results:** All matching Proposal BOMs regardless of which field matched
- **Display:** Shows all results matching "amans" anywhere in the hierarchy

### Flow 3: API Failure Handling
- **User clicks:** Proposal BOM dropdown
- **System:** API call fails (network error, 500, etc.)
- **System shows:** Toast "Search unavailable - showing default list"
- **System loads:** Fallback static list (pre-loaded server-side)
- **User:** Can still select and continue (not blocked)

---

## 5️⃣ Database Query Optimization

### Indexes to Add (if not exists):
```sql
-- For faster client name searches
CREATE INDEX idx_clients_clientname ON clients(ClientName);

-- For faster project name searches  
CREATE INDEX idx_projects_name ON projects(Name);

-- For faster panel name searches
CREATE INDEX idx_quotation_sales_salecustomname ON quotation_sales(SaleCustomName);

-- For faster feeder/BOM name searches
CREATE INDEX idx_quotation_sale_boms_feedername ON quotation_sale_boms(FeederName);
CREATE INDEX idx_quotation_sale_boms_bomname ON quotation_sale_boms(BomName);

-- For faster quotation number searches
CREATE INDEX idx_quotations_quotationno ON quotations(QuotationNo);
```

---

## 6️⃣ UI/UX Considerations

### Search Input Behavior:
1. **Minimum Characters:** Start searching after 2-3 characters (to avoid too many results)
2. **Debouncing:** Wait 300ms after user stops typing before searching
3. **Loading Indicator:** Show spinner while searching
4. **No Results Message:** "No Proposal BOMs found matching '{search term}'"
5. **Result Limit:** Show max 50 results per search (with pagination if needed)

### Display Format Options:

**Option 1: Single Line (Current)**
```
BOM Name - Panel Name - Project Name - Client Name - Quotation No
```

**Option 2: Multi-Line (More Readable)**
```
BOM Name
Panel Name | Project Name | Client Name
Quotation No
```

**Option 3: With Badges**
```
[Badge: Client] Client Name
[Badge: Project] Project Name  
[Badge: Panel] Panel Name
BOM Name - Quotation No
```

**Recommendation:** Start with Option 1, can enhance later

---

## 7️⃣ Implementation Steps

### Phase 1: Fix Proposal BOM Core (Apply Same Corrections)
**Priority: HIGH - Must work independently of search**

1. ✅ Create `applyProposalBom()` method in QuotationV2Controller
   - Copy tree with correct Level, ParentBomId
   - Handle Description null (same fixes as Master BOM)
   - Preserve RateSource, IsClientSupplied, IsPriceConfirmed
   - Apply Phase 1 pricing logic

2. ✅ Update `selectProposalBom()` to use same modal structure as Master BOM
   - Remove Custom Name field (V2 requirement)
   - Add "Save & Apply" button
   - Wire up `applyProposalBomToFeeder()` function

3. ✅ Update `getProposalBomVal()` to use same fixes as `getMasterBomVal()`
   - Product validation (check exists)
   - Description fallback handling

4. ✅ Test Proposal BOM application works same as Master BOM
   - Works without search
   - Works with search
   - Proper tree structure
   - Proper pricing flags

### Phase 2: Add Enhanced Search (Optional Helper)
**Priority: MEDIUM - Nice to have, but not required**

1. ✅ Create `searchProposalBom()` API endpoint
   - Empty search → return default 50 results
   - Non-empty search → filter with LIKE %term%
   - Return Select2-compatible JSON

2. ✅ Add database indexes for faster searches (if not exists)
   - ClientName, ProjectName, SaleCustomName, FeederName, BomName, QuotationNo

3. ✅ Update Proposal BOM modal to use Select2 AJAX
   - Load default list on open (no typing required)
   - Update list as user types (minimumInputLength = 2 for typing only)
   - Graceful failure handling

4. ✅ Test search with various terms
   - Empty search → shows default list
   - Partial terms → filters correctly
   - API failure → shows fallback

5. ✅ Add loading indicators and error handling
   - Show spinner while searching
   - Show fallback if API fails
   - Never block user

### Phase 3: Polish & Optimization (Optional)
**Priority: LOW - Enhancements only**

1. ✅ Optimize search query performance
2. ✅ Add result highlighting (bold matching terms) - Optional
3. ✅ Add search history/suggestions - Optional
4. ✅ User testing and feedback

---

## 8️⃣ Final Specifications (Locked-In Decisions)

### ✅ Confirmed Decisions:

1. **Search Approach:** Option A (Select2 AJAX) - **CONFIRMED**
   - Single search box
   - Real-time filtering
   - Default list on open (no typing required)
   - Partial matching with LIKE '%term%'

2. **Display Format:** Single-line format - **CONFIRMED**
   ```
   <BOM Name> — <Panel Name> — <Project Name> — <Client Name> — <Quotation No>
   ```

3. **Search Scope:** Main fields only - **CONFIRMED**
   - ClientName, ProjectName, PanelName (SaleCustomName), FeederName, BomName, QuotationNo
   - Component descriptions/categories: NOT included (can add later if needed)

4. **Result Limit:** 50 results maximum - **CONFIRMED**
   - Ordered by most recent (updated_at DESC)
   - Pagination: Optional enhancement later

5. **Minimum Characters:** 0 for default list, 2 for typing - **CONFIRMED**
   - Dropdown open → Load default list immediately
   - User types 2+ chars → Filter results

6. **Core Principle:** Search is optional helper - **CONFIRMED**
   - Proposal BOM import must work without search
   - Search failure → Show fallback, never block user
   - Default list always available

---

## 9️⃣ Estimated Impact

### Benefits:
- ✅ Faster to find relevant Proposal BOMs
- ✅ No need to scroll through long lists
- ✅ Can search by any part of the hierarchy
- ✅ Partial matching makes search forgiving

### Performance:
- ⚠️ Search queries may be slower with large datasets
- ✅ Indexes will help
- ✅ Limit results to 50 per search
- ✅ Cache frequently searched terms

---

## ✅ Implementation Priority

### MUST DO (Phase 1):
1. ✅ Fix Proposal BOM core functionality
   - Same corrections as Master BOM
   - Works independently of search
   - Proper tree structure (Level, ParentBomId)
   - Phase 1 pricing logic

### SHOULD DO (Phase 2):
2. ✅ Add optional search helper
   - Makes finding Proposal BOMs easier
   - But not required for core functionality

### NICE TO HAVE (Phase 3):
3. ✅ Enhancements and polish
   - Result highlighting
   - Search suggestions
   - Performance optimization

---

## 📋 Cursor Implementation Instructions

**Copy-paste this block to Cursor:**

```
PART A — Core Rules (Must Follow Exactly)

1. Proposal BOM import must NOT depend on search
   • Core function: applyProposalBom(sourceBomId, targetBomIdOrFeederId)
   • It should work even if no search is used
   • As long as user selects a BOM ID, the tree must copy correctly

2. Search is optional — never required
   • The user must be able to open the dropdown and choose from a default list without typing anything
   • Empty search → return last 50 active Proposal BOMs
   • No validation should block Apply because no filter is typed
   • If search API fails → show a fallback list and continue

3. Search must support partial matches
   Use %term% matching on: client name, project name, panel name, feeder name, BOM name, quotation no
   Return 50 results maximum

4. Display format: <BOM Name> — <Panel Name> — <Project> — <Client> — <Quotation No>

5. Select2 AJAX: minimumInputLength = 0 (allow opening without typing), load default list on open

PART B — Implementation Steps

1. Create applyProposalBom() method (copy tree with Level, ParentBomId, pricing logic)
2. Create searchProposalBom() API (empty q = default list, non-empty = filtered)
3. Update Proposal BOM modal to use Select2 AJAX with default list on open
4. Add failure handling (fallback list if API fails)

PART C — Tree Integration

When applying Proposal BOM:
- Preserve FeederName, BomName, Level, ParentBomId
- Components inherit Phase 1 pricing logic (RateSource, IsClientSupplied, IsPriceConfirmed)
- Handle Description null (same fixes as Master BOM)
```

---

**Status:** ✅ Plan Updated & Ready for Implementation  
**Updated:** December 2024  
**Key Changes:** Search marked as optional, default list required, failure handling added

