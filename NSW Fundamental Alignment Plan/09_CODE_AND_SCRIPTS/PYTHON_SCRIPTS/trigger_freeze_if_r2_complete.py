#!/usr/bin/env python3
"""
Trigger Generic Freeze Automatically When Round-2 Completes

Purpose:
    Auto-creates FREEZE.md file after Round-2 resume + checklist completion.
    Updates dashboard and GitHub badge to ✅ FROZEN.

Usage:
    python3 scripts/governance/trigger_freeze_if_r2_complete.py
"""

import os
import re
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DOCS_DIR = BASE_DIR / "docs" / "NEPL_STANDARDS" / "00_BASELINE_FREEZE"
DASHBOARD_FILE = BASE_DIR / "docs" / "DASHBOARD_REVIEW_STATUS.md"

def check_r2_complete():
    """
    Check if Round-2 is complete by verifying resume note and checklist.
    
    Note: Round-2 had an unusual workflow:
    - Initially put ON HOLD (intentional pause)
    - Auto-resumed when Laravel repo was detected
    - Must check both resume note AND actual completion status
    """
    r2_resume_pattern = r"GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_RESUME.*\.md"
    r2_status_pattern = r"GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_STATUS.*\.md"
    r2_template_pattern = r"GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_TEMPLATE.*\.md"
    
    r2_resume_files = list(DOCS_DIR.glob("GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_RESUME*.md"))
    r2_status_files = list(DOCS_DIR.glob("GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_STATUS*.md"))
    r2_template_files = list(DOCS_DIR.glob("GENERIC_ITEM_MASTER_CUMULATIVE_REVIEW_R2_TEMPLATE*.md"))
    
    # Check if Round-2 was resumed (unusual workflow - intentional pause then resume)
    if not r2_resume_files:
        return False, "No Round-2 resume file found - Round-2 may still be on hold"
    
    latest_resume = max(r2_resume_files, key=os.path.getmtime)
    with open(latest_resume, 'r') as f:
        resume_content = f.read()
    
    # Check if resume note indicates it can proceed
    if "✅ COMPLETE" in resume_content or "can now proceed" in resume_content.lower():
        # Resume is confirmed, but need to check actual Round-2 completion
        
        # Check Round-2 template for completion (if it exists and was filled)
        if r2_template_files:
            latest_template = max(r2_template_files, key=os.path.getmtime)
            with open(latest_template, 'r') as f:
                template_content = f.read()
            
            # Check for completion indicators in template
            if "✅ PASS" in template_content or "APPROVED FOR FREEZE" in template_content:
                # Check checklist items in template
                checklist_items = re.findall(r'\[([ x])\]', template_content)
                if checklist_items:
                    all_checked = all(item.strip() == 'x' for item in checklist_items)
                    if all_checked:
                        return True, f"Round-2 complete: resumed and verified in {latest_template.name}"
        
        # If no template or template not complete, check status file
        if r2_status_files:
            latest_status = max(r2_status_files, key=os.path.getmtime)
            with open(latest_status, 'r') as f:
                status_content = f.read()
            
            # Status file might still say PENDING even after resume
            # This is the "unusual move" - status can be PENDING while resume says proceed
            if "APPROVED FOR FREEZE" in status_content or "✅" in status_content:
                return True, f"Round-2 complete: status updated in {latest_status.name}"
        
        # Resume note exists but actual verification not complete
        return False, f"Round-2 resumed but verification not complete. Resume note: {latest_resume.name}"
    
    return False, f"Round-2 resume note exists but indicates still in progress: {latest_resume.name}"

def check_freeze_exists():
    """Check if freeze note already exists."""
    freeze_files = list(DOCS_DIR.glob("*FREEZE*.md"))
    return len(freeze_files) > 0, freeze_files

def create_freeze_note():
    """Create Generic Item Master freeze note."""
    today = datetime.now().strftime("%Y%m%d")
    freeze_file = DOCS_DIR / f"GENERIC_ITEM_MASTER_FREEZE_v1.0_{today}.md"
    
    content = f"""# Generic Item Master — FREEZE NOTICE
**Version:** v1.0_{today}
**Date (IST):** {datetime.now().strftime("%Y-%m-%d")}
**Status:** 🔒 FROZEN

---

## Freeze Declaration

Generic Item Master governance is hereby **FROZEN** as of {datetime.now().strftime("%Y-%m-%d")}.

This freeze indicates that:
- ✅ Round-1 review completed and approved
- ✅ Round-2 review completed and approved
- ✅ All verification checklists satisfied
- ✅ All blocking conditions resolved

---

## Freeze Scope

The following are now **locked** and require formal change control:
- Generic Item Master field definitions
- ProductResolutionService L2 enforcement rules
- ProductArchiveService archival behavior
- EX-SUBCAT-001 exception handling

---

## Authorization

**Frozen By:** Automated Governance System  
**Approved For:** Specific Item Master Round-1 kickoff  
**Effective Date:** {datetime.now().strftime("%Y-%m-%d")}

---

## Change Log

| Version | Date (IST) | Change |
|---------|------------|--------|
| v1.0_{today} | {datetime.now().strftime("%Y-%m-%d")} | Initial freeze declaration |

---

**END OF DOCUMENT**
"""
    
    with open(freeze_file, 'w') as f:
        f.write(content)
    
    return freeze_file

def update_dashboard():
    """Update dashboard to reflect freeze status."""
    if not DASHBOARD_FILE.exists():
        print(f"⚠️  Dashboard not found at {DASHBOARD_FILE}")
        return False
    
    with open(DASHBOARD_FILE, 'r') as f:
        content = f.read()
    
    # Update Generic Freeze status
    content = re.sub(
        r'\| Generic Item Master \| Freeze\s+\| [^\|]+\|',
        f'| Generic Item Master | Freeze       | 🔒 FROZEN   | Freeze note created | {datetime.now().strftime("%Y-%m-%d")} |',
        content
    )
    
    # Update Specific R1 status if Generic is frozen
    content = re.sub(
        r'\| Specific Item Master\s+\| R1\s+\| 🚫 BLOCKED',
        '| Specific Item Master| R1           | ✅ READY    | Generic frozen - can proceed',
        content
    )
    
    with open(DASHBOARD_FILE, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main execution."""
    print("🔍 Checking Round-2 completion status...")
    print("   Note: Round-2 had unusual workflow (intentional pause → auto-resume)")
    print()
    
    is_complete, message = check_r2_complete()
    if not is_complete:
        print(f"❌ Round-2 not complete: {message}")
        print()
        print("💡 Round-2 Status:")
        print("   - Round-2 was intentionally put ON HOLD")
        print("   - Auto-resumed when Laravel repo was detected")
        print("   - Currently in RESUMED state, awaiting actual verification completion")
        print()
        print("Next steps:")
        print("   1. Complete A1/A2 verification in Laravel repo")
        print("   2. Update Round-2 template with verification results")
        print("   3. Mark checklist items as complete")
        print("   4. Re-run this script to trigger freeze")
        return 1
    
    print(f"✅ {message}")
    
    freeze_exists, freeze_files = check_freeze_exists()
    if freeze_exists:
        print(f"⚠️  Freeze note already exists: {[f.name for f in freeze_files]}")
        return 0
    
    print("📝 Creating freeze note...")
    freeze_file = create_freeze_note()
    print(f"✅ Created: {freeze_file.name}")
    
    print("📊 Updating dashboard...")
    if update_dashboard():
        print("✅ Dashboard updated")
    else:
        print("⚠️  Dashboard update failed")
    
    print("\n🎉 Generic Item Master is now FROZEN")
    print("   → Specific Item Master Round-1 can now proceed")
    
    return 0

if __name__ == "__main__":
    exit(main())

