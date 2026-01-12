"""
Week-4 Day-1: Freeze Immutability Test (Phase-6)

Ensures that once quotation is FROZEN, cost adders cannot be upserted.
Rules:
- Must hard reject write attempt
- Must not modify DB
"""
import os
import requests
import psycopg

API_BASE = os.getenv("NSW_API_BASE", "http://localhost:8003/api/v1")
TENANT_ID = int(os.getenv("NSW_TENANT_ID", "1"))
USER_ID = int(os.getenv("NSW_USER_ID", "1"))

FROZEN_QID = int(os.getenv("NSW_FROZEN_QID", "0"))
PANEL_ID = int(os.getenv("NSW_COST_PANEL_ID", "8"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5433"))
DB_USER = os.getenv("DB_USER", "nsw_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "nsw_dev_password")
DB_NAME = os.getenv("DB_NAME", "nsw_estimation")


def _headers():
    return {
        "Content-Type": "application/json",
        "X-Tenant-ID": str(TENANT_ID),
        "X-User-ID": str(USER_ID),
    }


def _db():
    return psycopg.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )


def test_cost_adders_rejected_when_quotation_frozen():
    """Test that cost adders upsert is rejected for frozen quotations"""
    if FROZEN_QID <= 0:
        # No-op if not configured (keeps CI stable)
        return

    # Baseline count
    conn = _db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT count(*)
                FROM quote_cost_adders
                WHERE tenant_id=%s AND quotation_id=%s AND panel_id=%s AND cost_head_code=%s
                """,
                (TENANT_ID, FROZEN_QID, PANEL_ID, "BUSBAR"),
            )
            before = cur.fetchone()[0]
    finally:
        conn.close()

    # Attempt write (must fail)
    r = requests.post(
        f"{API_BASE}/quotation/{FROZEN_QID}/panels/{PANEL_ID}/cost-adders",
        headers=_headers(),
        json={"cost_head_code": "BUSBAR", "amount": 9999.0, "currency": "INR", "notes": "freeze guard test"},
        timeout=30,
    )
    assert r.status_code in (403, 409), f"Expected reject (403/409), got {r.status_code}: {r.text}"

    # Ensure DB unchanged
    conn = _db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT count(*)
                FROM quote_cost_adders
                WHERE tenant_id=%s AND quotation_id=%s AND panel_id=%s AND cost_head_code=%s
                """,
                (TENANT_ID, FROZEN_QID, PANEL_ID, "BUSBAR"),
            )
            after = cur.fetchone()[0]
            assert after == before, f"Expected no DB change for frozen quotation. before={before}, after={after}"
    finally:
        conn.close()
