#!/usr/bin/env python3
"""
Review Item Master Excel File
Analyzes Excel file structure and compares with patch requirements
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from collections import defaultdict


def analyze_excel_structure(file_path):
    """Analyze Excel file structure and extract metadata."""
    print("=" * 80)
    print("Excel File Structure Analysis")
    print("=" * 80)
    print(f"File: {file_path}\n")
    
    try:
        xls = pd.ExcelFile(file_path)
        sheet_info = []
        
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, nrows=5)  # Read first 5 rows for structure
            info = {
                'name': sheet_name,
                'columns': list(df.columns),
                'row_count_estimate': len(pd.read_excel(xls, sheet_name=sheet_name)),
                'type': categorize_sheet(sheet_name, df)
            }
            sheet_info.append(info)
        
        return sheet_info, xls
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        sys.exit(1)


def categorize_sheet(sheet_name, df):
    """Categorize sheet as README, Process, or Data."""
    name_lower = sheet_name.lower()
    
    if 'readme' in name_lower or 'doc' in name_lower or 'guide' in name_lower:
        return 'README'
    elif 'process' in name_lower or 'workflow' in name_lower or 'instruction' in name_lower:
        return 'PROCESS'
    elif 'data' in name_lower or 'master' in name_lower or 'item' in name_lower:
        return 'DATA'
    else:
        # Check column structure
        if len(df.columns) < 5:
            return 'README/PROCESS'
        else:
            return 'DATA'


def check_terminology_conflicts(sheet_info):
    """Check for terminology conflicts with patch requirements."""
    print("\n" + "=" * 80)
    print("Terminology Conflict Analysis")
    print("=" * 80)
    
    conflicts = []
    findings = []
    
    for sheet in sheet_info:
        if sheet['type'] == 'DATA':
            columns = [col.lower() for col in sheet['columns']]
            
            # Check for SC_Lx usage
            sc_columns = [col for col in columns if 'sc_l' in col or 'sc_l1' in col or 'sc_l2' in col or 'sc_l3' in col or 'sc_l4' in col]
            if sc_columns:
                findings.append({
                    'sheet': sheet['name'],
                    'issue': 'SC_Lx columns found',
                    'columns': sc_columns,
                    'severity': 'HIGH',
                    'note': 'Need to verify if used as SCL or Capability'
                })
            
            # Check for business_subcategory vs business_segment
            if 'business_subcategory' in columns:
                conflicts.append({
                    'sheet': sheet['name'],
                    'issue': 'Uses business_subcategory (legacy alias)',
                    'recommendation': 'Should use business_segment as canonical',
                    'severity': 'MEDIUM'
                })
            
            # Check for capability_class columns
            capability_cols = [col for col in columns if 'capability_class' in col or 'capability' in col]
            if capability_cols:
                findings.append({
                    'sheet': sheet['name'],
                    'issue': 'Capability columns found',
                    'columns': capability_cols,
                    'severity': 'INFO',
                    'note': 'Verify alignment with SC_Lx separation'
                })
            
            # Check for generic naming violations (vendor/series in generic names)
            generic_cols = [col for col in columns if 'generic' in col and ('name' in col or 'description' in col)]
            if generic_cols:
                findings.append({
                    'sheet': sheet['name'],
                    'issue': 'Generic name columns found - need content validation',
                    'columns': generic_cols,
                    'severity': 'MEDIUM',
                    'note': 'Check for vendor/series neutrality violations'
                })
    
    return conflicts, findings


def analyze_readme_sheets(xls, sheet_info):
    """Analyze README sheets for terminology and definitions."""
    print("\n" + "=" * 80)
    print("README Sheets Analysis")
    print("=" * 80)
    
    readme_findings = []
    
    for sheet in sheet_info:
        if sheet['type'] == 'README':
            try:
                df = pd.read_excel(xls, sheet_name=sheet['name'])
                content = df.to_string()
                
                # Check for key terminology
                checks = {
                    'SC_Lx mentioned': 'sc_l' in content.lower(),
                    'Capability mentioned': 'capability' in content.lower(),
                    'business_subcategory mentioned': 'business_subcategory' in content.lower(),
                    'business_segment mentioned': 'business_segment' in content.lower(),
                    'SCL mentioned': 'scl' in content.lower() or 'structural' in content.lower(),
                }
                
                readme_findings.append({
                    'sheet': sheet['name'],
                    'checks': checks,
                    'row_count': len(df)
                })
                
            except Exception as e:
                print(f"  ⚠️  Error reading README sheet {sheet['name']}: {e}")
    
    return readme_findings


def generate_comparison_report(sheet_info, conflicts, findings, readme_findings):
    """Generate comparison report with patch requirements."""
    print("\n" + "=" * 80)
    print("Comparison Report - Excel vs Patch Requirements")
    print("=" * 80)
    
    report = {
        'sheet_summary': sheet_info,
        'conflicts': conflicts,
        'findings': findings,
        'readme_analysis': readme_findings,
        'recommendations': []
    }
    
    # Generate recommendations
    if conflicts:
        report['recommendations'].append({
            'priority': 'HIGH',
            'action': 'Update terminology to align with patch requirements',
            'details': conflicts
        })
    
    if any('SC_Lx' in str(f.get('columns', [])) for f in findings):
        report['recommendations'].append({
            'priority': 'CRITICAL',
            'action': 'Verify SC_Lx usage - must be SCL (Structural), not Capability',
            'details': 'Per patch requirements, SC_Lx = Structural Construction Layers only'
        })
    
    return report


def print_report(report):
    """Print formatted report."""
    print("\n" + "=" * 80)
    print("DETAILED FINDINGS")
    print("=" * 80)
    
    print("\n1. SHEET SUMMARY")
    print("-" * 80)
    for sheet in report['sheet_summary']:
        print(f"\n  Sheet: {sheet['name']}")
        print(f"    Type: {sheet['type']}")
        print(f"    Rows: ~{sheet['row_count_estimate']}")
        print(f"    Columns: {len(sheet['columns'])}")
        if len(sheet['columns']) <= 10:
            print(f"    Column names: {', '.join(sheet['columns'])}")
        else:
            print(f"    First 10 columns: {', '.join(sheet['columns'][:10])}...")
    
    if report['conflicts']:
        print("\n2. TERMINOLOGY CONFLICTS")
        print("-" * 80)
        for conflict in report['conflicts']:
            print(f"\n  Sheet: {conflict['sheet']}")
            print(f"    Issue: {conflict['issue']}")
            print(f"    Severity: {conflict['severity']}")
            print(f"    Recommendation: {conflict['recommendation']}")
    
    if report['findings']:
        print("\n3. STRUCTURAL FINDINGS")
        print("-" * 80)
        for finding in report['findings']:
            print(f"\n  Sheet: {finding['sheet']}")
            print(f"    Issue: {finding['issue']}")
            print(f"    Severity: {finding['severity']}")
            if 'columns' in finding:
                print(f"    Columns: {finding['columns']}")
            if 'note' in finding:
                print(f"    Note: {finding['note']}")
    
    if report['readme_analysis']:
        print("\n4. README SHEETS ANALYSIS")
        print("-" * 80)
        for readme in report['readme_analysis']:
            print(f"\n  Sheet: {readme['sheet']}")
            print(f"    Rows: {readme['row_count']}")
            for check, result in readme['checks'].items():
                status = "✓" if result else "✗"
                print(f"    {status} {check}")
    
    if report['recommendations']:
        print("\n5. RECOMMENDATIONS")
        print("-" * 80)
        for rec in report['recommendations']:
            print(f"\n  Priority: {rec['priority']}")
            print(f"  Action: {rec['action']}")
            if 'details' in rec:
                if isinstance(rec['details'], str):
                    print(f"  Details: {rec['details']}")
                else:
                    print(f"  Details: {len(rec['details'])} items")


def main():
    parser = argparse.ArgumentParser(description='Review Item Master Excel file')
    parser.add_argument('file_path', help='Path to Excel file')
    parser.add_argument('--output', help='Output report file (optional)')
    
    args = parser.parse_args()
    
    file_path = Path(args.file_path)
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        print("\nPlease check the file path. Expected location:")
        print("  tools/input/revised item master/item_master_020126.xlsx")
        sys.exit(1)
    
    # Analyze structure
    sheet_info, xls = analyze_excel_structure(file_path)
    
    # Check for conflicts
    conflicts, findings = check_terminology_conflicts(sheet_info)
    
    # Analyze README sheets
    readme_findings = analyze_readme_sheets(xls, sheet_info)
    
    # Generate report
    report = generate_comparison_report(sheet_info, conflicts, findings, readme_findings)
    
    # Print report
    print_report(report)
    
    # Save to file if requested
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n✓ Report saved to: {args.output}")
    
    print("\n" + "=" * 80)
    print("Analysis Complete")
    print("=" * 80)


if __name__ == '__main__':
    main()

