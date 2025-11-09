"""
Database seeding script
Run: python -m scripts.seed_db
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URL, DB_NAME

async def seed_database():
    """Seed database with sample data"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    # Sample categories
    categories = [
        {"name": "Mathematics", "description": "Math questions"},
        {"name": "Science", "description": "Science questions"},
        {"name": "History", "description": "History questions"},
    ]
    
    await db["categories"].insert_many(categories)
    print(f"Inserted {len(categories)} categories")
    
    # Sample sources
    sources = [
        {"name": "JEE Advanced", "year": 2023},
        {"name": "UPSC", "year": 2023},
        {"name": "IIT", "year": 2022},
    ]
    
    await db["sources"].insert_many(sources)
    print(f"Inserted {len(sources)} sources")
    
    # Sample questions
    questions = [
        {
            "text": "What is 2+2?",
            "category_id": "mathematics",
            "source_id": "jee",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4",
            "metadata": {"difficulty": "easy", "tags": ["arithmetic"]}
        },
        {
            "text": "What is the capital of France?",
            "category_id": "history",
            "source_id": "upsc",
            "type": "multiple_choice",
            "options": ["London", "Paris", "Berlin", "Madrid"],
            "correct_answer": "Paris",
            "metadata": {"difficulty": "easy", "tags": ["geography"]}
        },
    ]
    
    await db["questions"].insert_many(questions)
    print(f"Inserted {len(questions)} questions")
    
    client.close()
    print("Database seeding completed")

if __name__ == "__main__":
    asyncio.run(seed_database())
