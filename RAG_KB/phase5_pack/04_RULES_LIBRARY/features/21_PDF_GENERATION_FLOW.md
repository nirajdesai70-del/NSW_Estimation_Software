---
Source: features/quotation/reports/21_PDF_GENERATION_FLOW.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T01:31:07.528201
KB_Path: phase5_pack/04_RULES_LIBRARY/features/21_PDF_GENERATION_FLOW.md
---

> Source: source_snapshot/docs/05_WORKFLOWS/21_PDF_GENERATION_FLOW.md
> Bifurcated into: features/quotation/reports/21_PDF_GENERATION_FLOW.md
> Module: Quotation > Reports
> Date: 2025-12-17 (IST)

# PDF Generation Flow - Quotation Document Creation

**Document:** 21_PDF_GENERATION_FLOW.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## 📋 Overview

**Purpose:** Generate professional PDF quotation documents for clients.

**Library Used:** DomPDF (Laravel wrapper)

**Output:** Formatted PDF with company branding, quotation details, and pricing.

---

## 🔄 Complete PDF Generation Workflow

```
START: User wants PDF of quotation
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│ QUOTATION LIST PAGE                                             │
│ User finds quotation                                            │
│ Clicks PDF icon (document icon)                                │
└────────────────────────────────────────────────────────────────┘
         │
         │ GET /quotation/pdf/{id}
         ▼
┌────────────────────────────────────────────────────────────────┐
│ PDF GENERATION PROCESS                                          │
│ Controller: QuotationController@quotationPdf($id)              │
│                                                                 │
│ PHASE 1: DATA LOADING                                          │
│ ├─ Load quotation record                                       │
│ ├─ Load client details                                         │
│ ├─ Load project details                                        │
│ ├─ Load contact details                                        │
│ ├─ Load sales person                                           │
│ ├─ Load employee                                               │
│ └─ Load all sale items + BOMs + items (nested)                │
│                                                                 │
│ PHASE 2: DATA STRUCTURING                                      │
│ ├─ Organize data in hierarchical array                        │
│ ├─ Calculate totals at each level                             │
│ └─ Format numbers for display                                  │
│                                                                 │
│ PHASE 3: TEMPLATE RENDERING                                    │
│ ├─ Load Blade template: quotationPDF.blade.php                │
│ ├─ Pass all data to template                                   │
│ └─ Render HTML with data                                       │
│                                                                 │
│ PHASE 4: PDF CONVERSION                                        │
│ ├─ DomPDF converts HTML to PDF                                 │
│ ├─ Apply formatting (paper size, margins)                      │
│ └─ Generate PDF file                                           │
│                                                                 │
│ PHASE 5: DELIVERY                                              │
│ └─ Download PDF to user's browser                             │
└────────────────────────────────────────────────────────────────┘
         │
         │ PDF file downloaded
         ▼
┌────────────────────────────────────────────────────────────────┐
│ PDF FILE READY                                                  │
│ Filename: Quotation_220716001.pdf                              │
│ Size: ~200-500 KB                                              │
│ Format: A4 Portrait                                            │
│ Ready to email to client                                       │
└────────────────────────────────────────────────────────────────┘

END OF WORKFLOW
```

---

## 💻 Complete Technical Implementation

### PDF Controller Method (Full Code)

```php
// File: app/Http/Controllers/QuotationController.php
// Method: quotationPdf($id)
// Line: ~1600-1750

public function quotationPdf($id)
{
    // PHASE 1: LOAD MAIN QUOTATION DATA
    $quotation = Quotation::where('QuotationId', $id)->first();
    
    if(!$quotation) {
        return redirect()->back()->with('error', 'Quotation not found');
    }
    
    // PHASE 2: LOAD RELATED DATA
    
    // Client Information
    $customer = Client::where('ClientId', $quotation->ClientId)->first();
    
    // Contact Person
    $contact = Contact::where('ContactId', $quotation->ContactId)->first();
    
    // Sales Person
    $sales = User::where('id', $quotation->SalesId)->first();
    
    // Project
    $project = Project::where('ProjectId', $quotation->ProjectId)->first();
    
    // Employee
    $employee = User::where('id', $quotation->EmployeeId)->first();
    
    // Company/Organization
    $company = Organization::first(); // Company details for header
    
    // PHASE 3: LOAD QUOTATION STRUCTURE
    
    // Get all sale items
    $quotationSaleData = DB::select(
        'SELECT (ROW_NUMBER() OVER(ORDER BY qs.QuotationSaleId ASC)) AS srno,
                qs.QuotationSaleId, qs.Name, qs.SaleCustomName, 
                qs.Qty, qs.Amount, qs.Rate
         FROM quotation_sales qs
         WHERE qs.QuotationId = ? AND qs.Status = 0',
        [$id]
    );
    
    // Calculate total quantity and amount
    $totalQty = DB::select(
        'SELECT SUM(qs.Qty) as totalQty, 
                SUM(qs.Qty * qs.Rate) as totalAmount
         FROM quotation_sales qs
         WHERE qs.QuotationId = ? AND qs.Status = 0',
        [$id]
    );
    
    // PHASE 4: BUILD NESTED DATA STRUCTURE
    $allData = [];
    
    if(count($quotationSaleData) > 0) {
        foreach($quotationSaleData as $data) {
            $QuotationSaleId = $data->QuotationSaleId;
            
            // Sale item data
            $sale = [
                'Name' => $data->Name,
                'SaleCustomName' => $data->SaleCustomName,
                'Qty' => $data->Qty,
                'Bom' => []
            ];
            
            // Get BOMs for this sale
            $SelectedBom = DB::select(
                "SELECT mb.QuotationSaleId, mb.QuotationSaleBomId, 
                        mb.MasterBomId, mb.MasterBomName, mb.Qty, 
                        mb.Rate, mb.Amount
                 FROM quotation_sale_boms mb
                 WHERE mb.QuotationId = ? 
                   AND mb.QuotationSaleId = ? 
                   AND mb.Status = 0",
                [$id, $QuotationSaleId]
            );
            
            foreach($SelectedBom as $bom) {
                $bomData = [
                    'MasterBomName' => $bom->MasterBomName,
                    'Qty' => $bom->Qty,
                    'Items' => []
                ];
                
                $QuotationSaleBomId = $bom->QuotationSaleBomId;
                
                // Get items for this BOM
                $SelectedItem = DB::select(
                    'SELECT (ROW_NUMBER() OVER(PARTITION BY mb.QuotationSaleBomId 
                            ORDER BY mbi.QuotationSaleBomItemId)) AS srno,
                            (SELECT c.Name FROM products c WHERE c.ProductId=pr.ProductId) AS GenericName,
                            (SELECT m.Name FROM makes m WHERE m.MakeId=mbi.MakeId) AS MakeName,
                            (SELECT s.Name FROM series s WHERE s.SeriesId=mbi.SeriesId) AS SeriesName,
                            (SELECT p.SKU FROM products p WHERE p.ProductId=mbi.Description) AS SKU, 
                            mbi.Remark, mbi.Qty
                     FROM quotation_sale_boms mb
                     JOIN quotation_sale_bom_items mbi ON mbi.QuotationSaleBomId=mb.QuotationSaleBomId
                     JOIN products pr ON pr.ProductId=mbi.ProductId
                     WHERE mb.QuotationId = ? 
                       AND mbi.QuotationSaleBomId = ? 
                       AND mbi.Status = 0',
                    [$id, $QuotationSaleBomId]
                );
                
                foreach($SelectedItem as $item) {
                    $bomData['Items'][] = [
                        'srno' => $item->srno,
                        'GenericName' => $item->GenericName,
                        'MakeName' => $item->MakeName,
                        'SeriesName' => $item->SeriesName,
                        'SKU' => $item->SKU,
                        'Remark' => $item->Remark,
                        'Qty' => $item->Qty,
                    ];
                }
                
                $sale['Bom'][] = $bomData;
            }
            
            $allData[] = $sale;
        }
    }
    
    // PHASE 5: RENDER PDF
    $pdf = PDF::loadView('quotation.quotationPDF', compact(
        'quotation',
        'customer',
        'contact',
        'sales',
        'project',
        'employee',
        'company',
        'allData',
        'totalQty'
    ));
    
    // PHASE 6: CONFIGURE PDF SETTINGS
    $pdf->setPaper('A4', 'portrait');
    $pdf->setOptions([
        'isHtml5ParserEnabled' => true,
        'isRemoteEnabled' => true,
        'defaultFont' => 'Arial',
        'dpi' => 150,
    ]);
    
    // PHASE 7: DOWNLOAD
    $filename = 'Quotation_' . $quotation->QuotationNo . '.pdf';
    return $pdf->download($filename);
}
```

---

## 📄 PDF Template Structure

### Template File
**Location:** `resources/views/quotation/quotationPDF.blade.php`

**Structure:**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Quotation {{ $quotation->QuotationNo }}</title>
    <style>
        /* PDF-specific CSS */
        body { font-family: Arial, sans-serif; font-size: 12px; }
        .header { text-align: center; margin-bottom: 20px; }
        .company-logo { width: 150px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #000; padding: 5px; }
        .total-row { font-weight: bold; background: #f0f0f0; }
    </style>
</head>
<body>
    <!-- COMPANY HEADER -->
    <div class="header">
        <h1>NISH ELECTROMATION</h1>
        <p>Address Line 1, City, State, PIN</p>
        <p>Phone: +91-XXXXXXXXXX | Email: info@nish.com</p>
        <p>GST: XXXXXXXXXXXX</p>
    </div>
    
    <!-- QUOTATION HEADER -->
    <h2>QUOTATION</h2>
    <table>
        <tr>
            <td><strong>Quotation No:</strong></td>
            <td>{{ $quotation->QuotationNo }}</td>
            <td><strong>Date:</strong></td>
            <td>{{ date('d-M-Y', strtotime($quotation->created_at)) }}</td>
        </tr>
    </table>
    
    <!-- CLIENT DETAILS -->
    <h3>TO:</h3>
    <table>
        <tr>
            <td><strong>Company:</strong></td>
            <td>{{ $customer->ClientName }}</td>
        </tr>
        <tr>
            <td><strong>Attention:</strong></td>
            <td>{{ $contact->ContactName }}</td>
        </tr>
        <tr>
            <td><strong>Address:</strong></td>
            <td>{{ $customer->Address }}</td>
        </tr>
        <tr>
            <td><strong>Contact:</strong></td>
            <td>{{ $contact->Mobile }}</td>
        </tr>
        <tr>
            <td><strong>Email:</strong></td>
            <td>{{ $contact->Email }}</td>
        </tr>
    </table>
    
    <!-- PROJECT DETAILS -->
    <table>
        <tr>
            <td><strong>Project:</strong></td>
            <td>{{ $project->Name }}</td>
        </tr>
        <tr>
            <td><strong>Location:</strong></td>
            <td>{{ $project->Location }}</td>
        </tr>
    </table>
    
    <!-- QUOTATION ITEMS -->
    <h3>Items & Pricing:</h3>
    
    <table>
        <thead>
            <tr>
                <th>Sr</th>
                <th>Description</th>
                <th>Make/Series</th>
                <th>SKU</th>
                <th>Qty</th>
                <th>Rate</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
            @php $srno = 1; @endphp
            
            @foreach($allData as $sale)
                <!-- Sale Item Header -->
                <tr class="sale-row">
                    <td>{{ $srno++ }}</td>
                    <td colspan="6">
                        <strong>{{ $sale['SaleCustomName'] ?? $sale['Name'] }}</strong>
                    </td>
                </tr>
                
                @foreach($sale['Bom'] as $bom)
                    <!-- BOM Header -->
                    <tr class="bom-row">
                        <td></td>
                        <td colspan="6">
                            <em>{{ $bom['MasterBomName'] }}</em>
                        </td>
                    </tr>
                    
                    @foreach($bom['Items'] as $item)
                        <!-- BOM Item -->
                        <tr>
                            <td>{{ $item['srno'] }}</td>
                            <td>{{ $item['GenericName'] }}</td>
                            <td>{{ $item['MakeName'] }} {{ $item['SeriesName'] }}</td>
                            <td>{{ $item['SKU'] }}</td>
                            <td>{{ $item['Qty'] }}</td>
                            <td>{{ number_format($item['Rate'], 2) }}</td>
                            <td>{{ number_format($item['Amount'], 2) }}</td>
                        </tr>
                    @endforeach
                @endforeach
            @endforeach
            
            <!-- TOTAL ROW -->
            <tr class="total-row">
                <td colspan="6" align="right"><strong>TOTAL:</strong></td>
                <td><strong>{{ number_format($totalQty[0]->totalAmount, 2) }}</strong></td>
            </tr>
        </tbody>
    </table>
    
    <!-- TERMS & CONDITIONS -->
    <h3>Terms & Conditions:</h3>
    <ol>
        <li>Delivery: 4-6 weeks from order confirmation</li>
        <li>Payment: 50% advance, 50% on delivery</li>
        <li>Warranty: 12 months from delivery</li>
        <li>Validity: This quotation is valid for 30 days</li>
        <li>Freight: Extra as applicable</li>
        <li>Installation: Extra as per actual</li>
    </ol>
    
    <!-- FOOTER -->
    <div class="footer">
        <p>For NISH ELECTROMATION</p>
        <br><br>
        <p>_______________________</p>
        <p>Authorized Signatory</p>
        <br>
        <p>Sales Person: {{ $sales->name }}</p>
        <p>Date: {{ date('d-M-Y') }}</p>
    </div>
</body>
</html>
```

---

## 🎨 PDF Layout Variations

### PrintType 0 vs PrintType 1

**System supports two PDF formats:**

**PrintType 0: Detailed View (Default)**
- Shows all sales, BOMs, and items
- Complete breakdown
- Used for: Technical specifications, detailed quotes

**PrintType 1: Simplified View**
- Shows only sale items
- Hides BOM/item breakdown
- Used for: Simple quotes, price comparison

**Code Check:**
```php
if($quotation->PrintType == 0) {
    // Show full breakdown
} else {
    // Show simplified
}
```

---

## 🔧 PDF Configuration

### DomPDF Settings

**Paper Size:**
```php
$pdf->setPaper('A4', 'portrait');
// Options: A4, Letter, Legal
// Orientation: portrait, landscape
```

**Options:**
```php
$pdf->setOptions([
    'isHtml5ParserEnabled' => true,    // Use HTML5 parser
    'isRemoteEnabled' => true,          // Allow remote images
    'defaultFont' => 'Arial',           // Default font
    'dpi' => 150,                       // Print quality
    'isFontSubsettingEnabled' => true,  // Reduce file size
]);
```

### CSS for PDF

**Best Practices:**

**✅ Do:**
- Use inline styles or `<style>` tags
- Use absolute units (px, pt)
- Keep layouts simple
- Use tables for alignment
- Test rendering frequently

**❌ Don't:**
- Use external CSS files (may not load)
- Use complex flexbox/grid
- Use JavaScript
- Use web fonts (unless embedded)
- Assume pixel-perfect rendering

**Example CSS:**
```css
/* Good for PDF */
body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12pt;
    margin: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}

th, td {
    border: 1px solid #000;
    padding: 8px;
    text-align: left;
}

.header {
    text-align: center;
    margin-bottom: 30px;
    border-bottom: 2px solid #000;
}

.total-row {
    background-color: #f0f0f0;
    font-weight: bold;
}

@page {
    margin: 2cm;
}
```

---

## 📊 Data Structure for PDF

### Hierarchical Data Array

```php
$allData = [
    [
        'Name' => 'Distribution Panel System',
        'SaleCustomName' => 'DP-100A Complete Assembly',
        'Qty' => 2,
        'Bom' => [
            [
                'MasterBomName' => 'Panel Components',
                'Qty' => 1,
                'Items' => [
                    [
                        'srno' => 1,
                        'GenericName' => 'Panel Enclosure',
                        'MakeName' => 'Siemens',
                        'SeriesName' => 'SIVACON S8',
                        'SKU' => 'SIV-S8-100A',
                        'Remark' => 'IP54 rated',
                        'Qty' => 1,
                        'Rate' => 800,
                        'Amount' => 800
                    ],
                    [
                        'srno' => 2,
                        'GenericName' => 'Circuit Breaker',
                        'MakeName' => 'ABB',
                        'SeriesName' => 'Tmax XT',
                        'SKU' => 'XT1N-160',
                        'Remark' => '100A rated',
                        'Qty' => 1,
                        'Rate' => 600,
                        'Amount' => 600
                    ],
                    // ... more items
                ]
            ],
            // ... more BOMs
        ]
    ],
    // ... more sale items
];
```

### Rendering Loop

```blade
@foreach($allData as $saleIndex => $sale)
    <tr>
        <td colspan="7">
            <strong>{{ $sale['SaleCustomName'] }}</strong>
        </td>
    </tr>
    
    @foreach($sale['Bom'] as $bomIndex => $bom)
        <tr>
            <td></td>
            <td colspan="6">
                <em>{{ $bom['MasterBomName'] }}</em>
            </td>
        </tr>
        
        @foreach($bom['Items'] as $itemIndex => $item)
            <tr>
                <td>{{ $item['srno'] }}</td>
                <td>{{ $item['GenericName'] }}</td>
                <td>{{ $item['MakeName'] }} {{ $item['SeriesName'] }}</td>
                <td>{{ $item['SKU'] }}</td>
                <td>{{ $item['Qty'] }}</td>
                <td>{{ number_format($item['Rate'], 2) }}</td>
                <td>{{ number_format($item['Amount'], 2) }}</td>
            </tr>
        @endforeach
    @endforeach
@endforeach
```

---

## 🎨 PDF Customization Options

### Company Branding

**Add Logo:**
```html
<div class="header">
    <img src="{{ public_path('images/company-logo.png') }}" 
         alt="Company Logo" 
         style="width: 200px;">
</div>
```

**Company Info:**
```php
// Load from organization table
$company = Organization::first();

// In template:
{{ $company->Name }}
{{ $company->Address }}
{{ $company->Phone }}
{{ $company->Email }}
{{ $company->GSTNo }}
```

### Custom Terms & Conditions

**Dynamic Terms:**
```php
// Load from settings table
$terms = Setting::where('Key', 'quotation_terms')->first();

// In template:
{!! $terms->Value !!}  // HTML content
```

**Per-Client Terms:**
```php
// Load client-specific terms
$clientTerms = Client::find($clientId)->QuotationTerms;
```

### Watermark (Draft/Final)

```css
.watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 100px;
    color: rgba(0,0,0,0.1);
    z-index: -1;
}
```

```html
@if($quotation->Status == 0)
    <div class="watermark">DRAFT</div>
@endif
```

---

## 🐛 Troubleshooting

### Issue 1: "PDF shows blank or errors"
**Causes:**
- Template syntax error
- Missing data
- DomPDF rendering issue

**Debug:**
```php
// Instead of ->download(), use ->stream() for browser view
return $pdf->stream($filename);

// Or render HTML only (no PDF)
return view('quotation.quotationPDF', compact(...));
```

**Check:** Laravel log at `storage/logs/laravel.log`

### Issue 2: "Images not showing"
**Cause:** Relative paths don't work in PDF
**Solution:**
```php
// Use absolute paths
<img src="{{ public_path('images/logo.png') }}">

// Or base64 encode
<img src="data:image/png;base64,{{ base64_encode(file_get_contents(public_path('images/logo.png'))) }}">
```

### Issue 3: "Layout broken in PDF"
**Cause:** CSS not compatible with DomPDF
**Solution:**
- Avoid complex CSS
- Use tables for layout
- Test frequently
- Simplify styling

### Issue 4: "PDF file too large"
**Cause:** High-resolution images, large tables
**Solution:**
- Optimize images
- Reduce DPI setting
- Enable font subsetting

### Issue 5: "Special characters display wrong"
**Cause:** Encoding issues
**Solution:**
```html
<meta charset="UTF-8">
```
```php
$pdf->setOptions(['isUnicode' => true]);
```

---

## ⚡ Performance Optimization

### For Large Quotations

**Problem:** 100+ items = slow PDF generation

**Solutions:**

**1. Eager Loading:**
```php
$quotation = Quotation::with([
    'client',
    'project',
    'contact',
    'sales' => function($q) {
        $q->where('Status', 0);
    },
    'sales.boms' => function($q) {
        $q->where('Status', 0);
    },
    'sales.boms.items' => function($q) {
        $q->where('Status', 0);
    }
])->find($id);
```

**2. Pagination (if applicable):**
- Consider multi-page PDFs
- Page breaks for large BOMs

**3. Caching:**
```php
// Cache generated PDF for repeated downloads
$cacheKey = 'quotation_pdf_' . $id . '_' . $quotation->updated_at->timestamp;

return Cache::remember($cacheKey, 3600, function() use ($quotation, ...) {
    return PDF::loadView(...)->output();
});
```

---

## 📊 Summary

### PDF Generation Process:
1. Load quotation data (nested structure)
2. Render Blade template with data
3. Convert HTML to PDF (DomPDF)
4. Download to user

### Key Points:
- ✅ **Professional Output:** Branded, formatted
- ✅ **Complete Data:** All items, BOMs, pricing
- ✅ **Client-Ready:** Suitable for direct delivery
- ✅ **Customizable:** Template can be modified
- ✅ **Fast:** Generates in 2-5 seconds

### Technical:
- Uses DomPDF library
- Blade templating
- A4 portrait format
- Download or stream options

---

**End of Document 21 - PDF Generation Flow**

[← Back: Pricing Calculation](20_PRICING_CALCULATION_FLOW.md) | [Next: Data Import Flow →](22_DATA_IMPORT_FLOW.md)

