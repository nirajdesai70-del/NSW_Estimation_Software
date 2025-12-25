# Quick Reference: File Organization & Usage

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## 🎯 Quick Answers

### ✅ All Phase 5 Files Mapped?
**YES** - All 20 files in `docs/PHASE_5/` are mapped in `PHASE_5_DOC_INDEX.md`

### ✅ Planning Complete?
**YES** - Every file has a target location and purpose

### ✅ Do Code Files Need Rearrangement?
**NO** - `project/nish/` files stay as reference only (no movement needed)

### ✅ Same Language Established?
**YES** - See `PHASE_5_FILE_ORGANIZATION_POLICY.md` for complete rules

---

## 📁 Three Locations - Three Purposes

### 1. `docs/PHASE_5/` → Phase 5 Senate (CANONICAL TRUTH)
**Purpose:** Phase 5 analysis and design work

**Contains:**
- Data Dictionary (Step 1 - FROZEN)
- Schema Canon (Step 2 - FROZEN)
- Governance documents
- Traceability matrices

**When to Use:**
- Creating Phase 5 deliverables
- Writing canonical definitions
- During Step 1 and Step 2

**Rules:**
- ✅ Canonical truth goes here
- ❌ Do NOT copy from `project/nish/`

---

### 2. `project/nish/` → Legacy Analysis (REFERENCE ONLY)
**Purpose:** Legacy system analysis (read-only)

**Contains:**
- Legacy schema extraction plans
- Migration strategy documents
- `NSW_SCHEMA_CANON.md` (planning doc, NOT canonical schema)

**When to Use:**
- Studying legacy behavior
- Understanding legacy structure
- Identifying anti-patterns

**Rules:**
- ✅ READ-ONLY reference
- ✅ Study for "what not to do"
- ❌ Do NOT copy code/schema
- ❌ Do NOT move files
- ❌ Do NOT use as canonical truth

**Key Point:**
- `project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` = Planning document
- `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` = Actual canonical schema (to be created)

---

### 3. `features/` → Feature Documentation (BASELINE)
**Purpose:** Curated feature documentation (frozen)

**Contains:**
- Module documentation
- Feature specifications
- Frozen baselines

**When to Use:**
- Understanding existing features
- Aligning canonical definitions

**Rules:**
- ✅ Reference for semantics
- ❌ Do NOT modify during Phase 5

---

## 🔄 How Information Flows

```
project/nish/ (Legacy - Reference)
    ↓ Study & Learn
    ↓
docs/PHASE_5/01_REFERENCE/LEGACY_REVIEW/ (Document Learnings)
    ↓
docs/PHASE_5/05_TRACEABILITY/LEGACY_TO_CANONICAL_MAP.md (Map Decisions)
    ↓
docs/PHASE_5/03_DATA_DICTIONARY/ (Canonical Definitions)
    ↓
docs/PHASE_5/04_SCHEMA_CANON/ (Canonical Schema)
```

**Important:** Information flows FROM legacy TO canonical, but code/schema does NOT flow directly.

---

## 📋 File Status

### Phase 5 Files
- **Total:** 20 files
- **Status:** ✅ All mapped
- **Location:** `docs/PHASE_5/` root
- **Action:** Can move to senate folders (optional, gradual)

### project/nish Files
- **Status:** ✅ Reference only
- **Action:** ✅ NO ACTION NEEDED - Stay as-is

---

## 🎯 Decision: Where Does a File Belong?

```
Is this Phase 5 canonical work?
├─ YES → docs/PHASE_5/ (senate folder)
│
├─ NO → Is this legacy analysis?
│   ├─ YES → project/nish/ (keep as-is)
│   │
│   └─ NO → features/ (keep as-is)
```

---

## 📚 Key Documents

| Document | Purpose |
|----------|---------|
| `PHASE_5_FILE_ORGANIZATION_POLICY.md` | Complete file organization rules |
| `PHASE_5_FILE_STATUS_REPORT.md` | Complete status report |
| `PHASE_5_DOC_INDEX.md` | All files mapped |
| `QUICK_REFERENCE_FILE_ORGANIZATION.md` | This document |

---

## ✅ Verification Checklist

- [x] All Phase 5 files mapped ✅
- [x] project/nish files identified as reference ✅
- [x] Clear separation of purposes ✅
- [x] Policy document created ✅
- [x] Same language established ✅

**Result:** ✅ Everything is organized and clear!

---

## Change Log
- v1.0: Created quick reference guide

