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

🔒 SEMANTIC FREEZE REFERENCE:
- Page-8 semantics are FROZEN in: archives/schneider/LC1E/2025-07-15_WEF/04_docs/LC1E_PAGE8_SEMANTIC_FREEZE.md
- HP semantics: HP is engineering attribute (like kW), NOT a variant, stored only at L1, duty-independent
- Frame: Stateful carry-forward (not row-local)
- BaseRef: Normalize by removing *, #, trailing spaces
- Duty: AC1/AC3 create two L1 rows, same HP/kW for both
- Do NOT re-interpret Page-8. Follow freeze document verbatim.
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
    'M5': {'voltage': 220, 'voltage_type': 'AC'},  # Higher frame variant
    'N7': {'voltage': 415, 'voltage_type': 'AC'},  # Higher frame variant
    # DC coil codes (Page 9 3P DC)
    'BD': {'voltage': 24, 'voltage_type': 'DC'},
}

# All coil codes to search for in headers
ALL_COIL_CODES = ['M7', 'N5', 'BD', 'B7', 'F7', 'M5WB', 'N5WB', 'M5', 'N7']

# Base reference pattern (defined here for use in functions)
BASE_REF_PATTERN = re.compile(r'(LC1E[0-9A-Z]+\*+\s*IN|LC1E[0-9A-Z]+\*+|LC1E[0-9A-Z]+)', re.IGNORECASE)

COIL_SUFFIX_PATTERN = r'(M7|N5|F7|B7|BD|M5WB|N5WB|M5|N7)$'


def infer_frame_from_base_ref(base_ref):
    """
    Infer frame label from LC1E base reference pattern.
    
    NOTE: This is a fallback when FRAME- rows are not found in source.
    The actual frame should come from source XLSX FRAME- rows (frame carry-forward).
    
    Frame mapping (from source XLSX analysis):
    - LC1E0601-2510: FRAME-1 (typically, but check source)
    - LC1E3201-40B10: FRAME-2 (typically, but check source)
    - LC1E40, LC1E50, LC1E65: FRAME-3 (from source)
    - LC1E80, LC1E95: FRAME-4 (from source - user noted missing)
    - LC1E120, LC1E160: FRAME-5 (from source)
    - LC1E200, LC1E250: FRAME-6 (from source)
    - LC1E300, LC1E400: FRAME-7 (from source)
    - LC1E500: FRAME-8 (from source)
    - LC1E630: FRAME-9 (from source)
    
    IMPORTANT: This function should only be used as fallback.
    Primary source of truth is FRAME- rows in source XLSX.
    """
    if not base_ref or pd.isna(base_ref):
        return ''
    
    base_str = str(base_ref).strip().upper()
    
    # Handle non-numeric patterns first (LC1E40, LC1E50, etc.)
    # These are from source XLSX FRAME- rows
    if base_str in ['LC1E40', 'LC1E50', 'LC1E65']:
        return 'FRAME-3'
    elif base_str in ['LC1E80', 'LC1E95']:
        return 'FRAME-4'  # User noted these are FRAME-4, not FRAME-3
    elif base_str in ['LC1E120', 'LC1E160']:
        return 'FRAME-5'
    elif base_str in ['LC1E200', 'LC1E250']:
        return 'FRAME-6'
    elif base_str in ['LC1E300', 'LC1E400']:
        return 'FRAME-7'
    elif base_str == 'LC1E500':
        return 'FRAME-8'
    elif base_str == 'LC1E630':
        return 'FRAME-9'
    
    # Extract numeric part
    num_match = re.search(r'LC1E(\d+)', base_str)
    if not num_match:
        return ''
    
    num = int(num_match.group(1))
    
    # Frame mapping based on numeric range (from source XLSX)
    # Note: This is approximate - actual frames should come from source
    if 601 <= num <= 2510:
        return 'FRAME-1'
    elif 3201 <= num <= 4010 or '40B' in base_str:
        return 'FRAME-2'
    else:
        # Fallback: try to infer from first digits
        first_digits = num // 100
        if first_digits == 6:
            return 'FRAME-1'
        elif first_digits == 9:
            return 'FRAME-1'
        elif first_digits == 12:
            return 'FRAME-1'
        elif first_digits == 18:
            return 'FRAME-1'
        elif first_digits == 25:
            return 'FRAME-1'
        elif first_digits == 32:
            return 'FRAME-2'
        elif first_digits == 38:
            return 'FRAME-2'
        elif first_digits == 40:
            return 'FRAME-2'
    
    return ''


def normalize_base_ref(sku_ref):
    """Normalize base reference - remove *, #, spaces, and coil suffixes."""
    if pd.isna(sku_ref) or str(sku_ref).strip() == '':
        return None
    
    sku_str = str(sku_ref).strip()
    
    # Remove trailing stars, #, and spaces
    sku_str = re.sub(r'\*+\s*$', '', sku_str)
    sku_str = re.sub(r'#+\s*$', '', sku_str)
    sku_str = sku_str.strip()
    
    # Extract coil suffix if present and remove it
    match = re.search(COIL_SUFFIX_PATTERN, sku_str)
    if match:
        sku_str = re.sub(COIL_SUFFIX_PATTERN, '', sku_str).strip()
    
    return sku_str if sku_str else None


def has_numeric_price(value):
    """Check if value is a valid numeric price."""
    if pd.isna(value):
        return False
    try:
        price = float(value)
        return price > 0
    except (ValueError, TypeError):
        return False


def normalize_row_to_string(row):
    """Normalize a row to a single string for pattern matching."""
    return ' '.join([str(v) if pd.notna(v) else '' for v in row])


def find_coil_header_row(df, start_row, end_row):
    """
    Find header row that contains coil code labels.
    Returns (header_row_idx, coil_label_to_col_map) or (None, None)
    """
    for idx in range(start_row, min(end_row, len(df))):
        row = df.iloc[idx]
        row_str = normalize_row_to_string(row)
        
        # Check if this row contains coil code labels
        coil_col_map = {}
        for col_idx, val in enumerate(row):
            if pd.notna(val):
                val_str = str(val).strip().upper()
                # Check for coil codes (exact match or with voltage in parentheses)
                for coil_code in ALL_COIL_CODES:
                    if coil_code.upper() in val_str or f"{coil_code} (" in val_str.upper():
                        coil_col_map[coil_code] = col_idx
                        break
        
        if coil_col_map:
            return idx, coil_col_map
    
    return None, None


def extract_current_value(cell_value):
    """Extract numeric current value from cell (e.g., '20 A' -> 20)."""
    if pd.isna(cell_value):
        return None
    val_str = str(cell_value).strip()
    # Extract number before 'A' or space
    match = re.search(r'(\d+(?:\.\d+)?)', val_str)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None


def extract_numeric_value(cell_value):
    """Extract numeric value from cell."""
    if pd.isna(cell_value):
        return None
    try:
        val = float(cell_value)
        return val if val > 0 else None
    except (ValueError, TypeError):
        return None

# Helper to parse kW range values (e.g., "25/30" -> 25, "22/37" -> 22)
# FROZEN RULE: Use minimum value for ranges (LC1E_PAGE8_SEMANTIC_FREEZE.md)
def parse_kw_range(cell_value):
    """Parse kW values that may be ranges like 25/30. Returns (min_value, range_note)."""
    if pd.isna(cell_value): return None, None
    val_str = str(cell_value).strip()
    # Check for range pattern (e.g., "25/30", "22/37")
    range_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', val_str)
    if range_match:
        min_val = float(range_match.group(1))
        max_val = float(range_match.group(2))
        return min_val, f"KW_RANGE={min_val}/{max_val}; motor_kw=min={min_val}"  # Store min, note the range
    # Try regular numeric
    try:
        val = float(val_str)
        return val if val > 0 else None, None
    except (ValueError, TypeError):
        return None, None

# Helper to parse HP range values (e.g., "25/30" -> 25)
# FROZEN RULE: HP uses minimum value for ranges, same as kW (LC1E_PAGE8_SEMANTIC_FREEZE.md)
def parse_hp_range(cell_value):
    """Parse HP values that may be ranges like 25/30. Returns (min_value, range_note)."""
    if pd.isna(cell_value): return None, None
    val_str = str(cell_value).strip()
    # Check for range pattern (e.g., "25/30", "22/37")
    range_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', val_str)
    if range_match:
        min_val = float(range_match.group(1))
        max_val = float(range_match.group(2))
        return min_val, f"HP_RANGE={min_val}/{max_val}; motor_hp=min={min_val}"  # Store min, note the range
    # Try regular numeric
    try:
        val = float(val_str)
        return val if val > 0 else None, None
    except (ValueError, TypeError):
        return None, None

# Helper to parse aux contacts from text (e.g., "4NO", "2NO + 2NC")
def parse_aux_contacts(cell_value):
    """Parse aux contact strings. Returns (no_count, nc_count)."""
    if pd.isna(cell_value): return None, None
    val_str = str(cell_value).strip().upper()
    no_count = None
    nc_count = None
    
    # Pattern: "4NO" or "2NO + 2NC" or "1NO+1NC"
    no_match = re.search(r'(\d+)\s*NO', val_str)
    if no_match:
        no_count = int(no_match.group(1))
    
    nc_match = re.search(r'(\d+)\s*NC', val_str)
    if nc_match:
        nc_count = int(nc_match.group(1))
    
    return no_count, nc_count


def extract_lc1e_canonical_rows(xlsx_file):
    """
    Extract LC1E canonical rows from raw pricelist XLSX using section-driven parsing.
    """
    print("=" * 80)
    print("LC1E Canonical Extraction - Section-Driven Parsing")
    print("=" * 80)
    print()
    
    # Load raw grid (no header)
    df = pd.read_excel(xlsx_file, sheet_name=0, header=None)
    print(f"✓ Loaded sheet: {len(df)} rows, {len(df.columns)} columns")
    print()
    
    canonical_rows = []
    coil_code_prices = []
    accessory_skus = []
    
    # Track sections found
    sections_found = []
    
    # SECTION A: LC1E 3P AC Control
    print("Searching for Section A: LC1E 3P AC Control...")
    section_a_start = None
    
    for idx in range(len(df)):
        row_str = normalize_row_to_string(df.iloc[idx])
        # Look for LC1E 3P AC section markers
        if (('Power Contactors LC1E' in row_str or 'LC1E' in row_str) and 
            ('3 Pole AC' in row_str or '3P' in row_str or 'AC Control' in row_str)) or \
           (('Rated Operational' in row_str or 'Motor Power' in row_str) and 
            'LC1E' in normalize_row_to_string(df.iloc[max(0, idx-5):idx+1])):
            # Check if this section has M7/N5 in nearby rows
            for check_idx in range(idx, min(idx + 20, len(df))):
                check_str = normalize_row_to_string(df.iloc[check_idx])
                if 'M7' in check_str or 'N5' in check_str:
                    section_a_start = idx
                    print(f"  ✓ Found Section A start at row {idx}")
                    break
            if section_a_start:
                break
    
    if section_a_start:
        # Find header row and extract data
        header_row, coil_map = find_coil_header_row(df, section_a_start, min(section_a_start + 50, len(df)))
        if header_row and coil_map:
            print(f"  ✓ Found header at row {header_row}, coil columns: {coil_map}")
            
            # Track current frame label
            current_frame_label = ''
            
            # Build frame-to-base-ref mapping from source (for better accuracy)
            # Scan ahead to find all FRAME- rows and their associated base refs
            frame_base_ref_map = {}
            temp_frame = None
            for scan_idx in range(header_row + 1, min(header_row + 300, len(df))):
                scan_row = df.iloc[scan_idx]
                scan_row_str = normalize_row_to_string(scan_row)
                
                # Check for FRAME- label
                frame_match = re.search(r'FRAME-[\dA-Z]+', scan_row_str, re.IGNORECASE)
                if frame_match:
                    temp_frame = frame_match.group(0).upper()
                    if temp_frame not in frame_base_ref_map:
                        frame_base_ref_map[temp_frame] = []
                
                # If we have a frame, look for base refs in nearby rows (within 10 rows)
                if temp_frame:
                    base_match = BASE_REF_PATTERN.search(scan_row_str)
                    if base_match:
                        base_ref_raw = base_match.group(1)
                        base_ref_clean = normalize_base_ref(base_ref_raw)
                        if base_ref_clean and base_ref_clean not in frame_base_ref_map[temp_frame]:
                            frame_base_ref_map[temp_frame].append(base_ref_clean)
            
            # Next section markers (proper section boundaries)
            NEXT_SECTION_MARKERS = [
                '3 Pole DC Control', '3P DC', 'DC Control',
                '4 Pole', '4P',
                'Control Relays', 'Spare Coil',
                'Accessories - For', 'Mechanical Interlock'
            ]
            
            # Extract data rows until next major section
            for data_idx in range(header_row + 1, min(header_row + 200, len(df))):
                row = df.iloc[data_idx]
                row_str = normalize_row_to_string(row)
                
                # Skip FRAME- rows (separators, not section boundaries)
                if 'FRAME-' in row_str:
                    # Extract frame label for subsequent rows
                    frame_match = re.search(r'FRAME-[\dA-Z]+', row_str, re.IGNORECASE)
                    if frame_match:
                        current_frame_label = frame_match.group(0).upper()
                    continue  # Skip separator row, don't break
                
                # Check if we hit next section (proper boundary)
                if any(marker.lower() in row_str.lower() for marker in NEXT_SECTION_MARKERS):
                    break
                
                # Find base reference in any column
                base_ref_raw = None
                base_ref_clean = None
                
                for col_idx in range(min(80, len(row))):
                    val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                    if pd.notna(val):
                        val_str = str(val).strip()
                        base_match = BASE_REF_PATTERN.search(val_str)
                        if base_match:
                            base_ref_raw = base_match.group(1)
                            base_ref_clean = normalize_base_ref(base_ref_raw)
                            break
                
                if base_ref_clean:
                    # CRITICAL: Only accept row if at least one coil price is numeric AND >= 100 (contactor threshold)
                    priced_rows = []
                    
                    for coil_code, col_idx in coil_map.items():
                        if col_idx < len(row):
                            price_val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                            price = extract_numeric_value(price_val)
                            
                            # Contactor price threshold: >= 100 (filters out 4/3/2 bug values)
                            if price and price >= 100:
                                priced_rows.append({
                                    'coil_code': coil_code,
                                    'price': price,
                                    'col_idx': col_idx
                                })
                    
                    # Skip row if no valid priced coil codes found (prevents range-text pollution)
                    if not priced_rows:
                        continue
                    
                    # Extract ratings (best effort - look for AC1/AC3/HP/kW patterns)
                    ac1_current = None
                    ac3_current = None
                    hp = None
                    kw = None
                    no_count = None
                    nc_count = None
                    
                    # Get header row for context
                    header_str = normalize_row_to_string(df.iloc[header_row])
                    
                    # Try to find AC1/AC3/HP/kW/NO/NC in row cells
                    for col_idx in range(min(80, len(row))):
                        val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                        if pd.notna(val):
                            val_str = str(val).strip()
                            
                            # Check header context for this column
                            header_val = df.iloc[header_row].iloc[col_idx] if col_idx < len(df.iloc[header_row]) else None
                            header_val_str = str(header_val).upper() if pd.notna(header_val) else ''
                            
                            # AC1 current
                            if 'AC-1' in header_val_str or 'AC1' in header_val_str:
                                ac1_current = extract_current_value(val)
                            # AC3 current
                            elif 'AC-3' in header_val_str or 'AC3' in header_val_str:
                                ac3_current = extract_current_value(val)
                            # HP (handle ranges like 25/30 - use minimum per frozen rules)
                            elif 'HP' in header_val_str:
                                hp, hp_range_note = parse_hp_range(val)
                            # kW (handle ranges like 25/30)
                            elif 'KW' in header_val_str or 'kW' in header_val_str:
                                kw, kw_range_note = parse_kw_range(val)
                                if kw_range_note:
                                    # Store range note in notes_raw (will be set later)
                                    pass  # We'll handle this in canonical row append
                            # NO aux (try numeric first, then parse text)
                            elif 'NO' in header_val_str and col_idx not in coil_map.values():
                                no_val = extract_numeric_value(val)
                                if no_val is not None:
                                    no_count = int(no_val)
                                else:
                                    # Try parsing from text (e.g., "4NO")
                                    parsed_no, _ = parse_aux_contacts(val)
                                    if parsed_no is not None:
                                        no_count = parsed_no
                            # NC aux (try numeric first, then parse text)
                            elif 'NC' in header_val_str and col_idx not in coil_map.values():
                                nc_val = extract_numeric_value(val)
                                if nc_val is not None:
                                    nc_count = int(nc_val)
                                else:
                                    # Try parsing from text (e.g., "2NC")
                                    _, parsed_nc = parse_aux_contacts(val)
                                    if parsed_nc is not None:
                                        nc_count = parsed_nc
                    
                    # Collect range notes if present (HP and kW) - FROZEN RULE: use minimum for ranges
                    hp_range_note = None
                    kw_range_note = None
                    for col_idx in range(min(80, len(row))):
                        val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                        if pd.notna(val):
                            header_val = df.iloc[header_row].iloc[col_idx] if col_idx < len(df.iloc[header_row]) else None
                            header_val_str = str(header_val).upper() if pd.notna(header_val) else ''
                            if 'HP' in header_val_str:
                                _, note = parse_hp_range(val)
                                if note:
                                    hp_range_note = note
                            elif 'KW' in header_val_str or 'kW' in header_val_str:
                                _, note = parse_kw_range(val)
                                if note:
                                    kw_range_note = note
                    
                    # Combine range notes
                    range_notes = []
                    if hp_range_note:
                        range_notes.append(hp_range_note)
                    if kw_range_note:
                        range_notes.append(kw_range_note)
                    combined_notes = '; '.join(range_notes) if range_notes else ''
                    
                    # Extract coil prices (only for priced coils found above)
                    for coil_price_info in priced_rows:
                        coil_code = coil_price_info['coil_code']
                        price = coil_price_info['price']
                        completed_sku = f"{base_ref_clean}{coil_code}"
                        coil_code_prices.append({
                            'base_ref_clean': base_ref_clean,
                            'coil_code': coil_code,
                            'voltage_type': LC1E_COIL_CODES.get(coil_code, {}).get('voltage_type', 'AC'),
                            'voltage_value': LC1E_COIL_CODES.get(coil_code, {}).get('voltage', None),
                            'completed_sku': completed_sku,
                            'price': price,
                            'currency': 'INR',
                            'source_page_or_block': 'Table 1',
                            'table_id': 'LC1E_3P_AC',
                            'source_row_id': str(data_idx + 1)
                        })
                    
                    # Determine frame label: 
                    # 1. First try: Look up in frame_base_ref_map (from source)
                    # 2. Second try: Use current_frame_label (from FRAME- rows)
                    # 3. Fallback: Infer from base_ref pattern
                    frame_label = ''
                    for frame, base_refs in frame_base_ref_map.items():
                        if base_ref_clean in base_refs:
                            frame_label = frame
                            break
                    
                    if not frame_label:
                        frame_label = current_frame_label if current_frame_label else infer_frame_from_base_ref(base_ref_clean)
                    
                    # Add canonical row (once per base_ref)
                    # FROZEN RULE: HP and kW are duty-independent, same for AC1 and AC3
                    canonical_rows.append({
                        'source_doc': xlsx_file,
                        'source_page_or_block': 'Table 1',
                        'table_id': 'LC1E_3P_AC',
                        'source_row_id': str(data_idx + 1),
                        'make': 'Schneider',  # Locked
                        'series_bucket': 'LC1E',  # Locked
                        'item_producttype': 'Contactor',  # Locked (not "contractor")
                        'business_subcategory': 'Power Contactor',  # Locked
                        'frame_label': frame_label,  # Tracked from FRAME- rows or inferred from base_ref
                        'poles': '3P',  # Locked
                        'ac1_current_a': ac1_current,
                        'ac3_current_a': ac3_current,
                        'motor_hp': hp,  # FROZEN: duty-independent, same for AC1/AC3
                        'motor_kw': kw,  # FROZEN: duty-independent, same for AC1/AC3
                        'aux_no_count': no_count,
                        'aux_nc_count': nc_count,
                        'aux_raw_text': '',
                        'base_ref_raw': base_ref_raw,
                        'base_ref_clean': base_ref_clean,
                        'notes_raw': combined_notes
                    })
            
            sections_found.append('LC1E_3P_AC')
    
    # SECTION B: LC1E 3P DC Control  
    print()
    print("Searching for Section B: LC1E 3P DC Control...")
    section_b_start = None
    
    for idx in range(len(df)):
        row_str = normalize_row_to_string(df.iloc[idx])
        # Look for DC control section
        if (('3 Pole DC' in row_str or 'DC Control' in row_str or '3P DC' in row_str) and 
            'LC1E' in row_str) or \
           (('BD' in row_str or '24V DC' in row_str) and 
            'LC1E' in normalize_row_to_string(df.iloc[max(0, idx-3):idx+1])):
            section_b_start = idx
            print(f"  ✓ Found Section B start at row {idx}")
            break
    
    if section_b_start:
        header_row, coil_map = find_coil_header_row(df, section_b_start, min(section_b_start + 50, len(df)))
        if header_row and coil_map:
            print(f"  ✓ Found header at row {header_row}, coil columns: {coil_map}")
            
            current_frame_label = ''
            for data_idx in range(header_row + 1, min(header_row + 200, len(df))):
                row = df.iloc[data_idx]
                row_str = normalize_row_to_string(row)
                
                # Skip FRAME- rows
                if 'FRAME-' in row_str:
                    frame_match = re.search(r'FRAME-[\dA-Z]+', row_str)
                    if frame_match:
                        current_frame_label = frame_match.group(0)
                    continue
                
                # Check for next section
                if any(marker.lower() in row_str.lower() for marker in NEXT_SECTION_MARKERS):
                    break
                
                # Find base reference
                base_ref_raw = None
                base_ref_clean = None
                for col_idx in range(min(80, len(row))):
                    val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                    if pd.notna(val):
                        val_str = str(val).strip()
                        base_match = BASE_REF_PATTERN.search(val_str)
                        if base_match:
                            base_ref_raw = base_match.group(1)
                            base_ref_clean = normalize_base_ref(base_ref_raw)
                            break
                
                if base_ref_clean:
                    # CRITICAL: Only accept if at least one coil price is numeric AND >= 100
                    priced_rows = []
                    
                    for coil_code, col_idx in coil_map.items():
                        if col_idx < len(row):
                            price_val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                            price = extract_numeric_value(price_val)
                            if price and price >= 100:  # Contactor threshold
                                priced_rows.append({'coil_code': coil_code, 'price': price})
                    
                    if not priced_rows:
                        continue
                    
                    # Extract ratings
                    ac1_current = None
                    ac3_current = None
                    hp = None
                    kw = None
                    no_count = None
                    nc_count = None
                    
                    header_str = normalize_row_to_string(df.iloc[header_row])
                    for col_idx in range(min(80, len(row))):
                        val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                        if pd.notna(val):
                            header_val = df.iloc[header_row].iloc[col_idx] if col_idx < len(df.iloc[header_row]) else None
                            header_val_str = str(header_val).upper() if pd.notna(header_val) else ''
                            
                            if 'AC-1' in header_val_str or 'AC1' in header_val_str:
                                ac1_current = extract_current_value(val)
                            elif 'AC-3' in header_val_str or 'AC3' in header_val_str:
                                ac3_current = extract_current_value(val)
                            elif 'HP' in header_val_str:
                                hp, _ = parse_hp_range(val)  # FROZEN: use minimum for ranges
                            elif 'KW' in header_val_str or 'kW' in header_val_str:
                                kw_val, _ = parse_kw_range(val)
                                kw = kw_val
                            elif 'NO' in header_val_str and col_idx not in coil_map.values():
                                no_val = extract_numeric_value(val)
                                if no_val is not None:
                                    no_count = int(no_val)
                                else:
                                    parsed_no, _ = parse_aux_contacts(val)
                                    if parsed_no is not None:
                                        no_count = parsed_no
                            elif 'NC' in header_val_str and col_idx not in coil_map.values():
                                nc_val = extract_numeric_value(val)
                                if nc_val is not None:
                                    nc_count = int(nc_val)
                                else:
                                    _, parsed_nc = parse_aux_contacts(val)
                                    if parsed_nc is not None:
                                        nc_count = parsed_nc
                    
                    # Collect range notes if present (HP and kW) - FROZEN RULE: use minimum for ranges
                    hp_range_note = None
                    kw_range_note = None
                    for col_idx in range(min(80, len(row))):
                        val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                        if pd.notna(val):
                            header_val = df.iloc[header_row].iloc[col_idx] if col_idx < len(df.iloc[header_row]) else None
                            header_val_str = str(header_val).upper() if pd.notna(header_val) else ''
                            if 'HP' in header_val_str:
                                _, note = parse_hp_range(val)
                                if note:
                                    hp_range_note = note
                            elif 'KW' in header_val_str or 'kW' in header_val_str:
                                _, note = parse_kw_range(val)
                                if note:
                                    kw_range_note = note
                    
                    # Combine range notes
                    range_notes = []
                    if hp_range_note:
                        range_notes.append(hp_range_note)
                    if kw_range_note:
                        range_notes.append(kw_range_note)
                    combined_notes = '; '.join(range_notes) if range_notes else ''
                    
                    # Extract coil prices
                    for coil_price_info in priced_rows:
                        coil_code = coil_price_info['coil_code']
                        price = coil_price_info['price']
                        completed_sku = f"{base_ref_clean}{coil_code}"
                        coil_code_prices.append({
                            'base_ref_clean': base_ref_clean,
                            'coil_code': coil_code,
                            'voltage_type': LC1E_COIL_CODES.get(coil_code, {}).get('voltage_type', 'DC'),
                            'voltage_value': LC1E_COIL_CODES.get(coil_code, {}).get('voltage', None),
                            'completed_sku': completed_sku,
                            'price': price,
                            'currency': 'INR',
                            'source_page_or_block': 'Table 1',
                            'table_id': 'LC1E_3P_DC',
                            'source_row_id': str(data_idx + 1)
                        })
                    
                    # Add canonical row
                    # FROZEN RULE: HP and kW are duty-independent, same for AC1 and AC3
                    canonical_rows.append({
                        'source_doc': xlsx_file,
                        'source_page_or_block': 'Table 1',
                        'table_id': 'LC1E_3P_DC',
                        'source_row_id': str(data_idx + 1),
                        'make': 'Schneider',  # Locked
                        'series_bucket': 'LC1E',  # Locked
                        'item_producttype': 'Contactor',  # Locked
                        'business_subcategory': 'Power Contactor',  # Locked
                        'frame_label': current_frame_label if current_frame_label else infer_frame_from_base_ref(base_ref_clean),
                        'poles': '3P',  # Locked
                        'ac1_current_a': ac1_current,
                        'ac3_current_a': ac3_current,
                        'motor_hp': hp,  # FROZEN: duty-independent, same for AC1/AC3
                        'motor_kw': kw,  # FROZEN: duty-independent, same for AC1/AC3
                        'aux_no_count': no_count,
                        'aux_nc_count': nc_count,
                        'aux_raw_text': '',
                        'base_ref_raw': base_ref_raw,
                        'base_ref_clean': base_ref_clean,
                        'notes_raw': combined_notes
                    })
            
            sections_found.append('LC1E_3P_DC')
    
    # SECTION C: LC1E 4P AC Control
    print()
    print("Searching for Section C: LC1E 4P AC Control...")
    section_c_start = None
    
    for idx in range(len(df)):
        row_str = normalize_row_to_string(df.iloc[idx])
        if ('4 Pole' in row_str or '4P' in row_str) and 'LC1E' in row_str:
            section_c_start = idx
            print(f"  ✓ Found Section C start at row {idx}")
            break
    
    if section_c_start:
        header_row, coil_map = find_coil_header_row(df, section_c_start, min(section_c_start + 50, len(df)))
        # Tighten 4P detection: header must include at least 2 of B7/F7/M5WB/N5WB
        required_4p_coils = ['B7', 'F7', 'M5WB', 'N5WB']
        found_4p_coils = [c for c in required_4p_coils if c in coil_map]
        if header_row and coil_map and len(found_4p_coils) >= 2:
            print(f"  ✓ Found header at row {header_row}, coil columns: {coil_map} (4P validated)")
            
            current_frame_label = ''
            for data_idx in range(header_row + 1, min(header_row + 200, len(df))):
                row = df.iloc[data_idx]
                row_str = normalize_row_to_string(row)
                
                # Skip FRAME- rows
                if 'FRAME-' in row_str:
                    frame_match = re.search(r'FRAME-[\dA-Z]+', row_str)
                    if frame_match:
                        current_frame_label = frame_match.group(0)
                    continue
                
                # Check for next section
                if any(marker.lower() in row_str.lower() for marker in NEXT_SECTION_MARKERS):
                    break
                
                # Find base reference
                base_ref_raw = None
                base_ref_clean = None
                for col_idx in range(min(80, len(row))):
                    val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                    if pd.notna(val):
                        val_str = str(val).strip()
                        base_match = BASE_REF_PATTERN.search(val_str)
                        if base_match:
                            base_ref_raw = base_match.group(1)
                            base_ref_clean = normalize_base_ref(base_ref_raw)
                            break
                
                if base_ref_clean:
                    # CRITICAL: 4P base refs must contain 00(4|8) pattern (e.g., LC1E06004, LC1E06008)
                    if not re.search(r'00(4|8)', base_ref_clean):
                        continue  # Skip LC1E0600/2500/4000 contamination
                    
                    # CRITICAL: Only accept if at least one coil price is numeric AND >= 100
                    priced_rows = []
                    
                    for coil_code, col_idx in coil_map.items():
                        if col_idx < len(row):
                            price_val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                            price = extract_numeric_value(price_val)
                            if price and price >= 100:  # Contactor threshold
                                priced_rows.append({'coil_code': coil_code, 'price': price})
                    
                    if not priced_rows:
                        continue
                    
                    # Extract ratings (best effort for 4P)
                    ac1_current = None
                    ac3_current = None
                    hp = None
                    kw = None
                    no_count = None
                    nc_count = None
                    
                    # Collect range notes if present (HP and kW) - FROZEN RULE: use minimum for ranges
                    # Note: 4P section may not have HP/kW columns, but handle if present
                    hp_range_note = None
                    kw_range_note = None
                    
                    # Extract coil prices
                    for coil_price_info in priced_rows:
                        coil_code = coil_price_info['coil_code']
                        price = coil_price_info['price']
                        completed_sku = f"{base_ref_clean}{coil_code}"
                        coil_code_prices.append({
                            'base_ref_clean': base_ref_clean,
                            'coil_code': coil_code,
                            'voltage_type': LC1E_COIL_CODES.get(coil_code, {}).get('voltage_type', 'AC'),
                            'voltage_value': LC1E_COIL_CODES.get(coil_code, {}).get('voltage', None),
                            'completed_sku': completed_sku,
                            'price': price,
                            'currency': 'INR',
                            'source_page_or_block': 'Table 1',
                            'table_id': 'LC1E_4P_AC',
                            'source_row_id': str(data_idx + 1)
                        })
                    
                    # Combine range notes
                    range_notes = []
                    if hp_range_note:
                        range_notes.append(hp_range_note)
                    if kw_range_note:
                        range_notes.append(kw_range_note)
                    combined_notes = '; '.join(range_notes) if range_notes else ''
                    
                    # Add canonical row
                    # FROZEN RULE: HP and kW are duty-independent, same for AC1 and AC3
                    canonical_rows.append({
                        'source_doc': xlsx_file,
                        'source_page_or_block': 'Table 1',
                        'table_id': 'LC1E_4P_AC',
                        'source_row_id': str(data_idx + 1),
                        'make': 'Schneider',  # Locked
                        'series_bucket': 'LC1E',  # Locked
                        'item_producttype': 'Contactor',  # Locked
                        'business_subcategory': 'Power Contactor',  # Locked
                        'frame_label': current_frame_label if current_frame_label else infer_frame_from_base_ref(base_ref_clean),
                        'poles': '4P',  # Locked
                        'ac1_current_a': ac1_current,
                        'ac3_current_a': ac3_current,
                        'motor_hp': hp,  # FROZEN: duty-independent, same for AC1/AC3
                        'motor_kw': kw,  # FROZEN: duty-independent, same for AC1/AC3
                        'aux_no_count': no_count,
                        'aux_nc_count': nc_count,
                        'aux_raw_text': '',
                        'base_ref_raw': base_ref_raw,
                        'base_ref_clean': base_ref_clean,
                        'notes_raw': combined_notes
                    })
            
            sections_found.append('LC1E_4P_AC')
    
    # SECTION D: Accessories (global scan, not section-dependent)
    print()
    print("Searching for LC1E Accessories (global scan)...")
    # Robust accessory pattern: allows optional spaces and trailing digits/zeros
    accessory_pattern = re.compile(r'^(LAEN|LAET|LAERC|LAER|LAEM|LAEX|LAETSD)[A-Z0-9 ]{0,10}$', re.IGNORECASE)
    
    # Global scan: check all rows for accessory patterns
    for data_idx in range(len(df)):
        row = df.iloc[data_idx]
        row_str = normalize_row_to_string(row)
        
        # Skip if this looks like a header or section marker
        if any(marker in row_str.upper() for marker in ['POWER CONTACTORS', 'RATED OPERATIONAL', 'AC-1', 'AC-3', 'REFERENCE']):
            continue
        
        # Check each cell for accessory pattern
        for col_idx, cell in enumerate(row):
            if pd.notna(cell):
                cell_str = str(cell).strip()
                if accessory_pattern.match(cell_str):
                    # Found accessory SKU - extract price from nearby cells (right side)
                    price = None
                    # Look for first numeric value in remaining cells of this row
                    for price_col_idx in range(col_idx + 1, min(col_idx + 10, len(row))):
                        if price_col_idx < len(row):
                            price_cell = row.iloc[price_col_idx] if hasattr(row, 'iloc') else row[price_col_idx]
                            price_val = extract_numeric_value(price_cell)
                            if price_val and price_val >= 1:  # Accessories can be < 100
                                price = price_val
                                break
                    
                    if price:
                        accessory_skus.append({
                            'make': 'Schneider',
                            'series_bucket': 'LC1E',
                            'item_producttype': 'Contactor',
                            'business_subcategory': 'Power Contactor',
                            'sc_l4_accessory_class': 'AUX',
                            'oem_catalog_no': cell_str,
                            'price': price,
                            'currency': 'INR',
                            'compatibility_note': 'LC1E Series',
                            'source_page_or_block': 'Table 1',
                            'table_id': 'LC1E_ACCESSORIES',
                            'source_row_id': str(data_idx + 1)
                        })
    
    if len(accessory_skus) > 0:
        sections_found.append('LC1E_ACCESSORIES')
        print(f"  ✓ Found {len(accessory_skus)} accessory SKUs")
    
    print()
    print("=" * 80)
    print(f"✓ Sections found: {len(sections_found)} - {sections_found}")
    print(f"✓ Base refs extracted (before dedup): {len(set([r['base_ref_clean'] for r in canonical_rows]))}")
    print(f"✓ Coil price rows created (before dedup): {len(coil_code_prices)}")
    print(f"✓ Accessory SKUs extracted: {len(accessory_skus)}")
    print()
    
    # Deduplicate coil price rows by (base_ref_clean, coil_code, price)
    seen_coil_prices = set()
    deduped_coil_prices = []
    for row in coil_code_prices:
        key = (row['base_ref_clean'], row['coil_code'], row['price'])
        if key not in seen_coil_prices:
            seen_coil_prices.add(key)
            deduped_coil_prices.append(row)
    
    coil_code_prices = deduped_coil_prices
    
    print(f"✓ Coil price rows (after dedup): {len(coil_code_prices)}")
    print()
    
    # Sanity check
    if len(coil_code_prices) == 0:
        raise RuntimeError("No priced coil rows extracted; check section detection")
    
    # Show sample rows
    if canonical_rows:
        print("Sample canonical rows (first 3):")
        for i, row in enumerate(canonical_rows[:3], 1):
            print(f"  {i}. Base: {row['base_ref_clean']}, AC1: {row['ac1_current_a']}, AC3: {row['ac3_current_a']}")
    
    if coil_code_prices:
        print()
        print("Sample coil price rows (first 5):")
        for i, row in enumerate(coil_code_prices[:5], 1):
            print(f"  {i}. {row['completed_sku']}: {row['coil_code']} @ {row['price']}")
    
    if accessory_skus:
        print()
        print("Sample accessory rows (first 3):")
        for i, row in enumerate(accessory_skus[:3], 1):
            print(f"  {i}. {row['oem_catalog_no']}: {row['price']}")
    
    print()
    print("=" * 80)
    
    # Dedupe canonical rows by base_ref_clean
    seen_bases = set()
    deduped_canonical = []
    for row in canonical_rows:
        base = row['base_ref_clean']
        if base and base not in seen_bases:
            seen_bases.add(base)
            deduped_canonical.append(row)
    
    # Always create accessory DataFrame with columns (even if empty)
    accessory_columns = [
        'make', 'series_bucket', 'item_producttype', 'business_subcategory',
        'sc_l4_accessory_class', 'oem_catalog_no', 'price', 'currency',
        'compatibility_note', 'source_page_or_block', 'table_id', 'source_row_id'
    ]
    if len(accessory_skus) > 0:
        accessory_df = pd.DataFrame(accessory_skus)
    else:
        accessory_df = pd.DataFrame(columns=accessory_columns)
    
    return pd.DataFrame(deduped_canonical), pd.DataFrame(coil_code_prices), accessory_df


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
    
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract canonical data
    try:
        canonical_df, coil_price_df, accessory_df = extract_lc1e_canonical_rows(args.input_xlsx)
        
        # Write to Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            canonical_df.to_excel(writer, sheet_name='LC1E_CANONICAL_ROWS', index=False)
            coil_price_df.to_excel(writer, sheet_name='LC1E_COIL_CODE_PRICES', index=False)
            accessory_df.to_excel(writer, sheet_name='LC1E_ACCESSORY_SKUS', index=False)
        
        print()
        print(f"✓ Created canonical workbook: {output_path}")
        print(f"  - LC1E_CANONICAL_ROWS: {len(canonical_df)} rows")
        print(f"  - LC1E_COIL_CODE_PRICES: {len(coil_price_df)} rows")
        print(f"  - LC1E_ACCESSORY_SKUS: {len(accessory_df)} rows")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


