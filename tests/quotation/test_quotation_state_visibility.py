"""
Week-4 Day-1: Quotation State Visibility Test (Phase-6)

Ensures quotation lifecycle state is visible via read APIs.
Hard rules:
- Read-only validation only (no transitions)
- No breakup exposure
"""
import os
import requests

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))

QID = int(os.getenv("NSW_COST_QID", "4"))

VALID_STATES = {"DRAFT", "FROZEN", "ISSUED", "ARCHIVED"}


def _headers():
    return {
        "Content-Type": "application/json",
        "X-Tenant-ID": str(TENANT_ID),
        "X-User-ID": str(USER_ID),
    }


def test_cost_summary_includes_state_fields_and_valid_values():
    """Test that cost summary API includes quotation state fields"""
    r = requests.get(
        f"{API_BASE}/quotation/{QID}/cost-summary",
        headers=_headers(),
        timeout=30,
    )
    assert r.status_code == 200, r.text
    data = r.json()

    # Week-3 compatibility
    assert data.get("quotation_id") == QID
    assert "panels" in data and isinstance(data["panels"], list)

    # Week-4 Day-1 additions (read-only)
    assert "quotation_state" in data, "Missing quotation_state in response"
    assert data["quotation_state"] in VALID_STATES, f"Invalid state: {data['quotation_state']}"

    assert "state_timestamp" in data, "Missing state_timestamp in response"
    ts = str(data["state_timestamp"])
    assert len(ts) >= 10, f"state_timestamp too short/unexpected: {ts}"
