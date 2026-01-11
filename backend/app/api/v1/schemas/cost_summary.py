"""
Cost Summary API Schemas (QCA summary)

Week-3 Day-2: Read-only cost summary per quotation/panel
Week-4 Day-1: Added quotation state visibility
Week-4 Day-2: Added integrity fields
Week-4 Day-3: Added read-only render helper fields (no breakup)
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class PanelCostSummary(BaseModel):
    panel_id: int
    currency: str = "INR"
    cost_heads: Dict[str, float]


class QuotationCostSummaryResponse(BaseModel):
    quotation_id: int
    panels: List[PanelCostSummary]
    
    # Week-4 Day-1
    quotation_state: str  # DRAFT/FROZEN/ISSUED/ARCHIVED
    state_timestamp: Optional[str] = None  # ISO timestamp
    
    # Week-4 Day-2 (read-only integrity)
    integrity_status: str = "OK"  # OK / DRIFT
    integrity_hash: Optional[str] = None  # sha256 hex
    integrity_reasons: List[str] = Field(default_factory=list)  # Fixed mutable default
    
    # Week-4 Day-3 (render helpers; still summary-only)
    panel_count: int = 0
    has_catalog_bindings: bool = False
    cost_head_codes: List[str] = Field(default_factory=list)  # sorted unique codes present
