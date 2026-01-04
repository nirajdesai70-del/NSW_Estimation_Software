# Archive Old System Analysis: catalog_pipeline → catalog_pipeline_v2

**Date:** 2025-01-03  
**Status:** DECISION DOCUMENT  
**Purpose:** Comprehensive analysis of archiving `catalog_pipeline/` (old) and making `catalog_pipeline_v2/` the final clean system

---

## Executive Summary

**Recommendation:** ✅ **YES, ARCHIVE OLD SYSTEM** - But with a **phased migration approach** and **preserve critical outputs**.

**Key Finding:** The two systems serve different purposes but v2 is the future. Archive v1 safely while ensuring no data loss and maintaining reference access.

---

## 1. System Comparison

### 1.1 Old System (`catalog_pipeline/`)

**Purpose:**
- PDF/XLSX → CSV conversion
- Profile-based normalization (YAML profiles)
- Import-ready CSV outputs
- Simpler, linear workflow

**Key Features:**
- ✅ CSV-based (lightweight)
- ✅ Profile-driven (flexible)
- ✅ TEST vs FINAL governance
- ✅ Error tracking
- ✅ Log summaries

**Current Status:**
- ✅ Has working outputs in `output/final/`
- ✅ Has profiles in `profiles/schneider/`
- ✅ Has historical data (6 final CSVs, 23 archived CSVs)
- ⚠️ May still be referenced by legacy import processes

---

### 1.2 New System (`catalog_pipeline_v2/`)

**Purpose:**
- Canonical extraction → L2 SKU Master → L1 Lines
- XLSX-based Engineer Review workbooks
- Phase-5 aligned architecture
- Structured active/archives workflow

**Key Features:**
- ✅ L1/L2 separation (better data model)
- ✅ XLSX workbooks (richer format)
- ✅ Active/Archives structure (clear workflow)
- ✅ QC processes (validation)
- ✅ Templates for new series
- ✅ Operating model (Cursor + ChatGPT)
- ✅ Phase-5 ready

**Current Status:**
- ✅ Active LC1E work in progress
- ✅ LC1E archived (2025-07-15 WEF)
- ✅ Templates and documentation complete
- ⚠️ Still in development (QC validation failing)

---

## 2. Pros of Archiving Old System

### 2.1 Clean Workspace ✅

**Benefits:**
- ✅ Single source of truth (no confusion)
- ✅ Clearer project structure
- ✅ Easier onboarding (one system to learn)
- ✅ Reduced maintenance burden
- ✅ Focused development effort

**Impact:** High - Reduces cognitive load and maintenance overhead

---

### 2.2 Alignment with Phase-5 ✅

**Benefits:**
- ✅ v2 is designed for Phase-5 architecture
- ✅ L1/L2 model matches Phase-5 requirements
- ✅ XLSX format aligns with Engineer Review workflow
- ✅ Active/Archives structure supports governance

**Impact:** Critical - v2 is the future direction

---

### 2.3 Better Data Model ✅

**Benefits:**
- ✅ L2-first approach (one SKU per catalog number)
- ✅ L1 derivation (duty × voltage combinations)
- ✅ Price at L2 only (no duplication)
- ✅ Accessory handling (FEATURE lines)

**Impact:** High - Better data integrity and consistency

---

### 2.4 Improved Workflow ✅

**Benefits:**
- ✅ Standardized folder structure
- ✅ QC processes (validation, freeze gates)
- ✅ Templates for new series (faster conversion)
- ✅ Operating model (clear responsibilities)

**Impact:** Medium - Better repeatability and quality

---

## 3. Cons of Archiving Old System

### 3.1 Potential Data Loss ⚠️

**Risks:**
- ⚠️ Legacy CSV outputs may be needed for reference
- ⚠️ Historical profiles may have unique logic
- ⚠️ Import processes may still reference old CSVs
- ⚠️ Test data and calibration work may be lost

**Mitigation:**
- ✅ Archive all outputs before deletion
- ✅ Document what was archived and why
- ✅ Keep profiles for reference
- ✅ Verify no active dependencies

**Impact:** Medium - Mitigatable with proper archiving

---

### 3.2 Loss of Working Reference ⚠️

**Risks:**
- ⚠️ Old system may have working solutions for edge cases
- ⚠️ Profile logic may be useful for new series
- ⚠️ CSV format may be needed for some integrations
- ⚠️ Historical decisions documented in old system

**Mitigation:**
- ✅ Archive with full documentation
- ✅ Extract key decisions to v2 docs
- ✅ Keep profiles accessible (read-only)
- ✅ Document migration path

**Impact:** Low - Can be preserved in archive

---

### 3.3 Breaking Active Dependencies ⚠️

**Risks:**
- ⚠️ Import scripts may reference old CSV paths
- ⚠️ Other tools may depend on old structure
- ⚠️ Documentation may reference old paths
- ⚠️ CI/CD may have old system checks

**Mitigation:**
- ✅ Audit all dependencies first
- ✅ Update references before archiving
- ✅ Create migration guide
- ✅ Test after archiving

**Impact:** High - Must audit before archiving

---

### 3.4 v2 Still Has Issues ⚠️

**Risks:**
- ⚠️ QC validation currently failing (Page 8)
- ⚠️ Some features may not be complete
- ⚠️ May need old system as fallback
- ⚠️ Migration may reveal gaps

**Mitigation:**
- ✅ Fix v2 issues before full archive
- ✅ Keep old system accessible during transition
- ✅ Create rollback plan
- ✅ Test thoroughly before archive

**Impact:** Medium - Must fix v2 issues first

---

## 4. What TO DO

### 4.1 Before Archiving ✅

1. **✅ Audit Dependencies**
   - Search codebase for references to `catalog_pipeline/`
   - Check import scripts, documentation, CI/CD
   - List all dependencies

2. **✅ Preserve Critical Data**
   - Archive all CSV outputs (final + test)
   - Archive all profiles (YAML files)
   - Archive logs and error reports
   - Document what's being preserved

3. **✅ Extract Key Knowledge**
   - Document profile logic for reference
   - Extract decisions to v2 docs
   - Note any edge cases handled in v1
   - Create migration notes

4. **✅ Fix v2 Issues**
   - Resolve QC validation failures
   - Complete missing features
   - Test thoroughly
   - Get approval before archive

5. **✅ Create Archive Structure**
   ```
   ARCHIVE/2025-01-03_catalog_pipeline_v1/
   ├── 00_outputs/          # All CSV outputs
   ├── 01_profiles/          # YAML profiles
   ├── 02_scripts/           # normalize.py and tools
   ├── 03_logs/              # Historical logs
   ├── 04_errors/            # Error reports
   ├── 05_documentation/     # README and docs
   └── ARCHIVE_INDEX.md      # What's archived and why
   ```

---

### 4.2 During Archiving ✅

1. **✅ Move, Don't Delete**
   - Move to `ARCHIVE/` directory (not delete)
   - Keep structure intact
   - Preserve all files
   - Maintain git history

2. **✅ Update References**
   - Update documentation references
   - Update import scripts (if needed)
   - Update CI/CD (if needed)
   - Create redirect/alias if needed

3. **✅ Document Migration**
   - Create migration guide
   - Document what changed
   - Note breaking changes
   - Provide v1 → v2 mapping

4. **✅ Test After Archive**
   - Verify no broken references
   - Test v2 workflows
   - Confirm archive is accessible
   - Validate data preservation

---

### 4.3 After Archiving ✅

1. **✅ Update Documentation**
   - Update main README
   - Update SOPs
   - Update Phase-5 docs
   - Note archive location

2. **✅ Clean Workspace**
   - Remove old system from active paths
   - Update .gitignore if needed
   - Clean up temporary files
   - Organize v2 structure

3. **✅ Monitor**
   - Watch for missing references
   - Track v2 adoption
   - Collect feedback
   - Adjust as needed

---

## 5. What NOT TO DO

### 5.1 Don't Delete Immediately ❌

**Why:**
- ❌ May have active dependencies
- ❌ May need reference data
- ❌ May need rollback option
- ❌ May lose historical context

**Instead:**
- ✅ Archive first (move, don't delete)
- ✅ Keep accessible for reference
- ✅ Monitor for dependencies
- ✅ Delete only after verification

---

### 5.2 Don't Archive While v2 Has Issues ❌

**Why:**
- ❌ May need fallback
- ❌ May break workflows
- ❌ May lose working solution
- ❌ May create confusion

**Instead:**
- ✅ Fix v2 issues first
- ✅ Complete migration
- ✅ Test thoroughly
- ✅ Get approval

---

### 5.3 Don't Archive Without Documentation ❌

**Why:**
- ❌ May lose context
- ❌ May forget decisions
- ❌ May lose reference
- ❌ May break future work

**Instead:**
- ✅ Document everything
- ✅ Create archive index
- ✅ Extract key knowledge
- ✅ Preserve decisions

---

### 5.4 Don't Archive Without Audit ❌

**Why:**
- ❌ May break dependencies
- ❌ May lose active references
- ❌ May break imports
- ❌ May break CI/CD

**Instead:**
- ✅ Audit all dependencies
- ✅ Update references first
- ✅ Test after archive
- ✅ Monitor for issues

---

### 5.5 Don't Mix Systems ❌

**Why:**
- ❌ Creates confusion
- ❌ Duplicates effort
- ❌ Maintains two systems
- ❌ Slows adoption

**Instead:**
- ✅ Choose one system (v2)
- ✅ Archive old completely
- ✅ Update all references
- ✅ Focus on v2

---

## 6. Recommended Approach

### 6.1 Phased Migration (Recommended) ✅

**Phase 1: Preparation (Week 1)**
- [ ] Audit all dependencies
- [ ] Document what to preserve
- [ ] Fix v2 QC issues
- [ ] Create archive structure

**Phase 2: Archive (Week 2)**
- [ ] Move old system to ARCHIVE/
- [ ] Preserve all outputs and profiles
- [ ] Create ARCHIVE_INDEX.md
- [ ] Extract key knowledge to v2

**Phase 3: Update (Week 3)**
- [ ] Update all references
- [ ] Update documentation
- [ ] Update import scripts (if needed)
- [ ] Test thoroughly

**Phase 4: Clean (Week 4)**
- [ ] Remove old system from active paths
- [ ] Clean workspace
- [ ] Update .gitignore
- [ ] Final verification

---

### 6.2 Alternative: Keep Both (Not Recommended) ❌

**Why Not:**
- ❌ Maintains confusion
- ❌ Duplicates effort
- ❌ Slows v2 adoption
- ❌ Creates technical debt

**When to Consider:**
- ⚠️ If v2 has critical gaps
- ⚠️ If old system has active production use
- ⚠️ If migration is too risky

**Current Assessment:** ❌ Not needed - v2 is ready

---

## 7. Risk Assessment

### 7.1 Low Risk ✅
- Archiving completed work
- Preserving historical data
- Creating archive structure
- Documenting migration

### 7.2 Medium Risk ⚠️
- Breaking dependencies (mitigated by audit)
- Losing reference data (mitigated by archive)
- v2 issues (mitigated by fixing first)
- Migration gaps (mitigated by testing)

### 7.3 High Risk ❌
- Data loss (mitigated by move, not delete)
- Breaking production (mitigated by audit)
- Losing working solutions (mitigated by extraction)

---

## 8. Success Criteria

**Archive is successful when:**
- ✅ All dependencies identified and updated
- ✅ All data preserved in archive
- ✅ v2 issues resolved
- ✅ All references updated
- ✅ Documentation complete
- ✅ No broken workflows
- ✅ Archive accessible for reference
- ✅ v2 is the single active system

---

## 9. Decision Matrix

| Factor | Weight | Archive Now | Keep Both | Archive Later |
|--------|--------|-------------|-----------|---------------|
| Clean workspace | High | ✅ +2 | ❌ -1 | ⚠️ 0 |
| Phase-5 alignment | Critical | ✅ +3 | ❌ -2 | ⚠️ 0 |
| Data preservation | High | ✅ +1 | ✅ +1 | ✅ +1 |
| Risk of breakage | Medium | ⚠️ -1 | ✅ +1 | ✅ +1 |
| Maintenance burden | Medium | ✅ +2 | ❌ -2 | ⚠️ 0 |
| **Total Score** | | **+7** | **-3** | **+2** |

**Recommendation:** ✅ **Archive Now** (with proper preparation)

---

## 10. Action Plan

### Immediate Actions (This Week)

1. **✅ Audit Dependencies**
   ```bash
   # Search for references
   grep -r "catalog_pipeline/" --exclude-dir=ARCHIVE
   grep -r "normalize.py" --exclude-dir=ARCHIVE
   ```

2. **✅ Fix v2 QC Issues**
   - Resolve Page 8 validation failures
   - Complete missing features
   - Test thoroughly

3. **✅ Create Archive Structure**
   - Create `ARCHIVE/2025-01-03_catalog_pipeline_v1/`
   - Plan what goes where
   - Create ARCHIVE_INDEX.md template

### Next Week Actions

4. **✅ Archive Old System**
   - Move files to ARCHIVE/
   - Preserve all outputs
   - Document everything

5. **✅ Update References**
   - Update documentation
   - Update scripts
   - Update CI/CD

6. **✅ Test and Verify**
   - Test v2 workflows
   - Verify no broken references
   - Confirm archive accessibility

---

## 11. Conclusion

**Final Recommendation:** ✅ **YES, ARCHIVE OLD SYSTEM** - But do it **carefully and systematically**.

**Key Points:**
1. ✅ v2 is the future (Phase-5 aligned)
2. ✅ Archive preserves data (move, don't delete)
3. ✅ Fix v2 issues first
4. ✅ Audit dependencies before archive
5. ✅ Document everything

**Timeline:** 3-4 weeks for safe migration

**Risk Level:** Low (with proper preparation)

---

## 12. References

- `ARCHIVE_AND_MIGRATION_PLAN.md` - Existing migration plan
- `OPERATING_MODEL.md` - v2 operating model
- `NEXT_SERIES_BOOTSTRAP.md` - v2 workflow
- `catalog_pipeline/README.md` - Old system docs

---

**Status:** ✅ ANALYSIS COMPLETE - READY FOR DECISION

**Next Step:** Review this analysis and decide on approach, then execute action plan.




