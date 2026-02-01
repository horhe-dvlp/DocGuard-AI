"""
Pydantic models for Preprocessing FastAPI service.

This module contains data models used for API request/response validation.
"""

from typing import List, Optional, Dict, Any
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


class BBoxInfo(BaseModel):
    """Information about a bounding box within a segment.

    Attributes:
        bbox: Bounding box coordinates (relative to segment)
        type: Type of the bbox (text, table, figure, etc.)
    """

    bbox: BBox = Field(..., description="Bounding box coordinates")
    type: str = Field(..., description="Bbox type/class")


class SegmentContent(BaseModel):
    """Parsed content from a document segment.

    Attributes:
        text: Extracted text content from VL model
        metadata: Additional metadata from VL analysis
    """

    text: str = Field(..., description="Extracted text content")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional metadata"
    )


class DocumentSegment(BaseModel):
    """Document segment with layout and content information.

    Attributes:
        bbox: Bounding box coordinates of the horizontal segment
        segment_type: Type of segment - 'horizontal_segment' or specific type
        content: Parsed content from VL model
        confidence: Confidence score (if available)
        bbox_info: List of detected bboxes within this horizontal segment with their types
    """

    bbox: BBox = Field(..., description="Bounding box coordinates")
    segment_type: str = Field(..., description="Segment type/class")
    content: SegmentContent = Field(..., description="Parsed content")
    confidence: Optional[float] = Field(
        None, description="Confidence score", ge=0, le=1
    )
    bbox_info: Optional[List[BBoxInfo]] = Field(
        default_factory=list, description="List of bboxes detected within this segment"
    )


class ProcessResponse(BaseModel):
    """Response model for document processing.

    Attributes:
        segments: List of processed document segments with content
        total_segments: Total number of segments processed
        elapsed_ms: Processing time in milliseconds
        status: Processing status
    """

    segments: List[DocumentSegment] = Field(
        default_factory=list, description="List of processed segments"
    )
    total_segments: int = Field(..., description="Total number of segments", ge=0)
    elapsed_ms: float = Field(..., description="Processing time in milliseconds", ge=0)
    status: str = Field(default="success", description="Processing status")


class HealthResponse(BaseModel):
    """Health check response model.

    Attributes:
        status: Service health status
        service: Service identifier
    """

    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")


class ErrorResponse(BaseModel):
    """Error response model.

    Attributes:
        detail: Error message
        code: Error code (optional)
    """

    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
