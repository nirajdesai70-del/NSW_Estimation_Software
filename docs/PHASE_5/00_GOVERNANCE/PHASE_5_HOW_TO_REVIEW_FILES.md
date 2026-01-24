# How to Review Files - Step-by-Step Guide

**Version:** 1.0  
**Date:** 2025-01-27  
**Status:** CANONICAL  
**Owner:** Phase 5 Senate  

_Link audit fix: 2026-01-21 (Phase E) — escaped placeholder link syntax and corrected example references; no content meaning changed._

## Purpose
Practical step-by-step guide on how to review each file to ensure content is mapped and nothing is lost.

## Source of Truth
- **Canonical:** This is the practical review guide

---

## 🎯 Quick Answer

**Question:** Do we need to review each file individually?

**Answer:** YES - But we have a systematic process to make it efficient and ensure nothing is lost.

---

## 📋 Review Process (5 Steps)

### Step 1: Open the File
```
1. Open the file in your editor
2. Read through it once (get overview)
3. Note the file's main purpose
```

### Step 2: Extract Content Structure
```
1. List all major sections (H1 headings)
2. List all subsections (H2, H3 headings)
3. Note any key information blocks
4. Note any tables, lists, or structured data
```

**Template:**
```
File: [FILENAME]
Sections Found:
- Section 1: [NAME]
- Section 2: [NAME]
- Section 3: [NAME]
...
```

### Step 3: Map Content to Target
```
1. For each section, determine:
   - Does it stay in this file? (YES/NO)
   - If NO, where does it go?
   - Does it need to be split?
   - Does it need to be merged with other content?
```

**Template:**
```
Section: [SECTION_NAME]
- Stays in file: [YES/NO]
- If NO, target: [TARGET_FILE]
- Split needed: [YES/NO]
- Merge needed: [YES/NO]
```

### Step 4: Track References
```
1. Find all markdown links: [text] (path)
2. Find all file references: mentions of other files
3. Find all section references: #section-name
4. Note which references will break
5. Plan how to update them
```

**Template:**
```
References Found:
- Link: [text] (path) → Will break? [YES/NO] → Update to: [NEW_PATH]
- File reference: [FILENAME] → Will break? [YES/NO] → Update to: [NEW_PATH]
- Section reference: #section → Will break? [YES/NO] → Update to: [NEW_SECTION]
```

### Step 5: Verify Completeness
```
1. Count sections: [NUMBER]
2. Verify all sections mapped: [YES/NO]
3. Verify all references tracked: [YES/NO]
4. Verify nothing missed: [YES/NO]
```

---

## 📝 Practical Example

### Example: Reviewing `PHASE_5_SCOPE_FENCE.md`

**Step 1: Open File**
- File opened, read through once
- Purpose: Defines Phase 5 scope and exclusions

**Step 2: Extract Structure**
```
Sections Found:
- Phase 5 Purpose
- Phase 5 Scope (Step 1 & 2)
- Explicit Exclusions
- Success Criteria
- Post-Phase 5 Scope
- Execution Order
- Related Documents
```

**Step 3: Map Content**
```
Section: Phase 5 Purpose
- Stays in file: YES
- Target: Same file (00_GOVERNANCE/PHASE_5_SCOPE_FENCE.md)

Section: Phase 5 Scope
- Stays in file: YES
- Target: Same file (00_GOVERNANCE/PHASE_5_SCOPE_FENCE.md)

Section: Explicit Exclusions
- Stays in file: YES
- Target: Same file (00_GOVERNANCE/PHASE_5_SCOPE_FENCE.md)

... (all sections stay in same file)
```

**Step 4: Track References**
```
References Found:
\- Link: [PHASE_5_PENDING_UPGRADES_INTEGRATION.md] (PHASE_5_PENDING_UPGRADES_INTEGRATION.md)
  → Will break? YES (file moving to 02_FREEZE_GATE/)
  → Update to: [PHASE_5_PENDING_UPGRADES_INTEGRATION.md] (../02_FREEZE_GATE/PHASE_5_PENDING_UPGRADES_INTEGRATION.md)

\- Link: [SCOPE_SEPARATION.md] (SCOPE_SEPARATION.md)
  → Will break? YES (file moving to 00_GOVERNANCE/)
  → Update to: [SCOPE_SEPARATION.md] (SCOPE_SEPARATION.md) (same folder, no change)
```

**Step 5: Verify**
```
- Sections: 7
- All mapped: YES
- References: 2
- All tracked: YES
- Nothing missed: YES
```

---

## 🛠️ Tools to Help

### Option 1: Manual Review (Recommended for First Time)
- Use the template above
- Review each file one by one
- Document findings
- Create update plan

### Option 2: Automated Extraction (Helper Script)
Create a script that:
1. Extracts all headings
2. Extracts all links
3. Creates inventory
4. Helps with mapping

### Option 3: Hybrid Approach
1. Use script to extract structure
2. Manually review content
3. Manually map to targets
4. Use script to update links

---

## 📊 Review Progress Tracker

Create a simple spreadsheet or table:

| File | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Status |
|------|--------|--------|--------|--------|--------|--------|
| PHASE_5_SCOPE_FENCE.md | ✅ | ✅ | ✅ | ✅ | ✅ | COMPLETE |
| PHASE_5_EXECUTION_SUMMARY.md | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | PENDING |
| ... | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | PENDING |

---

## ⏱️ Time Estimate

**Per File:**
- Step 1 (Open & Read): 5-10 minutes
- Step 2 (Extract Structure): 5 minutes
- Step 3 (Map Content): 5-10 minutes
- Step 4 (Track References): 5-10 minutes
- Step 5 (Verify): 2-3 minutes

**Total per file:** 20-40 minutes

**For 19 files:** 6-13 hours (can be done incrementally)

---

## ✅ Quality Checklist

After reviewing each file, verify:
- [ ] All sections identified
- [ ] All content mapped
- [ ] All references tracked
- [ ] Update plan created
- [ ] Nothing missed

---

## 🚀 Recommended Approach

### Phase 1: Review All (1-2 days)
1. Review all 19 files
2. Document all findings
3. Create master update plan
4. Get approval

### Phase 2: Move Files (1 day)
1. Move files one by one
2. Update references as you go
3. Verify after each move

### Phase 3: Final Verification (1 day)
1. Verify all files moved
2. Verify all content present
3. Verify all links working
4. Final approval

**Total Time:** 3-4 days (can be done incrementally)

---

## 📚 Related Documents

- `PHASE_5_CONTENT_TRACEABILITY.md` - Content mapping matrix
- `PHASE_5_FILE_CONTENT_REVIEW_CHECKLIST.md` - Detailed checklist
- `PHASE_5_CONTENT_SAFETY_PROTOCOL.md` - Safety measures

---

## Change Log
- v1.0: Created practical review guide

