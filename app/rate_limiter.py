from datetime import datetime, timedelta
from typing import Dict, Tuple
from collections import defaultdict

class SimpleRateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(
        self,
        identifier: str,
        max_requests: int = 100,
        window_seconds: int = 60
    ) -> Tuple[bool, Dict]:
        """Check if request is allowed"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[identifier]) < max_requests:
            self.requests[identifier].append(now)
            return True, {
                "limit": max_requests,
                "remaining": max_requests - len(self.requests[identifier]),
                "reset": (window_start + timedelta(seconds=window_seconds)).timestamp()
            }
        
        return False, {
            "limit": max_requests,
            "remaining": 0,
            "reset": (window_start + timedelta(seconds=window_seconds)).timestamp()
        }

rate_limiter = SimpleRateLimiter()
