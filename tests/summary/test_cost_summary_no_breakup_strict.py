"""
Week-4 Day-3: Cost Summary Strict No-Breakup Test (Phase-6)

Hard denies detail/breakup-style fields by scanning JSON keys recursively.
This is stricter than Week-3 and protects against accidental feature creep.
"""
import os
import requests
from typing import Any, Iterable, Set

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))
QID = int(os.getenv("NSW_COST_QID", "4"))

# Denylist (exact + substring)
FORBIDDEN_KEY_SUBSTRINGS = {
    "breakup",
    "split",
    "detail",
    "details",
    "line_items",
    "lineitems",
    "items",
    "components",
    "materials",
    "material",
    "bom_lines",
    "bom_items",
    "rows",
    "ledger",
    "journal",
}

# Keys explicitly allowed even if they contain risky words (keep empty unless needed)
ALLOW_EXCEPTIONS: Set[str] = set()


def _headers():
    return {
        "Content-Type": "application/json",
        "X-Tenant-ID": str(TENANT_ID),
        "X-User-ID": str(USER_ID),
    }


def _walk_keys(obj: Any) -> Iterable[str]:
    """Recursively walk JSON structure and yield all keys"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k)
            yield from _walk_keys(v)
    elif isinstance(obj, list):
        for it in obj:
            yield from _walk_keys(it)


def test_cost_summary_has_no_breakup_or_detail_keys():
    """Test that cost summary response has no breakup or detail keys"""
    r = requests.get(f"{API_BASE}/quotation/{QID}/cost-summary", headers=_headers(), timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()

    for key in _walk_keys(data):
        k = key.lower()
        if key in ALLOW_EXCEPTIONS:
            continue
        for bad in FORBIDDEN_KEY_SUBSTRINGS:
            assert bad not in k, f"Forbidden key substring '{bad}' found in key: '{key}'"
