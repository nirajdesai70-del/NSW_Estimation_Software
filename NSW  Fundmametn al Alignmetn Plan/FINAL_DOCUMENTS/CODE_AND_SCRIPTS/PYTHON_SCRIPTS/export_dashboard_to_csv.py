#!/usr/bin/env python3
"""
Export Governance Dashboard to CSV

Purpose:
    Converts Markdown dashboard to CSV for audit/reporting.
    Can be imported into Excel or other reporting tools.

Usage:
    python3 scripts/governance/export_dashboard_to_csv.py [--output output.csv]
"""

import re
import csv
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DASHBOARD_FILE = BASE_DIR / "docs" / "DASHBOARD_REVIEW_STATUS.md"

def parse_dashboard_table(content):
    """Parse markdown table from dashboard."""
    lines = content.split('\n')
    table_data = []
    in_table = False
    
    for line in lines:
        # Detect table start
        if '| Item Master' in line and 'Round' in line:
            in_table = True
            headers = [h.strip() for h in line.split('|')[1:-1]]
            continue
        
        if in_table:
            # Skip separator line
            if '---' in line or '|-----' in line:
                continue
            
            # Parse data row
            if '|' in line:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if len(cells) == len(headers):
                    table_data.append(dict(zip(headers, cells)))
            else:
                # End of table
                break
    
    return headers, table_data

def export_to_csv(headers, data, output_file):
    """Export data to CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    return output_file

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Export governance dashboard to CSV')
    parser.add_argument('--output', '-o', 
                       default=f'governance_dashboard_{datetime.now().strftime("%Y%m%d")}.csv',
                       help='Output CSV file path')
    
    args = parser.parse_args()
    
    if not DASHBOARD_FILE.exists():
        print(f"❌ Dashboard not found at {DASHBOARD_FILE}")
        return 1
    
    print(f"📖 Reading dashboard from {DASHBOARD_FILE}...")
    with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📊 Parsing dashboard table...")
    headers, data = parse_dashboard_table(content)
    
    if not data:
        print("⚠️  No table data found in dashboard")
        return 1
    
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path
    
    print(f"💾 Exporting to {output_path}...")
    export_to_csv(headers, data, output_path)
    
    print(f"✅ Exported {len(data)} rows to {output_path}")
    print(f"\nColumns: {', '.join(headers)}")
    
    return 0

if __name__ == "__main__":
    exit(main())

