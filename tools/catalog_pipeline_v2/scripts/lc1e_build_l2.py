#!/usr/bin/env python3
"""
LC1E Series - Build L2 SKU Master, Price History, and RATING_MAP from Canonical

Purpose:
- Reads LC1E canonical tables (LC1E_CANONICAL_ROWS, LC1E_COIL_CODE_PRICES, LC1E_ACCESSORY_SKUS)
- Builds L2_SKU_MASTER (completed SKUs only)
- Builds L2_PRICE_HISTORY (price rows)
- Builds RATING_MAP (AC1/AC3 ratings from canonical rows)
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Import shared functions from main pipeline
sys.path.insert(0, str(Path(__file__).parent.parent))
from build_l2_from_canonical import (
    normalize_base_ref, has_numeric_price, COIL_CODE_MAP, COIL_RANGE_CODES
)


def read_lc1e_canonical(canonical_file):
    """Read LC1E canonical tables."""
    try:
        canonical_rows = pd.read_excel(canonical_file, sheet_name='LC1E_CANONICAL_ROWS')
        coil_code_prices = pd.read_excel(canonical_file, sheet_name='LC1E_COIL_CODE_PRICES')
        
        # Accessory SKUs sheet may be empty
        try:
            accessory_skus = pd.read_excel(canonical_file, sheet_name='LC1E_ACCESSORY_SKUS')
        except:
            accessory_skus = pd.DataFrame()
        
        print(f"✓ Read LC1E canonical:")
        print(f"  - LC1E_CANONICAL_ROWS: {len(canonical_rows)} rows")
        print(f"  - LC1E_COIL_CODE_PRICES: {len(coil_code_prices)} rows")
        print(f"  - LC1E_ACCESSORY_SKUS: {len(accessory_skus)} rows")
        
        return canonical_rows, coil_code_prices, accessory_skus
    except Exception as e:
        print(f"✗ Error reading LC1E canonical: {e}")
        sys.exit(1)


def build_l2_sku_master_from_coil_prices(coil_code_prices, accessory_skus, source_file_name):
    """Build L2_SKU_MASTER from LC1E_COIL_CODE_PRICES and accessories."""
    l2_rows = []
    
    # Process coil code prices (base contactors)
    for idx, row in coil_code_prices.iterrows():
        sku = row.get('completed_sku')
        if pd.isna(sku) or str(sku).strip() == '':
            continue
        
        l2_row = {
            'Make': 'Schneider',
            'OEM_Catalog_No': str(sku).strip(),
            'OEM_Series_Range': 'Easy TeSys',
            'SeriesBucket': 'LC1E',
            'Item_ProductType': 'Contactor',
            'Business_SubCategory': 'Power Contactor',
            'UOM': 'EA',
            'IsActive': True,
            'SourceFile': source_file_name,
            'SourcePageOrTableId': str(row.get('table_id', '')),
            'SourceRow': str(row.get('source_row_id', '')),
            'Notes': ''
        }
        l2_rows.append(l2_row)
    
    # Process accessory SKUs
    for idx, row in accessory_skus.iterrows():
        sku = row.get('oem_catalog_no')
        if pd.isna(sku) or str(sku).strip() == '':
            continue
        
        l2_row = {
            'Make': row.get('make', 'Schneider'),
            'OEM_Catalog_No': str(sku).strip(),
            'OEM_Series_Range': 'Easy TeSys',
            'SeriesBucket': row.get('series_bucket', 'LC1E'),
            'Item_ProductType': row.get('item_producttype', 'Contactor'),
            'Business_SubCategory': row.get('business_subcategory', 'Power Contactor'),
            'UOM': 'EA',
            'IsActive': True,
            'SourceFile': source_file_name,
            'SourcePageOrTableId': str(row.get('table_id', '')),
            'SourceRow': '',
            'Notes': f"Accessory: {row.get('sc_l4_accessory_class', '')}"
        }
        l2_rows.append(l2_row)
    
    result = pd.DataFrame(l2_rows)
    # Remove duplicates (same Make + OEM_Catalog_No)
    result = result.drop_duplicates(subset=['Make', 'OEM_Catalog_No'], keep='first')
    
    print(f"✓ Created L2_SKU_MASTER: {len(result)} distinct SKUs")
    return result


def build_l2_price_history_from_coil_prices(coil_code_prices, accessory_skus, pricelist_ref, effective_from, currency, region, source_file_name):
    """Build L2_PRICE_HISTORY from LC1E_COIL_CODE_PRICES and accessories."""
    price_rows = []
    
    # Process coil code prices
    for idx, row in coil_code_prices.iterrows():
        sku = row.get('completed_sku')
        price = row.get('price')
        if pd.isna(sku) or not has_numeric_price(price):
            continue
        
        price_row = {
            'Make': 'Schneider',
            'OEM_Catalog_No': str(sku).strip(),
            'PriceListRef': pricelist_ref,
            'EffectiveFrom': effective_from,
            'Currency': currency,
            'Region': region,
            'Rate': float(price),
            'ImportBatchId': '',
            'SourceFile': source_file_name,
            'SourceRow': str(row.get('source_row_id', '')),
            'Notes': ''
        }
        price_rows.append(price_row)
    
    # Process accessory SKUs
    for idx, row in accessory_skus.iterrows():
        sku = row.get('oem_catalog_no')
        price = row.get('price')
        if pd.isna(sku) or not has_numeric_price(price):
            continue
        
        price_row = {
            'Make': row.get('make', 'Schneider'),
            'OEM_Catalog_No': str(sku).strip(),
            'PriceListRef': pricelist_ref,
            'EffectiveFrom': effective_from,
            'Currency': currency,
            'Region': region,
            'Rate': float(price),
            'ImportBatchId': '',
            'SourceFile': source_file_name,
            'SourceRow': '',
            'Notes': ''
        }
        price_rows.append(price_row)
    
    result = pd.DataFrame(price_rows)
    print(f"✓ Created L2_PRICE_HISTORY: {len(result)} price rows")
    return result


def build_rating_map_from_canonical(canonical_rows, source_file_name):
    """Build RATING_MAP from LC1E_CANONICAL_ROWS."""
    rating_rows = []
    
    for idx, row in canonical_rows.iterrows():
        base_ref = row.get('base_ref')
        if pd.isna(base_ref) or str(base_ref).strip() == '':
            continue
        
        base_ref_clean = str(base_ref).strip()
        
        # Extract AC1 ratings
        ac1_current = row.get('ac1_current_a')
        if pd.notna(ac1_current):
            try:
                ac1_current_val = float(ac1_current)
                if ac1_current_val > 0:
                    rating_row = {
                        'Base_Ref': base_ref_clean,
                        'DutyClass': 'AC1',
                        'Current_A': ac1_current_val,
                        'kW': float(row.get('motor_kw')) if pd.notna(row.get('motor_kw')) else '',
                        'HP': float(row.get('motor_hp')) if pd.notna(row.get('motor_hp')) else '',
                        'Poles': str(row.get('poles')) if pd.notna(row.get('poles')) else '',
                        'Aux_Contacts': str(row.get('aux_raw_text')) if pd.notna(row.get('aux_raw_text')) else '',
                        'SourcePageOrTableId': str(row.get('table_id')) if pd.notna(row.get('table_id')) else '',
                        'SourceRow': str(row.get('source_row_id')) if pd.notna(row.get('source_row_id')) else ''
                    }
                    rating_rows.append(rating_row)
            except (ValueError, TypeError):
                pass
        
        # Extract AC3 ratings
        ac3_current = row.get('ac3_current_a')
        if pd.notna(ac3_current):
            try:
                ac3_current_val = float(ac3_current)
                if ac3_current_val > 0:
                    rating_row = {
                        'Base_Ref': base_ref_clean,
                        'DutyClass': 'AC3',
                        'Current_A': ac3_current_val,
                        'kW': float(row.get('motor_kw')) if pd.notna(row.get('motor_kw')) else '',
                        'HP': float(row.get('motor_hp')) if pd.notna(row.get('motor_hp')) else '',
                        'Poles': str(row.get('poles')) if pd.notna(row.get('poles')) else '',
                        'Aux_Contacts': str(row.get('aux_raw_text')) if pd.notna(row.get('aux_raw_text')) else '',
                        'SourcePageOrTableId': str(row.get('table_id')) if pd.notna(row.get('table_id')) else '',
                        'SourceRow': str(row.get('source_row_id')) if pd.notna(row.get('source_row_id')) else ''
                    }
                    rating_rows.append(rating_row)
            except (ValueError, TypeError):
                pass
    
    result = pd.DataFrame(rating_rows)
    print(f"✓ Created RATING_MAP: {len(result)} rating rows")
    return result


def main():
    parser = argparse.ArgumentParser(description='LC1E Series - Build L2 from Canonical')
    parser.add_argument('--canonical', required=True, help='Input LC1E canonical Excel file')
    parser.add_argument('--pricelist_ref', required=True, help='Price list reference')
    parser.add_argument('--effective_from', required=True, help='Effective from date (YYYY-MM-DD)')
    parser.add_argument('--currency', default='INR', help='Currency code')
    parser.add_argument('--region', default='INDIA', help='Region')
    parser.add_argument('--out', required=True, help='Output Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LC1E Series - Build L2 from Canonical")
    print("=" * 60)
    
    # Read canonical tables
    canonical_rows, coil_code_prices, accessory_skus = read_lc1e_canonical(args.canonical)
    
    # Get source file name
    source_file_name = Path(args.canonical).name
    
    # Build L2 tables
    l2_sku_master = build_l2_sku_master_from_coil_prices(coil_code_prices, accessory_skus, source_file_name)
    l2_price_history = build_l2_price_history_from_coil_prices(
        coil_code_prices, accessory_skus, args.pricelist_ref, args.effective_from,
        args.currency, args.region, source_file_name
    )
    rating_map = build_rating_map_from_canonical(canonical_rows, source_file_name)
    
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


