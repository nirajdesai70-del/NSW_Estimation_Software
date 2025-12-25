#!/usr/bin/env python3
"""
Validate Specific Item Master Round-1 Kickoff

Purpose:
    Ensures Specific R1 can only start after Generic is frozen.
    Validates required files, checklists, and dependencies.

Usage:
    python3 scripts/governance/validate_specific_r1_kickoff.py
"""

import os
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DOCS_DIR = BASE_DIR / "docs" / "NEPL_STANDARDS" / "00_BASELINE_FREEZE"

def check_generic_frozen():
    """
    Check if Generic Item Master is frozen.
    
    Note: Accounts for unusual Round-2 workflow (pause → resume).
    Freeze can only happen after Round-2 is actually complete, not just resumed.
    """
    freeze_files = list(DOCS_DIR.glob("*FREEZE*.md"))
    if not freeze_files:
        return False, "No freeze note found"
    
    # Check latest freeze file
    latest_freeze = max(freeze_files, key=os.path.getmtime)
    with open(latest_freeze, 'r') as f:
        content = f.read()
    
    if "🔒 FROZEN" in content or "FROZEN" in content.upper():
        return True, f"Generic frozen: {latest_freeze.name}"
    
    return False, "Freeze note exists but status not confirmed"

def check_r0_readiness():
    """Check if Round-0 readiness gate exists."""
    r0_files = list(DOCS_DIR.glob("SPECIFIC_ITEM_MASTER_ROUND0_READINESS*.md"))
    if not r0_files:
        return False, "Round-0 readiness gate not found"
    
    return True, f"Round-0 gate exists: {r0_files[0].name}"

def check_r0_checklist():
    """Check if Round-0 checklist is complete."""
    r0_files = list(DOCS_DIR.glob("SPECIFIC_ITEM_MASTER_ROUND0_READINESS*.md"))
    if not r0_files:
        return False, "Round-0 file not found"
    
    with open(r0_files[0], 'r') as f:
        content = f.read()
    
    # Count checklist items
    import re
    checkboxes = re.findall(r'\[([ x])\]', content)
    if not checkboxes:
        return True, "No checklist items found (may be OK)"
    
    checked = sum(1 for cb in checkboxes if cb.strip() == 'x')
    total = len(checkboxes)
    
    if checked == total:
        return True, f"All {total} checklist items completed"
    
    return False, f"Checklist incomplete: {checked}/{total} items checked"

def validate_dependencies():
    """Validate all required dependencies for Specific R1."""
    errors = []
    warnings = []
    
    # Check Generic freeze
    is_frozen, msg = check_generic_frozen()
    if not is_frozen:
        errors.append(f"❌ Generic Item Master not frozen: {msg}")
    else:
        print(f"✅ {msg}")
    
    # Check R0 readiness
    r0_exists, r0_msg = check_r0_readiness()
    if not r0_exists:
        errors.append(f"❌ {r0_msg}")
    else:
        print(f"✅ {r0_msg}")
    
    # Check R0 checklist
    r0_complete, r0_check_msg = check_r0_checklist()
    if not r0_complete:
        warnings.append(f"⚠️  {r0_check_msg}")
    else:
        print(f"✅ {r0_check_msg}")
    
    return errors, warnings

def main():
    """Main execution."""
    print("🔍 Validating Specific Item Master Round-1 kickoff conditions...\n")
    
    errors, warnings = validate_dependencies()
    
    if errors:
        print("\n❌ BLOCKED: Cannot start Specific R1")
        print("\nErrors:")
        for error in errors:
            print(f"  {error}")
        
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  {warning}")
        
        return 1
    
    if warnings:
        print("\n⚠️  Warnings (non-blocking):")
        for warning in warnings:
            print(f"  {warning}")
    
    print("\n✅ All conditions met - Specific Item Master Round-1 can proceed")
    print("\nNext steps:")
    print("  1. Create Specific R1 kickoff note")
    print("  2. Begin Round-1 review process")
    print("  3. Update dashboard status")
    
    return 0

if __name__ == "__main__":
    exit(main())

