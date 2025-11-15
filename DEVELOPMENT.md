# Development Guide

## Project Structure

\`\`\`
master-data-service/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # Database setup
│   ├── events.py              # Event logging
│   ├── exceptions.py          # Custom exceptions
│   ├── idempotency.py         # Idempotency handling
│   ├── middleware.py          # Custom middleware
│   ├── models.py              # Pydantic models
│   ├── rate_limiter.py        # Rate limiting
│   ├── utils.py               # Utility functions
│   ├── validators.py          # Data validation
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── questions.py       # Question endpoints
│   │   ├── categories.py      # Category endpoints
│   │   ├── sources.py         # Source endpoints
│   │   ├── bulk.py            # Bulk operation endpoints
│   │   ├── search.py          # Search endpoints
│   │   └── events.py          # Event endpoints
│   └── services/
│       ├── __init__.py
│       ├── question_service.py
│       ├── category_service.py
│       ├── source_service.py
│       ├── bulk_service.py
│       └── search_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_question_service.py
│   ├── test_bulk_service.py
│   ├── test_search_service.py
│   ├── test_idempotency.py
│   ├── test_events.py
│   ├── test_validators.py
│   ├── test_api_endpoints.py
│   └── test_integration.py
├── main.py                    # FastAPI app entry point
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Local development setup
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── pytest.ini                # Pytest configuration
├── README.md                 # Project documentation
├── DEPLOYMENT.md             # Deployment guide
├── API_DOCUMENTATION.md      # API details
└── DEVELOPMENT.md            # This file
\`\`\`

## Code Style

Follow PEP 8 with these conventions:

- Max line length: 100 characters
- Use type hints for all functions
- Docstrings for all public functions
- Use logging instead of print()

## Git Workflow

\`\`\`bash
# Create feature branch
git checkout -b feature/description

# Make changes and commit
git add .
git commit -m "feat: description of changes"

# Push and create PR
git push origin feature/description
\`\`\`

### Commit Messages

- \`feat:\` New feature
- \`fix:\` Bug fix
- \`docs:\` Documentation
- \`style:\` Code style
- \`refactor:\` Code refactoring
- \`test:\` Test additions
- \`chore:\` Build/dependency updates

## Adding New Features

### 1. Create Model

Update \`app/models.py\` with Pydantic models.

### 2. Create Service

Implement business logic in \`app/services/\`.

### 3. Create Routes

Add endpoints in \`app/routes/\`.

### 4. Add Validation

Implement validators in \`app/validators.py\`.

### 5. Add Tests

Write tests in \`tests/\`.

### 6. Update Documentation

Update README.md and API_DOCUMENTATION.md.

## Testing Guidelines

- Write unit tests for services
- Write integration tests for workflows
- Aim for >80% code coverage
- Use pytest fixtures for setup
- Mock external dependencies

Example test:
\`\`\`python
@pytest.mark.asyncio
async def test_create_question(test_db):
    service = QuestionService(test_db)
    
    result = await service.create_question({
        "text": "Test",
        "category_id": "cat_1",
        "source_id": "src_1",
        "correct_answer": "A"
    })
    
    assert result.text == "Test"
\`\`\`

## Common Issues

### ModuleNotFoundError

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Database Connection Error

Ensure MongoDB is running:
\`\`\`bash
docker-compose up -d mongodb
\`\`\`

### Async/await Issues

Always use \`async def\` for async functions and \`await\` for calls.

## Performance Profiling

\`\`\`bash
# Using cProfile
python -m cProfile -s cumtime -m pytest tests/

# Memory profiling
pip install memory-profiler
python -m memory_profiler main.py
\`\`\`

## Database Migrations

Manual migrations:
\`\`\`bash
# Connect to MongoDB


# Run migrations manually
db.questions.createIndex({category_id: 1})
\`\`\`

Future: Use Alembic for schema versioning.

## Contributing

1. Follow code style
2. Write tests
3. Update documentation
4. Create PR with description
5. Request review
6. Address feedback
7. Merge when approved
\`\`\`
