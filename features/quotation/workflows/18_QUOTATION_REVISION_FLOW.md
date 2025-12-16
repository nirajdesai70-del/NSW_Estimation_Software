> Source: source_snapshot/docs/05_WORKFLOWS/18_QUOTATION_REVISION_FLOW.md
> Bifurcated into: features/quotation/workflows/18_QUOTATION_REVISION_FLOW.md
> Module: Quotation > Workflows
> Date: 2025-12-17 (IST)

# Quotation Revision Flow - Complete Guide

**Document:** 18_QUOTATION_REVISION_FLOW.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Overview

**Purpose:** Create a new version of an existing quotation (revision) while preserving the original.

**When Used:**
- Client requests changes to quotation
- Pricing updates needed
- Product substitutions required
- Quantity changes
- Scope modifications

**Result:** New quotation with revision number (e.g., 220716001R001) with all data copied from original

---

## Complete Revision Workflow

```
QUOTATION REVISION PROCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

START: User has existing quotation #220716001
├── Client requested changes
├── Pricing updates needed
└── Want to keep original for reference

STEP 1: INITIATE REVISION
┌────────────────────────────────────────────────────────────┐
│ Quotation List Page                                        │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ Quotation No │ Client        │ Date       │ Actions  │  │
│ ├──────────────┼───────────────┼────────────┼──────────┤  │
│ │ 220716001    │ ABC Industries│ 2022-07-16 │ [Edit]   │  │
│ │              │               │            │ [PDF]    │  │
│ │              │               │            │ [Revision]│  │
│ └──────────────┴───────────────┴────────────┴──────────┘  │
└────────────────────────────────────────────────────────────┘
         │
         │ User clicks [Revision] button
         ▼
┌────────────────────────────────────────────────────────────┐
│ CONFIRMATION MODAL                                          │
│ ┌──────────────────────────────────────────────────────┐  │
│ │ Create Revision?                                      │  │
│ │                                                        │  │
│ │ This will create a new quotation copying all data    │  │
│ │ from Quotation #220716001                            │  │
│ │                                                        │  │
│ │ New revision number will be:                          │  │
│ │ 220716001R001                                         │  │
│ │                                                        │  │
│ │ Original quotation will remain unchanged.             │  │
│ │                                                        │  │
│ │ [Cancel]                        [Create Revision]     │  │
│ └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
         │
         │ User clicks [Create Revision]
         ▼

STEP 2: SERVER-SIDE PROCESSING (COMPLEX!)
┌────────────────────────────────────────────────────────────┐
│ Route: POST /quotation/revision/{id}                       │
│ Controller: QuotationController@revision($id)              │
│                                                             │
│ PHASE 1: Load Original Quotation                           │
│ ├── Load quotation header (client, project, etc.)         │
│ ├── Load all sale items                                   │
│ ├── Load all BOMs for each sale                           │
│ ├── Load all items for each BOM                           │
│ └── Load make/series selections                           │
│                                                             │
│ PHASE 2: Generate Revision Number                          │
│ ├── Extract first 10 chars of original (220716001)        │
│ ├── Check if revisions exist:                             │
│ │   ├── No revisions: Create 220716001R001               │
│ │   └── Has revisions: Find highest R### and increment   │
│ │       (e.g., R002 exists → create R003)                │
│ └── Result: New unique revision number                    │
│                                                             │
│ PHASE 3: Create New Quotation Record                       │
│ ├── Copy all fields from original                         │
│ ├── Set QuotationNo = revision number                     │
│ ├── Set ParentId = original QuotationId                   │
│ ├── Set created_at = now()                                │
│ └── INSERT into quotations table                          │
│                                                             │
│ PHASE 4: Copy Make/Series Selections                       │
│ └── For each original quotation_make_series:              │
│     ├── Create new record with new QuotationId            │
│     ├── Copy CategoryId, MakeId, SeriesId                 │
│     └── INSERT into quotation_make_series                 │
│                                                             │
│ PHASE 5: Copy All Sale Items (NESTED LOOP!)                │
│ └── For each original QuotationSale:                      │
│     ├── Create new QuotationSale record                   │
│     ├── Copy: Name, CustomName, Qty, Rate, Amount, etc.  │
│     ├── Get new QuotationSaleId                           │
│     │                                                      │
│     └── PHASE 6: Copy BOMs for this Sale                  │
│         └── For each QuotationSaleBom:                    │
│             ├── Create new QuotationSaleBom record        │
│             ├── Link to new sale and quotation            │
│             ├── Copy: Name, Qty, Rate, Amount, etc.       │
│             ├── Get new QuotationSaleBomId                │
│             │                                              │
│             └── PHASE 7: Copy Items for this BOM          │
│                 └── For each QuotationSaleBomItem:        │
│                     ├── Create new record                  │
│                     ├── Link to new BOM, sale, quotation  │
│                     ├── Copy: Product, Make, Series, etc. │
│                     ├── Copy: Qty, Rate, Discount, Amount │
│                     └── INSERT into quotation_sale_bom_items│
│                                                             │
│ RESULT:                                                     │
│ ├── 1 new Quotation created                                │
│ ├── N QuotationMakeSeries records                          │
│ ├── N QuotationSale records                                │
│ ├── N×M QuotationSaleBom records                          │
│ └── N×M×P QuotationSaleBomItem records                    │
│                                                             │
│ Example: Original had 3 sales, 5 BOMs, 23 items           │
│ → Revision creates 32 new database records!                │
└────────────────────────────────────────────────────────────┘
         │
         │ Success! Redirect to edit new revision
         ▼

STEP 3: EDIT REVISION
┌────────────────────────────────────────────────────────────┐
│ Edit Quotation: #220716001R001                             │
│ (Parent: #220716001)                                        │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ All data copied from original:                             │
│ ✓ Client, Project, Contact                                 │
│ ✓ All sale items                                           │
│ ✓ All BOMs                                                 │
│ ✓ All items with quantities and rates                      │
│                                                             │
│ User can now:                                               │
│ ├── Change quantities                                      │
│ ├── Update rates/prices                                    │
│ ├── Add/remove items                                       │
│ ├── Modify BOMs                                            │
│ └── Add/remove sale items                                  │
│                                                             │
│ [Update Quotation] button                                  │
└────────────────────────────────────────────────────────────┘
         │
         │ User makes changes and saves
         ▼

STEP 4: SAVE CHANGES
┌────────────────────────────────────────────────────────────┐
│ Updates saved to revision (220716001R001)                  │
│ Original (220716001) remains unchanged                     │
└────────────────────────────────────────────────────────────┘
         │
         │ Generate PDF of revision
         ▼

STEP 5: SEND TO CLIENT
┌────────────────────────────────────────────────────────────┐
│ PDF Generated:                                              │
│ Quotation Revision: 220716001R001                          │
│ (Supersedes: 220716001)                                     │
│                                                             │
│ Shows all updated pricing/items                            │
└────────────────────────────────────────────────────────────┘

END OF REVISION WORKFLOW
```

---

## Detailed Code Analysis

### Revision Controller Method

```php
// File: app/Http/Controllers/QuotationController.php
// Method: revision($id)
// Line: ~118-188

public function revision($id)
{
    // STEP 1: Load Original Quotation
    $Quotations = Quotation::find($id);
    
    if(!$Quotations) {
        return redirect()->back()->with('error', 'Quotation not found');
    }
    
    // STEP 2: Generate Revision Number
    $QuotationNo = $Quotations->QuotationNo;
    
    // Check if this is first revision or subsequent
    $revisionCheck = Quotation::where('QuotationNo', 'like', $QuotationNo.'R%')->count();
    
    if($revisionCheck == 0) {
        // First revision: Add R001
        $QuotationNo = $QuotationNo.'R001';
        $ParentId = $id; // Original quotation is parent
    } else {
        // Subsequent revision: Increment R number
        // Extract base number (first 10 chars: YYMMDD###)
        $baseNo = substr($QuotationNo, 0, 10);
        
        // Find highest revision number
        $v_StartNo1 = DB::select(
            "SELECT CONCAT(?, LPAD(CAST(MAX(RIGHT(QuotationNo, 3)) + 1 AS CHAR), 3, '0')) AS MaxNumber 
             FROM quotations 
             WHERE QuotationNo LIKE ?",
            [$baseNo.'R', $baseNo.'R%']
        );
        
        $QuotationNo = $v_StartNo1[0]->MaxNumber ?? $baseNo.'R001';
        
        // Parent is the original (not the previous revision)
        $ParentId = $Quotations->ParentId ?: $id;
    }
    
    // STEP 3: Create New Quotation Record
    $new_quotation = Quotation::create([
        'ClientId'    => $Quotations->ClientId,
        'ProjectId'   => $Quotations->ProjectId,
        'QuotationNo' => $QuotationNo,
        'ParentId'    => $ParentId,
        'ContactId'   => $Quotations->ContactId,
        'EmployeeId'  => $Quotations->EmployeeId,
        'SalesId'     => $Quotations->SalesId,
        'CategoryId'  => $Quotations->CategoryId,
        'MakeId'      => $Quotations->MakeId,
        'SeriesId'    => $Quotations->SeriesId,
        'Discount'    => $Quotations->Discount,
        'PrintType'   => 0, // Reset print type
        'Status'      => 0,
    ]);
    
    $newQuotationId = $new_quotation->QuotationId;
    
    // STEP 4: Copy Make/Series Selections
    $makeSeriesRecords = DB::insert(
        "INSERT INTO quotation_make_series(QuotationId, CategoryId, MakeId, SeriesId, created_at, updated_at)
         SELECT ? as QuotationId, CategoryId, MakeId, SeriesId, NOW(), NOW() 
         FROM quotation_make_series 
         WHERE QuotationId = ?",
        [$newQuotationId, $id]
    );
    
    // STEP 5: Copy All Sales
    $sales = QuotationSale::where('QuotationId', $id)
        ->where('Status', 0)
        ->get();
    
    foreach($sales as $sale) {
        // Create new sale record
        $newSale = QuotationSale::create([
            'QuotationId'    => $newQuotationId,
            'SaleId'         => $sale->SaleId,
            'Name'           => $sale->Name,
            'SaleCustomName' => $sale->SaleCustomName,
            'Qty'            => $sale->Qty,
            'Rate'           => $sale->Rate,
            'Amount'         => $sale->Amount,
            'Margin'         => $sale->Margin,
            'MarginAmount'   => $sale->MarginAmount,
            'MarginTotal'    => $sale->MarginTotal,
            'Status'         => 0,
        ]);
        
        $newSaleId = $newSale->QuotationSaleId;
        $oldSaleId = $sale->QuotationSaleId;
        
        // STEP 6: Copy BOMs for this sale
        $boms = QuotationSaleBom::where('QuotationId', $id)
            ->where('QuotationSaleId', $oldSaleId)
            ->where('Status', 0)
            ->get();
        
        foreach($boms as $bom) {
            // Create new BOM record
            $newBom = QuotationSaleBom::create([
                'QuotationId'     => $newQuotationId,
                'QuotationSaleId' => $newSaleId,
                'MasterBomId'     => $bom->MasterBomId,
                'MasterBomName'   => $bom->MasterBomName,
                'Qty'             => $bom->Qty,
                'Rate'            => $bom->Rate,
                'Amount'          => $bom->Amount,
                'Status'          => 0,
            ]);
            
            $newBomId = $newBom->QuotationSaleBomId;
            $oldBomId = $bom->QuotationSaleBomId;
            
            // STEP 7: Copy Items for this BOM
            $items = QuotationSaleBomItem::where('QuotationId', $id)
                ->where('QuotationSaleId', $oldSaleId)
                ->where('QuotationSaleBomId', $oldBomId)
                ->where('Status', 0)
                ->get();
            
            foreach($items as $item) {
                // Create new item record
                QuotationSaleBomItem::create([
                    'QuotationId'        => $newQuotationId,
                    'QuotationSaleId'    => $newSaleId,
                    'QuotationSaleBomId' => $newBomId,
                    'ProductId'          => $item->ProductId,
                    'MakeId'             => $item->MakeId,
                    'SeriesId'           => $item->SeriesId,
                    'Description'        => $item->Description,
                    'Remark'             => $item->Remark,
                    'Qty'                => $item->Qty,
                    'Rate'               => $item->Rate,
                    'Discount'           => $item->Discount,
                    'NetRate'            => $item->NetRate,
                    'Amount'             => $item->Amount,
                    'Status'             => 0,
                ]);
            }
        }
    }
    
    // STEP 8: Calculate totals for new quotation
    DB::select("CALL quotationAmount(?)", [$newQuotationId]);
    
    // STEP 9: Redirect to edit the new revision
    return redirect()->route('quotation.edit', $newQuotationId)
        ->with('success', 'Revision created successfully! Quotation No: ' . $QuotationNo);
}
```

---

## Revision Number Logic

### First Revision

```
Original: 220716001
         ↓
First Revision: 220716001R001

Logic:
1. Take original number: "220716001"
2. Append "R001": "220716001R001"
3. ParentId = original QuotationId
```

### Second Revision

```
Original: 220716001
First Revision: 220716001R001
         ↓
Second Revision: 220716001R002

Logic:
1. Extract base (first 10 chars): "220716001R"
2. Find all revisions: 220716001R%
3. Get MAX revision number: R001
4. Increment: R002
5. Result: "220716001R002"
6. ParentId = original QuotationId (not R001's ID!)
```

### Multiple Revisions

```
220716001       ← Original (Parent)
├── 220716001R001  ← Revision 1 (ParentId → 220716001)
├── 220716001R002  ← Revision 2 (ParentId → 220716001)
├── 220716001R003  ← Revision 3 (ParentId → 220716001)
└── 220716001R004  ← Revision 4 (ParentId → 220716001)

All revisions point back to original parent!
```

---

## Data Copying Process

### What Gets Copied

**Quotation Header:**
```sql
✓ ClientId
✓ ProjectId
✓ ContactId
✓ SalesId
✓ EmployeeId
✓ CategoryId, MakeId, SeriesId
✓ Discount
✗ QuotationNo (new revision number)
✗ ParentId (set to original)
✗ created_at (set to now)
✗ PrintType (reset to 0)
```

**Make/Series Selections:**
```sql
✓ All quotation_make_series records
✓ CategoryId, MakeId, SeriesId
✗ QuotationMakeSeriesId (new IDs)
```

**Sale Items:**
```sql
✓ All QuotationSale records
✓ Name, CustomName, Qty, Rate, Amount
✓ Margin, MarginAmount, MarginTotal
✗ QuotationSaleId (new IDs)
```

**BOMs:**
```sql
✓ All QuotationSaleBom records
✓ MasterBomId, MasterBomName
✓ Qty, Rate, Amount
✗ QuotationSaleBomId (new IDs)
```

**BOM Items:**
```sql
✓ All QuotationSaleBomItem records
✓ ProductId, MakeId, SeriesId, Description
✓ Qty, Rate, Discount, NetRate, Amount
✓ Remark
✗ QuotationSaleBomItemId (new IDs)
```

### Database Operations Count

Example quotation with:
- 3 Sale Items
- 5 BOMs (across all sales)
- 23 BOM Items (across all BOMs)
- 2 Make/Series selections

**Revision creates:**
```
1 Quotation record (header)
2 QuotationMakeSeries records
3 QuotationSale records
5 QuotationSaleBom records
23 QuotationSaleBomItem records
────────────────────────────
34 new database INSERT operations!
```

---

## Parent-Child Relationships

### Database Structure

```sql
-- quotations table
QuotationId | QuotationNo    | ParentId
─────────────────────────────────────────
100         | 220716001      | NULL      ← Original
101         | 220716001R001  | 100       ← Revision 1
102         | 220716001R002  | 100       ← Revision 2
103         | 220716001R003  | 100       ← Revision 3
```

### Querying Relationships

**Find all revisions of original:**
```php
$revisions = Quotation::where('ParentId', $originalId)->get();
```

**Find original from revision:**
```php
$original = Quotation::find($revision->ParentId);
```

**Find all versions (original + revisions):**
```php
$allVersions = Quotation::where('QuotationId', $originalId)
    ->orWhere('ParentId', $originalId)
    ->orderBy('created_at')
    ->get();
```

---

## Common Use Cases

### Use Case 1: Price Update

**Scenario:** Product prices changed, need to update quotation

**Process:**
1. Create revision of original quotation
2. Edit revision
3. System shows old rates
4. Update rates to new prices
5. Amounts recalculate automatically
6. Save and generate new PDF
7. Send updated quotation to client

**Original:** Preserved with old pricing  
**Revision:** Shows new pricing

---

### Use Case 2: Quantity Change

**Scenario:** Client wants different quantities

**Process:**
1. Create revision
2. Edit quantities in revision
3. Amounts recalculate (Qty × Rate)
4. BOM quantities adjust if needed
5. Save and generate PDF

**Benefit:** Can compare quantities side-by-side with original

---

### Use Case 3: Product Substitution

**Scenario:** Original product unavailable, offer alternative

**Process:**
1. Create revision
2. Edit revision
3. Remove old product
4. Add new product
5. Adjust pricing
6. Save and send to client

**Original:** Shows first product option  
**Revision:** Shows alternative product

---

### Use Case 4: Scope Change

**Scenario:** Client wants to add/remove items

**Process:**
1. Create revision
2. Add new sale items or BOMs
3. Remove unwanted items (or set Status=1)
4. Recalculate totals
5. Save and generate PDF

**Original:** Original scope  
**Revision:** Updated scope

---

## Business Rules

### Revision Numbering Rules

1. **Format:** `YYMMDD###R###`
   - YYMMDD### = Original quotation number
   - R### = Revision sequential (R001, R002, etc.)

2. **Uniqueness:** Revision numbers must be unique

3. **Sequential:** Revisions numbered sequentially (R001, R002, R003...)

4. **No Gaps:** If R002 exists, R001 must exist

5. **Parent Reference:** All revisions reference original parent

### Data Integrity Rules

1. **Original Immutable:** Creating revision doesn't modify original

2. **Status Independent:** Original and revisions have independent Status flags

3. **Complete Copy:** All nested data copied (sales → BOMs → items)

4. **Timestamps:** created_at reflects revision creation, not original

5. **Print Type:** Reset to 0 for new revision

### Workflow Rules

1. **Edit After Create:** User redirected to edit page after creation

2. **Calculations:** Totals recalculated via stored procedure

3. **PDF Independent:** Each version has its own PDF

4. **Client Communication:** Send only latest revision to client

---

## Revision Comparison

### How to Compare Versions

**Manual Comparison:**
```php
// Load original
$original = Quotation::with('sales.boms.items')->find($originalId);

// Load revision
$revision = Quotation::with('sales.boms.items')->find($revisionId);

// Compare fields
$priceChanges = [];
foreach($original->sales as $key => $originalSale) {
    $revisedSale = $revision->sales[$key] ?? null;
    if($revisedSale && $originalSale->Rate != $revisedSale->Rate) {
        $priceChanges[] = [
            'item' => $originalSale->Name,
            'old_rate' => $originalSale->Rate,
            'new_rate' => $revisedSale->Rate,
            'difference' => $revisedSale->Rate - $originalSale->Rate,
        ];
    }
}
```

### Comparison Report (Example)

```
QUOTATION COMPARISON REPORT
Original: 220716001 (July 16, 2022)
Revision: 220716001R001 (July 18, 2022)

CHANGES DETECTED:

Sale Item #1: Distribution Panel
├── Quantity: 2 → 3 (+1)
├── Rate: 50,000 → 48,000 (-2,000)
└── Amount: 100,000 → 144,000 (+44,000)

BOM Item: Circuit Breaker (Sale #1, BOM #1, Item #2)
├── Quantity: 12 → 15 (+3)
└── Rate: 1,500 → 1,400 (-100)

New Item Added: Cable Glands (Sale #1, BOM #2)
├── Quantity: 20
├── Rate: 150
└── Amount: 3,000

TOTALS:
Original: 2,500,000
Revision: 2,647,000
Difference: +147,000 (+5.88%)
```

---

## PDF Generation for Revisions

### PDF Header

```
┌────────────────────────────────────────────────────────────┐
│              NISH ELECTROMATION                             │
│          Electrical Equipment & Solutions                   │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ QUOTATION REVISION                                          │
│                                                             │
│ Quotation No: 220716001R001                                │
│ Revision Date: July 18, 2022                               │
│                                                             │
│ (Supersedes: Quotation #220716001 dated July 16, 2022)    │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### PDF Notes Section

```
REVISION NOTES:
- Updated pricing as per latest price list
- Quantity increased from 2 to 3 units
- Added cable glands as per client request
- Total revised to ₹26,47,000

Please refer to this revised quotation. 
Previous quotation #220716001 is now superseded.
```

---

## Troubleshooting

### Issue 1: Revision Number Error

**Error:** "Duplicate quotation number"

**Cause:** Two users creating revision simultaneously

**Solution:**
```php
// Add database transaction
DB::transaction(function() use ($id) {
    // Lock original quotation row
    $quotation = Quotation::where('QuotationId', $id)->lockForUpdate()->first();
    
    // Generate revision number
    // Create revision
    // Release lock
});
```

### Issue 2: Items Not Copied

**Symptom:** Revision created but no items

**Cause:** Status=1 (deleted) items in original

**Solution:** Only active items (Status=0) are copied - this is correct behavior

### Issue 3: Wrong Parent ID

**Symptom:** R002 points to R001 instead of original

**Cause:** Logic error in parent assignment

**Fix:** Already fixed in code above - always use original QuotationId

### Issue 4: Totals Incorrect

**Symptom:** Amounts don't match original

**Cause:** Stored procedure not called or failed

**Solution:** Ensure `quotationAmount()` called after copying data

---

## Best Practices

### When to Create Revision

✅ **DO create revision when:**
- Client requests changes
- Prices updated
- Significant scope change
- More than 1 week passed since original

❌ **DON'T create revision when:**
- Minor typo fixes (edit original)
- Same-day changes (edit original)
- Quotation not yet sent to client (edit original)

### Naming Revisions

**In PDF/Communication:**
- Quotation 220716001R001 (Revision 1)
- Revised Quotation 220716001R001
- Quotation 220716001 Rev. R001

**File Names:**
- Quotation_220716001R001_Rev1.pdf
- ABC_Industries_220716001_R001.pdf

### Communication

**Email Template:**
```
Dear [Client],

Please find attached our revised quotation 220716001R001.

This supersedes our previous quotation 220716001 dated July 16, 2022.

Key Changes:
- Updated pricing as per latest price list
- Quantity adjusted to 3 units as requested
- Added cable glands to scope

Please review and let us know if you have any questions.

Best regards,
[Sales Person]
```

---

## Summary

### Key Points

1. **Purpose:** Create modified version of quotation while preserving original

2. **Process:**
   - Click Revision button
   - System copies all data
   - New revision number assigned
   - Edit and save changes

3. **Numbering:** Original + R + sequential (220716001R001, R002, etc.)

4. **Data:** Complete copy of all sales, BOMs, and items

5. **Parent Link:** All revisions link back to original

6. **Independence:** Each version is separate and editable

7. **PDF:** Each version generates its own PDF

8. **Use Cases:** Price updates, quantity changes, scope modifications

### Technical Summary

**Database Operations:**
- 1 INSERT for quotation header
- N INSERTs for make/series
- N INSERTs for sales
- N×M INSERTs for BOMs
- N×M×P INSERTs for items
- 1 CALL to stored procedure

**Complexity:** O(n³) where n = average items per level

**Performance:** ~0.5-2 seconds for typical quotation

---

## Next Steps

**After Reading This:**
- Practice creating revisions
- Compare original vs revision
- Generate PDFs of both versions
- Understand parent-child relationships

**Related Documentation:**
- 17_QUOTATION_CREATION_FLOW.md - How to create original
- 21_PDF_GENERATION_FLOW.md - PDF details
- 07_QUOTATION_MODULE.md - Complete quotation system

---

**End of Document 18 - Quotation Revision Flow**

[← Back to Quotation Creation](17_QUOTATION_CREATION_FLOW.md) | [Next: BOM Creation Flow →](19_BOM_CREATION_FLOW.md)
