# Planning Mode Policy

**Status:** 🟡 ACTIVE  
**Date:** 2025-12-24  
**Purpose:** Define rules and procedures for planning-only work

---

## 🎯 Planning Mode Definition

**Planning Mode** is a work state where:
- ✅ Test work can be **documented and prepared**
- ✅ Execution instructions can be **written**
- ✅ Verification contracts can be **defined**
- ❌ Tests **cannot be executed** (no DB access)
- ❌ Code **cannot be modified** for testing
- ❌ Live systems **cannot be accessed**

---

## 📋 Planning Mode Rules

### ✅ What IS Allowed

1. **Documentation:**
   - Write test cases
   - Define test scenarios
   - Document expected results
   - Create execution instructions
   - Write verification contracts

2. **Preparation:**
   - Identify test fixtures
   - Define test data requirements
   - Prepare result templates
   - Document prerequisites
   - Create transition plans

3. **Organization:**
   - Organize test work by phase
   - Create test registries
   - Document dependencies
   - Plan execution order

### ❌ What IS NOT Allowed

1. **Execution:**
   - ❌ Execute tests against any database
   - ❌ Run queries against production
   - ❌ Make API calls to live systems
   - ❌ Modify code for testing
   - ❌ Create test databases

2. **Infrastructure:**
   - ❌ Set up test environments
   - ❌ Configure DB connections
   - ❌ Install test tools
   - ❌ Access production systems

3. **Code Changes:**
   - ❌ Write test code
   - ❌ Modify application code
   - ❌ Create migrations
   - ❌ Update configurations

---

## 🟡 Planning Mode Indicators

All planning mode work must be clearly marked with:

1. **Status Badge:** `🟡 PLANNING MODE` or `⏳ PENDING EXECUTION`
2. **Mode Notice:** Clear statement that work is planning-only
3. **Execution Block:** Explanation of why execution is blocked
4. **Transition Reference:** Link to `TRANSITION_PLAN.md`

---

## 📁 Planning Mode Structure

All planning mode work must be organized in:

```
PLANNING/
├── README.md                    # Test work registry
├── PLANNING_MODE_POLICY.md     # This document
├── TRANSITION_PLAN.md           # How to move to execution
├── EXECUTION/                   # Execution instructions
├── VERIFICATION/                # Verification contracts
└── PRESERVED_WORK/              # Preserved test work
    ├── test_cases/              # Test case documentation
    ├── fixtures/                # Fixture definitions
    └── results/                 # Result templates/placeholders
```

---

## 🔄 Transition to Execution Mode

Planning mode work can transition to execution mode when:

1. **Phase 5 Begins:**
   - Phase 4 complete
   - Phase 5 approved
   - DB access available

2. **Infrastructure Ready:**
   - Test DB accessible
   - API endpoints available
   - Test environment isolated

3. **Prerequisites Met:**
   - All test work documented
   - Execution instructions complete
   - Verification contracts defined

**Transition Process:** Follow `TRANSITION_PLAN.md`

---

## 📝 Documenting Planning Mode Work

When creating planning mode documents:

1. **Header Section:**
   ```markdown
   **Status:** 🟡 PLANNING MODE - Ready for Phase 5 Execution
   **Mode:** Planning Only - No DB Access Available
   **⚠️ PLANNING MODE:** [Explanation]
   ```

2. **Execution Block Notice:**
   ```markdown
   **⚠️ PLANNING MODE:** This [test/plan] is documented and ready 
   but **cannot be executed** until Phase 5 begins with DB access. 
   See `../TRANSITION_PLAN.md` for execution procedures.
   ```

3. **Registry Entry:**
   - Add to `PLANNING/README.md` Test Work Registry
   - Mark status as "Ready" (not "Executed")
   - Include location and prerequisites

---

## ✅ Planning Mode Checklist

Before marking work as "Planning Mode Complete":

- [ ] Test work fully documented
- [ ] Execution instructions complete
- [ ] Verification contracts defined
- [ ] Test fixtures identified
- [ ] Expected results documented
- [ ] Prerequisites listed
- [ ] Result templates created
- [ ] Registered in Test Work Registry
- [ ] Status clearly marked as Planning Mode
- [ ] Transition plan referenced

---

## 🚨 Important Notes

1. **No Execution:** Planning mode means NO execution, even if you think you can test something
2. **Preserve Work:** All test work must be preserved for Phase 5
3. **Clear Status:** Always mark work as planning mode
4. **Transition Ready:** Work should be ready to execute when Phase 5 begins
5. **No Assumptions:** Don't assume DB access will be available

---

## 🔗 Related Documents

- **Planning Mode README:** `PLANNING/README.md`
- **Transition Plan:** `PLANNING/TRANSITION_PLAN.md`
- **Phase 5 README:** `docs/PHASE_5/README.md`
- **Phase 5 Scope Fence:** `docs/PHASE_5/PHASE_5_SCOPE_FENCE.md`

---

**Last Updated:** 2025-12-24  
**Policy Status:** ACTIVE

