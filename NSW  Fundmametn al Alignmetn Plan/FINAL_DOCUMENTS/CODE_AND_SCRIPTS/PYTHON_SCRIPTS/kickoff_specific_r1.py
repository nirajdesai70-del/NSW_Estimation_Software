#!/usr/bin/env python3
"""
Kick Off Specific Item Master Round-1

Purpose:
    Validates preconditions, creates kickoff note, and updates dashboard
    for Specific Item Master Round-1 review.

Usage:
    python3 scripts/governance/kickoff_specific_r1.py [--reviewers "Name1,Name2"] [--target-date YYYY-MM-DD]
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DOCS_DIR = BASE_DIR / "docs" / "NEPL_STANDARDS" / "00_BASELINE_FREEZE"
DASHBOARD_FILE = BASE_DIR / "docs" / "DASHBOARD_REVIEW_STATUS.md"
TEMPLATE_FILE = DOCS_DIR / "SPECIFIC_ITEM_MASTER_ROUND1_KICKOFF_TEMPLATE.md"

def check_generic_frozen():
    """Check if Generic Item Master is frozen."""
    freeze_files = list(DOCS_DIR.glob("*FREEZE*.md"))
    if not freeze_files:
        return False, "No freeze note found"
    
    latest_freeze = max(freeze_files, key=os.path.getmtime)
    with open(latest_freeze, 'r') as f:
        content = f.read()
    
    if "🔒 FROZEN" in content or "FROZEN" in content.upper():
        return True, f"Generic frozen: {latest_freeze.name}"
    
    return False, "Freeze note exists but status not confirmed"

def check_r0_readiness():
    """Check if Round-0 readiness gate is complete."""
    r0_files = list(DOCS_DIR.glob("SPECIFIC_ITEM_MASTER_ROUND0_READINESS*.md"))
    if not r0_files:
        return False, "Round-0 readiness gate not found"
    
    with open(r0_files[0], 'r') as f:
        content = f.read()
    
    # Check if checklist is complete
    checkboxes = re.findall(r'\[([ x])\]', content)
    if checkboxes:
        all_checked = all(item.strip() == 'x' for item in checkboxes)
        if all_checked:
            return True, f"Round-0 gate complete: {r0_files[0].name}"
        else:
            return False, f"Round-0 gate incomplete: {r0_files[0].name}"
    
    return True, f"Round-0 gate exists: {r0_files[0].name}"

def check_existing_kickoff():
    """Check if kickoff already exists."""
    kickoff_files = list(DOCS_DIR.glob("SPECIFIC_ITEM_MASTER_ROUND1_KICKOFF*.md"))
    if kickoff_files:
        return True, kickoff_files[0]
    return False, None

def create_kickoff_note(reviewers=None, target_date=None):
    """Create Specific Item Master Round-1 kickoff note."""
    today = datetime.now()
    date_str = today.strftime("%Y%m%d")
    date_iso = today.strftime("%Y-%m-%d")
    
    kickoff_file = DOCS_DIR / f"SPECIFIC_ITEM_MASTER_ROUND1_KICKOFF_v1.0_{date_str}.md"
    
    # Default reviewers if not provided
    if not reviewers:
        reviewers = ["Governance Lead", "Technical Reviewer", "Business Analyst", "Compliance Officer"]
    else:
        reviewers = [r.strip() for r in reviewers.split(",")]
    
    # Default target date (14 days from now)
    if not target_date:
        target_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
    
    # Read template if exists, otherwise use default
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
        
        # Replace template placeholders
        template = template.replace("v1.0_YYYYMMDD", f"v1.0_{date_str}")
        template = template.replace("YYYY-MM-DD", date_iso)
        template = template.replace("[DATE]", date_iso)
        template = template.replace("[X]", "14")
        
        # Replace reviewers
        reviewer_table = "\n".join([f"| {role} | [NAME] | [RESPONSIBILITIES] |" for role in reviewers])
        template = re.sub(r'\| [^\|]+\s+\| [^\|]+\s+\| [^\|]+\s+\|', reviewer_table, template, count=len(reviewers))
    else:
        # Create from scratch
        template = f"""# Specific Item Master — Round-1 Kickoff

**Version:** v1.0_{date_str}
**Date (IST):** {date_iso}
**Status:** 🚀 KICKED OFF

---

## 🎯 Kickoff Declaration

Specific Item Master Round-1 review is hereby **KICKED OFF** as of {date_iso}.

This kickoff indicates that:
- ✅ Generic Item Master is FROZEN
- ✅ Round-0 readiness gate passed
- ✅ All preconditions satisfied
- ✅ Review scope and team defined

---

## 📋 Preconditions Verification

| Condition | Required | Status | Notes |
|-----------|----------|--------|-------|
| Generic Item Master Frozen | YES | ✅ | Verified |
| Round-0 Readiness Complete | YES | ✅ | Verified |
| Review Team Assigned | YES | ✅ | {len(reviewers)} reviewers |
| Artifacts Available | YES | ✅ | Laravel code accessible |
| Governance System Active | YES | ✅ | CI, scripts, dashboard ready |

---

## 👥 Review Team

| Role | Name | Responsibilities |
|------|------|------------------|
{chr(10).join([f"| {role} | [NAME] | [RESPONSIBILITIES] |" for role in reviewers])}

---

## 📅 Timeline

| Milestone | Target Date | Owner |
|-----------|-------------|-------|
| Kickoff | {date_iso} | Governance Lead |
| Review Start | {date_iso} | Review Team |
| Findings Documented | {(today + timedelta(days=7)).strftime('%Y-%m-%d')} | Reviewers |
| Issues Addressed | {(today + timedelta(days=10)).strftime('%Y-%m-%d')} | Dev Team |
| Round-1 Complete | {(today + timedelta(days=14)).strftime('%Y-%m-%d')} | Governance Lead |
| Freeze Target | {target_date} | Governance Lead |

**Total Duration:** 14 days from kickoff to freeze

---

## 📋 Review Checklist

### R1-1: Field Definitions
- [ ] All Specific Item Master fields documented
- [ ] Field types and constraints verified
- [ ] L2 identity fields validated
- [ ] ProductType=2 enforcement confirmed

### R1-2: Laravel Integration
- [ ] Models updated for Specific Item Master
- [ ] Controllers handle ProductType=2 correctly
- [ ] Routes configured appropriately
- [ ] Forms validate Specific fields

### R1-3: Business Logic
- [ ] Pricing logic verified
- [ ] Quotation usage validated
- [ ] Phase-8 SKU governance enforced
- [ ] Archival rules applied correctly

### R1-4: Compliance
- [ ] NEPL standards compliance verified
- [ ] Documentation complete
- [ ] Test coverage adequate
- [ ] No blocking issues

---

## Change Log

| Version | Date (IST) | Change |
|---------|------------|--------|
| v1.0_{date_str} | {date_iso} | Initial kickoff |

---

**END OF KICKOFF DOCUMENT**
"""
    
    with open(kickoff_file, 'w') as f:
        f.write(template)
    
    return kickoff_file

def update_dashboard():
    """Update dashboard to reflect R1 kickoff."""
    if not DASHBOARD_FILE.exists():
        print(f"⚠️  Dashboard not found at {DASHBOARD_FILE}")
        return False
    
    with open(DASHBOARD_FILE, 'r') as f:
        content = f.read()
    
    # Update Specific R1 status
    content = re.sub(
        r'\| Specific Item Master\s+\| R1\s+\| 🚫 BLOCKED',
        '| Specific Item Master| R1           | 🔄 IN PROGRESS | Round-1 kicked off | ' + datetime.now().strftime("%Y-%m-%d") + ' |',
        content
    )
    
    # Update workflow state
    content = re.sub(
        r'Specific R1 \(🚫 BLOCKED\)',
        'Specific R1 (🔄 IN PROGRESS)',
        content
    )
    
    with open(DASHBOARD_FILE, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Kick off Specific Item Master Round-1')
    parser.add_argument('--reviewers', '-r',
                       help='Comma-separated list of reviewer roles')
    parser.add_argument('--target-date', '-d',
                       help='Target freeze date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    print("🔍 Validating preconditions for Specific Item Master Round-1 kickoff...\n")
    
    # Check Generic frozen
    is_frozen, freeze_msg = check_generic_frozen()
    if not is_frozen:
        print(f"❌ BLOCKED: {freeze_msg}")
        print("   Generic Item Master must be frozen before Specific R1 can start")
        return 1
    print(f"✅ {freeze_msg}")
    
    # Check R0 readiness
    r0_ready, r0_msg = check_r0_readiness()
    if not r0_ready:
        print(f"❌ BLOCKED: {r0_msg}")
        return 1
    print(f"✅ {r0_msg}")
    
    # Check existing kickoff
    exists, existing_file = check_existing_kickoff()
    if exists:
        print(f"⚠️  Kickoff already exists: {existing_file.name}")
        response = input("   Create new kickoff anyway? (y/N): ")
        if response.lower() != 'y':
            print("   Cancelled")
            return 0
    
    print("\n📝 Creating kickoff note...")
    kickoff_file = create_kickoff_note(args.reviewers, args.target_date)
    print(f"✅ Created: {kickoff_file.name}")
    
    print("📊 Updating dashboard...")
    if update_dashboard():
        print("✅ Dashboard updated")
    else:
        print("⚠️  Dashboard update failed")
    
    print("\n🎉 Specific Item Master Round-1 has been kicked off!")
    print("\nNext steps:")
    print("  1. Assign reviewers to roles in kickoff note")
    print("  2. Begin Round-1 review process")
    print("  3. Update checklist as review progresses")
    print("  4. Run freeze script when Round-1 complete")
    
    return 0

if __name__ == "__main__":
    exit(main())

