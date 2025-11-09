from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models import Question, QuestionCreate
from app.events import EventService, EventType

class BulkService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "questions"
        self.event_service = EventService(db)
    
    async def bulk_import(self, questions_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk import questions"""
        imported = 0
        failed = 0
        errors = []
        
        for idx, question_data in enumerate(questions_data):
            try:
                question_data["created_at"] = datetime.utcnow()
                question_data["updated_at"] = datetime.utcnow()
                
                result = await self.db[self.collection_name].insert_one(question_data)
                await self.event_service.log_event(
                    EventType.BULK_IMPORT,
                    str(result.inserted_id),
                    "Question"
                )
                imported += 1
            except Exception as e:
                failed += 1
                errors.append({"row": idx, "error": str(e)})
        
        return {"imported": imported, "failed": failed, "errors": errors}
    
    async def bulk_export(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Bulk export questions"""
        filters = filters or {}
        cursor = self.db[self.collection_name].find(filters)
        questions = await cursor.to_list(length=None)
        
        # Convert ObjectId to string
        for q in questions:
            q["_id"] = str(q["_id"])
        
        return questions
    
    async def bulk_update(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk update questions"""
        updated = 0
        failed = 0
        errors = []
        
        for idx, update in enumerate(updates):
            try:
                question_id = update.pop("id")
                update["updated_at"] = datetime.utcnow()
                
                result = await self.db[self.collection_name].find_one_and_update(
                    {"_id": ObjectId(question_id)},
                    {"$set": update},
                    return_document=True
                )
                
                if result:
                    await self.event_service.log_event(
                        EventType.QUESTION_UPDATED,
                        question_id,
                        "Question",
                        changes=update
                    )
                    updated += 1
                else:
                    failed += 1
                    errors.append({"row": idx, "error": "Question not found"})
            except Exception as e:
                failed += 1
                errors.append({"row": idx, "error": str(e)})
        
        return {"updated": updated, "failed": failed, "errors": errors}
    
    async def bulk_delete(self, question_ids: List[str]) -> Dict[str, Any]:
        """Bulk delete questions"""
        deleted = 0
        failed = 0
        
        for question_id in question_ids:
            try:
                result = await self.db[self.collection_name].delete_one(
                    {"_id": ObjectId(question_id)}
                )
                
                if result.deleted_count > 0:
                    await self.event_service.log_event(
                        EventType.QUESTION_DELETED,
                        question_id,
                        "Question"
                    )
                    deleted += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        
        return {"deleted": deleted, "failed": failed}
