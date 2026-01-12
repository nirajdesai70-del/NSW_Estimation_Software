"""
Authentication endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login():
    """Login endpoint (to be implemented)"""
    return {"message": "Login endpoint - to be implemented"}


@router.post("/refresh")
async def refresh_token():
    """Refresh token endpoint (to be implemented)"""
    return {"message": "Refresh token endpoint - to be implemented"}


@router.get("/me")
async def get_current_user():
    """Get current user endpoint (to be implemented)"""
    return {"message": "Get current user endpoint - to be implemented"}


