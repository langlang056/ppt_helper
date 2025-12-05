"""Pydantic models for API requests/responses."""
from pydantic import BaseModel, Field
from typing import Literal, Optional


class KeyPoint(BaseModel):
    """A single key point extracted from the page."""

    concept: str = Field(..., description="The academic concept name")
    explanation: str = Field(..., description="Simplified explanation in Chinese")
    is_important: bool = Field(default=False, description="Whether this is a critical concept")


class PageContent(BaseModel):
    """Structured explanation content for a single page."""

    summary: str = Field(..., description="One sentence summary in Chinese")
    key_points: list[KeyPoint] = Field(default_factory=list, description="List of key concepts")
    analogy: str = Field(default="", description="A relatable analogy in Chinese")
    example: str = Field(default="", description="A concrete example in Chinese")


class PageExplanation(BaseModel):
    """Complete explanation for a single PDF page."""

    page_number: int = Field(..., ge=1, description="1-indexed page number")
    page_type: Literal["TITLE", "CONTENT", "END", "INDEX"] = Field(
        default="CONTENT", description="Type of page classified by Navigator"
    )
    content: PageContent
    original_language: str | None = Field(
        default=None, description="Detected language (fr/en/mixed)"
    )


# 新增：Markdown格式的解释响应
class PageExplanationMarkdown(BaseModel):
    """Markdown format explanation for a single PDF page."""

    page_number: int = Field(..., ge=1, description="1-indexed page number")
    markdown_content: str = Field(..., description="Markdown formatted explanation")
    summary: str = Field(default="", description="Brief summary for context")


class UploadResponse(BaseModel):
    """Response after successful PDF upload."""

    pdf_id: str = Field(..., description="Unique identifier for the uploaded PDF")
    total_pages: int = Field(..., ge=1, description="Total number of pages")
    filename: str
    message: str = "PDF uploaded and parsed successfully"


class ExplanationRequest(BaseModel):
    """Request to get explanation for specific page."""

    pdf_id: str
    page_number: int = Field(..., ge=1)


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: str | None = None


# 新增：处理进度响应
class ProcessingProgress(BaseModel):
    """Processing progress for a PDF."""

    pdf_id: str
    total_pages: int
    processed_pages: int
    status: str  # pending, processing, completed, failed
    progress_percentage: float
