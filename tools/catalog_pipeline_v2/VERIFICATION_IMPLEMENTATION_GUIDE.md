# Verification System Implementation Guide

**Version:** 1.0  
**Status:** 🔒 READY FOR IMPLEMENTATION  
**Effective From:** 2026-01-03

---

## ✅ System Status

**All verification documents are ready:**
- ✅ `STANDING_VERIFICATION_INSTRUCTION.md` (v2.1) - Master instruction
- ✅ `VERIFICATION_CHECKLIST_QUICK_REFERENCE.md` (v2.1) - Quick checklist
- ✅ `TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md` (v1.0) - Track A worksheet
- ✅ Integrated into `IMPORTER_BUILD_TICKET.md` (v1.1)

---

## 🚀 How to Implement

### For the Current Build: Generic Catalog Importer

#### Step 1: Start Track A Verification (15-20 min)

1. **Check RETAIN Register first:**
   ```
   tools/catalog_pipeline_v2/TRACK_A_RETAIN_REGISTER.md
   ```
   - Review existing RETAIN decisions that may apply
   - Reference applicable items in your worksheet

2. **Open the worksheet:**
   ```
   tools/catalog_pipeline_v2/TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md
   ```

3. **Fill in build information:**
   - Build: Generic Catalog Importer
   - Legacy Reference: `project/nish/` [catalog import area]

4. **Identify legacy business decisions:**
   - Check `project/nish/` for catalog import functionality
   - Look for: price list usage, WEF date handling, error handling, idempotency expectations
   - Focus on **business decisions**, NOT schema/code structure
   - **If decision already in RETAIN register, reference it rather than rediscover**

4. **Tag each decision:**
   - 🔴 **RETAIN** - Must exist (blocking if missing)
   - 🟡 **REPLACE** - Handled differently (non-blocking)
   - ⚪ **DROP** - Intentionally removed (non-blocking)

5. **Validate RETAIN items:**
   - For each RETAIN item, verify it exists in the new importer
   - Document evidence (API endpoint, logic, workflow)
   - If new RETAIN item discovered, add to `TRACK_A_RETAIN_REGISTER.md`

#### Step 2: Start Track B Verification (30 min)

1. **Review Master Fundamentals:**
   ```
   NSW Fundamental Alignment Plan/01_FUNDAMENTALS/MASTER_FUNDAMENTALS_v2.0.md
   ```

2. **Check Canonical Rules:**
   ```
   NSW Fundamental Alignment Plan/02_GOVERNANCE/NEPL_CANONICAL_RULES.md
   ```
   - Verify L0/L1/L2 definitions are followed

3. **Review Design Documents:**
   - Check for catalog/import related designs in:
   ```
   NSW Fundamental Alignment Plan/05_DESIGN_DOCUMENTS/
   ```

4. **Check Gap Registers:**
   ```
   NSW Fundamental Alignment Plan/02_GOVERNANCE/BOM_GAP_REGISTER.md
   ```
   - Verify related gaps are addressed

5. **Run Verification Queries:**
   ```
   NSW Fundamental Alignment Plan/07_VERIFICATION/FUNDAMENTALS_VERIFICATION_QUERIES.md
   ```

6. **Complete Checklist:**
   ```
   NSW Fundamental Alignment Plan/07_VERIFICATION/FUNDAMENTALS_VERIFICATION_CHECKLIST.md
   ```

#### Step 3: Combined Verification & Sign-off (10 min)

1. **Review both tracks:**
   - Track A: All RETAIN items satisfied?
   - Track B: All fundamentals compliant?
   - Any conflicts? (Track B wins)

2. **Create verification report:**
   - Use template from `VERIFICATION_CHECKLIST_QUICK_REFERENCE.md`
   - Document findings from both tracks

3. **Get sign-off:**
   - Update `IMPORTER_BUILD_TICKET.md` with verification status
   - Mark build as verified once both tracks pass

---

## 📋 Quick Start Workflow

```
1. Open: TRACK_A_LEGACY_BUSINESS_DECISION_WORKSHEET.md
   ↓
2. Fill in build info
   ↓
3. Review project/nish/ for business decisions
   ↓
4. Tag: RETAIN / REPLACE / DROP
   ↓
5. Validate RETAIN items (verify they exist in new build)
   ↓
6. Complete Track B (NSW Fundamentals verification)
   ↓
7. Combined review & sign-off
   ↓
8. Update build ticket
```

---

## ⚠️ Important Rules

### Track A Rules
- ✅ **RETAIN** items must exist → blocks if missing
- ✅ **REPLACE/DROP** items → document only, non-blocking
- ❌ **No legacy migration** - don't check schema/data migration
- ❌ **No schema parity** - don't compare table structures
- ❌ **Business decisions only** - ignore code/UI patterns

### Track B Rules
- ✅ **Always mandatory** - must pass to complete build
- ✅ **Blocking** - failures block completion
- ✅ **Authoritative** - if conflict with Track A, Track B wins

---

## 📝 Example: Importer Build

### Track A Example

**RETAIN Items:**
1. ✅ Idempotent import (can run multiple times) - SATISFIED
   - Evidence: Import batch tracking, lookup by tenant_id + make + oem_catalog_no

2. ✅ Price effective dating (WEF date) - SATISFIED
   - Evidence: `wef_date` → `effective_from` in sku_prices

**REPLACE Items:**
1. 🟡 Legacy Excel format → New normalized structure
   - New approach: Generic importer handles all product types uniformly
   - Rationale: Improved architecture, no product-specific branching

**DROP Items:**
1. ⚪ Legacy product-specific import scripts
   - Rationale: Replaced with generic importer per Schema Canon

### Track B Example

**Fundamentals Compliance:**
- ✅ Master Fundamentals v2.0: Compliant
- ✅ Canonical Rules (L0/L1/L2): Compliant
- ✅ Governance Standards: Compliant

**Design Alignment:**
- ✅ Matches importer design specifications

**Gap Register:**
- ✅ All related gaps addressed

---

## 🔧 Integration Points

### In Build Tickets

Add verification section:
```markdown
## 🔍 Verification Status

**Track A:** ⬜ PENDING / ✅ PASS / ❌ FAIL
**Track B:** ⬜ PENDING / ✅ PASS / ❌ FAIL
**Status:** ⬜ PENDING / ✅ VERIFIED / ❌ BLOCKED

**Verification Report:** [Link to report]
```

### In Code Reviews

- Reference verification report
- Confirm RETAIN items satisfied
- Confirm Track B compliance

### In Deployment

- Block deployment if verification not complete
- Both tracks must pass before deployment

---

## 📊 Tracking

### Verification Status Dashboard

| Build | Track A | Track B | Status | Report |
|-------|---------|---------|--------|--------|
| Generic Catalog Importer | ⬜ | ⬜ | ⬜ | [Link] |
| [Next Build] | ⬜ | ⬜ | ⬜ | [Link] |

---

## ❓ Frequently Asked Questions

**Q: Can I skip Track A if no legacy reference exists?**  
A: Yes, if no relevant legacy functionality exists, Track A is N/A. Mark as N/A and auto-PASS. Document this in the worksheet summary.

**Q: What if I can't find any legacy business decisions for my build?**  
A: That's fine. Mark Track A as N/A and auto-PASS. Focus on Track B which is always mandatory.

**Q: How detailed should the "Evidence" be in RETAIN items?**  
A: Keep it concise - API endpoint, config flag, workflow step, rule document, or test case reference. Don't write paragraphs.

**Q: What if Track A and Track B conflict?**  
A: Track B always wins. Document the conflict and resolution.

**Q: How detailed should Track A be?**  
A: Focus on business decisions only. Don't dive into code/schema details.

**Q: Can REPLACE items become RETAIN later?**  
A: Yes, if business requirements change. Update the worksheet and re-verify.

**Q: What if I can't complete verification in time?**  
A: Verification blocks build completion. Plan verification time into sprint.

---

## 🎯 Success Criteria

Implementation is successful when:
- ✅ All new builds include verification
- ✅ Track A worksheet completed for each build
- ✅ Track B verification completed for each build
- ✅ Verification reports created and reviewed
- ✅ Build tickets updated with verification status
- ✅ No builds deployed without verification

---

**Ready to implement?** Start with the current Generic Catalog Importer build using the workflow above!

