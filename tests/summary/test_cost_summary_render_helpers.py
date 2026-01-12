"""
Week-4 Day-3: Cost Summary Render Helpers Test (Phase-6)

Validates new helper fields:
- panel_count matches len(panels)
- has_catalog_bindings is boolean
- cost_head_codes is sorted, unique, and subset of allowed heads
"""
import os
import requests

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))
QID = int(os.getenv("NSW_COST_QID", "4"))

ALLOWED = {
    "FABRICATION",
    "BUSBAR",
    "LABOUR",
    "TRANSPORTATION",
    "ERECTION",
    "COMMISSIONING",
}


def _headers():
    return {
        "Content-Type": "application/json",
        "X-Tenant-ID": str(TENANT_ID),
        "X-User-ID": str(USER_ID),
    }


def test_cost_summary_includes_render_helpers_and_consistent_values():
    """Test that render helper fields are present and consistent"""
    r = requests.get(f"{API_BASE}/quotation/{QID}/cost-summary", headers=_headers(), timeout=30)
    assert r.status_code == 200, r.text
    d = r.json()

    assert "panels" in d and isinstance(d["panels"], list)

    assert "panel_count" in d and isinstance(d["panel_count"], int)
    assert d["panel_count"] == len(d["panels"]), f"panel_count mismatch: {d['panel_count']} != {len(d['panels'])}"

    assert "has_catalog_bindings" in d and isinstance(d["has_catalog_bindings"], bool)

    assert "cost_head_codes" in d and isinstance(d["cost_head_codes"], list)
    codes = d["cost_head_codes"]
    assert codes == sorted(codes), "cost_head_codes must be sorted"
    assert len(codes) == len(set(codes)), "cost_head_codes must be unique"
    for c in codes:
        assert c in ALLOWED, f"Unexpected cost head code in cost_head_codes: {c}"
