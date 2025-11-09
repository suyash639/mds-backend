from fastapi import APIRouter, Depends, HTTPException, Query
from app.events import EventService
from typing import Optional

router = APIRouter()

async def get_event_service(request) -> EventService:
    db = request.app.db
    return EventService(db)

@router.get("/")
async def list_events(
    entity_id: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    service: EventService = Depends(get_event_service)
):
    """Get audit trail events"""
    try:
        events = await service.get_events(entity_id, entity_type, limit)
        return {"total": len(events), "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
