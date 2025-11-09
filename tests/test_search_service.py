import pytest
from app.services.search_service import SearchService

@pytest.mark.asyncio
async def test_text_search(test_db):
    """Test text search functionality"""
    service = SearchService(test_db)
    
    # Create test data
    await test_db["questions"].insert_one({
        "text": "What is photosynthesis?",
        "category_id": "bio_1",
        "source_id": "src_1",
        "correct_answer": "A",
        "metadata": {"difficulty": "medium", "tags": ["biology"]}
    })
    
    # Search
    result = await service.text_search("photosynthesis", 1, 10)
    
    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["text"] == "What is photosynthesis?"

@pytest.mark.asyncio
async def test_search_by_difficulty(test_db):
    """Test difficulty filter"""
    service = SearchService(test_db)
    
    # Create test data
    for i in range(3):
        await test_db["questions"].insert_one({
            "text": f"Question {i}",
            "category_id": "cat_1",
            "source_id": "src_1",
            "correct_answer": "A",
            "metadata": {"difficulty": "easy" if i < 2 else "hard"}
        })
    
    # Search
    result = await service.search_by_difficulty("easy", 1, 10)
    
    assert result["total"] >= 2

@pytest.mark.asyncio
async def test_get_statistics(test_db):
    """Test statistics generation"""
    service = SearchService(test_db)
    
    # Create test data
    await test_db["questions"].insert_many([
        {"text": "Q1", "category_id": "cat_1", "source_id": "src_1", "correct_answer": "A", "metadata": {"difficulty": "easy"}},
        {"text": "Q2", "category_id": "cat_2", "source_id": "src_1", "correct_answer": "B", "metadata": {"difficulty": "hard"}},
    ])
    
    # Get stats
    stats = await service.get_statistics()
    
    assert stats["total_questions"] == 2
    assert "by_difficulty" in stats
    assert "by_category" in stats
