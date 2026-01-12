"""
Cost Integrity Service (Phase-6)

Week-4 Day-2: Drift detection and integrity hash (read-only)
Rules:
- Must not modify DB
- Must not expose costing breakup
- Must not recompute pricing
- Must not touch QCD tables
"""
from __future__ import annotations
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import text
import hashlib

# Keep aligned with CostSummaryService allowed cost heads
ALLOWED_COST_HEADS = {
    "FABRICATION",
    "BUSBAR",
    "LABOUR",
    "TRANSPORTATION",
    "ERECTION",
    "COMMISSIONING",
}

INTEGRITY_OK = "OK"
INTEGRITY_DRIFT = "DRIFT"


class CostIntegrityService:
    def __init__(self, db: Session, *, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def compute(
        self, *, quotation_id: int, quotation_state: str, state_timestamp: str | None
    ) -> Dict[str, Any]:
        """
        Compute integrity status, hash, and drift reasons (read-only).
        
        Args:
            quotation_id: Quotation ID
            quotation_state: Quotation state (DRAFT/FROZEN/ISSUED/ARCHIVED)
            state_timestamp: State timestamp (ISO format or None)
            
        Returns:
            Dict with integrity_status, integrity_hash, integrity_reasons
        """
        reasons: List[str] = []

        # ---- QCA read: quote_cost_adders only ----
        rows = self.db.execute(
            text(
                """
                SELECT panel_id, cost_head_code, amount, currency
                FROM quote_cost_adders
                WHERE tenant_id=:tenant_id AND quotation_id=:qid
                ORDER BY panel_id, cost_head_code
                """
            ),
            {"tenant_id": self.tenant_id, "qid": quotation_id},
        ).mappings().all()

        # Detect unknown cost heads present in DB (should not leak; we only flag)
        for r in rows:
            code = str(r.get("cost_head_code") or "")
            if code and code not in ALLOWED_COST_HEADS:
                reasons.append("UNKNOWN_COST_HEAD")
                break

        # Duplicate-group check (should be prevented by unique constraint, but we verify)
        dups = self.db.execute(
            text(
                """
                SELECT panel_id, cost_head_code, count(*) AS c
                FROM quote_cost_adders
                WHERE tenant_id=:tenant_id AND quotation_id=:qid
                GROUP BY panel_id, cost_head_code
                HAVING count(*) > 1
                """
            ),
            {"tenant_id": self.tenant_id, "qid": quotation_id},
        ).mappings().all()

        if dups:
            reasons.append("QCA_DUPLICATE_GROUP")

        # Optional: include catalog binding presence in hash only (no new exposure)
        # (DB-only read; does not touch QCD tables.)
        bind_cnt_row = self.db.execute(
            text(
                """
                SELECT count(*) AS c
                FROM quote_bom_items
                WHERE tenant_id=:tenant_id
                  AND quotation_id=:qid
                  AND (metadata_json ? 'catalog_sku_id')
                """
            ),
            {"tenant_id": self.tenant_id, "qid": quotation_id},
        ).mappings().first()
        bind_cnt = int(bind_cnt_row["c"]) if bind_cnt_row and bind_cnt_row.get("c") is not None else 0

        integrity_status = INTEGRITY_OK if not reasons else INTEGRITY_DRIFT

        # Build stable digest payload (deterministic order already enforced by ORDER BY)
        digest = self._sha256_digest(
            quotation_id=quotation_id,
            quotation_state=quotation_state,
            state_timestamp=state_timestamp,
            bind_cnt=bind_cnt,
            qca_rows=rows,
        )

        # De-dup reasons for clean output
        reasons = sorted(list(set(reasons)))

        return {
            "integrity_status": integrity_status,
            "integrity_hash": digest,
            "integrity_reasons": reasons,
        }

    def _sha256_digest(
        self,
        *,
        quotation_id: int,
        quotation_state: str,
        state_timestamp: str | None,
        bind_cnt: int,
        qca_rows: List[Dict[str, Any]],
    ) -> str:
        """Generate stable SHA256 hash for integrity checking"""
        parts: List[str] = []
        parts.append(f"tenant_id={self.tenant_id}")
        parts.append(f"quotation_id={quotation_id}")
        parts.append(f"quotation_state={quotation_state or ''}")
        parts.append(f"state_timestamp={state_timestamp or ''}")
        parts.append(f"catalog_bind_cnt={bind_cnt}")

        for r in qca_rows:
            panel_id = int(r.get("panel_id") or 0)
            code = str(r.get("cost_head_code") or "")
            amt = float(r.get("amount") or 0.0)
            cur = str(r.get("currency") or "")
            parts.append(f"qca|{panel_id}|{code}|{amt:.6f}|{cur}")

        payload = "\n".join(parts).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
