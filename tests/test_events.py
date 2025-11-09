import pytest
from app.events import EventService, EventType

@pytest.mark.asyncio
async def test_log_event(test_db):
    """Test event logging"""
    service = EventService(test_db)
    
    await service.log_event(
        EventType.QUESTION_CREATED,
        "123",
        "Question",
        {"text": "New question"}
    )
    
    events = await service.get_events(entity_id="123")
    
    assert len(events) == 1
    assert events[0]["event_type"] == "question.created"

@pytest.mark.asyncio
async def test_get_events_filtered(test_db):
    """Test retrieving filtered events"""
    service = EventService(test_db)
    
    # Log multiple events
    await service.log_event(EventType.QUESTION_CREATED, "q1", "Question")
    await service.log_event(EventType.QUESTION_UPDATED, "q2", "Question")
    
    # Get specific events
    events = await service.get_events(entity_id="q1")
    
    assert len(events) == 1
    assert events[0]["entity_id"] == "q1"
