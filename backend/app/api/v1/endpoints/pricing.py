"""
Pricing endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/import")
async def import_prices():
    """Import catalog prices (to be implemented)"""
    return {"message": "Import prices endpoint - to be implemented"}


@router.get("/rules")
async def list_price_rules():
    """List price rules (to be implemented)"""
    return {"message": "List price rules endpoint - to be implemented"}

