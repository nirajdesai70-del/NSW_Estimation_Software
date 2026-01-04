#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parents[2]

# Feedback log location (same pattern as telemetry; adjust if you store elsewhere)
FEEDBACK_LOG = REPO_ROOT / "source_snapshot" / "storage" / "logs" / "rag_feedback.jsonl"
OUT_MD = REPO_ROOT / "RAG_KB" / "phase5_pack" / "10_FEEDBACK_SUMMARY.md"

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
    ap.add_argument("--tail", type=int, default=2000, help="Read last N lines of feedback log")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    lines = []
    if FEEDBACK_LOG.exists():
        raw = FEEDBACK_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
        lines = raw[-args.tail:]
    else:
        raw = []
        lines = []

    events = []
    for ln in lines:
        obj = parse_jsonl_line(ln)
        if obj:
            # Only process feedback records (ignore any test markers)
            if obj.get("status") in ("feedback", "ok", "error") or obj.get("rating") in ("up", "down"):
                events.append(obj)

    total = len(events)
    up = sum(1 for e in events if (e.get("rating") or "").lower() == "up")
    down = sum(1 for e in events if (e.get("rating") or "").lower() == "down")

    screens = Counter((e.get("context", {}).get("screen") if isinstance(e.get("context"), dict) else None) or "unknown" for e in events)
    best_auth = Counter((e.get("best_authority") or "unknown") for e in events)

    # Latency
    lat = [int(e.get("latency_ms")) for e in events if str(e.get("latency_ms", "")).isdigit()]
    avg_lat = int(mean(lat)) if lat else 0
    p95_lat = percentile(lat, 0.95) if lat else 0

    # Queries
    q_all = Counter(normalize_query(e.get("query", "")) for e in events if e.get("query"))
    q_down = Counter(normalize_query(e.get("query", "")) for e in events if (e.get("rating") or "").lower() == "down" and e.get("query"))
    q_up = Counter(normalize_query(e.get("query", "")) for e in events if (e.get("rating") or "").lower() == "up" and e.get("query"))

    # Top cited sources in downvotes
    cited_down = Counter()
    cited_up = Counter()

    # Track per-query downvote citations to highlight likely weak docs
    down_citations_by_query = defaultdict(Counter)

    for e in events:
        rating = (e.get("rating") or "").lower()
        citations = e.get("citations") or []
        nq = normalize_query(e.get("query", ""))

        for c in citations[:10]:
            key = c.get("kb_path") or c.get("source_path") or ""
            if not key:
                continue
            if rating == "down":
                cited_down[key] += 1
                if nq:
                    down_citations_by_query[nq][key] += 1
            elif rating == "up":
                cited_up[key] += 1

    # Canonical exposure in downvotes
    down_canonical = sum(1 for e in events if (e.get("rating") or "").lower() == "down" and (e.get("best_authority") or "").upper() == "CANONICAL")
    down_rate_canonical = round((down_canonical / down) * 100, 2) if down else 0.0

    now = datetime.now().isoformat(timespec="seconds")

    md = []
    md.append("# Feedback Summary (Auto-Generated)")
    md.append("")
    md.append(f"**Generated:** {now}")
    md.append(f"**Source:** `{FEEDBACK_LOG.relative_to(REPO_ROOT) if FEEDBACK_LOG.exists() else str(FEEDBACK_LOG)}`")
    md.append(f"**Lines Read:** {min(len(lines), args.tail)}")
    md.append(f"**Events Parsed:** {total}")
    md.append("")
    md.append("## Health")
    md.append(f"- 👍 Up: {up}")
    md.append(f"- 👎 Down: {down}")
    md.append(f"- Avg latency: {avg_lat} ms")
    md.append(f"- P95 latency: {p95_lat} ms")
    md.append(f"- Downvotes with CANONICAL best_authority: {down_rate_canonical}%")
    md.append("")
    md.append("## Top Screens")
    for k, v in screens.most_common(10):
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Best Authority Distribution")
    for k, v in best_auth.most_common(10):
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Top Queries (All)")
    for q, v in q_all.most_common(10):
        md.append(f"- ({v}) {q}")
    md.append("")
    md.append("## Top Queries (Downvoted)")
    if down:
        for q, v in q_down.most_common(10):
            md.append(f"- ({v}) {q}")
    else:
        md.append("- None")
    md.append("")
    md.append("## Top Cited Sources in Downvotes")
    if cited_down:
        for s, v in cited_down.most_common(15):
            md.append(f"- ({v}) `{s}`")
    else:
        md.append("- None")
    md.append("")
    md.append("## Top Cited Sources in Upvotes")
    if cited_up:
        for s, v in cited_up.most_common(15):
            md.append(f"- ({v}) `{s}`")
    else:
        md.append("- None")
    md.append("")
    md.append("## Weak-Signal Drilldown (Top 5 Downvoted Queries → top citations)")
    if q_down:
        for q, _ in q_down.most_common(5):
            md.append(f"### {q}")
            top_cites = down_citations_by_query[q].most_common(5)
            if not top_cites:
                md.append("- No citations logged")
            else:
                for s, v in top_cites:
                    md.append(f"- ({v}) `{s}`")
            md.append("")
    else:
        md.append("- None")
        md.append("")
    md.append("## Notes / Actions")
    md.append("- Repeated downvotes on the same query usually indicate missing KB coverage or wrong top-ranked sources.")
    md.append("- If downvotes cluster around WORKING sources, consider promoting the correct governance/rules doc to CANONICAL.")
    md.append("- If downvotes cluster around CANONICAL sources, the canonical doc may need clarification, examples, or split into smaller rules.")
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

