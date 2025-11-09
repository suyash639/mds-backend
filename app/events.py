from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import json

class EventType(str, Enum):
    QUESTION_CREATED = "question.created"
    QUESTION_UPDATED = "question.updated"
    QUESTION_DELETED = "question.deleted"
    BULK_IMPORT = "bulk.import"
    BULK_EXPORT = "bulk.export"

class EventService:
    """Handles event logging for audit trail and webhooks"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "events"
    
    async def log_event(
        self,
        event_type: EventType,
        entity_id: str,
        entity_type: str,
        changes: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> None:
        """Log an event to the database"""
        event = {
            "event_type": event_type.value,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "changes": changes or {},
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }
        await self.db[self.collection_name].insert_one(event)
    
    async def get_events(
        self,
        entity_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        limit: int = 100
    ) -> list:
        """Retrieve events for audit trail"""
        filters = {}
        if entity_id:
            filters["entity_id"] = entity_id
        if entity_type:
            filters["entity_type"] = entity_type
        
        cursor = self.db[self.collection_name].find(filters).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)
