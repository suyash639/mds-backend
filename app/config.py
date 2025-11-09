import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mds_db")
API_KEY = os.getenv("API_KEY", "your-api-key-here")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Pagination defaults
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Idempotency settings
IDEMPOTENCY_TTL = 3600  # 1 hour in seconds

# Bulk operation settings
BULK_BATCH_SIZE = 100
MAX_BULK_SIZE = 10000
