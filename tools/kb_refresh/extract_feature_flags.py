#!/usr/bin/env python3
"""
Feature Flags Extractor - Scans Phase 5 docs and features for feature flags

Extracts feature flag candidates and populates 03_FEATURE_FLAGS.md registry.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
RAG_KB_ROOT = REPO_ROOT / "RAG_KB"
KB_PACK_ROOT = RAG_KB_ROOT / "phase5_pack"

# Scan paths
PHASE5_ROOT = REPO_ROOT / "docs" / "PHASE_5"
FEATURES_ROOT = REPO_ROOT / "features"
CHAT_MIRROR_ROOT = RAG_KB_ROOT / "chat_mirror"


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
    """Normalize status string"""
    s = (s or "").strip().upper()
    if s == "LOCKED":
        return "CANONICAL"
    if s in ("CANONICAL", "WORKING", "DRAFT", "DEPRECATED"):
        return s
    return "WORKING"


def get_file_status(file_path: Path) -> str:
    """Get status from file front-matter or infer from filename"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(2000)
        front_matter = parse_front_matter(content)
        if "Status" in front_matter:
            return normalize_status(front_matter["Status"])
        filename = file_path.name.upper()
        if "CANONICAL" in filename or "LOCKED" in filename or "FINAL" in filename:
            return "CANONICAL"
    except:
        pass
    return "WORKING"


def extract_feature_flags_from_content(content: str, source_path: str, source_status: str) -> List[Dict]:
    """Extract feature flag candidates from content"""
    flags = []
    
    # Pattern 1: Explicit flag declarations
    # "Feature Flag: NAME" or "FEATURE_FLAG: NAME" or "Flag: NAME" or "FF_: NAME"
    flag_decl_patterns = [
        r"(?:Feature\s+Flag|FEATURE_FLAG|Flag|FF_)\s*[:\-]\s*([A-Za-z0-9_]+)",
        r"feature[_\s]+flag[_\s]+([A-Za-z0-9_]+)",
        r"FEATURE_FLAG_([A-Za-z0-9_]+)",
        r"FF_([A-Za-z0-9_]+)",
    ]
    
    flag_names = set()
    for pattern in flag_decl_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
            flag_name = match.group(1).strip()
            if flag_name:
                flag_names.add(flag_name)
    
    # Pattern 2: Toggle/enabled/disabled mentions (context-dependent)
    toggle_patterns = [
        r"toggle[_\s]+([A-Za-z0-9_]+)",
        r"([A-Za-z0-9_]+)[_\s]+(?:enabled|disabled)",
        r"(?:enable|disable)[_\s]+([A-Za-z0-9_]+)",
    ]
    
    for pattern in toggle_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
            flag_name = match.group(1).strip()
            if flag_name and len(flag_name) > 2:  # Filter very short matches
                flag_names.add(flag_name)
    
    # For each flag name, try to extract more context
    for flag_name in flag_names:
        # Try to find default value
        default = "OPEN"
        default_match = re.search(
            rf"{re.escape(flag_name)}[^\n]*?(?:default|defaults?|initial)[\s:=]+(enabled|disabled|true|false|on|off|yes|no)",
            content,
            re.IGNORECASE
        )
        if default_match:
            default_val = default_match.group(1).lower()
            if default_val in ("enabled", "true", "on", "yes"):
                default = "enabled"
            elif default_val in ("disabled", "false", "off", "no"):
                default = "disabled"
        
        # Try to find scope/module
        scope = "OPEN"
        # Extract heading context (previous heading might indicate module/scope)
        flag_pos = content.lower().find(flag_name.lower())
        if flag_pos > 0:
            # Look backwards for heading
            before_text = content[:flag_pos]
            heading_match = re.search(r"^#+\s+(.+)$", before_text, re.MULTILINE)
            if heading_match:
                scope = heading_match.group(1).strip()[:50]  # Limit length
        
        # If source path contains module info, use that
        if "features/" in source_path:
            parts = source_path.split("features/")
            if len(parts) > 1:
                module_part = parts[1].split("/")[0]
                if module_part and scope == "OPEN":
                    scope = f"features/{module_part}"
        
        flags.append({
            "name": flag_name,
            "default": default,
            "scope": scope,
            "source_path": source_path,
            "authority": source_status,
            "source_heading": scope,  # Use scope as heading context for now
        })
    
    return flags


def scan_for_feature_flags(root: Path, recursive: bool = True, limit_status: Optional[str] = None) -> List[Dict]:
    """Scan directory for feature flag candidates"""
    all_flags = []
    
    if not root.exists():
        return all_flags
    
    pattern = root.rglob if recursive else root.glob
    for file_path in pattern("*.md"):
        try:
            source_status = get_file_status(file_path)
            
            # If limit_status is set, only scan files with that status
            if limit_status and source_status != limit_status:
                continue
            
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            source_path = str(file_path.relative_to(REPO_ROOT))
            
            flags = extract_feature_flags_from_content(content, source_path, source_status)
            all_flags.extend(flags)
        except Exception as e:
            continue  # Silently skip errors
    
    return all_flags


def deduplicate_flags(flags: List[Dict]) -> List[Dict]:
    """Deduplicate flags by name, keeping the one with highest authority"""
    flag_map = {}
    
    # Authority priority: CANONICAL > WORKING > DRAFT
    authority_priority = {"CANONICAL": 3, "WORKING": 2, "DRAFT": 1, "DEPRECATED": 0}
    
    for flag in flags:
        name = flag["name"]
        if name not in flag_map:
            flag_map[name] = flag
        else:
            existing = flag_map[name]
            existing_priority = authority_priority.get(existing["authority"], 0)
            new_priority = authority_priority.get(flag["authority"], 0)
            
            if new_priority > existing_priority:
                flag_map[name] = flag
            elif new_priority == existing_priority:
                # Prefer the one with more context (non-OPEN default/scope)
                if flag["default"] != "OPEN" and existing["default"] == "OPEN":
                    flag_map[name] = flag
                elif flag["scope"] != "OPEN" and existing["scope"] == "OPEN":
                    flag_map[name] = flag
    
    return list(flag_map.values())


def generate_feature_flags_registry(flags: List[Dict], dry_run: bool = False):
    """Generate 03_FEATURE_FLAGS.md registry"""
    flags_path = KB_PACK_ROOT / "03_FEATURE_FLAGS.md"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Sort flags by name
    sorted_flags = sorted(flags, key=lambda x: x["name"].lower())
    
    content = f"""# Feature Flags Registry

**Version:** 1.0  
**Last Updated:** {today}  
**Status:** AUTO-GENERATED (Run kb_refresh to update)
**Generated By:** tools/kb_refresh/extract_feature_flags.py

---

## Purpose

This registry documents all feature flags, their defaults, scopes, and phase mappings extracted from Phase 5 documentation.

---

## Extraction Sources

- Phase-5 governance docs
- Features directory
- Execution plans
- Implementation roadmaps
- Mode policies
- Chat mirror (WORKING status only)

---

## Feature Flags

"""
    
    if not sorted_flags:
        content += "_No feature flags found in scanned sources. This registry will be populated as flags are discovered._\n\n"
    else:
        content += f"**Total Flags:** {len(sorted_flags)}\n\n"
        content += "---\n\n"
        
        for flag in sorted_flags:
            content += f"### Flag: {flag['name']}\n\n"
            content += f"- **Default**: {flag['default']}\n"
            content += f"- **Scope**: {flag['scope']}\n"
            content += f"- **Source**: `{flag['source_path']}`\n"
            content += f"- **Authority**: {flag['authority']}\n"
            content += f"- **Description**: _Extracted from {flag['source_path']}_\n"
            content += "\n---\n\n"
    
    content += """
## Format Notes

Each feature flag entry includes:
- **Flag name**: Unique identifier
- **Default**: enabled | disabled | OPEN (unknown)
- **Scope**: Module/component/phase where flag applies (or OPEN if unknown)
- **Source**: Document path where flag was found
- **Authority**: CANONICAL | WORKING | DRAFT (from source document status)
- **Description**: Brief context (may need manual enhancement)

---

## Next Steps

- Review extracted flags for accuracy
- Add descriptions for flags marked "OPEN"
- Promote flags to CANONICAL sources when finalized
- Update this registry after each kb_refresh run

"""
    
    if not dry_run:
        flags_path.parent.mkdir(parents=True, exist_ok=True)
        with open(flags_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {flags_path}: {len(sorted_flags)} flag(s)")
    else:
        print(f"DRY RUN: Would generate feature flags registry with {len(sorted_flags)} flag(s)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract feature flags from Phase 5 docs")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    print("Scanning for feature flags...")
    
    # Scan Phase 5 docs (all statuses)
    phase5_flags = scan_for_feature_flags(PHASE5_ROOT, recursive=True)
    print(f"Found {len(phase5_flags)} flag(s) in Phase 5 docs")
    
    # Scan features directory
    features_flags = scan_for_feature_flags(FEATURES_ROOT, recursive=True)
    print(f"Found {len(features_flags)} flag(s) in features directory")
    
    # Scan chat_mirror (WORKING only by default)
    chat_flags = scan_for_feature_flags(CHAT_MIRROR_ROOT, recursive=True, limit_status="WORKING")
    print(f"Found {len(chat_flags)} flag(s) in chat_mirror")
    
    all_flags = phase5_flags + features_flags + chat_flags
    
    # Deduplicate
    unique_flags = deduplicate_flags(all_flags)
    print(f"After deduplication: {len(unique_flags)} unique flag(s)")
    
    # Generate registry
    generate_feature_flags_registry(unique_flags, dry_run=args.dry_run)
    
    print("Feature flag extraction complete!")


if __name__ == "__main__":
    main()

