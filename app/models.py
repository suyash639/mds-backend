from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        schema = handler(core_schema)
        schema.update(type="string")
        return schema

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class Category(CategoryBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class SourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    url: Optional[str] = None
    year: Optional[int] = None

class Source(SourceBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class MetadataBase(BaseModel):
    tags: Optional[List[str]] = []
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    time_limit_seconds: Optional[int] = None
    passing_score: Optional[float] = None
    is_active: bool = True

class Metadata(MetadataBase):
    pass

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1)
    category_id: str
    source_id: str
    type: str = Field(default="multiple_choice")
    options: Optional[List[str]] = []
    correct_answer: str
    explanation: Optional[str] = None
    metadata: Metadata = Field(default_factory=Metadata)

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    category_id: Optional[str] = None
    source_id: Optional[str] = None
    type: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    metadata: Optional[Metadata] = None

class Question(QuestionBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class QuestionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Question]

class ErrorResponse(BaseModel):
    detail: str
    error_code: str

class SearchQueryRequest(BaseModel):
    text: Optional[str] = None
    category_id: Optional[str] = None
    source_id: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

class StatisticsResponse(BaseModel):
    total_questions: int
    by_difficulty: Dict[str, int]
    by_category: Dict[str, int]
    by_source: Dict[str, int]
