from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any, Optional, List
from app.models import Source

class SourceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "sources"
    
    async def create_source(self, source_data: Dict[str, Any]) -> Source:
        source_data["created_at"] = datetime.utcnow()
        source_data["updated_at"] = datetime.utcnow()
        
        result = await self.db[self.collection_name].insert_one(source_data)
        created = await self.db[self.collection_name].find_one({"_id": result.inserted_id})
        return Source(**created)
    
    async def get_source(self, source_id: str) -> Optional[Source]:
        source = await self.db[self.collection_name].find_one({"_id": ObjectId(source_id)})
        return Source(**source) if source else None
    
    async def list_sources(self) -> List[Source]:
        cursor = self.db[self.collection_name].find({})
        sources = await cursor.to_list(length=None)
        return [Source(**s) for s in sources]
    
    async def update_source(
        self,
        source_id: str,
        update_data: Dict[str, Any]
    ) -> Optional[Source]:
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(source_id)},
            {"$set": update_data},
            return_document=True
        )
        return Source(**result) if result else None
    
    async def delete_source(self, source_id: str) -> bool:
        result = await self.db[self.collection_name].delete_one({"_id": ObjectId(source_id)})
        return result.deleted_count > 0
