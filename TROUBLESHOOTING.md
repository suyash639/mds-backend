# Troubleshooting Guide

## Common Issues & Solutions

### 1. MongoDB Connection Refused

**Error:** \`Connection refused\`

**Solutions:**
- Ensure MongoDB is running: \`docker-compose up -d mongodb\`
- Check MongoDB port: \`netstat -an | grep 27017\`
- Verify credentials in .env file

### 2. API Port Already in Use

**Error:** \`Address already in use\`

**Solutions:**
\`\`\`bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
docker run -p 8001:8000 mds-api:latest
\`\`\`

### 3. Test Failures

**Error:** \`ModuleNotFoundError\`

**Solutions:**
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest -v -s
\`\`\`

### 4. Docker Build Fails

**Error:** \`failed to build\`

**Solutions:**
\`\`\`bash
# Clean docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
\`\`\`

### 5. Validation Errors

**Error:** \`Validation failed\`

**Solutions:**
- Check request JSON format
- Verify all required fields are present
- Use Swagger UI for testing: \`/docs\`

## Performance Issues

### Slow Queries

- Check MongoDB indexes
- Use pagination (\`page_size\` parameter)
- Monitor database metrics

### High Memory Usage

\`\`\`bash
# Check container memory
docker stats mds_api

# Increase limits if needed
docker update --memory 2g mds_api
\`\`\`

## Debug Mode

Enable detailed logging:

\`\`\`env
DEBUG=true
LOG_LEVEL=DEBUG
\`\`\`

Then check logs:
\`\`\`bash
docker logs -f mds_api
\`\`\`

## Getting Help

1. Check this guide
2. Review logs: \`docker logs mds_api\`
3. Test with curl or Swagger UI
4. Open an issue with error message and logs
\`\`\`
