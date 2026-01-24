# D0 Gate Checklist (Definition Only)

**Version:** v1.0  
**Status:** ✅ CHECKLIST DEFINED (Week-0)  
**Date:** 2026-01-12  
**Phase:** Phase-6 Week-0

> **Critical Note:**  
> This is the checklist definition only. Signoff file (`D0_GATE_SIGNOFF.md`) is separate and not part of Week-0 unless the frozen plan explicitly requires signoff in Week-0.  
> **This checklist being defined ≠ Gate passed.**

---

## 1. Gate Intent

The D0 Gate proves readiness baseline for Track D (Costing & Reporting) execution.

**Purpose:**
- Ensure QCD v1.0 is stable before building costing UI/reporting
- Ensure QCA v1.0 is stable (if cost adders are included)
- Verify engine-first approach is established
- Confirm no schema meaning changes have occurred

**Blocks:** Track D (Costing & Reporting) cannot proceed until D0 Gate passed.

---

## 2. Checklist Items (Minimum Set)

### 2.1 Environment & Evidence

- [ ] Environment sanity evidence exists
  - **Evidence:** `evidence/PHASE6_WEEK0_RUN_20260112_140401/`
  - **Verification:** Week-0 runner script executed successfully

- [ ] Schema canon drift check passes (or drift status recorded)
  - **Evidence:** `scripts/check_schema_drift.sh` output
  - **Verification:** No unauthorized schema changes detected

- [ ] Week-0 evidence pack exists
  - **Evidence:** `PHASE6_WEEK0_EVIDENCE_PACK.md`
  - **Verification:** Document exists and is accessible

---

### 2.2 Governance Documents

- [ ] Task register exists
  - **Evidence:** `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`
  - **Verification:** Register is active and maintained

- [ ] QCD contract exists and frozen
  - **Evidence:** `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
  - **Verification:** Contract is versioned v1.0 and marked FROZEN

- [ ] Naming compliance doc exists
  - **Evidence:** `docs/PHASE_6/ENTRIES/P6_ENTRY_006_NAMING_COMPLIANCE.md`
  - **Verification:** Compliance verified and PASSED

- [ ] D0 Gate checklist exists (this document)
  - **Evidence:** `docs/PHASE_6/COSTING/D0_GATE_CHECKLIST.md`
  - **Verification:** Checklist is defined and accessible

---

### 2.3 Future Evaluation Criteria (Not Executed in Week-0)

> **Note:** These items are evaluated at D0 Gate signoff (per plan), not Week-0.

- [ ] QCD generator functional (BOM-only, stable contract)
  - **Verification:** QCD JSON endpoint returns valid data

- [ ] QCA generator functional (cost adders summary, if applicable)
  - **Verification:** QCA JSON endpoint returns valid data

- [ ] Cost sheet calculation engine working (if cost adders included)
  - **Verification:** Cost sheet calculations are correct

- [ ] Roll-up generator working (if cost adders included)
  - **Verification:** Cost adder roll-ups are correct

- [ ] Numeric validation passing
  - **Verification:** Engine output matches reference Excel (engine-first)

- [ ] Performance acceptable for large quotations
  - **Verification:** QCD generation < 5 seconds for typical quotation

---

## 3. How to Mark PASS

### 3.1 Week-0 Checklist Definition (This Document)

**Status:** ✅ DEFINED

This checklist is defined and ready for use at Week-6 D0 Gate signoff.

---

### 3.2 Week-6 D0 Gate Signoff (Separate Document)

**File:** `docs/PHASE_6/COSTING/D0_GATE_SIGNOFF.md`

**Requirements:**
- All checklist items must be marked PASS
- Evidence links must be provided for each item
- Signoff must include:
  - Date
  - Signer (role/name)
  - Status: PASS/FAIL
  - Evidence references

**Who Can Mark:**
- Phase-6 Technical Lead
- Phase-6 Governance Lead
- Or as defined in Phase-6 Decision Register

**Evidence Requirements:**
- Links to all evidence files mandatory
- No checklist item may be marked PASS without evidence

---

## 4. Must Not Proceed If Missing

The following items **must exist** before D0 Gate can be evaluated:

1. ✅ Environment sanity evidence
2. ✅ Schema canon drift check results
3. ✅ Week-0 evidence pack
4. ✅ Task register
5. ✅ QCD contract v1.0 (frozen)
6. ✅ Naming compliance document
7. ✅ D0 Gate checklist (this document)

If any of the above are missing, D0 Gate evaluation cannot proceed.

---

## 5. References

- **Week-0 Evidence Pack:** `PHASE6_WEEK0_EVIDENCE_PACK.md`
- **Week-0 Evidence Folder:** `evidence/PHASE6_WEEK0_RUN_20260112_140401/`
- **Task Register:** `docs/PHASE_6/REGISTERS/PHASE6_TASK_REGISTER.md`
- **QCD Contract:** `docs/PHASE_6/COSTING/QCD_CONTRACT_v1.0.md`
- **Schema Canon:** `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`

---

## 6. Checklist Acceptance

**P6-SETUP-006:** ✅ COMPLETE

This checklist is defined and ready for Week-6 D0 Gate evaluation.

---

**End of Document**
