#!/usr/bin/env python3
"""V1.0 baseline → execution repo full path mapping (Phase B).

Phase B is "read + report only":
- No copying
- No deletions
- No renames
- No link fixing

This script inventories **operational artifacts only** (by extension) in:
- Baseline root (external, read-only): /Volumes/T9/Projects/NSW Estimation Software V1.0/
- Execution root (authoritative): this repo root

Outputs:
- docs/MIGRATION/INVENTORIES/v1_operational_inventory.csv
- docs/MIGRATION/INVENTORIES/execution_operational_inventory.csv
- docs/MIGRATION/V1_TO_EXECUTION_FULL_PATH_MAP.csv
- docs/MIGRATION/MISSING_IN_EXECUTION_DECISION_LIST.csv

Mapping is intentionally conservative: only exact relative-path matches are treated as mapped.

Usage:
  python3 tools/migration/v1_to_exec_map.py
  python3 tools/migration/v1_to_exec_map.py --v1-root "/Volumes/T9/Projects/NSW Estimation Software V1.0" --exec-root .
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


# Per docs/GOVERNANCE/ROOT_STREAMLINING_PLAN_v1.0.md §4.1
INCLUDE_EXTS = {
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".txt",
    ".csv",
    ".py",
    ".sh",
}

# Special filename patterns explicitly called out
INCLUDE_FILENAMES_PREFIX = {
    "docker-compose",  # docker-compose.yml, docker-compose.rag.yml, etc.
    ".env",  # .env, .env.local, .env.production, etc.
}

# Generic excludes (noise / build / VCS)
EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    # caches / editor state (not operational artifacts)
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".cache",
    ".tox",
    ".idea",
    ".vscode",
    ".cursor",
}


@dataclass(frozen=True)
class InventoryRow:
    rel_path: str
    abs_path: str
    size_bytes: int
    mtime_utc: str


def _iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def iter_operational_files(root: Path) -> Iterable[Path]:
    """
    Yield operational artifacts under root.
    Rules:
    - include by extension set OR by filename prefix (docker-compose*, .env*)
    - exclude common noise dirs
    """
    for p in root.rglob("*"):
        # fast path: skip excluded dirs
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue

        # macOS filesystem noise (AppleDouble/resource forks, Finder)
        # These are not operational artifacts and create massive false "missing" noise.
        if p.name.startswith("._") or p.name in {".DS_Store", "Icon\r"}:
            continue

        low_name = p.name.lower()
        low_suffix = p.suffix.lower()

        if low_suffix in INCLUDE_EXTS:
            yield p
            continue

        # include docker-compose* even if extension isn't caught (still usually .yml)
        if any(low_name.startswith(pref) for pref in INCLUDE_FILENAMES_PREFIX):
            yield p


def build_inventory(root: Path) -> dict[str, InventoryRow]:
    """
    Inventory keyed by repo-relative POSIX path.
    """
    inv: dict[str, InventoryRow] = {}
    for f in iter_operational_files(root):
        try:
            rel = f.relative_to(root).as_posix()
        except Exception:
            # should never happen, but keep conservative
            continue
        try:
            st = f.stat()
        except Exception:
            continue
        inv[rel] = InventoryRow(
            rel_path=rel,
            abs_path=str(f.resolve()),
            size_bytes=int(st.st_size),
            mtime_utc=_iso_utc(st.st_mtime),
        )
    return inv


def write_inventory_csv(out_path: Path, rows: Iterable[InventoryRow]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rel_path", "abs_path", "size_bytes", "mtime_utc"])
        for r in sorted(rows, key=lambda x: x.rel_path):
            w.writerow([r.rel_path, r.abs_path, r.size_bytes, r.mtime_utc])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--v1-root",
        default="/Volumes/T9/Projects/NSW Estimation Software V1.0",
        help="Baseline root (external read-only).",
    )
    ap.add_argument(
        "--exec-root",
        default=None,
        help="Execution repo root. Defaults to repo root inferred from this script location.",
    )
    ap.add_argument(
        "--out-map",
        default=None,
        help="Output mapping CSV path. Defaults to docs/MIGRATION/V1_TO_EXECUTION_FULL_PATH_MAP.csv under exec root.",
    )
    ap.add_argument(
        "--out-inv-dir",
        default=None,
        help="Inventory output directory. Defaults to docs/MIGRATION/INVENTORIES under exec root.",
    )
    ap.add_argument(
        "--out-missing",
        default=None,
        help="Output decision list CSV for status=MISSING_IN_EXECUTION.",
    )
    args = ap.parse_args()

    run_date = datetime.now(timezone.utc).date().isoformat()  # YYYY-MM-DD (UTC)

    v1_root = Path(args.v1_root).resolve()
    exec_root = (
        Path(args.exec_root).resolve()
        if args.exec_root
        else Path(__file__).resolve().parents[2]
    )

    if not v1_root.exists() or not v1_root.is_dir():
        raise SystemExit(f"Baseline root not found or not a directory: {v1_root}")
    if not exec_root.exists() or not exec_root.is_dir():
        raise SystemExit(f"Execution root not found or not a directory: {exec_root}")

    out_map = (
        Path(args.out_map).resolve()
        if args.out_map
        else (exec_root / "docs/MIGRATION/V1_TO_EXECUTION_FULL_PATH_MAP.csv").resolve()
    )
    out_inv_dir = (
        Path(args.out_inv_dir).resolve()
        if args.out_inv_dir
        else (exec_root / "docs/MIGRATION/INVENTORIES").resolve()
    )
    out_missing = (
        Path(args.out_missing).resolve()
        if args.out_missing
        else (exec_root / "docs/MIGRATION/MISSING_IN_EXECUTION_DECISION_LIST.csv").resolve()
    )

    # Optional date-stamped siblings (prevents overwrite) when using defaults
    out_map_dated = None
    out_missing_dated = None
    if args.out_map is None:
        out_map_dated = (out_map.parent / f"V1_TO_EXECUTION_FULL_PATH_MAP_{run_date}.csv").resolve()
    if args.out_missing is None:
        out_missing_dated = (out_missing.parent / f"MISSING_IN_EXECUTION_DECISION_LIST_{run_date}.csv").resolve()

    # Build inventories
    v1_inv = build_inventory(v1_root)
    exec_inv = build_inventory(exec_root)

    # Write inventories (operational artifacts only)
    write_inventory_csv(out_inv_dir / "v1_operational_inventory.csv", v1_inv.values())
    write_inventory_csv(out_inv_dir / "execution_operational_inventory.csv", exec_inv.values())

    # Build mapping rows (union of relative paths)
    all_rel = set(v1_inv.keys()) | set(exec_inv.keys())

    out_map.parent.mkdir(parents=True, exist_ok=True)
    out_missing.parent.mkdir(parents=True, exist_ok=True)
    if out_map_dated is not None:
        out_map_dated.parent.mkdir(parents=True, exist_ok=True)
    if out_missing_dated is not None:
        out_missing_dated.parent.mkdir(parents=True, exist_ok=True)

    missing_rows: list[list[str]] = []

    def write_map_csv(path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            # Required columns per ROOT_STREAMLINING_PLAN_v1.0.md §4.2
            # Governance: use repo-relative paths (portable; avoids absolute-path ban)
            w.writerow(["old_path", "new_path", "mapping_type", "status", "notes"])

            for rel in sorted(all_rel):
                v1_row = v1_inv.get(rel)
                ex_row = exec_inv.get(rel)

                if v1_row and ex_row:
                    w.writerow([v1_row.rel_path, ex_row.rel_path, "EXACT_RELATIVE_PATH", "MAPPED", ""])
                elif v1_row and not ex_row:
                    w.writerow([v1_row.rel_path, "", "NONE", "MISSING_IN_EXECUTION", ""])
                elif ex_row and not v1_row:
                    w.writerow(["", ex_row.rel_path, "NONE", "NEW_IN_EXECUTION", ""])

    # Build missing list once (relative paths)
    for rel in sorted(all_rel):
        v1_row = v1_inv.get(rel)
        ex_row = exec_inv.get(rel)
        if v1_row and not ex_row:
            missing_rows.append([v1_row.rel_path, "", "NONE", "MISSING_IN_EXECUTION", ""])

    # Write canonical map (+ dated sibling if applicable)
    write_map_csv(out_map)
    if out_map_dated is not None:
        write_map_csv(out_map_dated)

    # Decision list: status=MISSING_IN_EXECUTION
    def write_missing_csv(path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["old_path", "new_path", "mapping_type", "status", "notes", "decision"])
            for r in missing_rows:
                # decision is intentionally blank for human triage: ADOPTED / REFERENCE_ONLY / REJECTED
                w.writerow([*r, ""])

    write_missing_csv(out_missing)
    if out_missing_dated is not None:
        write_missing_csv(out_missing_dated)

    print("✅ Phase B outputs written:")
    print(f"- {out_inv_dir / 'v1_operational_inventory.csv'}")
    print(f"- {out_inv_dir / 'execution_operational_inventory.csv'}")
    print(f"- {out_map}")
    print(f"- {out_missing}")
    if out_map_dated is not None:
        print(f"- {out_map_dated}")
    if out_missing_dated is not None:
        print(f"- {out_missing_dated}")
    print(f"\nCounts:")
    print(f"- v1_operational_files: {len(v1_inv)}")
    print(f"- execution_operational_files: {len(exec_inv)}")
    print(f"- mapped_exact: {len(set(v1_inv.keys()) & set(exec_inv.keys()))}")
    print(f"- missing_in_execution: {len(missing_rows)}")
    print(f"- new_in_execution: {len(set(exec_inv.keys()) - set(v1_inv.keys()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

