"""
Week-4 Day-2: Integrity Hash Change on QCA Update (Phase-6)

Uses existing cost-adder upsert (Week-3) to change a value and confirms
integrity hash changes, then reverts to keep environment stable.
"""
import os
import requests

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))

QID = int(os.getenv("NSW_COST_QID", "4"))
PANEL_ID = int(os.getenv("NSW_COST_PANEL_ID", "8"))


def _headers():
    return {"Content-Type": "application/json", "X-Tenant-ID": str(TENANT_ID), "X-User-ID": str(USER_ID)}


def _get_summary():
    """Get cost summary and return JSON"""
    r = requests.get(f"{API_BASE}/quotation/{QID}/cost-summary", headers=_headers(), timeout=30)
    assert r.status_code == 200, r.text
    return r.json()


def _upsert_busbar(amount: float, notes: str):
    """Upsert BUSBAR cost adder"""
    r = requests.post(
        f"{API_BASE}/quotation/{QID}/panels/{PANEL_ID}/cost-adders",
        headers=_headers(),
        json={"cost_head_code": "BUSBAR", "amount": amount, "currency": "INR", "notes": notes},
        timeout=30,
    )
    assert r.status_code == 200, r.text
    return r.json()


def test_integrity_hash_changes_on_qca_update_then_reverts():
    """Test that integrity hash changes on QCA update, then reverts"""
    before = _get_summary()
    h1 = before.get("integrity_hash")
    assert isinstance(h1, str) and len(h1) >= 32

    # Capture current BUSBAR value if present (for revert)
    cur_busbar = None
    for p in before.get("panels", []):
        if p.get("panel_id") == PANEL_ID:
            cur_busbar = float((p.get("cost_heads") or {}).get("BUSBAR", 0.0))

    # Update to a different amount
    new_amt = cur_busbar + 123.0 if cur_busbar is not None else 123.0
    _upsert_busbar(new_amt, "week4 day2 integrity change")

    mid = _get_summary()
    h2 = mid.get("integrity_hash")
    assert h2 != h1, f"Expected integrity_hash to change after QCA update. {h1} == {h2}"

    # Revert to original amount (best-effort environment stability)
    if cur_busbar is not None:
        _upsert_busbar(cur_busbar, "week4 day2 revert")

        after = _get_summary()
        h3 = after.get("integrity_hash")
        assert h3 == h1, "Expected integrity_hash to revert after restoring original BUSBAR amount"
