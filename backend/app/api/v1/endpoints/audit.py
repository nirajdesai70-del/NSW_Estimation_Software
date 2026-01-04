"""
Audit endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/events")
async def list_audit_events():
    """List audit events (to be implemented)"""
    return {"message": "List audit events endpoint - to be implemented"}


@router.get("/changes/{entity_type}/{entity_id}")
async def get_change_log(entity_type: str, entity_id: int):
    """Get change log for an entity (to be implemented)"""
    return {
        "message": f"Get change log for {entity_type} {entity_id} endpoint - to be implemented"
    }

