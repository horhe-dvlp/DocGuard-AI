"""
PPStructure v3 FastAPI service for document layout analysis.

This service provides endpoints for analyzing document structure using
PaddleOCR's PPStructure v3 pipeline with optimized performance settings.
"""

import io
import time
import logging
from contextlib import asynccontextmanager

import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from paddleocr import PPStructureV3

from .models import AnalyzeResponse, Detection, BBox, HealthResponse, ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events.

    Initializes PPStructure v3 on startup with optimized settings
    for document layout analysis and cleans up on shutdown.

    Args:
        app: FastAPI application instance
    """
    logger.info("Initializing PPStructure v3...")
    try:
        # Initialize PPStructure with optimized configuration
        # Disable unnecessary components for better performance
        app.state.ppstruct = PPStructureV3(
            lang="ru",
            use_table_recognition=False,
            use_formula_recognition=False,
            use_chart_recognition=False,
            use_seal_recognition=False,
            use_region_detection=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
        )
        logger.info("PPStructure v3 initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize PPStructure: {e}")
        raise

    yield

    # Cleanup on shutdown
    logger.info("Shutting down PPStructure service...")
    if hasattr(app.state, "ppstruct"):
        app.state.ppstruct = None


# Initialize FastAPI application
app = FastAPI(
    title="PPStructure v3 Service",
    description="Document layout analysis service using PaddleOCR PPStructure v3",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint for service status check.

    Returns:
        dict: Service status message
    """
    return {"message": "PPStructure v3 service is running"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify service readiness.

    Returns:
        HealthResponse: Service health status and identification

    Raises:
        HTTPException: 503 if service is not properly initialized
    """
    if not hasattr(app.state, "ppstruct") or app.state.ppstruct is None:
        logger.error("Health check failed: PPStructure not initialized")
        raise HTTPException(
            status_code=503, detail="Service not ready - PPStructure not initialized"
        )

    return HealthResponse(status="healthy", service="PPStructure v3")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(image: UploadFile = File(...)):
    """Analyze document layout and extract structural elements.

    This endpoint processes an uploaded image to detect and classify
    structural elements like text blocks, tables, figures, etc. using
    PPStructure v3 pipeline.

    Args:
        image: Uploaded image file (JPEG, PNG, etc.)

    Returns:
        AnalyzeResponse: Analysis results with detected elements and processing time

    Raises:
        HTTPException:
            - 400 if file is not a valid image
            - 503 if service is not initialized
            - 500 if processing fails
    """
    # Validate file type
    if not image.content_type or not image.content_type.startswith("image/"):
        logger.warning(f"Invalid file type uploaded: {image.content_type}")
        raise HTTPException(
            status_code=400, detail="File must be an image (JPEG, PNG, etc.)"
        )

    # Check service readiness
    if not hasattr(app.state, "ppstruct") or app.state.ppstruct is None:
        logger.error("Analysis failed: PPStructure not initialized")
        raise HTTPException(
            status_code=503, detail="Service not ready - PPStructure not initialized"
        )

    # Start timing
    start_time = time.perf_counter()

    try:
        # Read and preprocess image
        logger.info(f"Processing image: {image.filename}")
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data)).convert("RGB")
        img_array = np.array(pil_image)

        # Perform document structure analysis
        logger.info("Running PPStructure analysis...")
        ppstruct = app.state.ppstruct
        result = ppstruct.predict(img_array)[0].json

        # Extract layout analysis results
        layout_res = result.get("res", {}).get("parsing_res_list", [])
        detections = []

        for obj in layout_res:
            try:
                # PPStructure returns bbox in xyxy format
                x1, y1, x2, y2 = map(int, obj["block_bbox"])

                detections.append(
                    Detection(
                        bbox=BBox(x1=x1, y1=y1, x2=x2, y2=y2),
                        cls=obj.get("block_label", "unknown"),
                    )
                )
            except (KeyError, ValueError, TypeError) as e:
                logger.warning(f"Skipping invalid detection object: {e}")
                continue

        # Calculate processing time
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            f"Analysis completed in {elapsed_ms:.2f}ms, "
            f"found {len(detections)} elements for {image.filename}"
        )

        return AnalyzeResponse(detections=detections, elapsed_ms=elapsed_ms)

    except Exception as e:
        logger.error(f"Error processing image {image.filename}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process image: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors.

    Args:
        request: The HTTP request that caused the exception
        exc: The exception that was raised

    Returns:
        JSONResponse: Error response with details
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    # Run the service directly (for development)
    uvicorn.run(app, host="0.0.0.0", port=8072, log_level="info")
