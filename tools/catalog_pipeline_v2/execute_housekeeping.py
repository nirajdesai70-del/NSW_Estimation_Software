#!/usr/bin/env python3
"""
Catalog Pipeline v2 - Safe Housekeeping Script (Python)

Purpose: Execute the housekeeping plan to organize scripts and archive execution debris
Usage: python3 execute_housekeeping.py [--phase1-only] [--dry-run]

This script:
1. Creates ARCH_EXECUTION structure
2. Backs up scripts/ folder
3. Safely tags active scripts (only if shebang exists)
4. Archives output debris
5. Archives documentation debris
6. Creates stub files for moved scripts
7. Creates README files

Safety features:
- Full backup before any moves
- Stub files for moved scripts (prevents broken references)
- Safe script tagging (only shebang files, checks for existing tags)
- Two-phase approach (Phase 1 safe, Phase 2 script moves)
- Dry-run mode for preview
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class HousekeepingExecutor:
    def __init__(self, root_dir: Path, dry_run: bool = False, phase1_only: bool = False):
        self.root_dir = Path(root_dir).resolve()
        self.dry_run = dry_run
        self.phase1_only = phase1_only
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.arch_base = self.root_dir / "ARCH_EXECUTION" / f"2026-01-03_PHASE5_CLEANUP_{self.timestamp}"
        
    def log(self, message: str, level: str = "INFO"):
        """Print log message with prefix."""
        prefix = {
            "INFO": "📋",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DRY": "🔍 [DRY-RUN]"
        }.get(level, "📋")
        print(f"{prefix} {message}")
        
    def ensure_dir(self, path: Path):
        """Create directory if it doesn't exist."""
        if not self.dry_run:
            path.mkdir(parents=True, exist_ok=True)
        self.log(f"Created directory: {path.relative_to(self.root_dir)}", "INFO")
        
    def backup_scripts(self):
        """Backup scripts/ folder before any modifications."""
        scripts_dir = self.root_dir / "scripts"
        if not scripts_dir.exists():
            self.log("No scripts/ folder found, skipping backup", "WARNING")
            return
            
        backup_dir = self.arch_base / "backup" / "scripts"
        self.log(f"Backing up scripts/ to {backup_dir.relative_to(self.root_dir)}", "INFO")
        
        if not self.dry_run:
            shutil.copytree(scripts_dir, backup_dir, dirs_exist_ok=True)
        self.log("Backup complete", "SUCCESS")
        
    def safe_tag_script(self, script_path: Path, tag: str) -> bool:
        """
        Safely tag a script file.
        Only tags files with shebang. Checks for existing tag.
        Returns True if tagged, False otherwise.
        """
        if not script_path.exists():
            return False
            
        # Check if already tagged
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if tag in content:
                    self.log(f"  Already tagged: {script_path.name}", "INFO")
                    return False
        except Exception as e:
            self.log(f"  Error reading {script_path.name}: {e}", "WARNING")
            return False
            
        # Only tag files with shebang
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if not first_line.startswith('#!'):
                    self.log(f"  Skipping {script_path.name} (no shebang)", "INFO")
                    return False
        except Exception as e:
            self.log(f"  Error checking shebang in {script_path.name}: {e}", "WARNING")
            return False
            
        # Tag the file (insert after shebang)
        if not self.dry_run:
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                # Insert tag after shebang (line 2)
                if len(lines) > 0:
                    lines.insert(1, f"{tag}\n")
                    
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                    
                self.log(f"  Tagged: {script_path.name}", "SUCCESS")
                return True
            except Exception as e:
                self.log(f"  Error tagging {script_path.name}: {e}", "ERROR")
                return False
        else:
            self.log(f"  [DRY-RUN] Would tag: {script_path.name}", "DRY")
            return True
            
    def create_stub(self, original_path: Path, archive_path: Path):
        """Create a stub file at original location pointing to archive."""
        if not self.dry_run:
            stub_content = f'''#!/usr/bin/env python3
"""
STUB FILE - Script has been moved to archive.

Original: {original_path.name}
Moved to: {archive_path.relative_to(self.root_dir)}

This script has been archived and should not be used.
If you need this script, find it in ARCH_EXECUTION/one_off_scripts/

To restore:
    cp {archive_path} {original_path}
"""

import sys

print("=" * 60)
print("ERROR: This script has been moved to archive.")
print("=" * 60)
print(f"Original: {original_path.name}")
print(f"Archived to: {archive_path.relative_to(self.root_dir)}")
print("")
print("This script is no longer in active use.")
print("If you need it, copy it back from the archive location.")
print("=" * 60)
sys.exit(1)
'''
            with open(original_path, 'w', encoding='utf-8') as f:
                f.write(stub_content)
            # Make executable
            os.chmod(original_path, 0o755)
        self.log(f"  Created stub: {original_path.name}", "INFO")
        
    def move_with_stub(self, source: Path, dest: Path, create_stub_file: bool = True):
        """Move file and optionally create stub at original location."""
        if not source.exists():
            return False

        original_path = source  # keep original location
        archived_path = dest

        if not self.dry_run:
            archived_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(original_path), str(archived_path))
            if create_stub_file:
                self.create_stub(original_path, archived_path)
        else:
            self.log(f"  [DRY-RUN] Would move: {original_path.name} -> {archived_path.relative_to(self.root_dir)}", "DRY")

        return True
        
    def phase1_safe_cleanup(self):
        """Phase 1: Safe cleanup (outputs + docs, no script moves)."""
        self.log("=" * 60, "INFO")
        self.log("Phase 1: Safe Cleanup (Outputs + Docs)", "INFO")
        self.log("=" * 60, "INFO")
        self.log("")
        
        # Create archive structure
        self.log("Creating archive structure...", "INFO")
        for subdir in ["tmp_outputs", "test_outputs", "old_outputs", "debug", "docs", "backup"]:
            self.ensure_dir(self.arch_base / subdir)
        self.log("")
        
        # Backup scripts
        self.backup_scripts()
        self.log("")
        
        # Archive output debris
        self.log("Archiving output debris...", "INFO")
        output_dir = self.root_dir / "output"
        if output_dir.exists():
            # Create snapshot
            if not self.dry_run:
                snapshot_dir = self.arch_base / "output_snapshot"
                snapshot_dir.mkdir(exist_ok=True)
                shutil.copytree(output_dir, snapshot_dir / f"output_{self.timestamp}", dirs_exist_ok=True)
            self.log(f"  Created output snapshot", "INFO")
            
            # Move specific debris files
            debris_patterns = [
                ("l1_tmp.xlsx", "tmp_outputs"),
                ("l2_tmp.xlsx", "tmp_outputs"),
                ("*TEST*.xlsx", "test_outputs"),
                ("*DEBUG*", "debug"),
                ("*VISIBILITY*", "debug"),
                ("*FINDER*", "debug"),
            ]
            
            for pattern, subdir in debris_patterns:
                if "*" in pattern:
                    # Use glob
                    for file in output_dir.glob(pattern):
                        dest = self.arch_base / subdir / file.name
                        self.move_with_stub(file, dest, create_stub_file=False)
                else:
                    # Exact match
                    file = output_dir / pattern
                    if file.exists():
                        dest = self.arch_base / subdir / file.name
                        self.move_with_stub(file, dest, create_stub_file=False)
                        
            # Handle lc1e subfolder
            lc1e_dir = output_dir / "lc1e"
            if lc1e_dir.exists():
                self.log("  Reviewing output/lc1e/ subfolder...", "INFO")
                for file in lc1e_dir.glob("*TEST*"):
                    dest = self.arch_base / "tmp_outputs" / file.name
                    self.move_with_stub(file, dest, create_stub_file=False)
                for file in lc1e_dir.glob("*tmp*"):
                    dest = self.arch_base / "tmp_outputs" / file.name
                    self.move_with_stub(file, dest, create_stub_file=False)
                for file in lc1e_dir.glob("*~$*"):
                    dest = self.arch_base / "tmp_outputs" / file.name
                    self.move_with_stub(file, dest, create_stub_file=False)
        self.log("  ✅ Output debris archived", "SUCCESS")
        self.log("")
        
        # Archive documentation
        self.log("Archiving historical documentation...", "INFO")
        protected = {
            "README.md",
            "OPERATING_MODEL.md",
            "NEXT_SERIES_BOOTSTRAP.md",
            "HOUSEKEEPING_PLAN.md",
            "HOUSEKEEPING_SUMMARY.md",
        }
        doc_patterns = [
            "PHASE_2_*.md",
            "PHASE_3_*.md",
            "EXECUTION_*.md",
            "EXCEL_REVIEW_*.md",
            "GAP_*.md",
            "PATCH_REVIEW_*.md",
            "REVIEW_COMPLETE_*.md",
            "CRITICAL_FIXES_APPLIED.md",
            "CANONICAL_EXTRACTOR_*.md",
            "NSW_BUILDER_FIX_COMPLETE.md",
            "FIX_FINDER_VISIBILITY.md",
            "ACCESSORIES_MASTER_GAPS_RESOLVED.md",
            "V6_*.md",
            "OPTION_B_*.md",
            "NEXT_STEPS_LC1E.md",
            "LC1E_STATUS.md",
            "PAUSE_NOTE.md",
        ]
        
        docs_moved = 0
        for pattern in doc_patterns:
            for doc in self.root_dir.glob(pattern):
                if doc.is_file():
                    # Skip protected docs
                    if doc.name in protected:
                        continue
                    dest = self.arch_base / "docs" / doc.name
                    self.move_with_stub(doc, dest, create_stub_file=False)
                    docs_moved += 1
                    
        self.log(f"  ✅ Archived {docs_moved} documentation files", "SUCCESS")
        self.log("")
        self.log("  Keeping governance/reference docs in root:", "INFO")
        self.log("    - README.md", "INFO")
        self.log("    - OPERATING_MODEL.md", "INFO")
        self.log("    - NEXT_SERIES_BOOTSTRAP.md", "INFO")
        self.log("    - SETUP_COMPLETE.md", "INFO")
        self.log("    - HOUSEKEEPING_PLAN.md", "INFO")
        self.log("")
        
        # Create archive README
        self.create_archive_readme()
        
        self.log("=" * 60, "SUCCESS")
        self.log("Phase 1 Complete!", "SUCCESS")
        self.log("=" * 60, "SUCCESS")
        self.log("")
        self.log(f"Archive created at: {self.arch_base.relative_to(self.root_dir)}", "INFO")
        
    def phase2_script_cleanup(self):
        """Phase 2: Script organization (tagging + moving one-off scripts)."""
        if self.phase1_only:
            self.log("Phase 2 skipped (--phase1-only)", "INFO")
            return
            
        self.log("=" * 60, "INFO")
        self.log("Phase 2: Script Organization", "INFO")
        self.log("=" * 60, "INFO")
        self.log("")
        
        scripts_dir = self.root_dir / "scripts"
        if not scripts_dir.exists():
            self.log("No scripts/ folder found", "WARNING")
            return
            
        # Ensure legacy directory exists
        legacy_dir = scripts_dir / "legacy"
        self.ensure_dir(legacy_dir)
        
        # Tag active scripts
        self.log("Tagging active scripts...", "INFO")
        active_scripts = [
            "lc1e_extract_canonical.py",
            "lc1e_build_l2.py",
            "derive_l1_from_l2.py",
            "build_nsw_workbook_from_canonical.py",
            "migrate_sku_price_pack.py",
            "build_l2_from_canonical.py",
            "build_master_workbook.py",
        ]
        
        tagged_count = 0
        for script_name in active_scripts:
            script_path = scripts_dir / script_name
            if script_path.exists():
                if self.safe_tag_script(script_path, "# STATUS: ACTIVE — Phase-5 v1.2 CLEAN"):
                    tagged_count += 1
                    
        self.log(f"  ✅ Tagged {tagged_count} active scripts", "SUCCESS")
        self.log("")
        
        # Move legacy scripts
        self.log("Moving legacy scripts...", "INFO")
        legacy_scripts = [
            "build_nsw_workbook.py",
        ]
        
        for script_name in legacy_scripts:
            script_path = scripts_dir / script_name
            if script_path.exists():
                # Tag before moving
                self.safe_tag_script(script_path, "# STATUS: LEGACY — superseded, do not use")
                dest = legacy_dir / script_name
                self.move_with_stub(script_path, dest, create_stub_file=False)
        self.log("")
        
        # Move one-off scripts (with stubs)
        self.log("Moving one-off scripts to ARCH_EXECUTION (with stubs)...", "INFO")
        one_off_scripts = [
            "apply_phase2_fixes.py",
            "apply_phase2_fixes_openpyxl.py",
            "apply_phase3_fixes.py",
            "review_phase2_file.py",
            "review_item_master_excel.py",
            "validate_against_v6_v2.py",
            "validate_canonical_against_source.py",
            "inspect_lc1e_raw.py",
            "inspect_pricelist.py",
            "build_catalog_chain_master.py",
        ]
        
        one_off_dir = self.arch_base / "one_off_scripts"
        self.ensure_dir(one_off_dir)
        
        moved_count = 0
        for script_name in one_off_scripts:
            script_path = scripts_dir / script_name
            if script_path.exists():
                dest = one_off_dir / script_name
                self.move_with_stub(script_path, dest, create_stub_file=True)
                moved_count += 1
                
        # Handle lc1e subfolder
        lc1e_subdir = scripts_dir / "lc1e"
        if lc1e_subdir.exists():
            dest_subdir = one_off_dir / "lc1e"
            if not self.dry_run:
                shutil.move(str(lc1e_subdir), str(dest_subdir))
            self.log(f"  Moved scripts/lc1e/ subfolder", "INFO")
            
        self.log(f"  ✅ Moved {moved_count} one-off scripts (with stubs)", "SUCCESS")
        self.log("")
        
        # Create scripts README
        self.create_scripts_readme()
        
        self.log("=" * 60, "SUCCESS")
        self.log("Phase 2 Complete!", "SUCCESS")
        self.log("=" * 60, "SUCCESS")
        
    def create_archive_readme(self):
        """Create README in archive directory."""
        readme_path = self.arch_base / "README.md"
        if not self.dry_run:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"""# Housekeeping Archive

Created: {self.timestamp}

This archive contains:
- Output debris (tmp/test/debug files)
- Selected historical markdown execution docs
- Full backup snapshot of scripts/ before any moves
- One-off scripts (if Phase 2 was run)

**No files were deleted.**

## Structure

- `tmp_outputs/` - Temporary intermediate files
- `test_outputs/` - Test execution outputs
- `old_outputs/` - Superseded final outputs
- `debug/` - Debug files and logs
- `docs/` - Historical execution documentation
- `backup/` - Full backup of scripts/ folder
- `one_off_scripts/` - Temporary fix scripts (if Phase 2 run)

## Next Steps

- **Phase 1 only**: Safe cleanup complete. Scripts untouched.
- **Phase 2 run**: Scripts organized. Stub files created for moved scripts.

**Rule:** New execution debris should go to `SoW/` (temporary) or `ARCH/` (after freeze), not here.
""")
        self.log("  Created archive README", "INFO")
        
    def create_scripts_readme(self):
        """Create README in scripts directory."""
        readme_path = self.root_dir / "scripts" / "README.md"
        if not self.dry_run:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("""# Pipeline Scripts

**Active Scripts** (scripts/ root):
- Scripts currently used in Phase-5 LC1E pipeline
- Kept at root level for backward compatibility with `templates/run_pipeline.sh`
- Tagged with `# STATUS: ACTIVE — Phase-5 v1.2 CLEAN`
- Includes both series-specific (lc1e_*) and generic scripts

**Legacy Scripts** (`legacy/`):
- Superseded scripts, kept for reference
- Tagged with `# STATUS: LEGACY — superseded, do not use`

**One-off Scripts** (`ARCH_EXECUTION/`):
- Temporary fix scripts and validation tools
- Moved to execution archive after use
- **Stub files** created at original locations to prevent broken references

## Active Scripts (scripts/ root)

These scripts are kept at the root level for backward compatibility:

- `lc1e_extract_canonical.py` - Extract canonical from raw pricelist (LC1E-specific)
- `lc1e_build_l2.py` - Build L2 from canonical (LC1E-specific)
- `derive_l1_from_l2.py` - Derive L1 from L2 (generic)
- `build_nsw_workbook_from_canonical.py` - Build NSW workbook (PRIMARY, generic)
- `migrate_sku_price_pack.py` - Migrate SKU/price/ratings
- `build_l2_from_canonical.py` - Generic L2 builder (used by template)
- `build_master_workbook.py` - Legacy format builder (optional output)

All active scripts are tagged with: `# STATUS: ACTIVE — Phase-5 v1.2 CLEAN`

**Note:** Active scripts remain at scripts/ root to maintain compatibility with existing templates and execution scripts.
""")
        self.log("  Created scripts README", "INFO")
        
    def run(self):
        """Execute housekeeping."""
        self.log("=" * 60, "INFO")
        self.log("Catalog Pipeline v2 - Safe Housekeeping", "INFO")
        if self.dry_run:
            self.log("DRY-RUN MODE (no changes will be made)", "DRY")
        if self.phase1_only:
            self.log("PHASE 1 ONLY (safe cleanup, no script moves)", "INFO")
        self.log("=" * 60, "INFO")
        self.log("")
        
        try:
            # Phase 1: Safe cleanup
            self.phase1_safe_cleanup()
            
            # Phase 2: Script organization (if not phase1_only)
            if not self.phase1_only:
                self.log("")
                self.phase2_script_cleanup()
                
            self.log("")
            self.log("=" * 60, "SUCCESS")
            self.log("✅ Housekeeping Complete!", "SUCCESS")
            self.log("=" * 60, "SUCCESS")
            self.log("")
            self.log("Summary:", "INFO")
            self.log(f"  ✅ Archive created: {self.arch_base.relative_to(self.root_dir)}", "INFO")
            self.log("  ✅ Scripts backed up", "INFO")
            if not self.phase1_only:
                self.log("  ✅ Scripts organized (with stubs for moved scripts)", "INFO")
            self.log("")
            self.log("Next steps:", "INFO")
            self.log("  1. Review moved files in ARCH_EXECUTION/", "INFO")
            if not self.phase1_only:
                self.log("  2. Verify active scripts still work", "INFO")
                self.log("  3. Test pipeline execution", "INFO")
            else:
                self.log("  2. Run Phase 2 later (after confirming pipeline works)", "INFO")
            self.log("")
            
        except Exception as e:
            self.log(f"Error during housekeeping: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Safe housekeeping for catalog_pipeline_v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run Phase 1 only (preview changes)
  python3 execute_housekeeping.py --phase1-only --dry-run
  
  # Execute Phase 1 only (safe cleanup)
  python3 execute_housekeeping.py --phase1-only
  
  # Execute full housekeeping (Phase 1 + Phase 2)
  python3 execute_housekeeping.py
        """
    )
    parser.add_argument(
        "--phase1-only",
        action="store_true",
        help="Run only Phase 1 (safe cleanup, no script moves)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without making them"
    )
    
    args = parser.parse_args()
    
    # Get script directory
    script_dir = Path(__file__).parent.resolve()
    
    executor = HousekeepingExecutor(
        root_dir=script_dir,
        dry_run=args.dry_run,
        phase1_only=args.phase1_only
    )
    
    executor.run()


if __name__ == "__main__":
    main()

