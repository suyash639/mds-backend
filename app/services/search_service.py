from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Any, Optional, List
from app.utils import PaginationHelper

class SearchService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "questions"
    
    async def text_search(
        self,
        query: str,
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        """Perform text search"""
        page, page_size = PaginationHelper.validate_pagination(page, page_size)
        skip = PaginationHelper.calculate_skip(page, page_size)
        
        filters = {
            "$or": [
                {"text": {"$regex": query, "$options": "i"}},
                {"explanation": {"$regex": query, "$options": "i"}},
                {"metadata.tags": {"$regex": query, "$options": "i"}}
            ]
        }
        
        total = await self.db[self.collection_name].count_documents(filters)
        cursor = self.db[self.collection_name].find(filters).skip(skip).limit(page_size)
        items = await cursor.to_list(length=page_size)
        
        # Convert ObjectId to string
        for item in items:
            item["_id"] = str(item["_id"])
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
    
    async def advanced_search(
        self,
        filters: Dict[str, Any],
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        """Perform advanced search with multiple filters"""
        page, page_size = PaginationHelper.validate_pagination(page, page_size)
        skip = PaginationHelper.calculate_skip(page, page_size)
        
        total = await self.db[self.collection_name].count_documents(filters)
        cursor = self.db[self.collection_name].find(filters).skip(skip).limit(page_size)
        items = await cursor.to_list(length=page_size)
        
        # Convert ObjectId to string
        for item in items:
            item["_id"] = str(item["_id"])
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
    
    async def search_by_difficulty(
        self,
        difficulty: str,
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        """Search questions by difficulty level"""
        page, page_size = PaginationHelper.validate_pagination(page, page_size)
        skip = PaginationHelper.calculate_skip(page, page_size)
        
        filters = {"metadata.difficulty": difficulty}
        
        total = await self.db[self.collection_name].count_documents(filters)
        cursor = self.db[self.collection_name].find(filters).skip(skip).limit(page_size)
        items = await cursor.to_list(length=page_size)
        
        # Convert ObjectId to string
        for item in items:
            item["_id"] = str(item["_id"])
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        total_questions = await self.db[self.collection_name].count_documents({})
        
        # Group by difficulty
        difficulty_pipeline = [
            {"$group": {"_id": "$metadata.difficulty", "count": {"$sum": 1}}}
        ]
        difficulty_stats = await self.db[self.collection_name].aggregate(difficulty_pipeline).to_list(None)
        
        # Group by category
        category_pipeline = [
            {"$group": {"_id": "$category_id", "count": {"$sum": 1}}}
        ]
        category_stats = await self.db[self.collection_name].aggregate(category_pipeline).to_list(None)
        
        # Group by source
        source_pipeline = [
            {"$group": {"_id": "$source_id", "count": {"$sum": 1}}}
        ]
        source_stats = await self.db[self.collection_name].aggregate(source_pipeline).to_list(None)
        
        return {
            "total_questions": total_questions,
            "by_difficulty": {item["_id"]: item["count"] for item in difficulty_stats},
            "by_category": {item["_id"]: item["count"] for item in category_stats},
            "by_source": {item["_id"]: item["count"] for item in source_stats}
        }
