#!/usr/bin/env python3
"""
KB Refresh Runner - Populates RAG Knowledge Pack from Phase 5 sources

This script implements the KB refresh process as defined in RAG_KB/kb_refresh.md.
It scans Phase 5 folders, selects latest files, and builds the curated knowledge pack.

Usage:
    python3 run_kb_refresh.py [--dry-run] [--verbose]
"""

import json
import os
import re
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
RAG_KB_ROOT = REPO_ROOT / "RAG_KB"
KB_PACK_ROOT = RAG_KB_ROOT / "phase5_pack"
BUILD_REPORTS_ROOT = RAG_KB_ROOT / "build_reports"
CHAT_MIRROR_ROOT = RAG_KB_ROOT / "chat_mirror"

# Scan roots (relative to REPO_ROOT)
SCAN_ROOTS = {
    "phase5_docs": {
        "path": "docs/PHASE_5",
        "namespace": "phase5_docs",
        "recursive": True,
    },
    "catalog_pipeline": {
        "path": "tools/catalog_pipeline_v2",
        "namespace": "catalog_pipeline",
        "recursive": True,
    },
    "master_docs": {
        "path": "docs",
        "namespace": "master_docs",
        "files": ["NSW_ESTIMATION_MASTER.md", "NSW_ESTIMATION_BASELINE.md"],
        "recursive": False,
    },
    "features": {
        "path": "features",
        "namespace": "features",
        "recursive": True,
    },
    "changes": {
        "path": "changes",
        "namespace": "changes",
        "recursive": True,
    },
    "trace": {
        "path": "trace",
        "namespace": "trace",
        "recursive": True,
    },
    "rag_governance": {
        "path": "RAG_KB",
        "namespace": "rag_governance",
        "files": [
            "RAG_RULEBOOK.md",
            "phase5_pack/08_PROMOTION_WORKFLOW.md",
            "phase5_pack/01_CANONICAL_MASTER.md",
            "phase5_pack/02_DECISIONS_LOG.md",
            "phase5_pack/03_FEATURE_FLAGS.md",
        ],
        "recursive": False,
    },
}

# Ignore patterns (files/folders to skip)
IGNORE_PATTERNS = [
    r"_old",
    r"_copy",
    r"_backup",
    r"\.bak$",
    r"^\.git",
    r"^__pycache__",
    r"^\.venv",
    r"^venv",
    r"^node_modules",
    r"\.pyc$",
    r"\.pyo$",
]

# File extensions to process
ALLOWED_EXTENSIONS = {".md", ".py", ".yml", ".yaml", ".json", ".sql", ".txt"}

# Patterns indicating canonical/final status
CANONICAL_PATTERNS = [
    r"CANONICAL",
    r"FINAL",
    r"_v1\.0",
    r"_v\d+\.\d+$",  # versioned files
]

# Patterns indicating draft status (lower priority)
DRAFT_PATTERNS = [
    r"DRAFT",
    r"_draft",
    r"_temp",
    r"TEMP",
]


def parse_front_matter(text: str) -> dict:
    """Parse YAML-like front-matter from text"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def normalize_status(s: str) -> str:
    """Normalize status string to standard values"""
    s = (s or "").strip().upper()
    # Treat LOCKED as CANONICAL
    if s == "LOCKED":
        return "CANONICAL"
    if s in ("CANONICAL", "WORKING", "DRAFT", "DEPRECATED"):
        return s
    return "WORKING"


def status_score(status: str) -> int:
    """Get numeric score for status (higher = more authoritative)"""
    m = {"CANONICAL": 3, "WORKING": 2, "DRAFT": 1, "DEPRECATED": 0}
    return m.get(status, 2)


def parse_version(v: str) -> tuple:
    """Parse version string to tuple (major, minor, patch)"""
    if not v:
        return (0, 0, 0)
    v = v.strip().lower()
    v = re.sub(r"^(v|rev)\s*", "", v)
    nums = re.findall(r"\d+", v)
    parts = [int(n) for n in nums[:3]]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


class KBRefresher:
    """Main refresh orchestrator"""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.index_manifest = {
            "version": "1.0",
            "last_refresh": None,
            "files": [],
            "statistics": {
                "total_files": 0,
                "canonical_count": 0,
                "working_count": 0,
                "draft_count": 0,
            },
        }
        self.folder_map = {}
        self.previous_index = self._load_previous_index()
        self.delta = {
            "new_files": [],
            "updated_files": [],
            "removed_files": [],
            "authority_changes": [],
        }
        # Track files missing headers and broken active file pointers
        self.missing_headers = []
        self.broken_active_files = []

    def _load_previous_index(self) -> Optional[Dict]:
        """Load previous index if it exists"""
        index_path = KB_PACK_ROOT / "00_INDEX.json"
        if index_path.exists():
            try:
                with open(index_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Could not load previous index: {e}")
        return None

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file content for change detection (streaming)."""
        try:
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):  # 1MB chunks
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not compute hash for {file_path}: {e}")
            return ""

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        path_str = str(path)
        for pattern in IGNORE_PATTERNS:
            if re.search(pattern, path_str, re.IGNORECASE):
                return True
        return False

    def _is_allowed_extension(self, path: Path) -> bool:
        """Check if file extension is allowed"""
        return path.suffix.lower() in ALLOWED_EXTENSIONS

    def _get_authority_status(self, filename: str, content: Optional[str] = None) -> str:
        """Determine authority status from filename and optionally content"""
        # Check content for metadata first (front-matter has highest priority)
        if content:
            front_matter = parse_front_matter(content)
            if "Status" in front_matter:
                return normalize_status(front_matter["Status"])
        
        # Check filename patterns
        for pattern in CANONICAL_PATTERNS:
            if re.search(pattern, filename, re.IGNORECASE):
                return "CANONICAL"

        for pattern in DRAFT_PATTERNS:
            if re.search(pattern, filename, re.IGNORECASE):
                return "DRAFT"

        # Default to WORKING
        return "WORKING"

    def _select_latest_file(self, folder: Path, namespace: str) -> Optional[Tuple[Path, Dict]]:
        """
        Select active file from a folder using: _ACTIVE_FILE.txt override OR Authority → Version → Timestamp ranking
        """
        if not folder.exists() or not folder.is_dir():
            return None

        # Check for _ACTIVE_FILE.txt override
        active_file_marker = folder / "_ACTIVE_FILE.txt"
        if active_file_marker.exists():
            try:
                with open(active_file_marker, "r", encoding="utf-8") as f:
                    active_filename = f.read().strip()
                active_file_path = folder / active_filename
                if active_file_path.exists() and active_file_path.is_file():
                    if not self._should_ignore(active_file_path) and self._is_allowed_extension(active_file_path):
                        stat = active_file_path.stat()
                        try:
                            with open(active_file_path, "r", encoding="utf-8", errors="ignore") as f:
                                content_preview = f.read(2000)
                        except:
                            content_preview = None
                        authority = self._get_authority_status(active_file_path.name, content_preview)
                        front_matter = parse_front_matter(content_preview) if content_preview else {}
                        
                        return (
                            active_file_path,
                            {
                                "authority": authority,
                                "mtime": stat.st_mtime,
                                "size": stat.st_size,
                                "selected_by": "ACTIVE_FILE",
                                "header_status": front_matter.get("Status"),
                                "header_version": front_matter.get("Version"),
                            },
                        )
                else:
                    # Broken active file pointer
                    self.broken_active_files.append({
                        "folder": str(folder.relative_to(REPO_ROOT)),
                        "referenced_file": active_filename,
                    })
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Could not read _ACTIVE_FILE.txt in {folder}: {e}")

        # No override or override failed - use ranking
        candidates = []
        for file_path in folder.iterdir():
            if not file_path.is_file():
                continue
            if file_path.name == "_ACTIVE_FILE.txt":
                continue  # Skip the marker file itself
            if self._should_ignore(file_path):
                continue
            if not self._is_allowed_extension(file_path):
                continue

            # Check if it's a large binary file (XLSX, PDF)
            if file_path.suffix.lower() in {".xlsx", ".pdf", ".xls"}:
                continue

            try:
                stat = file_path.stat()
                # Read content to check front-matter
                content_preview = None
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content_preview = f.read(2000)  # First 2KB
                except:
                    pass

                # Get authority (from front-matter if present, else filename heuristics)
                authority = self._get_authority_status(file_path.name, content_preview)
                
                # Parse front-matter
                front_matter = parse_front_matter(content_preview) if content_preview else {}
                header_status = front_matter.get("Status")
                header_version = front_matter.get("Version")
                
                # Track files missing headers (in Phase-5 folders)
                if namespace == "phase5_docs" and not header_status and not header_version:
                    self.missing_headers.append(str(file_path.relative_to(REPO_ROOT)))

                # Use header status if present, otherwise use inferred authority
                final_status = normalize_status(header_status) if header_status else authority
                version_tuple = parse_version(header_version) if header_version else (0, 0, 0)

                candidates.append({
                    "path": file_path,
                    "mtime": stat.st_mtime,
                    "authority": final_status,
                    "size": stat.st_size,
                    "version": version_tuple,
                    "header_status": header_status,
                    "header_version": header_version,
                })
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Could not process {file_path}: {e}")
                continue

        if not candidates:
            return None

        # Sort by: status_score (desc), version (desc), mtime (desc)
        def sort_key(c):
            # For tuple version, we need to negate each element for descending order
            version_tuple = c["version"]
            negated_version = tuple(-x for x in version_tuple) if version_tuple else (0, 0, 0)
            return (
                -status_score(c["authority"]),  # Negative for descending
                negated_version,  # Negated tuple for descending version order
                -c["mtime"],  # Negative for descending (newest first)
            )

        candidates.sort(key=sort_key)
        best = candidates[0]

        return (
            best["path"],
            {
                "authority": best["authority"],
                "mtime": best["mtime"],
                "size": best["size"],
                "selected_by": "RANKING",
                "header_status": best["header_status"],
                "header_version": best["header_version"],
            },
        )

    def _scan_folder(self, root_path: Path, namespace: str, recursive: bool = True) -> List[Dict]:
        """Scan a folder and collect latest files"""
        files_found = []

        if not root_path.exists():
            if self.verbose:
                print(f"Warning: Path does not exist: {root_path}")
            return files_found

        # If recursive, process subdirectories
        if recursive:
            for item in root_path.rglob("*"):
                if item.is_dir():
                    continue
                if self._should_ignore(item):
                    continue

                # For files, check parent folder
                parent = item.parent
                folder_key = str(parent.relative_to(REPO_ROOT))

                # Select latest file per folder
                if folder_key not in self.folder_map:
                    selected = self._select_latest_file(parent, namespace)
                    if selected:
                        file_path, metadata = selected
                        self.folder_map[folder_key] = {
                            "selected": file_path,
                            "namespace": namespace,
                            "metadata": metadata,  # Include selection metadata
                        }
        else:
            # Non-recursive: process specific files or root folder
            if root_path.is_file():
                if not self._should_ignore(root_path) and self._is_allowed_extension(root_path):
                    files_found.append({
                        "path": root_path,
                        "namespace": namespace,
                        "folder": str(root_path.parent.relative_to(REPO_ROOT)),
                        "selected_by": "DIRECT",  # Direct file, no selection needed
                        "header_status": None,
                        "header_version": None,
                    })
            elif root_path.is_dir():
                selected = self._select_latest_file(root_path, namespace)
                if selected:
                    file_path, metadata = selected
                    files_found.append({
                        "path": file_path,
                        "namespace": namespace,
                        "folder": str(root_path.relative_to(REPO_ROOT)),
                        "selected_by": metadata.get("selected_by", "RANKING"),
                        "header_status": metadata.get("header_status"),
                        "header_version": metadata.get("header_version"),
                    })

        return files_found

    def _determine_kb_path(self, file_path: Path, namespace: str, authority: str) -> Path:
        """Determine where file should be placed in KB pack"""
        relative_path = file_path.relative_to(REPO_ROOT)
        filename = file_path.name

        # Map namespaces to KB pack locations
        if namespace == "phase5_docs":
            if "00_GOVERNANCE" in str(relative_path):
                return KB_PACK_ROOT / "04_RULES_LIBRARY" / "governance" / filename
            elif "CANONICAL" in str(relative_path) or "04_SCHEMA_CANON" in str(relative_path):
                return KB_PACK_ROOT / "05_IMPLEMENTATION_NOTES" / "schema" / filename
            elif "03_DATA_DICTIONARY" in str(relative_path):
                return KB_PACK_ROOT / "04_RULES_LIBRARY" / "data_dictionary" / filename
            elif "06_IMPLEMENTATION_REFERENCE" in str(relative_path):
                return KB_PACK_ROOT / "05_IMPLEMENTATION_NOTES" / "reference" / filename
            else:
                return KB_PACK_ROOT / "04_RULES_LIBRARY" / "misc" / filename
        elif namespace == "catalog_pipeline":
            if file_path.suffix == ".py":
                return KB_PACK_ROOT / "05_IMPLEMENTATION_NOTES" / "scripts" / filename
            else:
                return KB_PACK_ROOT / "04_RULES_LIBRARY" / "catalog" / filename
        elif namespace == "implementation_artifacts":
            return KB_PACK_ROOT / "05_IMPLEMENTATION_NOTES" / filename
        elif namespace == "rag_governance":
            # Route governance files to appropriate locations
            if filename == "RAG_RULEBOOK.md":
                return KB_PACK_ROOT / "04_RULES_LIBRARY" / "governance" / filename
            elif filename in ("08_PROMOTION_WORKFLOW.md", "01_CANONICAL_MASTER.md", "02_DECISIONS_LOG.md", "03_FEATURE_FLAGS.md"):
                # These are already in phase5_pack, so keep them there
                return KB_PACK_ROOT / filename
            else:
                return KB_PACK_ROOT / "04_RULES_LIBRARY" / "governance" / filename
        else:
            return KB_PACK_ROOT / "04_RULES_LIBRARY" / namespace / filename

    def _copy_file_to_kb(self, source: Path, dest: Path, metadata: Dict) -> Dict:
        """Copy file to KB pack with metadata header"""
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Read source content
        try:
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {source}: {e}")
            return None

        # Check if metadata header exists
        metadata_header = f"""---
Source: {source.relative_to(REPO_ROOT)}
KB_Namespace: {metadata['namespace']}
Status: {metadata['authority']}
Last_Updated: {datetime.fromtimestamp(metadata['mtime']).isoformat()}
KB_Path: {dest.relative_to(RAG_KB_ROOT)}
---

"""
        # Add metadata header if not present
        if not content.startswith("---"):
            content = metadata_header + content
        else:
            # Update existing metadata
            content = re.sub(
                r"^---\s*\n(.*?)\n---\s*\n",
                metadata_header.strip() + "\n",
                content,
                flags=re.MULTILINE | re.DOTALL,
                count=1,
            )

        if not self.dry_run:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)

        return {
            "source": str(source.relative_to(REPO_ROOT)),
            "dest": str(dest.relative_to(RAG_KB_ROOT)),
            "size": len(content),
        }

    def scan_and_collect(self):
        """Scan all configured roots and collect files"""
        print("Scanning repository folders...")

        all_files = []

        for scan_name, config in SCAN_ROOTS.items():
            root_path = REPO_ROOT / config["path"]
            namespace = config["namespace"]
            recursive = config.get("recursive", True)

            if self.verbose:
                print(f"Scanning {scan_name}: {root_path}")

            if "files" in config:
                # Specific files mode
                for filename in config["files"]:
                    file_path = root_path / filename
                    if file_path.exists():
                        all_files.append({
                            "path": file_path,
                            "namespace": namespace,
                            "folder": str(root_path.relative_to(REPO_ROOT)),
                            "selected_by": "DIRECT",  # Specific file, not selected
                            "header_status": None,
                            "header_version": None,
                        })
            else:
                # Folder scan mode
                files = self._scan_folder(root_path, namespace, recursive)
                all_files.extend(files)

        # Process folder_map to get unique latest files
        unique_files = {}
        for folder_key, info in self.folder_map.items():
            file_path = info["selected"]
            namespace = info["namespace"]
            key = str(file_path.relative_to(REPO_ROOT))
            if key not in unique_files:
                metadata = info.get("metadata", {})
                unique_files[key] = {
                    "path": file_path,
                    "namespace": namespace,
                    "folder": folder_key,
                    "selected_by": metadata.get("selected_by", "RANKING"),
                    "header_status": metadata.get("header_status"),
                    "header_version": metadata.get("header_version"),
                }

        # Add direct file matches
        for file_info in all_files:
            key = str(file_info["path"].relative_to(REPO_ROOT))
            if key not in unique_files:
                unique_files[key] = file_info

        print(f"Found {len(unique_files)} unique files to process")
        return list(unique_files.values())

    def build_kb_pack(self, files: List[Dict]):
        """Build the knowledge pack from collected files"""
        print("Building knowledge pack...")

        for file_info in files:
            file_path = file_info["path"]
            namespace = file_info["namespace"]

            # Get file metadata
            stat = file_path.stat()
            
            # Compute SHA256 hash for change detection
            content_hash = self._compute_file_hash(file_path)
            
            # Read content to check front-matter
            content_preview = None
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content_preview = f.read(2000)
            except:
                pass
            
            authority = self._get_authority_status(file_path.name, content_preview)

            # Determine KB destination
            kb_path = self._determine_kb_path(file_path, namespace, authority)
            kb_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            copy_result = self._copy_file_to_kb(
                file_path,
                kb_path,
                {
                    "namespace": namespace,
                    "authority": authority,
                    "mtime": stat.st_mtime,
                },
            )

            if copy_result:
                # Get selection metadata if available (from file_info or metadata)
                selected_by = file_info.get("selected_by", "RANKING")
                header_status = file_info.get("header_status")
                header_version = file_info.get("header_version")
                
                # Add to index
                self.index_manifest["files"].append({
                    "namespace": namespace,
                    "folder": file_info["folder"],
                    "filename": file_path.name,
                    "status": authority,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "authority": authority,
                    "kb_path": str(kb_path.relative_to(RAG_KB_ROOT)),
                    "source_path": str(file_path.relative_to(REPO_ROOT)),
                    "selected_by": selected_by,
                    "header_status": header_status,
                    "header_version": header_version,
                    "content_hash": content_hash,  # SHA256 hash for change detection
                })

                # Update statistics
                self.index_manifest["statistics"]["total_files"] += 1
                if authority == "CANONICAL":
                    self.index_manifest["statistics"]["canonical_count"] += 1
                elif authority == "WORKING":
                    self.index_manifest["statistics"]["working_count"] += 1
                elif authority == "DRAFT":
                    self.index_manifest["statistics"]["draft_count"] += 1

    def build_folder_map(self):
        """Build human-readable folder map"""
        print("Building folder map...")

        folder_map_content = """# Phase 5 Folder Structure Map

**Version:** 1.0  
**Last Updated:** {timestamp}  
**Generated By:** KB Refresh Process

---

## Purpose

This document provides a human-readable map of the Phase 5 folder structure, showing which files exist and which is the latest/authoritative file per folder.

---

## Repository Structure

""".format(timestamp=datetime.now(timezone.utc).isoformat())

        # Group by namespace
        by_namespace = {}
        for file_entry in self.index_manifest["files"]:
            ns = file_entry["namespace"]
            if ns not in by_namespace:
                by_namespace[ns] = []
            by_namespace[ns].append(file_entry)

        for namespace, files in sorted(by_namespace.items()):
            folder_map_content += f"### {namespace}\n\n"
            by_folder = {}
            for file_entry in files:
                folder = file_entry["folder"]
                if folder not in by_folder:
                    by_folder[folder] = []
                by_folder[folder].append(file_entry)

            for folder, folder_files in sorted(by_folder.items()):
                folder_map_content += f"#### {folder}\n"
                
                # Find the selected file for this folder (if we have it in folder_map)
                selected_file = None
                for file_entry in folder_files:
                    # Check if this file was selected (by matching folder path)
                    folder_key = file_entry.get("folder", "")
                    if folder_key in self.folder_map:
                        selected_path = self.folder_map[folder_key]["selected"]
                        if str(selected_path.relative_to(REPO_ROOT)) == file_entry.get("source_path", ""):
                            selected_file = file_entry
                            break
                
                if selected_file:
                    selected_by = selected_file.get("selected_by", "RANKING")
                    header_status = selected_file.get("header_status")
                    header_version = selected_file.get("header_version")
                    authority = selected_file.get("authority", "WORKING")
                    authority_badge = f"[{authority}]" if authority != "WORKING" else ""
                    status_info = f"Status: {header_status}" if header_status else f"Inferred: {authority}"
                    version_info = f", Version: {header_version}" if header_version else ""
                    folder_map_content += f"- **Active File:** {selected_file['filename']} {authority_badge}\n"
                    folder_map_content += f"  - Selected by: {selected_by}\n"
                    folder_map_content += f"  - {status_info}{version_info}\n"
                    folder_map_content += f"  - Last Modified: {selected_file['last_modified'][:10]}\n"
                else:
                    folder_map_content += f"- **Files:**\n"
                    for file_entry in sorted(folder_files, key=lambda x: x["last_modified"], reverse=True):
                        authority_badge = f"[{file_entry['authority']}]" if file_entry['authority'] != "WORKING" else ""
                        folder_map_content += f"  - {file_entry['filename']} {authority_badge} ({file_entry['last_modified'][:10]})\n"
                folder_map_content += "\n"

        folder_map_path = KB_PACK_ROOT / "00_FOLDER_MAP.md"
        if not self.dry_run:
            with open(folder_map_path, "w", encoding="utf-8") as f:
                f.write(folder_map_content)

    def build_delta_report(self):
        """Build delta report comparing with previous index"""
        print("Building delta report...")

        if not self.previous_index:
            delta_content = """# Delta Report - KB Refresh

**Refresh Date:** {timestamp}  
**Previous Refresh:** None (First refresh)

---

## New Files Added

{new_files_count} files added (first refresh)

""".format(
                timestamp=datetime.now().isoformat(),
                new_files_count=len(self.index_manifest["files"]),
            )
        else:
            # Compare with previous
            prev_files = {f["kb_path"]: f for f in self.previous_index.get("files", [])}
            curr_files = {f["kb_path"]: f for f in self.index_manifest["files"]}

            new_files = [f for k, f in curr_files.items() if k not in prev_files]
            removed_files = [f for k, f in prev_files.items() if k not in curr_files]
            updated_files = []

            for k in set(prev_files.keys()) & set(curr_files.keys()):
                prev = prev_files[k]
                curr = curr_files[k]
                # Use SHA256 hash for more reliable change detection (strict policy)
                prev_hash = prev.get("content_hash", "")
                curr_hash = curr.get("content_hash", "")
                if not prev_hash or not curr_hash:
                    # If hashing missing, treat as updated to avoid false negatives (conservative)
                    updated_files.append({"filename": curr["filename"], "previous": prev, "current": curr})
                elif prev_hash != curr_hash:
                    updated_files.append({"filename": curr["filename"], "previous": prev, "current": curr})

            delta_content = f"""# Delta Report - KB Refresh

**Refresh Date:** {datetime.now(timezone.utc).isoformat()}  
**Previous Refresh:** {self.previous_index.get('last_refresh', 'Unknown')}

---

## New Files Added

{len(new_files)} files added:
{chr(10).join(f"- {f['filename']} ({f['folder']})" for f in new_files[:20])}
{f"({len(new_files) - 20} more files...)" if len(new_files) > 20 else ""}

## Files Updated

{len(updated_files)} files updated:
{chr(10).join(f"- {f['filename']}" for f in updated_files[:20])}
{f"({len(updated_files) - 20} more files...)" if len(updated_files) > 20 else ""}

## Files Removed/Deprecated

{len(removed_files)} files removed:
{chr(10).join(f"- {f['filename']}" for f in removed_files[:10])}
{f"({len(removed_files) - 10} more files...)" if len(removed_files) > 10 else ""}

"""

        delta_path = BUILD_REPORTS_ROOT / "DELTA_SINCE_LAST.md"
        if not self.dry_run:
            delta_path.parent.mkdir(parents=True, exist_ok=True)
            with open(delta_path, "w", encoding="utf-8") as f:
                f.write(delta_content)

    def save_index(self):
        """Save the index manifest"""
        self.index_manifest["last_refresh"] = datetime.now(timezone.utc).isoformat()
        index_path = KB_PACK_ROOT / "00_INDEX.json"
        if not self.dry_run:
            with open(index_path, "w", encoding="utf-8") as f:
                json.dump(self.index_manifest, f, indent=2, ensure_ascii=False)
        print(f"Index saved: {len(self.index_manifest['files'])} files")

    def generate_master_md(self) -> str:
        """Generate 01_CANONICAL_MASTER.md content"""
        stats = self.index_manifest["statistics"]
        files = self.index_manifest["files"]
        
        # Count by namespace
        by_ns: Dict[str, int] = {}
        for f in files:
            ns = f.get("namespace", "")
            by_ns[ns] = by_ns.get(ns, 0) + 1
        
        # Filter by authority
        canonical = [f for f in files if f.get("authority") == "CANONICAL"]
        working = [f for f in files if f.get("authority") == "WORKING"]
        draft = [f for f in files if f.get("authority") == "DRAFT"]
        
        lines = []
        lines.append("# Phase 5 Master Consolidation")
        lines.append("")
        lines.append(f"**KB Version:** {self.index_manifest.get('version', '1.0')}")
        lines.append(f"**Last Refresh (UTC):** {self.index_manifest.get('last_refresh', '')}")
        lines.append("**Generated By:** tools/kb_refresh/run_kb_refresh.py")
        lines.append("")
        lines.append("## Metadata")
        lines.append(f"- Total files (latest-only): {stats['total_files']}")
        lines.append(f"- CANONICAL: {stats['canonical_count']} | WORKING: {stats['working_count']} | DRAFT: {stats['draft_count']}")
        lines.append("- Namespaces:")
        for ns in sorted(by_ns.keys()):
            lines.append(f"  - {ns}: {by_ns[ns]}")
        lines.append("")
        lines.append("## Canonical Evidence (Locked Sources)")
        if canonical:
            for f in sorted(canonical, key=lambda x: x.get("source_path", "")):
                source_path = f.get("source_path", "")
                last_modified = f.get("last_modified", "")
                lines.append(f"- `{source_path}` (LastModifiedUTC: {last_modified})")
        else:
            lines.append("- OPEN: No canonical files detected by heuristics.")
        lines.append("")
        lines.append("## Working Evidence (Latest-only)")
        # Keep this bounded to avoid huge output
        top_working = sorted(working, key=lambda x: x.get("source_path", ""))[:50]
        for f in top_working:
            source_path = f.get("source_path", "")
            last_modified = f.get("last_modified", "")
            lines.append(f"- `{source_path}` (LastModifiedUTC: {last_modified})")
        if len(working) > 50:
            lines.append(f"- ... ({len(working) - 50} more WORKING files; see 00_INDEX.json)")
        lines.append("")
        if draft:
            lines.append("## Draft Evidence")
            for f in sorted(draft, key=lambda x: x.get("source_path", "")):
                source_path = f.get("source_path", "")
                lines.append(f"- `{source_path}`")
            lines.append("")
        lines.append("## OPEN Sections (to be promoted later)")
        lines.append("- Canonical Definitions (Locked): OPEN (promote from governance docs)")
        lines.append("- Entry Gates / Scope: OPEN (promote from Phase-5 governance)")
        lines.append("- Feature Flags: OPEN (populate from Phase-5 sources)")
        lines.append("- Decisions Log: OPEN (extract LOCKED decisions)")
        lines.append("")
        lines.append("## References")
        lines.append(f"- Folder map: `phase5_pack/00_FOLDER_MAP.md`")
        lines.append(f"- Index manifest: `phase5_pack/00_INDEX.json`")
        lines.append("")
        return "\n".join(lines) + "\n"

    def generate_risks_md(self) -> str:
        """Generate RISKS_AND_GAPS.md content"""
        stats = self.index_manifest["statistics"]
        files = self.index_manifest["files"]
        
        canonical_count = stats["canonical_count"]
        total = stats["total_files"]
        
        # Count by namespace
        ns_counts: Dict[str, int] = {}
        for f in files:
            ns = f.get("namespace", "")
            ns_counts[ns] = ns_counts.get(ns, 0) + 1
        
        lines = []
        lines.append("# Risks and Gaps Report")
        lines.append("")
        lines.append(f"**Generated (UTC):** {datetime.now(timezone.utc).isoformat()}")
        lines.append(f"**KB Version:** {self.index_manifest.get('version', '1.0')}")
        lines.append("")
        lines.append("## Blocking Issues")
        if total == 0:
            lines.append("- No files indexed. Check SCAN_ROOTS and repo paths.")
        else:
            lines.append("- None detected (baseline heuristics).")
        lines.append("")
        lines.append("## High Priority Gaps")
        if canonical_count == 0:
            lines.append("- No CANONICAL files detected. Add CANONICAL/FINAL/LOCKED markers to authoritative Phase-5 docs.")
        elif canonical_count < 10:
            lines.append(f"- Low canonical coverage: {canonical_count}/{total}. Consider promoting key governance docs to CANONICAL.")
        lines.append("")
        
        # Missing Front-Matter Headers
        if self.missing_headers:
            lines.append("## Missing Front-Matter Headers")
            lines.append(f"{len(self.missing_headers)} Phase-5 files are missing front-matter headers (Status/Version):")
            for path in sorted(self.missing_headers)[:20]:  # Limit to first 20
                lines.append(f"- `{path}`")
            if len(self.missing_headers) > 20:
                lines.append(f"- ... ({len(self.missing_headers) - 20} more files)")
            lines.append("")
            lines.append("**Recommendation:** Add front-matter headers with Status and Version to ensure proper ranking.")
            lines.append("")
        else:
            lines.append("## Missing Front-Matter Headers")
            lines.append("- None detected (all Phase-5 files have headers).")
            lines.append("")
        
        # Broken _ACTIVE_FILE.txt
        if self.broken_active_files:
            lines.append("## Broken _ACTIVE_FILE.txt References")
            lines.append(f"{len(self.broken_active_files)} _ACTIVE_FILE.txt marker(s) reference missing files:")
            for item in self.broken_active_files:
                lines.append(f"- `{item['folder']}/_ACTIVE_FILE.txt` → `{item['referenced_file']}` (file not found)")
            lines.append("")
            lines.append("**Recommendation:** Fix or remove broken _ACTIVE_FILE.txt markers.")
            lines.append("")
        else:
            lines.append("## Broken _ACTIVE_FILE.txt References")
            lines.append("- None detected (all _ACTIVE_FILE.txt markers are valid).")
            lines.append("")
        
        lines.append("## Coverage Notes")
        for ns in sorted(ns_counts.keys()):
            lines.append(f"- Namespace `{ns}`: {ns_counts[ns]} files")
        lines.append("")
        lines.append("## Input/Binary Handling")
        lines.append("- PDFs/XLSX are summarized only (no binary ingestion). Add manual summaries for critical inputs if needed.")
        lines.append("")
        lines.append("## Next Actions")
        lines.append("- Promote true LOCKED decisions into `phase5_pack/02_DECISIONS_LOG.md`.")
        lines.append("- Populate `03_FEATURE_FLAGS.md` from Phase-5 sources.")
        lines.append("- After master + risks are stable, proceed to indexer/query upgrade.")
        lines.append("")
        return "\n".join(lines) + "\n"

    def run(self):
        """Execute the full refresh process"""
        print("=" * 60)
        print("KB Refresh Process")
        print("=" * 60)
        if self.dry_run:
            print("DRY RUN MODE - No files will be modified")
        print()

        # Step 1: Scan and collect
        files = self.scan_and_collect()

        # Step 2: Build KB pack
        self.build_kb_pack(files)

        # Step 3: Build folder map
        self.build_folder_map()

        # Step 4: Build delta report
        self.build_delta_report()

        # Step 5: Save index
        self.save_index()

        # Step 6: Generate master and risks files
        self.build_master_and_risks()

        # Step 7: Run extractors (decisions and feature flags)
        self.run_extractors()

        print()
        print("=" * 60)
        print("Refresh Complete!")
        print("=" * 60)
        print(f"Files processed: {self.index_manifest['statistics']['total_files']}")
        print(f"  - CANONICAL: {self.index_manifest['statistics']['canonical_count']}")
        print(f"  - WORKING: {self.index_manifest['statistics']['working_count']}")
        print(f"  - DRAFT: {self.index_manifest['statistics']['draft_count']}")

    def run_extractors(self):
        """Run decision and feature flag extractors"""
        print()
        print("=" * 60)
        print("Running Extractors")
        print("=" * 60)
        
        # Import extractors
        import subprocess
        import sys
        
        extractors = [
            ("extract_decisions.py", "Decision extraction"),
            ("extract_feature_flags.py", "Feature flag extraction"),
            ("extract_telemetry_summary.py", "Telemetry summary extraction"),
            ("extract_feedback_summary.py", "Feedback summary extraction"),
            ("extract_kb_improvement_backlog.py", "KB improvement backlog"),
        ]
        
        for script_name, description in extractors:
            print(f"\n{description}...")
            script_path = Path(__file__).parent / script_name
            if script_path.exists():
                try:
                    cmd = [sys.executable, str(script_path)]
                    if self.dry_run:
                        cmd.append("--dry-run")
                    if self.verbose:
                        cmd.append("--verbose")
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
                    if result.returncode == 0:
                        print(result.stdout)
                    else:
                        print(f"Warning: {script_name} failed:")
                        print(result.stderr)
                except Exception as e:
                    print(f"Warning: Could not run {script_name}: {e}")
            else:
                print(f"Warning: {script_name} not found, skipping")

    def build_master_and_risks(self):
        """Generate 01_CANONICAL_MASTER.md and RISKS_AND_GAPS.md"""
        print("Generating master and risks files...")
        
        master_content = self.generate_master_md()
        risks_content = self.generate_risks_md()
        
        if not self.dry_run:
            master_path = KB_PACK_ROOT / "01_CANONICAL_MASTER.md"
            risks_path = BUILD_REPORTS_ROOT / "RISKS_AND_GAPS.md"
            
            with open(master_path, "w", encoding="utf-8") as f:
                f.write(master_content)
            
            risks_path.parent.mkdir(parents=True, exist_ok=True)
            with open(risks_path, "w", encoding="utf-8") as f:
                f.write(risks_content)
            
            print(f"  Generated: {master_path.relative_to(REPO_ROOT)}")
            print(f"  Generated: {risks_path.relative_to(REPO_ROOT)}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Refresh RAG Knowledge Pack")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (no files modified)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    refresher = KBRefresher(dry_run=args.dry_run, verbose=args.verbose)
    refresher.run()


if __name__ == "__main__":
    main()

