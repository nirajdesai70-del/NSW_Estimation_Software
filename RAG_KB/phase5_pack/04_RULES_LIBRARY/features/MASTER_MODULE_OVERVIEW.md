---
Source: features/master/_general/MASTER_MODULE_OVERVIEW.md
KB_Namespace: features
Status: WORKING
Last_Updated: 2025-12-17T02:18:25.994254
KB_Path: phase5_pack/04_RULES_LIBRARY/features/MASTER_MODULE_OVERVIEW.md
---

# Master Module Overview

> Source: Created for Batch 10B  
> Bifurcated into: features/master/_general/MASTER_MODULE_OVERVIEW.md  
> Module: Master > General  
> Date: 2025-12-17 (IST)

---

## Overview

The Master module contains global masters and shared resources that affect all modules in the system. These include organization data, vendor/manufacturer information, PDF formats, templates, and system defaults.

---

## Key Concepts

- **Organization Master**: Company/organization data, addresses, GST information, letterhead data
- **Vendor/Manufacturer**: Represented as "Make" and "Brand" in Product Module (Component/Item Master)
- **PDF Formats**: PDF generation, layouts, print templates, headers/footers
- **Templates**: Reusable templates used by quotation/project/PDF
- **Defaults**: System defaults, settings, global configuration used across modules

---

## Module Structure

```
Master Module
├── Organization (company/org master)
├── Vendor (make/brand - covered in Component/Item Master)
├── PDF Formats (PDF generation, layouts, templates)
├── Templates (reusable templates)
└── Defaults (system defaults, global config)
```

---

## Integration Points

- **Organization** → Used by Project, Client, Quotation modules
- **Vendor/Make** → Used by Product Module (Component/Item Master)
- **PDF Formats** → Used by Quotation module for PDF generation
- **Templates** → Used across Quotation, Project, PDF modules
- **Defaults** → Used system-wide

---

## Primary References

- `organization/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md` - Organization master data integration
- `organization/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md` - Quotation master data integration
- `pdf_formats/21_PDF_GENERATION_FLOW.md` - PDF generation flow
- `../../component_item_master/_general/08_PRODUCT_MODULE.md` - Make/Brand (vendor) concept

---

## Scope Boundary

### What Master Module Includes:
- **Organization Master**: Company/organization definitions (if dedicated docs exist)
- **PDF Formats**: PDF template/layout standards (not operational workflows)
- **Templates**: Reusable template definitions
- **Defaults**: System-wide default values and configuration

### What Master Module Excludes:
- **Vendor/Manufacturer**: Covered as "Make" and "Brand" in Component/Item Master
- **PDF Generation Workflow**: Covered in Quotation module (operational flow)
- **Master Data Integration**: Covered in Project/Quotation modules (integration perspective)

## Reference Links

### Organization Master Data Integration:
- `../organization/README.md` - References to Project/Quotation integration docs
- `../../project/_general/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md` - Project perspective
- `../../quotation/_general/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md` - Quotation perspective

### PDF Generation:
- `../../quotation/reports/21_PDF_GENERATION_FLOW.md` - PDF generation workflow

### Vendor/Manufacturer:
- `../../component_item_master/_general/08_PRODUCT_MODULE.md` - Make/Brand concept

## Notes

- Vendor concept is implemented as "Make" and "Brand" in the Product Module
- PDF generation workflow is documented in Quotation module (operational flow)
- PDF formats/templates would be documented here if they exist as standards
- Organization master data integration is documented from Project/Quotation perspective

