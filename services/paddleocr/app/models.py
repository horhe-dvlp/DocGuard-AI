"""
Pydantic models for PPStructure v3 FastAPI service.

This module contains data models used for API request/response validation.
"""

from typing import List
from pydantic import BaseModel, Field


class BBox(BaseModel):
    """Bounding box coordinates model.

    Attributes:
        x1: Left coordinate (top-left corner)
        y1: Top coordinate (top-left corner)
        x2: Right coordinate (bottom-right corner)
        y2: Bottom coordinate (bottom-right corner)
    """

    x1: int = Field(..., description="Left coordinate", ge=0)
    y1: int = Field(..., description="Top coordinate", ge=0)
    x2: int = Field(..., description="Right coordinate", ge=0)
    y2: int = Field(..., description="Bottom coordinate", ge=0)


class Detection(BaseModel):
    """Detection result model for document layout elements.

    Attributes:
        bbox: Bounding box coordinates of the detected element
        cls: Classification/type of the detected element (text, table, figure, etc.)
        confidence: Detection confidence score (0.0 to 1.0)
    """

    bbox: BBox = Field(..., description="Bounding box coordinates")
    cls: str = Field(..., description="Element type/class")
    confidence: float | None = Field(
        None, description="Detection confidence score", ge=0.0, le=1.0
    )


class AnalyzeResponse(BaseModel):
    """Response model for document layout analysis.

    Attributes:
        detections: List of detected layout elements with their positions and types
        elapsed_ms: Processing time in milliseconds
    """

    detections: List[Detection] = Field(
        default_factory=list, description="List of detected elements"
    )
    elapsed_ms: float = Field(..., description="Processing time in milliseconds", ge=0)


class HealthResponse(BaseModel):
    """Health check response model.

    Attributes:
        status: Service health status
        service: Service name identifier
    """

    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")


class ErrorResponse(BaseModel):
    """Error response model.

    Attributes:
        detail: Error message details
    """

    detail: str = Field(..., description="Error message details")
