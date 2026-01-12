# VBA Macro Quick Start

**Fastest way to apply SoR governance: ~5 minutes**

---

## 🎯 What It Does

Automatically:
- ✅ Colors sheet tabs (Blue=DATA, Green=README, Red=ARCHIVE)
- ✅ Protects all sheets (DATA allows filter/sort)
- ✅ Locks workbook structure (prevents sheet changes)
- ✅ Enforces SoR discipline

---

## 📁 Files Created

### For CONTACTOR (Current)
- **Macro:** `SoR/CONTACTOR/v1.4/APPLY_SOR_GOVERNANCE.bas`
- **Guide:** `SoR/CONTACTOR/v1.4/HOW_TO_USE_VBA_MACRO.md`

### For Future Categories (MPCB, MCCB, ACB)
- **Macro:** `SoR/TEMPLATE_APPLY_SOR_GOVERNANCE_PATTERN.bas`
- **Guide:** `SoR/TEMPLATE_VBA_USAGE.md`

---

## ⚡ Quick Steps (5 minutes)

### 1. Open Excel File
```
SoR/CONTACTOR/v1.4/SoR_CONTACTOR_DATASET_v1.4_CLEAN.xlsx
```

### 2. Enable Developer
**Excel → Preferences → Ribbon & Toolbar → Check Developer**

### 3. Open VBA Editor
Press: **⌥ + F11** (Option + F11)

### 4. Insert Module
**Insert → Module**

### 5. Paste Macro
- Open: `SoR/CONTACTOR/v1.4/APPLY_SOR_GOVERNANCE.bas`
- Copy all code
- Paste into module

### 6. Set Password (Optional)
Change this line if you want a password:
```vba
Private Const PWD As String = ""   ' or "YourPassword"
```

### 7. Run Macro
Press **F5** or **Run → Run Sub/UserForm**

Select: `APPLY_SOR_GOVERNANCE`

### 8. Save as .xlsm
**File → Save As → Excel Macro-Enabled Workbook (.xlsm)**

---

## ✅ What You Get

**Tab Colors:**
- 🟦 Blue: 7 DATA sheets
- 🟩 Green: README sheets
- 🟥 Red: Archive sheets
- ⬜ Gray: Other sheets

**Protection:**
- DATA sheets: Locked but filter/sort allowed
- Other sheets: Fully locked
- Workbook: Structure protected

---

## 🔄 For Future Categories

Use the **pattern-based macro** instead:
- File: `SoR/TEMPLATE_APPLY_SOR_GOVERNANCE_PATTERN.bas`
- Automatically detects `item_*_work` sheets
- No code editing needed

---

## ⏱️ Time Comparison

| Method | Time |
|--------|------|
| **VBA Macro** | ~5 minutes |
| Manual | ~15 minutes |

**Macro is 3x faster!**

---

## 📚 Full Documentation

- **Detailed guide:** `SoR/CONTACTOR/v1.4/HOW_TO_USE_VBA_MACRO.md`
- **Template guide:** `SoR/TEMPLATE_VBA_USAGE.md`
- **Manual alternative:** `MANUAL_EXCEL_STEPS.md`

---

**Ready to use. Run it once and you're done!**



