# Master Module

## Overview

The Master module contains global masters and shared resources that affect all modules in the system. These include organization data, vendor/manufacturer information, PDF formats, templates, and system defaults.

## Key Concepts

- **Organization Master**: Company/organization definitions, addresses, GST information, letterhead data
- **Vendor/Manufacturer**: Represented as "Make" and "Brand" in Product Module (Component/Item Master)
- **PDF Formats**: PDF template/layout standards (not operational workflows)
- **Templates**: Reusable template definitions used across modules
- **Defaults**: System defaults, settings, global configuration used across modules

## Baseline Status

- **Status:** ✅ FROZEN
- **Freeze Date:** 2025-12-17 (IST)
- **Batches Included:** 10B
- **Total Files:** 6 (1 content + 5 stubs)

> **Note:** Master baseline is intentionally stub-heavy. Core masters (Organization, PDF) are referenced from other modules where operational workflows are documented. Master data integration docs are kept in Project/Quotation modules (their usage perspective).

> **Note:** "Total Files Frozen" counts module-curated artifacts only (feature docs, change docs, stubs). Git "Files Changed" includes scaffolding/README/index updates, folder structure, and other repository infrastructure files.

> **Note:** Master baseline is intentionally stub-heavy. Core masters (Organization, PDF) are referenced from other modules where operational workflows are documented.

## Primary References

### General
- `_general/MASTER_MODULE_OVERVIEW.md` - Module overview and scope boundaries

### Organization
- `organization/README.md` - References to Project/Quotation integration docs

### PDF Formats
- `pdf_formats/README.md` - References to Quotation PDF generation workflow

### Vendor
- `vendor/README.md` - References to Component/Item Master (Make/Brand)

### Templates
- `templates/README.md` - Placeholder for template documentation

### Defaults
- `defaults/README.md` - Placeholder for defaults documentation

## Cross-Module References

- `../quotation/reports/21_PDF_GENERATION_FLOW.md` - PDF generation workflow
- `../component_item_master/_general/08_PRODUCT_MODULE.md` - Make/Brand (vendor) concept
- `../project/_general/PROJECT_BACKEND_DESIGN_PART7_MASTER_DATA.md` - Organization integration (if exists)
- `../quotation/_general/QUOTATION_BACKEND_DESIGN_PART7_MASTER_DATA.md` - Organization integration (if exists)

## Sub-Modules (Areas)

1. `_general/` — **General Overview** (module overview, scope boundaries)
2. `organization/` — **Organization** (references to integration docs - see README)
3. `vendor/` — **Vendor** (references to Make/Brand in Component/Item Master - see README)
4. `pdf_formats/` — **PDF Formats** (references to Quotation PDF workflow - see README)
5. `templates/` — **Templates** (reusable templates - see README for references)
6. `defaults/` — **Defaults** (system defaults - see README for references)
7. `import_export/` — **Import/Export** (empty - to be added if needed)
8. `reports/` — **Reports** (empty - to be added if needed)

## Directory Structure

```
features/master/
├── README.md (this file)
├── _general/ (1 file - overview)
├── organization/ (README stub)
├── vendor/ (README stub)
├── pdf_formats/ (README stub)
├── templates/ (README stub)
├── defaults/ (README stub)
├── import_export/ (empty)
└── reports/ (empty)

changes/master/
├── migration/ (empty)
├── fixes/ (empty)
└── validation/ (empty)
```

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

## Next Steps

1. **Validation:** Review all placements and structure
2. **Next Module:** Proceed to next module bifurcation (Employee/Role, etc.)
3. **Future Enhancement:** Add dedicated master docs if found

