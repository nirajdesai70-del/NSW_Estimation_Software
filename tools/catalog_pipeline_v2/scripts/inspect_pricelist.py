#!/usr/bin/env python3
"""Quick script to inspect pricelist structure"""
import pandas as pd
import sys

xlsx_file = 'input/schneider/lc1e/Switching _All_WEF 15th Jul 25.xlsx'

try:
    xls = pd.ExcelFile(xlsx_file)
    print(f"Sheets: {xls.sheet_names}")
    print(f"\nTotal sheets: {len(xls.sheet_names)}")
    
    # Read first sheet
    df = pd.read_excel(xlsx_file, sheet_name='Table 1', nrows=100, header=None)
    print(f"\nShape: {df.shape}")
    
    # Search for LC1E
    print("\nSearching for LC1E...")
    for idx in range(min(100, len(df))):
        row_vals = df.iloc[idx].astype(str).fillna('')
        row_str = ' '.join(row_vals.values)
        if 'LC1E' in row_str.upper() and 'LC1E' in str(row_vals.values).upper():
            print(f"\nFound LC1E near row {idx}:")
            # Show surrounding rows
            start = max(0, idx - 2)
            end = min(len(df), idx + 10)
            print(df.iloc[start:end, :25].to_string())
            break
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()


