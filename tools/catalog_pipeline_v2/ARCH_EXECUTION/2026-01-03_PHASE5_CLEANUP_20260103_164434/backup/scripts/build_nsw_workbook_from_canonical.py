#!/usr/bin/env python3
"""
NSW Phase-5 Catalog Pipeline v2 - Build NSW Format Workbook from Canonical

Purpose:
- Builds NSW format workbook (PRIMARY freeze artifact) from canonical extraction
- Creates all NSW format sheets: L0/L1/L2 + Variants + Price Matrix
- Implements normalized selection model (duty + voltage normalization)

Input: <SERIES>_CANONICAL_vX.xlsx (canonical rows + coil prices)
Output: NSW_<SERIES>_WEF_<DATE>_vX.xlsx (NSW format workbook)
"""

import argparse
import pandas as pd
import sys
import os
from pathlib import Path
from datetime import datetime


def read_canonical_data(canonical_file, series_name):
    """Read canonical tables from extraction output."""
    try:
        xls = pd.ExcelFile(canonical_file)
        sheet_names = xls.sheet_names
        
        # Find canonical sheets (pattern: <SERIES>_CANONICAL_ROWS, <SERIES>_COIL_CODE_PRICES)
        canonical_rows = None
        coil_prices = None
        accessories = None
        
        for sheet in sheet_names:
            if 'CANONICAL_ROWS' in sheet.upper() or (series_name.upper() in sheet.upper() and 'CANONICAL' in sheet.upper()):
                canonical_rows = pd.read_excel(canonical_file, sheet_name=sheet)
            elif 'COIL' in sheet.upper() and ('PRICE' in sheet.upper() or 'CODE' in sheet.upper()):
                coil_prices = pd.read_excel(canonical_file, sheet_name=sheet)
            elif 'ACCESSORY' in sheet.upper():
                accessories = pd.read_excel(canonical_file, sheet_name=sheet)
        
        if canonical_rows is None:
            raise ValueError(f"Could not find canonical rows sheet in {canonical_file}")
        if coil_prices is None:
            raise ValueError(f"Could not find coil prices sheet in {canonical_file}")
        
        print(f"✓ Read canonical data:")
        print(f"  - Canonical rows: {len(canonical_rows)} rows")
        print(f"  - Coil prices: {len(coil_prices)} rows")
        if accessories is not None and len(accessories) > 0:
            print(f"  - Accessories: {len(accessories)} rows")
        else:
            print(f"  - Accessories: not detected")
        
        return canonical_rows, coil_prices, accessories
    except Exception as e:
        print(f"✗ Error reading canonical file: {e}")
        sys.exit(1)


def build_nsw_l2_products(canonical_rows, series_name, series_bucket):
    """
    Build NSW_L2_PRODUCTS from canonical rows.
    
    L2 = Product identity only (no price, no voltage, no duty)
    """
    l2_list = []
    
    # Get unique base refs
    base_ref_col = None
    for col in ['base_ref_clean', 'Base_Ref', 'base_ref', 'l2_product_code']:
        if col in canonical_rows.columns:
            base_ref_col = col
            break
    
    if base_ref_col is None:
        raise ValueError("Could not find base reference column in canonical rows")
    
    unique_base_refs = canonical_rows[base_ref_col].dropna().unique()
    
    for base_ref in unique_base_refs:
        # Get first row for this base ref (for metadata)
        base_row = canonical_rows[canonical_rows[base_ref_col] == base_ref].iloc[0]
        
        # Extract metadata
        make = base_row.get('make', 'Schneider')
        item_type = base_row.get('item_producttype', 'Contactor')
        subcategory = base_row.get('business_subcategory', 'Power Contactor')
        poles = base_row.get('poles', '3P')
        frame = base_row.get('frame_label', '')
        
        # Handle frame carry-forward (if NaN, convert to empty string)
        if pd.isna(frame) or frame == '' or str(frame).lower() == 'nan':
            frame = ''
        else:
            frame = str(frame).strip()
        
        # Build generic name
        generic_name = f"Power Contactor – {series_bucket} – {poles}"
        
        l2_list.append({
            'make': make,
            'series_name': series_name,
            'series_bucket': series_bucket,
            'item_producttype': item_type,
            'business_subcategory': subcategory,
            'poles': poles,
            'frame_label': frame if frame else '',
            'l2_product_code': base_ref,
            'generic_name': generic_name,
            'status': 'ACTIVE'
        })
    
    nsw_l2 = pd.DataFrame(l2_list)
    print(f"  ✓ Built NSW_L2_PRODUCTS: {len(nsw_l2)} rows")
    return nsw_l2


def build_nsw_variant_master(coil_prices):
    """
    Build NSW_VARIANT_MASTER from unique coil codes.
    
    Extracts unique variants (coil codes) and their voltage properties.
    """
    # Get unique coil codes
    coil_code_col = None
    for col in ['coil_code', 'variant_code', 'Coil_Code']:
        if col in coil_prices.columns:
            coil_code_col = col
            break
    
    if coil_code_col is None:
        raise ValueError("Could not find coil code column in coil prices")
    
    # Get voltage columns
    voltage_type_col = None
    voltage_value_col = None
    for col in coil_prices.columns:
        if 'voltage_type' in col.lower():
            voltage_type_col = col
        if 'voltage_value' in col.lower() or 'voltage_v' in col.lower():
            voltage_value_col = col
    
    variants_list = []
    seen_variants = set()
    
    for _, row in coil_prices.iterrows():
        variant_code = row[coil_code_col]
        if pd.isna(variant_code) or variant_code in seen_variants:
            continue
        
        seen_variants.add(variant_code)
        
        # Get voltage info
        voltage_type = row.get(voltage_type_col, 'AC') if voltage_type_col else 'AC'
        voltage_v = row.get(voltage_value_col, 0) if voltage_value_col else 0
        
        # Build display label
        display_label = f"{variant_code} ({int(voltage_v)}V {voltage_type})"
        
        variants_list.append({
            'variant_type': 'COIL_VOLTAGE',
            'variant_code': variant_code,
            'voltage_type': voltage_type,
            'voltage_V': int(voltage_v) if not pd.isna(voltage_v) else 0,
            'display_label': display_label,
            'is_active': True
        })
    
    nsw_variants = pd.DataFrame(variants_list)
    print(f"  ✓ Built NSW_VARIANT_MASTER: {len(nsw_variants)} rows")
    return nsw_variants


def build_nsw_product_variants(nsw_l2, coil_prices, nsw_variants):
    """
    Build NSW_PRODUCT_VARIANTS - maps which variants are valid for which L2 products.
    """
    coil_code_col = None
    for col in ['coil_code', 'variant_code', 'Coil_Code']:
        if col in coil_prices.columns:
            coil_code_col = col
            break
    
    base_ref_col = None
    for col in ['base_ref_clean', 'Base_Ref', 'base_ref', 'l2_product_code']:
        if col in coil_prices.columns:
            base_ref_col = col
            break
    
    voltage_type_col = None
    voltage_value_col = None
    for col in coil_prices.columns:
        if 'voltage_type' in col.lower():
            voltage_type_col = col
        if 'voltage_value' in col.lower() or 'voltage_v' in col.lower():
            voltage_value_col = col
    
    product_variants_list = []
    
    # Get series info from L2
    make = nsw_l2['make'].iloc[0] if len(nsw_l2) > 0 else 'Schneider'
    series_name = nsw_l2['series_name'].iloc[0] if len(nsw_l2) > 0 else ''
    series_bucket = nsw_l2['series_bucket'].iloc[0] if len(nsw_l2) > 0 else ''
    
    # Create mapping from variant code to display label
    variant_map = {row['variant_code']: row['display_label'] for _, row in nsw_variants.iterrows()}
    
    for _, price_row in coil_prices.iterrows():
        base_ref = price_row[base_ref_col]
        variant_code = price_row[coil_code_col]
        voltage_type = price_row.get(voltage_type_col, 'AC') if voltage_type_col else 'AC'
        voltage_v = price_row.get(voltage_value_col, 0) if voltage_value_col else 0
        catalog_label = variant_map.get(variant_code, f"{variant_code} ({int(voltage_v)}V {voltage_type})")
        
        product_variants_list.append({
            'make': make,
            'series_name': series_name,
            'series_bucket': series_bucket,
            'variant_type': 'COIL_VOLTAGE',
            'l2_product_code': base_ref,
            'variant_code': variant_code,
            'voltage_type': voltage_type,
            'voltage_V': int(voltage_v) if not pd.isna(voltage_v) else 0,
            'catalog_voltage_label': catalog_label
        })
    
    # Deduplicate
    product_variants_df = pd.DataFrame(product_variants_list)
    product_variants_df = product_variants_df.drop_duplicates(subset=['l2_product_code', 'variant_code'])
    
    print(f"  ✓ Built NSW_PRODUCT_VARIANTS: {len(product_variants_df)} rows")
    return product_variants_df


def build_nsw_price_matrix(coil_prices, nsw_l2, canonical_rows, wef_date, pricelist_ref, series_bucket='LC1E'):
    """
    Build NSW_PRICE_MATRIX from coil prices.
    
    Price matrix: l2_product_code × variant_code → price
    """
    coil_code_col = None
    for col in ['coil_code', 'variant_code', 'Coil_Code']:
        if col in coil_prices.columns:
            coil_code_col = col
            break
    
    base_ref_col = None
    for col in ['base_ref_clean', 'Base_Ref', 'base_ref', 'l2_product_code']:
        if col in coil_prices.columns:
            base_ref_col = col
            break
    
    price_col = None
    for col in ['price', 'Price', 'rate_inr', 'Rate']:
        if col in coil_prices.columns:
            price_col = col
            break
    
    voltage_type_col = None
    voltage_value_col = None
    for col in coil_prices.columns:
        if 'voltage_type' in col.lower():
            voltage_type_col = col
        if 'voltage_value' in col.lower() or 'voltage_v' in col.lower():
            voltage_value_col = col
    
    # Get series info from L2
    make = nsw_l2['make'].iloc[0] if len(nsw_l2) > 0 else 'Schneider'
    series_name = nsw_l2['series_name'].iloc[0] if len(nsw_l2) > 0 else ''
    series_bucket = nsw_l2['series_bucket'].iloc[0] if len(nsw_l2) > 0 else ''
    
    # Create base_ref to poles mapping from canonical rows
    base_ref_to_poles = {}
    base_ref_col_canonical = None
    for col in ['base_ref_clean', 'Base_Ref', 'base_ref', 'l2_product_code']:
        if col in canonical_rows.columns:
            base_ref_col_canonical = col
            break
    
    if base_ref_col_canonical:
        for _, row in canonical_rows.iterrows():
            base_ref_canonical = row[base_ref_col_canonical]
            poles_val = row.get('poles', '3P')
            if pd.notna(base_ref_canonical):
                base_ref_to_poles[base_ref_canonical] = poles_val
    
    price_matrix_list = []
    
    for _, price_row in coil_prices.iterrows():
        base_ref = price_row[base_ref_col]
        variant_code = price_row[coil_code_col]
        price = price_row[price_col] if price_col else 0
        voltage_type = price_row.get(voltage_type_col, 'AC') if voltage_type_col else 'AC'
        voltage_v = price_row.get(voltage_value_col, 0) if voltage_value_col else 0
        
        # Get source info if available
        source_page_raw = price_row.get('source_page_or_block', '')
        table_id_raw = price_row.get('table_id', '')
        completed_ref = price_row.get('completed_sku', f"{base_ref}{variant_code}")
        
        # Extract page number from source_page_or_block
        # V6 format: numeric (8), canonical format: "Table 1" or similar
        # For LC1E, "Table 1" refers to page 8 in the pricelist
        source_page = ''
        if source_page_raw:
            import re
            # For LC1E series, "Table 1" means page 8
            if 'Table' in str(source_page_raw) and series_bucket == 'LC1E':
                source_page = 8
            else:
                # Try to extract numeric page number
                page_match = re.search(r'(\d+)', str(source_page_raw))
                if page_match:
                    source_page = int(page_match.group(1))
                else:
                    source_page = source_page_raw
        
        # Build table_id in v6 format: P8_T1_3P_AC_M7_N5
        # Format: P{page}_T{table}_{poles}_{voltage_type}_{variants}
        table_id = ''
        if table_id_raw and source_page:
            # Extract table number if available
            table_num_match = re.search(r'T(\d+)', str(source_page_raw))
            table_num = table_num_match.group(1) if table_num_match else '1'
            
            # Get poles from mapping
            poles_str = base_ref_to_poles.get(base_ref, '3P')
            voltage_str = voltage_type
            
            # Get variants for this table (simplified - use variant_code)
            variant_str = variant_code
            
            # Build v6 format: P8_T1_3P_AC_M7_N5
            # For now, use simplified format: P{page}_T{table}_{poles}_{voltage}_{variant}
            table_id = f"P{source_page}_T{table_num}_{poles_str}_{voltage_str}_{variant_str}"
        elif table_id_raw:
            # Fallback to original table_id if page extraction failed
            table_id = table_id_raw
        
        price_matrix_list.append({
            'make': make,
            'series_name': series_name,
            'series_bucket': series_bucket,
            'l2_product_code': base_ref,
            'variant_type': 'COIL_VOLTAGE',
            'variant_code': variant_code,
            'voltage_type': voltage_type,
            'voltage_V': int(voltage_v) if not pd.isna(voltage_v) else 0,
            'duty_class': None,  # Price doesn't depend on duty for LC1E
            'rate_inr': float(price) if not pd.isna(price) else 0,
            'currency': 'INR',
            'effective_from': wef_date,
            'pricelist_ref': pricelist_ref,
            'source_page': source_page if source_page else '',
            'table_id': table_id if table_id else '',
            'completed_ref': completed_ref
        })
    
    price_matrix = pd.DataFrame(price_matrix_list)
    print(f"  ✓ Built NSW_PRICE_MATRIX: {len(price_matrix)} rows")
    return price_matrix


def build_nsw_l1_config_lines(canonical_rows, coil_prices, nsw_l2, nsw_variants, price_matrix):
    """
    Build NSW_L1_CONFIG_LINES with duty × voltage expansion and normalization.
    
    L1 = Configuration + engineering meaning
    - Duty normalization: duty_class, duty_current_A, catalog_ac1_A, catalog_ac3_A
    - Voltage normalization: variant_code, voltage_class_code, selected_voltage_V, catalog_voltage_label
    - Engineering context: motor_kw, motor_hp, aux_no, aux_nc, poles, frame_label
    """
    base_ref_col = None
    for col in ['base_ref_clean', 'Base_Ref', 'base_ref', 'l2_product_code']:
        if col in canonical_rows.columns:
            base_ref_col = col
            break
    
    coil_code_col = None
    for col in ['coil_code', 'variant_code', 'Coil_Code']:
        if col in coil_prices.columns:
            coil_code_col = col
            break
    
    # Get series info
    series_name = nsw_l2['series_name'].iloc[0] if len(nsw_l2) > 0 else ''
    
    l1_list = []
    l1_seq = 1
    
    # Get unique base refs
    unique_base_refs = canonical_rows[base_ref_col].dropna().unique()
    
    # Duty classes to expand
    duty_classes = ['AC1', 'AC3']
    
    # Create variant lookup
    variant_lookup = {}
    for _, var_row in nsw_variants.iterrows():
        variant_lookup[var_row['variant_code']] = {
            'voltage_type': var_row['voltage_type'],
            'voltage_V': var_row['voltage_V'],
            'display_label': var_row['display_label']
        }
    
    for base_ref in unique_base_refs:
        # Get canonical row for this base ref
        base_canonical = canonical_rows[canonical_rows[base_ref_col] == base_ref].iloc[0]
        
        # Get L2 info
        l2_info = nsw_l2[nsw_l2['l2_product_code'] == base_ref].iloc[0]
        
        # Get available variants for this base ref (from price matrix)
        available_variants = price_matrix[price_matrix['l2_product_code'] == base_ref]['variant_code'].unique()
        
        # Get ratings
        ac1_current = base_canonical.get('ac1_current_a', 0)
        ac3_current = base_canonical.get('ac3_current_a', 0)
        motor_kw = base_canonical.get('motor_kw', 0)
        motor_hp = base_canonical.get('motor_hp', 0)
        aux_no = base_canonical.get('aux_no_count', 0)
        aux_nc = base_canonical.get('aux_nc_count', 0)
        poles = base_canonical.get('poles', '3P')
        frame = base_canonical.get('frame_label', '')
        
        # Handle frame_label - convert NaN to empty string
        if pd.isna(frame) or str(frame).lower() == 'nan':
            frame = ''
        else:
            frame = str(frame).strip()
        
        # Build L1 group ID
        l1_group_id = f"GRP-Schneider-{base_ref}"
        
        # Expand: duty × voltage
        for duty_class in duty_classes:
            # Duty normalization
            if duty_class == 'AC1':
                duty_current = ac1_current
            else:  # AC3
                duty_current = ac3_current
            
            for variant_code in available_variants:
                variant_info = variant_lookup.get(variant_code, {})
                
                # Voltage normalization
                voltage_class_code = variant_code
                selected_voltage_type = variant_info.get('voltage_type', 'AC')
                selected_voltage_v = variant_info.get('voltage_V', 0)
                catalog_voltage_label = variant_info.get('display_label', f"{variant_code}")
                
                # Build generic descriptor (series-neutral per v1.2 CLEAN)
                kw_str = f"{motor_kw}kW@415V" if motor_kw and not pd.isna(motor_kw) else ""
                aux_no_int = int(aux_no) if not pd.isna(aux_no) else 0
                aux_nc_int = int(aux_nc) if not pd.isna(aux_nc) else 0
                aux_str = f"Aux {aux_no_int}NO+{aux_nc_int}NC" if (aux_no_int or aux_nc_int) else ""
                # Note: series_bucket removed from generic_descriptor to maintain series-neutrality (v1.2 CLEAN)
                generic_desc = f"Power Contactor – {poles} | {duty_class} | {selected_voltage_v}V {selected_voltage_type} | {kw_str} | {aux_str}".strip(" |")
                
                # Get price from price matrix
                price_row = price_matrix[
                    (price_matrix['l2_product_code'] == base_ref) &
                    (price_matrix['variant_code'] == variant_code)
                ]
                resolved_price = price_row['rate_inr'].iloc[0] if len(price_row) > 0 else None
                catalog_trace = price_row['completed_ref'].iloc[0] if len(price_row) > 0 else f"{base_ref}{variant_code}"
                
                l1_list.append({
                    'l1_seq_no': l1_seq,
                    'series_name': series_name,
                    'generic_descriptor': generic_desc,
                    'l1_group_id': l1_group_id,
                    'l1_id': None,  # Filled at quote time
                    'l1_line_type': 'BASE',
                    'l2_product_code': base_ref,
                    'poles': poles,
                    'no_of_poles': poles,
                    'frame_label': '' if (pd.isna(frame) or str(frame).strip().lower() in ['nan', 'none', '']) else str(frame).strip(),
                    'variant_code': variant_code,
                    'voltage_class_code': voltage_class_code,
                    'voltage_type': selected_voltage_type,
                    'selected_voltage_type': selected_voltage_type,
                    'voltage_V': selected_voltage_v,
                    'selected_voltage_V': selected_voltage_v,
                    'catalog_voltage_label': catalog_voltage_label,
                    'duty_class': duty_class,
                    'duty_current_A': duty_current,
                    'catalog_ac1_A': ac1_current,
                    'catalog_ac3_A': ac3_current,
                    'motor_kw': motor_kw,
                    'motor_hp': motor_hp,
                    'aux_no': int(aux_no) if aux_no is not None and not pd.isna(aux_no) else 0,
                    'aux_nc': int(aux_nc) if aux_nc is not None and not pd.isna(aux_nc) else 0,
                    'resolved_price_inr': resolved_price,
                    'catalog_trace_ref': catalog_trace,
                    'status': 'ACTIVE'
                })
                
                l1_seq += 1
    
    nsw_l1 = pd.DataFrame(l1_list)
    print(f"  ✓ Built NSW_L1_CONFIG_LINES: {len(nsw_l1)} rows")
    return nsw_l1


def build_nsw_l0_templates():
    """
    Build NSW_L0_TEMPLATE - optional intent layer.
    
    Can be empty or populated with starter intents.
    """
    l0_template = pd.DataFrame(columns=[
        'l0_template_id', 'l0_intent_name', 'description', 'status'
    ])
    
    # Optional: Add starter intents
    # l0_template = pd.DataFrame([
    #     {'l0_template_id': 'L0-001', 'l0_intent_name': 'Motor Starter', 'description': 'Motor control applications', 'status': 'ACTIVE'},
    #     {'l0_template_id': 'L0-002', 'l0_intent_name': 'Pump Panel', 'description': 'Pump control applications', 'status': 'ACTIVE'},
    # ])
    
    print(f"  ✓ Built NSW_L0_TEMPLATE: {len(l0_template)} rows (empty)")
    return l0_template


def build_nsw_l0_eligibility(nsw_l2):
    """
    Build NSW_L0_L2_ELIGIBILITY - optional L0→L2 mapping.
    
    Can be empty or populated with eligibility mappings.
    """
    l0_eligibility = pd.DataFrame(columns=[
        'l0_template_id', 'l2_product_code', 'status'
    ])
    
    print(f"  ✓ Built NSW_L0_L2_ELIGIBILITY: {len(l0_eligibility)} rows (empty)")
    return l0_eligibility


def build_nsw_workbook(canonical_file, output_path, series_name, series_bucket, wef_date, pricelist_ref):
    """
    Build complete NSW format workbook from canonical extraction.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Build NSW Format Workbook from Canonical")
    print("=" * 60)
    print(f"  Series: {series_name} ({series_bucket})")
    print(f"  WEF: {wef_date}")
    print(f"  Input: {canonical_file}")
    print(f"  Output: {output_path}")
    print()
    
    # Read canonical data
    canonical_rows, coil_prices, accessories = read_canonical_data(canonical_file, series_bucket)
    
    # Build NSW sheets
    print("\nBuilding NSW sheets...")
    nsw_l2 = build_nsw_l2_products(canonical_rows, series_name, series_bucket)
    nsw_variants = build_nsw_variant_master(coil_prices)
    nsw_product_variants = build_nsw_product_variants(nsw_l2, coil_prices, nsw_variants)
    nsw_price_matrix = build_nsw_price_matrix(coil_prices, nsw_l2, canonical_rows, wef_date, pricelist_ref, series_bucket)
    nsw_l1 = build_nsw_l1_config_lines(canonical_rows, coil_prices, nsw_l2, nsw_variants, nsw_price_matrix)
    nsw_l0_template = build_nsw_l0_templates()
    nsw_l0_eligibility = build_nsw_l0_eligibility(nsw_l2)
    
    # Write to Excel
    print(f"\nWriting NSW workbook...")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        nsw_l0_template.to_excel(writer, sheet_name='NSW_L0_TEMPLATE', index=False)
        nsw_l0_eligibility.to_excel(writer, sheet_name='NSW_L0_L2_ELIGIBILITY', index=False)
        nsw_l2.to_excel(writer, sheet_name='NSW_L2_PRODUCTS', index=False)
        nsw_variants.to_excel(writer, sheet_name='NSW_VARIANT_MASTER', index=False)
        nsw_product_variants.to_excel(writer, sheet_name='NSW_PRODUCT_VARIANTS', index=False)
        nsw_price_matrix.to_excel(writer, sheet_name='NSW_PRICE_MATRIX', index=False)
        nsw_l1.to_excel(writer, sheet_name='NSW_L1_CONFIG_LINES', index=False)
        
        # Optional: Include canonical sheets for reference
        canonical_rows.to_excel(writer, sheet_name=f'{series_bucket}_CANONICAL_ROWS', index=False)
        coil_prices.to_excel(writer, sheet_name=f'{series_bucket}_COIL_CODE_PRICES', index=False)
        if accessories is not None and len(accessories) > 0:
            accessories.to_excel(writer, sheet_name=f'{series_bucket}_ACCESSORY_SKUS', index=False)
    
    # Set proper file permissions (readable by owner and group, writable by owner)
    try:
        os.chmod(output_path, 0o644)
    except (OSError, PermissionError):
        # On some filesystems (exFAT/NTFS), chmod may not work - this is OK
        pass
    
    # Clear extended attributes that can cause visibility issues on external drives
    try:
        import subprocess
        subprocess.run(['xattr', '-c', str(output_path)], check=False, capture_output=True)
    except (OSError, FileNotFoundError):
        # xattr command not available or failed - this is OK
        pass
    
    print(f"\n✓ NSW format workbook written to: {output_path}")
    print(f"\nSheets created:")
    print(f"  - NSW_L0_TEMPLATE: {len(nsw_l0_template)} rows")
    print(f"  - NSW_L0_L2_ELIGIBILITY: {len(nsw_l0_eligibility)} rows")
    print(f"  - NSW_L2_PRODUCTS: {len(nsw_l2)} rows")
    print(f"  - NSW_VARIANT_MASTER: {len(nsw_variants)} rows")
    print(f"  - NSW_PRODUCT_VARIANTS: {len(nsw_product_variants)} rows")
    print(f"  - NSW_PRICE_MATRIX: {len(nsw_price_matrix)} rows")
    print(f"  - NSW_L1_CONFIG_LINES: {len(nsw_l1)} rows")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Build NSW Format Workbook from Canonical (Primary Freeze Artifact)')
    parser.add_argument('--canonical', required=True, help='Input canonical Excel file')
    parser.add_argument('--series', required=True, help='Series code (e.g., LC1E, LC1D)')
    parser.add_argument('--series_name', required=True, help='Series name (e.g., Easy TeSys)')
    parser.add_argument('--wef', required=True, help='WEF date (YYYY-MM-DD)')
    parser.add_argument('--pricelist_ref', default='', help='Price list reference (e.g., WEF 15 Jul 2025)')
    parser.add_argument('--out', required=True, help='Output NSW format Excel file path')
    
    args = parser.parse_args()
    
    # Default pricelist_ref if not provided
    if not args.pricelist_ref:
        args.pricelist_ref = f"WEF {args.wef}"
    
    build_nsw_workbook(
        args.canonical,
        args.out,
        args.series_name,
        args.series,
        args.wef,
        args.pricelist_ref
    )
    
    print("\n" + "=" * 60)
    print("✓ NSW format workbook ready (PRIMARY freeze artifact)")
    print("=" * 60)


if __name__ == '__main__':
    main()

