"""
Public API endpoints for Preprocessing service.

This module contains the main FastAPI endpoints for document preprocessing.
"""

import os
import time
import logging

from fastapi import APIRouter, File, UploadFile, HTTPException

from .models import ProcessResponse, HealthResponse
from ..private.pipeline import run_preprocessing_pipeline_with_splits

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Get service URLs from environment variables
PPSTRUCTURE_URL = os.getenv("PPSTRUCTURE_URL", "http://paddleocr:8080")
PADDLEVL_URL = os.getenv("PADDLEVL_URL", "http://paddleocr-vl:8080")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify service readiness.

    Returns:
        HealthResponse: Service health status and identification
    """
    return HealthResponse(status="healthy", service="Preprocessing")


@router.post("/process", response_model=ProcessResponse)
async def process_document(
    image: UploadFile = File(...),
    max_segments: int = 8,
    min_height: int = 50,
):
    """Process document image through preprocessing pipeline.

    Args:
        image: Uploaded document image file (JPEG, PNG, etc.)
        max_segments: Maximum number of segments to create (default: 8)
        min_height: Minimum segment height in pixels (default: 50)

    Returns:
        ProcessResponse: Processing results with all segments and their content

    Raises:
        HTTPException:
            - 400 if file is not a valid image
            - 500 if processing fails
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        logger.warning(f"Invalid file type uploaded: {image.content_type}")
        raise HTTPException(
            status_code=400, detail="File must be an image (JPEG, PNG, etc.)"
        )

    start_time = time.perf_counter()

    try:
        logger.info(f"Processing document: {image.filename}")
        image_data = await image.read()

        results = await run_preprocessing_pipeline_with_splits(
            image_data=image_data,
            ppstructure_url=PPSTRUCTURE_URL,
            paddlevl_url=PADDLEVL_URL,
            max_segments=max_segments,
            min_height=min_height,
        )

        # Extract segments from results
        segments = []
        for segment_image, segment_list in results:
            segments.extend(segment_list)

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            f"Document processing completed in {elapsed_ms:.2f}ms. "
            f"Processed {len(segments)} horizontal segments"
        )

        return ProcessResponse(
            segments=segments,
            total_segments=len(segments),
            elapsed_ms=elapsed_ms,
            status="success",
        )

    except Exception as e:
        logger.error(f"Error processing document {image.filename}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process document: {str(e)}"
        )
