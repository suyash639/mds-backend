import pytest
from app.services.question_service import QuestionService
from app.services.category_service import CategoryService
from app.services.bulk_service import BulkService

@pytest.mark.asyncio
async def test_full_workflow(test_db):
    """Test complete workflow: create category, question, bulk operations"""
    category_service = CategoryService(test_db)
    question_service = QuestionService(test_db)
    bulk_service = BulkService(test_db)
    
    # Create category
    category = await category_service.create_category({
        "name": "Test Category",
        "description": "A test category"
    })
    assert category.name == "Test Category"
    
    # Create question
    question = await question_service.create_question({
        "text": "Test question",
        "category_id": str(category.id),
        "source_id": "src_1",
        "correct_answer": "A",
        "metadata": {"difficulty": "easy"}
    })
    assert question.text == "Test question"
    
    # Bulk export
    exported = await bulk_service.bulk_export({"category_id": str(category.id)})
    assert len(exported) >= 1
    assert exported[0]["text"] == "Test question"

@pytest.mark.asyncio
async def test_error_handling_in_workflow(test_db):
    """Test error handling in integrated workflow"""
    question_service = QuestionService(test_db)
    
    # Try to get non-existent question
    result = await question_service.get_question("000000000000000000000000")
    assert result is None
    
    # Try to delete non-existent question
    success = await question_service.delete_question("000000000000000000000000")
    assert success is False
