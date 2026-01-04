"""
API v1 Router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, catalog, bom, pricing, quotation, audit, discounts, tax

api_router = APIRouter()

# Register all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
api_router.include_router(bom.router, prefix="/bom", tags=["bom"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(quotation.router, prefix="/quotation", tags=["quotation"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(discounts.router, prefix="", tags=["discounts"])  # No prefix, routes are already full paths
api_router.include_router(tax.router, prefix="", tags=["tax"])  # No prefix, routes are already full paths


