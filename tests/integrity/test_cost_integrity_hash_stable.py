"""
Week-4 Day-2: Integrity Hash Stability Test (Phase-6)

Ensures cost-summary returns integrity hash and it is stable between calls
when data is unchanged.
"""
import os
import requests
import time

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))
QID = int(os.getenv("NSW_COST_QID", "4"))


def _headers():
    return {"Content-Type": "application/json", "X-Tenant-ID": str(TENANT_ID), "X-User-ID": str(USER_ID)}


def test_integrity_hash_present_and_stable_when_unchanged():
    """Test that integrity hash is present and stable when data is unchanged"""
    r1 = requests.get(f"{API_BASE}/quotation/{QID}/cost-summary", headers=_headers(), timeout=30)
    assert r1.status_code == 200, r1.text
    d1 = r1.json()
    assert d1.get("integrity_status") in ("OK", "DRIFT")
    h1 = d1.get("integrity_hash")
    assert isinstance(h1, str) and len(h1) >= 32, f"Missing/invalid integrity_hash: {h1}"

    # small delay (should not change because state_timestamp is derived from DB updated_at)
    time.sleep(0.1)

    r2 = requests.get(f"{API_BASE}/quotation/{QID}/cost-summary", headers=_headers(), timeout=30)
    assert r2.status_code == 200, r2.text
    d2 = r2.json()
    h2 = d2.get("integrity_hash")
    assert h2 == h1, f"Expected stable integrity_hash for unchanged data. {h1} != {h2}"
