import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Waiver:
    rule_id: str
    expires_on: date
    owner: str
    rationale: str
    scope: str | None = None
    link: str | None = None


def _parse_date(s: str) -> date:
    return date.fromisoformat(s)


def _load_waivers(path: Path) -> dict[str, Waiver]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"Waivers must be a JSON list: {path}")
    out: dict[str, Waiver] = {}
    for i, row in enumerate(raw):
        if not isinstance(row, dict):
            raise ValueError(f"Invalid waiver entry at index {i}: must be object")
        wid = str(row.get("rule_id") or "").strip()
        if not wid:
            raise ValueError(f"Invalid waiver entry at index {i}: missing rule_id")
        expires = str(row.get("expires_on") or "").strip()
        owner = str(row.get("owner") or "").strip()
        rationale = str(row.get("rationale") or "").strip()
        if not expires or not owner or not rationale:
            raise ValueError(f"Invalid waiver entry for {wid}: requires expires_on/owner/rationale")
        out[wid] = Waiver(
            rule_id=wid,
            expires_on=_parse_date(expires),
            owner=owner,
            rationale=rationale,
            scope=(str(row.get("scope")).strip() if row.get("scope") is not None else None),
            link=(str(row.get("link")).strip() if row.get("link") is not None else None),
        )
    return out


def _severity_for_result(result: dict[str, Any], rules_by_id: dict[str, dict[str, Any]]) -> float | None:
    """
    Try a few common SARIF encodings:
    - result.properties.securitySeverity (CodeQL style)
    - result.properties["security-severity"]
    - rule.properties.securitySeverity (rule-level)
    """
    rule_id = str(result.get("ruleId") or "")
    props = result.get("properties") if isinstance(result.get("properties"), dict) else {}
    if isinstance(props, dict):
        for key in ("securitySeverity", "security-severity", "security_severity"):
            if key in props:
                try:
                    return float(props[key])
                except Exception:
                    return None
    rule = rules_by_id.get(rule_id) if rule_id else None
    if isinstance(rule, dict):
        rprops = rule.get("properties") if isinstance(rule.get("properties"), dict) else {}
        if isinstance(rprops, dict):
            for key in ("securitySeverity", "security-severity", "security_severity"):
                if key in rprops:
                    try:
                        return float(rprops[key])
                    except Exception:
                        return None
    return None


def _collect_rules_by_id(sarif: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    runs = sarif.get("runs") if isinstance(sarif.get("runs"), list) else []
    if not runs:
        return out
    tool = runs[0].get("tool") if isinstance(runs[0].get("tool"), dict) else {}
    driver = tool.get("driver") if isinstance(tool.get("driver"), dict) else {}
    rules = driver.get("rules") if isinstance(driver.get("rules"), list) else []
    for r in rules:
        if isinstance(r, dict) and r.get("id"):
            out[str(r["id"])] = r
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Gate pip-audit SARIF by severity with expiring waivers.")
    ap.add_argument("--sarif", nargs="+", required=True, help="One or more pip-audit SARIF files.")
    ap.add_argument(
        "--waivers",
        default="docs/GOVERNANCE/waivers_sca.json",
        help="Path to JSON waivers list.",
    )
    ap.add_argument("--medium", type=float, default=4.0, help="MEDIUM threshold (inclusive).")
    ap.add_argument("--high", type=float, default=7.0, help="HIGH threshold (inclusive).")
    args = ap.parse_args()

    waivers = _load_waivers(Path(args.waivers))
    today = date.today()

    high_findings: list[tuple[str, float, str]] = []
    medium_findings_unwaived: list[tuple[str, float, str]] = []
    expired_waivers: list[str] = []

    for p in [Path(x) for x in args.sarif]:
        if not p.exists():
            continue
        sarif = json.loads(p.read_text(encoding="utf-8"))
        rules_by_id = _collect_rules_by_id(sarif)
        runs = sarif.get("runs") if isinstance(sarif.get("runs"), list) else []
        if not runs:
            continue
        results = runs[0].get("results") if isinstance(runs[0].get("results"), list) else []
        for res in results:
            if not isinstance(res, dict):
                continue
            rule_id = str(res.get("ruleId") or "").strip() or "UNKNOWN"
            sev = _severity_for_result(res, rules_by_id)
            # If pip-audit doesn't supply a numeric severity, be conservative.
            sev_val = float(sev) if sev is not None else 10.0

            waiver = waivers.get(rule_id)
            if waiver and waiver.expires_on < today:
                expired_waivers.append(f"{rule_id} (expired {waiver.expires_on.isoformat()})")
                waiver = None

            if sev_val >= args.high:
                high_findings.append((rule_id, sev_val, p.name))
            elif sev_val >= args.medium:
                if not waiver:
                    medium_findings_unwaived.append((rule_id, sev_val, p.name))

    if expired_waivers:
        print("Expired SCA waivers found (must be renewed or removed):")
        for x in sorted(set(expired_waivers)):
            print(f"- {x}")
        return 2

    if high_findings:
        print(f"SCA gate: HIGH findings present (severity >= {args.high}). No waivers allowed.")
        for rule_id, sev, fname in sorted(high_findings, key=lambda t: (-t[1], t[0], t[2])):
            print(f"- {rule_id} severity={sev} file={fname}")
        return 1

    if medium_findings_unwaived:
        print(f"SCA gate: MEDIUM findings present (severity >= {args.medium}) without waivers.")
        print(f"Add expiring waivers in: {args.waivers}")
        for rule_id, sev, fname in sorted(medium_findings_unwaived, key=lambda t: (-t[1], t[0], t[2])):
            print(f"- {rule_id} severity={sev} file={fname}")
        return 1

    print("SCA gate: PASS (no HIGH findings; MEDIUM findings waived or absent).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

