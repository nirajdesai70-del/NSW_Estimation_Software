"""
BOM (Bill of Materials) endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/explode")
async def explode_bom():
    """BOM explosion (L1 → L2, multi-SKU → multi-line-items) (to be implemented)"""
    return {"message": "BOM explode endpoint - to be implemented"}


@router.get("/{bom_id}")
async def get_bom(bom_id: int):
    """Get BOM by ID (to be implemented)"""
    return {"message": f"Get BOM {bom_id} endpoint - to be implemented"}


