import pytest
from app.services.question_service import QuestionService
from app.models import QuestionCreate, Question
from datetime import datetime

@pytest.mark.asyncio
async def test_create_question(test_db):
    """Test creating a question"""
    service = QuestionService(test_db)
    
    question_data = {
        "text": "What is 2+2?",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "4",
        "options": ["3", "4", "5"],
        "metadata": {"difficulty": "easy"}
    }
    
    result = await service.create_question(question_data)
    
    assert result.text == "What is 2+2?"
    assert result.correct_answer == "4"
    assert result.id is not None

@pytest.mark.asyncio
async def test_get_question(test_db):
    """Test retrieving a question"""
    service = QuestionService(test_db)
    
    # Create
    question_data = {
        "text": "Test question",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "A",
        "metadata": {"difficulty": "medium"}
    }
    created = await service.create_question(question_data)
    
    # Retrieve
    retrieved = await service.get_question(str(created.id))
    
    assert retrieved is not None
    assert retrieved.text == "Test question"

@pytest.mark.asyncio
async def test_update_question(test_db):
    """Test updating a question"""
    service = QuestionService(test_db)
    
    # Create
    question_data = {
        "text": "Original text",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "A",
        "metadata": {"difficulty": "easy"}
    }
    created = await service.create_question(question_data)
    
    # Update
    update_data = {"text": "Updated text"}
    updated = await service.update_question(str(created.id), update_data)
    
    assert updated.text == "Updated text"

@pytest.mark.asyncio
async def test_delete_question(test_db):
    """Test deleting a question"""
    service = QuestionService(test_db)
    
    # Create
    question_data = {
        "text": "To be deleted",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "A",
        "metadata": {"difficulty": "hard"}
    }
    created = await service.create_question(question_data)
    
    # Delete
    success = await service.delete_question(str(created.id))
    assert success is True
    
    # Verify deletion
    retrieved = await service.get_question(str(created.id))
    assert retrieved is None

@pytest.mark.asyncio
async def test_list_questions(test_db):
    """Test listing questions with pagination"""
    service = QuestionService(test_db)
    
    # Create multiple questions
    for i in range(5):
        await service.create_question({
            "text": f"Question {i}",
            "category_id": "cat_1",
            "source_id": "src_1",
            "correct_answer": "A",
            "metadata": {"difficulty": "easy"}
        })
    
    # List with pagination
    result = await service.list_questions(1, 3)
    
    assert result.total == 5
    assert len(result.items) == 3
    assert result.page == 1
    assert result.page_size == 3
