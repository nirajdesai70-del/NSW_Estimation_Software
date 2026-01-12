#!/usr/bin/env python3
"""
Validate Canonical Extraction Against Source Files

Purpose:
- Cross-validates canonical extraction against input XLSX/PDF
- Detects missing frames, incorrect coil codes, missing base refs
- Provides validation report without requiring v6 reference file
- Self-validating pipeline verification
"""

import argparse
import pandas as pd
import sys
import re
from pathlib import Path


def normalize_row_to_string(row):
    """Normalize a row to a single string for pattern matching."""
    return ' '.join([str(v) if pd.notna(v) else '' for v in row])


def extract_base_refs_from_xlsx(xlsx_file, sheet_name='Table 1'):
    """
    Extract all base references from source XLSX.
    Returns set of base refs found in source.
    """
    try:
        df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
        base_refs = set()
        base_ref_pattern = re.compile(r'LC1E[0-9A-Z]+', re.IGNORECASE)
        
        for idx in range(len(df)):
            row_str = normalize_row_to_string(df.iloc[idx])
            matches = base_ref_pattern.findall(row_str)
            for match in matches:
                # Clean up (remove *, #, coil codes)
                clean_ref = re.sub(r'[\*#]+', '', match).strip()
                clean_ref = re.sub(r'(M7|N5|F7|B7|BD|M5WB|N5WB|M5|N7)$', '', clean_ref, flags=re.IGNORECASE).strip()
                if clean_ref and len(clean_ref) > 4:  # Valid base ref
                    base_refs.add(clean_ref.upper())
        
        return base_refs
    except Exception as e:
        print(f"⚠️  Error reading XLSX: {e}")
        return set()


def extract_frame_labels_from_xlsx(xlsx_file, sheet_name='Table 1'):
    """
    Extract all FRAME- labels from source XLSX.
    Returns dict mapping base_ref -> frame_label (if found nearby).
    """
    try:
        df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
        frame_labels = {}
        frame_pattern = re.compile(r'FRAME-[\dA-Z]+', re.IGNORECASE)
        base_ref_pattern = re.compile(r'LC1E[0-9A-Z]+', re.IGNORECASE)
        
        current_frame = ''
        for idx in range(len(df)):
            row_str = normalize_row_to_string(df.iloc[idx])
            
            # Check for FRAME- label
            frame_match = frame_pattern.search(row_str)
            if frame_match:
                current_frame = frame_match.group(0).upper()
            
            # Check for base refs in this row
            base_matches = base_ref_pattern.findall(row_str)
            for match in base_matches:
                clean_ref = re.sub(r'[\*#]+', '', match).strip()
                clean_ref = re.sub(r'(M7|N5|F7|B7|BD|M5WB|N5WB|M5|N7)$', '', clean_ref, flags=re.IGNORECASE).strip()
                if clean_ref and len(clean_ref) > 4:
                    # If we have a current frame, associate it
                    if current_frame:
                        frame_labels[clean_ref.upper()] = current_frame
        
        return frame_labels
    except Exception as e:
        print(f"⚠️  Error extracting frames from XLSX: {e}")
        return {}


def extract_coil_codes_from_xlsx(xlsx_file, sheet_name='Table 1'):
    """
    Extract coil codes mentioned in source XLSX.
    Returns set of coil codes found.
    """
    try:
        df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
        coil_codes = set()
        coil_pattern = re.compile(r'\b(M7|N5|F7|B7|BD|M5WB|N5WB|M5|N7)\b', re.IGNORECASE)
        
        for idx in range(len(df)):
            row_str = normalize_row_to_string(df.iloc[idx])
            matches = coil_pattern.findall(row_str)
            for match in matches:
                coil_codes.add(match.upper())
        
        return coil_codes
    except Exception as e:
        print(f"⚠️  Error extracting coil codes from XLSX: {e}")
        return set()


def check_section_coil_codes(xlsx_file, sheet_name='Table 1'):
    """
    Check which coil codes are present in which sections.
    Returns dict: section -> set of coil codes
    """
    try:
        df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
        sections = {}
        current_section = None
        coil_pattern = re.compile(r'\b(M7|N5|F7|B7|BD|M5WB|N5WB|M5|N7)\b', re.IGNORECASE)
        
        for idx in range(len(df)):
            row_str = normalize_row_to_string(df.iloc[idx])
            
            # Detect section headers
            if '3 POLE AC' in row_str.upper() or '3P AC' in row_str.upper():
                current_section = '3P_AC'
                sections[current_section] = set()
            elif '3 POLE DC' in row_str.upper() or '3P DC' in row_str.upper():
                current_section = '3P_DC'
                sections[current_section] = set()
            elif '4 POLE' in row_str.upper() or '4P' in row_str.upper():
                current_section = '4P_AC'
                sections[current_section] = set()
            
            # Collect coil codes in current section
            if current_section:
                matches = coil_pattern.findall(row_str)
                for match in matches:
                    sections[current_section].add(match.upper())
        
        return sections
    except Exception as e:
        print(f"⚠️  Error checking sections: {e}")
        return {}


def validate_canonical_against_source(canonical_file, xlsx_file, pdf_file=None):
    """
    Validate canonical extraction against source files.
    """
    print("=" * 60)
    print("Canonical Validation Against Source Files")
    print("=" * 60)
    print(f"Canonical file: {canonical_file}")
    print(f"Source XLSX: {xlsx_file}")
    if pdf_file:
        print(f"Source PDF: {pdf_file}")
    print()
    
    # Read canonical data
    try:
        canonical_rows = pd.read_excel(canonical_file, sheet_name='LC1E_CANONICAL_ROWS')
        coil_prices = pd.read_excel(canonical_file, sheet_name='LC1E_COIL_CODE_PRICES')
    except Exception as e:
        print(f"❌ Error reading canonical file: {e}")
        return False
    
    print(f"✓ Read canonical data:")
    print(f"  - Canonical rows: {len(canonical_rows)}")
    print(f"  - Coil prices: {len(coil_prices)}")
    print()
    
    # Extract from source XLSX
    print("Extracting data from source XLSX...")
    source_base_refs = extract_base_refs_from_xlsx(xlsx_file)
    source_frame_labels = extract_frame_labels_from_xlsx(xlsx_file)
    source_coil_codes = extract_coil_codes_from_xlsx(xlsx_file)
    section_coil_codes = check_section_coil_codes(xlsx_file)
    
    print(f"✓ Extracted from source:")
    print(f"  - Base refs found: {len(source_base_refs)}")
    print(f"  - Frame labels found: {len(source_frame_labels)}")
    print(f"  - Coil codes found: {sorted(source_coil_codes)}")
    print(f"  - Sections: {list(section_coil_codes.keys())}")
    print()
    
    # Validation checks
    issues = []
    warnings = []
    
    # Check 1: Base refs in canonical vs source
    canonical_base_refs = set(canonical_rows['base_ref_clean'].dropna().str.upper())
    missing_in_canonical = source_base_refs - canonical_base_refs
    extra_in_canonical = canonical_base_refs - source_base_refs
    
    if missing_in_canonical:
        warnings.append(f"Base refs in source but not in canonical ({len(missing_in_canonical)}): {sorted(list(missing_in_canonical))[:10]}")
    if extra_in_canonical:
        warnings.append(f"Base refs in canonical but not in source ({len(extra_in_canonical)}): {sorted(list(extra_in_canonical))[:10]}")
    
    # Check 2: Frame labels
    canonical_frames = canonical_rows[canonical_rows['frame_label'].notna()]['frame_label'].unique()
    missing_frames = []
    for base_ref in canonical_base_refs:
        canonical_frame = canonical_rows[canonical_rows['base_ref_clean'].str.upper() == base_ref]['frame_label'].iloc[0] if len(canonical_rows[canonical_rows['base_ref_clean'].str.upper() == base_ref]) > 0 else None
        if pd.isna(canonical_frame) or canonical_frame == '':
            missing_frames.append(base_ref)
        # Check against source if available
        if base_ref in source_frame_labels:
            source_frame = source_frame_labels[base_ref]
            if canonical_frame and str(canonical_frame).upper() != source_frame:
                warnings.append(f"Frame mismatch for {base_ref}: canonical={canonical_frame}, source={source_frame}")
    
    if missing_frames:
        issues.append(f"Missing frame labels ({len(missing_frames)}): {missing_frames[:10]}")
    
    # Check 3: Coil codes
    canonical_coil_codes = set(coil_prices['coil_code'].str.upper().unique())
    missing_coil_codes = source_coil_codes - canonical_coil_codes
    extra_coil_codes = canonical_coil_codes - source_coil_codes
    
    if missing_coil_codes:
        warnings.append(f"Coil codes in source but not in canonical: {sorted(missing_coil_codes)}")
    if extra_coil_codes:
        warnings.append(f"Coil codes in canonical but not in source: {sorted(extra_coil_codes)}")
    
    # Check 4: Section-specific coil codes
    # Check if DC coils are in 3P_AC section (should not be)
    canonical_table_ids = set(canonical_rows['table_id'].dropna().unique())
    if 'LC1E_3P_AC' in canonical_table_ids:
        # Check if BD (DC coil) is in 3P AC canonical
        ac_coil_codes_in_canonical = set(coil_prices[coil_prices['table_id'] == 'LC1E_3P_AC']['coil_code'].str.upper().unique())
        dc_in_ac = {'BD'} & ac_coil_codes_in_canonical
        if dc_in_ac:
            issues.append(f"❌ CRITICAL: DC coil codes (BD) found in 3P AC canonical table. DC coils should be in separate 3P DC section.")
    
    # Check if source shows DC section but canonical doesn't have it
    if '3P_DC' in section_coil_codes and 'LC1E_3P_DC' not in canonical_table_ids:
        issues.append(f"❌ CRITICAL: Source has 3P DC section with coil codes {section_coil_codes['3P_DC']}, but canonical doesn't have LC1E_3P_DC table.")
    
    # Check 5: Frame distribution
    frame_dist = canonical_rows['frame_label'].value_counts()
    print("Frame label distribution in canonical:")
    print(frame_dist.to_string())
    
    # Check for missing FRAME-4 (user mentioned this)
    if 'FRAME-4' not in frame_dist.index:
        issues.append("❌ CRITICAL: FRAME-4 not found in canonical. User reported many FRAME-4 items are missing.")
    else:
        frame4_count = frame_dist.get('FRAME-4', 0)
        if frame4_count < 5:  # Expect more FRAME-4 items
            warnings.append(f"⚠️  FRAME-4 count is low ({frame4_count}). Source may have more FRAME-4 base refs.")
    
    # Check if FRAME-9 is being overused (may be a section header, not actual frame)
    if 'FRAME-9' in frame_dist.index:
        frame9_count = frame_dist.get('FRAME-9', 0)
        if frame9_count > len(canonical_rows) * 0.5:  # More than 50% of rows
            warnings.append(f"⚠️  FRAME-9 is assigned to {frame9_count} rows ({frame9_count/len(canonical_rows)*100:.1f}%). This may be a section header, not actual frame labels. Review frame carry-forward logic.")
    
    # Print results
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    
    if issues:
        print("\n❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ No critical issues found")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("\n✅ No warnings")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Canonical base refs: {len(canonical_base_refs)}")
    print(f"Source base refs: {len(source_base_refs)}")
    print(f"Match: {len(canonical_base_refs & source_base_refs)} common")
    print(f"Canonical coil codes: {sorted(canonical_coil_codes)}")
    print(f"Source coil codes: {sorted(source_coil_codes)}")
    print(f"Frame labels in canonical: {len(canonical_frames)} unique frames")
    
    return len(issues) == 0


def main():
    parser = argparse.ArgumentParser(description='Validate Canonical Extraction Against Source Files')
    parser.add_argument('--canonical', required=True, help='Canonical Excel file to validate')
    parser.add_argument('--xlsx', required=True, help='Source XLSX file')
    parser.add_argument('--pdf', help='Source PDF file (optional, for future PDF parsing)')
    parser.add_argument('--out', help='Output validation report file (optional)')
    
    args = parser.parse_args()
    
    success = validate_canonical_against_source(args.canonical, args.xlsx, args.pdf)
    
    if args.out:
        # Write validation report to file
        report = f"Validation Report\n"
        report += f"Canonical: {args.canonical}\n"
        report += f"Source: {args.xlsx}\n"
        report += f"Status: {'PASS' if success else 'FAIL'}\n"
        with open(args.out, 'w') as f:
            f.write(report)
        print(f"\n✓ Validation report written to: {args.out}")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

