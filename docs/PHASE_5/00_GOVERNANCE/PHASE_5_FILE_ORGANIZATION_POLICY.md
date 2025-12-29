# Phase 5 File Organization Policy

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

## Purpose
Clear policy on where files belong, how to use them, and when to use them. This ensures everyone speaks the same language about file locations and purposes.

## Source of Truth
- **Canonical:** This is the authoritative file organization policy

---

## 🎯 Quick Answer to Your Questions

### Q1: Are all Phase 5 files already mapped?
**Answer: YES ✅**
- All 20 existing files in `docs/PHASE_5/` are mapped in `PHASE_5_DOC_INDEX.md`
- Planning is complete and documented
- Each file has a target senate location

### Q2: Do code files need to be rearranged?
**Answer: NO - Different Purpose**
- `project/nish/` is **read-only reference** (legacy analysis)
- `docs/PHASE_5/` is **canonical truth** (Phase 5 Senate)
- They serve different purposes and should NOT be mixed

---

## 📁 Three-Location Model

### Location 1: `docs/PHASE_5/` (Phase 5 Senate) ✅ CANONICAL

**Purpose:** Phase 5 analysis and design work (canonical truth)

**Contains:**
- Phase 5 governance documents
- Data Dictionary (Step 1 output - FROZEN)
- Schema Canon (Step 2 output - FROZEN)
- Freeze gate verification
- Traceability matrices

**Rules:**
- ✅ This is where Phase 5 work happens
- ✅ Canonical definitions go here
- ✅ FROZEN documents stay here
- ❌ Do NOT copy from `project/nish/` here
- ❌ Do NOT mix legacy analysis with canonical work

**When to Use:**
- During Phase 5 Step 1 (Data Dictionary)
- During Phase 5 Step 2 (Schema Design)
- During Freeze Gate verification
- When creating canonical definitions

---

### Location 2: `project/nish/` (Legacy Analysis) 📖 REFERENCE ONLY

**Purpose:** Legacy system analysis (read-only reference)

**Contains:**
- Legacy schema extraction plans
- Legacy data model notes
- Migration strategy documents
- NSW schema extraction plans (from legacy)

**Rules:**
- ✅ READ-ONLY reference only
- ✅ Study for "what not to do"
- ✅ Extract anti-patterns
- ❌ Do NOT copy code/schema from here
- ❌ Do NOT use as canonical truth
- ❌ Do NOT modify files here

**When to Use:**
- When reviewing legacy system behavior
- When identifying anti-patterns to avoid
- When documenting "what not to do"
- When creating legacy-to-canonical mapping

**Example:**
- `project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md` is a **planning document** for extracting schema from legacy
- This is NOT the canonical schema - it's a reference/plan
- The actual canonical schema will be created in `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`

---

### Location 3: `features/` (Feature Documentation) 📚 BASELINE

**Purpose:** Curated feature documentation (frozen baselines)

**Contains:**
- Module documentation (CIM, Quotation, Master BOM, etc.)
- Feature specifications
- Frozen baselines

**Rules:**
- ✅ Reference for understanding existing features
- ✅ Use for semantic alignment
- ❌ Do NOT modify during Phase 5
- ❌ Do NOT copy directly into Phase 5

**When to Use:**
- When understanding existing feature semantics
- When aligning canonical definitions with existing features
- When verifying consistency

---

## 🔄 How They Relate

```
project/nish/ (Legacy Analysis)
    ↓ (read-only reference)
    ↓ Study for anti-patterns
    ↓
docs/PHASE_5/01_REFERENCE/LEGACY_REVIEW/ (document learnings)
    ↓
docs/PHASE_5/05_TRACEABILITY/LEGACY_TO_CANONICAL_MAP.md (map decisions)
    ↓
docs/PHASE_5/03_DATA_DICTIONARY/ (canonical definitions)
    ↓
docs/PHASE_5/04_SCHEMA_CANON/ (canonical schema)
```

**Key Point:** Information flows FROM legacy (reference) TO canonical (truth), but code/schema does NOT flow directly.

---

## 📋 File Mapping Status

### Phase 5 Files (All Mapped ✅)

| File | Current Location | Target Location | Status |
|------|------------------|----------------|--------|
| All 20 files | `docs/PHASE_5/` | Various senate folders | ✅ Mapped in DOC_INDEX |

**Action:** Files can be moved to senate locations when ready (see `PHASE_5_DOC_INDEX.md`)

---

### project/nish Files (Reference Only - No Rearrangement Needed ✅)

| File | Location | Purpose | Action |
|------|----------|---------|--------|
| `NSW_SCHEMA_CANON.md` | `project/nish/03_NSW_SCHEMA/` | Legacy extraction plan | ✅ Keep as-is (reference) |
| Other nish files | `project/nish/` | Legacy analysis | ✅ Keep as-is (reference) |

**Action:** NO rearrangement needed - these are reference documents

---

## 🎯 Decision Framework: Where Does a File Belong?

### Use This Decision Tree:

```
Is this Phase 5 canonical work?
├─ YES → docs/PHASE_5/ (appropriate senate folder)
│   ├─ Governance → 00_GOVERNANCE/
│   ├─ Data Dictionary → 03_DATA_DICTIONARY/
│   ├─ Schema Canon → 04_SCHEMA_CANON/
│   └─ etc.
│
├─ NO → Is this legacy analysis?
│   ├─ YES → project/nish/ (keep as-is, read-only)
│   │
│   └─ NO → Is this feature documentation?
│       └─ YES → features/ (keep as-is, baseline)
```

---

## 🚫 What NOT to Do

### ❌ Do NOT:
1. Copy files from `project/nish/` into `docs/PHASE_5/`
2. Mix legacy analysis with canonical definitions
3. Use `project/nish/` files as canonical truth
4. Rearrange `project/nish/` files (they're reference only)
5. Modify `project/nish/` files during Phase 5

### ✅ DO:
1. Study `project/nish/` files for reference
2. Document learnings in `docs/PHASE_5/01_REFERENCE/LEGACY_REVIEW/`
3. Create canonical definitions in `docs/PHASE_5/03_DATA_DICTIONARY/`
4. Create canonical schema in `docs/PHASE_5/04_SCHEMA_CANON/`
5. Map legacy decisions in `docs/PHASE_5/05_TRACEABILITY/LEGACY_TO_CANONICAL_MAP.md`

---

## 📚 Specific Examples

### Example 1: `project/nish/03_NSW_SCHEMA/NSW_SCHEMA_CANON.md`

**What it is:**
- Planning document for extracting schema from legacy
- Reference material for understanding legacy schema

**What it is NOT:**
- The canonical schema (that goes in `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`)
- A file to copy or move

**How to use it:**
1. Read it to understand legacy schema structure
2. Document learnings in `docs/PHASE_5/01_REFERENCE/LEGACY_REVIEW/LEGACY_DATA_MODEL_NOTES.md`
3. Create canonical schema in `docs/PHASE_5/04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md` (new, clean design)

---

### Example 2: Phase 5 Files

**Current state:**
- 20 files in `docs/PHASE_5/` root
- All mapped to senate locations

**Action needed:**
- Move files to senate locations (optional, can be done gradually)
- Or keep in root and reference from senate structure
- Senate structure is ready for new work

---

## ✅ Verification Checklist

Use this to verify file organization:

- [ ] All Phase 5 files mapped in `PHASE_5_DOC_INDEX.md`
- [ ] `project/nish/` files remain as reference only
- [ ] No files copied from `project/nish/` to `docs/PHASE_5/`
- [ ] Legacy learnings documented in `01_REFERENCE/LEGACY_REVIEW/`
- [ ] Canonical work happens in `03_DATA_DICTIONARY/` and `04_SCHEMA_CANON/`
- [ ] Clear separation between reference and canonical

---

## 🎯 Summary

1. **All Phase 5 files are mapped** ✅ - See `PHASE_5_DOC_INDEX.md`
2. **No code files need rearrangement** ✅ - `project/nish/` stays as reference
3. **Clear separation of purposes** ✅ - Each location has a specific role
4. **Same language** ✅ - This policy document defines it

---

## Change Log
- v1.0: Created file organization policy

