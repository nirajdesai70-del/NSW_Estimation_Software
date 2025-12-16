> Source: source_snapshot/QUOTATION_V2_IMPLEMENTATION_PLAN.md
> Bifurcated into: features/quotation/v2/QUOTATION_V2_IMPLEMENTATION_PLAN.md
> Module: Quotation > V2
> Date: 2025-12-17 (IST)

# Quotation V2 Implementation Plan

**Date:** December 6, 2025  
**Status:** 🚀 STARTING  
**Goal:** Build new quotation format with proper hierarchy while reusing Phase 1 pricing work

---

## 🎯 Why We're Pivoting

### Current Problem
- Old Step page structure is too constrained
- Pricing UI controls only appear when BOM items exist
- Empty quotations show no controls at all
- Structure doesn't match business workflow (Panel → Feeder → BOM hierarchy)

### Solution
- Build new Quotation V2 with proper hierarchy
- Reuse all Phase 1 pricing work (RateSource, IsClientSupplied, etc.)
- Create clean, intuitive UI for the new structure
- Keep legacy quotations on old screens (read-only)

---

## 📐 Target Hierarchy

```
Customer
  → Project
      → Quotation
          → Item (Panel)          [quotation_sales]
              → Feeder            [quotation_sale_boms, Level=0]
                  → BOM Level 1   [quotation_sale_boms, Level=1, ParentBomId=Feeder]
                      → Components [quotation_sale_bom_items]
                      → BOM Level 2 [quotation_sale_boms, Level=2, ParentBomId=BOM_L1]
                          → Components [quotation_sale_bom_items]
```

### Table Mapping

| Hierarchy Level | Table | Key Fields |
|----------------|-------|------------|
| Item (Panel) | `quotation_sales` | QuotationSaleId, SaleCustomName, Qty, Rate, Amount |
| Feeder | `quotation_sale_boms` | Level=0, ParentBomId=NULL, FeederName, Qty, Rate, Amount |
| BOM Level 1 | `quotation_sale_boms` | Level=1, ParentBomId=Feeder, BomName, Qty, Rate, Amount |
| BOM Level 2 | `quotation_sale_boms` | Level=2, ParentBomId=BOM_L1, BomName, Qty, Rate, Amount |
| Components | `quotation_sale_bom_items` | ProductId, Qty, Rate, RateSource, IsClientSupplied, etc. |

---

## 🗄️ Database Schema (Already Prepared)

### Existing Fields (Phase 1)
- ✅ `quotation_sale_bom_items.RateSource` (ENUM: PRICELIST, MANUAL_WITH_DISCOUNT, FIXED_NO_DISCOUNT)
- ✅ `quotation_sale_bom_items.IsClientSupplied` (TINYINT)
- ✅ `quotation_sale_bom_items.IsPriceConfirmed` (TINYINT)

### Fields Needed (From Phase 1 Spec - May Need Migration)
- ⏳ `quotation_sale_boms.Level` (TINYINT, 0=Feeder, 1=BOM L1, 2=BOM L2)
- ⏳ `quotation_sale_boms.ParentBomId` (BIGINT, NULL for Feeders)
- ⏳ `quotation_sale_boms.FeederName` (VARCHAR, for Level=0)
- ⏳ `quotation_sale_boms.BomName` (VARCHAR, for Level>0)

**Note:** Check if these fields already exist from Phase 1 planning.

---

## 🎨 UI Structure for Quotation V2

### 1. Quotation Overview Page
**Route:** `/quotation/{id}/v2`  
**View:** `quotation/v2/index.blade.php`

**Shows:**
- Quotation header (Client, Project, Quotation No)
- List of all Panels (Items) for this quotation
- For each Panel:
  - Panel name, Qty, Rate, Amount
  - Count of Feeders
  - Count of total items
  - Pricing status (complete / X items unpriced)
- Actions: Add Panel, Edit Panel, View Details

### 2. Panel Details Page
**Route:** `/quotation/{id}/panel/{panelId}`  
**View:** `quotation/v2/panel.blade.php`

**Shows:**
- Panel header (Panel name, Qty, Rate, Amount)
- Feeder list (Level=0 BOMs)
- For each Feeder:
  - Feeder name, Qty, Rate, Amount
  - BOM Level 1 list (Level=1, ParentBomId=Feeder)
  - Actions: Add BOM L1, Edit Feeder
- Actions: Add Feeder, Save Panel

### 3. BOM Details View (Collapsible Tree)
**Shows:**
- Feeder (Level 0)
  - BOM Level 1 (Level 1)
    - Components list (with pricing controls)
    - BOM Level 2 (Level 2) [optional]
      - Components list (with pricing controls)
  - Components list (direct under Feeder) [if any]

### 4. Component Row (Reusing Phase 1 UI)
**Each component row shows:**
- Category, SubCategory, Item, Generic
- Make, Series, Description
- SKU, Qty, Rate
- **Pricing Mode** dropdown (Pricelist / Manual + Disc / Fixed)
- **Client Supplied** checkbox
- Discount, NetRate, Amount
- Warning badge if unpriced

---

## 🔧 Implementation Steps

### Step 1: Verify Database Schema
- [ ] Check if `Level`, `ParentBomId`, `FeederName`, `BomName` exist in `quotation_sale_boms`
- [ ] If not, create migration to add them
- [ ] Verify Phase 1 pricing fields exist in `quotation_sale_bom_items`

### Step 2: Create Models & Relationships
- [ ] Update `QuotationSaleBom` model:
  - Add `parentBom()` relationship
  - Add `childBoms()` relationship
  - Add scopes: `feeders()`, `bomLevel1()`, `bomLevel2()`
- [ ] Update `QuotationSale` model:
  - Add `feeders()` relationship (Level=0 BOMs)

### Step 3: Create Controllers
- [ ] `QuotationV2Controller@index()` - List all panels
- [ ] `QuotationV2Controller@panel()` - Show panel with feeders/BOMs
- [ ] `QuotationV2Controller@addPanel()` - Add new panel
- [ ] `QuotationV2Controller@addFeeder()` - Add feeder to panel
- [ ] `QuotationV2Controller@addBom()` - Add BOM L1 or L2
- [ ] `QuotationV2Controller@addItem()` - Add component to BOM
- [ ] `QuotationV2Controller@save()` - Save panel/BOM/item changes

### Step 4: Create Views
- [ ] `quotation/v2/index.blade.php` - Panel list
- [ ] `quotation/v2/panel.blade.php` - Panel details with tree
- [ ] `quotation/v2/_feeder.blade.php` - Feeder row (partial)
- [ ] `quotation/v2/_bom.blade.php` - BOM row (partial, recursive)
- [ ] `quotation/v2/_item.blade.php` - Component row (reuse Phase 1 UI)

### Step 5: Add Routes
- [ ] `GET /quotation/{id}/v2` - V2 index
- [ ] `GET /quotation/{id}/panel/{panelId}` - Panel details
- [ ] `POST /quotation/{id}/panel` - Add panel
- [ ] `POST /quotation/{id}/panel/{panelId}/feeder` - Add feeder
- [ ] `POST /quotation/{id}/bom/{bomId}/bom` - Add child BOM
- [ ] `POST /quotation/{id}/bom/{bomId}/item` - Add component
- [ ] `PUT /quotation/{id}/panel/{panelId}` - Update panel
- [ ] `PUT /quotation/{id}/bom/{bomId}` - Update BOM
- [ ] `PUT /quotation/{id}/item/{itemId}` - Update component

### Step 6: Integrate Phase 1 Pricing
- [ ] Reuse pricing mode selector from `item.blade.php`
- [ ] Reuse client supplied checkbox
- [ ] Reuse auto-pricing logic (`getItemRate()`)
- [ ] Reuse warning badges and status indicator
- [ ] Ensure `RateSource`, `IsClientSupplied` are saved correctly

### Step 7: Master BOM / Proposal BOM Integration
- [ ] Add "Import Master BOM" button on BOM row
- [ ] Add "Import Proposal BOM" button on BOM row
- [ ] Reuse existing `getMasterBomVal()` and `getProposalBomVal()` logic
- [ ] Ensure imported items get correct `RateSource` and auto-pricing

---

## 🎯 Phase 1 Pricing Integration

### What We're Reusing
- ✅ Database fields: `RateSource`, `IsClientSupplied`, `IsPriceConfirmed`
- ✅ Model logic: `QuotationSaleBomItem` with pricing fields
- ✅ Controller logic: Auto-pricing from pricelist
- ✅ UI components: Pricing Mode selector, Client Supplied checkbox
- ✅ JavaScript: `handleRateSourceChange()`, `handleClientSuppliedChange()`, `updatePricingStatus()`

### What We're Not Using (Yet)
- ⏳ Old Step page structure
- ⏳ Old panel/BOM rendering logic
- ⏳ Old form submission flow

---

## 📋 Deliverables

### Immediate (This Session)
1. ✅ Verify database schema
2. ✅ Create migration if needed
3. ✅ Update models with relationships
4. ✅ Create basic V2 controller structure
5. ✅ Create V2 index view (panel list)

### Next Session
1. Panel details page with tree view
2. Add Panel/Feeder/BOM functionality
3. Component rows with pricing controls
4. Master BOM / Proposal BOM import
5. Save/update functionality

### Future
1. Migrate existing quotations (optional)
2. Enhanced tree visualization
3. Bulk operations
4. Export/print functionality

---

## 🔄 Legacy Quotations

### Strategy
- Keep old Step page (`/quotation/{id}/step`) for existing quotations
- Mark old quotations with flag or date cutoff
- New quotations use V2 flow
- Old quotations can be viewed but editing limited

### Implementation
- Add `IsV2` flag to `quotations` table (optional)
- Or use date cutoff: Quotations created after X date use V2
- Or manual selection: User chooses V1 or V2 when creating

---

## 🧪 Testing Plan

### Unit Tests
- [ ] Model relationships work correctly
- [ ] Scopes return correct BOMs by level
- [ ] Pricing fields save correctly

### Integration Tests
- [ ] Create new quotation → V2 flow
- [ ] Add panel → Shows in list
- [ ] Add feeder → Shows under panel
- [ ] Add BOM L1 → Shows under feeder
- [ ] Add BOM L2 → Shows under BOM L1
- [ ] Add component → Pricing controls visible
- [ ] Change pricing mode → Behavior correct
- [ ] Mark client supplied → Rate = 0 allowed
- [ ] Import Master BOM → Items added with pricing
- [ ] Save → All data persisted correctly

---

## 📝 Notes

### Backward Compatibility
- All existing quotations continue to work on old screens
- No data migration required initially
- Can migrate quotations one by one later if needed

### Performance
- Use eager loading for relationships
- Implement pagination for large panels
- Cache pricing status calculations

### UX Considerations
- Tree view should be collapsible/expandable
- Clear visual hierarchy (indentation, colors)
- Drag-and-drop for reordering (future)
- Bulk edit capabilities (future)

---

*Plan created: December 6, 2025*  
*Next: Start with Step 1 - Verify Database Schema*

