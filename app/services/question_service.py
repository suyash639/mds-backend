from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models import Question, QuestionListResponse
from app.idempotency import IdempotencyService
from app.events import EventService, EventType
import logging

logger = logging.getLogger(__name__)

class QuestionService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "questions"
        self.idempotency_service = IdempotencyService(db)
        self.event_service = EventService(db)
    
    async def create_question(
        self,
        question_data: Dict[str, Any],
        idempotency_key: Optional[str] = None
    ) -> Question:
        """Create a new question in the database"""
        if idempotency_key:
            existing = await self.idempotency_service.check_idempotency(idempotency_key)
            if existing:
                return Question(**existing["response"])
        
        question_data["created_at"] = datetime.utcnow()
        question_data["updated_at"] = datetime.utcnow()
        
        result = await self.db[self.collection_name].insert_one(question_data)
        
        created_question = await self.db[self.collection_name].find_one(
            {"_id": result.inserted_id}
        )
        question = Question(**created_question)
        
        # Log event
        await self.event_service.log_event(
            EventType.QUESTION_CREATED,
            str(result.inserted_id),
            "Question"
        )
        
        # Store idempotency key
        if idempotency_key:
            await self.idempotency_service.store_idempotency(
                idempotency_key,
                question.dict(),
                201
            )
        
        return question
    
    async def get_question(self, question_id: str) -> Optional[Question]:
        """Get a question by ID"""
        question = await self.db[self.collection_name].find_one(
            {"_id": ObjectId(question_id)}
        )
        if question:
            return Question(**question)
        return None
    
    async def list_questions(
        self,
        page: int,
        page_size: int,
        filters: Optional[Dict[str, Any]] = None
    ) -> QuestionListResponse:
        """List questions with pagination and filtering"""
        filters = filters or {}
        
        total = await self.db[self.collection_name].count_documents(filters)
        
        skip = (page - 1) * page_size
        cursor = self.db[self.collection_name].find(filters).skip(skip).limit(page_size)
        questions = await cursor.to_list(length=page_size)
        
        items = [Question(**q) for q in questions]
        return QuestionListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=items
        )
    
    async def update_question(
        self,
        question_id: str,
        update_data: Dict[str, Any]
    ) -> Optional[Question]:
        """Update a question"""
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(question_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            # Log event
            await self.event_service.log_event(
                EventType.QUESTION_UPDATED,
                question_id,
                "Question",
                changes=update_data
            )
            return Question(**result)
        return None
    
    async def delete_question(self, question_id: str) -> bool:
        """Delete a question"""
        result = await self.db[self.collection_name].delete_one(
            {"_id": ObjectId(question_id)}
        )
        
        if result.deleted_count > 0:
            # Log event
            await self.event_service.log_event(
                EventType.QUESTION_DELETED,
                question_id,
                "Question"
            )
            return True
        return False
    
    async def count_by_category(self, category_id: str) -> int:
        """Count questions in a category"""
        count = await self.db[self.collection_name].count_documents(
            {"category_id": category_id}
        )
        return count
