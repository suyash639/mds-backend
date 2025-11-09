from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from app.models import QuestionCreate
from app.services.bulk_service import BulkService
import json

router = APIRouter()

async def get_bulk_service(request) -> BulkService:
    db = request.app.db
    return BulkService(db)

@router.post("/import/json", status_code=status.HTTP_201_CREATED)
async def bulk_import_json(
    file: UploadFile = File(...),
    service: BulkService = Depends(get_bulk_service)
):
    """Bulk import questions from JSON file"""
    try:
        contents = await file.read()
        data = json.loads(contents)
        
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Expected JSON array")
        
        result = await service.bulk_import(data)
        return {
            "total_imported": result["imported"],
            "total_failed": result["failed"],
            "errors": result["errors"]
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export/json")
async def bulk_export_json(
    category_id: str = None,
    source_id: str = None,
    service: BulkService = Depends(get_bulk_service)
):
    """Export questions to JSON"""
    try:
        filters = {}
        if category_id:
            filters["category_id"] = category_id
        if source_id:
            filters["source_id"] = source_id
        
        data = await service.bulk_export(filters)
        return {"data": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/update", status_code=status.HTTP_200_OK)
async def bulk_update(
    updates: List[dict],
    service: BulkService = Depends(get_bulk_service)
):
    """Bulk update multiple questions"""
    try:
        result = await service.bulk_update(updates)
        return {
            "total_updated": result["updated"],
            "total_failed": result["failed"],
            "errors": result["errors"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/delete", status_code=status.HTTP_200_OK)
async def bulk_delete(
    question_ids: List[str],
    service: BulkService = Depends(get_bulk_service)
):
    """Bulk delete multiple questions"""
    try:
        result = await service.bulk_delete(question_ids)
        return {
            "total_deleted": result["deleted"],
            "total_failed": result["failed"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
