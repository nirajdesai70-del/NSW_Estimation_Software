> Source: source_snapshot/docs/05_WORKFLOWS/20_PRICING_CALCULATION_FLOW.md
> Bifurcated into: features/quotation/costing/20_PRICING_CALCULATION_FLOW.md
> Module: Quotation > Costing
> Date: 2025-12-17 (IST)

# Pricing Calculation Flow - Complete Mathematical Logic

**Document:** 20_PRICING_CALCULATION_FLOW.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Overview

**Purpose:** Understand how prices are calculated at every level in the quotation system.

**Calculation Levels:**
1. Item Level (individual products)
2. BOM Level (groups of items)
3. Sale Level (top-level services)
4. Quotation Level (overall total)

**Complexity:** Multi-level calculations with discounts, margins, and aggregations.

---

## 🧮 Complete Calculation Hierarchy

```
QUOTATION TOTAL
    ↑ SUM
    │
┌───┴────────────────────────────────────────────────────────────┐
│                                                                  │
SALE ITEM 1          SALE ITEM 2          SALE ITEM 3
Amount: $50,000      Amount: $75,000      Amount: $25,000
    ↑ SUM                ↑ SUM                ↑ SUM
    │                    │                    │
┌───┴──────────┐    ┌───┴──────────┐    ┌───┴──────────┐
│              │    │              │    │              │
BOM 1    BOM 2      BOM 3    BOM 4      BOM 5
$30K     $20K       $45K     $30K       $25K
↑ SUM    ↑ SUM     ↑ SUM    ↑ SUM     ↑ SUM
│        │         │        │         │
Items    Items     Items    Items     Items
(5)      (3)       (8)      (6)       (4)

Each Item: Qty × Rate × (1 - Discount%) = Amount
```

---

## 📊 Level 1: Item-Level Calculation

### Formula

```
Item Amount = Quantity × Net Rate

Where:
Net Rate = Base Rate × (1 - Discount/100)
```

### Detailed Breakdown

**Input Values:**
- **Quantity** (Qty): Number of units
- **Base Rate**: Price per unit (from prices table)
- **Discount %**: Discount percentage (0-100)

**Calculated Values:**
- **Net Rate**: Rate after discount
- **Amount**: Final amount for this item

### Example 1: Simple Calculation

**Item:** Circuit Breaker

**Input:**
```
Quantity: 10 pieces
Base Rate: $150 per piece
Discount: 0%
```

**Calculation:**
```
Net Rate = $150 × (1 - 0/100) = $150 × 1 = $150
Amount = 10 × $150 = $1,500
```

**Result:** $1,500

### Example 2: With Discount

**Item:** Cable

**Input:**
```
Quantity: 100 meters
Base Rate: $5 per meter
Discount: 10%
```

**Calculation:**
```
Step 1: Calculate Net Rate
Net Rate = $5 × (1 - 10/100)
Net Rate = $5 × (1 - 0.10)
Net Rate = $5 × 0.90
Net Rate = $4.50 per meter

Step 2: Calculate Amount
Amount = 100 meters × $4.50
Amount = $450
```

**Result:** $450 (saved $50 with discount)

### Example 3: Multiple Discounts (Sequential)

**Item:** Panel Enclosure

**Input:**
```
Quantity: 5 units
List Price: $1,000
Discount 1 (Item level): 5%
Discount 2 (BOM level): Additional 3%
```

**Calculation:**
```
Step 1: Apply first discount
Rate after Discount 1 = $1,000 × (1 - 5/100) = $950

Step 2: Apply second discount
Net Rate = $950 × (1 - 3/100) = $921.50

Step 3: Calculate amount
Amount = 5 × $921.50 = $4,607.50
```

**Result:** $4,607.50

### Code Implementation

```php
// File: resources/views/quotation/item.blade.php
// JavaScript calculation

function calculateItemAmount(itemId) {
    // Get values
    var qty = parseFloat($('#qty_' + itemId).val()) || 0;
    var rate = parseFloat($('#rate_' + itemId).val()) || 0;
    var discount = parseFloat($('#discount_' + itemId).val()) || 0;
    
    // Calculate net rate
    var netRate = rate * (1 - discount/100);
    $('#netrate_' + itemId).val(netRate.toFixed(2));
    
    // Calculate amount
    var amount = qty * netRate;
    $('#amount_' + itemId).val(amount.toFixed(2));
    
    // Trigger BOM calculation
    calculateBomTotal(bomId);
}
```

---

## 📊 Level 2: BOM-Level Calculation

### Formula

```
BOM Amount = SUM of all Item Amounts in BOM

BOM Amount = Item1.Amount + Item2.Amount + ... + ItemN.Amount
```

### Example: Panel Assembly BOM

**BOM Name:** "Panel Components"

**Items:**
```
Item 1: Panel Enclosure
  Qty: 1, Rate: $500, Discount: 0%
  Net Rate: $500
  Amount: $500

Item 2: Circuit Breakers
  Qty: 12, Rate: $50, Discount: 5%
  Net Rate: $50 × 0.95 = $47.50
  Amount: 12 × $47.50 = $570

Item 3: Busbar
  Qty: 1, Rate: $200, Discount: 0%
  Net Rate: $200
  Amount: $200

Item 4: Terminals
  Qty: 20, Rate: $5, Discount: 0%
  Net Rate: $5
  Amount: 20 × $5 = $100
```

**BOM Calculation:**
```
BOM Amount = $500 + $570 + $200 + $100 = $1,370
```

**BOM Total:** $1,370

### BOM Quantity Multiplier

**Important:** BOMs have their own quantity!

**Example:**
```
BOM: "Panel Assembly"
BOM Qty: 3  ← Three complete assemblies
Items in BOM:
  - Enclosure: Qty 1
  - Breakers: Qty 12
```

**Effective Quantities:**
```
Enclosure: 1 × 3 = 3 units total
Breakers: 12 × 3 = 36 units total
```

**Calculation:**
```
Per-BOM Amount = $1,370 (from above)
BOM Qty = 3
Total BOM Amount = $1,370 × 3 = $4,110
```

### Code Implementation

```php
// JavaScript: Calculate BOM total
function calculateBomTotal(bomId) {
    var total = 0;
    
    // Sum all items in this BOM
    $('.bom-item-' + bomId).each(function() {
        var itemAmount = parseFloat($(this).find('.item-amount').val()) || 0;
        total += itemAmount;
    });
    
    // Set BOM amount
    $('#bom_amount_' + bomId).val(total.toFixed(2));
    
    // Apply BOM quantity if needed
    var bomQty = parseFloat($('#bom_qty_' + bomId).val()) || 1;
    var bomTotal = total * bomQty;
    $('#bom_total_' + bomId).val(bomTotal.toFixed(2));
    
    // Trigger sale calculation
    calculateSaleTotal(saleId);
}
```

---

## 📊 Level 3: Sale-Level Calculation

### Formula

```
Sale Amount = SUM of all BOM Amounts for this Sale

OR (if no BOMs):

Sale Amount = Sale Qty × Sale Rate
```

### Example: Sale with Multiple BOMs

**Sale Item:** "Complete Panel System"

**Sale Qty:** 1 (one complete system)

**BOMs:**
```
BOM 1: Main Panel Components
  Items: 7 items
  BOM Amount: $2,500

BOM 2: Accessories
  Items: 5 items
  BOM Amount: $750

BOM 3: Installation Hardware
  Items: 3 items
  BOM Amount: $250
```

**Sale Calculation:**
```
Sale Amount = $2,500 + $750 + $250 = $3,500
```

### Example: Sale WITHOUT BOMs

**Sale Item:** "Engineering Services"

**Input:**
```
Sale Qty: 1
Sale Rate: $5,000
```

**Calculation:**
```
Sale Amount = 1 × $5,000 = $5,000
```

**No items breakdown needed.**

### Margin Calculation (Sale Level)

**Margin Fields:**
- Margin % (user input)
- Margin Amount (calculated)
- Margin Total (calculated)

**Formula:**
```
Margin Amount = Sale Amount × (Margin % / 100)
Margin Total = Sale Amount + Margin Amount
```

**Example:**
```
Sale Amount: $3,500
Margin %: 15%

Margin Amount = $3,500 × 0.15 = $525
Margin Total = $3,500 + $525 = $4,025
```

**Purpose:** Track profit margin on sales

---

## 📊 Level 4: Quotation-Level Calculation

### Formula (Basic)

```
Quotation Total = SUM of all Sale Amounts
```

### Formula (With Quotation-Level Discount)

```
Quotation Subtotal = SUM of all Sale Amounts
Quotation Discount Amount = Subtotal × (Discount % / 100)
Quotation Total = Subtotal - Discount Amount
```

### Example: Complete Quotation

**Sales:**
```
Sale 1: Distribution Panel System
  Amount: $50,000

Sale 2: Control Panel
  Amount: $30,000

Sale 3: Installation Services
  Amount: $15,000
```

**Calculation:**
```
Step 1: Sum all sales
Subtotal = $50,000 + $30,000 + $15,000 = $95,000

Step 2: Apply quotation-level discount
Quotation Discount: 5%
Discount Amount = $95,000 × 0.05 = $4,750

Step 3: Final total
Quotation Total = $95,000 - $4,750 = $90,250
```

**Result:** $90,250

### Stored Procedure: quotationAmount

**Purpose:** Calculate and update all quotation totals

**Trigger:** Called after quotation save/update

**What It Does:**
```sql
CALL quotationAmount(25);  -- QuotationId = 25
```

**Process (Estimated Logic):**
```sql
-- Stored procedure quotationAmount (approximate)

DELIMITER $$

CREATE PROCEDURE quotationAmount(IN quotationId INT)
BEGIN
    -- Calculate item amounts
    UPDATE quotation_sale_bom_items
    SET Amount = Qty * NetRate
    WHERE QuotationId = quotationId AND Status = 0;
    
    -- Calculate BOM amounts (sum of items)
    UPDATE quotation_sale_boms qsb
    SET Amount = (
        SELECT SUM(Amount)
        FROM quotation_sale_bom_items
        WHERE QuotationSaleBomId = qsb.QuotationSaleBomId
          AND Status = 0
    )
    WHERE QuotationId = quotationId AND Status = 0;
    
    -- Calculate sale amounts (sum of BOMs or direct)
    UPDATE quotation_sales qs
    SET Amount = (
        SELECT COALESCE(SUM(Amount), qs.Qty * qs.Rate)
        FROM quotation_sale_boms
        WHERE QuotationSaleId = qs.QuotationSaleId
          AND Status = 0
    )
    WHERE QuotationId = quotationId AND Status = 0;
    
    -- Calculate margins
    UPDATE quotation_sales
    SET MarginAmount = Amount * (Margin / 100),
        MarginTotal = Amount + (Amount * Margin / 100)
    WHERE QuotationId = quotationId AND Status = 0;
    
    -- Update quotation total (done in application layer)
END$$

DELIMITER ;
```

**Call from Controller:**
```php
// After saving quotation
DB::select("CALL quotationAmount(?)", [$quotationId]);
```

---

## 💰 Price Loading Logic

### How Prices are Retrieved

**Query Process:**
```php
// Controller: QuotationController@getPrice(Request $request)

public function getPrice(Request $request)
{
    $ProductId = $request->id;      // Specific product (with Make+Series)
    $date = date('Y-m-d');           // Current date
    
    // Get latest price effective on or before today
    $Rate = Price::where('ProductId', $ProductId)
        ->where('EffectiveDate', '<=', $date)
        ->orderBy('EffectiveDate', 'DESC')
        ->first();
    
    $data = [
        'rate' => $Rate ? $Rate->Rate : 0
    ];
    
    return response()->json($data);
}
```

### Price Selection Logic

**Scenario 1: Single Price**
```sql
SELECT * FROM prices WHERE ProductId = 455;

Result:
PriceId | ProductId | Rate  | EffectiveDate
--------|-----------|-------|---------------
1001    | 455       | 45000 | 2022-01-01
```
**Selected Price:** $45,000 (only option)

**Scenario 2: Multiple Prices (History)**
```sql
SELECT * FROM prices WHERE ProductId = 455 ORDER BY EffectiveDate DESC;

Result:
PriceId | ProductId | Rate  | EffectiveDate
--------|-----------|-------|---------------
1003    | 455       | 42000 | 2022-07-01  ← Latest, but future
1002    | 455       | 45000 | 2022-05-01  ← SELECTED (current)
1001    | 455       | 48000 | 2022-01-01  ← Old price
```

**Query:**
```sql
SELECT Rate FROM prices
WHERE ProductId = 455
  AND EffectiveDate <= '2022-06-15'  -- Today's date
ORDER BY EffectiveDate DESC
LIMIT 1;
```

**Selected Price:** $45,000 (effective May 1, current on June 15)

**Scenario 3: Future-Dated Price**
```sql
-- Today is June 15, 2022

Prices:
PriceId | Rate  | EffectiveDate
--------|-------|---------------
1002    | 42000 | 2022-08-01  ← Future (not used yet)
1001    | 45000 | 2022-05-01  ← SELECTED (current)
```

**Selected:** $45,000 (future price not active yet)

**On August 1, 2022:**
- Price becomes $42,000 automatically

---

## 🎯 Complete Calculation Examples

### Example 1: Simple Quotation

**Quotation: Single item, no BOM**

**Structure:**
```
Quotation #220716001
└── Sale 1: "Engineering Consultation"
    Qty: 1
    Rate: $5,000
    Discount: 0%
```

**Calculation:**
```
Item Level:
  Net Rate = $5,000 × (1 - 0%) = $5,000
  Amount = 1 × $5,000 = $5,000

Sale Level:
  Amount = $5,000 (no BOMs, uses sale amount directly)

Quotation Level:
  Total = $5,000
```

**Final Total:** $5,000

---

### Example 2: Single Sale with BOM

**Quotation: One sale item with BOM**

**Structure:**
```
Quotation #220716002
└── Sale 1: "Distribution Panel"
    Sale Qty: 2
    └── BOM 1: "Panel Components"
        BOM Qty: 1
        ├── Item 1: Enclosure
        │   Qty: 1, Rate: $800, Discount: 0%
        ├── Item 2: Breakers
        │   Qty: 12, Rate: $60, Discount: 5%
        └── Item 3: Busbar
            Qty: 1, Rate: $300, Discount: 0%
```

**Calculation:**

**Level 1 - Items:**
```
Item 1 (Enclosure):
  Net Rate = $800 × (1 - 0%) = $800
  Amount = 1 × $800 = $800

Item 2 (Breakers):
  Net Rate = $60 × (1 - 5%) = $60 × 0.95 = $57
  Amount = 12 × $57 = $684

Item 3 (Busbar):
  Net Rate = $300 × (1 - 0%) = $300
  Amount = 1 × $300 = $300
```

**Level 2 - BOM:**
```
BOM 1 Amount = $800 + $684 + $300 = $1,784
BOM Qty = 1
BOM Total = $1,784 × 1 = $1,784
```

**Level 3 - Sale:**
```
Sale Amount = BOM Total = $1,784
Sale Qty = 2  ← Important multiplier!
Sale Total = $1,784 × 2 = $3,568
```

**Level 4 - Quotation:**
```
Quotation Total = $3,568
```

**Final Total:** $3,568

---

### Example 3: Complex Multi-Level

**Quotation: Multiple sales, multiple BOMs**

**Structure:**
```
Quotation #220716003
├── Sale 1: "Main Panel"
│   Sale Qty: 2
│   ├── BOM 1: "Panel Core"
│   │   BOM Qty: 1
│   │   ├── Item 1: Enclosure ($800)
│   │   └── Item 2: Breaker ($684)
│   └── BOM 2: "Accessories"
│       BOM Qty: 1
│       └── Item 3: Glands ($150)
│
├── Sale 2: "Sub-Panel"
│   Sale Qty: 3
│   └── BOM 3: "Sub-Panel Components"
│       BOM Qty: 1
│       ├── Item 4: Enclosure ($400)
│       └── Item 5: MCBs ($240)
│
└── Sale 3: "Installation"
    Qty: 1, Rate: $2,000 (no BOM)
```

**Complete Calculation:**

**Sale 1 - Main Panel:**
```
BOM 1 (Panel Core):
  Item 1: 1 × $800 = $800
  Item 2: 12 × $57 = $684
  BOM 1 Total = $1,484

BOM 2 (Accessories):
  Item 3: 10 × $15 = $150
  BOM 2 Total = $150

Sale 1 Subtotal = $1,484 + $150 = $1,634
Sale 1 Qty = 2
Sale 1 Amount = $1,634 × 2 = $3,268
```

**Sale 2 - Sub-Panel:**
```
BOM 3 (Sub-Panel Components):
  Item 4: 1 × $400 = $400
  Item 5: 6 × $40 = $240
  BOM 3 Total = $640

Sale 2 Subtotal = $640
Sale 2 Qty = 3
Sale 2 Amount = $640 × 3 = $1,920
```

**Sale 3 - Installation:**
```
No BOM
Sale 3 Qty = 1
Sale 3 Rate = $2,000
Sale 3 Amount = 1 × $2,000 = $2,000
```

**Quotation Total:**
```
Subtotal = $3,268 + $1,920 + $2,000 = $7,188

Apply Quotation Discount: 5%
Discount Amount = $7,188 × 0.05 = $359.40

Final Total = $7,188 - $359.40 = $6,828.60
```

**Final Total:** $6,828.60

---

## 💡 Advanced Calculations

### Margin Calculation

**Purpose:** Track profit margin on sales

**Formula:**
```
Margin Amount = Sale Amount × (Margin % / 100)
Margin Total = Sale Amount + Margin Amount
```

**Example:**
```
Sale Amount: $10,000
Margin %: 20%

Margin Amount = $10,000 × 0.20 = $2,000
Margin Total = $10,000 + $2,000 = $12,000
```

**Usage:**
- Internal tracking (not shown to client)
- Profit analysis
- Pricing strategy

### Tax Calculation (If Implemented)

**Typical Tax Structure:**
```
Subtotal:           $100,000
Discount (5%):      - $5,000
                    ─────────
After Discount:      $95,000

GST (18%):          + $17,100
                    ─────────
Final Total:        $112,100
```

**Code (If Implemented):**
```php
$subtotal = $quotationAmount;
$discount = $subtotal * ($discountPercent / 100);
$afterDiscount = $subtotal - $discount;
$gst = $afterDiscount * 0.18; // 18% GST
$finalTotal = $afterDiscount + $gst;
```

### Rounding

**System Rounding:**
- All amounts rounded to 2 decimal places
- Uses standard rounding (0.5 rounds up)
- PHP: `round($amount, 2)` or `number_format($amount, 2)`

**Example:**
```
Calculated: $1,234.567
Displayed: $1,234.57

Calculated: $1,234.564
Displayed: $1,234.56
```

---

## 🔄 Recalculation Triggers

### When Amounts Recalculate:

**1. Item Quantity Change**
```
User changes Qty: 10 → 15
↓
Item Amount recalculates
↓
BOM Amount recalculates
↓
Sale Amount recalculates
↓
Quotation Total recalculates
```

**2. Item Rate Change**
```
User changes Rate: $100 → $95
↓
Net Rate recalculates
↓
Item Amount recalculates
↓
... cascades up ...
```

**3. Discount Applied**
```
User adds Discount: 0% → 10%
↓
Net Rate recalculates
↓
Item Amount recalculates
↓
... cascades up ...
```

**4. Item Added/Removed**
```
User adds new item to BOM
↓
BOM Amount increases
↓
Sale Amount increases
↓
Quotation Total increases
```

**5. BOM Quantity Change**
```
User changes BOM Qty: 1 → 2
↓
BOM Total doubles
↓
Sale Amount doubles
↓
Quotation Total increases
```

### Code: Cascade Calculation

```javascript
// Event handlers for recalculation

// Item field change
$('.item-qty, .item-rate, .item-discount').on('change', function() {
    var itemId = $(this).data('item-id');
    var bomId = $(this).data('bom-id');
    var saleId = $(this).data('sale-id');
    
    calculateItemAmount(itemId);      // Level 1
    calculateBomTotal(bomId);         // Level 2
    calculateSaleTotal(saleId);       // Level 3
    calculateQuotationTotal();        // Level 4
});

// BOM quantity change
$('.bom-qty').on('change', function() {
    var bomId = $(this).data('bom-id');
    var saleId = $(this).data('sale-id');
    
    calculateBomTotal(bomId);         // Level 2
    calculateSaleTotal(saleId);       // Level 3
    calculateQuotationTotal();        // Level 4
});

// Sale quantity change
$('.sale-qty').on('change', function() {
    var saleId = $(this).data('sale-id');
    
    calculateSaleTotal(saleId);       // Level 3
    calculateQuotationTotal();        // Level 4
});
```

---

## 📊 Detailed Calculation Walkthrough

### Real-World Example: Panel Quotation

**Scenario:** Client needs 3 distribution panels

**Step-by-Step:**

**1. Create Quotation**
- Client: "Tech Industries"
- Project: "Factory Setup"
- QuotationNo: 220716005

**2. Add Sale Item**
- Sale Name: "Distribution Panel 100A"
- Sale Qty: 3 panels

**3. Add BOM using Master BOM**
- Select: "Standard Distribution Panel - 100A"
- Master BOM has 7 items
- System copies all 7 items

**4. Items Copied (with calculations):**

```
Item 1: Panel Enclosure
  ProductId: 305 (Generic: "Panel Enclosure Indoor")
  User selects Make: Siemens
  User selects Series: SIVACON S8
  System loads Rate: $800
  Qty: 1 (from Master BOM)
  Discount: 0%
  Net Rate: $800
  Amount: 1 × $800 = $800

Item 2: Main Circuit Breaker 100A
  ProductId: 310
  Make: ABB
  Series: Tmax XT
  Rate: $600 (auto-loaded)
  Qty: 1
  Discount: 5%
  Net Rate: $600 × 0.95 = $570
  Amount: 1 × $570 = $570

Item 3: Branch MCB 10A
  ProductId: 315
  Make: Schneider
  Series: Easy9
  Rate: $50 (auto-loaded)
  Qty: 12
  Discount: 10%
  Net Rate: $50 × 0.90 = $45
  Amount: 12 × $45 = $540

Item 4: Busbar 100A
  ProductId: 320
  Rate: $300
  Qty: 1
  Net Rate: $300
  Amount: $300

Item 5: Terminal Blocks
  ProductId: 325
  Rate: $8
  Qty: 24
  Net Rate: $8
  Amount: 24 × $8 = $192

Item 6: Cable Glands
  ProductId: 330
  Rate: $12
  Qty: 8
  Net Rate: $12
  Amount: 8 × $12 = $96

Item 7: Earthing Kit
  ProductId: 335
  Rate: $150
  Qty: 1
  Net Rate: $150
  Amount: $150
```

**5. BOM Calculation:**
```
BOM Amount = $800 + $570 + $540 + $300 + $192 + $96 + $150
BOM Amount = $2,648 (per panel)

BOM Qty = 1 (standard)
BOM Total = $2,648
```

**6. Sale Calculation:**
```
Sale Amount (per unit) = $2,648
Sale Qty = 3 panels
Sale Total = $2,648 × 3 = $7,944
```

**7. Apply Margin (Internal):**
```
Margin % = 15%
Margin Amount = $7,944 × 0.15 = $1,191.60
Margin Total = $7,944 + $1,191.60 = $9,135.60
```

**8. Quotation Total:**
```
Only one sale item
Quotation Total = $7,944 (before margin)
Or $9,135.60 (with margin - if shown to client)
```

**9. Apply Quotation Discount:**
```
Quotation Discount: 5% (special client discount)
Discount Amount = $7,944 × 0.05 = $397.20
Final Total = $7,944 - $397.20 = $7,546.80
```

**FINAL QUOTATION TOTAL:** $7,546.80

**Client Sees:** $7,546.80  
**Internal Margin:** $1,191.60 (15% profit tracked internally)

---

## 🎓 Pricing Strategy Tips

### For Accurate Quotations:

**1. Keep Prices Updated:**
- Regular price reviews
- Update effective dates
- Monitor competitor pricing

**2. Use Effective Dates:**
- Future-date price increases
- System applies automatically
- No manual intervention

**3. Discount Strategy:**
- Item-level: Bulk purchase discounts
- BOM-level: Assembly discounts
- Sale-level: Product line discounts
- Quotation-level: Client relationship discounts

**4. Margin Management:**
- Track margins per sale
- Analyze profitability
- Adjust pricing strategy
- Balance competitiveness vs profit

---

## 🐛 Troubleshooting

### Issue 1: "Amount shows as 0.00"
**Causes:**
- Rate not set (no price in database)
- Quantity is 0
- JavaScript error

**Check:**
```javascript
console.log('Qty:', qty, 'Rate:', rate, 'Amount:', qty * rate);
```

**Solution:**
- Ensure product has price in price table
- Verify quantity > 0
- Check browser console for errors

### Issue 2: "BOM total doesn't match items"
**Cause:** JavaScript calculation not triggered
**Solution:**
- Manually trigger recalculation
- Refresh page and re-enter amounts
- Check JavaScript console for errors

### Issue 3: "Quotation total wrong"
**Cause:** Stored procedure not called or error in procedure
**Solution:**
```php
// Manually recalculate
DB::select("CALL quotationAmount(?)", [$quotationId]);
```

### Issue 4: "Price from last year showing"
**Cause:** No current price, using old effective date
**Solution:**
- Add new price with current effective date
- Or update existing price effective date

### Issue 5: "Discount not applying"
**Cause:** Discount field not saving or calculation error
**Check:**
```sql
SELECT Discount, Rate, NetRate, Amount 
FROM quotation_sale_bom_items 
WHERE QuotationSaleBomItemId = ?;
```

**Verify:**
- NetRate = Rate × (1 - Discount/100)
- Amount = Qty × NetRate

---

## 📊 Summary

### Calculation Flow:
```
Item → BOM → Sale → Quotation
 ↓       ↓      ↓        ↓
$100   $500  $1,500   $5,000
```

### Key Formulas:
```
Item:      Amount = Qty × Rate × (1 - Discount%)
BOM:       Amount = SUM(Items) × BOM Qty
Sale:      Amount = SUM(BOMs) × Sale Qty OR Qty × Rate
Quotation: Total = SUM(Sales) × (1 - Discount%)
```

### Calculation Triggers:
- ✅ Field changes (automatic)
- ✅ Item add/remove (automatic)
- ✅ Save quotation (stored procedure)
- ✅ Manual refresh (if needed)

### Price Sources:
- ✅ Price table (ProductId + latest EffectiveDate)
- ✅ Manual entry (override allowed)
- ✅ Import from Excel (bulk updates)

---

## 🔗 Related Documents

- **17_QUOTATION_CREATION_FLOW.md** - Where prices are used
- **11_PRICING_MODULE.md** - Price management
- **04_DATABASE_SCHEMA.md** - Price table structure
- **28_BUSINESS_RULES.md** - Pricing rules and policies

---

**End of Document 20 - Pricing Calculation Flow**

[← Back: BOM Creation](19_BOM_CREATION_FLOW.md) | [Next: PDF Generation Flow →](21_PDF_GENERATION_FLOW.md)

