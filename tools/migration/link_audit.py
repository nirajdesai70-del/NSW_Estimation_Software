#!/usr/bin/env python3
"""Repo-wide link/path/URL audit.

Scans operational artifacts (md/yaml/json/env/compose/sh/py/ts/tsx/js/csv/txt)
for:
- Markdown links ([text](target))
- Bare URLs
- Absolute paths (macOS /Volumes/..., Windows drive letters)
- localhost/0.0.0.0 ports and service endpoints

Outputs TSV/CSV reports and a summary.

Usage:
  python3 tools/migration/link_audit.py --repo /path/to/repo --out docs/MIGRATION/LINK_AUDIT
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


INCLUDE_EXTS = {
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".env",
    ".txt",
    ".csv",
    ".py",
    ".sh",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}

INCLUDE_FILENAMES_PREFIX = {
    "docker-compose",  # docker-compose.yml, docker-compose.rag.yml, etc.
}

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
}

# Markdown link targets: [text](target) and ![alt](target)
MD_LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")

# Bare URLs
URL_RE = re.compile(r"\bhttps?://[^\s)\]>'\"]+")

# Ports/endpoints
PORT_RE = re.compile(
    r"\b(localhost|127\.0\.0\.1|0\.0\.0\.0)(?::\d{2,5})?\b|\bPORT\b",
    re.IGNORECASE,
)

# Absolute paths
ABS_MAC_RE = re.compile(r"/Volumes/[^\s)\]>'\"]+")
ABS_UNIX_RE = re.compile(r"\b/[^\s)\]>'\"]+")
ABS_WIN_RE = re.compile(r"\b[A-Za-z]:\\[^\s)\]>'\"]+")

# Legacy V1.0 references we specifically care about
V1_HINT_RE = re.compile(r"NSW Estimation Software V1\.0|NSW_Estimation_Software V1\.0", re.IGNORECASE)


def iter_files(repo: Path) -> Iterable[Path]:
    for p in repo.rglob("*"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue
        if p.name.startswith(".") and p.suffix.lower() not in INCLUDE_EXTS:
            # allow hidden only if ext matches
            continue
        if p.suffix.lower() in INCLUDE_EXTS:
            yield p
            continue
        low = p.name.lower()
        if any(low.startswith(pref) for pref in INCLUDE_FILENAMES_PREFIX):
            yield p


def is_probably_external(target: str) -> bool:
    t = target.strip()
    return t.startswith("http://") or t.startswith("https://") or t.startswith("mailto:")


def normalize_md_target(raw: str) -> str:
    t = raw.strip().strip("<>").strip()
    # drop title part: (path "title")
    if " " in t and not t.startswith("http"):
        # keep first token only; titles are separated by space
        t = t.split(" ", 1)[0].strip()
    # strip quotes around target
    t = t.strip('"').strip("'")
    return t


def resolve_internal_target(file_path: Path, repo: Path, target: str) -> Path | None:
    # ignore anchors only
    if target.startswith("#"):
        return None

    # Remove anchor
    base = target.split("#", 1)[0]
    if not base:
        return None

    # If absolute path within repo
    if base.startswith("/"):
        # treat as repo-relative (not filesystem absolute) if it exists under repo
        candidate = (repo / base.lstrip("/")).resolve()
        return candidate

    # relative path
    candidate = (file_path.parent / base).resolve()
    return candidate


@dataclass
class Finding:
    kind: str
    file: str
    line: int
    value: str
    extra: str = ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out_dir = (repo / args.out).resolve() if not str(args.out).startswith("/") else Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    findings: list[Finding] = []
    broken: list[Finding] = []

    for f in iter_files(repo):
        try:
            text = f.read_text(errors="ignore")
        except Exception:
            continue

        rel = f.relative_to(repo).as_posix()
        for i, line in enumerate(text.splitlines(), start=1):
            # URLs
            for m in URL_RE.finditer(line):
                findings.append(Finding("url", rel, i, m.group(0)))

            # Ports/endpoints hints
            if PORT_RE.search(line):
                findings.append(Finding("port_hint", rel, i, line.strip()))

            # V1.0 references
            if V1_HINT_RE.search(line):
                findings.append(Finding("v1_reference", rel, i, line.strip()))

            # Absolute paths
            for m in ABS_MAC_RE.finditer(line):
                findings.append(Finding("abs_path", rel, i, m.group(0), "mac"))
            for m in ABS_WIN_RE.finditer(line):
                findings.append(Finding("abs_path", rel, i, m.group(0), "win"))

            # Markdown links
            if f.suffix.lower() == ".md":
                for m in MD_LINK_RE.finditer(line):
                    raw_target = m.group(2)
                    target = normalize_md_target(raw_target)
                    findings.append(Finding("md_link", rel, i, target))

                    if is_probably_external(target):
                        continue

                    resolved = resolve_internal_target(f, repo, target)
                    if resolved is None:
                        continue

                    # If it looks like a file path (has a dot ext) verify existence
                    # Otherwise still verify existence as directory/file.
                    if not resolved.exists():
                        broken.append(
                            Finding(
                                "broken_md_link",
                                rel,
                                i,
                                target,
                                extra=str(resolved.relative_to(repo).as_posix())
                                if str(resolved).startswith(str(repo))
                                else str(resolved),
                            )
                        )

    # Write outputs
    def write_tsv(name: str, rows: list[Finding]):
        p = out_dir / name
        with p.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, delimiter="\t")
            w.writerow(["kind", "file", "line", "value", "extra"])
            for r in rows:
                w.writerow([r.kind, r.file, r.line, r.value, r.extra])

    write_tsv("all_findings.tsv", findings)
    write_tsv("broken_internal_links.tsv", broken)

    # Summary
    counts = {}
    for r in findings:
        counts[r.kind] = counts.get(r.kind, 0) + 1

    summary_path = out_dir / "summary.txt"
    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write(f"Repo: {repo}\n")
        fh.write(f"Scanned files: {sum(1 for _ in iter_files(repo))}\n")
        fh.write("\nCounts by kind:\n")
        for k in sorted(counts):
            fh.write(f"- {k}: {counts[k]}\n")
        fh.write(f"\nBroken internal markdown links: {len(broken)}\n")

    print(f"✅ Wrote: {out_dir}/all_findings.tsv")
    print(f"✅ Wrote: {out_dir}/broken_internal_links.tsv")
    print(f"✅ Wrote: {out_dir}/summary.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
