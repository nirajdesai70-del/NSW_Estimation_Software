#!/usr/bin/env python3
"""
H3 Governance Gate — Quality and control gates to prevent Phase-5 knowledge base
from drifting into "mostly WORKING noise" again.

What it protects:
- Authority integrity: CANONICAL governance docs must always stay present and discoverable
- Operational stability: prevents accidental removal/renaming of key governance files
- Audit readiness: ensures decisions/policies remain traceable and not overwritten by drafts
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "RAG_KB" / "phase5_pack" / "00_INDEX.json"
RISKS = REPO / "RAG_KB" / "build_reports" / "RISKS_AND_GAPS.md"

MANDATORY_FILES = [
    "RAG_KB/RAG_RULEBOOK.md",
    "RAG_KB/phase5_pack/08_PROMOTION_WORKFLOW.md",
    "docs/PHASE_5/00_GOVERNANCE/PHASE_5_CHARTER.md",
]

CANONICAL_FLOOR = 10
GOV_CANONICAL_FLOOR = 3

def fail(msg: str) -> None:
    """Print failure message and exit with error code."""
    print(f"H3 GATE FAIL: {msg}")
    sys.exit(1)

def read_text(p: Path) -> str:
    """Read file text, returning empty string if file doesn't exist."""
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def has_version_header(text: str) -> bool:
    """Check if file has Version in front-matter header."""
    # simple front-matter check
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    block = text[3:end]
    return bool(re.search(r"(?im)^Version\s*:\s*.+$", block))

def main():
    """Run H3 governance gate checks."""
    if not INDEX.exists():
        fail("Missing 00_INDEX.json. Run kb_refresh first.")

    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    files = idx.get("files", [])
    stats = idx.get("statistics", {})

    # Gate 1: mandatory files present in source set (by source_path)
    src_paths = {f.get("source_path") for f in files}
    for m in MANDATORY_FILES:
        if m not in src_paths:
            fail(f"Mandatory governance doc not indexed: {m}")

    # Gate 2: canonical coverage floors
    canonical_count = stats.get("canonical_count", 0)
    if canonical_count < CANONICAL_FLOOR:
        fail(f"canonical_count={canonical_count} < floor={CANONICAL_FLOOR}")

    # governance canonical floor: count canonical among mandatory set
    gov_canon = 0
    for f in files:
        if f.get("source_path") in MANDATORY_FILES and (f.get("authority") or "").upper() == "CANONICAL":
            gov_canon += 1
    if gov_canon < GOV_CANONICAL_FLOOR:
        fail(f"governance_canonical_count={gov_canon} < floor={GOV_CANONICAL_FLOOR}")

    # Gate 3: no broken active files (from RISKS report)
    risks_text = read_text(RISKS)
    if "Broken _ACTIVE_FILE.txt References" in risks_text and "None detected" not in risks_text:
        # if section exists and isn't "None detected"
        fail("Broken _ACTIVE_FILE.txt detected (see RISKS_AND_GAPS.md)")

    # Gate 4: canonical must have Version in front-matter (for mandatory docs)
    for m in MANDATORY_FILES:
        p = REPO / m
        txt = read_text(p)
        if "Status: CANONICAL" in txt or "Status: LOCKED" in txt:
            if not has_version_header(txt):
                fail(f"Canonical file missing Version header: {m}")

    print("H3 GATE PASS: governance integrity checks OK ✅")

if __name__ == "__main__":
    main()

