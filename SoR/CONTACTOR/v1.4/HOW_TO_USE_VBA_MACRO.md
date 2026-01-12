# How to Use VBA Macro for SoR Governance

**File:** `APPLY_SOR_GOVERNANCE.bas`  
**Purpose:** Automatically apply tab colors, sheet protection, and workbook structure protection

---

## Quick Start (Mac Excel)

### Step 1: Enable Developer Tools

1. Open Excel
2. **Excel → Preferences → Ribbon & Toolbar**
3. Check **Developer** checkbox
4. Click **OK**

---

### Step 2: Open Your Dataset

Open: `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx`

**Note:** Excel will ask to save as `.xlsm` to keep macros. Click **Yes**.

---

### Step 3: Open VBA Editor

Press: **⌥ + F11** (Option + F11)

Or: **Tools → Macro → Visual Basic Editor**

---

### Step 4: Insert Module

1. In VBA Editor: **Insert → Module**
2. A new module window opens

---

### Step 5: Paste Macro Code

1. Open: `APPLY_SOR_GOVERNANCE.bas`
2. Copy all code (Cmd+A, Cmd+C)
3. Paste into the module window (Cmd+V)

---

### Step 6: Set Password (Optional)

At the top of the code, find:

```vba
Private Const PWD As String = ""
```

**Option A: No password (simplest)**
- Leave as: `""`

**Option B: Set password**
- Change to: `"YourPasswordHere"`
- Example: `"Niraj@SoR2026"`

---

### Step 7: Run the Macro

**Method 1: From VBA Editor**
1. Click anywhere in the `APPLY_SOR_GOVERNANCE` function
2. Press **F5** or **Run → Run Sub/UserForm**

**Method 2: From Excel**
1. **Tools → Macro → Macros...**
2. Select: `APPLY_SOR_GOVERNANCE`
3. Click **Run**

---

### Step 8: Save as .xlsm

1. **File → Save As**
2. Format: **Excel Macro-Enabled Workbook (.xlsm)**
3. Name: `SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsm`
4. Click **Save**

---

## What Happens After Running

### Tab Colors Applied

- 🟦 **Blue:** 7 DATA sheets
  - `item_tesys_eocr_work`
  - `item_tesys_protect_work`
  - `item_giga_series_work`
  - `item_k_series_work`
  - `item_capacitor_duty_work`
  - `nsw_item_master_engineering_view`
  - `accessory_master`

- 🟩 **Green:** README/CONTROL sheets
  - `README_DATASET_CONTROL`
  - Any sheet with "readme", "control", or "governance" in name

- 🟥 **Red:** Archive sheets
  - `accessory_master_archive_old`
  - Any sheet with "archive", "old", or "legacy" in name

- ⬜ **Gray:** All other sheets

---

### Protection Applied

**DATA Sheets:**
- ✅ Locked (cannot edit)
- ✅ Filter allowed
- ✅ Sort allowed
- ✅ Pivot tables allowed

**README/ARCHIVE/OTHER Sheets:**
- ✅ Fully locked (no edits)

**Workbook Structure:**
- ✅ Cannot add/delete/rename/move sheets
- ✅ Structure protected

---

## Removing Protection (Admin Only)

If you need to edit the file later:

1. Open VBA Editor (⌥ + F11)
2. Run: `REMOVE_SOR_GOVERNANCE`
3. Make your edits
4. Run: `APPLY_SOR_GOVERNANCE` again

---

## Troubleshooting

### "Macros are disabled"

1. **Excel → Preferences → Security**
2. Set **Macro Security** to **Medium** or **Low** (for trusted files)
3. Reopen the file

### "Cannot run macro"

- Make sure Developer tools are enabled
- Make sure file is saved as `.xlsm`
- Check that code was pasted correctly

### "Sheet names don't match"

- Check exact spelling of your 7 DATA sheets
- If names differ, edit the `IsDataSheet()` function in the macro

---

## For Future Categories (MPCB, MCCB, ACB)

Use the **pattern-based macro** instead:
- File: `SoR/TEMPLATE_APPLY_SOR_GOVERNANCE_PATTERN.bas`
- Automatically detects `item_*_work` sheets
- No need to edit code per category

---

## Time Estimate

- First time setup: ~5 minutes
- Running macro: ~2 seconds
- **Total: ~5 minutes** (vs 15 minutes manual)

---

**Macro is ready. Run it once and you're done!**



