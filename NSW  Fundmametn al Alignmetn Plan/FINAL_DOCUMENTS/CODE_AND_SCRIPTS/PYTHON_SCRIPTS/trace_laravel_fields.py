#!/usr/bin/env python3
"""
Laravel Field Traceability Parser

Purpose:
    Scans Laravel codebase for field references (Customer_ID, Product_ID, etc.)
    Ensures fields in Generic/Specific are mapped to Laravel models/controllers/routes.

Usage:
    python3 scripts/governance/trace_laravel_fields.py [--laravel-path path/to/laravel]
"""

import os
import re
import argparse
from pathlib import Path
from collections import defaultdict

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent

# Common field patterns to search for
FIELD_PATTERNS = [
    r'Customer_ID',
    r'Product_ID',
    r'ProductType',
    r'Make',
    r'SKU',
    r'SkuType',
    r'L2',
    r'ProductResolutionService',
    r'ProductArchiveService',
]

def find_laravel_path(base_dir):
    """Try to find Laravel application path."""
    # Common Laravel locations
    possible_paths = [
        base_dir / "laravel",
        base_dir / "app",
        base_dir.parent / "laravel",
        base_dir.parent / "app",
    ]
    
    for path in possible_paths:
        if (path / "artisan").exists() or (path / "composer.json").exists():
            composer_json = path / "composer.json"
            if composer_json.exists():
                with open(composer_json, 'r') as f:
                    content = f.read()
                    if '"laravel/framework"' in content or '"laravel/laravel"' in content:
                        return path
    
    return None

def scan_file(file_path, patterns):
    """Scan a file for field patterns."""
    matches = defaultdict(list)
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    matches[pattern].append({
                        'line': line_num,
                        'content': line.strip()[:100]  # First 100 chars
                    })
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
    
    return matches

def scan_laravel_directory(laravel_path):
    """Scan Laravel directory for field references."""
    results = defaultdict(lambda: defaultdict(list))
    
    # Directories to scan
    scan_dirs = ['app', 'routes', 'database/migrations', 'resources/views']
    
    for scan_dir in scan_dirs:
        dir_path = laravel_path / scan_dir
        if not dir_path.exists():
            continue
        
        print(f"📂 Scanning {scan_dir}...")
        
        # File extensions to check
        extensions = ['.php', '.blade.php', '.js', '.vue']
        
        for ext in extensions:
            for file_path in dir_path.rglob(f'*{ext}'):
                if file_path.is_file():
                    matches = scan_file(file_path, FIELD_PATTERNS)
                    if matches:
                        rel_path = file_path.relative_to(laravel_path)
                        for pattern, occurrences in matches.items():
                            results[pattern][str(rel_path)].extend(occurrences)
    
    return results

def generate_report(results, output_file=None):
    """Generate traceability report."""
    report_lines = [
        "# Laravel Field Traceability Report",
        f"Generated: {Path(__file__).stat().st_mtime}",
        "",
        "## Summary",
        ""
    ]
    
    total_matches = sum(len(files) for files in results.values())
    report_lines.append(f"Total field patterns found: {len(results)}")
    report_lines.append(f"Total file matches: {total_matches}")
    report_lines.append("")
    
    for pattern, files in sorted(results.items()):
        report_lines.append(f"## Field: `{pattern}`")
        report_lines.append("")
        
        for file_path, occurrences in sorted(files.items()):
            report_lines.append(f"### {file_path}")
            report_lines.append("")
            for occ in occurrences[:10]:  # Limit to 10 per file
                report_lines.append(f"  Line {occ['line']}: {occ['content']}")
            if len(occurrences) > 10:
                report_lines.append(f"  ... and {len(occurrences) - 10} more")
            report_lines.append("")
    
    report = "\n".join(report_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 Report saved to {output_file}")
    else:
        print(report)
    
    return report

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Trace Laravel field references')
    parser.add_argument('--laravel-path', '-p', 
                       help='Path to Laravel application root')
    parser.add_argument('--output', '-o',
                       help='Output report file path')
    
    args = parser.parse_args()
    
    # Find Laravel path
    if args.laravel_path:
        laravel_path = Path(args.laravel_path)
    else:
        laravel_path = find_laravel_path(BASE_DIR)
    
    if not laravel_path or not laravel_path.exists():
        print("❌ Laravel application not found")
        print("   Please specify --laravel-path or ensure Laravel is in a standard location")
        return 1
    
    print(f"🔍 Scanning Laravel application at: {laravel_path}")
    
    results = scan_laravel_directory(laravel_path)
    
    if not results:
        print("⚠️  No field references found")
        return 0
    
    output_path = None
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = BASE_DIR / output_path
    
    generate_report(results, output_path)
    
    print(f"\n✅ Traceability scan complete")
    print(f"   Found {len(results)} field patterns across Laravel codebase")
    
    return 0

if __name__ == "__main__":
    exit(main())

