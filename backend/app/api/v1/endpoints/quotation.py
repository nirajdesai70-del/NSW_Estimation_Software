"""
Quotation endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_quotations():
    """List quotations (to be implemented)"""
    return {"message": "List quotations endpoint - to be implemented"}


@router.post("/")
async def create_quotation():
    """Create quotation (to be implemented)"""
    return {"message": "Create quotation endpoint - to be implemented"}


@router.get("/{quotation_id}")
async def get_quotation(quotation_id: int):
    """Get quotation by ID (to be implemented)"""
    return {"message": f"Get quotation {quotation_id} endpoint - to be implemented"}


@router.post("/{quotation_id}/revisions")
async def create_revision(quotation_id: int):
    """Create quotation revision (to be implemented)"""
    return {"message": f"Create revision for quotation {quotation_id} endpoint - to be implemented"}

