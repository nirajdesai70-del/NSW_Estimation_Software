# Week-1 Closure Checklist

**Date:** 2026-01-12  
**Status:** ⏳ **3 MANDATORY + 2 OPTIONAL items remaining**

---

## ✅ COMPLETED (6/11 items)

1. ✅ **Scutwork Plan Created** - Structural completion
2. ✅ **Add Panel API Implemented** (P6-UI-005 backend)
   - Endpoint: `POST /api/v1/quotation/{quotation_id}/panels`
   - Schema: `AddPanelRequest`, `AddPanelResponse`
   - Tenant isolation + validation
3. ✅ **Customer Snapshot Enforcement Implemented** (P6-UI-001A/001B)
   - Copy flow: customer_name_snapshot always populated
   - Logic: customer_id → master name, else source snapshot/customer_name
   - Evidence note: Create is stubbed, enforced in copy only
4. ✅ **Tests Created**
   - `test_add_panel.py` - Add Panel tests
   - `test_customer_snapshot_rules.py` - Customer snapshot tests
5. ✅ **Week-1 Runner Exists** - `scripts/run_week1_checks.sh`
6. ✅ **Week-1 Evidence Pack Complete** - `evidence/PHASE6_WEEK1_EVIDENCE_PACK.md`

---

## ⏳ REMAINING - MANDATORY (3 items)

### 1. **Add Panel UI Implemented** (P6-UI-005 frontend) 🔴 **BLOCKER**
   - **Status:** ⏳ PENDING
   - **Required:** 
     - Add "Add Panel" button on quotation detail page
     - Modal form with name (required) and quantity (default=1)
     - On success: Refresh panel list (no page reload)
   - **File:** `frontend/src/pages/QuotationDetail.tsx` (or similar)
   - **Priority:** 🔴 **HIGH** (Compliance alarm - ALARM-CRUD)

### 2. **All Tests Passing** 🔴 **BLOCKER**
   - **Status:** ⏳ PENDING
   - **Required:**
     - Run `pytest tests/quotation/test_add_panel.py` - must pass
     - Run `pytest tests/quotation/test_customer_snapshot_rules.py` - must pass
     - Or run `./scripts/run_week1_checks.sh` - must pass all checks
   - **Priority:** 🔴 **HIGH** (Closure gate)

### 3. **Run Week-1 Runner and Verify** 🔴 **BLOCKER**
   - **Status:** ⏳ PENDING
   - **Required:**
     - Execute: `./scripts/run_week1_checks.sh`
     - Verify all checks pass (backend health, endpoint exists, tests pass)
     - Review evidence output in `evidence/PHASE6_WEEK1_RUN_<timestamp>/`
   - **Priority:** 🔴 **HIGH** (Closure gate)

---

## ⏳ REMAINING - OPTIONAL (2 items)

### 4. **Design Documents Created** (P6-UI-001, P6-UI-003) 🟠 **OPTIONAL**
   - **Status:** ⏳ PENDING
   - **Required:**
     - `docs/PHASE_6/UI/QUOTATION_OVERVIEW_DESIGN.md`
     - `docs/PHASE_6/UI/PANEL_DETAILS_DESIGN.md`
   - **Priority:** 🟠 **MEDIUM** (Documentation, not blocking closure if UI exists)

### 5. **UI Pages Verification** (P6-UI-002, P6-UI-004) 🟡 **VERIFY**
   - **Status:** ⏳ NEEDS VERIFICATION
   - **Required:**
     - Verify quotation overview page exists and works
     - Verify panel details page exists and works
   - **Priority:** 🟡 **LOW** (May already exist, needs verification)

---

## 📊 Summary

**Total Items:** 11  
**Completed:** 6 ✅  
**Remaining Mandatory:** 3 🔴  
**Remaining Optional:** 2 🟠

**Closure Status:** ⏳ **3 MANDATORY items remaining**

---

## 🎯 To Close Week-1

### Minimum Required (3 items):
1. ✅ Implement Add Panel frontend UI
2. ✅ Run tests and verify they pass
3. ✅ Run Week-1 runner and verify all checks pass

### Optional (2 items):
4. Create design documents (if not already done)
5. Verify existing UI pages (if not already verified)

---

## ⚠️ Compliance Alarms Status

### ALARM-CRUD (Week-1 portion)
- **Status:** ⏳ **PARTIALLY RESOLVED**
- **Backend:** ✅ Complete
- **Frontend:** ⏳ Pending (Add Panel UI)
- **Resolution:** Complete frontend UI to fully resolve

### ALARM-CUSTOMER-SNAPSHOT
- **Status:** ✅ **RESOLVED**
- **Backend:** ✅ Complete (Copy flow enforcement)
- **Evidence:** ✅ Note added (Create is stubbed, enforced in copy only)

---

## 📝 Next Actions

1. **Implement Add Panel Frontend UI** (Step-7)
   - Add button + modal on quotation detail page
   - Form validation
   - API integration
   - List refresh

2. **Run Tests**
   ```bash
   pytest tests/quotation/test_add_panel.py -v
   pytest tests/quotation/test_customer_snapshot_rules.py -v
   ```

3. **Run Week-1 Runner**
   ```bash
   ./scripts/run_week1_checks.sh
   ```

4. **Verify Closure**
   - All tests pass
   - Runner passes
   - Frontend UI works
   - Evidence pack updated

---

**Last Updated:** 2026-01-12  
**Closure ETA:** After completing 3 mandatory items
