#!/usr/bin/env python3
"""
LC1E Raw Pricelist Inspector

Purpose:
- Inspect raw Schneider pricelist XLSX to locate LC1E tables
- Print sheet names and search for LC1E occurrences
- Display surrounding rows for matches
"""

import argparse
import pandas as pd
import sys
from pathlib import Path

def inspect_pricelist(xlsx_file, max_rows=5000, context_rows=20, max_matches=5):
    """
    Inspect pricelist XLSX file for LC1E content.
    
    Args:
        xlsx_file: Path to XLSX file
        max_rows: Maximum rows to search per sheet
        context_rows: Number of surrounding rows to show
        max_matches: Maximum number of matches to display per sheet
    """
    print("=" * 80)
    print("LC1E Raw Pricelist Inspector")
    print("=" * 80)
    print()
    
    if not Path(xlsx_file).exists():
        print(f"✗ Error: File not found: {xlsx_file}")
        sys.exit(1)
    
    try:
        xls = pd.ExcelFile(xlsx_file)
        print(f"✓ Opened file: {xlsx_file}")
        print(f"✓ Total sheets: {len(xls.sheet_names)}")
        print(f"Sheet names: {xls.sheet_names}")
        print()
        
        # Search each sheet for LC1E
        total_matches = 0
        for sheet_name in xls.sheet_names:
            print("-" * 80)
            print(f"Sheet: {sheet_name}")
            print("-" * 80)
            
            try:
                # Read first max_rows rows
                df = pd.read_excel(xlsx_file, sheet_name=sheet_name, nrows=max_rows, header=None)
                print(f"  Rows read: {len(df)}")
                
                # Search for LC1E in all columns
                matches = []
                for idx in range(len(df)):
                    row_vals = df.iloc[idx].astype(str).fillna('')
                    row_str = ' '.join(row_vals.values)
                    
                    if 'LC1E' in row_str.upper():
                        matches.append(idx)
                        if len(matches) >= max_matches:
                            break
                
                if matches:
                    print(f"  ✓ Found {len(matches)} LC1E matches (showing first {min(len(matches), max_matches)})")
                    total_matches += len(matches)
                    
                    for i, match_idx in enumerate(matches[:max_matches], 1):
                        print()
                        print(f"  Match #{i} at row {match_idx + 1}:")
                        print("  " + "-" * 76)
                        
                        # Show surrounding rows
                        start_row = max(0, match_idx - context_rows // 2)
                        end_row = min(len(df), match_idx + context_rows // 2 + 1)
                        
                        # Display subset of columns (first 25 to avoid overflow)
                        subset_df = df.iloc[start_row:end_row, :25]
                        print(subset_df.to_string(index=False))
                        print()
                else:
                    print(f"  ⚠ No LC1E matches found in first {max_rows} rows")
                    
            except Exception as e:
                print(f"  ✗ Error reading sheet {sheet_name}: {e}")
                continue
        
        print()
        print("=" * 80)
        if total_matches > 0:
            print(f"✓ Total LC1E matches found: {total_matches}")
        else:
            print("⚠ No LC1E matches found in any sheet")
        print("=" * 80)
        
    except Exception as e:
        print(f"✗ Error opening file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Inspect raw LC1E pricelist XLSX')
    parser.add_argument('--input_xlsx', 
                       default='input/schneider/lc1e/Switching_All_WEF_15th_Jul_25.xlsx',
                       help='Input raw pricelist XLSX file')
    parser.add_argument('--max_rows', type=int, default=5000,
                       help='Maximum rows to search per sheet (default: 5000)')
    parser.add_argument('--context_rows', type=int, default=20,
                       help='Number of surrounding rows to show (default: 20)')
    parser.add_argument('--max_matches', type=int, default=5,
                       help='Maximum matches to display per sheet (default: 5)')
    
    args = parser.parse_args()
    
    inspect_pricelist(args.input_xlsx, args.max_rows, args.context_rows, args.max_matches)


if __name__ == '__main__':
    main()

