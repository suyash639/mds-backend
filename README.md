# Master Data Service (MDS) API

Production-grade FastAPI backend for managing exam question data with advanced search, bulk operations, and event tracking.

## Features

- **CRUD Operations**: Create, read, update, delete questions, categories, and sources
- **Advanced Search**: Full-text search, difficulty filtering, date ranges, and tags
- **Bulk Operations**: Import/export JSON, bulk updates, bulk deletes
- **Event Tracking**: Audit trail for all changes with event logging
- **Idempotency**: Safe request retries with idempotency keys
- **Pagination**: Efficient pagination with configurable page sizes
- **Error Handling**: Comprehensive error responses with error codes
- **Database Indexing**: Optimized MongoDB indexes for performance
- **API Documentation**: Interactive Swagger UI and ReDoc

## Tech Stack

- **FastAPI**: Modern Python web framework
- **MongoDB**: Document database with async Motor driver
- **Pydantic**: Data validation and serialization
- **Docker**: Containerization for easy deployment
- **Pytest**: Testing framework with async support

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker Compose

\`\`\`bash
# Clone the repository
git clone <repository-url>
cd master-data-service

# Start services
docker-compose up

# API will be available at http://localhost:8000
\`\`\`

### Local Development

\`\`\`bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Run the server
uvicorn main:app --reload
\`\`\`

## API Endpoints

### Questions
- `POST /api/v1/questions` - Create question
- `GET /api/v1/questions/{id}` - Get question
- `GET /api/v1/questions` - List questions (paginated)
- `PUT /api/v1/questions/{id}` - Update question
- `DELETE /api/v1/questions/{id}` - Delete question

### Categories
- `POST /api/v1/categories` - Create category
- `GET /api/v1/categories` - List categories
- `GET /api/v1/categories/{id}` - Get category
- `PUT /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Sources
- `POST /api/v1/sources` - Create source
- `GET /api/v1/sources` - List sources
- `GET /api/v1/sources/{id}` - Get source
- `PUT /api/v1/sources/{id}` - Update source
- `DELETE /api/v1/sources/{id}` - Delete source

### Bulk Operations
- `POST /api/v1/bulk/import/json` - Bulk import questions
- `POST /api/v1/bulk/export/json` - Bulk export questions
- `POST /api/v1/bulk/update` - Bulk update questions
- `POST /api/v1/bulk/delete` - Bulk delete questions

### Search
- `GET /api/v1/search/text-search` - Full-text search
- `GET /api/v1/search/advanced` - Advanced search with filters
- `GET /api/v1/search/by-difficulty` - Filter by difficulty
- `GET /api/v1/search/statistics` - Get database statistics

### Events
- `GET /api/v1/events` - Get audit trail events

## Example Usage

### Create a Question
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is the capital of France?",
    "category_id": "geo_101",
    "source_id": "src_1",
    "correct_answer": "Paris",
    "options": ["London", "Paris", "Berlin"],
    "metadata": {
      "difficulty": "easy",
      "tags": ["geography", "capitals"]
    }
  }'
\`\`\`

### Search Questions
\`\`\`bash
curl "http://localhost:8000/api/v1/search/advanced?text=France&difficulty=easy"
\`\`\`

### Bulk Import
\`\`\`bash
curl -X POST http://localhost:8000/api/v1/bulk/import/json \
  -F "file=@questions.json"
\`\`\`

## Configuration

Create `.env` file with:
\`\`\`
MONGODB_URL=mongodb://admin:password@mongodb:27017/
DB_NAME=mds_db
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
\`\`\`

## Testing

Run tests with pytest:
\`\`\`bash
# All tests
pytest

# Specific test file
pytest tests/test_question_service.py

# With coverage
pytest --cov=app tests/
\`\`\`

## Database Indexes

Indexes are created automatically on startup:
- Questions: category_id, source_id, difficulty, created_at
- Idempotency: idempotency_key (unique, 1 hour TTL)
- Events: created_at, entity_id

## Error Handling

All errors follow this format:
\`\`\`json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE"
}
\`\`\`

## Performance

- Pagination: Max 100 items per page
- Text search: Regex-based with case-insensitive matching
- Aggregations: MongoDB pipelines for statistics
- Bulk operations: Batch processing with error tracking

## Deployment

### Docker Build
\`\`\`bash
docker build -t mds-api:latest .
docker run -p 8000:8000 mds-api:latest
\`\`\`

### Kubernetes
See `k8s-deployment.yaml` for Kubernetes deployment

## License

MIT
