from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import MONGODB_URL, DB_NAME

class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(MONGODB_URL)
        cls.db = cls.client[DB_NAME]
        # Create indexes
        await cls._create_indexes()
        print("Database connected and indexes created")

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
        print("Database disconnected")

    @classmethod
    async def _create_indexes(cls):
        """Create database indexes for performance"""
        if cls.db:
            # Questions collection indexes
            questions = cls.db["questions"]
            await questions.create_index("category_id")
            await questions.create_index("source_id")
            await questions.create_index([("metadata.difficulty", 1)])
            await questions.create_index([("created_at", -1)])
            
            # Idempotency key index
            idempotency = cls.db["idempotency_keys"]
            await idempotency.create_index("idempotency_key", unique=True)
            await idempotency.create_index("created_at", expireAfterSeconds=3600)
            
            # Events collection index
            events = cls.db["events"]
            await events.create_index([("created_at", -1)])
            await events.create_index("entity_id")
            
            print("Indexes created successfully")
