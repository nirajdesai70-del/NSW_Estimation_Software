#!/usr/bin/env python3
"""
Script B: Build Catalog Chain Master

Purpose: Rebuild NSW_CATALOG_CHAIN_MASTER from canonical extraction
with corrected L0/L1 naming rules.

This is NOT a migration - it's a rebuild with semantic corrections:
- No OEM series at L0/L1
- Option B: coil voltage is SKU-defining and kept at L2; not part of L1 generic identity
- Business segment vs capability separation

Input:
- Canonical extraction: LC1E_CANONICAL_v1.xlsx
- Source pricelist: (optional, for reference)

Output:
- NSW_CATALOG_CHAIN_MASTER sheet (in master workbook)

Status: Rebuild required - Semantic corrections applied
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime


def build_catalog_chain_from_canonical(canonical_rows, coil_prices=None):
    """
    Build L0/L1/L2 chain from canonical extraction.
    
    Rules:
    - L0: Generic intent (no ratings, no OEM series)
    - L1: Generic spec (ratings, but no OEM series, no coil voltage)
    - L2: OEM specific (make, series, SKU, coil voltage)
    
    Option B: Coil voltage is L2-only (SKU-defining), not in L1.
    """
    print("\n🔗 Building Catalog Chain Master...")
    
    chain_list = []
    
    # Get base reference column
    base_ref_col = None
    for col in ['base_ref_clean', 'Base_Ref', 'base_ref', 'l2_product_code']:
        if col in canonical_rows.columns:
            base_ref_col = col
            break
    
    if base_ref_col is None:
        print("  ✗ Error: Could not find base reference column")
        return pd.DataFrame()
    
    # Group by base reference to build chain
    unique_base_refs = canonical_rows[base_ref_col].dropna().unique()
    
    for base_ref in unique_base_refs:
        # Get all rows for this base ref
        base_rows = canonical_rows[canonical_rows[base_ref_col] == base_ref]
        first_row = base_rows.iloc[0]
        
        # Extract metadata
        make = first_row.get('make', 'Schneider')
        item_type = first_row.get('item_producttype', 'Contactor')
        business_segment = first_row.get('business_subcategory', first_row.get('business_segment', 'Power Contactor'))
        poles = first_row.get('poles', '3P')
        frame = first_row.get('frame_label', '')
        
        # L0: Generic intent (no ratings, no OEM series)
        l0_code = f"L0_{item_type}_{poles}"
        l0_name = f"{item_type} - {poles}"
        
        # L1: Generic spec (ratings, but no OEM series, no coil voltage)
        # Extract ratings from canonical
        duty = first_row.get('duty_class', '')
        current_a = first_row.get('duty_current_A', '')
        ac1_a = first_row.get('catalog_ac1_A', '')
        ac3_a = first_row.get('catalog_ac3_A', '')
        kw = first_row.get('motor_kw', '')
        hp = first_row.get('motor_hp', '')
        
        # Build L1 identifier (no coil voltage - that's L2-only per Option B)
        l1_parts = [item_type, poles]
        if duty:
            l1_parts.append(duty)
        if current_a:
            l1_parts.append(f"{current_a}A")
        if kw:
            l1_parts.append(f"{kw}kW")
        
        l1_code = f"L1_{'_'.join([str(p) for p in l1_parts if p])}"
        l1_name = ' - '.join([str(p) for p in l1_parts if p])
        
        # L2: OEM specific (make, series, SKU, coil voltage)
        series_bucket = first_row.get('series_bucket', '')
        l2_code = base_ref  # Base ref is the L2 product code
        
        # Build chain entry
        chain_entry = {
            'business_category': 'Motor Control',  # Default, should be extracted
            'business_segment': business_segment,
            'item_producttype': item_type,
            'l0_code': l0_code,
            'l0_name': l0_name,
            'l1_code': l1_code,
            'l1_name': l1_name,
            'l2_code': l2_code,
            'l2_product_code': base_ref,
            'make': make,
            'series_bucket': series_bucket,
            'poles': poles,
            'frame_label': frame if frame else '',
            'duty_class': duty if duty else '',
            'duty_current_A': current_a if current_a else '',
            'catalog_ac1_A': ac1_a if ac1_a else '',
            'catalog_ac3_A': ac3_a if ac3_a else '',
            'motor_kw': kw if kw else '',
            'motor_hp': hp if hp else '',
            'status': 'ACTIVE'
        }
        
        chain_list.append(chain_entry)
    
    chain_df = pd.DataFrame(chain_list)
    
    # Deduplicate by l2_code (one entry per L2 product)
    chain_df = chain_df.drop_duplicates(subset=['l2_code'], keep='first')
    
    print(f"  ✓ Built Catalog Chain: {len(chain_df)} L2 products")
    print(f"    - Unique L0 codes: {chain_df['l0_code'].nunique()}")
    print(f"    - Unique L1 codes: {chain_df['l1_code'].nunique()}")
    
    return chain_df


def validate_chain_structure(chain_df):
    """
    Validate chain structure:
    - L0 → L1 → L2 continuity
    - No OEM series at L0/L1
    - Coil voltage not in L1 (Option B)
    """
    print("\n✅ Validating Chain Structure...")
    
    issues = []
    
    # Check required columns
    required_cols = ['l0_code', 'l1_code', 'l2_code', 'item_producttype', 'business_segment']
    for col in required_cols:
        if col not in chain_df.columns:
            issues.append(f"Missing required column: {col}")
    
    # Check for OEM series in L0/L1 (should not be present)
    if 'series_bucket' in chain_df.columns:
        l0_with_series = chain_df[chain_df['l0_code'].str.contains('LC1E|LC1D', case=False, na=False)]
        l1_with_series = chain_df[chain_df['l1_code'].str.contains('LC1E|LC1D', case=False, na=False)]
        
        if len(l0_with_series) > 0:
            issues.append(f"L0 codes contain OEM series (should not): {len(l0_with_series)} entries")
        if len(l1_with_series) > 0:
            issues.append(f"L1 codes contain OEM series (should not): {len(l1_with_series)} entries")
    
    # Check for coil voltage in L1 (should not be present per Option B)
    if 'l1_name' in chain_df.columns:
        l1_with_coil = chain_df[chain_df['l1_name'].str.contains('coil|voltage|220V|415V', case=False, na=False)]
        if len(l1_with_coil) > 0:
            issues.append(f"L1 names contain coil/voltage (should not per Option B): {len(l1_with_coil)} entries")
    
    if issues:
        print("  ⚠️  Validation Issues Found:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print("  ✓ Validation passed")
        print("    - L0/L1 do not contain OEM series ✓")
        print("    - L1 does not contain coil voltage (Option B) ✓")
        return True


def main():
    parser = argparse.ArgumentParser(description='Build Catalog Chain Master (Script B)')
    parser.add_argument('--canonical', required=True, help='Path to canonical extraction file')
    parser.add_argument('--output_workbook', required=True, help='Path to master workbook (will add sheet)')
    parser.add_argument('--validate', action='store_true', help='Run validation after build')
    
    args = parser.parse_args()
    
    canonical_path = Path(args.canonical)
    output_path = Path(args.output_workbook)
    
    if not canonical_path.exists():
        print(f"✗ Error: Canonical file not found: {canonical_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("Script B: Build Catalog Chain Master")
    print("=" * 60)
    print(f"Canonical file: {canonical_path}")
    print(f"Output workbook: {output_path}")
    print()
    
    # Read canonical data
    try:
        xls = pd.ExcelFile(canonical_path)
        canonical_sheet = None
        
        # Find canonical rows sheet
        for sheet_name in xls.sheet_names:
            if 'canonical' in sheet_name.lower() and 'row' in sheet_name.lower():
                canonical_sheet = sheet_name
                break
        
        if not canonical_sheet:
            # Try first sheet
            canonical_sheet = xls.sheet_names[0]
        
        canonical_rows = pd.read_excel(canonical_path, sheet_name=canonical_sheet)
        print(f"✓ Read canonical data: {len(canonical_rows)} rows from '{canonical_sheet}'")
        
    except Exception as e:
        print(f"✗ Error reading canonical file: {e}")
        sys.exit(1)
    
    # Build chain
    chain_df = build_catalog_chain_from_canonical(canonical_rows)
    
    if len(chain_df) == 0:
        print("✗ Error: Chain build failed or produced no data")
        sys.exit(1)
    
    # Validate if requested
    if args.validate:
        validation_passed = validate_chain_structure(chain_df)
        if not validation_passed:
            print("\n⚠️  Validation issues found. Review output before proceeding.")
    
    # Write to workbook
    if output_path.exists():
        # Append to existing workbook
        with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            chain_df.to_excel(writer, sheet_name='NSW_CATALOG_CHAIN_MASTER', index=False)
        print(f"\n✓ Added NSW_CATALOG_CHAIN_MASTER to existing workbook: {output_path}")
    else:
        # Create new workbook
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            chain_df.to_excel(writer, sheet_name='NSW_CATALOG_CHAIN_MASTER', index=False)
        print(f"\n✓ Created new workbook with NSW_CATALOG_CHAIN_MASTER: {output_path}")
    
    print("\n" + "=" * 60)
    print("✓ Chain Build Complete")
    print(f"  Output: {output_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()


