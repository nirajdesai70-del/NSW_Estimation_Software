#!/usr/bin/env python3
"""
Generate Signoff Sheet for Governance Items

Purpose:
    Creates a signoff template (CSV/Markdown) per item with reviewer,
    timestamp, and digital signature space.

Usage:
    python3 scripts/governance/generate_signoff_sheet.py [--item Generic] [--format csv|md]
"""

import csv
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent

# Default reviewers
DEFAULT_REVIEWERS = [
    "Governance Lead",
    "Project Owner",
    "Compliance Officer",
]

def generate_csv_signoff(item_name, output_file):
    """Generate CSV signoff sheet."""
    fieldnames = [
        "Item Master",
        "Round",
        "Reviewer Role",
        "Reviewer Name",
        "Signature",
        "Date",
        "Notes"
    ]
    
    rounds = ["Round-1", "Round-2", "Freeze"]
    if "Specific" in item_name:
        rounds = ["Round-0", "Round-1", "Freeze"]
    
    rows = []
    for round_name in rounds:
        for reviewer_role in DEFAULT_REVIEWERS:
            rows.append({
                "Item Master": item_name,
                "Round": round_name,
                "Reviewer Role": reviewer_role,
                "Reviewer Name": "",
                "Signature": "",
                "Date": "",
                "Notes": ""
            })
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return output_file

def generate_markdown_signoff(item_name, output_file):
    """Generate Markdown signoff sheet."""
    rounds = ["Round-1", "Round-2", "Freeze"]
    if "Specific" in item_name:
        rounds = ["Round-0", "Round-1", "Freeze"]
    
    content = f"""# {item_name} — Digital Signoff Sheet
**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Purpose:** Formal approval tracking for governance compliance

---

## Signoff Requirements

Each round requires approval from:
- Governance Lead
- Project Owner
- Compliance Officer

---

## Signoff Table

| Round | Reviewer Role | Reviewer Name | Signature | Date | Notes |
|-------|---------------|---------------|-----------|------|-------|
"""
    
    for round_name in rounds:
        for reviewer_role in DEFAULT_REVIEWERS:
            content += f"| {round_name} | {reviewer_role} | | | | |\n"
        content += "| | | | | | |\n"  # Spacer row
    
    content += f"""
---

## Instructions

1. **Reviewer Name:** Full name of the person signing off
2. **Signature:** Digital signature or initials
3. **Date:** Date of signoff (YYYY-MM-DD)
4. **Notes:** Any additional comments or conditions

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| v1.0 | {datetime.now().strftime("%Y-%m-%d")} | Initial signoff sheet created |

---

**END OF DOCUMENT**
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Generate signoff sheet')
    parser.add_argument('--item', '-i', default='Generic Item Master',
                       choices=['Generic Item Master', 'Specific Item Master'],
                       help='Item Master to generate signoff for')
    parser.add_argument('--format', '-f', default='csv',
                       choices=['csv', 'md'],
                       help='Output format (default: csv)')
    parser.add_argument('--output', '-o',
                       help='Output file path')
    
    args = parser.parse_args()
    
    today = datetime.now().strftime("%Y%m%d")
    item_slug = args.item.replace(" ", "_").lower()
    
    if args.output:
        output_path = Path(args.output)
    else:
        if args.format == 'csv':
            output_path = BASE_DIR / f"{item_slug}_signoff_{today}.csv"
        else:
            output_path = BASE_DIR / f"{item_slug}_signoff_{today}.md"
    
    print(f"📝 Generating {args.format.upper()} signoff sheet for {args.item}...")
    
    if args.format == 'csv':
        generate_csv_signoff(args.item, output_path)
    else:
        generate_markdown_signoff(args.item, output_path)
    
    print(f"✅ Signoff sheet created: {output_path}")
    print(f"\nNext steps:")
    print(f"  1. Distribute to reviewers")
    print(f"  2. Collect signatures")
    print(f"  3. Store completed sheet in governance docs")
    
    return 0

if __name__ == "__main__":
    exit(main())

