#!/usr/bin/env python3
"""
Decision Extractor - Scans governance docs and chat_mirror for decisions

Extracts decision candidates and updates 02_DECISIONS_LOG.md (append-only)
and creates DECISION_CANDIDATES.md with items not eligible for promotion.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
RAG_KB_ROOT = REPO_ROOT / "RAG_KB"
KB_PACK_ROOT = RAG_KB_ROOT / "phase5_pack"
BUILD_REPORTS_ROOT = RAG_KB_ROOT / "build_reports"
CHAT_MIRROR_ROOT = RAG_KB_ROOT / "chat_mirror"

# Scan paths
GOVERNANCE_ROOT = REPO_ROOT / "docs" / "PHASE_5" / "00_GOVERNANCE"


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
            content = f.read(2000)  # First 2KB
        front_matter = parse_front_matter(content)
        if "Status" in front_matter:
            return normalize_status(front_matter["Status"])
        # Check filename patterns
        filename = file_path.name.upper()
        if "CANONICAL" in filename or "LOCKED" in filename or "FINAL" in filename:
            return "CANONICAL"
    except:
        pass
    return "WORKING"


def extract_decisions_from_content(content: str, source_path: str, source_status: str) -> List[Dict]:
    """Extract decision candidates from content"""
    decisions = []
    
    # Pattern 1: Headings containing "Decision"
    decision_heading_pattern = r"^#+\s+(.*?Decision.*?)$"
    for match in re.finditer(decision_heading_pattern, content, re.MULTILINE | re.IGNORECASE):
        heading = match.group(1)
        # Find content under this heading (until next heading of same or higher level)
        heading_level = len(match.group(0)) - len(match.group(0).lstrip("#"))
        start_pos = match.end()
        next_heading = re.search(rf"^#{{1,{heading_level}}}\s+", content[start_pos:], re.MULTILINE)
        if next_heading:
            decision_text = content[start_pos:start_pos + next_heading.start()].strip()
        else:
            decision_text = content[start_pos:start_pos + 2000].strip()  # Limit to 2000 chars
        
        if decision_text:
            decisions.append({
                "heading": heading,
                "text": decision_text[:500],  # Limit excerpt
                "source_path": source_path,
                "source_status": source_status,
            })
    
    # Pattern 2: Lines starting with "Decision:" or containing "Status: LOCKED/CANONICAL"
    decision_line_pattern = r"^(?:Decision|Status):\s*(.*?)(?:\n|$)"
    for match in re.finditer(decision_line_pattern, content, re.MULTILINE | re.IGNORECASE):
        decision_text = match.group(1).strip()
        if decision_text and len(decision_text) > 10:  # Filter out very short matches
            decisions.append({
                "heading": "Decision",
                "text": decision_text[:500],
                "source_path": source_path,
                "source_status": source_status,
            })
    
    # Pattern 3: ADR files (Architecture Decision Records)
    if "ADR" in source_path.upper() or "ARCHITECTURE_DECISION" in source_path.upper():
        # Extract decision from ADR format
        context_match = re.search(r"##\s*Context.*?\n(.*?)(?=##|$)", content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        decision_match = re.search(r"##\s*Decision.*?\n(.*?)(?=##|$)", content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if context_match and decision_match:
            decisions.append({
                "heading": "ADR Decision",
                "text": f"Context: {context_match.group(1)[:200]}... Decision: {decision_match.group(1)[:300]}",
                "source_path": source_path,
                "source_status": source_status,
            })
    
    return decisions


def scan_for_decisions(root: Path, recursive: bool = True) -> List[Dict]:
    """Scan directory for decision candidates"""
    all_decisions = []
    
    if not root.exists():
        return all_decisions
    
    pattern = root.rglob if recursive else root.glob
    for file_path in pattern("*.md"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            source_path = str(file_path.relative_to(REPO_ROOT))
            source_status = get_file_status(file_path)
            
            decisions = extract_decisions_from_content(content, source_path, source_status)
            all_decisions.extend(decisions)
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {e}")
            continue
    
    return all_decisions


def is_eligible_for_promotion(decision: Dict) -> bool:
    """Check if decision is eligible to promote to Decisions Log"""
    # Promote if source is CANONICAL/LOCKED, or decision text contains explicit LOCKED/CANONICAL status
    if decision["source_status"] in ("CANONICAL", "LOCKED"):
        return True
    # Check if decision text contains explicit status markers
    text_upper = decision["text"].upper()
    if "STATUS: LOCKED" in text_upper or "STATUS: CANONICAL" in text_upper:
        return True
    return False


def format_decision_entry(decision: Dict, date: str) -> str:
    """Format decision entry for Decisions Log"""
    lines = []
    lines.append(f"### {decision['heading']}")
    lines.append("")
    lines.append(f"**Source:** `{decision['source_path']}`")
    lines.append(f"**Status:** {decision['source_status']}")
    lines.append(f"**Date:** {date}")
    lines.append("")
    lines.append(decision['text'])
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def update_decisions_log(eligible_decisions: List[Dict], dry_run: bool = False):
    """Append eligible decisions to Decisions Log (append-only)"""
    decisions_log_path = KB_PACK_ROOT / "02_DECISIONS_LOG.md"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Read existing log if it exists
    existing_content = ""
    if decisions_log_path.exists():
        with open(decisions_log_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        # Create header if new file
        existing_content = """# Decisions Log

**Purpose:** Append-only log of LOCKED/CANONICAL decisions extracted from Phase 5 governance documents.

**Format:** Decisions are organized by date and include source path, status, and decision text.

---

"""
    
    # Check which decisions are already in the log (by source_path and heading)
    existing_sources = set()
    for match in re.finditer(r"\*\*Source:\*\*\s*`([^`]+)`", existing_content):
        existing_sources.add(match.group(1))
    
    # Filter out decisions that already exist
    new_decisions = [d for d in eligible_decisions if d["source_path"] not in existing_sources]
    
    if not new_decisions:
        print("No new decisions to add to Decisions Log.")
        return
    
    # Append new decisions
    new_content = existing_content
    new_content += f"\n## {today}\n\n"
    for decision in new_decisions:
        new_content += format_decision_entry(decision, today)
    
    if not dry_run:
        decisions_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(decisions_log_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {decisions_log_path}: Added {len(new_decisions)} decision(s)")
    else:
        print(f"DRY RUN: Would add {len(new_decisions)} decision(s) to Decisions Log")


def generate_candidates_report(all_decisions: List[Dict], eligible_decisions: List[Dict], dry_run: bool = False):
    """Generate report of all decision candidates (including non-eligible)"""
    candidates_path = BUILD_REPORTS_ROOT / "DECISION_CANDIDATES.md"
    
    # Separate eligible vs non-eligible
    eligible_paths = {d["source_path"] for d in eligible_decisions}
    non_eligible = [d for d in all_decisions if d["source_path"] not in eligible_paths]
    
    today = datetime.now().isoformat()
    
    content = f"""# Decision Candidates Report

**Generated:** {today}
**Purpose:** Lists all decision candidates found during extraction, including those not eligible for promotion.

---

## Eligible for Promotion ({len(eligible_decisions)})

These decisions are from CANONICAL/LOCKED sources and will be promoted to `02_DECISIONS_LOG.md`:

"""
    
    for decision in eligible_decisions:
        content += f"- **{decision['heading']}** from `{decision['source_path']}` (Status: {decision['source_status']})\n"
        content += f"  - Excerpt: {decision['text'][:150]}...\n\n"
    
    content += f"\n## Not Eligible ({len(non_eligible)})\n\n"
    content += "These decisions are from WORKING/DRAFT sources and remain as candidates only:\n\n"
    
    for decision in non_eligible:
        content += f"- **{decision['heading']}** from `{decision['source_path']}` (Status: {decision['source_status']})\n"
        content += f"  - Excerpt: {decision['text'][:150]}...\n\n"
    
    content += "\n---\n\n"
    content += "**Note:** Non-eligible decisions can be promoted after their source documents are promoted to CANONICAL status.\n"
    
    if not dry_run:
        candidates_path.parent.mkdir(parents=True, exist_ok=True)
        with open(candidates_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {candidates_path}: {len(all_decisions)} candidates total")
    else:
        print(f"DRY RUN: Would generate candidates report with {len(all_decisions)} candidates")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract decisions from governance docs")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    print("Scanning for decisions...")
    
    # Scan governance docs
    governance_decisions = scan_for_decisions(GOVERNANCE_ROOT, recursive=True)
    print(f"Found {len(governance_decisions)} decision(s) in governance docs")
    
    # Scan chat_mirror
    chat_decisions = scan_for_decisions(CHAT_MIRROR_ROOT, recursive=True)
    print(f"Found {len(chat_decisions)} decision(s) in chat_mirror")
    
    all_decisions = governance_decisions + chat_decisions
    
    # Separate eligible vs non-eligible
    eligible_decisions = [d for d in all_decisions if is_eligible_for_promotion(d)]
    print(f"{len(eligible_decisions)} eligible for promotion, {len(all_decisions) - len(eligible_decisions)} candidates only")
    
    # Update Decisions Log
    update_decisions_log(eligible_decisions, dry_run=args.dry_run)
    
    # Generate candidates report
    generate_candidates_report(all_decisions, eligible_decisions, dry_run=args.dry_run)
    
    print("Decision extraction complete!")


if __name__ == "__main__":
    main()

