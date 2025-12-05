"""PDF parsing service using LlamaParse."""
import os
import hashlib
from pathlib import Path
from typing import List, Dict
from llama_parse import LlamaParse
from app.config import get_settings

settings = get_settings()


class PDFParserService:
    """Handles PDF parsing with LlamaParse."""

    def __init__(self):
        """Initialize LlamaParse client."""
        self.parser = LlamaParse(
            api_key=settings.llama_cloud_api_key,
            result_type="markdown",  # Get structured text
            language="mixed",  # Support French/English/Chinese
            verbose=True,
            show_progress=True,
        )

    async def parse_pdf(self, file_path: str) -> Dict[str, any]:
        """
        Parse PDF and return page-by-page content.

        Args:
            file_path: Absolute path to the PDF file

        Returns:
            {
                "pdf_id": "sha256_hash",
                "total_pages": 42,
                "pages": [
                    {
                        "page_number": 1,
                        "text": "extracted markdown text...",
                        "image_path": "temp/pdf_id_page_1.png"  # Optional
                    },
                    ...
                ]
            }
        """
        # Generate unique ID for this PDF
        pdf_id = self._generate_pdf_id(file_path)

        # Parse the PDF
        documents = await self.parser.aload_data(file_path)

        # LlamaParse returns a list of Document objects
        pages = []
        for idx, doc in enumerate(documents, start=1):
            page_data = {
                "page_number": idx,
                "text": doc.text,  # Markdown formatted text
                "metadata": doc.metadata,  # Contains page info
            }
            pages.append(page_data)

        return {
            "pdf_id": pdf_id,
            "total_pages": len(pages),
            "pages": pages,
        }

    async def parse_single_page(self, file_path: str, page_number: int) -> str:
        """
        Extract text from a specific page.

        Args:
            file_path: Path to PDF
            page_number: 1-indexed page number

        Returns:
            Extracted text in markdown format
        """
        # For efficiency, parse whole document once and cache
        # In production, you'd check cache first
        result = await self.parse_pdf(file_path)
        pages = result["pages"]

        if page_number < 1 or page_number > len(pages):
            raise ValueError(f"Page {page_number} out of range (1-{len(pages)})")

        return pages[page_number - 1]["text"]

    def _generate_pdf_id(self, file_path: str) -> str:
        """Generate SHA256 hash of PDF content for unique identification."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]  # Use first 16 chars

    def get_page_count(self, file_path: str) -> int:
        """Quick method to get total pages without full parsing."""
        from PyPDF2 import PdfReader

        reader = PdfReader(file_path)
        return len(reader.pages)


# Singleton instance
pdf_parser = PDFParserService()
