---
Source: features/proposal_bom/workflows/V2_MASTER_PROPOSAL_BOM_FINAL_PLAN.md
KB_Namespace: features
Status: CANONICAL
Last_Updated: 2025-12-17T01:55:38.405738
KB_Path: phase5_pack/04_RULES_LIBRARY/features/V2_MASTER_PROPOSAL_BOM_FINAL_PLAN.md
---

> Source: source_snapshot/V2_MASTER_PROPOSAL_BOM_FINAL_PLAN.md
> Bifurcated into: features/proposal_bom/workflows/V2_MASTER_PROPOSAL_BOM_FINAL_PLAN.md
> Module: Proposal BOM > Workflows
> Date: 2025-12-17 (IST)

# Master BOM vs Proposal BOM - Final Implementation Plan

## 📋 REVISION HISTORY

| Version | Date | Author | Changes | Notes |
|---------|------|--------|---------|-------|
| 1.0 | 2025-12-11 | Auto | Final consolidated plan | Includes Proposal BOM sidebar and auto-naming |

---

## 🎯 EXECUTIVE SUMMARY

**Proposal Analysis:** ✅ **VERY USEFUL - 90% aligned with existing code**

**Recommendation:** ✅ **PROCEED with implementation**

**Key Additions:**
1. ✅ Re-establish Proposal BOM sidebar (missing menu item)
2. ✅ Implement auto-naming standard (Panel/Feeder/BOM)
3. ✅ Add modification tracking
4. ✅ Create orchestration function
5. ✅ Add promotion feature
6. ✅ Complete bulk operations

---

## 📊 CURRENT STATE vs PROPOSAL

| Concept | Current State | Alignment | Action |
|---------|---------------|-----------|--------|
| Master BOM = Library | ✅ Exists | ✅ 100% | Document |
| Proposal BOM = Instance | ✅ Exists | ✅ 100% | Document |
| Always Copy Rule | ✅ Already does | ✅ 100% | Document |
| Service-only computation | ✅ Enforced | ✅ 100% | Document |
| Soft delete (Status=1) | ✅ Consistent | ✅ 100% | Document |
| Proposal BOM Sidebar | ❌ Missing | ⚠️ Gap | **Add** |
| Auto-naming | ⚠️ Partial | ⚠️ Partial | **Standardize** |
| Modification tracking | ❌ Missing | ⚠️ Gap | **Add** |
| Orchestration function | ❌ Missing | ⚠️ Gap | **Add** |
| Promotion feature | ❌ Missing | ⚠️ Gap | **Add** |
| Bulk operations | ⚠️ Partial | ⚠️ Partial | **Complete** |

**Overall:** 90% aligned - Most concepts already implemented, need to add missing pieces.

---

## 📋 COMPLETE IMPLEMENTATION PLAN

### Phase 0: Proposal BOM Sidebar & Auto-Naming (6-9 hours) ⭐ START HERE

**Priority:** HIGH - User explicitly requested

**Tasks:**

1. **Create Proposal BOM Sidebar:**
   - Create `ProposalBomController` with `index()` and `show()` methods
   - Create listing page (`proposal-bom/index.blade.php`)
   - Create detail page (`proposal-bom/show.blade.php`)
   - Add sidebar link after "Feeder Library"
   - Add routes

2. **Implement Auto-Naming Service:**
   - Create `AutoNamingService` with methods:
     - `generatePanelName($quotationId, $providedName)`
     - `generateFeederName($panelId, $providedName)`
     - `generateBomName($parentBomId, $level, $providedName)`
   - Update `addPanel()`, `addFeeder()`, `addBom()` to use service
   - Make name fields nullable in request validation
   - Document as standard instruction

3. **Ensure Links Everywhere:**
   - Verify Proposal BOM button in V2 panel works
   - Verify Proposal BOM button in legacy step page works
   - Add links in Proposal BOM listing page
   - Add cross-references where appropriate

**Files:**
- `app/Http/Controllers/ProposalBomController.php` (NEW)
- `app/Services/AutoNamingService.php` (NEW)
- `resources/views/proposal-bom/index.blade.php` (NEW)
- `resources/views/proposal-bom/show.blade.php` (NEW)
- `resources/views/layouts/sidebar.blade.php` (add link)
- `app/Http/Controllers/QuotationV2Controller.php` (use AutoNamingService)
- `app/Http/Requests/AddPanelRequest.php` (make nullable)
- `app/Http/Requests/AddFeederRequest.php` (make nullable)
- `app/Http/Requests/AddBomRequest.php` (make nullable)
- `routes/web.php` (add routes)
- `V2_AUTO_NAMING_STANDARD.md` (NEW)

**Risk:** ⭐⭐ Low-Medium - New features, backward compatible

---

### Phase 1: Terminology & Documentation (1-2 hours)

**Priority:** MEDIUM - Improves clarity

**Tasks:**
1. Create terminology glossary
2. Add code comments
3. Update UI labels
4. Document "Always Copy" rule

**Files:**
- `V2_TERMINOLOGY.md` (NEW)
- Code comments
- UI labels

**Risk:** ⭐ Low - Documentation only

---

### Phase 2: Modification Tracking (2-3 hours)

**Priority:** MEDIUM - Enables other features

**Tasks:**
1. Create migration for `IsModified`, `ModifiedBy`, `ModifiedAt`, `OriginMasterBomId`
2. Update `QuotationSaleBom` model
3. Update BOM creation/edit logic
4. Set modification flags

**Files:**
- Migration file (NEW)
- `app/Models/QuotationSaleBom.php`
- `app/Http/Controllers/QuotationV2Controller.php`

**Risk:** ⭐⭐ Medium - Database changes, but backward compatible

---

### Phase 3: Orchestration Function (3-4 hours)

**Priority:** MEDIUM - Improves consistency

**Tasks:**
1. Create `BomChangeOrchestrator` service
2. Refactor existing operations to use orchestrator
3. Ensure all changes go through orchestrator

**Files:**
- `app/Services/BomChangeOrchestrator.php` (NEW)
- `app/Http/Controllers/QuotationV2Controller.php` (refactor)
- `app/Http/Controllers/QuotationController.php` (refactor)

**Risk:** ⭐⭐ Medium - Refactoring, but improves consistency

---

### Phase 4: Promotion Feature (2-3 hours)

**Priority:** MEDIUM - High user value

**Tasks:**
1. Add "Promote to Master BOM" button
2. Create `promoteToMasterBom()` method
3. Add route and modal

**Files:**
- `app/Http/Controllers/QuotationV2Controller.php`
- `resources/views/quotation/v2/_bom.blade.php`
- `routes/web.php`

**Risk:** ⭐⭐ Low-Medium - New feature

---

### Phase 5: Complete Bulk Operations (4-5 hours)

**Priority:** MEDIUM - Completing existing work

**Tasks:**
1. Create multi-edit modal UI
2. Implement bulk operations
3. Use orchestration function

**Files:**
- `resources/views/quotation/v2/_multi_edit_modal.blade.php` (NEW)
- `app/Http/Controllers/QuotationV2Controller.php` (enhance)

**Risk:** ⭐⭐ Medium - Completing structure

---

### Phase 6: Audit Trail (1-2 hours)

**Priority:** LOW - Good for compliance

**Tasks:**
1. Add audit logging in orchestration function
2. Optional: Create audit table

**Files:**
- `app/Services/BomChangeOrchestrator.php`
- Optional: Migration

**Risk:** ⭐ Low - Additive

---

## 🔧 STANDARD RULES - GLOBAL IMPLEMENTATION

### Rule 1: Auto-Naming Standard ⭐ NEW

**For Panel:**
- If `SaleCustomName` provided → Use it
- If empty/null → Auto-generate "Panel 1", "Panel 2", ...
- Count existing panels in quotation

**For Feeder:**
- If `FeederName` provided → Use it
- If empty/null → Auto-generate "Feeder 1", "Feeder 2", ...
- Count existing feeders in panel

**For BOM:**
- If `BomName` provided → Use it
- If empty/null → Auto-generate:
  - BOM1: "BOM 1", "BOM 2", ...
  - BOM2: "BOM2-1", "BOM2-2", ...
- Count existing BOMs at same level under same parent

**Implementation:**
- Use `AutoNamingService` for all name generation
- Apply in all creation methods
- Document as standard instruction

---

### Rule 2: Proposal BOM Sidebar ⭐ NEW

**Menu Item:**
- Add "Proposal BOM" in sidebar (after "Feeder Library")
- Icon: `la la-file-text`
- Route: `/proposal-bom`

**Listing Page:**
- Show all Proposal BOMs from `quotation_sale_boms`
- Filter by: Quotation, Project, Customer, Date
- Columns: BOM Name, Quotation, Project, Customer, Components, Actions
- Actions: View, Reuse, Promote

**Links:**
- Ensure Proposal BOM links work in:
  - V2 Panel (BOM header) ✅ Already exists
  - Legacy Step Page ✅ Already exists
  - Proposal BOM listing page (NEW)
  - Master BOM page (cross-reference)

---

### Rule 3: Terminology Standard

**Everywhere:**
- "Master BOM" = Reusable library template
- "Proposal BOM" = Quotation-specific instance
- Use consistently

---

### Rule 4: Always Copy Rule

**When selecting Master BOM:**
- NEVER link directly
- ALWAYS create new Proposal BOM by copying
- Set `OriginMasterBomId` to track origin

---

### Rule 5: Service-Only Computation

**Quantities:** Only `QuotationQuantityService`
**Costs:** Only `CostingService`
**UI/Controllers:** Never calculate

---

### Rule 6: Soft Delete Standard

**Use `Status = 1` for soft delete:**
- All queries must filter `WHERE Status = 0`

---

### Rule 7: Recalculation Cascade

**After ANY change:**
1. Recalculate quantities
2. Recalculate costs
3. Roll-up to parent levels
4. Update quotation totals

---

### Rule 8: Orchestration Function

**All BOM changes must go through:**
```php
BomChangeOrchestrator::applyProposalBomChange($quotationId, $bomId, $changeSet)
```

---

## 📝 RECOMMENDED IMPLEMENTATION ORDER

### Week 1: Foundation & User Requests
1. **Phase 0: Proposal BOM Sidebar & Auto-Naming** (6-9 hours) ⭐ START HERE
   - User explicitly requested
   - High value
   - Low-medium risk

### Week 2: Core Standards
2. **Phase 1: Terminology** (1-2 hours)
   - Immediate clarity
   - Zero risk

3. **Phase 2: Modification Tracking** (2-3 hours)
   - Enables other features
   - Backward compatible

### Week 3: Advanced Features
4. **Phase 3: Orchestration Function** (3-4 hours)
   - Improves consistency
   - Foundation for other features

5. **Phase 4: Promotion Feature** (2-3 hours)
   - High user value
   - Independent feature

### Week 4: Enhancements
6. **Phase 5: Complete Bulk Operations** (4-5 hours)
   - Completing existing work
   - High efficiency gain

7. **Phase 6: Audit Trail** (1-2 hours)
   - Good for compliance
   - Low risk

**Total Estimated Time:** 19-28 hours over 4 weeks

---

## ✅ BENEFITS SUMMARY

1. **Proposal BOM Visibility:** Engineers can see all Proposal BOMs in sidebar
2. **Auto-Naming:** Consistent naming when engineers don't provide names
3. **Clear Terminology:** Easier to understand and maintain
4. **Modification Tracking:** Know which BOMs were customized
5. **Orchestration:** Prevents bugs, ensures consistency
6. **Promotion:** Reuse successful BOMs as templates
7. **Bulk Operations:** Efficient multi-component editing
8. **Audit Trail:** Compliance and debugging
9. **Standard Rules:** Consistent behavior across system

---

## 🎯 FINAL RECOMMENDATION

**✅ PROCEED with implementation in phases:**

1. **Start with Phase 0** (Proposal BOM Sidebar & Auto-Naming) - User explicitly requested
2. **Then Phase 1** (Terminology) - Immediate clarity
3. **Then Phase 2** (Modification Tracking) - Enables other features
4. **Then Phases 3-6** as needed

**This approach:**
- ✅ Addresses user's immediate needs first
- ✅ Minimizes risk
- ✅ Provides incremental value
- ✅ Maintains backward compatibility
- ✅ Aligns with existing architecture (90% match)

**Ready to proceed?** Start with Phase 0 (Proposal BOM Sidebar & Auto-Naming) - it's what you explicitly requested!


