#!/usr/bin/env python3
"""
NSW Phase-5 Catalog Pipeline v2 - Script B
Derive L1 Lines from L2 SKU Master

Purpose:
- Reads L2 SKU Master, Price History, and RATING_MAP
- Creates L1 BASE lines with full combinations (Duty × Voltage)
- Creates L1 FEATURE lines for accessories (SC_L4), NOT multiplied across duty/voltage

Rules:
- Duty AC1/AC3: SC_L3 labels on L1. Ratings (Current A, kW, HP) are KVU attributes on L1.
- Voltage: KVU attribute on L1. Voltage creates multiple L1 lines in full-combination mode.
- Accessories: create FEATURE L1 lines (SC_L4) once per base group; do NOT explode them across duty/voltage combinations.
- Frame is derived classification only; never multiplies.
"""

import argparse
import pandas as pd
import sys
import re
from pathlib import Path

# Coil suffix pattern for base reference extraction (includes range codes for stripping)
# Patch 1: Added LC1E-specific codes: N5, M5, M5WB, N5WB
COIL_SUFFIX_PATTERN = r'(M7|N7|F7|B7|N5|M5|M5WB|N5WB|BD|FD|MD|BL|FL|ML|EL|BBE|BNE|EHE|KUE)$'

# Coil code map for voltage extraction (fixed voltages only)
# Patch 1: Added LC1E-specific codes
COIL_VOLTAGE_MAP = {
    'M7': 220, 'N7': 415, 'F7': 110, 'B7': 24,
    'N5': 415, 'M5': 220, 'M5WB': 220, 'N5WB': 415,  # LC1E codes
    'MD': 220, 'FD': 110, 'BD': 24,
    'BL': 24, 'FL': 110, 'ML': 220, 'EL': 48  # EL is 48V
}

# Duty classes
DUTY_CLASSES = ['AC1', 'AC3']


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
            print("⚠ Warning: RATING_MAP sheet not found. KVU values will be blank.")
        
        print(f"✓ Read L2 data:")
        print(f"  - L2_SKU_MASTER: {len(l2_sku_master)} rows")
        print(f"  - L2_PRICE_HISTORY: {len(l2_price_history)} rows")
        print(f"  - RATING_MAP: {len(rating_map)} rows")
        return l2_sku_master, l2_price_history, rating_map
    except Exception as e:
        print(f"✗ Error reading L2 file: {e}")
        sys.exit(1)


def extract_base_ref_from_sku(sku):
    """
    Extract base reference from SKU using regex.
    
    Removes coil suffix tokens: (M7|N7|F7|B7|BD|FD|MD|BL|FL|ML|EL|BBE|BNE|EHE|KUE)$
    """
    if pd.isna(sku):
        return None
    
    sku_str = str(sku).strip()
    
    # Remove coil suffix
    base_ref = re.sub(COIL_SUFFIX_PATTERN, '', sku_str)
    
    return base_ref if base_ref else sku_str


def extract_voltage_from_sku(sku):
    """Extract voltage value from SKU suffix (fixed voltage codes only)."""
    match = re.search(COIL_SUFFIX_PATTERN, str(sku))
    if match:
        suffix = match.group(1)
        # Only return voltage if it's a fixed voltage code (not a range code)
        if suffix in COIL_VOLTAGE_MAP:
            return COIL_VOLTAGE_MAP[suffix]
        # Range codes (BBE, BNE, EHE, KUE) don't have fixed voltages - return None
        return None
    
    return None  # No voltage suffix found


def extract_voltage_type_from_sku(sku):
    """Extract voltage type (AC/DC) from SKU suffix."""
    # Patch 1: Added LC1E-specific codes, removed range codes from fixed voltage lists
    dc_suffixes = ['BD', 'FD', 'MD', 'BL', 'FL', 'ML', 'EL']  # Fixed DC voltages only (not range codes)
    ac_suffixes = ['M7', 'N7', 'F7', 'B7', 'N5', 'M5', 'M5WB', 'N5WB']  # LC1E codes are AC
    
    match = re.search(COIL_SUFFIX_PATTERN, str(sku))
    if match:
        suffix = match.group(1)
        if suffix in dc_suffixes:
            return 'DC'
        if suffix in ac_suffixes:
            return 'AC'
        # Range codes (BBE, BNE, EHE, KUE) - determine type based on code pattern
        if suffix in ['BBE', 'BNE', 'EHE', 'KUE']:
            # These are typically DC ranges, but could be AC/DC - default to DC for now
            return 'DC'
    
    return None  # No match found


def create_l1_base_lines(l2_sku_master, l2_price_history, rating_map, l1_mode='duty_x_voltage'):
    """
    Create L1 BASE lines from L2 SKU Master with full combinations.
    
    If l1_mode == 'duty_x_voltage':
    - Group L2 SKUs by base reference
    - For each base reference, create L1 lines for each combination of:
      - Duty class (AC1, AC3) from RATING_MAP
      - Voltage variant (from actual L2 SKUs that exist)
    
    If l1_mode == 'base_only':
    - Create one L1 line per L2 SKU
    """
    l1_lines = []
    l1_id_counter = 1
    
    # Get latest price per SKU (sorted by EffectiveFrom descending)
    latest_prices = l2_price_history.sort_values('EffectiveFrom', ascending=False).groupby('OEM_Catalog_No').first().reset_index()
    l2_with_price = l2_sku_master.merge(
        latest_prices[['OEM_Catalog_No', 'Rate']],
        on='OEM_Catalog_No',
        how='left'
    )
    
    if l1_mode == 'duty_x_voltage':
        # Patch 2: Helper function to get duties per Base_Ref (not global)
        def duties_for_base(base_ref, rating_map):
            """Get duty classes for a specific base reference from RATING_MAP."""
            if rating_map is None or len(rating_map) == 0:
                return ['AC1', 'AC3'], True  # Return duties and fallback flag
            duties = rating_map[rating_map['Base_Ref'] == base_ref]['DutyClass'].dropna().unique().tolist()
            if duties:
                return duties, False  # Duties found, no fallback
            else:
                return ['AC1', 'AC3'], True  # Fallback to default
        
        # Group L2 SKUs by base reference
        l2_with_price['Base_Ref'] = l2_with_price['OEM_Catalog_No'].apply(extract_base_ref_from_sku)
        
        # Group by base reference
        for base_ref, group in l2_with_price.groupby('Base_Ref'):
            if pd.isna(base_ref) or base_ref == '':
                base_ref = group.iloc[0]['OEM_Catalog_No']
            
            make = group.iloc[0]['Make']
            product_type = group.iloc[0].get('Item_ProductType', '')
            series_bucket = group.iloc[0].get('SeriesBucket', '')
            poles = group.iloc[0].get('poles', '')  # Get poles from merged canonical data
            
            # Patch 2: Get duties PER base_ref (not global)
            duties, used_fallback = duties_for_base(base_ref, rating_map)
            
            # Get voltage variants from actual SKUs in this group
            voltage_variants = []
            for _, sku_row in group.iterrows():
                sku = sku_row['OEM_Catalog_No']
                voltage_value = extract_voltage_from_sku(sku)
                voltage_type = extract_voltage_type_from_sku(sku)
                # Include all voltage variants (including range codes with voltage=None)
                voltage_variants.append({
                    'sku': sku,
                    'voltage': voltage_value,
                    'voltage_type': voltage_type
                })
            
            # Patch 4: De-dup voltage variants (by sku, voltage, voltage_type tuple)
            seen = set()
            unique_variants = []
            for v in voltage_variants:
                key = (v['sku'], v['voltage'], v['voltage_type'])
                if key not in seen:
                    unique_variants.append(v)
                    seen.add(key)
            voltage_variants = unique_variants
            
            # Create L1 lines for each combination of duty × voltage
            for duty in duties:
                for voltage_info in voltage_variants:
                    l1_id = f"L1-{l1_id_counter:06d}"
                    group_id = f"GRP-{make}-{base_ref}"
                    
                    # Patch 4: SC_L2_Operation for range codes (voltage is None)
                    if voltage_info['voltage'] is None:
                        sc_l2_operation = f"{voltage_info['voltage_type']} Coil Range" if voltage_info['voltage_type'] else "Coil Range"
                    else:
                        sc_l2_operation = f"{voltage_info['voltage_type']} Coil" if voltage_info['voltage_type'] else "Coil"
                    
                    # Patch 2: Mark notes if fallback was used
                    notes = 'DUTY_FALLBACK_REVIEW' if used_fallback else ''
                    
                    # Build descriptive GenericDescriptor
                    desc_parts = []
                    if product_type:
                        desc_parts.append(product_type)
                    if series_bucket:
                        desc_parts.append(series_bucket)
                    
                    # Add poles if available from L2 (via merge from canonical)
                    if poles:
                        desc_parts.append(poles)
                    
                    # Add coil type
                    if voltage_info['voltage_type']:
                        desc_parts.append(f"{voltage_info['voltage_type']} Coil")
                    if voltage_info['voltage']:
                        desc_parts.append(f"{voltage_info['voltage']}V")
                    
                    # Add duty
                    if duty:
                        desc_parts.append(duty)
                    
                    # Add kW if available from rating map
                    if rating_map is not None and len(rating_map) > 0:
                        rating_row = rating_map[
                            (rating_map['Base_Ref'] == base_ref) &
                            (rating_map['DutyClass'] == duty)
                        ]
                        if len(rating_row) > 0 and pd.notna(rating_row.iloc[0].get('kW')) and rating_row.iloc[0]['kW'] != '':
                            kw_val = rating_row.iloc[0]['kW']
                            desc_parts.append(f"{kw_val}kW")
                    
                    generic_desc = ", ".join(desc_parts) if desc_parts else product_type
                    
                    l1_lines.append({
                        'L1_Id': l1_id,
                        'L1_Group_Id': group_id,
                        'L1_Line_Type': 'BASE',
                        'Parent_Base_L1_Id': '',
                        'Feature_Code': '',
                        'Category': 'Motor Control',  # Default - should come from taxonomy
                        'Item_ProductType': product_type,
                        'GenericLevel': 'L1',
                        'GenericDescriptor': generic_desc,
                        'SC_L1_Construction': 'Base Contactor',  # Non-blank default
                        'SC_L2_Operation': sc_l2_operation,
                        'SC_L3_FeatureClass': duty if duty else '',
                        'SC_L4_AccessoryClass': '',
                        'L2_OEM_Catalog_No': voltage_info['sku'],
                        'L2_Make': make,
                        'Requested_By_User': '',
                        'Notes': notes,
                        'Status': 'ACTIVE'
                    })
                    l1_id_counter += 1
    else:
        # base_only mode - one L1 line per L2 SKU
        for idx, l2_row in l2_with_price.iterrows():
            sku = l2_row['OEM_Catalog_No']
            make = l2_row['Make']
            product_type = l2_row.get('Item_ProductType', '')
            voltage_type = extract_voltage_type_from_sku(sku)
            base_ref = extract_base_ref_from_sku(sku)
            
            l1_id = f"L1-{l1_id_counter:06d}"
            group_id = f"GRP-{make}-{base_ref}"
            
            l1_lines.append({
                'L1_Id': l1_id,
                'L1_Group_Id': group_id,
                'L1_Line_Type': 'BASE',
                'Parent_Base_L1_Id': '',
                'Feature_Code': '',
                'Category': 'Motor Control',  # Default
                'Item_ProductType': product_type,
                'GenericLevel': 'L1',
                'GenericDescriptor': product_type,
                'SC_L1_Construction': 'Base Contactor',  # Non-blank default
                'SC_L2_Operation': voltage_type + ' Coil',
                'SC_L3_FeatureClass': '',
                'SC_L4_AccessoryClass': '',
                'L2_OEM_Catalog_No': sku,
                'L2_Make': make,
                'Requested_By_User': '',
                'Notes': '',
                'Status': 'ACTIVE'
            })
            l1_id_counter += 1
    
    print(f"✓ Created {len(l1_lines)} L1 BASE lines")
    return pd.DataFrame(l1_lines)


def create_l1_feature_lines_for_accessories(l2_sku_master, base_l1_lines):
    """
    Create L1 FEATURE lines for accessories (SC_L4).
    
    Patch 3: Accessories are identified by IsAccessory flag (canonical-tag driven),
    NOT by keyword matching. This ensures deterministic, correct classification.
    
    Rule: Create FEATURE L1 lines in separate accessory groups (GRP-{Make}-{SeriesBucket}-ACCESSORIES).
    Do NOT attach them to base groups automatically to avoid incorrect linking.
    Accessories must NOT multiply across duty/voltage.
    
    LOCKED VALUES:
    - Item_ProductType = "Contactor" (locked rule)
    - Business_SubCategory = "Power Contactor" (locked rule)
    """
    feature_lines = []
    l1_id_counter = len(base_l1_lines) + 1
    
    # Patch 3: Use IsAccessory flag (canonical-tag driven), not keyword matching
    if 'IsAccessory' not in l2_sku_master.columns:
        print("  ⚠ No IsAccessory column in L2_SKU_MASTER - skipping accessory feature lines")
        return pd.DataFrame(feature_lines)
    
    accessory_skus = l2_sku_master[l2_sku_master['IsAccessory'] == True].copy()
    
    if len(accessory_skus) == 0:
        print("  ⚠ No accessories detected in L2_SKU_MASTER (IsAccessory=True)")
        return pd.DataFrame(feature_lines)
    
    # Patch 3: Group accessories by Make and SeriesBucket to create series-specific accessory groups
    for (make, series_bucket), group in accessory_skus.groupby(['Make', 'SeriesBucket']):
        series_bucket_str = str(series_bucket) if pd.notna(series_bucket) and str(series_bucket).strip() else ''
        
        for idx, acc_row in group.iterrows():
            acc_sku = acc_row['OEM_Catalog_No']
            acc_make = acc_row['Make']
            
            # Patch 3: Locked values (as per locked rules)
            # Item_ProductType = "Contactor" (locked)
            # Business_SubCategory = "Power Contactor" (locked)
            acc_product_type = "Contactor"
            acc_subcategory = "Power Contactor"
            
            # Get SC_L4_AccessoryClass if available (from canonical source)
            sc_l4_class = acc_row.get('SC_L4_AccessoryClass', '') if 'SC_L4_AccessoryClass' in acc_row else ''
            if pd.isna(sc_l4_class) or str(sc_l4_class).strip() == '':
                # Fallback: Try to infer from other columns if SC_L4 not available
                acc_product_type_orig = acc_row.get('Item_ProductType', '')
                acc_subcategory_orig = acc_row.get('Business_SubCategory', '')
                product_type_lower = str(acc_product_type_orig).lower()
                subcategory_lower = str(acc_subcategory_orig).lower()
                
                if 'overload' in product_type_lower or 'olr' in product_type_lower or 'overload' in subcategory_lower:
                    sc_l4_class = 'OLR'
                elif 'suppressor' in product_type_lower or 'suppressor' in subcategory_lower:
                    sc_l4_class = 'SUPPRESSOR'
                elif 'interlock' in product_type_lower or 'interlock' in subcategory_lower:
                    sc_l4_class = 'INTERLOCK'
                elif 'aux' in product_type_lower or 'auxiliary' in product_type_lower:
                    sc_l4_class = 'AUX'
                else:
                    sc_l4_class = 'AUX'  # Default
            else:
                sc_l4_class = str(sc_l4_class).strip()
            
            # Patch 3: Create group ID with series bucket if available
            if series_bucket_str:
                group_id = f"GRP-{acc_make}-{series_bucket_str}-ACCESSORIES"
            else:
                group_id = f"GRP-{acc_make}-ACCESSORIES"
            
            # Create FEATURE line in separate accessory group
            # IMPORTANT: Do NOT multiply across duty/voltage - one FEATURE line per accessory SKU
            l1_id = f"L1-{l1_id_counter:06d}"
            
            feature_lines.append({
                'L1_Id': l1_id,
                'L1_Group_Id': group_id,  # Separate accessory group (series-specific if available)
                'L1_Line_Type': 'FEATURE',
                'Parent_Base_L1_Id': '',  # Not linked to base - engineer will map later
                'Feature_Code': sc_l4_class,  # Use SC_L4_AccessoryClass
                'Category': 'Motor Control',  # Default
                'Item_ProductType': acc_product_type,  # LOCKED: "Contactor"
                'GenericLevel': 'L1',
                'GenericDescriptor': acc_product_type,
                'SC_L1_Construction': 'Accessory',  # Non-blank default
                'SC_L2_Operation': '',
                'SC_L3_FeatureClass': '',
                'SC_L4_AccessoryClass': sc_l4_class,
                'L2_OEM_Catalog_No': acc_sku,
                'L2_Make': acc_make,
                'Requested_By_User': '',
                'Notes': 'Accessory - compatibility mapping required',
                'Status': 'ACTIVE'
            })
            l1_id_counter += 1
    
    print(f"✓ Created {len(feature_lines)} L1 FEATURE lines for accessories (in separate groups)")
    return pd.DataFrame(feature_lines)


def create_l1_attributes_kvu(l1_base_lines, l2_sku_master, rating_map):
    """
    Create L1_ATTRIBUTES_KVU table with KVU attributes for each L1 line.
    
    Uses RATING_MAP to populate duty-specific ratings (Current A, kW, HP).
    """
    attributes = []
    
    # Merge L1 with L2 to get SKU info
    l1_with_l2 = l1_base_lines.merge(
        l2_sku_master[['OEM_Catalog_No', 'Make', 'SeriesBucket']],
        left_on='L2_OEM_Catalog_No',
        right_on='OEM_Catalog_No',
        how='left'
    )
    
    # Extract base refs for rating map lookup
    l1_with_l2['Base_Ref'] = l1_with_l2['L2_OEM_Catalog_No'].apply(extract_base_ref_from_sku)
    
    for idx, l1_row in l1_with_l2.iterrows():
        l1_id = l1_row['L1_Id']
        sku = l1_row['L2_OEM_Catalog_No']
        duty = l1_row.get('SC_L3_FeatureClass', '')
        base_ref = l1_row['Base_Ref']
        
        # Extract voltage info
        voltage_value = extract_voltage_from_sku(sku)
        voltage_type = extract_voltage_type_from_sku(sku)
        
        # Add voltage attributes (only if fixed voltage exists)
        if voltage_value is not None:
            attributes.append({
                'L1_Id': l1_id,
                'AttributeCode': 'VOLTAGE',
                'AttributeValue': str(voltage_value),
                'AttributeUnit': 'V',
                'ValueType': 'NUMBER',
                'AppliesToFeature': '',
                'Confidence': 'HIGH',
                'Source': 'L2_SKU'
            })
        
        attributes.append({
            'L1_Id': l1_id,
            'AttributeCode': 'VOLTAGE_TYPE',
            'AttributeValue': voltage_type,
            'AttributeUnit': '',
            'ValueType': 'ENUM',
            'AppliesToFeature': '',
            'Confidence': 'HIGH',
            'Source': 'L2_SKU'
        })
        
        # Add duty-specific ratings from RATING_MAP
        if duty and len(rating_map) > 0:
            rating_row = rating_map[
                (rating_map['Base_Ref'] == base_ref) &
                (rating_map['DutyClass'] == duty)
            ]
            
            if len(rating_row) > 0:
                rating = rating_row.iloc[0]
                
                # Current A
                if pd.notna(rating.get('Current_A')) and rating['Current_A'] != '':
                    attributes.append({
                        'L1_Id': l1_id,
                        'AttributeCode': f'{duty}_CURRENT_A',
                        'AttributeValue': str(rating['Current_A']),
                        'AttributeUnit': 'A',
                        'ValueType': 'NUMBER',
                        'AppliesToFeature': '',
                        'Confidence': 'HIGH',
                        'Source': 'RATING_MAP'
                    })
                
                # kW
                if pd.notna(rating.get('kW')) and rating['kW'] != '':
                    attributes.append({
                        'L1_Id': l1_id,
                        'AttributeCode': f'{duty}_KW',
                        'AttributeValue': str(rating['kW']),
                        'AttributeUnit': 'kW',
                        'ValueType': 'NUMBER',
                        'AppliesToFeature': '',
                        'Confidence': 'HIGH',
                        'Source': 'RATING_MAP'
                    })
                
                # HP
                if pd.notna(rating.get('HP')) and rating['HP'] != '':
                    attributes.append({
                        'L1_Id': l1_id,
                        'AttributeCode': f'{duty}_HP',
                        'AttributeValue': str(rating['HP']),
                        'AttributeUnit': 'HP',
                        'ValueType': 'NUMBER',
                        'AppliesToFeature': '',
                        'Confidence': 'HIGH',
                        'Source': 'RATING_MAP'
                    })
            else:
                # Rating not found in map - add placeholder
                attributes.append({
                    'L1_Id': l1_id,
                    'AttributeCode': f'{duty}_CURRENT_A',
                    'AttributeValue': '',
                    'AttributeUnit': 'A',
                    'ValueType': 'NUMBER',
                    'AppliesToFeature': '',
                    'Confidence': 'REQUIRES_REVIEW',
                    'Source': 'CATALOG'
                })
        elif duty:
            # No rating map - add placeholders
            attributes.append({
                'L1_Id': l1_id,
                'AttributeCode': f'{duty}_CURRENT_A',
                'AttributeValue': '',
                'AttributeUnit': 'A',
                'ValueType': 'NUMBER',
                'AppliesToFeature': '',
                'Confidence': 'REQUIRES_REVIEW',
                'Source': 'CATALOG'
            })
    
    print(f"✓ Created {len(attributes)} L1 attribute rows")
    return pd.DataFrame(attributes)


def main():
    parser = argparse.ArgumentParser(description='Derive L1 Lines from L2 SKU Master')
    parser.add_argument('--l2', required=True, help='Input L2 Excel file (from script A)')
    parser.add_argument('--l1_mode', choices=['duty_x_voltage', 'base_only'], default='duty_x_voltage',
                        help='L1 creation mode (default: duty_x_voltage)')
    parser.add_argument('--include_accessories', type=str, default='true',
                        choices=['true', 'false'],
                        help='Include accessories as FEATURE L1 lines (default: true)')
    parser.add_argument('--out', required=True, help='Output Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NSW Phase-5 Catalog Pipeline v2 - Script B")
    print("Derive L1 Lines from L2")
    print("=" * 60)
    
    # Read L2 data (including RATING_MAP)
    l2_sku_master, l2_price_history, rating_map = read_l2_data(args.l2)
    
    # Create L1 BASE lines
    l1_base_lines = create_l1_base_lines(l2_sku_master, l2_price_history, rating_map, args.l1_mode)
    
    # Create L1 FEATURE lines for accessories (if requested)
    l1_feature_lines = pd.DataFrame()
    if args.include_accessories.lower() == 'true':
        l1_feature_lines = create_l1_feature_lines_for_accessories(l2_sku_master, l1_base_lines)
    
    # Combine BASE and FEATURE lines
    l1_lines = pd.concat([l1_base_lines, l1_feature_lines], ignore_index=True) if len(l1_feature_lines) > 0 else l1_base_lines
    
    # Create L1 attributes (using RATING_MAP)
    l1_attributes_kvu = create_l1_attributes_kvu(l1_base_lines, l2_sku_master, rating_map)
    
    # Write output
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        l1_lines.to_excel(writer, sheet_name='L1_LINES', index=False)
        l1_attributes_kvu.to_excel(writer, sheet_name='L1_ATTRIBUTES_KVU', index=False)
    
    print(f"\n✓ Output written to: {output_path}")
    print(f"  - L1_LINES: {len(l1_lines)} rows ({len(l1_base_lines)} BASE, {len(l1_feature_lines)} FEATURE)")
    print(f"  - L1_ATTRIBUTES_KVU: {len(l1_attributes_kvu)} rows")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
