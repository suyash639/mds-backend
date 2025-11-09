from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re

class SearchFilters:
    """Helper class for building search filters"""
    
    @staticmethod
    def build_text_search(query: str) -> Dict[str, Any]:
        """Build text search filter"""
        return {
            "$or": [
                {"text": {"$regex": query, "$options": "i"}},
                {"explanation": {"$regex": query, "$options": "i"}}
            ]
        }
    
    @staticmethod
    def build_difficulty_filter(difficulty: str) -> Dict[str, Any]:
        """Build difficulty filter"""
        return {"metadata.difficulty": difficulty}
    
    @staticmethod
    def build_date_range_filter(start_date: str, end_date: str) -> Dict[str, Any]:
        """Build date range filter"""
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            return {
                "created_at": {
                    "$gte": start,
                    "$lte": end
                }
            }
        except ValueError:
            raise ValueError("Invalid date format. Use ISO format: YYYY-MM-DD")
    
    @staticmethod
    def build_tag_filter(tags: List[str]) -> Dict[str, Any]:
        """Build tag filter"""
        return {"metadata.tags": {"$in": tags}}
    
    @staticmethod
    def combine_filters(*filters: Dict[str, Any]) -> Dict[str, Any]:
        """Combine multiple filters with AND logic"""
        combined = {}
        for f in filters:
            if f:
                combined.update(f)
        return combined

class PaginationHelper:
    """Helper for pagination calculations"""
    
    @staticmethod
    def calculate_skip(page: int, page_size: int) -> int:
        """Calculate skip value for MongoDB"""
        if page < 1:
            page = 1
        return (page - 1) * page_size
    
    @staticmethod
    def validate_pagination(page: int, page_size: int) -> tuple:
        """Validate and normalize pagination parameters"""
        page = max(1, page)
        page_size = max(1, min(page_size, 100))  # Max 100 per page
        return page, page_size

class ValidationHelper:
    """Helper for data validation"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input"""
        if not text:
            return ""
        text = text.strip()
        text = text[:max_length]
        return text
