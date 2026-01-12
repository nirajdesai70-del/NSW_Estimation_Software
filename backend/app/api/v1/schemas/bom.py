"""
BOM (Bill of Materials) request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, List


class BomExplodeRequest(BaseModel):
    """Request schema for BOM explosion (L1 → L2)"""
    l1_intent_line_ids: List[int] = Field(..., min_length=1, description="List of L1 intent line IDs to explode")
    include_attributes: bool = Field(default=False, description="Include L1 attributes in response")
    include_sku: bool = Field(default=True, description="Include SKU details (code, name, uom)")
    aggregate_by_sku: bool = Field(default=True, description="Aggregate multiple L1 lines mapping to same SKU")


class BomExplodeResponse(BaseModel):
    """Response schema for BOM explosion"""
    tenant_id: int
    input: Dict[str, Any]
    summary: Dict[str, Any]
    unmapped: List[Dict[str, Any]]
    items: List[Dict[str, Any]]
    warnings: List[str]

