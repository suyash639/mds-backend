from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.services.search_service import SearchService
from app.utils import SearchFilters

router = APIRouter()

async def get_search_service(request) -> SearchService:
    db = request.app.db
    return SearchService(db)

@router.get("/text-search")
async def text_search(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: SearchService = Depends(get_search_service)
):
    """Full-text search across questions"""
    try:
        result = await service.text_search(q, page, page_size)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search failed")

@router.get("/advanced")
async def advanced_search(
    text: Optional[str] = None,
    category_id: Optional[str] = None,
    source_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: SearchService = Depends(get_search_service)
):
    """Advanced search with multiple filters"""
    try:
        filters = {}
        
        if text:
            filters.update(SearchFilters.build_text_search(text))
        if category_id:
            filters["category_id"] = category_id
        if source_id:
            filters["source_id"] = source_id
        if difficulty:
            filters.update(SearchFilters.build_difficulty_filter(difficulty))
        if tags:
            filters.update(SearchFilters.build_tag_filter(tags))
        if start_date and end_date:
            filters.update(SearchFilters.build_date_range_filter(start_date, end_date))
        
        result = await service.advanced_search(filters, page, page_size)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search failed")

@router.get("/by-difficulty")
async def get_by_difficulty(
    difficulty: str = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: SearchService = Depends(get_search_service)
):
    """Get questions filtered by difficulty"""
    try:
        result = await service.search_by_difficulty(difficulty, page, page_size)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search failed")

@router.get("/statistics")
async def get_statistics(
    service: SearchService = Depends(get_search_service)
):
    """Get statistics about questions in database"""
    try:
        stats = await service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get statistics")
