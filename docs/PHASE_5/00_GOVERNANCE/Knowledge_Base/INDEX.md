# Knowledge Base Index
## All Engineering Decision Documents

**Last Updated:** 2025-01-XX

---

## Active Documents (Under Review or Pending)

### 1. Schneider Final Rules v1.2 ⭐ **PRIMARY REFERENCE**

**File:** `SCHNEIDER_FINAL_RULES_v1.2.md`  
**Status:** LOCKED  
**Created:** 2025-01-XX  
**Last Updated:** 2025-01-XX (v1.2 - SC_L alignment + duty clarification corrected)  
**Purpose:** Single-page reference of final, locked rules for Schneider catalog interpretation

**v1.2 Changes:**
- ✅ Duty classification corrected: SC_L3 (Feature Class), not attribute
- ✅ Duty-specific ratings clarified as KVU attributes
- ✅ L2 multiplication triggers corrected (SKU-based only, not price-based)
- ✅ All contradictions resolved

**Key Content:**
- 16 locked rules extracted and compiled
- Implementation-ready reference
- No ambiguity, no theory - just rules

**Usage:** Primary reference document for all Schneider catalog work.

---

### 2. Schneider L2/L1 Differentiation Clarification v1.0

**File:** `SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md`  
**Status:** LOCKED  
**Created:** 2025-01-XX  
**Purpose:** Final clarification on L2 vs L1 differentiation, resolving confusion around AC1/AC3, duty, and ratings

**Key Decisions:**
- L2 is NOT multiplied for AC1/AC3/ratings
- Differentiation happens ONLY at L1
- Multiple L1 lines can reference same L2 SKU
- Golden sentence: "Different engineering interpretations of the same OEM product are represented as multiple L1 lines referencing a single L2 SKU"

---

### 3. Schneider Catalog Interpretation Rules v1.2

**File:** `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md`  
**Status:** REVIEW_REQUIRED  
**Created:** 2025-01-XX  
**Last Updated:** 2025-01-XX (v1.1 - Critical corrections)  
**Reviewers:** Engineering + Procurement  
**Purpose:** Single authoritative reference for Schneider catalog (Page 8 to End) interpretation, aligned strictly to NSW Estimation Fundamentals v2.0

**Key Decisions:**
- **CRITICAL:** L2 generation rule - No combinatorial multiplication, only distinct SKUs from price list
- **CRITICAL:** Frame handling - Derived classification, NOT multiplier
- **CRITICAL:** Duty handling - AC1/AC3 are attributes unless SKU or price changes
- SC Layer mapping (SC_L1–SC_L4) for all Schneider items
- Accessory multiplication rules (SC_L4, never multiply)
- Frame and Pole coexistence (both SC_L1, but Frame is derived)
- Correct L2 generation approach: count(distinct (Make, OEM_Catalog_No))

**Transfer Path (after confirmation):**
- `docs/PHASE_5/ENGINEERING_REVIEW/` OR
- `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/`

**Dependency:** LC1E, LP1K completed; LC1D pending

---

## Confirmed Documents (Ready for Transfer)

*None yet*

---

## Transferred Documents (Archived)

*None yet*

---

## Document Categories

### Final Rules (Implementation Reference) ⭐
- **Schneider Final Rules v1.2** - Primary reference for all Schneider work

### Clarifications
- Schneider L2/L1 Differentiation Clarification v1.0
- **Schneider L1/L2 Expansion Logic v1.0** - The "6 Lines" question resolved

### Detailed Interpretation Guides
- Schneider Catalog Interpretation Rules v1.2

### Voltage Mapping Decisions
*(To be added)*

### Accessory Handling Rules
*(To be added)*

### OEM-Specific Policies
*(To be added)*

---

## Quick Reference

**How to add a new document:**
1. Create document in this folder
2. Add entry to this INDEX.md
3. Set status to DRAFT or REVIEW_REQUIRED
4. Assign reviewers
5. Update README.md if needed

**How to transfer a document:**
1. Confirm document status is CONFIRMED
2. Copy to target working folder
3. Update document metadata with transfer date/path
4. Change status to TRANSFERRED
5. Update this INDEX.md

---

**Maintained by:** Engineering Team

