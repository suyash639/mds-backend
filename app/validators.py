from pydantic import BaseModel, field_validator, ValidationError
from typing import List, Optional, Dict, Any
from app.utils import ValidationHelper

class QuestionValidator:
    """Validation logic for questions"""
    
    @staticmethod
    def validate_question_text(text: str) -> str:
        """Validate question text"""
        if not text or len(text.strip()) == 0:
            raise ValueError("Question text cannot be empty")
        if len(text) > 10000:
            raise ValueError("Question text exceeds maximum length of 10000 characters")
        return text.strip()
    
    @staticmethod
    def validate_options(options: List[str]) -> List[str]:
        """Validate question options"""
        if not options or len(options) < 2:
            raise ValueError("At least 2 options are required")
        if len(options) > 10:
            raise ValueError("Maximum 10 options allowed")
        if len(set(options)) != len(options):
            raise ValueError("Duplicate options are not allowed")
        return options
    
    @staticmethod
    def validate_correct_answer(correct_answer: str, options: Optional[List[str]] = None) -> str:
        """Validate correct answer"""
        if not correct_answer or len(correct_answer.strip()) == 0:
            raise ValueError("Correct answer cannot be empty")
        if options and correct_answer not in options:
            raise ValueError("Correct answer must be one of the provided options")
        return correct_answer.strip()
    
    @staticmethod
    def validate_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata"""
        if metadata.get("time_limit_seconds"):
            if metadata["time_limit_seconds"] < 0:
                raise ValueError("Time limit must be positive")
        
        if metadata.get("passing_score"):
            score = metadata["passing_score"]
            if not (0 <= score <= 100):
                raise ValueError("Passing score must be between 0 and 100")
        
        return metadata

class CategoryValidator:
    """Validation logic for categories"""
    
    @staticmethod
    def validate_name(name: str) -> str:
        """Validate category name"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Category name cannot be empty")
        if len(name) > 100:
            raise ValueError("Category name exceeds maximum length")
        return name.strip()
    
    @staticmethod
    def validate_description(description: Optional[str]) -> Optional[str]:
        """Validate category description"""
        if description and len(description) > 1000:
            raise ValueError("Description exceeds maximum length")
        return description

class SourceValidator:
    """Validation logic for sources"""
    
    @staticmethod
    def validate_name(name: str) -> str:
        """Validate source name"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Source name cannot be empty")
        if len(name) > 100:
            raise ValueError("Source name exceeds maximum length")
        return name.strip()
    
    @staticmethod
    def validate_url(url: Optional[str]) -> Optional[str]:
        """Validate source URL"""
        if url and not ValidationHelper.validate_url(url):
            raise ValueError("Invalid URL format")
        return url
    
    @staticmethod
    def validate_year(year: Optional[int]) -> Optional[int]:
        """Validate source year"""
        if year and (year < 1900 or year > 2100):
            raise ValueError("Invalid year")
        return year
