from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any, Optional, List
from app.models import Category

class CategoryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "categories"
    
    async def create_category(self, category_data: Dict[str, Any]) -> Category:
        category_data["created_at"] = datetime.utcnow()
        category_data["updated_at"] = datetime.utcnow()
        
        result = await self.db[self.collection_name].insert_one(category_data)
        created = await self.db[self.collection_name].find_one({"_id": result.inserted_id})
        return Category(**created)
    
    async def get_category(self, category_id: str) -> Optional[Category]:
        category = await self.db[self.collection_name].find_one({"_id": ObjectId(category_id)})
        return Category(**category) if category else None
    
    async def list_categories(self) -> List[Category]:
        cursor = self.db[self.collection_name].find({})
        categories = await cursor.to_list(length=None)
        return [Category(**c) for c in categories]
    
    async def update_category(
        self,
        category_id: str,
        update_data: Dict[str, Any]
    ) -> Optional[Category]:
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(category_id)},
            {"$set": update_data},
            return_document=True
        )
        return Category(**result) if result else None
    
    async def delete_category(self, category_id: str) -> bool:
        result = await self.db[self.collection_name].delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count > 0
