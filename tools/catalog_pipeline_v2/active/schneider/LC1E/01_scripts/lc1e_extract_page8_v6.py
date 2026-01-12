#!/usr/bin/env python3
"""
LC1E Page-8 Extraction - v6 Format (Semantic Lock Compliant)

Purpose:
- Extracts ONLY Page-8 tables (P8_T1 and P8_T3) from raw pricelist
- Follows LC1E_Page8_SEMANTIC_LOCK.yaml exactly (no inference)
- Outputs v6-compatible sheet names:
  - P8_T1_CANONICAL_ROWS (21 rows)
  - P8_T1_COIL_PRICES (40 rows)
  - P8_T3_CANONICAL_ROWS (8 rows)
  - P8_T3_COIL_PRICES (15 rows)

Rules (FROZEN):
1) Frame labels from frozen_frame_ranges (P8_T1) or explicit rows (P8_T3)
2) Base ref normalization: remove */#, trailing 0 artifacts
3) Priced-only: dash/blank means NO price row
4) kW/HP ranges: use minimum value
5) Aux contacts: dash means zero
"""

import argparse
import pandas as pd
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Load semantic lock
SEMANTIC_LOCK_PATH = Path(__file__).parent.parent / "04_docs" / "LC1E_Page8_SEMANTIC_LOCK.yaml"

def load_semantic_lock():
    """Load and validate semantic lock YAML."""
    with open(SEMANTIC_LOCK_PATH, 'r') as f:
        lock = yaml.safe_load(f)
    assert lock['status'] == 'FROZEN', "Semantic lock must be FROZEN"
    return lock

def normalize_base_ref(raw_ref: str, lock: Dict) -> Optional[str]:
    """
    Normalize base reference per semantic lock rules.
    """
    if pd.isna(raw_ref) or str(raw_ref).strip() == '':
        return None
    
    ref = str(raw_ref).strip()
    
    # Apply cleanup rules from semantic lock
    rules = lock['base_reference_normalization']['cleanup_rules']
    for rule in rules:
        if rule['name'] == 'trim_whitespace':
            ref = ref.strip()
        elif rule['name'] == 'remove_trailing_star_block':
            pattern = rule['pattern']
            ref = re.sub(pattern + r'\s*$', '', ref)
        elif rule['name'] == 'remove_trailing_hash':
            ref = re.sub(r'#+\s*$', '', ref)
        elif rule['name'] == 'remove_trailing_zero_artifact':
            # Pattern: "LC1E0601* 0" -> "LC1E0601"
            ref = re.sub(r'\s+0\s*$', '', ref)
    
    # Keep tokens (IN only if printed - Page-8 has no IN in 3P tables)
    # No action needed for Page-8
    
    return ref if ref else None

def extract_numeric_price(value) -> Optional[float]:
    """Extract numeric price, return None if dash/blank/invalid."""
    if pd.isna(value):
        return None
    val_str = str(value).strip()
    # Dash means no price
    if val_str == '-' or val_str == '':
        return None
    try:
        price = float(val_str)
        return price if price > 0 else None
    except (ValueError, TypeError):
        return None

def extract_current_value(cell_value) -> Optional[float]:
    """Extract numeric current from cell (e.g., '20 A' -> 20)."""
    if pd.isna(cell_value):
        return None
    val_str = str(cell_value).strip()
    match = re.search(r'(\d+(?:\.\d+)?)', val_str)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None

def parse_range_min(cell_value, field: str, range_policy: str = "min") -> Tuple[Optional[float], Optional[str]]:
    """
    Parse kW/HP range values. Returns (min_value, range_note).
    FROZEN RULE: range_policy="min" means use minimum value.
    field: "kw" or "hp" to generate correct note format.
    """
    if pd.isna(cell_value):
        return None, None
    val_str = str(cell_value).strip()
    
    # Check for range pattern (e.g., "25/30")
    range_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', val_str)
    if range_match:
        min_val = float(range_match.group(1))
        max_val = float(range_match.group(2))
        if field == "kw":
            note = f"KW_RANGE={min_val}/{max_val}; motor_kw=min={min_val}"
        else:
            note = f"HP_RANGE={min_val}/{max_val}; motor_hp=min={min_val}"
        return min_val, note
    
    # Try regular numeric
    try:
        val = float(val_str)
        return val if val > 0 else None, None
    except (ValueError, TypeError):
        return None, None

def parse_aux_contact(cell_value, dash_means_zero: bool = True) -> Optional[int]:
    """Parse aux contact count. Dash means zero if dash_means_zero=True."""
    if pd.isna(cell_value):
        return None
    val_str = str(cell_value).strip()
    if dash_means_zero and (val_str == '-' or val_str == ''):
        return 0
    try:
        return int(float(val_str))
    except (ValueError, TypeError):
        return None

def get_frame_label_for_base_ref(base_ref_clean: str, table_config: Dict) -> str:
    """
    Get frame label for base_ref using frozen_frame_ranges (P8_T1) or explicit (P8_T3).
    """
    frame_semantics = table_config.get('frame_semantics', {})
    
    if frame_semantics.get('type') == 'carry_forward_with_frozen_ranges':
        # P8_T1: Use frozen ranges
        for frame_range in frame_semantics.get('frozen_frame_ranges', []):
            if base_ref_clean in frame_range['base_refs']:
                return frame_range['frame_label']
        # Fallback: should not happen if base_ref is valid
        return ''
    elif frame_semantics.get('type') == 'explicit_rows_only':
        # P8_T3: Frame labels are explicit in table (handled during extraction)
        return ''  # Will be set from source during extraction
    
    return ''

def extract_p8_t1(xlsx_file: str, lock: Dict, df: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract P8_T1: LC1E 3P AC Control 6A–95A (M7/N5 only).
    Returns (canonical_rows, coil_prices).
    """
    table_config = lock['tables'][0]  # P8_T1_3P_AC_M7_N5
    coil_variants = table_config['coil_variants']  # M7, N5
    
    canonical_rows = []
    coil_prices = []
    
    # Gap 3 fix: Find header row first (M7+N5 in same row), then validate section markers
    header_row = None
    coil_col_map = {}
    section_markers = ['Power Contactors LC1E', 'Rated Operational Motor Power']
    
    # First, find header row with M7+N5 in same row
    for idx in range(len(df)):
        row = df.iloc[idx]
        row_coil_cols = {}
        for col_idx, val in enumerate(row):
            if pd.notna(val):
                val_str = str(val).strip().upper()
                if 'M7' in val_str:
                    row_coil_cols['M7'] = col_idx
                if 'N5' in val_str:
                    row_coil_cols['N5'] = col_idx
        
        # Require both M7 and N5 in same row
        if len(row_coil_cols) >= 2 and 'M7' in row_coil_cols and 'N5' in row_coil_cols:
            # Check for section markers nearby (within 10 rows before)
            has_section_marker = False
            for check_idx in range(max(0, idx - 10), idx + 1):
                check_str = ' '.join([str(v) if pd.notna(v) else '' for v in df.iloc[check_idx]])
                if any(marker in check_str for marker in section_markers):
                    has_section_marker = True
                    break
            
            if has_section_marker:
                coil_col_map = row_coil_cols
                header_row = idx
                break
    
    if not header_row:
        print("  ✗ P8_T1 header row not found (M7+N5 in same row + section markers required)")
        return canonical_rows, coil_prices
    
    print(f"  ✓ Found P8_T1 header at row {header_row}, coil columns: {coil_col_map}")
    
    # Extract data rows
    NEXT_SECTION_MARKERS = ['3 Pole DC', '3P DC', 'DC Control', '4 Pole', '4P', 
                           'FRAME-5', 'FRAME-6', 'FRAME-7', 'FRAME-8', 'FRAME-9']
    
    for data_idx in range(header_row + 1, min(header_row + 200, len(df))):
        row = df.iloc[data_idx]
        row_str = ' '.join([str(v) if pd.notna(v) else '' for v in row])
        
        # Skip FRAME- rows (but extract frame label for P8_T1)
        if 'FRAME-' in row_str:
            continue
        
        # Check for next section
        if any(marker.lower() in row_str.lower() for marker in NEXT_SECTION_MARKERS):
            break
        
        # Find base reference column (Gap 2: use reference-relative offsets)
        base_ref_raw = None
        base_ref_clean = None
        ref_col = None
        BASE_REF_PATTERN = re.compile(r'LC1E[0-9A-Z]+(?:\*+|#+)?', re.IGNORECASE)
        
        for col_idx in range(min(80, len(row))):
            val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
            if pd.notna(val):
                val_str = str(val).strip()
                match = BASE_REF_PATTERN.search(val_str)
                if match:
                    base_ref_raw = match.group(0)
                    base_ref_clean = normalize_base_ref(base_ref_raw, lock)
                    ref_col = col_idx
                    break
        
        if not base_ref_clean or ref_col is None:
            continue
        
        # CRITICAL: Only accept if at least one coil (M7 or N5) has numeric price
        priced_coils = []
        for variant in coil_variants:
            variant_code = variant['variant_code']
            if variant_code in coil_col_map:
                col_idx = coil_col_map[variant_code]
                if col_idx < len(row):
                    price_val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                    price = extract_numeric_price(price_val)
                    if price:
                        priced_coils.append({
                            'variant_code': variant_code,
                            'price': price,
                            'voltage_type': variant['voltage_type'],
                            'voltage_V': variant['voltage_V']
                        })
        
        # FROZEN RULE: priced_only=true, dash_means_no_price_row=true
        if not priced_coils:
            continue  # Skip row if no priced coils
        
        # Extract ratings using reference-relative offsets (Gap 2 fix)
        # Fields are left of Reference column in fixed order: AC-1, AC-3, HP, kW, NO, NC
        # Build label->col map from header row for robustness
        field_col_map = {}
        for col_idx in range(min(80, len(df.iloc[header_row]))):
            header_val = df.iloc[header_row].iloc[col_idx] if col_idx < len(df.iloc[header_row]) else None
            if pd.notna(header_val):
                header_val_str = str(header_val).strip().upper()
                if ('AC-1' in header_val_str or 'AC1' in header_val_str) and 'AC-3' not in header_val_str and 'AC3' not in header_val_str:
                    field_col_map['AC1'] = col_idx
                elif 'AC-3' in header_val_str or 'AC3' in header_val_str:
                    field_col_map['AC3'] = col_idx
                elif 'HP' in header_val_str and col_idx not in coil_col_map.values():
                    field_col_map['HP'] = col_idx
                elif ('KW' in header_val_str or 'kW' in header_val_str) and col_idx not in coil_col_map.values():
                    field_col_map['KW'] = col_idx
                elif 'NO' in header_val_str and col_idx not in coil_col_map.values():
                    field_col_map['NO'] = col_idx
                elif 'NC' in header_val_str and col_idx not in coil_col_map.values():
                    field_col_map['NC'] = col_idx
        
        # Extract values using field map
        ac1_current = None
        ac3_current = None
        hp = None
        kw = None
        no_count = None
        nc_count = None
        kw_range_note = None
        hp_range_note = None
        
        if 'AC1' in field_col_map:
            col_idx = field_col_map['AC1']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                ac1_current = extract_current_value(val)
        
        if 'AC3' in field_col_map:
            col_idx = field_col_map['AC3']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                ac3_current = extract_current_value(val)
        
        if 'HP' in field_col_map:
            col_idx = field_col_map['HP']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                hp, hp_range_note = parse_range_min(val, "hp", "min")
        
        if 'KW' in field_col_map:
            col_idx = field_col_map['KW']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                kw, kw_range_note = parse_range_min(val, "kw", "min")
        
        if 'NO' in field_col_map:
            col_idx = field_col_map['NO']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                no_count = parse_aux_contact(val, dash_means_zero=True)
        
        if 'NC' in field_col_map:
            col_idx = field_col_map['NC']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                nc_count = parse_aux_contact(val, dash_means_zero=True)
        
        # Get frame label from frozen ranges
        frame_label = get_frame_label_for_base_ref(base_ref_clean, table_config)
        
        # Build range notes (Gap 1 fix: notes already correct from parse_range_min)
        range_notes = []
        if kw_range_note:
            range_notes.append(kw_range_note)
        if hp_range_note:
            range_notes.append(hp_range_note)
        combined_notes = '; '.join(range_notes) if range_notes else ''
        
        # Add canonical row (once per base_ref) - v6 schema
        canonical_rows.append({
            'make': lock['oem'],
            'series_name': lock['series_name'],
            'series_bucket': lock['series_bucket'],
            'item_producttype': 'Contactor',
            'business_subcategory': 'Power Contactor',
            'source_page': 8,  # v6 uses numeric
            'table_id': table_config['table_id'],
            'frame_label': frame_label,
            'poles': table_config['poles'],
            'base_ref_clean': base_ref_clean,
            'ac1_A': ac1_current,  # v6 uses ac1_A not ac1_current_a
            'ac3_A': ac3_current,  # v6 uses ac3_A not ac3_current_a
            'motor_hp': hp,
            'motor_kw': kw,
            'aux_no': no_count if no_count is not None else 0,  # v6 uses aux_no not aux_no_count
            'aux_nc': nc_count if nc_count is not None else 0,  # v6 uses aux_nc not aux_nc_count
            'notes_raw': combined_notes if combined_notes else None
        })
        
        # Add coil prices (only for priced coils) - v6 schema
        for coil_info in priced_coils:
            completed_ref = f"{base_ref_clean}{coil_info['variant_code']}"
            coil_prices.append({
                'make': lock['oem'],
                'series_name': lock['series_name'],
                'series_bucket': lock['series_bucket'],
                'currency': lock['source']['currency'],
                'effective_from': lock['source'].get('effective_from', '2025-07-15'),
                'pricelist_ref': lock['source'].get('pricelist_ref', 'WEF 15 Jul 2025'),
                'source_page': 8,  # v6 uses numeric
                'table_id': table_config['table_id'],
                'base_ref_clean': base_ref_clean,
                'coil_code': coil_info['variant_code'],
                'voltage_type': coil_info['voltage_type'],
                'voltage_V': coil_info['voltage_V'],  # v6 uses voltage_V not voltage_value
                'completed_ref': completed_ref,  # v6 uses completed_ref not completed_sku
                'price_inr': coil_info['price']  # v6 uses price_inr not price
            })
    
    # Deduplicate canonical rows by base_ref_clean
    seen_bases = set()
    deduped_canonical = []
    for row in canonical_rows:
        base = row['base_ref_clean']
        if base and base not in seen_bases:
            seen_bases.add(base)
            deduped_canonical.append(row)
    
    print(f"  ✓ P8_T1: {len(deduped_canonical)} canonical rows, {len(coil_prices)} coil prices")
    
    return deduped_canonical, coil_prices

def extract_p8_t3(xlsx_file: str, lock: Dict, df: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract P8_T3: LC1E 3P AC Control High Ratings (Frames 5–9) (M5/N5/M7/N7).
    Returns (canonical_rows, coil_prices).
    """
    table_config = lock['tables'][1]  # P8_T3_3P_AC_HIGH_M7_N5_M5_N7
    coil_variants_by_row = table_config['coil_variants_by_row']
    allowed_variant_codes = coil_variants_by_row['allowed_variant_codes']  # M5, N5, M7, N7
    voltage_map = coil_variants_by_row['voltage_map']
    
    canonical_rows = []
    coil_prices = []
    
    # Find header row by detecting AC-1, AC-3, HP, kW and at least 2 coil codes (Gap 4 fix)
    header_row = None
    coil_col_map = {}
    field_col_map = {}
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        row_str = ' '.join([str(v) if pd.notna(v) else '' for v in row])
        
        # Check for header row: must have AC-1, AC-3, HP, kW and at least 2 coil codes
        row_coil_cols = {}
        row_field_cols = {}
        
        for col_idx, val in enumerate(row):
            if pd.notna(val):
                val_str = str(val).strip().upper()
                
                # Check for coil codes
                for variant_code in allowed_variant_codes:
                    if variant_code in val_str:
                        row_coil_cols[variant_code] = col_idx
                
                # Check for field labels
                if ('AC-1' in val_str or 'AC1' in val_str) and 'AC-3' not in val_str and 'AC3' not in val_str:
                    row_field_cols['AC1'] = col_idx
                elif 'AC-3' in val_str or 'AC3' in val_str:
                    row_field_cols['AC3'] = col_idx
                elif 'HP' in val_str:
                    row_field_cols['HP'] = col_idx
                elif 'KW' in val_str or 'kW' in val_str:
                    row_field_cols['KW'] = col_idx
        
        # Require: at least 2 coil codes AND at least AC-1/AC-3/HP/kW fields
        if len(row_coil_cols) >= 2 and len(row_field_cols) >= 2:
            # Additional check: should be in high ratings section (Frames 5-9 nearby)
            # Check nearby rows for frame markers
            has_frame_marker = False
            for check_idx in range(max(0, idx - 10), min(idx + 10, len(df))):
                check_str = ' '.join([str(v) if pd.notna(v) else '' for v in df.iloc[check_idx]])
                if any(f'FRAME-{i}' in check_str for i in [5, 6, 7, 8, 9]):
                    has_frame_marker = True
                    break
            
            if has_frame_marker:
                coil_col_map = row_coil_cols
                field_col_map = row_field_cols
                header_row = idx
                break
    
    if not header_row:
        print("  ✗ P8_T3 header row not found (need AC-1/AC-3/HP/kW + 2+ coil codes)")
        return canonical_rows, coil_prices
    
    print(f"  ✓ Found P8_T3 header at row {header_row}, coil columns: {coil_col_map}, field columns: {field_col_map}")
    
    # Extract data rows
    NEXT_SECTION_MARKERS = ['Accessories', 'Mechanical Interlock', 'Control Relays']
    current_frame_label = ''
    
    for data_idx in range(header_row + 1, min(header_row + 200, len(df))):
        row = df.iloc[data_idx]
        row_str = ' '.join([str(v) if pd.notna(v) else '' for v in row])
        
        # Extract frame label from FRAME- rows (explicit_rows_only)
        frame_match = re.search(r'FRAME-[\dA-Z]+', row_str, re.IGNORECASE)
        if frame_match:
            current_frame_label = frame_match.group(0).upper()
            continue
        
        # Check for next section
        if any(marker.lower() in row_str.lower() for marker in NEXT_SECTION_MARKERS):
            break
        
        # Find base reference (Gap 2: use field map approach like P8_T1)
        base_ref_raw = None
        base_ref_clean = None
        BASE_REF_PATTERN = re.compile(r'LC1E[0-9A-Z]+(?:\*+|#+)?', re.IGNORECASE)
        
        for col_idx in range(min(80, len(row))):
            val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
            if pd.notna(val):
                val_str = str(val).strip()
                match = BASE_REF_PATTERN.search(val_str)
                if match:
                    base_ref_raw = match.group(0)
                    base_ref_clean = normalize_base_ref(base_ref_raw, lock)
                    break
        
        if not base_ref_clean:
            continue
        
        # CRITICAL: Only accept if at least one allowed coil has numeric price
        priced_coils = []
        for variant_code in allowed_variant_codes:
            if variant_code in coil_col_map:
                col_idx = coil_col_map[variant_code]
                if col_idx < len(row):
                    price_val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                    price = extract_numeric_price(price_val)
                    if price:
                        variant_info = voltage_map[variant_code]
                        priced_coils.append({
                            'variant_code': variant_code,
                            'price': price,
                            'voltage_type': variant_info['voltage_type'],
                            'voltage_V': variant_info['voltage_V']
                        })
        
        # FROZEN RULE: priced_only=true
        if not priced_coils:
            continue
        
        # Extract ratings using field map (Gap 2 fix: same approach as P8_T1)
        ac1_current = None
        ac3_current = None
        hp = None
        kw = None
        no_count = None
        nc_count = None
        
        # Build complete field map including NO/NC if not already found
        if 'NO' not in field_col_map or 'NC' not in field_col_map:
            for col_idx in range(min(80, len(df.iloc[header_row]))):
                header_val = df.iloc[header_row].iloc[col_idx] if col_idx < len(df.iloc[header_row]) else None
                if pd.notna(header_val):
                    header_val_str = str(header_val).strip().upper()
                    if 'NO' in header_val_str and col_idx not in coil_col_map.values():
                        field_col_map['NO'] = col_idx
                    elif 'NC' in header_val_str and col_idx not in coil_col_map.values():
                        field_col_map['NC'] = col_idx
        
        # Extract values using field map
        if 'AC1' in field_col_map:
            col_idx = field_col_map['AC1']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                ac1_current = extract_current_value(val)
        
        if 'AC3' in field_col_map:
            col_idx = field_col_map['AC3']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                ac3_current = extract_current_value(val)
        
        if 'HP' in field_col_map:
            col_idx = field_col_map['HP']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                hp, _ = parse_range_min(val, "hp", "min")
        
        if 'KW' in field_col_map:
            col_idx = field_col_map['KW']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                kw, _ = parse_range_min(val, "kw", "min")
        
        if 'NO' in field_col_map:
            col_idx = field_col_map['NO']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                no_count = parse_aux_contact(val, dash_means_zero=True)
        
        if 'NC' in field_col_map:
            col_idx = field_col_map['NC']
            if col_idx < len(row):
                val = row.iloc[col_idx] if hasattr(row, 'iloc') else row[col_idx]
                nc_count = parse_aux_contact(val, dash_means_zero=True)
        
        # Use current_frame_label (from explicit FRAME- rows)
        frame_label = current_frame_label
        
        # Add canonical row - v6 schema
        canonical_rows.append({
            'make': lock['oem'],
            'series_name': lock['series_name'],
            'series_bucket': lock['series_bucket'],
            'item_producttype': 'Contactor',
            'business_subcategory': 'Power Contactor',
            'source_page': 8,  # v6 uses numeric
            'table_id': table_config['table_id'],
            'frame_label': frame_label,
            'poles': table_config['poles'],
            'base_ref_clean': base_ref_clean,
            'ac1_A': ac1_current,  # v6 uses ac1_A not ac1_current_a
            'ac3_A': ac3_current,  # v6 uses ac3_A not ac3_current_a
            'motor_hp': hp,
            'motor_kw': kw,
            'aux_no': no_count if no_count is not None else 0,  # v6 uses aux_no not aux_no_count
            'aux_nc': nc_count if nc_count is not None else 0,  # v6 uses aux_nc not aux_nc_count
            'notes_raw': None
        })
        
        # Add coil prices - v6 schema
        for coil_info in priced_coils:
            completed_ref = f"{base_ref_clean}{coil_info['variant_code']}"
            coil_prices.append({
                'make': lock['oem'],
                'series_name': lock['series_name'],
                'series_bucket': lock['series_bucket'],
                'currency': lock['source']['currency'],
                'effective_from': lock['source'].get('effective_from', '2025-07-15'),
                'pricelist_ref': lock['source'].get('pricelist_ref', 'WEF 15 Jul 2025'),
                'source_page': 8,  # v6 uses numeric
                'table_id': table_config['table_id'],
                'base_ref_clean': base_ref_clean,
                'coil_code': coil_info['variant_code'],
                'voltage_type': coil_info['voltage_type'],
                'voltage_V': coil_info['voltage_V'],  # v6 uses voltage_V not voltage_value
                'completed_ref': completed_ref,  # v6 uses completed_ref not completed_sku
                'price_inr': coil_info['price']  # v6 uses price_inr not price
            })
    
    # Deduplicate canonical rows by base_ref_clean
    seen_bases = set()
    deduped_canonical = []
    for row in canonical_rows:
        base = row['base_ref_clean']
        if base and base not in seen_bases:
            seen_bases.add(base)
            deduped_canonical.append(row)
    
    print(f"  ✓ P8_T3: {len(deduped_canonical)} canonical rows, {len(coil_prices)} coil prices")
    
    return deduped_canonical, coil_prices

def main():
    parser = argparse.ArgumentParser(description='LC1E Page-8 Extraction - v6 Format')
    parser.add_argument('--input_xlsx', required=True, help='Input raw pricelist XLSX file')
    parser.add_argument('--out', required=True, help='Output canonical Excel file path')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("LC1E Page-8 Extraction - v6 Format (Semantic Lock Compliant)")
    print("=" * 80)
    print()
    
    # Load semantic lock
    print("Loading semantic lock...")
    lock = load_semantic_lock()
    print(f"✓ Loaded: {lock['status']} - {lock['series_bucket']} {lock['series_name']}")
    print()
    
    # Load raw XLSX
    print(f"Loading input XLSX: {args.input_xlsx}")
    df = pd.read_excel(args.input_xlsx, sheet_name=0, header=None)
    print(f"✓ Loaded: {len(df)} rows, {len(df.columns)} columns")
    print()
    
    # Extract P8_T1
    print("Extracting P8_T1 (3P AC Control 6A–95A)...")
    p8_t1_canonical, p8_t1_prices = extract_p8_t1(args.input_xlsx, lock, df)
    print()
    
    # Extract P8_T3
    print("Extracting P8_T3 (3P AC Control High Ratings)...")
    p8_t3_canonical, p8_t3_prices = extract_p8_t3(args.input_xlsx, lock, df)
    print()
    
    # Write to Excel with v6 sheet names
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("Writing output...")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        pd.DataFrame(p8_t1_canonical).to_excel(writer, sheet_name='P8_T1_CANONICAL_ROWS', index=False)
        pd.DataFrame(p8_t1_prices).to_excel(writer, sheet_name='P8_T1_COIL_PRICES', index=False)
        pd.DataFrame(p8_t3_canonical).to_excel(writer, sheet_name='P8_T3_CANONICAL_ROWS', index=False)
        pd.DataFrame(p8_t3_prices).to_excel(writer, sheet_name='P8_T3_COIL_PRICES', index=False)
    
    print()
    print("=" * 80)
    print(f"✓ Created v6-format workbook: {output_path}")
    print(f"  - P8_T1_CANONICAL_ROWS: {len(p8_t1_canonical)} rows (expected: 21)")
    print(f"  - P8_T1_COIL_PRICES: {len(p8_t1_prices)} rows (expected: 40)")
    print(f"  - P8_T3_CANONICAL_ROWS: {len(p8_t3_canonical)} rows (expected: 8)")
    print(f"  - P8_T3_COIL_PRICES: {len(p8_t3_prices)} rows (expected: 15)")
    print("=" * 80)
    
    # Validate row counts
    expected_counts = {
        'P8_T1_CANONICAL_ROWS': 21,
        'P8_T1_COIL_PRICES': 40,
        'P8_T3_CANONICAL_ROWS': 8,
        'P8_T3_COIL_PRICES': 15
    }
    
    actual_counts = {
        'P8_T1_CANONICAL_ROWS': len(p8_t1_canonical),
        'P8_T1_COIL_PRICES': len(p8_t1_prices),
        'P8_T3_CANONICAL_ROWS': len(p8_t3_canonical),
        'P8_T3_COIL_PRICES': len(p8_t3_prices)
    }
    
    mismatches = []
    for sheet, expected in expected_counts.items():
        actual = actual_counts[sheet]
        if actual != expected:
            mismatches.append(f"{sheet}: {actual} (expected {expected})")
    
    if mismatches:
        print()
        print("⚠ WARNING: Row count mismatches:")
        for mismatch in mismatches:
            print(f"  - {mismatch}")
    else:
        print()
        print("✓ All row counts match v6 expectations")

if __name__ == '__main__':
    main()

