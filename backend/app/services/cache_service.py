"""Caching service to avoid redundant LLM calls."""
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import PageExplanationCache, PDFDocument
from app.models.schemas import PageExplanation


class CacheService:
    """Handles reading/writing explanation cache."""

    @staticmethod
    async def get_cached_explanation(
        db: AsyncSession, pdf_id: str, page_number: int
    ) -> PageExplanation | None:
        """
        Retrieve cached explanation for a specific page.

        Returns:
            PageExplanation if cache hit, None if cache miss
        """
        stmt = select(PageExplanationCache).where(
            PageExplanationCache.pdf_id == pdf_id,
            PageExplanationCache.page_number == page_number,
        )
        result = await db.execute(stmt)
        cache_entry = result.scalar_one_or_none()

        if cache_entry:
            # Deserialize JSON to Pydantic model
            explanation_dict = json.loads(cache_entry.explanation_json)
            return PageExplanation(**explanation_dict)

        return None

    @staticmethod
    async def save_explanation(
        db: AsyncSession, pdf_id: str, page_number: int, explanation: PageExplanation
    ):
        """Save explanation to cache."""
        # Serialize Pydantic model to JSON
        explanation_json = explanation.model_dump_json()

        cache_entry = PageExplanationCache(
            pdf_id=pdf_id,
            page_number=page_number,
            page_type=explanation.page_type,
            explanation_json=explanation_json,
        )

        db.add(cache_entry)
        await db.commit()

    @staticmethod
    async def get_pdf_metadata(db: AsyncSession, pdf_id: str) -> PDFDocument | None:
        """Get PDF document metadata."""
        stmt = select(PDFDocument).where(PDFDocument.id == pdf_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def save_pdf_metadata(
        db: AsyncSession,
        pdf_id: str,
        filename: str,
        total_pages: int,
        file_path: str,
    ):
        """Save uploaded PDF metadata."""
        pdf_doc = PDFDocument(
            id=pdf_id,
            filename=filename,
            total_pages=total_pages,
            file_path=file_path,
        )
        db.add(pdf_doc)
        await db.commit()

    @staticmethod
    async def check_pdf_exists(db: AsyncSession, pdf_id: str) -> bool:
        """Check if PDF has been processed before."""
        stmt = select(PDFDocument).where(PDFDocument.id == pdf_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None


cache_service = CacheService()
