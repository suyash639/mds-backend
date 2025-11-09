from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.models import Category, CategoryBase
from app.services.category_service import CategoryService
from bson import ObjectId

router = APIRouter()

async def get_category_service(request) -> CategoryService:
    db = request.app.db
    return CategoryService(db)

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryBase,
    service: CategoryService = Depends(get_category_service)
):
    """Create a new category"""
    try:
        result = await service.create_category(category.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[Category])
async def list_categories(
    service: CategoryService = Depends(get_category_service)
):
    """List all categories"""
    try:
        return await service.list_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: str,
    service: CategoryService = Depends(get_category_service)
):
    """Get a category by ID"""
    try:
        if not ObjectId.is_valid(category_id):
            raise HTTPException(status_code=400, detail="Invalid category ID")
        
        category = await service.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: str,
    category_update: CategoryBase,
    service: CategoryService = Depends(get_category_service)
):
    """Update a category"""
    try:
        if not ObjectId.is_valid(category_id):
            raise HTTPException(status_code=400, detail="Invalid category ID")
        
        updated = await service.update_category(category_id, category_update.dict())
        if not updated:
            raise HTTPException(status_code=404, detail="Category not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    service: CategoryService = Depends(get_category_service)
):
    """Delete a category"""
    try:
        if not ObjectId.is_valid(category_id):
            raise HTTPException(status_code=400, detail="Invalid category ID")
        
        success = await service.delete_category(category_id)
        if not success:
            raise HTTPException(status_code=404, detail="Category not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
