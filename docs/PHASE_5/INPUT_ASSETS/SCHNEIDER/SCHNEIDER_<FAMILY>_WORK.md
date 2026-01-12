# SCHNEIDER <FAMILY> — WORK FILE
## Catalog Conversion Execution Notes

**Family Code:** <FAMILY>  
**Family Name:** <Full Product Family Name>  
**OEM:** Schneider Electric  
**Status:** ⏳ Pending | ⚙ In Progress | ✅ Complete  
**Profile:** schneider_<family>_v1.yml  
**Owner:** <Name>  
**Started On:** <YYYY-MM-DD>  
**Completed On:** <YYYY-MM-DD>

---

## 1. Purpose of This File

This document captures **family-specific execution details** while converting the Schneider <FAMILY> catalog into NSW canonical CSV format.

It exists to:
- Record **data quirks and exceptions**
- Track **profile tuning decisions**
- Document **why rules were adjusted**
- Support **SOP derivation**

⚠️ This file is **not canonical**. Once the SOP stabilizes, this becomes reference-only.

---

## 2. Source Artifacts

### 2.1 Original Sources
- **PDF:**  
  `tools/catalog_pipeline/input/raw/schneider/<family>/<filename>.pdf`
- **WEF / Revision Date:** <Date from document>
- **Pages Covered:** <Page range>

### 2.2 XLSX Conversion
- **Converted XLSX:**  
  `tools/catalog_pipeline/input/raw/schneider/<family>/<filename>.xlsx`
- **Conversion Tool Used:** <Tool Name>
- **Manual Cleanup Performed:**  
  - [ ] Removed headers/footers  
  - [ ] Merged split tables  
  - [ ] Other: <notes>

---

## 3. Profile Configuration

### 3.1 Profile File
- `tools/catalog_pipeline/profiles/schneider/schneider_<family>_v1.yml`

### 3.2 Key Profile Decisions
- **Column Mapping:**  
  - SKU column index: <n>  
  - Price column index: <n>  
- **Series Detection:**  
  - Heading-based: <Yes/No>  
  - Prefix-based fallback: <Yes/No>
- **Scope Filter:**  
  - Applied: <Yes/No>  
  - Pattern(s): `<pattern>`

---

## 4. TEST Normalization Notes

### 4.1 TEST Runs
| Run | Date | Rows Output | Issues Found | Action Taken |
|----|------|-------------|--------------|--------------|
| T1 | <date> | <count> | <issue> | <fix> |
| T2 | <date> | <count> | — | — |

### 4.2 Common Issues Observed
- SKU format inconsistencies:
  - e.g. `<example>`
- Price formatting:
  - e.g. commas, ranges, "On Request"
- Header noise / section bleed:
  - e.g. `<example>`

---

## 5. FINAL Freeze

### 5.1 FINAL Source
- **FINAL XLSX:**  
  `tools/catalog_pipeline/input/final/schneider/<family>/Schneider_<Family>_FINAL_<YYYY-MM-DD>.xlsx`

### 5.2 FINAL Output
- **FINAL CSV:**  
  `tools/catalog_pipeline/output/final/schneider_<Family>_FINAL_<YYYY-MM-DD>_normalized_<timestamp>.csv`
- **Profile Version:** `v1`
- **Rows Output:** <count>

⚠️ FINAL artifacts are **immutable**.

---

## 6. Import Verification

### 6.1 Dry-Run
- Result: ✅ Pass / ❌ Fail
- Errors (if any): <summary>

### 6.2 Commit Import
- **Batch ID:** <uuid>
- **CatalogItem Created:** <item_code>
- **SKUs Imported:** <count>
- **Price Rows Inserted:** <count>

---

## 7. Exceptions & Decisions

Document any non-obvious decisions:
- Why certain rows were excluded
- Why SKU validation rules differ
- Any assumptions made

Example:
> "Accessories listed inline with main SKUs were excluded and will be handled as a separate family."

---

## 8. SOP Feedback (Important)

List **generalizable learnings** that should feed back into the SOP:

- [ ] New ignore rule discovered
- [ ] Better series detection pattern
- [ ] Column-shift heuristic needed
- [ ] Validation rule refinement

> These items must be reviewed when updating  
> `docs/SOP/CATALOG_PDF_TO_CSV_SOP.md`

---

## 9. Completion Declaration

When done, fill this:

> **Status:** ✅ Complete  
> **FINAL CSV Imported Successfully**  
> **No pending issues for <FAMILY>**

---

## 10. Next Family Pointer

Next family to process:
- `<NEXT_FAMILY_CODE>` — `<NEXT_FAMILY_NAME>`

---

**Document Lifecycle**
- Active during execution
- Read-only after completion
- Archived once Schneider track is complete

