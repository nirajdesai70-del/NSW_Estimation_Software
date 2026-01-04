---
Source: tools/catalog_pipeline_v2/scripts/build_l2_from_canonical.py
KB_Namespace: catalog_pipeline
Status: CANONICAL
Last_Updated: 2025-12-27T21:47:05.397017
KB_Path: phase5_pack/05_IMPLEMENTATION_NOTES/scripts/build_l2_from_canonical.py
---

#!/usr/bin/env python3
"""
NSW Phase-5 Catalog Pipeline v2 - Script A
Build L2 SKU Master and Price History from Canonical Table

Purpose:
- Reads Schneider_CANONICAL_TABLE_v3.xlsx
- Expands completed OEM catalog numbers (base + coil code suffix)
- Creates L2_SKU_MASTER (distinct SKUs only)
- Creates L2_PRICE_HISTORY (price rows per SKU)

Rules:
- L2 row = distinct (Make + Completed OEM_Catalog_No) present in catalog
- Completed SKU: base reference with '*' must be completed using coil code columns (M7/N7/F7/B7 and BD/FD/MD etc.) ONLY when a numeric price exists
- No combinatorial multiplication - only SKUs with prices
"""

import argparse
import pandas as pd
import sys
import re
from pathlib import Path
from datetime import datetime

# Coil code mapping (AC and DC) - Fixed voltage codes only
COIL_CODE_MAP = {
    # AC coil codes (fixed voltages)
    'F7': {'voltage': 110, 'voltage_type': 'AC', 'voltage_unit': 'V'},
    'M7': {'voltage': 220, 'voltage_type': 'AC', 'voltage_unit': 'V'},
    'N7': {'voltage': 415, 'voltage_type': 'AC', 'voltage_unit': 'V'},
    'B7': {'voltage': 24, 'voltage_type': 'AC', 'voltage_unit': 'V'},
    # LC1E-specific AC coil codes
    'N5': {'voltage': 415, 'voltage_type': 'AC', 'voltage_unit': 'V'},  # LC1E uses N5 for 415V
    'M5': {'voltage': 220, 'voltage_type': 'AC', 'voltage_unit': 'V'},  # LC1E higher frame (verify in raw XLSX)
    'M5WB': {'voltage': 220, 'voltage_type': 'AC', 'voltage_unit': 'V'},  # LC1E 4P variant
    'N5WB': {'voltage': 415, 'voltage_type': 'AC', 'voltage_unit': 'V'},  # LC1E 4P variant
    # DC coil codes (fixed voltages)
    'BD': {'voltage': 24, 'voltage_type': 'DC', 'voltage_unit': 'V'},
    'FD': {'voltage': 110, 'voltage_type': 'DC', 'voltage_unit': 'V'},
    'MD': {'voltage': 220, 'voltage_type': 'DC', 'voltage_unit': 'V'},
    # Low consumption variants (fixed voltages)
    'BL': {'voltage': 24, 'voltage_type': 'DC', 'voltage_unit': 'V'},
    'FL': {'voltage': 110, 'voltage_type': 'DC', 'voltage_unit': 'V'},
    'ML': {'voltage': 220, 'voltage_type': 'DC', 'voltage_unit': 'V'},
    'EL': {'voltage': 48, 'voltage_type': 'DC', 'voltage_unit': 'V'},  # Corrected: EL is 48V
}

# Coil range codes (not fixed voltages - these represent ranges/families)
# BBE, BNE, EHE, KUE are coil range codes, not voltage codes
COIL_RANGE_CODES = ['BBE', 'BNE', 'EHE', 'KUE']

# Coil suffix tokens for regex matching (includes range codes for stripping, but they don't map to voltages)
COIL_SUFFIX_PATTERN = r'(M7|N7|F7|B7|N5|M5|M5WB|N5WB|BD|FD|MD|BL|FL|ML|EL|BBE|BNE|EHE|KUE)$'


def detect_input_mode(df):
    """
    Detect input mode: CANONICAL or RAW.
    
    CANONICAL mode: has sku_code, price_primary (or similar), coil_code
    RAW mode: has M7, N7, F7, BD, FD, MD columns (coil code columns)
    """
    # Check for canonical columns
    has_sku_code = 'sku_code' in df.columns
    has_price_primary = any(col in df.columns for col in ['price_primary', 'price', 'Price', 'Rate', 'list_price'])
    has_coil_code = 'coil_code' in df.columns or 'CoilCode' in df.columns
    
    if has_sku_code and (has_price_primary or has_coil_code):
        return 'CANONICAL'
    
    # Check for RAW mode (coil code columns) - includes LC1E-specific codes
    coil_columns = ['M7', 'N7', 'F7', 'B7', 'N5', 'M5', 'M5WB', 'N5WB', 'BD', 'FD', 'MD']
    has_coil_columns = any(col in df.columns for col in coil_columns)
    
    if has_coil_columns:
        return 'RAW'
    
    # Default to RAW if ambiguous
    return 'RAW'


def read_canonical_table(input_file):
    """Read canonical table Excel file."""
    try:
        # Check if file has L2_STAGING_PRICES sheet (pre-processed L2 format)
        xls = pd.ExcelFile(input_file)
        if 'L2_STAGING_PRICES' in xls.sheet_names:
            print("✓ Found L2_STAGING_PRICES sheet - using pre-processed L2 data")
            df = pd.read_excel(input_file, sheet_name='L2_STAGING_PRICES')
            print(f"✓ Read L2_STAGING_PRICES: {len(df)} rows")
            df['_input_mode'] = 'L2_PREPROCESSED'
            return df
        
        # Otherwise, try to read first sheet
        df = pd.read_excel(input_file, sheet_name=0)
        print(f"✓ Read canonical table: {len(df)} rows")
        
        # Detect input mode
        mode = detect_input_mode(df)
        print(f"✓ Detected input mode: {mode}")
        df['_input_mode'] = mode
        
        return df
    except Exception as e:
        print(f"✗ Error reading canonical table: {e}")
        sys.exit(1)


def normalize_base_ref(sku_ref):
    """
    Normalize base reference using regex.
    
    Removes:
    - Trailing stars: *, **, ****
    - Trailing #
    - Coil suffix tokens if already present (M7/N7/F7/BD/FD/MD/BL/EL/BBE/BNE/EHE/KUE)
    
    Returns:
    - (base_ref_clean, suffix_token) where suffix_token is the detected coil suffix or None
    """
    if pd.isna(sku_ref) or str(sku_ref).strip() == '':
        return None, None
    
    sku_str = str(sku_ref).strip()
    
    # Extract coil suffix if present
    match = re.search(COIL_SUFFIX_PATTERN, sku_str)
    suffix_token = match.group(1) if match else None
    
    # Remove coil suffix if found
    if suffix_token:
        sku_str = re.sub(COIL_SUFFIX_PATTERN, '', sku_str)
    
    # Remove trailing stars (*, **, ****)
    sku_str = re.sub(r'\*+$', '', sku_str)
    
    # Remove trailing #
    sku_str = re.sub(r'#$', '', sku_str)
    
    # Strip whitespace
    sku_str = sku_str.strip()
    
    return sku_str, suffix_token


def complete_sku(base_ref, coil_code):
    """Complete SKU by appending coil code to base reference."""
    base_ref_clean, existing_suffix = normalize_base_ref(base_ref)
    
    if base_ref_clean is None:
        return None
    
    # If coil code is provided and different from existing suffix, append it
    if pd.notna(coil_code) and str(coil_code).strip():
        coil_code = str(coil_code).strip()
        # Only append if not already present
        if not existing_suffix or existing_suffix != coil_code:
            return base_ref_clean + coil_code
    
    # If no coil code but base has suffix, return as-is
    if existing_suffix:
        return base_ref_clean + existing_suffix
    
    return base_ref_clean


def has_numeric_price(price_value):
    """Check if price value is numeric and valid."""
    if pd.isna(price_value):
        return False
    try:
        price = float(price_value)
        return price > 0
    except (ValueError, TypeError):
        return False


def expand_completed_skus(df):
    """
    Expand canonical table rows into completed SKUs.
    
    Supports three modes:
    - L2_PREPROCESSED: Already has completed SKUs in L2_STAGING_PRICES format
    - CANONICAL: Uses sku_code, price_primary, coil_code columns
    - RAW: Uses base reference with coil code columns (M7, N7, F7, etc.)
    """
    expanded_rows = []
    mode = df['_input_mode'].iloc[0] if '_input_mode' in df.columns else 'RAW'
    
    if mode == 'L2_PREPROCESSED':
        # L2_STAGING_PRICES already has completed SKUs - just map to our format
        for idx, row in df.iterrows():
            sku = row.get('OEM_Catalog_No')
            if pd.isna(sku) or str(sku).strip() == '':
                continue
            
            price = row.get('Rate')
            if not has_numeric_price(price):
                continue
            
            # Extract base ref and coil code from SKU
            base_ref_clean, existing_suffix = normalize_base_ref(sku)
            
            new_row = row.copy()
            new_row['Completed_OEM_Catalog_No'] = str(sku).strip()
            new_row['Base_Ref'] = base_ref_clean if base_ref_clean else str(sku).strip()
            new_row['CoilCode'] = existing_suffix if existing_suffix else ''
            new_row['Price'] = float(price)
            
            # Extract voltage from coil code if present
            if existing_suffix and existing_suffix in COIL_CODE_MAP:
                new_row['Voltage'] = COIL_CODE_MAP[existing_suffix]['voltage']
                new_row['VoltageType'] = COIL_CODE_MAP[existing_suffix]['voltage_type']
            elif existing_suffix in COIL_RANGE_CODES:
                new_row['Voltage'] = None
                new_row['VoltageType'] = 'DC' if existing_suffix in ['BBE', 'BNE', 'EHE', 'KUE'] else 'AC'
                new_row['CoilRangeCode'] = existing_suffix
            
            expanded_rows.append(new_row)
        
        expanded_df = pd.DataFrame(expanded_rows)
        print(f"✓ Processed L2_PREPROCESSED: {len(expanded_df)} rows with completed SKUs")
        return expanded_df
    
    # Common coil code column names for RAW mode
    # Patch 1: Added LC1E-specific coil columns
    coil_columns = ['M7', 'N7', 'F7', 'B7', 'N5', 'M5', 'M5WB', 'N5WB', 'BD', 'FD', 'MD', 'BL', 'FL', 'ML', 'EL', 'BBE', 'BNE', 'EHE', 'KUE']
    
    for idx, row in df.iterrows():
        if mode == 'CANONICAL':
            # CANONICAL mode: use sku_code, price_primary, coil_code
            sku_col = None
            for col in ['sku_code', 'SKU', 'OEM_Catalog_No', 'sku']:
                if col in df.columns:
                    sku_col = col
                    break
            
            if not sku_col:
                continue
            
            sku_value = row.get(sku_col)
            if pd.isna(sku_value) or str(sku_value).strip() == '':
                continue
            
            sku_str = str(sku_value).strip()
            base_ref_clean, existing_suffix = normalize_base_ref(sku_str)
            
            # Get coil code
            coil_code_col = None
            for col in ['coil_code', 'CoilCode', 'coil_suffix']:
                if col in df.columns:
                    coil_code_col = col
                    break
            
            coil_code = row.get(coil_code_col) if coil_code_col else existing_suffix
            
            # Get price
            price_col = None
            for col in ['price_primary', 'Price', 'Rate', 'price', 'list_price', 'List_Price']:
                if col in df.columns:
                    price_col = col
                    break
            
            if not price_col:
                continue
            
            price_value = row.get(price_col)
            if not has_numeric_price(price_value):
                continue
            
            # Complete SKU
            if base_ref_clean and coil_code:
                completed_sku = complete_sku(base_ref_clean, coil_code)
            elif existing_suffix:
                completed_sku = base_ref_clean + existing_suffix if base_ref_clean else sku_str
            else:
                completed_sku = base_ref_clean if base_ref_clean else sku_str
            
            if completed_sku:
                new_row = row.copy()
                new_row['Completed_OEM_Catalog_No'] = completed_sku
                new_row['Base_Ref'] = base_ref_clean if base_ref_clean else completed_sku.split(coil_code)[0] if coil_code else completed_sku
                new_row['CoilCode'] = coil_code if pd.notna(coil_code) else (existing_suffix if existing_suffix else '')
                new_row['Price'] = float(price_value)
                
                # Add voltage info (only if it's a fixed voltage code, not a range code)
                if coil_code and coil_code in COIL_CODE_MAP:
                    new_row['Voltage'] = COIL_CODE_MAP[coil_code]['voltage']
                    new_row['VoltageType'] = COIL_CODE_MAP[coil_code]['voltage_type']
                elif coil_code and coil_code in COIL_RANGE_CODES:
                    # Coil range code - don't set fixed voltage, set as range attribute
                    new_row['Voltage'] = None  # No fixed voltage for range codes
                    new_row['VoltageType'] = 'DC' if coil_code in ['BBE', 'BNE', 'EHE', 'KUE'] else 'AC'
                    new_row['CoilRangeCode'] = coil_code  # Store range code separately
                elif 'voltage_value' in df.columns and pd.notna(row.get('voltage_value')):
                    new_row['Voltage'] = int(row.get('voltage_value'))
                    new_row['VoltageType'] = row.get('voltage_type', 'AC') if 'voltage_type' in df.columns else 'AC'
                
                expanded_rows.append(new_row)
        
        else:
            # RAW mode: original logic with coil code columns
            base_ref = None
            for col in ['Base_Reference', 'Reference', 'OEM_Catalog_No', 'SKU', 'Part_Number', 'sku_code']:
                if col in df.columns:
                    base_ref = row.get(col)
                    break
            
            if pd.isna(base_ref) or str(base_ref).strip() == '':
                continue
            
            base_ref_str = str(base_ref).strip()
            base_ref_clean, _ = normalize_base_ref(base_ref_str)
            has_asterisk = '*' in base_ref_str or '#' in base_ref_str
            
            # Check if base reference needs completion
            if has_asterisk or base_ref_clean != base_ref_str:
                # Check each coil code column for prices
                for coil_code in coil_columns:
                    if coil_code in df.columns:
                        price_value = row.get(coil_code)
                        if has_numeric_price(price_value):
                            completed_sku = complete_sku(base_ref_clean, coil_code)
                            if completed_sku:
                                new_row = row.copy()
                                new_row['Completed_OEM_Catalog_No'] = completed_sku
                                new_row['Base_Ref'] = base_ref_clean
                                new_row['CoilCode'] = coil_code
                                new_row['Price'] = float(price_value)
                                if coil_code in COIL_CODE_MAP:
                                    new_row['Voltage'] = COIL_CODE_MAP[coil_code]['voltage']
                                    new_row['VoltageType'] = COIL_CODE_MAP[coil_code]['voltage_type']
                                elif coil_code in COIL_RANGE_CODES:
                                    new_row['Voltage'] = None
                                    new_row['VoltageType'] = 'DC' if coil_code in ['BBE', 'BNE', 'EHE', 'KUE'] else 'AC'
                                    new_row['CoilRangeCode'] = coil_code
                                expanded_rows.append(new_row)
            else:
                # No asterisk - check for price in standard price column
                price_col = None
                for col in ['Price', 'Rate', 'Unit_Price', 'List_Price', 'price_primary']:
                    if col in df.columns:
                        price_col = col
                        break
                
                if price_col and has_numeric_price(row.get(price_col)):
                    new_row = row.copy()
                    new_row['Completed_OEM_Catalog_No'] = base_ref_clean if base_ref_clean else base_ref_str
                    new_row['Base_Ref'] = base_ref_clean if base_ref_clean else base_ref_str
                    new_row['CoilCode'] = ''
                    new_row['Price'] = float(row.get(price_col))
                    expanded_rows.append(new_row)
    
    expanded_df = pd.DataFrame(expanded_rows)
    print(f"✓ Expanded to {len(expanded_df)} rows with completed SKUs")
    return expanded_df


def build_l2_sku_master(expanded_df, source_file_name):
    """Build L2_SKU_MASTER table - distinct (Make + Completed OEM_Catalog_No)."""
    # Determine Make column
    make_col = None
    for col in ['Make', 'Manufacturer', 'Brand', 'make']:
        if col in expanded_df.columns:
            make_col = col
            break
    
    if not make_col:
        # Default to Schneider if not found
        expanded_df['Make'] = 'Schneider'
        make_col = 'Make'
    
    # Get distinct SKUs
    l2_sku_master = expanded_df.groupby([make_col, 'Completed_OEM_Catalog_No']).first().reset_index()
    
    # Try to find series/product type columns
    series_col = None
    for col in ['Series', 'SeriesBucket', 'OEM_Series_Range', 'Product_Series', 'series_bucket', 'series']:
        if col in expanded_df.columns:
            series_col = col
            break
    
    product_type_col = None
    for col in ['Item_ProductType', 'ProductType', 'Item', 'Type', 'item_product_type', 'product_type']:
        if col in expanded_df.columns:
            product_type_col = col
            break
    
    subcategory_col = None
    for col in ['Business_SubCategory', 'SubCategory', 'Sub_Category', 'business_subcategory', 'subcategory']:
        if col in expanded_df.columns:
            subcategory_col = col
            break
    
    # Source lineage columns
    page_col = None
    for col in ['table_id', 'page', 'Page', 'table_id', 'SourcePageOrTableId']:
        if col in expanded_df.columns:
            page_col = col
            break
    
    row_col = None
    for col in ['row', 'Row', 'source_row', 'SourceRow']:
        if col in expanded_df.columns:
            row_col = col
            break
    
    # Build output DataFrame
    result = pd.DataFrame()
    result['Make'] = l2_sku_master[make_col]
    result['OEM_Catalog_No'] = l2_sku_master['Completed_OEM_Catalog_No']
    result['OEM_Series_Range'] = l2_sku_master[series_col].fillna('') if series_col and series_col in l2_sku_master.columns else ''
    result['SeriesBucket'] = l2_sku_master[series_col].fillna('') if series_col and series_col in l2_sku_master.columns else ''
    result['Item_ProductType'] = l2_sku_master[product_type_col].fillna('') if product_type_col and product_type_col in l2_sku_master.columns else ''
    result['Business_SubCategory'] = l2_sku_master[subcategory_col].fillna('') if subcategory_col and subcategory_col in l2_sku_master.columns else ''
    result['UOM'] = 'EA'
    result['IsActive'] = True
    result['SourceFile'] = source_file_name
    result['SourcePageOrTableId'] = l2_sku_master[page_col].fillna('').astype(str) if page_col and page_col in l2_sku_master.columns else ''
    result['SourceRow'] = l2_sku_master[row_col].fillna('').astype(str) if row_col and row_col in l2_sku_master.columns else ''
    result['Notes'] = ''
    
    # Patch 3: Add IsAccessory flag (canonical-tag driven)
    # Set IsAccessory = True if source has SC_L4_AccessoryClass / AccessoryClass / is_accessory / SC_L4 non-empty
    result['IsAccessory'] = False  # Default to False (safer than wrong classification)
    
    accessory_col_candidates = ['SC_L4_AccessoryClass', 'AccessoryClass', 'is_accessory', 'SC_L4', 'sc_l4_accessory_class']
    for acc_col in accessory_col_candidates:
        if acc_col in l2_sku_master.columns:
            # Set IsAccessory=True if column is non-empty (after stripping)
            non_empty_mask = l2_sku_master[acc_col].fillna('').astype(str).str.strip().ne('')
            result.loc[non_empty_mask, 'IsAccessory'] = True
            print(f"✓ Set IsAccessory=True based on column: {acc_col} ({non_empty_mask.sum()} rows)")
            break  # Use first matching column found
    
    print(f"✓ Created L2_SKU_MASTER: {len(result)} distinct SKUs")
    print(f"  - Accessories (IsAccessory=True): {result['IsAccessory'].sum()}")
    return result


def build_l2_price_history(expanded_df, pricelist_ref, effective_from, currency, region, source_file_name):
    """Build L2_PRICE_HISTORY table - price rows per SKU."""
    make_col = None
    for col in ['Make', 'Manufacturer', 'Brand', 'make']:
        if col in expanded_df.columns:
            make_col = col
            break
    
    if not make_col:
        expanded_df['Make'] = 'Schneider'
        make_col = 'Make'
    
    # Source row column
    row_col = None
    for col in ['row', 'Row', 'source_row', 'SourceRow', '_original_index']:
        if col in expanded_df.columns:
            row_col = col
            break
    
    # Create price history rows
    price_rows = []
    for idx, row in expanded_df.iterrows():
        source_row = ''
        if row_col and row_col in row:
            source_row = str(row[row_col])
        elif '_original_index' in row:
            source_row = str(int(row['_original_index']) + 2)  # Excel row (1-based header + row)
        else:
            source_row = str(idx + 2)
        
        price_row = {
            'Make': row[make_col] if make_col in row else 'Schneider',
            'OEM_Catalog_No': row['Completed_OEM_Catalog_No'],
            'PriceListRef': pricelist_ref,
            'EffectiveFrom': effective_from,
            'Currency': currency,
            'Region': region,
            'Rate': row['Price'],
            'ImportBatchId': '',
            'SourceFile': source_file_name,
            'SourceRow': source_row,
            'Notes': ''
        }
        price_rows.append(price_row)
    
    result = pd.DataFrame(price_rows)
    print(f"✓ Created L2_PRICE_HISTORY: {len(result)} price rows")
    return result


def build_rating_map(expanded_df, source_file_name):
    """
    Build RATING_MAP table with duty ratings (AC1/AC3) extracted from canonical table.
    
    Columns:
    - Base_Ref (e.g., LC1D09)
    - DutyClass (AC1 / AC3 / CapacitorDuty)
    - Current_A
    - kW
    - HP
    - Poles
    - Aux_Contacts (if printed)
    - SourcePage/TableId
    - SourceRow
    """
    rating_rows = []
    
    # Store original index for source row tracking
    expanded_df['_original_index'] = expanded_df.index
    
    # Find duty rating columns (common names)
    ac1_current_col = None
    ac3_current_col = None
    for col in expanded_df.columns:
        col_lower = str(col).lower()
        if 'ac1' in col_lower and ('current' in col_lower or 'a' in col_lower):
            ac1_current_col = col
        if 'ac3' in col_lower and ('current' in col_lower or 'a' in col_lower):
            ac3_current_col = col
    
    kw_col = None
    hp_col = None
    poles_col = None
    aux_col = None
    
    for col in expanded_df.columns:
        col_lower = str(col).lower()
        if 'kw' in col_lower and 'ac1' not in col_lower and 'ac3' not in col_lower:
            kw_col = col
        if 'hp' in col_lower and 'ac1' not in col_lower and 'ac3' not in col_lower:
            hp_col = col
        if 'pole' in col_lower:
            poles_col = col
        if 'aux' in col_lower or 'contact' in col_lower:
            aux_col = col
    
    # Source lineage
    page_col = None
    for col in ['table_id', 'page', 'Page', 'table_id', 'SourcePageOrTableId']:
        if col in expanded_df.columns:
            page_col = col
            break
    
    # Group by base reference to extract ratings
    base_ref_col = 'Base_Ref' if 'Base_Ref' in expanded_df.columns else 'Completed_OEM_Catalog_No'
    
    for base_ref, group in expanded_df.groupby(base_ref_col):
        # Get first row from group for base info
        first_row = group.iloc[0]
        
        # Extract AC1 ratings
        if ac1_current_col and ac1_current_col in group.columns:
            ac1_value = first_row.get(ac1_current_col)
            if pd.notna(ac1_value):
                try:
                    ac1_current = float(ac1_value)
                    if ac1_current > 0:
                        rating_row = {
                            'Base_Ref': base_ref,
                            'DutyClass': 'AC1',
                            'Current_A': ac1_current,
                            'kW': float(first_row.get(kw_col)) if kw_col and kw_col in group.columns and pd.notna(first_row.get(kw_col)) else '',
                            'HP': float(first_row.get(hp_col)) if hp_col and hp_col in group.columns and pd.notna(first_row.get(hp_col)) else '',
                            'Poles': str(first_row.get(poles_col)) if poles_col and poles_col in group.columns and pd.notna(first_row.get(poles_col)) else '',
                            'Aux_Contacts': str(first_row.get(aux_col)) if aux_col and aux_col in group.columns and pd.notna(first_row.get(aux_col)) else '',
                            'SourcePageOrTableId': str(first_row.get(page_col)) if page_col and page_col in group.columns and pd.notna(first_row.get(page_col)) else '',
                            'SourceRow': str(int(first_row['_original_index']) + 2) if '_original_index' in first_row else ''
                        }
                        rating_rows.append(rating_row)
                except (ValueError, TypeError):
                    pass
        
        # Extract AC3 ratings
        if ac3_current_col and ac3_current_col in group.columns:
            ac3_value = first_row.get(ac3_current_col)
            if pd.notna(ac3_value):
                try:
                    ac3_current = float(ac3_value)
                    if ac3_current > 0:
                        rating_row = {
                            'Base_Ref': base_ref,
                            'DutyClass': 'AC3',
                            'Current_A': ac3_current,
                            'kW': float(first_row.get(kw_col)) if kw_col and kw_col in group.columns and pd.notna(first_row.get(kw_col)) else '',
                            'HP': float(first_row.get(hp_col)) if hp_col and hp_col in group.columns and pd.notna(first_row.get(hp_col)) else '',
                            'Poles': str(first_row.get(poles_col)) if poles_col and poles_col in group.columns and pd.notna(first_row.get(poles_col)) else '',
                            'Aux_Contacts': str(first_row.get(aux_col)) if aux_col and aux_col in group.columns and pd.notna(first_row.get(aux_col)) else '',
                            'SourcePageOrTableId': str(first_row.get(page_col)) if page_col and page_col in group.columns and pd.notna(first_row.get(page_col)) else '',
                            'SourceRow': str(int(first_row['_original_index']) + 2) if '_original_index' in first_row else ''
                        }
                        rating_rows.append(rating_row)
                except (ValueError, TypeError):
                    pass
    
    result = pd.DataFrame(rating_rows)
    print(f"✓ Created RATING_MAP: {len(result)} rating rows")
    return result


def main():
    parser = argparse.ArgumentParser(description='Build L2 SKU Master and Price History from Canonical Table')
    parser.add_argument('--input', required=True, help='Input canonical table Excel file')
    parser.add_argument('--pricelist_ref', required=True, help='Price list reference (e.g., "WEF 15 Jul 2025")')
    parser.add_argument('--effective_from', required=True, help='Effective from date (YYYY-MM-DD)')
    parser.add_argument('--currency', default='INR', help='Currency code (default: INR)')
    parser.add_argument('--region', default='INDIA', help='Region (default: INDIA)')
    parser.add_argument('--out', required=True, help='Output Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NSW Phase-5 Catalog Pipeline v2 - Script A")
    print("Build L2 from Canonical Table")
    print("=" * 60)
    
    # Read canonical table
    df = read_canonical_table(args.input)
    
    # Store original index for source row tracking
    df['_original_index'] = df.index
    
    # Get source file name
    source_file_name = Path(args.input).name
    
    # Expand completed SKUs
    expanded_df = expand_completed_skus(df)
    
    if len(expanded_df) == 0:
        print("✗ Error: No completed SKUs found. Check input file format.")
        sys.exit(1)
    
    # Build L2 tables
    l2_sku_master = build_l2_sku_master(expanded_df, source_file_name)
    l2_price_history = build_l2_price_history(
        expanded_df, args.pricelist_ref, args.effective_from, args.currency, args.region, source_file_name
    )
    
    # Build RATING_MAP
    rating_map = build_rating_map(expanded_df, source_file_name)
    
    # Write output
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        l2_sku_master.to_excel(writer, sheet_name='L2_SKU_MASTER', index=False)
        l2_price_history.to_excel(writer, sheet_name='L2_PRICE_HISTORY', index=False)
        rating_map.to_excel(writer, sheet_name='RATING_MAP', index=False)
    
    print(f"\n✓ Output written to: {output_path}")
    print(f"  - L2_SKU_MASTER: {len(l2_sku_master)} rows")
    print(f"  - L2_PRICE_HISTORY: {len(l2_price_history)} rows")
    print(f"  - RATING_MAP: {len(rating_map)} rows")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()

