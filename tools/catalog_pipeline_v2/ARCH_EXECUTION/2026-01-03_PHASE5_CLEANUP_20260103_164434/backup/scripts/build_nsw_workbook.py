#!/usr/bin/env python3
"""
NSW Phase-5 Catalog Pipeline v2 - Build NSW Format Workbook

Purpose:
- Builds NSW format workbook from canonical + intermediate files
- Creates NSW_L2_PRODUCTS, NSW_L1_CONFIG_LINES, NSW_VARIANT_MASTER, etc.
- Output: NSW_<SERIES>_WEF_<DATE>_vX.xlsx (canonical freeze artifact)

This is the PRIMARY freeze artifact (not the engineer review workbook).
"""

import argparse
import pandas as pd
import sys
from pathlib import Path


def read_canonical_data(canonical_file):
    """Read canonical tables from extraction output."""
    try:
        # Try to read canonical sheets (series-specific names)
        canonical_rows = None
        coil_prices = None
        accessories = None
        
        xls = pd.ExcelFile(canonical_file)
        sheet_names = xls.sheet_names
        
        # Find canonical sheets (pattern: <SERIES>_CANONICAL_ROWS, <SERIES>_COIL_CODE_PRICES, etc.)
        for sheet in sheet_names:
            if 'CANONICAL_ROWS' in sheet.upper() or 'CANONICAL' in sheet.upper():
                canonical_rows = pd.read_excel(canonical_file, sheet_name=sheet)
            elif 'COIL' in sheet.upper() and 'PRICE' in sheet.upper():
                coil_prices = pd.read_excel(canonical_file, sheet_name=sheet)
            elif 'ACCESSORY' in sheet.upper():
                accessories = pd.read_excel(canonical_file, sheet_name=sheet)
        
        if canonical_rows is None:
            raise ValueError("Could not find canonical rows sheet")
        if coil_prices is None:
            raise ValueError("Could not find coil prices sheet")
        
        print(f"✓ Read canonical data:")
        print(f"  - Canonical rows: {len(canonical_rows)} rows")
        print(f"  - Coil prices: {len(coil_prices)} rows")
        if accessories is not None:
            print(f"  - Accessories: {len(accessories)} rows")
        else:
            print(f"  - Accessories: not detected")
        
        return canonical_rows, coil_prices, accessories
    except Exception as e:
        print(f"✗ Error reading canonical file: {e}")
        sys.exit(1)


def read_intermediate_data(l2_file, l1_file):
    """Read intermediate L2 and L1 data (if available)."""
    l2_data = None
    l1_data = None
    
    try:
        # Try to read L2_SKU_MASTER (old format) or NSW_L2_PRODUCTS (new format)
        xls_l2 = pd.ExcelFile(l2_file)
        if 'NSW_L2_PRODUCTS' in xls_l2.sheet_names:
            l2_data = pd.read_excel(l2_file, sheet_name='NSW_L2_PRODUCTS')
        elif 'L2_SKU_MASTER' in xls_l2.sheet_names:
            l2_data = pd.read_excel(l2_file, sheet_name='L2_SKU_MASTER')
            print("  ⚠️  L2 file uses old format (L2_SKU_MASTER), will need transformation")
    except:
        print("  ⚠️  Could not read L2 file, will build from canonical only")
    
    try:
        # Try to read L1_LINES (old format) or NSW_L1_CONFIG_LINES (new format)
        xls_l1 = pd.ExcelFile(l1_file)
        if 'NSW_L1_CONFIG_LINES' in xls_l1.sheet_names:
            l1_data = pd.read_excel(l1_file, sheet_name='NSW_L1_CONFIG_LINES')
        elif 'L1_LINES' in xls_l1.sheet_names:
            l1_data = pd.read_excel(l1_file, sheet_name='L1_LINES')
            print("  ⚠️  L1 file uses old format (L1_LINES), will need transformation")
    except:
        print("  ⚠️  Could not read L1 file, will build from canonical only")
    
    return l2_data, l1_data


def build_nsw_l2_products(canonical_rows):
    """
    Build NSW_L2_PRODUCTS from canonical rows.
    
    NSW_L2_PRODUCTS contains:
    - make, series_name, series_bucket
    - item_producttype, business_subcategory
    - poles, frame_label
    - l2_product_code (base ref, no voltage/duty)
    - generic_name
    - status
    """
    # Extract base reference (strip voltage/duty codes)
    # This is series-specific logic - placeholder for now
    # TODO: Implement series-specific extraction based on canonical structure
    
    nsw_l2 = pd.DataFrame()
    
    # Placeholder: This should extract from canonical_rows based on series structure
    # For now, return empty with correct structure
    nsw_l2 = pd.DataFrame(columns=[
        'make', 'series_name', 'series_bucket', 'item_producttype',
        'business_subcategory', 'poles', 'frame_label', 'l2_product_code',
        'generic_name', 'status'
    ])
    
    print("  ⚠️  NSW_L2_PRODUCTS building not yet implemented - requires series-specific logic")
    return nsw_l2


def build_nsw_variant_master(coil_prices):
    """
    Build NSW_VARIANT_MASTER from coil prices.
    
    NSW_VARIANT_MASTER contains:
    - variant_type (usually 'COIL_VOLTAGE')
    - variant_code (M7, N5, M5, N7, etc.)
    - voltage_V, voltage_type (AC/DC)
    - display_label (e.g., 'N5 (415V AC)')
    """
    # Extract unique variants from coil prices
    # This is series-specific logic - placeholder for now
    # TODO: Implement variant extraction based on coil price structure
    
    variants = pd.DataFrame(columns=[
        'variant_type', 'variant_code', 'voltage_V', 'voltage_type', 'display_label'
    ])
    
    print("  ⚠️  NSW_VARIANT_MASTER building not yet implemented - requires series-specific logic")
    return variants


def build_nsw_price_matrix(coil_prices, l2_product_codes):
    """
    Build NSW_PRICE_MATRIX from coil prices.
    
    NSW_PRICE_MATRIX contains:
    - l2_product_code
    - variant_type, variant_code
    - voltage_V
    - rate_inr
    - effective_from
    """
    # Extract prices by variant
    # This is series-specific logic - placeholder for now
    # TODO: Implement price matrix extraction
    
    price_matrix = pd.DataFrame(columns=[
        'l2_product_code', 'variant_type', 'variant_code', 'voltage_V',
        'rate_inr', 'effective_from'
    ])
    
    print("  ⚠️  NSW_PRICE_MATRIX building not yet implemented - requires series-specific logic")
    return price_matrix


def build_nsw_l1_config_lines(canonical_rows, coil_prices, nsw_l2, price_matrix):
    """
    Build NSW_L1_CONFIG_LINES from canonical + L2 + price matrix.
    
    NSW_L1_CONFIG_LINES contains:
    - l1_seq_no, l1_group_id, l1_id, l1_line_type
    - l2_product_code
    - duty_class, duty_current_A, catalog_ac1_A, catalog_ac3_A
    - voltage_class_code, selected_voltage_V, selected_voltage_type, catalog_voltage_label
    - motor_kw, motor_hp, poles, frame_label, aux_no, aux_nc
    - generic_descriptor
    - resolved_price_inr (filled at quote time)
    - catalog_trace_ref
    """
    # Build L1 lines as duty × voltage combinations
    # This is series-specific logic - placeholder for now
    # TODO: Implement L1 expansion logic
    
    l1_lines = pd.DataFrame(columns=[
        'l1_seq_no', 'series_name', 'generic_descriptor', 'l1_group_id', 'l1_id',
        'l1_line_type', 'l2_product_code', 'poles', 'no_of_poles', 'frame_label',
        'variant_code', 'voltage_class_code', 'voltage_type', 'selected_voltage_type',
        'voltage_V', 'selected_voltage_V', 'catalog_voltage_label', 'duty_class',
        'duty_current_A', 'catalog_ac1_A', 'catalog_ac3_A', 'motor_kw', 'motor_hp',
        'aux_no', 'aux_nc', 'resolved_price_inr', 'catalog_trace_ref', 'status'
    ])
    
    print("  ⚠️  NSW_L1_CONFIG_LINES building not yet implemented - requires series-specific logic")
    return l1_lines


def build_nsw_workbook(canonical_file, l2_file, l1_file, output_path, series_name, wef_date):
    """
    Build NSW format workbook from canonical + intermediate files.
    
    This creates the PRIMARY freeze artifact with NSW format sheets.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\nBuilding NSW format workbook...")
    print(f"  Series: {series_name}")
    print(f"  WEF: {wef_date}")
    
    # Read canonical data
    canonical_rows, coil_prices, accessories = read_canonical_data(canonical_file)
    
    # Read intermediate data (if available)
    l2_intermediate, l1_intermediate = read_intermediate_data(l2_file, l1_file)
    
    # Build NSW sheets
    nsw_l2 = build_nsw_l2_products(canonical_rows)
    nsw_variants = build_nsw_variant_master(coil_prices)
    nsw_price_matrix = build_nsw_price_matrix(coil_prices, nsw_l2['l2_product_code'].tolist() if len(nsw_l2) > 0 else [])
    nsw_l1 = build_nsw_l1_config_lines(canonical_rows, coil_prices, nsw_l2, nsw_price_matrix)
    
    # Build L0 sheets (optional, can be empty)
    nsw_l0_template = pd.DataFrame(columns=['l0_template_id', 'l0_intent_name', 'description', 'status'])
    nsw_l0_eligibility = pd.DataFrame(columns=['l0_template_id', 'l2_product_code', 'status'])
    
    # Build product-variant mapping
    nsw_product_variants = pd.DataFrame(columns=['l2_product_code', 'variant_type', 'variant_code', 'status'])
    
    # Write to Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Required NSW sheets
        nsw_l0_template.to_excel(writer, sheet_name='NSW_L0_TEMPLATE', index=False)
        print(f"  ✓ Added sheet: NSW_L0_TEMPLATE ({len(nsw_l0_template)} rows)")
        
        nsw_l0_eligibility.to_excel(writer, sheet_name='NSW_L0_L2_ELIGIBILITY', index=False)
        print(f"  ✓ Added sheet: NSW_L0_L2_ELIGIBILITY ({len(nsw_l0_eligibility)} rows)")
        
        nsw_l2.to_excel(writer, sheet_name='NSW_L2_PRODUCTS', index=False)
        print(f"  ✓ Added sheet: NSW_L2_PRODUCTS ({len(nsw_l2)} rows)")
        
        nsw_variants.to_excel(writer, sheet_name='NSW_VARIANT_MASTER', index=False)
        print(f"  ✓ Added sheet: NSW_VARIANT_MASTER ({len(nsw_variants)} rows)")
        
        nsw_product_variants.to_excel(writer, sheet_name='NSW_PRODUCT_VARIANTS', index=False)
        print(f"  ✓ Added sheet: NSW_PRODUCT_VARIANTS ({len(nsw_product_variants)} rows)")
        
        nsw_price_matrix.to_excel(writer, sheet_name='NSW_PRICE_MATRIX', index=False)
        print(f"  ✓ Added sheet: NSW_PRICE_MATRIX ({len(nsw_price_matrix)} rows)")
        
        nsw_l1.to_excel(writer, sheet_name='NSW_L1_CONFIG_LINES', index=False)
        print(f"  ✓ Added sheet: NSW_L1_CONFIG_LINES ({len(nsw_l1)} rows)")
        
        # Optional: Include canonical sheets for reference
        canonical_rows.to_excel(writer, sheet_name=f'{series_name}_CANONICAL_ROWS', index=False)
        coil_prices.to_excel(writer, sheet_name=f'{series_name}_COIL_CODE_PRICES', index=False)
        if accessories is not None and len(accessories) > 0:
            accessories.to_excel(writer, sheet_name=f'{series_name}_ACCESSORY_SKUS', index=False)
    
    print(f"\n✓ NSW format workbook written to: {output_path}")
    print(f"\n⚠️  NOTE: This is a placeholder implementation.")
    print(f"   Series-specific logic must be implemented for:")
    print(f"   - NSW_L2_PRODUCTS extraction from canonical")
    print(f"   - NSW_VARIANT_MASTER from coil codes")
    print(f"   - NSW_PRICE_MATRIX from prices")
    print(f"   - NSW_L1_CONFIG_LINES duty × voltage expansion")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Build NSW Format Workbook (Primary Freeze Artifact)')
    parser.add_argument('--canonical', required=True, help='Input canonical Excel file')
    parser.add_argument('--l2', required=True, help='Input L2 intermediate Excel file')
    parser.add_argument('--l1', required=True, help='Input L1 intermediate Excel file')
    parser.add_argument('--series', required=True, help='Series name (e.g., LC1E, LC1D)')
    parser.add_argument('--wef', required=True, help='WEF date (YYYY-MM-DD)')
    parser.add_argument('--out', required=True, help='Output NSW format Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NSW Phase-5 Catalog Pipeline v2 - Build NSW Format Workbook")
    print("=" * 60)
    
    # Build NSW workbook
    output_path = build_nsw_workbook(
        args.canonical,
        args.l2,
        args.l1,
        args.out,
        args.series,
        args.wef
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Output file: {output_path}")
    print(f"\nThis is the PRIMARY freeze artifact (NSW format).")
    print(f"Upload this file + QC summary to ChatGPT for review.")
    print("=" * 60)


if __name__ == '__main__':
    main()

