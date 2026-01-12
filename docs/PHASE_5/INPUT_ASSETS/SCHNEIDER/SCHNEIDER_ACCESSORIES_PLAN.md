# SCHNEIDER ACCESSORIES PLAN
## Deferred Extraction Strategy

**Status:** 📋 DEFERRED (Planned for Post-Main-Series)  
**Purpose:** Track accessory extraction strategy to ensure systematic coverage after main product families are complete.  
**Created:** 2025-12-26  
**Target Execution:** After LC1E, LP1K, LC1D, LC1K, GV are complete

---

## 1. Why Accessories Are Deferred

### 1.1 Cross-Family Nature
Accessories (aux contacts, coils, mounting kits) serve **multiple main families**:
- LC1E (Easy TeSys)
- LC1D (TeSys Deca)
- LC1K (TeSys K AC control)
- LP1K (TeSys K DC control)
- GV (MPCB)

Including them now would create:
- Duplicate SKU entries
- Confusion about which family they belong to
- Profile complexity that breaks the "one family = one profile" rule

### 1.2 Messy SKU Patterns
Accessory SKU prefixes are inconsistent:
- **Auxiliary Contacts:** LAD, LA, LB, LC, LD, LE, LF...
- **Coils:** Voltage-dependent variants (24V, 110V, 220V, etc.)
- **Mounting Kits:** Various prefixes
- **Terminal Covers:** Separate product codes

These appear:
- Inline with main SKU tables
- In separate accessory sections
- In footnotes
- In cross-reference tables

This increases false positives and slows extraction.

### 1.3 Phase-5 Logic Dependency
Accessories become meaningful only when we decide:

- **Are they optional add-ons?** → `SKUType: ADDON`
- **Are they mandatory splits for certain configurations?** → `SKUType: MANDATORY_SPLIT`
- **Are they built-in?** → `SKUType: BUILT_IN`

This decision is **Phase-5-level business logic**, not catalog-only extraction.

---

## 2. Common Accessory Prefixes Observed

### 2.1 Auxiliary Contacts
- **LAD** — Auxiliary contact blocks
- **LA** — Auxiliary contact (NO)
- **LB** — Auxiliary contact (NC)
- **LC** — Auxiliary contact (NO+NC)
- **LD** — Additional variants
- **LE** — Additional variants
- **LF** — Additional variants

### 2.2 Coils
- Voltage-dependent variants:
  - 24V DC (BD)
  - 110V AC (FD)
  - 220V AC (MD)
  - Other voltages (B7, F7, M7, N7, etc.)

### 2.3 Mounting & Installation
- Mounting kits
- Terminal covers
- DIN rail accessories
- Enclosure accessories

### 2.4 Other Accessories
- Surge suppressors
- Time delay modules
- Interlock kits

---

## 3. Proposed SKUType Mapping Rules (Future)

These rules will be finalized during Phase-5 execution:

| Accessory Type | Proposed SKUType | Rationale |
|---------------|------------------|-----------|
| Auxiliary contacts (LAD/LA/LB/LC) | `ADDON` | Optional add-on for additional I/O |
| Coils (voltage variants) | `MANDATORY_SPLIT` | Required selection (one voltage per contactor) |
| Mounting kits | `ADDON` | Optional installation accessory |
| Terminal covers | `ADDON` | Optional safety/installation accessory |
| Surge suppressors | `ADDON` | Optional protection accessory |
| Time delay modules | `ADDON` | Optional functionality extension |

**Note:** Final mapping will be validated against Phase-5 estimation requirements.

---

## 4. Which Main Families They Attach To

### 4.1 Auxiliary Contacts
- ✅ LC1E (Easy TeSys)
- ✅ LC1D (TeSys Deca)
- ✅ LC1K (TeSys K AC)
- ✅ LP1K (TeSys K DC)
- ✅ GV (MPCB — some variants)

### 4.2 Coils
- ✅ LC1E (voltage selection)
- ✅ LC1D (voltage selection)
- ✅ LC1K (voltage selection)
- ✅ LP1K (voltage selection — already handled in main SKU)

### 4.3 Mounting Kits
- ✅ LC1E
- ✅ LC1D
- ✅ LC1K
- ✅ LP1K
- ✅ GV

---

## 5. Extraction Strategy (When Executed)

### 5.1 Create Separate Accessory Families

**Option A: By Accessory Type**
- `SCHNEIDER_LAD_AUX_CONTACTS`
- `SCHNEIDER_COILS`
- `SCHNEIDER_MOUNTING_KITS`
- `SCHNEIDER_TERMINAL_COVERS`

**Option B: By Main Family Mapping**
- `SCHNEIDER_LC1E_ACCESSORIES`
- `SCHNEIDER_LC1D_ACCESSORIES`
- `SCHNEIDER_LC1K_ACCESSORIES`
- `SCHNEIDER_LP1K_ACCESSORIES`
- `SCHNEIDER_GV_ACCESSORIES`

**Recommendation:** Option A (by type) to avoid duplication, with explicit mapping to applicable main families.

### 5.2 Profile Design Considerations

- **Scope filters:** Must exclude main family SKUs
- **SKU validation:** Must validate against known accessory prefixes
- **Price extraction:** May require different column mapping (accessories often in separate tables)
- **Cross-reference:** Must link to applicable main families

### 5.3 Source File Sections

Accessories typically appear in:
- Separate "Accessories" sections in price lists
- Inline tables with main SKUs (must be filtered out)
- Cross-reference appendices
- Technical specification sheets

---

## 6. Execution Checklist (Future)

When main families are complete:

- [ ] Review all source files for accessory sections
- [ ] Identify all accessory SKU prefixes
- [ ] Create accessory family profiles
- [ ] Extract accessory SKUs (separate from main families)
- [ ] Map accessories to applicable main families
- [ ] Define SKUType rules (ADDON vs MANDATORY_SPLIT)
- [ ] Import accessory families
- [ ] Update Phase-5 logic to handle accessory selection

---

## 7. Relationship to Main Series

This plan ensures:

✅ **No rework** of main family profiles (LC1E, LP1K, etc.)  
✅ **No pollution** of main family imports  
✅ **Controlled path** so accessories are not forgotten  
✅ **Clean separation** between main products and accessories  
✅ **Phase-5 alignment** for SKUType mapping

---

## 8. Exit Criteria

Accessories extraction is ready when:

- All main product families (LC1E, LP1D, LC1K, LP1K, GV) are ✅ Complete
- Phase-5 SKUType rules are defined
- Accessory-to-main-family mapping rules are clear
- Source file sections containing accessories are identified

---

**Document Control**
- Status: 📋 Planned (Deferred)
- Execution: After main series completion
- Owner: Catalog Pipeline Track
- Related: `SCHNEIDER_CATALOG_MASTER.md`

