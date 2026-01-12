#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parents[2]

# Telemetry is stored in source_snapshot (verified in Step 1)
TELEMETRY_LOG = REPO_ROOT / "source_snapshot" / "storage" / "logs" / "rag_telemetry.jsonl"
OUT_MD = REPO_ROOT / "RAG_KB" / "phase5_pack" / "09_TELEMETRY_SUMMARY.md"

JSON_RE = re.compile(r"(\{.*\})\s*$")  # last {...} on each line


def parse_jsonl_line(line: str) -> dict | None:
    m = JSON_RE.search(line)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def normalize_query(q: str) -> str:
    q = (q or "").strip()
    q = re.sub(r"\s+", " ", q)
    return q[:400]


def percentile(values: list[int], p: float) -> int:
    if not values:
        return 0
    values = sorted(values)
    k = int(round((len(values) - 1) * p))
    return values[max(0, min(k, len(values) - 1))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tail", type=int, default=2000, help="Read last N lines of telemetry")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    lines = []
    if TELEMETRY_LOG.exists():
        raw = TELEMETRY_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
        lines = raw[-args.tail:]
    else:
        raw = []
        lines = []

    events = []
    for ln in lines:
        obj = parse_jsonl_line(ln)
        if obj:
            events.append(obj)

    total = len(events)
    ok = sum(1 for e in events if e.get("status") == "ok")
    err = sum(1 for e in events if e.get("status") == "error")

    screens = Counter((e.get("screen") or "unknown") for e in events)
    best_auth = Counter((e.get("best_authority") or "unknown") for e in events)

    queries = Counter(normalize_query(e.get("query", "")) for e in events if e.get("query"))

    lat = [int(e.get("latency_ms")) for e in events if str(e.get("latency_ms", "")).isdigit()]
    avg_lat = int(mean(lat)) if lat else 0
    p95_lat = percentile(lat, 0.95) if lat else 0

    cited = Counter()
    for e in events:
        for c in (e.get("citations") or []):
            key = c.get("kb_path") or c.get("source_path") or ""
            if key:
                cited[key] += 1

    canonical_hits = sum(1 for e in events if (e.get("best_authority") or "").upper() == "CANONICAL")
    canonical_rate = round((canonical_hits / total) * 100, 2) if total else 0.0

    now = datetime.now().isoformat(timespec="seconds")

    md = []
    md.append("# Telemetry Summary (Auto-Generated)")
    md.append("")
    md.append(f"**Generated:** {now}")
    md.append(f"**Source:** `{TELEMETRY_LOG.relative_to(REPO_ROOT) if TELEMETRY_LOG.exists() else str(TELEMETRY_LOG)}`")
    md.append(f"**Lines Read:** {min(len(lines), args.tail)}")
    md.append(f"**Events Parsed:** {total}")
    md.append("")
    md.append("## Health")
    md.append(f"- OK: {ok}")
    md.append(f"- Error: {err}")
    md.append(f"- Canonical exposure rate: {canonical_rate}%")
    md.append(f"- Avg latency: {avg_lat} ms")
    md.append(f"- P95 latency: {p95_lat} ms")
    md.append("")
    md.append("## Top Screens")
    for k, v in screens.most_common(10):
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Best Authority Distribution")
    for k, v in best_auth.most_common(10):
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Top Queries")
    for q, v in queries.most_common(10):
        md.append(f"- ({v}) {q}")
    md.append("")
    md.append("## Top Cited Sources")
    for s, v in cited.most_common(15):
        md.append(f"- ({v}) `{s}`")
    md.append("")
    md.append("## Notes / Actions")
    md.append("- If canonical exposure is low, promote key governance/rules docs to CANONICAL.")
    md.append("- If latency p95 is high, review caching and kb_query health.")
    md.append("- If repeated queries fail, add missing docs or improve flags/decisions extraction.")
    md.append("")

    out_text = "\n".join(md) + "\n"

    if args.dry_run:
        print(out_text)
        return

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(out_text, encoding="utf-8")
    print(f"[OK] Wrote {OUT_MD}")


if __name__ == "__main__":
    main()

