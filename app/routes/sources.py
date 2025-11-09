from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.models import Source, SourceBase
from app.services.source_service import SourceService
from bson import ObjectId

router = APIRouter()

async def get_source_service(request) -> SourceService:
    db = request.app.db
    return SourceService(db)

@router.post("/", response_model=Source, status_code=status.HTTP_201_CREATED)
async def create_source(
    source: SourceBase,
    service: SourceService = Depends(get_source_service)
):
    """Create a new source"""
    try:
        result = await service.create_source(source.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[Source])
async def list_sources(
    service: SourceService = Depends(get_source_service)
):
    """List all sources"""
    try:
        return await service.list_sources()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{source_id}", response_model=Source)
async def get_source(
    source_id: str,
    service: SourceService = Depends(get_source_service)
):
    """Get a source by ID"""
    try:
        if not ObjectId.is_valid(source_id):
            raise HTTPException(status_code=400, detail="Invalid source ID")
        
        source = await service.get_source(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        return source
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{source_id}", response_model=Source)
async def update_source(
    source_id: str,
    source_update: SourceBase,
    service: SourceService = Depends(get_source_service)
):
    """Update a source"""
    try:
        if not ObjectId.is_valid(source_id):
            raise HTTPException(status_code=400, detail="Invalid source ID")
        
        updated = await service.update_source(source_id, source_update.dict())
        if not updated:
            raise HTTPException(status_code=404, detail="Source not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: str,
    service: SourceService = Depends(get_source_service)
):
    """Delete a source"""
    try:
        if not ObjectId.is_valid(source_id):
            raise HTTPException(status_code=400, detail="Invalid source ID")
        
        success = await service.delete_source(source_id)
        if not success:
            raise HTTPException(status_code=404, detail="Source not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
