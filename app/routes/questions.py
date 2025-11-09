from fastapi import APIRouter, Depends, HTTPException, Query, status, Header
from typing import List, Optional
from app.models import Question, QuestionCreate, QuestionUpdate, QuestionListResponse
from app.services.question_service import QuestionService
from app.validators import QuestionValidator
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_question_service(request) -> QuestionService:
    """Dependency injection for QuestionService"""
    db = request.app.db
    return QuestionService(db)

@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate,
    service: QuestionService = Depends(get_question_service),
    idempotency_key: Optional[str] = Header(None)
):
    """Create a new question"""
    try:
        QuestionValidator.validate_question_text(question.text)
        if question.options:
            QuestionValidator.validate_options(question.options)
        QuestionValidator.validate_correct_answer(question.correct_answer, question.options)
        QuestionValidator.validate_metadata(question.metadata.dict())
        
        result = await service.create_question(question.dict(), idempotency_key)
        logger.info(f"Created question: {result.id}")
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating question: {e}")
        raise HTTPException(status_code=500, detail="Failed to create question")

@router.get("/{question_id}", response_model=Question)
async def get_question(
    question_id: str,
    service: QuestionService = Depends(get_question_service)
):
    """Get a question by ID"""
    try:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        
        question = await service.get_question(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving question: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve question")

@router.get("/", response_model=QuestionListResponse)
async def list_questions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category_id: Optional[str] = None,
    source_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    service: QuestionService = Depends(get_question_service)
):
    """List questions with pagination and filters"""
    try:
        filters = {}
        if category_id:
            filters["category_id"] = category_id
        if source_id:
            filters["source_id"] = source_id
        if difficulty:
            valid_difficulties = ["easy", "medium", "hard"]
            if difficulty not in valid_difficulties:
                raise HTTPException(status_code=400, detail="Invalid difficulty level")
            filters["metadata.difficulty"] = difficulty
        
        result = await service.list_questions(page, page_size, filters)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to list questions")

@router.put("/{question_id}", response_model=Question)
async def update_question(
    question_id: str,
    question_update: QuestionUpdate,
    service: QuestionService = Depends(get_question_service)
):
    """Update a question"""
    try:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        
        update_data = question_update.dict(exclude_unset=True)
        if "text" in update_data:
            update_data["text"] = QuestionValidator.validate_question_text(update_data["text"])
        if "options" in update_data:
            update_data["options"] = QuestionValidator.validate_options(update_data["options"])
        if "correct_answer" in update_data:
            update_data["correct_answer"] = QuestionValidator.validate_correct_answer(
                update_data["correct_answer"],
                update_data.get("options")
            )
        
        updated_question = await service.update_question(question_id, update_data)
        if not updated_question:
            raise HTTPException(status_code=404, detail="Question not found")
        logger.info(f"Updated question: {question_id}")
        return updated_question
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating question: {e}")
        raise HTTPException(status_code=500, detail="Failed to update question")

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: str,
    service: QuestionService = Depends(get_question_service)
):
    """Delete a question"""
    try:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        
        success = await service.delete_question(question_id)
        if not success:
            raise HTTPException(status_code=404, detail="Question not found")
        logger.info(f"Deleted question: {question_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting question: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete question")

@router.get("/category/{category_id}/count")
async def count_by_category(
    category_id: str,
    service: QuestionService = Depends(get_question_service)
):
    """Get count of questions by category"""
    try:
        count = await service.count_by_category(category_id)
        return {"category_id": category_id, "count": count}
    except Exception as e:
        logger.error(f"Error counting questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to count questions")
