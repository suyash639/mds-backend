from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
import hashlib
from typing import Optional, Dict, Any

class IdempotencyService:
    """Handles idempotent requests to ensure safe retries"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "idempotency_keys"
    
    async def check_idempotency(self, idempotency_key: str) -> Optional[Dict[str, Any]]:
        """Check if request was already processed"""
        result = await self.db[self.collection_name].find_one(
            {"idempotency_key": idempotency_key}
        )
        return result
    
    async def store_idempotency(
        self,
        idempotency_key: str,
        response_data: Dict[str, Any],
        status_code: int = 201
    ) -> None:
        """Store idempotency key with response"""
        await self.db[self.collection_name].insert_one({
            "idempotency_key": idempotency_key,
            "response": response_data,
            "status_code": status_code,
            "created_at": datetime.utcnow()
        })
    
    async def generate_key(self, data: str) -> str:
        """Generate idempotency key from request data"""
        return hashlib.sha256(data.encode()).hexdigest()
