> Source: source_snapshot/PROPOSAL_BOM_MULTI_FILTER_PROPOSAL.md
> Bifurcated into: features/proposal_bom/validation/PROPOSAL_BOM_MULTI_FILTER_PROPOSAL.md
> Module: Proposal BOM > Validation
> Date: 2025-12-17 (IST)

# Proposal BOM Multi-Filter Search Proposal

## 📋 Current Issue

The Select2 dropdown is blocking typing in the search box. User wants separate filter fields for better control.

---

## 🎯 Proposed Solution: Multi-Field Filter Form

Instead of a single search box, provide **separate filter fields** that can be used independently or together.

---

## 📐 UI Design Option

### Option A: Horizontal Filter Bar (Recommended)

```
┌─────────────────────────────────────────────────────────────┐
│ Select Proposal BOM                                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Client:  [________________]  Panel:  [________________]   │
│                                                               │
│  Feeder:  [________________]  BOM:    [________________]     │
│                                                               │
│  [🔍 Search]  [🔄 Clear]                                    │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ Results: (50 found)                                          │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ☐ feeder out — mcc 1 — test panel — Arcelor...        │ │
│ │ ☐ Unnamed — mcc 1 — test panel — Arcelor...           │ │
│ │ ☐ MCCB INCOMER — mcc 1 — test panel — Arcelor...      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  [Cancel]  [Save & Apply]                                    │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- 4 separate input fields (Client, Panel, Feeder, BOM)
- Each field supports partial matching
- "Search" button to apply filters
- "Clear" button to reset all filters
- Results list below with checkboxes
- Can select multiple BOMs if needed

---

### Option B: Vertical Stack Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Select Proposal BOM                                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Client:                                                      │
│  [________________________________]                          │
│                                                               │
│  Panel (Item):                                                │
│  [________________________________]                          │
│                                                               │
│  Feeder:                                                      │
│  [________________________________]                          │
│                                                               │
│  BOM Name:                                                    │
│  [________________________________]                          │
│                                                               │
│  [🔍 Search]  [🔄 Clear]                                    │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ Results: (50 found)                                          │
│ [Results list here]                                          │
│                                                               │
│  [Cancel]  [Save & Apply]                                    │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Cleaner vertical layout
- More space for each field
- Easier to read labels
- Same functionality as Option A

---

### Option C: Accordion/Collapsible Filters

```
┌─────────────────────────────────────────────────────────────┐
│ Select Proposal BOM                                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [▼] Advanced Filters                                        │
│                                                               │
│  Client:  [________________]                                │
│  Panel:   [________________]                                │
│  Feeder:  [________________]                                │
│  BOM:     [________________]                                │
│                                                               │
│  [🔍 Search]  [🔄 Clear]                                    │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│ Results: (50 found)                                          │
│ [Results list here]                                          │
│                                                               │
│  [Cancel]  [Save & Apply]                                    │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Filters can be collapsed to save space
- Quick search still available when collapsed
- Expand for detailed filtering

---

## 🔍 How It Works

### Filter Behavior:

1. **Client Filter:**
   - Type: "amans" → Shows all BOMs from clients with "amans" in name
   - Partial matching: `WHERE ClientName LIKE '%amans%'`

2. **Panel Filter:**
   - Type: "vfd" → Shows all BOMs from panels with "vfd" in name
   - Partial matching: `WHERE SaleCustomName LIKE '%vfd%'`

3. **Feeder Filter:**
   - Type: "132 kw" → Shows all BOMs from feeders with "132 kw" in name
   - Partial matching: `WHERE FeederName LIKE '%132 kw%'`

4. **BOM Filter:**
   - Type: "starter" → Shows all BOMs with "starter" in BOM name
   - Partial matching: `WHERE BomName LIKE '%starter%' OR MasterBomName LIKE '%starter%'`

### Combined Filters:

- If user fills multiple fields → **AND** logic (all conditions must match)
- Example: Client="amans" + Panel="vfd" → Shows BOMs from "amans" clients AND "vfd" panels

### Search Button:

- Click "Search" → Applies all filters and shows results
- Results update in real-time below

### Clear Button:

- Resets all filter fields
- Shows default list (last 50 active BOMs)

---

## 💻 Technical Implementation

### Backend API:

**Route:** `GET /api/proposal-bom/search`

**Parameters:**
```php
[
    'client' => 'amans',      // Optional
    'panel' => 'vfd',         // Optional
    'feeder' => '132 kw',     // Optional
    'bom' => 'starter'        // Optional
]
```

**SQL Query:**
```sql
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
    AND (c.ClientName LIKE '%client%' OR :client IS NULL)
    AND (qs.SaleCustomName LIKE '%panel%' OR :panel IS NULL)
    AND (qsb.FeederName LIKE '%feeder%' OR :feeder IS NULL)
    AND (qsb.BomName LIKE '%bom%' OR qsb.MasterBomName LIKE '%bom%' OR :bom IS NULL)
ORDER BY qsb.updated_at DESC
LIMIT 50
```

### Frontend:

**HTML Structure:**
```html
<div class="modal-body">
    <!-- Filter Form -->
    <div class="row mb-3">
        <div class="col-md-6">
            <label>Client:</label>
            <input type="text" id="filterClient" class="form-control" placeholder="Search by client name...">
        </div>
        <div class="col-md-6">
            <label>Panel (Item):</label>
            <input type="text" id="filterPanel" class="form-control" placeholder="Search by panel name...">
        </div>
    </div>
    <div class="row mb-3">
        <div class="col-md-6">
            <label>Feeder:</label>
            <input type="text" id="filterFeeder" class="form-control" placeholder="Search by feeder name...">
        </div>
        <div class="col-md-6">
            <label>BOM Name:</label>
            <input type="text" id="filterBom" class="form-control" placeholder="Search by BOM name...">
        </div>
    </div>
    <div class="row mb-3">
        <div class="col-md-12 text-right">
            <button type="button" class="btn btn-primary" onclick="searchProposalBoms()">
                <i class="la la-search"></i> Search
            </button>
            <button type="button" class="btn btn-secondary" onclick="clearFilters()">
                <i class="la la-refresh"></i> Clear
            </button>
        </div>
    </div>
    
    <!-- Results List -->
    <div id="proposalBomResults">
        <p class="text-muted">Click "Search" to find Proposal BOMs</p>
    </div>
</div>
```

**JavaScript:**
```javascript
function searchProposalBoms() {
    var filters = {
        client: $('#filterClient').val(),
        panel: $('#filterPanel').val(),
        feeder: $('#filterFeeder').val(),
        bom: $('#filterBom').val()
    };
    
    $.ajax({
        url: '{{ route('api.proposalBom.search') }}',
        type: 'GET',
        data: filters,
        headers: {
            'X-CSRF-TOKEN': '{{ csrf_token() }}'
        },
        success: function(data) {
            displayResults(data.results);
        },
        error: function(xhr) {
            toastr.error('Failed to search Proposal BOMs', 'Error');
        }
    });
}

function clearFilters() {
    $('#filterClient, #filterPanel, #filterFeeder, #filterBom').val('');
    searchProposalBoms(); // Show default list
}

function displayResults(results) {
    var html = '<div class="list-group">';
    if (results.length === 0) {
        html += '<p class="text-muted">No results found</p>';
    } else {
        results.forEach(function(item) {
            html += '<label class="list-group-item">';
            html += '<input type="radio" name="selectedBom" value="' + item.id + '"> ';
            html += item.text;
            html += '</label>';
        });
    }
    html += '</div>';
    $('#proposalBomResults').html(html);
}
```

---

## ✅ Advantages

1. **Clear Separation:** Each filter has its own field
2. **Easy to Use:** Users know exactly what each field does
3. **Flexible:** Can use one or multiple filters
4. **No Typing Issues:** Regular input fields, not Select2
5. **Better UX:** Clear "Search" button action

---

## ❌ Disadvantages

1. **Takes More Space:** 4 fields instead of 1
2. **Requires Click:** Must click "Search" button (not real-time)
3. **More Clicks:** Slightly more steps than single search box

---

## 🎯 Recommendation

**I recommend Option B (Vertical Stack Layout)** because:
- Cleaner and easier to read
- More space for labels
- Professional appearance
- Easy to understand

**Alternative:** We could also add **real-time search** (search as you type) if preferred, but that might be slower with large datasets.

---

## 📝 Questions for Review

1. **Which layout do you prefer?**
   - Option A: Horizontal (2x2 grid)
   - Option B: Vertical (stacked)
   - Option C: Collapsible

2. **Search behavior:**
   - Click "Search" button (recommended)
   - OR Real-time as you type (might be slower)

3. **Results display:**
   - Radio buttons (select one)
   - OR Checkboxes (select multiple)

4. **Default behavior:**
   - Show default list on modal open?
   - OR Show empty until user searches?

---

**Please review and let me know your preferences, then I'll implement it!**

