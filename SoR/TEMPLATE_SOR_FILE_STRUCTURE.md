# Template: SoR File Structure for Future Categories

**This template ensures MPCB / MCCB / ACB never repeat today's confusion.**

---

## Required File Name Pattern

```
SoR_<CATEGORY>_DATASET_v<version>_CLEAN.xlsx
```

**Examples:**
- `SoR_MPCB_DATASET_v1.0_CLEAN.xlsx`
- `SoR_MCCB_DATASET_v1.0_CLEAN.xlsx`
- `SoR_ACB_DATASET_v1.0_CLEAN.xlsx`

---

## Required Sheets (IN THIS ORDER)

### 1️⃣ README_DATASET_CONTROL (MANDATORY - FIRST SHEET)

**Purpose:** Lock file that declares intent, scope, and data sheets.

**Content:** See `SoR/CONTACTOR/v1.4/README_DATASET_CONTROL.md` for template.

**Must Include:**
- Dataset identity (role, scope, version, state)
- What this file IS and IS NOT
- Authoritative data sheets list
- Non-data sheets list
- Usage rules
- Golden rule
- Change log

---

### 2️⃣ README_SCOPE_AND_LIMITS (OPTIONAL BUT RECOMMENDED)

**Purpose:** Explicit declaration of category coverage and exclusions.

**Content:**
- Category covered
- Explicit exclusions
- Version intent
- Allowed usage
- Not allowed usage

---

### 3️⃣ DATA SHEETS (ONLY THESE HOLD DATA)

**Naming Rule:**
```
item_<category>_<series>_work
```

**Examples:**
- `item_mpcb_gv2_work`
- `item_mccb_nsx_work`
- `item_acb_masterpact_work`
- `item_contactor_tesys_eocr_work`

**Rule:** Only sheets matching this pattern contain real data.

---

### 4️⃣ nsw_item_master_engineering_view (MANDATORY)

**Purpose:** Consolidated read-only view of all items.

**Rules:**
- Read-only
- No manual edits
- Derived from data sheets
- Used for engineering review

---

### 5️⃣ accessory_master (MANDATORY)

**Purpose:** Accessories only.

**Rules:**
- No base items
- Accessories only
- Must be clearly separated from base items

---

### 6️⃣ ARCHIVE SHEETS (OPTIONAL)

**Naming Pattern:**
```
*_archive_old
```

**Rules:**
- Must be clearly suffixed with `_archive_old`
- Never referenced in logic
- Historical only
- Must be listed in README_DATASET_CONTROL as excluded

---

## Template Rule (MANDATORY)

> **If a sheet does not appear in the README_DATASET_CONTROL as a DATA sheet, it is not data.**

---

## Excel Protection Policy

### DATA SHEETS (LOCKED)

| Sheet Type | Protection |
|------------|------------|
| `item_*_work` | 🔒 Locked |
| `nsw_item_master_engineering_view` | 🔒 Locked |
| `accessory_master` | 🔒 Locked |

**Allowed:** Filter, sort  
**Disallowed:** Edit, insert, delete

### README / CONTROL SHEETS
- 🔒 Locked
- No edits except Admin

### ARCHIVE SHEETS
- 🔒 Locked
- Greyed visually

---

## Visual Color Coding

| Sheet Type | Tab Color | Meaning |
|------------|-----------|---------|
| DATA | 🟦 Blue | Authoritative |
| README / CONTROL | 🟩 Green | Explanation |
| ARCHIVE | 🟥 Red | Do Not Use |
| WORK (SoW only) | 🟨 Yellow | Temporary |

---

## Header Row Coloring (DATA SHEETS)

| Column Type | Color |
|-------------|-------|
| Identity fields | Light Blue |
| Attributes | Light Grey |
| Ratings | Light Orange |
| Metadata | Light Green |

---

## Password Policy (OPTIONAL BUT RECOMMENDED)

- Same password for all SoR files
- Known only to Admin + Director
- Engineers get read-only access

---

## Checklist for New Category

When creating a new SoR file (e.g., MPCB):

- [ ] File named `SoR_<CATEGORY>_DATASET_v1.0_CLEAN.xlsx`
- [ ] README_DATASET_CONTROL sheet added (first sheet)
- [ ] All data sheets listed in README_DATASET_CONTROL
- [ ] All non-data sheets listed as excluded
- [ ] Data sheets follow naming pattern `item_<category>_<series>_work`
- [ ] `nsw_item_master_engineering_view` sheet included
- [ ] `accessory_master` sheet included
- [ ] Archive sheets (if any) suffixed with `_archive_old`
- [ ] Data sheets locked and protected
- [ ] Tab colors applied (Blue = Data, Green = README, Red = Archive)
- [ ] File placed in `SoR/<CATEGORY>/v<version>/`
- [ ] README_DATASET_CONTROL explicitly declares category scope
- [ ] README_DATASET_CONTROL explicitly excludes other categories

---

## Golden Rule

> **Each category gets its own SoR file. Never reuse or duplicate.**

---

**This template prevents future confusion and ensures consistency across all categories.**



