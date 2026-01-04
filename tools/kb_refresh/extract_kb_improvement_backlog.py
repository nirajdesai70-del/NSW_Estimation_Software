#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

FEEDBACK_LOG = REPO_ROOT / "source_snapshot" / "storage" / "logs" / "rag_feedback.jsonl"
TELEMETRY_LOG = REPO_ROOT / "source_snapshot" / "storage" / "logs" / "rag_telemetry.jsonl"

OUT_MD = REPO_ROOT / "RAG_KB" / "phase5_pack" / "11_KB_IMPROVEMENT_BACKLOG.md"

JSON_RE = re.compile(r"(\{.*\})\s*$")

def parse_jsonl_line(line: str) -> dict | None:
    m = JSON_RE.search(line)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

def norm_query(q: str) -> str:
    q = (q or "").strip()
    q = re.sub(r"\s+", " ", q)
    return q[:300]

def load_events(path: Path, tail: int) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[-tail:]
    out = []
    for ln in lines:
        obj = parse_jsonl_line(ln)
        if obj:
            out.append(obj)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feedback-tail", type=int, default=3000)
    ap.add_argument("--telemetry-tail", type=int, default=3000)
    ap.add_argument("--min-downvotes", type=int, default=2)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    fb = load_events(FEEDBACK_LOG, args.feedback_tail)
    tel = load_events(TELEMETRY_LOG, args.telemetry_tail)

    # --- Build downvote clusters ---
    down = [e for e in fb if (e.get("rating") or "").lower() == "down"]
    up = [e for e in fb if (e.get("rating") or "").lower() == "up"]

    down_by_query = Counter(norm_query(e.get("query","")) for e in down if e.get("query"))
    up_by_query = Counter(norm_query(e.get("query","")) for e in up if e.get("query"))

    # citations implicated in downvotes
    down_cites = Counter()
    down_cites_by_query = defaultdict(Counter)

    for e in down:
        q = norm_query(e.get("query",""))
        for c in (e.get("citations") or [])[:10]:
            key = c.get("kb_path") or c.get("source_path") or ""
            if not key:
                continue
            down_cites[key] += 1
            if q:
                down_cites_by_query[q][key] += 1

    # --- Telemetry for "high traffic but low confidence" ---
    tel_queries = Counter(norm_query(e.get("query","")) for e in tel if e.get("query"))
    tel_errors = sum(1 for e in tel if e.get("status") == "error")
    tel_ok = sum(1 for e in tel if e.get("status") == "ok")

    best_auth = Counter((e.get("best_authority") or "unknown").upper() for e in tel)

    # Identify "high traffic & downvoted"
    high_traffic_down = []
    for q, dv in down_by_query.most_common(50):
        if dv >= args.min_downvotes:
            high_traffic_down.append((q, dv, tel_queries.get(q, 0)))

    # Identify "high traffic but no feedback yet"
    no_feedback = []
    for q, cnt in tel_queries.most_common(50):
        if q and down_by_query.get(q, 0) == 0 and up_by_query.get(q, 0) == 0:
            no_feedback.append((q, cnt))

    now = datetime.now().isoformat(timespec="seconds")

    md = []
    md.append("# KB Improvement Backlog (Auto-Generated)")
    md.append("")
    md.append(f"**Generated:** {now}")
    md.append(f"**Feedback Source:** `{FEEDBACK_LOG.relative_to(REPO_ROOT) if FEEDBACK_LOG.exists() else str(FEEDBACK_LOG)}`")
    md.append(f"**Telemetry Source:** `{TELEMETRY_LOG.relative_to(REPO_ROOT) if TELEMETRY_LOG.exists() else str(TELEMETRY_LOG)}`")
    md.append("")
    md.append("## Summary Signals")
    md.append(f"- Feedback events: {len(fb)} (👍 {len(up)} / 👎 {len(down)})")
    md.append(f"- Telemetry events: {len(tel)} (ok {tel_ok} / error {tel_errors})")
    md.append(f"- Best authority distribution (telemetry): {dict(best_auth)}")
    md.append("")

    md.append("## P0 — Repeated Downvotes (Action Required)")
    if not high_traffic_down:
        md.append("- None (no repeated downvoted queries above threshold).")
    else:
        for q, dv, tc in high_traffic_down[:15]:
            md.append(f"### {q}")
            md.append(f"- Downvotes: **{dv}** | Telemetry occurrences: **{tc}**")
            top_cites = down_cites_by_query[q].most_common(5)
            if top_cites:
                md.append("- Most implicated sources:")
                for s, n in top_cites:
                    md.append(f"  - ({n}) `{s}`")
            md.append("- Recommended actions:")
            md.append("  - Verify whether correct CANONICAL doc exists; promote if missing.")
            md.append("  - If source is WORKING and correct, promote to CANONICAL with Version.")
            md.append("  - If CANONICAL is wrong/unclear, split rules or add examples.")
            md.append("")

    md.append("## P1 — Top Downvoted Sources (Fix or Deprecate)")
    if not down_cites:
        md.append("- None")
    else:
        for s, n in down_cites.most_common(15):
            md.append(f"- ({n}) `{s}`")
    md.append("")
    md.append("## P2 — High Traffic Queries With No Feedback Yet")
    if not no_feedback:
        md.append("- None")
    else:
        for q, cnt in no_feedback[:15]:
            md.append(f"- ({cnt}) {q}")
    md.append("")
    md.append("## Operating Notes")
    md.append("- This backlog is generated automatically at each kb_refresh.")
    md.append("- Use P0 items for immediate KB corrections (promotions, rule clarifications).")
    md.append("- Use P1 to identify noisy or misleading sources.")
    md.append("- Use P2 to decide where to request feedback (add prompts).")
    md.append("")

    out = "\n".join(md) + "\n"

    if args.dry_run:
        print(out)
        return

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(out, encoding="utf-8")
    print(f"[OK] Wrote {OUT_MD}")

if __name__ == "__main__":
    main()

