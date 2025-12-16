> Source: source_snapshot/docs/03_MODULES/13_REPORTS_EXPORTS.md
> Bifurcated into: features/component_item_master/import_export/13_REPORTS_EXPORTS.md
> Module: Component / Item Master > Import/Export
> Date: 2025-12-17 (IST)

# Reports & Exports Module

**Document:** 13_REPORTS_EXPORTS.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## Overview

**Export Capabilities:**
- PDF quotation generation
- Excel quotation export
- Product data export
- Price list export

---

## PDF Generation

**Route:** GET /quotation/pdf/{id}  
**Controller:** QuotationController@quotationPdf  
**Library:** DomPDF  
**Format:** A4 Portrait

**Features:**
- Company header with logo
- Client details
- Project information
- Complete item breakdown
- Pricing summary
- Terms & conditions
- Signature block

**Process:**
1. Load quotation with all data
2. Render Blade template
3. Convert HTML → PDF
4. Download file

**See Document 21_PDF_GENERATION_FLOW.md for details**

---

## Excel Export

**Route:** GET /quotation/excel/{id}  
**Controller:** QuotationController@quotationExcelExport  
**Library:** Maatwebsite/Excel  
**Format:** XLSX

**Export Class:** app/Exports/QuotationExport.php

**Exports:**
- Quotation header
- All sale items
- All BOMs
- All items with details
- Pricing breakdown

---

## Excel Import

**Routes:**
- GET /import/product - Show import form
- POST /import/product - Process import

**Import Classes:**
- ProductImport.php
- PriceImport.php

**Process:**
1. Upload Excel file
2. Validate data
3. Create/update records
4. Return summary (success/errors)

**See Document 22_DATA_IMPORT_FLOW.md for details**

---

## Summary

**PDF:** Professional quotations for clients  
**Excel Export:** Data analysis  
**Excel Import:** Bulk operations  
**Formats:** XLSX, CSV, PDF

---

**End of Document 13 - Reports & Exports**

[← Back](12_USER_MANAGEMENT.md) | [Next: All Pages Reference →](14_ALL_PAGES_REFERENCE.md)

