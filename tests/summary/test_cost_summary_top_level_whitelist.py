"""
Week-4 Day-4: Cost Summary Top-Level Whitelist Test (Phase-6)

Prevents accidental API surface creep by enforcing an explicit allowlist
of top-level keys in the cost-summary response.

If a new top-level field is needed, update the allowlist deliberately.
"""
import os
import requests

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))
QID = int(os.getenv("NSW_COST_QID", "4"))

ALLOWED_TOP_LEVEL_KEYS = {
    "quotation_id",
    "panels",
    "quotation_state",
    "state_timestamp",
    "integrity_status",
    "integrity_hash",
    "integrity_reasons",
    "panel_count",
    "has_catalog_bindings",
    "cost_head_codes",
}


def _headers():
    return {
        "Content-Type": "application/json",
        "X-Tenant-ID": str(TENANT_ID),
        "X-User-ID": str(USER_ID),
    }


def test_cost_summary_top_level_keys_are_whitelisted():
    r = requests.get(
        f"{API_BASE}/quotation/{QID}/cost-summary", headers=_headers(), timeout=30
    )
    assert r.status_code == 200, r.text
    d = r.json()
    assert isinstance(d, dict)

    keys = set(d.keys())
    unexpected = keys - ALLOWED_TOP_LEVEL_KEYS
    assert not unexpected, (
        f"Unexpected top-level keys in cost-summary response: {sorted(list(unexpected))}"
    )
