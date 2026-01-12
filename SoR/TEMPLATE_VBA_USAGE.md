# Template: VBA Macro Usage for Future Categories

**For:** MPCB, MCCB, ACB, and all future categories  
**File:** `TEMPLATE_APPLY_SOR_GOVERNANCE_PATTERN.bas`

---

## Why Pattern-Based?

The pattern-based macro automatically detects DATA sheets using naming patterns, so you don't need to edit code for each new category.

---

## Pattern Detection Rules

### DATA Sheets (Auto-detected)

**Pattern 1:** `item_*_work`
- Examples:
  - `item_mpcb_gv2_work`
  - `item_mccb_nsx_work`
  - `item_acb_masterpact_work`
  - `item_contactor_tesys_eocr_work`

**Pattern 2:** Standard sheets (always DATA)
- `nsw_item_master_engineering_view`
- `accessory_master`

### README Sheets (Auto-detected)
- Any sheet starting with `readme`
- Any sheet containing `control` or `governance`

### ARCHIVE Sheets (Auto-detected)
- Any sheet containing `archive`, `old`, or `legacy`

---

## How to Use (Same as CONTACTOR)

### Step 1: Open Your New Dataset

Example: `SoR_MPCB_DATASET_v1.0_CLEAN.xlsx`

---

### Step 2: Open VBA Editor

Press: **⌥ + F11**

---

### Step 3: Insert Module

**Insert → Module**

---

### Step 4: Paste Pattern-Based Macro

1. Open: `SoR/TEMPLATE_APPLY_SOR_GOVERNANCE_PATTERN.bas`
2. Copy all code
3. Paste into module

---

### Step 5: Set Password (Optional)

```vba
Private Const PWD As String = ""   ' or "YourPassword"
```

---

### Step 6: Run Macro

Press **F5** or **Run → Run Sub/UserForm**

Select: `APPLY_SOR_GOVERNANCE`

---

### Step 7: Save as .xlsm

**File → Save As → Excel Macro-Enabled Workbook (.xlsm)**

---

## What Gets Protected

**Automatically detected as DATA (Blue tabs):**
- All `item_*_work` sheets
- `nsw_item_master_engineering_view`
- `accessory_master`

**Automatically detected as README (Green tabs):**
- `README_DATASET_CONTROL`
- Any `README_*` sheet

**Automatically detected as ARCHIVE (Red tabs):**
- Any `*_archive_*` sheet
- Any sheet with `old` or `legacy` in name

**Everything else (Gray tabs):**
- Locked but not DATA

---

## Customization (If Needed)

If you have non-standard sheet names, edit the `IsDataSheet()` function:

```vba
Private Function IsDataSheet(ByVal wsName As String) As Boolean
    Dim n As String
    n = LCase(Trim(wsName))
    
    ' Add custom patterns here
    IsDataSheet = ( _
        (Left(n, 5) = "item_" And Right(n, 5) = "_work") Or _
        n = "nsw_item_master_engineering_view" Or _
        n = "accessory_master" Or _
        n = "your_custom_sheet_name" _  ' Add custom names here
    )
End Function
```

---

## Advantages of Pattern-Based

✅ **No code editing** per category  
✅ **Automatic detection** of DATA sheets  
✅ **Consistent protection** across all categories  
✅ **Future-proof** for new series  

---

## Example: MPCB Workflow

1. Create: `SoR_MPCB_DATASET_v1.0_CLEAN.xlsx`
2. Add sheets:
   - `item_mpcb_gv2_work`
   - `item_mpcb_gv3_work`
   - `nsw_item_master_engineering_view`
   - `accessory_master`
   - `README_DATASET_CONTROL`
3. Paste pattern-based macro
4. Run `APPLY_SOR_GOVERNANCE`
5. Done! All sheets automatically protected and colored.

---

**Pattern-based macro = zero maintenance for new categories.**



