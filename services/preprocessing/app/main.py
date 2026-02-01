"""
Preprocessing FastAPI service for document preprocessing.

This service provides endpoints for complete document preprocessing pipeline:
1. Document segmentation using PPStructure
2. Content extraction from segments using PaddleVL
3. JSON serialization of structured results
"""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .public.api import router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Initialize FastAPI application
app = FastAPI(
    title="Preprocessing Service",
    description="Document preprocessing service with PPStructure and PaddleVL integration",
    version="1.0.0",
)

# Include API router
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors.

    Args:
        request: The HTTP request that caused the exception
        exc: The exception that was raised

    Returns:
        JSONResponse: Error response with details
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    # Run the service directly (for development)
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
