# Track A — Legacy Business Decision Worksheet

**Version:** 1.0  
**Status:** 🔒 ACTIVE  
**Effective From:** 2026-01-03  
**Usage:** Mandatory artifact per build/module

---

## Build Information

**Build / Module:** __________________________  
**Date:** __________________________  
**Reviewed By:** __________________________  
**Legacy Reference Area:** `project/nish/` ____________________

**Default Rule:** If no explicit legacy business decision is identified for this build, Track A is N/A and auto-PASS.

**Reference:** Check `TRACK_A_RETAIN_REGISTER.md` first for existing RETAIN decisions that may apply to this build.

---

## 🔴 RETAIN — Blocking Items

Business decisions that **must exist** in the new system.

| # | Legacy Business Decision | Decision Source | Evidence in New System | Owner | Status |
|---|-------------------------|----------------|----------------------|-------|--------|
| 1 | | (email/meeting/SOP/screen/contract) | | | ⬜ SATISFIED / ⬜ MISSING |
| 2 | | (email/meeting/SOP/screen/contract) | | | ⬜ SATISFIED / ⬜ MISSING |
| 3 | | (email/meeting/SOP/screen/contract) | | | ⬜ SATISFIED / ⬜ MISSING |
| 4 | | (email/meeting/SOP/screen/contract) | | | ⬜ SATISFIED / ⬜ MISSING |
| 5 | | (email/meeting/SOP/screen/contract) | | | ⬜ SATISFIED / ⬜ MISSING |

**Rule:** If any row is marked **MISSING** → **BUILD BLOCKED**

**Evidence Examples:** API endpoint, config flag, workflow step, rule document, test case reference.

---

## 🟡 REPLACE — Non-Blocking Items

Business intent covered, but implemented differently or improved.

| # | Legacy Business Decision | New Approach | Notes |
|---|-------------------------|--------------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

---

## ⚪ DROP — Non-Blocking Items

Legacy behavior intentionally removed.

| # | Legacy Business Decision | Rationale for Drop |
|---|-------------------------|-------------------|
| 1 | | |
| 2 | | |
| 3 | | |

---

## Track A Summary

- **Total RETAIN items:** _____
- **RETAIN satisfied:** ⬜ YES ⬜ NO
- **Total REPLACE items:** _____
- **Total DROP items:** _____
- **Track A Status:** ⬜ PASS ⬜ FAIL (BLOCK) ⬜ N/A (no legacy decisions identified)

---

## Sign-off

**Reviewed By:** __________________________  
**Date:** __________________________  
**Track A Approval:** ⬜ APPROVED ⬜ NOT APPROVED

---

## Authority Note

This worksheet validates **business intent only**.  
It does not validate schema, migration, or technical parity.  
Final authority remains with Track B (NSW Fundamentals).

---

## Execution Guidelines

**Time-box:** Track A should complete in **15-20 minutes maximum**.
- ✅ Quick business decision identification
- ✅ Tag RETAIN/REPLACE/DROP
- ✅ Validate RETAIN items only
- ❌ No deep dives into legacy code
- ❌ No reverse engineering
- ❌ No schema/code structure analysis

**Artifact:** Keep lightweight - one worksheet per build/module, not per file or table.

---

## Quick Reference: Business Decision Categories

When reviewing `project/nish/`, only check these:

### 1. Quotation Flow Decisions
- How quotation numbers are generated
- Panel/feeder/BOM expectations (conceptual)

### 2. Pricing Decisions
- WEF date usage
- Price source priority
- Discount logic expectations (not exact formula parity)

### 3. Locking Decisions
- When locking applies
- Who can unlock

### 4. Audit Expectations
- Which user actions must be logged

**Anything outside this is REPLACE by default.**

