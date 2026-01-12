#!/usr/bin/env python3
"""
NSW Phase-5 Catalog Pipeline v2 - Script C
Build Master Engineer Review Workbook

Purpose:
- Combines L2 SKU Master, L2 Price History, L1 Lines, and L1 Attributes KVU
- Creates final Engineer Review workbook with all sheets
- Output: NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx (or custom name)
"""

import argparse
import pandas as pd
import sys
from pathlib import Path


def read_l2_data(l2_file):
    """Read L2 SKU Master, Price History, and RATING_MAP from Excel file."""
    try:
        l2_sku_master = pd.read_excel(l2_file, sheet_name='L2_SKU_MASTER')
        l2_price_history = pd.read_excel(l2_file, sheet_name='L2_PRICE_HISTORY')
        
        # Try to read RATING_MAP (may not exist in older outputs)
        try:
            rating_map = pd.read_excel(l2_file, sheet_name='RATING_MAP')
        except:
            rating_map = pd.DataFrame()
        
        print(f"✓ Read L2 data:")
        print(f"  - L2_SKU_MASTER: {len(l2_sku_master)} rows")
        print(f"  - L2_PRICE_HISTORY: {len(l2_price_history)} rows")
        print(f"  - RATING_MAP: {len(rating_map)} rows")
        return l2_sku_master, l2_price_history, rating_map
    except Exception as e:
        print(f"✗ Error reading L2 file: {e}")
        sys.exit(1)


def read_l1_data(l1_file):
    """Read L1 Lines and Attributes KVU from Excel file."""
    try:
        l1_lines = pd.read_excel(l1_file, sheet_name='L1_LINES')
        l1_attributes_kvu = pd.read_excel(l1_file, sheet_name='L1_ATTRIBUTES_KVU')
        print(f"✓ Read L1 data:")
        print(f"  - L1_LINES: {len(l1_lines)} rows")
        print(f"  - L1_ATTRIBUTES_KVU: {len(l1_attributes_kvu)} rows")
        return l1_lines, l1_attributes_kvu
    except Exception as e:
        print(f"✗ Error reading L1 file: {e}")
        sys.exit(1)


def validate_data(l2_sku_master, l2_price_history, l1_lines, l1_attributes_kvu, rating_map):
    """Validate data consistency between L2 and L1."""
    errors = []
    warnings = []
    
    # Check that all L2 SKUs referenced in L1 exist in L2_SKU_MASTER
    l1_skus = set(l1_lines['L2_OEM_Catalog_No'].dropna().unique())
    l2_skus = set(l2_sku_master['OEM_Catalog_No'].unique())
    
    missing_skus = l1_skus - l2_skus
    if missing_skus:
        errors.append(f"L1 references {len(missing_skus)} SKUs not in L2_SKU_MASTER: {list(missing_skus)[:5]}...")
    
    # Check that all L1 IDs in attributes exist in L1_LINES
    l1_ids = set(l1_lines['L1_Id'].unique())
    attr_l1_ids = set(l1_attributes_kvu['L1_Id'].dropna().unique())
    
    orphan_attrs = attr_l1_ids - l1_ids
    if orphan_attrs:
        warnings.append(f"L1_ATTRIBUTES_KVU contains {len(orphan_attrs)} L1 IDs not in L1_LINES")
    
    # Check price history SKU references
    price_skus = set(l2_price_history['OEM_Catalog_No'].dropna().unique())
    orphan_prices = price_skus - l2_skus
    if orphan_prices:
        warnings.append(f"L2_PRICE_HISTORY contains {len(orphan_prices)} SKUs not in L2_SKU_MASTER")
    
    if errors:
        print("\n✗ Validation Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print("\n⚠ Validation Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    return True


def build_master_workbook(l2_sku_master, l2_price_history, rating_map, l1_lines, l1_attributes_kvu, output_path):
    """Build final Engineer Review workbook with all sheets."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\nBuilding master workbook...")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Sheet 1: L2_SKU_MASTER
        l2_sku_master.to_excel(writer, sheet_name='L2_SKU_MASTER', index=False)
        print(f"  ✓ Added sheet: L2_SKU_MASTER ({len(l2_sku_master)} rows)")
        
        # Sheet 2: L2_PRICE_HISTORY
        l2_price_history.to_excel(writer, sheet_name='L2_PRICE_HISTORY', index=False)
        print(f"  ✓ Added sheet: L2_PRICE_HISTORY ({len(l2_price_history)} rows)")
        
        # Sheet 3: L1_LINES
        l1_lines.to_excel(writer, sheet_name='L1_LINES', index=False)
        
        # Count BASE vs FEATURE lines
        base_count = len(l1_lines[l1_lines['L1_Line_Type'] == 'BASE']) if 'L1_Line_Type' in l1_lines.columns else len(l1_lines)
        feature_count = len(l1_lines[l1_lines['L1_Line_Type'] == 'FEATURE']) if 'L1_Line_Type' in l1_lines.columns else 0
        print(f"  ✓ Added sheet: L1_LINES ({len(l1_lines)} rows: {base_count} BASE, {feature_count} FEATURE)")
        
        # Sheet 4: L1_ATTRIBUTES_KVU
        l1_attributes_kvu.to_excel(writer, sheet_name='L1_ATTRIBUTES_KVU', index=False)
        print(f"  ✓ Added sheet: L1_ATTRIBUTES_KVU ({len(l1_attributes_kvu)} rows)")
        
        # Sheet 5: RATING_MAP
        if len(rating_map) > 0:
            rating_map.to_excel(writer, sheet_name='RATING_MAP', index=False)
            print(f"  ✓ Added sheet: RATING_MAP ({len(rating_map)} rows)")
        else:
            # Create empty RATING_MAP with correct structure
            empty_rating_map = pd.DataFrame(columns=[
                'Base_Ref', 'DutyClass', 'Current_A', 'kW', 'HP', 'Poles', 'Aux_Contacts', 'SourcePageOrTableId', 'SourceRow'
            ])
            empty_rating_map.to_excel(writer, sheet_name='RATING_MAP', index=False)
            print(f"  ✓ Added sheet: RATING_MAP (empty)")
    
    print(f"\n✓ Master workbook written to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Build Master Engineer Review Workbook')
    parser.add_argument('--l2', required=True, help='Input L2 Excel file (from script A)')
    parser.add_argument('--l1', required=True, help='Input L1 Excel file (from script B)')
    parser.add_argument('--out', required=True, help='Output Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NSW Phase-5 Catalog Pipeline v2 - Script C")
    print("Build Master Engineer Review Workbook")
    print("=" * 60)
    
    # Read L2 data (including RATING_MAP)
    l2_sku_master, l2_price_history, rating_map = read_l2_data(args.l2)
    
    # Read L1 data
    l1_lines, l1_attributes_kvu = read_l1_data(args.l1)
    
    # Validate data
    if not validate_data(l2_sku_master, l2_price_history, l1_lines, l1_attributes_kvu, rating_map):
        print("\n✗ Validation failed. Please fix errors before building workbook.")
        sys.exit(1)
    
    # Build master workbook
    output_path = build_master_workbook(
        l2_sku_master, l2_price_history, rating_map, l1_lines, l1_attributes_kvu, args.out
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Output file: {output_path}")
    print(f"\nSheets created:")
    print(f"  1. L2_SKU_MASTER: {len(l2_sku_master)} distinct SKUs")
    print(f"  2. L2_PRICE_HISTORY: {len(l2_price_history)} price rows")
    
    base_count = len(l1_lines[l1_lines['L1_Line_Type'] == 'BASE']) if 'L1_Line_Type' in l1_lines.columns else len(l1_lines)
    feature_count = len(l1_lines[l1_lines['L1_Line_Type'] == 'FEATURE']) if 'L1_Line_Type' in l1_lines.columns else 0
    print(f"  3. L1_LINES: {len(l1_lines)} lines ({base_count} BASE, {feature_count} FEATURE)")
    print(f"  4. L1_ATTRIBUTES_KVU: {len(l1_attributes_kvu)} attribute rows")
    print(f"  5. RATING_MAP: {len(rating_map)} rating rows")
    print("\n" + "=" * 60)
    print("✓ Engineer Review workbook ready for review")
    print("=" * 60)


if __name__ == '__main__':
    main()

