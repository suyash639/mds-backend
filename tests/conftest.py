import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URL, DB_NAME

@pytest.fixture
async def test_db():
    """Create test database"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[f"{DB_NAME}_test"]
    yield db
    
    # Cleanup
    await client.drop_database(f"{DB_NAME}_test")
    client.close()

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
