#!/usr/bin/env python3
"""
Archive Governance Artifacts

Purpose:
    Gathers specified folders/files and packages them into a versioned archive ZIP
    for NEPL artifacts. Ensures all source files, configs, diagrams, and outputs
    are versioned and locked.

Usage:
    python3 scripts/governance/archive_artifacts.py [--version v1.0] [--output archive.zip]
"""

import os
import zipfile
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent

# Default directories to archive
DEFAULT_ARCHIVE_DIRS = [
    "docs",
    "scripts",
    ".github/workflows",
]

# Default files to archive
DEFAULT_ARCHIVE_FILES = [
    "README.md",
    "mkdocs.yml",
]

def create_archive(version, output_path, include_dirs=None, include_files=None):
    """Create ZIP archive of governance artifacts."""
    if include_dirs is None:
        include_dirs = DEFAULT_ARCHIVE_DIRS
    if include_files is None:
        include_files = DEFAULT_ARCHIVE_FILES
    
    archive_name = f"NEPL_Governance_Artifacts_v{version}_{datetime.now().strftime('%Y%m%d')}.zip"
    if output_path:
        archive_path = Path(output_path)
    else:
        archive_path = BASE_DIR / archive_name
    
    print(f"📦 Creating archive: {archive_path}")
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Archive directories
        for dir_name in include_dirs:
            dir_path = BASE_DIR / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"  📁 Adding directory: {dir_name}")
                for root, dirs, files in os.walk(dir_path):
                    # Skip hidden files and common ignore patterns
                    files = [f for f in files if not f.startswith('.')]
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(BASE_DIR)
                        zipf.write(file_path, arcname)
                        print(f"    ✓ {arcname}")
            else:
                print(f"  ⚠️  Directory not found: {dir_name}")
        
        # Archive individual files
        for file_name in include_files:
            file_path = BASE_DIR / file_name
            if file_path.exists() and file_path.is_file():
                print(f"  📄 Adding file: {file_name}")
                zipf.write(file_path, file_name)
            else:
                print(f"  ⚠️  File not found: {file_name}")
        
        # Add manifest
        manifest = f"""NEPL Governance Artifacts Archive
Version: {version}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Archive: {archive_name}

Contents:
- Governance documentation (docs/)
- Automation scripts (scripts/)
- CI/CD workflows (.github/workflows/)
- Configuration files (mkdocs.yml, README.md)

This archive represents a frozen snapshot of governance artifacts
for audit and compliance purposes.
"""
        zipf.writestr("ARCHIVE_MANIFEST.txt", manifest)
    
    # Get archive size
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    print(f"\n✅ Archive created: {archive_path}")
    print(f"   Size: {size_mb:.2f} MB")
    
    return archive_path

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Archive governance artifacts')
    parser.add_argument('--version', '-v', default='1.0',
                       help='Version tag for archive (default: 1.0)')
    parser.add_argument('--output', '-o',
                       help='Output archive file path')
    parser.add_argument('--dirs', nargs='+',
                       help='Additional directories to include')
    parser.add_argument('--files', nargs='+',
                       help='Additional files to include')
    
    args = parser.parse_args()
    
    include_dirs = DEFAULT_ARCHIVE_DIRS.copy()
    if args.dirs:
        include_dirs.extend(args.dirs)
    
    include_files = DEFAULT_ARCHIVE_FILES.copy()
    if args.files:
        include_files.extend(args.files)
    
    archive_path = create_archive(
        args.version,
        args.output,
        include_dirs,
        include_files
    )
    
    print(f"\n🎉 Archive ready for distribution")
    print(f"   Location: {archive_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())

