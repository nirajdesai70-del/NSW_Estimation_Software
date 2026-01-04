# Manual Excel Steps — Quick Reference

**After running `EXECUTE_CLEANUP.sh`, complete these steps.**

**⚠️ RECOMMENDED: Use VBA Macro (5 minutes) instead of manual steps (15 minutes)**

See: `SoR/CONTACTOR/v1.4/HOW_TO_USE_VBA_MACRO.md` for automated approach.

---

## Manual Approach (15 minutes)

**If you prefer manual steps:**

---

## Step 1: Add README_DATASET_CONTROL Sheet

### File to Open
```
SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx
```

### Actions
1. **Open the Excel file**
2. **Insert new sheet** (right-click on first sheet → Insert → Worksheet)
3. **Rename sheet** to: `README_DATASET_CONTROL`
4. **Move sheet** to position 1 (first sheet)
5. **Copy content** from: `SoR/CONTACTOR/v1.4/README_DATASET_CONTROL.md`
6. **Format as table** (optional but recommended)
7. **Save**

### Content Source
The markdown file contains all the content you need. Copy these sections:
- Dataset Identity table
- What This File IS / IS NOT
- Authoritative Data Sheets list
- Non-Data / Governance Sheets
- Usage Rules
- Golden Rule

---

## Step 2: Apply Excel Protection & Colors

### DATA Sheets (7 sheets — make BLUE)

**Sheets to protect:**
1. `item_tesys_eocr_work`
2. `item_tesys_protect_work`
3. `item_giga_series_work`
4. `item_k_series_work`
5. `item_capacitor_duty_work`
6. `nsw_item_master_engineering_view`
7. `accessory_master`

**For each DATA sheet:**
1. Right-click sheet tab → **Tab Color** → **Blue**
2. Select all cells (Ctrl+A / Cmd+A)
3. **Format Cells** → **Protection** tab → Check **Locked**
4. **Review** tab → **Protect Sheet**
   - ✅ Allow: Select locked cells, Select unlocked cells, Filter, Sort
   - ❌ Uncheck everything else
   - (Optional: Set password)

---

### README Sheet (make GREEN)

**Sheet:** `README_DATASET_CONTROL`

**Actions:**
1. Right-click sheet tab → **Tab Color** → **Green**
2. **Review** tab → **Protect Sheet**
   - Lock entire sheet
   - (Optional: Set password)

---

### ARCHIVE Sheets (make RED)

**Sheets matching pattern:** `*_archive_*`

**Example:** `accessory_master_archive_old`

**For each archive sheet:**
1. Right-click sheet tab → **Tab Color** → **Red**
2. **Review** tab → **Protect Sheet**
   - Lock entire sheet
   - (Optional: Set password)

---

### Workbook Protection (Optional)

1. **Review** tab → **Protect Workbook**
   - ✅ Protect structure (prevents sheet deletion/renaming)
   - (Optional: Set password)

---

## Quick Checklist

- [ ] README_DATASET_CONTROL sheet added (first sheet)
- [ ] Content copied from markdown file
- [ ] 7 DATA sheets: Blue tabs + protected
- [ ] README sheet: Green tab + protected
- [ ] Archive sheets: Red tabs + protected
- [ ] Workbook structure protected (optional)
- [ ] File saved

---

## Time Estimate

- Step 1 (Add README sheet): ~5 minutes
- Step 2 (Protection & colors): ~10 minutes
- **Total: ~15 minutes**

---

## ⚡ Faster Alternative: VBA Macro

**Use VBA macro instead:**
- Setup: ~5 minutes (one-time)
- Run macro: ~2 seconds
- **Total: ~5 minutes**

**See:** `SoR/CONTACTOR/v1.4/HOW_TO_USE_VBA_MACRO.md`

---

**After completing these steps, your SoR file is fully locked and protected.**

