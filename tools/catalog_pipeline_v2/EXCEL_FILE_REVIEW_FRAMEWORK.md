# Excel File Review Framework - Item Master Analysis

**Date:** 2025-01-XX  
**Status:** AWAITING FILE ACCESS  
**Target File:** `tools/input/revised item master/item_master_020126.xlsx`

---

## Review Scope

This document will be used to review the Excel file and compare it with:
1. Current PATCH_REVIEW_REPORT_v1.2.md analysis
2. NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.md
3. NSW_SHEET_SET_INDEX_v1.md
4. migrate_sku_price_pack.py script

---

## Expected Excel File Structure

Based on user description, the file should contain:
- Multiple README sheets (documentation)
- Process sheets (workflow/instructions)
- Data sheets (actual item master data)

---

## Review Checklist

### 1. Sheet Inventory
- [ ] List all sheet names
- [ ] Categorize sheets (README, Process, Data)
- [ ] Identify sheet purposes

### 2. README Sheets Review
- [ ] Terminology used (SC_Lx vs SCL vs Capability)
- [ ] Definitions provided
- [ ] Alignment with freeze documents
- [ ] Conflicts with patch requirements

### 3. Process Sheets Review
- [ ] Workflow steps documented
- [ ] Data entry rules
- [ ] Validation rules
- [ ] Alignment with migration script logic

### 4. Data Sheets Review
- [ ] Column structure
- [ ] Column naming (business_subcategory vs business_segment)
- [ ] SC_Lx columns (how they're used)
- [ ] Capability columns (if any)
- [ ] Generic naming (vendor/series neutrality)
- [ ] Data completeness

### 5. Comparison with Patch Requirements
- [ ] SC_Lx usage (SCL vs Capability conflict)
- [ ] Generic naming violations
- [ ] Terminology alignment
- [ ] Missing validations
- [ ] Structural gaps

---

## Analysis Framework

Once file is accessible, I will:

1. **Extract Sheet Names and Structure**
   ```python
   import pandas as pd
   xls = pd.ExcelFile('path/to/file.xlsx')
   for sheet in xls.sheet_names:
       df = pd.read_excel(xls, sheet_name=sheet)
       # Analyze structure
   ```

2. **Compare Terminology**
   - Check for SC_Lx usage
   - Check for capability_class_x usage
   - Check for business_subcategory vs business_segment
   - Check for generic naming patterns

3. **Identify Conflicts**
   - SC_Lx treated as capability (WRONG per patch)
   - Generic names with vendor/series (WRONG per patch)
   - Missing validations
   - Structural misalignments

4. **Document Gaps**
   - Missing rules
   - Missing validations
   - Missing documentation
   - Inconsistencies

---

## Next Steps

**Waiting for:**
1. Confirmation of exact file path, OR
2. File upload/share, OR
3. Alternative file location

Once file is accessible, I will:
1. Read all sheets
2. Analyze structure and content
3. Compare with patch requirements
4. Create detailed comparison report
5. Update PATCH_REVIEW_REPORT with new findings

---

**Status:** ⏳ AWAITING FILE ACCESS

