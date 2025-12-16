> Source: source_snapshot/docs/05_WORKFLOWS/19_BOM_CREATION_FLOW.md
> Bifurcated into: features/master_bom/workflows/19_BOM_CREATION_FLOW.md
> Module: Master BOM > Workflows
> Date: 2025-12-17 (IST)

# BOM (Bill of Materials) Creation Flow

**Document:** 19_BOM_CREATION_FLOW.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Overview

**BOM Types:**
1. **Master BOM** - Reusable template (created once, used many times)
2. **Quotation BOM** - Specific to quotation (custom or from master)

**Purpose:** Define assemblies/kits with multiple component products

---

## Complete BOM Workflow

```
BOM CREATION TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPE A: MASTER BOM (Template) - Create Once, Use Forever
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Navigate to Master BOM
┌────────────────────────────────────────────────────────────┐
│ Sidebar → Master Data → Master BOM                         │
└────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────┐
│ Master BOM List                                             │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ BOM Name              │ Items │ Actions              │  │
│ ├───────────────────────┼───────┼──────────────────────┤  │
│ │ Distribution Panel    │   8   │ [Edit] [Delete]      │  │
│ │ Control Panel         │  12   │ [Edit] [Delete]      │  │
│ │ Cable Termination Kit │   5   │ [Edit] [Delete]      │  │
│ └──────────────────────────────────────────────────────┘  │
│ [+ Create Master BOM]                                      │
└────────────────────────────────────────────────────────────┘
         ↓
         Click [+ Create Master BOM]
         ↓

STEP 2: Create Master BOM Form
┌────────────────────────────────────────────────────────────┐
│ Create Master BOM                                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ BOM Name: [Text input_______________________________]      │
│ Example: "Distribution Panel Standard Components"          │
│                                                             │
│ [Save BOM] (saves header only)                             │
└────────────────────────────────────────────────────────────┘
         ↓
         User enters name and saves
         ↓

STEP 3: Edit to Add Items
┌────────────────────────────────────────────────────────────┐
│ Edit Master BOM: "Distribution Panel Components"           │
├────────────────────────────────────────────────────────────┤
│ BOM Name: Distribution Panel Components                    │
│                                                             │
│ ITEMS:                         [+ Add Item]                │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ #  │ Product             │ Qty │ Actions             │  │
│ ├────┼─────────────────────┼─────┼─────────────────────┤  │
│ │ 1  │ Panel Enclosure     │  1  │ [Edit] [Delete]     │  │
│ │ 2  │ Circuit Breaker MCB │ 12  │ [Edit] [Delete]     │  │
│ │ 3  │ Busbar - Copper     │  3  │ [Edit] [Delete]     │  │
│ └────┴─────────────────────┴─────┴─────────────────────┘  │
│                                                             │
│ [Update Master BOM]                                         │
└────────────────────────────────────────────────────────────┘
         ↓
         Click [+ Add Item]
         ↓

STEP 4: Add Item to Master BOM
┌────────────────────────────────────────────────────────────┐
│ Add Item to BOM                                             │
├────────────────────────────────────────────────────────────┤
│ Product: [Dropdown - Select Generic Product ▼_________]    │
│                                                             │
│ Quantity: [Number: 1___] (default quantity in BOM)        │
│                                                             │
│ [Cancel]                                      [Add Item]    │
└────────────────────────────────────────────────────────────┘
         ↓
         User selects product and quantity
         ↓

STEP 5: Item Added to Master BOM
┌────────────────────────────────────────────────────────────┐
│ Edit Master BOM: "Distribution Panel Components"           │
│                                                             │
│ ITEMS:                         [+ Add Item]                │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ #  │ Product             │ Qty │ Actions             │  │
│ ├────┼─────────────────────┼─────┼─────────────────────┤  │
│ │ 1  │ Panel Enclosure     │  1  │ [Edit] [Delete]     │  │
│ │ 2  │ Circuit Breaker MCB │ 12  │ [Edit] [Delete]     │  │
│ │ 3  │ Busbar - Copper     │  3  │ [Edit] [Delete]     │  │
│ │ 4  │ Terminal Block      │  6  │ [Edit] [Delete] ✨  │  │
│ └────┴─────────────────────┴─────┴─────────────────────┘  │
│                                                             │
│ [Update Master BOM]                                         │
└────────────────────────────────────────────────────────────┘
         ↓
         Repeat: Add more items
         ↓

MASTER BOM COMPLETE!
✓ Can now be used in any quotation
✓ All items pre-configured
✓ One-click insertion

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPE B: QUOTATION BOM (Specific) - Created in Quotation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT: User is editing a quotation
└── See Document 17_QUOTATION_CREATION_FLOW.md for quotation context

OPTION 1: Add Custom BOM
┌────────────────────────────────────────────────────────────┐
│ Quotation Edit Page                                         │
│ └── Sale Item #1                                            │
│     └── Click [+ Add BOM]                                  │
└────────────────────────────────────────────────────────────┘
         ↓
         AJAX: /quotation/addmorebom
         ↓
┌────────────────────────────────────────────────────────────┐
│ BOM Form Inserted                                           │
│ ├── BOM Name: [Input_________________]                     │
│ ├── Quantity: [1__]                                        │
│ ├── Rate: [0.00___]                                        │
│ ├── [+ Add Item]                                           │
│ └── Items: (None - user adds manually)                     │
└────────────────────────────────────────────────────────────┘
         ↓
         User adds items one by one (see Step 7 in Doc 17)
         ↓
         Complete custom BOM created

OPTION 2: Add Master BOM (Template)
┌────────────────────────────────────────────────────────────┐
│ Quotation Edit Page                                         │
│ └── Sale Item #1                                            │
│     └── Click [+ Add Master BOM]                           │
└────────────────────────────────────────────────────────────┘
         ↓
         Modal opens
         ↓
┌────────────────────────────────────────────────────────────┐
│ Select Master BOM                             [✕ Close]     │
├────────────────────────────────────────────────────────────┤
│ Master BOM: [Distribution Panel Components ▼]              │
│                                                             │
│ PREVIEW:                                                    │
│ This BOM contains 4 items:                                 │
│ 1. Panel Enclosure (Qty: 1)                                │
│ 2. Circuit Breaker MCB (Qty: 12)                           │
│ 3. Busbar - Copper (Qty: 3)                                │
│ 4. Terminal Block (Qty: 6)                                 │
│                                                             │
│ [Cancel]                        [Add BOM to Quotation]     │
└────────────────────────────────────────────────────────────┘
         ↓
         User clicks [Add BOM to Quotation]
         ↓
┌────────────────────────────────────────────────────────────┐
│ SERVER PROCESSING                                           │
│ Controller: QuotationController@getMasterBomVal()           │
│                                                             │
│ 1. Load master BOM details                                 │
│ 2. Load all master BOM items                               │
│ 3. For each master BOM item:                               │
│    ├── Get product details                                 │
│    ├── Get current price                                   │
│    ├── Get make/series options                             │
│    └── Create item form HTML                               │
│ 4. Create BOM container                                    │
│ 5. Insert all item forms                                   │
│ 6. Return complete HTML                                    │
└────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────┐
│ BOM with ALL ITEMS appears in quotation!                   │
│ ├── BOM Name: "Distribution Panel Components"              │
│ ├── All 4 items pre-loaded                                 │
│ ├── Quantities pre-filled                                  │
│ ├── Prices auto-loaded                                     │
│ └── User can edit before saving                            │
└────────────────────────────────────────────────────────────┘
         ↓
         Much faster than adding manually!

END OF BOM WORKFLOW
```

---

## Master BOM Controller

**File:** app/Http/Controllers/MasterBomController.php  
**Lines:** 283

### Key Methods

#### index() - List Master BOMs
```php
public function index()
{
    $masterBoms = MasterBom::where('Status', 0)->get();
    
    // Add item count to each BOM
    foreach($masterBoms as $bom) {
        $bom->itemCount = MasterBomItem::where('MasterBomId', $bom->MasterBomId)
            ->where('Status', 0)
            ->count();
    }
    
    return view('masterbom.index', compact('masterBoms'));
}
```

---

#### create() - Show Create Form
```php
public function create()
{
    return view('masterbom.create');
}
```

**Simple Form:**
- BOM Name only
- Items added after creation

---

#### store() - Save Master BOM
```php
public function store(Request $request)
{
    $validation = ['Name' => 'required'];
    $validator = Validator::make($request->all(), $validation);
    
    if ($validator->fails()) {
        return redirect()->back()->with('error', 'BOM name required');
    }
    
    $masterBom = MasterBom::create([
        'Name' => $request->Name,
        'Status' => 0,
    ]);
    
    // Redirect to edit to add items
    return redirect()->route('masterbom.edit', $masterBom->MasterBomId)
        ->with('success', 'Master BOM created. Now add items.');
}
```

---

#### edit($id) - Show Edit Form
```php
public function edit($id)
{
    $masterBom = MasterBom::find($id);
    
    // Load existing items
    $items = MasterBomItem::where('MasterBomId', $id)
        ->with('product')
        ->where('Status', 0)
        ->get();
    
    // Load products for dropdown (generics only)
    $products = Product::where('ProductType', 1)
        ->where('Status', 0)
        ->pluck('Name', 'ProductId')
        ->ToArray();
    
    return view('masterbom.edit', compact('masterBom', 'items', 'products'));
}
```

---

#### update($id) - Save BOM Changes
```php
public function update(Request $request, $id)
{
    // Update BOM name
    MasterBom::where('MasterBomId', $id)->update([
        'Name' => $request->Name,
    ]);
    
    // Soft delete existing items
    MasterBomItem::where('MasterBomId', $id)->update(['Status' => 1]);
    
    // Re-insert items
    if($request->has('items')) {
        foreach($request->items as $item) {
            MasterBomItem::create([
                'MasterBomId' => $id,
                'ProductId' => $item['product_id'],
                'Quantity' => $item['quantity'],
                'Status' => 0,
            ]);
        }
    }
    
    return redirect()->route('masterbom.index')
        ->with('success', 'Master BOM updated successfully');
}
```

---

## Database Schema

### master_boms Table

```sql
CREATE TABLE master_boms (
    MasterBomId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Status TINYINT DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Example Records:**
```
MasterBomId | Name                              | Status
─────────────────────────────────────────────────────────
1           | Distribution Panel Components     | 0
2           | Control Panel Standard BOM        | 0
3           | Cable Termination Kit             | 0
4           | Transformer Installation Set      | 0
```

---

### master_bom_items Table

```sql
CREATE TABLE master_bom_items (
    MasterBomItemId INT PRIMARY KEY AUTO_INCREMENT,
    MasterBomId INT NOT NULL,
    ProductId INT NOT NULL,          -- Generic product only!
    Quantity DECIMAL(10,2) NOT NULL, -- Default quantity
    Status TINYINT DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (MasterBomId) REFERENCES master_boms(MasterBomId) ON DELETE CASCADE,
    FOREIGN KEY (ProductId) REFERENCES products(ProductId)
);
```

**Example Records:**
```
MasterBomItemId | MasterBomId | ProductId | Quantity | Status
───────────────────────────────────────────────────────────────
1               | 1           | 250       | 1.00     | 0
2               | 1           | 251       | 12.00    | 0
3               | 1           | 252       | 3.00     | 0
4               | 1           | 253       | 6.00     | 0
```

**Relationship:**
```
master_boms (1) ──→ (N) master_bom_items (N) ──→ (1) products
```

---

## Using Master BOM in Quotation

### Complete Process

**Step 1: In Quotation Edit**
```
User has sale item ready
└── Click [+ Add Master BOM]
```

**Step 2: Modal Opens**

```javascript
// JavaScript
$('#addMasterBomBtn').click(function() {
    var saleId = $(this).data('sale-id');
    var quotationId = $(this).data('quotation-id');
    
    // Load modal
    $.get('/quotation/masterbom/' + saleId, function(html) {
        $('#masterBomModal').html(html).modal('show');
    });
});
```

**Step 3: Server Returns Modal HTML**

```php
// Controller: QuotationController@getMasterBomItem($saleId)
public function getMasterBomItem($id)
{
    $quotationSale = QuotationSale::find($id);
    $MasterBom = MasterBom::where('Status', 0)
        ->pluck('Name', 'MasterBomId')
        ->ToArray();
    
    return view('quotation.masterbom', compact(
        'id', 'MasterBom', 'quotationSale', ...
    ));
}
```

**Step 4: User Selects BOM**

```javascript
// JavaScript - BOM selection triggers preview
$('#masterBomSelect').change(function() {
    var bomId = $(this).val();
    
    // Load BOM preview
    $.post('/quotation/masterbom/value', {
        id: bomId,
        _token: csrfToken
    }, function(items) {
        // Display preview
        var html = '<h4>BOM Preview:</h4><ul>';
        items.forEach(function(item) {
            html += '<li>' + item.ProductName + ' (Qty: ' + item.Quantity + ')</li>';
        });
        html += '</ul>';
        $('#bomPreview').html(html);
    });
});
```

**Step 5: User Clicks "Add BOM"**

```php
// Controller: QuotationController@getMasterBomVal(Request)
public function getMasterBomVal(Request $request)
{
    $MasterBomId = $request->id;
    
    // Load master BOM items
    $MasterBomItems = MasterBomItem::where('MasterBomId', $MasterBomId)
        ->where('Status', 0)
        ->get();
    
    $items = [];
    foreach($MasterBomItems as $bomItem) {
        $Product = Product::find($bomItem->ProductId);
        
        // Get current price
        $date = date('Y-m-d');
        $price = Price::where('ProductId', $bomItem->ProductId)
            ->where('EffectiveDate', '<=', $date)
            ->orderBy('EffectiveDate', 'DESC')
            ->first();
        
        // Get available makes for this product
        $makes = MakeCategory::join('makes', 'makes.MakeId', '=', 'make_categories.MakeId')
            ->where('make_categories.CategoryId', $Product->CategoryId)
            ->pluck('makes.Name', 'makes.MakeId');
        
        $items[] = [
            'ProductId' => $Product->ProductId,
            'ProductName' => $Product->Name,
            'CategoryId' => $Product->CategoryId,
            'CategoryName' => $Product->category->Name,
            'Quantity' => $bomItem->Quantity,
            'Rate' => $price ? $price->Rate : 0,
            'Makes' => $makes,
            // ... more data
        ];
    }
    
    // Generate item forms for all products
    $html = view('quotation.bom-items', compact('items'))->render();
    
    return response()->json([
        'success' => true,
        'html' => $html,
        'itemCount' => count($items)
    ]);
}
```

**Step 6: BOM + Items Inserted**

```
Result in Quotation:
├── BOM: "Distribution Panel Components"
│   ├── Item 1: Panel Enclosure (Qty: 1, Rate: 25000)
│   ├── Item 2: Circuit Breaker (Qty: 12, Rate: 1500)
│   ├── Item 3: Busbar (Qty: 3, Rate: 5000)
│   └── Item 4: Terminal Block (Qty: 6, Rate: 500)

All pre-filled! User can adjust before saving.
```

---

## BOM Quantity Multiplication

### Important Concept!

**Master BOM quantities are templates:**
- Master BOM: Circuit Breaker (Qty: 12)
- Meaning: 12 breakers per assembly

**When used in quotation:**
- Sale Qty: 2 (two panels)
- BOM Qty: 1 (one BOM per panel)
- Item Qty from template: 12

**Final calculation:**
```
Final Item Qty = Sale Qty × BOM Qty × Item Template Qty
               = 2 × 1 × 12
               = 24 circuit breakers total
```

**In Quotation:**
```
Sale Item: Distribution Panel
├── Quantity: 2 panels
└── BOM: Panel Components
    ├── Quantity: 1 (1 BOM per panel)
    └── Item: Circuit Breaker
        ├── Template Qty: 12
        ├── Actual Qty: 24 (2 × 1 × 12)
        └── Amount: 24 × 1500 = 36,000
```

---

## Business Rules

### Master BOM Rules

1. **Name:** Unique and descriptive
2. **Items:** Only generic products (Type 1)
3. **Quantities:** Template quantities (default)
4. **Pricing:** No prices in master BOM (loaded when used)
5. **Reusable:** Can be used in unlimited quotations
6. **Editable:** Can be edited (affects future quotations only)

---

### Quotation BOM Rules

1. **Source:** Can be from master BOM or custom
2. **MasterBomId:** Set if from master, NULL if custom
3. **Items:** Can have make/series (specific variants)
4. **Pricing:** Actual prices stored
5. **Independence:** Changes don't affect master BOM
6. **Quantities:** Can be adjusted from template
7. **Deletion:** Soft delete (Status=1)

---

### Item Selection Rules

**In Master BOM:**
- Generic products only
- No Make/Series
- Template quantities

**In Quotation BOM:**
- Start with generic
- Can specify Make
- Can specify Series
- Can select specific SKU
- Actual quantities and prices

---

## Common Use Cases

### Use Case 1: Standard Assembly

**Scenario:** Selling standard distribution panel kit

**Process:**
1. Create master BOM: "DP-100A Standard Kit"
2. Add items:
   - Panel enclosure (1)
   - Circuit breakers (12)
   - Busbars (3)
   - Terminal blocks (20)
   - Cable glands (8)
   - Hardware kit (1)
3. Save master BOM
4. In quotations: Add master BOM
5. Specify makes/series as needed
6. Done!

**Benefit:** 5-second BOM creation vs 5-minute manual entry

---

### Use Case 2: Custom Assembly

**Scenario:** Unique configuration for specific project

**Process:**
1. In quotation, add custom BOM
2. Name: "Custom Control Panel - Project ABC"
3. Add items manually
4. Specify all products, makes, series
5. Save quotation
6. (Optional) Convert to master BOM if reusable

---

### Use Case 3: Mixed Approach

**Scenario:** Standard kit + customizations

**Process:**
1. Add master BOM (standard items)
2. Edit quantities as needed
3. Add additional custom items
4. Delete unwanted items from template
5. Save quotation

---

### Use Case 4: BOM Variants

**Scenario:** Same kit, different brands

**Master BOM (Brand-agnostic):**
```
"Control Panel Standard BOM"
├── PLC (Generic)
├── HMI (Generic)
├── Power Supply (Generic)
└── I/O Modules (Generic)
```

**Quotation 1 (Siemens variant):**
```
"Control Panel - Siemens"
├── PLC → Siemens S7-1200
├── HMI → Siemens TP700
├── Power Supply → Siemens SITOP
└── I/O Modules → Siemens ET200
```

**Quotation 2 (ABB variant):**
```
"Control Panel - ABB"
├── PLC → ABB AC500
├── HMI → ABB PP886
├── Power Supply → ABB CP-E
└── I/O Modules → ABB TB511
```

Same master BOM, different makes/series selected!

---

## BOM Views

### masterbom/index.blade.php

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Master BOMs                      [+ Create Master BOM]     │
├────────────────────────────────────────────────────────────┤
│ Search: [_____________] [🔍]                               │
├────────────────────────────────────────────────────────────┤
│ BOM Name                    │ Items │ Created  │ Actions  │
├─────────────────────────────┼───────┼──────────┼──────────┤
│ Distribution Panel BOM      │   8   │ Jan 2022 │ [✏️][🗑️]│
│ Control Panel Standard      │  12   │ Feb 2022 │ [✏️][🗑️]│
│ Cable Termination Kit       │   5   │ Mar 2022 │ [✏️][🗑️]│
│ Transformer Installation    │   7   │ Apr 2022 │ [✏️][🗑️]│
└─────────────────────────────┴───────┴──────────┴──────────┘
```

---

### masterbom/create.blade.php

**Simple Form:**
```
┌────────────────────────────────────────────────────────────┐
│ Create Master BOM                                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ BOM Name: [Text input_______________________________] *    │
│                                                             │
│ Example: "Distribution Panel Standard Components"          │
│          "Control Panel - 10 I/O BOM"                      │
│          "Cable Termination Kit - HT"                      │
│                                                             │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│ Note: After creating BOM, you'll add items on next page.  │
│                                                             │
│ [Cancel]                                   [Create BOM]    │
└────────────────────────────────────────────────────────────┘
```

---

### masterbom/edit.blade.php

**Complex Form:**
```
┌────────────────────────────────────────────────────────────┐
│ Edit Master BOM                                             │
├────────────────────────────────────────────────────────────┤
│ BOM Name: [Distribution Panel Components___________]      │
│                                                             │
│ ─────────────────────────────────────────────────────────  │
│                                                             │
│ BOM ITEMS                               [+ Add Item]       │
│                                                             │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ # │ Product           │ Qty  │ Actions               │  │
│ ├───┼───────────────────┼──────┼───────────────────────┤  │
│ │ 1 │ Panel Enclosure   │ 1.00 │ [Edit] [Delete]       │  │
│ │ 2 │ MCB Circuit Break │12.00 │ [Edit] [Delete]       │  │
│ │ 3 │ Copper Busbar     │ 3.00 │ [Edit] [Delete]       │  │
│ │ 4 │ Terminal Block    │ 6.00 │ [Edit] [Delete]       │  │
│ │ 5 │ Cable Gland       │ 8.00 │ [Edit] [Delete]       │  │
│ │ 6 │ Mounting Hardware │ 1.00 │ [Edit] [Delete]       │  │
│ │ 7 │ Earth Bar         │ 1.00 │ [Edit] [Delete]       │  │
│ │ 8 │ Door Lock         │ 1.00 │ [Edit] [Delete]       │  │
│ └───┴───────────────────┴──────┴───────────────────────┘  │
│                                                             │
│ Total Items: 8                                             │
│                                                             │
│ [Cancel]                             [Update Master BOM]   │
└────────────────────────────────────────────────────────────┘
```

**Add Item Section (Expanded):**
```
┌────────────────────────────────────────────────────────────┐
│ Add Item to BOM                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Product: [Select Generic Product ▼_____________________]  │
│          (Only shows generic products - Type 1)            │
│                                                             │
│ Quantity: [Number: 1.00___]                                │
│           (Default quantity per assembly)                  │
│                                                             │
│ [Cancel]                                      [Add Item]    │
└────────────────────────────────────────────────────────────┘
```

---

## BOM Benefits

### Time Savings

**Without Master BOM:**
- Create quotation: 2 min
- Add sale item: 1 min
- Add BOM: 1 min
- Add 8 items manually: 8 × 2 min = 16 min
- **Total: ~20 minutes per quotation**

**With Master BOM:**
- Create quotation: 2 min
- Add sale item: 1 min
- Select master BOM: 30 sec
- All 8 items auto-added: 0 min
- Adjust if needed: 2 min
- **Total: ~5 minutes per quotation**

**Savings: 75% time reduction!**

---

### Consistency

**Benefits:**
✅ Standard configurations  
✅ No missing items  
✅ Consistent quantities  
✅ Reduced errors  
✅ Quality assurance  

---

### Ease of Maintenance

**Price Updates:**
- Update prices in Price module
- All future uses auto-load new prices
- No need to update BOMs

**Product Changes:**
- Update product in Product module
- All BOMs automatically reference latest
- No manual updates needed

---

## Advanced Features

### BOM Nesting

**Current System:**
```
Quotation
└── Sale Item
    └── BOM
        └── Items
```

**Not Supported (Would Require Development):**
```
Quotation
└── Sale Item
    └── BOM
        └── Item (could itself be a BOM)
            └── Sub-items
```

---

### BOM Templates by Category

**Organizational Strategy:**
```
Master BOMs organized by product category:

Electrical Panels:
├── DP-100A Standard BOM
├── DP-200A Standard BOM
├── DP-400A Standard BOM
├── CP-10IO Standard BOM
└── CP-20IO Standard BOM

Transformers:
├── 25KVA Installation Kit
├── 63KVA Installation Kit
└── 100KVA Installation Kit

Cables:
├── Cable Termination Kit - LT
└── Cable Termination Kit - HT
```

---

### BOM Versioning

**Challenge:** Master BOM updated, what about old quotations?

**Solution in Current System:**
- Quotation BOMs are copies (independent)
- Master BOM changes don't affect existing quotations
- Only new quotations use updated master BOM

**Example:**
```
Master BOM Updated: Jan 15, 2023
├── Quotation from Jan 10, 2023 → Uses old structure ✓
├── Quotation from Jan 20, 2023 → Uses new structure ✓
└── Independence maintained
```

---

## Best Practices

### Creating Master BOMs

**1. Use Clear Names**
```
✓ Good: "Distribution Panel 100A - Standard Components"
✓ Good: "Control Panel - 10 I/O - Basic Configuration"
✗ Bad: "BOM1"
✗ Bad: "Panel"
```

**2. Logical Grouping**
```
✓ Group by function:
  - Main Components BOM
  - Accessories BOM
  - Installation Materials BOM

✓ Group by system:
  - Power System BOM
  - Control System BOM
  - Safety System BOM
```

**3. Standard Quantities**
- Use most common quantities as defaults
- Easy to adjust in quotation if needed

**4. Documentation**
- Add notes/remarks in items
- Explain special requirements
- Reference standards/specifications

---

### Using BOMs in Quotations

**1. Choose Appropriate BOM**
- Match project requirements
- Consider variants (capacity, configuration)

**2. Customize as Needed**
- Adjust quantities
- Add extra items
- Remove unnecessary items
- Specify makes/series

**3. Verify Pricing**
- Check auto-loaded rates
- Confirm prices current
- Apply discounts if applicable

---

## Summary

### Master BOM Module

**Purpose:** Create reusable BOM templates  
**Tables:** 2 (master_boms, master_bom_items)  
**Controller:** MasterBomController (283 lines)  
**Views:** 3 (index, create, edit)  
**Relationships:** → products (generics only)

### Quotation BOM Usage

**Purpose:** Use templates in quotations  
**Tables:** 2 (quotation_sale_boms, quotation_sale_bom_items)  
**Integration:** Via QuotationController methods  
**Flexibility:** Copy template, customize, or create custom

### Key Benefits

✅ **Time Savings:** 75% faster quotation creation  
✅ **Consistency:** Standard configurations  
✅ **Accuracy:** No missing items  
✅ **Flexibility:** Can customize each usage  
✅ **Maintainability:** Update once, use everywhere  

### Critical Concepts

1. **Templates vs Instances:** Master BOMs are templates, quotation BOMs are instances
2. **Generic Products:** Master BOMs use generics (flexibility)
3. **Specific Products:** Quotations specify makes/series (actual products)
4. **Independence:** Quotation BOMs are copies (editable)
5. **Quantity Multiplication:** Sale × BOM × Item quantities

---

**End of Document 08 & 19 - Product & BOM Modules**

[← Back to Quotation Module](07_QUOTATION_MODULE.md) | [Next: Client/Project Module →](10_CLIENT_PROJECT_MODULE.md)
