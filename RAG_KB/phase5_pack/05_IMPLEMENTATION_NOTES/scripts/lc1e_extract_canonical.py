---
Source: tools/catalog_pipeline_v2/scripts/lc1e_extract_canonical.py
KB_Namespace: catalog_pipeline
Status: CANONICAL
Last_Updated: 2025-12-27T19:38:21.456799
KB_Path: phase5_pack/05_IMPLEMENTATION_NOTES/scripts/lc1e_extract_canonical.py
---

#!/usr/bin/env python3
"""
LC1E Series - Extract Canonical Tables from Raw Pricelist

Purpose:
- Reads raw Schneider pricelist XLSX/PDF
- Extracts LC1E tables from Pages 8-10
- Outputs canonical format: LC1E_CANONICAL_ROWS, LC1E_COIL_CODE_PRICES, LC1E_ACCESSORY_SKUS

Rules (LOCKED):
1) L2 SKU = completed OEM catalog number only
2) Completed SKU = BaseRef (strip */#) + CoilCode ONLY when price is numeric
3) AC1 vs AC3 NEVER creates new L2 - creates two L1 BASE lines referencing same L2
4) Accessories are L2 SKUs but keep Item/ProductType = Contactor, Business_SubCategory = Power Contactor, SC_L4 = accessory class
"""

import argparse
import pandas as pd
import sys
import re
from pathlib import Path

# LC1E coil code mapping
LC1E_COIL_CODES = {
    # AC coil codes (Page 8, Page 9 4P)
    'M7': {'voltage': 220, 'voltage_type': 'AC'},
    'N5': {'voltage': 415, 'voltage_type': 'AC'},
    'F7': {'voltage': 110, 'voltage_type': 'AC'},
    'B7': {'voltage': 24, 'voltage_type': 'AC'},
    'M5WB': {'voltage': 220, 'voltage_type': 'AC'},  # 4P variant
    'N5WB': {'voltage': 415, 'voltage_type': 'AC'},  # 4P variant
    # DC coil codes (Page 9 3P DC)
    'BD': {'voltage': 24, 'voltage_type': 'DC'},
}

COIL_SUFFIX_PATTERN = r'(M7|N5|F7|B7|BD|M5WB|N5WB)$'


def normalize_base_ref(sku_ref):
    """Normalize base reference - remove *, #, and coil suffixes."""
    if pd.isna(sku_ref) or str(sku_ref).strip() == '':
        return None, None
    
    sku_str = str(sku_ref).strip()
    
    # Extract coil suffix if present
    match = re.search(COIL_SUFFIX_PATTERN, sku_str)
    suffix_token = match.group(1) if match else None
    
    # Remove coil suffix if found
    if suffix_token:
        sku_str = re.sub(COIL_SUFFIX_PATTERN, '', sku_str)
    
    # Remove trailing stars and #
    sku_str = re.sub(r'\*+$', '', sku_str)
    sku_str = re.sub(r'#$', '', sku_str)
    
    return sku_str.strip(), suffix_token


def has_numeric_price(value):
    """Check if value is a valid numeric price."""
    if pd.isna(value):
        return False
    try:
        price = float(value)
        return price > 0
    except (ValueError, TypeError):
        return False


def extract_lc1e_canonical_rows(xlsx_file):
    """
    Extract LC1E canonical rows from raw pricelist XLSX.
    
    This is a placeholder - will need to be customized based on actual pricelist structure.
    """
    print("⚠ LC1E extraction from raw pricelist requires custom parsing logic")
    print("   This script needs to be customized based on actual pricelist structure")
    print("   For now, returning empty canonical tables")
    
    # Placeholder canonical rows structure
    canonical_rows = []
    coil_code_prices = []
    accessory_skus = []
    
    return pd.DataFrame(canonical_rows), pd.DataFrame(coil_code_prices), pd.DataFrame(accessory_skus)


def main():
    parser = argparse.ArgumentParser(description='LC1E Series - Extract Canonical Tables')
    parser.add_argument('--input_xlsx', required=True, help='Input raw pricelist XLSX file')
    parser.add_argument('--input_pdf', help='Input raw pricelist PDF file (optional)')
    parser.add_argument('--out', required=True, help='Output canonical Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LC1E Series - Extract Canonical Tables")
    print("=" * 60)
    print()
    print("⚠ NOTE: This script requires customization based on actual pricelist structure")
    print("   Pages 8-10 need to be parsed to extract:")
    print("   - Base references with AC1/AC3 ratings")
    print("   - Coil code price columns (M7, N5, F7, B7, BD, M5WB, N5WB)")
    print("   - Accessory SKUs from page 10")
    print()
    print("=" * 60)
    
    # For now, create empty canonical structure as placeholder
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create empty DataFrames with correct structure (as per specification)
    canonical_cols = [
        'source_doc', 'source_page_or_block', 'table_id', 'source_row_id',
        'make', 'series_bucket', 'item_producttype', 'business_subcategory',
        'frame_label', 'poles',
        'ac1_current_a', 'ac3_current_a', 'motor_hp', 'motor_kw',
        'aux_no_count', 'aux_nc_count', 'aux_raw_text',
        'base_ref_raw', 'base_ref_clean',
        'notes_raw'
    ]
    
    coil_price_cols = [
        'base_ref_clean', 'coil_code', 'voltage_type', 'voltage_value',
        'completed_sku', 'price', 'currency',
        'source_page_or_block', 'table_id', 'source_row_id'
    ]
    
    accessory_cols = [
        'make', 'series_bucket',
        'item_producttype',  # LOCK to "Contactor"
        'business_subcategory',  # LOCK to "Power Contactor"
        'sc_l4_accessory_class',
        'oem_catalog_no', 'price', 'currency',
        'compatibility_note',
        'source_page_or_block', 'table_id', 'source_row_id'
    ]
    
    canonical_df = pd.DataFrame(columns=canonical_cols)
    coil_price_df = pd.DataFrame(columns=coil_price_cols)
    accessory_df = pd.DataFrame(columns=accessory_cols)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        canonical_df.to_excel(writer, sheet_name='LC1E_CANONICAL_ROWS', index=False)
        coil_price_df.to_excel(writer, sheet_name='LC1E_COIL_CODE_PRICES', index=False)
        accessory_df.to_excel(writer, sheet_name='LC1E_ACCESSORY_SKUS', index=False)
    
    print(f"✓ Created empty canonical structure: {output_path}")
    print("  Next: Customize extraction logic based on actual pricelist structure")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()


