import pytest
from app.services.bulk_service import BulkService

@pytest.mark.asyncio
async def test_bulk_import(test_db):
    """Test bulk importing questions"""
    service = BulkService(test_db)
    
    questions = [
        {
            "text": "Q1",
            "category_id": "cat_1",
            "source_id": "src_1",
            "correct_answer": "A",
            "metadata": {"difficulty": "easy"}
        },
        {
            "text": "Q2",
            "category_id": "cat_1",
            "source_id": "src_1",
            "correct_answer": "B",
            "metadata": {"difficulty": "medium"}
        }
    ]
    
    result = await service.bulk_import(questions)
    
    assert result["imported"] == 2
    assert result["failed"] == 0

@pytest.mark.asyncio
async def test_bulk_export(test_db):
    """Test bulk exporting questions"""
    service = BulkService(test_db)
    
    # Import first
    questions = [
        {
            "text": "Export test",
            "category_id": "cat_1",
            "source_id": "src_1",
            "correct_answer": "A",
            "metadata": {"difficulty": "easy"}
        }
    ]
    await service.bulk_import(questions)
    
    # Export
    data = await service.bulk_export({"category_id": "cat_1"})
    
    assert len(data) >= 1
