"""
Cost Summary Service (QCA only)

Week-3 Day-2: Read-only summary service.
Rules:
- One line per cost head (no breakup)
- No QCD access
- No pricing recompute
Week-4 Day-3: Adds render helper fields (panel_count, has_catalog_bindings, cost_head_codes)
"""
from typing import Dict, Any, Set, List
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.cost_integrity_service import CostIntegrityService

ALLOWED_COST_HEADS = {
    "FABRICATION",
    "BUSBAR",
    "LABOUR",
    "TRANSPORTATION",
    "ERECTION",
    "COMMISSIONING",
}


class CostSummaryService:
    def __init__(self, db: Session, *, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id

    def get_cost_summary(self, *, quotation_id: int) -> Dict[str, Any]:
        """
        Get read-only cost summary for a quotation.
        
        Returns one line per cost head per panel (summary-only, no breakup).
        Only reads from quote_cost_adders (QCA), never touches QCD tables.
        Week-4 Day-1: Also includes quotation state visibility.
        
        Args:
            quotation_id: Quotation ID
            
        Returns:
            Dict with quotation_id, panels list, quotation_state, and state_timestamp
        """
        # Week-4 Day-1: Read quotation state (read-only)
        quote_row = self.db.execute(
            text("""
                SELECT status, updated_at
                FROM quotations
                WHERE tenant_id=:tenant_id AND id=:qid
            """),
            {"tenant_id": self.tenant_id, "qid": quotation_id},
        ).mappings().first()
        
        if not quote_row:
            raise ValueError(f"Quotation {quotation_id} not found for tenant")
        
        # Map status to quotation_state (Week-4 Day-1: DRAFT/FROZEN/ISSUED/ARCHIVED)
        # Strict mapping with fallback to avoid unexpected DB values leaking
        status = (quote_row.get("status") or "DRAFT").upper()
        STATE_MAP = {
            "DRAFT": "DRAFT",
            "FROZEN": "FROZEN",
            "ISSUED": "ISSUED",
            "ARCHIVED": "ARCHIVED",
        }
        quotation_state = STATE_MAP.get(status, "DRAFT")  # Fallback to DRAFT for unknown values
        
        # Use updated_at as state_timestamp (Week-4 Day-1)
        state_ts = quote_row.get("updated_at")
        state_timestamp = state_ts.isoformat() if state_ts and hasattr(state_ts, "isoformat") else None
        
        # Week-3 Day-2: Read cost adders (QCA only)
        rows = self.db.execute(
            text("""
                SELECT panel_id, cost_head_code, amount, currency
                FROM quote_cost_adders
                WHERE tenant_id=:tenant_id AND quotation_id=:qid
                ORDER BY panel_id, cost_head_code
            """),
            {"tenant_id": self.tenant_id, "qid": quotation_id},
        ).mappings().all()

        panels: Dict[int, Dict[str, Any]] = {}
        codes_present: Set[str] = set()

        for r in rows:
            pid = int(r["panel_id"])
            code = str(r["cost_head_code"])

            if code not in ALLOWED_COST_HEADS:
                # Safety: ignore unknown codes rather than breaking summary
                continue

            codes_present.add(code)

            if pid not in panels:
                panels[pid] = {
                    "panel_id": pid,
                    "currency": r.get("currency") or "INR",
                    "cost_heads": {},
                }

            panels[pid]["cost_heads"][code] = float(r.get("amount") or 0)

        # Week-4 Day-2: Integrity (read-only)
        integrity = CostIntegrityService(self.db, tenant_id=self.tenant_id).compute(
            quotation_id=quotation_id,
            quotation_state=quotation_state,
            state_timestamp=state_timestamp,
        )

        # Week-4 Day-3: Render helpers (read-only, no breakup)
        panel_list: List[Dict[str, Any]] = list(panels.values())
        panel_count = len(panel_list)

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
        has_catalog_bindings = bind_cnt > 0

        cost_head_codes = sorted(list(codes_present))

        # Fabrication special rule (Week-0 lock): summary-only, no breakup.
        # Here we keep FABRICATION as a single number (no splits returned).
        return {
            "quotation_id": quotation_id,
            "panels": panel_list,
            # Week-4 Day-1
            "quotation_state": quotation_state,
            "state_timestamp": state_timestamp,
            # Week-4 Day-2
            "integrity_status": integrity["integrity_status"],
            "integrity_hash": integrity["integrity_hash"],
            "integrity_reasons": integrity["integrity_reasons"],
            # Week-4 Day-3
            "panel_count": panel_count,
            "has_catalog_bindings": has_catalog_bindings,
            "cost_head_codes": cost_head_codes,
        }
