import pytest
from app.idempotency import IdempotencyService

@pytest.mark.asyncio
async def test_store_and_check_idempotency(test_db):
    """Test idempotency storage and retrieval"""
    service = IdempotencyService(test_db)
    
    key = "test-key-123"
    response_data = {"id": "123", "text": "Test question"}
    
    # Store
    await service.store_idempotency(key, response_data, 201)
    
    # Check
    result = await service.check_idempotency(key)
    
    assert result is not None
    assert result["response"] == response_data
    assert result["status_code"] == 201

@pytest.mark.asyncio
async def test_generate_idempotency_key(test_db):
    """Test idempotency key generation"""
    service = IdempotencyService(test_db)
    
    data = '{"text": "Question", "answer": "A"}'
    key = await service.generate_key(data)
    
    assert isinstance(key, str)
    assert len(key) > 0
