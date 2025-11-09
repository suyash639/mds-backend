# Master Data Service API - Detailed Documentation

## Authentication

Currently using API_KEY environment variable. Future versions will support JWT and OAuth.

## Request/Response Format

All requests and responses use JSON format.

### Success Response (2xx)
\`\`\`json
{
  "id": "507f1f77bcf86cd799439011",
  "text": "Sample question",
  "category_id": "cat_1",
  ...
}
\`\`\`

### Error Response (4xx, 5xx)
\`\`\`json
{
  "detail": "Detailed error message",
  "error_code": "ERROR_CODE"
}
\`\`\`

## Pagination

List endpoints support pagination with these query parameters:
- `page`: Page number (default: 1, min: 1)
- `page_size`: Items per page (default: 10, max: 100)

Response includes:
\`\`\`json
{
  "total": 100,
  "page": 1,
  "page_size": 10,
  "items": [...]
}
\`\`\`

## Filtering

Filters can be combined for advanced queries:
- `category_id`: Filter by category
- `source_id`: Filter by source
- `difficulty`: Filter by difficulty (easy, medium, hard)
- `tags`: Filter by tags (array)
- `start_date`: Filter by creation date (ISO format)
- `end_date`: Filter by creation date (ISO format)

## Rate Limiting

No rate limiting currently implemented. Subject to change in production.

## Idempotency

For safe retries, include `Idempotency-Key` header:
\`\`\`
POST /api/v1/questions
Idempotency-Key: unique-key-12345
\`\`\`

## Bulk Operations

### Import Limitations
- Max file size: 10MB
- Max items per file: 10,000
- Errors are logged per item, import continues on failure

### Export Filters
- Supports same filters as search endpoints
- Max export size: 50,000 items

## Status Codes

- `200 OK`: Successful GET/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate/conflict error
- `500 Internal Server Error`: Server error

## Rate Limits (Future)

Planned rate limits:
- Public API: 100 requests/minute
- Authenticated: 1000 requests/minute
- Bulk operations: 10 requests/minute
\`\`\`

```python file="" isHidden
