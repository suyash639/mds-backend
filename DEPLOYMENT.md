# Master Data Service - Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- MongoDB (optional, included in docker-compose)
- Python 3.11+ (for local development)

## Local Development

### 1. Setup

\`\`\`bash
# Clone repository
git clone <repository-url>
cd master-data-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
\`\`\`

### 2. Run Locally with Docker Compose

\`\`\`bash
# Start all services
docker-compose up

# Access API at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
# ReDoc at http://localhost:8000/redoc
\`\`\`

### 3. Run Tests

\`\`\`bash
# All tests
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_question_service.py -v

# Run with asyncio
pytest -s
\`\`\`

## Production Deployment

### Docker Build

\`\`\`bash
# Build image
docker build -t mds-api:1.0.0 .

# Tag for registry
docker tag mds-api:1.0.0 your-registry/mds-api:1.0.0

# Push to registry
docker push your-registry/mds-api:1.0.0
\`\`\`

### Environment Variables

Set these in production:

\`\`\`

ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
API_KEY=secure-api-key
\`\`\`

### Docker Run

\`\`\`bash
docker run -d \
  -p 8000:8000 \
  -e ENVIRONMENT="production" \
  --name mds-api \
  mds-api:1.0.0
\`\`\`

### With External MongoDB

\`\`\`bash
docker run -d \
  -p 8000:8000 \
  --name mds-api \
  mds-api:1.0.0
\`\`\`

## Kubernetes Deployment

### Create ConfigMap

\`\`\`bash
kubectl create configmap mds-config \
  --from-literal=DB_NAME=mds_db \
  --from-literal=LOG_LEVEL=INFO
\`\`\`

### Create Secret

\`\`\`bash
kubectl create secret generic mds-secrets \
 
\`\`\`

### Deploy

\`\`\`bash
kubectl apply -f k8s-deployment.yaml
\`\`\`

## Monitoring & Logging

### Health Check

\`\`\`bash
curl http://localhost:8000/health
\`\`\`

### Logs

\`\`\`bash
# Docker logs
docker logs mds_api

# Follow logs
docker logs -f mds_api
\`\`\`

### Metrics

Enable Prometheus metrics (future version):
\`\`\`
GET /metrics
\`\`\`

## Scaling

### Docker Swarm

\`\`\`bash
docker service create \
  --name mds-api \
  --replicas 3 \
  -p 8000:8000 \
\
  mds-api:1.0.0
\`\`\`

### Kubernetes Scaling

\`\`\`bash
kubectl scale deployment mds-api --replicas=3
\`\`\`

## Troubleshooting

### MongoDB Connection Issues

Check MongoDB is running:
\`\`\`bash
docker ps | grep mongodb
\`\`\`

Test connection:
\`\`\`bash
\`\`

### API Not Responding

Check if container is running:
\`\`\`bash
docker ps | grep mds_api
\`\`\`

Check logs:
\`\`\`bash
docker logs mds_api
\`\`\`

### Port Already in Use

Change port in docker-compose.yml or run:
\`\`\`bash
docker run -d -p 8001:8000 mds-api:1.0.0
\`\`\`

## Performance Tuning

### MongoDB Optimization

- Create indexes (auto-created on startup)
- Use connection pooling
- Enable compression

### API Optimization

- Pagination (max 100 items/page)
- Caching headers
- Gzip compression

## Security Checklist

- [ ] Use strong MongoDB credentials
- [ ] Enable authentication
- [ ] Use HTTPS in production
- [ ] Set DEBUG=false in production
- [ ] Rotate API keys regularly
- [ ] Use network policies/firewalls
- [ ] Enable MongoDB encryption at rest
- [ ] Use strong container registry credentials
- [ ] Regular security updates

## Backup & Recovery

### MongoDB Backup

\`\`\`bash
# Backup
docker exec mds_mongodb mongodump --out /backup/

# Restore
docker exec mds_mongodb mongorestore /backup/
\`\`\`

### Database Export

\`\`\`bash
curl "http://localhost:8000/api/v1/bulk/export/json" > backup.json
\`\`\`

## Rollback Procedure

\`\`\`bash
# Stop current version
docker stop mds_api

# Run previous version
docker run -d --name mds_api mds-api:0.9.0

# Verify
curl http://localhost:8000/health
\`\`\`
\`\`\`
