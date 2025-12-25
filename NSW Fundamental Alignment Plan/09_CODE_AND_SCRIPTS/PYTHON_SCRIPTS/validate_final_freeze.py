#!/usr/bin/env python3
"""
Validate Final Freeze Conditions

Purpose:
    Verifies that everything is frozen and signed before archiving.
    Confirms all governance gates were passed.

Usage:
    python3 scripts/governance/validate_final_freeze.py [--item Generic]
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DOCS_DIR = BASE_DIR / "docs" / "NEPL_STANDARDS" / "00_BASELINE_FREEZE"

def check_freeze_note(item_name):
    """Check if freeze note exists and is valid."""
    if "Generic" in item_name:
        pattern = "*GENERIC*FREEZE*.md"
    else:
        pattern = "*SPECIFIC*FREEZE*.md"
    
    freeze_files = list(DOCS_DIR.glob(pattern))
    if not freeze_files:
        return False, "No freeze note found"
    
    latest_freeze = max(freeze_files, key=os.path.getmtime)
    with open(latest_freeze, 'r') as f:
        content = f.read()
    
    if "🔒 FROZEN" in content or "FROZEN" in content.upper():
        return True, f"Freeze note valid: {latest_freeze.name}"
    
    return False, f"Freeze note exists but not confirmed: {latest_freeze.name}"

def check_signoff(item_name):
    """Check if signoff sheet exists and is completed."""
    item_slug = item_name.replace(" ", "_").lower()
    signoff_files = list(BASE_DIR.glob(f"{item_slug}_signoff*.csv"))
    signoff_files.extend(list(BASE_DIR.glob(f"{item_slug}_signoff*.md")))
    signoff_files.extend(list(DOCS_DIR.glob(f"*{item_slug}*signoff*.csv")))
    signoff_files.extend(list(DOCS_DIR.glob(f"*{item_slug}*signoff*.md")))
    
    if not signoff_files:
        return False, "No signoff sheet found"
    
    # Check if signoff is completed (has signatures)
    latest_signoff = max(signoff_files, key=os.path.getmtime)
    
    if latest_signoff.suffix == '.csv':
        import csv
        with open(latest_signoff, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            signed = sum(1 for row in rows if row.get('Signature', '').strip() or row.get('Reviewer Name', '').strip())
            if signed > 0:
                return True, f"Signoff sheet has {signed} signatures: {latest_signoff.name}"
    else:
        with open(latest_signoff, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for filled signatures (non-empty cells)
            if re.search(r'\| [^|]+\s+\| [^|]+\s+\| [^|]+\s+\|', content):
                return True, f"Signoff sheet appears completed: {latest_signoff.name}"
    
    return False, f"Signoff sheet exists but not completed: {latest_signoff.name}"

def check_rounds_complete(item_name):
    """Check if all required rounds are complete."""
    if "Generic" in item_name:
        required_rounds = ["R1", "R2"]
        r1_pattern = "*GENERIC*R1*.md"
        r2_pattern = "*GENERIC*R2*.md"
        r2_resume_pattern = "*GENERIC*R2*RESUME*.md"
    else:
        required_rounds = ["R0", "R1"]
        r1_pattern = "*SPECIFIC*R0*.md"
        r2_pattern = "*SPECIFIC*R1*.md"
        r2_resume_pattern = None
    
    r1_files = list(DOCS_DIR.glob(r1_pattern))
    r2_files = list(DOCS_DIR.glob(r2_pattern))
    r2_resume_files = list(DOCS_DIR.glob(r2_resume_pattern)) if r2_resume_pattern else []
    
    rounds_status = []
    
    if r1_files:
        with open(r1_files[0], 'r') as f:
            content = f.read()
            if "✅" in content or "PASS" in content.upper() or "COMPLETE" in content.upper():
                rounds_status.append(("Round-1", True))
            else:
                rounds_status.append(("Round-1", False))
    else:
        rounds_status.append(("Round-1", False))
    
    # For Generic R2, account for unusual workflow (pause → resume)
    if "Generic" in item_name and r2_resume_files:
        # Check if Round-2 was resumed (unusual workflow)
        latest_resume = max(r2_resume_files, key=os.path.getmtime)
        with open(latest_resume, 'r') as f:
            resume_content = f.read()
        
        # Check if resume indicates completion or just resumption
        if "can now proceed" in resume_content.lower() or "✅ COMPLETE" in resume_content:
            # Resume exists, but need to check actual verification
            if r2_files:
                # Check template or status file for actual completion
                r2_template_files = list(DOCS_DIR.glob("*GENERIC*R2*TEMPLATE*.md"))
                if r2_template_files:
                    latest_template = max(r2_template_files, key=os.path.getmtime)
                    with open(latest_template, 'r') as f:
                        template_content = f.read()
                    if "✅ PASS" in template_content or "APPROVED FOR FREEZE" in template_content:
                        rounds_status.append(("Round-2", True))
                    else:
                        rounds_status.append(("Round-2", False, "Resumed but verification pending"))
                else:
                    rounds_status.append(("Round-2", False, "Resumed but template not found"))
            else:
                rounds_status.append(("Round-2", False, "Resumed but no R2 files found"))
        else:
            rounds_status.append(("Round-2", False, "Resume note exists but not complete"))
    elif r2_files:
        with open(r2_files[0], 'r') as f:
            content = f.read()
            if "✅" in content or "PASS" in content.upper() or "COMPLETE" in content.upper():
                rounds_status.append(("Round-2", True))
            else:
                rounds_status.append(("Round-2", False))
    else:
        rounds_status.append(("Round-2", False))
    
    # Check if all rounds are complete (handle both 2-tuples and 3-tuples)
    all_complete = all(
        status for status in rounds_status 
        if isinstance(status, tuple) and len(status) >= 2 and status[1] is True
    )
    return all_complete, rounds_status

def validate_final_freeze(item_name):
    """Validate all final freeze conditions."""
    errors = []
    warnings = []
    
    print(f"🔍 Validating final freeze for {item_name}...\n")
    
    # Check freeze note
    is_frozen, freeze_msg = check_freeze_note(item_name)
    if is_frozen:
        print(f"✅ {freeze_msg}")
    else:
        errors.append(f"❌ {freeze_msg}")
    
    # Check signoff
    is_signed, signoff_msg = check_signoff(item_name)
    if is_signed:
        print(f"✅ {signoff_msg}")
    else:
        warnings.append(f"⚠️  {signoff_msg}")
    
    # Check rounds
    rounds_complete, rounds_status = check_rounds_complete(item_name)
    for round_info in rounds_status:
        if isinstance(round_info, tuple):
            if len(round_info) == 2:
                round_name, status = round_info
                if status:
                    print(f"✅ {round_name} complete")
                else:
                    errors.append(f"❌ {round_name} not complete")
            elif len(round_info) == 3:
                round_name, status, note = round_info
                if status:
                    print(f"✅ {round_name} complete")
                else:
                    errors.append(f"❌ {round_name} not complete: {note}")
    
    return errors, warnings

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Validate final freeze conditions')
    parser.add_argument('--item', '-i', default='Generic Item Master',
                       choices=['Generic Item Master', 'Specific Item Master'],
                       help='Item Master to validate')
    
    args = parser.parse_args()
    
    errors, warnings = validate_final_freeze(args.item)
    
    print("\n" + "="*60)
    
    if errors:
        print("\n❌ FINAL FREEZE VALIDATION FAILED")
        print("\nBlocking issues:")
        for error in errors:
            print(f"  {error}")
        
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  {warning}")
        
        print("\n⚠️  Cannot proceed with archival until all errors are resolved")
        return 1
    
    if warnings:
        print("\n⚠️  FINAL FREEZE VALIDATION PASSED WITH WARNINGS")
        print("\nWarnings:")
        for warning in warnings:
            print(f"  {warning}")
        print("\n✅ Can proceed with archival, but consider addressing warnings")
    else:
        print("\n✅ FINAL FREEZE VALIDATION PASSED")
        print("\nAll conditions met:")
        print("  ✓ Freeze note exists and confirmed")
        print("  ✓ Signoff sheet completed")
        print("  ✓ All required rounds complete")
        print("\n✅ Ready for artifact archival")
    
    return 0

if __name__ == "__main__":
    exit(main())

