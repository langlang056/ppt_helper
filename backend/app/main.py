"""FastAPI application entry point."""
import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.config import get_settings
from app.models.database import init_db, get_db
from app.models.schemas import (
    UploadResponse,
    PageExplanation,
    ErrorResponse,
)
from app.services.pdf_parser import pdf_parser
from app.services.cache_service import cache_service

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup/shutdown events."""
    # Startup: Initialize database and create upload directories
    await init_db()
    Path(settings.upload_dir).mkdir(exist_ok=True)
    Path(settings.temp_dir).mkdir(exist_ok=True)
    print(f"✅ Database initialized")
    print(f"✅ Upload directory: {settings.upload_dir}")
    yield
    # Shutdown: cleanup if needed
    print("👋 Shutting down UniTutor AI")


app = FastAPI(
    title="UniTutor AI Backend",
    description="Multi-Agent Courseware Explainer API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "UniTutor AI Backend is running",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.post("/api/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload and parse a PDF file.

    Steps:
    1. Validate file format and size
    2. Calculate PDF hash to check for duplicates
    3. Save file to upload directory
    4. Parse with LlamaParse
    5. Store metadata in database

    Returns:
        UploadResponse with pdf_id and total_pages
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Read file content
    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)

    if file_size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.max_file_size_mb}MB",
        )

    # Save file temporarily to calculate hash
    temp_path = Path(settings.temp_dir) / file.filename
    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        # Generate PDF ID (hash)
        pdf_id = pdf_parser._generate_pdf_id(str(temp_path))

        # Check if already processed
        if await cache_service.check_pdf_exists(db, pdf_id):
            # Return existing metadata
            pdf_doc = await cache_service.get_pdf_metadata(db, pdf_id)
            return UploadResponse(
                pdf_id=pdf_id,
                total_pages=pdf_doc.total_pages,
                filename=file.filename,
                message="PDF already exists in cache",
            )

        # Move to permanent storage
        final_path = Path(settings.upload_dir) / f"{pdf_id}.pdf"
        temp_path.rename(final_path)

        # Get page count (quick method without full parsing)
        total_pages = pdf_parser.get_page_count(str(final_path))

        # Save metadata
        await cache_service.save_pdf_metadata(
            db,
            pdf_id=pdf_id,
            filename=file.filename,
            total_pages=total_pages,
            file_path=str(final_path),
        )

        return UploadResponse(
            pdf_id=pdf_id,
            total_pages=total_pages,
            filename=file.filename,
        )

    except Exception as e:
        # Cleanup on error
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/api/explain/{pdf_id}/{page_number}", response_model=PageExplanation)
async def get_explanation(
    pdf_id: str,
    page_number: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI-generated explanation for a specific page.

    Steps:
    1. Check cache first
    2. If cache miss, parse the page with LlamaParse
    3. Return raw text (Phase 2 will add LangGraph processing)

    Args:
        pdf_id: Unique PDF identifier
        page_number: 1-indexed page number

    Returns:
        PageExplanation with structured content
    """
    # Verify PDF exists
    pdf_doc = await cache_service.get_pdf_metadata(db, pdf_id)
    if not pdf_doc:
        raise HTTPException(status_code=404, detail="PDF not found")

    if page_number < 1 or page_number > pdf_doc.total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Must be between 1 and {pdf_doc.total_pages}",
        )

    # Check cache
    cached = await cache_service.get_cached_explanation(db, pdf_id, page_number)
    if cached:
        return cached

    # Cache miss - Parse the page
    try:
        page_text = await pdf_parser.parse_single_page(pdf_doc.file_path, page_number)

        # TODO: Phase 2 - Process with LangGraph agents
        # For now, return a simple response
        from app.models.schemas import PageContent, KeyPoint

        explanation = PageExplanation(
            page_number=page_number,
            page_type="CONTENT",
            content=PageContent(
                summary=f"第 {page_number} 页内容(待 AI 处理)",
                key_points=[
                    KeyPoint(
                        concept="原始文本",
                        explanation=page_text[:200] + "...",  # Preview
                        is_important=False,
                    )
                ],
                analogy="[将在 Phase 2 添加 LangGraph 处理]",
                example="",
            ),
            original_language="mixed",
        )

        # Save to cache
        await cache_service.save_explanation(db, pdf_id, page_number, explanation)

        return explanation

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process page: {str(e)}"
        )


@app.get("/api/pdf/{pdf_id}/info")
async def get_pdf_info(pdf_id: str, db: AsyncSession = Depends(get_db)):
    """Get PDF metadata."""
    pdf_doc = await cache_service.get_pdf_metadata(db, pdf_id)
    if not pdf_doc:
        raise HTTPException(status_code=404, detail="PDF not found")

    return {
        "pdf_id": pdf_doc.id,
        "filename": pdf_doc.filename,
        "total_pages": pdf_doc.total_pages,
        "uploaded_at": pdf_doc.uploaded_at.isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
