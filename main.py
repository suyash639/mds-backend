from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from app.routes import questions, categories, sources, bulk, events
from app.middleware import ErrorHandlingMiddleware, RequestLoggingMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client: AsyncIOMotorClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global client
    from app.config import MONGODB_URL, DB_NAME
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        app.db = client[DB_NAME]
        await create_indexes(app.db)
        logger.info("MongoDB connected and indexes created")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    yield
    # Shutdown
    if client:
        client.close()
        logger.info("MongoDB disconnected")

async def create_indexes(db):
    """Create database indexes"""
    questions_col = db["questions"]
    await questions_col.create_index("category_id")
    await questions_col.create_index("source_id")
    await questions_col.create_index([("metadata.difficulty", 1)])
    await questions_col.create_index([("created_at", -1)])
    
    idempotency_col = db["idempotency_keys"]
    await idempotency_col.create_index("idempotency_key", unique=True)
    await idempotency_col.create_index("created_at", expireAfterSeconds=3600)
    
    events_col = db["events"]
    await events_col.create_index([("created_at", -1)])
    await events_col.create_index("entity_id")
    
    logger.info("Indexes created successfully")

app = FastAPI(
    title="Master Data Service API",
    description="Production-grade API for managing exam question data",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router, prefix="/api/v1/questions", tags=["questions"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(sources.router, prefix="/api/v1/sources", tags=["sources"])
app.include_router(bulk.router, prefix="/api/v1/bulk", tags=["bulk operations"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Master Data Service", "version": "2.0.0"}

@app.get("/")
async def root():
    """API root endpoint with documentation link"""
    return {
        "message": "Master Data Service API",
        "docs": "/docs",
        "version": "2.0.0"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )
