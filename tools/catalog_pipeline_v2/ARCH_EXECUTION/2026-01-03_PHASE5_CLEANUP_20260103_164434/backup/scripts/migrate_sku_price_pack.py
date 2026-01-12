#!/usr/bin/env python3
"""
Script A: Migrate SKU + Price + Ratings + Accessories

Purpose: Deterministic migration of SKU, Price, Ratings, and Accessories data
from legacy workbook structure to new freeze structure.

Input:
- Legacy workbook: NSW_MASTER_SCHNEIDER_WEF_2025-07-15_ENGINEER_REVIEW.xlsx
- Legacy sheets: NSW_L2_PRODUCTS, NSW_PRICE_MATRIX, ratings, accessories

Output:
- New workbook: NSW_SKU_PRICE_PACK_MASTER.xlsx
- New sheets: NSW_SKU_MASTER_CANONICAL, NSW_PRICE_MATRIX_CANONICAL, 
              NSW_SKU_RATINGS, NSW_ACCESSORY_SKU_MASTER

Status: Deterministic - No semantic changes, only column renaming
Aligned with: NSW_TERMINOLOGY_AND_LEVELS_FREEZE_v1.2_CLEAN.md

Phase 4 Fixes:
- Removed SC_Lx → capability_class_x auto-mapping (SC_Lx = SCL, not capability)
- Added generic naming validator (warnings only, non-blocking)
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime


def validate_generic_naming(df, sheet_name='UNKNOWN', generic_name_columns=None):
    """
    Validate generic names for vendor/series neutrality (read-only, warning-only).
    
    Per freeze v1.2: Generic names must NOT contain:
    - OEM names: Schneider, ABB, Siemens, etc.
    - Series: LC1E, GZ1E, NSX, NW, etc.
    - Family names
    
    Returns list of warnings (non-blocking, does NOT modify dataframe).
    
    Warning format: WARN GenericNaming: sheet=<name> row=<idx> col=<col> token=<token> value="<value>"
    """
    if generic_name_columns is None:
        generic_name_columns = ['l0_name', 'l1_name', 'generic_name', 'generic_description']
    
    warnings = []
    forbidden_oem = ['schneider', 'abb', 'siemens', 'legrand', 'hager', 'chint', 'eaton', 'ge']
    forbidden_series = ['lc1e', 'gz1e', 'nsx', 'nw', 'gv2', 'gv3', 'ic60', 'ic65', 'acti9']
    
    for col in generic_name_columns:
        if col not in df.columns:
            continue
        
        for idx, value in df[col].items():
            if pd.isna(value) or not isinstance(value, str):
                continue
            
            value_lower = value.lower()
            
            # Check for OEM names
            for oem in forbidden_oem:
                if oem in value_lower:
                    warnings.append(
                        f"WARN GenericNaming: sheet={sheet_name} row={idx} col={col} "
                        f"token={oem.upper()} value=\"{value}\""
                    )
            
            # Check for series names
            for series in forbidden_series:
                if series in value_lower:
                    warnings.append(
                        f"WARN GenericNaming: sheet={sheet_name} row={idx} col={col} "
                        f"token={series.upper()} value=\"{value}\""
                    )
    
    return warnings


def rename_columns_for_freeze(df, sheet_type='sku'):
    """
    Rename columns according to freeze terminology v1.2.
    
    Column mappings:
    - business_subcategory → business_segment (legacy alias supported during transition)
    
    IMPORTANT: SC_Lx columns are NOT renamed to capability_class_x.
    Per freeze v1.2: SC_Lx = SCL (Structural Construction Layers), not capability.
    SC_Lx columns are preserved as-is.
    """
    df = df.copy()
    
    # Business segment mapping (legacy alias support)
    if 'business_subcategory' in df.columns:
        df = df.rename(columns={'business_subcategory': 'business_segment'})
        print(f"  ✓ Renamed business_subcategory → business_segment (legacy alias)")
    
    # SC_Lx columns are preserved as-is (SCL, not capability_class)
    # Do NOT auto-map SC_Lx to capability_class_x
    
    return df


def migrate_sku_master(legacy_workbook_path, output_writer):
    """
    Migrate NSW_L2_PRODUCTS → NSW_SKU_MASTER_CANONICAL
    
    Note: NSW_L2_PRODUCTS is legacy parse/compat output.
    NSW_SKU_MASTER_CANONICAL is the authoritative SKU list.
    """
    print("\n📦 Migrating SKU Master...")
    
    try:
        # Read legacy sheet
        legacy_l2 = pd.read_excel(legacy_workbook_path, sheet_name='NSW_L2_PRODUCTS')
        print(f"  ✓ Read NSW_L2_PRODUCTS: {len(legacy_l2)} rows")
        
        # Rename columns for freeze terminology
        sku_master = rename_columns_for_freeze(legacy_l2, sheet_type='sku')
        
        # Validate generic naming (warnings only, non-blocking)
        naming_warnings = validate_generic_naming(sku_master, sheet_name='NSW_SKU_MASTER_CANONICAL')
        if naming_warnings:
            print(f"  ⚠️  Generic Naming Warnings ({len(naming_warnings)}):")
            for warning in naming_warnings[:10]:  # Show first 10
                print(f"    - {warning}")
            if len(naming_warnings) > 10:
                print(f"    ... and {len(naming_warnings) - 10} more warnings")
        
        # Ensure required columns exist
        required_cols = ['make', 'series_bucket', 'item_producttype', 'l2_product_code']
        for col in required_cols:
            if col not in sku_master.columns:
                print(f"  ⚠️  Warning: Missing column '{col}', adding with default value")
                sku_master[col] = ''
        
        # Write to new sheet
        sku_master.to_excel(output_writer, sheet_name='NSW_SKU_MASTER_CANONICAL', index=False)
        print(f"  ✓ Wrote NSW_SKU_MASTER_CANONICAL: {len(sku_master)} rows")
        
        return sku_master
        
    except Exception as e:
        print(f"  ✗ Error migrating SKU master: {e}")
        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=['make', 'series_bucket', 'item_producttype', 
                                     'business_segment', 'l2_product_code', 'status'])


def migrate_price_matrix(legacy_workbook_path, output_writer):
    """
    Migrate NSW_PRICE_MATRIX → NSW_PRICE_MATRIX_CANONICAL
    
    Same structure, just copy with sheet rename.
    """
    print("\n💰 Migrating Price Matrix...")
    
    try:
        # Read legacy sheet
        legacy_price = pd.read_excel(legacy_workbook_path, sheet_name='NSW_PRICE_MATRIX')
        print(f"  ✓ Read NSW_PRICE_MATRIX: {len(legacy_price)} rows")
        
        # Copy as-is (same structure)
        price_matrix = legacy_price.copy()
        
        # Write to new sheet
        price_matrix.to_excel(output_writer, sheet_name='NSW_PRICE_MATRIX_CANONICAL', index=False)
        print(f"  ✓ Wrote NSW_PRICE_MATRIX_CANONICAL: {len(price_matrix)} rows")
        
        return price_matrix
        
    except Exception as e:
        print(f"  ✗ Error migrating price matrix: {e}")
        return pd.DataFrame()


def migrate_sku_ratings(legacy_workbook_path, output_writer):
    """
    Migrate ratings data → NSW_SKU_RATINGS
    
    Look for ratings sheet in legacy workbook.
    """
    print("\n📊 Migrating SKU Ratings...")
    
    try:
        # Try to find ratings sheet (may have different names)
        xls = pd.ExcelFile(legacy_workbook_path)
        ratings_sheet = None
        
        for sheet_name in xls.sheet_names:
            if 'rating' in sheet_name.lower() or 'RATING' in sheet_name:
                ratings_sheet = sheet_name
                break
        
        if ratings_sheet:
            ratings = pd.read_excel(legacy_workbook_path, sheet_name=ratings_sheet)
            print(f"  ✓ Read {ratings_sheet}: {len(ratings)} rows")
            
            # Rename columns if needed
            ratings = rename_columns_for_freeze(ratings, sheet_type='ratings')
            
            # Validate generic naming (warnings only)
            naming_warnings = validate_generic_naming(ratings, sheet_name='NSW_SKU_RATINGS')
            if naming_warnings:
                print(f"  ⚠️  Generic Naming Warnings in ratings ({len(naming_warnings)}):")
                for warning in naming_warnings[:5]:
                    print(f"    - {warning}")
            
            ratings.to_excel(output_writer, sheet_name='NSW_SKU_RATINGS', index=False)
            print(f"  ✓ Wrote NSW_SKU_RATINGS: {len(ratings)} rows")
            return ratings
        else:
            print(f"  ⚠️  No ratings sheet found, creating empty structure")
            return pd.DataFrame(columns=['l2_product_code', 'rating_type', 'rating_value', 'rating_unit'])
            
    except Exception as e:
        print(f"  ✗ Error migrating ratings: {e}")
        return pd.DataFrame()


def migrate_accessory_skus(legacy_workbook_path, output_writer):
    """
    Migrate accessory SKU data → NSW_ACCESSORY_SKU_MASTER
    
    Look for accessory sheet in legacy workbook.
    """
    print("\n🔧 Migrating Accessory SKUs...")
    
    try:
        # Try to find accessory sheet
        xls = pd.ExcelFile(legacy_workbook_path)
        accessory_sheet = None
        
        for sheet_name in xls.sheet_names:
            if 'accessory' in sheet_name.lower() or 'ACCESSORY' in sheet_name:
                accessory_sheet = sheet_name
                break
        
        if accessory_sheet:
            accessories = pd.read_excel(legacy_workbook_path, sheet_name=accessory_sheet)
            print(f"  ✓ Read {accessory_sheet}: {len(accessories)} rows")
            
            # Rename columns if needed
            accessories = rename_columns_for_freeze(accessories, sheet_type='accessory')
            
            # Validate generic naming (warnings only)
            naming_warnings = validate_generic_naming(accessories, sheet_name='NSW_ACCESSORY_SKU_MASTER')
            if naming_warnings:
                print(f"  ⚠️  Generic Naming Warnings in accessories ({len(naming_warnings)}):")
                for warning in naming_warnings[:5]:
                    print(f"    - {warning}")
            
            accessories.to_excel(output_writer, sheet_name='NSW_ACCESSORY_SKU_MASTER', index=False)
            print(f"  ✓ Wrote NSW_ACCESSORY_SKU_MASTER: {len(accessories)} rows")
            return accessories
        else:
            print(f"  ⚠️  No accessory sheet found, creating empty structure")
            return pd.DataFrame(columns=['accessory_sku', 'item_producttype', 'business_segment', 
                                         'capability_class_4', 'price', 'status'])
            
    except Exception as e:
        print(f"  ✗ Error migrating accessories: {e}")
        return pd.DataFrame()


def validate_migration(sku_master, price_matrix, ratings, accessories):
    """
    Validate migration - check row counts and data integrity.
    """
    print("\n✅ Validating Migration...")
    
    issues = []
    
    # Check SKU master
    if len(sku_master) == 0:
        issues.append("SKU Master is empty")
    else:
        required_cols = ['make', 'l2_product_code']
        for col in required_cols:
            if col not in sku_master.columns:
                issues.append(f"SKU Master missing required column: {col}")
    
    # Check price matrix
    if len(price_matrix) == 0:
        issues.append("Price Matrix is empty")
    
    # Check for data loss (basic check)
    if len(sku_master) > 0 and len(price_matrix) > 0:
        # Check if SKU codes in price matrix exist in SKU master
        if 'l2_product_code' in price_matrix.columns and 'l2_product_code' in sku_master.columns:
            price_skus = set(price_matrix['l2_product_code'].dropna().unique())
            master_skus = set(sku_master['l2_product_code'].dropna().unique())
            orphan_prices = price_skus - master_skus
            if orphan_prices:
                issues.append(f"Price matrix contains {len(orphan_prices)} SKUs not in master")
    
    if issues:
        print("  ⚠️  Validation Issues Found:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print("  ✓ Validation passed")
        return True


def main():
    parser = argparse.ArgumentParser(description='Migrate SKU + Price + Ratings + Accessories (Script A)')
    parser.add_argument('--legacy_workbook', required=True, help='Path to legacy workbook')
    parser.add_argument('--output', required=True, help='Path to output master workbook')
    parser.add_argument('--validate', action='store_true', help='Run validation after migration')
    
    args = parser.parse_args()
    
    legacy_path = Path(args.legacy_workbook)
    output_path = Path(args.output)
    
    if not legacy_path.exists():
        print(f"✗ Error: Legacy workbook not found: {legacy_path}")
        sys.exit(1)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Script A: Migrate SKU + Price + Ratings + Accessories")
    print("=" * 60)
    print(f"Legacy workbook: {legacy_path}")
    print(f"Output workbook: {output_path}")
    print()
    
    # Create output workbook
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Migrate each component
        sku_master = migrate_sku_master(legacy_path, writer)
        price_matrix = migrate_price_matrix(legacy_path, writer)
        ratings = migrate_sku_ratings(legacy_path, writer)
        accessories = migrate_accessory_skus(legacy_path, writer)
        
        # Validate if requested
        if args.validate:
            validation_passed = validate_migration(sku_master, price_matrix, ratings, accessories)
            if not validation_passed:
                print("\n⚠️  Validation issues found. Review output before proceeding.")
    
    print("\n" + "=" * 60)
    print("✓ Migration Complete")
    print(f"  Output: {output_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()


