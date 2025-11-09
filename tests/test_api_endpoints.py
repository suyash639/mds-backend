import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.json()

@pytest.mark.asyncio
async def test_create_question_endpoint(test_db):
    """Test question creation endpoint"""
    payload = {
        "text": "Test question",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "A",
        "options": ["A", "B", "C"],
        "metadata": {"difficulty": "easy"}
    }
    
    # This would require a test client with mocked db
    # Implementation depends on your test setup

@pytest.mark.asyncio
async def test_invalid_question_data(test_db):
    """Test validation of invalid question data"""
    # Invalid text
    payload = {
        "text": "",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "A"
    }
    
    # Test would validate the error response
